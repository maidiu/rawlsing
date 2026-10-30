"""BP4R sourcefree repair court: episode origin/location + C9 writer versions."""
from __future__ import annotations

import json
import os
import sqlite3
import sys
from pathlib import Path

import pytest

C9_DIR = Path(os.environ.get("BP4R_C9_DIR", "/tmp/bp4r/c9/SOROK_PRODUCT_CONTROL_ROOM/V3_COURTS/SYN02/POST_R2_REVIEW/R3/C9_SQL"))
if str(C9_DIR) not in sys.path:
    sys.path.insert(0, str(C9_DIR))

import c9_actor_r3 as c9
from bp2p4.c12_guard import (
    GuardedC12Store,
    anchor_payload,
    check_c9_mirror_handshake,
    check_schema,
    two_store_readiness,
    verify_store,
)
from bp2p4.product import JoinedProduct
from bp4.canon import seal
from bp4.store import C12Store, GRADE, StoreRefusal


def _event(event_id: str, clock: int) -> dict:
    from bp4.canon import digest

    event = {"event_id": event_id, "clock": clock, "kind": "POSITION"}
    event["hash"] = digest(event)
    return event


def _seed_c12(path: Path) -> None:
    store = C12Store(path)
    store.create_root("root", clock=10, actor_ids=["A"], state={"world": 1})
    event = seal({
        "schema": "BP4_C12_WORLD_EVENT@1",
        "branch_id": "root",
        "event_id": "ev1",
        "clock": 10,
        "body": {},
        "grade": GRADE,
        "native": False,
    })
    store.append_world_event("root", event)
    store.record_perception("root", actor_id="A", event_id="ev1", clock=10,
                            channel="test")
    store.close()


def _expected_perception_hash(path: Path) -> str:
    first = c9.c12_fork_guard(path, "root")
    assert first["state"] == "FORK_HELD"
    assert first["code"] == "C12_BASE_PERCEPTION_IDENTITY_UNPROVEN"
    return first["base_perception_hash"]


def test_legitimate_episode_bearing_fork_passes(intact, tmp_path):
    product = JoinedProduct(tmp_path / "product", artifacts=intact)
    try:
        product.say("legitimate episode before fork")
        product.close()
        guarded = GuardedC12Store(tmp_path / "product" / "c12.sqlite")
        try:
            fork = guarded.fork("root", "alt")
            report = verify_store(guarded, "alt")
            assert report["ok"] is True, report
            assert report["content_ok"] is True
            assert report["fork_ok"] is True
            assert report["fork"]["status"] == "VERIFIED"
            rows = guarded.db.execute(
                "SELECT branch_id, body FROM episode WHERE branch_id='alt' ORDER BY seq"
            ).fetchall()
            assert len(rows) == 1
            assert rows[0][0] == "alt"  # current storage location
            assert json.loads(rows[0][1])["branch_id"] == "root"  # immutable origin
            assert guarded.shared_root_equal("root", "alt")["equal"] is True
            assert fork["root_hash"].startswith("BP4_C12_FORK_ROOT@2:")
        finally:
            guarded.close()
        reopened = GuardedC12Store(tmp_path / "product" / "c12.sqlite")
        try:
            cold = verify_store(reopened, "alt")
            assert cold["ok"] is True, cold
            row = reopened.db.execute(
                "SELECT branch_id, body FROM episode WHERE branch_id='alt' ORDER BY seq"
            ).fetchone()
            assert row[0] == "alt"
            assert json.loads(row[1])["branch_id"] == "root"
        finally:
            reopened.close()
    finally:
        try:
            product.close()
        except Exception:
            pass


def test_forged_branch_transplant_fails_at_same_read(intact, tmp_path):
    product = JoinedProduct(tmp_path / "product", artifacts=intact)
    try:
        product.say("seed")
        product.close()
        guarded = GuardedC12Store(tmp_path / "product" / "c12.sqlite")
        try:
            guarded.fork("root", "alt")
            guarded.append_episode("alt", actor_id="A", kind="SAY", clock=11,
                                   body={"local": "alt-only"})
            guarded.fork("root", "other")
            seq = guarded.db.execute(
                "SELECT seq FROM episode WHERE branch_id='alt' ORDER BY seq DESC LIMIT 1"
            ).fetchone()[0]
            guarded.db.execute("DROP TRIGGER episode_no_update")
            guarded.db.execute(
                "UPDATE episode SET branch_id='other' WHERE branch_id='alt' AND seq=?",
                (seq,))
            report = verify_store(guarded, "other")
            assert report["ok"] is False
            assert any("branch_id_origin_mismatch" in error
                       for error in report["errors"]), report
        finally:
            guarded.close()
    finally:
        try:
            product.close()
        except Exception:
            pass


def test_actual_c9_consumer_rejects_unsupported_writer_at_2(tmp_path):
    path = tmp_path / "c12.db"
    _seed_c12(path)
    expected = _expected_perception_hash(path)
    with sqlite3.connect(path) as db:
        db.execute("UPDATE meta SET value='BP4_C12_STORE@2' WHERE key='schema'")
        db.commit()
    guard = c9.c12_fork_guard(
        path, "root", expected_base_perception_hash=expected)
    assert guard["state"] == "FORK_HELD"
    assert guard["code"] == "C12_WRITER_SCHEMA_UNSUPPORTED"
    assert guard["writer_schema"] == "BP4_C12_STORE@2"

    mirror_meta = {"schema": "C12_ACTOR_MIRROR_R3@1",
                   "c12_source_domain": "BP4_C12_STORE@2"}
    helper = two_store_readiness(
        mirror_meta, "BP4_C12_STORE@2", watermark_state="CLEAN",
        outbox_state="ACKED")
    assert helper["ok"] is False
    assert helper["state"] == "SYNC_HELD"
    assert "c12_writer_schema_unsupported:BP4_C12_STORE@2" in helper["errors"]
    handshake = check_c9_mirror_handshake(mirror_meta, "BP4_C12_STORE@2")
    assert handshake["ok"] is False
    assert "c12_writer_schema_unsupported:BP4_C12_STORE@2" in handshake["errors"]


