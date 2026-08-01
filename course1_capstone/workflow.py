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
import os
import re
import stat
import tempfile
import threading
import uuid
from collections import Counter
from contextlib import contextmanager
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Callable, Iterator

ASSESSMENT_DATE = date.fromisoformat("2026-07-26")
PIPELINE_VERSION = "course1-offline-v1"
RULES_VERSION = "course1-rules-v1"
PROMPT_VERSION = "course1-summary-v1"
MOCK_GENERATOR_VERSION = "course1-offline-mock-v1"
FALLBACK_GENERATOR_VERSION = "course1-deterministic-fallback-v1"
RUN_CONFIG_SCHEMA_VERSION = "course1-run-config-v1"
REVIEW_MANIFEST_SCHEMA_VERSION = "course1-review-manifest-v1"
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
    "review_manifest_sha256",
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
WORKFLOW_STATES = {
    "received",
    "validated",
    "issues_ready",
    "summary_ready",
    "needs_review",
    "changes_requested",
    "approved_for_local_export",
    "approved_draft",
    "rejected",
    "expired",
    "no_action_needed",
    "failed_manual",
}
PERSISTED_STATES = {
    "needs_review",
    "changes_requested",
    "approved_for_local_export",
    "approved_draft",
    "rejected",
    "expired",
    "no_action_needed",
}
STATE_FIELDS = {
    "run_id",
    "run_config_sha256",
    "input_sha256",
    "assessment_date",
    "pipeline_version",
    "rules_version",
    "prompt_version",
    "current_state",
    "draft_revision",
    "draft_sha256",
    "review_manifest_sha256",
    "active_decision_path",
    "ai_mode_requested",
    "summary_generator",
    "summary_fallback_reason",
    "external_actions",
    "local_export_count",
    "expected_keys",
}
RUN_CONFIG_FIELDS = {
    "schema_version",
    "input_sha256",
    "assessment_date",
    "pipeline_version",
    "rules_version",
    "prompt_version",
    "requested_adapter_mode",
    "mock_generator_version",
    "fallback_generator_version",
    "expected_oracle_present",
    "expected_oracle_sha256",
}
CONTROL = {
    "EXTERNAL_ACTIONS_ENABLED": False,
    "allowed_output": "local_draft_only",
    "dataset_kind": "synthetic",
}
REVIEW_PACKAGE_FIELDS = {
    "run_id",
    "draft_revision",
    "draft_sha256",
    "issue_count",
    "issues_json_path",
    "issues_csv_path",
    "source_path",
    "summary_path",
    "control_path",
    "run_config_path",
    "review_manifest_path",
    "reviewer_must_check",
    "allowed_decisions",
    "external_actions",
}
EXPECTED_ORACLE_EVIDENCE_PATH = "source/expected_issues.evidence"
EXPECTED_ORACLE_ABSENT_BYTES = b"EXPECTED_ORACLE_NOT_SUPPLIED\n"
STAGING_PREFIX = ".course1-staging-"
PROTECTED_REVIEW_ARTIFACTS = {
    "source": "source/work_items.csv",
    "expected_oracle": EXPECTED_ORACLE_EVIDENCE_PATH,
    "issues_json": "issues/issues.json",
    "issues_csv": "issues/issues.csv",
    "summary": "draft/summary.json",
    "control": "control.json",
    "run_config": "run_config.json",
    "review_package": "review/review_package.json",
}
OPERATION_LOCK_NAME = ".course1-operation.lock"
TRANSACTION_INCOMPLETE_NAME = "CONTROLLED_TRANSACTION_INCOMPLETE.txt"
STAGING_MARKER_NAME = ".course1-staging-owner.json"
STAGING_MARKER_FORMAT = "course1-owned-staging-v1"
MIB = 1024 * 1024
MAX_WORK_ITEM_CSV_BYTES = 2 * MIB
MAX_WORK_ITEM_ROWS = 2_000
MAX_EXPECTED_CSV_BYTES = 2 * MIB
MAX_EXPECTED_ROWS = 25_000
MAX_CSV_CELL_CODE_POINTS = 16_384
MAX_JSON_BYTES = 4 * MIB
MAX_JSON_DEPTH = 32
MAX_JSON_ARRAY_ITEMS = 25_000
MAX_JSON_OBJECT_PROPERTIES = 256
MAX_JSON_STRING_CODE_POINTS = 65_536
MAX_AUDIT_BYTES = 16 * MIB
MAX_AUDIT_EVENTS = 25_000
MAX_AUDIT_LINE_BYTES = 256 * 1024
MAX_WORKSPACE_PATH_CHARACTERS = 175
BIDI_CONTROLS = {
    "\u061c",
    "\u200e",
    "\u200f",
    "\u202a",
    "\u202b",
    "\u202c",
    "\u202d",
    "\u202e",
    "\u2066",
    "\u2067",
    "\u2068",
    "\u2069",
}
WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}
AUDIT_EVENT_CONTRACTS = {
    "run_received": (
        {"received"},
        "system",
        {"input_sha256", "run_config_sha256", "dataset_kind"},
    ),
    "input_validated": (
        {"validated"},
        "system",
        {"row_count", "header_count"},
    ),
    "no_verified_issues": (
        {"no_action_needed"},
        "system",
        {"issue_count", "external_actions"},
    ),
    "issues_created": (
        {"issues_ready"},
        "system",
        {"issue_count", "identity_fields"},
    ),
    "summary_fallback": (
        {"summary_ready"},
        "system",
        {"reason", "generator"},
    ),
    "mock_summary_validated": (
        {"summary_ready"},
        "mock_ai",
        {"generator", "issue_reference_count"},
    ),
    "human_review_required": (
        {"needs_review"},
        "system",
        {"draft_revision", "draft_sha256", "review_manifest_sha256"},
    ),
    "duplicate_retry_ignored": (
        PERSISTED_STATES,
        "system",
        {"input_sha256", "run_config_sha256", "no_duplicate_effect"},
    ),
    "review_decision_recorded": (
        {"approved_for_local_export", "changes_requested", "rejected", "expired"},
        "reviewer",
        {
            "decision_id",
            "decision",
            "draft_revision",
            "draft_sha256",
            "review_manifest_sha256",
            "evidence_reviewed",
            "integrity_scope",
        },
    ),
    "draft_revision_created": (
        {"needs_review"},
        "system",
        {
            "previous_revision",
            "draft_revision",
            "previous_sha256",
            "draft_sha256",
            "review_manifest_sha256",
        },
    ),
    "candidate_summary_validated": (
        {"needs_review"},
        "system",
        {
            "candidate_sha256",
            "draft_revision",
            "issue_reference_count",
            "prose_support_status",
            "human_support_review_required",
        },
    ),
    "local_export_created": (
        {"approved_draft"},
        "system",
        {"decision_id", "draft_revision", "files", "external_actions"},
    ),
    "review_expired": (
        {"expired"},
        "system",
        {"decision_id", "draft_revision"},
    ),
    "safe_stop_recorded": (
        {"failed_manual"},
        "system",
        {"attempt_id", "error_code", "command", "external_actions"},
    ),
}
_LOCK_OWNERS = threading.local()


