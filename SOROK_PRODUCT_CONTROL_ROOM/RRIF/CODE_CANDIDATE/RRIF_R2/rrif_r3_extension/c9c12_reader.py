"""Sourcefree C9 actor-snapshot and guarded C12 cold-read composite.

This is a candidate consumer, not an owner-frozen C9/C12 contract. It reads the
exact C9 R3B actor SQLite schema and the BP4R guarded C12 store without writing
either database. External anchor custody is always reported as a separate HOLD.
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from c12_guard import (
    GuardedC12Store,
    anchor_payload,
    check_anchor,
    verify_store,
)

C9_WRITER_SCHEMA = "C9_ACTOR_AUTHORITY_R3@1"
MIRROR_SCHEMA = "C12_ACTOR_MIRROR_R3@1"
SUPPORTED_C9_SNAPSHOT_VERSIONS = frozenset({"GENESIS_VALID_EMPTY", "FORK_INHERITED",
                                            "SEMANTIC_CHANGE",
                                            "ADMINISTRATIVE_NOCHANGE"})


class C9C12Refusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


def _connect_ro(path: str | Path) -> sqlite3.Connection:
    p = Path(path)
    if not p.is_file():
        raise C9C12Refusal("C9_SOURCE_MISSING")
    conn = sqlite3.connect(f"file:{p.resolve()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def _row(conn: sqlite3.Connection, sql: str, args: tuple = ()) -> sqlite3.Row | None:
    return conn.execute(sql, args).fetchone()


def read_actor_snapshot(
    path: str | Path,
    *,
    actor_id: str,
    branch_id: str = "b0",
    branch_epoch: str = "e0",
    mirror_path: str | Path | None = None,
) -> dict[str, Any]:
    """Read the exact C9 actor head/version/outbox and optional mirror state."""
    conn = _connect_ro(path)
    try:
        meta = {str(r[0]): str(r[1]) for r in conn.execute("SELECT key,value FROM actor_meta")}
        if meta.get("schema") != C9_WRITER_SCHEMA:
            raise C9C12Refusal("C9_WRITER_SCHEMA_UNSUPPORTED",
                               str(meta.get("schema")))
        branch = _row(conn, "SELECT * FROM actor_branch WHERE actor_id=? AND branch_id=?",
                      (actor_id, branch_id))
        if branch is None:
            raise C9C12Refusal("C9_ACTOR_BRANCH_MISSING")
        if branch["branch_epoch"] != branch_epoch:
            raise C9C12Refusal("C9_BRANCH_EPOCH_MISMATCH")
        head = _row(conn, "SELECT * FROM actor_head WHERE actor_id=? AND branch_id=?",
                    (actor_id, branch_id))
        if head is None:
            raise C9C12Refusal("C9_ACTOR_HEAD_MISSING")
        version = _row(conn, "SELECT * FROM actor_version WHERE actor_id=? AND branch_id=? "
                             "AND branch_epoch=? AND version_no=?",
                       (actor_id, branch_id, branch_epoch, head["head_version_no"]))
        if version is None:
            raise C9C12Refusal("C9_ACTOR_VERSION_MISSING")
        if version["version_hash"] != head["head_version_hash"]:
            raise C9C12Refusal("C9_HEAD_VERSION_HASH_MISMATCH")
        if version["semantic_hash"] != head["head_semantic_hash"]:
            raise C9C12Refusal("C9_HEAD_SEMANTIC_HASH_MISMATCH")
        if version["version_kind"] not in SUPPORTED_C9_SNAPSHOT_VERSIONS:
            raise C9C12Refusal("C9_VERSION_KIND_HELD", version["version_kind"])
        receipt = None
        if head["last_receipt_seq"] > 0:
            receipt = _row(conn, "SELECT * FROM decision_receipt WHERE actor_id=? AND "
                                 "branch_id=? AND branch_epoch=? AND commit_seq=?",
                           (actor_id, branch_id, branch_epoch, head["last_receipt_seq"]))
            if receipt is None:
                raise C9C12Refusal("C9_FINAL_RECEIPT_MISSING")
            if (version["decision_receipt_hash"] is not None
                    and receipt["receipt_hash"] != version["decision_receipt_hash"]):
                raise C9C12Refusal("C9_HEAD_RECEIPT_VERSION_MISMATCH")
            if (version["decision_receipt_hash"] is None
                    and receipt["decision_kind"] in
                    ("COMMITTED_CHANGE", "TRUE_NO_CHANGE_EVALUATED")):
                raise C9C12Refusal("C9_HEAD_RECEIPT_VERSION_MISMATCH")
        outbox = None
        if receipt is not None:
            outbox = _row(conn, "SELECT * FROM projection_outbox WHERE receipt_hash=?",
                          (receipt["receipt_hash"],))
            if outbox is None:
                raise C9C12Refusal("C9_OUTBOX_MISSING")
            if outbox["projection_state"] != "ACKED":
                raise C9C12Refusal("C9_OUTBOX_HELD", outbox["projection_state"])
        mirror = None
        if mirror_path is not None:
            mpath = Path(mirror_path)
            if not mpath.is_file():
                raise C9C12Refusal("C9_MIRROR_MISSING")
            mconn = sqlite3.connect(f"file:{mpath.resolve()}?mode=ro", uri=True)
            try:
                mmeta = {str(r[0]): str(r[1]) for r in
                         mconn.execute("SELECT key,value FROM mirror_meta")}
                if mmeta.get("schema") != MIRROR_SCHEMA:
                    raise C9C12Refusal("C9_MIRROR_SCHEMA_UNSUPPORTED")
                mirror = _row(mconn, "SELECT * FROM mirror_branch WHERE c12_branch_id=?",
                              (branch["c12_branch_id"],))
                if mirror is None:
                    raise C9C12Refusal("C9_MIRROR_BRANCH_MISSING")
                if mirror["mirror_state"] not in ("ROOT_READY", "FORK_READY"):
                    raise C9C12Refusal("C9_MIRROR_HELD", mirror["mirror_state"])
            finally:
                mconn.close()
        return {
            "status": "ACTOR_SNAPSHOT_OK",
            "actor_id": actor_id,
            "branch_id": branch_id,
            "branch_epoch": branch_epoch,
            "head_version_no": head["head_version_no"],
            "head_version_hash": head["head_version_hash"],
            "head_semantic_hash": head["head_semantic_hash"],
            "version_kind": version["version_kind"],
            "canonical_state_json": version["canonical_state_json"],
            "last_receipt_seq": head["last_receipt_seq"],
            "last_finalized_seq": head["last_finalized_seq"],
            "decision_kind": None if receipt is None else receipt["decision_kind"],
            "receipt_hash": None if receipt is None else receipt["receipt_hash"],
            "outbox_state": None if outbox is None else outbox["projection_state"],
            "c9_writer_schema": meta["schema"],
            "mirror_state": None if mirror is None else mirror["mirror_state"],
            "mirror_selected": mirror_path is not None,
            "source_owner_frozen": False,
            "grade": "SOURCEFREE_CANDIDATE_READER_NOT_OWNER_ADOPTED",
        }
    finally:
        conn.close()


def guarded_c12_cold_read(
    path: str | Path,
    *,
    branch_id: str = "root",
    anchor: dict | None = None,
    verify_signature: Any = None,
) -> dict[str, Any]:
    """Run the BP4R C12 cold reader and keep external custody explicit."""
    store = GuardedC12Store(path)
    try:
        report = verify_store(store, branch_id)
        payload = anchor_payload(store, branch_id)
        anchor_result = check_anchor(anchor, payload, verify_signature)
        return {
            "status": "C12_COLD_READ_OK" if report["ok"] else "C12_HELD",
            "ok": bool(report["ok"]),
            "content_ok": report["content_ok"],
            "fork_ok": report["fork_ok"],
            "schema_ok": report["schema_ok"],
            "errors": list(report["errors"]),
            "counts": report["counts"],
            "fork_status": report["fork"]["status"],
            "anchor_status": anchor_result,
            "external_custody": "OWNER_ANCHOR_REQUIRED",
            "grade": "SOURCEFREE_CANDIDATE_READER_NOT_OWNER_ADOPTED",
        }
    finally:
        store.close()


def read_composite(
    c9_path: str | Path,
    c12_path: str | Path,
    *,
    actor_id: str,
    branch_id: str = "b0",
    branch_epoch: str = "e0",
    c12_branch_id: str = "root",
    mirror_path: str | Path | None = None,
) -> dict[str, Any]:
    """The actual sourcefree first consumer for I1/CP-A5-compatible use."""
    actor = read_actor_snapshot(c9_path, actor_id=actor_id, branch_id=branch_id,
                                branch_epoch=branch_epoch, mirror_path=mirror_path)
    c12 = guarded_c12_cold_read(c12_path, branch_id=c12_branch_id)
    return {
        "status": "COMPOSITE_OK__EXTERNAL_ANCHOR_REQUIRED"
        if actor["status"] == "ACTOR_SNAPSHOT_OK" and c12["ok"]
        else "COMPOSITE_HELD",
        "actor": actor,
        "c12": c12,
        "first_consumer": "sourcefree C9 snapshot + BP4R C12 cold-read composite",
        "owner_adoption": "NONE",
        "native_person": False,
    }


__all__ = ["C9C12Refusal", "read_actor_snapshot", "guarded_c12_cold_read",
           "read_composite"]
