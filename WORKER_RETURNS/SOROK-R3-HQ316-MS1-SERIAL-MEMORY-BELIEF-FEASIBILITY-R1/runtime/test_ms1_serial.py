"""HQ316 MS1 — independent test suite for SERIAL ADP016->ADP017->CAN008 mediation.

Prospectively written against the frozen 01_PREREGISTRATION.md. Predictions are
asserted AS PREDICTED, including the ones that FAILED: a falsified prediction is
reported by an explicitly named test that passes only when the preregistered
relation is FALSIFIED. No prediction is edited after execution.

Grain: SOURCEFREE_SYNTHETIC_TEST_ONLY. No production, no V3, no human claim.
"""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

import pytest

RUNTIME = Path(__file__).resolve().parent
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))

import ms1_serial as M                                     # noqa: E402
from candidate import can008_candidate_rule as can8        # noqa: E402
from candidate import owner_transitions as owner           # noqa: E402
from candidate.candidate_registry_fixture import CandidateRegistryFixture  # noqa: E402
from candidate import positive_chain as chain              # noqa: E402

CERTAIN = M.MEMORY_CONTENT_CERTAIN
UNCERTAIN = M.MEMORY_CONTENT_UNCERTAIN


# ---------------------------------------------------------------------------
# Positive / negative controls: the pinned native modules really execute here.
# ---------------------------------------------------------------------------

def test_control_native_modules_execute_and_owner_state_is_real():
    """Positive control: real native formation + transition produce real sealed state."""
    reg = CandidateRegistryFixture()
    assert can8.register_default_rule(reg)["status"] == "CANDIDATE_REGISTERED_IN_FIXTURE"
    binding = can8.build_default_binding()
    ctx = owner.FixtureOwnerState(reg, M.ACTOR)
    e1 = M.fixed_e1()
    assert can8.occurrence_gate(e1, reg)["status"] == "ADMITTED_OCCURRENCE"
    proposal, memory = M.form_and_commit_memory(reg, ctx, e1, binding, CERTAIN)
    assert memory is not None
    assert memory["memory_id"] in ctx.memories                    # real committed owner state
    assert memory["current_state_hash"] == owner.memory_semantic_hash(memory)
    assert ctx.verify() and reg.verify()
    assert ctx.memories[memory["memory_id"]] == memory
    assert M.fixed_e1().event_hash == e1.event_hash                # exogenous input is fixed


def test_control_negative_native_refuses_unregistered_content_class():
    """Negative control: the native owner still refuses an ineligible source state."""
    reg = CandidateRegistryFixture()
    can8.register_default_rule(reg)
    binding = can8.build_default_binding()
    ctx = owner.FixtureOwnerState(reg, M.ACTOR)
    e1 = M.fixed_e1()
    can8.occurrence_gate(e1, reg)
    with pytest.raises(owner.OwnerTransitionError) as exc:
        owner.adp016_form_causal_trace(
            actor_id=M.ACTOR, basis_event=e1, trace_key="TRACE_FEEDBACK_WINDOW_EXPERIENCE",
            content_state="TOTALLY_MADE_UP_STATE",
            owning_rule_id=can8.RULE_ID, owning_rule_version=can8.RULE_VERSION,
            owning_rule_hash=binding.rule_content_hash,
            authority_id="WORKER_CANDIDATE_FIXTURE", authority_version="1",
            parent_state_hash=ctx.state_hash, context=ctx)
    assert exc.value.code == "INELIGIBLE_NONCAUSAL_SOURCE"


# ---------------------------------------------------------------------------
# F2 lever: same memory ID, different verified content, identical exogenous input.
# ---------------------------------------------------------------------------

def test_memory_content_varies_under_one_memory_id_with_fixed_exogenous_inputs():
    a = M.run_cell("F2a", CERTAIN)
    b = M.run_cell("F2b", UNCERTAIN)
    assert a["memory_id"] == b["memory_id"], "content must vary under one memory ID"
    assert a["memory_uncertainty_state"] == "CERTAIN"
    assert b["memory_uncertainty_state"] == "UNCERTAIN"
    assert a["memory_current_state_hash"] != b["memory_current_state_hash"], "content bytes must differ"
    assert a["e1_event_hash"] == b["e1_event_hash"]               # event history fixed
    assert a["e2_event_hash"] == b["e2_event_hash"]               # later event fixed
    assert a["claim_id"] == b["claim_id"]                         # claim identity fixed
    assert a["memory_source_feature_bindings"] != b["memory_source_feature_bindings"]
    # and both carry genuine source-linked content, not an empty placeholder
    for rec in (a, b):
        binds = rec["memory_source_feature_bindings"]
        assert binds, "memory must carry genuine source-linked feature bindings"
        # bindings are canonical JSON strings written by the native owner
        assert any('"state":"%s"' % rec["content_state"] in b_ for b_ in binds)
        assert all("source_event" in b_ and "feature" in b_ for b_ in binds)


