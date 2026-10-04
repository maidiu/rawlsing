import os, io, pyreadstat, pandas as pd
WORK="/tmp/hq196"; os.makedirs(WORK, exist_ok=True)
df = pd.DataFrame({"Q10B":[1,2,997], "AGE":[20,30,40], "SEX":[1,2,1]})
sav = os.path.join(WORK,"synth.sav"); pyreadstat.write_sav(df, sav)
print("synthetic SAV bytes:", os.path.getsize(sav))

class LoggingFile(io.BufferedReader):
    """Real file-like with full seek/tell/read semantics; logs every read/seek."""
    def __init__(self, path):
        self._raw = open(path, "rb")
        super().__init__(self._raw)
        self.calls=[]; self.bytes_read=0; self.source_path_used=path
    def read(self, size=-1):
        d = super().read(size)
        self.calls.append(("read", size, len(d))); self.bytes_read += len(d); return d
    def seek(self, pos, whence=0):
        r = super().seek(pos, whence); self.calls.append(("seek", pos, whence)); return r

print("\n=== A1: io.BytesIO-backed / BufferedReader broker ===")
b=LoggingFile(sav)
try:
    d2,m2 = pyreadstat.read_sav(b, usecols=["Q10B"])
    print("OK, cols:", list(d2.columns), "rows:", len(d2))
    print("read calls:", sum(1 for c in b.calls if c[0]=='read'),
          "| seek calls:", sum(1 for c in b.calls if c[0]=='seek'),
          "| bytes:", b.bytes_read, "| file size:", os.path.getsize(sav))
except Exception as e:
    print("FAILED:", type(e).__name__, str(e)[:200])

print("\n=== A2: bytes accounting, usecols vs full ===")
for label,kw in (("usecols=['Q10B']",{"usecols":["Q10B"]}),
                 ("usecols=['Q10B','AGE']",{"usecols":["Q10B","AGE"]}),
                 ("full (no usecols)",{})):
    bb=LoggingFile(sav)
    try:
        dd,mm=pyreadstat.read_sav(bb, **kw)
        print(f"  {label:24s} read_calls={sum(1 for c in bb.calls if c[0]=='read'):4d} bytes={bb.bytes_read:6d} cols={len(dd.columns)}")
    except Exception as e:
        print(f"  {label:24s} FAILED {type(e).__name__} {str(e)[:80]}")

print("\n=== A3: pure io.BytesIO (no fd at all) ===")
try:
    bio = io.BytesIO(open(sav,"rb").read())
    d3,m3 = pyreadstat.read_sav(bio, usecols=["Q10B"])
    print("BytesIO OK, cols:", list(d3.columns))
except Exception as e:
    print("BytesIO FAILED:", type(e).__name__, str(e)[:200])

print("\n=== A4: metadataonly + usecols on broker ===")
for kw in ({"metadataonly":True},{"usecols":["Q10B"],"row_limit":1},{"row_offset":1,"row_limit":1}):
    bb=LoggingFile(sav)
    try:
        dd,mm=pyreadstat.read_sav(bb,**kw)
        print(f"  {kw}: OK rows={len(dd)} bytes={bb.bytes_read}")
    except Exception as e:
        print(f"  {kw}: FAILED {type(e).__name__} {str(e)[:80]}")
