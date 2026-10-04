import sys, os, functools
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq200-r9-session-review")
print = functools.partial(__builtins__.print, flush=True)
import pyreadstat, pandas as pd
from rawlsing_next.pre553_source_session import GovernedSourceSession, SourceOperationPlan, RowDataMode
from rawlsing_next.pre553_source_access_broker import SourceAccessBudget, SourceAccessViolation
W="/tmp/hq200"; sav=os.path.join(W,"s.sav")
def S(**kw): return GovernedSourceSession(source_entry_key="SRC-TEST", path=sav, source_format="SAV", **kw)

print("--- C13: no SRCxx policy hard-coded in production ---")
import subprocess
for f in ("pre553_source_session.py","pre553_physical_decoder.py","pre553_source_access_broker.py"):
    p=f"/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq200-r9-session-review/rawlsing_next/{f}"
    hits=[l.strip() for l in open(p) if "SRC" in l and "SRCxx" not in l and "SRC02" not in l and "SRC06" not in l and "SRC14" not in l and "SRC27" not in l]
    src=[l.strip() for l in open(p) if any(t in l for t in ("SRC02","SRC06","SRC08","SRC12","SRC14","SRC26","SRC27","SRC35"))]
    code=[l for l in src if not l.lstrip().startswith("#")]
    print(f"  {f}: SRCxx in non-comment code = {len(code)} {'(none)' if not code else code[:2]}")

print("\n--- C14: no raw source path reaches pyreadstat ---")
s=S(); s.run(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY))
v=s.broker._reader_arg()
print(f"  reader arg type: {type(v).__name__} (not str/bytes/PathLike: {not isinstance(v,(str,bytes,os.PathLike))})")
print(f"  broker guard present: {hasattr(s.broker,'_reader_arg')}")

print("\n--- C15: accepted reader_bytes limiter intact ---")
s=S(budget=SourceAccessBudget(reader_bytes=200))
try:
    s.run(SourceOperationPlan(mode=RowDataMode.FULL)); print("  cap=200 survived (BAD)")
except SourceAccessViolation as e:
    a=s.account_dict(); print(f"  cap=200 refused: {e.code}; reader_bytes consumed={a['reader_bytes']} <=200? {a['reader_bytes']<=200}")
s=S(budget=SourceAccessBudget(reader_bytes=200000))
s.run(SourceOperationPlan(mode=RowDataMode.FULL)); a=s.account_dict()
print(f"  generous cap: succeeded, reader_bytes={a['reader_bytes']}")

print("\n--- plan validation (python guardrails) ---")
for label,kw in (("SELECTED without names",{"mode":RowDataMode.SELECTED}),
                 ("CHUNKED_FULL without chunk_rows",{"mode":RowDataMode.CHUNKED_FULL}),
                 ("selected_variables on FULL",{"mode":RowDataMode.FULL,"selected_variables":("A",)})):
    try: SourceOperationPlan(**kw); print(f"  {label}: ACCEPTED (BAD)")
    except Exception as e: print(f"  {label}: refused {type(e).__name__}")

print("\n--- generic owner: multiple plan runs WITHOUT a ceiling (allowed?) ---")
s=S(); 
for i in (1,2,3): s.run(SourceOperationPlan(mode=RowDataMode.METADATA_ONLY))
a=s.account_dict()
print(f"  three runs: decoder_invocations={a['decoder_invocations']} metadata_reads={a['metadata_reads']} path_opens={a['path_opens']}")
print("  -> generic owner permits multiple plan runs when no ceiling is supplied (bound layer must supply the cap)")
