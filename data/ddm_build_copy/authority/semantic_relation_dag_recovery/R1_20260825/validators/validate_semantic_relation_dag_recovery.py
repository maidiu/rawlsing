#!/usr/bin/env python3
"""Hostile validator for semantic_relation_dag_recovery/R1_20260825.

Stdlib-only. Fails closed on row-count, uniqueness, succession, or cross-layer drift.
"""
from pathlib import Path
import csv, json, sys

ROOT = Path(__file__).resolve().parents[1]
CG = ROOT / "canonical_graph"
PROV = ROOT / "provenance"

def read_csv(name):
    p = CG / name
    with p.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def read_prov(name):
    p = PROV / name
    with p.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def parse_json_list(s):
    if not s:
        return []
    try:
        v = json.loads(s)
    except Exception as e:
        raise AssertionError(f"invalid JSON list: {s[:120]!r}: {e}")
    assert isinstance(v, list), f"expected list JSON, got {type(v)}"
    return [str(x) for x in v]

def member_key(row):
    return tuple(sorted(parse_json_list(row.get("member_implementation_ids_json", ""))))

exp = json.loads((ROOT/"validators"/"EXPECTED_COUNTS.json").read_text())

job3 = read_csv("JOB3_R3_FINAL_GOVERNED_RELATION_TOPOLOGY.csv")
accept = read_csv("JOB3_R3_ACCEPTED_EDGE_METADATA.csv")
reject = read_csv("JOB3_R3_REJECTED_TYPED_RELATION_CANDIDATES.csv")
blocked = read_csv("JOB3_R3_BLOCKED_CANDIDATES.csv")
o12 = read_csv("O12_R3_EXISTING_GOVERNED_TOPOLOGY.csv")
r16f = read_csv("R16F_POSITIVE_S14_RELATION_AUTHORITY.csv")
r16f_neg = read_csv("R16F_PROVEN_NEGATIVE_S14_RELATION_AUTHORITY.csv")
r16f_cov = read_csv("R16F_WAVE_RULE_COVERAGE.csv")
r16g = read_csv("R16G_T03_T11_CAPABILITY_ATLAS.csv")
t06 = read_csv("T06_STRICT_SOURCE_FIRST_RELATION_AUTHORITY.csv")
t15 = read_csv("T15_POSITIVE_RELATION_AUTHORITY_COMPACT.csv")
o11 = read_csv("O11_T15_WAVE_RELATION_CAPABILITY_ATLAS.csv")
succ = read_prov("R16F_TO_CURRENT_EDGE_SUCCESSION.csv")

assert len(job3) == exp["job3_final_positive_edges"]
assert len(accept) == exp["job3_new_accepts"]
assert len(reject) == exp["job3_rejected_candidates"]
assert len(blocked) == exp["job3_blocked_candidates"]
assert len(o12) == exp["o12_existing_governed_positive_edges"]
assert len(r16f) == exp["r16f_positive_edges"]
assert len(r16f_neg) == exp["r16f_proven_negative_rows"]
assert len(r16f_cov) == exp["r16f_wave_rule_cells"]
assert len(r16g) == exp["r16g_wave_rule_cells"]
assert len(t06) == exp["strict_t06_edges"]
assert len(t15) == exp["t15_positive_edges"]
assert len(o11) == exp["o11_t15_wave_rule_cells"]

job3_ids = [r["authority_id"] for r in job3]
assert len(job3_ids) == len(set(job3_ids)), "duplicate Job3 terminal authority_id"
accept_ids = [r["authority_id"] for r in accept]
assert len(accept_ids) == len(set(accept_ids)), "duplicate accepted authority_id"
assert set(accept_ids).issubset(set(job3_ids)), "accepted edges missing from terminal topology"

origins = {}
for r in job3:
    origins[r["authority_origin"]] = origins.get(r["authority_origin"], 0) + 1
expected_origins = {
    "JOB3_R3_TYPED_SEMANTIC_ADJUDICATION": 552,
    "R6_EXISTING_RELATION_AUTHORITY": 249,
    "CENTRAL_T15_SOURCE_FIRST_R1": 188,
    "R16F_SOURCE_FIRST_RELATION_AUTHORITY": 137,
    "CENTRAL_STRICT_T06_SOURCE_FIRST_R1": 64,
}
assert origins == expected_origins, f"terminal origin drift: {origins}"

r16f_t06 = [r for r in r16f if r["rule_id"] == "T06"]
assert len(r16f_t06) == exp["r16f_t06_edges"]
assert sum(1 for r in r16f if r["authority_class"] == "RETAIN_EXISTING_GOVERNED_R6") == 117
assert sum(1 for r in r16f if r["authority_class"] == "CENTRAL_ACCEPTED_NEW_R16E") == 27

job3_set = set(job3_ids)
o12_set = {r["authority_id"] for r in o12}
t06_set = {r["central_relation_id"] for r in t06}
t15_set = {r["central_relation_id"] for r in t15}
assert t06_set <= o12_set and t06_set <= job3_set, "strict T06 not fully carried into O12/Job3"
assert t15_set <= o12_set and t15_set <= job3_set, "T15 not fully carried into O12/Job3"

# Old R16F T06 IDs must NOT be unioned into current graph.
old_t06_ids = {r["central_relation_id"] for r in r16f_t06}
assert not (old_t06_ids & job3_set), "obsolete R16F T06 ID leaked into current Job3 topology"

# But every old T06 member-set must be independently represented by exactly one strict source-first T06 edge.
t06_by_members = {}
for r in t06:
    t06_by_members.setdefault(member_key(r), []).append(r["central_relation_id"])
for r in r16f_t06:
    matches = t06_by_members.get(member_key(r), [])
    assert len(matches) == 1, f"R16F T06 edge {r['central_relation_id']} does not map 1:1 by exact members: {matches}"

assert len(succ) == 144
assert sum(r["succession_status"] == "SURVIVES_SAME_ID_TO_JOB3" for r in succ) == 137
assert sum(r["succession_status"] == "RECERTIFIED_SOURCE_FIRST_T06_NEW_ID" for r in succ) == 7
assert sum(r["succession_status"] == "NO_AUTOMATIC_CURRENT_SUCCESSOR__REVIEW_REQUIRED" for r in succ) == 0

# Open-world law: R16F must license no wave×rule absence claims.
licensed = [r for r in r16f_cov if str(r.get("absence_claim_licensed","")).strip().upper() in {"TRUE","YES","1"}]
assert not licensed, f"R16F unexpectedly licenses absence in {len(licensed)} cells"

# Candidate court partitions are disjoint at candidate-id grain.
a_cids = {r["candidate_id"] for r in accept}
r_cids = {r["candidate_id"] for r in reject}
b_cids = {r["candidate_id"] for r in blocked}
assert not (a_cids & r_cids or a_cids & b_cids or r_cids & b_cids), "Job3 candidate dispositions overlap"
assert len(a_cids | r_cids | b_cids) == 1264, "Job3 candidate court does not partition 1,264 candidates"

print(json.dumps({
    "result": "PASS",
    "job3_terminal_edges": len(job3),
    "job3_candidate_partition": {"ACCEPT":len(a_cids),"REJECT":len(r_cids),"BLOCKED":len(b_cids)},
    "r16f_same_id_survivors": 137,
    "r16f_t06_recertified": 7,
    "strict_t06": len(t06),
    "t15": len(t15),
    "r16f_absence_claim_cells": len(licensed)
}, indent=2))
