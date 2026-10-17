#!/usr/bin/env python3
"""Compile the V553 thin layer artifact."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v5_thin_end_to_end import build_thin_layer  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile the v553 thin Rawlsing layer.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--input-root", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--source", required=True, help="Explicit survey family")
    parser.add_argument("--country-code", required=True, help="Explicit country code")
    parser.add_argument("--v553-temporal-context-root")
    parser.add_argument("--v553-wave-harmonization-root")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    readiness = build_thin_layer(
        layer="v553",
        run_id=args.run_id,
        input_root=args.input_root,
        output_root=args.output_root,
        survey_family=args.source,
        country_code=args.country_code,
        v553_temporal_context_root=args.v553_temporal_context_root,
        v553_wave_harmonization_root=args.v553_wave_harmonization_root,
    )
    print(readiness["status"])
    print(readiness["packet_path"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
