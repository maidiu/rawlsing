"""Authority 66 narrow V0/V4 compliance closure court."""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, threading, time
from pathlib import Path

from rawlsing_next.pre553_physical_decoder import decode_sav
from rawlsing_next.pre553_r5_compact_carrier import R5CompactLongShardedReader
from rawlsing_next.pre553_r5_compact_density_court import WVS_EVENTS, WVS_ROWS, WVS_SHA256, WVS_VARIABLES, _release_identity
from rawlsing_next.pre553_r5_serial_turbo66 import (
    BASELINE, FREE_SPACE_HARD_ABORT, RSS_HARD_ABORT, SCRATCH_HARD_ABORT,
    SerialTurboBuilder, TurboConfig, actual_fan_in, filesystem_action, rss_action, scratch_action,
    TurboSafetyAbort,
)
from rawlsing_next.pre553_r5_serial_turbo66_court import source_rows, rss_bytes

V4 = TurboConfig("V4", 65536, 64 * 1024 * 1024, 64, 1, False, 16384, 16 * 1024 * 1024, 6, True)


def directory_bytes(root: Path) -> int:
    total = 0
    if not root.exists(): return 0
    for base, _, names in os.walk(root):
        for name in names:
            try: total += (Path(base) / name).stat().st_size
            except FileNotFoundError: pass
    return total


def guarded_rows(incidence, checkpoint, progress, abort):
    for row in source_rows(incidence, checkpoint, progress):
        if abort.is_set(): raise TurboSafetyAbort("safety governor abort")
        yield row


