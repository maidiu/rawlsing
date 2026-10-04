import sys, os
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq197-r9-review")
import pyreadstat, pandas as pd
from rawlsing_next.pre553_source_access_broker import SourceAccessBroker, SourceAccessBudget
W="/tmp/hq197"
big=pd.DataFrame({f"C{i}":list(range(4000)) for i in range(6)})
sav=os.path.join(W,"big.sav"); dta=os.path.join(W,"big.dta")
pyreadstat.write_sav(big,sav); pyreadstat.write_dta(big,dta)
print("sav",os.path.getsize(sav),"dta",os.path.getsize(dta))
for label,path,kind in (("SAV",sav,"SAV"),("DTA",dta,"DTA")):
    print(f"\n=== {label}: selected_read(['C0']) vs full_read ===")
    for what in ("selected","full"):
        b=SourceAccessBroker(path, budget=SourceAccessBudget()); b.bind_reader(kind)
        if what=="selected":
            fr,md=b.selected_read(["C0"]); cols=list(fr.columns)
        else:
            fr,md=b.full_read(); cols=list(fr.columns)
        a=b.account_dict()
        print(f"  {what:9s} returned_cols={cols} read_calls={a['reader_read_calls']:6d} bytes={a['reader_bytes']:8d} reads_account={a.get('selected_reads' if what=='selected' else 'full_reads')}")
