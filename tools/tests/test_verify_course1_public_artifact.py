from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
import urllib.parse
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from verify_course1_promotion import PUBLIC_SERVED_PATHS  # noqa: E402
from verify_course1_public_artifact import (  # noqa: E402
    public_root,
    selected_bytes_tree_sha256,
    verify_once,
)


class PublicArtifactVerifierTests(unittest.TestCase):
    COMMIT = "a" * 40

    def test_public_url_is_exact_https_course_scope(self) -> None:
        value = "https://example.github.io/ai-workflow-course/"
        self.assertEqual(public_root(value), value)
        for invalid in (
            "http://example.github.io/ai-workflow-course/",
            "https://localhost/ai-workflow-course/",
            "https://example.github.io/other/",
            "https://user@example.github.io/ai-workflow-course/",
            "https://example.github.io/ai-workflow-course/?trust=true",
        ):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    public_root(invalid)

    def test_public_tree_requires_the_exact_served_set(self) -> None:
        files = {
            relative: f"synthetic {relative}\n".encode("utf-8")
            for relative in PUBLIC_SERVED_PATHS
        }
        digest = hashlib.sha256()
        for relative in sorted(files):
            digest.update(relative.encode("utf-8"))
            digest.update(b"\0")
            digest.update(hashlib.sha256(files[relative]).digest())
            digest.update(b"\n")
        self.assertEqual(selected_bytes_tree_sha256(files), digest.hexdigest())
        files.pop(next(iter(files)))
        with self.assertRaisesRegex(ValueError, "exact public-served set"):
            selected_bytes_tree_sha256(files)

    def test_live_comparison_accepts_exact_bytes_and_expected_nojekyll_404(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            dist = Path(temporary)
            file_bytes: dict[str, bytes] = {}
            for relative in PUBLIC_SERVED_PATHS:
                path = dist / Path(*relative.split("/"))
                path.parent.mkdir(parents=True, exist_ok=True)
                body = f"synthetic {relative}\n".encode("utf-8")
                path.write_bytes(body)
                file_bytes[relative] = body
            version = {
                "courseVersion": "2.6.0",
                "productStatus": "UNVERIFIED",
                "distributionPurpose": "personal-synthetic-study",
                "buildId": "123456789abc",
            }
            import json

            file_bytes["version.json"] = (
                json.dumps(version, sort_keys=True) + "\n"
            ).encode("utf-8")
            (dist / "version.json").write_bytes(file_bytes["version.json"])
            served_hash = selected_bytes_tree_sha256(file_bytes)
            identity = {
                "version": version,
                "assetManifestSha256": "b" * 64,
                "artifactTreeSha256": "c" * 64,
                "publicServedTreeSha256": served_hash,
            }

            def fake_fetch(url: str, *, timeout: float) -> tuple[int, bytes, str]:
                self.assertGreater(timeout, 0)
                path = urllib.parse.urlsplit(url).path
                relative = path.removeprefix("/ai-workflow-course/")
                if relative == "":
                    return 200, file_bytes["index.html"], url
                if relative == ".nojekyll":
                    return 404, b"not found", url
                return 200, file_bytes[relative], url

            with (
                patch(
                    "verify_course1_public_artifact.inspect_artifact_identity",
                    return_value=identity,
                ),
                patch(
                    "verify_course1_public_artifact.fetch_bytes",
                    side_effect=fake_fetch,
                ),
            ):
                result = verify_once(
                    dist=dist,
                    public_url="https://example.github.io/ai-workflow-course/",
                    expected_commit=self.COMMIT,
                    timeout=1,
                )
            self.assertEqual(result["result"], "PASS")
            self.assertEqual(result["publicServedTreeSha256"], served_hash)
            self.assertEqual(
                result["nonPublicArtifactFiles"][0]["actualPublicStatus"],
                404,
            )

            def mismatched_fetch(
                url: str,
                *,
                timeout: float,
            ) -> tuple[int, bytes, str]:
                status, body, final_url = fake_fetch(url, timeout=timeout)
                if urllib.parse.urlsplit(url).path.endswith("/app.js"):
                    body = b"mismatched public bytes\n"
                return status, body, final_url

            with (
                patch(
                    "verify_course1_public_artifact.inspect_artifact_identity",
                    return_value=identity,
                ),
                patch(
                    "verify_course1_public_artifact.fetch_bytes",
                    side_effect=mismatched_fetch,
                ),
            ):
                mismatch = verify_once(
                    dist=dist,
                    public_url="https://example.github.io/ai-workflow-course/",
                    expected_commit=self.COMMIT,
                    timeout=1,
                )
            self.assertEqual(mismatch["result"], "FAIL")
            self.assertTrue(any("app.js" in item for item in mismatch["failures"]))

            def exposed_nojekyll_fetch(
                url: str,
                *,
                timeout: float,
            ) -> tuple[int, bytes, str]:
                status, body, final_url = fake_fetch(url, timeout=timeout)
                if urllib.parse.urlsplit(url).path.endswith("/.nojekyll"):
                    return 200, b"", final_url
                return status, body, final_url

            with (
                patch(
                    "verify_course1_public_artifact.inspect_artifact_identity",
                    return_value=identity,
                ),
                patch(
                    "verify_course1_public_artifact.fetch_bytes",
                    side_effect=exposed_nojekyll_fetch,
                ),
            ):
                exposed = verify_once(
                    dist=dist,
                    public_url="https://example.github.io/ai-workflow-course/",
                    expected_commit=self.COMMIT,
                    timeout=1,
                )
            self.assertEqual(exposed["result"], "FAIL")
            self.assertTrue(any(".nojekyll" in item for item in exposed["failures"]))

            def redirected_fetch(
                url: str,
                *,
                timeout: float,
            ) -> tuple[int, bytes, str]:
                status, body, final_url = fake_fetch(url, timeout=timeout)
                if urllib.parse.urlsplit(url).path.endswith("/app.js"):
                    final_url = "https://redirect.invalid/ai-workflow-course/app.js"
                return status, body, final_url

            with (
                patch(
                    "verify_course1_public_artifact.inspect_artifact_identity",
                    return_value=identity,
                ),
                patch(
                    "verify_course1_public_artifact.fetch_bytes",
                    side_effect=redirected_fetch,
                ),
            ):
                redirected = verify_once(
                    dist=dist,
                    public_url="https://example.github.io/ai-workflow-course/",
                    expected_commit=self.COMMIT,
                    timeout=1,
                )
            self.assertEqual(redirected["result"], "FAIL")
            self.assertTrue(
                any("redirected" in item for item in redirected["failures"])
            )


if __name__ == "__main__":
    unittest.main()
