from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class FixtureRecord(StrictModel):
    case_id: str
    relative_path: str
    sha256: str
    byte_length: int
    page_count: int | None
    expected_path: str


class EvidenceLink(StrictModel):
    evidence_id: str
    document_sha256: str
    page_number: int
    start_index: int
    end_index: int
    exact_quote: str
    quote_sha256: str
    normalized_bbox: list[float] | None = None


class ExtractedField(StrictModel):
    field_name: str
    value: str | None
    status: Literal["verified", "missing", "needs_review"]
    evidence_ids: list[str] = Field(default_factory=list)


class SummaryStatement(StrictModel):
    text: str
    evidence_ids: list[str] = Field(min_length=1, max_length=4)


class ProposedAction(StrictModel):
    action_type: Literal[
        "verify_missing_field",
        "review_commercial_terms",
        "resolve_discrepancy",
        "no_action_required",
    ]
    instruction: str
    evidence_ids: list[str] = Field(min_length=1, max_length=4)


class AiDraft(StrictModel):
    summary: list[SummaryStatement] = Field(min_length=1, max_length=5)
    proposed_actions: list[ProposedAction] = Field(min_length=1, max_length=4)


class GeminiSelection(StrictModel):
    summary_candidate_ids: list[str] = Field(min_length=1, max_length=3)
    action_type: Literal[
        "verify_missing_field",
        "review_commercial_terms",
        "resolve_discrepancy",
        "no_action_required",
    ]
    action_candidate_ids: list[str] = Field(min_length=1, max_length=2)


class ProcessingProof(StrictModel):
    synthetic_allowlist_match: bool
    temporary_file_created: bool
    temporary_file_deleted: bool
    raw_file_persisted: bool
    provider_mode: Literal["fake", "google"]
    document_ai_location: Literal["eu"]
    vertex_location: Literal["eu"]
    model_id: str


class DraftPackage(StrictModel):
    schema_version: Literal["1.0"]
    run_id: str
    case_id: str
    document_sha256: str
    created_at: str
    review_expires_at: str
    page_count: int
    state: Literal["pending_approval", "needs_review"]
    fields: list[ExtractedField]
    evidence: list[EvidenceLink]
    ai_draft: AiDraft
    findings: list[str]
    processing_proof: ProcessingProof
    proposal_hash: str


class IntakeResponse(StrictModel):
    package: DraftPackage
    package_signature: str


class ApprovalRequest(StrictModel):
    package: DraftPackage
    package_signature: str
    decision: Literal["approved", "rejected", "needs_correction"]
    reviewer_alias: str
    source_links_checked: bool
    comment: str = Field(default="", max_length=500)

    @field_validator("reviewer_alias")
    @classmethod
    def validate_reviewer_alias(cls, value: str) -> str:
        if (
            len(value) != 16
            or not value.startswith("reviewer-demo-")
            or not value[-2:].isdigit()
        ):
            raise ValueError("Use a fictional alias such as reviewer-demo-01.")
        return value


class ApprovalRecord(StrictModel):
    decision: Literal["approved", "rejected", "needs_correction"]
    reviewer_alias: str
    proposal_hash: str
    source_links_checked: bool
    comment: str
    approved_for_export: bool
    decided_at: str


class ApprovalResponse(StrictModel):
    approval: ApprovalRecord
    json_export: str | None
    csv_export: str | None


class DocumentText(StrictModel):
    text: str
    segments: list["TextSegment"]


class TextSegment(StrictModel):
    page_number: int
    start_index: int
    end_index: int
    normalized_bbox: list[float] | None = None