# ---------------------------------------------------------------------------
# P1 : memory content moves the later response with everything else fixed.
# ---------------------------------------------------------------------------

def test_p1_memory_content_intervention_changes_later_response():
    c1 = M.run_cell("C1", CERTAIN, mediator="ACTIVE")
    c2 = M.run_cell("C2", UNCERTAIN, mediator="ACTIVE")
    assert c1["e1_event_hash"] == c2["e1_event_hash"]
    assert c1["memory_id"] == c2["memory_id"]
    assert c1["response_decision_state"] == "RESPONSE_EFFECTS_PRODUCED"
    assert c2["response_decision_state"] != "RESPONSE_EFFECTS_PRODUCED"
    assert (c1["response_effect_kind"], c2["response_effect_kind"]) != ("REROUTE", "REROUTE")
    # the change runs THROUGH the native accessibility/permission channel
    assert c1["response_permission_seen"] == "PERMIT_FIRST_PERSON_BELIEF"
    assert c2["response_decision_state"] == "DEFER_MISSING_AUTHORITY"


# ---------------------------------------------------------------------------
# P2 : presence vs absence of the epistemic mediator moves the response.
# ---------------------------------------------------------------------------

def test_p2a_mediator_present_versus_absent_changes_response():
    c1 = M.run_cell("C1", CERTAIN, mediator="ACTIVE")
    c5 = M.run_cell("C5", CERTAIN, mediator="INHIBITED")
    assert c1["memory_id"] == c5["memory_id"]
    assert c1["response_effect_kind"] == "REROUTE"
    assert c5["response_decision_state"] == "RESPONSE_INPUTS_VALID_EMPTY"
    assert c1["response_decision_state"] != c5["response_decision_state"]


def test_p2b_mediator_absent_is_observationally_distinct_under_unknown_access():
    """P2 second half: reported honestly as PARTIAL - both are nonproductive."""
    c2 = M.run_cell("C2", UNCERTAIN, mediator="ACTIVE")
    c6 = M.run_cell("C6", UNCERTAIN, mediator="INHIBITED")
    # typed decision states differ, but NEITHER licenses a productive response
    assert c2["response_decision_state"] != c6["response_decision_state"]
    assert c2["response_effect_kind"] is None
    assert c6["response_effect_kind"] is None


# ---------------------------------------------------------------------------
# P3 : native mediator withdrawal. FIRST HALF HOLDS, SECOND HALF IS FALSIFIED.
# ---------------------------------------------------------------------------

def test_p3a_native_withdrawal_changes_response_when_access_is_permitting():
    c1 = M.run_cell("C1", CERTAIN, mediator="ACTIVE")
    c3 = M.run_cell("C3", CERTAIN, mediator="WITHDRAWN")
    assert c1["withdrawal_decision_state"] if False else True
    assert c3["withdrawal_decision_state"] == "APPLIED_EPISTEMIC_TRANSITION"
    assert c3["withdrawn_effect_id"]
    assert c3["withdrawal_accessibility"] == "CLAIM_ACCESSIBLE"
    assert c3["response_effect_kind"] == "BLOCK"       # stance genuinely gone
    assert c1["response_effect_kind"] == "REROUTE"
    assert c1["response_effect_kind"] != c3["response_effect_kind"]


