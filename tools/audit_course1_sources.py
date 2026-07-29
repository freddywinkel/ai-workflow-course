"""Validate Course 1 claim-to-source ownership, freshness, and availability."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CLAIMS_PATH = ROOT / "source_claims.json"
REGISTER_PATH = ROOT / "SOURCE_REGISTER.md"
ID_PATTERN = re.compile(r"^SRC-[A-Z0-9]+-[0-9]{3}$")
MARKDOWN_URL_PATTERN = re.compile(r"\[[^\]]+\]\((https://[^)]+)\)")
ALLOWED_CATEGORIES = {
    "legal-guidance",
    "market",
    "security-guidance",
    "software",
    "standard",
    "vendor",
}
ALLOWED_CHECKS = {"get", "manual-browser"}


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain one JSON object")
    return value


def parse_date(value: Any, field: str) -> dt.date:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be an ISO date")
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field} must be an ISO date") from exc


def check_url(url: str) -> tuple[int, str]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "text/html,application/pdf,application/json;q=0.9,*/*;q=0.8",
            "User-Agent": "course1-source-audit/1",
        },
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        response.read(1)
        return int(response.status), response.geturl()


def write_report(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--online",
        action="store_true",
        help="also request sources configured for automated checking",
    )
    parser.add_argument(
        "--as-of",
        type=dt.date.fromisoformat,
        default=dt.date.today(),
        help="freshness date in YYYY-MM-DD format",
    )
    parser.add_argument("--report", type=Path, default=None)
    args = parser.parse_args()

    failures: list[str] = []
    checks: list[dict[str, Any]] = []
    manual_review_required: list[str] = []
    try:
        claims = read_json(CLAIMS_PATH)
        entries = claims.get("entries")
        if not isinstance(entries, list) or not entries:
            raise ValueError("source_claims.json has no entries")

        register_urls = MARKDOWN_URL_PATTERN.findall(
            REGISTER_PATH.read_text(encoding="utf-8")
        )
        register_counter = Counter(register_urls)
        duplicate_register_urls = sorted(
            url for url, count in register_counter.items() if count != 1
        )
        if duplicate_register_urls:
            failures.append(
                "SOURCE_REGISTER.md must contain each external source once: "
                f"{duplicate_register_urls}"
            )

        ids: set[str] = set()
        manifest_urls: list[str] = []
        last_verified_dates: list[dt.date] = []
        for entry in entries:
            if not isinstance(entry, dict):
                failures.append("source manifest contains a non-object entry")
                continue
            claim_id = entry.get("id")
            if not isinstance(claim_id, str) or not ID_PATTERN.fullmatch(claim_id):
                failures.append(f"invalid source claim ID: {claim_id!r}")
                continue
            if claim_id in ids:
                failures.append(f"duplicate source claim ID: {claim_id}")
                continue
            ids.add(claim_id)

            category = entry.get("category")
            if category not in ALLOWED_CATEGORIES:
                failures.append(f"{claim_id} has invalid category {category!r}")
            url = entry.get("url")
            if not isinstance(url, str) or not url.startswith("https://"):
                failures.append(f"{claim_id} must use one HTTPS source URL")
                continue
            manifest_urls.append(url)

            for field in ("topic", "locator", "courseUse", "owner"):
                if not isinstance(entry.get(field), str) or not entry[field].strip():
                    failures.append(f"{claim_id}.{field} must be non-empty")
            triggers = entry.get("reviewTriggers")
            if (
                not isinstance(triggers, list)
                or not triggers
                or any(not isinstance(item, str) or not item.strip() for item in triggers)
            ):
                failures.append(f"{claim_id}.reviewTriggers must be non-empty text")
            automated_check = entry.get("automatedCheck")
            if automated_check not in ALLOWED_CHECKS:
                failures.append(
                    f"{claim_id} has invalid automatedCheck {automated_check!r}"
                )

            try:
                last_verified = parse_date(
                    entry.get("lastVerified"), f"{claim_id}.lastVerified"
                )
                last_verified_dates.append(last_verified)
                max_age = entry.get("maxAgeDays")
                if not isinstance(max_age, int) or not 1 <= max_age <= 365:
                    raise ValueError(f"{claim_id}.maxAgeDays must be 1..365")
                age_days = (args.as_of - last_verified).days
                if age_days < 0:
                    failures.append(f"{claim_id} is verified in the future")
                elif age_days > max_age:
                    failures.append(
                        f"{claim_id} is stale: {age_days} days exceeds {max_age}"
                    )
            except ValueError as exc:
                failures.append(str(exc))

            check_result: dict[str, Any] = {
                "id": claim_id,
                "url": url,
                "mode": automated_check,
                "result": "NOT_RUN",
            }
            if args.online and automated_check == "get":
                try:
                    status, final_url = check_url(url)
                    if not 200 <= status < 400:
                        raise ValueError(f"HTTP {status}")
                    check_result.update(
                        {"result": "PASS", "status": status, "finalUrl": final_url}
                    )
                except (OSError, ValueError, urllib.error.HTTPError) as exc:
                    check_result.update({"result": "UNVERIFIED", "error": str(exc)})
                    failures.append(f"{claim_id} could not be opened: {exc}")
            elif args.online:
                check_result["result"] = "MANUAL_CURRENT_DATE_REQUIRED"
                manual_review_required.append(claim_id)
            checks.append(check_result)

        manifest_counter = Counter(manifest_urls)
        duplicate_manifest_urls = sorted(
            url for url, count in manifest_counter.items() if count != 1
        )
        if duplicate_manifest_urls:
            failures.append(
                "source_claims.json must contain each URL once: "
                f"{duplicate_manifest_urls}"
            )
        if set(register_counter) != set(manifest_counter):
            missing_from_manifest = sorted(set(register_counter) - set(manifest_counter))
            missing_from_register = sorted(set(manifest_counter) - set(register_counter))
            failures.append(
                "source register and claim manifest differ; "
                f"missing from manifest={missing_from_manifest}; "
                f"missing from register={missing_from_register}"
            )

        verified_through = parse_date(
            claims.get("verifiedThrough"), "verifiedThrough"
        )
        if last_verified_dates and verified_through != min(last_verified_dates):
            failures.append(
                "verifiedThrough must equal the oldest entry lastVerified date"
            )
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        failures.append(str(exc))

    result = "FAIL" if failures else (
        "PASS_WITH_MANUAL_REVIEW_REQUIRED"
        if args.online and manual_review_required
        else "PASS"
    )
    report = {
        "schemaVersion": 1,
        "checkedAt": dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "asOf": args.as_of.isoformat(),
        "onlineChecksPerformed": bool(args.online),
        "result": result,
        "manualReviewRequiredIds": manual_review_required,
        "checks": checks,
        "failures": failures,
    }
    if args.report:
        write_report(args.report.resolve(), report)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
