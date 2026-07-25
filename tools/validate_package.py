#!/usr/bin/env python3
"""Validate the static course package and generated synthetic corpus.

This script performs deterministic structural checks. It does not claim that
external links, legal statements, model behaviour, or visual rendering are
current/correct; those require the evergreen live audit and render review.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import unquote


REQUIRED_WEEK_HEADINGS = (
    "## Outcome",
    "## Concepts",
    "## Official readings",
    "## Guided build",
    "## Capstone increment",
    "## Required artifact",
    "## Test gate",
    "## Common failures",
    "## Estimated time",
)

REQUIRED_ROOT_FILES = (
    "README.md",
    "BEGINNER_READINESS_CHECK.md",
    "COURSE_OVERVIEW.md",
    "SOFTWARE_MATRIX.md",
    "SETUP_WINDOWS.md",
    "ARCHITECTURE_AND_CONTRACTS.md",
    "CAPSTONE_SPECIFICATION.md",
    "ASSESSMENT_AND_RUBRIC.md",
    "SOURCE_REGISTER.md",
    "COURSE_CHANGELOG.md",
    "EVERGREEN_UPDATE_PROMPT.md",
    "PWA_AND_UPDATES.md",
    "RELEASE_VALIDATION.md",
    "stack-manifest.yaml",
    "requirements-course.txt",
    "schemas/contracts.schema.json",
    "schemas/golden_case.schema.json",
    "corpus/README.md",
    "corpus/manifest.jsonl",
    "corpus/golden.jsonl",
    "updates/README.md",
    "foundations/README.md",
    "foundations/01_FILES_AND_TEXT.md",
    "foundations/02_COMMAND_LINE_SURVIVAL.md",
    "foundations/03_CODE_AND_PYTHON.md",
    "foundations/04_WEB_APIS_AND_JSON.md",
    "foundations/05_GIT_AND_SAFE_CHANGES.md",
    "foundations/06_AI_AND_DOCUMENT_WORKFLOWS.md",
    "foundations/07_SAFE_VIBE_CODING.md",
    "foundations/08_N8N_DOCKER_AND_DATABASES.md",
    "foundations/GLOSSARY.md",
    "templates/ai_assistance_log.md",
    "templates/debugging_record.md",
    "tools/requirements-validation.txt",
)

STATE_ENUM = {
    "received",
    "validated",
    "parsed",
    "needs_review",
    "pending_approval",
    "approved",
    "rejected",
    "expired",
    "completed",
    "failed_manual",
}

MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
IGNORED_DIRECTORY_NAMES = {
    ".git",
    ".pytest_cache",
    ".validation-deps",
    "__pycache__",
    "dist",
    "node_modules",
}


@dataclass
class Report:
    checks: list[dict[str, str]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def passed(self, name: str, detail: str) -> None:
        self.checks.append({"status": "PASS", "name": name, "detail": detail})

    def failed(self, name: str, detail: str) -> None:
        self.checks.append({"status": "FAIL", "name": name, "detail": detail})
        self.errors.append(f"{name}: {detail}")

    def warn(self, name: str, detail: str) -> None:
        self.checks.append({"status": "WARN", "name": name, "detail": detail})
        self.warnings.append(f"{name}: {detail}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_number}: JSONL row is not an object")
        rows.append(value)
    return rows


def iter_course_files(root: Path, suffix: str) -> list[Path]:
    """Return course files while pruning generated/dependency directories."""

    matches: list[Path] = []
    for current_root, directory_names, file_names in os.walk(root):
        directory_names[:] = [
            name for name in directory_names if name not in IGNORED_DIRECTORY_NAMES
        ]
        for file_name in file_names:
            if file_name.endswith(suffix):
                matches.append(Path(current_root) / file_name)
    return sorted(matches)


def validate_required_files(root: Path, report: Report) -> None:
    missing = [name for name in REQUIRED_ROOT_FILES if not (root / name).is_file()]
    if missing:
        report.failed("required-files", f"missing: {', '.join(missing)}")
    else:
        report.passed("required-files", f"{len(REQUIRED_ROOT_FILES)} required files present")


def validate_weeks(root: Path, report: Report) -> None:
    week_files = sorted((root / "weeks").glob("WEEK_*.md"))
    expected_names = [f"WEEK_{number:02d}.md" for number in range(1, 13)]
    actual_names = [path.name for path in week_files]
    if actual_names != expected_names:
        report.failed("week-count-and-names", f"expected {expected_names}; found {actual_names}")
        return
    report.passed("week-count-and-names", "exactly WEEK_01.md through WEEK_12.md")

    failures: list[str] = []
    for path in week_files:
        text = path.read_text(encoding="utf-8")
        positions = [text.find(heading) for heading in REQUIRED_WEEK_HEADINGS]
        missing = [
            heading for heading, position in zip(REQUIRED_WEEK_HEADINGS, positions) if position < 0
        ]
        if missing:
            failures.append(f"{path.name} missing {missing}")
        elif positions != sorted(positions):
            failures.append(f"{path.name} headings are out of order")
    if failures:
        report.failed("week-structure", "; ".join(failures))
    else:
        report.passed("week-structure", "all nine required headings appear in order")


def validate_machine_files(root: Path, report: Report) -> None:
    json_files = iter_course_files(root, ".json")
    failures: list[str] = []
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # precise path retained in report
            failures.append(f"{path.relative_to(root)}: {exc}")
    if failures:
        report.failed("json-parse", "; ".join(failures))
    else:
        report.passed("json-parse", f"{len(json_files)} JSON files parsed")

    jsonl_files = iter_course_files(root, ".jsonl")
    failures = []
    row_count = 0
    for path in jsonl_files:
        try:
            row_count += len(load_jsonl(path))
        except Exception as exc:
            failures.append(str(exc))
    if failures:
        report.failed("jsonl-parse", "; ".join(failures))
    else:
        report.passed("jsonl-parse", f"{len(jsonl_files)} JSONL files / {row_count} rows parsed")

    try:
        import yaml  # type: ignore

        yaml.safe_load((root / "stack-manifest.yaml").read_text(encoding="utf-8"))
        report.passed("yaml-parse", "stack-manifest.yaml parsed")
    except ModuleNotFoundError:
        report.warn("yaml-parse", "PyYAML unavailable; YAML parse not run")
    except Exception as exc:
        report.failed("yaml-parse", str(exc))

    try:
        import jsonschema  # type: ignore

        for relative in ("schemas/contracts.schema.json", "schemas/golden_case.schema.json"):
            schema = json.loads((root / relative).read_text(encoding="utf-8"))
            jsonschema.Draft202012Validator.check_schema(schema)
        report.passed("json-schema-meta-validation", "both schemas valid under Draft 2020-12")

        golden_schema = json.loads(
            (root / "schemas/golden_case.schema.json").read_text(encoding="utf-8")
        )
        golden_rows = load_jsonl(root / "corpus/golden.jsonl")
        validator = jsonschema.Draft202012Validator(
            golden_schema,
            format_checker=jsonschema.FormatChecker(),
        )
        instance_errors: list[str] = []
        for row in golden_rows:
            errors = sorted(validator.iter_errors(row), key=lambda error: list(error.path))
            for error in errors:
                location = ".".join(str(part) for part in error.path) or "<root>"
                instance_errors.append(f"{row.get('case_id')}:{location}: {error.message}")
        if instance_errors:
            report.failed("golden-schema-validation", "; ".join(instance_errors))
        else:
            report.passed(
                "golden-schema-validation",
                f"{len(golden_rows)} golden rows validate against the course schema",
            )
    except ModuleNotFoundError:
        report.warn("json-schema-meta-validation", "jsonschema unavailable; meta-validation not run")
    except Exception as exc:
        report.failed("json-schema-meta-validation", str(exc))


def clean_link_target(raw: str) -> str | None:
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    if target.startswith(("http://", "https://", "mailto:", "#")):
        return None
    target = target.split("#", 1)[0].split("?", 1)[0]
    return unquote(target) if target else None


def validate_internal_links(root: Path, report: Report) -> None:
    missing: list[str] = []
    checked = 0
    for markdown in iter_course_files(root, ".md"):
        text = markdown.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK_RE.finditer(text):
            target = clean_link_target(match.group(1))
            if target is None:
                continue
            checked += 1
            resolved = (markdown.parent / target).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                missing.append(f"{markdown.relative_to(root)} -> escapes root: {target}")
                continue
            if not resolved.exists():
                missing.append(f"{markdown.relative_to(root)} -> {target}")
    if missing:
        report.failed("internal-links", "; ".join(missing))
    else:
        report.passed("internal-links", f"{checked} local targets exist")


def case_id(row: dict[str, Any]) -> str | None:
    return row.get("case_id") or row.get("id")


def validate_corpus(root: Path, report: Report) -> None:
    corpus = root / "corpus"
    manifest_path = corpus / "manifest.jsonl"
    golden_path = corpus / "golden.jsonl"
    if not manifest_path.exists() or not golden_path.exists():
        report.failed("corpus", "manifest.jsonl or golden.jsonl missing")
        return

    try:
        manifest = load_jsonl(manifest_path)
        golden = load_jsonl(golden_path)
    except Exception as exc:
        report.failed("corpus-jsonl", str(exc))
        return

    manifest_ids = [case_id(row) for row in manifest]
    golden_ids = [case_id(row) for row in golden]
    expected = [f"C{number:03d}" for number in range(1, 21)]
    if manifest_ids != expected or golden_ids != expected:
        report.failed(
            "corpus-case-set",
            f"expected ordered {expected}; manifest={manifest_ids}; golden={golden_ids}",
        )
    else:
        report.passed("corpus-case-set", "20 ordered unique cases agree")

    state_failures = []
    for row in manifest + golden:
        state = row.get("expected_checkpoint_state")
        if state not in STATE_ENUM:
            state_failures.append(f"{case_id(row)}:{state}")
    if state_failures:
        report.failed("corpus-states", ", ".join(state_failures))
    else:
        report.passed("corpus-states", "all manifest/gold checkpoint states are named states")

    file_failures: list[str] = []
    files_checked = 0
    file_by_document_id: dict[str, Path] = {}
    for row in manifest:
        for item in row.get("files", []):
            relative = item.get("relative_path")
            if not relative:
                file_failures.append(f"{case_id(row)} file lacks relative_path")
                continue
            path = corpus / relative
            if not path.is_file():
                file_failures.append(f"missing {relative}")
                continue
            files_checked += 1
            actual_hash = sha256_file(path)
            actual_size = path.stat().st_size
            if item.get("sha256") != actual_hash:
                file_failures.append(f"{relative} sha256 mismatch")
            expected_size = item.get("byte_length", item.get("byte_size"))
            if expected_size is not None and expected_size != actual_size:
                file_failures.append(f"{relative} byte length mismatch")
            document_id = item.get("fixture_document_id") or item.get("document_id")
            if document_id:
                file_by_document_id[document_id] = path
    if file_failures:
        report.failed("corpus-file-integrity", "; ".join(file_failures))
    else:
        report.passed("corpus-file-integrity", f"{files_checked} referenced files match metadata")

    by_case = {case_id(row): row for row in manifest}
    try:
        c001 = by_case["C001"]
        c009 = by_case["C009"]
        for role in ("quotation", "terms"):
            one = next(item for item in c001["files"] if item["role"] == role)
            nine = next(item for item in c009["files"] if item["role"] == role)
            one_path = corpus / one["relative_path"]
            nine_path = corpus / nine["relative_path"]
            if one_path.read_bytes() != nine_path.read_bytes():
                raise AssertionError(f"{role} bytes differ")
            if nine.get("duplicate_of_fixture_document_id") not in (
                one.get("fixture_document_id"),
                one.get("document_id"),
            ):
                raise AssertionError(f"{role} duplicate reference is wrong")
        report.passed("corpus-C009-duplicate", "quotation and terms are byte-identical to C001")
    except Exception as exc:
        report.failed("corpus-C009-duplicate", str(exc))

    try:
        c010 = by_case["C010"]
        quote = next(item for item in c010["files"] if item["role"] == "quotation")
        path = corpus / quote["relative_path"]
        expected_bytes = b"NOT_A_PDF\nSYNTHETIC_CASE=C010\n"
        if path.read_bytes() != expected_bytes:
            raise AssertionError(f"unexpected bytes: {path.read_bytes()!r}")
        report.passed("corpus-C010-corrupt", "exact specified corrupt bytes")
    except Exception as exc:
        report.failed("corpus-C010-corrupt", str(exc))

    safety_failures = []
    for row in manifest:
        safety = row.get("safety", {})
        if safety.get("synthetic") is not True:
            safety_failures.append(f"{case_id(row)} not marked synthetic")
        for key in (
            "contains_personal_data",
            "contains_special_category_data",
            "contains_real_organisation_data",
        ):
            if safety.get(key) is not False:
                safety_failures.append(f"{case_id(row)} {key} is not false")
    if safety_failures:
        report.failed("corpus-safety-flags", "; ".join(safety_failures))
    else:
        report.passed("corpus-safety-flags", "all cases carry strict synthetic/no-data flags")

    checksum_path = corpus / "checksums.sha256"
    checksum_failures: list[str] = []
    checksum_count = 0
    if not checksum_path.is_file():
        checksum_failures.append("checksums.sha256 missing")
    else:
        for line_number, line in enumerate(
            checksum_path.read_text(encoding="utf-8").splitlines(), 1
        ):
            if not line.strip():
                continue
            match = re.fullmatch(r"([a-f0-9]{64})  (.+)", line)
            if not match:
                checksum_failures.append(f"line {line_number} malformed")
                continue
            expected_hash, relative = match.groups()
            path = corpus / relative
            if not path.is_file():
                checksum_failures.append(f"missing {relative}")
                continue
            checksum_count += 1
            if sha256_file(path) != expected_hash:
                checksum_failures.append(f"{relative} hash mismatch")
    if checksum_failures:
        report.failed("corpus-checksum-file", "; ".join(checksum_failures))
    else:
        report.passed("corpus-checksum-file", f"{checksum_count} checksum entries verified")


def write_report(root: Path, report: Report, output: Path) -> None:
    lines = [
        "# Package Validation Report",
        "",
        "Course root: repository root (`.`)  ",
        f"Result: **{'PASS' if not report.errors else 'FAIL'}**  ",
        f"Checks: {len(report.checks)}; failures: {len(report.errors)}; warnings: {len(report.warnings)}",
        "",
        "| Status | Check | Detail |",
        "|---|---|---|",
    ]
    for check in report.checks:
        detail = check["detail"].replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {check['status']} | {check['name']} | {detail} |")
    lines.extend(
        [
            "",
            "This is deterministic structural validation only. External-source currency and visual quality require the live audit and render review.",
            "",
        ]
    )
    output.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Course package root",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help="Markdown report path (default: <root>/VALIDATION_REPORT.md)",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    output = (args.report or (root / "VALIDATION_REPORT.md")).resolve()

    report = Report()
    validate_required_files(root, report)
    validate_weeks(root, report)
    validate_machine_files(root, report)
    validate_internal_links(root, report)
    validate_corpus(root, report)
    write_report(root, report, output)

    summary = {
        "result": "PASS" if not report.errors else "FAIL",
        "checks": len(report.checks),
        "failures": report.errors,
        "warnings": report.warnings,
        "report": str(output),
    }
    print(json.dumps(summary, indent=2))
    return 0 if not report.errors else 1


if __name__ == "__main__":
    sys.exit(main())
