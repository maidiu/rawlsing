import sys, os
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq198-r9-review")
import pyreadstat, pandas as pd
import rawlsing_next.pre553_physical_decoder as dec
W="/tmp/hq198"; sav=os.path.join(W,"six.sav")
def run(**kw):
    inc=dec.decode_sav(sav,**kw); cells=list(inc.iter_cells(50)); r=inc.source_access_receipt; inc.close_source_access(); return r,cells
r1,c1=run(selected_variables=("A",)); a1=r1["accounts"]
print("D1 SELECTED: selected_reads=%s full_reads=%s path_opens=%s reader_bytes=%s cols=%s"%(
    a1['selected_reads'],a1['full_reads'],a1['path_opens'],a1['reader_bytes'],sorted({c.variable_name for c in c1})))
r2,c2=run(); a2=r2["accounts"]
print("D2 FULL    : selected_reads=%s full_reads=%s reader_bytes=%s"%(a2['selected_reads'],a2['full_reads'],a2['reader_bytes']))
print("D2 non-suppression: selected bytes == full bytes ? %s"%(a1['reader_bytes']==a2['reader_bytes']))
print("D2 disclosure field:", str(r1.get("selected_route_physical_column_suppression"))[:60])
try:
    run(selected_variables=("NOPE",)); print("D3 absent-variable: NO FAILURE (BAD)")
except Exception as e:
    print("D3 absent-variable: %s: %s"%(type(e).__name__,str(e)[:60]))
