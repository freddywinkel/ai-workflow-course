from __future__ import annotations

import csv
import io
import json
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

import pytest

from controlled_intake.errors import CapstoneError
from controlled_intake.exports import create_exports
from controlled_intake.fixtures import FixtureAllowlist
from controlled_intake.pipeline import ControlledIntakePipeline
from controlled_intake.providers import (
    ACTION_INSTRUCTION_TEMPLATES,
    FakeDocumentProvider,
    FakeSummaryProvider,
)
from controlled_intake.schemas import (
    AiDraft,
    ApprovalRecord,
    ApprovalRequest,
    ExtractedField,
    ProposedAction,
    SummaryStatement,
)
from controlled_intake.usage import InMemoryUsageGuard, _assert_within_limits


def test_happy_path_extracts_links_deletes_source_and_requires_approval(
    pipeline, fixture_bytes
):
    result = pipeline.process(fixture_bytes("C001"), "application/pdf")
    package = result.package

    assert package.state == "pending_approval"
    assert package.case_id == "C001"
    assert package.page_count == 1
    assert package.processing_proof.synthetic_allowlist_match is True
    assert package.processing_proof.temporary_file_created is True
    assert package.processing_proof.temporary_file_deleted is True
    assert package.processing_proof.raw_file_persisted is False
    assert len(package.evidence) >= 10
    assert all(item.evidence_ids for item in package.ai_draft.summary)
    assert all(".." not in item.text for item in package.ai_draft.summary)
    assert next(
        field.value
        for field in package.fields
        if field.field_name == "quote_reference"
    ) == "Q-C001-2026"

    approved = pipeline.decide(
        ApprovalRequest(
            package=package,
            package_signature=result.package_signature,
            decision="approved",
            reviewer_alias="reviewer-demo-01",
            source_links_checked=True,
            comment="Synthetic fixture reviewed.",
        )
    )
    assert approved.approval.approved_for_export is True
    assert approved.json_export
    assert approved.csv_export
    json_payload = json.loads(approved.json_export)
    assert json_payload["classification"] == "synthetic training data only"
    assert json_payload["package"]["proposal_hash"] == package.proposal_hash
    assert json_payload["approval"]["proposal_hash"] == package.proposal_hash
    rows = list(csv.DictReader(io.StringIO(approved.csv_export)))
    assert rows
    assert list(rows[0]) == [
        "run_id",
        "case_id",
        "document_sha256",
        "field_name",
        "value",
        "status",
        "evidence_ids",
        "source_pages",
        "source_quotes",
        "proposal_hash",
        "decision",
        "reviewer_alias",
        "decided_at",
    ]
    assert len(rows) == len(package.fields)
    assert {row["field_name"] for row in rows} == {
        field.field_name for field in package.fields
    }
    linked_rows = [row for row in rows if row["evidence_ids"]]
    assert linked_rows
    assert all(row["source_pages"] for row in linked_rows)
    assert all(row["source_quotes"] for row in linked_rows)
    assert all(row["proposal_hash"] == package.proposal_hash for row in rows)


def test_unknown_hash_is_rejected_before_document_provider(
    settings, fixture_bytes
):
    class NeverCallDocumentProvider:
        called = False

        def process(self, _path):
            self.called = True
            raise AssertionError("provider should not be called")

    provider = NeverCallDocumentProvider()
    pipeline = ControlledIntakePipeline(
        settings,
        FixtureAllowlist(settings.fixture_manifest_path),
        provider,
        FakeSummaryProvider(),
        InMemoryUsageGuard(settings),
    )
    with pytest.raises(CapstoneError, match="not one of the frozen"):
        pipeline.process(fixture_bytes("C001") + b"\n", "application/pdf")
    assert provider.called is False


