"""HQ316 MS1 — SERIAL ADP016 -> ADP017 -> CAN008 mediation experiment harness.

GRAIN: SOURCEFREE_SYNTHETIC_TEST_ONLY. NOT ADOPTED. NOT A SEMANTIC ISSUER.
NOT PRODUCTION. NOT V3 OPERATION. NO HUMAN PSYCHOLOGICAL CLAIM.

This module contains the two HYPOTHETICAL, UNISSUED test-only rules declared in
01_PREREGISTRATION.md:

  * MS1_SERIAL_MEDIATOR@1.0.0-TEST_ONLY   - reads real memory CONTENT, maps it to a
    native ADP017 accessibility class, applies via the REAL native transition.
  * MS1_SERIAL_CONSUMER@1.0.0-TEST_ONLY  - reads real EPISTEMIC owner state only
    (it receives full ctx; its epistemic choice restriction is authored, not
    type-enforced exclusion of every direct dependence), and applies its choice through the REAL native CAN008
    coupline_evaluate / response_rule_apply / build_response_receipt.

Everything else imported here is pinned native candidate source, staged byte-exact
from CAN2 authored commit ee6a48b40247b113c614fe2099d4c443e8dd7bb7.
"""
from __future__ import annotations

import hashlib
import ms3_native_custody as custody
import json
import sys
from copy import deepcopy
from pathlib import Path

_RUNTIME = Path(__file__).resolve().parent / "runtime"
if str(_RUNTIME) not in sys.path:
    sys.path.insert(0, str(_RUNTIME))

from candidate import can008_candidate_rule as can8           # noqa: E402
from candidate import owner_transitions as owner              # noqa: E402
from candidate import positive_chain as chain                 # noqa: E402
from candidate.candidate_registry_fixture import (            # noqa: E402
    CandidateRegistryFixture,
    digest,
    parse_time,
)

MEDIATOR_ID = "MS1_SERIAL_MEDIATOR@1.0.0-TEST_ONLY"
CONSUMER_ID = "MS1_SERIAL_CONSUMER@1.0.0-TEST_ONLY"
RULE_GRAIN = "SOURCEFREE_SYNTHETIC_TEST_ONLY__UNISSUED__NOT_ACCEPTED__NOT_V3"

ACTOR = "ACTOR_SYNTH_1"
WORLD = "W_SYNTH_1998"
WORLD_AS_OF = "1998-10-03T16:00:00Z"
T_E1 = "1998-10-03T16:00:00Z"
T_E2 = "1998-11-20T09:00:00Z"

MEMORY_CONTENT_CERTAIN = "AVAILABLE_SOURCE_BOUND"
MEMORY_CONTENT_UNCERTAIN = "AVAILABLE_UNCERTAIN"

# native, transcribed from adopted_contract.first_person_permission
PERMISSION_TO_EFFECT = {
    "PERMIT_FIRST_PERSON_BELIEF": "REROUTE",
    "DENY_FIRST_PERSON_CLAIM": "BLOCK",
    # DEFER_MISSING_AUTHORITY and "no state at all" are NOT productive effects.
}


def refuse(code, detail=""):
    return dict(decision_state=code, code=code, status="REFUSED", committed=False,
                detail=detail, production_owner_commit=False, stance_persisted=False)


# ---------------------------------------------------------------------------
# Fixed exogenous events. Identical bytes in every cell (P1 requires this).
# ---------------------------------------------------------------------------

def fixed_e1():
    return chain.seal_event(
        event_id="EV1_FEEDBACK_WINDOW_ENCOUNTER",
        issuer_authority_id="ISSUER_AUTH_WORLD_SCHED",
        issuer_authority_version="1",
        event_kind="EXTERNAL_RUNTIME_EVENT",
        effective_causal_time=T_E1,
        actor_scope=ACTOR,
        world_ref=WORLD,
        world_as_of=WORLD_AS_OF,
        admission_state="ADMITTED",
        public_features=("shift_feedback_window_open", "supervisor_solicits_comment"),
    )


def fixed_e2():
    return chain.seal_event(
        event_id="EV2_LATER_SHIFT_CHANGE_REQUEST",
        issuer_authority_id="ISSUER_AUTH_INSTITUTION",
        issuer_authority_version="1",
        event_kind="EXTERNAL_RUNTIME_EVENT",
        effective_causal_time=T_E2,
        actor_scope=ACTOR,
        world_ref=WORLD,
        world_as_of=WORLD_AS_OF,
        admission_state="ADMITTED",
        public_features=("shift_change_request_window",),
    )


