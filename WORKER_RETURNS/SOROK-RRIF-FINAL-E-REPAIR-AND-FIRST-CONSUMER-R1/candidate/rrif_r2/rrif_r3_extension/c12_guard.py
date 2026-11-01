"""Sourcefree C12 owner-court guard.

This candidate does not edit the pinned BP4 store. It supplies a read-only
verification and fork-guard add-on that is explicit about the three separate
questions a C12 row can answer:

1. content: does the stored preimage hash to the stored hash?
2. fork: does a child branch's copied prefix, including perceptions, match its
   parent at the declared fork clock?
3. authenticity/completeness: is there an owner-issued external anchor that
   covers the exact chain digest? This module never invents a key or a signer.
   Without an owner-issued anchor the answer is ``OWNER_ANCHOR_REQUIRED``.

The writer schema is the pinned ``BP4_C12_STORE@1``. The reader is this file's
``C12_GUARD_READER@1``. Unknown schema versions fail closed. Legacy episode-id
forms are classified and refused; no migration is performed without a separate
owner decision.
"""
from __future__ import annotations

import json
from typing import Any, Callable

from bp4.store import C12Store, StoreRefusal

WRITER_SCHEMA = "BP4_C12_STORE@1"
SUPPORTED_WRITER_SCHEMAS = frozenset({WRITER_SCHEMA})
READER_VERSION = "C12_GUARD_READER@1"
EPISODE_PREFIX = "TEST_ONLY_BP4_EP_"
FORK_ROOT_SCHEMA = "BP4_C12_FORK_ROOT@2"
FORK_ROOT_PREFIX = FORK_ROOT_SCHEMA + ":"
ANCHOR_SCHEMA = "SOROK_C12_EXTERNAL_ANCHOR@1"
C9_MIRROR_SCHEMA = "C12_ACTOR_MIRROR_R3@1"
C9_MIRROR_SOURCE_DOMAIN = WRITER_SCHEMA
FORK_TABLES = ("episode", "world_event", "perception", "checkpoint")
_FORK_IDENTITY = {
    "episode": (1, 2, 3, 4, 5, 7),
    "world_event": (1, 2, 3, 5),
    "perception": (1, 2, 3, 4, 5),
    "checkpoint": (1, 2, 4),
}
_FORK_CLOCK_INDEX = {"episode": 4, "world_event": 2, "perception": 3,
                     "checkpoint": 1}
_ROW_COLUMNS = {
    "episode": ("seq", "episode_id", "actor_id", "kind", "clock", "hash"),
    "world_event": ("seq", "event_id", "clock", "hash"),
    "perception": ("seq", "actor_id", "event_id", "clock", "channel"),
    "checkpoint": ("seq", "clock", "hash"),
}


def _digest(value: Any) -> str:
    from bp1.canon import digest
    return digest(value)


def _canonical(value: Any) -> str:
    from bp1.canon import canonical
    return canonical(value)


def _row_dicts(store: C12Store, branch_id: str, table: str) -> list[dict]:
    cursor = store.db.execute(
        f"SELECT * FROM {table} WHERE branch_id=? ORDER BY seq", (branch_id,))
    names = [description[0] for description in cursor.description]
    return [dict(zip(names, row)) for row in cursor.fetchall()]


def check_schema(store: C12Store) -> dict:
    """Fail closed unless the writer schema is the one this reader knows."""
    errors: list[str] = []
    try:
        meta = dict(store.db.execute("SELECT key,value FROM meta").fetchall())
    except Exception as error:  # noqa: BLE001 - a malformed store is a refusal
        return {"ok": False, "errors": ["schema_meta_unreadable:" + str(error)],
                "writer_schema": None, "reader_version": READER_VERSION}
    schema = meta.get("schema")
    if schema is None:
        errors.append("schema_meta_missing")
    elif schema != WRITER_SCHEMA:
        errors.append("schema_version_unsupported:" + str(schema))
    user_version = store.db.execute("PRAGMA user_version").fetchone()[0]
    application_id = store.db.execute("PRAGMA application_id").fetchone()[0]
    if user_version != 0:
        errors.append("sqlite_user_version_unsupported:" + str(user_version))
    if application_id != 0:
        errors.append("sqlite_application_id_unsupported:" + str(application_id))
    return {"ok": not errors, "errors": errors, "writer_schema": schema,
            "reader_version": READER_VERSION}


