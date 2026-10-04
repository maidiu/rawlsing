import os, io, pyreadstat, pandas as pd
WORK="/tmp/hq196"
dta=os.path.join(WORK,"trunc.dta")   # 500 rows
class LF(io.BufferedReader):
    def __init__(self,p):
        self._r=open(p,"rb"); super().__init__(self._r); self.reads=0; self.b=0
    def read(self,s=-1):
        d=super().read(s); self.reads+=1; self.b+=len(d); return d

print("=== pattern: fresh broker per read call, replaying read_file_in_chunks manually ===")
sizes=[]; total_reads=0; total_bytes=0
for off in (0,200,400):
    b=LF(dta)
    d,m=pyreadstat.read_dta(b,row_offset=off,row_limit=200)
    sizes.append((off,len(d))); total_reads+=b.reads; total_bytes+=b.b
print("  chunks:",sizes)
print(f"  aggregate broker accounting: reads={total_reads} bytes={total_bytes}")

print("\n=== does benchmark row_limit reduce OBSERVED bytes? (i.e. is row_limit post-read too) ===")
for kw in ({}, {"row_limit":10}, {"row_offset":450,"row_limit":10}):
    b=LF(dta); d,m=pyreadstat.read_dta(b,**kw)
    print(f"  {str(kw):34s} rows={len(d):4d} reads={b.reads:5d} bytes={b.b:8d}")

print("\n=== position after a read (reuse hazard) ===")
b=LF(dta); pyreadstat.read_dta(b,row_limit=10)
print("  tell() =",b.tell(),"of",os.path.getsize(dta))
try:
    pyreadstat.read_dta(b,row_limit=10); print("  second call on SAME broker: OK")
except Exception as e:
    print(f"  second call on SAME broker: {type(e).__name__}: {str(e)[:70]}  <-- reuse is unsafe")
