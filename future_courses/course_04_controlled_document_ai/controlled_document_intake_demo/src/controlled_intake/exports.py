from __future__ import annotations

import csv
import io
import json

from .schemas import ApprovalRecord, DraftPackage


def _safe_csv_cell(value: object) -> str:
    text = "" if value is None else str(value)
    first_visible = text.lstrip(" \t\r\n")
    if first_visible.startswith(("=", "+", "-", "@")):
        return "'" + text
    return text


def create_exports(
    package: DraftPackage,
    approval: ApprovalRecord,
) -> tuple[str, str]:
    payload = {
        "schema_version": "1.0",
        "classification": "synthetic training data only",
        "package": package.model_dump(mode="json"),
        "approval": approval.model_dump(mode="json"),
    }
    json_export = json.dumps(
        payload,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"

    evidence_by_id = {item.evidence_id: item for item in package.evidence}
    output = io.StringIO(newline="")
    headers = [
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
    writer = csv.DictWriter(output, fieldnames=headers, lineterminator="\n")
    writer.writeheader()
    for field in package.fields:
        links = [
            evidence_by_id[evidence_id]
            for evidence_id in field.evidence_ids
            if evidence_id in evidence_by_id
        ]
        writer.writerow(
            {
                "run_id": _safe_csv_cell(package.run_id),
                "case_id": _safe_csv_cell(package.case_id),
                "document_sha256": _safe_csv_cell(package.document_sha256),
                "field_name": _safe_csv_cell(field.field_name),
                "value": _safe_csv_cell(field.value),
                "status": _safe_csv_cell(field.status),
                "evidence_ids": _safe_csv_cell(";".join(field.evidence_ids)),
                "source_pages": _safe_csv_cell(
                    ";".join(str(link.page_number) for link in links)
                ),
                "source_quotes": _safe_csv_cell(
                    " | ".join(link.exact_quote for link in links)
                ),
                "proposal_hash": _safe_csv_cell(package.proposal_hash),
                "decision": _safe_csv_cell(approval.decision),
                "reviewer_alias": _safe_csv_cell(approval.reviewer_alias),
                "decided_at": _safe_csv_cell(approval.decided_at),
            }
        )
    return json_export, output.getvalue()
