"""Focused candidate tests for C12 fork perception/root/ancestry and atomicity."""
from __future__ import annotations

import importlib.util
import sqlite3
import sys
from pathlib import Path

import pytest

SCRATCH = Path(__file__).resolve().parents[1]
CAND = SCRATCH / "candidate"
J = CAND / "WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1/vendor/j"
for path in (J / "candidate/vendor/bp4", J / "candidate/vendor/bp4/vendor"):
    sys.path.insert(0, str(path))

from bp4.canon import canonical, digest  # noqa: E402
from bp4.store import C12Store, StoreRefusal  # noqa: E402

SPEC = importlib.util.spec_from_file_location(
    "candidate_c12_integrity", J / "r26e/c12_integrity.py")
_C12 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(_C12)
QualifiedC12Store = _C12.QualifiedC12Store


def _event(event_id, clock):
    event = {"event_id": event_id, "clock": clock, "kind": "POSITION"}
    event["hash"] = digest(event)
    return event


def _seed(path, store_cls=C12Store):
    store = store_cls(path)
    store.create_root("root", clock=0, actor_ids=["A", "B"], state={"clock": 0})
    store.append_world_event("root", _event("event10", 10))
    store.checkpoint("root", 10, {"clock": 10})
    store.record_perception("root", actor_id="A", event_id="event10",
                            clock=10, channel="co_present")
    store.record_perception("root", actor_id="B", event_id="event10",
                            clock=11, channel="own_action")
    return store


def test_legitimate_fork_binds_perception_and_verifies(tmp_path):
    for cls in (C12Store, QualifiedC12Store):
        store = _seed(tmp_path / f"{cls.__name__}.sqlite", cls)
        try:
            before = store.perceptions("root")
            fork = store.fork("root", "alt")
            assert fork["fork_clock"] == 11
            assert fork["root_hash"].startswith("BP4_C12_FORK_ROOT@2:")
            assert store.perceptions("alt") == before
            assert store.verify("root")["ok"] is True
            assert store.verify("alt")["ok"] is True
            assert store.verify("alt")["fork"]["status"] == "VERIFIED"
        finally:
            store.close()


def test_same_count_substituted_perception_rejected(tmp_path):
    store = _seed(tmp_path / "sub.sqlite", QualifiedC12Store)
    try:
        store.fork("root", "alt")
        store.db.execute("DROP TRIGGER perception_no_update")
        store.db.execute(
            "UPDATE perception SET channel='substituted' "
            "WHERE branch_id='alt' AND seq=1")
        assert len(store.perceptions("alt")) == 2
        direct = store.verify("alt")
        assert direct["ok"] is False
        assert any("prefix_mismatch" in error for error in direct["errors"])
    finally:
        store.close()


def test_root_and_parent_metadata_tamper_rejected(tmp_path):
    store = _seed(tmp_path / "root_tamper.sqlite")
    try:
        store.fork("root", "alt")
        store.db.execute(
            "UPDATE branch SET root_hash=? WHERE branch_id='alt'",
            ("BP4_C12_FORK_ROOT@2:tampered",))
        result = store.verify("alt")
        assert result["ok"] is False
        assert any("root_hash_mismatch" in e for e in result["errors"])
    finally:
        store.close()

    store = _seed(tmp_path / "parent_tamper.sqlite")
    try:
        store.fork("root", "alt")
        store.db.execute(
            "UPDATE branch SET root_hash='tampered' WHERE branch_id='root'")
        result = store.verify("alt")
        assert result["ok"] is False
        assert any("root_hash_mismatch" in e for e in result["errors"])
    finally:
        store.close()


def test_legacy_root_is_held_not_certified(tmp_path):
    store = _seed(tmp_path / "legacy.sqlite")
    try:
        store.fork("root", "alt")
        legacy = digest({"parent": "root", "fork_clock": 11, "hashes": []})
        store.db.execute(
            "UPDATE branch SET root_hash=? WHERE branch_id='alt'", (legacy,))
        result = store.verify("alt")
        assert result["ok"] is False
        assert result["fork"]["status"] == "LEGACY_HELD"
        with pytest.raises(StoreRefusal) as exc:
            store.fork("alt", "grand")
        assert exc.value.code == "FORK_HELD"
        assert sorted(row["branch_id"] for row in store.branches()) == [
            "alt", "root"]
    finally:
        store.close()


def test_nested_cold_and_parent_suffix_isolation(tmp_path):
    path = tmp_path / "cold.sqlite"
    store = _seed(path)
    try:
        store.fork("root", "alt")
        store.append_world_event("root", _event("event20", 20))
        store.checkpoint("root", 20, {"clock": 20})
        store.record_perception("root", actor_id="A", event_id="event20",
                                clock=20, channel="co_present")
        store.append_world_event("alt", _event("event30", 30))
        store.checkpoint("alt", 30, {"clock": 30})
        store.fork("alt", "grand")
        assert "event20" not in {
            row["event_id"] for row in store.world_events("alt")}
        assert store.verify("root")["ok"] is True
        assert store.verify("alt")["ok"] is True
        assert store.verify("grand")["ok"] is True
    finally:
        store.close()

    reopened = C12Store(path)
    try:
        assert reopened.verify("grand")["ok"] is True
        assert reopened.branch("grand")["parent_branch_id"] == "alt"
        assert reopened.perceptions("grand")[:2] == [
            {"actor_id": "A", "event_id": "event10", "clock": 10,
             "channel": "co_present"},
            {"actor_id": "B", "event_id": "event10", "clock": 11,
             "channel": "own_action"},
        ]
    finally:
        reopened.close()


