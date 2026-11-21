#!/usr/bin/env python3
"""Bounded read-only integrity court for the SOROK TOTAL source-conservation bank.

This checks deposited source identifiers, paths and user-idea completeness.
It is NOT review of every cited historical source, accepted native code or
human-psychological scientific evidence.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
source = json.loads((ROOT / "01_MACHINE_SOURCE_UNION_757_ROWS.json").read_text())
paths = json.loads((ROOT / "02_CURATED_SOURCE_DIRECTORY_LOCATOR.json").read_text())
ideas = (ROOT / "04_USER_CONVERSATION_NO_DROP_AND_NEW_IDEAS.md").read_text()

o = source["original_function_and_source_registry"]
h = source["original_ideation_H001_H190"]
q = source["original_product_questions_Q"]
s = source["original_workstreams_S0_S16"]
c = source["sorokuda_source_and_alternative_versions"]

expected = [
    ("OINDEX", o, 144),
    ("H", h, 190),
    ("Q", q, 123),
    ("S", s, 17),
    ("SOROKUDA", c, 300),
]
for name, rows, total in expected:
    assert len(rows) == total, (name, "COUNT", len(rows), total)
    ids = [r["id"] for r in rows]
    assert len(set(ids)) == total, (name, "DUPLICATE", [x for x, n in Counter(ids).items() if n > 1])
    assert all(isinstance(r["id"], str) and r["id"] for r in rows)
assert {r["id"] for r in h} == {f"H{i:03d}" for i in range(1, 191)}
assert {r["id"] for r in s} == {f"S{i}" for i in range(17)}
assert {r["id"] for r in s} == {r["id"] for r in o if r["kind"] == "DECLARED_S0_S16_WORKSTREAM"}
assert set(x["kind"] for x in c) == {
    "CODE_MODULE", "TEST_SOURCE",
    "HISTORICAL_IMPLEMENTER_POINTER_NOT_VALIDATED_STRANDED",
    "SOURCE_BODY_INDEPENDENTLY_READ_AND_GIT_BLOB_VERIFIED",
    "POST_REWORK_DISTINCT_SOURCE_VERSION_OR_TEST",
}
assert Counter(x["kind"] for x in c) == {
    "CODE_MODULE": 61,
    "TEST_SOURCE": 56,
    "HISTORICAL_IMPLEMENTER_POINTER_NOT_VALIDATED_STRANDED": 98,
    "SOURCE_BODY_INDEPENDENTLY_READ_AND_GIT_BLOB_VERIFIED": 67,
    "POST_REWORK_DISTINCT_SOURCE_VERSION_OR_TEST": 18,
}
assert all(x["source_link"].startswith("https://github.com/maidiu/rawlsing/") for x in h)
assert all(x["source_link"].startswith("https://github.com/maidiu/rawlsing/") for x in q)
assert all(x["first_consumer_required"] for x in o)
assert len(source["source_files"]) == 5
mulch = json.loads((ROOT / "07_THEMATIC_PER_SOURCE_MULCH_COVERAGE_757.json").read_text())
assert mulch["counts"]["unique_source_slots"] == 757
assert mulch["counts"]["embedded_workstreams"] == 17
for kind, key, src_rows in (
    ("H", "H_original_ideation_first_pass", h),
    ("Q", "Q_original_questions_first_pass", q),
    ("OINDEX", "O_index_owner_first_pass", o),
    ("SOROKUDA", "SOROKUDA_code_source_first_pass", c),
):
    rows = mulch[key]
    assert len(rows) == len(src_rows), (kind, "MULCH_COUNT")
    assert [z["source_id"] for z in rows] == [z["id"] for z in src_rows], (kind, "LOSS_OR_REORDER")
    assert all(z["coverage"] and z.get("source_id") for z in rows)
assert paths["total_file_entries"] == sum(
    z["type"] == "file" for d in paths["directories"] for z in d.get("rows", [])
)
assert paths["total_file_entries"] == 227, paths["total_file_entries"]
assert paths["total_directory_entries"] == 25, paths["total_directory_entries"]
assert all(d.get("rows") and not d.get("error") for d in paths["directories"])

idea_numbers = [int(x) for x in re.findall(r"^\| NM-(\d{3}) \|", ideas, re.M)]
assert idea_numbers == list(range(1, 45)), idea_numbers
for excerpt in (
    "and then he cheated on mom", "and the", "the family has one",
    "MULCHINEERING", "I want *everything in one place*",
    "there are too many good ideas",
):
    assert excerpt in ideas, ("MISSING_USER_SOURCE_FRAGMENT", excerpt)

for leaf in (
    "00_START_HERE_TOTAL_SOROK_MULCH.md",
    "03_DIALECTICAL_CONSTITUTIVE_PRODUCT_SYNTHESIS.md",
    "05_CAPABILITY_OWNER_AND_FIRST_CONSUMER_CROSSWALK.md",
    "06_RECIPROCAL_MULCH_AND_NO_DROP_PROTOCOL.md",
):
    assert (ROOT / leaf).is_file(), leaf

print("SOURCE_IDENTITY_NO_DROP PASS: 144 + 190 + 123 + 300 = 757 raw records")
print("S0–S16 PASS: 17 original workstreams are INCLUDED in 144, not additional")
print("CURATED_DIRECTORY PASS: 227 files + 25 linked directories, scope explicitly limited")
print("USER_CONVERSATION PASS: NM-001 through NM-044 contiguous; exact latest source snippets preserved")
print("SOURCE_MULCH PASS: all 757 exact source identities have an explicitly scoped thematic/owner coverage row")
print("GRADE WARNING: SOURCEFREE/DOCUMENTARY, no native science, independent review or protected receiving")
sys.exit(0)
