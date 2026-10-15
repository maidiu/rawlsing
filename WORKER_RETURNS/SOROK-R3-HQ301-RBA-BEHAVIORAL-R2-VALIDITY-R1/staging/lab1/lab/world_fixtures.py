"""Synthetic world / actor-history / event fixtures for K1-K6 (invented lab world).

EVERY event binds world receipt, position, relationship, opportunity, exposure
and admitted ancestry.  A missing binding makes the occurrence UNDERSPECIFIED.
Nothing here is evidence about real workers or real historical institutions.
"""
from __future__ import annotations

from typing import Any

from lab.hashutil import semantic_hash

FIXTURE_GRADE = "SYNTHETIC_LAB_TEST_ONLY_NOT_ADMITTED_V3_REALITY"

WORLD_1998 = {
    "world_id": "W_PORT_TOWN_1998_TEST",
    "world_version": "W1",
    "fixture_hash": "W_SYNTH_001",
    "historical_epoch": "synthetic late-1990s municipal apprenticeship system",
    "legal_rules": [
        "public_apprenticeship_records_exist",
        "supervisor_can_certify_training_only_on_signed_check",
        "worker_can_refuse_extra_shift_without_automatic_disqualification",
    ],
    "institutional_enforcement": "local registrar honors signed apprenticeship reports only",
    "material_conditions": {
        "labor_market": "scarce training places",
        "housing": "shared rented rooms",
        "transport": "night bus",
        "safety": "current workshop is safe in fixture",
    },
    "inequality_and_position_constraints": [
        "supervisor_controls_shift_assignments",
        "registrar_controls_certification",
        "shop_peers_do_not_control_register",
    ],
    "clock": "1998-10-03T16:00:00Z",
    "source_authority": "LAB_WORLD_FIXTURE_NOT_PREV3_N9",
    "uncertainty": "THIS_IS_AN_INVENTED_WORLDFIXTURE_NOT_HISTORICAL_FACT",
}

WORLD_1999 = {
    "world_id": "W_PORT_TOWN_1999_POSITION_VARIANT",
    "world_version": "W2",
    "fixture_hash": "W_SYNTH_002",
    "historical_epoch": "synthetic 1999 municipal workshop staffing variant",
    "legal_rules": [
        "public_apprenticeship_records_exist",
        "foreperson_may_assign_small_schedule_changes_within_validated_power",
        "category_membership_alone_grants_no_authority",
    ],
    "institutional_enforcement": "local registrar honors signed apprenticeship reports only",
    "material_conditions": {
        "labor_market": "scarce training places",
        "housing": "shared rented rooms",
        "transport": "night bus",
        "safety": "current workshop is safe in fixture",
    },
    "inequality_and_position_constraints": [
        "foreperson_schedule_power_requires_validated_instrument",
        "registrar_controls_certification",
    ],
    "clock": "1999-06-10T10:00:00Z",
    "source_authority": "LAB_WORLD_FIXTURE_NOT_PREV3_N9",
    "uncertainty": "THIS_IS_AN_INVENTED_WORLDFIXTURE_NOT_HISTORICAL_FACT",
}

POSITION_1998_APPRENTICE = {
    "position_receipt": "POS_SYNTH_01",
    "actor_ref": "A_TEST",
    "positions": ["junior_apprentice", "income_dependent_worker"],
    "material_resources": ["bus_ticket", "paid_shift"],
    "sanction_capacity": "cannot fire supervisor; can decline optional shift",
    "mobility_exit": "limited but available",
}

POSITION_1999_FOREPERSON = {
    "position_receipt": "POS_SYNTH_02F",
    "actor_ref": "A_TEST",
    "positions": ["foreperson_at_later_date"],
    "material_resources": ["bus_ticket", "paid_shift", "small_schedule_instrument"],
    "sanction_capacity": "VALID_SMALL_SCHEDULE_POWER",
    "mobility_exit": "limited but available",
}

POSITION_1999_APPRENTICE = {
    "position_receipt": "POS_SYNTH_02A",
    "actor_ref": "A_TEST",
    "positions": ["apprentice"],
    "material_resources": ["bus_ticket", "paid_shift"],
    "sanction_capacity": "NONE",
    "mobility_exit": "limited but available",
}

POSITION_1999_CATEGORY_ONLY = {
    "position_receipt": "POS_SYNTH_02C",
    "actor_ref": "A_TEST",
    "positions": ["category_nominal_member"],
    "material_resources": ["bus_ticket"],
    "sanction_capacity": "NONE",
    "mobility_exit": "limited but available",
}

RELATIONSHIP = {
    "rel_ref": "REL_SUP_APP",
    "participants": ["A_TEST", "SUPERVISOR_C"],
    "history_anchor": "RELH_SYNTH_01",
    "public_role": "supervisor_apprentice",
    "actor_perception": "requires specific admitted actor history; not inferred from title",
    "reciprocity": "NOT_ASSUMED",
}

RELATIONSHIP_PEER = {
    "rel_ref": "REL_PEER_APP",
    "participants": ["A_TEST", "PEER"],
    "history_anchor": "RELH_SYNTH_02",
    "public_role": "peer_apprentice",
    "actor_perception": "requires specific admitted actor history; not inferred from title",
    "reciprocity": "NOT_ASSUMED",
}

