"""C9-R3 test-only actor authority helper.

This is a sourcefree SQLite proof, not a production C9 implementation or a
storage-owner freeze. It repairs the two RRP0-R2 helper defects: exact
same-key/same-digest replay and held/final status-axis separation. The SQL
schema is a provenance copy under this R3 directory; the old S36 readset is not
modified.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
SCHEMA = HERE / "schema_actor_r3.sql"
MIRROR_SCHEMA = HERE / "schema_mirror_r3.sql"
NOW = 1_780_000_000_000_000
FINAL_KINDS = {"COMMITTED_CHANGE", "TRUE_NO_CHANGE_EVALUATED"}
HELD_RULE_T = {
    "HELD_MISSING_RULE": {"HELD_MISSING_RULE"},
    "HELD_MISSING_SOURCE": {"HELD_MISSING_SOURCE", "HELD_MISSING_RULE"},
    "SOURCE_DENIED": {"HELD_MISSING_SOURCE", "INTEGRITY_FAILED"},
    "DEFERRED": {"DEFERRED"},
    "NOT_APPLICABLE_BY_ISSUED_RULE": {"NOT_APPLICABLE_BY_ISSUED_RULE"},
    "INTEGRITY_FAILED": {"INTEGRITY_FAILED"},
}


class ActorR3Error(RuntimeError):
    """Typed sourcefree refusal; not a production C9 error registry."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


