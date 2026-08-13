#!/usr/bin/env python3
"""Compile the V5 app-facing handoff bundle.

This is the concrete bridge between the thin V551J→V557 chain and the V558+
governance layer. It intentionally stays non-runtime: it packages the latest
available chain outputs into an app-review handoff surface without enabling
persona generation or app wiring.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v5_app_handoff import (  # noqa: E402
    DEFAULT_V5_APP_HANDOFF_OUTPUT_ROOT,
    build_v5_app_handoff_bundle,
    validate_v5_app_handoff_bundle,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile the V5 app-facing handoff bundle.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--wave", required=True)
    parser.add_argument("--thin-run-root", required=True)
    parser.add_argument("--v558-plus-run-root", required=True)
    parser.add_argument("--output-root", default=str(DEFAULT_V5_APP_HANDOFF_OUTPUT_ROOT))
    parser.add_argument("--write-csv", action="store_true", default=False)
    parser.add_argument("--write-parquet", action="store_true", default=True)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    readiness = build_v5_app_handoff_bundle(
        run_id=args.run_id,
        wave=args.wave,
        thin_run_root=args.thin_run_root,
        v558_plus_run_root=args.v558_plus_run_root,
        output_root=args.output_root,
        write_csv=args.write_csv,
        write_parquet=args.write_parquet,
    )
    errors = validate_v5_app_handoff_bundle(readiness)
    if errors:
        raise RuntimeError("V5_APP_HANDOFF_VALIDATION_FAILED: " + "; ".join(errors))
    if args.verbose:
        print(f"[V5_APP] status={readiness['status']}")
        print(f"[V5_APP] report={readiness['readiness_report_path']}")
        print(f"[V5_APP] blockers={readiness['blocker_count']}")
        print(f"[V5_APP] packet={readiness['packet_path']}")
    else:
        print(readiness["status"])
        print(readiness["readiness_report_path"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
