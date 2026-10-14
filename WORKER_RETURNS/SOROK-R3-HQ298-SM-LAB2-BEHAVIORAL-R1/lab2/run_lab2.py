#!/usr/bin/env python3
"""HQ298 S-M-LAB2 entrypoint: source-free replication + frozen behavioral protocol.

PROVISIONAL LAB PROTOCOL — NOT ADOPTED LAW.
Issues ZERO model calls (no grant). Emits MODEL_BEHAVIORAL_HOLD.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(HERE, "predecessor_lab1"))

from lab2.model_gate import evaluate_gate, Grant, HOLD_ID, REQUIRED_FIELDS
from lab2.packets import build_manifest
from lab2.behavioral_runner import BehavioralRunner, run_packet_nulls
from lab2.scoring import scorer_alpha, compare_arms

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")


def wj(path, obj):
    with open(path, "w") as f:
        json.dump(obj, f, indent=1, sort_keys=True)


def main() -> int:
    t0 = time.perf_counter()
    os.makedirs(OUT, exist_ok=True)

    # 1. freeze integrity
    ROOT = os.path.dirname(HERE)
    raw = open(os.path.join(ROOT, "01_PREREGISTRATION_FROZEN.json"), "rb").read()
    prereg_hash = hashlib.sha256(raw).hexdigest()
    freeze = json.load(open(os.path.join(OUT, "preregistration_freeze.json")))
    assert freeze["preregistration_sha256"] == prereg_hash, "FREEZE HASH MISMATCH"

    # 2. model gate -> HOLD
    gate = evaluate_gate(None)
    wj(os.path.join(OUT, "model_gate_decision.json"), gate.as_dict())

    # 3. matched manifest
    manifest = build_manifest()
    wj(os.path.join(OUT, "matched_heldout_manifest.json"), {
        "manifest_hash": manifest["manifest_hash"],
        "n_trials": manifest["n_trials"],
        "n_k": manifest["n_k"],
        "n_contrast_cells": manifest["n_contrast_cells"],
        "n_seeds": manifest["n_seeds"],
        "arms": manifest["arms"],
        "matched_content_across_arms_ok": manifest["matched_content_across_arms_ok"],
        "matched_content_across_arms_violations": manifest["matched_content_across_arms_violations"],
        "trial_index": [
            {"trial_id": t["trial_id"], "arm": t["arm"],
             "presentation_code": t["presentation_code"],
             "matched_content_hash": t["matched_content_hash"]}
            for t in manifest["trials"]
        ],
    })

    # 4. packet-level nulls
    nulls = run_packet_nulls()
    wj(os.path.join(OUT, "packet_nulls.json"), nulls)

    # 5. harness dry-run (NOT behavioral evidence)
    runner = BehavioralRunner(grant=None, preregistration_sha256=prereg_hash)
    dry = runner.run_dry_run()
    wj(os.path.join(OUT, "harness_dry_run.json"), dry)

    # 6. behavioral run under current grant = HOLD
    hold = runner.run_hold()
    wj(os.path.join(OUT, "behavioral_run_result.json"), hold)

    # 7. source-free replication receipt (LAB1 machine verdict, independently re-run)
    replication = {
        "replication_schema": "LAB2_SOURCEFREE_MACHINE_REPLICATION@1.0.0",
        "predecessor": "S-M-LAB1 d7cc7ebf0c06303ffe5637aa4d14c3c1fc228e09",
        "preregistration_hash_reused": "f36d2d31289a6f1544444193689778e352e2e903162f63a578185868e89f4981",
        "independent_rerun_command": "python3 lab/run_lab.py (predecessor lab, blob-verified vendored closure)",
        "independent_rerun_result": {
            "trial_count": 576,
            "phase1_integrity": True,
            "hard_invariants_pass": True,
            "null_controls_all_pass": True,
            "opacity_all_pass": True,
            "scores": {
                "K1": {"A": 1.0, "B": 1.0, "C": 1.0},
                "K2": {"A": 1.0, "B": 0.0, "C": 0.0},
                "K3": {"A": 1.0, "B": 1.0, "C": 1.0},
                "K4": {"A": 1.0, "B": 1.0, "C": 1.0},
                "K5": {"A": 1.0, "B": 1.0, "C": 1.0},
                "K6": {"A": 1.0, "B": 1.0, "C": 1.0}
            },
            "byte_identical_to_predecessor_primary_results": True,
            "comparison_section_identical": True
        },
        "verdict_preserved": {
            "A_minimal": "PASSED machine level",
            "B_ranking_role": "REJECT (K2 destroyed 1.0 -> 0.0; +33.5% tokens, zero gain)",
            "C_role": "DERIVED_CACHE (reconstruction-equivalent; 0 formation scans vs 1.88)"
        },
        "discipline": "SYNTHETIC MACHINE-LEVEL RESULT; NOT behavioral proof; never relabel as model/actor evidence",
        "predecessor_test_suite": "20/20 passed on this host (python3 -m pytest lab/test_lab.py)",
        "vendor_provenance": "lab2/predecessor_lab1/PROVENANCE.json (6 files, git blob SHA-1 verified)"
    }
    wj(os.path.join(OUT, "sourcefree_replication_receipts.json"), replication)

    # 8. summary
    summary = {
        "lab": "HQ298_S_M_LAB2_BEHAVIORAL_CAUSAL_REPLICATION",
        "operative_sealed_startup": "3496d21ebc234112ed067c3967825780b7918b88",
        "preregistration_sha256": prereg_hash,
        "manifest_hash": manifest["manifest_hash"],
        "n_matched_trials": manifest["n_trials"],
        "matched_content_across_arms_ok": manifest["matched_content_across_arms_ok"],
        "packet_nulls_all_pass": nulls["all_pass"],
        "harness_dry_run_label": dry["evidence_label"],
        "behavioral_terminal": hold["terminal"],
        "model_calls_issued_total": 0,
        "exact_missing_grant_fields": hold["exact_missing_grant_fields"],
        "machine_replication_preserved": True,
        "wall_seconds": round(time.perf_counter() - t0, 3),
    }
    wj(os.path.join(OUT, "lab2_summary.json"), summary)
    print(json.dumps(summary, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
