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

CONTINUATION_VERSION = "FORWARD_CONTINUATION@1.0-LAB"


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


def forward_continuation(anchor: Dict[str, Any],
                         dad_events: List[Dict[str, Any]],
                         relation: Dict[str, Any]) -> Dict[str, Any]:
    """Both parents continue independently after the boundary marker.
    Parent project change / relationship care / absence register only through
    typed continuation events — never fixed family labels."""
    mom_id = anchor["actor_id"]
    dad_id = (relation.get("objective_relation", {}).get("participants", ["", ""])[1])
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
        {
            "event_id": h_concat("CONT", dad_id, "project_change"),
            "kind": "PARENT_CONTINUATION",
            "actor": dad_id,
            "payload": {
                "project_change": "repair_bench_saving_and_cooperative_rotation_continues",
                "care_or_absence": "periodic_presence_via_shared_route",
                "causal_basis": "pre_boundary project and striving events",
            },
            "effective_index": 1001,
        },
        {
            "event_id": h_concat("CONT", "rel", "state"),
            "kind": "RELATION_CONTINUATION",
            "actor": "PAIR",
            "payload": {
                "objective_relation_continues": True,
                "household_membership": "NOT_AUTOMATICALLY_ESTABLISHED",
                "note": "relationship continuation distinct from household admission",
            },
            "effective_index": 1002,
        },
    ]
    return {
        "continuation_version": CONTINUATION_VERSION,
        "continuation_events": continuation_events,
        "both_parents_continue_independently": True,
        "parent_project_change_registered_as_event": True,
        "care_or_absence_registered_as_event": True,
        "no_fixed_family_labels": True,
    }


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
