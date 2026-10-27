#!/usr/bin/env python3
"""TEST_ONLY sourcefree probe for the proposed RP0-R2 actor authority DDL."""
from __future__ import annotations

import hashlib
import json
import sqlite3
import tempfile
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
SCHEMA = HERE / "schema_actor.sql"
NOW = 1_780_000_000_000_000


def canon(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha(value: Any) -> str:
    return hashlib.sha256(canon(value).encode("utf8")).hexdigest()


def connect(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(path), isolation_level=None)
    conn.executescript(SCHEMA.read_text(encoding="utf8"))
    return conn


def seed(conn: sqlite3.Connection, actor: str, branch: str, epoch: str, c12: str) -> None:
    conn.execute(
        "INSERT INTO actor_branch VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (actor, branch, epoch, None, None, None, None, None, None, None, None,
         "TEST_ONLY_SOURCE_GRANT", c12, NOW),
    )
    zero = sha({"actor": actor, "branch": branch, "epoch": epoch, "version": 0})
    conn.execute(
        "INSERT INTO actor_version VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (actor, branch, epoch, 0, "GENESIS_VALID_EMPTY", zero, None,
         sha({}), "{}", "VALID_EMPTY", "TEST_ONLY_SOURCE_CUT", None, None, NOW),
    )
    conn.execute(
        "INSERT INTO actor_head VALUES (?,?,?,?,?,?,?,?,?)",
        (actor, branch, epoch, 0, zero, sha({}), 0, 0, NOW),
    )
    conn.execute(
        "INSERT INTO world_receipt VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (f"wr-{actor}-{branch}", f"we-{actor}-{branch}", f"c8-{actor}",
         "c8root", "c8head", None, NOW, "TEST_ONLY_C8_OWNER",
         "TEST_ONLY_SOURCEFREE", "TEST_ONLY_SOURCE_CUT", sha({"world": 1}),
         canon({"world": 1}), NOW),
    )
    legacy = f"legacy-{actor}-{branch}"
    conn.execute(
        "INSERT INTO legacy_bridge VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        (legacy, "C9P_CANDIDATE_TRANSACTION@1", f"ev-{actor}-{branch}",
         f"response-{actor}-{branch}", "NO_CHANGE", "NO_PROPOSAL",
         "before", "after", "legacy-domain", canon({"legacy": legacy}), NOW),
    )


def head(conn: sqlite3.Connection, actor: str, branch: str) -> tuple:
    return conn.execute(
        "SELECT head_version_no,head_version_hash,head_semantic_hash,"
        "last_receipt_seq,last_finalized_seq FROM actor_head "
        "WHERE actor_id=? AND branch_id=?", (actor, branch)
    ).fetchone()


