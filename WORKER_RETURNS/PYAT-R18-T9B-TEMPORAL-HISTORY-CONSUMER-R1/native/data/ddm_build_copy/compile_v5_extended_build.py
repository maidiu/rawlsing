#!/usr/bin/env python3
"""Compile the extended V5 build: V553 harmonization plus the thin forward path."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v5_extended_build import build_v5_extended_build


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile the extended Rawlsing V5 build.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--v551j-run-root", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--country-code", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = build_v5_extended_build(
        run_id=args.run_id,
        repo_root=args.repo_root,
        v551j_run_root=args.v551j_run_root,
        output_root=args.output_root,
        survey_family=args.source,
        country_code=args.country_code,
    )
    print(summary["final_status"])
    print(str(Path(args.output_root) / args.run_id / "manifest" / "v5_extended_build_readiness_report.json"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
