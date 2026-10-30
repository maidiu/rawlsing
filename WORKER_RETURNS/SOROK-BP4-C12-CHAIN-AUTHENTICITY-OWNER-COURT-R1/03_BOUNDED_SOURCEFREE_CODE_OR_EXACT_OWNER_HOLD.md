# Bounded sourcefree code candidate or exact owner HOLD

## Decision

This return carries **both**:

1. a bounded sourcefree engineering candidate for the checkable parts — episode preimage, derived episode id, schema version, fork prefix/perception clocks, atomic fork, fail-closed anchor refusal; and
2. an exact owner HOLD for the uncheckable parts — a real C12 anchor trust root, monotonic anchor counter, legacy migration authority, upstream BP4 verifier disposition and native/production receiver.

No key, signature, issuer, secret, source-native authority or test fixture oracle is invented. The candidate is not adopted and does not change the original BP4 store or any original branch.

## Candidate files and exact bytes

The candidate was executed in a throwaway checkout of `5b3e6577400ea1d88971ae6b48e41a118b8059ae`. It consists of:

| Part | Path | Git blob | SHA-256 |
|---|---|---|---|
| F2 preimage overlay (prior verified candidate) | `bp2p4/c12_verify.py` | `c1699c8da5e944ed079708e272c3af50d5a30a44` | `6ad07d75f3ebb785e847e761e2db65df37abf8eea72559df3a6c54f031141d20` |
| F2 focused test | `tests/test_episode_verifier_regression.py` | `ebe1e8287f9b8485b6c862b66b6c2a9dafcf59aa` | `b55f148f5623458259c7fe3b05b340c19c3bc1a5f721a12145f50df7caa28c58` |
| New guard reader | `bp2p4/c12_guard.py` | `a6a8de75ad92967e9fde354d76adce8b9572217e` | `7fd5dd55912e5d8a16ece9eb47909728fc69ca5031064c809b6d2673232a8021` |
| New guard test | `tests/test_c12_guard.py` | `8ca11491af25b98825c88f1355e391ce82659ab7` | `fa4b6d8e347be254a40bdf9e0aaa8ee077c8a4ea3fdd11fb8bf5422df91ca82a` |

The generated combined patch (F2 verifier diff plus the two guard files) has SHA-256 `00b365d660a97957a28b684e5b8454b60cd7ec0fa94652074d8a9f1a452ac194`. The F2 test is extracted byte-exactly from immutable blob `ebe1e828…` in commit `0636d257…` and is not duplicated in the patch. The F2 verifier diff is applied from the repository root; the guard patch is applied with `--directory=WORKER_RETURNS/SOROK-20261020-BP2P4J-ACTUAL-JOINED-ALPHA-R1`. No original file outside the F2 one-line verifier overlay is edited.

## Part A — F2 preimage overlay (required for the legacy verifier API)

```diff
diff --git a/WORKER_RETURNS/SOROK-20261020-BP2P4J-ACTUAL-JOINED-ALPHA-R1/bp2p4/c12_verify.py b/WORKER_RETURNS/SOROK-20261020-BP2P4J-ACTUAL-JOINED-ALPHA-R1/bp2p4/c12_verify.py
index b8e7cf397..c1699c8da 100644
--- a/WORKER_RETURNS/SOROK-20261020-BP2P4J-ACTUAL-JOINED-ALPHA-R1/bp2p4/c12_verify.py
+++ b/WORKER_RETURNS/SOROK-20261020-BP2P4J-ACTUAL-JOINED-ALPHA-R1/bp2p4/c12_verify.py
@@ -4,7 +4,10 @@ BP4's ``C12Store.verify`` recomputes ``digest(body)`` where ``body`` still
 contains its own ``hash`` field, so the recomputation is self-referential and
 every non-empty table reports an error. This module verifies the chain the way
 the rows were actually written (``digest(body without hash) == body.hash``) and
-provides an out-of-band chain digest for deletion detection.
+provides an out-of-band chain digest for deletion detection. Episodes hash
+before their derived ``episode_id`` is appended, so the episode preimage
+excludes both ``hash`` and ``episode_id``; the verifier separately requires the
+stored id to equal the pinned derivation from the body hash.
 
 This is a verification add-on over BP4's durable store. It does not modify BP4.
 Completeness (that no row was deleted by someone with raw database access) is
@@ -29,6 +32,8 @@ TABLES = {
     "perception": ("seq", "event_id"),
 }
 
+EPISODE_ID_PREFIX = "TEST_ONLY_BP4_EP_"
+
 
 def _rows(store, branch_id: str, table: str) -> list[tuple]:
     columns = {
@@ -53,10 +58,16 @@ def verify_branch_chain(store, branch_id: str) -> dict:
         for seq, body, stored_hash in rows:
             parsed = json.loads(body)
             body_hash = parsed.get("hash")
-            recomputed = digest({key: value for key, value in parsed.items()
-                                 if key != "hash"})
+            recomputed = digest({
+                key: value for key, value in parsed.items()
+                if key != "hash"
+                and not (table == "episode" and key == "episode_id")
+            })
             if body_hash != recomputed:
                 errors.append(f"{table}:{seq}:body_hash_mismatch")
+            if table == "episode":
+                if parsed.get("episode_id") != f"{EPISODE_ID_PREFIX}{body_hash}":
+                    errors.append(f"{table}:{seq}:episode_id_mismatch")
             if stored_hash != body_hash:
                 errors.append(f"{table}:{seq}:column_hash_mismatch")
         if [row[0] for row in rows] != list(range(len(rows))):
```

## Part B — C12 guard reader, schema/fork/anchor candidate (additive)

