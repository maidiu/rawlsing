from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

import receiving_preflight as preflight


HERE = Path(__file__).resolve().parent
ALLOWLIST = json.loads(
    (HERE / "EXACT_PATCH_PATH_AND_BLOB_ALLOWLIST.json").read_text(encoding="utf-8")
)
REVIEWER_SHA = {
    "g1_e4f_d02": "1111111111111111111111111111111111111111",
    "g2_e5_s06g": "2222222222222222222222222222222222222222",
}


def make_observed(premain_head=None):
    observed = {
        "premain_head": premain_head or ALLOWLIST["premain_pin"],
        "candidates": {},
    }
    for gate_id, gate in ALLOWLIST["gates"].items():
        changed = [item["path"] for item in gate["payload"]]
        changed.extend(prefix + "evidence.md" for prefix in gate["branch_evidence_prefixes"])
        observed["candidates"][gate_id] = {
            "sha": gate["candidate_sha"],
            "changed": changed,
            "payload_blobs": {
                item["path"]: {"before": item["before_blob"], "after": item["after_blob"]}
                for item in gate["payload"]
            },
            "reviewer_sha": REVIEWER_SHA[gate_id],
            "reviewer_receipt_present": True,
        }
    return observed


def make_receipts(gates=("g1_e4f_d02", "g2_e5_s06g")):
    receipts = {"schema": "PYAT_RRIF_F0_RECEIPTS@1.0.0", "receipts": {}}
    for gate_id in gates:
        gate = ALLOWLIST["gates"][gate_id]
        entry = {
            "review": {
                "verdict": gate["review_verdict_required"],
                "reviewed_sha": gate["candidate_sha"],
                "reviewer_branch": gate["review_branch"],
                "reviewer_sha": REVIEWER_SHA[gate_id],
                "receipt_path": gate["review_receipt_path"],
                "reviewer_distinct_from_author": True,
            },
            "tests": copy.deepcopy(gate["required_test_receipts"]),
        }
        if "owner_decision_required" in gate:
            spec = gate["owner_decision_required"]
            entry["owner_decision"] = {
                "decision": spec["decision_values_allowing_accept"][0],
                "reviewed_sha": gate["candidate_sha"],
                "conflict_tests": list(spec["exact_conflict_tests"]),
                "owner": "original-M2-owner",
                "decision_ref": "OWNER-M2-FIXTURE-AMENDMENT-1",
            }
        receipts["receipts"][gate_id] = entry
    return receipts


def test_pending_state_blocks_both_gates_and_selects_nothing():
    decision = preflight.evaluate_receiving(
        ALLOWLIST, {"receipts": {}}, make_observed()
    )
    assert decision["receiving_ready"] is False
    assert decision["selectable_payload"] == []
    assert decision["gates"]["g1_e4f_d02"]["status"] == "BLOCKED"
    assert decision["gates"]["g2_e5_s06g"]["status"] == "BLOCKED"
    assert "MISSING_EXACT_INDEPENDENT_REVIEW_RECEIPT" in decision["gates"]["g1_e4f_d02"]["blockers"]
    assert "MISSING_M2_OWNER_COMPATIBILITY_DECISION" in decision["gates"]["g2_e5_s06g"]["blockers"]


def test_e4f_gate_can_become_selectable_without_selecting_e5():
    decision = preflight.evaluate_receiving(
        ALLOWLIST, make_receipts(("g1_e4f_d02",)), make_observed()
    )
    assert decision["receiving_ready"] is False
    assert decision["gates"]["g1_e4f_d02"]["selectable"] is True
    assert decision["gates"]["g2_e5_s06g"]["selectable"] is False
    assert all(path.startswith(("rawlsing_next/pre553_physical_decoder",
                                "rawlsing_next/pre553_r5_codec",
                                "rawlsing_next/tests/test_rrif_e1_c3",
                                "rawlsing_next/tests/test_rrif_e4f"))
               for path in decision["selectable_payload"])


