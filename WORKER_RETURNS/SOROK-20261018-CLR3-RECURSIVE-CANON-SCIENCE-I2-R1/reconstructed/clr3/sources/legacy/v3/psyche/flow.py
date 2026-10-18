"""PressureFlow mediation cycle (V515b.2).

PressureFlow is not a narrative generator and not a consciousness shortcut. It is the
runtime membrane that records how historically-conditioned vital charge is routed
through existing v3 psyche mechanics.

Core law:
    Raw structure may influence psyche.
    Raw structure may not speak directly as psyche.

V515b.2 corrections:
    - There is no inert "unexpressed" remainder in a living person.
    - Charge that does not cross the overt Aim-expression gate still routes internally
      and leaves trace.
    - internally_routed_charge is conserved charge.
    - trace_intensity is conductance-amplified effect strength.
    - trace provenance is per-domain.
    - route application is transactional: route effects are first applied to a working
      copy, then committed only after snapshot/history/memory construction succeeds.

Compatibility bridge:
    - DomainState.baseline_load remains the V513 latent structural pressure field.
    - DomainState.expressed_aim is interpreted here only as overt_aim_charge.
    - This module owns the post-year charge-routing audit and trace memory.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from v3.core.enums import DOMAIN_NAMES, domain_axis_to_label
from v3.core.state import BackboneState, clamp
from v3.psyche.channels import SUBLIMATION_CHANNELS, assign_sublimation_channels
from v3.psyche.gating import apply_expression_gating, compute_baseline_load
from v3.psyche.insulation import derive_insulation_profile
from v3.psyche.vitality import derive_vitality_profile
from v3.psyche.vessels import derive_attribution_and_vessel_hint

PRESSURE_FLOW_SCHEMA_VERSION = "v516_surface_psyche_profile"
RECENT_WINDOW_YEARS = 5
MAX_HISTORY_LENGTH = 120

_NUMERIC_TRACE_PATHS = (
    ("capacity", ("time", "money", "health", "social_support", "skill", "mobility", "risk_tolerance", "legitimacy")),
    ("psychological_capacity", ("vitality", "aperture", "reality_anchor", "binding", "coherence", "agency", "transmutation")),
    ("practice_stack", ("study", "care", "organizing", "craft", "spiritual", "risk_training")),
    ("peak_routing", ("harm_constraint", "rage_metabolization", "coherence", "impunity_access")),
    ("intensity_and_capture", ("intensity", "craft_talent", "opportunity_access", "attention_field_exposure", "capture_pressure")),
    ("style_traits", ("playfulness", "novelty_seeking", "conscientiousness", "social_energy", "absurdist_humor", "aesthetic_sensitivity", "impulsivity")),
    ("wound_vector", ("shame", "fear", "anger", "abandonment", "control", "recognition", "loss")),
)

_ROUTE_OBJECTS_TO_COMMIT = (
    "capacity",
    "psychological_capacity",
    "practice_stack",
    "peak_routing",
    "intensity_and_capture",
    "style_traits",
    "wound_vector",
)

_CHANNEL_FELT_REGISTER = {
    "humor_irony": "irony_play_compressed_aggression",
    "hyper_competence": "effort_mastery_self_tightening",
    "caretaking_warmth": "duty_tenderness_guilt_private_irritation",
    "piety_ritual": "surrender_fear_repetition_symbolic_holding",
    "aesthetic_intensification": "beauty_hunger_melancholy_sensory_heightening",
    "withdrawal_numbness": "constriction_low_aperture_fatigue_disappearance_pull",
    "micro_authoritarianism": "control_displacement_ordering_near_others",
    "conspiracy_symbolic": "pattern_hunger_suspicion_fragile_totality",
    "quiet_organizing": "contained_anger_collective_vector_practical_courage",
    "somatic_irritability": "body_noise_hot_edges_irritability_symptom_pressure",
}

_CHANNEL_ORDINARY_ATTRIBUTION = {
    "humor_irony": "things_are_absurd_so_i_joke",
    "hyper_competence": "i_need_to_get_better_and_stay_ahead",
    "caretaking_warmth": "people_need_me_and_this_is_what_one_does",
    "piety_ritual": "God_will_hold_this_or_test_me_through_it",
    "aesthetic_intensification": "beauty_or_art_is_where_the_pressure_can_breathe",
    "withdrawal_numbness": "i_am_tired_negative_or_need_to_be_left_alone",
    "micro_authoritarianism": "someone_has_to_keep_order_or_people_will_ruin_things",
    "conspiracy_symbolic": "hidden_forces_are_arranging_this_against_us_or_me",
    "quiet_organizing": "this_can_be_changed_if_we_move_carefully_together",
    "somatic_irritability": "my_body_is_off_or_everything_gets_under_my_skin",
}

# V515b.2 still treats vessel as a hint, not a full vessel model. A real vessel
# registry belongs after the runtime membrane proves charge provenance and history.
_CHANNEL_VESSEL_HINT = {
    "humor_irony": "joke_style_social_distance_or_absurdity_vessel",
    "hyper_competence": "study_work_craft_mastery_vessel",
    "caretaking_warmth": "family_duty_care_role_or_religious_service_vessel",
    "piety_ritual": "ritual_prayer_surrender_or_obedience_vessel",
    "aesthetic_intensification": "art_beauty_romance_sensory_or_private_world_vessel",
    "withdrawal_numbness": "bedroom_silence_sleep_screen_fantasy_or_disappearance_vessel",
    "micro_authoritarianism": "local_order_household_rules_workplace_control_vessel",
    "conspiracy_symbolic": "hidden_totality_enemy_pattern_or_online_explanation_vessel",
    "quiet_organizing": "collective_practical_friend_group_union_church_or_mutual_aid_vessel",
    "somatic_irritability": "body_symptom_pain_food_sleep_or_health_anxiety_vessel",
}

_SURFACE_CHARGE_BANDS = (
    (5.0, "dormant"),
    (25.0, "low"),
    (55.0, "moderate"),
    (80.0, "high"),
)

_SURFACE_OVERT_AIM_BANDS = (
    (0.10, "suppressed"),
    (0.35, "latent"),
    (0.70, "salient"),
)

_SURFACE_INTERNAL_ROUTE_BANDS = (
    (0.10, "trace"),
    (0.35, "minor"),
    (0.70, "major"),
)

_SURFACE_AVOIDANCE_BY_CHANNEL = {
    "humor_irony": "deflective",
    "hyper_competence": "overcontrolled",
    "caretaking_warmth": "relationally_defensive",
    "piety_ritual": "ritualized",
    "aesthetic_intensification": "aesthetic_sublimation",
    "withdrawal_numbness": "avoidant",
    "micro_authoritarianism": "controlling",
    "conspiracy_symbolic": "projective",
    "quiet_organizing": "contained",
    "somatic_irritability": "somatic_reactive",
}

_SURFACE_POSTURE_BY_GATE = {
    "gate_open_but_not_voice_permission": "public",
    "flickering_requires_vessel": "split",
    "blocked_by_distortion": "private",
    "blocked_unknown": "inner",
}

_ANALYST_ROUTE_ACCOUNT = {
    "humor_irony": "charge routed into symbolic distancing and socialized pressure release",
    "hyper_competence": "charge routed into mastery, performance, and self-tightening",
    "caretaking_warmth": "charge routed into relational reproduction, care, and duty management",
    "piety_ritual": "charge routed through religious-symbolic repetition and surrender vessel",
    "aesthetic_intensification": "charge routed into beauty, craft, sensibility, and melancholy form",
    "withdrawal_numbness": "charge routed into aperture constriction, risk withdrawal, and low outward claim",
    "micro_authoritarianism": "charge routed into local control and displaced domination of proximate field",
    "conspiracy_symbolic": "charge routed into totalizing symbolic suspicion under weak reality anchor",
    "quiet_organizing": "charge routed into collective-practical action without automatic narrative lucidity",
    "somatic_irritability": "charge routed into bodily symptom/noise and anger edge",
}

_EXPECTED_TRACE_PATH_BY_CHANNEL = {
    "humor_irony": "style_traits.absurdist_humor",
    "hyper_competence": "practice_stack.study",
    "caretaking_warmth": "practice_stack.care",
    "piety_ritual": "practice_stack.spiritual",
    "aesthetic_intensification": "style_traits.aesthetic_sensitivity",
    "withdrawal_numbness": "psychological_capacity.aperture",
    "micro_authoritarianism": "style_traits.conscientiousness",
    "conspiracy_symbolic": "psychological_capacity.reality_anchor",
    "quiet_organizing": "practice_stack.organizing",
    "somatic_irritability": "capacity.health",
}


class PressureFlowError(RuntimeError):
    """Raised when the pressure-flow membrane cannot complete without hiding damage."""


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _snapshot_numeric_state(state: BackboneState) -> dict[str, float]:
    snap: dict[str, float] = {}
    for obj_name, fields in _NUMERIC_TRACE_PATHS:
        obj = getattr(state, obj_name, None)
        if obj is None:
            continue
        for field in fields:
            if hasattr(obj, field):
                snap[f"{obj_name}.{field}"] = round(_safe_float(getattr(obj, field), 0.0), 4)
    return snap


def _numeric_delta(before: dict[str, float], after: dict[str, float]) -> dict[str, float]:
    delta: dict[str, float] = {}
    for key in sorted(set(before) | set(after)):
        diff = round(after.get(key, 0.0) - before.get(key, 0.0), 4)
        if abs(diff) >= 0.0001:
            delta[key] = diff
    return delta


def _compact_event_context(state: BackboneState) -> dict[str, Any]:
    events = getattr(state, "events_this_year", []) or []
    micro = getattr(state, "micro_trace_this_year", []) or []
    event_types: dict[str, int] = {}
    for item in events:
        if not isinstance(item, dict):
            continue
        kind = str(item.get("type") or item.get("event_type") or item.get("id") or "unknown")
        event_types[kind] = event_types.get(kind, 0) + 1
    micro_types: dict[str, int] = {}
    for item in micro:
        if not isinstance(item, dict):
            continue
        kind = str(item.get("type") or item.get("source") or item.get("id") or "unknown")
        micro_types[kind] = micro_types.get(kind, 0) + 1
    return {
        "events_this_year_count": len(events) if isinstance(events, list) else 0,
        "micro_trace_this_year_count": len(micro) if isinstance(micro, list) else 0,
        "event_type_counts": event_types,
        "micro_trace_type_counts": micro_types,
    }


def _wound_mean(state: BackboneState) -> float:
    values = []
    for key in ("shame", "fear", "anger", "abandonment", "control", "recognition", "loss"):
        values.append(_safe_float(getattr(state.wound_vector, key, 50.0), 50.0))
    return sum(values) / max(1, len(values))


def _prior_memory(state: BackboneState) -> dict[str, Any]:
    memory = getattr(state, "pressure_flow_memory", {})
    return memory if isinstance(memory, dict) else {}


def _relational_field_conductance_bonus(state: BackboneState, domain_name: str, channel: str) -> float:
    """Small explicit mediation from relational-field projection into trace conductance."""
    strata_salience = getattr(state, "strata_salience", {})
    if not isinstance(strata_salience, dict):
        return 0.0
    relational = strata_salience.get("relational_field")
    if not isinstance(relational, dict):
        return 0.0
    if str(relational.get("status") or "").lower() != "ok":
        return 0.0
    absolute_horizon = relational.get("absolute_horizon") if isinstance(relational.get("absolute_horizon"), dict) else {}
    strata_count = _safe_float(relational.get("strata_count", 0), 0.0)
    bonus = min(0.04, strata_count / 250.0)
    if absolute_horizon and not bool(absolute_horizon.get("surface_export_allowed", True)):
        bonus += 0.02
    if domain_name in ("family_household", "neighborhood_household"):
        bonus += 0.02
    if channel in ("quiet_organizing", "caretaking_warmth"):
        bonus += 0.02
    elif channel in ("micro_authoritarianism", "conspiracy_symbolic"):
        bonus -= 0.01
    return round(clamp(bonus, -0.03, 0.08), 3)


def _prior_groove(memory: dict[str, Any], domain_name: str, channel: str) -> float:
    grooves = memory.get("grooves") if isinstance(memory.get("grooves"), dict) else {}
    domain_grooves = grooves.get(domain_name) if isinstance(grooves.get(domain_name), dict) else {}
    return clamp(_safe_float(domain_grooves.get(channel), 0.0), 0.0, 100.0)


def _derive_current_charge(state: BackboneState, domain_name: str) -> float:
    """Derive vital charge active in this domain this year.

    Charge is anchored to baseline_load but is not reduced because vitality is low.
    Exhaustion alters conductance and recovery cost; it does not make contradiction
    disappear. Route-specific wound sensitivity is intentionally deferred to the next
    vessel/channel pack; this membrane only needs a bounded pressure sensitivity term.
    """
    domain = state.domains.get(domain_name)
    if domain is None:
        return 0.0
    latent_pressure = _safe_float(getattr(domain, "baseline_load", 0.0), 0.0)
    inner_load = _safe_float(getattr(state.registers, "inner_load", 50.0), 50.0)
    wound_mean = _wound_mean(state)
    inner_load_factor = 0.90 + (inner_load / 500.0)  # 0.90 - 1.10
    wound_factor = 0.92 + (wound_mean / 625.0)       # 0.92 - 1.08
    return round(clamp(latent_pressure * inner_load_factor * wound_factor), 3)


def _structural_gate_label(domain: Any) -> str:
    a_label = domain_axis_to_label("A", _safe_float(getattr(domain, "A", 0.0), 0.0))
    if a_label == "structural":
        return "gate_open_but_not_voice_permission"
    if a_label == "partial":
        return "flickering_requires_vessel"
    if a_label == "distorted":
        return "blocked_by_distortion"
    return "blocked_unknown"


def _surface_band(value: float, bands: tuple[tuple[float, str], ...], fallback: str) -> str:
    for threshold, label in bands:
        if value < threshold:
            return label
    return fallback


def _surface_charge_band(value: float) -> str:
    return _surface_band(clamp(_safe_float(value, 0.0), 0.0, 100.0), _SURFACE_CHARGE_BANDS, "extreme")


def _surface_overt_aim_band(current_charge: float, overt_aim_charge: float) -> str:
    current_charge = clamp(_safe_float(current_charge, 0.0), 0.0, 100.0)
    overt_aim_charge = clamp(_safe_float(overt_aim_charge, 0.0), 0.0, 100.0)
    if current_charge <= 0.0:
        return "none"
    ratio = overt_aim_charge / current_charge if current_charge else 0.0
    return _surface_band(ratio, _SURFACE_OVERT_AIM_BANDS, "overt")


def _surface_internal_route_band(current_charge: float, internally_routed_charge: float) -> str:
    current_charge = clamp(_safe_float(current_charge, 0.0), 0.0, 100.0)
    internally_routed_charge = clamp(_safe_float(internally_routed_charge, 0.0), 0.0, 100.0)
    if current_charge <= 0.0:
        return "none"
    ratio = internally_routed_charge / current_charge if current_charge else 0.0
    return _surface_band(ratio, _SURFACE_INTERNAL_ROUTE_BANDS, "dominant")


def _surface_avoidance_or_deflection(primary_channel: str) -> str:
    return _SURFACE_AVOIDANCE_BY_CHANNEL.get(primary_channel, "compartmentalized")


def _surface_public_private_inner_posture(item: dict[str, Any]) -> str:
    gate = str(item.get("structural_consideration_gate") or "blocked_unknown")
    return _SURFACE_POSTURE_BY_GATE.get(gate, "inner")


def _surface_historical_relation(name: str, item: dict[str, Any], memory: dict[str, Any]) -> str:
    historical = memory.get("historical_relation") if isinstance(memory.get("historical_relation"), dict) else {}
    grooves = memory.get("grooves") if isinstance(memory.get("grooves"), dict) else {}
    dominant = memory.get("dominant_channel_by_domain") if isinstance(memory.get("dominant_channel_by_domain"), dict) else {}
    recent = memory.get("recent_dominant_channel_by_domain") if isinstance(memory.get("recent_dominant_channel_by_domain"), dict) else {}
    relation = str(historical.get(name) or "first_recorded_cycle")
    groove_values = grooves.get(name) if isinstance(grooves.get(name), dict) else {}
    groove_total = 0.0
    for value in groove_values.values():
        groove_total += _safe_float(value, 0.0)
    if relation == "first_recorded_cycle":
        return "degraded"
    if groove_total >= 3.0 and dominant.get(name) and recent.get(name) == dominant.get(name):
        return "chronic/old_groove"
    if relation in ("rising_against_prior_recent_history", "falling_against_prior_recent_history"):
        return "recent_shift"
    if recent.get(name) and dominant.get(name) and recent.get(name) != dominant.get(name):
        return "recent_shift"
    if item.get("primary_channel") and recent.get(name) and item.get("primary_channel") != recent.get(name):
        return "recent_shift"
    return "continuous"


def _dominant_channel(domain: Any) -> str:
    ch = str(getattr(domain, "affect_channel", "compartmentalization") or "compartmentalization")
    if ch in SUBLIMATION_CHANNELS:
        return ch
    return "compartmentalization"


def _channel_conductance(state: BackboneState, domain_name: str, channel: str, memory: dict[str, Any]) -> float:
    """Return bounded trace-effect conductance.

    Conductance does not create additional conserved charge. It changes how strongly
    internally routed charge etches trace in the person.
    """
    conductance = 1.0
    groove = _prior_groove(memory, domain_name, channel)
    conductance += min(0.35, groove / 250.0)

    vitality = _safe_float(getattr(state.psychological_capacity, "vitality", 50.0), 50.0)
    agency = _safe_float(getattr(state.psychological_capacity, "agency", 50.0), 50.0)
    aperture = _safe_float(getattr(state.psychological_capacity, "aperture", 50.0), 50.0)
    social_support = _safe_float(getattr(state.capacity, "social_support", 50.0), 50.0)
    network_density = _safe_float(getattr(state.collective_infrastructure, "network_density", 0.0), 0.0)
    repression_pressure = _safe_float(getattr(state.collective_infrastructure, "repression_pressure", 0.0), 0.0)

    if vitality <= 35.0:
        if channel in ("withdrawal_numbness", "somatic_irritability"):
            conductance += 0.18
        if channel in ("quiet_organizing", "hyper_competence"):
            conductance -= 0.16
    elif vitality >= 70.0:
        if channel in ("quiet_organizing", "hyper_competence", "aesthetic_intensification"):
            conductance += 0.08

    if channel == "quiet_organizing":
        conductance += min(0.18, (social_support + network_density) / 800.0)
        conductance -= min(0.12, repression_pressure / 700.0)
    if channel == "piety_ritual" and _safe_float(getattr(state.practice_stack, "spiritual", 0.0), 0.0) >= 50.0:
        conductance += 0.08
    if channel == "aesthetic_intensification" and aperture >= 60.0:
        conductance += 0.06
    if channel == "micro_authoritarianism" and agency < 40.0:
        conductance += 0.08
    conductance += _relational_field_conductance_bonus(state, domain_name, channel)

    return round(clamp(conductance, 0.65, 1.45), 3)


def _domain_charge_ledger(state: BackboneState, memory: dict[str, Any]) -> dict[str, dict[str, Any]]:
    ledger: dict[str, dict[str, Any]] = {}
    for name in DOMAIN_NAMES:
        domain = state.domains.get(name)
        if domain is None:
            continue
        current_charge = _derive_current_charge(state, name)
        overt_aim_charge = clamp(_safe_float(getattr(domain, "expressed_aim", 0.0), 0.0))
        overt_aim_charge = min(overt_aim_charge, current_charge)
        internally_routed_charge = max(0.0, round(current_charge - overt_aim_charge, 3))
        ch = _dominant_channel(domain)
        conductance = _channel_conductance(state, name, ch, memory)
        trace_intensity = round(internally_routed_charge * conductance, 3)
        vessel = derive_attribution_and_vessel_hint(
            state,
            name,
            ch,
            {
                "current_charge": current_charge,
                "overt_aim_charge": overt_aim_charge,
                "internally_routed_charge": internally_routed_charge,
                "trace_intensity": trace_intensity,
            },
            memory,
        )
        insulation = derive_insulation_profile(
            state,
            name,
            {
                "current_charge": current_charge,
                "overt_aim_charge": overt_aim_charge,
                "internally_routed_charge": internally_routed_charge,
                "trace_intensity": trace_intensity,
                "primary_channel": ch,
            },
            vessel,
            memory,
        )
        ledger[name] = {
            "latent_structural_pressure": round(_safe_float(getattr(domain, "baseline_load", 0.0), 0.0), 3),
            "current_charge": current_charge,
            "overt_aim_charge": round(overt_aim_charge, 3),
            "overt_aim_charge_semantics": "overt_aim_charge_only_not_total_external_expression",
            "internally_routed_charge": internally_routed_charge,
            "channel_conductance": conductance,
            "trace_intensity": trace_intensity,
            "trace_intensity_semantics": "conductance_amplified_effect_strength_not_additional_charge",
            "primary_channel": ch,
            "vessel_hint": vessel["vessel_hint"],
            "ordinary_attribution": vessel["ordinary_attribution"],
            "attribution_confidence": vessel["attribution_confidence"],
            "vessel_status": vessel["vessel_status"],
            "insulation_mode": insulation["insulation_mode"],
            "cognitive_shelter": insulation["cognitive_shelter"],
            "insulation_confidence": insulation["insulation_confidence"],
            "insulation_status": insulation["insulation_status"],
            "felt_register": _CHANNEL_FELT_REGISTER.get(ch, "compartmentalized_pressure"),
            "structural_consideration_gate": _structural_gate_label(domain),
        }
    return ledger


def _merge_vitality_profile(charge_ledger: dict[str, dict[str, Any]], vitality_profile: dict[str, Any]) -> None:
    if not isinstance(vitality_profile, dict):
        return
    global_profile = vitality_profile.get("global") if isinstance(vitality_profile.get("global"), dict) else {}
    domain_profiles = vitality_profile.get("domains") if isinstance(vitality_profile.get("domains"), dict) else {}
    for name, item in charge_ledger.items():
        domain_profile = domain_profiles.get(name) if isinstance(domain_profiles.get(name), dict) else {}
        if global_profile:
            item["vitality_schema_version"] = vitality_profile.get("schema_version", "v519_vitality_fatigue_age_phase_future_horizon")
            item["age_phase"] = global_profile.get("age_phase", "unknown")
            item["vitality_band"] = global_profile.get("vitality_band", "moderate")
            item["fatigue_band"] = global_profile.get("fatigue_band", "moderate")
            item["future_horizon"] = global_profile.get("future_horizon", "moderate")
            item["future_horizon_years"] = global_profile.get("future_horizon_years", 4)
            item["recovery_cost"] = global_profile.get("recovery_cost", 0.0)
            item["conductance_multiplier"] = global_profile.get("conductance_multiplier", 1.0)
            item["routing_bias"] = global_profile.get("routing_bias", "balanced")
        if domain_profile:
            item.update(
                {
                    "domain_age_phase": domain_profile.get("age_phase", item.get("age_phase", "unknown")),
                    "domain_vitality_band": domain_profile.get("vitality_band", item.get("vitality_band", "moderate")),
                    "domain_fatigue_band": domain_profile.get("fatigue_band", item.get("fatigue_band", "moderate")),
                    "domain_future_horizon": domain_profile.get("future_horizon", item.get("future_horizon", "moderate")),
                    "domain_future_horizon_years": domain_profile.get("future_horizon_years", item.get("future_horizon_years", 4)),
                    "domain_recovery_cost": domain_profile.get("recovery_cost", item.get("recovery_cost", 0.0)),
                    "domain_conductance_multiplier": domain_profile.get("conductance_multiplier", item.get("conductance_multiplier", 1.0)),
                    "domain_routing_bias": domain_profile.get("routing_bias", item.get("routing_bias", "balanced")),
                }
            )


def _apply_single_domain_route(state: BackboneState, item: dict[str, Any]) -> None:
    """Apply one domain's internally routed charge to a working state only."""
    routed = _safe_float(item.get("trace_intensity"), 0.0)
    if routed <= 0.0:
        return
    ch = str(item.get("primary_channel") or "compartmentalization")
    if ch == "humor_irony":
        state.style_traits.absurdist_humor += routed * 0.10
    elif ch == "hyper_competence":
        state.practice_stack.study += routed * 0.05
        state.practice_stack.craft += routed * 0.05
        state.intensity_and_capture.craft_talent += routed * 0.02
    elif ch == "caretaking_warmth":
        state.practice_stack.care += routed * 0.08
        state.practice_stack.spiritual += routed * 0.01
    elif ch == "piety_ritual":
        state.practice_stack.spiritual += routed * 0.08
        state.peak_routing.coherence += routed * 0.02
    elif ch == "aesthetic_intensification":
        state.style_traits.aesthetic_sensitivity += routed * 0.07
        state.practice_stack.craft += routed * 0.03
    elif ch == "withdrawal_numbness":
        state.psychological_capacity.aperture -= routed * 0.03
        state.practice_stack.risk_training -= routed * 0.05
    elif ch == "micro_authoritarianism":
        state.style_traits.conscientiousness += routed * 0.04
        state.peak_routing.coherence += routed * 0.01
    elif ch == "conspiracy_symbolic":
        state.psychological_capacity.reality_anchor -= routed * 0.03
        state.peak_routing.theory_of_change_style = "witness_exposure"
    elif ch == "quiet_organizing":
        state.practice_stack.organizing += routed * 0.08
        state.peak_routing.coherence += routed * 0.02
    elif ch == "somatic_irritability":
        state.capacity.health -= routed * 0.02
        state.wound_vector.anger += routed * 0.05
    else:
        state.practice_stack.craft += routed * 0.02

    state.capacity.clamp_all()
    state.psychological_capacity.clamp_all()
    state.practice_stack.clamp_all()
    state.peak_routing.clamp_all()
    state.style_traits.clamp_all()
    state.wound_vector.clamp_all()