```diff
diff --git a/bp2p4/c12_guard.py b/bp2p4/c12_guard.py
new file mode 100644
index 000000000..a6a8de75a
--- /dev/null
+++ b/bp2p4/c12_guard.py
@@ -0,0 +1,489 @@
+"""Sourcefree C12 owner-court guard.
+
+This candidate does not edit the pinned BP4 store. It supplies a read-only
+verification and fork-guard add-on that is explicit about the three separate
+questions a C12 row can answer:
+
+1. content: does the stored preimage hash to the stored hash?
+2. fork: does a child branch's copied prefix, including perceptions, match its
+   parent at the declared fork clock?
+3. authenticity/completeness: is there an owner-issued external anchor that
+   covers the exact chain digest? This module never invents a key or a signer.
+   Without an owner-issued anchor the answer is ``OWNER_ANCHOR_REQUIRED``.
+
+The writer schema is the pinned ``BP4_C12_STORE@1``. The reader is this file's
+``C12_GUARD_READER@1``. Unknown schema versions fail closed. Legacy episode-id
+forms are classified and refused; no migration is performed without a separate
+owner decision.
+"""
+from __future__ import annotations
+
+import json
+from typing import Any, Callable
+
+from bp4.store import C12Store, StoreRefusal
+
+WRITER_SCHEMA = "BP4_C12_STORE@1"
+READER_VERSION = "C12_GUARD_READER@1"
+EPISODE_PREFIX = "TEST_ONLY_BP4_EP_"
+FORK_ROOT_SCHEMA = "BP4_C12_FORK_ROOT@2"
+FORK_ROOT_PREFIX = FORK_ROOT_SCHEMA + ":"
+ANCHOR_SCHEMA = "SOROK_C12_EXTERNAL_ANCHOR@1"
+C9_MIRROR_SCHEMA = "C12_ACTOR_MIRROR_R3@1"
+C9_MIRROR_SOURCE_DOMAIN = WRITER_SCHEMA
+FORK_TABLES = ("episode", "world_event", "perception", "checkpoint")
+_FORK_IDENTITY = {
+    "episode": (1, 2, 3, 4, 5, 7),
+    "world_event": (1, 2, 3, 5),
+    "perception": (1, 2, 3, 4, 5),
+    "checkpoint": (1, 2, 4),
+}
+_FORK_CLOCK_INDEX = {"episode": 4, "world_event": 2, "perception": 3,
+                     "checkpoint": 1}
+_ROW_COLUMNS = {
+    "episode": ("seq", "episode_id", "actor_id", "kind", "clock", "hash"),
+    "world_event": ("seq", "event_id", "clock", "hash"),
+    "perception": ("seq", "actor_id", "event_id", "clock", "channel"),
+    "checkpoint": ("seq", "clock", "hash"),
+}
+
+
+def _digest(value: Any) -> str:
+    from bp1.canon import digest
+    return digest(value)
+
+
+def _canonical(value: Any) -> str:
+    from bp1.canon import canonical
+    return canonical(value)
+
+
+def _row_dicts(store: C12Store, branch_id: str, table: str) -> list[dict]:
+    cursor = store.db.execute(
+        f"SELECT * FROM {table} WHERE branch_id=? ORDER BY seq", (branch_id,))
+    names = [description[0] for description in cursor.description]
+    return [dict(zip(names, row)) for row in cursor.fetchall()]
+
+
+def check_schema(store: C12Store) -> dict:
+    """Fail closed unless the writer schema is the one this reader knows."""
+    errors: list[str] = []
+    try:
+        meta = dict(store.db.execute("SELECT key,value FROM meta").fetchall())
+    except Exception as error:  # noqa: BLE001 - a malformed store is a refusal
+        return {"ok": False, "errors": ["schema_meta_unreadable:" + str(error)],
+                "writer_schema": None, "reader_version": READER_VERSION}
+    schema = meta.get("schema")
+    if schema is None:
+        errors.append("schema_meta_missing")
+    elif schema != WRITER_SCHEMA:
+        errors.append("schema_version_unsupported:" + str(schema))
+    user_version = store.db.execute("PRAGMA user_version").fetchone()[0]
+    application_id = store.db.execute("PRAGMA application_id").fetchone()[0]
+    if user_version != 0:
+        errors.append("sqlite_user_version_unsupported:" + str(user_version))
+    if application_id != 0:
+        errors.append("sqlite_application_id_unsupported:" + str(application_id))
+    return {"ok": not errors, "errors": errors, "writer_schema": schema,
+            "reader_version": READER_VERSION}
+
+
+def expected_episode_id(body_hash: str) -> str:
+    return EPISODE_PREFIX + str(body_hash)
+
+
+def _check_row_columns(table: str, row: dict, parsed: dict,
+                       errors: list[str]) -> None:
+    seq = row["seq"]
+    if table == "episode":
+        expected = expected_episode_id(parsed.get("hash", ""))
+        if row["episode_id"] != expected:
+            errors.append(f"episode:{seq}:episode_id_column_mismatch")
+        if parsed.get("episode_id") != expected:
+            errors.append(f"episode:{seq}:episode_id_body_mismatch")
+        for column, key in (("branch_id", "branch_id"), ("actor_id", "actor_id"),
+                            ("kind", "kind"), ("clock", "clock")):
+            if parsed.get(key) != row[column]:
+                errors.append(f"episode:{seq}:{column}_column_body_mismatch")
+    elif table == "world_event":
+        for column in ("event_id", "clock"):
+            if parsed.get(column) != row[column]:
+                errors.append(f"world_event:{seq}:{column}_column_body_mismatch")
+        if parsed.get("sequence") is not None and parsed["sequence"] != seq:
+            errors.append(f"world_event:{seq}:sequence_body_mismatch")
+    elif table == "checkpoint":
+        if parsed.get("clock") != row["clock"]:
+            errors.append(f"checkpoint:{seq}:clock_column_body_mismatch")
+
+
+def verify_rows(store: C12Store, branch_id: str) -> dict:
+    store.branch(branch_id)
+    errors: list[str] = []
+    counts: dict[str, int] = {}
+    for table, column in (("episode", "body"), ("world_event", "body"),
+                          ("checkpoint", "state")):
+        rows = _row_dicts(store, branch_id, table)
+        counts[table] = len(rows)
+        for row in rows:
+            parsed = json.loads(row[column])
+            body_hash = parsed.get("hash")
+            preimage = {key: value for key, value in parsed.items()
+                        if key != "hash"}
+            if table == "episode":
+                preimage.pop("episode_id", None)
+            if body_hash != _digest(preimage):
+                errors.append(f"{table}:{row['seq']}:body_hash_mismatch")
+            if row["hash"] != body_hash:
+                errors.append(f"{table}:{row['seq']}:column_hash_mismatch")
+            _check_row_columns(table, row, parsed, errors)
+        if [row["seq"] for row in rows] != list(range(len(rows))):
+            errors.append(f"{table}:seq_not_contiguous")
+    perceptions = _row_dicts(store, branch_id, "perception")
+    counts["perception"] = len(perceptions)
+    if [row["seq"] for row in perceptions] != list(range(len(perceptions))):
+        errors.append("perception:seq_not_contiguous")
+    branch = store.branch(branch_id)
+    actors = set(branch["actor_ids"])
+    events = {row["event_id"] for row in _row_dicts(store, branch_id,
+                                                    "world_event")}
+    for row in perceptions:
+        if row["event_id"] not in events:
+            errors.append(f"perception:{row['seq']}:event_not_in_branch")
+        if row["actor_id"] not in actors:
+            errors.append(f"perception:{row['seq']}:actor_not_in_branch")
+    return {"ok": not errors, "errors": errors, "counts": counts,
+            "branch_id": branch_id}
+
+
+def chain_digest(store: C12Store, branch_id: str) -> str:
+    """Full ordered identity digest, including perception clocks and channels."""
+    store.branch(branch_id)
+    rows: list[list[Any]] = []
+    for table in ("episode", "world_event", "perception", "checkpoint"):
+        for row in _row_dicts(store, branch_id, table):
+            rows.append([table] + [row[column] for column in _ROW_COLUMNS[table]])
+    return _digest(rows)
+
+
+def _fork_rows(store: C12Store, branch_id: str, table: str,
+               limit: int | None = None) -> list[tuple]:
+    sql = f"SELECT * FROM {table} WHERE branch_id=? ORDER BY seq"
+    values: tuple = (branch_id,)
+    if limit is not None:
+        sql += " LIMIT ?"
+        values += (int(limit),)
+    return [tuple(row) for row in store.db.execute(sql, values)]
+
+
+def _fork_identity(table: str, row: tuple) -> list:
+    return [row[index] for index in _FORK_IDENTITY[table]]
+
+
+def _fork_payload(parent: dict, fork_clock: int, counts: dict[str, int],
+                  rows: dict[str, list[tuple]]) -> dict:
+    return {
+        "schema": FORK_ROOT_SCHEMA,
+        "parent_branch": parent["branch_id"],
+        "parent_root_hash": parent["root_hash"] or "",
+        "fork_clock": int(fork_clock),
+        "counts": {table: int(counts[table]) for table in FORK_TABLES},
+        "rows": {table: [_fork_identity(table, row) for row in rows[table]]
+                 for table in FORK_TABLES},
+    }
+
+
+def fork_integrity(store: C12Store, branch_id: str) -> dict:
+    """Verify the child prefix, perception clocks, ancestry and root hash."""
+    errors: list[str] = []
+    status = "VERIFIED"
+    seen: set[str] = set()
+    current_id = branch_id
+    while True:
+        if current_id in seen:
+            errors.append(f"fork:{current_id}:ancestry_cycle")
+            status = "INVALID"
+            break
+        seen.add(current_id)
+        current = store._branch(current_id)
+        if current is None:
+            errors.append(f"fork:{current_id}:branch_missing")
+            status = "INVALID"
+            break
+        parent_id = current["parent_branch_id"]
+        if parent_id in (None, ""):
+            if current["root_hash"]:
+                errors.append(f"fork:{current_id}:root_hash_on_root_branch")
+            if current["root_counts"]:
+                errors.append(f"fork:{current_id}:root_counts_on_root_branch")
+            break
+        root_hash = current["root_hash"] or ""
+        if not root_hash.startswith(FORK_ROOT_PREFIX):
+            errors.append(f"fork:{current_id}:legacy_root_unverified")
+            status = "LEGACY_HELD"
+            break
+        parent = store._branch(parent_id)
+        if parent is None:
+            errors.append(f"fork:{current_id}:parent_missing")
+            status = "INVALID"
+            break
+        counts = current["root_counts"]
+        if (not isinstance(counts, dict) or set(counts) != set(FORK_TABLES)
+                or any(type(counts[t]) is not int or counts[t] < 0
+                       for t in FORK_TABLES)):
+            errors.append(f"fork:{current_id}:root_counts_invalid")
+            status = "INVALID"
+            break
+        parent_rows: dict[str, list[tuple]] = {}
+        child_rows: dict[str, list[tuple]] = {}
+        for table in FORK_TABLES:
+            limit = counts[table]
+            parent_rows[table] = _fork_rows(store, parent_id, table, limit)
+            child_rows[table] = _fork_rows(store, current_id, table, limit)
+            if len(parent_rows[table]) != limit:
+                errors.append(f"fork:{current_id}:{table}:parent_prefix_short")
+            if len(child_rows[table]) != limit:
+                errors.append(f"fork:{current_id}:{table}:child_prefix_short")
+            if (len(parent_rows[table]) != limit
+                    or len(child_rows[table]) != limit
+                    or [_fork_identity(table, row) for row in parent_rows[table]]
+                    != [_fork_identity(table, row) for row in child_rows[table]]):
+                errors.append(f"fork:{current_id}:{table}:prefix_mismatch")
+        if errors:
+            status = "INVALID"
+            break
+        clock_values = [
+            _fork_identity(table, row)[_FORK_CLOCK_INDEX[table]]
+            for table in FORK_TABLES for row in parent_rows[table]
+        ]
+        expected_clock = max(clock_values, default=0)
+        if current["fork_clock"] != expected_clock:
+            errors.append(f"fork:{current_id}:fork_clock_mismatch")
+        if current["created_clock"] != current["fork_clock"]:
+            errors.append(f"fork:{current_id}:created_clock_mismatch")
+        expected = FORK_ROOT_PREFIX + _digest(_fork_payload(
+            parent, current["fork_clock"], counts, parent_rows))
+        if root_hash != expected:
+            errors.append(f"fork:{current_id}:root_hash_mismatch")
+        if errors:
+            status = "INVALID"
+            break
+        current_id = parent_id
+    if errors and status == "VERIFIED":
+        status = "INVALID"
+    return {"ok": not errors, "status": status, "errors": errors,
+            "branch_id": branch_id}
+
+
+def verify_store(store: C12Store, branch_id: str) -> dict:
+    """Content + fork verification only; never an authenticity claim."""
+    schema = check_schema(store)
+    rows = verify_rows(store, branch_id)
+    fork = fork_integrity(store, branch_id)
+    errors = list(schema["errors"]) + list(rows["errors"]) + list(fork["errors"])
+    return {
+        "ok": not errors,
+        "content_ok": rows["ok"],
+        "fork_ok": fork["ok"],
+        "schema_ok": schema["ok"],
+        "errors": errors,
+        "counts": rows["counts"],
+        "fork": fork,
+        "branch_id": branch_id,
+        "reader_version": READER_VERSION,
+        "authenticity": {"state": "UNVERIFIED",
+                         "code": "OWNER_ANCHOR_REQUIRED"},
+        "completeness": {"state": "UNVERIFIED",
+                         "code": "OWNER_ANCHOR_REQUIRED"},
+    }
+
+
+def anchor_payload(store: C12Store, branch_id: str) -> dict:
+    """The exact owner-visible object an external anchor must cover."""
+    report = verify_store(store, branch_id)
+    return {
+        "schema": ANCHOR_SCHEMA,
+        "reader_version": READER_VERSION,
+        "branch_id": branch_id,
+        "chain": chain_digest(store, branch_id),
+        "counts": report["counts"],
+        "fork_status": report["fork"]["status"],
+    }
+
+
+def check_anchor(anchor: dict | None, payload: dict,
+                 verify_signature: Callable[[dict], bool] | None,
+                 *, min_sequence: int | None = None) -> dict:
+    """Fail closed unless a real owner trust root verifies the exact anchor.
+
+    This function deliberately cannot create a key, sign, or accept a test
+    fixture as an owner. The caller must supply an out-of-band verifier bound
+    to the original owner/anchor custodian. ``None`` is a HOLD, not a pass.
+    """
+    if anchor is None:
+        return {"ok": False, "state": "HOLD", "code": "OWNER_ANCHOR_REQUIRED",
+                "security_boundary": False}
+    if not isinstance(anchor, dict):
+        return {"ok": False, "state": "HOLD", "code": "ANCHOR_MALFORMED",
+                "security_boundary": False}
+    for key in ("schema", "issuer", "key_id", "signature", "payload",
+                "sequence"):
+        if anchor.get(key) is None or anchor.get(key) == "":
+            return {"ok": False, "state": "HOLD",
+                    "code": "ANCHOR_MALFORMED:" + key,
+                    "security_boundary": False}
+    if type(anchor["sequence"]) is not int or anchor["sequence"] < 0:
+        return {"ok": False, "state": "HOLD",
+                "code": "ANCHOR_MALFORMED:sequence",
+                "security_boundary": False}
+    if anchor["schema"] != ANCHOR_SCHEMA:
+        return {"ok": False, "state": "HOLD",
+                "code": "ANCHOR_SCHEMA_UNSUPPORTED:" + str(anchor["schema"]),
+                "security_boundary": False}
+    if _canonical(anchor["payload"]) != _canonical(payload):
+        return {"ok": False, "state": "HOLD",
+                "code": "ANCHOR_PAYLOAD_MISMATCH",
+                "security_boundary": False}
+    if min_sequence is None:
+        return {"ok": False, "state": "HOLD",
+                "code": "ANCHOR_ROLLBACK_WINDOW_UNPROVEN",
+                "security_boundary": False}
+    if anchor["sequence"] < int(min_sequence):
+        return {"ok": False, "state": "HOLD",
+                "code": "ANCHOR_ROLLBACK",
+                "security_boundary": False}
+    if verify_signature is None:
+        return {"ok": False, "state": "HOLD",
+                "code": "OWNER_TRUST_ROOT_ABSENT",
+                "security_boundary": False}
+    try:
+        valid = verify_signature(anchor)
+    except Exception:  # noqa: BLE001 - verifier failure is a refusal
+        valid = False
+    if valid is not True:
+        return {"ok": False, "state": "HOLD",
+                "code": "ANCHOR_SIGNATURE_INVALID",
+                "security_boundary": False}
+    return {"ok": True, "state": "AUTHENTICATED",
+            "code": "OWNER_ANCHOR_VERIFIED", "issuer": anchor["issuer"],
+            "key_id": anchor["key_id"], "security_boundary": True}
+
+
+
+def check_c9_mirror_handshake(mirror_meta: dict, writer_schema: str) -> dict:
+    """Check the C9 mirror reader's declared C12 source domain.
+
+    The C9 mirror is a separate database. This check does not create a mirror
+    or claim cross-database atomicity; it only refuses a version mismatch before
+    a caller treats a mirror row as a C12 projection.
+    """
+    errors: list[str] = []
+    if mirror_meta.get("schema") != C9_MIRROR_SCHEMA:
+        errors.append("c9_mirror_schema_unsupported:" + str(
+            mirror_meta.get("schema")))
+    if mirror_meta.get("c12_source_domain") != writer_schema:
+        errors.append("c9_mirror_c12_domain_mismatch:" + str(
+            mirror_meta.get("c12_source_domain")))
+    return {"ok": not errors, "errors": errors,
+            "mirror_schema": mirror_meta.get("schema"),
+            "c12_source_domain": mirror_meta.get("c12_source_domain"),
+            "writer_schema": writer_schema}
+
+
+def two_store_readiness(mirror_meta: dict, writer_schema: str, *,
+                        watermark_state: str, outbox_state: str) -> dict:
+    """No cross-DB ACID: only CLEAN + ACKED is a materialized read."""
+    handshake = check_c9_mirror_handshake(mirror_meta, writer_schema)
+    errors = list(handshake["errors"])
+    if watermark_state != "CLEAN":
+        errors.append("c12_watermark_not_clean:" + watermark_state)
+    if outbox_state != "ACKED":
+        errors.append("c9_outbox_not_acked:" + outbox_state)
+    return {"ok": not errors, "state": "READY" if not errors else "SYNC_HELD",
+            "errors": errors, "atomicity": "NO_CROSS_DATABASE_ACID__OUTBOX_AND_WATERMARK"}
+
+
+def classify_episode_ids(store: C12Store, branch_id: str) -> dict:
+    """Report legacy/non-lawful ids without rewriting any row."""
+    rows = _row_dicts(store, branch_id, "episode")
+    legacy = []
+    for row in rows:
+        parsed = json.loads(row["body"])
+        expected = expected_episode_id(parsed.get("hash", ""))
+        if row["episode_id"] != expected or parsed.get("episode_id") != expected:
+            legacy.append({"seq": row["seq"], "episode_id": row["episode_id"],
+                           "body_episode_id": parsed.get("episode_id"),
+                           "expected": expected})
+    return {"ok": not legacy, "legacy_rows": legacy,
+            "migration": "OWNER_ISSUED_MIGRATION_REQUIRED" if legacy else
+            "NOT_REQUIRED",
+            "write_performed": False}
+
+
+class GuardedC12Store(C12Store):
+    """BP4 C12 store with owner-court verification and atomic fork repair."""
+
+    def verify(self, branch_id: str) -> dict:
+        return verify_store(self, branch_id)
+
+    def fork(self, parent_branch_id: str, new_branch_id: str) -> dict:
+        savepoint = "c12_guard_fork"
+        self.db.execute(f"SAVEPOINT {savepoint}")
+        try:
+            parent = self.branch(parent_branch_id)
+            if self._branch(new_branch_id) is not None:
+                raise StoreRefusal("BRANCH_EXISTS")
+            schema = check_schema(self)
+            if not schema["ok"]:
+                raise StoreRefusal("SCHEMA_UNSUPPORTED")
+            parent_fork = fork_integrity(self, parent_branch_id)
+            if not parent_fork["ok"]:
+                raise StoreRefusal("FORK_HELD", "parent_fork_integrity_unverified")
+            latest_perception = self.db.execute(
+                "SELECT coalesce(max(clock),0) FROM perception WHERE branch_id=?",
+                (parent_branch_id,)).fetchone()[0]
+            fork_clock = max(self.last_clock(parent_branch_id),
+                             int(latest_perception))
+            rows = {table: _fork_rows(self, parent_branch_id, table)
+                    for table in FORK_TABLES}
+            counts = {table: len(rows[table]) for table in FORK_TABLES}
+            root_hash = FORK_ROOT_PREFIX + _digest(
+                _fork_payload(parent, fork_clock, counts, rows))
+            self.db.execute(
+                "INSERT INTO branch VALUES (?,?,?,?,?,?,?)",
+                (new_branch_id, parent_branch_id, int(fork_clock), root_hash,
+                 _canonical(counts), int(fork_clock),
+                 _canonical(parent["actor_ids"])))
+            for table in FORK_TABLES:
+                self._copy_fork_rows(table, new_branch_id, rows[table])
+            created = self.branch(new_branch_id)
+            self.db.execute(f"RELEASE {savepoint}")
+        except Exception:
+            try:
+                self.db.execute(f"ROLLBACK TO {savepoint}")
+                self.db.execute(f"RELEASE {savepoint}")
+            except Exception:  # noqa: BLE001 - preserve original fork failure
+                pass
+            raise
+        return created
+
+    def _copy_fork_rows(self, table: str, new_branch_id: str,
+                        rows: list[tuple]) -> None:
+        columns = {"episode": 8, "world_event": 6, "perception": 6,
+                   "checkpoint": 5}[table]
+        placeholders = ",".join("?" for _ in range(columns))
+        for row in rows:
+            values = list(row)
+            values[0] = new_branch_id
+            self.db.execute(
+                f"INSERT INTO {table} VALUES ({placeholders})", tuple(values))
+
+
+__all__ = [
+    "ANCHOR_SCHEMA", "EPISODE_PREFIX", "FORK_ROOT_PREFIX", "FORK_ROOT_SCHEMA",
+    "GuardedC12Store", "READER_VERSION", "WRITER_SCHEMA", "anchor_payload",
+    "C9_MIRROR_SCHEMA", "C9_MIRROR_SOURCE_DOMAIN", "chain_digest",
+    "check_anchor", "check_c9_mirror_handshake", "check_schema",
+    "classify_episode_ids",
+    "expected_episode_id", "fork_integrity", "two_store_readiness",
+    "verify_rows", "verify_store",
+]
diff --git a/tests/test_c12_guard.py b/tests/test_c12_guard.py
new file mode 100644
index 000000000..8ca11491a
--- /dev/null
+++ b/tests/test_c12_guard.py
@@ -0,0 +1,344 @@
+"""Independent sourcefree court for the C12 guard candidate.
+
+Positive: valid SAY rows verify and remain green through cold reopen and fork.
+Negative: tampered rows, legacy ids, unknown schema and forged fork prefixes are
+refused. Residual: deletion/injection/full rehash are content-green but anchored
+out-of-band; no anchor means HOLD, never PASS.
+"""
+from __future__ import annotations
+
+import json
+import sqlite3
+from pathlib import Path
+
+import pytest
+
+from bp2p4.c12_guard import (
+    ANCHOR_SCHEMA, GuardedC12Store, anchor_payload, check_anchor,
+    check_c9_mirror_handshake, check_schema, classify_episode_ids,
+    expected_episode_id, two_store_readiness, verify_store,
+)
+from bp2p4.product import JoinedProduct
+from bp4.canon import canonical, digest
+from bp4.store import C12Store, StoreRefusal
+
+
+def _event(event_id, clock):
+    event = {"event_id": event_id, "clock": clock, "kind": "POSITION"}
+    event["hash"] = digest(event)
+    return event
+
+
+def _seed(path, cls=C12Store):
+    store = cls(path)
+    store.create_root("root", clock=0, actor_ids=["A", "B"], state={"clock": 0})
+    store.append_world_event("root", _event("event10", 10))
+    store.checkpoint("root", 10, {"clock": 10})
+    store.record_perception("root", actor_id="A", event_id="event10",
+                            clock=10, channel="co_present")
+    store.record_perception("root", actor_id="B", event_id="event10",
+                            clock=11, channel="own_action")
+    return store
+
+
+def test_valid_say_is_content_green_but_never_authenticated(intact, tmp_path):
+    product = JoinedProduct(tmp_path / "product", artifacts=intact)
+    try:
+        product.say("a real episode before verification")
+        report = verify_store(product.store, "root")
+        assert report["ok"] is True
+        assert report["content_ok"] is True
+        assert report["schema_ok"] is True
+        assert report["fork_ok"] is True
+        assert report["authenticity"] == {
+            "state": "UNVERIFIED", "code": "OWNER_ANCHOR_REQUIRED"}
+        assert report["completeness"] == {
+            "state": "UNVERIFIED", "code": "OWNER_ANCHOR_REQUIRED"}
+        assert product.store.verify("root")["ok"] is False  # upstream remains RED
+        payload = anchor_payload(product.store, "root")
+        assert check_anchor(None, payload, None)["code"] == "OWNER_ANCHOR_REQUIRED"
+        assert check_anchor({}, payload, None)["code"].startswith(
+            "ANCHOR_MALFORMED")
+        shaped = {"schema": ANCHOR_SCHEMA, "issuer": "ORIGINAL_OWNER",
+                  "key_id": "OWNER_KEY_UNISSUED", "signature": "not-a-signature",
+                  "payload": payload, "sequence": 7}
+        assert check_anchor(shaped, payload, None)["code"] == (
+            "ANCHOR_ROLLBACK_WINDOW_UNPROVEN")
+        assert check_anchor(shaped, payload, None, min_sequence=1)["code"] == (
+            "OWNER_TRUST_ROOT_ABSENT")
+        rolled = dict(shaped, sequence=0)
+        assert check_anchor(rolled, payload, None, min_sequence=1)["code"] == (
+            "ANCHOR_ROLLBACK")
+        assert check_anchor(shaped, payload, lambda _anchor: False,
+                            min_sequence=1)["code"] == (
+            "ANCHOR_SIGNATURE_INVALID")
+    finally:
+        product.close()
+
+
+def test_episode_id_derivation_column_and_legacy_refusal(intact, tmp_path):
+    product = JoinedProduct(tmp_path / "product", artifacts=intact)
+    try:
+        product.say("derive the episode id")
+        row = product.store.db.execute(
+            "SELECT seq, body, hash FROM episode WHERE branch_id='root'"
+        ).fetchone()
+        body = json.loads(row[1])
+        assert body["episode_id"] == expected_episode_id(body["hash"])
+        assert classify_episode_ids(product.store, "root")["ok"] is True
+        product.store.db.execute("DROP TRIGGER episode_no_update")
+        product.store.db.execute(
+            "UPDATE episode SET episode_id=? WHERE branch_id='root' AND seq=?",
+            ("LEGACY_BP4_EP_" + body["hash"], row[0]))
+        report = verify_store(product.store, "root")
+        assert report["ok"] is False
+        assert "episode:0:episode_id_column_mismatch" in report["errors"]
+        legacy = classify_episode_ids(product.store, "root")
+        assert legacy["ok"] is False
+        assert legacy["migration"] == "OWNER_ISSUED_MIGRATION_REQUIRED"
+        assert legacy["write_performed"] is False
+    finally:
+        product.close()
+
+
+def test_raw_deletion_is_content_green_but_anchor_payload_changes(
+        intact, tmp_path):
+    product = JoinedProduct(tmp_path / "product", artifacts=intact)
+    try:
+        product.say("delete me")
+        before = anchor_payload(product.store, "root")
+        db_path = str(product.store.path)
+    finally:
+        product.close()
+    with sqlite3.connect(db_path) as db:
+        db.execute("DROP TRIGGER IF EXISTS episode_no_delete")
+        assert db.execute(
+            "DELETE FROM episode WHERE branch_id='root'").rowcount == 1
+        db.commit()
+    store = GuardedC12Store(db_path)
+    try:
+        report = verify_store(store, "root")
+        assert report["ok"] is True
+        assert report["counts"]["episode"] == 0
+        after = anchor_payload(store, "root")
+        assert after["chain"] != before["chain"]
+        shaped = {"schema": ANCHOR_SCHEMA, "issuer": "ORIGINAL_OWNER",
+                  "key_id": "K", "signature": "sig", "payload": before,
+                  "sequence": 1}
+        assert check_anchor(shaped, after, None, min_sequence=0)["code"] == (
+            "ANCHOR_PAYLOAD_MISMATCH")
+    finally:
+        store.close()
+
+
+def test_injected_world_event_is_content_green_but_anchor_payload_changes(
+        intact, tmp_path):
+    product = JoinedProduct(tmp_path / "product", artifacts=intact)
+    try:
+        product.say("seed")
+        before = anchor_payload(product.store, "root")
+        last_clock = product.store.last_clock("root")
+        last_seq = product.store.db.execute(
+            "SELECT coalesce(max(seq),-1) FROM world_event WHERE branch_id='root'"
+        ).fetchone()[0]
+        event = _event("INJECTED_WORLD_EVENT", last_clock + 1)
+        product.store.db.execute(
+            "INSERT INTO world_event VALUES (?,?,?,?,?,?)",
+            ("root", last_seq + 1, event["event_id"], event["clock"],
+             canonical(event), event["hash"]))
+        report = verify_store(product.store, "root")
+        assert report["ok"] is True
+        after = anchor_payload(product.store, "root")
+        assert after["chain"] != before["chain"]
+    finally:
+        product.close()
+
+
+def test_fully_rehashed_episode_is_content_green_but_anchor_payload_changes(
+        intact, tmp_path):
+    product = JoinedProduct(tmp_path / "product", artifacts=intact)
+    try:
+        product.say("original utterance")
+        before = anchor_payload(product.store, "root")
+        product.store.db.execute("DROP TRIGGER episode_no_update")
+        row = product.store.db.execute(
+            "SELECT seq, body FROM episode WHERE branch_id='root'"
+        ).fetchone()
+        parsed = json.loads(row[1])
+        parsed["body"]["event_id"] = "FORGED_EVENT_ID"
+        parsed.pop("episode_id", None)
+        parsed.pop("hash", None)
+        new_hash = digest(parsed)
+        parsed["hash"] = new_hash
+        parsed["episode_id"] = expected_episode_id(new_hash)
+        product.store.db.execute(
+            "UPDATE episode SET body=?, hash=?, episode_id=? "
+            "WHERE branch_id='root' AND seq=?",
+            (canonical(parsed), new_hash, parsed["episode_id"], row[0]))
+        report = verify_store(product.store, "root")
+        assert report["ok"] is True
+        after = anchor_payload(product.store, "root")
+        assert after["chain"] != before["chain"]
+    finally:
+        product.close()
+
+
+def test_perception_channel_tamper_is_only_visible_to_anchor(
+        intact, tmp_path):
+    product = JoinedProduct(tmp_path / "product", artifacts=intact)
+    try:
+        product.say("perception target")
+        before = anchor_payload(product.store, "root")
+        product.store.db.execute("DROP TRIGGER perception_no_update")
+        product.store.db.execute(
+            "UPDATE perception SET channel='substituted' "
+            "WHERE branch_id='root' AND seq=0")
+        report = verify_store(product.store, "root")
+        assert report["ok"] is True
+        after = anchor_payload(product.store, "root")
+        assert after["chain"] != before["chain"]
+    finally:
+        product.close()
+
+
+def test_unknown_schema_version_fails_closed(intact, tmp_path):
+    product = JoinedProduct(tmp_path / "product", artifacts=intact)
+    try:
+        product.say("schema target")
+        product.store.db.execute(
+            "UPDATE meta SET value='BP4_C12_STORE@2' WHERE key='schema'")
+        assert check_schema(product.store)["ok"] is False
+        report = verify_store(product.store, "root")
+        assert report["ok"] is False
+        assert "schema_version_unsupported:BP4_C12_STORE@2" in report["errors"]
+        db_path = str(product.store.path)
+    finally:
+        product.close()
+    guarded = GuardedC12Store(db_path)
+    try:
+        with pytest.raises(StoreRefusal) as error:
+            guarded.fork("root", "alt")
+        assert error.value.code == "SCHEMA_UNSUPPORTED"
+    finally:
+        guarded.close()
+
+
+def test_fork_keeps_perception_suffix_and_is_atomic(tmp_path, monkeypatch):
+    original = _seed(tmp_path / "original.sqlite")
+    try:
+        original.fork("root", "alt")
+        assert original.perceptions("alt") == [
+            {"actor_id": "A", "event_id": "event10", "clock": 10,
+             "channel": "co_present"}]
+    finally:
+        original.close()
+
+    guarded = _seed(tmp_path / "guarded.sqlite", GuardedC12Store)
+    try:
+        fork = guarded.fork("root", "alt")
+        assert fork["fork_clock"] == 11
+        assert fork["root_hash"].startswith("BP4_C12_FORK_ROOT@2:")
+        assert guarded.perceptions("alt") == [
+            {"actor_id": "A", "event_id": "event10", "clock": 10,
+             "channel": "co_present"},
+            {"actor_id": "B", "event_id": "event10", "clock": 11,
+             "channel": "own_action"}]
+        assert guarded.verify("alt")["ok"] is True
+        assert guarded.verify("alt")["fork"]["status"] == "VERIFIED"
+        calls = []
+
+        def fail(table, new_branch_id, rows):
+            calls.append(table)
+            if table == "perception":
+                raise RuntimeError("INJECTED_COPY_FAILURE")
+            return original_copy(table, new_branch_id, rows)
+
+        original_copy = guarded._copy_fork_rows
+        monkeypatch.setattr(guarded, "_copy_fork_rows", fail)
+        with pytest.raises(RuntimeError):
+            guarded.fork("root", "discarded")
+        assert calls == ["episode", "world_event", "perception"]
+        assert guarded._branch("discarded") is None
+        for table in ("episode", "world_event", "perception", "checkpoint"):
+            assert guarded.db.execute(
+                f"SELECT count(*) FROM {table} WHERE branch_id='discarded'"
+            ).fetchone()[0] == 0
+        assert guarded.verify("root")["ok"] is True
+    finally:
+        guarded.close()
+
+
+def test_legacy_fork_root_and_tampered_prefix_are_held(tmp_path):
+    store = _seed(tmp_path / "legacy.sqlite", GuardedC12Store)
+    try:
+        store.fork("root", "alt")
+        legacy = digest({"parent": "root", "fork_clock": 11, "hashes": []})
+        store.db.execute(
+            "UPDATE branch SET root_hash=? WHERE branch_id='alt'", (legacy,))
+        report = store.verify("alt")
+        assert report["ok"] is False
+        assert report["fork"]["status"] == "LEGACY_HELD"
+        with pytest.raises(StoreRefusal) as error:
+            store.fork("alt", "grand")
+        assert error.value.code == "FORK_HELD"
+    finally:
+        store.close()
+
+    store = _seed(tmp_path / "prefix.sqlite", GuardedC12Store)
+    try:
+        store.fork("root", "alt")
+        store.db.execute("DROP TRIGGER perception_no_update")
+        store.db.execute(
+            "UPDATE perception SET channel='substituted' "
+            "WHERE branch_id='alt' AND seq=0")
+        report = store.verify("alt")
+        assert report["ok"] is False
+        assert any("perception:prefix_mismatch" in error
+                   for error in report["fork"]["errors"])
+    finally:
+        store.close()
+
+
+def test_cold_reopen_preserves_chain_and_fork(tmp_path):
+    path = tmp_path / "cold.sqlite"
+    store = _seed(path, GuardedC12Store)
+    try:
+        before = anchor_payload(store, "root")
+        store.fork("root", "alt")
+        store.append_world_event("alt", _event("event20", 20))
+        store.checkpoint("alt", 20, {"clock": 20})
+    finally:
+        store.close()
+    reopened = GuardedC12Store(path)
+    try:
+        assert reopened.verify("root")["ok"] is True
+        assert reopened.verify("alt")["ok"] is True
+        assert anchor_payload(reopened, "root")["chain"] == before["chain"]
+        assert reopened.branch("alt")["parent_branch_id"] == "root"
+    finally:
+        reopened.close()
+
+
+def test_c9_mirror_domain_handshake_and_two_store_hold(tmp_path):
+    schema = Path(
+        "/private/tmp/bp4c12-c9r3/SOROK_PRODUCT_CONTROL_ROOM/V3_COURTS/"
+        "SYN02/POST_R2_REVIEW/R3/C9_SQL/schema_mirror_r3.sql")
+    if not schema.exists():
+        pytest.skip("C9 mirror schema source unavailable")
+    path = tmp_path / "mirror.sqlite"
+    with sqlite3.connect(path) as conn:
+        conn.executescript(schema.read_text())
+        meta = dict(conn.execute("SELECT key,value FROM mirror_meta").fetchall())
+    assert check_c9_mirror_handshake(meta, "BP4_C12_STORE@1")["ok"] is True
+    mismatch = check_c9_mirror_handshake(meta, "BP4_C12_STORE@2")
+    assert mismatch["ok"] is False
+    held = two_store_readiness(
+        meta, "BP4_C12_STORE@1", watermark_state="SYNC_HELD",
+        outbox_state="PENDING")
+    assert held["state"] == "SYNC_HELD"
+    assert held["atomicity"] == (
+        "NO_CROSS_DATABASE_ACID__OUTBOX_AND_WATERMARK")
+    ready = two_store_readiness(
+        meta, "BP4_C12_STORE@1", watermark_state="CLEAN",
+        outbox_state="ACKED")
+    assert ready["ok"] is True
```

