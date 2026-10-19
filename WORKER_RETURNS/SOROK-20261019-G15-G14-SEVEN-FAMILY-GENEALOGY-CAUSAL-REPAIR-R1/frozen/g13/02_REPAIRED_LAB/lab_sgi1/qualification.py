"""Layered candidate qualification: hard feasibility, synthetic empirical support,
model-relative plausibility, and final eligibility — kept strictly distinct.

PROVISIONAL_LAB_RULE__NOT_ADOPTED. Verbal rankings are never converted into
fake precise frequencies.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .core import h_obj, typed, S
from .world import WorldSnapshot, generic_possibility_query

QUALIFICATION_VERSION = "QUALIFICATION_LAYERS@1.0-LAB"


def hard_world_court(candidate: Dict[str, Any], anchor: Dict[str, Any],
                     world: WorldSnapshot) -> Dict[str, Any]:
    """Layer 1: hard institution/location/time/route/actor feasibility.

    INFEASIBLE excludes; UNKNOWN_REQUIRED defers; FEASIBLE proceeds.
    Route reachability is checked against the mother checkpoint (no backdating).
    A KNOWN_COUNTERPART contradiction is an exact hard hold, never silent replace.
    """
    known = anchor.get("known_counterpart_identity_ref_or_null")
    if known and candidate.get("candidate_kind") != "KNOWN_COUNTERPART":
        return {
            "status": S.SHARED_HISTORY_CONTRADICTION_HOLD,
            "layer": "HARD_WORLD",
            "reason": "mother history identifies counterpart; incompatible provisional "
                      "candidate is CONTRADICTION_WITH_ADMITTED_MOTHER_HISTORY",
            "known_counterpart": known,
            "proposed_candidate_kind": candidate.get("candidate_kind"),
            "detail": {"disposition": "REUSE_EXACT_ACTOR_OR_HOLD", "replace_forbidden": True},
        }
    route_id = candidate.get("route_kind_id")
    route = next((r for r in world.routes if r.route_id == route_id), None)
    if route is None:
        return typed(S.SCENARIO_INFEASIBLE, reason="route not in world premise",
                     route_id=route_id, layer="HARD_WORLD")
    if route.requires_mobility:
        if anchor.get("mobility_history_present"):
            basis = "PAST_MOBILITY_HISTORY_IN_CHECKPOINT"
        elif anchor.get("prospective_opportunity_refs"):
            basis = "PROSPECTIVE_REACHABLE_OPPORTUNITY_IN_CHECKPOINT"
        else:
            return typed(
                S.SCENARIO_INFEASIBLE,
                reason="mobility route requires past mobility or a lawful reachable "
                       "opportunity in the immutable checkpoint; backdating forbidden",
                route_id=route_id,
                layer="HARD_WORLD",
                mother_mobility_history_present=False,
                prospective_opportunity_present=False,
            )
    else:
        basis = "NON_MOBILITY_ROUTE"
    if route_id not in anchor.get("route_availability", []):
        return typed(
            S.SCENARIO_INFEASIBLE,
            reason="route not among this mother's admitted route availabilities",
            route_id=route_id,
            layer="HARD_WORLD",
            mother_route_availability=anchor.get("route_availability"),
        )
    if not route.lawful_for_mother:
        return typed(S.SCENARIO_INFEASIBLE, reason="route unlawful in world",
                     route_id=route_id, layer="HARD_WORLD")
    return {
        "status": "FEASIBLE",
        "layer": "HARD_WORLD",
        "route_id": route_id,
        "mobility_or_opportunity_basis": basis,
        "note": "hard world court: route lawful and reachable without backdating "
                "mother history",
    }


def empirical_possibility(candidate: Dict[str, Any], world: WorldSnapshot,
                          direction: str = "TARGET_GIVEN_CONDITIONERS") -> Dict[str, Any]:
    """Layer 2: generic synthetic possibility. Source-free; use ceiling always labeled.

    Single-person marginals never become a dyad law. Joint requests return
    NOT_ESTIMABLE, never zero plausibility.
    """
    ec = candidate.get("endpoint_constraints") or {}
    if not isinstance(ec, dict):
        ec = {}
    requires_joint = any(
        "two_person" in str(x).lower() or "joint" in str(x).lower() or "dyad" in str(x).lower()
        for x in ec.get("second_parent_structure_and_position_constraints", [])
    ) or candidate.get("requires_joint_propensity", False)
    request = {
        "operation_id": "GENERIC_POSITIONED_POSSIBILITY@1.0-LAB",
        "exact_world_snapshot_ref": world.ref(),
        "subject_universe_and_observation_unit": "SYNTHETIC_LAB_INDIVIDUAL",
        "target_variable": candidate.get("route_kind_id", "encounter"),
        "condition_bindings": ec.get("admissible_world_context_refs", []),
        "direction": direction,
        "joint_topology": (
            "MULTI_UNIT_WITH_QUALIFIED_BRIDGE" if requires_joint else "SAME_PERSON"
        ),
        "requires_joint": requires_joint,
        "comparison_mode": "WITHIN_SYNTHETIC_UNIVERSE",
    }
    return generic_possibility_query(world, request)


def model_plausibility_label(candidate: Dict[str, Any]) -> Dict[str, Any]:
    """Layer 3: model-relative plausibility. Ordinal only. NEVER a frequency, NEVER
    converted into selection weights without an adopted policy owner."""
    rank = candidate.get("plausibility_rank_ordinal")
    return {
        "layer": "MODEL_RELATIVE_PLAUSIBILITY",
        "plausibility_rank_ordinal": rank,
        "model_reference": candidate.get("model_reference", "see proposal record"),
        "is_frequency": False,
        "is_selection_weight": False,
        "conversion_performed": False,
        "note": "ordinal ranking retained as-is; no normalization to probabilities",
    }


def classify_eligibility(candidate: Dict[str, Any], hard: Dict[str, Any],
                         empirical: Dict[str, Any]) -> Dict[str, Any]:
    """Eligibility/support classification. Hard feasibility gates; empirical lack of
    support cannot mechanically mean population impossibility; unknowns defer."""
    if hard.get("status") != "FEASIBLE":
        return {
            "eligible": False,
            "reason": hard.get("status"),
            "reason_detail": hard.get("detail", {}),
            "eligibility_class": "EXCLUDED_HARD_INFEASIBLE",
        }
    emp_state = empirical.get("result_state")
    if emp_state in ("NOT_ESTIMABLE", "UNKNOWN", "NONCOMPARABLE"):
        return {
            "eligible": True,
            "empirical_support": emp_state,
            "eligibility_class": "ELIGIBLE_SYNTHETIC_SUPPORT_CEILING",
            "note": "hard-feasible; empirical support ceiling-limited or unknown — "
                    "not recoded as impossible",
        }
    return {
        "eligible": True,
        "empirical_support": emp_state,
        "eligibility_class": "ELIGIBLE_SYNTHETIC_SUPPORTED",
    }


def qualify(candidate: Dict[str, Any], anchor: Dict[str, Any],
            world: WorldSnapshot) -> Dict[str, Any]:
    hard = hard_world_court(candidate, anchor, world)
    emp = empirical_possibility(candidate, world)
    model = model_plausibility_label(candidate)
    elig = classify_eligibility(candidate, hard, emp)
    return {
        "candidate_local_id": candidate.get("candidate_local_id"),
        "class_key": candidate.get("class_key"),
        "qualification_version": QUALIFICATION_VERSION,
        "hard_feasibility": hard,
        "empirical_or_synthetic_support": emp,
        "model_relative_plausibility": model,
        "eligibility": elig,
    }
