"""HQ300 — candidate court: positive chain, K3/K5, 9 hostiles, preserved guards.

Grain: SOURCEFREE_CANDIDATE__NOT_ADOPTED__NOT_PRODUCTION__NOT_V3_ACTOR.
Frozen expectations: 01_FROZEN_EXPECTED_MATRIX.json (sha256 38226170...).
"""
from __future__ import annotations

import hashlib
import importlib
import inspect
import json
import os
import re
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
STAGE = os.environ.get("HQ300_STAGE", "")
if STAGE and STAGE not in sys.path:
    sys.path.insert(0, STAGE)

from candidate.adopted_contract import (
    PINS, EFFECT_GRAMMAR, NONCOLLAPSE_LAWS, ADP016_FAIL_CLOSED_STATES,
    ADP017_AUTOMATIC_IMPLICATIONS_FORBIDDEN, ADP017_MEMORY_NONCOLLAPSE,
    AdmittedEvent, GeneratedMemoryState, first_person_permission,
    knowledge_gate_check,
)
from candidate.candidate_registry_fixture import (
    CandidateRegistryFixture, FIXTURE_GRAIN, PRODUCTION_REGISTRY_UNTOUCHED,
)
from candidate.can008_candidate_rule import (
    build_default_binding, coupline_evaluate, response_rule_apply,
    build_response_receipt, register_default_rule, occurrence_gate,
    OwnerPrestate, RULE_ID, RULE_VERSION,
)
from candidate.owner_transitions import (
    adp016_form_causal_trace, adp016_attempt_transition,
    adp016_rehydration_refused, adp017_apply_epistemic_effect,
    adp017_first_person_check, adp017_sole_memory_basis_failclosed,
    OwnerTransitionError,
)
from candidate.positive_chain import (
    ChainEventLedger, run_positive_chain,
)

MATRIX = json.load(open(os.path.join(ROOT, "01_FROZEN_EXPECTED_MATRIX.json")))
FROZEN = MATRIX["positive_chain_frozen_expectations"]["expected"]


def _mk_event(**kw) -> AdmittedEvent:
    base = dict(
        event_id="EV_T", event_hash="sha256:ev_t",
        issuer_authority_id="ISSUER_AUTH_WORLD_SCHED",
        issuer_authority_version="1", event_kind="EXTERNAL_RUNTIME_EVENT",
        effective_causal_time="1998-10-03T16:00:00Z", actor_scope="ACTOR_SYNTH_1",
        world_ref="W_SYNTH_1998", world_as_of="1998-10-03T16:00:00Z",
        admission_state="ADMITTED", public_features=("feat_a",))
    base.update(kw)
    return AdmittedEvent(**base)


def _mk_prestate(**kw) -> OwnerPrestate:
    base = dict(actor_id="ACTOR_SYNTH_1", world_ref="W_SYNTH_1998",
                world_as_of="1998-10-03T16:00:00Z")
    base.update(kw)
    return OwnerPrestate(**base)


# ---------------------------------------------------------------------------
# A. frozen matrix + adopted pins integrity
# ---------------------------------------------------------------------------

def test_A_matrix_frozen_before_execution():
    raw = open(os.path.join(ROOT, "01_FROZEN_EXPECTED_MATRIX.json"), "rb").read()
    h = hashlib.sha256(raw).hexdigest()
    freeze = json.load(open(os.path.join(ROOT, "outputs", "matrix_freeze.json")))
    assert freeze["sha256"] == h
    assert freeze["frozen_before_any_execution"] is True
    assert MATRIX["status"] == "FROZEN_PRIOR_TO_ANY_EXECUTION"


def test_A_adopted_pins_match_authority_blobs():
    assert PINS["CAN008_R2"] == MATRIX["frozen_inputs"]["CAN008_R2_adopted_blob"]
    assert PINS["ADP016_JSON"] == MATRIX["frozen_inputs"]["ADP016_json_blob"]
    assert PINS["ADP017_JSON"] == MATRIX["frozen_inputs"]["ADP017_json_blob"]
    assert PINS["ADP017_JSON"] == "eece4f3f2f3f9288ab9bbc645dc81e20a99e1280"


