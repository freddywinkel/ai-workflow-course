from __future__ import annotations

from fastapi.testclient import TestClient
import pytest

from controlled_intake.errors import CapstoneError
from controlled_intake.main import _parse_content_length, create_app


def test_http_contract_and_security_headers(settings, pipeline, fixture_bytes):
    client = TestClient(create_app(settings, pipeline))

    health = client.get("/api/health")
    assert health.status_code == 200
    assert health.json()["synthetic_only"] is True
    assert health.json()["document_ai_location"] == "eu"
    assert health.json()["vertex_location"] == "eu"
    assert health.headers["cache-control"] == "no-store"
    assert health.headers["content-security-policy"].startswith("default-src")

    unconfirmed = client.post(
        "/api/intake",
        content=fixture_bytes("C001"),
        headers={"Content-Type": "application/pdf"},
    )
    assert unconfirmed.status_code == 422
    assert (
        unconfirmed.json()["error"]["code"]
        == "SYNTHETIC_ACKNOWLEDGEMENT_REQUIRED"
    )

    intake = client.post(
        "/api/intake",
        content=fixture_bytes("C001"),
        headers={
            "Content-Type": "application/pdf",
            "X-Synthetic-Acknowledged": "true",
        },
    )
    assert intake.status_code == 200
    payload = intake.json()
    assert payload["package"]["state"] == "pending_approval"
    assert "json_export" not in payload
    assert "csv_export" not in payload

    decision = client.post(
        "/api/decision",
        json={
            "package": payload["package"],
            "package_signature": payload["package_signature"],
            "decision": "approved",
            "reviewer_alias": "reviewer-demo-01",
            "source_links_checked": True,
            "comment": "Synthetic review.",
        },
    )
    assert decision.status_code == 200
    assert decision.json()["json_export"]
    assert decision.json()["csv_export"]


def test_invalid_reviewer_alias_is_safely_redacted(
    settings, pipeline, fixture_bytes
):
    client = TestClient(create_app(settings, pipeline))
    intake = client.post(
        "/api/intake",
        content=fixture_bytes("C001"),
        headers={
            "Content-Type": "application/pdf",
            "X-Synthetic-Acknowledged": "true",
        },
    ).json()
    response = client.post(
        "/api/decision",
        json={
            "package": intake["package"],
            "package_signature": intake["package_signature"],
            "decision": "approved",
            "reviewer_alias": "A Real Person",
            "source_links_checked": True,
            "comment": "",
        },
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "REQUEST_SCHEMA_REJECTED"
    assert "A Real Person" not in response.text


@pytest.mark.parametrize(
    "values",
    [
        [""],
        ["-1"],
        ["+1"],
        ["1.0"],
        ["1, 1"],
        ["１２"],
        ["1", "1"],
        ["9" * 21],
    ],
)
def test_malformed_content_length_values_are_rejected(values):
    with pytest.raises(CapstoneError) as error:
        _parse_content_length(values)
    assert error.value.code == "INVALID_CONTENT_LENGTH"
    assert error.value.status_code == 400


def test_malformed_content_length_stops_before_pipeline(settings):
    class NeverCallPipeline:
        called = False

        def process(self, *_args):
            self.called = True
            raise AssertionError("pipeline should not be called")

        def decide(self, *_args):
            raise AssertionError("decision should not be called")

    pipeline = NeverCallPipeline()
    client = TestClient(create_app(settings, pipeline))
    response = client.post(
        "/api/intake",
        content=b"%PDF-test",
        headers={
            "Content-Type": "application/pdf",
            "Content-Length": "not-a-number",
            "X-Synthetic-Acknowledged": "true",
        },
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "INVALID_CONTENT_LENGTH"
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["x-content-type-options"] == "nosniff"
    assert pipeline.called is False


def test_declared_oversize_stops_before_pipeline(settings):
    class NeverCallPipeline:
        called = False

        def process(self, *_args):
            self.called = True
            raise AssertionError("pipeline should not be called")

        def decide(self, *_args):
            raise AssertionError("decision should not be called")

    pipeline = NeverCallPipeline()
    client = TestClient(create_app(settings, pipeline))
    response = client.post(
        "/api/intake",
        content=b"",
        headers={
            "Content-Type": "application/pdf",
            "Content-Length": str(settings.max_file_bytes + 1),
            "X-Synthetic-Acknowledged": "true",
        },
    )

    assert response.status_code == 413
    assert response.json()["error"]["code"] == "REQUEST_TOO_LARGE"
    assert pipeline.called is False
