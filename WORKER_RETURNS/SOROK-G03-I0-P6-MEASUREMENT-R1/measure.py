#!/usr/bin/env python3
"""G03-I0 real P6 process meter: sourcefree, no cohort claim."""
import argparse, hashlib, json, os, platform, signal, sqlite3, subprocess, sys, time
from pathlib import Path

SCHEMA="G03_I0_REAL_P6_V2"
STATE_DIGEST_SCHEME="G03_STATE_PATH_CONTENT_SHA256_V1"
STATE_LOGICAL_SCHEME="G03_SQLITE_ROWS_AND_OTHER_CONTENT_V1"
SQLITE_REL="actual-p2/p3_psyche.sqlite3"
P6="WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/run_p6.py"
FILES=[P6, "WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/house.py",
       "WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/mii.py",
       "WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/situated.py",
       "WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1/situated_provider.py",
       "WORKER_RETURNS/SOROK-P5-CONTINUOUS-EXPERIENCE-R1/run_p5.py"]
PLAN=[("new",["new"]),("view",["view"]),("wait",["wait","1"]),
      ("cold_view",["view"]),("fail_wait",["wait","0"])]

def hashbytes(b): return hashlib.sha256(b).hexdigest()
def data(x): return (json.dumps(x,sort_keys=True,ensure_ascii=False,allow_nan=False,separators=(",",":"))+"\n").encode()
def save(p,x):
    p=Path(p); tmp=p.with_name(p.name+".tmp")
    with tmp.open("xb") as f:
        f.write(data(x)); f.flush(); os.fsync(f.fileno())
    tmp.replace(p)
def state_snapshot(root, *, logical=False):
    """Best-effort, path-sensitive state content snapshot; not a transaction/OS attestation."""
    root=Path(root)
    if not root.exists():
        return {"status":"ABSENT","bytes":0,"files":0,
                "sha256":hashbytes(data({"v":1,"status":"ABSENT"}))}
    if root.is_symlink() or not root.is_dir(): raise ValueError("STATE_ROOT_UNSAFE")
    entries=[]; total=0; count=0
    for parent,dirs,names in os.walk(root,followlinks=False):
        dirs.sort();names.sort()
        for name in dirs:
            q=Path(parent)/name
            if q.is_symlink() or not q.is_dir(): raise ValueError("STATE_DIR_UNSAFE")
            entries.append(["D",q.relative_to(root).as_posix()])
        for name in names:
            q=Path(parent)/name
            if q.is_symlink() or not q.is_file():raise ValueError("STATE_FILE_UNSAFE")
            before=q.stat(); raw=q.read_bytes(); after=q.stat()
            if (before.st_size,before.st_mtime_ns,before.st_ino)!=(after.st_size,after.st_mtime_ns,after.st_ino):
                raise ValueError("STATE_CHANGED_DURING_SNAPSHOT")
            rel=q.relative_to(root).as_posix()
            if logical and rel==SQLITE_REL:
                sql=sqlite_logical_digest(root)
                if sql.get("status")!="MEASURED":
                    raise ValueError("SQLITE_LOGICAL_SNAPSHOT_UNAVAILABLE")
                entries.append(["SQLITE_ROWS",rel,sql["sha256"]])
            else:
                entries.append(["F",rel,len(raw),hashbytes(raw)])
            count+=1;total+=len(raw)
    entries.sort()
    return {"status":"PRESENT","bytes":total,"files":count,
            "sha256":hashbytes(data({"v":1,"status":"PRESENT","entries":entries}))}

def state_file_digests(root):
    """Diagnostic only: report paths whose persisted bytes changed on refused P6."""
    root=Path(root)
    if not root.exists():return {}
    found={}
    for parent,_,names in os.walk(root,followlinks=False):
        for name in names:
            q=Path(parent)/name
            if q.is_file() and not q.is_symlink():
                found[q.relative_to(root).as_posix()]=hashbytes(q.read_bytes())
    return found