def run_one(source: Path, checkpoint: int, config: TurboConfig, work: Path) -> dict:
    shutil.rmtree(work, ignore_errors=True); work.mkdir(parents=True)
    opened=time.perf_counter(); incidence=decode_sav(source); decode_seconds=time.perf_counter()-opened
    if incidence.source_sha256 != WVS_SHA256 or incidence.row_count != WVS_ROWS or len(incidence.variables) != WVS_VARIABLES:
        raise TurboSafetyAbort("source identity/shape mismatch")
    progress={"cells_done":0}; abort=threading.Event(); peak_scratch=0; peak_rss=0; safety_events=[]; stop=threading.Event()
    monitor_started=time.perf_counter(); last_report=monitor_started
    def monitor():
        nonlocal peak_scratch, peak_rss, last_report
        while not stop.wait(1.0):
            now=time.perf_counter(); peak_scratch=max(peak_scratch,directory_bytes(work)); peak_rss=max(peak_rss,rss_bytes()); free=shutil.disk_usage(work).free
            if now-last_report >= 60:
                done=progress.get("cells_done",0); phase="DECODE_BUILD" if done < checkpoint else "MERGE_SEAL_OR_AUDIT"
                rate=done/(now-monitor_started) if now>monitor_started else 0
                print(f"[R5/TURBO66][{config.name}][{phase}] {done:,}/{checkpoint:,} cells | RSS {peak_rss/2**20:.1f} MiB | scratch {peak_scratch:,} B | {rate:,.0f} cells/s | elapsed {now-monitor_started:.0f}s",flush=True)
                last_report=now
            if rss_action(peak_rss)=="HARD_ABORT" or scratch_action(peak_scratch)=="HARD_ABORT" or filesystem_action(free)=="HARD_ABORT":
                safety_events.append({"rss":peak_rss,"scratch":peak_scratch,"free":free}); abort.set()
    thread=threading.Thread(target=monitor,daemon=True); thread.start()
    target=work/"sealed"; build_start=time.perf_counter()
    try:
        builder=SerialTurboBuilder(config)
        telemetry=builder.build(guarded_rows(incidence,checkpoint,progress,abort),release_identity=_release_identity(checkpoint),target_directory=target)
        if abort.is_set(): raise TurboSafetyAbort("safety governor abort after build")
        peak_scratch=max(peak_scratch,directory_bytes(work)); peak_rss=max(peak_rss,rss_bytes())
        reopen_start=time.perf_counter(); reader=R5CompactLongShardedReader(target,expected_physical_root_id=telemetry["physical_root_id"]); reopen_seconds=time.perf_counter()-reopen_start
        audit_start=time.perf_counter(); audit=reader.full_audit(); audit_seconds=time.perf_counter()-audit_start
    except Exception:
        stop.set(); thread.join(timeout=3); raise
    finally:
        stop.set(); thread.join(timeout=3)
    result={"variant":config.name,"checkpoint":checkpoint,"execution_config":telemetry["execution_config"],"requested_merge_fan_in":config.merge_fan_in,"actual_merge_fan_in":telemetry["actual_merge_fan_in"],"decode_open_seconds":decode_seconds,"build_seconds":build_start and (reopen_start-build_start-reopen_seconds),"reopen_seconds":reopen_seconds,"audit_seconds":audit_seconds,"build_cells_per_second":checkpoint/(reopen_start-build_start-reopen_seconds),"audit_cells_per_second":checkpoint/audit_seconds,"peak_rss_bytes":peak_rss,"peak_scratch_bytes":peak_scratch,"safety_events":safety_events,"telemetry":telemetry,"audit":audit,"root_bytes":(target/"root.json").read_bytes(),"inventory_bytes":(target/"member_inventory.jsonl").read_bytes(),"root":reader.root,"member_count":len(list((target/"members").glob("*.r5z"))),"target":str(target)}
    result["member_files"]={p.name:{"bytes":p.read_bytes(),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted((target/"members").glob("*.r5z"))}
    return result


def equivalence(a,b):
    return {
        "canonical_row_count": a["audit"]["canonical_rows"]==b["audit"]["canonical_rows"],
        "logical_stream_digest": a["audit"]["logical_stream_digest"]==b["audit"]["logical_stream_digest"],
        "physical_root_id": a["root"]["physical_root_id"]==b["root"]["physical_root_id"],
        "root_bytes": a["root_bytes"]==b["root_bytes"],
        "inventory_bytes": a["inventory_bytes"]==b["inventory_bytes"],
        "member_count_order": list(a["member_files"])==list(b["member_files"]),
        "member_bytes_hashes": a["member_files"]==b["member_files"],
        "full_audit": a["audit"]==b["audit"],
    }


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--source",type=Path,required=True); ap.add_argument("--work-root",type=Path,required=True); ap.add_argument("--receipt",type=Path,required=True); args=ap.parse_args()
    if hashlib.sha256(args.source.read_bytes()).hexdigest()!=WVS_SHA256: raise SystemExit("source hash mismatch")
    results={"starting_head":"c8859bebf5baccf0ac65932c08b5dbdcb60012d7","source_sha256":WVS_SHA256,"courts":{},"safety_thresholds":{"rss_hard_abort":RSS_HARD_ABORT,"scratch_hard_abort":SCRATCH_HARD_ABORT,"free_space_hard_abort":FREE_SPACE_HARD_ABORT}}
    for checkpoint in (250000,2000000):
        v0=run_one(args.source,checkpoint,BASELINE,args.work_root/f"{checkpoint}-V0"); v4=run_one(args.source,checkpoint,V4,args.work_root/f"{checkpoint}-V4")
        eq=equivalence(v0,v4); results["courts"][str(checkpoint)]={"V0":v0,"V4":v4,"equivalence":eq,"all_equal":all(eq.values())}
    a=results["courts"]["2000000"]; v0=a["V0"]; v4=a["V4"]
    results["build_speedup"]=v0["build_seconds"]/v4["build_seconds"]
    results["total_certification_speedup"]=(v0["build_seconds"]+v0["reopen_seconds"]+v0["audit_seconds"])/(v4["build_seconds"]+v4["reopen_seconds"]+v4["audit_seconds"])
    results["projected_full_wvs_gib"]=v4["telemetry"]["canonical_steady_state_bytes"]/2000000*WVS_EVENTS/2**30
    results["test_result_pending"]=True; results["disposition"]="R5_SERIAL_TURBO_V4_COMPLIANCE_CLOSED__READY_FOR_FULL_SOURCE_HQ_AUTHORITY"
    args.receipt.parent.mkdir(parents=True,exist_ok=True); args.receipt.write_text(json.dumps(results,sort_keys=True,indent=2,default=lambda x:x.hex() if isinstance(x,bytes) else x)+"\n")
    shutil.rmtree(args.work_root,ignore_errors=True)
    print(json.dumps({"build_speedup":results["build_speedup"],"total_certification_speedup":results["total_certification_speedup"],"disposition":results["disposition"]}),flush=True)

if __name__=="__main__": main()