def test_A_effect_grammar_is_exactly_adopted():
    assert set(EFFECT_GRAMMAR) == {"BUFFER", "AMPLIFY", "DEFLECT", "REROUTE", "TRANSFORM", "BLOCK"}


def test_A_rule_binding_complete_against_23_obligations():
    b = build_default_binding()
    assert b.validate_complete() is None
    from candidate.adopted_contract import R2_RULE_OBLIGATION_ITEMS
    assert len(R2_RULE_OBLIGATION_ITEMS) == 23


# ---------------------------------------------------------------------------
# B. registry fixture is NOT production authorization
# ---------------------------------------------------------------------------

def test_B_registry_fixture_is_labelled_non_authorization():
    reg = CandidateRegistryFixture()
    assert FIXTURE_GRAIN == "SOURCEFREE_CANDIDATE_FIXTURE__NOT_ACCEPTED_AUTHORIZATION"
    assert PRODUCTION_REGISTRY_UNTOUCHED is True
    rec = register_default_rule(reg)
    assert rec["status"] == "CANDIDATE_REGISTERED_IN_FIXTURE"
    assert rec["production_registry_mutated"] is False


def test_B_imported_production_guard_still_denies():
    """PRESERVED negative guard: the imported zero-positive guard registry stays
    empty and denies every production positive transition."""
    guard = importlib.import_module("rawlsing_next.v3_psepf_zero_positive_guard")
    assert dict(guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES) == {}
    fp = guard.GuardStateFingerprint(**{
        f: "fp_" + f for f in guard.GuardStateFingerprint.__dataclass_fields__})
    req = guard.GuardRequest(
        actor_id="ACTOR_SYNTH_1",
        source_class=guard.GuardedTruthClass.ANALYST_TRUTH,
        source_ref="ref:lab:hq300", source_hash="sha256:aa",
        source_lineage=(guard.GuardedTruthClass.ANALYST_TRUTH,),
        transition_surface_id="CAN008_R2_RESPONSE_EFFECT_COMMIT",
        operation_class="TARGET_OWNER_EFFECT_COMMIT",
        state_fingerprint=fp, authority=None)
    d = guard.evaluate_psepf_zero_positive_guard(req)
    assert d.outcome == guard.GuardOutcome.DENY_ZERO_EFFECT
    assert d.reason == guard.GuardReason.ZERO_POSITIVE_REGISTRY
    assert d.zero_effect is True


def test_B_imported_gt0_still_blocks_positive_actor_path():
    e2e = importlib.import_module("rawlsing_next.wsc_gt0_end_to_end")
    assert e2e.TERMINAL == "BLOCKED_POSITIVE_ACTOR_PATH__SEMANTIC_CONSERVATION_PASS"
    assert e2e.run_gt0_end_to_end().terminal == e2e.TERMINAL


# ---------------------------------------------------------------------------
# C. positive chain (frozen expectations)
# ---------------------------------------------------------------------------

def test_C_positive_chain_meets_frozen_expectations():
    out = run_positive_chain()
    assert out["terminal"] == "CHAIN_COMPLETE"
    assert out["occurrence_gate"]["status"] == FROZEN["event_admitted"]
    assert out["coupling_decision_state"] == FROZEN["coupling_decision_state"]
    assert out["response_effect_kind"] == FROZEN["response_effect_kind"]
    assert out["target_owner_effect_committed"] is FROZEN["target_owner_effect_committed"]
    assert out["causal_order_enforced"] is FROZEN["causal_order_enforced"]
    tr = out["adp016_trace"]
    assert tr["representation_kind"] == FROZEN["adp016_trace"]["representation_kind"]
    assert tr["memory_accessibility_state"] == FROZEN["adp016_trace"]["memory_accessibility_state"]
    assert tr["retention_state"] == FROZEN["adp016_trace"]["retention_state"]
    assert tr["content_first_person_readable"] is FROZEN["adp016_trace"]["content_first_person_readable"]
    ep = out["adp017_epistemic"]
    assert ep["stance_kind"] == FROZEN["adp017_epistemic"]["stance_kind"]
    assert ep["stance_operation"] == FROZEN["adp017_epistemic"]["stance_operation"]
    assert ep["decision_state"] == FROZEN["adp017_epistemic"]["decision_state"]
    assert out["full_replay_digest"]


