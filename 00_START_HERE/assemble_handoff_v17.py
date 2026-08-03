#!/usr/bin/env python3
"""Path-specific finalizer used for Rawlsing cumulative handoff v17.

The semantic authority surfaces are rebuilt by section 38's delivered builder and
frozen selection. This finalizer removes generated test debris and regenerates
full-coverage top-level manifests for an already assembled cumulative tree.
"""
from __future__ import annotations
import csv, hashlib, shutil, sys
from pathlib import Path
sys.dont_write_bytecode = True
ROOT=Path('/mnt/data/rawlsing_v17_build/Rawlsing_J_Family_Authority_Strategy_Handoff_v17_20260731')

def sha(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()

def remove_caches(root: Path) -> None:
    for p in sorted(root.rglob('*'),reverse=True):
        if p.is_dir() and p.name in {'__pycache__','.pytest_cache'}: shutil.rmtree(p)
        elif p.is_file() and p.suffix in {'.pyc','.pyo'}: p.unlink()

def manifests(root: Path) -> None:
    idx=root/'PACKAGE_INDEX.csv'; sums=root/'SHA256SUMS.csv'
    for p in (idx,sums):
        if p.exists(): p.unlink()
    records=[]
    for p in sorted(x for x in root.rglob('*') if x.is_file()):
        records.append({'relative_path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)})
    for p in (idx,sums):
        with p.open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=['relative_path','bytes','sha256']); w.writeheader(); w.writerows(records)

if __name__=='__main__':
    if not ROOT.exists(): raise SystemExit(f'missing assembled tree: {ROOT}')
    remove_caches(ROOT); manifests(ROOT); print(ROOT)
