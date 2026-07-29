from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from validate_package import curriculum_date_metadata_failures  # noqa: E402


class CurriculumDateMetadataTests(unittest.TestCase):
    def setUp(self) -> None:
        self.curriculum = json.loads(
            (ROOT / "curriculum.json").read_text(encoding="utf-8")
        )
        self.source_claims = json.loads(
            (ROOT / "source_claims.json").read_text(encoding="utf-8")
        )
        self.contract = json.loads(
            (
                ROOT
                / "audit_control/course1/curriculum_date_contract.json"
            ).read_text(encoding="utf-8")
        )

    def failures(
        self,
        curriculum: dict,
        *,
        source_claims: dict | None = None,
        contract: dict | None = None,
    ) -> list[str]:
        return curriculum_date_metadata_failures(
            ROOT,
            curriculum,
            source_claims_override=(
                self.source_claims if source_claims is None else source_claims
            ),
            contract_override=self.contract if contract is None else contract,
        )

    def assert_failure_contains(
        self,
        failures: list[str],
        phrase: str,
    ) -> None:
        self.assertTrue(
            any(phrase in failure for failure in failures),
            failures,
        )

    def test_current_separated_metadata_passes(self) -> None:
        self.assertEqual(self.failures(self.curriculum), [])
        self.assertEqual(
            self.curriculum["course"]["sourceVerifiedThrough"],
            "2026-07-28",
        )
        self.assertEqual(
            self.curriculum["course"]["contentRevisionThrough"],
            "2026-07-29",
        )

    def test_content_revision_can_advance_without_source_claim(self) -> None:
        curriculum = copy.deepcopy(self.curriculum)
        changed = False
        for group in curriculum["groups"]:
            for document in group["documents"]:
                if document["revision"] == "2026-07-29":
                    document["revision"] = "2026-07-30"
                    changed = True
                    break
            if changed:
                break
        self.assertTrue(changed)
        curriculum["course"]["contentRevisionThrough"] = "2026-07-30"

        self.assertEqual(self.failures(curriculum), [])
        self.assertEqual(
            curriculum["course"]["sourceVerifiedThrough"],
            "2026-07-28",
        )
        self.assertEqual(curriculum["course"]["verifiedThrough"], "2026-07-28")

    def test_false_source_advance_fails_against_claim_evidence(self) -> None:
        curriculum = copy.deepcopy(self.curriculum)
        source_claims = copy.deepcopy(self.source_claims)
        curriculum["course"]["sourceVerifiedThrough"] = "2026-07-29"
        curriculum["course"]["verifiedThrough"] = "2026-07-29"
        source_claims["verifiedThrough"] = "2026-07-29"

        failures = self.failures(curriculum, source_claims=source_claims)
        self.assert_failure_contains(
            failures,
            "must equal the oldest entries[].lastVerified date",
        )

    def test_curriculum_source_date_cannot_drift_from_source_claims(self) -> None:
        curriculum = copy.deepcopy(self.curriculum)
        curriculum["course"]["sourceVerifiedThrough"] = "2026-07-29"
        curriculum["course"]["verifiedThrough"] = "2026-07-29"

        failures = self.failures(curriculum)
        self.assert_failure_contains(
            failures,
            "must equal source_claims.json verifiedThrough",
        )

    def test_legacy_alias_cannot_become_an_independent_claim(self) -> None:
        curriculum = copy.deepcopy(self.curriculum)
        curriculum["course"]["verifiedThrough"] = "2026-07-29"

        failures = self.failures(curriculum)
        self.assert_failure_contains(
            failures,
            "compatibility alias must equal course.sourceVerifiedThrough",
        )

    def test_content_summary_must_equal_latest_document_revision(self) -> None:
        curriculum = copy.deepcopy(self.curriculum)
        curriculum["course"]["contentRevisionThrough"] = "2026-07-30"

        failures = self.failures(curriculum)
        self.assert_failure_contains(
            failures,
            "must equal the latest document revision",
        )

    def test_date_contract_is_closed_and_semantic(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["fields"]["contentRevisionThrough"]["researchMeaning"] = (
            "not allowed"
        )

        failures = self.failures(self.curriculum, contract=contract)
        self.assert_failure_contains(
            failures,
            "contentRevisionThrough must use its exact closed shape",
        )


if __name__ == "__main__":
    unittest.main()
