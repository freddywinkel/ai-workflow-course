from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from validate_package import (  # noqa: E402
    EXPECTED_LEARNING_METHOD_IDS,
    LEARNING_EVIDENCE_CLASSES,
    learning_audit_control_failures,
    load_json_object,
    validate_learning_evidence_record,
)


class LearningAuditControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = (
            ROOT / "COURSE_1_LEARNING_VALIDATION_CONTRACT.md"
        ).read_text(encoding="utf-8")
        cls.matrix = load_json_object(
            ROOT / "audit_control/course1/learning_claim_evidence_matrix.json"
        )
        cls.template = load_json_object(
            ROOT
            / "release_evidence/templates/COURSE_1_LEARNING_EVIDENCE_RECORD.template.json"
        )

    def failures(
        self,
        *,
        contract: str | None = None,
        matrix: dict | None = None,
        template: dict | None = None,
    ) -> list[str]:
        return learning_audit_control_failures(
            ROOT,
            contract_text=self.contract if contract is None else contract,
            matrix=copy.deepcopy(self.matrix) if matrix is None else matrix,
            template=copy.deepcopy(self.template) if template is None else template,
        )

    def assert_failure_contains(self, failures: list[str], phrase: str) -> None:
        self.assertTrue(
            any(phrase in failure for failure in failures),
            failures,
        )

    def test_current_matrix_is_closed_and_honestly_unverified(self) -> None:
        self.assertEqual(self.failures(), [])
        self.assertEqual(len(self.matrix["requirements"]), 17)
        self.assertEqual(
            {
                method["methodId"]
                for row in self.matrix["requirements"]
                for method in row["assessmentMethods"]
            },
            EXPECTED_LEARNING_METHOD_IDS,
        )
        self.assertTrue(
            all(
                row["currentEvidence"]
                == {"status": "UNVERIFIED", "records": []}
                and row["learningDecision"]["status"] == "NOT YET"
                for row in self.matrix["requirements"]
            )
        )

    def test_missing_or_duplicate_requirement_fails_closed(self) -> None:
        matrix = copy.deepcopy(self.matrix)
        matrix["requirements"].pop()
        failures = self.failures(matrix=matrix)
        self.assert_failure_contains(
            failures,
            "does not exactly cover C1-LV-001 through C1-LV-017",
        )

        matrix = copy.deepcopy(self.matrix)
        matrix["requirements"].append(copy.deepcopy(matrix["requirements"][0]))
        failures = self.failures(matrix=matrix)
        self.assert_failure_contains(failures, "duplicate requirement IDs")

    def test_malformed_contract_requirement_heading_fails_closed(self) -> None:
        contract = self.contract.replace(
            "### `C1-LV-004`",
            "### C1-LV-004",
            1,
        )
        failures = self.failures(contract=contract)
        self.assert_failure_contains(failures, "malformed requirement heading")
        self.assert_failure_contains(failures, "requirement inventory/order")

    def test_unknown_matrix_key_or_evidence_class_fails_closed(self) -> None:
        matrix = copy.deepcopy(self.matrix)
        matrix["requirements"][0]["silentlyTrusted"] = True
        failures = self.failures(matrix=matrix)
        self.assert_failure_contains(failures, "unknown keys")

        matrix = copy.deepcopy(self.matrix)
        matrix["requirements"][0]["evidenceClasses"] = ["AI_REVIEW"]
        failures = self.failures(matrix=matrix)
        self.assert_failure_contains(failures, "unsupported evidence class")

    def test_missing_method_or_selector_fails_closed(self) -> None:
        matrix = copy.deepcopy(self.matrix)
        matrix["requirements"][0]["assessmentMethods"] = []
        failures = self.failures(matrix=matrix)
        self.assert_failure_contains(
            failures,
            "assessmentMethods must be a non-empty array",
        )
        self.assert_failure_contains(
            failures,
            "does not exactly cover C1-LVM-001 through C1-LVM-017",
        )

        matrix = copy.deepcopy(self.matrix)
        matrix["requirements"][0]["assessmentMethods"][0][
            "selector"
        ] = "not a real selector"
        failures = self.failures(matrix=matrix)
        self.assert_failure_contains(failures, "selector is absent")

    def test_unverified_or_pass_without_evidence_fails_closed(self) -> None:
        matrix = copy.deepcopy(self.matrix)
        matrix["requirements"][0]["currentEvidence"]["records"] = [
            {
                "path": (
                    "release_evidence/course1_learning_validation/"
                    "2.6.0/does-not-exist.json"
                ),
                "sha256": "a" * 64,
            }
        ]
        failures = self.failures(matrix=matrix)
        self.assert_failure_contains(
            failures,
            "UNVERIFIED evidence must have no records",
        )
        self.assert_failure_contains(failures, "does not exist")

        matrix = copy.deepcopy(self.matrix)
        matrix["requirements"][0]["currentEvidence"]["status"] = "PASS"
        matrix["requirements"][0]["learningDecision"]["status"] = "PASS"
        failures = self.failures(matrix=matrix)
        self.assert_failure_contains(failures, "PASS evidence must have records")
        self.assert_failure_contains(failures, "PASS evidence-class coverage mismatch")

    def test_unverified_cannot_claim_a_pass_decision(self) -> None:
        matrix = copy.deepcopy(self.matrix)
        matrix["requirements"][0]["learningDecision"]["status"] = "PASS"
        failures = self.failures(matrix=matrix)
        self.assert_failure_contains(
            failures,
            "UNVERIFIED evidence requires a NOT YET decision",
        )

    def test_evidence_record_rejects_unknown_keys_and_bad_candidate(self) -> None:
        record = copy.deepcopy(self.template)
        record["silentlyTrusted"] = True
        failures: list[str] = []
        validate_learning_evidence_record(
            record,
            label="test record",
            expected_requirement_id="C1-LV-001",
            allowed_evidence_classes=LEARNING_EVIDENCE_CLASSES,
            allowed_method_ids=EXPECTED_LEARNING_METHOD_IDS,
            expected_overall_status=None,
            failures=failures,
        )
        self.assert_failure_contains(failures, "unknown keys")

        record = copy.deepcopy(self.template)
        record["candidate"]["commit"] = "short"
        failures = []
        validate_learning_evidence_record(
            record,
            label="test record",
            expected_requirement_id="C1-LV-001",
            allowed_evidence_classes=LEARNING_EVIDENCE_CLASSES,
            allowed_method_ids=EXPECTED_LEARNING_METHOD_IDS,
            expected_overall_status=None,
            failures=failures,
        )
        self.assert_failure_contains(failures, "full Git SHA")

    def test_human_evidence_requires_full_consent_and_privacy_fields(self) -> None:
        record = copy.deepcopy(self.template)
        record["requirementId"] = "C1-LV-007"
        record["evidenceClass"] = "REAL_SYNTHETIC_UAT"
        record["task"]["methodId"] = "C1-LVM-007"
        failures: list[str] = []
        validate_learning_evidence_record(
            record,
            label="human record",
            expected_requirement_id="C1-LV-007",
            allowed_evidence_classes={"REAL_SYNTHETIC_UAT"},
            allowed_method_ids={"C1-LVM-007"},
            expected_overall_status=None,
            failures=failures,
        )
        self.assert_failure_contains(
            failures,
            "voluntaryAndRightToStopStated must be True",
        )
        self.assert_failure_contains(
            failures,
            "participationConsent must be 'YES'",
        )
        self.assert_failure_contains(
            failures,
            "retentionDeletionDate is required for human evidence",
        )


if __name__ == "__main__":
    unittest.main()
