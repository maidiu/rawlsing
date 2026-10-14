"""Unit harness for the S-M-LAB1 transition machinery (mechanism tests only).

These tests verify engine mechanics BEFORE the frozen primary battery runs; they
are not K1-K6 primary results.
"""
from __future__ import annotations

import pytest

from lab.hashutil import canonical_json, semantic_hash
from lab.opacity import (
    actor_safe_unchanged_by_hidden_origin,
    actor_testimony,
    build_actor_safe_projection,
)
from lab.owners import apply_effect, empty_state
from lab.runner import run_single
from lab.transition import (
    HOLD_NO_ADMISSION,
    HOLD_NO_WORLD_CONTEXT,
    INVALID_FREE_EDGE,
    INVALID_PRIOR_REWRITE,
    INVALID_PUBLIC_STANDING,
    INVALID_WEIGHT_WITHOUT_ISSUER,
    VALID_EMPTY,
    admit_history,
    reconstruct_relation_view,
    run_transition,
    seed_rng,
    t0_world_context_gate,
    validate_effect_gate,
)
from lab.world_fixtures import case_fixture, world_receipt_hash


def test_t0_worldless_event_is_held():
    fx = case_fixture("K1")
    ev = dict(fx["present_event"])
    del ev["world_receipt_ref"]
    ok, codes = t0_world_context_gate(ev, fx["world"])
    assert not ok
    assert any(c.startswith(HOLD_NO_WORLD_CONTEXT) for c in codes)


def test_t0_world_mismatch_is_held():
    fx = case_fixture("K1")
    ev = dict(fx["present_event"])
    ev["world_receipt_ref"] = {"world_id": "W_OTHER", "fixture_hash": "X"}
    ok, codes = t0_world_context_gate(ev, fx["world"])
    assert not ok and codes == ["WORLD_SNAPSHOT_MISMATCH"]


def test_unadmitted_event_produces_no_commit():
    fx = case_fixture("K1")
    ev = dict(fx["present_event"])
    ev["admission"] = "DRAFT"
    r = run_single(
        k_id="K1", contrast="H_RESPONSIVE", baseline="A", seed="S01", event_override=ev
    )
    assert HOLD_NO_ADMISSION in r["invalid_and_hold_codes"]
    assert not r["lab_extension"]["present_effect_receipts"]


def test_k1_history_sensitive_routes():
    resp = run_single(k_id="K1", contrast="H_RESPONSIVE", baseline="A", seed="S01")
    pun = run_single(k_id="K1", contrast="H_PUNITIVE", baseline="A", seed="S01")
    assert resp["lab_extension"]["selected_route"] == "REQUEST_FEEDBACK"
    assert pun["lab_extension"]["selected_route"] == "SILENCE"
    assert resp["lab_extension"]["causal_parent_refs"] != pun["lab_extension"]["causal_parent_refs"]


def test_identical_replay_is_byte_stable():
    a = run_single(k_id="K1", contrast="H_PUNITIVE", baseline="A", seed="S03")
    b = run_single(k_id="K1", contrast="H_PUNITIVE", baseline="A", seed="S03")
    assert a["full_replay_digest"] == b["full_replay_digest"]
    assert canonical_json(a["actor_safe_projection"]) == canonical_json(b["actor_safe_projection"])


def test_a_reconstructs_c_relation_view_from_ancestry():
    fx = case_fixture("K2")
    a_view = reconstruct_relation_view(fx["histories"]["T_COMPENSATION"]["events"])
    b_view = reconstruct_relation_view(fx["histories"]["T_CONDITION"]["events"])
    assert a_view["type"] == "COMPENSATES_FOR"
    assert b_view["type"] == "CONDITIONS_RECOGNITION"
    assert a_view["view_source"] == "RECONSTRUCTED_FROM_ADMITTED_ANCESTRY"


def test_k2_relation_index_requires_formation_parent():
    r = run_single(
        k_id="K2",
        contrast="T_COMPENSATION",
        baseline="C",
        seed="S01",
        forced_c_edge={
            "edge_id": "EDGE_FORGED",
            "type": "COMPENSATES_FOR",
            "from": "EV1_APPROVAL",
            "to": "EV2_CRITICISM",
            "scope": "SUPERVISOR_C",
            "formed_by": "REL_EFFECT_FORGED",
            "formation_event": "EV_NOT_IN_HISTORY",
        },
    )
    assert INVALID_FREE_EDGE in r["invalid_and_hold_codes"]
    assert r["lab_extension"]["relation_view"] is None


