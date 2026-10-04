import sys, os, functools, hashlib
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq201-r9-binding-review")
print = functools.partial(__builtins__.print, flush=True)
from rawlsing_next.pre553_execution_binding import (BoundSourceExecution, BoundExecutionSpec,
    RoutePassSpec, AccountConstraint, CountKind)
from rawlsing_next.pre553_source_access_broker import SourceAccessBudget, SourceAccessViolation
from rawlsing_next.pre553_source_session import SourceOperationPlan, RowDataMode
sav="/tmp/hq201/s.sav"
def spec(plan, route, sha):
    return BoundExecutionSpec(source_entry_key="SRC-TEST", path=sav, source_format="SAV",
        plan=plan, expected_sha256=sha, budget=SourceAccessBudget(), route_pass=route)

print("===== ATTACK B (sharpest): failure BEFORE the pass increment =====")
print("Case: source operation raises (identity mismatch -> session.run raises) so the increment never runs")
p=SourceOperationPlan(mode=RowDataMode.METADATA_ONLY)
be=BoundSourceExecution(spec(p, RoutePassSpec(expected=1, maximum=1), sha="0"*64))
try: be.execute(); print("  attempt 1: no failure (unexpected)")
except SourceAccessViolation as e: print(f"  attempt 1 FAILED: {e.code}")
a1=dict(be._observed_snapshot())
print(f"  after failure: passes_completed={be._passes_completed} accounts: existence={a1.get('existence_checks')} hash={a1.get('hash_passes')} metadata={a1.get('metadata_reads')}")
try:
    o=be.execute()
    a2=dict(be._observed_snapshot())
    print(f"  attempt 2 RAN: passes_completed={be._passes_completed} metadata_reads={a2.get('metadata_reads')} existence={a2.get('existence_checks')} hash={a2.get('hash_passes')}")
    print(f"  -> a SECOND SOURCE OPERATION OCCURRED even though retries max is 0")
    print(f"  -> retries account observed: {a2.get('retries')} (never incremented)")
except SourceAccessViolation as e:
    print(f"  attempt 2 REFUSED: {e.code}")

print("\n===== does the wrapper enforce a retry CEILING at all? =====")
be2=BoundSourceExecution(spec(p, RoutePassSpec(expected=1, maximum=1), sha="0"*64))
be2.spec.budget  # budget has retries default 0
tries=0
for i in range(3):
    try: be2.execute(); tries+=1; print(f"  attempt {i+1}: ran")
    except SourceAccessViolation as e:
        a=be2._observed_snapshot()
        print(f"  attempt {i+1}: {e.code}; metadata_reads={a.get('metadata_reads')} retries={a.get('retries')}")
print(f"  total attempts that executed: {tries}")