## What the candidate verifies

| Check | Candidate behavior | Actual test evidence |
|---|---|---|
| Episode preimage | Excludes top-level `hash` and post-hash `episode_id`; recomputes `digest(preimage) == body.hash` | valid SAY green; tampered body red; cold reopen green |
| Episode id | Requires `episode.episode_id` column and `body.episode_id` both equal `TEST_ONLY_BP4_EP_ + body.hash` | id-only tamper and legacy prefix red; classifier reports migration required without writing |
| Row columns | Episode `branch_id/actor_id/kind/clock`, world `event_id/clock/sequence`, checkpoint `clock` must match the body | column/body mismatch red |
| Perception references | Every perception event exists in the branch and every perception actor is in the branch | impossible reference red |
| Schema version | Writer must declare exactly `BP4_C12_STORE@1`; non-zero unknown `user_version`/`application_id` fail closed | `BP4_C12_STORE@2` => `schema_version_unsupported`; fork raises `SCHEMA_UNSUPPORTED` |
| Fork | All four tables, perception clocks, `BP4_C12_FORK_ROOT@2`, counts/identities, ancestry, atomic savepoint | perception-only suffix preserved; failed copy rolls back; tampered prefix red; legacy root `LEGACY_HELD`; subsequent fork `FORK_HELD` |
| Chain digest | Full ordered identity digest including perception clock and channel | deletion/injection/rehash/perception substitution change the digest |
| Anchor | Never creates or trusts a key; fails closed until a real owner trust root and monotonic sequence are supplied | `OWNER_ANCHOR_REQUIRED`, `ANCHOR_ROLLBACK_WINDOW_UNPROVEN`, `ANCHOR_ROLLBACK`, `OWNER_TRUST_ROOT_ABSENT`, `ANCHOR_SIGNATURE_INVALID` |
| C9 mirror handshake | `C12_ACTOR_MIRROR_R3@1` must declare `c12_source_domain=BP4_C12_STORE@1` | actual mirror schema compatible; forced @2 mismatch refused |
| Two-store read | `READY` only for `watermark_state=CLEAN` and `outbox_state=ACKED` | all other states `SYNC_HELD`; no cross-DB ACID claimed |

