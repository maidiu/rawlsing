from __future__ import annotations

from conftest import event, projection, year_input

from v3core_adapter.contracts import ANNUAL_STEP_IDS, Status
from v3core_adapter.scheduler import run_year


def test_year_record_separates_source_facts_state_derived_and_expression() -> None:
    proj = projection()
    result = run_year(proj, year_input(prior=proj.prior_snapshot))
    assert result.committed is True
    record = result.year_record
    assert record is not None
    assert record.schema == "SOROK_V3CORE_R1_YEAR_RECORD@1"
    assert record.annual_year == 1
    assert record.schedule_clock_domain.value == "V3_M25_ANNUAL_SCHEDULE"
    assert record.source_event_ids == ("EV_MARKET_WORK",)
    assert record.authority == "TEST_ONLY_SOURCEFREE_NO_SCIENCE_ISSUANCE"
    assert record.canonical_c9_claimed is False
    assert len(record.derived_diagnostic_hash) == 64
    assert record.state_before_hash != record.state_after_hash
    assert record.published_material_index_before == 11.3
    assert record.published_material_index_after == 11.6
    assert len(record.material_deltas) == 1
    assert record.material_deltas[0].before == 54.0
    assert record.material_deltas[0].delta == 2.0
    assert record.material_deltas[0].after == 56.0
    assert record.event_dispositions[0].status == Status.APPLIED_TEST_ONLY_SOURCEFREE
    assert record.event_dispositions[0].durable_mutation is True
    assert record.generation_status == "degraded"
    assert record.readiness == "DEGRADED_READY_TEST_ONLY"
    assert proj.state.metabolic_style == {}
    assert proj.state.registers.public_expression_gate == 0


def test_all_nineteen_steps_have_typed_outcomes() -> None:
    proj = projection()
    result = run_year(proj, year_input(prior=proj.prior_snapshot))
    outcomes = {item.step_id: item for item in result.step_outcomes}
    for step_id in ANNUAL_STEP_IDS:
        assert step_id in outcomes
    assert outcomes["event_sampling"].status == Status.APPLIED_TEST_ONLY_SOURCEFREE
    assert outcomes["event_sampling"].details["sampled"] is False
    assert outcomes["capacity_update"].status == Status.APPLIED_TEST_ONLY_SOURCEFREE
    assert outcomes["render_layer"].status == Status.DERIVED_EVALUATED_SCOPED
    assert outcomes["post_year_pressure_flow"].status == Status.HELD_CONSERVED_CHARGE_MODEL
    held = [
        step_id
        for step_id in ANNUAL_STEP_IDS
        if step_id not in {"event_sampling", "capacity_update", "render_layer"}
    ]
    for step_id in held:
        assert outcomes[step_id].status == Status.HELD_MISSING_ISSUED_RULE
        assert outcomes[step_id].details["admitted"] is False


def test_age_is_only_advanced_when_supplied() -> None:
    proj = projection()
    result = run_year(proj, year_input(prior=proj.prior_snapshot, age=30))
    assert result.committed is True
    assert result.year_record.age == 30
    assert proj.state.age == 31


def test_actual_event_is_not_sampled_or_duplicated() -> None:
    proj = projection()
    result = run_year(proj, year_input(prior=proj.prior_snapshot))
    assert result.committed is True
    assert [item["event_id"] for item in proj.state.events_this_year] == ["EV_MARKET_WORK"]
    assert proj.state.events_this_year[0]["body"]["cash_delta"] == 2
    assert proj.state.micro_trace_this_year[0]["field"] == "capacity.money"
    assert proj.state.yearly_integrity["material_accounting"]["status"] == "clean"
    assert result.year_record.source_event_ids == ("EV_MARKET_WORK",)