def _simulate_domain_routes_transactionally(
    state: BackboneState,
    charge_ledger: dict[str, dict[str, Any]],
) -> tuple[BackboneState, dict[str, dict[str, float]], dict[str, float]]:
    """Apply routes to a working copy and return exact per-domain and aggregate deltas.

    The original state is not mutated here. This is the V515b.2 audit membrane: if later
    snapshot/memory construction fails, no route effects have been committed.
    """
    working = deepcopy(state)
    per_domain_trace_delta: dict[str, dict[str, float]] = {}
    for domain_name in DOMAIN_NAMES:
        item = charge_ledger.get(domain_name)
        if not item:
            continue
        before = _snapshot_numeric_state(working)
        _apply_single_domain_route(working, item)
        after = _snapshot_numeric_state(working)
        per_domain_trace_delta[domain_name] = _numeric_delta(before, after)
    aggregate = _numeric_delta(_snapshot_numeric_state(state), _snapshot_numeric_state(working))
    return working, per_domain_trace_delta, aggregate


def _commit_route_state(original: BackboneState, routed: BackboneState) -> None:
    for obj_name in _ROUTE_OBJECTS_TO_COMMIT:
        setattr(original, obj_name, deepcopy(getattr(routed, obj_name)))
    original.clamp_all()


