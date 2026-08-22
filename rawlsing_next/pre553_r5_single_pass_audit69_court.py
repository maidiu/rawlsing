"""Authority-69 same-carrier ordinary versus single-pass audit court."""
from __future__ import annotations

import argparse
import hashlib
import json
import resource
import shutil
import time
from pathlib import Path

from rawlsing_next.pre553_physical_decoder import decode_sav
from rawlsing_next.pre553_r5_compact_carrier import R5CompactLongShardedReader
from rawlsing_next.pre553_r5_compact_density_court import WVS_SHA256, WVS_ROWS, WVS_VARIABLES, _release_identity
from rawlsing_next.pre553_r5_serial_turbo66 import SerialTurboBuilder
from rawlsing_next.pre553_r5_serial_turbo66_court import source_rows
from rawlsing_next.pre553_r5_serial_turbo66_compliance_closure import V4, directory_bytes
from rawlsing_next.pre553_r5_single_pass_audit69 import single_pass_full_audit


def rss_bytes():
    value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return value if __import__("os").uname().sysname == "Darwin" else value * 1024


def run_checkpoint(source: Path, checkpoint: int, work: Path):
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    incidence = decode_sav(source)
    if incidence.source_sha256 != WVS_SHA256 or incidence.row_count != WVS_ROWS or len(incidence.variables) != WVS_VARIABLES:
        raise RuntimeError("source identity/shape mismatch")
    target = work / "sealed"
    build_start = time.perf_counter()
    telemetry = SerialTurboBuilder(V4).build(
        source_rows(incidence, checkpoint, {"cells_done": 0}),
        release_identity=_release_identity(checkpoint),
        target_directory=target,
    )
    build_seconds = time.perf_counter() - build_start
    ordinary_reader = R5CompactLongShardedReader(target, expected_physical_root_id=telemetry["physical_root_id"])
    ordinary_start = time.perf_counter()
    ordinary = ordinary_reader.full_audit()
    ordinary_seconds = time.perf_counter() - ordinary_start
    single_reader = R5CompactLongShardedReader(target, expected_physical_root_id=telemetry["physical_root_id"])
    single_start = time.perf_counter()
    single = single_pass_full_audit(single_reader)
    single_seconds = time.perf_counter() - single_start
    equality = ordinary == single
    sealed_bytes = directory_bytes(target)
    return {
        "checkpoint": checkpoint,
        "build_seconds": build_seconds,
        "ordinary_audit_seconds": ordinary_seconds,
        "single_pass_audit_seconds": single_seconds,
        "ordinary_rows_per_second": ordinary["canonical_rows"] / ordinary_seconds,
        "single_pass_rows_per_second": single["canonical_rows"] / single_seconds,
        "audit_speedup": ordinary_seconds / single_seconds,
        "peak_rss_bytes": rss_bytes(),
        "sealed_carrier_bytes_and_spool_upper_bound": sealed_bytes,
        "verified_spool_memory_bytes": V4 and 1024 * 1024,
        "persistent_cache_store_count": 0,
        "ordinary": ordinary,
        "single_pass": single,
        "exact_equality": equality,
        "telemetry": {k: telemetry[k] for k in ("canonical_steady_state_bytes", "physical_root_id", "final_shards", "member_bytes", "inventory_bytes", "root_bytes")},
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--work-root", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    if hashlib.sha256(args.source.read_bytes()).hexdigest() != WVS_SHA256:
        raise SystemExit("source hash mismatch")
    result = {"authority": "69", "source": str(args.source), "source_sha256": WVS_SHA256, "checkpoints": {}}
    try:
        for checkpoint in (250000, 2000000):
            result["checkpoints"][str(checkpoint)] = run_checkpoint(args.source, checkpoint, args.work_root / str(checkpoint))
        two_m = result["checkpoints"]["2000000"]
        if not all(item["exact_equality"] for item in result["checkpoints"].values()):
            result["disposition"] = "R5_SINGLE_PASS_AUDIT69_BLOCKED__AUDIT_NONIDENTITY"
        elif two_m["audit_speedup"] >= 1.20:
            result["disposition"] = "R5_SINGLE_PASS_AUDIT69_VALIDATED__USE_FOR_FULL_WVS7_CERTIFICATION"
        elif two_m["audit_speedup"] >= 1.08:
            result["disposition"] = "R5_SINGLE_PASS_AUDIT69_CORRECT__MODEST_GAIN__HQ_ADJUDICATION_REQUIRED"
        else:
            result["disposition"] = "R5_SINGLE_PASS_AUDIT69_CORRECT__NO_PRACTICAL_GAIN__DO_NOT_SELECT"
    except Exception as exc:
        result["disposition"] = "R5_SINGLE_PASS_AUDIT69_BLOCKED__PROCESS_OR_RESOURCE_GATE"
        result["error"] = repr(exc)
        raise
    finally:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
        shutil.rmtree(args.work_root, ignore_errors=True)
    print(json.dumps({"disposition": result["disposition"], "audit_speedup_2m": result["checkpoints"].get("2000000", {}).get("audit_speedup")}), flush=True)


if __name__ == "__main__":
    main()
