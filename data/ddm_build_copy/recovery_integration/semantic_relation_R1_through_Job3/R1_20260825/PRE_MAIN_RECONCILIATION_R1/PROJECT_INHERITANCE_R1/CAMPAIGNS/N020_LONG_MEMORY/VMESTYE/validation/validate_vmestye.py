#!/usr/bin/env python3
"""VMESTYE P0 bootstrap integrity: drift/no-drop only, not functional zero-loss proof.

Exact source/semantic correspondence requires the separate independently received P0
source-field court. This script deliberately cannot approve a scientific/actor claim.
"""
from __future__ import annotations

import csv
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []

# Seed rows were compared against the pinned D01 and C6 source contents at P0
# authoring scope. These blob pins block unreviewed silent mutation, not semantic
# equivalence. Changing seed schema requires a new reviewed source-fidelity record.
FROZEN_BLOBS = {
    "DATA/LMX44_SEED.tsv": "f09548a0c67293983c775b5dc2b506cec3b74af4",
    "DATA/LMQ30_SEED.tsv": "e9aece8890d2e5495413b22c4e90b7c60f4dcb38",
    "DATA/LEGACY_F29_SEED.tsv": "d571847a13117d3b039057edbbec314300000d79",
    "DATA/LEGACY_AR58_SEED.tsv": "49513d3040ca4f8c3ccc17f0abd5092260fa2463",
    "DATA/C6_AUXILIARY7_SEED.tsv": "cf64464249772c713a10f96644a1f9ef214aaebd",
}

def check(predicate: bool, why: str) -> None:
    if not predicate:
        ERRORS.append(why)

def table(path: str) -> list[dict[str, str]]:
    full = ROOT / path
    if not full.is_file():
        ERRORS.append("MISSING_FILE " + path)
        return []
    with full.open(encoding="utf-8", newline="") as file:
        raw = list(csv.reader(file, delimiter="\t", strict=True))
    if not raw:
        ERRORS.append("EMPTY_FILE " + path)
        return []
    fields, *records = raw
    check(all(fields) and len(fields) == len(set(fields)), f"{path}: missing/duplicate header")
    result = []
    for num, row in enumerate(records, 2):
        if not any(row):
            ERRORS.append(f"{path}:{num}: empty row")
            continue
        check(len(row) == len(fields), f"{path}:{num}: width {len(row)} != {len(fields)}")
        result.append(dict(zip(fields, row)))
    return result

def exact_ids(rows: list[dict[str,str]], key: str, want: set[str], name: str) -> None:
    have = [r.get(key, "") for r in rows]
    check(len(have) == len(want), f"{name}: expected {len(want)} rows; observed {len(have)}")
    check(len(have) == len(set(have)), f"{name}: duplicated IDs")
    check(set(have) == want, f"{name}: missing={sorted(want-set(have))}, unexpected={sorted(set(have)-want)}")

def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

for path, expected in FROZEN_BLOBS.items():
    full = ROOT / path
    if full.is_file():
        check(git_blob(full.read_bytes()) == expected, f"{path}: frozen seed source-content drift")
    else:
        ERRORS.append(f"{path}: frozen seed missing")

lmx = table("DATA/LMX44_SEED.tsv")
lmq = table("DATA/LMQ30_SEED.tsv")
ff = table("DATA/LEGACY_F29_SEED.tsv")
ar = table("DATA/LEGACY_AR58_SEED.tsv")
aux = table("DATA/C6_AUXILIARY7_SEED.tsv")
atlas = table("DATA/FUNCTION_ATLAS.tsv")
flights = table("CONTROL/FLIGHT_BOARD.tsv")
gates = table("CONTROL/PHASE_GATES.tsv")
estate = table("CONTROL/ESTATE_COVERAGE.tsv")
recent = table("CONTROL/RECENT_CAMPAIGN_INTAKE.tsv")
sr = table("CONTROL/SR01_RETURN_REGISTER.tsv")
disputes = table("CONTROL/OPEN_DISPUTES.tsv")