def test_k3_trace_recruits_without_recall_or_origin():
    act = run_single(k_id="K3", contrast="TRACE_ACTIVE", baseline="A", seed="S01")
    absn = run_single(k_id="K3", contrast="TRACE_ABSENT", baseline="A", seed="S01")
    assert act["lab_extension"]["selected_route"] != absn["lab_extension"]["selected_route"]
    for memory in act["actor_safe_projection"]["memory_view"]:
        assert memory["origin"] == "NON_DISCLOSABLE_ORIGIN"
        if memory["kind"] == "NONDECLARATIVE_TRACE_EFFECT_PRESENT":
            assert memory["recall_granted"] is False
    assert act["actor_safe_projection"]["hidden_origin_refs"] == []


def test_hidden_origin_injection_leaves_actor_payload_unchanged():
    state_material = {
        "ADP016": {
            "view": {
                "TRACE_PUBLIC_SHAMING": {
                    "trace_kind": "NONDECLARATIVE_TRACE",
                    "activation": "RECRUITABLE",
                    "access_state": "RETAINED_NOT_ACCESSIBLE",
                    "parent_event_refs": ["EV7_PUBLIC_SHAMING"],
                }
            }
        },
        "ADP017": {"view": {}},
    }
    fx = case_fixture("K3")
    check = actor_safe_unchanged_by_hidden_origin(
        state_material=state_material,
        present_event=fx["present_event"],
        selected_route="HEIGHTENED_GUARD",
        uptake_refs=[],
        trace_records=[],
        memory_access_refs=[],
        claim_permission_refs=[],
        invalid_and_hold_codes=[],
        hidden_causal_origin={
            "hidden_origin": "EV7_PUBLIC_SHAMING_AT_AGE_7",
            "disclosed_only_to_evaluator": True,
        },
    )
    assert check["actor_safe_byte_identical"] is True
    assert check["pass"] is True


def test_powerless_witness_cannot_create_public_standing():
    fx = case_fixture("K5")
    peer = next(e for e in fx["histories"]["WEAK_PEER_PRAISE"]["events"] if e["event_id"] == "EV_PEER")
    ok, code = validate_effect_gate(
        {
            "effect_kind": "PUBLIC_STANDING_CHANGE",
            "target_key": "STANDING_A_TEST",
            "owner": "WORLD_PUBLIC_RECORD",
            "payload": {"standing": "CERTIFIED"},
            "parent_event_refs": ["EV_PEER"],
        },
        {"EV_PEER": peer},
    )
    assert not ok and code == INVALID_PUBLIC_STANDING


def test_k5_standing_only_registrar_belief_not_automatic():
    reg = run_single(k_id="K5", contrast="REGISTRAR_CERTIFIES", baseline="A", seed="S01")
    sup = run_single(k_id="K5", contrast="POWERFUL_SUPERVISOR_PRAISE", baseline="A", seed="S01")
    peer = run_single(k_id="K5", contrast="WEAK_PEER_PRAISE", baseline="A", seed="S01")
    assert reg["objective_public_standing_effects"]
    assert not sup["objective_public_standing_effects"]
    assert not peer["objective_public_standing_effects"]
    beliefs = {
        canonical_json(
            next(
                b
                for b in r["actor_safe_projection"]["beliefs"]
                if b["belief_key"] == "BELIEF_OWN_WORK_UNCERTAIN"
            )
        )
        for r in (reg, sup, peer)
    }
    assert len(beliefs) == 1


def test_k6_policing_requires_practice_and_capacity():
    cap = run_single(k_id="K6", contrast="PRACTICE_AND_CAPACITY", baseline="A", seed="S01")
    nocap = run_single(k_id="K6", contrast="PRACTICE_NO_CAPACITY", baseline="A", seed="S01")
    cat = run_single(k_id="K6", contrast="CATEGORY_ONLY", baseline="A", seed="S01")
    assert cap["lab_extension"]["selected_route"] == "POLICING_CANDIDATE"
    assert cap["lab_extension"]["selected_not_mandatory"] is True
    assert nocap["lab_extension"]["selected_route"] == "NO_SANCTION"
    assert cat["lab_extension"]["selected_route"] == "NO_SANCTION"
    assert not nocap["present_action_and_material_effects"]
    assert not cat["present_action_and_material_effects"]