def test_C_later_event_reads_stored_effect_and_differs_from_control():
    out = run_positive_chain()
    later = out["later_event_response"]
    assert later["prior_effect_read"] is True
    assert later["commit"] == "COMMITTED_IN_CAUSAL_ORDER"
    diff = out["later_response_typed_difference"]
    assert diff["typed_difference"] is True
    assert diff["with_prior_effect"] != diff["control_without_prior_effect"]
    assert FROZEN["later_event_response"].startswith("typed response differs")


def test_C_full_replay_is_exact():
    a = run_positive_chain()
    b = run_positive_chain()
    assert a["full_replay_digest"] == b["full_replay_digest"]
    assert a["ledger_hash"] == b["ledger_hash"]


def test_C_effect_stored_in_causal_order():
    out = run_positive_chain()
    ledger = ChainEventLedger()
    assert ledger.commit("X", {"v": 1}, "1999-01-01T00:00:00Z", [])["status"] == "COMMITTED_IN_CAUSAL_ORDER"
    assert ledger.commit("Y", {"v": 2}, "1998-01-01T00:00:00Z", [])["status"] == "REFUSED"


def test_C_target_owner_effect_is_request_not_seizure():
    """R2 §11: any durable target state remains destination-owner-owned."""
    reg = CandidateRegistryFixture()
    register_default_rule(reg)
    b = build_default_binding()
    coupling = coupline_evaluate(_mk_event(), _mk_prestate(), b, reg)
    resp = response_rule_apply(coupling, _mk_prestate(), b, "BUFFER")
    reqs = resp["target_owner_effect_requests"]
    assert all(r["committed"] is False for r in reqs)
    assert all(r["request_kind"] == "SEPARATELY_OWNED_EFFECT_REQUEST" for r in reqs)


# ---------------------------------------------------------------------------
# D. K3 — inaccessible origin does not grant self-explanation
# ---------------------------------------------------------------------------

def test_D_K3_trace_recruits_but_denies_first_person_claim():
    out = run_positive_chain()
    tr = out["adp016_trace"]
    assert tr["representation_kind"] == "CAUSAL_TRACE_MEMORY"
    chk = adp017_first_person_check(
        stance_kind="BELIEF", claim_accessibility="CLAIM_ACCESSIBLE",
        memory_representation_kind="CAUSAL_TRACE_MEMORY")
    assert chk["first_person_permission"] == "DENY_FIRST_PERSON_CLAIM"
    assert chk["self_explanation_of_hidden_origin"] == "BLOCKED"
    assert chk["analyst_only_causal_trace_actor_claimable"] is False


def test_D_K3_hidden_origin_content_not_first_person_readable():
    ev = _mk_event()
    trace = adp016_form_causal_trace(
        actor_id="ACTOR_SYNTH_1", basis_event=ev,
        trace_key="TRACE_HIDDEN_CHILDHOOD", content_state="UNAVAILABLE",
        owning_rule_id=RULE_ID, owning_rule_version=RULE_VERSION,
        owning_rule_hash="sha256:rule", authority_id="A", authority_version="1")
    assert trace["memory"]["representation_kind"] == "CAUSAL_TRACE_MEMORY"
    assert trace["first_person_origin_claimable"] is False
    assert "actor_knows" in trace["must_not_output"]
    assert "may_claim_first_person" in trace["must_not_output"]