## What the candidate does not verify

It does **not** prove that a row was written by the original actor/owner, that no row was deleted by someone with raw SQLite access, that a self-consistent injected row is false, that a fully rehashed row is forged, or that the chain is complete after the last anchor. Those require the owner-issued external anchor and monotonic counter described in `02_...md`. Until then the candidate returns `authenticity=UNVERIFIED`, `completeness=UNVERIFIED`, `OWNER_ANCHOR_REQUIRED`.

## Exact owner HOLD contract (if the candidate is not adopted)

If the original owner rejects the candidate, the minimum unissuable contract is:

1. **Episode id law:** `TEST_ONLY_BP4_EP_ + digest(body minus hash and episode_id)`; the column and body must both carry it. Any legacy form is refused or migrated only by an owner-issued migration with a new schema version.
2. **Reader version law:** a reader may read only `BP4_C12_STORE@1`; a writer schema change must bump `meta.schema`, declare a new reader version and publish an owner migration. Unknown schema is a refusal, never a best-effort read.
3. **Fork law:** fork clock includes perception; the child prefix covers all four tables; the root binds parent/root/counts/identities; the copy is atomic; legacy roots are `LEGACY_HELD`.
4. **Two-store law:** no cross-database ACID; C9 commit + outbox is the recovery unit; C12 projection is idempotent; `CLEAN` + `ACKED` is the only materialized read.
5. **Anchor law:** original owner or independent custodian signs `SOROK_C12_EXTERNAL_ANCHOR@1` over the exact payload; key is outside the repo/DB; sequence is monotonic outside the DB; an older anchor is refused; coverage is only to the anchored point.
6. **Upstream BP4:** owner either repairs `C12Store.verify` to hash the stored preimage (episode excludes `episode_id`) or retains the self-referential RED as an explicit HOLD. This worker does not edit it.
7. **Receiver:** the first real receiver must be the original C12/C9 owner or a named production consumer; no native C12, C11, CAN/ADP, Pyat or person claim is made here.

