import sys, os, functools
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq200-r9-session-review")
print = functools.partial(__builtins__.print, flush=True)
import pyreadstat, pandas as pd
from rawlsing_next.pre553_source_session import GovernedSourceSession, SourceOperationPlan, RowDataMode, SessionPlanError
from rawlsing_next.pre553_source_access_broker import SourceAccessBudget, SourceAccessViolation
W="/tmp/hq200"; os.makedirs(W, exist_ok=True)
sav=os.path.join(W,"s.sav")
if not os.path.exists(sav):
    pyreadstat.write_sav(pd.DataFrame({"A":list(range(300)),"B":list(range(300)),"C":list(range(300))}), sav)
print("carrier:", sav, os.path.getsize(sav), "bytes")
def S(**kw): return GovernedSourceSession(source_entry_key="SRC-TEST", path=sav, source_format="SAV", **kw)

print("\n--- C1: one session owns ONE broker lifecycle ---")
s=S(); b1=s.broker; s.run(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY)); b2=s.broker
a=s.account_dict()
print(f"  same broker object: {b1 is b2}; path_opens={a['path_opens']} after two runs")

print("\n--- C2: decoder_invocations separate from reader_invocations ---")
s=S(); s.run(SourceOperationPlan(mode=RowDataMode.FULL)); a=s.account_dict()
print(f"  decoder_invocations={a['decoder_invocations']} reader_invocations={a['reader_invocations']} (metadata+full)")
print(f"  distinct keys both present: {'decoder_invocations' in a and 'reader_invocations' in a}")

print("\n--- C3+C4: max decoder_invocations=1 refuses 2nd entry BEFORE any source op; accounts unchanged ---")
s=S(budget=SourceAccessBudget(decoder_invocations=1))
s.run(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY))
before=dict(s.account_dict())
try:
    s.run(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY))
    print("  2nd entry NOT refused (BAD)")
except SourceAccessViolation as e:
    after=dict(s.account_dict())
    print(f"  2nd entry refused: {e.code}")
    changed={k:(before[k],after[k]) for k in before if before[k]!=after[k]}
    print(f"  accounts changed on refusal: {changed if changed else 'NONE (all unchanged)'}")

print("\n--- C5: METADATA_ONLY + non-null encoding => metadata only, no row data ---")
s=S(); s.run(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, encoding="latin1")); a=s.account_dict()
print(f"  metadata_reads={a['metadata_reads']} selected={a['selected_reads']} full={a['full_reads']} chunk={a['chunk_reads']}")

print("\n--- C6/7/8: SELECTED / FULL / CHUNKED_FULL account exactly their own mode ---")
for mode,kw in ((RowDataMode.SELECTED,{"selected_variables":("A",)}),
                (RowDataMode.FULL,{}),
                (RowDataMode.CHUNKED_FULL,{"chunk_rows":100})):
    s=S(); s.run(SourceOperationPlan(mode=mode, **kw)); a=s.account_dict()
    print(f"  {mode.value:13s} metadata={a['metadata_reads']} selected={a['selected_reads']} full={a['full_reads']} chunk={a['chunk_reads']}")

print("\n--- C9/C10: header_prefix_bytes None => zero; 176 => exactly one 176 ---")
s=S(); s.run(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY)); a=s.account_dict()
print(f"  None : header_prefix_reads={a['header_prefix_reads']} bytes={a['header_prefix_bytes']}")
s=S(); s.run(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY, header_prefix_bytes=176)); a=s.account_dict()
print(f"  176  : header_prefix_reads={a['header_prefix_reads']} bytes={a['header_prefix_bytes']}")

print("\n--- C11: session receipt LIVE after chunk activity ---")
s=S(); s.run(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY))
r_before=s.aggregate_receipt()["accounts"]["chunk_reads"]
s.run(SourceOperationPlan(mode=RowDataMode.CHUNKED_FULL, chunk_rows=50))
r_after=s.aggregate_receipt()["accounts"]["chunk_reads"]
print(f"  chunk_reads in receipt before={r_before} after={r_after} (live: {r_after>r_before})")

print("\n--- C12: close deterministic/idempotent (normal + error path) ---")
s=S(); s.close(); s.close(); print(f"  double close OK; closed={s.closed}")
try:
    s.run(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY)); print("  run after close NOT refused (BAD)")
except SourceAccessViolation as e: print(f"  run after close refused: {e.code}")
s2=S()
try: s2.run(SourceOperationPlan(mode=RowDataMode.SELECTED, selected_variables=("NOPE",)))
except Exception as e: print(f"  error path raised {type(e).__name__}; closed={s2.closed}")
s2.close(); s2.close(); print(f"  error-path close idempotent: closed={s2.closed}")
