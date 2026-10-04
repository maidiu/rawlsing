import sys, os
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq198-r9-review")
import rawlsing_next.pre553_physical_decoder as dec
from rawlsing_next.pre553_source_access_broker import SourceAccessViolation, SourceAccessBudget
sav="/tmp/hq198/six.sav"
try:
    inc=dec.decode_sav(sav,selected_variables=("A",),source_access_budget=SourceAccessBudget(reader_bytes=5000))
    list(inc.iter_cells(50)); print("survived cap=5000")
except SourceAccessViolation as e:
    print("code:", e.code)
    print("attributes:", [a for a in ("account","code","args") if hasattr(e,a)])
    print("args:", e.args[:2] if e.args else None)
except Exception as e:
    print("other:", type(e).__name__, str(e)[:60])
