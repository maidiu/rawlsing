import sys, os, functools, hashlib
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq202-r9-binding-final-review")
print = functools.partial(__builtins__.print, flush=True)
import pyreadstat
from rawlsing_next.pre553_execution_binding import BoundSourceExecution, BoundExecutionSpec, RoutePassSpec
from rawlsing_next.pre553_source_access_broker import SourceAccessBudget
from rawlsing_next.pre553_source_session import SourceOperationPlan, RowDataMode
sav="/tmp/hq202/s.sav"; SHA=hashlib.sha256(open(sav,"rb").read()).hexdigest()

class Consulted:
    """Seam-valid (version pinned, callables present) but poisoned: if consulted, it raises a sentinel."""
    __version__ = "1.3.6"
    def read_sav(self, *a, **k): raise RuntimeError("STUB_READ_SAV_CONSULTED")
    def read_dta(self, *a, **k): raise RuntimeError("STUB_READ_DTA_CONSULTED")

be=BoundSourceExecution(BoundExecutionSpec(source_entry_key="K", path=sav, source_format="SAV",
    plan=SourceOperationPlan(mode=RowDataMode.METADATA_ONLY), expected_sha256=SHA,
    budget=SourceAccessBudget(), route_pass=RoutePassSpec()), pyreadstat_module=Consulted())
s=be._ensure_session()
print(f"broker.pyreadstat is supplied object? {s.broker.pyreadstat is Consulted}")
print(f"broker.pyreadstat is real pyreadstat? {s.broker.pyreadstat is pyreadstat}")
try:
    be.execute(); print("NOT consulted (real reader used) -> parameter still ignored")
except Exception as e:
    print(f"{type(e).__name__}: {str(e)[:70]}  <- the SUPPLIED object was consulted")
be.close()
