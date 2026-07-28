from __future__ import annotations

import hashlib
import re
from collections.abc import Iterable

from .schemas import DocumentText, EvidenceLink, ExtractedField, TextSegment


FIELD_PATTERNS: dict[str, tuple[str, ...]] = {
    "supplier_name": (r"(?:Leverancier|Supplier):\s*(.+)",),
    "supplier_code": (r"(?:Leverancierscode|Supplier code):\s*(.+)",),
    "quote_reference": (
        r"(?:Offert\.referentie|Quotation reference):\s*(.+)",
    ),
    "quote_date": (r"(?:Offertedatum|Quotation date):\s*(\d{4}-\d{2}-\d{2})",),
    "valid_until": (
        r"(?:Geldig tot|Valid through):\s*(\d{4}-\d{2}-\d{2}|NIET VERMELD|NOT STATED)",
    ),
    "currency": (r"(?:Valuta|Currency):\s*([A-Z]{3})",),
    "terms_version": (
        r"(?:Voorwaardenversie|Terms version):\s*(.+)",
    ),
    "subtotal_ex_vat": (
        r"(?:Subtotaal excl\. btw|Subtotal ex VAT):\s*(.+)",
    ),
    "net_total_ex_vat": (
        r"(?:Netto excl\. btw|Net ex VAT):\s*(.+)",
    ),
    "vat_amount": (r"(?:Btw|VAT)\s*\([^)]+\):\s*(.+)",),
    "total_inc_vat": (
        r"(?:Totaal incl\. btw|Total inc VAT):\s*(.+)",
    ),
    "payment_days": (
        r"(?:Betalingstermijn|Payment term):\s*(\d+)\s+",
    ),
    "delivery_days": (r"(?:Levertijd|Delivery):\s*(\d+)\s+",),
    "warranty_months": (r"(?:Garantie|Warranty):\s*(\d+)\s+",),
}

MISSING_VALUES = {"NIET VERMELD", "NOT STATED", "NIET AANGELEVERD", "NOT PROVIDED"}


def _segment_for_span(
    segments: Iterable[TextSegment], start: int, end: int
) -> TextSegment | None:
    overlapping = [
        segment
        for segment in segments
        if segment.start_index < end and segment.end_index > start
    ]
    if not overlapping:
        return None
    return min(overlapping, key=lambda item: item.end_index - item.start_index)


def _normalise_quote(value: str) -> str:
    return " ".join(value.replace("\r", "\n").split())


def extract_fields(
    document: DocumentText,
    document_sha256: str,
) -> tuple[list[ExtractedField], list[EvidenceLink]]:
    fields: list[ExtractedField] = []
    evidence: list[EvidenceLink] = []
    evidence_number = 1

    for field_name, patterns in FIELD_PATTERNS.items():
        match = None
        for pattern in patterns:
            match = re.search(pattern, document.text, re.IGNORECASE)
            if match:
                break
        if not match:
            fields.append(
                ExtractedField(
                    field_name=field_name,
                    value=None,
                    status="missing",
                    evidence_ids=[],
                )
            )
            continue

        raw_value = _normalise_quote(match.group(1))
        missing = raw_value.upper() in MISSING_VALUES
        quote = _normalise_quote(match.group(0))
        segment = _segment_for_span(
            document.segments, match.start(0), match.end(0)
        )
        page_number = segment.page_number if segment else 1
        evidence_id = f"EV-P{page_number}-{evidence_number:03d}"
        evidence_number += 1
        evidence.append(
            EvidenceLink(
                evidence_id=evidence_id,
                document_sha256=document_sha256,
                page_number=page_number,
                start_index=match.start(0),
                end_index=match.end(0),
                exact_quote=quote,
                quote_sha256=hashlib.sha256(
                    quote.encode("utf-8")
                ).hexdigest(),
                normalized_bbox=segment.normalized_bbox if segment else None,
            )
        )
        fields.append(
            ExtractedField(
                field_name=field_name,
                value=None if missing else raw_value,
                status="missing" if missing else "verified",
                evidence_ids=[evidence_id],
            )
        )
    return fields, evidence


def verify_evidence(
    document: DocumentText,
    evidence: list[EvidenceLink],
) -> None:
    for link in evidence:
        resolved = _normalise_quote(
            document.text[link.start_index : link.end_index]
        )
        if resolved != link.exact_quote:
            raise ValueError(
                f"{link.evidence_id} does not resolve to its exact source quote."
            )
        digest = hashlib.sha256(resolved.encode("utf-8")).hexdigest()
        if digest != link.quote_sha256:
            raise ValueError(
                f"{link.evidence_id} source quote hash does not match."
            )
