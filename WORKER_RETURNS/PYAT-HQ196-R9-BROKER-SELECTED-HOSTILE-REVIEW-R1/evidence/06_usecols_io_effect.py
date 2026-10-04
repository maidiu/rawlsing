import os, io, pyreadstat, pandas as pd
WORK="/tmp/hq196"
# larger synthetic DTA so I/O differences are visible
n=4000
df=pd.DataFrame({"Q10B":list(range(n)),"AGE":list(range(n)),"SEX":[i%2 for i in range(n)],"X4":[i*2 for i in range(n)],"X5":[i*3 for i in range(n)]})
dta=os.path.join(WORK,"big.dta"); sav=os.path.join(WORK,"big.sav")
pyreadstat.write_dta(df,dta); pyreadstat.write_sav(df,sav)
print("dta",os.path.getsize(dta),"sav",os.path.getsize(sav))
class LF(io.BufferedReader):
    def __init__(self,p):
        self._r=open(p,"rb"); super().__init__(self._r); self.reads=0; self.b=0
    def read(self,s=-1):
        d=super().read(s); self.reads+=1; self.b+=len(d); return d
for label,path,fn in (("DTA",dta,pyreadstat.read_dta),("SAV",sav,pyreadstat.read_sav)):
    print(f"\n=== {label} usecols effect on OBSERVED I/O ===")
    for kw in ({}, {"usecols":["Q10B"]}, {"usecols":["Q10B","AGE"]}):
        f=LF(path)
        d,m=fn(f, **kw)
        print(f"  {str(kw):34s} cols={len(d.columns):2d} reads={f.reads:5d} bytes={f.b:8d}")
