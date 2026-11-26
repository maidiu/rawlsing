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


def supervise(root, rows, interval, *, risk_mode="factored", shared_source=None):
    root = root.resolve()
    if not root.is_dir() or any(root.iterdir()):
        raise ValueError("campaign root must be an existing empty private directory")
    (root / "tmp").mkdir()
    env = dict(os.environ, PYAT_R9_CAMPAIGN_ROOT=str(root),
               PYAT_R9_COUNTRY_ROWS=rows, TMPDIR=str(root / "tmp"),
               PYTHONUNBUFFERED="1",PYAT_R10_REPLAY_RISK=risk_mode)
    if shared_source is not None:
        env["PYAT_R10_SHARED_SOURCE"]=str(shared_source)
    else:
        env.pop("PYAT_R10_SHARED_SOURCE",None)
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
              "rows_requested": rows,"replay_risk_mode":risk_mode,
              "grade": "SOURCEFREE_COUNTRY_CAMPAIGN__NOT_100K_FULL_VERTICAL_OR_ORIGINAL"}
    print("R9_CAMPAIGN_RESOURCE", json.dumps(report, sort_keys=True), flush=True)
    return 1 if exceeded or proc.returncode else 0


def compare_replay_risk(root,rows,interval,*,factored_first=False):
    """Same exact generated SAV, independently executed/certified campaigns.
    Full-preimage output censuses and release identities must match. A
    single sequential pair is not a statistically controlled timing result.
    """
    root=root.resolve()
    if not root.is_dir() or any(root.iterdir()):
        raise ValueError("matched campaign root must be empty")
    source=root/"shared-generated.sav"
    reports={}
    order=("factored","legacy") if factored_first else ("legacy","factored")
    for mode in order:
        dest=root/mode;dest.mkdir()
        started=time.monotonic()
        if supervise(dest,rows,interval,risk_mode=mode,shared_source=source):
            return 1
        reports[mode]=json.loads((dest/"campaign-proof.json").read_text())
        reports[mode]["outer_wall_seconds"]=time.monotonic()-started
    old,new=reports["legacy"],reports["factored"]
    if (old["source_sha256"]!=new["source_sha256"]
            or old["proofs"]!=new["proofs"]
            or old["country_sha256"]!=new["country_sha256"]
            or old["country_files"]["logical_file_bytes"]!=new["country_files"]["logical_file_bytes"]):
        raise AssertionError("matched campaign source/release/output census/physical estate drift")
    # Compare actual CAS payloads outside the worker resource samples.
    # Root manifests intentionally differ, but no evidence blob should.
    import hashlib
    def inventory(mode):
        base=root/mode/"products"/"cas"
        return {str(path.relative_to(base)):hashlib.sha256(path.read_bytes()).hexdigest()
                for path in base.rglob("*") if path.is_file()}
    if inventory("legacy")!=inventory("factored"):
        raise AssertionError("matched campaign retained CAS bytes drift")
    if new["retained_products"]["logical_file_bytes"]>=old["retained_products"]["logical_file_bytes"]:
        raise AssertionError("factored campaign did not reduce retained product bytes")
    print("R10_MATCHED_CAMPAIGN",json.dumps({
        "order":order,"source_sha256":old["source_sha256"],"exact_output_and_release_parity":True,"exact_cas_file_parity":True,
        "legacy":old,"factored":new,
        "grade":"SAME_HOST_SAME_SOURCE_PAIRED_CAMPAIGNS__TIMING_ORDER_UNCONTROLLED__NOT_ORIGINAL"
    },sort_keys=True),flush=True)
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", default="128,192,256")
    parser.add_argument("--sample-seconds", type=float, default=.1)
    parser.add_argument("--root", type=Path)
    parser.add_argument("--replay-risk", choices=("legacy","factored"),default="factored")
    parser.add_argument("--compare-replay-risk",action="store_true")
    parser.add_argument("--factored-first",action="store_true")
    args = parser.parse_args()
    if not .02 <= args.sample_seconds <= 1:
        parser.error("sample interval must be within 0.02..1 seconds")
    def run(root):
        if args.compare_replay_risk:
            return compare_replay_risk(root,args.rows,args.sample_seconds,
                                       factored_first=args.factored_first)
        return supervise(root,args.rows,args.sample_seconds,risk_mode=args.replay_risk)
    if args.root is not None:
        return run(args.root)
    with tempfile.TemporaryDirectory(prefix="pyat-country-campaign-") as directory:
        return run(Path(directory))


if __name__ == "__main__":
    raise SystemExit(main())
