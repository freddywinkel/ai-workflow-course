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
    prepare_run,
    record_decision,
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
        self.assertEqual(len(files), 6)
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
            for event in audit_events:
                validate(event, "audit_event.schema.json")


if __name__ == "__main__":
    unittest.main(verbosity=2)