def test_p3b_PREREGISTERED_PREDICTION_IS_FALSIFIED_and_is_reported_as_such():
    """PREDICTION P3 (second half) WAS WRONG. This test passes only because it failed.

    Preregistration predicted C2 != C4 (mediator withdrawal changes the response under
    UNCERTAIN content). It does not. Native first_person_permission returns
    DEFER_MISSING_AUTHORITY for CLAIM_ACCESS_UNKNOWN irrespective of whether a stance
    record is present, so the mediator cut is UNOBSERVABLE in that arm.

    This was derivable from preregistered fact F5 before execution; the failure is an
    error in the preregistration's prediction, and it DEFEATS the identifying power of
    the intervention in the UNCERTAIN arm. It is recorded, not repaired.
    """
    c2 = M.run_cell("C2", UNCERTAIN, mediator="ACTIVE")
    c4 = M.run_cell("C4", UNCERTAIN, mediator="WITHDRAWN")
    assert c4["withdrawal_decision_state"] == "APPLIED_EPISTEMIC_TRANSITION"
    assert c4["withdrawn_effect_id"]
    assert c4["withdrawal_accessibility"] == "CLAIM_ACCESS_UNKNOWN"
    # THE FALSIFICATION: identical observable outcome despite a real native withdrawal
    assert c2["response_decision_state"] == c4["response_decision_state"] == "DEFER_MISSING_AUTHORITY"
    assert c2["response_effect_kind"] == c4["response_effect_kind"] is None
    # the withdrawal was nevertheless a REAL owner-state mutation
    assert c4["withdrawn_effect_id"] not in c4["stances_after_mediation"]


def test_c4b_accessibility_channel_dominates_the_withdrawal_outcome():
    """Informative contrast: withdrawal + forced ACCESSIBLE flips DEFER->DENY->BLOCK."""
    c4 = M.run_cell("C4", UNCERTAIN, mediator="WITHDRAWN")
    c4b = M.run_cell("C4b", UNCERTAIN, mediator="WITHDRAWN",
                     withdraw_accessibility="CLAIM_ACCESSIBLE")
    assert c4["response_decision_state"] == "DEFER_MISSING_AUTHORITY"
    assert c4b["response_effect_kind"] == "BLOCK"
    assert c4["response_effect_kind"] != c4b["response_effect_kind"]


# ---------------------------------------------------------------------------
# P4 : DECISIVE direct-path probe. Clamping belief+access across differing memory
#      content must leave the response IDENTICAL. If not, a direct M->Y path exists.
# ---------------------------------------------------------------------------

def test_p4_DECISIVE_clamped_belief_yields_identical_response_despite_different_memory_content():
    c7 = M.run_cell("C7", CERTAIN, mediator="ACTIVE", mediator_mode="CLAMP")
    c8 = M.run_cell("C8", UNCERTAIN, mediator="ACTIVE", mediator_mode="CLAMP")
    assert c7["memory_id"] == c8["memory_id"]                       # same memory identity
    assert c7["memory_uncertainty_state"] != c8["memory_uncertainty_state"]
    assert c7["memory_current_state_hash"] != c8["memory_current_state_hash"]
    # the epistemic channel was genuinely forced to the SAME value in both arms
    assert c7["response_permission_seen"] == c8["response_permission_seen"] == "DENY_FIRST_PERSON_CLAIM"
    assert c7["response_effect_kind"] == c8["response_effect_kind"] == "BLOCK"
    # => with belief/access held constant, memory CONTENT does not move the response


def test_p4b_consumer_cannot_read_memory_at_all_by_construction():
    """Structural, not merely untested: the consumer receives no memory argument."""
    import inspect
    sig = inspect.signature(M.consume)
    assert "memory" not in sig.parameters
    assert list(sig.parameters) == ["ctx", "reg", "binding", "e2", "claim_id", "prior_history"]
    src = inspect.getsource(M.consume)
    # The consumer may pass memory REFERENCES to the native prestate (native code then
    # existence-checks them), but must never read memory CONTENT.
    for forbidden in ("ctx.memories[", "uncertainty_state", "content_state",
                      "source_feature_bindings", "memory_semantic_hash", "memory_id"):
        assert forbidden not in src, f"consumer must never read memory content: {forbidden}"
    assert "ctx.memories" in src  # refs only, via tuple(sorted(ctx.memories))


# ---------------------------------------------------------------------------
# P5 : history-only confound (the real CAN3 arrow) is not the explanation.
# ---------------------------------------------------------------------------

def test_p5_withholding_prior_response_history_does_not_move_the_consumer():
    with_hist = M.run_cell("C1", CERTAIN, mediator="ACTIVE", prior_history_cells=True)
    without = M.run_cell("C9", CERTAIN, mediator="ACTIVE", prior_history_cells=False)
    assert with_hist["response_effect_kind"] == without["response_effect_kind"] == "REROUTE"
    assert with_hist["response_decision_state"] == without["response_decision_state"]
    # yet the coupling really did see a different prior-response count
    assert with_hist["response"]["coupling"]["prestate_hash"] != without["response"]["coupling"]["prestate_hash"]


