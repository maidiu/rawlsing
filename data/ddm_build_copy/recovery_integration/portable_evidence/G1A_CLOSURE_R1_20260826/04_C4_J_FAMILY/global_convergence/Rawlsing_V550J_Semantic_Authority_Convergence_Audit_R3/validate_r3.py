#!/usr/bin/env python3
import csv, json, sys
from pathlib import Path

root = Path(__file__).resolve().parent
out = root / "output"

scope = list(csv.DictReader((out/"CANONICAL_35_WAVE_SCOPE_R3.csv").open()))
assert len(scope) == 35, len(scope)

expected = {
    "Afrobarometer": {"R1","R5","R9"},
    "Arab Barometer": {"I","II","V","VIII"},
    "Asian Barometer": {"W1","W4","W5"},
    "EVS": {"1981","1990","1999","2008","2017"},
    "GSS": {"1972","1973","1984","1993","2002","2010","2016","2024"},
    "Latinobarómetro": {"1995","2011","2024"},
    "LiTS": {"2006","II","III","IV"},
    "South Asia": {"W1","W2"},
    "WVS": {"W1","W4","W7"},
}
actual = {}
for r in scope:
    actual.setdefault(r["source_family"], set()).add(r["canonical_wave"])
assert actual == expected, (actual, expected)

q = list(csv.DictReader((out/"SEMANTIC_EDGE_ADJUDICATION_QUEUE_R3_SOURCE_INTEGRITY_GATED.csv").open()))
assert len(q) == 445
from collections import Counter
c=Counter(r["r3_adjudication_status"] for r in q)
assert c["READY_FOR_TYPED_SEMANTIC_ADJUDICATION"] == 431, c
assert c["READY_FOR_SEMANTIC_ADJUDICATION_RUNTIME_FAIL_CLOSED"] == 3, c
assert c["HOLD_SOURCE_STRUCTURE_CORRECTION_BEFORE_AUTHORITY"] == 7, c
assert c["DISCOVERY_ONLY_NOT_IN_GOVERNING_JOINT_DENOMINATOR"] == 3, c
assert c["HOLD_NORMALIZE_SOURCE_OBJECT_BEFORE_AUTHORITY"] == 1, c

corr = list(csv.DictReader((out/"R14_SOURCE_NATIVE_CORRECTION_OVERLAY_PROPOSED_R3.csv").open()))
assert len(corr) == 11, len(corr)

summary=json.load((out/"R3_VALIDATION_SUMMARY.json").open())
assert summary["canonical_scope_entry_count"]==35
print("PASS: R3 scope and source-integrity gate validated")
