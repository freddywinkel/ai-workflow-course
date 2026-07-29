from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from build_course1_ground_up_audit import (  # noqa: E402
    MACHINE_FILES,
    MARKDOWN_FILES,
    build,
    normalise_git_branch,
    raw_evidence,
    validate_raw_evidence_manifest,
    validate_machine_documents,
    validated_unique_ids,
)
from validate_package import iter_current_files  # noqa: E402


class GroundUpAuditArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory()
        cls.output = Path(cls.temporary.name) / "audit"
        build(ROOT, cls.output, "2026-07-29", None)
        cls.schema = json.loads(
            (
                ROOT
                / "audit_control/course1/ground_up_audit_artifact.schema.json"
            ).read_text(encoding="utf-8")
        )
        cls.validator = Draft202012Validator(cls.schema)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def read(self, name: str) -> dict:
        return json.loads((self.output / name).read_text(encoding="utf-8"))

    def test_detached_head_has_an_explicit_provenance_label(self) -> None:
        self.assertEqual(normalise_git_branch(""), "DETACHED_HEAD")
        self.assertEqual(
            normalise_git_branch("codex/course1-v2.6-repair"),
            "codex/course1-v2.6-repair",
        )

    def test_schema_is_valid_and_every_machine_artifact_matches(self) -> None:
        Draft202012Validator.check_schema(self.schema)
        for name in MACHINE_FILES:
            errors = list(self.validator.iter_errors(self.read(name)))
            self.assertEqual(errors, [], f"{name}: {errors}")

    def test_exact_required_fourteen_file_set_exists(self) -> None:
        actual = sorted(path.name for path in self.output.iterdir() if path.is_file())
        self.assertEqual(actual, sorted(MACHINE_FILES + MARKDOWN_FILES))

    def test_inventory_and_graph_counts_are_complete(self) -> None:
        inventory = self.read("normative-id-inventory.json")
        counts = {
            row["family"]: row["count"] for row in inventory["idFamilies"]
        }
        self.assertEqual(counts["TECHNICAL_REQUIREMENT"], 118)
        self.assertEqual(counts["TECHNICAL_TEST"], 33)
        self.assertEqual(counts["LEARNING_REQUIREMENT"], 17)
        self.assertEqual(counts["LEARNING_METHOD"], 17)
        self.assertEqual(counts["TECHNICAL_FINDING"], 6)
        self.assertEqual(counts["CONTENT_FINDING"], 9)
        self.assertEqual(counts["GOVERNANCE_FINDING"], 15)
        self.assertEqual(
            counts["TECHNICAL_FINDING"]
            + counts["CONTENT_FINDING"]
            + counts["GOVERNANCE_FINDING"],
            30,
        )
        self.assertEqual(counts["AUDIT_ASSURANCE"], 16)
        graph = self.read("requirement-test-evidence-graph.json")
        self.assertEqual(len(graph["technicalRequirements"]), 118)
        self.assertEqual(len(graph["technicalTests"]), 33)
        self.assertEqual(len(graph["learningRequirements"]), 17)
        self.assertEqual(graph["technicalEdgeCount"], 133)

    def test_missing_external_and_candidate_evidence_stays_unverified(self) -> None:
        baseline = self.read("baseline-file-inventory.json")
        change_map = self.read("change-to-evidence-map.json")
        self.assertEqual(
            baseline["git"]["dirty"],
            bool(change_map["changes"]),
        )
        self.assertEqual(baseline["status"], "UNVERIFIED")
        self.assertEqual(baseline["preRepairBaseline"]["status"], "UNVERIFIED")
        raw = self.read("raw-evidence-index.json")
        self.assertTrue(all(row["result"] == "UNVERIFIED" for row in raw["entries"]))
        self.assertTrue(all(not row["exists"] for row in raw["entries"]))
        assurance = self.read("audit-assurance-result.json")
        self.assertEqual(assurance["overallAuditStatus"], "UNVERIFIED")
        self.assertFalse(assurance["allMandatoryRulesPassed"])
        self.assertEqual(
            [row["id"] for row in assurance["rules"]],
            [f"C1-AA-{number:03d}" for number in range(1, 17)],
        )

    def test_schema_rejects_unknown_key_and_false_overall_pass(self) -> None:
        scope = self.read("scope-and-authority.json")
        scope["unknown"] = True
        self.assertTrue(list(self.validator.iter_errors(scope)))
        assurance = self.read("audit-assurance-result.json")
        assurance["overallAuditStatus"] = "PASS"
        self.assertTrue(list(self.validator.iter_errors(assurance)))

    def test_clean_change_map_accepts_zero_changes_and_stays_fail_closed(
        self,
    ) -> None:
        clean = self.read("change-to-evidence-map.json")
        clean["baseline"]["dirty"] = False
        clean["changes"] = []
        self.assertEqual(list(self.validator.iter_errors(clean)), [])

        dirty_without_changes = self.read("change-to-evidence-map.json")
        dirty_without_changes["baseline"]["dirty"] = True
        dirty_without_changes["changes"] = []
        self.assertTrue(list(self.validator.iter_errors(dirty_without_changes)))

        malformed = self.read("change-to-evidence-map.json")
        malformed["baseline"]["dirty"] = True
        malformed["changes"] = [
            {
                "path": "tools/example.py",
                "workingTreeStatus": "TRACKED_UNCHANGED",
                "classification": "COURSE1_ONLY",
                "invalidatedEvidenceFamilies": [],
                "rerunRequired": True,
                "unexpected": True,
            }
        ]
        self.assertTrue(list(self.validator.iter_errors(malformed)))

    def test_generator_gate_rejects_invalid_machine_document(self) -> None:
        documents = {name: self.read(name) for name in MACHINE_FILES}
        documents["audit-assurance-result.json"]["overallAuditStatus"] = "PASS"
        with self.assertRaisesRegex(ValueError, "closed-schema validation failed"):
            validate_machine_documents(self.schema, documents)

    def test_raw_input_manifest_has_a_closed_schema(self) -> None:
        input_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$ref": "#/$defs/rawEvidenceInputManifest",
            "$defs": self.schema["$defs"],
        }
        Draft202012Validator.check_schema(input_schema)
        validator = Draft202012Validator(input_schema)
        row = {
            "id": "C1-RAW-TOOLS",
            "path": "local-tools.log",
            "result": "PASS",
            "candidateBinding": "UNBOUND_WORKING_COPY",
            "candidateCommit": None,
            "commandOrProcedure": "python -m unittest",
            "environment": "local",
            "reviewer": "repair author",
            "recordedAt": "2026-07-29T12:00:00+02:00",
            "reason": "Local focused test only.",
        }
        valid = {
            "schemaVersion": "course1-ground-up-raw-input-v1",
            "entries": [row],
        }
        self.assertEqual(list(validator.iter_errors(valid)), [])
        widened = dict(valid)
        widened["unexpected"] = True
        self.assertTrue(list(validator.iter_errors(widened)))

    def test_generator_is_deterministic_for_unchanged_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first"
            second = Path(directory) / "second"
            build(ROOT, first, "2026-07-29", None)
            build(ROOT, second, "2026-07-29", None)
            for name in MACHINE_FILES + MARKDOWN_FILES:
                self.assertEqual(
                    (first / name).read_bytes(),
                    (second / name).read_bytes(),
                    name,
                )

    def test_dirty_copy_cannot_accept_claimed_immutable_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            raw = base / "tools.log"
            raw.write_text("local tools result\n", encoding="utf-8")
            baseline = self.read("baseline-file-inventory.json")
            manifest = base / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schemaVersion": "course1-ground-up-raw-input-v1",
                        "entries": [
                            {
                                "id": "C1-RAW-TOOLS",
                                "path": str(raw),
                                "result": "PASS",
                                "candidateBinding": "IMMUTABLE_CANDIDATE",
                                "candidateCommit": baseline["git"]["headCommit"],
                                "commandOrProcedure": "python -m unittest",
                                "environment": "local",
                                "reviewer": "repair author",
                                "recordedAt": "2026-07-29T12:00:00+02:00",
                                "reason": "Local focused test only.",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            output = base / "audit"
            evidence = raw_evidence(
                output,
                manifest,
                True,
                baseline["git"]["headCommit"],
                self.schema,
            )[0]
            self.assertTrue(evidence["exists"])
            self.assertEqual(evidence["result"], "UNVERIFIED")
            self.assertEqual(evidence["candidateBinding"], "UNBOUND_WORKING_COPY")

    def test_raw_manifest_rejects_duplicate_ids_before_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evidence.log"
            path.write_text("evidence\n", encoding="utf-8")
            row = {
                "id": "C1-RAW-TOOLS",
                "path": str(path),
                "result": "PASS",
                "candidateBinding": "UNBOUND_WORKING_COPY",
                "candidateCommit": None,
                "commandOrProcedure": "python -m unittest",
                "environment": "local",
                "reviewer": "repair author",
                "recordedAt": "2026-07-29T12:00:00+02:00",
                "reason": "Local focused test only.",
            }
            manifest = {
                "schemaVersion": "course1-ground-up-raw-input-v1",
                "entries": [row, dict(row)],
            }
            with self.assertRaisesRegex(ValueError, "duplicate raw evidence ID"):
                validate_raw_evidence_manifest(
                    manifest, Path(directory) / "manifest.json"
                )

    def test_raw_manifest_rejects_unknown_top_and_row_keys(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evidence.log"
            path.write_text("evidence\n", encoding="utf-8")
            row = {
                "id": "C1-RAW-TOOLS",
                "path": str(path),
                "result": "PASS",
                "candidateBinding": "UNBOUND_WORKING_COPY",
                "candidateCommit": None,
                "commandOrProcedure": "python -m unittest",
                "environment": "local",
                "reviewer": "repair author",
                "recordedAt": "2026-07-29T12:00:00+02:00",
                "reason": "Local focused test only.",
            }
            with self.assertRaisesRegex(ValueError, "keys must be exactly"):
                validate_raw_evidence_manifest(
                    {
                        "schemaVersion": "course1-ground-up-raw-input-v1",
                        "entries": [row],
                        "unexpected": True,
                    },
                    Path(directory) / "manifest.json",
                )
            widened = dict(row)
            widened["unexpected"] = True
            with self.assertRaisesRegex(ValueError, "keys must be exactly"):
                validate_raw_evidence_manifest(
                    {
                        "schemaVersion": "course1-ground-up-raw-input-v1",
                        "entries": [widened],
                    },
                    Path(directory) / "manifest.json",
                )

    def test_duplicate_threat_or_invariant_id_fails_before_deduplication(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicates=.*C1-INV-001"):
            validated_unique_ids(
                "C1-INV-001\nC1-INV-001\n",
                r"C1-INV(?:-[A-Z]+)?-[0-9]{3}",
                "INVARIANT",
            )

    def test_no_manifest_rerun_removes_generator_owned_stale_raw(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source = base / "tools.log"
            source.write_text("local tools result\n", encoding="utf-8")
            manifest = base / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schemaVersion": "course1-ground-up-raw-input-v1",
                        "entries": [
                            {
                                "id": "C1-RAW-TOOLS",
                                "path": str(source),
                                "result": "PASS",
                                "candidateBinding": "UNBOUND_WORKING_COPY",
                                "candidateCommit": None,
                                "commandOrProcedure": "python -m unittest",
                                "environment": "local",
                                "reviewer": "repair author",
                                "recordedAt": "2026-07-29T12:00:00+02:00",
                                "reason": "Local focused test only.",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            output = base / "audit"
            build(ROOT, output, "2026-07-29", manifest)
            self.assertTrue((output / "raw/c1-raw-tools.log").is_file())
            build(ROOT, output, "2026-07-29", None)
            self.assertFalse((output / "raw").exists())
            raw_index = json.loads(
                (output / "raw-evidence-index.json").read_text(encoding="utf-8")
            )
            tools = next(
                row for row in raw_index["entries"] if row["id"] == "C1-RAW-TOOLS"
            )
            self.assertFalse(tools["exists"])
            self.assertEqual(tools["result"], "UNVERIFIED")

    def test_generic_json_validation_ignores_only_generator_owned_raw_evidence(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            audit = (
                root
                / "release_evidence"
                / "course1_ground_up_audit"
                / "2.6.0"
                / "2026-07-29"
            )
            audit.mkdir(parents=True)
            machine = audit / "audit-assurance-result.json"
            machine.write_text("{}\n", encoding="utf-8")
            raw = audit / "raw"
            raw.mkdir()
            opaque = raw / "c1-raw-tools.json"
            opaque.write_text("not package JSON\n", encoding="utf-8")
            unrelated = root / "other" / "raw"
            unrelated.mkdir(parents=True)
            unrelated_json = unrelated / "current.json"
            unrelated_json.write_text("{}\n", encoding="utf-8")

            observed = {
                path.relative_to(root).as_posix()
                for path in iter_current_files(root, ".json")
            }

            self.assertIn(
                "release_evidence/course1_ground_up_audit/2.6.0/"
                "2026-07-29/audit-assurance-result.json",
                observed,
            )
            self.assertNotIn(
                "release_evidence/course1_ground_up_audit/2.6.0/"
                "2026-07-29/raw/c1-raw-tools.json",
                observed,
            )
            self.assertIn("other/raw/current.json", observed)


if __name__ == "__main__":
    unittest.main()
