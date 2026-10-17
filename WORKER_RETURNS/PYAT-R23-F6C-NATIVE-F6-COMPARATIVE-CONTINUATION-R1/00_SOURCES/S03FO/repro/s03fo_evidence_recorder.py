"""PYAT HQ287 S03FO — evidence recorder for the canonical order repair."""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import time


def run_tests(cmd: list[str]) -> dict:
    import os
    started = time.time()
    env = dict(os.environ, S03FO_CANDIDATE_ROOT=".", PYTHONPATH=".")
    result = subprocess.run(cmd, capture_output=True, text=True,
                            cwd="/Users/matthewsmith/Desktop/Rawlsing", env=env)
    return {
        "cmd": " ".join(cmd),
        "exit_code": result.returncode,
        "elapsed_seconds": round(time.time() - started, 3),
        "stdout_tail": result.stdout[-500:] if result.stdout else "",
    }


def main() -> dict:
    return {
        "original_s03_tests": run_tests([
            sys.executable, "-m", "pytest",
            "rawlsing_next/tests/test_pre553_heterogeneous_synthesis.py", "-q"
        ]),
        "s03fo_court": run_tests([
            sys.executable, "-m", "pytest",
            "rawlsing_next/tests/test_hq287_s03fo_f6_canonical_order_court.py", "-v"
        ]),
        "combined": run_tests([
            sys.executable, "-m", "pytest",
            "rawlsing_next/tests/test_pre553_heterogeneous_synthesis.py",
            "rawlsing_next/tests/test_hq287_s03fo_f6_canonical_order_court.py", "-q"
        ]),
    }


if __name__ == "__main__":
    result = main()
    out = pathlib.Path(__file__).parent / "s03fo_evidence.json"
    out.write_text(json.dumps(result, indent=2, default=str))
    print(f"evidence written to {out}")
    for name, r in result.items():
        print(f"{name}: exit={r['exit_code']} elapsed={r['elapsed_seconds']}s")