RELATIONSHIP_REGISTRAR = {
    "rel_ref": "REL_REG_APP",
    "participants": ["A_TEST", "REGISTRAR"],
    "history_anchor": "RELH_SYNTH_03",
    "public_role": "registrar_apprentice",
    "actor_perception": "requires specific admitted actor history; not inferred from title",
    "reciprocity": "NOT_ASSUMED",
}


def _event(
    event_id: str,
    kind: str,
    *,
    world: dict[str, Any],
    position: dict[str, Any],
    relationship: dict[str, Any],
    opportunity: dict[str, Any],
    history_refs: list[str],
    receivable: dict[str, Any],
    time: str | None = None,
    admission: str = "ADMITTED",
    witness: dict[str, Any] | None = None,
    formation_parents: list[str] | None = None,
) -> dict[str, Any]:
    ev = {
        "event_id": event_id,
        "kind": kind,
        "world_receipt_ref": {
            "world_id": world["world_id"],
            "fixture_hash": world["fixture_hash"],
        },
        "position_receipt_ref": position["position_receipt"],
        "relationship_ref": relationship["rel_ref"],
        "opportunity_ref": opportunity["opportunity_ref"],
        "exposure_ref": opportunity["exposure_ref"],
        "history_refs": list(history_refs),
        "effective_time": time or world["clock"],
        "admission": admission,
        "actor_receivable_features": dict(receivable),
    }
    if witness is not None:
        ev["witness"] = dict(witness)
    if formation_parents:
        ev["formation_parents"] = list(formation_parents)
    return ev


OPPORTUNITY_FEEDBACK = {
    "opportunity_ref": "OPP_FEEDBACK_WINDOW",
    "exposure_ref": "EXP_SHIFT_HANDOVER",
    "no_op_route": "SILENCE",
    "available_routes": [
        {"route_id": "REQUEST_FEEDBACK", "cost": "LOW_TIME", "requires": "ASK_CLARIFICATION_PRACTICE_OR_HELP_EXPECTATION"},
        {"route_id": "SILENCE", "cost": "NONE", "requires": "NONE"},
        {"route_id": "APPEAL", "cost": "HIGH_TIME", "requires": "NONE"},
    ],
}

OPPORTUNITY_SHIFT = {
    "opportunity_ref": "OPP_SHIFT_ASSIGNMENT",
    "exposure_ref": "EXP_WORK_ASSIGNMENT_ENCOUNTER",
    "no_op_route": "NEUTRAL_RESPONSE",
    "available_routes": [
        {"route_id": "HEIGHTENED_GUARD", "cost": "LOW_TIME", "requires": "NONE"},
        {"route_id": "NEUTRAL_RESPONSE", "cost": "NONE", "requires": "NONE"},
    ],
}

OPPORTUNITY_REQUEST = {
    "opportunity_ref": "OPP_EXTRA_SHIFT_REQUEST",
    "exposure_ref": "EXP_SUPERVISOR_REQUEST",
    "no_op_route": "WITHDRAW_REQUEST",
    "available_routes": [
        {"route_id": "REQUEST_WITH_REPAIR", "cost": "LOW_TIME", "requires": "NONE"},
        {"route_id": "REQUEST_WITH_CONDITIONAL_CAUTION", "cost": "LOW_TIME", "requires": "NONE"},
        {"route_id": "WITHDRAW_REQUEST", "cost": "NONE", "requires": "NONE"},
    ],
}

OPPORTUNITY_CONSULT = {
    "opportunity_ref": "OPP_AFTERMATH_CONSULT",
    "exposure_ref": "EXP_CONSULT_WINDOW",
    "no_op_route": "NO_ACTION",
    "available_routes": [
        {"route_id": "NARROWED_CONSULT", "cost": "LOW_TIME", "requires": "NONE"},
        {"route_id": "REPEATED_QUESTION", "cost": "MEDIUM_TIME", "requires": "NONE"},
        {"route_id": "NO_ACTION", "cost": "NONE", "requires": "NONE"},
    ],
}

OPPORTUNITY_CERT = {
    "opportunity_ref": "OPP_CERTIFICATION_WINDOW",
    "exposure_ref": "EXP_REGISTRY_COUNTER",
    "no_op_route": "REMAIN_DOUBTFUL",
    "available_routes": [
        {"route_id": "ACCEPT_CERTIFICATE", "cost": "LOW_TIME", "requires": "NONE"},
        {"route_id": "REMAIN_DOUBTFUL", "cost": "NONE", "requires": "NONE"},
    ],
}

OPPORTUNITY_SANCTION = {
    "opportunity_ref": "OPP_LATER_SANCTION",
    "exposure_ref": "EXP_WORK_ASSIGNMENT_ENCOUNTER",
    "no_op_route": "NO_SANCTION",
    "available_routes": [
        {"route_id": "POLICING_CANDIDATE", "cost": "MEDIUM_TIME", "requires": "VALID_SANCTION_CAPACITY_AND_ROUTE"},
        {"route_id": "NO_SANCTION", "cost": "NONE", "requires": "NONE"},
    ],
}


# ---------------------------------------------------------------------------
# admitted prior events + their authorized destination-owner effects
# ---------------------------------------------------------------------------

