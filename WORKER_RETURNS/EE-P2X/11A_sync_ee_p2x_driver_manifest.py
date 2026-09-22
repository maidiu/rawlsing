#!/usr/bin/env python3
"""Synchronize the normalized EE-P2X court manifest from the Darwin driver ledger.

No carrier is opened and no measured value is invented. This is a convenience
entrypoint over the driver-bound verifier's --sync-only mode.
"""
from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
BRIDGE = HERE / "12A_verify_ee_p2x_driver_bound_local_court.py"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--driver-work-root", type=Path, required=True)
    args = ap.parse_args(argv)
    spec = importlib.util.spec_from_file_location("_ee_p2x_driver_bound_verifier", BRIDGE)
    if spec is None or spec.loader is None:
        raise SystemExit("BLOCKER__DRIVER_BOUND_VERIFIER_IMPORT")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    raise SystemExit(mod.main(["--driver-work-root", str(args.driver_work_root), "--sync-only"]))


if __name__ == "__main__":
    main()
