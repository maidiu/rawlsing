#!/usr/bin/env python3
"""Execute the RRIF-E sourcefree first consumer and print its receipt."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = next(parent for parent in ROOT.parents if (parent / ".git").exists())
for path in (str(ROOT), str(ROOT / "rrif_r3_extension"), str(REPO)):
    if path not in sys.path:
        sys.path.insert(0, path)

from joined.first_consumer import run_first_consumer  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args(argv)
    print(json.dumps(run_first_consumer(args.root), indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
