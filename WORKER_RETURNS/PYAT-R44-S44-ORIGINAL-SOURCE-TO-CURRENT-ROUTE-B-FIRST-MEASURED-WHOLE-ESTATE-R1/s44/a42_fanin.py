"""S44 fan-in: merge U43/B43/J42/F43 + the AS2B historical positive into A42."""
from __future__ import annotations

import json
import sys
from pathlib import Path

RETURN_ROOT = Path(__file__).resolve().parent.parent
if str(RETURN_ROOT) not in sys.path:
    sys.path.insert(0, str(RETURN_ROOT))

from frozen_a42.a42 import core as a42core  # noqa: E402
from s44 import handoff, historical  # noqa: E402

U43_DIR = "WORKER_RETURNS/PYAT-R43-U43-ORIGINAL35-PROSPECTIVE-WORKLOAD-R1"
B43_DIR = "WORKER_RETURNS/PYAT-R43-B43-SELECTED-ROUTE-B-ORIGINAL35-SOURCE-POSITIVE-ENDTOEND-R1"
J42_DIR = "WORKER_RETURNS/PYAT-R42-J42-COMPLETE-E41-W41-P41-ACTUAL-JOINT-PREV3-CONSUMER-R1"
F43_DIR = "WORKER_RETURNS/PYAT-R43-F43-SOURCE-QUALIFIED-OBJECTIVE-WORLD-R1"


def _receipt(rid, commit, claim, grade, *, waves=(), axes=(), gates=(),
             funcs=(), globals_=(), note="", unknown=None):
    return {
        "receipt_id": rid, "origin_commit": commit, "claim_id": claim, "grade": grade,
        "coverage": {"wave_ids": list(waves), "axis_ids": list(axes), "f_gate_ids": list(gates),
                     "functional_gates": list(funcs), "register_151_ids": [],
                     "ledger_101_ids": [], "global_relations": list(globals_),
                     "global_contributions": [], "occupancy_grain_note": note},
        "unknown_bounds": unknown or {},
        "currentness": {"archive_or_current": "CURRENT", "as_of": "2026-10-19T14:40:00-0400"},
    }


def s44_receipts(gp, hist):
    # Verify exact artifacts for each return (preimages).
    checks = {
        handoff.U43_COMMIT: [U43_DIR + "/B43_A42_HANDOFF.json",
                             U43_DIR + "/currently_permitted_native_manifests.json",
                             "rawlsing_next/pre553_issued_workload.py"],
        handoff.B43_COMMIT: [B43_DIR + "/00_RETURN.md", B43_DIR + "/b43/admission.py",
                             B43_DIR + "/evidence/logs/b43_four_edge_witness.json"],
        handoff.J42_COMMIT: [J42_DIR + "/00_RETURN.md", J42_DIR + "/evidence/j42-suite.xml",
                             J42_DIR + "/evidence/proof-gate-changed.json"],
        handoff.F43_COMMIT: [F43_DIR + "/00_RETURN.md", F43_DIR + "/A42_RECEIPT_BANK.json",
                             F43_DIR + "/a42_dependency_manifest.json"],
    }
    verified = {}
    for commit, paths in checks.items():
        verified[commit] = [gp.verify(commit, p) for p in paths]
    recs = [
        historical.a42_historical_receipt(hist),
        _receipt("U43-PROSPECTIVE-FRONTIER", handoff.U43_COMMIT,
                 "U43_PROSPECTIVE_FRONTIER_AND_AUTHENTICATED_INGRESS__NO_MEASURED_ORIGINAL",
                 "DEVELOPMENT_BLOCKER_WITH_NARROW_OWNER",
                 note="prospective frontier/ingress ready; original U/E_pre and runtime unissued"),
        _receipt("B43-SELECTED-B-FEEDER", handoff.B43_COMMIT,
                 "B43_SELECTED_B_FEEDER_AND_ISSUER_BOUND_ADMISSION__NO_GRANT",
                 "DEVELOPMENT_BLOCKER_WITH_NARROW_OWNER",
                 note="executable feeder + WG0L repairs; no source grant/stream"),
        _receipt("J42-JOINED-CONSUMER", handoff.J42_COMMIT,
                 "J42_E41_W41_P41_ACTUAL_JOINT_TEST_ONLY_CONSUMER",
                 "SOURCEFREE_INTEGRATED_POSITIVE", funcs=("F5", "F6", "F7", "F8"),
                 note="sourcefree same-source joined E04/P41 TEST_ONLY; not original source"),
        _receipt("F43-BOUNDED-WORLD", handoff.F43_COMMIT,
                 "F43_RETAINED_SOURCEFREE_STRUCTURAL_FIELD_TEMPORAL_BOUNDED",
                 "SOURCEFREE_INTEGRATED_POSITIVE", funcs=("F5", "F6", "F7"),
                 note="retained/sourcefree bounded F5/F6/F7 traces; no transport/measured pair"),
    ]
    return recs, {k: len(v) for k, v in verified.items()}


def run(gp):
    scope = a42core.load_scope(gp)
    a41 = a42core.a41_receipts_v2(gp)
    bank = json.loads((RETURN_ROOT / "frozen_a42" / "evidence" /
                       "r41_receipt_bank_v2.json").read_text())
    r41 = a42core.ingest_r41_bank(bank, gp, scope)
    hist = historical.verify_historical(gp)
    new, verified_counts = s44_receipts(gp, hist)
    w41reg = a42core.load_w41_register(gp)
    old_manifest = json.loads(gp.blob_at(
        a42core.A41_COMMIT, a42core.A41_DIR + "/estate_acceptance_manifest.json"))
    base = a42core.assess_v2(scope, a41 + r41, w41reg, old_manifest)
    after = a42core.assess_v2(scope, a41 + r41 + new, w41reg, old_manifest)
    delta = {
        "schema": "S44_A42_SOURCE_GRADE_DELTA@1",
        "base_a42": {"original_measured": base["verdict"]["original_measured_occupied_cells"],
                     "historical_or_retained": base["verdict"]["historical_or_retained_cells"],
                     "missing": base["verdict"]["missing_expected_cells"]},
        "after_s44": {"original_measured": after["verdict"]["original_measured_occupied_cells"],
                      "historical_or_retained": after["verdict"]["historical_or_retained_cells"],
                      "missing": after["verdict"]["missing_expected_cells"],
                      "functional_evidence_gates": after["verdict"].get("functional_evidence_gates")},
        "new_original_measured_cells": (after["verdict"]["original_measured_occupied_cells"]
                                        - base["verdict"]["original_measured_occupied_cells"]),
        "new_historical_cells": (after["verdict"]["historical_or_retained_cells"]
                                 - base["verdict"]["historical_or_retained_cells"]),
        "source_grant_present": False,
        "source_positive_state": "FIRST_ORIGINAL_CURRENT_B_MEASURED_NOT_YET_EARNED",
        "verified_artifact_counts": verified_counts,
        "note": ("AS2B LiTS-I is genuine historical original-source science at historical scope; "
                 "it is NOT current selected-B or original measured occupancy."),
    }
    return scope, hist, new, base, after, delta
