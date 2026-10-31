from __future__ import annotations

from v3.core.state import BackboneState
from v3.psyche.insulation import derive_insulation_profile
from v3.psyche.flow import run_pressure_flow_cycle


def _state(channel: str, *, buffer_type: str = "", spiritual: float = 0.0, organizing: float = 0.0, study: float = 0.0, care: float = 0.0) -> BackboneState:
    state = BackboneState()
    state.practice_stack.spiritual = spiritual
    state.practice_stack.organizing = organizing
    state.practice_stack.study = study
    state.practice_stack.care = care
    state.collective_infrastructure.network_density = organizing
    for domain in state.domains.values():
        domain.affect_channel = channel
        domain.buffer_type = buffer_type
        domain.baseline_load = 88.0
        domain.expressed_aim = 8.0
    return state


def test_piety_ritual_prefers_religious_surrender_over_spiritual_bypass() -> None:
    state = _state("piety_ritual", buffer_type="piety", spiritual=80.0)
    run_pressure_flow_cycle(state, assign_channels=False, compute_pressure=False, apply_gating=False, route_internal_charge=False)
    profile = state.surface_psyche_profile["domains"]["body_self"]

    assert profile["insulation_mode"] == "religious_surrender"
    assert profile["cognitive_shelter"] == "ritual_prayer_surrender"
    assert profile["insulation_confidence"] == "high"


def test_quiet_organizing_gets_collective_holding_high_confidence() -> None:
    state = _state("quiet_organizing", buffer_type="work", organizing=85.0)
    run_pressure_flow_cycle(state, assign_channels=False, compute_pressure=False, apply_gating=False, route_internal_charge=False)
    profile = state.surface_psyche_profile["domains"]["body_self"]

    assert profile["insulation_mode"] == "collective_holding"
    assert profile["cognitive_shelter"] == "mutual_aid_container"
    assert profile["insulation_status"] == "high_confidence"


def test_conspiracy_symbolic_does_not_become_structural_lucidity() -> None:
    state = _state("conspiracy_symbolic", buffer_type="ideology", study=10.0)
    state.psychological_capacity.reality_anchor = 15.0
    run_pressure_flow_cycle(state, assign_channels=False, compute_pressure=False, apply_gating=False, route_internal_charge=False)
    profile = state.surface_psyche_profile["domains"]["body_self"]

    assert profile["insulation_mode"] in {
        "nationalism_or_state_identification",
        "reactionary_displacement",
    }
    assert "structural" not in profile["cognitive_shelter"].lower()


def test_missing_inputs_fallback_to_compartmentalization() -> None:
    state = BackboneState()
    profile = derive_insulation_profile(
        state,
        "body_self",
        {"current_charge": 0.0, "overt_aim_charge": 0.0, "internally_routed_charge": 0.0, "primary_channel": ""},
        {"vessel_hint": "fallback_channel_container"},
        {},
    )

    assert profile["insulation_mode"] == "compartmentalization"
    assert profile["cognitive_shelter"] == "fallback_channel_container"
    assert profile["insulation_confidence"] == "low"
    assert profile["insulation_status"] == "low_confidence_fallback"
