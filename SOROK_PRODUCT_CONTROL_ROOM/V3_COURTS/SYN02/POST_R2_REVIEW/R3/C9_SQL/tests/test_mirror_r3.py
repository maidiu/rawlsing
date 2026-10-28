"""C9-R3 outbox/C12-mirror ACK and watermark-held tests."""
from __future__ import annotations

import c9_actor_r3 as r3


def _publish(conn):
    return r3.publish(
        conn, actor="A", branch="b0", epoch="e0", event_key="event-mirror",
        attempt_no=1, idempotency_key="mirror-key", request_digest="mirror-digest",
        decision_kind="COMMITTED_CHANGE", legacy_receipt="legacy-A-b0",
        source_scope="source-mirror", settled_scope="settled-mirror",
        rule_t_status="COMMITTED_CHANGE", rule_t_hash="rule-t-test",
        readset_hash="readset-test",
    )


def _mirror_rows(mirror, receipt, projection):
    mirror.execute(
        "INSERT INTO mirror_branch VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        ("root", "A", "e0", None, "c12-root", None, 10, 0, None,
         None, None, 0, "ROOT_READY", r3.NOW),
    )
    mirror.execute(
        "INSERT INTO mirror_watermark VALUES (?,?,?,?,?,?)",
        ("root", 0, None, None, "CLEAN", r3.NOW),
    )
    mirror.execute(
        "INSERT INTO mirror_receipt VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        ("root", 1, receipt["receipt_hash"], receipt["version"],
         "COMMITTED_CHANGE", None, projection, r3.canon({"receipt": receipt["receipt_hash"]}),
         "c12-root", 10, "wr-A-b0", r3.NOW),
    )
    mirror.execute(
        "UPDATE mirror_watermark SET last_seq=1,last_receipt_hash=?,"
        "last_projection_hash=?,updated_admin_us=? WHERE c12_branch_id='root'",
        (receipt["receipt_hash"], projection, r3.NOW),
    )


def test_unmirrored_receipt_stays_sync_held_and_ack_is_idempotent(tmp_path):
    actor = r3.connect(tmp_path / "actor.sqlite")
    r3.seed(actor, "A", "b0", "e0", "root")
    receipt = _publish(actor)
    assert r3.outbox(actor, receipt["receipt_hash"]) == "PENDING"
    mirror = r3.mirror_connect(tmp_path / "mirror.sqlite")
    projection = r3.sha({"projection": receipt["receipt_hash"]})
    assert r3.mirror_ready(mirror, "root", 1, receipt["receipt_hash"], projection) is False
    versions = actor.execute("SELECT count(*) FROM actor_version").fetchone()[0]
    _mirror_rows(mirror, receipt, projection)
    assert r3.mirror_ready(mirror, "root", 1, receipt["receipt_hash"], projection) is True
    r3.mark_projected(actor, receipt["receipt_hash"], projection)
    r3.ack_outbox(actor, receipt["receipt_hash"], projection)
    r3.ack_outbox(actor, receipt["receipt_hash"], projection)
    assert r3.outbox(actor, receipt["receipt_hash"]) == "ACKED"
    assert actor.execute("SELECT count(*) FROM actor_version").fetchone()[0] == versions
    mirror.close()
    actor.close()


def test_held_watermark_is_never_clean(tmp_path):
    actor = r3.connect(tmp_path / "actor.sqlite")
    r3.seed(actor, "A", "b0", "e0", "root")
    receipt = _publish(actor)
    mirror = r3.mirror_connect(tmp_path / "mirror.sqlite")
    projection = r3.sha({"projection": receipt["receipt_hash"]})
    _mirror_rows(mirror, receipt, projection)
    mirror.execute("UPDATE mirror_watermark SET watermark_state='SYNC_HELD' WHERE c12_branch_id='root'")
    assert r3.mirror_ready(mirror, "root", 1, receipt["receipt_hash"], projection) is False
    mirror.execute("UPDATE mirror_watermark SET watermark_state='CLEAN' WHERE c12_branch_id='root'")
    mirror.close()
    actor.close()