def _compact_surface_profile(
    charge_ledger: dict[str, dict[str, Any]],
    memory: dict[str, Any],
    vitality_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    domains: dict[str, Any] = {}
    for name, item in charge_ledger.items():
        primary_channel = str(item.get("primary_channel") or "compartmentalization")
        domains[name] = {
            "felt_register": item.get("felt_register", "compartmentalized_pressure"),
            "ordinary_attribution": item.get("ordinary_attribution", "this_is_just_how_things_are"),
            "attribution_confidence": item.get("attribution_confidence", "low"),
            "vessel_hint": item.get("vessel_hint", "unspecified_compartmentalization_vessel"),
            "vessel_status": "placeholder_hint_not_full_vessel_model",
            "insulation_mode": item.get("insulation_mode", "compartmentalization"),
            "cognitive_shelter": item.get("cognitive_shelter", "fallback_channel_container"),
            "insulation_confidence": item.get("insulation_confidence", "low"),
            "insulation_status": item.get("insulation_status", "low_confidence_fallback"),
            "age_phase": item.get("age_phase", "unknown"),
            "vitality_band": item.get("vitality_band", "moderate"),
            "fatigue_band": item.get("fatigue_band", "moderate"),
            "future_horizon": item.get("future_horizon", "moderate"),
            "future_horizon_years": item.get("future_horizon_years", 4),
            "recovery_cost": item.get("recovery_cost", 0.0),
            "conductance_multiplier": item.get("conductance_multiplier", 1.0),
            "routing_bias": item.get("routing_bias", "balanced"),
            "avoidance_or_deflection": _surface_avoidance_or_deflection(primary_channel),
            "public_private_inner_posture": _surface_public_private_inner_posture(item),
            "historical_relation": _surface_historical_relation(name, item, memory),
            "dominant_channel": primary_channel,
            "charge_band": _surface_charge_band(item.get("current_charge", 0.0)),
            "overt_aim_band": _surface_overt_aim_band(item.get("current_charge", 0.0), item.get("overt_aim_charge", 0.0)),
            "internally_routed_band": _surface_internal_route_band(item.get("current_charge", 0.0), item.get("internally_routed_charge", 0.0)),
            "charge_relation_to_prior_history": (memory.get("historical_relation") or {}).get(name, "insufficient_history"),
        }
    return {
        "schema_version": PRESSURE_FLOW_SCHEMA_VERSION,
        "export_rule": "mediated_surface_only_not_persona_voice_permission",
        "domains": domains,
        "dominant_recent_channels": memory.get("recent_dominant_channel_by_domain", {}),
        "vitality_profile": vitality_profile or {},
    }


def _analyst_account(
    charge_ledger: dict[str, dict[str, Any]],
    trace_delta: dict[str, float],
    per_domain_trace_delta: dict[str, dict[str, float]],
) -> dict[str, Any]:
    domains: dict[str, Any] = {}
    for name, item in charge_ledger.items():
        ch = item["primary_channel"]
        domains[name] = {
            "latent_structural_pressure": item["latent_structural_pressure"],
            "current_charge": item["current_charge"],
            "overt_aim_charge": item["overt_aim_charge"],
            "internally_routed_charge": item["internally_routed_charge"],
            "channel_conductance": item["channel_conductance"],
            "trace_intensity": item["trace_intensity"],
            "primary_channel": ch,
            "vessel_hint": item["vessel_hint"],
            "vessel_status": item["vessel_status"],
            "route_account": _ANALYST_ROUTE_ACCOUNT.get(ch, "charge routed through fallback compartmentalization"),
            "per_domain_trace_delta": per_domain_trace_delta.get(name, {}),
            "voice_export_allowed": False,
        }
    return {
        "schema_version": PRESSURE_FLOW_SCHEMA_VERSION,
        "export_rule": "analyst_model_only_do_not_render_as_persona_consciousness",
        "domains": domains,
        "trace_delta": trace_delta,
        "per_domain_trace_delta": per_domain_trace_delta,
    }


def _history_after_append(state: BackboneState, snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    history = getattr(state, "pressure_flow_history", None)
    if not isinstance(history, list):
        history = []
    history = [x for x in history if isinstance(x, dict)]
    history.append(snapshot)
    if len(history) > MAX_HISTORY_LENGTH:
        history = history[-MAX_HISTORY_LENGTH:]
    return history


def _avg(values: list[float]) -> float:
    return round(sum(values) / max(1, len(values)), 3)


def _relation_to_prior(current: float, prior_values: list[float]) -> str:
    if not prior_values:
        return "first_recorded_cycle"
    prior_recent = prior_values[-RECENT_WINDOW_YEARS:]
    prior_avg = _avg(prior_recent)
    if current >= prior_avg + 10.0:
        return "rising_against_prior_recent_history"
    if current <= prior_avg - 10.0:
        return "falling_against_prior_recent_history"
    return "continuous_with_prior_recent_history"


def _update_memory(history: list[dict[str, Any]], previous_memory: dict[str, Any] | None = None) -> dict[str, Any]:
    previous_memory = previous_memory if isinstance(previous_memory, dict) else {}
    recent = history[-RECENT_WINDOW_YEARS:]
    lifetime_domain_charge_avg: dict[str, float] = {}
    recent_domain_charge_avg: dict[str, float] = {}
    lifetime_channel_totals: dict[str, float] = {}
    recent_channel_totals: dict[str, float] = {}
    dominant_channel_by_domain: dict[str, str] = {}
    recent_dominant_channel_by_domain: dict[str, str] = {}
    historical_relation: dict[str, str] = {}
    grooves: dict[str, dict[str, float]] = deepcopy(previous_memory.get("grooves") or {})
    if not isinstance(grooves, dict):
        grooves = {}

    for domain in DOMAIN_NAMES:
        lifetime_values: list[float] = []
        recent_values: list[float] = []
        lifetime_routes: dict[str, float] = {}
        recent_routes: dict[str, float] = {}
        prior_values: list[float] = []
        for idx, row in enumerate(history):
            item = ((row.get("charge_ledger") or {}).get(domain) or {}) if isinstance(row, dict) else {}
            charge = _safe_float(item.get("current_charge"), 0.0)
            traced = _safe_float(item.get("trace_intensity", item.get("internally_routed_charge")), 0.0)
            ch = str(item.get("primary_channel") or "compartmentalization")
            lifetime_values.append(charge)
            lifetime_routes[ch] = lifetime_routes.get(ch, 0.0) + traced
            if idx < len(history) - 1:
                prior_values.append(charge)
        for row in recent:
            item = ((row.get("charge_ledger") or {}).get(domain) or {}) if isinstance(row, dict) else {}
            charge = _safe_float(item.get("current_charge"), 0.0)
            traced = _safe_float(item.get("trace_intensity", item.get("internally_routed_charge")), 0.0)
            ch = str(item.get("primary_channel") or "compartmentalization")
            recent_values.append(charge)
            recent_routes[ch] = recent_routes.get(ch, 0.0) + traced

        lifetime_domain_charge_avg[domain] = _avg(lifetime_values)
        recent_domain_charge_avg[domain] = _avg(recent_values)
        if lifetime_routes:
            dominant_channel_by_domain[domain] = max(lifetime_routes, key=lifetime_routes.get)
        if recent_routes:
            recent_dominant_channel_by_domain[domain] = max(recent_routes, key=recent_routes.get)

        current = lifetime_values[-1] if lifetime_values else 0.0
        historical_relation[domain] = _relation_to_prior(current, prior_values)

        domain_grooves = grooves.get(domain) if isinstance(grooves.get(domain), dict) else {}
        domain_grooves = {str(k): round(clamp(_safe_float(v, 0.0) * 0.985), 3) for k, v in domain_grooves.items()}
        current_item = ((history[-1].get("charge_ledger") or {}).get(domain) or {}) if history else {}
        current_channel = str(current_item.get("primary_channel") or "compartmentalization")
        current_traced = _safe_float(current_item.get("trace_intensity", current_item.get("internally_routed_charge")), 0.0)
        if current_traced > 0.0:
            domain_grooves[current_channel] = round(clamp(domain_grooves.get(current_channel, 0.0) + current_traced * 0.035), 3)
        grooves[domain] = domain_grooves
        for ch, total in lifetime_routes.items():
            lifetime_channel_totals[ch] = round(lifetime_channel_totals.get(ch, 0.0) + total, 3)
        for ch, total in recent_routes.items():
            recent_channel_totals[ch] = round(recent_channel_totals.get(ch, 0.0) + total, 3)

    return {
        "schema_version": PRESSURE_FLOW_SCHEMA_VERSION,
        "cycles_recorded": len(history),
        "recent_window_years": RECENT_WINDOW_YEARS,
        "lifetime_domain_charge_avg": lifetime_domain_charge_avg,
        "recent_domain_charge_avg": recent_domain_charge_avg,
        "lifetime_channel_totals": lifetime_channel_totals,
        "recent_channel_totals": recent_channel_totals,
        "dominant_channel_by_domain": dominant_channel_by_domain,
        "recent_dominant_channel_by_domain": recent_dominant_channel_by_domain,
        "historical_relation": historical_relation,
        "grooves": grooves,
    }


def run_pressure_flow_cycle(
    state: BackboneState,
    *,
    assign_channels: bool = True,
    compute_pressure: bool = True,
    apply_gating: bool = True,
    route_internal_charge: bool = True,
) -> dict[str, Any]:
    """Run the V515b.2 post-year pressure-flow membrane.

    Deterministic, non-generative, and historically self-modifying. It does not
    produce persona text, activate frameworks, or grant voice access to analyst pressure.
    """
    try:
        if assign_channels:
            assign_sublimation_channels(state)
        if compute_pressure:
            compute_baseline_load(state)
        if apply_gating:
            apply_expression_gating(state)

        prior_memory = _prior_memory(state)
        charge_ledger = _domain_charge_ledger(state, prior_memory)
        vitality_profile = derive_vitality_profile(state, charge_ledger, prior_memory)
        _merge_vitality_profile(charge_ledger, vitality_profile)

        if route_internal_charge:
            routed_state, per_domain_trace_delta, trace_delta = _simulate_domain_routes_transactionally(state, charge_ledger)
        else:
            routed_state = deepcopy(state)
            per_domain_trace_delta = {name: {} for name in charge_ledger}
            trace_delta = {}

        snapshot = {
            "schema_version": PRESSURE_FLOW_SCHEMA_VERSION,
            "year": int(getattr(state, "year", 0)),
            "age": int(getattr(state, "age", 0)),
            "event_context": _compact_event_context(state),
            "charge_ledger": charge_ledger,
            "per_domain_trace_delta": per_domain_trace_delta,
            "trace_delta": trace_delta,
            "vitality_profile": vitality_profile,
            "export_rule": "history_evidence_not_persona_voice",
        }
        history = _history_after_append(state, snapshot)
        memory = _update_memory(history, prior_memory)
        memory["vitality_profile"] = deepcopy(vitality_profile)
        surface = _compact_surface_profile(charge_ledger, memory, vitality_profile)
        analyst = _analyst_account(charge_ledger, trace_delta, per_domain_trace_delta)

        # Transactional commit point: no route mutation is applied to the live state until
        # snapshot, memory, surface, and analyst accounts have all been built successfully.
        _commit_route_state(state, routed_state)
        state.pressure_flow_history = history
        state.pressure_flow_memory = memory
        state.surface_psyche_profile = surface
        state.analyst_pressure_account = analyst
        state.yearly_integrity["pressure_flow"] = {
            "status": "clean",
            "schema_version": PRESSURE_FLOW_SCHEMA_VERSION,
            "cycle_recorded": True,
            "history_length": len(history),
            "fields_impacted": [
                "pressure_flow_history",
                "pressure_flow_memory",
                "surface_psyche_profile",
                "analyst_pressure_account",
                "vitality_profile",
            ],
        }
        return snapshot
    except Exception as exc:  # diagnostic then re-raise; caller decides whether to degrade or stop.
        diag = {
            "stage": "pressure_flow",
            "status": "error",
            "fallback_used": False,
            "fallback_reason": "pressure_flow_cycle_failed",
            "fields_impacted": [
                "pressure_flow_history",
                "pressure_flow_memory",
                "surface_psyche_profile",
                "analyst_pressure_account",
                "vitality_profile",
            ],
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
        }
        if hasattr(state, "generation_diagnostics"):
            state.generation_diagnostics.append(diag)
        state.yearly_integrity["pressure_flow"] = diag
        raise PressureFlowError(str(exc)) from exc