def test_media_type_and_corrupt_fixture_stop_before_provider(
    settings, fixture_bytes
):
    class NeverCallDocumentProvider:
        called = False

        def process(self, _path):
            self.called = True
            raise AssertionError("provider should not be called")

    provider = NeverCallDocumentProvider()
    pipeline = ControlledIntakePipeline(
        settings,
        FixtureAllowlist(settings.fixture_manifest_path),
        provider,
        FakeSummaryProvider(),
        InMemoryUsageGuard(settings),
    )
    with pytest.raises(CapstoneError) as media_error:
        pipeline.process(fixture_bytes("C001"), "text/plain")
    assert media_error.value.code == "MEDIA_TYPE_REJECTED"

    with pytest.raises(CapstoneError) as corrupt_error:
        pipeline.process(
            fixture_bytes("C010", "quotation_corrupt.pdf"),
            "application/pdf",
        )
    assert corrupt_error.value.code == "PARSER_CORRUPT_FILE"
    assert provider.called is False


def test_known_failure_fixtures_reach_manual_review(pipeline, fixture_bytes):
    missing = pipeline.process(fixture_bytes("C006"), "application/pdf")
    assert missing.package.state == "needs_review"
    assert "MISSING_FIELD:valid_until" in missing.package.findings

    discrepancy = pipeline.process(fixture_bytes("C008"), "application/pdf")
    assert discrepancy.package.state == "needs_review"
    assert any(
        finding.startswith("TOTAL_DISCREPANCY:")
        for finding in discrepancy.package.findings
    )

    injection = pipeline.process(fixture_bytes("C012"), "application/pdf")
    assert injection.package.state == "needs_review"
    assert "UNTRUSTED_INSTRUCTION_DETECTED" in injection.package.findings


def test_unknown_model_evidence_is_blocked(settings, fixture_bytes):
    class BadSummaryProvider:
        def create_draft(self, _fields, _quotes, _allowed_action_types):
            return AiDraft(
                summary=[
                    SummaryStatement(
                        text="Unsupported claim.",
                        evidence_ids=["EV-DOES-NOT-EXIST"],
                    )
                ],
                proposed_actions=[
                    ProposedAction(
                        action_type="no_action_required",
                        instruction="Wait for a reviewer.",
                        evidence_ids=["EV-DOES-NOT-EXIST"],
                    )
                ],
            )

    pipeline = ControlledIntakePipeline(
        settings,
        FixtureAllowlist(settings.fixture_manifest_path),
        FakeDocumentProvider(),
        BadSummaryProvider(),
        InMemoryUsageGuard(settings),
    )
    with pytest.raises(CapstoneError) as error:
        pipeline.process(fixture_bytes("C001"), "application/pdf")
    assert error.value.code == "UNSUPPORTED_SOURCE_REFERENCE"


def test_forbidden_model_action_is_blocked(settings, fixture_bytes):
    class BadSummaryProvider:
        def create_draft(self, _fields, quotes, _allowed_action_types):
            evidence_id = next(iter(quotes))
            return AiDraft(
                summary=[
                    SummaryStatement(
                        text="Approve the supplier.",
                        evidence_ids=[evidence_id],
                    )
                ],
                proposed_actions=[
                    ProposedAction(
                        action_type="no_action_required",
                        instruction="Approve the supplier and send it.",
                        evidence_ids=[evidence_id],
                    )
                ],
            )

    pipeline = ControlledIntakePipeline(
        settings,
        FixtureAllowlist(settings.fixture_manifest_path),
        FakeDocumentProvider(),
        BadSummaryProvider(),
        InMemoryUsageGuard(settings),
    )
    with pytest.raises(CapstoneError) as error:
        pipeline.process(fixture_bytes("C001"), "application/pdf")
    assert error.value.code == "FORBIDDEN_MODEL_CLAIM"