def canon(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha(value: Any) -> str:
    return hashlib.sha256(canon(value).encode("utf8")).hexdigest()


def connect(path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(path), isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(SCHEMA.read_text(encoding="utf8"))
    return conn


def mirror_connect(path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(path), isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(MIRROR_SCHEMA.read_text(encoding="utf8"))
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
    row = conn.execute(
        "SELECT head_version_no,head_version_hash,head_semantic_hash,"
        "last_receipt_seq,last_finalized_seq FROM actor_head "
        "WHERE actor_id=? AND branch_id=?", (actor, branch)
    ).fetchone()
    return tuple(row)


def _status_axes(decision_kind: str, rule_t_status: str, sci05_status: str,
                 rule_t_hash: str | None, readset_hash: str | None) -> None:
    if decision_kind in FINAL_KINDS:
        if sci05_status in ("DENIED", "HELD", "INTEGRITY_FAILED"):
            raise ActorR3Error("SCI05_DENIED_CANNOT_FINALIZE")
        if not rule_t_hash or not readset_hash:
            raise ActorR3Error("RULE_T_MISSING")
        if rule_t_status != decision_kind:
            raise ActorR3Error("STATUS_AXIS_CONFLICT")
        return
    if decision_kind not in HELD_RULE_T:
        raise ActorR3Error("DECISION_KIND_UNKNOWN")
    if rule_t_status not in HELD_RULE_T[decision_kind]:
        raise ActorR3Error("STATUS_AXIS_CONFLICT")


def _receipt(conn: sqlite3.Connection, receipt_hash: str) -> dict:
    row = conn.execute(
        "SELECT r.receipt_hash,r.commit_seq,r.decision_kind,r.canonical_receipt_json,"
        "r.result_version_hash,e.attempt_state "
        "FROM decision_receipt r JOIN event_attempt e "
        "ON e.receipt_hash=r.receipt_hash WHERE r.receipt_hash=?",
        (receipt_hash,),
    ).fetchone()
    if row is None:
        raise ActorR3Error("RECEIPT_MISSING", receipt_hash)
    return {
        "receipt_hash": row["receipt_hash"],
        "seq": row["commit_seq"],
        "decision_kind": row["decision_kind"],
        "version": row["result_version_hash"],
        "attempt_state": row["attempt_state"],
    }


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
    rule_t_status: str | None = None,
    actor_state_status: str = "VERSIONED_PRESENT",
    memory_evidence: str = "ACTOR_ACCESSIBLE",
    sci05_status: str = "ADMITTED",
    sci05_certificate: str | None = None,
    target_id: str | None = None,
    target_hash: str | None = None,
    expected_head: tuple | None = None,
    prior_attempt_id: str | None = None,
    rule_t_hash: str | None = None,
    readset_hash: str | None = None,
) -> dict:
    """Publish one test-only actor decision, or replay the exact receipt."""
    final = decision_kind in FINAL_KINDS
    rule_t_status = rule_t_status or decision_kind
    _status_axes(decision_kind, rule_t_status, sci05_status, rule_t_hash, readset_hash)

    conn.execute("BEGIN IMMEDIATE")
    try:
        existing = conn.execute(
            "SELECT request_digest,receipt_hash FROM event_attempt WHERE idempotency_key=?",
            (idempotency_key,),
        ).fetchone()
        if existing is not None:
            if existing["request_digest"] != request_digest:
                raise ActorR3Error("IDEMPOTENCY_PAYLOAD_CONFLICT")
            conn.execute("COMMIT")
            result = _receipt(conn, existing["receipt_hash"])
            result["replay"] = True
            result["head"] = head(conn, actor, branch)
            return result

        old = head(conn, actor, branch)
        if expected_head is not None and tuple(old) != tuple(expected_head):
            raise ActorR3Error("STALE_ACTOR_PARENT")

        final_row = conn.execute(
            "SELECT receipt_hash FROM event_attempt WHERE actor_id=? AND branch_id=? "
            "AND branch_epoch=? AND event_key=? AND attempt_state='FINALIZED'",
            (actor, branch, epoch, event_key),
        ).fetchone()
        if final_row is not None:
            raise ActorR3Error("EVENT_ALREADY_FINALIZED")

        prior = conn.execute(
            "SELECT attempt_id,attempt_no,receipt_hash FROM event_attempt "
            "WHERE actor_id=? AND branch_id=? AND branch_epoch=? AND event_key=? "
            "ORDER BY attempt_no DESC LIMIT 1",
            (actor, branch, epoch, event_key),
        ).fetchone()
        if int(attempt_no) > 1 and prior is None:
            raise ActorR3Error("PRIOR_ATTEMPT_REQUIRED")
        if prior is not None:
            if int(attempt_no) <= int(prior["attempt_no"]):
                raise ActorR3Error("ATTEMPT_ORDER_INVALID")
            if prior_attempt_id is None:
                prior_attempt_id = str(prior["attempt_id"])

        seq = int(old[3]) + 1
        before_version = str(old[1])
        before_semantic = str(old[2])
        after_semantic = None
        if final:
            if decision_kind == "TRUE_NO_CHANGE_EVALUATED":
                after_semantic = before_semantic
            else:
                after_semantic = sha({"actor": actor, "event": event_key, "seq": seq})
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
                receipt_hash, decision_kind, actor, branch, epoch, seq,
                str(prior["receipt_hash"]) if prior is not None else None,
                event_key, attempt_no, source_scope, settled_scope, legacy_receipt,
                f"legacy-event-{actor}", "legacy-after", "legacy-domain",
                f"wr-{actor}-{branch}", f"we-{actor}-{branch}", source_status,
                world_occurrence, actor_presence, actor_reception, rule_a_status,
                rule_t_status, actor_state_status, memory_evidence, sci05_status,
                sci05_certificate, before_version, result_version, before_semantic,
                after_semantic, source_scope,
                "rule-a" if rule_a_status.startswith("APPLIED") else None,
                rule_t_hash, readset_hash,
                "permission" if final else None, decision_kind, canon(receipt_body),
                NOW, NOW,
            ),
        )
        attempt_id = f"attempt-{actor}-{branch}-{event_key}-{attempt_no}"
        conn.execute(
            "INSERT INTO event_attempt VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                attempt_id, event_key, actor, branch, epoch, attempt_no,
                idempotency_key, request_digest, source_scope, settled_scope,
                prior_attempt_id, receipt_hash, "FINALIZED" if final else "HELD",
                None, None, canon({"attempt": attempt_no, "key": idempotency_key}),
                NOW,
            ),
        )
        conn.execute(
            "INSERT INTO projection_outbox VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (receipt_hash, actor, branch, epoch, seq, result_version,
             f"wr-{actor}-{branch}", sha({"outbox": receipt_hash}),
             canon({"receipt": receipt_hash}), "PENDING", None, None, 0, None),
        )
        if target_id is not None:
            if not target_hash:
                raise ActorR3Error("TARGET_HASH_REQUIRED")
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
            raise ActorR3Error("CAS_CONFLICT")
        conn.execute("COMMIT")
    except BaseException:
        if conn.in_transaction:
            conn.execute("ROLLBACK")
        raise
    result = _receipt(conn, receipt_hash)
    result.update({"replay": False, "head": head(conn, actor, branch)})
    return result


