"""B05 bounded rolling material reproduction over B02 periods and B04 stock.

The household rent is a real obligation on the B01 fixed-A household cash, not
the registered parent's cash. Parent work remains C02 parent-local activity.
No elapsed-time psychology, second ledger, scheduler or public event is created.
"""
from __future__ import annotations

from contextlib import contextmanager
import fcntl
from pathlib import Path
from typing import Any, Mapping

from developmental_recursion.contracts import (
    RealizedEvent, RecursionRefusal, StateIdentity, detached, digest,
)
from developmental_recursion.parent_activity import _StoreWrite

try:
    import house as p6_house
except ImportError:  # pragma: no cover
    p6_house = None

try:
    import historical_period as hp
except ImportError:  # pragma: no cover
    hp = None

RENT_KIND = "P2_HOUSEHOLD_RENT"
RENT_RECEIPT_SCHEMA = "SOROK_HOUSEHOLD_RENT_RECEIPT@1"
HOUSEHOLD_OBLIGATION_SCHEMA = "SOROK_HOUSEHOLD_OBLIGATION_READ@1"
GRADE = "SOURCEFREE_S2_ONLY"
READ_BOUNDARY = {
    "psyche_store": "NOT_READ",
    "psychology_state": "NOT_WRITTEN",
    "class_to_trait": "NOT_APPLIED",
    "model_prose": "NOT_READ",
}


@contextmanager
def _rent_lock(session):
    """Serialize rent read/check/write on the existing state root.

    A file lock, not a scheduler or ledger.  It prevents two callers from both
    observing no rent for a period and then each appending a debit/receipt.
    """
    root = Path(session.state_root)
    root.mkdir(parents=True, exist_ok=True)
    with (root / "rolling_reproduction.lock").open("a") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