# ---------------------------------------------------------------------------
# Stage 1: real native ADP016 formation + commit of memory with real content.
# ---------------------------------------------------------------------------

def _form_and_commit_memory_unchecked(reg, ctx, e1, binding, content_state):
    """Real native ADP016 formation, then the real native owner commit.

    Returns (proposal, memory_dict) or (None, refusal_dict).
    """
    before = ctx.checkpoint()
    try:
        proposal = owner.adp016_form_causal_trace(
            actor_id=ACTOR, basis_event=e1,
            trace_key="TRACE_FEEDBACK_WINDOW_EXPERIENCE",
            content_state=content_state,
            owning_rule_id=can8.RULE_ID, owning_rule_version=can8.RULE_VERSION,
            owning_rule_hash=binding.rule_content_hash,
            authority_id="WORKER_CANDIDATE_FIXTURE", authority_version="1",
            parent_state_hash=ctx.state_hash, context=ctx,
        )
        if proposal.get("status") != "ADP016_FORMATION_VALIDATED_IN_FIXTURE":
            return None, refuse("DEFERRED_MISSING_MEMORY_BASIS")
        commit = ctx.commit_memory(proposal)
        if commit.get("status") != "ADP016_TRACE_COMMITTED_IN_FIXTURE":
            return None, refuse(commit.get("status", "MEMORY_COMMIT_REFUSED"))
        return proposal, proposal["memory"]
    except owner.OwnerTransitionError as exc:
        ctx.restore(before)
        return None, refuse(exc.code, exc.detail)


# ---------------------------------------------------------------------------
# HYPOTHETICAL RULE 1: MS1_SERIAL_MEDIATOR@1.0.0-TEST_ONLY
# Reads REAL memory CONTENT from ACTUAL owner state; decides ONLY the native
# accessibility class; applies through the REAL native ADP017 transition.
# ---------------------------------------------------------------------------

def _verify_memory_provenance(ctx, reg, memory):
    """Re-derive the memory identity and its causal provenance from owner state."""
    mid = memory["memory_id"]
    if mid not in ctx.memories:
        return "UNKNOWN_MEMORY_ID"
    if ctx.memories[mid] != memory:
        return "MEMORY_STATE_MISMATCH"
    if memory.get("current_state_hash") != owner.memory_semantic_hash(memory):
        return "INTEGRITY_FAILURE"
    if memory.get("integrity_state") != "INTACT":
        return "INTEGRITY_FAILURE"
    tid = memory.get("formation_transition_id")
    if not tid or tid not in ctx.memory_transitions:
        return "UNKNOWN_FORMATION_TRANSITION"
    if ctx.memory_transitions[tid].get("memory_id") != mid:
        return "INTEGRITY_FAILURE"
    if memory.get("actor_id") != ACTOR:
        return "ACTOR_MISMATCH"
    if memory.get("representation_kind") != "CAUSAL_TRACE_MEMORY":
        return "INELIGIBLE_REPRESENTATION"
    for ref in memory.get("objective_source_event_refs", ()):
        eid, _, ehash = ref.partition(":")
        ev = reg.event(eid)
        if ev is None or ev["event_hash"] != ehash:
            return "SOURCE_EVENT_NOT_ADMITTED"
    if not memory.get("source_feature_bindings"):
        return "MISSING_SOURCE_FEATURE_BINDINGS"
    try:
        custody.validate(ctx, reg, can8.build_default_binding(), fixed_e1())
    except Exception as exc:
        return str(exc) if isinstance(exc, custody.NativeProofError) else "MS3_NATIVE_MEMORY_INVALID"
    return None


