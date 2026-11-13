"""Native P3 pending-reservation tests for the #1010 performer.

These tests create ACTUAL PREPARED rows through the frozen PsycheStore.reserve
ABI instead of monkeypatching ``pending()``. The reserved operation is never
completed, which is the head-invisible state the custody guard exists to catch.
"""
from __future__ import annotations

import copy
import sqlite3
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
WR = HERE.parent
for item in (
    HERE,
    WR / "SOROK-E01-J1-995-R1",
    WR / "SOROK-D03-E01-1010-AGENT-A-R1",
    WR / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1",
    WR / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1" / "tests",
    WR / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1",
    WR / "SOROK-DUEL-B02-R1",
    WR / "SOROK-DUEL-B04-R1",
    WR / "SOROK-DUEL-B05-R1",
    WR / "SOROK-P6-ONE-LIVING-HOUSE-R1",
    WR / "SOROK-P4-FIRST-FULL-MPC-R1",
    WR / "SOROK-S45-S47-PROJECTION-20261105-R1",
    WR / "SOROK-DUEL-D03-R1" / "tests",
):
    if str(item) not in sys.path:
        sys.path.insert(0, str(item))

from developmental_recursion.contracts import RecursionRefusal, digest  # noqa: E402
from test_d03_e01_performer import (  # noqa: E402
    ExactActorProvider,
    _close,
    _invoke,
)
from test_j1_three_head_join import open_j1_case  # noqa: E402


def _reserve_real_pending(owner, plan, operation_id):
    base = owner.base_owner.snapshot()
    return owner.store.reserve(
        operation_id,
        proposal_hash=digest({"fixture": operation_id}),
        expected=owner.snapshot().document(),
        plan_hash=plan["hash"],
        base_before=base.document(),
        psyche_before=owner.store.head(),
        plan=plan,
    )


def test_real_preexisting_p3_reservation_refuses_at_d03_entry(tmp_path):
    opened = open_j1_case(tmp_path / "real-pre")
    owner = opened["case"].owner
    provider = ExactActorProvider(owner.base_owner)
    before_events = list(opened["session"].read_events())
    before_head = copy.deepcopy(owner.store.head())
    try:
        row = _reserve_real_pending(owner, opened["plan"], "native-real-pre")
        assert row["phase"] == "PREPARED"
        assert owner.store.head() == before_head
        assert owner.store.pending()
        with pytest.raises(RecursionRefusal, match="D03_PENDING_OPERATION"):
            _invoke(opened, provider)
        assert provider.calls == []
        assert opened["session"].read_events() == before_events
        assert owner.store.head() == before_head
        assert [item["operation_id"] for item in owner.store.pending()] == [
            "native-real-pre"]
        assert not (opened["path"] / "e01_recursion_cycle.json").exists()
        assert not (opened["path"] / "e01_p2_journal.sqlite").exists()
    finally:
        _close(opened)


class ReservingProvider:
    """Hostile provider that creates a real PREPARED P3 row after returning."""

    def __init__(self, delegate, owner, plan, operation_id):
        self._delegate = delegate
        self._owner = owner
        self._plan = plan
        self._operation_id = operation_id
        self.calls = []

    def call(self, request):
        response = self._delegate.call(request)
        self.calls.append(copy.deepcopy(request))
        row = _reserve_real_pending(
            self._owner, self._plan, self._operation_id)
        assert row["phase"] == "PREPARED"
        return response


def test_real_pending_after_provider_refuses_before_any_p2_write(tmp_path):
    opened = open_j1_case(tmp_path / "real-post")
    owner = opened["case"].owner
    delegate = ExactActorProvider(owner.base_owner)
    provider = ReservingProvider(
        delegate, owner, opened["plan"], "native-real-post")
    before_events = list(opened["session"].read_events())
    before_head = copy.deepcopy(owner.store.head())
    try:
        with pytest.raises(
                RecursionRefusal, match="E01_POSTPROVIDER_P3_PENDING_OPERATION"):
            _invoke(opened, provider)
        assert len(provider.calls) == 1
        assert opened["session"].read_events() == before_events
        assert owner.store.head() == before_head
        assert [item["operation_id"] for item in owner.store.pending()] == [
            "native-real-post"]
        assert (opened["path"] / "e01_recursion_cycle.json").exists()
        journal = opened["path"] / "e01_p2_journal.sqlite"
        with sqlite3.connect(journal) as connection:
            batches = connection.execute(
                "SELECT COUNT(*) FROM batches").fetchone()[0]
            events = connection.execute(
                "SELECT COUNT(*) FROM events").fetchone()[0]
        assert (batches, events) == (0, 0)
    finally:
        _close(opened)
