#!/usr/bin/env python3
"""Build the V550 question-use contract."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v550_question_use import build_question_use_contract


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the V550 question-use contract.")
    parser.add_argument("--input", required=True, help="Input parquet/csv containing question metadata.")
    parser.add_argument("--output", required=True, help="Output parquet path for the question-use contract.")
    parser.add_argument("--csv-output", default=None, help="Optional CSV mirror.")
    parser.add_argument(
        "--source",
        default="",
        help="Survey family. Required unless the input contains exactly one source value.",
    )
    parser.add_argument(
        "--wave",
        default="",
        help="Canonical wave. Required unless the input contains exactly one wave value.",
    )
    parser.add_argument(
        "--question-use-overrides",
        default=None,
        help="Optional manual designation CSV. Defaults to the repository manifest when omitted.",
    )
    parser.add_argument(
        "--wave-itinerary",
        default=None,
        help="Optional wave review itinerary CSV. Defaults to the repository manifest when omitted.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    if input_path.suffix.lower() == ".parquet":
        frame = pd.read_parquet(input_path)
    else:
        frame = pd.read_csv(input_path, low_memory=False)
    contract = build_question_use_contract(
        frame,
        question_use_overrides_path=Path(args.question_use_overrides) if args.question_use_overrides else None,
        wave_itinerary_path=Path(args.wave_itinerary) if args.wave_itinerary else None,
        survey_family=args.source,
        canonical_wave=args.wave,
    )
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    contract.to_parquet(output_path, index=False)
    if args.csv_output:
        csv_path = Path(args.csv_output)
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        contract.to_csv(csv_path, index=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
