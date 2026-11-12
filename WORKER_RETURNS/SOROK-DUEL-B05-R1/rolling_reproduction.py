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
    RealizedEvent, RecursionRefusal, detached, digest,
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
    only advances B02 material periods after selected real P3 events and reports
    the post-materialization owner snapshot as the event's after state.  It is
    not a new P3 owner, scheduler or psychology rule.
    """

    def __init__(self, owner, session, after_event_dates):
        self.owner = owner
        self.session = session
        self.after_event_dates = list(after_event_dates)
        self._index = 0
        self.materializations = []

    def snapshot(self):
        return self.owner.snapshot()

    def validate_proposal(self, proposal):
        return self.owner.validate_proposal(proposal)

    def realize(self, operation_id, proposal, expected):
        result = self.owner.realize(operation_id, proposal, expected)
        target = None
        if self._index < len(self.after_event_dates):
            target = self.after_event_dates[self._index]
            self._index += 1
            advance = hp.materialize_to(self.session, target)
            self.materializations.append({
                "target_date": target,
                "status": advance["status"],
                "produced_states": advance["produced_states"],
                "recovered_receipts": advance["recovered_receipts"],
                "clock": advance["clock"],
            })
        after = self.owner.snapshot()
        objective = detached(result.objective)
        if target is not None:
            objective["b02_materialized_after_event"] = detached(
                self.materializations[-1])
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
    if receipt.get("status") == "ADMITTED" and before_cash - rent != after_cash:
        return False, False
    if receipt.get("status") != "ADMITTED" and before_cash != after_cash:
        return False, False
    current_cash = _household_cash(household)
    if current_cash is None:
        return False, False
    return True, current_cash != after_cash


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


def read_household_obligation(session, operation_id: str) -> dict:
    """Read a rent receipt and verify its source chain and stable household doc."""
    if p6_house is None:
        raise RecursionRefusal("B05_COMPOSITION_UNAVAILABLE")
    episodes = _rent_episodes(session, operation_id)
    if len(episodes) != 1:
        raise RecursionRefusal("B05_RENT_NOT_FOUND")
    receipt = dict((episodes[0].get("body") or {}).get("receipt") or {})
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
    if receipt.get("status") == "ADMITTED" and before_cash - rent != after_cash:
        raise RecursionRefusal("B05_RENT_RECEIPT_INVALID")
    if receipt.get("status") != "ADMITTED" and before_cash != after_cash:
        raise RecursionRefusal("B05_RENT_RECEIPT_INVALID")
    period_id = receipt.get("period_id")
    valid, historical = _rent_chain(
        session, episodes[0].get("episode_id"), receipt)
    if not valid:
        raise RecursionRefusal("B05_RENT_SOURCE_STALE")
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