def outbox(conn: sqlite3.Connection, receipt_hash: str) -> str:
    row = conn.execute(
        "SELECT projection_state FROM projection_outbox WHERE receipt_hash=?",
        (receipt_hash,),
    ).fetchone()
    if row is None:
        raise ActorR3Error("OUTBOX_MISSING", receipt_hash)
    return str(row[0])


def mark_projected(conn: sqlite3.Connection, receipt_hash: str, projection_hash: str) -> None:
    state = outbox(conn, receipt_hash)
    if state == "ACKED":
        raise ActorR3Error("OUTBOX_ALREADY_ACKED")
    if state == "PENDING":
        conn.execute(
            "UPDATE projection_outbox SET projection_state='PROJECTED',"
            "projected_c12_hash=?,attempt_count=attempt_count+1 WHERE receipt_hash=?",
            (projection_hash, receipt_hash),
        )


def ack_outbox(conn: sqlite3.Connection, receipt_hash: str, projection_hash: str) -> None:
    state = outbox(conn, receipt_hash)
    row = conn.execute(
        "SELECT projected_c12_hash FROM projection_outbox WHERE receipt_hash=?",
        (receipt_hash,),
    ).fetchone()
    if state == "ACKED":
        if row is not None and row[0] == projection_hash:
            return
        raise ActorR3Error("OUTBOX_ACK_CONFLICT")
    if state != "PROJECTED" or row is None or row[0] != projection_hash:
        raise ActorR3Error("OUTBOX_NOT_PROJECTED")
    conn.execute(
        "UPDATE projection_outbox SET projection_state='ACKED',"
        "acked_admin_us=?,attempt_count=attempt_count+1 WHERE receipt_hash=?",
        (NOW, receipt_hash),
    )


def mirror_ready(
    mirror: sqlite3.Connection,
    c12_branch_id: str,
    c9_seq: int,
    receipt_hash: str,
    projection_hash: str,
) -> bool:
    """Return true only for a CLEAN, exact, contiguous mirror watermark."""
    watermark = mirror.execute(
        "SELECT last_seq,last_receipt_hash,last_projection_hash,watermark_state "
        "FROM mirror_watermark WHERE c12_branch_id=?", (c12_branch_id,)
    ).fetchone()
    if watermark is None or watermark["watermark_state"] != "CLEAN":
        return False
    if watermark["last_seq"] != c9_seq:
        return False
    if watermark["last_receipt_hash"] != receipt_hash:
        return False
    if watermark["last_projection_hash"] != projection_hash:
        return False
    row = mirror.execute(
        "SELECT c9_receipt_hash,projection_hash FROM mirror_receipt "
        "WHERE c12_branch_id=? AND c9_seq=?", (c12_branch_id, c9_seq)
    ).fetchone()
    return row is not None and row["c9_receipt_hash"] == receipt_hash and row["projection_hash"] == projection_hash


__all__ = [
    "ActorR3Error",
    "FINAL_KINDS",
    "HELD_RULE_T",
    "MIRROR_SCHEMA",
    "NOW",
    "SCHEMA",
    "ack_outbox",
    "canon",
    "connect",
    "head",
    "mark_projected",
    "mirror_connect",
    "mirror_ready",
    "outbox",
    "publish",
    "seed",
    "sha",
]
