#!/usr/bin/env python3
"""Read-only conservation court for the ONE current NEIGHBOR theory file.

The inherited filename is deliberately unchanged to avoid a new file/checker.
Verifies the existing in-file source-conservation foundation against #1275
source records and the existing 104-bank. It does not certify semantic truth.
"""
from __future__ import annotations

import json
import re
import hashlib
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
    # The historical foundation must be byte-exact, not merely count-correct.
    marker = "## SOURCE-CONSERVATION FOUNDATION — IN THIS DOCUMENT, NOT A COMPETING THEORY"
    must(whole.count(marker) == 1, "exact foundation marker not unique")
    main, suffix = whole.split(marker, 1)
    foundation = marker + suffix
    must(len(foundation) == 238941, "historical foundation length differs from frozen source")
    must(hashlib.sha256(foundation.encode("utf-8")).hexdigest()
         == "23a896874a157e6c361a0eea7589a7a806dec32a02f374e9303a4421fdb4f1db",
         "historical foundation SHA256 differs from exact predecessor")

    expected_chapters = {
        "I": "The wish to meet a person who was not made to meet you",
        "II": "A real human in a materially equal starting position, without a counterfeit childhood",
        "III": "The world is actual before attention; discovered facts are not invented causes",
        "IV": "An action has to occur: saying, doing, attending and the return of control",
        "V": "The textual surface gives finite experience, not a privileged explanation",
        "VI": "The Other is an active, contradictory organism, not the visible tip of a questionnaire",
        "VII": "One scene, several real centers: collective activity without a collective mind",
        "VIII": "The between: pleasurable companionship, learned practices and unequal psychic investment",
        "IX": "Knowing and becoming known: recursive models, self-giving and resistant evidence",
        "X": "Time and reachability: another life continues without making the visitor captive",
        "XI": "Care is material, affection is not vindication, and a difficult person need not be sanitized",
        "XII": "The past can be reread but not undone: memory, rupture and unfinished becoming",
        "XIII": "One lived movement; what may not be resolved for the sake of a finished theory",
    }
    chapters = list(re.finditer(r"(?m)^## ([IVX]+)\. ([^\n]+)$", main))
    must([m.group(1) for m in chapters] == list(expected_chapters),
         "promoted HOME not exactly thirteen ordered Roman movements")
    must([m.group(2) for m in chapters] == list(expected_chapters.values()),
         "reviewed 13-movement chapter identity changed without source reconciliation")
    must(not re.search(r"(?m)^## \d+\. ", main),
         "old 23-movement structure still active or mixed")
    must("Branch-local promotion only; protected receiving is still HELD" in main,
         "candidate falsely portrayed as independently accredited")
    must("4e5030e2c526e8491b2b77e005f3ec10bade8da5" in main,
         "exact predecessor Git blob custody lost")
    must(not (CURRENT / "15_NEIGHBOR_HOME_TOTAL_MULCH_CANDIDATE.md").exists(),
         "second positive theory still active after single-HOME replacement")

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

    # R35: preserve old addresses while making provisional current Roman
    # destinations inspectable under the EXISTING ledger/source identity bank.
    must("## N-T1 / Round Thirty-Five" in (CURRENT / "13_NEIGHBOR_THEORYMULCH_SOURCE_DRAW_LEDGER.md").read_text(encoding="utf-8"),
         "R35 source-location overlay missing from existing ledger")
    stage35 = (CURRENT / "13_NEIGHBOR_THEORYMULCH_SOURCE_DRAW_LEDGER.md").read_text(encoding="utf-8").split(
        "## N-T1 / Round Thirty-Five", 1)[1]
    must("### R35 / 197" in stage35 and "### R35 / 104" in stage35 and
         "### R35 / 757" in stage35, "source mapping family boundaries lost")
    current197 = stage35.split("### R35 / 197", 1)[1].split("### R35 / 104", 1)[0]
    current104 = stage35.split("### R35 / 104", 1)[1].split("### R35 / 757", 1)[0]
    # R35 overlays use Markdown code-spanned IDs; inherited foundation tables
    # intentionally use literal IDs. Parse each format without normalizing away
    # exact identities or weakening the set-equality checks below.
    route197, route104 = {}, {}
    for line in current197.splitlines():
        match = re.match(r"^\| `((?:R1_INITIAL|R1_CORRECTED|R[2-9])-S\d\d)` \|", line)
        if match:
            key = match.group(1)
            must(key not in route197, "duplicated current 197 locator " + key)
            route197[key] = line
    for line in current104.splitlines():
        match = re.match(r"^\| `((?:C\d\d|NM-\d\d\d|R9-\d\d))` \|", line)
        if match:
            key = match.group(1)
            must(key not in route104, "duplicated current 104 locator " + key)
            route104[key] = line
    must(set(route197) == set(section_rows) and len(route197) == 197,
         "R35 current 197 historical-section route coverage incomplete")
    must(set(route104) == set(ideas) and len(route104) == 104,
         "R35 current 104 original conversation/idea route coverage incomplete")
    permitted = set(expected_chapters)
    for key, row in route197.items():
        roman = re.findall(r"`([IVX]+)`", row)
        must(roman and all(v in permitted for v in roman),
             "historical theory source has no current Roman candidate: " + key)
        must("PROVISIONAL" in row, "R35 author candidate falsely upgraded: " + key)
    for key, row in route104.items():
        roman = re.findall(r"`([IVX]+)`", row)
        must((roman and all(v in permitted for v in roman)) or
             ("OUTSIDE-HOME" in row or "SOURCE_ONLY" in row),
             "original user idea lacks bounded in-game/outside/source-only disposition: " + key)
        must(any(status in row for status in
                 ("PROVISIONAL_SEMANTIC_DESTINATION", "SOURCE_ONLY")),
             "R35 idea location silently accredited: " + key)
    must("### Original SOROK H001–H190:" in whole and
         "### Original SOROK Q001–Q123:" in whole and
         "### Original 144 O-Index" in whole and
         "### Original 300 SOROKUDA" in whole,
         "757 original historical source-family locations lost from canonical file")

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

    # Source-conscious new thirteen-movement coverage, not old title token checks.
    chapter_text = {m.group(1): main[m.start():(chapters[i+1].start() if i+1 < len(chapters) else len(main))].lower()
                    for i, m in enumerate(chapters)}
    hard_shards = {
        "I": ("independent person", "invitation", "ordinary", "interest"),
        "II": ("socioeconomic", "your resources", "carry", "local body"),
        "III": ("not_materialized_yet", "counterfactual", "historical", "common root"),
        "IV": ("say, do and attend", "interrupted", "control", "actual"),
        "V": ("phenomenal surface", "observer", "accessibility", "attention"),
        "VI": ("constitution itself is relational", "pyat", "recruitment", "self"),
        "VII": ("polycentric", "conversational floor", "third party", "independent"),
        "VIII": ("cathexis", "companionship", "real humans", "shared"),
        "IX": ("model", "visitor", "self-knowledge", "recognition"),
        "X": ("calendar", "friday/saturday", "account control plane", "message"),
        "XI": ("care", "coercion", "flourishing", "material"),
        "XII": ("reinterpretation", "repair", "irreversible", "past"),
        "XIII": ("one lived movement", "history", "world", "visitor"),
    }
    for roman, shards in hard_shards.items():
        for shard in shards:
            must(shard in chapter_text[roman],
                 f"reviewed 13-movement source distinction missing from {roman}: {shard}")

    # R26 maps every original 23-movement paragraph to the proposed 13-movement
    # destination. Crosswalk presence does not confer semantic accreditation.
    must("## N-T1 / Round Twenty-Six" in ledger and
         "## N-T1 / Round Twenty-Seven" in ledger, "R26 crosswalk absent")
    crosswalk = ledger.split("## N-T1 / Round Twenty-Six", 1)[1].split(
        "## N-T1 / Round Twenty-Seven", 1)[0]
    src_rows = re.findall(r"(?m)^\| `(\d+\.\d+)` \| [^|\n]* \| ([^|\n]+) \|", crosswalk)
    must(len(src_rows) == 272, "R26 original-to-successor crosswalk lost 272 rows")
    seen_src, old_sections = set(), {}
    for source_id, destinations in src_rows:
        must(source_id not in seen_src, "duplicate crosswalk source: " + source_id)
        seen_src.add(source_id)
        old_chapter, old_paragraph = map(int, source_id.split("."))
        must(1 <= old_chapter <= 23 and old_paragraph >= 1, "bad old source ID")
        old_sections.setdefault(old_chapter, set()).add(old_paragraph)
        current = re.findall(r"`([IVX]+)`", destinations)
        must(current and all(d in chapter_text for d in current),
             "current Roman source locator missing for " + source_id)
    must(len(old_sections) == 23 and all(
         p == set(range(1, len(p)+1)) for p in old_sections.values()),
         "original 23-movement source paragraphs not preserved by row ID")

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
        "historically constituted fictional Other",
        "actual human",
        "Constitutive Organism",
        "finite", "different", "permission", "misunderstanding",
        "moralized score",
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
    must("12_NEIGHBOR_THEORYMULCH_CURRENT.md" in main and
         "4e5030e2c526e8491b2b77e005f3ec10bade8da5" in main and
         "DRAFT PR #1277" in main,
         "new one-HOME destination, exact prior blob or draft receiving grade missing")

    print("[PASS] ONE UX-first 13-movement HOME and SHA256-frozen 238941-character foundation IN SAME FILE")
    print("[PASS] R35 positive reconstitution with original R22 outside custody unchanged")
    print("[PASS] SORACLE-NEIGHBOR-UX experiential authority distinct from SORACLE-CO psychic theory")
    print("[PASS] 197 source sections from 10 immutable predecessor cuts")
    print("[PASS] 104 distinct source-graded ideas and exact original propositions")
    print("[PASS] 190 H + 123 Q + 144 O + 300 SOROKUDA source identities and original text/path")
    print("[PASS] historical no-new-doc user source preserved; latest explicit one subordinate bank admitted")
    print("[PASS] source-conscious 272-paragraph destination crosswalk and thirteen active chapters")
    print("[PASS] provisional 197/104 new Roman locators and 757 historic family locators preserved")
    print("[PASS] unselected early mechanics preserved outside HOME")
    print("[LIMIT] Structure/text/source custody; NOT independent full semantic proof, "
          "complete original chat transcript, live organism execution, or protected receiving")


if __name__ == "__main__":
    main()
