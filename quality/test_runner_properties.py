"""Maintainer-only generated properties for Course 1 runner contracts.

These tests are intentionally outside ``course1_capstone/tests`` so they do
not become beginner prerequisites or silently change the frozen 67-scenario
learner runner manifest. The quality gate runs both suites.
"""

from __future__ import annotations

import copy
import csv
import io
import json
import tempfile
import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable
from unittest.mock import Mock, patch

from course1_capstone import workflow as workflow
from course1_capstone import cli as cli_module


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "practice_data" / "work_items.csv"
EXPECTED = ROOT / "practice_data" / "expected_issues.csv"
FUTURE = datetime(2099, 1, 1, tzinfo=timezone.utc)


def changed_type(value: Any) -> Any:
    if value is None:
        return ["not-null"]
    if isinstance(value, bool):
        return "not-a-boolean"
    if isinstance(value, int):
        return "not-an-integer"
    if isinstance(value, str):
        return []
    if isinstance(value, list):
        return {}
    if isinstance(value, dict):
        return []
    return None


class RunnerGeneratedPropertyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temporary.name)
        self.run_dir = workflow.prepare_run(
            INPUT,
            self.workspace,
            "mock",
            workflow.SYNTHETIC_CONFIRMATION,
            EXPECTED,
        )
        workflow.record_decision(
            self.run_dir,
            "approve",
            "course_learner",
            "Every synthetic source link and statement was reviewed.",
            1,
            True,
            FUTURE,
            None,
        )
        self.run_id = self.run_dir.name
        self.issues = workflow.read_json(self.run_dir / "issues" / "issues.json")
        self.summary = workflow.read_json(self.run_dir / "draft" / "summary.json")
        self.approval = workflow.read_json(
            self.run_dir / "review" / "decision-r1.json"
        )
        self.run_config = workflow.read_json(self.run_dir / "run_config.json")
        self.state = workflow.read_json(self.run_dir / "state.json")
        self.control = workflow.read_json(self.run_dir / "control.json")
        self.review_package = workflow.read_json(
            self.run_dir / "review" / "review_package.json"
        )
        self.review_manifest = workflow.read_json(
            self.run_dir / "review" / "review_manifest.json"
        )
        self.evaluation = workflow.read_json(self.run_dir / "evaluation.json")
        with INPUT.open("r", encoding="utf-8-sig", newline="") as stream:
            self.source_rows = list(csv.DictReader(stream))
        self.audit_events = [
            json.loads(line)
            for line in (self.run_dir / "audit" / "events.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
            if line.strip()
        ]

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def assert_safe_stop(
        self,
        validator: Callable[[Any], Any],
        value: Any,
        *,
        label: str,
    ) -> None:
        with self.subTest(label=label):
            with self.assertRaises(workflow.SafeStop):
                validator(value)

    def assert_mutation_safe_stops(
        self,
        valid: dict[str, Any],
        validator: Callable[[Any], Any],
        mutations: list[tuple[str, Callable[[dict[str, Any]], None]]],
    ) -> None:
        for label, mutate in mutations:
            with self.subTest(label=label):
                value = copy.deepcopy(valid)
                mutate(value)
                with self.assertRaises(workflow.SafeStop):
                    validator(value)

    def validators(self) -> list[tuple[str, dict[str, Any], Callable[[Any], Any]]]:
        package = self.review_package
        return [
            ("issue", self.issues[0], workflow.validate_issue),
            (
                "summary",
                self.summary,
                lambda value: workflow.validate_summary(
                    value,
                    self.issues,
                    self.run_id,
                    self.source_rows,
                ),
            ),
            ("approval", self.approval, workflow.validate_approval),
            ("run-config", self.run_config, workflow.validate_run_config),
            ("state", self.state, workflow.validate_state),
            ("control", self.control, workflow.validate_control),
            (
                "review-package",
                package,
                lambda value: workflow.validate_review_package(
                    value,
                    run_id=self.run_id,
                    draft_revision=package["draft_revision"],
                    draft_sha256=package["draft_sha256"],
                    issue_count=package["issue_count"],
                ),
            ),
            (
                "review-manifest",
                self.review_manifest,
                lambda value: workflow.validate_review_manifest(
                    value,
                    run_id=self.run_id,
                    draft_revision=package["draft_revision"],
                    run_config=self.run_config,
                ),
            ),
            (
                "audit-event",
                self.audit_events[-1],
                lambda value: workflow.validate_audit_event(
                    value,
                    expected_run_id=self.run_id,
                ),
            ),
            ("evaluation", self.evaluation, workflow.validate_evaluation),
        ]

    def test_prop_runner_001_closed_objects_reject_extra_and_missing_keys(self) -> None:
        for name, valid, validator in self.validators():
            with self.subTest(name=name, mutation="valid"):
                validator(copy.deepcopy(valid))

            extra = copy.deepcopy(valid)
            extra["unexpected_property"] = True
            self.assert_safe_stop(validator, extra, label=f"{name}:extra")

            for key in sorted(valid):
                missing = copy.deepcopy(valid)
                del missing[key]
                self.assert_safe_stop(
                    validator,
                    missing,
                    label=f"{name}:missing:{key}",
                )

    def test_prop_runner_002_every_top_level_field_rejects_wrong_type(self) -> None:
        for name, valid, validator in self.validators():
            for key, current in valid.items():
                mutated = copy.deepcopy(valid)
                mutated[key] = changed_type(current)
                self.assert_safe_stop(
                    validator,
                    mutated,
                    label=f"{name}:wrong-type:{key}",
                )

    def test_prop_runner_003_canonical_json_ignores_mapping_insertion_order(self) -> None:
        left = {
            "z": [3, 2, 1],
            "a": {"b": "synthetic", "a": 1},
            "m": True,
        }
        right = {
            "m": True,
            "a": {"a": 1, "b": "synthetic"},
            "z": [3, 2, 1],
        }
        self.assertEqual(workflow.canonical_bytes(left), workflow.canonical_bytes(right))
        self.assertEqual(
            workflow.sha256_bytes(workflow.canonical_bytes(left)),
            workflow.sha256_bytes(workflow.canonical_bytes(right)),
        )

    def test_prop_runner_004_spreadsheet_prefixes_are_always_escaped(self) -> None:
        for prefix in ("=", "+", "-", "@", "\t=", "\r+", "  -"):
            for suffix in ("1+1", "cmd", "HYPERLINK", " synthetic"):
                value = prefix + suffix
                escaped = workflow._spreadsheet_safe(value)
                self.assertEqual(escaped, "'" + value)
        for value in ("safe", "", 42, None):
            self.assertEqual(workflow._spreadsheet_safe(value), value)

    def test_prop_runner_005_datetime_parser_rejects_noncanonical_corpus(self) -> None:
        for value in (
            "",
            "2026-07-29",
            "2026-07-29 08:00:00",
            "2026-07-29T08:00:00",
            "not-a-date",
            42,
        ):
            with self.subTest(value=value):
                with self.assertRaises(workflow.SafeStop):
                    workflow.parse_datetime(value, "generated_time")
        parsed = workflow.parse_datetime(
            "2026-07-29T08:00:00Z",
            "generated_time",
        )
        self.assertEqual(workflow.iso_utc(parsed), "2026-07-29T08:00:00Z")
        offset = workflow.parse_datetime(
            "2026-07-29T10:00:00+02:00",
            "generated_time",
        )
        self.assertEqual(workflow.iso_utc(offset), "2026-07-29T08:00:00Z")

    def test_prop_runner_006_reserved_device_names_never_pass_path_preflight(
        self,
    ) -> None:
        for name in (
            "CON",
            "con.txt",
            "PRN.csv",
            "AUX",
            "NUL.json",
            "COM1",
            "COM9.log",
            "LPT1",
            "LPT9.txt",
        ):
            with self.subTest(name=name):
                with self.assertRaisesRegex(
                    workflow.SafeStop,
                    "reserved Windows device name",
                ):
                    workflow._validate_supported_path(Path(name), "Generated path")

    def test_prop_runner_007_nested_summary_control_branches_fail_closed(
        self,
    ) -> None:
        validator = lambda value: workflow.validate_summary(
            value,
            self.issues,
            self.run_id,
            self.source_rows,
        )
        first_group = self.summary["groups"][0]
        first_action = self.summary["review_actions"][0]
        mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
            ("different run", lambda value: value.__setitem__("run_id", "RUN-ABCDEF123456")),
            ("prompt version", lambda value: value.__setitem__("prompt_version", "other")),
            ("generator", lambda value: value.__setitem__("generator", "network-ai")),
            ("headline claim", lambda value: value.__setitem__("headline", "Everything is safe.")),
            ("review bypass", lambda value: value.__setitem__("review_required", False)),
            (
                "unsupported statement",
                lambda value: value.__setitem__("unsupported_statements", ["unsupported"]),
            ),
            ("empty groups", lambda value: value.__setitem__("groups", [])),
            ("group not object", lambda value: value.__setitem__("groups", ["group"])),
            (
                "empty group references",
                lambda value: value["groups"][0].__setitem__("issue_ids", []),
            ),
            (
                "non-text group reference",
                lambda value: value["groups"][0].__setitem__("issue_ids", [1]),
            ),
            (
                "duplicate group reference",
                lambda value: value["groups"][0].__setitem__(
                    "issue_ids",
                    [first_group["issue_ids"][0], first_group["issue_ids"][0]],
                ),
            ),
            (
                "unknown group reference",
                lambda value: value["groups"][0].__setitem__(
                    "issue_ids",
                    ["WI-9999|R001|title"],
                ),
            ),
            (
                "uncited group",
                lambda value: value["groups"][0].__setitem__(
                    "summary",
                    first_group["summary"].replace(
                        f"[{first_group['issue_ids'][0]}]",
                        "uncited",
                    ),
                ),
            ),
            (
                "mixed severity group",
                lambda value: value["groups"][0].__setitem__(
                    "issue_ids",
                    [
                        first_group["issue_ids"][0],
                        next(
                            issue["issue_id"]
                            for issue in self.issues
                            if issue["severity"]
                            != next(
                                candidate["severity"]
                                for candidate in self.issues
                                if candidate["issue_id"] == first_group["issue_ids"][0]
                            )
                        ),
                    ],
                ),
            ),
            (
                "changed controlled group prose",
                lambda value: value["groups"][0].__setitem__(
                    "label",
                    "Important issues",
                ),
            ),
            (
                "issue grouped twice",
                lambda value: value["groups"].append(copy.deepcopy(value["groups"][0])),
            ),
            ("missing group", lambda value: value["groups"].pop()),
            ("empty actions", lambda value: value.__setitem__("review_actions", [])),
            ("action not object", lambda value: value.__setitem__("review_actions", ["action"])),
            (
                "invalid action id",
                lambda value: value["review_actions"][0].__setitem__("action_id", "ACTION-1"),
            ),
            (
                "action type not text",
                lambda value: value["review_actions"][0].__setitem__("action_type", 1),
            ),
            (
                "unsafe action type",
                lambda value: value["review_actions"][0].__setitem__("action_type", "email"),
            ),
            (
                "external action",
                lambda value: value["review_actions"][0].__setitem__("external_action", True),
            ),
            (
                "empty action references",
                lambda value: value["review_actions"][0].__setitem__("issue_ids", []),
            ),
            (
                "non-text action reference",
                lambda value: value["review_actions"][0].__setitem__("issue_ids", [1]),
            ),
            (
                "duplicate action reference",
                lambda value: value["review_actions"][0].__setitem__(
                    "issue_ids",
                    [first_action["issue_ids"][0], first_action["issue_ids"][0]],
                ),
            ),
            (
                "more than one action reference",
                lambda value: value["review_actions"][0].__setitem__(
                    "issue_ids",
                    [
                        first_action["issue_ids"][0],
                        value["review_actions"][1]["issue_ids"][0],
                    ],
                ),
            ),
            (
                "unknown action reference",
                lambda value: value["review_actions"][0].__setitem__(
                    "issue_ids",
                    ["WI-9999|R001|title"],
                ),
            ),
            (
                "changed action instruction",
                lambda value: value["review_actions"][0].__setitem__(
                    "instruction",
                    "Send it now.",
                ),
            ),
            (
                "duplicate action id",
                lambda value: value["review_actions"][1].__setitem__(
                    "action_id",
                    value["review_actions"][0]["action_id"],
                ),
            ),
            (
                "duplicate action coverage",
                lambda value: value["review_actions"].append(
                    {
                        **copy.deepcopy(value["review_actions"][0]),
                        "action_id": "ACT-999",
                    }
                ),
            ),
            ("missing action", lambda value: value["review_actions"].pop()),
        ]
        self.assert_mutation_safe_stops(self.summary, validator, mutations)

    def test_prop_runner_008_issue_and_decision_semantics_fail_closed(self) -> None:
        issue_mutations: list[
            tuple[str, Callable[[dict[str, Any]], None]]
        ] = [
            ("issue id", lambda value: value.__setitem__("issue_id", "different")),
            (
                "work item",
                lambda value: (
                    value.__setitem__("work_item_id", "BAD-0001"),
                    value.__setitem__(
                        "issue_id",
                        f"BAD-0001|{value['rule_code']}|{value['field']}",
                    ),
                ),
            ),
            (
                "rule",
                lambda value: (
                    value.__setitem__("rule_code", "BAD"),
                    value.__setitem__(
                        "issue_id",
                        f"{value['work_item_id']}|BAD|{value['field']}",
                    ),
                ),
            ),
            (
                "field",
                lambda value: (
                    value.__setitem__("field", "unknown"),
                    value.__setitem__(
                        "issue_id",
                        f"{value['work_item_id']}|{value['rule_code']}|unknown",
                    ),
                ),
            ),
            ("severity", lambda value: value.__setitem__("severity", "critical")),
            ("source row", lambda value: value.__setitem__("source_row", 1)),
            ("message", lambda value: value.__setitem__("message", "")),
            (
                "assessment date",
                lambda value: value.__setitem__("assessment_date", "20260729"),
            ),
        ]
        self.assert_mutation_safe_stops(
            self.issues[0],
            workflow.validate_issue,
            issue_mutations,
        )

        approval_mutations: list[
            tuple[str, Callable[[dict[str, Any]], None]]
        ] = [
            ("decision value", lambda value: value.__setitem__("decision", "send")),
            ("revision zero", lambda value: value.__setitem__("draft_revision", 0)),
            ("bad decided time", lambda value: value.__setitem__("decided_at", "today")),
            ("bad expiry time", lambda value: value.__setitem__("expires_at", "tomorrow")),
            ("evidence missing", lambda value: value.__setitem__("evidence_reviewed", False)),
            (
                "expiry before decision",
                lambda value: value.__setitem__(
                    "expires_at",
                    value["decided_at"],
                ),
            ),
        ]
        self.assert_mutation_safe_stops(
            self.approval,
            workflow.validate_approval,
            approval_mutations,
        )

    def test_prop_runner_009_state_lifecycle_cross_fields_fail_closed(self) -> None:
        mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
            ("unknown state", lambda value: value.__setitem__("current_state", "sent")),
            ("negative revision", lambda value: value.__setitem__("draft_revision", -1)),
            ("bad draft hash", lambda value: value.__setitem__("draft_sha256", "bad")),
            (
                "bad review hash",
                lambda value: value.__setitem__("review_manifest_sha256", "bad"),
            ),
            (
                "bad decision path",
                lambda value: value.__setitem__("active_decision_path", "../decision.json"),
            ),
            ("bad adapter", lambda value: value.__setitem__("ai_mode_requested", "online")),
            (
                "bad generator",
                lambda value: value.__setitem__("summary_generator", "remote"),
            ),
            ("external action", lambda value: value.__setitem__("external_actions", 1)),
            ("bad export count", lambda value: value.__setitem__("local_export_count", 1)),
            ("expected keys type", lambda value: value.__setitem__("expected_keys", {})),
            (
                "malformed expected key",
                lambda value: value.__setitem__("expected_keys", [["only", "two"]]),
            ),
            (
                "duplicate expected key",
                lambda value: value.__setitem__(
                    "expected_keys",
                    [value["expected_keys"][0], value["expected_keys"][0]],
                ),
            ),
            ("no action with draft", lambda value: value.__setitem__("current_state", "no_action_needed")),
            (
                "issue state missing draft",
                lambda value: (
                    value.__setitem__("current_state", "needs_review"),
                    value.__setitem__("active_decision_path", None),
                    value.__setitem__("draft_revision", 0),
                ),
            ),
            ("needs review has decision", lambda value: value.__setitem__("current_state", "needs_review")),
            (
                "decision state missing path",
                lambda value: value.__setitem__("active_decision_path", None),
            ),
            (
                "decision revision mismatch",
                lambda value: value.__setitem__(
                    "active_decision_path",
                    "review/decision-r999.json",
                ),
            ),
            ("approved draft count", lambda value: value.__setitem__("current_state", "approved_draft")),
            (
                "early export count",
                lambda value: (
                    value.__setitem__("current_state", "approved_for_local_export"),
                    value.__setitem__("local_export_count", 2),
                ),
            ),
        ]
        self.assert_mutation_safe_stops(
            self.state,
            workflow.validate_state,
            mutations,
        )

    def test_prop_runner_010_expected_oracle_semantic_corpus_fails_closed(
        self,
    ) -> None:
        headers = [
            "issue_id",
            "work_item_id",
            "field",
            "rule_code",
            "severity",
            "expected_message",
        ]
        valid = {
            "issue_id": "WI-0001|R001|title",
            "work_item_id": "WI-0001",
            "field": "title",
            "rule_code": "R001",
            "severity": "high",
            "expected_message": "Synthetic title is required.",
        }

        def encoded(rows: list[dict[str, str]], fieldnames=headers) -> bytes:
            stream = io.StringIO(newline="")
            writer = csv.DictWriter(
                stream,
                fieldnames=fieldnames,
                extrasaction="ignore",
            )
            writer.writeheader()
            writer.writerows(rows)
            return stream.getvalue().encode("utf-8")

        invalid_values: list[tuple[str, bytes]] = [
            ("wrong headers", encoded([valid], headers[:-1])),
            ("empty", encoded([])),
            (
                "invalid work item",
                encoded([{**valid, "work_item_id": "WORK-1"}]),
            ),
            ("invalid rule", encoded([{**valid, "rule_code": "R999"}])),
            ("invalid field", encoded([{**valid, "field": "unknown"}])),
            ("inconsistent id", encoded([{**valid, "issue_id": "different"}])),
            ("invalid severity", encoded([{**valid, "severity": "low"}])),
            ("empty message", encoded([{**valid, "expected_message": ""}])),
            ("duplicate key", encoded([valid, valid])),
            (
                "oversized cell",
                encoded(
                    [
                        {
                            **valid,
                            "expected_message": "x"
                            * (workflow.MAX_CSV_CELL_CODE_POINTS + 1),
                        }
                    ]
                ),
            ),
            (
                "oversized file",
                b"x" * (workflow.MAX_EXPECTED_CSV_BYTES + 1),
            ),
        ]
        for label, value in invalid_values:
            with self.subTest(label=label):
                with self.assertRaises(workflow.SafeStop):
                    workflow._parse_expected_oracle_bytes(value)

    def test_prop_runner_011_json_complexity_and_encoding_fail_closed(self) -> None:
        cases = [
            ("depth", {"a": {"b": {"c": "deep"}}}, {"depth": workflow.MAX_JSON_DEPTH}),
            (
                "long string",
                "x" * (workflow.MAX_JSON_STRING_CODE_POINTS + 1),
                {},
            ),
            (
                "array items",
                [None] * (workflow.MAX_JSON_ARRAY_ITEMS + 1),
                {},
            ),
            (
                "object properties",
                {str(index): None for index in range(workflow.MAX_JSON_OBJECT_PROPERTIES + 1)},
                {},
            ),
            ("unsupported", {1, 2}, {}),
        ]
        for label, value, options in cases:
            with self.subTest(label=label):
                with self.assertRaises(workflow.SafeStop):
                    workflow._validate_json_complexity(
                        value,
                        "Generated JSON",
                        **options,
                    )
        with self.assertRaises(workflow.SafeStop):
            workflow._validate_json_complexity({1: "non-text key"}, "Generated JSON")
        with self.assertRaises(workflow.SafeStop):
            workflow.canonical_bytes(float("nan"))
        with self.assertRaises(workflow.SafeStop):
            workflow._decode_utf8(b"\xff", "Generated bytes", code="bad_utf8")

    def test_prop_runner_012_decision_entry_boundaries_fail_closed(self) -> None:
        reason = "All synthetic evidence was reviewed."
        calls = [
            ("unknown decision", ("send", "reviewer", reason, 1, True, None, None)),
            ("non-text role", ("approve", 1, reason, 1, True, None, None)),
            ("non-boolean review", ("approve", "reviewer", reason, 1, "yes", None, None)),
            ("bad expiry type", ("approve", "reviewer", reason, 1, True, "tomorrow", None)),
            ("bad decision time type", ("approve", "reviewer", reason, 1, True, None, "today")),
        ]
        for label, arguments in calls:
            with self.subTest(label=label):
                with self.assertRaises(workflow.SafeStop):
                    workflow._record_decision_unlocked(self.run_dir, *arguments)

        needs_review = copy.deepcopy(self.state)
        needs_review["current_state"] = "needs_review"
        needs_review["active_decision_path"] = None
        no_action = copy.deepcopy(needs_review)
        no_action["current_state"] = "no_action_needed"
        invalid_state = copy.deepcopy(needs_review)
        invalid_state["current_state"] = "approved_for_local_export"

        loaded_cases = [
            ("no action", (no_action, [], None), "edit", False, None, None),
            ("missing summary", (needs_review, self.issues, None), "edit", False, None, None),
            (
                "invalid current state",
                (invalid_state, self.issues, self.summary),
                "edit",
                False,
                None,
                None,
            ),
            (
                "expired at decision",
                (needs_review, self.issues, self.summary),
                "approve",
                True,
                FUTURE,
                FUTURE,
            ),
        ]
        for label, loaded, decision, reviewed, expires, decided in loaded_cases:
            with self.subTest(label=label):
                with patch.object(workflow, "_load_run", return_value=loaded):
                    with self.assertRaises(workflow.SafeStop):
                        workflow._record_decision_unlocked(
                            self.run_dir,
                            decision,
                            "reviewer",
                            reason,
                            1,
                            reviewed,
                            expires,
                            decided,
                        )

        with (
            patch.object(
                workflow,
                "_load_run",
                return_value=(needs_review, self.issues, self.summary),
            ),
            patch.object(workflow, "_read_bytes", return_value=b"changed"),
        ):
            with self.assertRaises(workflow.SafeStop):
                workflow._record_decision_unlocked(
                    self.run_dir,
                    "edit",
                    "reviewer",
                    reason,
                    1,
                    False,
                )

        with patch.object(
            workflow,
            "_load_run",
            return_value=(needs_review, self.issues, self.summary),
        ):
            with self.assertRaises(workflow.SafeStop):
                workflow._record_decision_unlocked(
                    self.run_dir,
                    "edit",
                    "reviewer",
                    reason,
                    1,
                    False,
                )

    def test_prop_runner_013_candidate_retry_evidence_is_atomic(self) -> None:
        def new_candidate_run(label: str) -> tuple[Path, Path]:
            run_dir = workflow.prepare_run(
                INPUT,
                self.workspace / label,
                "mock",
                workflow.SYNTHETIC_CONFIRMATION,
                EXPECTED,
            )
            candidate_path = self.workspace / f"{label}.json"
            workflow.write_json(
                candidate_path,
                workflow.read_json(run_dir / "draft" / "summary.json"),
            )
            return run_dir, candidate_path

        retry_run, retry_candidate = new_candidate_run("candidate-retry")
        result_path = workflow._validate_candidate_summary_unlocked(
            retry_run,
            retry_candidate,
        )
        self.assertEqual(
            workflow._validate_candidate_summary_unlocked(
                retry_run,
                retry_candidate,
            ),
            result_path,
        )

        result_path.unlink()
        with self.assertRaises(workflow.SafeStop):
            workflow._validate_candidate_summary_unlocked(
                retry_run,
                retry_candidate,
            )

        mismatch_run, mismatch_candidate = new_candidate_run("candidate-mismatch")
        mismatch_result = workflow._validate_candidate_summary_unlocked(
            mismatch_run,
            mismatch_candidate,
        )
        value = workflow.read_json(mismatch_result)
        value["candidate_sha256"] = "0" * 64
        workflow.write_json(mismatch_result, value)
        with self.assertRaises(workflow.SafeStop):
            workflow._validate_candidate_summary_unlocked(
                mismatch_run,
                mismatch_candidate,
            )

        needs_review = copy.deepcopy(self.state)
        needs_review["current_state"] = "needs_review"
        needs_review["active_decision_path"] = None
        with patch.object(
            workflow,
            "_load_run",
            return_value=(needs_review, self.issues, None),
        ):
            with self.assertRaises(workflow.SafeStop):
                workflow._validate_candidate_summary_unlocked(
                    self.run_dir,
                    self.workspace / "candidate.json",
                )
        with patch.object(
            workflow,
            "_load_run",
            return_value=(needs_review, self.issues, self.summary),
        ):
            with self.assertRaises(workflow.SafeStop):
                workflow._validate_candidate_summary_unlocked(
                    self.run_dir,
                    "not-a-path",
                )

    def test_prop_runner_014_audit_lifecycle_mutation_matrix_fails_closed(
        self,
    ) -> None:
        def reconcile(
            events: list[dict[str, Any]],
            *,
            state: dict[str, Any] | None = None,
            issues: list[dict[str, Any]] | None = None,
            run_dir: Path | None = None,
            source_count: int | None = None,
        ) -> None:
            workflow._reconcile_audit_history(
                run_dir or self.run_dir,
                state or self.state,
                self.issues if issues is None else issues,
                events,
                len(self.source_rows) if source_count is None else source_count,
            )

        reconcile(copy.deepcopy(self.audit_events))

        def event(event_type: str, details: dict[str, Any]) -> dict[str, Any]:
            return {
                "event_type": event_type,
                "state": "needs_review",
                "actor_type": "system",
                "details": details,
            }

        cases: list[
            tuple[
                str,
                Callable[[list[dict[str, Any]], dict[str, Any]], None],
            ]
        ] = [
            (
                "material event fields",
                lambda events, _state: events[0].__setitem__("state", "wrong"),
            ),
            (
                "receipt ordering",
                lambda events, _state: events.__setitem__(
                    slice(0, 2),
                    [events[1], events[0]],
                ),
            ),
            (
                "duplicate retries",
                lambda events, _state: events.extend(
                    [
                        event("duplicate_retry_ignored", {}),
                        event("duplicate_retry_ignored", {}),
                    ]
                ),
            ),
            (
                "bad retry evidence",
                lambda events, _state: events.append(
                    {
                        **event(
                            "duplicate_retry_ignored",
                            {
                                "input_sha256": self.state["input_sha256"],
                                "run_config_sha256": self.state["run_config_sha256"],
                                "no_duplicate_effect": True,
                            },
                        ),
                        "actor_type": "reviewer",
                    }
                ),
            ),
            (
                "contradictory no issues",
                lambda events, _state: events.append(
                    event("no_verified_issues", {}),
                ),
            ),
            (
                "conflicting generators",
                lambda events, _state: events.append(event("summary_fallback", {})),
            ),
            (
                "base order",
                lambda events, _state: events.__setitem__(
                    slice(2, 5),
                    [events[4], events[3], events[2]],
                ),
            ),
            (
                "early retry",
                lambda events, _state: events.insert(
                    0,
                    event("duplicate_retry_ignored", {}),
                ),
            ),
            (
                "decision paths",
                lambda _events, state: state.__setitem__("draft_revision", 2),
            ),
            (
                "decision evidence",
                lambda events, _state: next(
                    item
                    for item in events
                    if item["event_type"] == "review_decision_recorded"
                )["details"].__setitem__("decision_id", "DEC-000000000000"),
            ),
            (
                "impossible export",
                lambda events, _state: events.append(
                    event(
                        "local_export_created",
                        {
                            "decision_id": self.approval["decision_id"],
                            "draft_revision": 1,
                            "external_actions": 0,
                        },
                    )
                ),
            ),
            (
                "impossible expiry",
                lambda events, _state: events.append(
                    event(
                        "review_expired",
                        {
                            "decision_id": self.approval["decision_id"],
                            "draft_revision": 1,
                        },
                    )
                ),
            ),
            (
                "duplicate candidate evidence",
                lambda events, _state: events.extend(
                    [
                        event(
                            "candidate_summary_validated",
                            {"candidate_sha256": "1" * 64, "draft_revision": 1},
                        ),
                        event(
                            "candidate_summary_validated",
                            {"candidate_sha256": "1" * 64, "draft_revision": 1},
                        ),
                    ]
                ),
            ),
            (
                "candidate revision",
                lambda events, _state: events.append(
                    event(
                        "candidate_summary_validated",
                        {"candidate_sha256": "2" * 64, "draft_revision": 0},
                    )
                ),
            ),
            (
                "candidate without result",
                lambda events, _state: events.append(
                    event(
                        "candidate_summary_validated",
                        {"candidate_sha256": "3" * 64, "draft_revision": 1},
                    )
                ),
            ),
        ]
        for label, mutate in cases:
            with self.subTest(label=label):
                events = copy.deepcopy(self.audit_events)
                state = copy.deepcopy(self.state)
                mutate(events, state)
                with self.assertRaises(workflow.SafeStop):
                    reconcile(events, state=state)

        no_action_run = workflow.prepare_run(
            ROOT / "course1_capstone" / "fixtures" / "failures" / "valid_no_issue.csv",
            self.workspace / "no-action-audit",
            "mock",
            workflow.SYNTHETIC_CONFIRMATION,
            None,
        )
        no_action_state = workflow.read_json(no_action_run / "state.json")
        no_action_events = [
            json.loads(line)
            for line in (no_action_run / "audit" / "events.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        with (
            (no_action_run / "source" / "work_items.csv").open(
                "r",
                encoding="utf-8-sig",
                newline="",
            ) as stream
        ):
            no_action_rows = list(csv.DictReader(stream))
        workflow._reconcile_audit_history(
            no_action_run,
            no_action_state,
            [],
            no_action_events,
            len(no_action_rows),
        )
        for label, extra in (
            (
                "material decision in no action",
                event("review_decision_recorded", {}),
            ),
            ("unknown event in no action", event("candidate_summary_validated", {})),
        ):
            with self.subTest(label=label):
                with self.assertRaises(workflow.SafeStop):
                    workflow._reconcile_audit_history(
                        no_action_run,
                        no_action_state,
                        [],
                        [*copy.deepcopy(no_action_events), extra],
                        len(no_action_rows),
                    )

    def test_prop_runner_015_export_preconditions_fail_closed(self) -> None:
        with self.assertRaises(workflow.SafeStop):
            workflow._export_approved_unlocked(self.run_dir, "today")

        base_state = copy.deepcopy(self.state)
        loaded_cases = [
            (
                "no action",
                {**base_state, "current_state": "no_action_needed"},
                [],
                None,
            ),
            ("missing summary", base_state, self.issues, None),
            (
                "terminal",
                {**base_state, "current_state": "rejected"},
                self.issues,
                self.summary,
            ),
            (
                "review required",
                {**base_state, "current_state": "needs_review"},
                self.issues,
                self.summary,
            ),
            (
                "missing decision",
                {**base_state, "active_decision_path": None},
                self.issues,
                self.summary,
            ),
        ]
        for label, state, issues, summary in loaded_cases:
            with self.subTest(label=label):
                with patch.object(
                    workflow,
                    "_load_run",
                    return_value=(state, issues, summary),
                ):
                    with self.assertRaises(workflow.SafeStop):
                        workflow._export_approved_unlocked(self.run_dir, FUTURE)

        original_read_json = workflow.read_json

        def changed_decision(**changes: Any) -> dict[str, Any]:
            value = copy.deepcopy(self.approval)
            value.update(changes)
            material = {
                field: value[field]
                for field in sorted(workflow.APPROVAL_FIELDS - {"decision_id"})
            }
            value["decision_id"] = workflow._decision_id(material)
            return value

        decision_cases = [
            ("not approve", changed_decision(decision="reject")),
            ("wrong run", changed_decision(run_id="RUN-ABCDEF123456")),
            ("wrong revision", changed_decision(draft_revision=2)),
            ("wrong draft hash", changed_decision(draft_sha256="0" * 64)),
        ]
        for label, decision in decision_cases:
            def reader(path: Path, decision=decision):
                if Path(path).name.startswith("decision-r"):
                    return decision
                return original_read_json(path)

            with self.subTest(label=label):
                with (
                    patch.object(
                        workflow,
                        "_load_run",
                        return_value=(
                            copy.deepcopy(base_state),
                            self.issues,
                            self.summary,
                        ),
                    ),
                    patch.object(workflow, "read_json", side_effect=reader),
                ):
                    with self.assertRaises(workflow.SafeStop):
                        workflow._export_approved_unlocked(self.run_dir, FUTURE)

        draft_mismatch = copy.deepcopy(base_state)
        draft_mismatch["draft_sha256"] = "0" * 64
        manifest_mismatch = copy.deepcopy(base_state)
        manifest_mismatch["review_manifest_sha256"] = "0" * 64
        for label, state in (
            ("state draft hash", draft_mismatch),
            ("review manifest", manifest_mismatch),
        ):
            with self.subTest(label=label):
                with patch.object(
                    workflow,
                    "_load_run",
                    return_value=(state, self.issues, self.summary),
                ):
                    with self.assertRaises(workflow.SafeStop):
                        workflow._export_approved_unlocked(self.run_dir, FUTURE)

        decided_at = workflow.parse_datetime(
            self.approval["decided_at"],
            "decided_at",
        )
        with patch.object(
            workflow,
            "_load_run",
            return_value=(copy.deepcopy(base_state), self.issues, self.summary),
        ):
            with self.assertRaises(workflow.SafeStop):
                workflow._export_approved_unlocked(
                    self.run_dir,
                    decided_at.replace(year=decided_at.year - 1),
                )

    def test_prop_runner_016_path_namespace_and_inspection_matrix_fails_closed(
        self,
    ) -> None:
        paths: list[tuple[str, Any]] = [
            ("not a Path", "course"),
            ("control character", Path("bad\x01name")),
            ("bidirectional control", Path("bad\u202ename")),
            ("device namespace", Path(r"\\?\C:\synthetic-course")),
            ("network path", Path(r"\\server\synthetic-course")),
            ("trailing dot", Path("synthetic.")),
            ("alternate stream", Path("synthetic:stream")),
        ]
        for label, value in paths:
            with self.subTest(label=label):
                with self.assertRaises(workflow.SafeStop):
                    workflow._validate_supported_path(value, "Generated path")

        with self.assertRaises(workflow.SafeStop):
            workflow._validate_supported_path(
                Path("x" * (workflow.MAX_WORKSPACE_PATH_CHARACTERS + 1)),
                "Generated workspace",
                workspace_root=True,
            )
        with patch.object(Path, "absolute", side_effect=OSError("injected")):
            with self.assertRaises(workflow.SafeStop):
                workflow._validate_supported_path(Path("ordinary"), "Generated path")
        with patch.object(Path, "lstat", side_effect=OSError("injected")):
            with self.assertRaises(workflow.SafeStop):
                workflow._validate_supported_path(Path("ordinary"), "Generated path")

    def test_prop_runner_017_operation_lock_error_matrix_fails_closed(self) -> None:
        with self.assertRaises(workflow.SafeStop):
            with workflow._exclusive_operation_lock("not-a-path"):
                pass

        scope_file = self.workspace / "lock-scope-file"
        scope_file.write_text("file", encoding="utf-8")
        with self.assertRaises(workflow.SafeStop):
            with workflow._exclusive_operation_lock(scope_file):
                pass

        exists_error_scope = self.workspace / "exists-error"
        with patch.object(Path, "exists", side_effect=OSError("injected")):
            with self.assertRaises(workflow.SafeStop):
                with workflow._exclusive_operation_lock(exists_error_scope):
                    pass

        resolve_error_scope = self.workspace / "resolve-error"
        original_resolve = Path.resolve

        def resolve_or_fail(path: Path, *args: Any, **kwargs: Any) -> Path:
            if path == resolve_error_scope:
                raise OSError("injected")
            return original_resolve(path, *args, **kwargs)

        with patch.object(Path, "resolve", resolve_or_fail):
            with self.assertRaises(workflow.SafeStop):
                with workflow._exclusive_operation_lock(resolve_error_scope):
                    pass

        nested_scope = self.workspace / "nested-lock"
        with workflow._exclusive_operation_lock(nested_scope):
            with workflow._exclusive_operation_lock(nested_scope):
                self.assertTrue(
                    (nested_scope / workflow.OPERATION_LOCK_NAME).is_file()
                )

        stale_scope = self.workspace / "stale-lock"
        stale_scope.mkdir()
        (stale_scope / workflow.OPERATION_LOCK_NAME).mkdir()
        with self.assertRaises(workflow.SafeStop):
            with workflow._exclusive_operation_lock(stale_scope):
                pass

        safe_stop_scope = self.workspace / "safe-stop-lock"
        with patch.object(
            workflow,
            "utc_now",
            return_value=datetime(2026, 7, 29),
        ):
            with self.assertRaises(workflow.SafeStop):
                with workflow._exclusive_operation_lock(safe_stop_scope):
                    pass
        self.assertFalse((safe_stop_scope / workflow.OPERATION_LOCK_NAME).exists())

        write_error_scope = self.workspace / "write-error-lock"
        with patch.object(workflow.os, "write", side_effect=OSError("injected")):
            with self.assertRaises(workflow.SafeStop):
                with workflow._exclusive_operation_lock(write_error_scope):
                    pass
        self.assertFalse((write_error_scope / workflow.OPERATION_LOCK_NAME).exists())

        missing_release_scope = self.workspace / "missing-release-lock"
        with workflow._exclusive_operation_lock(missing_release_scope):
            (missing_release_scope / workflow.OPERATION_LOCK_NAME).unlink()

        release_error_scope = self.workspace / "release-error-lock"
        lock_path = release_error_scope / workflow.OPERATION_LOCK_NAME
        original_unlink = Path.unlink

        def unlink_or_fail(path: Path, *args: Any, **kwargs: Any) -> None:
            if path == lock_path:
                raise OSError("injected")
            original_unlink(path, *args, **kwargs)

        with patch.object(Path, "unlink", unlink_or_fail):
            with self.assertRaises(workflow.SafeStop):
                with workflow._exclusive_operation_lock(release_error_scope):
                    pass

    def test_prop_runner_018_load_run_integrity_matrix_fails_closed(self) -> None:
        with self.assertRaises(workflow.SafeStop):
            workflow._load_run("not-a-path")

        transaction_marker = self.run_dir / workflow.TRANSACTION_INCOMPLETE_NAME
        transaction_marker.write_text("incomplete", encoding="utf-8")
        try:
            with self.assertRaises(workflow.SafeStop):
                workflow._load_run(self.run_dir)
        finally:
            transaction_marker.unlink()

        original_read_json = workflow.read_json

        def with_state(state: dict[str, Any]):
            def reader(path: Path):
                if Path(path).name == "state.json":
                    return copy.deepcopy(state)
                return original_read_json(path)

            return reader

        different_run = copy.deepcopy(self.state)
        different_run["run_id"] = "RUN-ABCDEF123456"
        config_mismatch = copy.deepcopy(self.state)
        config_mismatch["run_config_sha256"] = "0" * 64
        state_config_mismatch = copy.deepcopy(self.state)
        state_config_mismatch["assessment_date"] = "2026-07-25"
        for label, state in (
            ("directory identity", different_run),
            ("config hash", config_mismatch),
            ("state config fields", state_config_mismatch),
        ):
            with self.subTest(label=label):
                with patch.object(workflow, "read_json", side_effect=with_state(state)):
                    with self.assertRaises(workflow.SafeStop):
                        workflow._load_run(self.run_dir)

        with patch.object(
            workflow,
            "_run_id_from_config",
            return_value="RUN-ABCDEF123456",
        ):
            with self.assertRaises(workflow.SafeStop):
                workflow._load_run(self.run_dir)

        with patch.object(workflow, "PIPELINE_VERSION", "unsupported"):
            with self.assertRaises(workflow.SafeStop):
                workflow._load_run(self.run_dir)

        def issues_not_list(path: Path):
            if Path(path).name == "issues.json":
                return {"not": "a list"}
            return original_read_json(path)

        with patch.object(workflow, "read_json", side_effect=issues_not_list):
            with self.assertRaises(workflow.SafeStop):
                workflow._load_run(self.run_dir)

        with patch.object(workflow, "_load_audit_events", return_value=[]):
            with self.assertRaises(workflow.SafeStop):
                workflow._load_run(self.run_dir)

        prompt_mismatch = copy.deepcopy(self.state)
        original_summary = copy.deepcopy(self.summary)
        changed_summary = copy.deepcopy(self.summary)
        changed_summary["prompt_version"] = "other"

        def changed_summary_reader(path: Path):
            if Path(path).name == "state.json":
                return prompt_mismatch
            if Path(path).name == "summary.json":
                return changed_summary
            return original_read_json(path)

        with (
            patch.object(workflow, "read_json", side_effect=changed_summary_reader),
            patch.object(workflow, "validate_summary", return_value=None),
        ):
            with self.assertRaises(workflow.SafeStop):
                workflow._load_run(self.run_dir)

        manifest_mismatch = copy.deepcopy(self.state)
        manifest_mismatch["review_manifest_sha256"] = "0" * 64
        with patch.object(
            workflow,
            "read_json",
            side_effect=with_state(manifest_mismatch),
        ):
            with self.assertRaises(workflow.SafeStop):
                workflow._load_run(self.run_dir)

        reject_decision = copy.deepcopy(self.approval)
        reject_decision["decision"] = "reject"
        reject_decision["decision_id"] = workflow._decision_id(
            {
                field: reject_decision[field]
                for field in sorted(workflow.APPROVAL_FIELDS - {"decision_id"})
            }
        )

        def reject_reader(path: Path):
            if Path(path).name.startswith("decision-r"):
                return reject_decision
            return original_read_json(path)

        with patch.object(workflow, "read_json", side_effect=reject_reader):
            with self.assertRaises(workflow.SafeStop):
                workflow._load_run(self.run_dir)

        outbox = self.run_dir / "outbox"
        outbox.mkdir(exist_ok=True)
        unexpected_json = outbox / "approved-r1.json"
        unexpected_csv = outbox / "approved-r1.csv"
        unexpected_json.write_bytes(b"synthetic")
        unexpected_csv.write_bytes(b"synthetic")
        try:
            with self.assertRaises(workflow.SafeStop):
                workflow._load_run(self.run_dir)
        finally:
            unexpected_json.unlink()
            unexpected_csv.unlink()

    def test_prop_runner_019_revision_preconditions_fail_closed(self) -> None:
        with self.assertRaises(workflow.SafeStop):
            workflow._revise_draft_unlocked(self.run_dir, "not-a-path", 1)

        changes_requested = copy.deepcopy(self.state)
        changes_requested["current_state"] = "changes_requested"
        loaded_cases = [
            (
                "no action",
                ({**changes_requested, "current_state": "no_action_needed"}, [], None),
                1,
            ),
            (
                "wrong state",
                (self.state, self.issues, self.summary),
                1,
            ),
            (
                "stale revision",
                (changes_requested, self.issues, self.summary),
                2,
            ),
        ]
        for label, loaded, revision in loaded_cases:
            with self.subTest(label=label):
                with patch.object(workflow, "_load_run", return_value=loaded):
                    with self.assertRaises(workflow.SafeStop):
                        workflow._revise_draft_unlocked(
                            self.run_dir,
                            self.run_dir / "draft" / "summary.json",
                            revision,
                        )

        with patch.object(
            workflow,
            "_load_run",
            return_value=(changes_requested, self.issues, self.summary),
        ):
            with self.assertRaises(workflow.SafeStop):
                workflow._revise_draft_unlocked(
                    self.run_dir,
                    self.run_dir / "draft" / "summary.json",
                    1,
                )

    def test_prop_runner_020_revision_export_and_expiry_audit_matrix(
        self,
    ) -> None:
        def rows_for(run_dir: Path) -> list[dict[str, str]]:
            with (run_dir / "source" / "work_items.csv").open(
                "r",
                encoding="utf-8-sig",
                newline="",
            ) as stream:
                return list(csv.DictReader(stream))

        def events_for(run_dir: Path) -> list[dict[str, Any]]:
            return [
                json.loads(line)
                for line in (run_dir / "audit" / "events.jsonl")
                .read_text(encoding="utf-8")
                .splitlines()
            ]

        def reconcile_run(
            run_dir: Path,
            state: dict[str, Any],
            events: list[dict[str, Any]],
        ) -> None:
            issues = workflow.read_json(run_dir / "issues" / "issues.json")
            workflow._reconcile_audit_history(
                run_dir,
                state,
                issues,
                events,
                len(rows_for(run_dir)),
            )

        retry_details = {
            "input_sha256": self.state["input_sha256"],
            "run_config_sha256": self.state["run_config_sha256"],
            "no_duplicate_effect": True,
        }
        no_action_run = workflow.prepare_run(
            ROOT / "course1_capstone" / "fixtures" / "failures" / "valid_no_issue.csv",
            self.workspace / "no-action-branches",
            "mock",
            workflow.SYNTHETIC_CONFIRMATION,
            None,
        )
        no_action_state = workflow.read_json(no_action_run / "state.json")
        no_action_events = events_for(no_action_run)
        no_issues_position = next(
            index
            for index, value in enumerate(no_action_events)
            if value["event_type"] == "no_verified_issues"
        )
        retry_event = {
            **copy.deepcopy(no_action_events[-1]),
            "event_type": "duplicate_retry_ignored",
            "state": "no_action_needed",
            "actor_type": "system",
            "details": retry_details,
        }
        early_no_action = copy.deepcopy(no_action_events)
        early_no_action.insert(no_issues_position, retry_event)
        with self.assertRaises(workflow.SafeStop):
            reconcile_run(no_action_run, no_action_state, early_no_action)
        with self.assertRaises(workflow.SafeStop):
            workflow._reconcile_audit_history(
                no_action_run,
                no_action_state,
                [copy.deepcopy(self.issues[0])],
                no_action_events,
                len(rows_for(no_action_run)),
            )

        early_issue_retry = copy.deepcopy(self.audit_events)
        review_position = next(
            index
            for index, value in enumerate(early_issue_retry)
            if value["event_type"] == "human_review_required"
        )
        issue_retry = {
            **copy.deepcopy(early_issue_retry[-1]),
            "event_type": "duplicate_retry_ignored",
            "state": "needs_review",
            "actor_type": "system",
            "details": retry_details,
        }
        early_issue_retry.insert(review_position, issue_retry)
        with self.assertRaises(workflow.SafeStop):
            workflow._reconcile_audit_history(
                self.run_dir,
                self.state,
                self.issues,
                early_issue_retry,
                len(self.source_rows),
            )

        revision_run = workflow.prepare_run(
            INPUT,
            self.workspace / "revision-audit",
            "mock",
            workflow.SYNTHETIC_CONFIRMATION,
            EXPECTED,
        )
        workflow.record_decision(
            revision_run,
            "edit",
            "reviewer",
            "Revise the controlled synthetic summary.",
            1,
            False,
            FUTURE,
            None,
        )
        replacement = workflow.read_json(revision_run / "draft" / "summary.json")
        replacement["headline"] = (
            f"Human review is required for {len(self.issues)} verified synthetic issues."
        )
        replacement_path = self.workspace / "revision-replacement.json"
        workflow.write_json(replacement_path, replacement)
        workflow.revise_draft(revision_run, replacement_path, 1)
        revision_state = workflow.read_json(revision_run / "state.json")
        revision_events = events_for(revision_run)
        reconcile_run(revision_run, revision_state, revision_events)

        missing_revision_event = [
            value
            for value in copy.deepcopy(revision_events)
            if value["event_type"] != "draft_revision_created"
        ]
        with self.assertRaises(workflow.SafeStop):
            reconcile_run(revision_run, revision_state, missing_revision_event)

        wrong_revision_event = copy.deepcopy(revision_events)
        next(
            value
            for value in wrong_revision_event
            if value["event_type"] == "draft_revision_created"
        )["details"]["previous_revision"] = 99
        with self.assertRaises(workflow.SafeStop):
            reconcile_run(revision_run, revision_state, wrong_revision_event)

        decision_path = revision_run / "review" / "decision-r1.json"
        original_decision_bytes = decision_path.read_bytes()
        changed_decision = workflow.read_json(decision_path)
        changed_decision["decision"] = "approve"
        changed_decision["evidence_reviewed"] = True
        changed_decision["decision_id"] = workflow._decision_id(
            {
                field: changed_decision[field]
                for field in sorted(workflow.APPROVAL_FIELDS - {"decision_id"})
            }
        )
        workflow.write_json(decision_path, changed_decision)
        try:
            with self.assertRaises(workflow.SafeStop):
                reconcile_run(revision_run, revision_state, revision_events)
        finally:
            workflow.atomic_write_bytes(decision_path, original_decision_bytes)

        reordered_revision = copy.deepcopy(revision_events)
        decision_index = next(
            index
            for index, value in enumerate(reordered_revision)
            if value["event_type"] == "review_decision_recorded"
        )
        revision_index = next(
            index
            for index, value in enumerate(reordered_revision)
            if value["event_type"] == "draft_revision_created"
        )
        reordered_revision[decision_index], reordered_revision[revision_index] = (
            reordered_revision[revision_index],
            reordered_revision[decision_index],
        )
        with self.assertRaises(workflow.SafeStop):
            reconcile_run(revision_run, revision_state, reordered_revision)

        export_run = workflow.prepare_run(
            INPUT,
            self.workspace / "export-audit",
            "mock",
            workflow.SYNTHETIC_CONFIRMATION,
            EXPECTED,
        )
        workflow.record_decision(
            export_run,
            "approve",
            "reviewer",
            "All synthetic evidence was reviewed.",
            1,
            True,
            FUTURE,
            None,
        )
        workflow.export_approved(export_run, datetime(2098, 1, 1, tzinfo=timezone.utc))
        export_state = workflow.read_json(export_run / "state.json")
        export_events = events_for(export_run)
        reconcile_run(export_run, export_state, export_events)

        without_export = [
            value
            for value in copy.deepcopy(export_events)
            if value["event_type"] != "local_export_created"
        ]
        with self.assertRaises(workflow.SafeStop):
            reconcile_run(export_run, export_state, without_export)

        wrong_export = copy.deepcopy(export_events)
        next(
            value
            for value in wrong_export
            if value["event_type"] == "local_export_created"
        )["details"]["decision_id"] = "DEC-000000000000"
        with self.assertRaises(workflow.SafeStop):
            reconcile_run(export_run, export_state, wrong_export)

        moved_export = copy.deepcopy(export_events)
        export_index = next(
            index
            for index, value in enumerate(moved_export)
            if value["event_type"] == "local_export_created"
        )
        decision_index = next(
            index
            for index, value in enumerate(moved_export)
            if value["event_type"] == "review_decision_recorded"
        )
        export_value = moved_export.pop(export_index)
        moved_export.insert(decision_index, export_value)
        with self.assertRaises(workflow.SafeStop):
            reconcile_run(export_run, export_state, moved_export)

        expiry_run = workflow.prepare_run(
            INPUT,
            self.workspace / "expiry-audit",
            "mock",
            workflow.SYNTHETIC_CONFIRMATION,
            EXPECTED,
        )
        decided = workflow.utc_now() + timedelta(seconds=1)
        expires = decided + timedelta(hours=1)
        workflow.record_decision(
            expiry_run,
            "approve",
            "reviewer",
            "All synthetic evidence was reviewed.",
            1,
            True,
            expires,
            decided,
        )
        with self.assertRaises(workflow.SafeStop):
            workflow.export_approved(expiry_run, expires + timedelta(seconds=1))
        expiry_state = workflow.read_json(expiry_run / "state.json")
        expiry_events = events_for(expiry_run)
        reconcile_run(expiry_run, expiry_state, expiry_events)

        without_expiry = [
            value
            for value in copy.deepcopy(expiry_events)
            if value["event_type"] != "review_expired"
        ]
        with self.assertRaises(workflow.SafeStop):
            reconcile_run(expiry_run, expiry_state, without_expiry)

        wrong_expiry = copy.deepcopy(expiry_events)
        next(
            value
            for value in wrong_expiry
            if value["event_type"] == "review_expired"
        )["details"]["decision_id"] = "DEC-000000000000"
        with self.assertRaises(workflow.SafeStop):
            reconcile_run(expiry_run, expiry_state, wrong_expiry)

        candidate_events = copy.deepcopy(self.audit_events)
        decision_position = next(
            index
            for index, value in enumerate(candidate_events)
            if value["event_type"] == "review_decision_recorded"
        )
        candidate = {
            **copy.deepcopy(candidate_events[-1]),
            "event_type": "candidate_summary_validated",
            "state": "needs_review",
            "actor_type": "system",
            "details": {
                "candidate_sha256": "a" * 64,
                "draft_revision": 1,
            },
        }
        candidate_events.insert(decision_position, copy.deepcopy(candidate))
        candidate_events.insert(decision_position + 1, copy.deepcopy(candidate))
        with self.assertRaises(workflow.SafeStop):
            workflow._reconcile_audit_history(
                self.run_dir,
                self.state,
                self.issues,
                candidate_events,
                len(self.source_rows),
            )

    def test_prop_runner_021_cli_failure_evidence_branches_are_named(self) -> None:
        prepare_args = Namespace(command="prepare", workspace=self.workspace)
        run_args = Namespace(command="status", run_dir=self.run_dir)
        unknown_args = Namespace(command="unknown")
        self.assertEqual(
            cli_module.command_artifact_base(prepare_args),
            self.workspace.resolve(),
        )
        self.assertEqual(
            cli_module.command_artifact_base(run_args),
            self.run_dir.resolve(),
        )
        self.assertIsNone(cli_module.command_artifact_base(unknown_args))

        with self.assertRaises(workflow.SafeStop):
            cli_module.relative_artifact_locator(
                self.workspace / "outside.txt",
                self.workspace / "inside",
            )

        concurrent = workflow.SafeStop("concurrent_operation", "busy")
        ordinary = workflow.SafeStop("generated_failure", "synthetic failure")
        self.assertIsNone(
            cli_module._record_safe_stop_unlocked(run_args, concurrent)
        )
        self.assertIsNone(
            cli_module._record_safe_stop_unlocked(unknown_args, ordinary)
        )
        with patch.object(cli_module, "write_json", side_effect=OSError("injected")):
            self.assertIsNone(
                cli_module._record_safe_stop_unlocked(prepare_args, ordinary)
            )

        audit_base = self.workspace / "cli-audit-error"
        audit_base.mkdir()
        cli_module.write_json(
            audit_base / "state.json",
            {"run_id": "RUN-ABCDEF123456"},
        )
        audit_args = Namespace(command="status", run_dir=audit_base)
        with patch.object(
            cli_module,
            "append_audit_event",
            side_effect=ValueError("injected"),
        ):
            evidence = cli_module._record_safe_stop_unlocked(audit_args, ordinary)
        self.assertIsNotNone(evidence)
        self.assertEqual(
            cli_module.read_json(evidence)["audit_error"],
            "ValueError",
        )

        self.assertIsNone(cli_module.record_safe_stop(run_args, concurrent))
        self.assertIsNone(cli_module.record_safe_stop(unknown_args, ordinary))
        with patch.object(
            cli_module,
            "_exclusive_operation_lock",
            side_effect=workflow.SafeStop("lock_error", "injected"),
        ):
            self.assertIsNone(cli_module.record_safe_stop(run_args, ordinary))

        revise_args = Namespace(
            command="revise",
            run_dir=self.run_dir,
            replacement=self.workspace / "replacement.json",
            expected_revision=1,
        )
        output = io.StringIO()
        with (
            patch.object(cli_module, "revise_draft", return_value=2),
            redirect_stdout(output),
        ):
            self.assertEqual(cli_module._main_with_args(revise_args), 0)
        self.assertIn("revision 2", output.getvalue())

        failing_args = Namespace(
            command="prepare",
            input=INPUT,
            workspace=self.workspace / "cli-main-failure",
            ai_mode="mock",
            synthetic_confirmation=workflow.SYNTHETIC_CONFIRMATION,
            expected=EXPECTED,
        )
        output = io.StringIO()
        with (
            patch.object(
                cli_module,
                "prepare_run",
                side_effect=workflow.SafeStop("injected", "failure"),
            ),
            patch.object(cli_module, "record_safe_stop", return_value=None),
            redirect_stdout(output),
        ):
            self.assertEqual(cli_module._main_with_args(failing_args), 1)
        self.assertIn("FAILURE_EVIDENCE=unavailable", output.getvalue())

        fake_parser = Mock()
        fake_parser.parse_args.return_value = unknown_args
        with (
            patch.object(cli_module, "build_parser", return_value=fake_parser),
            patch.object(cli_module, "_main_with_args", return_value=7),
        ):
            self.assertEqual(cli_module.main(), 7)


if __name__ == "__main__":
    unittest.main()
