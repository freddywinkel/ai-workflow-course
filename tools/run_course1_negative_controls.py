#!/usr/bin/env python3
"""Run the Course 1 family-level negative controls in disposable copies."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--node",
        type=Path,
        default=Path(shutil.which("node") or "node"),
    )
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    command = [
        sys.executable,
        str(ROOT / "tools" / "run_course1_mutations.py"),
        "--profile",
        "negative",
        "--node",
        str(args.node),
    ]
    if args.report:
        command.extend(["--report", str(args.report)])
    return subprocess.run(command, cwd=ROOT, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
