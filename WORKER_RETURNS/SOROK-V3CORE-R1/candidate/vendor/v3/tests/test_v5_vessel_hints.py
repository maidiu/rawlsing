from __future__ import annotations

from v3.core.state import BackboneState
from v3.psyche.vessels import derive_attribution_and_vessel_hint
from v3.psyche.flow import run_pressure_flow_cycle


def _run_state(channel: str, *, spiritual: float = 0.0, organizing: float = 0.0, study: float = 0.0, care: float = 0.0, health: float = 50.0) -> BackboneState:
    state = BackboneState()
    state.practice_stack.spiritual = spiritual
    state.practice_stack.organizing = organizing
    state.practice_stack.study = study
    state.practice_stack.care = care
    state.capacity.health = health
    for domain in state.domains.values():
        domain.affect_channel = channel
        domain.baseline_load = 88.0
        domain.expressed_aim = 8.0
    return state


def test_piety_ritual_gets_ritual_vessel_without_analyst_explanation() -> None:
    state = _run_state("piety_ritual", spiritual=85.0)
    run_pressure_flow_cycle(state, assign_channels=False, compute_pressure=False, apply_gating=False, route_internal_charge=False)
    body = state.surface_psyche_profile["domains"]["body_self"]
    helper = derive_attribution_and_vessel_hint(
        state,
        "body_self",
        "piety_ritual",
        {"current_charge": 88.0, "overt_aim_charge": 8.0, "internally_routed_charge": 80.0},
        state.pressure_flow_memory,
    )

    assert body["vessel_hint"] == "ritual_prayer_surrender"
    assert body["attribution_confidence"] == "high"
    assert "analyst" not in body["ordinary_attribution"].lower()
    assert helper["vessel_status"] == "high_confidence"


def test_quiet_organizing_gets_collective_container_high_confidence() -> None:
    state = _run_state("quiet_organizing", organizing=80.0)
    state.collective_infrastructure.network_density = 80.0
    run_pressure_flow_cycle(state, assign_channels=False, compute_pressure=False, apply_gating=False, route_internal_charge=False)
    body = state.surface_psyche_profile["domains"]["body_self"]
    helper = derive_attribution_and_vessel_hint(
        state,
        "body_self",
        "quiet_organizing",
        {"current_charge": 88.0, "overt_aim_charge": 8.0, "internally_routed_charge": 80.0},
        state.pressure_flow_memory,
    )

    assert body["vessel_hint"] == "collective_practical_container"
    assert body["attribution_confidence"] == "high"
    assert helper["vessel_status"] == "high_confidence"


def test_conspiracy_symbolic_does_not_become_structural_lucidity() -> None:
    state = _run_state("conspiracy_symbolic", study=10.0)
    state.psychological_capacity.reality_anchor = 20.0
    run_pressure_flow_cycle(state, assign_channels=False, compute_pressure=False, apply_gating=False, route_internal_charge=False)
    body = state.surface_psyche_profile["domains"]["body_self"]
    helper = derive_attribution_and_vessel_hint(
        state,
        "body_self",
        "conspiracy_symbolic",
        {"current_charge": 88.0, "overt_aim_charge": 8.0, "internally_routed_charge": 80.0},
        state.pressure_flow_memory,
    )

    assert body["vessel_hint"] == "online_enemy_pattern_container"
    assert body["attribution_confidence"] in {"low", "medium"}
    assert "structural" not in body["ordinary_attribution"].lower()
    assert helper["vessel_hint"] == "online_enemy_pattern_container"


def test_missing_inputs_produce_low_confidence_fallback() -> None:
    state = BackboneState()
    charge_item = {
        "current_charge": 0.0,
        "overt_aim_charge": 0.0,
        "internally_routed_charge": 0.0,
    }

    derived = derive_attribution_and_vessel_hint(state, "body_self", "", charge_item, {})

    assert derived["vessel_hint"] == "fallback_channel_container"
    assert derived["ordinary_attribution"] == "i_do_not_have_a_clear_read_yet"
    assert derived["attribution_confidence"] == "low"
    assert derived["vessel_status"] == "low_confidence_fallback"