def publish(
    conn: sqlite3.Connection,
    *,
    actor: str,
    branch: str,
    epoch: str,
    event_key: str,
    attempt_no: int,
    idempotency_key: str,
    request_digest: str,
    decision_kind: str,
    legacy_receipt: str,
    source_scope: str,
    settled_scope: str,
    source_status: str = "QUALIFIED",
    world_occurrence: str = "OCCURRED",
    actor_presence: str = "CO_PRESENT",
    actor_reception: str = "RECEIVED",
    rule_a_status: str = "APPLIED_WITH_RESPONSE",
    rule_t_status: str = "COMMITTED_CHANGE",
    actor_state_status: str = "VERSIONED_PRESENT",
    memory_evidence: str = "ACTOR_ACCESSIBLE",
    sci05_status: str = "ADMITTED",
    sci05_certificate: str | None = None,
    target_id: str | None = None,
    target_hash: str | None = None,
    expected_head: tuple | None = None,
) -> dict:
    final = decision_kind in ("COMMITTED_CHANGE", "TRUE_NO_CHANGE_EVALUATED")
    if sci05_status in ("DENIED", "HELD", "INTEGRITY_FAILED") and final:
        raise RuntimeError("SCI05_DENIED_CANNOT_FINALIZE")
    if sci05_status in ("DENIED", "HELD", "INTEGRITY_FAILED") and sci05_certificate:
        raise RuntimeError("SCI05_DENIED_WITH_CERTIFICATE_INVALID")
    old = head(conn, actor, branch)
    if expected_head is not None and tuple(old) != tuple(expected_head):
        raise RuntimeError("STALE_ACTOR_PARENT")
    seq = int(old[3]) + 1
    before_version = str(old[1])
    before_semantic = str(old[2])
    after_semantic = sha({"actor": actor, "event": event_key, "seq": seq}) if final else None
    if decision_kind == "TRUE_NO_CHANGE_EVALUATED":
        after_semantic = before_semantic
    result_version = None
    if final:
        result_version = sha({
            "actor": actor, "branch": branch, "epoch": epoch, "seq": seq,
            "parent": before_version, "semantic": after_semantic,
            "kind": decision_kind,
        })
    receipt_body = {
        "actor": actor, "branch": branch, "epoch": epoch, "seq": seq,
        "event": event_key, "attempt": attempt_no, "decision": decision_kind,
        "before_version": before_version, "result_version": result_version,
        "before_semantic": before_semantic, "after_semantic": after_semantic,
        "legacy": legacy_receipt, "source_scope": source_scope,
        "settled_scope": settled_scope, "request_digest": request_digest,
        "sci05": sci05_status,
    }
    receipt_hash = sha(receipt_body)
    conn.execute("BEGIN IMMEDIATE")
    try:
        if final:
            conn.execute(
                "INSERT INTO actor_version VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (actor, branch, epoch, int(old[0]) + 1,
                 "ADMINISTRATIVE_NOCHANGE" if decision_kind == "TRUE_NO_CHANGE_EVALUATED"
                 else "SEMANTIC_CHANGE", result_version, before_version,
                 after_semantic, canon({"after": after_semantic}),
                 actor_state_status, source_scope, NOW, receipt_hash, NOW),
            )
        conn.execute(
            "INSERT INTO decision_receipt VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                receipt_hash, decision_kind, actor, branch, epoch, seq, None,
                event_key, attempt_no, source_scope, settled_scope, legacy_receipt,
                f"legacy-event-{actor}", "legacy-after", "legacy-domain",
                f"wr-{actor}-{branch}", f"we-{actor}-{branch}", source_status,
                world_occurrence, actor_presence, actor_reception, rule_a_status,
                rule_t_status, actor_state_status, memory_evidence, sci05_status,
                sci05_certificate, before_version, result_version, before_semantic,
                after_semantic, source_scope,
                "rule-a" if rule_a_status.startswith("APPLIED") else None,
                "rule-t" if final else None, "readset" if final else None,
                "permission" if final else None, decision_kind, canon(receipt_body),
                NOW, NOW,
            ),
        )
        conn.execute(
            "INSERT INTO event_attempt VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                f"attempt-{actor}-{branch}-{event_key}-{attempt_no}",
                event_key, actor, branch, epoch, attempt_no, idempotency_key,
                request_digest, source_scope, settled_scope, None, receipt_hash,
                "FINALIZED" if final else "HELD", None, None,
                canon({"attempt": attempt_no, "key": idempotency_key}), NOW,
            ),
        )
        conn.execute(
            "INSERT INTO projection_outbox VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (receipt_hash, actor, branch, epoch, seq, result_version,
             f"wr-{actor}-{branch}", sha({"outbox": receipt_hash}),
             canon({"receipt": receipt_hash}), "PENDING", None, None, 0, None),
        )
        if target_id is not None:
            if target_hash is None:
                raise RuntimeError("TARGET_HASH_REQUIRED")
            conn.execute(
                "INSERT INTO actor_target VALUES (?,?,?,?,?,?,?,?,?)",
                (actor, branch, epoch, target_id, target_hash,
                 canon({"target": target_id}), f"wr-{actor}-{branch}",
                 receipt_hash, NOW),
            )
        changed = conn.execute(
            "UPDATE actor_head SET head_version_no=?,head_version_hash=?,"
            "head_semantic_hash=?,last_receipt_seq=?,last_finalized_seq=?,"
            "updated_admin_us=? WHERE actor_id=? AND branch_id=? AND branch_epoch=? "
            "AND head_version_no=? AND head_version_hash=? AND last_receipt_seq=? "
            "AND last_finalized_seq=?",
            (
                int(old[0]) + (1 if final else 0),
                result_version if final else old[1],
                after_semantic if final else old[2], seq,
                seq if final else old[4], NOW, actor, branch, epoch,
                old[0], old[1], old[3], old[4],
            ),
        ).rowcount
        if changed != 1:
            raise RuntimeError("CAS_CONFLICT")
        conn.execute("COMMIT")
    except BaseException:
        if conn.in_transaction:
            conn.execute("ROLLBACK")
        raise
    return {"receipt_hash": receipt_hash, "seq": seq, "final": final,
            "version": result_version, "head": head(conn, actor, branch)}