class SafeStop(RuntimeError):
    """A named, expected failure that must route to manual handling."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code

    def __str__(self) -> str:
        return f"{self.code}: {super().__str__()}"


def _reject_disallowed_controls(value: str, label: str) -> None:
    if not isinstance(value, str):
        raise SafeStop("invalid_text", f"{label} must be text.")
    if any(ord(character) < 32 and character not in "\t\r\n" for character in value):
        raise SafeStop(
            "invalid_text_control",
            f"{label} contains an unsupported control character.",
        )


def _reject_bidi_controls(value: str, label: str) -> None:
    if any(character in BIDI_CONTROLS for character in value):
        raise SafeStop(
            "invalid_bidi_control",
            f"{label} contains an unsupported bidirectional control character.",
        )


def _path_has_reparse_attribute(path_stat: os.stat_result) -> bool:
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return bool(getattr(path_stat, "st_file_attributes", 0) & reparse_flag)


def _validate_supported_path(
    path: Path,
    label: str,
    *,
    workspace_root: bool = False,
) -> None:
    if not isinstance(path, Path):
        raise SafeStop("invalid_argument", f"{label} path must be a Path.")
    raw = str(path)
    _reject_disallowed_controls(raw, f"{label} path")
    _reject_bidi_controls(raw, f"{label} path")
    normalized_slashes = raw.replace("/", "\\")
    if normalized_slashes.startswith(("\\\\?\\", "\\\\.\\")):
        raise SafeStop(
            "unsupported_path",
            f"{label} must not use a Windows device namespace.",
        )
    if normalized_slashes.startswith("\\\\"):
        raise SafeStop(
            "unsupported_path",
            f"{label} must use an ordinary local folder, not a network or device path.",
        )
    for component in path.parts:
        if component in {path.anchor, path.drive, "\\", "/"}:
            continue
        if component.endswith((" ", ".")):
            raise SafeStop(
                "unsupported_path",
                f"{label} has a name ending in a space or dot.",
            )
        if ":" in component:
            raise SafeStop(
                "unsupported_path",
                f"{label} must not use an alternate data stream.",
            )
        stem = component.split(".", 1)[0].upper()
        if stem in WINDOWS_RESERVED_NAMES:
            raise SafeStop(
                "unsupported_path",
                f"{label} uses a reserved Windows device name.",
            )
    try:
        absolute = path.absolute()
    except OSError as error:
        raise SafeStop(
            "filesystem_check_error",
            f"Could not inspect the {label} path.",
        ) from error
    if workspace_root and len(str(absolute)) > MAX_WORKSPACE_PATH_CHARACTERS:
        raise SafeStop(
            "workspace_path_too_long",
            "The workspace path is longer than 175 characters. Choose a shorter "
            "ordinary local folder, then retry; nothing was moved or deleted.",
        )
    existing_chain = [absolute, *absolute.parents]
    for component in reversed(existing_chain):
        try:
            component_stat = component.lstat()
        except FileNotFoundError:
            continue
        except OSError as error:
            raise SafeStop(
                "filesystem_check_error",
                f"Could not safely inspect the {label} path.",
            ) from error
        if stat.S_ISLNK(component_stat.st_mode) or _path_has_reparse_attribute(
            component_stat
        ):
            raise SafeStop(
                "unsupported_reparse_path",
                f"{label} must use an ordinary local folder without links or reparse points.",
            )


def _read_regular_bytes(
    path: Path,
    label: str,
    *,
    max_bytes: int,
    missing_code: str = "missing_file",
) -> bytes:
    _validate_supported_path(path, label)
    try:
        before = path.lstat()
    except FileNotFoundError as error:
        raise SafeStop(missing_code, f"Required {label} is missing.") from error
    except OSError as error:
        raise SafeStop(
            "file_read_error",
            f"Could not safely inspect {label}.",
        ) from error
    if (
        not stat.S_ISREG(before.st_mode)
        or stat.S_ISLNK(before.st_mode)
        or _path_has_reparse_attribute(before)
    ):
        raise SafeStop(
            "unsupported_file_type",
            f"{label} must be an ordinary file, not a folder, link, device, or stream.",
        )
    if before.st_size > max_bytes:
        raise SafeStop(
            "input_limit_exceeded",
            f"{label} is larger than the supported {max_bytes}-byte limit.",
        )
    try:
        with path.open("rb") as stream:
            opened = os.fstat(stream.fileno())
            value = stream.read(max_bytes + 1)
            after_open = os.fstat(stream.fileno())
        after_path = path.lstat()
    except OSError as error:
        raise SafeStop(
            "file_read_error",
            f"Could not safely read {label}.",
        ) from error
    identities = {
        (before.st_dev, before.st_ino),
        (opened.st_dev, opened.st_ino),
        (after_open.st_dev, after_open.st_ino),
        (after_path.st_dev, after_path.st_ino),
    }
    if (
        len(identities) != 1
        or opened.st_size != after_open.st_size
        or before.st_size != after_path.st_size
        or len(value) != after_open.st_size
    ):
        raise SafeStop(
            "file_changed_during_read",
            f"{label} changed while it was being read; nothing was trusted.",
        )
    if len(value) > max_bytes:
        raise SafeStop(
            "input_limit_exceeded",
            f"{label} is larger than the supported {max_bytes}-byte limit.",
        )
    return value


def _decode_utf8(value: bytes, label: str, *, code: str) -> str:
    try:
        text = value.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise SafeStop(code, f"{label} is not valid UTF-8 text.") from error
    if text.startswith("\ufeff"):
        raise SafeStop(code, f"{label} contains more than one UTF-8 byte-order mark.")
    _reject_disallowed_controls(text, label)
    return text


def _validate_json_complexity(value: Any, label: str, depth: int = 0) -> None:
    if depth > MAX_JSON_DEPTH:
        raise SafeStop("json_limit_exceeded", f"{label} is nested too deeply.")
    if value is None or type(value) in {bool, int, float}:
        return
    if isinstance(value, str):
        if len(value) > MAX_JSON_STRING_CODE_POINTS:
            raise SafeStop("json_limit_exceeded", f"{label} contains an oversized string.")
        _reject_disallowed_controls(value, label)
        return
    if isinstance(value, list):
        if len(value) > MAX_JSON_ARRAY_ITEMS:
            raise SafeStop("json_limit_exceeded", f"{label} contains too many array items.")
        for item in value:
            _validate_json_complexity(item, label, depth + 1)
        return
    if isinstance(value, dict):
        if len(value) > MAX_JSON_OBJECT_PROPERTIES:
            raise SafeStop(
                "json_limit_exceeded",
                f"{label} contains too many object properties.",
            )
        for key, item in value.items():
            if not isinstance(key, str):
                raise SafeStop("malformed_json", f"{label} contains a non-text key.")
            _reject_disallowed_controls(key, f"{label} key")
            _reject_bidi_controls(key, f"{label} key")
            _validate_json_complexity(item, label, depth + 1)
        return
    raise SafeStop("malformed_json", f"{label} contains an unsupported JSON value.")


def _json_object_without_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise SafeStop("malformed_json", "JSON contains a duplicate object key.")
        result[key] = value
    return result


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_utc(value: datetime) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise SafeStop("invalid_datetime", "A timezone-aware date-time is required.")
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_datetime(value: str, field: str) -> datetime:
    if not isinstance(value, str) or not isinstance(field, str):
        raise SafeStop(
            "invalid_datetime",
            "A date-time value and field name must both be text.",
        )
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError) as error:
        raise SafeStop(
            "invalid_datetime", f"{field} is not a valid date-time."
        ) from error
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise SafeStop("invalid_datetime", f"{field} must include a timezone.")
    return parsed.astimezone(timezone.utc)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    _validate_json_complexity(value, "Controlled JSON")
    try:
        rendered = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as error:
        raise SafeStop(
            "malformed_json",
            "Controlled JSON contains an unsupported value.",
        ) from error
    encoded = (rendered + "\n").encode("utf-8")
    if len(encoded) > MAX_JSON_BYTES:
        raise SafeStop(
            "json_limit_exceeded",
            f"Controlled JSON is larger than the supported {MAX_JSON_BYTES}-byte limit.",
        )
    return encoded


def read_json(path: Path) -> Any:
    try:
        encoded = _read_regular_bytes(
            path,
            f"JSON file {path.name}",
            max_bytes=MAX_JSON_BYTES,
        )
        text = _decode_utf8(encoded, f"JSON file {path.name}", code="malformed_json")
        value = json.loads(
            text,
            object_pairs_hook=_json_object_without_duplicates,
            parse_constant=lambda _: (_ for _ in ()).throw(
                SafeStop("malformed_json", f"Invalid JSON value in {path.name}.")
            ),
        )
        _validate_json_complexity(value, f"JSON file {path.name}")
        return value
    except json.JSONDecodeError as error:
        raise SafeStop(
            "malformed_json", f"Invalid JSON in {path.name}: {error.msg}"
        ) from error


def atomic_write_bytes(path: Path, value: bytes) -> None:
    if not isinstance(path, Path) or type(value) is not bytes:
        raise SafeStop(
            "invalid_argument",
            "Controlled writes require a Path and bytes.",
        )
    _validate_supported_path(path, "Controlled output")
    temporary_path = path.parent / f"~{uuid.uuid4().hex[:16]}.tmp"
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        _validate_supported_path(path.parent, "Controlled output folder")
        parent_before = path.parent.lstat()
        if not stat.S_ISDIR(parent_before.st_mode):
            raise SafeStop(
                "output_parent_type_mismatch",
                "A controlled output parent must be an ordinary folder.",
            )
        if path.exists():
            existing = path.lstat()
            if (
                not stat.S_ISREG(existing.st_mode)
                or stat.S_ISLNK(existing.st_mode)
                or _path_has_reparse_attribute(existing)
            ):
                raise SafeStop(
                    "output_type_mismatch",
                    "A controlled output target is not an ordinary file.",
                )
        with temporary_path.open("xb") as stream:
            stream.write(value)
            stream.flush()
            os.fsync(stream.fileno())
        parent_after = path.parent.lstat()
        if (parent_before.st_dev, parent_before.st_ino) != (
            parent_after.st_dev,
            parent_after.st_ino,
        ):
            raise SafeStop(
                "output_parent_changed",
                "The controlled output folder changed during the write; nothing was published.",
            )
        os.replace(temporary_path, path)
    except SafeStop:
        try:
            temporary_path.unlink(missing_ok=True)
        except OSError:
            pass
        raise
    except OSError as error:
        try:
            temporary_path.unlink(missing_ok=True)
        except OSError:
            pass
        raise SafeStop(
            "file_write_error",
            f"Could not safely write controlled file {path.name}.",
        ) from error


def write_json(path: Path, value: Any) -> None:
    atomic_write_bytes(path, canonical_bytes(value))


def _read_bytes(path: Path, label: str) -> bytes:
    return _read_regular_bytes(path, label, max_bytes=MAX_JSON_BYTES)


def _path_exists(path: Path, label: str) -> bool:
    if not isinstance(path, Path):
        raise SafeStop("invalid_argument", f"{label} path must be a Path.")
    try:
        return path.exists()
    except OSError as error:
        raise SafeStop(
            "filesystem_check_error",
            f"Could not safely inspect {label}.",
        ) from error


@contextmanager
def _exclusive_operation_lock(scope: Path) -> Iterator[None]:
    """Reject overlapping operations instead of interleaving controlled writes."""

    if not isinstance(scope, Path):
        raise SafeStop("invalid_argument", "Lock scope must be a Path.")
    _validate_supported_path(scope, "Controlled lock scope")
    try:
        if scope.exists() and not scope.is_dir():
            raise SafeStop(
                "scope_not_directory",
                "The selected controlled scope is a file, not a folder. Choose an "
                "ordinary local folder and retry.",
            )
    except OSError as error:
        raise SafeStop(
            "filesystem_check_error",
            "The controlled lock scope could not be inspected.",
        ) from error
    try:
        scope_key = os.path.normcase(str(scope.resolve()))
    except OSError as error:
        raise SafeStop("lock_error", "The lock scope could not be resolved.") from error
    held = getattr(_LOCK_OWNERS, "held", {})
    if held.get(scope_key, 0):
        held[scope_key] += 1
        _LOCK_OWNERS.held = held
        try:
            yield
        finally:
            held[scope_key] -= 1
            if held[scope_key] == 0:
                del held[scope_key]
        return
    lock_path = scope / OPERATION_LOCK_NAME
    descriptor: int | None = None
    try:
        scope.mkdir(parents=True, exist_ok=True)
        scope_stat = scope.lstat()
        if (
            not stat.S_ISDIR(scope_stat.st_mode)
            or stat.S_ISLNK(scope_stat.st_mode)
            or _path_has_reparse_attribute(scope_stat)
        ):
            raise SafeStop(
                "scope_not_directory",
                "The selected controlled scope is not an ordinary local folder.",
            )
        descriptor = os.open(
            lock_path,
            os.O_CREAT | os.O_EXCL | os.O_WRONLY,
            0o600,
        )
        os.write(
            descriptor,
            canonical_bytes(
                {
                    "pid": os.getpid(),
                    "created_at": iso_utc(utc_now()),
                }
            ),
        )
        os.fsync(descriptor)
    except FileExistsError as error:
        try:
            lock_stat = lock_path.lstat()
        except OSError:
            lock_stat = None
        if lock_stat is not None and (
            not stat.S_ISREG(lock_stat.st_mode)
            or stat.S_ISLNK(lock_stat.st_mode)
            or _path_has_reparse_attribute(lock_stat)
        ):
            raise SafeStop(
                "lock_contract_error",
                "The controlled lock path is not an ordinary lock file. Stop and "
                "inspect the folder; nothing was removed.",
            ) from error
        raise SafeStop(
            "concurrent_operation",
            "Another Course 1 operation is already using this controlled scope. "
            "Wait for it to finish, then retry. After a confirmed crash, follow "
            "the proof-first stale-lock steps in course1_capstone/README.md.",
        ) from error
    except SafeStop:
        if descriptor is not None:
            try:
                os.close(descriptor)
            except OSError:
                pass
            descriptor = None
            try:
                lock_path.unlink(missing_ok=True)
            except OSError:
                pass
        raise
    except OSError as error:
        if descriptor is not None:
            try:
                os.close(descriptor)
            except OSError:
                pass
            descriptor = None
            try:
                lock_path.unlink(missing_ok=True)
            except OSError:
                pass
        raise SafeStop(
            "lock_error",
            "The controlled operation lock could not be created.",
        ) from error
    finally:
        if descriptor is not None:
            try:
                os.close(descriptor)
            except OSError:
                pass
    try:
        held[scope_key] = 1
        _LOCK_OWNERS.held = held
        yield
    finally:
        held[scope_key] -= 1
        if held[scope_key] == 0:
            del held[scope_key]
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass
        except OSError as error:
            raise SafeStop(
                "lock_release_error",
                "The operation finished but its lock could not be removed. "
                "Do not continue until the lock is checked.",
            ) from error


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


def _require_sha256(value: Any, label: str, code: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[a-f0-9]{64}", value):
        raise SafeStop(code, f"{label} must be a lowercase SHA-256 hash.")
    return value


def _require_run_id(value: Any, label: str, code: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"RUN-[A-F0-9]{12}", value):
        raise SafeStop(code, f"{label} is invalid.")
    return value


def _spreadsheet_safe(value: Any) -> Any:
    """Keep spreadsheet software from evaluating controlled CSV text as a formula."""

    if not isinstance(value, str):
        return value
    if re.match(r"^[\s\x00-\x1f]*[=+\-@]", value):
        return "'" + value
    return value


def _csv_bytes(rows: list[dict[str, Any]], fields: list[str]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=fields, lineterminator="\r\n")
    writer.writeheader()
    writer.writerows(
        [{field: _spreadsheet_safe(row[field]) for field in fields} for row in rows]
    )
    return buffer.getvalue().encode("utf-8")


def _run_locator(run_id: str) -> str:
    """Return the username-free locator stored in a workspace."""

    return (Path("runs") / run_id).as_posix()


def _write_latest_run_locator(workspace: Path, run_id: str) -> None:
    atomic_write_bytes(
        workspace / "latest_run.txt",
        (_run_locator(run_id) + "\n").encode("utf-8"),
    )


def _parse_csv_bytes(input_bytes: bytes, source_name: str) -> list[dict[str, str]]:
    if len(input_bytes) > MAX_WORK_ITEM_CSV_BYTES:
        raise SafeStop(
            "input_limit_exceeded",
            f"{source_name} is larger than the supported 2 MiB work-item limit.",
        )
    text = _decode_utf8(input_bytes, source_name, code="malformed_input")
    try:
        reader = csv.DictReader(io.StringIO(text, newline=""), strict=True)
        if reader.fieldnames != HEADERS:
            raise SafeStop(
                "header_mismatch",
                f"Expected headers {HEADERS}; received {reader.fieldnames}.",
            )
        rows: list[dict[str, str]] = []
        for row in reader:
            if len(rows) >= MAX_WORK_ITEM_ROWS:
                raise SafeStop(
                    "input_limit_exceeded",
                    f"{source_name} contains more than {MAX_WORK_ITEM_ROWS} work-item rows.",
                )
            rows.append(row)
    except csv.Error as error:
        raise SafeStop(
            "malformed_input", f"{source_name} is malformed CSV: {error}."
        ) from error
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
        for field, value in clean.items():
            if len(value) > MAX_CSV_CELL_CODE_POINTS:
                raise SafeStop(
                    "input_limit_exceeded",
                    f"CSV row {source_row} field {field} exceeds the supported cell limit.",
                )
        clean["_source_row"] = str(source_row)
        clean_rows.append(clean)
    return clean_rows


def load_work_items(input_path: Path) -> tuple[bytes, list[dict[str, str]]]:
    if not isinstance(input_path, Path):
        raise SafeStop("invalid_argument", "Input path must be a Path.")
    input_bytes = _read_regular_bytes(
        input_path,
        f"input file {input_path.name}",
        max_bytes=MAX_WORK_ITEM_CSV_BYTES,
    )
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
                "Source reference is duplicated.",
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
    for field in (
        "issue_id",
        "work_item_id",
        "source_reference",
        "field",
        "raw_value",
        "rule_code",
        "severity",
        "message",
        "assessment_date",
    ):
        if not isinstance(issue[field], str):
            raise SafeStop("invalid_issue", f"Issue {field} must be a string.")
    if type(issue["source_row"]) is not int:
        raise SafeStop("invalid_issue", "Issue source_row must be an integer.")
    expected_id = f"{issue['work_item_id']}|{issue['rule_code']}|{issue['field']}"
    if issue["issue_id"] != expected_id:
        raise SafeStop("invalid_issue_id", f"{issue['issue_id']} is not canonical.")
    if not re.fullmatch(r"WI-[0-9]{4}", issue["work_item_id"]):
        raise SafeStop("invalid_issue", "Issue work_item_id is invalid.")
    if not re.fullmatch(r"R[0-9]{3}", issue["rule_code"]):
        raise SafeStop("invalid_issue", "Issue rule_code is invalid.")
    if issue["field"] not in HEADERS:
        raise SafeStop("invalid_issue", "Issue field is invalid.")
    if issue["severity"] not in {"low", "medium", "high"}:
        raise SafeStop("invalid_issue", "Issue severity is invalid.")
    if issue["source_row"] < 2:
        raise SafeStop("invalid_issue", "Issue source_row is invalid.")
    if not issue["message"]:
        raise SafeStop("invalid_issue", "Issue evidence or message is invalid.")
    try:
        parsed_assessment_date = date.fromisoformat(issue["assessment_date"])
    except ValueError as error:
        raise SafeStop("invalid_issue", "Issue assessment_date is invalid.") from error
    if parsed_assessment_date.isoformat() != issue["assessment_date"]:
        raise SafeStop("invalid_issue", "Issue assessment_date is not canonical.")


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
        "prompt_version": PROMPT_VERSION,
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
    source_rows: list[dict[str, str]] | None = None,
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
    if summary["prompt_version"] != PROMPT_VERSION:
        raise SafeStop(
            "summary_contract",
            "Summary prompt_version is not the controlled Course 1 version.",
        )
    if not isinstance(summary["generator"], str) or summary["generator"] not in {
        "offline-mock",
        "deterministic-fallback",
    }:
        raise SafeStop("summary_contract", "Summary generator is not permitted.")
    headline = _require_non_empty_string(
        summary["headline"], "Summary headline", "summary_contract"
    )
    safe_headlines = {
        f"{len(issues)} verified synthetic issues require human review.",
        f"Human review is required for {len(issues)} verified synthetic issues.",
    }
    if headline not in safe_headlines:
        raise SafeStop(
            "unsupported_summary_claim",
            "Summary headline must use one of the controlled evidence-count templates.",
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

    issue_by_id = {issue["issue_id"]: issue for issue in issues}
    known_ids = set(issue_by_id)
    grouped_ids: list[str] = []
    if not isinstance(summary["groups"], list) or not summary["groups"]:
        raise SafeStop("summary_contract", "At least one summary group is required.")
    for group in summary["groups"]:
        if not isinstance(group, dict):
            raise SafeStop("summary_contract", "Each group must be an object.")
        _require_exact_keys(group, {"label", "issue_ids", "summary"}, "group")
        group_label = _require_non_empty_string(
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
        selected_issues = [issue_by_id[issue_id] for issue_id in group["issue_ids"]]
        severities = {issue["severity"] for issue in selected_issues}
        if len(severities) != 1:
            raise SafeStop(
                "unsupported_summary_claim",
                "A controlled summary group cannot mix issue severities.",
            )
        severity = next(iter(severities))
        expected_label = f"{severity.title()}-severity verified issues"
        expected_text = " ".join(
            f"[{issue['issue_id']}] {issue['message']}" for issue in selected_issues
        )
        if group_label != expected_label or group_text != expected_text:
            raise SafeStop(
                "unsupported_summary_claim",
                "Group prose must be rendered only from verified issue identifiers "
                "and controlled rule messages.",
            )
    if len(grouped_ids) != len(set(grouped_ids)):
        raise SafeStop("duplicate_ai_issue_reference", "An issue is grouped twice.")
    if set(grouped_ids) != known_ids:
        raise SafeStop(
            "missing_ai_issue_reference",
            f"Summary omitted issue IDs {sorted(known_ids - set(grouped_ids))}.",
        )

    action_ids: list[str] = []
    covered_by_actions: list[str] = []
    if not isinstance(summary["review_actions"], list) or not summary["review_actions"]:
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
        if not isinstance(action["action_type"], str):
            raise SafeStop("summary_contract", "Review action_type must be text.")
        if action["action_type"] != "human_review":
            raise SafeStop("unsafe_action", "Only human_review actions are permitted.")
        if action["external_action"] is not False:
            raise SafeStop("external_action_blocked", "External action must be false.")
        instruction = _require_non_empty_string(
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
        if len(action["issue_ids"]) != 1:
            raise SafeStop(
                "unsafe_action",
                "Each controlled human-review action must identify exactly one issue.",
            )
        action_ids.append(action["action_id"])
        for issue_id in action["issue_ids"]:
            if issue_id not in known_ids:
                raise SafeStop(
                    "unknown_ai_issue_reference",
                    f"Review action contains unknown issue_id {issue_id}.",
                )
            covered_by_actions.append(issue_id)
            issue = issue_by_id[issue_id]
            expected_instruction = (
                f"Review field {issue['field']} in synthetic source row "
                f"{issue['source_row']}; do not perform an external action."
            )
            if instruction != expected_instruction:
                raise SafeStop(
                    "unsafe_action",
                    "Review instructions must use the controlled no-external-action "
                    "template.",
                )
    if len(action_ids) != len(set(action_ids)):
        raise SafeStop("summary_contract", "Review action IDs are not unique.")
    if len(covered_by_actions) != len(set(covered_by_actions)):
        raise SafeStop("summary_contract", "An issue has duplicate review actions.")
    if set(covered_by_actions) != known_ids:
        raise SafeStop(
            "summary_contract",
            "Every verified issue needs exactly one source-linked review action.",
        )
    # Generated summaries are safe by construction: every accepted prose field
    # is an exact controlled template or a deterministic rule message. Learner
    # candidates use this same bounded contract. No substring matching against
    # source prose is used, so ordinary words and short tokens cannot cause
    # false positives.


def _decision_id(approval_without_id: dict[str, Any]) -> str:
    return "DEC-" + sha256_bytes(canonical_bytes(approval_without_id))[:12].upper()


def validate_approval(approval: Any) -> tuple[datetime, datetime]:
    """Validate and locally fingerprint every material decision field."""

    _require_exact_keys(approval, APPROVAL_FIELDS, "approval")
    if not isinstance(approval["decision_id"], str) or not re.fullmatch(
        r"DEC-[A-F0-9]{12}",
        approval["decision_id"],
    ):
        raise SafeStop("approval_contract", "Approval decision_id is invalid.")
    _require_run_id(approval["run_id"], "Approval run_id", "approval_contract")
    _require_non_empty_string(
        approval["reviewer_role"],
        "Approval reviewer_role",
        "approval_contract",
    )
    if (
        not isinstance(approval["decision"], str)
        or approval["decision"] not in DECISIONS
    ):
        raise SafeStop("approval_contract", "Approval decision is invalid.")
    if type(approval["draft_revision"]) is not int or approval["draft_revision"] < 1:
        raise SafeStop(
            "approval_contract",
            "Approval draft_revision must be an integer of at least 1.",
        )
    _require_sha256(
        approval["draft_sha256"],
        "Approval draft_sha256",
        "approval_contract",
    )
    _require_sha256(
        approval["review_manifest_sha256"],
        "Approval review_manifest_sha256",
        "approval_contract",
    )
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
    expected_decision_id = _decision_id(
        {field: approval[field] for field in sorted(APPROVAL_FIELDS - {"decision_id"})}
    )
    if approval["decision_id"] != expected_decision_id:
        raise SafeStop(
            "decision_integrity_mismatch",
            "Decision fields no longer match decision_id. This is local tamper "
            "detection, not identity authentication.",
        )
    return decided_at, expires_at


def validate_run_config(config: Any) -> None:
    _require_exact_keys(config, RUN_CONFIG_FIELDS, "run configuration")
    if config["schema_version"] != RUN_CONFIG_SCHEMA_VERSION:
        raise SafeStop("run_config_contract", "Run configuration version is invalid.")
    _require_sha256(
        config["input_sha256"],
        "Run configuration input_sha256",
        "run_config_contract",
    )
    try:
        configured_date = date.fromisoformat(config["assessment_date"])
    except (TypeError, ValueError) as error:
        raise SafeStop(
            "run_config_contract",
            "Run configuration assessment_date is invalid.",
        ) from error
    if configured_date.isoformat() != config["assessment_date"]:
        raise SafeStop(
            "run_config_contract",
            "Run configuration assessment_date is not canonical.",
        )
    for field in (
        "pipeline_version",
        "rules_version",
        "prompt_version",
        "mock_generator_version",
        "fallback_generator_version",
    ):
        _require_non_empty_string(
            config[field],
            f"Run configuration {field}",
            "run_config_contract",
        )
    if (
        not isinstance(config["requested_adapter_mode"], str)
        or config["requested_adapter_mode"] not in AI_MODES
    ):
        raise SafeStop(
            "run_config_contract",
            "Run configuration requested_adapter_mode is invalid.",
        )
    if not isinstance(config["expected_oracle_present"], bool):
        raise SafeStop(
            "run_config_contract",
            "Run configuration expected_oracle_present must be boolean.",
        )
    oracle_hash = config["expected_oracle_sha256"]
    if config["expected_oracle_present"]:
        _require_sha256(
            oracle_hash,
            "Run configuration expected_oracle_sha256",
            "run_config_contract",
        )
    elif oracle_hash is not None:
        raise SafeStop(
            "run_config_contract",
            "Absent expected oracle must have a null hash.",
        )


def _run_config_hash(config: dict[str, Any]) -> str:
    validate_run_config(config)
    return sha256_bytes(canonical_bytes(config))


def _run_id_from_config(config: dict[str, Any]) -> str:
    return "RUN-" + _run_config_hash(config)[:12].upper()


def validate_state(state: Any) -> None:
    _require_exact_keys(state, STATE_FIELDS, "state")
    _require_run_id(state["run_id"], "State run_id", "state_contract")
    for field in ("run_config_sha256", "input_sha256"):
        _require_sha256(state[field], f"State {field}", "state_contract")
    try:
        state_date = date.fromisoformat(state["assessment_date"])
    except (TypeError, ValueError) as error:
        raise SafeStop("state_contract", "State assessment_date is invalid.") from error
    if state_date.isoformat() != state["assessment_date"]:
        raise SafeStop("state_contract", "State assessment_date is not canonical.")
    for field in ("pipeline_version", "rules_version", "prompt_version"):
        _require_non_empty_string(state[field], f"State {field}", "state_contract")
    if (
        not isinstance(state["current_state"], str)
        or state["current_state"] not in PERSISTED_STATES
    ):
        raise SafeStop("state_contract", "State current_state is invalid.")
    if type(state["draft_revision"]) is not int or state["draft_revision"] < 0:
        raise SafeStop("state_contract", "State draft_revision is invalid.")
    if state["draft_sha256"] is not None:
        _require_sha256(
            state["draft_sha256"],
            "State draft_sha256",
            "state_contract",
        )
    if state["review_manifest_sha256"] is not None:
        _require_sha256(
            state["review_manifest_sha256"],
            "State review_manifest_sha256",
            "state_contract",
        )
    active_path = state["active_decision_path"]
    if active_path is not None and (
        not isinstance(active_path, str)
        or not re.fullmatch(r"review/decision-r[1-9][0-9]*\.json", active_path)
    ):
        raise SafeStop("state_contract", "State active_decision_path is invalid.")
    if (
        not isinstance(state["ai_mode_requested"], str)
        or state["ai_mode_requested"] not in AI_MODES
    ):
        raise SafeStop("state_contract", "State ai_mode_requested is invalid.")
    if state["summary_generator"] is not None and (
        not isinstance(state["summary_generator"], str)
        or state["summary_generator"] not in {"offline-mock", "deterministic-fallback"}
    ):
        raise SafeStop("state_contract", "State summary_generator is invalid.")
    if state["summary_fallback_reason"] is not None and not isinstance(
        state["summary_fallback_reason"],
        str,
    ):
        raise SafeStop("state_contract", "State fallback reason is invalid.")
    if type(state["external_actions"]) is not int or state["external_actions"] != 0:
        raise SafeStop("external_action_blocked", "State external_actions must be 0.")
    if type(state["local_export_count"]) is not int or state[
        "local_export_count"
    ] not in {0, 2}:
        raise SafeStop("state_contract", "State local_export_count must be 0 or 2.")
    expected_keys = state["expected_keys"]
    if expected_keys is not None:
        if not isinstance(expected_keys, list):
            raise SafeStop("state_contract", "State expected_keys must be a list.")
        normalized: list[tuple[str, str, str]] = []
        for value in expected_keys:
            if (
                not isinstance(value, list)
                or len(value) != 3
                or not all(isinstance(item, str) for item in value)
            ):
                raise SafeStop("state_contract", "State expected key is invalid.")
            normalized.append(tuple(value))
        if len(normalized) != len(set(normalized)):
            raise SafeStop("state_contract", "State expected keys are not unique.")
    if state["current_state"] == "no_action_needed":
        if any(
            (
                state["draft_revision"] != 0,
                state["draft_sha256"] is not None,
                state["review_manifest_sha256"] is not None,
                state["summary_generator"] is not None,
                state["active_decision_path"] is not None,
            )
        ):
            raise SafeStop("state_contract", "No-action state contains draft data.")
    else:
        if (
            state["draft_revision"] < 1
            or state["draft_sha256"] is None
            or state["review_manifest_sha256"] is None
            or state["summary_generator"] is None
        ):
            raise SafeStop(
                "state_contract",
                "Issue-bearing state is missing controlled draft evidence.",
            )
    if state["current_state"] == "needs_review" and active_path is not None:
        raise SafeStop(
            "state_contract",
            "Needs-review state cannot have an active decision.",
        )
    if (
        state["current_state"]
        in (
            TERMINAL_NON_EXPORT_STATES | {"approved_for_local_export", "approved_draft"}
        )
        and active_path is None
    ):
        raise SafeStop(
            "state_contract",
            "Decision state is missing its active decision path.",
        )
    if active_path is not None and active_path != (
        f"review/decision-r{state['draft_revision']}.json"
    ):
        raise SafeStop(
            "state_contract",
            "State active decision path does not match the current revision.",
        )
    if state["current_state"] == "approved_draft":
        if state["local_export_count"] != 2:
            raise SafeStop(
                "state_contract",
                "Approved-draft state must identify the complete two-file export.",
            )
    elif state["local_export_count"] != 0:
        raise SafeStop(
            "state_contract",
            "Only approved-draft state may identify local export files.",
        )


def validate_control(control: Any) -> None:
    if not isinstance(control, dict) or canonical_bytes(control) != canonical_bytes(
        CONTROL
    ):
        raise SafeStop(
            "external_action_blocked",
            "Control must explicitly allow only synthetic local drafts with "
            "EXTERNAL_ACTIONS_ENABLED=false.",
        )


def validate_review_package(
    package: Any,
    *,
    run_id: str,
    draft_revision: int,
    draft_sha256: str,
    issue_count: int,
) -> None:
    _require_exact_keys(package, REVIEW_PACKAGE_FIELDS, "review package")
    if (
        type(package["draft_revision"]) is not int
        or type(package["issue_count"]) is not int
    ):
        raise SafeStop(
            "review_package_contract",
            "Review package revision and issue count must be integers.",
        )
    if package["run_id"] != run_id:
        raise SafeStop("review_package_contract", "Review package run_id differs.")
    if package["draft_revision"] != draft_revision:
        raise SafeStop(
            "review_package_contract",
            "Review package draft revision differs.",
        )
    if package["draft_sha256"] != draft_sha256:
        raise SafeStop("review_package_contract", "Review package draft hash differs.")
    if package["issue_count"] != issue_count:
        raise SafeStop("review_package_contract", "Review package issue count differs.")
    expected_paths = {
        "issues_json_path": PROTECTED_REVIEW_ARTIFACTS["issues_json"],
        "issues_csv_path": PROTECTED_REVIEW_ARTIFACTS["issues_csv"],
        "source_path": PROTECTED_REVIEW_ARTIFACTS["source"],
        "summary_path": PROTECTED_REVIEW_ARTIFACTS["summary"],
        "control_path": PROTECTED_REVIEW_ARTIFACTS["control"],
        "run_config_path": PROTECTED_REVIEW_ARTIFACTS["run_config"],
        "review_manifest_path": "review/review_manifest.json",
    }
    if any(package[field] != value for field, value in expected_paths.items()):
        raise SafeStop(
            "review_package_contract",
            "Review package contains a non-canonical artifact path.",
        )
    if (
        not isinstance(package["reviewer_must_check"], list)
        or len(package["reviewer_must_check"]) < 4
        or any(
            not isinstance(item, str) or not item.strip()
            for item in package["reviewer_must_check"]
        )
    ):
        raise SafeStop(
            "review_package_contract",
            "Review package checklist is invalid.",
        )
    if package["allowed_decisions"] != ["approve", "edit", "reject", "expire"]:
        raise SafeStop(
            "review_package_contract",
            "Review package decisions are invalid.",
        )
    if type(package["external_actions"]) is not int or package["external_actions"] != 0:
        raise SafeStop(
            "external_action_blocked",
            "Review package external_actions must be 0.",
        )


def validate_review_manifest(
    manifest: Any,
    *,
    run_id: str,
    draft_revision: int,
    run_config: dict[str, Any],
) -> None:
    required = {
        "schema_version",
        "run_id",
        "draft_revision",
        "run_config_sha256",
        "configuration",
        "artifact_sha256",
    }
    _require_exact_keys(manifest, required, "review manifest")
    if type(manifest["draft_revision"]) is not int or manifest["draft_revision"] < 1:
        raise SafeStop(
            "review_manifest_contract",
            "Review manifest draft revision must be an integer.",
        )
    if manifest["schema_version"] != REVIEW_MANIFEST_SCHEMA_VERSION:
        raise SafeStop(
            "review_manifest_contract", "Review manifest version is invalid."
        )
    if manifest["run_id"] != run_id or manifest["draft_revision"] != draft_revision:
        raise SafeStop(
            "review_manifest_contract",
            "Review manifest identifies a different run or revision.",
        )
    expected_config_hash = _run_config_hash(run_config)
    if manifest["run_config_sha256"] != expected_config_hash:
        raise SafeStop(
            "review_manifest_contract",
            "Review manifest configuration hash differs.",
        )
    configuration = manifest["configuration"]
    expected_configuration = {
        "assessment_date": run_config["assessment_date"],
        "pipeline_version": run_config["pipeline_version"],
        "rules_version": run_config["rules_version"],
        "prompt_version": run_config["prompt_version"],
        "requested_adapter_mode": run_config["requested_adapter_mode"],
        "mock_generator_version": run_config["mock_generator_version"],
        "fallback_generator_version": run_config["fallback_generator_version"],
        "expected_oracle_present": run_config["expected_oracle_present"],
        "expected_oracle_sha256": run_config["expected_oracle_sha256"],
    }
    if not isinstance(configuration, dict) or canonical_bytes(
        configuration
    ) != canonical_bytes(expected_configuration):
        raise SafeStop(
            "review_manifest_contract",
            "Review manifest configuration values differ.",
        )
    artifact_hashes = manifest["artifact_sha256"]
    if not isinstance(artifact_hashes, dict) or set(artifact_hashes) != set(
        PROTECTED_REVIEW_ARTIFACTS.values()
    ):
        raise SafeStop(
            "review_manifest_contract",
            "Review manifest protected artifact set differs.",
        )
    for path, digest in artifact_hashes.items():
        _require_sha256(
            digest,
            f"Review manifest hash for {path}",
            "review_manifest_contract",
        )


def _review_package(
    run_id: str,
    draft_revision: int,
    draft_sha256: str,
    issue_count: int,
) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "draft_revision": draft_revision,
        "draft_sha256": draft_sha256,
        "issue_count": issue_count,
        "issues_json_path": PROTECTED_REVIEW_ARTIFACTS["issues_json"],
        "issues_csv_path": PROTECTED_REVIEW_ARTIFACTS["issues_csv"],
        "source_path": PROTECTED_REVIEW_ARTIFACTS["source"],
        "summary_path": PROTECTED_REVIEW_ARTIFACTS["summary"],
        "control_path": PROTECTED_REVIEW_ARTIFACTS["control"],
        "run_config_path": PROTECTED_REVIEW_ARTIFACTS["run_config"],
        "review_manifest_path": "review/review_manifest.json",
        "reviewer_must_check": [
            "Every issue against the named synthetic source row and field.",
            "The JSON and spreadsheet-safe CSV issue registers contain the same issues.",
            "Every summary sentence against its visible issue identifiers.",
            "Every proposed action is human_review with external_action false.",
            "The exact protected review-manifest hash and revision before deciding.",
        ],
        "allowed_decisions": ["approve", "edit", "reject", "expire"],
        "external_actions": 0,
    }


def _build_review_manifest(
    run_dir: Path,
    run_id: str,
    draft_revision: int,
    run_config: dict[str, Any],
) -> dict[str, Any]:
    artifact_hashes: dict[str, str] = {}
    for relative_path in PROTECTED_REVIEW_ARTIFACTS.values():
        path = run_dir / relative_path
        if relative_path == PROTECTED_REVIEW_ARTIFACTS["source"]:
            max_bytes = MAX_WORK_ITEM_CSV_BYTES
        elif relative_path == PROTECTED_REVIEW_ARTIFACTS["expected_oracle"]:
            max_bytes = MAX_EXPECTED_CSV_BYTES
        else:
            max_bytes = MAX_JSON_BYTES
        artifact_hashes[relative_path] = sha256_bytes(
            _read_regular_bytes(
                path,
                f"protected review artifact {relative_path}",
                max_bytes=max_bytes,
            )
        )
    manifest = {
        "schema_version": REVIEW_MANIFEST_SCHEMA_VERSION,
        "run_id": run_id,
        "draft_revision": draft_revision,
        "run_config_sha256": _run_config_hash(run_config),
        "configuration": {
            "assessment_date": run_config["assessment_date"],
            "pipeline_version": run_config["pipeline_version"],
            "rules_version": run_config["rules_version"],
            "prompt_version": run_config["prompt_version"],
            "requested_adapter_mode": run_config["requested_adapter_mode"],
            "mock_generator_version": run_config["mock_generator_version"],
            "fallback_generator_version": run_config["fallback_generator_version"],
            "expected_oracle_present": run_config["expected_oracle_present"],
            "expected_oracle_sha256": run_config["expected_oracle_sha256"],
        },
        "artifact_sha256": artifact_hashes,
    }
    validate_review_manifest(
        manifest,
        run_id=run_id,
        draft_revision=draft_revision,
        run_config=run_config,
    )
    return manifest


def _review_manifest_hash(manifest: dict[str, Any]) -> str:
    return sha256_bytes(canonical_bytes(manifest))


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
            raise SafeStop(
                "malformed_ai_json", "The simulated AI JSON is malformed."
            ) from error
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
    if not isinstance(mode, str) or mode not in AI_MODES:
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
    occurred_at: str,
    actor_type: str,
    details: dict[str, Any],
) -> str:
    seed = canonical_bytes(
        {
            "run_id": run_id,
            "event_type": event_type,
            "state": state,
            "occurred_at": occurred_at,
            "actor_type": actor_type,
            "details": details,
        }
    )
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
    audit_path = run_dir / "audit" / "events.jsonl"
    existing = _load_audit_events(audit_path, expected_run_id=run_id)
    occurred = occurred_at or utc_now()
    if existing:
        latest = parse_datetime(existing[-1]["occurred_at"], "occurred_at")
        if occurred_at is None and occurred <= latest:
            occurred = latest + timedelta(microseconds=1)
        elif occurred <= latest:
            raise SafeStop(
                "audit_history_mismatch",
                "The new audit event must be dated after the latest controlled event.",
            )
    occurred_at_text = iso_utc(occurred)
    event = {
        "event_id": _event_id(
            run_id,
            event_type,
            state,
            occurred_at_text,
            actor_type,
            details,
        ),
        "run_id": run_id,
        "event_type": event_type,
        "state": state,
        "occurred_at": occurred_at_text,
        "actor_type": actor_type,
        "details": details,
    }
    validate_audit_event(event)
    if event["event_id"] not in {item["event_id"] for item in existing}:
        candidate_events = [*existing, event]
        if len(candidate_events) > MAX_AUDIT_EVENTS:
            raise SafeStop(
                "audit_limit_exceeded",
                f"Audit history exceeds the supported {MAX_AUDIT_EVENTS}-event limit.",
            )
        rendered_lines = [
            json.dumps(
                item,
                ensure_ascii=False,
                sort_keys=True,
                allow_nan=False,
            )
            + "\n"
            for item in candidate_events
        ]
        if any(len(line.encode("utf-8")) > MAX_AUDIT_LINE_BYTES for line in rendered_lines):
            raise SafeStop(
                "audit_limit_exceeded",
                "An audit event exceeds the supported 256 KiB line limit.",
            )
        encoded = "".join(rendered_lines).encode("utf-8")
        if len(encoded) > MAX_AUDIT_BYTES:
            raise SafeStop(
                "audit_limit_exceeded",
                "Audit history exceeds the supported 16 MiB limit.",
            )
        try:
            atomic_write_bytes(audit_path, encoded)
        except SafeStop as error:
            raise SafeStop(
                "audit_write_error",
                "Could not atomically persist the controlled audit event.",
            ) from error
    return event


def _positive_int(value: Any) -> bool:
    return type(value) is int and value > 0


def _validate_audit_details(event_type: str, state: str, details: Any) -> None:
    contract = AUDIT_EVENT_CONTRACTS.get(event_type)
    if contract is None:
        raise SafeStop(
            "invalid_audit_event",
            "Audit event_type is outside the closed Course 1 vocabulary.",
        )
    allowed_states, _, required_details = contract
    if state not in allowed_states:
        raise SafeStop(
            "invalid_audit_event",
            "Audit event_type is not permitted in the recorded state.",
        )
    _require_exact_keys(details, required_details, f"{event_type} audit details")

    def hash_field(name: str) -> bool:
        return isinstance(details[name], str) and bool(
            re.fullmatch(r"[a-f0-9]{64}", details[name])
        )

    if event_type == "run_received":
        valid = (
            hash_field("input_sha256")
            and hash_field("run_config_sha256")
            and details["dataset_kind"] == "synthetic"
        )
    elif event_type == "input_validated":
        valid = (
            _positive_int(details["row_count"])
            and details["row_count"] <= MAX_WORK_ITEM_ROWS
            and details["header_count"] == len(HEADERS)
        )
    elif event_type == "no_verified_issues":
        valid = (
            type(details["issue_count"]) is int
            and details["issue_count"] == 0
            and type(details["external_actions"]) is int
            and details["external_actions"] == 0
        )
    elif event_type == "issues_created":
        valid = (
            _positive_int(details["issue_count"])
            and details["identity_fields"]
            == ["work_item_id", "rule_code", "field"]
        )
    elif event_type == "summary_fallback":
        valid = (
            details["reason"]
            in {
                "ai_disabled",
                "ai_timeout",
                "ai_refusal",
                "malformed_ai_json",
                "unknown_ai_issue_reference",
            }
            and details["generator"] == "deterministic-fallback"
        )
    elif event_type == "mock_summary_validated":
        valid = (
            details["generator"] == "offline-mock"
            and _positive_int(details["issue_reference_count"])
        )
    elif event_type == "human_review_required":
        valid = (
            details["draft_revision"] == 1
            and hash_field("draft_sha256")
            and hash_field("review_manifest_sha256")
        )
    elif event_type == "duplicate_retry_ignored":
        valid = (
            hash_field("input_sha256")
            and hash_field("run_config_sha256")
            and details["no_duplicate_effect"] is True
        )
    elif event_type == "review_decision_recorded":
        decision_state = {
            "approve": "approved_for_local_export",
            "edit": "changes_requested",
            "reject": "rejected",
            "expire": "expired",
        }
        valid = (
            isinstance(details["decision_id"], str)
            and bool(re.fullmatch(r"DEC-[A-F0-9]{12}", details["decision_id"]))
            and details["decision"] in decision_state
            and state == decision_state.get(details["decision"])
            and _positive_int(details["draft_revision"])
            and hash_field("draft_sha256")
            and hash_field("review_manifest_sha256")
            and type(details["evidence_reviewed"]) is bool
            and details["integrity_scope"]
            == "local_tamper_detection_not_authentication"
        )
    elif event_type == "draft_revision_created":
        valid = (
            _positive_int(details["previous_revision"])
            and details["draft_revision"] == details["previous_revision"] + 1
            and hash_field("previous_sha256")
            and hash_field("draft_sha256")
            and hash_field("review_manifest_sha256")
        )
    elif event_type == "candidate_summary_validated":
        valid = (
            hash_field("candidate_sha256")
            and _positive_int(details["draft_revision"])
            and _positive_int(details["issue_reference_count"])
            and details["prose_support_status"] == "controlled_templates_only"
            and details["human_support_review_required"] is True
        )
    elif event_type == "local_export_created":
        revision = details["draft_revision"]
        valid = (
            isinstance(details["decision_id"], str)
            and bool(re.fullmatch(r"DEC-[A-F0-9]{12}", details["decision_id"]))
            and _positive_int(revision)
            and details["files"]
            == [f"approved-r{revision}.json", f"approved-r{revision}.csv"]
            and type(details["external_actions"]) is int
            and details["external_actions"] == 0
        )
    elif event_type == "review_expired":
        valid = (
            isinstance(details["decision_id"], str)
            and bool(re.fullmatch(r"DEC-[A-F0-9]{12}", details["decision_id"]))
            and _positive_int(details["draft_revision"])
        )
    else:
        valid = (
            isinstance(details["attempt_id"], str)
            and bool(re.fullmatch(r"A[0-9]{4,}", details["attempt_id"]))
            and isinstance(details["error_code"], str)
            and bool(re.fullmatch(r"[a-z][a-z0-9_]{0,63}", details["error_code"]))
            and details["command"]
            in {"prepare", "decide", "revise", "validate-summary", "export", "status"}
            and type(details["external_actions"]) is int
            and details["external_actions"] == 0
        )
    if not valid:
        raise SafeStop(
            "invalid_audit_event",
            f"{event_type} audit details do not match the closed event contract.",
        )


def validate_audit_event(
    event: dict[str, Any],
    expected_run_id: str | None = None,
) -> None:
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
    if not isinstance(event["event_id"], str) or not re.fullmatch(
        r"EVT-[A-F0-9]{16}",
        event["event_id"],
    ):
        raise SafeStop("invalid_audit_event", "Audit event_id is invalid.")
    _require_run_id(event["run_id"], "Audit run_id", "invalid_audit_event")
    if expected_run_id is not None and event["run_id"] != expected_run_id:
        raise SafeStop("invalid_audit_event", "Audit event belongs to another run.")
    if not isinstance(event["event_type"], str):
        raise SafeStop("invalid_audit_event", "Audit event_type is invalid.")
    contract = AUDIT_EVENT_CONTRACTS.get(event["event_type"])
    if contract is None:
        raise SafeStop(
            "invalid_audit_event",
            "Audit event_type is outside the closed Course 1 vocabulary.",
        )
    if not isinstance(event["state"], str) or event["state"] not in WORKFLOW_STATES:
        raise SafeStop("invalid_audit_event", "Audit state is invalid.")
    if (
        not isinstance(event["actor_type"], str)
        or event["actor_type"] != contract[1]
    ):
        raise SafeStop("invalid_audit_event", "Audit actor_type is invalid.")
    parse_datetime(event["occurred_at"], "occurred_at")
    if not isinstance(event["details"], dict):
        raise SafeStop("invalid_audit_event", "Audit details must be an object.")
    expected_id = _event_id(
        event["run_id"],
        event["event_type"],
        event["state"],
        event["occurred_at"],
        event["actor_type"],
        event["details"],
    )
    if event["event_id"] != expected_id:
        raise SafeStop(
            "audit_integrity_mismatch",
            "Audit event fields no longer match event_id.",
        )
    _validate_audit_details(
        event["event_type"],
        event["state"],
        event["details"],
    )


def _load_audit_events(
    path: Path,
    *,
    expected_run_id: str | None = None,
) -> list[dict[str, Any]]:
    _validate_supported_path(path, "Audit file")
    if not path.exists():
        return []
    encoded = _read_regular_bytes(
        path,
        "audit file",
        max_bytes=MAX_AUDIT_BYTES,
    )
    text = _decode_utf8(encoded, "Audit file", code="audit_corrupt")
    lines = text.splitlines()
    events: list[dict[str, Any]] = []
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        if len(line.encode("utf-8")) > MAX_AUDIT_LINE_BYTES:
            raise SafeStop(
                "audit_limit_exceeded",
                f"Audit line {line_number} exceeds the supported 256 KiB limit.",
            )
        try:
            event = json.loads(
                line,
                object_pairs_hook=_json_object_without_duplicates,
                parse_constant=lambda _: (_ for _ in ()).throw(
                    SafeStop(
                        "audit_corrupt",
                        f"Audit line {line_number} contains an invalid JSON value.",
                    )
                ),
            )
        except json.JSONDecodeError as error:
            raise SafeStop(
                "audit_corrupt",
                f"Audit line {line_number} is not valid JSON.",
            ) from error
        validate_audit_event(event, expected_run_id)
        if events and parse_datetime(
            event["occurred_at"], "occurred_at"
        ) <= parse_datetime(events[-1]["occurred_at"], "occurred_at"):
            raise SafeStop(
                "audit_history_mismatch",
                "Audit event dates are not strictly increasing in the controlled history.",
            )
        events.append(event)
        if len(events) > MAX_AUDIT_EVENTS:
            raise SafeStop(
                "audit_limit_exceeded",
                f"Audit history exceeds the supported {MAX_AUDIT_EVENTS}-event limit.",
            )
    if len({event["event_id"] for event in events}) != len(events):
        raise SafeStop("audit_corrupt", "Audit event identifiers are duplicated.")
    return events


def _write_issues_csv(path: Path, issues: list[dict[str, Any]]) -> None:
    atomic_write_bytes(path, _csv_bytes(issues, ISSUE_FIELDS))


def _read_expected_oracle(
    path: Path | None,
) -> tuple[set[tuple[str, str, str]] | None, str | None, bytes]:
    if path is None:
        return None, None, EXPECTED_ORACLE_ABSENT_BYTES
    oracle_bytes = _read_regular_bytes(
        path,
        f"expected-issues file {path.name}",
        max_bytes=MAX_EXPECTED_CSV_BYTES,
    )
    return (
        _parse_expected_oracle_bytes(oracle_bytes),
        sha256_bytes(oracle_bytes),
        oracle_bytes,
    )


def _parse_expected_oracle_bytes(
    oracle_bytes: bytes,
) -> set[tuple[str, str, str]]:
    if len(oracle_bytes) > MAX_EXPECTED_CSV_BYTES:
        raise SafeStop(
            "input_limit_exceeded",
            "Expected-issues CSV is larger than the supported 2 MiB limit.",
        )
    text = _decode_utf8(
        oracle_bytes,
        "Expected-issues CSV",
        code="malformed_input",
    )
    try:
        reader = csv.DictReader(io.StringIO(text, newline=""), strict=True)
        expected_headers = [
            "issue_id",
            "work_item_id",
            "field",
            "rule_code",
            "severity",
            "expected_message",
        ]
        if reader.fieldnames != expected_headers:
            raise SafeStop(
                "expected_contract",
                "Expected-issues CSV must use the exact six published headers.",
            )
        rows: list[dict[str, str]] = []
        for row in reader:
            if len(rows) >= MAX_EXPECTED_ROWS:
                raise SafeStop(
                    "input_limit_exceeded",
                    f"Expected-issues CSV contains more than {MAX_EXPECTED_ROWS} rows.",
                )
            rows.append(row)
    except csv.Error as error:
        raise SafeStop(
            "malformed_input", f"Expected-issues CSV is malformed: {error}"
        ) from error
    if not rows:
        raise SafeStop(
            "expected_contract",
            "Expected-issues CSV must contain at least one expected issue.",
        )
    for row_number, row in enumerate(rows, start=2):
        if None in row or any(value is None for value in row.values()):
            raise SafeStop(
                "expected_contract",
                f"Expected-issues row {row_number} does not have exactly six values.",
            )
        for field_name, value in row.items():
            if len(value) > MAX_CSV_CELL_CODE_POINTS:
                raise SafeStop(
                    "input_limit_exceeded",
                    f"Expected-issues row {row_number} field {field_name} exceeds the cell limit.",
                )
        work_item_id = row["work_item_id"]
        rule_code = row["rule_code"]
        field_name = row["field"]
        _reject_bidi_controls(work_item_id, "Expected work-item identifier")
        _reject_bidi_controls(rule_code, "Expected rule code")
        _reject_bidi_controls(field_name, "Expected field")
        if not re.fullmatch(r"WI-[0-9]{4}", work_item_id):
            raise SafeStop(
                "expected_contract",
                f"Expected-issues row {row_number} has an invalid work_item_id.",
            )
        if not re.fullmatch(r"R(?:00[1-9]|01[01])", rule_code):
            raise SafeStop(
                "expected_contract",
                f"Expected-issues row {row_number} has an invalid rule_code.",
            )
        if field_name not in HEADERS:
            raise SafeStop(
                "expected_contract",
                f"Expected-issues row {row_number} has an unknown field.",
            )
        if row["issue_id"] != f"{work_item_id}|{rule_code}|{field_name}":
            raise SafeStop(
                "expected_contract",
                f"Expected-issues row {row_number} has an inconsistent issue_id.",
            )
        if row["severity"] not in {"medium", "high"} or not row[
            "expected_message"
        ].strip():
            raise SafeStop(
                "expected_contract",
                f"Expected-issues row {row_number} has invalid expected evidence.",
            )
    keys = {(row["work_item_id"], row["rule_code"], row["field"]) for row in rows}
    if len(keys) != len(rows):
        raise SafeStop("expected_contract", "Expected issue keys are not unique.")
    return keys


def _expected_keys_from_run_evidence(
    run_dir: Path,
    run_config: dict[str, Any],
) -> set[tuple[str, str, str]] | None:
    evidence_bytes = _read_bytes(
        run_dir / EXPECTED_ORACLE_EVIDENCE_PATH,
        "protected expected-issue evidence",
    )
    if run_config["expected_oracle_present"]:
        if sha256_bytes(evidence_bytes) != run_config["expected_oracle_sha256"]:
            raise SafeStop(
                "expected_oracle_integrity_mismatch",
                "Protected expected-issue evidence differs from the run identity.",
            )
        return _parse_expected_oracle_bytes(evidence_bytes)
    if (
        run_config["expected_oracle_sha256"] is not None
        or evidence_bytes != EXPECTED_ORACLE_ABSENT_BYTES
    ):
        raise SafeStop(
            "expected_oracle_integrity_mismatch",
            "The run identity says no expected-issue oracle was supplied, but "
            "protected evidence disagrees.",
        )
    return None


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
    evaluation = {
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
    validate_evaluation(evaluation)
    return evaluation


def validate_evaluation(evaluation: Any) -> None:
    required = {
        "run_id",
        "dataset_kind",
        "expected_issue_count",
        "detected_issue_count",
        "true_positives",
        "false_positives",
        "false_negatives",
        "correct_issue_references",
        "unsupported_ai_claims",
        "summary_fallback_used",
        "duplicate_retry_safe",
        "external_actions",
        "current_state",
        "course1_recommendation",
        "recommendation_reason",
    }
    _require_exact_keys(evaluation, required, "evaluation")
    _require_run_id(
        evaluation["run_id"],
        "Evaluation run_id",
        "evaluation_contract",
    )
    if (
        not isinstance(evaluation["dataset_kind"], str)
        or evaluation["dataset_kind"] != "synthetic"
    ):
        raise SafeStop("evaluation_contract", "Evaluation dataset_kind is invalid.")
    for field in (
        "expected_issue_count",
        "true_positives",
        "false_positives",
        "false_negatives",
    ):
        value = evaluation[field]
        if value is not None and (type(value) is not int or value < 0):
            raise SafeStop("evaluation_contract", f"Evaluation {field} is invalid.")
    for field in (
        "detected_issue_count",
        "correct_issue_references",
        "unsupported_ai_claims",
    ):
        if type(evaluation[field]) is not int or evaluation[field] < 0:
            raise SafeStop("evaluation_contract", f"Evaluation {field} is invalid.")
    if not isinstance(evaluation["summary_fallback_used"], bool):
        raise SafeStop(
            "evaluation_contract",
            "Evaluation summary_fallback_used is invalid.",
        )
    if (
        type(evaluation["duplicate_retry_safe"]) is not bool
        or evaluation["duplicate_retry_safe"] is not True
    ):
        raise SafeStop("evaluation_contract", "Evaluation retry control is invalid.")
    if (
        type(evaluation["external_actions"]) is not int
        or evaluation["external_actions"] != 0
    ):
        raise SafeStop(
            "external_action_blocked", "Evaluation external_actions must be 0."
        )
    if (
        not isinstance(evaluation["current_state"], str)
        or evaluation["current_state"] not in PERSISTED_STATES
    ):
        raise SafeStop("evaluation_contract", "Evaluation current_state is invalid.")
    if not isinstance(evaluation["course1_recommendation"], str) or evaluation[
        "course1_recommendation"
    ] not in {
        "ACCEPT FOR SYNTHETIC PORTFOLIO",
        "REWORK",
        "DO NOT CONTINUE",
    }:
        raise SafeStop("evaluation_contract", "Evaluation recommendation is invalid.")
    _require_non_empty_string(
        evaluation["recommendation_reason"],
        "Evaluation recommendation_reason",
        "evaluation_contract",
    )


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


def _create_staging_marker(staging_directory: Path) -> None:
    marker_path = staging_directory / STAGING_MARKER_NAME
    marker_bytes = canonical_bytes(
        {
            "format": STAGING_MARKER_FORMAT,
            "directory": staging_directory.name,
            "operation_id": uuid.uuid4().hex,
            "created_at": iso_utc(utc_now()),
        }
    )
    try:
        with marker_path.open("xb") as stream:
            stream.write(marker_bytes)
            stream.flush()
            os.fsync(stream.fileno())
    except OSError as error:
        try:
            marker_path.unlink(missing_ok=True)
            staging_directory.rmdir()
        except OSError:
            pass
        raise SafeStop(
            "staging_marker_error",
            "The private staging folder could not be ownership-marked. Nothing "
            "was published.",
        ) from error


def _validate_staging_marker(staging_directory: Path) -> dict[str, Any]:
    marker_path = staging_directory / STAGING_MARKER_NAME
    try:
        marker = read_json(marker_path)
        _require_exact_keys(
            marker,
            {"format", "directory", "operation_id", "created_at"},
            "staging ownership marker",
        )
    except SafeStop as error:
        raise SafeStop(
            "staging_ownership_mismatch",
            "A private staging folder has no valid Course 1 ownership marker. "
            "Nothing was removed.",
        ) from error
    if (
        marker["format"] != STAGING_MARKER_FORMAT
        or marker["directory"] != staging_directory.name
        or not isinstance(marker["operation_id"], str)
        or not re.fullmatch(r"[a-f0-9]{32}", marker["operation_id"])
    ):
        raise SafeStop(
            "staging_ownership_mismatch",
            "A private staging folder has no valid Course 1 ownership marker. "
            "Nothing was removed.",
        )
    parse_datetime(marker["created_at"], "staging created_at")
    return marker


def _remove_owned_staging_tree(path: Path, staging_root: Path) -> None:
    path_stat = path.lstat()
    if stat.S_ISLNK(path_stat.st_mode) or _path_has_reparse_attribute(path_stat):
        raise SafeStop(
            "staging_ownership_mismatch",
            "A private staging folder contains a link or reparse point. Nothing was removed.",
        )
    if stat.S_ISDIR(path_stat.st_mode):
        for child in path.iterdir():
            _remove_owned_staging_tree(child, staging_root)
        path.rmdir()
        return
    if stat.S_ISREG(path_stat.st_mode):
        path.unlink()
        return
    raise SafeStop(
        "staging_ownership_mismatch",
        "A private staging folder contains an unsupported file type. Nothing was removed.",
    )


def _discard_owned_staging_directory(staging_directory: Path) -> None:
    try:
        staging_directory.lstat()
    except FileNotFoundError:
        return
    except OSError as error:
        raise SafeStop(
            "staging_cleanup_error",
            "The private staging folder could not be safely inspected.",
        ) from error
    _validate_staging_marker(staging_directory)
    try:
        _remove_owned_staging_tree(staging_directory, staging_directory)
    except SafeStop:
        raise
    except OSError as error:
        raise SafeStop(
            "staging_cleanup_error",
            "The owned private staging folder could not be removed.",
        ) from error


def _cleanup_prepare_staging(workspace: Path) -> None:
    runs_root = workspace.absolute() / "runs"
    try:
        if not runs_root.exists():
            return
        root_stat = runs_root.lstat()
        if (
            not stat.S_ISDIR(root_stat.st_mode)
            or stat.S_ISLNK(root_stat.st_mode)
            or _path_has_reparse_attribute(root_stat)
        ):
            raise SafeStop(
                "staging_cleanup_error",
                "The controlled runs path is not an ordinary folder. Nothing was removed.",
            )
        for path in runs_root.iterdir():
            if not path.name.startswith(STAGING_PREFIX):
                continue
            path_stat = path.lstat()
            if (
                not stat.S_ISDIR(path_stat.st_mode)
                or stat.S_ISLNK(path_stat.st_mode)
                or _path_has_reparse_attribute(path_stat)
            ):
                raise SafeStop(
                    "staging_ownership_mismatch",
                    "A staging-like path is not an owned ordinary folder. Nothing was removed.",
                )
            _validate_staging_marker(path)
            _remove_owned_staging_tree(path, path)
    except SafeStop:
        raise
    except OSError as error:
        raise SafeStop(
            "staging_cleanup_error",
            "A private prepare staging folder could not be removed. Do not "
            "continue until it is inspected.",
        ) from error


def _publish_staged_run(
    staging_parent: Path,
    staged_run_dir: Path,
    final_run_dir: Path,
) -> None:
    _validate_staging_marker(staging_parent)
    _load_run(staged_run_dir)
    try:
        os.replace(staged_run_dir, final_run_dir)
        (staging_parent / STAGING_MARKER_NAME).unlink()
        staging_parent.rmdir()
    except OSError as error:
        raise SafeStop(
            "run_publish_error",
            "The fully validated run could not be atomically published.",
        ) from error


def _audit_matches(
    event: dict[str, Any],
    event_type: str,
    details: dict[str, Any],
) -> bool:
    return event["event_type"] == event_type and all(
        event["details"].get(key) == value for key, value in details.items()
    )


def _reconcile_safe_stop_history(
    run_dir: Path,
    events: list[dict[str, Any]],
    *,
    base_complete_index: int,
) -> None:
    safe_stop_positions = [
        index
        for index, event in enumerate(events)
        if event["event_type"] == "safe_stop_recorded"
    ]
    seen_attempts: set[str] = set()
    for index in safe_stop_positions:
        event = events[index]
        attempt_id = event["details"]["attempt_id"]
        if index <= base_complete_index or attempt_id in seen_attempts:
            raise SafeStop(
                "audit_history_mismatch",
                "Safe-stop audit evidence is duplicated or out of lifecycle order.",
            )
        seen_attempts.add(attempt_id)
        attempt_number = int(attempt_id[1:])
        history_path = run_dir / "failures" / f"a{attempt_number:04d}.json"
        failure = read_json(history_path)
        if (
            failure.get("attempt_id") != attempt_id
            or failure.get("error_code") != event["details"]["error_code"]
            or failure.get("command") != event["details"]["command"]
            or failure.get("state") != "failed_manual"
            or type(failure.get("external_actions")) is not int
            or failure.get("external_actions") != 0
            or failure.get("audit_recorded") is not True
            or failure.get("history_path")
            != f"failures/a{attempt_number:04d}.json"
        ):
            raise SafeStop(
                "audit_history_mismatch",
                "Safe-stop audit evidence differs from its controlled failure record.",
            )


def _reconcile_audit_history(
    run_dir: Path,
    state: dict[str, Any],
    issues: list[dict[str, Any]],
    events: list[dict[str, Any]],
    source_row_count: int,
) -> None:
    """Bind material audit history to the actual controlled lifecycle."""

    def positions(event_type: str) -> list[int]:
        return [
            index
            for index, event in enumerate(events)
            if event["event_type"] == event_type
        ]

    def one(event_type: str) -> int:
        found = positions(event_type)
        if len(found) != 1:
            raise SafeStop(
                "audit_history_mismatch",
                f"Material audit event {event_type} must occur exactly once.",
            )
        return found[0]

    def require_exact_event(
        index: int,
        *,
        event_type: str,
        event_state: str,
        actor_type: str,
        details: dict[str, Any],
    ) -> None:
        event = events[index]
        if (
            event["event_type"] != event_type
            or event["state"] != event_state
            or event["actor_type"] != actor_type
            or canonical_bytes(event["details"]) != canonical_bytes(details)
        ):
            raise SafeStop(
                "audit_history_mismatch",
                f"Material audit event {event_type} differs from controlled evidence.",
            )

    received = one("run_received")
    validated = one("input_validated")
    if received >= validated:
        raise SafeStop(
            "audit_history_mismatch",
            "Run receipt must precede input validation in the audit history.",
        )
    require_exact_event(
        received,
        event_type="run_received",
        event_state="received",
        actor_type="system",
        details={
            "input_sha256": state["input_sha256"],
            "run_config_sha256": state["run_config_sha256"],
            "dataset_kind": "synthetic",
        },
    )
    require_exact_event(
        validated,
        event_type="input_validated",
        event_state="validated",
        actor_type="system",
        details={
            "row_count": source_row_count,
            "header_count": len(HEADERS),
        },
    )

    duplicate_retry_positions = positions("duplicate_retry_ignored")
    if len(duplicate_retry_positions) > 1 or any(
        index <= validated for index in duplicate_retry_positions
    ):
        raise SafeStop(
            "audit_history_mismatch",
            "Duplicate-retry audit history is duplicated or out of order.",
        )
    for index in duplicate_retry_positions:
        event = events[index]
        if event["actor_type"] != "system" or canonical_bytes(
            event["details"]
        ) != canonical_bytes(
            {
                "input_sha256": state["input_sha256"],
                "run_config_sha256": state["run_config_sha256"],
                "no_duplicate_effect": True,
            }
        ):
            raise SafeStop(
                "audit_history_mismatch",
                "Duplicate-retry audit evidence differs from controlled state.",
            )

    material_decision_types = {
        "review_decision_recorded",
        "draft_revision_created",
        "local_export_created",
        "review_expired",
    }
    if state["current_state"] == "no_action_needed":
        no_issues = one("no_verified_issues")
        if validated >= no_issues or issues:
            raise SafeStop(
                "audit_history_mismatch",
                "No-action audit history conflicts with detected issues.",
            )
        if any(index <= no_issues for index in duplicate_retry_positions):
            raise SafeStop(
                "audit_history_mismatch",
                "Duplicate retry precedes completed no-action evidence.",
            )
        require_exact_event(
            no_issues,
            event_type="no_verified_issues",
            event_state="no_action_needed",
            actor_type="system",
            details={"issue_count": 0, "external_actions": 0},
        )
        if any(positions(event_type) for event_type in material_decision_types):
            raise SafeStop(
                "audit_history_mismatch",
                "No-action history contains an impossible review or export event.",
            )
        allowed_no_action = {
            "run_received",
            "input_validated",
            "no_verified_issues",
            "duplicate_retry_ignored",
            "safe_stop_recorded",
        }
        if any(event["event_type"] not in allowed_no_action for event in events):
            raise SafeStop(
                "audit_history_mismatch",
                "No-action history contains an event from the issue-review lifecycle.",
            )
        _reconcile_safe_stop_history(
            run_dir,
            events,
            base_complete_index=no_issues,
        )
        return

    if positions("no_verified_issues"):
        raise SafeStop(
            "audit_history_mismatch",
            "Issue-bearing history contains a contradictory no-action event.",
        )
    issues_created = one("issues_created")
    summary_event_type = (
        "summary_fallback"
        if state["summary_fallback_reason"] is not None
        else "mock_summary_validated"
    )
    other_summary_type = (
        "mock_summary_validated"
        if summary_event_type == "summary_fallback"
        else "summary_fallback"
    )
    summary_ready = one(summary_event_type)
    if positions(other_summary_type):
        raise SafeStop(
            "audit_history_mismatch",
            "Audit history contains conflicting summary-generation events.",
        )
    review_required = one("human_review_required")
    if not (validated < issues_created < summary_ready < review_required):
        raise SafeStop(
            "audit_history_mismatch",
            "Base issue, summary, and human-review events are out of order.",
        )
    if any(index <= review_required for index in duplicate_retry_positions):
        raise SafeStop(
            "audit_history_mismatch",
            "Duplicate retry precedes completed human-review evidence.",
        )
    require_exact_event(
        issues_created,
        event_type="issues_created",
        event_state="issues_ready",
        actor_type="system",
        details={
            "issue_count": len(issues),
            "identity_fields": ["work_item_id", "rule_code", "field"],
        },
    )
    if summary_event_type == "summary_fallback":
        summary_details = {
            "reason": state["summary_fallback_reason"],
            "generator": "deterministic-fallback",
        }
        summary_actor = "system"
    else:
        summary_details = {
            "generator": "offline-mock",
            "issue_reference_count": len(issues),
        }
        summary_actor = "mock_ai"
    require_exact_event(
        summary_ready,
        event_type=summary_event_type,
        event_state="summary_ready",
        actor_type=summary_actor,
        details=summary_details,
    )

    revision = state["draft_revision"]
    decision_paths: dict[int, Path] = {}
    review_dir = run_dir / "review"
    try:
        for path in review_dir.iterdir():
            match = re.fullmatch(r"decision-r([1-9][0-9]*)\.json", path.name)
            if match:
                decision_paths[int(match.group(1))] = path
    except OSError as error:
        raise SafeStop(
            "file_read_error",
            "Could not inspect controlled decision records.",
        ) from error

    expected_decision_revisions = set(range(1, revision))
    if state["active_decision_path"] is not None:
        expected_decision_revisions.add(revision)
    if set(decision_paths) != expected_decision_revisions:
        raise SafeStop(
            "audit_history_mismatch",
            "Decision files do not match the controlled revision lifecycle.",
        )

    decision_event_positions = positions("review_decision_recorded")
    if len(decision_event_positions) != len(decision_paths):
        raise SafeStop(
            "audit_history_mismatch",
            "Decision audit events do not match controlled decision files.",
        )
    decision_positions_by_revision: dict[int, int] = {}
    decision_records: dict[int, dict[str, Any]] = {}
    for decision_revision, decision_path in sorted(decision_paths.items()):
        decision = read_json(decision_path)
        validate_approval(decision)
        if (
            decision["run_id"] != state["run_id"]
            or decision["draft_revision"] != decision_revision
        ):
            raise SafeStop(
                "audit_history_mismatch",
                "A decision file identifies a different run or revision.",
            )
        if decision_revision < revision and decision["decision"] != "edit":
            raise SafeStop(
                "audit_history_mismatch",
                "Only an edit decision can precede a later controlled revision.",
            )
        matches = [
            index
            for index, event in enumerate(events)
            if _audit_matches(
                event,
                "review_decision_recorded",
                {
                    "decision_id": decision["decision_id"],
                    "decision": decision["decision"],
                    "draft_revision": decision_revision,
                    "draft_sha256": decision["draft_sha256"],
                    "review_manifest_sha256": decision["review_manifest_sha256"],
                    "evidence_reviewed": decision["evidence_reviewed"],
                },
            )
        ]
        if len(matches) != 1:
            raise SafeStop(
                "audit_history_mismatch",
                "A controlled decision lacks one exact matching audit event.",
            )
        expected_decision_state = {
            "approve": "approved_for_local_export",
            "edit": "changes_requested",
            "reject": "rejected",
            "expire": "expired",
        }[decision["decision"]]
        require_exact_event(
            matches[0],
            event_type="review_decision_recorded",
            event_state=expected_decision_state,
            actor_type="reviewer",
            details={
                "decision_id": decision["decision_id"],
                "decision": decision["decision"],
                "draft_revision": decision_revision,
                "draft_sha256": decision["draft_sha256"],
                "review_manifest_sha256": decision["review_manifest_sha256"],
                "evidence_reviewed": decision["evidence_reviewed"],
                "integrity_scope": "local_tamper_detection_not_authentication",
            },
        )
        decision_positions_by_revision[decision_revision] = matches[0]
        decision_records[decision_revision] = decision

    initial_evidence = decision_records.get(1)
    initial_draft_sha256 = (
        initial_evidence["draft_sha256"]
        if initial_evidence is not None
        else state["draft_sha256"]
    )
    initial_manifest_sha256 = (
        initial_evidence["review_manifest_sha256"]
        if initial_evidence is not None
        else state["review_manifest_sha256"]
    )
    require_exact_event(
        review_required,
        event_type="human_review_required",
        event_state="needs_review",
        actor_type="system",
        details={
            "draft_revision": 1,
            "draft_sha256": initial_draft_sha256,
            "review_manifest_sha256": initial_manifest_sha256,
        },
    )

    revision_event_positions = positions("draft_revision_created")
    if len(revision_event_positions) != revision - 1:
        raise SafeStop(
            "audit_history_mismatch",
            "Draft-revision audit events do not match the current revision.",
        )
    revision_positions: dict[int, int] = {}
    for created_revision in range(2, revision + 1):
        matches = [
            index
            for index, event in enumerate(events)
            if _audit_matches(
                event,
                "draft_revision_created",
                {
                    "previous_revision": created_revision - 1,
                    "draft_revision": created_revision,
                },
            )
        ]
        if len(matches) != 1:
            raise SafeStop(
                "audit_history_mismatch",
                "A controlled draft revision lacks one exact audit event.",
            )
        previous_decision = decision_records[created_revision - 1]
        created_evidence = decision_records.get(created_revision)
        created_sha256 = (
            created_evidence["draft_sha256"]
            if created_evidence is not None
            else state["draft_sha256"]
        )
        created_manifest_sha256 = (
            created_evidence["review_manifest_sha256"]
            if created_evidence is not None
            else state["review_manifest_sha256"]
        )
        require_exact_event(
            matches[0],
            event_type="draft_revision_created",
            event_state="needs_review",
            actor_type="system",
            details={
                "previous_revision": created_revision - 1,
                "draft_revision": created_revision,
                "previous_sha256": previous_decision["draft_sha256"],
                "draft_sha256": created_sha256,
                "review_manifest_sha256": created_manifest_sha256,
            },
        )
        revision_positions[created_revision] = matches[0]
        if decision_positions_by_revision[created_revision - 1] >= matches[0]:
            raise SafeStop(
                "audit_history_mismatch",
                "A draft revision event precedes its required edit decision.",
            )

    for decision_revision, decision_position in decision_positions_by_revision.items():
        prerequisite = (
            review_required
            if decision_revision == 1
            else revision_positions[decision_revision]
        )
        if decision_position <= prerequisite:
            raise SafeStop(
                "audit_history_mismatch",
                "A decision event precedes the evidence revision it reviews.",
            )

    export_positions = positions("local_export_created")
    if state["current_state"] == "approved_draft":
        if len(export_positions) != 1:
            raise SafeStop(
                "audit_history_mismatch",
                "Approved draft must have one material export audit event.",
            )
        current_decision = decision_records.get(revision)
        if current_decision is None or not _audit_matches(
            events[export_positions[0]],
            "local_export_created",
            {
                "decision_id": current_decision["decision_id"],
                "draft_revision": revision,
                "external_actions": 0,
            },
        ):
            raise SafeStop(
                "audit_history_mismatch",
                "Export audit evidence differs from the active approval.",
            )
        require_exact_event(
            export_positions[0],
            event_type="local_export_created",
            event_state="approved_draft",
            actor_type="system",
            details={
                "decision_id": current_decision["decision_id"],
                "draft_revision": revision,
                "files": [
                    f"approved-r{revision}.json",
                    f"approved-r{revision}.csv",
                ],
                "external_actions": 0,
            },
        )
        if export_positions[0] <= decision_positions_by_revision[revision]:
            raise SafeStop(
                "audit_history_mismatch",
                "Export audit event precedes its approval.",
            )
    elif export_positions:
        raise SafeStop(
            "audit_history_mismatch",
            "A non-export state contains an impossible material export event.",
        )

    expiry_positions = positions("review_expired")
    active = decision_records.get(revision)
    expiry_required = (
        state["current_state"] == "expired"
        and active is not None
        and active["decision"] == "approve"
    )
    if expiry_required:
        if (
            len(expiry_positions) != 1
            or expiry_positions[0] <= decision_positions_by_revision[revision]
        ):
            raise SafeStop(
                "audit_history_mismatch",
                "Expired approval must have one ordered expiry audit event.",
            )
        require_exact_event(
            expiry_positions[0],
            event_type="review_expired",
            event_state="expired",
            actor_type="system",
            details={
                "decision_id": active["decision_id"],
                "draft_revision": revision,
            },
        )
    elif expiry_positions:
        raise SafeStop(
            "audit_history_mismatch",
            "Audit history contains an impossible review-expiry event.",
        )

    candidate_positions = positions("candidate_summary_validated")
    candidate_pairs: set[tuple[int, str]] = set()
    for index in candidate_positions:
        event = events[index]
        event_revision = event["details"]["draft_revision"]
        candidate_key = (
            event_revision,
            event["details"]["candidate_sha256"],
        )
        if candidate_key in candidate_pairs:
            raise SafeStop(
                "audit_history_mismatch",
                "Candidate validation audit evidence is duplicated.",
            )
        candidate_pairs.add(candidate_key)
        if event_revision < 1 or event_revision > revision:
            raise SafeStop(
                "audit_history_mismatch",
                "Candidate validation identifies an impossible draft revision.",
            )
        prerequisite = (
            review_required
            if event_revision == 1
            else revision_positions[event_revision]
        )
        decision_position = decision_positions_by_revision.get(event_revision)
        if index <= prerequisite or (
            decision_position is not None and index >= decision_position
        ):
            raise SafeStop(
                "audit_history_mismatch",
                "Candidate validation is out of order for its draft revision.",
            )

    candidate_result_path = run_dir / "review" / "candidate-validation.json"
    if candidate_result_path.exists():
        candidate_result = read_json(candidate_result_path)
        required_candidate_result = {
            "run_id",
            "candidate_sha256",
            "draft_revision",
            "status",
            "prose_support_status",
            "issue_reference_count",
            "human_support_review_required",
            "external_actions",
        }
        _require_exact_keys(
            candidate_result,
            required_candidate_result,
            "candidate validation result",
        )
        matching_candidates = [
            event
            for event in events
            if event["event_type"] == "candidate_summary_validated"
            and event["details"]["candidate_sha256"]
            == candidate_result["candidate_sha256"]
            and event["details"]["draft_revision"]
            == candidate_result["draft_revision"]
        ]
        if (
            candidate_result["run_id"] != state["run_id"]
            or candidate_result["status"]
            != "bounded_structure_and_references_valid"
            or candidate_result["prose_support_status"]
            != "controlled_templates_only"
            or candidate_result["issue_reference_count"] != len(issues)
            or candidate_result["human_support_review_required"] is not True
            or type(candidate_result["external_actions"]) is not int
            or candidate_result["external_actions"] != 0
            or len(matching_candidates) != 1
        ):
            raise SafeStop(
                "audit_history_mismatch",
                "Candidate validation result differs from its audit evidence.",
            )
    elif candidate_positions:
        raise SafeStop(
            "audit_history_mismatch",
            "Candidate validation audit exists without its controlled result.",
        )

    _reconcile_safe_stop_history(
        run_dir,
        events,
        base_complete_index=review_required,
    )


def _prepare_run_unlocked(
    input_path: Path,
    workspace: Path,
    ai_mode: str,
    synthetic_confirmation: str,
    expected_path: Path | None = None,
) -> Path:
    if (
        not isinstance(input_path, Path)
        or not isinstance(workspace, Path)
        or (expected_path is not None and not isinstance(expected_path, Path))
    ):
        raise SafeStop(
            "invalid_argument",
            "Prepare paths must be Path values.",
        )
    _validate_supported_path(workspace, "Workspace", workspace_root=True)
    try:
        if workspace.exists() and not workspace.is_dir():
            raise SafeStop(
                "workspace_not_directory",
                "The selected workspace is a file, not a folder. Choose a short "
                "ordinary local folder and retry.",
            )
    except OSError as error:
        raise SafeStop(
            "filesystem_check_error",
            "Could not safely inspect the workspace.",
        ) from error
    if synthetic_confirmation != SYNTHETIC_CONFIRMATION:
        raise SafeStop(
            "synthetic_confirmation_required",
            f"Use the exact confirmation {SYNTHETIC_CONFIRMATION}; never use real data.",
        )
    if not isinstance(ai_mode, str) or ai_mode not in AI_MODES:
        raise SafeStop("invalid_ai_mode", f"Unknown AI mode: {ai_mode}.")
    input_bytes, rows = load_work_items(input_path)
    input_hash = sha256_bytes(input_bytes)
    expected_keys, expected_oracle_hash, expected_oracle_evidence = (
        _read_expected_oracle(expected_path)
    )
    run_config = {
        "schema_version": RUN_CONFIG_SCHEMA_VERSION,
        "input_sha256": input_hash,
        "assessment_date": ASSESSMENT_DATE.isoformat(),
        "pipeline_version": PIPELINE_VERSION,
        "rules_version": RULES_VERSION,
        "prompt_version": PROMPT_VERSION,
        "requested_adapter_mode": ai_mode,
        "mock_generator_version": MOCK_GENERATOR_VERSION,
        "fallback_generator_version": FALLBACK_GENERATOR_VERSION,
        "expected_oracle_present": expected_path is not None,
        "expected_oracle_sha256": expected_oracle_hash,
    }
    validate_run_config(run_config)
    run_config_hash = _run_config_hash(run_config)
    run_id = _run_id_from_config(run_config)
    try:
        resolved_workspace = workspace.resolve()
    except OSError as error:
        raise SafeStop(
            "filesystem_check_error",
            "Could not resolve the workspace path.",
        ) from error
    run_dir = resolved_workspace / "runs" / run_id
    longest_generated = run_dir / "failures" / "a99999999.json"
    if len(str(longest_generated)) >= 260:
        raise SafeStop(
            "workspace_path_too_long",
            "This workspace would create a path at or above 260 characters. "
            "Choose a shorter ordinary local folder, then retry.",
        )
    state_path = run_dir / "state.json"
    try:
        workspace.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        raise SafeStop(
            "file_write_error",
            "Could not create the controlled workspace.",
        ) from error

    if state_path.exists():
        with _exclusive_operation_lock(run_dir):
            state = read_json(state_path)
            validate_state(state)
            existing_config = read_json(run_dir / "run_config.json")
            validate_run_config(existing_config)
            if (
                canonical_bytes(existing_config) != canonical_bytes(run_config)
                or state["run_config_sha256"] != run_config_hash
                or state["run_id"] != run_id
            ):
                raise SafeStop(
                    "run_collision",
                    "Existing run has a different canonical run configuration.",
                )
            _load_run(run_dir)
            existing_events = _load_audit_events(
                run_dir / "audit" / "events.jsonl",
                expected_run_id=run_id,
            )
            if not any(
                event["event_type"] == "duplicate_retry_ignored"
                and event["details"].get("run_config_sha256") == run_config_hash
                for event in existing_events
            ):
                append_audit_event(
                    run_dir,
                    run_id,
                    "duplicate_retry_ignored",
                    state["current_state"],
                    "system",
                    {
                        "input_sha256": input_hash,
                        "run_config_sha256": run_config_hash,
                        "no_duplicate_effect": True,
                    },
                )
            _write_latest_run_locator(workspace, run_id)
            return run_dir

    runs_root = resolved_workspace / "runs"
    try:
        runs_root.mkdir(parents=True, exist_ok=True)
        staging_parent = Path(tempfile.mkdtemp(prefix=STAGING_PREFIX, dir=runs_root))
        _create_staging_marker(staging_parent)
        staged_run_dir = staging_parent / run_id
        staged_run_dir.mkdir()
    except OSError as error:
        raise SafeStop(
            "file_write_error",
            "Could not create the private run staging folder.",
        ) from error
    final_run_dir = run_dir
    run_dir = staged_run_dir
    state_path = run_dir / "state.json"

    issues = detect_issues(rows)
    for issue in issues:
        validate_issue(issue)
    expected_keys_value = (
        [list(key) for key in sorted(expected_keys)]
        if expected_keys is not None
        else None
    )
    state_common = {
        "run_id": run_id,
        "run_config_sha256": run_config_hash,
        "input_sha256": input_hash,
        "assessment_date": ASSESSMENT_DATE.isoformat(),
        "pipeline_version": PIPELINE_VERSION,
        "rules_version": RULES_VERSION,
        "prompt_version": PROMPT_VERSION,
        "ai_mode_requested": ai_mode,
        "external_actions": 0,
        "local_export_count": 0,
        "expected_keys": expected_keys_value,
    }
    write_json(run_dir / "run_config.json", run_config)
    atomic_write_bytes(run_dir / "source" / "work_items.csv", input_bytes)
    atomic_write_bytes(
        run_dir / EXPECTED_ORACLE_EVIDENCE_PATH,
        expected_oracle_evidence,
    )
    _write_issues_csv(run_dir / "issues" / "issues.csv", issues)
    write_json(run_dir / "issues" / "issues.json", issues)
    write_json(run_dir / "control.json", CONTROL)

    if not issues:
        state = {
            **state_common,
            "current_state": "no_action_needed",
            "draft_revision": 0,
            "draft_sha256": None,
            "review_manifest_sha256": None,
            "active_decision_path": None,
            "summary_generator": None,
            "summary_fallback_reason": None,
        }
        validate_state(state)
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
            {
                "input_sha256": input_hash,
                "run_config_sha256": run_config_hash,
                "dataset_kind": "synthetic",
            },
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
        _publish_staged_run(staging_parent, run_dir, final_run_dir)
        _write_latest_run_locator(workspace, run_id)
        return final_run_dir

    summary, fallback_reason = create_bounded_summary(ai_mode, run_id, issues)
    validate_summary(summary, issues, run_id, rows)
    draft_bytes = canonical_bytes(summary)
    draft_hash = sha256_bytes(draft_bytes)
    atomic_write_bytes(run_dir / "draft" / "summary.json", draft_bytes)
    review_package = _review_package(run_id, 1, draft_hash, len(issues))
    validate_review_package(
        review_package,
        run_id=run_id,
        draft_revision=1,
        draft_sha256=draft_hash,
        issue_count=len(issues),
    )
    write_json(run_dir / "review" / "review_package.json", review_package)
    review_manifest = _build_review_manifest(run_dir, run_id, 1, run_config)
    review_manifest_hash = _review_manifest_hash(review_manifest)
    write_json(run_dir / "review" / "review_manifest.json", review_manifest)
    atomic_write_bytes(
        run_dir / "manual_fallback.md",
        _manual_fallback_text(run_id, issues).encode("utf-8"),
    )
    state = {
        **state_common,
        "current_state": "needs_review",
        "draft_revision": 1,
        "draft_sha256": draft_hash,
        "review_manifest_sha256": review_manifest_hash,
        "active_decision_path": None,
        "summary_generator": summary["generator"],
        "summary_fallback_reason": fallback_reason,
    }
    validate_state(state)
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
        {
            "input_sha256": input_hash,
            "run_config_sha256": run_config_hash,
            "dataset_kind": "synthetic",
        },
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
        {
            "draft_revision": 1,
            "draft_sha256": draft_hash,
            "review_manifest_sha256": review_manifest_hash,
        },
    )
    _publish_staged_run(staging_parent, run_dir, final_run_dir)
    _write_latest_run_locator(workspace, run_id)
    return final_run_dir


def _load_run(
    run_dir: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any] | None]:
    if not isinstance(run_dir, Path):
        raise SafeStop("invalid_argument", "Run directory must be a Path.")
    if _path_exists(
        run_dir / TRANSACTION_INCOMPLETE_NAME,
        "controlled transaction marker",
    ):
        raise SafeStop(
            "incomplete_controlled_transaction",
            "A prior controlled mutation could not be rolled back completely. "
            "Do not continue until the visible transaction marker is resolved.",
        )
    if _path_exists(run_dir / "outbox" / "INCOMPLETE.txt", "export marker"):
        raise SafeStop(
            "incomplete_export_transaction",
            "A prior export could not be rolled back completely. Do not use "
            "the outbox until a human resolves the visible INCOMPLETE marker.",
        )
    state = read_json(run_dir / "state.json")
    validate_state(state)
    if run_dir.name != state["run_id"]:
        raise SafeStop("run_directory_mismatch", "Run folder name differs from run_id.")
    run_config = read_json(run_dir / "run_config.json")
    validate_run_config(run_config)
    config_hash = _run_config_hash(run_config)
    if state["run_config_sha256"] != config_hash:
        raise SafeStop(
            "run_config_integrity_mismatch",
            "State no longer identifies the actual run configuration.",
        )
    if _run_id_from_config(run_config) != state["run_id"]:
        raise SafeStop(
            "run_config_integrity_mismatch",
            "Run identifier no longer matches its canonical configuration.",
        )
    expected_config_values = {
        "assessment_date": ASSESSMENT_DATE.isoformat(),
        "pipeline_version": PIPELINE_VERSION,
        "rules_version": RULES_VERSION,
        "prompt_version": PROMPT_VERSION,
        "mock_generator_version": MOCK_GENERATOR_VERSION,
        "fallback_generator_version": FALLBACK_GENERATOR_VERSION,
    }
    if any(
        run_config[field] != value for field, value in expected_config_values.items()
    ):
        raise SafeStop(
            "unsupported_run_version",
            "Run configuration uses a version this runner cannot safely execute.",
        )
    if (
        state["input_sha256"] != run_config["input_sha256"]
        or state["assessment_date"] != run_config["assessment_date"]
        or state["pipeline_version"] != run_config["pipeline_version"]
        or state["rules_version"] != run_config["rules_version"]
        or state["prompt_version"] != run_config["prompt_version"]
        or state["ai_mode_requested"] != run_config["requested_adapter_mode"]
    ):
        raise SafeStop(
            "run_config_integrity_mismatch",
            "State configuration fields differ from run_config.json.",
        )
    source_path = run_dir / "source" / "work_items.csv"
    source_bytes = _read_regular_bytes(
        source_path,
        "protected source file",
        max_bytes=MAX_WORK_ITEM_CSV_BYTES,
    )
    if sha256_bytes(source_bytes) != state["input_sha256"]:
        raise SafeStop(
            "source_integrity_mismatch",
            "Protected source bytes differ from the canonical run configuration.",
        )
    source_rows = _parse_csv_bytes(source_bytes, source_path.name)
    detected_issues = detect_issues(source_rows)
    for issue in detected_issues:
        validate_issue(issue)
    issues = read_json(run_dir / "issues" / "issues.json")
    if not isinstance(issues, list):
        raise SafeStop("contract_mismatch", "issues.json must contain a list.")
    for issue in issues:
        validate_issue(issue)
    if issues != detected_issues:
        raise SafeStop(
            "issues_integrity_mismatch",
            "Issue JSON differs from deterministic source evaluation.",
        )
    issues_csv_path = run_dir / "issues" / "issues.csv"
    issues_csv_bytes = _read_regular_bytes(
        issues_csv_path,
        "controlled issue CSV",
        max_bytes=MAX_JSON_BYTES,
    )
    if issues_csv_bytes != _csv_bytes(issues, ISSUE_FIELDS):
        raise SafeStop(
            "issues_integrity_mismatch",
            "Issue CSV differs from the canonical issue JSON.",
        )
    control = read_json(run_dir / "control.json")
    validate_control(control)
    protected_expected_keys = _expected_keys_from_run_evidence(
        run_dir,
        run_config,
    )
    audit_events = _load_audit_events(
        run_dir / "audit" / "events.jsonl",
        expected_run_id=state["run_id"],
    )
    if not audit_events:
        raise SafeStop("audit_corrupt", "Run audit has no valid events.")
    evaluation = read_json(run_dir / "evaluation.json")
    validate_evaluation(evaluation)
    expected_raw = state["expected_keys"]
    state_expected_keys = (
        {tuple(value) for value in expected_raw} if expected_raw is not None else None
    )
    if state_expected_keys != protected_expected_keys:
        raise SafeStop(
            "expected_oracle_integrity_mismatch",
            "Mutable state expected keys differ from protected run evidence.",
        )
    recomputed_evaluation = _evaluation(
        state["run_id"],
        issues,
        protected_expected_keys,
        state["summary_fallback_reason"],
        state["current_state"],
    )
    if evaluation != recomputed_evaluation:
        raise SafeStop(
            "evaluation_integrity_mismatch",
            "Evaluation differs from exact deterministic recomputation.",
        )
    if state["current_state"] == "no_action_needed":
        if issues:
            raise SafeStop(
                "state_contract",
                "No-action state contains verified issues.",
            )
        _reconcile_audit_history(
            run_dir,
            state,
            issues,
            audit_events,
            len(source_rows),
        )
        return state, issues, None

    summary = read_json(run_dir / "draft" / "summary.json")
    validate_summary(summary, issues, state["run_id"], source_rows)
    draft_bytes = _read_bytes(
        run_dir / "draft" / "summary.json",
        "controlled summary draft",
    )
    if sha256_bytes(draft_bytes) != state["draft_sha256"]:
        raise SafeStop(
            "draft_integrity_mismatch",
            "Draft bytes differ from the controlled state hash.",
        )
    if (
        summary["prompt_version"] != run_config["prompt_version"]
        or summary["generator"] != state["summary_generator"]
    ):
        raise SafeStop(
            "summary_contract",
            "Summary version or generator differs from controlled configuration.",
        )
    review_package = read_json(run_dir / "review" / "review_package.json")
    validate_review_package(
        review_package,
        run_id=state["run_id"],
        draft_revision=state["draft_revision"],
        draft_sha256=state["draft_sha256"],
        issue_count=len(issues),
    )
    stored_manifest = read_json(run_dir / "review" / "review_manifest.json")
    validate_review_manifest(
        stored_manifest,
        run_id=state["run_id"],
        draft_revision=state["draft_revision"],
        run_config=run_config,
    )
    recomputed_manifest = _build_review_manifest(
        run_dir,
        state["run_id"],
        state["draft_revision"],
        run_config,
    )
    if stored_manifest != recomputed_manifest:
        raise SafeStop(
            "review_manifest_mismatch",
            "Protected artifact bytes differ from the stored review manifest.",
        )
    current_manifest_hash = _review_manifest_hash(recomputed_manifest)
    if current_manifest_hash != state["review_manifest_sha256"]:
        raise SafeStop(
            "review_manifest_mismatch",
            "Review manifest no longer matches controlled state.",
        )
    decision_relative = state["active_decision_path"]
    if decision_relative is not None:
        decision = read_json(run_dir / decision_relative)
        validate_approval(decision)
        if (
            decision["run_id"] != state["run_id"]
            or decision["draft_revision"] != state["draft_revision"]
            or decision["draft_sha256"] != state["draft_sha256"]
            or decision["review_manifest_sha256"] != current_manifest_hash
        ):
            raise SafeStop(
                "decision_integrity_mismatch",
                "Active decision identifies different protected review evidence.",
            )
        expected_decisions = {
            "approved_for_local_export": {"approve"},
            "approved_draft": {"approve"},
            "changes_requested": {"edit"},
            "rejected": {"reject"},
            "expired": {"approve", "expire"},
        }
        allowed = expected_decisions.get(state["current_state"])
        if allowed is None or decision["decision"] not in allowed:
            raise SafeStop(
                "decision_state_mismatch",
                "The active decision does not permit the controlled run state.",
            )
    elif state["current_state"] in {
        "approved_for_local_export",
        "approved_draft",
        "changes_requested",
        "rejected",
        "expired",
    }:
        raise SafeStop(
            "decision_state_mismatch",
            "A decision-controlled state is missing its active decision.",
        )

    outbox = run_dir / "outbox"
    json_path = outbox / f"approved-r{state['draft_revision']}.json"
    csv_path = outbox / f"approved-r{state['draft_revision']}.csv"
    json_exists = _path_exists(json_path, "approved JSON export")
    csv_exists = _path_exists(csv_path, "approved CSV export")
    if json_exists != csv_exists:
        raise SafeStop(
            "export_pair_mismatch",
            "Only one member of the controlled export pair exists.",
        )
    if state["current_state"] == "approved_draft":
        if not json_exists:
            raise SafeStop(
                "missing_approved_export",
                "Approved-draft state is missing its controlled JSON/CSV pair.",
            )
        if decision_relative is None:
            raise SafeStop(
                "decision_state_mismatch", "Approved export has no decision."
            )
        decision = read_json(run_dir / decision_relative)
        export_count = _local_export_audit_count(
            run_dir,
            state["run_id"],
            decision["decision_id"],
            state["draft_revision"],
        )
        if export_count != 1:
            raise SafeStop(
                "export_audit_mismatch",
                "Approved export must have exactly one matching audit event.",
            )
        expected_json, expected_csv = _expected_export_bytes(
            state,
            issues,
            summary,
            decision,
            current_manifest_hash,
        )
        if (
            _read_bytes(json_path, "approved JSON export") != expected_json
            or _read_bytes(csv_path, "approved CSV export") != expected_csv
        ):
            raise SafeStop(
                "export_integrity_mismatch",
                "Approved export bytes differ from the exact controlled evidence.",
            )
    elif json_exists:
        raise SafeStop(
            "unexpected_export",
            "Controlled export files exist before approved-draft state.",
        )
    _reconcile_audit_history(
        run_dir,
        state,
        issues,
        audit_events,
        len(source_rows),
    )
    return state, issues, summary


def _record_decision_unlocked(
    run_dir: Path,
    decision: str,
    reviewer_role: str,
    reason: str,
    expected_revision: int,
    evidence_reviewed: bool,
    expires_at: datetime | None = None,
    decided_at: datetime | None = None,
) -> Path:
    if not isinstance(decision, str) or decision not in DECISIONS:
        raise SafeStop(
            "invalid_decision", f"Decision must be one of {sorted(DECISIONS)}."
        )
    if (
        not isinstance(reviewer_role, str)
        or not isinstance(reason, str)
        or not reviewer_role.strip()
        or not reason.strip()
    ):
        raise SafeStop("invalid_decision", "Reviewer role and reason are required.")
    if type(expected_revision) is not int or expected_revision < 1:
        raise SafeStop(
            "invalid_decision",
            "Expected revision must be a positive integer.",
        )
    if type(evidence_reviewed) is not bool:
        raise SafeStop(
            "invalid_decision",
            "Evidence-reviewed must be true or false.",
        )
    if expires_at is not None and not isinstance(expires_at, datetime):
        raise SafeStop("invalid_datetime", "expires_at must be a date-time.")
    if decided_at is not None and not isinstance(decided_at, datetime):
        raise SafeStop("invalid_datetime", "decided_at must be a date-time.")
    state, _, summary = _load_run(run_dir)
    if state["current_state"] == "no_action_needed":
        raise SafeStop(
            "no_action_needed",
            "A run with no verified issues has no draft to decide.",
        )
    if summary is None:
        raise SafeStop("state_contract", "Issue-bearing run has no summary.")
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
    current_hash = sha256_bytes(_read_bytes(draft_path, "controlled summary draft"))
    if current_hash != state["draft_sha256"]:
        raise SafeStop(
            "draft_changed_before_decision",
            "The draft changed; create and review a new controlled revision.",
        )
    material = {
        "run_id": state["run_id"],
        "reviewer_role": reviewer_role.strip(),
        "decision": decision,
        "draft_revision": expected_revision,
        "draft_sha256": current_hash,
        "review_manifest_sha256": state["review_manifest_sha256"],
        "decided_at": iso_utc(decided),
        "expires_at": iso_utc(expires),
        "evidence_reviewed": evidence_reviewed,
        "reason": reason.strip(),
    }
    record = {"decision_id": _decision_id(material), **material}
    validate_approval(record)
    decision_path = run_dir / "review" / f"decision-r{expected_revision}.json"
    if decision_path.exists():
        raise SafeStop(
            "decision_already_recorded",
            f"Revision {expected_revision} already has a recorded decision.",
        )
    if decision == "approve":
        new_state = "approved_for_local_export"
    elif decision == "edit":
        new_state = "changes_requested"
    elif decision == "reject":
        new_state = "rejected"
    else:
        new_state = "expired"
    state_path = run_dir / "state.json"
    audit_path = run_dir / "audit" / "events.jsonl"
    evaluation_path = run_dir / "evaluation.json"

    def commit_decision() -> None:
        write_json(decision_path, record)
        state["current_state"] = new_state
        state["active_decision_path"] = decision_path.relative_to(run_dir).as_posix()
        validate_state(state)
        write_json(state_path, state)
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
                "review_manifest_sha256": state["review_manifest_sha256"],
                "evidence_reviewed": evidence_reviewed,
                "integrity_scope": "local_tamper_detection_not_authentication",
            },
            decided,
        )
        _refresh_evaluation(run_dir, state, new_state)

    _execute_controlled_transaction(
        run_dir,
        [decision_path, state_path, audit_path, evaluation_path],
        commit_decision,
        failure_code="decision_finalize_error",
        failure_message=(
            "The decision could not be finalized. Prior controlled state was "
            "restored; retry is safe."
        ),
    )
    return decision_path


def _revise_draft_unlocked(
    run_dir: Path,
    replacement_path: Path,
    expected_revision: int,
) -> int:
    if not isinstance(replacement_path, Path) or type(expected_revision) is not int:
        raise SafeStop(
            "invalid_argument",
            "Revision requires a replacement Path and integer expected revision.",
        )
    state, issues, current_summary = _load_run(run_dir)
    if current_summary is None:
        raise SafeStop("no_action_needed", "A no-action run has no draft to revise.")
    if state["current_state"] != "changes_requested":
        raise SafeStop("invalid_state", "A new draft requires an edit decision.")
    if expected_revision != state["draft_revision"]:
        raise SafeStop(
            "stale_update",
            f"Expected revision {expected_revision}, current revision is "
            f"{state['draft_revision']}.",
        )
    replacement = read_json(replacement_path)
    run_config = read_json(run_dir / "run_config.json")
    validate_run_config(run_config)
    if (
        not isinstance(replacement, dict)
        or replacement.get("prompt_version") != run_config["prompt_version"]
        or replacement.get("generator") != state["summary_generator"]
    ):
        raise SafeStop(
            "replacement_run_mismatch",
            "Replacement prompt version and generator must match this exact run.",
        )
    source_bytes = _read_regular_bytes(
        run_dir / "source" / "work_items.csv",
        "protected source file",
        max_bytes=MAX_WORK_ITEM_CSV_BYTES,
    )
    source_rows = _parse_csv_bytes(source_bytes, "work_items.csv")
    validate_summary(replacement, issues, state["run_id"], source_rows)
    replacement_bytes = canonical_bytes(replacement)
    old_hash = state["draft_sha256"]
    new_hash = sha256_bytes(replacement_bytes)
    if new_hash == old_hash:
        raise SafeStop("unchanged_revision", "The replacement draft did not change.")
    next_revision = expected_revision + 1
    draft_path = run_dir / "draft" / "summary.json"
    review_package = _review_package(
        state["run_id"],
        next_revision,
        new_hash,
        len(issues),
    )
    validate_review_package(
        review_package,
        run_id=state["run_id"],
        draft_revision=next_revision,
        draft_sha256=new_hash,
        issue_count=len(issues),
    )
    package_path = run_dir / "review" / "review_package.json"
    manifest_path = run_dir / "review" / "review_manifest.json"
    state_path = run_dir / "state.json"
    audit_path = run_dir / "audit" / "events.jsonl"
    evaluation_path = run_dir / "evaluation.json"

    def commit_revision() -> None:
        atomic_write_bytes(draft_path, replacement_bytes)
        write_json(package_path, review_package)
        review_manifest = _build_review_manifest(
            run_dir,
            state["run_id"],
            next_revision,
            run_config,
        )
        review_manifest_hash = _review_manifest_hash(review_manifest)
        write_json(manifest_path, review_manifest)
        state["draft_revision"] = next_revision
        state["draft_sha256"] = new_hash
        state["review_manifest_sha256"] = review_manifest_hash
        state["current_state"] = "needs_review"
        state["active_decision_path"] = None
        state["local_export_count"] = 0
        validate_state(state)
        write_json(state_path, state)
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
                "review_manifest_sha256": review_manifest_hash,
            },
        )
        _refresh_evaluation(run_dir, state, "needs_review")

    _execute_controlled_transaction(
        run_dir,
        [
            draft_path,
            package_path,
            manifest_path,
            state_path,
            audit_path,
            evaluation_path,
        ],
        commit_revision,
        failure_code="revision_finalize_error",
        failure_message=(
            "The new revision could not be finalized. Prior controlled state "
            "was restored; retry is safe."
        ),
    )
    return next_revision


def _validate_candidate_summary_unlocked(
    run_dir: Path,
    candidate_path: Path,
) -> Path:
    """Validate a learner-created mock summary without replacing the run draft."""
    state, issues, summary = _load_run(run_dir)
    if summary is None:
        raise SafeStop("no_action_needed", "A no-action run has no summary contract.")
    if state["current_state"] != "needs_review":
        raise SafeStop(
            "invalid_state",
            "A learner candidate can only be validated while the run needs review.",
        )
    if not isinstance(candidate_path, Path):
        raise SafeStop("invalid_argument", "Candidate path must be a Path.")
    candidate = read_json(candidate_path)
    run_config = read_json(run_dir / "run_config.json")
    validate_run_config(run_config)
    if (
        not isinstance(candidate, dict)
        or candidate.get("prompt_version") != run_config["prompt_version"]
        or candidate.get("generator") != state["summary_generator"]
    ):
        raise SafeStop(
            "candidate_run_mismatch",
            "Candidate prompt version and generator must match this exact run.",
        )
    source_rows = _parse_csv_bytes(
        _read_regular_bytes(
            run_dir / "source" / "work_items.csv",
            "protected source file",
            max_bytes=MAX_WORK_ITEM_CSV_BYTES,
        ),
        "work_items.csv",
    )
    validate_summary(candidate, issues, state["run_id"], source_rows)
    result_path = run_dir / "review" / "candidate-validation.json"
    audit_path = run_dir / "audit" / "events.jsonl"
    candidate_hash = sha256_bytes(canonical_bytes(candidate))
    existing_events = _load_audit_events(
        audit_path,
        expected_run_id=state["run_id"],
    )
    duplicate = [
        event
        for event in existing_events
        if event["event_type"] == "candidate_summary_validated"
        and event["details"]["candidate_sha256"] == candidate_hash
        and event["details"]["draft_revision"] == state["draft_revision"]
    ]
    if duplicate:
        if len(duplicate) != 1 or not result_path.is_file():
            raise SafeStop(
                "audit_history_mismatch",
                "Candidate validation retry evidence is incomplete or duplicated.",
            )
        existing_result = read_json(result_path)
        if (
            existing_result.get("candidate_sha256") != candidate_hash
            or existing_result.get("draft_revision") != state["draft_revision"]
        ):
            raise SafeStop(
                "audit_history_mismatch",
                "Candidate validation result differs from its audit evidence.",
            )
        return result_path

    def commit_candidate_result() -> None:
        write_json(
            result_path,
            {
                "run_id": state["run_id"],
                "candidate_sha256": candidate_hash,
                "draft_revision": state["draft_revision"],
                "status": "bounded_structure_and_references_valid",
                "prose_support_status": "controlled_templates_only",
                "issue_reference_count": len(issues),
                "human_support_review_required": True,
                "external_actions": 0,
            },
        )
        append_audit_event(
            run_dir,
            state["run_id"],
            "candidate_summary_validated",
            state["current_state"],
            "system",
            {
                "candidate_sha256": candidate_hash,
                "draft_revision": state["draft_revision"],
                "issue_reference_count": len(issues),
                "prose_support_status": "controlled_templates_only",
                "human_support_review_required": True,
            },
        )

    _execute_controlled_transaction(
        run_dir,
        [result_path, audit_path],
        commit_candidate_result,
        failure_code="candidate_validation_write_error",
        failure_message=(
            "Candidate validation evidence could not be finalized. Prior "
            "controlled evidence was restored; retry is safe."
        ),
    )
    return result_path


def _refresh_evaluation(
    run_dir: Path,
    state: dict[str, Any],
    current_state: str,
) -> None:
    issues = read_json(run_dir / "issues" / "issues.json")
    if not isinstance(issues, list):
        raise SafeStop("contract_mismatch", "issues.json must contain a list.")
    for issue in issues:
        validate_issue(issue)
    run_config = read_json(run_dir / "run_config.json")
    validate_run_config(run_config)
    protected_expected_keys = _expected_keys_from_run_evidence(run_dir, run_config)
    expected_raw = state.get("expected_keys")
    state_expected_keys = (
        {tuple(value) for value in expected_raw} if expected_raw is not None else None
    )
    if state_expected_keys != protected_expected_keys:
        raise SafeStop(
            "expected_oracle_integrity_mismatch",
            "State expected keys differ from protected run evidence.",
        )
    write_json(
        run_dir / "evaluation.json",
        _evaluation(
            state["run_id"],
            issues,
            protected_expected_keys,
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


def _expected_export_bytes(
    state: dict[str, Any],
    issues: list[dict[str, Any]],
    summary: dict[str, Any],
    decision: dict[str, Any],
    review_manifest_sha256: str,
) -> tuple[bytes, bytes]:
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
    payload = {
        "run_id": state["run_id"],
        "draft_revision": state["draft_revision"],
        "draft_sha256": state["draft_sha256"],
        "review_manifest_sha256": review_manifest_sha256,
        "decision_id": decision["decision_id"],
        "dataset_kind": "synthetic",
        "output_kind": "local_draft_only",
        "external_actions": 0,
        "records": records,
    }
    return canonical_bytes(payload), _csv_bytes(records, list(records[0]))


def _local_export_audit_count(
    run_dir: Path,
    run_id: str,
    decision_id: str,
    draft_revision: int,
) -> int:
    events = _load_audit_events(
        run_dir / "audit" / "events.jsonl",
        expected_run_id=run_id,
    )
    return sum(
        1
        for event in events
        if event["event_type"] == "local_export_created"
        and event["state"] == "approved_draft"
        and event["details"].get("decision_id") == decision_id
        and event["details"].get("draft_revision") == draft_revision
    )


def _controlled_file_snapshot(
    path: Path,
    label: str,
    *,
    max_bytes: int = MAX_JSON_BYTES,
) -> bytes | None:
    try:
        return _read_regular_bytes(path, label, max_bytes=max_bytes)
    except SafeStop as error:
        if error.code == "missing_file":
            return None
        raise


def _restore_controlled_file(path: Path, snapshot: bytes | None) -> None:
    try:
        if snapshot is None:
            path.unlink(missing_ok=True)
        else:
            atomic_write_bytes(path, snapshot)
    except OSError as error:
        raise SafeStop(
            "file_write_error",
            f"Could not restore controlled file {path.name}.",
        ) from error


def _execute_controlled_transaction(
    run_dir: Path,
    paths: list[Path],
    action: Callable[[], Any],
    *,
    failure_code: str,
    failure_message: str,
) -> Any:
    """Run a multi-file mutation with byte-for-byte rollback on failure."""

    unique_paths = list(dict.fromkeys(paths))
    snapshots = {
        path: _controlled_file_snapshot(
            path,
            path.name,
            max_bytes=(
                MAX_AUDIT_BYTES if path.name == "events.jsonl" else MAX_JSON_BYTES
            ),
        )
        for path in unique_paths
    }
    try:
        return action()
    except Exception as error:
        rollback_errors: list[str] = []
        for path, snapshot in snapshots.items():
            try:
                _restore_controlled_file(path, snapshot)
            except Exception:
                rollback_errors.append(path.name)
        if rollback_errors:
            marker = run_dir / TRANSACTION_INCOMPLETE_NAME
            try:
                atomic_write_bytes(
                    marker,
                    (
                        "CONTROLLED TRANSACTION INCOMPLETE\n"
                        "Do not continue until a human verifies and restores the "
                        "last valid controlled artifacts.\n"
                        f"Rollback failures: {sorted(set(rollback_errors))}\n"
                    ).encode("utf-8"),
                )
            except Exception:
                pass
            raise SafeStop(
                "transaction_rollback_failed",
                "The controlled mutation failed and rollback could not restore "
                "every prior artifact. Do not continue while the transaction "
                "marker is present.",
            ) from error
        if isinstance(error, SafeStop):
            raise error
        raise SafeStop(failure_code, failure_message) from error


def _append_local_export_audit(
    run_dir: Path,
    state: dict[str, Any],
    decision: dict[str, Any],
    json_path: Path,
    csv_path: Path,
    checked: datetime,
) -> None:
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


def _export_approved_unlocked(
    run_dir: Path,
    checked_at: datetime | None = None,
) -> tuple[Path, Path]:
    if checked_at is not None and not isinstance(checked_at, datetime):
        raise SafeStop("invalid_datetime", "checked_at must be a date-time.")
    checked = checked_at or utc_now()
    try:
        state, issues, summary = _load_run(run_dir)
    except SafeStop as error:
        if error.code == "draft_integrity_mismatch":
            raise SafeStop(
                "edited_draft_after_approval",
                "Draft bytes changed after review; the decision is invalid.",
            ) from error
        raise
    if state["current_state"] == "no_action_needed":
        raise SafeStop(
            "no_action_needed",
            "A run with no verified issues has no draft to export.",
        )
    if summary is None:
        raise SafeStop("state_contract", "Issue-bearing run has no summary.")
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
    current_hash = sha256_bytes(
        _read_bytes(
            run_dir / "draft" / "summary.json",
            "controlled summary draft",
        )
    )
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
    run_config = read_json(run_dir / "run_config.json")
    validate_run_config(run_config)
    recomputed_manifest = _build_review_manifest(
        run_dir,
        state["run_id"],
        state["draft_revision"],
        run_config,
    )
    recomputed_manifest_hash = _review_manifest_hash(recomputed_manifest)
    if (
        recomputed_manifest_hash != state["review_manifest_sha256"]
        or decision["review_manifest_sha256"] != recomputed_manifest_hash
    ):
        raise SafeStop(
            "review_manifest_mismatch",
            "Approval does not identify the current protected source, issue "
            "registers, summary, control, review package, and run configuration.",
        )
    if checked < decided_at:
        raise SafeStop(
            "approval_not_yet_effective",
            "The export check is earlier than the approval decision.",
        )
    if checked >= expires_at:
        state_path = run_dir / "state.json"
        audit_path = run_dir / "audit" / "events.jsonl"
        evaluation_path = run_dir / "evaluation.json"

        def commit_expiry() -> None:
            state["current_state"] = "expired"
            validate_state(state)
            write_json(state_path, state)
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

        _execute_controlled_transaction(
            run_dir,
            [state_path, audit_path, evaluation_path],
            commit_expiry,
            failure_code="expiry_finalize_error",
            failure_message=(
                "Review expiry could not be finalized. Prior controlled state "
                "was restored; retry is safe."
            ),
        )
        raise SafeStop("expired_review", "The approval expired before export.")

    outbox = run_dir / "outbox"
    try:
        outbox.mkdir(parents=True, exist_ok=True)
        _validate_supported_path(outbox, "Controlled outbox")
        outbox_stat = outbox.lstat()
        if (
            not stat.S_ISDIR(outbox_stat.st_mode)
            or stat.S_ISLNK(outbox_stat.st_mode)
            or _path_has_reparse_attribute(outbox_stat)
        ):
            raise SafeStop(
                "export_write_error",
                "The controlled outbox is not an ordinary local folder.",
            )
    except SafeStop:
        raise
    except OSError as error:
        raise SafeStop(
            "export_write_error",
            "Could not create the controlled outbox.",
        ) from error
    json_path = outbox / f"approved-r{state['draft_revision']}.json"
    csv_path = outbox / f"approved-r{state['draft_revision']}.csv"
    json_bytes, csv_bytes = _expected_export_bytes(
        state,
        issues,
        summary,
        decision,
        recomputed_manifest_hash,
    )
    json_exists = _path_exists(json_path, "approved JSON export")
    csv_exists = _path_exists(csv_path, "approved CSV export")
    if json_exists != csv_exists:
        raise SafeStop(
            "idempotency_conflict",
            "Only one member of the approved JSON/CSV export pair exists; "
            "nothing was written.",
        )
    already_exported = json_exists and csv_exists
    if already_exported:
        if _read_bytes(json_path, "approved JSON export") != json_bytes:
            raise SafeStop("idempotency_conflict", "Existing JSON export differs.")
        if _read_bytes(csv_path, "approved CSV export") != csv_bytes:
            raise SafeStop("idempotency_conflict", "Existing CSV export differs.")
        return json_path, csv_path

    state_path = run_dir / "state.json"
    evaluation_path = run_dir / "evaluation.json"
    audit_path = run_dir / "audit" / "events.jsonl"
    snapshots = {
        state_path: _controlled_file_snapshot(state_path, "state.json"),
        evaluation_path: _controlled_file_snapshot(
            evaluation_path,
            "evaluation.json",
        ),
        audit_path: _controlled_file_snapshot(
            audit_path,
            "events.jsonl",
            max_bytes=MAX_AUDIT_BYTES,
        ),
    }
    incomplete_marker = outbox / "INCOMPLETE.txt"
    atomic_write_bytes(
        incomplete_marker,
        (
            "CONTROLLED EXPORT INCOMPLETE\n"
            "Do not use files in this outbox until this marker is absent.\n"
        ).encode("utf-8"),
    )
    finalization_started = already_exported
    staging_dir: Path | None = None
    promoted_outputs: set[Path] = set()
    try:
        if not already_exported:
            try:
                staging_dir = Path(
                    tempfile.mkdtemp(prefix=STAGING_PREFIX, dir=outbox)
                )
                _create_staging_marker(staging_dir)
            except SafeStop:
                raise
            except OSError as error:
                raise SafeStop(
                    "export_write_error",
                    "Could not create the owned private export staging folder.",
                ) from error
            staged_json = staging_dir / json_path.name
            staged_csv = staging_dir / csv_path.name
            try:
                atomic_write_bytes(staged_json, json_bytes)
                atomic_write_bytes(staged_csv, csv_bytes)
                staging_verified = (
                    _read_regular_bytes(
                        staged_json,
                        "staged JSON export",
                        max_bytes=MAX_JSON_BYTES,
                    )
                    == json_bytes
                    and _read_regular_bytes(
                        staged_csv,
                        "staged CSV export",
                        max_bytes=MAX_JSON_BYTES,
                    )
                    == csv_bytes
                )
            except SafeStop as error:
                raise SafeStop(
                    "export_write_error",
                    "Could not safely create and verify the private staged export pair.",
                ) from error
            if not staging_verified:
                raise SafeStop(
                    "export_write_error",
                    "The staged JSON/CSV export pair did not verify byte for byte.",
                )
            try:
                os.link(staged_json, json_path, follow_symlinks=False)
                promoted_outputs.add(json_path)
                os.link(staged_csv, csv_path, follow_symlinks=False)
                promoted_outputs.add(csv_path)
            except OSError as error:
                raise SafeStop(
                    "export_write_error",
                    "The complete JSON/CSV pair could not be published without "
                    "overwriting an existing path.",
                ) from error
            if (
                _read_bytes(json_path, "approved JSON export") != json_bytes
                or _read_bytes(csv_path, "approved CSV export") != csv_bytes
            ):
                raise SafeStop(
                    "export_write_error",
                    "The published JSON/CSV export pair did not verify byte for byte.",
                )
            finalization_started = True
            _discard_owned_staging_directory(staging_dir)
            staging_dir = None

        state["current_state"] = "approved_draft"
        state["local_export_count"] = 2
        state["external_actions"] = 0
        validate_state(state)
        write_json(state_path, state)
        _append_local_export_audit(
            run_dir,
            state,
            decision,
            json_path,
            csv_path,
            checked,
        )
        _refresh_evaluation(run_dir, state, "approved_draft")
        if (
            _local_export_audit_count(
                run_dir,
                state["run_id"],
                decision["decision_id"],
                state["draft_revision"],
            )
            != 1
        ):
            raise SafeStop(
                "export_audit_mismatch",
                "Exactly one local export audit event could not be verified.",
            )
        incomplete_marker.unlink()
        return json_path, csv_path
    except Exception as error:
        rollback_errors: list[str] = []
        if staging_dir is not None:
            try:
                _discard_owned_staging_directory(staging_dir)
                staging_dir = None
            except Exception:
                rollback_errors.append(staging_dir.name)
        for output_path in promoted_outputs:
            try:
                output_path.unlink(missing_ok=True)
            except OSError:
                rollback_errors.append(output_path.name)
        for controlled_path, snapshot in snapshots.items():
            try:
                _restore_controlled_file(controlled_path, snapshot)
            except Exception:
                rollback_errors.append(controlled_path.name)
        if not rollback_errors:
            try:
                incomplete_marker.unlink(missing_ok=True)
            except OSError:
                rollback_errors.append(incomplete_marker.name)
        if rollback_errors:
            raise SafeStop(
                "export_rollback_failed",
                "The export did not complete and rollback could not restore every "
                "controlled artifact. Do not use the outbox while INCOMPLETE.txt "
                "is present.",
            ) from error
        if (
            not finalization_started
            and isinstance(error, SafeStop)
            and error.code == "export_write_error"
        ):
            raise error
        raise SafeStop(
            "export_finalize_error",
            "The local export could not be finalized. The JSON/CSV pair and "
            "controlled state changes were rolled back; retry is safe.",
        ) from error


def _inspect_run_unlocked(run_dir: Path) -> dict[str, Any]:
    state, issues, summary = _load_run(run_dir)
    if state["current_state"] == "no_action_needed":
        summary_generator = None
    else:
        if summary is None:
            raise SafeStop("state_contract", "Issue-bearing run has no summary.")
        summary_generator = summary["generator"]
    audit_path = run_dir / "audit" / "events.jsonl"
    events = _load_audit_events(audit_path, expected_run_id=state["run_id"])
    if not events:
        raise SafeStop("audit_corrupt", "Run audit has no events.")
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


def _run_locked(
    scope: Path,
    action: Callable[[], Any],
) -> Any:
    try:
        with _exclusive_operation_lock(scope):
            return action()
    except SafeStop:
        raise
    except OSError as error:
        raise SafeStop(
            "filesystem_operation_error",
            "A filesystem operation failed safely; no external action occurred.",
        ) from error


def prepare_run(
    input_path: Path,
    workspace: Path,
    ai_mode: str,
    synthetic_confirmation: str,
    expected_path: Path | None = None,
) -> Path:
    if not isinstance(workspace, Path):
        raise SafeStop("invalid_argument", "Workspace must be a Path.")
    _validate_supported_path(workspace, "Workspace", workspace_root=True)
    try:
        if workspace.exists() and not workspace.is_dir():
            raise SafeStop(
                "workspace_not_directory",
                "The selected workspace is a file, not a folder. Choose a short "
                "ordinary local folder and retry.",
            )
    except OSError as error:
        raise SafeStop(
            "filesystem_check_error",
            "Could not safely inspect the workspace.",
        ) from error

    def prepare_and_cleanup() -> Path:
        try:
            return _prepare_run_unlocked(
                input_path,
                workspace,
                ai_mode,
                synthetic_confirmation,
                expected_path,
            )
        finally:
            _cleanup_prepare_staging(workspace)

    return _run_locked(
        workspace,
        prepare_and_cleanup,
    )


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
    if not isinstance(run_dir, Path):
        raise SafeStop("invalid_argument", "Run directory must be a Path.")
    return _run_locked(
        run_dir,
        lambda: _record_decision_unlocked(
            run_dir,
            decision,
            reviewer_role,
            reason,
            expected_revision,
            evidence_reviewed,
            expires_at,
            decided_at,
        ),
    )


def revise_draft(
    run_dir: Path,
    replacement_path: Path,
    expected_revision: int,
) -> int:
    if not isinstance(run_dir, Path):
        raise SafeStop("invalid_argument", "Run directory must be a Path.")
    return _run_locked(
        run_dir,
        lambda: _revise_draft_unlocked(
            run_dir,
            replacement_path,
            expected_revision,
        ),
    )


def validate_candidate_summary(run_dir: Path, candidate_path: Path) -> Path:
    if not isinstance(run_dir, Path):
        raise SafeStop("invalid_argument", "Run directory must be a Path.")
    return _run_locked(
        run_dir,
        lambda: _validate_candidate_summary_unlocked(run_dir, candidate_path),
    )


def export_approved(
    run_dir: Path,
    checked_at: datetime | None = None,
) -> tuple[Path, Path]:
    if not isinstance(run_dir, Path):
        raise SafeStop("invalid_argument", "Run directory must be a Path.")
    return _run_locked(
        run_dir,
        lambda: _export_approved_unlocked(run_dir, checked_at),
    )


def inspect_run(run_dir: Path) -> dict[str, Any]:
    if not isinstance(run_dir, Path):
        raise SafeStop("invalid_argument", "Run directory must be a Path.")
    return _run_locked(run_dir, lambda: _inspect_run_unlocked(run_dir))
