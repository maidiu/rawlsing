"""C9-R3 sourcefree actor-helper idempotency, status and recovery tests."""
from __future__ import annotations

import sqlite3

import pytest

import c9_actor_r3 as r3


def _final(conn, *, key="key-1", digest="digest-1", event="event-1", attempt=1,
           actor="A", branch="b0", epoch="e0", target=None, prior=None,
           decision="COMMITTED_CHANGE", **extra):
    return r3.publish(
        conn,
        actor=actor,
        branch=branch,
        epoch=epoch,
        event_key=event,
        attempt_no=attempt,
        idempotency_key=key,
        request_digest=digest,
        decision_kind=decision,
        legacy_receipt=f"legacy-{actor}-{branch}",
        source_scope="source-test",
        settled_scope="settled-test",
        rule_t_status=decision,
        rule_t_hash="rule-t-test",
        readset_hash="readset-test",
        target_id=target,
        target_hash="target-hash" if target else None,
        prior_attempt_id=prior,
        **extra,
    )


def _counts(conn):
    return {
        "versions": conn.execute("SELECT count(*) FROM actor_version").fetchone()[0],
        "receipts": conn.execute("SELECT count(*) FROM decision_receipt").fetchone()[0],
        "attempts": conn.execute("SELECT count(*) FROM event_attempt").fetchone()[0],
        "outbox": conn.execute("SELECT count(*) FROM projection_outbox").fetchone()[0],
    }


def test_same_key_same_digest_returns_exact_original_without_extra_rows(tmp_path):
    conn = r3.connect(tmp_path / "actor.sqlite")
    r3.seed(conn, "A", "b0", "e0", "root")
    first = _final(conn)
    assert first["replay"] is False
    before = _counts(conn)
    head_before = r3.head(conn, "A", "b0")
    second = _final(conn)
    assert second["replay"] is True
    assert second["receipt_hash"] == first["receipt_hash"]
    assert second["seq"] == first["seq"]
    assert second["version"] == first["version"]
    assert _counts(conn) == before
    assert r3.head(conn, "A", "b0") == head_before
    conn.close()


def test_same_key_changed_digest_is_typed_conflict_without_mutation(tmp_path):
    conn = r3.connect(tmp_path / "actor.sqlite")
    r3.seed(conn, "A", "b0", "e0", "root")
    _final(conn)
    before = _counts(conn)
    with pytest.raises(r3.ActorR3Error) as exc:
        _final(conn, digest="changed-digest")
    assert exc.value.code == "IDEMPOTENCY_PAYLOAD_CONFLICT"
    assert _counts(conn) == before
    conn.close()


def test_finalized_event_cannot_rerun_rule_t(tmp_path):
    conn = r3.connect(tmp_path / "actor.sqlite")
    r3.seed(conn, "A", "b0", "e0", "root")
    _final(conn)
    with pytest.raises(r3.ActorR3Error) as exc:
        _final(conn, key="key-new", digest="digest-new", attempt=2)
    assert exc.value.code == "EVENT_ALREADY_FINALIZED"
    conn.close()


def test_held_cannot_carry_committed_rule_t_axis(tmp_path):
    conn = r3.connect(tmp_path / "actor.sqlite")
    r3.seed(conn, "A", "b0", "e0", "root")
    with pytest.raises(r3.ActorR3Error) as exc:
        r3.publish(
            conn, actor="A", branch="b0", epoch="e0", event_key="event-held",
            attempt_no=1, idempotency_key="held-key", request_digest="held-digest",
            decision_kind="HELD_MISSING_RULE", legacy_receipt="legacy-A-b0",
            source_scope="source-held", settled_scope="settled-held",
            rule_t_status="COMMITTED_CHANGE", sci05_status="HELD",
        )
    assert exc.value.code == "STATUS_AXIS_CONFLICT"
    assert _counts(conn)["receipts"] == 0
    conn.close()


def test_true_nochange_requires_explicit_rule_and_stays_semantically_equal(tmp_path):
    conn = r3.connect(tmp_path / "actor.sqlite")
    r3.seed(conn, "A", "b0", "e0", "root")
    with pytest.raises(r3.ActorR3Error) as exc:
        r3.publish(
            conn, actor="A", branch="b0", epoch="e0", event_key="event-nochange",
            attempt_no=1, idempotency_key="nc-bad", request_digest="nc-bad",
            decision_kind="TRUE_NO_CHANGE_EVALUATED", legacy_receipt="legacy-A-b0",
            source_scope="source-nc", settled_scope="settled-nc",
            rule_t_status="TRUE_NO_CHANGE_EVALUATED",
        )
    assert exc.value.code == "RULE_T_MISSING"
    result = _final(conn, key="nc-key", digest="nc-digest", event="event-nochange",
                    decision="TRUE_NO_CHANGE_EVALUATED")
    row = conn.execute(
        "SELECT before_semantic_hash,after_semantic_hash,rule_t_hash,evaluated_readset_hash "
        "FROM decision_receipt WHERE receipt_hash=?", (result["receipt_hash"],)
    ).fetchone()
    assert row[0] == row[1]
    assert row[2] == "rule-t-test" and row[3] == "readset-test"
    conn.close()


