import sys, os, functools, hashlib, shutil
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq202-r9-binding-final-review")
print = functools.partial(__builtins__.print, flush=True)
import pyreadstat, pandas as pd
from rawlsing_next.pre553_execution_binding import (BoundSourceExecution, BoundExecutionSpec,
    RoutePassSpec, RoutePassApplicability, AccountConstraint, CountKind, AuthorityLabel)
from rawlsing_next.pre553_source_access_broker import SourceAccessBudget, SourceAccessViolation
from rawlsing_next.pre553_source_session import SourceOperationPlan, RowDataMode
W="/tmp/hq202"; sav=os.path.join(W,"s.sav")
SHA=hashlib.sha256(open(sav,"rb").read()).hexdigest()
class Stub:
    __version__="1.3.6"; read_sav=None; read_dta=None; _probe="STUB"

print("===== B4: retries>0 advances exactly and stops at ceiling (both knobs = 2) =====")
src=W+"/t2.sav"; park=W+"/t2.parked"; shutil.copy(sav, src)
sha2=hashlib.sha256(open(src,"rb").read()).hexdigest()
spec=BoundExecutionSpec(source_entry_key="T", path=src, source_format="SAV",
    plan=SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, max_retries=2), expected_sha256=sha2,
    budget=SourceAccessBudget(retries=2), route_pass=RoutePassSpec(expected=1,maximum=1),
    route_applicability=RoutePassApplicability.APPLICABLE)
be=BoundSourceExecution(spec)
shutil.move(src, park)   # every attempt fails pre-pass so we stay on the retry path
codes=[]
for i in range(6):
    try: be.execute(); codes.append("RAN")
    except SourceAccessViolation as e: codes.append(e.code)
shutil.move(park, src)
a=dict(be._observed_snapshot())
print(f"  ceiling=2 -> {codes}")
print(f"  attempts={be._attempts} retries_account={a.get('retries')} completed={be._completed}")
print(f"  distinct counters: attempts={be._attempts} retries={a.get('retries')} completed={be._completed}")
be.close()

print("\n===== C1: lower-layer postcondition failure -> NOT completed =====")
c999=AccountConstraint(account="metadata_reads", kind=CountKind.FLOOR, value=999, authority=AuthorityLabel.FROZEN_AUTHORITY)
be=BoundSourceExecution(BoundExecutionSpec(source_entry_key="K", path=sav, source_format="SAV",
    plan=SourceOperationPlan(mode=RowDataMode.METADATA_ONLY), expected_sha256=SHA,
    budget=SourceAccessBudget(), route_pass=RoutePassSpec(expected=1,maximum=1),
    route_applicability=RoutePassApplicability.APPLICABLE, constraints=(c999,)))
try: be.execute()
except SourceAccessViolation as e: print(f"  {e.code}; _completed={be._completed} (expect 0)")
be.close()

print("\n===== C2: outer exact failure -> NOT completed =====")
be=BoundSourceExecution(BoundExecutionSpec(source_entry_key="K", path=sav, source_format="SAV",
    plan=SourceOperationPlan(mode=RowDataMode.METADATA_ONLY), expected_sha256=SHA,
    budget=SourceAccessBudget(), route_pass=RoutePassSpec(expected=5,maximum=9),
    route_applicability=RoutePassApplicability.APPLICABLE))
try: be.execute()
except SourceAccessViolation as e: print(f"  {e.code}; _completed={be._completed} (expect 0)")
be.close()

print("\n===== D: injected module reaches the seam AND is consulted =====")
be=BoundSourceExecution(BoundExecutionSpec(source_entry_key="K", path=sav, source_format="SAV",
    plan=SourceOperationPlan(mode=RowDataMode.METADATA_ONLY), expected_sha256=SHA,
    budget=SourceAccessBudget(), route_pass=RoutePassSpec()), pyreadstat_module=Stub())
s=be._ensure_session()
print(f"  broker.pyreadstat is the supplied stub object? {s.broker.pyreadstat is Stub}")
print(f"  broker.pyreadstat is real pyreadstat? {s.broker.pyreadstat is pyreadstat}")
print(f"  broker.pyreadstat_version={getattr(s.broker,'pyreadstat_version',None)}")
be.close()

print("\n===== D2: is the stub actually CONSULTED (not just stored)? =====")
class Exploding:
    __version__="1.3.6"
    def read_sav(self,*a,**k): raise RuntimeError("STUB_CONSULTED")
    def read_dta(self,*a,**k): raise RuntimeError("STUB_CONSULTED")
be=BoundSourceExecution(BoundExecutionSpec(source_entry_key="K", path=sav, source_format="SAV",
    plan=SourceOperationPlan(mode=RowDataMode.METADATA_ONLY), expected_sha256=SHA,
    budget=SourceAccessBudget(), route_pass=RoutePassSpec()), pyreadstat_module=Exploding())
try:
    be.execute(); print("  stub not consulted (real reader used)")
except Exception as e:
    print(f"  {type(e).__name__}: {str(e)[:60]}  <- the supplied stub WAS consulted")
be.close()