exact_ids(lmx, "obligation_id", {f"LMX-{n:03d}" for n in range(1,45)}, "Long Memory")
exact_ids(lmq, "queue_id", {f"LMQ-{n:03d}" for n in range(1,31)}, "Long Memory debt")
exact_ids(ar, "release_id", {f"AR-{n:04d}" for n in range(1,59)}, "C6 authority")
fids = [r.get("function_id","") for r in ff]
check(len(fids) == 29 and len(set(fids)) == 29 and
      {int(match.group(1)) for fid in fids if (match := re.fullmatch(r"F(\d{2})_.+", fid))} == set(range(1,30)),
      "F29 exact original function IDs 01..29 / duplicates")
check(len(aux)==7 and sum(x.get("row_type")=="DENOMINATOR" for x in aux)==6 and
      sum(x.get("row_type")=="CROSSREF" for x in aux)==1, "C6 auxiliary 6+1 mismatch")
aid={r.get("record_id") for r in atlas}
check(len(atlas)==73 and len(aid)==73 and
      aid == {x.get("obligation_id") for x in lmx}|set(fids),
      "Atlas 44 LMX +29 F exact identity mismatch")
check(all(x.get("current_disposition")=="NOT_ASSESSED_CURRENT" for x in lmx+lmq),
      "Inherited baseline improperly promoted as current")
check(all(x.get("disposition")=="NOT_ASSESSED_CURRENT" for x in atlas),
      "Bootstrap atlas falsely claims current functional disposition")
check(all(x.get("baseline_source") for x in lmx+lmq+ff+ar+aux),
      "Inherited source cut/row missing")
check([r.get("worker_id") for r in flights]==[f"ZL-{n:02d}" for n in range(18)],
      "Fleet 00..17 not exactly conserved")
check(all(x.get("status")=="NOT_DISPATCHED" for x in flights),
      "Bootstrap cannot prove worker launched")
check(len(gates)==9 and len({g.get("gate_id") for g in gates})==9 and
      all(g.get("state")=="NOT_RUN" for g in gates),
      "Exactly 9 P0..P4 gates expected NOT_RUN until independent court")

exact_ids(recent, "record_id",{f"RM{n:02d}" for n in range(1,31)},"recent campaign intake")
lookup={r.get("record_id"):r for r in recent}
for key, exact_sha, key_phrase in [
    ("RM23","ee68062789fe55ebac0255060039c756a8d36b30","RETURNED"),
    ("RM24","37915a47ed3e33a71ad8334c0aa505f5d65796ca","RETURNED"),
    ("RM09","b8df0fa0e46e5c9be63978168ad6d2392944cca5","REPAIR"),
    ("RM30","41533b89c4f7cfd1d8067a2c0a2b8afd0463163b","PROTECTED"),
]:
    r=lookup.get(key,{})
    check(r.get("sha_or_cut")==exact_sha and key_phrase in r.get("status_at_read_cut",""),
          f"{key}: stale or misrepresented branch/return status")
    check(bool(r.get("source_link")), f"{key}: lost reviewed locator")

expected_sr={
    "PYAT_SR01": {
        "branch_head":"ee68062789fe55ebac0255060039c756a8d36b30",
        "classification_rows":2416,"reference_only":1203,"spine_current":468,
        "historical_candidate":310,"unresolved":373,"spine_required_unbuilt":55,
        "historical_rejected":7,"historical_sublated":0
    },
    "SOROK_SR01": {
        "branch_head":"37915a47ed3e33a71ad8334c0aa505f5d65796ca",
        "classification_rows":1314,"reference_only":949,"spine_current":47,
        "historical_candidate":163,"unresolved":51,"spine_required_unbuilt":96,
        "historical_rejected":8,"historical_sublated":0
    }
}
exact_ids(sr,"estate_id",set(expected_sr),"SR-01 source returns")
for row in sr:
    ex=expected_sr.get(row.get("estate_id"),{})
    for key,value in ex.items():
        check(row.get(key)==str(value),f"SR-01 {row.get('estate_id')} {key}: bad pinned count")
    count=sum(int(row.get(k,0)) for k in (
        "reference_only","spine_current","historical_candidate","unresolved",
        "spine_required_unbuilt","historical_rejected","historical_sublated"))
    check(count==int(row.get("classification_rows",0)),
          f"SR-01 {row.get('estate_id')}: classification class sum mismatch")
    check(row.get("worker_return_grade")=="RETURNED_S0_S1_SOURCE_GRADED" and
          row.get("independent_review_grade")=="PENDING" and
          row.get("functional_conservation_grade")=="NOT_PROVED",
          f"SR-01 {row.get('estate_id')}: false independent or functionality green")
    check(bool(row.get("worker_return_path")) and bool(row.get("classification_manifest_path")),
          f"SR-01 {row.get('estate_id')}: missing source paths")

