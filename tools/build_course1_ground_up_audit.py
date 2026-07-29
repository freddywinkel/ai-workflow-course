#!/usr/bin/env python3
"""Build the conservative Course 1 ground-up audit artifact package.

This records the current working copy. It never upgrades local results to an
immutable-candidate, human, repository, installed-client, or production pass.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import locale
import platform
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


COURSE_ID = "course-1-controlled-ai-workflow-foundations"
SCHEMA_VERSION = "course1-ground-up-audit-artifact-v1"
MACHINE_FILES = (
    "scope-and-authority.json",
    "baseline-file-inventory.json",
    "normative-id-inventory.json",
    "requirement-test-evidence-graph.json",
    "test-and-scenario-manifest.json",
    "change-to-evidence-map.json",
    "environment-and-toolchain.json",
    "raw-evidence-index.json",
    "audit-assurance-result.json",
)
MARKDOWN_FILES = (
    "pre-repair-findings.md",
    "audit-gap-review.md",
    "repair-and-invalidation-record.md",
    "independent-review-and-adjudication.md",
    "final-decision.md",
)
EXPECTED_RAW = (
    ("C1-RAW-TOOLS", "Complete Python tools suite", "AUTOMATED_LOCAL"),
    ("C1-RAW-PACKAGE", "Complete Course 1 package validation", "AUTOMATED_LOCAL"),
    ("C1-RAW-PY312", "Fresh Python 3.12 clean-room run", "NATIVE_WINDOWS"),
    ("C1-RAW-PY313", "Fresh Python 3.13 clean-room run", "NATIVE_WINDOWS"),
    ("C1-RAW-PY314", "Fresh Python 3.14 clean-room run", "NATIVE_WINDOWS"),
    ("C1-RAW-NODE", "Exact Node unit suite", "AUTOMATED_LOCAL"),
    ("C1-RAW-CHROME", "Fresh-profile Chrome browser smoke", "REAL_BROWSER"),
    ("C1-RAW-EDGE", "Fresh-profile Edge browser smoke", "REAL_BROWSER"),
    ("C1-RAW-QUALITY", "Coverage, property, mutation and negative-control gate", "AUTOMATED_LOCAL"),
    ("C1-RAW-SUPPLY", "Online supply-chain audit", "REPOSITORY"),
    ("C1-RAW-SOURCES", "Online and manual source review", "MANUAL_SOURCE"),
    ("C1-RAW-BEGINNER", "Literal-beginner completion evidence", "LEARNER"),
    ("C1-RAW-UAT", "Independent assessment and real synthetic UAT", "ASSESSOR_UAT"),
    ("C1-RAW-SPECIALIST", "Practitioner, legal/privacy and security review", "PRACTITIONER_LEGAL_SECURITY"),
    ("C1-RAW-ACCESSIBILITY", "Device and assistive-technology evidence", "ACCESSIBILITY_DEVICE"),
    ("C1-RAW-REPOSITORY", "Repository protection and workflow evidence", "REPOSITORY"),
    ("C1-RAW-INSTALLED", "Installed old-client update and state preservation", "INSTALLED_CLIENT"),
    ("C1-RAW-PRODUCTION", "Public bytes, live checks and rollback", "PRODUCTION"),
)


def load_json(path: Path) -> dict[str, Any]:
    def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"{path}: duplicate JSON key {key!r}")
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def git(root: Path, *args: str) -> bytes:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout


def git_text(root: Path, *args: str) -> str:
    return git(root, *args).decode("utf-8", errors="strict").strip()


def normalise_git_branch(branch: str) -> str:
    """Give detached commits an explicit, non-branch provenance label."""

    return branch or "DETACHED_HEAD"


def common(course_version: str, audit_date: str, artifact_type: str) -> dict[str, Any]:
    return {
        "schemaVersion": SCHEMA_VERSION,
        "artifactType": artifact_type,
        "auditId": f"C1-GROUND-UP-{audit_date}",
        "courseId": COURSE_ID,
        "courseVersion": course_version,
        "auditDate": audit_date,
    }


def classify(path: str) -> str:
    if path == ".github/workflows/course4-offline.yml":
        return "COURSE4_ONLY"
    if path.startswith(("advanced_capstone/", "future_courses/course_04_")):
        return "COURSE4_ONLY"
    if path == "curriculum.json" or path.startswith("app/") or path == ".github/workflows/pages.yml":
        return "SHARED_COURSE_READER"
    if path in {
        "AGENTS.md",
        "README.md",
        "STRATEGIC_FOCUS.md",
        "CAREER_SEQUENCE.md",
        "COURSE_CHANGELOG.md",
        "PWA_AND_UPDATES.md",
        "RELEASE_VALIDATION.md",
    }:
        return "SHARED_GOVERNANCE"
    return "COURSE1_ONLY"


def snapshot_files(root: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    tracked = set(filter(None, git(root, "ls-files", "-z").decode().split("\0")))
    untracked = set(
        filter(
            None,
            git(root, "ls-files", "--others", "--exclude-standard", "-z")
            .decode()
            .split("\0"),
        )
    )
    output_prefix = "release_evidence/course1_ground_up_audit/"
    tracked = {p for p in tracked if not p.startswith(output_prefix)}
    untracked = {p for p in untracked if not p.startswith(output_prefix)}
    changed = set(
        filter(
            None,
            git(root, "diff", "--name-only", "-z", "HEAD", "--").decode().split("\0"),
        )
    )
    deleted = set(
        filter(
            None,
            git(root, "diff", "--diff-filter=D", "--name-only", "-z", "HEAD", "--")
            .decode()
            .split("\0"),
        )
    )
    rows: list[dict[str, Any]] = []
    for relative in sorted(tracked | untracked):
        path = root / relative
        if relative in untracked:
            status = "UNTRACKED"
        elif relative in deleted:
            status = "TRACKED_DELETED"
        elif relative in changed:
            status = "TRACKED_MODIFIED"
        else:
            status = "TRACKED_UNCHANGED"
        current = path.read_bytes() if path.is_file() else None
        if relative in tracked:
            if status == "TRACKED_UNCHANGED" and current is not None:
                head_hash = sha256_bytes(current)
            else:
                head_hash = sha256_bytes(git(root, "show", f"HEAD:{relative}"))
        else:
            head_hash = None
        rows.append(
            {
                "path": relative,
                "classification": classify(relative),
                "workingTreeStatus": status,
                "headSha256": head_hash,
                "currentSha256": sha256_bytes(current) if current is not None else None,
                "currentSizeBytes": len(current) if current is not None else None,
            }
        )
    metadata = {
        "branch": normalise_git_branch(
            git_text(root, "branch", "--show-current")
        ),
        "headCommit": git_text(root, "rev-parse", "HEAD"),
        "headTree": git_text(root, "rev-parse", "HEAD^{tree}"),
        "dirty": any(row["workingTreeStatus"] != "TRACKED_UNCHANGED" for row in rows),
        "trackedChangeCount": sum(
            row["workingTreeStatus"].startswith("TRACKED_")
            and row["workingTreeStatus"] != "TRACKED_UNCHANGED"
            for row in rows
        ),
        "untrackedCount": sum(row["workingTreeStatus"] == "UNTRACKED" for row in rows),
    }
    return rows, metadata


def file_ref(root: Path, relative: str) -> dict[str, str]:
    path = root / relative
    if not path.is_file():
        raise ValueError(f"required authority is missing: {relative}")
    return {"path": relative, "sha256": sha256_file(path)}


def validated_unique_ids(text: str, pattern: str, family: str) -> list[str]:
    raw_ids = sorted(re.findall(pattern, text))
    duplicates = sorted(
        {identifier for identifier in raw_ids if raw_ids.count(identifier) > 1}
    )
    malformed = [
        identifier
        for identifier in raw_ids
        if re.fullmatch(pattern, identifier) is None
    ]
    if not raw_ids or duplicates or malformed:
        raise ValueError(
            f"{family} ID inventory failed: duplicates={duplicates}, "
            f"malformed={malformed}, count={len(raw_ids)}"
        )
    return sorted(set(raw_ids))


def validated_exact_sequence(ids: list[str], prefix: str, count: int) -> list[str]:
    expected = [f"{prefix}-{number:03d}" for number in range(1, count + 1)]
    if ids != expected:
        raise ValueError(
            f"{prefix} ledger inventory must be exactly {expected}; found {ids}"
        )
    return ids


def build_id_inventory(root: Path, files: list[dict[str, Any]]) -> dict[str, Any]:
    threat_path = root / "COURSE_1_PRODUCT_THREAT_MODEL.md"
    protocol_path = root / "COURSE_1_GROUND_UP_AUDIT_PROTOCOL.md"
    ledger_path = root / "COURSE_1_AUDIT_STATUS_AND_REPAIR_LEDGER.md"
    threat = threat_path.read_text(encoding="utf-8")
    protocol = protocol_path.read_text(encoding="utf-8")
    ledger = ledger_path.read_text(encoding="utf-8")
    graph = load_json(root / "audit_control/course1/technical_requirement_graph.json")
    learning = load_json(root / "audit_control/course1/learning_claim_evidence_matrix.json")
    negative = load_json(root / "quality/negative-control-manifest.json")
    mutation = load_json(root / "quality/mutation-manifest.json")
    families: list[tuple[str, str, str, list[str]]] = []
    for name, token in (
        ("THREAT_SCOPE_PRIVACY", "TM"),
        ("ASSET", "AST"),
        ("ACTOR", "ACT"),
        ("TRUST_BOUNDARY", "TB"),
        ("INVARIANT", "INV"),
        ("THREAT", "THR"),
        ("ABUSE", "ABUSE"),
        ("RESIDUAL_RISK", "RSK"),
    ):
        pattern = rf"C1-{token}(?:-[A-Z]+)?-[0-9]{{3}}"
        families.append(
            (
                name,
                pattern,
                threat_path.name,
                validated_unique_ids(threat, pattern, name),
            )
        )
    families.extend(
        [
            (
                "TECHNICAL_REQUIREMENT",
                r"C1-TA-(?:[A-Z0-9]+-)+[0-9]{3}",
                "audit_control/course1/technical_requirement_graph.json",
                sorted(row["id"] for row in graph["requirements"]),
            ),
            (
                "TECHNICAL_TEST",
                r"C1-TST-(?:[A-Z0-9]+-)+[0-9]{3}",
                "audit_control/course1/technical_requirement_graph.json",
                sorted(row["id"] for row in graph["tests"]),
            ),
            (
                "LEARNING_REQUIREMENT",
                r"C1-LV-[0-9]{3}",
                "audit_control/course1/learning_claim_evidence_matrix.json",
                sorted(row["requirementId"] for row in learning["requirements"]),
            ),
            (
                "LEARNING_METHOD",
                r"C1-LVM-[0-9]{3}",
                "audit_control/course1/learning_claim_evidence_matrix.json",
                sorted(
                    method["methodId"]
                    for row in learning["requirements"]
                    for method in row["assessmentMethods"]
                ),
            ),
            (
                "TECHNICAL_FINDING",
                r"C1-TECH-[0-9]{3}",
                ledger_path.name,
                validated_exact_sequence(
                    re.findall(
                        r"^\| `(C1-TECH-[0-9]{3})` \|", ledger, re.MULTILINE
                    ),
                    "C1-TECH",
                    6,
                ),
            ),
            (
                "CONTENT_FINDING",
                r"C1-CONT-[0-9]{3}",
                ledger_path.name,
                validated_exact_sequence(
                    re.findall(
                        r"^\| `(C1-CONT-[0-9]{3})` \|", ledger, re.MULTILINE
                    ),
                    "C1-CONT",
                    9,
                ),
            ),
            (
                "GOVERNANCE_FINDING",
                r"C1-GOV-[0-9]{3}",
                ledger_path.name,
                validated_exact_sequence(
                    re.findall(
                        r"^\| `(C1-GOV-[0-9]{3})` \|", ledger, re.MULTILINE
                    ),
                    "C1-GOV",
                    15,
                ),
            ),
            (
                "AUDIT_ASSURANCE",
                r"C1-AA-[0-9]{3}",
                protocol_path.name,
                re.findall(r"^\| `(C1-AA-[0-9]{3})` \|", protocol, re.MULTILINE),
            ),
            (
                "NEGATIVE_CONTROL",
                r"C1-NEG-[A-Z0-9-]+-[0-9]{3}",
                "quality/negative-control-manifest.json",
                sorted(row["id"] for row in negative["controls"]),
            ),
            (
                "MUTATION",
                r"C1-MUT-[A-Z0-9-]+-[0-9]{3}",
                "quality/mutation-manifest.json",
                sorted(row["id"] for row in mutation["mutants"]),
            ),
        ]
    )
    duplicates: list[str] = []
    malformed: list[str] = []
    family_rows = []
    for name, pattern, authority, ids in families:
        if len(ids) != len(set(ids)):
            duplicates.extend(identifier for identifier in ids if ids.count(identifier) > 1)
        if not ids or any(re.fullmatch(pattern, identifier) is None for identifier in ids):
            malformed.append(name)
        family_rows.append(
            {
                "family": name,
                "pattern": f"^{pattern}$",
                "authorityPath": authority,
                "count": len(ids),
                "ids": ids,
            }
        )
    if duplicates or malformed:
        raise ValueError(f"normative ID inventory failed: duplicates={duplicates}, malformed={malformed}")

    in_scope = [
        row["path"] for row in files if row["classification"] != "COURSE4_ONLY"
    ]
    resource_groups = [
        {
            "kind": "SCHEMAS",
            "paths": sorted(path for path in in_scope if path.endswith(".schema.json")),
        },
        {
            "kind": "FIXTURES_AND_ORACLES",
            "paths": sorted(
                path
                for path in in_scope
                if "/fixtures/" in path
                or path in {"practice_data/work_items.csv", "practice_data/expected_issues.csv"}
            ),
        },
        {
            "kind": "TEMPLATES",
            "paths": sorted(path for path in in_scope if path.startswith("templates/")),
        },
        {
            "kind": "WORKFLOWS",
            "paths": sorted(path for path in in_scope if path.startswith(".github/workflows/")),
        },
        {
            "kind": "DEPENDENCY_LOCKS_AND_SBOM",
            "paths": sorted(
                path
                for path in in_scope
                if "requirements" in Path(path).name.lower()
                or path.endswith("package-lock.json")
                or path.startswith("supply_chain/")
            ),
        },
        {
            "kind": "SOURCE_CLAIMS",
            "paths": ["source_claims.json"],
        },
        {
            "kind": "PWA_STATE_AND_CACHE_IDENTIFIERS",
            "paths": [
                "app/src/app.js::ai-workflow-course-state-v1",
                "app/src/app.js::ai-workflow-course-recovery-v1",
                "app/src/app.js::ai-workflow-course-reset-barrier-v1",
                "app/src/sw.js::ai-workflow-course-",
            ],
        },
    ]
    authorities = [
        "AGENTS.md",
        "STRATEGIC_FOCUS.md",
        "COURSE_1_GROUND_UP_AUDIT_PROTOCOL.md",
        "COURSE_1_PRODUCT_THREAT_MODEL.md",
        "COURSE_1_TECHNICAL_ACCEPTANCE_CONTRACT.md",
        "COURSE_1_LEARNING_VALIDATION_CONTRACT.md",
        "COURSE_1_AUDIT_STATUS_AND_REPAIR_LEDGER.md",
        "RELEASE_VALIDATION.md",
        "ROLLBACK_RUNBOOK.md",
    ]
    return {
        "authorities": [file_ref(root, path) for path in authorities],
        "idFamilies": family_rows,
        "resourceGroups": resource_groups,
        "duplicateIds": [],
        "unparsedOrMalformedIds": [],
        "structuralStatus": "PASS",
        "candidateEvidenceStatus": "UNVERIFIED",
    }


def build_graph(root: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    graph = load_json(root / "audit_control/course1/technical_requirement_graph.json")
    manifest = load_json(root / "audit_control/course1/technical_test_manifest.json")
    learning = load_json(root / "audit_control/course1/learning_claim_evidence_matrix.json")
    manifest_by_id = {row["id"]: row for row in manifest["tests"]}
    reverse = {row["id"]: sorted(row["requirements"]) for row in graph["tests"]}
    technical_tests = []
    for test_id in sorted(manifest_by_id):
        row = manifest_by_id[test_id]
        if row["currentEvidence"] != {"status": "UNVERIFIED", "records": []}:
            raise ValueError(f"{test_id}: ground-up package requires honest UNVERIFIED evidence")
        technical_tests.append(
            {
                "id": test_id,
                "owner": row["owner"],
                "type": row["type"],
                "environments": sorted(row["environments"]),
                "evidenceClass": row["evidenceClass"],
                "requirements": reverse[test_id],
                "procedures": row["procedures"],
                "currentEvidenceStatus": "UNVERIFIED",
            }
        )
    requirements = [
        {
            "id": row["id"],
            "family": row["family"],
            "owner": "Course 1 technical contract owner",
            "testIds": sorted(row["tests"]),
        }
        for row in sorted(graph["requirements"], key=lambda item: item["id"])
    ]
    learning_requirements = []
    learning_methods = []
    for row in sorted(learning["requirements"], key=lambda item: item["requirementId"]):
        if row["currentEvidence"] != {"status": "UNVERIFIED", "records": []}:
            raise ValueError(f"{row['requirementId']}: expected UNVERIFIED learning evidence")
        methods = row["assessmentMethods"]
        learning_requirements.append(
            {
                "id": row["requirementId"],
                "owner": row["owner"],
                "claim": row["claim"],
                "methodIds": sorted(method["methodId"] for method in methods),
                "evidenceClasses": sorted(row["evidenceClasses"]),
                "limitation": row["limitation"],
                "currentEvidenceStatus": "UNVERIFIED",
            }
        )
        for method in methods:
            learning_methods.append(
                {
                    "id": method["methodId"],
                    "requirementId": row["requirementId"],
                    "type": method["type"],
                    "locator": method["locator"],
                    "selector": method["selector"],
                    "environment": method["environment"],
                    "passCondition": method["passCondition"],
                }
            )
    graph_body = {
        "canonicalReferences": [
            file_ref(root, "audit_control/course1/technical_requirement_graph.json"),
            file_ref(root, "audit_control/course1/technical_test_manifest.json"),
            file_ref(root, "audit_control/course1/learning_claim_evidence_matrix.json"),
        ],
        "technicalRequirements": requirements,
        "technicalTests": technical_tests,
        "learningRequirements": learning_requirements,
        "learningMethods": sorted(learning_methods, key=lambda item: item["id"]),
        "technicalEdgeCount": sum(len(row["testIds"]) for row in requirements),
        "structuralStatus": "PASS",
        "candidateEvidenceStatus": "UNVERIFIED",
    }
    return graph_body, technical_tests, sorted(learning_methods, key=lambda item: item["id"])


def invalidated_families(path: str, classification: str) -> list[str]:
    if classification == "COURSE4_ONLY":
        return ["COURSE4_ONLY"]
    families = {"CANDIDATE_IDENTITY", "PACKAGE_VALIDATION"}
    if path.startswith("app/") or path == "curriculum.json":
        families.update({"PWA_BUILD", "BROWSER", "SERVICE_WORKER"})
    if path.startswith(("course1_capstone/", "schemas/", "practice_data/")):
        families.update({"RUNNER", "CLEANROOM"})
    if path.startswith(("tools/", "audit_control/", "quality/")):
        families.update({"AUDIT_CONTROL", "INTEGRATED_SUITE"})
    if path.startswith(".github/") or "requirements" in path or path.startswith("supply_chain/"):
        families.update({"SUPPLY_CHAIN", "REPOSITORY"})
    if path.endswith(".md") or path == "curriculum.json":
        families.update({"LEARNING_CONTENT", "PWA_BUILD"})
    return sorted(families)


def raw_evidence(
    output: Path,
    manifest_path: Path | None,
    dirty: bool,
    head_commit: str,
    audit_schema: dict[str, Any],
) -> list[dict[str, Any]]:
    supplied: dict[str, dict[str, Any]] = {}
    if manifest_path:
        manifest = load_json(manifest_path)
        rows = validate_raw_evidence_manifest(manifest, manifest_path)
        input_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$ref": "#/$defs/rawEvidenceInputManifest",
            "$defs": audit_schema["$defs"],
        }
        errors = sorted(
            Draft202012Validator(
                input_schema, format_checker=FormatChecker()
            ).iter_errors(manifest),
            key=lambda error: list(error.absolute_path),
        )
        if errors:
            raise ValueError(
                f"{manifest_path}: raw evidence schema validation failed: "
                + "; ".join(error.message for error in errors)
            )
        supplied = {row["id"]: row for row in rows}
    raw_candidate = (output / "raw").resolve(strict=False)
    for row in supplied.values():
        source = Path(row["path"]).resolve()
        if source == raw_candidate or raw_candidate in source.parents:
            raise ValueError(
                "raw evidence input must be outside the generator-owned output/raw directory"
            )
    raw_dir = clear_owned_raw_directory(output)
    entries = []
    for evidence_id, label, evidence_class in EXPECTED_RAW:
        item = supplied.get(evidence_id)
        if not item:
            entries.append(
                {
                    "id": evidence_id,
                    "label": label,
                    "evidenceClass": evidence_class,
                    "result": "UNVERIFIED",
                    "path": None,
                    "exists": False,
                    "sha256": None,
                    "candidateBinding": "UNBOUND_WORKING_COPY",
                    "commandOrProcedure": None,
                    "environment": None,
                    "reviewer": None,
                    "recordedAt": None,
                    "reason": "No raw evidence input was supplied; no result is inferred.",
                }
            )
            continue
        source = Path(item["path"]).resolve()
        suffix = source.suffix.lower() if source.suffix.lower() in {".json", ".md", ".txt"} else ".log"
        destination = raw_dir / f"{evidence_id.lower()}{suffix}"
        raw_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        requested_binding = item.get("candidateBinding", "UNBOUND_WORKING_COPY")
        valid_candidate = (
            requested_binding == "IMMUTABLE_CANDIDATE"
            and not dirty
            and item.get("candidateCommit") == head_commit
        )
        result = item.get("result", "UNVERIFIED")
        if requested_binding in {"IMMUTABLE_CANDIDATE", "PUBLIC_ARTIFACT"} and not valid_candidate:
            result = "UNVERIFIED"
            reason = "The supplied file exists, but its claimed immutable/public binding is not valid for this dirty working copy."
            binding = "UNBOUND_WORKING_COPY"
        else:
            reason = item.get("reason", "Supplied local evidence; not release acceptance.")
            binding = requested_binding
        entries.append(
            {
                "id": evidence_id,
                "label": label,
                "evidenceClass": evidence_class,
                "result": result,
                "path": f"raw/{destination.name}",
                "exists": True,
                "sha256": sha256_file(destination),
                "candidateBinding": binding,
                "commandOrProcedure": item.get("commandOrProcedure"),
                "environment": item.get("environment"),
                "reviewer": item.get("reviewer"),
                "recordedAt": item.get("recordedAt"),
                "reason": reason,
            }
        )
    return entries


def clear_owned_raw_directory(output: Path) -> Path:
    output_resolved = output.resolve()
    raw_path = output / "raw"
    raw_resolved = raw_path.resolve(strict=False)
    if raw_resolved.parent != output_resolved or raw_path.name != "raw":
        raise ValueError("refusing to clear a raw directory outside the exact audit output")
    if raw_path.exists():
        if raw_path.is_symlink() or (
            hasattr(raw_path, "is_junction") and raw_path.is_junction()
        ):
            raise ValueError("refusing to clear a linked or junction raw directory")
        if not raw_path.is_dir():
            raise ValueError("refusing to replace a non-directory output/raw path")
        shutil.rmtree(raw_path)
    return raw_path


def validate_raw_evidence_manifest(
    manifest: dict[str, Any], manifest_path: Path
) -> list[dict[str, Any]]:
    expected_top_keys = {"schemaVersion", "entries"}
    actual_top_keys = set(manifest)
    if actual_top_keys != expected_top_keys:
        raise ValueError(
            f"{manifest_path}: raw evidence manifest keys must be exactly "
            f"{sorted(expected_top_keys)}; found {sorted(actual_top_keys)}"
        )
    if manifest["schemaVersion"] != "course1-ground-up-raw-input-v1":
        raise ValueError(f"{manifest_path}: raw evidence manifest has the wrong schemaVersion")
    rows = manifest["entries"]
    if not isinstance(rows, list):
        raise ValueError(f"{manifest_path}: entries must be an array")
    expected_row_keys = {
        "id",
        "path",
        "result",
        "candidateBinding",
        "candidateCommit",
        "commandOrProcedure",
        "environment",
        "reviewer",
        "recordedAt",
        "reason",
    }
    known_ids = {row[0] for row in EXPECTED_RAW}
    seen: set[str] = set()
    for index, row in enumerate(rows):
        label = f"{manifest_path}: entries[{index}]"
        if not isinstance(row, dict):
            raise ValueError(f"{label} must be an object")
        actual_row_keys = set(row)
        if actual_row_keys != expected_row_keys:
            raise ValueError(
                f"{label} keys must be exactly {sorted(expected_row_keys)}; "
                f"found {sorted(actual_row_keys)}"
            )
        evidence_id = row["id"]
        if not isinstance(evidence_id, str) or re.fullmatch(
            r"C1-RAW-[A-Z0-9-]+", evidence_id
        ) is None:
            raise ValueError(f"{label}.id is malformed")
        if evidence_id in seen:
            raise ValueError(f"{manifest_path}: duplicate raw evidence ID {evidence_id}")
        seen.add(evidence_id)
        if evidence_id not in known_ids:
            raise ValueError(f"{manifest_path}: unknown raw evidence ID {evidence_id}")
        path_value = row["path"]
        if not isinstance(path_value, str) or not path_value:
            raise ValueError(f"{label}.path must be a non-empty local file path")
        source = Path(path_value)
        if not source.is_file():
            raise ValueError(f"{label}.path does not identify an existing local file")
        if row["result"] not in {"PASS", "FAIL", "UNVERIFIED"}:
            raise ValueError(f"{label}.result is not in the closed vocabulary")
        binding = row["candidateBinding"]
        if binding not in {
            "UNBOUND_WORKING_COPY",
            "IMMUTABLE_CANDIDATE",
            "PUBLIC_ARTIFACT",
        }:
            raise ValueError(f"{label}.candidateBinding is not in the closed vocabulary")
        commit = row["candidateCommit"]
        if commit is not None and (
            not isinstance(commit, str)
            or re.fullmatch(r"[a-f0-9]{40}", commit) is None
        ):
            raise ValueError(f"{label}.candidateCommit must be null or a full commit")
        if binding == "UNBOUND_WORKING_COPY" and commit is not None:
            raise ValueError(f"{label}.candidateCommit must be null for an unbound result")
        if binding != "UNBOUND_WORKING_COPY" and commit is None:
            raise ValueError(f"{label}.candidateCommit is required for a bound result")
        for key in ("commandOrProcedure", "environment", "reviewer", "reason"):
            if not isinstance(row[key], str) or not row[key].strip():
                raise ValueError(f"{label}.{key} must be a non-empty string")
        recorded_at = row["recordedAt"]
        if not isinstance(recorded_at, str):
            raise ValueError(f"{label}.recordedAt must be an ISO 8601 date-time")
        try:
            parsed = datetime.fromisoformat(recorded_at.replace("Z", "+00:00"))
        except ValueError as error:
            raise ValueError(f"{label}.recordedAt must be an ISO 8601 date-time") from error
        if parsed.tzinfo is None:
            raise ValueError(f"{label}.recordedAt must include a timezone offset")
    return rows


def ledger_status(root: Path) -> str:
    text = (root / "COURSE_1_AUDIT_STATUS_AND_REPAIR_LEDGER.md").read_text(encoding="utf-8")
    matches = re.findall(
        r"^- Current status: \*\*`(PASS|REPAIR REQUIRED|UNVERIFIED|SUPERSEDED)`\*\*$",
        text,
        re.MULTILINE,
    )
    if len(matches) != 1:
        raise ValueError(f"expected exactly one authoritative current status, found {matches}")
    return matches[0]


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def validate_machine_documents(
    schema: dict[str, Any], documents: dict[str, dict[str, Any]]
) -> None:
    if set(documents) != set(MACHINE_FILES):
        raise ValueError(
            "machine artifact set is not exact: "
            f"expected {sorted(MACHINE_FILES)}, found {sorted(documents)}"
        )
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for name in MACHINE_FILES:
        errors = sorted(
            validator.iter_errors(documents[name]),
            key=lambda error: (list(error.absolute_path), error.message),
        )
        if errors:
            details = "; ".join(
                f"{error.json_path}: {error.message}" for error in errors
            )
            raise ValueError(f"{name}: closed-schema validation failed: {details}")


def write_markdown(
    output: Path,
    audit_date: str,
    course_version: str,
    product_status: str,
    git_meta: dict[str, Any],
    changes: list[dict[str, Any]],
) -> None:
    head = git_meta["headCommit"]
    output.joinpath("pre-repair-findings.md").write_text(
        f"""# Course 1 pre-repair findings preservation

