"""Bounded genuine DTA full-cell baseline versus selected projection."""
from __future__ import annotations
import argparse, hashlib, json, os, pickle, resource, signal, subprocess, sys, time
from pathlib import Path
HERE=Path(__file__).resolve(); REPO_ROOT=HERE.parents[4]
if str(REPO_ROOT) not in sys.path: sys.path.insert(0,str(REPO_ROOT))
from rawlsing_next.pre553_original35_physical_stream import bounded_physical_cell_stream
from rawlsing_next.pre553_physical_decoder import decode_dta
from rawlsing_next.source_configuration.library import SourceConfigLibrary
from rawlsing_next.source_configuration.reader import reader_configuration_from_config


def rss():
    try: return int(subprocess.check_output(["ps","-o","rss=","-p",str(os.getpid())],text=True).strip())*1024
    except Exception: return None


def selection(doc):
    for slot in doc.get("response_slots",()):
        if any(v.get("response_state")=="SUBSTANTIVE_RESPONSE" and v.get("canonical_value") is not None for v in slot.get("values",())):
            response=slot["slot"]["name"]; break
    else: raise RuntimeError("NO_SUBSTANTIVE_RESPONSE_SLOT")
    if not doc.get("coordinate_slots"): raise RuntimeError("NO_COORDINATE_SLOT")
    coordinate=doc["coordinate_slots"][0]["slot"]["name"]
    return response,coordinate


def scan(cells, selected_set):
    h=hashlib.sha256(); selected=0; all_cells=0; first=last=None; rows=set()
    for cell in cells:
        all_cells+=1
        if cell.variable_name not in selected_set: continue
        h.update(pickle.dumps(cell, protocol=5)); selected+=1; rows.add(cell.row_ordinal)
        ident=[cell.row_ordinal,cell.variable_ordinal,cell.variable_name]
        if first is None: first=ident
        last=ident
    return {"digest":h.hexdigest(),"selected_cells":selected,"all_cells_created":all_cells,
            "selected_rows":len(rows),"first":first,"last":last,"row_min":min(rows) if rows else None,
            "row_max":max(rows) if rows else None}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--source-id",required=True); ap.add_argument("--mode",choices=("baseline","projected"),required=True)
    ap.add_argument("--batch-size",type=int,default=10000); ap.add_argument("--max-seconds",type=int,default=900)
    ap.add_argument("--binding",default=str(REPO_ROOT/".local-logs/pyat-universal35/source-runtime-binding.local.json")); ap.add_argument("--outdir",default=str(REPO_ROOT/".local-logs/pyat-universal35/physical-stream/results")); ap.add_argument("--tmpdir",default=str(REPO_ROOT/".local-logs/pyat-universal35/physical-stream/tmp"))
    args=ap.parse_args(); Path(args.tmpdir).mkdir(parents=True,exist_ok=True); os.environ["TMPDIR"]=args.tmpdir
    binding=json.loads(Path(args.binding).read_text()); root=binding["USER_ORIGINAL35_DATA_ROOT"]
    lib=SourceConfigLibrary(source_root=root); cfg=lib.load_original(args.source_id); doc=cfg.document; rc=reader_configuration_from_config(cfg); res=lib.resolve_source_path(args.source_id)
    if res["status"]!="RESOLVED_UNDER_EFFECTIVE_ROOT": raise RuntimeError(res["status"])
    path=res["resolved_source_path"]; source_bytes=Path(path).stat().st_size
    response,coordinate=selection(doc); selected=(response,coordinate); selected_set=set(selected)
    out=Path(args.outdir); out.mkdir(parents=True,exist_ok=True); target=out/f"{args.source_id}_{args.mode}.json"
    payload={"schema":"PYAT_UNIVERSAL35_DTA_SOURCE_COMPARE@1","source_id":args.source_id,"mode":args.mode,
             "scope":"LOCAL_READ_ONLY_PHYSICAL_ENGINEERING_NOT_NATIVE_OR_SCIENTIFIC_ISSUANCE","source_format":"DTA",
             "source_bytes":source_bytes,"source_sha256":cfg.original_source_sha256,"row_count":cfg.active_row_count,
             "physical_slots":len(doc.get("physical_slots",())),"response_slots":len(doc.get("response_slots",())),
             "coordinate_slots":len(doc.get("coordinate_slots",())),"selected_columns":list(selected),
             "batch_size":args.batch_size,"status":"STARTED","started_epoch":time.time()}
    target.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    def alarm(_signum,_frame): raise TimeoutError("MEASUREMENT_TIME_LIMIT")
    old=signal.signal(signal.SIGALRM,alarm); signal.alarm(args.max_seconds)
    try:
        start_wall=time.perf_counter(); start_cpu=time.process_time(); start_rss=rss()
        incidence=decode_dta(path,encoding=rc.encoding,expected_source_sha256=cfg.original_source_sha256)
        decode_end=time.perf_counter(); decode_rss=rss(); decode_maxrss=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        if args.mode=="baseline":
            cells=incidence.iter_cells(args.batch_size)
        else:
            cells=bounded_physical_cell_stream(incidence,batch_size=args.batch_size,include_variables=selected).iter_cells()
        result=scan(cells,selected_set)
        end_wall=time.perf_counter(); end_cpu=time.process_time(); end_rss=rss(); end_maxrss=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        incidence.close()
        payload.update({"status":"OK","decode_wall_s":decode_end-start_wall,"decode_cpu_s":None,"decode_rss":decode_rss,"decode_maxrss":decode_maxrss,
                        "scan_wall_s":end_wall-decode_end,"scan_cpu_s":end_cpu-start_cpu,"scan_rss_before":decode_rss,"scan_rss_after":end_rss,"scan_maxrss":end_maxrss,
                        "selected_count_expected":cfg.active_row_count*len(selected),"physical_metadata_digest":incidence.physical_metadata_digest,
                        **result})
    except BaseException as exc:
        payload.update({"status":"TIME_LIMIT" if isinstance(exc,TimeoutError) else "FAILED","error":type(exc).__name__+":"+str(exc)[:300],"elapsed_s":time.time()-payload["started_epoch"],"maxrss":int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)})
    finally:
        signal.alarm(0); signal.signal(signal.SIGALRM,old)
    payload["finished_epoch"]=time.time(); target.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"path":str(target),"source_id":args.source_id,"mode":args.mode,"status":payload["status"],
                      "scan_wall_s":payload.get("scan_wall_s"),"selected_cells":payload.get("selected_cells"),
                      "all_cells_created":payload.get("all_cells_created"),"selected_rows":payload.get("selected_rows"),
                      "digest":payload.get("digest"),"maxrss":payload.get("scan_maxrss") or payload.get("maxrss")},sort_keys=True))

if __name__=="__main__": main()
