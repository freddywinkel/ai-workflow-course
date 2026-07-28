from __future__ import annotations

import csv
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

import jsonschema

from course1_capstone.workflow import (
    SYNTHETIC_CONFIRMATION,
    SafeStop,
    prepare_run,
    record_decision,
    validate_review_manifest,
    validate_state,
)

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "schemas"
INPUT = ROOT / "practice_data" / "work_items.csv"
EXPECTED = ROOT / "practice_data" / "expected_issues.csv"


def load_schema(name: str) -> dict:
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def validate(instance, schema_name: str) -> None:
    validator = jsonschema.Draft202012Validator(
        load_schema(schema_name),
        format_checker=jsonschema.FormatChecker(),
    )
    validator.validate(instance)


class SchemaContractTests(unittest.TestCase):
    def test_all_schemas_are_valid_draft_2020_12(self) -> None:
        files = sorted(SCHEMAS.glob("*.schema.json"))
        self.assertEqual(len(files), 11)
        for path in files:
            with self.subTest(path=path.name):
                jsonschema.Draft202012Validator.check_schema(
                    json.loads(path.read_text(encoding="utf-8"))
                )

    def test_every_generated_artifact_matches_its_schema(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_dir = prepare_run(
                INPUT,
                Path(temporary),
                "mock",
                SYNTHETIC_CONFIRMATION,
                EXPECTED,
            )
            record_decision(
                run_dir,
                "approve",
                "course_learner",
                "Every synthetic source link and statement was reviewed.",
                1,
                True,
                datetime(2099, 1, 1, tzinfo=timezone.utc),
                datetime(2026, 7, 28, 10, 0, tzinfo=timezone.utc),
            )
            with INPUT.open("r", encoding="utf-8-sig", newline="") as stream:
                work_items = list(csv.DictReader(stream))
            issues = json.loads(
                (run_dir / "issues" / "issues.json").read_text(encoding="utf-8")
            )
            summary = json.loads(
                (run_dir / "draft" / "summary.json").read_text(encoding="utf-8")
            )
            approval = json.loads(
                (run_dir / "review" / "decision-r1.json").read_text(encoding="utf-8")
            )
            evaluation = json.loads(
                (run_dir / "evaluation.json").read_text(encoding="utf-8")
            )
            state = json.loads((run_dir / "state.json").read_text(encoding="utf-8"))
            control = json.loads((run_dir / "control.json").read_text(encoding="utf-8"))
            run_config = json.loads(
                (run_dir / "run_config.json").read_text(encoding="utf-8")
            )
            review_package = json.loads(
                (run_dir / "review" / "review_package.json").read_text(encoding="utf-8")
            )
            review_manifest = json.loads(
                (run_dir / "review" / "review_manifest.json").read_text(
                    encoding="utf-8"
                )
            )
            audit_events = [
                json.loads(line)
                for line in (run_dir / "audit" / "events.jsonl")
                .read_text(encoding="utf-8")
                .splitlines()
                if line.strip()
            ]
            for item in work_items:
                validate(item, "work_item.schema.json")
            for issue in issues:
                validate(issue, "issue.schema.json")
            validate(summary, "summary.schema.json")
            validate(approval, "approval.schema.json")
            validate(evaluation, "evaluation.schema.json")
            validate(state, "state.schema.json")
            validate(control, "control.schema.json")
            validate(run_config, "run_config.schema.json")
            validate(review_package, "review_package.schema.json")
            validate(review_manifest, "review_manifest.schema.json")
            for event in audit_events:
                validate(event, "audit_event.schema.json")

            invalid_state = dict(state)
            invalid_state["external_actions"] = False
            with self.assertRaises(SafeStop):
                validate_state(invalid_state)
            with self.assertRaises(jsonschema.ValidationError):
                validate(invalid_state, "state.schema.json")
            invalid_state = dict(state)
            invalid_state.update(
                {
                    "current_state": "needs_review",
                    "active_decision_path": state["active_decision_path"],
                    "local_export_count": 0,
                }
            )
            with self.assertRaises(SafeStop):
                validate_state(invalid_state)
            with self.assertRaises(jsonschema.ValidationError):
                validate(invalid_state, "state.schema.json")
            invalid_state = dict(state)
            invalid_state.update(
                {
                    "current_state": "needs_review",
                    "draft_revision": 0,
                    "draft_sha256": None,
                    "review_manifest_sha256": None,
                    "active_decision_path": None,
                    "summary_generator": None,
                    "local_export_count": 0,
                }
            )
            with self.assertRaises(SafeStop):
                validate_state(invalid_state)
            with self.assertRaises(jsonschema.ValidationError):
                validate(invalid_state, "state.schema.json")
            invalid_state = dict(state)
            invalid_state.update(
                {
                    "current_state": "needs_review",
                    "active_decision_path": None,
                    "summary_generator": None,
                    "local_export_count": 0,
                }
            )
            with self.assertRaises(SafeStop):
                validate_state(invalid_state)
            with self.assertRaises(jsonschema.ValidationError):
                validate(invalid_state, "state.schema.json")
            invalid_manifest = json.loads(json.dumps(review_manifest))
            invalid_manifest["draft_revision"] = 0
            with self.assertRaises(SafeStop):
                validate_review_manifest(
                    invalid_manifest,
                    run_id=state["run_id"],
                    draft_revision=0,
                    run_config=run_config,
                )
            with self.assertRaises(jsonschema.ValidationError):
                validate(
                    invalid_manifest,
                    "review_manifest.schema.json",
                )
            invalid_evaluation = dict(evaluation)
            invalid_evaluation["current_state"] = "summary_ready"
            with self.assertRaises(jsonschema.ValidationError):
                validate(invalid_evaluation, "evaluation.schema.json")
            invalid_evaluation = dict(evaluation)
            invalid_evaluation["external_actions"] = False
            with self.assertRaises(jsonschema.ValidationError):
                validate(invalid_evaluation, "evaluation.schema.json")
            invalid_summary = json.loads(json.dumps(summary))
            invalid_summary["review_actions"][0]["instruction"] = (
                "Pay the vendor and update the source system."
            )
            with self.assertRaises(jsonschema.ValidationError):
                validate(invalid_summary, "summary.schema.json")


if __name__ == "__main__":
    unittest.main(verbosity=2)
