from __future__ import annotations

from v3.core.state import BackboneState
from v3.io.calibration_from_identity import apply_calibration_to_state
from v3.psyche.flow import run_pressure_flow_cycle
from v3.systems.relational_field import apply_relational_field_to_state


def _make_state(with_relational_field: bool) -> BackboneState:
    state = BackboneState(year=2026, age=29)
    identity = {
        "country_code": "US",
        "region": "Northeast",
        "class_origin": "working",
        "current_class": "middle",
        "urbanicity": "city",
        "minority_status": "dominant",
    }
    apply_calibration_to_state(state, identity)
    if with_relational_field:
        apply_relational_field_to_state(
            state,
            {
                "status": "ok",
                "source": "validated_9_plus_absolute",
                "projection": {
                    "channels": ["formal_legibility", "boundary_pressure"],
                    "notes": ["mediated into conductance only"],
                },
                "absolute_horizon": {
                    "status": "internal_only",
                    "surface_export_allowed": False,
                    "surface_label_allowed": False,
                },
                "notes": ["no surface leak"],
            },
        )
    return state


def test_v5_pressureflow_mediates_relation_state_without_surface_leak() -> None:
    baseline_state = _make_state(with_relational_field=False)
    relational_state = _make_state(with_relational_field=True)

    run_pressure_flow_cycle(baseline_state, route_internal_charge=False)
    run_pressure_flow_cycle(relational_state, route_internal_charge=False)

    baseline_conductance = baseline_state.analyst_pressure_account["domains"]["family_household"]["channel_conductance"]
    relational_conductance = relational_state.analyst_pressure_account["domains"]["family_household"]["channel_conductance"]

    assert relational_conductance > baseline_conductance
    assert relational_state.yearly_integrity["pressure_flow"]["status"] == "clean"
    assert "relational_field" not in relational_state.surface_psyche_profile
    assert "absolute_horizon" not in relational_state.surface_psyche_profile
    assert relational_state.yearly_integrity["pressure_flow"]["cycle_recorded"] is True
