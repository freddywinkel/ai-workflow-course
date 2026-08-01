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

from verify_course1_promotion import (  # noqa: E402
    DECLARED_TECHNICAL_TEST_IDS,
    EXPECTED_LEDGER_FINDING_IDS,
    PROMOTION_DEPENDENT_IDS,
    PROMOTION_REQUIRED_TEST_IDS,
    ROLLBACK_REQUIRED_TEST_IDS,
    read_object,
    resolve_record,
    validate,
    validate_ledger,
)
from verify_course1_final_acceptance import (  # noqa: E402
    FINAL_DECISION,
    FINAL_SCHEMA_VERSION,
    validate_final_record,
    validate_public_url,
)


LEDGER_HEADER = (
    "| ID | Severity | Requirement | Closure test and evidence | Status | Owner |\n"
    "|---|---|---|---|---|---|\n"
)


def ledger(
    *rows: tuple[str, str],
    product_status: str = "UNVERIFIED",
) -> str:
    configured: dict[str, str] = {}
    duplicates: list[tuple[str, str]] = []
    unknown: list[tuple[str, str]] = []
    for finding_id, status in rows:
        if finding_id not in EXPECTED_LEDGER_FINDING_IDS:
            unknown.append((finding_id, status))
        elif finding_id in configured:
            duplicates.append((finding_id, status))
        else:
            configured[finding_id] = status
    complete_rows = [
        (finding_id, configured.get(finding_id, "CLOSED"))
        for finding_id in sorted(EXPECTED_LEDGER_FINDING_IDS)
    ]
    complete_rows.extend(unknown)
    complete_rows.extend(duplicates)
    body = "\n".join(
        f"| `{finding_id}` | High | Requirement | Evidence | {status} | Owner |"
        for finding_id, status in complete_rows
    )
    return (
        f"- Current status: **`{product_status}`**\n\n"
        f"{LEDGER_HEADER}{body}\n"
    )


