#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
from all35_complete_metadata import build_all35  # noqa: E402


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-id", required=True)
    args = parser.parse_args(argv)
    records = build_all35()["records"]
    if args.source_id not in records:
        raise SystemExit(f"unknown source {args.source_id}")
    print(json.dumps(records[args.source_id], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
