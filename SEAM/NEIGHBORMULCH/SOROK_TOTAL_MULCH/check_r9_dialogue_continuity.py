#!/usr/bin/env python3
"""Read-only conservation court for the ONE current NEIGHBOR theory file.

The inherited filename is deliberately unchanged to avoid a new file/checker.
Verifies the existing in-file source-conservation foundation against #1275
source records and the existing 104-bank. It does not certify semantic truth.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from collections import Counter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CURRENT = ROOT / "SOROK_PRODUCT_CONTROL_ROOM" / "NEIGHBORMULCH"
SHARED = ROOT / "SEAM" / "NEIGHBORMULCH"

WHOLE = CURRENT / "12_NEIGHBOR_THEORYMULCH_CURRENT.md"


def must(ok: bool, why: str):
    if not ok:
        raise AssertionError(why)


def lines_between(text: str, begin: str, end: str) -> str:
    a = text.find(begin)
    b = text.find(end, a + len(begin))
    must(a >= 0 and b > a, "missing in-document source family: " + begin)
    return text[a:b]


def table(text: str, matcher: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        m = re.match(r"^\| (" + matcher + r") \|", line)
        if not m:
            continue
        key = m.group(1)
        must(key not in result, "duplicated source identity: " + key)
        result[key] = line
    return result


def normalized(s: object) -> str:
    return re.sub(r"\s+", " ", str(s).replace("|", "/")).strip()


def check_exact_source_name(row: str, name: str, key: str):
    must(normalized(name) in normalized(row),
         "source identity preserved but original meaning/locator missing: " + key)


def main():
    whole = WHOLE.read_text(encoding="utf-8")
    original = json.loads((HERE / "07_THEMATIC_PER_SOURCE_MULCH_COVERAGE_757.json").read_text())
    prior = json.loads((HERE / "11_CROSS_LINEAGE_CONVERSATION_NO_DROP_UNION.json").read_text())
    main = whole.split("## SOURCE-CONSERVATION FOUNDATION —", 1)[0]

    acts = [int(i) for i in re.findall(r"(?m)^## (\d+)\. ", main)]
    must(acts == list(range(1, 24)), "current theory is not one 23-movement integrated whole")
    must("## 23. Historical inheritance without greenfield restoration" in main,
         "R22 mature HOME lost its explicit source-custody and scope movement")

    # Source families MUST live inside the SAME existing theory document.
    section_family = lines_between(
        whole, "### 197 source sections:", "### 104 cross-lineage")
    ideas_family = lines_between(
        whole, "### 104 cross-lineage", "### Original SOROK H001–H190:")
    h_family = lines_between(
        whole, "### Original SOROK H001–H190:", "### Original SOROK Q001–Q123:")
    q_family = lines_between(
        whole, "### Original SOROK Q001–Q123:", "### Original 144 O-Index")
    o_family = lines_between(
        whole, "### Original 144 O-Index", "### Original 300 SOROKUDA")
    uda_family = lines_between(
        whole, "### Original 300 SOROKUDA", "### Direct user corrections")

    section_rows = table(section_family, r"(?:R1_INITIAL|R1_CORRECTED|R[2-9])-S\d\d")
    require_versions = {
        "R1_INITIAL": 18, "R1_CORRECTED": 18,
        "R2": 16, "R3": 14, "R4": 16, "R5": 18,
        "R6": 19, "R7": 24, "R8": 29, "R9": 25,
    }
    actual_versions = Counter(k.split("-S")[0] for k in section_rows)
    must(dict(actual_versions) == require_versions,
         f"ten predecessor theory cuts/197 sections altered: {dict(actual_versions)}")
    must(len(section_rows) == 197, "historic R1–R9 section custody lost")

    ideas = table(ideas_family, r"(?:C\d\d|NM-\d\d\d|R9-\d\d)")
    must(len(ideas) == 104 and len(prior["rows"]) == 104,
         "104 directly source-banked conversation/idea identities lost")
    for record in prior["rows"]:
        k = record["id"]
        must(k in ideas, "lost user idea " + k)
        check_exact_source_name(ideas[k], record["proposition"], k)
        must(normalized(record["r9_disposition"]) in ideas[k],
             "original idea disposition missing: " + k)
        must(normalized(record.get("source", "")) in ideas[k],
             "source provenance was silently lost: " + k)

    h_rows = table(h_family, r"H\d\d\d")
    q_rows = table(q_family, r"Q-[A-Za-z0-9_-]+")
    o_rows = table(o_family, r"(?!ID\b)[A-Za-z][A-Za-z0-9_-]*")
    uda_rows = table(uda_family, r"SOROKUDA-[A-Za-z0-9_-]+")
    must(len(h_rows) == 190 and len(q_rows) == 123 and
         len(o_rows) == 144 and len(uda_rows) == 300,
         "original 757 H/Q/O/SOROKUDA identities are incomplete")

    for source_name, source_table, attr in [
        ("H_original_ideation_first_pass", h_rows, "original_claim"),
        ("Q_original_questions_first_pass", q_rows, "historical_question"),
        ("O_index_owner_first_pass", o_rows, "title"),
        ("SOROKUDA_code_source_first_pass", uda_rows,
         "module_or_historical_path"),
    ]:
        for record in original[source_name]:
            key = record["source_id"]
            must(key in source_table, "lost original identity: " + key)
            if source_name.startswith("H_"):
                # Both the original heading and its separate Claim paragraph
                # (where one existed) are now preserved in the single whole.
                check_exact_source_name(source_table[key], record[attr], key)
            elif source_name.startswith("SOROKUDA"):
                # Original source union deliberately includes 98 source-cut-only
                # entries, without a module path. Demand exact path where known,
                # otherwise preserve the actual cut; do NOT invent a locator.
                loc = record.get("module_or_historical_path")
                if loc:
                    check_exact_source_name(source_table[key], loc, key)
                elif record.get("source_cut"):
                    check_exact_source_name(
                        source_table[key], record["source_cut"], key)
                else:
                    must(key in source_table, "lost source-only code ID " + key)
            else:
                check_exact_source_name(source_table[key], record[attr], key)

    # R22 USER-CONTROLLING RECONSTITUTION:
    # Keep original source tables IN the unchanged HOME foundation, but route
    # provisional, early-only meta-product possibilities into exactly one
    # subordinate OUTSIDE-HOME bank. The older R9/R10/R11 paragraph-by-paragraph
    # word-for-word active-chapter requirements are historically wrong after
    # the user's explicit 2026-11-22 redirection.
    outside_path = CURRENT / "14_OUTSIDE_HOME_META_PREUX_AND_GREENFIELD_HOLD.md"
    must(outside_path.is_file(), "new R22 outside-HOME provenance bank missing")
    outside = outside_path.read_text(encoding="utf-8")
    start = (CURRENT / "00_START_HERE.md").read_text(encoding="utf-8")
    ledger = (CURRENT / "13_NEIGHBOR_THEORYMULCH_SOURCE_DRAW_LEDGER.md").read_text(encoding="utf-8")
    old_head = "c449dcd9ebdb9377a1910998cf279a886b2e120e"

    must(old_head in outside and old_head in ledger,
         "exact prior complete HOME not preserved in routing ledger")
    must("## N-T1 / Round Twenty-Two" in ledger,
         "R22 controlling user correction not recorded in cumulative ledger")
    must("14_OUTSIDE_HOME_META_PREUX_AND_GREENFIELD_HOLD.md" in start,
         "canonical entrance not updated to explain outside HOME")
    must("12_NEIGHBOR_THEORYMULCH_CURRENT.md" in start,
         "canonical current positive HOME lost from entrypoint")

    # The original literal complete speculative §§11 and 12 were moved as
    # primary historical evidence, NOT silently discarded. Their pre-R22
    # section titles and substantive source text must be in the outside bank.
    for phrase in (
        "### MOVED §11 / WHOLE",
        "## 11. The social entrance: invitation, warrant, shared origins",
        "### MOVED §12 / WHOLE",
        "## 12. The platform can mediate experience or exploit",
        "relational warrant", "one-for-one",
        "mutual-aid", "real-world donations",
        "time modes", "research", "monetization",
        "terminal/TI-84", "first dinner",
        "formal flourishing", "institution",
    ):
        must(phrase.lower() in outside.lower(),
             "source-grounded outside-HOME candidate lost: " + phrase)
    must("Source-conservation" in whole or "SOURCE-CONSERVATION" in whole,
         "original corpus no longer carried in one master source foundation")

    # The old cultural, material, phenomenal and psychological kernel remains
    # positively IN the HOME, but its center is a *person*, not the early
    # platform's growth strategy, institutional-transformation game or
    # self-assessment engine. This is a routing court, not philosophical proof.
    ux_hits = list(re.finditer(r"(?m)^## (\d+)\. ", main))
    ux_sections = {int(m.group(1)): main[m.start():(ux_hits[i+1].start() if i+1<len(ux_hits) else len(main))].lower()
                   for i, m in enumerate(ux_hits)}
    governing = {
        1: ("know someone", "independent"),
        2: ("first knock", "prelude", "already"),
        3: ("economic peer", "financial", "socioeconomic"),
        4: ("say, do and attend", "attempt", "world"),
        5: ("textual world", "attention", "perceptual"),
        6: ("day does not wait", "absence", "world"),
        7: ("door, message, absence", "messaging", "reachable"),
        8: ("misrecognized", "reciprocity", "interpretation"),
        9: ("social powers", "permission", "reachability"),
        10: ("relationship becomes specific", "score", "attachment"),
        11: ("another encounter possible", "introduction", "permission"),
        12: ("human can be affected", "diagnoses", "human"),
        13: ("generated by the day", "say, do and attend", "not"),
        14: ("difficult encounters", "refusal", "ordinary"),
        15: ("world history", "testimony", "object"),
        16: ("not ux's jurisdiction", "pyat", "person"),
        17: ("care and coercion", "labor", "care"),
        18: ("contradictory psyche", "soracle-co", "history"),
        19: ("objects, practices", "material", "meaning"),
        20: ("person rereads herself", "interpretation", "psyche"),
        21: ("coming to know someone whose life is not for you", "historically constituted", "ordinary"),
        22: ("encounter in one continuous motion", "independently", "human"),
        23: ("historical inheritance", "outside", "source"),
    }
    for chapter, phrases in governing.items():
        must(chapter in ux_sections, "missing reconstituted movement: " + str(chapter))
        for phrase in phrases:
            must(phrase in ux_sections[chapter],
                 f"mature encounter shard missing from movement {chapter}: {phrase}")

    # The rejected early source has *not* been restored as the governing game.
    for old_title in (
        "## 11. The social entrance: invitation, warrant",
        "## 12. The platform can mediate experience",
        "## 13. A first dinner teaches the whole",
        "## 21. The generative kernel is the increasingly capable encounter",
        "## 22. A human at the threshold of several independently becoming lives",
    ):
        must(old_title not in main,
             "an early/extraneous movement is still installed as controlling: "+old_title)
    for phrase in (
        "one historically constituted fictional Other",
        "actual human",
        "SORACLE-CO",
        "finite", "different", "permission", "misunderstanding",
        "no programmed moral destination",
        "ordinary", "consequences", "historical",
    ):
        must(phrase.lower() in main.lower(),
             "substantive mature first-consumer theory unexpectedly absent: " + phrase)
    must("source-conservation foundation" in main.lower(),
         "source and semantic authority distinction erased")

    # Original November 21 user's opposite (no additional documents) remains
    # literal in the immutable foundation. Latest November 22 explicitly
    # authorizes ONE subordinate outside bank, not a second positive theory.
    must("### November 21 direct user theoretical clarification" in whole,
         "November 21 correction not preserved verbatim")
    must("Nadia should only get *more* pulsatingly contradictorily alive" in whole,
         "November 21 irreducible contradiction correction lost")
    must("### November 21 — direct user NEIGHBOR-UX jurisdiction" in whole,
         "jurisdiction source lost from unchanged foundation")
    must("### UX-R10 / user correction — the philosophy must travel" in ledger,
         "previous user-philosophy correction not retained in ledger")
    for historical_source in (
        "dockets/D008_ADAPTIVE_PHENOMENAL_LENS_AND_USER_MODEL/",
        "dockets/D009_HUMAN_FACULTY_CAPABILITY_AUTHORITY_AND_TRANSPOSITION/",
        "dockets/D003_FLOURISHING_INDEPENDENT_OF_ATTACHMENT/",
        "101_BINDING_SURFACE_ACTOR_PHENOMENOLOGY_SEGREGATION_AND_TWO_CALL_RENDERING_R1.md",
        "ASTRA_NATIVE_GAMEPLAY_NECESSITY_SYNTHESIS_R1/",
    ):
        must(historical_source in ledger,
             "older exact-source court dropped in the reconstitution: " + historical_source)

    direct = whole.split("### Direct user corrections", 1)[1]
    must("### Governing latest direct user instructions" in direct,
         "latest direct user's one-document and no-branch instruction lost")
    must("I do not want you to craete new documents" in direct,
         "source user wording not preserved verbatim")
    must("HELD_MISSING_ORIGINAL_CHAT" in whole and
         "HELD_SEMANTIC_INDEPENDENCE" in whole,
         "independent evidence gap concealed")
    must("ONE existing canonical HOME in #1277" in whole or "existing draft PR #1277" in whole,
         "historical source custody lost its own one-HOME destination")

    print("[PASS] ONE UX-first 23-movement HOME, with source foundation IN THE SAME FILE")
    print("[PASS] R22 positive in-game UX reconstitution and separate meta-pre-UX/open-ideation custody")
    print("[PASS] SORACLE-NEIGHBOR-UX experiential authority distinct from SORACLE-CO psychic theory")
    print("[PASS] 197 source sections from 10 immutable predecessor cuts")
    print("[PASS] 104 distinct source-graded ideas and exact original propositions")
    print("[PASS] 190 H + 123 Q + 144 O + 300 SOROKUDA source identities and original text/path")
    print("[PASS] historical no-new-doc user source preserved; latest explicit one subordinate bank admitted")
    print("[PASS] mature encounter features in active HOME; unselected early mechanics preserved outside")
    print("[LIMIT] Structure/text/source custody; NOT independent full semantic proof, "
          "complete original chat transcript, live organism execution, or protected receiving")


if __name__ == "__main__":
    main()
