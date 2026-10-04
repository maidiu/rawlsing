import sys, os, functools, hashlib, shutil
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq202-r9-binding-final-review")
print = functools.partial(__builtins__.print, flush=True)
import pyreadstat, pandas as pd
from rawlsing_next.pre553_execution_binding import (BoundSourceExecution, BoundExecutionSpec,
    RoutePassSpec, RoutePassApplicability, AccountConstraint, CountKind, AuthorityLabel)
from rawlsing_next.pre553_source_access_broker import SourceAccessBudget, SourceAccessViolation
from rawlsing_next.pre553_source_session import SourceOperationPlan, RowDataMode
W="/tmp/hq202"; os.makedirs(W, exist_ok=True)
sav=os.path.join(W,"s.sav")
if not os.path.exists(sav):
    pyreadstat.write_sav(pd.DataFrame({"A":list(range(300)),"B":list(range(300))}), sav)
SHA=hashlib.sha256(open(sav,"rb").read()).hexdigest()
def SPEC(plan, route, app=RoutePassApplicability.NOT_APPLICABLE, cons=(), budget=None, sha=SHA):
    return BoundExecutionSpec(source_entry_key="K", path=sav, source_format="SAV", plan=plan,
        expected_sha256=sha, budget=budget or SourceAccessBudget(), route_pass=route,
        route_applicability=app, constraints=cons)

print("===== A1: METADATA_ONLY non-route with outer EXACT 0 =====")
be=BoundSourceExecution(SPEC(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY), RoutePassSpec(expected=0, maximum=0)))
o=be.execute()
print(f"  status={o.route_pass_status} applicable={o.route_pass_applicable} observed={o.full_route_passes_observed} metadata={o.observed_accounts.get('metadata_reads')}")
be.close()

print("\n===== A2: SELECTED non-route with outer EXACT 0 =====")
be=BoundSourceExecution(SPEC(SourceOperationPlan(mode=RowDataMode.SELECTED, selected_variables=("A",)), RoutePassSpec(expected=0, maximum=0)))
o=be.execute()
print(f"  status={o.route_pass_status} observed={o.full_route_passes_observed} selected={o.observed_accounts.get('selected_reads')}")
be.close()

print("\n===== A3: FULL plan NOT_APPLICABLE with outer EXACT 0 =====")
be=BoundSourceExecution(SPEC(SourceOperationPlan(mode=RowDataMode.FULL), RoutePassSpec(expected=0, maximum=0)))
o=be.execute()
print(f"  status={o.route_pass_status} observed={o.full_route_passes_observed} full_reads={o.observed_accounts.get('full_reads')}")
be.close()

print("\n===== A4: APPLICABLE route max0 blocks BEFORE session/source op =====")
be=BoundSourceExecution(SPEC(SourceOperationPlan(mode=RowDataMode.FULL), RoutePassSpec(expected=1, maximum=0), app=RoutePassApplicability.APPLICABLE))
try: be.execute(); print("  NOT blocked (BAD)")
except SourceAccessViolation as e: print(f"  {e.code}; session created? {be._session is not None} (expect False)")
be.close()

print("\n===== A5: non-route max0 does NOT block underlying source work =====")
be=BoundSourceExecution(SPEC(SourceOperationPlan(mode=RowDataMode.SELECTED, selected_variables=("B",)), RoutePassSpec(maximum=0)))
o=be.execute()
print(f"  selected_reads={o.observed_accounts.get('selected_reads')} existence={o.observed_accounts.get('existence_checks')} (source work DID occur)")
be.close()

print("\n===== A6: incoherent NOT_APPLICABLE + exact1 fails AT BIND TIME =====")
try:
    SPEC(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY), RoutePassSpec(expected=1))
    print("  spec accepted (BAD)")
except Exception as e: print(f"  refused at bind time: {type(e).__name__}: {str(e)[:70]}")

print("\n===== B1/B2: retries0 -> failed first attempt, second execute refused pre-op =====")
shutil.copy(sav, W+"/t.sav"); sha_t=hashlib.sha256(open(W+"/t.sav","rb").read()).hexdigest()
def tspec(budget=None):
    return BoundExecutionSpec(source_entry_key="T", path=W+"/t.sav", source_format="SAV",
        plan=SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, max_retries=0), expected_sha256=sha_t,
        budget=budget or SourceAccessBudget(retries=0), route_pass=RoutePassSpec(expected=1, maximum=1),
        route_applicability=RoutePassApplicability.APPLICABLE)