def test_both_gates_selectable_only_with_full_e4fr_e6_and_m2_owner_receipts():
    decision = preflight.evaluate_receiving(
        ALLOWLIST, make_receipts(), make_observed()
    )
    assert decision["receiving_ready"] is True
    assert decision["gates"]["g1_e4f_d02"]["selectable"] is True
    assert decision["gates"]["g2_e5_s06g"]["selectable"] is True
    assert len(decision["selectable_payload"]) == 12


def test_changed_premain_head_fails_closed():
    decision = preflight.evaluate_receiving(
        ALLOWLIST, make_receipts(), make_observed(premain_head="f" * 40)
    )
    assert decision["receiving_ready"] is False
    assert decision["selectable_payload"] == []
    assert "PREMAIN_HEAD_CHANGED_OR_MISMATCH" in decision["blockers"]


def test_wrong_after_blob_fails_closed():
    observed = make_observed()
    observed["candidates"]["g1_e4f_d02"]["payload_blobs"]["rawlsing_next/pre553_r5_codec.py"]["after"] = "0" * 40
    decision = preflight.evaluate_receiving(ALLOWLIST, make_receipts(), observed)
    assert decision["gates"]["g1_e4f_d02"]["selectable"] is False
    assert any("AFTER_BLOB_MISMATCH" in b for b in decision["gates"]["g1_e4f_d02"]["blockers"])


def test_changed_path_outside_allowlist_fails_closed():
    observed = make_observed()
    observed["candidates"]["g1_e4f_d02"]["changed"].append("rawlsing_next/unallowed_production.py")
    decision = preflight.evaluate_receiving(ALLOWLIST, make_receipts(), observed)
    assert decision["gates"]["g1_e4f_d02"]["selectable"] is False
    assert any("CHANGED_PATH_OUTSIDE_ALLOWLIST" in b for b in decision["gates"]["g1_e4f_d02"]["blockers"])


def test_payload_collision_fails_closed():
    allowlist = copy.deepcopy(ALLOWLIST)
    duplicate = copy.deepcopy(allowlist["gates"]["g2_e5_s06g"]["payload"][0])
    allowlist["gates"]["g1_e4f_d02"]["payload"].append(duplicate)
    observed = make_observed()
    observed["candidates"]["g1_e4f_d02"]["payload_blobs"][duplicate["path"]] = {
        "before": duplicate["before_blob"], "after": duplicate["after_blob"],
    }
    decision = preflight.evaluate_receiving(allowlist, make_receipts(), observed)
    assert decision["receiving_ready"] is False
    assert any("PAYLOAD_COLLISION" in b for b in decision["blockers"])


def test_e5_without_owner_decision_stays_blocked():
    receipts = make_receipts()
    receipts["receipts"]["g2_e5_s06g"].pop("owner_decision")
    decision = preflight.evaluate_receiving(ALLOWLIST, receipts, make_observed())
    assert decision["gates"]["g2_e5_s06g"]["selectable"] is False
    assert "MISSING_M2_OWNER_COMPATIBILITY_DECISION" in decision["gates"]["g2_e5_s06g"]["blockers"]


def test_e5_owner_decision_must_bind_both_exact_conflicts():
    receipts = make_receipts()
    receipts["receipts"]["g2_e5_s06g"]["owner_decision"]["conflict_tests"] = [
        "test_17_binding_cannot_resolve_different_release"
    ]
    decision = preflight.evaluate_receiving(ALLOWLIST, receipts, make_observed())
    assert decision["gates"]["g2_e5_s06g"]["selectable"] is False
    assert any("CONFLICT_TEST_SET_MISMATCH" in b for b in decision["gates"]["g2_e5_s06g"]["blockers"])