def expect_error(fn, contains: str) -> None:
    try:
        fn()
    except Exception as exc:
        text = str(exc)
        assert contains in text or contains == "", (contains, text)
        return
    raise AssertionError("EXPECTED_ERROR_NOT_RAISED:" + contains)


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "actor.sqlite"
        conn = connect(path)
        seed(conn, "A", "b0", "e0", "root")
        seed(conn, "B", "b0", "e0", "root")

        first = publish(
            conn, actor="A", branch="b0", epoch="e0", event_key="event-1",
            attempt_no=1, idempotency_key="idem-1", request_digest="digest-1",
            decision_kind="COMMITTED_CHANGE", legacy_receipt="legacy-A-b0",
            source_scope="source-1", settled_scope="settled-1",
            target_id="target-same", target_hash="target-hash-a",
        )
        assert first["final"] and first["seq"] == 1
        assert first["head"][0] == 1 and first["head"][3] == 1
        assert conn.execute(
            "SELECT projection_state FROM projection_outbox WHERE receipt_hash=?",
            (first["receipt_hash"],),
        ).fetchone()[0] == "PENDING"

        held = publish(
            conn, actor="A", branch="b0", epoch="e0", event_key="event-2",
            attempt_no=1, idempotency_key="idem-2", request_digest="digest-2",
            decision_kind="HELD_MISSING_RULE", legacy_receipt="legacy-A-b0",
            source_scope="source-2", settled_scope="settled-2",
            rule_t_status="HELD_MISSING_RULE", sci05_status="HELD",
        )
        assert held["seq"] == 2 and held["head"][0] == 1
        assert conn.execute(
            "SELECT count(*) FROM actor_version WHERE actor_id='A' AND branch_id='b0'"
        ).fetchone()[0] == 2

        requal = publish(
            conn, actor="A", branch="b0", epoch="e0", event_key="event-2",
            attempt_no=2, idempotency_key="idem-2-r2", request_digest="digest-2b",
            decision_kind="TRUE_NO_CHANGE_EVALUATED", legacy_receipt="legacy-A-b0",
            source_scope="source-2b", settled_scope="settled-2b",
            rule_t_status="TRUE_NO_CHANGE_EVALUATED",
        )
        assert requal["seq"] == 3 and requal["head"][0] == 2
        assert requal["head"][4] == 3
        assert conn.execute(
            "SELECT count(*) FROM event_attempt WHERE event_key='event-2'"
        ).fetchone()[0] == 2

        expect_error(lambda: publish(
            conn, actor="A", branch="b0", epoch="e0", event_key="event-2",
            attempt_no=3, idempotency_key="idem-2-r3", request_digest="digest-2c",
            decision_kind="COMMITTED_CHANGE", legacy_receipt="legacy-A-b0",
            source_scope="source-2c", settled_scope="settled-2c",
        ), "UNIQUE constraint failed")

        expect_error(lambda: publish(
            conn, actor="A", branch="b0", epoch="e0", event_key="event-3",
            attempt_no=1, idempotency_key="idem-1", request_digest="changed",
            decision_kind="HELD_MISSING_RULE", legacy_receipt="legacy-A-b0",
            source_scope="source-3", settled_scope="settled-3",
            sci05_status="HELD",
        ), "UNIQUE constraint failed")

        before = conn.execute("SELECT count(*) FROM decision_receipt").fetchone()[0]
        expect_error(lambda: publish(
            conn, actor="A", branch="b0", epoch="e0", event_key="event-4",
            attempt_no=1, idempotency_key="idem-4", request_digest="digest-4",
            decision_kind="HELD_MISSING_RULE", legacy_receipt="legacy-A-b0",
            source_scope="source-4", settled_scope="settled-4",
            expected_head=(0, "stale", "stale", 0, 0), sci05_status="HELD",
        ), "STALE_ACTOR_PARENT")
        assert conn.execute("SELECT count(*) FROM decision_receipt").fetchone()[0] == before

        conn.execute(
            "INSERT INTO actor_target VALUES (?,?,?,?,?,?,?,?,?)",
            ("B", "b0", "e0", "target-same", "target-hash-b",
             canon({"target": "target-same", "actor": "B"}), "wr-B-b0", None, NOW),
        )
        assert conn.execute(
            "SELECT count(*) FROM actor_target WHERE target_id='target-same'"
        ).fetchone()[0] == 2
        assert conn.execute(
            "SELECT count(*) FROM actor_target WHERE actor_id='A' AND target_id='target-same'"
        ).fetchone()[0] == 1

        expect_error(lambda: conn.execute(
            "UPDATE event_attempt SET attempt_state='SUPERSEDED'"
        ), "EVENT_ATTEMPT_APPEND_ONLY")
        expect_error(lambda: conn.execute(
            "UPDATE projection_outbox SET projection_state='ACKED'"
        ), "OUTBOX_STATE_TRANSITION_REFUSED")

        conn.execute("BEGIN IMMEDIATE")
        conn.execute(
            "INSERT INTO actor_target VALUES (?,?,?,?,?,?,?,?,?)",
            ("A", "b0", "e0", "rollback-target", "rh", "{}", None, None, NOW),
        )
        conn.execute("ROLLBACK")
        assert conn.execute(
            "SELECT count(*) FROM actor_target WHERE target_id='rollback-target'"
        ).fetchone()[0] == 0

        print("PASS actor_authority: atomic final/held/requalification, CAS, idempotency, target scope, append-only and rollback")
        print("PASS actor_head=version=%s receipt_seq=%s finalized_seq=%s" %
              (requal["head"][0], requal["head"][3], requal["head"][4]))
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