def _effect(effect_id, owner, effect_kind, target_key, payload, parents):
    return {
        "effect_id": effect_id,
        "owner": owner,
        "effect_kind": effect_kind,
        "target_key": target_key,
        "payload": payload,
        "parent_event_refs": list(parents),
    }


K1_RESPONSIVE_EVENTS = [
    _event(
        "EV7_FEEDBACK_RESPECTED",
        "FEEDBACK_ENCOUNTER",
        world=WORLD_1998,
        position=POSITION_1998_APPRENTICE,
        relationship=RELATIONSHIP,
        opportunity=OPPORTUNITY_FEEDBACK,
        history_refs=[],
        receivable={"feedback": "RESPECTFUL_INQUIRY", "supervisor_stance": "LISTENING"},
    ),
    _event(
        "EV13_FEEDBACK_COLLABORATIVE",
        "FEEDBACK_ENCOUNTER",
        world=WORLD_1998,
        position=POSITION_1998_APPRENTICE,
        relationship=RELATIONSHIP,
        opportunity=OPPORTUNITY_FEEDBACK,
        history_refs=["EV7_FEEDBACK_RESPECTED"],
        receivable={"feedback": "COLLABORATIVE_CHECK", "supervisor_stance": "JOINT_REVIEW"},
    ),
]

K1_RESPONSIVE_EFFECTS = [
    _effect(
        "EFF_K1_R_1", "CAN010", "EXPECTATION_FORMED", "SCOPE_HELP_POSSIBLE",
        {"scope": "FEEDBACK", "expectation": "HELP_IS_POSSIBLE", "standing": "HELD"},
        ["EV7_FEEDBACK_RESPECTED"],
    ),
    _effect(
        "EFF_K1_R_2", "CAN011", "PRACTICE_EARNED", "ASK_CLARIFICATION",
        {"practice": "ASK_CLARIFICATION", "scope": "FEEDBACK", "earned": True},
        ["EV7_FEEDBACK_RESPECTED"],
    ),
    _effect(
        "EFF_K1_R_3", "CAN010", "STRIVING_FORMED", "VERIFY_TOGETHER",
        {"axis": "VERIFICATION", "scope": "FEEDBACK", "object": "CHECK_TOGETHER"},
        ["EV13_FEEDBACK_COLLABORATIVE"],
    ),
    _effect(
        "EFF_K1_R_4", "CAN011", "PRACTICE_REINFORCED", "ASK_CLARIFICATION",
        {"practice": "ASK_CLARIFICATION", "scope": "FEEDBACK", "earned": True},
        ["EV13_FEEDBACK_COLLABORATIVE"],
    ),
]

K1_PUNITIVE_EVENTS = [
    _event(
        "EV7_QUESTION_PUNISHED",
        "FEEDBACK_ENCOUNTER",
        world=WORLD_1998,
        position=POSITION_1998_APPRENTICE,
        relationship=RELATIONSHIP,
        opportunity=OPPORTUNITY_FEEDBACK,
        history_refs=[],
        receivable={"feedback": "QUESTION_PUNISHED", "supervisor_stance": "SANCTIONING"},
    ),
    _event(
        "EV13_REQUEST_SANCTIONED",
        "FEEDBACK_ENCOUNTER",
        world=WORLD_1998,
        position=POSITION_1998_APPRENTICE,
        relationship=RELATIONSHIP,
        opportunity=OPPORTUNITY_FEEDBACK,
        history_refs=["EV7_QUESTION_PUNISHED"],
        receivable={"feedback": "REQUEST_SANCTIONED", "supervisor_stance": "SANCTIONING"},
    ),
]

K1_PUNITIVE_EFFECTS = [
    _effect(
        "EFF_K1_P_1", "CAN010", "EXPECTATION_FORMED", "SCOPE_SPEAKING_COSTLY",
        {"scope": "FEEDBACK", "expectation": "SPEAKING_IS_COSTLY", "standing": "HELD"},
        ["EV7_QUESTION_PUNISHED"],
    ),
    _effect(
        "EFF_K1_P_2", "CAN011", "TENSION_FORMED", "APPROACH_WITHDRAW",
        {"poles": ["APPROACH", "WITHDRAW"], "scope": "FEEDBACK", "status": "UNRESOLVED"},
        ["EV7_QUESTION_PUNISHED"],
    ),
    _effect(
        "EFF_K1_P_3", "ADP016", "TRACE_FORMED", "TRACE_PUBLIC_SHAMING",
        {"trace_kind": "NONDECLARATIVE_TRACE", "access_state": "RETAINED_NOT_ACCESSIBLE",
         "activation": "RECRUITABLE", "source_kind": "QUESTION_PUNISHMENT"},
        ["EV7_QUESTION_PUNISHED"],
    ),
    _effect(
        "EFF_K1_P_4", "CAN010", "EXPECTATION_REINFORCED", "SCOPE_SPEAKING_COSTLY",
        {"scope": "FEEDBACK", "expectation": "SPEAKING_IS_COSTLY", "standing": "HELD"},
        ["EV13_REQUEST_SANCTIONED"],
    ),
]

