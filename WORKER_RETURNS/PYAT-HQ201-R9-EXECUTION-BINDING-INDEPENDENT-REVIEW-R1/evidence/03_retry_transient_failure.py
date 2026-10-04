import sys, os, functools, hashlib, shutil
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq201-r9-binding-review")
print = functools.partial(__builtins__.print, flush=True)
from rawlsing_next.pre553_execution_binding import (BoundSourceExecution, BoundExecutionSpec, RoutePassSpec)
from rawlsing_next.pre553_source_access_broker import SourceAccessBudget, SourceAccessViolation
from rawlsing_next.pre553_source_session import SourceOperationPlan, RowDataMode
src="/tmp/hq201/s.sav"; dst="/tmp/hq201/transient.sav"
shutil.copy(src,dst)
sha=hashlib.sha256(open(dst,"rb").read()).hexdigest()
moved="/tmp/hq201/transient.parked"
if os.path.exists(moved): os.remove(moved)
spec=lambda: BoundExecutionSpec(source_entry_key="T", path=dst, source_format="SAV",
    plan=SourceOperationPlan(mode=RowDataMode.METADATA_ONLY), expected_sha256=sha,
    budget=SourceAccessBudget(), route_pass=RoutePassSpec(expected=1, maximum=1))
be=BoundSourceExecution(spec())
os.rename(dst, moved)   # make the source transiently unavailable
try: be.execute(); print("attempt 1: no failure (unexpected)")
except SourceAccessViolation as e:
    a=dict(be._observed_snapshot())
    print(f"attempt 1 FAILED: {e.code}  passes_completed={be._passes_completed} accounts={a if a else '{} (none)'}")
os.rename(moved, dst)   # restore the source
try:
    o=be.execute()
    a=dict(be._observed_snapshot())
    print(f"attempt 2 SUCCEEDED: passes_completed={be._passes_completed} full_route_passes_observed={o.full_route_passes_observed}")
    print(f"  accounts: existence={a.get('existence_checks')} hash={a.get('hash_passes')} metadata={a.get('metadata_reads')} retries={a.get('retries')}")
    print(f"  DECISIVE: two source operations (4 pre-op ops) under one bound execution; retries account stayed {a.get('retries')}")
except SourceAccessViolation as e:
    print(f"attempt 2 REFUSED: {e.code}")
