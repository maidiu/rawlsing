import sys, os, functools
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq200-r9-session-review")
print = functools.partial(__builtins__.print, flush=True)
import pyreadstat, pandas as pd
from rawlsing_next.pre553_source_session import GovernedSourceSession, SourceOperationPlan, RowDataMode
from rawlsing_next.pre553_source_access_broker import SourceAccessBudget, SourceAccessViolation
W="/tmp/hq200"; sav=os.path.join(W,"s.sav")
def S(**kw): return GovernedSourceSession(source_entry_key="SRC-TEST", path=sav, source_format="SAV", **kw)

print("--- error path: budget breach mid-run, then continue? ---")
s=S(budget=SourceAccessBudget(reader_bytes=200, decoder_invocations=5))
try: s.run(SourceOperationPlan(mode=RowDataMode.FULL))
except SourceAccessViolation as e: print(f"  run failed: {e.code}")
a1=s.account_dict()
print(f"  after failure: decoder_invocations={a1['decoder_invocations']} metadata_reads={a1['metadata_reads']} full_reads={a1['full_reads']} reader_bytes={a1['reader_bytes']} closed={s.closed}")
# can a second run proceed on the same session after the failure?
try:
    s.run(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY)); a2=s.account_dict()
    print(f"  second run PROCEEDED: decoder_invocations={a2['decoder_invocations']} metadata_reads={a2['metadata_reads']}")
except SourceAccessViolation as e: print(f"  second run refused: {e.code}")

print("\n--- identity mismatch path ---")
s2=GovernedSourceSession(source_entry_key="K", path=sav, source_format="SAV", expected_source_sha256="0"*64)
try: s2.run(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY))
except SourceAccessViolation as e:
    a=s2.account_dict()
    print(f"  {e.code}; metadata_reads={a['metadata_reads']} (0 = refused before reader); hash_passes={a['hash_passes']}")
print("\n--- selection absent path: does it leave partial state? ---")
s3=S()
try: s3.run(SourceOperationPlan(mode=RowDataMode.SELECTED, selected_variables=("NOPE",)))
except SourceAccessViolation as e:
    a=s3.account_dict()
    print(f"  {e.code}; metadata_reads={a['metadata_reads']} selected_reads={a['selected_reads']} (row read not issued)")
