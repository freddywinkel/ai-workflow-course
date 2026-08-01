"""Fail closed unless a manual Course 1 promotion matches accepted evidence."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = ROOT / "COURSE_1_AUDIT_STATUS_AND_REPAIR_LEDGER.md"
HEX_40 = re.compile(r"^[0-9a-f]{40}$")
HEX_64 = re.compile(r"^[0-9a-f]{64}$")
PRODUCT_STATUS_LINE = re.compile(
    r"^- Current status: \*\*`(?P<status>[^`\r\n]+)`\*\*$",
    re.MULTILINE,
)
PRODUCT_STATUS_FRAGMENT = re.compile(
    r"- Current status: \*\*`(?P<status>[^`\r\n]+)`\*\*"
)
PRODUCT_STATUSES = {
    "PASS",
    "REPAIR REQUIRED",
    "UNVERIFIED",
    "SUPERSEDED",
}
LEDGER_HEADER = (
    "ID",
    "Severity",
    "Requirement",
    "Closure test and evidence",
    "Status",
    "Owner",
)
LEDGER_FINDING_ID = re.compile(r"^`(C1-(?:TECH|CONT|GOV)-\d{3})`$")
EXPECTED_LEDGER_FINDING_IDS = {
    *(f"C1-TECH-{number:03d}" for number in range(1, 7)),
    *(f"C1-CONT-{number:03d}" for number in range(1, 10)),
    *(f"C1-GOV-{number:03d}" for number in range(1, 16)),
}
LEDGER_STATUSES = {
    "OPEN",
    "PARTIAL",
    "EVIDENCE PENDING",
    "CLOSED",
    "REOPENED",
}
TECHNICAL_TEST_ID = re.compile(r"^C1-TST-(?:[A-Z0-9]+-)+\d{3}$")
TECHNICAL_EVIDENCE_ID = re.compile(r"^C1-EV-[A-Z0-9-]+-\d{3}$")
TECHNICAL_EVIDENCE_CLASSES = {
    "AUTOMATED_LOCAL",
    "NATIVE_WINDOWS",
    "REAL_BROWSER",
    "CI_SUPPLY_CHAIN",
    "POST_DEPLOY",
    "INDEPENDENT_REVIEW",
}
TECHNICAL_ARTIFACT_KINDS = {
    "COMMAND_LOG",
    "RAW_RESULT",
    "SCREENSHOT",
    "BROWSER_TRACE",
    "REVIEW_RECORD",
    "ENVIRONMENT_ATTESTATION",
}
DECLARED_TECHNICAL_TEST_IDS = {
    "C1-TST-DATA-001",
    "C1-TST-FS-001",
    "C1-TST-FS-002",
    "C1-TST-FS-003",
    "C1-TST-FS-004",
    "C1-TST-FS-005",
    "C1-TST-FS-006",
    "C1-TST-FS-007",
    "C1-TST-FS-008",
    "C1-TST-FS-009",
    "C1-TST-FS-010",
    "C1-TST-FS-011",
    "C1-TST-IO-001",
    "C1-TST-IO-002",
    "C1-TST-CAP-001",
    "C1-TST-CAP-002",
    "C1-TST-CAP-003",
    "C1-TST-CAP-005",
    "C1-TST-PWA-NET-001",
    "C1-TST-PWA-STORAGE-001",
    "C1-TST-PWA-BACKUP-001",
    "C1-TST-WEB-001",
    "C1-TST-WEB-002",
    "C1-TST-WEB-003",
    "C1-TST-SW-001",
    "C1-TST-SW-002",
    "C1-TST-SC-001",
    "C1-TST-PROV-001",
    "C1-TST-ORACLE-001",
    "C1-TST-QUALITY-001",
    "C1-TST-WIN-E2E-001",
    "C1-TST-BROWSER-MATRIX-001",
    "C1-TST-RECOVERY-001",
}
PROMOTION_REQUIRED_TEST_IDS = (
    DECLARED_TECHNICAL_TEST_IDS - {"C1-TST-PROV-001"}
)
ROLLBACK_REQUIRED_TEST_IDS = {
    "C1-TST-PROV-001",
    "C1-TST-RECOVERY-001",
    "C1-TST-SW-002",
}
PROMOTION_DEPENDENT_IDS = {
    "C1-GOV-002",
    "C1-GOV-005",
    "C1-GOV-006",
}
REQUIRED_GATES = {
    "independentReview",
    "manualSourceReview",
    "packageValidation",
    "pwaBrowserSmoke",
    "pwaUnitTests",
    "pwaUpdateSmoke",
    "course1CleanRoomMatrix",
    "sourceClaimsOnline",
    "supplyChainOnline",
}
REQUIRED_ROLLBACK_GATES = {
    "artifactIdentity",
    "lastKnownGoodAcceptance",
    "learnerStateRecoveryPlan",
    "rollbackAuthorized",
}
MANIFEST_ARTIFACT_FORMAT = "manifest-v1"
LEGACY_V25_ARTIFACT_FORMAT = "legacy-v2.5"
LEGACY_V25_COMMIT = "69d868a713d42b19b12ec11c64898b29e829be71"
LEGACY_V25_BUILD_ID = "ad5f59e8f800"
LEGACY_V25_CONTENT_HASH = (
    "ddc88ff3b2a9ac9080b05abebad5f578de122406a6bab00bb52b28a92353258a"
)
LEGACY_V25_TREE_SHA256 = (
    "df958cd62ff5ddd76cace021d86c46eb6f4a252215467487170639d72d84462d"
)
LEGACY_V25_ACCEPTANCE_PATH = (
    "release_evidence/COURSE_1_V2.5.0_ACCEPTANCE.md"
)
LEGACY_V25_ACCEPTANCE_SHA256 = (
    "eccb39d215b0378c02360b6323c7eceb7137d6542c438654b5fae573466269a5"
)
LEGACY_V25_FILES = {
    ".nojekyll",
    "app.js",
    "course-content.json",
    "favicon.svg",
    "icons/apple-touch-icon.png",
    "icons/icon-192.png",
    "icons/icon-512.png",
    "icons/icon-maskable-512.png",
    "index.html",
    "manifest.webmanifest",
    "markdown.js",
    "styles.css",
    "sw.js",
    "version.json",
}
MANIFEST_ASSET_PATHS = {
    "index.html",
    "bootstrap.js",
    "app.js",
    "markdown.js",
    "state.js",
    "styles.css",
    "favicon.svg",
    "course-content.json",
    "manifest.webmanifest",
    "version.json",
    "icons/icon-192.png",
    "icons/icon-512.png",
    "icons/icon-maskable-512.png",
    "icons/apple-touch-icon.png",
}
PUBLIC_SERVED_PATHS = MANIFEST_ASSET_PATHS | {
    "asset-manifest.json",
    "sw.js",
}
STUDY_PRODUCT_STATUS = "UNVERIFIED"
STUDY_DISTRIBUTION_PURPOSE = "personal-synthetic-study"
PROMOTION_DISTRIBUTION_PURPOSE = "accepted-release-candidate"


def reject_duplicate_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def read_object(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_bytes().decode("utf-8"),
        object_pairs_hook=reject_duplicate_json_keys,
    )
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def artifact_tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    files = sorted(
        (path for path in root.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(root).as_posix(),
    )
    if not files:
        raise ValueError(f"artifact directory contains no files: {root}")
    for path in files:
        relative = path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
        digest.update(b"\n")
    return digest.hexdigest()


def selected_tree_sha256(root: Path, relative_paths: set[str]) -> str:
    """Hash an exact named set using the same framing as the artifact tree."""

    digest = hashlib.sha256()
    if not relative_paths:
        raise ValueError("selected artifact tree contains no files")
    for relative in sorted(relative_paths):
        path = root / Path(*PurePosixPath(relative).parts)
        if not path.is_file():
            raise ValueError(f"selected artifact file is missing: {relative}")
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
        digest.update(b"\n")
    return digest.hexdigest()


def artifact_relative_files(root: Path) -> set[str]:
    return {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file()
    }


def require_exact_object_keys(
    value: Any,
    expected: set[str],
    label: str,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    actual = set(value)
    if actual != expected:
        raise ValueError(
            f"{label} keys must be exactly {sorted(expected)}; got {sorted(actual)}"
        )
    return value


def inspect_artifact_identity(
    dist: Path,
    *,
    expected_commit: str,
    operation: str,
) -> dict[str, Any]:
    artifact_root = dist.resolve()
    version = read_object(artifact_root / "version.json")
    legacy_version_keys = {
        "buildId",
        "bundleSchemaVersion",
        "programId",
        "courseId",
        "courseVersion",
        "verifiedThrough",
        "contentHash",
        "commit",
    }
    separated_date_version_keys = legacy_version_keys | {
        "sourceVerifiedThrough",
        "contentRevisionThrough",
    }
    release_version_keys = separated_date_version_keys | {
        "productStatus",
        "distributionPurpose",
    }
    actual_version_keys = set(version)
    if (
        actual_version_keys != legacy_version_keys
        and actual_version_keys != separated_date_version_keys
        and actual_version_keys != release_version_keys
    ):
        raise ValueError(
            "version.json keys must be exactly the current release shape, "
            "the earlier separated-date shape, or the legacy compatibility shape"
        )
    if (
        actual_version_keys != release_version_keys
        and operation in {"promote", "personal-study"}
    ):
        raise ValueError(
            f"{operation} version.json must contain separated dates and release metadata"
        )
    if actual_version_keys in (separated_date_version_keys, release_version_keys):
        if (
            not re.fullmatch(
                r"\d{4}-\d{2}-\d{2}",
                str(version.get("sourceVerifiedThrough", "")),
            )
            or not re.fullmatch(
                r"\d{4}-\d{2}-\d{2}",
                str(version.get("contentRevisionThrough", "")),
            )
            or version.get("verifiedThrough")
            != version.get("sourceVerifiedThrough")
        ):
            raise ValueError(
                "version.json separated date metadata is malformed or "
                "contradictory"
            )
    if actual_version_keys == release_version_keys:
        if version.get("productStatus") != STUDY_PRODUCT_STATUS:
            raise ValueError("version.json productStatus must be UNVERIFIED")
        purpose = version.get("distributionPurpose")
        expected_purpose = {
            "personal-study": STUDY_DISTRIBUTION_PURPOSE,
            "promote": PROMOTION_DISTRIBUTION_PURPOSE,
        }.get(operation)
        if expected_purpose is not None and purpose != expected_purpose:
            raise ValueError(
                f"{operation} requires distributionPurpose {expected_purpose}"
            )
        if operation == "rollback" and purpose not in {
            STUDY_DISTRIBUTION_PURPOSE,
            PROMOTION_DISTRIBUTION_PURPOSE,
        }:
            raise ValueError("rollback version.json has an unsupported distributionPurpose")
    if version.get("courseId") != "course-1-controlled-ai-workflow-foundations":
        raise ValueError("version.json is not Course 1")
    if not re.fullmatch(r"[0-9a-f]{12}", str(version.get("buildId", ""))):
        raise ValueError("version.json buildId is not 12 lowercase hex")
    if not HEX_64.fullmatch(str(version.get("contentHash", ""))):
        raise ValueError("version.json contentHash is not SHA-256")

    actual_files = artifact_relative_files(artifact_root)
    tree_hash = artifact_tree_sha256(artifact_root)
    manifest_path = artifact_root / "asset-manifest.json"
    if not manifest_path.is_file():
        if operation != "rollback":
            raise ValueError("promotion artifact is missing asset-manifest.json")
        expected_legacy = {
            "commit": LEGACY_V25_COMMIT,
            "courseVersion": "2.5.0",
            "buildId": LEGACY_V25_BUILD_ID,
            "contentHash": LEGACY_V25_CONTENT_HASH,
            "artifactTreeSha256": LEGACY_V25_TREE_SHA256,
        }
        actual_legacy = {
            "commit": expected_commit,
            "courseVersion": version.get("courseVersion"),
            "buildId": version.get("buildId"),
            "contentHash": version.get("contentHash"),
            "artifactTreeSha256": tree_hash,
        }
        if actual_legacy != expected_legacy:
            raise ValueError(
                "artifact without asset-manifest.json is not the exact accepted legacy v2.5 rollback"
            )
        if version.get("commit") != LEGACY_V25_COMMIT[:12]:
            raise ValueError(
                "legacy v2.5 version.json commit does not match its accepted source"
            )
        if actual_files != LEGACY_V25_FILES:
            raise ValueError(
                "legacy v2.5 artifact does not contain its exact historical file set"
            )
        return {
            "version": version,
            "artifactFormat": LEGACY_V25_ARTIFACT_FORMAT,
            "assetManifestSha256": None,
            "artifactTreeSha256": tree_hash,
        }

    if version.get("commit") != expected_commit:
        raise ValueError(
            "version.json commit must equal the full 40-character candidate commit"
        )
    manifest = read_object(manifest_path)
    require_exact_object_keys(
        manifest,
        {"schemaVersion", "buildId", "contentHash", "provenance", "assets"},
        "asset-manifest.json",
    )
    if manifest.get("schemaVersion") != 1:
        raise ValueError("asset-manifest.json schemaVersion must be 1")
    if (
        manifest.get("buildId") != version.get("buildId")
        or manifest.get("contentHash") != version.get("contentHash")
    ):
        raise ValueError("asset-manifest.json does not match version.json")
    provenance = require_exact_object_keys(
        manifest.get("provenance"),
        {"commit"},
        "asset-manifest.json provenance",
    )
    if provenance.get("commit") != expected_commit:
        raise ValueError(
            "asset-manifest.json provenance must equal the full candidate commit"
        )
    assets = manifest.get("assets")
    if not isinstance(assets, dict) or set(assets) != MANIFEST_ASSET_PATHS:
        raise ValueError(
            "asset-manifest.json does not contain the exact manifest-v1 asset set"
        )
    for relative_path, metadata_value in assets.items():
        metadata = require_exact_object_keys(
            metadata_value,
            {"sha256", "contentType"},
            f"asset-manifest.json asset {relative_path}",
        )
        asset_path = artifact_root / Path(*PurePosixPath(relative_path).parts)
        if not asset_path.is_file():
            raise ValueError(f"manifest asset is missing: {relative_path}")
        if metadata.get("sha256") != sha256(asset_path):
            raise ValueError(f"manifest asset hash does not match: {relative_path}")
        if not isinstance(metadata.get("contentType"), str) or not metadata[
            "contentType"
        ]:
            raise ValueError(f"manifest asset contentType is missing: {relative_path}")
    expected_files = MANIFEST_ASSET_PATHS | {
        ".nojekyll",
        "asset-manifest.json",
        "sw.js",
    }
    if actual_files != expected_files:
        raise ValueError("manifest-v1 artifact contains an unexpected file set")
    manifest_hash = sha256(manifest_path)
    service_worker = (artifact_root / "sw.js").read_text(encoding="utf-8")
    if (
        f'const BUILD_PROVENANCE = "{expected_commit}";' not in service_worker
        or f'const ASSET_MANIFEST_SHA256 = "{manifest_hash}";'
        not in service_worker
    ):
        raise ValueError(
            "service worker is not bound to the full commit and asset-manifest hash"
        )
    return {
        "version": version,
        "artifactFormat": MANIFEST_ARTIFACT_FORMAT,
        "assetManifestSha256": manifest_hash,
        "artifactTreeSha256": tree_hash,
        "publicServedTreeSha256": selected_tree_sha256(
            artifact_root,
            PUBLIC_SERVED_PATHS,
        ),
    }


def parse_timestamp(value: Any, label: str = "acceptedAt") -> dt.datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty ISO 8601 timestamp")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = dt.datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError(f"{label} must include a timezone")
    return parsed


def exact_keys(
    value: Any,
    expected: set[str],
    label: str,
    failures: list[str],
) -> dict[str, Any]:
    if not isinstance(value, dict):
        failures.append(f"{label} must be an object")
        return {}
    missing = sorted(expected - set(value))
    unknown = sorted(set(value) - expected)
    if missing:
        failures.append(f"{label} is missing required keys: {missing}")
    if unknown:
        failures.append(f"{label} has unknown keys: {unknown}")
    return value


def markdown_cells(line: str) -> list[str] | None:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return None
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def embedded_markdown_cells(line: str) -> list[str] | None:
    first_pipe = line.find("|")
    last_pipe = line.rfind("|")
    if first_pipe < 0 or last_pipe <= first_pipe:
        return None
    return markdown_cells(line[first_pipe : last_pipe + 1])


def without_blockquote_prefix(line: str) -> str:
    return re.sub(r"^(?:\s*>\s*)+", "", line)


def visible_markdown_line_indexes(lines: list[str]) -> set[int]:
    visible: set[int] = set()
    fence_character: str | None = None
    fence_length = 0
    for index, line in enumerate(lines):
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match is not None:
            marker = match.group(1)
            if fence_character is None:
                fence_character = marker[0]
                fence_length = len(marker)
            elif marker[0] == fence_character and len(marker) >= fence_length:
                fence_character = None
                fence_length = 0
            continue
        if fence_character is None:
            visible.add(index)
    return visible


def authoritative_product_status(
    ledger_text: str,
) -> tuple[str | None, list[str]]:
    failures: list[str] = []
    lines = ledger_text.splitlines()
    visible = visible_markdown_line_indexes(lines)
    matches = [
        match
        for index, line in enumerate(lines)
        if index in visible
        for match in [PRODUCT_STATUS_LINE.fullmatch(line)]
        if match is not None
    ]
    quoted_matches = [
        match
        for index, line in enumerate(lines)
        if index in visible and without_blockquote_prefix(line) != line
        for match in [
            PRODUCT_STATUS_LINE.fullmatch(without_blockquote_prefix(line))
        ]
        if match is not None
    ]
    embedded_markers = [
        index + 1
        for index, line in enumerate(lines)
        if index in visible
        and PRODUCT_STATUS_FRAGMENT.search(line) is not None
        and PRODUCT_STATUS_LINE.fullmatch(line) is None
    ]
    if embedded_markers:
        failures.append(
            "non-authoritative current-status text is not allowed on lines "
            f"{embedded_markers}"
        )
    if quoted_matches:
        failures.append(
            "quoted current-status markers are misleading and not allowed"
        )
    if len(matches) != 1:
        failures.append(
            "the authoritative ledger must contain exactly one unquoted "
            "current-status marker"
        )
        return None, failures
    status = matches[0].group("status")
    if status not in PRODUCT_STATUSES:
        failures.append(f"unsupported authoritative product status: {status}")
        return None, failures
    return status, failures


def parse_ledger_rows(ledger_text: str) -> tuple[dict[str, str], list[str]]:
    failures: list[str] = []
    rows: list[tuple[str, str]] = []
    lines = ledger_text.splitlines()
    visible = visible_markdown_line_indexes(lines)
    accounted_row_indexes: set[int] = set()
    header_indexes = [
        index
        for index, line in enumerate(lines)
        if index in visible
        and tuple(markdown_cells(line) or ()) == LEDGER_HEADER
    ]
    if not header_indexes:
        return {}, ["no authoritative High/Medium ledger tables were found"]

    for header_index in header_indexes:
        separator_index = header_index + 1
        if separator_index >= len(lines):
            failures.append(
                f"ledger table at line {header_index + 1} has no separator row"
            )
            continue
        separator = markdown_cells(lines[separator_index])
        if (
            separator is None
            or len(separator) != len(LEDGER_HEADER)
            or any(not re.fullmatch(r":?-{3,}:?", cell) for cell in separator)
        ):
            failures.append(
                f"ledger table at line {header_index + 1} has a malformed separator"
            )
            continue

        index = separator_index + 1
        while index < len(lines) and index in visible:
            cells = markdown_cells(lines[index])
            if cells is None:
                break
            accounted_row_indexes.add(index)
            line_number = index + 1
            if len(cells) != len(LEDGER_HEADER):
                failures.append(
                    f"ledger row {line_number} has {len(cells)} cells; expected 6"
                )
                index += 1
                continue
            finding_match = LEDGER_FINDING_ID.fullmatch(cells[0])
            if finding_match is None:
                failures.append(
                    f"ledger row {line_number} has a malformed or unsupported finding ID"
                )
                index += 1
                continue
            finding_id = finding_match.group(1)
            severity, requirement, evidence, status, owner = cells[1:]
            if severity not in {"High", "Medium"}:
                failures.append(
                    f"{finding_id} uses unsupported severity: {severity or '<missing>'}"
                )
            if not requirement:
                failures.append(f"{finding_id} requirement is missing")
            if not evidence:
                failures.append(f"{finding_id} closure test and evidence are missing")
            if status not in LEDGER_STATUSES:
                failures.append(
                    f"{finding_id} uses unsupported or missing status: {status or '<missing>'}"
                )
            if not owner:
                failures.append(f"{finding_id} owner is missing")
            rows.append((finding_id, status))
            index += 1

    for index, line in enumerate(lines):
        if index not in visible or index in accounted_row_indexes:
            continue
        cells = embedded_markdown_cells(line)
        has_severity_cell = re.search(
            r"(?:^|\|)\s*(?:High|Medium|Critical)\s*(?=\|)",
            line,
        ) is not None
        finding_like = (
            line.count("|") >= 4
            and ("C1-" in line or has_severity_cell)
        ) or (
            cells is not None
            and (
                (
                    len(cells) >= 2
                    and cells[1] in {"High", "Medium", "Critical"}
                )
                or (cells and "C1-" in cells[0])
            )
        )
        if finding_like:
            first_pipe = line.find("|")
            prefix = line[:first_pipe] if first_pipe >= 0 else line
            qualifier = (
                "quoted finding-like ledger row"
                if ">" in prefix
                else "embedded finding-like ledger row"
            )
            failures.append(
                f"{qualifier} {index + 1} is outside an exact authoritative table"
            )

    identifiers = [finding_id for finding_id, _ in rows]
    duplicates = sorted(
        identifier
        for identifier, count in Counter(identifiers).items()
        if count > 1
    )
    if duplicates:
        failures.append(f"duplicate High/Medium ledger finding IDs: {duplicates}")
    declared = set(identifiers)
    missing = sorted(EXPECTED_LEDGER_FINDING_IDS - declared)
    unknown = sorted(declared - EXPECTED_LEDGER_FINDING_IDS)
    if missing:
        failures.append(f"authoritative ledger finding rows are missing: {missing}")
    if unknown:
        failures.append(f"authoritative ledger has unknown finding IDs: {unknown}")
    return dict(rows), failures


def resolve_record(value: str, evidence_repository_root: Path) -> Path:
    if not isinstance(value, str) or not re.fullmatch(
        r"release_evidence/(?!templates/)[A-Za-z0-9._/-]+\.json",
        value,
    ):
        raise ValueError(
            "acceptance record must name a non-template JSON file inside release_evidence/"
        )
    relative = PurePosixPath(value)
    if "//" in value or any(
        part in {"", ".", ".."} for part in relative.parts
    ):
        raise ValueError(
            "acceptance record must not contain empty, dot, or parent segments"
        )
    repository_root = evidence_repository_root.resolve()
    release_evidence_root = repository_root / "release_evidence"
    candidate = (repository_root / Path(*relative.parts)).resolve()
    try:
        candidate.relative_to(release_evidence_root.resolve())
    except ValueError as exc:
        raise ValueError(
            "acceptance record must be inside release_evidence/"
        ) from exc
    if candidate.suffix.casefold() != ".json":
        raise ValueError("acceptance record must be JSON")
    return candidate


def validate_ledger(
    ledger_text: str,
    recorded_promotion_dependent_ids: Any,
) -> list[str]:
    product_status, status_failures = authoritative_product_status(ledger_text)
    rows, row_failures = parse_ledger_rows(ledger_text)
    failures = [*status_failures, *row_failures]
    if product_status is not None and product_status != "UNVERIFIED":
        failures.append(
            "the authoritative ledger must be UNVERIFIED before promotion; "
            "REPAIR REQUIRED and PASS are not promotable pre-release states"
        )
    if not rows:
        return failures + ["no High or Medium ledger rows could be parsed"]

    open_ids = sorted(
        finding_id
        for finding_id, status in rows.items()
        if status in {"OPEN", "REOPENED"}
    )
    if open_ids:
        failures.append(f"open or reopened High/Medium findings remain: {open_ids}")

    partial_ids = sorted(
        finding_id
        for finding_id, status in rows.items()
        if status == "PARTIAL"
    )
    if partial_ids:
        failures.append(
            "High/Medium findings remain partially implemented: "
            f"{partial_ids}"
        )

    evidence_pending_ids = {
        finding_id
        for finding_id, status in rows.items()
        if status == "EVIDENCE PENDING"
    }
    unexpected_evidence_pending = sorted(
        evidence_pending_ids - PROMOTION_DEPENDENT_IDS
    )
    if unexpected_evidence_pending:
        failures.append(
            "non-promotion-dependent High/Medium evidence remains pending: "
            f"{unexpected_evidence_pending}"
        )

    expected_recorded = sorted(evidence_pending_ids & PROMOTION_DEPENDENT_IDS)
    if recorded_promotion_dependent_ids != expected_recorded:
        failures.append(
            "promotionDependentFindingIds must exactly identify the remaining "
            f"promotion-dependent evidence-pending findings: {expected_recorded}"
        )
    return failures


def declared_test_definitions() -> dict[str, dict[str, Any]]:
    path = ROOT / "audit_control/course1/technical_test_manifest.json"
    manifest = read_object(path)
    failures: list[str] = []
    exact_keys(
        manifest,
        {"schemaVersion", "courseId", "graphPath", "tests"},
        "technical test manifest",
        failures,
    )
    if manifest.get("schemaVersion") != "course1-technical-test-manifest-v1":
        failures.append("technical test manifest schemaVersion is unsupported")
    if manifest.get("courseId") != "course-1-controlled-ai-workflow-foundations":
        failures.append("technical test manifest courseId is not Course 1")
    rows = manifest.get("tests")
    if not isinstance(rows, list):
        failures.append("technical test manifest tests must be an array")
        rows = []
    definitions: dict[str, dict[str, Any]] = {}
    identifiers: list[str] = []
    for index, raw in enumerate(rows):
        row = exact_keys(
            raw,
            {
                "id",
                "type",
                "owner",
                "environments",
                "evidenceClass",
                "procedures",
                "currentEvidence",
            },
            f"technical test manifest tests[{index}]",
            failures,
        )
        test_id = row.get("id")
        evidence_class = row.get("evidenceClass")
        if test_id not in DECLARED_TECHNICAL_TEST_IDS:
            failures.append(
                f"technical test manifest tests[{index}].id is undeclared"
            )
            continue
        identifiers.append(test_id)
        if evidence_class not in TECHNICAL_EVIDENCE_CLASSES:
            failures.append(f"{test_id}.evidenceClass is unsupported")
            continue
        environments = row.get("environments")
        if (
            not isinstance(environments, list)
            or not environments
            or any(
                not isinstance(environment, str) or not environment.strip()
                for environment in environments
            )
            or len(environments) != len(set(environments))
        ):
            failures.append(
                f"{test_id}.environments must be non-empty unique strings"
            )
            environments = []

        procedures = row.get("procedures")
        procedure_bindings: list[tuple[str, str]] = []
        if not isinstance(procedures, list) or not procedures:
            failures.append(f"{test_id}.procedures must be a non-empty array")
            procedures = []
        for procedure_index, raw_procedure in enumerate(procedures):
            procedure_label = f"{test_id}.procedures[{procedure_index}]"
            procedure = exact_keys(
                raw_procedure,
                {"locator", "selector", "command", "expected"},
                procedure_label,
                failures,
            )
            for field in ("locator", "selector", "command", "expected"):
                if (
                    not isinstance(procedure.get(field), str)
                    or not procedure[field].strip()
                ):
                    failures.append(
                        f"{procedure_label}.{field} must be recorded"
                    )
            locator = procedure.get("locator")
            selector = procedure.get("selector")
            if not isinstance(locator, str) or not isinstance(selector, str):
                continue
            relative = PurePosixPath(locator)
            if (
                relative.is_absolute()
                or "\\" in locator
                or any(part in {"", ".", ".."} for part in relative.parts)
            ):
                failures.append(
                    f"{procedure_label}.locator is not a safe repository path"
                )
                continue
            locator_path = (ROOT / Path(*relative.parts)).resolve()
            try:
                locator_path.relative_to(ROOT.resolve())
            except ValueError:
                failures.append(
                    f"{procedure_label}.locator escapes the repository"
                )
                continue
            if not locator_path.is_file():
                failures.append(
                    f"{procedure_label}.locator does not exist: {locator}"
                )
                continue
            try:
                locator_text = locator_path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                failures.append(
                    f"{procedure_label}.locator could not be read: {exc}"
                )
                continue
            if selector not in locator_text:
                failures.append(
                    f"{procedure_label}.selector is absent from {locator}"
                )
            procedure_bindings.append((locator, selector))
        if len(procedure_bindings) != len(set(procedure_bindings)):
            failures.append(
                f"{test_id}.procedures contain duplicate locator/selector bindings"
            )
        definitions[test_id] = {
            "evidenceClass": evidence_class,
            "environments": tuple(environments),
            "procedures": tuple(procedure_bindings),
        }
    duplicates = sorted(
        identifier
        for identifier, count in Counter(identifiers).items()
        if count > 1
    )
    if duplicates:
        failures.append(f"technical test manifest has duplicate IDs: {duplicates}")
    if set(definitions) != DECLARED_TECHNICAL_TEST_IDS:
        failures.append(
            "technical test manifest does not exactly cover all declared tests"
        )
    if failures:
        raise ValueError("; ".join(failures))
    return definitions


def resolve_evidence_file(value: Any, evidence_repository_root: Path) -> Path:
    if not isinstance(value, str) or not re.fullmatch(
        r"release_evidence/(?!templates/)[A-Za-z0-9._/-]+\.json",
        value,
    ):
        raise ValueError(
            "evidence.path must name a non-template JSON file inside release_evidence/"
        )
    relative = PurePosixPath(value)
    if "//" in value or any(
        part in {"", ".", ".."} for part in relative.parts
    ):
        raise ValueError("evidence.path must not contain empty, dot, or parent segments")
    repository_root = evidence_repository_root.resolve()
    evidence_root = (repository_root / "release_evidence").resolve()
    candidate = (repository_root / Path(*relative.parts)).resolve()
    try:
        candidate.relative_to(evidence_root)
    except ValueError as exc:
        raise ValueError("evidence.path escapes release_evidence/") from exc
    if not candidate.is_file():
        raise ValueError(f"evidence file does not exist: {value}")
    return candidate


def resolve_evidence_artifact_file(
    value: Any,
    evidence_repository_root: Path,
) -> Path:
    if not isinstance(value, str) or not re.fullmatch(
        r"release_evidence/(?!templates(?:/|$))[A-Za-z0-9._/-]+\.[A-Za-z0-9]+",
        value,
    ):
        raise ValueError(
            "artifact.path must name a non-template file inside release_evidence/"
        )
    relative = PurePosixPath(value)
    if "//" in value or any(
        part in {"", ".", ".."} for part in relative.parts
    ):
        raise ValueError(
            "artifact.path must not contain empty, dot, or parent segments"
        )
    repository_root = evidence_repository_root.resolve()
    evidence_root = (repository_root / "release_evidence").resolve()
    candidate = (repository_root / Path(*relative.parts)).resolve()
    try:
        candidate.relative_to(evidence_root)
    except ValueError as exc:
        raise ValueError("artifact.path escapes release_evidence/") from exc
    if not candidate.is_file():
        raise ValueError(f"artifact file does not exist: {value}")
    return candidate


def validate_last_known_good_acceptance(
    raw_locator: Any,
    *,
    candidate: dict[str, Any],
    evidence_repository_root: Path | None,
    rollback_accepted_at: dt.datetime | None,
    artifact_format: str,
) -> list[str]:
    failures: list[str] = []
    label = "rollback.lastKnownGoodAcceptanceRecord"
    locator = exact_keys(
        raw_locator,
        {"path", "sha256"},
        label,
        failures,
    )
    if evidence_repository_root is None:
        return failures + [
            "an evidence repository root is required to verify the last-known-good acceptance"
        ]
    path_value = locator.get("path")
    expected_hash = locator.get("sha256")
    if not isinstance(expected_hash, str) or not HEX_64.fullmatch(expected_hash):
        failures.append(f"{label}.sha256 must be lowercase SHA-256")

    if artifact_format == LEGACY_V25_ARTIFACT_FORMAT:
        if path_value != LEGACY_V25_ACCEPTANCE_PATH:
            failures.append(
                f"{label}.path must be the exact historical v2.5 acceptance record"
            )
            return failures
        acceptance_path = (
            evidence_repository_root.resolve()
            / Path(*PurePosixPath(LEGACY_V25_ACCEPTANCE_PATH).parts)
        ).resolve()
        evidence_root = (
            evidence_repository_root.resolve() / "release_evidence"
        ).resolve()
        try:
            acceptance_path.relative_to(evidence_root)
        except ValueError:
            failures.append(f"{label}.path escapes release_evidence/")
            return failures
        if not acceptance_path.is_file():
            failures.append(
                f"{label}.path does not exist: {LEGACY_V25_ACCEPTANCE_PATH}"
            )
            return failures
        try:
            acceptance_bytes = acceptance_path.read_bytes()
        except OSError as exc:
            failures.append(f"{label}.path could not be read: {exc}")
            return failures
        actual_hash = hashlib.sha256(acceptance_bytes).hexdigest()
        if (
            expected_hash != actual_hash
            or actual_hash != LEGACY_V25_ACCEPTANCE_SHA256
        ):
            failures.append(
                f"{label} does not match the immutable historical v2.5 acceptance"
            )
        return failures

    if artifact_format != MANIFEST_ARTIFACT_FORMAT:
        failures.append(f"{label} cannot verify an unsupported artifact format")
        return failures
    try:
        acceptance_path = resolve_evidence_file(
            path_value,
            evidence_repository_root,
        )
    except (OSError, ValueError, TypeError) as exc:
        failures.append(f"{label}: {exc}")
        return failures
    try:
        acceptance_bytes = acceptance_path.read_bytes()
    except OSError as exc:
        failures.append(f"{label}.path could not be read: {exc}")
        return failures
    if expected_hash != hashlib.sha256(acceptance_bytes).hexdigest():
        failures.append(f"{label}.sha256 does not match the acceptance file")
    try:
        acceptance = json.loads(
            acceptance_bytes.decode("utf-8"),
            object_pairs_hook=reject_duplicate_json_keys,
        )
        if not isinstance(acceptance, dict):
            raise ValueError("top-level acceptance JSON must be one object")
    except (UnicodeError, ValueError, json.JSONDecodeError) as exc:
        failures.append(f"{label}.path is not valid closed JSON: {exc}")
        return failures

    acceptance_label = f"{label} record"
    exact_keys(
        acceptance,
        {
            "schemaVersion",
            "decision",
            "courseId",
            "candidate",
            "acceptedAt",
            "reviewer",
            "gates",
            "promotionDependentFindingIds",
            "evidence",
        },
        acceptance_label,
        failures,
    )
    if acceptance.get("schemaVersion") != 1:
        failures.append(f"{acceptance_label}.schemaVersion must be 1")
    if acceptance.get("decision") != "ACCEPTED_FOR_PROMOTION":
        failures.append(
            f"{acceptance_label}.decision must be ACCEPTED_FOR_PROMOTION"
        )
    if (
        acceptance.get("courseId")
        != "course-1-controlled-ai-workflow-foundations"
    ):
        failures.append(f"{acceptance_label}.courseId is not Course 1")

    prior_candidate = exact_keys(
        acceptance.get("candidate"),
        {
            "artifactFormat",
            "commit",
            "courseVersion",
            "buildId",
            "contentHash",
            "assetManifestSha256",
            "artifactTreeSha256",
        },
        f"{acceptance_label}.candidate",
        failures,
    )
    if prior_candidate != candidate:
        failures.append(
            f"{acceptance_label}.candidate does not exactly match the rollback target"
        )
    if prior_candidate.get("artifactFormat") != MANIFEST_ARTIFACT_FORMAT:
        failures.append(
            f"{acceptance_label}.candidate.artifactFormat must be manifest-v1"
        )

    prior_accepted_at: dt.datetime | None = None
    try:
        prior_accepted_at = parse_timestamp(
            acceptance.get("acceptedAt"),
            f"{acceptance_label}.acceptedAt",
        )
    except (TypeError, ValueError) as exc:
        failures.append(str(exc))
    if (
        prior_accepted_at is not None
        and rollback_accepted_at is not None
        and prior_accepted_at > rollback_accepted_at
    ):
        failures.append(
            f"{acceptance_label}.acceptedAt is after the rollback authorization"
        )

    reviewer = exact_keys(
        acceptance.get("reviewer"),
        {"name", "independentOfImplementation"},
        f"{acceptance_label}.reviewer",
        failures,
    )
    if not isinstance(reviewer.get("name"), str) or not reviewer["name"].strip():
        failures.append(f"{acceptance_label}.reviewer.name must be recorded")
    if reviewer.get("independentOfImplementation") is not True:
        failures.append(
            f"{acceptance_label}.reviewer.independentOfImplementation must be true"
        )

    gates = acceptance.get("gates")
    if not isinstance(gates, dict):
        failures.append(f"{acceptance_label}.gates must be an object")
    else:
        missing_or_false = sorted(
            gate for gate in REQUIRED_GATES if gates.get(gate) is not True
        )
        unknown = sorted(set(gates) - REQUIRED_GATES)
        if missing_or_false:
            failures.append(
                f"{acceptance_label}.gates are missing or false: {missing_or_false}"
            )
        if unknown:
            failures.append(
                f"{acceptance_label}.gates contain unknown keys: {unknown}"
            )

    prior_promotion_ids = acceptance.get("promotionDependentFindingIds")
    if (
        not isinstance(prior_promotion_ids, list)
        or prior_promotion_ids != sorted(prior_promotion_ids)
        or len(prior_promotion_ids) != len(set(prior_promotion_ids))
        or any(
            finding_id not in PROMOTION_DEPENDENT_IDS
            for finding_id in prior_promotion_ids
        )
    ):
        failures.append(
            f"{acceptance_label}.promotionDependentFindingIds must be a "
            "sorted unique subset of the controlled promotion set"
        )
    failures.extend(
        validate_technical_evidence(
            acceptance.get("evidence"),
            candidate=prior_candidate,
            evidence_repository_root=evidence_repository_root,
            required_test_ids=PROMOTION_REQUIRED_TEST_IDS,
            accepted_at=prior_accepted_at,
        )
    )
    return failures


def validate_technical_evidence(
    evidence: Any,
    *,
    candidate: dict[str, Any],
    evidence_repository_root: Path | None,
    required_test_ids: set[str],
    accepted_at: dt.datetime | None,
) -> list[str]:
    failures: list[str] = []
    if (
        not isinstance(evidence, list)
        or not evidence
        or any(not isinstance(item, dict) for item in evidence)
    ):
        return ["evidence must be a non-empty list of closed evidence objects"]
    if evidence_repository_root is None:
        return ["an evidence repository root is required to verify evidence files"]
    try:
        expected_test_definitions = declared_test_definitions()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"technical test manifest is not trustworthy: {exc}"]

    paths: list[str] = []
    artifact_paths: list[str] = []
    evidence_ids: list[str] = []
    test_ids: list[str] = []
    for index, raw_locator in enumerate(evidence):
        locator_label = f"evidence[{index}]"
        locator = exact_keys(
            raw_locator,
            {"path", "sha256"},
            locator_label,
            failures,
        )
        path_value = locator.get("path")
        if isinstance(path_value, str):
            paths.append(path_value)
        expected_hash = locator.get("sha256")
        if not isinstance(expected_hash, str) or not HEX_64.fullmatch(expected_hash):
            failures.append(f"{locator_label}.sha256 must be lowercase SHA-256")
        try:
            evidence_path = resolve_evidence_file(
                path_value,
                evidence_repository_root,
            )
        except (OSError, ValueError, TypeError) as exc:
            failures.append(f"{locator_label}: {exc}")
            continue
        try:
            evidence_bytes = evidence_path.read_bytes()
        except OSError as exc:
            failures.append(f"{locator_label}.path could not be read: {exc}")
            continue
        if expected_hash != hashlib.sha256(evidence_bytes).hexdigest():
            failures.append(f"{locator_label}.sha256 does not match the evidence file")
        try:
            evidence_record = json.loads(
                evidence_bytes.decode("utf-8"),
                object_pairs_hook=reject_duplicate_json_keys,
            )
            if not isinstance(evidence_record, dict):
                raise ValueError("top-level evidence JSON must be one object")
        except (UnicodeError, ValueError, json.JSONDecodeError) as exc:
            failures.append(f"{locator_label}.path is not valid closed JSON: {exc}")
            continue

        record_label = f"{locator_label} record"
        record = exact_keys(
            evidence_record,
            {
                "schemaVersion",
                "evidenceId",
                "testId",
                "candidate",
                "result",
                "evidenceClass",
                "recordedAt",
                "reviewer",
                "artifacts",
            },
            record_label,
            failures,
        )
        if record.get("schemaVersion") != "course1-technical-evidence-v1":
            failures.append(f"{record_label}.schemaVersion is unsupported")
        evidence_id = record.get("evidenceId")
        if not isinstance(evidence_id, str) or not TECHNICAL_EVIDENCE_ID.fullmatch(
            evidence_id
        ):
            failures.append(f"{record_label}.evidenceId is malformed")
        else:
            evidence_ids.append(evidence_id)
        if (
            not isinstance(record.get("testId"), str)
            or not TECHNICAL_TEST_ID.fullmatch(record["testId"])
            or record["testId"] not in DECLARED_TECHNICAL_TEST_IDS
        ):
            failures.append(f"{record_label}.testId is malformed or undeclared")
            test_id: str | None = None
        else:
            test_id = record["testId"]
            test_ids.append(test_id)
        if record.get("result") != "PASS":
            failures.append(f"{record_label}.result must be PASS")
        if record.get("evidenceClass") not in TECHNICAL_EVIDENCE_CLASSES:
            failures.append(f"{record_label}.evidenceClass is unsupported")
        elif (
            test_id is not None
            and test_id in expected_test_definitions
            and record.get("evidenceClass")
            != expected_test_definitions[test_id]["evidenceClass"]
        ):
            failures.append(
                f"{record_label}.evidenceClass does not match the declared test"
            )
        recorded_at: dt.datetime | None = None
        try:
            recorded_at = parse_timestamp(
                record.get("recordedAt"),
                f"{record_label}.recordedAt",
            )
        except (TypeError, ValueError) as exc:
            failures.append(str(exc))
        if (
            recorded_at is not None
            and accepted_at is not None
            and recorded_at > accepted_at
        ):
            failures.append(
                f"{record_label}.recordedAt is after the acceptance decision"
            )

        evidence_candidate = exact_keys(
            record.get("candidate"),
            {"commit", "courseVersion", "buildId", "contentHash"},
            f"{record_label}.candidate",
            failures,
        )
        for field in ("commit", "courseVersion", "buildId", "contentHash"):
            if evidence_candidate.get(field) != candidate.get(field):
                failures.append(
                    f"{record_label}.candidate.{field} does not match the acceptance candidate"
                )
        if not HEX_40.fullmatch(str(evidence_candidate.get("commit", ""))):
            failures.append(f"{record_label}.candidate.commit must be a full Git SHA")
        if not re.fullmatch(
            r"\d+\.\d+\.\d+",
            str(evidence_candidate.get("courseVersion", "")),
        ):
            failures.append(
                f"{record_label}.candidate.courseVersion must use x.y.z"
            )
        if not re.fullmatch(
            r"[0-9a-f]{12}",
            str(evidence_candidate.get("buildId", "")),
        ):
            failures.append(
                f"{record_label}.candidate.buildId must be 12 lowercase hex"
            )
        if not HEX_64.fullmatch(str(evidence_candidate.get("contentHash", ""))):
            failures.append(
                f"{record_label}.candidate.contentHash must be SHA-256"
            )

        reviewer = exact_keys(
            record.get("reviewer"),
            {"name", "independentOfImplementation"},
            f"{record_label}.reviewer",
            failures,
        )
        if not isinstance(reviewer.get("name"), str) or not reviewer["name"].strip():
            failures.append(f"{record_label}.reviewer.name must be recorded")
        if not isinstance(reviewer.get("independentOfImplementation"), bool):
            failures.append(
                f"{record_label}.reviewer.independentOfImplementation must be boolean"
            )
        elif (
            record.get("evidenceClass") == "INDEPENDENT_REVIEW"
            and reviewer.get("independentOfImplementation") is not True
        ):
            failures.append(
                f"{record_label} independent-review evidence requires an independent reviewer"
            )

        raw_artifacts = record.get("artifacts")
        if (
            not isinstance(raw_artifacts, list)
            or not raw_artifacts
            or any(not isinstance(item, dict) for item in raw_artifacts)
        ):
            failures.append(
                f"{record_label}.artifacts must be a non-empty list of closed artifact objects"
            )
            raw_artifacts = []

        expected_procedures: set[tuple[str, str]] = set()
        expected_environments: set[str] = set()
        if test_id is not None and test_id in expected_test_definitions:
            definition = expected_test_definitions[test_id]
            expected_procedures = set(definition["procedures"])
            expected_environments = set(definition["environments"])
        actual_bindings: list[tuple[str, str, str, str]] = []
        actual_procedures: set[tuple[str, str]] = set()
        actual_environments: set[str] = set()
        record_artifact_paths: list[str] = []
        for artifact_index, raw_artifact in enumerate(raw_artifacts):
            artifact_label = (
                f"{record_label}.artifacts[{artifact_index}]"
            )
            artifact = exact_keys(
                raw_artifact,
                {
                    "path",
                    "sha256",
                    "kind",
                    "procedureLocator",
                    "procedureSelector",
                    "environment",
                },
                artifact_label,
                failures,
            )
            artifact_path_value = artifact.get("path")
            if isinstance(artifact_path_value, str):
                artifact_paths.append(artifact_path_value)
                record_artifact_paths.append(artifact_path_value)
                if artifact_path_value == path_value:
                    failures.append(
                        f"{artifact_label}.path cannot be its own evidence record"
                    )
            artifact_hash = artifact.get("sha256")
            if (
                not isinstance(artifact_hash, str)
                or not HEX_64.fullmatch(artifact_hash)
            ):
                failures.append(
                    f"{artifact_label}.sha256 must be lowercase SHA-256"
                )
            artifact_kind = artifact.get("kind")
            if artifact_kind not in TECHNICAL_ARTIFACT_KINDS:
                failures.append(f"{artifact_label}.kind is unsupported")
            binding_values = (
                artifact.get("procedureLocator"),
                artifact.get("procedureSelector"),
                artifact.get("environment"),
            )
            if all(
                isinstance(value, str) and value.strip()
                for value in binding_values
            ) and isinstance(artifact_kind, str):
                procedure_binding = (
                    binding_values[0],
                    binding_values[1],
                )
                actual_procedures.add(procedure_binding)  # type: ignore[arg-type]
                actual_environments.add(binding_values[2])  # type: ignore[arg-type]
                actual_bindings.append(
                    (
                        binding_values[0],
                        binding_values[1],
                        binding_values[2],
                        artifact_kind,
                    )
                )  # type: ignore[arg-type]
            else:
                failures.append(
                    f"{artifact_label} procedure and environment binding must be recorded"
                )
            try:
                artifact_path = resolve_evidence_artifact_file(
                    artifact_path_value,
                    evidence_repository_root,
                )
            except (OSError, ValueError, TypeError) as exc:
                failures.append(f"{artifact_label}: {exc}")
                continue
            try:
                artifact_bytes = artifact_path.read_bytes()
            except OSError as exc:
                failures.append(f"{artifact_label}.path could not be read: {exc}")
                continue
            if not artifact_bytes:
                failures.append(f"{artifact_label}.path is empty")
            if artifact_hash != hashlib.sha256(artifact_bytes).hexdigest():
                failures.append(
                    f"{artifact_label}.sha256 does not match the artifact file"
                )

        duplicate_record_artifact_paths = sorted(
            path
            for path, count in Counter(record_artifact_paths).items()
            if count > 1
        )
        duplicate_bindings = sorted(
            binding
            for binding, count in Counter(actual_bindings).items()
            if count > 1
        )
        if duplicate_record_artifact_paths:
            failures.append(
                f"{record_label} has duplicate artifact paths: "
                f"{duplicate_record_artifact_paths}"
            )
        if duplicate_bindings:
            failures.append(
                f"{record_label} has duplicate procedure/environment bindings: "
                f"{duplicate_bindings}"
            )
        missing_procedures = sorted(expected_procedures - actual_procedures)
        unexpected_procedures = sorted(actual_procedures - expected_procedures)
        missing_environments = sorted(
            expected_environments - actual_environments
        )
        unexpected_environments = sorted(
            actual_environments - expected_environments
        )
        if missing_procedures:
            failures.append(
                f"{record_label} is missing declared procedure artifact "
                f"coverage: {missing_procedures}"
            )
        if unexpected_procedures:
            failures.append(
                f"{record_label} has undeclared procedure artifact "
                f"bindings: {unexpected_procedures}"
            )
        if missing_environments:
            failures.append(
                f"{record_label} is missing declared environment artifact "
                f"coverage: {missing_environments}"
            )
        if unexpected_environments:
            failures.append(
                f"{record_label} has undeclared environment artifact "
                f"bindings: {unexpected_environments}"
            )

    duplicate_paths = sorted(
        path for path, count in Counter(paths).items() if count > 1
    )
    duplicate_evidence_ids = sorted(
        evidence_id
        for evidence_id, count in Counter(evidence_ids).items()
        if count > 1
    )
    duplicate_test_ids = sorted(
        test_id
        for test_id, count in Counter(test_ids).items()
        if count > 1
    )
    if duplicate_paths:
        failures.append(f"duplicate evidence paths: {duplicate_paths}")
    duplicate_artifact_paths = sorted(
        path for path, count in Counter(artifact_paths).items() if count > 1
    )
    if duplicate_artifact_paths:
        failures.append(
            f"duplicate raw artifact paths: {duplicate_artifact_paths}"
        )
    if duplicate_evidence_ids:
        failures.append(f"duplicate evidence IDs: {duplicate_evidence_ids}")
    if duplicate_test_ids:
        failures.append(
            f"duplicate technical test evidence: {duplicate_test_ids}"
        )
    missing_test_ids = sorted(required_test_ids - set(test_ids))
    unexpected_test_ids = sorted(set(test_ids) - required_test_ids)
    if missing_test_ids:
        failures.append(
            f"required technical test evidence is missing: {missing_test_ids}"
        )
    if unexpected_test_ids:
        failures.append(
            f"technical test evidence is outside this operation: {unexpected_test_ids}"
        )
    return failures


def validate(
    record: dict[str, Any],
    version: dict[str, Any],
    *,
    expected_commit: str,
    asset_manifest_sha256: str | None,
    artifact_tree_sha256_value: str,
    ledger_text: str,
    operation: str,
    evidence_repository_root: Path | None = None,
    artifact_format: str = MANIFEST_ARTIFACT_FORMAT,
) -> list[str]:
    failures: list[str] = []
    expected_record_keys = (
        {
            "schemaVersion",
            "decision",
            "courseId",
            "candidate",
            "acceptedAt",
            "reviewer",
            "gates",
            "promotionDependentFindingIds",
            "evidence",
        }
        if operation == "promote"
        else {
            "schemaVersion",
            "decision",
            "courseId",
            "candidate",
            "acceptedAt",
            "authorizedBy",
            "gates",
            "rollback",
            "evidence",
        }
    )
    exact_keys(record, expected_record_keys, "acceptance record", failures)
    if record.get("schemaVersion") != 1:
        failures.append("schemaVersion must be 1")
    expected_decision = (
        "ACCEPTED_FOR_PROMOTION"
        if operation == "promote"
        else "ACCEPTED_FOR_ROLLBACK"
    )
    if record.get("decision") != expected_decision:
        failures.append(f"decision must be {expected_decision}")
    if record.get("courseId") != "course-1-controlled-ai-workflow-foundations":
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
    comparisons = {
        "artifactFormat": artifact_format,
        "commit": expected_commit,
        "courseVersion": version.get("courseVersion"),
        "buildId": version.get("buildId"),
        "contentHash": version.get("contentHash"),
        "assetManifestSha256": asset_manifest_sha256,
        "artifactTreeSha256": artifact_tree_sha256_value,
    }
    for field, expected in comparisons.items():
        if candidate.get(field) != expected:
            failures.append(
                f"candidate.{field} does not match the inspected artifact"
            )

    if artifact_format == MANIFEST_ARTIFACT_FORMAT:
        if version.get("commit") != expected_commit:
            failures.append(
                "version.json commit does not match the full workflow commit"
            )
        if not isinstance(asset_manifest_sha256, str) or not HEX_64.fullmatch(
            asset_manifest_sha256
        ):
            failures.append(
                "manifest-v1 artifact requires an asset-manifest SHA-256"
            )
    elif artifact_format == LEGACY_V25_ARTIFACT_FORMAT:
        if operation != "rollback":
            failures.append("legacy-v2.5 artifact format is rollback-only")
        if expected_commit != LEGACY_V25_COMMIT:
            failures.append("legacy-v2.5 rollback commit is not allowlisted")
        if version.get("commit") != LEGACY_V25_COMMIT[:12]:
            failures.append(
                "legacy v2.5 version.json commit does not match its accepted source"
            )
        if asset_manifest_sha256 is not None:
            failures.append(
                "legacy-v2.5 artifact must not claim an asset-manifest SHA-256"
            )
        if (
            version.get("courseVersion") != "2.5.0"
            or version.get("buildId") != LEGACY_V25_BUILD_ID
            or version.get("contentHash") != LEGACY_V25_CONTENT_HASH
            or artifact_tree_sha256_value != LEGACY_V25_TREE_SHA256
        ):
            failures.append("legacy-v2.5 artifact identity is not exact")
    else:
        failures.append("artifact format is unsupported")
    if not HEX_64.fullmatch(str(version.get("contentHash", ""))):
        failures.append("version.json contentHash is not SHA-256")
    if not re.fullmatch(r"[0-9a-f]{12}", str(version.get("buildId", ""))):
        failures.append("version.json buildId is not the expected 12-hex identity")

    reviewer_field = "reviewer" if operation == "promote" else "authorizedBy"
    reviewer = exact_keys(
        record.get(reviewer_field),
        (
            {"name", "independentOfImplementation"}
            if operation == "promote"
            else {"name"}
        ),
        reviewer_field,
        failures,
    )
    if not isinstance(reviewer.get("name"), str) or not reviewer["name"].strip():
        failures.append(f"{reviewer_field}.name must be recorded")
    if (
        operation == "promote"
        and reviewer.get("independentOfImplementation") is not True
    ):
        failures.append("reviewer.independentOfImplementation must be true")

    accepted_at: dt.datetime | None = None
    try:
        accepted_at = parse_timestamp(record.get("acceptedAt"))
    except (TypeError, ValueError) as exc:
        failures.append(str(exc))

    required_gates = (
        REQUIRED_GATES if operation == "promote" else REQUIRED_ROLLBACK_GATES
    )
    gates = record.get("gates")
    if not isinstance(gates, dict):
        failures.append("gates must be an object")
    else:
        missing_or_false = sorted(
            gate for gate in required_gates if gates.get(gate) is not True
        )
        extra = sorted(set(gates) - required_gates)
        if missing_or_false:
            failures.append(f"required acceptance gates are not true: {missing_or_false}")
        if extra:
            failures.append(f"unknown acceptance gates must be removed: {extra}")

    failures.extend(
        validate_technical_evidence(
            record.get("evidence"),
            candidate=candidate,
            evidence_repository_root=evidence_repository_root,
            required_test_ids=(
                PROMOTION_REQUIRED_TEST_IDS
                if operation == "promote"
                else ROLLBACK_REQUIRED_TEST_IDS
            ),
            accepted_at=accepted_at,
        )
    )

    if operation == "promote":
        failures.extend(
            validate_ledger(
                ledger_text,
                record.get("promotionDependentFindingIds"),
            )
        )
    else:
        product_status, status_failures = authoritative_product_status(ledger_text)
        rollback_rows, row_failures = parse_ledger_rows(ledger_text)
        failures.extend(status_failures)
        failures.extend(row_failures)
        if not rollback_rows:
            failures.append("no High or Medium ledger rows could be parsed")
        if product_status not in {"REPAIR REQUIRED", "UNVERIFIED"}:
            failures.append(
                "rollback requires an authoritative REPAIR REQUIRED or UNVERIFIED state"
            )
        rollback = exact_keys(
            record.get("rollback"),
            {
                "failedCandidateCommit",
                "trigger",
                "lastKnownGoodAcceptanceRecord",
                "learnerStateRisk",
            },
            "rollback",
            failures,
        )
        failed_commit = str(rollback.get("failedCandidateCommit", "")).casefold()
        if not HEX_40.fullmatch(failed_commit):
            failures.append(
                "rollback.failedCandidateCommit must be a full Git SHA"
            )
        elif failed_commit == expected_commit:
            failures.append(
                "rollback target cannot equal rollback.failedCandidateCommit"
            )
        for field in ("trigger", "learnerStateRisk"):
            if (
                not isinstance(rollback.get(field), str)
                or not rollback[field].strip()
            ):
                failures.append(f"rollback.{field} must be recorded")
        failures.extend(
            validate_last_known_good_acceptance(
                rollback.get("lastKnownGoodAcceptanceRecord"),
                candidate=candidate,
                evidence_repository_root=evidence_repository_root,
                rollback_accepted_at=accepted_at,
                artifact_format=artifact_format,
            )
        )
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", required=True)
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--dist", type=Path, default=ROOT / "app" / "dist")
    parser.add_argument(
        "--evidence-root",
        type=Path,
        default=ROOT,
        help="repository copy that owns the acceptance record",
    )
    parser.add_argument(
        "--ledger",
        type=Path,
        default=LEDGER_PATH,
        help="authoritative ledger path (default: current repository ledger)",
    )
    parser.add_argument(
        "--operation",
        choices=("promote", "rollback"),
        default="promote",
    )
    args = parser.parse_args()

    failures: list[str] = []
    expected_commit = args.expected_commit.strip().casefold()
    if not HEX_40.fullmatch(expected_commit):
        failures.append("expected commit must be a full 40-character Git SHA")

    try:
        record_path = resolve_record(args.record, args.evidence_root)
        dist = args.dist.resolve()
        record = read_object(record_path)
        artifact_identity = inspect_artifact_identity(
            dist,
            expected_commit=expected_commit,
            operation=args.operation,
        )
        version = artifact_identity["version"]
        ledger_text = args.ledger.resolve().read_text(encoding="utf-8")
        failures.extend(
            validate(
                record,
                version,
                expected_commit=expected_commit,
                asset_manifest_sha256=artifact_identity[
                    "assetManifestSha256"
                ],
                artifact_tree_sha256_value=artifact_identity[
                    "artifactTreeSha256"
                ],
                ledger_text=ledger_text,
                operation=args.operation,
                evidence_repository_root=args.evidence_root.resolve(),
                artifact_format=artifact_identity["artifactFormat"],
            )
        )
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        failures.append(str(exc))

    result = {
        "result": "PASS" if not failures else "FAIL",
        "expectedCommit": expected_commit,
        "failures": failures,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
