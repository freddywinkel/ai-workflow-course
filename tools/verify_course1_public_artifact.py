"""Verify that GitHub Pages serves the exact tested Course 1 study artifact."""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from verify_course1_promotion import (
    HEX_40,
    PUBLIC_SERVED_PATHS,
    inspect_artifact_identity,
)


EXPECTED_PUBLIC_PATH = "/ai-workflow-course/"


def public_root(value: str) -> str:
    parsed = urllib.parse.urlsplit(value)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
        or parsed.path != EXPECTED_PUBLIC_PATH
    ):
        raise ValueError(
            "public URL must be one HTTPS origin URL ending in "
            f"{EXPECTED_PUBLIC_PATH}"
        )
    hostname = parsed.hostname.casefold()
    if hostname == "localhost" or hostname.endswith(".localhost"):
        raise ValueError("public URL must not name localhost")
    return value


def selected_bytes_tree_sha256(files: dict[str, bytes]) -> str:
    if set(files) != PUBLIC_SERVED_PATHS:
        raise ValueError("downloaded file set is not the exact public-served set")
    digest = hashlib.sha256()
    for relative in sorted(files):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(files[relative]).digest())
        digest.update(b"\n")
    return digest.hexdigest()


def same_public_target(requested_url: str, final_url: str) -> bool:
    requested = urllib.parse.urlsplit(requested_url)
    final = urllib.parse.urlsplit(final_url)
    return (
        final.scheme == requested.scheme
        and (final.hostname or "").casefold()
        == (requested.hostname or "").casefold()
        and final.port == requested.port
        and final.path == requested.path
        and final.username is None
        and final.password is None
    )


def media_type(value: str | None) -> str:
    return (value or "").split(";", 1)[0].strip().casefold()


def accepted_media_types(expected: str) -> set[str]:
    checked = media_type(expected)
    if not checked:
        raise ValueError("expected media type is empty")
    if checked == "text/javascript":
        return {"text/javascript", "application/javascript"}
    return {checked}


def expected_public_media_types(dist: Path) -> dict[str, set[str]]:
    try:
        manifest = json.loads((dist / "asset-manifest.json").read_text(encoding="utf-8"))
        assets = manifest["assets"]
    except (OSError, UnicodeError, ValueError, KeyError, json.JSONDecodeError) as exc:
        raise ValueError(f"candidate asset manifest media types are invalid: {exc}") from exc
    if not isinstance(assets, dict):
        raise ValueError("candidate asset manifest assets must be one object")

    expected: dict[str, set[str]] = {
        "asset-manifest.json": {"application/json"},
        "sw.js": accepted_media_types("text/javascript"),
    }
    for relative, metadata in assets.items():
        if not isinstance(relative, str) or not isinstance(metadata, dict):
            raise ValueError("candidate asset manifest media metadata is malformed")
        content_type = metadata.get("contentType")
        if not isinstance(content_type, str):
            raise ValueError(f"candidate media type is missing: {relative}")
        expected[relative] = accepted_media_types(content_type)
    if set(expected) != PUBLIC_SERVED_PATHS:
        raise ValueError("candidate media types do not cover the exact public-served set")
    return expected


