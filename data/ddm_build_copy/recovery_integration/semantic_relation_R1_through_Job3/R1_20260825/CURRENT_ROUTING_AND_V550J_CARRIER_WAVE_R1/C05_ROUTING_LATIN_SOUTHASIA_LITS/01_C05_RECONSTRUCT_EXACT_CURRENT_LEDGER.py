#!/usr/bin/env python3
"""Reconstruct C05's exact 5,387-row Authority-45 ledger from the pinned current catalog."""
import argparse, csv, hashlib, json, sys

TARGET_FAMILIES = {"Latinobarómetro", "South Asia", "LiTS"}

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""): h.update(chunk)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--catalog", required=True, help="Rawlsing_P2_Phase0_Governed_Question_Node_Catalog_v1.json")
    ap.add_argument("--carrier", default="01_C05_COMPACT_EXACT_CURRENT_LEDGER.json")
    ap.add_argument("--out", default="-")
    a=ap.parse_args()
    carrier=json.load(open(a.carrier,encoding="utf-8"))
    expected=carrier["input"]["phase0_catalog"]["sha256"]
    actual=sha256_file(a.catalog)
    if actual != expected:
        raise SystemExit(f"catalog SHA mismatch: {actual} != {expected}")
    obj=json.load(open(a.catalog,encoding="utf-8"))
    rows=[r for r in obj["question_implementations"] if r["source_family"] in TARGET_FAMILIES]
    rows.sort(key=lambda r:r["question_implementation_id"])
    ids=[r["question_implementation_id"] for r in rows]
    if len(ids)!=5387 or len(set(ids))!=5387:
        raise SystemExit("current C05 denominator is not exactly 5,387 unique IDs")
    id_sha=hashlib.sha256(("\n".join(ids)+"\n").encode()).hexdigest()
    if id_sha != carrier["input"]["ordered_question_implementation_ids_sha256"]:
        raise SystemExit("ordered current-ID hash mismatch")
    codes=carrier["encoding"]["codes"]
    if len(codes)!=len(rows): raise SystemExit("code count mismatch")
    code_map=carrier["encoding"]["code_map"]
    out=sys.stdout if a.out=="-" else open(a.out,"w",encoding="utf-8",newline="")
    w=csv.writer(out,delimiter="\t")
    w.writerow(["question_implementation_id","source_family","wave","source_variable_code","disposition"])
    pair_hash=hashlib.sha256()
    for r,c in zip(rows,codes):
        if c not in code_map: raise SystemExit(f"illegal disposition code {c}")
        pair_hash.update(f"{r['question_implementation_id']}\t{c}\n".encode())
        w.writerow([r["question_implementation_id"],r["source_family"],r["wave"],r["source_variable_code"],code_map[c]])
    if out is not sys.stdout: out.close()
    if pair_hash.hexdigest()!=carrier["encoding"]["pair_stream_sha256"]:
        raise SystemExit("ID/disposition pair hash mismatch")

if __name__=="__main__":
    main()
