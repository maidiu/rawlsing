from __future__ import annotations

import pytest

from v3.core.enums import DOMAIN_NAMES
from v3.core.state import BackboneState
from v3.psyche.flow import run_pressure_flow_cycle
from v3.psyche.vitality import derive_vitality_profile


def _state_for_vitality(*, age: int, vitality: float, channel: str, baseline: float = 75.0) -> BackboneState:
    state = BackboneState(year=2000, age=age)
    state.psychological_capacity.vitality = vitality
    state.psychological_capacity.aperture = 60.0
    state.psychological_capacity.agency = 55.0
    state.capacity.social_support = 55.0
    state.registers.inner_load = 60.0
    for name in DOMAIN_NAMES:
        domain = state.domains[name]
        domain.baseline_load = baseline
        domain.expressed_aim = 10.0
        domain.affect_channel = channel
        domain.A = 25.0
        domain.S = 50.0
        domain.V = 70.0
    return state


def _charge_ledger(channel: str, current_charge: float = 72.0, routed_charge: float = 24.0) -> dict[str, dict[str, float | str]]:
    return {
        "body_self": {
            "current_charge": current_charge,
            "overt_aim_charge": 10.0,
            "internally_routed_charge": routed_charge,
            "trace_intensity": routed_charge * 0.8,
            "primary_channel": channel,
        }
    }


def test_derive_vitality_profile_tracks_age_phase_and_horizon() -> None:
    young = _state_for_vitality(age=28, vitality=86.0, channel="hyper_competence")
    elder = _state_for_vitality(age=68, vitality=18.0, channel="withdrawal_numbness")

    young_profile = derive_vitality_profile(young, _charge_ledger("hyper_competence"), {})
    elder_profile = derive_vitality_profile(elder, _charge_ledger("withdrawal_numbness"), {})

    assert young_profile["schema_version"] == "v519_vitality_fatigue_age_phase_future_horizon"
    assert young_profile["global"]["age_phase"] == "early_adult"
    assert elder_profile["global"]["age_phase"] == "elder"
    assert elder_profile["global"]["vitality_band"] == "low"
    assert elder_profile["global"]["fatigue_band"] in {"heavy", "severe"}
    assert elder_profile["domains"]["body_self"]["future_horizon_years"] < young_profile["domains"]["body_self"]["future_horizon_years"]
    assert elder_profile["domains"]["body_self"]["recovery_cost"] > young_profile["domains"]["body_self"]["recovery_cost"]


def test_low_vitality_changes_conductance_without_reducing_charge() -> None:
    rested = _state_for_vitality(age=32, vitality=85.0, channel="hyper_competence")
    exhausted = _state_for_vitality(age=32, vitality=18.0, channel="hyper_competence")

    rested_snapshot = run_pressure_flow_cycle(rested, assign_channels=False, compute_pressure=False, apply_gating=False)
    exhausted_snapshot = run_pressure_flow_cycle(exhausted, assign_channels=False, compute_pressure=False, apply_gating=False)

    assert exhausted_snapshot["charge_ledger"]["body_self"]["current_charge"] == pytest.approx(
        rested_snapshot["charge_ledger"]["body_self"]["current_charge"]
    )
    assert exhausted_snapshot["charge_ledger"]["body_self"]["channel_conductance"] < rested_snapshot["charge_ledger"]["body_self"]["channel_conductance"]
    assert exhausted_snapshot["charge_ledger"]["body_self"]["future_horizon_years"] < rested_snapshot["charge_ledger"]["body_self"]["future_horizon_years"]
    assert exhausted_snapshot["charge_ledger"]["body_self"]["recovery_cost"] > rested_snapshot["charge_ledger"]["body_self"]["recovery_cost"]


def test_vitality_profile_persists_into_pressure_flow_memory_and_surface() -> None:
    state = _state_for_vitality(age=68, vitality=18.0, channel="withdrawal_numbness")
    snapshot = run_pressure_flow_cycle(state, assign_channels=False, compute_pressure=False, apply_gating=False)

    assert "vitality_profile" in snapshot
    assert state.pressure_flow_memory["vitality_profile"]["global"]["age_phase"] == "elder"
    assert state.pressure_flow_memory["vitality_profile"]["domains"]["body_self"]["routing_bias"] == "somatic_or_withdrawal"
    assert state.surface_psyche_profile["vitality_profile"]["global"]["future_horizon_years"] == snapshot["vitality_profile"]["global"]["future_horizon_years"]
    assert state.surface_psyche_profile["domains"]["body_self"]["age_phase"] == "elder"
    assert state.surface_psyche_profile["domains"]["body_self"]["routing_bias"] == "somatic_or_withdrawal"