- Audit: `C1-GROUND-UP-{audit_date}`
- Course version: `{course_version}`
- Surviving immutable reference: `{head}`
- Exact pre-repair dirty working tree: **UNVERIFIED**

The repair phase began before this repository package captured an exact
file-by-file hash inventory of the dirty diagnostic baseline. That baseline
cannot be reconstructed honestly. The dated audit report and authoritative
ledger remain surviving records, but neither is represented here as a clean
immutable pre-repair candidate. This limitation keeps `C1-AA-001` unverified.
""",
        encoding="utf-8",
        newline="\n",
    )
    output.joinpath("audit-gap-review.md").write_text(
        """# Course 1 audit-gap review

1. No clean immutable candidate or exact pre-repair dirty-tree freeze exists.
2. Presence, headings, and green local checks cannot prove comprehension or human use.
3. Product and test logic may share assumptions; independent oracle review remains required.
4. Local results can depend on cached runtimes, profiles, packages, PATH, locale, and network state.
5. Candidate/public/installed-client/rollback and human/device combinations remain unexecuted.
6. Parser controls require candidate-bound final negative evidence after the last change.
7. Historical evidence is not current-candidate evidence and must not close current rows.
8. Every source, content, test, tool, workflow, schema, or evidence edit invalidates affected results.
9. Beginner, assessor/UAT, specialist, accessibility/device, repository, installed-client, and production evidence is missing.
10. A skeptical human reviewer should reproduce each layer from a clean candidate and retain disagreements.

