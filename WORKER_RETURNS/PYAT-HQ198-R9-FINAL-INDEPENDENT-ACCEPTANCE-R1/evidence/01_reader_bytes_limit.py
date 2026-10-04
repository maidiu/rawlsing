import sys, os, io
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq198-r9-review")
import pyreadstat, pandas as pd
from rawlsing_next.pre553_source_access_broker import SourceAccessBroker, SourceAccessBudget, SourceAccessViolation
W="/tmp/hq198"; os.makedirs(W,exist_ok=True)
sav=os.path.join(W,"synth.sav")
if not os.path.exists(sav) or os.path.getsize(sav)<5000:
    pyreadstat.write_sav(pd.DataFrame({f"C{i}":list(range(500)) for i in range(4)}), sav)
print("carrier:", sav, os.path.getsize(sav), "bytes")

def measure(path, kind, op):
    """Return bytes pulled by the compiled reader for op under an unbounded budget."""
    b=SourceAccessBroker(path, budget=SourceAccessBudget()); b.bind_reader(kind)
    if op=="metadata": b.metadata_read()
    elif op=="full": b.full_read()
    elif op=="selected": b.selected_read(["C0"])
    return b.account_dict()["reader_bytes"]

print("\n=== T1: how many reader bytes does each op need? (unbounded) ===")
need={}
for op in ("metadata","full","selected"):
    need[op]=measure(sav,"SAV",op)
    print(f"  {op:9s} reader_bytes = {need[op]}")

print("\n=== T2: EXACTLY ENOUGH succeeds ===")
for op in ("metadata","full","selected"):
    b=SourceAccessBroker(sav, budget=SourceAccessBudget(reader_bytes=need[op])); b.bind_reader("SAV")
    try:
        if op=="metadata": b.metadata_read()
        elif op=="full": b.full_read()
        else: b.selected_read(["C0"])
        a=b.account_dict()
        ok = a["reader_bytes"] <= need[op]
        print(f"  {op:9s} cap={need[op]:6d} -> SUCCESS, consumed={a['reader_bytes']:6d}  {'OK' if ok else 'OVER CAP'}")
    except Exception as e:
        print(f"  {op:9s} cap={need[op]:6d} -> {type(e).__name__}: {str(e)[:70]}  <-- UNEXPECTED")

print("\n=== T3: ONE BYTE SHORT fails, prompt + typed ===")
import time
for op in ("metadata","full","selected"):
    cap=need[op]-1
    b=SourceAccessBroker(sav, budget=SourceAccessBudget(reader_bytes=cap)); b.bind_reader("SAV")
    t0=time.time()
    try:
        if op=="metadata": b.metadata_read()
        elif op=="full": b.full_read()
        else: b.selected_read(["C0"])
        print(f"  {op:9s} cap={cap:6d} -> NO FAILURE (BAD)")
    except SourceAccessViolation as e:
        a=b.account_dict()
        print(f"  {op:9s} cap={cap:6d} -> {e.code} in {time.time()-t0:.3f}s; consumed={a['reader_bytes']} <= cap? {a['reader_bytes']<=cap}")
    except Exception as e:
        print(f"  {op:9s} cap={cap:6d} -> {type(e).__name__} (NOT typed SourceAccessViolation): {str(e)[:60]}")

print("\n=== T4: far-too-small cap never over-consumes ===")
for cap in (0,1,10):
    b=SourceAccessBroker(sav, budget=SourceAccessBudget(reader_bytes=cap)); b.bind_reader("SAV")
    try: b.full_read(); print(f"  cap={cap}: NO FAILURE (BAD)")
    except SourceAccessViolation as e:
        a=b.account_dict(); print(f"  cap={cap:3d} -> {e.code}; consumed={a['reader_bytes']} <= cap? {a['reader_bytes']<=cap}")
    except Exception as e:
        print(f"  cap={cap}: {type(e).__name__} {str(e)[:50]}")
