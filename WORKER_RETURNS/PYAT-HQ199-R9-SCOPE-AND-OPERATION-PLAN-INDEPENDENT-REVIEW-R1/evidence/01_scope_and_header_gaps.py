import sys, os
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq198-r9-review")
# use the accepted repaired code, materialized read-only from git
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq198-r9-review")
import pyreadstat, pandas as pd
import rawlsing_next.pre553_physical_decoder as dec
W="/tmp/hq199"; os.makedirs(W, exist_ok=True)
sav=os.path.join(W,"s.sav")
if not os.path.exists(sav):
    pyreadstat.write_sav(pd.DataFrame({"A":list(range(200)),"B":list(range(200))}), sav)
print("carrier:", os.path.getsize(sav),"bytes")
print("module from:", dec.__file__)

print("\n=== G1: TWO independent _decode calls on the SAME source (no session owner) ===")
r=[]
for i in (1,2):
    inc=dec.decode_sav(sav); list(inc.iter_cells(50)); a=inc.source_access_receipt["accounts"]; inc.close_source_access()
    r.append(a)
    print(f"  decode #{i}: path_opens={a['path_opens']} hash_passes={a['hash_passes']} metadata_reads={a['metadata_reads']} "
          f"header_prefix_reads={a['header_prefix_reads']} chunk_reads={a['chunk_reads']}")
print(f"  AGGREGATE across two decodes: path_opens={r[0]['path_opens']+r[1]['path_opens']} "
      f"metadata_reads={r[0]['metadata_reads']+r[1]['metadata_reads']} hash_passes={r[0]['hash_passes']+r[1]['hash_passes']}")
print(f"  was the SECOND decode refused? NO — each _decode builds its own broker with its own budget")

print("\n=== G2: header-prefix read performed for a source whose class does not admit it ===")
inc=dec.decode_sav(sav); a=inc.source_access_receipt["accounts"]; inc.close_source_access()
print(f"  SAV header_prefix_reads={a['header_prefix_reads']} header_prefix_bytes={a['header_prefix_bytes']}")
print(f"  (SRC26 is the ONLY source with a frozen header-prefix operation; this carrier's class admits none)")

print("\n=== G3: compatibility/encoding route performs a FULL read ===")
inc=dec.decode_sav(sav, encoding="latin1"); list(inc.iter_cells(50)); a=inc.source_access_receipt["accounts"]; inc.close_source_access()
print(f"  encoding='latin1' (no selected set): full_reads={a['full_reads']} metadata_reads={a['metadata_reads']}")
print(f"  (SRC08/SRC12 are metadata-only with declared encodings: expected_metadata_reads=1, expected_full_reads=0)")

print("\n=== G4: decoder_invocations account exists? ===")
inc=dec.decode_sav(sav); a=inc.source_access_receipt["accounts"]; inc.close_source_access()
print(f"  account keys: {sorted(a.keys())}")
print(f"  'decoder_invocations' present? {'decoder_invocations' in a}")
print(f"  reader_invocations present? {'reader_invocations' in a} -> value semantics = compiled-reader calls, NOT decoder entries")
