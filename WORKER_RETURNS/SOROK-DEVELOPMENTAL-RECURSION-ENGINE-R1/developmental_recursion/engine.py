"""Durable, owner-governed execution of one ordered developmental batch.

The engine is deliberately ignorant of psychology, sources, participants and
narrative.  It validates the frozen ``EventProposal`` boundary, reserves an
operation before the sole writer is called, and records the owner's immutable
result.  The owner decides every state change and scientific status.

Recovery is built around the owner's operation receipt.  A reservation is
committed before ``owner.realize`` is called.  If the process stops after that
point, the same operation identifier is offered to the owner again; the owner
must either resolve it from its own durable receipt or refuse it as ambiguous.
The engine never invents a replacement operation and never repeats an effect
on its own authority.
"""
from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import sqlite3
import threading
from typing import Any, Iterable, Mapping

from .contracts import (
    EventProposal,
    RealizedEvent,
    RecursionRefusal,
    StateIdentity,
    canonical,
    detached,
    digest,
)

try:  # macOS/Linux use the process file lock.  The in-process lock still holds elsewhere.
    import fcntl
except ImportError:  # pragma: no cover - exercised only on non-POSIX platforms.
    fcntl = None


SCHEMA = "SOROK_DEVELOPMENTAL_BATCH_JOURNAL@1"
STATUS_RESERVED = "RESERVED"
STATUS_COMPLETE = "COMPLETE"
BATCH_RUNNING = "RUNNING"
BATCH_COMPLETE = "COMPLETE"
CORE_STATUSES = frozenset(
    {"REALIZED", "IMMEDIATE_ONLY", "NO_CHANGE", "HELD", "REFUSED", "OMITTED"}
)
_STATE_KEYS = frozenset({"root", "actor", "branch", "clock", "state_hash"})
_PROPOSAL_KEYS = frozenset(
    {
        "event_id",
        "event_time",
        "operation",
        "source_refs",
        "participants",
        "circumstances",
        "interval",
    }
)
_RECORD_KEYS = frozenset(
    {
        "event_id",
        "operation_id",
        "proposal_hash",
        "before",
        "after",
        "status",
        "objective",
        "accessible",
        "consequences",
        "readset",
        "receipt_ref",
    }
)
_MAX_CLOCK = (1 << 63) - 1
_MAX_JSON_DEPTH = 100

_LOCKS: dict[str, threading.RLock] = {}
_LOCKS_GUARD = threading.Lock()


def _journal_lock(key: str) -> threading.RLock:
    with _LOCKS_GUARD:
        lock = _LOCKS.get(key)
        if lock is None:
            lock = threading.RLock()
            _LOCKS[key] = lock
        return lock


def _text(value: Any, code: str) -> str:
    if not isinstance(value, str) or not value or not value.strip():
        raise RecursionRefusal(code)
    return value