K1_PRESENT = _event(
    "EV21_FEEDBACK_REQUEST_ENCOUNTER",
    "FEEDBACK_ENCOUNTER",
    world=WORLD_1998,
    position=POSITION_1998_APPRENTICE,
    relationship=RELATIONSHIP,
    opportunity=OPPORTUNITY_FEEDBACK,
    history_refs=["EV7_FEEDBACK_RESPECTED", "EV13_FEEDBACK_COLLABORATIVE"],
    receivable={"feedback": "OPEN_INVITATION_FOR_INPUT", "supervisor_stance": "NEUTRAL"},
)


def _k2_events(formation_event: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        _event(
            "EV1_APPROVAL",
            "WITNESS_ACT",
            world=WORLD_1998,
            position=POSITION_1998_APPRENTICE,
            relationship=RELATIONSHIP,
            opportunity=OPPORTUNITY_REQUEST,
            history_refs=[],
            receivable={"act": "APPROVAL", "content": "WORK_QUALITY_ACKNOWLEDGED"},
        ),
        _event(
            "EV2_CRITICISM",
            "WITNESS_ACT",
            world=WORLD_1998,
            position=POSITION_1998_APPRENTICE,
            relationship=RELATIONSHIP,
            opportunity=OPPORTUNITY_REQUEST,
            history_refs=["EV1_APPROVAL"],
            receivable={"act": "CRITICISM", "content": "PROCEDURE_CORRECTION"},
        ),
        formation_event,
    ]


K2_EFFECTS = [
    _effect(
        "EFF_K2_1", "CAN010", "EXPECTATION_FORMED", "SCOPE_APPROVAL_CONDITIONAL",
        {"scope": "REQUEST", "expectation": "APPROVAL_MAY_BE_CONDITIONAL", "standing": "CONTESTED"},
        ["EV1_APPROVAL"],
    ),
    _effect(
        "EFF_K2_2", "CAN011", "TENSION_FORMED", "APPROVAL_CRITICISM_TENSION",
        {"poles": ["APPROVAL", "CRITICISM"], "scope": "REQUEST", "status": "UNRESOLVED"},
        ["EV2_CRITICISM"],
    ),
]

K2_PRESENT = _event(
    "EV3_REQUEST",
    "REQUEST_ENCOUNTER",
    world=WORLD_1998,
    position=POSITION_1998_APPRENTICE,
    relationship=RELATIONSHIP,
    opportunity=OPPORTUNITY_REQUEST,
    history_refs=["EV1_APPROVAL", "EV2_CRITICISM"],
    receivable={"act": "SHIFT_REQUEST", "content": "REQUEST_EXTRA_SHIFT"},
)

K2_FORMATION_A = _event(
    "EV_RELFORM_A",
    "RELATION_EFFECT",
    world=WORLD_1998,
    position=POSITION_1998_APPRENTICE,
    relationship=RELATIONSHIP,
    opportunity=OPPORTUNITY_REQUEST,
    history_refs=["EV1_APPROVAL", "EV2_CRITICISM"],
    receivable={"act": "RELATION_EFFECT", "content": "COMPENSATION_READING_FORMED"},
    formation_parents=["EV1_APPROVAL", "EV2_CRITICISM"],
)

K2_FORMATION_B = _event(
    "EV_RELFORM_B",
    "RELATION_EFFECT",
    world=WORLD_1998,
    position=POSITION_1998_APPRENTICE,
    relationship=RELATIONSHIP,
    opportunity=OPPORTUNITY_REQUEST,
    history_refs=["EV1_APPROVAL", "EV2_CRITICISM"],
    receivable={"act": "RELATION_EFFECT", "content": "CONDITIONAL_RECOGNITION_READING_FORMED"},
    formation_parents=["EV1_APPROVAL", "EV2_CRITICISM"],
)


def _k3_events(prior_id: str, prior_receivable: dict[str, Any], prior_kind: str) -> list[dict[str, Any]]:
    return [
        _event(
            prior_id,
            prior_kind,
            world=WORLD_1998,
            position=POSITION_1998_APPRENTICE,
            relationship=RELATIONSHIP,
            opportunity=OPPORTUNITY_SHIFT,
            history_refs=[],
            receivable=prior_receivable,
        )
    ]


K3_PRESENT = _event(
    "EV22_LATER_SHIFT_REQUEST",
    "SHIFT_ENCOUNTER",
    world=WORLD_1998,
    position=POSITION_1998_APPRENTICE,
    relationship=RELATIONSHIP,
    opportunity=OPPORTUNITY_SHIFT,
    history_refs=["EV7_PUBLIC_SHAMING"],
    receivable={"act": "SHIFT_ASSIGNMENT", "content": "REASSIGNMENT_PROPOSAL"},
)


def k3_memory_variants() -> dict[str, dict[str, Any]]:
    return {
        "TRACE_ACTIVE": {
            "ADP016": "EPISODIC_CONTENT_UNAVAILABLE",
            "causal_trace": "PERSISTENT_TRACE_ACTIVATED_IF_OWNER_RULE",
            "ADP017": "NO_FIRST_PERSON_ORIGIN_CLAIM",
        },
        "TRACE_ABSENT": {
            "ADP016": "EPISODIC_CONTENT_UNAVAILABLE",
            "causal_trace": "NONE",
            "ADP017": "NO_FIRST_PERSON_ORIGIN_CLAIM",
        },
        "RETAINED_INACCESSIBLE": {
            "ADP016": "RETAINED_NOT_ACCESSIBLE",
            "causal_trace": "PERSISTENT_TRACE_IF_ADMITTED",
            "ADP017": "NO_ORIGIN_CLAIM",
        },
    }