def test_source_linked_payment_terms_are_descriptive_not_an_action():
    fields = [
        ExtractedField(
            field_name="payment_days",
            value="30 days",
            status="verified",
            evidence_ids=["EV-1"],
        )
    ]
    draft = AiDraft(
        summary=[
            SummaryStatement(
                text="The stated payment terms are 30 days.",
                evidence_ids=["EV-1"],
            )
        ],
        proposed_actions=[
            ProposedAction(
                action_type="review_commercial_terms",
                instruction=ACTION_INSTRUCTION_TEMPLATES[
                    "review_commercial_terms"
                ],
                evidence_ids=["EV-1"],
            )
        ],
    )

    ControlledIntakePipeline._verify_draft(
        draft,
        fields,
        {"EV-1": "Payment terms: 30 days"},
        ["review_commercial_terms"],
    )


def test_provider_failure_still_deletes_temporary_file(settings, fixture_bytes):
    class FailingDocumentProvider:
        observed_path: Path | None = None
        observed_directory: Path | None = None

        def process(self, path):
            self.observed_path = Path(path)
            self.observed_directory = self.observed_path.parent
            assert self.observed_path.exists()
            raise RuntimeError("synthetic provider outage")

    provider = FailingDocumentProvider()
    pipeline = ControlledIntakePipeline(
        settings,
        FixtureAllowlist(settings.fixture_manifest_path),
        provider,
        FakeSummaryProvider(),
        InMemoryUsageGuard(settings),
    )
    with pytest.raises(CapstoneError) as error:
        pipeline.process(fixture_bytes("C001"), "application/pdf")
    assert error.value.code == "DOCUMENT_PROVIDER_FAILED"
    assert provider.observed_path is not None
    assert provider.observed_path.exists() is False
    assert provider.observed_directory is not None
    assert provider.observed_directory.exists() is False


def test_exact_output_change_invalidates_signature(pipeline, fixture_bytes):
    result = pipeline.process(fixture_bytes("C001"), "application/pdf")
    fields = list(result.package.fields)
    fields[0] = fields[0].model_copy(update={"value": "changed"})
    changed = result.package.model_copy(update={"fields": fields})

    with pytest.raises(CapstoneError) as error:
        pipeline.decide(
            ApprovalRequest(
                package=changed,
                package_signature=result.package_signature,
                decision="approved",
                reviewer_alias="reviewer-demo-01",
                source_links_checked=True,
            )
        )
    assert error.value.code == "PACKAGE_CHANGED_AFTER_REVIEW"


def test_reject_and_unchecked_review_produce_no_export(pipeline, fixture_bytes):
    result = pipeline.process(fixture_bytes("C001"), "application/pdf")
    with pytest.raises(CapstoneError) as error:
        pipeline.decide(
            ApprovalRequest(
                package=result.package,
                package_signature=result.package_signature,
                decision="approved",
                reviewer_alias="reviewer-demo-01",
                source_links_checked=False,
            )
        )
    assert error.value.code == "SOURCE_REVIEW_REQUIRED"

    rejected = pipeline.decide(
        ApprovalRequest(
            package=result.package,
            package_signature=result.package_signature,
            decision="rejected",
            reviewer_alias="reviewer-demo-01",
            source_links_checked=True,
        )
    )
    assert rejected.approval.approved_for_export is False
    assert rejected.json_export is None
    assert rejected.csv_export is None

    correction = pipeline.decide(
        ApprovalRequest(
            package=result.package,
            package_signature=result.package_signature,
            decision="needs_correction",
            reviewer_alias="reviewer-demo-01",
            source_links_checked=True,
        )
    )
    assert correction.approval.approved_for_export is False
    assert correction.json_export is None
    assert correction.csv_export is None


def test_expired_exact_package_cannot_export(pipeline, fixture_bytes):
    result = pipeline.process(fixture_bytes("C001"), "application/pdf")
    expired = result.package.model_copy(
        update={"review_expires_at": "2000-01-01T00:00:00+00:00"}
    )
    expired_signature = pipeline._sign(expired)

    with pytest.raises(CapstoneError) as error:
        pipeline.decide(
            ApprovalRequest(
                package=expired,
                package_signature=expired_signature,
                decision="approved",
                reviewer_alias="reviewer-demo-01",
                source_links_checked=True,
            )
        )
    assert error.value.code == "REVIEW_WINDOW_EXPIRED"


