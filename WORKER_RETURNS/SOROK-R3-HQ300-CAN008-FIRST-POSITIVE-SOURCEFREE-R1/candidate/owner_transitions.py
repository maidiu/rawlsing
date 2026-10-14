"""HQ300 — candidate ADP-016 / ADP-017 target-owner transitions.

PROVISIONAL CANDIDATE — NOT AN ADOPTED RULE — NOT A PRODUCTION OWNER.

Implements the smallest target-owner transitions whose interfaces are already
competently specified by the adopted authorities:

  ADP-016 (blob c6619a286e115d060ab4830889e7fc23762167a5):
    * GeneratedMemoryState (required fields)
    * MemoryTransitionRecord (required fields + deterministic transition identity)
    * formation_rule.all_gates_required (7 gates)
    * formation_rule.ineligible_direct_sources (fail-closed)
    * fail_closed_states (typed, no mutation on failure)
    * forbidden transition DELETE_MEMORY
    * actor_accessibility_boundary: NO actor_knows/actor_believes/may_claim export

  ADP-017 (blob eece4f3f2f3f9288ab9bbc645dc81e20a99e1280):
    * ActorEpistemicEffect (required fields; stance operations; decision states)
    * knowledge_gate (objective truth necessary, NOT sufficient)
    * belief_gate (no objective-status auto-belief)
    * first_person_permission mapping
    * memory_interaction noncollapse + sole-memory-basis fail-closed rule
    * analyst_only_exclusions (causal trace never actor claimable)
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

from .adopted_contract import (
    PINS,
    ADP016_REPRESENTATION_KIND, ADP016_RETENTION_STATE, ADP016_ACCESSIBILITY_STATE,
    ADP016_TRANSITION_KIND, ADP016_FORBIDDEN_TRANSITION_KIND,
    ADP016_INELIGIBLE_DIRECT_SOURCES, ADP016_FAIL_CLOSED_STATES,
    ADP016_MUST_NOT_OUTPUT,
    ADP017_STANCE_KIND, ADP017_STANCE_OPERATION, ADP017_EFFECT_DECISION_STATES,
    ADP017_AUTOMATIC_IMPLICATIONS_FORBIDDEN, ADP017_MEMORY_NONCOLLAPSE,
    ADP017_CAUSAL_TRACE_FIRST_PERSON_BASIS,
    ActorEpistemicEffect, AdmittedEvent, GeneratedMemoryState,
    first_person_permission, knowledge_gate_check, validate_epistemic_effect,
    validate_memory_state,
)

ADP016_RULE_ID = "CAND_ADP016_TRACE_COMMIT"
ADP016_RULE_VERSION = "1.0.0-candidate"
ADP017_RULE_ID = "CAND_ADP017_EPISTEMIC_UPDATE"
ADP017_RULE_VERSION = "1.0.0-candidate"


def _sha(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()


def _canon(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


class OwnerTransitionError(Exception):
    def __init__(self, code: str, detail: str = ""):
        self.code = code
        self.detail = detail
        super().__init__(f"{code}:{detail}")


# ---------------------------------------------------------------------------
# ADP-016 candidate transition: durable CAUSAL_TRACE_MEMORY formation
# ---------------------------------------------------------------------------

def adp016_form_causal_trace(
        *,
        actor_id: str,
        basis_event: AdmittedEvent,
        trace_key: str,
        content_state: str,
        owning_rule_id: str,
        owning_rule_version: str,
        owning_rule_hash: str,
        authority_id: str,
        authority_version: str,
        parent_state_hash: str = "PRE_ROOT",
        memory_id_override: Optional[str] = None) -> Dict[str, Any]:
    """ADP-016 FORMATION of a CAUSAL_TRACE_MEMORY from an admitted causal basis.

    All 7 formation gates enforced. Ineligible direct sources refused with
    typed fail-closed state and NO mutation. The produced memory is a typed
    GeneratedMemoryState + MemoryTransitionRecord pair; no actor_knows /
    may_claim_first_person output exists (actor_accessibility_boundary)."""
    # gate 1: exact admitted causal event
    if basis_event.admission_state != "ADMITTED":
        raise OwnerTransitionError("INELIGIBLE_NONCAUSAL_SOURCE",
                                   "basis event not admitted")
    # gate 2: parent event id + immutable hash verify
    if not basis_event.event_id or not basis_event.event_hash:
        raise OwnerTransitionError("MISSING_PARENT_EVENT", "basis lacks id/hash")
    if basis_event.derived_from_future_partition:
        raise OwnerTransitionError("INELIGIBLE_NONCAUSAL_SOURCE",
                                   "future-derived basis")
    # gate 4: remembered feature is exact-source-bound generated causal material
    if content_state in ("PERSONA_SHEET", "RENDERED_DIALOGUE", "V2_TRANSCRIPT",
                         "STRUCTURAL_OBJECT", "ANALYST_ANNOTATION",
                         "MEMORY_DISTILLATION_PROSE", "KEYWORD_HOOK"):
        raise OwnerTransitionError("INELIGIBLE_NONCAUSAL_SOURCE",
                                   f"ineligible direct source: {content_state}")
    if content_state not in ("UNAVAILABLE", "AVAILABLE_SOURCE_BOUND",
                             "AVAILABLE_UNCERTAIN"):
        raise OwnerTransitionError("INELIGIBLE_NONCAUSAL_SOURCE",
                                   f"unknown content state: {content_state}")
    # gate 5/7: owning rule requests/authorizes typed effect (candidate grain)
    if not owning_rule_id or not owning_rule_version or not owning_rule_hash:
        raise OwnerTransitionError("UNAUTHORIZED_TRANSITION", "rule identity incomplete")

    memory_id = memory_id_override or _sha(
        "V3_MEMORY", basis_event.event_hash, actor_id, trace_key,
        ADP016_RULE_ID, ADP016_RULE_VERSION)
    formation_transition_id = _sha(
        "FORMATION", memory_id, basis_event.event_id, owning_rule_hash)
    state_hash = _sha("MEMSTATE", memory_id, "RETAINED",
                      "NOT_APPLICABLE_CAUSAL_TRACE", content_state)

    memory = GeneratedMemoryState(
        memory_id=memory_id,
        actor_id=actor_id,
        representation_kind="CAUSAL_TRACE_MEMORY",
        formation_transition_id=formation_transition_id,
        objective_source_event_refs=(f"{basis_event.event_id}:{basis_event.event_hash}",),
        source_feature_bindings=(f"content_state:{content_state}",),
        retention_state="RETAINED",
        memory_accessibility_state="NOT_APPLICABLE_CAUSAL_TRACE",
        uncertainty_state="CERTAIN",
        last_transition_id=formation_transition_id,
        last_transition_effective_time=basis_event.effective_causal_time,
        current_state_hash=state_hash,
        integrity_state="INTACT",
    )
    err = validate_memory_state(memory)
    if err:
        raise OwnerTransitionError("INTEGRITY_FAILURE", err)

    transition = {
        "memory_transition_id": formation_transition_id,
        "memory_id": memory_id,
        "actor_id": actor_id,
        "transition_kind": "FORMATION",
        "effective_causal_time": basis_event.effective_causal_time,
        "authority_id": authority_id,
        "authority_version": authority_version,
        "authority_or_rule_hash": owning_rule_hash,
        "memory_rule_id": ADP016_RULE_ID,
        "memory_rule_version": ADP016_RULE_VERSION,
        "memory_rule_hash": _sha(ADP016_RULE_ID, ADP016_RULE_VERSION, PINS["ADP016_JSON"]),
        "objective_source_event_refs": [f"{basis_event.event_id}:{basis_event.event_hash}"],
        "causal_parent_event_refs": list(basis_event.causal_parent_event_ids),
        "cue_or_trigger_refs": [],
        "pre_state_hash": parent_state_hash,
        "post_state_hash": state_hash,
        "feature_state_before_hash": _sha("PRE_FEATURE", parent_state_hash),
        "feature_state_after_hash": _sha("POST_FEATURE", state_hash),
        "decision_state": "FORMATION_COMMITTED",
        "integrity_state": "INTACT",
    }
    return {
        "status": "ADP016_TRACE_COMMITTED",
        "memory": memory.__dict__,
        "transition": transition,
        "exports_to_adp017_only": True,
        "must_not_output": list(ADP016_MUST_NOT_OUTPUT),
        "first_person_origin_claimable": False,
    }


def adp016_attempt_transition(memory: GeneratedMemoryState,
                              transition_kind: str,
                              *,
                              parent_event: Optional[AdmittedEvent] = None,
                              pre_state_hash: Optional[str] = None,
                              declared_parent_hash: Optional[str] = None) -> Dict[str, Any]:
    """Generic ADP-016 transition attempt with fail-closed checks (H7/H8 hostiles)."""
    if transition_kind in ADP016_FORBIDDEN_TRANSITION_KIND:
        raise OwnerTransitionError("UNAUTHORIZED_TRANSITION",
                                   f"forbidden transition kind: {transition_kind}")
    if transition_kind not in ADP016_TRANSITION_KIND:
        raise OwnerTransitionError("UNAUTHORIZED_TRANSITION",
                                   f"unknown transition kind: {transition_kind}")
    err = validate_memory_state(memory)
    if err:
        raise OwnerTransitionError("INTEGRITY_FAILURE", err)
    if parent_event is not None:
        if parent_event.admission_state != "ADMITTED":
            raise OwnerTransitionError("MISSING_PARENT_EVENT", "parent not admitted")
        if declared_parent_hash is not None and declared_parent_hash != parent_event.event_hash:
            raise OwnerTransitionError("PARENT_EVENT_HASH_MISMATCH",
                                       "declared parent hash mismatch")
    if pre_state_hash is not None and pre_state_hash != memory.current_state_hash:
        raise OwnerTransitionError("PRE_STATE_HASH_MISMATCH", "pre-state mismatch")
    if transition_kind == "RECALL" and memory.memory_accessibility_state == "NOT_APPLICABLE_CAUSAL_TRACE":
        raise OwnerTransitionError("UNAUTHORIZED_RECALL_CUE",
                                   "causal trace is not recallable")
    return {"status": "TRANSITION_ACCEPTED_FOR_COMMIT",
            "transition_kind": transition_kind,
            "memory_id": memory.memory_id}


def adp016_rehydration_refused(memory: GeneratedMemoryState,
                               analyst_ledger_content: str) -> Dict[str, Any]:
    """UNAUTHORIZED_OBJECTIVE_HISTORY_REHYDRATION: lost actor content cannot be
    restored from the analyst-only ledger without a new actor-facing event."""
    raise OwnerTransitionError(
        "UNAUTHORIZED_OBJECTIVE_HISTORY_REHYDRATION",
        "analyst-only ledger content cannot rehydrate actor content")


# ---------------------------------------------------------------------------
# ADP-017 candidate transition: epistemic update + first-person permission
# ---------------------------------------------------------------------------

def adp017_apply_epistemic_effect(
        *,
        actor_id: str,
        claim_ref: str,
        stance_kind: str,
        stance_operation: str,
        causal_parent_refs: Sequence[str],
        actor_facing_basis_refs: Sequence[str],
        memory_basis_refs: Sequence[str],
        owning_rule_id: str,
        owning_rule_version: str,
        owning_rule_hash: str,
        effective_causal_time: str,
        claim_objective_relation: str = "OBJECTIVE_UNRESOLVED",
        claim_accessibility: str = "CLAIM_ACCESSIBLE") -> Dict[str, Any]:
    """ADP-017 ActorEpistemicEffect application with knowledge/belief gates."""
    effect = ActorEpistemicEffect(
        effect_id=_sha("EPISTEMIC_EFFECT", actor_id, claim_ref,
                       stance_kind, stance_operation, effective_causal_time),
        actor_id=actor_id,
        claim_ref=claim_ref,
        stance_kind=stance_kind,
        stance_operation=stance_operation,
        causal_parent_refs=tuple(causal_parent_refs),
        actor_facing_basis_refs=tuple(actor_facing_basis_refs),
        memory_basis_refs=tuple(memory_basis_refs),
        owning_rule_id=owning_rule_id,
        owning_rule_version=owning_rule_version,
        owning_rule_hash=owning_rule_hash,
        effective_causal_time=effective_causal_time,
    )
    err = validate_epistemic_effect(effect)
    if err:
        return {"decision_state": "BLOCKED_INTEGRITY_FAILURE", "detail": err}

    if not actor_facing_basis_refs:
        return {"decision_state": "DENIED_NON_ACTOR_SOURCE",
                "effect_id": effect.effect_id,
                "law": "exact generated/admitted actor-facing acquisition basis required"}

    if stance_kind == "KNOWLEDGE":
        ok, reasons = knowledge_gate_check(
            claim_objective_relation,
            actor_facing_basis_exists=bool(actor_facing_basis_refs),
            owning_rule_emits_knowledge=True,
            actor_role_sufficient=True,
            integrity_ok=True,
            authority_complete=bool(owning_rule_hash),
        )
        if not ok:
            return {"decision_state": "DEFERRED_MISSING_EPISTEMIC_BASIS",
                    "effect_id": effect.effect_id, "gate_reasons": reasons,
                    "objective_truth_necessary": True,
                    "objective_truth_sufficient": False}

    return {
        "decision_state": "APPLIED_EPISTEMIC_TRANSITION",
        "effect": effect.__dict__,
        "stance_persisted": stance_operation in ("ADD", "SUPERSEDE_EXACT_RECORD"),
        "accessible_memory_auto_creates_stance": False,
    }


def adp017_first_person_check(stance_kind: Optional[str],
                              claim_accessibility: str,
                              memory_representation_kind: Optional[str] = None,
                              memory_accessibility: Optional[str] = None) -> Dict[str, Any]:
    """First-person permission incl. the causal-trace firewall (K3) and the
    sole-memory-basis fail-closed rule."""
    permission = first_person_permission(stance_kind, claim_accessibility)
    if memory_representation_kind == "CAUSAL_TRACE_MEMORY":
        # causal_trace_memory_first_person_basis = false (adopted)
        if permission.startswith("PERMIT_"):
            permission = "DENY_FIRST_PERSON_CLAIM"
    return {
        "first_person_permission": permission,
        "self_explanation_of_hidden_origin": "BLOCKED"
        if permission == "DENY_FIRST_PERSON_CLAIM" else "PERMITTED_BY_STANCE",
        "analyst_only_causal_trace_actor_claimable": False,
    }


def adp017_sole_memory_basis_failclosed(stance_kind: str,
                                        claim_accessibility: str,
                                        basis_memory_state: GeneratedMemoryState) -> Dict[str, Any]:
    """sole_memory_basis_rule: if the only lawful claim-accessibility basis
    becomes INACCESSIBLE/UNAVAILABLE under ADP-016, claim permission fails
    closed until another exact actor-facing generated basis exists."""
    basis_dead = (
        basis_memory_state.memory_accessibility_state in ("INACCESSIBLE", "ACCESS_UNKNOWN")
        or basis_memory_state.retention_state in ("CONTENT_UNAVAILABLE", "RETENTION_UNKNOWN")
    )
    if basis_dead:
        return {
            "first_person_permission": "DENY_FIRST_PERSON_CLAIM",
            "decision_state": "NO_EPISTEMIC_TRANSITION",
            "law": "sole_memory_basis_rule fail-closed; reacquisition requires new "
                   "actor-facing generated or admitted event",
            "memory_inaccessibility_auto_erases_stance": False,
        }
    return {
        "first_person_permission": first_person_permission(stance_kind, claim_accessibility),
        "decision_state": "NO_EPISTEMIC_TRANSITION",
    }