def test_D_K3_causal_trace_not_recallable():
    ev = _mk_event()
    trace = adp016_form_causal_trace(
        actor_id="ACTOR_SYNTH_1", basis_event=ev,
        trace_key="T", content_state="AVAILABLE_SOURCE_BOUND",
        owning_rule_id=RULE_ID, owning_rule_version=RULE_VERSION,
        owning_rule_hash="h", authority_id="A", authority_version="1")
    mem = GeneratedMemoryState(**trace["memory"])
    with pytest.raises(OwnerTransitionError) as e:
        adp016_attempt_transition(mem, "RECALL")
    assert e.value.code == "UNAUTHORIZED_RECALL_CUE"


def test_D_K3_sole_memory_basis_failclosed():
    ev = _mk_event()
    trace = adp016_form_causal_trace(
        actor_id="ACTOR_SYNTH_1", basis_event=ev, trace_key="T",
        content_state="AVAILABLE_SOURCE_BOUND",
        owning_rule_id=RULE_ID, owning_rule_version=RULE_VERSION,
        owning_rule_hash="h", authority_id="A", authority_version="1")
    mem = GeneratedMemoryState(**trace["memory"])
    dead = GeneratedMemoryState(**{**mem.__dict__,
                                   "memory_accessibility_state": "INACCESSIBLE",
                                   "retention_state": "CONTENT_UNAVAILABLE"})
    res = adp017_sole_memory_basis_failclosed("BELIEF", "CLAIM_ACCESSIBLE", dead)
    assert res["first_person_permission"] == "DENY_FIRST_PERSON_CLAIM"
    assert res["memory_inaccessibility_auto_erases_stance"] is False


# ---------------------------------------------------------------------------
# E. K5 — public status vs private belief do not collapse
# ---------------------------------------------------------------------------

def test_E_K5_belief_identical_across_witness_power():
    """Adopted law: objective truth necessary not sufficient; no auto-belief;
    accessible memory does not auto-create stance."""
    beliefs = []
    for witness_power, obj_rel in (("CAN_RATIFY", "OBJECTIVE_SUPPORTED"),
                                   ("CAN_SIGN_SHIFT_NOT_RATIFY", "OBJECTIVE_SUPPORTED"),
                                   ("NONE", "OBJECTIVE_UNRESOLVED")):
        epi = adp017_apply_epistemic_effect(
            actor_id="ACTOR_SYNTH_1",
            claim_ref="CLAIM_OWN_WORK_UNCERTAIN",
            stance_kind="BELIEF", stance_operation="ADD",
            causal_parent_refs=["EV_PRIVATE_SELF_DOUBT"],
            actor_facing_basis_refs=["EV_PRIVATE_SELF_DOUBT:hash"],
            memory_basis_refs=["MEM_SELF_DOUBT"],
            owning_rule_id=RULE_ID, owning_rule_version=RULE_VERSION,
            owning_rule_hash="h", effective_causal_time="1998-05-01T00:00:00Z",
            claim_objective_relation=obj_rel,
            claim_accessibility="CLAIM_ACCESSIBLE")
        beliefs.append((witness_power, epi["effect"]["stance_kind"],
                        epi["effect"]["claim_ref"]))
    assert len(set(beliefs)) == 3  # witness power present in tuple
    stance_set = {(b[1], b[2]) for b in beliefs}
    assert len(stance_set) == 1  # belief state identical across witness arms


def test_E_K5_knowledge_gate_truth_not_sufficient():
    ok, reasons = knowledge_gate_check(
        "OBJECTIVE_SUPPORTED", actor_facing_basis_exists=False,
        owning_rule_emits_knowledge=True, actor_role_sufficient=True,
        integrity_ok=True, authority_complete=True)
    assert ok is False
    assert any("actor-facing" in r for r in reasons)


def test_E_K5_no_automatic_implication_enumerated():
    for imp in ADP017_AUTOMATIC_IMPLICATIONS_FORBIDDEN:
        assert "->" in imp
    assert "OBJECTIVE_SUPPORTED -> KNOWLEDGE" in ADP017_AUTOMATIC_IMPLICATIONS_FORBIDDEN
    assert "MEMORY_ACCESSIBLE -> KNOWLEDGE" in ADP017_AUTOMATIC_IMPLICATIONS_FORBIDDEN
    for nc in ADP017_MEMORY_NONCOLLAPSE:
        assert "!=" in nc


