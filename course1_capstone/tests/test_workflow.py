from __future__ import annotations

import argparse
import ast
import contextlib
import csv
import hashlib
import io
import json
import os
import sys
import tempfile
import threading
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from course1_capstone import cli as cli_module
from course1_capstone import workflow as workflow_module
from course1_capstone.cli import main as cli_main, record_safe_stop
from course1_capstone.workflow import (
    SYNTHETIC_CONFIRMATION,
    SafeStop,
    export_approved,
    inspect_run,
    prepare_run,
    read_json,
    record_decision,
    revise_draft,
    validate_candidate_summary,
    validate_evaluation,
    validate_issue,
    validate_state,
    write_json,
)

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "course1_capstone" / "fixtures"
FROZEN_INPUT = ROOT / "practice_data" / "work_items.csv"
FROZEN_EXPECTED = ROOT / "practice_data" / "expected_issues.csv"
DECIDED = datetime(2026, 7, 28, 10, 0, tzinfo=timezone.utc)
FUTURE = datetime(2099, 1, 1, 0, 0, tzinfo=timezone.utc)
CHECKED = datetime(2026, 7, 28, 11, 0, tzinfo=timezone.utc)


class WorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def prepare(
        self,
        *,
        input_path: Path = FROZEN_INPUT,
        expected_path: Path | None = FROZEN_EXPECTED,
        mode: str = "mock",
        workspace_name: str = "workspace",
    ) -> Path:
        return prepare_run(
            input_path,
            self.workspace / workspace_name,
            mode,
            SYNTHETIC_CONFIRMATION,
            expected_path,
        )

    def approve(self, run_dir: Path, revision: int = 1) -> Path:
        return record_decision(
            run_dir,
            "approve",
            "course_learner",
            "Every synthetic source link and statement was reviewed.",
            revision,
            True,
            FUTURE,
            DECIDED,
        )

    def assert_safe_stop(self, code: str, function, *args, **kwargs) -> SafeStop:
        with self.assertRaises(SafeStop) as caught:
            function(*args, **kwargs)
        self.assertEqual(caught.exception.code, code)
        return caught.exception

    def run_cli(self, arguments: list[str]) -> tuple[int, str]:
        output = io.StringIO()
        with (
            patch.object(
                sys,
                "argv",
                ["course1-capstone", *arguments],
            ),
            contextlib.redirect_stdout(output),
        ):
            result = cli_main()
        return result, output.getvalue()

    def test_runtime_has_no_network_or_process_connector_import(self) -> None:
        source_path = ROOT / "course1_capstone" / "workflow.py"
        tree = ast.parse(source_path.read_text(encoding="utf-8"))
        imported_roots: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".")[0])
        forbidden = {
            "aiohttp",
            "ftplib",
            "http",
            "paramiko",
            "requests",
            "smtplib",
            "socket",
            "subprocess",
            "urllib",
        }
        self.assertEqual(imported_roots & forbidden, set())

    def test_frozen_input_detects_exact_thirteen_triple_keys(self) -> None:
        run_dir = self.prepare()
        issues = read_json(run_dir / "issues" / "issues.json")
        expected_rows = list(
            csv.DictReader(FROZEN_EXPECTED.read_text(encoding="utf-8").splitlines())
        )
        found = {
            (row["work_item_id"], row["rule_code"], row["field"]) for row in issues
        }
        expected = {
            (row["work_item_id"], row["rule_code"], row["field"])
            for row in expected_rows
        }
        self.assertEqual(found, expected)
        self.assertEqual(len(found), 13)
        self.assertEqual(
            len({row["issue_id"] for row in issues}),
            13,
        )
        for row in issues:
            self.assertEqual(
                row["issue_id"],
                f"{row['work_item_id']}|{row['rule_code']}|{row['field']}",
            )
            self.assertGreaterEqual(row["source_row"], 2)

    def test_every_issue_field_wrong_type_safely_stops_without_raw_error(self) -> None:
        run_dir = self.prepare()
        original = read_json(run_dir / "issues" / "issues.json")[0]
        wrong_types = {
            "issue_id": [],
            "work_item_id": 42,
            "source_reference": {"unexpected": "object"},
            "source_row": "2",
            "field": ["status"],
            "raw_value": False,
            "rule_code": {"unexpected": "object"},
            "severity": ["high"],
            "message": None,
            "assessment_date": 20260728,
        }
        self.assertEqual(set(wrong_types), set(original))
        for field, wrong_value in wrong_types.items():
            with self.subTest(field=field):
                candidate = dict(original)
                candidate[field] = wrong_value
                self.assert_safe_stop(
                    "invalid_issue",
                    validate_issue,
                    candidate,
                )
        state = read_json(run_dir / "state.json")
        for field, expected_code in (
            ("external_actions", "external_action_blocked"),
            ("local_export_count", "state_contract"),
        ):
            with self.subTest(field=field, wrong_type="boolean"):
                wrong_state = dict(state)
                wrong_state[field] = False
                self.assert_safe_stop(expected_code, validate_state, wrong_state)
        evaluation = read_json(run_dir / "evaluation.json")
        wrong_evaluation = dict(evaluation)
        wrong_evaluation["external_actions"] = False
        self.assert_safe_stop(
            "external_action_blocked",
            validate_evaluation,
            wrong_evaluation,
        )
        self.assert_safe_stop(
            "invalid_decision",
            record_decision,
            run_dir,
            "approve",
            "course_learner",
            "Reviewed.",
            True,
            True,
            FUTURE,
            DECIDED,
        )

    def test_latest_run_locator_is_relative_to_workspace(self) -> None:
        run_dir = self.prepare()
        workspace = self.workspace / "workspace"
        locator = (workspace / "latest_run.txt").read_text(encoding="utf-8").strip()
        self.assertEqual(locator, f"runs/{run_dir.name}")
        self.assertNotIn(str(self.workspace), locator)
        self.assertEqual((workspace / Path(locator)).resolve(), run_dir.resolve())

    def test_recreated_input_detects_exact_five_triple_keys(self) -> None:
        run_dir = self.prepare(
            input_path=FIXTURES / "recreated_work_items.csv",
            expected_path=FIXTURES / "recreated_expected_issues.csv",
        )
        evaluation = read_json(run_dir / "evaluation.json")
        self.assertEqual(evaluation["detected_issue_count"], 5)
        self.assertEqual(evaluation["true_positives"], 5)
        self.assertEqual(evaluation["false_positives"], 0)
        self.assertEqual(evaluation["false_negatives"], 0)

    def test_missing_required_value_creates_r001_source_link(self) -> None:
        run_dir = self.prepare()
        issues = read_json(run_dir / "issues" / "issues.json")
        issue = next(
            row
            for row in issues
            if (
                row["work_item_id"],
                row["rule_code"],
                row["field"],
            )
            == ("WI-0013", "R001", "title")
        )
        self.assertEqual(issue["raw_value"], "")
        self.assertGreaterEqual(issue["source_row"], 2)

    def test_invalid_status_creates_r002(self) -> None:
        run_dir = self.prepare()
        keys = {
            (row["work_item_id"], row["rule_code"], row["field"])
            for row in read_json(run_dir / "issues" / "issues.json")
        }
        self.assertIn(("WI-0014", "R002", "status"), keys)

    def test_duplicate_reference_creates_r010_for_both_source_rows(self) -> None:
        run_dir = self.prepare()
        issues = [
            row
            for row in read_json(run_dir / "issues" / "issues.json")
            if row["rule_code"] == "R010"
        ]
        self.assertEqual(
            {row["work_item_id"] for row in issues},
            {"WI-0006", "WI-0007"},
        )
        self.assertTrue(all(row["source_reference"] == "REF-1006" for row in issues))

    def test_contradictory_dates_create_r005(self) -> None:
        run_dir = self.prepare()
        keys = {
            (row["work_item_id"], row["rule_code"], row["field"])
            for row in read_json(run_dir / "issues" / "issues.json")
        }
        self.assertIn(("WI-0003", "R005", "due_date"), keys)

    def test_overdue_open_item_creates_r011_on_fixed_date(self) -> None:
        run_dir = self.prepare()
        issues = read_json(run_dir / "issues" / "issues.json")
        issue = next(row for row in issues if row["rule_code"] == "R011")
        self.assertEqual(issue["work_item_id"], "WI-0010")
        self.assertEqual(issue["assessment_date"], "2026-07-26")

    def test_valid_row_ends_in_named_no_action_needed_state(self) -> None:
        run_dir = self.prepare(
            input_path=FIXTURES / "failures" / "valid_no_issue.csv",
            expected_path=None,
        )
        status = inspect_run(run_dir)
        self.assertEqual(status["current_state"], "no_action_needed")
        self.assertEqual(status["issue_count"], 0)
        self.assertEqual(status["external_actions"], 0)
        self.assertFalse((run_dir / "draft").exists())
        self.assertFalse((run_dir / "outbox").exists())
        self.assert_safe_stop(
            "no_action_needed",
            export_approved,
            run_dir,
            CHECKED,
        )

    def test_duplicate_work_item_id_safely_stops(self) -> None:
        self.assert_safe_stop(
            "duplicate_work_item_id",
            self.prepare,
            input_path=FIXTURES / "failures" / "duplicate_work_item_id.csv",
            expected_path=None,
        )

    def test_required_review_without_evidence_safely_stops(self) -> None:
        run_dir = self.prepare()
        self.assert_safe_stop(
            "review_evidence_required",
            record_decision,
            run_dir,
            "approve",
            "course_learner",
            "I looked at the draft but did not verify the evidence.",
            1,
            False,
            FUTURE,
            DECIDED,
        )
        self.assertFalse((run_dir / "review" / "decision-r1.json").exists())
        self.assertFalse((run_dir / "outbox").exists())

    def test_stale_update_safely_stops(self) -> None:
        run_dir = self.prepare()
        self.assert_safe_stop(
            "stale_update",
            record_decision,
            run_dir,
            "approve",
            "course_learner",
            "Reviewed.",
            2,
            True,
            FUTURE,
            DECIDED,
        )

    def test_missing_input_file_safely_stops(self) -> None:
        self.assert_safe_stop(
            "missing_file",
            self.prepare,
            input_path=self.workspace / "does-not-exist.csv",
            expected_path=None,
        )
        self.assert_safe_stop(
            "file_read_error",
            self.prepare,
            input_path=self.workspace,
            expected_path=None,
            workspace_name="directory-input",
        )
        self.assert_safe_stop(
            "invalid_argument",
            prepare_run,
            "not-a-path",
            self.workspace,
            "mock",
            SYNTHETIC_CONFIRMATION,
            None,
        )
        io_workspace = self.workspace / "io-failure-evidence"
        result, output = self.run_cli(
            [
                "prepare",
                "--input",
                str(self.workspace),
                "--workspace",
                str(io_workspace),
                "--ai-mode",
                "mock",
                "--synthetic-confirmation",
                SYNTHETIC_CONFIRMATION,
            ]
        )
        self.assertEqual(result, 1)
        self.assertIn("SAFE STOP: file_read_error", output)
        self.assertNotIn("Traceback", output)
        self.assertEqual(
            read_json(io_workspace / "failures" / "latest.json")["error_code"],
            "file_read_error",
        )

    def test_cli_persists_named_failure_evidence(self) -> None:
        workspace = self.workspace / "cli-failure"
        result, command_output = self.run_cli(
            [
                "prepare",
                "--input",
                str(self.workspace / "does-not-exist.csv"),
                "--workspace",
                str(workspace),
                "--ai-mode",
                "mock",
                "--synthetic-confirmation",
                SYNTHETIC_CONFIRMATION,
            ]
        )
        self.assertEqual(result, 1)
        evidence = workspace / "failures" / "latest.json"
        self.assertTrue(evidence.exists())
        record = read_json(evidence)
        self.assertEqual(record["state"], "failed_manual")
        self.assertEqual(record["error_code"], "missing_file")
        self.assertEqual(record["external_actions"], 0)
        self.assertIn(
            "FAILURE_EVIDENCE=failures/latest.json",
            command_output,
        )
        self.assertNotIn(str(self.workspace), command_output)
        self.assertNotIn(str(self.workspace), record["message"])
        self.assertIn("does-not-exist.csv", record["message"])

    def test_all_missing_path_roles_are_sanitized_in_cli_evidence(self) -> None:
        scenarios = [
            {
                "name": "expected_file",
                "arguments": [
                    "prepare",
                    "--input",
                    str(FROZEN_INPUT),
                    "--expected",
                    str(self.workspace / "private-folder" / "expected.csv"),
                    "--workspace",
                    str(self.workspace / "missing-expected-workspace"),
                    "--ai-mode",
                    "mock",
                    "--synthetic-confirmation",
                    SYNTHETIC_CONFIRMATION,
                ],
                "evidence": (
                    self.workspace
                    / "missing-expected-workspace"
                    / "failures"
                    / "latest.json"
                ),
                "visible_name": "expected.csv",
            },
            {
                "name": "required_json",
                "arguments": [
                    "status",
                    "--run-dir",
                    str(self.workspace / "private-folder" / "missing-run"),
                ],
                "evidence": (
                    self.workspace
                    / "private-folder"
                    / "missing-run"
                    / "failures"
                    / "latest.json"
                ),
                "visible_name": "state.json",
            },
        ]
        for scenario in scenarios:
            with self.subTest(name=scenario["name"]):
                result, command_output = self.run_cli(scenario["arguments"])
                self.assertEqual(result, 1)
                evidence = read_json(scenario["evidence"])
                self.assertNotIn(str(self.workspace), command_output)
                self.assertNotIn(str(self.workspace), evidence["message"])
                self.assertNotIn("private-folder", command_output)
                self.assertNotIn("private-folder", evidence["message"])
                self.assertIn(scenario["visible_name"], evidence["message"])

    def test_unexpected_header_safely_stops(self) -> None:
        self.assert_safe_stop(
            "header_mismatch",
            self.prepare,
            input_path=FIXTURES / "failures" / "unexpected_header.csv",
            expected_path=None,
        )

    def test_malformed_input_safely_stops(self) -> None:
        self.assert_safe_stop(
            "malformed_input",
            self.prepare,
            input_path=FIXTURES / "failures" / "malformed_input.csv",
            expected_path=None,
        )

    def test_duplicate_retry_is_idempotent(self) -> None:
        run_dir = self.prepare()
        source_hash_before = (run_dir / "source" / "work_items.csv").read_bytes()
        same_run = self.prepare()
        third_run = self.prepare()
        self.assertEqual(run_dir, same_run)
        self.assertEqual(run_dir, third_run)
        self.assertEqual(
            source_hash_before,
            (run_dir / "source" / "work_items.csv").read_bytes(),
        )
        events = [
            json.loads(line)
            for line in (run_dir / "audit" / "events.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        retry_events = [
            event
            for event in events
            if event["event_type"] == "duplicate_retry_ignored"
        ]
        self.assertEqual(len(retry_events), 1)
        self.assertFalse((run_dir / "outbox").exists())
        workspace = self.workspace / "workspace"
        workspace_lock = workspace / workflow_module.OPERATION_LOCK_NAME
        workspace_lock.write_text(
            "held by synthetic concurrency test", encoding="utf-8"
        )
        self.assert_safe_stop(
            "concurrent_operation",
            self.prepare,
        )
        workspace_lock.unlink()
        run_lock = run_dir / workflow_module.OPERATION_LOCK_NAME
        run_lock.write_text("held by synthetic concurrency test", encoding="utf-8")
        audit_before = (run_dir / "audit" / "events.jsonl").read_bytes()
        self.assert_safe_stop(
            "concurrent_operation",
            inspect_run,
            run_dir,
        )
        result, output = self.run_cli(["status", "--run-dir", str(run_dir)])
        self.assertEqual(result, 1)
        self.assertIn("SAFE STOP: concurrent_operation", output)
        self.assertIn("FAILURE_EVIDENCE=unavailable", output)
        self.assertEqual(
            (run_dir / "audit" / "events.jsonl").read_bytes(),
            audit_before,
        )
        run_lock.unlink()

        overlap_workspace = self.workspace / "overlap"
        overlap_run = prepare_run(
            FROZEN_INPUT,
            overlap_workspace,
            "mock",
            SYNTHETIC_CONFIRMATION,
            FROZEN_EXPECTED,
        )
        decision_entered = threading.Event()
        release_decision = threading.Event()
        real_append = workflow_module.append_audit_event

        def hold_decision_audit(*args, **kwargs):
            if len(args) >= 3 and args[2] == "review_decision_recorded":
                decision_entered.set()
                if not release_decision.wait(timeout=10):
                    raise AssertionError("Synthetic overlap release timed out.")
            return real_append(*args, **kwargs)

        thread_errors: list[BaseException] = []

        def decide_in_thread() -> None:
            try:
                self.approve(overlap_run)
            except BaseException as error:
                thread_errors.append(error)

        with patch.object(
            workflow_module,
            "append_audit_event",
            side_effect=hold_decision_audit,
        ):
            decision_thread = threading.Thread(target=decide_in_thread)
            decision_thread.start()
            self.assertTrue(decision_entered.wait(timeout=10))
            self.assert_safe_stop(
                "concurrent_operation",
                prepare_run,
                FROZEN_INPUT,
                overlap_workspace,
                "mock",
                SYNTHETIC_CONFIRMATION,
                FROZEN_EXPECTED,
            )
            release_decision.set()
            decision_thread.join(timeout=10)
        self.assertFalse(decision_thread.is_alive())
        self.assertEqual(thread_errors, [])
        self.assertEqual(
            prepare_run(
                FROZEN_INPUT,
                overlap_workspace,
                "mock",
                SYNTHETIC_CONFIRMATION,
                FROZEN_EXPECTED,
            ),
            overlap_run,
        )
        candidate_path = self.workspace / "overlap-candidate.json"
        write_json(
            candidate_path,
            read_json(overlap_run / "draft" / "summary.json"),
        )
        failure_entered = threading.Event()
        release_failure = threading.Event()
        real_record_failure = cli_module._record_safe_stop_unlocked
        failure_results: list[int] = []
        failure_errors: list[BaseException] = []

        def hold_failure_record(*args, **kwargs):
            failure_entered.set()
            if not release_failure.wait(timeout=10):
                raise AssertionError("Synthetic failure-record release timed out.")
            return real_record_failure(*args, **kwargs)

        def fail_in_thread() -> None:
            try:
                result, _ = self.run_cli(
                    [
                        "validate-summary",
                        "--run-dir",
                        str(overlap_run),
                        "--candidate",
                        str(candidate_path),
                    ]
                )
                failure_results.append(result)
            except BaseException as error:
                failure_errors.append(error)

        with patch.object(
            cli_module,
            "_record_safe_stop_unlocked",
            side_effect=hold_failure_record,
        ):
            failure_thread = threading.Thread(target=fail_in_thread)
            failure_thread.start()
            self.assertTrue(failure_entered.wait(timeout=10))
            self.assert_safe_stop(
                "concurrent_operation",
                inspect_run,
                overlap_run,
            )
            release_failure.set()
            failure_thread.join(timeout=10)
        self.assertFalse(failure_thread.is_alive())
        self.assertEqual(failure_errors, [])
        self.assertEqual(failure_results, [1])
        self.assertEqual(
            inspect_run(overlap_run)["current_state"],
            "approved_for_local_export",
        )
        overlap_events = [
            json.loads(line)
            for line in (overlap_run / "audit" / "events.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        for event_type in (
            "review_decision_recorded",
            "duplicate_retry_ignored",
            "safe_stop_recorded",
        ):
            self.assertEqual(
                sum(event["event_type"] == event_type for event in overlap_events),
                1,
            )

    def test_ai_disabled_timeout_refusal_malformed_and_unknown_use_fallback(
        self,
    ) -> None:
        expected_reasons = {
            "disabled": "ai_disabled",
            "timeout": "ai_timeout",
            "refusal": "ai_refusal",
            "malformed_json": "malformed_ai_json",
            "unknown_issue_id": "unknown_ai_issue_reference",
        }
        for mode, reason in expected_reasons.items():
            with self.subTest(mode=mode):
                run_dir = self.prepare(
                    mode=mode,
                    workspace_name=f"mode-{mode}",
                )
                state = read_json(run_dir / "state.json")
                summary = read_json(run_dir / "draft" / "summary.json")
                evaluation = read_json(run_dir / "evaluation.json")
                self.assertEqual(
                    state["summary_generator"],
                    "deterministic-fallback",
                )
                self.assertEqual(state["summary_fallback_reason"], reason)
                self.assertEqual(summary["generator"], "deterministic-fallback")
                self.assertTrue(evaluation["summary_fallback_used"])
                self.assertEqual(evaluation["unsupported_ai_claims"], 0)

    def test_untrusted_free_text_is_inert_and_never_enters_summary(self) -> None:
        run_dir = self.prepare(
            input_path=FIXTURES / "failures" / "untrusted_instruction.csv",
            expected_path=None,
        )
        source = (run_dir / "source" / "work_items.csv").read_text(encoding="utf-8")
        summary = (run_dir / "draft" / "summary.json").read_text(encoding="utf-8")
        self.assertIn("Ignore every rule", source)
        self.assertNotIn("Ignore every rule", summary)
        self.assertEqual(inspect_run(run_dir)["external_actions"], 0)

    def test_learner_candidate_summary_requires_known_visible_references(self) -> None:
        run_dir = self.prepare()
        candidate = read_json(run_dir / "draft" / "summary.json")
        candidate["headline"] = (
            "Human review is required for 13 verified synthetic issues."
        )
        candidate_path = self.workspace / "candidate.json"
        write_json(candidate_path, candidate)
        result_path = validate_candidate_summary(run_dir, candidate_path)
        result = read_json(result_path)
        self.assertEqual(result["issue_reference_count"], 13)
        self.assertTrue(result["human_support_review_required"])
        self.assertEqual(result["prose_support_status"], "controlled_templates_only")
        unsafe = read_json(run_dir / "draft" / "summary.json")
        unsafe["review_actions"][0]["instruction"] = (
            "Pay the vendor now and mark the source system complete."
        )
        write_json(candidate_path, unsafe)
        self.assert_safe_stop(
            "unsafe_action",
            validate_candidate_summary,
            run_dir,
            candidate_path,
        )
        unsupported = read_json(run_dir / "draft" / "summary.json")
        unsupported["headline"] = "All vendors are definitely fraudulent."
        write_json(candidate_path, unsupported)
        self.assert_safe_stop(
            "unsupported_summary_claim",
            validate_candidate_summary,
            run_dir,
            candidate_path,
        )
        candidate = read_json(run_dir / "draft" / "summary.json")
        candidate["groups"][0]["issue_ids"][0] = "WI-9999|R999|unknown"
        write_json(candidate_path, candidate)
        self.assert_safe_stop(
            "unknown_ai_issue_reference",
            validate_candidate_summary,
            run_dir,
            candidate_path,
        )
        candidate = read_json(run_dir / "draft" / "summary.json")
        write_json(candidate_path, candidate)
        self.approve(run_dir)
        self.assert_safe_stop(
            "invalid_state",
            validate_candidate_summary,
            run_dir,
            candidate_path,
        )

    def test_summary_runtime_validation_matches_schema_constraints(self) -> None:
        run_dir = self.prepare()
        candidate_path = self.workspace / "candidate.json"
        invalid_changes = {
            "wrong_prompt_version": (
                "candidate_run_mismatch",
                lambda value: value.__setitem__("prompt_version", "other-version"),
            ),
            "generator_switch": (
                "candidate_run_mismatch",
                lambda value: value.__setitem__(
                    "generator",
                    "deterministic-fallback",
                ),
            ),
            "invalid_action_id": (
                "summary_contract",
                lambda value: value["review_actions"][0].__setitem__(
                    "action_id",
                    "ACTION-1",
                ),
            ),
            "non_array_action_issue_ids": (
                "summary_contract",
                lambda value: value["review_actions"][0].__setitem__(
                    "issue_ids",
                    7,
                ),
            ),
        }
        for name, (expected_code, change) in invalid_changes.items():
            with self.subTest(name=name):
                candidate = read_json(run_dir / "draft" / "summary.json")
                change(candidate)
                write_json(candidate_path, candidate)
                self.assert_safe_stop(
                    expected_code,
                    validate_candidate_summary,
                    run_dir,
                    candidate_path,
                )

    def test_malformed_candidate_cli_creates_named_failure_evidence(self) -> None:
        run_dir = self.prepare()
        candidate = read_json(run_dir / "draft" / "summary.json")
        candidate["review_actions"][0]["issue_ids"] = 7
        candidate_path = self.workspace / "malformed-candidate.json"
        write_json(candidate_path, candidate)
        result, command_output = self.run_cli(
            [
                "validate-summary",
                "--run-dir",
                str(run_dir),
                "--candidate",
                str(candidate_path),
            ]
        )
        self.assertEqual(result, 1)
        self.assertIn("SAFE STOP: summary_contract", command_output)
        self.assertIn(
            "FAILURE_EVIDENCE=failures/latest.json",
            command_output,
        )
        evidence = read_json(run_dir / "failures" / "latest.json")
        self.assertEqual(evidence["state"], "failed_manual")
        self.assertEqual(evidence["external_actions"], 0)
        status = inspect_run(run_dir)
        self.assertEqual(status["current_state"], "needs_review")
        self.assertEqual(status["latest_attempt_state"], "failed_manual")
        self.assertEqual(status["latest_event_type"], "safe_stop_recorded")

    def test_approve_then_local_json_and_csv_export(self) -> None:
        original_source = FROZEN_INPUT.read_bytes()
        run_dir = self.prepare()
        self.approve(run_dir)
        json_path, csv_path = export_approved(run_dir, CHECKED)
        self.assertTrue(json_path.exists())
        self.assertTrue(csv_path.exists())
        payload = read_json(json_path)
        self.assertEqual(payload["dataset_kind"], "synthetic")
        self.assertEqual(payload["output_kind"], "local_draft_only")
        self.assertEqual(payload["external_actions"], 0)
        self.assertEqual(len(payload["records"]), 13)
        csv_rows = list(
            csv.DictReader(csv_path.read_text(encoding="utf-8").splitlines())
        )
        self.assertEqual(len(csv_rows), 13)
        self.assertEqual(FROZEN_INPUT.read_bytes(), original_source)
        status = inspect_run(run_dir)
        self.assertEqual(status["current_state"], "approved_draft")
        self.assertEqual(status["local_export_count"], 2)
        self.assertEqual(status["external_actions"], 0)
        original_json = json_path.read_bytes()
        json_path.write_bytes(original_json + b"\n")
        self.assert_safe_stop(
            "export_integrity_mismatch",
            inspect_run,
            run_dir,
        )
        json_path.write_bytes(original_json)
        json_path.unlink()
        csv_path.unlink()
        self.assert_safe_stop(
            "missing_approved_export",
            inspect_run,
            run_dir,
        )

    def test_export_retry_creates_no_duplicate_logical_effect(self) -> None:
        run_dir = self.prepare()
        self.approve(run_dir)
        first_paths = export_approved(run_dir, CHECKED)
        first_bytes = [path.read_bytes() for path in first_paths]
        second_paths = export_approved(run_dir, CHECKED)
        self.assertEqual(first_paths, second_paths)
        self.assertEqual(first_bytes, [path.read_bytes() for path in second_paths])
        events = [
            json.loads(line)
            for line in (run_dir / "audit" / "events.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        export_events = [
            event for event in events if event["event_type"] == "local_export_created"
        ]
        self.assertEqual(len(export_events), 1)

    def test_export_retry_rejects_missing_export_audit_event(self) -> None:
        run_dir = self.prepare()
        self.approve(run_dir)
        first_paths = export_approved(run_dir, CHECKED)
        audit_path = run_dir / "audit" / "events.jsonl"
        events = [
            json.loads(line)
            for line in audit_path.read_text(encoding="utf-8").splitlines()
        ]
        retained = [
            event for event in events if event["event_type"] != "local_export_created"
        ]
        audit_path.write_text(
            "".join(
                json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n"
                for event in retained
            ),
            encoding="utf-8",
        )

        self.assert_safe_stop(
            "export_audit_mismatch",
            export_approved,
            run_dir,
            CHECKED,
        )
        self.assertTrue(all(path.exists() for path in first_paths))
        self.assertEqual(
            audit_path.read_text(encoding="utf-8").count("local_export_created"), 0
        )

    def test_post_promotion_persistence_failures_roll_back_and_retry_cleanly(
        self,
    ) -> None:
        for failure_stage in ("state", "audit", "evaluation"):
            with self.subTest(failure_stage=failure_stage):
                run_dir = self.prepare(
                    workspace_name=f"finalize-{failure_stage}",
                )
                self.approve(run_dir)
                state_path = run_dir / "state.json"
                evaluation_path = run_dir / "evaluation.json"
                original_state = state_path.read_bytes()
                original_evaluation = evaluation_path.read_bytes()
                injected = {"fired": False}

                if failure_stage == "state":
                    real_write_json = workflow_module.write_json

                    def fail_once(path, value):
                        if (
                            not injected["fired"]
                            and Path(path).name == "state.json"
                            and isinstance(value, dict)
                            and value.get("current_state") == "approved_draft"
                        ):
                            injected["fired"] = True
                            raise SafeStop(
                                "injected_state_failure",
                                "Injected state persistence failure.",
                            )
                        return real_write_json(path, value)

                    persistence_patch = patch.object(
                        workflow_module,
                        "write_json",
                        side_effect=fail_once,
                    )
                elif failure_stage == "audit":
                    real_append_audit = workflow_module.append_audit_event

                    def fail_once(*args, **kwargs):
                        if (
                            not injected["fired"]
                            and len(args) >= 3
                            and args[2] == "local_export_created"
                        ):
                            injected["fired"] = True
                            raise SafeStop(
                                "injected_audit_failure",
                                "Injected audit persistence failure.",
                            )
                        return real_append_audit(*args, **kwargs)

                    persistence_patch = patch.object(
                        workflow_module,
                        "append_audit_event",
                        side_effect=fail_once,
                    )
                else:
                    real_refresh = workflow_module._refresh_evaluation

                    def fail_once(run, state, current_state):
                        if not injected["fired"] and current_state == "approved_draft":
                            injected["fired"] = True
                            raise SafeStop(
                                "injected_evaluation_failure",
                                "Injected evaluation persistence failure.",
                            )
                        return real_refresh(run, state, current_state)

                    persistence_patch = patch.object(
                        workflow_module,
                        "_refresh_evaluation",
                        side_effect=fail_once,
                    )

                with persistence_patch:
                    result, command_output = self.run_cli(
                        [
                            "export",
                            "--run-dir",
                            str(run_dir),
                            "--checked-at",
                            "2026-07-28T11:00:00Z",
                        ]
                    )

                self.assertTrue(injected["fired"])
                self.assertEqual(result, 1)
                self.assertIn("SAFE STOP: export_finalize_error", command_output)
                self.assertEqual(state_path.read_bytes(), original_state)
                self.assertEqual(
                    evaluation_path.read_bytes(),
                    original_evaluation,
                )
                self.assertFalse((run_dir / "outbox" / "approved-r1.json").exists())
                self.assertFalse((run_dir / "outbox" / "approved-r1.csv").exists())
                self.assertFalse((run_dir / "outbox" / "INCOMPLETE.txt").exists())
                failed_events = [
                    json.loads(line)
                    for line in (run_dir / "audit" / "events.jsonl")
                    .read_text(encoding="utf-8")
                    .splitlines()
                ]
                self.assertFalse(
                    any(
                        event["event_type"] == "local_export_created"
                        for event in failed_events
                    )
                )
                failure_evidence = read_json(run_dir / "failures" / "latest.json")
                self.assertEqual(
                    failure_evidence["error_code"],
                    "export_finalize_error",
                )

                export_paths = export_approved(run_dir, CHECKED)
                self.assertTrue(all(path.exists() for path in export_paths))
                self.assertEqual(
                    read_json(state_path)["current_state"],
                    "approved_draft",
                )
                self.assertEqual(
                    read_json(evaluation_path)["current_state"],
                    "approved_draft",
                )
                retry_events = [
                    json.loads(line)
                    for line in (run_dir / "audit" / "events.jsonl")
                    .read_text(encoding="utf-8")
                    .splitlines()
                ]
                self.assertEqual(
                    len(
                        [
                            event
                            for event in retry_events
                            if event["event_type"] == "local_export_created"
                        ]
                    ),
                    1,
                )

        def exercise_atomic_prepare(
            *,
            label: str,
            input_path: Path,
            expected_path: Path | None,
            base_event_types: tuple[str, ...],
        ) -> None:
            real_atomic = workflow_module.atomic_write_bytes
            observed_writes: list[str] = []

            def observe_write(path, value):
                observed_writes.append(Path(path).name)
                return real_atomic(path, value)

            baseline_workspace = self.workspace / f"prepare-baseline-{label}"
            with patch.object(
                workflow_module,
                "atomic_write_bytes",
                side_effect=observe_write,
            ):
                prepare_run(
                    input_path,
                    baseline_workspace,
                    "mock",
                    SYNTHETIC_CONFIRMATION,
                    expected_path,
                )
            self.assertGreater(len(observed_writes), 5)

            for failure_index in range(1, len(observed_writes) + 1):
                with self.subTest(
                    prepare_kind=label,
                    failure_write=failure_index,
                ):
                    workspace = (
                        self.workspace / f"prepare-{label}-write-{failure_index:02d}"
                    )
                    counter = {"value": 0}

                    def fail_selected_write(path, value):
                        counter["value"] += 1
                        if counter["value"] == failure_index:
                            raise SafeStop(
                                "injected_prepare_write_failure",
                                "Synthetic prepare finalization failure.",
                            )
                        return real_atomic(path, value)

                    with patch.object(
                        workflow_module,
                        "atomic_write_bytes",
                        side_effect=fail_selected_write,
                    ):
                        with self.assertRaises(SafeStop):
                            prepare_run(
                                input_path,
                                workspace,
                                "mock",
                                SYNTHETIC_CONFIRMATION,
                                expected_path,
                            )
                    runs_root = workspace / "runs"
                    if runs_root.exists():
                        self.assertFalse(
                            any(
                                path.name.startswith(workflow_module.STAGING_PREFIX)
                                for path in runs_root.iterdir()
                            )
                        )
                    latest = workspace / "latest_run.txt"
                    published_before_retry = (
                        [
                            path
                            for path in runs_root.iterdir()
                            if path.is_dir() and path.name.startswith("RUN-")
                        ]
                        if runs_root.exists()
                        else []
                    )
                    if latest.exists():
                        self.assertEqual(len(published_before_retry), 1)

                    run_dir = prepare_run(
                        input_path,
                        workspace,
                        "mock",
                        SYNTHETIC_CONFIRMATION,
                        expected_path,
                    )
                    self.assertEqual(inspect_run(run_dir)["run_id"], run_dir.name)
                    self.assertEqual(
                        latest.read_text(encoding="utf-8").strip(),
                        f"runs/{run_dir.name}",
                    )
                    events = [
                        json.loads(line)
                        for line in (run_dir / "audit" / "events.jsonl")
                        .read_text(encoding="utf-8")
                        .splitlines()
                    ]
                    for event_type in base_event_types:
                        self.assertEqual(
                            sum(event["event_type"] == event_type for event in events),
                            1,
                        )
                    self.assertLessEqual(
                        sum(
                            event["event_type"] == "duplicate_retry_ignored"
                            for event in events
                        ),
                        1,
                    )

            publish_workspace = self.workspace / f"prepare-{label}-publish"
            real_replace = workflow_module.os.replace

            def fail_run_publish(source, destination):
                if Path(source).is_dir() and Path(destination).name.startswith("RUN-"):
                    raise OSError("Synthetic directory publication failure.")
                return real_replace(source, destination)

            with patch.object(
                workflow_module.os,
                "replace",
                side_effect=fail_run_publish,
            ):
                self.assert_safe_stop(
                    "run_publish_error",
                    prepare_run,
                    input_path,
                    publish_workspace,
                    "mock",
                    SYNTHETIC_CONFIRMATION,
                    expected_path,
                )
            self.assertFalse((publish_workspace / "latest_run.txt").exists())
            if (publish_workspace / "runs").exists():
                self.assertEqual(
                    list((publish_workspace / "runs").iterdir()),
                    [],
                )
            published_retry = prepare_run(
                input_path,
                publish_workspace,
                "mock",
                SYNTHETIC_CONFIRMATION,
                expected_path,
            )
            self.assertEqual(
                inspect_run(published_retry)["run_id"],
                published_retry.name,
            )

        exercise_atomic_prepare(
            label="issues",
            input_path=FROZEN_INPUT,
            expected_path=FROZEN_EXPECTED,
            base_event_types=(
                "run_received",
                "input_validated",
                "issues_created",
                "mock_summary_validated",
                "human_review_required",
            ),
        )
        exercise_atomic_prepare(
            label="no-action",
            input_path=FIXTURES / "failures" / "valid_no_issue.csv",
            expected_path=None,
            base_event_types=(
                "run_received",
                "input_validated",
                "no_verified_issues",
            ),
        )

    def test_failed_export_rollback_leaves_a_blocking_incomplete_marker(
        self,
    ) -> None:
        run_dir = self.prepare(workspace_name="rollback-marker")
        self.approve(run_dir)
        real_restore = workflow_module._restore_controlled_file
        real_refresh = workflow_module._refresh_evaluation

        def fail_evaluation(run, state, current_state):
            if current_state == "approved_draft":
                raise SafeStop(
                    "injected_evaluation_failure",
                    "Injected evaluation persistence failure.",
                )
            return real_refresh(
                run,
                state,
                current_state,
            )

        def fail_state_restore(path, snapshot):
            if Path(path).name == "state.json":
                raise SafeStop(
                    "injected_restore_failure",
                    "Injected state rollback failure.",
                )
            return real_restore(path, snapshot)

        with (
            patch.object(
                workflow_module,
                "_refresh_evaluation",
                side_effect=fail_evaluation,
            ),
            patch.object(
                workflow_module,
                "_restore_controlled_file",
                side_effect=fail_state_restore,
            ),
        ):
            self.assert_safe_stop(
                "export_rollback_failed",
                export_approved,
                run_dir,
                CHECKED,
            )

        marker = run_dir / "outbox" / "INCOMPLETE.txt"
        self.assertTrue(marker.is_file())
        self.assertIn(
            "Do not use files",
            marker.read_text(encoding="utf-8"),
        )
        self.assertFalse((run_dir / "outbox" / "approved-r1.json").exists())
        self.assertFalse((run_dir / "outbox" / "approved-r1.csv").exists())
        self.assert_safe_stop(
            "incomplete_export_transaction",
            inspect_run,
            run_dir,
        )

    def test_edited_draft_after_approval_safely_stops(self) -> None:
        run_dir = self.prepare()
        self.approve(run_dir)
        draft_path = run_dir / "draft" / "summary.json"
        draft_path.write_bytes(draft_path.read_bytes() + b" ")
        self.assert_safe_stop(
            "edited_draft_after_approval",
            export_approved,
            run_dir,
            CHECKED,
        )
        self.assertFalse((run_dir / "outbox").exists())

    def test_expired_approval_safely_stops_and_records_expiry(self) -> None:
        run_dir = self.prepare()
        record_decision(
            run_dir,
            "approve",
            "course_learner",
            "Reviewed every source link.",
            1,
            True,
            CHECKED,
            DECIDED,
        )
        self.assert_safe_stop(
            "expired_review",
            export_approved,
            run_dir,
            CHECKED,
        )
        self.assertEqual(read_json(run_dir / "state.json")["current_state"], "expired")
        self.assertFalse((run_dir / "outbox").exists())

    def test_reject_edit_and_expire_are_real_non_export_decisions(self) -> None:
        expected_states = {
            "reject": "rejected",
            "edit": "changes_requested",
            "expire": "expired",
        }
        for decision, state in expected_states.items():
            with self.subTest(decision=decision):
                run_dir = self.prepare(workspace_name=f"decision-{decision}")
                record_decision(
                    run_dir,
                    decision,
                    "course_learner",
                    f"Synthetic {decision} decision.",
                    1,
                    True,
                    FUTURE,
                    DECIDED,
                )
                self.assertEqual(
                    read_json(run_dir / "state.json")["current_state"],
                    state,
                )
                self.assert_safe_stop(
                    "decision_not_approved",
                    export_approved,
                    run_dir,
                    CHECKED,
                )
                self.assertFalse((run_dir / "outbox").exists())

    def test_edit_creates_new_revision_that_needs_new_review(self) -> None:
        run_dir = self.prepare()
        record_decision(
            run_dir,
            "edit",
            "course_learner",
            "Make the headline clearer.",
            1,
            True,
            FUTURE,
            DECIDED,
        )
        replacement = read_json(run_dir / "draft" / "summary.json")
        replacement["headline"] = (
            "Human review is required for 13 verified synthetic issues."
        )
        replacement_path = self.workspace / "replacement.json"
        write_json(replacement_path, replacement)
        revision = revise_draft(run_dir, replacement_path, 1)
        self.assertEqual(revision, 2)
        state = read_json(run_dir / "state.json")
        self.assertEqual(state["current_state"], "needs_review")
        self.assertIsNone(state["active_decision_path"])
        self.assert_safe_stop(
            "review_required",
            export_approved,
            run_dir,
            CHECKED,
        )
        self.approve(run_dir, revision=2)
        export_approved(run_dir, CHECKED)
        self.assertTrue((run_dir / "outbox" / "approved-r2.json").exists())

        decision_run = self.prepare(workspace_name="decision-transaction")
        decision_paths = [
            decision_run / "state.json",
            decision_run / "evaluation.json",
            decision_run / "audit" / "events.jsonl",
        ]
        decision_before = {path: path.read_bytes() for path in decision_paths}
        with patch.object(
            workflow_module,
            "_refresh_evaluation",
            side_effect=SafeStop(
                "injected_evaluation_failure",
                "Synthetic decision finalization failure.",
            ),
        ):
            self.assert_safe_stop(
                "injected_evaluation_failure",
                record_decision,
                decision_run,
                "approve",
                "course_learner",
                "Reviewed.",
                1,
                True,
                FUTURE,
                DECIDED,
            )
        self.assertFalse((decision_run / "review" / "decision-r1.json").exists())
        self.assertEqual(
            {path: path.read_bytes() for path in decision_paths},
            decision_before,
        )
        self.approve(decision_run)

        revision_run = self.prepare(workspace_name="revision-transaction")
        record_decision(
            revision_run,
            "edit",
            "course_learner",
            "Use the alternate controlled headline.",
            1,
            True,
            FUTURE,
            DECIDED,
        )
        bounded_replacement = read_json(revision_run / "draft" / "summary.json")
        bounded_replacement["headline"] = (
            "Human review is required for 13 verified synthetic issues."
        )
        bounded_path = self.workspace / "bounded-replacement.json"
        write_json(bounded_path, bounded_replacement)
        for field, wrong_value in (
            ("prompt_version", "other-prompt"),
            ("generator", "deterministic-fallback"),
        ):
            with self.subTest(replacement_field=field):
                mismatched = dict(bounded_replacement)
                mismatched[field] = wrong_value
                write_json(bounded_path, mismatched)
                self.assert_safe_stop(
                    "replacement_run_mismatch",
                    revise_draft,
                    revision_run,
                    bounded_path,
                    1,
                )
        write_json(bounded_path, bounded_replacement)
        revision_paths = [
            revision_run / "draft" / "summary.json",
            revision_run / "review" / "review_package.json",
            revision_run / "review" / "review_manifest.json",
            revision_run / "state.json",
            revision_run / "evaluation.json",
            revision_run / "audit" / "events.jsonl",
        ]
        revision_before = {path: path.read_bytes() for path in revision_paths}
        real_append = workflow_module.append_audit_event

        def fail_revision_audit(*args, **kwargs):
            if len(args) >= 3 and args[2] == "draft_revision_created":
                raise SafeStop(
                    "injected_audit_failure",
                    "Synthetic revision audit failure.",
                )
            return real_append(*args, **kwargs)

        with patch.object(
            workflow_module,
            "append_audit_event",
            side_effect=fail_revision_audit,
        ):
            self.assert_safe_stop(
                "injected_audit_failure",
                revise_draft,
                revision_run,
                bounded_path,
                1,
            )
        self.assertEqual(
            {path: path.read_bytes() for path in revision_paths},
            revision_before,
        )
        self.assertFalse(
            (revision_run / workflow_module.TRANSACTION_INCOMPLETE_NAME).exists()
        )
        self.assertEqual(revise_draft(revision_run, bounded_path, 1), 2)

    def test_external_actions_must_remain_false(self) -> None:
        run_dir = self.prepare()
        self.approve(run_dir)
        control = read_json(run_dir / "control.json")
        self.assertIs(control["EXTERNAL_ACTIONS_ENABLED"], False)
        control["EXTERNAL_ACTIONS_ENABLED"] = True
        write_json(run_dir / "control.json", control)
        self.assert_safe_stop(
            "external_action_blocked",
            export_approved,
            run_dir,
            CHECKED,
        )
        self.assertFalse((run_dir / "outbox").exists())

    def test_forged_evidence_review_false_cannot_export(self) -> None:
        run_dir = self.prepare()
        decision_path = self.approve(run_dir)
        decision = read_json(decision_path)
        decision["evidence_reviewed"] = False
        write_json(decision_path, decision)
        self.assert_safe_stop(
            "review_evidence_required",
            export_approved,
            run_dir,
            CHECKED,
        )

    def test_schema_invalid_approval_record_cannot_export(self) -> None:
        changes = {
            "invalid_decision_id": lambda value: value.__setitem__(
                "decision_id",
                "FORGED",
            ),
            "blank_reviewer_role": lambda value: value.__setitem__(
                "reviewer_role",
                "",
            ),
            "blank_reason": lambda value: value.__setitem__("reason", ""),
            "invalid_decided_at": lambda value: value.__setitem__(
                "decided_at",
                "not-a-date",
            ),
        }
        for name, change in changes.items():
            with self.subTest(name=name):
                run_dir = self.prepare(workspace_name=f"approval-{name}")
                decision_path = self.approve(run_dir)
                decision = read_json(decision_path)
                change(decision)
                write_json(decision_path, decision)
                self.assert_safe_stop(
                    "approval_contract",
                    export_approved,
                    run_dir,
                    CHECKED,
                )
                self.assertFalse((run_dir / "outbox").exists())

    def test_schema_invalid_approval_cli_creates_named_failure_evidence(self) -> None:
        run_dir = self.prepare(workspace_name="approval-cli")
        decision_path = self.approve(run_dir)
        decision = read_json(decision_path)
        decision["reason"] = ""
        write_json(decision_path, decision)
        result, command_output = self.run_cli(
            [
                "export",
                "--run-dir",
                str(run_dir),
                "--checked-at",
                "2026-07-28T11:00:00Z",
            ]
        )
        self.assertEqual(result, 1)
        self.assertIn("SAFE STOP: approval_contract", command_output)
        self.assertIn(
            "FAILURE_EVIDENCE=failures/latest.json",
            command_output,
        )
        evidence = read_json(run_dir / "failures" / "latest.json")
        self.assertEqual(evidence["state"], "failed_manual")
        self.assertEqual(evidence["external_actions"], 0)
        self.assertFalse((run_dir / "outbox").exists())

    def test_cli_outputs_only_neutral_artifact_locators(self) -> None:
        workspace = self.workspace / "neutral-cli"
        prepare_result, prepare_output = self.run_cli(
            [
                "prepare",
                "--input",
                str(FROZEN_INPUT),
                "--expected",
                str(FROZEN_EXPECTED),
                "--workspace",
                str(workspace),
                "--ai-mode",
                "mock",
                "--synthetic-confirmation",
                SYNTHETIC_CONFIRMATION,
            ]
        )
        self.assertEqual(prepare_result, 0)
        run_locator = (workspace / "latest_run.txt").read_text(encoding="utf-8").strip()
        run_dir = (workspace / Path(run_locator)).resolve()
        self.assertIn(f"RUN_ID={run_dir.name}", prepare_output)
        self.assertIn(f"RUN_LOCATOR={run_locator}", prepare_output)

        candidate = read_json(run_dir / "draft" / "summary.json")
        candidate["headline"] = (
            "Human review is required for 13 verified synthetic issues."
        )
        candidate_path = self.workspace / "neutral-candidate.json"
        write_json(candidate_path, candidate)
        validate_result, validate_output = self.run_cli(
            [
                "validate-summary",
                "--run-dir",
                str(run_dir),
                "--candidate",
                str(candidate_path),
            ]
        )
        self.assertEqual(validate_result, 0)
        self.assertIn("RESULT=review/candidate-validation.json", validate_output)

        decide_result, decide_output = self.run_cli(
            [
                "decide",
                "--run-dir",
                str(run_dir),
                "--decision",
                "approve",
                "--reviewer-role",
                "course_learner",
                "--reason",
                "Every synthetic source link was reviewed.",
                "--expected-revision",
                "1",
                "--evidence-reviewed",
                "--decided-at",
                "2026-07-28T10:00:00Z",
                "--expires-at",
                "2099-01-01T00:00:00Z",
            ]
        )
        self.assertEqual(decide_result, 0)
        self.assertIn("DECISION=review/decision-r1.json", decide_output)

        export_result, export_output = self.run_cli(
            [
                "export",
                "--run-dir",
                str(run_dir),
                "--checked-at",
                "2026-07-28T11:00:00Z",
            ]
        )
        self.assertEqual(export_result, 0)
        self.assertIn("JSON=outbox/approved-r1.json", export_output)
        self.assertIn("CSV=outbox/approved-r1.csv", export_output)

        combined_output = (
            prepare_output + validate_output + decide_output + export_output
        )
        self.assertNotIn(str(self.workspace), combined_output)

    def test_manual_fallback_and_evaluation_are_usable(self) -> None:
        run_dir = self.prepare(mode="timeout")
        fallback = (run_dir / "manual_fallback.md").read_text(encoding="utf-8")
        self.assertIn("Owner:", fallback)
        self.assertIn("issues/issues.csv", fallback)
        self.assertIn("External action: none", fallback)
        evaluation = read_json(run_dir / "evaluation.json")
        self.assertEqual(evaluation["true_positives"], 13)
        self.assertEqual(evaluation["false_positives"], 0)
        self.assertEqual(evaluation["false_negatives"], 0)
        self.assertEqual(evaluation["course1_recommendation"], "REWORK")
        self.assertIn("Modules 1-3 and 7-9", evaluation["recommendation_reason"])

    def test_every_audit_event_has_the_canonical_contract(self) -> None:
        run_dir = self.prepare(mode="refusal")
        self.approve(run_dir)
        export_approved(run_dir, CHECKED)
        events = [
            json.loads(line)
            for line in (run_dir / "audit" / "events.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        required = {
            "event_id",
            "run_id",
            "event_type",
            "state",
            "occurred_at",
            "actor_type",
            "details",
        }
        self.assertGreaterEqual(len(events), 7)
        self.assertEqual(len(events), len({event["event_id"] for event in events}))
        for event in events:
            self.assertEqual(set(event), required)
            self.assertEqual(event["run_id"], inspect_run(run_dir)["run_id"])

    def test_synthetic_confirmation_is_mandatory(self) -> None:
        self.assert_safe_stop(
            "synthetic_confirmation_required",
            prepare_run,
            FROZEN_INPUT,
            self.workspace,
            "mock",
            "yes",
            FROZEN_EXPECTED,
        )

    def test_run_identity_includes_mode_and_expected_oracle_hash(self) -> None:
        workspace = self.workspace / "run-identity"
        mock_run = prepare_run(
            FROZEN_INPUT,
            workspace,
            "mock",
            SYNTHETIC_CONFIRMATION,
            FROZEN_EXPECTED,
        )
        timeout_run = prepare_run(
            FROZEN_INPUT,
            workspace,
            "timeout",
            SYNTHETIC_CONFIRMATION,
            FROZEN_EXPECTED,
        )
        no_oracle_run = prepare_run(
            FROZEN_INPUT,
            workspace,
            "mock",
            SYNTHETIC_CONFIRMATION,
            None,
        )
        changed_oracle = self.workspace / "changed-expected.csv"
        changed_oracle.write_bytes(FROZEN_EXPECTED.read_bytes() + b"\n")
        changed_oracle_run = prepare_run(
            FROZEN_INPUT,
            workspace,
            "mock",
            SYNTHETIC_CONFIRMATION,
            changed_oracle,
        )
        self.assertEqual(
            len(
                {
                    mock_run.name,
                    timeout_run.name,
                    no_oracle_run.name,
                    changed_oracle_run.name,
                }
            ),
            4,
        )
        self.assertEqual(
            read_json(mock_run / "run_config.json")["requested_adapter_mode"],
            "mock",
        )
        self.assertEqual(
            read_json(timeout_run / "run_config.json")["requested_adapter_mode"],
            "timeout",
        )

    def test_review_manifest_binds_every_protected_artifact(self) -> None:
        run_dir = self.prepare()
        manifest = read_json(run_dir / "review" / "review_manifest.json")
        self.assertEqual(
            set(manifest["artifact_sha256"]),
            {
                "source/work_items.csv",
                "source/expected_issues.evidence",
                "issues/issues.json",
                "issues/issues.csv",
                "draft/summary.json",
                "control.json",
                "run_config.json",
                "review/review_package.json",
            },
        )
        state = read_json(run_dir / "state.json")
        self.assertEqual(
            state["review_manifest_sha256"],
            hashlib.sha256(
                json.dumps(
                    manifest,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
                + b"\n"
            ).hexdigest(),
        )
        decision = read_json(self.approve(run_dir))
        self.assertEqual(
            decision["review_manifest_sha256"],
            state["review_manifest_sha256"],
        )

    def test_schema_valid_issue_message_tamper_after_approval_blocks_export(
        self,
    ) -> None:
        run_dir = self.prepare()
        self.approve(run_dir)
        issues_path = run_dir / "issues" / "issues.json"
        issues = read_json(issues_path)
        issues[0]["message"] = "A different but schema-valid issue message."
        write_json(issues_path, issues)
        self.assert_safe_stop(
            "issues_integrity_mismatch",
            export_approved,
            run_dir,
            CHECKED,
        )
        self.assertFalse((run_dir / "outbox" / "approved-r1.json").exists())

    def test_other_protected_artifact_tampering_blocks_export(self) -> None:
        changes = {
            "source": (
                "source_integrity_mismatch",
                lambda run_dir: (run_dir / "source" / "work_items.csv").write_bytes(
                    (run_dir / "source" / "work_items.csv").read_bytes() + b"\n"
                ),
            ),
            "expected_oracle_evidence": (
                "expected_oracle_integrity_mismatch",
                lambda run_dir: (
                    run_dir / workflow_module.EXPECTED_ORACLE_EVIDENCE_PATH
                ).write_bytes(
                    (
                        run_dir / workflow_module.EXPECTED_ORACLE_EVIDENCE_PATH
                    ).read_bytes()
                    + b"\n"
                ),
            ),
            "coordinated_state_evaluation_oracle_tamper": (
                "expected_oracle_integrity_mismatch",
                self._tamper_state_and_evaluation_expected_keys,
            ),
            "issues_csv": (
                "issues_integrity_mismatch",
                lambda run_dir: (run_dir / "issues" / "issues.csv").write_bytes(
                    (run_dir / "issues" / "issues.csv").read_bytes() + b"\n"
                ),
            ),
            "review_package": (
                "review_manifest_mismatch",
                lambda run_dir: self._change_json(
                    run_dir / "review" / "review_package.json",
                    lambda value: value["reviewer_must_check"].__setitem__(
                        0,
                        "A different but structurally valid review instruction.",
                    ),
                ),
            ),
            "review_package_boolean_revision": (
                "review_package_contract",
                lambda run_dir: self._change_json(
                    run_dir / "review" / "review_package.json",
                    lambda value: value.__setitem__("draft_revision", True),
                ),
            ),
            "control_boolean_numeric_confusion": (
                "external_action_blocked",
                lambda run_dir: self._change_json(
                    run_dir / "control.json",
                    lambda value: value.__setitem__(
                        "EXTERNAL_ACTIONS_ENABLED",
                        0,
                    ),
                ),
            ),
            "run_config": (
                "run_config_integrity_mismatch",
                lambda run_dir: self._change_json(
                    run_dir / "run_config.json",
                    lambda value: value.__setitem__(
                        "fallback_generator_version",
                        "different-fallback-v1",
                    ),
                ),
            ),
            "stored_manifest": (
                "review_manifest_mismatch",
                lambda run_dir: self._change_json(
                    run_dir / "review" / "review_manifest.json",
                    lambda value: value["artifact_sha256"].__setitem__(
                        "control.json",
                        "0" * 64,
                    ),
                ),
            ),
            "manifest_boolean_revision": (
                "review_manifest_contract",
                lambda run_dir: self._change_json(
                    run_dir / "review" / "review_manifest.json",
                    lambda value: value.__setitem__("draft_revision", True),
                ),
            ),
            "evaluation_recommendation_reason": (
                "evaluation_integrity_mismatch",
                lambda run_dir: self._change_json(
                    run_dir / "evaluation.json",
                    lambda value: value.__setitem__(
                        "recommendation_reason",
                        "Different but schema-valid prose.",
                    ),
                ),
            ),
        }
        for name, (expected_code, change) in changes.items():
            with self.subTest(name=name):
                run_dir = self.prepare(workspace_name=f"protected-{name}")
                self.approve(run_dir)
                change(run_dir)
                self.assert_safe_stop(
                    expected_code,
                    export_approved,
                    run_dir,
                    CHECKED,
                )
                self.assertFalse((run_dir / "outbox" / "approved-r1.json").exists())

    @staticmethod
    def _change_json(path: Path, change) -> None:
        value = read_json(path)
        change(value)
        write_json(path, value)

    @staticmethod
    def _tamper_state_and_evaluation_expected_keys(run_dir: Path) -> None:
        state_path = run_dir / "state.json"
        state = read_json(state_path)
        state["expected_keys"] = None
        write_json(state_path, state)
        issues = read_json(run_dir / "issues" / "issues.json")
        write_json(
            run_dir / "evaluation.json",
            workflow_module._evaluation(
                state["run_id"],
                issues,
                None,
                state["summary_fallback_reason"],
                state["current_state"],
            ),
        )

    def test_audit_event_field_tamper_is_detected_by_event_id(self) -> None:
        run_dir = self.prepare()
        state_before = (run_dir / "state.json").read_bytes()
        audit_path = run_dir / "audit" / "events.jsonl"
        events = [
            json.loads(line)
            for line in audit_path.read_text(encoding="utf-8").splitlines()
        ]
        events[0]["details"]["dataset_kind"] = "changed"
        audit_path.write_text(
            "".join(
                json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n"
                for event in events
            ),
            encoding="utf-8",
        )
        self.assert_safe_stop(
            "audit_integrity_mismatch",
            inspect_run,
            run_dir,
        )
        self.assert_safe_stop(
            "audit_integrity_mismatch",
            record_decision,
            run_dir,
            "approve",
            "course_learner",
            "Reviewed.",
            1,
            True,
            FUTURE,
            DECIDED,
        )
        self.assertEqual((run_dir / "state.json").read_bytes(), state_before)
        self.assertFalse((run_dir / "review" / "decision-r1.json").exists())

        missing_run = self.prepare(workspace_name="audit-missing-decision")
        self.approve(missing_run)
        missing_audit = missing_run / "audit" / "events.jsonl"
        missing_events = [
            json.loads(line)
            for line in missing_audit.read_text(encoding="utf-8").splitlines()
        ]
        missing_events = [
            event
            for event in missing_events
            if event["event_type"] != "review_decision_recorded"
        ]
        missing_audit.write_text(
            "".join(
                json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n"
                for event in missing_events
            ),
            encoding="utf-8",
        )
        self.assert_safe_stop(
            "audit_history_mismatch",
            inspect_run,
            missing_run,
        )
        self.assert_safe_stop(
            "audit_history_mismatch",
            export_approved,
            missing_run,
            CHECKED,
        )
        self.assertFalse((missing_run / "outbox").exists())

        duplicate_run = self.prepare(workspace_name="audit-duplicate-decision")
        self.approve(duplicate_run)
        duplicate_events = [
            json.loads(line)
            for line in (duplicate_run / "audit" / "events.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        decision_event = next(
            event
            for event in duplicate_events
            if event["event_type"] == "review_decision_recorded"
        )
        workflow_module.append_audit_event(
            duplicate_run,
            decision_event["run_id"],
            decision_event["event_type"],
            decision_event["state"],
            decision_event["actor_type"],
            decision_event["details"],
            CHECKED,
        )
        self.assert_safe_stop(
            "audit_history_mismatch",
            inspect_run,
            duplicate_run,
        )

        order_run = self.prepare(workspace_name="audit-impossible-order")
        self.approve(order_run)
        order_path = order_run / "audit" / "events.jsonl"
        order_events = [
            json.loads(line)
            for line in order_path.read_text(encoding="utf-8").splitlines()
        ]
        decision_index = next(
            index
            for index, event in enumerate(order_events)
            if event["event_type"] == "review_decision_recorded"
        )
        decision_first = order_events.pop(decision_index)
        order_events.insert(0, decision_first)
        order_path.write_text(
            "".join(
                json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n"
                for event in order_events
            ),
            encoding="utf-8",
        )
        self.assert_safe_stop(
            "audit_history_mismatch",
            inspect_run,
            order_run,
        )

    def test_prior_expiry_cannot_be_extended_by_editing_decision(self) -> None:
        run_dir = self.prepare()
        original_expiry = datetime(2026, 7, 28, 10, 30, tzinfo=timezone.utc)
        decision_path = record_decision(
            run_dir,
            "approve",
            "course_learner",
            "Every synthetic source link was reviewed.",
            1,
            True,
            original_expiry,
            DECIDED,
        )
        decision = read_json(decision_path)
        decision["expires_at"] = "2099-01-01T00:00:00Z"
        write_json(decision_path, decision)
        self.assert_safe_stop(
            "decision_integrity_mismatch",
            export_approved,
            run_dir,
            CHECKED,
        )
        self.assertFalse((run_dir / "outbox" / "approved-r1.json").exists())

    def test_every_material_decision_field_is_locally_fingerprinted(self) -> None:
        changes = {
            "reviewer_role": lambda value: value.__setitem__(
                "reviewer_role", "different_reviewer"
            ),
            "reason": lambda value: value.__setitem__(
                "reason", "A different but non-empty reason."
            ),
            "expires_at": lambda value: value.__setitem__(
                "expires_at", "2098-01-01T00:00:00Z"
            ),
            "review_manifest_sha256": lambda value: value.__setitem__(
                "review_manifest_sha256", "0" * 64
            ),
        }
        for name, change in changes.items():
            with self.subTest(name=name):
                run_dir = self.prepare(workspace_name=f"decision-integrity-{name}")
                decision_path = self.approve(run_dir)
                decision = read_json(decision_path)
                change(decision)
                write_json(decision_path, decision)
                self.assert_safe_stop(
                    "decision_integrity_mismatch",
                    export_approved,
                    run_dir,
                    CHECKED,
                )

    def test_existing_csv_conflict_cannot_leave_partial_json_export(self) -> None:
        run_dir = self.prepare()
        self.approve(run_dir)
        outbox = run_dir / "outbox"
        outbox.mkdir()
        (outbox / "approved-r1.csv").write_text(
            "different\n",
            encoding="utf-8",
        )
        self.assert_safe_stop(
            "export_pair_mismatch",
            export_approved,
            run_dir,
            CHECKED,
        )
        self.assertFalse((outbox / "approved-r1.json").exists())
        self.assertEqual(
            (outbox / "approved-r1.csv").read_text(encoding="utf-8"),
            "different\n",
        )
        blocked_run = self.prepare(workspace_name="outbox-wrong-type")
        self.approve(blocked_run)
        (blocked_run / "outbox").write_text("not a directory", encoding="utf-8")
        self.assert_safe_stop(
            "export_write_error",
            export_approved,
            blocked_run,
            CHECKED,
        )
        result, output = self.run_cli(
            [
                "export",
                "--run-dir",
                str(blocked_run),
                "--checked-at",
                "2026-07-28T11:00:00Z",
            ]
        )
        self.assertEqual(result, 1)
        self.assertIn("SAFE STOP: export_write_error", output)
        self.assertNotIn("Traceback", output)
        self.assertEqual(
            read_json(blocked_run / "failures" / "latest.json")["error_code"],
            "export_write_error",
        )

    def test_second_export_promotion_failure_rolls_back_first_file(self) -> None:
        run_dir = self.prepare()
        self.approve(run_dir)
        real_replace = os.replace

        def fail_csv_promotion(source, destination):
            destination_path = Path(destination)
            if destination_path.name == "approved-r1.csv":
                raise OSError("simulated second promotion failure")
            return real_replace(source, destination)

        with patch(
            "course1_capstone.workflow.os.replace",
            side_effect=fail_csv_promotion,
        ):
            self.assert_safe_stop(
                "export_write_error",
                export_approved,
                run_dir,
                CHECKED,
            )
        self.assertFalse((run_dir / "outbox" / "approved-r1.json").exists())
        self.assertFalse((run_dir / "outbox" / "approved-r1.csv").exists())

    def test_csv_exports_neutralize_formula_prefixes_but_json_keeps_evidence(
        self,
    ) -> None:
        input_path = self.workspace / "spreadsheet-risk.csv"
        rows = [
            [
                "WI-9101",
                "=REF",
                "Controlled title one",
                "operations",
                "new",
                " +FORMULA",
                "2026-07-20",
                "2026-08-01",
                "",
                "",
                "",
                "admin",
            ],
            [
                "WI-9102",
                "=REF",
                "Controlled title two",
                "operations",
                "new",
                "low",
                "2026-07-20",
                "2026-08-01",
                "",
                "\t-FORMULA",
                "EUR",
                "admin",
            ],
            [
                "WI-9103",
                "REF-9103",
                "Controlled title three",
                "operations",
                "\t@FORMULA",
                "low",
                "2026-07-20",
                "2026-08-01",
                "",
                "",
                "",
                "admin",
            ],
        ]
        with input_path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(
                [
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
            )
            writer.writerows(rows)
        run_dir = self.prepare(input_path=input_path, expected_path=None)
        self.approve(run_dir)
        json_path, csv_path = export_approved(run_dir, CHECKED)
        payload_text = json_path.read_text(encoding="utf-8")
        self.assertIn('"source_reference":"=REF"', payload_text)
        self.assertIn('"raw_value":" +FORMULA"', payload_text)
        self.assertIn('"raw_value":"\\t-FORMULA"', payload_text)
        self.assertIn('"raw_value":"\\t@FORMULA"', payload_text)
        exported_rows = list(
            csv.DictReader(csv_path.read_text(encoding="utf-8").splitlines())
        )
        dangerous_cells = [
            cell
            for row in exported_rows
            for cell in row.values()
            if cell and any(marker in cell for marker in ("FORMULA", "=REF"))
        ]
        self.assertTrue(dangerous_cells)
        self.assertTrue(all(cell.startswith("'") for cell in dangerous_cells))

    def test_all_untrusted_prose_fields_remain_out_of_summary(self) -> None:
        input_path = self.workspace / "untrusted-prose.csv"
        markers = {
            "source_reference": "SOURCE-INSTRUCTION-ALPHA",
            "title": "TITLE-INSTRUCTION-BRAVO",
            "owner_role": "OWNER-INSTRUCTION-CHARLIE",
            "category": "CATEGORY-INSTRUCTION-DELTA",
        }
        base = {
            "source_reference": "do",
            "title": "Review",
            "owner_role": "field",
            "category": "row",
        }
        with input_path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(
                stream,
                fieldnames=[
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
                ],
            )
            writer.writeheader()
            for index, (field, marker) in enumerate(markers.items(), start=1):
                values = dict(base)
                values[field] = marker
                writer.writerow(
                    {
                        "work_item_id": f"WI-92{index:02d}",
                        **values,
                        "status": "new",
                        "priority": "urgent",
                        "received_date": "2026-07-20",
                        "due_date": "2026-08-01",
                        "completed_date": "",
                        "amount": "",
                        "currency": "",
                    }
                )
        run_dir = self.prepare(input_path=input_path, expected_path=None)
        summary_text = (run_dir / "draft" / "summary.json").read_text(encoding="utf-8")
        for marker in markers.values():
            self.assertNotIn(marker, summary_text)

    def test_repeated_safe_stops_keep_unique_attempt_history(self) -> None:
        run_dir = self.prepare()
        candidate = read_json(run_dir / "draft" / "summary.json")
        candidate["review_actions"][0]["issue_ids"] = 7
        candidate_path = self.workspace / "bad-repeat-candidate.json"
        write_json(candidate_path, candidate)
        arguments = [
            "validate-summary",
            "--run-dir",
            str(run_dir),
            "--candidate",
            str(candidate_path),
        ]
        for _ in range(2):
            result, _ = self.run_cli(arguments)
            self.assertEqual(result, 1)
        attempts = sorted((run_dir / "failures").glob("a*.json"))
        self.assertEqual(len(attempts), 2)
        attempt_ids = {read_json(path)["attempt_id"] for path in attempts}
        self.assertEqual(len(attempt_ids), 2)
        status = inspect_run(run_dir)
        self.assertEqual(status["current_state"], "needs_review")
        self.assertEqual(status["latest_attempt_state"], "failed_manual")

    def test_damaged_state_still_produces_named_failed_manual_evidence(self) -> None:
        run_dir = self.prepare()
        (run_dir / "state.json").write_text("{broken", encoding="utf-8")
        result, output = self.run_cli(["status", "--run-dir", str(run_dir)])
        self.assertEqual(result, 1)
        self.assertIn("SAFE STOP: malformed_json", output)
        evidence = read_json(run_dir / "failures" / "latest.json")
        self.assertEqual(evidence["state"], "failed_manual")
        self.assertFalse(evidence["audit_recorded"])
        self.assertTrue((run_dir / evidence["history_path"]).exists())

    def test_damaged_audit_still_produces_named_failed_manual_evidence(self) -> None:
        run_dir = self.prepare()
        with (run_dir / "audit" / "events.jsonl").open("a", encoding="utf-8") as stream:
            stream.write("{broken\n")
        result, output = self.run_cli(["status", "--run-dir", str(run_dir)])
        self.assertEqual(result, 1)
        self.assertIn("SAFE STOP: audit_corrupt", output)
        evidence = read_json(run_dir / "failures" / "latest.json")
        self.assertEqual(evidence["state"], "failed_manual")
        self.assertFalse(evidence["audit_recorded"])
        self.assertEqual(evidence["audit_error"], "audit_corrupt")

    def test_failure_evidence_stays_within_legacy_windows_path_budget(self) -> None:
        long_base = self.workspace / "p"
        target_base_length = 228
        while len(str(long_base)) < target_base_length:
            available = target_base_length - len(str(long_base)) - 1
            if available <= 0:
                break
            long_base /= "x" * min(40, available)
        long_base.mkdir(parents=True)
        args = argparse.Namespace(command="status", run_dir=long_base)
        latest_path = record_safe_stop(
            args,
            SafeStop("unknown_ai_issue_reference", "Synthetic test stop."),
        )
        self.assertEqual(latest_path, long_base / "failures" / "latest.json")
        self.assertTrue(latest_path.is_file())
        latest = read_json(latest_path)
        history_path = long_base / latest["history_path"]
        self.assertTrue(history_path.is_file())
        self.assertLess(len(str(latest_path)), 260)
        self.assertLess(len(str(history_path)), 260)
        self.assertFalse(
            any(
                path.name.startswith("~") for path in (long_base / "failures").iterdir()
            )
        )

    def test_long_workspace_unknown_reference_cli_keeps_failure_evidence(self) -> None:
        long_workspace = self.workspace / "learner"
        target_workspace_length = 175
        while len(str(long_workspace)) < target_workspace_length:
            available = target_workspace_length - len(str(long_workspace)) - 1
            if available <= 0:
                break
            long_workspace /= "w" * min(35, available)
        run_dir = prepare_run(
            FROZEN_INPUT,
            long_workspace,
            "mock",
            SYNTHETIC_CONFIRMATION,
            FROZEN_EXPECTED,
        )
        candidate = read_json(run_dir / "draft" / "summary.json")
        candidate["groups"][0]["issue_ids"][0] = "WI-9999|R999|unknown"
        candidate["groups"][0]["summary"] = (
            "[WI-9999|R999|unknown] This reference was not verified."
        )
        candidate_path = long_workspace / "candidate.json"
        write_json(candidate_path, candidate)
        result, output = self.run_cli(
            [
                "validate-summary",
                "--run-dir",
                str(run_dir),
                "--candidate",
                str(candidate_path),
            ]
        )
        self.assertEqual(result, 1)
        self.assertIn("SAFE STOP: unknown_ai_issue_reference", output)
        self.assertIn("FAILURE_EVIDENCE=failures/latest.json", output)
        latest = read_json(run_dir / "failures" / "latest.json")
        self.assertEqual(latest["error_code"], "unknown_ai_issue_reference")
        self.assertTrue((run_dir / latest["history_path"]).is_file())
        self.assertLess(
            len(str(run_dir / "failures" / "latest.json")),
            260,
        )

    def test_failure_scenario_register_names_every_required_failure(self) -> None:
        scenarios = read_json(FIXTURES / "failure_scenarios.json")
        required = {
            "duplicate_work_item_id",
            "required_review_without_evidence",
            "stale_update",
            "malformed_input",
            "missing_file",
            "unexpected_header",
            "duplicate_retry",
            "ai_disabled",
            "ai_timeout",
            "ai_refusal",
            "malformed_ai_json",
            "unknown_ai_issue_reference",
            "edited_draft_after_approval",
            "rejected_review",
            "edit_review",
            "expired_review",
            "explicit_expire",
            "external_actions_false",
            "external_actions_tampered",
            "untrusted_free_text",
        }
        self.assertTrue(required.issubset(set(scenarios)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
