from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
for path in (str(ROOT), str(ROOT / "vendor"), str(ROOT / "vendor" / "py3deps")):
    if path not in sys.path:
        sys.path.insert(0, path)

from v3core_adapter.contracts import (  # noqa: E402
    ActorAccess,
    ActorResponse,
    ActorWorldEvent,
    AnnualBinding,
    ClockDomain,
    Provenance,
    SourceActorSnapshot,
    YearInput,
)
from v3core_adapter.ledger import HistoricalProjection  # noqa: E402
from v3core_adapter.quarantine import build_projection_state  # noqa: E402
from v3core_adapter.scheduler import run_year  # noqa: E402
from v3core_adapter.transitions import default_registry  # noqa: E402

WORLD_ID = "TEST_ONLY_WORLD_V3CORE"


def prov(record_id: str = "RECORD") -> Provenance:
    return Provenance(
        source_system="V3CORE_TEST_FIXTURE",
        source_ref="SOROK-V3CORE-R1-TESTS",
        source_commit="750548ddbb9b4392a16ce93097b856f349e16182",
        source_branch="agent/sorok-v3core-r1-sourcefree-activity-time-adapter-20261030",
        source_path="tests/conftest.py",
        source_sha256="0" * 64,
        source_record_id=record_id,
        captured_by="V3CORE_TEST",
        captured_at="2026-10-30",
        native=False,
        authority="TEST_ONLY_SOURCEFREE",
    )


def snapshot(
    *,
    actor: str = "B",
    clock: int = 10,
    cash: float = 54.0,
    position: str = "workshop",
    material_remaining: float = 0.0,
    free_hours: float = 13.0,
    completed_units: float = 3.0,
    skill: float = 6.0,
    debt_units: float = 2.0,
    tools_remaining: float = 1.0,
) -> SourceActorSnapshot:
    return SourceActorSnapshot(
        actor_id=actor,
        world_id=WORLD_ID,
        source_clock_domain=ClockDomain.CURRENT_C12_ACTOR_WORLD,
        source_clock=clock,
        position=position,
        cash=cash,
        material_remaining=material_remaining,
        free_hours=free_hours,
        completed_units=completed_units,
        skill=skill,
        debt_units=debt_units,
        tools_remaining=tools_remaining,
        projects=("communal_irrigation_pump_repair",),
        provenance=prov("SNAPSHOT_" + actor),
    )


def post_snapshot(**kwargs) -> SourceActorSnapshot:
    defaults = {
        "clock": 40,
        "cash": 56.0,
        "position": "market",
        "completed_units": 4.0,
    }
    defaults.update(kwargs)
    return snapshot(**defaults)


def event(
    *,
    event_id: str = "EV_MARKET_WORK",
    actor: str = "B",
    kind: str = "OFFSCREEN_REPAIR",
    clock: int = 40,
    clock_domain: ClockDomain = ClockDomain.CURRENT_C12_ACTOR_WORLD,
    body: dict | None = None,
    source_owned: bool = True,
) -> ActorWorldEvent:
    return ActorWorldEvent(
        event_id=event_id,
        actor_id=actor,
        world_id=WORLD_ID,
        kind=kind,
        location="market",
        source_clock_domain=clock_domain,
        source_clock=clock,
        body=body
        if body is not None
        else {
            "cash_delta": 2,
            "completed_delta": 1,
            "material_delta": -1,
            "source_owned": True,
            "tool_used": True,
        },
        provenance=prov(event_id),
        owner_receipt_hash="a" * 64,
        source_owned=source_owned,
    )


def access(
    event_id: str = "EV_MARKET_WORK",
    *,
    actor: str = "B",
    clock: int = 40,
    clock_domain: ClockDomain = ClockDomain.CURRENT_C12_ACTOR_WORLD,
    perceived: bool = True,
    channel: str = "own_action",
) -> ActorAccess:
    return ActorAccess(
        event_id=event_id,
        actor_id=actor,
        channel=channel,
        perceived=perceived,
        source_clock_domain=clock_domain,
        source_clock=clock,
        provenance=prov(event_id + ":access"),
    )


def response(
    event_id: str = "EV_MARKET_WORK",
    *,
    actor: str = "B",
    kind: str = "PERFORMED_OFFSCREEN_WORK",
    clock: int = 40,
    clock_domain: ClockDomain = ClockDomain.CURRENT_C12_ACTOR_WORLD,
    performed: bool = True,
) -> ActorResponse:
    return ActorResponse(
        event_id=event_id,
        actor_id=actor,
        kind=kind,
        performed=performed,
        body={"source_owned": True, "performed": performed},
        source_clock_domain=clock_domain,
        source_clock=clock,
        provenance=prov(event_id + ":response"),
    )


def binding(
    event_id: str = "EV_MARKET_WORK",
    *,
    annual_year: int = 1,
    schedule_clock_domain: ClockDomain = ClockDomain.V3_M25_ANNUAL,
) -> AnnualBinding:
    return AnnualBinding(
        event_id=event_id,
        schedule_clock_domain=schedule_clock_domain,
        annual_year=annual_year,
        bound_by="TEST",
        provenance=prov(event_id + ":binding"),
    )


def year_input(
    *,
    annual_year: int = 1,
    events=None,
    accesses=None,
    responses=None,
    bindings=None,
    allow_empty_year: bool = False,
    age: int | None = None,
    prior=None,
    post=None,
) -> YearInput:
    return YearInput(
        annual_year=annual_year,
        schedule_clock_domain=ClockDomain.V3_M25_ANNUAL,
        events=tuple(events if events is not None else (event(),)),
        accesses=tuple(accesses if accesses is not None else (access(),)),
        responses=tuple(responses if responses is not None else (response(),)),
        bindings=tuple(bindings if bindings is not None else (binding(),)),
        allow_empty_year=allow_empty_year,
        age=age,
        prior_snapshot=prior if prior is not None else snapshot(),
        post_snapshot=post if post is not None else post_snapshot(),
    )


def projection(*, actor: str = "B", prior: SourceActorSnapshot | None = None) -> HistoricalProjection:
    prior = prior or snapshot(actor=actor)
    return HistoricalProjection(
        projection_id="TEST_PROJECTION",
        actor_id=actor,
        world_id=WORLD_ID,
        state=build_projection_state(annual_year=1, age=None, snapshot=prior),
        prior_snapshot=prior,
    )


def apply_default(proj: HistoricalProjection, request: YearInput | None = None, **kwargs):
    request = request or year_input(prior=proj.prior_snapshot, post=post_snapshot())
    return run_year(proj, request, **kwargs)


@pytest.fixture()
def registry():
    return default_registry()
