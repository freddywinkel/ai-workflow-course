from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import verify_course1_study_release as study  # noqa: E402


class StudyReleaseVerifierTests(unittest.TestCase):
    COMMIT = "a" * 40

    def setUp(self) -> None:
        self.curriculum = json.loads(
            (ROOT / "curriculum.json").read_text(encoding="utf-8")
        )
        self.ledger = (
            ROOT / "COURSE_1_AUDIT_STATUS_AND_REPAIR_LEDGER.md"
        ).read_text(encoding="utf-8")

    def write_fixture(
        self,
        root: Path,
        *,
        curriculum: dict | None = None,
        ledger: str | None = None,
        bundled_course: dict | None = None,
        boundary: str | None = None,
    ) -> tuple[Path, Path, Path]:
        curriculum_value = curriculum or self.curriculum
        curriculum_path = root / "curriculum.json"
        curriculum_path.write_text(
            f"{json.dumps(curriculum_value, indent=2)}\n",
            encoding="utf-8",
        )
        ledger_path = root / "ledger.md"
        ledger_path.write_text(ledger or self.ledger, encoding="utf-8")
        dist = root / "dist"
        dist.mkdir()
        course = bundled_course or {
            key: curriculum_value["course"][key]
            for key in ("id", "version", "productStatus", "distributionPurpose")
        }
        (dist / "course-content.json").write_text(
            f"{json.dumps({'course': course}, indent=2)}\n",
            encoding="utf-8",
        )
        (dist / "index.html").write_text(
            boundary or " | ".join(study.BOUNDARY_TEXT),
            encoding="utf-8",
        )
        return dist, curriculum_path, ledger_path

    def identity(self) -> dict:
        return {
            "artifactFormat": "manifest-v1",
            "version": {
                "courseVersion": "2.6.0",
                "buildId": "123456789abc",
                "contentHash": "b" * 64,
                "productStatus": "UNVERIFIED",
                "distributionPurpose": "personal-synthetic-study",
            },
            "assetManifestSha256": "c" * 64,
            "artifactTreeSha256": "d" * 64,
            "publicServedTreeSha256": "e" * 64,
        }

    def validate(self, root: Path, **overrides: object) -> list[str]:
        dist, curriculum, ledger = self.write_fixture(root, **overrides)
        with patch.object(
            study,
            "inspect_artifact_identity",
            return_value=self.identity(),
        ) as inspect:
            failures, _, _ = study.validate_study_release(
                dist,
                expected_commit=self.COMMIT,
                curriculum_path=curriculum,
                ledger_path=ledger,
            )
        inspect.assert_called_once_with(
            dist,
            expected_commit=self.COMMIT,
            operation="personal-study",
        )
        return failures

    def test_current_unverified_personal_study_boundary_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            self.assertEqual(self.validate(Path(temporary)), [])

    def test_product_status_and_distribution_purpose_fail_closed(self) -> None:
        for field, wrong_value, phrase in (
            ("productStatus", "PASS", "productStatus must be UNVERIFIED"),
            (
                "distributionPurpose",
                "accepted-course-release",
                "distributionPurpose must be personal-synthetic-study",
            ),
        ):
            curriculum = copy.deepcopy(self.curriculum)
            curriculum["course"][field] = wrong_value
            with tempfile.TemporaryDirectory() as temporary:
                failures = self.validate(Path(temporary), curriculum=curriculum)
            self.assertTrue(any(phrase in failure for failure in failures), failures)

    def test_known_defect_status_blocks_publication(self) -> None:
        ledger = self.ledger.replace(
            "| CLOSED | Runner maintainer |",
            "| OPEN | Runner maintainer |",
            1,
        )
        with tempfile.TemporaryDirectory() as temporary:
            failures = self.validate(Path(temporary), ledger=ledger)
        self.assertTrue(
            any("known High/Medium defects" in failure for failure in failures),
            failures,
        )

    def test_new_unclassified_pending_finding_blocks_publication(self) -> None:
        ledger = self.ledger.replace(
            "| CLOSED | PWA contract and test owners |",
            "| EVIDENCE PENDING | PWA contract and test owners |",
            1,
        )
        with tempfile.TemporaryDirectory() as temporary:
            failures = self.validate(Path(temporary), ledger=ledger)
        self.assertTrue(
            any("unclassified evidence-pending" in failure for failure in failures),
            failures,
        )

    def test_missing_public_boundary_copy_blocks_publication(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            failures = self.validate(Path(temporary), boundary="UNVERIFIED")
        self.assertTrue(
            any("published learner boundary" in failure for failure in failures),
            failures,
        )

    def test_short_commit_is_rejected_without_artifact_inspection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            dist, curriculum, ledger = self.write_fixture(Path(temporary))
            with patch.object(study, "inspect_artifact_identity") as inspect:
                failures, _, _ = study.validate_study_release(
                    dist,
                    expected_commit=self.COMMIT[:12],
                    curriculum_path=curriculum,
                    ledger_path=ledger,
                )
            inspect.assert_not_called()
        self.assertTrue(any("40-character" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
