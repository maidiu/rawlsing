#!/usr/bin/env python3
"""External supervisor for ONE locality profile; no retry."""
from __future__ import annotations

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

CAP = 120.0
RSS = 2 * 1024**3
SCRATCH = 2 * 1024**3


def main() -> int:
    cmd = [sys.executable, str(HERE / "locality_profile.py")]
    started = time.monotonic()
    p = subprocess.Popen(cmd, cwd=str(REPO), text=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, start_new_session=True)
    samples = []
    aborted = None
    while p.poll() is None:
        time.sleep(0.25)
        elapsed = time.monotonic() - started
        rss = process_tree_rss_bytes(p.pid)
        scratch = directory_bytes(ROOT / ".local-data-pilot")
        samples.append({"elapsed_seconds": elapsed,
                        "process_tree_rss_bytes": rss,
                        "scratch_bytes": scratch})
        if elapsed > CAP:
            aborted = f"WALL_LIMIT:{CAP}"
        elif rss > RSS:
            aborted = f"RSS_LIMIT:{rss}>{RSS}"
        elif scratch > SCRATCH:
            aborted = f"SCRATCH_LIMIT:{scratch}>{SCRATCH}"
        if aborted:
            break
    if aborted:
        try:
            os.killpg(p.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            p.wait(timeout=3)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            p.wait(timeout=3)
    out, err = p.communicate(timeout=10)
    child = json.loads((HERE / "child_result.json").read_text()) if (HERE / "child_result.json").exists() else None
    result = {
        "schema": "ANVIL_CUT2_R4_LOCALITY_SUPERVISED@1",
        "command": cmd, "exit": p.returncode, "aborted": aborted,
        "external_wall_seconds": time.monotonic() - started,
        "sample_count": len(samples),
        "process_tree_rss_peak_sampled_bytes": max(
            (s["process_tree_rss_bytes"] for s in samples), default=0),
        "scratch_peak_sampled_bytes": max(
            (s["scratch_bytes"] for s in samples), default=0),
        "caps": {"wall_seconds": CAP, "process_tree_rss_bytes": RSS,
                 "scratch_bytes": SCRATCH, "sampling_seconds": 0.25},
        "stdout": out, "stderr": err, "child": child,
        "product_candidate": "347baec696c8b395d750ac3b9e74417a6490c223",
        "cut1_review": "092bf29ffa6724d477abb4ccfc770e3bc492250d",
    }
    (HERE / "RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    (HERE / "samples.json").write_text(json.dumps(samples, indent=2, sort_keys=True) + "\n")
    (HERE / "stdout.txt").write_text(out)
    (HERE / "stderr.txt").write_text(err)
    print(json.dumps({"exit": p.returncode, "aborted": aborted,
                      "wall": result["external_wall_seconds"],
                      "rss": result["process_tree_rss_peak_sampled_bytes"],
                      "scratch": result["scratch_peak_sampled_bytes"],
                      "child": (child or {}).get("status")}, sort_keys=True))
    return p.returncode or (1 if aborted else 0)


if __name__ == "__main__":
    raise SystemExit(main())
