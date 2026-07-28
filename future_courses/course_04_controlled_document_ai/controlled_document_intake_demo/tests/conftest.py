from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

DEMO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = DEMO_ROOT / "src"
COURSE_FOUR_ROOT = DEMO_ROOT.parent
CORPUS_ROOT = COURSE_FOUR_ROOT / "source_material" / "corpus"

sys.path.insert(0, str(SOURCE_ROOT))

from controlled_intake.fixtures import FixtureAllowlist
from controlled_intake.pipeline import ControlledIntakePipeline
from controlled_intake.providers import FakeDocumentProvider, FakeSummaryProvider
from controlled_intake.settings import Settings
from controlled_intake.usage import InMemoryUsageGuard


@pytest.fixture
def settings() -> Settings:
    return Settings(
        provider_mode="fake",
        signing_secret="test-signing-secret-that-is-longer-than-32-characters",
        fixture_manifest_path=DEMO_ROOT / "fixtures" / "manifest.json",
        project_id="",
        document_ai_location="eu",
        document_ai_processor_id="",
        vertex_location="eu",
        gemini_model="gemini-3.5-flash-lite",
        firestore_database="(default)",
        max_file_bytes=5_000_000,
        max_pages_per_document=3,
        max_live_runs=20,
        max_total_pages=60,
        max_gemini_input_characters=24_000,
        max_gemini_output_tokens=800,
        review_ttl_minutes=30,
        live_hard_stop=datetime(2026, 10, 20, tzinfo=timezone.utc),
    )


@pytest.fixture
def pipeline(settings: Settings) -> ControlledIntakePipeline:
    return ControlledIntakePipeline(
        settings,
        FixtureAllowlist(settings.fixture_manifest_path),
        FakeDocumentProvider(),
        FakeSummaryProvider(),
        InMemoryUsageGuard(settings),
    )


@pytest.fixture
def fixture_bytes():
    def load(case_id: str, file_name: str = "quotation.pdf") -> bytes:
        return (CORPUS_ROOT / "cases" / case_id / file_name).read_bytes()

    return load
