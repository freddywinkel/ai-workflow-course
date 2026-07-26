#!/usr/bin/env python3
"""Deterministically validate the current Course 1 package.

The curriculum manifest is the source of truth for the current course. Archived
future-course material and generated/dependency directories are intentionally
outside this validator's scope.

Only the Python standard library is required. When jsonschema or PyYAML is not
installed, the related optional checks are reported as warnings rather than
silently skipped.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path, PurePosixPath
from typing import Any, Iterable
from urllib.parse import unquote


EXPECTED_PROGRAM_ID = "controlled-ai-workflow-consultant-path"
EXPECTED_COURSE_ID = "course-1-controlled-ai-workflow-foundations"
EXPECTED_SCHEMA_VERSION = 2
FIXED_ASSESSMENT_DATE_TEXT = "2026-07-26"
FIXED_ASSESSMENT_DATE = date.fromisoformat(FIXED_ASSESSMENT_DATE_TEXT)

STABLE_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REVISION_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
WORK_ITEM_ID_RE = re.compile(r"^WI-\d{4}$")
SOURCE_REFERENCE_RE = re.compile(r"^REF-\d{4}$")

REQUIRED_MODULE_HEADINGS = (
    "## Outcome",
    "## Beginner checkpoint",
    "## Concepts",
    "## Official readings",
    "## Guided build",
    "## Consultant lens",
    "## Capstone increment",
    "## Required artifact",
    "## Test gate",
    "## Stop or rework",
    "## Common failures",
    "## Estimated time",
)

REQUIRED_PRACTICE_HEADINGS = (
    "## Follow along — I show you exactly how",
    "## Now recreate it yourself",
    "## Ask Codex to check your work",
    "## Pass criteria",
)

REQUIRED_ONBOARDING_PHRASES = {
    "README.md": (
        "Artificial Intelligence (AI)",
        "Small and Medium-sized Enterprises (SMEs)",
        "progressive web app (PWA)",
        "comma-separated values (CSV)",
        "application programming interfaces (APIs)",
        "user acceptance testing (UAT)",
        "Git is the name of a version-control tool",
    ),
    "BEGINNER_READINESS_CHECK.md": (
        "application programming interface (API)",
        "JavaScript Object Notation (JSON)",
        "artificial intelligence (AI)",
        "progressive web app (PWA)",
        "comma-separated values (CSV)",
        "identifier (ID)",
    ),
    "SETUP_WINDOWS.md": (
        "artificial intelligence (AI)",
        "Small and Medium-sized Enterprise (SME)",
        "comma-separated values (CSV)",
        "application programming interface (API)",
        "Long-Term Support (LTS)",
    ),
}

EXPECTED_SCHEMA_FILES = {
    "approval.schema.json",
    "audit_event.schema.json",
    "issue.schema.json",
    "summary.schema.json",
    "work_item.schema.json",
}

WORK_ITEM_FIELDS = (
    "work_item_id",
    "source_reference",
    "title",
    "owner_role",
    "status",
    "priority",
    "received_date",
    "due_date",
    "completed_date",
    "amount",
    "currency",
    "category",
)

EXPECTED_ISSUE_FIELDS = (
    "issue_id",
    "work_item_id",
    "field",
    "rule_code",
    "severity",
    "expected_message",
)

RULE_CODES = {f"R{number:03d}" for number in range(1, 12)}
ALLOWED_STATUSES = {"new", "in_progress", "waiting", "completed", "cancelled"}
OPEN_STATUSES = {"new", "in_progress", "waiting"}
OWNER_REQUIRED_STATUSES = {"in_progress", "waiting", "completed"}
ALLOWED_PRIORITIES = {"low", "medium", "high"}
ALLOWED_SEVERITIES = {"low", "medium", "high"}
REQUIRED_VALUE_FIELDS = (
    "work_item_id",
    "source_reference",
    "title",
    "received_date",
    "category",
)
DATE_FIELDS = ("received_date", "due_date", "completed_date")

IGNORED_DIRECTORY_NAMES = {
    ".git",
    ".pytest_cache",
    ".validation-deps",
    "__pycache__",
    "dist",
    "node_modules",
}
IGNORED_TOP_LEVEL_DIRECTORIES = {"future_courses"}

FENCED_CODE_RE = re.compile(r"```.*?```|~~~.*?~~~", re.DOTALL)
INLINE_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REFERENCE_LINK_RE = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.MULTILINE)


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


def compact(items: Iterable[str], limit: int = 12) -> str:
    values = [str(item) for item in items]
    if len(values) <= limit:
        return "; ".join(values)
    return "; ".join(values[:limit]) + f"; ... and {len(values) - limit} more"


def is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def valid_revision(value: Any) -> bool:
    if not isinstance(value, str) or not REVISION_RE.fullmatch(value):
        return False
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def path_is_ignored(relative: Path) -> bool:
    parts = relative.parts
    if not parts:
        return False
    if parts[0] in IGNORED_TOP_LEVEL_DIRECTORIES:
        return True
    return any(part in IGNORED_DIRECTORY_NAMES for part in parts)


def iter_current_files(root: Path, suffix: str) -> list[Path]:
    """Return in-scope files while pruning archives, generated files, and deps."""

    matches: list[Path] = []
    for current_root, directory_names, file_names in os.walk(root):
        current = Path(current_root)
        retained: list[str] = []
        for directory_name in directory_names:
            relative = (current / directory_name).relative_to(root)
            if not path_is_ignored(relative):
                retained.append(directory_name)
        directory_names[:] = retained

        for file_name in file_names:
            if file_name.endswith(suffix):
                matches.append(current / file_name)
    return sorted(matches)


def load_json_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("top-level JSON value is not an object")
    return value


def validate_curriculum(root: Path, report: Report) -> dict[str, Any] | None:
    path = root / "curriculum.json"
    if not path.is_file():
        report.failed("curriculum-load", "curriculum.json is missing")
        return None

    try:
        curriculum = load_json_object(path)
    except Exception as exc:
        report.failed("curriculum-load", str(exc))
        return None
    report.passed("curriculum-load", "curriculum.json parsed as a JSON object")

    metadata_failures: list[str] = []
    if curriculum.get("schemaVersion") != EXPECTED_SCHEMA_VERSION:
        metadata_failures.append(
            f"schemaVersion must be {EXPECTED_SCHEMA_VERSION}"
        )

    program = curriculum.get("program")
    course = curriculum.get("course")
    groups = curriculum.get("groups")
    career = curriculum.get("career")
    if not isinstance(program, dict):
        metadata_failures.append("program must be an object")
        program = {}
    if not isinstance(course, dict):
        metadata_failures.append("course must be an object")
        course = {}
    if not isinstance(groups, list):
        metadata_failures.append("groups must be an array")
        groups = []
    if not isinstance(career, dict):
        metadata_failures.append("career must be an object")
        career = {}

    if program.get("id") != EXPECTED_PROGRAM_ID:
        metadata_failures.append(f"program.id must be {EXPECTED_PROGRAM_ID}")
    if not is_nonempty_string(program.get("title")):
        metadata_failures.append("program.title is missing")
    expected_target_market = "Dutch small and medium-sized enterprises (SMEs)"
    if program.get("targetMarket") != expected_target_market:
        metadata_failures.append(
            f"program.targetMarket must be {expected_target_market}"
        )
    if not is_nonempty_string(program.get("positioning")):
        metadata_failures.append("program.positioning is missing")
    if not is_nonempty_string(program.get("durableValue")):
        metadata_failures.append("program.durableValue is missing")

    if course.get("id") != EXPECTED_COURSE_ID:
        metadata_failures.append(f"course.id must be {EXPECTED_COURSE_ID}")
    if course.get("sequence") != 1:
        metadata_failures.append("course.sequence must be 1")
    if not is_nonempty_string(course.get("title")):
        metadata_failures.append("course.title is missing")
    if not isinstance(course.get("version"), str) or not SEMVER_RE.fullmatch(
        course.get("version", "")
    ):
        metadata_failures.append("course.version must use x.y.z")
    if (
        not isinstance(course.get("practiceRevision"), int)
        or course.get("practiceRevision") < 1
    ):
        metadata_failures.append("course.practiceRevision must be a positive integer")
    verified_through = course.get("verifiedThrough")
    if not valid_revision(verified_through):
        metadata_failures.append("course.verifiedThrough must be a valid ISO date")

    estimated_hours = course.get("estimatedHours")
    if not isinstance(estimated_hours, dict):
        metadata_failures.append("course.estimatedHours must be an object")
    else:
        minimum = estimated_hours.get("minimum")
        typical = estimated_hours.get("typical")
        maximum = estimated_hours.get("maximum")
        if not all(
            isinstance(value, int) and value > 0
            for value in (minimum, typical, maximum)
        ):
            metadata_failures.append(
                "course estimated hours must be positive integers"
            )
        elif not minimum <= typical <= maximum:
            metadata_failures.append(
                "course estimated hours must satisfy minimum <= typical <= maximum"
            )

    capstone = course.get("capstone")
    if not isinstance(capstone, dict):
        metadata_failures.append("course.capstone must be an object")
    else:
        if capstone.get("title") != "Synthetic SME Operations Exception Assistant":
            metadata_failures.append("unexpected Course 1 capstone title")
        if not is_nonempty_string(capstone.get("summary")):
            metadata_failures.append("course.capstone.summary is missing")
        non_goals = capstone.get("nonGoals")
        if not isinstance(non_goals, list) or not all(
            is_nonempty_string(item) for item in non_goals
        ):
            metadata_failures.append("course.capstone.nonGoals must be text entries")

    if metadata_failures:
        report.failed("curriculum-metadata", compact(metadata_failures))
    else:
        report.passed(
            "curriculum-metadata",
            f"Course 1 metadata is complete through {verified_through}",
        )

    group_failures: list[str] = []
    document_failures: list[str] = []
    identity_failures: list[str] = []
    group_ids: list[str] = []
    current_ids: list[str] = []
    legacy_ids: list[str] = []
    source_paths: list[str] = []

    for group_index, group in enumerate(groups):
        location = f"groups[{group_index}]"
        if not isinstance(group, dict):
            group_failures.append(f"{location} is not an object")
            continue
        group_id = group.get("id")
        if not isinstance(group_id, str) or not STABLE_ID_RE.fullmatch(group_id):
            group_failures.append(f"{location}.id is not a stable slug")
            group_id = f"<invalid-{group_index}>"
        else:
            group_ids.append(group_id)
        if not is_nonempty_string(group.get("title")):
            group_failures.append(f"{group_id}.title is missing")
        if not is_nonempty_string(group.get("kind")):
            group_failures.append(f"{group_id}.kind is missing")
        if not isinstance(group.get("core"), bool):
            group_failures.append(f"{group_id}.core must be boolean")

        documents = group.get("documents")
        if not isinstance(documents, list) or not documents:
            group_failures.append(f"{group_id}.documents must be a non-empty array")
            continue

        for document_index, document in enumerate(documents):
            document_location = f"{group_id}.documents[{document_index}]"
            if not isinstance(document, dict):
                document_failures.append(f"{document_location} is not an object")
                continue

            document_id = document.get("id")
            if not isinstance(document_id, str) or not STABLE_ID_RE.fullmatch(
                document_id
            ):
                identity_failures.append(
                    f"{document_location}.id is not a stable slug"
                )
                document_id = document_location
            else:
                current_ids.append(document_id)
                if not document_id.startswith("course-1-"):
                    identity_failures.append(
                        f"{document_id} must start with course-1-"
                    )

            revision = document.get("revision")
            if not valid_revision(revision):
                document_failures.append(
                    f"{document_id}.revision is not a valid ISO date"
                )
            elif valid_revision(verified_through) and revision > verified_through:
                document_failures.append(
                    f"{document_id}.revision is after course.verifiedThrough"
                )

            if "title" in document and not is_nonempty_string(document.get("title")):
                document_failures.append(
                    f"{document_id}.title is present but empty"
                )

            legacy = document.get("legacyIds")
            if not isinstance(legacy, list):
                identity_failures.append(f"{document_id}.legacyIds must be an array")
            else:
                for legacy_id in legacy:
                    if not isinstance(legacy_id, str) or not STABLE_ID_RE.fullmatch(
                        legacy_id
                    ):
                        identity_failures.append(
                            f"{document_id} has invalid legacy ID {legacy_id!r}"
                        )
                    else:
                        legacy_ids.append(legacy_id)

            source_path = document.get("sourcePath")
            if not isinstance(source_path, str) or not source_path:
                document_failures.append(f"{document_id}.sourcePath is missing")
                continue
            pure_path = PurePosixPath(source_path)
            if (
                pure_path.is_absolute()
                or ".." in pure_path.parts
                or "." in pure_path.parts
                or "\\" in source_path
                or pure_path.as_posix() != source_path
            ):
                document_failures.append(
                    f"{document_id}.sourcePath is not a normalized relative path"
                )
                continue
            source_paths.append(source_path)
            relative = Path(*pure_path.parts)
            if path_is_ignored(relative):
                document_failures.append(
                    f"{document_id}.sourcePath points outside the current-course scope"
                )
                continue
            resolved = (root / relative).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                document_failures.append(
                    f"{document_id}.sourcePath escapes the course root"
                )
                continue
            if not resolved.is_file() and source_path != "VALIDATION_REPORT.md":
                document_failures.append(
                    f"{document_id}.sourcePath does not exist: {source_path}"
                )

    duplicate_groups = sorted(
        group_id for group_id, count in Counter(group_ids).items() if count > 1
    )
    if duplicate_groups:
        group_failures.append(f"duplicate group IDs: {duplicate_groups}")

    duplicate_current = sorted(
        item_id for item_id, count in Counter(current_ids).items() if count > 1
    )
    duplicate_legacy = sorted(
        item_id for item_id, count in Counter(legacy_ids).items() if count > 1
    )
    collisions = sorted(set(current_ids) & set(legacy_ids))
    duplicate_paths = sorted(
        source for source, count in Counter(source_paths).items() if count > 1
    )
    if duplicate_current:
        identity_failures.append(f"duplicate current IDs: {duplicate_current}")
    if duplicate_legacy:
        identity_failures.append(f"duplicate legacy IDs: {duplicate_legacy}")
    if collisions:
        identity_failures.append(
            f"IDs used as both current and legacy IDs: {collisions}"
        )
    if duplicate_paths:
        document_failures.append(f"duplicate source paths: {duplicate_paths}")

    if group_failures:
        report.failed("curriculum-groups", compact(group_failures))
    else:
        report.passed(
            "curriculum-groups",
            f"{len(groups)} configured groups have stable IDs and valid structure",
        )
    if identity_failures:
        report.failed("curriculum-stable-ids", compact(identity_failures))
    else:
        report.passed(
            "curriculum-stable-ids",
            f"{len(current_ids)} unique current IDs and {len(legacy_ids)} unique legacy IDs",
        )
    if document_failures:
        report.failed("curriculum-documents", compact(document_failures))
    else:
        report.passed(
            "curriculum-documents",
            f"{len(source_paths)} unique configured lesson paths and revisions are valid",
        )

    core_group_ids = course.get("coreGroupIds")
    groups_by_id = {
        group.get("id"): group for group in groups if isinstance(group, dict)
    }
    core_failures: list[str] = []
    if core_group_ids != ["foundations", "modules"]:
        core_failures.append(
            "course.coreGroupIds must be ['foundations', 'modules'] in that order"
        )
    for group_id in ("foundations", "modules"):
        group = groups_by_id.get(group_id)
        if not isinstance(group, dict):
            core_failures.append(f"missing {group_id} group")
        elif group.get("core") is not True:
            core_failures.append(f"{group_id} group must be core")
    if core_failures:
        report.failed("curriculum-core-groups", compact(core_failures))
    else:
        report.passed(
            "curriculum-core-groups",
            "only foundations and modules are configured as progress groups",
        )

    validate_career_metadata(career, report)
    return curriculum


def validate_career_metadata(career: dict[str, Any], report: Report) -> None:
    failures: list[str] = []
    if career.get("targetRole") != (
        "Controlled Artificial Intelligence (AI) Workflow Implementation "
        "Consultant for Dutch Small and Medium-sized Enterprises (SMEs)"
    ):
        failures.append("career.targetRole is missing or unexpected")
    courses = career.get("courses")
    if not isinstance(courses, list) or not courses:
        failures.append("career.courses must be a non-empty array")
        courses = []

    course_ids: list[str] = []
    sequences: list[int] = []
    current_ids: list[str] = []
    for index, course in enumerate(courses):
        if not isinstance(course, dict):
            failures.append(f"career.courses[{index}] is not an object")
            continue
        course_id = course.get("id")
        if not isinstance(course_id, str) or not STABLE_ID_RE.fullmatch(course_id):
            failures.append(f"career.courses[{index}].id is not stable")
        else:
            course_ids.append(course_id)
        sequence = course.get("sequence")
        if not isinstance(sequence, int) or sequence < 1:
            failures.append(f"{course_id}.sequence is invalid")
        else:
            sequences.append(sequence)
        if not all(
            is_nonempty_string(course.get(field_name))
            for field_name in ("title", "status", "purpose", "exitEvidence")
        ):
            failures.append(f"{course_id} is missing descriptive metadata")
        if course.get("status") == "current" and isinstance(course_id, str):
            current_ids.append(course_id)

    if len(course_ids) != len(set(course_ids)):
        failures.append("career course IDs are not unique")
    if sequences != list(range(1, len(sequences) + 1)):
        failures.append("career course sequences must be ordered 1..N")
    if current_ids != [EXPECTED_COURSE_ID]:
        failures.append("the Course 1 ID must be the only current career course")

    if failures:
        report.failed("career-metadata", compact(failures))
    else:
        report.passed(
            "career-metadata",
            f"{len(courses)} ordered career courses; Course 1 is the only current course",
        )


def group_documents(
    curriculum: dict[str, Any], group_id: str
) -> list[dict[str, Any]]:
    groups = curriculum.get("groups")
    if not isinstance(groups, list):
        return []
    for group in groups:
        if isinstance(group, dict) and group.get("id") == group_id:
            documents = group.get("documents")
            if isinstance(documents, list):
                return [
                    document
                    for document in documents
                    if isinstance(document, dict)
                ]
    return []


def validate_progress_lessons(
    root: Path, curriculum: dict[str, Any] | None, report: Report
) -> None:
    if curriculum is None:
        report.failed(
            "progress-lessons",
            "cannot validate progress lessons without curriculum.json",
        )
        return

    foundations = group_documents(curriculum, "foundations")
    modules = group_documents(curriculum, "modules")
    foundation_failures: list[str] = []
    module_failures: list[str] = []

    expected_foundation_ids = [
        f"course-1-foundation-{number:02d}" for number in range(1, 10)
    ]
    actual_foundation_ids = [item.get("id") for item in foundations]
    if actual_foundation_ids != expected_foundation_ids:
        foundation_failures.append(
            f"expected IDs {expected_foundation_ids}; found {actual_foundation_ids}"
        )

    expected_foundation_paths: list[str] = []
    for number, document in enumerate(foundations, 1):
        source_path = document.get("sourcePath")
        if not isinstance(source_path, str) or not re.fullmatch(
            rf"foundations/{number:02d}_[A-Z0-9_]+\.md", source_path
        ):
            foundation_failures.append(
                f"foundation {number} has unexpected source path {source_path!r}"
            )
        else:
            expected_foundation_paths.append(source_path)
        if not is_nonempty_string(document.get("title")):
            foundation_failures.append(
                f"foundation {number} requires a progress title"
            )

    disk_foundations = sorted(
        path.relative_to(root).as_posix()
        for path in (root / "foundations").glob("[0-9][0-9]_*.md")
    )
    if sorted(expected_foundation_paths) != disk_foundations:
        foundation_failures.append(
            "configured foundation paths do not match numbered foundation files"
        )

    expected_module_ids = [
        f"course-1-module-{number:02d}" for number in range(1, 10)
    ]
    expected_module_paths = [
        f"modules/MODULE_{number:02d}.md" for number in range(1, 10)
    ]
    actual_module_ids = [item.get("id") for item in modules]
    actual_module_paths = [item.get("sourcePath") for item in modules]
    if actual_module_ids != expected_module_ids:
        module_failures.append(
            f"expected IDs {expected_module_ids}; found {actual_module_ids}"
        )
    if actual_module_paths != expected_module_paths:
        module_failures.append(
            f"expected paths {expected_module_paths}; found {actual_module_paths}"
        )
    for number, document in enumerate(modules, 1):
        if not is_nonempty_string(document.get("title")):
            module_failures.append(f"module {number} requires a progress title")

    disk_modules = sorted(
        path.relative_to(root).as_posix()
        for path in (root / "modules").glob("MODULE_*.md")
    )
    if disk_modules != expected_module_paths:
        module_failures.append(
            f"disk module set must be MODULE_01.md through MODULE_09.md; found {disk_modules}"
        )

    if foundation_failures:
        report.failed("progress-foundations", compact(foundation_failures))
    else:
        report.passed(
            "progress-foundations",
            "exactly 9 ordered foundation progress lessons",
        )
    if module_failures:
        report.failed("progress-modules", compact(module_failures))
    else:
        report.passed(
            "progress-modules",
            "exactly 9 ordered module progress lessons",
        )

    if not foundation_failures and not module_failures:
        report.passed(
            "progress-total",
            "18 progress lessons: 9 foundations plus 9 modules",
        )
    else:
        report.failed(
            "progress-total",
            f"found {len(foundations)} foundation and {len(modules)} module entries",
        )


def validate_module_structure(
    root: Path, curriculum: dict[str, Any] | None, report: Report
) -> None:
    if curriculum is None:
        report.failed(
            "module-structure",
            "cannot validate modules without curriculum.json",
        )
        return

    failures: list[str] = []
    modules = group_documents(curriculum, "modules")
    for number, document in enumerate(modules, 1):
        source_path = document.get("sourcePath")
        if not isinstance(source_path, str):
            failures.append(f"module {number} lacks sourcePath")
            continue
        path = root / Path(*PurePosixPath(source_path).parts)
        if not path.is_file():
            failures.append(f"{source_path} is missing")
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except Exception as exc:
            failures.append(f"{source_path} cannot be read: {exc}")
            continue
        if not lines or not re.fullmatch(rf"# Module {number} .+", lines[0]):
            failures.append(
                f"{source_path} first line must identify Module {number}"
            )

        positions: list[int] = []
        for heading in REQUIRED_MODULE_HEADINGS:
            indexes = [index for index, line in enumerate(lines) if line == heading]
            if len(indexes) != 1:
                failures.append(
                    f"{source_path} requires exactly one {heading!r}; found {len(indexes)}"
                )
            else:
                positions.append(indexes[0])
        if len(positions) == len(REQUIRED_MODULE_HEADINGS) and positions != sorted(
            positions
        ):
            failures.append(f"{source_path} required headings are out of order")

    if failures:
        report.failed("module-structure", compact(failures))
    else:
        report.passed(
            "module-structure",
            f"all {len(modules)} modules use the {len(REQUIRED_MODULE_HEADINGS)} required headings in order",
        )


def section_text(lines: list[str], heading: str) -> str:
    """Return one level-two Markdown section without later level-two sections."""

    try:
        start = lines.index(heading) + 1
    except ValueError:
        return ""
    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return "\n".join(lines[start:end])


def validate_beginner_practice_contract(
    root: Path, curriculum: dict[str, Any] | None, report: Report
) -> None:
    if curriculum is None:
        report.failed(
            "beginner-practice-structure",
            "cannot validate the practice contract without curriculum.json",
        )
        return

    documents = group_documents(curriculum, "foundations") + group_documents(
        curriculum, "modules"
    )
    structure_failures: list[str] = []
    inspection_failures: list[str] = []
    pass_failures: list[str] = []

    for document in documents:
        source_path = document.get("sourcePath")
        if not isinstance(source_path, str):
            structure_failures.append(
                f"{document.get('id', '<unknown>')} lacks sourcePath"
            )
            continue
        path = root / Path(*PurePosixPath(source_path).parts)
        if not path.is_file():
            structure_failures.append(f"{source_path} is missing")
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except Exception as exc:
            structure_failures.append(f"{source_path} cannot be read: {exc}")
            continue
        expected_title = document.get("title")
        if (
            not isinstance(expected_title, str)
            or not lines
            or lines[0] != f"# {expected_title}"
        ):
            structure_failures.append(
                f"{source_path} H1 must exactly match its curriculum title"
            )

        positions: list[int] = []
        for heading in REQUIRED_PRACTICE_HEADINGS:
            indexes = [index for index, line in enumerate(lines) if line == heading]
            if len(indexes) != 1:
                structure_failures.append(
                    f"{source_path} requires exactly one {heading!r}; found {len(indexes)}"
                )
            else:
                positions.append(indexes[0])
        if len(positions) == len(REQUIRED_PRACTICE_HEADINGS):
            if positions != sorted(positions):
                structure_failures.append(
                    f"{source_path} practice headings are out of order"
                )

            follow_text = section_text(
                lines, "## Follow along — I show you exactly how"
            ).lower()
            recreate_text = section_text(
                lines, "## Now recreate it yourself"
            ).lower()
            if "expected result" not in follow_text:
                structure_failures.append(
                    f"{source_path} follow-along lacks an explicit expected result"
                )
            if not any(word in recreate_text for word in ("different", "new")):
                structure_failures.append(
                    f"{source_path} recreation does not require changed material"
                )

            inspection_text = section_text(
                lines, "## Ask Codex to check your work"
            )
            normalized_inspection = " ".join(inspection_text.lower().split())
            required_inspection_terms = (
                "read-only",
                "full path",
                "pass",
                "not yet",
            )
            missing_terms = [
                term
                for term in required_inspection_terms
                if term not in normalized_inspection
            ]
            if "[paste" not in normalized_inspection:
                missing_terms.append("[PASTE ...] path placeholder")
            if not any(
                phrase in normalized_inspection
                for phrase in (
                    "do not create",
                    "do not change",
                    "do not edit",
                )
            ):
                missing_terms.append("explicit no-change instruction")
            if not any(
                phrase in normalized_inspection
                for phrase in (
                    "real employer",
                    "real work",
                    "real client",
                    "no secrets",
                    "contains no secrets",
                )
            ):
                missing_terms.append("real-data or secret safety check")
            if missing_terms:
                inspection_failures.append(
                    f"{source_path} Codex prompt lacks: {', '.join(missing_terms)}"
                )

            pass_text = section_text(lines, "## Pass criteria")
            checklist_count = len(
                re.findall(r"^\s*-\s+\[\s\]\s+", pass_text, re.MULTILINE)
            )
            if checklist_count < 3:
                pass_failures.append(
                    f"{source_path} has {checklist_count} pass checkboxes; expected at least 3"
                )

    if structure_failures:
        report.failed(
            "beginner-practice-structure",
            compact(structure_failures, limit=24),
        )
    else:
        report.passed(
            "beginner-practice-structure",
            f"all {len(documents)} progress lessons use the ordered follow, recreate, inspect, and pass loop",
        )

    if inspection_failures:
        report.failed(
            "beginner-practice-codex-check",
            compact(inspection_failures, limit=24),
        )
    else:
        report.passed(
            "beginner-practice-codex-check",
            f"all {len(documents)} progress lessons include bounded read-only Codex inspection prompts",
        )

    if pass_failures:
        report.failed(
            "beginner-practice-pass-criteria",
            compact(pass_failures, limit=24),
        )
    else:
        report.passed(
            "beginner-practice-pass-criteria",
            f"all {len(documents)} progress lessons include objective pass checklists",
        )


def validate_beginner_terminology(root: Path, report: Report) -> None:
    failures: list[str] = []
    checked = 0
    for source_path, required_phrases in REQUIRED_ONBOARDING_PHRASES.items():
        path = root / source_path
        if not path.is_file():
            failures.append(f"{source_path} is missing")
            continue
        try:
            text = " ".join(
                path.read_text(encoding="utf-8").replace("*", "").split()
            ).lower()
        except Exception as exc:
            failures.append(f"{source_path} cannot be read: {exc}")
            continue
        for phrase in required_phrases:
            checked += 1
            if " ".join(phrase.split()).lower() not in text:
                failures.append(f"{source_path} lacks first-use explanation {phrase!r}")

    if failures:
        report.failed("beginner-first-use-terms", compact(failures, limit=24))
    else:
        report.passed(
            "beginner-first-use-terms",
            f"{checked} required first-use expansions and product explanations are present in onboarding",
        )


def validate_current_json(root: Path, report: Report) -> None:
    failures: list[str] = []
    json_files = iter_current_files(root, ".json")
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"{path.relative_to(root)}: {exc}")
    if failures:
        report.failed("current-json-syntax", compact(failures))
    else:
        report.passed(
            "current-json-syntax",
            f"{len(json_files)} in-scope JSON files parsed",
        )


def validate_json_schemas(root: Path, report: Report) -> None:
    schema_directory = root / "schemas"
    schema_paths = sorted(schema_directory.glob("*.schema.json"))
    names = {path.name for path in schema_paths}
    missing = sorted(EXPECTED_SCHEMA_FILES - names)
    if missing:
        report.failed("schema-set", f"missing current schemas: {missing}")
    else:
        report.passed(
            "schema-set",
            f"{len(schema_paths)} current schema files include all required Course 1 contracts",
        )

    structural_failures: list[str] = []
    schemas: list[tuple[Path, dict[str, Any]]] = []
    schema_ids: list[str] = []
    for path in schema_paths:
        try:
            schema = load_json_object(path)
        except Exception as exc:
            structural_failures.append(f"{path.name}: {exc}")
            continue
        schemas.append((path, schema))
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            structural_failures.append(
                f"{path.name}: $schema must identify Draft 2020-12"
            )
        schema_id = schema.get("$id")
        if not is_nonempty_string(schema_id):
            structural_failures.append(f"{path.name}: $id is missing")
        else:
            schema_ids.append(schema_id)
        if not is_nonempty_string(schema.get("title")):
            structural_failures.append(f"{path.name}: title is missing")
        if schema.get("type") != "object":
            structural_failures.append(f"{path.name}: top-level type must be object")
        if schema.get("additionalProperties") is not False:
            structural_failures.append(
                f"{path.name}: additionalProperties must be false"
            )
        properties = schema.get("properties")
        required = schema.get("required")
        if not isinstance(properties, dict) or not properties:
            structural_failures.append(f"{path.name}: properties must be non-empty")
        if not isinstance(required, list) or not all(
            isinstance(item, str) for item in required
        ):
            structural_failures.append(
                f"{path.name}: required must be an array of strings"
            )
        elif isinstance(properties, dict):
            unknown_required = sorted(set(required) - set(properties))
            if unknown_required:
                structural_failures.append(
                    f"{path.name}: required fields absent from properties {unknown_required}"
                )

    duplicate_schema_ids = sorted(
        schema_id
        for schema_id, count in Counter(schema_ids).items()
        if count > 1
    )
    if duplicate_schema_ids:
        structural_failures.append(
            f"duplicate schema IDs: {duplicate_schema_ids}"
        )

    if structural_failures:
        report.failed("schema-structure", compact(structural_failures))
    else:
        report.passed(
            "schema-structure",
            f"{len(schemas)} schemas have unique IDs and closed object contracts",
        )

    try:
        import jsonschema  # type: ignore
    except ModuleNotFoundError:
        report.warn(
            "schema-meta-validation",
            "jsonschema is not installed; standard-library schema structure checks passed, but Draft 2020-12 meta-validation was not run",
        )
    except Exception as exc:
        report.warn(
            "schema-meta-validation",
            f"jsonschema could not be imported: {exc}",
        )
    else:
        meta_failures: list[str] = []
        for path, schema in schemas:
            try:
                jsonschema.Draft202012Validator.check_schema(schema)
            except Exception as exc:
                meta_failures.append(f"{path.name}: {exc}")
        if meta_failures:
            report.failed("schema-meta-validation", compact(meta_failures))
        else:
            report.passed(
                "schema-meta-validation",
                f"jsonschema accepted all {len(schemas)} schemas as Draft 2020-12",
            )


def validate_optional_yaml(root: Path, report: Report) -> None:
    path = root / "stack-manifest.yaml"
    if not path.is_file():
        report.warn("yaml-parse", "stack-manifest.yaml is not present")
        return
    try:
        import yaml  # type: ignore
    except ModuleNotFoundError:
        report.warn(
            "yaml-parse",
            "PyYAML is not installed; stack-manifest.yaml was not parsed",
        )
    except Exception as exc:
        report.warn("yaml-parse", f"PyYAML could not be imported: {exc}")
    else:
        try:
            value = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(value, dict):
                raise ValueError("top-level YAML value is not a mapping")
        except Exception as exc:
            report.failed("yaml-parse", str(exc))
        else:
            report.passed("yaml-parse", "stack-manifest.yaml parsed as a mapping")


def load_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        headers = list(reader.fieldnames or [])
        rows: list[dict[str, str]] = []
        for row_number, row in enumerate(reader, 2):
            if None in row:
                raise ValueError(
                    f"row {row_number} has more values than the header"
                )
            normalized: dict[str, str] = {}
            for key, value in row.items():
                normalized[key] = "" if value is None else value
            rows.append(normalized)
    return headers, rows


def blank(value: str) -> bool:
    return value.strip() == ""


def parse_iso_date(value: str) -> date | None:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return None
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        return None
    return parsed if parsed.isoformat() == value else None


def parse_decimal(value: str) -> Decimal | None:
    try:
        parsed = Decimal(value)
    except (InvalidOperation, ValueError):
        return None
    return parsed if parsed.is_finite() else None


def computed_practice_issues(
    rows: list[dict[str, str]]
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    parsed_dates_by_item: dict[str, dict[str, date | None]] = {}

    def add(
        row: dict[str, str],
        field_name: str,
        rule_code: str,
        severity: str,
        message: str,
    ) -> None:
        issues.append(
            {
                "work_item_id": row["work_item_id"],
                "field": field_name,
                "rule_code": rule_code,
                "severity": severity,
                "expected_message": message,
            }
        )

    for row in rows:
        for field_name in REQUIRED_VALUE_FIELDS:
            if blank(row[field_name]):
                add(
                    row,
                    field_name,
                    "R001",
                    "medium",
                    f"Required {field_name} is missing.",
                )

        status = row["status"].strip()
        priority = row["priority"].strip()
        if status not in ALLOWED_STATUSES:
            add(
                row,
                "status",
                "R002",
                "high",
                "Status is not in the allowed list.",
            )
        if priority not in ALLOWED_PRIORITIES:
            add(
                row,
                "priority",
                "R003",
                "medium",
                "Priority is not in the allowed list.",
            )

        parsed_dates: dict[str, date | None] = {}
        for field_name in DATE_FIELDS:
            value = row[field_name].strip()
            parsed = parse_iso_date(value) if value else None
            parsed_dates[field_name] = parsed
            if value and parsed is None:
                add(
                    row,
                    field_name,
                    "R004",
                    "high",
                    "Date must use ISO format YYYY-MM-DD.",
                )
        parsed_dates_by_item[row["work_item_id"]] = parsed_dates

        received = parsed_dates["received_date"]
        due = parsed_dates["due_date"]
        if received is not None and due is not None and due < received:
            add(
                row,
                "due_date",
                "R005",
                "high",
                "Due date is before received date.",
            )

        completion_value = row["completed_date"].strip()
        if status == "completed" and not completion_value:
            add(
                row,
                "completed_date",
                "R006",
                "high",
                "Completed work requires a completion date.",
            )
        elif status in (ALLOWED_STATUSES - {"completed"}) and completion_value:
            add(
                row,
                "completed_date",
                "R006",
                "medium",
                "Non-completed work must not have a completion date.",
            )

        if status in OWNER_REQUIRED_STATUSES and blank(row["owner_role"]):
            add(
                row,
                "owner_role",
                "R007",
                "medium",
                "Active work requires an owner role.",
            )

        amount_value = row["amount"].strip()
        currency_value = row["currency"].strip()
        if amount_value:
            parsed_amount = parse_decimal(amount_value)
            if parsed_amount is None or parsed_amount < 0:
                add(
                    row,
                    "amount",
                    "R008",
                    "high",
                    "Amount must not be negative.",
                )
            if currency_value != "EUR":
                add(
                    row,
                    "currency",
                    "R009",
                    "medium",
                    "A populated amount requires currency EUR.",
                )
        elif currency_value:
            add(
                row,
                "currency",
                "R009",
                "medium",
                "Currency must be blank when amount is blank.",
            )

    reference_counts = Counter(
        row["source_reference"].strip()
        for row in rows
        if row["source_reference"].strip()
    )
    for row in rows:
        reference = row["source_reference"].strip()
        if reference and reference_counts[reference] > 1:
            add(
                row,
                "source_reference",
                "R010",
                "high",
                f"Source reference {reference} is duplicated.",
            )

    for row in rows:
        status = row["status"].strip()
        due = parsed_dates_by_item[row["work_item_id"]]["due_date"]
        if (
            status in OPEN_STATUSES
            and due is not None
            and due < FIXED_ASSESSMENT_DATE
        ):
            add(
                row,
                "due_date",
                "R011",
                "high",
                "Open work is overdue on the fixed assessment date.",
            )

    return issues


def validate_practice_data(root: Path, report: Report) -> None:
    directory = root / "practice_data"
    readme_path = directory / "README.md"
    work_path = directory / "work_items.csv"
    expected_path = directory / "expected_issues.csv"
    missing = [
        path.relative_to(root).as_posix()
        for path in (readme_path, work_path, expected_path)
        if not path.is_file()
    ]
    if missing:
        report.failed("practice-files", f"missing: {missing}")
        return
    report.passed(
        "practice-files",
        "practice README, work_items.csv, and expected_issues.csv are present",
    )

    try:
        work_headers, work_rows = load_csv_rows(work_path)
        issue_headers, expected_rows = load_csv_rows(expected_path)
    except Exception as exc:
        report.failed("practice-csv-parse", str(exc))
        return

    shape_failures: list[str] = []
    if tuple(work_headers) != WORK_ITEM_FIELDS:
        shape_failures.append(
            f"work-item headers differ: expected {WORK_ITEM_FIELDS}; found {tuple(work_headers)}"
        )
    if tuple(issue_headers) != EXPECTED_ISSUE_FIELDS:
        shape_failures.append(
            f"expected-issue headers differ: expected {EXPECTED_ISSUE_FIELDS}; found {tuple(issue_headers)}"
        )
    if len(work_rows) != 15:
        shape_failures.append(f"work_items.csv must have 15 rows; found {len(work_rows)}")
    if len(expected_rows) != 13:
        shape_failures.append(
            f"expected_issues.csv must have 13 rows; found {len(expected_rows)}"
        )
    if shape_failures:
        report.failed("practice-shape", compact(shape_failures))
    else:
        report.passed(
            "practice-shape",
            "12 work-item columns / 15 rows and 6 issue columns / 13 rows",
        )

    key_failures: list[str] = []
    work_item_ids = [row.get("work_item_id", "") for row in work_rows]
    expected_work_item_ids = [f"WI-{number:04d}" for number in range(1, 16)]
    if work_item_ids != expected_work_item_ids:
        key_failures.append(
            f"work item IDs must be ordered WI-0001..WI-0015; found {work_item_ids}"
        )
    if len(work_item_ids) != len(set(work_item_ids)):
        key_failures.append("work_item_id values are not unique")

    issue_ids = [row.get("issue_id", "") for row in expected_rows]
    expected_issue_ids = [f"ISS-{number:03d}" for number in range(1, 14)]
    if issue_ids != expected_issue_ids:
        key_failures.append(
            f"issue IDs must be ordered ISS-001..ISS-013; found {issue_ids}"
        )
    if len(issue_ids) != len(set(issue_ids)):
        key_failures.append("issue_id values are not unique")

    comparison_keys = [
        (row.get("work_item_id", ""), row.get("rule_code", ""))
        for row in expected_rows
    ]
    if len(comparison_keys) != len(set(comparison_keys)):
        key_failures.append(
            "(work_item_id, rule_code) expected-issue keys are not unique"
        )

    known_work_items = set(work_item_ids)
    for row in expected_rows:
        if row.get("work_item_id") not in known_work_items:
            key_failures.append(
                f"{row.get('issue_id')} references unknown {row.get('work_item_id')}"
            )
        if row.get("field") not in WORK_ITEM_FIELDS:
            key_failures.append(
                f"{row.get('issue_id')} references unknown field {row.get('field')}"
            )
        if row.get("severity") not in ALLOWED_SEVERITIES:
            key_failures.append(
                f"{row.get('issue_id')} has invalid severity {row.get('severity')}"
            )
        if not is_nonempty_string(row.get("expected_message")):
            key_failures.append(
                f"{row.get('issue_id')} has no expected message"
            )

    if key_failures:
        report.failed("practice-unique-keys", compact(key_failures))
    else:
        report.passed(
            "practice-unique-keys",
            "work-item IDs, issue IDs, and expected comparison keys are unique and referentially valid",
        )

    rule_failures: list[str] = []
    actual_rule_codes = {row.get("rule_code", "") for row in expected_rows}
    if actual_rule_codes != RULE_CODES:
        rule_failures.append(
            f"expected issues must cover R001-R011; found {sorted(actual_rule_codes)}"
        )
    readme = readme_path.read_text(encoding="utf-8")
    readme_rule_codes = re.findall(r"^\|\s*(R\d{3})\s*\|", readme, re.MULTILINE)
    if set(readme_rule_codes) != RULE_CODES:
        rule_failures.append(
            f"README rule register must contain R001-R011; found {sorted(set(readme_rule_codes))}"
        )
    duplicated_readme_rules = sorted(
        code for code, count in Counter(readme_rule_codes).items() if count != 1
    )
    if duplicated_readme_rules:
        rule_failures.append(
            f"README rule codes must appear once in the table: {duplicated_readme_rules}"
        )
    if FIXED_ASSESSMENT_DATE_TEXT not in readme:
        rule_failures.append(
            f"README does not state fixed assessment date {FIXED_ASSESSMENT_DATE_TEXT}"
        )

    if rule_failures:
        report.failed("practice-rule-register", compact(rule_failures))
    else:
        report.passed(
            "practice-rule-register",
            f"R001-R011 are documented and covered using fixed date {FIXED_ASSESSMENT_DATE_TEXT}",
        )

    safety_failures: list[str] = []
    lower_readme = " ".join(readme.lower().split())
    required_safety_statements = (
        "every row is fictional",
        "do not describe a real person, employer, customer, or transaction",
        "do not replace these files with workplace or customer exports",
    )
    for statement in required_safety_statements:
        if statement not in lower_readme:
            safety_failures.append(f"README lacks safety statement: {statement}")

    sensitive_headers = {
        "name",
        "email",
        "phone",
        "address",
        "bsn",
        "patient",
        "diagnosis",
        "employee",
        "birth_date",
    }
    present_sensitive_headers = sorted(sensitive_headers & set(work_headers))
    if present_sensitive_headers:
        safety_failures.append(
            f"unexpected personal/sensitive columns: {present_sensitive_headers}"
        )

    for row in work_rows:
        if not WORK_ITEM_ID_RE.fullmatch(row.get("work_item_id", "")):
            safety_failures.append(
                f"non-synthetic work-item identifier {row.get('work_item_id')!r}"
            )
        reference = row.get("source_reference", "")
        if reference and not SOURCE_REFERENCE_RE.fullmatch(reference):
            safety_failures.append(
                f"non-synthetic source reference {reference!r}"
            )
        owner_role = row.get("owner_role", "")
        if owner_role and not re.fullmatch(r"[a-z][a-z0-9_]*", owner_role):
            safety_failures.append(
                f"owner_role must remain a role token, not a name: {owner_role!r}"
            )

    if safety_failures:
        report.failed("practice-synthetic-safety", compact(safety_failures))
    else:
        report.passed(
            "practice-synthetic-safety",
            "fixed fictional identifiers, role-only ownership, no personal-data columns, and explicit no-real-data guarantees",
        )

    if not shape_failures:
        computed = computed_practice_issues(work_rows)
        tuple_fields = (
            "work_item_id",
            "field",
            "rule_code",
            "severity",
            "expected_message",
        )
        computed_set = {
            tuple(row[field_name] for field_name in tuple_fields)
            for row in computed
        }
        expected_set = {
            tuple(row[field_name] for field_name in tuple_fields)
            for row in expected_rows
        }
        oracle_failures: list[str] = []
        missing_expected = sorted(computed_set - expected_set)
        unexpected_expected = sorted(expected_set - computed_set)
        if missing_expected:
            oracle_failures.append(
                f"computed issues absent from answer key: {missing_expected}"
            )
        if unexpected_expected:
            oracle_failures.append(
                f"answer-key issues not reproduced by rules: {unexpected_expected}"
            )
        if len(computed) != 13:
            oracle_failures.append(
                f"deterministic evaluator produced {len(computed)} issues, expected 13"
            )

        r010_items = {
            row["work_item_id"]
            for row in computed
            if row["rule_code"] == "R010"
        }
        if r010_items != {"WI-0006", "WI-0007"}:
            oracle_failures.append(
                f"R010 must identify both duplicate rows; found {sorted(r010_items)}"
            )
        r011_items = {
            row["work_item_id"]
            for row in computed
            if row["rule_code"] == "R011"
        }
        if r011_items != {"WI-0010"}:
            oracle_failures.append(
                f"R011 fixed-date result must be WI-0010; found {sorted(r011_items)}"
            )

        if oracle_failures:
            report.failed("practice-rule-oracle", compact(oracle_failures))
        else:
            report.passed(
                "practice-rule-oracle",
                "standard-library evaluator reproduces all 13 frozen issues, including both R010 duplicates and fixed-date R011",
            )
    else:
        report.failed(
            "practice-rule-oracle",
            "not run because practice-data shape is invalid",
        )


def clean_link_target(raw_target: str) -> str | None:
    target = raw_target.strip()
    if target.startswith("<"):
        closing = target.find(">")
        if closing < 0:
            return target
        target = target[1:closing]
    else:
        target = target.split(maxsplit=1)[0]

    lower = target.lower()
    if lower.startswith(
        (
            "http://",
            "https://",
            "mailto:",
            "tel:",
            "data:",
            "javascript:",
            "//",
        )
    ):
        return None
    if target.startswith("#"):
        return None
    target = target.split("#", 1)[0].split("?", 1)[0]
    return unquote(target) if target else None


def validate_internal_links(root: Path, report: Report) -> None:
    failures: list[str] = []
    checked = 0
    ignored_targets = 0
    markdown_files = iter_current_files(root, ".md")

    for markdown in markdown_files:
        try:
            text = markdown.read_text(encoding="utf-8")
        except Exception as exc:
            failures.append(f"{markdown.relative_to(root)} cannot be read: {exc}")
            continue
        searchable = FENCED_CODE_RE.sub("", text)
        raw_targets = [
            match.group(1) for match in INLINE_LINK_RE.finditer(searchable)
        ]
        raw_targets.extend(
            match.group(1) for match in REFERENCE_LINK_RE.finditer(searchable)
        )
        for raw_target in raw_targets:
            target = clean_link_target(raw_target)
            if target is None:
                continue
            candidate = markdown.parent / Path(target.replace("/", os.sep))
            resolved = candidate.resolve()
            try:
                relative = resolved.relative_to(root.resolve())
            except ValueError:
                failures.append(
                    f"{markdown.relative_to(root)} -> escapes root: {target}"
                )
                continue
            if path_is_ignored(relative):
                ignored_targets += 1
                continue
            checked += 1
            if not resolved.exists():
                failures.append(f"{markdown.relative_to(root)} -> {target}")

    if failures:
        report.failed("internal-links", compact(failures, limit=20))
    else:
        report.passed(
            "internal-links",
            f"{checked} current local targets exist; {ignored_targets} archived/generated targets ignored",
        )


def write_report(
    root: Path,
    report: Report,
    output: Path,
    curriculum: dict[str, Any] | None,
) -> None:
    result = "PASS" if not report.errors else "FAIL"
    course = curriculum.get("course", {}) if isinstance(curriculum, dict) else {}
    course_title = course.get("title", "Course 1")
    course_version = course.get("version", "unknown")
    verified_through = course.get("verifiedThrough", "unknown")

    lines = [
        "# Course 1 Package Validation Report",
        "",
        f"Course: **{course_title}**",
        "",
        f"Course version: `{course_version}`",
        "",
        f"Curriculum verified through: `{verified_through}`",
        "",
        f"Result: **{result}**",
        "",
        f"Checks: {len(report.checks)}; failures: {len(report.errors)}; warnings: {len(report.warnings)}",
        "",
        "## Scope",
        "",
        "This report covers the current curriculum manifest, configured lesson files,",
        "the 9 foundation and 9 module progress lessons, module structure, current",
        "JSON contracts, synthetic practice data, and current internal links.",
        "`future_courses/`, `app/dist/`, dependency folders, Git metadata, caches, and",
        "external websites are outside this deterministic validation.",
        "",
        "| Status | Check | Detail |",
        "|---|---|---|",
    ]
    for check in report.checks:
        detail = check["detail"].replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {check['status']} | {check['name']} | {detail} |")

    if report.errors:
        lines.extend(["", "## Release blockers", ""])
        lines.extend(f"- {error}" for error in report.errors)
    if report.warnings:
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {warning}" for warning in report.warnings)

    lines.extend(
        [
            "",
            "## Limits",
            "",
            "A PASS confirms deterministic package structure; it does not confirm external",
            "source currency, legal compliance, production security, model quality, visual",
            "layout, accessibility, or a learner's implementation. Those require the live",
            "source audit, PWA tests and visual review, and the course evaluation and UAT",
            "gates.",
            "",
        ]
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the current Course 1 package"
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="course package root (default: parent of tools/)",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help="report path (default: <root>/VALIDATION_REPORT.md)",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    output = (args.report or (root / "VALIDATION_REPORT.md")).resolve()

    if not root.is_dir():
        print(
            json.dumps(
                {
                    "result": "FAIL",
                    "failures": [f"course root is not a directory: {root}"],
                },
                indent=2,
            )
        )
        return 2

    report = Report()
    curriculum = validate_curriculum(root, report)
    validate_progress_lessons(root, curriculum, report)
    validate_module_structure(root, curriculum, report)
    validate_beginner_practice_contract(root, curriculum, report)
    validate_beginner_terminology(root, report)
    validate_current_json(root, report)
    validate_json_schemas(root, report)
    validate_optional_yaml(root, report)
    validate_practice_data(root, report)
    validate_internal_links(root, report)

    try:
        write_report(root, report, output, curriculum)
    except Exception as exc:
        print(
            json.dumps(
                {
                    "result": "FAIL",
                    "failures": [f"could not write validation report: {exc}"],
                },
                indent=2,
            )
        )
        return 2

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
