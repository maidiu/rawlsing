"""Objective Mom<->Dad relation reconciliation and asymmetric perceived states.

PROVISIONAL_LAB_RULE__NOT_ADOPTED.
One objective relation event; Mom->Dad and Dad->Mom perceived states generated
separately. No reciprocity inference, no auto household membership, conception
never equals relationship.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from .core import h_obj, h_concat, typed, S

RELATION_VERSION = "RELATION_RECONCILIATION@2.0-G13-REPAIRED"

# Kinds that can constitute a forming witness for a NEW relationship.
FORMING_WITNESS_KINDS = frozenset({
    "SHARED_ENCOUNTER", "SHARED_EVENT", "ENCOUNTER", "COMMUNITY_CALLOUT",
    "COMMISSIONED_WORK", "ENROLLMENT", "MOBILITY_HISTORY",
})


def _witness_events(dad_events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [e for e in (dad_events or []) if e.get("kind") in FORMING_WITNESS_KINDS]


def _actual_second_parent_actor(dad_events: List[Dict[str, Any]]) -> Optional[str]:
    """The ACTUAL actor identity carried by the supplied second-parent history."""
    for e in dad_events or []:
        actors = e.get("actors") or []
        if actors:
            return actors[0]
    return None


def reconcile(anchor: Dict[str, Any], dad_events: List[Dict[str, Any]],
              scenario: Dict[str, Any],
              force_mom_affectionate_dad_unknown: bool = False) -> Dict[str, Any]:
    """Reconcile identity + shared history; admit exactly one objective relation event;
    initialize directional perceived states independently.

    G13 REPAIR (defect family 7 -- relationship admission).

    The pre-repair helper IGNORED its ``dad_events`` argument entirely, minted the
    literal counterpart ``LAB_SECOND_PARENT_SELECTED``, and returned COMMITTED
    with no second-parent history and no forming witness at all. It therefore
    emitted a committed relationship out of an empty history and bound the wrong
    actor identity.

    Now a NEW relationship requires BOTH:
      * an actual supplied second-parent history (non-empty, with a real actor ID);
      * at least one forming witness event in that history.
    Either missing produces a typed HOLD, never a committed relation. The
    counterpart is the ACTUAL supplied actor id, never a placeholder.
    """
    known_counterpart = anchor.get("known_counterpart_identity_ref_or_null")
    existing_shared = [
        e for e in anchor.get("history_events", [])
        if e.get("kind") == "SHARED_ENCOUNTER"
    ]

    if known_counterpart and scenario.get("candidate_kind") != "KNOWN_COUNTERPART":
        return typed(
            S.SHARED_HISTORY_CONTRADICTION_HOLD,
            reason="mother history identifies counterpart; conflicting provisional "
                   "candidate refused — reuse exact actor or hold",
            known_counterpart=known_counterpart,
            proposed=scenario.get("candidate_local_id"),
            mother_history_unchanged=True,
            unapproved_rng_draws=0,
        )

    if known_counterpart:
        # Existing identified partner: reuse exact actor identity; no new actor minted.
        objective_relation = {
            "relation_id": h_concat("REL_OBJ", anchor["actor_id"], known_counterpart),
            "participants": [anchor["actor_id"], known_counterpart],
            "relation_kind": "partner_relationship",
            "admission_basis": "already_admitted_mother_history_identity",
            "shared_event_refs": [e["event_id"] for e in existing_shared],
            "single_objective_record": True,
        }
        relation_state = "REUSED_EXISTING_RELATION"
    else:
        # G13: require an ACTUAL second-parent history and a forming witness.
        supplied_history = list(dad_events or [])
        actual_actor = _actual_second_parent_actor(supplied_history)
        witnesses = _witness_events(supplied_history)
        hold_reasons: List[str] = []
        if not supplied_history:
            hold_reasons.append("NO_SECOND_PARENT_HISTORY_SUPPLIED")
        if actual_actor is None:
            hold_reasons.append("SECOND_PARENT_ACTOR_IDENTITY_ABSENT")
        if not witnesses:
            hold_reasons.append("NO_FORMING_WITNESS_EVENT")
        if hold_reasons:
            return typed(
                S.NOT_EXECUTED_AUTHORITY_HOLD,
                relation_version=RELATION_VERSION,
                status=S.NOT_EXECUTED_AUTHORITY_HOLD,
                relationship_committed=False,
                reason="a new laboratory relationship requires an actual "
                       "second-parent history, a bound actor id and a forming witness",
                hold_reasons=hold_reasons,
                n_supplied_history_events=len(supplied_history),
                n_forming_witnesses=len(witnesses),
                actor_id_minted=False,
                placeholder_counterpart_used=False,
                mother_history_unchanged=True,
                unapproved_rng_draws=0,
                is_HOLD_not_CONCEPTION=True,
            )
        counterpart = actual_actor
        objective_relation = {
            "relation_id": h_concat("REL_OBJ", anchor["actor_id"], counterpart),
            "participants": [anchor["actor_id"], counterpart],
            "relation_kind": "encounter_relationship_initialized",
            "admission_basis": "FORMING_WITNESS_IN_SUPPLIED_SECOND_PARENT_HISTORY",
            "shared_event_refs": [e["event_id"] for e in witnesses],
            "second_parent_history_event_count": len(supplied_history),
            "second_parent_actor_id_bound_from_history": counterpart,
            "single_objective_record": True,
        }
        relation_state = "NEW_RELATION_INITIALIZED_FROM_FORMING_WITNESS"
        known_counterpart = counterpart

    # Directional perceived states — independent, asymmetric permitted.
    if force_mom_affectionate_dad_unknown:
        mom_to_dad = {
            "perceiver": anchor["actor_id"],
            "target": known_counterpart,
            "perceived_state": "affectionate_bond_perceived",
            "causal_basis": "encounter_and_continuing_contact_experiences",
        }
        dad_to_mom = {
            "perceiver": known_counterpart,
            "target": anchor["actor_id"],
            "perceived_state": "UNKNOWN_OR_NONRECIPROCAL",
            "causal_basis": "TYPED_UNKNOWN_not_inferred",
        }
    else:
        mom_to_dad = {
            "perceiver": anchor["actor_id"],
            "target": known_counterpart,
            "perceived_state": "positive_regard_perceived",
            "causal_basis": "shared_encounter_and_continuing_contact",
        }
        dad_to_mom = {
            "perceiver": known_counterpart,
            "target": anchor["actor_id"],
            "perceived_state": "positive_regard_perceived",
            "causal_basis": "shared_encounter_and_continuing_contact",
        }

    return {
        "relation_version": RELATION_VERSION,
        "status": S.COMMITTED,
        "relationship_committed": True,
        "relation_state": relation_state,
        "objective_relation": objective_relation,
        "perceived_states": [mom_to_dad, dad_to_mom],
        "reciprocity_inferred": False,
        "household_membership_auto": False,
        "household_membership_requires_separate_admission": True,
        "conception_is_not_relationship": True,
        "second_parent_history_required": True,
        "forming_witness_required": True,
        "identity_reuse_check": {
            "known_counterpart_identity_ref_or_null": anchor.get(
                "known_counterpart_identity_ref_or_null"
            ),
            "duplicate_actor_minted": False,
        },
    }
