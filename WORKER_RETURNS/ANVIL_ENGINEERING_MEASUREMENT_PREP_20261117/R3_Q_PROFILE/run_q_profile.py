#!/usr/bin/env python3
"""External supervisor for ONE profiled query; no retry/matrix."""
from __future__ import annotations

import hashlib
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "vendor"))

from court_instrumentation import directory_bytes, process_tree_rss_bytes  # noqa: E402

CAP_SECONDS = 120.0
RSS_LIMIT = 2 * 1024**3
SCRATCH_LIMIT = 2 * 1024**3
SCRATCH_ROOT = ROOT / ".local-data-pilot"


def main() -> int:
    command = [sys.executable, str(HERE / "profile_q.py")]
    started = time.monotonic()
    process = subprocess.Popen(
        command, cwd=str(REPO), text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, start_new_session=True,
    )
    samples = []
    aborted = None
    while process.poll() is None:
        time.sleep(0.25)
        elapsed = time.monotonic() - started
        rss = process_tree_rss_bytes(process.pid)
        scratch = directory_bytes(SCRATCH_ROOT)
        samples.append({"elapsed_seconds": elapsed,
                        "process_tree_rss_bytes": rss,
                        "scratch_bytes": scratch})
        if elapsed > CAP_SECONDS:
            aborted = f"WALL_LIMIT:{CAP_SECONDS}"
            break
        if rss > RSS_LIMIT:
            aborted = f"RSS_LIMIT:{rss}>{RSS_LIMIT}"
            break
        if scratch > SCRATCH_LIMIT:
            aborted = f"SCRATCH_LIMIT:{scratch}>{SCRATCH_LIMIT}"
            break
    if aborted:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait(timeout=3)
    stdout, stderr = process.communicate(timeout=10)
    wall = time.monotonic() - started
    child = None
    child_path = HERE / "child_result.json"
    if child_path.exists():
        child = json.loads(child_path.read_text())
    result = {
        "schema": "ANVIL_CUT2_R3_Q_PROFILE_SUPERVISED@1",
        "command": command,
        "exit": process.returncode,
        "aborted": aborted,
        "external_wall_seconds": wall,
        "sample_count": len(samples),
        "process_tree_rss_peak_sampled_bytes": max(
            (s["process_tree_rss_bytes"] for s in samples), default=0),
        "scratch_peak_sampled_bytes": max(
            (s["scratch_bytes"] for s in samples), default=0),
        "caps": {
            "wall_seconds": CAP_SECONDS,
            "process_tree_rss_bytes": RSS_LIMIT,
            "scratch_bytes": SCRATCH_LIMIT,
            "sampling_seconds": 0.25,
        },
        "stdout": stdout,
        "stderr": stderr,
        "child": child,
        "harness_sha256": hashlib.sha256(
            (ROOT / "measure_cut1_prepared.py").read_bytes()).hexdigest(),
        "product_candidate": "347baec696c8b395d750ac3b9e74417a6490c223",
        "cut1_review": "092bf29ffa6724d477abb4ccfc770e3bc492250d",
    }
    (HERE / "RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n")
    (HERE / "samples.json").write_text(
        json.dumps(samples, indent=2, sort_keys=True) + "\n")
    (HERE / "stdout.txt").write_text(stdout)
    (HERE / "stderr.txt").write_text(stderr)
    print(json.dumps({
        "exit": process.returncode,
        "aborted": aborted,
        "wall": wall,
        "rss_peak": result["process_tree_rss_peak_sampled_bytes"],
        "scratch_peak": result["scratch_peak_sampled_bytes"],
        "child_status": (child or {}).get("status"),
    }, sort_keys=True))
    return process.returncode or (1 if aborted else 0)


if __name__ == "__main__":
    raise SystemExit(main())
