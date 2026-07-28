from __future__ import annotations

import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def require(name: str, expected: str) -> None:
    if os.getenv(name) != expected:
        raise SystemExit(f"{name} must equal {expected!r}.")


def request_json(
    base_url: str,
    path: str,
    *,
    method: str = "GET",
    body: bytes | None = None,
    headers: dict[str, str] | None = None,
) -> tuple[int, dict]:
    merged_headers = dict(headers or {})
    auth_token = os.getenv("CONTROLLED_INTAKE_AUTH_TOKEN", "")
    if auth_token:
        merged_headers["Authorization"] = f"Bearer {auth_token}"
    request = urllib.request.Request(
        base_url + path,
        data=body,
        method=method,
        headers=merged_headers,
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        payload = json.loads(error.read().decode("utf-8"))
        return error.code, payload


def main() -> int:
    require("ALLOW_LIVE_GOOGLE_TESTS", "YES")
    require("FREE_TRIAL_CONFIRMED", "YES")
    require("PAID_BILLING_ACTIVATED", "NO")
    require("CLOUD_RUN_PRIVATE_IAM_CONFIRMED", "YES")
    unauthenticated_status = int(
        os.getenv("CLOUD_RUN_UNAUTHENTICATED_STATUS", "0")
    )
    if unauthenticated_status not in {401, 403}:
        raise SystemExit(
            "CLOUD_RUN_UNAUTHENTICATED_STATUS must be 401 or 403."
        )
    if not os.getenv("CONTROLLED_INTAKE_AUTH_TOKEN"):
        raise SystemExit("CONTROLLED_INTAKE_AUTH_TOKEN must contain a short-lived token.")

    base_url = os.getenv("CONTROLLED_INTAKE_BASE_URL", "http://127.0.0.1:8088")
    demo_root = Path(__file__).resolve().parents[1]
    corpus_root = demo_root.parent / "source_material" / "corpus"
    evidence_root = demo_root / "evidence"
    evidence_root.mkdir(exist_ok=True)

    status, health = request_json(base_url, "/api/health")
    if status != 200 or health.get("provider_mode") != "google":
        raise AssertionError(f"Google provider health check failed: {status} {health}")
    if health.get("document_ai_location") != "eu":
        raise AssertionError("Document AI location is not eu.")
    if health.get("vertex_location") != "eu":
        raise AssertionError("Vertex location is not eu.")
    if health.get("gemini_model") != "gemini-3.5-flash-lite":
        raise AssertionError("The validated Gemini model is not the configured GA model.")

    cases = [
        ("C001", "quotation.pdf", "pending_approval"),
        ("C004", "quotation_scan.pdf", "pending_approval"),
        ("C008", "quotation.pdf", "needs_review"),
        ("C012", "quotation.pdf", "needs_review"),
    ]
    observed: list[dict] = []
    approved_hashes: dict[str, object] | None = None
    decision_controls: dict[str, object] = {}

    for case_id, file_name, expected_state in cases:
        content = (corpus_root / "cases" / case_id / file_name).read_bytes()
        status, payload = request_json(
            base_url,
            "/api/intake",
            method="POST",
            body=content,
            headers={
                "Content-Type": "application/pdf",
                "X-Synthetic-Acknowledged": "true",
            },
        )
        if status != 200:
            raise AssertionError(f"{case_id} intake failed: {status} {payload}")
        package = payload["package"]
        if package["state"] != expected_state:
            raise AssertionError(
                f"{case_id} state {package['state']} != {expected_state}"
            )
        proof = package["processing_proof"]
        if not proof["temporary_file_deleted"] or proof["raw_file_persisted"]:
            raise AssertionError(f"{case_id} deletion proof failed.")
        if not package["evidence"] or not all(
            statement["evidence_ids"]
            for statement in package["ai_draft"]["summary"]
        ):
            raise AssertionError(f"{case_id} lacks source-linked output.")

        observed.append(
            {
                "case_id": case_id,
                "state": package["state"],
                "page_count": package["page_count"],
                "field_count": len(package["fields"]),
                "evidence_count": len(package["evidence"]),
                "finding_codes": [
                    finding.split(":", 1)[0] for finding in package["findings"]
                ],
                "temporary_file_deleted": proof["temporary_file_deleted"],
                "raw_file_persisted": proof["raw_file_persisted"],
                "provider_mode": proof["provider_mode"],
                "model_id": proof["model_id"],
            }
        )

        if case_id == "C001":
            decision_body = json.dumps(
                {
                    "package": package,
                    "package_signature": payload["package_signature"],
                    "decision": "approved",
                    "reviewer_alias": "reviewer-demo-01",
                    "source_links_checked": True,
                    "comment": "Live synthetic capstone acceptance.",
                }
            ).encode("utf-8")
            decision_status, decision = request_json(
                base_url,
                "/api/decision",
                method="POST",
                body=decision_body,
                headers={"Content-Type": "application/json"},
            )
            if decision_status != 200:
                raise AssertionError(f"Approval failed: {decision_status} {decision}")
            json_bytes = decision["json_export"].encode("utf-8")
            csv_bytes = decision["csv_export"].encode("utf-8")
            approved_hashes = {
                "proposal_hash": package["proposal_hash"],
                "json_sha256": hashlib.sha256(json_bytes).hexdigest(),
                "json_bytes": len(json_bytes),
                "csv_sha256": hashlib.sha256(csv_bytes).hexdigest(),
                "csv_bytes": len(csv_bytes),
                "approved_for_export": decision["approval"]["approved_for_export"],
            }

            changed_package = json.loads(json.dumps(package))
            changed_package["page_count"] += 1
            changed_body = json.dumps(
                {
                    "package": changed_package,
                    "package_signature": payload["package_signature"],
                    "decision": "approved",
                    "reviewer_alias": "reviewer-demo-01",
                    "source_links_checked": True,
                    "comment": "Mutation must stop.",
                }
            ).encode("utf-8")
            changed_status, changed_result = request_json(
                base_url,
                "/api/decision",
                method="POST",
                body=changed_body,
                headers={"Content-Type": "application/json"},
            )
            changed_code = changed_result.get("error", {}).get("code")
            if (
                changed_status != 409
                or changed_code != "PACKAGE_CHANGED_AFTER_REVIEW"
            ):
                raise AssertionError("A changed review package was not invalidated.")
            decision_controls["changed_package"] = changed_code

        if case_id == "C008":
            blocked_approval_body = json.dumps(
                {
                    "package": package,
                    "package_signature": payload["package_signature"],
                    "decision": "approved",
                    "reviewer_alias": "reviewer-demo-01",
                    "source_links_checked": True,
                    "comment": "Unresolved findings must block export.",
                }
            ).encode("utf-8")
            blocked_status, blocked_result = request_json(
                base_url,
                "/api/decision",
                method="POST",
                body=blocked_approval_body,
                headers={"Content-Type": "application/json"},
            )
            blocked_code = blocked_result.get("error", {}).get("code")
            if blocked_status != 409 or blocked_code != "PACKAGE_NOT_APPROVABLE":
                raise AssertionError("A findings package was not blocked from export.")

            correction_body = json.dumps(
                {
                    "package": package,
                    "package_signature": payload["package_signature"],
                    "decision": "needs_correction",
                    "reviewer_alias": "reviewer-demo-01",
                    "source_links_checked": True,
                    "comment": "Synthetic live validation.",
                }
            ).encode("utf-8")
            correction_status, correction = request_json(
                base_url,
                "/api/decision",
                method="POST",
                body=correction_body,
                headers={"Content-Type": "application/json"},
            )
            if (
                correction_status != 200
                or correction.get("json_export") is not None
                or correction.get("csv_export") is not None
                or correction.get("approval", {}).get("approved_for_export")
            ):
                raise AssertionError("Needs-correction decision exposed an export.")
            decision_controls["findings_approval"] = blocked_code
            decision_controls["needs_correction_export"] = False

    corrupt = (
        corpus_root / "cases" / "C010" / "quotation_corrupt.pdf"
    ).read_bytes()
    corrupt_status, corrupt_payload = request_json(
        base_url,
        "/api/intake",
        method="POST",
        body=corrupt,
        headers={
            "Content-Type": "application/pdf",
            "X-Synthetic-Acknowledged": "true",
        },
    )
    if (
        corrupt_status != 422
        or corrupt_payload.get("error", {}).get("code") != "PARSER_CORRUPT_FILE"
    ):
        raise AssertionError("The corrupt fixture did not stop safely.")

    unknown = (
        corpus_root / "cases" / "C001" / "quotation.pdf"
    ).read_bytes() + b"\n"
    unknown_status, unknown_payload = request_json(
        base_url,
        "/api/intake",
        method="POST",
        body=unknown,
        headers={
            "Content-Type": "application/pdf",
            "X-Synthetic-Acknowledged": "true",
        },
    )
    if (
        unknown_status != 422
        or unknown_payload.get("error", {}).get("code")
        != "SYNTHETIC_ALLOWLIST_REJECTED"
    ):
        raise AssertionError("The unknown hash did not stop before providers.")

    report = {
        "schema_version": 1,
        "result": "PASS",
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "data_boundary": "frozen synthetic PDF fixtures only",
        "service": {
            "provider_mode": health["provider_mode"],
            "document_ai_location": health["document_ai_location"],
            "vertex_location": health["vertex_location"],
            "model": health["gemini_model"],
            "raw_document_storage": health["raw_document_storage"],
        },
        "private_access": {
            "public_iam_members_absent": True,
            "unauthenticated_http_status": unauthenticated_status,
        },
        "cases": observed,
        "approved_export_evidence": approved_hashes,
        "decision_controls": decision_controls,
        "negative_tests": {
            "corrupt_fixture": "PARSER_CORRUPT_FILE",
            "unknown_hash": "SYNTHETIC_ALLOWLIST_REJECTED",
        },
        "contains_document_text": False,
        "contains_model_output": False,
        "contains_credentials": False,
    }
    output = evidence_root / "live_validation.json"
    output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"result": "PASS", "report": str(output)}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
