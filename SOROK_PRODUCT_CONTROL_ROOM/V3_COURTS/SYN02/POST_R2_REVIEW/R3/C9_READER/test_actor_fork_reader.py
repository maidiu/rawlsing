"""Focused inherited-branch reads over real C9 candidate and repaired C12 source."""
from __future__ import annotations

import json
import os
from pathlib import Path
import sqlite3

import pytest

import actor_reader
from actor_reader import ReaderHeld, load_c12_source, load_candidate, read_actor_snapshot

SCRATCH = Path(__file__).resolve().parent
from test_actor_reader import SOURCE
C12_SOURCE = Path(os.environ.get(
    "C12_READER_SOURCE",
    "/Users/matthewsmith/Desktop/Rawlsing/rawlsing-join-e/WORKER_RETURNS/SOROK-20261022-SAME-PERSON-JOIN-R1"))


def _event(event_id, clock):
    event = {"event_id": event_id, "clock": clock, "kind": "POSITION"}
    event["hash"] = actor_reader.sha(event)
    return event


def _publish(candidate, obj, key, *, text="I received help", memory="ACTOR_ACCESSIBLE",
             held=False):
    obj.add_world_receipt(world_receipt_hash="world-" + key, world_event_id="event-" + key,
                          c8_branch_id="c8", c8_root_hash="root", c8_head_hash="head",
                          effective_us=10)
    common = dict(event_key=key, idempotency_key=key,
                  source_cut_hash=obj.source_cut_hash, source_scope_hash="scope",
                  settled_scope_hash="settled", world_receipt_hash="world-" + key,
                  memory_evidence=memory)
    if held:
        request = candidate.PublishRequest(
            **common, decision_kind="HELD_MISSING_RULE", actor_presence="NOT_PRESENT",
            actor_reception="NOT_WITNESSED")
    else:
        obj.add_rule(rule_hash="T-" + key, rule_kind="T", issuer_ref="TEST_ONLY",
                     source_cut_hash=obj.source_cut_hash)
        request = candidate.PublishRequest(
            **common, decision_kind="COMMITTED_CHANGE", rule_t_hash="T-" + key,
            rule_t_status="COMMITTED_CHANGE", evaluation_basis="ISSUED_RULE_T_EVALUATED",
            evaluated_readset_hash="readset",
            semantic_payload={"actor_surface": {"text": text}})
    return obj.publish(request)


def _perception_hash(conn, branch_id, limit=None):
    sql = ("SELECT seq,actor_id,event_id,clock,channel FROM perception "
           "WHERE branch_id=? ORDER BY seq")
    values = (branch_id,)
    if limit is not None:
        sql += " LIMIT ?"
        values += (limit,)
    previous = conn.row_factory
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(sql, values).fetchall()
    finally:
        conn.row_factory = previous
    return actor_reader._perception_rows_hash(rows)


def _read(c9_path, branch="alt", epoch="e-alt", c12=True, **overrides):
    arguments = dict(actor_id="A", branch_id=branch, branch_epoch=epoch,
                     source_cut="TEST_ONLY_SOURCE_CUT")
    arguments.update(overrides)
    if c12:
        arguments.update(c12_source=C12_SOURCE, c12_database=c9_path.with_suffix(".c12.sqlite"))
    return read_actor_snapshot(SOURCE, c9_path, **arguments)


