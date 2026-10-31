"""Atomic candidate transaction with full semantic custody and no-ghost rollback.

C9R hardening:
- The exact evaluated sealed target record (including semantic object, effective
  time, payload and causal parents) is preserved and republished, not replaced by
  a smaller row; the committed identity is the exact validated `target_id`.
- CREATE requires a sealed authorization preimage carried by the decision. Commit
  revalidates the live permission/rule entry, revocation, currentness, prestate,
  response binding and the full record digest. A fabricated decision or a
  permission mutated between evaluation and commit is refused.
- The publication readset reuses the accepted B3AS logical schema/readset shape:
  sqlite_master definitions, durable PRAGMA metadata and table rows.
- The occurrence identity is immutable: a duplicate event_id with different
  content is refused.
"""
from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .canon import canonical, digest, seal, valid
from .target_rules import (
    GRADE_TEST_ONLY,
    TEST_ONLY_PREFIX,
    TEST_ONLY_SCOPE,
    TargetBranch,
    TargetDecision,
)

TRANSACTION_SCHEMA = "C9P_CANDIDATE_TRANSACTION@1"


class TransactionRefusal(Exception):
    """A candidate transaction refused and rolled back with no ghost state."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True)
class CommitReceipt:
    """One committed candidate transaction receipt."""

    status: str
    joint_transaction_id: str
    admitted_event_ref: str
    before_hash: str
    after_hash: str
    target_branch: str
    target_reason: str
    readset_refs: tuple[str, ...]
    record_hash: str
    receipt_hash: str
    no_mutation: bool
    target_id: str = ""
    authorization_hash: str = ""
    publication_grade: str = ""
    response_ref: str = ""

    @property
    def committed(self) -> bool:
        return self.status == "COMMITTED"


def _live_preimage_body(preimage: Mapping[str, Any]) -> dict:
    return {k: v for k, v in preimage.items() if k != "hash"}


class CandidateStore:
    """SQLite-backed candidate store with atomic publication and no-ghost rollback."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.db = sqlite3.connect(str(self.path), isolation_level=None)
        self.db.executescript(
            """
            CREATE TABLE IF NOT EXISTS occurrence (hash TEXT PRIMARY KEY, body TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS event_identity (event_id TEXT PRIMARY KEY, hash TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS response (hash TEXT PRIMARY KEY, body TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS target_state (id TEXT PRIMARY KEY, body TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS target_journal (id TEXT PRIMARY KEY, body TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS receipt (hash TEXT PRIMARY KEY, body TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS clock (clock INTEGER PRIMARY KEY);
            """
        )

    def close(self) -> None:
        self.db.close()

    def __enter__(self) -> "CandidateStore":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def snapshot(self) -> dict[str, list[tuple]]:
        """Return every table's rows keyed by table name, ordered for comparison."""
        names = [
            row[0]
            for row in self.db.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            )
        ]
        return {
            name: self.db.execute(
                'SELECT * FROM "' + name.replace('"', '""') + '" ORDER BY 1'
            ).fetchall()
            for name in names
        }

    def _logical_readset(self) -> dict:
        """Capture the accepted B3AS-shaped logical publication readset."""
        return {
            "schema": self.db.execute(
                "SELECT type,name,tbl_name,sql FROM sqlite_master ORDER BY type,name"
            ).fetchall(),
            "metadata": {
                name: self.db.execute("PRAGMA " + name).fetchone()[0]
                for name in ("schema_version", "user_version", "application_id")
            },
            "tables": self.snapshot(),
        }

    def admit_occurrence(self, event: Mapping[str, Any]) -> dict:
        """Commit one admitted occurrence with immutable event identity."""
        if not isinstance(event, Mapping) or not valid(dict(event)):
            raise TransactionRefusal("EVENT_INTEGRITY_FAILURE")
        event_hash = event.get("hash", "")
        event_id = event.get("event_id", "")
        body = canonical({k: v for k, v in event.items() if k != "hash"})
        try:
            self.db.execute("BEGIN IMMEDIATE")
            prior = self.db.execute(
                "SELECT hash FROM event_identity WHERE event_id=?", (event_id,)
            ).fetchone()
            if prior is not None and prior[0] != event_hash:
                raise TransactionRefusal("EVENT_IDENTITY_CONFLICT")
            self.db.execute(
                "INSERT OR IGNORE INTO occurrence VALUES (?,?)", (event_hash, body)
            )
            self.db.execute(
                "INSERT OR IGNORE INTO event_identity VALUES (?,?)", (event_id, event_hash)
            )
            row = self.db.execute(
                "SELECT body FROM occurrence WHERE hash=?", (event_hash,)
            ).fetchone()
            if row is None or row[0] != body:
                raise TransactionRefusal("OCCURRENCE_ADMISSION_FAILED")
            self.db.execute("COMMIT")
        except BaseException:
            if self.db.in_transaction:
                self.db.execute("ROLLBACK")
            raise
        return dict(event)

    def event_identity_conflict(self, event: Mapping[str, Any]) -> bool:
        event_hash = event.get("hash", "")
        event_id = event.get("event_id", "")
        row = self.db.execute(
            "SELECT hash FROM event_identity WHERE event_id=?", (event_id,)
        ).fetchone()
        return row is not None and row[0] != event_hash

    def last_clock(self) -> int:
        row = self.db.execute("SELECT coalesce(max(clock),0) FROM clock").fetchone()
        return int(row[0]) if row else 0

    def committed_target_ids(self) -> frozenset[str]:
        rows = self.db.execute("SELECT id FROM target_state").fetchall()
        return frozenset(row[0] for row in rows)

    def target_state_hash(self) -> str:
        rows = self.db.execute("SELECT body FROM target_state ORDER BY id").fetchall()
        return digest([json.loads(row[0]) for row in rows])

    def read_target_state(self, middle_state_id: str) -> Mapping[str, Any] | None:
        """Read one committed full target record. Returns None when absent."""
        row = self.db.execute(
            "SELECT body FROM target_state WHERE id=?", (middle_state_id,)
        ).fetchone()
        return json.loads(row[0]) if row else None

    def committed_event_hashes(self) -> frozenset[str]:
        rows = self.db.execute("SELECT hash FROM occurrence").fetchall()
        return frozenset(row[0] for row in rows)

    def _revalidate(self, decision: TargetDecision, event_hash: str) -> None:
        record = decision.record_body
        if not isinstance(record, Mapping) or not valid(dict(record)):
            raise TransactionRefusal("TARGET_RECORD_PREIMAGE_MISSING")
        record_body = {k: v for k, v in record.items() if k != "hash"}
        if digest(record_body) != decision.record_hash:
            raise TransactionRefusal("TARGET_RECORD_DIGEST_MISMATCH")
        if record.get("middle_state_id") != decision.target_id:
            raise TransactionRefusal("TARGET_IDENTITY_MISMATCH")
        if record.get("actor_id") != decision.actor_id:
            raise TransactionRefusal("TARGET_ACTOR_MISMATCH")
        if record.get("permission_ref") != decision.permission_ref:
            raise TransactionRefusal("TARGET_PERMISSION_REF_MISMATCH")
        if record.get("before_target_hash") != decision.before_target_hash:
            raise TransactionRefusal("TARGET_PRESTATE_BINDING_MISMATCH")
        if record.get("response_hash", "") != decision.response_hash:
            raise TransactionRefusal("TARGET_RESPONSE_BINDING_MISMATCH")
        if record.get("publication_grade") != decision.publication_grade:
            raise TransactionRefusal("TARGET_GRADE_MISMATCH")
        preimage = decision.authorization_preimage
        if not isinstance(preimage, Mapping) or not preimage:
            raise TransactionRefusal("AUTHORIZATION_PREIMAGE_MISSING")
        if not valid(dict(preimage)):
            raise TransactionRefusal("AUTHORIZATION_PREIMAGE_UNSEALED")
        if digest(_live_preimage_body(preimage)) != preimage.get("hash"):
            raise TransactionRefusal("AUTHORIZATION_PREIMAGE_MUTATED")
        if preimage.get("hash") != decision.authorization_hash:
            raise TransactionRefusal("AUTHORIZATION_HASH_MISMATCH")
        permission = preimage.get("permission")
        rule_entry = preimage.get("rule_entry")
        if not isinstance(permission, Mapping) or not valid(dict(permission)):
            raise TransactionRefusal("PERMISSION_REVALIDATION_FAILED")
        if not isinstance(rule_entry, Mapping) or not valid(dict(rule_entry)):
            raise TransactionRefusal("RULE_REVALIDATION_FAILED")
        if permission.get("revoked"):
            raise TransactionRefusal("PERMISSION_REVOKED_AT_COMMIT")
        if permission.get("actor_id") != decision.actor_id:
            raise TransactionRefusal("PERMISSION_ACTOR_MISMATCH")
        if permission.get("grant_id") != decision.permission_ref:
            raise TransactionRefusal("PERMISSION_GRANT_MISMATCH")
        if permission.get("grade") != GRADE_TEST_ONLY:
            raise TransactionRefusal("PERMISSION_GRADE_UNVERIFIED")
        if not str(permission.get("issuer_ref", "")).startswith(TEST_ONLY_PREFIX):
            raise TransactionRefusal("PERMISSION_ISSUER_UNVERIFIED")
        if permission.get("issuer_scope") != TEST_ONLY_SCOPE:
            raise TransactionRefusal("PERMISSION_SCOPE_INVALID")
        if permission.get("rule_content_hash") != record.get("creation_rule_ref"):
            raise TransactionRefusal("PERMISSION_RULE_MISMATCH")
        if permission.get("before_target_hash") != self.target_state_hash():
            raise TransactionRefusal("PRESTATE_CONFLICT_AT_COMMIT")
        issued_at = permission.get("issued_at")
        as_of = preimage.get("as_of")
        if not isinstance(issued_at, int) or not isinstance(as_of, int):
            raise TransactionRefusal("PERMISSION_TIME_UNVERIFIABLE")
        if issued_at > as_of:
            raise TransactionRefusal("PERMISSION_NOT_YET_VALID_AT_COMMIT")
        expires_at = permission.get("expires_at")
        if isinstance(expires_at, int) and as_of >= expires_at:
            raise TransactionRefusal("PERMISSION_EXPIRED_AT_COMMIT")
        declared_response = permission.get("response_hash", "")
        if declared_response and declared_response != preimage.get("response_hash"):
            raise TransactionRefusal("PERMISSION_RESPONSE_MISMATCH_AT_COMMIT")
        if rule_entry.get("rule_content_hash") != record.get("creation_rule_ref"):
            raise TransactionRefusal("RULE_CONTENT_MISMATCH")
        if not rule_entry.get("issuer_verified", False):
            raise TransactionRefusal("RULE_ISSUER_UNVERIFIED")
        if rule_entry.get("grade") != GRADE_TEST_ONLY:
            raise TransactionRefusal("RULE_GRADE_UNVERIFIED")
        if not str(rule_entry.get("issuer_ref", "")).startswith(TEST_ONLY_PREFIX):
            raise TransactionRefusal("RULE_ISSUER_NAMESPACE_UNVERIFIED")
        if record.get("state_kind_id") != rule_entry.get("state_kind_id"):
            raise TransactionRefusal("RULE_STATE_KIND_MISMATCH")
        if record.get("semantic_object_ref") not in rule_entry.get(
            "accepted_semantic_objects", []
        ):
            raise TransactionRefusal("RULE_SEMANTIC_OBJECT_MISMATCH")
        if preimage.get("event_hash") != event_hash:
            raise TransactionRefusal("AUTHORIZATION_EVENT_MISMATCH")
        history = preimage.get("enacted_history_refs", [])
        if not isinstance(history, list) or len(history) < 2 or len(set(history)) != len(history):
            raise TransactionRefusal("ENACTED_HISTORY_REVALIDATION_FAILED")
        for ref in history:
            if not isinstance(ref, str) or not ref.startswith(TEST_ONLY_PREFIX):
                raise TransactionRefusal("ENACTED_HISTORY_REVALIDATION_FAILED")
        if record.get("response_hash", "") != preimage.get("response_hash"):
            raise TransactionRefusal("AUTHORIZATION_RESPONSE_MISMATCH")

    def commit(
        self,
        *,
        event: Mapping[str, Any],
        response: Mapping[str, Any],
        decision: TargetDecision,
        readset_refs: tuple[str, ...],
        fault: str | None = None,
    ) -> CommitReceipt:
        """Commit occurrence, response and accepted target effect atomically."""
        before = self._logical_readset()
        before_hash = digest(before)
        event_hash = event.get("hash", "")
        try:
            self.db.execute("BEGIN IMMEDIATE")
            row = self.db.execute(
                "SELECT body FROM occurrence WHERE hash=?", (event_hash,)
            ).fetchone()
            if row is None or row[0] != canonical(
                {k: v for k, v in event.items() if k != "hash"}
            ):
                raise TransactionRefusal("EVENT_NOT_ADMITTED")
            if not valid(dict(response)):
                raise TransactionRefusal("RESPONSE_INTEGRITY_FAILURE")
            if response.get("event_ref") != event_hash:
                raise TransactionRefusal("RESPONSE_EVENT_MISMATCH")
            if decision.response_hash:
                if response.get("receipt_hash") != decision.response_hash:
                    raise TransactionRefusal("COMMIT_RESPONSE_BINDING_MISMATCH")
            elif decision.branch is TargetBranch.CREATE and decision.target_id == decision.proposal_hash:
                raise TransactionRefusal("COMMIT_EXACT_BINDING_REQUIRED")
            target_rows: list[tuple[str, str]] = []
            journal_rows: list[tuple[str, str]] = []
            if decision.branch is TargetBranch.CREATE:
                if not decision.record_hash:
                    raise TransactionRefusal("TARGET_RECORD_MISSING")
                self._revalidate(decision, event_hash)
                if decision.before_target_hash != self.target_state_hash():
                    raise TransactionRefusal("STALE_TARGET_PRESTATE")
                if not decision.target_id:
                    raise TransactionRefusal("TARGET_IDENTITY_MISSING")
                if decision.target_id in self.committed_target_ids():
                    raise TransactionRefusal("DUPLICATE_TARGET_IDENTITY")
                record = dict(decision.record_body or {})
                stored = dict(record)
                stored["record_hash"] = decision.record_hash
                stored["record_preimage"] = record
                target_rows.append(
                    (decision.target_id, canonical(stored))
                )
                journal_rows.append(
                    (
                        decision.record_hash,
                        canonical(
                            {
                                "record_hash": decision.record_hash,
                                "target_id": decision.target_id,
                                "proposal_hash": decision.proposal_hash,
                                "branch": decision.branch.value,
                                "reason": decision.reason.value,
                                "authorization_hash": decision.authorization_hash,
                                "permission_ref": decision.permission_ref,
                                "response_hash": decision.response_hash,
                                "readset_refs": list(decision.readset_refs),
                            }
                        ),
                    )
                )
            elif decision.branch is TargetBranch.DENY:
                if decision.record_hash:
                    raise TransactionRefusal("DENY_WITH_RECORD")
            if decision.branch is TargetBranch.CREATE:
                missing = [ref for ref in decision.readset_refs if ref not in readset_refs]
                if missing:
                    raise TransactionRefusal("COMMIT_READSET_MISSING")
            response_body = canonical({k: v for k, v in response.items() if k != "hash"})
            self.db.execute(
                "INSERT OR IGNORE INTO response VALUES (?,?)",
                (response.get("hash", ""), response_body),
            )
            for row_id, body in target_rows:
                self.db.execute("INSERT INTO target_state VALUES (?,?)", (row_id, body))
            for row_id, body in journal_rows:
                self.db.execute("INSERT INTO target_journal VALUES (?,?)", (row_id, body))
            current = self._logical_readset()
            if current["schema"] != before["schema"]:
                raise TransactionRefusal("PUBLICATION_SCHEMA_CHANGED")
            for name in ("user_version", "application_id"):
                if current["metadata"][name] != before["metadata"][name]:
                    raise TransactionRefusal("PUBLICATION_METADATA_CHANGED")
            for table, rows in current["tables"].items():
                if not set(before["tables"].get(table, [])).issubset(set(rows)):
                    raise TransactionRefusal("PUBLICATION_NONADDITIVE_CHANGE")
            after = self._logical_readset()
            receipt = seal(
                {
                    "schema": TRANSACTION_SCHEMA,
                    "event_ref": event_hash,
                    "response_ref": response.get("hash", ""),
                    "before_hash": before_hash,
                    "after_hash": digest(after),
                    "target_branch": decision.branch.value,
                    "target_reason": decision.reason.value,
                    "readset_refs": list(readset_refs),
                    "record_hash": decision.record_hash,
                    "target_id": decision.target_id,
                    "authorization_hash": decision.authorization_hash,
                    "publication_grade": decision.publication_grade,
                }
            )
            self.db.execute(
                "INSERT INTO receipt VALUES (?,?)",
                (receipt["hash"], canonical({k: v for k, v in receipt.items() if k != "hash"})),
            )
            self.db.execute(
                "INSERT OR IGNORE INTO clock VALUES (?)", (event.get("time", 0),)
            )
            if fault == "after_receipt_before_commit":
                raise TransactionRefusal("INJECTED_STORAGE_FAILURE")
            self.db.execute("COMMIT")
            return CommitReceipt(
                status="COMMITTED",
                joint_transaction_id=receipt["hash"],
                admitted_event_ref=event_hash,
                before_hash=before_hash,
                after_hash=receipt["after_hash"],
                target_branch=decision.branch.value,
                target_reason=decision.reason.value,
                readset_refs=tuple(readset_refs),
                record_hash=decision.record_hash,
                receipt_hash=receipt["hash"],
                no_mutation=False,
                target_id=decision.target_id,
                authorization_hash=decision.authorization_hash,
                publication_grade=decision.publication_grade,
                response_ref=response.get("hash", ""),
            )
        except (TransactionRefusal, sqlite3.Error, KeyError, TypeError, ValueError) as error:
            if self.db.in_transaction:
                self.db.execute("ROLLBACK")
            after = self._logical_readset()
            no_ghost = after == before
            if not no_ghost:
                raise TransactionRefusal("ROLLBACK_INTEGRITY_FAILURE") from error
            return CommitReceipt(
                status="TRANSACTION_ABORTED_ROLLBACK",
                joint_transaction_id="",
                admitted_event_ref=event_hash,
                before_hash=before_hash,
                after_hash=digest(after),
                target_branch=decision.branch.value if decision else "",
                target_reason=str(error),
                readset_refs=tuple(readset_refs),
                record_hash="",
                receipt_hash="",
                no_mutation=True,
                target_id="",
                authorization_hash="",
                publication_grade="",
                response_ref="",
            )


__all__ = [
    "TRANSACTION_SCHEMA",
    "CandidateStore",
    "CommitReceipt",
    "TransactionRefusal",
]
