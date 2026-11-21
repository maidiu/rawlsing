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
    must(acts == list(range(1, 18)), "current theory is not one 17-movement integrated whole")
    must("## 17. The game becomes serious where nobody can know what their action meant" in main,
         "whole lacks its reconstituted historical circuit")

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
        "untranslatable", "SAY, DO and ATTEND", "ATTEND",
        "bodily needs", "adult", "prelude", "source-root",
        "message", "deletion", "third", "ordinary",
        "source-qualified", "CONSTITUTIVE", "G4", "Mechanism",
        "God", "religious", "horizon", "relationship",
        "cannot comprehensively read", "public", "rent", "fallible",
    ]
    for phrase in important:
        must(phrase.lower() in main.lower(),
             "significant previously affirmed topic absent from active whole: " + phrase)

    # External #1278 reciprocal challenge: mere headings are insufficient;
    # retain a deliberately bounded negative vocabulary across the *active*
    # theory, not only the historical source foundation. This is text/source
    # custody, NOT an execution of observer-to-observer world/actor machinery.
    for phrase in (
        "misrecognized", "actor-local", "false belief",
        "human powers", "objectification", "institutional",
        "SAY plus covert ATTEND", "single world occurrence",
        "different sensory", "Nadia's belief",
        "no computationally preferred", "sourcefree",
        "same SES as Nadia", "YOUR RESOURCES", "message",
        "scarce Roll", "unvisited reference",
    ):
        must(phrase.lower() in main.lower(),
             "external reciprocal challenge unaccounted for: " + phrase)

    direct = whole.split("### Direct user corrections", 1)[1]
    must("### Governing latest direct user instructions" in direct,
         "latest direct user's one-document and no-branch instruction lost")
    must("I do not want you to craete new documents" in direct,
         "source user wording not preserved verbatim")
    must("HELD_MISSING_ORIGINAL_CHAT" in whole and
         "HELD_SEMANTIC_INDEPENDENCE" in whole,
         "independent evidence gap concealed")
    must("pre-existing file in the existing #1277 branch" in whole or "existing draft PR #1277" in whole,
         "current output does not identify its single existing destination")

    print("[PASS] ONE current integrated 17-movement whole, with source foundation IN THE SAME FILE")
    print("[PASS] 197 source sections from 10 immutable predecessor cuts")
    print("[PASS] 104 distinct source-graded ideas and exact original propositions")
    print("[PASS] 190 H + 123 Q + 144 O + 300 SOROKUDA source identities and original text/path")
    print("[PASS] current user no-new-document/no-new-branch instruction preserved as direct source")
    print("[PASS] named substantive positive ideas have actual passages in the whole")
    print("[LIMIT] Structure/text/source custody; NOT independent full semantic proof, "
          "complete original chat transcript, live organism execution, or protected receiving")


if __name__ == "__main__":
    main()
