from __future__ import annotations

from conftest import (
    access,
    binding,
    event,
    projection,
    response,
    snapshot,
    year_input,
)
from v3core_adapter.contracts import ClockDomain, Status
from v3core_adapter.derived_scope import material_capacity_index
from v3core_adapter.scheduler import run_year


def _assert_held(proj, request, status: Status) -> None:
    before = proj.state_hash()
    before_index = material_capacity_index(proj.state)
    result = run_year(proj, request)
    assert result.status == status, (result.status, result.reason)
    assert result.committed is False
    assert proj.state_hash() == before
    assert material_capacity_index(proj.state) == before_index


def test_foreign_actor_is_held_without_mutation() -> None:
    proj = projection(actor="B")
    request = year_input(
        events=(event(actor="A"),),
        accesses=(access(actor="A"),),
        responses=(response(actor="A"),),
        bindings=(binding(),),
        prior=snapshot(actor="A"),
    )
    _assert_held(proj, request, Status.HELD_FOREIGN_ACTOR)


def test_sorok_n11_clock_is_not_an_m25_year_event() -> None:
    proj = projection()
    domain = ClockDomain.SOROK_NEO_N11_EVENT
    request = year_input(
        events=(event(clock_domain=domain),),
        accesses=(access(clock_domain=domain),),
        responses=(response(clock_domain=domain),),
        bindings=(binding(),),
    )
    _assert_held(proj, request, Status.HELD_CLOCK_MISMATCH)


def test_pyat_n11_objective_world_clock_is_not_an_m25_year_event() -> None:
    proj = projection()
    domain = ClockDomain.PYAT_N11_OBJECTIVE_WORLD
    request = year_input(
        events=(event(clock_domain=domain),),
        accesses=(access(clock_domain=domain),),
        responses=(response(clock_domain=domain),),
        bindings=(binding(),),
    )
    _assert_held(proj, request, Status.HELD_CLOCK_MISMATCH)


def test_missing_actor_perception_is_held() -> None:
    proj = projection()
    request = year_input(accesses=())
    _assert_held(proj, request, Status.HELD_MISSING_PERCEPTION)


def test_missing_actor_response_is_held() -> None:
    proj = projection()
    request = year_input(responses=())
    _assert_held(proj, request, Status.HELD_MISSING_RESPONSE)


def test_missing_transition_rule_is_held_and_distinct_from_no_change() -> None:
    proj = projection()
    request = year_input(
        events=(event(kind="SPEECH"),),
        responses=(response(kind="PERFORMED_SPEECH"),),
    )
    _assert_held(proj, request, Status.HELD_MISSING_RULE)


def test_unissued_scientific_rule_is_held() -> None:
    proj = projection()
    request = year_input(
        events=(event(kind="SCIENTIFIC_PENDING_EVENT"),),
        responses=(response(kind="SCIENTIFIC_PENDING_RESPONSE"),),
    )
    _assert_held(proj, request, Status.HELD_RULE_NOT_ISSUED)


def test_evaluated_test_only_zero_is_no_change_not_missing_rule() -> None:
    proj = projection()
    before_index = material_capacity_index(proj.state)
    request = year_input(
        events=(event(kind="TEST_ONLY_ZERO_EVENT"),),
        responses=(response(kind="TEST_ONLY_ZERO_RESPONSE"),),
    )
    result = run_year(proj, request)
    assert result.status == Status.NO_CHANGE_EVALUATED
    assert result.committed is True
    assert result.dispositions[0].status == Status.NO_CHANGE_EVALUATED
    assert result.dispositions[0].reason == "rule_evaluated_zero_delta"
    assert result.year_record.material_deltas == ()
    assert material_capacity_index(proj.state) == before_index
    assert proj.state.capacity.money == 54.0
    assert [item["event_id"] for item in proj.state.events_this_year] == ["EV_MARKET_WORK"]


def test_source_event_removal_cannot_become_an_annual_occurrence() -> None:
    proj = projection()
    request = year_input(
        events=(),
        accesses=(),
        responses=(),
        bindings=(binding("EV_WITHDRAWN"),),
    )
    _assert_held(proj, request, Status.HELD_SOURCE_EVENT_WITHDRAWN)


def test_empty_year_without_source_event_is_held() -> None:
    proj = projection()
    request = year_input(events=(), accesses=(), responses=(), bindings=())
    _assert_held(proj, request, Status.HELD_NO_EVENT_SOURCE)


def test_wrong_annual_binding_is_held() -> None:
    proj = projection()
    request = year_input(bindings=(binding(annual_year=2),))
    _assert_held(proj, request, Status.HELD_CLOCK_BINDING_MISMATCH)


def test_duplicate_event_is_not_reapplied() -> None:
    proj = projection()
    first = run_year(proj, year_input())
    assert first.committed is True
    before = proj.state_hash()
    second = run_year(
        proj,
        year_input(
            annual_year=2,
            bindings=(binding(annual_year=2),),
        ),
    )
    assert second.status == Status.HELD_DUPLICATE_EVENT
    assert second.committed is False
    assert proj.state_hash() == before


def test_unowned_event_is_held_as_accounting_mismatch() -> None:
    proj = projection()
    request = year_input(events=(event(source_owned=False),))
    _assert_held(proj, request, Status.HELD_ACCOUNTING_MISMATCH)
