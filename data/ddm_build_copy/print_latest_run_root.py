from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_latest_run import latest_dir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Print the latest run root matching a glob-style pattern.")
    parser.add_argument("pattern", help="Glob-style pattern relative to the search root, e.g. 'gss1993_*' or 'runs/gss1993_*'")
    parser.add_argument(
        "--root",
        default=".",
        help="Search root to resolve against the pattern prefix. Defaults to the current directory.",
    )
    args = parser.parse_args(argv)

    result = latest_dir(Path(args.root), args.pattern)
    if result is None:
        return 1
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
