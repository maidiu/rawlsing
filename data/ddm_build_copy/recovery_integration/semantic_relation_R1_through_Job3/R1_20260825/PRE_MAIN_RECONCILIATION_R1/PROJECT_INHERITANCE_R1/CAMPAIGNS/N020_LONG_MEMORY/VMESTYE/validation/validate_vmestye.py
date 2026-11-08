#!/usr/bin/env python3
"""VMESTYE bootstrap integrity only. Does NOT certify functional or native zero loss."""
from __future__ import annotations
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAILURES: list[str] = []

def read(rel: str) -> list[dict[str, str]]:
    path = ROOT / rel
    if not path.is_file():
        FAILURES.append("MISSING_FILE " + rel)
        return []
    with path.open(encoding="utf-8", newline="") as fp:
        return list(csv.DictReader(fp, delimiter="\t"))

def require(cond: bool, message: str) -> None:
    if not cond:
        FAILURES.append(message)

def exact_ids(rows: list[dict[str, str]], field: str, prefix: str, count: int, label: str) -> None:
    have = [x.get(field, "") for x in rows]
    wanted = {f"{prefix}{i:03d}" for i in range(1, count + 1)}
    require(len(have) == count, f"{label}: expected {count} rows got {len(have)}")
    require(len(set(have)) == len(have), f"{label}: duplicate IDs")
    require(set(have) == wanted, f"{label}: missing={sorted(wanted-set(have))}, extra={sorted(set(have)-wanted)}")

lmx = read("DATA/LMX44_SEED.tsv")
lmq = read("DATA/LMQ30_SEED.tsv")
ff = read("DATA/LEGACY_F29_SEED.tsv")
ar = read("DATA/LEGACY_AR58_SEED.tsv")
aux = read("DATA/C6_AUXILIARY7_SEED.tsv")
atlas = read("DATA/FUNCTION_ATLAS.tsv")
flights = read("CONTROL/FLIGHT_BOARD.tsv")
gates = read("CONTROL/PHASE_GATES.tsv")
estate = read("CONTROL/ESTATE_COVERAGE.tsv")
disputes = read("CONTROL/OPEN_DISPUTES.tsv")
exact_ids(lmx, "obligation_id", "LMX-", 44, "LMX")
exact_ids(lmq, "queue_id", "LMQ-", 30, "LMQ")
have_f = [x.get("function_id", "") for x in ff]
require(len(have_f) == 29 and len(set(have_f)) == 29 and {s[:3] for s in have_f} == {"F01","F02"} if False else len(have_f)==29 and len(set(have_f))==29 and set(int(x[1:3]) for x in have_f if x.startswith("F")) == set(range(1,30)), "F29: ids not exact 01..29")
exact_ids(ar, "release_id", "AR-", 58, "AR")
require(len(aux) == 7, "C6 aux count !=7 (6 DENOMINATOR, 1 CROSSREF expected)")
require(sum(x["row_type"] == "DENOMINATOR" for x in aux) == 6, "C6 denominator rows !=6")
require(sum(x["row_type"] == "CROSSREF" for x in aux) == 1, "C6 crossref rows !=1")
ids = [r.get("record_id","") for r in atlas]
require(len(ids) == 73 and len(set(ids)) == 73, "atlas: missing or duplicate 44 LMX +29 historical category seed IDs")
require(set(ids) == {r["obligation_id"] for r in lmx} | set(have_f), "atlas seed ID anti-join FAIL")
require(all(r.get("current_disposition") == "NOT_ASSESSED_CURRENT" for r in lmx + lmq), "bootstrap seed falsely promotes current status")
require(all(r.get("disposition") == "NOT_ASSESSED_CURRENT" for r in atlas), "bootstrap atlas falsely promotes a success")
require(all(r.get("baseline_source") for r in lmx + lmq + ff + ar + aux), "missing exact source locator in inherited seed")
workers = [r.get("worker_id","") for r in flights]
require(workers == [f"ZL-{i:02d}" for i in range(18)], "flight roster must contain ZL-00..17 exactly")
require(all(r.get("status") == "NOT_DISPATCHED" for r in flights), "bootstrap falsely asserts launched workers")
require(len(gates) == 9 and len({x.get("gate_id") for x in gates}) == 9, "expected 9 unique phase gates")
require(all(g.get("state") == "NOT_RUN" for g in gates), "bootstrap falsely asserts passed phase gate")
expected = {"LMX44":44,"LMQ30":30,"C6_F29":29,"C6_AR58":58,"C6_AUX7":7}
coverage = {r.get("estate_id"):r for r in estate}
for k,n in expected.items():
    require(k in coverage and int(coverage[k].get("bootstrapped_ids","-1")) == n, f"estate {k} bootstrapped count mismatch")
for k in ("C777_CASE55","PROG_COMPONENT62","PROG_SEAM82","PROG_GAP49","PROG_OWNER345","SECTIONS11","R157_SOURCES35"):
    require(k in coverage and coverage[k].get("bootstrap_status") == "NOT_IMPORTED", f"estate {k} must be explicitly NOT_IMPORTED")
require(len(disputes) >= 10, "missing initial negative/unproved issue register")
for w in flights:
    path = w.get("write_scope","")
    if path.startswith("PRONGS/"):
        require((ROOT / path / "00_SCOPE_AND_FINDINGS.md").is_file(), "missing prong route for " + w["worker_id"])
        require((ROOT / path / "FINDINGS.tsv").is_file(), "missing prong findings sheet for " + w["worker_id"])
for rel in ("DATA/OPERATION_TRACES.tsv","DATA/AUTHORITY_APPLICATIONS.tsv","DATA/RELATIONS.tsv","DATA/EVIDENCE.tsv","DATA/DECISION_EVENTS.tsv","CONTROL/RECEIVING_LEDGER.tsv","CONTROL/WORK_ITEM_BOARD.tsv"):
    require((ROOT / rel).is_file(), "missing normalized slot "+rel)
if FAILURES:
    print("BOOTSTRAP_SCHEMA_FAIL__NO_ZERO_LOSS_CERTIFICATION", file=sys.stderr)
    for failure in FAILURES:
        print("FAIL:",failure,file=sys.stderr)
    raise SystemExit(1)
print("BOOTSTRAP_SCHEMA_OK__NO_FUNCTIONAL_OR_NATIVE_CERTIFICATION")
print("Inherited IDs: 44 LMX / 30 LMQ / 29 F / 58 AR / 7 C6 auxiliary; historical-category atlas 73")
print("Fleet: 18 NOT_DISPATCHED; gates: 9 NOT_RUN; additional estates explicitly NOT_IMPORTED")
