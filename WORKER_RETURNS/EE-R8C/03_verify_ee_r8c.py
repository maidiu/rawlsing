#!/usr/bin/env python3
"""Structural verification for the EE-R8C governed blocker return."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def main() -> None:
    matrix = load("01_SOURCE_CANDIDATE_PREPARATION_MATRIX.json")
    receipt = load("02_VERIFICATION_RECEIPT.json")
    assert matrix["status"] == "BLOCKED__ALL_SIX_REQUIRED_PREPARATIONS_NOT_QUALIFIED"
    assert matrix["candidate_order"] == ["A", "B", "C"]
    assert matrix["universe_order"] == ["WVS7", "LiTS-I"]
    assert len(matrix["cells"]) == 6
    assert [
        (cell["universe"], cell["candidate"])
        for cell in matrix["cells"]
    ] == [
        ("WVS7", "A"), ("WVS7", "B"), ("WVS7", "C"),
        ("LiTS-I", "A"), ("LiTS-I", "B"), ("LiTS-I", "C"),
    ]
    assert all(cell["status"] == "BLOCKED" for cell in matrix["cells"])
    assert matrix["smallest_frozen_order_blocker"] == "R8C-WVS7-A-R5-COMPACT-CARRIER"
    assert receipt["sources"]["WVS7"]["sha256"] == matrix["source_identities"]["WVS7"]["sha256"]
    assert receipt["sources"]["LiTS-I"]["sha256"] == matrix["source_identities"]["LiTS-I"]["sha256"]
    probe = receipt["direct_declared_dependency_probe"]
    assert probe["chunks"]["concatenated_modulo_4"] == 1
    assert probe["mandatory_strict_decode"] == "binascii.Error: Excess data after padding"
    assert receipt["execution"] == {
        "owner_executor_implemented": False,
        "candidate_processes_launched": 0,
        "source_decodes_for_bakeoff": 0,
        "partial_bakeoff": False,
        "semantic_parity": "NOT_RUN",
        "identity_parity": "NOT_RUN",
        "lifecycle_replay": "NOT_RUN",
        "frozen_telemetry_vectors": 0,
        "ranking_or_policy_decision": False,
    }
    print("PASS__EE_R8C_BLOCKER_RETURN_STRUCTURALLY_VERIFIED")


if __name__ == "__main__":
    main()