This review records missing evidence as `UNVERIFIED`; it does not infer a defect.
""",
        encoding="utf-8",
        newline="\n",
    )
    output.joinpath("repair-and-invalidation-record.md").write_text(
        f"""# Course 1 repair and invalidation record

The current snapshot contains **{len(changes)}** changed or untracked paths
relative to `{head}`. `change-to-evidence-map.json` records each path and the
evidence families it invalidates. Because this audit-package code and evidence
were added after earlier local runs, a complete integrated rerun must follow
the last material change. No build hash in this package is an accepted
candidate identity.
""",
        encoding="utf-8",
        newline="\n",
    )
    output.joinpath("independent-review-and-adjudication.md").write_text(
        """# Course 1 independent review and adjudication

Status: **UNVERIFIED**

No named human independent technical, curriculum/learning,
Progressive Web App/accessibility, or governance reviewer reproduced this
exact working copy from a clean immutable candidate. AI-assisted reviews and
repair-author reruns are useful local inputs, but they do not satisfy
`C1-AA-008`. No disagreement is suppressed; no independent adjudication is
claimed.
""",
        encoding="utf-8",
        newline="\n",
    )
    output.joinpath("final-decision.md").write_text(
        f"""# Course 1 ground-up audit final decision

- Audit assurance: **UNVERIFIED**
- Authoritative product status at generation: **{product_status}**
- Candidate: **not created**
- Promotion: **not permitted**