def test_e5_filtered_selection_cannot_be_claimed_green():
    receipts = make_receipts()
    receipts["receipts"]["g2_e5_s06g"]["tests"]["filtered_selection"]["status"] = "PASS"
    decision = preflight.evaluate_receiving(ALLOWLIST, receipts, make_observed())
    assert decision["gates"]["g2_e5_s06g"]["selectable"] is False
    assert any("SELECTION_NOT_GREEN" in b for b in decision["gates"]["g2_e5_s06g"]["blockers"])


def test_review_must_bind_exact_candidate_sha_and_distinct_reviewer():
    receipts = make_receipts()
    receipts["receipts"]["g1_e4f_d02"]["review"]["reviewed_sha"] = "0" * 40
    receipts["receipts"]["g1_e4f_d02"]["review"]["reviewer_distinct_from_author"] = False
    decision = preflight.evaluate_receiving(ALLOWLIST, receipts, make_observed())
    blockers = decision["gates"]["g1_e4f_d02"]["blockers"]
    assert any("REVIEW_DOES_NOT_BIND_EXACT_CANDIDATE_SHA" in b for b in blockers)
    assert any("REVIEWER_NOT_DISTINCT_FROM_AUTHOR" in b for b in blockers)


def test_reviewer_branch_still_at_premain_refuses_even_with_claimed_receipts():
    observed = make_observed()
    observed["candidates"]["g1_e4f_d02"]["reviewer_sha"] = ALLOWLIST["premain_pin"]
    decision = preflight.evaluate_receiving(ALLOWLIST, make_receipts(), observed)
    assert decision["gates"]["g1_e4f_d02"]["selectable"] is False
    assert any("REVIEWER_BRANCH_STILL_AT_PREMAIN" in b for b in decision["gates"]["g1_e4f_d02"]["blockers"])

def test_live_reviewer_receipt_absence_fails_closed():
    observed = make_observed()
    observed["candidates"]["g1_e4f_d02"]["reviewer_receipt_present"] = False
    decision = preflight.evaluate_receiving(ALLOWLIST, make_receipts(), observed)
    assert decision["gates"]["g1_e4f_d02"]["selectable"] is False
    assert any(
        "REVIEW_RECEIPT_NOT_PRESENT_AT_LIVE_REVIEWER_SHA" in b
        for b in decision["gates"]["g1_e4f_d02"]["blockers"]
    )


def test_receipt_path_must_match_declared_reviewer_receipt():
    receipts = make_receipts()
    receipts["receipts"]["g1_e4f_d02"]["review"]["receipt_path"] = "WORKER_RETURNS/other/review.md"
    decision = preflight.evaluate_receiving(ALLOWLIST, receipts, make_observed())
    assert decision["gates"]["g1_e4f_d02"]["selectable"] is False
    assert any("REVIEW_RECEIPT_PATH_MISMATCH" in b for b in decision["gates"]["g1_e4f_d02"]["blockers"])


def test_receipt_reviewer_sha_must_match_live_reviewer_branch():
    receipts = make_receipts()
    receipts["receipts"]["g1_e4f_d02"]["review"]["reviewer_sha"] = "0" * 40
    decision = preflight.evaluate_receiving(ALLOWLIST, receipts, make_observed())
    assert decision["gates"]["g1_e4f_d02"]["selectable"] is False
    assert any("REVIEWER_SHA_DOES_NOT_MATCH_LIVE_BRANCH" in b for b in decision["gates"]["g1_e4f_d02"]["blockers"])


def test_absent_reviewer_branch_refuses_even_with_claimed_receipts():
    observed = make_observed()
    observed["candidates"]["g1_e4f_d02"]["reviewer_sha"] = None
    observed["candidates"]["g1_e4f_d02"]["reviewer_receipt_present"] = False
    decision = preflight.evaluate_receiving(ALLOWLIST, make_receipts(), observed)
    assert decision["gates"]["g1_e4f_d02"]["selectable"] is False
    assert "REVIEWER_BRANCH_ABSENT" in decision["gates"]["g1_e4f_d02"]["blockers"]
