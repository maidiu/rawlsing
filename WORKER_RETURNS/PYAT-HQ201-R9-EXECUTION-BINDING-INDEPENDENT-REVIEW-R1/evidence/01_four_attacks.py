import sys, os, functools
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq201-r9-binding-review")
print = functools.partial(__builtins__.print, flush=True)
import pyreadstat, pandas as pd
from rawlsing_next.pre553_execution_binding import (BoundSourceExecution, BoundExecutionSpec,
    RoutePassSpec, AccountConstraint, CountKind, AuthorityLabel)
from rawlsing_next.pre553_source_access_broker import SourceAccessBudget, SourceAccessViolation
from rawlsing_next.pre553_source_session import SourceOperationPlan, RowDataMode
W="/tmp/hq201"; os.makedirs(W, exist_ok=True)
sav=os.path.join(W,"s.sav")
if not os.path.exists(sav):
    pyreadstat.write_sav(pd.DataFrame({"A":list(range(300)),"B":list(range(300)),"C":list(range(300))}), sav)
SHA=__import__("hashlib").sha256(open(sav,"rb").read()).hexdigest()
print("carrier:", os.path.getsize(sav), "bytes")

def spec(plan, route, constraints=(), budget=None, sha=SHA):
    return BoundExecutionSpec(source_entry_key="SRC-TEST", path=sav, source_format="SAV",
        plan=plan, expected_sha256=sha, budget=budget or SourceAccessBudget(),
        route_pass=route, constraints=constraints)

print("\n===== ATTACK A: ROUTE-PASS APPLICABILITY (non-route source, outer exact 0) =====")
p_sel=SourceOperationPlan(mode=RowDataMode.SELECTED, selected_variables=("A",))
be=BoundSourceExecution(spec(p_sel, RoutePassSpec(expected=0, maximum=0, token="NON_ROUTE_SOURCE")))
try:
    out=be.execute()
    print(f"  executed: passes_observed={out.full_route_passes_observed} (expected 0)")
except SourceAccessViolation as e:
    print(f"  REFUSED before any operation: {e.code}")
    print(f"  -> a non-route source with outer exact 0 CANNOT perform its admitted SELECTED operation")
print(f"  lower-layer accounts: {be._observed_snapshot()}")

print("\n  -- variant: expected=0 but maximum unset (None) --")
be2=BoundSourceExecution(spec(p_sel, RoutePassSpec(expected=0, maximum=None)))
try:
    out=be2.execute()
    print(f"  executed, passes_observed={out.full_route_passes_observed} -> violates EXACT 0 truthfully reported?")
except SourceAccessViolation as e:
    print(f"  refused AFTER operation: {e.code} (operation already performed!)")
    print(f"  accounts after refusal: {be2._observed_snapshot()}")

print("\n===== ATTACK B: FAILED ATTEMPT / RETRY ZERO =====")
# first attempt fails via a post-execution constraint (FLOOR 999 unsatisfiable)
p_meta=SourceOperationPlan(mode=RowDataMode.METADATA_ONLY)
c_floor=AccountConstraint(account="metadata_reads", kind=CountKind.FLOOR, value=999)
be3=BoundSourceExecution(spec(p_meta, RoutePassSpec(expected=1, maximum=1), (c_floor,)))
try: be3.execute(); print("  attempt 1: no failure (unexpected)")
except SourceAccessViolation as e:
    print(f"  attempt 1 FAILED: {e.code}")
print(f"  after failure: passes_completed={be3._passes_completed} attempted={be3._pass_attempted}")
print(f"  accounts after failure: metadata_reads={be3._observed_snapshot().get('metadata_reads')}")
try:
    be3.execute(); print("  attempt 2: RAN (a second source operation occurred)")
except SourceAccessViolation as e:
    print(f"  attempt 2 REFUSED: {e.code}")
print(f"  after attempt 2: metadata_reads={be3._observed_snapshot().get('metadata_reads')} passes_completed={be3._passes_completed}")

print("\n  -- retry accounting: is 'retries' a separate account/budget? --")
from rawlsing_next.pre553_source_access_broker import SourceAccessAccount
print(f"  account fields include 'retries': {'retries' in SourceAccessAccount().as_dict()}")
o=BoundSourceExecution(spec(p_meta, RoutePassSpec(expected=1, maximum=1), (c_floor,)))
try: o.execute()
except SourceAccessViolation: pass
print(f"  retries observed after failed+failed: {o._observed_snapshot().get('retries')}  (retry law is max 0)")

print("\n===== ATTACK C: COMPLETION SEMANTICS (postcondition fails) =====")
be4=BoundSourceExecution(spec(p_meta, RoutePassSpec(expected=1, maximum=1), (c_floor,)))
try: be4.execute()
except SourceAccessViolation: pass
print(f"  operation returned; postcondition FAILED; _passes_completed={be4._passes_completed}")
print(f"  -> counter incremented BEFORE postcondition check: {be4._passes_completed==1}")

print("\n===== ATTACK D: PYREADSTAT DEPENDENCY INJECTION =====")
class FakePS:
    __version__="1.3.6"; read_sav=None; read_dta=None
fake=FakePS()
be5=BoundSourceExecution(spec(p_meta, RoutePassSpec()), pyreadstat_module=fake)
s=be5._ensure_session()
print(f"  supplied module is: {type(fake).__name__}")
print(f"  session.pyreadstat is the supplied object? {s.broker.pyreadstat is fake}")
print(f"  session.pyreadstat is real pyreadstat? {s.broker.pyreadstat is pyreadstat}")
print(f"  -> supplied dependency SILENTLY DISCARDED (hard-coded None)")
be5.close()
