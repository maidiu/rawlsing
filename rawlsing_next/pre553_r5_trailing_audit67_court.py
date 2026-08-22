"""Bounded Authority-67 OA court; V4 only, no full WVS/LiTS execution."""
from __future__ import annotations

import argparse, hashlib, json, shutil, time
from pathlib import Path

from rawlsing_next.pre553_r5_serial_turbo66_compliance_closure import run_one
from rawlsing_next.pre553_r5_trailing_audit67 import V4, run_overlap


def _files(root: Path):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file() and ".work" not in p.parts}


def run_checkpoint(source: Path, checkpoint: int, work: Path):
    ordinary = run_one(source, checkpoint, V4, work / "ordinary")
    overlap = run_overlap(source, checkpoint, work / "overlap")
    ordinary_root = Path(ordinary["target"]); overlap_root = Path(overlap["target"])
    bytes_equal = _files(ordinary_root) == _files(overlap_root)
    if not bytes_equal or ordinary["audit"] != overlap["audit"] or overlap["audit"] != overlap["ordinary_audit"]:
        raise RuntimeError("Authority-67 exact V4 output/audit equality failure")
    ordinary_total = ordinary["build_seconds"] + ordinary["reopen_seconds"] + ordinary["audit_seconds"]
    return {
        "checkpoint": checkpoint,
        "v4_execution_config": {"run_max_rows":65536,"run_max_bytes":67108864,"merge_fan_in":64,"temp_gzip_level":1,"temp_fsync":False,"shard_max_rows":16384,"shard_max_bytes":16777216,"final_gzip_level":6},
        "ordinary": {"build_seconds":ordinary["build_seconds"],"audit_seconds":ordinary["audit_seconds"],"total_certification_seconds":ordinary_total,"audit":ordinary["audit"]},
        "overlap": overlap,
        "output_bytes_root_inventory_member_hashes_equal": bytes_equal,
        "audit_result_equal": ordinary["audit"] == overlap["audit"],
        "overlap_speedup": ordinary_total / overlap["overlap_wall_seconds"],
        "build_slowdown_fraction": (overlap["telemetry"]["phases"]["initial_run_generation_sort_write"] + overlap["telemetry"]["phases"]["merge_reduction"] + overlap["telemetry"]["phases"]["final_merge_member_sealing"] + overlap["telemetry"]["phases"]["hash_inventory_root_closure"]) / ordinary["build_seconds"] - 1,
    }


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--source",type=Path,required=True); ap.add_argument("--work-root",type=Path,required=True); ap.add_argument("--receipt",type=Path,required=True); args=ap.parse_args()
    args.work_root.mkdir(parents=True,exist_ok=True)
    results={"authority":"67","source":str(args.source),"courts":{}}
    try:
        for checkpoint in (250000,2000000):
            results["courts"][str(checkpoint)] = run_checkpoint(args.source, checkpoint, args.work_root / str(checkpoint))
        two=results["courts"]["2000000"]
        speed=two["overlap_speedup"]
        if speed >= 1.25 and two["build_slowdown_fraction"] <= .10:
            status="R5_TRAILING_AUDIT67_VALIDATED__USE_FOR_FULL_WVS7_CERTIFICATION"
        elif speed >= 1.15:
            status="R5_TRAILING_AUDIT67_CORRECT__MODEST_GAIN__HQ_ADJUDICATION_REQUIRED"
        else:
            status="R5_TRAILING_AUDIT67_CORRECT__NO_PRACTICAL_GAIN__DO_NOT_SELECT"
        results["disposition"] = status
        args.receipt.parent.mkdir(parents=True,exist_ok=True)
        args.receipt.write_text(json.dumps(results,sort_keys=True,indent=2)+"\n")
        print(json.dumps({"disposition":status,"2m_speedup":speed}),flush=True)
    finally:
        shutil.rmtree(args.work_root,ignore_errors=True)


if __name__ == "__main__": main()