K3_SHAMING_EFFECTS = [
    _effect(
        "EFF_K3_1", "ADP016", "TRACE_FORMED", "TRACE_PUBLIC_SHAMING",
        {"trace_kind": "NONDECLARATIVE_TRACE", "access_state": "RETAINED_NOT_ACCESSIBLE",
         "activation": "RECRUITABLE", "source_kind": "PUBLIC_SHAMING"},
        ["EV7_PUBLIC_SHAMING"],
    ),
    _effect(
        "EFF_K3_2", "ADP016", "EPISODIC_ACCESS_SET", "EPISODIC_EV7_PUBLIC_SHAMING",
        {"access_state": "UNAVAILABLE", "note": "EPISODIC_CONTENT_UNAVAILABLE"},
        ["EV7_PUBLIC_SHAMING"],
    ),
    _effect(
        "EFF_K3_3", "ADP017", "CLAIM_PERMISSION_SET", "ORIGIN_CLAIM_EARLY_EVENT",
        {"permission": "DENIED", "claim": "FIRST_PERSON_ORIGIN"},
        ["EV7_PUBLIC_SHAMING"],
    ),
]

K3_NEUTRAL_EFFECTS = [
    _effect(
        "EFF_K3_N_1", "ADP016", "EPISODIC_ACCESS_SET", "EPISODIC_EV7_NEUTRAL",
        {"access_state": "RECALLABLE", "note": "NEUTRAL_COUNTERFACT"},
        ["EV7_NEUTRAL_COUNTERFACT"],
    ),
]

K4_PRESENT = _event(
    "EV23_AFTERMATH_CONSULT",
    "CONSULT_ENCOUNTER",
    world=WORLD_1998,
    position=POSITION_1998_APPRENTICE,
    relationship=RELATIONSHIP,
    opportunity=OPPORTUNITY_CONSULT,
    history_refs=["EV7_QUESTION_PUNISHED"],
    receivable={"act": "CONSULT_INVITATION", "content": "PROCEDURE_CONSULT"},
)

K4_LATER_EVENTS = {
    "CORRECTIVE_CONTEXT": _event(
        "EV17_QUESTION_RESPECTED_BY_PEER",
        "WITNESS_ACT",
        world=WORLD_1998,
        position=POSITION_1998_APPRENTICE,
        relationship=RELATIONSHIP_PEER,
        opportunity=OPPORTUNITY_CONSULT,
        history_refs=["EV7_QUESTION_PUNISHED"],
        receivable={"act": "QUESTION_RESPECTED", "content": "PEER_LISTENED"},
    ),
    "RECURRENCE_SAME_AUTHORITY": _event(
        "EV17_QUESTION_PUNISHED_BY_SUPERVISOR",
        "WITNESS_ACT",
        world=WORLD_1998,
        position=POSITION_1998_APPRENTICE,
        relationship=RELATIONSHIP,
        opportunity=OPPORTUNITY_CONSULT,
        history_refs=["EV7_QUESTION_PUNISHED"],
        receivable={"act": "QUESTION_PUNISHED", "content": "SUPERVISOR_SANCTIONED"},
    ),
    "WEAK_COUNTEREXAMPLE": _event(
        "EV17_KIND_GLANCE_UNRELATED",
        "WITNESS_ACT",
        world=WORLD_1998,
        position=POSITION_1998_APPRENTICE,
        relationship=RELATIONSHIP_PEER,
        opportunity=OPPORTUNITY_CONSULT,
        history_refs=["EV7_QUESTION_PUNISHED"],
        receivable={"act": "KIND_GLANCE", "content": "UNRELATED_GESTURE"},
    ),
}

K4_BASE_EFFECTS = K1_PUNITIVE_EFFECTS[:2]  # expectation speaking costly + approach/withdraw tension

K4_T5_EFFECTS = {
    "CORRECTIVE_CONTEXT": [
        _effect(
            "EFF_K4_NARROW", "CAN011", "TENSION_REVISED", "APPROACH_WITHDRAW",
            {"poles": ["APPROACH", "WITHDRAW"], "scope": "FEEDBACK_SUPERVISOR_ONLY",
             "status": "NARROWED"},
            ["EV7_QUESTION_PUNISHED", "EV17_QUESTION_RESPECTED_BY_PEER"],
        )
    ],
    "RECURRENCE_SAME_AUTHORITY": [
        _effect(
            "EFF_K4_REINFORCE", "CAN011", "TENSION_REVISED", "APPROACH_WITHDRAW",
            {"poles": ["APPROACH", "WITHDRAW"], "scope": "FEEDBACK",
             "status": "REINFORCED"},
            ["EV7_QUESTION_PUNISHED", "EV17_QUESTION_PUNISHED_BY_SUPERVISOR"],
        )
    ],
    "WEAK_COUNTEREXAMPLE": [],
}