def test_partial_copy_failure_after_nonempty_table_rolls_back(tmp_path, monkeypatch):
    store = _seed(tmp_path / "failure.sqlite")
    try:
        calls = []
        copied = {}
        original = store._copy_fork_rows

        def fail_before_perception(table, new_branch_id, rows):
            calls.append(table)
            if table == "perception":
                copied["world"] = store.db.execute(
                    "SELECT count(*) FROM world_event WHERE branch_id=?",
                    (new_branch_id,)).fetchone()[0]
                raise RuntimeError("INJECTED_COPY_FAILURE")
            return original(table, new_branch_id, rows)

        monkeypatch.setattr(store, "_copy_fork_rows", fail_before_perception)
        with pytest.raises(RuntimeError):
            store.fork("root", "alt")
        assert calls == ["episode", "world_event", "perception"]
        assert copied["world"] > 0
        assert store._branch("alt") is None
        assert sorted(row["branch_id"] for row in store.branches()) == ["root"]
        for table in ("episode", "world_event", "perception", "checkpoint"):
            rows = store.db.execute(
                f"SELECT count(*) FROM {table} WHERE branch_id='alt'").fetchone()
            assert rows[0] == 0
        assert store.verify("root")["ok"] is True
    finally:
        store.close()


def test_second_connection_writer_during_capture_is_coherent(tmp_path, monkeypatch):
    path = tmp_path / "concurrent.sqlite"
    store = _seed(path)
    try:
        attempted = {}
        fired = []
        original_fork_rows = store._fork_rows

        def capture_with_writer(branch_id, table, limit=None):
            rows = original_fork_rows(branch_id, table, limit)
            if table == "world_event" and not fired:
                fired.append(True)
                writer = sqlite3.connect(
                    str(path), timeout=0.05, isolation_level=None)
                try:
                    writer.execute("BEGIN IMMEDIATE")
                    seq = writer.execute(
                        "SELECT coalesce(max(seq),-1)+1 FROM world_event "
                        "WHERE branch_id='root'").fetchone()[0]
                    event = _event("event20", 20)
                    writer.execute(
                        "INSERT INTO world_event VALUES (?,?,?,?,?,?)",
                        ("root", seq, "event20", 20, canonical(event),
                         event["hash"]))
                    seq = writer.execute(
                        "SELECT coalesce(max(seq),-1)+1 FROM perception "
                        "WHERE branch_id='root'").fetchone()[0]
                    writer.execute(
                        "INSERT INTO perception VALUES (?,?,?,?,?,?)",
                        ("root", seq, "A", "event20", 20, "co_present"))
                    writer.execute("COMMIT")
                    attempted["writer"] = "committed"
                except sqlite3.OperationalError as exc:
                    if writer.in_transaction:
                        writer.execute("ROLLBACK")
                    attempted["writer"] = "refused"
                    attempted["error"] = str(exc)
                finally:
                    writer.close()
            return rows

        monkeypatch.setattr(store, "_fork_rows", capture_with_writer)
        fork = store.fork("root", "alt")
        assert fired
        assert attempted.get("writer") in {"committed", "refused"}
        suffix = {
            "world": any(row["event_id"] == "event20"
                         for row in store.world_events("alt")),
            "perception": any(row["event_id"] == "event20"
                              for row in store.perceptions("alt")),
        }
        assert (all(suffix.values()) or not any(suffix.values()))
        if any(suffix.values()):
            assert fork["fork_clock"] == 20
        else:
            assert fork["fork_clock"] == 11
        assert store.verify("alt")["ok"] is True
        assert store.verify("root")["ok"] is True
    finally:
        store.close()


def test_outer_wrapper_savepoint_controls_inner_fork(tmp_path):
    store = _seed(tmp_path / "outer.sqlite")
    try:
        parent_before = store.branch("root")
        store.db.execute("SAVEPOINT outer_wrapper")
        store.fork("root", "kept")
        store.db.execute("RELEASE outer_wrapper")
        assert store.verify("kept")["ok"] is True

        store.db.execute("SAVEPOINT outer_wrapper_rollback")
        store.fork("root", "discarded")
        store.db.execute("ROLLBACK TO outer_wrapper_rollback")
        store.db.execute("RELEASE outer_wrapper_rollback")
        assert store._branch("discarded") is None
        assert store.branch("root") == parent_before
        for table in ("episode", "world_event", "perception", "checkpoint"):
            rows = store.db.execute(
                f"SELECT count(*) FROM {table} WHERE branch_id='discarded'").fetchone()
            assert rows[0] == 0
    finally:
        store.close()