## Exact commands used for the candidate

```sh
# prepare base
git worktree add --detach /private/tmp/bp4c12-f2-base \
  5b3e6577400ea1d88971ae6b48e41a118b8059ae
cd /private/tmp/bp4c12-f2-base/WORKER_RETURNS/SOROK-20261020-BP2P4J-ACTUAL-JOINED-ALPHA-R1

# apply Part A (F2 verifier + immutable F2 test) and Part B (guard)
cd /private/tmp/bp4c12-f2-base
git apply /private/tmp/c12_verify_f2.patch
git show 0636d257f588f8874e65b2cb183d1d47c7f53327:WORKER_RETURNS/SOROK-HR1-F2-BP2P4J-EPISODE-VERIFY-REPAIR-R1/candidate/tests/test_episode_verifier_regression.py \
  > WORKER_RETURNS/SOROK-20261020-BP2P4J-ACTUAL-JOINED-ALPHA-R1/tests/test_episode_verifier_regression.py
git apply -p1 --directory=WORKER_RETURNS/SOROK-20261020-BP2P4J-ACTUAL-JOINED-ALPHA-R1 /private/tmp/c12_guard_candidate.patch
cd WORKER_RETURNS/SOROK-20261020-BP2P4J-ACTUAL-JOINED-ALPHA-R1

# candidate tests
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 \
  python3 -m pytest tests/test_c12_guard.py -v
PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 \
  python3 -m pytest tests -v
```

