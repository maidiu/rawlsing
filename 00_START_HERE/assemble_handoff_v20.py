#!/usr/bin/env python3
from __future__ import annotations
import csv, hashlib, shutil, sys
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
def clean(root):
 for p in sorted(root.rglob('*'),reverse=True):
  if p.is_dir() and p.name in {'__pycache__','.pytest_cache'}: shutil.rmtree(p)
  elif p.is_file() and p.suffix in {'.pyc','.pyo'}: p.unlink()
def section_manifest(sec):
 p=sec/'SECTION_MANIFEST.csv'
 final_gate=sec/'FINAL_RELEASE_GATE_RETURN.json'
 if p.exists(): p.unlink()
 rec=[]
 for x in sorted(y for y in sec.rglob('*') if y.is_file() and y not in (p,final_gate)): rec.append({'relative_path':x.relative_to(sec).as_posix(),'bytes':x.stat().st_size,'sha256':sha(x)})
 with p.open('w',encoding='utf-8',newline='') as f: w=csv.DictWriter(f,fieldnames=['relative_path','bytes','sha256']); w.writeheader(); w.writerows(rec)
def manifests(root):
 idx=root/'PACKAGE_INDEX.csv'; sums=root/'SHA256SUMS.csv'; final_gate=root/'42_P2_GLOBAL_CROSS_TRANCHE_CLOSURE'/'FINAL_RELEASE_GATE_RETURN.json'
 for p in (idx,sums):
  if p.exists(): p.unlink()
 rec=[]
 for x in sorted(y for y in root.rglob('*') if y.is_file() and y not in (idx,sums,final_gate)): rec.append({'relative_path':x.relative_to(root).as_posix(),'bytes':x.stat().st_size,'sha256':sha(x)})
 for p in (idx,sums):
  with p.open('w',encoding='utf-8',newline='') as f: w=csv.DictWriter(f,fieldnames=['relative_path','bytes','sha256']); w.writeheader(); w.writerows(rec)
if __name__=='__main__':
 clean(ROOT)
 for section in ['41_P2_GLOBAL_FINAL_2847_PAIR_TRANCHE8','42_P2_GLOBAL_CROSS_TRANCHE_CLOSURE']: section_manifest(ROOT/section)
 manifests(ROOT)
 print(ROOT)
