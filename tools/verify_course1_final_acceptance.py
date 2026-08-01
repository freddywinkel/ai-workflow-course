"""Fail closed unless one deployed Course 1 candidate has all 33 test records.

This is deliberately separate from pre-deployment promotion. Promotion keeps
its exact 32-test gate; this final adjudication is possible only after the
public provenance test exists and is bound to the same immutable candidate.
"""

from __future__ import annotations

import argparse
import datetime as dt
import ipaddress
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from verify_course1_promotion import (
    DECLARED_TECHNICAL_TEST_IDS,
    HEX_40,
    HEX_64,
    LEDGER_PATH,
    MANIFEST_ARTIFACT_FORMAT,
    exact_keys,
    inspect_artifact_identity,
    parse_timestamp,
    read_object,
    reject_duplicate_json_keys,
    resolve_evidence_file,
    resolve_record,
    sha256,
    validate_last_known_good_acceptance,
    validate_ledger,
    validate_technical_evidence,
)


ROOT = Path(__file__).resolve().parents[1]
FINAL_SCHEMA_VERSION = "course1-final-technical-acceptance-v1"
FINAL_DECISION = "ACCEPTED_AFTER_DEPLOYMENT"
COURSE_ID = "course-1-controlled-ai-workflow-foundations"
PUBLIC_PATH = "/ai-workflow-course/"


def validate_public_url(value: Any) -> list[str]:
    failures: list[str] = []
    if not isinstance(value, str) or not value:
        return ["deployment.publicUrl must be one non-empty HTTPS URL"]
    parsed = urlsplit(value)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
        or parsed.path != PUBLIC_PATH
    ):
        failures.append(
            "deployment.publicUrl must be an origin-only HTTPS URL ending "
            f"in the exact Course 1 path {PUBLIC_PATH}"
        )
        return failures
    hostname = parsed.hostname.casefold()
    if hostname == "localhost" or hostname.endswith(".localhost"):
        failures.append("deployment.publicUrl must not name localhost")
    try:
        address = ipaddress.ip_address(hostname)
    except ValueError:
        address = None
    if address is not None and not address.is_global:
        failures.append(
            "deployment.publicUrl must not use a private, loopback, or reserved IP"
        )
    return failures


def _read_locator_record(
    locator: Any,
    *,
    evidence_repository_root: Path | None,
    label: str,
) -> tuple[dict[str, Any] | None, Path | None, list[str]]:
    failures: list[str] = []
    locator_object = exact_keys(
        locator,
        {"path", "sha256"},
        label,
        failures,
    )
    if evidence_repository_root is None:
        return None, None, failures + [
            "an evidence repository root is required to resolve final records"
        ]
    expected_hash = locator_object.get("sha256")
    if not isinstance(expected_hash, str) or not HEX_64.fullmatch(expected_hash):
        failures.append(f"{label}.sha256 must be lowercase SHA-256")
    try:
        path = resolve_evidence_file(
            locator_object.get("path"),
            evidence_repository_root,
        )
    except (OSError, TypeError, ValueError) as exc:
        return None, None, failures + [f"{label}: {exc}"]
    if expected_hash != sha256(path):
        failures.append(f"{label}.sha256 does not match the referenced file")
    try:
        value = json.loads(
            path.read_bytes().decode("utf-8"),
            object_pairs_hook=reject_duplicate_json_keys,
        )
        if not isinstance(value, dict):
            raise ValueError("top-level JSON must be one object")
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        return None, path, failures + [f"{label} is not valid closed JSON: {exc}"]
    return value, path, failures