def expected_episode_id(body_hash: str) -> str:
    return EPISODE_PREFIX + str(body_hash)


def _episode_origin_for_seq(store: C12Store, branch_id: str, seq: int,
                            seen: frozenset[str] = frozenset()) -> str:
    """Return the immutable branch that originally authored this episode row.

    The SQL ``branch_id`` column is the current storage location. The sealed
    episode body's ``branch_id`` is the immutable origin. A copied row keeps the
    parent body's origin while its location changes to the child branch. Local
    child rows have the child as origin. This function resolves that origin from
    the exact fork prefix counts; it never rewrites the hashed body.
    """
    if branch_id in seen:
        raise StoreRefusal("FORK_HELD", "episode_origin_ancestry_cycle")
    branch = store._branch(branch_id)
    if branch is None:
        raise StoreRefusal("FORK_HELD", "episode_origin_branch_missing")
    parent_id = branch["parent_branch_id"]
    if parent_id in (None, ""):
        return branch_id
    counts = branch["root_counts"]
    if not isinstance(counts, dict):
        raise StoreRefusal("FORK_HELD", "episode_origin_root_counts_invalid")
    copied = counts.get("episode", 0)
    if type(copied) is not int or copied < 0:
        raise StoreRefusal("FORK_HELD", "episode_origin_root_counts_invalid")
    if seq < copied:
        return _episode_origin_for_seq(
            store, parent_id, seq, seen | {branch_id})
    return branch_id


def _check_row_columns(table: str, row: dict, parsed: dict,
                       errors: list[str],
                       *, expected_origin_branch_id: str | None = None) -> None:
    seq = row["seq"]
    if table == "episode":
        expected = expected_episode_id(parsed.get("hash", ""))
        if row["episode_id"] != expected:
            errors.append(f"episode:{seq}:episode_id_column_mismatch")
        if parsed.get("episode_id") != expected:
            errors.append(f"episode:{seq}:episode_id_body_mismatch")
        origin = parsed.get("branch_id")
        expected_origin = (
            expected_origin_branch_id
            if expected_origin_branch_id is not None
            else row["branch_id"]
        )
        if not isinstance(origin, str) or not origin:
            errors.append(f"episode:{seq}:branch_id_origin_missing")
        elif origin != expected_origin:
            errors.append(f"episode:{seq}:branch_id_origin_mismatch")
        # ``row["branch_id"]`` is the current storage location; the sealed
        # body's branch_id is the immutable origin. Only the origin, actor,
        # kind and clock are body/column identity constraints.
        for column, key in (("actor_id", "actor_id"),
                            ("kind", "kind"), ("clock", "clock")):
            if parsed.get(key) != row[column]:
                errors.append(f"episode:{seq}:{column}_column_body_mismatch")
    elif table == "world_event":
        for column in ("event_id", "clock"):
            if parsed.get(column) != row[column]:
                errors.append(f"world_event:{seq}:{column}_column_body_mismatch")
        if parsed.get("sequence") is not None and parsed["sequence"] != seq:
            errors.append(f"world_event:{seq}:sequence_body_mismatch")
    elif table == "checkpoint":
        if parsed.get("clock") != row["clock"]:
            errors.append(f"checkpoint:{seq}:clock_column_body_mismatch")


def verify_rows(store: C12Store, branch_id: str) -> dict:
    store.branch(branch_id)
    errors: list[str] = []
    counts: dict[str, int] = {}
    for table, column in (("episode", "body"), ("world_event", "body"),
                          ("checkpoint", "state")):
        rows = _row_dicts(store, branch_id, table)
        counts[table] = len(rows)
        for row in rows:
            parsed = json.loads(row[column])
            body_hash = parsed.get("hash")
            preimage = {key: value for key, value in parsed.items()
                        if key != "hash"}
            if table == "episode":
                preimage.pop("episode_id", None)
            if body_hash != _digest(preimage):
                errors.append(f"{table}:{row['seq']}:body_hash_mismatch")
            if row["hash"] != body_hash:
                errors.append(f"{table}:{row['seq']}:column_hash_mismatch")
            if table == "episode":
                try:
                    origin = _episode_origin_for_seq(
                        store, branch_id, int(row["seq"]))
                except StoreRefusal as error:
                    errors.append(
                        f"episode:{row['seq']}:origin_unresolved:{error.code}")
                    origin = None
                _check_row_columns(
                    table, row, parsed, errors,
                    expected_origin_branch_id=origin)
            else:
                _check_row_columns(table, row, parsed, errors)
        if [row["seq"] for row in rows] != list(range(len(rows))):
            errors.append(f"{table}:seq_not_contiguous")
    perceptions = _row_dicts(store, branch_id, "perception")
    counts["perception"] = len(perceptions)
    if [row["seq"] for row in perceptions] != list(range(len(perceptions))):
        errors.append("perception:seq_not_contiguous")
    branch = store.branch(branch_id)
    actors = set(branch["actor_ids"])
    events = {row["event_id"] for row in _row_dicts(store, branch_id,
                                                    "world_event")}
    for row in perceptions:
        if row["event_id"] not in events:
            errors.append(f"perception:{row['seq']}:event_not_in_branch")
        if row["actor_id"] not in actors:
            errors.append(f"perception:{row['seq']}:actor_not_in_branch")
    return {"ok": not errors, "errors": errors, "counts": counts,
            "branch_id": branch_id}