def _mediate_unchecked(*, ctx, reg, binding, e1, claim_id, memory,
            mode="CONTENT_SENSITIVE", tamper=False):
    """Apply the hypothetical mediator and the REAL native ADP017 transition.

    mode:
      CONTENT_SENSITIVE - preregistered map from real memory content (the experiment)
      CLAMP             - ignores content, forces CLAIM_INACCESSIBLE (decisive probe)
      REFERENCE_ONLY    - ignores content, forces CLAIM_ACCESSIBLE (falsifier)
    """
    probe = deepcopy(memory)
    if tamper:
        # forge the CONTENT while leaving identity/metadata intact
        probe["uncertainty_state"] = "CERTAIN" if memory.get("uncertainty_state") != "CERTAIN" else "UNCERTAIN"

    bad = _verify_memory_provenance(ctx, reg, probe)
    if bad is not None:
        return refuse(bad, "mediator provenance verification failed")

    uncertainty = probe.get("uncertainty_state")
    if mode == "CONTENT_SENSITIVE":
        if uncertainty == "CERTAIN":
            accessibility = "CLAIM_ACCESSIBLE"
        elif uncertainty == "UNCERTAIN":
            accessibility = "CLAIM_ACCESS_UNKNOWN"
        else:
            return refuse("INELIGIBLE_NONCAUSAL_SOURCE", "unknown memory uncertainty_state")
    elif mode == "CLAMP":
        accessibility = "CLAIM_INACCESSIBLE"
    elif mode == "REFERENCE_ONLY":
        accessibility = "CLAIM_ACCESSIBLE"
    else:
        return refuse("UNAUTHORIZED_TRANSITION", "unknown mediator mode")

    result = owner.adp017_apply_epistemic_effect(
        actor_id=ACTOR, claim_ref=claim_id, stance_kind="BELIEF",
        stance_operation="ADD",
        causal_parent_refs=[e1.event_id],
        actor_facing_basis_refs=[e1.event_id + ":" + e1.event_hash],
        memory_basis_refs=[memory["memory_id"]],
        owning_rule_id=can8.RULE_ID, owning_rule_version=can8.RULE_VERSION,
        owning_rule_hash=binding.rule_content_hash,
        effective_causal_time=T_E1,
        claim_accessibility=accessibility,
        context=ctx, pre_state_hash=ctx.state_hash,
    )
    result["mediator_rule_id"] = MEDIATOR_ID
    result["mediator_mode"] = mode
    result["mediator_read_uncertainty_state"] = uncertainty
    result["is_unissued_synthetic"] = True
    return result


def _withdraw_mediator_unchecked(*, ctx, reg, binding, e1, claim_id, memory, target_effect_id,
                      claim_accessibility="CLAIM_ACCESSIBLE"):
    """Lawful NATIVE mediator withdrawal: ADP017 WITHDRAW with an exact target.

    This is a real owner-state deletion performed by pinned native code, not a
    simulation and not a flag.

    `claim_accessibility` must be the cell's OWN accessibility so that the
    intervention isolates the mediator (stance present vs absent) and does not
    silently re-map the accessibility class as well. Passing
    claim_accessibility='PRESERVE' is deliberately NOT supported: a withdrawal
    that also changes accessibility would confound the mediator cut.
    """
    result = owner.adp017_apply_epistemic_effect(
        actor_id=ACTOR, claim_ref=claim_id, stance_kind="BELIEF",
        stance_operation="WITHDRAW", target_record_ref=target_effect_id,
        causal_parent_refs=[e1.event_id],
        actor_facing_basis_refs=[e1.event_id + ":" + e1.event_hash],
        memory_basis_refs=[memory["memory_id"]],
        owning_rule_id=can8.RULE_ID, owning_rule_version=can8.RULE_VERSION,
        owning_rule_hash=binding.rule_content_hash,
        effective_causal_time=T_E1,
        claim_accessibility=claim_accessibility,
        context=ctx, pre_state_hash=ctx.state_hash,
    )
    result["withdrawal_is_native"] = True
    result["withdrawal_accessibility"] = claim_accessibility
    return result


# ---------------------------------------------------------------------------
# HYPOTHETICAL RULE 2: MS1_SERIAL_CONSUMER@1.0.0-TEST_ONLY
# Reads verified native epistemic state for choice. Full ctx remains available;
# this dependency restriction is authored, not a type-level isolation guarantee.
# ---------------------------------------------------------------------------

