import sys, os
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq197-r9-review")
import pyreadstat, pandas as pd
from rawlsing_next.pre553_source_access_broker import SourceAccessBroker, SourceAccessBudget
W="/tmp/hq197"
f=os.path.join(W,"rows1000.sav")
pyreadstat.write_sav(pd.DataFrame({"a":list(range(1000))}), f)
b=SourceAccessBroker(f, budget=SourceAccessBudget()); b.bind_reader("SAV")
md=b.metadata_read()
for cr in (7, 100):
    b2=SourceAccessBroker(f, budget=SourceAccessBudget()); b2.bind_reader("SAV"); b2.metadata_read()
    sizes=[len(x) for x in b2.chunk_reads(chunk_rows=cr, total_rows=int(md.number_rows))]
    print(f"  chunk_rows={cr:4d} -> chunk sizes {sizes[:6]}{'...' if len(sizes)>6 else ''} n_chunks={len(sizes)} total={sum(sizes)}")
    print(f"     bounded to chunk_rows? {'YES' if all(s<=cr for s in sizes) else 'NO'}")
