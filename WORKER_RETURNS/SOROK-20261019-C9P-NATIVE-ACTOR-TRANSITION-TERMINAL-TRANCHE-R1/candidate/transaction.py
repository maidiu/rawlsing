"""Atomic candidate transaction with occurrence, effect, no-ghost rollback and readset.

The store commits the admitted occurrence, the response receipt, and any accepted
target effect inside one `BEGIN IMMEDIATE` transaction. A refusal or injected
storage fault rolls back to the exact pre-state and verifies no ghost rows were
left behind. The committed readset is bound into the joint receipt.
"""
from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .canon import canonical, digest, seal, valid
from .target_rules import TargetBranch, TargetDecision

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

    @property
    def committed(self) -> bool:
        return self.status == "COMMITTED"


class CandidateStore:
    """SQLite-backed candidate store with atomic publication and no-ghost rollback.

    Admission of the occurrence is a separate prior step, so response rollback
    preserves the occurrence record. One event per invocation; unresolved
    same-time transitions fail closed.
    """

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.db = sqlite3.connect(str(self.path), isolation_level=None)
        self.db.executescript(
            """
            CREATE TABLE IF NOT EXISTS occurrence (hash TEXT PRIMARY KEY, body TEXT NOT NULL);
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

    def admit_occurrence(self, event: Mapping[str, Any]) -> dict:
        """Commit one admitted occurrence before any response transaction."""
        if not isinstance(event, Mapping) or not valid(event):
            raise TransactionRefusal("EVENT_INTEGRITY_FAILURE")
        event_hash = event.get("hash", "")
        body = canonical({k: v for k, v in event.items() if k != "hash"})
        self.db.execute(
            "INSERT OR IGNORE INTO occurrence VALUES (?,?)", (event_hash, body)
        )
        row = self.db.execute(
            "SELECT body FROM occurrence WHERE hash=?", (event_hash,)
        ).fetchone()
        if row is None or row[0] != body:
            raise TransactionRefusal("OCCURRENCE_ADMISSION_FAILED")
        return dict(event)

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
        """Read one committed target record. Returns None when the id is absent."""
        row = self.db.execute(
            "SELECT body FROM target_state WHERE id=?", (middle_state_id,)
        ).fetchone()
        return json.loads(row[0]) if row else None

    def committed_event_hashes(self) -> frozenset[str]:
        rows = self.db.execute("SELECT hash FROM occurrence").fetchall()
        return frozenset(row[0] for row in rows)

    def commit(
        self,
        *,
        event: Mapping[str, Any],
        response: Mapping[str, Any],
        decision: TargetDecision,
        readset_refs: tuple[str, ...],
        fault: str | None = None,
    ) -> CommitReceipt:
        """Commit occurrence, response and accepted target effect atomically.

        On any refusal or injected fault the transaction rolls back, the store is
        verified byte-identical at the logical level and a `TRANSACTION_ABORTED_ROLLBACK`
        receipt is returned. A committed receipt binds the exact readset.
        """
        before_snapshot = self.snapshot()
        before_hash = digest(before_snapshot)
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
            if not valid(response):
                raise TransactionRefusal("RESPONSE_INTEGRITY_FAILURE")
            if response.get("event_ref") != event_hash:
                raise TransactionRefusal("RESPONSE_EVENT_MISMATCH")
            target_rows: list[dict] = []
            journal_rows: list[dict] = []
            if decision.branch is TargetBranch.CREATE:
                if not decision.record_hash:
                    raise TransactionRefusal("TARGET_RECORD_MISSING")
                if decision.before_target_hash != self.target_state_hash():
                    raise TransactionRefusal("STALE_TARGET_PRESTATE")
                record = {
                    "schema": "C9P_TARGET_RECORD@1",
                    "record_hash": decision.record_hash,
                    "actor_id": decision.actor_id,
                    "middle_state_id": decision.proposal_hash,
                    "state_kind_id": decision.state_kind_id,
                    "permission_ref": decision.permission_ref,
                    "before_target_hash": decision.before_target_hash,
                    "after_target_hash": decision.after_target_hash,
                }
                sealed_record = seal(record)
                target_rows.append(
                    (decision.proposal_hash, canonical({k: v for k, v in sealed_record.items() if k != "hash"}))
                )
                journal_rows.append(
                    (
                        decision.record_hash,
                        canonical(
                            {
                                "record_hash": decision.record_hash,
                                "proposal_hash": decision.proposal_hash,
                                "branch": decision.branch.value,
                                "reason": decision.reason.value,
                                "readset_refs": list(decision.readset_refs),
                            }
                        ),
                    )
                )
            elif decision.branch is TargetBranch.DENY:
                if decision.record_hash:
                    raise TransactionRefusal("DENY_WITH_RECORD")
            response_body = canonical({k: v for k, v in response.items() if k != "hash"})
            self.db.execute(
                "INSERT OR IGNORE INTO response VALUES (?,?)",
                (response.get("hash", ""), response_body),
            )
            for row_id, body in target_rows:
                self.db.execute(
                    "INSERT INTO target_state VALUES (?,?)", (row_id, body)
                )
            for row_id, body in journal_rows:
                self.db.execute(
                    "INSERT INTO target_journal VALUES (?,?)", (row_id, body)
                )
            after_snapshot_rows = self.snapshot()
            receipt = seal(
                {
                    "schema": TRANSACTION_SCHEMA,
                    "event_ref": event_hash,
                    "response_ref": response.get("hash", ""),
                    "before_hash": before_hash,
                    "after_hash": digest(after_snapshot_rows),
                    "target_branch": decision.branch.value,
                    "target_reason": decision.reason.value,
                    "readset_refs": list(readset_refs),
                    "record_hash": decision.record_hash,
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
            )
        except (TransactionRefusal, sqlite3.Error, KeyError, TypeError, ValueError) as error:
            if self.db.in_transaction:
                self.db.execute("ROLLBACK")
            after = self.snapshot()
            no_ghost = after == before_snapshot
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
            )


__all__ = [
    "TRANSACTION_SCHEMA",
    "CandidateStore",
    "CommitReceipt",
    "TransactionRefusal",
]
