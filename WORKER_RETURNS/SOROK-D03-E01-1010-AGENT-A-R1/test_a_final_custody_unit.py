"""Dependency-free adversarial custody proof for D03/E01 #1010.

These tests prove owner-lease sequencing, not integrated P2 event semantics.
The full PR #996 native owners and J1/P6 tests require a real checkout.
"""
from __future__ import annotations

import sys
import threading
from contextlib import contextmanager
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from owner_custody import P3CoordinatedP2Owner


class MockP3:
    def __init__(self, base):
        self.base_owner = base
        self.lock = threading.Lock()
        self.head = "old"
        self.pending = []
        self.source = "original"
        self.records = []

    @contextmanager
    def _root_lock(self):
        with self.lock:
            self.records.append("P3_LOCK")
            try:
                yield
            finally:
                self.records.append("P3_UNLOCK")


class MockP2:
    def __init__(self):
        self.state = 0
        self.writes = []
        self.records = []
        self.after_write = None

    def snapshot(self):
        return self.state

    def validate_proposal(self, proposal):
        self.records.append("VALIDATED")
        return True

    def realize(self, op, proposal, expected):
        assert expected == self.state
        self.records.append("P2_LOCK")
        self.writes.append((op, proposal))
        self.state += 1
        if self.after_write:
            self.after_write()
        self.records.append("P2_UNLOCK")
        return {"after": self.state}


def scene():
    base = MockP2()
    p3 = MockP3(base)

    def check():
        if p3.pending:
            raise ValueError("E01_P3_PENDING_OPERATION")
        if p3.head != "old":
            raise ValueError("E01_P3_HEAD_CHANGED")
        if p3.source != "original":
            raise ValueError("E01_SOURCE_CHANGED")

    return base, p3, P3CoordinatedP2Owner(p3, base, check)


def test_normal_delegated_realization_preserves_p3_then_p2_lock_order():
    base, p3, adapter = scene()
    assert adapter.snapshot() == 0
    assert adapter.validate_proposal("qualified") is True
    assert adapter.realize("op1", "qualified", 0)["after"] == 1
    assert p3.records == ["P3_LOCK", "P3_UNLOCK"]
    assert base.records == ["VALIDATED", "P2_LOCK", "P2_UNLOCK"]
    assert base.writes == [("op1", "qualified")]


def test_pending_while_head_unchanged_is_rejected_before_any_p2_write():
    base, p3, adapter = scene()
    # B's head/identity only guard would miss this independently reserved op.
    p3.pending = [{"phase": "PREPARED", "id": "unresolved"}]
    assert p3.head == "old" and base.snapshot() == 0
    with pytest.raises(ValueError, match="E01_P3_PENDING_OPERATION"):
        adapter.realize("op1", "qualified", 0)
    assert base.writes == [] and p3.records == ["P3_LOCK", "P3_UNLOCK"]


def test_source_change_after_provider_before_realize_is_rejected():
    base, p3, adapter = scene()
    p3.source = "different"
    with pytest.raises(ValueError, match="E01_SOURCE_CHANGED"):
        adapter.realize("op1", "qualified", 0)
    assert base.writes == []


def test_expected_owner_state_must_match_under_lease():
    base, p3, adapter = scene()
    with pytest.raises(ValueError, match="E01_OWNER_MOVED_BEFORE_P2_REALIZE"):
        adapter.realize("op1", "qualified", 100)
    assert base.writes == []


def test_reservation_between_batch_events_holds_second_event():
    base, p3, adapter = scene()
    adapter.realize("op1", "qualified", 0)
    p3.pending = [{"phase": "PREPARED"}]
    with pytest.raises(ValueError, match="E01_P3_PENDING_OPERATION"):
        adapter.realize("op2", "qualified", 1)
    assert len(base.writes) == 1


def test_p3_owner_mutation_attempt_waits_for_original_p2_owner_write():
    base, p3, adapter = scene()
    entered_p2 = threading.Event()
    allow_complete = threading.Event()
    completed_p3 = threading.Event()
    started_p3 = threading.Event()
    worker_errors = []

    def stall():
        entered_p2.set()
        if not allow_complete.wait(timeout=3):
            raise RuntimeError("test worker timed out")

    base.after_write = stall

    def perform():
        try:
            adapter.realize("op1", "qualified", 0)
        except Exception as exc:
            worker_errors.append(exc)

    def competing_p3_operation():
        started_p3.set()
        with p3._root_lock():
            p3.pending = [{"phase": "PREPARED"}]
            completed_p3.set()

    first = threading.Thread(target=perform)
    second = threading.Thread(target=competing_p3_operation)
    first.start()
    try:
        assert entered_p2.wait(timeout=3)
        second.start()
        assert started_p3.wait(timeout=3)
        assert not completed_p3.wait(timeout=0.08), (
            "P3 mutation entered while original P2 event writer still held lease")
        allow_complete.set()
        first.join(timeout=3)
        second.join(timeout=3)
        assert not worker_errors
        assert not first.is_alive() and not second.is_alive()
        assert completed_p3.is_set()
        assert base.writes == [("op1", "qualified")]
    finally:
        allow_complete.set()
        first.join(timeout=3)
        if second.ident is not None:
            second.join(timeout=3)


def test_after_write_guard_reports_illicit_unlocked_mutation_not_atomicity():
    base, p3, adapter = scene()
    base.after_write = lambda: setattr(p3, "head", "foreign_direct_writer")
    with pytest.raises(ValueError, match="E01_P3_HEAD_CHANGED"):
        adapter.realize("op1", "qualified", 0)
    assert len(base.writes) == 1, "Check cannot roll back a direct bypass writer"