def _fixture(tmp_path, child_cut="TEST_ONLY_SOURCE_CUT"):
    candidate = load_candidate(SOURCE)
    c12_mods = load_c12_source(C12_SOURCE)
    c9_path = tmp_path / "actor.sqlite"
    c12_path = c9_path.with_suffix(".c12.sqlite")
    c12 = c12_mods["store"].C12Store(c12_path)
    c12.create_root("c12-root", clock=0, actor_ids=["A", "B"], state={"clock": 0})
    c12.append_world_event("c12-root", _event("event-before-fork", 10))
    c12.checkpoint("c12-root", 10, {"clock": 10})
    c12.record_perception("c12-root", actor_id="B", event_id="event-before-fork",
                          clock=10, channel="own_action")
    c12.record_perception("c12-root", actor_id="A", event_id="event-before-fork",
                          clock=11, channel="co_present")
    parent = candidate.ActorAuthority(c9_path, actor_id="A")
    _publish(candidate, parent, "before-fork", text="I read the message.")
    _publish(candidate, parent, "hidden", text="HIDDEN_UNSEEN", memory="ACTOR_UNKNOWN",
             held=True)
    c12_child = c12.fork("c12-root", "c12-alt")
    prefix_hash = _perception_hash(c12.db, "c12-root")
    fork = parent.fork_branch(
        branch_id="alt", branch_epoch="e-alt",
        source_cut_hash=child_cut, source_root_hash=parent.source_root_hash,
        source_grant_hash="TEST_ONLY_SOURCE_GRANT", c12_branch_id="c12-alt",
        c12_root_hash=c12_child["root_hash"], c12_perception_hash=prefix_hash,
        c12_watermark=c12_child["fork_clock"])
    return candidate, c12, c12_path, c9_path, parent, fork, prefix_hash


def _close(*objects):
    for obj in objects:
        try:
            obj.conn.close()
        except Exception:
            pass


def test_inherited_nested_cold_read_and_parent_suffix_isolation(tmp_path):
    candidate, c12, c12_path, c9_path, parent, fork, _ = _fixture(tmp_path)
    child = candidate.ActorAuthority(c9_path, actor_id="A", branch_id="alt",
                                     branch_epoch="e-alt")
    try:
        before_c9 = "\n".join(sqlite3.connect(c9_path).iterdump())
        before_c12 = c12_path.read_bytes()
        first = _read(c9_path)
        assert "\n".join(sqlite3.connect(c9_path).iterdump()) == before_c9
        assert c12_path.read_bytes() == before_c12
        assert first.delivery_status == "SYNC_HELD"
        assert {"actor_id": "A", "event_id": "event-before-fork",
                "clock": 11, "channel": "co_present"} in c12.perceptions("c12-alt")
        assert [r.text for r in first.visible_records] == [
            "I read the message."]
        assert all("HIDDEN_UNSEEN" not in record.text
                   for record in first.visible_records)

        c12.append_world_event("c12-root", _event("event20", 20))
        c12.checkpoint("c12-root", 20, {"clock": 20})
        c12.record_perception("c12-root", actor_id="A", event_id="event20",
                              clock=20, channel="co_present")
        _publish(candidate, parent, "parent-later", text="PARENT_LATER")
        assert [r.text for r in _read(c9_path).visible_records] == [
            "I read the message."]

        _publish(candidate, child, "child-event", text="I practiced after the fork.")
        visible = _read(c9_path)
        assert [r.text for r in visible.visible_records] == [
            "I read the message.", "I practiced after the fork."]

        c12_grand = c12.fork("c12-alt", "c12-grand")
        prefix_hash = _perception_hash(c12.db, "c12-alt",
                                       c12.branch("c12-alt")["root_counts"]["perception"])
        child.fork_branch(
            branch_id="grand", branch_epoch="e-grand",
            source_cut_hash=child.source_cut_hash, source_root_hash=child.source_root_hash,
            source_grant_hash="TEST_ONLY_SOURCE_GRANT", c12_branch_id="c12-grand",
            c12_root_hash=c12_grand["root_hash"], c12_perception_hash=prefix_hash,
            c12_watermark=c12_grand["fork_clock"])
        grand = _read(c9_path, branch="grand", epoch="e-grand")
        assert [r.text for r in grand.visible_records] == [
            "I read the message.", "I practiced after the fork."]

        _publish(candidate, child, "child-later", text="CHILD_LATER")
        assert [r.text for r in _read(c9_path, branch="grand", epoch="e-grand").visible_records] == [
            "I read the message.", "I practiced after the fork."]
        assert all("PARENT_LATER" not in record.text
                   for record in grand.visible_records)
    finally:
        _close(c9_path, c12.db, parent, child)
        c12.close()

    cold = _read(c9_path, branch="grand", epoch="e-grand")
    assert [r.text for r in cold.visible_records] == [
        "I read the message.", "I practiced after the fork."]


