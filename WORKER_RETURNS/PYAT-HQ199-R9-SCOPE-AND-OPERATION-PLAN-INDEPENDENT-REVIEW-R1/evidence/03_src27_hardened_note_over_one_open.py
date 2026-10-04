import sys, os
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq198-r9-review")
import pyreadstat, pandas as pd
import rawlsing_next.pre553_physical_decoder as dec
from rawlsing_next.pre553_source_access_broker import SourceAccessBudget
W="/tmp/hq199"
# an SRC27-like DTA carrier: latin1 compatibility lane, full route pass
dta=os.path.join(W,"s.dta")
if not os.path.exists(dta):
    pyreadstat.write_dta(pd.DataFrame({"A":list(range(200)),"B":list(range(200))}), dta)
import hashlib
h=hashlib.sha256(open(dta,"rb").read()).hexdigest()
dec.COMPATIBILITY_ALLOWLIST[h]="latin1"
inc=dec.decode_dta(dta, encoding="latin1"); list(inc.iter_cells(50))
a=inc.source_access_receipt["accounts"]; inc.close_source_access()
print("=== SRC27-shaped run: hardened-note requirements vs observed ===")
req=[("existence/access check","existence_checks"),("full SHA-256 hash pass","hash_passes"),
     ("metadata read","metadata_reads"),("full compatibility read","full_reads")]
for label,k in req:
    print(f"  {label:26s}: {k}={a[k]}  {'PRESENT' if a[k]>=1 else 'MISSING'}")
print(f"  physical path_opens        : {a['path_opens']}   <- ONE open serves all four logical operations")
print(f"  header_prefix_reads        : {a['header_prefix_reads']} (DTA -> {a['header_prefix_bytes']} bytes, invented for this class)")
print(f"  chunk_reads                : {a['chunk_reads']}")
print(f"  reader_invocations         : {a['reader_invocations']}")
print(f"  decoder_invocations        : {'decoder_invocations' in a and a['decoder_invocations'] or 'ABSENT'}")
print()
print(f"  hardened-note minimum satisfied over ONE open? {all(a[k]>=1 for _,k in req) and a['path_opens']==1}")
