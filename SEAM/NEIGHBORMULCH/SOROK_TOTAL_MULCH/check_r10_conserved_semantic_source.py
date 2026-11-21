#!/usr/bin/env python3
"""Read-only continuity and source-custody court for the R10 NEIGHBOR candidate.

Establishes exact source-row custody, source-consistent counts, manually labeled
lineage routes, known historical retractions and active textual obligations.
It does NOT independently decide whether every historical idea has been correctly
integrated, execute the organism, or validate psychology / protected adoption.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
N = ROOT / "SOROK_PRODUCT_CONTROL_ROOM" / "NEIGHBORMULCH"
SHARED = ROOT / "SEAM" / "NEIGHBORMULCH"


def require(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)


def load(name: str):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def main() -> None:
    whole = (N / "12_NEIGHBOR_THEORYMULCH_CURRENT.md").read_text(encoding="utf-8")
    ledger = (N / "13_NEIGHBOR_THEORYMULCH_SOURCE_DRAW_LEDGER.md").read_text(encoding="utf-8")
    sections = [int(x) for x in re.findall(r"(?m)^## (\d+)\. ", whole)]
    require(sections == list(range(1, 38)), "R10 whole must have 37 consecutive, uniquely headed chapters")
    require("NEIGHBOR — ONE HISTORY, TWO HORIZONS" in whole, "single R10 whole title")
    require("N-T1 / ROUND TEN" in ledger, "complete R1–R10 source ledger not appended")
    require("N-T1 / Round Nine" in ledger and "N-T1 / Round 1" in ledger, "historical source ledger lost")

    prev = load("12_ALL_TEN_VERSIONED_WHOLE_THEORY_SECTION_FATES_R10.json")
    require(prev["counts"]["source_sections"] == 197 and len(prev["rows"]) == 197,
            "one of 197 prior theory sections missing")
    require(prev["counts"]["versions"] == 10 and len(prev["historical_versions"]) == 10,
            "one of ten historical whole versions missing")
    require(len({x["id"] for x in prev["rows"]}) == 197, "duplicate historical section identity")
    require(sum(v["section_rows"] for v in prev["historical_versions"]) == 197,
            "source version totals diverged")
    require("personally adjudicated" in prev["manual_reconciliation"],
            "unexamined automated regex route was reinstated")
    for x in prev["rows"]:
        require(x["source_heading"] and x["source_excerpt_open"], f"missing exact source evidence {x['id']}")
        require(x.get("mapping_method", "").startswith("INDIVIDUALLY_CURATED"),
                f"historical source route not source-curated {x['id']}")
        require(x.get("r10_claimed_sections"), f"missing theory route {x['id']}")
        require(all(i in sections for i in x["r10_claimed_sections"]),
                f"invalid R10 chapter route {x['id']}")
        require(x.get("review_grade", "").endswith("NOT_YET"), 
                f"overclaimed independent review {x['id']}")

    retractions = {x["id"]: x for x in prev["rows"]}
    for key in ["R8-S05", "R8-S08", "R8-S11", "R8-S12"]:
        require("SUPERSEDED_IN_PART" in retractions[key]["fate"],
                "missing newest user's contradiction disposition: " + key)
    require("NO_LAWFUL_HOMOLOGY" in whole, "portal nontranslation principle disappeared")
    require("ATTEND should reliably increase resolution" in whole, 
            "positive ATTEND rule disappeared")
    require("house and text" in whole.lower() or "house and messaging" in whole.lower(),
            "two legitimate communication modes collapsed")
    require("deletion/export" in whole, "actual user's data control rights disappeared")
    require("SAY, DO and ATTEND" in whole, "founding open-action user grammar disappeared")
    require("not an optimizer" in whole or "not a machine objective" in whole,
            "user desire vs world optimization collapsed")
    require("fictional prelude" in whole, "bounded entry consent disappeared")
    require("user-unaffected reference" in whole, "same-day independent reference idea disappeared")
    require("your own resources bar" in whole.lower() or "visitor's own resources bar" in whole.lower(),
            "own-only financial bar disappeared")

    union = load("13_CONVERSATION_AND_757_SOURCE_FATES_R10.json")
    old_user = load("11_CROSS_LINEAGE_CONVERSATION_NO_DROP_UNION.json")
    original = load("07_THEMATIC_PER_SOURCE_MULCH_COVERAGE_757.json")
    require(union["counts"]["user_source_records"] == 104 and
            union["counts"]["original_sorok_source_records"] == 757 and
            union["counts"]["total"] == 861, "861 overlapping source records were altered")
    require(len(union["user_rows"]) == 104 and len(union["original_sorok_rows"]) == 757,
            "cross-lineage item actually missing")
    require(len({x["id"] for x in union["user_rows"]}) == 104, "user source id duplicate")
    user_index = {x["id"]: x for x in old_user["rows"]}
    for row in union["user_rows"]:
        key = row["id"]
        require(key in user_index and row["proposition"] == user_index[key]["proposition"],
                "verbatim user-source identity/cell changed: " + key)
        require(row.get("r10_claimed_theory_sections"), "missing current user fate " + key)
    originals = {x["source_id"]: x for x in union["original_sorok_rows"]}
    require(len(originals) == 757, "duplicate original source identifier")
    for name, n in [("H_original_ideation_first_pass", 190),
                    ("Q_original_questions_first_pass", 123),
                    ("O_index_owner_first_pass", 144),
                    ("SOROKUDA_code_source_first_pass", 300)]:
        orig_rows = original[name]
        require(len(orig_rows) == n, "original source-family count failure " + name)
        for row in orig_rows:
            key = row["source_id"]
            require(key in originals and originals[key].get("r10_sections"),
                    "source-family identity or theory owner route missing: " + key)

    h = load("16_ORIGINAL_H190_FULL_PARAGRAPH_SOURCE_AND_R10_FATES.json")
    q = load("17_ORIGINAL_Q123_FULL_SOURCE_AND_R10_FATES.json")
    require(h["source_count"] == 190 and len(h["rows"]) == 190, "original H source paragraph loss")
    require(q["count"] == 123 and len(q["rows"]) == 123, "original Q row loss")
    require(h["explicit_claim_line_count"] + h["inherited_without_standalone_claim_count"] == 190,
            "invented or omitted original H Claim body")
    for row in h["rows"]:
        require(row["source_id"] in originals and row["original_full_section_body"],
                "missing exact original H paragraph " + row["source_id"])
        require(row["source_title"] == originals[row["source_id"]]["original_claim"],
                "H original source title altered " + row["source_id"])
    for row in q["rows"]:
        require(row["id"] in originals, "Q source identifier not original " + row["id"])
        require(row["question"] == originals[row["id"]]["historical_question"],
                "original Q question altered " + row["id"])
        require(row["exact_original_line_number"] >= 1, "Q original line proof absent")
    require("HOLD_MISSING_ORIGINAL" in (HERE / 
            "15_RECOVERED_HISTORICAL_CHAT_EVIDENCE_AND_SOURCE_GAPS_R10.md").read_text(),
            "absent original chat must never be called complete")

    entrypoints = [
        HERE / "00_START_HERE_TOTAL_SOROK_MULCH.md",
        SHARED / "00_READ_FIRST.md",
        N / "00_START_HERE.md",
        SHARED / "01_SHARED_SORACLE_CO_NEIGHBOR_MULCH_BANK.md",
    ]
    for path in entrypoints:
        text = path.read_text(encoding="utf-8")
        require("14_R10_HOSTILE_SEMANTIC_CONSERVATION_COURT.md" in text,
                "missing explicit current R10 source court pointer " + str(path))

    print("[PASS] 37 ordered single-current-R10 theory chapters")
    print("[PASS] 197 source-evidenced/manually-routed sections from ten Git versions")
    print("[PASS] 104 prior conversation identities + 757 exact SOROK source identities")
    print("[PASS] 190 original historical H paragraphs, 123 original Q full JSON rows")
    print("[PASS] R8 financial epistemic error and prelude overrestriction explicitly superseded")
    print("[PASS] recovered historical controls and four reciprocal entrypoints")
    print("[LIMIT] Documentary/custody verification only; no semantic independent G5, "
          "complete original ChatGPT transcript, integrated organism, or protected receiving")


if __name__ == "__main__":
    main()
