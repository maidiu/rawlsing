"""Supervise the existing real country campaign court, not a mock benchmark.

Sample aggregate worker-tree RSS and workspace disk (including staging and
uncommitted files) from outside the worker. Sample maxima are lower bounds,
not an absolute process or filesystem high-water guarantee. No original data.
Run with the pinned repository dependencies plus psutil, e.g.
  python -m tools.pyat_country_campaign_court --rows 128,192,256
Use --root on an empty private directory to retain the generated artifacts.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import tempfile
import time

import psutil

LIMIT = 6 * 1024**3
TEST = ("rawlsing_next.tests.test_pre553_country_numeric_economics."
        "CountryNativeEconomics.test_grouped_country_campaign_economics")


def disk_snapshot(root):
    seen = set()
    scratch_seen = set()
    logical = allocated = scratch = scratch_allocated = 0
    for directory, _, files in os.walk(root):
        base = Path(directory)
        relative = base.relative_to(root)
        staging_dir = any(part.startswith((".staging-", ".country-")) or part == "tmp"
                          for part in relative.parts)
        for name in files:
            path = base / name
            try:
                st = path.stat()
            except FileNotFoundError:
                # Atomic publication may move a file during the sample.
                continue
            key = (st.st_dev, st.st_ino)
            if key not in seen:
                seen.add(key)
                logical += st.st_size
                allocated += getattr(st, "st_blocks", 0) * 512
            temporary = (staging_dir or ".tmp-" in name or name.endswith(
                         (".tmp", "-journal", "-wal", "-shm")) or name.startswith(".country-"))
            if temporary and key not in scratch_seen:
                scratch_seen.add(key)
                scratch += st.st_size
                scratch_allocated += getattr(st, "st_blocks", 0) * 512
    return {"workspace_logical_bytes": logical, "workspace_allocated_bytes": allocated,
            "temporary_logical_bytes": scratch, "temporary_allocated_bytes": scratch_allocated}


def sample_tree(pid):
    try:
        root = psutil.Process(pid)
        processes = [root, *root.children(recursive=True)]
    except psutil.NoSuchProcess:
        return 0, 0
    rss = count = 0
    for process in processes:
        try:
            rss += process.memory_info().rss
            count += 1
        except psutil.NoSuchProcess:
            continue
    return rss, count


def kill_tree(proc):
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def supervise(root, rows, interval):
    root = root.resolve()
    if not root.is_dir() or any(root.iterdir()):
        raise ValueError("campaign root must be an existing empty private directory")
    (root / "tmp").mkdir()
    env = dict(os.environ, PYAT_R9_CAMPAIGN_ROOT=str(root),
               PYAT_R9_COUNTRY_ROWS=rows, TMPDIR=str(root / "tmp"),
               PYTHONUNBUFFERED="1")
    started = time.monotonic()
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    proc = subprocess.Popen([sys.executable, "-m", "unittest", TEST, "-v"],
                            env=env, start_new_session=True)
    maxima = {}
    counts = {}
    phase = "startup"
    exceeded = False
    samples = 0
    max_gap = 0.0
    previous = started
    try:
        while True:
            now = time.monotonic()
            max_gap = max(max_gap, now - previous)
            previous = now
            try:
                phase = json.loads((root / "phase.json").read_text())["phase"]
            except (FileNotFoundError, json.JSONDecodeError):
                pass
            rss, live = sample_tree(proc.pid)
            snap = {"aggregate_worker_tree_rss_bytes": rss, "live_processes": live,
                    **disk_snapshot(root)}
            for label in ("all", phase):
                peak = maxima.setdefault(label, {})
                for key, value in snap.items():
                    peak[key] = max(peak.get(key, 0), value)
                counts[label] = counts.get(label, 0) + 1
            samples += 1
            if rss > LIMIT:
                exceeded = True
                kill_tree(proc)
                break
            if proc.poll() is not None:
                break
            time.sleep(interval)
    except BaseException:
        kill_tree(proc)
        raise
    finally:
        proc.wait()
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    report = {"worker_exit": proc.returncode, "wall_seconds": time.monotonic()-started,
              "child_cpu_user_seconds": after.ru_utime-before.ru_utime,
              "child_cpu_system_seconds": after.ru_stime-before.ru_stime,
              "samples": samples, "requested_interval_seconds": interval,
              "largest_observed_sampling_gap_seconds": max_gap,
              "sample_counts_by_phase": counts, "sampled_peak_by_phase": maxima,
              "final_disk": disk_snapshot(root), "rss_limit_bytes": LIMIT,
              "rss_sample_exceeded_limit": exceeded,
              "scope": "SAMPLED_WORKER_AND_DESCENDANTS_RSS__INODE_DEDUP_DISK__NOT_ABSOLUTE_PEAK",
              "rows_requested": rows,
              "grade": "SOURCEFREE_COUNTRY_CAMPAIGN__NOT_100K_FULL_VERTICAL_OR_ORIGINAL"}
    print("R9_CAMPAIGN_RESOURCE", json.dumps(report, sort_keys=True), flush=True)
    return 1 if exceeded or proc.returncode else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", default="128,192,256")
    parser.add_argument("--sample-seconds", type=float, default=.1)
    parser.add_argument("--root", type=Path)
    args = parser.parse_args()
    if not .02 <= args.sample_seconds <= 1:
        parser.error("sample interval must be within 0.02..1 seconds")
    if args.root is not None:
        return supervise(args.root, args.rows, args.sample_seconds)
    with tempfile.TemporaryDirectory(prefix="pyat-country-campaign-") as directory:
        return supervise(Path(directory), args.rows, args.sample_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
