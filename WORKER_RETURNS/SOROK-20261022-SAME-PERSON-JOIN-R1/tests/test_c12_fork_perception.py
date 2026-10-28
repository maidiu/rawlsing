"""Focused regression: a fork keeps perceptions recorded after the last event/checkpoint."""
from __future__ import annotations

from joined.imports import install

install()

from bp4.store import C12Store  # noqa: E402


def _world_event(event_id: str, clock: int) -> dict:
    return {"event_id": event_id, "clock": clock, "kind": "POSITION",
            "hash": "TEST_ONLY_HASH_" + event_id}


def _seed(path):
    store = C12Store(path)
    store.create_root("root", clock=0, actor_ids=["A", "B"], state={"clock": 0})
    store.append_world_event("root", _world_event("event10", 10))
    store.checkpoint("root", 10, {"clock": 10})
    store.record_perception("root", actor_id="A", event_id="event10",
                            clock=10, channel="co_present")
    store.record_perception("root", actor_id="B", event_id="event10",
                            clock=11, channel="own_action")
    return store


def test_clock11_perception_survives_fork_after_clock10_cut(tmp_path):
    store = _seed(tmp_path / "c12.sqlite")
    try:
        assert store.last_clock("root") == 10
        parent = store.perceptions("root")
        assert [row["clock"] for row in parent] == [10, 11]

        fork = store.fork("root", "alt")

        assert fork["fork_clock"] == 11
        assert store.perceptions("alt") == parent
        assert [row["clock"] for row in store.perceptions("alt")] == [10, 11]
    finally:
        store.close()


def test_copied_perception_fields_survive_cold_reopen(tmp_path):
    path = tmp_path / "c12.sqlite"
    store = _seed(path)
    try:
        store.fork("root", "alt")
        copied = store.perceptions("alt")
        assert copied == [
            {"actor_id": "A", "event_id": "event10", "clock": 10,
             "channel": "co_present"},
            {"actor_id": "B", "event_id": "event10", "clock": 11,
             "channel": "own_action"},
        ]
    finally:
        store.close()

    reopened = C12Store(path)
    try:
        assert reopened.perceptions("alt") == copied
        assert reopened.branch("alt")["fork_clock"] == 11
    finally:
        reopened.close()


def test_parent_post_fork_activity_does_not_leak_to_child(tmp_path):
    store = _seed(tmp_path / "c12.sqlite")
    try:
        store.fork("root", "alt")
        child_before = {
            "episode": store.episodes("alt"),
            "world_event": store.world_events("alt"),
            "perception": store.perceptions("alt"),
            "checkpoint": store.checkpoints("alt"),
        }

        store.append_world_event("root", _world_event("event20", 20))
        store.record_perception("root", actor_id="A", event_id="event20",
                                clock=20, channel="co_present")
        store.checkpoint("root", 20, {"clock": 20})

        assert store.last_clock("root") == 20
        assert store.branch("alt")["fork_clock"] == 11
        assert store.episodes("alt") == child_before["episode"]
        assert store.world_events("alt") == child_before["world_event"]
        assert store.perceptions("alt") == child_before["perception"]
        assert store.checkpoints("alt") == child_before["checkpoint"]
        assert "event20" not in {
            row["event_id"] for row in store.perceptions("alt")}
    finally:
        store.close()
