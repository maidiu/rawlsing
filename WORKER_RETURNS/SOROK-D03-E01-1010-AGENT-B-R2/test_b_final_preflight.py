"""B optional final exchange: refuse already-known P3 HOLD before provider call.

This is an actual J1/P3/P2 fixture test, NOT independently executed in this
GitHub-only review environment. Run with the original inherited test suite.
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


def test_preexisting_p3_pending_refuses_before_provider_and_cycle(tmp_path, monkeypatch):
    opened = open_j1_case(tmp_path / "already-pending")
    owner = opened["case"].owner
    session = opened["session"]
    provider = ExactActorProvider(owner.base_owner)
    before_world = copy.deepcopy(session.read_events())
    before_head = copy.deepcopy(owner.store.head())
    monkeypatch.setattr(
        owner.store,
        "pending",
        lambda: [{"phase": "PREPARED", "operation_id": "unresolved-before-call"}],
    )
    try:
        with pytest.raises(
            RecursionRefusal,
            match="E01_POSTPROVIDER_P3_PENDING_OPERATION",
        ):
            _invoke(opened, provider)
        assert provider.calls == [], "already-known invalid P3 state charged a model call"
        assert session.read_events() == before_world
        assert owner.store.head() == before_head
        assert not (opened["path"] / "e01_p2_journal.sqlite").exists()
        assert not (opened["path"] / "e01_recursion_cycle.json").exists()
    finally:
        monkeypatch.undo()
        _close(opened)
