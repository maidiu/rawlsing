#!/usr/bin/env python3
"""Independent read-only first consumer for saved raw G03-I0 P6 receipts."""
import argparse,hashlib,json,math,statistics,os,sqlite3,subprocess
from pathlib import Path
# Deliberately independent of the measurement writer's declared plan.
SCHEMA="G03_I0_REAL_P6_V2"
STATE_DIGEST_SCHEME="G03_STATE_PATH_CONTENT_SHA256_V1"
STATE_LOGICAL_SCHEME="G03_SQLITE_ROWS_AND_OTHER_CONTENT_V1"
SQLITE_REL="actual-p2/p3_psyche.sqlite3"
P6="WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py"
FILES=[P6,"WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/house.py",
       "WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/mii.py",
       "WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/situated.py",
       "WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/situated_provider.py",
       "WORKER_RETURNS/SOROK-P5-CONTINUOUS-EXPERIENCE-R1/run_p5.py"]
PLAN=[("new",["new"]),("view",["view"]),("wait",["wait","1"]),
      ("cold_view",["view"]),("fail_wait",["wait","0"])]

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
def canonical(obj):
    return (json.dumps(obj,sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(",",":"))+"\n").encode()
def sqlite_logical_digest(root):
    path=Path(root)/SQLITE_REL
    require(path.is_file() and not path.is_symlink(),"SQLITE_LOGICAL_PATH_UNAVAILABLE")
    try:
        with sqlite3.connect("file:"+str(path.resolve())+"?mode=ro&immutable=1",uri=True) as db:
            require(db.execute("PRAGMA quick_check(1)").fetchone()[0]=="ok",
                    "SQLITE_INTEGRITY_CHECK_FAILED")
            names=[row[0] for row in db.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
            tables=[]
            for name in names:
                safe=name.replace('"','""')
                rows=[[(v.hex() if isinstance(v,bytes) else v) for v in row]
                      for row in db.execute('SELECT * FROM "'+safe+'"')]
                rows.sort(key=lambda row:canonical(row))
                tables.append([name,rows])
            schema=list(db.execute("SELECT type,name,sql FROM sqlite_master ORDER BY type,name"))
            return sha(canonical({"tables":tables,"schema":schema,
                    "user_version":db.execute("PRAGMA user_version").fetchone()[0]}))
    except sqlite3.DatabaseError as e:
        raise Reject("SQLITE_LOGICAL_READ_FAILED") from e

def state_snapshot(root, *, logical=False):
    """Independent receiver's path/content check; no dependency on the meter."""
    root=Path(root)
    if not root.exists():
        return {"status":"ABSENT","bytes":0,"files":0,
                "sha256":sha(canonical({"v":1,"status":"ABSENT"}))}
    require(not root.is_symlink() and root.is_dir(),"STATE_ROOT_UNSAFE")
    entries=[];total=0;count=0
    for parent,dirs,names in os.walk(root,followlinks=False):
        dirs.sort();names.sort()
        for name in dirs:
            q=Path(parent)/name
            require(not q.is_symlink() and q.is_dir(),"STATE_DIR_UNSAFE")
            entries.append(["D",q.relative_to(root).as_posix()])
        for name in names:
            q=Path(parent)/name
            require(not q.is_symlink() and q.is_file(),"STATE_FILE_UNSAFE")
            before=q.stat();raw=q.read_bytes();after=q.stat()
            require((before.st_size,before.st_mtime_ns,before.st_ino)==
                    (after.st_size,after.st_mtime_ns,after.st_ino),"STATE_SNAPSHOT_RACE")
            rel=q.relative_to(root).as_posix()
            if logical and rel==SQLITE_REL:
                entries.append(["SQLITE_ROWS",rel,sqlite_logical_digest(root)])
            else:
                entries.append(["F",rel,len(raw),sha(raw)])
            count+=1;total+=len(raw)
    entries.sort()
    return {"status":"PRESENT","bytes":total,"files":count,
            "sha256":sha(canonical({"v":1,"status":"PRESENT","entries":entries}))}
def check_snapshot(s):
    require(isinstance(s,dict) and set(s)=={"status","bytes","files","sha256"},"STATE_SNAPSHOT_INVALID")
    require(s["status"] in ("PRESENT","ABSENT") and type(s["bytes"]) is int and s["bytes"]>=0
            and type(s["files"]) is int and s["files"]>=0 and validhash(s["sha256"]),"STATE_SNAPSHOT_INVALID")
    if s["status"]=="ABSENT":
        require(s["bytes"]==0 and s["files"]==0 and
                s["sha256"]==sha(canonical({"v":1,"status":"ABSENT"})),
                "STATE_ABSENT_DIGEST_BAD")
def verify_repo(repo,head,source):
    """Optional present-checkout source attestation. Not needed for offline archive reading."""
    repo=Path(repo).resolve()
    try:
        actual=subprocess.check_output(["git","-C",str(repo),"rev-parse","HEAD"],text=True).strip()
        dirty=subprocess.check_output(["git","-C",str(repo),"status","--porcelain",
                                       "--untracked-files=all"],text=True).strip()
    except (OSError,subprocess.CalledProcessError) as e:
        raise Reject("SOURCE_RECHECK_UNAVAILABLE") from e
    require(actual==head,"SOURCE_REPO_SHA_MISMATCH")
    require(not dirty,"SOURCE_REPO_DIRTY_OR_UNTRACKED")
    for p,digest in source.items():
        q=repo/p
        require(q.is_file() and not q.is_symlink(),"SOURCE_FILE_NOT_REGULAR:"+p)
        require(sha(q.read_bytes())==digest,"SOURCE_FILE_HASH_MISMATCH:"+p)

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
    require(isinstance(idx.get("entries"),dict) and
            idx["entries"].get("manifest.json")==sha((root/"manifest.json").read_bytes()),
            "MANIFEST_NOT_INDEXED")
    require(man.get("schema")==SCHEMA and idx.get("schema")==SCHEMA,"SCHEMA_BAD")
    require(man.get("state_digest_scheme")==STATE_DIGEST_SCHEME,"STATE_DIGEST_SCHEME_MISSING")
    require(man.get("state_logical_scheme")==STATE_LOGICAL_SCHEME,"STATE_LOGICAL_SCHEME_MISSING")
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
    expected={"manifest.json"} | {"attempts/"+n+"/"+f for n,_ in PLAN for f in ("start.json","receipt.json","stdout.bin","stderr.bin")}
    require(isinstance(idx.get("entries"),dict) and set(idx["entries"])==expected,"INDEX_ATTEMPTS_MISSING")
    rows=[]; outputs=[]
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
        before_snap=r.get("state_snapshot_before"); after_snap=r.get("state_snapshot_after")
        check_snapshot(before_snap);check_snapshot(after_snap)
        log_before=r.get("state_logical_before");log_after=r.get("state_logical_after")
        check_snapshot(log_before);check_snapshot(log_after)
        require(log_before["bytes"]==before_snap["bytes"] and
                log_after["bytes"]==after_snap["bytes"],"STATE_LOGICAL_SIZE_MISMATCH")
        require(start.get("state_snapshot_before")==before_snap and
                before_snap["bytes"]==r["state_bytes_before"] and
                after_snap["bytes"]==r["state_bytes_after"],"STATE_SNAPSHOT_SIZE_OR_START_MISMATCH")
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
        rows.append(r);outputs.append(o)
    require(len({r["child_pid"] for r in rows})==len(rows),"DUPLICATED_CHILD_EXEC_ID")
    require(rows[0]["state_bytes_before"]==0 and
            rows[0]["state_snapshot_before"]["status"]=="ABSENT","STATE_NOT_FRESH")
    require(all(a["state_bytes_after"]==b["state_bytes_before"] and a["argv"][3]==b["argv"][3]
                for a,b in zip(rows,rows[1:])),"STATE_CONTINUITY_BAD")
    require(all(a["state_snapshot_after"]==b["state_snapshot_before"]
                for a,b in zip(rows,rows[1:])),"STATE_CONTENT_CONTINUITY_BAD")
    require(all(a["state_logical_after"]["sha256"]==b["state_logical_before"]["sha256"]
                for a,b in zip(rows,rows[1:])),"STATE_LOGICAL_CONTINUITY_BAD")
    refused_physical_changed=(rows[-1]["state_snapshot_before"]["sha256"] !=
                              rows[-1]["state_snapshot_after"]["sha256"])
    refused_logical_changed=(rows[-1]["state_logical_before"]["sha256"] !=
                             rows[-1]["state_logical_after"]["sha256"])
    require(state_snapshot(root/"state")==rows[-1]["state_snapshot_after"],
            "STATE_FINAL_CONTENT_MISMATCH")
    require(state_snapshot(root/"state",logical=True)["sha256"]==
            rows[-1]["state_logical_after"]["sha256"],"STATE_FINAL_LOGICAL_MISMATCH")
    # Source-exact semantic oracle: fresh root, genuine +1 wait, reopened
    # clock preservation, specified refusal and zero state mutation on refusal.
    semantic=(all(isinstance(o,dict) and type(o.get("clock")) is int
                  and isinstance(o.get("mii_surface"),dict) for o in outputs[:4])
              and outputs[0]["clock"]==outputs[1]["clock"]
              and outputs[2]["clock"]==outputs[1]["clock"]+1
              and outputs[3]["clock"]==outputs[2]["clock"]
              and outputs[2].get("admission")=="ADMITTED"
              and isinstance(outputs[4],dict)
              and outputs[4].get("reason")=="P6_WAIT_DURATION_OUT_OF_RANGE"
              and rows[4]["state_bytes_before"]==rows[4]["state_bytes_after"])
    expected=all(r["exit_code"]==0 and r["output"]["json"] and not r["timeout"] for r in rows[:4])
    expected=expected and rows[-1]["exit_code"]==2 and rows[-1]["output"]["status"]=="REFUSED" and semantic and not refused_logical_changed
    walls=[r["wall_seconds"] for r in rows]
    rss=[r["resources"]["peak_rss_bytes"] for r in rows if r["resources"]["status"]=="MEASURED"]
    result={"schema":SCHEMA,"source_sha":head,"attempts":len(rows),"success":sum(r["exit_code"]==0 for r in rows),
            "failed_or_refused":sum(r["exit_code"]!=0 for r in rows),
            "timed_out":sum(r["timeout"] for r in rows),
            "expected_scenario_pass":bool(expected),"cold_reopened":1,"distinct_process_execs":len(rows),
            "wall_seconds":{"min":min(walls),"median":statistics.median(walls),"max":max(walls),"total":sum(walls)},
            "peak_direct_child_rss_bytes":({"status":"MEASURED","max":max(rss)} if len(rss)==len(rows)
                                             else {"status":"UNOBSERVED","reason":"missing_child_measurement"}),
            "provider_mode":"OFFLINE_VERIFIED_CHILD_ALLOWLIST",
            "provider_calls":"UNOBSERVED","tokens":"UNOBSERVED","retries":"UNOBSERVED","billable_cost":"UNOBSERVED",
            "descendant_process_count":"UNOBSERVED","index_sha256":sha(rawidx),
            "G03_FULL":"NOT_EVALUATED_G02_MISSING",
            "refused_state":{"physical_content_changed":refused_physical_changed,
                             "logical_content_changed":refused_logical_changed,
                             "logical_witness":STATE_LOGICAL_SCHEME,
                             "sqlite_page_churn_not_equated_with_actor_change":True}}
    # Do not launder the planned negative into a 20% real-world failure rate.
    observed_refusals=sum(r["exit_code"]!=0 and isinstance(o,dict)
                          and o.get("status")=="REFUSED" for r,o in zip(rows,outputs))
    expected_refusals=int(rows[4]["exit_code"]==2 and isinstance(outputs[4],dict)
                         and outputs[4].get("reason")=="P6_WAIT_DURATION_OUT_OF_RANGE")
    result["expected_refusals"]=expected_refusals
    result["all_refusals"]=observed_refusals
    result["unexpected_failed_or_refused"]=result["failed_or_refused"]-expected_refusals
    result["observed_refusal_fraction_of_attempts"]=observed_refusals/len(rows)
    result["unexpected_nonzero_fraction_of_attempts"]=result["unexpected_failed_or_refused"]/len(rows)
    result["wall_by_attempt_seconds"]={n:r["wall_seconds"] for (n,_),r in zip(PLAN,rows)}
    result["state_after_bytes"]={n:r["state_bytes_after"] for (n,_),r in zip(PLAN,rows)}
    result["state_net_bytes"]=rows[-1]["state_bytes_after"]-rows[0]["state_bytes_before"]
    result["rss_direct_child_bytes"]=({"status":"MEASURED","min":min(rss),
                  "median":statistics.median(rss),"max":max(rss)}
                  if len(rss)==len(rows) else {"status":"UNOBSERVED","reason":"incomplete_wait4_samples"})
    if all(r["resources"]["status"]=="MEASURED" for r in rows):
        result["cpu_direct_child_seconds"]={
            "status":"MEASURED","user_total":sum(r["resources"]["cpu_user_s"] for r in rows),
            "system_total":sum(r["resources"]["cpu_system_s"] for r in rows),
            "scope":"sum_direct_child_wait4_not_process_tree"}
    else:
        result["cpu_direct_child_seconds"]={"status":"UNOBSERVED","reason":"incomplete_wait4_samples"}
    if (root/"summary.json").is_file():
        require(load(root/"summary.json")==result,"SUMMARY_FORGED")
    return result
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("root",type=Path)
    p.add_argument("--index-sha256");p.add_argument("--repo",type=Path)
    p.add_argument("--require-expected",action="store_true")
    a=p.parse_args()
    try:
        result=consume(a.root,a.index_sha256)
        if a.repo is not None:
            man=load(a.root/"manifest.json")
            verify_repo(a.repo,man["repo_sha"],man["source_hashes"])
        require(not a.require_expected or result["expected_scenario_pass"],"SCENARIO_FAILED")
    except Reject as e:
        print("REJECT "+str(e));return 2
    print(json.dumps(result,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())