cov={x.get("estate_id"):x for x in estate}
check(len(cov)==len(estate), "Estate duplicate IDs")
for id,want in {
 "LMX44":44,"LMQ30":30,"C6_F29":29,"C6_AR58":58,"C6_AUX7":7,
 "RECENT_CAMPAIGN30":30}.items():
    check(cov.get(id,{}).get("bootstrapped_ids")==str(want),
          f"Estate {id} imported identity number invalid")
for id,want in {
 "C777_CASE55":55,"PROG_COMPONENT62":62,"PROG_SEAM82":82,
 "PROG_GAP49":49,"PROG_OWNER345":345,"SECTIONS11":11,"R157_SOURCES35":35,
 "PYAT_SR01_2416":2416,"SOROK_SR01_1314":1314,"SOROK_ASSETS304":304,
 "SOROK_FUNCTION144":144,"SOROK_W1_INPUT100":100,
 "SOROK_VERSIONED_SEAM38":38,"SOROK_PHASE_GATES83":83,
 "SOROK_SOURCE_INDEX_ONLY48":48,"PYAT_SR01_UNRESOLVED373":373,
 "SOROK_SR01_UNRESOLVED51":51}.items():
    x=cov.get(id,{})
    check(x.get("expected_ids_at_source_cut")==str(want) and
          x.get("bootstrapped_ids")=="0" and "NOT_IMPORTED" in x.get("bootstrap_status",""),
          f"Estate {id} must remain identified yet not substantively imported at P0 bootstrap")
check(len(disputes)>=10, "Missing known negative/uncertain disputes")
for w in flights:
    path=w.get("write_scope","")
    if path.startswith("PRONGS/"):
        for item in ("00_SCOPE_AND_FINDINGS.md","FINDINGS.tsv"):
            check((ROOT/path/item).is_file(),f"Missing {path}/{item}")
for path in (
    "DATA/OPERATION_TRACES.tsv","DATA/AUTHORITY_APPLICATIONS.tsv",
    "DATA/RELATIONS.tsv","DATA/EVIDENCE.tsv","DATA/DECISION_EVENTS.tsv",
    "DATA/IMPLEMENTATIONS.tsv","DATA/CONSUMER_EDGES.tsv",
    "CONTROL/RECEIVING_LEDGER.tsv","CONTROL/WORK_ITEM_BOARD.tsv",
    "12_NOVEMBER_RECOVERY_AND_BRANCH_INTAKE.md",
    "13_SR01_CLASSIFICATION_AND_FUNCTIONAL_CONSERVATION.md"):
    check((ROOT/path).is_file(), "Missing required VMESTYE contract: "+path)

if ERRORS:
    print("BOOTSTRAP_ID_AND_STATUS_FAIL__FUNCTIONAL_ZERO_LOSS_UNPROVED",file=sys.stderr)
    for err in ERRORS:
        print("FAIL:",err,file=sys.stderr)
    raise SystemExit(1)
print("BOOTSTRAP_SOURCE_PIN_AND_SHAPE_OK__FUNCTIONAL_ZERO_LOSS_UNPROVED")
print("Inherited 44/30/29/58/7 IDs and source blobs pinned; 30 recent campaign records")
print("Pyat SR-01 2416 / Sorok SR-01 1314 pinned branch return grades, not adopted")
print("18 workers NOT_DISPATCHED / 9 gates NOT_RUN; current functional atlas not proved")
