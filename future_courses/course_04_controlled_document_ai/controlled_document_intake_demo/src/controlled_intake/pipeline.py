from __future__ import annotations

import hashlib
import hmac
import json
import logging
import re
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from tempfile import TemporaryDirectory

from .errors import CapstoneError
from .evidence import extract_fields, verify_evidence
from .exports import create_exports
from .fixtures import FixtureAllowlist
from .providers import (
    ACTION_EVIDENCE_FIELD_ALLOWLISTS,
    ACTION_INSTRUCTION_TEMPLATES,
    DocumentProvider,
    SummaryProvider,
)
from .schemas import (
    AiDraft,
    ApprovalRecord,
    ApprovalRequest,
    ApprovalResponse,
    DraftPackage,
    IntakeResponse,
    ProcessingProof,
)
from .security import verify_pdf
from .settings import Settings
from .usage import UsageGuard

LOGGER = logging.getLogger("controlled_intake")

FORBIDDEN_DRAFT_PATTERNS = (
    r"\bapprove(?:d|s|ing)?\s+(?:the\s+)?supplier\b",
    r"\bselect(?:ed|s|ing)?\s+(?:the\s+)?supplier\b",
    r"\b(?:pay|pays|paying|paid)\b",
    r"\bsend(?:ing)?\b",
    r"\blegally compliant\b",
    r"\bcertif(?:y|ied|ication)\b",
)

UNTRUSTED_INSTRUCTION_PATTERNS = (
    r"ignore (?:all |the )?(?:previous|prior) instructions",
    r"system prompt",
    r"override (?:the )?(?:rules|policy|approval)",
    r"mark (?:this|the) (?:supplier|quotation) approved",
)


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _parse_money(value: str | None) -> Decimal | None:
    if value is None:
        return None
    cleaned = re.sub(r"[^0-9,.\-]", "", value)
    if not cleaned:
        return None
    if "," in cleaned and "." in cleaned:
        if cleaned.rfind(",") > cleaned.rfind("."):
            cleaned = cleaned.replace(".", "").replace(",", ".")
        else:
            cleaned = cleaned.replace(",", "")
    elif "," in cleaned:
        cleaned = cleaned.replace(",", ".")
    try:
        return Decimal(cleaned)
    except InvalidOperation:
        return None


def _normalise_support_text(value: str) -> str:
    return " ".join(value.casefold().split())


def _allowed_action_types(findings: list[str]) -> list[str]:
    codes = {finding.split(":", 1)[0] for finding in findings}
    allowed: list[str] = []
    if "MISSING_FIELD" in codes:
        allowed.append("verify_missing_field")
    if "TOTAL_DISCREPANCY" in codes:
        allowed.append("resolve_discrepancy")
    if codes - {"MISSING_FIELD", "TOTAL_DISCREPANCY"}:
        allowed.append("review_commercial_terms")
    return allowed or ["review_commercial_terms"]