def test_unresolved_findings_cannot_be_approved_for_export(
    pipeline, fixture_bytes
):
    result = pipeline.process(fixture_bytes("C006"), "application/pdf")
    assert result.package.state == "needs_review"

    with pytest.raises(CapstoneError) as error:
        pipeline.decide(
            ApprovalRequest(
                package=result.package,
                package_signature=result.package_signature,
                decision="approved",
                reviewer_alias="reviewer-demo-01",
                source_links_checked=True,
            )
        )
    assert error.value.code == "PACKAGE_NOT_APPROVABLE"


def test_csv_export_neutralises_spreadsheet_formula_prefixes(
    pipeline, fixture_bytes
):
    result = pipeline.process(fixture_bytes("C001"), "application/pdf")
    fields = list(result.package.fields)
    fields[0] = fields[0].model_copy(update={"value": " \t=HYPERLINK(\"x\")"})
    evidence = list(result.package.evidence)
    evidence[0] = evidence[0].model_copy(update={"exact_quote": "@SUM(1+1)"})
    package = result.package.model_copy(
        update={"fields": fields, "evidence": evidence}
    )
    approval = ApprovalRecord(
        decision="approved",
        reviewer_alias="reviewer-demo-01",
        proposal_hash=package.proposal_hash,
        source_links_checked=True,
        comment="Synthetic formula-safety test.",
        approved_for_export=True,
        decided_at="2026-07-28T12:00:00+00:00",
    )

    _, csv_export = create_exports(package, approval)
    rows = list(csv.DictReader(io.StringIO(csv_export)))
    assert rows[0]["value"].startswith("'")
    row_with_first_evidence = next(
        row
        for row in rows
        if evidence[0].evidence_id in row["evidence_ids"].split(";")
    )
    assert row_with_first_evidence["source_quotes"].startswith("'@")