class PromotionLedgerTests(unittest.TestCase):
    def assert_failure_contains(self, failures: list[str], phrase: str) -> None:
        self.assertTrue(
            any(phrase in failure for failure in failures),
            failures,
        )

    def test_only_named_live_promotion_evidence_may_remain(self) -> None:
        text = ledger(
            ("C1-TECH-001", "CLOSED"),
            ("C1-GOV-002", "EVIDENCE PENDING"),
            ("C1-GOV-005", "EVIDENCE PENDING"),
            ("C1-GOV-006", "EVIDENCE PENDING"),
        )
        self.assertEqual(
            validate_ledger(
                text,
                ["C1-GOV-002", "C1-GOV-005", "C1-GOV-006"],
            ),
            [],
        )

    def test_non_promotion_evidence_pending_fails_closed(self) -> None:
        for finding_id in ("C1-CONT-001", "C1-TECH-006", "C1-GOV-007"):
            with self.subTest(finding_id=finding_id):
                failures = validate_ledger(
                    ledger(
                        (finding_id, "EVIDENCE PENDING"),
                        ("C1-GOV-002", "EVIDENCE PENDING"),
                    ),
                    ["C1-GOV-002"],
                )
                self.assert_failure_contains(
                    failures,
                    "non-promotion-dependent",
                )

    def test_open_partial_and_unknown_statuses_fail_closed(self) -> None:
        cases = (
            ("OPEN", "open or reopened"),
            ("REOPENED", "open or reopened"),
            ("PARTIAL", "partially implemented"),
            ("WAITING", "unsupported or missing status"),
        )
        for status, phrase in cases:
            with self.subTest(status=status):
                failures = validate_ledger(
                    ledger(("C1-TECH-001", status)),
                    [],
                )
                self.assert_failure_contains(failures, phrase)

    def test_authoritative_status_is_exact_and_unique(self) -> None:
        cases = (
            (
                "> - Current status: **`UNVERIFIED`**\n\n"
                + LEDGER_HEADER
                + "| `C1-TECH-001` | High | Requirement | Evidence | CLOSED | Owner |\n",
                "exactly one unquoted",
            ),
            (
                "- Current status: **`UNVERIFIED`**\n"
                "- Current status: **`UNVERIFIED`**\n\n"
                + LEDGER_HEADER
                + "| `C1-TECH-001` | High | Requirement | Evidence | CLOSED | Owner |\n",
                "exactly one unquoted",
            ),
            (
                ledger(("C1-TECH-001", "CLOSED"), product_status="READY"),
                "unsupported authoritative",
            ),
            (
                ledger(("C1-TECH-001", "CLOSED"), product_status="PASS"),
                "must be UNVERIFIED",
            ),
        )
        for text, phrase in cases:
            with self.subTest(phrase=phrase):
                self.assert_failure_contains(
                    validate_ledger(text, []),
                    phrase,
                )

        code_only = (
            "```\n"
            "- Current status: **`UNVERIFIED`**\n"
            "```\n\n"
            + LEDGER_HEADER
            + "| `C1-TECH-001` | High | Requirement | Evidence | CLOSED | Owner |\n"
        )
        self.assert_failure_contains(
            validate_ledger(code_only, []),
            "exactly one unquoted",
        )

        for prefix in ("- ", "* ", "1. ", "### ", "text "):
            with self.subTest(prefix=prefix):
                contradictory = (
                    ledger(("C1-TECH-001", "CLOSED"))
                    + f"\n{prefix}- Current status: **`PASS`**\n"
                )
                self.assert_failure_contains(
                    validate_ledger(contradictory, []),
                    "non-authoritative current-status text",
                )

    def test_duplicate_finding_ids_fail_closed(self) -> None:
        failures = validate_ledger(
            ledger(
                ("C1-TECH-001", "CLOSED"),
                ("C1-TECH-001", "CLOSED"),
            ),
            [],
        )
        self.assert_failure_contains(failures, "duplicate")

    def test_missing_or_unknown_finding_ids_fail_closed(self) -> None:
        missing = "\n".join(
            line
            for line in ledger().splitlines()
            if "`C1-GOV-015`" not in line
        )
        self.assert_failure_contains(
            validate_ledger(missing, []),
            "finding rows are missing",
        )
        self.assert_failure_contains(
            validate_ledger(
                ledger(("C1-GOV-999", "CLOSED")),
                [],
            ),
            "unknown finding IDs",
        )

    def test_malformed_and_undeclared_finding_ids_are_never_invisible(self) -> None:
        bad_ids = (
            "`C1-TECH-ABC`",
            "C1-TECH-001",
            "`C1-OPS-001`",
            "`C1-AUDIT-001`",
            "`C1-GOV-0001`",
        )
        for bad_id in bad_ids:
            with self.subTest(bad_id=bad_id):
                text = (
                    "- Current status: **`UNVERIFIED`**\n\n"
                    + LEDGER_HEADER
                    + f"| {bad_id} | High | Requirement | Evidence | CLOSED | Owner |\n"
                )
                self.assert_failure_contains(
                    validate_ledger(text, []),
                    "malformed or unsupported finding ID",
                )

    def test_unknown_severity_and_shifted_cells_fail_closed(self) -> None:
        texts = (
            (
                "- Current status: **`UNVERIFIED`**\n\n"
                + LEDGER_HEADER
                + "| `C1-TECH-001` | Critical | Requirement | Evidence | CLOSED | Owner |\n",
                "unsupported severity",
            ),
            (
                "- Current status: **`UNVERIFIED`**\n\n"
                + LEDGER_HEADER
                + "| `C1-TECH-001` | High | Requirement | Evidence | WAITING | CLOSED | Owner |\n",
                "expected 6",
            ),
            (
                "- Current status: **`UNVERIFIED`**\n\n"
                + LEDGER_HEADER
                + "| `C1-TECH-001` | High | Requirement | Evidence | WAITING | CLOSED |\n",
                "unsupported or missing status",
            ),
        )
        for text, phrase in texts:
            with self.subTest(phrase=phrase):
                self.assert_failure_contains(
                    validate_ledger(text, []),
                    phrase,
                )

    def test_finding_rows_outside_exact_tables_fail_closed(self) -> None:
        hidden_after_bad_header = (
            "- Current status: **`UNVERIFIED`**\n\n"
            + LEDGER_HEADER
            + "| `C1-TECH-001` | High | Requirement | Evidence | CLOSED | Owner |\n\n"
            + "| Identifier | Severity | Requirement | Closure test and evidence | Status | Owner |\n"
            + "|---|---|---|---|---|---|\n"
            + "| `C1-GOV-999` | High | Requirement | Evidence | OPEN | Owner |\n"
        )
        self.assert_failure_contains(
            validate_ledger(hidden_after_bad_header, []),
            "outside an exact authoritative table",
        )

        loose_row = (
            ledger(("C1-TECH-001", "CLOSED"))
            + "\n| `C1-GOV-999` | High | Requirement | Evidence | OPEN | Owner |\n"
        )
        self.assert_failure_contains(
            validate_ledger(loose_row, []),
            "outside an exact authoritative table",
        )

        quoted_row = (
            ledger(("C1-TECH-001", "CLOSED"))
            + "\n> | `C1-GOV-011` | High | Requirement | Evidence | OPEN | Owner |\n"
        )
        self.assert_failure_contains(
            validate_ledger(quoted_row, []),
            "quoted finding-like ledger row",
        )

        for prefix in ("- ", "1. ", "> - ", "### "):
            with self.subTest(prefix=prefix):
                disguised_row = (
                    ledger(("C1-TECH-001", "CLOSED"))
                    + f"\n{prefix}| `C1-GOV-011` | High | Requirement | "
                    "Evidence | OPEN | Owner |\n"
                )
                self.assert_failure_contains(
                    validate_ledger(disguised_row, []),
                    "outside an exact authoritative table",
                )

        for row_without_outer_pipes in (
            "`C1-GOV-011` | High | Requirement | Evidence | OPEN | Owner",
            "`C1-GOV-011` | High | Requirement | Evidence | OPEN | Owner |",
            "`C2-GOV-999` | High | Requirement | Evidence | OPEN | Owner",
            "`GOV-999` | High | Requirement | Evidence | OPEN | Owner",
            "Identifier | High | Requirement | Evidence | OPEN | Owner",
        ):
            with self.subTest(row=row_without_outer_pipes):
                self.assert_failure_contains(
                    validate_ledger(
                        ledger(("C1-TECH-001", "CLOSED"))
                        + f"\n{row_without_outer_pipes}\n",
                        [],
                    ),
                    "outside an exact authoritative table",
                )

    def test_recorded_promotion_ids_must_match_exactly(self) -> None:
        failures = validate_ledger(
            ledger(("C1-GOV-002", "EVIDENCE PENDING")),
            [],
        )
        self.assert_failure_contains(failures, "must exactly identify")
        failures = validate_ledger(
            ledger(("C1-GOV-002", "CLOSED")),
            ["C1-GOV-002"],
        )
        self.assert_failure_contains(failures, "must exactly identify")

    def test_promotion_template_ids_match_the_code_allowlist(self) -> None:
        template = json.loads(
            (
                ROOT
                / "release_evidence"
                / "templates"
                / "course1-promotion-acceptance.template.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            template["promotionDependentFindingIds"],
            sorted(PROMOTION_DEPENDENT_IDS),
        )
        self.assertEqual(template["candidate"]["artifactFormat"], "manifest-v1")
        self.assertEqual(
            set(template["evidence"][0]),
            {"path", "sha256"},
        )
        self.assertEqual(
            {Path(item["path"]).stem for item in template["evidence"]},
            PROMOTION_REQUIRED_TEST_IDS,
        )

        rollback_template = json.loads(
            (
                ROOT
                / "release_evidence"
                / "templates"
                / "course1-rollback-authorization.template.json"
            ).read_text(encoding="utf-8")
        )
        self.assertIn(
            "legacy-v2.5",
            rollback_template["candidate"]["artifactFormat"],
        )
        self.assertEqual(
            set(rollback_template["evidence"][0]),
            {"path", "sha256"},
        )
        self.assertEqual(
            set(
                rollback_template["rollback"][
                    "lastKnownGoodAcceptanceRecord"
                ]
            ),
            {"path", "sha256"},
        )
        self.assertEqual(
            {
                Path(item["path"]).stem
                for item in rollback_template["evidence"]
            },
            ROLLBACK_REQUIRED_TEST_IDS,
        )
        promotion_schema = json.loads(
            (
                ROOT
                / "audit_control"
                / "course1"
                / "promotion_record.schema.json"
            ).read_text(encoding="utf-8")
        )
        rollback_schema = json.loads(
            (
                ROOT
                / "audit_control"
                / "course1"
                / "rollback_record.schema.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            promotion_schema["properties"]["evidence"]["minItems"],
            len(PROMOTION_REQUIRED_TEST_IDS),
        )
        self.assertEqual(
            promotion_schema["properties"]["evidence"]["maxItems"],
            len(PROMOTION_REQUIRED_TEST_IDS),
        )
        self.assertEqual(
            rollback_schema["properties"]["evidence"]["minItems"],
            len(ROLLBACK_REQUIRED_TEST_IDS),
        )
        self.assertEqual(
            rollback_schema["properties"]["evidence"]["maxItems"],
            len(ROLLBACK_REQUIRED_TEST_IDS),
        )


class AcceptanceRecordTests(unittest.TestCase):
    EXPECTED_COMMIT = "a" * 40
    FAILED_COMMIT = "b" * 40
    CONTENT_HASH = "c" * 64
    ASSET_HASH = "d" * 64
    TREE_HASH = "e" * 64
    PUBLIC_SERVED_HASH = "f" * 64

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.evidence_root = Path(self.temporary.name)
        (self.evidence_root / "release_evidence").mkdir()
        self.version = {
            "courseVersion": "2.6.0",
            "buildId": "123456789abc",
            "contentHash": self.CONTENT_HASH,
            "commit": self.EXPECTED_COMMIT,
        }
        manifest = json.loads(
            (
                ROOT
                / "audit_control"
                / "course1"
                / "technical_test_manifest.json"
            ).read_text(encoding="utf-8")
        )
        self.test_definitions = {
            row["id"]: row for row in manifest["tests"]
        }
        self.evidence_classes = {
            test_id: row["evidenceClass"]
            for test_id, row in self.test_definitions.items()
        }

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def candidate(self) -> dict:
        return {
            "artifactFormat": "manifest-v1",
            "commit": self.EXPECTED_COMMIT,
            "courseVersion": "2.6.0",
            "buildId": "123456789abc",
            "contentHash": self.CONTENT_HASH,
            "assetManifestSha256": self.ASSET_HASH,
            "artifactTreeSha256": self.TREE_HASH,
        }

    def write_evidence(
        self,
        *,
        filename: str | None = None,
        evidence_id: str | None = None,
        test_id: str = "C1-TST-QUALITY-001",
        evidence_class: str | None = None,
        candidate_overrides: dict | None = None,
        raw_text: str | None = None,
    ) -> dict:
        if filename is None:
            filename = test_id.casefold().replace("c1-tst-", "technical-") + ".json"
        if evidence_id is None:
            evidence_id = test_id.replace("C1-TST-", "C1-EV-")
        path = self.evidence_root / "release_evidence" / filename
        candidate = {
            "commit": self.EXPECTED_COMMIT,
            "courseVersion": "2.6.0",
            "buildId": "123456789abc",
            "contentHash": self.CONTENT_HASH,
        }
        candidate.update(candidate_overrides or {})
        value = {
            "schemaVersion": "course1-technical-evidence-v1",
            "evidenceId": evidence_id,
            "testId": test_id,
            "candidate": candidate,
            "result": "PASS",
            "evidenceClass": (
                evidence_class
                if evidence_class is not None
                else self.evidence_classes[test_id]
            ),
            "recordedAt": "2026-07-29T01:00:00+02:00",
            "reviewer": {
                "name": "Independent reviewer",
                "independentOfImplementation": True,
            },
            "artifacts": [],
        }
        definition = self.test_definitions[test_id]
        procedures = [
            (procedure["locator"], procedure["selector"])
            for procedure in definition["procedures"]
        ]
        environments = definition["environments"]
        artifact_count = max(len(procedures), len(environments))
        artifact_directory = self.evidence_root / "release_evidence" / "artifacts"
        artifact_directory.mkdir(exist_ok=True)
        artifact_stem = Path(filename).stem
        for index in range(artifact_count):
            procedure_locator, procedure_selector = procedures[
                index % len(procedures)
            ]
            environment = environments[index % len(environments)]
            artifact_filename = f"{artifact_stem}-{index + 1}.log"
            artifact_path = artifact_directory / artifact_filename
            artifact_path.write_text(
                (
                    f"testId={test_id}\n"
                    f"result=PASS\n"
                    f"procedure={procedure_locator}#{procedure_selector}\n"
                    f"environment={environment}\n"
                ),
                encoding="utf-8",
            )
            value["artifacts"].append(
                {
                    "path": f"release_evidence/artifacts/{artifact_filename}",
                    "sha256": hashlib.sha256(
                        artifact_path.read_bytes()
                    ).hexdigest(),
                    "kind": "COMMAND_LOG",
                    "procedureLocator": procedure_locator,
                    "procedureSelector": procedure_selector,
                    "environment": environment,
                }
            )
        text = raw_text if raw_text is not None else json.dumps(value, indent=2)
        path.write_text(text, encoding="utf-8")
        return {
            "path": f"release_evidence/{filename}",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }

    def mutate_evidence(self, locator: dict, mutate) -> None:
        path = self.evidence_root / Path(*locator["path"].split("/"))
        value = json.loads(path.read_text(encoding="utf-8"))
        mutate(value)
        path.write_text(json.dumps(value, indent=2), encoding="utf-8")
        locator["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()

    def mutate_acceptance(self, locator: dict, mutate) -> None:
        path = self.evidence_root / Path(*locator["path"].split("/"))
        value = json.loads(path.read_text(encoding="utf-8"))
        mutate(value)
        path.write_text(json.dumps(value, indent=2), encoding="utf-8")
        locator["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()

    def record(
        self,
        operation: str = "promote",
        *,
        evidence_prefix: str = "",
    ) -> dict:
        required_test_ids = (
            PROMOTION_REQUIRED_TEST_IDS
            if operation == "promote"
            else ROLLBACK_REQUIRED_TEST_IDS
        )
        common = {
            "schemaVersion": 1,
            "decision": (
                "ACCEPTED_FOR_PROMOTION"
                if operation == "promote"
                else "ACCEPTED_FOR_ROLLBACK"
            ),
            "courseId": "course-1-controlled-ai-workflow-foundations",
            "candidate": self.candidate(),
            "acceptedAt": "2026-07-29T01:00:00+02:00",
            "evidence": [
                self.write_evidence(
                    test_id=test_id,
                    filename=(
                        (
                            f"{evidence_prefix}"
                            f"{test_id.casefold()}.json"
                        )
                        if evidence_prefix
                        else None
                    ),
                )
                for test_id in sorted(required_test_ids)
            ],
        }
        if operation == "promote":
            common.update(
                {
                    "reviewer": {
                        "name": "Promotion reviewer",
                        "independentOfImplementation": True,
                    },
                    "gates": {
                        "independentReview": True,
                        "manualSourceReview": True,
                        "packageValidation": True,
                        "pwaBrowserSmoke": True,
                        "pwaUnitTests": True,
                        "pwaUpdateSmoke": True,
                        "course1CleanRoomMatrix": True,
                        "sourceClaimsOnline": True,
                        "supplyChainOnline": True,
                    },
                    "promotionDependentFindingIds": [
                        "C1-GOV-002",
                        "C1-GOV-005",
                        "C1-GOV-006",
                    ],
                }
            )
        else:
            prior_record = self.record(
                "promote",
                evidence_prefix="prior-",
            )
            prior_path = (
                self.evidence_root / "release_evidence" / "last-pass.json"
            )
            prior_path.write_text(
                json.dumps(prior_record, indent=2),
                encoding="utf-8",
            )
            common.update(
                {
                    "authorizedBy": {"name": "Rollback owner"},
                    "gates": {
                        "artifactIdentity": True,
                        "lastKnownGoodAcceptance": True,
                        "learnerStateRecoveryPlan": True,
                        "rollbackAuthorized": True,
                    },
                    "rollback": {
                        "failedCandidateCommit": self.FAILED_COMMIT,
                        "trigger": "Blocking live failure",
                        "lastKnownGoodAcceptanceRecord": {
                            "path": "release_evidence/last-pass.json",
                            "sha256": hashlib.sha256(
                                prior_path.read_bytes()
                            ).hexdigest(),
                        },
                        "learnerStateRisk": "Preserve and verify local state",
                    },
                }
            )
        return common

    def final_record(self) -> dict:
        promotion_record = self.record("promote", evidence_prefix="promotion-")
        promotion_path = (
            self.evidence_root / "release_evidence" / "promotion-pass.json"
        )
        promotion_path.write_text(
            json.dumps(promotion_record, indent=2),
            encoding="utf-8",
        )
        evidence = [
            self.write_evidence(
                test_id=test_id,
                filename=f"final-{test_id.casefold()}.json",
            )
            for test_id in sorted(DECLARED_TECHNICAL_TEST_IDS)
        ]
        provenance = next(
            locator
            for locator in evidence
            if Path(locator["path"]).stem
            == "final-c1-tst-prov-001"
        )
        self.mutate_evidence(
            provenance,
            lambda value: value.update(
                {"recordedAt": "2026-07-29T01:30:00+02:00"}
            ),
        )
        return {
            "schemaVersion": FINAL_SCHEMA_VERSION,
            "decision": FINAL_DECISION,
            "courseId": "course-1-controlled-ai-workflow-foundations",
            "candidate": self.candidate(),
            "deployment": {
                "publicUrl": "https://example.github.io/ai-workflow-course/",
                "promotionWorkflowRunId": "123456789",
                "deploymentId": "pages-deployment-123",
                "deployedAt": "2026-07-29T01:15:00+02:00",
                "publicCommit": self.EXPECTED_COMMIT,
                "publicBuildId": "123456789abc",
                "publicContentHash": self.CONTENT_HASH,
                "publicAssetManifestSha256": self.ASSET_HASH,
                "publicServedTreeSha256": self.PUBLIC_SERVED_HASH,
                "nonPublicArtifactFiles": [".nojekyll"],
            },
            "adjudicatedAt": "2026-07-29T02:00:00+02:00",
            "reviewer": {
                "name": "Final independent reviewer",
                "independentOfImplementation": True,
            },
            "promotionAcceptanceRecord": {
                "path": "release_evidence/promotion-pass.json",
                "sha256": hashlib.sha256(
                    promotion_path.read_bytes()
                ).hexdigest(),
            },
            "promotionDependentFindingIds": [
                "C1-GOV-002",
                "C1-GOV-005",
                "C1-GOV-006",
            ],
            "evidence": evidence,
        }

    def run_validate(
        self,
        record: dict,
        *,
        operation: str = "promote",
        ledger_text: str | None = None,
    ) -> list[str]:
        return validate(
            record,
            self.version,
            expected_commit=self.EXPECTED_COMMIT,
            asset_manifest_sha256=self.ASSET_HASH,
            artifact_tree_sha256_value=self.TREE_HASH,
            ledger_text=ledger_text
            or (
                ledger(
                    ("C1-TECH-001", "CLOSED"),
                    ("C1-GOV-002", "EVIDENCE PENDING"),
                    ("C1-GOV-005", "EVIDENCE PENDING"),
                    ("C1-GOV-006", "EVIDENCE PENDING"),
                )
                if operation == "promote"
                else ledger(
                    ("C1-TECH-001", "CLOSED"),
                    product_status="REPAIR REQUIRED",
                )
            ),
            operation=operation,
            evidence_repository_root=self.evidence_root,
        )

    def run_final_validate(
        self,
        record: dict,
        *,
        ledger_text: str | None = None,
    ) -> list[str]:
        return validate_final_record(
            record,
            self.version,
            expected_commit=self.EXPECTED_COMMIT,
            expected_promotion_run_id="123456789",
            asset_manifest_sha256=self.ASSET_HASH,
            artifact_tree_sha256_value=self.TREE_HASH,
            public_served_tree_sha256_value=self.PUBLIC_SERVED_HASH,
            ledger_text=ledger_text
            or ledger(
                ("C1-GOV-002", "EVIDENCE PENDING"),
                ("C1-GOV-005", "EVIDENCE PENDING"),
                ("C1-GOV-006", "EVIDENCE PENDING"),
            ),
            evidence_repository_root=self.evidence_root,
        )

    def assert_failure_contains(self, failures: list[str], phrase: str) -> None:
        self.assertTrue(
            any(phrase in failure for failure in failures),
            failures,
        )

    def test_valid_closed_promotion_and_rollback_records_pass(self) -> None:
        self.assertEqual(self.run_validate(self.record()), [])
        self.assertEqual(
            self.run_validate(self.record("rollback"), operation="rollback"),
            [],
        )

    def test_unknown_keys_fail_at_every_acceptance_level(self) -> None:
        cases = (
            ("acceptance record", (), "silentlyTrusted"),
            ("candidate", ("candidate",), "silentlyTrusted"),
            ("reviewer", ("reviewer",), "silentlyTrusted"),
        )
        for label, route, key in cases:
            with self.subTest(label=label):
                record = self.record()
                target = record
                for part in route:
                    target = target[part]
                target[key] = True
                self.assert_failure_contains(
                    self.run_validate(record),
                    f"{label} has unknown keys",
                )

        record = self.record("rollback")
        record["authorizedBy"]["silentlyTrusted"] = True
        self.assert_failure_contains(
            self.run_validate(record, operation="rollback"),
            "authorizedBy has unknown keys",
        )
        record = self.record("rollback")
        record["rollback"]["silentlyTrusted"] = True
        self.assert_failure_contains(
            self.run_validate(record, operation="rollback"),
            "rollback has unknown keys",
        )

    def test_unknown_evidence_fields_and_test_ids_fail_closed(self) -> None:
        record = self.record()
        record["evidence"][0]["silentlyTrusted"] = True
        self.assert_failure_contains(
            self.run_validate(record),
            "evidence[0] has unknown keys",
        )

        record = self.record()
        self.mutate_evidence(
            record["evidence"][0],
            lambda value: value.update({"silentlyTrusted": True}),
        )
        self.assert_failure_contains(
            self.run_validate(record),
            "record has unknown keys",
        )

        record = self.record()
        self.mutate_evidence(
            record["evidence"][0],
            lambda value: value.update({"testId": "C1-TST-UNKNOWN-001"}),
        )
        self.assert_failure_contains(
            self.run_validate(record),
            "malformed or undeclared",
        )

        record = self.record()
        self.mutate_evidence(
            record["evidence"][0],
            lambda value: value.update({"evidenceClass": "POST_DEPLOY"}),
        )
        self.assert_failure_contains(
            self.run_validate(record),
            "does not match the declared test",
        )

    def test_verifier_test_allowlist_matches_the_graph(self) -> None:
        graph = json.loads(
            (
                ROOT
                / "audit_control"
                / "course1"
                / "technical_requirement_graph.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            DECLARED_TECHNICAL_TEST_IDS,
            {row["id"] for row in graph["tests"]},
        )
        evidence_schema = json.loads(
            (
                ROOT
                / "audit_control"
                / "course1"
                / "technical_evidence_record.schema.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            DECLARED_TECHNICAL_TEST_IDS,
            set(evidence_schema["properties"]["testId"]["enum"]),
        )

    def test_string_locator_missing_file_and_path_escape_fail_closed(self) -> None:
        record = self.record()
        record["evidence"] = ["release_evidence/anything.json"]
        self.assert_failure_contains(
            self.run_validate(record),
            "closed evidence objects",
        )

        record = self.record()
        record["evidence"][0]["path"] = "release_evidence/missing.json"
        self.assert_failure_contains(
            self.run_validate(record),
            "does not exist",
        )

        record = self.record()
        record["evidence"][0]["path"] = "release_evidence/../outside.json"
        self.assert_failure_contains(
            self.run_validate(record),
            "must not contain empty, dot, or parent segments",
        )

        record = self.record()
        record["evidence"][0]["path"] = "release_evidence//anything.json"
        self.assert_failure_contains(
            self.run_validate(record),
            "must not contain empty, dot, or parent segments",
        )

        with self.assertRaisesRegex(
            ValueError,
            "must not contain empty, dot, or parent segments",
        ):
            resolve_record(
                "release_evidence/../release_evidence/record.json",
                self.evidence_root,
            )

    def test_wrong_evidence_hash_or_candidate_fails_closed(self) -> None:
        record = self.record()
        record["evidence"][0]["sha256"] = "f" * 64
        self.assert_failure_contains(
            self.run_validate(record),
            "does not match the evidence file",
        )

        record = self.record()
        record["evidence"] = [
            self.write_evidence(candidate_overrides={"commit": self.FAILED_COMMIT})
        ]
        self.assert_failure_contains(
            self.run_validate(record),
            "does not match the acceptance candidate",
        )

    def test_evidence_requires_raw_artifacts_for_declared_procedures_and_environments(
        self,
    ) -> None:
        record = self.record()
        quality_locator = next(
            item
            for item in record["evidence"]
            if Path(item["path"]).stem == "technical-quality-001"
        )
        self.mutate_evidence(
            quality_locator,
            lambda value: (
                value.pop("artifacts"),
                value.update(
                    {
                        "commandOrProcedure": "x",
                        "environment": "x",
                    }
                ),
            ),
        )
        failures = self.run_validate(record)
        self.assert_failure_contains(failures, "record has unknown keys")
        self.assert_failure_contains(failures, "artifacts must be a non-empty")

        record = self.record()
        quality_locator = next(
            item
            for item in record["evidence"]
            if Path(item["path"]).stem == "technical-quality-001"
        )
        self.mutate_evidence(
            quality_locator,
            lambda value: value["artifacts"].pop(),
        )
        failures = self.run_validate(record)
        self.assert_failure_contains(
            failures,
            "missing declared procedure artifact coverage",
        )
        self.assert_failure_contains(
            failures,
            "missing declared environment artifact coverage",
        )

        record = self.record()
        quality_locator = next(
            item
            for item in record["evidence"]
            if Path(item["path"]).stem == "technical-quality-001"
        )
        self.mutate_evidence(
            quality_locator,
            lambda value: value["artifacts"][0].update(
                {"procedureSelector": "undeclared selector"}
            ),
        )
        failures = self.run_validate(record)
        self.assert_failure_contains(
            failures,
            "undeclared procedure artifact bindings",
        )
        self.assert_failure_contains(
            failures,
            "missing declared procedure artifact coverage",
        )

    def test_raw_artifact_path_hash_shape_and_uniqueness_fail_closed(
        self,
    ) -> None:
        record = self.record()
        locator = record["evidence"][0]
        evidence_path = self.evidence_root / Path(*locator["path"].split("/"))
        evidence_value = json.loads(evidence_path.read_text(encoding="utf-8"))
        artifact_path = self.evidence_root / Path(
            *evidence_value["artifacts"][0]["path"].split("/")
        )
        artifact_path.unlink()
        self.assert_failure_contains(
            self.run_validate(record),
            "artifact file does not exist",
        )

        record = self.record()
        locator = record["evidence"][0]
        self.mutate_evidence(
            locator,
            lambda value: value["artifacts"][0].update(
                {"sha256": "f" * 64}
            ),
        )
        self.assert_failure_contains(
            self.run_validate(record),
            "does not match the artifact file",
        )

        record = self.record()
        locator = record["evidence"][0]
        self.mutate_evidence(
            locator,
            lambda value: value["artifacts"].append(
                copy.deepcopy(value["artifacts"][0])
            ),
        )
        failures = self.run_validate(record)
        self.assert_failure_contains(failures, "duplicate artifact paths")
        self.assert_failure_contains(
            failures,
            "duplicate procedure/environment bindings",
        )

        record = self.record()
        locator = record["evidence"][0]
        evidence_path = self.evidence_root / Path(*locator["path"].split("/"))
        evidence_value = json.loads(evidence_path.read_text(encoding="utf-8"))
        artifact_path = self.evidence_root / Path(
            *evidence_value["artifacts"][0]["path"].split("/")
        )
        artifact_path.write_bytes(b"")
        evidence_value["artifacts"][0]["sha256"] = hashlib.sha256(b"").hexdigest()
        evidence_path.write_text(
            json.dumps(evidence_value, indent=2),
            encoding="utf-8",
        )
        locator["sha256"] = hashlib.sha256(
            evidence_path.read_bytes()
        ).hexdigest()
        self.assert_failure_contains(
            self.run_validate(record),
            "path is empty",
        )

        record = self.record()
        locator = record["evidence"][0]
        self.mutate_evidence(
            locator,
            lambda value: value["artifacts"][0].update(
                {"kind": "TRUST_ME"}
            ),
        )
        self.assert_failure_contains(
            self.run_validate(record),
            "kind is unsupported",
        )

    def test_evidence_must_precede_acceptance_and_independent_class_is_real(
        self,
    ) -> None:
        record = self.record()
        self.mutate_evidence(
            record["evidence"][0],
            lambda value: value.update(
                {"recordedAt": "2026-07-29T02:00:00+02:00"}
            ),
        )
        self.assert_failure_contains(
            self.run_validate(record),
            "after the acceptance decision",
        )

        record = self.record()
        oracle_locator = next(
            item
            for item in record["evidence"]
            if Path(item["path"]).stem == "technical-oracle-001"
        )
        self.mutate_evidence(
            oracle_locator,
            lambda value: value["reviewer"].update(
                {"independentOfImplementation": False}
            ),
        )
        self.assert_failure_contains(
            self.run_validate(record),
            "requires an independent reviewer",
        )

    def test_duplicate_evidence_path_and_id_fail_closed(self) -> None:
        record = self.record()
        record["evidence"].append(copy.deepcopy(record["evidence"][0]))
        self.assert_failure_contains(
            self.run_validate(record),
            "duplicate evidence paths",
        )
        self.assert_failure_contains(
            self.run_validate(record),
            "duplicate evidence IDs",
        )

        record = self.record()
        record["evidence"].append(
            self.write_evidence(
                filename="second.json",
                evidence_id="C1-EV-QUALITY-001",
            )
        )
        self.assert_failure_contains(
            self.run_validate(record),
            "duplicate evidence IDs",
        )

    def test_duplicate_json_keys_are_rejected_for_records_and_evidence(self) -> None:
        record_path = self.evidence_root / "release_evidence" / "record.json"
        record_path.write_text('{"schemaVersion": 1, "schemaVersion": 2}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            read_object(record_path)

        locator = self.write_evidence(
            filename="duplicate-key-evidence.json",
            raw_text=(
                '{"schemaVersion":"course1-technical-evidence-v1",'
                '"schemaVersion":"shadowed"}'
            )
        )
        record = self.record()
        record["evidence"] = [locator]
        self.assert_failure_contains(
            self.run_validate(record),
            "duplicate JSON key",
        )

    def test_rollback_requires_one_exact_authoritative_status(self) -> None:
        record = self.record("rollback")
        quoted_only = (
            "> - Current status: **`REPAIR REQUIRED`**\n\n"
            + LEDGER_HEADER
            + "| `C1-TECH-001` | High | Requirement | Evidence | CLOSED | Owner |\n"
        )
        self.assert_failure_contains(
            self.run_validate(
                record,
                operation="rollback",
                ledger_text=quoted_only,
            ),
            "exactly one unquoted",
        )

        historical_substring = (
            "Historical Current status: **`REPAIR REQUIRED`**\n"
            + ledger(
                ("C1-TECH-001", "CLOSED"),
                product_status="PASS",
            )
        )
        self.assert_failure_contains(
            self.run_validate(
                record,
                operation="rollback",
                ledger_text=historical_substring,
            ),
            "rollback requires an authoritative",
        )

    def test_rollback_last_known_good_acceptance_is_hash_and_candidate_bound(
        self,
    ) -> None:
        record = self.record("rollback")
        record["rollback"]["lastKnownGoodAcceptanceRecord"]["path"] = (
            "release_evidence/missing.json"
        )
        self.assert_failure_contains(
            self.run_validate(record, operation="rollback"),
            "does not exist",
        )

        record = self.record("rollback")
        record["rollback"]["lastKnownGoodAcceptanceRecord"]["sha256"] = "f" * 64
        self.assert_failure_contains(
            self.run_validate(record, operation="rollback"),
            "does not match the acceptance file",
        )

        mutations = (
            (
                "unknown top-level key",
                lambda value: value.update({"silentlyTrusted": True}),
                "record has unknown keys",
            ),
            (
                "wrong decision",
                lambda value: value.update({"decision": "LOOKS_GOOD"}),
                "decision must be ACCEPTED_FOR_PROMOTION",
            ),
            (
                "wrong candidate",
                lambda value: value["candidate"].update(
                    {"commit": self.FAILED_COMMIT}
                ),
                "does not exactly match the rollback target",
            ),
            (
                "non-independent reviewer",
                lambda value: value["reviewer"].update(
                    {"independentOfImplementation": False}
                ),
                "must be true",
            ),
            (
                "future acceptance",
                lambda value: value.update(
                    {"acceptedAt": "2026-07-29T02:00:00+02:00"}
                ),
                "after the rollback authorization",
            ),
        )
        for label, mutate, phrase in mutations:
            with self.subTest(label=label):
                record = self.record("rollback")
                locator = record["rollback"][
                    "lastKnownGoodAcceptanceRecord"
                ]
                self.mutate_acceptance(locator, mutate)
                self.assert_failure_contains(
                    self.run_validate(record, operation="rollback"),
                    phrase,
                )

    def test_final_adjudication_requires_the_exact_all_33_evidence_set(
        self,
    ) -> None:
        record = self.final_record()
        self.assertEqual(self.run_final_validate(record), [])
        self.assertEqual(
            {Path(item["path"]).stem.removeprefix("final-") for item in record["evidence"]},
            {test_id.casefold() for test_id in DECLARED_TECHNICAL_TEST_IDS},
        )

        record = self.final_record()
        record["evidence"] = [
            item
            for item in record["evidence"]
            if "c1-tst-prov-001" not in item["path"]
        ]
        failures = self.run_final_validate(record)
        self.assert_failure_contains(failures, "required technical test evidence is missing")
        self.assert_failure_contains(
            failures,
            "exactly one C1-TST-PROV-001",
        )

    def test_final_adjudication_rejects_predeployment_provenance(self) -> None:
        record = self.final_record()
        provenance = next(
            item
            for item in record["evidence"]
            if "c1-tst-prov-001" in item["path"]
        )
        self.mutate_evidence(
            provenance,
            lambda value: value.update(
                {"recordedAt": "2026-07-29T01:14:59+02:00"}
            ),
        )
        self.assert_failure_contains(
            self.run_final_validate(record),
            "at or after deployment",
        )

    def test_final_adjudication_rejects_public_identity_drift(self) -> None:
        record = self.final_record()
        record["deployment"]["publicContentHash"] = "f" * 64
        self.assert_failure_contains(
            self.run_final_validate(record),
            "publicContentHash does not match",
        )

        record = self.final_record()
        record["deployment"]["publicServedTreeSha256"] = "0" * 64
        self.assert_failure_contains(
            self.run_final_validate(record),
            "publicServedTreeSha256 does not match",
        )

        record = self.final_record()
        record["deployment"]["nonPublicArtifactFiles"] = []
        self.assert_failure_contains(
            self.run_final_validate(record),
            "must exactly record .nojekyll",
        )

    def test_final_adjudication_binds_the_publication_run_id(self) -> None:
        record = self.final_record()
        record["deployment"]["promotionWorkflowRunId"] = "987654321"
        self.assert_failure_contains(
            self.run_final_validate(record),
            "does not match the verified workflow run",
        )

    def test_final_adjudication_rejects_unsafe_or_wrong_scope_url(self) -> None:
        for url in (
            "http://example.github.io/ai-workflow-course/",
            "https://localhost/ai-workflow-course/",
            "https://example.github.io/other/",
            "https://user@example.github.io/ai-workflow-course/",
            "https://example.github.io/ai-workflow-course/?trust=true",
        ):
            with self.subTest(url=url):
                self.assertTrue(validate_public_url(url))

    def test_final_adjudication_rechecks_the_promotion_record(self) -> None:
        record = self.final_record()
        record["promotionAcceptanceRecord"]["sha256"] = "f" * 64
        failures = self.run_final_validate(record)
        self.assert_failure_contains(
            failures,
            "does not match the acceptance file",
        )

    def test_final_schema_and_template_freeze_the_exact_inventory(self) -> None:
        schema = json.loads(
            (
                ROOT
                / "audit_control"
                / "course1"
                / "final_acceptance_record.schema.json"
            ).read_text(encoding="utf-8")
        )
        template = json.loads(
            (
                ROOT
                / "release_evidence"
                / "templates"
                / "course1-final-technical-acceptance.template.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            schema["properties"]["evidence"]["minItems"],
            len(DECLARED_TECHNICAL_TEST_IDS),
        )
        self.assertEqual(
            schema["properties"]["evidence"]["maxItems"],
            len(DECLARED_TECHNICAL_TEST_IDS),
        )
        self.assertEqual(
            {Path(item["path"]).stem for item in template["evidence"]},
            DECLARED_TECHNICAL_TEST_IDS,
        )
        self.assertEqual(
            template["deployment"]["nonPublicArtifactFiles"],
            [".nojekyll"],
        )
        self.assertEqual(template["decision"], FINAL_DECISION)

        workflow = (
            ROOT / ".github" / "workflows" / "course1-final-adjudication.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("permissions:\n  actions: read\n  contents: read", workflow)
        self.assertIn("ref: ${{ github.sha }}", workflow)
        self.assertNotIn("ref: main", workflow)
        self.assertIn('CONTROL_REF: ${{ github.ref }}', workflow)
        self.assertIn("final adjudication must be dispatched from main", workflow)
        self.assertIn("run-id: ${{ inputs.promotion_run_id }}", workflow)
        self.assertIn("actions/runs/$PROMOTION_RUN_ID", workflow)
        self.assertIn('.head_branch == "main"', workflow)
        self.assertIn("prepare-accepted-pages-artifact deploy", workflow)
        self.assertIn("verify_course1_final_acceptance.py", workflow)
        self.assertIn('--promotion-run-id "$PROMOTION_RUN_ID"', workflow)
        self.assertIn("--evidence-root acceptance-control", workflow)
        self.assertNotIn("actions/deploy-pages@", workflow)


if __name__ == "__main__":
    unittest.main()
