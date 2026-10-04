import sys, os, io, json
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq197-r9-review")
import pyreadstat, pandas as pd
from rawlsing_next.pre553_source_access_broker import (
    SourceAccessBroker, SourceAccessBudget, SourceAccessViolation, GovernedSourceOpen)

W="/tmp/hq197"; os.makedirs(W, exist_ok=True)
df=pd.DataFrame({"A":list(range(500)),"B":list(range(500)),"C":list(range(500))})
sav=os.path.join(W,"synth.sav"); dta=os.path.join(W,"synth.dta")
pyreadstat.write_sav(df,sav); pyreadstat.write_dta(df,dta)
print("sav",os.path.getsize(sav),"dta",os.path.getsize(dta))

print("\n=== T1: reader_bytes cap declared but is it ENFORCED? ===")
# a cap so small ANY read exceeds it
b=SourceAccessBroker(sav, budget=SourceAccessBudget(reader_bytes=10))
try:
    b.bind_reader("SAV"); md=b.metadata_read()
    acct=b.account_dict()
    print(f"  metadata_read SUCCEEDED with reader_bytes cap=10")
    print(f"  bytes actually pulled through the governed view: {acct['reader_bytes']}")
    print(f"  reader_read_calls: {acct['reader_read_calls']}")
    if acct['reader_bytes'] > 10:
        print(f"  >>> ENFORCEMENT FAILURE: {acct['reader_bytes']} bytes consumed, cap was 10, NO violation raised")
    else:
        print("  cap respected")
except SourceAccessViolation as e:
    print(f"  SourceAccessViolation: {e.code}: {e}")
except Exception as e:
    print(f"  {type(e).__name__}: {e}")

print("\n=== T2: same cap, full read + selected read ===")
for label, fn in (("full_read", lambda bb: bb.full_read()),
                  ("selected_read(['A'])", lambda bb: bb.selected_read(["A"]))):
    b=SourceAccessBroker(sav, budget=SourceAccessBudget(reader_bytes=10)); b.bind_reader("SAV")
    try:
        fn(b); a=b.account_dict()
        verdict = "ENFORCEMENT FAILURE" if a['reader_bytes']>10 else "respected"
        print(f"  {label:24s} OK  bytes={a['reader_bytes']:6d} cap=10  -> {verdict}")
    except SourceAccessViolation as e:
        print(f"  {label:24s} RAISED {e.code}")
    except Exception as e:
        print(f"  {label:24s} {type(e).__name__}: {str(e)[:70]}")

print("\n=== T3: which caps DO fire (control) ===")
for kw,label in (({"path_opens":0},"path_opens=0"),({"metadata_reads":0},"metadata_reads=0"),
                 ({"reader_invocations":0},"reader_invocations=0")):
    b=SourceAccessBroker(sav, budget=SourceAccessBudget(**kw)); b.bind_reader("SAV")
    try:
        b.metadata_read(); print(f"  {label:22s} did NOT fire")
    except SourceAccessViolation as e:
        print(f"  {label:22s} FIRED {e.code}")

print("\n=== T4: one physical open across multiple logical parses ===")
b=SourceAccessBroker(sav, budget=SourceAccessBudget()); b.bind_reader("SAV")
b.metadata_read(); b.selected_read(["A"]); b.full_read()
a=b.account_dict()
print(f"  physical path_opens={a['path_opens']} logical_views={a['logical_views']} reads={a['reader_read_calls']} bytes={a['reader_bytes']}")
print(f"  ONE-OPEN ROUTE: {'CONFIRMED' if a['path_opens']==1 else 'FAILED'}")