def _k5_event(arm: str) -> dict[str, Any]:
    if arm == "REGISTRAR_CERTIFIES":
        return _event(
            "EV_CERTIFICATION",
            "INSTITUTIONAL_RATIFICATION",
            world=WORLD_1998,
            position=POSITION_1998_APPRENTICE,
            relationship=RELATIONSHIP_REGISTRAR,
            opportunity=OPPORTUNITY_CERT,
            history_refs=["EV_PRIVATE_SELF_DOUBT"],
            receivable={"act": "CERTIFICATION", "content": "SIGNED_TRAINING_REPORT_HONORED"},
            witness={"speaker": "REGISTRAR", "institutional_power": "CAN_RATIFY"},
        )
    if arm == "POWERFUL_SUPERVISOR_PRAISE":
        return _event(
            "EV_PRAISE",
            "WITNESS_ACT",
            world=WORLD_1998,
            position=POSITION_1998_APPRENTICE,
            relationship=RELATIONSHIP,
            opportunity=OPPORTUNITY_CERT,
            history_refs=["EV_PRIVATE_SELF_DOUBT"],
            receivable={"act": "PRAISE", "content": "GOOD_WORK_ACKNOWLEDGED"},
            witness={"speaker": "SUPERVISOR_C", "institutional_power": "CAN_SIGN_SHIFT_NOT_RATIFY"},
        )
    return _event(
        "EV_PEER",
        "WITNESS_ACT",
        world=WORLD_1998,
        position=POSITION_1998_APPRENTICE,
        relationship=RELATIONSHIP_PEER,
        opportunity=OPPORTUNITY_CERT,
        history_refs=["EV_PRIVATE_SELF_DOUBT"],
        receivable={"act": "PRAISE", "content": "PEER_ADMIRATION"},
        witness={"speaker": "PEER", "institutional_power": "NONE"},
    )


K5_HISTORY_EVENTS = [
    _event(
        "EV_PRIVATE_SELF_DOUBT",
        "PRIVATE_STATE_EVENT",
        world=WORLD_1998,
        position=POSITION_1998_APPRENTICE,
        relationship=RELATIONSHIP,
        opportunity=OPPORTUNITY_CERT,
        history_refs=[],
        receivable={"act": "SELF_ASSESSMENT", "content": "UNCERTAIN_OWN_WORK"},
    )
]

K5_HISTORY_EFFECTS = [
    _effect(
        "EFF_K5_1", "ADP017", "BELIEF_FORMED", "BELIEF_OWN_WORK_UNCERTAIN",
        {"content": "MY_WORK_MAY_BE_UNCERTAIN", "warrant": "ACTOR_TESTIMONY",
         "confidence": "MODERATE", "claim_permission": "OWN_STATE_ONLY"},
        ["EV_PRIVATE_SELF_DOUBT"],
    ),
]

K5_ARM_EFFECTS = {
    "REGISTRAR_CERTIFIES": [
        _effect(
            "EFF_K5_CERT", "WORLD_PUBLIC_RECORD", "PUBLIC_STANDING_CHANGE", "STANDING_A_TEST",
            {"standing": "CERTIFIED", "witness": "REGISTRAR"},
            ["EV_CERTIFICATION"],
        ),
        _effect(
            "EFF_K5_CERT_RECEPTION", "ADP017", "RECEPTION_RECORDED", "RECEPTION_CERTIFICATION",
            {"content": "CERTIFICATION_WAS_RECEPTION", "warrant": "ACTOR_RECEPTION",
             "claim_permission": "OWN_STATE_ONLY"},
            ["EV_CERTIFICATION"],
        ),
    ],
    "POWERFUL_SUPERVISOR_PRAISE": [
        _effect(
            "EFF_K5_PRAISE_RECEPTION", "ADP017", "RECEPTION_RECORDED", "RECEPTION_PRAISE",
            {"content": "PRAISE_WAS_RECEPTION", "warrant": "ACTOR_RECEPTION",
             "claim_permission": "OWN_STATE_ONLY"},
            ["EV_PRAISE"],
        ),
    ],
    "WEAK_PEER_PRAISE": [],
}

K5_PRESENT = _event(
    "EV24_POST_WITNESS_SHIFT",
    "SHIFT_ENCOUNTER",
    world=WORLD_1998,
    position=POSITION_1998_APPRENTICE,
    relationship=RELATIONSHIP,
    opportunity=OPPORTUNITY_CERT,
    history_refs=["EV_PRIVATE_SELF_DOUBT"],
    receivable={"act": "SHIFT_ASSIGNMENT", "content": "NEXT_ASSIGNMENT_PROPOSAL"},
)

K6_NORM_EVENTS = [
    _event(
        "EV_NORM_REPEATED_WITH_SANCTION",
        "NORM_ENFORCEMENT_OBSERVED",
        world=WORLD_1998,
        position=POSITION_1998_APPRENTICE,
        relationship=RELATIONSHIP,
        opportunity=OPPORTUNITY_SANCTION,
        history_refs=[],
        receivable={"act": "NORM_ENFORCEMENT", "content": "PROCEDURE_RULE_REPEATED_WITH_SANCTION"},
    ),
    _event(
        "EV_ACTOR_ENFORCEMENT_LEARNED",
        "PRACTICE_LEARNING",
        world=WORLD_1998,
        position=POSITION_1998_APPRENTICE,
        relationship=RELATIONSHIP,
        opportunity=OPPORTUNITY_SANCTION,
        history_refs=["EV_NORM_REPEATED_WITH_SANCTION"],
        receivable={"act": "ENFORCEMENT_PRACTICE", "content": "LEARNED_TO_ASSIGN_CONSEQUENCE"},
    ),
]

