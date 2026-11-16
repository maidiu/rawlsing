#!/usr/bin/env python3
"""Reproducible P3 vertical A-H proof runner.

This runner executes only when the independently returned normalized PsycheStore
module is present. Missing store is an explicit dependency disposition, never a
silent skip, fake store or in-memory fallback.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENGINE_ROOT = ROOT.parent / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
PROJECTION_ROOT = ROOT.parent / "SOROK-S45-S47-PROJECTION-20261105-R1"
TEST_FILE = ROOT / "tests" / "test_p3_vertical_slice.py"
STORE = ROOT / "p3" / "state_store.py"
STORE_MISSING = "DEPENDENT_EXECUTION_NOT_RUN_MISSING_RETURNED_STATE_STORE"


def status(status: str, **extra: object) -> dict:
    return {"schema": "SOROK_P3_VERTICAL_RUNNER@1.0.0", "status": status,
            "store_path": str(STORE), "store_present": STORE.is_file(),
            "test_file": str(TEST_FILE), **extra}


def _metrics_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--metrics-path", default="evidence/full-vertical-execution/actual_metrics.json",
        help="Machine-readable resource receipt path; defaults to the new evidence directory.",
    )
    parser.add_argument(
        "--test", action="append", dest="tests", default=None,
        help="Optional pytest node ID (without file prefix), repeatable for a scoped actual run.",
    )
    parser.add_argument(
        "--timeout", type=float, default=0.0,
        help="Finite subprocess timeout in seconds; 0 disables an outer timeout.",
    )
    args = parser.parse_args()
    if not STORE.is_file():
        result = status(STORE_MISSING, executed=False,
                        reason="returned normalized PsycheStore not present at startup")
        print(json.dumps(result, indent=2, sort_keys=True))
        return 3
    payload = status("RUNNING", executed=True)
    target = str(TEST_FILE) if not args.tests else "::".join(
        [str(TEST_FILE), *args.tests])
    payload["command"] = [sys.executable, "-m", "pytest", target,
                          "-q", "-o", "addopts=", "-p", "no:cacheprovider"]
    payload["tests"] = args.tests
    payload["timeout_seconds"] = args.timeout or None
    env = dict(os.environ)
    paths = [str(ROOT), str(ENGINE_ROOT), str(PROJECTION_ROOT)]
    env["PYTHONPATH"] = os.pathsep.join(
        paths + ([env["PYTHONPATH"]] if env.get("PYTHONPATH") else []))
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONHASHSEED"] = "0"
    metrics_path = _metrics_path(args.metrics_path)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    env["P3_VERTICAL_METRICS_PATH"] = str(metrics_path)
    payload["metrics_path"] = str(metrics_path)
    try:
        completed = subprocess.run(
            payload["command"], cwd=str(ROOT), env=env,
            capture_output=True, text=True,
            timeout=args.timeout if args.timeout > 0 else None,
        )
    except subprocess.TimeoutExpired as exc:
        payload["exit"] = 124
        payload["stdout"] = (exc.stdout or "") if isinstance(exc.stdout, str) else ""
        payload["stderr"] = (exc.stderr or "") if isinstance(exc.stderr, str) else ""
        payload["status"] = "TIMEOUT"
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 124
    payload["exit"] = completed.returncode
    payload["stdout"] = completed.stdout
    payload["stderr"] = completed.stderr
    payload["status"] = "PASS" if completed.returncode == 0 else "FAIL"
    print(json.dumps(payload, indent=2, sort_keys=True))
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
