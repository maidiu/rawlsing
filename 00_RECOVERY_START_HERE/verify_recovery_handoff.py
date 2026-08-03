#!/usr/bin/env python3
from pathlib import Path
import csv, hashlib, sys
root=Path(__file__).resolve().parents[1]
manifest=root/'SHA256SUMS.csv'
rows=list(csv.DictReader(manifest.open(encoding='utf-8')))
missing=[]; mismatched=[]
for row in rows:
 p=root/row['relative_path']
 if not p.is_file(): missing.append(row['relative_path']); continue
 h=hashlib.sha256(p.read_bytes()).hexdigest()
 if h!=row['sha256'] or p.stat().st_size!=int(row['size']): mismatched.append(row['relative_path'])
print({'manifest_rows':len(rows),'missing':len(missing),'mismatched':len(mismatched),'status':'PASS' if not missing and not mismatched else 'FAIL'})
sys.exit(0 if not missing and not mismatched else 1)
