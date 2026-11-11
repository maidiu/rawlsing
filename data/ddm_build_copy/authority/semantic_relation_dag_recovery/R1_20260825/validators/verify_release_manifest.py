#!/usr/bin/env python3
from pathlib import Path
import csv, hashlib, sys

ROOT=Path(__file__).resolve().parents[1]
MAN=ROOT/"provenance"/"FILE_MANIFEST_SHA256.csv"

def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()

with MAN.open(newline="",encoding="utf-8-sig") as f:
    rows=list(csv.DictReader(f))
expected={r["relative_path"]:(int(r["bytes"]),r["sha256"]) for r in rows}
for rel,(n,h) in expected.items():
    p=ROOT/rel
    assert p.is_file(), f"missing manifest file: {rel}"
    assert p.stat().st_size==n, f"size mismatch: {rel}"
    assert sha(p)==h, f"sha mismatch: {rel}"

ignored={"provenance/FILE_MANIFEST_SHA256.csv","provenance/INSTALL_RECEIPT.json"}
actual={str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file() and str(p.relative_to(ROOT)) not in ignored}
extra=actual-set(expected)
missing=set(expected)-actual
assert not extra, f"unmanifested supplied files: {sorted(extra)}"
assert not missing, f"manifest entries absent: {sorted(missing)}"
print(f"PASS manifest files={len(expected)}")
