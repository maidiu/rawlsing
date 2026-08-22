from __future__ import annotations
import argparse, hashlib, json, shutil, time
from pathlib import Path

from rawlsing_next.pre553_physical_decoder import decode_sav
from rawlsing_next.pre553_r5_compact_carrier import R5CompactLongShardedReader
from rawlsing_next.pre553_r5_compact_density_court import WVS_EVENTS, WVS_ROWS, WVS_SHA256, WVS_VARIABLES, _release_identity
from rawlsing_next.pre553_r5_serial_turbo66 import SerialTurboBuilder
from rawlsing_next.pre553_r5_serial_turbo66_court import source_rows, rss_bytes
from rawlsing_next.pre553_r5_serial_turbo66_compliance_closure import V4, directory_bytes
from rawlsing_next.pre553_r5_v4_trailing_audit67 import run_trailing


def ordinary(source, checkpoint, work):
    shutil.rmtree(work,ignore_errors=True); work.mkdir(parents=True); incidence=decode_sav(source); target=work/"sealed"; start=time.perf_counter()
    telemetry=SerialTurboBuilder(V4).build(source_rows(incidence,checkpoint,{"cells_done":0}),release_identity=_release_identity(checkpoint),target_directory=target); build_seconds=time.perf_counter()-start
    reopen_start=time.perf_counter(); reader=R5CompactLongShardedReader(target,expected_physical_root_id=telemetry["physical_root_id"]); reopen_seconds=time.perf_counter()-reopen_start
    audit_start=time.perf_counter(); audit=reader.full_audit(); audit_seconds=time.perf_counter()-audit_start
    return {"build_seconds":build_seconds,"reopen_seconds":reopen_seconds,"audit_seconds":audit_seconds,"total_seconds":build_seconds+reopen_seconds+audit_seconds,"telemetry":telemetry,"audit":audit,"target":target,"root":(target/"root.json").read_bytes(),"inventory":(target/"member_inventory.jsonl").read_bytes(),"members":{p.name:p.read_bytes() for p in sorted((target/"members").glob("*.r5z"))},"peak_rss_bytes":rss_bytes(),"peak_scratch_bytes":directory_bytes(work)}


def overlap(source, checkpoint, work):
    shutil.rmtree(work,ignore_errors=True); work.mkdir(parents=True); incidence=decode_sav(source); target=work/"sealed"; start=time.perf_counter()
    telemetry,trailing,overlap_metrics=run_trailing(SerialTurboBuilder(V4),source_rows(incidence,checkpoint,{"cells_done":0}),_release_identity(checkpoint),target)
    overlap_metrics["builder_seconds"]=time.perf_counter()-start
    reader=R5CompactLongShardedReader(target,expected_physical_root_id=telemetry["physical_root_id"]); ordinary_audit=reader.full_audit()
    return {"build_seconds":overlap_metrics["builder_seconds"],"trailing":trailing,"metrics":overlap_metrics,"telemetry":telemetry,"ordinary_audit_after":ordinary_audit,"target":target,"root":(target/"root.json").read_bytes(),"inventory":(target/"member_inventory.jsonl").read_bytes(),"members":{p.name:p.read_bytes() for p in sorted((target/"members").glob("*.r5z"))},"peak_rss_bytes":rss_bytes(),"peak_scratch_bytes":directory_bytes(work)}


def equality(a,b):
    return {"root_bytes":a["root"]==b["root"],"inventory_bytes":a["inventory"]==b["inventory"],"member_order_count":list(a["members"])==list(b["members"]),"member_bytes_hashes":a["members"]==b["members"],"ordinary_audit_equals_trailing":b["ordinary_audit_after"]==b["trailing"]["audit"],"ordinary_audit_equals_ordinary":a["audit"]==b["ordinary_audit_after"]}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--source",type=Path,required=True); ap.add_argument("--work-root",type=Path,required=True); ap.add_argument("--receipt",type=Path,required=True); args=ap.parse_args()
    if hashlib.sha256(args.source.read_bytes()).hexdigest()!=WVS_SHA256: raise SystemExit("source hash mismatch")
    results={"source_sha256":WVS_SHA256,"worker_count":1,"trailing_auditor_count":1,"persistent_cache_count":0,"courts":{}}
    for checkpoint in (250000,2000000):
        o=ordinary(args.source,checkpoint,args.work_root/f"{checkpoint}-ordinary"); t=overlap(args.source,checkpoint,args.work_root/f"{checkpoint}-overlap"); eq=equality(o,t)
        results["courts"][str(checkpoint)]={"ordinary":o,"overlap":t,"equality":eq,"all_equal":all(eq.values())}
    a=results["courts"]["2000000"]; results["overlap_speedup_2m"]=a["ordinary"]["total_seconds"]/a["overlap"]["metrics"]["overlap_total_seconds"]; results["disposition"]="R5_TRAILING_AUDIT67_VALIDATED__USE_FOR_FULL_WVS7_CERTIFICATION" if results["overlap_speedup_2m"]>=1.25 else ("R5_TRAILING_AUDIT67_CORRECT__MODEST_GAIN__HQ_ADJUDICATION_REQUIRED" if results["overlap_speedup_2m"]>=1.15 else "R5_TRAILING_AUDIT67_CORRECT__NO_PRACTICAL_GAIN__DO_NOT_SELECT")
    compact={"source_sha256":WVS_SHA256,"disposition":results["disposition"],"overlap_speedup_2m":results["overlap_speedup_2m"],"courts":{}}
    for ck in ("250000","2000000"):
        x=results["courts"][ck]; compact["courts"][ck]={"ordinary":{k:x["ordinary"][k] for k in ("build_seconds","reopen_seconds","audit_seconds","total_seconds","peak_rss_bytes","peak_scratch_bytes")},"overlap":{k:x["overlap"]["metrics"].get(k) for k in ("builder_seconds","overlap_total_seconds","auditor_seconds","auditor_finish_lag_after_root_seal_seconds","builder_blocked_seconds","queue_peak","aggregate_peak_rss_bytes")},"equality":x["equality"],"logical_digest":x["ordinary"]["audit"]["logical_stream_digest"],"physical_root_id":x["ordinary"]["audit"]["physical_root_id"]}
    args.receipt.parent.mkdir(parents=True,exist_ok=True); args.receipt.write_text(json.dumps(compact,sort_keys=True,indent=2)+"\n"); shutil.rmtree(args.work_root,ignore_errors=True); print(json.dumps({"disposition":results["disposition"],"overlap_speedup_2m":results["overlap_speedup_2m"]}),flush=True)

if __name__=="__main__": main()
