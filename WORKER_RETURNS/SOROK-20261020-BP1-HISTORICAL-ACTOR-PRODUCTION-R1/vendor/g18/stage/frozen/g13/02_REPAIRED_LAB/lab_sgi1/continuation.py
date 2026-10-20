"""Forward continuation of both parents and the child developmental-environment fixture.

PROVISIONAL_LAB_RULE__NOT_ADOPTED.
Explicit LAB_CONCEPTION_BOUNDARY is used; no adopted conception/gestation/birth
semantics are claimed. ZERO CHILD_GENERATED events are minted (biological/timing
owner not authorized). The child artifact is a LAB developmental-environment
fixture, not an admitted child actor and not a PRE-V3 parent object.
"""
from __future__ import annotations

from typing import Any, Dict, List

from .core import h_obj, h_concat, typed, S

CONTINUATION_VERSION = "FORWARD_CONTINUATION@2.0-G13-REPAIRED"


def lab_conception_boundary() -> Dict[str, Any]:
    return {
        "marker_id": "LAB_CONCEPTION_BOUNDARY",
        "marker_semantics": S.LAB_CONCEPTION_BOUNDARY,
        "target_status": "PENDING_NOT_ADMITTED_CONCEPTION",
        "child_generated_events": 0,
        "birth_alias": False,
        "gestation_birth_semantics": "HOLD_NO_ADOPTED_BIOLOGICAL_AUTHORITY",
        "missing_authority": ["CONCEPTION_BIOLOGY_AUTHORITY_HOLD"],
    }


def _history_actor(dad_events: List[Dict[str, Any]]) -> Optional[str]:
    for e in dad_events or []:
        actors = e.get("actors") or []
        if actors:
            return actors[0]
    return None


def forward_continuation(anchor: Dict[str, Any],
                         dad_events: List[Dict[str, Any]],
                         relation: Dict[str, Any]) -> Dict[str, Any]:
    """Both parents continue independently after the boundary marker.

    G13 REPAIR (defect family 7 -- paternal continuation).

    The pre-repair helper ignored ``dad_events`` and unconditionally emitted a
    PARENT_CONTINUATION event for whatever second participant the relation
    dictionary named. An EMPTY paternal history therefore still produced a
    paternal project-continuation event for an unformed actor.

    A paternal continuation event is now emitted only when the supplied history
    actually contains that actor. Otherwise a typed HOLD is returned and NO
    paternal continuation event is minted. The maternal continuation is
    unaffected: it is grounded in the mother anchor, not in the second-parent
    history.
    """
    from .relation import FORMING_WITNESS_KINDS, _actual_second_parent_actor

    mom_id = anchor["actor_id"]
    participants = (relation.get("objective_relation", {}) or {}).get("participants") or ["", ""]
    claimed_dad_id = participants[1] if len(participants) > 1 else ""
    supplied = list(dad_events or [])
    history_actor = _actual_second_parent_actor(supplied)
    witnesses = [e for e in supplied if e.get("kind") in FORMING_WITNESS_KINDS]

    # Paternal continuation requires REAL supplied history for that actor.
    dad_id = history_actor
    paternal_admitted = bool(
        supplied and dad_id is not None and claimed_dad_id == dad_id and witnesses
    )

    continuation_events = [
        {
            "event_id": h_concat("CONT", mom_id, "project_change"),
            "kind": "PARENT_CONTINUATION",
            "actor": mom_id,
            "payload": {
                "project_change": "evening_certificate_completion_window",
                "care_or_absence": "continuing_care_routine_for_household",
                "causal_basis": "pre_boundary striving and enrollment events",
            },
            "effective_index": 1000,
        },
    ]

    hold_reasons: List[str] = []
    if paternal_admitted:
        continuation_events.append({
            "event_id": h_concat("CONT", dad_id, "project_change"),
            "kind": "PARENT_CONTINUATION",
            "actor": dad_id,
            "payload": {
                "project_change": "repair_bench_saving_and_cooperative_rotation_continues",
                "care_or_absence": "periodic_presence_via_shared_route",
                "causal_basis": "pre_boundary project and striving events",
                "second_parent_history_event_count": len(supplied),
            },
            "effective_index": 1001,
        })
    else:
        if not supplied:
            hold_reasons.append("NO_SECOND_PARENT_HISTORY_SUPPLIED")
        elif dad_id is None:
            hold_reasons.append("SECOND_PARENT_ACTOR_IDENTITY_ABSENT")
        elif claimed_dad_id != dad_id:
            hold_reasons.append("RELATION_PARTICIPANT_NOT_BOUND_TO_SUPPLIED_HISTORY")
        if not witnesses:
            hold_reasons.append("NO_FORMING_WITNESS_EVENT")
        if not hold_reasons:
            hold_reasons.append("PATERNAL_CONTINUATION_NOT_ADMITTED")

    relation_continued = paternal_admitted
    continuation_events.append({
        "event_id": h_concat("CONT", "rel", "state"),
        "kind": "RELATION_CONTINUATION",
        "actor": "PAIR",
        "payload": {
            "objective_relation_continues": relation_continued,
            "household_membership": "NOT_AUTOMATICALLY_ESTABLISHED",
            "note": "relationship continuation distinct from household admission",
            "paternal_continuation_admitted": paternal_admitted,
        },
        "effective_index": 1002,
    })

    out = {
        "continuation_version": CONTINUATION_VERSION,
        "continuation_events": continuation_events,
        "both_parents_continue_independently": bool(paternal_admitted),
        "maternal_continuation_admitted": True,
        "paternal_continuation_admitted": paternal_admitted,
        "paternal_continuation_requires_supplied_history": True,
        "parent_project_change_registered_as_event": True,
        "care_or_absence_registered_as_event": True,
        "no_fixed_family_labels": True,
        "unformed_actor_continuation_minted": False,
    }
    if hold_reasons:
        out["typed_hold"] = {
            "hold_state": S.NOT_EXECUTED_AUTHORITY_HOLD,
            "hold_reasons": hold_reasons,
            "paternal_events_emitted": 0,
            "claimed_unformed_participant": (claimed_dad_id
                                              if not paternal_admitted else None),
            "is_HOLD_not_world_truth": True,
        }
    return out


