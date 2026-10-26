#!/usr/bin/env python3
"""Render one machine-consumable all35 reuse preparation record."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
from all35_reuse_binder import build_source  # noqa: E402


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-id", required=True)
    args = parser.parse_args(argv)
    print(json.dumps(build_source(args.source_id), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