def sqlite_logical_digest(root):
    """Diagnose physical SQLite page churn versus independently readable table contents."""
    path=Path(root)/"actual-p2"/"p3_psyche.sqlite3"
    if not path.exists():return {"status":"ABSENT"}
    try:
        uri="file:"+str(path.resolve())+"?mode=ro&immutable=1"
        with sqlite3.connect(uri,uri=True) as db:
            names=[row[0] for row in db.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
            tables=[]
            for name in names:
                safe=name.replace('"','""')
                rows=[[(v.hex() if isinstance(v,bytes) else v) for v in row]
                      for row in db.execute('SELECT * FROM "'+safe+'"')]
                rows.sort(key=lambda row:data(row))
                tables.append([name,rows])
            schema=list(db.execute("SELECT type,name,sql FROM sqlite_master ORDER BY type,name"))
            return {"status":"MEASURED","sha256":hashbytes(data(
                    {"tables":tables,"schema":schema,
                     "user_version":db.execute("PRAGMA user_version").fetchone()[0]})),
                    "tables":{name:len(rows) for name,rows in tables}}
    except sqlite3.DatabaseError:
        return {"status":"UNOBSERVED","reason":"sqlite_readonly_inspection_failed"}

def env_offline():
    return {"PATH":os.environ.get("PATH","/usr/bin:/bin"),"LANG":"C.UTF-8",
            "PYTHONDONTWRITEBYTECODE":"1","PYTHONNOUSERSITE":"1","PYTHONHASHSEED":"0"}
def measure(argv,cwd,environment,stdout,stderr,timeout):
    began=time.perf_counter(); timed_out=False; usage=None
    with stdout.open("xb") as out,stderr.open("xb") as err:
        proc=subprocess.Popen(argv,cwd=cwd,env=environment,stdin=subprocess.DEVNULL,
                              stdout=out,stderr=err,start_new_session=True)
        while True:
            if hasattr(os,"wait4"):
                pid,status,ru=os.wait4(proc.pid,os.WNOHANG)
                if pid==proc.pid:
                    proc.returncode=os.waitstatus_to_exitcode(status); usage=ru; break
            elif proc.poll() is not None: break
            if time.perf_counter()-began>timeout and not timed_out:
                timed_out=True
                try: os.killpg(proc.pid,signal.SIGKILL)
                except ProcessLookupError: pass
            time.sleep(.02)
        out.flush(); err.flush()
    return proc.pid,proc.returncode,time.perf_counter()-began,usage,timed_out
def process_usage(ru):
    if ru is None: return {"status":"UNOBSERVED","reason":"wait4_unavailable"}
    sysname=platform.system()
    if sysname not in ("Linux","Darwin"):
        return {"status":"UNOBSERVED","reason":"unknown_ru_maxrss_unit"}
    unit,mult=("KiB",1024) if sysname=="Linux" else ("bytes",1)
    return {"status":"MEASURED","scope":"single_wait4_child_not_process_tree",
            "cpu_user_s":ru.ru_utime,"cpu_system_s":ru.ru_stime,
            "ru_maxrss_native":ru.ru_maxrss,"ru_maxrss_native_unit":unit,
            "peak_rss_bytes":int(ru.ru_maxrss)*mult}
def missing_provider():
    return {key:{"status":"UNOBSERVED","reason":"no_authenticated_"+key+"_observation"}
            for key in ("calls","tokens","retries","billable_cost")}
def run(repo,out,timeout):
    repo=repo.resolve(); out=out.resolve()
    if out==repo or repo in out.parents: raise ValueError("OUTPUT_MUST_BE_OUTSIDE_SOURCE_TREE")
    if not (repo/P6).is_file(): raise ValueError("ACTUAL_P6_SOURCE_MISSING")
    head=subprocess.check_output(["git","-C",str(repo),"rev-parse","HEAD"],text=True).strip()
    if len(head)!=40: raise ValueError("SOURCE_HEAD_INVALID")
    if subprocess.check_output(["git","-C",str(repo),"status","--porcelain","--untracked-files=all"],text=True).strip():
        raise ValueError("SOURCE_TREE_DIRTY_OR_UNTRACKED")
    hashes={p:hashbytes((repo/p).read_bytes()) for p in FILES}
    env=env_offline()
    out.mkdir(parents=True,exist_ok=False); (out/"attempts").mkdir()
    state=out/"state"
    manifest={"schema":SCHEMA,"repo_sha":head,"source_hashes":hashes,
              "state_digest_scheme":STATE_DIGEST_SCHEME,
              "state_logical_scheme":STATE_LOGICAL_SCHEME,
              "runner_sha256":hashbytes(Path(__file__).read_bytes()),
              "python_executable_sha256":hashbytes(Path(sys.executable).read_bytes()),
              "os":platform.system(),"os_release":platform.release(),
              "python":platform.python_version(),
              "env_keys":sorted(env),"env_fingerprint_sha256":hashbytes(data(env)),
              "provider_mode":"OFFLINE_VERIFIED_CHILD_ALLOWLIST",
              "network_calls":"UNOBSERVED","descendant_processes":"UNOBSERVED",
              "plan":[{"id":n,"args":a,"cold":n=="cold_view"} for n,a in PLAN]}
    save(out/"manifest.json",manifest)
    for name,args in PLAN:
        p=out/"attempts"/name;p.mkdir()
        argv=[sys.executable,str(repo/P6),"--state",str(state),*args]
        snap_before=state_snapshot(state);logical_before=state_snapshot(state,logical=True)
        before=snap_before["bytes"]
        before_files=state_file_digests(state) if name=="fail_wait" else None
        before_sqlite=sqlite_logical_digest(state) if name=="fail_wait" else None
        save(p/"start.json",{"id":name,"source_sha":head,"argv":argv,
                             "state_bytes_before":before,"state_snapshot_before":snap_before})
        stdout=p/"stdout.bin";stderr=p/"stderr.bin"
        pid,code,wall,usage,timed_out=measure(argv,repo,env,stdout,stderr,timeout)
        snap_after=state_snapshot(state);logical_after=state_snapshot(state,logical=True)
        if name=="fail_wait" and snap_before!=snap_after:
            after_files=state_file_digests(state)
            changed=sorted(k for k in set(before_files)|set(after_files)
                           if before_files.get(k)!=after_files.get(k))
            print("REFUSED_P6_CHANGED_PERSISTED_PATHS="+json.dumps(changed),file=sys.stderr)
            print("REFUSED_P6_SQLITE_LOGICAL_BEFORE_AFTER="+json.dumps([before_sqlite,sqlite_logical_digest(state)]),file=sys.stderr)
        raw=stdout.read_bytes()
        try:
            output=json.loads(raw)
            if not isinstance(output,dict):output=None
        except (ValueError,UnicodeDecodeError):output=None
        save(p/"receipt.json",{
            "schema":SCHEMA,"id":name,"source_sha":head,"source_hashes":hashes,
            "argv":argv,"child_pid":pid,"exit_code":code,"timeout":timed_out,
            "wall_seconds":wall,"resources":process_usage(usage),
            "direct_children_started":1,"descendants":"UNOBSERVED",
            "state_bytes_before":before,"state_bytes_after":snap_after["bytes"],
            "state_snapshot_before":snap_before,"state_snapshot_after":snap_after,
            "state_logical_before":logical_before,"state_logical_after":logical_after,
            "stdout_sha256":hashbytes(raw),"stdout_bytes":len(raw),
            "stderr_sha256":hashbytes(stderr.read_bytes()),"stderr_bytes":stderr.stat().st_size,
            "output":{"json":output is not None,"status":output.get("status") if output else None,
                      "clock":output.get("clock") if output else None},
            "provider_mode":"OFFLINE_VERIFIED_CHILD_ALLOWLIST",
            "provider":missing_provider(),
            "cold":name=="cold_view",
            "cold_basis":"separate_python_exec_after_wait" if name=="cold_view" else "NOT_APPLICABLE"})
    # The original external index anchored attempts but NOT manifest provenance.
    # Fail closed on untracked/new source imports or source mutation during the sample.
    if subprocess.check_output(["git","-C",str(repo),"rev-parse","HEAD"],text=True).strip()!=head:
        raise ValueError("SOURCE_HEAD_CHANGED_DURING_RUN")
    if subprocess.check_output(["git","-C",str(repo),"status","--porcelain","--untracked-files=all"],text=True).strip():
        raise ValueError("SOURCE_TREE_CHANGED_DURING_RUN")
    if any(hashbytes((repo/p).read_bytes())!=digest for p,digest in hashes.items()):
        raise ValueError("SOURCE_FILE_CHANGED_DURING_RUN")
    entries={"manifest.json":hashbytes((out/"manifest.json").read_bytes())}
    entries.update({"attempts/"+n+"/"+f:hashbytes((out/"attempts"/n/f).read_bytes())
             for n,_ in PLAN for f in ("start.json","receipt.json","stdout.bin","stderr.bin")})
    save(out/"index.json",{"schema":SCHEMA,"entries":entries})
    import read_receipts
    summary=read_receipts.consume(out)
    save(out/"summary.json",summary)
    print("EVIDENCE_INDEX_SHA256="+hashbytes((out/"index.json").read_bytes()))
    print(json.dumps(summary,sort_keys=True,allow_nan=False))
    return 0 if summary["expected_scenario_pass"] else 1
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo",required=True,type=Path);p.add_argument("--out",required=True,type=Path)
    p.add_argument("--timeout",type=float,default=120);a=p.parse_args()
    if a.timeout<=0:p.error("timeout must be positive")
    return run(a.repo,a.out,a.timeout)
if __name__=="__main__":raise SystemExit(main())
