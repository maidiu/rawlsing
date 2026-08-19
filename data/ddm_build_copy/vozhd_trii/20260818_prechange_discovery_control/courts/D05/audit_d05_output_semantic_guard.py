#!/usr/bin/env python3
"""Guard D05 outputs against false preservation claims when fields are absent.

This post-pass changes only D05 output files. It never connects to or mutates the
database. Its purpose is mechanical: a comparison cannot equal PASS when the
field being compared is not physically exposed by the target relation.
"""
from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path

COURT = Path("data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/courts/D05")


def root() -> Path:
    r = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    return Path(r)


def read(path: Path):
    if not path.exists(): return [], []
    with path.open(newline="",encoding="utf-8") as f:
        rr=csv.DictReader(f); return rr.fieldnames or [], list(rr)


def write(path: Path, fields, rows):
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore"); w.writeheader(); w.writerows(rows)


def main() -> int:
    d=root()/COURT
    _,pre=read(d/"RELATION_PREFLIGHT.csv")
    cols={r["relation"]:set(json.loads(r["actual_columns_json"] or "[]")) for r in pre if r.get("relation")}
    pf,par=read(d/"FACET_READY_PARITY_AUDIT.csv")
    for r in par:
        c=cols.get(r.get("relation",""),set())
        tags=[]
        if "value_raw" not in c:
            r["value_raw_mismatch_rows"]="NOT_EXPOSED"; tags.append("VALUE_RAW_NOT_EXPOSED")
        if "value_text" not in c:
            r["value_text_mismatch_rows"]="NOT_EXPOSED"; tags.append("VALUE_TEXT_NOT_EXPOSED")
        if tags:
            r["status"]=(r.get("status","")+"|"+"|".join(tags)).strip("|")
    if pf: write(d/"FACET_READY_PARITY_AUDIT.csv",pf,par)

    inf,info=read(d/"INFORMATION_LOSS_AUDIT.csv")
    for r in info:
        target=r.get("surface","")
        prop=r.get("property","")
        c=cols.get(target,set())
        if prop=="raw_code_multiset" and "value_raw" not in c:
            r["observed_value"]="NOT_EXPOSED"; r["status"]="UNPROVED_NOT_EXPOSED"; r["failure_code"]="D05_W_RAW_CODE_NOT_EXPOSED"
        if prop=="raw_text_multiset" and "value_text" not in c:
            r["observed_value"]="NOT_EXPOSED"; r["status"]="UNPROVED_NOT_EXPOSED"; r["failure_code"]="D05_W_RAW_TEXT_NOT_EXPOSED"
    if inf: write(d/"INFORMATION_LOSS_AUDIT.csv",inf,info)
    return 0


if __name__=="__main__": raise SystemExit(main())
