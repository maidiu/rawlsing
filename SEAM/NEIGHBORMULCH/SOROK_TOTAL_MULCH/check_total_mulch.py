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
# ONE-HOUSE DOC CONSERVATION: 03 is fully reconstituted from two
# independently authored theory lineages and the executed R28 organism.
# Structural/semantic-marker evidence only: no claim of human science,
# full independent 197/104 conceptual adjudication or protected receiving.
theory = (ROOT / "03_DIALECTICAL_CONSTITUTIVE_PRODUCT_SYNTHESIS.md").read_text()
start = (ROOT / "00_START_HERE_TOTAL_SOROK_MULCH.md").read_text()
critique = (ROOT / "06_RECIPROCAL_MULCH_AND_NO_DROP_PROTOCOL.md").read_text()
crosswalk = (ROOT / "05_CAPABILITY_OWNER_AND_FIRST_CONSUMER_CROSSWALK.md").read_text()
heads = re.findall(r"^## ([IVX]+)\. ", theory, re.M)
assert heads == ["I","II","III","IV","V","VI","VII","VIII","IX",
                 "X","XI","XII","XIII","XIV","XV","XVI","XVII"], (
                 "ONE_HOUSE_CHAPTER_DISPLACEMENT",heads)
assert len(theory)>=68000 and "STAGING ONLY" not in theory
for phrase in (
    "ONE HOUSE", "two former theories", "same-SES", "YOUR RESOURCES",
    "NO_LAWFUL_HOMOLOGY", "Sabbath", "Mark 2:27", "firewood",
    "M0–M8", "relational_metabolism", "historical_self_organization",
    "R28", "628", "two-meal", "false", "Birkenstocks", "H0–H3",
    "Mechanism I", "Mechanism II", "Mechanism III", "MII", "MIII",
    "S0–S16", "C0–C12", "Q123", "messaging", "F1–F10",
    "RC1–RC6", "platform", "SES", "coincidence", "source"
):
    # Keep quality checks honest: verifying the claim is articulated cannot
    # prove the claim is correct or integrated in running source.
    assert phrase.casefold() in theory.casefold(), (
        "ONE_HOUSE_THEORY_SPECIFIC_OMISSION",phrase)
for i in range(1,11):
    assert ("**F"+str(i)+" " in crosswalk or "**F"+str(i)+" —" in crosswalk), (
        "LOST_OLD_03_EXECUTABLE_FALSIFIER",i)
for i in range(1,7):
    assert "**RC-"+str(i)+"**" in crosswalk, ("LOST_OBSERVER_FIRST_CONSUMER",i)
for i in range(1,9):
    assert "JH-"+str(i)+":" in crosswalk, ("MISSING_TWO_HOUSE_FIRST_CONSUMER",i)
for lo,hi in ((1,12),(13,26),(27,39),(40,52),(53,62),(63,86),
              (87,99),(100,116),(117,139),(140,163),(164,190)):
    assert f"H{lo:03d}–H{hi:03d}" in crosswalk, (
        "LOST_ORIGINAL_H_FAMILY_FALSIFIER",lo,hi)
assert "ONE FULLY REWRITTEN theory document" in start
assert "03 — The Dialectical Constitutive Person and Its Game" in start
assert "Mandatory WHOLE-THEORY replacement rule" in critique
assert "THEORY_MULCH_INCOMPLETE" in critique
for doc in (start,crosswalk,critique,theory):
    assert not re.search(r"\]\((?:10_OVERLAPPING|11_FIVE|12_HUMAN|13_TARGETED)[^)]+\)",doc), (
        "DEAD_SATELLITE_LINK")

# The second house is preserved as provenance, not smuggled as another
# active theory. 104 cross-lineage propositions: C44 + NM44 + R9-16.
# 197 predecessor source/fate sections are preserved before retirement.
rival=ideas.split("## H. SECOND INDEPENDENT HOUSE:",1)[1]
rival_lineage=rival.split("### 197 source sections:",1)[1].split(
    "### 104 cross-lineage user/theory propositions",1)[0]
