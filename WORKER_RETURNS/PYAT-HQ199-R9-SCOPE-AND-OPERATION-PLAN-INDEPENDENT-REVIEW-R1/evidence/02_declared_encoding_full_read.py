import sys, os
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq198-r9-review")
import pyreadstat, pandas as pd
import rawlsing_next.pre553_physical_decoder as dec
from rawlsing_next.pre553_source_access_broker import SourceAccessBudget
sav="/tmp/hq199/s.sav"
sha=dec._sha.__wrapped__(sav) if hasattr(dec._sha,"__wrapped__") else None
# put this carrier's own SHA into the allowlist to emulate a DECLARED-ENCODING LANE
import hashlib
h=hashlib.sha256(open(sav,"rb").read()).hexdigest()
dec.COMPATIBILITY_ALLOWLIST[h]="latin1"
print("carrier sha registered as a declared-encoding lane:", h[:16])
print("=== does the declared-encoding route perform a FULL read? ===")
inc=dec.decode_sav(sav, encoding="latin1"); list(inc.iter_cells(50))
a=inc.source_access_receipt["accounts"]; inc.close_source_access()
print(f"  metadata_reads={a['metadata_reads']} full_reads={a['full_reads']} selected_reads={a['selected_reads']} header_prefix_reads={a['header_prefix_reads']}")
print(f"  -> a declared-encoding source performs metadata + FULL read")
print()
print("=== with the frozen SRC08/SRC12 expectation (full_reads=0) declared, does it refuse? ===")
try:
    inc=dec.decode_sav(sav, encoding="latin1", source_access_budget=SourceAccessBudget(full_reads=0))
    list(inc.iter_cells(50)); print("  NO REFUSAL (BAD)")
except Exception as e:
    print(f"  {type(e).__name__}: {getattr(e,'code','')} {str(e)[:70]}")