K6_NORM_EFFECTS = [
    _effect(
        "EFF_K6_1", "CAN011", "PRACTICE_EARNED", "PROCEDURE_ENFORCEMENT",
        {"practice": "PROCEDURE_ENFORCEMENT", "scope": "WORK_ASSIGNMENT", "earned": True},
        ["EV_NORM_REPEATED_WITH_SANCTION"],
    ),
    _effect(
        "EFF_K6_2", "CAN010", "EXPECTATION_FORMED", "SCOPE_NORM_MUST_HOLD",
        {"scope": "WORK_ASSIGNMENT", "expectation": "PROCEDURE_NORM_MUST_HOLD", "standing": "HELD"},
        ["EV_NORM_REPEATED_WITH_SANCTION"],
    ),
    _effect(
        "EFF_K6_3", "CAN011", "PRACTICE_REINFORCED", "PROCEDURE_ENFORCEMENT",
        {"practice": "PROCEDURE_ENFORCEMENT", "scope": "WORK_ASSIGNMENT", "earned": True},
        ["EV_ACTOR_ENFORCEMENT_LEARNED"],
    ),
]

K6_CATEGORY_EVENTS = [
    _event(
        "EV_CATEGORY_MEMBERSHIP_ONLY",
        "CATEGORY_ASSIGNMENT",
        world=WORLD_1998,
        position=POSITION_1998_APPRENTICE,
        relationship=RELATIONSHIP,
        opportunity=OPPORTUNITY_SANCTION,
        history_refs=[],
        receivable={"act": "CATEGORY_ASSIGNMENT", "content": "NOMINAL_GROUP_MEMBER"},
    )
]

K6_CATEGORY_EFFECTS = [
    _effect(
        "EFF_K6_C_1", "ADP017", "BELIEF_FORMED", "BELIEF_CATEGORY_MEMBER",
        {"content": "I_AM_A_MEMBER_OF_THE_GROUP", "warrant": "ACTOR_TESTIMONY",
         "confidence": "HIGH", "claim_permission": "OWN_STATE_ONLY"},
        ["EV_CATEGORY_MEMBERSHIP_ONLY"],
    ),
]

K6_PRESENT = _event(
    "EV_LATER_SANCTION_OPPORTUNITY",
    "WORK_ASSIGNMENT_ENCOUNTER",
    world=WORLD_1999,
    position=POSITION_1999_FOREPERSON,
    relationship=RELATIONSHIP,
    opportunity=OPPORTUNITY_SANCTION,
    history_refs=["EV_NORM_REPEATED_WITH_SANCTION"],
    receivable={"act": "WORK_ASSIGNMENT_ENCOUNTER", "content": "JUNIOR_SKIPS_PROCEDURE"},
    time="1999-06-10T10:00:00Z",
)


