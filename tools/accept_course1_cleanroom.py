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
    schemas = sorted((root / "schemas").glob("*.schema.json"))

    required = [cli, source, expected, *schemas]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        print(json.dumps({"result": "FAIL", "missing": missing}, indent=2))
        return 2

    protected_hashes = {str(path.relative_to(root)): sha256(path) for path in required}
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
                    "--decided-at",
                    "2026-07-28T10:00:00Z",
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
                "--checked-at",
                "2026-07-28T10:01:00Z",
            ]
            first_export_output = run_command(
                export_arguments,
                root=root,
                environment=environment,
            )

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
                "prepare_passed": "PASS: prepared controlled run" in prepare_output,
                "decision_passed": "PASS: decision recorded" in decision_output,
                "first_export_passed": "external actions=0" in first_export_output,
                "retry_prepare_same_run": "PASS: prepared controlled run"
                in retry_prepare_output,
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

            test_count_match = re.search(r"Ran (\d+) tests?", test_output)
            if test_count_match is None:
                raise RuntimeError("Could not read the unittest test count.")
            result = {
                "result": "PASS",
                "python": sys.version.split()[0],
                "test_count": int(test_count_match.group(1)),
                "clean_process_commands": 6,
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
