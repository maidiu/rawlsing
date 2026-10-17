#!/usr/bin/env python3
"""Compile the V558 runtime input gate."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v558_runtime_input_gate import (  # noqa: E402
    DEFAULT_V558_OUTPUT_ROOT,
    build_v558_runtime_input_gate,
    validate_v558_runtime_input_gate,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile the V558 runtime input gate.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--v557-run-root", required=True)
    parser.add_argument("--output-root", default=str(DEFAULT_V558_OUTPUT_ROOT))
    parser.add_argument("--governance-root", default=None)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    readiness = build_v558_runtime_input_gate(
        run_id=args.run_id,
        v557_run_root=args.v557_run_root,
        output_root=args.output_root,
        governance_root=args.governance_root,
    )
    errors = validate_v558_runtime_input_gate(readiness)
    if errors:
        raise RuntimeError("V558_RUNTIME_INPUT_GATE_VALIDATION_FAILED: " + "; ".join(errors))
    if args.verbose:
        print(f"[V558] status={readiness['status']}")
        print(f"[V558] report={readiness['report_path']}")
        print(f"[V558] gate={readiness['gate_packet_path']}")
        print(f"[V558] build_ledger={readiness['build_ledger_path']}")
        print(f"[V558] blockers={readiness['blocker_count']}")
    else:
        print(readiness["status"])
        print(readiness["report_path"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
