"""Print the exact identity block for a built Course 1 Pages artifact."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from verify_course1_promotion import (
    ROOT,
    inspect_artifact_identity,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--dist", type=Path, default=ROOT / "app" / "dist")
    parser.add_argument(
        "--operation",
        choices=("promote", "rollback"),
        default="promote",
    )
    args = parser.parse_args()

    commit = args.commit.strip().casefold()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        print("commit must be a full lower-case 40-character Git SHA", file=sys.stderr)
        return 1

    try:
        dist = args.dist.resolve()
        inspected = inspect_artifact_identity(
            dist,
            expected_commit=commit,
            operation=args.operation,
        )
        version = inspected["version"]
        identity = {
            "artifactFormat": inspected["artifactFormat"],
            "commit": commit,
            "courseVersion": version["courseVersion"],
            "buildId": version["buildId"],
            "contentHash": version["contentHash"],
            "assetManifestSha256": inspected["assetManifestSha256"],
            "artifactTreeSha256": inspected["artifactTreeSha256"],
        }
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(json.dumps(identity, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
