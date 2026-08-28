#!/usr/bin/env python3
"""Experiment-only hostile oracle for Authority 35 full fracture-map conservation.

This module deliberately imports no Rawlsing production code. It freezes and
validates the expected semantic answer independently of current I05 capability.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

FIXTURE_SHA256 = "83c496c9482c2e9736a6797e243965110899c1aa97436d752795b15d483a8215"
LOGICAL_DIGEST = "e4ef71ccf3815b0734013a5ebf1c85f9f3ac94720b30f2c5cf6285aa784a0017"
MIN_SUPPORT = 3
NUMERIC_FIELDS = {"eligible","P","Q","R","S","U","C1","C2","XOR_A","XOR_B","XOR_C","weight"}

def _load(path: Path):
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == FIXTURE_SHA256, "fixture byte hash drift"
    rows = []
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for key in NUMERIC_FIELDS:
                if row[key] != "":
                    row[key] = int(row[key])
            rows.append(row)
    return rows

def _logical_digest(rows):
    fields = ["respondent_id","replay_key","eligible","response_state","response_pattern","P","Q","R","S","U","C1","C2","FOLLOWUP","XOR_A","XOR_B","XOR_C","weight","segment"]
    material = [{k: row[k] for k in fields} for row in sorted(rows, key=lambda r: r["respondent_id"])]
    payload = json.dumps(material, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()

def _substantive(rows):
    return [r for r in rows if r["response_state"] == "SUBSTANTIVE"]

def _contingency(rows, a, b):
    c = Counter((r[a], r[b]) for r in rows)
    return {f"{x}{y}": c[(x, y)] for x in (0, 1) for y in (0, 1)}

def _phi(table):
    n00, n01, n10, n11 = table["00"], table["01"], table["10"], table["11"]
    num = n11*n00 - n10*n01
    den = math.sqrt((n10+n11)*(n00+n01)*(n01+n11)*(n00+n10))
    return 0.0 if den == 0 else num/den

def _modal_rate(rows):
    if not rows:
        return None
    return sum(r["response_pattern"] == "A+B" for r in rows) / len(rows)

def _signature(rows):
    return {
        "overall_patterns": dict(sorted(Counter(r["response_pattern"] for r in rows).items())),
        "p1_n": sum(r["P"] == 1 for r in rows),
        "p0_n": sum(r["P"] == 0 for r in rows),
        "q1_deviant_n": sum(r["P"] == 1 and r["response_pattern"] != "A+B" and r["Q"] == 1 for r in rows),
        "stable_b_n": sum(r["P"] == 0 and r["response_pattern"] == "B_ONLY" for r in rows),
        "cosig_global": _contingency(rows, "C1", "C2"),
        "xor_triples": dict(sorted((f"{a}{b}{c}", n) for (a,b,c), n in Counter((r["XOR_A"],r["XOR_B"],r["XOR_C"]) for r in rows).items())),
    }

def run_oracle(fixture: Path):
    rows = _load(fixture)
    assert len(rows) == 52
    assert len({r["respondent_id"] for r in rows}) == 52
    assert len({r["replay_key"] for r in rows}) == 52
    assert _logical_digest(rows) == LOGICAL_DIGEST

    substantive = _substantive(rows)
    assert len(substantive) == 48
    assert Counter(r["response_pattern"] for r in substantive) == {"A+B":24,"A_ONLY":14,"B_ONLY":6,"NONE":4}
    assert Counter(r["response_state"] for r in rows) == {"SUBSTANTIVE":48,"MISSING":1,"REFUSED":1,"NOT_APPLICABLE":1,"UNKNOWN":1}

    p1 = [r for r in substantive if r["P"] == 1]
    p0 = [r for r in substantive if r["P"] == 0]
    assert (len(p1), len(p0)) == (28,20)
    assert sum(r["response_pattern"] == "A+B" for r in p1) == 20
    assert sum(r["response_pattern"] == "A+B" for r in p0) == 4
    assert _modal_rate(p1) > _modal_rate(p0)

    assert sum(r["P"] == 1 and r["response_pattern"] == "A+B" for r in substantive) == 20
    assert sum(r["P"] == 1 and r["response_pattern"] != "A+B" for r in substantive) == 8
    assert sum(r["P"] == 0 and r["response_pattern"] == "A+B" for r in substantive) == 4
    assert sum(r["P"] == 0 and r["response_pattern"] != "A+B" for r in substantive) == 16

    deviants = [r for r in substantive if r["P"] == 1 and r["response_pattern"] != "A+B"]
    q1 = [r for r in deviants if r["Q"] == 1]
    q0 = [r for r in deviants if r["Q"] == 0]
    assert len(q1) == 6 and {r["response_pattern"] for r in q1} == {"A_ONLY"}
    assert len(q0) == 2 and {r["response_pattern"] for r in q0} == {"NONE"}

    r1 = [r for r in p0 if r["R"] == 1]
    r0 = [r for r in p0 if r["R"] == 0]
    assert (len(r1), sum(r["response_pattern"] == "A+B" for r in r1)) == (6,4)
    assert (len(r0), sum(r["response_pattern"] == "A+B" for r in r0)) == (14,0)

    s1 = [r for r in q1 if r["S"] == 1]
    s0 = [r for r in q1 if r["S"] == 0]
    assert len(s1) == 4 and {r["FOLLOWUP"] for r in s1} == {"F_HIGH"}
    assert len(s0) == 2 and {r["FOLLOWUP"] for r in s0} == {"F_LOW"}

    global_cosig = _contingency(substantive, "C1", "C2")
    branch_cosig = _contingency(q1, "C1", "C2")
    assert global_cosig == {"00":3,"01":21,"10":21,"11":3}
    assert branch_cosig == {"00":3,"01":0,"10":0,"11":3}
    assert abs(_phi(global_cosig) + 0.75) < 1e-12
    assert abs(_phi(branch_cosig) - 1.0) < 1e-12

    a_present = sum(r["response_pattern"] in {"A+B","A_ONLY"} for r in substantive)
    b_present = sum(r["response_pattern"] in {"A+B","B_ONLY"} for r in substantive)
    assert (a_present,b_present) == (38,30)
    assert 22+16 == a_present and 22+8 == b_present and 22+16+8+2 == 48

    for a,b in (("XOR_A","XOR_B"),("XOR_A","XOR_C"),("XOR_B","XOR_C")):
        table = _contingency(substantive,a,b)
        assert table == {"00":12,"01":12,"10":12,"11":12}
        assert abs(_phi(table)) < 1e-12
    triples = Counter((r["XOR_A"],r["XOR_B"],r["XOR_C"]) for r in substantive)
    assert triples == {(0,0,0):12,(0,1,1):12,(1,0,1):12,(1,1,0):12}
    assert all(r["XOR_C"] == (r["XOR_A"] ^ r["XOR_B"]) for r in substantive)

    stable_b = [r for r in substantive if r["P"] == 0 and r["response_pattern"] == "B_ONLY"]
    assert len(stable_b) == 6
    underpowered = [r for r in stable_b if r["U"] == 1]
    assert len(underpowered) == 2 and len(underpowered) < MIN_SUPPORT
    assert not [r for r in substantive if r["P"] == 1 and r["response_pattern"] == "B_ONLY"]
    residual_none = [r for r in substantive if r["response_pattern"] == "NONE"]
    assert len(residual_none) == 4 and all(r["response_state"] == "SUBSTANTIVE" for r in residual_none)

    base_sig = _signature(substantive)
    perturbed = [dict(r) for r in substantive]
    target = next(r for r in perturbed if r["respondent_id"] == "SYN-R035")
    assert target["R"] == 0
    target["R"] = 1
    assert _signature(perturbed) == base_sig
    p0_after = [r for r in perturbed if r["P"] == 0]
    r1_after = [r for r in p0_after if r["R"] == 1]
    r0_after = [r for r in p0_after if r["R"] == 0]
    assert (len(r1_after),sum(r["response_pattern"] == "A+B" for r in r1_after)) == (7,4)
    assert (len(r0_after),sum(r["response_pattern"] == "A+B" for r in r0_after)) == (13,0)

    return {
        "status":"PASS",
        "fixture_sha256":FIXTURE_SHA256,
        "logical_digest":LOGICAL_DIGEST,
        "substantive_n":48,
        "modal_response":"A+B",
        "global_cosignature_phi":-0.75,
        "branch_cosignature_phi":1.0,
        "xor_pairwise_phi":0.0,
        "stable_minority_n":6,
        "underpowered_n":2,
        "valid_empty_n":0,
        "perturbation":"SYN-R035:R:0->1",
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path, nargs="?", default=Path(__file__).with_name("SYNTHETIC_RESPONDENTS.csv"))
    args = parser.parse_args()
    print(json.dumps(run_oracle(args.fixture), sort_keys=True, indent=2))

if __name__ == "__main__":
    main()