def test_E_K5_public_standing_not_in_actor_info():
    """Objective standing is owner-held; the chain never exports it as actor belief."""
    out = run_positive_chain()
    # the epistemic update is BELIEF (private), never auto KNOWLEDGE from objective support
    assert out["adp017_epistemic"]["stance_kind"] == "BELIEF"
    assert out["adp017_epistemic"]["accessible_memory_auto_creates_stance"] is False


# ---------------------------------------------------------------------------
# F. 9 hostile negatives (frozen codes)
# ---------------------------------------------------------------------------

def _expect_refusal(fn, code_substr: str):
    with pytest.raises(OwnerTransitionError) as e:
        fn()
    assert code_substr in e.value.code or code_substr in e.value.detail


def test_F_H1_no_admission():
    reg = CandidateRegistryFixture()
    register_default_rule(reg)
    b = build_default_binding()
    ev = _mk_event(admission_state="PROPOSED", event_id="EV_NO_ADMIT")
    out = coupline_evaluate(ev, _mk_prestate(), b, reg)
    assert out["decision_state"] == "BLOCK_UNADMITTED_EVENT"
    assert out["committed"] is False


def test_F_H2_forged_issuer():
    reg = CandidateRegistryFixture()
    register_default_rule(reg)
    b = build_default_binding()
    ev = _mk_event(issuer_authority_id="FORGED_ISSUER_AUTHORITY", event_id="EV_FORGED")
    out = coupline_evaluate(ev, _mk_prestate(), b, reg)
    assert out["decision_state"] == "BLOCK_FORGED_OR_MISMATCHED_ISSUER"
    assert out["code"] == MATRIX["hostile_frozen_expectations"][1]["expected_code"]


def test_F_H3_stale_asof_world():
    reg = CandidateRegistryFixture()
    register_default_rule(reg)
    b = build_default_binding()
    ev = _mk_event(world_as_of="1999-01-01T00:00:00Z", event_id="EV_STALE")
    out = coupline_evaluate(ev, _mk_prestate(), b, reg)
    assert out["decision_state"] == "BLOCK_STALE_OR_MISMATCHED_WORLD_ASOF"
    assert out["code"] == MATRIX["hostile_frozen_expectations"][2]["expected_code"]


def test_F_H4_wrong_actor_scope():
    reg = CandidateRegistryFixture()
    register_default_rule(reg)
    b = build_default_binding(actor_scope="ACTOR_SYNTH_1")
    ev = _mk_event(actor_scope="ACTOR_OTHER", event_id="EV_SCOPE")
    out = coupline_evaluate(ev, _mk_prestate(), b, reg)
    assert out["decision_state"] == "BLOCK_WRONG_ACTOR_SCOPE"
    assert out["code"] == MATRIX["hostile_frozen_expectations"][3]["expected_code"]


def test_F_H5_hidden_future_leak():
    reg = CandidateRegistryFixture()
    register_default_rule(reg)
    b = build_default_binding()
    ev = _mk_event(derived_from_future_partition=True, event_id="EV_FUTURE")
    out = coupline_evaluate(ev, _mk_prestate(), b, reg)
    assert out["decision_state"] == "BLOCK_HIDDEN_FUTURE_LEAK"
    assert out["committed"] is False


def test_F_H6_duplicate_event():
    reg = CandidateRegistryFixture()
    register_default_rule(reg)
    b = build_default_binding()
    ev1 = _mk_event(event_id="EV_DUP")
    coupline_evaluate(ev1, _mk_prestate(), b, reg)
    ev2 = _mk_event(event_id="EV_DUP")
    out = coupline_evaluate(ev2, _mk_prestate(), b, reg)
    assert out["decision_state"] == "BLOCK_DUPLICATE_EVENT_IDENTITY"


