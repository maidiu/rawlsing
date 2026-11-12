#!/usr/bin/env python3
"""Independent read-only first consumer for saved raw G03-I0 P6 receipts."""
import argparse,hashlib,json,math,statistics
from pathlib import Path
from measure import SCHEMA,PLAN,FILES,P6

class Reject(ValueError):pass
def require(ok,why):
    if not ok:raise Reject(why)
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(seq):
    d={}
    for k,v in seq:
        require(k not in d,"DUPLICATE_JSON_KEY");d[k]=v
    return d
def load(p):
    try:
        return json.loads(Path(p).read_text(),object_pairs_hook=pairs,
             parse_constant=lambda x: (_ for _ in ()).throw(Reject("NONFINITE_JSON")))
    except (OSError,UnicodeError,ValueError) as e:raise Reject("INVALID_JSON:"+str(e)) from e
def validhash(x,n=64):return isinstance(x,str) and len(x)==n and all(c in "0123456789abcdef" for c in x)
def num(x):return type(x) in (int,float) and math.isfinite(x) and x>=0
def resources(r,osname):
    require(isinstance(r,dict),"RESOURCE_MISSING")
    if r.get("status")=="UNOBSERVED":
        require(r.get("reason") in ("wait4_unavailable","unknown_ru_maxrss_unit"),"RESOURCE_FAKE")
    else:
        require(r.get("status")=="MEASURED" and r.get("scope")=="single_wait4_child_not_process_tree","RESOURCE_SCOPE_FALSE")
        require(num(r.get("cpu_user_s")) and num(r.get("cpu_system_s")),"CPU_INVALID")
        unit,mult={"Linux":("KiB",1024),"Darwin":("bytes",1)}.get(osname,(None,None))
        require(unit is not None and r.get("ru_maxrss_native_unit")==unit,"RSS_UNITS_FALSE")
        require(num(r.get("ru_maxrss_native")) and type(r.get("peak_rss_bytes")) is int
                and r["peak_rss_bytes"]==int(r["ru_maxrss_native"])*mult,"RSS_CONVERSION_FALSE")
