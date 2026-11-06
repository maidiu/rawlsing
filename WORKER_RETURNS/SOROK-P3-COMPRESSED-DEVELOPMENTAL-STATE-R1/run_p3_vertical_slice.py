#!/usr/bin/env python3
"""Reproducible P3 vertical A-H proof runner.

This runner executes only when the independently returned normalized PsycheStore
module is present. Missing store is an explicit dependency disposition, never a
silent skip, fake store or in-memory fallback.
"""
from __future__ import annotations

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


def main() -> int:
    if not STORE.is_file():
        result = status(STORE_MISSING, executed=False,
                        reason="returned normalized PsycheStore not present at startup")
        print(json.dumps(result, indent=2, sort_keys=True))
        return 3
    payload = status("RUNNING", executed=True)
    payload["command"] = [sys.executable, "-m", "pytest", str(TEST_FILE),
                          "-q", "-o", "addopts=", "-p", "no:cacheprovider"]
    env = dict(os.environ)
    paths = [str(ROOT), str(ENGINE_ROOT), str(PROJECTION_ROOT)]
    env["PYTHONPATH"] = os.pathsep.join(
        paths + ([env["PYTHONPATH"]] if env.get("PYTHONPATH") else []))
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONHASHSEED"] = "0"
    completed = subprocess.run(payload["command"], cwd=str(ROOT),
                               env=env, capture_output=True, text=True)
    payload["exit"] = completed.returncode
    payload["stdout"] = completed.stdout
    payload["stderr"] = completed.stderr
    payload["status"] = "PASS" if completed.returncode == 0 else "FAIL"
    print(json.dumps(payload, indent=2, sort_keys=True))
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
