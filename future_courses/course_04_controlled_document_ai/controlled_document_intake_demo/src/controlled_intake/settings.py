from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


PROTOTYPE_LIVE_HARD_STOP = datetime(
    2026,
    10,
    20,
    tzinfo=timezone.utc,
)
PROTOTYPE_GEMINI_MODEL = "gemini-3.5-flash-lite"
MAX_GEMINI_INPUT_CHARACTERS_CEILING = 24_000
MAX_GEMINI_OUTPUT_TOKENS_CEILING = 800
UNSAFE_SIGNING_SECRETS = {
    "local-synthetic-demo-secret-change-before-cloud-use",
    "replace-with-at-least-32-random-characters",
}


@dataclass(frozen=True)
class Settings:
    provider_mode: str
    signing_secret: str
    fixture_manifest_path: Path
    project_id: str
    document_ai_location: str
    document_ai_processor_id: str
    vertex_location: str
    gemini_model: str
    firestore_database: str
    max_file_bytes: int
    max_pages_per_document: int
    max_live_runs: int
    max_total_pages: int
    max_gemini_input_characters: int
    max_gemini_output_tokens: int
    review_ttl_minutes: int
    live_hard_stop: datetime

    def __post_init__(self) -> None:
        self.validate()

    @classmethod
    def from_env(cls) -> "Settings":
        mode = os.getenv("PROVIDER_MODE", "fake").strip().lower()
        if mode not in {"fake", "google"}:
            raise ValueError("PROVIDER_MODE must be fake or google.")

        secret = os.getenv(
            "APP_SIGNING_SECRET",
            "local-synthetic-demo-secret-change-before-cloud-use",
        )
        if len(secret) < 32:
            raise ValueError("APP_SIGNING_SECRET must contain at least 32 characters.")

        manifest_path = Path(
            os.getenv("FIXTURE_MANIFEST_PATH", "fixtures/manifest.json")
        )
        hard_stop = datetime.fromisoformat(
            os.getenv("LIVE_HARD_STOP", "2026-10-20T00:00:00+00:00")
        )
        if hard_stop.tzinfo is None:
            hard_stop = hard_stop.replace(tzinfo=timezone.utc)

        return cls(
            provider_mode=mode,
            signing_secret=secret,
            fixture_manifest_path=manifest_path,
            project_id=os.getenv("GOOGLE_CLOUD_PROJECT", "").strip(),
            document_ai_location=os.getenv("DOCUMENT_AI_LOCATION", "eu").strip(),
            document_ai_processor_id=os.getenv(
                "DOCUMENT_AI_PROCESSOR_ID", ""
            ).strip(),
            vertex_location=os.getenv("VERTEX_LOCATION", "eu").strip(),
            gemini_model=os.getenv(
                "GEMINI_MODEL", PROTOTYPE_GEMINI_MODEL
            ).strip(),
            firestore_database=os.getenv(
                "FIRESTORE_DATABASE", "(default)"
            ).strip(),
            max_file_bytes=int(os.getenv("MAX_FILE_BYTES", "5000000")),
            max_pages_per_document=int(
                os.getenv("MAX_PAGES_PER_DOCUMENT", "3")
            ),
            max_live_runs=int(os.getenv("MAX_LIVE_RUNS", "20")),
            max_total_pages=int(os.getenv("MAX_TOTAL_PAGES", "60")),
            max_gemini_input_characters=int(
                os.getenv("MAX_GEMINI_INPUT_CHARACTERS", "24000")
            ),
            max_gemini_output_tokens=int(
                os.getenv("MAX_GEMINI_OUTPUT_TOKENS", "800")
            ),
            review_ttl_minutes=int(os.getenv("REVIEW_TTL_MINUTES", "30")),
            live_hard_stop=hard_stop.astimezone(timezone.utc),
        )

    def validate(self) -> None:
        if self.document_ai_location != "eu":
            raise ValueError("DOCUMENT_AI_LOCATION must remain eu for this capstone.")
        if self.vertex_location != "eu":
            raise ValueError("VERTEX_LOCATION must remain eu for this capstone.")
        if self.max_file_bytes > 5_000_000 or self.max_file_bytes < 1:
            raise ValueError("MAX_FILE_BYTES must be between 1 and 5000000.")
        if not 1 <= self.max_pages_per_document <= 3:
            raise ValueError("MAX_PAGES_PER_DOCUMENT must be between 1 and 3.")
        if not 1 <= self.max_live_runs <= 20:
            raise ValueError("MAX_LIVE_RUNS must be between 1 and 20.")
        if not 1 <= self.max_total_pages <= 60:
            raise ValueError("MAX_TOTAL_PAGES must be between 1 and 60.")
        if not 1 <= self.review_ttl_minutes <= 60:
            raise ValueError("REVIEW_TTL_MINUTES must be between 1 and 60.")
        if self.provider_mode == "google":
            if not self.project_id or not self.document_ai_processor_id:
                raise ValueError(
                    "Google mode requires GOOGLE_CLOUD_PROJECT and "
                    "DOCUMENT_AI_PROCESSOR_ID."
                )
            if self.signing_secret in UNSAFE_SIGNING_SECRETS:
                raise ValueError(
                    "Replace the documented signing-secret placeholder before "
                    "using Google mode."
                )
            if self.live_hard_stop != PROTOTYPE_LIVE_HARD_STOP:
                raise ValueError(
                    "Google mode requires the immutable prototype hard stop "
                    "of 20 October 2026."
                )
            if self.gemini_model != PROTOTYPE_GEMINI_MODEL:
                raise ValueError(
                    f"Google mode requires {PROTOTYPE_GEMINI_MODEL}."
                )
            if not (
                1
                <= self.max_gemini_input_characters
                <= MAX_GEMINI_INPUT_CHARACTERS_CEILING
            ):
                raise ValueError(
                    "MAX_GEMINI_INPUT_CHARACTERS must be between 1 and 24000."
                )
            if not (
                1
                <= self.max_gemini_output_tokens
                <= MAX_GEMINI_OUTPUT_TOKENS_CEILING
            ):
                raise ValueError(
                    "MAX_GEMINI_OUTPUT_TOKENS must be between 1 and 800."
                )
