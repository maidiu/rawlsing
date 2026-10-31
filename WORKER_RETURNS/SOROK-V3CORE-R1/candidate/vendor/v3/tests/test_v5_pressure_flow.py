from __future__ import annotations

import pytest

from v3.core.derived import DerivedIndices
from v3.core.enums import DOMAIN_NAMES
from v3.core.state import BackboneState
from v3.engine.yearly_step import run_one_year
from v3.io.json_codec import state_from_json, state_to_json
from v3.psyche.channels import SUBLIMATION_CHANNELS
from v3.psyche.flow import (
    PressureFlowError,
    _EXPECTED_TRACE_PATH_BY_CHANNEL,
    _derive_current_charge,
    run_pressure_flow_cycle,
)


def _state_for_channel(channel: str, *, baseline: float = 80.0, expressed: float = 10.0) -> BackboneState:
    state = BackboneState(year=2000, age=30)
    for name in DOMAIN_NAMES:
        domain = state.domains[name]
        domain.baseline_load = baseline
        domain.expressed_aim = expressed
        domain.affect_channel = channel
        domain.A = 25.0
        domain.S = 50.0
        domain.V = 70.0
    state.registers.inner_load = 60.0
    state.psychological_capacity.vitality = 55.0
    state.psychological_capacity.aperture = 60.0
    state.psychological_capacity.agency = 55.0
    state.capacity.social_support = 55.0
    return state


def _path_value(state: BackboneState, path: str) -> float:
    obj_name, field_name = path.split(".", 1)
    return float(getattr(getattr(state, obj_name), field_name))


def _empty_step_order() -> dict:
    return {"steps": [], "execution": {"clamp_after_each_step": True}, "derived_indices_schedule": {}}


def test_pressure_flow_records_vital_charge_not_inert_unexpressed_remainder() -> None:
    state = _state_for_channel("caretaking_warmth", baseline=70.0, expressed=12.0)
    snapshot = run_pressure_flow_cycle(state, assign_channels=False, compute_pressure=False, apply_gating=False)

    item = snapshot["charge_ledger"]["family_household"]
    assert item["current_charge"] > 0
    assert item["overt_aim_charge"] == 12.0
    assert item["overt_aim_charge_semantics"] == "overt_aim_charge_only_not_total_external_expression"
    assert item["internally_routed_charge"] > 0
    assert item["trace_intensity"] > 0
    assert item["trace_intensity_semantics"] == "conductance_amplified_effect_strength_not_additional_charge"
    assert "unexpressed" not in str(snapshot).lower()
    assert state.practice_stack.care > 0


@pytest.mark.parametrize("channel", SUBLIMATION_CHANNELS)
def test_every_channel_leaves_expected_trace_path(channel: str) -> None:
    state = _state_for_channel(channel, baseline=85.0, expressed=0.0)
    path = _EXPECTED_TRACE_PATH_BY_CHANNEL[channel]
    before = _path_value(state, path)
    snapshot = run_pressure_flow_cycle(state, assign_channels=False, compute_pressure=False, apply_gating=False)
    after = _path_value(state, path)
    delta = snapshot["trace_delta"]

    assert path in delta
    if channel in {"withdrawal_numbness", "conspiracy_symbolic", "somatic_irritability"}:
        assert after < before
        assert delta[path] < 0
    else:
        assert after > before
        assert delta[path] > 0


def test_per_domain_trace_delta_attributes_domain_current_to_exact_trace_path() -> None:
    state = BackboneState(year=2000, age=30)
    for name in DOMAIN_NAMES:
        state.domains[name].baseline_load = 0.0
        state.domains[name].expressed_aim = 0.0
        state.domains[name].affect_channel = "humor_irony"
    state.domains["family_household"].baseline_load = 80.0
    state.domains["family_household"].affect_channel = "caretaking_warmth"
    state.domains["body_self"].baseline_load = 80.0
    state.domains["body_self"].affect_channel = "somatic_irritability"

    snapshot = run_pressure_flow_cycle(state, assign_channels=False, compute_pressure=False, apply_gating=False)
    per_domain = snapshot["per_domain_trace_delta"]

    assert "practice_stack.care" in per_domain["family_household"]
    assert per_domain["family_household"]["practice_stack.care"] > 0
    assert "capacity.health" not in per_domain["family_household"]
    assert "capacity.health" in per_domain["body_self"]
    assert per_domain["body_self"]["capacity.health"] < 0
    assert "practice_stack.care" not in per_domain["body_self"]