def test_missing_c12_proof_keeps_fork_held_and_reads_are_write_free(tmp_path):
    candidate, c12, c12_path, c9_path, parent, fork, _ = _fixture(tmp_path)
    _close(parent)
    c12.close()
    before_c9 = "\n".join(sqlite3.connect(c9_path).iterdump())
    before_c12 = c12_path.read_bytes()
    try:
        with pytest.raises(ReaderHeld, match="FORK_HELD"):
            _read(c9_path, c12=False)
        assert "\n".join(sqlite3.connect(c9_path).iterdump()) == before_c9
        assert c12_path.read_bytes() == before_c12
    finally:
        pass


@pytest.mark.parametrize("field,value,error", [
    ("branch_epoch", "wrong-epoch", "ACTOR_BRANCH_EPOCH_MISMATCH"),
    ("source_cut", "WRONG_CUT", "ACTOR_SOURCE_CUT_MISMATCH"),
])
def test_wrong_actor_epoch_or_source_refuses(tmp_path, field, value, error):
    candidate, c12, c12_path, c9_path, parent, fork, _ = _fixture(tmp_path)
    _close(parent)
    c12.close()
    with pytest.raises(ReaderHeld, match=error):
        _read(c9_path, **{field: value})


@pytest.mark.parametrize("column,error", [
    ("fork_c12_root_hash", "C12_FORK_ROOT_MISMATCH"),
    ("fork_c12_perception_hash", "C12_INHERITED_PERCEPTION_HASH_MISMATCH"),
    ("fork_source_cut_hash", "C9_FORK_SOURCE_CUT_MISMATCH"),
])
def test_wrong_fork_metadata_refuses(tmp_path, column, error):
    candidate, c12, c12_path, c9_path, parent, fork, _ = _fixture(tmp_path)
    _close(parent)
    c12.close()
    db = sqlite3.connect(c9_path)
    db.execute("DROP TRIGGER actor_branch_no_update")
    db.execute(f"UPDATE actor_branch SET {column}='tampered' WHERE branch_id='alt'")
    db.commit()
    db.close()
    with pytest.raises(ReaderHeld, match=error):
        _read(c9_path)


def test_invalid_or_legacy_c12_root_refuses(tmp_path):
    candidate, c12, c12_path, c9_path, parent, fork, _ = _fixture(tmp_path)
    _close(parent)
    legacy = actor_reader.sha({"parent": "c12-root", "fork_clock": 11, "hashes": []})
    c12.db.execute("UPDATE branch SET root_hash=? WHERE branch_id='c12-alt'", (legacy,))
    c12.close()
    db = sqlite3.connect(c9_path)
    db.execute("DROP TRIGGER actor_branch_no_update")
    db.execute("UPDATE actor_branch SET fork_c12_root_hash=? WHERE branch_id='alt'", (legacy,))
    db.commit()
    db.close()
    with pytest.raises(ReaderHeld, match="C12_FORK_INTEGRITY_HELD"):
        _read(c9_path)


def test_child_new_source_cut_inherits_parent_frozen_prefix(tmp_path):
    candidate, c12, c12_path, c9_path, parent, fork, _ = _fixture(
        tmp_path, child_cut="CHILD_NEW_SOURCE_CUT")
    _close(parent)
    c12.close()
    snapshot = _read(c9_path, source_cut="CHILD_NEW_SOURCE_CUT")
    assert snapshot.source_cut == "CHILD_NEW_SOURCE_CUT"
    assert [record.text for record in snapshot.visible_records] == [
        "I read the message."]
    assert snapshot.delivery_status == "SYNC_HELD"


