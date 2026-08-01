from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from validate_package import (  # noqa: E402
    load_json_object,
    technical_audit_control_failures,
    validate_technical_evidence_record,
)


class TechnicalAuditControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = (
            ROOT / "COURSE_1_TECHNICAL_ACCEPTANCE_CONTRACT.md"
        ).read_text(encoding="utf-8")
        cls.graph = load_json_object(
            ROOT / "audit_control/course1/technical_requirement_graph.json"
        )
        cls.manifest = load_json_object(
            ROOT / "audit_control/course1/technical_test_manifest.json"
        )

    def failures(
        self,
        *,
        contract: str | None = None,
        graph: dict | None = None,
        manifest: dict | None = None,
    ) -> list[str]:
        return technical_audit_control_failures(
            ROOT,
            contract_text=self.contract if contract is None else contract,
            graph=copy.deepcopy(self.graph) if graph is None else graph,
            manifest=copy.deepcopy(self.manifest) if manifest is None else manifest,
        )

    def assert_failure_contains(self, failures: list[str], phrase: str) -> None:
        self.assertTrue(
            any(phrase in failure for failure in failures),
            failures,
        )

    def test_current_graph_is_exact_and_honestly_unverified(self) -> None:
        self.assertEqual(self.failures(), [])
        self.assertEqual(len(self.graph["requirements"]), 118)
        self.assertEqual(len(self.graph["tests"]), 33)
        self.assertTrue(
            all(
                row["currentEvidence"] == {
                    "status": "UNVERIFIED",
                    "records": [],
                }
                for row in self.manifest["tests"]
            )
        )

    def test_missing_requirement_fails_closed(self) -> None:
        graph = copy.deepcopy(self.graph)
        graph["requirements"].pop()
        failures = self.failures(graph=graph)
        self.assert_failure_contains(failures, "118-ID contract")

    def test_duplicate_requirement_fails_closed(self) -> None:
        graph = copy.deepcopy(self.graph)
        graph["requirements"].append(copy.deepcopy(graph["requirements"][0]))
        failures = self.failures(graph=graph)
        self.assert_failure_contains(failures, "duplicate requirement IDs")

    def test_unknown_or_orphan_test_fails_closed(self) -> None:
        graph = copy.deepcopy(self.graph)
        graph["tests"].append(
            {
                "id": "C1-TST-UNKNOWN-001",
                "requirements": ["C1-TA-DATA-001"],
            }
        )
        failures = self.failures(graph=graph)
        self.assert_failure_contains(failures, "33-ID contract")
        self.assert_failure_contains(
            failures,
            "requirement-to-test and test-to-requirement mappings disagree",
        )

    def test_reverse_mapping_contradiction_fails_closed(self) -> None:
        graph = copy.deepcopy(self.graph)
        graph["tests"][0]["requirements"].remove("C1-TA-DATA-004")
        failures = self.failures(graph=graph)
        self.assert_failure_contains(
            failures,
            "requirement-to-test and test-to-requirement mappings disagree",
        )

    def test_direct_contract_reference_contradiction_fails_closed(self) -> None:
        contract = self.contract.replace(
            "| `C1-TA-FS-001` | Before a read",
            "| `C1-TA-FS-001` | Before a read",
            1,
        ).replace(
            "`C1-TST-FS-001`; Windows native containment tests",
            "`C1-TST-FS-002`; Windows native containment tests",
            1,
        )
        failures = self.failures(contract=contract)
        self.assert_failure_contains(
            failures,
            "direct test references contradict the graph",
        )

    def test_malformed_or_unbackticked_contract_id_fails_closed(self) -> None:
        contract = self.contract.replace(
            "| `C1-TA-FS-001` |",
            "| C1-TA-FS-001 |",
            1,
        )
        failures = self.failures(contract=contract)
        self.assert_failure_contains(failures, "malformed requirement ID")

        contract = self.contract.replace(
            "| `C1-TST-FS-001` |",
            "| `C1-CHECK-FS-001` |",
            1,
        )
        failures = self.failures(contract=contract)
        self.assert_failure_contains(failures, "unsupported ID family")

    def test_missing_procedure_locator_or_selector_fails_closed(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["tests"][0]["procedures"][0][
            "locator"
        ] = "audit_control/course1/does-not-exist.md"
        failures = self.failures(manifest=manifest)
        self.assert_failure_contains(failures, "does not exist")

        manifest = copy.deepcopy(self.manifest)
        manifest["tests"][0]["procedures"][0][
            "selector"
        ] = "not a real selector"
        failures = self.failures(manifest=manifest)
        self.assert_failure_contains(failures, "selector is absent")

    def test_unknown_manifest_key_fails_closed(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["tests"][0]["silentlyTrusted"] = True
        failures = self.failures(manifest=manifest)
        self.assert_failure_contains(failures, "unknown keys")

    def test_unverified_test_cannot_claim_an_evidence_locator(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["tests"][0]["currentEvidence"]["records"] = [
            {
                "path": "release_evidence/fake.json",
                "sha256": "a" * 64,
            }
        ]
        failures = self.failures(manifest=manifest)
        self.assert_failure_contains(
            failures,
            "UNVERIFIED evidence must have no records",
        )
        self.assert_failure_contains(failures, "does not exist")

    def test_duplicate_json_keys_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.json"
            path.write_text('{"id": 1, "id": 2}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                load_json_object(path)

    def test_package_evidence_parser_requires_hash_bound_raw_coverage(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence_root = root / "release_evidence"
            evidence_root.mkdir()
            evidence_path = evidence_root / "evidence.json"
            procedures = {
                ("tools/one.py", "test_one"),
                ("manual.md", "## manual"),
            }
            environments = {"python", "native Windows"}
            artifacts = []
            for index, ((locator, selector), environment) in enumerate(
                zip(sorted(procedures), sorted(environments)),
                1,
            ):
                raw_path = evidence_root / f"raw-{index}.log"
                raw_path.write_text(
                    f"result=PASS\n{locator}\n{selector}\n{environment}\n",
                    encoding="utf-8",
                )
                artifacts.append(
                    {
                        "path": f"release_evidence/raw-{index}.log",
                        "sha256": hashlib.sha256(
                            raw_path.read_bytes()
                        ).hexdigest(),
                        "kind": "COMMAND_LOG",
                        "procedureLocator": locator,
                        "procedureSelector": selector,
                        "environment": environment,
                    }
                )
            record = {
                "schemaVersion": "course1-technical-evidence-v1",
                "evidenceId": "C1-EV-DATA-001",
                "testId": "C1-TST-DATA-001",
                "candidate": {
                    "commit": "a" * 40,
                    "courseVersion": "2.6.0",
                    "buildId": "b" * 12,
                    "contentHash": "c" * 64,
                },
                "result": "PASS",
                "evidenceClass": "NATIVE_WINDOWS",
                "recordedAt": "2026-07-29T01:00:00+02:00",
                "reviewer": {
                    "name": "Reviewer",
                    "independentOfImplementation": True,
                },
                "artifacts": artifacts,
            }
            evidence_path.write_text(
                json.dumps(record, indent=2),
                encoding="utf-8",
            )
            failures: list[str] = []
            validate_technical_evidence_record(
                record,
                root=root,
                evidence_record_path=evidence_path,
                label="evidence",
                expected_test_id="C1-TST-DATA-001",
                expected_evidence_class="NATIVE_WINDOWS",
                expected_result="PASS",
                expected_procedures=procedures,
                expected_environments=environments,
                failures=failures,
            )
            self.assertEqual(failures, [])

            summary_only = copy.deepcopy(record)
            summary_only.pop("artifacts")
            summary_only["commandOrProcedure"] = "x"
            summary_only["environment"] = "x"
            failures = []
            validate_technical_evidence_record(
                summary_only,
                root=root,
                evidence_record_path=evidence_path,
                label="evidence",
                expected_test_id="C1-TST-DATA-001",
                expected_evidence_class="NATIVE_WINDOWS",
                expected_result="PASS",
                expected_procedures=procedures,
                expected_environments=environments,
                failures=failures,
            )
            self.assert_failure_contains(failures, "unknown keys")
            self.assert_failure_contains(
                failures,
                "artifacts must be a non-empty",
            )


if __name__ == "__main__":
    unittest.main()
