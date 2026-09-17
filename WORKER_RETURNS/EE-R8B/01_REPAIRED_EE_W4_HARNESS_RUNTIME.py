from __future__ import annotations
import os, stat, sys, threading, time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence
from .ee_w4_harness_contract import HARNESS_ACTIONS, INELIGIBLE_STATES

def dir_stats(path:Path)->dict[str,int]:
    total=files=max_single=0
    if not path.exists(): return {"bytes":0,"files":0,"max_single_file_bytes":0}
    for root,dirs,names in os.walk(path,followlinks=False):
        dirs[:]=[d for d in dirs if not (Path(root)/d).is_symlink()]
        for name in names:
            p=Path(root)/name
            try: st=p.lstat()
            except FileNotFoundError: continue
            if stat.S_ISREG(st.st_mode):
                z=int(st.st_size); total+=z; files+=1; max_single=max(max_single,z)
    return {"bytes":total,"files":files,"max_single_file_bytes":max_single}

@dataclass
class PeakMonitor:
    scratch:Path; durable:Path; interval_seconds:float=.005
    def __post_init__(self):
        self.stop_event=threading.Event(); self.peak_scratch_bytes=0; self.peak_scratch_files=0; self.max_single_temp_object_bytes=0; self.peak_durable_bytes=0; self.thread=None
    def sample(self):
        s=dir_stats(self.scratch); d=dir_stats(self.durable)
        self.peak_scratch_bytes=max(self.peak_scratch_bytes,s["bytes"]); self.peak_scratch_files=max(self.peak_scratch_files,s["files"]); self.max_single_temp_object_bytes=max(self.max_single_temp_object_bytes,s["max_single_file_bytes"]); self.peak_durable_bytes=max(self.peak_durable_bytes,d["bytes"])
    def run(self):
        while not self.stop_event.is_set(): self.sample(); self.stop_event.wait(self.interval_seconds)
        self.sample()
    def start(self): self.sample(); self.thread=threading.Thread(target=self.run,daemon=True); self.thread.start()
    def stop(self):
        self.stop_event.set()
        if self.thread is not None: self.thread.join(timeout=max(1.,10*self.interval_seconds))
        self.sample()

def expand_argv(t:Sequence[str],request:Path,response:Path,scratch:Path,durable:Path)->list[str]:
    r={"{request}":str(request),"{response}":str(response),"{scratch}":str(scratch),"{durable}":str(durable)}
    return [r.get(x,x) for x in t]

def run_wait4(argv:Sequence[str],stdout_path:Path,stderr_path:Path,env:Mapping[str,str],monitor:PeakMonitor|None=None):
    if not hasattr(os,"wait4") or not hasattr(os,"posix_spawnp"): raise RuntimeError("POSIX posix_spawnp/wait4 required")
    actions=[(os.POSIX_SPAWN_OPEN,1,str(stdout_path),os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600),(os.POSIX_SPAWN_OPEN,2,str(stderr_path),os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600)]
    start=time.monotonic_ns(); pid=os.posix_spawnp(argv[0],list(argv),dict(env),file_actions=actions)
    if monitor: monitor.start()
    try: _,status,usage=os.wait4(pid,0)
    finally:
        if monitor: monitor.stop()
    wall=time.monotonic_ns()-start
    code=os.WEXITSTATUS(status) if os.WIFEXITED(status) else 128+os.WTERMSIG(status) if os.WIFSIGNALED(status) else 126
    return code,usage,wall

def rusage_metrics(u:Any)->dict[str,Any]:
    if sys.platform.startswith("linux"):
        unit="KiB"; peak_rss_bytes=int(u.ru_maxrss*1024)
    elif sys.platform == "darwin":
        unit="bytes"; peak_rss_bytes=int(u.ru_maxrss)
    else:
        raise RuntimeError(f"unsupported ru_maxrss unit for platform: {sys.platform!r}")
    return {"cpu_user_ns":int(u.ru_utime*1e9),"cpu_system_ns":int(u.ru_stime*1e9),"peak_rss_native":int(u.ru_maxrss),"peak_rss_native_unit":unit,"peak_rss_bytes":peak_rss_bytes}
def ineligible_outcome(s:str)->str:
    return {"MISSING_AUTHORITY":"INELIGIBLE_MISSING_AUTHORITY","INELIGIBLE":"INELIGIBLE_CONFIGURED","NONCOMPARABLE":"INELIGIBLE_NONCOMPARABLE","OUTSIDE_REQUESTED_JURISDICTION":"INELIGIBLE_OUTSIDE_REQUESTED_JURISDICTION","SOURCE_CELL_UNAVAILABLE":"INELIGIBLE_SOURCE_CELL_UNAVAILABLE","UNRESOLVED_AUTHORITY":"INELIGIBLE_UNRESOLVED_AUTHORITY"}[s]
def identity_status(oracle:Mapping[str,Any],identities:Mapping[str,Any])->str:
    e=oracle.get("identities")
    if e is None: return "NOT_REQUESTED"
    return "PASS" if isinstance(e,dict) and all(identities.get(k)==v for k,v in e.items()) else "FAIL"
def apply_harness_action(action:str,scratch:Path,durable:Path):
    import shutil
    if action in {"DELETE_SCRATCH","RESET_CANDIDATE_STATE"}: shutil.rmtree(scratch,ignore_errors=True); scratch.mkdir(parents=True,exist_ok=True)
    if action in {"DELETE_DURABLE","RESET_CANDIDATE_STATE"}: shutil.rmtree(durable,ignore_errors=True); durable.mkdir(parents=True,exist_ok=True)