def _clock(value: Any, code: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise RecursionRefusal(code)
    if value < 0 or value > _MAX_CLOCK:
        raise RecursionRefusal(code)
    return value


def _json_value(value: Any, code: str, depth: int = 0) -> Any:
    """Return a detached JSON value, refusing non-finite or non-JSON material."""
    if depth > _MAX_JSON_DEPTH:
        raise RecursionRefusal(code + ":DEPTH")
    if value is None or isinstance(value, str):
        return value
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise RecursionRefusal(code + ":NONFINITE")
        return value
    if isinstance(value, Mapping):
        result = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise RecursionRefusal(code + ":NONSTRING_KEY")
            result[key] = _json_value(item, code, depth + 1)
        return result
    if isinstance(value, (list, tuple)):
        return [_json_value(item, code, depth + 1) for item in value]
    raise RecursionRefusal(code + ":NOT_JSON")


def _json_mapping(value: Any, code: str) -> dict:
    if not isinstance(value, Mapping):
        raise RecursionRefusal(code + ":NOT_OBJECT")
    return _json_value(value, code)


def _text_sequence(value: Any, code: str, *, allow_empty: bool = True) -> tuple[str, ...]:
    if not isinstance(value, (tuple, list)):
        raise RecursionRefusal(code + ":NOT_SEQUENCE")
    result = []
    for item in value:
        result.append(_text(item, code + ":ELEMENT"))
    if not allow_empty and not result:
        raise RecursionRefusal(code + ":EMPTY")
    return tuple(result)


def _state(value: Any, code: str) -> StateIdentity:
    if not isinstance(value, StateIdentity):
        raise RecursionRefusal(code + ":NOT_STATE_IDENTITY")
    root = _text(value.root, code + ":ROOT")
    actor = _text(value.actor, code + ":ACTOR")
    branch = _text(value.branch, code + ":BRANCH")
    clock = _clock(value.clock, code + ":CLOCK")
    state_hash = _text(value.state_hash, code + ":STATE_HASH")
    return StateIdentity(root, actor, branch, clock, state_hash)


def _state_from_document(value: Any, code: str) -> StateIdentity:
    if not isinstance(value, Mapping) or set(value) != _STATE_KEYS:
        raise RecursionRefusal(code + ":SCHEMA")
    return _state(
        StateIdentity(
            value["root"], value["actor"], value["branch"],
            value["clock"], value["state_hash"],
        ),
        code,
    )


def _proposal_from_document(value: Any, code: str) -> EventProposal:
    if not isinstance(value, Mapping) or set(value) != _PROPOSAL_KEYS:
        raise RecursionRefusal(code + ":SCHEMA")
    return _normalize_proposal(value, code)


def _load_json(value: Any, code: str) -> Any:
    try:
        return json.loads(value)
    except (TypeError, ValueError) as exc:
        raise RecursionRefusal(code + ":JSON") from exc


def _normalize_proposal(value: Any, code: str, *, mapping_ok: bool = True) -> EventProposal:
    if isinstance(value, EventProposal):
        event_id = value.event_id
        event_time = value.event_time
        operation = value.operation
        source_refs = value.source_refs
        participants = value.participants
        circumstances = value.circumstances
        interval = value.interval
    elif mapping_ok and isinstance(value, Mapping):
        keys = set(value)
        if keys not in (_PROPOSAL_KEYS, _PROPOSAL_KEYS - {"interval"}):
            raise RecursionRefusal(code + ":SCHEMA")
        event_id = value["event_id"]
        event_time = value["event_time"]
        operation = value["operation"]
        source_refs = value["source_refs"]
        participants = value["participants"]
        circumstances = value["circumstances"]
        interval = value.get("interval")
    else:
        raise RecursionRefusal(code + ":NOT_EVENT_PROPOSAL")

    event_id = _text(event_id, code + ":EVENT_ID")
    event_time = _clock(event_time, code + ":EVENT_TIME")
    operation = _text(operation, code + ":OPERATION")
    source_refs = _text_sequence(source_refs, code + ":SOURCE_REFS")
    participants = _text_sequence(participants, code + ":PARTICIPANTS")
    circumstances = _json_mapping(circumstances, code + ":CIRCUMSTANCES")
    if interval is not None:
        interval = _json_mapping(interval, code + ":INTERVAL")
    return EventProposal(
        event_id,
        event_time,
        operation,
        source_refs,
        participants,
        circumstances,
        interval,
    )


def _normalize_batch(value: Any) -> tuple[EventProposal, ...]:
    if not isinstance(value, (list, tuple)):
        raise RecursionRefusal("PROPOSALS_NOT_A_SEQUENCE")
    if len(value) < 3 or len(value) > 5:
        raise RecursionRefusal("PROPOSAL_COUNT_REQUIRES_3_TO_5")
    proposals = tuple(
        _normalize_proposal(item, f"PROPOSAL[{index}]")
        for index, item in enumerate(value)
    )
    event_ids = [proposal.event_id for proposal in proposals]
    if len(set(event_ids)) != len(event_ids):
        raise RecursionRefusal("DUPLICATE_EVENT_ID")
    return proposals


def _operation_id(batch_id: str, event_id: str) -> str:
    return "op:" + digest({"batch_id": batch_id, "event_id": event_id})


def _owner_proposal(proposal: EventProposal) -> EventProposal:
    """Give the owner detached material, never the engine's journal source."""
    return _proposal_from_document(proposal.document(), "OWNER_PROPOSAL")


def _validate_record_document(record: Any, code: str) -> dict:
    if not isinstance(record, Mapping) or set(record) != _RECORD_KEYS:
        raise RecursionRefusal(code + ":SCHEMA")
    event_id = _text(record["event_id"], code + ":EVENT_ID")
    operation_id = _text(record["operation_id"], code + ":OPERATION_ID")
    proposal_hash = _text(record["proposal_hash"], code + ":PROPOSAL_HASH")
    before = _state_from_document(record["before"], code + ":BEFORE")
    after = _state_from_document(record["after"], code + ":AFTER")
    if after.root != before.root or after.actor != before.actor or after.branch != before.branch:
        raise RecursionRefusal(code + ":IDENTITY_CHANGED")
    if after.clock < before.clock:
        raise RecursionRefusal(code + ":CLOCK_REGRESSION")
    status = _text(record["status"], code + ":STATUS")
    if status not in CORE_STATUSES:
        raise RecursionRefusal(code + ":STATUS")
    objective = _json_mapping(record["objective"], code + ":OBJECTIVE")
    accessible = _json_mapping(record["accessible"], code + ":ACCESSIBLE")
    consequences = _json_mapping(record["consequences"], code + ":CONSEQUENCES")
    readset = _text_sequence(record["readset"], code + ":READSET")
    receipt_ref = _text(record["receipt_ref"], code + ":RECEIPT")
    return {
        "event_id": event_id,
        "operation_id": operation_id,
        "proposal_hash": proposal_hash,
        "before": before.document(),
        "after": after.document(),
        "status": status,
        "objective": objective,
        "accessible": accessible,
        "consequences": consequences,
        "readset": list(readset),
        "receipt_ref": receipt_ref,
    }


class BatchEngine:
    """Execute and replay ordered batches against a supplied ``DevelopmentOwner``.

    ``owner`` is kept as the actual object at ``engine.owner``.  The engine does
    not wrap it, select actors, or supply any scientific rule.
    """

    def __init__(self, owner: Any, journal_path: str | os.PathLike[str]):
        for method in ("snapshot", "validate_proposal", "realize"):
            if not callable(getattr(owner, method, None)):
                raise RecursionRefusal("OWNER_PROTOCOL_INCOMPLETE:" + method)
        self.owner = owner

        raw_path = str(journal_path)
        if not raw_path or not raw_path.strip():
            raise RecursionRefusal("JOURNAL_PATH_REQUIRED")
        self._memory = raw_path == ":memory:"
        if self._memory:
            self._journal_path = ":memory:"
            self._lock_path = None
            self._lock_key = f"memory:{id(self)}"
            self._memory_conn: sqlite3.Connection | None = None
        else:
            path = Path(raw_path).expanduser()
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                raise RecursionRefusal("JOURNAL_PARENT_UNAVAILABLE:" + str(exc)) from exc
            path = path.resolve()
            self._journal_path = str(path)
            self._lock_path = str(path) + ".lock"
            self._lock_key = self._journal_path
            self._memory_conn = None
        self.journal_path = self._journal_path
        self._thread_lock = _journal_lock(self._lock_key)

        with self._exclusive():
            conn = self._connect()
            try:
                self._init_schema(conn)
                snapshot = self._snapshot_owner()
                self._binding = (snapshot.root, snapshot.actor, snapshot.branch)
                self._bind_journal(conn, snapshot)
            finally:
                self._release(conn)

    # ------------------------------------------------------------------
    # Public surface

    def run_batch(self, batch_id: str, proposals: Any) -> dict:
        batch_id = _text(batch_id, "BATCH_ID_REQUIRED")
        proposals = _normalize_batch(proposals)
        proposal_documents = [proposal.document() for proposal in proposals]
        proposal_hash = digest(proposal_documents)
        proposal_json = canonical(proposal_documents)

        with self._exclusive():
            conn = self._connect()
            try:
                self._verify_meta(conn)
                batch = self._read_batch(conn, batch_id)
                if batch is not None:
                    self._assert_batch_material(batch, proposals, proposal_hash, proposal_json)
                    records, pending, last_after, chain = self._load_batch(
                        conn, batch, proposals
                    )
                    if batch["status"] == BATCH_COMPLETE:
                        if pending is not None:
                            raise RecursionRefusal("JOURNAL_INTEGRITY:PENDING_IN_COMPLETE_BATCH")
                        snapshot = self._snapshot_owner()
                        self._check_binding(snapshot)
                        if snapshot.clock < last_after.clock:
                            raise RecursionRefusal("OWNER_CLOCK_REGRESSION")
                        return self._result(batch_id, records)
                    snapshot = self._snapshot_owner()
                    self._check_binding(snapshot)
                    if pending is not None:
                        pending_before = _state_from_document(
                            _load_json(
                                pending["before_json"], "JOURNAL_PENDING_BEFORE"
                            ),
                            "JOURNAL_PENDING_BEFORE",
                        )
                        if snapshot.clock < pending_before.clock:
                            raise RecursionRefusal("OWNER_CLOCK_REGRESSION")
                    else:
                        if snapshot != last_after:
                            raise RecursionRefusal("OWNER_STATE_DIVERGED_DURING_INTERRUPTION")
                    start_index = len(records)
                else:
                    snapshot = self._snapshot_owner()
                    self._check_binding(snapshot)
                    self._check_new_batch(conn, snapshot, proposals)
                    self._validate_all(proposals)
                    after_validation = self._snapshot_owner()
                    self._check_binding(after_validation)
                    if after_validation != snapshot:
                        raise RecursionRefusal("OWNER_MUTATED_DURING_VALIDATION")
                    self._claim_batch(
                        conn, batch_id, snapshot, proposal_hash, proposal_json
                    )
                    batch = self._read_batch(conn, batch_id)
                    if batch is None:
                        raise RecursionRefusal("JOURNAL_INTEGRITY:BATCH_CLAIM_LOST")
                    records = []
                    pending = None
                    last_after = snapshot
                    chain = proposal_hash
                    start_index = 0

                for index in range(start_index, len(proposals)):
                    proposal = proposals[index]
                    operation_id = _operation_id(batch_id, proposal.event_id)
                    event_hash = digest(proposal.document())
                    if pending is not None and index == start_index:
                        expected = _state_from_document(
                            _load_json(
                                pending["before_json"], "JOURNAL_PENDING_BEFORE"
                            ),
                            "JOURNAL_PENDING_BEFORE",
                        )
                    else:
                        expected = self._snapshot_owner()
                        self._check_binding(expected)
                        if index == 0:
                            start_document = _load_json(
                                batch["start_state_json"], "JOURNAL_START_STATE"
                            )
                            start_state = _state_from_document(
                                start_document, "JOURNAL_START_STATE"
                            )
                            if expected != start_state:
                                raise RecursionRefusal("OWNER_STATE_MOVED_BEFORE_FIRST_EVENT")
                        elif expected != last_after:
                            raise RecursionRefusal("OWNER_STATE_DIVERGED_BETWEEN_EVENTS")
                        pending = self._reserve_event(
                            conn,
                            batch_id,
                            index,
                            proposal,
                            operation_id,
                            event_hash,
                            expected,
                        )

                    try:
                        realized = self.owner.realize(
                            operation_id, _owner_proposal(proposal), expected
                        )
                    except BaseException as exc:
                        self._mark_error(conn, batch_id, index, exc)
                        if isinstance(exc, RecursionRefusal):
                            raise
                        if isinstance(exc, Exception):
                            raise RecursionRefusal(
                                "OWNER_REALIZE_FAILED:"
                                + type(exc).__name__
                                + ":"
                                + str(exc)
                            ) from exc
                        raise

                    try:
                        realized = self._validate_owner_result(
                            realized,
                            operation_id=operation_id,
                            proposal_hash=event_hash,
                            expected=expected,
                        )
                        current = self._snapshot_owner()
                        self._check_binding(current)
                        if current != realized.after:
                            raise RecursionRefusal(
                                "OWNER_RESULT_AFTER_NOT_CURRENT_STATE"
                            )
                        if current.clock < expected.clock:
                            raise RecursionRefusal("OWNER_CLOCK_REGRESSION")
                    except BaseException as exc:
                        self._mark_error(conn, batch_id, index, exc)
                        raise

                    record = realized.document()
                    record["event_id"] = proposal.event_id
                    record = _validate_record_document(record, "OWNER_RECORD")
                    next_chain = digest(
                        {
                            "batch_id": batch_id,
                            "event_index": index,
                            "previous": chain,
                            "record": record,
                        }
                    )
                    self._complete_event(
                        conn,
                        batch_id,
                        index,
                        realized,
                        record,
                        next_chain,
                    )
                    records.append(record)
                    last_after = realized.after
                    chain = next_chain
                    pending = None

                if len(records) != len(proposals):
                    raise RecursionRefusal("JOURNAL_INTEGRITY:INCOMPLETE_RECORD_SET")
                history_hash = digest(records)
                self._complete_batch(conn, batch_id, records, history_hash, chain)
                return self._result(batch_id, records)
            finally:
                self._release(conn)

    def history(self, batch_id: str) -> dict:
        batch_id = _text(batch_id, "BATCH_ID_REQUIRED")
        with self._exclusive(shared=True):
            conn = self._connect()
            try:
                self._verify_meta(conn)
                batch = self._read_batch(conn, batch_id)
                if batch is None:
                    raise RecursionRefusal("UNKNOWN_BATCH")
                proposals = self._stored_proposals(batch)
                self._assert_batch_material(
                    batch,
                    proposals,
                    digest([proposal.document() for proposal in proposals]),
                    canonical([proposal.document() for proposal in proposals]),
                )
                records, pending, last_after, _chain = self._load_batch(
                    conn, batch, proposals
                )
                snapshot = self._snapshot_owner()
                self._check_binding(snapshot)
                if snapshot.clock < last_after.clock:
                    raise RecursionRefusal("OWNER_CLOCK_REGRESSION")
                if batch["status"] == BATCH_RUNNING:
                    if pending is not None:
                        pending_before = _state_from_document(
                            _load_json(
                                pending["before_json"], "JOURNAL_PENDING_BEFORE"
                            ),
                            "JOURNAL_PENDING_BEFORE",
                        )
                        if snapshot.clock < pending_before.clock:
                            raise RecursionRefusal("OWNER_CLOCK_REGRESSION")
                    elif snapshot != last_after:
                        raise RecursionRefusal("OWNER_STATE_DIVERGED_DURING_INTERRUPTION")
                return self._result(batch_id, records)
            finally:
                self._release(conn)

    def verify(self) -> bool:
        with self._exclusive(shared=True):
            conn = self._connect()
            try:
                self._verify_meta(conn)
                snapshot = self._snapshot_owner()
                self._check_binding(snapshot)
                orphan = conn.execute(
                    "SELECT e.batch_id FROM events e LEFT JOIN batches b "
                    "ON b.batch_id=e.batch_id WHERE b.batch_id IS NULL LIMIT 1"
                ).fetchone()
                if orphan is not None:
                    raise RecursionRefusal("JOURNAL_INTEGRITY:ORPHAN_EVENT")
                rows = conn.execute(
                    "SELECT * FROM batches ORDER BY rowid"
                ).fetchall()
                running = []
                latest_clock = 0
                for batch in rows:
                    proposals = self._stored_proposals(batch)
                    records, pending, last_after, _chain = self._load_batch(
                        conn, batch, proposals
                    )
                    latest_clock = max(latest_clock, last_after.clock)
                    if batch["status"] == BATCH_RUNNING:
                        running.append((batch, pending, last_after))
                if len(running) > 1:
                    raise RecursionRefusal("JOURNAL_INTEGRITY:MULTIPLE_RUNNING_BATCHES")
                if running:
                    batch, pending, last_after = running[0]
                    if pending is not None:
                        pending_before = _state_from_document(
                            _load_json(
                                pending["before_json"], "JOURNAL_PENDING_BEFORE"
                            ),
                            "JOURNAL_PENDING_BEFORE",
                        )
                        if snapshot.clock < pending_before.clock:
                            raise RecursionRefusal("OWNER_CLOCK_REGRESSION")
                        latest_clock = max(latest_clock, pending_before.clock)
                    elif snapshot != last_after:
                        raise RecursionRefusal("OWNER_STATE_DIVERGED_DURING_INTERRUPTION")
                if snapshot.clock < latest_clock:
                    raise RecursionRefusal("OWNER_CLOCK_REGRESSION")
                return True
            finally:
                self._release(conn)

    def close(self) -> None:
        if self._memory and self._memory_conn is not None:
            self._memory_conn.close()
            self._memory_conn = None

    def __enter__(self) -> "BatchEngine":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    # ------------------------------------------------------------------
    # Owner and binding

    def _snapshot_owner(self) -> StateIdentity:
        try:
            snapshot = self.owner.snapshot()
        except RecursionRefusal:
            raise
        except Exception as exc:
            raise RecursionRefusal(
                "OWNER_SNAPSHOT_FAILED:" + type(exc).__name__ + ":" + str(exc)
            ) from exc
        return _state(snapshot, "OWNER_SNAPSHOT_INVALID")

    def _check_binding(self, snapshot: StateIdentity) -> None:
        if (snapshot.root, snapshot.actor, snapshot.branch) != self._binding:
            raise RecursionRefusal("OWNER_ROOT_ACTOR_BRANCH_MISMATCH")

    def _validate_all(self, proposals: Iterable[EventProposal]) -> None:
        for proposal in proposals:
            try:
                verdict = self.owner.validate_proposal(_owner_proposal(proposal))
            except RecursionRefusal:
                raise
            except Exception as exc:
                raise RecursionRefusal(
                    "OWNER_VALIDATION_FAILED:"
                    + type(exc).__name__
                    + ":"
                    + str(exc)
                ) from exc
            if verdict is False:
                raise RecursionRefusal("OWNER_PROPOSAL_REFUSED")

    def _validate_owner_result(
        self,
        result: Any,
        *,
        operation_id: str,
        proposal_hash: str,
        expected: StateIdentity,
    ) -> RealizedEvent:
        code = "OWNER_RESULT_INVALID"
        if not isinstance(result, RealizedEvent):
            raise RecursionRefusal(code + ":NOT_REALIZED_EVENT")
        if _text(result.operation_id, code + ":OPERATION_ID") != operation_id:
            raise RecursionRefusal("OWNER_RESULT_OPERATION_MISMATCH")
        if _text(result.proposal_hash, code + ":PROPOSAL_HASH") != proposal_hash:
            raise RecursionRefusal("OWNER_RESULT_PROPOSAL_MISMATCH")
        before = _state(result.before, code + ":BEFORE")
        if before != expected:
            raise RecursionRefusal("OWNER_RESULT_BEFORE_MISMATCH")
        after = _state(result.after, code + ":AFTER")
        if (after.root, after.actor, after.branch) != self._binding:
            raise RecursionRefusal("OWNER_RESULT_IDENTITY_CHANGED")
        if after.clock < before.clock:
            raise RecursionRefusal("OWNER_RESULT_CLOCK_REGRESSION")
        status = _text(result.status, code + ":STATUS")
        if status not in CORE_STATUSES:
            raise RecursionRefusal("OWNER_RESULT_STATUS_INVALID")
        objective = _json_mapping(result.objective, code + ":OBJECTIVE")
        accessible = _json_mapping(result.accessible, code + ":ACCESSIBLE")
        consequences = _json_mapping(result.consequences, code + ":CONSEQUENCES")
        readset = _text_sequence(result.readset, code + ":READSET")
        receipt_ref = _text(result.receipt_ref, code + ":RECEIPT")
        return RealizedEvent(
            operation_id=operation_id,
            proposal_hash=proposal_hash,
            before=before,
            after=after,
            status=status,
            objective=objective,
            accessible=accessible,
            consequences=consequences,
            readset=readset,
            receipt_ref=receipt_ref,
        )

    # ------------------------------------------------------------------
    # Journal lifecycle

    def _connect(self) -> sqlite3.Connection:
        if self._memory:
            if self._memory_conn is None:
                self._memory_conn = sqlite3.connect(
                    ":memory:",
                    timeout=30.0,
                    isolation_level=None,
                    check_same_thread=False,
                )
                self._memory_conn.row_factory = sqlite3.Row
            conn = self._memory_conn
        else:
            conn = sqlite3.connect(
                self._journal_path,
                timeout=30.0,
                isolation_level=None,
            )
            conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA busy_timeout=30000")
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("PRAGMA synchronous=FULL")
        return conn

    def _release(self, conn: sqlite3.Connection) -> None:
        if not (self._memory and conn is self._memory_conn):
            conn.close()

    @contextmanager
    def _exclusive(self, *, shared: bool = False):
        with self._thread_lock:
            descriptor = None
            try:
                if fcntl is not None and self._lock_path is not None:
                    descriptor = os.open(
                        self._lock_path, os.O_CREAT | os.O_RDWR, 0o600
                    )
                    fcntl.flock(
                        descriptor, fcntl.LOCK_SH if shared else fcntl.LOCK_EX
                    )
                yield
            finally:
                if descriptor is not None:
                    try:
                        fcntl.flock(descriptor, fcntl.LOCK_UN)
                    finally:
                        os.close(descriptor)

    def _init_schema(self, conn: sqlite3.Connection) -> None:
        if not self._memory:
            conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("BEGIN IMMEDIATE")
        try:
            version = conn.execute("PRAGMA user_version").fetchone()[0]
            existing = {
                row["name"]
                for row in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' "
                    "AND name IN ('meta','batches','events')"
                )
            }
            if version not in (0, 1):
                raise RecursionRefusal("JOURNAL_SCHEMA_UNSUPPORTED")
            if version == 0 and existing:
                raise RecursionRefusal("JOURNAL_SCHEMA_UNMARKED")
            conn.execute(
                "CREATE TABLE IF NOT EXISTS meta ("
                "key TEXT PRIMARY KEY, value TEXT NOT NULL)"
            )
            conn.execute(
                "CREATE TABLE IF NOT EXISTS batches ("
                "batch_id TEXT PRIMARY KEY,"
                "proposal_hash TEXT NOT NULL,"
                "proposal_json TEXT NOT NULL,"
                "root TEXT NOT NULL,"
                "actor TEXT NOT NULL,"
                "branch TEXT NOT NULL,"
                "start_state_json TEXT NOT NULL,"
                "status TEXT NOT NULL,"
                "history_hash TEXT,"
                "chain_head TEXT,"
                "created_at TEXT NOT NULL,"
                "last_error TEXT)"
            )
            conn.execute(
                "CREATE TABLE IF NOT EXISTS events ("
                "batch_id TEXT NOT NULL,"
                "event_index INTEGER NOT NULL,"
                "event_id TEXT NOT NULL,"
                "operation_id TEXT NOT NULL,"
                "proposal_hash TEXT NOT NULL,"
                "proposal_json TEXT NOT NULL,"
                "before_json TEXT NOT NULL,"
                "before_clock INTEGER NOT NULL,"
                "after_clock INTEGER,"
                "status TEXT NOT NULL,"
                "result_json TEXT,"
                "record_json TEXT,"
                "chain_hash TEXT,"
                "receipt_ref TEXT,"
                "readset_json TEXT,"
                "last_error TEXT,"
                "PRIMARY KEY (batch_id, event_index),"
                "UNIQUE (event_id),"
                "UNIQUE (operation_id),"
                "FOREIGN KEY (batch_id) REFERENCES batches(batch_id) ON DELETE CASCADE)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS events_batch_order "
                "ON events(batch_id, event_index)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS events_after_clock "
                "ON events(after_clock)"
            )
            conn.execute("PRAGMA user_version=1")
            conn.execute("COMMIT")
        except BaseException:
            conn.execute("ROLLBACK")
            raise

    def _bind_journal(
        self, conn: sqlite3.Connection, snapshot: StateIdentity
    ) -> None:
        rows = {
            row["key"]: row["value"]
            for row in conn.execute("SELECT key, value FROM meta")
        }
        expected = {
            "schema": SCHEMA,
            "root": snapshot.root,
            "actor": snapshot.actor,
            "branch": snapshot.branch,
        }
        if not rows:
            has_data = conn.execute(
                "SELECT 1 FROM batches LIMIT 1"
            ).fetchone()
            if has_data is not None:
                raise RecursionRefusal("JOURNAL_INTEGRITY:MISSING_BINDING")
            conn.execute("BEGIN IMMEDIATE")
            try:
                for key, value in expected.items():
                    conn.execute(
                        "INSERT INTO meta(key, value) VALUES (?, ?)", (key, value)
                    )
                conn.execute("COMMIT")
            except BaseException:
                conn.execute("ROLLBACK")
                raise
            return
        for key, value in expected.items():
            if rows.get(key) != value:
                raise RecursionRefusal("OWNER_JOURNAL_BINDING_MISMATCH:" + key)

    def _verify_meta(self, conn: sqlite3.Connection) -> None:
        rows = {
            row["key"]: row["value"]
            for row in conn.execute("SELECT key, value FROM meta")
        }
        if rows.get("schema") != SCHEMA:
            raise RecursionRefusal("JOURNAL_INTEGRITY:SCHEMA_META")
        binding = (rows.get("root"), rows.get("actor"), rows.get("branch"))
        if binding != self._binding:
            raise RecursionRefusal("OWNER_JOURNAL_BINDING_MISMATCH")

    # ------------------------------------------------------------------
    # Batch material and claims

    def _stored_proposals(self, batch: sqlite3.Row) -> tuple[EventProposal, ...]:
        try:
            document = json.loads(batch["proposal_json"])
        except (TypeError, ValueError) as exc:
            raise RecursionRefusal("JOURNAL_INTEGRITY:PROPOSAL_JSON") from exc
        if not isinstance(document, list) or not 3 <= len(document) <= 5:
            raise RecursionRefusal("JOURNAL_INTEGRITY:PROPOSAL_COUNT")
        proposals = tuple(
            _proposal_from_document(item, f"JOURNAL_PROPOSAL[{index}]")
            for index, item in enumerate(document)
        )
        event_ids = [proposal.event_id for proposal in proposals]
        if len(set(event_ids)) != len(event_ids):
            raise RecursionRefusal("JOURNAL_INTEGRITY:DUPLICATE_EVENT_ID")
        return proposals

    def _assert_batch_material(
        self,
        batch: sqlite3.Row,
        proposals: tuple[EventProposal, ...],
        proposal_hash: str,
        proposal_json: str,
    ) -> None:
        if batch["proposal_hash"] != proposal_hash:
            raise RecursionRefusal("BATCH_REUSE_MISMATCH")
        if batch["proposal_json"] != proposal_json:
            raise RecursionRefusal("BATCH_REUSE_MISMATCH")
        if (batch["root"], batch["actor"], batch["branch"]) != self._binding:
            raise RecursionRefusal("OWNER_JOURNAL_BINDING_MISMATCH")
        start = _state_from_document(
            _load_json(batch["start_state_json"], "JOURNAL_START_STATE"),
            "JOURNAL_START_STATE",
        )
        if (start.root, start.actor, start.branch) != self._binding:
            raise RecursionRefusal("JOURNAL_INTEGRITY:START_IDENTITY")
        if batch["status"] not in {BATCH_RUNNING, BATCH_COMPLETE}:
            raise RecursionRefusal("JOURNAL_INTEGRITY:BATCH_STATUS")
        if len(proposals) < 3 or len(proposals) > 5:
            raise RecursionRefusal("JOURNAL_INTEGRITY:PROPOSAL_COUNT")

    def _check_new_batch(
        self,
        conn: sqlite3.Connection,
        snapshot: StateIdentity,
        proposals: tuple[EventProposal, ...],
    ) -> None:
        running = conn.execute(
            "SELECT batch_id FROM batches WHERE status=? LIMIT 1",
            (BATCH_RUNNING,),
        ).fetchone()
        if running is not None:
            raise RecursionRefusal(
                "INTERRUPTED_BATCH_REQUIRES_RECOVERY:" + running["batch_id"]
            )
        for prior in conn.execute("SELECT * FROM batches ORDER BY rowid").fetchall():
            prior_proposals = self._stored_proposals(prior)
            self._load_batch(conn, prior, prior_proposals)
        row = conn.execute("SELECT MAX(after_clock) AS clock FROM events").fetchone()
        maximum = row["clock"] if row is not None else None
        if maximum is not None and snapshot.clock < maximum:
            raise RecursionRefusal("OWNER_CLOCK_REGRESSION")
        placeholders = ",".join("?" for _ in proposals)
        conflict = conn.execute(
            "SELECT event_id FROM events WHERE event_id IN (" + placeholders + ") LIMIT 1",
            [proposal.event_id for proposal in proposals],
        ).fetchone()
        if conflict is not None:
            raise RecursionRefusal("EVENT_ID_CONFLICT:" + conflict["event_id"])

    def _claim_batch(
        self,
        conn: sqlite3.Connection,
        batch_id: str,
        snapshot: StateIdentity,
        proposal_hash: str,
        proposal_json: str,
    ) -> None:
        now = datetime.now(timezone.utc).isoformat()
        conn.execute("BEGIN IMMEDIATE")
        try:
            conn.execute(
                "INSERT INTO batches("
                "batch_id, proposal_hash, proposal_json, root, actor, branch,"
                "start_state_json, status, history_hash, chain_head, created_at,"
                "last_error) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    batch_id,
                    proposal_hash,
                    proposal_json,
                    snapshot.root,
                    snapshot.actor,
                    snapshot.branch,
                    canonical(snapshot.document()),
                    BATCH_RUNNING,
                    None,
                    None,
                    now,
                    None,
                ),
            )
            conn.execute("COMMIT")
        except sqlite3.IntegrityError as exc:
            conn.execute("ROLLBACK")
            raise RecursionRefusal("BATCH_ID_CONFLICT") from exc
        except BaseException:
            conn.execute("ROLLBACK")
            raise

    def _reserve_event(
        self,
        conn: sqlite3.Connection,
        batch_id: str,
        index: int,
        proposal: EventProposal,
        operation_id: str,
        proposal_hash: str,
        before: StateIdentity,
    ) -> sqlite3.Row:
        conn.execute("BEGIN IMMEDIATE")
        try:
            conn.execute(
                "INSERT INTO events("
                "batch_id, event_index, event_id, operation_id, proposal_hash,"
                "proposal_json, before_json, before_clock, after_clock, status,"
                "result_json, record_json, chain_hash, receipt_ref, readset_json,"
                "last_error) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    batch_id,
                    index,
                    proposal.event_id,
                    operation_id,
                    proposal_hash,
                    canonical(proposal.document()),
                    canonical(before.document()),
                    before.clock,
                    None,
                    STATUS_RESERVED,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                ),
            )
            conn.execute("COMMIT")
        except sqlite3.IntegrityError as exc:
            conn.execute("ROLLBACK")
            raise RecursionRefusal("EVENT_ID_CONFLICT:" + proposal.event_id) from exc
        except BaseException:
            conn.execute("ROLLBACK")
            raise
        row = self._read_event(conn, batch_id, index)
        if row is None:
            raise RecursionRefusal("JOURNAL_INTEGRITY:RESERVATION_LOST")
        return row

    def _complete_event(
        self,
        conn: sqlite3.Connection,
        batch_id: str,
        index: int,
        result: RealizedEvent,
        record: dict,
        chain_hash: str,
    ) -> None:
        result_json = canonical(result.document())
        record_json = canonical(record)
        readset_json = canonical(record["readset"])
        conn.execute("BEGIN IMMEDIATE")
        try:
            cursor = conn.execute(
                "UPDATE events SET status=?, result_json=?, record_json=?,"
                "chain_hash=?, receipt_ref=?, readset_json=?, after_clock=?,"
                "last_error=NULL WHERE batch_id=? AND event_index=? AND status=?",
                (
                    STATUS_COMPLETE,
                    result_json,
                    record_json,
                    chain_hash,
                    record["receipt_ref"],
                    readset_json,
                    result.after.clock,
                    batch_id,
                    index,
                    STATUS_RESERVED,
                ),
            )
            if cursor.rowcount != 1:
                raise RecursionRefusal("JOURNAL_INTEGRITY:EVENT_COMPLETION")
            conn.execute("COMMIT")
        except BaseException:
            conn.execute("ROLLBACK")
            raise

    def _complete_batch(
        self,
        conn: sqlite3.Connection,
        batch_id: str,
        records: list[dict],
        history_hash: str,
        chain_head: str,
    ) -> None:
        conn.execute("BEGIN IMMEDIATE")
        try:
            cursor = conn.execute(
                "UPDATE batches SET status=?, history_hash=?, chain_head=?,"
                "last_error=NULL WHERE batch_id=? AND status=?",
                (BATCH_COMPLETE, history_hash, chain_head, batch_id, BATCH_RUNNING),
            )
            if cursor.rowcount != 1:
                row = conn.execute(
                    "SELECT status, history_hash, chain_head FROM batches "
                    "WHERE batch_id=?",
                    (batch_id,),
                ).fetchone()
                if (
                    row is None
                    or row["status"] != BATCH_COMPLETE
                    or row["history_hash"] != history_hash
                    or row["chain_head"] != chain_head
                ):
                    raise RecursionRefusal("JOURNAL_INTEGRITY:BATCH_COMPLETION")
            conn.execute("COMMIT")
        except BaseException:
            conn.execute("ROLLBACK")
            raise

    def _mark_error(
        self,
        conn: sqlite3.Connection,
        batch_id: str,
        index: int | None,
        exc: BaseException,
    ) -> None:
        message = (type(exc).__name__ + ":" + str(exc))[:1000]
        try:
            conn.execute("BEGIN IMMEDIATE")
            try:
                if index is not None:
                    conn.execute(
                        "UPDATE events SET last_error=? WHERE batch_id=? AND event_index=?",
                        (message, batch_id, index),
                    )
                conn.execute(
                    "UPDATE batches SET last_error=? WHERE batch_id=?",
                    (message, batch_id),
                )
                conn.execute("COMMIT")
            except BaseException:
                conn.execute("ROLLBACK")
        except BaseException:
            # Evidence persistence must never hide the owner/coherence error.
            pass

    # ------------------------------------------------------------------
    # Journal reads and integrity

    def _read_batch(
        self, conn: sqlite3.Connection, batch_id: str
    ) -> sqlite3.Row | None:
        return conn.execute(
            "SELECT * FROM batches WHERE batch_id=?", (batch_id,)
        ).fetchone()

    def _read_event(
        self, conn: sqlite3.Connection, batch_id: str, index: int
    ) -> sqlite3.Row | None:
        return conn.execute(
            "SELECT * FROM events WHERE batch_id=? AND event_index=?",
            (batch_id, index),
        ).fetchone()

    def _load_batch(
        self,
        conn: sqlite3.Connection,
        batch: sqlite3.Row,
        proposals: tuple[EventProposal, ...],
    ) -> tuple[list[dict], sqlite3.Row | None, StateIdentity, str]:
        code = "JOURNAL_INTEGRITY"
        batch_id = batch["batch_id"]
        if batch["status"] not in {BATCH_RUNNING, BATCH_COMPLETE}:
            raise RecursionRefusal(code + ":BATCH_STATUS")
        if (batch["root"], batch["actor"], batch["branch"]) != self._binding:
            raise RecursionRefusal(code + ":BATCH_IDENTITY")
        proposal_documents = [proposal.document() for proposal in proposals]
        if batch["proposal_hash"] != digest(proposal_documents):
            raise RecursionRefusal(code + ":BATCH_PROPOSAL_HASH")
        if batch["proposal_json"] != canonical(proposal_documents):
            raise RecursionRefusal(code + ":BATCH_PROPOSAL_JSON")
        start = _state_from_document(
            _load_json(batch["start_state_json"], code + ":START_STATE"),
            code + ":START_STATE",
        )
        if (start.root, start.actor, start.branch) != self._binding:
            raise RecursionRefusal(code + ":START_IDENTITY")
        previous_after = start
        previous_chain = batch["proposal_hash"]
        records: list[dict] = []
        pending: sqlite3.Row | None = None
        rows = conn.execute(
            "SELECT * FROM events WHERE batch_id=? ORDER BY event_index",
            (batch_id,),
        ).fetchall()
        for expected_index, row in enumerate(rows):
            if expected_index >= len(proposals):
                raise RecursionRefusal(code + ":EXTRA_EVENT")
            if row["event_index"] != expected_index:
                raise RecursionRefusal(code + ":EVENT_GAP")
            proposal = proposals[expected_index]
            expected_hash = digest(proposal.document())
            operation_id = _operation_id(batch_id, proposal.event_id)
            if row["event_id"] != proposal.event_id:
                raise RecursionRefusal(code + ":EVENT_ID")
            if row["operation_id"] != operation_id:
                raise RecursionRefusal(code + ":OPERATION_ID")
            if row["proposal_hash"] != expected_hash:
                raise RecursionRefusal(code + ":PROPOSAL_HASH")
            if row["proposal_json"] != canonical(proposal.document()):
                raise RecursionRefusal(code + ":PROPOSAL_JSON")
            before = _state_from_document(
                _load_json(row["before_json"], code + ":BEFORE"), code + ":BEFORE"
            )
            if before != previous_after:
                raise RecursionRefusal(code + ":BEFORE_CHAIN")
            if row["before_clock"] != before.clock:
                raise RecursionRefusal(code + ":BEFORE_CLOCK")
            if row["status"] == STATUS_RESERVED:
                if pending is not None or len(rows) != expected_index + 1:
                    raise RecursionRefusal(code + ":PENDING_ORDER")
                pending = row
                break
            if row["status"] != STATUS_COMPLETE:
                raise RecursionRefusal(code + ":EVENT_STATUS")
            record = self._read_completed_record(
                row,
                proposal,
                operation_id,
                expected_hash,
                before,
                previous_chain,
                expected_index,
            )
            records.append(record)
            previous_after = _state_from_document(
                record["after"], code + ":RECORD_AFTER"
            )
            if previous_after.clock < before.clock:
                raise RecursionRefusal(code + ":RECORD_CLOCK")
            previous_chain = row["chain_hash"]
        if pending is None and len(rows) > len(records):
            raise RecursionRefusal(code + ":UNREAD_EVENT")
        if batch["status"] == BATCH_COMPLETE:
            if pending is not None:
                raise RecursionRefusal(code + ":PENDING_IN_COMPLETE")
            if len(records) != len(proposals):
                raise RecursionRefusal(code + ":INCOMPLETE_COMPLETE_BATCH")
            if batch["history_hash"] != digest(records):
                raise RecursionRefusal(code + ":HISTORY_HASH")
            expected_head = rows[-1]["chain_hash"] if rows else batch["proposal_hash"]
            if batch["chain_head"] != expected_head:
                raise RecursionRefusal(code + ":CHAIN_HEAD")
        else:
            if batch["history_hash"] is not None or batch["chain_head"] is not None:
                raise RecursionRefusal(code + ":RUNNING_HAS_COMPLETION")
        return records, pending, previous_after, previous_chain

    def _read_completed_record(
        self,
        row: sqlite3.Row,
        proposal: EventProposal,
        operation_id: str,
        proposal_hash: str,
        before: StateIdentity,
        previous_chain: str,
        index: int,
    ) -> dict:
        code = "JOURNAL_INTEGRITY"
        try:
            record = json.loads(row["record_json"])
            result = json.loads(row["result_json"])
            readset = json.loads(row["readset_json"])
        except (TypeError, ValueError) as exc:
            raise RecursionRefusal(code + ":RECORD_JSON") from exc
        record = _validate_record_document(record, code + ":RECORD")
        if record["event_id"] != proposal.event_id:
            raise RecursionRefusal(code + ":RECORD_EVENT_ID")
        if record["operation_id"] != operation_id:
            raise RecursionRefusal(code + ":RECORD_OPERATION_ID")
        if record["proposal_hash"] != proposal_hash:
            raise RecursionRefusal(code + ":RECORD_PROPOSAL_HASH")
        if record["before"] != before.document():
            raise RecursionRefusal(code + ":RECORD_BEFORE")
        if canonical(record["after"]) != canonical(
            _state_from_document(record["after"], code + ":RECORD_AFTER").document()
        ):
            raise RecursionRefusal(code + ":RECORD_AFTER_DOCUMENT")
        if row["record_json"] != canonical(record):
            raise RecursionRefusal(code + ":RECORD_CANONICAL")
        if result != {key: value for key, value in record.items() if key != "event_id"}:
            raise RecursionRefusal(code + ":RESULT_DOCUMENT")
        if row["receipt_ref"] != record["receipt_ref"]:
            raise RecursionRefusal(code + ":RECEIPT")
        if readset != record["readset"]:
            raise RecursionRefusal(code + ":READSET")
        if row["after_clock"] != record["after"]["clock"]:
            raise RecursionRefusal(code + ":AFTER_CLOCK")
        expected_chain = digest(
            {
                "batch_id": row["batch_id"],
                "event_index": index,
                "previous": previous_chain,
                "record": record,
            }
        )
        if row["chain_hash"] != expected_chain:
            raise RecursionRefusal(code + ":CHAIN")
        after = _state_from_document(record["after"], code + ":RECORD_AFTER")
        if (after.root, after.actor, after.branch) != self._binding:
            raise RecursionRefusal(code + ":RECORD_IDENTITY")
        return record

    def _result(self, batch_id: str, records: list[dict]) -> dict:
        detached_records = detached(records)
        return {
            "batch_id": batch_id,
            "history_hash": digest(detached_records),
            "records": detached_records,
        }
