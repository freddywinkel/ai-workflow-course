from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .errors import CapstoneError
from .schemas import FixtureRecord


class FixtureAllowlist:
    def __init__(self, manifest_path: Path):
        try:
            payload = json.loads(manifest_path.read_text(encoding="utf-8"))
            records = payload["allowed_documents"]
        except (OSError, KeyError, json.JSONDecodeError) as error:
            raise RuntimeError(
                f"Could not read synthetic fixture manifest: {error}"
            ) from error
        self._records = {
            item.sha256: item
            for item in (FixtureRecord.model_validate(record) for record in records)
        }

    def match(self, content: bytes) -> tuple[str, FixtureRecord]:
        digest = hashlib.sha256(content).hexdigest()
        record = self._records.get(digest)
        if record is None:
            raise CapstoneError(
                "SYNTHETIC_ALLOWLIST_REJECTED",
                "This file is not one of the frozen synthetic course documents. "
                "Document AI, Gemini, and the Firestore usage counter were not "
                "called.",
                422,
            )
        if len(content) != record.byte_length:
            raise CapstoneError(
                "FIXTURE_LENGTH_MISMATCH",
                "The file hash matched but its recorded byte length did not.",
                422,
            )
        return digest, record
