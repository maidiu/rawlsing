#!/usr/bin/env python3
"""Compile the full V551J→V557 thin end-to-end Rawlsing pipeline."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v5_thin_end_to_end import (  # noqa: E402
    build_v5_thin_end_to_end,
    validate_thin_end_to_end,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile V5 thin end-to-end layer artifacts from a V551J run root.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--v551j-run-root", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--source", required=True, help="Explicit survey family")
    parser.add_argument("--country-code", required=True, help="Explicit country code")
    parser.add_argument("--v553-temporal-context-root")
    parser.add_argument("--v553-wave-harmonization-root")
    parser.add_argument("--strict", action="store_true", default=True)
    parser.add_argument("--no-strict", dest="strict", action="store_false")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = build_v5_thin_end_to_end(
        run_id=args.run_id,
        v551j_run_root=args.v551j_run_root,
        output_root=args.output_root,
        survey_family=args.source,
        country_code=args.country_code,
        v553_temporal_context_root=args.v553_temporal_context_root,
        v553_wave_harmonization_root=args.v553_wave_harmonization_root,
    )
    errors = validate_thin_end_to_end(summary)
    if args.strict and errors:
        raise RuntimeError("V5_THIN_END_TO_END_VALIDATION_FAILED: " + "; ".join(errors))
    print(summary["final_status"])
    print(str(Path(args.output_root) / args.run_id / "manifest" / "v5_thin_end_to_end_readiness_report.json"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
