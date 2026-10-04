import sys, os, functools, hashlib
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq202-r9-binding-final-review")
print = functools.partial(__builtins__.print, flush=True)
import pyreadstat, pandas as pd
from rawlsing_next.pre553_execution_binding import (BoundSourceExecution, BoundExecutionSpec, RoutePassSpec,
    RoutePassApplicability, AccountConstraint, CountKind, AuthorityLabel)
from rawlsing_next.pre553_source_access_broker import SourceAccessBudget, SourceAccessViolation
from rawlsing_next.pre553_source_session import SourceOperationPlan, RowDataMode
W="/tmp/hq202"; os.makedirs(W,exist_ok=True)
sav=os.path.join(W,"w.sav")
if not os.path.exists(sav): pyreadstat.write_sav(pd.DataFrame({c:list(range(200)) for c in "ABC"}), sav)
dta=os.path.join(W,"w.dta")
if not os.path.exists(dta): pyreadstat.write_dta(pd.DataFrame({"A":list(range(200))}), dta)
sh=lambda p: hashlib.sha256(open(p,"rb").read()).hexdigest()
print("===== six non-route plan shapes with outer EXACT 0 =====")
shapes=[("SRC02 SELECTED Q10B",sav,"SAV",SourceOperationPlan(mode=RowDataMode.SELECTED,selected_variables=("A",))),
        ("SRC06 SELECTED Q101,Q2061B",sav,"SAV",SourceOperationPlan(mode=RowDataMode.SELECTED,selected_variables=("A","B"))),
        ("SRC08 METADATA BIG5",sav,"SAV",SourceOperationPlan(mode=RowDataMode.METADATA_ONLY,encoding="big5")),
        ("SRC12 METADATA WIN1252",sav,"SAV",SourceOperationPlan(mode=RowDataMode.METADATA_ONLY,encoding="cp1252")),
        ("SRC14 SELECTED v372",sav,"SAV",SourceOperationPlan(mode=RowDataMode.SELECTED,selected_variables=("C",))),
        ("SRC26 METADATA + 176 prefix",sav,"SAV",SourceOperationPlan(mode=RowDataMode.METADATA_ONLY,header_prefix_bytes=176))]
for label,p,fmt,plan in shapes:
    be=BoundSourceExecution(BoundExecutionSpec(source_entry_key=label, path=p, source_format=fmt,
        plan=plan, expected_sha256=sh(p), budget=SourceAccessBudget(retries=0),
        route_pass=RoutePassSpec(expected=0, maximum=0), route_applicability=RoutePassApplicability.NOT_APPLICABLE))
    o=be.execute()
    a=o.observed_accounts
    print(f"  {label:30s} observed={o.full_route_passes_observed} status={o.route_pass_status:15s} meta={a['metadata_reads']} sel={a['selected_reads']} full={a['full_reads']} prefix={a['header_prefix_reads']}")
    be.close()

print("\n===== SRC27-shaped route exact/max 1 executes ONCE, then refuses =====")
be=BoundSourceExecution(BoundExecutionSpec(source_entry_key="SRC27", path=dta, source_format="DTA",
    plan=SourceOperationPlan(mode=RowDataMode.FULL, encoding="latin1"), expected_sha256=sh(dta),
    budget=SourceAccessBudget(retries=0), route_pass=RoutePassSpec(expected=1, maximum=1),
    route_applicability=RoutePassApplicability.APPLICABLE,
    constraints=(AccountConstraint("full_reads", CountKind.FLOOR, 1, AuthorityLabel.FROZEN_AUTHORITY),)))
o=be.execute()
a=o.observed_accounts
print(f"  pass1: observed={o.full_route_passes_observed} completed={o.completed_route_passes} full_reads={a['full_reads']} chunk={a['chunk_reads']} prefix={a['header_prefix_reads']}")
print(f"  full_reads floor1 satisfied by full_reads (not chunk): {a['full_reads']>=1 and a['chunk_reads']==0}")
try:
    be.execute(); print("  pass2 RAN (BAD)")
except SourceAccessViolation as e: print(f"  pass2 REFUSED pre-op: {e.code}")
be.close()

print("\n===== chunk_reads cannot satisfy the full_reads floor =====")
be=BoundSourceExecution(BoundExecutionSpec(source_entry_key="CHK", path=sav, source_format="SAV",
    plan=SourceOperationPlan(mode=RowDataMode.CHUNKED_FULL, chunk_rows=50), expected_sha256=sh(sav),
    budget=SourceAccessBudget(retries=0), route_pass=RoutePassSpec(expected=0,maximum=0),
    route_applicability=RoutePassApplicability.NOT_APPLICABLE,
    constraints=(AccountConstraint("full_reads", CountKind.FLOOR, 1, AuthorityLabel.FROZEN_AUTHORITY),)))
try:
    be.execute(); print("  chunk satisfied the full_reads floor (BAD)")
except SourceAccessViolation as e: print(f"  refused: {e.code} -> chunk_reads did NOT satisfy the full_reads floor")
be.close()