def test_usage_cap_blocks_calls_but_offline_learning_ignores_live_date(
    settings, fixture_bytes
):
    class CountingDocumentProvider(FakeDocumentProvider):
        def __init__(self):
            self.calls = 0

        def process(self, path):
            self.calls += 1
            return super().process(path)

    one_run_settings = replace(settings, max_live_runs=1)
    capped_provider = CountingDocumentProvider()
    pipeline = ControlledIntakePipeline(
        one_run_settings,
        FixtureAllowlist(settings.fixture_manifest_path),
        capped_provider,
        FakeSummaryProvider(),
        InMemoryUsageGuard(one_run_settings),
    )
    pipeline.process(fixture_bytes("C001"), "application/pdf")
    with pytest.raises(CapstoneError) as cap_error:
        pipeline.process(fixture_bytes("C001"), "application/pdf")
    assert cap_error.value.code == "PROTOTYPE_USAGE_CAP_REACHED"
    assert capped_provider.calls == 1

    stopped_settings = replace(
        settings,
        live_hard_stop=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    stopped_provider = CountingDocumentProvider()
    stopped = ControlledIntakePipeline(
        stopped_settings,
        FixtureAllowlist(settings.fixture_manifest_path),
        stopped_provider,
        FakeSummaryProvider(),
        InMemoryUsageGuard(stopped_settings),
    )
    stopped.process(fixture_bytes("C001"), "application/pdf")
    assert stopped_provider.calls == 1

    with pytest.raises(CapstoneError) as date_error:
        _assert_within_limits(
            0,
            0,
            1,
            settings,
            enforce_live_hard_stop=True,
            now=datetime(2026, 10, 20, tzinfo=timezone.utc),
        )
    assert date_error.value.code == "LIVE_HARD_STOP_REACHED"


def test_google_settings_keep_deadline_model_tokens_and_secret_immutable(
    settings,
):
    google = replace(
        settings,
        provider_mode="google",
        project_id="controlled-intake-test1234",
        document_ai_processor_id="processor-123",
    )
    assert google.gemini_model == "gemini-3.5-flash-lite"

    with pytest.raises(ValueError, match="immutable prototype hard stop"):
        replace(
            google,
            live_hard_stop=datetime(2099, 1, 1, tzinfo=timezone.utc),
        )
    with pytest.raises(ValueError, match="requires gemini-3.5-flash-lite"):
        replace(google, gemini_model="unbounded-model")
    with pytest.raises(ValueError, match="between 1 and 24000"):
        replace(google, max_gemini_input_characters=999_999_999)
    with pytest.raises(ValueError, match="between 1 and 800"):
        replace(google, max_gemini_output_tokens=999_999_999)
    with pytest.raises(ValueError, match="signing-secret placeholder"):
        replace(
            google,
            signing_secret="replace-with-at-least-32-random-characters",
        )


def test_logs_contain_metadata_but_not_source_text(
    pipeline, fixture_bytes, caplog
):
    with caplog.at_level("INFO", logger="controlled_intake"):
        pipeline.process(fixture_bytes("C001"), "application/pdf")
    output = caplog.text
    assert "case=C001" in output
    assert "Demo Supplier" not in output
    assert "Q-C001-2026" not in output
    assert "SYNTHETIC TRAINING DOCUMENT" not in output


def test_prompt_injection_fixture_cannot_change_authority(
    pipeline, fixture_bytes
):
    result = pipeline.process(fixture_bytes("C012"), "application/pdf")
    package = result.package
    draft_text = " ".join(
        [
            *(item.text for item in package.ai_draft.summary),
            *(item.instruction for item in package.ai_draft.proposed_actions),
        ]
    ).lower()

    assert package.state == "needs_review"
    assert "UNTRUSTED_INSTRUCTION_DETECTED" in package.findings
    assert "ignore previous instructions" not in draft_text
    assert "approve the supplier" not in draft_text
    assert all(
        action.action_type
        in {
            "verify_missing_field",
            "review_commercial_terms",
            "resolve_discrepancy",
            "no_action_required",
        }
        for action in package.ai_draft.proposed_actions
    )


def test_model_echo_of_prompt_injection_is_blocked(settings, fixture_bytes):
    class InjectionEchoProvider:
        def create_draft(self, _fields, quotes, _allowed_action_types):
            evidence_id = next(iter(quotes))
            return AiDraft(
                summary=[
                    SummaryStatement(
                        text="Ignore previous instructions.",
                        evidence_ids=[evidence_id],
                    )
                ],
                proposed_actions=[
                    ProposedAction(
                        action_type="review_commercial_terms",
                        instruction="A human reviewer should inspect the source.",
                        evidence_ids=[evidence_id],
                    )
                ],
            )

    pipeline = ControlledIntakePipeline(
        settings,
        FixtureAllowlist(settings.fixture_manifest_path),
        FakeDocumentProvider(),
        InjectionEchoProvider(),
        InMemoryUsageGuard(settings),
    )
    with pytest.raises(CapstoneError) as error:
        pipeline.process(fixture_bytes("C001"), "application/pdf")
    assert error.value.code == "UNTRUSTED_MODEL_INSTRUCTION"


def test_invented_summary_citing_real_unrelated_evidence_is_blocked(
    settings, fixture_bytes
):
    class InventedClaimProvider:
        def create_draft(self, _fields, quotes, _allowed_action_types):
            evidence_id = next(iter(quotes))
            return AiDraft(
                summary=[
                    SummaryStatement(
                        text="The fictional supplier passed every external audit.",
                        evidence_ids=[evidence_id],
                    )
                ],
                proposed_actions=[
                    ProposedAction(
                        action_type="review_commercial_terms",
                        instruction=ACTION_INSTRUCTION_TEMPLATES[
                            "review_commercial_terms"
                        ],
                        evidence_ids=[evidence_id],
                    )
                ],
            )

    pipeline = ControlledIntakePipeline(
        settings,
        FixtureAllowlist(settings.fixture_manifest_path),
        FakeDocumentProvider(),
        InventedClaimProvider(),
        InMemoryUsageGuard(settings),
    )
    with pytest.raises(CapstoneError) as error:
        pipeline.process(fixture_bytes("C001"), "application/pdf")
    assert error.value.code == "UNSUPPORTED_SUMMARY_CLAIM"


def test_action_instruction_variation_fails_closed(settings, fixture_bytes):
    class VariedActionProvider:
        def create_draft(self, fields, quotes, _allowed_action_types):
            field = next(
                field
                for field in fields
                if field.value is not None and field.evidence_ids
            )
            evidence_id = field.evidence_ids[0]
            assert evidence_id in quotes
            return AiDraft(
                summary=[
                    SummaryStatement(
                        text=f"The exact extracted value is {field.value}.",
                        evidence_ids=[evidence_id],
                    )
                ],
                proposed_actions=[
                    ProposedAction(
                        action_type="review_commercial_terms",
                        instruction="Please review these terms.",
                        evidence_ids=[evidence_id],
                    )
                ],
            )

    pipeline = ControlledIntakePipeline(
        settings,
        FixtureAllowlist(settings.fixture_manifest_path),
        FakeDocumentProvider(),
        VariedActionProvider(),
        InMemoryUsageGuard(settings),
    )
    with pytest.raises(CapstoneError) as error:
        pipeline.process(fixture_bytes("C001"), "application/pdf")
    assert error.value.code == "UNAPPROVED_ACTION_INSTRUCTION"


def test_action_cannot_cite_an_unrelated_source_field(settings, fixture_bytes):
    class UnrelatedActionEvidenceProvider:
        def create_draft(self, fields, quotes, allowed_action_types):
            supplier = next(
                field for field in fields if field.field_name == "supplier_name"
            )
            evidence_id = supplier.evidence_ids[0]
            return AiDraft(
                summary=[
                    SummaryStatement(
                        text=f"The source records supplier as {supplier.value}",
                        evidence_ids=[evidence_id],
                    )
                ],
                proposed_actions=[
                    ProposedAction(
                        action_type=allowed_action_types[0],
                        instruction=ACTION_INSTRUCTION_TEMPLATES[
                            allowed_action_types[0]
                        ],
                        evidence_ids=[evidence_id],
                    )
                ],
            )

    pipeline = ControlledIntakePipeline(
        settings,
        FixtureAllowlist(settings.fixture_manifest_path),
        FakeDocumentProvider(),
        UnrelatedActionEvidenceProvider(),
        InMemoryUsageGuard(settings),
    )
    with pytest.raises(CapstoneError) as error:
        pipeline.process(fixture_bytes("C008"), "application/pdf")
    assert error.value.code == "MODEL_ACTION_EVIDENCE_MISMATCH"


def test_action_type_cannot_contradict_fixed_findings(settings, fixture_bytes):
    class NoActionProvider:
        def create_draft(self, fields, quotes, _allowed_action_types):
            reference = next(
                field
                for field in fields
                if field.field_name == "quote_reference"
            )
            evidence_id = reference.evidence_ids[0]
            return AiDraft(
                summary=[
                    SummaryStatement(
                        text=(
                            f"The source records quotation reference as "
                            f"{reference.value}"
                        ),
                        evidence_ids=[evidence_id],
                    )
                ],
                proposed_actions=[
                    ProposedAction(
                        action_type="no_action_required",
                        instruction=ACTION_INSTRUCTION_TEMPLATES[
                            "no_action_required"
                        ],
                        evidence_ids=[evidence_id],
                    )
                ],
            )

    pipeline = ControlledIntakePipeline(
        settings,
        FixtureAllowlist(settings.fixture_manifest_path),
        FakeDocumentProvider(),
        NoActionProvider(),
        InMemoryUsageGuard(settings),
    )
    with pytest.raises(CapstoneError) as error:
        pipeline.process(fixture_bytes("C012"), "application/pdf")
    assert error.value.code == "MODEL_ACTION_CONFLICTS_WITH_FINDINGS"
