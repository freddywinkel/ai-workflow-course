from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from validate_package import learning_content_repair_failures  # noqa: E402


class LearningContentRepairTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def assert_failure_contains(self, failures: list[str], phrase: str) -> None:
        self.assertTrue(
            any(phrase in failure for failure in failures),
            failures,
        )

    def test_current_content_repairs_pass_the_structural_contract(self) -> None:
        self.assertEqual(learning_content_repair_failures(ROOT), [])

    def test_study_block_over_60_minutes_fails_closed(self) -> None:
        path = "BEGINNER_READINESS_CHECK.md"
        changed = self.read(path).replace("| 1 | 45 minutes |", "| 1 | 61 minutes |", 1)
        failures = learning_content_repair_failures(
            ROOT,
            text_overrides={path: changed},
        )
        self.assert_failure_contains(failures, "planned block over 60 minutes")

    def test_missing_estimate_or_resume_boundary_fails_closed(self) -> None:
        path = "BEGINNER_SOFTWARE_CHECK.md"
        changed = self.read(path).replace(
            "AUTHOR ESTIMATE — NOT BEGINNER MEASURED",
            "planning range",
            1,
        )
        failures = learning_content_repair_failures(
            ROOT,
            text_overrides={path: changed},
        )
        self.assert_failure_contains(failures, "AUTHOR ESTIMATE")

    def test_private_note_regression_fails_closed(self) -> None:
        path = "README.md"
        changed = self.read(path).replace("learner notes", "private notes", 1)
        failures = learning_content_repair_failures(
            ROOT,
            text_overrides={path: changed},
        )
        self.assert_failure_contains(failures, "shared-origin learner notes as private")

    def test_role_simulation_mislabelling_fails_closed(self) -> None:
        path = "modules/MODULE_09.md"
        changed = self.read(path).replace(
            "# Worked role-simulated acceptance rehearsal and handover",
            "# Worked UAT and handover",
            1,
        )
        failures = learning_content_repair_failures(
            ROOT,
            text_overrides={path: changed},
        )
        self.assert_failure_contains(failures, "titles role simulation as Worked UAT")

    def test_missing_consent_or_oral_safeguard_fails_closed(self) -> None:
        path = "templates/uat_script.md"
        changed = self.read(path).replace(
            "Voluntary choice explained",
            "Choice discussed",
            1,
        )
        failures = learning_content_repair_failures(
            ROOT,
            text_overrides={path: changed},
        )
        self.assert_failure_contains(failures, "Voluntary choice explained")

        path = "ASSESSMENT_AND_RUBRIC.md"
        changed = self.read(path).replace("`I do not know`", "`unknown`", 1)
        failures = learning_content_repair_failures(
            ROOT,
            text_overrides={path: changed},
        )
        self.assert_failure_contains(failures, "`I do not know`")

    def test_optional_abbreviation_regression_fails_closed(self) -> None:
        path = "templates/runbook_and_fallback.md"
        changed = self.read(path).replace(
            "Recovery Time Objective (RTO) / Recovery Point Objective (RPO)",
            "RTO/RPO",
            1,
        )
        failures = learning_content_repair_failures(
            ROOT,
            text_overrides={path: changed},
        )
        self.assert_failure_contains(failures, "does not expand RTO and RPO")

    def test_hard_coded_module_six_test_count_fails_closed(self) -> None:
        path = "modules/MODULE_06.md"
        changed = self.read(path).replace(
            "$expectedCourseOneTests = $declaredCourseOneTests.Count",
            "$expectedCourseOneTests = 61",
            1,
        )
        failures = learning_content_repair_failures(
            ROOT,
            text_overrides={path: changed},
        )
        self.assert_failure_contains(
            failures,
            "hard-codes the Course 1 automated test count",
        )


if __name__ == "__main__":
    unittest.main()
