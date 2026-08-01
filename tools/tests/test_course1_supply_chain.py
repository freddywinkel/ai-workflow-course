from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from audit_course1_supply_chain import (  # noqa: E402
    compare_requirement_hashes,
    parse_requirements,
    read_json,
    validate_offline,
)


VALID_HASH_A = "a" * 64
VALID_HASH_B = "b" * 64


def write_requirement_file(directory: Path, body: str) -> Path:
    path = directory / "requirements.txt"
    path.write_text(body, encoding="utf-8", newline="\n")
    return path


class SupplyChainLockTests(unittest.TestCase):
    def test_current_offline_supply_contract_passes(self) -> None:
        manifest = read_json(ROOT / "supply_chain" / "course1-dependencies.json")
        failures, inventory = validate_offline(manifest)
        self.assertEqual(failures, [])
        self.assertGreater(len(inventory), 0)

    def test_hash_required_options_and_complete_pin_parse(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = write_requirement_file(
                Path(temp_dir),
                "\n".join(
                    [
                        "--index-url=https://pypi.org/simple",
                        "--only-binary=:all:",
                        "--require-hashes",
                        "",
                        "Example==1.2.3 \\",
                        f"  --hash=sha256:{VALID_HASH_A} \\",
                        f"  --hash=sha256:{VALID_HASH_B}",
                        "",
                    ]
                ),
            )
            self.assertEqual(
                parse_requirements(path),
                {
                    "example": {
                        "version": "1.2.3",
                        "hashes": [VALID_HASH_A, VALID_HASH_B],
                    }
                },
            )

    def test_missing_require_hashes_option_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = write_requirement_file(
                Path(temp_dir),
                "\n".join(
                    [
                        "--index-url=https://pypi.org/simple",
                        "--only-binary=:all:",
                        "",
                        "Example==1.2.3 \\",
                        f"  --hash=sha256:{VALID_HASH_A}",
                        "",
                    ]
                ),
            )
            with self.assertRaisesRegex(ValueError, "must contain exactly"):
                parse_requirements(path)

    def test_duplicate_or_unsupported_hash_syntax_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            duplicate = write_requirement_file(
                Path(temp_dir),
                "\n".join(
                    [
                        "--index-url=https://pypi.org/simple",
                        "--only-binary=:all:",
                        "--require-hashes",
                        "",
                        "Example==1.2.3 \\",
                        f"  --hash=sha256:{VALID_HASH_A} \\",
                        f"  --hash=sha256:{VALID_HASH_A}",
                        "",
                    ]
                ),
            )
            with self.assertRaisesRegex(ValueError, "repeats a SHA-256"):
                parse_requirements(duplicate)

    def test_altered_or_missing_artifact_hash_is_rejected(self) -> None:
        pins = {
            "example": {
                "version": "1.2.3",
                "hashes": [VALID_HASH_A, VALID_HASH_B],
            }
        }
        locked = {
            "example": {
                "artifacts": [
                    {"sha256": VALID_HASH_A},
                    {"sha256": "c" * 64},
                ]
            }
        }
        failures = compare_requirement_hashes(pins, locked)
        self.assertEqual(
            failures,
            [
                "hashes differ from the complete artifact lock for "
                "example==1.2.3"
            ],
        )


if __name__ == "__main__":
    unittest.main()
