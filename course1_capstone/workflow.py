"""Controlled, synthetic-only Course 1 workflow.

This module intentionally uses only Python's standard library. It has no
network client and no function that can send, pay, order, approve in a source
system, or write back to an external system.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

ASSESSMENT_DATE = date.fromisoformat("2026-07-26")
PIPELINE_VERSION = "course1-offline-v1"
SYNTHETIC_CONFIRMATION = "I_CONFIRM_SYNTHETIC_DATA_ONLY"
HEADERS = [
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
]
STATUSES = {"new", "in_progress", "waiting", "completed", "cancelled"}
OPEN_STATUSES = {"new", "in_progress", "waiting"}
OWNER_STATUSES = {"in_progress", "waiting", "completed"}
PRIORITIES = {"low", "medium", "high"}
DATE_FIELDS = ("received_date", "due_date", "completed_date")
ISSUE_FIELDS = [
    "issue_id",
    "work_item_id",
    "source_reference",
    "source_row",
    "field",
    "raw_value",
    "rule_code",
    "severity",
    "message",
    "assessment_date",
]
APPROVAL_FIELDS = {
    "decision_id",
    "run_id",
    "reviewer_role",
    "decision",
    "draft_revision",
    "draft_sha256",
    "decided_at",
    "expires_at",
    "evidence_reviewed",
    "reason",
}
AI_MODES = {
    "mock",
    "disabled",
    "timeout",
    "refusal",
    "malformed_json",
    "unknown_issue_id",
}
DECISIONS = {"approve", "edit", "reject", "expire"}
TERMINAL_NON_EXPORT_STATES = {"changes_requested", "rejected", "expired"}


class SafeStop(RuntimeError):
    """A named, expected failure that must route to manual handling."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code

    def __str__(self) -> str:
        return f"{self.code}: {super().__str__()}"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_utc(value: datetime) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise SafeStop("invalid_datetime", "A timezone-aware date-time is required.")
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_datetime(value: str, field: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError) as error:
        raise SafeStop("invalid_datetime", f"{field} is not a valid date-time.") from error
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise SafeStop("invalid_datetime", f"{field} must include a timezone.")
    return parsed.astimezone(timezone.utc)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as error:
        raise SafeStop(
            "missing_file",
            f"Required JSON file is missing: {path.name}.",
        ) from error
    except json.JSONDecodeError as error:
        raise SafeStop("malformed_json", f"Invalid JSON in {path.name}: {error.msg}") from error


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def _require_exact_keys(value: Any, required: set[str], label: str) -> None:
    if not isinstance(value, dict):
        raise SafeStop(
            "contract_mismatch",
            f"{label} must be a JSON object.",
        )
    if set(value) != required:
        missing = sorted(required - set(value))
        extra = sorted(set(value) - required)
        raise SafeStop(
            "contract_mismatch",
            f"{label} fields differ; missing={missing}, extra={extra}.",
        )


