"""PYAT HQ292 I01K — evidence recorder for typed selection-key restore repair."""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import time


def run_tests(cmd: list[str]) -> dict:
    started = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True,
                            cwd="/Users/matthewsmith/Desktop/Rawlsing")
    return {
        "cmd": " ".join(cmd),
        "exit_code": result.returncode,
        "elapsed_seconds": round(time.time() - started, 3),
        "stdout_tail": result.stdout[-500:] if result.stdout else "",
    }


def main() -> dict:
    return {
        "frozen_typed_index": run_tests([
            sys.executable, "-m", "pytest",
            "WORKER_RETURNS/PYAT-R3-HQ291-S00V3X-INDEPENDENT-OFFLINE-EXECUTION-R1/repro/test_hq291_s00v3x_typed_index.py", "-v"
        ]),
        "i01k_tests": run_tests([
            sys.executable, "-m", "pytest",
            "rawlsing_next/tests/test_hq292_i01k_typed_selection_restore.py", "-v"
        ]),
        "i01_author": run_tests([
            sys.executable, "-m", "pytest",
            "rawlsing_next/tests/test_hq287_i01_sourcefree_world_lifecycle.py", "-q"
        ]),
        "i01r_independent": run_tests([
            sys.executable, "-m", "pytest",
            "rawlsing_next/tests/test_hq288_i01r_independent_product.py", "-q"
        ]),
    }


if __name__ == "__main__":
    result = main()
    out = pathlib.Path(__file__).parent / "i01k_evidence.json"
    out.write_text(json.dumps(result, indent=2, default=str))
    print(f"evidence written to {out}")
    for name, r in result.items():
        print(f"{name}: exit={r['exit_code']} elapsed={r['elapsed_seconds']}s")