def consume(ctx, reg, binding, e2, claim_id, prior_history=()):
    """Validate native input; construct an uncommitted response with atomic refusal."""
    before = None
    try:
        before = (ctx.checkpoint(), reg.checkpoint())
        proof = custody.validate(ctx, reg, binding, fixed_e1(), claim_id, e2.effective_causal_time, require_selection=True)
        def apply_verified():
            """Choose the later response from real owner state, then apply native CAN008."""
            if not ctx.verify():
                return refuse("BLOCKED_INTEGRITY_FAILURE", "owner state failed verification")
            if e2.actor_scope != ACTOR or (e2.world_ref, e2.world_as_of) != (WORLD, WORLD_AS_OF):
                return refuse("BLOCK_WRONG_ACTOR_SCOPE")
            if parse_time(e2.effective_causal_time) <= parse_time(T_E1):
                return refuse("BLOCK_REVERSE_CHRONOLOGY_CAUSAL_PARENT")
        
            state_set = ctx.state_sets.get(claim_id)
            permission = ctx.permissions.get(claim_id)
        
            # Real owner state is the ONLY epistemic input.
            if state_set is None or permission is None:
                chosen = None
                decision = "RESPONSE_INPUTS_VALID_EMPTY"
                permission_seen = None
                absent_epistemic_state = True
            else:
                absent_epistemic_state = False
                permission_seen = permission.get("permission")
                if permission.get("epistemic_state_hash") != state_set.get("current_state_hash"):
                    return refuse("BLOCKED_INTEGRITY_FAILURE", "permission/epistemic snapshot mismatch")
                if state_set.get("actor_id") != ACTOR:
                    return refuse("BLOCK_WRONG_ACTOR_SCOPE")
                decision = permission_seen
                chosen = PERMISSION_TO_EFFECT.get(permission_seen)
        
            prestate = can8.OwnerPrestate(
                actor_id=ACTOR,
                adp016_memory_refs=tuple(sorted(ctx.memories)),
                adp017_claim_refs=tuple(sorted(ctx.stances)),
                prior_can008_response_count=len(prior_history),
                world_ref=WORLD, world_as_of=WORLD_AS_OF,
            )
            prestate._context = ctx
        
            # Always evaluate the SAME E2 through the real native coupline, so event
            # admission is identical in every cell (P1 requires E2 fixed).
            coupling = can8.coupline_evaluate(e2, prestate, binding, reg)
            if coupling.get("decision_state") != "COUPLING_EVALUATED":
                return refuse(coupling.get("code", coupling.get("decision_state", "RESPONSE_REFUSED")))
        
            if chosen is None:
                # No productive effect: native grammar forbids guessing under DEFER/empty.
                r = refuse(decision,
                           f"no productive response licensed by owner state "
                           f"(permission={permission_seen})")
                r["chosen_from_permission"] = permission_seen
                r["epistemic_state_absent"] = absent_epistemic_state
                r["owner_state_hash_read"] = ctx.state_hash
                r["consumer_rule_id"] = CONSUMER_ID
                r["is_unissued_synthetic"] = True
                r["committed"] = False
                r["production_owner_commit"] = False
                return r
        
            response = can8.response_rule_apply(coupling, prestate, binding, chosen)
            if response.get("decision_state") != "RESPONSE_EFFECTS_PRODUCED":
                return refuse(response.get("decision_state", "RESPONSE_REFUSED"))
            receipt = can8.build_response_receipt(e2, prestate, binding, coupling, response)
            return dict(
                decision_state="RESPONSE_EFFECTS_PRODUCED",
                chosen_from_permission=permission_seen,
                effect_kind=chosen,
                receipt=receipt,
                receipt_hash=receipt["receipt_hash"],
                coupling=deepcopy(coupling),
                owner_state_hash_read=ctx.state_hash,
                consumer_rule_id=CONSUMER_ID,
                is_unissued_synthetic=True,
                committed=False,
                production_owner_commit=False,
            )
        result = apply_verified()
        result["native_owner_provenance"] = proof
        if result.get("decision_state") != "RESPONSE_EFFECTS_PRODUCED":
            ctx.restore(before[0]); reg.restore(before[1])
        return result
    except Exception as exc:
        if before is not None:
            ctx.restore(before[0]); reg.restore(before[1])
        return refuse(str(exc) if isinstance(exc, custody.NativeProofError) else "MS3_NATIVE_CONSUMPTION_FAILURE")


