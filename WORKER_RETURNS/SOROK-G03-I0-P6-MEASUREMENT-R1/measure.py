#!/usr/bin/env python3
"""G03-I0 real P6 process meter: sourcefree, no cohort claim."""
import argparse, hashlib, json, os, platform, signal, subprocess, sys, time
from pathlib import Path

SCHEMA="G03_I0_REAL_P6_V1"
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
def tree_bytes(p):
    if not p.exists(): return 0
    count=0
    for parent,dirs,files in os.walk(p,followlinks=False):
        for name in dirs+files:
            q=Path(parent)/name
            if q.is_symlink(): raise ValueError("STATE_SYMLINK")
            if q.is_file(): count+=q.stat().st_size
            elif not q.is_dir(): raise ValueError("STATE_SPECIAL_FILE")
    return count
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
    if not (repo/P6).is_file(): raise ValueError("ACTUAL_P6_SOURCE_MISSING")
    head=subprocess.check_output(["git","-C",str(repo),"rev-parse","HEAD"],text=True).strip()
    if len(head)!=40: raise ValueError("SOURCE_HEAD_INVALID")
    if subprocess.check_output(["git","-C",str(repo),"status","--porcelain","--untracked-files=no"],text=True).strip():
        raise ValueError("TRACKED_CODE_DIRTY")
    hashes={p:hashbytes((repo/p).read_bytes()) for p in FILES}
    env=env_offline()
    out.mkdir(parents=True,exist_ok=False); (out/"attempts").mkdir()
    state=out/"state"
    manifest={"schema":SCHEMA,"repo_sha":head,"source_hashes":hashes,
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
        before=tree_bytes(state)
        save(p/"start.json",{"id":name,"source_sha":head,"argv":argv,"state_bytes_before":before})
        stdout=p/"stdout.bin";stderr=p/"stderr.bin"
        pid,code,wall,usage,timed_out=measure(argv,repo,env,stdout,stderr,timeout)
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
            "state_bytes_before":before,"state_bytes_after":tree_bytes(state),
            "stdout_sha256":hashbytes(raw),"stdout_bytes":len(raw),
            "stderr_sha256":hashbytes(stderr.read_bytes()),"stderr_bytes":stderr.stat().st_size,
            "output":{"json":output is not None,"status":output.get("status") if output else None,
                      "clock":output.get("clock") if output else None},
            "provider_mode":"OFFLINE_VERIFIED_CHILD_ALLOWLIST",
            "provider":missing_provider(),
            "cold":name=="cold_view",
            "cold_basis":"separate_python_exec_after_wait" if name=="cold_view" else "NOT_APPLICABLE"})
    entries={"attempts/"+n+"/"+f:hashbytes((out/"attempts"/n/f).read_bytes())
             for n,_ in PLAN for f in ("start.json","receipt.json","stdout.bin","stderr.bin")}
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
