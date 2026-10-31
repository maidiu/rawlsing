"""First current consumer: historical material projection over I1's actual event.

The adapter reads one actual B offscreen market-work event from the I1 guarded
joined product. It never writes to I1's C12 database and never creates a rival
C9 actor store.
"""

from __future__ import annotations

import hashlib
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .contracts import (
    ActorAccess,
    ActorResponse,
    ActorWorldEvent,
    AnnualBinding,
    ClockDomain,
    Provenance,
    SourceActorSnapshot,
    Status,
    YearInput,
    YearRecord,
    YearResult,
)
from .ledger import HistoricalProjection
from .quarantine import build_projection_state
from .scheduler import run_year

I1_COMMIT = "7d44e30064f8e873e1a3ff9cb05fe75456756b88"
I1_BRANCH = "agent/sorok-i1-sourcefree-continuing-person-joined-implementation-20261030-r1"
I1_RETURN = "WORKER_RETURNS/SOROK-I1-CONTINUING-PERSON-R1"
I1_ROOT = Path(__file__).resolve().parent.parent / "vendor" / "i1"
WORLD_REF = "I1_GUARDED_JOINED_PRODUCT_WORLD"


class I1ConsumerRefusal(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code
        self.detail = detail


@dataclass(frozen=True)
class ActualI1Event:
    event: ActorWorldEvent
    access: ActorAccess
    response: ActorResponse
    prior: SourceActorSnapshot
    post: SourceActorSnapshot
    c12_verify_before: dict[str, Any]
    c12_verify_after: dict[str, Any]
    observed_world_hash: str = ""


@dataclass(frozen=True)
class I1ProjectionResult:
    status: Status
    event_id: str
    source_clock: int
    source_clock_domain: ClockDomain
    material_index_before: float
    material_index_after: float
    material_index_delta: float
    cash_before: float
    cash_after: float
    completed_units_before: float
    completed_units_after: float
    position_before: str
    position_after: str
    state_hash_before: str
    state_hash_after: str
    year_record: YearRecord | None
    year_result: YearResult
    c12_verify_before: dict[str, Any]
    c12_verify_after: dict[str, Any]
    observed_world_hash: str = ""
    canonical_c9_claimed: bool = False
    rival_store_created: bool = False
    authority: str = "TEST_ONLY_SOURCEFREE_NOT_NATIVE_NOT_SCIENCE"


def _install_i1() -> None:
    if str(I1_ROOT) not in sys.path:
        sys.path.insert(0, str(I1_ROOT))
    import bp2p4

    bp2p4.install()


def _i1_source_sha256() -> str:
    path = I1_ROOT / "bp2p4" / "i1_product.py"
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _provenance(source_record_id: str) -> Provenance:
    return Provenance(
        source_system="I1_GUARDED_JOINED_PRODUCT",
        source_ref="SOROK-I1-CONTINUING-PERSON-R1",
        source_commit=I1_COMMIT,
        source_branch=I1_BRANCH,
        source_path=f"{I1_RETURN}/candidate/bp2p4/i1_product.py",
        source_sha256=_i1_source_sha256(),
        source_record_id=source_record_id,
        captured_by="SOROK-V3CORE-R1",
        captured_at="2026-10-30",
        native=False,
        authority="TEST_ONLY_SOURCEFREE",
    )


def _world_id(product: Any) -> str:
    state = product.store.latest_state(product.branch_id)
    return str((state.get("world") or {}).get("hash") or "WORLD_HASH_ABSENT")


def _snapshot(
    product: Any,
    material: dict[str, Any],
    actor_state: dict[str, Any],
    *,
    clock: int,
    source_record_id: str,
) -> SourceActorSnapshot:
    state = material["state"]
    return SourceActorSnapshot(
        actor_id="B",
        world_id=WORLD_REF,
        source_clock_domain=ClockDomain.CURRENT_C12_ACTOR_WORLD,
        source_clock=int(clock),
        position=str(state.get("position") or ""),
        cash=float(state.get("cash") or 0.0),
        material_remaining=float(state.get("material_remaining") or 0.0),
        free_hours=float(state.get("free_hours") or 0.0),
        completed_units=float(state.get("completed_units") or 0.0),
        skill=float(actor_state.get("skill") or 0.0),
        debt_units=float(actor_state.get("debt_units") or 0.0),
        tools_remaining=float(actor_state.get("tools_remaining") or 0.0),
        projects=tuple(str(x) for x in (actor_state.get("projects") or [])),
        provenance=_provenance(source_record_id),
    )


def capture_actual_event(product: Any, *, hours: int = 30) -> ActualI1Event:
    """Drive one actual I1 offscreen event and read its exact source records."""
    before = product.owner_material_readout("B")
    before_clock = int(product.store.last_clock(product.branch_id))
    before_actor_state = dict(
        product.store.latest_state(product.branch_id)["actors"]["B"]["state"]
    )
    product.wait(hours)
    after = product.owner_material_readout("B")
    after_clock = int(product.store.last_clock(product.branch_id))
    after_actor_state = dict(
        product.store.latest_state(product.branch_id)["actors"]["B"]["state"]
    )
    latest = after.get("latest_work_event")
    if not latest or latest.get("kind") != "OFFSCREEN_REPAIR":
        raise I1ConsumerRefusal("I1_ACTUAL_OFFSCREEN_EVENT_ABSENT")
    event_id = str(latest["event_id"])
    perceptions = [
        row for row in product.store.perceptions(product.branch_id, "B")
        if row.get("event_id") == event_id
    ]
    if not perceptions:
        raise I1ConsumerRefusal("I1_ACTUAL_PERCEPTION_ABSENT", event_id)
    perception = perceptions[-1]
    episodes = [
        row for row in product.store.episodes(product.branch_id)
        if row.get("actor_id") == "B"
        and row.get("kind") == "OFFSCREEN"
        and (row.get("body") or {}).get("event_id") == event_id
    ]
    if not episodes:
        raise I1ConsumerRefusal("I1_ACTUAL_RESPONSE_ABSENT", event_id)
    response_record = episodes[-1]
    observed_world_hash = _world_id(product)
    prior = _snapshot(
        product,
        before,
        before_actor_state,
        clock=before_clock,
        source_record_id="I1_BEFORE_" + event_id,
    )
    post = _snapshot(
        product,
        after,
        after_actor_state,
        clock=after_clock,
        source_record_id="I1_AFTER_" + event_id,
    )
    event = ActorWorldEvent(
        event_id=event_id,
        actor_id="B",
        world_id=WORLD_REF,
        kind=str(latest["kind"]),
        location=str(latest["location"]),
        source_clock_domain=ClockDomain.CURRENT_C12_ACTOR_WORLD,
        source_clock=int(latest["clock"]),
        body=dict(latest.get("body") or {}),
        provenance=_provenance(event_id),
        owner_receipt_hash=(
            response_record.get("body", {}).get("owner_receipt")
            if isinstance(response_record.get("body"), dict) else None
        ),
        source_owned=bool((latest.get("body") or {}).get("source_owned")),
    )
    access = ActorAccess(
        event_id=event_id,
        actor_id="B",
        channel=str(perception.get("channel") or ""),
        perceived=True,
        source_clock_domain=ClockDomain.CURRENT_C12_ACTOR_WORLD,
        source_clock=int(perception.get("clock") or 0),
        provenance=_provenance(event_id + ":perception"),
    )
    response = ActorResponse(
        event_id=event_id,
        actor_id="B",
        kind="PERFORMED_OFFSCREEN_WORK",
        performed=bool((latest.get("body") or {}).get("source_owned")),
        body=dict(response_record.get("body") or {}),
        source_clock_domain=ClockDomain.CURRENT_C12_ACTOR_WORLD,
        source_clock=int(response_record.get("clock") or 0),
        provenance=_provenance(event_id + ":response"),
    )
    c12_before = product.verify_c12()
    if not c12_before.get("ok"):
        raise I1ConsumerRefusal("I1_C12_NOT_VERIFIED_BEFORE_PROJECTION")
    return ActualI1Event(
        event=event,
        access=access,
        response=response,
        prior=prior,
        post=post,
        c12_verify_before=c12_before,
        c12_verify_after=c12_before,
        observed_world_hash=observed_world_hash,
    )


def project_actual_market_event(
    root: str | Path,
    *,
    projection_path: str | Path | None = None,
    hours: int = 30,
) -> I1ProjectionResult:
    """Consume I1's actual event through the historical M25 projection."""
    _install_i1()
    from bp2p4.i1_product import GuardedJoinedProduct
    from bp2p4.reunion import build_fresh

    root = Path(root)
    product = GuardedJoinedProduct(root, artifacts=build_fresh(root))
    try:
        actual = capture_actual_event(product, hours=hours)
        binding = AnnualBinding(
            event_id=actual.event.event_id,
            schedule_clock_domain=ClockDomain.V3_M25_ANNUAL,
            annual_year=1,
            bound_by="I1_V3CORE_R1_ADAPTER",
            provenance=_provenance(actual.event.event_id + ":annual_binding"),
        )
        year_input = YearInput(
            annual_year=1,
            schedule_clock_domain=ClockDomain.V3_M25_ANNUAL,
            events=(actual.event,),
            accesses=(actual.access,),
            responses=(actual.response,),
            bindings=(binding,),
            allow_empty_year=False,
            age=None,
            prior_snapshot=actual.prior,
            post_snapshot=actual.post,
        )
        projection = HistoricalProjection(
            projection_id="I1_B_ACTUAL_OFFSCREEN_MARKET_WORK",
            actor_id="B",
            world_id=WORLD_REF,
            state=build_projection_state(
                annual_year=1,
                age=None,
                snapshot=actual.prior,
            ),
            prior_snapshot=actual.prior,
        )
        projection.add_source(actual.event, actual.access, actual.response)
        projection.source_metadata = {
            "observed_world_hash": actual.observed_world_hash,
            "event_id": actual.event.event_id,
            "c12_verify_before": actual.c12_verify_before,
        }
        result = run_year(
            projection,
            year_input,
            ledger_path=projection_path,
        )
        c12_after = product.verify_c12()
        if not c12_after.get("ok"):
            raise I1ConsumerRefusal("I1_C12_NOT_VERIFIED_AFTER_PROJECTION")
        if c12_after.get("counts") != actual.c12_verify_before.get("counts"):
            raise I1ConsumerRefusal("I1_C12_COUNTS_CHANGED_BY_PROJECTION")
        if projection_path is not None and Path(projection_path).resolve() == (root / "c12.sqlite").resolve():
            raise I1ConsumerRefusal("PROJECTION_PATH_COLLIDES_WITH_C12")
        delta = round(result.material_index_after - result.material_index_before, 6)
        return I1ProjectionResult(
            status=result.status,
            event_id=actual.event.event_id,
            source_clock=actual.event.source_clock,
            source_clock_domain=actual.event.source_clock_domain,
            material_index_before=result.material_index_before,
            material_index_after=result.material_index_after,
            material_index_delta=delta,
            cash_before=actual.prior.cash,
            cash_after=actual.post.cash,
            completed_units_before=actual.prior.completed_units,
            completed_units_after=actual.post.completed_units,
            position_before=actual.prior.position,
            position_after=actual.post.position,
            state_hash_before=result.state_before_hash,
            state_hash_after=result.state_after_hash,
            year_record=result.year_record,
            year_result=result,
            c12_verify_before=actual.c12_verify_before,
            c12_verify_after=c12_after,
            observed_world_hash=actual.observed_world_hash,
            canonical_c9_claimed=False,
            rival_store_created=False,
        )
    finally:
        product.close()
