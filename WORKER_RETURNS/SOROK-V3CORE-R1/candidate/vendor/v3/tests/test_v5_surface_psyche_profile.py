from __future__ import annotations

from v3.core.enums import DOMAIN_NAMES
from v3.core.state import BackboneState
from v3.psyche.flow import PRESSURE_FLOW_SCHEMA_VERSION, _compact_surface_profile, run_pressure_flow_cycle


def _make_state(*, channel: str = "quiet_organizing", baseline: float = 88.0, expressed: float = 8.0) -> BackboneState:
    state = BackboneState()
    for domain in state.domains.values():
        domain.baseline_load = baseline
        domain.expressed_aim = expressed
        domain.affect_channel = channel
    return state


def _make_history_row(
    *,
    channel: str,
    charge: float,
    trace_intensity: float,
    overt_aim_charge: float = 8.0,
) -> dict[str, object]:
    charge_ledger: dict[str, dict[str, object]] = {}
    for name in DOMAIN_NAMES:
        charge_ledger[name] = {
            "current_charge": 12.0,
            "overt_aim_charge": 2.0,
            "internally_routed_charge": 10.0,
            "trace_intensity": 5.0,
            "primary_channel": "quiet_organizing",
            "felt_register": "contained",
            "ordinary_attribution": "this_can_be_changed_if_we_move_carefully_together",
            "vessel_hint": "collective_practical_friend_group_union_church_or_mutual_aid_vessel",
            "vessel_status": "placeholder_hint_not_full_vessel_model",
            "structural_consideration_gate": "blocked_unknown",
            "latent_structural_pressure": 12.0,
            "overt_aim_charge_semantics": "overt_aim_charge_only_not_total_external_expression",
            "trace_intensity_semantics": "conductance_amplified_effect_strength_not_additional_charge",
        }
    charge_ledger["body_self"].update(
        {
            "current_charge": charge,
            "overt_aim_charge": overt_aim_charge,
            "internally_routed_charge": max(0.0, charge - overt_aim_charge),
            "trace_intensity": trace_intensity,
            "primary_channel": channel,
            "felt_register": "body_noise_hot_edges_irritability_symptom_pressure",
            "ordinary_attribution": "my_body_is_off_or_everything_gets_under_my_skin",
            "vessel_hint": "body_symptom_pain_food_sleep_or_health_anxiety_vessel",
            "structural_consideration_gate": "blocked_unknown",
        }
    )
    return {
        "schema_version": PRESSURE_FLOW_SCHEMA_VERSION,
        "year": 2000,
        "age": 30,
        "event_context": {},
        "charge_ledger": charge_ledger,
        "per_domain_trace_delta": {},
        "trace_delta": {},
        "export_rule": "history_evidence_not_persona_voice",
    }


def _forbidden_key_present(value: object, forbidden: set[str]) -> bool:
    if isinstance(value, dict):
        for key, nested in value.items():
            if key in forbidden:
                return True
            if _forbidden_key_present(nested, forbidden):
                return True
    elif isinstance(value, list):
        for item in value:
            if _forbidden_key_present(item, forbidden):
                return True
    return False


def test_surface_profile_exists_and_matches_required_schema() -> None:
    state = _make_state(channel="quiet_organizing")
    run_pressure_flow_cycle(state, assign_channels=False, compute_pressure=False, apply_gating=False, route_internal_charge=False)

    surface = state.surface_psyche_profile
    assert surface["schema_version"] == "v516_surface_psyche_profile"
    assert surface["export_rule"] == "mediated_surface_only_not_persona_voice_permission"
    assert set(surface["domains"]) == set(DOMAIN_NAMES)

    body = surface["domains"]["body_self"]
    required_keys = {
        "felt_register",
        "ordinary_attribution",
        "attribution_confidence",
        "vessel_hint",
        "vessel_status",
        "insulation_mode",
        "cognitive_shelter",
        "insulation_confidence",
        "insulation_status",
        "avoidance_or_deflection",
        "public_private_inner_posture",
        "historical_relation",
        "dominant_channel",
        "charge_band",
        "overt_aim_band",
        "internally_routed_band",
        "charge_relation_to_prior_history",
    }
    assert required_keys.issubset(body)
    assert not _forbidden_key_present(surface, {
        "analyst_cause",
        "analyst_pressure_account",
        "pressure_flow_history",
        "per_domain_trace_delta",
        "DOMAIN_STRATA_LATENT_PRESSURE_WEIGHTS",
        "raw_strata_pressure",
    })


def test_high_pressure_low_awareness_stays_on_ordinary_attribution() -> None:
    state = _make_state(channel="somatic_irritability")
    state.domains["body_self"].A = 10.0
    state.domains["body_self"].V = 95.0
    state.domains["body_self"].baseline_load = 95.0
    state.domains["body_self"].expressed_aim = 4.0

    run_pressure_flow_cycle(state, assign_channels=False, compute_pressure=False, apply_gating=False, route_internal_charge=False)

    body = state.surface_psyche_profile["domains"]["body_self"]
    assert body["ordinary_attribution"] == "my_body_is_off_or_everything_gets_under_my_skin"
    assert "structural" not in body["ordinary_attribution"]
    assert body["public_private_inner_posture"] == "inner"
    assert body["charge_band"] in {"high", "extreme"}


def test_chronic_groove_maps_to_old_groove_surface_relation() -> None:
    state = _make_state(channel="quiet_organizing", baseline=92.0, expressed=8.0)
    state.pressure_flow_history = [
        _make_history_row(channel="quiet_organizing", charge=88.0, trace_intensity=65.0)
        for _ in range(10)
    ]

    run_pressure_flow_cycle(state, assign_channels=False, compute_pressure=False, apply_gating=False, route_internal_charge=False)

    body = state.surface_psyche_profile["domains"]["body_self"]
    assert body["historical_relation"] == "chronic/old_groove"


def test_route_shift_maps_to_recent_shift_surface_relation() -> None:
    state = _make_state(channel="somatic_irritability", baseline=90.0, expressed=6.0)
    state.pressure_flow_history = [
        _make_history_row(channel="quiet_organizing", charge=82.0, trace_intensity=60.0)
        for _ in range(8)
    ] + [
        _make_history_row(channel="somatic_irritability", charge=84.0, trace_intensity=62.0)
        for _ in range(3)
    ]

    run_pressure_flow_cycle(state, assign_channels=False, compute_pressure=False, apply_gating=False, route_internal_charge=False)

    body = state.surface_psyche_profile["domains"]["body_self"]
    assert body["historical_relation"] == "recent_shift"


def test_missing_pressure_flow_history_yields_empty_degraded_surface_profile() -> None:
    surface = _compact_surface_profile({}, {})

    assert surface["schema_version"] == "v516_surface_psyche_profile"
    assert surface["domains"] == {}
    assert surface["dominant_recent_channels"] == {}
