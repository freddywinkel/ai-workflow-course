from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from validate_package import Report, validate_current_status_consumers  # noqa: E402


PROTOCOL_PATH = ROOT / "COURSE_1_GROUND_UP_AUDIT_PROTOCOL.md"
REQUEST_PATH = ROOT / "COURSE_1_AUDIT_REQUEST_TEMPLATE.md"
AGENTS_PATH = ROOT / "AGENTS.md"
CURRICULUM_PATH = ROOT / "curriculum.json"


class GroundUpAuditProtocolTests(unittest.TestCase):
    def _write_minimal_status_consumers(self, root: Path) -> None:
        (root / "COURSE_1_AUDIT_STATUS_AND_REPAIR_LEDGER.md").write_text(
            "# Ledger\n\n- Current status: **`UNVERIFIED`**\n",
            encoding="utf-8",
        )
        (root / "README.md").write_text(
            "Current product status: **`UNVERIFIED`**\n",
            encoding="utf-8",
        )
        (root / "RELEASE_VALIDATION.md").write_text(
            "The ledger currently records version 2.6.0 as\n`UNVERIFIED`.\n",
            encoding="utf-8",
        )
        (root / "PWA_AND_UPDATES.md").write_text(
            "The current local version 2.6.0 working copy is "
            "**`UNVERIFIED`**.\n",
            encoding="utf-8",
        )
        (root / "COURSE_CHANGELOG.md").write_text(
            "The authoritative ledger currently\nrecords `UNVERIFIED`; follow.\n",
            encoding="utf-8",
        )

    def test_all_stable_audit_assurance_rules_exist_once(self) -> None:
        protocol = PROTOCOL_PATH.read_text(encoding="utf-8")
        declared_rows = re.findall(r"^\| `(C1-AA-\d{3})` \|", protocol, re.MULTILINE)
        expected = [f"C1-AA-{number:03d}" for number in range(1, 17)]
        self.assertEqual(declared_rows, expected)

    def test_project_instructions_cross_link_both_audit_documents(self) -> None:
        agents = AGENTS_PATH.read_text(encoding="utf-8")
        self.assertIn("COURSE_1_GROUND_UP_AUDIT_PROTOCOL.md", agents)
        self.assertIn("COURSE_1_AUDIT_REQUEST_TEMPLATE.md", agents)
        self.assertIn("read-only diagnosis", agents)
        self.assertIn("Do not begin repair until the user", agents)

    def test_request_separates_diagnosis_from_approved_repair(self) -> None:
        request = REQUEST_PATH.read_text(encoding="utf-8")
        self.assertIn("COURSE_1_GROUND_UP_AUDIT_PROTOCOL.md", request)
        self.assertIn("diagnostic and read-only", request)
        self.assertIn("Stop after the plan and wait for my approval.", request)
        self.assertIn("Implement the approved ground-up Course 1 repair plan", request)
        self.assertIn("disposable isolated copies", request)
        self.assertIn("if I separately authorized a commit/candidate freeze", request)

    def test_audit_documents_remain_unbundled_governance(self) -> None:
        curriculum = json.loads(CURRICULUM_PATH.read_text(encoding="utf-8"))
        serialized = json.dumps(curriculum, ensure_ascii=False)
        self.assertNotIn("COURSE_1_GROUND_UP_AUDIT_PROTOCOL.md", serialized)
        self.assertNotIn("COURSE_1_AUDIT_REQUEST_TEMPLATE.md", serialized)

    def test_current_status_and_delta_mode_consumers_are_aligned(self) -> None:
        ledger = (
            ROOT / "COURSE_1_AUDIT_STATUS_AND_REPAIR_LEDGER.md"
        ).read_text(encoding="utf-8")
        release = (ROOT / "RELEASE_VALIDATION.md").read_text(encoding="utf-8")
        evergreen = (ROOT / "EVERGREEN_UPDATE_PROMPT.md").read_text(encoding="utf-8")
        learning = (ROOT / "COURSE_1_LEARNING_VALIDATION_CONTRACT.md").read_text(
            encoding="utf-8"
        )
        changelog = (ROOT / "COURSE_CHANGELOG.md").read_text(encoding="utf-8")
        pwa_updates = (ROOT / "PWA_AND_UPDATES.md").read_text(encoding="utf-8")
        tools_readme = (ROOT / "tools" / "README.md").read_text(encoding="utf-8")
        rollback = (ROOT / "ROLLBACK_RUNBOOK.md").read_text(encoding="utf-8")
        root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
        acceptance_24 = (
            ROOT / "release_evidence" / "COURSE_1_V2.4.0_ACCEPTANCE.md"
        ).read_text(encoding="utf-8")
        acceptance_25 = (
            ROOT / "release_evidence" / "COURSE_1_V2.5.0_ACCEPTANCE.md"
        ).read_text(encoding="utf-8")
        gap_review = (
            ROOT / "updates" / "COURSE_1_AUDIT_METHOD_GAP_REVIEW_2026-07-29.md"
        ).read_text(encoding="utf-8")
        repair_candidate = (
            ROOT
            / "release_evidence"
            / "COURSE_1_V2.6.0_REPAIR_CANDIDATE_2026-07-28.md"
        ).read_text(encoding="utf-8")
        normalized_changelog = re.sub(
            r"\s+",
            " ",
            re.sub(r"(?m)^>\s?", "", changelog),
        )

        current_markers = re.findall(
            r"^- Current status: \*\*`([^`\r\n]+)`\*\*$",
            ledger,
            re.MULTILINE,
        )
        self.assertEqual(current_markers, ["UNVERIFIED"])

        finding_states: dict[str, str] = {}
        for line in ledger.splitlines():
            if not line.startswith("| `C1-GOV-"):
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            self.assertEqual(len(cells), 6)
            finding_states[cells[0].strip("`")] = cells[4]
        self.assertEqual(finding_states["C1-GOV-007"], "EVIDENCE PENDING")
        self.assertEqual(finding_states["C1-GOV-011"], "EVIDENCE PENDING")
        self.assertEqual(finding_states["C1-GOV-013"], "CLOSED")
        self.assertEqual(finding_states["C1-GOV-015"], "CLOSED")

        self.assertIn("ledger currently records version 2.6.0 as", release)
        self.assertIn("`UNVERIFIED`", release)
        self.assertIn("all-33-test final-adjudication gate is implemented", release)
        self.assertNotIn(
            "`REPAIR REQUIRED` because known audit-control findings remain",
            release,
        )
        self.assertIn("READ-ONLY DELTA DIAGNOSIS", evergreen)
        self.assertIn("APPROVED DELTA REPAIR", evergreen)
        self.assertIn("COURSE_1_GROUND_UP_AUDIT_PROTOCOL.md", evergreen)
        self.assertIn("explicitly unpromoted", learning)
        self.assertIn(
            "The authoritative ledger currently records",
            normalized_changelog,
        )
        self.assertIn("records `UNVERIFIED`; follow", normalized_changelog)
        self.assertIn(
            "the later audit-control repair closed them",
            changelog,
        )
        self.assertIn("Steps 2–14 apply only to an `APPROVED DELTA REPAIR`", pwa_updates)
        self.assertIn("This closes the reproduced parser bypasses", tools_readme)
        self.assertIn("under `C1-GOV-012`", tools_readme)
        self.assertIn("adversarial parser suite recorded under `C1-GOV-012`", rollback)
        self.assertIn("- Version: 2.6.0 repair working copy", root_readme)
        self.assertIn("Current product status: **`UNVERIFIED`**", root_readme)
        self.assertIn("C1-GOV-011` is implemented", root_readme)
        self.assertIn("working copy is **`UNVERIFIED`**, not `PASS`", pwa_updates)
        self.assertIn("all-33-test final-adjudication gate is", pwa_updates)
        self.assertIn("`SUPERSEDED`", acceptance_24)
        self.assertIn("COURSE_1_AUDIT_STATUS_AND_REPAIR_LEDGER.md", acceptance_24)
        self.assertIn("COURSE_1_AUDIT_STATUS_AND_REPAIR_LEDGER.md", acceptance_25)
        self.assertNotIn("**`UNVERIFIED`** for the version 2.6.0", acceptance_25)
        self.assertIn("`C1-GOV-013` and `C1-GOV-015` are now `CLOSED`", gap_review)
        self.assertIn(
            "authoritative current product status is `UNVERIFIED`, not `PASS`",
            repair_candidate,
        )

    def test_status_consumer_gate_rejects_a_stale_active_document(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_minimal_status_consumers(root)
            (root / "README.md").write_text(
                "Current product status: **`REPAIR REQUIRED`**\n",
                encoding="utf-8",
            )
            report = Report()
            validate_current_status_consumers(root, report)
            self.assertTrue(report.errors)
            self.assertIn("README.md", report.errors[0])

    def test_status_consumer_gate_rejects_duplicate_authority_markers(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_minimal_status_consumers(root)
            ledger = root / "COURSE_1_AUDIT_STATUS_AND_REPAIR_LEDGER.md"
            ledger.write_text(
                ledger.read_text(encoding="utf-8")
                + "- Current status: **`PASS`**\n",
                encoding="utf-8",
            )
            report = Report()
            validate_current_status_consumers(root, report)
            self.assertTrue(report.errors)
            self.assertIn("exactly one exact", report.errors[0])


if __name__ == "__main__":
    unittest.main()
