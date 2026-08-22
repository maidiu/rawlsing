"""Authority-68 gate-enforcing court for the frozen fast Authority-67 path."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from rawlsing_next.pre553_r5_compact_density_court import WVS_SHA256
from rawlsing_next.pre553_r5_serial_turbo66_compliance_closure import V4
from rawlsing_next.pre553_r5_v4_trailing_audit67_court import equality, ordinary, overlap


DISPOSITION_VALIDATED = "R5_TRAILING_AUDIT67_FAST_RECERTIFIED__USE_FOR_FULL_WVS7_CERTIFICATION"
DISPOSITION_MODEST = "R5_TRAILING_AUDIT67_FAST_RECERTIFIED__MODEST_GAIN__HQ_ADJUDICATION_REQUIRED"
DISPOSITION_NO_GAIN = "R5_TRAILING_AUDIT67_FAST_RECERTIFIED__NO_PRACTICAL_GAIN__DO_NOT_SELECT"
DISPOSITION_BLOCKED_TESTS = "R5_TRAILING_AUDIT67_FAST_RECERT_BLOCKED__IMPLEMENTATION_WITNESS_RETURNED"
DISPOSITION_BLOCKED_PROCESS = "R5_TRAILING_AUDIT67_FAST_RECERT_BLOCKED__PROCESS_RESOURCE_OR_INTEGRITY"


def _hostile_suite():
    path = Path(__file__).with_name("test_pre553_r5_v4_trailing_audit67_recert68.py")
    proc = subprocess.run([sys.executable, "-m", "pytest", "-q", str(path)], text=True, capture_output=True)
    output = proc.stdout + proc.stderr
    match = re.search(r"(\d+) passed(?:, (\d+) skipped)?", output)
    passed = int(match.group(1)) if match else 0
    skipped = int(match.group(2) or 0) if match and match.group(2) else 0
    return {"exit_code": proc.returncode, "passed": passed, "skipped": skipped, "output": output[-4000:]}


def _compact(checkpoint, ordinary_result, overlap_result, eq):
    om = overlap_result["metrics"]
    return {
        "checkpoint": checkpoint,
        "ordinary": {k: ordinary_result[k] for k in ("build_seconds", "reopen_seconds", "audit_seconds", "total_seconds", "peak_rss_bytes", "peak_scratch_bytes")},
        "overlap": {k: om.get(k) for k in ("builder_seconds", "overlap_total_seconds", "auditor_seconds", "auditor_finish_lag_after_root_seal_seconds", "builder_blocked_seconds", "queue_peak", "aggregate_peak_rss_bytes", "builder_rss_bytes", "auditor_rss_bytes")},
        "equality": eq,
        "canonical_row_count": ordinary_result["audit"]["canonical_rows"],
        "logical_stream_digest": ordinary_result["audit"]["logical_stream_digest"],
        "physical_root_id": ordinary_result["audit"]["physical_root_id"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--work-root", type=Path, required=True)
    ap.add_argument("--receipt", type=Path, required=True)
    args = ap.parse_args()
    source_sha = hashlib.sha256(args.source.read_bytes()).hexdigest()
    if source_sha != WVS_SHA256:
        raise SystemExit("source hash mismatch")

    hostile = _hostile_suite()
    result = {"authority": "68", "source": str(args.source), "source_sha256": source_sha, "queue_capacity": 8, "builder_count": 1, "trailing_auditor_count": 1, "persistent_cache_count": 0, "hostile_process_suite": {k: v for k, v in hostile.items() if k != "output"}, "checkpoints": {}}
    if hostile["exit_code"] != 0 or hostile["skipped"] != 0:
        result["disposition"] = DISPOSITION_BLOCKED_TESTS
        result["hostile_process_suite"]["output_tail"] = hostile["output"]
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
        print(json.dumps({"disposition": result["disposition"], "tests": hostile}), flush=True)
        return 2

    for checkpoint in (250000, 2000000):
        ordinary_result = ordinary(args.source, checkpoint, args.work_root / f"{checkpoint}-ordinary")
        overlap_result = overlap(args.source, checkpoint, args.work_root / f"{checkpoint}-overlap")
        eq = equality(ordinary_result, overlap_result)
        om = overlap_result["metrics"]
        parity = all(eq.values())
        queue_ok = om.get("queue_peak", 99) <= 8
        if not parity or not queue_ok or overlap_result["peak_scratch_bytes"] < 0:
            result["disposition"] = DISPOSITION_BLOCKED_PROCESS
            result["checkpoints"][str(checkpoint)] = _compact(checkpoint, ordinary_result, overlap_result, eq)
            args.receipt.parent.mkdir(parents=True, exist_ok=True)
            args.receipt.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
            shutil.rmtree(args.work_root, ignore_errors=True)
            print(json.dumps({"disposition": result["disposition"], "checkpoint": checkpoint}), flush=True)
            return 3
        result["checkpoints"][str(checkpoint)] = _compact(checkpoint, ordinary_result, overlap_result, eq)

    two_m = result["checkpoints"]["2000000"]
    ordinary_total = two_m["ordinary"]["total_seconds"]
    overlap_total = two_m["overlap"]["overlap_total_seconds"]
    speedup = ordinary_total / overlap_total
    slowdown = two_m["overlap"]["builder_seconds"] / two_m["ordinary"]["build_seconds"] - 1
    result["overlap_speedup_2m"] = speedup
    result["builder_slowdown_2m"] = slowdown
    result["preferred_speedup_gate"] = speedup >= 1.25
    result["preferred_builder_slowdown_gate"] = slowdown <= 0.10
    if result["preferred_speedup_gate"] and result["preferred_builder_slowdown_gate"]:
        result["disposition"] = DISPOSITION_VALIDATED
    elif speedup >= 1.15:
        result["disposition"] = DISPOSITION_MODEST
    else:
        result["disposition"] = DISPOSITION_NO_GAIN
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    shutil.rmtree(args.work_root, ignore_errors=True)
    print(json.dumps({"disposition": result["disposition"], "speedup_2m": speedup, "builder_slowdown_2m": slowdown}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
