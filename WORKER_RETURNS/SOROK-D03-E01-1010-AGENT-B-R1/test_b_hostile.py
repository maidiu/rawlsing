"""Agent B: full-fixture red controls for A's post-provider P3/source race.

Requires the exact PR #996 + A descendant and the inherited test dependencies.
These are NOT substitutes for the full J1/G2 end-to-end performed-action proof.
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
A_DIR = HERE.parent / "SOROK-D03-E01-1010-AGENT-A-R1"
if str(A_DIR) not in sys.path:
    sys.path.insert(0, str(A_DIR))

from test_d03_e01_performer import (  # noqa: E402
    ExactActorProvider, _close, _invoke, open_j1_case,
)
from developmental_recursion.contracts import RecursionRefusal  # noqa: E402
import j1_join  # noqa: E402


def test_b_provider_changes_p3_head_before_p2_write(tmp_path, monkeypatch):
    opened = open_j1_case(tmp_path / "b-p3-drift")
    owner = opened["case"].owner
    base = owner.base_owner
    original_head = owner.store.head
    provider_events_before = list(opened["session"].read_events())
    original_p3 = copy.deepcopy(original_head())

    class MovingP3Provider(ExactActorProvider):
        def call(self, request):
            response = super().call(request)
            def drift():
                value = copy.deepcopy(original_head())
                value["hash"] = ("0" * 64 if value["hash"] != "0" * 64
                                 else "f" * 64)
                return value
            monkeypatch.setattr(owner.store, "head", drift)
            return response

    provider = MovingP3Provider(base)
    try:
        with pytest.raises(RecursionRefusal, match="E01_POSTPROVIDER_P3_HEAD_CHANGED"):
            _invoke(opened, provider)
        assert len(provider.calls) == 1
        assert opened["session"].read_events() == provider_events_before
        assert (opened["path"] / "e01_recursion_cycle.json").exists()
    finally:
        monkeypatch.undo()
        assert owner.store.head() == original_p3
        _close(opened)


def test_b_provider_changes_source_closure_before_p2_write(tmp_path, monkeypatch):
    opened = open_j1_case(tmp_path / "b-source-drift")
    before = list(opened["session"].read_events())
    original_closure = j1_join.source_closure
    class MovingSourceProvider(ExactActorProvider):
        def call(self, request):
            response = super().call(request)
            monkeypatch.setattr(
                j1_join, "source_closure", lambda: {"hash": "0" * 64})
            return response

    provider = MovingSourceProvider(opened["case"].owner.base_owner)
    try:
        assert original_closure()["hash"] != "0" * 64
        with pytest.raises(RecursionRefusal, match="E01_POSTPROVIDER_J1_SOURCE_CHANGED"):
            _invoke(opened, provider)
        assert len(provider.calls) == 1
        assert opened["session"].read_events() == before
    finally:
        monkeypatch.undo()
        _close(opened)
