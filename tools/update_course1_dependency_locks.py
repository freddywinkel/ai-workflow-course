"""Regenerate Course 1 hash-required Python locks from official PyPI metadata.

This maintainer-only tool deliberately keeps learner and validator dependency
sets separate. It records every non-yanked distribution published for each
exact pinned version, then writes pip requirement files that:

* use the intended PyPI Simple API;
* reject source distributions during installation;
* require a locally recorded SHA-256 hash for every installed wheel; and
* spell out every direct and transitive dependency.

Run this only as an intentional dependency review. Regeneration is not proof
that the new dependency set is acceptable: the supply-chain audit, clean
installs, test matrix, licence review, and advisory checks must follow.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "supply_chain" / "course1-dependencies.json"
ARTIFACT_LOCK_PATH = ROOT / "supply_chain" / "python-artifact-lock.json"
SBOM_PATH = ROOT / "supply_chain" / "course1-sbom.cdx.json"
PYPI_JSON_BASE = "https://pypi.org/pypi"
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


def normalize_name(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value).lower()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain one JSON object")
    return value


def fetch_release(name: str, version: str) -> dict[str, Any]:
    safe_name = urllib.parse.quote(name, safe="")
    safe_version = urllib.parse.quote(version, safe="")
    url = f"{PYPI_JSON_BASE}/{safe_name}/{safe_version}/json"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "course1-dependency-lock-maintainer/1",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        value = json.loads(response.read().decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{url} did not return one JSON object")
    return value


def build_artifact_lock(
    manifest: dict[str, Any], *, verified_at: str
) -> dict[str, Any]:
    packages: list[dict[str, Any]] = []
    for package in sorted(
        manifest["packages"], key=lambda item: item["normalizedName"]
    ):
        name = package["normalizedName"]
        version = package["version"]
        release = fetch_release(name, version)
        if str(release.get("info", {}).get("version")) != version:
            raise ValueError(f"PyPI returned a different version for {name}")

        artifacts: list[dict[str, str]] = []
        for item in release.get("urls", []):
            if not isinstance(item, dict) or item.get("yanked", False):
                continue
            filename = item.get("filename")
            packagetype = item.get("packagetype")
            sha256 = item.get("digests", {}).get("sha256")
            if (
                not isinstance(filename, str)
                or packagetype not in {"bdist_wheel", "sdist"}
                or not isinstance(sha256, str)
                or not SHA256_PATTERN.fullmatch(sha256)
            ):
                raise ValueError(
                    f"PyPI returned incomplete artifact metadata for {name}=={version}"
                )
            artifacts.append(
                {
                    "filename": filename,
                    "packagetype": packagetype,
                    "sha256": sha256,
                }
            )
        artifacts.sort(key=lambda item: item["filename"])
        if not artifacts:
            raise ValueError(f"PyPI returned no accepted artifacts for {name}=={version}")
        if not any(item["packagetype"] == "bdist_wheel" for item in artifacts):
            raise ValueError(f"{name}=={version} has no wheel; source builds are prohibited")

        packages.append(
            {
                "name": name,
                "version": version,
                "artifacts": artifacts,
            }
        )

    return {
        "schemaVersion": 1,
        "source": "https://pypi.org/pypi/<package>/<version>/json",
        "verifiedAt": verified_at,
        "installationPolicy": {
            "indexUrl": "https://pypi.org/simple",
            "requireHashes": True,
            "onlyBinary": ":all:",
            "allowYanked": False,
        },
        "packages": packages,
    }


def render_requirements(
    manifest: dict[str, Any],
    artifact_lock: dict[str, Any],
    *,
    group: str,
) -> str:
    package_metadata = {
        item["normalizedName"]: item for item in manifest["packages"]
    }
    artifact_metadata = {
        item["name"]: item for item in artifact_lock["packages"]
    }
    selected = sorted(
        (
            item
            for item in manifest["packages"]
            if group in item.get("groups", [])
        ),
        key=lambda item: item["normalizedName"],
    )
    lines = [
        "# Hash-required Course 1 dependency lock.",
        "# Generated by tools/update_course1_dependency_locks.py from official",
        "# PyPI release metadata. Maintainers must review, audit, and test any change.",
        "--index-url=https://pypi.org/simple",
        "--only-binary=:all:",
        "--require-hashes",
        "",
    ]
    for selected_package in selected:
        name = selected_package["normalizedName"]
        package = package_metadata[name]
        artifacts = artifact_metadata[name]["artifacts"]
        hashes = sorted({item["sha256"] for item in artifacts})
        lines.append(f"{package['name']}=={package['version']} \\")
        for index, digest in enumerate(hashes):
            suffix = " \\" if index < len(hashes) - 1 else ""
            lines.append(f"    --hash=sha256:{digest}{suffix}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--verified-at",
        default=dt.date.today().isoformat(),
        help="ISO date on which official PyPI metadata was reviewed",
    )
    args = parser.parse_args()
    dt.date.fromisoformat(args.verified_at)

    manifest = read_json(MANIFEST_PATH)
    artifact_lock = build_artifact_lock(manifest, verified_at=args.verified_at)
    write_json(ARTIFACT_LOCK_PATH, artifact_lock)
    (ROOT / "requirements-course.txt").write_text(
        render_requirements(manifest, artifact_lock, group="course1"),
        encoding="utf-8",
        newline="\n",
    )
    (ROOT / "tools" / "requirements-validation.txt").write_text(
        render_requirements(manifest, artifact_lock, group="validator"),
        encoding="utf-8",
        newline="\n",
    )
    (ROOT / "tools" / "requirements-maintainer.txt").write_text(
        render_requirements(manifest, artifact_lock, group="maintainer"),
        encoding="utf-8",
        newline="\n",
    )
    from audit_course1_supply_chain import expected_sbom

    course_version = read_json(ROOT / "curriculum.json")["course"]["version"]
    write_json(
        SBOM_PATH,
        expected_sbom(manifest, artifact_lock, course_version),
    )
    print(
        "Updated the Python artifact lock, all hash-required requirement "
        "files, and the CycloneDX SBOM"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
