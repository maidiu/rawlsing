import sys, os, io
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq197-r9-review")
import pyreadstat, pandas as pd
from rawlsing_next.pre553_source_access_broker import SourceAccessBroker, SourceAccessBudget, GovernedSourceOpen
W="/tmp/hq197"
dta=os.path.join(W,"synth.dta"); sav=os.path.join(W,"synth.sav")

print("=== D1: candidate chunk route over ONE physical open (DTA and SAV) ===")
for label,path,kind in (("DTA",dta,"DTA"),("SAV",sav,"SAV")):
    b=SourceAccessBroker(path, budget=SourceAccessBudget()); b.bind_reader(kind)
    md=b.metadata_read()
    total=sum(len(f) for f in b.chunk_reads(chunk_rows=100, total_rows=int(md.number_rows)))
    a=b.account_dict()
    print(f"  {label}: rows={md.number_rows} chunk_rows_total={total} physical_opens={a['path_opens']} views={a['logical_views']} chunk_reads={a['chunk_reads']} bytes={a['reader_bytes']}")
    print(f"        {'CONFIRMED one-open chunk route' if a['path_opens']==1 and total==md.number_rows else 'MISMATCH'}")

print("\n=== D2: does read_file_in_chunks still fail over the governed view for DTA? (candidate avoided it) ===")
for label,path,kind,rf in (("DTA",dta,"DTA",pyreadstat.read_dta),("SAV",sav,"SAV",pyreadstat.read_sav)):
    b=SourceAccessBroker(path, budget=SourceAccessBudget()); b.bind_reader(kind)
    v=b._reader_arg()
    try:
        out=[len(c) for c,_ in pyreadstat.read_file_in_chunks(rf, v, chunksize=100)]
        print(f"  {label}: read_file_in_chunks over broker view -> {out}")
    except Exception as e:
        print(f"  {label}: read_file_in_chunks FAILS as HQ196 found -> {type(e).__name__}: {str(e)[:60]}")

print("\n=== D3: view() position-zero semantics ===")
o=GovernedSourceOpen(sav)
v1=o.view(); v1.read(50)
v2=o.view()   # new view must be at 0
print(f"  after v1.read(50): v2.tell()={v2.tell()} physical_opens={o.physical_opens} views={o.views_issued}")
print(f"  {'OK position-zero view over same open' if v2.tell()==0 and o.physical_opens==1 else 'FAILED'}")
o.close()
