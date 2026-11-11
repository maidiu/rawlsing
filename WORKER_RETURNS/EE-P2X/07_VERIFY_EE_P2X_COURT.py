#!/usr/bin/env python3
"""Deterministic structural verifier for the bounded EE-P2X return."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).parent


def load(name: str) -> dict:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def sha(name: str) -> str:
    return hashlib.sha256((ROOT / name).read_bytes()).hexdigest()


def main() -> None:
    binding = load("00_EXECUTION_BINDING.json")
    a = load("01_LITS_I_A_FIRST_BUILD_STAGE.json")
    ab = load("02_LITS_I_A_TERMINAL_BINDING_BLOCKER.json")
    b = load("03_LITS_I_B_CACHELESS_C11_STAGE.json")
    bb = load("04_LITS_I_B_TERMINAL_BINDING_BLOCKER.json")
    c = load("05_LITS_I_C_TERMINAL_BINDING_BLOCKER.json")
    w = load("06_WVS7_COMMON_PREEXECUTION_AND_CANDIDATE_BLOCKERS.json")
    assert binding["source_order"] == ["LITS_I", "WVS7"]
    assert binding["candidate_order"] == ["A", "B", "C"]
    assert binding["lock2_hash"] == w["lock2"]["hash"]
    assert a["candidate"]["id"] == "A" and ab["candidate"]["id"] == "A"
    assert b["candidate"]["id"] == "B" and bb["candidate"]["id"] == "B"
    assert c["candidate"]["id"] == "C"
    assert b["identities"]["c11_logical_release"] == a["identity"]["c11_logical_release"]
    assert [x["candidate"] for x in w["ordered_candidate_cells"]] == ["A", "B", "C"]
    assert w["common_effects"]["ranking_or_selection"] is False
    print(json.dumps({
        "schema": "RAWLSING_EE_P2X_COURT_VERIFIER_RECEIPT@1.0.0",
        "status": "PASS__ORDER_LOCK_IDENTITIES_AND_NONADJUDICATION_BOUNDARY_VERIFIED",
        "return_file_sha256": {name: sha(name) for name in (
            "00_EXECUTION_BINDING.json", "01_LITS_I_A_FIRST_BUILD_STAGE.json",
            "02_LITS_I_A_TERMINAL_BINDING_BLOCKER.json", "03_LITS_I_B_CACHELESS_C11_STAGE.json",
            "04_LITS_I_B_TERMINAL_BINDING_BLOCKER.json", "05_LITS_I_C_TERMINAL_BINDING_BLOCKER.json",
            "06_WVS7_COMMON_PREEXECUTION_AND_CANDIDATE_BLOCKERS.json")},
        "ranking_or_selection": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