def test_genesis_v0_cannot_replace_inherited_branch(tmp_path):
    candidate, c12, c12_path, c9_path, parent, fork, _ = _fixture(tmp_path)
    _close(parent)
    c12.close()
    empty = actor_reader.sha({})
    genesis = actor_reader.sha({
        "schema": "C9_ACTOR_VERSION_R3@1", "actor": "A", "branch": "alt",
        "epoch": "e-alt", "version": 0, "kind": "GENESIS_VALID_EMPTY",
        "parent": None, "semantic": empty, "state": {}})
    db = sqlite3.connect(c9_path)
    db.execute("PRAGMA foreign_keys=OFF")
    db.execute("DROP TRIGGER actor_version_no_update")
    db.execute("DROP TRIGGER actor_version_no_delete")
    db.execute(
        "UPDATE actor_version SET version_kind='GENESIS_VALID_EMPTY', version_hash=?, "
        "parent_version_hash=NULL, semantic_hash=?, canonical_state_json='{}', "
        "state_grade='VALID_EMPTY', decision_receipt_hash=NULL "
        "WHERE actor_id='A' AND branch_id='alt' AND version_no=0",
        (genesis, empty))
    db.execute(
        "UPDATE actor_head SET head_version_hash=?, head_semantic_hash=? "
        "WHERE actor_id='A' AND branch_id='alt'", (genesis, empty))
    db.commit()
    db.close()
    with pytest.raises(ReaderHeld, match="GENESIS_ANCESTRY_MISMATCH"):
        _read(c9_path)


def test_missing_child_in_valid_c12_database_is_typed_hold_and_cli_exit2(tmp_path):
    import subprocess
    import sys
    candidate, c12, c12_path, c9_path, parent, fork, _ = _fixture(tmp_path)
    _close(parent)
    c12.close()
    wrong_path = tmp_path / "wrong-valid-c12.sqlite"
    wrong = load_c12_source(C12_SOURCE)["store"].C12Store(wrong_path)
    wrong.create_root("c12-root", clock=0, actor_ids=["A", "B"],
                      state={"clock": 0})
    wrong.close()
    with pytest.raises(ReaderHeld, match="C12_FORK_BRANCH_MISSING"):
        read_actor_snapshot(
            SOURCE, c9_path, actor_id="A", branch_id="alt", branch_epoch="e-alt",
            source_cut="TEST_ONLY_SOURCE_CUT", c12_source=C12_SOURCE,
            c12_database=wrong_path)
    command = [
        sys.executable, "-B", str(SCRATCH / "actor_reader.py"),
        "--source", str(SOURCE), "--database", str(c9_path),
        "--actor", "A", "--branch", "alt", "--epoch", "e-alt",
        "--source-cut", "TEST_ONLY_SOURCE_CUT",
        "--c12-source", str(C12_SOURCE), "--c12-database", str(wrong_path)]
    result = subprocess.run(command, capture_output=True, text=True)
    assert result.returncode == 2
    assert result.stdout == ""
    assert result.stderr == "ACTOR_SURFACE_HELD\n"


def test_c12_source_hash_and_foreign_cache_refuse(tmp_path):
    candidate, c12, c12_path, c9_path, parent, fork, _ = _fixture(tmp_path)
    _close(parent)
    c12.close()
    with pytest.raises(ReaderHeld, match="C12_SOURCE_CHANGED_BEFORE_IMPORT"):
        read_actor_snapshot(SOURCE, c9_path, actor_id="A", branch_id="alt",
                            branch_epoch="e-alt", source_cut="TEST_ONLY_SOURCE_CUT",
                            c12_source=tmp_path / "absent", c12_database=c12_path)
    import sys
    import types
    foreign = types.ModuleType("bp4.store")
    foreign.__file__ = str(tmp_path / "foreign-store.py")
    saved = sys.modules.get("bp4.store")
    sys.modules["bp4.store"] = foreign
    try:
        with pytest.raises(ReaderHeld, match="C12_FOREIGN_CACHE_HELD"):
            _read(c9_path)
    finally:
        if saved is None:
            sys.modules.pop("bp4.store", None)
        else:
            sys.modules["bp4.store"] = saved