be=BoundSourceExecution(tspec()); shutil.move(W+"/t.sav", W+"/t.parked")
try: be.execute()
except SourceAccessViolation as e: print(f"  attempt 1 failed: {e.code}")
a1=dict(be._observed_snapshot()); print(f"  after fail: attempts={be._attempts} retries={a1.get('retries')} existence={a1.get('existence_checks')}")
shutil.move(W+"/t.parked", W+"/t.sav")
try:
    be.execute(); print("  attempt 2 RAN (BAD)")
except SourceAccessViolation as e:
    a2=dict(be._observed_snapshot())
    print(f"  attempt 2 REFUSED: {e.code}")
    print(f"  accounts moved on refusal? {[k for k in a2 if a2[k]!=a1.get(k)] or 'NONE'}")
be.close()

print("\n===== B3: counters distinct =====")
be=BoundSourceExecution(SPEC(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY), RoutePassSpec(expected=1,maximum=1), app=RoutePassApplicability.APPLICABLE))
o=be.execute()
print(f"  attempts={o.route_pass_attempts} retries_observed={o.retries_observed} completed={o.completed_route_passes}")
be.close()

print("\n===== B4: retries>0 advances exactly and stops at ceiling =====")
be=BoundSourceExecution(tspec(budget=SourceAccessBudget(retries=2)))
class Plan:  # non-failing plan after N attempts
    pass
# force failures: park the file so every attempt fails pre-pass (attempt path still admits)
shutil.move(W+"/t.sav", W+"/t.parked")
codes=[]
for i in range(5):
    try: be.execute(); codes.append("RAN")
    except SourceAccessViolation as e: codes.append(e.code)
shutil.move(W+"/t.parked", W+"/t.sav")
a=dict(be._observed_snapshot())
print(f"  ceiling=2 -> codes={codes}")
print(f"  attempts={be._attempts} retries={a.get('retries')} completed={be._completed}")
be.close()

print("\n===== B5: retry binding law (plan.max_retries must equal budget.retries) =====")
try:
    BoundExecutionSpec(source_entry_key="K", path=sav, source_format="SAV", plan=SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, max_retries=3),
        budget=SourceAccessBudget(retries=0), route_pass=RoutePassSpec())
    print("  divergent knobs accepted (BAD)")
except Exception as e: print(f"  divergent knobs refused: {type(e).__name__}: {str(e)[:60]}")
try:
    BoundExecutionSpec(source_entry_key="K", path=sav, source_format="SAV", plan=SourceOperationPlan(mode=RowDataMode.METADATA_ONLY),
        budget=SourceAccessBudget(retries=None), route_pass=RoutePassSpec())
    print("  unbounded ceiling accepted (BAD)")
except Exception as e: print(f"  unbounded ceiling refused: {type(e).__name__}: {str(e)[:60]}")

print("\n===== C1: lower-layer postcondition failure -> NOT a completed pass =====")
c999=AccountConstraint(account="metadata_reads", kind=CountKind.FLOOR, value=999, authority=AuthorityLabel.FROZEN_AUTHORITY)
be=BoundSourceExecution(SPEC(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY), RoutePassSpec(expected=1,maximum=1), app=RoutePassApplicability.APPLICABLE, cons=(c999,)))
try: be.execute()
except SourceAccessViolation as e: print(f"  {e.code}; _completed={be._completed} (expect 0)")
be.close()

print("\n===== C2: outer exact failure (expected=5) -> NOT a completed pass =====")
be=BoundSourceExecution(SPEC(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY), RoutePassSpec(expected=5,maximum=9), app=RoutePassApplicability.APPLICABLE))
try: be.execute()
except SourceAccessViolation as e: print(f"  {e.code}; _completed={be._completed} (expect 0)")
be.close()

print("\n===== D: injected module reaches the seam =====")
class Stub:
    __version__="1.3.6"; read_sav=None; read_dta=None; _probe="STUB"
be=BoundSourceExecution(SPEC(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY), RoutePassSpec()), pyreadstat_module=Stub())
s=be._ensure_session()
print(f"  session.broker.pyreadstat is supplied stub? {s.broker.pyreadstat is Stub or getattr(s.broker.pyreadstat,'_probe',None)=='STUB'}")
print(f"  is real pyreadstat? {s.broker.pyreadstat is pyreadstat}")
be.close()
