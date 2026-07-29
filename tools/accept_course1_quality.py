"""Run the fail-closed maintainer quality gate for Course 1.

This command is deliberately separate from beginner setup. It combines the
frozen learner suite, generated properties, Python and PWA line/branch
coverage, mutation testing, and family-level negative controls. Every layer is
reported separately; one green layer cannot substitute for another.
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
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
EXPECTED_PYTHON_MODULES = [
    "course1_capstone/cli.py",
    "course1_capstone/workflow.py",
]
EXPECTED_PWA_MODULES = [
    "app/src/markdown.js",
    "app/src/state.js",
]
EXPECTED_PROPERTIES = {
    "persistentCorpus": "quality/property-regression-corpus.json",
    "pythonSuite": "quality/test_runner_properties.py",
    "pwaSuite": "app/tests/property-security.test.mjs",
    "requiredPrefixes": ["test_prop_runner_", "PWA-PROP-"],
}
EXPECTED_MUTATION_FAMILIES = [
    "deterministic-rules",
    "approval-binding",
    "audit-reconciliation",
    "transaction-rollback",
    "path-guards",
    "markdown-url-safety",
    "backup-validation",
    "storage-conflict",
    "service-worker-identity",
]
EXPECTED_NEGATIVE_CONTROL_FAMILIES = [
    "DATA",
    "FS",
    "IO",
    "CAP",
    "PWA",
    "WEB",
    "SW",
    "SC",
    "TEST",
    "WIN",
    "BR",
    "REC",
]


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return value


def run_command(
    name: str,
    command: list[str],
    *,
    cwd: Path,
    environment: dict[str, str] | None = None,
) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
    except OSError as exc:
        return {
            "name": name,
            "command": command,
            "cwd": str(cwd.relative_to(ROOT)) if cwd != ROOT else ".",
            "exitCode": None,
            "result": "FAIL",
            "output": f"could not start command: {exc}",
        }
    return {
        "name": name,
        "command": command,
        "cwd": str(cwd.relative_to(ROOT)) if cwd != ROOT else ".",
        "exitCode": completed.returncode,
        "result": "PASS" if completed.returncode == 0 else "FAIL",
        "output": completed.stdout,
    }


def coverage_percent(covered: int, total: int) -> float:
    return 100.0 if total == 0 else round((covered / total) * 100, 2)


def validate_runtime_dependencies(
    maintainer_dependencies: set[str],
) -> list[str]:
    """Verify required maintainer tools exist in this Python environment."""

    failures: list[str] = []
    if "coverage" in maintainer_dependencies:
        try:
            coverage_spec = importlib.util.find_spec("coverage")
        except (ImportError, AttributeError, ValueError) as exc:
            failures.append(
                "maintainer dependency 'coverage' could not be inspected in the "
                f"executing Python environment: {exc}"
            )
        else:
            if coverage_spec is None:
                failures.append(
                    "maintainer dependency 'coverage' is not installed in the "
                    "executing Python environment; install "
                    "tools/requirements-maintainer.txt"
                )
    return failures


def final_quality_decision(
    existing_failures: list[str],
    commands: list[dict[str, Any]],
    evidence_layers: dict[str, Any],
) -> tuple[str, list[str]]:
    """Make every failed command or evidence layer block the overall result."""

    failures = list(existing_failures)

    def add_failure(reason: str) -> None:
        if reason not in failures:
            failures.append(reason)

    for index, command in enumerate(commands):
        name = command.get("name")
        if not isinstance(name, str) or not name:
            name = f"commands[{index}]"
        result = command.get("result")
        exit_code = command.get("exitCode")
        if result != "PASS" or exit_code != 0:
            add_failure(
                f"command '{name}' did not pass "
                f"(result={result!r}, exitCode={exit_code!r})"
            )

    for name, evidence in evidence_layers.items():
        layer_result = (
            evidence.get("result") if isinstance(evidence, dict) else evidence
        )
        if layer_result != "PASS":
            add_failure(
                f"evidence layer '{name}' did not pass "
                f"(result={layer_result!r})"
            )

    return ("PASS" if not failures else "FAIL"), failures


def validate_contract(contract: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    expected_keys = {
        "schemaVersion",
        "contractId",
        "requirements",
        "coverage",
        "properties",
        "mutationManifest",
        "requiredMutationFamilies",
        "negativeControlManifest",
        "requiredNegativeControlFamilies",
        "learnerRequirementFiles",
        "maintainerRequirementFiles",
    }
    if set(contract) != expected_keys:
        failures.append("quality contract has unknown or missing top-level keys")
    if contract.get("schemaVersion") != 1:
        failures.append("quality contract schemaVersion must be 1")
    if contract.get("contractId") != "C1-TST-QUALITY-001":
        failures.append("quality contract has the wrong stable test identifier")
    if contract.get("requirements") != [
        f"C1-TA-TEST-{number:03d}" for number in range(3, 10)
    ]:
        failures.append("quality contract must cover C1-TA-TEST-003 through -009")
    coverage = contract.get("coverage")
    if not isinstance(coverage, dict):
        failures.append("coverage contract must be one JSON object")
        coverage = {}
    if set(coverage) != {
        "minimumLinePercent",
        "minimumBranchPercent",
        "pythonModules",
        "pwaModules",
        "pwaLimitation",
    }:
        failures.append("coverage contract has unknown or missing keys")
    for field in ("minimumLinePercent", "minimumBranchPercent"):
        value = coverage.get(field)
        if not isinstance(value, (int, float)) or value < 90 or value > 100:
            failures.append(f"{field} must be between 90 and 100")
    if coverage.get("pythonModules") != EXPECTED_PYTHON_MODULES:
        failures.append("coverage contract must retain both critical Python modules")
    if coverage.get("pwaModules") != EXPECTED_PWA_MODULES:
        failures.append("coverage contract must retain both importable PWA security modules")
    if not isinstance(coverage.get("pwaLimitation"), str) or not coverage.get(
        "pwaLimitation", ""
    ).strip():
        failures.append("coverage contract must state the PWA coverage limitation")

    properties = contract.get("properties")
    if properties != EXPECTED_PROPERTIES:
        failures.append("property contract must retain the corpus, suites, and ID prefixes")

    exact_values = {
        "mutationManifest": "quality/mutation-manifest.json",
        "requiredMutationFamilies": EXPECTED_MUTATION_FAMILIES,
        "negativeControlManifest": "quality/negative-control-manifest.json",
        "requiredNegativeControlFamilies": EXPECTED_NEGATIVE_CONTROL_FAMILIES,
        "learnerRequirementFiles": ["requirements-course.txt"],
        "maintainerRequirementFiles": ["tools/requirements-maintainer.txt"],
    }
    for field, expected in exact_values.items():
        if contract.get(field) != expected:
            failures.append(f"{field} does not match the frozen quality contract")

    for field in (
        "requirements",
        "requiredMutationFamilies",
        "requiredNegativeControlFamilies",
        "learnerRequirementFiles",
        "maintainerRequirementFiles",
    ):
        values = contract.get(field)
        if (
            not isinstance(values, list)
            or not values
            or len(values) != len(set(values))
            or not all(isinstance(value, str) and value for value in values)
        ):
            failures.append(f"{field} must be one non-empty unique string list")

    referenced_files = [
        *EXPECTED_PROPERTIES.values(),
        contract.get("mutationManifest"),
        contract.get("negativeControlManifest"),
        *(contract.get("learnerRequirementFiles") or []),
        *(contract.get("maintainerRequirementFiles") or []),
    ]
    for value in referenced_files:
        if isinstance(value, list):
            continue
        if not isinstance(value, str) or not (ROOT / value).is_file():
            failures.append(f"quality-contract file is missing: {value!r}")
    return failures


def requirement_names(path: Path) -> set[str]:
    names: set[str] = set()
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("--"):
            continue
        match = re.match(r"^([A-Za-z0-9_.-]+)==", line)
        if match:
            names.add(re.sub(r"[-_.]+", "-", match.group(1)).lower())
    return names


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--node",
        type=Path,
        default=Path(shutil.which("node") or "node"),
        help="exact Node executable used for the PWA quality layer",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help="optional machine-readable report destination",
    )
    parser.add_argument(
        "--skip-mutations",
        action="store_true",
        help="repair-iteration aid; always records the mutation layer as NOT RUN",
    )
    args = parser.parse_args()

    failures: list[str] = []
    commands: list[dict[str, Any]] = []
    contract = read_json(CONTRACT_PATH)
    failures.extend(validate_contract(contract))

    learner_dependencies: set[str] = set()
    for relative in contract["learnerRequirementFiles"]:
        learner_dependencies.update(requirement_names(ROOT / relative))
    maintainer_dependencies: set[str] = set()
    for relative in contract["maintainerRequirementFiles"]:
        maintainer_dependencies.update(requirement_names(ROOT / relative))
    overlap = learner_dependencies & maintainer_dependencies
    if overlap:
        failures.append(
            "maintainer-only dependencies leaked into learner requirements: "
            f"{sorted(overlap)}"
        )
    if "coverage" not in maintainer_dependencies:
        failures.append("coverage.py is not present in the maintainer-only lock")
    runtime_dependency_failures = validate_runtime_dependencies(
        maintainer_dependencies
    )
    failures.extend(runtime_dependency_failures)

    node_path = args.node.resolve()
    if not node_path.is_file():
        failures.append(f"Node executable does not exist: {node_path}")

    with tempfile.TemporaryDirectory(prefix="course1-quality-") as temporary:
        evidence_root = Path(temporary)
        python_coverage = evidence_root / "python-coverage.json"
        coverage_environment = os.environ.copy()
        coverage_environment["COVERAGE_FILE"] = str(evidence_root / ".coverage")

        commands.append(
            run_command(
                "python-runner-properties-and-coverage",
                [
                    sys.executable,
                    "-m",
                    "coverage",
                    "run",
                    "--branch",
                    "--source=course1_capstone",
                    "--omit=course1_capstone/tests/*",
                    "-m",
                    "pytest",
                    "-q",
                    "course1_capstone/tests",
                    "quality/test_runner_properties.py",
                ],
                cwd=ROOT,
                environment=coverage_environment,
            )
        )
        if commands[-1]["exitCode"] == 0:
            commands.append(
                run_command(
                    "python-coverage-json",
                    [
                        sys.executable,
                        "-m",
                        "coverage",
                        "json",
                        "-o",
                        str(python_coverage),
                    ],
                    cwd=ROOT,
                    environment=coverage_environment,
                )
            )
        python_result: dict[str, Any] = {
            "result": "FAIL",
            "linePercent": 0.0,
            "branchPercent": 0.0,
        }
        if python_coverage.is_file():
            value = read_json(python_coverage)
            files = {
                str(path).replace("\\", "/"): details
                for path, details in value.get("files", {}).items()
            }
            selected = contract["coverage"]["pythonModules"]
            missing = [path for path in selected if path not in files]
            if missing:
                failures.append(f"Python coverage omitted critical modules: {missing}")
            totals = {
                "covered_lines": 0,
                "num_statements": 0,
                "covered_branches": 0,
                "num_branches": 0,
            }
            for path in selected:
                summary = files.get(path, {}).get("summary", {})
                for key in totals:
                    totals[key] += int(summary.get(key, 0))
            line_percent = coverage_percent(
                totals["covered_lines"], totals["num_statements"]
            )
            branch_percent = coverage_percent(
                totals["covered_branches"], totals["num_branches"]
            )
            python_result = {
                "result": (
                    "PASS"
                    if line_percent
                    >= contract["coverage"]["minimumLinePercent"]
                    and branch_percent
                    >= contract["coverage"]["minimumBranchPercent"]
                    else "FAIL"
                ),
                "linePercent": line_percent,
                "branchPercent": branch_percent,
                "totals": totals,
            }
            if python_result["result"] != "PASS":
                failures.append(
                    "Python critical-module coverage is below the 90% line/"
                    f"branch contract: {python_result}"
                )

        pwa_result = {
            "result": "NOT RUN",
            "limitation": contract["coverage"]["pwaLimitation"],
        }
        if node_path.is_file():
            pwa_modules = [
                str(Path(path).relative_to("app")).replace("\\", "/")
                for path in contract["coverage"]["pwaModules"]
            ]
            command = [
                str(node_path),
                "--experimental-test-coverage",
                f"--test-coverage-lines={contract['coverage']['minimumLinePercent']}",
                f"--test-coverage-branches={contract['coverage']['minimumBranchPercent']}",
            ]
            for path in pwa_modules:
                command.append(f"--test-coverage-include={path}")
            pwa_tests = [
                str(path.relative_to(ROOT / "app")).replace("\\", "/")
                for path in sorted((ROOT / "app" / "tests").glob("*.test.mjs"))
            ]
            if not pwa_tests:
                failures.append("no PWA test modules were discovered")
            command.extend(["--test", *pwa_tests])
            commands.append(
                run_command(
                    "pwa-properties-and-coverage",
                    command,
                    cwd=ROOT / "app",
                )
            )
            pwa_result = {
                "result": commands[-1]["result"],
                "limitation": contract["coverage"]["pwaLimitation"],
            }
            if commands[-1]["exitCode"] != 0:
                failures.append("PWA critical-module coverage or property tests failed")

        mutation_result = "NOT RUN"
        if args.skip_mutations:
            failures.append("mutation layer was explicitly skipped")
        else:
            mutation_tool = ROOT / "tools" / "run_course1_mutations.py"
            if not mutation_tool.is_file():
                failures.append("mutation runner is missing")
            else:
                commands.append(
                    run_command(
                        "mutation-testing",
                        [
                            sys.executable,
                            str(mutation_tool),
                            "--node",
                            str(node_path),
                        ],
                        cwd=ROOT,
                    )
                )
                mutation_result = commands[-1]["result"]
                if commands[-1]["exitCode"] != 0:
                    failures.append("one or more required mutants survived")

        negative_tool = ROOT / "tools" / "run_course1_negative_controls.py"
        negative_result = "NOT RUN"
        if not negative_tool.is_file():
            failures.append("family negative-control runner is missing")
        else:
            commands.append(
                run_command(
                    "family-negative-controls",
                    [
                        sys.executable,
                        str(negative_tool),
                        "--node",
                        str(node_path),
                    ],
                    cwd=ROOT,
                )
            )
            negative_result = commands[-1]["result"]
            if commands[-1]["exitCode"] != 0:
                failures.append("one or more critical-family negative controls failed")

    evidence_layers = {
        "pythonCoverageAndProperties": python_result,
        "pwaCoverageAndProperties": pwa_result,
        "mutation": mutation_result,
        "negativeControls": negative_result,
        "learnerMaintainerDependencySeparation": (
            "PASS" if not overlap and "coverage" in maintainer_dependencies else "FAIL"
        ),
        "maintainerRuntimeDependencies": (
            "PASS" if not runtime_dependency_failures else "FAIL"
        ),
    }
    overall_result, failures = final_quality_decision(
        failures,
        commands,
        evidence_layers,
    )

    report = {
        "schemaVersion": 1,
        "contractId": contract["contractId"],
        "checkedAt": dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "python": {
            "executable": sys.executable,
            "version": sys.version,
        },
        "node": str(node_path),
        "evidenceLayers": evidence_layers,
        "commands": commands,
        "failures": failures,
        "result": overall_result,
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
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