The local working copy is dirty and not an immutable candidate. Required
literal-beginner, human assessment and User Acceptance Testing (UAT),
practitioner/legal/security, accessibility/device, repository, manual-source,
installed-client, and production evidence is missing or not bound to this
working copy. Local automated results cannot substitute for those classes.

Next: finish the last material edits, rerun the complete integrated suite,
then request separate authority for a clean candidate freeze and independent
release evidence. Do not deploy this package as proof of Course 1 acceptance.
""",
        encoding="utf-8",
        newline="\n",
    )


def build(root: Path, output: Path, audit_date: str, raw_manifest: Path | None) -> None:
    curriculum = load_json(root / "curriculum.json")
    audit_schema = load_json(
        root / "audit_control/course1/ground_up_audit_artifact.schema.json"
    )
    course = curriculum["course"]
    course_version = course["version"]
    files, git_meta = snapshot_files(root)
    product_status = ledger_status(root)
    output.mkdir(parents=True, exist_ok=True)
    shared = [
        {
            "path": row["path"],
            "classification": row["classification"],
            "rationale": (
                "Rendered Course 1 and later-course material share this reader surface."
                if row["classification"] == "SHARED_COURSE_READER"
                else "This governance surface can affect more than one course and is classified explicitly."
            ),
        }
        for row in files
        if row["classification"] in {"SHARED_COURSE_READER", "SHARED_GOVERNANCE"}
    ]
    scope = common(course_version, audit_date, "SCOPE_AND_AUTHORITY") | {
        "mode": "APPROVED_REPAIR_EVIDENCE",
        "authority": {
            "repairAndEvidenceWrites": True,
            "candidateFreeze": False,
            "commitPushDeploy": False,
            "cloudBillingOrRealData": False,
        },
        "scope": {
            "included": [
                "Course 1 curriculum, runner, assessment, PWA and release controls",
                "Explicitly classified shared surfaces",
            ],
            "excluded": [
                "Course 4 lesson and implementation quality",
                "Commit, push, deployment, billing, cloud activation and real data",
            ],
            "sharedSurfaces": shared,
        },
        "prohibitedActions": [
            "commit",
            "push",
            "deploy",
            "activate paid billing",
            "use real client, medical, employer, personal or confidential data",
        ],
        "baselineLimitations": [
            "The exact dirty pre-repair working tree was not frozen before repairs.",
            "This generated repository evidence changes the working tree and is not an immutable candidate.",
        ],
        "status": "UNVERIFIED",
    }
    version_path = root / "app/dist/version.json"
    version = load_json(version_path) if version_path.is_file() else {}
    baseline = common(course_version, audit_date, "BASELINE_FILE_INVENTORY") | {
        "snapshotBoundary": "Current working tree immediately before this audit output directory was written; that output directory is explicitly excluded to avoid self-reference.",
        "git": git_meta,
        "course": {
            "practiceRevision": course["practiceRevision"],
            "sourceVerifiedThrough": course["sourceVerifiedThrough"],
            "contentRevisionThrough": course["contentRevisionThrough"],
            "workingBuildIdentity": {
                "status": "UNVERIFIED",
                "buildId": version.get("buildId"),
                "contentHash": version.get("contentHash"),
                "reason": "A generated local build identity is not an immutable accepted candidate.",
            },
        },
        "preRepairBaseline": {
            "captured": False,
            "status": "UNVERIFIED",
            "reason": "Repairs preceded this exact repository inventory, so the untouched dirty diagnostic baseline cannot be reconstructed.",
        },
        "excludedPaths": [
            ".git/",
            "ignored dependency/cache/build directories",
            "release_evidence/course1_ground_up_audit/",
        ],
        "files": files,
        "status": "UNVERIFIED",
    }
    inventory = common(course_version, audit_date, "NORMATIVE_ID_INVENTORY") | build_id_inventory(root, files)
    graph_body, technical_tests, learning_methods = build_graph(root)
    evidence_graph = common(course_version, audit_date, "REQUIREMENT_TEST_EVIDENCE_GRAPH") | graph_body
    unittest_manifest = load_json(root / "course1_capstone/tests/test_manifest.json")
    negative = load_json(root / "quality/negative-control-manifest.json")
    mutation = load_json(root / "quality/mutation-manifest.json")
    scenarios = common(course_version, audit_date, "TEST_AND_SCENARIO_MANIFEST") | {
        "sourceManifests": [
            file_ref(root, "audit_control/course1/technical_test_manifest.json"),
            file_ref(root, "course1_capstone/tests/test_manifest.json"),
            file_ref(root, "quality/negative-control-manifest.json"),
            file_ref(root, "quality/mutation-manifest.json"),
        ],
        "technicalTests": technical_tests,
        "learningMethods": learning_methods,
        "namedUnitTests": sorted(unittest_manifest["tests"]),
        "negativeControls": [
            {"id": row["id"], "family": row["family"], "target": row["target"]}
            for row in sorted(negative["controls"], key=lambda item: item["id"])
        ],
        "mutations": [
            {"id": row["id"], "family": row["family"], "target": row["target"]}
            for row in sorted(mutation["mutants"], key=lambda item: item["id"])
        ],
        "requiredExternalEvidenceClasses": [
            "ACCESSIBILITY_DEVICE",
            "ASSESSOR_UAT",
            "INSTALLED_CLIENT",
            "LEARNER",
            "MANUAL_SOURCE",
            "PRACTITIONER_LEGAL_SECURITY",
            "PRODUCTION",
            "REPOSITORY",
        ],
        "currentAcceptanceStatus": "UNVERIFIED",
    }
    changes = [
        {
            "path": row["path"],
            "workingTreeStatus": row["workingTreeStatus"],
            "classification": row["classification"],
            "invalidatedEvidenceFamilies": invalidated_families(
                row["path"], row["classification"]
            ),
            "rerunRequired": row["classification"] != "COURSE4_ONLY",
        }
        for row in files
        if row["workingTreeStatus"] != "TRACKED_UNCHANGED"
    ]
    change_map = common(course_version, audit_date, "CHANGE_TO_EVIDENCE_MAP") | {
        "baseline": {"headCommit": git_meta["headCommit"], "dirty": git_meta["dirty"]},
        "changes": changes,
        "priorEvidenceDisposition": "INVALIDATED",
        "lastMaterialChangeFrozen": False,
        "integratedRerunAfterLastMaterialChange": {
            "status": "UNVERIFIED",
            "evidenceIds": [],
            "reason": "The audit generator, schema, tests and output package are material changes after earlier runs.",
        },
    }
    python_version = platform.python_version()
    components = [
        {
            "name": "generator Python",
            "status": "PASS",
            "version": python_version,
            "pathRedacted": True,
            "reason": "Runtime used to generate this local artifact package only.",
        },
        {
            "name": "Git",
            "status": "PASS",
            "version": git_text(root, "--version"),
            "pathRedacted": True,
            "reason": "Runtime used to inventory the current repository only.",
        },
        {
            "name": "PowerShell",
            "status": "UNVERIFIED",
            "version": None,
            "pathRedacted": True,
            "reason": "Exact learner-shell execution evidence was not supplied to this package.",
        },
        {
            "name": "Chrome and Edge profiles",
            "status": "UNVERIFIED",
            "version": None,
            "pathRedacted": True,
            "reason": "Fresh browser-profile evidence was not supplied to this package.",
        },
    ]
    environment = common(course_version, audit_date, "ENVIRONMENT_AND_TOOLCHAIN") | {
        "host": {
            "operatingSystem": platform.system() or "Windows",
            "release": platform.release() or "unrecorded",
            "version": platform.version() or "unrecorded",
            "machine": platform.machine() or "unrecorded",
            "hostnameRedacted": True,
            "filesystem": "Windows workspace; exact volume/filesystem attestation not captured",
            "timezone": "Europe/Amsterdam",
            "locale": locale.getlocale()[0] or "unrecorded",
        },
        "components": components,
        "learnerEnvironment": {
            "status": "UNVERIFIED",
            "reason": "This maintainer runtime is not the learner's approved clean setup.",
        },
        "cleanEnvironment": {
            "status": "UNVERIFIED",
            "reason": "The repository is dirty and this generator did not create a fresh workspace/profile.",
        },
        "networkBoundary": {
            "status": "UNVERIFIED",
            "reason": "No complete network-denial or leakage trace is bound to an immutable candidate.",
        },
    }
    evidence_entries = raw_evidence(
        output,
        raw_manifest,
        git_meta["dirty"],
        git_meta["headCommit"],
        audit_schema,
    )
    raw_index = common(course_version, audit_date, "RAW_EVIDENCE_INDEX") | {
        "entries": evidence_entries,
        "candidateBindingStatus": "UNVERIFIED",
        "missingEvidenceClasses": sorted(
            {
                row["evidenceClass"]
                for row in evidence_entries
                if row["result"] != "PASS"
                or row["candidateBinding"] == "UNBOUND_WORKING_COPY"
            }
        ),
    }
    reasons = {
        1: "The tree is dirty and the exact pre-repair dirty baseline was not frozen.",
        2: "Canonical ID families are machine-enumerated without duplicates, but this is local working-copy evidence.",
        3: "The graph is structurally complete, but all technical and learning acceptance evidence remains UNVERIFIED.",
        4: "Closed-status semantics still require one immutable candidate and current evidence.",
        5: "Required candidate-bound provenance, reviewers, expiry and rerun records are incomplete.",
        6: "Local adversarial controls are inventoried, but no post-final-change candidate-bound raw result was supplied.",
        7: "No clean immutable candidate, accepted artifact, public byte comparison or installed-client identity exists.",
        8: "No named human non-owner reproduced all layers from a separate clean environment.",
        9: "The audit package itself is a material change after earlier integrated runs.",
        10: "Closed schemas and parser tests exist, but their final candidate-bound raw evidence is not supplied.",
        11: "Git is dirty and no fresh learner workspace/profile post-run pollution record exists.",
        12: "Evidence classes are kept separate, but the mandatory external classes are missing.",
        13: "All sixteen rules are listed, but mandatory rules and external gates are not all PASS.",
        14: "Consumer alignment requires the final frozen-tree run and candidate evidence.",
        15: "The package stayed within approved repository evidence writes and performed no prohibited external action.",
        16: "Date meanings are separated in source, but final independent negative evidence is not candidate-bound.",
    }
    pass_rules = {2, 15}
    assurance_rules = [
        {
            "id": f"C1-AA-{number:03d}",
            "status": "PASS" if number in pass_rules else "UNVERIFIED",
            "evidenceIds": (
                ["normative-id-inventory.json"]
                if number == 2
                else ["scope-and-authority.json"]
                if number == 15
                else []
            ),
            "exclusions": (
                ["Immutable candidate and external evidence are outside current authority."]
                if number not in pass_rules
                else []
            ),
            "reason": reasons[number],
        }
        for number in range(1, 17)
    ]
    assurance = common(course_version, audit_date, "AUDIT_ASSURANCE_RESULT") | {
        "rules": assurance_rules,
        "overallAuditStatus": "UNVERIFIED",
        "productStatusAtGeneration": product_status,
        "allMandatoryRulesPassed": False,
        "unverifiedExternalGates": [
            "literal-beginner completion",
            "independent assessment and real synthetic UAT",
            "practitioner, legal/privacy and security review",
            "accessibility and device matrix",
            "repository settings and scheduled-run evidence",
            "manual OECD source review",
            "installed old-client update and preservation",
            "public byte identity, live verification and rollback",
        ],
        "decisionReason": "The working copy is not a clean immutable candidate and mandatory non-substitutable evidence is missing.",
    }
    documents = {
        "scope-and-authority.json": scope,
        "baseline-file-inventory.json": baseline,
        "normative-id-inventory.json": inventory,
        "requirement-test-evidence-graph.json": evidence_graph,
        "test-and-scenario-manifest.json": scenarios,
        "change-to-evidence-map.json": change_map,
        "environment-and-toolchain.json": environment,
        "raw-evidence-index.json": raw_index,
        "audit-assurance-result.json": assurance,
    }
    validate_machine_documents(audit_schema, documents)
    for name in MACHINE_FILES:
        write_json(output / name, documents[name])
    write_markdown(
        output, audit_date, course_version, product_status, git_meta, changes
    )
    missing = [name for name in MACHINE_FILES + MARKDOWN_FILES if not (output / name).is_file()]
    if missing:
        raise ValueError(f"audit package is incomplete: {missing}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--audit-date", default="2026-07-29")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--raw-evidence-manifest", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    course_version = load_json(root / "curriculum.json")["course"]["version"]
    output = (
        args.output.resolve()
        if args.output
        else root
        / "release_evidence"
        / "course1_ground_up_audit"
        / course_version
        / args.audit_date
    )
    build(root, output, args.audit_date, args.raw_evidence_manifest)
    print(f"PASS: wrote the conservative 14-file audit package to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