def test_trace_intensity_is_effect_strength_not_conserved_charge() -> None:
    state = _state_for_channel("quiet_organizing", baseline=80.0, expressed=0.0)
    state.pressure_flow_memory = {"grooves": {"family_household": {"quiet_organizing": 100.0}}}
    snapshot = run_pressure_flow_cycle(state, assign_channels=False, compute_pressure=False, apply_gating=False)
    item = snapshot["charge_ledger"]["family_household"]

    assert item["internally_routed_charge"] <= item["current_charge"]
    assert item["channel_conductance"] > 1.0
    assert item["trace_intensity"] > item["internally_routed_charge"]
    assert item["trace_intensity_semantics"] == "conductance_amplified_effect_strength_not_additional_charge"


def test_transactional_failure_after_route_projection_does_not_mutate_live_state(monkeypatch: pytest.MonkeyPatch) -> None:
    import v3.psyche.flow as flow

    state = _state_for_channel("humor_irony", baseline=85.0, expressed=0.0)
    before = state.style_traits.absurdist_humor

    def explode(_history, _previous_memory=None):
        raise RuntimeError("post-route memory boom")

    monkeypatch.setattr(flow, "_update_memory", explode)
    with pytest.raises(PressureFlowError):
        run_pressure_flow_cycle(state, assign_channels=False, compute_pressure=False, apply_gating=False)

    assert state.style_traits.absurdist_humor == before
    assert not state.pressure_flow_history
    assert state.generation_diagnostics[-1]["stage"] == "pressure_flow"


def test_grooves_actively_increase_future_channel_conductance() -> None:
    state = _state_for_channel("quiet_organizing", baseline=70.0, expressed=10.0)
    first = run_pressure_flow_cycle(state, assign_channels=False, compute_pressure=False, apply_gating=False)
    first_conductance = first["charge_ledger"]["family_household"]["channel_conductance"]

    state.year += 1
    state.age += 1
    for name in DOMAIN_NAMES:
        state.domains[name].baseline_load = 70.0
        state.domains[name].expressed_aim = 10.0
        state.domains[name].affect_channel = "quiet_organizing"
    second = run_pressure_flow_cycle(state, assign_channels=False, compute_pressure=False, apply_gating=False)
    second_conductance = second["charge_ledger"]["family_household"]["channel_conductance"]

    assert state.pressure_flow_memory["grooves"]["family_household"]["quiet_organizing"] > 0
    assert second_conductance > first_conductance
    assert second["charge_ledger"]["family_household"]["trace_intensity"] > first["charge_ledger"]["family_household"]["trace_intensity"]


def test_low_vitality_does_not_reduce_current_charge_but_changes_conductance() -> None:
    rested = _state_for_channel("withdrawal_numbness", baseline=75.0, expressed=0.0)
    exhausted = _state_for_channel("withdrawal_numbness", baseline=75.0, expressed=0.0)
    rested.psychological_capacity.vitality = 85.0
    exhausted.psychological_capacity.vitality = 20.0

    rested_charge = _derive_current_charge(rested, "body_self")
    exhausted_charge = _derive_current_charge(exhausted, "body_self")
    rested_snapshot = run_pressure_flow_cycle(rested, assign_channels=False, compute_pressure=False, apply_gating=False)
    exhausted_snapshot = run_pressure_flow_cycle(exhausted, assign_channels=False, compute_pressure=False, apply_gating=False)

    assert exhausted_charge == pytest.approx(rested_charge)
    assert exhausted_snapshot["charge_ledger"]["body_self"]["channel_conductance"] > rested_snapshot["charge_ledger"]["body_self"]["channel_conductance"]


def test_historical_relation_compares_against_prior_not_current_included_average() -> None:
    state = _state_for_channel("aesthetic_intensification", baseline=30.0, expressed=0.0)
    for i in range(3):
        state.year = 2000 + i
        state.age = 20 + i
        for name in DOMAIN_NAMES:
            state.domains[name].baseline_load = 30.0
            state.domains[name].expressed_aim = 0.0
        run_pressure_flow_cycle(state, assign_channels=False, compute_pressure=False, apply_gating=False)

    state.year = 2003
    state.age = 23
    for name in DOMAIN_NAMES:
        state.domains[name].baseline_load = 80.0
        state.domains[name].expressed_aim = 0.0
    run_pressure_flow_cycle(state, assign_channels=False, compute_pressure=False, apply_gating=False)

    assert state.pressure_flow_memory["historical_relation"]["body_self"] == "rising_against_prior_recent_history"
    assert state.surface_psyche_profile["domains"]["body_self"]["charge_relation_to_prior_history"] == "rising_against_prior_recent_history"


