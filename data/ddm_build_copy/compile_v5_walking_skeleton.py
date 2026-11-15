#!/usr/bin/env python3
"""Compile the V551J→V557 walking-skeleton control surface."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v5_walking_skeleton import (
    build_walking_skeleton_manifests,
    validate_walking_skeleton_output,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile V5 walking skeleton manifests from a V551J run root.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--v551j-run-root", required=True)
    parser.add_argument("--output-root", required=True)
    parser.add_argument("--strict", action="store_true", default=True)
    parser.add_argument("--no-strict", dest="strict", action="store_false")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    readiness = build_walking_skeleton_manifests(
        run_id=args.run_id,
        v551j_run_root=args.v551j_run_root,
        output_root=args.output_root,
    )
    errors = validate_walking_skeleton_output(readiness)
    if args.strict and errors:
        raise RuntimeError("V5_WALKING_SKELETON_VALIDATION_FAILED: " + "; ".join(errors))
    print(readiness["final_status"])
    print(readiness["contract_path"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