def test_held_requalification_preserves_old_receipt_and_links_prior_attempt(tmp_path):
    conn = r3.connect(tmp_path / "actor.sqlite")
    r3.seed(conn, "A", "b0", "e0", "root")
    held = r3.publish(
        conn, actor="A", branch="b0", epoch="e0", event_key="event-requal",
        attempt_no=1, idempotency_key="h1", request_digest="h1-digest",
        decision_kind="HELD_MISSING_RULE", legacy_receipt="legacy-A-b0",
        source_scope="source-h1", settled_scope="settled-h1",
        rule_t_status="HELD_MISSING_RULE", sci05_status="HELD",
    )
    old_row = conn.execute(
        "SELECT canonical_receipt_json FROM decision_receipt WHERE receipt_hash=?", (held["receipt_hash"],)
    ).fetchone()
    final = _final(conn, key="h2", digest="h2-digest", event="event-requal",
                   attempt=2, decision="TRUE_NO_CHANGE_EVALUATED")
    assert tuple(conn.execute(
        "SELECT attempt_state,prior_attempt_id FROM event_attempt "
        "WHERE idempotency_key='h1'"
    ).fetchone()) == ("HELD", None) if False else tuple(conn.execute(
        "SELECT attempt_state,prior_attempt_id FROM event_attempt "
        "WHERE idempotency_key='h1'"
    ).fetchone()) == ("HELD", None)
    assert conn.execute(
        "SELECT prior_attempt_id FROM event_attempt WHERE idempotency_key='h2'"
    ).fetchone()[0] == f"attempt-A-b0-event-requal-1"
    assert conn.execute(
        "SELECT canonical_receipt_json FROM decision_receipt WHERE receipt_hash=?", (held["receipt_hash"],)
    ).fetchone() == old_row
    assert final["version"] is not None
    with pytest.raises(r3.ActorR3Error) as exc:
        _final(conn, key="h3", digest="h3-digest", event="event-requal", attempt=3)
    assert exc.value.code == "EVENT_ALREADY_FINALIZED"
    conn.close()


def test_two_actors_same_local_target_and_stale_cas(tmp_path):
    conn = r3.connect(tmp_path / "actor.sqlite")
    r3.seed(conn, "A", "b0", "e0", "root")
    r3.seed(conn, "B", "b0", "e0", "root")
    _final(conn, actor="A", key="a-key", digest="a-digest", event="a-event",
           target="target-same")
    _final(conn, actor="B", key="b-key", digest="b-digest", event="b-event",
           target="target-same")
    assert conn.execute(
        "SELECT count(*) FROM actor_target WHERE target_id='target-same'"
    ).fetchone()[0] == 2
    stale = (0, "stale", "stale", 0, 0)
    with pytest.raises(r3.ActorR3Error) as exc:
        _final(conn, actor="A", key="a-stale", digest="a-st", event="a-stale",
               target="stale-target", expected_head=stale)
    assert exc.value.code == "STALE_ACTOR_PARENT"
    assert r3.head(conn, "A", "b0")[0] == 1
    conn.close()


def test_rollback_leaves_no_ghost_version_receipt_or_outbox(tmp_path):
    conn = r3.connect(tmp_path / "actor.sqlite")
    r3.seed(conn, "A", "b0", "e0", "root")
    before = _counts(conn)
    with pytest.raises(r3.ActorR3Error) as exc:
        r3.publish(
            conn, actor="A", branch="b0", epoch="e0", event_key="ghost",
            attempt_no=1, idempotency_key="ghost-key", request_digest="ghost-digest",
            decision_kind="COMMITTED_CHANGE", legacy_receipt="legacy-A-b0",
            source_scope="source-ghost", settled_scope="settled-ghost",
            rule_t_status="COMMITTED_CHANGE", rule_t_hash="rule-t-test",
            readset_hash="readset-test", target_id="ghost-target",
        )
    assert exc.value.code == "TARGET_HASH_REQUIRED"
    assert _counts(conn) == before
    assert r3.head(conn, "A", "b0") == (0, r3.sha({"actor": "A", "branch": "b0", "epoch": "e0", "version": 0}), r3.sha({}), 0, 0)
    conn.close()


