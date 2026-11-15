#!/usr/bin/env python3
"""Compile the V555 thin layer artifact."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v5_thin_end_to_end import build_thin_layer  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile the v555 thin Rawlsing layer.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--input-root", required=True)
    parser.add_argument("--output-root", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    readiness = build_thin_layer(layer="v555", run_id=args.run_id, input_root=args.input_root, output_root=args.output_root)
    print(readiness["status"])
    print(readiness["packet_path"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
