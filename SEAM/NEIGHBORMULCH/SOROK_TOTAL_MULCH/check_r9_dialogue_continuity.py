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
    must("## 23. Source-conservation, explicit alternatives, and what this HOME still does not settle" in main,
         "whole lacks its reconstituted source-accountable circuit")

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

    important = [
        "same SES", "YOUR RESOURCES", "financial",
        "no lawful counterpart", "SAY, DO and ATTEND", "ATTEND",
        "bodily needs", "adult", "prelude", "source-root",
        "message", "deletion", "third", "ordinary",
        "source-qualified", "CONSTITUTIVE", "PYAT", "historical",
        "God", "religious", "horizon", "relationship",
        "more contextual differentiation", "public", "rent", "fallible",
    ]
    for phrase in important:
        must(phrase.lower() in main.lower(),
             "significant previously affirmed topic absent from active whole: " + phrase)

    # External #1278 reciprocal challenge: mere headings are insufficient;
    # retain a deliberately bounded negative vocabulary across the *active*
    # theory, not only the historical source foundation. This is text/source
    # custody, NOT an execution of observer-to-observer world/actor machinery.
    for phrase in (
        "misrecognition", "actor-local", "false belief",
        "human powers", "objectification", "institutional",
        "cover remark", "world history",
        "perceptual availability", "Nadia can believe",
        "no computationally preferred", "source",
        "exactly Nadia's socioeconomic", "YOUR RESOURCES", "message",
        "scarce", "unvisited reference",
    ):
        must(phrase.lower() in main.lower(),
             "external reciprocal challenge unaccounted for: " + phrase)

    # R10 THEORY-CORPUS FUSION: each inherited source identity must be
    # accounted for within the currently active unified HOME; historical
    # R9 locations are not valid as current semantic pointers.
    for record in prior["rows"]:
        locations = record.get("fusion_home_sections", "")
        must(bool(locations), "missing current source-to-whole position: " + record["id"])
        for section_id in locations.split(","):
            must(section_id.isdigit() and int(section_id) in acts,
                 "invalid current section pointer: " + record["id"] + " -> " + section_id)
        must(record.get("fusion_coverage_grade") ==
             "AUTHOR_CLAIMED_CONCEPTUAL_PASSAGE_NOT_INDEPENDENT_SEMANTIC_PROOF",
             "overclaimed no-drop proof grade: " + record["id"])

    # These source-external concepts cut across the current HOME, not just its
    # conservation appendix; presence alone is NOT proof of semantic sufficiency.
    fused = (
        "constrained openness", "care", "self-myth", "reality pressure",
        "coherent", "contradiction", "ordinary", "time", "source-root",
        "material", "inhibitions", "unchosen", "no predetermined",
        "one-for-one", "non-possession", "deletion", "export",
        "privacy", "attention regime", "recognition", "testimony",
        "objectification", "institutions", "emotional",
        "no lawful counterpart", "human access invitation",
        "persona introduction", "family", "sibling",
        "pay", "rent", "initial entry", "world",
        "actor-local", "unvisited reference",
    )
    for phrase in fused:
        must(phrase.lower() in main.lower(),
             "cross-corpus generative concept absent from current whole: " + phrase)

    # Latest direct user MULCH correction: the kernel/axis must illuminate
    # *multiplying, historically generated contradiction*, not smoother
    # personality coherence or automatic resolution.
    must("### November 21 direct user theoretical clarification" in whole,
         "latest direct user theoretical correction not conserved verbatim")
    must("Nadia should only get *more* pulsatingly contradictorily alive" in whole,
         "latest direct user operative correction missing")
    for phrase in (
        "generative axes", "germinal relations",
        "more pulsatingly, specifically, multiply contradictory and alive",
        "more concrete and internally multiple",
        "contradictions acquire form, intensity, scale",
        "not to reduce complexity",
    ):
        must(phrase.lower() in main.lower(),
             "conceptual fusion still reduces Nadia's contradictions: " + phrase)

    # UX-FIRST SOURCE COURT: authenticated original UX phenomena must appear
    # inside the active one-HOME articulation, not only its source appendix.
    ux_hits = list(re.finditer(r"(?m)^## (\d+)\. ", main))
    ux_sections = {int(m.group(1)): main[m.start():(ux_hits[i+1].start() if i+1<len(ux_hits) else len(main))].lower() for i,m in enumerate(ux_hits)}
    ux_requirements = {
        1: ("the actual beginning is an invitation", "become neighbor", "first reward"),
        2: ("the ux question", "first screen", "first contact"),
        3: ("carry", "homologize", "bracket", "user-select", "habitus friction"),
        4: ("enter → reveal concrete affordances", "omission delegates", "fractions"),
        5: ("coarse shared gestalt", "attend", "recognition repertoire"),
        6: ("calendar", "read-but-unanswered", "meaningful new action"),
        7: ("terminal/ti-84", "outside", "messaging", "thread"),
        8: ("self-presentation is not self-verification", "becoming someone", "spectacle"),
        9: ("reachability", "route", "permission", "access can expand"),
        10: ("relational warrant", "progress", "moral score"),
        11: ("human access invitation", "credential", "persona", "commissioned roll"),
        12: ("optional reflection", "export", "privacy", "real human"),
        13: ("first-session sequence", "ordinary", "contact"),
        14: ("endogenous interpersonal difficulty", "guilt", "platform"),
        15: ("truth api", "public", "object"),
        16: ("private psychology", "pyat", "person"),
        17: ("care", "coercion"),
        18: ("soracle-co", "psyche"),
        19: ("objectification", "institution"),
        20: ("self-myth", "reread"),
        21: ("generative nucleus of the encounter", "history"),
        22: ("the experience in one uninterrupted line", "independently"),
    }
    for section, phrases in ux_requirements.items():
        for phrase in phrases:
            must(phrase in ux_sections[section], f"UX source shard missing in movement {section}: {phrase}")
    must("### November 21 — direct user NEIGHBOR-UX jurisdiction" in whole, "UX correction source missing")
    must("Jurisdiction and reciprocal horizon — NEIGHBOR-UX, not SORACLE-CO" in main, "UX ownership blurred")
    must("SORACLE-CO is the distinct theorist and authority" in main, "CO psyche owner distinction blurred")
    must("original sorok product and experiential courts" in main.lower(), "source UX court not grounded")

    # The real-visitor-formation requirement is CONSTITUTIVE UX THEORY:
    # psychological, historical-material, philosophical and theological
    # motives must travel through the encounter's design, not sit outside it.
    must("**The mechanics' constitutive reason.**" in main,
         "UX became a value-neutral action grammar")
    must("**The original philosophical and theological horizon remains part of the experience" in main,
         "theology/philosophy excluded from the UX generative center")
    formation_demands = {
        3: ("class transposition is an experiential intervention",
            "material equivalence"),
        4: ("action decompression has a philosophical task",
            "the human must actually think and act"),
        5: ("finite attention is an epistemology made bodily",
            "knowledge produces justice"),
        8: ("reciprocity is also the visitor's encounter with their own non-sovereignty",
            "formation through the other is not obedience"),
        10: ("the visitor's formation is similarly plural",
             "attachment, trust, health"),
        12: ("the platform's political economy is not external to the spiritual wager",
             "actual human"),
        21: ("why this is rawlsing ux and not merely a sophisticated story interface",
             "user-formation is a historically open possibility"),
    }
    for chapter, phrases in formation_demands.items():
        for phrase in phrases:
            must(phrase in ux_sections[chapter],
                 f"founding philosophy/user formation detached from movement {chapter}: {phrase}")
    ledger = (CURRENT / "13_NEIGHBOR_THEORYMULCH_SOURCE_DRAW_LEDGER.md").read_text(encoding="utf-8")
    must("### UX-R10 / user correction — the philosophy must travel" in ledger,
         "latest direct user philosophical-UX correction absent from existing ledger")

    # UX Round 11: demand the actual generative philosophical/experiential
    # collision at its source-bearing chapters, not a table of names or a
    # bolt-on summary. Textual coverage remains author-level, NOT independent
    # philosophical adjudication or executed person/world first consumer.
    round11 = {
        1: ("the original game-loop failure makes a philosophical demand",
            "several native scales"),
        3: ("the portal makes a difficult experiment",
            "lexical recognition, strategic signaling"),
        4: ("the distinction between demonstrated human faculty",
            "one may succeed through luck"),
        5: ("the phenomenal lens is the most dangerous instrument",
            "more faithful rendition of the user's eye"),
        6: ("historical hypercompression, high-intensity possibility",
            "no event consumes the person"),
        8: ("the reciprocal gaze becomes more serious",
            "no participant is exhausted"),
        10: ("the sharpest normative counterexample", "local norm"),
        11: ("shared-origin social play", "retro-resolved precontact canon"),
        12: ("a fourth party exists",
             "preserve relational history while minimizing the dossier"),
        13: ("one ordinary scene gives neighbor a dual obligation",
             "ontic flesh versus phenomenal flesh"),
        14: ("a lawful life includes event classes", "ordinary-life re-entry"),
        15: ("the world is answerable both backward",
             "backward continuity + forward binding"),
        16: ("the neighbor/co boundary should sharpen",),
        17: ("care and social reproduction are not moral abstractions",),
        19: ("the visitor meets not just private individuals",
             "objectification is ordinary historical life"),
        20: ("the right to interpret is distributed among persons",),
        21: ("the complete encounter is the historical development",
             "the philosophical and theological motive"),
        22: ("return to one ordinary evening",),
        23: ("round eleven / exact source-recovery correction",),
    }
    for section, terms in round11.items():
        for term in terms:
            must(term in ux_sections[section],
                 f"Round 11 NEGLECTED UX SOURCE absent from chapter {section}: {term}")
    must("## N-T1 / Round Eleven — THE LENS, THE OTHER, AND THE HISTORY IT CANNOT OWN" in ledger,
         "Round 11 exact-source provenance missing from existing ledger")
    for source in (
        "dockets/D008_ADAPTIVE_PHENOMENAL_LENS_AND_USER_MODEL/",
        "dockets/D009_HUMAN_FACULTY_CAPABILITY_AUTHORITY_AND_TRANSPOSITION/",
        "dockets/D003_FLOURISHING_INDEPENDENT_OF_ATTACHMENT/",
        "101_BINDING_SURFACE_ACTOR_PHENOMENOLOGY_SEGREGATION_AND_TWO_CALL_RENDERING_R1.md",
        "ASTRA_NATIVE_GAMEPLAY_NECESSITY_SYNTHESIS_R1/",
    ):
        must(source in ledger,
             f"Round 11 original UX source omitted from existing ledger: {source}")

    direct = whole.split("### Direct user corrections", 1)[1]
    must("### Governing latest direct user instructions" in direct,
         "latest direct user's one-document and no-branch instruction lost")
    must("I do not want you to craete new documents" in direct,
         "source user wording not preserved verbatim")
    must("HELD_MISSING_ORIGINAL_CHAT" in whole and
         "HELD_SEMANTIC_INDEPENDENCE" in whole,
         "independent evidence gap concealed")
    must("ONE existing canonical HOME in #1277" in whole or "existing draft PR #1277" in whole,
         "current output does not identify its single existing destination")

    print("[PASS] ONE UX-first 23-movement HOME, with source foundation IN THE SAME FILE")
    print("[PASS] UX court phenomena, action/attention/access, time/interface/first-session original theories mapped")
    print("[PASS] SORACLE-NEIGHBOR-UX experiential authority distinct from SORACLE-CO psychic theory")
    print("[PASS] 197 source sections from 10 immutable predecessor cuts")
    print("[PASS] 104 distinct source-graded ideas and exact original propositions")
    print("[PASS] 190 H + 123 Q + 144 O + 300 SOROKUDA source identities and original text/path")
    print("[PASS] current user no-new-document/no-new-branch instruction preserved as direct source")
    print("[PASS] named substantive positive ideas have actual passages in the whole")
    print("[LIMIT] Structure/text/source custody; NOT independent full semantic proof, "
          "complete original chat transcript, live organism execution, or protected receiving")


if __name__ == "__main__":
    main()
