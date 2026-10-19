"""Objective Mom<->Dad relation reconciliation and asymmetric perceived states.

PROVISIONAL_LAB_RULE__NOT_ADOPTED.
One objective relation event; Mom->Dad and Dad->Mom perceived states generated
separately. No reciprocity inference, no auto household membership, conception
never equals relationship.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from .core import h_obj, h_concat, typed, S

RELATION_VERSION = "RELATION_RECONCILIATION@1.0-LAB"


def reconcile(anchor: Dict[str, Any], dad_events: List[Dict[str, Any]],
              scenario: Dict[str, Any],
              force_mom_affectionate_dad_unknown: bool = False) -> Dict[str, Any]:
    """Reconcile identity + shared history; admit exactly one objective relation event;
    initialize directional perceived states independently."""
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
        counterpart = "LAB_SECOND_PARENT_SELECTED"
        objective_relation = {
            "relation_id": h_concat("REL_OBJ", anchor["actor_id"], counterpart),
            "participants": [anchor["actor_id"], counterpart],
            "relation_kind": "encounter_relationship_initialized",
            "admission_basis": "ENCOUNTER_WITNESS_MIN_1",
            "shared_event_refs": [h_concat("SHARED_ENCOUNTER", anchor["actor_id"], counterpart)],
            "single_objective_record": True,
        }
        relation_state = "NEW_RELATION_INITIALIZED_FROM_ENCOUNTER"
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
        "relation_state": relation_state,
        "objective_relation": objective_relation,
        "perceived_states": [mom_to_dad, dad_to_mom],
        "reciprocity_inferred": False,
        "household_membership_auto": False,
        "household_membership_requires_separate_admission": True,
        "conception_is_not_relationship": True,
        "identity_reuse_check": {
            "known_counterpart_identity_ref_or_null": anchor.get(
                "known_counterpart_identity_ref_or_null"
            ),
            "duplicate_actor_minted": False,
        },
    }
