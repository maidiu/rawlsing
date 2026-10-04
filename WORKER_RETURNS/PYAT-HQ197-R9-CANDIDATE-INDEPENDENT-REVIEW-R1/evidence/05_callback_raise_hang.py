import sys, os, io
sys.path.insert(0, "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq197-r9-review")
import pyreadstat
from rawlsing_next.pre553_source_access_broker import GovernedSourceOpen, _GovernedView
sav="/tmp/hq197/synth.sav"; dta="/tmp/hq197/synth.dta"

class RaisingView(_GovernedView):
    """Simulates an implementation that enforces a cap by RAISING in read()."""
    def __init__(self, owner, after):
        super().__init__(owner); self.n=0; self.after=after
    def read(self, size=-1):
        self.n+=1
        if self.n>self.after: raise RuntimeError("CEILING")
        return super().read(size)

print("=== H1: raising from the read callback (must return promptly or be rejected) ===")
for label,path,rf in (("SAV",sav,pyreadstat.read_sav),("DTA",dta,pyreadstat.read_dta)):
    o=GovernedSourceOpen(path)
    v=RaisingView(o, 3)
    try:
        rf(v); print(f"  {label}: returned normally (unexpected)")
    except Exception as e:
        print(f"  {label}: {type(e).__name__}: {str(e)[:70]}")
    o.close()