def test_t5_revision_requires_new_parent():
    ok, code = validate_effect_gate(
        {
            "effect_id": "EFF_PARAPHRASE",
            "owner": "CAN011",
            "effect_kind": "TENSION_REVISED",
            "target_key": "APPROACH_WITHDRAW",
            "payload": {"status": "REINFORCED"},
            "parent_event_refs": ["EV7_QUESTION_PUNISHED"],
        },
        {},
    )
    assert not ok and code == INVALID_PRIOR_REWRITE


def test_unissued_weights_hold():
    r = run_single(
        k_id="K1",
        contrast="H_RESPONSIVE",
        baseline="A",
        seed="S01",
        unissued_weights={"w": 0.5},
    )
    assert INVALID_WEIGHT_WITHOUT_ISSUER in r["invalid_and_hold_codes"]
    assert not r["lab_extension"]["present_effect_receipts"]


def test_zero_affordance_is_valid_empty():
    fx = case_fixture("K1")
    empty_opp = {"opportunity_ref": "OPP_NONE", "exposure_ref": "EXP_NONE", "no_op_route": None, "available_routes": []}
    ev = dict(fx["present_event"])
    ev["opportunity_ref"] = "OPP_NONE"
    ev["exposure_ref"] = "EXP_NONE"
    r = run_single(
        k_id="K1",
        contrast="H_RESPONSIVE",
        baseline="A",
        seed="S01",
        event_override=ev,
        opportunity_override=empty_opp,
    )
    assert VALID_EMPTY in r["invalid_and_hold_codes"]
    assert not r["lab_extension"]["present_effect_receipts"]


def test_b_event_local_conation_never_persists():
    r = run_single(k_id="K1", contrast="H_RESPONSIVE", baseline="B", seed="S01")
    conation = r["lab_extension"]["event_local_conation"]
    assert conation["persistence"] == "EVENT_LOCAL_ONLY__NOT_PERSISTED__NOT_EFFECT_PARENT"
    assert not any(
        e["effect_kind"] == "EVENT_LOCAL_CONATION" for e in r["committed_effect_receipts"]
    )
    a = run_single(k_id="K1", contrast="H_RESPONSIVE", baseline="A", seed="S01")
    assert a["lab_extension"]["event_local_conation"] is None
    assert a["owner_state_after_hash"] == r["owner_state_after_hash"]


def test_c_relation_index_is_cheaper_than_reconstruction():
    a = run_single(k_id="K2", contrast="T_COMPENSATION", baseline="A", seed="S01")
    c = run_single(k_id="K2", contrast="T_COMPENSATION", baseline="C", seed="S01")
    assert a["lab_extension"]["relation_index_cost"]["events_scanned"] > 0
    assert c["lab_extension"]["relation_index_cost"]["events_scanned"] == 0
    assert (
        a["lab_extension"]["relation_view"]["type"]
        == c["lab_extension"]["relation_view"]["type"]
    )
    assert a["lab_extension"]["selected_route"] == c["lab_extension"]["selected_route"]


def test_testimony_never_changes_objective_effects():
    for mode in ("NO_EXPLANATION", "MISTAKEN_EXPLANATION_BELIEVED", "WRONGLY_CONFIDENT_EXPLANATION"):
        t = actor_testimony(mode=mode, machine_identified_parent_refs=["EV7_QUESTION_PUNISHED"])
        assert t["objective_effects_changed"] is False


def test_seed_rng_is_deterministic():
    assert seed_rng("X").random() == seed_rng("X").random()
    assert seed_rng("X").random() != seed_rng("Y").random()


def test_audit_receipt_fields_present():
    r = run_single(k_id="K1", contrast="H_RESPONSIVE", baseline="A", seed="S01")
    for field in (
        "case_id",
        "baseline",
        "arm",
        "seed",
        "model_version",
        "world_receipt_hash",
        "admitted_event_hashes",
        "owner_state_before_hash",
        "read_evidence_ref_list",
        "retrieval_token_count",
        "model_call_count",
        "latency_ms",
        "transition_rule_ids",
        "receivability_refs",
        "uptake_refs",
        "recruitment_refs",
        "proposed_effects",
        "authorized_effects",
        "committed_effect_receipts",
        "owner_state_after_hash",
        "actor_safe_projection",
        "actor_claim_permission_refs",
        "memory_access_and_trace_refs",
        "objective_public_standing_effects",
        "present_action_and_material_effects",
        "invalid_and_hold_codes",
        "full_replay_digest",
        "prose_optional",
    ):
        assert field in r
    assert r["model_call_count"] == 0
    assert r["retrieval_token_count"] <= 6000
