#!/usr/bin/env python3
"""Build the A42 R41 receipt bank with real Git preimages."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RETURN_ROOT = HERE.parent
sys.path.insert(0, str(RETURN_ROOT))
from frozen_a41.a41.gitpreimage import GitPreimage  # noqa: E402
from a42 import core  # noqa: E402

REPO = RETURN_ROOT.parents[1]
E41 = "WORKER_RETURNS/PYAT-R41-E41-FULL-EMPIRICAL-F1F4-COMPUTED-POSSIBILITY-R1"
W41 = "WORKER_RETURNS/PYAT-R41-W41-OBJECTIVE-WORLD-R1"
P41 = "WORKER_RETURNS/PYAT-R41-P41-GENERIC-PROGRESSIVE-N10E-N10W-SERVING-R1"

DECLS = [
    {
        "receipt_id": "E41-SOURCEFREE-INTEGRATED",
        "origin_commit": core.E41_COMMIT,
        "source_return": "E41",
        "claim_id": "E41_FULL_F1F4_31_OPS_18_N10E_SLICES_ORIGINAL_E04_CONSUMER",
        "grade": "SOURCEFREE_INTEGRATED_POSITIVE",
        "coverage": {
            "wave_ids": [], "axis_ids": [], "f_gate_ids": [],
            "functional_gates": ["F1", "F2", "F3", "F4"],
            "register_151_ids": [], "ledger_101_ids": [],
            "global_relations": [], "global_contributions": [],
            "occupancy_grain_note": ("SOURCEFREE 31/31 ops / 14 families / 18 N10E slices / "
                                     "original E04 consumer; occupies NO original35 wave cell"),
        },
        "downstream_consumer_read_refs": ["product.nonparent.consume"],
        "unknown_bounds": {"original_source_occupied_count": 0,
                           "authorized_original_reads_this_pass": 0,
                           "route_probability": None,
                           "held_original_scope": "UNISSUED_HELD"},
        "currentness": {"archive_or_current": "CURRENT", "as_of": "2026-10-19T10:00:00-0400"},
        "artifacts": [E41 + "/00_RETURN.md", E41 + "/artifacts/f1f4_coverage_ledger.json",
                      E41 + "/artifacts/computed_slice_evidence.json",
                      E41 + "/artifacts/slice_consumer_receipt.json",
                      E41 + "/frozen/expected_use_universe.json",
                      E41 + "/evidence/e41_junit.xml", E41 + "/evidence/proof_witness.json"],
    },
    {
        "receipt_id": "W41-RETAINED-GT2-J04",
        "origin_commit": core.W41_COMMIT,
        "source_return": "W41",
        "claim_id": "W41_RETAINED_GT2_J04_EXACT_LIMITED_STRUCTURAL_POSITIVES",
        "grade": "HISTORICAL_RETAINED_EVIDENCE",
        "coverage": {
            "wave_ids": ["SRC02"], "axis_ids": ["S25", "S26"], "f_gate_ids": ["F5"],
            "functional_gates": ["F5"],
            "register_151_ids": [], "ledger_101_ids": ["F05"],
            "global_relations": [], "global_contributions": [],
            "occupancy_grain_note": ("retained canonical-constructor replay: Afro R5 GT2 "
                                     "(19,210 denom, 36 cells) + J04 position; NOT a fresh "
                                     "source measurement; NOT all original35 F5"),
        },
        "downstream_consumer_read_refs": ["product.nonparent.consume"],
        "unknown_bounds": {"F5_scope": "EXACT_SCOPED_RETAINED_ONLY",
                           "all_original35_F5": "HELD",
                           "route_probability": None},
        "currentness": {"archive_or_current": "CURRENT", "as_of": "2026-10-19T10:00:00-0400"},
        "artifacts": [W41 + "/00_RETURN.md",
                      W41 + "/original35_world_eligibility_register.json",
                      W41 + "/field_forge_structural_product_refs.json",
                      W41 + "/evidence/proof_witness.json",
                      W41 + "/evidence/cold_replay.json",
                      W41 + "/P41_A41_HAND_BACK.json"],
    },
    {
        "receipt_id": "W41-SOURCEFREE-INTEGRATED",
        "origin_commit": core.W41_COMMIT,
        "source_return": "W41",
        "claim_id": "W41_SOURCEFREE_MULTIFIELD_TEMPORAL_84_VIEWS_F6_8_CASES_EE1_9_CASES",
        "grade": "SOURCEFREE_INTEGRATED_POSITIVE",
        "coverage": {
            "wave_ids": [], "axis_ids": [], "f_gate_ids": [],
            "functional_gates": ["F5", "F6", "F7"],
            "register_151_ids": [], "ledger_101_ids": [],
            "global_relations": [],
            "global_contributions": ["cross_family_F6", "temporal_F7"],
            "occupancy_grain_note": ("SOURCEFREE: 84 synthetic 7x3x4 views, F6M/F6P 8 cases, "
                                     "EE1 9 cases; F6 transport/join HELD; no measured F7 pair"),
        },
        "downstream_consumer_read_refs": ["product.nonparent.consume", "consume_f6m_evidence"],
        "unknown_bounds": {"uncovered_target_mass_W2": "1/4", "uncovered_target_mass_W3": "1/5",
                           "uncovered_target_mass_W7": "1/2",
                           "F6_N9_join": "HOLD_EXACT_F6_REAL_USE_AND_WORLD_PURPOSE_ADMISSION_REQUIRED",
                           "Ghana_measured_change": None,
                           "measured_pairs": [], "route_probability": None},
        "currentness": {"archive_or_current": "CURRENT", "as_of": "2026-10-19T10:00:00-0400"},
        "artifacts": [W41 + "/multifield_nonpooling_and_bounds_receipts.json",
                      W41 + "/measured_temporal_eligibility_and_method.json",
                      W41 + "/current_historical_asof_world_consumer_receipts.json",
                      W41 + "/evidence/proof_witness.json"],
    },
    {
        "receipt_id": "P41-SOURCEFREE-INTEGRATED",
        "origin_commit": core.P41_COMMIT,
        "source_return": "P41",
        "claim_id": "P41_GENERIC_PROGRESSIVE_N9_N10E_N10W_19_TRAJECTORIES",
        "grade": "SOURCEFREE_INTEGRATED_POSITIVE",
        "coverage": {
            "wave_ids": [], "axis_ids": [], "f_gate_ids": [],
            "functional_gates": ["F8"],
            "register_151_ids": [], "ledger_101_ids": [],
            "global_relations": [], "global_contributions": ["possibility_F8"],
            "occupancy_grain_note": ("SOURCEFREE generic N9/N10E/N10W service, 19 trajectories, "
                                     "actual original E04 + generic receiver; no global permission"),
        },
        "downstream_consumer_read_refs": ["product.nonparent.consume"],
        "unknown_bounds": {"N10W_global_installation": "NOT_CLAIMED",
                           "CONCEPTION_SCENARIO_PROPOSALS": "CONSUMER_PERMISSION_UNISSUED",
                           "route_probability": None},
        "currentness": {"archive_or_current": "CURRENT", "as_of": "2026-10-19T10:00:00-0400"},
        "artifacts": [P41 + "/00_RETURN.md",
                      P41 + "/computed_progressive_conditioning_receipts.json",
                      P41 + "/generic_consumer_values_read.json",
                      P41 + "/actor_firewall_receipt.json",
                      P41 + "/current_historical_serving_invalidation.json",
                      P41 + "/evidence/p41-suite.xml", P41 + "/evidence/proof-gate-changed.json"],
    },
]


def main():
    gp = GitPreimage(REPO)
    receipts = []
    for d in DECLS:
        arts = [gp.verify(d["origin_commit"], p) for p in d["artifacts"]]
        receipts.append({
            "schema": core.R41_SCHEMA, "receipt_id": d["receipt_id"],
            "origin_commit": d["origin_commit"], "source_return": d["source_return"],
            "claim_id": d["claim_id"], "grade": d["grade"], "coverage": d["coverage"],
            "downstream_consumer_read_refs": d["downstream_consumer_read_refs"],
            "unknown_bounds": d["unknown_bounds"], "currentness": d["currentness"],
            "artifacts": arts,
        })
    bank = {"schema": "A42_RECEIPT_BANK@2.0.0", "receipts": receipts,
            "note": "real R41 native returns at exact preimages; grades non-substitutable; J42 pending"}
    bank["bank_digest"] = hashlib.sha256(
        json.dumps(bank, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    scope = core.load_scope(gp)
    core.ingest_r41_bank(bank, gp, scope)
    out = RETURN_ROOT / "evidence" / "r41_receipt_bank_v2.json"
    out.write_text(json.dumps(bank, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"out": str(out), "receipts": len(receipts),
                      "bank_digest": bank["bank_digest"],
                      "grades": [r["grade"] for r in receipts]}, indent=2))


if __name__ == "__main__":
    main()