def test_source_change_replay_is_exact_or_typed_conflict(tmp_path):
    conn = r3.connect(tmp_path / "actor.sqlite")
    r3.seed(conn, "A", "b0", "e0", "root")
    held = r3.publish(
        conn, actor="A", branch="b0", epoch="e0", event_key="event-source",
        attempt_no=1, idempotency_key="source-key", request_digest="source-digest",
        decision_kind="HELD_MISSING_RULE", legacy_receipt="legacy-A-b0",
        source_scope="source-v1", settled_scope="settled-v1",
        rule_t_status="HELD_MISSING_RULE", sci05_status="HELD",
    )
    replay = r3.publish(
        conn, actor="A", branch="b0", epoch="e0", event_key="event-source",
        attempt_no=1, idempotency_key="source-key", request_digest="source-digest",
        decision_kind="HELD_MISSING_RULE", legacy_receipt="legacy-A-b0",
        source_scope="source-v1", settled_scope="settled-v1",
        rule_t_status="HELD_MISSING_RULE", sci05_status="HELD",
    )
    assert replay["receipt_hash"] == held["receipt_hash"] and replay["replay"] is True
    with pytest.raises(r3.ActorR3Error) as exc:
        r3.publish(
            conn, actor="A", branch="b0", epoch="e0", event_key="event-source",
            attempt_no=1, idempotency_key="source-key", request_digest="source-digest-v2",
            decision_kind="HELD_MISSING_RULE", legacy_receipt="legacy-A-b0",
            source_scope="source-v2", settled_scope="settled-v2",
            rule_t_status="HELD_MISSING_RULE", sci05_status="HELD",
        )
    assert exc.value.code == "IDEMPOTENCY_PAYLOAD_CONFLICT"
    conn.close()


def test_outbox_projected_acked_is_idempotent_without_new_version(tmp_path):
    conn = r3.connect(tmp_path / "actor.sqlite")
    r3.seed(conn, "A", "b0", "e0", "root")
    first = _final(conn)
    assert r3.outbox(conn, first["receipt_hash"]) == "PENDING"
    versions = _counts(conn)["versions"]
    projection = r3.sha({"projection": first["receipt_hash"]})
    r3.mark_projected(conn, first["receipt_hash"], projection)
    assert r3.outbox(conn, first["receipt_hash"]) == "PROJECTED"
    r3.ack_outbox(conn, first["receipt_hash"], projection)
    r3.ack_outbox(conn, first["receipt_hash"], projection)
    assert r3.outbox(conn, first["receipt_hash"]) == "ACKED"
    assert _counts(conn)["versions"] == versions
    with pytest.raises(r3.ActorR3Error) as exc:
        r3.ack_outbox(conn, first["receipt_hash"], "different-projection")
    assert exc.value.code == "OUTBOX_ACK_CONFLICT"
    conn.close()


def test_world_occurred_actor_unseen_is_held_not_true_nochange(tmp_path):
    conn = r3.connect(tmp_path / "actor.sqlite")
    r3.seed(conn, "A", "b0", "e0", "root")
    result = r3.publish(
        conn, actor="A", branch="b0", epoch="e0", event_key="unseen-care",
        attempt_no=1, idempotency_key="unseen-key", request_digest="unseen-digest",
        decision_kind="HELD_MISSING_RULE", legacy_receipt="legacy-A-b0",
        source_scope="source-unseen", settled_scope="settled-unseen",
        world_occurrence="OCCURRED", actor_presence="NOT_PRESENT",
        actor_reception="NOT_WITNESSED", rule_t_status="HELD_MISSING_RULE",
        sci05_status="HELD",
    )
    row = conn.execute(
        "SELECT decision_kind,world_occurrence,actor_presence,actor_reception,"
        "rule_t_status,result_version_hash FROM decision_receipt WHERE receipt_hash=?",
        (result["receipt_hash"],),
    ).fetchone()
    assert tuple(row) == (
        "HELD_MISSING_RULE", "OCCURRED", "NOT_PRESENT", "NOT_WITNESSED",
        "HELD_MISSING_RULE", None,
    )
    assert r3.head(conn, "A", "b0")[0] == 0
    conn.close()


def test_two_connection_cas_loser_is_stale_not_duplicate(tmp_path):
    path = tmp_path / "actor.sqlite"
    first = r3.connect(path)
    second = r3.connect(path)
    r3.seed(first, "A", "b0", "e0", "root")
    stale = r3.head(first, "A", "b0")
    _final(first, key="winner", digest="winner-digest", event="winner")
    with pytest.raises(r3.ActorR3Error) as exc:
        _final(second, key="loser", digest="loser-digest", event="loser",
               expected_head=stale)
    assert exc.value.code == "STALE_ACTOR_PARENT"
    assert second.execute("SELECT count(*) FROM event_attempt WHERE idempotency_key='loser'").fetchone()[0] == 0
    first.close()
    second.close()