def chain_digest(store: C12Store, branch_id: str) -> str:
    """Full ordered identity digest, including perception clocks and channels."""
    store.branch(branch_id)
    rows: list[list[Any]] = []
    for table in ("episode", "world_event", "perception", "checkpoint"):
        for row in _row_dicts(store, branch_id, table):
            rows.append([table] + [row[column] for column in _ROW_COLUMNS[table]])
    return _digest(rows)


def _fork_rows(store: C12Store, branch_id: str, table: str,
               limit: int | None = None) -> list[tuple]:
    sql = f"SELECT * FROM {table} WHERE branch_id=? ORDER BY seq"
    values: tuple = (branch_id,)
    if limit is not None:
        sql += " LIMIT ?"
        values += (int(limit),)
    return [tuple(row) for row in store.db.execute(sql, values)]


def _fork_identity(table: str, row: tuple) -> list:
    return [row[index] for index in _FORK_IDENTITY[table]]


def _fork_payload(parent: dict, fork_clock: int, counts: dict[str, int],
                  rows: dict[str, list[tuple]]) -> dict:
    return {
        "schema": FORK_ROOT_SCHEMA,
        "parent_branch": parent["branch_id"],
        "parent_root_hash": parent["root_hash"] or "",
        "fork_clock": int(fork_clock),
        "counts": {table: int(counts[table]) for table in FORK_TABLES},
        "rows": {table: [_fork_identity(table, row) for row in rows[table]]
                 for table in FORK_TABLES},
    }


def fork_integrity(store: C12Store, branch_id: str) -> dict:
    """Verify the child prefix, perception clocks, ancestry and root hash."""
    errors: list[str] = []
    status = "VERIFIED"
    seen: set[str] = set()
    current_id = branch_id
    while True:
        if current_id in seen:
            errors.append(f"fork:{current_id}:ancestry_cycle")
            status = "INVALID"
            break
        seen.add(current_id)
        current = store._branch(current_id)
        if current is None:
            errors.append(f"fork:{current_id}:branch_missing")
            status = "INVALID"
            break
        parent_id = current["parent_branch_id"]
        if parent_id in (None, ""):
            if current["root_hash"]:
                errors.append(f"fork:{current_id}:root_hash_on_root_branch")
            if current["root_counts"]:
                errors.append(f"fork:{current_id}:root_counts_on_root_branch")
            break
        root_hash = current["root_hash"] or ""
        if not root_hash.startswith(FORK_ROOT_PREFIX):
            errors.append(f"fork:{current_id}:legacy_root_unverified")
            status = "LEGACY_HELD"
            break
        parent = store._branch(parent_id)
        if parent is None:
            errors.append(f"fork:{current_id}:parent_missing")
            status = "INVALID"
            break
        counts = current["root_counts"]
        if (not isinstance(counts, dict) or set(counts) != set(FORK_TABLES)
                or any(type(counts[t]) is not int or counts[t] < 0
                       for t in FORK_TABLES)):
            errors.append(f"fork:{current_id}:root_counts_invalid")
            status = "INVALID"
            break
        parent_rows: dict[str, list[tuple]] = {}
        child_rows: dict[str, list[tuple]] = {}
        for table in FORK_TABLES:
            limit = counts[table]
            parent_rows[table] = _fork_rows(store, parent_id, table, limit)
            child_rows[table] = _fork_rows(store, current_id, table, limit)
            if len(parent_rows[table]) != limit:
                errors.append(f"fork:{current_id}:{table}:parent_prefix_short")
            if len(child_rows[table]) != limit:
                errors.append(f"fork:{current_id}:{table}:child_prefix_short")
            if (len(parent_rows[table]) != limit
                    or len(child_rows[table]) != limit
                    or [_fork_identity(table, row) for row in parent_rows[table]]
                    != [_fork_identity(table, row) for row in child_rows[table]]):
                errors.append(f"fork:{current_id}:{table}:prefix_mismatch")
        if errors:
            status = "INVALID"
            break
        clock_values = [
            _fork_identity(table, row)[_FORK_CLOCK_INDEX[table]]
            for table in FORK_TABLES for row in parent_rows[table]
        ]
        expected_clock = max(clock_values, default=0)
        if current["fork_clock"] != expected_clock:
            errors.append(f"fork:{current_id}:fork_clock_mismatch")
        if current["created_clock"] != current["fork_clock"]:
            errors.append(f"fork:{current_id}:created_clock_mismatch")
        expected = FORK_ROOT_PREFIX + _digest(_fork_payload(
            parent, current["fork_clock"], counts, parent_rows))
        if root_hash != expected:
            errors.append(f"fork:{current_id}:root_hash_mismatch")
        if errors:
            status = "INVALID"
            break
        current_id = parent_id
    if errors and status == "VERIFIED":
        status = "INVALID"
    return {"ok": not errors, "status": status, "errors": errors,
            "branch_id": branch_id}