def _require_non_empty_string(value: Any, label: str, code: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SafeStop(code, f"{label} must be a non-empty string.")
    return value


def _run_locator(run_id: str) -> str:
    """Return the username-free locator stored in a workspace."""

    return (Path("runs") / run_id).as_posix()


def _write_latest_run_locator(workspace: Path, run_id: str) -> None:
    (workspace / "latest_run.txt").write_text(
        _run_locator(run_id) + "\n",
        encoding="utf-8",
    )


def _parse_csv_bytes(input_bytes: bytes, source_name: str) -> list[dict[str, str]]:
    try:
        text = input_bytes.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise SafeStop("malformed_input", f"{source_name} is not UTF-8 text.") from error
    try:
        reader = csv.DictReader(io.StringIO(text, newline=""), strict=True)
        if reader.fieldnames != HEADERS:
            raise SafeStop(
                "header_mismatch",
                f"Expected headers {HEADERS}; received {reader.fieldnames}.",
            )
        rows = list(reader)
    except csv.Error as error:
        raise SafeStop("malformed_input", f"{source_name} is malformed CSV: {error}.") from error
    if not rows:
        raise SafeStop("malformed_input", f"{source_name} contains no work-item rows.")
    clean_rows: list[dict[str, str]] = []
    for source_row, row in enumerate(rows, start=2):
        if None in row or any(value is None for value in row.values()):
            raise SafeStop(
                "malformed_input",
                f"CSV row {source_row} does not have exactly {len(HEADERS)} values.",
            )
        clean = {field: row[field] for field in HEADERS}
        clean["_source_row"] = str(source_row)
        clean_rows.append(clean)
    return clean_rows


def load_work_items(input_path: Path) -> tuple[bytes, list[dict[str, str]]]:
    try:
        input_bytes = input_path.read_bytes()
    except FileNotFoundError as error:
        raise SafeStop(
            "missing_file",
            f"Input file does not exist: {input_path.name}.",
        ) from error
    rows = _parse_csv_bytes(input_bytes, input_path.name)
    work_ids = [row["work_item_id"].strip() for row in rows]
    if any(not re.fullmatch(r"WI-[0-9]{4}", value) for value in work_ids):
        raise SafeStop(
            "invalid_work_item_id",
            "Every work_item_id must use the form WI-0001.",
        )
    duplicate_ids = sorted(
        value for value, count in Counter(work_ids).items() if count > 1
    )
    if duplicate_ids:
        raise SafeStop(
            "duplicate_work_item_id",
            f"Duplicate work_item_id values are not safe to process: {duplicate_ids}.",
        )
    return input_bytes, rows


def _blank(value: str) -> bool:
    return value.strip() == ""


def _parse_date(value: str) -> date | None:
    if len(value) != 10 or value[4] != "-" or value[7] != "-":
        return None
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        return None
    return parsed if parsed.isoformat() == value else None


def _parse_amount(value: str) -> Decimal | None:
    try:
        parsed = Decimal(value)
    except (InvalidOperation, ValueError):
        return None
    return parsed if parsed.is_finite() else None


def issue_key(issue: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(issue["work_item_id"]),
        str(issue["rule_code"]),
        str(issue["field"]),
    )


def detect_issues(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    parsed_dates: dict[str, dict[str, date | None]] = {}

    def add_issue(
        row: dict[str, str],
        field: str,
        rule_code: str,
        severity: str,
        message: str,
    ) -> None:
        work_id = row["work_item_id"].strip()
        issues.append(
            {
                "issue_id": f"{work_id}|{rule_code}|{field}",
                "work_item_id": work_id,
                "source_reference": row["source_reference"],
                "source_row": int(row["_source_row"]),
                "field": field,
                "raw_value": row[field],
                "rule_code": rule_code,
                "severity": severity,
                "message": message,
                "assessment_date": ASSESSMENT_DATE.isoformat(),
            }
        )

    for row in rows:
        for field in (
            "source_reference",
            "title",
            "received_date",
            "category",
        ):
            if _blank(row[field]):
                add_issue(
                    row,
                    field,
                    "R001",
                    "medium",
                    f"Required {field} is missing.",
                )

        status = row["status"].strip()
        priority = row["priority"].strip()
        if status not in STATUSES:
            add_issue(
                row,
                "status",
                "R002",
                "high",
                "Status is not in the allowed list.",
            )
        if priority not in PRIORITIES:
            add_issue(
                row,
                "priority",
                "R003",
                "medium",
                "Priority is not in the allowed list.",
            )

        row_dates: dict[str, date | None] = {}
        for field in DATE_FIELDS:
            raw = row[field].strip()
            parsed = _parse_date(raw) if raw else None
            row_dates[field] = parsed
            if raw and parsed is None:
                add_issue(
                    row,
                    field,
                    "R004",
                    "high",
                    "Date must use ISO format YYYY-MM-DD.",
                )
        parsed_dates[row["work_item_id"]] = row_dates

        received = row_dates["received_date"]
        due = row_dates["due_date"]
        if received is not None and due is not None and due < received:
            add_issue(
                row,
                "due_date",
                "R005",
                "high",
                "Due date is before received date.",
            )

        completed_raw = row["completed_date"].strip()
        if status == "completed" and not completed_raw:
            add_issue(
                row,
                "completed_date",
                "R006",
                "high",
                "Completed work requires a completion date.",
            )
        elif status in (STATUSES - {"completed"}) and completed_raw:
            add_issue(
                row,
                "completed_date",
                "R006",
                "medium",
                "Non-completed work must not have a completion date.",
            )

        if status in OWNER_STATUSES and _blank(row["owner_role"]):
            add_issue(
                row,
                "owner_role",
                "R007",
                "medium",
                "Active work requires an owner role.",
            )

        amount_raw = row["amount"].strip()
        currency = row["currency"].strip()
        if amount_raw:
            amount = _parse_amount(amount_raw)
            if amount is None:
                add_issue(
                    row,
                    "amount",
                    "R008",
                    "high",
                    "Amount must be a non-negative decimal.",
                )
            elif amount < 0:
                add_issue(
                    row,
                    "amount",
                    "R008",
                    "high",
                    "Amount must not be negative.",
                )
            if currency != "EUR":
                add_issue(
                    row,
                    "currency",
                    "R009",
                    "medium",
                    "A populated amount requires currency EUR.",
                )
        elif currency:
            add_issue(
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
            add_issue(
                row,
                "source_reference",
                "R010",
                "high",
                f"Source reference {reference} is duplicated.",
            )

    for row in rows:
        due = parsed_dates[row["work_item_id"]]["due_date"]
        if (
            row["status"].strip() in OPEN_STATUSES
            and due is not None
            and due < ASSESSMENT_DATE
        ):
            add_issue(
                row,
                "due_date",
                "R011",
                "high",
                "Open work is overdue on the fixed assessment date.",
            )

    issues.sort(key=issue_key)
    identities = [issue_key(issue) for issue in issues]
    if len(identities) != len(set(identities)):
        raise SafeStop(
            "duplicate_issue_identity",
            "Two issues have the same (work_item_id, rule_code, field) identity.",
        )
    return issues


def validate_issue(issue: dict[str, Any]) -> None:
    _require_exact_keys(issue, set(ISSUE_FIELDS), "issue")
    expected_id = (
        f"{issue['work_item_id']}|{issue['rule_code']}|{issue['field']}"
    )
    if issue["issue_id"] != expected_id:
        raise SafeStop("invalid_issue_id", f"{issue['issue_id']} is not canonical.")
    if not re.fullmatch(r"WI-[0-9]{4}", issue["work_item_id"]):
        raise SafeStop("invalid_issue", "Issue work_item_id is invalid.")
    if not re.fullmatch(r"R[0-9]{3}", issue["rule_code"]):
        raise SafeStop("invalid_issue", "Issue rule_code is invalid.")
    if issue["severity"] not in {"low", "medium", "high"}:
        raise SafeStop("invalid_issue", "Issue severity is invalid.")
    if not isinstance(issue["source_row"], int) or issue["source_row"] < 2:
        raise SafeStop("invalid_issue", "Issue source_row is invalid.")
    if not isinstance(issue["raw_value"], str) or not issue["message"]:
        raise SafeStop("invalid_issue", "Issue evidence or message is invalid.")


def _build_summary(
    run_id: str,
    issues: list[dict[str, Any]],
    generator: str,
) -> dict[str, Any]:
    groups: list[dict[str, Any]] = []
    for severity in ("high", "medium", "low"):
        selected = [issue for issue in issues if issue["severity"] == severity]
        if not selected:
            continue
        groups.append(
            {
                "label": f"{severity.title()}-severity verified issues",
                "issue_ids": [issue["issue_id"] for issue in selected],
                "summary": " ".join(
                    f"[{issue['issue_id']}] {issue['message']}" for issue in selected
                ),
            }
        )
    actions = [
        {
            "action_id": f"ACT-{index:03d}",
            "action_type": "human_review",
            "issue_ids": [issue["issue_id"]],
            "instruction": (
                f"Review field {issue['field']} in synthetic source row "
                f"{issue['source_row']}; do not perform an external action."
            ),
            "external_action": False,
        }
        for index, issue in enumerate(issues, start=1)
    ]
    return {
        "run_id": run_id,
        "prompt_version": "course1-summary-v1",
        "generator": generator,
        "headline": f"{len(issues)} verified synthetic issues require human review.",
        "groups": groups,
        "review_actions": actions,
        "unsupported_statements": [],
        "review_required": True,
    }


def validate_summary(
    summary: Any,
    issues: list[dict[str, Any]],
    run_id: str,
) -> None:
    required = {
        "run_id",
        "prompt_version",
        "generator",
        "headline",
        "groups",
        "review_actions",
        "unsupported_statements",
        "review_required",
    }
    _require_exact_keys(summary, required, "summary")
    if not isinstance(summary["run_id"], str) or not re.fullmatch(
        r"RUN-[A-F0-9]{12}",
        summary["run_id"],
    ):
        raise SafeStop("summary_contract", "Summary run_id is invalid.")
    if summary["run_id"] != run_id:
        raise SafeStop("summary_run_mismatch", "Summary run_id is not this run.")
    _require_non_empty_string(
        summary["prompt_version"],
        "Summary prompt_version",
        "summary_contract",
    )
    if not isinstance(summary["generator"], str) or summary["generator"] not in {
        "offline-mock",
        "deterministic-fallback",
    }:
        raise SafeStop("summary_contract", "Summary generator is not permitted.")
    _require_non_empty_string(
        summary["headline"],
        "Summary headline",
        "summary_contract",
    )
    if summary["review_required"] is not True:
        raise SafeStop("review_bypass", "review_required must be true.")
    if not isinstance(summary["unsupported_statements"], list) or any(
        not isinstance(statement, str) or not statement
        for statement in summary["unsupported_statements"]
    ):
        raise SafeStop(
            "summary_contract",
            "unsupported_statements must be an array of non-empty strings.",
        )
    if summary["unsupported_statements"]:
        raise SafeStop(
            "unsupported_statement",
            "Unsupported statements require deterministic fallback.",
        )

    known_ids = {issue["issue_id"] for issue in issues}
    grouped_ids: list[str] = []
    if not isinstance(summary["groups"], list) or not summary["groups"]:
        raise SafeStop("summary_contract", "At least one summary group is required.")
    for group in summary["groups"]:
        if not isinstance(group, dict):
            raise SafeStop("summary_contract", "Each group must be an object.")
        _require_exact_keys(group, {"label", "issue_ids", "summary"}, "group")
        _require_non_empty_string(
            group["label"],
            "Group label",
            "summary_contract",
        )
        group_text = _require_non_empty_string(
            group["summary"],
            "Group summary",
            "summary_contract",
        )
        if not isinstance(group["issue_ids"], list) or not group["issue_ids"]:
            raise SafeStop("summary_contract", "A group needs issue references.")
        if any(
            not isinstance(issue_id, str) or not issue_id
            for issue_id in group["issue_ids"]
        ):
            raise SafeStop(
                "summary_contract",
                "Every group issue_id must be a non-empty string.",
            )
        if len(group["issue_ids"]) != len(set(group["issue_ids"])):
            raise SafeStop(
                "duplicate_ai_issue_reference",
                "A group contains the same issue more than once.",
            )
        for issue_id in group["issue_ids"]:
            if issue_id not in known_ids:
                raise SafeStop(
                    "unknown_ai_issue_reference",
                    f"Summary contains unknown issue_id {issue_id}.",
                )
            if f"[{issue_id}]" not in group_text:
                raise SafeStop(
                    "uncited_summary",
                    f"Summary text does not visibly cite {issue_id}.",
                )
            grouped_ids.append(issue_id)
    if len(grouped_ids) != len(set(grouped_ids)):
        raise SafeStop("duplicate_ai_issue_reference", "An issue is grouped twice.")
    if set(grouped_ids) != known_ids:
        raise SafeStop(
            "missing_ai_issue_reference",
            f"Summary omitted issue IDs {sorted(known_ids - set(grouped_ids))}.",
        )

    action_ids: list[str] = []
    covered_by_actions: list[str] = []
    if not isinstance(summary["review_actions"], list) or not summary[
        "review_actions"
    ]:
        raise SafeStop(
            "summary_contract",
            "review_actions must be a non-empty list.",
        )
    for action in summary["review_actions"]:
        if not isinstance(action, dict):
            raise SafeStop("summary_contract", "Each review action must be an object.")
        _require_exact_keys(
            action,
            {
                "action_id",
                "action_type",
                "issue_ids",
                "instruction",
                "external_action",
            },
            "review action",
        )
        if not isinstance(action["action_id"], str) or not re.fullmatch(
            r"ACT-[0-9]{3}",
            action["action_id"],
        ):
            raise SafeStop(
                "summary_contract",
                "Review action_id must use the form ACT-001.",
            )
        if action["action_type"] != "human_review":
            raise SafeStop("unsafe_action", "Only human_review actions are permitted.")
        if action["external_action"] is not False:
            raise SafeStop("external_action_blocked", "External action must be false.")
        _require_non_empty_string(
            action["instruction"],
            "Review instruction",
            "summary_contract",
        )
        if not isinstance(action["issue_ids"], list) or not action["issue_ids"]:
            raise SafeStop(
                "summary_contract",
                "Every review action needs a non-empty issue_ids list.",
            )
        if any(
            not isinstance(issue_id, str) or not issue_id
            for issue_id in action["issue_ids"]
        ):
            raise SafeStop(
                "summary_contract",
                "Every review-action issue_id must be a non-empty string.",
            )
        if len(action["issue_ids"]) != len(set(action["issue_ids"])):
            raise SafeStop(
                "summary_contract",
                "A review action contains the same issue more than once.",
            )
        action_ids.append(action["action_id"])
        for issue_id in action["issue_ids"]:
            if issue_id not in known_ids:
                raise SafeStop(
                    "unknown_ai_issue_reference",
                    f"Review action contains unknown issue_id {issue_id}.",
                )
            covered_by_actions.append(issue_id)
    if len(action_ids) != len(set(action_ids)):
        raise SafeStop("summary_contract", "Review action IDs are not unique.")
    if len(covered_by_actions) != len(set(covered_by_actions)):
        raise SafeStop("summary_contract", "An issue has duplicate review actions.")
    if set(covered_by_actions) != known_ids:
        raise SafeStop(
            "summary_contract",
            "Every verified issue needs exactly one source-linked review action.",
        )


def validate_approval(approval: Any) -> tuple[datetime, datetime]:
    """Validate the complete portable approval contract at every use."""

    _require_exact_keys(approval, APPROVAL_FIELDS, "approval")
    if not isinstance(approval["decision_id"], str) or not re.fullmatch(
        r"DEC-[A-F0-9]{12}",
        approval["decision_id"],
    ):
        raise SafeStop("approval_contract", "Approval decision_id is invalid.")
    if not isinstance(approval["run_id"], str) or not re.fullmatch(
        r"RUN-[A-F0-9]{12}",
        approval["run_id"],
    ):
        raise SafeStop("approval_contract", "Approval run_id is invalid.")
    _require_non_empty_string(
        approval["reviewer_role"],
        "Approval reviewer_role",
        "approval_contract",
    )
    if not isinstance(approval["decision"], str) or approval[
        "decision"
    ] not in DECISIONS:
        raise SafeStop("approval_contract", "Approval decision is invalid.")
    if type(approval["draft_revision"]) is not int or approval["draft_revision"] < 1:
        raise SafeStop(
            "approval_contract",
            "Approval draft_revision must be an integer of at least 1.",
        )
    if not isinstance(approval["draft_sha256"], str) or not re.fullmatch(
        r"[a-f0-9]{64}",
        approval["draft_sha256"],
    ):
        raise SafeStop("approval_contract", "Approval draft_sha256 is invalid.")
    date_time_pattern = (
        r"[0-9]{4}-[0-9]{2}-[0-9]{2}T"
        r"[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?"
        r"(?:Z|[+-][0-9]{2}:[0-9]{2})"
    )
    if not isinstance(approval["decided_at"], str) or not re.fullmatch(
        date_time_pattern,
        approval["decided_at"],
    ):
        raise SafeStop("approval_contract", "Approval decided_at is invalid.")
    if not isinstance(approval["expires_at"], str) or not re.fullmatch(
        date_time_pattern,
        approval["expires_at"],
    ):
        raise SafeStop("approval_contract", "Approval expires_at is invalid.")
    try:
        decided_at = parse_datetime(approval["decided_at"], "decided_at")
        expires_at = parse_datetime(approval["expires_at"], "expires_at")
    except SafeStop as error:
        raise SafeStop("approval_contract", str(error)) from error
    if not isinstance(approval["evidence_reviewed"], bool):
        raise SafeStop(
            "approval_contract",
            "Approval evidence_reviewed must be true or false.",
        )
    _require_non_empty_string(
        approval["reason"],
        "Approval reason",
        "approval_contract",
    )
    if approval["decision"] == "approve":
        if approval["evidence_reviewed"] is not True:
            raise SafeStop(
                "review_evidence_required",
                "Approval requires an explicit completed evidence review.",
            )
        if expires_at <= decided_at:
            raise SafeStop(
                "approval_contract",
                "Approval expires_at must be after decided_at.",
            )
    return decided_at, expires_at


def _simulate_ai_response(
    mode: str,
    run_id: str,
    issues: list[dict[str, Any]],
) -> dict[str, Any]:
    if mode == "timeout":
        raise SafeStop("ai_timeout", "The simulated AI adapter timed out.")
    if mode == "refusal":
        raise SafeStop("ai_refusal", "The simulated AI adapter refused the request.")
    if mode == "malformed_json":
        try:
            return json.loads('{"run_id":')
        except json.JSONDecodeError as error:
            raise SafeStop("malformed_ai_json", "The simulated AI JSON is malformed.") from error
    response = _build_summary(run_id, issues, "offline-mock")
    if mode == "unknown_issue_id":
        response["groups"][0]["issue_ids"][0] = "WI-9999|R999|unknown"
        response["groups"][0]["summary"] = (
            "[WI-9999|R999|unknown] This reference was not verified."
        )
    return response


def create_bounded_summary(
    mode: str,
    run_id: str,
    issues: list[dict[str, Any]],
) -> tuple[dict[str, Any], str | None]:
    if mode not in AI_MODES:
        raise SafeStop("invalid_ai_mode", f"Unknown AI mode: {mode}.")
    if not issues:
        raise SafeStop("no_action_needed", "There are no issues to summarize.")
    if mode == "disabled":
        fallback = _build_summary(run_id, issues, "deterministic-fallback")
        validate_summary(fallback, issues, run_id)
        return fallback, "ai_disabled"
    try:
        response = _simulate_ai_response(mode, run_id, issues)
        validate_summary(response, issues, run_id)
        return response, None
    except SafeStop as error:
        if error.code not in {
            "ai_timeout",
            "ai_refusal",
            "malformed_ai_json",
            "unknown_ai_issue_reference",
        }:
            raise
        fallback = _build_summary(run_id, issues, "deterministic-fallback")
        validate_summary(fallback, issues, run_id)
        return fallback, error.code


def _event_id(
    run_id: str,
    event_type: str,
    state: str,
    details: dict[str, Any],
) -> str:
    seed = canonical_bytes([run_id, event_type, state, details])
    return "EVT-" + sha256_bytes(seed)[:16].upper()


def append_audit_event(
    run_dir: Path,
    run_id: str,
    event_type: str,
    state: str,
    actor_type: str,
    details: dict[str, Any],
    occurred_at: datetime | None = None,
) -> dict[str, Any]:
    event = {
        "event_id": _event_id(run_id, event_type, state, details),
        "run_id": run_id,
        "event_type": event_type,
        "state": state,
        "occurred_at": iso_utc(occurred_at or utc_now()),
        "actor_type": actor_type,
        "details": details,
    }
    validate_audit_event(event)
    audit_path = run_dir / "audit" / "events.jsonl"
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    if audit_path.exists():
        for line in audit_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                existing.append(json.loads(line))
    if event["event_id"] not in {item["event_id"] for item in existing}:
        with audit_path.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
    return event


def validate_audit_event(event: dict[str, Any]) -> None:
    required = {
        "event_id",
        "run_id",
        "event_type",
        "state",
        "occurred_at",
        "actor_type",
        "details",
    }
    _require_exact_keys(event, required, "audit event")
    if not re.fullmatch(r"EVT-[A-F0-9]{16}", event["event_id"]):
        raise SafeStop("invalid_audit_event", "Audit event_id is invalid.")
    if event["actor_type"] not in {"system", "mock_ai", "ai", "reviewer"}:
        raise SafeStop("invalid_audit_event", "Audit actor_type is invalid.")
    parse_datetime(event["occurred_at"], "occurred_at")
    if not isinstance(event["details"], dict):
        raise SafeStop("invalid_audit_event", "Audit details must be an object.")


def _write_issues_csv(path: Path, issues: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=ISSUE_FIELDS)
        writer.writeheader()
        writer.writerows(issues)


def _read_expected_keys(path: Path | None) -> set[tuple[str, str, str]] | None:
    if path is None:
        return None
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.DictReader(stream, strict=True))
    except FileNotFoundError as error:
        raise SafeStop(
            "missing_file",
            f"Expected-issues file is missing: {path.name}.",
        ) from error
    except csv.Error as error:
        raise SafeStop("malformed_input", f"Expected-issues CSV is malformed: {error}") from error
    required = {"work_item_id", "rule_code", "field"}
    if not rows or not required.issubset(set(rows[0])):
        raise SafeStop(
            "expected_contract",
            "Expected issues must contain work_item_id, rule_code, and field.",
        )
    keys = {
        (row["work_item_id"], row["rule_code"], row["field"])
        for row in rows
    }
    if len(keys) != len(rows):
        raise SafeStop("expected_contract", "Expected issue keys are not unique.")
    return keys


def _evaluation(
    run_id: str,
    issues: list[dict[str, Any]],
    expected_keys: set[tuple[str, str, str]] | None,
    fallback_reason: str | None,
    current_state: str,
) -> dict[str, Any]:
    found_keys = {issue_key(issue) for issue in issues}
    if expected_keys is None:
        expected_count: int | None = None
        true_positives: int | None = None
        false_positives: int | None = None
        false_negatives: int | None = None
        recommendation = "REWORK"
        reason = (
            "No frozen expected-issue file was supplied, so accuracy is not yet "
            "demonstrated."
        )
    else:
        expected_count = len(expected_keys)
        true_positives = len(found_keys & expected_keys)
        false_positives = len(found_keys - expected_keys)
        false_negatives = len(expected_keys - found_keys)
        recommendation = "REWORK"
        reason = (
            "The technical run can support a synthetic portfolio, but Course 1 "
            "Modules 1-3 and 7-9 must also pass before the learner may change "
            "this recommendation."
        )
    return {
        "run_id": run_id,
        "dataset_kind": "synthetic",
        "expected_issue_count": expected_count,
        "detected_issue_count": len(issues),
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "correct_issue_references": len(issues),
        "unsupported_ai_claims": 0,
        "summary_fallback_used": fallback_reason is not None,
        "duplicate_retry_safe": True,
        "external_actions": 0,
        "current_state": current_state,
        "course1_recommendation": recommendation,
        "recommendation_reason": reason,
    }


def _manual_fallback_text(run_id: str, issues: list[dict[str, Any]]) -> str:
    return f"""# Manual fallback for {run_id}

Trigger: any failed validation, unavailable summary step, invalid review,
rejection, edit request, expiry, or system unavailability.

Owner: synthetic operations reviewer.

1. Stop automated progression.
2. Open `issues/issues.csv` ({len(issues)} verified issue rows).
3. Review each row against `source/work_items.csv` using `source_row`, `field`,
   `raw_value`, and `rule_code`.
4. Prepare a new internal draft without sending or writing back.
5. Review the exact new revision and record a new decision.

External action: none. Real, workplace, client, personal, and medical data are
prohibited in this Course 1 runner.
"""


def prepare_run(
    input_path: Path,
    workspace: Path,
    ai_mode: str,
    synthetic_confirmation: str,
    expected_path: Path | None = None,
) -> Path:
    if synthetic_confirmation != SYNTHETIC_CONFIRMATION:
        raise SafeStop(
            "synthetic_confirmation_required",
            f"Use the exact confirmation {SYNTHETIC_CONFIRMATION}; never use real data.",
        )
    input_bytes, rows = load_work_items(input_path)
    input_hash = sha256_bytes(input_bytes)
    run_seed = (
        input_hash + "|" + ASSESSMENT_DATE.isoformat() + "|" + PIPELINE_VERSION
    ).encode("utf-8")
    run_id = "RUN-" + sha256_bytes(run_seed)[:12].upper()
    run_dir = workspace.resolve() / "runs" / run_id
    state_path = run_dir / "state.json"
    workspace.mkdir(parents=True, exist_ok=True)

    if state_path.exists():
        state = read_json(state_path)
        if state.get("input_sha256") != input_hash:
            raise SafeStop("run_collision", "Existing run has a different source hash.")
        append_audit_event(
            run_dir,
            run_id,
            "duplicate_retry_ignored",
            state["current_state"],
            "system",
            {"input_sha256": input_hash, "no_duplicate_effect": True},
        )
        _write_latest_run_locator(workspace, run_id)
        return run_dir

    issues = detect_issues(rows)
    for issue in issues:
        validate_issue(issue)
    expected_keys = _read_expected_keys(expected_path)
    if not issues:
        (run_dir / "source").mkdir(parents=True, exist_ok=True)
        (run_dir / "source" / "work_items.csv").write_bytes(input_bytes)
        _write_issues_csv(run_dir / "issues" / "issues.csv", issues)
        write_json(run_dir / "issues" / "issues.json", issues)
        write_json(
            run_dir / "control.json",
            {
                "EXTERNAL_ACTIONS_ENABLED": False,
                "allowed_output": "local_draft_only",
                "dataset_kind": "synthetic",
            },
        )
        state = {
            "run_id": run_id,
            "input_sha256": input_hash,
            "assessment_date": ASSESSMENT_DATE.isoformat(),
            "pipeline_version": PIPELINE_VERSION,
            "current_state": "no_action_needed",
            "draft_revision": 0,
            "draft_sha256": None,
            "active_decision_path": None,
            "ai_mode_requested": ai_mode,
            "summary_generator": None,
            "summary_fallback_reason": None,
            "external_actions": 0,
            "local_export_count": 0,
            "expected_keys": (
                [list(key) for key in sorted(expected_keys)]
                if expected_keys is not None
                else None
            ),
        }
        write_json(state_path, state)
        write_json(
            run_dir / "evaluation.json",
            _evaluation(
                run_id,
                issues,
                expected_keys,
                None,
                "no_action_needed",
            ),
        )
        append_audit_event(
            run_dir,
            run_id,
            "run_received",
            "received",
            "system",
            {"input_sha256": input_hash, "dataset_kind": "synthetic"},
        )
        append_audit_event(
            run_dir,
            run_id,
            "input_validated",
            "validated",
            "system",
            {"row_count": len(rows), "header_count": len(HEADERS)},
        )
        append_audit_event(
            run_dir,
            run_id,
            "no_verified_issues",
            "no_action_needed",
            "system",
            {"issue_count": 0, "external_actions": 0},
        )
        _write_latest_run_locator(workspace, run_id)
        return run_dir
    summary, fallback_reason = create_bounded_summary(ai_mode, run_id, issues)
    draft_bytes = canonical_bytes(summary)
    draft_hash = sha256_bytes(draft_bytes)

    (run_dir / "source").mkdir(parents=True, exist_ok=True)
    (run_dir / "source" / "work_items.csv").write_bytes(input_bytes)
    _write_issues_csv(run_dir / "issues" / "issues.csv", issues)
    write_json(run_dir / "issues" / "issues.json", issues)
    (run_dir / "draft").mkdir(parents=True, exist_ok=True)
    (run_dir / "draft" / "summary.json").write_bytes(draft_bytes)
    write_json(
        run_dir / "review" / "review_package.json",
        {
            "run_id": run_id,
            "draft_revision": 1,
            "draft_sha256": draft_hash,
            "issue_count": len(issues),
            "issues_path": "issues/issues.json",
            "source_path": "source/work_items.csv",
            "summary_path": "draft/summary.json",
            "reviewer_must_check": [
                "Every issue against the named synthetic source row and field.",
                "Every summary sentence against its visible issue identifiers.",
                "Every proposed action is human_review with external_action false.",
                "The exact draft hash and revision before deciding.",
            ],
            "allowed_decisions": ["approve", "edit", "reject", "expire"],
            "external_actions": 0,
        },
    )
    write_json(
        run_dir / "control.json",
        {
            "EXTERNAL_ACTIONS_ENABLED": False,
            "allowed_output": "local_draft_only",
            "dataset_kind": "synthetic",
        },
    )
    (run_dir / "manual_fallback.md").write_text(
        _manual_fallback_text(run_id, issues),
        encoding="utf-8",
    )
    state = {
        "run_id": run_id,
        "input_sha256": input_hash,
        "assessment_date": ASSESSMENT_DATE.isoformat(),
        "pipeline_version": PIPELINE_VERSION,
        "current_state": "needs_review",
        "draft_revision": 1,
        "draft_sha256": draft_hash,
        "active_decision_path": None,
        "ai_mode_requested": ai_mode,
        "summary_generator": summary["generator"],
        "summary_fallback_reason": fallback_reason,
        "external_actions": 0,
        "local_export_count": 0,
        "expected_keys": (
            [list(key) for key in sorted(expected_keys)]
            if expected_keys is not None
            else None
        ),
    }
    write_json(state_path, state)
    write_json(
        run_dir / "evaluation.json",
        _evaluation(
            run_id,
            issues,
            expected_keys,
            fallback_reason,
            "needs_review",
        ),
    )

    append_audit_event(
        run_dir,
        run_id,
        "run_received",
        "received",
        "system",
        {"input_sha256": input_hash, "dataset_kind": "synthetic"},
    )
    append_audit_event(
        run_dir,
        run_id,
        "input_validated",
        "validated",
        "system",
        {"row_count": len(rows), "header_count": len(HEADERS)},
    )
    append_audit_event(
        run_dir,
        run_id,
        "issues_created",
        "issues_ready",
        "system",
        {
            "issue_count": len(issues),
            "identity_fields": ["work_item_id", "rule_code", "field"],
        },
    )
    if fallback_reason is not None:
        append_audit_event(
            run_dir,
            run_id,
            "summary_fallback",
            "summary_ready",
            "system",
            {
                "reason": fallback_reason,
                "generator": "deterministic-fallback",
            },
        )
    else:
        append_audit_event(
            run_dir,
            run_id,
            "mock_summary_validated",
            "summary_ready",
            "mock_ai",
            {"generator": "offline-mock", "issue_reference_count": len(issues)},
        )
    append_audit_event(
        run_dir,
        run_id,
        "human_review_required",
        "needs_review",
        "system",
        {"draft_revision": 1, "draft_sha256": draft_hash},
    )
    _write_latest_run_locator(workspace, run_id)
    return run_dir


def _load_run(run_dir: Path) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    state = read_json(run_dir / "state.json")
    issues = read_json(run_dir / "issues" / "issues.json")
    if not isinstance(issues, list):
        raise SafeStop("contract_mismatch", "issues.json must contain a list.")
    for issue in issues:
        validate_issue(issue)
    summary = read_json(run_dir / "draft" / "summary.json")
    validate_summary(summary, issues, state["run_id"])
    return state, issues, summary


def record_decision(
    run_dir: Path,
    decision: str,
    reviewer_role: str,
    reason: str,
    expected_revision: int,
    evidence_reviewed: bool,
    expires_at: datetime | None = None,
    decided_at: datetime | None = None,
) -> Path:
    if decision not in DECISIONS:
        raise SafeStop("invalid_decision", f"Decision must be one of {sorted(DECISIONS)}.")
    if not reviewer_role.strip() or not reason.strip():
        raise SafeStop("invalid_decision", "Reviewer role and reason are required.")
    initial_state = read_json(run_dir / "state.json")
    if initial_state.get("current_state") == "no_action_needed":
        raise SafeStop(
            "no_action_needed",
            "A run with no verified issues has no draft to decide.",
        )
    state, _, _ = _load_run(run_dir)
    if state["current_state"] not in {"needs_review"}:
        raise SafeStop(
            "invalid_state",
            f"A decision cannot be recorded from state {state['current_state']}.",
        )
    if expected_revision != state["draft_revision"]:
        raise SafeStop(
            "stale_update",
            f"Expected revision {expected_revision}, current revision is "
            f"{state['draft_revision']}.",
        )
    if decision == "approve" and evidence_reviewed is not True:
        raise SafeStop(
            "review_evidence_required",
            "Approval requires an explicit completed evidence review.",
        )
    decided = decided_at or utc_now()
    expires = expires_at or (decided + timedelta(hours=24))
    if decision == "approve" and expires <= decided:
        raise SafeStop("expired_review", "Approval must expire after it is decided.")

    draft_path = run_dir / "draft" / "summary.json"
    current_hash = sha256_bytes(draft_path.read_bytes())
    if current_hash != state["draft_sha256"]:
        raise SafeStop(
            "draft_changed_before_decision",
            "The draft changed; create and review a new controlled revision.",
        )
    decision_seed = canonical_bytes(
        [
            state["run_id"],
            decision,
            expected_revision,
            current_hash,
            reviewer_role,
            iso_utc(decided),
        ]
    )
    record = {
        "decision_id": "DEC-" + sha256_bytes(decision_seed)[:12].upper(),
        "run_id": state["run_id"],
        "reviewer_role": reviewer_role.strip(),
        "decision": decision,
        "draft_revision": expected_revision,
        "draft_sha256": current_hash,
        "decided_at": iso_utc(decided),
        "expires_at": iso_utc(expires),
        "evidence_reviewed": evidence_reviewed,
        "reason": reason.strip(),
    }
    validate_approval(record)
    decision_path = run_dir / "review" / f"decision-r{expected_revision}.json"
    if decision_path.exists():
        raise SafeStop(
            "decision_already_recorded",
            f"Revision {expected_revision} already has a recorded decision.",
        )
    write_json(decision_path, record)
    if decision == "approve":
        new_state = "approved_for_local_export"
    elif decision == "edit":
        new_state = "changes_requested"
    elif decision == "reject":
        new_state = "rejected"
    else:
        new_state = "expired"
    state["current_state"] = new_state
    state["active_decision_path"] = str(decision_path.relative_to(run_dir))
    write_json(run_dir / "state.json", state)
    append_audit_event(
        run_dir,
        state["run_id"],
        "review_decision_recorded",
        new_state,
        "reviewer",
        {
            "decision_id": record["decision_id"],
            "decision": decision,
            "draft_revision": expected_revision,
            "draft_sha256": current_hash,
            "evidence_reviewed": evidence_reviewed,
        },
        decided,
    )
    _refresh_evaluation(run_dir, state, new_state)
    return decision_path


def revise_draft(
    run_dir: Path,
    replacement_path: Path,
    expected_revision: int,
) -> int:
    state, issues, _ = _load_run(run_dir)
    if state["current_state"] != "changes_requested":
        raise SafeStop("invalid_state", "A new draft requires an edit decision.")
    if expected_revision != state["draft_revision"]:
        raise SafeStop(
            "stale_update",
            f"Expected revision {expected_revision}, current revision is "
            f"{state['draft_revision']}.",
        )
    replacement = read_json(replacement_path)
    validate_summary(replacement, issues, state["run_id"])
    replacement_bytes = canonical_bytes(replacement)
    old_hash = state["draft_sha256"]
    new_hash = sha256_bytes(replacement_bytes)
    if new_hash == old_hash:
        raise SafeStop("unchanged_revision", "The replacement draft did not change.")
    next_revision = expected_revision + 1
    (run_dir / "draft" / "summary.json").write_bytes(replacement_bytes)
    state["draft_revision"] = next_revision
    state["draft_sha256"] = new_hash
    state["current_state"] = "needs_review"
    state["active_decision_path"] = None
    write_json(run_dir / "state.json", state)
    review_package = read_json(run_dir / "review" / "review_package.json")
    review_package["draft_revision"] = next_revision
    review_package["draft_sha256"] = new_hash
    write_json(run_dir / "review" / "review_package.json", review_package)
    append_audit_event(
        run_dir,
        state["run_id"],
        "draft_revision_created",
        "needs_review",
        "system",
        {
            "previous_revision": expected_revision,
            "draft_revision": next_revision,
            "previous_sha256": old_hash,
            "draft_sha256": new_hash,
        },
    )
    _refresh_evaluation(run_dir, state, "needs_review")
    return next_revision


def validate_candidate_summary(run_dir: Path, candidate_path: Path) -> Path:
    """Validate a learner-created mock summary without replacing the run draft."""
    state, issues, _ = _load_run(run_dir)
    candidate = read_json(candidate_path)
    validate_summary(candidate, issues, state["run_id"])
    result_path = run_dir / "review" / "candidate-validation.json"
    write_json(
        result_path,
        {
            "run_id": state["run_id"],
            "candidate_sha256": sha256_bytes(canonical_bytes(candidate)),
            "status": "structure_and_issue_references_valid",
            "issue_reference_count": len(issues),
            "human_support_review_required": True,
            "external_actions": 0,
        },
    )
    append_audit_event(
        run_dir,
        state["run_id"],
        "candidate_summary_validated",
        "needs_review",
        "system",
        {
            "candidate_sha256": sha256_bytes(canonical_bytes(candidate)),
            "issue_reference_count": len(issues),
            "human_support_review_required": True,
        },
    )
    return result_path


def _refresh_evaluation(
    run_dir: Path,
    state: dict[str, Any],
    current_state: str,
) -> None:
    issues = read_json(run_dir / "issues" / "issues.json")
    expected_raw = state.get("expected_keys")
    expected_keys = (
        {tuple(value) for value in expected_raw}
        if expected_raw is not None
        else None
    )
    write_json(
        run_dir / "evaluation.json",
        _evaluation(
            state["run_id"],
            issues,
            expected_keys,
            state.get("summary_fallback_reason"),
            current_state,
        ),
    )


def _find_group_label(summary: dict[str, Any], issue_id: str) -> str:
    for group in summary["groups"]:
        if issue_id in group["issue_ids"]:
            return group["label"]
    raise SafeStop("summary_contract", f"No group contains {issue_id}.")


def _find_review_action(summary: dict[str, Any], issue_id: str) -> str:
    for action in summary["review_actions"]:
        if issue_id in action["issue_ids"]:
            return action["instruction"]
    raise SafeStop("summary_contract", f"No review action contains {issue_id}.")


def export_approved(
    run_dir: Path,
    checked_at: datetime | None = None,
) -> tuple[Path, Path]:
    checked = checked_at or utc_now()
    initial_state = read_json(run_dir / "state.json")
    if initial_state.get("current_state") == "no_action_needed":
        raise SafeStop(
            "no_action_needed",
            "A run with no verified issues has no draft to export.",
        )
    state, issues, summary = _load_run(run_dir)
    control = read_json(run_dir / "control.json")
    if control != {
        "EXTERNAL_ACTIONS_ENABLED": False,
        "allowed_output": "local_draft_only",
        "dataset_kind": "synthetic",
    }:
        raise SafeStop(
            "external_action_blocked",
            "Control must explicitly allow only synthetic local drafts with "
            "EXTERNAL_ACTIONS_ENABLED=false.",
        )
    if state["current_state"] in TERMINAL_NON_EXPORT_STATES:
        raise SafeStop(
            "decision_not_approved",
            f"State {state['current_state']} cannot create an export.",
        )
    if state["current_state"] not in {
        "approved_for_local_export",
        "approved_draft",
    }:
        raise SafeStop(
            "review_required",
            "A valid approve decision is required before local export.",
        )
    decision_relative = state.get("active_decision_path")
    if not decision_relative:
        raise SafeStop("review_required", "The approved decision record is missing.")
    decision = read_json(run_dir / decision_relative)
    decided_at, expires_at = validate_approval(decision)
    if decision.get("decision") != "approve":
        raise SafeStop("decision_not_approved", "Decision is not approve.")
    if decision.get("run_id") != state["run_id"]:
        raise SafeStop("approval_run_mismatch", "Decision belongs to another run.")
    if decision.get("draft_revision") != state["draft_revision"]:
        raise SafeStop("stale_update", "Decision belongs to another revision.")
    current_hash = sha256_bytes((run_dir / "draft" / "summary.json").read_bytes())
    if current_hash != state["draft_sha256"]:
        raise SafeStop(
            "edited_draft_after_approval",
            "Draft bytes changed after review; the decision is invalid.",
        )
    if decision.get("draft_sha256") != current_hash:
        raise SafeStop(
            "edited_draft_after_approval",
            "Decision hash does not match the current draft.",
        )
    if checked < decided_at:
        raise SafeStop(
            "approval_not_yet_effective",
            "The export check is earlier than the approval decision.",
        )
    if checked >= expires_at:
        state["current_state"] = "expired"
        write_json(run_dir / "state.json", state)
        append_audit_event(
            run_dir,
            state["run_id"],
            "review_expired",
            "expired",
            "system",
            {
                "decision_id": decision["decision_id"],
                "draft_revision": decision["draft_revision"],
            },
            checked,
        )
        _refresh_evaluation(run_dir, state, "expired")
        raise SafeStop("expired_review", "The approval expired before export.")

    records = [
        {
            "run_id": state["run_id"],
            "draft_revision": state["draft_revision"],
            "issue_id": issue["issue_id"],
            "work_item_id": issue["work_item_id"],
            "source_reference": issue["source_reference"],
            "source_row": issue["source_row"],
            "field": issue["field"],
            "raw_value": issue["raw_value"],
            "rule_code": issue["rule_code"],
            "severity": issue["severity"],
            "message": issue["message"],
            "summary_group": _find_group_label(summary, issue["issue_id"]),
            "review_action": _find_review_action(summary, issue["issue_id"]),
        }
        for issue in issues
    ]
    export_payload = {
        "run_id": state["run_id"],
        "draft_revision": state["draft_revision"],
        "draft_sha256": current_hash,
        "decision_id": decision["decision_id"],
        "dataset_kind": "synthetic",
        "output_kind": "local_draft_only",
        "external_actions": 0,
        "records": records,
    }
    outbox = run_dir / "outbox"
    outbox.mkdir(parents=True, exist_ok=True)
    json_path = outbox / f"approved-r{state['draft_revision']}.json"
    csv_path = outbox / f"approved-r{state['draft_revision']}.csv"
    json_bytes = canonical_bytes(export_payload)
    if json_path.exists() and json_path.read_bytes() != json_bytes:
        raise SafeStop("idempotency_conflict", "Existing JSON export differs.")
    json_path.write_bytes(json_bytes)
    fields = list(records[0])
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields)
    writer.writeheader()
    writer.writerows(records)
    csv_bytes = buffer.getvalue().encode("utf-8")
    if csv_path.exists() and csv_path.read_bytes() != csv_bytes:
        raise SafeStop("idempotency_conflict", "Existing CSV export differs.")
    csv_path.write_bytes(csv_bytes)

    state["current_state"] = "approved_draft"
    state["local_export_count"] = 2
    state["external_actions"] = 0
    write_json(run_dir / "state.json", state)
    append_audit_event(
        run_dir,
        state["run_id"],
        "local_export_created",
        "approved_draft",
        "system",
        {
            "decision_id": decision["decision_id"],
            "draft_revision": state["draft_revision"],
            "files": [json_path.name, csv_path.name],
            "external_actions": 0,
        },
        checked,
    )
    _refresh_evaluation(run_dir, state, "approved_draft")
    return json_path, csv_path


def inspect_run(run_dir: Path) -> dict[str, Any]:
    state = read_json(run_dir / "state.json")
    issues = read_json(run_dir / "issues" / "issues.json")
    if state["current_state"] == "no_action_needed":
        summary_generator = None
    else:
        _, issues, summary = _load_run(run_dir)
        summary_generator = summary["generator"]
    audit_path = run_dir / "audit" / "events.jsonl"
    events = [
        json.loads(line)
        for line in audit_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    for event in events:
        validate_audit_event(event)
    return {
        "run_id": state["run_id"],
        "current_state": state["current_state"],
        "latest_attempt_state": events[-1]["state"],
        "latest_event_type": events[-1]["event_type"],
        "draft_revision": state["draft_revision"],
        "issue_count": len(issues),
        "summary_generator": summary_generator,
        "audit_event_count": len(events),
        "local_export_count": state["local_export_count"],
        "external_actions": state["external_actions"],
    }
