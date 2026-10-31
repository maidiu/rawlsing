"""R2 sourcefree C9/C12 compatibility and fault/restore tests.

Run from the candidate directory with the BP2P4J return tree on PYTHONPATH.
The candidate C12 guard imports the original BP4 store; no original source file
is modified.
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

import c9_actor_r3 as c9
from c12_guard import (
    GuardedC12Store, anchor_payload, check_anchor, verify_store,
)
from bp4.canon import digest, seal
from bp4.store import C12Store, GRADE, StoreRefusal

CUT = "1998-11-20T09:00:00Z"


def _event(event_id: str, clock: int) -> dict:
    event = {"event_id": event_id, "clock": clock, "kind": "POSITION"}
    event["hash"] = digest(event)
    return event


def _seed_c12(path: Path) -> None:
    store = C12Store(path)
    store.create_root("root", clock=10, actor_ids=["A"], state={"world": 1})
    store.append_world_event("root", _event("ev1", 10))
    store.record_perception("root", actor_id="A", event_id="ev1", clock=10,
                            channel="test")
    store.close()


def _held_request(a, world, *, key="k1", event="e1"):
    return c9.PublishRequest(
        event_key=event,
        idempotency_key=key,
        decision_kind="HELD_MISSING_RULE",
        source_cut_hash=a.source_cut_hash,
        source_scope_hash="source-scope",
        settled_scope_hash="settled-scope",
        world_receipt_hash=world,
    )


def _c9_with_held(tmp_path: Path):
    a = c9.ActorAuthority(tmp_path / "actor.db", actor_id="A")
    a.add_world_receipt(
        world_receipt_hash="w1", world_event_id="event-w1",
        c8_branch_id="c8-branch", c8_root_hash="c8-root",
        c8_head_hash="c8-head", effective_us=10)
    receipt = a.publish(_held_request(a, "w1"))
    return a, receipt


def test_intact_c12_append_fork_cold_and_c9_genesis(tmp_path):
    c12 = tmp_path / "c12.db"
    _seed_c12(c12)
    store = GuardedC12Store(c12)
    try:
        store.append_episode("root", actor_id="A", kind="SAY", clock=10,
                             body={"x": 1})
        store.fork("root", "alt")
        assert verify_store(store, "alt")["ok"] is True
    finally:
        store.close()
    reopened = GuardedC12Store(c12)
    try:
        report = verify_store(reopened, "alt")
        assert report["ok"] is True
        row = reopened.db.execute(
            "SELECT branch_id, body FROM episode WHERE branch_id='alt' ORDER BY seq"
        ).fetchone()
        assert row[0] == "alt"
        assert json.loads(row[1])["branch_id"] == "root"
    finally:
        reopened.close()

    a = c9.ActorAuthority(tmp_path / "actor.db", actor_id="A")
    from c9c12_reader import read_actor_snapshot, read_composite
    snapshot = read_actor_snapshot(a.path, actor_id="A")
    assert snapshot["status"] == "ACTOR_SNAPSHOT_OK"
    assert snapshot["version_kind"] == "GENESIS_VALID_EMPTY"
    composite = read_composite(a.path, c12, actor_id="A", c12_branch_id="alt")
    assert composite["status"] == "COMPOSITE_OK__EXTERNAL_ANCHOR_REQUIRED"
    assert composite["c12"]["anchor_status"]["code"] == "OWNER_ANCHOR_REQUIRED"


def test_writer_clock_inversion_is_refused(tmp_path):
    path = tmp_path / "clock.db"
    store = GuardedC12Store(path)
    try:
        store.create_root("root", clock=10, actor_ids=["A"], state={"world": 1})
        store.append_world_event("root", _event("ev1", 10))
        store.record_perception("root", actor_id="A", event_id="ev1", clock=11,
                                channel="test")
        with pytest.raises(StoreRefusal) as error:
            store.append_episode("root", actor_id="A", kind="SAY", clock=10,
                                 body={"x": 1})
        assert error.value.code == "NON_MONOTONIC_GLOBAL_CLOCK"
    finally:
        store.close()


def test_anchor_binds_actor_and_created_clock(tmp_path):
    path = tmp_path / "anchor.db"
    store = GuardedC12Store(path)
    try:
        store.create_root("root", clock=10, actor_ids=["A"], state={"world": 1})
        before = anchor_payload(store, "root")
        store.db.execute(
            "UPDATE branch SET actor_ids=?, created_clock=? WHERE branch_id='root'",
            (json.dumps(["A", "C"]), 999))
        after = anchor_payload(store, "root")
        assert after != before
        assert after["branch_identity"]["actor_ids"] == ["A", "C"]
        assert after["branch_identity"]["created_clock"] == 999
        check = check_anchor(None, after, None)
        assert check["code"] == "OWNER_ANCHOR_REQUIRED"
    finally:
        store.close()


def test_writer_version_2_and_wrong_parent_are_refused(tmp_path):
    path = tmp_path / "version.db"
    _seed_c12(path)
    first = c9.c12_fork_guard(path, "root")
    assert first["state"] == "FORK_HELD"
    assert first["code"] == "C12_BASE_PERCEPTION_IDENTITY_UNPROVEN"
    with sqlite3.connect(path) as db:
        db.execute("UPDATE meta SET value='BP4_C12_STORE@2' WHERE key='schema'")
        db.commit()
    assert c9.c12_fork_guard(path, "root")["code"] == "C12_WRITER_SCHEMA_UNSUPPORTED"
    store = GuardedC12Store(path)
    try:
        with pytest.raises(StoreRefusal) as error:
            store.fork("root", "alt")
        assert error.value.code == "SCHEMA_UNSUPPORTED"
        with pytest.raises(StoreRefusal):
            store.fork("missing", "alt2")
    finally:
        store.close()


def test_forged_child_transplant_and_restore(tmp_path):
    path = tmp_path / "fork.db"
    _seed_c12(path)
    store = GuardedC12Store(path)
    try:
        store.append_episode("root", actor_id="A", kind="SAY", clock=10, body={"x": 1})
        store.fork("root", "alt")
        store.fork("root", "other")
        store.append_episode("alt", actor_id="A", kind="SAY", clock=11, body={"local": True})
        store.db.execute("DROP TRIGGER episode_no_update")
        store.db.execute("UPDATE episode SET branch_id='other' WHERE branch_id='alt' AND seq=1")
        assert verify_store(store, "other")["ok"] is False
        store.db.execute("UPDATE episode SET branch_id='alt' WHERE branch_id='other' AND seq=1")
        assert verify_store(store, "alt")["ok"] is True
    finally:
        store.close()


def test_c9_missing_c8_receipt_and_outbox_missing(tmp_path):
    a = c9.ActorAuthority(tmp_path / "actor.db", actor_id="A")
    with pytest.raises(c9.Refusal):
        a.publish(_held_request(a, "does-not-exist"))
    a, receipt = _c9_with_held(tmp_path)
    from c9c12_reader import read_actor_snapshot
    with pytest.raises(Exception) as error:
        read_actor_snapshot(a.path, actor_id="A")
    assert getattr(error.value, "code", "") == "C9_OUTBOX_HELD"
    row = a.conn.execute("SELECT * FROM projection_outbox WHERE receipt_hash=?",
                         (receipt["receipt_hash"],)).fetchone()
    columns = [r[1] for r in a.conn.execute("PRAGMA table_info(projection_outbox)")]
    a.conn.execute("DELETE FROM projection_outbox WHERE receipt_hash=?",
                   (receipt["receipt_hash"],))
    a.conn.commit()
    with pytest.raises(Exception) as error:
        read_actor_snapshot(a.path, actor_id="A")
    assert getattr(error.value, "code", "") == "C9_OUTBOX_MISSING"
    a.conn.execute(
        "INSERT INTO projection_outbox (" + ",".join(columns) + ") VALUES (" +
        ",".join("?" for _ in columns) + ")", tuple(row))
    a.conn.commit()
    # The restored row is the exact original PENDING row; the reader still
    # reports the typed outbox hold, not a fabricated ACK.
    with pytest.raises(Exception) as error:
        read_actor_snapshot(a.path, actor_id="A")
    assert getattr(error.value, "code", "") == "C9_OUTBOX_HELD"
