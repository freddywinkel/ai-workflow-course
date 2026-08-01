from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import verify_course1_promotion as promotion_verifier  # noqa: E402
from verify_course1_promotion import (  # noqa: E402
    LEGACY_V25_ARTIFACT_FORMAT,
    LEGACY_V25_BUILD_ID,
    LEGACY_V25_COMMIT,
    LEGACY_V25_CONTENT_HASH,
    LEGACY_V25_TREE_SHA256,
    EXPECTED_LEDGER_FINDING_IDS,
    MANIFEST_ARTIFACT_FORMAT,
    MANIFEST_ASSET_PATHS,
    inspect_artifact_identity,
    validate,
)


def write_manifest_v1_artifact(root: Path, commit: str) -> None:
    root.mkdir(parents=True, exist_ok=True)
    version = {
        "buildId": "123456789abc",
        "bundleSchemaVersion": 2,
        "programId": "controlled-ai-workflow-consultant-path",
        "courseId": "course-1-controlled-ai-workflow-foundations",
        "courseVersion": "2.6.0",
        "productStatus": "UNVERIFIED",
        "distributionPurpose": "accepted-release-candidate",
        "sourceVerifiedThrough": "2026-07-28",
        "contentRevisionThrough": "2026-07-29",
        "verifiedThrough": "2026-07-28",
        "contentHash": "c" * 64,
        "commit": commit,
    }
    for relative_path in MANIFEST_ASSET_PATHS:
        path = root / Path(*relative_path.split("/"))
        path.parent.mkdir(parents=True, exist_ok=True)
        body = (
            f"{json.dumps(version, indent=2)}\n".encode()
            if relative_path == "version.json"
            else f"synthetic {relative_path}\n".encode()
        )
        path.write_bytes(body)

    assets = {}
    for relative_path in sorted(MANIFEST_ASSET_PATHS):
        path = root / Path(*relative_path.split("/"))
        assets[relative_path] = {
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "contentType": "application/octet-stream",
        }
    manifest = {
        "schemaVersion": 1,
        "buildId": version["buildId"],
        "contentHash": version["contentHash"],
        "provenance": {"commit": commit},
        "assets": assets,
    }
    manifest_text = f"{json.dumps(manifest, indent=2)}\n"
    (root / "asset-manifest.json").write_bytes(manifest_text.encode())
    manifest_hash = hashlib.sha256(manifest_text.encode()).hexdigest()
    (root / "sw.js").write_text(
        f'const BUILD_PROVENANCE = "{commit}";\n'
        f'const ASSET_MANIFEST_SHA256 = "{manifest_hash}";\n',
        encoding="utf-8",
    )
    (root / ".nojekyll").write_bytes(b"")


