from pathlib import Path
import csv,hashlib,sys
root=Path(__file__).resolve().parent
missing=[]; mismatched=[]; checked=0
with (root/"MULTIPART_SHA256SUMS.csv").open(newline="",encoding="utf-8") as f:
    for row in csv.DictReader(f):
        p=root/row["path"]
        if not p.is_file(): missing.append(row["path"]); continue
        h=hashlib.sha256()
        with p.open("rb") as fh:
            for block in iter(lambda:fh.read(1024*1024),b""): h.update(block)
        if p.stat().st_size!=int(row["size_bytes"]) or h.hexdigest()!=row["sha256"]: mismatched.append(row["path"])
        checked+=1
print(f"checked={checked} missing={len(missing)} mismatched={len(mismatched)}")
if missing: print("MISSING",*missing[:20],sep="\n")
if mismatched: print("MISMATCHED",*mismatched[:20],sep="\n")
sys.exit(1 if missing or mismatched else 0)
