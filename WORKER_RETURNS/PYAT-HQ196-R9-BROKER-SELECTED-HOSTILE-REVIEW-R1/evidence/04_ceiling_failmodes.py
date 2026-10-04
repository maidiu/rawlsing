import os, io, sys
mode=sys.argv[1]
cap=int(sys.argv[2]) if len(sys.argv)>2 else 5
import pyreadstat, pandas as pd
WORK="/tmp/hq196"; os.makedirs(WORK,exist_ok=True)
sav=os.path.join(WORK,"ceil.sav")
if not os.path.exists(sav):
    pyreadstat.write_sav(pd.DataFrame({"A":list(range(500)),"B":list(range(500))}),sav)

class Base(io.BufferedReader):
    def __init__(self,p):
        self._r=open(p,"rb"); super().__init__(self._r); self.reads=0
    def _log(self): self.reads+=1

if mode=="raise":
    class B(Base):
        def read(self,size=-1):
            self._log()
            if self.reads>cap: raise RuntimeError("CEILING")
            return super().read(size)
elif mode=="eof":
    class B(Base):
        def read(self,size=-1):
            self._log()
            if self.reads>cap: return b""      # pretend EOF
            return super().read(size)
elif mode=="short":
    class B(Base):
        def read(self,size=-1):
            self._log()
            if self.reads>cap: return b""      # same as eof
            return super().read(size)
b=B(sav)
try:
    d,m=pyreadstat.read_sav(b)
    print(f"MODE={mode} cap={cap}: RETURNED rows={len(d)} cols={list(d.columns)} reads={b.reads}  <-- SILENT/TRUNCATED SUCCESS")
except Exception as e:
    print(f"MODE={mode} cap={cap}: {type(e).__name__}: {str(e)[:90]} (reads={b.reads})  <-- LOUD FAILURE")
