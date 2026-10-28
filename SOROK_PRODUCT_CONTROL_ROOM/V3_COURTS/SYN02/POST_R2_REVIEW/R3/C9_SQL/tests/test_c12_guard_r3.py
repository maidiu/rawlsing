"""C9-R3 C12 fork-guard policy test over actual JOIN-E source; read-only."""
from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

import c12_guard_r3 as guard


def _root(store, C12Store=None):
    from bp4.world import make_event
    store.create_root(
        "root", clock=10, actor_ids=["A", "B"],
        state={"world": {"clock": 10}, "actors": {"A": {}, "B": {}}},
    )
    e1 = make_event(clock=10, kind="NO_CHANGE", actor_id="A",
                    location="workshop", summary="clock-ten", body={"n": 1})
    store.append_world_event("root", e1)
    store.record_perception("root", actor_id="A", event_id=e1["event_id"],
                            clock=10, channel="co_present")
    e2 = make_event(clock=10, kind="NO_CHANGE", actor_id="A",
                    location="workshop", summary="clock-eleven", body={"n": 2})
    store.append_world_event("root", e2)
    store.record_perception("root", actor_id="A", event_id=e2["event_id"],
                            clock=11, channel="co_present")
    return e1, e2


def test_actual_perception_only_suffix_returns_fork_held():
    try:
        _, C12Store = guard.load_c12()
    except RuntimeError as exc:
        pytest.skip(str(exc))
    with tempfile.TemporaryDirectory() as td:
        store = C12Store(Path(td) / "c12.sqlite")
        try:
            _root(store)
            with pytest.raises(guard.C12ForkHeld) as exc:
                guard.guard_fork(store, "root", "blocked")
            assert exc.value.code == "C12_PERCEPTION_ONLY_SUFFIX"
            assert store._branch("blocked") is None
            assert store.verify("root")["ok"] is True
        finally:
            store.close()


def test_clean_perception_cut_can_fork_with_guard():
    try:
        _, C12Store = guard.load_c12()
    except RuntimeError as exc:
        pytest.skip(str(exc))
    from bp4.world import make_event
    with tempfile.TemporaryDirectory() as td:
        store = C12Store(Path(td) / "c12.sqlite")
        try:
            store.create_root(
                "root", clock=10, actor_ids=["A", "B"],
                state={"world": {"clock": 10}, "actors": {"A": {}, "B": {}}},
            )
            event = make_event(clock=10, kind="NO_CHANGE", actor_id="A",
                               location="workshop", summary="clean", body={"n": 1})
            store.append_world_event("root", event)
            store.record_perception("root", actor_id="A", event_id=event["event_id"],
                                    clock=10, channel="co_present")
            child = guard.guard_fork(store, "root", "clean-child")
            assert child["fork_clock"] >= 10
            assert store.verify("clean-child")["ok"] is True
        finally:
            store.close()
