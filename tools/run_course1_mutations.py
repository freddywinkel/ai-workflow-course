#!/usr/bin/env python3
"""Run Course 1 security mutants in disposable repository copies.

The live checkout is never edited. Each command must pass against the baseline,
then fail for the declared reason after exactly one attributed source mutation.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "quality" / "course1-quality-contract.json"
IGNORED_COPY_NAMES = {
    ".coverage",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".validation",
    "__pycache__",
    "audit-evidence",
    "coverage.json",
    "dist",
    "node_modules",
    "release_evidence",
}


def read_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return value


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def safe_relative_path(raw: Any, label: str) -> Path:
    if not isinstance(raw, str) or not raw or "\\" in raw:
        raise ValueError(f"{label} must be one non-empty POSIX-style relative path")
    path = Path(raw)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{label} escapes the repository")
    return path


def validate_manifest(
    manifest: dict[str, Any],
    *,
    expected_families: list[str],
    expected_manifest_id: str = "course1-security-mutations-v1",
    entry_field: str = "mutants",
    id_pattern: str = r"C1-MUT-[A-Z0-9-]+-[0-9]{3}",
) -> list[dict[str, Any]]:
    if set(manifest) != {"schemaVersion", "manifestId", entry_field}:
        raise ValueError("mutation manifest has unknown or missing top-level keys")
    if manifest["schemaVersion"] != 1:
        raise ValueError("mutation manifest schemaVersion must be 1")
    if manifest["manifestId"] != expected_manifest_id:
        raise ValueError("mutation manifestId is unsupported")
    mutants = manifest[entry_field]
    if not isinstance(mutants, list) or not mutants:
        raise ValueError("mutation manifest mutants must be a non-empty array")

    exact_entry_keys = {
        "id",
        "family",
        "target",
        "find",
        "replace",
        "workingDirectory",
        "command",
        "expectedFailurePattern",
    }
    identifiers: list[str] = []
    families: list[str] = []
    for index, raw in enumerate(mutants):
        label = f"mutants[{index}]"
        if not isinstance(raw, dict) or set(raw) != exact_entry_keys:
            raise ValueError(f"{label} has unknown or missing keys")
        identifier = raw["id"]
        family = raw["family"]
        if not isinstance(identifier, str) or not re.fullmatch(id_pattern, identifier):
            raise ValueError(f"{label}.id is invalid")
        if not isinstance(family, str) or family not in expected_families:
            raise ValueError(f"{label}.family is invalid")
        safe_relative_path(raw["target"], f"{label}.target")
        safe_relative_path(raw["workingDirectory"], f"{label}.workingDirectory")
        if (
            not isinstance(raw["find"], str)
            or not raw["find"]
            or not isinstance(raw["replace"], str)
            or raw["find"] == raw["replace"]
        ):
            raise ValueError(f"{label} must declare one material replacement")
        command = raw["command"]
        if (
            not isinstance(command, list)
            or not command
            or not all(isinstance(value, str) and value for value in command)
        ):
            raise ValueError(f"{label}.command must be a non-empty string array")
        pattern = raw["expectedFailurePattern"]
        if not isinstance(pattern, str) or not pattern:
            raise ValueError(f"{label}.expectedFailurePattern is required")
        re.compile(pattern)
        identifiers.append(identifier)
        families.append(family)

    if len(identifiers) != len(set(identifiers)):
        raise ValueError("mutation identifiers must be unique")
    if sorted(families) != sorted(expected_families):
        raise ValueError(
            "mutation manifest must contain exactly one mutant for every "
            f"required family; observed={sorted(families)}"
        )
    return mutants


def expand_command(
    values: list[str],
    *,
    python: Path,
    node: Path,
) -> list[str]:
    replacements = {
        "{python}": str(python),
        "{node}": str(node),
    }
    expanded: list[str] = []
    for value in values:
        rendered = value
        for token, replacement in replacements.items():
            rendered = rendered.replace(token, replacement)
        if "{" in rendered or "}" in rendered:
            raise ValueError(f"unsupported command placeholder in {value!r}")
        expanded.append(rendered)
    return expanded


def run_command(command: list[str], *, cwd: Path) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=cwd,
        env={
            **os.environ,
            "PYTHONDONTWRITEBYTECODE": "1",
            "EXTERNAL_ACTIONS_ENABLED": "false",
            "COURSE1_DATA_BOUNDARY": "synthetic-only",
        },
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    output = completed.stdout
    return {
        "command": command,
        "cwd": str(cwd),
        "exitCode": completed.returncode,
        "outputSha256": sha256_bytes(output.encode("utf-8")),
        "outputLength": len(output),
        "outputTail": output[-12000:],
    }


def copy_repository(destination: Path) -> None:
    def ignore(_directory: str, names: list[str]) -> set[str]:
        return {name for name in names if name in IGNORED_COPY_NAMES}

    shutil.copytree(ROOT, destination, ignore=ignore)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--node",
        type=Path,
        default=Path(shutil.which("node") or "node"),
        help="exact Node executable used by PWA mutants",
    )
    parser.add_argument(
        "--profile",
        choices=("mutation", "negative"),
        default="mutation",
        help="closed manifest profile; the default is the release mutation suite",
    )
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    failures: list[str] = []
    results: list[dict[str, Any]] = []
    try:
        node = args.node.resolve(strict=True)
        python = Path(sys.executable).resolve(strict=True)
        contract = read_object(CONTRACT_PATH)
        if args.profile == "mutation":
            expected_families = contract["requiredMutationFamilies"]
            default_manifest = ROOT / "quality" / "mutation-manifest.json"
            expected_manifest_id = "course1-security-mutations-v1"
            entry_field = "mutants"
            id_pattern = r"C1-MUT-[A-Z0-9-]+-[0-9]{3}"
        else:
            expected_families = contract["requiredNegativeControlFamilies"]
            default_manifest = ROOT / "quality" / "negative-control-manifest.json"
            expected_manifest_id = "course1-family-negative-controls-v1"
            entry_field = "controls"
            id_pattern = r"C1-NEG-[A-Z0-9-]+-[0-9]{3}"
        manifest_path = (args.manifest or default_manifest).resolve(strict=True)
        if not manifest_path.is_relative_to(ROOT):
            raise ValueError("mutation manifest must be inside the repository")
        manifest = read_object(manifest_path)
        mutants = validate_manifest(
            manifest,
            expected_families=expected_families,
            expected_manifest_id=expected_manifest_id,
            entry_field=entry_field,
            id_pattern=id_pattern,
        )
    except (KeyError, OSError, TypeError, ValueError, re.error) as error:
        failures.append(str(error))
        mutants = []
        node = args.node
        python = Path(sys.executable)

    baseline_cache: dict[str, dict[str, Any]] = {}
    original_hashes: dict[Path, str] = {}
    for mutant in mutants:
        identifier = mutant["id"]
        target_relative = safe_relative_path(mutant["target"], f"{identifier}.target")
        cwd_relative = safe_relative_path(
            mutant["workingDirectory"],
            f"{identifier}.workingDirectory",
        )
        target = ROOT / target_relative
        command = expand_command(mutant["command"], python=python, node=node)
        cache_key = json.dumps(
            {"command": command, "cwd": cwd_relative.as_posix()},
            sort_keys=True,
        )
        if target not in original_hashes:
            original_hashes[target] = sha256_bytes(target.read_bytes())

        baseline = baseline_cache.get(cache_key)
        if baseline is None:
            baseline = run_command(command, cwd=ROOT / cwd_relative)
            baseline_cache[cache_key] = baseline
        record: dict[str, Any] = {
            "id": identifier,
            "family": mutant["family"],
            "target": target_relative.as_posix(),
            "sourceSha256": original_hashes[target],
            "baseline": baseline,
            "mutation": None,
            "result": "FAIL",
        }
        if baseline["exitCode"] != 0:
            failures.append(f"{identifier}: baseline command did not pass")
            results.append(record)
            continue

        try:
            source = target.read_text(encoding="utf-8")
            count = source.count(mutant["find"])
            if count != 1:
                raise ValueError(
                    f"declared source text occurs {count} times instead of exactly once"
                )
            with tempfile.TemporaryDirectory(prefix="c1-mut-") as temporary:
                clone = Path(temporary) / "repo"
                copy_repository(clone)
                clone_target = clone / target_relative
                clone_before = clone_target.read_bytes()
                mutated_text = clone_target.read_text(encoding="utf-8").replace(
                    mutant["find"],
                    mutant["replace"],
                    1,
                )
                clone_target.write_text(
                    mutated_text,
                    encoding="utf-8",
                    newline="\n",
                )
                clone_after = clone_target.read_bytes()
                if clone_before == clone_after:
                    raise ValueError("declared mutation did not change the target")
                execution = run_command(command, cwd=clone / cwd_relative)
                expected_pattern = re.compile(
                    mutant["expectedFailurePattern"],
                    re.IGNORECASE | re.MULTILINE,
                )
                killed = (
                    execution["exitCode"] != 0
                    and expected_pattern.search(execution["outputTail"]) is not None
                )
                record["mutation"] = {
                    "beforeSha256": sha256_bytes(clone_before),
                    "afterSha256": sha256_bytes(clone_after),
                    "execution": execution,
                    "expectedFailurePattern": mutant["expectedFailurePattern"],
                    "attributed": True,
                }
                record["result"] = "PASS" if killed else "FAIL"
                if not killed:
                    failures.append(
                        f"{identifier}: mutant survived or failed for an "
                        "unexpected reason"
                    )
        except (OSError, ValueError) as error:
            failures.append(f"{identifier}: {error}")
        finally:
            if target.is_file() and sha256_bytes(target.read_bytes()) != original_hashes[target]:
                failures.append(f"{identifier}: live source changed during isolated mutation")
                record["result"] = "FAIL"
        results.append(record)

    report = {
        "schemaVersion": 1,
        "manifestId": (
            manifest.get("manifestId") if isinstance(locals().get("manifest"), dict) else None
        ),
        "profile": args.profile,
        "checkedAt": dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "python": str(python),
        "node": str(node),
        "mutationIsolation": "disposable-full-repository-copy",
        "results": results,
        "failures": failures,
        "result": "PASS" if mutants and not failures else "FAIL",
    }
    if args.report:
        destination = args.report.resolve()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