class PeriodInterleaveOwner:
    """Thin orchestration adapter over the real P3 owner and B02 period advance.

    The BatchEngine still owns batching, reservation and replay.  This adapter
    advances B02 material periods after selected real P3 events and reports the
    post-materialization owner snapshot as the event's after state.  It is not a
    new P3 owner, scheduler or psychology rule.

    ``after_event_dates`` is keyed by the exact P3 event id, not by an in-memory
    position.  A restarted adapter therefore cannot advance the next event's
    date for an already committed event.  A target already elapsed by the time
    the event returns is reported as ALREADY_ELAPSED and is not rewound.
    """

    def __init__(self, owner, session, after_event_dates):
        if not isinstance(after_event_dates, Mapping):
            raise RecursionRefusal("B05_INTERLEAVE_DATES_SCHEMA")
        self.owner = owner
        self.session = session
        self.after_event_dates = {
            str(event_id): str(target_date)
            for event_id, target_date in after_event_dates.items()
        }
        self.materializations = []

    def snapshot(self):
        return self.owner.snapshot()

    def validate_proposal(self, proposal):
        return self.owner.validate_proposal(proposal)

    def _target_tick(self, target_date):
        if hp is None:
            raise RecursionRefusal("B05_INTERLEAVE_B02_UNAVAILABLE")
        try:
            plan = hp.read_period_plan(self.session)
            target = hp._date(target_date, "B05_INTERLEAVE_TARGET_DATE")
            tick = hp._logical_tick(plan, target)
        except RecursionRefusal:
            raise
        except Exception as exc:
            raise RecursionRefusal("B05_INTERLEAVE_TARGET_DATE") from exc
        if not (plan["periods"][0]["start_clock"] <= tick
                <= plan["periods"][-1]["end_clock"]):
            raise RecursionRefusal("B05_INTERLEAVE_TARGET_OUTSIDE_PLAN")
        return tick

    def _stored_result(self, operation_id, proposal, expected):
        """Recover an already committed P3 result after a B02 clock advance.

        P3Owner's normal replay correctly refuses when its recorded after state
        is no longer the current composite state.  That is exactly what happens
        after this adapter legitimately advances B02 following the event.  The
        adapter may read the durable P3 operation receipt here, but it must not
        call the owner again or invent a new event/receipt.
        """
        store = getattr(self.owner, "store", None)
        get_operation = getattr(store, "get_operation", None)
        if not callable(get_operation):
            return None
        try:
            document = get_operation(operation_id)
        except Exception:
            return None
        if not isinstance(document, Mapping) or document.get("phase") != "COMPLETE":
            return None
        value = document.get("result")
        if not isinstance(value, Mapping):
            return None
        if (value.get("operation_id") != operation_id
                or value.get("proposal_hash") != digest(proposal.document())):
            return None
        try:
            before = StateIdentity(**detached(value["before"]))
            after = StateIdentity(**detached(value["after"]))
        except Exception:
            return None
        if before != expected:
            return None
        readset = value.get("readset")
        if not isinstance(readset, (list, tuple)):
            return None
        return RealizedEvent(
            value["operation_id"], value["proposal_hash"], before, after,
            value["status"], detached(value["objective"]),
            detached(value["accessible"]), detached(value["consequences"]),
            tuple(readset), value["receipt_ref"],
        )

    def realize(self, operation_id, proposal, expected):
        target = self.after_event_dates.get(proposal.event_id)
        target_tick = self._target_tick(target) if target is not None else None
        try:
            result = self.owner.realize(operation_id, proposal, expected)
        except RecursionRefusal:
            result = self._stored_result(operation_id, proposal, expected)
            if result is None:
                raise
        advance = None
        if target is not None:
            current = self.session.clock()
            if target_tick < current:
                advance = {
                    "target_date": target,
                    "status": "ALREADY_ELAPSED",
                    "produced_states": 0,
                    "recovered_receipts": 0,
                    "clock": current,
                }
            else:
                advance = hp.materialize_to(self.session, target)
            self.materializations.append({
                "event_id": proposal.event_id,
                "target_date": target,
                "status": advance["status"],
                "produced_states": advance["produced_states"],
                "recovered_receipts": advance["recovered_receipts"],
                "clock": advance["clock"],
            })
        after = self.owner.snapshot()
        objective = detached(result.objective)
        if advance is not None:
            objective["b02_materialized_after_event"] = detached(advance)
        return RealizedEvent(
            result.operation_id, result.proposal_hash, result.before, after,
            result.status, objective, result.accessible, result.consequences,
            result.readset, result.receipt_ref,
        )


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _hash_text(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def _household_cash(household: Mapping[str, Any]) -> int | None:
    for binding in household.get("resources") or ():
        if (binding.get("kind") == "ACTOR_STATE"
                and binding.get("actor_slot") == "A"):
            cash = (binding.get("fields") or {}).get("cash")
            return cash if type(cash) is int and cash >= 0 else None
    return None


def _rent_episodes(session, operation_id: str) -> list[dict]:
    return [
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("kind") == RENT_KIND
        and (row.get("body") or {}).get("operation_id") == operation_id
    ]


def _receipt(session, *, operation_id: str, period_id: str, period_status: str,
             progress: Mapping[str, Any], rent: int, cash_before: int,
             cash_after: int, household_before: Mapping[str, Any],
             household_after: Mapping[str, Any], dwelling: Mapping[str, Any],
             status: str, reasons: list[str]) -> dict:
    return {
        "schema": RENT_RECEIPT_SCHEMA,
        "grade": GRADE,
        "status": status,
        "operation_id": operation_id,
        "root": session.read_root()["root_hash"],
        "branch": session.branch_id,
        "clock": session.clock(),
        "period_id": period_id,
        "period_status": period_status,
        "period_b02_coverage": detached(progress.get("b02_coverage") or []),
        "period_state_coverage": detached(progress.get("state_coverage") or []),
        "period_uncovered": detached(progress.get("uncovered") or []),
        "period_elapsed_ticks": progress.get("elapsed_ticks"),
        "period_remaining_ticks": progress.get("remaining_ticks"),
        "monthly_rent": rent,
        "household_cash_before": cash_before,
        "household_cash_after": cash_after,
        "household_document_source": household_before["source"],
        "household_material_hash_before": household_before["material_hash"],
        "household_material_hash_after": household_after["material_hash"],
        "dwelling_source": dwelling["source"],
        "dwelling_material_hash": dwelling["material_hash"],
        "reasons": list(reasons),
        "scheduled_participation": "NOT_PERFORMED",
        "event_effect": "NONE",
        "public_event": "NOT_EMITTED",
        "psychology_state": "NOT_WRITTEN",
        "actual_reader": "rolling_reproduction.read_household_obligation",
        "read_boundary": detached(READ_BOUNDARY),
    }


def _rent_chain(session, episode_id: str, receipt: Mapping[str, Any]) -> tuple[bool, bool]:
    """Validate the durable rent receipt; current cash may be a later state."""
    household = p6_house.read_household(session)
    dwelling = p6_house.read_dwelling(session)
    if (dwelling["source"] != receipt.get("dwelling_source")
            or household["source"] != receipt.get("household_document_source")):
        return False, False
    before_cash = receipt.get("household_cash_before")
    after_cash = receipt.get("household_cash_after")
    rent = receipt.get("monthly_rent")
    if (type(before_cash) is not int or type(after_cash) is not int
            or type(rent) is not int or rent < 0):
        return False, False
    if receipt.get("status") == "ADMITTED":
        if (rent <= 0 or after_cash >= before_cash
                or before_cash - rent != after_cash):
            return False, False
    elif before_cash != after_cash:
        return False, False
    current_cash = _household_cash(household)
    if current_cash is None:
        return False, False
    return True, current_cash != after_cash


def _checkpoint_household(checkpoint: Mapping[str, Any], *, world_type: Any,
                          root: str, branch: str,
                          actor_ids: tuple[str, ...]) -> dict | None:
    state = checkpoint.get("state")
    snapshot = state.get("world") if isinstance(state, Mapping) else None
    if not isinstance(snapshot, Mapping):
        return None
    try:
        world = world_type.restore(dict(snapshot))
        document = world.resources.get(p6_house.HOUSEHOLD_SLOT)
        if not isinstance(document, Mapping):
            return None
        return p6_house._read_household_document(
            document, world, root, branch, actor_ids)
    except Exception:
        return None


def _rent_transition(receipt: Mapping[str, Any]) -> tuple:
    return (
        receipt.get("root"), receipt.get("branch"), receipt.get("clock"),
        receipt.get("household_cash_before"),
        receipt.get("household_cash_after"),
        receipt.get("household_material_hash_before"),
        receipt.get("household_material_hash_after"),
    )


def _require_actual_rent_transition(session, receipt: Mapping[str, Any], *,
                                    clock: int, rows: list[dict]) -> None:
    """Prove an ADMITTED receipt from the existing C12 checkpoint history.

    ``apply_household_rent`` writes one A-household-cash checkpoint inside its
    ``_StoreWrite`` unit at the same clock as the receipt, immediately after the
    prior checkpoint.  The receipt is admitted only if two adjacent durable
    checkpoints reproduce its exact before/after cash and household material
    hashes.  A caller-computed self-consistent receipt has no such owner
    transition.  The same transition may back exactly one rent operation, so an
    appended sibling cannot copy a real debit as its own evidence.
    """
    root_row = session.read_root()
    root = root_row["root_hash"]
    branch = session.branch_id
    actor_ids = tuple(root_row.get("actor_ids") or ())
    world_type = type(session.world())
    before_cash = receipt.get("household_cash_before")
    after_cash = receipt.get("household_cash_after")
    before_hash = receipt.get("household_material_hash_before")
    after_hash = receipt.get("household_material_hash_after")
    source = receipt.get("household_document_source")
    previous_checkpoint = None
    previous_household = None
    matched = False
    for checkpoint in session.product.store.checkpoints(branch):
        household = _checkpoint_household(
            checkpoint, world_type=world_type, root=root, branch=branch,
            actor_ids=actor_ids)
        if (previous_household is not None and household is not None
                and checkpoint.get("clock") == clock
                and previous_checkpoint.get("clock") <= clock
                and _household_cash(previous_household) == before_cash
                and previous_household["material_hash"] == before_hash
                and _household_cash(household) == after_cash
                and household["material_hash"] == after_hash
                and previous_household["source"] == source
                and household["source"] == source):
            matched = True
            break
        previous_checkpoint = checkpoint
        previous_household = household
    if not matched:
        raise RecursionRefusal("B05_RENT_OPERATION_UNPROVEN")
    identity = _rent_transition(receipt)
    shared = [
        row for row in rows
        if _rent_transition(
            (row.get("body") or {}).get("receipt") or {}) == identity
    ]
    if len(shared) != 1:
        raise RecursionRefusal("B05_RENT_OPERATION_UNPROVEN")


def _apply_household_rent(session, *, operation_id: str, period_id: str,
                         expected_clock: int | None = None) -> dict:
    """Charge one completed period's household rent against fixed-A cash."""
    if p6_house is None or hp is None:
        raise RecursionRefusal("B05_COMPOSITION_UNAVAILABLE")
    if not _text(operation_id) or not _text(period_id):
        raise RecursionRefusal("B05_RENT_SCHEMA")
    if expected_clock is not None and expected_clock != session.clock():
        raise RecursionRefusal("B05_RENT_CLOCK_MISMATCH")
    progress = hp.period_progress(session, period_id)
    if progress["status"] != "COMPLETE":
        raise RecursionRefusal("B05_PERIOD_NOT_COMPLETE")
    household = p6_house.read_household(session)
    dwelling = p6_house.read_dwelling(session)
    rent = dwelling["costs"].get("monthly_rent")
    if rent == "UNKNOWN":
        raise RecursionRefusal("B05_RENT_UNKNOWN")
    if type(rent) is not int or rent < 0:
        raise RecursionRefusal("B05_RENT_SCHEMA")
    cash = _household_cash(household)
    if cash is None:
        raise RecursionRefusal("B05_HOUSEHOLD_CASH_UNKNOWN")
    episodes = _rent_episodes(session, operation_id)
    if len(episodes) > 1:
        raise RecursionRefusal("B05_RENT_OPERATION_DUPLICATE")
    if episodes:
        body = episodes[0].get("body") or {}
        receipt = dict(body.get("receipt") or {})
        if (receipt.get("period_id") != period_id
                or receipt.get("monthly_rent") != rent
                or receipt.get("dwelling_source") != dwelling["source"]):
            raise RecursionRefusal("B05_RENT_OPERATION_REUSE_MISMATCH")
        valid, historical = _rent_chain(
            session, episodes[0].get("episode_id"), receipt)
        if not valid:
            raise RecursionRefusal("B05_RENT_REPLAY_STALE")
        receipt["status"] = "REPLAY"
        receipt["historical"] = historical
        return receipt
    period_episodes = [
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("kind") == RENT_KIND
        and ((row.get("body") or {}).get("receipt") or {}).get("period_id")
        == period_id
    ]
    if period_episodes:
        raise RecursionRefusal("B05_RENT_ALREADY_RECORDED")
    reasons = []
    status = "ADMITTED"
    cash_after = cash
    if rent > cash:
        status = "REFUSED"
        reasons = ["B05_INSUFFICIENT_HOUSEHOLD_CASH"]
    elif rent == 0:
        status = "UNCHANGED"
    else:
        cash_after = cash - rent
    store = session.product.store
    with _StoreWrite(store):
        if status == "ADMITTED":
            world = session.world()
            world.actor_state["A"]["cash"] = cash_after
            session.product._checkpoint(session.branch_id, world.clock, world)
            after = p6_house.read_household(session)
        else:
            after = household
        receipt = _receipt(
            session, operation_id=operation_id, period_id=period_id,
            period_status=progress["status"], progress=progress, rent=rent,
            cash_before=cash, cash_after=cash_after, household_before=household,
            household_after=after, dwelling=dwelling, status=status,
            reasons=reasons,
        )
        store.append_episode(
            session.branch_id, actor_id="A", kind=RENT_KIND,
            clock=session.clock(),
            body={
                "schema": RENT_RECEIPT_SCHEMA, "grade": GRADE,
                "root": receipt["root"], "branch": receipt["branch"],
                "operation_id": operation_id, "status": status,
                "receipt": receipt,
            },
        )
    return receipt


def apply_household_rent(session, *, operation_id: str, period_id: str,
                         expected_clock: int | None = None) -> dict:
    """Charge one completed period's household rent under the rent lock."""
    with _rent_lock(session):
        return _apply_household_rent(
            session, operation_id=operation_id, period_id=period_id,
            expected_clock=expected_clock,
        )


def _rent_read_provenance(session, episode: Mapping[str, Any],
                          receipt: Mapping[str, Any], *,
                          operation_id: str) -> str:
    root = session.read_root()["root_hash"]
    branch = session.branch_id
    body = episode.get("body") or {}
    if (episode.get("actor_id") != "A"
            or body.get("schema") != RENT_RECEIPT_SCHEMA
            or body.get("grade") != GRADE
            or body.get("root") != root
            or body.get("branch") != branch
            or body.get("operation_id") != operation_id):
        raise RecursionRefusal("B05_RENT_PROVENANCE_MISMATCH")
    if (receipt.get("schema") != RENT_RECEIPT_SCHEMA
            or receipt.get("grade") != GRADE
            or receipt.get("root") != root
            or receipt.get("branch") != branch
            or receipt.get("operation_id") != operation_id):
        raise RecursionRefusal("B05_RENT_PROVENANCE_MISMATCH")
    status = receipt.get("status")
    if (status not in {"ADMITTED", "REFUSED", "UNCHANGED"}
            or body.get("status") != status):
        raise RecursionRefusal("B05_RENT_PROVENANCE_MISMATCH")
    if receipt.get("clock") != episode.get("clock"):
        raise RecursionRefusal("B05_RENT_PROVENANCE_MISMATCH")
    return status


def read_household_obligation(session, operation_id: str) -> dict:
    """Read a rent receipt and verify its source chain and stable household doc."""
    if p6_house is None or hp is None:
        raise RecursionRefusal("B05_COMPOSITION_UNAVAILABLE")
    rows = [
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("kind") == RENT_KIND
    ]
    episodes = [
        row for row in rows
        if (row.get("body") or {}).get("operation_id") == operation_id
    ]
    if len(episodes) != 1:
        raise RecursionRefusal("B05_RENT_NOT_FOUND")
    receipt = dict((episodes[0].get("body") or {}).get("receipt") or {})
    status = _rent_read_provenance(
        session, episodes[0], receipt, operation_id=operation_id)
    household = p6_house.read_household(session)
    dwelling = p6_house.read_dwelling(session)
    if (dwelling["source"] != receipt.get("dwelling_source")
            or household["source"] != receipt.get("household_document_source")):
        raise RecursionRefusal("B05_RENT_SOURCE_STALE")
    before_hash = receipt.get("household_material_hash_before")
    after_hash = receipt.get("household_material_hash_after")
    before_cash = receipt.get("household_cash_before")
    after_cash = receipt.get("household_cash_after")
    rent = receipt.get("monthly_rent")
    if (not _hash_text(before_hash) or not _hash_text(after_hash)
            or type(before_cash) is not int or type(after_cash) is not int
            or type(rent) is not int or rent < 0):
        raise RecursionRefusal("B05_RENT_RECEIPT_INVALID")
    if status == "ADMITTED":
        if (rent <= 0 or after_cash >= before_cash
                or before_cash - rent != after_cash):
            raise RecursionRefusal("B05_RENT_RECEIPT_INVALID")
    elif before_cash != after_cash:
        raise RecursionRefusal("B05_RENT_RECEIPT_INVALID")
    current_rent = dwelling["costs"].get("monthly_rent")
    if type(current_rent) is not int or rent != current_rent:
        raise RecursionRefusal("B05_RENT_PROVENANCE_MISMATCH")
    period_id = receipt.get("period_id")
    if not _text(period_id) or receipt.get("period_status") != "COMPLETE":
        raise RecursionRefusal("B05_RENT_PERIOD_MISMATCH")
    try:
        progress = hp.period_progress(session, period_id)
    except RecursionRefusal as exc:
        raise RecursionRefusal("B05_RENT_PERIOD_MISMATCH") from exc
    if progress.get("status") != "COMPLETE":
        raise RecursionRefusal("B05_RENT_PERIOD_MISMATCH")
    period_episodes = [
        row for row in rows
        if ((row.get("body") or {}).get("receipt") or {}).get("period_id")
        == period_id
    ]
    if len(period_episodes) != 1 or period_episodes[0] is not episodes[0]:
        raise RecursionRefusal("B05_RENT_OPERATION_NOT_UNIQUE")
    valid, historical = _rent_chain(
        session, episodes[0].get("episode_id"), receipt)
    if not valid:
        raise RecursionRefusal("B05_RENT_SOURCE_STALE")
    if status == "ADMITTED":
        _require_actual_rent_transition(
            session, receipt, clock=episodes[0].get("clock"), rows=rows)
    current_hash = household["material_hash"]
    return {
        "schema": HOUSEHOLD_OBLIGATION_SCHEMA,
        "grade": GRADE,
        "status": "READ",
        "operation_id": operation_id,
        "receipt": receipt,
        "historical": historical,
        "household_source": household["source"],
        "household_material_hash": current_hash,
        "household_cash": _household_cash(household),
        "dwelling_source": dwelling["source"],
        "scheduled_participation": "NOT_PERFORMED",
        "psychology_state": "NOT_WRITTEN",
        "read_boundary": detached(READ_BOUNDARY),
    }


__all__ = [
    "RENT_KIND", "RENT_RECEIPT_SCHEMA", "HOUSEHOLD_OBLIGATION_SCHEMA",
    "GRADE", "PeriodInterleaveOwner", "apply_household_rent",
    "read_household_obligation",
]
