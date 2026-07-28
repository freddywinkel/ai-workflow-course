from __future__ import annotations

import threading
from datetime import datetime, timezone
from typing import Protocol

from .errors import CapstoneError
from .settings import PROTOTYPE_LIVE_HARD_STOP, Settings


class UsageGuard(Protocol):
    def reserve(self, pages: int) -> dict[str, int]: ...


def _assert_within_limits(
    runs: int,
    pages: int,
    requested_pages: int,
    settings: Settings,
    *,
    enforce_live_hard_stop: bool,
    now: datetime | None = None,
) -> tuple[int, int]:
    active_now = now or datetime.now(timezone.utc)
    if enforce_live_hard_stop and active_now >= PROTOTYPE_LIVE_HARD_STOP:
        raise CapstoneError(
            "LIVE_HARD_STOP_REACHED",
            "New live provider calls stopped on 20 October 2026. Teardown is required.",
            403,
        )
    next_runs = runs + 1
    next_pages = pages + requested_pages
    if next_runs > settings.max_live_runs or next_pages > settings.max_total_pages:
        raise CapstoneError(
            "PROTOTYPE_USAGE_CAP_REACHED",
            "The fixed prototype run or page allowance is exhausted.",
            429,
        )
    return next_runs, next_pages


class InMemoryUsageGuard:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._runs = 0
        self._pages = 0
        self._lock = threading.Lock()

    def reserve(self, pages: int) -> dict[str, int]:
        with self._lock:
            self._runs, self._pages = _assert_within_limits(
                self._runs,
                self._pages,
                pages,
                self._settings,
                enforce_live_hard_stop=False,
            )
            return {"runs": self._runs, "pages": self._pages}


class FirestoreUsageGuard:
    """Stores counts only. No filename, hash, text, prompt, or result is stored."""

    def __init__(self, settings: Settings):
        from google.cloud import firestore

        self._settings = settings
        self._client = firestore.Client(
            project=settings.project_id,
            database=settings.firestore_database,
        )
        self._reference = self._client.collection(
            "controlled_intake_control"
        ).document("prototype_usage")

    def reserve(self, pages: int) -> dict[str, int]:
        from google.cloud import firestore

        transaction = self._client.transaction()

        @firestore.transactional
        def reserve_in_transaction(active_transaction):
            snapshot = self._reference.get(transaction=active_transaction)
            current = snapshot.to_dict() if snapshot.exists else {}
            runs, total_pages = _assert_within_limits(
                int(current.get("runs", 0)),
                int(current.get("pages", 0)),
                pages,
                self._settings,
                enforce_live_hard_stop=True,
            )
            active_transaction.set(
                self._reference,
                {
                    "runs": runs,
                    "pages": total_pages,
                    "limit_runs": self._settings.max_live_runs,
                    "limit_pages": self._settings.max_total_pages,
                    "updated_at": firestore.SERVER_TIMESTAMP,
                },
            )
            return {"runs": runs, "pages": total_pages}

        return reserve_in_transaction(transaction)


def build_usage_guard(settings: Settings) -> UsageGuard:
    if settings.provider_mode == "google":
        return FirestoreUsageGuard(settings)
    return InMemoryUsageGuard(settings)
