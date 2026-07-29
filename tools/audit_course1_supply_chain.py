"""Validate the Course 1 dependency inventory, SBOM, licences, and advisories.

The offline gate is deterministic and uses only the Python standard library.
The online gate verifies release metadata and vulnerability records through
PyPI and queries OSV for the exact pinned package versions. It never installs
a package.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import urllib.parse
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "supply_chain" / "course1-dependencies.json"
SBOM_PATH = ROOT / "supply_chain" / "course1-sbom.cdx.json"
PIN_PATTERN = re.compile(r"^([A-Za-z0-9_.-]+)==([^\s;]+)(?:\s+(.+))?$")
HASH_OPTION_PATTERN = re.compile(r"--hash=sha256:([0-9a-f]{64})")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
GIT_SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
REQUIREMENT_OPTIONS = {
    "--index-url=https://pypi.org/simple",
    "--only-binary=:all:",
    "--require-hashes",
}
CYCLONEDX_SCHEMA_URL = (
    "https://raw.githubusercontent.com/CycloneDX/specification/"
    "1.6/schema/bom-1.6.schema.json"
)


def normalize_name(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value).lower()


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{display_path(path)} must contain one JSON object")
    return value


def parse_requirements(path: Path) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    options: list[str] = []
    logical_lines: list[tuple[int, str]] = []
    buffer = ""
    buffer_start = 0
    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or (line.startswith("#") and not buffer):
            continue
        if not buffer:
            buffer_start = line_number
        if line.endswith("\\"):
            buffer += line[:-1].strip() + " "
            continue
        logical_lines.append((buffer_start, (buffer + line).strip()))
        buffer = ""
    if buffer:
        raise ValueError(f"{display_path(path)} ends in a continued line")

    for line_number, line in logical_lines:
        if line.startswith("--"):
            options.append(line)
            continue
        match = PIN_PATTERN.fullmatch(line)
        if not match:
            raise ValueError(
                f"{display_path(path)}:{line_number} is not one exact "
                "hash-bound pin"
            )
        name, version, hash_text = match.groups()
        hashes = HASH_OPTION_PATTERN.findall(hash_text or "")
        residual = HASH_OPTION_PATTERN.sub("", hash_text or "").strip()
        if residual or not hashes:
            raise ValueError(
                f"{display_path(path)}:{line_number} contains a missing "
                "or unsupported hash option"
            )
        if len(hashes) != len(set(hashes)):
            raise ValueError(
                f"{display_path(path)}:{line_number} repeats a SHA-256 hash"
            )
        normalized = normalize_name(name)
        if normalized in result:
            raise ValueError(
                f"{display_path(path)} repeats dependency {normalized}"
            )
        result[normalized] = {"version": version, "hashes": sorted(hashes)}

    if len(options) != len(set(options)) or set(options) != REQUIREMENT_OPTIONS:
        raise ValueError(
            f"{display_path(path)} must contain exactly the approved "
            "index, only-binary, and require-hashes options"
        )
    return result


def compare_requirement_hashes(
    pins: dict[str, dict[str, Any]],
    locked_by_name: dict[str, dict[str, Any]],
) -> list[str]:
    failures: list[str] = []
    for name, pin in pins.items():
        version = pin["version"]
        locked_hashes = {
            artifact["sha256"]
            for artifact in locked_by_name.get(name, {}).get("artifacts", [])
        }
        if set(pin["hashes"]) != locked_hashes:
            failures.append(
                "hashes differ from the complete artifact lock for "
                f"{name}=={version}"
            )
    return failures


def expected_sbom(
    manifest: dict[str, Any],
    artifact_lock: dict[str, Any],
    course_version: str,
) -> dict[str, Any]:
    components: list[dict[str, Any]] = []
    component_refs: list[str] = []
    locked_packages = {
        package["name"]: package for package in artifact_lock["packages"]
    }
    packages = sorted(
        manifest["packages"], key=lambda package: package["normalizedName"]
    )
    for package in packages:
        purl = f"pkg:pypi/{package['normalizedName']}@{package['version']}"
        component_refs.append(purl)
        artifacts = locked_packages[package["normalizedName"]]["artifacts"]
        components.append(
            {
                "type": "library",
                "bom-ref": purl,
                "name": package["name"],
                "version": package["version"],
                "purl": purl,
                "hashes": [
                    {
                        "alg": "SHA-256",
                        "content": digest,
                    }
                    for digest in sorted(
                        {artifact["sha256"] for artifact in artifacts}
                    )
                ],
                "licenses": [{"expression": package["licenseExpression"]}],
                "properties": [
                    {
                        "name": "course1:artifact",
                        "value": (
                            f"{artifact['filename']}|{artifact['packagetype']}|"
                            f"sha256:{artifact['sha256']}"
                        ),
                    }
                    for artifact in artifacts
                ],
            }
        )

    for action in sorted(
        manifest["githubActions"], key=lambda item: item["repository"]
    ):
        ref = f"pkg:github/{action['repository']}@{action['commit']}"
        component_refs.append(ref)
        components.append(
            {
                "type": "framework",
                "bom-ref": ref,
                "name": action["repository"],
                "version": action["commit"],
                "purl": ref,
                "licenses": [{"expression": action["licenseExpression"]}],
                "properties": [
                    {
                        "name": "course1:expected-release-tag",
                        "value": action["releaseTag"],
                    },
                    {
                        "name": "course1:full-commit-pin",
                        "value": action["commit"],
                    },
                ],
            }
        )

    for index, toolchain in enumerate(manifest["toolchains"], start=1):
        ref = f"course1-toolchain-{index}"
        component_refs.append(ref)
        components.append(
            {
                "type": toolchain["type"],
                "bom-ref": ref,
                "name": toolchain["name"],
                "version": toolchain["version"],
                "properties": [
                    {
                        "name": "course1:scope",
                        "value": toolchain["scope"],
                    }
                ],
            }
        )

    root_ref = "course1-controlled-ai-workflow-foundations"
    return {
        "$schema": "http://cyclonedx.org/schema/bom-1.6.schema.json",
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "version": 1,
        "metadata": {
            "component": {
                "type": "application",
                "bom-ref": root_ref,
                "name": "Course 1 Controlled AI Workflow Foundations",
                "version": course_version,
            },
            "properties": [
                {
                    "name": "course1:inventory-scope",
                    "value": (
                        "Course 1 Python, Node, GitHub Action, browser-test, "
                        "build, and continuous-integration dependencies"
                    ),
                },
                {
                    "name": "course1:node-external-dependency-count",
                    "value": str(
                        manifest["node"]["expectedExternalDependencyCount"]
                    ),
                },
            ],
        },
        "components": components,
        "dependencies": [{"ref": root_ref, "dependsOn": component_refs}],
        "compositions": [
            {
                "aggregate": "complete",
                "assemblies": component_refs,
            }
        ],
    }


def request_json_value(
    url: str, *, body: dict[str, Any] | None = None
) -> Any:
    data = None
    headers = {
        "Accept": "application/json",
        "User-Agent": "course1-supply-chain-audit/1",
    }
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def request_json(url: str, *, body: dict[str, Any] | None = None) -> dict[str, Any]:
    value = request_json_value(url, body=body)
    if not isinstance(value, dict):
        raise ValueError(f"{url} did not return one JSON object")
    return value


def license_value(info: dict[str, Any], evidence: dict[str, str]) -> Any:
    kind = evidence["kind"]
    if kind == "license_expression":
        return info.get("license_expression")
    if kind == "license":
        return info.get("license")
    if kind == "classifier":
        return evidence["value"] if evidence["value"] in info.get("classifiers", []) else None
    raise ValueError(f"unsupported licence-evidence kind: {kind}")


def validate_offline(
    manifest: dict[str, Any],
) -> tuple[list[str], list[dict[str, Any]]]:
    failures: list[str] = []
    inventory: list[dict[str, Any]] = []
    if manifest.get("schemaVersion") != 2:
        failures.append("dependency manifest schemaVersion must be 2")
    packages = manifest.get("packages")
    if not isinstance(packages, list) or not packages:
        return ["dependency manifest has no packages"], inventory

    try:
        verified_at = dt.date.fromisoformat(manifest["verifiedAt"])
        maximum_age = manifest["policy"]["maximumOnlineReportAgeDaysForRelease"]
        if not isinstance(maximum_age, int) or maximum_age < 1:
            raise ValueError(
                "maximumOnlineReportAgeDaysForRelease must be a positive integer"
            )
        age_days = (dt.date.today() - verified_at).days
        if age_days < 0:
            failures.append("dependency manifest verifiedAt is in the future")
        elif age_days > maximum_age:
            failures.append(
                "dependency evidence is stale: "
                f"{age_days} days exceeds {maximum_age}"
            )
    except (KeyError, TypeError, ValueError) as exc:
        failures.append(f"invalid dependency evidence freshness policy: {exc}")

    manifest_by_name: dict[str, dict[str, Any]] = {}
    allowed_licenses = set(manifest["policy"]["allowedLicenseExpressions"])
    for package in packages:
        if not isinstance(package, dict):
            failures.append("dependency manifest contains a non-object package")
            continue
        normalized = normalize_name(str(package.get("normalizedName", "")))
        if normalized != package.get("normalizedName"):
            failures.append(f"package has non-normalized name: {package.get('name')}")
            continue
        if normalized in manifest_by_name:
            failures.append(f"dependency manifest repeats {normalized}")
            continue
        manifest_by_name[normalized] = package
        license_expression = package.get("licenseExpression")
        if license_expression not in allowed_licenses:
            failures.append(
                f"{normalized} has unapproved licence expression {license_expression!r}"
            )
        sdist = package.get("sdist", {})
        if not SHA256_PATTERN.fullmatch(str(sdist.get("sha256", ""))):
            failures.append(f"{normalized} has no valid source-distribution SHA-256")
        inventory.append(
            {
                "name": normalized,
                "version": package.get("version"),
                "licenseExpression": license_expression,
                "sdistSha256": sdist.get("sha256"),
            }
        )

    artifact_lock_path = ROOT / str(manifest.get("pythonArtifactLock", ""))
    try:
        artifact_lock = read_json(artifact_lock_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        failures.append(f"invalid Python artifact lock: {exc}")
        artifact_lock = {"packages": [], "installationPolicy": {}}

    expected_lock_policy = {
        "indexUrl": manifest["policy"]["simpleIndex"],
        "requireHashes": True,
        "onlyBinary": ":all:",
        "allowYanked": False,
    }
    if artifact_lock.get("schemaVersion") != 1:
        failures.append("Python artifact lock schemaVersion must be 1")
    if artifact_lock.get("verifiedAt") != manifest.get("verifiedAt"):
        failures.append(
            "Python artifact lock verifiedAt differs from dependency manifest"
        )
    if artifact_lock.get("installationPolicy") != expected_lock_policy:
        failures.append("Python artifact lock installation policy is not closed")

    locked_by_name: dict[str, dict[str, Any]] = {}
    for locked_package in artifact_lock.get("packages", []):
        if not isinstance(locked_package, dict):
            failures.append("Python artifact lock contains a non-object package")
            continue
        name = str(locked_package.get("name", ""))
        if normalize_name(name) != name or name in locked_by_name:
            failures.append(f"Python artifact lock has invalid/repeated package {name!r}")
            continue
        artifacts = locked_package.get("artifacts")
        if not isinstance(artifacts, list) or not artifacts:
            failures.append(f"Python artifact lock has no artifacts for {name}")
            continue
        filenames: set[str] = set()
        hashes: set[str] = set()
        has_wheel = False
        for artifact in artifacts:
            if not isinstance(artifact, dict):
                failures.append(f"Python artifact lock has invalid artifact for {name}")
                continue
            filename = artifact.get("filename")
            packagetype = artifact.get("packagetype")
            digest = artifact.get("sha256")
            if (
                not isinstance(filename, str)
                or filename in filenames
                or packagetype not in {"bdist_wheel", "sdist"}
                or not SHA256_PATTERN.fullmatch(str(digest))
                or digest in hashes
            ):
                failures.append(
                    f"Python artifact lock has duplicate/malformed artifact for {name}"
                )
                continue
            filenames.add(filename)
            hashes.add(str(digest))
            has_wheel = has_wheel or packagetype == "bdist_wheel"
        if not has_wheel:
            failures.append(f"Python artifact lock has no allowed wheel for {name}")
        locked_by_name[name] = locked_package

    manifest_versions = {
        name: package["version"] for name, package in manifest_by_name.items()
    }
    locked_versions = {
        name: package.get("version") for name, package in locked_by_name.items()
    }
    if locked_versions != manifest_versions:
        failures.append("Python artifact lock differs from dependency manifest")

    requirements_union: dict[str, str] = {}
    expected_by_group = {
        "requirements-course.txt": "course1",
        "tools/requirements-validation.txt": "validator",
        "tools/requirements-maintainer.txt": "maintainer",
    }
    for relative_path in manifest["requirementFiles"]:
        path = ROOT / relative_path
        if not path.is_file():
            failures.append(f"required dependency file is missing: {relative_path}")
            continue
        try:
            pins = parse_requirements(path)
        except ValueError as exc:
            failures.append(str(exc))
            continue
        expected_group = expected_by_group.get(relative_path)
        if expected_group:
            expected_versions = {
                name: package["version"]
                for name, package in manifest_by_name.items()
                if expected_group in package["groups"]
            }
            actual_versions = {
                name: pin["version"] for name, pin in pins.items()
            }
            if actual_versions != expected_versions:
                failures.append(
                    f"{relative_path} differs from the {expected_group} manifest inventory"
                )
        for hash_failure in compare_requirement_hashes(pins, locked_by_name):
            failures.append(f"{relative_path} {hash_failure}")
        for name, pin in pins.items():
            version = pin["version"]
            previous = requirements_union.setdefault(name, version)
            if previous != version:
                failures.append(
                    f"{name} has conflicting pins {previous} and {version}"
                )

    if requirements_union != manifest_versions:
        failures.append("requirements union differs from dependency manifest")

    stack_text = (ROOT / "stack-manifest.yaml").read_text(encoding="utf-8")
    pytest_version = manifest_versions.get("pytest")
    if f'version_policy: "{pytest_version}"' not in stack_text:
        failures.append("stack-manifest.yaml does not match the pytest manifest pin")

    setup_text = (ROOT / "SETUP_WINDOWS.md").read_text(encoding="utf-8")
    if f"pytest=={pytest_version}" not in setup_text or f"pytest {pytest_version}" not in setup_text:
        failures.append("SETUP_WINDOWS.md does not match the pytest manifest pin")
    if "pytest==9.0.2" in setup_text or "pytest 9.0.2" in setup_text:
        failures.append("SETUP_WINDOWS.md still contains vulnerable pytest 9.0.2")

    node = manifest["node"]
    package_json = read_json(ROOT / node["packageManifest"])
    package_lock = read_json(ROOT / node["packageLock"])
    dependency_names: set[str] = set()
    for key in (
        "dependencies",
        "devDependencies",
        "optionalDependencies",
        "peerDependencies",
    ):
        values = package_json.get(key, {})
        if isinstance(values, dict):
            dependency_names.update(values)
    lock_packages = package_lock.get("packages", {})
    if isinstance(lock_packages, dict):
        dependency_names.update(
            name.removeprefix("node_modules/")
            for name in lock_packages
            if name.startswith("node_modules/")
        )
    if len(dependency_names) != node["expectedExternalDependencyCount"]:
        failures.append(
            "Node dependency inventory changed; update the manifest and SBOM intentionally"
        )

    declared_actions: dict[str, dict[str, Any]] = {}
    for action in manifest.get("githubActions", []):
        repository = str(action.get("repository", ""))
        commit = str(action.get("commit", ""))
        if (
            not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository)
            or repository in declared_actions
            or not GIT_SHA_PATTERN.fullmatch(commit)
            or not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", str(action.get("releaseTag", "")))
            or action.get("licenseExpression") not in allowed_licenses
        ):
            failures.append(f"invalid or duplicate GitHub Action inventory: {repository!r}")
            continue
        declared_actions[repository] = action

    used_actions: set[str] = set()
    workflow_paths = sorted((ROOT / ".github" / "workflows").glob("*.yml"))
    if not workflow_paths:
        failures.append("no GitHub Actions workflows were found")
    for workflow_path in workflow_paths:
        text = workflow_path.read_text(encoding="utf-8")
        if not re.search(r"(?m)^permissions:\s*$", text):
            failures.append(
                f"{workflow_path.relative_to(ROOT)} has no explicit workflow permissions"
            )
        if re.search(
            r"(?m)^\s*(?:write-all|contents:\s*write)\s*$|\bsecrets\.",
            text,
        ):
            failures.append(
                f"{workflow_path.relative_to(ROOT)} requests a prohibited "
                "broad permission or repository secret"
            )
        if re.search(r"(?m)^\s*runs-on:\s*\S*-latest\s*$", text):
            failures.append(
                f"{workflow_path.relative_to(ROOT)} uses an unbounded latest runner"
            )
        for match in re.finditer(
            r"(?m)^\s*uses:\s*"
            r"([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)@([0-9a-f]+)"
            r"(?:\s*#\s*(v[0-9]+\.[0-9]+\.[0-9]+))?\s*$",
            text,
        ):
            repository, commit, comment_tag = match.groups()
            used_actions.add(repository)
            declared = declared_actions.get(repository)
            if declared is None:
                failures.append(
                    f"{workflow_path.relative_to(ROOT)} uses undeclared Action "
                    f"{repository}"
                )
                continue
            if (
                commit != declared["commit"]
                or not GIT_SHA_PATTERN.fullmatch(commit)
                or comment_tag != declared["releaseTag"]
            ):
                failures.append(
                    f"{workflow_path.relative_to(ROOT)} Action pin/tag differs "
                    f"from the reviewed inventory for {repository}"
                )
        for line in re.findall(r"(?m)^\s*uses:\s*(\S+)", text):
            if not re.fullmatch(
                r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{40}", line
            ):
                failures.append(
                    f"{workflow_path.relative_to(ROOT)} has a non-full-SHA "
                    f"external Action reference: {line}"
                )
    if used_actions != set(declared_actions):
        failures.append(
            "GitHub Action inventory differs from workflow references"
        )

    toolchains = manifest.get("toolchains")
    if not isinstance(toolchains, list) or not toolchains:
        failures.append("toolchain inventory is empty")
    else:
        toolchain_keys: set[tuple[str, str, str, str]] = set()
        for item in toolchains:
            if not isinstance(item, dict):
                failures.append("toolchain inventory contains a non-object")
                continue
            key = (
                str(item.get("type", "")),
                str(item.get("name", "")),
                str(item.get("version", "")),
                str(item.get("scope", "")),
            )
            if not all(key) or key in toolchain_keys or "latest" in key[2].lower():
                failures.append(f"toolchain inventory has invalid/duplicate item: {key}")
            toolchain_keys.add(key)

    course_version = read_json(ROOT / "curriculum.json")["course"]["version"]
    sbom = read_json(SBOM_PATH)
    if sbom != expected_sbom(manifest, artifact_lock, course_version):
        failures.append("tracked CycloneDX SBOM differs from the dependency manifest")

    return failures, inventory


def validate_online(
    manifest: dict[str, Any],
) -> tuple[list[str], list[dict[str, Any]], dict[str, list[str]]]:
    failures: list[str] = []
    package_results: list[dict[str, Any]] = []
    packages = manifest["packages"]
    pypi_base = manifest["policy"]["packageIndex"].rstrip("/")
    artifact_lock = read_json(ROOT / manifest["pythonArtifactLock"])
    locked_by_name = {
        package["name"]: package for package in artifact_lock["packages"]
    }

    for package in packages:
        name = package["normalizedName"]
        version = package["version"]
        try:
            response = request_json(f"{pypi_base}/{name}/{version}/json")
            info = response.get("info", {})
            urls = response.get("urls", [])
            if str(info.get("version")) != version:
                failures.append(f"PyPI returned a different version for {name}")
            published_artifacts = {
                (
                    item.get("filename"),
                    item.get("packagetype"),
                    item.get("digests", {}).get("sha256"),
                )
                for item in urls
                if isinstance(item, dict)
                and not item.get("yanked", False)
                and item.get("packagetype") in {"bdist_wheel", "sdist"}
            }
            locked_artifacts = {
                (
                    item["filename"],
                    item["packagetype"],
                    item["sha256"],
                )
                for item in locked_by_name[name]["artifacts"]
            }
            if published_artifacts != locked_artifacts:
                failures.append(
                    f"official PyPI artifacts changed for {name}=={version}; "
                    "regenerate and review the lock"
                )
            expected_sdist = package["sdist"]
            matching = [
                item
                for item in urls
                if item.get("filename") == expected_sdist["filename"]
                and item.get("digests", {}).get("sha256") == expected_sdist["sha256"]
                and item.get("packagetype") == "sdist"
                and not item.get("yanked", False)
            ]
            if len(matching) != 1:
                failures.append(
                    f"PyPI source-distribution provenance mismatch for {name}=={version}"
                )
            pypi_vulnerabilities = response.get("vulnerabilities", [])
            if not isinstance(pypi_vulnerabilities, list):
                failures.append(
                    f"PyPI returned invalid vulnerability metadata for {name}=={version}"
                )
            elif pypi_vulnerabilities:
                identifiers = sorted(
                    {
                        str(item.get("id") or item.get("aliases") or "unknown")
                        for item in pypi_vulnerabilities
                        if isinstance(item, dict)
                    }
                )
                failures.append(
                    f"PyPI reports {name}=={version} vulnerabilities: {identifiers}"
                )
            evidence = package["licenseEvidence"]
            if license_value(info, evidence) != evidence["value"]:
                failures.append(
                    f"PyPI licence evidence changed for {name}=={version}"
                )
            package_results.append(
                {
                    "name": name,
                    "version": version,
                    "pypi": "PASS",
                    "license": package["licenseExpression"],
                    "sdistSha256": expected_sdist["sha256"],
                    "artifactCount": len(locked_artifacts),
                }
            )
        except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
            failures.append(f"PyPI verification failed for {name}=={version}: {exc}")

    query_body = {
        "queries": [
            {
                "package": {
                    "ecosystem": "PyPI",
                    "name": package["normalizedName"],
                },
                "version": package["version"],
            }
            for package in packages
        ]
    }
    vulnerabilities: dict[str, list[str]] = {}
    try:
        osv = request_json(manifest["policy"]["vulnerabilityApi"], body=query_body)
        results = osv.get("results")
        if not isinstance(results, list) or len(results) != len(packages):
            raise ValueError("OSV querybatch returned an unexpected result count")
        for package, result in zip(packages, results, strict=True):
            ids = sorted(
                {
                    str(vulnerability.get("id"))
                    for vulnerability in result.get("vulns", [])
                    if vulnerability.get("id")
                }
            )
            vulnerabilities[package["normalizedName"]] = ids
            if ids and manifest["policy"]["failOnAnyKnownVulnerability"]:
                failures.append(
                    f"OSV reports {package['normalizedName']}=={package['version']}: {ids}"
                )
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        failures.append(f"OSV verification failed: {exc}")

    github_advisory_base = manifest["policy"]["githubAdvisoryApi"]
    try:
        query = urllib.parse.urlencode(
            {
                "ecosystem": "pip",
                "affects": ",".join(
                    f"{package['normalizedName']}@{package['version']}"
                    for package in packages
                ),
                "per_page": "100",
            }
        )
        advisories = request_json_value(f"{github_advisory_base}?{query}")
        if not isinstance(advisories, list):
            raise ValueError("GitHub pip advisory query returned a non-list")
        ids = sorted(
            {
                str(item.get("ghsa_id"))
                for item in advisories
                if isinstance(item, dict) and item.get("ghsa_id")
            }
        )
        vulnerabilities["github:pip"] = ids
        if ids and manifest["policy"]["failOnAnyKnownVulnerability"]:
            failures.append(f"GitHub advisories affect the Python lock: {ids}")
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        failures.append(f"GitHub pip advisory verification failed: {exc}")

    actions = manifest["githubActions"]
    try:
        query = urllib.parse.urlencode(
            {
                "ecosystem": "actions",
                "affects": ",".join(
                    f"{action['repository']}@{action['releaseTag']}"
                    for action in actions
                ),
                "per_page": "100",
            }
        )
        advisories = request_json_value(f"{github_advisory_base}?{query}")
        if not isinstance(advisories, list):
            raise ValueError("GitHub Actions advisory query returned a non-list")
        ids = sorted(
            {
                str(item.get("ghsa_id"))
                for item in advisories
                if isinstance(item, dict) and item.get("ghsa_id")
            }
        )
        vulnerabilities["github:actions"] = ids
        if ids and manifest["policy"]["failOnAnyKnownVulnerability"]:
            failures.append(f"GitHub advisories affect the Action inventory: {ids}")
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        failures.append(f"GitHub Actions advisory verification failed: {exc}")

    for action in actions:
        repository = action["repository"]
        tag = action["releaseTag"]
        try:
            resolved = request_json(
                f"https://api.github.com/repos/{repository}/commits/{tag}"
            )
            if resolved.get("sha") != action["commit"]:
                failures.append(
                    f"{repository} {tag} no longer resolves to the reviewed commit"
                )
        except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
            failures.append(
                f"GitHub Action provenance failed for {repository}@{tag}: {exc}"
            )

    try:
        schema = request_json(CYCLONEDX_SCHEMA_URL)
        sbom = read_json(SBOM_PATH)
        try:
            import jsonschema
        except ImportError as exc:
            raise ValueError(
                "online SBOM validation requires the hash-locked validator "
                "dependency set"
            ) from exc
        jsonschema.validate(instance=sbom, schema=schema)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        failures.append(f"CycloneDX schema validation failed: {exc}")
    except Exception as exc:  # jsonschema exposes version-specific error classes
        failures.append(f"CycloneDX schema validation failed: {exc}")

    return failures, package_results, vulnerabilities


def write_report(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--online",
        action="store_true",
        help="also verify PyPI provenance/licences and query OSV",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help="optional machine-readable JSON report path",
    )
    args = parser.parse_args()

    failures: list[str] = []
    online_packages: list[dict[str, Any]] = []
    vulnerabilities: dict[str, list[str]] = {}
    try:
        manifest = read_json(MANIFEST_PATH)
        offline_failures, inventory = validate_offline(manifest)
        failures.extend(offline_failures)
        if args.online:
            online_failures, online_packages, vulnerabilities = validate_online(
                manifest
            )
            failures.extend(online_failures)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        inventory = []
        failures.append(str(exc))

    report = {
        "schemaVersion": 2,
        "checkedAt": dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "onlineChecksPerformed": bool(args.online),
        "result": "PASS" if not failures else "FAIL",
        "inventory": inventory,
        "artifacts": {
            "dependencyManifest": {
                "path": str(MANIFEST_PATH.relative_to(ROOT)),
                "sha256": sha256_file(MANIFEST_PATH),
            },
            "pythonArtifactLock": {
                "path": manifest.get("pythonArtifactLock")
                if "manifest" in locals()
                else None,
                "sha256": sha256_file(
                    ROOT / manifest["pythonArtifactLock"]
                )
                if "manifest" in locals()
                else None,
            },
            "sbom": {
                "path": str(SBOM_PATH.relative_to(ROOT)),
                "sha256": sha256_file(SBOM_PATH),
            },
            "requirementFiles": [
                {
                    "path": path,
                    "sha256": sha256_file(ROOT / path),
                }
                for path in manifest.get("requirementFiles", [])
            ]
            if "manifest" in locals()
            else [],
        },
        "onlinePackages": online_packages,
        "vulnerabilities": vulnerabilities,
        "failures": failures,
    }
    if args.report:
        write_report(args.report.resolve(), report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