def test_c9_writer_schema_gate_source_severance_red_then_restored(tmp_path):
    path = tmp_path / "c12.db"
    _seed_c12(path)
    expected = _expected_perception_hash(path)
    with sqlite3.connect(path) as db:
        db.execute("UPDATE meta SET value='BP4_C12_STORE@2' WHERE key='schema'")
        db.commit()
    original = c9.SUPPORTED_C12_WRITER_SCHEMAS
    try:
        c9.SUPPORTED_C12_WRITER_SCHEMAS = frozenset(
            {"BP4_C12_STORE@1", "BP4_C12_STORE@2"})
        severed = c9.c12_fork_guard(
            path, "root", expected_base_perception_hash=expected)
        assert severed["state"] == "FORK_READY"
    finally:
        c9.SUPPORTED_C12_WRITER_SCHEMAS = original
    restored = c9.c12_fork_guard(
        path, "root", expected_base_perception_hash=expected)
    assert restored["state"] == "FORK_HELD"
    assert restored["code"] == "C12_WRITER_SCHEMA_UNSUPPORTED"


def test_supported_writer_still_reaches_ready_and_mirror_handshake(tmp_path):
    path = tmp_path / "c12.db"
    _seed_c12(path)
    expected = _expected_perception_hash(path)
    guard = c9.c12_fork_guard(
        path, "root", expected_base_perception_hash=expected)
    assert guard["state"] == "FORK_READY"
    mirror_meta = {"schema": "C12_ACTOR_MIRROR_R3@1",
                   "c12_source_domain": "BP4_C12_STORE@1"}
    assert check_c9_mirror_handshake(mirror_meta, "BP4_C12_STORE@1")["ok"] is True
    ready = two_store_readiness(
        mirror_meta, "BP4_C12_STORE@1", watermark_state="CLEAN",
        outbox_state="ACKED")
    assert ready["ok"] is True
    assert ready["state"] == "READY"


def test_cold_reopen_and_forced_schema_mismatch_fail_closed(tmp_path):
    path = tmp_path / "c12.db"
    _seed_c12(path)
    expected = _expected_perception_hash(path)
    assert c9.c12_fork_guard(
        path, "root", expected_base_perception_hash=expected)["state"] == "FORK_READY"
    with sqlite3.connect(path) as db:
        db.execute("UPDATE meta SET value='BP4_C12_STORE@2' WHERE key='schema'")
        db.commit()
    assert c9.c12_fork_guard(
        path, "root", expected_base_perception_hash=expected)["code"] == (
            "C12_WRITER_SCHEMA_UNSUPPORTED")
    guarded = GuardedC12Store(path)
    try:
        assert check_schema(guarded)["ok"] is False
        with pytest.raises(StoreRefusal) as error:
            guarded.fork("root", "alt")
        assert error.value.code == "SCHEMA_UNSUPPORTED"
    finally:
        guarded.close()


def test_mixed_writer_domain_is_refused(tmp_path):
    path = tmp_path / "c12.db"
    _seed_c12(path)
    expected = _expected_perception_hash(path)
    mirror_meta = {"schema": "C12_ACTOR_MIRROR_R3@1",
                   "c12_source_domain": "BP4_C12_STORE@2"}
    mixed = two_store_readiness(
        mirror_meta, "BP4_C12_STORE@1", watermark_state="CLEAN",
        outbox_state="ACKED")
    assert mixed["ok"] is False
    assert "c9_mirror_c12_domain_unsupported:BP4_C12_STORE@2" in mixed["errors"]
    assert c9.c12_fork_guard(
        path, "root", expected_base_perception_hash=expected)["state"] == "FORK_READY"


def test_residual_global_writer_clock_is_still_accepted_red(tmp_path):
    """Diagnostic RED: global writer chronology remains a separate HOLD."""
    path = tmp_path / "clock.db"
    store = GuardedC12Store(path)
    try:
        store.create_root("root", clock=10, actor_ids=["A"], state={"world": 1})
        store.append_world_event("root", _event("ev1", 10))
        store.record_perception("root", actor_id="A", event_id="ev1", clock=11,
                                channel="test")
        episode = store.append_episode(
            "root", actor_id="A", kind="SAY", clock=10, body={"x": 1})
        assert episode["clock"] == 10
        assert store.last_clock("root") == 10
        assert verify_store(store, "root")["ok"] is True
    finally:
        store.close()


def test_residual_anchor_actor_clock_coverage_remains_unbound_red(tmp_path):
    """Diagnostic RED: anchor payload still excludes branch actor/created clock."""
    path = tmp_path / "anchor.db"
    store = GuardedC12Store(path)
    try:
        store.create_root("root", clock=10, actor_ids=["A"], state={"world": 1})
        before = anchor_payload(store, "root")
        store.db.execute(
            "UPDATE branch SET actor_ids=?, created_clock=? WHERE branch_id='root'",
            (json.dumps(["A", "C"]), 999))
        after = anchor_payload(store, "root")
        assert after == before
        assert store.branch("root")["created_clock"] == 999
    finally:
        store.close()