class ControlledIntakePipeline:
    def __init__(
        self,
        settings: Settings,
        allowlist: FixtureAllowlist,
        document_provider: DocumentProvider,
        summary_provider: SummaryProvider,
        usage_guard: UsageGuard,
    ):
        self._settings = settings
        self._allowlist = allowlist
        self._document_provider = document_provider
        self._summary_provider = summary_provider
        self._usage_guard = usage_guard

    def _sign(self, package: DraftPackage) -> str:
        return hmac.new(
            self._settings.signing_secret.encode("utf-8"),
            _canonical_bytes(package.model_dump(mode="json")),
            hashlib.sha256,
        ).hexdigest()

    def _verify_signature(self, package: DraftPackage, signature: str) -> None:
        if not hmac.compare_digest(self._sign(package), signature):
            raise CapstoneError(
                "PACKAGE_CHANGED_AFTER_REVIEW",
                "The review package changed after it was created. Process the "
                "synthetic document again and review the new exact output.",
                409,
            )

    @staticmethod
    def _verify_draft(
        draft: AiDraft,
        fields,
        evidence_quotes: dict[str, str],
        allowed_action_types: list[str],
    ) -> None:
        known_evidence_ids = set(evidence_quotes)
        items = [*draft.summary, *draft.proposed_actions]
        for item in items:
            unknown = set(item.evidence_ids) - known_evidence_ids
            if unknown:
                raise CapstoneError(
                    "UNSUPPORTED_SOURCE_REFERENCE",
                    "The model cited an evidence identifier that does not exist. "
                    "Manual review is required.",
                    502,
                )
            text = getattr(item, "text", None) or getattr(
                item, "instruction", ""
            )
            if any(
                re.search(pattern, text, re.IGNORECASE)
                for pattern in FORBIDDEN_DRAFT_PATTERNS
            ):
                raise CapstoneError(
                    "FORBIDDEN_MODEL_CLAIM",
                    "The model proposed an action outside the capstone boundary. "
                    "Manual review is required.",
                    502,
                )
            if any(
                re.search(pattern, text, re.IGNORECASE)
                for pattern in UNTRUSTED_INSTRUCTION_PATTERNS
            ):
                raise CapstoneError(
                    "UNTRUSTED_MODEL_INSTRUCTION",
                    "The model repeated an untrusted document instruction. "
                    "Manual review is required.",
                    502,
                )

        values_by_evidence: dict[str, set[str]] = {}
        for field in fields:
            if field.value is None:
                continue
            normalized_value = _normalise_support_text(field.value)
            if len(re.sub(r"\W", "", normalized_value)) < 4:
                continue
            for evidence_id in field.evidence_ids:
                normalized_quote = _normalise_support_text(
                    evidence_quotes.get(evidence_id, "")
                )
                if normalized_value in normalized_quote:
                    values_by_evidence.setdefault(evidence_id, set()).add(
                        normalized_value
                    )

        for statement in draft.summary:
            normalized_statement = _normalise_support_text(statement.text)
            cited_values = {
                value
                for evidence_id in statement.evidence_ids
                for value in values_by_evidence.get(evidence_id, set())
            }
            if not cited_values or not any(
                value in normalized_statement for value in cited_values
            ):
                raise CapstoneError(
                    "UNSUPPORTED_SUMMARY_CLAIM",
                    "A model summary did not repeat a meaningful value from its "
                    "cited source quote. Manual review is required.",
                    502,
                )

        for action in draft.proposed_actions:
            expected_instruction = ACTION_INSTRUCTION_TEMPLATES[
                action.action_type
            ]
            if action.instruction != expected_instruction:
                raise CapstoneError(
                    "UNAPPROVED_ACTION_INSTRUCTION",
                    "A model action did not match the approved human-review "
                    "template. Manual review is required.",
                    502,
                )
            if action.action_type not in allowed_action_types:
                raise CapstoneError(
                    "MODEL_ACTION_CONFLICTS_WITH_FINDINGS",
                    "The selected action did not match the fixed finding rules. "
                    "Manual review is required.",
                    502,
                )
            field_names_by_evidence: dict[str, set[str]] = {}
            for field in fields:
                for evidence_id in field.evidence_ids:
                    field_names_by_evidence.setdefault(
                        evidence_id, set()
                    ).add(field.field_name)
            cited_field_names = {
                field_name
                for evidence_id in action.evidence_ids
                for field_name in field_names_by_evidence.get(
                    evidence_id, set()
                )
            }
            allowed_field_names = ACTION_EVIDENCE_FIELD_ALLOWLISTS[
                action.action_type
            ]
            if not cited_field_names or not cited_field_names.issubset(
                allowed_field_names
            ):
                raise CapstoneError(
                    "MODEL_ACTION_EVIDENCE_MISMATCH",
                    "The selected action cited a source field that does not "
                    "support that action. Manual review is required.",
                    502,
                )

    @staticmethod
    def _findings(document_text: str, fields) -> list[str]:
        findings = [
            f"MISSING_FIELD:{field.field_name}"
            for field in fields
            if field.status == "missing"
        ]
        if any(
            re.search(pattern, document_text, re.IGNORECASE)
            for pattern in UNTRUSTED_INSTRUCTION_PATTERNS
        ):
            findings.append("UNTRUSTED_INSTRUCTION_DETECTED")

        values = {field.field_name: field.value for field in fields}
        net = _parse_money(values.get("net_total_ex_vat"))
        vat = _parse_money(values.get("vat_amount"))
        declared = _parse_money(values.get("total_inc_vat"))
        if None not in (net, vat, declared):
            calculated = (net + vat).quantize(Decimal("0.01"))
            if calculated != declared:
                findings.append(
                    f"TOTAL_DISCREPANCY:declared={declared};calculated={calculated}"
                )
        return findings

    def process(
        self,
        content: bytes,
        content_type: str,
    ) -> IntakeResponse:
        digest, fixture = self._allowlist.match(content)
        page_count = verify_pdf(
            content,
            content_type,
            self._settings.max_file_bytes,
            self._settings.max_pages_per_document,
        )
        if fixture.page_count != page_count:
            raise CapstoneError(
                "FIXTURE_PAGE_COUNT_MISMATCH",
                "The frozen fixture page count no longer matches its manifest.",
                422,
            )
        self._usage_guard.reserve(page_count)

        temporary_file_created = False
        temporary_file_deleted = False
        with TemporaryDirectory(prefix="controlled-intake-") as directory:
            file_path = Path(directory) / "source.pdf"
            file_path.write_bytes(content)
            temporary_file_created = file_path.exists()
            try:
                document = self._document_provider.process(file_path)
            except CapstoneError:
                raise
            except Exception as error:
                raise CapstoneError(
                    "DOCUMENT_PROVIDER_FAILED",
                    f"Document processing stopped safely: {type(error).__name__}.",
                    502,
                ) from error
            finally:
                file_path.unlink(missing_ok=True)
                temporary_file_deleted = not file_path.exists()

        if not temporary_file_deleted:
            raise CapstoneError(
                "TEMPORARY_FILE_DELETE_FAILED",
                "The temporary source could not be deleted. Processing stopped.",
                500,
            )

        fields, evidence = extract_fields(document, digest)
        try:
            verify_evidence(document, evidence)
        except ValueError as error:
            raise CapstoneError(
                "EVIDENCE_RESOLUTION_FAILED",
                str(error),
                502,
            ) from error
        if not evidence:
            raise CapstoneError(
                "NO_SOURCE_LINKS",
                "No exact source links could be created. Manual review is required.",
                422,
            )

        evidence_quotes = {
            item.evidence_id: item.exact_quote for item in evidence
        }
        findings = self._findings(document.text, fields)
        allowed_action_types = _allowed_action_types(findings)
        try:
            draft = self._summary_provider.create_draft(
                fields,
                evidence_quotes,
                allowed_action_types,
            )
        except CapstoneError:
            raise
        except Exception as error:
            raise CapstoneError(
                "MODEL_PROVIDER_FAILED",
                f"Gemini processing stopped safely: {type(error).__name__}.",
                502,
            ) from error
        self._verify_draft(
            draft,
            fields,
            evidence_quotes,
            allowed_action_types,
        )

        state = "needs_review" if findings else "pending_approval"
        proposal_material = {
            "document_sha256": digest,
            "fields": [field.model_dump(mode="json") for field in fields],
            "evidence": [item.model_dump(mode="json") for item in evidence],
            "ai_draft": draft.model_dump(mode="json"),
            "findings": findings,
        }
        proposal_hash = hashlib.sha256(
            _canonical_bytes(proposal_material)
        ).hexdigest()
        created_at = datetime.now(timezone.utc)
        package = DraftPackage(
            schema_version="1.0",
            run_id=f"RUN-{fixture.case_id}-{digest[:12]}",
            case_id=fixture.case_id,
            document_sha256=digest,
            created_at=created_at.isoformat(),
            review_expires_at=(
                created_at
                + timedelta(minutes=self._settings.review_ttl_minutes)
            ).isoformat(),
            page_count=page_count,
            state=state,
            fields=fields,
            evidence=evidence,
            ai_draft=draft,
            findings=findings,
            processing_proof=ProcessingProof(
                synthetic_allowlist_match=True,
                temporary_file_created=temporary_file_created,
                temporary_file_deleted=temporary_file_deleted,
                raw_file_persisted=False,
                provider_mode=self._settings.provider_mode,
                document_ai_location="eu",
                vertex_location="eu",
                model_id=(
                    self._settings.gemini_model
                    if self._settings.provider_mode == "google"
                    else "offline-fake-adapter"
                ),
            ),
            proposal_hash=proposal_hash,
        )
        LOGGER.info(
            "draft_ready case=%s pages=%d state=%s provider=%s",
            fixture.case_id,
            page_count,
            state,
            self._settings.provider_mode,
        )
        return IntakeResponse(
            package=package,
            package_signature=self._sign(package),
        )

    def decide(self, request: ApprovalRequest) -> ApprovalResponse:
        self._verify_signature(request.package, request.package_signature)
        approved = request.decision == "approved"
        if approved:
            try:
                expires_at = datetime.fromisoformat(
                    request.package.review_expires_at
                )
                if expires_at.tzinfo is None:
                    raise ValueError("timezone is required")
            except ValueError as error:
                raise CapstoneError(
                    "INVALID_REVIEW_WINDOW",
                    "The signed review expiry was invalid. Process the document again.",
                    409,
                ) from error
            if datetime.now(timezone.utc) >= expires_at.astimezone(timezone.utc):
                raise CapstoneError(
                    "REVIEW_WINDOW_EXPIRED",
                    "This exact draft expired. Process and review the document again.",
                    409,
                )
            if request.package.state != "pending_approval":
                raise CapstoneError(
                    "PACKAGE_NOT_APPROVABLE",
                    "A package with unresolved findings cannot be exported as approved.",
                    409,
                )
        if not request.source_links_checked:
            raise CapstoneError(
                "SOURCE_REVIEW_REQUIRED",
                "Inspect the source links before recording a decision.",
                422,
            )
        approval = ApprovalRecord(
            decision=request.decision,
            reviewer_alias=request.reviewer_alias,
            proposal_hash=request.package.proposal_hash,
            source_links_checked=True,
            comment=request.comment,
            approved_for_export=approved,
            decided_at=datetime.now(timezone.utc).isoformat(),
        )
        json_export = None
        csv_export = None
        if approved:
            json_export, csv_export = create_exports(request.package, approval)
        LOGGER.info(
            "human_decision case=%s decision=%s export=%s",
            request.package.case_id,
            request.decision,
            approved,
        )
        return ApprovalResponse(
            approval=approval,
            json_export=json_export,
            csv_export=csv_export,
        )
