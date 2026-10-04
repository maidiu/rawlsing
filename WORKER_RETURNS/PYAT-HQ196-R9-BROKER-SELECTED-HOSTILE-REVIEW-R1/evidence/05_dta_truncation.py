import os, io, sys, subprocess, pyreadstat, pandas as pd
WORK="/tmp/hq196"; os.makedirs(WORK,exist_ok=True)
dta=os.path.join(WORK,"trunc.dta")
pyreadstat.write_dta(pd.DataFrame({"A":list(range(500)),"B":list(range(500))}),dta)
class EOFBroker(io.BufferedReader):
    def __init__(self,p,cap):
        self._r=open(p,"rb"); super().__init__(self._r); self.reads=0; self.cap=cap
    def read(self,size=-1):
        self.reads+=1
        if self.reads>self.cap: return b""   # premature EOF
        return super().read(size)
for cap in (5,20,60):
    b=EOFBroker(dta,cap)
    try:
        d,m=pyreadstat.read_dta(b)
        print(f"DTA cap={cap}: RETURNED rows={len(d)} (metadata number_rows={m.number_rows}) reads={b.reads}  <-- {'SILENT TRUNCATION' if len(d)<m.number_rows else 'full'}")
    except Exception as e:
        print(f"DTA cap={cap}: {type(e).__name__}: {str(e)[:80]} (reads={b.reads})  <-- LOUD")
