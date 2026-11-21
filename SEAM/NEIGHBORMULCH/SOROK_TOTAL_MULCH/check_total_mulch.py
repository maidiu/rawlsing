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
selected = json.loads((ROOT / "08_FULL_SELECTED_SOROK_AND_SEAM_SOURCE_TREE_374_FILES.json").read_text())
assert [z["files"] for z in selected["counts"]] == [242, 78, 54]
assert sum(z["files"] for z in selected["counts"]) == 374
assert selected["distinct_paths_across_all_cuts"] == 372
assert len(selected["file_records"]) == 374
assert len(selected["subdirectory_records"]) == 32
assert all(x["truncated"] is False for x in selected["source_cuts"])
assert all(row["path"] and row["sha"] and row["source_url"].startswith(
    "https://github.com/maidiu/rawlsing/blob/") for row in selected["file_records"])
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
assert idea_numbers == list(range(1, 86)), idea_numbers
# The exact originating user words from source essays that were deleted must
# survive in the EXISTING 04 source register, rather than permanent sub-essays.
for phrase in (
    "in a public forest with a borrowed axe",
    "value I created now lives inside the wood",
    "the Sabbath was made for man, not man for the Sabbath",
    "the free hand of the market",
    "is your brain falling out",
    "everything is a dialectic",
    "it needs to be modeled like many overlapping dialectics",
    "also, what I have just said is a riff",
):
    assert phrase in ideas, ("LOST_ORIGINAL_USER_SPEECH", phrase)
assert "### G1. Overlapping dialectical fields" in ideas
assert "### G2. Marxian human value" in ideas

# The specific six-case user MULCHINEERING ask belongs in EXISTING 05.
crosswalk = (ROOT / "05_CAPABILITY_OWNER_AND_FIRST_CONSUMER_CROSSWALK.md").read_text()
for phrase in (
    "IV-A. Explicit MULCHINEERING work item",
    "H053", "H059", "NEIGHBOR R2",
    "**RC-1**", "**RC-2**", "**RC-3**",
    "**RC-4**", "**RC-5**", "**RC-6**",
):
    assert phrase in crosswalk, ("LOST_GAZE_ENGINEERING_REQUIREMENT", phrase)

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

# An integrity guard against the concrete regression that occurred in this turn:
# old CI proved source custody while the designated living theory hub (03)
# was NOT revised by substantive new user/source arguments. This check
# establishes only that the source themes now appear IN the hub and 05/06;
# it cannot prove their intellectual adequacy or independent owner adoption.
theory = (ROOT / "03_DIALECTICAL_CONSTITUTIVE_PRODUCT_SYNTHESIS.md").read_text()
start = (ROOT / "00_START_HERE_TOTAL_SOROK_MULCH.md").read_text()
crosswalk = (ROOT / "05_CAPABILITY_OWNER_AND_FIRST_CONSUMER_CROSSWALK.md").read_text()
critique = (ROOT / "06_RECIPROCAL_MULCH_AND_NO_DROP_PROTOCOL.md").read_text()
# The central 03 was REWRITTEN as a complete 17-chapter theory, not
# appended with numbered rival essays; 00 points there, 04 preserves exact
# speech, 05 accepts first-consumer courts and 06 enforces full reconstitution.
theory = (ROOT / "03_DIALECTICAL_CONSTITUTIVE_PRODUCT_SYNTHESIS.md").read_text()
start = (ROOT / "00_START_HERE_TOTAL_SOROK_MULCH.md").read_text()
critique = (ROOT / "06_RECIPROCAL_MULCH_AND_NO_DROP_PROTOCOL.md").read_text()
heads = re.findall(r"^## ([IVX]+)\. ", theory, re.M)
assert heads == [
    "I","II","III","IV","V","VI","VII","VIII","IX","X",
    "XI","XII","XIII","XIV","XV","XVI","XVII"
], ("THEORY_NOT_FULLY_RECONSTITUTED", heads)
assert len(theory) >= 68000 and "STAGING ONLY" not in theory
for phrase in (
    "The object is neither a dialogue bot",
    "Material world, social reproduction",
    "infant activity and caregiver alterity",
    "Overlapping relational fields",
    "firewood",
    "fetishism, God and power",
    "the Sabbath was made for man, not man for the Sabbath",
    "relational_metabolism",
    "historical_self_organization",
    "M0",
    "M8",
    "Nadia sibling falsifier",
    "Birkenstocks",
    "H0–H3",
    "Mechanism I",
    "Mechanism II",
    "Mechanism III",
    "copy-on-write",
    "visitor's gaze",
    "World consequences without social recognition",
    "The player inhabits a world position",
    "homologous-peer",
    "The product itself is a social institution",
    "One continuing organism",
    "Falsification, not stage-show confirmation",
    "Open contradictions and the ongoing duty",
    "What conservation means here",
    "S0–S16",
    "C0–C12",
    "Q123",
):
    assert phrase.casefold() in theory.casefold(), ("RECONSTITUTED_THEORY_LOSS", phrase)
for i in range(1,11):
    assert ("**F" + str(i) + " " in theory or "**F" + str(i) + " —" in theory), ("MISSING_FALSIFIER", i)
for lo,hi in ((1,12),(13,26),(27,39),(40,52),(53,62),
              (63,86),(87,99),(100,116),(117,139),(140,163),(164,190)):
    assert f"H{lo:03d}–H{hi:03d}" in theory, ("H_SOURCE_FAMILY_NOT_MULCHED", lo, hi)
assert "ONE FULLY REWRITTEN theory document" in start
assert "03 — The Dialectical Constitutive Person and Its Game" in start
assert "Mandatory WHOLE-THEORY replacement rule" in critique
assert "THEORY_MULCH_INCOMPLETE" in critique
for doc in (start, crosswalk, critique, theory):
    assert not re.search(r"\]\((?:10_OVERLAPPING|11_FIVE|12_HUMAN|13_TARGETED)[^)]+\)", doc), "DEAD_SATELLITE_LINK"

print("SOURCE_IDENTITY_NO_DROP PASS: 144 + 190 + 123 + 300 = 757 raw records")
print("S0–S16 PASS: 17 original workstreams are INCLUDED in 144, not additional")
print("CURATED_DIRECTORY PASS: 227 files + 25 linked directories, scope explicitly limited")
print("USER_CONVERSATION PASS: NM-001 through NM-085 contiguous; exact latest source snippets preserved")
print("SELECTED_TREES PASS: 242 original + 78 SEAM + 54 protected = 374 exact file records; 372 distinct paths")
print("SOURCE_MULCH PASS: all 757 exact source identities have an explicitly scoped thematic/owner coverage row")
print("WHOLE_THEORY_RECONSTITUTION_DOC_COURT_PASS: 03 rebuilt in 17 chapters, 11 original H-source families, F1-F10 and 04/05/06 integrated; document-level checks, NOT independent philosophical/scientific certification")
print("GRADE WARNING: SOURCEFREE/DOCUMENTARY, no native science, independent review or protected receiving")
sys.exit(0)
