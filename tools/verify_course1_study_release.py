"""Fail closed unless an exact Course 1 artifact is safe to publish for study.

This verifier authorizes distribution only. It does not accept Course 1,
award learner competence, close human-evidence findings, or establish Course 2
readiness.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any

from verify_course1_promotion import (
    LEDGER_PATH,
    MANIFEST_ARTIFACT_FORMAT,
    STUDY_DISTRIBUTION_PURPOSE,
    STUDY_PRODUCT_STATUS,
    authoritative_product_status,
    inspect_artifact_identity,
    parse_ledger_rows,
    read_object,
)


ROOT = Path(__file__).resolve().parents[1]
CURRICULUM_PATH = ROOT / "curriculum.json"
HEX_40 = re.compile(r"^[0-9a-f]{40}$")
ALLOWED_PENDING_FINDING_IDS = {
    "C1-TECH-006",
    *(f"C1-CONT-{number:03d}" for number in range(1, 8)),
    "C1-GOV-002",
    "C1-GOV-004",
    "C1-GOV-005",
    "C1-GOV-006",
    "C1-GOV-007",
    "C1-GOV-009",
    "C1-GOV-011",
}
BOUNDARY_TEXT = (
    "UNVERIFIED personal-study release",
    "Use synthetic data only",
    "cannot award Course 1 completion",
    "Course 2",
    "production readiness",
)


def validate_study_release(
    dist: Path,
    *,
    expected_commit: str,
    curriculum_path: Path = CURRICULUM_PATH,
    ledger_path: Path = LEDGER_PATH,
) -> tuple[list[str], dict[str, Any] | None, list[str]]:
    failures: list[str] = []
    identity: dict[str, Any] | None = None

    if not HEX_40.fullmatch(expected_commit):
        failures.append("expected commit must be a full lower-case 40-character Git SHA")

    try:
        curriculum = read_object(curriculum_path)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        curriculum = {}
        failures.append(f"curriculum could not be read: {exc}")

    course = curriculum.get("course")
    if not isinstance(course, dict):
        failures.append("curriculum.course must be an object")
        course = {}
    if course.get("productStatus") != STUDY_PRODUCT_STATUS:
        failures.append("curriculum productStatus must be UNVERIFIED")
    if course.get("distributionPurpose") != STUDY_DISTRIBUTION_PURPOSE:
        failures.append(
            "curriculum distributionPurpose must be personal-synthetic-study"
        )

    try:
        ledger_text = ledger_path.read_text(encoding="utf-8", errors="strict")
    except (OSError, UnicodeError) as exc:
        ledger_text = ""
        failures.append(f"ledger could not be read: {exc}")

    product_status, status_failures = authoritative_product_status(ledger_text)
    rows, row_failures = parse_ledger_rows(ledger_text)
    failures.extend(status_failures)
    failures.extend(row_failures)
    if product_status != STUDY_PRODUCT_STATUS:
        failures.append("authoritative product status must be UNVERIFIED")

    blocked = sorted(
        finding_id
        for finding_id, status in rows.items()
        if status in {"OPEN", "PARTIAL", "REOPENED"}
    )
    if blocked:
        failures.append(f"known High/Medium defects block study publication: {blocked}")
    pending = sorted(
        finding_id
        for finding_id, status in rows.items()
        if status == "EVIDENCE PENDING"
    )
    unexpected_pending = sorted(set(pending) - ALLOWED_PENDING_FINDING_IDS)
    if unexpected_pending:
        failures.append(
            "study publication has unclassified evidence-pending findings: "
            f"{unexpected_pending}"
        )

    if HEX_40.fullmatch(expected_commit):
        try:
            identity = inspect_artifact_identity(
                dist,
                expected_commit=expected_commit,
                operation="personal-study",
            )
        except (OSError, UnicodeError, ValueError, KeyError, TypeError) as exc:
            failures.append(f"artifact identity failed: {exc}")

    try:
        bundle = read_object(dist / "course-content.json")
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        bundle = {}
        failures.append(f"course-content.json could not be read: {exc}")
    bundled_course = bundle.get("course")
    if not isinstance(bundled_course, dict):
        failures.append("course-content.json course must be an object")
        bundled_course = {}
    for field in ("id", "version", "productStatus", "distributionPurpose"):
        if bundled_course.get(field) != course.get(field):
            failures.append(f"bundled course {field} does not match curriculum")
    if identity is not None:
        version = identity["version"]
        if identity.get("artifactFormat") != MANIFEST_ARTIFACT_FORMAT:
            failures.append("personal study requires a manifest-v1 artifact")
        if version.get("courseVersion") != course.get("version"):
            failures.append("artifact course version does not match curriculum")
        if version.get("productStatus") != STUDY_PRODUCT_STATUS:
            failures.append("artifact product status is not UNVERIFIED")
        if version.get("distributionPurpose") != STUDY_DISTRIBUTION_PURPOSE:
            failures.append("artifact is not classified for personal synthetic study")

    try:
        index_text = (dist / "index.html").read_text(
            encoding="utf-8",
            errors="strict",
        )
    except (OSError, UnicodeError) as exc:
        index_text = ""
        failures.append(f"index.html could not be read: {exc}")
    for required_text in BOUNDARY_TEXT:
        if required_text not in index_text:
            failures.append(
                f"published learner boundary is missing text: {required_text}"
            )

    return failures, identity, pending


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dist", required=True, type=Path)
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--curriculum", type=Path, default=CURRICULUM_PATH)
    parser.add_argument("--ledger", type=Path, default=LEDGER_PATH)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    failures, identity, pending = validate_study_release(
        args.dist,
        expected_commit=args.expected_commit,
        curriculum_path=args.curriculum,
        ledger_path=args.ledger,
    )
    report = {
        "schemaVersion": 1,
        "result": "PASS" if not failures else "FAIL",
        "decision": (
            "AUTHORIZED_FOR_PERSONAL_SYNTHETIC_STUDY"
            if not failures
            else "STUDY_PUBLICATION_BLOCKED"
        ),
        "checkedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "candidateCommit": args.expected_commit,
        "productStatus": STUDY_PRODUCT_STATUS,
        "distributionPurpose": STUDY_DISTRIBUTION_PURPOSE,
        "pendingFindingIds": pending,
        "artifact": (
            {
                "courseVersion": identity["version"]["courseVersion"],
                "buildId": identity["version"]["buildId"],
                "contentHash": identity["version"]["contentHash"],
                "assetManifestSha256": identity["assetManifestSha256"],
                "artifactTreeSha256": identity["artifactTreeSha256"],
                "publicServedTreeSha256": identity["publicServedTreeSha256"],
            }
            if identity is not None
            else None
        ),
        "failures": failures,
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(
            f"{json.dumps(report, indent=2)}\n",
            encoding="utf-8",
        )
    print(json.dumps(report, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