source_rows=re.findall(r"^\| R[^|]+-S\d+ \|",rival_lineage,re.M)
assert len(source_rows)==197, ("RIVAL_PREDECESSOR_SOURCE_LOSS",len(source_rows))
rival_propositions=rival.split("### 104 cross-lineage user/theory propositions",1)[1]
for prefix,count in (("C",44),("NM-",44),("R9-",16)):
    if prefix=="C":
        rows=re.findall(r"^\| C\d{2} \|",rival_propositions,re.M)
    elif prefix=="NM-":
        rows=re.findall(r"^\| NM-\d{3} \|",rival_propositions,re.M)
    else:
        rows=re.findall(r"^\| R9-\d{2} \|",rival_propositions,re.M)
    assert len(rows)==count, ("RIVAL_ORIGINAL_PROPOSITION_LOSS",prefix,len(rows))
assert "original user" in ideas.casefold()
assert "ONE-HOUSE JOINED FIRST-CONSUMER" in crosswalk

# Terminal cleanup gate: the source essays were intermediate material for
# the whole-theory rewrite, not permanent documents. Keep the actual original
# H/Q/O/SOROKUDA source atlas, 04 verbatim and 05 courts.
superseded = (
    "03_FULL_REWRITE_STAGING_TEMPORARY.md",
    "10_OVERLAPPING_DIALECTICAL_FIELDS_AND_INFANT_WORLD_RIFF_20261121.md",
    "11_FIVE_UNDERINTEGRATED_BACK_CATALOGUE_DISCOVERIES_AND_MULCH.md",
    "12_HUMAN_VALUE_EXTERNALIZATION_FETISH_RELIGION_MARKET_AND_PROPHETIC_REORIENTATION_20261121.md",
    "13_TARGETED_MULCHINEERING_RECIPROCAL_ATTENTION_AND_FALSE_INFERENCE_INTAKE_20261121.md",
)
for leaf in superseded:
    assert not (ROOT / leaf).exists(), ("SUPERSEDED_THEORY_STILL_LIVE", leaf)
assert [z.name for z in ROOT.glob("03_*.md")] == [
    "03_DIALECTICAL_CONSTITUTIVE_PRODUCT_SYNTHESIS.md"
], "PARALLEL_03_THEORY_FOUND"
original_g1 = ideas.split("### G1. Overlapping dialectical fields")[1].split(
    "### G2. Marxian human value")[0]
original_g2 = ideas.split("### G2. Marxian human value")[1].split(
    "**No-drop:**")[0]
assert len(original_g1) > 3079 and len(original_g2) > 4096, "VERBATIM_USER_QUOTE_LOST"
assert not re.search(
    r"\]\((?:10_OVERLAPPING|11_FIVE|12_HUMAN|13_TARGETED)[^)]+\)",
    ideas), "BROKEN_VERBATIM_SOURCE_LINK"

print("SOURCE_IDENTITY_NO_DROP PASS: 144 + 190 + 123 + 300 = 757 raw records")
print("S0–S16 PASS: 17 original workstreams are INCLUDED in 144, not additional")
print("CURATED_DIRECTORY PASS: 227 files + 25 linked directories, scope explicitly limited")
print("USER_CONVERSATION PASS: NM-001 through NM-085 contiguous; exact latest source snippets preserved")
print("SELECTED_TREES PASS: 242 original + 78 SEAM + 54 protected = 374 exact file records; 372 distinct paths")
print("SOURCE_MULCH PASS: all 757 exact source identities have an explicitly scoped thematic/owner coverage row")
print("ONE_HOUSE_RECONSTITUTED_STRUCTURE_PASS: 17 chapters, two theory lineages represented, 104 original claims + 197 predecessor references in existing 04, original F1-F10/RC1-RC6 and new JH1-JH8 in existing 05; semantic and runtime claims NOT independently certified")
print("ONE_LIVING_03_NO_SATELLITES_PASS: staging and 10–13 deleted from active tree; 04 original quotes + 05 RC courts preserved")
print("GRADE WARNING: SOURCEFREE/DOCUMENTARY, no native science, independent review or protected receiving")
sys.exit(0)