class ArtifactIdentityTests(unittest.TestCase):
    def test_public_served_tree_excludes_only_the_nojekyll_control(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            commit = "9" * 40
            write_manifest_v1_artifact(root, commit)
            self.assertEqual(len(promotion_verifier.PUBLIC_SERVED_PATHS), 16)
            full_before = promotion_verifier.artifact_tree_sha256(root)
            public_before = promotion_verifier.selected_tree_sha256(
                root,
                promotion_verifier.PUBLIC_SERVED_PATHS,
            )

            (root / ".nojekyll").write_bytes(b"deployment control changed\n")
            self.assertNotEqual(
                promotion_verifier.artifact_tree_sha256(root),
                full_before,
            )
            self.assertEqual(
                promotion_verifier.selected_tree_sha256(
                    root,
                    promotion_verifier.PUBLIC_SERVED_PATHS,
                ),
                public_before,
            )

            (root / "app.js").write_bytes(b"served asset changed\n")
            self.assertNotEqual(
                promotion_verifier.selected_tree_sha256(
                    root,
                    promotion_verifier.PUBLIC_SERVED_PATHS,
                ),
                public_before,
            )

    def test_promotion_requires_separated_version_dates(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            commit = "a" * 40
            write_manifest_v1_artifact(root, commit)
            version_path = root / "version.json"
            version = json.loads(version_path.read_text(encoding="utf-8"))
            del version["sourceVerifiedThrough"]
            del version["contentRevisionThrough"]
            del version["productStatus"]
            del version["distributionPurpose"]
            version_path.write_text(
                f"{json.dumps(version, indent=2)}\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                ValueError,
                "promote version.json must contain separated",
            ):
                inspect_artifact_identity(
                    root,
                    expected_commit=commit,
                    operation="promote",
                )

    def test_promotion_rejects_contradictory_date_alias(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            commit = "a" * 40
            write_manifest_v1_artifact(root, commit)
            version_path = root / "version.json"
            version = json.loads(version_path.read_text(encoding="utf-8"))
            version["verifiedThrough"] = "2026-07-29"
            version_path.write_text(
                f"{json.dumps(version, indent=2)}\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                ValueError,
                "separated date metadata is malformed or contradictory",
            ):
                inspect_artifact_identity(
                    root,
                    expected_commit=commit,
                    operation="promote",
                )

    def test_release_workflows_select_candidate_mode_and_retain_legacy_history(
        self,
    ) -> None:
        pages = (ROOT / ".github" / "workflows" / "pages.yml").read_text(
            encoding="utf-8"
        )
        rollback = (
            ROOT / ".github" / "workflows" / "course1-rollback.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("COURSE1_BUILD_MODE: candidate", pages)
        self.assertIn("fetch-depth: 0", pages)
        self.assertIn("COURSE1_BUILD_MODE=candidate", rollback)
        self.assertIn('GITHUB_SHA="$LAST_KNOWN_GOOD_COMMIT"', rollback)
        self.assertIn("fetch-depth: 0", rollback)
        self.assertIn(
            "if [[ -f dist/asset-manifest.json ]]; then",
            rollback,
        )

    def test_personal_study_workflow_is_manual_main_only_and_exact_artifact(
        self,
    ) -> None:
        pages = (ROOT / ".github" / "workflows" / "pages.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("          - personal-study", pages)
        self.assertIn("study_boundary_acknowledgement:", pages)
        self.assertIn("UNVERIFIED-SYNTHETIC-STUDY-ONLY", pages)
        self.assertIn(
            'course1-pages-${{ (inputs.mode == \'promote\' || inputs.mode == \'personal-study\')',
            pages,
        )

        prepare = pages.split("  prepare-personal-study-pages-artifact:", 1)[1]
        prepare = prepare.split("\n  deploy-personal-study:", 1)[0]
        for required in (
            "github.event_name == 'workflow_dispatch'",
            "inputs.mode == 'personal-study'",
            "github.ref == 'refs/heads/main'",
            "- validate-and-build",
            "- test-course1-offline",
            "- audit-course1-supply-and-sources",
            "- test-course1-quality-controls",
            'if [[ "$ACCEPTED_COMMIT" != "$WORKFLOW_COMMIT" ]]',
            "name: course1-candidate-${{ github.sha }}",
            "python tools/verify_course1_study_release.py",
            "uses: actions/upload-pages-artifact@",
            "path: app/dist",
            "if-no-files-found: error",
        ):
            self.assertIn(required, prepare)
        self.assertNotIn("npm run build", prepare)
        self.assertNotIn("node scripts/build.mjs", prepare)

        deploy = pages.split("  deploy-personal-study:", 1)[1]
        deploy = deploy.split("\n  verify-personal-study-live:", 1)[0]
        self.assertIn("github.ref == 'refs/heads/main'", deploy)
        self.assertIn("name: github-pages", deploy)
        self.assertIn("uses: actions/deploy-pages@", deploy)
        self.assertNotIn("npm run build", deploy)

        live = pages.split("  verify-personal-study-live:", 1)[1]
        live = live.split("\n  prepare-accepted-pages-artifact:", 1)[0]
        self.assertIn("github.ref == 'refs/heads/main'", live)
        self.assertIn("- deploy-personal-study", live)
        self.assertIn("name: course1-candidate-${{ github.sha }}", live)
        self.assertIn(
            "PUBLIC_URL: ${{ needs.deploy-personal-study.outputs.page_url }}",
            live,
        )
        self.assertIn("ACCEPTED_COMMIT: ${{ inputs.accepted_commit }}", live)
        self.assertIn("verify_course1_public_artifact.py", live)
        self.assertIn("if-no-files-found: error", live)

    def test_manifest_v1_requires_and_returns_one_full_commit(self) -> None:
        commit = "a" * 40
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_manifest_v1_artifact(root, commit)
            identity = inspect_artifact_identity(
                root,
                expected_commit=commit,
                operation="promote",
            )
            self.assertEqual(identity["artifactFormat"], MANIFEST_ARTIFACT_FORMAT)
            self.assertEqual(identity["version"]["commit"], commit)
            self.assertRegex(identity["assetManifestSha256"], r"^[0-9a-f]{64}$")
            self.assertRegex(identity["artifactTreeSha256"], r"^[0-9a-f]{64}$")
            self.assertRegex(
                identity["publicServedTreeSha256"],
                r"^[0-9a-f]{64}$",
            )

    def test_personal_study_requires_its_distinct_distribution_purpose(self) -> None:
        commit = "d" * 40
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_manifest_v1_artifact(root, commit)
            version_path = root / "version.json"
            version = json.loads(version_path.read_text(encoding="utf-8"))
            version["distributionPurpose"] = "personal-synthetic-study"
            version_path.write_text(
                f"{json.dumps(version, indent=2)}\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "manifest asset hash"):
                inspect_artifact_identity(
                    root,
                    expected_commit=commit,
                    operation="personal-study",
                )

            write_manifest_v1_artifact(root, commit)
            version = json.loads(version_path.read_text(encoding="utf-8"))
            version["distributionPurpose"] = "personal-synthetic-study"
            version_path.write_text(
                f"{json.dumps(version, indent=2)}\n",
                encoding="utf-8",
            )
            assets = json.loads(
                (root / "asset-manifest.json").read_text(encoding="utf-8")
            )
            assets["assets"]["version.json"]["sha256"] = hashlib.sha256(
                version_path.read_bytes()
            ).hexdigest()
            manifest_text = f"{json.dumps(assets, indent=2)}\n"
            (root / "asset-manifest.json").write_bytes(
                manifest_text.encode("utf-8")
            )
            manifest_hash = hashlib.sha256(manifest_text.encode()).hexdigest()
            (root / "sw.js").write_text(
                f'const BUILD_PROVENANCE = "{commit}";\n'
                f'const ASSET_MANIFEST_SHA256 = "{manifest_hash}";\n',
                encoding="utf-8",
            )
            identity = inspect_artifact_identity(
                root,
                expected_commit=commit,
                operation="personal-study",
            )
            self.assertEqual(
                identity["version"]["distributionPurpose"],
                "personal-synthetic-study",
            )
            with self.assertRaisesRegex(ValueError, "accepted-release-candidate"):
                inspect_artifact_identity(
                    root,
                    expected_commit=commit,
                    operation="promote",
                )

    def test_manifest_v1_rejects_a_short_version_commit(self) -> None:
        commit = "b" * 40
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_manifest_v1_artifact(root, commit)
            version_path = root / "version.json"
            version = json.loads(version_path.read_text(encoding="utf-8"))
            version["commit"] = commit[:12]
            version_path.write_text(
                f"{json.dumps(version, indent=2)}\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "full 40-character"):
                inspect_artifact_identity(
                    root,
                    expected_commit=commit,
                    operation="promote",
                )

    def test_artifact_without_manifest_is_never_promotable(self) -> None:
        commit = "c" * 40
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_manifest_v1_artifact(root, commit)
            (root / "asset-manifest.json").unlink()
            with self.assertRaisesRegex(ValueError, "missing asset-manifest"):
                inspect_artifact_identity(
                    root,
                    expected_commit=commit,
                    operation="promote",
                )

    def test_explicit_legacy_format_is_rollback_only_and_has_no_manifest_hash(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            version = {
                "buildId": LEGACY_V25_BUILD_ID,
                "bundleSchemaVersion": 2,
                "programId": "controlled-ai-workflow-consultant-path",
                "courseId": "course-1-controlled-ai-workflow-foundations",
                "courseVersion": "2.5.0",
                "verifiedThrough": "2026-07-28",
                "contentHash": LEGACY_V25_CONTENT_HASH,
                "commit": LEGACY_V25_COMMIT[:12],
            }
            (root / "version.json").write_bytes(
                f"{json.dumps(version, indent=2)}\n".encode()
            )
            tree_hash = promotion_verifier.artifact_tree_sha256(root)
            with (
                patch.object(
                    promotion_verifier,
                    "LEGACY_V25_FILES",
                    {"version.json"},
                ),
                patch.object(
                    promotion_verifier,
                    "LEGACY_V25_TREE_SHA256",
                    tree_hash,
                ),
            ):
                identity = inspect_artifact_identity(
                    root,
                    expected_commit=LEGACY_V25_COMMIT,
                    operation="rollback",
                )
            self.assertEqual(
                identity["artifactFormat"],
                LEGACY_V25_ARTIFACT_FORMAT,
            )
            self.assertIsNone(identity["assetManifestSha256"])

    def test_legacy_acceptance_record_uses_null_manifest_and_full_source_commit(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            evidence_root = Path(temporary)
            release_evidence = evidence_root / "release_evidence"
            release_evidence.mkdir()
            evidence_candidate = {
                "commit": LEGACY_V25_COMMIT,
                "courseVersion": "2.5.0",
                "buildId": LEGACY_V25_BUILD_ID,
                "contentHash": LEGACY_V25_CONTENT_HASH,
            }
            manifest = json.loads(
                (
                    ROOT
                    / "audit_control"
                    / "course1"
                    / "technical_test_manifest.json"
                ).read_text(encoding="utf-8")
            )
            test_definitions = {
                row["id"]: row for row in manifest["tests"]
            }
            artifact_directory = release_evidence / "artifacts"
            artifact_directory.mkdir()
            evidence = []
            for evidence_id, test_id, evidence_class in (
                ("C1-EV-PROV-001", "C1-TST-PROV-001", "POST_DEPLOY"),
                (
                    "C1-EV-RECOVERY-001",
                    "C1-TST-RECOVERY-001",
                    "AUTOMATED_LOCAL",
                ),
                ("C1-EV-SW-002", "C1-TST-SW-002", "REAL_BROWSER"),
            ):
                definition = test_definitions[test_id]
                procedures = [
                    (procedure["locator"], procedure["selector"])
                    for procedure in definition["procedures"]
                ]
                environments = definition["environments"]
                artifacts = []
                for index in range(max(len(procedures), len(environments))):
                    procedure_locator, procedure_selector = procedures[
                        index % len(procedures)
                    ]
                    environment = environments[index % len(environments)]
                    artifact_filename = (
                        f"{test_id.casefold()}-{index + 1}.log"
                    )
                    artifact_path = artifact_directory / artifact_filename
                    artifact_path.write_text(
                        (
                            f"testId={test_id}\n"
                            "result=PASS\n"
                            f"procedure={procedure_locator}#{procedure_selector}\n"
                            f"environment={environment}\n"
                        ),
                        encoding="utf-8",
                    )
                    artifacts.append(
                        {
                            "path": (
                                "release_evidence/artifacts/"
                                f"{artifact_filename}"
                            ),
                            "sha256": hashlib.sha256(
                                artifact_path.read_bytes()
                            ).hexdigest(),
                            "kind": "COMMAND_LOG",
                            "procedureLocator": procedure_locator,
                            "procedureSelector": procedure_selector,
                            "environment": environment,
                        }
                    )
                evidence_record = {
                    "schemaVersion": "course1-technical-evidence-v1",
                    "evidenceId": evidence_id,
                    "testId": test_id,
                    "candidate": evidence_candidate,
                    "result": "PASS",
                    "evidenceClass": evidence_class,
                    "recordedAt": "2026-07-29T01:00:00+02:00",
                    "reviewer": {
                        "name": "Rollback reviewer",
                        "independentOfImplementation": True,
                    },
                    "artifacts": artifacts,
                }
                filename = f"{test_id.casefold()}.json"
                evidence_path = release_evidence / filename
                evidence_path.write_bytes(
                    f"{json.dumps(evidence_record, indent=2)}\n".encode()
                )
                evidence.append(
                    {
                        "path": f"release_evidence/{filename}",
                        "sha256": hashlib.sha256(
                            evidence_path.read_bytes()
                        ).hexdigest(),
                    }
                )
            candidate = {
                "artifactFormat": LEGACY_V25_ARTIFACT_FORMAT,
                **evidence_candidate,
                "assetManifestSha256": None,
                "artifactTreeSha256": LEGACY_V25_TREE_SHA256,
            }
            historical_acceptance = (
                ROOT
                / "release_evidence"
                / "COURSE_1_V2.5.0_ACCEPTANCE.md"
            ).read_bytes()
            historical_acceptance_path = (
                release_evidence / "COURSE_1_V2.5.0_ACCEPTANCE.md"
            )
            historical_acceptance_path.write_bytes(historical_acceptance)
            record = {
                "schemaVersion": 1,
                "decision": "ACCEPTED_FOR_ROLLBACK",
                "courseId": "course-1-controlled-ai-workflow-foundations",
                "candidate": candidate,
                "acceptedAt": "2026-07-29T01:00:00+02:00",
                "authorizedBy": {"name": "Rollback owner"},
                "gates": {
                    "artifactIdentity": True,
                    "lastKnownGoodAcceptance": True,
                    "learnerStateRecoveryPlan": True,
                    "rollbackAuthorized": True,
                },
                "rollback": {
                    "failedCandidateCommit": "f" * 40,
                    "trigger": "Blocking public failure",
                    "lastKnownGoodAcceptanceRecord": {
                        "path": (
                            "release_evidence/"
                            "COURSE_1_V2.5.0_ACCEPTANCE.md"
                        ),
                        "sha256": hashlib.sha256(
                            historical_acceptance_path.read_bytes()
                        ).hexdigest(),
                    },
                    "learnerStateRisk": (
                        "Schema compatibility must pass before deployment"
                    ),
                },
                "evidence": evidence,
            }
            version = {
                "courseVersion": "2.5.0",
                "buildId": LEGACY_V25_BUILD_ID,
                "contentHash": LEGACY_V25_CONTENT_HASH,
                "commit": LEGACY_V25_COMMIT[:12],
            }
            ledger_text = (
                "- Current status: **`REPAIR REQUIRED`**\n\n"
                "| ID | Severity | Requirement | Closure test and evidence | Status | Owner |\n"
                "|---|---|---|---|---|---|\n"
                + "".join(
                    f"| `{finding_id}` | High | Requirement | Evidence | CLOSED | Owner |\n"
                    for finding_id in sorted(EXPECTED_LEDGER_FINDING_IDS)
                )
            )
            self.assertEqual(
                validate(
                    record,
                    version,
                    expected_commit=LEGACY_V25_COMMIT,
                    asset_manifest_sha256=None,
                    artifact_tree_sha256_value=LEGACY_V25_TREE_SHA256,
                    ledger_text=ledger_text,
                    operation="rollback",
                    evidence_repository_root=evidence_root,
                    artifact_format=LEGACY_V25_ARTIFACT_FORMAT,
                ),
                [],
            )
            record["rollback"]["lastKnownGoodAcceptanceRecord"][
                "sha256"
            ] = "f" * 64
            failures = validate(
                record,
                version,
                expected_commit=LEGACY_V25_COMMIT,
                asset_manifest_sha256=None,
                artifact_tree_sha256_value=LEGACY_V25_TREE_SHA256,
                ledger_text=ledger_text,
                operation="rollback",
                evidence_repository_root=evidence_root,
                artifact_format=LEGACY_V25_ARTIFACT_FORMAT,
            )
            self.assertTrue(
                any(
                    "immutable historical v2.5 acceptance" in failure
                    for failure in failures
                ),
                failures,
            )


if __name__ == "__main__":
    unittest.main()
