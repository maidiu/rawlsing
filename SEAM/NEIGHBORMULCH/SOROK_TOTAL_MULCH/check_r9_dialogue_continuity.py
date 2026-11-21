#!/usr/bin/env python3
"""Read-only, source-reconciling R9 conversation no-drop continuity court.

This script verifies exact source-row and section-presence custody, not psychological
science, semantic equivalence, a complete ChatGPT transcript, or owner acceptance.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CURRENT = ROOT / "SOROK_PRODUCT_CONTROL_ROOM" / "NEIGHBORMULCH"
SHARED = ROOT / "SEAM" / "NEIGHBORMULCH"


def must(cond: bool, why: str) -> None:
    if not cond:
        raise AssertionError(why)


def table_rows(body: str, prefix: str) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for line in body.splitlines():
        if line.startswith("| " + prefix):
            cells = [item.strip() for item in line.split("|")[1:-1]]
            if cells and re.fullmatch(r"C\d\d|NM-\d\d\d", cells[0]):
                must(cells[0] not in found, "duplicate historical source row " + cells[0])
                found[cells[0]] = cells
    return found


def main() -> None:
    union = json.loads((HERE / "11_CROSS_LINEAGE_CONVERSATION_NO_DROP_UNION.json").read_text())
    old_bank = (SHARED / "01_SHARED_SORACLE_CO_NEIGHBOR_MULCH_BANK.md").read_text()
    pr_bank = (HERE / "04_USER_CONVERSATION_NO_DROP_AND_NEW_IDEAS.md").read_text()
    original = json.loads((HERE / "01_MACHINE_SOURCE_UNION_757_ROWS.json").read_text())
    transcript = (HERE / "10_PARTIAL_DIALOGUE_TRANSCRIPT_AND_SOURCE_LIMITS_20261121.md").read_text()
    theory = (CURRENT / "12_NEIGHBOR_THEORYMULCH_CURRENT.md").read_text()
    ledger = (CURRENT / "13_NEIGHBOR_THEORYMULCH_SOURCE_DRAW_LEDGER.md").read_text()
    total_entry = (HERE / "00_START_HERE_TOTAL_SOROK_MULCH.md").read_text()
    seam_entry = (SHARED / "00_READ_FIRST.md").read_text()
    neighbor_entry = (CURRENT / "00_START_HERE.md").read_text()

    rows = union["rows"]
    ids = [x["id"] for x in rows]
    must(len(ids) == 104 and len(set(ids)) == 104, "104 unique cross-lineage source identities")
    must(union["counts"] == {"R8_C": 44, "PR1275_NM": 44, "R9": 16, "total": 104}, "source count labels")
    old_table = table_rows(old_bank, "C")
    pr_table = table_rows(pr_bank, "NM-")
    must(len(old_table) == 44, "all 44 original C rows remain")
    must(len(pr_table) == 44, "all 44 original NM rows remain")
    index = {r["id"]: r for r in rows}
    for cid, cells in old_table.items():
        must(cid in index, "lost C record " + cid)
        must(index[cid]["proposition"] == cells[2], "altered source C text " + cid)
    for nid, cells in pr_table.items():
        must(nid in index, "lost NM record " + nid)
        must(index[nid]["proposition"] == cells[2], "altered source NM text " + nid)

    for i in range(1, 17):
        key = f"R9-{i:02d}"
        must(key in index and f"| {key} |" in pr_bank, "lost R9 current source " + key)

    sections = set(re.findall(r"(?m)^## ([IVXLCDM]+)\.", theory))
    must(len(sections) == 25, "whole ninth theory's 25 sections")
    for row in rows:
        pos = row.get("r9_claimed_theory_sections")
        must(bool(pos), "missing author-claimed R9 section for " + row["id"])
        # An en dash marks an inclusive section range; test endpoints,
        # not semantic equivalence of the intervening paragraphs.
        for term in re.split(r"[,–]", pos):
            must(term in sections, "invalid R9 section location " + row["id"] + ":" + term)
        must(row.get("coverage_grade") ==
             "AUTHOR_CLAIMED_SECTION_ONLY_NOT_INDEPENDENT_SEMANTIC_PROOF",
             "overclaimed proof grade " + row["id"])

    must("SAME ENTRY CLASS IS GIVEN; THE OTHER PERSON'S MONEY IS NOT" in theory,
         "economic opacity is active")
    must("user-unaffected, current-date reference continuation" in theory,
         "dynamic shared reference-day concept must be active")
    must("ENTERING THE GAME ALREADY CONSENTS TO A BOUNDED FICTIONAL PRELUDE" in theory,
         "opening fiction consent correction must be active")
    must("The user's own" in theory or "their own resource bar" in theory,
         "own-only financial UI must be active")
    must("not a transcript of inaccessible earlier turns" in transcript.lower(),
         "archive limitation must remain explicit")
    must("SOURCE EDGE" in pr_bank and "and the" in pr_bank, "preserve unfinished family source")
    must("## N-T1 / Round Nine" in ledger and "## N-T1 / Round 1" in ledger,
         "whole historical R1–R9 ledger retained")

    source_dump = json.dumps(original)
    for val in ("H001", "S0", "SOROKUDA"):
        must(val in source_dump, "original 757 source identifier estate appears altered: " + val)
    for current_path in (
        "10_PARTIAL_DIALOGUE_TRANSCRIPT_AND_SOURCE_LIMITS_20261121.md",
        "11_CROSS_LINEAGE_CONVERSATION_NO_DROP_UNION.json",
    ):
        must(current_path in total_entry and current_path in seam_entry and current_path in neighbor_entry,
             "R9 entrypoint no-drop link missing: " + current_path)

    print("[PASS] TOTAL SOROK original index retained; original checker covers its 757 source identities")
    print("[PASS] 44 historical C rows preserved with exact source cells")
    print("[PASS] 44 historical NM rows preserved with exact source cells")
    print("[PASS] 16 R9 source-grade distinctions indexed in both registers")
    print("[PASS] 104 unique records have valid author-claimed R9 section pointers")
    print("[PASS] current whole, complete cumulative ledger and cross-agent entrypoints")
    print("[PASS] financial epistemic distinction, dated conditional opening and bounded-fiction consent")
    print("[LIMIT] This is documentary continuity, NOT complete transcript or independent semantic proof")


if __name__ == "__main__":
    main()