def verify_store(store: C12Store, branch_id: str) -> dict:
    """Content + fork verification only; never an authenticity claim."""
    schema = check_schema(store)
    rows = verify_rows(store, branch_id)
    fork = fork_integrity(store, branch_id)
    errors = list(schema["errors"]) + list(rows["errors"]) + list(fork["errors"])
    return {
        "ok": not errors,
        "content_ok": rows["ok"],
        "fork_ok": fork["ok"],
        "schema_ok": schema["ok"],
        "errors": errors,
        "counts": rows["counts"],
        "fork": fork,
        "branch_id": branch_id,
        "reader_version": READER_VERSION,
        "authenticity": {"state": "UNVERIFIED",
                         "code": "OWNER_ANCHOR_REQUIRED"},
        "completeness": {"state": "UNVERIFIED",
                         "code": "OWNER_ANCHOR_REQUIRED"},
    }


def anchor_payload(store: C12Store, branch_id: str) -> dict:
    """The exact owner-visible object an external anchor must cover.

    The branch identity fields are included so a raw branch-table mutation of
    ``actor_ids`` or ``created_clock`` changes the anchor payload; the previous
    payload omitted both and could not detect that substitution.
    """
    report = verify_store(store, branch_id)
    branch = store.branch(branch_id)
    return {
        "schema": ANCHOR_SCHEMA,
        "reader_version": READER_VERSION,
        "branch_id": branch_id,
        "branch_identity": {
            "actor_ids": list(branch["actor_ids"]),
            "created_clock": int(branch["created_clock"]),
            "fork_clock": branch["fork_clock"],
            "root_hash": branch["root_hash"],
        },
        "chain": chain_digest(store, branch_id),
        "counts": report["counts"],
        "fork_status": report["fork"]["status"],
    }


