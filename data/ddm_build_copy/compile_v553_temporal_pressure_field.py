#!/usr/bin/env python3
"""Compile the V553 temporal pressure field artifact."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v553_temporal_pressure import build_v553_temporal_pressure_field, validate_v553_temporal_pressure_readiness  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile the V553 thin temporal pressure field.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--wave-harmonization-report-path", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--write-csv", action="store_true", default=False)
    parser.add_argument("--write-parquet", action="store_true", default=True)
    parser.add_argument(
        "--country-code",
        default="",
        help="Explicit country for the temporal field; required if absent from the harmonization report.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    readiness = build_v553_temporal_pressure_field(
        run_id=args.run_id,
        wave_harmonization_report_path=args.wave_harmonization_report_path,
        output_root=args.output_root,
        write_csv=args.write_csv,
        write_parquet=args.write_parquet,
        country_code=args.country_code,
    )
    errors = validate_v553_temporal_pressure_readiness(readiness)
    if errors:
        raise RuntimeError("V553_TEMPORAL_PRESSURE_VALIDATION_FAILED: " + "; ".join(errors))
    print(readiness["status"])
    print(readiness["packet_path"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
