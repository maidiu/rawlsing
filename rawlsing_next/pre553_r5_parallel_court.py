"""Serial-vs-parallel-12 Compact V2 equivalence court."""
from __future__ import annotations
import argparse, hashlib, json, shutil, time
from pathlib import Path
from rawlsing_next.pre553_r5_compact_density_court import run as serial_run
from rawlsing_next.pre553_r5_compact_carrier import R5LongShardedReader
from rawlsing_next.pre553_r5_parallel_compiler import build_parallel, cleanup

def _inventory(root: Path) -> list[dict]:
    return [json.loads(line) for line in (root / "member_inventory.jsonl").read_text().splitlines()]

def _equivalence(serial_root: Path, parallel_root: Path) -> dict:
    sr = R5LongShardedReader(serial_root); pr = R5LongShardedReader(parallel_root)
    root_equal = (serial_root / "root.json").read_bytes() == (parallel_root / "root.json").read_bytes()
    serial_inventory = _inventory(serial_root); parallel_inventory = _inventory(parallel_root)
    member_equal = []
    for left, right in zip(serial_inventory, parallel_inventory):
        lp = serial_root / "members" / left["member"]; rp = parallel_root / "members" / right["member"]
        member_equal.append({"name": left["member"], "bytes_equal": lp.read_bytes() == rp.read_bytes(),
                             "sha_equal": left["sha256"] == right["sha256"], "logical_digest_equal": left["logical_digest"] == right["logical_digest"],
                             "coverage_equal": left["first_identity"] == right["first_identity"] and left["last_identity"] == right["last_identity"]})
    sa, pa = sr.full_audit(), pr.full_audit()
    return {"root_bytes_equal": root_equal, "inventory_bytes_equal": (serial_root / "member_inventory.jsonl").read_bytes() == (parallel_root / "member_inventory.jsonl").read_bytes(),
            "member_count_equal": len(serial_inventory) == len(parallel_inventory), "member_order_equal": [x["member"] for x in serial_inventory] == [x["member"] for x in parallel_inventory],
            "members": member_equal, "all_members_equal": all(all(x.values()) for x in member_equal),
            "logical_stream_digest_equal": sr.root["logical_stream_digest"] == pr.root["logical_stream_digest"],
            "physical_root_id_equal": sr.root["physical_root_id"] == pr.root["physical_root_id"], "audit_equal": sa == pa,
            "serial_audit": sa, "parallel_audit": pa}

def run(source: Path, checkpoint: int, work_root: Path, receipt: Path) -> dict:
    serial_root = work_root / "serial" / f"sealed-{checkpoint}"
    started = time.perf_counter(); serial = serial_run(source, checkpoint, work_root / "serial", keep=True); serial_wall = serial["build_seconds"]
    parallel = build_parallel(source, checkpoint, work_root / "parallel-staging"); parallel_root = Path(parallel["target"]); parallel_wall = parallel["parallel_build_seconds"]
    eq = _equivalence(serial_root, parallel_root)
    if not all(eq[k] for k in ("root_bytes_equal","inventory_bytes_equal","member_count_equal","member_order_equal","all_members_equal","logical_stream_digest_equal","physical_root_id_equal","audit_equal")):
        disposition = "R5_PARALLEL12_BLOCKED__SERIAL_PARALLEL_NONIDENTITY"
    else:
        speedup = serial_wall / parallel_wall if parallel_wall else 0
        disposition = "R5_PARALLEL12_VALIDATED__USE_FOR_FULL_SOURCE_COURT" if speedup >= 2 else ("R5_PARALLEL12_CORRECT__MODEST_GAIN__HQ_ADJUDICATION_REQUIRED" if speedup >= 1.25 else "R5_PARALLEL12_CORRECT__NO_PRACTICAL_GAIN__DO_NOT_SELECT")
    result = {"checkpoint":checkpoint,"serial_build_seconds":serial_wall,"parallel_build_seconds":parallel_wall,"speedup":serial_wall/parallel_wall if parallel_wall else 0,"serial":serial,"parallel":parallel,"equivalence":eq,"disposition":disposition,"elapsed_seconds":time.perf_counter()-started}
    receipt.parent.mkdir(parents=True,exist_ok=True); receipt.write_text(json.dumps(result,sort_keys=True,separators=(",",":"))+"\n")
    cleanup(parallel); shutil.rmtree(work_root / "serial", ignore_errors=True)
    print(json.dumps(result,sort_keys=True),flush=True); return result

def main():
    p=argparse.ArgumentParser(); p.add_argument("--source",type=Path,required=True); p.add_argument("--checkpoint",type=int,required=True); p.add_argument("--work-root",type=Path,required=True); p.add_argument("--receipt",type=Path,required=True); a=p.parse_args(); run(a.source,a.checkpoint,a.work_root,a.receipt)
if __name__ == "__main__": main()