def form_and_commit_memory(reg, ctx, e1, binding, content_state):
    """Actual native formation/commit, with complete rollback on refusal/exception."""
    before = None
    try:
        before = (ctx.checkpoint(), reg.checkpoint())
        custody.need(e1 == fixed_e1(), "MS3_SOURCE_EVENT_BINDING")
        custody.validate(ctx, reg, binding, fixed_e1())
        result = _form_and_commit_memory_unchecked(reg, ctx, e1, binding, content_state)
        if result[0] is None:
            ctx.restore(before[0]); reg.restore(before[1])
        else:
            custody.validate(ctx, reg, binding, fixed_e1())
        return result
    except Exception as exc:
        if before is not None:
            ctx.restore(before[0]); reg.restore(before[1])
        return None, refuse(str(exc) if isinstance(exc, custody.NativeProofError) else "MS3_NATIVE_FORMATION_FAILURE")


def mediate(*, ctx, reg, binding, e1, claim_id, memory, mode="CONTENT_SENSITIVE", tamper=False):
    """Apply the unissued map only to an exact reproducible native owner trajectory."""
    before = None
    try:
        before = (ctx.checkpoint(), reg.checkpoint())
        custody.need(e1 == fixed_e1(), "MS3_SOURCE_EVENT_BINDING")
        custody.validate(ctx, reg, binding, e1, claim_id, require_selection=True)
        result = _mediate_unchecked(ctx=ctx, reg=reg, binding=binding, e1=e1, claim_id=claim_id, memory=memory, mode=mode, tamper=tamper)
        if result.get("decision_state") != "APPLIED_EPISTEMIC_TRANSITION":
            ctx.restore(before[0]); reg.restore(before[1])
        else:
            result["native_owner_provenance"] = custody.validate(ctx, reg, binding, e1, claim_id, require_selection=True)
        return result
    except Exception as exc:
        if before is not None:
            ctx.restore(before[0]); reg.restore(before[1])
        return refuse(str(exc) if isinstance(exc, custody.NativeProofError) else "MS3_NATIVE_MEDIATION_FAILURE")


def withdraw_mediator(*, ctx, reg, binding, e1, claim_id, memory, target_effect_id, claim_accessibility="CLAIM_ACCESSIBLE"):
    """Real exact-target native withdrawal, retaining UNKNOWN semantics and rollback."""
    before = None
    try:
        before = (ctx.checkpoint(), reg.checkpoint())
        custody.need(e1 == fixed_e1(), "MS3_SOURCE_EVENT_BINDING")
        custody.validate(ctx, reg, binding, e1, claim_id, require_selection=True)
        bad = _verify_memory_provenance(ctx, reg, memory)
        if bad is not None:
            return refuse(bad)
        result = _withdraw_mediator_unchecked(ctx=ctx, reg=reg, binding=binding, e1=e1, claim_id=claim_id, memory=memory, target_effect_id=target_effect_id, claim_accessibility=claim_accessibility)
        if result.get("decision_state") != "APPLIED_EPISTEMIC_TRANSITION":
            ctx.restore(before[0]); reg.restore(before[1])
        else:
            result["native_owner_provenance"] = custody.validate(ctx, reg, binding, e1, claim_id, require_selection=True)
        return result
    except Exception as exc:
        if before is not None:
            ctx.restore(before[0]); reg.restore(before[1])
        return refuse(str(exc) if isinstance(exc, custody.NativeProofError) else "MS3_NATIVE_WITHDRAWAL_FAILURE")


# ---------------------------------------------------------------------------
# One experimental cell. Fresh identical prestates per cell (factorial design).
# ---------------------------------------------------------------------------

