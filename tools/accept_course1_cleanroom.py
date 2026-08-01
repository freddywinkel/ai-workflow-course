#!/usr/bin/env python3
"""Run Course 1's offline workflow in fresh processes and temporary folders."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_command(
    arguments: list[str],
    *,
    root: Path,
    environment: dict[str, str],
) -> str:
    completed = subprocess.run(
        arguments,
        cwd=root,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "Command failed:\n"
            + subprocess.list2cmdline(arguments)
            + "\nSTDOUT:\n"
            + completed.stdout
            + "\nSTDERR:\n"
            + completed.stderr
        )
    return completed.stdout + completed.stderr


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_unittest_inventory(output: str) -> dict[str, str]:
    observed: dict[str, str] = {}
    pattern = re.compile(
        r"^(test_[A-Za-z0-9_]+) \(([^)]+)\) \.\.\. (.+)$",
        re.MULTILINE,
    )
    for match in pattern.finditer(output):
        short_name, test_id, status = match.groups()
        if not test_id.endswith(f".{short_name}"):
            raise RuntimeError(f"Unrecognized unittest identity: {match.group(0)}")
        if test_id in observed:
            raise RuntimeError(f"Duplicate unittest execution: {test_id}")
        observed[test_id] = status.strip()
    if not observed:
        raise RuntimeError("Could not read the named unittest inventory.")
    return observed


def require_exact_test_inventory(
    expected: list[str],
    observed: dict[str, str],
) -> None:
    if expected != sorted(set(expected)):
        raise RuntimeError("Declared unittest manifest must be sorted and unique.")
    missing = sorted(set(expected) - set(observed))
    unexpected = sorted(set(observed) - set(expected))
    non_passing = {
        test_id: status
        for test_id, status in observed.items()
        if status != "ok"
    }
    if missing or unexpected or non_passing:
        raise RuntimeError(
            "Named unittest inventory mismatch: "
            f"missing={missing}, unexpected={unexpected}, non_passing={non_passing}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Clean-room acceptance for the synthetic offline Course 1 runner."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    cli = root / "course1_capstone" / "cli.py"
    source = root / "practice_data" / "work_items.csv"
    expected = root / "practice_data" / "expected_issues.csv"
    test_manifest_path = root / "course1_capstone" / "tests" / "test_manifest.json"
    schemas = sorted((root / "schemas").glob("*.schema.json"))
    runner_files = sorted(
        path
        for path in (root / "course1_capstone").rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    )

    required = [
        Path(__file__).resolve(),
        source,
        expected,
        test_manifest_path,
        *schemas,
        *runner_files,
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        print(json.dumps({"result": "FAIL", "missing": missing}, indent=2))
        return 2

    protected_hashes = {str(path.relative_to(root)): sha256(path) for path in required}
    test_manifest = load_json(test_manifest_path)
    if (
        not isinstance(test_manifest, dict)
        or set(test_manifest) != {"schema_version", "tests"}
        or test_manifest["schema_version"] != "course1-unittest-manifest-v1"
        or not isinstance(test_manifest["tests"], list)
        or not all(isinstance(value, str) for value in test_manifest["tests"])
    ):
        print(
            json.dumps(
                {"result": "FAIL", "error": "Invalid named unittest manifest."},
                indent=2,
            )
        )
        return 2
    expected_tests = test_manifest["tests"]
    environment = os.environ.copy()
    environment.update(
        {
            "PYTHONDONTWRITEBYTECODE": "1",
            "EXTERNAL_ACTIONS_ENABLED": "false",
            "COURSE1_DATA_BOUNDARY": "synthetic-only",
        }
    )

    try:
        with tempfile.TemporaryDirectory(prefix="course1-cleanroom-") as temporary:
            temporary_root = Path(temporary)
            workspace = temporary_root / "learner-project" / "output"

            test_output = run_command(
                [
                    sys.executable,
                    "-m",
                    "unittest",
                    "discover",
                    "-s",
                    "course1_capstone/tests",
                    "-v",
                ],
                root=root,
                environment=environment,
            )
            observed_tests = parse_unittest_inventory(test_output)
            require_exact_test_inventory(expected_tests, observed_tests)
            deliberately_reduced = dict(observed_tests)
            deliberately_reduced.pop(expected_tests[0])
            try:
                require_exact_test_inventory(expected_tests, deliberately_reduced)
            except RuntimeError:
                manifest_negative_control_passed = True
            else:
                raise RuntimeError(
                    "Named unittest manifest negative control did not fail."
                )

            prepare_arguments = [
                sys.executable,
                str(cli),
                "prepare",
                "--input",
                str(source),
                "--expected",
                str(expected),
                "--workspace",
                str(workspace),
                "--ai-mode",
                "mock",
                "--synthetic-confirmation",
                "I_CONFIRM_SYNTHETIC_DATA_ONLY",
            ]
            prepare_output = run_command(
                prepare_arguments,
                root=root,
                environment=environment,
            )
            run_locator = (
                workspace / "latest_run.txt"
            ).read_text(encoding="utf-8").strip()
            run_dir = (workspace / Path(run_locator)).resolve()
            if not run_dir.is_relative_to(temporary_root):
                raise RuntimeError("Runner wrote outside the temporary clean room.")

            decision_output = run_command(
                [
                    sys.executable,
                    str(cli),
                    "decide",
                    "--run-dir",
                    str(run_dir),
                    "--decision",
                    "approve",
                    "--reviewer-role",
                    "cleanroom_reviewer",
                    "--reason",
                    "All synthetic source links and statements were checked.",
                    "--expected-revision",
                    "1",
                    "--evidence-reviewed",
                    "--expires-at",
                    "2099-01-01T00:00:00Z",
                ],
                root=root,
                environment=environment,
            )
            export_arguments = [
                sys.executable,
                str(cli),
                "export",
                "--run-dir",
                str(run_dir),
            ]
            first_export_output = run_command(
                export_arguments,
                root=root,
                environment=environment,
            )
            controlled_retry_paths = [
                run_dir / "source" / "work_items.csv",
                run_dir / "issues" / "issues.json",
                run_dir / "issues" / "issues.csv",
                run_dir / "draft" / "summary.json",
                run_dir / "control.json",
                run_dir / "run_config.json",
                run_dir / "review" / "review_package.json",
                run_dir / "review" / "review_manifest.json",
                run_dir / "review" / "decision-r1.json",
                run_dir / "outbox" / "approved-r1.json",
                run_dir / "outbox" / "approved-r1.csv",
            ]
            controlled_hashes_before_retry = {
                path.relative_to(run_dir).as_posix(): sha256(path)
                for path in controlled_retry_paths
            }
            first_run_config_hash = load_json(
                run_dir / "state.json"
            )["run_config_sha256"]

            # New subprocesses simulate closing and reopening PowerShell.
            retry_prepare_output = run_command(
                prepare_arguments,
                root=root,
                environment=environment,
            )
            retry_export_output = run_command(
                export_arguments,
                root=root,
                environment=environment,
            )
            retry_locator = (
                workspace / "latest_run.txt"
            ).read_text(encoding="utf-8").strip()
            retry_run_dir = (workspace / Path(retry_locator)).resolve()
            controlled_hashes_after_retry = {
                path.relative_to(run_dir).as_posix(): sha256(path)
                for path in controlled_retry_paths
            }
            status_output = run_command(
                [
                    sys.executable,
                    str(cli),
                    "status",
                    "--run-dir",
                    str(run_dir),
                ],
                root=root,
                environment=environment,
            )

            issues = load_json(run_dir / "issues" / "issues.json")
            state = load_json(run_dir / "state.json")
            control = load_json(run_dir / "control.json")
            evaluation = load_json(run_dir / "evaluation.json")
            exported_json = load_json(run_dir / "outbox" / "approved-r1.json")
            with (run_dir / "outbox" / "approved-r1.csv").open(
                "r", encoding="utf-8", newline=""
            ) as stream:
                exported_csv = list(csv.DictReader(stream))
            audit_events = [
                json.loads(line)
                for line in (run_dir / "audit" / "events.jsonl")
                .read_text(encoding="utf-8")
                .splitlines()
                if line.strip()
            ]

            assertions = {
                "unittest_suite_passed": "OK" in test_output,
                "exact_named_unittest_manifest": (
                    sorted(observed_tests) == expected_tests
                    and all(status == "ok" for status in observed_tests.values())
                ),
                "test_manifest_negative_control": manifest_negative_control_passed,
                "prepare_passed": "PASS: prepared controlled run" in prepare_output,
                "decision_passed": "PASS: decision recorded" in decision_output,
                "first_export_passed": "external actions=0" in first_export_output,
                "retry_prepare_same_run": "PASS: prepared controlled run"
                in retry_prepare_output
                and f"RUN_LOCATOR={run_locator}" in retry_prepare_output
                and retry_locator == run_locator
                and retry_run_dir == run_dir,
                "retry_config_hash_unchanged": load_json(
                    run_dir / "state.json"
                )["run_config_sha256"]
                == first_run_config_hash,
                "retry_protected_artifact_hashes_unchanged": (
                    controlled_hashes_after_retry
                    == controlled_hashes_before_retry
                ),
                "retry_export_idempotent": "external actions=0"
                in retry_export_output,
                "status_is_json": load_json_text(status_output)["current_state"]
                == "approved_draft",
                "thirteen_issues": len(issues) == 13,
                "thirteen_csv_exports": len(exported_csv) == 13,
                "thirteen_json_exports": len(exported_json["records"]) == 13,
                "approved_draft_state": state["current_state"] == "approved_draft",
                "two_local_files_only": state["local_export_count"] == 2,
                "zero_external_actions": state["external_actions"] == 0,
                "external_control_false": control["EXTERNAL_ACTIONS_ENABLED"] is False,
                "technical_recommendation_honest": evaluation[
                    "course1_recommendation"
                ]
                == "REWORK",
                "audit_events_parse": len(audit_events) >= 1,
                "all_outputs_inside_cleanroom": all(
                    path.is_relative_to(temporary_root)
                    for path in run_dir.rglob("*")
                ),
            }
            failed_assertions = [
                name for name, passed in assertions.items() if not passed
            ]
            if failed_assertions:
                raise RuntimeError(
                    "Clean-room assertions failed: " + ", ".join(failed_assertions)
                )

            changed_sources = [
                relative
                for relative, original_hash in protected_hashes.items()
                if sha256(root / relative) != original_hash
            ]
            if changed_sources:
                raise RuntimeError(
                    "Acceptance changed protected course sources: "
                    + ", ".join(changed_sources)
                )

            result = {
                "result": "PASS",
                "python": sys.version.split()[0],
                "test_count": len(expected_tests),
                "test_manifest_sha256": sha256(test_manifest_path),
                "clean_process_commands": 7,
                "issue_count": len(issues),
                "local_export_files": 2,
                "external_actions": 0,
                "audit_event_count": len(audit_events),
                "protected_source_files_unchanged": len(protected_hashes),
                "temporary_workspace_removed_on_exit": True,
                "assertions": assertions,
            }
    except Exception as exc:
        print(json.dumps({"result": "FAIL", "error": str(exc)}, indent=2))
        return 1

    rendered = json.dumps(result, indent=2) + "\n"
    if args.report:
        report_path = args.report.resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    return 0


def load_json_text(text: str) -> Any:
    return json.loads(text)


if __name__ == "__main__":
    raise SystemExit(main())
