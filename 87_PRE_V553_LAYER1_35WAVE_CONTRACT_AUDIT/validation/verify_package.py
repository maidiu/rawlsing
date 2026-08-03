#!/usr/bin/env python3
from __future__ import annotations
import csv,hashlib,json,sys
from pathlib import Path

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def main():
    root=Path(__file__).resolve().parents[1]
    manifest=root/'SHA256SUMS.csv'
    rows=list(csv.DictReader(manifest.open(encoding='utf-8')))
    missing=[]; mismatch=[]
    for r in rows:
        p=root/r['relative_path']
        if not p.exists(): missing.append(r['relative_path']); continue
        if sha(p)!=r['sha256']: mismatch.append(r['relative_path'])
    result={'status':'PASS' if not missing and not mismatch else 'FAIL','manifest_rows':len(rows),'missing':missing,'mismatched':mismatch}
    print(json.dumps(result,indent=2,sort_keys=True))
    return 0 if result['status']=='PASS' else 1
if __name__=='__main__': raise SystemExit(main())
