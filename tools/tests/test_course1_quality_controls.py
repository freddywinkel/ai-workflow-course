"""Focused structural controls used by the Course 1 negative-control suite."""

from __future__ import annotations

import copy
import io
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import accept_course1_quality as quality_gate


ROOT = Path(__file__).resolve().parents[2]


class Course1QualityControlTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = json.loads(
            (ROOT / "quality" / "course1-quality-contract.json").read_text(
                encoding="utf-8"
            )
        )

    def test_quality_contract_is_closed_and_complete(self) -> None:
        self.assertEqual(quality_gate.validate_contract(self.contract), [])
        learner = quality_gate.requirement_names(ROOT / "requirements-course.txt")
        maintainer = quality_gate.requirement_names(
            ROOT / "tools" / "requirements-maintainer.txt"
        )
        self.assertIn("coverage", maintainer)
        self.assertNotIn("coverage", learner)
        self.assertFalse(learner & maintainer)

    def test_quality_contract_rejects_removed_critical_module(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["coverage"]["pythonModules"].remove("course1_capstone/cli.py")
        self.assertTrue(
            any(
                "critical Python modules" in failure
                for failure in quality_gate.validate_contract(changed)
            )
        )

    def test_quality_contract_rejects_removed_control_family(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["requiredNegativeControlFamilies"].remove("REC")
        self.assertTrue(
            any(
                "requiredNegativeControlFamilies" in failure
                for failure in quality_gate.validate_contract(changed)
            )
        )

    def test_quality_contract_rejects_substituted_manifest(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["mutationManifest"] = "quality/not-the-frozen-manifest.json"
        failures = quality_gate.validate_contract(changed)
        self.assertTrue(
            any("mutationManifest" in failure for failure in failures)
        )
        self.assertTrue(
            any("file is missing" in failure for failure in failures)
        )

    def test_failed_coverage_command_and_layer_force_overall_fail(self) -> None:
        commands = [
            {
                "name": "python-runner-properties-and-coverage",
                "exitCode": 1,
                "result": "FAIL",
            }
        ]
        evidence_layers = {
            "pythonCoverageAndProperties": {
                "result": "FAIL",
                "linePercent": 0.0,
                "branchPercent": 0.0,
            },
            "pwaCoverageAndProperties": {"result": "PASS"},
            "mutation": "PASS",
            "negativeControls": "PASS",
            "learnerMaintainerDependencySeparation": "PASS",
            "maintainerRuntimeDependencies": "PASS",
        }

        result, failures = quality_gate.final_quality_decision(
            [],
            commands,
            evidence_layers,
        )

        self.assertEqual(result, "FAIL")
        self.assertTrue(
            any(
                "command 'python-runner-properties-and-coverage' did not pass"
                in failure
                for failure in failures
            )
        )
        self.assertTrue(
            any(
                "evidence layer 'pythonCoverageAndProperties' did not pass"
                in failure
                for failure in failures
            )
        )

    def test_main_report_cannot_pass_when_coverage_command_exits_one(self) -> None:
        def fake_run_command(
            name: str,
            command: list[str],
            *,
            cwd: Path,
            environment: dict[str, str] | None = None,
        ) -> dict[str, object]:
            del environment
            failed = name == "python-runner-properties-and-coverage"
            return {
                "name": name,
                "command": command,
                "cwd": str(cwd),
                "exitCode": 1 if failed else 0,
                "result": "FAIL" if failed else "PASS",
                "output": "No module named coverage" if failed else "ok",
            }

        with tempfile.TemporaryDirectory() as temporary:
            report_path = Path(temporary) / "quality-report.json"
            with (
                mock.patch.object(
                    quality_gate.importlib.util,
                    "find_spec",
                    return_value=object(),
                ),
                mock.patch.object(
                    quality_gate,
                    "run_command",
                    side_effect=fake_run_command,
                ),
                mock.patch.object(
                    sys,
                    "argv",
                    [
                        "accept_course1_quality.py",
                        "--node",
                        sys.executable,
                        "--report",
                        str(report_path),
                    ],
                ),
                mock.patch("sys.stdout", new=io.StringIO()),
            ):
                exit_code = quality_gate.main()

            report = json.loads(report_path.read_text(encoding="utf-8"))

        self.assertEqual(exit_code, 1)
        self.assertEqual(report["result"], "FAIL")
        self.assertEqual(
            report["evidenceLayers"]["pythonCoverageAndProperties"]["result"],
            "FAIL",
        )
        self.assertTrue(report["failures"])
        self.assertTrue(
            any(
                "command 'python-runner-properties-and-coverage' did not pass"
                in failure
                for failure in report["failures"]
            )
        )

    def test_not_run_or_failed_layer_cannot_be_overall_pass(self) -> None:
        result, failures = quality_gate.final_quality_decision(
            [],
            [],
            {
                "pythonCoverageAndProperties": {"result": "PASS"},
                "pwaCoverageAndProperties": {"result": "PASS"},
                "mutation": "NOT RUN",
                "negativeControls": "FAIL",
                "learnerMaintainerDependencySeparation": "PASS",
                "maintainerRuntimeDependencies": "PASS",
            },
        )

        self.assertEqual(result, "FAIL")
        self.assertIn(
            "evidence layer 'mutation' did not pass (result='NOT RUN')",
            failures,
        )
        self.assertIn(
            "evidence layer 'negativeControls' did not pass (result='FAIL')",
            failures,
        )

    def test_missing_maintainer_runtime_dependency_is_explicitly_blocking(
        self,
    ) -> None:
        with mock.patch.object(
            quality_gate.importlib.util,
            "find_spec",
            return_value=None,
        ):
            runtime_failures = quality_gate.validate_runtime_dependencies(
                {"coverage"}
            )

        result, failures = quality_gate.final_quality_decision(
            runtime_failures,
            [],
            {
                "pythonCoverageAndProperties": {"result": "FAIL"},
                "pwaCoverageAndProperties": {"result": "PASS"},
                "mutation": "PASS",
                "negativeControls": "PASS",
                "learnerMaintainerDependencySeparation": "PASS",
                "maintainerRuntimeDependencies": "FAIL",
            },
        )

        self.assertEqual(result, "FAIL")
        self.assertTrue(
            any(
                "maintainer dependency 'coverage' is not installed"
                in failure
                for failure in failures
            )
        )
        self.assertTrue(
            any(
                "evidence layer 'maintainerRuntimeDependencies' did not pass"
                in failure
                for failure in failures
            )
        )

    def test_command_start_error_is_recorded_as_a_failed_command(self) -> None:
        with mock.patch.object(
            quality_gate.subprocess,
            "run",
            side_effect=FileNotFoundError("missing tool"),
        ):
            command = quality_gate.run_command(
                "missing-maintainer-tool",
                ["missing-maintainer-tool"],
                cwd=ROOT,
            )

        result, failures = quality_gate.final_quality_decision(
            [],
            [command],
            {"syntheticLayer": "PASS"},
        )
        self.assertEqual(command["result"], "FAIL")
        self.assertIsNone(command["exitCode"])
        self.assertIn("could not start command", command["output"])
        self.assertEqual(result, "FAIL")
        self.assertTrue(
            any("missing-maintainer-tool" in failure for failure in failures)
        )

    def test_pwa_quality_builds_without_preexisting_dist_before_serial_tests(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            tests_root = root / "app" / "tests"
            tests_root.mkdir(parents=True)
            (tests_root / "property-security.test.mjs").write_text(
                "// synthetic test placeholder\n",
                encoding="utf-8",
            )
            dist_root = root / "app" / "dist"
            observed: list[str] = []

            def fake_run_command(
                name: str,
                command: list[str],
                *,
                cwd: Path,
                environment: dict[str, str] | None = None,
            ) -> dict[str, object]:
                observed.append(name)
                self.assertEqual(cwd, root / "app")
                self.assertEqual(environment["BASE_PATH"], "/ai-workflow-course/")
                self.assertEqual(environment["COURSE1_BUILD_MODE"], "development")
                if name == "pwa-quality-build":
                    self.assertFalse(dist_root.exists())
                    dist_root.mkdir()
                    (dist_root / "index.html").write_text(
                        "fresh build",
                        encoding="utf-8",
                    )
                else:
                    self.assertTrue((dist_root / "index.html").is_file())
                    self.assertIn("--test-concurrency=1", command)
                return {
                    "name": name,
                    "command": command,
                    "cwd": str(cwd),
                    "exitCode": 0,
                    "result": "PASS",
                    "output": "ok",
                }

            with (
                mock.patch.dict(
                    quality_gate.os.environ,
                    {"GITHUB_ACTIONS": "false"},
                ),
                mock.patch.object(
                    quality_gate,
                    "run_command",
                    side_effect=fake_run_command,
                ),
            ):
                result, commands, failures = quality_gate.run_pwa_quality_layer(
                    Path("node"),
                    self.contract,
                    root=root,
                )

        self.assertEqual(observed, ["pwa-quality-build", "pwa-properties-and-coverage"])
        self.assertEqual([command["name"] for command in commands], observed)
        self.assertEqual(result["result"], "PASS")
        self.assertEqual(failures, [])

    def test_pwa_quality_uses_fail_closed_candidate_mode_on_github(self) -> None:
        self.assertEqual(
            quality_gate.quality_pwa_build_mode(
                {"GITHUB_ACTIONS": "true", "GITHUB_SHA": "not-a-full-sha"}
            ),
            "candidate",
        )
        self.assertEqual(
            quality_gate.quality_pwa_build_mode(
                {"GITHUB_ACTIONS": "false", "COURSE1_BUILD_MODE": "candidate"}
            ),
            "development",
        )

    def test_failed_pwa_build_blocks_tests_and_quality_result(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            tests_root = root / "app" / "tests"
            tests_root.mkdir(parents=True)
            (tests_root / "property-security.test.mjs").write_text(
                "// synthetic test placeholder\n",
                encoding="utf-8",
            )
            build_failure = {
                "name": "pwa-quality-build",
                "command": ["node", "scripts/build.mjs"],
                "cwd": "app",
                "exitCode": 1,
                "result": "FAIL",
                "output": "injected build failure",
            }
            with (
                mock.patch.dict(
                    quality_gate.os.environ,
                    {"GITHUB_ACTIONS": "false"},
                ),
                mock.patch.object(
                    quality_gate,
                    "run_command",
                    return_value=build_failure,
                ) as run,
            ):
                result, commands, failures = quality_gate.run_pwa_quality_layer(
                    Path("node"),
                    self.contract,
                    root=root,
                )

        self.assertEqual(run.call_count, 1)
        self.assertEqual(commands, [build_failure])
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(any("pre-existing app/dist" in item for item in failures))

        overall, overall_failures = quality_gate.final_quality_decision(
            failures,
            commands,
            {"pwaCoverageAndProperties": result},
        )
        self.assertEqual(overall, "FAIL")
        self.assertTrue(overall_failures)

    def test_windows_setup_preserves_beginner_dependency_boundary(self) -> None:
        text = (ROOT / "SETUP_WINDOWS.md").read_text(encoding="utf-8")
        for required in (
            "Do not install Node.js or n8n",
            "& $pythonExe -m pip list --format=freeze",
            r"evidence\setup-dependencies.txt",
            "--require-hashes",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_browser_smoke_keeps_exact_responsive_viewport_matrix(self) -> None:
        text = (ROOT / "app" / "scripts" / "browser-smoke.mjs").read_text(
            encoding="utf-8"
        )
        block = re.search(
            r"const viewportCases = \[(?P<body>[\s\S]+?)\n\s*\];",
            text,
        )
        self.assertIsNotNone(block)
        observed = [
            (int(width), int(height), label)
            for width, height, label in re.findall(
                r'\{ width: (\d+), height: (\d+), label: "([^"]+)" \}',
                block.group("body"),
            )
        ]
        self.assertEqual(
            observed,
            [
                (320, 568, "small phone portrait"),
                (390, 844, "phone portrait"),
                (430, 932, "large phone portrait"),
                (834, 1112, "tablet portrait"),
                (1440, 900, "desktop"),
                (844, 390, "short landscape"),
            ],
        )

    def test_browser_target_size_allows_only_subpixel_rounding(self) -> None:
        text = (ROOT / "app" / "scripts" / "browser-smoke.mjs").read_text(
            encoding="utf-8"
        )
        for required in (
            "const minimumTargetSize = 44;",
            "const targetSizeTolerance = 0.01;",
            "viewportLayout.primaryHeight + targetSizeTolerance >= minimumTargetSize",
            "button.width + targetSizeTolerance >= minimumTargetSize",
            "button.height + targetSizeTolerance >= minimumTargetSize",
            "measured ${button.width} by ${button.height} pixels",
            "allowing ${targetSizeTolerance} pixel browser-rounding tolerance",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
