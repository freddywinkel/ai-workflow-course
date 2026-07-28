from __future__ import annotations

import ast
import contextlib
import csv
import io
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from course1_capstone.cli import main as cli_main
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
        with patch.object(
            sys,
            "argv",
            ["course1-capstone", *arguments],
        ), contextlib.redirect_stdout(output):
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
            csv.DictReader(
                FROZEN_EXPECTED.read_text(encoding="utf-8").splitlines()
            )
        )
        found = {
            (row["work_item_id"], row["rule_code"], row["field"])
            for row in issues
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
        evidence = workspace / "failures" / "safe-stop-missing_file.json"
        self.assertTrue(evidence.exists())
        record = read_json(evidence)
        self.assertEqual(record["state"], "failed_manual")
        self.assertEqual(record["error_code"], "missing_file")
        self.assertEqual(record["external_actions"], 0)
        self.assertIn(
            "FAILURE_EVIDENCE=failures/safe-stop-missing_file.json",
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
                    / "safe-stop-missing_file.json"
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
                    / "safe-stop-missing_file.json"
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
        source_hash_before = (
            run_dir / "source" / "work_items.csv"
        ).read_bytes()
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

    def test_ai_disabled_timeout_refusal_malformed_and_unknown_use_fallback(self) -> None:
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
        candidate["headline"] = "A learner-created bounded synthetic summary."
        candidate_path = self.workspace / "candidate.json"
        write_json(candidate_path, candidate)
        result_path = validate_candidate_summary(run_dir, candidate_path)
        result = read_json(result_path)
        self.assertEqual(result["issue_reference_count"], 13)
        self.assertTrue(result["human_support_review_required"])
        candidate["groups"][0]["issue_ids"][0] = "WI-9999|R999|unknown"
        write_json(candidate_path, candidate)
        self.assert_safe_stop(
            "unknown_ai_issue_reference",
            validate_candidate_summary,
            run_dir,
            candidate_path,
        )

    def test_summary_runtime_validation_matches_schema_constraints(self) -> None:
        run_dir = self.prepare()
        candidate_path = self.workspace / "candidate.json"
        invalid_changes = {
            "blank_prompt_version": lambda value: value.__setitem__(
                "prompt_version",
                "",
            ),
            "invalid_action_id": lambda value: value["review_actions"][0].__setitem__(
                "action_id",
                "ACTION-1",
            ),
            "non_array_action_issue_ids": lambda value: value[
                "review_actions"
            ][0].__setitem__("issue_ids", 7),
        }
        for name, change in invalid_changes.items():
            with self.subTest(name=name):
                candidate = read_json(run_dir / "draft" / "summary.json")
                change(candidate)
                write_json(candidate_path, candidate)
                self.assert_safe_stop(
                    "summary_contract",
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
            "FAILURE_EVIDENCE=failures/safe-stop-summary_contract.json",
            command_output,
        )
        evidence = read_json(
            run_dir / "failures" / "safe-stop-summary_contract.json"
        )
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
        replacement["headline"] = "Human review is required for 13 verified issues."
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
            "FAILURE_EVIDENCE=failures/safe-stop-approval_contract.json",
            command_output,
        )
        evidence = read_json(
            run_dir / "failures" / "safe-stop-approval_contract.json"
        )
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
        run_locator = (
            workspace / "latest_run.txt"
        ).read_text(encoding="utf-8").strip()
        run_dir = (workspace / Path(run_locator)).resolve()
        self.assertIn(f"RUN_ID={run_dir.name}", prepare_output)
        self.assertIn(f"RUN_LOCATOR={run_locator}", prepare_output)

        candidate = read_json(run_dir / "draft" / "summary.json")
        candidate["headline"] = "A bounded candidate for neutral output testing."
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