def run_cell(cell_id, content_state, mediator="ACTIVE", mediator_mode="CONTENT_SENSITIVE",
             tamper=False, prior_history_cells=False, withdraw_accessibility=None):
    reg = CandidateRegistryFixture()
    registration = can8.register_default_rule(reg)
    assert registration.get("status") == "CANDIDATE_REGISTERED_IN_FIXTURE"
    binding = can8.build_default_binding()
    ctx = owner.FixtureOwnerState(reg, ACTOR)
    e1, e2 = fixed_e1(), fixed_e2()
    # Admit E1 through the REAL native occurrence gate before any formation.
    gate = can8.occurrence_gate(e1, reg)
    if gate.get("status") != "ADMITTED_OCCURRENCE":
        raise AssertionError("E1 admission refused: %r" % (gate,))
    rec = dict(cell=cell_id, content_state=content_state, mediator=mediator,
               mediator_mode=mediator_mode, tampered=tamper,
               e1_event_hash=e1.event_hash, e2_event_hash=e2.event_hash,
               rule_grain=RULE_GRAIN, mediator_id=MEDIATOR_ID, consumer_id=CONSUMER_ID)

    proposal, memory = form_and_commit_memory(reg, ctx, e1, binding, content_state)
    if proposal is None:
        rec.update(stage="MEMORY_REFUSED", outcome=memory, response=None,
                   response_effect_kind=None, response_decision_state=memory.get("decision_state"))
        return rec
    rec["memory_id"] = memory["memory_id"]
    rec["memory_uncertainty_state"] = memory["uncertainty_state"]
    rec["memory_current_state_hash"] = memory["current_state_hash"]
    rec["memory_source_feature_bindings"] = list(memory["source_feature_bindings"])

    claim = owner.canonical_claim(ACTOR, "FIXTURE_PRIVATE_FEEDBACK_APPRAISAL", "RESPECTED",
                                  T_E1, ACTOR, [e1.event_id])
    claim_id = ctx.bind_claim(claim, e1)
    rec["claim_id"] = claim_id

    epi = None
    if mediator == "ACTIVE":
        epi = mediate(ctx=ctx, reg=reg, binding=binding, e1=e1, claim_id=claim_id,
                      memory=memory, mode=mediator_mode, tamper=tamper)
        rec["epistemic_decision_state"] = epi.get("decision_state")
        rec["mediator_read_uncertainty_state"] = epi.get("mediator_read_uncertainty_state")
    elif mediator == "WITHDRAWN":
        first = mediate(ctx=ctx, reg=reg, binding=binding, e1=e1, claim_id=claim_id,
                        memory=memory, mode=mediator_mode, tamper=tamper)
        rec["epistemic_decision_state"] = first.get("decision_state")
        rec["mediator_read_uncertainty_state"] = first.get("mediator_read_uncertainty_state")
        target = first.get("effect", {}).get("effect_id")
        if withdraw_accessibility is None:
            # preserve THIS cell's own accessibility, isolating the mediator cut
            acc_seen = first.get("effect", {})
            ss = (ctx.state_sets.get(claim_id) or {}).get("current_claim_accessibility")
            withdraw_accessibility = ss or "CLAIM_ACCESSIBLE"
        w = withdraw_mediator(ctx=ctx, reg=reg, binding=binding, e1=e1, claim_id=claim_id,
                              memory=memory, target_effect_id=target,
                              claim_accessibility=withdraw_accessibility)
        rec["withdrawal_decision_state"] = w.get("decision_state")
        rec["withdrawn_effect_id"] = target
        rec["withdrawal_accessibility"] = w.get("withdrawal_accessibility")
        rec["accessibility_before_withdrawal"] = (ctx.state_sets.get(claim_id) or {}).get("current_claim_accessibility")
    elif mediator == "INHIBITED":
        rec["epistemic_decision_state"] = "MEDIATOR_NOT_APPLIED"
    else:
        raise ValueError("unknown mediator state")

    rec["stances_after_mediation"] = sorted(ctx.stances)
    rec["owner_state_hash_after_mediation"] = ctx.state_hash

    # The consumer is passed the claim id ONLY - never a memory.
    response = consume(ctx, reg, binding, e2, claim_id,
                       prior_history=() if not prior_history_cells else ("PRIOR",))
    rec["response"] = response
    rec["response_effect_kind"] = response.get("effect_kind")
    rec["response_decision_state"] = response.get("decision_state")
    rec["response_permission_seen"] = response.get("chosen_from_permission")

    # K5 / K3 invariants recorded from real owner state.
    perm = ctx.permissions.get(claim_id)
    rec["first_person_permission"] = perm.get("permission") if perm else None
    fp = owner.adp017_first_person_check(
        "BELIEF", (ctx.state_sets.get(claim_id) or {}).get("current_claim_accessibility",
                                                            "CLAIM_ACCESS_UNKNOWN"),
        memory["representation_kind"], memory["memory_accessibility_state"],
        context=ctx, claim_ref=claim_id,
        state_hash=(ctx.state_sets.get(claim_id) or {}).get("current_state_hash"))
    rec["trace_first_person_check"] = fp
    return rec


def cell(cell_id, content_state, **kw):
    return run_cell(cell_id, content_state, **kw)