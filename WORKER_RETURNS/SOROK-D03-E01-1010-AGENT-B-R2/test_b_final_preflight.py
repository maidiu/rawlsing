"""SOROK #1010 exact B-R2 correction: two *different* pending windows.

(1) Pending before original C04/P6/D03 join is refused by the *original D03*
    reader (D03_PENDING_OPERATION). The new B preflight cannot run first.
(2) Pending AFTER the completed J1/D03 read but BEFORE BatchEngine/provider
    is refused by B R2's E01_POSTPROVIDER_P3_PENDING_OPERATION preflight.

Only scenario (2) demonstrates added B R2 fail-fast behavior. These real
J1/P3/P2 fixtures are AUTHORED_NOT_RUN until an actual full checkout executes.
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
A = HERE.parent / "SOROK-D03-E01-1010-AGENT-A-R1"
if str(A) not in sys.path:
    sys.path.insert(0, str(A))

from test_d03_e01_performer import (  # noqa: E402
    ExactActorProvider, _close, _invoke, open_j1_case,
)
from developmental_recursion.contracts import RecursionRefusal  # noqa: E402
import j1_join  # noqa: E402


def _assert_clean(opened, provider, before_world, before_head):
    assert provider.calls == []
    assert opened["session"].read_events() == before_world
    assert opened["case"].owner.store.head() == before_head
    assert not (opened["path"] / "e01_p2_journal.sqlite").exists()
    assert not (opened["path"] / "e01_recursion_cycle.json").exists()


def test_preexisting_p3_pending_is_already_rejected_by_d03(tmp_path, monkeypatch):
    opened = open_j1_case(tmp_path / "already-pending")
    owner = opened["case"].owner
    session = opened["session"]
    provider = ExactActorProvider(owner.base_owner)
    before_world = copy.deepcopy(session.read_events())
    before_head = copy.deepcopy(owner.store.head())
    monkeypatch.setattr(
        owner.store, "pending",
        lambda: [{"phase": "PREPARED", "operation_id": "unresolved-before-j1"}],
    )
    try:
        # Original immediate_uptake.build_immediate_uptake inspects pending
        # before looking up the C12 receipt or reading acquired records.
        with pytest.raises(RecursionRefusal, match="D03_PENDING_OPERATION"):
            _invoke(opened, provider)
        _assert_clean(opened, provider, before_world, before_head)
    finally:
        monkeypatch.undo()
        _close(opened)


def test_pending_first_appears_after_real_j1_before_provider(tmp_path, monkeypatch):
    opened = open_j1_case(tmp_path / "between-j1-and-cycle")
    owner = opened["case"].owner
    provider = ExactActorProvider(owner.base_owner)
    before_world = copy.deepcopy(opened["session"].read_events())
    before_head = copy.deepcopy(owner.store.head())
    original_j1 = j1_join.compose_j1
    witnessed = {"joined": False}

    def inject_pending_after_completed_j1(*args, **kwargs):
        result = original_j1(*args, **kwargs)
        # Only modify source-owned *read* of pending AFTER original D03
        # successfully proved its real qualified public speech/actor readset.
        # This simulates a cooperating writer's new reservation, not a
        # preexisting D03 condition.
        assert result["status"] == j1_join.UPSTREAM_PROVEN
        witnessed["joined"] = True
        monkeypatch.setattr(
            owner.store, "pending",
            lambda: [{"phase": "PREPARED", "operation_id": "new-after-j1"}],
        )
        return result

    monkeypatch.setattr(j1_join, "compose_j1", inject_pending_after_completed_j1)
    try:
        with pytest.raises(
            RecursionRefusal, match="E01_POSTPROVIDER_P3_PENDING_OPERATION"
        ):
            _invoke(opened, provider)
        assert witnessed["joined"], "J1's actual prior D03 refusal is not B's fix"
        _assert_clean(opened, provider, before_world, before_head)
    finally:
        monkeypatch.undo()
        _close(opened)