def fetch_bytes(url: str, *, timeout: float) -> tuple[int, bytes, str, str]:
    request = urllib.request.Request(
        url,
        headers={
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "User-Agent": "Course1PublicArtifactVerifier/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return (
                response.status,
                response.read(),
                response.geturl(),
                media_type(response.headers.get("Content-Type")),
            )
    except urllib.error.HTTPError as exc:
        return (
            exc.code,
            exc.read(),
            exc.geturl(),
            media_type(exc.headers.get("Content-Type") if exc.headers else None),
        )


def verify_once(
    *,
    dist: Path,
    public_url: str,
    expected_commit: str,
    timeout: float,
    cache_nonce: str | None = None,
) -> dict[str, Any]:
    identity = inspect_artifact_identity(
        dist,
        expected_commit=expected_commit,
        operation="personal-study",
    )
    cache_key = urllib.parse.urlencode(
        {
            "course1-release": expected_commit,
            "attempt": cache_nonce or str(time.time_ns()),
        }
    )
    downloaded: dict[str, bytes] = {}
    file_records: list[dict[str, Any]] = []
    failures: list[str] = []
    expected_media_types = expected_public_media_types(dist)

    requested_urls = {
        relative: urllib.parse.urljoin(public_url, relative) + f"?{cache_key}"
        for relative in sorted(PUBLIC_SERVED_PATHS)
    }
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        responses = {
            relative: executor.submit(fetch_bytes, url, timeout=timeout)
            for relative, url in requested_urls.items()
        }
    for relative in sorted(PUBLIC_SERVED_PATHS):
        url = requested_urls[relative]
        status, body, final_url, actual_media_type = responses[relative].result()
        expected = (dist / Path(*relative.split("/"))).read_bytes()
        target_matches = same_public_target(url, final_url)
        allowed_media_types = expected_media_types[relative]
        media_type_matches = actual_media_type in allowed_media_types
        matches = (
            status == 200
            and body == expected
            and target_matches
            and media_type_matches
        )
        file_records.append(
            {
                "path": relative,
                "status": status,
                "contentType": actual_media_type,
                "expectedContentTypes": sorted(allowed_media_types),
                "contentTypeMatches": media_type_matches,
                "sha256": hashlib.sha256(body).hexdigest(),
                "expectedSha256": hashlib.sha256(expected).hexdigest(),
                "byteLength": len(body),
                "matches": matches,
                "targetMatches": target_matches,
                "finalUrl": final_url,
            }
        )
        if not matches:
            failures.append(
                f"{relative} returned status {status}, redirected, did not match the tested bytes, "
                f"or used incompatible media type {actual_media_type or '<missing>'}"
            )
        else:
            downloaded[relative] = body

    nojekyll_url = urllib.parse.urljoin(public_url, ".nojekyll") + f"?{cache_key}"
    nojekyll_status, _, nojekyll_final_url, _ = fetch_bytes(
        nojekyll_url,
        timeout=timeout,
    )
    nojekyll_target_matches = same_public_target(
        nojekyll_url,
        nojekyll_final_url,
    )
    if nojekyll_status != 404 or not nojekyll_target_matches:
        failures.append(
            ".nojekyll must stay on the requested public target and return HTTP 404"
        )

    root_url = f"{public_url}?{cache_key}"
    root_status, root_body, root_final_url, root_media_type = fetch_bytes(
        root_url,
        timeout=timeout,
    )
    root_target_matches = same_public_target(root_url, root_final_url)
    root_matches = (
        root_status == 200
        and root_body == (dist / "index.html").read_bytes()
        and root_target_matches
        and root_media_type == "text/html"
    )
    if not root_matches:
        failures.append(
            "the learner-facing course root redirected or did not serve exact index.html bytes"
        )

    served_hash = None
    if set(downloaded) == PUBLIC_SERVED_PATHS:
        served_hash = selected_bytes_tree_sha256(downloaded)
        if served_hash != identity["publicServedTreeSha256"]:
            failures.append("public-served tree SHA-256 does not match the candidate")

    public_version: dict[str, Any] | None = None
    if "version.json" in downloaded:
        try:
            value = json.loads(downloaded["version.json"].decode("utf-8"))
            if not isinstance(value, dict):
                raise ValueError("version.json is not one object")
            public_version = value
        except (UnicodeError, ValueError, json.JSONDecodeError) as exc:
            failures.append(f"public version.json is invalid: {exc}")
    expected_version = identity["version"]
    if public_version != expected_version:
        failures.append("public version.json does not exactly match the tested candidate")

    return {
        "result": "PASS" if not failures else "FAIL",
        "publicUrl": public_url,
        "expectedCommit": expected_commit,
        "courseVersion": expected_version.get("courseVersion"),
        "productStatus": expected_version.get("productStatus"),
        "distributionPurpose": expected_version.get("distributionPurpose"),
        "buildId": expected_version.get("buildId"),
        "contentHash": expected_version.get("contentHash"),
        "assetManifestSha256": identity["assetManifestSha256"],
        "artifactTreeSha256": identity["artifactTreeSha256"],
        "publicServedTreeSha256": served_hash,
        "expectedPublicServedTreeSha256": identity["publicServedTreeSha256"],
        "publicFiles": file_records,
        "learnerFacingRoot": {
            "status": root_status,
            "contentType": root_media_type,
            "expectedContentTypes": ["text/html"],
            "matchesIndexHtml": root_matches,
            "targetMatches": root_target_matches,
            "finalUrl": root_final_url,
        },
        "nonPublicArtifactFiles": [
            {
                "path": ".nojekyll",
                "expectedPublicStatus": 404,
                "actualPublicStatus": nojekyll_status,
                "targetMatches": nojekyll_target_matches,
                "finalUrl": nojekyll_final_url,
            }
        ],
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare the deployed Course 1 Pages bytes with one tested artifact"
    )
    parser.add_argument("--dist", type=Path, required=True)
    parser.add_argument("--public-url", required=True)
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--attempts", type=int, default=12)
    parser.add_argument("--delay-seconds", type=float, default=10.0)
    parser.add_argument("--timeout-seconds", type=float, default=20.0)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    failures: list[str] = []
    expected_commit = args.expected_commit.strip().casefold()
    if not HEX_40.fullmatch(expected_commit):
        failures.append("expected commit must be a full lower-case 40-character Git SHA")
    if args.attempts < 1 or args.attempts > 30:
        failures.append("attempts must be between 1 and 30")
    if args.delay_seconds < 0 or args.delay_seconds > 30:
        failures.append("delay-seconds must be between 0 and 30")
    if args.timeout_seconds <= 0 or args.timeout_seconds > 60:
        failures.append("timeout-seconds must be greater than 0 and at most 60")
    try:
        checked_public_url = public_root(args.public_url.strip())
    except ValueError as exc:
        checked_public_url = args.public_url.strip()
        failures.append(str(exc))

    result: dict[str, Any] = {
        "result": "FAIL",
        "publicUrl": checked_public_url,
        "expectedCommit": expected_commit,
        "failures": failures,
    }
    if not failures:
        last_error: str | None = None
        for attempt in range(1, args.attempts + 1):
            try:
                candidate = verify_once(
                    dist=args.dist.resolve(),
                    public_url=checked_public_url,
                    expected_commit=expected_commit,
                    timeout=args.timeout_seconds,
                    cache_nonce=f"{attempt}-{time.time_ns()}",
                )
                candidate["attempt"] = attempt
                result = candidate
                if candidate["result"] == "PASS":
                    break
                last_error = "; ".join(candidate["failures"])
            except (OSError, ValueError, KeyError, urllib.error.URLError) as exc:
                last_error = str(exc)
                result = {
                    "result": "FAIL",
                    "publicUrl": checked_public_url,
                    "expectedCommit": expected_commit,
                    "attempt": attempt,
                    "failures": [last_error],
                }
            if attempt < args.attempts:
                time.sleep(args.delay_seconds)
        if result["result"] != "PASS" and last_error:
            result["lastFailure"] = last_error

    result["verifiedAt"] = dt.datetime.now(dt.timezone.utc).isoformat()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.report:
        destination = args.report.resolve()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    return 0 if result.get("result") == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