def check_anchor(anchor: dict | None, payload: dict,
                 verify_signature: Callable[[dict], bool] | None,
                 *, min_sequence: int | None = None) -> dict:
    """Fail closed unless a real owner trust root verifies the exact anchor.

    This function deliberately cannot create a key, sign, or accept a test
    fixture as an owner. The caller must supply an out-of-band verifier bound
    to the original owner/anchor custodian. ``None`` is a HOLD, not a pass.
    """
    if anchor is None:
        return {"ok": False, "state": "HOLD", "code": "OWNER_ANCHOR_REQUIRED",
                "security_boundary": False}
    if not isinstance(anchor, dict):
        return {"ok": False, "state": "HOLD", "code": "ANCHOR_MALFORMED",
                "security_boundary": False}
    for key in ("schema", "issuer", "key_id", "signature", "payload",
                "sequence"):
        if anchor.get(key) is None or anchor.get(key) == "":
            return {"ok": False, "state": "HOLD",
                    "code": "ANCHOR_MALFORMED:" + key,
                    "security_boundary": False}
    if type(anchor["sequence"]) is not int or anchor["sequence"] < 0:
        return {"ok": False, "state": "HOLD",
                "code": "ANCHOR_MALFORMED:sequence",
                "security_boundary": False}
    if anchor["schema"] != ANCHOR_SCHEMA:
        return {"ok": False, "state": "HOLD",
                "code": "ANCHOR_SCHEMA_UNSUPPORTED:" + str(anchor["schema"]),
                "security_boundary": False}
    if _canonical(anchor["payload"]) != _canonical(payload):
        return {"ok": False, "state": "HOLD",
                "code": "ANCHOR_PAYLOAD_MISMATCH",
                "security_boundary": False}
    if min_sequence is None:
        return {"ok": False, "state": "HOLD",
                "code": "ANCHOR_ROLLBACK_WINDOW_UNPROVEN",
                "security_boundary": False}
    if anchor["sequence"] < int(min_sequence):
        return {"ok": False, "state": "HOLD",
                "code": "ANCHOR_ROLLBACK",
                "security_boundary": False}
    if verify_signature is None:
        return {"ok": False, "state": "HOLD",
                "code": "OWNER_TRUST_ROOT_ABSENT",
                "security_boundary": False}
    try:
        valid = verify_signature(anchor)
    except Exception:  # noqa: BLE001 - verifier failure is a refusal
        valid = False
    if valid is not True:
        return {"ok": False, "state": "HOLD",
                "code": "ANCHOR_SIGNATURE_INVALID",
                "security_boundary": False}
    return {"ok": True, "state": "AUTHENTICATED",
            "code": "OWNER_ANCHOR_VERIFIED", "issuer": anchor["issuer"],
            "key_id": anchor["key_id"], "security_boundary": True}



def check_c9_mirror_handshake(mirror_meta: dict, writer_schema: str) -> dict:
    """Check the C9 mirror reader's declared C12 source domain.

    The C9 mirror is a separate database. This check does not create a mirror
    or claim cross-database atomicity; it only refuses a version mismatch before
    a caller treats a mirror row as a C12 projection.
    """
    errors: list[str] = []
    if mirror_meta.get("schema") != C9_MIRROR_SCHEMA:
        errors.append("c9_mirror_schema_unsupported:" + str(
            mirror_meta.get("schema")))
    if writer_schema not in SUPPORTED_WRITER_SCHEMAS:
        errors.append("c12_writer_schema_unsupported:" + str(writer_schema))
    declared_domain = mirror_meta.get("c12_source_domain")
    if declared_domain not in SUPPORTED_WRITER_SCHEMAS:
        errors.append("c9_mirror_c12_domain_unsupported:" + str(
            declared_domain))
    if declared_domain != writer_schema:
        errors.append("c9_mirror_c12_domain_mismatch:" + str(
            mirror_meta.get("c12_source_domain")))
    return {"ok": not errors, "errors": errors,
            "mirror_schema": mirror_meta.get("schema"),
            "c12_source_domain": mirror_meta.get("c12_source_domain"),
            "writer_schema": writer_schema}


def two_store_readiness(mirror_meta: dict, writer_schema: str, *,
                        watermark_state: str, outbox_state: str) -> dict:
    """No cross-DB ACID: only CLEAN + ACKED is a materialized read."""
    handshake = check_c9_mirror_handshake(mirror_meta, writer_schema)
    errors = list(handshake["errors"])
    if watermark_state != "CLEAN":
        errors.append("c12_watermark_not_clean:" + watermark_state)
    if outbox_state != "ACKED":
        errors.append("c9_outbox_not_acked:" + outbox_state)
    return {"ok": not errors, "state": "READY" if not errors else "SYNC_HELD",
            "errors": errors, "atomicity": "NO_CROSS_DATABASE_ACID__OUTBOX_AND_WATERMARK"}


def classify_episode_ids(store: C12Store, branch_id: str) -> dict:
    """Report legacy/non-lawful ids without rewriting any row."""
    rows = _row_dicts(store, branch_id, "episode")
    legacy = []
    for row in rows:
        parsed = json.loads(row["body"])
        expected = expected_episode_id(parsed.get("hash", ""))
        if row["episode_id"] != expected or parsed.get("episode_id") != expected:
            legacy.append({"seq": row["seq"], "episode_id": row["episode_id"],
                           "body_episode_id": parsed.get("episode_id"),
                           "expected": expected})
    return {"ok": not legacy, "legacy_rows": legacy,
            "migration": "OWNER_ISSUED_MIGRATION_REQUIRED" if legacy else
            "NOT_REQUIRED",
            "write_performed": False}