def consume(root,expected_index_sha256=None):
    root=Path(root);man=load(root/"manifest.json");idxpath=root/"index.json";rawidx=idxpath.read_bytes()
    if expected_index_sha256 is not None:
        require(sha(rawidx)==expected_index_sha256,"INDEX_EXTERNAL_ANCHOR_MISMATCH")
    idx=load(idxpath)
    require(man.get("schema")==SCHEMA and idx.get("schema")==SCHEMA,"SCHEMA_BAD")
    head=man.get("repo_sha")
    require(validhash(head,40),"SOURCE_SHA_BAD")
    source=man.get("source_hashes")
    require(isinstance(source,dict) and set(source)==set(FILES)
            and all(validhash(v) for v in source.values()),"SOURCE_FILES_BAD")
    require(validhash(man.get("runner_sha256")) and validhash(man.get("python_executable_sha256")),"RUNNER_PROVENANCE_BAD")
    require(man.get("plan")==[{"id":n,"args":a,"cold":n=="cold_view"} for n,a in PLAN],"PLAN_DENOMINATOR_REDUCED")
    require(man.get("provider_mode")=="OFFLINE_VERIFIED_CHILD_ALLOWLIST"
            and man.get("env_keys")==["LANG","PATH","PYTHONDONTWRITEBYTECODE","PYTHONHASHSEED","PYTHONNOUSERSITE"]
            and validhash(man.get("env_fingerprint_sha256"))
            and man.get("network_calls")=="UNOBSERVED"
            and man.get("descendant_processes")=="UNOBSERVED","OFFLINE_OR_PROCESS_CLAIM_FALSE")
    expected={"attempts/"+n+"/"+f for n,_ in PLAN for f in ("start.json","receipt.json","stdout.bin","stderr.bin")}
    require(isinstance(idx.get("entries"),dict) and set(idx["entries"])==expected,"INDEX_ATTEMPTS_MISSING")
    rows=[]
    for name,args in PLAN:
        base=root/"attempts"/name
        for f in ("start.json","receipt.json","stdout.bin","stderr.bin"):
            path=base/f;key="attempts/"+name+"/"+f
            require(path.is_file() and not path.is_symlink(),"ATTEMPT_MISSING:"+key)
            require(sha(path.read_bytes())==idx["entries"][key],"RAW_EVIDENCE_EDITED:"+key)
        start=load(base/"start.json");r=load(base/"receipt.json")
        require(start.get("id")==name and r.get("id")==name and r.get("schema")==SCHEMA,"ID_SCHEMA_MISMATCH")
        require(start.get("source_sha")==head and r.get("source_sha")==head
                and r.get("source_hashes")==source,"MIXED_SOURCE_CUT")
        argv=r.get("argv")
        require(isinstance(argv,list) and len(argv)==4+len(args)
                and all(isinstance(v,str) for v in argv)
                and argv[1].endswith("/"+P6) and argv[2]=="--state"
                and argv[3].endswith("/state") and argv[4:]==args
                and argv==start.get("argv"),"COMMAND_OR_STATE_FORGED")
        require(type(r.get("child_pid")) is int and r["child_pid"]>0
                and type(r.get("exit_code")) is int
                and type(r.get("timeout")) is bool and num(r.get("wall_seconds")),"EXECUTION_METRICS_INVALID")
        require(type(r.get("state_bytes_before")) is int and r["state_bytes_before"]>=0
                and type(r.get("state_bytes_after")) is int and r["state_bytes_after"]>=0
                and start.get("state_bytes_before")==r["state_bytes_before"],"STATE_BYTES_FORGED")
        require(r.get("direct_children_started")==1 and r.get("descendants")=="UNOBSERVED","PROCESS_COUNT_FORGED")
        require(r.get("cold") is (name=="cold_view")
                and r.get("cold_basis")==("separate_python_exec_after_wait" if name=="cold_view" else "NOT_APPLICABLE"),"COLD_CLAIM_FORGED")
        resources(r.get("resources"),man.get("os"))
        require(r.get("provider_mode")=="OFFLINE_VERIFIED_CHILD_ALLOWLIST","PROVIDER_CONFIG_FORGED")
        provider=r.get("provider")
        require(isinstance(provider,dict) and set(provider)=={"calls","tokens","retries","billable_cost"},"PROVIDER_FIELDS_MISSING")
        for key,v in provider.items():
            require(isinstance(v,dict) and v.get("status")=="UNOBSERVED"
                    and isinstance(v.get("reason"),str) and bool(v["reason"]),"COUNTER_ZERO_FORGED:"+key)
        for stream in ("stdout","stderr"):
            b=(base/(stream+".bin")).read_bytes()
            require(r.get(stream+"_bytes")==len(b) and r.get(stream+"_sha256")==sha(b),"OUTPUT_MISMATCH")
        try:
            o=json.loads((base/"stdout.bin").read_text(),object_pairs_hook=pairs)
            if not isinstance(o,dict):o=None
        except (UnicodeError,ValueError):o=None
        view=r.get("output")
        require(isinstance(view,dict) and view.get("json") is (o is not None)
                and view.get("status")==(o.get("status") if o else None)
                and view.get("clock")==(o.get("clock") if o else None),"OUTPUT_CLAIM_FALSE")
        rows.append(r)
    require(rows[0]["state_bytes_before"]==0,"STATE_NOT_FRESH")
    require(all(a["state_bytes_after"]==b["state_bytes_before"] and a["argv"][3]==b["argv"][3]
                for a,b in zip(rows,rows[1:])),"STATE_CONTINUITY_BAD")
    expected=all(r["exit_code"]==0 and r["output"]["json"] and not r["timeout"] for r in rows[:4])
    expected=expected and rows[-1]["exit_code"]==2 and rows[-1]["output"]["status"]=="REFUSED"
    walls=[r["wall_seconds"] for r in rows]
    rss=[r["resources"]["peak_rss_bytes"] for r in rows if r["resources"]["status"]=="MEASURED"]
    return {"schema":SCHEMA,"source_sha":head,"attempts":len(rows),"success":sum(r["exit_code"]==0 for r in rows),
            "failed_or_refused":sum(r["exit_code"]!=0 for r in rows),
            "timed_out":sum(r["timeout"] for r in rows),
            "expected_scenario_pass":bool(expected),"cold_reopened":1,"distinct_process_execs":len(rows),
            "wall_seconds":{"min":min(walls),"median":statistics.median(walls),"max":max(walls),"total":sum(walls)},
            "peak_direct_child_rss_bytes":({"status":"MEASURED","max":max(rss)} if len(rss)==len(rows)
                                             else {"status":"UNOBSERVED","reason":"missing_child_measurement"}),
            "provider_mode":"OFFLINE_VERIFIED_CHILD_ALLOWLIST",
            "provider_calls":"UNOBSERVED","tokens":"UNOBSERVED","retries":"UNOBSERVED","billable_cost":"UNOBSERVED",
            "descendant_process_count":"UNOBSERVED","index_sha256":sha(rawidx),
            "G03_FULL":"NOT_EVALUATED_G02_MISSING"}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("root",type=Path)
    p.add_argument("--index-sha256");p.add_argument("--require-expected",action="store_true")
    a=p.parse_args()
    try:
        result=consume(a.root,a.index_sha256)
        require(not a.require_expected or result["expected_scenario_pass"],"SCENARIO_FAILED")
    except Reject as e:
        print("REJECT "+str(e));return 2
    print(json.dumps(result,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())