Observed: `11 passed` for the guard; `48 passed, 1 skipped` for the combined suite. The skip is the typed `BP2_ORIGIN_RUNTIME_ABSENT` literal-origin check, not a candidate assertion.

## Blob custody and review

- The F2 candidate and test are immutable blobs in commit `0636d257…`; this return does not alter them.
- The guard and its test are reproduced exactly by the Part B patch and hash rows above; they are not committed as separate files because the return contract permits only the five return artifacts.
- Independent review must replay the exact patch at the exact base, inspect the candidate source, run the positive and negative tests, and then decide adoption. The reviewer must not be this worker, the F2 author or the original BP4/C12 owner.

## FINDING / INTERPRETATION / HQ ACTION / OWNER

**FINDING:** the checkable C12 preimage, derived id, schema, fork and fail-closed anchor boundary can be made executable sourcefree with no key fabrication; the actual anchor cannot.

**INTERPRETATION:** the candidate closes the syntax/version/prefix classes, not the custody class. A sourcefree pass on the former is not authority for the latter.

**HQ ACTION:** route Part A and Part B to the original owners and a distinct reviewer; require a real anchor decision before any authenticity/completeness claim.

**OWNER:** original BP4/C12 and BP2P4J owners, C9-R3 owner, independent anchor custodian, incumbent HQ and a separate source-qualified reviewer.