def validate_final_record(
    record: dict[str, Any],
    version: dict[str, Any],
    *,
    expected_commit: str,
    expected_promotion_run_id: str,
    asset_manifest_sha256: str | None,
    artifact_tree_sha256_value: str,
    public_served_tree_sha256_value: str,
    ledger_text: str,
    evidence_repository_root: Path | None,
) -> list[str]:
    failures: list[str] = []
    exact_keys(
        record,
        {
            "schemaVersion",
            "decision",
            "courseId",
            "candidate",
            "deployment",
            "adjudicatedAt",
            "reviewer",
            "promotionAcceptanceRecord",
            "promotionDependentFindingIds",
            "evidence",
        },
        "final acceptance record",
        failures,
    )
    if record.get("schemaVersion") != FINAL_SCHEMA_VERSION:
        failures.append(f"schemaVersion must be {FINAL_SCHEMA_VERSION}")
    if record.get("decision") != FINAL_DECISION:
        failures.append(f"decision must be {FINAL_DECISION}")
    if record.get("courseId") != COURSE_ID:
        failures.append("courseId is not Course 1")

    candidate = exact_keys(
        record.get("candidate"),
        {
            "artifactFormat",
            "commit",
            "courseVersion",
            "buildId",
            "contentHash",
            "assetManifestSha256",
            "artifactTreeSha256",
        },
        "candidate",
        failures,
    )
    expected_candidate = {
        "artifactFormat": MANIFEST_ARTIFACT_FORMAT,
        "commit": expected_commit,
        "courseVersion": version.get("courseVersion"),
        "buildId": version.get("buildId"),
        "contentHash": version.get("contentHash"),
        "assetManifestSha256": asset_manifest_sha256,
        "artifactTreeSha256": artifact_tree_sha256_value,
    }
    if candidate != expected_candidate:
        failures.append(
            "candidate must exactly match the inspected immutable promotion artifact"
        )
    if not HEX_40.fullmatch(str(candidate.get("commit", ""))):
        failures.append("candidate.commit must be a full lower-case Git SHA")
    for field in (
        "contentHash",
        "assetManifestSha256",
        "artifactTreeSha256",
    ):
        if not HEX_64.fullmatch(str(candidate.get(field, ""))):
            failures.append(f"candidate.{field} must be lowercase SHA-256")

    deployment = exact_keys(
        record.get("deployment"),
        {
            "publicUrl",
            "promotionWorkflowRunId",
            "deploymentId",
            "deployedAt",
            "publicCommit",
            "publicBuildId",
            "publicContentHash",
            "publicAssetManifestSha256",
            "publicServedTreeSha256",
            "nonPublicArtifactFiles",
        },
        "deployment",
        failures,
    )
    failures.extend(validate_public_url(deployment.get("publicUrl")))
    if not isinstance(
        deployment.get("promotionWorkflowRunId"), str
    ) or not re.fullmatch(r"[1-9][0-9]*", deployment["promotionWorkflowRunId"]):
        failures.append("deployment.promotionWorkflowRunId must be a positive run ID")
    elif deployment["promotionWorkflowRunId"] != expected_promotion_run_id:
        failures.append(
            "deployment.promotionWorkflowRunId does not match the verified workflow run"
        )
    if not isinstance(deployment.get("deploymentId"), str) or not re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9._:-]*",
        deployment["deploymentId"],
    ):
        failures.append("deployment.deploymentId must be one recorded opaque ID")
    public_comparisons = {
        "publicCommit": candidate.get("commit"),
        "publicBuildId": candidate.get("buildId"),
        "publicContentHash": candidate.get("contentHash"),
        "publicAssetManifestSha256": candidate.get("assetManifestSha256"),
        "publicServedTreeSha256": public_served_tree_sha256_value,
    }
    for field, expected in public_comparisons.items():
        if deployment.get(field) != expected:
            failures.append(f"deployment.{field} does not match the candidate")
    if deployment.get("nonPublicArtifactFiles") != [".nojekyll"]:
        failures.append(
            "deployment.nonPublicArtifactFiles must exactly record .nojekyll"
        )

    deployed_at: dt.datetime | None = None
    adjudicated_at: dt.datetime | None = None
    try:
        deployed_at = parse_timestamp(
            deployment.get("deployedAt"),
            "deployment.deployedAt",
        )
    except (TypeError, ValueError) as exc:
        failures.append(str(exc))
    try:
        adjudicated_at = parse_timestamp(
            record.get("adjudicatedAt"),
            "adjudicatedAt",
        )
    except (TypeError, ValueError) as exc:
        failures.append(str(exc))
    if (
        deployed_at is not None
        and adjudicated_at is not None
        and deployed_at > adjudicated_at
    ):
        failures.append("deployment.deployedAt is after adjudicatedAt")

    reviewer = exact_keys(
        record.get("reviewer"),
        {"name", "independentOfImplementation"},
        "reviewer",
        failures,
    )
    if not isinstance(reviewer.get("name"), str) or not reviewer["name"].strip():
        failures.append("reviewer.name must be recorded")
    if reviewer.get("independentOfImplementation") is not True:
        failures.append("reviewer.independentOfImplementation must be true")

    failures.extend(
        validate_last_known_good_acceptance(
            record.get("promotionAcceptanceRecord"),
            candidate=candidate,
            evidence_repository_root=evidence_repository_root,
            rollback_accepted_at=deployed_at,
            artifact_format=MANIFEST_ARTIFACT_FORMAT,
        )
    )
    failures.extend(
        validate_technical_evidence(
            record.get("evidence"),
            candidate=candidate,
            evidence_repository_root=evidence_repository_root,
            required_test_ids=DECLARED_TECHNICAL_TEST_IDS,
            accepted_at=adjudicated_at,
        )
    )
    failures.extend(
        validate_ledger(
            ledger_text,
            record.get("promotionDependentFindingIds"),
        )
    )

    provenance_times: list[dt.datetime] = []
    raw_evidence = record.get("evidence")
    if isinstance(raw_evidence, list):
        for index, locator in enumerate(raw_evidence):
            value, _path, locator_failures = _read_locator_record(
                locator,
                evidence_repository_root=evidence_repository_root,
                label=f"evidence[{index}]",
            )
            if locator_failures:
                continue
            if value is not None and value.get("testId") == "C1-TST-PROV-001":
                try:
                    provenance_times.append(
                        parse_timestamp(
                            value.get("recordedAt"),
                            f"evidence[{index}] provenance recordedAt",
                        )
                    )
                except (TypeError, ValueError) as exc:
                    failures.append(str(exc))
    if len(provenance_times) != 1:
        failures.append(
            "final adjudication requires exactly one C1-TST-PROV-001 record"
        )
    elif deployed_at is not None and provenance_times[0] < deployed_at:
        failures.append(
            "C1-TST-PROV-001 must be recorded at or after deployment.deployedAt"
        )
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", required=True)
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--promotion-run-id", required=True)
    parser.add_argument("--dist", type=Path, default=ROOT / "app" / "dist")
    parser.add_argument(
        "--evidence-root",
        type=Path,
        default=ROOT,
        help="repository copy that owns the final record and evidence",
    )
    parser.add_argument(
        "--ledger",
        type=Path,
        default=LEDGER_PATH,
        help="authoritative pre-final ledger path",
    )
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    failures: list[str] = []
    expected_commit = args.expected_commit.strip().casefold()
    expected_promotion_run_id = args.promotion_run_id.strip()
    if not HEX_40.fullmatch(expected_commit):
        failures.append("expected commit must be a full 40-character Git SHA")
    if not re.fullmatch(r"[1-9][0-9]*", expected_promotion_run_id):
        failures.append("promotion run ID must be a positive integer")
    try:
        record_path = resolve_record(args.record, args.evidence_root)
        record = read_object(record_path)
        identity = inspect_artifact_identity(
            args.dist.resolve(),
            expected_commit=expected_commit,
            operation="promote",
        )
        ledger_text = args.ledger.resolve().read_text(encoding="utf-8")
        failures.extend(
            validate_final_record(
                record,
                identity["version"],
                expected_commit=expected_commit,
                expected_promotion_run_id=expected_promotion_run_id,
                asset_manifest_sha256=identity["assetManifestSha256"],
                artifact_tree_sha256_value=identity["artifactTreeSha256"],
                public_served_tree_sha256_value=identity[
                    "publicServedTreeSha256"
                ],
                ledger_text=ledger_text,
                evidence_repository_root=args.evidence_root.resolve(),
            )
        )
    except (OSError, TypeError, ValueError, KeyError, json.JSONDecodeError) as exc:
        failures.append(str(exc))

    result = {
        "schemaVersion": 1,
        "result": "PASS" if not failures else "FAIL",
        "expectedCommit": expected_commit,
        "requiredTestCount": len(DECLARED_TECHNICAL_TEST_IDS),
        "failures": failures,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.report:
        destination = args.report.resolve()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