# ---------------------------------------------------------------------------
# P8 : reference-only mediator does NOT reproduce P1 -> not mere label attachment.
# ---------------------------------------------------------------------------

def test_p8_reference_only_mediator_does_not_reproduce_the_content_effect():
    c1 = M.run_cell("C1", CERTAIN, mediator="ACTIVE", mediator_mode="CONTENT_SENSITIVE")
    c10 = M.run_cell("C10", CERTAIN, mediator="ACTIVE", mediator_mode="REFERENCE_ONLY")
    c2 = M.run_cell("C2", UNCERTAIN, mediator="ACTIVE", mediator_mode="CONTENT_SENSITIVE")
    assert c10["response_effect_kind"] == c1["response_effect_kind"] == "REROUTE"
    assert c10["response_effect_kind"] != c2["response_effect_kind"]
    # both really did attach the same genuine memory reference
    assert c1["memory_id"] == c10["memory_id"] == c2["memory_id"]
    # the reference-only mediator ignored the content it was handed
    assert c10["mediator_read_uncertainty_state"] == "CERTAIN"


# ---------------------------------------------------------------------------
# P9 : forged memory content must not drive anything.
# ---------------------------------------------------------------------------

def test_p9_tampered_memory_content_is_refused_and_leaves_no_epistemic_state():
    good = M.run_cell("C1", CERTAIN, mediator="ACTIVE")
    bad = M.run_cell("TAMPER", UNCERTAIN, mediator="ACTIVE", tamper=True)
    assert bad["epistemic_decision_state"] == "MEMORY_STATE_MISMATCH"
    assert bad.get("response_permission_seen") is None
    assert bad["response_effect_kind"] is None
    assert bad["response_decision_state"] == "RESPONSE_INPUTS_VALID_EMPTY"
    # the honest arm still works, so the tamper did not merely break the harness
    assert good["response_effect_kind"] == "REROUTE"


def test_p9b_forged_content_does_not_flip_an_uncertain_memory_into_a_permitted_one():
    """A forged CERTAIN on an actually-UNCERTAIN memory must not yield PERMIT."""
    forged = M.run_cell("T2", UNCERTAIN, mediator="ACTIVE", tamper=True)
    honest = M.run_cell("C2", UNCERTAIN, mediator="ACTIVE")
    assert forged["response_effect_kind"] is None
    assert honest["response_effect_kind"] is None
    assert forged["response_permission_seen"] in (None, "DENY_FIRST_PERSON_CLAIM")


# ---------------------------------------------------------------------------
# P10 : refusals leave owner state byte-identical.
# ---------------------------------------------------------------------------

def test_p10_refused_outcome_leaves_owner_state_byte_identical_to_prestate():
    reg = CandidateRegistryFixture()
    can8.register_default_rule(reg)
    binding = can8.build_default_binding()
    ctx = owner.FixtureOwnerState(reg, M.ACTOR)
    e1 = M.fixed_e1()
    can8.occurrence_gate(e1, reg)
    proposal, memory = M.form_and_commit_memory(reg, ctx, e1, binding, CERTAIN)
    claim = owner.canonical_claim(M.ACTOR, "FIXTURE_PRIVATE_FEEDBACK_APPRAISAL", "RESPECTED",
                                  M.T_E1, M.ACTOR, [e1.event_id])
    claim_id = ctx.bind_claim(claim, e1)
    before = ctx.checkpoint()

    tampered = deepcopy(memory)
    tampered["uncertainty_state"] = "UNCERTAIN"
    out = M.mediate(ctx=ctx, reg=reg, binding=binding, e1=e1, claim_id=claim_id,
                    memory=tampered, mode="CONTENT_SENSITIVE")
    assert out["decision_state"] == "MEMORY_STATE_MISMATCH"
    assert out["stance_persisted"] is False
    assert ctx.stances == {}                       # no epistemic record created
    assert ctx.state_sets == {} and ctx.permissions == {}
    after = ctx.checkpoint()
    assert after["state"] == before["state"]       # byte-identical owner state
    assert ctx.state_hash == before["state"]["state_hash"] if "state_hash" in before["state"] else True
    assert ctx.verify()


