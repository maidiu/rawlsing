import os, io, pyreadstat, pandas as pd
WORK="/tmp/hq196"; os.makedirs(WORK, exist_ok=True)

# synthetic DTA + SAV
df = pd.DataFrame({"Q10B":[1,2,3,4,5,6], "AGE":[20,21,22,23,24,25], "SEX":[1,2,1,2,1,2]})
dta=os.path.join(WORK,"synth.dta"); sav=os.path.join(WORK,"synth2.sav")
pyreadstat.write_dta(df, dta); pyreadstat.write_sav(df, sav)
print("dta bytes:",os.path.getsize(dta),"sav bytes:",os.path.getsize(sav))

class LoggingFile(io.BufferedReader):
    def __init__(self,path):
        self._raw=open(path,"rb"); super().__init__(self._raw)
        self.calls=[]; self.bytes_read=0; self.reads=0; self.seeks=0
    def read(self,size=-1):
        d=super().read(size); self.reads+=1; self.bytes_read+=len(d); return d
    def seek(self,pos,whence=0):
        self.seeks+=1; return super().seek(pos,whence)

def run(label, fn):
    try:
        r=fn(); print(f"  [OK]   {label}: {r}")
    except Exception as e:
        print(f"  [FAIL] {label}: {type(e).__name__}: {str(e)[:150]}")

print("\n=== D1: DTA via broker (plain) ===")
b=LoggingFile(dta)
run("read_dta(broker)", lambda: (list(pyreadstat.read_dta(b)[0].columns), f"reads={b.reads} bytes={b.bytes_read}"))

print("\n=== D2: DTA chunked via broker? (read_file_in_chunks expects a path) ===")
b2=LoggingFile(dta)
def chunked_broker():
    out=[]
    for chunk,meta in pyreadstat.read_file_in_chunks(pyreadstat.read_dta, b2, chunksize=2):
        out.append(len(chunk))
    return out
run("read_file_in_chunks(read_dta, broker)", chunked_broker)

print("\n=== D3: DTA/Sav chunked via PATH (baseline) ===")
run("chunks(dta,path)", lambda: [len(c) for c,_ in pyreadstat.read_file_in_chunks(pyreadstat.read_dta, dta, chunksize=2)])
run("chunks(sav,path)", lambda: [len(c) for c,_ in pyreadstat.read_file_in_chunks(pyreadstat.read_sav, sav, chunksize=2)])

print("\n=== D4: does read_file_in_chunks forward usecols? ===")
run("chunks(sav,path,usecols=['Q10B'])",
    lambda: [(list(c.columns),len(c)) for c,_ in pyreadstat.read_file_in_chunks(pyreadstat.read_sav, sav, chunksize=3, usecols=["Q10B"])])
run("chunks(sav,path,usecols=['AGE'])",
    lambda: [(list(c.columns),len(c)) for c,_ in pyreadstat.read_file_in_chunks(pyreadstat.read_sav, sav, chunksize=3, usecols=["AGE"])])

print("\n=== D5: fresh broker per chunk (reset semantics) ===")
def fresh_per_chunk():
    out=[]
    for off in (0,2,4):
        bb=LoggingFile(dta)
        d,m=pyreadstat.read_dta(bb, row_offset=off, row_limit=2)
        out.append((off,len(d),bb.reads,bb.bytes_read))
    return out
run("fresh broker + row_offset", fresh_per_chunk)

print("\n=== D6: REUSED broker across calls (position/reset hazard) ===")
reused=LoggingFile(dta)
def reused_broker():
    d1,_=pyreadstat.read_dta(reused, row_offset=0, row_limit=2)
    d2,_=pyreadstat.read_dta(reused, row_offset=2, row_limit=2)
    return [len(d1),len(d2)]
run("reused broker twice", reused_broker)

print("\n=== D7: broker position after a read (does ReadStat restore it?) ===")
b7=LoggingFile(dta)
pyreadstat.read_dta(b7, row_limit=2)
run("tell() after read_dta", lambda: (b7.tell(), os.path.getsize(dta)))