class GuardedC12Store(C12Store):
    """BP4 C12 store with owner-court verification and atomic fork repair."""

    def verify(self, branch_id: str) -> dict:
        return verify_store(self, branch_id)

    def append_episode(self, branch_id: str, *, actor_id: str, kind: str,
                       clock: int, body: dict) -> dict:
        """Reject a non-monotonic episode against perception and all rows.

        The inherited ``_last_clock`` excludes perception rows, so a perception
        at 11 followed by an episode at 10 was accepted. The same clock domain
        must use every append-only row as the lower bound.
        """
        latest_perception = self.db.execute(
            "SELECT coalesce(max(clock),0) FROM perception WHERE branch_id=?",
            (branch_id,)).fetchone()[0]
        latest = max(self.last_clock(branch_id), int(latest_perception))
        if int(clock) < latest:
            raise StoreRefusal("NON_MONOTONIC_GLOBAL_CLOCK")
        return super().append_episode(
            branch_id, actor_id=actor_id, kind=kind, clock=clock, body=body)

    def fork(self, parent_branch_id: str, new_branch_id: str) -> dict:
        savepoint = "c12_guard_fork"
        self.db.execute(f"SAVEPOINT {savepoint}")
        try:
            parent = self.branch(parent_branch_id)
            if self._branch(new_branch_id) is not None:
                raise StoreRefusal("BRANCH_EXISTS")
            schema = check_schema(self)
            if not schema["ok"]:
                raise StoreRefusal("SCHEMA_UNSUPPORTED")
            parent_fork = fork_integrity(self, parent_branch_id)
            if not parent_fork["ok"]:
                raise StoreRefusal("FORK_HELD", "parent_fork_integrity_unverified")
            latest_perception = self.db.execute(
                "SELECT coalesce(max(clock),0) FROM perception WHERE branch_id=?",
                (parent_branch_id,)).fetchone()[0]
            fork_clock = max(self.last_clock(parent_branch_id),
                             int(latest_perception))
            rows = {table: _fork_rows(self, parent_branch_id, table)
                    for table in FORK_TABLES}
            counts = {table: len(rows[table]) for table in FORK_TABLES}
            root_hash = FORK_ROOT_PREFIX + _digest(
                _fork_payload(parent, fork_clock, counts, rows))
            self.db.execute(
                "INSERT INTO branch VALUES (?,?,?,?,?,?,?)",
                (new_branch_id, parent_branch_id, int(fork_clock), root_hash,
                 _canonical(counts), int(fork_clock),
                 _canonical(parent["actor_ids"])))
            for table in FORK_TABLES:
                self._copy_fork_rows(table, new_branch_id, rows[table])
            created = self.branch(new_branch_id)
            self.db.execute(f"RELEASE {savepoint}")
        except Exception:
            try:
                self.db.execute(f"ROLLBACK TO {savepoint}")
                self.db.execute(f"RELEASE {savepoint}")
            except Exception:  # noqa: BLE001 - preserve original fork failure
                pass
            raise
        return created

    def _copy_fork_rows(self, table: str, new_branch_id: str,
                        rows: list[tuple]) -> None:
        columns = {"episode": 8, "world_event": 6, "perception": 6,
                   "checkpoint": 5}[table]
        placeholders = ",".join("?" for _ in range(columns))
        for row in rows:
            values = list(row)
            values[0] = new_branch_id
            self.db.execute(
                f"INSERT INTO {table} VALUES ({placeholders})", tuple(values))


__all__ = [
    "ANCHOR_SCHEMA", "EPISODE_PREFIX", "FORK_ROOT_PREFIX", "FORK_ROOT_SCHEMA",
    "GuardedC12Store", "READER_VERSION", "SUPPORTED_WRITER_SCHEMAS",
    "WRITER_SCHEMA", "anchor_payload",
    "C9_MIRROR_SCHEMA", "C9_MIRROR_SOURCE_DOMAIN", "chain_digest",
    "check_anchor", "check_c9_mirror_handshake", "check_schema",
    "classify_episode_ids",
    "expected_episode_id", "fork_integrity", "two_store_readiness",
    "verify_rows", "verify_store",
]