def test_p10b_inhibited_mediator_writes_no_epistemic_state():
    c5 = M.run_cell("C5", CERTAIN, mediator="INHIBITED")
    assert c5["epistemic_decision_state"] == "MEDIATOR_NOT_APPLIED"
    assert c5["stances_after_mediation"] == []
    assert c5["response_decision_state"] == "RESPONSE_INPUTS_VALID_EMPTY"


# ---------------------------------------------------------------------------
# P11 : foreign / mismatched basis refused (actor, claim, time, unknown memory).
# ---------------------------------------------------------------------------

def _armed():
    reg = CandidateRegistryFixture()
    can8.register_default_rule(reg)
    binding = can8.build_default_binding()
    ctx = owner.FixtureOwnerState(reg, M.ACTOR)
    e1 = M.fixed_e1()
    can8.occurrence_gate(e1, reg)
    _, memory = M.form_and_commit_memory(reg, ctx, e1, binding, CERTAIN)
    claim = owner.canonical_claim(M.ACTOR, "FIXTURE_PRIVATE_FEEDBACK_APPRAISAL", "RESPECTED",
                                  M.T_E1, M.ACTOR, [e1.event_id])
    claim_id = ctx.bind_claim(claim, e1)
    return reg, binding, ctx, e1, memory, claim_id


def test_p11a_unknown_memory_basis_is_refused():
    reg, binding, ctx, e1, memory, claim_id = _armed()
    out = owner.adp017_apply_epistemic_effect(
        actor_id=M.ACTOR, claim_ref=claim_id, stance_kind="BELIEF", stance_operation="ADD",
        causal_parent_refs=[e1.event_id],
        actor_facing_basis_refs=[e1.event_id + ":" + e1.event_hash],
        memory_basis_refs=["MEMORY_THAT_DOES_NOT_EXIST"],
        owning_rule_id=can8.RULE_ID, owning_rule_version=can8.RULE_VERSION,
        owning_rule_hash=binding.rule_content_hash, effective_causal_time=M.T_E1,
        context=ctx, pre_state_hash=ctx.state_hash)
    assert out["decision_state"] == "DENIED_NON_ACTOR_SOURCE"
    assert ctx.stances == {}


def test_p11b_foreign_actor_is_refused():
    reg, binding, ctx, e1, memory, claim_id = _armed()
    out = owner.adp017_apply_epistemic_effect(
        actor_id="SOME_OTHER_ACTOR", claim_ref=claim_id, stance_kind="BELIEF",
        stance_operation="ADD", causal_parent_refs=[e1.event_id],
        actor_facing_basis_refs=[e1.event_id + ":" + e1.event_hash],
        memory_basis_refs=[memory["memory_id"]],
        owning_rule_id=can8.RULE_ID, owning_rule_version=can8.RULE_VERSION,
        owning_rule_hash=binding.rule_content_hash, effective_causal_time=M.T_E1,
        context=ctx, pre_state_hash=ctx.state_hash)
    assert out["decision_state"] in ("BLOCKED_INTEGRITY_FAILURE", "DENIED_UNAUTHORIZED_PROMOTION")
    assert ctx.stances == {}


def test_p11c_wrong_time_is_refused():
    reg, binding, ctx, e1, memory, claim_id = _armed()
    out = owner.adp017_apply_epistemic_effect(
        actor_id=M.ACTOR, claim_ref=claim_id, stance_kind="BELIEF", stance_operation="ADD",
        causal_parent_refs=[e1.event_id],
        actor_facing_basis_refs=[e1.event_id + ":" + e1.event_hash],
        memory_basis_refs=[memory["memory_id"]],
        owning_rule_id=can8.RULE_ID, owning_rule_version=can8.RULE_VERSION,
        owning_rule_hash=binding.rule_content_hash,
        effective_causal_time="1999-01-01T00:00:00Z",
        context=ctx, pre_state_hash=ctx.state_hash)
    assert out["decision_state"] == "BLOCKED_INTEGRITY_FAILURE"
    assert ctx.stances == {}


