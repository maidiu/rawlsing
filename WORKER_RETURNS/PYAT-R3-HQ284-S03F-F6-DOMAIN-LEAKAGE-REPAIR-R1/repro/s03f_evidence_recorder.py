"""PYAT HQ284 S03F — before/after evidence for the two defect repairs."""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import time


def run_tests(cmd: list[str]) -> dict:
    started = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, cwd="/Users/matthewsmith/Desktop/Rawlsing")
    return {
        "cmd": " ".join(cmd),
        "exit_code": result.returncode,
        "elapsed_seconds": round(time.time() - started, 3),
        "stdout_tail": result.stdout[-500:] if result.stdout else "",
        "stderr_tail": result.stderr[-500:] if result.stderr else "",
    }


def main() -> dict:
    return {
        "original_s03_tests": run_tests([
            sys.executable, "-m", "pytest",
            "rawlsing_next/tests/test_pre553_heterogeneous_synthesis.py", "-q"
        ]),
        "independent_hostile_tests": run_tests([
            sys.executable, "-m", "pytest",
            "rawlsing_next/tests/test_hq283_s03r_f6_method_hostile.py", "-v"
        ]),
        "combined": run_tests([
            sys.executable, "-m", "pytest",
            "rawlsing_next/tests/test_pre553_heterogeneous_synthesis.py",
            "rawlsing_next/tests/test_hq283_s03r_f6_method_hostile.py", "-q"
        ]),
    }


if __name__ == "__main__":
    result = main()
    out = pathlib.Path(__file__).parent / "s03f_evidence.json"
    out.write_text(json.dumps(result, indent=2, default=str))
    print(f"evidence written to {out}")
    for name, r in result.items():
        print(f"{name}: exit={r['exit_code']} elapsed={r['elapsed_seconds']}s")
