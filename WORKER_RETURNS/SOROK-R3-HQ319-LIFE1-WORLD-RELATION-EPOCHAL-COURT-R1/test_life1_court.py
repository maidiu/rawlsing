"""HQ319 LIFE1 — independent frozen-expectation court.

Asserts only what 01_PREREGISTRATION.json froze before any LIFE1 test code existed.
A DEFER is recorded as a DEFER and is never converted into a PASS.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

RET = Path(__file__).resolve().parent
sys.path.insert(0, str(RET))

import life1_court as L                                    # noqa: E402

PREREG = json.loads((RET / "01_PREREGISTRATION.json").read_text())
LEDGER = json.loads((RET / "evidence/native_source_ledger.json").read_text())


# ============================================================ custody
def test_native_closure_verified_139_of_139():
    assert len(LEDGER) == 139
    assert all(r["verified"] for r in LEDGER)
    assert all(r["git_blob_sha1"] == r["recomputed"] for r in LEDGER)


def test_imports_land_inside_this_return():
    import rawlsing_next.wsc_gt0_end_to_end as m
    assert str(RET) in m.__file__


# ============================================================ LP1: native thread
def test_lp1_native_end_to_end_terminates_blocked_positive_actor_path():
    r = L.run_native_thread()
    assert r["terminal"] == "BLOCKED_POSITIVE_ACTOR_PATH__SEMANTIC_CONSERVATION_PASS"
    assert r["stages"][-1]["status"] == "BLOCKED_NAMED_AUTHORITY_REQUIRED"
    # the native thread asserts it did NOT mutate V3 state
    assert r["stages"][3]["status"] == "UNDEFINED_FOR_OBJECT"


def test_lp1b_native_thread_is_deterministic():
    a, b = L.run_native_thread(), L.run_native_thread()
    assert a["full_thread_hash"] == b["full_thread_hash"]
    assert [s["status"] for s in a["stages"]] == [s["status"] for s in b["stages"]]


# ============================================================ LP2: missing producer
def test_lp2_no_executable_can008_mechanism_rule_body_exists():
    p = L.probe_positive_producer_available()
    assert p["positive_producer_available"] is False
    assert p["coupling_producer_is_person_response"] is False
    assert p["coupling_producer_owner"] == "FIELD_FORGE_ACTOR_INDEPENDENT_RELATION_OWNER"
    assert p["actor_sentinel"] == "GT0_NO_ACTOR_BOUND"


def test_lp2b_the_one_present_producer_is_a_population_statistic_not_a_person_response():
    p = L.probe_positive_producer_available()
    assert p["coupling_producers_present"] == ["rawlsing_next.field_forge_conditional_support"]
    # its semantics are explicitly conditional-support counting, not person response
    assert "CONDITIONAL_SUPPORT" in p["coupling_producer_semantics"]
    mp = p["missing_positive_producer"].lower()
    assert "can008_r2" in mp and "rule body" in mp
    assert "durable target owner" in mp and "actor binding" in mp


def test_lp2c_mechanism_binding_module_declares_it_cannot_execute_rules():
    from rawlsing_next import sdtf_r4_mechanism_rule_authority_binding as M
    doc = (M.__doc__ or "").lower()
    assert "execute rule bodies" in doc
    assert "mint concrete mechanism rules" in doc


# ============================================================ construction
def test_required_construction_is_present_and_structural():
    w0, w1 = L.build_w0(), L.build_w1()
    assert w0.world_id != w1.world_id
    assert "SANCTION_ROUTE" in w0.lawful_routes and "SANCTION_ROUTE" not in w1.lawful_routes
    assert "SANCTION_ROUTE_WITHDRAWN" in w1.typed_unknowns
    ab = L.build_relation("A_TO_B", "BINDING_EVALUATOR")
    ba = L.build_relation("B_TO_A", "NONBINDING_OBSERVER")
    assert ab.direction != ba.direction and ab.subject != ba.subject
    ep = L.build_epoch()
    assert ep.user_absent is True and ep.intervening_changes


def test_construction_makes_no_person_actor_or_world_fact_claim():
    blob = json.dumps(L.build_w0().identity()) + json.dumps(L.build_relation("A_TO_B", "BINDING_EVALUATOR").identity())
    assert "GENERATED_PERSON" in blob and "REAL_WORLD_FACT" in blob
    assert "FELT_STATE" in blob
    for banned in ("feels", "loves", "wants", "intends"):
        assert banned not in blob.lower()


def test_world_identity_is_explicitly_hashable_and_stable():
    assert L.build_w0().identity() == L.build_w0().identity()
    assert L.build_w0().identity() != L.build_w1().identity()


def test_lp5_user_absence_epoch_is_independent_and_bounded():
    ep = L.build_epoch()
    assert ep.user_absent and ep.start < ep.end
    assert ep.independent_clock == "SOURCE_NATIVE_EPOCHAL_CLOCK"
    assert "W1_INSTITUTIONAL_CHANGE" in ep.intervening_changes


def test_lp5_actor_private_knowledge_is_not_an_actor_visible_field():
    ep = L.build_epoch()
    ident = json.dumps(ep.identity())
    # the epoch is analyst-visible structural material, never an actor render
    assert "rendered_text" not in ident
    assert "first_person" not in ident.lower()


# ============================================================ LP3: K1-K6
def test_lp3_all_six_cases_execute_and_every_arm_defers():
    res = L.run_all_cases(L.B0)
    assert len(ALL := L.ALL_CASES) == 6
    assert len(res["attempts"]) == 16          # K1:2 K2:2 K3:3 K4:3 K5:3 K6:3
    assert res["all_deferred"] is True
    assert {a.case for a in res["attempts"]} == set(ALL)


def test_lp3b_no_arm_is_answered_by_a_hand_authored_label():
    for a in L.run_all_cases(L.B0)["attempts"]:
        assert a.outcome == L.DEFER
        assert a.native_entered is False
        assert a.extras["missing_positive_producer"]


@pytest.mark.parametrize("case", sorted(L.ALL_CASES))
def test_each_case_records_exact_missing_authority(case):
    attempts = [a for a in L.run_all_cases(L.B0)["attempts"] if a.case == case]
    assert attempts
    for a in attempts:
        assert "NO_AUTHORIZED_CAN008_R2_MECHANISM_RULE_BODY" in a.detail


def test_lp6_a_defer_is_never_reported_as_a_typed_response_difference():
    res = L.run_all_cases(L.B0)
    outcomes = {a.outcome for a in res["attempts"]}
    assert outcomes == {L.DEFER}
    # no arm produced a response effect at all
    assert all(not a.requested_effect == a.outcome for a in res["attempts"])


# ============================================================ LP4: B0 vs B1
def test_lp4_b0_and_b1_consume_identical_matched_budgets():
    assert L.budget_match(L.B0, L.B1)
    assert L.B0.rule_label != L.B1.rule_label       # different rules...
    assert L.B0.mechanism_id != L.B1.mechanism_id


def test_lp4b_richer_mechanism_earns_nothing_at_matched_budget():
    r0, r1 = L.run_all_cases(L.B0), L.run_all_cases(L.B1)
    assert r0["all_deferred"] == r1["all_deferred"] is True
    assert ([(a.case, a.arm, a.outcome) for a in r0["attempts"]]
            == [(a.case, a.arm, a.outcome) for a in r1["attempts"]])
    # identical evidence/compute, identical (null) executable outcome
    assert all(a.evidence_reads == b.evidence_reads and a.compute_units == b.compute_units
               for a, b in zip(r0["attempts"], r1["attempts"]))


def test_lp4c_verdict_richer_mechanism_is_not_promoted():
    r1 = L.run_all_cases(L.B1)
    assert all(a.outcome == L.DEFER for a in r1["attempts"])
    # B1 proposes more structure but earns zero executable credit
    assert not any(a.outcome not in (L.DEFER,) for a in r1["attempts"])


# ============================================================ controls
def test_valid_empty_control_is_a_real_nonpositive_outcome():
    v = L.valid_empty_control()
    assert v["decision_state"] == "RESPONSE_EFFECTS_VALID_EMPTY"
    assert v["produced_effect"] is None
    assert v["rule_label"] == L.B0.rule_label


def test_valid_empty_is_distinct_from_defer():
    assert L.valid_empty_control()["decision_state"] != L.DEFER


def test_global_no_go_source_and_clock_boundaries_preserved():
    # world provenance is explicit and never a real world claim
    assert L.build_w0().provenance.startswith("SOURCE_FREE_LABORATORY")
    assert L.build_epoch().independent_clock == "SOURCE_NATIVE_EPOCHAL_CLOCK"


def test_rule_labels_are_proposed_unissued_never_accepted():
    assert "proposed" in L.B0.rule_label and "proposed" in L.B1.rule_label
    assert L.RULE_GRAIN.startswith("PROPOSED_UNISSUED")
    assert "NOT_CURRENT" in L.RULE_GRAIN
    assert L.FIXTURE_LABEL == "LABORATORY_STRUCTURAL_FIXTURE__NOT_PREV3_OUTPUT"


def test_preregistration_is_frozen_and_self_consistent():
    assert PREREG["status"] == "FROZEN_BEFORE_ANY_NEW_LIFE1_TEST_CODE_OR_MECHANISM"
    assert set(PREREG["K1_K6_CLASSES_FROZEN"]) == {f"K{i}" for i in range(1, 7)}
    assert "PRODUCT_WHITE_WHALE_DEPENDENCY_HOLD" in PREREG["permitted_outcomes"][1]
    assert PREREG["grain_and_authority_ceiling"]["no_actor_wake"] is True
    assert PREREG["grain_and_authority_ceiling"]["no_semantic_owner_creation"] is True


def test_lf1_hand_authored_expected_outcome_table_is_never_an_answer():
    """The arm expectations are PROPOSED labels; the recorded outcome is the native DEFER."""
    res = L.run_all_cases(L.B0)
    for a in res["attempts"]:
        assert a.requested_effect != a.outcome
        assert a.outcome == L.DEFER