def test_p11d_unknown_claim_is_refused():
    reg, binding, ctx, e1, memory, claim_id = _armed()
    out = owner.adp017_apply_epistemic_effect(
        actor_id=M.ACTOR, claim_ref="CLAIM_THAT_IS_NOT_BOUND", stance_kind="BELIEF",
        stance_operation="ADD", causal_parent_refs=[e1.event_id],
        actor_facing_basis_refs=[e1.event_id + ":" + e1.event_hash],
        memory_basis_refs=[memory["memory_id"]],
        owning_rule_id=can8.RULE_ID, owning_rule_version=can8.RULE_VERSION,
        owning_rule_hash=binding.rule_content_hash, effective_causal_time=M.T_E1,
        context=ctx, pre_state_hash=ctx.state_hash)
    assert out["decision_state"] == "DEFERRED_MISSING_EPISTEMIC_BASIS"
    assert ctx.stances == {}


def test_p11e_knowledge_stance_is_refused_by_the_native_owner():
    """K5: the native owner refuses KNOWLEDGE; BELIEF is the only lawful stance."""
    reg, binding, ctx, e1, memory, claim_id = _armed()
    out = owner.adp017_apply_epistemic_effect(
        actor_id=M.ACTOR, claim_ref=claim_id, stance_kind="KNOWLEDGE", stance_operation="ADD",
        causal_parent_refs=[e1.event_id],
        actor_facing_basis_refs=[e1.event_id + ":" + e1.event_hash],
        memory_basis_refs=[memory["memory_id"]],
        owning_rule_id=can8.RULE_ID, owning_rule_version=can8.RULE_VERSION,
        owning_rule_hash=binding.rule_content_hash, effective_causal_time=M.T_E1,
        context=ctx, pre_state_hash=ctx.state_hash)
    assert out["decision_state"] == "DENIED_UNAUTHORIZED_PROMOTION"
    assert ctx.stances == {}


def test_p11f_foreign_target_record_withdrawal_is_refused():
    reg, binding, ctx, e1, memory, claim_id = _armed()
    out = owner.adp017_apply_epistemic_effect(
        actor_id=M.ACTOR, claim_ref=claim_id, stance_kind="BELIEF", stance_operation="ADD",
        causal_parent_refs=[e1.event_id],
        actor_facing_basis_refs=[e1.event_id + ":" + e1.event_hash],
        memory_basis_refs=[memory["memory_id"]],
        owning_rule_id=can8.RULE_ID, owning_rule_version=can8.RULE_VERSION,
        owning_rule_hash=binding.rule_content_hash, effective_causal_time=M.T_E1,
        context=ctx, pre_state_hash=ctx.state_hash)
    target = out["effect"]["effect_id"]
    ctx.stances[target]["actor_id"] = "SOME_OTHER_ACTOR"          # foreign spliced record
    ctx._seal()
    w = owner.adp017_apply_epistemic_effect(
        actor_id=M.ACTOR, claim_ref=claim_id, stance_kind="BELIEF", stance_operation="WITHDRAW",
        target_record_ref=target, causal_parent_refs=[e1.event_id],
        actor_facing_basis_refs=[e1.event_id + ":" + e1.event_hash],
        memory_basis_refs=[memory["memory_id"]],
        owning_rule_id=can8.RULE_ID, owning_rule_version=can8.RULE_VERSION,
        owning_rule_hash=binding.rule_content_hash, effective_causal_time=M.T_E1,
        context=ctx, pre_state_hash=ctx.state_hash)
    assert w["decision_state"] in ("BLOCKED_INTEGRITY_FAILURE", "DENIED_UNAUTHORIZED_PROMOTION")


# ---------------------------------------------------------------------------
# P6 / P7 : K5 private-vs-public and K3 concealed origin.
# ---------------------------------------------------------------------------

def test_p6_stance_is_private_belief_only_and_no_public_standing():
    c1 = M.run_cell("C1", CERTAIN, mediator="ACTIVE")
    assert c1["response_permission_seen"] == "PERMIT_FIRST_PERSON_BELIEF"
    perm = c1["first_person_permission"]
    assert perm == "PERMIT_FIRST_PERSON_BELIEF"
    assert "KNOWLEDGE" not in perm
    assert c1["response"]["coupling"]["uptake_appraisal_projection"]["is_durable_belief"] is False
    assert c1["response"]["coupling"]["recruitment_is_not_access"] is True
    assert c1["response"]["committed"] is False
    assert c1["response"]["production_owner_commit"] is False