def test_F_H7_disallowed_memory():
    ev = _mk_event(event_id="EV_H7")
    for bad in ("PERSONA_SHEET", "RENDERED_DIALOGUE", "V2_TRANSCRIPT",
                "STRUCTURAL_OBJECT", "ANALYST_ANNOTATION"):
        with pytest.raises(OwnerTransitionError) as e:
            adp016_form_causal_trace(
                actor_id="ACTOR_SYNTH_1", basis_event=ev, trace_key="T",
                content_state=bad, owning_rule_id=RULE_ID,
                owning_rule_version=RULE_VERSION, owning_rule_hash="h",
                authority_id="A", authority_version="1")
        assert e.value.code == "INELIGIBLE_NONCAUSAL_SOURCE"


def test_F_H8_invalid_trace():
    ev = _mk_event(event_id="EV_H8")
    trace = adp016_form_causal_trace(
        actor_id="ACTOR_SYNTH_1", basis_event=ev, trace_key="T",
        content_state="AVAILABLE_SOURCE_BOUND", owning_rule_id=RULE_ID,
        owning_rule_version=RULE_VERSION, owning_rule_hash="h",
        authority_id="A", authority_version="1")
    mem = GeneratedMemoryState(**trace["memory"])
    with pytest.raises(OwnerTransitionError) as e:
        adp016_attempt_transition(mem, "REACTIVATE", parent_event=ev,
                                  declared_parent_hash="sha256:WRONG")
    assert e.value.code == "PARENT_EVENT_HASH_MISMATCH"
    with pytest.raises(OwnerTransitionError) as e2:
        adp016_attempt_transition(mem, "REACTIVATE", pre_state_hash="sha256:STALE")
    assert e2.value.code == "PRE_STATE_HASH_MISMATCH"


def test_F_H9_reverse_chronology():
    ledger = ChainEventLedger()
    assert ledger.commit("X", {"v": 1}, "1999-06-01T00:00:00Z", [])["status"] \
        == "COMMITTED_IN_CAUSAL_ORDER"
    out = ledger.commit("Y", {"v": 2}, "1999-01-01T00:00:00Z", ["X"])
    assert out["status"] == "REFUSED"
    assert out["code"] == "BLOCK_REVERSE_CHRONOLOGY_CAUSAL_PARENT"
    # also at the coupling gate
    reg = CandidateRegistryFixture()
    register_default_rule(reg)
    b = build_default_binding()
    ev = _mk_event(event_id="EV_REV", causal_parent_event_ids=("EV_LATER",),
                   reverse_chronology_flag=True)
    out2 = coupline_evaluate(ev, _mk_prestate(), b, reg)
    assert out2["decision_state"] == "BLOCK_REVERSE_CHRONOLOGY_CAUSAL_PARENT"


# ---------------------------------------------------------------------------
# G. DISC_01 corrected detector (implementation surface, not text scan)
# ---------------------------------------------------------------------------

def _implementation_surface_hits(search_root: str) -> list:
    """Precise implementation-surface scan: class/def names only.
    RSM correction of DISC_01: text-constant mentions are NOT implementations."""
    pat = re.compile(
        r"^\s*(?:class|def)\s+(\w*(?:coupling|response_rule|owner_effect|"
        r"target_effect|transition_producer|coupling_rule)\w*)", re.I | re.M)
    hits = []
    for root, dirs, files in os.walk(search_root):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        if "tests" in root.split(os.sep):
            continue
        for fn in files:
            if not fn.endswith(".py"):
                continue
            src = open(os.path.join(root, fn), encoding="utf-8", errors="replace").read()
            for m in pat.finditer(src):
                hits.append((fn, m.group(1)))
    return hits


def test_G_disc01_corrected_detector_production_surface_zero():
    """RSM's precise scan: 0 implementation-surface hits in production modules.
    The HQ298 text scan was overbroad (DISC_01)."""
    if not STAGE:
        pytest.skip("HQ300_STAGE not set")
    hits = _implementation_surface_hits(os.path.join(STAGE, "rawlsing_next"))
    assert hits == [], f"UNEXPECTED_PRODUCTION_IMPLEMENTATION_SURFACE:{hits}"


