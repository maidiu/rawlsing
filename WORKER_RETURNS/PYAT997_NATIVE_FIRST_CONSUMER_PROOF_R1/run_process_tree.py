"""Bounded process-tree measurement wrapper for the #997 native proof harness."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import time


ROOT = Path(__file__).resolve().parents[2]


def tree_rss(pid: int) -> int:
    try:
        text = subprocess.check_output(
            ["ps", "-axo", "pid=,ppid=,rss="], text=True, timeout=2)
    except Exception:
        return 0
    rows = {}
    for line in text.splitlines():
        parts = line.split()
        if len(parts) != 3:
            continue
        try:
            p, pp, rss = map(int, parts)
        except ValueError:
            continue
        rows[p] = (pp, rss)
    keys = {pid}
    changed = True
    while changed:
        changed = False
        for p, (pp, _rss) in rows.items():
            if pp in keys and p not in keys:
                keys.add(p)
                changed = True
    return sum(rows.get(p, (0, 0))[1] for p in keys) * 1024


def main() -> int:
    proofroot = Path(sys.argv[1]).resolve()
    evidence = Path(sys.argv[2]).resolve()
    env = os.environ.copy()
    env["PYTHONPATH"] = "."
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    started = time.time()
    proc = subprocess.Popen(
        [sys.executable, "-B",
         str(ROOT / "WORKER_RETURNS/PYAT997_NATIVE_FIRST_CONSUMER_PROOF_R1/native_proof_harness.py"),
         str(proofroot)],
        cwd=str(ROOT), env=env,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    peak = 0
    samples = 0
    stop = threading.Event()

    def sample():
        nonlocal peak, samples
        while not stop.is_set():
            peak = max(peak, tree_rss(proc.pid))
            samples += 1
            time.sleep(0.01)

    thread = threading.Thread(target=sample, daemon=True)
    thread.start()
    try:
        out, err = proc.communicate(timeout=300)
    finally:
        stop.set()
        thread.join(timeout=3)
    elapsed = time.time() - started
    result = {
        "harness_exit": proc.returncode,
        "elapsed_seconds": elapsed,
        "samples": samples,
        "process_tree_peak_rss_bytes": peak,
        "sample_interval_seconds": 0.01,
        "stdout": out,
        "stderr": err,
        "proofroot": str(proofroot),
        "note": "sampled process-tree RSS, not an absolute hardware maximum; single native process tree",
    }
    evidence.parent.mkdir(parents=True, exist_ok=True)
    evidence.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items()
                      if k not in {"stdout", "stderr"}}, indent=2))
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