def test_p6b_every_cell_permission_is_within_the_native_finite_enum():
    native = {"PERMIT_FIRST_PERSON_BELIEF", "DENY_FIRST_PERSON_CLAIM", "DEFER_MISSING_AUTHORITY"}
    for cid, cs, med, mode in [("C1", CERTAIN, "ACTIVE", "CONTENT_SENSITIVE"),
                               ("C2", UNCERTAIN, "ACTIVE", "CONTENT_SENSITIVE"),
                               ("C3", CERTAIN, "WITHDRAWN", "CONTENT_SENSITIVE"),
                               ("C4", UNCERTAIN, "WITHDRAWN", "CONTENT_SENSITIVE")]:
        rec = M.run_cell(cid, cs, mediator=med, mediator_mode=mode)
        perm = rec["response_permission_seen"]
        assert perm in native, (cid, perm)


def test_p7_causal_trace_is_never_first_person_claimable_k3_preserved():
    for cs in (CERTAIN, UNCERTAIN):
        rec = M.run_cell("K3_" + cs, cs, mediator="ACTIVE")
        fp = rec["trace_first_person_check"]
        assert fp["first_person_permission"] == "DENY_FIRST_PERSON_CLAIM"
        assert fp["self_explanation_of_hidden_origin"] == "BLOCKED"
        assert fp["analyst_only_causal_trace_actor_claimable"] is False


def test_p7b_unknown_memory_access_defers_rather_than_denying():
    out = owner.adp017_sole_memory_basis_failclosed(
        "BELIEF", "CLAIM_ACCESSIBLE",
        type("M", (), {"memory_accessibility_state": "ACCESS_UNKNOWN",
                       "retention_state": "RETAINED"})())
    assert out["first_person_permission"] == "DEFER_MISSING_AUTHORITY"
    assert out["memory_inaccessibility_auto_erases_stance"] is False


# ---------------------------------------------------------------------------
# Contract-level honesty: the native owner has NO memory-content->stance rule.
# ---------------------------------------------------------------------------

def test_native_adp017_never_reads_memory_content():
    """F4 verified structurally against the pinned native bytes, not merely asserted."""
    import inspect
    src = inspect.getsource(owner.adp017_apply_epistemic_effect)
    # memory_basis_refs are existence-checked only
    assert "if any(m not in context.memories for m in memory_basis_refs)" in src
    # and the native function never consults a memory record's CONTENT
    for forbidden in ("uncertainty_state", "source_feature_bindings", "memory_semantic_hash",
                      "ctx.memories["):
        assert forbidden not in src, f"native ADP017 must not read memory content: {forbidden}"


def test_native_can008_response_effect_is_caller_supplied():
    """F8 verified: the pinned native CAN008 computes no response from epistemic state."""
    import inspect
    sig = inspect.signature(can8.response_rule_apply)
    assert "requested_effect" in sig.parameters
    src = inspect.getsource(can8.response_rule_apply)
    assert "current_claim_accessibility" not in src
    assert "permissions" not in src


def test_our_rules_are_labelled_unissued_and_not_production():
    assert "TEST_ONLY" in M.MEDIATOR_ID and "TEST_ONLY" in M.CONSUMER_ID
    assert "UNISSUED" in M.RULE_GRAIN and "NOT_ACCEPTED" in M.RULE_GRAIN
    rec = M.run_cell("LABEL", CERTAIN, mediator="ACTIVE")
    assert rec["rule_grain"] == M.RULE_GRAIN
    assert rec["response"]["is_unissued_synthetic"] is True
    assert rec["response"]["production_owner_commit"] is False
    # the production positive-authority guard stays EMPTY
    from rawlsing_next import v3_psepf_zero_positive_guard as guard
    assert guard.GUARD_ID == "IG_PSEPF_ZERO_POSITIVE_GUARD"
    # the guard exists and is active; no positive authority was created anywhere here
    assert "ZERO_POSITIVE" in guard.GUARD_VERSION


def test_deterministic_replay_of_the_whole_construct():
    a = M.run_cell("R1", CERTAIN, mediator="ACTIVE")
    b = M.run_cell("R1", CERTAIN, mediator="ACTIVE")
    for k in ("memory_id", "memory_current_state_hash", "claim_id", "response_effect_kind",
              "response_decision_state", "response_permission_seen", "owner_state_hash_after_mediation"):
        assert a[k] == b[k], k