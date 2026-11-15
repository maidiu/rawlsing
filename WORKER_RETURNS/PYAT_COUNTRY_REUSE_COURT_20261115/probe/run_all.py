"""Bounded one-pass runner for the country-reuse court.

Runs preflight -> estate build -> 1/100 cold+grouped court -> summary -> focused
read-only tests.  No automatic repetitions and no background jobs.
"""
from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
REPO = BASE.parents[1]
E = BASE / "evidence"
L = BASE / "logs"
L.mkdir(exist_ok=True)
E.mkdir(exist_ok=True)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> int:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = f"{REPO}:{HERE}"
    commands = []
    started_all = time.monotonic()
    plan = [
        ("preflight", [sys.executable, str(HERE / "preflight.py")]),
        ("build_estate", [sys.executable, str(HERE / "build_estate.py")]),
        ("run_court", [sys.executable, str(HERE / "run_court.py")]),
        ("state_probe", [sys.executable, str(HERE / "state_probe.py")]),
        ("summarize", [sys.executable, str(HERE / "summarize.py")]),
        (
            "focused_existing_tests",
            [
                sys.executable, "-m", "pytest", "-q", "-o", "addopts=",
                "-p", "no:cacheprovider",
                "rawlsing_next/tests/test_pre553_i03_grouping.py",
                "rawlsing_next/tests/test_pre553_direct_estate_i03.py::test_cold_i03_rejects_grouped_cache_and_i05_outside_s2c_scope",
            ],
        ),
    ]
    for name, argv in plan:
        started = time.monotonic()
        started_utc = utc_now()
        completed = subprocess.run(
            argv, cwd=REPO, env=env, capture_output=True, text=True,
            timeout=280,
        )
        wall = time.monotonic() - started
        (L / f"{name}.stdout.log").write_text(completed.stdout, encoding="utf-8")
        (L / f"{name}.stderr.log").write_text(completed.stderr, encoding="utf-8")
        row = {
            "name": name,
            "argv": argv,
            "cwd": str(REPO),
            "started_utc": started_utc,
            "finished_utc": utc_now(),
            "wall_seconds": wall,
            "exit_code": completed.returncode,
            "stdout_log": f"logs/{name}.stdout.log",
            "stderr_log": f"logs/{name}.stderr.log",
            "stdout_tail": completed.stdout[-4000:],
            "stderr_tail": completed.stderr[-4000:],
        }
        commands.append(row)
        if completed.returncode != 0:
            break
    document = {
        "schema": "PYAT_COUNTRY_REUSE_COMMANDS@1",
        "grade": "SOURCEFREE_TEST_ONLY",
        "started_utc": utc_now(),
        "total_wall_seconds": time.monotonic() - started_all,
        "commands": commands,
        "all_exit_zero": all(row["exit_code"] == 0 for row in commands),
    }
    (E / "commands.json").write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "all_exit_zero": document["all_exit_zero"],
        "total_wall_seconds": document["total_wall_seconds"],
        "commands": [
            {
                "name": row["name"],
                "exit_code": row["exit_code"],
                "wall_seconds": row["wall_seconds"],
            }
            for row in commands
        ],
    }, indent=2, sort_keys=True))
    return 0 if document["all_exit_zero"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
