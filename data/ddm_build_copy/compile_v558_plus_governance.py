#!/usr/bin/env python3
"""Compile the V558+ runtime governance bundle."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v558_plus_governance import (  # noqa: E402
    DEFAULT_V558_PLUS_OUTPUT_ROOT,
    build_v558_plus_governance,
    validate_v558_plus_governance,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile the V558+ runtime governance bundle.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--v558-run-root", required=True)
    parser.add_argument("--output-root", default=str(DEFAULT_V558_PLUS_OUTPUT_ROOT))
    parser.add_argument("--governance-root", default=None)
    parser.add_argument("--write-csv", action="store_true", default=False)
    parser.add_argument("--write-parquet", action="store_true", default=True)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    readiness = build_v558_plus_governance(
        run_id=args.run_id,
        v558_run_root=args.v558_run_root,
        output_root=args.output_root,
        governance_root=args.governance_root,
        write_csv=args.write_csv,
        write_parquet=args.write_parquet,
    )
    errors = validate_v558_plus_governance(readiness)
    if errors:
        raise RuntimeError("V558_PLUS_GOVERNANCE_VALIDATION_FAILED: " + "; ".join(errors))
    if args.verbose:
        print(f"[V558+] status={readiness['status']}")
        print(f"[V558+] report={readiness['build_ledger_path']}")
        print(f"[V558+] blockers={readiness['blocker_count']}")
        print(f"[V558+] runtime_gate={readiness['artifact_paths']['runtime_gate']['json_path']}")
    else:
        print(readiness["status"])
        print(readiness["build_ledger_path"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
