"""Beginner-facing command line for the offline Course 1 capstone."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from .workflow import (
        AI_MODES,
        DECISIONS,
        SYNTHETIC_CONFIRMATION,
        SafeStop,
        append_audit_event,
        export_approved,
        inspect_run,
        parse_datetime,
        prepare_run,
        read_json,
        record_decision,
        revise_draft,
        utc_now,
        validate_candidate_summary,
        write_json,
    )
except ImportError:
    from workflow import (  # type: ignore[no-redef]
        AI_MODES,
        DECISIONS,
        SYNTHETIC_CONFIRMATION,
        SafeStop,
        append_audit_event,
        export_approved,
        inspect_run,
        parse_datetime,
        prepare_run,
        read_json,
        record_decision,
        revise_draft,
        utc_now,
        validate_candidate_summary,
        write_json,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Offline synthetic Course 1 workflow. It has no external-action "
            "capability."
        )
    )
    commands = parser.add_subparsers(dest="command", required=True)

    prepare = commands.add_parser(
        "prepare",
        help="Validate input and create issues, summary, review package, and evaluation.",
    )
    prepare.add_argument("--input", type=Path, required=True)
    prepare.add_argument("--workspace", type=Path, required=True)
    prepare.add_argument("--expected", type=Path)
    prepare.add_argument("--ai-mode", choices=sorted(AI_MODES), default="mock")
    prepare.add_argument(
        "--synthetic-confirmation",
        required=True,
        help=f"Must be exactly {SYNTHETIC_CONFIRMATION}.",
    )

    decide = commands.add_parser(
        "decide",
        help="Record approve, edit, reject, or expire for one exact draft revision.",
    )
    decide.add_argument("--run-dir", type=Path, required=True)
    decide.add_argument("--decision", choices=sorted(DECISIONS), required=True)
    decide.add_argument("--reviewer-role", required=True)
    decide.add_argument("--reason", required=True)
    decide.add_argument("--expected-revision", type=int, required=True)
    decide.add_argument("--evidence-reviewed", action="store_true")
    decide.add_argument("--expires-at")
    decide.add_argument("--decided-at")

    revise = commands.add_parser(
        "revise",
        help="Install a validated replacement after an edit decision.",
    )
    revise.add_argument("--run-dir", type=Path, required=True)
    revise.add_argument("--replacement", type=Path, required=True)
    revise.add_argument("--expected-revision", type=int, required=True)

    validate = commands.add_parser(
        "validate-summary",
        help="Validate a learner-created offline mock without replacing the run draft.",
    )
    validate.add_argument("--run-dir", type=Path, required=True)
    validate.add_argument("--candidate", type=Path, required=True)

    export = commands.add_parser(
        "export",
        help="Create idempotent local CSV and JSON only after valid approval.",
    )
    export.add_argument("--run-dir", type=Path, required=True)
    export.add_argument("--checked-at")

    status = commands.add_parser("status", help="Show the controlled run status.")
    status.add_argument("--run-dir", type=Path, required=True)
    return parser


def command_artifact_base(args: argparse.Namespace) -> Path | None:
    if args.command == "prepare":
        return args.workspace.resolve()
    if hasattr(args, "run_dir"):
        return args.run_dir.resolve()
    return None


def relative_artifact_locator(path: Path, base: Path) -> str:
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError as error:
        raise SafeStop(
            "output_path_escape",
            "A generated artifact escaped its controlled output folder.",
        ) from error


def record_safe_stop(args: argparse.Namespace, error: SafeStop) -> Path | None:
    base = command_artifact_base(args)
    if base is None:
        return None
    failure_path = base / "failures" / f"safe-stop-{error.code}.json"
    write_json(
        failure_path,
        {
            "state": "failed_manual",
            "error_code": error.code,
            "message": str(error),
            "command": args.command,
            "occurred_at": utc_now().isoformat().replace("+00:00", "Z"),
            "external_actions": 0,
        },
    )
    state_path = base / "state.json"
    if state_path.exists():
        state = read_json(state_path)
        if state.get("run_id"):
            append_audit_event(
                base,
                state["run_id"],
                "safe_stop_recorded",
                "failed_manual",
                "system",
                {
                    "error_code": error.code,
                    "command": args.command,
                    "external_actions": 0,
                },
            )
    return failure_path


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            run_dir = prepare_run(
                args.input,
                args.workspace,
                args.ai_mode,
                args.synthetic_confirmation,
                args.expected,
            )
            print(
                "PASS: prepared controlled run.\n"
                f"RUN_ID={run_dir.name}\n"
                "RUN_LOCATOR="
                f"{relative_artifact_locator(run_dir, args.workspace.resolve())}"
            )
        elif args.command == "decide":
            decision_path = record_decision(
                args.run_dir,
                args.decision,
                args.reviewer_role,
                args.reason,
                args.expected_revision,
                args.evidence_reviewed,
                (
                    parse_datetime(args.expires_at, "expires_at")
                    if args.expires_at
                    else None
                ),
                (
                    parse_datetime(args.decided_at, "decided_at")
                    if args.decided_at
                    else None
                ),
            )
            print(
                "PASS: decision recorded.\n"
                "DECISION="
                f"{relative_artifact_locator(decision_path, args.run_dir.resolve())}"
            )
        elif args.command == "revise":
            revision = revise_draft(
                args.run_dir,
                args.replacement,
                args.expected_revision,
            )
            print(f"PASS: draft revision {revision} now requires a new review.")
        elif args.command == "export":
            json_path, csv_path = export_approved(
                args.run_dir,
                (
                    parse_datetime(args.checked_at, "checked_at")
                    if args.checked_at
                    else None
                ),
            )
            print(
                "PASS: local draft exports created; external actions=0.\n"
                "JSON="
                f"{relative_artifact_locator(json_path, args.run_dir.resolve())}\n"
                "CSV="
                f"{relative_artifact_locator(csv_path, args.run_dir.resolve())}"
            )
        elif args.command == "validate-summary":
            result_path = validate_candidate_summary(
                args.run_dir,
                args.candidate,
            )
            print(
                "PASS: structure and issue references are valid; human support "
                "review is still required.\nRESULT="
                f"{relative_artifact_locator(result_path, args.run_dir.resolve())}"
            )
        else:
            print(json.dumps(inspect_run(args.run_dir), indent=2))
        return 0
    except SafeStop as error:
        print(f"SAFE STOP: {error}")
        failure_path = record_safe_stop(args, error)
        if failure_path is not None:
            base = command_artifact_base(args)
            if base is None:
                print("FAILURE_EVIDENCE=unavailable")
            else:
                print(
                    "FAILURE_EVIDENCE="
                    f"{relative_artifact_locator(failure_path, base)}"
                )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
