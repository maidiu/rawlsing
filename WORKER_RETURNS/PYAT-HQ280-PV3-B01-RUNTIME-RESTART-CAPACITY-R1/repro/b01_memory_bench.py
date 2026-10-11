"""Isolated peak-RSS measurement per manifest size (one process per size).

ru_maxrss on macOS/darwin is reported in BYTES.
"""
import json,resource,sys,time
sys.path.insert(0,'/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq280-b01')
from rawlsing_next.pre553_batch_runner import *
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import ExactRef
import hashlib
def sha(n): return hashlib.sha256(str(n).encode()).hexdigest()
def ref(k,t): return ExactRef(k,f"urn:b01:{k.lower()}:{t}",sha(abs(hash((k,t)))))
n=int(sys.argv[1])
base=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
t0=time.perf_counter(); repo=C11Repository(); units=[]
for i in range(n):
    r=ExactRef("C11LogicalRelease",f"B01-release-{i:05d}",sha(i)); repo._by_ref[r.key]=object()
    units.append(BatchUnitSpec(job_kind="QUERY",job_ref=ref("B01JobRef",f"job-{i:05d}"),
      release_refs=(r,),semantic_input_refs=(ref("B01InputRef",f"in-{i:05d}"),)))
m=BatchManifest(units=tuple(units)); tb=time.perf_counter()-t0
t1=time.perf_counter()
r=BatchExecutionRunner(manifest=m,repository=repo)
r.run(executors={"QUERY":ExecutorBinding(executor_ref=ref("B01Executor","m"),
   execute=lambda u: ExecutionOutcome(result_refs=(ref("B01Result","m"),)))})
te=time.perf_counter()-t1
peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
s=r.summary()
print(json.dumps({"units":n,"manifest_build_s":round(tb,4),"execute_s":round(te,4),
 "peak_rss_bytes":peak,"peak_rss_mib":round(peak/1048576,1),
 "baseline_rss_bytes":base,"delta_bytes":peak-base,"bytes_per_unit":round((peak-base)/n,1) if n else None,
 "receipts":s.actual_execution_receipts,"full":s.full_coverage}))
