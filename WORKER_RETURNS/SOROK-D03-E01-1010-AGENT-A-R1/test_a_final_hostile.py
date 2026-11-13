"""A final source-contract adversarial tests using the actual PR #996 fixture.

These are integrated first-consumer tests and MUST run against the complete
checkout. They are not covered by the seven local dependency-free unit PASSes.
"""
from __future__ import annotations

import copy
import sys
from contextlib import contextmanager
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from test_d03_e01_performer import (  # noqa: E402
    ExactActorProvider, _close, _invoke, open_j1_case,
)
from developmental_recursion.contracts import RecursionRefusal  # noqa: E402
import d03_e01_performer as a  # noqa: E402


def test_reserved_p3_operation_with_unchanged_head_rejects_before_world_write(
    tmp_path, monkeypatch,
):
    opened = open_j1_case(tmp_path / "pending-at-provider")
    owner = opened["case"].owner
    baseline = copy.deepcopy(owner.store.head())
    world_before = list(opened["session"].read_events())

    class PendingDuringProvider(ExactActorProvider):
        def call(self, request):
            result = super().call(request)
            monkeypatch.setattr(
                owner.store, "pending",
                lambda: [{"phase": "PREPARED", "operation_id": "foreign"}],
            )
            assert owner.store.head() == baseline
            return result

    provider = PendingDuringProvider(owner.base_owner)
    try:
        with pytest.raises(
            RecursionRefusal, match="E01_POSTPROVIDER_P3_PENDING_OPERATION"
        ):
            _invoke(opened, provider)
        assert len(provider.calls) == 1
        assert opened["session"].read_events() == world_before
        assert owner.store.head() == baseline
        assert (opened["path"] / "e01_recursion_cycle.json").exists()
    finally:
        monkeypatch.undo()
        _close(opened)


def test_pending_inserted_after_b_proxy_before_first_owner_realize_holds(
    tmp_path, monkeypatch,
):
    opened = open_j1_case(tmp_path / "pending-between-guard-and-write")
    owner = opened["case"].owner
    baseline = copy.deepcopy(owner.store.head())
    world_before = list(opened["session"].read_events())
    original_batch = a.BatchEngine.run_batch

    def inject_after_guard(self, batch_id, proposals):
        # Provider returned and B's GuardedProvider approved its readset.
        # The external reservation then appears before real P2 write custody.
        monkeypatch.setattr(
            owner.store, "pending",
            lambda: [{"phase": "PREPARED", "operation_id": "racing-p3"}],
        )
        assert owner.store.head() == baseline
        return original_batch(self, batch_id, proposals)

    provider = ExactActorProvider(owner.base_owner)
    monkeypatch.setattr(a.BatchEngine, "run_batch", inject_after_guard)
    try:
        with pytest.raises(
            RecursionRefusal, match="E01_EVENT_WRITE_P3_PENDING_OPERATION"
        ):
            _invoke(opened, provider)
        assert len(provider.calls) == 1
        assert opened["session"].read_events() == world_before
        assert owner.store.head() == baseline
    finally:
        monkeypatch.undo()
        _close(opened)


def test_actual_p2_writer_is_called_while_p3_owner_root_lock_is_held(
    tmp_path, monkeypatch,
):
    opened = open_j1_case(tmp_path / "witness-real-owner-lease")
    owner = opened["case"].owner
    base = owner.base_owner
    original_lock = owner._root_lock
    original_realize = base.realize
    state = {"locked": False, "writes": 0}

    @contextmanager
    def witness_lock():
        with original_lock():
            assert not state["locked"]
            state["locked"] = True
            try:
                yield
            finally:
                state["locked"] = False

    def witnessed_base_realize(operation_id, proposal, expected):
        assert state["locked"], "P2 owner write escaped P3 root lease"
        state["writes"] += 1
        return original_realize(operation_id, proposal, expected)

    monkeypatch.setattr(owner, "_root_lock", witness_lock)
    monkeypatch.setattr(base, "realize", witnessed_base_realize)
    provider = ExactActorProvider(base)
    try:
        report = _invoke(opened, provider)
        assert state["writes"] == 3
        assert report["world_events_written"] == 3
        assert report["g2_historical_child_performance"] == "HELD_NOT_ESTABLISHED"
        assert report["per_event_custody"] == (
            "P3_ROOT_LOCK_PER_P2_REALIZE_ORIGINAL_ORDER")
        assert report["cross_owner_atomicity"] == "NOT_CLAIMED"
        assert not state["locked"]
        for row in report["world_readbacks"]:
            actual = opened["session"].read_event(row["admitted_e1_event_id"])
            assert actual["e1_event_hash"] == row["admitted_e1_event_hash"]
    finally:
        monkeypatch.undo()
        _close(opened)
