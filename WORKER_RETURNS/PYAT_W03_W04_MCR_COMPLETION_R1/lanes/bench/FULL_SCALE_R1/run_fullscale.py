#!/usr/bin/env python3
"""Finite serial full-scale driver for the existing W03/W04 benchmark CLI.

No benchmark logic is replaced. One child process at a time. Raw receipts and
commands are written under the evidence directory; disposable fixture/cache
roots live under the native supervisor run directory only.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

CANDIDATE = Path("/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-verifier-repair-r1")
BASELINE = Path("/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/pyat-w03-w04-baseline-4f3413")
BASELINE_HEAD = "4f3413fc5c37b589be3412f826bf8f68ee617d4a"
CAP_BYTES = 6 * 1024 ** 3
MIN_FREE_BYTES = 512 * 1024 ** 2
EXPECTED_CANDIDATE_BLOBS = {
    "rawlsing_next/_pre553_c11_execution_view.py": "0f86148f504c06bc694dd980ae1da8913db929b6",
    "rawlsing_next/_pre553_w03_cold_compact.py": "06eefd8fe8c1839854a783c78045b170627806f2",
    "rawlsing_next/_pre553_w04_cache.py": "4bb7e933f0a5c3f34366ee9e9013b3714a3e4341",
    "rawlsing_next/pre553_source_backed_c11_facade.py": "c5f78e1f7385b188eda18ace063557c26a19fd40",
    "rawlsing_next/pre553_parquet_carrier.py": "2c09deeb9b85051cb9d4c36fc12b0a193095e085",
    "rawlsing_next/pre553_carrier_execution.py": "ee9b3af02bfca9238eb72ea45d94073d47769a07",
    "rawlsing_next/bench_w03_w04_physical.py": "6c72f7d67c16fe79b9260032f6ace4085c6f1f3d",
    "rawlsing_next/tests/test_bench_w03_w04_physical.py": "c765799a1ed54d3f74283b1f493d8a3e5256d9e7",
    "rawlsing_next/tests/test_pre553_w03_w04_completion.py": "7cd62ffc36091f6e36847f1498d1dc428ebda157",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def save(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def git_blob(root: Path, rel: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", f"HEAD:{rel}"], text=True, stderr=subprocess.STDOUT
    ).strip()


def git_head(root: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True, stderr=subprocess.STDOUT
    ).strip()


def disk_record(label: str) -> dict:
    usage = shutil.disk_usage("/Users/matthewsmith/Desktop")
    return {
        "label": label,
        "free_bytes": usage.free,
        "total_bytes": usage.total,
        "used_bytes": usage.used,
        "minimum_free_bytes": MIN_FREE_BYTES,
        "pass": usage.free >= MIN_FREE_BYTES,
        "observed_utc": now(),
    }


def run_child(name: str, argv: list[str], cwd: Path, env: dict, raw: Path, first_marker: Path | None = None) -> dict:
    launch_path = raw / f"{name}.launch.json"
    complete_path = raw / f"{name}.completion.json"
    stdout_path = raw / f"{name}.stdout.log"
    stderr_path = raw / f"{name}.stderr.log"
    launch = {
        "name": name,
        "argv": argv,
        "cwd": str(cwd),
        "pid": None,
        "started_utc": now(),
        "launch_is_not_completion": True,
    }
    with stdout_path.open("wb") as out, stderr_path.open("wb") as err:
        proc = subprocess.Popen(argv, cwd=str(cwd), env=env, stdout=out, stderr=err)
        launch["pid"] = proc.pid
        save(launch_path, launch)
        if first_marker is not None:
            save(first_marker, launch)
        code = proc.wait()
    completion = {
        "name": name,
        "pid": launch["pid"],
        "exit_code": code,
        "started_utc": launch["started_utc"],
        "finished_utc": now(),
        "stdout_path": str(stdout_path),
        "stderr_path": str(stderr_path),
        "launch_path": str(launch_path),
    }
    save(complete_path, completion)
    return completion


def main() -> int:
    if len(sys.argv) != 5:
        raise SystemExit("usage: run_fullscale.py RUN_DIR CANDIDATE BASELINE EVIDENCE_ROOT")
    run_dir = Path(sys.argv[1]).resolve()
    candidate = Path(sys.argv[2]).resolve()
    baseline = Path(sys.argv[3]).resolve()
    evidence = Path(sys.argv[4]).resolve()
    raw = evidence / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    cache = run_dir / "cache"
    cache.mkdir(parents=True, exist_ok=True)
    first_marker = evidence / "first_child_launch.json"
    preflight = {
        "schema": "PYAT_W03_W04_FULLSCALE_PREFLIGHT_R1",
        "started_utc": now(),
        "candidate_root": str(candidate),
        "candidate_head": git_head(candidate),
        "baseline_root": str(baseline),
        "baseline_head": git_head(baseline),
        "baseline_expected_head": BASELINE_HEAD,
        "candidate_blobs": {p: git_blob(candidate, p) for p in EXPECTED_CANDIDATE_BLOBS},
        "candidate_blob_expectations": EXPECTED_CANDIDATE_BLOBS,
        "candidate_blobs_match": all(git_blob(candidate, p) == v for p, v in EXPECTED_CANDIDATE_BLOBS.items()),
        "baseline_source_diff_empty": subprocess.run(
            ["git", "-C", str(baseline), "diff", "--quiet", "--", "rawlsing_next"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        ).returncode == 0,
        "host": {
            "node": platform.node(),
            "platform": platform.platform(),
            "python": sys.version,
            "memory_bytes": int(subprocess.check_output(["sysctl", "-n", "hw.memsize"], text=True).strip()),
        },
        "cap_bytes": CAP_BYTES,
        "disk_before": disk_record("before"),
    }
    save(evidence / "preflight.json", preflight)
    if preflight["candidate_blobs_match"] is not True:
        save(evidence / "run_summary.json", {"status": "BLOCKED_EXACT_DEPENDENCY", "reason": "CANDIDATE_BLOB_MISMATCH", "preflight": preflight})
        return 2
    if preflight["baseline_head"] != BASELINE_HEAD or preflight["baseline_source_diff_empty"] is not True:
        save(evidence / "run_summary.json", {"status": "BLOCKED_EXACT_DEPENDENCY", "reason": "BASELINE_IDENTITY_OR_DIFF_MISMATCH", "preflight": preflight})
        return 2
    if preflight["disk_before"]["pass"] is not True:
        save(evidence / "run_summary.json", {"status": "BLOCKED_EXACT_DEPENDENCY", "reason": "DISK_BELOW_SAFETY_FLOOR", "disk": preflight["disk_before"]})
        return 2

    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = str(candidate) + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")

    def benchmark_cmd(scenario: str, profiles: str, source_root: Path, root: Path, jsonpath: Path, baseline_json: Path | None = None, gate: bool = False) -> list[str]:
        cmd = [
            sys.executable, "-B", "-m", "rawlsing_next.bench_w03_w04_physical",
            "--scenario", scenario,
            "--profiles", profiles,
            "--rows", "100000",
            "--repetitions", "3",
            "--source-root", str(source_root),
            "--root", str(root),
            "--jsonpath", str(jsonpath),
            "--cap-bytes", str(CAP_BYTES),
        ]
        if baseline_json is not None:
            cmd += ["--baseline-json", str(baseline_json)]
        if gate:
            cmd.append("--acceptance-gate")
        return cmd

    baseline_combined = evidence / "raw" / "baseline_combined_cold_fullmatrix.json"
    candidate_combined = evidence / "raw" / "candidate_combined_cold_fullmatrix.json"
    baseline_cells = evidence / "raw" / "baseline_cells_and_hash.json"
    candidate_cells = evidence / "raw" / "candidate_cells_and_hash.json"
    base_combined_root = cache / "baseline-combined"
    cand_combined_root = cache / "candidate-combined"
    base_cells_root = cache / "baseline-cells"
    cand_cells_root = cache / "candidate-cells"
    stages = []
    first = True

    def stage(name, cmd, root, jsonpath, first_marker=None):
        nonlocal first
        disk = disk_record(f"before_{name}")
        save(evidence / "raw" / f"{name}.disk_before.json", disk)
        if not disk["pass"]:
            stages.append({"stage": name, "status": "BLOCKED_EXACT_DEPENDENCY", "reason": "DISK_BELOW_SAFETY_FLOOR", "disk": disk})
            return None
        completion = run_child(name, cmd, candidate, env, raw, first_marker if first else None)
        first = False
        exists = jsonpath.is_file()
        record = {
            "stage": name,
            "command": cmd,
            "root": str(root),
            "jsonpath": str(jsonpath),
            "json_present": exists,
            "json_sha256": sha256(jsonpath) if exists else None,
            "completion": completion,
            "disk_after": disk_record(f"after_{name}"),
        }
        stages.append(record)
        return record

    stage("baseline_combined_cold_fullmatrix",
          benchmark_cmd("cold,full-matrix", "narrow,wide,repeat", baseline, base_combined_root, baseline_combined),
          base_combined_root, baseline_combined, first_marker)
    baseline_ready = baseline_combined.is_file()
    if baseline_ready:
        baseline_receipt = {
            "baseline_json": str(baseline_combined),
            "baseline_json_sha256": sha256(baseline_combined),
            "saved_before_candidate_comparison": True,
            "source_head": json.loads(baseline_combined.read_text()).get("source_head"),
            "method_sha256": json.loads(baseline_combined.read_text()).get("method_sha256"),
            "command": json.loads(baseline_combined.read_text()).get("command"),
            "host": json.loads(baseline_combined.read_text()).get("host"),
            "saved_utc": now(),
        }
        save(evidence / "baseline_external_receipt.json", baseline_receipt)
        # Baseline cache is disposable after the exact raw receipt is saved.
        if base_combined_root.exists():
            save(evidence / "raw" / "baseline_combined.cache_usage.json", {"path": str(base_combined_root), "bytes": sum(p.stat().st_size for p in base_combined_root.rglob('*') if p.is_file())})
            shutil.rmtree(base_combined_root)
        stage("candidate_combined_cold_fullmatrix",
              benchmark_cmd("cold,full-matrix", "narrow,wide,repeat", candidate, cand_combined_root, candidate_combined, baseline_combined, gate=True),
              cand_combined_root, candidate_combined)
        if candidate_combined.is_file():
            raw_obj = json.loads(candidate_combined.read_text())
            raw_sha = sha256(candidate_combined)
            proof02 = {
                "schema": "PYAT_W03_W04_PROOF_02_DERIVED_VIEW_R1",
                "status": "DERIVED_FROM_ACTUAL_COMBINED_RAW_NOT_A_NEW_RUN",
                "execution_cut": raw_obj.get("source_head"),
                "candidate_source_root": raw_obj.get("source_root"),
                "method_sha256": raw_obj.get("method_sha256"),
                "command": raw_obj.get("command"),
                "baseline_external_receipt": "WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/lanes/bench/FULL_SCALE_R1/baseline_external_receipt.json",
                "raw_combined_path": "WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/lanes/bench/FULL_SCALE_R1/raw/candidate_combined_cold_fullmatrix.json",
                "raw_combined_sha256": raw_sha,
                "cold": raw_obj.get("results", {}).get("cold"),
                "acceptance": raw_obj.get("acceptance"),
                "limits": raw_obj.get("limits"),
            }
            save(Path("/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-verifier-repair-r1/WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/proof_02_cold_rss.json"), proof02)
            proof10 = {
                "schema": "PYAT_W03_W04_PROOF_10_DERIVED_VIEW_R1",
                "status": "DERIVED_FROM_ACTUAL_COMBINED_RAW_NOT_A_NEW_RUN",
                "execution_cut": raw_obj.get("source_head"),
                "candidate_source_root": raw_obj.get("source_root"),
                "method_sha256": raw_obj.get("method_sha256"),
                "command": raw_obj.get("command"),
                "baseline_external_receipt": "WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/lanes/bench/FULL_SCALE_R1/baseline_external_receipt.json",
                "raw_combined_path": "WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/lanes/bench/FULL_SCALE_R1/raw/candidate_combined_cold_fullmatrix.json",
                "raw_combined_sha256": raw_sha,
                "full_matrix": raw_obj.get("results", {}).get("full-matrix"),
                "acceptance": raw_obj.get("acceptance"),
                "limits": raw_obj.get("limits"),
            }
            save(Path("/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-verifier-repair-r1/WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/proof_10_resource_matrix.json"), proof10)
            if cand_combined_root.exists():
                save(evidence / "raw" / "candidate_combined.cache_usage.json", {"path": str(cand_combined_root), "bytes": sum(p.stat().st_size for p in cand_combined_root.rglob('*') if p.is_file())})
                shutil.rmtree(cand_combined_root)
    else:
        stages.append({"stage": "candidate_combined_cold_fullmatrix", "status": "SKIPPED_BASELINE_NOT_AVAILABLE"})

    stage("baseline_cells_and_hash",
          benchmark_cmd("cells-and-hash", "narrow,wide", baseline, base_cells_root, baseline_cells),
          base_cells_root, baseline_cells)
    if baseline_cells.is_file():
        save(evidence / "raw" / "baseline_cells_external_receipt.json", {
            "baseline_json": str(baseline_cells),
            "baseline_json_sha256": sha256(baseline_cells),
            "saved_before_candidate_comparison": True,
            "saved_utc": now(),
        })
        if base_cells_root.exists():
            save(evidence / "raw" / "baseline_cells.cache_usage.json", {"path": str(base_cells_root), "bytes": sum(p.stat().st_size for p in base_cells_root.rglob('*') if p.is_file())})
            shutil.rmtree(base_cells_root)
        stage("candidate_cells_and_hash",
              benchmark_cmd("cells-and-hash", "narrow,wide", candidate, cand_cells_root, candidate_cells, baseline_cells),
              cand_cells_root, candidate_cells)
        if candidate_cells.is_file():
            shutil.copyfile(candidate_cells, Path("/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-verifier-repair-r1/WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/proof_03_cost_comparison.json"))
        if cand_cells_root.exists():
            save(evidence / "raw" / "candidate_cells.cache_usage.json", {"path": str(cand_cells_root), "bytes": sum(p.stat().st_size for p in cand_cells_root.rglob('*') if p.is_file())})
            shutil.rmtree(cand_cells_root)
    else:
        stages.append({"stage": "candidate_cells_and_hash", "status": "SKIPPED_BASELINE_NOT_AVAILABLE"})

    summary = {
        "schema": "PYAT_W03_W04_FULLSCALE_RUN_SUMMARY_R1",
        "status": "MEASUREMENTS_COMPLETE_RAW_CUSTODY" if candidate_combined.is_file() and candidate_cells.is_file() else "INCOMPLETE_OR_BLOCKED",
        "started_utc": preflight["started_utc"],
        "finished_utc": now(),
        "execution_cut": preflight["candidate_head"],
        "source_blobs": preflight["candidate_blobs"],
        "baseline_head": preflight["baseline_head"],
        "cap_bytes": CAP_BYTES,
        "stages": stages,
        "raw_paths": {
            "baseline_combined": str(baseline_combined),
            "candidate_combined": str(candidate_combined),
            "baseline_cells": str(baseline_cells),
            "candidate_cells": str(candidate_cells),
        },
        "proof_paths": {
            "proof_02": "WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/proof_02_cold_rss.json",
            "proof_03": "WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/proof_03_cost_comparison.json",
            "proof_10": "WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/proof_10_resource_matrix.json",
        },
        "measurements_complete": candidate_combined.is_file() and candidate_cells.is_file(),
        "acceptance_claimed": False,
        "receiving_required": True,
    }
    save(evidence / "run_summary.json", summary)
    return 0 if summary["measurements_complete"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
