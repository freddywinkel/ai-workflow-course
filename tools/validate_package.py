#!/usr/bin/env python3
"""Deterministically validate Course 1 and its optional Course 4 capstone.

The curriculum manifest is the source of truth for the bundled learning
material. Archived future-course source material and generated/dependency
directories are intentionally outside this validator's scope; the runnable
Course 4 demo's required package surface is checked explicitly.

Only the Python standard library is required. When jsonschema or PyYAML is not
installed, the related optional checks are reported as warnings rather than
silently skipped.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path, PurePosixPath
from typing import Any, Iterable
from urllib.parse import unquote


EXPECTED_PROGRAM_ID = "controlled-ai-workflow-consultant-path"
EXPECTED_COURSE_ID = "course-1-controlled-ai-workflow-foundations"
EXPECTED_COURSE4_ID = "course-4-controlled-document-ai-systems"
EXPECTED_SCHEMA_VERSION = 3
FIXED_ASSESSMENT_DATE_TEXT = "2026-07-26"
FIXED_ASSESSMENT_DATE = date.fromisoformat(FIXED_ASSESSMENT_DATE_TEXT)

STABLE_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REVISION_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
WORK_ITEM_ID_RE = re.compile(r"^WI-\d{4}$")
SOURCE_REFERENCE_RE = re.compile(r"^REF-\d{4}$")
TECHNICAL_REQUIREMENT_RE = re.compile(
    r"^C1-TA-(DATA|FS|IO|CAP|PWA|WEB|SW|SC|TEST|WIN|BR|REC)-\d{3}$"
)
TECHNICAL_TEST_RE = re.compile(r"^C1-TST-(?:[A-Z0-9]+-)+\d{3}$")
TECHNICAL_REQUIREMENT_FAMILY_COUNTS = {
    "DATA": 4,
    "FS": 11,
    "IO": 13,
    "CAP": 7,
    "PWA": 14,
    "WEB": 8,
    "SW": 10,
    "SC": 12,
    "TEST": 9,
    "WIN": 12,
    "BR": 8,
    "REC": 10,
}
EXPECTED_TECHNICAL_TEST_IDS = {
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
LEARNING_REQUIREMENT_RE = re.compile(r"^C1-LV-\d{3}$")
EXPECTED_LEARNING_REQUIREMENT_IDS = tuple(
    f"C1-LV-{number:03d}" for number in range(1, 18)
)
EXPECTED_LEARNING_METHOD_IDS = {
    f"C1-LVM-{number:03d}" for number in range(1, 18)
}
LEARNING_EVIDENCE_CLASSES = {
    "AUTOMATED_ARTIFACT",
    "LEARNER_SELF_REFLECTION",
    "INDEPENDENT_ARTIFACT_ASSESSMENT",
    "INDEPENDENT_ORAL_ASSESSMENT",
    "ROLE_SIMULATED_ACCEPTANCE_REHEARSAL",
    "REAL_SYNTHETIC_UAT",
    "LITERAL_BEGINNER_TRIAL",
    "DELAYED_RETENTION",
    "UNSEEN_TRANSFER",
    "ACCESSIBILITY_REVIEW",
}
HUMAN_TRIAL_EVIDENCE_CLASSES = {
    "INDEPENDENT_ARTIFACT_ASSESSMENT",
    "INDEPENDENT_ORAL_ASSESSMENT",
    "REAL_SYNTHETIC_UAT",
    "LITERAL_BEGINNER_TRIAL",
    "DELAYED_RETENTION",
    "UNSEEN_TRANSFER",
    "ACCESSIBILITY_REVIEW",
}
PREMODULE_STUDY_BLOCK_COUNTS = {
    "BEGINNER_READINESS_CHECK.md": 2,
    "BEGINNER_SOFTWARE_CHECK.md": 2,
    "SETUP_WINDOWS.md": 5,
    "foundations/01_FILES_AND_TEXT.md": 6,
    "foundations/02_COMMAND_LINE_SURVIVAL.md": 7,
    "foundations/03_CODE_AND_PYTHON.md": 9,
    "foundations/04_WEB_APIS_AND_JSON.md": 6,
    "foundations/05_GIT_AND_SAFE_CHANGES.md": 6,
    "foundations/06_SPREADSHEETS_CSV_AND_DATA_QUALITY.md": 7,
    "foundations/07_AI_AND_CONTROLLED_WORKFLOWS.md": 6,
    "foundations/08_SAFE_AI_ASSISTED_BUILDING.md": 7,
    "foundations/09_WORKFLOW_TOOLS_AND_DATA_STORES.md": 6,
}

REQUIRED_MODULE_HEADINGS = (
    "## Outcome",
    "## Beginner checkpoint",
    "## Concepts",
    "## Official readings",
    "## Guided build",
    "## Consultant lens",
    "## Capstone increment",
    "## Required artifact",
    "## Test gate",
    "## Stop or rework",
    "## Common failures",
    "## Estimated time",
)

REQUIRED_PRACTICE_HEADINGS = (
    "## Follow along — I show you exactly how",
    "## Now recreate it yourself",
    "## Ask Codex to check your work",
    "## Pass criteria",
)

PROJECT_REPOSITORY_FRAGMENT = (
    r"AI-workflow-learning\operations-exception-assistant"
)
MODULE_TEMPLATE_REFERENCES = {
    1: ("stakeholder_and_user_map.md", "baseline_and_value_record.md"),
    2: ("workflow_opportunity_scorecard.md",),
    3: ("data_dictionary_and_quality_check.md",),
    7: ("risk_and_escalation_screen.md", "tool_fit_and_ownership_record.md"),
    8: ("pilot_decision_record.md",),
    9: (
        "uat_script.md",
        "adoption_and_training_plan.md",
        "acceptance_and_handover.md",
    ),
}
FINAL_DECISIONS = (
    "ACCEPT FOR SYNTHETIC PORTFOLIO",
    "REWORK",
    "DO NOT CONTINUE",
)
FINAL_DECISION_FILES = (
    "README.md",
    "COURSE_OVERVIEW.md",
    "CAPSTONE_SPECIFICATION.md",
    "ASSESSMENT_AND_RUBRIC.md",
    "modules/MODULE_08.md",
    "modules/MODULE_09.md",
    "templates/pilot_decision_record.md",
)
COURSE4_CAPSTONE_DOCUMENTS = (
    (
        "course-4-capstone-overview",
        "advanced_capstone/README.md",
    ),
    (
        "course-4-capstone-readiness-and-cost-gate",
        "advanced_capstone/00_READINESS_COST_GATE.md",
    ),
    (
        "course-4-capstone-local-baseline",
        "advanced_capstone/01_LOCAL_BASELINE.md",
    ),
    (
        "course-4-capstone-document-ai-eu",
        "advanced_capstone/02_SOURCE_INTEGRITY_DOCUMENT_AI.md",
    ),
    (
        "course-4-capstone-evidence-linked-extraction",
        "advanced_capstone/03_EVIDENCE_LINKED_EXTRACTION.md",
    ),
    (
        "course-4-capstone-vertex-gemini-eu",
        "advanced_capstone/04_GEMINI_SUMMARIES_ACTIONS.md",
    ),
    (
        "course-4-capstone-human-approval-and-exports",
        "advanced_capstone/05_HUMAN_APPROVAL_EXPORTS.md",
    ),
    (
        "course-4-capstone-tests-and-evaluation",
        "advanced_capstone/06_TESTS_AND_EVALUATION.md",
    ),
    (
        "course-4-capstone-cloud-run-deployment",
        "advanced_capstone/07_CLOUD_RUN_DEPLOYMENT.md",
    ),
    (
        "course-4-capstone-live-validation",
        "advanced_capstone/08_LIVE_VALIDATION.md",
    ),
    (
        "course-4-capstone-teardown",
        "advanced_capstone/09_TEARDOWN.md",
    ),
)
FORBIDDEN_FINAL_DECISION_PHRASES = (
    "`PILOT`",
    "`DO NOT PILOT`",
    "`STOP`",
    "SYNTHETIC DEMONSTRATION ONLY",
    "`REVISE AND RETEST`",
    "COMPLETE AS PORTFOLIO DEMO",
    "ASSESS A LATER CONTROLLED PILOT",
)

REQUIRED_ONBOARDING_PHRASES = {
    "README.md": (
        "Artificial Intelligence (AI)",
        "Small and Medium-sized Enterprises (SMEs)",
        "progressive web app (PWA)",
        "comma-separated values (CSV)",
        "application programming interfaces (APIs)",
        "user acceptance testing (UAT)",
        "Git is the name of a version-control tool",
    ),
    "BEGINNER_READINESS_CHECK.md": (
        "application programming interface (API)",
        "JavaScript Object Notation (JSON)",
        "artificial intelligence (AI)",
        "progressive web app (PWA)",
        "comma-separated values (CSV)",
        "identifier (ID)",
    ),
    "SETUP_WINDOWS.md": (
        "artificial intelligence (AI)",
        "Small and Medium-sized Enterprise (SME)",
        "comma-separated values (CSV)",
        "application programming interface (API)",
        "Long-Term Support (LTS)",
    ),
    "modules/MODULE_03.md": (
        "PowerShell represents each imported row as an object",
        "`PSObject.Properties.Name` asks that object for the names of its fields",
    ),
    "templates/architecture_decision_record.md": (
        "Architecture Decision Record (ADR)",
    ),
}

EXPECTED_SCHEMA_FILES = {
    "approval.schema.json",
    "audit_event.schema.json",
    "control.schema.json",
    "evaluation.schema.json",
    "issue.schema.json",
    "review_manifest.schema.json",
    "review_package.schema.json",
    "run_config.schema.json",
    "state.schema.json",
    "summary.schema.json",
    "work_item.schema.json",
}

WORK_ITEM_FIELDS = (
    "work_item_id",
    "source_reference",
    "title",
    "owner_role",
    "status",
    "priority",
    "received_date",
    "due_date",
    "completed_date",
    "amount",
    "currency",
    "category",
)

EXPECTED_ISSUE_FIELDS = (
    "issue_id",
    "work_item_id",
    "field",
    "rule_code",
    "severity",
    "expected_message",
)

RULE_CODES = {f"R{number:03d}" for number in range(1, 12)}
ALLOWED_STATUSES = {"new", "in_progress", "waiting", "completed", "cancelled"}
OPEN_STATUSES = {"new", "in_progress", "waiting"}
OWNER_REQUIRED_STATUSES = {"in_progress", "waiting", "completed"}
ALLOWED_PRIORITIES = {"low", "medium", "high"}
ALLOWED_SEVERITIES = {"low", "medium", "high"}
REQUIRED_VALUE_FIELDS = (
    "work_item_id",
    "source_reference",
    "title",
    "received_date",
    "category",
)
DATE_FIELDS = ("received_date", "due_date", "completed_date")

IGNORED_DIRECTORY_NAMES = {
    ".git",
    ".pytest_cache",
    ".validation-deps",
    "__pycache__",
    "dist",
    "node_modules",
}
IGNORED_TOP_LEVEL_DIRECTORIES = {"future_courses"}

FENCED_CODE_RE = re.compile(r"```.*?```|~~~.*?~~~", re.DOTALL)
INLINE_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REFERENCE_LINK_RE = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.MULTILINE)

STRATEGIC_FOCUS_REQUIREMENTS = {
    "AGENTS.md": (
        "STRATEGIC_FOCUS.md",
        "A new tool, artificial intelligence feature, promotional credit",
        "STRATEGIC FIT: PASS",
        "does not change the main goal",
        "explicitly approves a documented goal change",
    ),
    "STRATEGIC_FOCUS.md": (
        "Build the safest, most durable, market-relevant path",
        "Do not let a temporary opportunity choose the curriculum",
        "STRATEGIC FIT: PASS",
        "STRATEGIC FIT: PAUSE",
        "STRATEGIC FIT: REJECT",
        "Explicit goal-change procedure",
        "Promotional Google Cloud credit does not make Google the program-wide default",
    ),
    "README.md": (
        "## Project decision rule",
        "[Strategic Focus Rule](STRATEGIC_FOCUS.md)",
        "Changing the main goal requires a documented comparison",
    ),
}

PRODUCT_STATUSES = {"PASS", "REPAIR REQUIRED", "UNVERIFIED", "SUPERSEDED"}
CURRENT_PRODUCT_STATUS_RE = re.compile(
    r"^- Current status: \*\*`(?P<status>[^`\r\n]+)`\*\*$",
    re.MULTILINE,
)


@dataclass
class Report:
    checks: list[dict[str, str]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def passed(self, name: str, detail: str) -> None:
        self.checks.append({"status": "PASS", "name": name, "detail": detail})

    def failed(self, name: str, detail: str) -> None:
        self.checks.append({"status": "FAIL", "name": name, "detail": detail})
        self.errors.append(f"{name}: {detail}")

    def warn(self, name: str, detail: str) -> None:
        self.checks.append({"status": "WARN", "name": name, "detail": detail})
        self.warnings.append(f"{name}: {detail}")


def read_authoritative_product_status(root: Path) -> tuple[str | None, list[str]]:
    """Read the one exact current-product marker from the authoritative ledger."""

    failures: list[str] = []
    path = root / "COURSE_1_AUDIT_STATUS_AND_REPAIR_LEDGER.md"
    try:
        text = path.read_text(encoding="utf-8", errors="strict")
    except (OSError, UnicodeError) as exc:
        return None, [f"could not read authoritative Course 1 ledger: {exc}"]

    matches = list(CURRENT_PRODUCT_STATUS_RE.finditer(text))
    if len(matches) != 1:
        return None, [
            "authoritative Course 1 ledger must contain exactly one exact "
            "'- Current status: **`...`**' marker"
        ]

    status = matches[0].group("status")
    if status not in PRODUCT_STATUSES:
        failures.append(f"unsupported authoritative Course 1 product status: {status}")
        return None, failures
    return status, failures


def validate_current_status_consumers(root: Path, report: Report) -> None:
    """Keep active human-facing status consumers aligned with the ledger."""

    status, failures = read_authoritative_product_status(root)
    if status is None:
        report.failed("current-product-status-consumers", compact(failures))
        return

    consumer_patterns = {
        "README.md": re.compile(
            rf"Current product status:\s+\*\*`{re.escape(status)}`\*\*"
        ),
        "RELEASE_VALIDATION.md": re.compile(
            rf"ledger currently records version 2\.6\.0 as\s+`{re.escape(status)}`",
            re.DOTALL,
        ),
        "PWA_AND_UPDATES.md": re.compile(
            rf"current local version 2\.6\.0 working copy is "
            rf"\*\*`{re.escape(status)}`\*\*",
            re.IGNORECASE,
        ),
        "COURSE_CHANGELOG.md": re.compile(
            rf"authoritative ledger currently\s+(?:>\s*)?"
            rf"records `{re.escape(status)}`;",
            re.IGNORECASE,
        ),
    }
    for relative, pattern in consumer_patterns.items():
        path = root / relative
        try:
            text = path.read_text(encoding="utf-8", errors="strict")
        except (OSError, UnicodeError) as exc:
            failures.append(f"{relative} could not be read: {exc}")
            continue
        if pattern.search(text) is None:
            failures.append(
                f"{relative} does not present authoritative product status {status}"
            )

    if failures:
        report.failed("current-product-status-consumers", compact(failures))
    else:
        report.passed(
            "current-product-status-consumers",
            f"the ledger and four active human-facing consumers agree on {status}",
        )


def compact(items: Iterable[str], limit: int = 12) -> str:
    values = [str(item) for item in items]
    if len(values) <= limit:
        return "; ".join(values)
    return "; ".join(values[:limit]) + f"; ... and {len(values) - limit} more"


def is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def valid_revision(value: Any) -> bool:
    if not isinstance(value, str) or not REVISION_RE.fullmatch(value):
        return False
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def path_is_ignored(relative: Path) -> bool:
    parts = relative.parts
    if not parts:
        return False
    if parts[0] in IGNORED_TOP_LEVEL_DIRECTORIES:
        return True
    if (
        len(parts) >= 5
        and parts[0] == "release_evidence"
        and parts[1] == "course1_ground_up_audit"
        and SEMVER_RE.fullmatch(parts[2])
        and valid_revision(parts[3])
        and parts[4] == "raw"
    ):
        # Generator-owned raw evidence is opaque, hash-indexed audit input.
        # It may itself be JSON, but it is not a current package source and
        # must not alter the generated learner report or PWA build identity.
        return True
    return any(part in IGNORED_DIRECTORY_NAMES for part in parts)


def iter_current_files(root: Path, suffix: str) -> list[Path]:
    """Return in-scope files while pruning archives, generated files, and deps."""

    matches: list[Path] = []
    for current_root, directory_names, file_names in os.walk(root):
        current = Path(current_root)
        retained: list[str] = []
        for directory_name in directory_names:
            relative = (current / directory_name).relative_to(root)
            if not path_is_ignored(relative):
                retained.append(directory_name)
        directory_names[:] = retained

        for file_name in file_names:
            if file_name.endswith(suffix):
                matches.append(current / file_name)
    return sorted(matches)


def reject_duplicate_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def load_json_value(path: Path) -> Any:
    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_json_keys,
    )


def load_json_object(path: Path) -> dict[str, Any]:
    value = load_json_value(path)
    if not isinstance(value, dict):
        raise ValueError("top-level JSON value is not an object")
    return value


EXPECTED_CURRICULUM_DATE_CONTRACT = {
    "sourceVerifiedThrough": {
        "owner": "Source-claim owners",
        "evidenceSource": (
            "source_claims.json verifiedThrough and entries[].lastVerified"
        ),
        "consumers": {
            "app/scripts/build.mjs",
            "app/src/app.js",
            "tools/audit_course1_sources.py",
            "tools/validate_package.py",
        },
        "meaningTokens": ("research or source claim", "not a content-edit date"),
    },
    "contentRevisionThrough": {
        "owner": "Curriculum maintainer",
        "evidenceSource": "curriculum.json groups[].documents[].revision",
        "consumers": {
            "app/scripts/build.mjs",
            "app/src/app.js",
            "tools/validate_package.py",
        },
        "meaningTokens": ("Latest revision date", "does not assert"),
    },
    "verifiedThrough": {
        "owner": "PWA compatibility maintainer",
        "evidenceSource": "curriculum.json course.sourceVerifiedThrough",
        "consumers": {
            "app/scripts/build.mjs",
            "app/src/sw.js",
        },
        "meaningTokens": ("compatibility alias", "never limits content revisions"),
    },
}


def curriculum_date_metadata_failures(
    root: Path,
    curriculum: dict[str, Any],
    *,
    source_claims_override: dict[str, Any] | None = None,
    contract_override: dict[str, Any] | None = None,
) -> list[str]:
    """Validate independent content-revision and source-review claims."""

    failures: list[str] = []
    if curriculum.get("schemaVersion") != EXPECTED_SCHEMA_VERSION:
        failures.append(
            f"curriculum schemaVersion must be {EXPECTED_SCHEMA_VERSION}"
        )

    course = curriculum.get("course")
    if not isinstance(course, dict):
        return failures + ["curriculum.course must be an object"]

    source_verified = course.get("sourceVerifiedThrough")
    content_revised = course.get("contentRevisionThrough")
    compatibility_alias = course.get("verifiedThrough")
    if not valid_revision(source_verified):
        failures.append(
            "course.sourceVerifiedThrough must be a valid ISO date"
        )
    if not valid_revision(content_revised):
        failures.append(
            "course.contentRevisionThrough must be a valid ISO date"
        )
    if not valid_revision(compatibility_alias):
        failures.append(
            "course.verifiedThrough compatibility alias must be a valid ISO date"
        )
    if (
        valid_revision(source_verified)
        and valid_revision(compatibility_alias)
        and compatibility_alias != source_verified
    ):
        failures.append(
            "course.verifiedThrough compatibility alias must equal "
            "course.sourceVerifiedThrough"
        )

    revisions: list[str] = []
    groups = curriculum.get("groups")
    if isinstance(groups, list):
        for group in groups:
            if not isinstance(group, dict):
                continue
            documents = group.get("documents")
            if not isinstance(documents, list):
                continue
            for document in documents:
                if isinstance(document, dict) and valid_revision(
                    document.get("revision")
                ):
                    revisions.append(document["revision"])
    if not revisions:
        failures.append("curriculum has no valid document revision dates")
    elif valid_revision(content_revised) and content_revised != max(revisions):
        failures.append(
            "course.contentRevisionThrough must equal the latest document revision"
        )

    if source_claims_override is None:
        try:
            source_claims = load_json_object(root / "source_claims.json")
        except Exception as exc:
            source_claims = {}
            failures.append(f"source_claims.json cannot be read: {exc}")
    else:
        source_claims = source_claims_override
    if set(source_claims) != {"schemaVersion", "verifiedThrough", "entries"}:
        failures.append("source_claims.json must use its exact closed top-level shape")
    if source_claims.get("schemaVersion") != 1:
        failures.append("source_claims.json schemaVersion must be 1")
    claims_verified = source_claims.get("verifiedThrough")
    if not valid_revision(claims_verified):
        failures.append("source_claims.json verifiedThrough must be a valid ISO date")
    elif valid_revision(source_verified) and claims_verified != source_verified:
        failures.append(
            "course.sourceVerifiedThrough must equal "
            "source_claims.json verifiedThrough"
        )
    claim_entries = source_claims.get("entries")
    claim_dates: list[str] = []
    if not isinstance(claim_entries, list) or not claim_entries:
        failures.append("source_claims.json entries must be a non-empty array")
    else:
        for index, entry in enumerate(claim_entries):
            if not isinstance(entry, dict) or not valid_revision(
                entry.get("lastVerified")
            ):
                failures.append(
                    f"source_claims.json entries[{index}].lastVerified must "
                    "be a valid ISO date"
                )
            else:
                claim_dates.append(entry["lastVerified"])
    if (
        claim_dates
        and valid_revision(claims_verified)
        and claims_verified != min(claim_dates)
    ):
        failures.append(
            "source_claims.json verifiedThrough must equal the oldest "
            "entries[].lastVerified date"
        )

    if contract_override is None:
        contract_path = (
            root / "audit_control/course1/curriculum_date_contract.json"
        )
        try:
            contract = load_json_object(contract_path)
        except Exception as exc:
            contract = {}
            failures.append(
                f"audit_control/course1/curriculum_date_contract.json "
                f"cannot be read: {exc}"
            )
    else:
        contract = contract_override
    if set(contract) != {"schemaVersion", "courseId", "fields"}:
        failures.append("curriculum date contract must use its exact closed shape")
    if (
        contract.get("schemaVersion")
        != "course1-curriculum-date-contract-v1"
    ):
        failures.append("curriculum date contract schemaVersion is unsupported")
    if contract.get("courseId") != EXPECTED_COURSE_ID:
        failures.append("curriculum date contract courseId is incorrect")
    fields = contract.get("fields")
    if not isinstance(fields, dict):
        failures.append("curriculum date contract fields must be an object")
        fields = {}
    if set(fields) != set(EXPECTED_CURRICULUM_DATE_CONTRACT):
        failures.append(
            "curriculum date contract must define exactly "
            "sourceVerifiedThrough, contentRevisionThrough, and verifiedThrough"
        )
    for field_name, expected in EXPECTED_CURRICULUM_DATE_CONTRACT.items():
        definition = fields.get(field_name)
        if not isinstance(definition, dict):
            failures.append(
                f"curriculum date contract {field_name} must be an object"
            )
            continue
        if set(definition) != {
            "meaning",
            "owner",
            "evidenceSource",
            "consumers",
        }:
            failures.append(
                f"curriculum date contract {field_name} must use its exact "
                "closed shape"
            )
        meaning = definition.get("meaning")
        if not is_nonempty_string(meaning) or any(
            token not in meaning for token in expected["meaningTokens"]
        ):
            failures.append(
                f"curriculum date contract {field_name}.meaning is incomplete"
            )
        if definition.get("owner") != expected["owner"]:
            failures.append(
                f"curriculum date contract {field_name}.owner is incorrect"
            )
        if definition.get("evidenceSource") != expected["evidenceSource"]:
            failures.append(
                f"curriculum date contract {field_name}.evidenceSource is incorrect"
            )
        consumers = definition.get("consumers")
        if (
            not isinstance(consumers, list)
            or len(consumers) != len(set(consumers))
            or set(consumers) != expected["consumers"]
        ):
            failures.append(
                f"curriculum date contract {field_name}.consumers are incomplete"
            )
            continue
        for consumer in consumers:
            if not (root / consumer).is_file():
                failures.append(
                    f"curriculum date contract {field_name} consumer is missing: "
                    f"{consumer}"
                )

    schema_path = (
        root / "audit_control/course1/curriculum_date_contract.schema.json"
    )
    try:
        contract_schema = load_json_object(schema_path)
    except Exception as exc:
        failures.append(
            "audit_control/course1/curriculum_date_contract.schema.json "
            f"cannot be read: {exc}"
        )
    else:
        if (
            contract_schema.get("$schema")
            != "https://json-schema.org/draft/2020-12/schema"
            or contract_schema.get("additionalProperties") is not False
        ):
            failures.append(
                "curriculum date contract schema must be closed Draft 2020-12"
            )
        try:
            import jsonschema  # type: ignore
        except (ModuleNotFoundError, ImportError):
            pass
        except Exception as exc:
            failures.append(
                f"jsonschema could not be imported for curriculum date contract: {exc}"
            )
        else:
            try:
                jsonschema.Draft202012Validator.check_schema(contract_schema)
                jsonschema.Draft202012Validator(contract_schema).validate(contract)
            except Exception as exc:
                failures.append(
                    f"curriculum date contract schema validation failed: {exc}"
                )
    return failures


def validate_curriculum_date_metadata(
    root: Path,
    curriculum: dict[str, Any] | None,
    report: Report,
) -> None:
    if not isinstance(curriculum, dict):
        report.failed(
            "curriculum-date-separation",
            "cannot validate date meanings without curriculum.json",
        )
        return
    failures = curriculum_date_metadata_failures(root, curriculum)
    if failures:
        report.failed("curriculum-date-separation", compact(failures, limit=20))
    else:
        course = curriculum["course"]
        report.passed(
            "curriculum-date-separation",
            "content revised through "
            f"{course['contentRevisionThrough']}; research and sources verified "
            f"through {course['sourceVerifiedThrough']}; compatibility alias, "
            "evidence sources, owners, and consumers match the closed contract",
        )


def validate_strategic_focus_guardrail(root: Path, report: Report) -> None:
    failures: list[str] = []
    for relative_path, required_phrases in STRATEGIC_FOCUS_REQUIREMENTS.items():
        path = root / relative_path
        if not path.is_file():
            failures.append(f"{relative_path} is missing")
            continue

        content = path.read_text(encoding="utf-8")
        missing_phrases = [
            phrase for phrase in required_phrases if phrase not in content
        ]
        if missing_phrases:
            failures.append(
                f"{relative_path} is missing: {', '.join(missing_phrases)}"
            )

    if failures:
        report.failed(
            "strategic-focus-guardrail",
            compact(failures, limit=12),
        )
    else:
        report.passed(
            "strategic-focus-guardrail",
            "standing instructions, decision rule, and project overview enforce PASS/PAUSE/REJECT and explicit goal changes",
        )


def validate_curriculum(root: Path, report: Report) -> dict[str, Any] | None:
    path = root / "curriculum.json"
    if not path.is_file():
        report.failed("curriculum-load", "curriculum.json is missing")
        return None

    try:
        curriculum = load_json_object(path)
    except Exception as exc:
        report.failed("curriculum-load", str(exc))
        return None
    report.passed("curriculum-load", "curriculum.json parsed as a JSON object")

    metadata_failures: list[str] = []
    if curriculum.get("schemaVersion") != EXPECTED_SCHEMA_VERSION:
        metadata_failures.append(
            f"schemaVersion must be {EXPECTED_SCHEMA_VERSION}"
        )

    program = curriculum.get("program")
    course = curriculum.get("course")
    groups = curriculum.get("groups")
    career = curriculum.get("career")
    if not isinstance(program, dict):
        metadata_failures.append("program must be an object")
        program = {}
    if not isinstance(course, dict):
        metadata_failures.append("course must be an object")
        course = {}
    if not isinstance(groups, list):
        metadata_failures.append("groups must be an array")
        groups = []
    if not isinstance(career, dict):
        metadata_failures.append("career must be an object")
        career = {}

    if program.get("id") != EXPECTED_PROGRAM_ID:
        metadata_failures.append(f"program.id must be {EXPECTED_PROGRAM_ID}")
    if not is_nonempty_string(program.get("title")):
        metadata_failures.append("program.title is missing")
    expected_target_market = "Dutch small and medium-sized enterprises (SMEs)"
    if program.get("targetMarket") != expected_target_market:
        metadata_failures.append(
            f"program.targetMarket must be {expected_target_market}"
        )
    if not is_nonempty_string(program.get("positioning")):
        metadata_failures.append("program.positioning is missing")
    if not is_nonempty_string(program.get("durableValue")):
        metadata_failures.append("program.durableValue is missing")

    if course.get("id") != EXPECTED_COURSE_ID:
        metadata_failures.append(f"course.id must be {EXPECTED_COURSE_ID}")
    if course.get("sequence") != 1:
        metadata_failures.append("course.sequence must be 1")
    if not is_nonempty_string(course.get("title")):
        metadata_failures.append("course.title is missing")
    if not isinstance(course.get("version"), str) or not SEMVER_RE.fullmatch(
        course.get("version", "")
    ):
        metadata_failures.append("course.version must use x.y.z")
    if (
        not isinstance(course.get("practiceRevision"), int)
        or course.get("practiceRevision") < 1
    ):
        metadata_failures.append("course.practiceRevision must be a positive integer")
    source_verified_through = course.get("sourceVerifiedThrough")
    content_revision_through = course.get("contentRevisionThrough")
    verified_through = course.get("verifiedThrough")
    if not valid_revision(source_verified_through):
        metadata_failures.append(
            "course.sourceVerifiedThrough must be a valid ISO date"
        )
    if not valid_revision(content_revision_through):
        metadata_failures.append(
            "course.contentRevisionThrough must be a valid ISO date"
        )
    if not valid_revision(verified_through):
        metadata_failures.append(
            "course.verifiedThrough compatibility alias must be a valid ISO date"
        )
    if (
        valid_revision(source_verified_through)
        and valid_revision(verified_through)
        and verified_through != source_verified_through
    ):
        metadata_failures.append(
            "course.verifiedThrough compatibility alias must equal "
            "course.sourceVerifiedThrough"
        )

    estimated_hours = course.get("estimatedHours")
    if not isinstance(estimated_hours, dict):
        metadata_failures.append("course.estimatedHours must be an object")
    else:
        minimum = estimated_hours.get("minimum")
        typical = estimated_hours.get("typical")
        maximum = estimated_hours.get("maximum")
        if not all(
            isinstance(value, int) and value > 0
            for value in (minimum, typical, maximum)
        ):
            metadata_failures.append(
                "course estimated hours must be positive integers"
            )
        elif not minimum <= typical <= maximum:
            metadata_failures.append(
                "course estimated hours must satisfy minimum <= typical <= maximum"
            )

    capstone = course.get("capstone")
    if not isinstance(capstone, dict):
        metadata_failures.append("course.capstone must be an object")
    else:
        if capstone.get("title") != "Synthetic SME Operations Exception Assistant":
            metadata_failures.append("unexpected Course 1 capstone title")
        if not is_nonempty_string(capstone.get("summary")):
            metadata_failures.append("course.capstone.summary is missing")
        non_goals = capstone.get("nonGoals")
        if not isinstance(non_goals, list) or not all(
            is_nonempty_string(item) for item in non_goals
        ):
            metadata_failures.append("course.capstone.nonGoals must be text entries")

    if metadata_failures:
        report.failed("curriculum-metadata", compact(metadata_failures))
    else:
        report.passed(
            "curriculum-metadata",
            "Course 1 metadata separates source verification through "
            f"{source_verified_through} from content revision through "
            f"{content_revision_through}",
        )

    group_failures: list[str] = []
    document_failures: list[str] = []
    identity_failures: list[str] = []
    group_ids: list[str] = []
    current_ids: list[str] = []
    legacy_ids: list[str] = []
    source_paths: list[str] = []
    learning_sequence_ids = {
        item
        for item in course.get("learningSequenceIds", [])
        if isinstance(item, str)
    }
    career_courses = career.get("courses")
    course_sequence_by_id = (
        {
            item["id"]: item["sequence"]
            for item in career_courses
            if isinstance(item, dict)
            and isinstance(item.get("id"), str)
            and isinstance(item.get("sequence"), int)
        }
        if isinstance(career_courses, list)
        else {}
    )

    for group_index, group in enumerate(groups):
        location = f"groups[{group_index}]"
        if not isinstance(group, dict):
            group_failures.append(f"{location} is not an object")
            continue
        group_id = group.get("id")
        if not isinstance(group_id, str) or not STABLE_ID_RE.fullmatch(group_id):
            group_failures.append(f"{location}.id is not a stable slug")
            group_id = f"<invalid-{group_index}>"
        else:
            group_ids.append(group_id)
        if not is_nonempty_string(group.get("title")):
            group_failures.append(f"{group_id}.title is missing")
        if not is_nonempty_string(group.get("kind")):
            group_failures.append(f"{group_id}.kind is missing")
        if not isinstance(group.get("core"), bool):
            group_failures.append(f"{group_id}.core must be boolean")

        documents = group.get("documents")
        if not isinstance(documents, list) or not documents:
            group_failures.append(f"{group_id}.documents must be a non-empty array")
            continue

        for document_index, document in enumerate(documents):
            document_location = f"{group_id}.documents[{document_index}]"
            if not isinstance(document, dict):
                document_failures.append(f"{document_location} is not an object")
                continue

            document_id = document.get("id")
            if not isinstance(document_id, str) or not STABLE_ID_RE.fullmatch(
                document_id
            ):
                identity_failures.append(
                    f"{document_location}.id is not a stable slug"
                )
                document_id = document_location
            else:
                current_ids.append(document_id)
                document_course_id = document.get("courseId", EXPECTED_COURSE_ID)
                course_sequence = course_sequence_by_id.get(document_course_id)
                if course_sequence is None:
                    identity_failures.append(
                        f"{document_id} references unknown course {document_course_id!r}"
                    )
                elif not document_id.startswith(f"course-{course_sequence}-"):
                    identity_failures.append(
                        f"{document_id} must start with course-{course_sequence}-"
                    )

            revision = document.get("revision")
            if not valid_revision(revision):
                document_failures.append(
                    f"{document_id}.revision is not a valid ISO date"
                )
            if "title" in document and not is_nonempty_string(document.get("title")):
                document_failures.append(
                    f"{document_id}.title is present but empty"
                )

            if document_id in learning_sequence_ids:
                practice_hours = document.get("estimatedPracticeHours")
                if not isinstance(practice_hours, dict):
                    document_failures.append(
                        f"{document_id}.estimatedPracticeHours must be an object"
                    )
                else:
                    practice_minimum = practice_hours.get("minimum")
                    practice_maximum = practice_hours.get("maximum")
                    if not all(
                        isinstance(value, int) and value > 0
                        for value in (practice_minimum, practice_maximum)
                    ):
                        document_failures.append(
                            f"{document_id}.estimatedPracticeHours values must be positive integers"
                        )
                    elif practice_minimum > practice_maximum:
                        document_failures.append(
                            f"{document_id}.estimatedPracticeHours minimum exceeds maximum"
                        )

            legacy = document.get("legacyIds")
            if not isinstance(legacy, list):
                identity_failures.append(f"{document_id}.legacyIds must be an array")
            else:
                for legacy_id in legacy:
                    if not isinstance(legacy_id, str) or not STABLE_ID_RE.fullmatch(
                        legacy_id
                    ):
                        identity_failures.append(
                            f"{document_id} has invalid legacy ID {legacy_id!r}"
                        )
                    else:
                        legacy_ids.append(legacy_id)

            source_path = document.get("sourcePath")
            if not isinstance(source_path, str) or not source_path:
                document_failures.append(f"{document_id}.sourcePath is missing")
                continue
            pure_path = PurePosixPath(source_path)
            if (
                pure_path.is_absolute()
                or ".." in pure_path.parts
                or "." in pure_path.parts
                or "\\" in source_path
                or pure_path.as_posix() != source_path
            ):
                document_failures.append(
                    f"{document_id}.sourcePath is not a normalized relative path"
                )
                continue
            source_paths.append(source_path)
            relative = Path(*pure_path.parts)
            if path_is_ignored(relative):
                document_failures.append(
                    f"{document_id}.sourcePath points outside the bundled-course scope"
                )
                continue
            resolved = (root / relative).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                document_failures.append(
                    f"{document_id}.sourcePath escapes the course root"
                )
                continue
            if not resolved.is_file() and source_path != "VALIDATION_REPORT.md":
                document_failures.append(
                    f"{document_id}.sourcePath does not exist: {source_path}"
                )

    duplicate_groups = sorted(
        group_id for group_id, count in Counter(group_ids).items() if count > 1
    )
    if duplicate_groups:
        group_failures.append(f"duplicate group IDs: {duplicate_groups}")

    duplicate_current = sorted(
        item_id for item_id, count in Counter(current_ids).items() if count > 1
    )
    duplicate_legacy = sorted(
        item_id for item_id, count in Counter(legacy_ids).items() if count > 1
    )
    collisions = sorted(set(current_ids) & set(legacy_ids))
    duplicate_paths = sorted(
        source for source, count in Counter(source_paths).items() if count > 1
    )
    if duplicate_current:
        identity_failures.append(f"duplicate current IDs: {duplicate_current}")
    if duplicate_legacy:
        identity_failures.append(f"duplicate legacy IDs: {duplicate_legacy}")
    if collisions:
        identity_failures.append(
            f"IDs used as both current and legacy IDs: {collisions}"
        )
    if duplicate_paths:
        document_failures.append(f"duplicate source paths: {duplicate_paths}")

    if group_failures:
        report.failed("curriculum-groups", compact(group_failures))
    else:
        report.passed(
            "curriculum-groups",
            f"{len(groups)} configured groups have stable IDs and valid structure",
        )
    if identity_failures:
        report.failed("curriculum-stable-ids", compact(identity_failures))
    else:
        report.passed(
            "curriculum-stable-ids",
            f"{len(current_ids)} unique current IDs and {len(legacy_ids)} unique legacy IDs",
        )
    if document_failures:
        report.failed("curriculum-documents", compact(document_failures))
    else:
        report.passed(
            "curriculum-documents",
            f"{len(source_paths)} unique configured lesson paths and revisions are valid",
        )

    core_group_ids = course.get("coreGroupIds")
    groups_by_id = {
        group.get("id"): group for group in groups if isinstance(group, dict)
    }
    core_failures: list[str] = []
    if core_group_ids != ["foundations", "modules"]:
        core_failures.append(
            "course.coreGroupIds must be ['foundations', 'modules'] in that order"
        )
    for group_id in ("foundations", "modules"):
        group = groups_by_id.get(group_id)
        if not isinstance(group, dict):
            core_failures.append(f"missing {group_id} group")
        elif group.get("core") is not True:
            core_failures.append(f"{group_id} group must be core")
    for group_id, group in groups_by_id.items():
        if group_id not in {"foundations", "modules"} and group.get("core") is not False:
            core_failures.append(f"{group_id} group must remain non-core")
    if core_failures:
        report.failed("curriculum-core-groups", compact(core_failures))
    else:
        report.passed(
            "curriculum-core-groups",
            "only foundations and modules are configured as progress groups",
        )

    validate_career_metadata(career, report)
    return curriculum


def validate_career_metadata(career: dict[str, Any], report: Report) -> None:
    failures: list[str] = []
    if career.get("targetRole") != (
        "Controlled Artificial Intelligence (AI) Workflow Implementation "
        "Consultant for Dutch Small and Medium-sized Enterprises (SMEs)"
    ):
        failures.append("career.targetRole is missing or unexpected")
    courses = career.get("courses")
    if not isinstance(courses, list) or not courses:
        failures.append("career.courses must be a non-empty array")
        courses = []

    course_ids: list[str] = []
    sequences: list[int] = []
    current_ids: list[str] = []
    course4: dict[str, Any] | None = None
    for index, course in enumerate(courses):
        if not isinstance(course, dict):
            failures.append(f"career.courses[{index}] is not an object")
            continue
        course_id = course.get("id")
        if not isinstance(course_id, str) or not STABLE_ID_RE.fullmatch(course_id):
            failures.append(f"career.courses[{index}].id is not stable")
        else:
            course_ids.append(course_id)
        sequence = course.get("sequence")
        if not isinstance(sequence, int) or sequence < 1:
            failures.append(f"{course_id}.sequence is invalid")
        else:
            sequences.append(sequence)
        if not all(
            is_nonempty_string(course.get(field_name))
            for field_name in ("title", "status", "purpose", "exitEvidence")
        ):
            failures.append(f"{course_id} is missing descriptive metadata")
        if course.get("status") == "current" and isinstance(course_id, str):
            current_ids.append(course_id)
        if course_id == EXPECTED_COURSE4_ID:
            course4 = course

    if len(course_ids) != len(set(course_ids)):
        failures.append("career course IDs are not unique")
    if sequences != list(range(1, len(sequences) + 1)):
        failures.append("career course sequences must be ordered 1..N")
    if current_ids != [EXPECTED_COURSE_ID]:
        failures.append("the Course 1 ID must be the only current career course")
    if not isinstance(course4, dict):
        failures.append(f"career is missing {EXPECTED_COURSE4_ID}")
    else:
        if course4.get("status") != "prototype-capstone-available":
            failures.append(
                f"{EXPECTED_COURSE4_ID}.status must be prototype-capstone-available"
            )
        if course4.get("prototypeDocumentId") != "course-4-capstone-overview":
            failures.append(
                f"{EXPECTED_COURSE4_ID}.prototypeDocumentId must open the capstone overview"
            )
    for course in courses:
        if not isinstance(course, dict):
            continue
        sequence = course.get("sequence")
        expected_status = (
            "current"
            if sequence == 1
            else "prototype-capstone-available"
            if sequence == 4
            else "proposed"
        )
        if course.get("status") != expected_status:
            failures.append(
                f"{course.get('id', '<unknown>')}.status must be {expected_status}"
            )

    if failures:
        report.failed("career-metadata", compact(failures))
    else:
        report.passed(
            "career-metadata",
            f"{len(courses)} ordered career courses; Course 1 is current and the Course 4 prototype is optional",
        )


def validate_release_metadata_sync(
    root: Path,
    curriculum: dict[str, Any] | None,
    report: Report,
) -> None:
    if not isinstance(curriculum, dict):
        report.failed(
            "release-metadata-sync",
            "cannot compare release metadata without curriculum.json",
        )
        return

    course = curriculum.get("course")
    if not isinstance(course, dict):
        report.failed(
            "release-metadata-sync",
            "curriculum.course is not an object",
        )
        return

    version = course.get("version")
    practice_revision = course.get("practiceRevision")
    source_verified_through = course.get("sourceVerifiedThrough")
    content_revision_through = course.get("contentRevisionThrough")
    course_id = course.get("id")
    failures: list[str] = []

    stack_path = root / "stack-manifest.yaml"
    if not stack_path.is_file():
        failures.append("stack-manifest.yaml is missing")
    else:
        stack_text = stack_path.read_text(encoding="utf-8")
        expected_stack_lines = (
            f"course_id: {course_id}",
            f"course_version: {version}",
            f"practice_revision: {practice_revision}",
            f'last_verified: "{source_verified_through}"',
            f'content_revision_through: "{content_revision_through}"',
        )
        for line in expected_stack_lines:
            if line not in stack_text:
                failures.append(f"stack-manifest.yaml lacks {line!r}")

    package_path = root / "app" / "package.json"
    lock_path = root / "app" / "package-lock.json"
    for path, label in (
        (package_path, "app/package.json"),
        (lock_path, "app/package-lock.json"),
    ):
        if not path.is_file():
            failures.append(f"{label} is missing")
            continue
        try:
            value = load_json_object(path)
        except Exception as exc:
            failures.append(f"{label} cannot be read: {exc}")
            continue
        if value.get("version") != version:
            failures.append(f"{label} version is not {version}")
        if label.endswith("package-lock.json"):
            root_package = value.get("packages", {}).get("")
            if not isinstance(root_package, dict) or root_package.get("version") != version:
                failures.append(f"{label} root package version is not {version}")

    expected_text = {
        "README.md": f"- Version: {version}",
        "COURSE_CHANGELOG.md": f"## {version} —",
        "RELEASE_VALIDATION.md": f"Course 1 version {version}",
        "PWA_AND_UPDATES.md": f"Course 1 version {version}",
    }
    for relative_path, fragment in expected_text.items():
        path = root / relative_path
        if not path.is_file():
            failures.append(f"{relative_path} is missing")
        elif fragment not in path.read_text(encoding="utf-8"):
            failures.append(f"{relative_path} lacks current release marker {fragment!r}")

    if failures:
        report.failed("release-metadata-sync", compact(failures, limit=20))
    else:
        report.passed(
            "release-metadata-sync",
            f"Course 1 version {version}, practice revision {practice_revision}, app metadata, manifest, and release documents agree",
        )


def validate_course4_capstone_integration(
    root: Path,
    curriculum: dict[str, Any] | None,
    report: Report,
    *,
    include_course4_product: bool,
) -> None:
    check_name = (
        "course4-capstone-integration"
        if include_course4_product
        else "course4-structural-isolation"
    )
    if not isinstance(curriculum, dict):
        report.failed(
            check_name,
            "cannot validate Course 4 isolation without curriculum.json",
        )
        return

    groups = curriculum.get("groups")
    group = (
        next(
            (
                item
                for item in groups
                if isinstance(item, dict) and item.get("id") == "course-4-capstone"
            ),
            None,
        )
        if isinstance(groups, list)
        else None
    )
    failures: list[str] = []
    expected_ids = [document_id for document_id, _path in COURSE4_CAPSTONE_DOCUMENTS]
    expected_paths = [path for _document_id, path in COURSE4_CAPSTONE_DOCUMENTS]

    if not isinstance(group, dict):
        failures.append("missing non-core course-4-capstone group")
        documents: list[dict[str, Any]] = []
    else:
        if group.get("core") is not False:
            failures.append("course-4-capstone must be non-core")
        if group.get("kind") != "advanced":
            failures.append("course-4-capstone.kind must be advanced")
        documents = [
            item for item in group.get("documents", []) if isinstance(item, dict)
        ]
        actual_ids = [item.get("id") for item in documents]
        actual_paths = [item.get("sourcePath") for item in documents]
        if actual_ids != expected_ids:
            failures.append(
                f"course-4-capstone IDs must be {expected_ids}; found {actual_ids}"
            )
        if actual_paths != expected_paths:
            failures.append(
                f"course-4-capstone paths must be {expected_paths}; found {actual_paths}"
            )
        for document in documents:
            if document.get("courseId") != EXPECTED_COURSE4_ID:
                failures.append(
                    f"{document.get('id', '<unknown>')}.courseId must be {EXPECTED_COURSE4_ID}"
                )
            if document.get("legacyIds") != []:
                failures.append(
                    f"{document.get('id', '<unknown>')}.legacyIds must be an empty array"
                )

    learning_sequence = curriculum.get("course", {}).get("learningSequenceIds", [])
    leaked_ids = sorted(set(expected_ids) & set(learning_sequence))
    if leaked_ids:
        failures.append(
            f"Course 4 capstone IDs must not enter the Course 1 learning sequence: {leaked_ids}"
        )

    combined_text: list[str] = []
    for document_id, source_path in COURSE4_CAPSTONE_DOCUMENTS:
        path = root / Path(*PurePosixPath(source_path).parts)
        if not path.is_file():
            failures.append(f"{source_path} is missing")
            continue
        text = path.read_text(encoding="utf-8")
        combined_text.append(text)
        if (
            include_course4_product
            and source_path != "advanced_capstone/README.md"
        ):
            for heading in REQUIRED_PRACTICE_HEADINGS:
                if heading not in text:
                    failures.append(f"{source_path} is missing {heading}")

    if include_course4_product:
        joined = "\n".join(combined_text)
        required_boundary_phrases = (
            "synthetic",
            "€60",
            "Google Cloud Run",
            "Document AI",
            "Vertex AI",
            "human approval",
            "CSV",
            "JSON",
            "teardown",
            "26 October 2026",
        )
        for phrase in required_boundary_phrases:
            if phrase.casefold() not in joined.casefold():
                failures.append(
                    f"advanced capstone lessons omit required boundary: {phrase}"
                )

        implementation_root = (
            root
            / "future_courses"
            / "course_04_controlled_document_ai"
            / "controlled_document_intake_demo"
        )
        required_implementation_files = (
            "Dockerfile",
            "pyproject.toml",
            "requirements.txt",
            "requirements-ci.txt",
            "src/controlled_intake/main.py",
            "src/controlled_intake/pipeline.py",
            "src/controlled_intake/providers.py",
            "tests/test_contracts.py",
            "tests/test_http.py",
            "tests/test_pipeline.py",
            "scripts/preflight.ps1",
            "scripts/deploy.ps1",
            "scripts/verify_live.ps1",
            "scripts/teardown.ps1",
        )
        missing_implementation = [
            relative
            for relative in required_implementation_files
            if not (
                implementation_root / Path(*PurePosixPath(relative).parts)
            ).is_file()
        ]
        if missing_implementation:
            failures.append(
                "controlled intake implementation is incomplete: "
                f"{missing_implementation}"
            )

    if failures:
        report.failed(check_name, compact(failures, limit=20))
    elif include_course4_product:
        report.passed(
            check_name,
            "11 non-core Course 4 pages, the frozen Course 1 sequence, and the runnable demo package are wired consistently",
        )
    else:
        report.passed(
            check_name,
            "Course 4 remains non-core, outside the Course 1 sequence, and readable by the shared PWA; Course 4 lesson and implementation acceptance was not run",
        )


def group_documents(
    curriculum: dict[str, Any], group_id: str
) -> list[dict[str, Any]]:
    groups = curriculum.get("groups")
    if not isinstance(groups, list):
        return []
    for group in groups:
        if isinstance(group, dict) and group.get("id") == group_id:
            documents = group.get("documents")
            if isinstance(documents, list):
                return [
                    document
                    for document in documents
                    if isinstance(document, dict)
                ]
    return []


def validate_progress_lessons(
    root: Path, curriculum: dict[str, Any] | None, report: Report
) -> None:
    if curriculum is None:
        report.failed(
            "progress-lessons",
            "cannot validate progress lessons without curriculum.json",
        )
        return

    foundations = group_documents(curriculum, "foundations")
    modules = group_documents(curriculum, "modules")
    foundation_failures: list[str] = []
    module_failures: list[str] = []

    expected_foundation_ids = [
        f"course-1-foundation-{number:02d}" for number in range(1, 10)
    ]
    actual_foundation_ids = [item.get("id") for item in foundations]
    if actual_foundation_ids != expected_foundation_ids:
        foundation_failures.append(
            f"expected IDs {expected_foundation_ids}; found {actual_foundation_ids}"
        )

    expected_foundation_paths: list[str] = []
    for number, document in enumerate(foundations, 1):
        source_path = document.get("sourcePath")
        if not isinstance(source_path, str) or not re.fullmatch(
            rf"foundations/{number:02d}_[A-Z0-9_]+\.md", source_path
        ):
            foundation_failures.append(
                f"foundation {number} has unexpected source path {source_path!r}"
            )
        else:
            expected_foundation_paths.append(source_path)
        if not is_nonempty_string(document.get("title")):
            foundation_failures.append(
                f"foundation {number} requires a progress title"
            )

    disk_foundations = sorted(
        path.relative_to(root).as_posix()
        for path in (root / "foundations").glob("[0-9][0-9]_*.md")
    )
    if sorted(expected_foundation_paths) != disk_foundations:
        foundation_failures.append(
            "configured foundation paths do not match numbered foundation files"
        )

    expected_module_ids = [
        f"course-1-module-{number:02d}" for number in range(1, 10)
    ]
    expected_module_paths = [
        f"modules/MODULE_{number:02d}.md" for number in range(1, 10)
    ]
    actual_module_ids = [item.get("id") for item in modules]
    actual_module_paths = [item.get("sourcePath") for item in modules]
    if actual_module_ids != expected_module_ids:
        module_failures.append(
            f"expected IDs {expected_module_ids}; found {actual_module_ids}"
        )
    if actual_module_paths != expected_module_paths:
        module_failures.append(
            f"expected paths {expected_module_paths}; found {actual_module_paths}"
        )
    for number, document in enumerate(modules, 1):
        if not is_nonempty_string(document.get("title")):
            module_failures.append(f"module {number} requires a progress title")

    disk_modules = sorted(
        path.relative_to(root).as_posix()
        for path in (root / "modules").glob("MODULE_*.md")
    )
    if disk_modules != expected_module_paths:
        module_failures.append(
            f"disk module set must be MODULE_01.md through MODULE_09.md; found {disk_modules}"
        )

    if foundation_failures:
        report.failed("progress-foundations", compact(foundation_failures))
    else:
        report.passed(
            "progress-foundations",
            "exactly 9 ordered foundation progress lessons",
        )
    if module_failures:
        report.failed("progress-modules", compact(module_failures))
    else:
        report.passed(
            "progress-modules",
            "exactly 9 ordered module progress lessons",
        )

    if not foundation_failures and not module_failures:
        report.passed(
            "progress-total",
            "18 progress lessons: 9 foundations plus 9 modules",
        )
    else:
        report.failed(
            "progress-total",
            f"found {len(foundations)} foundation and {len(modules)} module entries",
        )


def validate_module_structure(
    root: Path, curriculum: dict[str, Any] | None, report: Report
) -> None:
    if curriculum is None:
        report.failed(
            "module-structure",
            "cannot validate modules without curriculum.json",
        )
        return

    failures: list[str] = []
    modules = group_documents(curriculum, "modules")
    for number, document in enumerate(modules, 1):
        source_path = document.get("sourcePath")
        if not isinstance(source_path, str):
            failures.append(f"module {number} lacks sourcePath")
            continue
        path = root / Path(*PurePosixPath(source_path).parts)
        if not path.is_file():
            failures.append(f"{source_path} is missing")
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except Exception as exc:
            failures.append(f"{source_path} cannot be read: {exc}")
            continue
        if not lines or not re.fullmatch(rf"# Module {number} .+", lines[0]):
            failures.append(
                f"{source_path} first line must identify Module {number}"
            )

        positions: list[int] = []
        for heading in REQUIRED_MODULE_HEADINGS:
            indexes = [index for index, line in enumerate(lines) if line == heading]
            if len(indexes) != 1:
                failures.append(
                    f"{source_path} requires exactly one {heading!r}; found {len(indexes)}"
                )
            else:
                positions.append(indexes[0])
        if len(positions) == len(REQUIRED_MODULE_HEADINGS) and positions != sorted(
            positions
        ):
            failures.append(f"{source_path} required headings are out of order")

    if failures:
        report.failed("module-structure", compact(failures))
    else:
        report.passed(
            "module-structure",
            f"all {len(modules)} modules use the {len(REQUIRED_MODULE_HEADINGS)} required headings in order",
        )


def section_text(lines: list[str], heading: str) -> str:
    """Return one level-two Markdown section without later level-two sections."""

    try:
        start = lines.index(heading) + 1
    except ValueError:
        return ""
    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return "\n".join(lines[start:end])


def validate_beginner_practice_contract(
    root: Path, curriculum: dict[str, Any] | None, report: Report
) -> None:
    if curriculum is None:
        report.failed(
            "beginner-practice-structure",
            "cannot validate the practice contract without curriculum.json",
        )
        return

    documents = group_documents(curriculum, "foundations") + group_documents(
        curriculum, "modules"
    )
    structure_failures: list[str] = []
    inspection_failures: list[str] = []
    pass_failures: list[str] = []

    for document in documents:
        source_path = document.get("sourcePath")
        if not isinstance(source_path, str):
            structure_failures.append(
                f"{document.get('id', '<unknown>')} lacks sourcePath"
            )
            continue
        path = root / Path(*PurePosixPath(source_path).parts)
        if not path.is_file():
            structure_failures.append(f"{source_path} is missing")
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except Exception as exc:
            structure_failures.append(f"{source_path} cannot be read: {exc}")
            continue
        expected_title = document.get("title")
        if (
            not isinstance(expected_title, str)
            or not lines
            or lines[0] != f"# {expected_title}"
        ):
            structure_failures.append(
                f"{source_path} H1 must exactly match its curriculum title"
            )

        positions: list[int] = []
        for heading in REQUIRED_PRACTICE_HEADINGS:
            indexes = [index for index, line in enumerate(lines) if line == heading]
            if len(indexes) != 1:
                structure_failures.append(
                    f"{source_path} requires exactly one {heading!r}; found {len(indexes)}"
                )
            else:
                positions.append(indexes[0])
        if len(positions) == len(REQUIRED_PRACTICE_HEADINGS):
            if positions != sorted(positions):
                structure_failures.append(
                    f"{source_path} practice headings are out of order"
                )

            follow_text = section_text(
                lines, "## Follow along — I show you exactly how"
            ).lower()
            recreate_text = section_text(
                lines, "## Now recreate it yourself"
            ).lower()
            if "expected result" not in follow_text:
                structure_failures.append(
                    f"{source_path} follow-along lacks an explicit expected result"
                )
            if not any(word in recreate_text for word in ("different", "new")):
                structure_failures.append(
                    f"{source_path} recreation does not require changed material"
                )

            inspection_text = section_text(
                lines, "## Ask Codex to check your work"
            )
            normalized_inspection = " ".join(inspection_text.lower().split())
            required_inspection_terms = (
                "read-only",
                "full path",
                "pass",
                "not yet",
            )
            missing_terms = [
                term
                for term in required_inspection_terms
                if term not in normalized_inspection
            ]
            if "[paste" not in normalized_inspection:
                missing_terms.append("[PASTE ...] path placeholder")
            if not any(
                phrase in normalized_inspection
                for phrase in (
                    "do not create",
                    "do not change",
                    "do not edit",
                )
            ):
                missing_terms.append("explicit no-change instruction")
            if not any(
                phrase in normalized_inspection
                for phrase in (
                    "real employer",
                    "real work",
                    "real client",
                    "no secrets",
                    "contains no secrets",
                )
            ):
                missing_terms.append("real-data or secret safety check")
            if missing_terms:
                inspection_failures.append(
                    f"{source_path} Codex prompt lacks: {', '.join(missing_terms)}"
                )

            pass_text = section_text(lines, "## Pass criteria")
            checklist_count = len(
                re.findall(r"^\s*-\s+\[\s\]\s+", pass_text, re.MULTILINE)
            )
            if checklist_count < 3:
                pass_failures.append(
                    f"{source_path} has {checklist_count} pass checkboxes; expected at least 3"
                )

    if structure_failures:
        report.failed(
            "beginner-practice-structure",
            compact(structure_failures, limit=24),
        )
    else:
        report.passed(
            "beginner-practice-structure",
            f"all {len(documents)} progress lessons use the ordered follow, recreate, inspect, and pass loop",
        )

    if inspection_failures:
        report.failed(
            "beginner-practice-codex-check",
            compact(inspection_failures, limit=24),
        )
    else:
        report.passed(
            "beginner-practice-codex-check",
            f"all {len(documents)} progress lessons include bounded read-only Codex inspection prompts",
        )

    if pass_failures:
        report.failed(
            "beginner-practice-pass-criteria",
            compact(pass_failures, limit=24),
        )
    else:
        report.passed(
            "beginner-practice-pass-criteria",
            f"all {len(documents)} progress lessons include objective pass checklists",
        )


def validate_beginner_terminology(root: Path, report: Report) -> None:
    failures: list[str] = []
    checked = 0
    for source_path, required_phrases in REQUIRED_ONBOARDING_PHRASES.items():
        path = root / source_path
        if not path.is_file():
            failures.append(f"{source_path} is missing")
            continue
        try:
            text = " ".join(
                path.read_text(encoding="utf-8").replace("*", "").split()
            ).lower()
        except Exception as exc:
            failures.append(f"{source_path} cannot be read: {exc}")
            continue
        for phrase in required_phrases:
            checked += 1
            if " ".join(phrase.split()).lower() not in text:
                failures.append(f"{source_path} lacks first-use explanation {phrase!r}")

    if failures:
        report.failed("beginner-first-use-terms", compact(failures, limit=24))
    else:
        report.passed(
            "beginner-first-use-terms",
            f"{checked} required first-use expansions and product explanations are present in onboarding",
        )


def validate_integrated_course_contract(
    root: Path, curriculum: dict[str, Any] | None, report: Report
) -> None:
    if curriculum is None:
        report.failed(
            "integrated-course-contract",
            "cannot validate the integrated contract without curriculum.json",
        )
        return

    repository_failures: list[str] = []
    artifact_failures: list[str] = []
    decision_failures: list[str] = []
    boundary_failures: list[str] = []
    dependency_failures: list[str] = []
    sequence_failures: list[str] = []

    modules = group_documents(curriculum, "modules")
    for number, document in enumerate(modules, start=1):
        source_path = document.get("sourcePath", f"module {number}")
        path = root / Path(*PurePosixPath(str(source_path)).parts)
        if not path.is_file():
            repository_failures.append(f"{source_path} is missing")
            continue
        text = path.read_text(encoding="utf-8")
        normalized = text.replace("/", "\\")
        required_repository_fragments = (
            PROJECT_REPOSITORY_FRAGMENT,
            f"evidence\\module-{number:02d}",
            f'git add -- "evidence\\module-{number:02d}"',
            f'git commit --only -m "complete module {number} evidence"',
            "COURSE_PROJECT.md",
            "rev-parse --show-toplevel",
        )
        for fragment in required_repository_fragments:
            if fragment not in normalized:
                repository_failures.append(
                    f"{source_path} lacks integrated repository step {fragment!r}"
                )
        if re.search(
            r"controlled-ai-course-practice[\\/]+module-\d+",
            text,
            re.IGNORECASE,
        ):
            repository_failures.append(
                f"{source_path} still creates a separate module practice root"
            )

        for template_name in MODULE_TEMPLATE_REFERENCES.get(number, ()):
            if template_name not in text:
                artifact_failures.append(
                    f"{source_path} does not teach or produce {template_name}"
                )

    if len(modules) != 9:
        repository_failures.append(
            f"integrated contract expected 9 modules; found {len(modules)}"
        )

    learning_sequence = curriculum.get("course", {}).get("learningSequenceIds")
    all_documents = [
        document
        for group in curriculum.get("groups", [])
        for document in group.get("documents", [])
    ]
    all_document_ids = {
        document.get("id")
        for document in all_documents
        if isinstance(document.get("id"), str)
    }
    core_document_ids = {
        document.get("id")
        for group in curriculum.get("groups", [])
        if group.get("core") is True
        or group.get("id") in curriculum.get("course", {}).get("coreGroupIds", [])
        for document in group.get("documents", [])
        if isinstance(document.get("id"), str)
    }
    if not isinstance(learning_sequence, list) or not learning_sequence:
        sequence_failures.append("course.learningSequenceIds is missing or empty")
    else:
        if len(learning_sequence) != len(set(learning_sequence)):
            sequence_failures.append("course.learningSequenceIds contains duplicates")
        unknown_ids = sorted(set(learning_sequence) - all_document_ids)
        if unknown_ids:
            sequence_failures.append(
                f"course.learningSequenceIds contains unknown IDs: {unknown_ids}"
            )
        missing_core = sorted(core_document_ids - set(learning_sequence))
        if missing_core:
            sequence_failures.append(
                f"course.learningSequenceIds omits core lessons: {missing_core}"
            )
        required_order = (
            "course-1-foundation-02",
            "course-1-beginner-software-check",
            "course-1-windows-setup",
            "course-1-foundation-03",
        )
        try:
            positions = [learning_sequence.index(item) for item in required_order]
            if positions != sorted(positions):
                sequence_failures.append(
                    "beginner learning order must be Foundation 2, software check, Windows Setup, Foundation 3"
                )
        except ValueError:
            sequence_failures.append(
                "beginner learning order lacks Foundation 2, software check, Windows Setup, or Foundation 3"
            )

    module_09_path = root / "modules" / "MODULE_09.md"
    if module_09_path.is_file():
        module_09_text = module_09_path.read_text(encoding="utf-8")
        for final_file in ("CAPSTONE_INDEX.md", "CHANGELOG.md"):
            if final_file not in module_09_text:
                artifact_failures.append(
                    f"modules/MODULE_09.md does not create {final_file}"
                )

    for source_path in FINAL_DECISION_FILES:
        path = root / Path(*PurePosixPath(source_path).parts)
        if not path.is_file():
            decision_failures.append(f"{source_path} is missing")
            continue
        text = path.read_text(encoding="utf-8")
        for decision in FINAL_DECISIONS:
            if decision not in text:
                decision_failures.append(
                    f"{source_path} lacks final decision {decision!r}"
                )
        for phrase in FORBIDDEN_FINAL_DECISION_PHRASES:
            if phrase.casefold() in text.casefold():
                decision_failures.append(
                    f"{source_path} retains obsolete final-decision phrase {phrase!r}"
                )

    beginner_files = (
        "README.md",
        "BEGINNER_READINESS_CHECK.md",
        "BEGINNER_SOFTWARE_CHECK.md",
        "SETUP_WINDOWS.md",
    )
    for source_path in beginner_files:
        path = root / source_path
        if not path.is_file():
            boundary_failures.append(f"{source_path} is missing")
            continue
        text = path.read_text(encoding="utf-8")
        if "EVERGREEN_UPDATE_PROMPT.md" in text:
            boundary_failures.append(
                f"{source_path} sends a beginner to the maintainer update prompt"
            )

    safety_files = (
        "SETUP_WINDOWS.md",
        "modules/MODULE_06.md",
        "templates/acceptance_and_handover.md",
    )
    for source_path in safety_files:
        path = root / Path(*PurePosixPath(source_path).parts)
        if not path.is_file():
            boundary_failures.append(f"{source_path} is missing")
            continue
        text = path.read_text(encoding="utf-8")
        if "EXTERNAL_ACTIONS_ENABLED=false" not in text:
            boundary_failures.append(
                f"{source_path} lacks EXTERNAL_ACTIONS_ENABLED=false"
            )
        if "KILL_SWITCH" in text:
            boundary_failures.append(
                f"{source_path} retains the ambiguous KILL_SWITCH setting"
            )

    requirements_path = root / "requirements-course.txt"
    if requirements_path.is_file():
        requirement_lines: list[str] = []
        requirement_options: list[str] = []
        logical_line = ""
        for raw_line in requirements_path.read_text(
            encoding="utf-8"
        ).splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("--") and not logical_line:
                requirement_options.append(line)
                continue
            logical_line += (" " if logical_line else "") + (
                line[:-1].strip() if line.endswith("\\") else line
            )
            if line.endswith("\\"):
                continue
            requirement_lines.append(logical_line)
            logical_line = ""
        if logical_line:
            dependency_failures.append(
                "requirements-course.txt ends with an incomplete continuation"
            )
        expected_options = {
            "--index-url=https://pypi.org/simple",
            "--only-binary=:all:",
            "--require-hashes",
        }
        if set(requirement_options) != expected_options or len(
            requirement_options
        ) != len(expected_options):
            dependency_failures.append(
                "requirements-course.txt must declare exactly the intended "
                "index, binary-only mode, and hash-required mode"
            )
        if not requirement_lines:
            dependency_failures.append(
                "requirements-course.txt has no required offline dependency"
            )
        for requirement in requirement_lines:
            if not re.fullmatch(
                r"[A-Za-z0-9_.-]+==[A-Za-z0-9_.+-]+"
                r"(?:\s+--hash=sha256:[0-9a-f]{64})+",
                requirement,
            ):
                dependency_failures.append(
                    "requirements-course.txt is not exactly version-and-hash "
                    f"pinned: {requirement!r}"
                )
        if any(line.casefold().startswith("openai") for line in requirement_lines):
            dependency_failures.append(
                "the optional OpenAI provider package remains in the required dependency set"
            )
        if not any(
            line.casefold().startswith("pytest==") for line in requirement_lines
        ):
            dependency_failures.append(
                "requirements-course.txt lacks an exact pytest pin"
            )
        if not any(
            line.casefold().startswith("jsonschema==")
            for line in requirement_lines
        ):
            dependency_failures.append(
                "requirements-course.txt lacks an exact jsonschema pin"
            )
    else:
        dependency_failures.append("requirements-course.txt is missing")

    setup_path = root / "SETUP_WINDOWS.md"
    if setup_path.is_file():
        setup_text = setup_path.read_text(encoding="utf-8")
        for fragment in (
            "& $pythonExe -m pip list --format=freeze",
            r"evidence\setup-dependencies.txt",
            "Do not install Node.js or n8n",
        ):
            if fragment not in setup_text:
                dependency_failures.append(
                    f"SETUP_WINDOWS.md lacks dependency boundary {fragment!r}"
                )

    workflow_path = root / ".github" / "workflows" / "pages.yml"
    if workflow_path.is_file():
        workflow_text = workflow_path.read_text(encoding="utf-8")
        action_refs = re.findall(
            r"^\s*uses:\s*([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)@([^\s#]+)",
            workflow_text,
            re.MULTILINE,
        )
        if not action_refs:
            dependency_failures.append("Pages workflow has no action references")
        for action_name, action_ref in action_refs:
            if not re.fullmatch(r"[0-9a-f]{40}", action_ref):
                dependency_failures.append(
                    f"{action_name} is not pinned to a full commit SHA"
                )

    if repository_failures:
        report.failed(
            "integrated-project-repository",
            compact(repository_failures, limit=30),
        )
    else:
        report.passed(
            "integrated-project-repository",
            "all 9 modules use one guarded Git repository, evidence/module-NN, and a pass-only checkpoint",
        )

    if artifact_failures:
        report.failed(
            "capstone-artifact-coverage",
            compact(artifact_failures, limit=20),
        )
    else:
        report.passed(
            "capstone-artifact-coverage",
            "Modules 1-3 and 7-9 use their required templates; Module 9 creates the final index and change log",
        )

    if decision_failures:
        report.failed(
            "course-final-decisions",
            compact(decision_failures, limit=24),
        )
    else:
        report.passed(
            "course-final-decisions",
            "all final-decision documents use the same three synthetic-only Course 1 outcomes",
        )

    if boundary_failures:
        report.failed(
            "learner-maintainer-and-action-boundaries",
            compact(boundary_failures, limit=20),
        )
    else:
        report.passed(
            "learner-maintainer-and-action-boundaries",
            "beginner start files avoid the mutating maintainer audit and action controls use EXTERNAL_ACTIONS_ENABLED=false",
        )

    if dependency_failures:
        report.failed(
            "reproducible-dependency-boundaries",
            compact(dependency_failures, limit=20),
        )
    else:
        report.passed(
            "reproducible-dependency-boundaries",
            "required Python packages and release actions are exactly pinned; optional provider and n8n tools remain outside core setup",
        )

    if sequence_failures:
        report.failed(
            "beginner-learning-sequence",
            compact(sequence_failures, limit=12),
        )
    else:
        report.passed(
            "beginner-learning-sequence",
            "the actionable sequence includes every core lesson and inserts the read-only software check plus Windows Setup before Foundation 3",
        )


def validate_course1_beginner_execution_contract(
    root: Path, curriculum: dict[str, Any] | None, report: Report
) -> None:
    """Catch learner-facing contradictions that heading checks cannot detect."""

    failures: list[str] = []

    controlled_python_files = (
        "SETUP_WINDOWS.md",
        "foundations/03_CODE_AND_PYTHON.md",
        "foundations/04_WEB_APIS_AND_JSON.md",
        "foundations/08_SAFE_AI_ASSISTED_BUILDING.md",
        "modules/MODULE_04.md",
        "modules/MODULE_05.md",
        "modules/MODULE_06.md",
        "modules/MODULE_08.md",
    )
    for source_path in controlled_python_files:
        path = root / source_path
        if not path.is_file():
            failures.append(f"{source_path} is missing")
            continue
        text = path.read_text(encoding="utf-8")
        if "Activate.ps1" in text:
            failures.append(
                f"{source_path} still depends on PowerShell environment activation"
            )
        powershell_blocks = re.findall(
            r"(?ms)^```(?:powershell|PowerShell|ps1)\s*\n(.*?)^```\s*$",
            text,
        )
        for block_number, block in enumerate(powershell_blocks, 1):
            if re.search(r"(?m)^\s*(?:python|python3|py|pip)\s+", block):
                failures.append(
                    f"{source_path} PowerShell block {block_number} contains a bare Python or pip learner command"
                )
        if "$pythonExe" not in text:
            failures.append(
                f"{source_path} does not define or use the controlled $pythonExe path"
            )

    for foundation_number in range(1, 10):
        candidates = sorted(
            (root / "foundations").glob(f"{foundation_number:02d}_*.md")
        )
        if len(candidates) != 1:
            failures.append(
                f"Foundation {foundation_number} does not resolve to exactly one file"
            )
            continue
        foundation_text = candidates[0].read_text(encoding="utf-8")
        resume_heading_count = len(
            re.findall(
                r"(?m)^#{2,4} Start or resume safely(?:\s|$)",
                foundation_text,
            )
        )
        if resume_heading_count != 1:
            failures.append(
                f"{candidates[0].relative_to(root)} must contain exactly one Start or resume safely section"
            )

    for module_number in range(1, 10):
        source_path = f"modules/MODULE_{module_number:02d}.md"
        path = root / source_path
        if not path.is_file():
            failures.append(f"{source_path} is missing")
            continue
        text = path.read_text(encoding="utf-8")
        for required in ("## Start or resume safely", "Suggested sessions:"):
            if required not in text:
                failures.append(f"{source_path} lacks {required!r}")

    beginner_block_contracts = {
        "modules/MODULE_01.md": (
            "Use eight focused blocks of 45–60 minutes",
            "stop at 60 minutes",
        ),
        "modules/MODULE_02.md": (
            "Use eight focused blocks of 45–60 minutes",
            "Never continue a block past 60",
        ),
        "modules/MODULE_03.md": (
            "Use ten focused blocks, each no longer than 60 minutes",
            "published 8–10-hour author estimate",
        ),
        "modules/MODULE_05.md": (
            "Use twelve focused blocks of 40–60 minutes",
            "No block exceeds 60",
        ),
        "modules/MODULE_07.md": (
            "Use twelve focused blocks of 40–60 minutes",
            "No block may exceed 60",
        ),
    }
    for source_path, required_fragments in beginner_block_contracts.items():
        path = root / source_path
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for fragment in (
            *required_fragments,
            "**UNDERSTAND**",
            "**PROTECTED PLUMBING",
        ):
            if fragment not in text:
                failures.append(
                    f"{source_path} lacks beginner block-plan contract "
                    f"{fragment!r}"
                )
        if re.search(
            r"(?i)(?:sessions?\s+of\s+(?:about\s+)?2\s*[-–]\s*3\s+hours"
            r"|2\s*[-–]\s*3[-– ]hour sessions?)",
            text,
        ):
            failures.append(
                f"{source_path} still recommends a 2–3-hour study session"
            )

    module_three_path = root / "modules" / "MODULE_03.md"
    if module_three_path.is_file():
        module_three = module_three_path.read_text(encoding="utf-8")
        matrix_contract_fragments = (
            "boundary_example,learner_explanation",
            "function Test-RuleExampleMatrix",
            "reason.Length -lt 20",
            "learner_explanation must contain at least 100 characters",
            "supplied_incorrect_matrix_case.csv",
            "supplied_corrected_matrix_case.csv",
            "matrix_checker_deliberate_failure.txt",
            "matrix_checker_correction_pass.txt",
            "EXPECTED FAILURE:",
            "The first record must remain failed",
            "case=R001-V; field=title;",
            "case=R011-D; field=status+due_date+assessment_date;",
            "Codex review below must inspect",
        )
        for fragment in matrix_contract_fragments:
            if fragment not in module_three:
                failures.append(
                    "Module 3 lacks bounded matrix/fail-retest contract "
                    f"{fragment!r}"
                )
        if "PASS: 11 rules x 4 example categories are present" in module_three:
            failures.append(
                "Module 3 still contains the obsolete nonblank-only matrix pass"
            )

    if isinstance(curriculum, dict):
        course = curriculum.get("course", {})
        learning_sequence = course.get("learningSequenceIds", [])
        document_paths = {
            document.get("id"): document.get("sourcePath")
            for group in curriculum.get("groups", [])
            if isinstance(group, dict)
            for document in group.get("documents", [])
            if isinstance(document, dict)
        }
        if len(learning_sequence) != 21:
            failures.append(
                f"Course 1 practical sequence must contain 21 pages; found {len(learning_sequence)}"
            )
        sequence_minimum = 0
        sequence_maximum = 0
        sequence_hours_complete = True
        documents_by_id = {
            document.get("id"): document
            for group in curriculum.get("groups", [])
            if isinstance(group, dict)
            for document in group.get("documents", [])
            if isinstance(document, dict)
        }
        for document_id in learning_sequence:
            source_path = document_paths.get(document_id)
            path = root / str(source_path)
            if not source_path or not path.is_file():
                failures.append(
                    f"required practice page {document_id!r} has no readable source"
                )
                continue
            text = path.read_text(encoding="utf-8")
            for practice_step in (
                "Follow along",
                "Now recreate it yourself",
                "Ask Codex to check your work",
                "Pass criteria",
            ):
                if practice_step not in text:
                    failures.append(
                        f"{source_path} lacks required practice step {practice_step!r}"
                    )
            estimate = documents_by_id.get(document_id, {}).get(
                "estimatedPracticeHours"
            )
            if not isinstance(estimate, dict) or not all(
                isinstance(estimate.get(key), int)
                for key in ("minimum", "maximum")
            ):
                sequence_hours_complete = False
            else:
                sequence_minimum += estimate["minimum"]
                sequence_maximum += estimate["maximum"]
        declared_hours = course.get("estimatedHours", {})
        if sequence_hours_complete and (
            declared_hours.get("minimum") != sequence_minimum
            or declared_hours.get("maximum") != sequence_maximum
        ):
            failures.append(
                "Course total-hour range does not equal the 21 required page "
                f"ranges: declared {declared_hours.get('minimum')}-"
                f"{declared_hours.get('maximum')}, calculated "
                f"{sequence_minimum}-{sequence_maximum}"
            )

    module_two_path = root / "modules" / "MODULE_02.md"
    scorecard_path = root / "templates" / "workflow_opportunity_scorecard.md"
    if module_two_path.is_file() and scorecard_path.is_file():
        combined = (
            module_two_path.read_text(encoding="utf-8")
            + "\n"
            + scorecard_path.read_text(encoding="utf-8")
        )
        required_score_factors = (
            "Repeated volume or frequency",
            "Measurable time, waiting, error, or rework",
            "Stable unit of work and completion condition",
            "Rules can be stated and tested",
            "Input data is available and understandable",
            "Process owner and reviewer are available",
            "Course evaluation can be synthetic, bounded, and reversible",
            "Users have a reason and capacity to adopt it",
            "Manual fallback is practical",
        )
        if "maximum 20" in combined or re.search(
            r"Scale:\s*0\s*=\s*poor.+?2\s*=\s*supported",
            combined,
            re.IGNORECASE | re.DOTALL,
        ):
            failures.append("Module 2 retains the obsolete 0-2 / maximum-20 score")
        if combined.count("maximum 27") < 2:
            failures.append(
                "Module 2 and its scorecard do not both use the maximum-27 contract"
            )
        for factor in required_score_factors:
            if factor not in combined:
                failures.append(f"canonical opportunity score lacks {factor!r}")

    assessment_path = root / "ASSESSMENT_AND_RUBRIC.md"
    if assessment_path.is_file():
        assessment = assessment_path.read_text(encoding="utf-8")
        for fragment in (
            "area points = area weight × level ÷ 4",
            "total is at least 75 points",
            "EXTERNAL UAT NOT VERIFIED",
            "They are independent",
        ):
            if fragment not in assessment:
                failures.append(
                    f"ASSESSMENT_AND_RUBRIC.md lacks objective rule {fragment!r}"
                )

    beginner_repair_contracts = {
        "BEGINNER_READINESS_CHECK.md": (
            "Required readiness exercise — complete before Foundation 1",
            "Do not begin Foundation 1 while any box above remains unchecked",
        ),
        "foundations/01_FILES_AND_TEXT.md": (
            "selected lesson-attempt folder",
            "foundation-01-retry-XX",
        ),
        "foundations/03_CODE_AND_PYTHON.md": (
            "You may access exactly these two locations",
            "Execute, but do not edit or replace, this one project Python file",
        ),
        "foundations/04_WEB_APIS_AND_JSON.md": (
            "Create a safe retry attempt",
            "Created request.json once",
            "Created response.json once",
            "You may access exactly these two locations",
        ),
        "foundations/07_AI_AND_CONTROLLED_WORKFLOWS.md": (
            "The required Course 1 exercise is fully local",
            "Do not call a live model",
        ),
        "foundations/08_SAFE_AI_ASSISTED_BUILDING.md": (
            "You may access exactly these two locations",
            "Execute, but do not edit or replace, this one project Python file",
        ),
        "modules/MODULE_01.md": (
            "complete Foundations 3 through 9",
            "Open-CreateOnceCourseFile",
            "non-detection is not proof",
            "Readiness → Foundations 1–2 → Software Check and Windows Setup →",
        ),
        "modules/MODULE_02.md": (
            "Open-CreateOnceCourseFile",
            "non-detection is not proof",
        ),
        "modules/MODULE_03.md": (
            "Open-CreateOnceCourseFile",
            "it still works after PowerShell has been closed",
        ),
        "modules/MODULE_04.md": (
            "reference_runner_hashes.json",
            "differs from the controlled course source",
            "A missing, wrong-type, changed, or partly copied runner file",
            "The controlled runner folder contains an unexpected entry",
        ),
        "modules/MODULE_05.md": (
            "function Resolve-SavedCourseRun",
            "reference_runner_hashes.json",
            "Safe stopping points",
            "The controlled runner folder contains an unexpected entry",
        ),
        "modules/MODULE_06.md": (
            "function Resolve-SavedCourseRun",
            "reference_runner_hashes.json",
            "Do not replay a completed",
            "$workedRunDir = Join-Path $workedDecisionParent (Split-Path -Leaf $moduleFiveWorkedRunDir)",
            "$recreatedRunDir = Join-Path $recreatedDecisionParent (Split-Path -Leaf $moduleFiveRecreatedRunDir)",
            "source/expected_issues.evidence",
            "Which eight protected artifact paths",
            "The controlled runner folder contains an unexpected entry",
        ),
        "modules/MODULE_07.md": (
            "Open-CreateOnceCourseFile",
            "non-detection is not proof",
        ),
        "modules/MODULE_08.md": (
            "CurrentCulture",
            "Completion marker: USABILITY TEST COMPLETE",
            "COURSE_PROJECT.md",
            "function Get-SavedCourseRunLocator",
            "initial_copy_hashes.json",
            "$controlledExpectedHash -ne $recreatedExpectedHash",
            "recreated_expected.csv does not match the controlled course answer key",
            "This statement is an attestation, not proof",
            "non-detection is not proof that none exists",
        ),
        "modules/MODULE_09.md": (
            "PRESERVED INCOMPLETE ATTEMPT",
            "COURSE_PROJECT.md",
            "failures\\latest.json",
            "function Resolve-SavedCourseRun",
            "reference_runner_hashes.json",
            "$savedRunnerHash[0].source_sha256 -ne",
            "The controlled runner folder contains an unexpected entry",
            "This statement is an attestation, not proof",
            "non-detection is not proof that none exists",
        ),
    }
    for relative_path, fragments in beginner_repair_contracts.items():
        repair_path = root / relative_path
        if not repair_path.is_file():
            failures.append(f"beginner repair contract is missing {relative_path}")
            continue
        repair_text = repair_path.read_text(encoding="utf-8")
        for fragment in fragments:
            if fragment not in repair_text:
                failures.append(
                    f"{relative_path} lacks repaired beginner contract {fragment!r}"
                )

    module_eight_path = root / "modules" / "MODULE_08.md"
    if module_eight_path.is_file():
        module_eight = module_eight_path.read_text(encoding="utf-8")
        if (
            'key = (row["work_item_id"], row["rule_code"], row["field"])'
            not in module_eight
        ):
            failures.append(
                "Module 8 does not evaluate occurrences by item, rule, and field"
            )
        if "templates\\pilot_decision_record.md" not in module_eight:
            failures.append(
                "Module 8 does not use the Course 1 final-decision worksheet"
            )
        if "found_issues.csv" in module_eight:
            failures.append("Module 8 still references nonexistent found_issues.csv")
        for fragment in (
            r"issues\issues.csv",
            "PROVISIONAL PRE-UAT",
            "not the final Course 1 decision",
            "recreated_module4_provenance.json",
            "source_project_relative",
            "destination_sha256",
            "recreated_matched_timing.md",
            "recreated_cost_scenarios.csv",
            "Completed low/expected/high cost scenarios",
            "licence/usage",
            "one-time setup",
        ):
            if fragment not in module_eight:
                failures.append(
                    f"Module 8 lacks current evaluation contract {fragment!r}"
                )

    module_nine_path = root / "modules" / "MODULE_09.md"
    if module_nine_path.is_file():
        module_nine = module_nine_path.read_text(encoding="utf-8")
        for fragment in (
            "TECH-01",
            "TECH-09",
            "TECH-D01",
            "FINAL POST-REHEARSAL",
            "recreated_course_assessment.md",
            "All ten oral questions",
            "function New-TechAttemptFolder",
            "attempt-info.json",
            "prior_attempts_preserved",
            "unseen_second_domain_transfer_lock.json",
            "retention_task_card.md",
            "lock_schema = 'course1-transfer-lock-v1'",
            "locked_at_utc",
            "transfer_sha256",
            "retention_task_card_sha256",
            "$checkedAt = [DateTimeOffset]::UtcNow",
            "$elapsedTotalDays = ($checkedAt - $lockedAt).TotalDays",
            "$elapsedWholeDays = [math]::Floor($elapsedTotalDays)",
            "$dueStart = $lockedAt.AddDays(7)",
            "$dueEndExclusive = $lockedAt.AddDays(15)",
            "WORKED ANSWERS OPENED BEFORE CHECK: YES / NO",
        ):
            if fragment not in module_nine:
                failures.append(
                    f"Module 9 lacks executable closeout contract {fragment!r}"
                )
        for scenario_number in range(1, 10):
            scenario_id = f"TECH-{scenario_number:02d}"
            match = re.search(
                rf"(?ms)^#### {re.escape(scenario_id)}\b.*?(?=^#### |^### )",
                module_nine,
            )
            if not match:
                failures.append(f"Module 9 lacks a distinct {scenario_id} section")
                continue
            scenario = match.group(0)
            for label in ("**Given:**", "**When:**", "**Then:**"):
                if label not in scenario:
                    failures.append(
                        f"Module 9 {scenario_id} lacks explicit {label.strip('*:')}"
                    )
            workspace_token = (
                f"$tech{scenario_number:02d}Workspace = "
                f"New-TechAttemptFolder -ScenarioId '{scenario_id}'"
            )
            if workspace_token not in scenario:
                failures.append(
                    f"Module 9 {scenario_id} does not create a fresh isolated attempt"
                )
        if (
            "$defectFolder = New-TechAttemptFolder -ScenarioId 'TECH-D01'"
            not in module_nine
        ):
            failures.append(
                "Module 9 TECH-D01 does not create a fresh isolated attempt"
            )
        if re.search(
            r"(?m)^####\s+UAT-(?:0[1-9]|D01)\b"
            r"|New-TechAttemptFolder\s+-ScenarioId\s+['\"]UAT-",
            module_nine,
        ):
            failures.append(
                "Module 9 still labels solo technical rehearsals with reserved UAT IDs"
            )
        for required_uat_boundary in (
            "external_synthetic_uat.md",
            "task IDs `UAT-01` onward",
            "REAL SYNTHETIC UAT: VERIFIED",
        ):
            if required_uat_boundary not in module_nine:
                failures.append(
                    "Module 9 lacks the separate intended-user UAT boundary "
                    f"{required_uat_boundary!r}"
                )
        for required_fragment in (
            "latest_attempt_state",
            "last valid `current_state`",
            "Role,RelativePath,SHA256",
            "It does not store your Windows username or an absolute computer path",
        ):
            if required_fragment not in module_nine:
                failures.append(
                    f"Module 9 lacks state/path evidence contract {required_fragment!r}"
                )
        if re.search(r"Select-Object\s+Path\s*,\s*Hash", module_nine):
            failures.append("Module 9 still exports absolute hash paths")

    uat_template_path = root / "templates" / "uat_script.md"
    uat_example_path = root / "worked_examples" / "module_09_uat_script.md"
    if uat_template_path.is_file() and uat_example_path.is_file():
        uat_template = uat_template_path.read_text(encoding="utf-8")
        uat_example = uat_example_path.read_text(encoding="utf-8")
        for fragment in (
            "### TECH-[NN] — [Technical scenario name]",
            "### UAT-[NN] — [Intended-user task name]",
            "NOT EXECUTED — EXTERNAL UAT NOT VERIFIED",
            "**Given**",
            "**When**",
            "**Then**",
        ):
            if fragment not in uat_template:
                failures.append(f"UAT template lacks {fragment!r}")
        for scenario_number in range(1, 10):
            scenario_id = f"TECH-{scenario_number:02d}"
            if scenario_id not in uat_example:
                failures.append(
                    f"completed role-simulated rehearsal example lacks {scenario_id}"
                )
        candidate_heading = re.search(
            r"(?im)^##\s+Candidate intended-user task[^\r\n]*$",
            uat_example,
        )
        if not candidate_heading:
            failures.append(
                "role-simulated rehearsal example lacks a separate candidate "
                "intended-user task section"
            )
        else:
            candidate_start = candidate_heading.start()
            following_heading = re.search(
                r"(?m)^##\s+", uat_example[candidate_heading.end() :]
            )
            candidate_end = (
                candidate_heading.end() + following_heading.start()
                if following_heading
                else len(uat_example)
            )
            candidate_uat = uat_example[candidate_start:candidate_end]
            solo_example = (
                uat_example[:candidate_start] + uat_example[candidate_end:]
            )
            for task_number in range(1, 7):
                task_id = f"UAT-{task_number:02d}"
                if task_id not in candidate_uat:
                    failures.append(
                        "candidate intended-user task section lacks "
                        f"{task_id}"
                    )
            if (
                "NOT EXECUTED — EXTERNAL UAT NOT VERIFIED"
                not in candidate_uat
            ):
                failures.append(
                    "candidate intended-user tasks are not explicitly marked "
                    "NOT EXECUTED — EXTERNAL UAT NOT VERIFIED"
                )
            if re.search(r"\bUAT-(?:0[1-9]|D01)\b", solo_example):
                failures.append(
                    "role-simulated rehearsal example records reserved UAT IDs "
                    "outside the unexecuted candidate-user section"
                )
        if not candidate_heading and re.search(
            r"\bUAT-(?:0[1-9]|D01)\b", uat_example
        ):
            failures.append(
                "role-simulated rehearsal example uses IDs reserved for real UAT"
            )
        if re.search(r"\bUAT-\d{3}\b", uat_template + "\n" + uat_example):
            failures.append("UAT template/example still uses three-digit scenario IDs")

    architecture_path = root / "ARCHITECTURE_AND_CONTRACTS.md"
    capstone_path = root / "CAPSTONE_SPECIFICATION.md"
    if architecture_path.is_file() and capstone_path.is_file():
        live_boundary = (
            architecture_path.read_text(encoding="utf-8")
            + "\n"
            + capstone_path.read_text(encoding="utf-8")
        )
        for fragment in (
            "Course 1 uses only the offline mock and deterministic fallback",
            "No live provider is used in the Course 1 capstone",
            "PROVISIONAL PRE-UAT",
            "FINAL POST-UAT",
        ):
            if fragment not in live_boundary:
                failures.append(
                    f"architecture/capstone boundary lacks {fragment!r}"
                )
        for fragment in (
            "last valid `current_state`",
            "`latest_attempt_state`",
            "does **not** overwrite",
        ):
            if fragment not in live_boundary:
                failures.append(
                    f"architecture/capstone state boundary lacks {fragment!r}"
                )

    course_boundary_paths = (
        "README.md",
        "COURSE_OVERVIEW.md",
        "ASSESSMENT_AND_RUBRIC.md",
        "CAREER_SEQUENCE.md",
        "curriculum.json",
        "app/src/app.js",
    )
    course_boundary_text = "\n".join(
        (root / source_path).read_text(encoding="utf-8")
        for source_path in course_boundary_paths
        if (root / source_path).is_file()
    )
    for obsolete_claim in (
        "Evidence-linked AI summary",
        "add artificial intelligence (AI) only where it helps",
        "uses AI only for bounded issue-linked explanation",
    ):
        if obsolete_claim in course_boundary_text:
            failures.append(
                f"learner overview still implies live Course 1 AI: {obsolete_claim!r}"
            )
    if course_boundary_text.count("Course 1 makes no live AI call") < 2:
        failures.append(
            "learner overview does not repeat the no-live-AI Course 1 boundary"
        )

    runner_workflow_path = root / "course1_capstone" / "workflow.py"
    runner_cli_path = root / "course1_capstone" / "cli.py"
    module_six_path = root / "modules" / "MODULE_06.md"
    if (
        runner_workflow_path.is_file()
        and runner_cli_path.is_file()
        and module_six_path.is_file()
    ):
        runner_workflow = runner_workflow_path.read_text(encoding="utf-8")
        runner_cli = runner_cli_path.read_text(encoding="utf-8")
        module_six = module_six_path.read_text(encoding="utf-8")
        if (
            "worked-decision-run" in module_six
            or "recreated-decision-run" in module_six
        ):
            failures.append(
                "Module 6 renames a protected run instead of preserving its exact RUN identifier"
            )
        for fragment in (
            "def _write_latest_run_locator",
            '"latest_attempt_state": events[-1]["state"]',
            "path.name",
        ):
            if fragment not in runner_workflow:
                failures.append(
                    f"Course 1 runner lacks path/state safeguard {fragment!r}"
                )
        if "relative_artifact_locator" not in runner_cli:
            failures.append("Course 1 CLI lacks neutral artifact locators")
        for fragment in (
            "raw_diagnostics_committed = $false",
            "outside_repository_temporary_file",
            "path-neutral structured automated",
        ):
            if fragment not in module_six:
                failures.append(
                    f"Module 6 lacks path-neutral test evidence rule {fragment!r}"
                )

    software_matrix_path = root / "SOFTWARE_MATRIX.md"
    stack_manifest_path = root / "stack-manifest.yaml"
    if software_matrix_path.is_file() and stack_manifest_path.is_file():
        software_text = software_matrix_path.read_text(encoding="utf-8")
        stack_text = stack_manifest_path.read_text(encoding="utf-8")
        software_and_stack = " ".join(f"{software_text}\n{stack_text}".split())
        for fragment in (
            "Course 1 contains no provider package, live-model option, API key, or paid call",
            "live_provider_in_course1: false",
            "status: deferred",
        ):
            if fragment not in software_and_stack:
                failures.append(
                    f"software/stack Course 1 provider boundary lacks {fragment!r}"
                )

    module_time_contracts = {
        "modules/MODULE_04.md": r"12[–-]16 hours",
        "modules/MODULE_06.md": r"8[–-]12 hours",
        "modules/MODULE_09.md": r"16[–-]22 hours",
    }
    for source_path, pattern in module_time_contracts.items():
        path = root / source_path
        if not path.is_file() or not re.search(
            pattern, path.read_text(encoding="utf-8")
        ):
            failures.append(
                f"{source_path} does not match its current curriculum time range"
            )

    template_index_path = root / "templates" / "README.md"
    if template_index_path.is_file():
        template_lines = template_index_path.read_text(encoding="utf-8").splitlines()
        advanced_section = section_text(
            template_lines, "## Advanced follow-on templates"
        )
        if "acceptance_and_handover.md" in advanced_section:
            failures.append(
                "acceptance_and_handover.md is still classified as advanced-only"
            )

    worked_example_paths = (
        "worked_examples/README.md",
        "worked_examples/module_07_risk_and_escalation_screen.md",
        "worked_examples/module_07_tool_fit_and_ownership_record.md",
        "worked_examples/module_09_uat_script.md",
        "worked_examples/module_09_adoption_and_training_plan.md",
        "worked_examples/module_09_acceptance_and_handover.md",
        "worked_examples/module_09_assessment_record.md",
    )
    configured_paths = {
        document.get("sourcePath")
        for group in (curriculum or {}).get("groups", [])
        for document in group.get("documents", [])
        if isinstance(document, dict)
    }
    for source_path in worked_example_paths:
        if not (root / source_path).is_file():
            failures.append(f"completed beginner example is missing: {source_path}")
        if source_path not in configured_paths:
            failures.append(
                f"completed beginner example is not bundled in the PWA: {source_path}"
            )

    if failures:
        report.failed(
            "course1-beginner-execution-contract",
            compact(failures, limit=40),
        )
    else:
        report.passed(
            "course1-beginner-execution-contract",
            "all 21 practice loops, controlled Python, resume blocks, one score, generated issue paths, provisional/final decisions, executable UAT, assessment gates, time ranges, and completed examples agree",
        )


def validate_current_json(root: Path, report: Report) -> None:
    failures: list[str] = []
    json_files = iter_current_files(root, ".json")
    for path in json_files:
        try:
            load_json_value(path)
        except Exception as exc:
            failures.append(f"{path.relative_to(root)}: {exc}")
    if failures:
        report.failed("current-json-syntax", compact(failures))
    else:
        report.passed(
            "current-json-syntax",
            f"{len(json_files)} in-scope JSON files parsed",
        )


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
        failures.append(f"{label} is missing keys: {missing}")
    if unknown:
        failures.append(f"{label} has unknown keys: {unknown}")
    return value


def safe_repository_file(
    root: Path,
    locator: Any,
    *,
    label: str,
    failures: list[str],
    release_evidence_only: bool = False,
    release_evidence_json_only: bool = True,
) -> Path | None:
    if not is_nonempty_string(locator):
        failures.append(f"{label} must be a non-empty relative path")
        return None
    text = str(locator)
    pure = PurePosixPath(text)
    if (
        pure.is_absolute()
        or "\\" in text
        or "//" in text
        or not pure.parts
        or any(part in {"", ".", ".."} for part in pure.parts)
    ):
        failures.append(f"{label} is not a safe repository-relative path: {text}")
        return None
    if release_evidence_only and (
        pure.parts[0] != "release_evidence"
        or len(pure.parts) < 2
        or pure.parts[1] == "templates"
        or not pure.suffix
        or (
            release_evidence_json_only
            and pure.suffix.casefold() != ".json"
        )
    ):
        failures.append(
            f"{label} must name a non-template "
            f"{'JSON ' if release_evidence_json_only else ''}"
            f"file inside release_evidence/: {text}"
        )
        return None
    resolved = (root / Path(*pure.parts)).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        failures.append(f"{label} escapes the repository: {text}")
        return None
    if not resolved.is_file():
        failures.append(f"{label} does not exist: {text}")
        return None
    return resolved


def markdown_cells(line: str) -> list[str] | None:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return None
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def expected_technical_requirements() -> set[str]:
    return {
        f"C1-TA-{family}-{number:03d}"
        for family, count in TECHNICAL_REQUIREMENT_FAMILY_COUNTS.items()
        for number in range(1, count + 1)
    }


def expand_requirement_references(
    cell: str,
    *,
    label: str,
    failures: list[str],
) -> set[str]:
    values = set(re.findall(r"C1-TA-[A-Z]+-\d{3}", cell))
    range_re = re.compile(
        r"C1-TA-(?P<first_family>[A-Z]+)-(?P<first>\d{3})"
        r"`?\s*[–—]\s*`?"
        r"C1-TA-(?P<last_family>[A-Z]+)-(?P<last>\d{3})"
    )
    for match in range_re.finditer(cell):
        first_family = match.group("first_family")
        last_family = match.group("last_family")
        first = int(match.group("first"))
        last = int(match.group("last"))
        if first_family != last_family or first > last:
            failures.append(f"{label} contains an invalid requirement range")
            continue
        values.update(
            f"C1-TA-{first_family}-{number:03d}"
            for number in range(first, last + 1)
        )
    return values


def parse_technical_contract(
    contract_text: str,
    failures: list[str],
) -> tuple[
    dict[str, set[str]],
    dict[str, set[str]],
]:
    requirement_rows: dict[str, set[str]] = {}
    test_rows: dict[str, set[str]] = {}
    seen_requirement_ids: list[str] = []
    seen_test_ids: list[str] = []

    for line_number, line in enumerate(contract_text.splitlines(), 1):
        cells = markdown_cells(line)
        if cells is None or not cells:
            continue
        first = cells[0]
        if "C1-TA-" in first:
            match = re.fullmatch(r"`(C1-TA-[A-Z]+-\d{3})`", first)
            if match is None:
                failures.append(
                    f"technical contract line {line_number} has a malformed requirement ID"
                )
                continue
            requirement_id = match.group(1)
            seen_requirement_ids.append(requirement_id)
            if len(cells) not in {2, 3, 4}:
                failures.append(
                    f"{requirement_id} row has {len(cells)} cells; expected 2, 3, or 4"
                )
            direct_tests = set(re.findall(r"C1-TST-(?:[A-Z0-9]+-)+\d{3}", line))
            requirement_rows[requirement_id] = direct_tests
        elif "C1-TST-" in first:
            match = re.fullmatch(r"`(C1-TST-(?:[A-Z0-9]+-)+\d{3})`", first)
            if match is None:
                failures.append(
                    f"technical contract line {line_number} has a malformed test ID"
                )
                continue
            test_id = match.group(1)
            seen_test_ids.append(test_id)
            if len(cells) != 4:
                failures.append(
                    f"{test_id} row has {len(cells)} cells; expected exactly 4"
                )
                mapped = set()
            else:
                mapped = expand_requirement_references(
                    cells[2],
                    label=f"{test_id} mapping",
                    failures=failures,
                )
            test_rows[test_id] = mapped
        elif first.startswith("`C1-") or first.startswith("C1-"):
            failures.append(
                f"technical contract line {line_number} has an unsupported ID family"
            )

    duplicate_requirements = sorted(
        identifier
        for identifier, count in Counter(seen_requirement_ids).items()
        if count > 1
    )
    duplicate_tests = sorted(
        identifier
        for identifier, count in Counter(seen_test_ids).items()
        if count > 1
    )
    if duplicate_requirements:
        failures.append(
            f"technical contract has duplicate requirement rows: {duplicate_requirements}"
        )
    if duplicate_tests:
        failures.append(
            f"technical contract has duplicate test rows: {duplicate_tests}"
        )
    return requirement_rows, test_rows


def validate_technical_evidence_record(
    value: Any,
    *,
    root: Path,
    evidence_record_path: Path,
    label: str,
    expected_test_id: str,
    expected_evidence_class: str,
    expected_result: str,
    expected_procedures: set[tuple[str, str]],
    expected_environments: set[str],
    failures: list[str],
    seen_artifact_paths: set[str] | None = None,
) -> tuple[str | None, dict[str, Any] | None]:
    record = exact_keys(
        value,
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
        label,
        failures,
    )
    if record.get("schemaVersion") != "course1-technical-evidence-v1":
        failures.append(f"{label}.schemaVersion is unsupported")
    evidence_id = record.get("evidenceId")
    if not isinstance(evidence_id, str) or not re.fullmatch(
        r"C1-EV-[A-Z0-9-]+-\d{3}", evidence_id
    ):
        failures.append(f"{label}.evidenceId is malformed")
        evidence_id = None
    if record.get("testId") != expected_test_id:
        failures.append(f"{label}.testId does not match {expected_test_id}")
    if record.get("result") != expected_result:
        failures.append(f"{label}.result does not match {expected_result}")
    if record.get("evidenceClass") != expected_evidence_class:
        failures.append(
            f"{label}.evidenceClass does not match {expected_evidence_class}"
        )
    timestamp = record.get("recordedAt")
    if not is_nonempty_string(timestamp):
        failures.append(f"{label}.recordedAt must be an ISO 8601 timestamp")
    else:
        try:
            normalized = timestamp[:-1] + "+00:00" if timestamp.endswith("Z") else timestamp
            parsed = datetime.fromisoformat(normalized)
            if parsed.tzinfo is None:
                raise ValueError("timezone missing")
        except ValueError:
            failures.append(
                f"{label}.recordedAt must be a valid ISO 8601 timestamp with timezone"
            )

    candidate = exact_keys(
        record.get("candidate"),
        {"commit", "courseVersion", "buildId", "contentHash"},
        f"{label}.candidate",
        failures,
    )
    if not re.fullmatch(r"[0-9a-f]{40}", str(candidate.get("commit", ""))):
        failures.append(f"{label}.candidate.commit must be a full Git SHA")
    if not SEMVER_RE.fullmatch(str(candidate.get("courseVersion", ""))):
        failures.append(f"{label}.candidate.courseVersion must use x.y.z")
    if not re.fullmatch(r"[0-9a-f]{12}", str(candidate.get("buildId", ""))):
        failures.append(f"{label}.candidate.buildId must be 12 lowercase hex")
    if not re.fullmatch(r"[0-9a-f]{64}", str(candidate.get("contentHash", ""))):
        failures.append(f"{label}.candidate.contentHash must be SHA-256")

    reviewer = exact_keys(
        record.get("reviewer"),
        {"name", "independentOfImplementation"},
        f"{label}.reviewer",
        failures,
    )
    if not is_nonempty_string(reviewer.get("name")):
        failures.append(f"{label}.reviewer.name must be recorded")
    if not isinstance(reviewer.get("independentOfImplementation"), bool):
        failures.append(
            f"{label}.reviewer.independentOfImplementation must be boolean"
        )
    if (
        expected_evidence_class == "INDEPENDENT_REVIEW"
        and reviewer.get("independentOfImplementation") is not True
    ):
        failures.append(
            f"{label} independent-review evidence requires an independent reviewer"
        )

    artifacts = record.get("artifacts")
    if (
        not isinstance(artifacts, list)
        or not artifacts
        or any(not isinstance(item, dict) for item in artifacts)
    ):
        failures.append(
            f"{label}.artifacts must be a non-empty list of closed artifact objects"
        )
        artifacts = []
    artifact_paths: list[str] = []
    bindings: list[tuple[str, str, str, str]] = []
    actual_procedures: set[tuple[str, str]] = set()
    actual_environments: set[str] = set()
    evidence_record_relative = evidence_record_path.relative_to(root).as_posix()
    for index, raw_artifact in enumerate(artifacts):
        artifact_label = f"{label}.artifacts[{index}]"
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
        artifact_path_text = artifact.get("path")
        if isinstance(artifact_path_text, str):
            artifact_paths.append(artifact_path_text)
            if seen_artifact_paths is not None:
                if artifact_path_text in seen_artifact_paths:
                    failures.append(
                        f"duplicate raw technical artifact path: {artifact_path_text}"
                    )
                seen_artifact_paths.add(artifact_path_text)
            if artifact_path_text == evidence_record_relative:
                failures.append(
                    f"{artifact_label}.path cannot be its own evidence record"
                )
        expected_hash = artifact.get("sha256")
        if not isinstance(expected_hash, str) or not re.fullmatch(
            r"[0-9a-f]{64}", expected_hash
        ):
            failures.append(
                f"{artifact_label}.sha256 must be lowercase SHA-256"
            )
        artifact_kind = artifact.get("kind")
        if artifact_kind not in TECHNICAL_ARTIFACT_KINDS:
            failures.append(f"{artifact_label}.kind is unsupported")
        procedure_locator = artifact.get("procedureLocator")
        procedure_selector = artifact.get("procedureSelector")
        environment = artifact.get("environment")
        if (
            is_nonempty_string(procedure_locator)
            and is_nonempty_string(procedure_selector)
            and is_nonempty_string(environment)
            and isinstance(artifact_kind, str)
        ):
            procedure = (
                str(procedure_locator),
                str(procedure_selector),
            )
            actual_procedures.add(procedure)
            actual_environments.add(str(environment))
            bindings.append(
                (
                    procedure[0],
                    procedure[1],
                    str(environment),
                    artifact_kind,
                )
            )
        else:
            failures.append(
                f"{artifact_label} procedure and environment binding must be recorded"
            )
        artifact_path = safe_repository_file(
            root,
            artifact_path_text,
            label=f"{artifact_label}.path",
            failures=failures,
            release_evidence_only=True,
            release_evidence_json_only=False,
        )
        if artifact_path is None:
            continue
        try:
            artifact_bytes = artifact_path.read_bytes()
        except OSError as exc:
            failures.append(f"{artifact_label}.path could not be read: {exc}")
            continue
        if not artifact_bytes:
            failures.append(f"{artifact_label}.path is empty")
        if expected_hash != hashlib.sha256(artifact_bytes).hexdigest():
            failures.append(
                f"{artifact_label}.sha256 does not match the artifact file"
            )
    duplicate_artifact_paths = sorted(
        path
        for path, count in Counter(artifact_paths).items()
        if count > 1
    )
    duplicate_bindings = sorted(
        binding
        for binding, count in Counter(bindings).items()
        if count > 1
    )
    if duplicate_artifact_paths:
        failures.append(
            f"{label} has duplicate artifact paths: {duplicate_artifact_paths}"
        )
    if duplicate_bindings:
        failures.append(
            f"{label} has duplicate procedure/environment/kind bindings: "
            f"{duplicate_bindings}"
        )
    missing_procedures = sorted(expected_procedures - actual_procedures)
    unexpected_procedures = sorted(actual_procedures - expected_procedures)
    missing_environments = sorted(expected_environments - actual_environments)
    unexpected_environments = sorted(actual_environments - expected_environments)
    if missing_procedures:
        failures.append(
            f"{label} is missing declared procedure artifact coverage: "
            f"{missing_procedures}"
        )
    if unexpected_procedures:
        failures.append(
            f"{label} has undeclared procedure artifact bindings: "
            f"{unexpected_procedures}"
        )
    if missing_environments:
        failures.append(
            f"{label} is missing declared environment artifact coverage: "
            f"{missing_environments}"
        )
    if unexpected_environments:
        failures.append(
            f"{label} has undeclared environment artifact bindings: "
            f"{unexpected_environments}"
        )
    return evidence_id, candidate or None


def technical_audit_control_failures(
    root: Path,
    *,
    contract_text: str | None = None,
    graph: dict[str, Any] | None = None,
    manifest: dict[str, Any] | None = None,
) -> list[str]:
    failures: list[str] = []
    contract_path = root / "COURSE_1_TECHNICAL_ACCEPTANCE_CONTRACT.md"
    graph_path = root / "audit_control/course1/technical_requirement_graph.json"
    manifest_path = root / "audit_control/course1/technical_test_manifest.json"
    schema_paths = (
        root / "audit_control/course1/technical_requirement_graph.schema.json",
        root / "audit_control/course1/technical_test_manifest.schema.json",
        root / "audit_control/course1/technical_evidence_record.schema.json",
        root / "audit_control/course1/promotion_record.schema.json",
        root / "audit_control/course1/final_acceptance_record.schema.json",
        root / "audit_control/course1/rollback_record.schema.json",
    )

    for path in (contract_path, graph_path, manifest_path, *schema_paths):
        if not path.is_file():
            failures.append(f"required audit-control file is missing: {path.relative_to(root)}")
    if failures:
        return failures

    try:
        if contract_text is None:
            contract_text = contract_path.read_text(encoding="utf-8")
        if graph is None:
            graph = load_json_object(graph_path)
        if manifest is None:
            manifest = load_json_object(manifest_path)
        schemas = [load_json_object(path) for path in schema_paths]
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"could not load technical audit control: {exc}"]

    contract_requirements, contract_tests = parse_technical_contract(
        contract_text,
        failures,
    )
    expected_requirements = expected_technical_requirements()
    if set(contract_requirements) != expected_requirements:
        missing = sorted(expected_requirements - set(contract_requirements))
        unknown = sorted(set(contract_requirements) - expected_requirements)
        failures.append(
            f"technical contract requirement inventory mismatch; missing={missing}, unknown={unknown}"
        )
    if set(contract_tests) != EXPECTED_TECHNICAL_TEST_IDS:
        missing = sorted(EXPECTED_TECHNICAL_TEST_IDS - set(contract_tests))
        unknown = sorted(set(contract_tests) - EXPECTED_TECHNICAL_TEST_IDS)
        failures.append(
            f"technical contract test inventory mismatch; missing={missing}, unknown={unknown}"
        )

    graph = exact_keys(
        graph,
        {"schemaVersion", "courseId", "contractPath", "requirements", "tests"},
        "technical requirement graph",
        failures,
    )
    if graph.get("schemaVersion") != "course1-technical-requirement-graph-v1":
        failures.append("technical requirement graph schemaVersion is unsupported")
    if graph.get("courseId") != EXPECTED_COURSE_ID:
        failures.append("technical requirement graph courseId is not Course 1")
    if graph.get("contractPath") != contract_path.name:
        failures.append("technical requirement graph contractPath is not authoritative")

    graph_requirement_rows = graph.get("requirements")
    graph_test_rows = graph.get("tests")
    if not isinstance(graph_requirement_rows, list):
        failures.append("technical requirement graph requirements must be an array")
        graph_requirement_rows = []
    if not isinstance(graph_test_rows, list):
        failures.append("technical requirement graph tests must be an array")
        graph_test_rows = []

    requirements_to_tests: dict[str, set[str]] = {}
    graph_requirement_ids: list[str] = []
    for index, raw in enumerate(graph_requirement_rows):
        row = exact_keys(
            raw,
            {"id", "family", "tests"},
            f"technical requirement graph requirements[{index}]",
            failures,
        )
        requirement_id = row.get("id")
        if not isinstance(requirement_id, str) or not TECHNICAL_REQUIREMENT_RE.fullmatch(
            requirement_id
        ):
            failures.append(
                f"technical requirement graph requirements[{index}].id is malformed"
            )
            continue
        graph_requirement_ids.append(requirement_id)
        family = TECHNICAL_REQUIREMENT_RE.fullmatch(requirement_id).group(1)
        if row.get("family") != family:
            failures.append(f"{requirement_id} family does not match its ID")
        test_ids = row.get("tests")
        if not isinstance(test_ids, list) or not test_ids:
            failures.append(f"{requirement_id} must map to at least one test")
            test_ids = []
        if any(not isinstance(item, str) or not TECHNICAL_TEST_RE.fullmatch(item) for item in test_ids):
            failures.append(f"{requirement_id} has a malformed test mapping")
        if len(test_ids) != len(set(item for item in test_ids if isinstance(item, str))):
            failures.append(f"{requirement_id} has duplicate test mappings")
        requirements_to_tests[requirement_id] = {
            item for item in test_ids if isinstance(item, str)
        }

    duplicate_requirement_ids = sorted(
        identifier
        for identifier, count in Counter(graph_requirement_ids).items()
        if count > 1
    )
    if duplicate_requirement_ids:
        failures.append(
            f"technical graph has duplicate requirement IDs: {duplicate_requirement_ids}"
        )
    if set(requirements_to_tests) != expected_requirements:
        failures.append(
            "technical graph requirement inventory does not exactly match the 118-ID contract"
        )

    tests_to_requirements: dict[str, set[str]] = {}
    graph_test_ids: list[str] = []
    for index, raw in enumerate(graph_test_rows):
        row = exact_keys(
            raw,
            {"id", "requirements"},
            f"technical requirement graph tests[{index}]",
            failures,
        )
        test_id = row.get("id")
        if not isinstance(test_id, str) or not TECHNICAL_TEST_RE.fullmatch(test_id):
            failures.append(
                f"technical requirement graph tests[{index}].id is malformed"
            )
            continue
        graph_test_ids.append(test_id)
        requirement_ids = row.get("requirements")
        if not isinstance(requirement_ids, list) or not requirement_ids:
            failures.append(f"{test_id} must map to at least one requirement")
            requirement_ids = []
        if any(
            not isinstance(item, str) or not TECHNICAL_REQUIREMENT_RE.fullmatch(item)
            for item in requirement_ids
        ):
            failures.append(f"{test_id} has a malformed requirement mapping")
        if len(requirement_ids) != len(
            set(item for item in requirement_ids if isinstance(item, str))
        ):
            failures.append(f"{test_id} has duplicate requirement mappings")
        tests_to_requirements[test_id] = {
            item for item in requirement_ids if isinstance(item, str)
        }

    duplicate_test_ids = sorted(
        identifier
        for identifier, count in Counter(graph_test_ids).items()
        if count > 1
    )
    if duplicate_test_ids:
        failures.append(f"technical graph has duplicate test IDs: {duplicate_test_ids}")
    if set(tests_to_requirements) != EXPECTED_TECHNICAL_TEST_IDS:
        failures.append(
            "technical graph test inventory does not exactly match the 33-ID contract"
        )

    derived_tests_to_requirements: dict[str, set[str]] = {
        test_id: set()
        for mapped_test_ids in requirements_to_tests.values()
        for test_id in mapped_test_ids
    }
    for requirement_id, test_ids in requirements_to_tests.items():
        for test_id in test_ids:
            derived_tests_to_requirements.setdefault(test_id, set()).add(requirement_id)
    if derived_tests_to_requirements != tests_to_requirements:
        failures.append(
            "technical graph requirement-to-test and test-to-requirement mappings disagree"
        )
    if contract_tests != tests_to_requirements:
        failures.append(
            "technical contract Section 14 mappings do not exactly match the technical graph"
        )
    for requirement_id, direct_tests in contract_requirements.items():
        unknown = sorted(direct_tests - EXPECTED_TECHNICAL_TEST_IDS)
        missing_reverse = sorted(
            test_id
            for test_id in direct_tests
            if requirement_id not in tests_to_requirements.get(test_id, set())
        )
        if unknown:
            failures.append(
                f"{requirement_id} references undeclared tests: {unknown}"
            )
        if missing_reverse:
            failures.append(
                f"{requirement_id} direct test references contradict the graph: {missing_reverse}"
            )

    manifest = exact_keys(
        manifest,
        {"schemaVersion", "courseId", "graphPath", "tests"},
        "technical test manifest",
        failures,
    )
    if manifest.get("schemaVersion") != "course1-technical-test-manifest-v1":
        failures.append("technical test manifest schemaVersion is unsupported")
    if manifest.get("courseId") != EXPECTED_COURSE_ID:
        failures.append("technical test manifest courseId is not Course 1")
    if manifest.get("graphPath") != graph_path.relative_to(root).as_posix():
        failures.append("technical test manifest graphPath is not authoritative")
    manifest_rows = manifest.get("tests")
    if not isinstance(manifest_rows, list):
        failures.append("technical test manifest tests must be an array")
        manifest_rows = []

    manifest_ids: list[str] = []
    evidence_paths: set[str] = set()
    raw_artifact_paths: set[str] = set()
    evidence_ids: set[str] = set()
    evidence_candidate: dict[str, Any] | None = None
    for index, raw in enumerate(manifest_rows):
        label = f"technical test manifest tests[{index}]"
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
            label,
            failures,
        )
        test_id = row.get("id")
        if not isinstance(test_id, str) or not TECHNICAL_TEST_RE.fullmatch(test_id):
            failures.append(f"{label}.id is malformed")
            continue
        manifest_ids.append(test_id)
        if row.get("type") not in {"executable", "manual", "hybrid"}:
            failures.append(f"{test_id}.type is unsupported")
        if not is_nonempty_string(row.get("owner")):
            failures.append(f"{test_id}.owner must be recorded")
        environments = row.get("environments")
        if (
            not isinstance(environments, list)
            or not environments
            or any(not is_nonempty_string(item) for item in environments)
            or len(environments) != len(set(item for item in environments if isinstance(item, str)))
        ):
            failures.append(f"{test_id}.environments must be non-empty and unique")
        evidence_class = row.get("evidenceClass")
        if evidence_class not in TECHNICAL_EVIDENCE_CLASSES:
            failures.append(f"{test_id}.evidenceClass is unsupported")

        procedures = row.get("procedures")
        procedure_bindings: set[tuple[str, str]] = set()
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
            for field in ("selector", "command", "expected"):
                if not is_nonempty_string(procedure.get(field)):
                    failures.append(f"{procedure_label}.{field} must be recorded")
            if (
                is_nonempty_string(procedure.get("locator"))
                and is_nonempty_string(procedure.get("selector"))
            ):
                binding = (
                    str(procedure["locator"]),
                    str(procedure["selector"]),
                )
                if binding in procedure_bindings:
                    failures.append(
                        f"{test_id}.procedures contain a duplicate locator/selector binding"
                    )
                procedure_bindings.add(binding)
            locator_path = safe_repository_file(
                root,
                procedure.get("locator"),
                label=f"{procedure_label}.locator",
                failures=failures,
            )
            if locator_path is not None and is_nonempty_string(procedure.get("selector")):
                try:
                    locator_text = locator_path.read_text(
                        encoding="utf-8",
                        errors="strict",
                    )
                except (OSError, UnicodeError) as exc:
                    failures.append(f"{procedure_label}.locator could not be read: {exc}")
                else:
                    if procedure["selector"] not in locator_text:
                        failures.append(
                            f"{procedure_label}.selector is absent from {procedure.get('locator')}"
                        )

        current = exact_keys(
            row.get("currentEvidence"),
            {"status", "records"},
            f"{test_id}.currentEvidence",
            failures,
        )
        status = current.get("status")
        records = current.get("records")
        if status not in {"UNVERIFIED", "PASS", "FAIL"}:
            failures.append(f"{test_id}.currentEvidence.status is unsupported")
        if not isinstance(records, list):
            failures.append(f"{test_id}.currentEvidence.records must be an array")
            records = []
        if status == "UNVERIFIED" and records:
            failures.append(f"{test_id} UNVERIFIED evidence must have no records")
        if status in {"PASS", "FAIL"} and not records:
            failures.append(f"{test_id} {status} evidence must have records")

        for record_index, raw_locator in enumerate(records):
            locator_label = f"{test_id}.currentEvidence.records[{record_index}]"
            locator = exact_keys(
                raw_locator,
                {"path", "sha256"},
                locator_label,
                failures,
            )
            evidence_path_text = locator.get("path")
            if evidence_path_text in evidence_paths:
                failures.append(f"duplicate technical evidence path: {evidence_path_text}")
            elif isinstance(evidence_path_text, str):
                evidence_paths.add(evidence_path_text)
            expected_hash = locator.get("sha256")
            if not isinstance(expected_hash, str) or not re.fullmatch(
                r"[0-9a-f]{64}", expected_hash
            ):
                failures.append(f"{locator_label}.sha256 must be lowercase SHA-256")
            evidence_path = safe_repository_file(
                root,
                evidence_path_text,
                label=f"{locator_label}.path",
                failures=failures,
                release_evidence_only=True,
            )
            if evidence_path is None:
                continue
            try:
                evidence_bytes = evidence_path.read_bytes()
            except OSError as exc:
                failures.append(f"{locator_label}.path could not be read: {exc}")
                continue
            actual_hash = hashlib.sha256(evidence_bytes).hexdigest()
            if expected_hash != actual_hash:
                failures.append(f"{locator_label}.sha256 does not match the evidence file")
            try:
                evidence_record = json.loads(
                    evidence_bytes.decode("utf-8"),
                    object_pairs_hook=reject_duplicate_json_keys,
                )
                if not isinstance(evidence_record, dict):
                    raise ValueError("top-level evidence JSON must be one object")
            except (UnicodeError, ValueError, json.JSONDecodeError) as exc:
                failures.append(f"{locator_label}.path is invalid JSON: {exc}")
                continue
            evidence_id, candidate = validate_technical_evidence_record(
                evidence_record,
                root=root,
                evidence_record_path=evidence_path,
                label=str(evidence_path.relative_to(root)),
                expected_test_id=test_id,
                expected_evidence_class=str(evidence_class),
                expected_result=str(status),
                expected_procedures=procedure_bindings,
                expected_environments={
                    str(environment)
                    for environment in environments
                    if is_nonempty_string(environment)
                },
                failures=failures,
                seen_artifact_paths=raw_artifact_paths,
            )
            if evidence_id is not None:
                if evidence_id in evidence_ids:
                    failures.append(f"duplicate technical evidenceId: {evidence_id}")
                evidence_ids.add(evidence_id)
            if candidate is not None:
                if evidence_candidate is None:
                    evidence_candidate = candidate
                elif evidence_candidate != candidate:
                    failures.append(
                        "technical evidence records are bound to different candidates"
                    )

    duplicate_manifest_ids = sorted(
        identifier
        for identifier, count in Counter(manifest_ids).items()
        if count > 1
    )
    if duplicate_manifest_ids:
        failures.append(
            f"technical test manifest has duplicate test IDs: {duplicate_manifest_ids}"
        )
    if set(manifest_ids) != EXPECTED_TECHNICAL_TEST_IDS:
        failures.append(
            "technical test manifest does not exactly cover all 33 declared tests"
        )

    try:
        import jsonschema  # type: ignore
    except (ModuleNotFoundError, ImportError):
        pass
    except Exception as exc:
        failures.append(f"jsonschema could not be imported for audit schemas: {exc}")
    else:
        schema_instances = (
            (schemas[0], graph, "technical requirement graph"),
            (schemas[1], manifest, "technical test manifest"),
        )
        for schema, instance, label in schema_instances:
            try:
                jsonschema.Draft202012Validator.check_schema(schema)
                jsonschema.Draft202012Validator(
                    schema,
                    format_checker=jsonschema.FormatChecker(),
                ).validate(instance)
            except Exception as exc:
                failures.append(f"{label} schema validation failed: {exc}")
        for path, schema in zip(schema_paths[2:], schemas[2:]):
            try:
                jsonschema.Draft202012Validator.check_schema(schema)
            except Exception as exc:
                failures.append(
                    f"{path.relative_to(root)} meta-validation failed: {exc}"
                )
    return failures


def validate_course1_technical_audit_control(root: Path, report: Report) -> None:
    failures = technical_audit_control_failures(root)
    if failures:
        report.failed(
            "course1-technical-audit-control",
            compact(failures, limit=30),
        )
        return
    graph = load_json_object(
        root / "audit_control/course1/technical_requirement_graph.json"
    )
    manifest = load_json_object(
        root / "audit_control/course1/technical_test_manifest.json"
    )
    edge_count = sum(len(row["tests"]) for row in graph["requirements"])
    unverified_count = sum(
        row["currentEvidence"]["status"] == "UNVERIFIED"
        for row in manifest["tests"]
    )
    report.passed(
        "course1-technical-audit-control",
        "118 requirements and 33 declared tests are bound bidirectionally "
        f"across {edge_count} edges; {unverified_count} candidate test results "
        "remain honestly UNVERIFIED",
    )


def learning_content_repair_failures(
    root: Path,
    *,
    text_overrides: dict[str, str] | None = None,
) -> list[str]:
    failures: list[str] = []
    overrides = text_overrides or {}

    def read(relative_path: str) -> str:
        if relative_path in overrides:
            return overrides[relative_path]
        path = root / relative_path
        if not path.is_file():
            failures.append(f"required learning-content file is missing: {relative_path}")
            return ""
        try:
            return path.read_text(encoding="utf-8", errors="strict")
        except (OSError, UnicodeError) as exc:
            failures.append(f"{relative_path} could not be read: {exc}")
            return ""

    for relative_path, expected_count in PREMODULE_STUDY_BLOCK_COUNTS.items():
        text = read(relative_path)
        heading_match = re.search(
            r"^## Study plan\b.*$",
            text,
            flags=re.MULTILINE,
        )
        if heading_match is None:
            failures.append(f"{relative_path} is missing its visible study plan")
            continue
        next_heading = re.search(
            r"^## (?!Study plan\b).+$",
            text[heading_match.end() :],
            flags=re.MULTILINE,
        )
        section_end = (
            heading_match.end() + next_heading.start()
            if next_heading is not None
            else len(text)
        )
        section = text[heading_match.start() : section_end]
        section_flat = " ".join(section.split())
        block_rows = re.findall(
            r"^\|\s*(\d+)\s*\|\s*(\d+)\s+minutes\s*\|",
            section,
            flags=re.MULTILINE,
        )
        if len(block_rows) != expected_count:
            failures.append(
                f"{relative_path} study plan has {len(block_rows)} blocks; "
                f"expected {expected_count}"
            )
        block_numbers = [int(number) for number, _ in block_rows]
        if block_numbers != list(range(1, expected_count + 1)):
            failures.append(
                f"{relative_path} study blocks are not numbered 1 through {expected_count}"
            )
        excessive = [
            f"block {number}={minutes}"
            for number, minutes in block_rows
            if int(minutes) > 60
        ]
        if excessive:
            failures.append(
                f"{relative_path} has a planned block over 60 minutes: {excessive}"
            )
        for required_phrase in (
            "AUTHOR ESTIMATE — NOT BEGINNER MEASURED",
            "60 focused minutes",
            "take a break",
            "Resume",
        ):
            if required_phrase.casefold() not in section_flat.casefold():
                failures.append(
                    f"{relative_path} study plan is missing: {required_phrase}"
                )

    note_files = (
        "README.md",
        "SETUP_WINDOWS.md",
        "modules/MODULE_01.md",
        "app/README.md",
        "COURSE_CHANGELOG.md",
    )
    for relative_path in note_files:
        text = read(relative_path)
        if re.search(r"\bprivate (?:course )?notes?\b", text, flags=re.IGNORECASE):
            failures.append(
                f"{relative_path} still describes shared-origin learner notes as private"
            )
    if (
        "not private from other applications served from the same website origin"
        not in " ".join(read("README.md").split())
    ):
        failures.append("README.md is missing the shared-origin note boundary")

    module_09 = read("modules/MODULE_09.md")
    module_09_flat = " ".join(module_09.split())
    if "# Worked UAT and handover" in module_09:
        failures.append("Module 9 still titles role simulation as Worked UAT")
    for phrase in (
        "# Worked role-simulated acceptance rehearsal and handover",
        "EXTERNAL UAT NOT VERIFIED",
        "participation is voluntary",
        "pause, skip a task, or stop at any time",
        "screen, audio, video, or quotations",
        "name who may access the structured record",
        "planned deletion date",
        "employment, medical, or professional evaluation",
        "invalidates the evidence",
        "weak, vague, or unsupported",
        "`I do not know`",
        "safe next step",
    ):
        if phrase not in module_09_flat:
            failures.append(f"modules/MODULE_09.md is missing: {phrase}")

    assessment = read("ASSESSMENT_AND_RUBRIC.md")
    assessment_flat = " ".join(assessment.split())
    for phrase in (
        "weak, vague, or",
        "`I do not know`",
        "safe next step",
        "requires separate explicit consent",
    ):
        if phrase not in assessment_flat:
            failures.append(f"ASSESSMENT_AND_RUBRIC.md is missing: {phrase}")

    uat_template = read("templates/uat_script.md")
    uat_template_flat = " ".join(uat_template.split())
    for phrase in (
        "# Role-Simulated Operational Acceptance Rehearsal and Candidate User Acceptance Test Record",
        "### Required participant briefing — complete before consent",
        "Voluntary choice explained",
        "Exact observations proposed",
        "Who may access the structured record",
        "Planned retention/deletion date",
        "participation is not employment, medical, or professional",
        "Screen recording proposed",
        "Audio recording proposed",
        "Video recording proposed",
        "Quotation proposed",
        "Missing consent",
        "invalidates the evidence",
    ):
        if phrase not in uat_template_flat:
            failures.append(f"templates/uat_script.md is missing: {phrase}")

    for number in range(1, 10):
        relative_path = f"modules/MODULE_{number:02d}.md"
        module = read(relative_path)
        if not re.search(
            r"AUTHOR\s+ESTIMATE\s+—\s+NOT\s+BEGINNER\s+MEASURED",
            module,
        ):
            failures.append(f"{relative_path} is missing its author-estimate label")

    app_source = read("app/src/app.js")
    for phrase in (
        "Practice — AUTHOR ESTIMATE, NOT BEGINNER MEASURED:",
        "AUTHOR ESTIMATE — NOT BEGINNER MEASURED:",
    ):
        if phrase not in app_source:
            failures.append(f"app/src/app.js is missing: {phrase}")

    if "Manual fallback Standard Operating Procedure (SOP)" not in read(
        "templates/runbook_and_fallback.md"
    ):
        failures.append(
            "templates/runbook_and_fallback.md does not expand Standard Operating Procedure"
        )
    if (
        "Recovery Time Objective (RTO) / Recovery Point Objective (RPO)"
        not in read("templates/runbook_and_fallback.md")
    ):
        failures.append(
            "templates/runbook_and_fallback.md does not expand RTO and RPO"
        )
    if "Accounts Payable (AP) list" not in read("templates/data_flow_avg_ai_act.md"):
        failures.append(
            "templates/data_flow_avg_ai_act.md does not expand the Accounts Payable list"
        )

    module_06 = read("modules/MODULE_06.md")
    hard_coded_test_counts = (
        r"`Ran \d+ tests?`",
        r"\$expectedCourseOneTests\s*=\s*\d+",
        r"exactly \d+ of \d+ expected tests",
        r"Exactly \d+ automated tests",
    )
    if any(
        re.search(pattern, module_06, flags=re.IGNORECASE)
        for pattern in hard_coded_test_counts
    ):
        failures.append(
            "modules/MODULE_06.md hard-codes the Course 1 automated test count"
        )
    for phrase in (
        r"course1_capstone\tests\test_manifest.json",
        "$expectedCourseOneTests = $declaredCourseOneTests.Count",
        "$testsRun -eq $expectedCourseOneTests",
        "manifest-declared automated test total",
    ):
        if phrase not in module_06:
            failures.append(
                "modules/MODULE_06.md does not bind learner acceptance to "
                f"the named-test manifest: {phrase}"
            )
    return failures


def validate_course1_learning_content_repairs(root: Path, report: Report) -> None:
    failures = learning_content_repair_failures(root)
    if failures:
        report.failed(
            "course1-learning-content-repair-contract",
            compact(failures, limit=30),
        )
        return
    report.passed(
        "course1-learning-content-repair-contract",
        "12 pre-module pages expose 69 separately numbered study blocks of at "
        "most 60 minutes; note privacy, role-simulated UAT, oral, consent, "
        "author-estimate, and optional abbreviation wording is structurally "
        "present (this does not prove human learning)",
    )


def parse_learning_contract(
    contract_text: str,
    failures: list[str],
) -> tuple[list[str], list[str]]:
    requirement_ids: list[str] = []
    for line_number, line in enumerate(contract_text.splitlines(), 1):
        if not line.startswith("###") or "C1-LV-" not in line:
            continue
        match = re.match(r"^### `(C1-LV-\d{3})`(?:\s|$)", line)
        if match is None:
            failures.append(
                f"learning contract line {line_number} has a malformed requirement heading"
            )
            continue
        requirement_ids.append(match.group(1))

    duplicate_requirements = sorted(
        identifier
        for identifier, count in Counter(requirement_ids).items()
        if count > 1
    )
    if duplicate_requirements:
        failures.append(
            f"learning contract has duplicate requirement headings: {duplicate_requirements}"
        )

    evidence_classes: list[str] = []
    start_marker = "## Evidence classes must remain separate"
    end_marker = "## Release and learner-result language"
    if start_marker not in contract_text or end_marker not in contract_text:
        failures.append("learning contract evidence-class table markers are missing")
    else:
        evidence_section = contract_text.split(start_marker, 1)[1].split(
            end_marker,
            1,
        )[0]
        for line in evidence_section.splitlines():
            cells = markdown_cells(line)
            if cells is None or not cells:
                continue
            match = re.fullmatch(r"`([A-Z][A-Z0-9_]+)`", cells[0])
            if match is not None:
                evidence_classes.append(match.group(1))

    duplicate_classes = sorted(
        identifier
        for identifier, count in Counter(evidence_classes).items()
        if count > 1
    )
    if duplicate_classes:
        failures.append(
            f"learning contract has duplicate evidence classes: {duplicate_classes}"
        )
    return requirement_ids, evidence_classes


def validate_learning_evidence_record(
    value: Any,
    *,
    label: str,
    expected_requirement_id: str | None,
    allowed_evidence_classes: set[str],
    allowed_method_ids: set[str],
    expected_overall_status: str | None,
    failures: list[str],
) -> tuple[
    str | None,
    dict[str, Any] | None,
    str | None,
    str | None,
]:
    record = exact_keys(
        value,
        {
            "schemaVersion",
            "evidenceId",
            "requirementId",
            "evidenceClass",
            "candidate",
            "recordedAt",
            "environment",
            "people",
            "task",
            "observations",
            "privacy",
            "limitation",
            "decision",
        },
        label,
        failures,
    )
    if record.get("schemaVersion") != "course1-learning-evidence-v1":
        failures.append(f"{label}.schemaVersion is unsupported")

    evidence_id = record.get("evidenceId")
    if not isinstance(evidence_id, str) or not re.fullmatch(
        r"C1-LV-EV-[A-Z0-9-]+-\d{3}",
        evidence_id,
    ):
        failures.append(f"{label}.evidenceId is malformed")
        evidence_id = None

    requirement_id = record.get("requirementId")
    if (
        not isinstance(requirement_id, str)
        or not LEARNING_REQUIREMENT_RE.fullmatch(requirement_id)
    ):
        failures.append(f"{label}.requirementId is malformed")
    elif expected_requirement_id is not None and requirement_id != expected_requirement_id:
        failures.append(
            f"{label}.requirementId does not match {expected_requirement_id}"
        )

    evidence_class = record.get("evidenceClass")
    if evidence_class not in LEARNING_EVIDENCE_CLASSES:
        failures.append(f"{label}.evidenceClass is unsupported")
        evidence_class = None
    elif evidence_class not in allowed_evidence_classes:
        failures.append(
            f"{label}.evidenceClass is not allowed for {expected_requirement_id}"
        )

    candidate = exact_keys(
        record.get("candidate"),
        {
            "commit",
            "courseVersion",
            "practiceRevision",
            "buildId",
            "contentHash",
        },
        f"{label}.candidate",
        failures,
    )
    if not re.fullmatch(r"[0-9a-f]{40}", str(candidate.get("commit", ""))):
        failures.append(f"{label}.candidate.commit must be a full Git SHA")
    if not SEMVER_RE.fullmatch(str(candidate.get("courseVersion", ""))):
        failures.append(f"{label}.candidate.courseVersion must use x.y.z")
    if (
        not isinstance(candidate.get("practiceRevision"), int)
        or isinstance(candidate.get("practiceRevision"), bool)
        or candidate.get("practiceRevision", 0) < 1
    ):
        failures.append(f"{label}.candidate.practiceRevision must be a positive integer")
    if not re.fullmatch(r"[0-9a-f]{12}", str(candidate.get("buildId", ""))):
        failures.append(f"{label}.candidate.buildId must be 12 lowercase hex")
    if not re.fullmatch(r"[0-9a-f]{64}", str(candidate.get("contentHash", ""))):
        failures.append(f"{label}.candidate.contentHash must be SHA-256")

    recorded_at = record.get("recordedAt")
    if not is_nonempty_string(recorded_at):
        failures.append(f"{label}.recordedAt must be an ISO 8601 timestamp")
    else:
        try:
            normalized = (
                recorded_at[:-1] + "+00:00"
                if str(recorded_at).endswith("Z")
                else str(recorded_at)
            )
            parsed = datetime.fromisoformat(normalized)
            if parsed.tzinfo is None:
                raise ValueError("timezone missing")
        except ValueError:
            failures.append(
                f"{label}.recordedAt must be a valid ISO 8601 timestamp with timezone"
            )

    environment = exact_keys(
        record.get("environment"),
        {
            "operatingSystem",
            "shellOrBrowser",
            "locale",
            "timezone",
            "context",
        },
        f"{label}.environment",
        failures,
    )
    for field in (
        "operatingSystem",
        "shellOrBrowser",
        "locale",
        "timezone",
        "context",
    ):
        if not is_nonempty_string(environment.get(field)):
            failures.append(f"{label}.environment.{field} must be recorded")

    people = record.get("people")
    if not isinstance(people, list) or not people:
        failures.append(f"{label}.people must be a non-empty array")
        people = []
    participant_codes: list[str] = []
    for index, raw_person in enumerate(people):
        person = exact_keys(
            raw_person,
            {
                "participantCode",
                "role",
                "relevantPriorExperience",
                "conflictOrAssistance",
            },
            f"{label}.people[{index}]",
            failures,
        )
        participant_code = person.get("participantCode")
        if not isinstance(participant_code, str) or not re.fullmatch(
            r"[A-Z0-9-]{3,40}",
            participant_code,
        ):
            failures.append(f"{label}.people[{index}].participantCode is malformed")
        else:
            participant_codes.append(participant_code)
        for field in ("role", "relevantPriorExperience", "conflictOrAssistance"):
            if not is_nonempty_string(person.get(field)):
                failures.append(f"{label}.people[{index}].{field} must be recorded")
    if len(participant_codes) != len(set(participant_codes)):
        failures.append(f"{label}.people has duplicate participant codes")

    task = exact_keys(
        record.get("task"),
        {"methodId", "predefinedTask", "passCriteria"},
        f"{label}.task",
        failures,
    )
    method_id = task.get("methodId")
    if not isinstance(method_id, str) or not re.fullmatch(
        r"C1-LVM-\d{3}",
        method_id,
    ):
        failures.append(f"{label}.task.methodId is malformed")
        method_id = None
    elif method_id not in allowed_method_ids:
        failures.append(f"{label}.task.methodId is not mapped to the requirement")
    for field in ("predefinedTask", "passCriteria"):
        if not is_nonempty_string(task.get(field)):
            failures.append(f"{label}.task.{field} must be recorded")

    observations = exact_keys(
        record.get("observations"),
        {"result", "help", "deviations", "defects", "retest"},
        f"{label}.observations",
        failures,
    )
    observation_result = observations.get("result")
    if observation_result not in {"PASS", "FAIL"}:
        failures.append(f"{label}.observations.result is unsupported")
    for field in ("help", "deviations", "defects", "retest"):
        if not is_nonempty_string(observations.get(field)):
            failures.append(f"{label}.observations.{field} must be recorded")

    privacy = exact_keys(
        record.get("privacy"),
        {
            "syntheticOnly",
            "purposeAndExpectedTimeStated",
            "voluntaryAndRightToStopStated",
            "observationScopeStated",
            "participationConsent",
            "recordingConsent",
            "accessStatement",
            "retentionDeletionDate",
            "nonEvaluationDisclaimerStated",
            "dataMinimisationStatement",
            "prohibitedDataFound",
        },
        f"{label}.privacy",
        failures,
    )
    for field in (
        "syntheticOnly",
        "purposeAndExpectedTimeStated",
        "voluntaryAndRightToStopStated",
        "observationScopeStated",
        "nonEvaluationDisclaimerStated",
        "prohibitedDataFound",
    ):
        if not isinstance(privacy.get(field), bool):
            failures.append(f"{label}.privacy.{field} must be boolean")
    if privacy.get("participationConsent") not in {"YES", "NO", "NOT APPLICABLE"}:
        failures.append(f"{label}.privacy.participationConsent is unsupported")
    if privacy.get("recordingConsent") not in {
        "NOT PROPOSED",
        "DECLINED",
        "GRANTED",
        "NOT APPLICABLE",
    }:
        failures.append(f"{label}.privacy.recordingConsent is unsupported")
    for field in ("accessStatement", "dataMinimisationStatement"):
        if not is_nonempty_string(privacy.get(field)):
            failures.append(f"{label}.privacy.{field} must be recorded")
    retention_date = privacy.get("retentionDeletionDate")
    if retention_date != "NOT APPLICABLE":
        try:
            date.fromisoformat(str(retention_date))
        except ValueError:
            failures.append(
                f"{label}.privacy.retentionDeletionDate must be YYYY-MM-DD or NOT APPLICABLE"
            )

    if evidence_class in HUMAN_TRIAL_EVIDENCE_CLASSES:
        human_requirements = {
            "syntheticOnly": True,
            "purposeAndExpectedTimeStated": True,
            "voluntaryAndRightToStopStated": True,
            "observationScopeStated": True,
            "participationConsent": "YES",
            "nonEvaluationDisclaimerStated": True,
            "prohibitedDataFound": False,
        }
        for field, expected in human_requirements.items():
            if privacy.get(field) != expected:
                failures.append(
                    f"{label}.privacy.{field} must be {expected!r} for human evidence"
                )
        if privacy.get("recordingConsent") == "NOT APPLICABLE":
            failures.append(
                f"{label}.privacy.recordingConsent must state the separate human choice"
            )
        if retention_date == "NOT APPLICABLE":
            failures.append(
                f"{label}.privacy.retentionDeletionDate is required for human evidence"
            )

    if not is_nonempty_string(record.get("limitation")):
        failures.append(f"{label}.limitation must be recorded")

    decision = exact_keys(
        record.get("decision"),
        {"status", "reviewerCode", "reviewerRole", "reason"},
        f"{label}.decision",
        failures,
    )
    decision_status = decision.get("status")
    if decision_status not in {"PASS", "FAIL"}:
        failures.append(f"{label}.decision.status is unsupported")
    reviewer_code = decision.get("reviewerCode")
    if not isinstance(reviewer_code, str) or not re.fullmatch(
        r"[A-Z0-9-]{3,40}",
        reviewer_code,
    ):
        failures.append(f"{label}.decision.reviewerCode is malformed")
    for field in ("reviewerRole", "reason"):
        if not is_nonempty_string(decision.get(field)):
            failures.append(f"{label}.decision.{field} must be recorded")

    if expected_overall_status in {"PASS", "FAIL"}:
        if observation_result != expected_overall_status:
            failures.append(
                f"{label}.observations.result does not match {expected_overall_status}"
            )
        if decision_status != expected_overall_status:
            failures.append(
                f"{label}.decision.status does not match {expected_overall_status}"
            )

    return evidence_id, candidate or None, evidence_class, method_id


def learning_audit_control_failures(
    root: Path,
    *,
    contract_text: str | None = None,
    matrix: dict[str, Any] | None = None,
    template: dict[str, Any] | None = None,
) -> list[str]:
    failures: list[str] = []
    contract_path = root / "COURSE_1_LEARNING_VALIDATION_CONTRACT.md"
    matrix_path = root / "audit_control/course1/learning_claim_evidence_matrix.json"
    matrix_schema_path = (
        root / "audit_control/course1/learning_claim_evidence_matrix.schema.json"
    )
    evidence_schema_path = (
        root / "audit_control/course1/learning_evidence_record.schema.json"
    )
    template_path = (
        root
        / "release_evidence/templates/COURSE_1_LEARNING_EVIDENCE_RECORD.template.json"
    )
    evidence_root = root / "release_evidence/course1_learning_validation"
    required_paths = (
        contract_path,
        matrix_path,
        matrix_schema_path,
        evidence_schema_path,
        template_path,
    )
    for path in required_paths:
        if not path.is_file():
            failures.append(
                f"required learning audit-control file is missing: {path.relative_to(root)}"
            )
    if not evidence_root.is_dir():
        failures.append(
            "required learning evidence root is missing: "
            "release_evidence/course1_learning_validation"
        )
    if failures:
        return failures

    try:
        if contract_text is None:
            contract_text = contract_path.read_text(encoding="utf-8")
        if matrix is None:
            matrix = load_json_object(matrix_path)
        if template is None:
            template = load_json_object(template_path)
        matrix_schema = load_json_object(matrix_schema_path)
        evidence_schema = load_json_object(evidence_schema_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"could not load learning audit control: {exc}"]

    contract_requirement_ids, contract_evidence_classes = parse_learning_contract(
        contract_text,
        failures,
    )
    if contract_requirement_ids != list(EXPECTED_LEARNING_REQUIREMENT_IDS):
        failures.append(
            "learning contract requirement inventory/order does not exactly match C1-LV-001 through C1-LV-017"
        )
    if set(contract_evidence_classes) != LEARNING_EVIDENCE_CLASSES:
        failures.append(
            "learning contract evidence-class inventory does not exactly match the closed 10-class vocabulary"
        )

    matrix = exact_keys(
        matrix,
        {
            "schemaVersion",
            "courseId",
            "contractPath",
            "evidenceRecordSchemaPath",
            "evidenceRecordTemplatePath",
            "releaseEvidenceRoot",
            "requirements",
        },
        "learning claim/evidence matrix",
        failures,
    )
    expected_metadata = {
        "schemaVersion": "course1-learning-claim-evidence-matrix-v1",
        "courseId": EXPECTED_COURSE_ID,
        "contractPath": contract_path.name,
        "evidenceRecordSchemaPath": evidence_schema_path.relative_to(root).as_posix(),
        "evidenceRecordTemplatePath": template_path.relative_to(root).as_posix(),
        "releaseEvidenceRoot": "release_evidence/course1_learning_validation",
    }
    for field, expected in expected_metadata.items():
        if matrix.get(field) != expected:
            failures.append(f"learning claim/evidence matrix {field} is not authoritative")

    rows = matrix.get("requirements")
    if not isinstance(rows, list):
        failures.append("learning claim/evidence matrix requirements must be an array")
        rows = []

    row_ids: list[str] = []
    method_ids: list[str] = []
    evidence_paths: set[str] = set()
    evidence_ids: set[str] = set()
    evidence_candidate: dict[str, Any] | None = None
    for index, raw_row in enumerate(rows):
        label = f"learning claim/evidence matrix requirements[{index}]"
        row = exact_keys(
            raw_row,
            {
                "requirementId",
                "owner",
                "observableCapability",
                "claim",
                "evidenceClasses",
                "assessmentMethods",
                "limitation",
                "laterBoundary",
                "currentEvidence",
                "learningDecision",
            },
            label,
            failures,
        )
        requirement_id = row.get("requirementId")
        if (
            not isinstance(requirement_id, str)
            or not LEARNING_REQUIREMENT_RE.fullmatch(requirement_id)
        ):
            failures.append(f"{label}.requirementId is malformed")
            continue
        row_ids.append(requirement_id)

        for field in (
            "owner",
            "observableCapability",
            "claim",
            "limitation",
            "laterBoundary",
        ):
            if not is_nonempty_string(row.get(field)):
                failures.append(f"{requirement_id}.{field} must be recorded")

        evidence_classes = row.get("evidenceClasses")
        if not isinstance(evidence_classes, list) or not evidence_classes:
            failures.append(
                f"{requirement_id}.evidenceClasses must be a non-empty array"
            )
            evidence_classes = []
        if any(item not in LEARNING_EVIDENCE_CLASSES for item in evidence_classes):
            failures.append(f"{requirement_id} has an unsupported evidence class")
        if len(evidence_classes) != len(set(evidence_classes)):
            failures.append(f"{requirement_id} has duplicate evidence classes")
        evidence_class_set = {
            item for item in evidence_classes if item in LEARNING_EVIDENCE_CLASSES
        }

        methods = row.get("assessmentMethods")
        if not isinstance(methods, list) or not methods:
            failures.append(
                f"{requirement_id}.assessmentMethods must be a non-empty array"
            )
            methods = []
        row_method_ids: set[str] = set()
        for method_index, raw_method in enumerate(methods):
            method_label = f"{requirement_id}.assessmentMethods[{method_index}]"
            method = exact_keys(
                raw_method,
                {
                    "methodId",
                    "type",
                    "locator",
                    "selector",
                    "environment",
                    "passCondition",
                },
                method_label,
                failures,
            )
            method_id = method.get("methodId")
            if not isinstance(method_id, str) or not re.fullmatch(
                r"C1-LVM-\d{3}",
                method_id,
            ):
                failures.append(f"{method_label}.methodId is malformed")
            else:
                method_ids.append(method_id)
                row_method_ids.add(method_id)
            if method.get("type") not in {"automated", "manual", "hybrid"}:
                failures.append(f"{method_label}.type is unsupported")
            for field in ("selector", "environment", "passCondition"):
                if not is_nonempty_string(method.get(field)):
                    failures.append(f"{method_label}.{field} must be recorded")
            locator_path = safe_repository_file(
                root,
                method.get("locator"),
                label=f"{method_label}.locator",
                failures=failures,
            )
            if locator_path is not None and is_nonempty_string(method.get("selector")):
                try:
                    locator_text = locator_path.read_text(
                        encoding="utf-8",
                        errors="strict",
                    )
                except (OSError, UnicodeError) as exc:
                    failures.append(f"{method_label}.locator could not be read: {exc}")
                else:
                    if method["selector"] not in locator_text:
                        failures.append(
                            f"{method_label}.selector is absent from {method.get('locator')}"
                        )

        current = exact_keys(
            row.get("currentEvidence"),
            {"status", "records"},
            f"{requirement_id}.currentEvidence",
            failures,
        )
        current_status = current.get("status")
        records = current.get("records")
        if current_status not in {"UNVERIFIED", "PASS", "FAIL"}:
            failures.append(f"{requirement_id}.currentEvidence.status is unsupported")
        if not isinstance(records, list):
            failures.append(
                f"{requirement_id}.currentEvidence.records must be an array"
            )
            records = []
        if current_status == "UNVERIFIED" and records:
            failures.append(
                f"{requirement_id} UNVERIFIED evidence must have no records"
            )
        if current_status in {"PASS", "FAIL"} and not records:
            failures.append(
                f"{requirement_id} {current_status} evidence must have records"
            )

        decision = exact_keys(
            row.get("learningDecision"),
            {"status", "reason"},
            f"{requirement_id}.learningDecision",
            failures,
        )
        decision_status = decision.get("status")
        if decision_status not in {"PASS", "NOT YET", "NOT APPLICABLE"}:
            failures.append(f"{requirement_id}.learningDecision.status is unsupported")
        if not is_nonempty_string(decision.get("reason")):
            failures.append(f"{requirement_id}.learningDecision.reason must be recorded")
        if current_status == "PASS" and decision_status != "PASS":
            failures.append(f"{requirement_id} PASS evidence requires a PASS decision")
        if current_status in {"UNVERIFIED", "FAIL"} and decision_status != "NOT YET":
            failures.append(
                f"{requirement_id} {current_status} evidence requires a NOT YET decision"
            )
        if decision_status == "NOT APPLICABLE" and "contract" not in str(
            decision.get("reason", "")
        ).casefold():
            failures.append(
                f"{requirement_id} NOT APPLICABLE requires a contract-supported reason"
            )

        covered_classes: set[str] = set()
        for record_index, raw_locator in enumerate(records):
            locator_label = (
                f"{requirement_id}.currentEvidence.records[{record_index}]"
            )
            locator = exact_keys(
                raw_locator,
                {"path", "sha256"},
                locator_label,
                failures,
            )
            evidence_path_text = locator.get("path")
            if evidence_path_text in evidence_paths:
                failures.append(f"duplicate learning evidence path: {evidence_path_text}")
            elif isinstance(evidence_path_text, str):
                evidence_paths.add(evidence_path_text)
            expected_hash = locator.get("sha256")
            if not isinstance(expected_hash, str) or not re.fullmatch(
                r"[0-9a-f]{64}",
                expected_hash,
            ):
                failures.append(f"{locator_label}.sha256 must be lowercase SHA-256")

            pure = (
                PurePosixPath(evidence_path_text)
                if isinstance(evidence_path_text, str)
                else PurePosixPath("")
            )
            if (
                len(pure.parts) < 4
                or pure.parts[:2]
                != ("release_evidence", "course1_learning_validation")
                or not SEMVER_RE.fullmatch(pure.parts[2])
                or pure.suffix.casefold() != ".json"
            ):
                failures.append(
                    f"{locator_label}.path must be versioned JSON under release_evidence/course1_learning_validation/"
                )
            evidence_path = safe_repository_file(
                root,
                evidence_path_text,
                label=f"{locator_label}.path",
                failures=failures,
                release_evidence_only=True,
            )
            if evidence_path is None:
                continue
            try:
                evidence_bytes = evidence_path.read_bytes()
            except OSError as exc:
                failures.append(f"{locator_label}.path could not be read: {exc}")
                continue
            actual_hash = hashlib.sha256(evidence_bytes).hexdigest()
            if expected_hash != actual_hash:
                failures.append(
                    f"{locator_label}.sha256 does not match the evidence file"
                )
            try:
                evidence_record = json.loads(
                    evidence_bytes.decode("utf-8"),
                    object_pairs_hook=reject_duplicate_json_keys,
                )
                if not isinstance(evidence_record, dict):
                    raise ValueError("top-level evidence JSON must be one object")
            except (UnicodeError, ValueError, json.JSONDecodeError) as exc:
                failures.append(f"{locator_label}.path is invalid JSON: {exc}")
                continue

            evidence_id, candidate, record_class, _ = (
                validate_learning_evidence_record(
                    evidence_record,
                    label=str(evidence_path.relative_to(root)),
                    expected_requirement_id=requirement_id,
                    allowed_evidence_classes=evidence_class_set,
                    allowed_method_ids=row_method_ids,
                    expected_overall_status=current_status,
                    failures=failures,
                )
            )
            if evidence_id is not None:
                if evidence_id in evidence_ids:
                    failures.append(f"duplicate learning evidenceId: {evidence_id}")
                evidence_ids.add(evidence_id)
            if record_class is not None:
                covered_classes.add(record_class)
            if candidate is not None:
                if len(pure.parts) >= 3 and pure.parts[2] != candidate.get(
                    "courseVersion"
                ):
                    failures.append(
                        f"{locator_label}.path version does not match candidate courseVersion"
                    )
                if evidence_candidate is None:
                    evidence_candidate = candidate
                elif evidence_candidate != candidate:
                    failures.append(
                        "learning evidence records are bound to different candidates"
                    )

        if current_status == "PASS" and covered_classes != evidence_class_set:
            missing_classes = sorted(evidence_class_set - covered_classes)
            unknown_classes = sorted(covered_classes - evidence_class_set)
            failures.append(
                f"{requirement_id} PASS evidence-class coverage mismatch; "
                f"missing={missing_classes}, unknown={unknown_classes}"
            )

    duplicate_row_ids = sorted(
        identifier
        for identifier, count in Counter(row_ids).items()
        if count > 1
    )
    if duplicate_row_ids:
        failures.append(
            f"learning claim/evidence matrix has duplicate requirement IDs: {duplicate_row_ids}"
        )
    if row_ids != list(EXPECTED_LEARNING_REQUIREMENT_IDS):
        failures.append(
            "learning claim/evidence matrix does not exactly cover C1-LV-001 through C1-LV-017 in order"
        )

    duplicate_method_ids = sorted(
        identifier
        for identifier, count in Counter(method_ids).items()
        if count > 1
    )
    if duplicate_method_ids:
        failures.append(
            f"learning claim/evidence matrix has duplicate method IDs: {duplicate_method_ids}"
        )
    if set(method_ids) != EXPECTED_LEARNING_METHOD_IDS:
        failures.append(
            "learning claim/evidence matrix does not exactly cover C1-LVM-001 through C1-LVM-017"
        )

    template_failures: list[str] = []
    template_id, _, _, _ = validate_learning_evidence_record(
        template,
        label=str(template_path.relative_to(root)),
        expected_requirement_id="C1-LV-001",
        allowed_evidence_classes=LEARNING_EVIDENCE_CLASSES,
        allowed_method_ids=EXPECTED_LEARNING_METHOD_IDS,
        expected_overall_status=None,
        failures=template_failures,
    )
    if template_id != "C1-LV-EV-TEMPLATE-000":
        template_failures.append("learning evidence template evidenceId is not the fixed template marker")
    failures.extend(template_failures)

    try:
        import jsonschema  # type: ignore
    except (ModuleNotFoundError, ImportError):
        pass
    except Exception as exc:
        failures.append(f"jsonschema could not be imported for learning schemas: {exc}")
    else:
        for schema, instance, label in (
            (matrix_schema, matrix, "learning claim/evidence matrix"),
            (evidence_schema, template, "learning evidence record template"),
        ):
            try:
                jsonschema.Draft202012Validator.check_schema(schema)
                jsonschema.Draft202012Validator(
                    schema,
                    format_checker=jsonschema.FormatChecker(),
                ).validate(instance)
            except Exception as exc:
                failures.append(f"{label} schema validation failed: {exc}")
    return failures


def validate_course1_learning_audit_control(root: Path, report: Report) -> None:
    failures = learning_audit_control_failures(root)
    if failures:
        report.failed(
            "course1-learning-audit-control",
            compact(failures, limit=30),
        )
        return
    matrix = load_json_object(
        root / "audit_control/course1/learning_claim_evidence_matrix.json"
    )
    unverified_count = sum(
        row["currentEvidence"]["status"] == "UNVERIFIED"
        for row in matrix["requirements"]
    )
    report.passed(
        "course1-learning-audit-control",
        "17 stable learning requirements and 17 assessment methods are closed, "
        f"mapped, and fail-closed; {unverified_count} candidate learning results "
        "remain honestly UNVERIFIED and NOT YET",
    )


def validate_json_schemas(root: Path, report: Report) -> None:
    schema_directory = root / "schemas"
    schema_paths = sorted(schema_directory.glob("*.schema.json"))
    names = {path.name for path in schema_paths}
    missing = sorted(EXPECTED_SCHEMA_FILES - names)
    if missing:
        report.failed("schema-set", f"missing current schemas: {missing}")
    else:
        report.passed(
            "schema-set",
            f"{len(schema_paths)} current schema files include all required Course 1 contracts",
        )

    structural_failures: list[str] = []
    schemas: list[tuple[Path, dict[str, Any]]] = []
    schema_ids: list[str] = []
    for path in schema_paths:
        try:
            schema = load_json_object(path)
        except Exception as exc:
            structural_failures.append(f"{path.name}: {exc}")
            continue
        schemas.append((path, schema))
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            structural_failures.append(
                f"{path.name}: $schema must identify Draft 2020-12"
            )
        schema_id = schema.get("$id")
        if not is_nonempty_string(schema_id):
            structural_failures.append(f"{path.name}: $id is missing")
        else:
            schema_ids.append(schema_id)
        if not is_nonempty_string(schema.get("title")):
            structural_failures.append(f"{path.name}: title is missing")
        if schema.get("type") != "object":
            structural_failures.append(f"{path.name}: top-level type must be object")
        if schema.get("additionalProperties") is not False:
            structural_failures.append(
                f"{path.name}: additionalProperties must be false"
            )
        properties = schema.get("properties")
        required = schema.get("required")
        if not isinstance(properties, dict) or not properties:
            structural_failures.append(f"{path.name}: properties must be non-empty")
        if not isinstance(required, list) or not all(
            isinstance(item, str) for item in required
        ):
            structural_failures.append(
                f"{path.name}: required must be an array of strings"
            )
        elif isinstance(properties, dict):
            unknown_required = sorted(set(required) - set(properties))
            if unknown_required:
                structural_failures.append(
                    f"{path.name}: required fields absent from properties {unknown_required}"
                )

    duplicate_schema_ids = sorted(
        schema_id
        for schema_id, count in Counter(schema_ids).items()
        if count > 1
    )
    if duplicate_schema_ids:
        structural_failures.append(
            f"duplicate schema IDs: {duplicate_schema_ids}"
        )

    if structural_failures:
        report.failed("schema-structure", compact(structural_failures))
    else:
        report.passed(
            "schema-structure",
            f"{len(schemas)} schemas have unique IDs and closed object contracts",
        )

    try:
        import jsonschema  # type: ignore
    except ModuleNotFoundError:
        report.warn(
            "schema-meta-validation",
            "jsonschema is not installed; standard-library schema structure checks passed, but Draft 2020-12 meta-validation was not run",
        )
    except Exception as exc:
        report.warn(
            "schema-meta-validation",
            f"jsonschema could not be imported: {exc}",
        )
    else:
        meta_failures: list[str] = []
        for path, schema in schemas:
            try:
                jsonschema.Draft202012Validator.check_schema(schema)
            except Exception as exc:
                meta_failures.append(f"{path.name}: {exc}")
        if meta_failures:
            report.failed("schema-meta-validation", compact(meta_failures))
        else:
            report.passed(
                "schema-meta-validation",
                f"jsonschema accepted all {len(schemas)} schemas as Draft 2020-12",
            )


def validate_optional_yaml(root: Path, report: Report) -> None:
    path = root / "stack-manifest.yaml"
    if not path.is_file():
        report.warn("yaml-parse", "stack-manifest.yaml is not present")
        return
    try:
        import yaml  # type: ignore
    except ModuleNotFoundError:
        report.warn(
            "yaml-parse",
            "PyYAML is not installed; stack-manifest.yaml was not parsed",
        )
    except Exception as exc:
        report.warn("yaml-parse", f"PyYAML could not be imported: {exc}")
    else:
        try:
            value = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(value, dict):
                raise ValueError("top-level YAML value is not a mapping")
        except Exception as exc:
            report.failed("yaml-parse", str(exc))
        else:
            report.passed("yaml-parse", "stack-manifest.yaml parsed as a mapping")


def load_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        headers = list(reader.fieldnames or [])
        rows: list[dict[str, str]] = []
        for row_number, row in enumerate(reader, 2):
            if None in row:
                raise ValueError(
                    f"row {row_number} has more values than the header"
                )
            normalized: dict[str, str] = {}
            for key, value in row.items():
                normalized[key] = "" if value is None else value
            rows.append(normalized)
    return headers, rows


def blank(value: str) -> bool:
    return value.strip() == ""


def parse_iso_date(value: str) -> date | None:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return None
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        return None
    return parsed if parsed.isoformat() == value else None


def parse_decimal(value: str) -> Decimal | None:
    try:
        parsed = Decimal(value)
    except (InvalidOperation, ValueError):
        return None
    return parsed if parsed.is_finite() else None


def computed_practice_issues(
    rows: list[dict[str, str]]
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    parsed_dates_by_item: dict[str, dict[str, date | None]] = {}

    def add(
        row: dict[str, str],
        field_name: str,
        rule_code: str,
        severity: str,
        message: str,
    ) -> None:
        issues.append(
            {
                "work_item_id": row["work_item_id"],
                "field": field_name,
                "rule_code": rule_code,
                "severity": severity,
                "expected_message": message,
            }
        )

    for row in rows:
        for field_name in REQUIRED_VALUE_FIELDS:
            if blank(row[field_name]):
                add(
                    row,
                    field_name,
                    "R001",
                    "medium",
                    f"Required {field_name} is missing.",
                )

        status = row["status"].strip()
        priority = row["priority"].strip()
        if status not in ALLOWED_STATUSES:
            add(
                row,
                "status",
                "R002",
                "high",
                "Status is not in the allowed list.",
            )
        if priority not in ALLOWED_PRIORITIES:
            add(
                row,
                "priority",
                "R003",
                "medium",
                "Priority is not in the allowed list.",
            )

        parsed_dates: dict[str, date | None] = {}
        for field_name in DATE_FIELDS:
            value = row[field_name].strip()
            parsed = parse_iso_date(value) if value else None
            parsed_dates[field_name] = parsed
            if value and parsed is None:
                add(
                    row,
                    field_name,
                    "R004",
                    "high",
                    "Date must use ISO format YYYY-MM-DD.",
                )
        parsed_dates_by_item[row["work_item_id"]] = parsed_dates

        received = parsed_dates["received_date"]
        due = parsed_dates["due_date"]
        if received is not None and due is not None and due < received:
            add(
                row,
                "due_date",
                "R005",
                "high",
                "Due date is before received date.",
            )

        completion_value = row["completed_date"].strip()
        if status == "completed" and not completion_value:
            add(
                row,
                "completed_date",
                "R006",
                "high",
                "Completed work requires a completion date.",
            )
        elif status in (ALLOWED_STATUSES - {"completed"}) and completion_value:
            add(
                row,
                "completed_date",
                "R006",
                "medium",
                "Non-completed work must not have a completion date.",
            )

        if status in OWNER_REQUIRED_STATUSES and blank(row["owner_role"]):
            add(
                row,
                "owner_role",
                "R007",
                "medium",
                "Active work requires an owner role.",
            )

        amount_value = row["amount"].strip()
        currency_value = row["currency"].strip()
        if amount_value:
            parsed_amount = parse_decimal(amount_value)
            if parsed_amount is None or parsed_amount < 0:
                add(
                    row,
                    "amount",
                    "R008",
                    "high",
                    "Amount must not be negative.",
                )
            if currency_value != "EUR":
                add(
                    row,
                    "currency",
                    "R009",
                    "medium",
                    "A populated amount requires currency EUR.",
                )
        elif currency_value:
            add(
                row,
                "currency",
                "R009",
                "medium",
                "Currency must be blank when amount is blank.",
            )

    reference_counts = Counter(
        row["source_reference"].strip()
        for row in rows
        if row["source_reference"].strip()
    )
    for row in rows:
        reference = row["source_reference"].strip()
        if reference and reference_counts[reference] > 1:
            add(
                row,
                "source_reference",
                "R010",
                "high",
                f"Source reference {reference} is duplicated.",
            )

    for row in rows:
        status = row["status"].strip()
        due = parsed_dates_by_item[row["work_item_id"]]["due_date"]
        if (
            status in OPEN_STATUSES
            and due is not None
            and due < FIXED_ASSESSMENT_DATE
        ):
            add(
                row,
                "due_date",
                "R011",
                "high",
                "Open work is overdue on the fixed assessment date.",
            )

    return issues


def validate_practice_data(root: Path, report: Report) -> None:
    directory = root / "practice_data"
    readme_path = directory / "README.md"
    work_path = directory / "work_items.csv"
    expected_path = directory / "expected_issues.csv"
    missing = [
        path.relative_to(root).as_posix()
        for path in (readme_path, work_path, expected_path)
        if not path.is_file()
    ]
    if missing:
        report.failed("practice-files", f"missing: {missing}")
        return
    report.passed(
        "practice-files",
        "practice README, work_items.csv, and expected_issues.csv are present",
    )

    try:
        work_headers, work_rows = load_csv_rows(work_path)
        issue_headers, expected_rows = load_csv_rows(expected_path)
    except Exception as exc:
        report.failed("practice-csv-parse", str(exc))
        return

    shape_failures: list[str] = []
    if tuple(work_headers) != WORK_ITEM_FIELDS:
        shape_failures.append(
            f"work-item headers differ: expected {WORK_ITEM_FIELDS}; found {tuple(work_headers)}"
        )
    if tuple(issue_headers) != EXPECTED_ISSUE_FIELDS:
        shape_failures.append(
            f"expected-issue headers differ: expected {EXPECTED_ISSUE_FIELDS}; found {tuple(issue_headers)}"
        )
    if len(work_rows) != 15:
        shape_failures.append(f"work_items.csv must have 15 rows; found {len(work_rows)}")
    if len(expected_rows) != 13:
        shape_failures.append(
            f"expected_issues.csv must have 13 rows; found {len(expected_rows)}"
        )
    if shape_failures:
        report.failed("practice-shape", compact(shape_failures))
    else:
        report.passed(
            "practice-shape",
            "12 work-item columns / 15 rows and 6 issue columns / 13 rows",
        )

    key_failures: list[str] = []
    work_item_ids = [row.get("work_item_id", "") for row in work_rows]
    expected_work_item_ids = [f"WI-{number:04d}" for number in range(1, 16)]
    if work_item_ids != expected_work_item_ids:
        key_failures.append(
            f"work item IDs must be ordered WI-0001..WI-0015; found {work_item_ids}"
        )
    if len(work_item_ids) != len(set(work_item_ids)):
        key_failures.append("work_item_id values are not unique")

    issue_ids = [row.get("issue_id", "") for row in expected_rows]
    expected_issue_ids = [
        f"{row.get('work_item_id', '')}|{row.get('rule_code', '')}|{row.get('field', '')}"
        for row in expected_rows
    ]
    if issue_ids != expected_issue_ids:
        key_failures.append(
            "issue_id must equal work_item_id|rule_code|field on every gold row"
        )
    if len(issue_ids) != len(set(issue_ids)):
        key_failures.append("issue_id values are not unique")

    comparison_keys = [
        (
            row.get("work_item_id", ""),
            row.get("rule_code", ""),
            row.get("field", ""),
        )
        for row in expected_rows
    ]
    if len(comparison_keys) != len(set(comparison_keys)):
        key_failures.append(
            "(work_item_id, rule_code, field) expected-issue keys are not unique"
        )

    known_work_items = set(work_item_ids)
    for row in expected_rows:
        if row.get("work_item_id") not in known_work_items:
            key_failures.append(
                f"{row.get('issue_id')} references unknown {row.get('work_item_id')}"
            )
        if row.get("field") not in WORK_ITEM_FIELDS:
            key_failures.append(
                f"{row.get('issue_id')} references unknown field {row.get('field')}"
            )
        if row.get("severity") not in ALLOWED_SEVERITIES:
            key_failures.append(
                f"{row.get('issue_id')} has invalid severity {row.get('severity')}"
            )
        if not is_nonempty_string(row.get("expected_message")):
            key_failures.append(
                f"{row.get('issue_id')} has no expected message"
            )

    if key_failures:
        report.failed("practice-unique-keys", compact(key_failures))
    else:
        report.passed(
            "practice-unique-keys",
            "work-item IDs, issue IDs, and expected comparison keys are unique and referentially valid",
        )

    rule_failures: list[str] = []
    actual_rule_codes = {row.get("rule_code", "") for row in expected_rows}
    if actual_rule_codes != RULE_CODES:
        rule_failures.append(
            f"expected issues must cover R001-R011; found {sorted(actual_rule_codes)}"
        )
    readme = readme_path.read_text(encoding="utf-8")
    readme_rule_codes = re.findall(r"^\|\s*(R\d{3})\s*\|", readme, re.MULTILINE)
    if set(readme_rule_codes) != RULE_CODES:
        rule_failures.append(
            f"README rule register must contain R001-R011; found {sorted(set(readme_rule_codes))}"
        )
    duplicated_readme_rules = sorted(
        code for code, count in Counter(readme_rule_codes).items() if count != 1
    )
    if duplicated_readme_rules:
        rule_failures.append(
            f"README rule codes must appear once in the table: {duplicated_readme_rules}"
        )
    if FIXED_ASSESSMENT_DATE_TEXT not in readme:
        rule_failures.append(
            f"README does not state fixed assessment date {FIXED_ASSESSMENT_DATE_TEXT}"
        )

    if rule_failures:
        report.failed("practice-rule-register", compact(rule_failures))
    else:
        report.passed(
            "practice-rule-register",
            f"R001-R011 are documented and covered using fixed date {FIXED_ASSESSMENT_DATE_TEXT}",
        )

    safety_failures: list[str] = []
    lower_readme = " ".join(readme.lower().split())
    required_safety_statements = (
        "every row is fictional",
        "do not describe a real person, employer, customer, or transaction",
        "do not replace these files with workplace or customer exports",
    )
    for statement in required_safety_statements:
        if statement not in lower_readme:
            safety_failures.append(f"README lacks safety statement: {statement}")

    sensitive_headers = {
        "name",
        "email",
        "phone",
        "address",
        "bsn",
        "patient",
        "diagnosis",
        "employee",
        "birth_date",
    }
    present_sensitive_headers = sorted(sensitive_headers & set(work_headers))
    if present_sensitive_headers:
        safety_failures.append(
            f"unexpected personal/sensitive columns: {present_sensitive_headers}"
        )

    for row in work_rows:
        if not WORK_ITEM_ID_RE.fullmatch(row.get("work_item_id", "")):
            safety_failures.append(
                f"non-synthetic work-item identifier {row.get('work_item_id')!r}"
            )
        reference = row.get("source_reference", "")
        if reference and not SOURCE_REFERENCE_RE.fullmatch(reference):
            safety_failures.append(
                f"non-synthetic source reference {reference!r}"
            )
        owner_role = row.get("owner_role", "")
        if owner_role and not re.fullmatch(r"[a-z][a-z0-9_]*", owner_role):
            safety_failures.append(
                f"owner_role must remain a role token, not a name: {owner_role!r}"
            )

    if safety_failures:
        report.failed("practice-synthetic-safety", compact(safety_failures))
    else:
        report.passed(
            "practice-synthetic-safety",
            "fixed fictional identifiers, role-only ownership, no personal-data columns, and explicit no-real-data guarantees",
        )

    if not shape_failures:
        computed = computed_practice_issues(work_rows)
        tuple_fields = (
            "work_item_id",
            "field",
            "rule_code",
            "severity",
            "expected_message",
        )
        computed_set = {
            tuple(row[field_name] for field_name in tuple_fields)
            for row in computed
        }
        expected_set = {
            tuple(row[field_name] for field_name in tuple_fields)
            for row in expected_rows
        }
        oracle_failures: list[str] = []
        missing_expected = sorted(computed_set - expected_set)
        unexpected_expected = sorted(expected_set - computed_set)
        if missing_expected:
            oracle_failures.append(
                f"computed issues absent from answer key: {missing_expected}"
            )
        if unexpected_expected:
            oracle_failures.append(
                f"answer-key issues not reproduced by rules: {unexpected_expected}"
            )
        if len(computed) != 13:
            oracle_failures.append(
                f"deterministic evaluator produced {len(computed)} issues, expected 13"
            )

        r010_items = {
            row["work_item_id"]
            for row in computed
            if row["rule_code"] == "R010"
        }
        if r010_items != {"WI-0006", "WI-0007"}:
            oracle_failures.append(
                f"R010 must identify both duplicate rows; found {sorted(r010_items)}"
            )
        r011_items = {
            row["work_item_id"]
            for row in computed
            if row["rule_code"] == "R011"
        }
        if r011_items != {"WI-0010"}:
            oracle_failures.append(
                f"R011 fixed-date result must be WI-0010; found {sorted(r011_items)}"
            )

        if oracle_failures:
            report.failed("practice-rule-oracle", compact(oracle_failures))
        else:
            report.passed(
                "practice-rule-oracle",
                "standard-library evaluator reproduces all 13 frozen issues, including both R010 duplicates and fixed-date R011",
            )
    else:
        report.failed(
            "practice-rule-oracle",
            "not run because practice-data shape is invalid",
        )


def clean_link_target(raw_target: str) -> str | None:
    target = raw_target.strip()
    if target.startswith("<"):
        closing = target.find(">")
        if closing < 0:
            return target
        target = target[1:closing]
    else:
        target = target.split(maxsplit=1)[0]

    lower = target.lower()
    if lower.startswith(
        (
            "http://",
            "https://",
            "mailto:",
            "tel:",
            "data:",
            "javascript:",
            "//",
        )
    ):
        return None
    if target.startswith("#"):
        return None
    target = target.split("#", 1)[0].split("?", 1)[0]
    return unquote(target) if target else None


def validate_internal_links(root: Path, report: Report) -> None:
    failures: list[str] = []
    checked = 0
    ignored_targets = 0
    markdown_files = iter_current_files(root, ".md")

    for markdown in markdown_files:
        try:
            text = markdown.read_text(encoding="utf-8")
        except Exception as exc:
            failures.append(f"{markdown.relative_to(root)} cannot be read: {exc}")
            continue
        searchable = FENCED_CODE_RE.sub("", text)
        raw_targets = [
            match.group(1) for match in INLINE_LINK_RE.finditer(searchable)
        ]
        raw_targets.extend(
            match.group(1) for match in REFERENCE_LINK_RE.finditer(searchable)
        )
        for raw_target in raw_targets:
            target = clean_link_target(raw_target)
            if target is None:
                continue
            candidate = markdown.parent / Path(target.replace("/", os.sep))
            resolved = candidate.resolve()
            try:
                relative = resolved.relative_to(root.resolve())
            except ValueError:
                failures.append(
                    f"{markdown.relative_to(root)} -> escapes root: {target}"
                )
                continue
            if path_is_ignored(relative):
                ignored_targets += 1
                continue
            checked += 1
            if not resolved.exists():
                failures.append(f"{markdown.relative_to(root)} -> {target}")

    if failures:
        report.failed("internal-links", compact(failures, limit=20))
    else:
        report.passed(
            "internal-links",
            f"{checked} current local targets exist; {ignored_targets} archived/generated targets ignored",
        )


def write_report(
    root: Path,
    report: Report,
    output: Path,
    curriculum: dict[str, Any] | None,
    *,
    scope: str,
) -> None:
    result = "PASS" if not report.errors else "FAIL"
    product_status, _ = read_authoritative_product_status(root)
    rendered_product_status = product_status or "INVALID"
    course = curriculum.get("course", {}) if isinstance(curriculum, dict) else {}
    course_title = course.get("title", "Course 1")
    course_version = course.get("version", "unknown")
    source_verified_through = course.get("sourceVerifiedThrough", "unknown")
    content_revision_through = course.get("contentRevisionThrough", "unknown")

    lines = [
        "# Course 1 Package Validation Report",
        "",
        f"Course: **{course_title}**",
        "",
        f"Course version: `{course_version}`",
        "",
        f"Research and sources verified through: `{source_verified_through}`",
        "",
        f"Course content revised through: `{content_revision_through}`",
        "",
        f"Deterministic package result: **{result}**",
        "",
        f"Current Course 1 product status: **`{rendered_product_status}`**",
        "",
        f"Checks: {len(report.checks)}; failures: {len(report.errors)}; warnings: {len(report.warnings)}",
        "",
        "## Scope",
        "",
        "This report covers the curriculum manifest, configured lesson files, the 9",
        "foundation and 9 module Course 1 progress lessons, current JSON contracts,",
        "synthetic practice data, the strategic-focus guardrail, and current internal",
        "links.",
        (
            "Course 4 is checked only for structural isolation and shared-reader "
            "compatibility; its lesson and implementation acceptance are outside this "
            "Course 1 report."
            if scope == "course1"
            else "The full scope also checks the 11-page non-core Course 4 capstone and its required runnable package surface."
        ),
        "Archived Course 4 source material, `app/dist/`, dependency folders, Git",
        "metadata, caches, live cloud resources, and external websites are outside",
        "this deterministic validation.",
        "",
        "| Status | Check | Detail |",
        "|---|---|---|",
    ]
    for check in report.checks:
        detail = check["detail"].replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {check['status']} | {check['name']} | {detail} |")

    if report.errors:
        lines.extend(["", "## Release blockers", ""])
        lines.extend(f"- {error}" for error in report.errors)
    if report.warnings:
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {warning}" for warning in report.warnings)

    lines.extend(
        [
            "",
            "## Limits",
            "",
            "The deterministic package result above covers package structure only; it",
            "does not change the authoritative Course 1 product status or confirm external",
            "source currency, legal compliance, production security, model quality, visual",
            "layout, accessibility, or a learner's implementation. Those require the live",
            "source audit, PWA tests and visual review, and the course evaluation and UAT",
            "gates. Follow `COURSE_1_AUDIT_STATUS_AND_REPAIR_LEDGER.md`; missing",
            "immutable, human, repository, installed-client, device, or live evidence",
            "keeps the current working copy `UNVERIFIED` rather than `PASS`.",
            "",
        ]
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate Course 1 or the full package including Course 4"
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="course package root (default: parent of tools/)",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help="report path (default: <root>/VALIDATION_REPORT.md)",
    )
    parser.add_argument(
        "--scope",
        choices=("course1", "full"),
        default="course1",
        help="course1 excludes Course 4 lesson and implementation acceptance",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    output = (args.report or (root / "VALIDATION_REPORT.md")).resolve()

    if not root.is_dir():
        print(
            json.dumps(
                {
                    "result": "FAIL",
                    "failures": [f"course root is not a directory: {root}"],
                },
                indent=2,
            )
        )
        return 2

    report = Report()
    validate_strategic_focus_guardrail(root, report)
    validate_current_status_consumers(root, report)
    curriculum = validate_curriculum(root, report)
    validate_curriculum_date_metadata(root, curriculum, report)
    validate_release_metadata_sync(root, curriculum, report)
    validate_course4_capstone_integration(
        root,
        curriculum,
        report,
        include_course4_product=args.scope == "full",
    )
    validate_progress_lessons(root, curriculum, report)
    validate_module_structure(root, curriculum, report)
    validate_beginner_practice_contract(root, curriculum, report)
    validate_beginner_terminology(root, report)
    validate_integrated_course_contract(root, curriculum, report)
    validate_course1_beginner_execution_contract(root, curriculum, report)
    validate_course1_learning_content_repairs(root, report)
    validate_current_json(root, report)
    validate_course1_technical_audit_control(root, report)
    validate_course1_learning_audit_control(root, report)
    validate_json_schemas(root, report)
    validate_optional_yaml(root, report)
    validate_practice_data(root, report)
    validate_internal_links(root, report)

    try:
        write_report(root, report, output, curriculum, scope=args.scope)
    except Exception as exc:
        print(
            json.dumps(
                {
                    "result": "FAIL",
                    "failures": [f"could not write validation report: {exc}"],
                },
                indent=2,
            )
        )
        return 2

    summary = {
        "result": "PASS" if not report.errors else "FAIL",
        "product_status": read_authoritative_product_status(root)[0] or "INVALID",
        "checks": len(report.checks),
        "failures": report.errors,
        "warnings": report.warnings,
        "report": str(output),
    }
    print(json.dumps(summary, indent=2))
    return 0 if not report.errors else 1


if __name__ == "__main__":
    sys.exit(main())