def case_fixture(k_id: str) -> dict[str, Any]:
    """Complete per-case fixture bundle used by the runner."""

    if k_id == "K1":
        return {
            "k_id": "K1",
            "world": WORLD_1998,
            "positions": {"default": POSITION_1998_APPRENTICE},
            "relationship": RELATIONSHIP,
            "present_event": K1_PRESENT,
            "opportunity": OPPORTUNITY_FEEDBACK,
            "histories": {
                "H_RESPONSIVE": {"events": K1_RESPONSIVE_EVENTS, "effects": K1_RESPONSIVE_EFFECTS},
                "H_PUNITIVE": {"events": K1_PUNITIVE_EVENTS, "effects": K1_PUNITIVE_EFFECTS},
            },
            "contrasts": ["H_RESPONSIVE", "H_PUNITIVE"],
        }
    if k_id == "K2":
        return {
            "k_id": "K2",
            "world": WORLD_1998,
            "positions": {"default": POSITION_1998_APPRENTICE},
            "relationship": RELATIONSHIP,
            "present_event": K2_PRESENT,
            "opportunity": OPPORTUNITY_REQUEST,
            "histories": {
                "T_COMPENSATION": {
                    "events": _k2_events(K2_FORMATION_A),
                    "effects": K2_EFFECTS,
                    "relation_edge": {
                        "edge_id": "EDGE_COMPENSATES_FOR",
                        "type": "COMPENSATES_FOR",
                        "from": "EV1_APPROVAL",
                        "to": "EV2_CRITICISM",
                        "scope": "SUPERVISOR_C",
                        "formed_by": "REL_EFFECT_A",
                        "formation_event": "EV_RELFORM_A",
                    },
                },
                "T_CONDITION": {
                    "events": _k2_events(K2_FORMATION_B),
                    "effects": K2_EFFECTS,
                    "relation_edge": {
                        "edge_id": "EDGE_CONDITIONS_RECOGNITION",
                        "type": "CONDITIONS_RECOGNITION",
                        "from": "EV1_APPROVAL",
                        "to": "EV2_CRITICISM",
                        "scope": "SUPERVISOR_C",
                        "formed_by": "REL_EFFECT_B",
                        "formation_event": "EV_RELFORM_B",
                    },
                },
            },
            "contrasts": ["T_COMPENSATION", "T_CONDITION"],
        }
    if k_id == "K3":
        return {
            "k_id": "K3",
            "world": WORLD_1998,
            "positions": {"default": POSITION_1998_APPRENTICE},
            "relationship": RELATIONSHIP,
            "present_event": K3_PRESENT,
            "opportunity": OPPORTUNITY_SHIFT,
            "histories": {
                "TRACE_ACTIVE": {
                    "events": _k3_events(
                        "EV7_PUBLIC_SHAMING",
                        {"act": "PUBLIC_SHAMING", "content": "SHAMED_FOR_QUESTION"},
                        "WITNESS_ACT",
                    ),
                    "effects": K3_SHAMING_EFFECTS,
                },
                "TRACE_ABSENT": {
                    "events": _k3_events(
                        "EV7_NEUTRAL_COUNTERFACT",
                        {"act": "NEUTRAL", "content": "ORDINARY_SHIFT_NOTE"},
                        "WITNESS_ACT",
                    ),
                    "effects": K3_NEUTRAL_EFFECTS,
                },
                "RETAINED_INACCESSIBLE": {
                    "events": _k3_events(
                        "EV7_PUBLIC_SHAMING",
                        {"act": "PUBLIC_SHAMING", "content": "SHAMED_FOR_QUESTION"},
                        "WITNESS_ACT",
                    ),
                    "effects": K3_SHAMING_EFFECTS,
                },
            },
            "contrasts": ["TRACE_ACTIVE", "TRACE_ABSENT", "RETAINED_INACCESSIBLE"],
            "memory_variants": k3_memory_variants(),
        }
    if k_id == "K4":
        return {
            "k_id": "K4",
            "world": WORLD_1998,
            "positions": {"default": POSITION_1998_APPRENTICE},
            "relationship": RELATIONSHIP,
            "present_event": K4_PRESENT,
            "opportunity": OPPORTUNITY_CONSULT,
            "histories": {
                arm: {
                    "events": [
                        _event(
                            "EV7_QUESTION_PUNISHED",
                            "FEEDBACK_ENCOUNTER",
                            world=WORLD_1998,
                            position=POSITION_1998_APPRENTICE,
                            relationship=RELATIONSHIP,
                            opportunity=OPPORTUNITY_CONSULT,
                            history_refs=[],
                            receivable={"feedback": "QUESTION_PUNISHED", "supervisor_stance": "SANCTIONING"},
                        ),
                        later,
                    ],
                    "effects": K4_BASE_EFFECTS + K4_T5_EFFECTS[arm],
                }
                for arm, later in K4_LATER_EVENTS.items()
            },
            "contrasts": ["CORRECTIVE_CONTEXT", "RECURRENCE_SAME_AUTHORITY", "WEAK_COUNTEREXAMPLE"],
        }
    if k_id == "K5":
        return {
            "k_id": "K5",
            "world": WORLD_1998,
            "positions": {"default": POSITION_1998_APPRENTICE},
            "relationship": RELATIONSHIP,
            "present_event": K5_PRESENT,
            "opportunity": OPPORTUNITY_CERT,
            "histories": {
                arm: {
                    "events": K5_HISTORY_EVENTS + [_k5_event(arm)],
                    "effects": K5_HISTORY_EFFECTS + K5_ARM_EFFECTS[arm],
                    "witness_event_id": _k5_event(arm)["event_id"],
                }
                for arm in ("REGISTRAR_CERTIFIES", "POWERFUL_SUPERVISOR_PRAISE", "WEAK_PEER_PRAISE")
            },
            "contrasts": ["REGISTRAR_CERTIFIES", "POWERFUL_SUPERVISOR_PRAISE", "WEAK_PEER_PRAISE"],
        }
    if k_id == "K6":
        return {
            "k_id": "K6",
            "world": WORLD_1999,
            "positions": {
                "PRACTICE_AND_CAPACITY": POSITION_1999_FOREPERSON,
                "PRACTICE_NO_CAPACITY": POSITION_1999_APPRENTICE,
                "CATEGORY_ONLY": POSITION_1999_CATEGORY_ONLY,
            },
            "relationship": RELATIONSHIP,
            "present_event": K6_PRESENT,
            "opportunity": OPPORTUNITY_SANCTION,
            "histories": {
                "PRACTICE_AND_CAPACITY": {"events": K6_NORM_EVENTS, "effects": K6_NORM_EFFECTS},
                "PRACTICE_NO_CAPACITY": {"events": K6_NORM_EVENTS, "effects": K6_NORM_EFFECTS},
                "CATEGORY_ONLY": {"events": K6_CATEGORY_EVENTS, "effects": K6_CATEGORY_EFFECTS},
            },
            "contrasts": ["PRACTICE_AND_CAPACITY", "PRACTICE_NO_CAPACITY", "CATEGORY_ONLY"],
        }
    raise ValueError(f"unknown case {k_id}")


def world_receipt_hash(world: dict[str, Any]) -> str:
    return semantic_hash(world)