def test_event_context_is_compactly_preserved_in_snapshot() -> None:
    state = _state_for_channel("piety_ritual", baseline=60.0, expressed=0.0)
    state.events_this_year = [{"type": "job_loss"}, {"event_type": "family_conflict"}]
    state.micro_trace_this_year = [{"source": "health_drift"}]
    snapshot = run_pressure_flow_cycle(state, assign_channels=False, compute_pressure=False, apply_gating=False)

    assert snapshot["event_context"]["events_this_year_count"] == 2
    assert snapshot["event_context"]["micro_trace_this_year_count"] == 1
    assert snapshot["event_context"]["event_type_counts"]["job_loss"] == 1
    assert snapshot["event_context"]["micro_trace_type_counts"]["health_drift"] == 1


def test_surface_and_analyst_accounts_are_separated_and_non_voice() -> None:
    state = _state_for_channel("piety_ritual", baseline=80.0, expressed=0.0)
    snapshot = run_pressure_flow_cycle(state, assign_channels=False, compute_pressure=False, apply_gating=False)

    assert snapshot["export_rule"] == "history_evidence_not_persona_voice"
    assert state.surface_psyche_profile["export_rule"] == "mediated_surface_only_not_persona_voice_permission"
    assert state.analyst_pressure_account["export_rule"] == "analyst_model_only_do_not_render_as_persona_consciousness"
    assert all(v["voice_export_allowed"] is False for v in state.analyst_pressure_account["domains"].values())
    assert "route_account" not in str(state.surface_psyche_profile)
    assert "vessel_hint" in state.surface_psyche_profile["domains"]["body_self"]
    assert state.surface_psyche_profile["domains"]["body_self"]["vessel_status"] == "placeholder_hint_not_full_vessel_model"


def test_pressure_flow_round_trips_through_json_codec() -> None:
    state = _state_for_channel("humor_irony", baseline=65.0, expressed=5.0)
    run_pressure_flow_cycle(state, assign_channels=False, compute_pressure=False, apply_gating=False)

    loaded = state_from_json(state_to_json(state))
    assert loaded.pressure_flow_history
    assert loaded.pressure_flow_memory["cycles_recorded"] == 1
    assert loaded.surface_psyche_profile["schema_version"] == state.surface_psyche_profile["schema_version"]
    assert loaded.analyst_pressure_account["export_rule"] == "analyst_model_only_do_not_render_as_persona_consciousness"


def test_pressure_flow_failure_records_diagnostic_and_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    import v3.psyche.flow as flow

    state = _state_for_channel("humor_irony")

    def explode(_state: BackboneState) -> dict[str, float]:
        raise RuntimeError("forced trace failure")

    monkeypatch.setattr(flow, "_compact_event_context", explode)
    with pytest.raises(PressureFlowError):
        run_pressure_flow_cycle(state, assign_channels=False, compute_pressure=False, apply_gating=False)

    assert state.generation_diagnostics
    diag = state.generation_diagnostics[-1]
    assert diag["stage"] == "pressure_flow"
    assert diag["exception_type"] == "RuntimeError"
    assert state.yearly_integrity["pressure_flow"]["status"] == "error"


def test_yearly_step_records_pressure_flow_success(monkeypatch: pytest.MonkeyPatch) -> None:
    import v3.psyche.flow as flow

    state = _state_for_channel("humor_irony", baseline=75.0, expressed=0.0)
    monkeypatch.setattr(flow, "compute_baseline_load", lambda s: None)
    monkeypatch.setattr(flow, "apply_expression_gating", lambda s: None)

    run_one_year(state, DerivedIndices(), {"invariants": {"repair_min_counts": False}}, _empty_step_order())

    assert state.pressure_flow_history
    assert state.yearly_integrity["pressure_flow"]["status"] == "clean"


def test_yearly_step_pressure_flow_failure_raise_or_degrade(monkeypatch: pytest.MonkeyPatch) -> None:
    import v3.psyche.flow as flow

    def explode(_state: BackboneState):
        raise flow.PressureFlowError("forced yearly failure")

    monkeypatch.setattr(flow, "run_pressure_flow_cycle", explode)

    state_stop = _state_for_channel("humor_irony")
    with pytest.raises(flow.PressureFlowError):
        run_one_year(state_stop, DerivedIndices(), {"invariants": {"repair_min_counts": False}}, _empty_step_order())
    assert state_stop.yearly_integrity["pressure_flow"]["status"] == "error"

    state_degrade = _state_for_channel("humor_irony")
    run_one_year(
        state_degrade,
        DerivedIndices(),
        {"invariants": {"repair_min_counts": False}, "allow_pressure_flow_failure": True},
        _empty_step_order(),
    )
    assert state_degrade.yearly_integrity["pressure_flow"]["status"] == "error"