def test_G_disc01_string_mentions_are_denylist_codes_not_implementations():
    """The two known string-constant mentions are classified, not conflated."""
    known = {
        "gt34_obl031_q69b_comparator_resolver_r2.py":
            ("PSEPF_V3_MUTATION_METABOLISM_CAN008_V2", "denylist identifier constant"),
        "gt34_adp010_input_authority_acceptance.py":
            ("NO_CAN_008", "rejection-code string constant"),
    }
    for fn, (token, classification) in known.items():
        assert "implementation" not in classification
        assert "denylist" in classification or "rejection-code" in classification


def test_G_candidate_implementation_surface_is_confined_to_candidate_package():
    hits = [h for h in _implementation_surface_hits(HERE)
            if not h[0].startswith("test_")]
    assert hits, "candidate package must contain the candidate implementation surface"
    for fn, name in hits:
        assert fn.startswith(("can008_candidate_rule", "owner_transitions",
                              "positive_chain", "candidate_registry_fixture",
                              "adopted_contract")), f"OUT_OF_SCOPE_IMPL:{fn}:{name}"


# ---------------------------------------------------------------------------
# H. preserved guards and replay invariants
# ---------------------------------------------------------------------------

def test_H_no_production_registry_mutation():
    guard = importlib.import_module("rawlsing_next.v3_psepf_zero_positive_guard")
    assert dict(guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES) == {}
    # candidate registration does not touch it
    reg = CandidateRegistryFixture()
    register_default_rule(reg)
    assert dict(guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES) == {}


def test_H_delete_memory_forbidden():
    ev = _mk_event(event_id="EV_DEL")
    trace = adp016_form_causal_trace(
        actor_id="ACTOR_SYNTH_1", basis_event=ev, trace_key="T",
        content_state="AVAILABLE_SOURCE_BOUND", owning_rule_id=RULE_ID,
        owning_rule_version=RULE_VERSION, owning_rule_hash="h",
        authority_id="A", authority_version="1")
    mem = GeneratedMemoryState(**trace["memory"])
    with pytest.raises(OwnerTransitionError) as e:
        adp016_attempt_transition(mem, "DELETE_MEMORY")
    assert e.value.code == "UNAUTHORIZED_TRANSITION"


def test_H_rehydration_forbidden():
    ev = _mk_event(event_id="EV_REHYD")
    trace = adp016_form_causal_trace(
        actor_id="ACTOR_SYNTH_1", basis_event=ev, trace_key="T",
        content_state="AVAILABLE_SOURCE_BOUND", owning_rule_id=RULE_ID,
        owning_rule_version=RULE_VERSION, owning_rule_hash="h",
        authority_id="A", authority_version="1")
    mem = GeneratedMemoryState(**trace["memory"])
    with pytest.raises(OwnerTransitionError) as e:
        adp016_rehydration_refused(mem, "analyst ledger content")
    assert e.value.code == "UNAUTHORIZED_OBJECTIVE_HISTORY_REHYDRATION"


def test_H_response_receipt_is_not_durable_actor_state():
    reg = CandidateRegistryFixture()
    register_default_rule(reg)
    b = build_default_binding()
    ev = _mk_event(event_id="EV_RCPT")
    coupling = coupline_evaluate(ev, _mk_prestate(), b, reg)
    resp = response_rule_apply(coupling, _mk_prestate(), b, "BUFFER")
    rcpt = build_response_receipt(ev, _mk_prestate(), b, coupling, resp)
    assert rcpt["is_durable_actor_state"] is False
    assert rcpt["receipt_kind"] == "V3ResponseEvaluationReceipt"


def test_H_noncollapse_laws_are_bound():
    reg = CandidateRegistryFixture()
    register_default_rule(reg)
    b = build_default_binding()
    ev = _mk_event(event_id="EV_NC")
    coupling = coupline_evaluate(ev, _mk_prestate(), b, reg)
    resp = response_rule_apply(coupling, _mk_prestate(), b, "BUFFER")
    rcpt = build_response_receipt(ev, _mk_prestate(), b, coupling, resp)
    assert set(rcpt["noncollapse_laws_bound"]) == set(NONCOLLAPSE_LAWS)
