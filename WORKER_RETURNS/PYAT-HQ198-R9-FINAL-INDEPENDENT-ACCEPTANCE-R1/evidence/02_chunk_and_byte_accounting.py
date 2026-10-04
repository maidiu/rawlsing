import sys, os
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq198-r9-review")
import pyreadstat, pandas as pd
from rawlsing_next.pre553_source_access_broker import SourceAccessBroker, SourceAccessBudget
W="/tmp/hq198"; os.makedirs(W,exist_ok=True)
big=os.path.join(W,"rows1000.sav")
if not os.path.exists(big):
    pyreadstat.write_sav(pd.DataFrame({"a":list(range(1000))}), big)
print("carrier:", big, os.path.getsize(big), "bytes, 1000 rows")

print("\n=== chunk_rows honoured on a carrier larger than one chunk ===")
for cr in (7, 100, 333):
    b=SourceAccessBroker(big, budget=SourceAccessBudget()); b.bind_reader("SAV")
    md=b.metadata_read()
    sizes=[len(x) for x in b.chunk_reads(chunk_rows=cr, total_rows=int(md.number_rows))]
    a=b.account_dict()
    print(f"  chunk_rows={cr:4d} -> n={len(sizes):4d} max={max(sizes):4d} total={sum(sizes):5d} "
          f"all<={cr}? {all(s<=cr for s in sizes)}  chunk_reads={a['chunk_reads']} path_opens={a['path_opens']}")

print("\n=== reader_bytes EXCLUDES application hash/header traffic ===")
b=SourceAccessBroker(big, budget=SourceAccessBudget()); b.bind_reader("SAV")
b.existence_check()
sha=b.hash_pass()                 # application hash: whole file
pfx=b.header_prefix(176)          # application header read
b.metadata_read()                 # compiled reader
a=b.account_dict()
print(f"  file size            : {os.path.getsize(big)}")
print(f"  hash_bytes account   : {a['hash_bytes']}")
print(f"  header_prefix_bytes  : {a['header_prefix_bytes']}")
print(f"  reader_bytes account : {a['reader_bytes']}")
print(f"  total via governed open: {b._open.bytes_read}")
print(f"  reader_bytes < total? {a['reader_bytes'] < b._open.bytes_read}  (excluded {b._open.bytes_read - a['reader_bytes']} app bytes)")
print(f"  reader_bytes == total - hash - header? {a['reader_bytes'] == b._open.bytes_read - a['hash_bytes'] - a['header_prefix_bytes']}")