def child_developmental_environment_fixture(anchor: Dict[str, Any],
                                            dad_events: List[Dict[str, Any]],
                                            continuation: Dict[str, Any],
                                            boundary: Dict[str, Any]) -> Dict[str, Any]:
    """Child developmental-environment fixture: exposure/effects entries derived only
    from lawfully continued parent material context AFTER the lab boundary admission.
    Never parent-profile averaging; never a child personality assignment."""
    mom_id = anchor["actor_id"]
    exposures = [
        {
            "exposure_id": "EXP_MATERNAL_ROUTINE_STABILITY",
            "material_context": "evening_study_routine_and_workshop_wage_continuity",
            "causal_parent_events": [
                e["event_id"] for e in continuation["continuation_events"]
                if e["actor"] == mom_id
            ],
            "effective_after_admission": True,
        },
        {
            "exposure_id": "EXP_PATERNAL_PROJECT_PRESENCE_PERIODIC",
            "material_context": "periodic_repair_bench_presence_and_cooperative_rotation_schedule",
            "causal_parent_events": [
                e["event_id"] for e in continuation["continuation_events"]
                if e["actor"] != mom_id and e["kind"] == "PARENT_CONTINUATION"
            ],
            "effective_after_admission": True,
        },
        {
            "exposure_id": "EXP_HOUSEHOLD_RESOURCE_LEVEL",
            "material_context": "combined_wage_artisan_income_band",
            "causal_parent_events": [
                e["event_id"] for e in continuation["continuation_events"]
            ],
            "effective_after_admission": True,
        },
    ]
    return {
        "fixture_kind": "LAB_CHILD_DEVELOPMENTAL_ENVIRONMENT_FIXTURE",
        "fixture_id": "LAB_CHILD_ENV_001",
        "is_admitted_child_actor": False,
        "is_PREV3_parent_object": False,
        "child_generated_events": boundary["child_generated_events"],
        "lab_conception_boundary": boundary["marker_id"],
        "birth_alias": boundary["birth_alias"],
        "exposures": exposures,
        "exposure_changes_only_after_admission": True,
        "personality_assigned_from_parent_profile": False,
        "developmental_effects_mechanism": "lawfully_encountered_exposed_processed_material_context",
        "lab_rule": "PROVISIONAL_LAB_RULE__NOT_ADOPTED",
    }
