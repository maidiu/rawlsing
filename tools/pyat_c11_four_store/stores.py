"""Four *physical* persistent C11 research stores. NO scientific issuer.

A = Parquet plus durable compact SQLite index; B = full TEXT SQLite;
C = full INTEGER SQLite; D = full INTEGER + SHA256 lookup SQLite.

Original canonical body_json and R5 typed lanes are never recomputed or
downcast. All four have independently durable result/audit tables.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sqlite3
import stat
import time
import zlib
from collections import OrderedDict
from typing import Any, Callable, Iterator, Mapping

FAMILIES = (
    "AuthoritySnapshot", "ComparatorReplayBinding",
    "DiscoveryBranchReplayBinding", "EmpiricalCoordinateFact",
    "EmpiricalPredicateReplayBinding", "EmpiricalUniverse",
    "QuestionVariableBinding", "RespondentEvent", "RespondentIdentity",
    "RoutingEligibilityFact", "SourceUniverseRelation",
    "StructuralAdmissionReplayBinding", "WeightMeasureFact",
)
ARMS = ("H", "S1", "S2", "S3")
SCHEMA = "PYAT_P0_FOUR_PERMANENT_STORE_RESEARCH@1"
NONE = ""

class StoreFailure(RuntimeError):
    pass

def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()

def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def size_tree(path: Path) -> int:
    # WAL/SHM files are created, truncated and removed while the sampler
    # walks this tree. They may vanish between rglob() and stat(); that is
    # not an empirical resource failure. Other I/O errors still propagate.
    try:
        info=path.stat()
    except (FileNotFoundError, NotADirectoryError):
        return 0
    if stat.S_ISREG(info.st_mode):
        return info.st_size
    total=0
    for p in path.rglob("*"):
        try:
            info=p.stat()
        except (FileNotFoundError, NotADirectoryError):
            continue
        if stat.S_ISREG(info.st_mode):
            total+=info.st_size
    return total

def _key(value: Any) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, str):
        return value
    if hasattr(value, "key"):
        return value.key
    if isinstance(value, dict) and {"kind", "object_id", "content_hash"} <= set(value):
        return value["kind"] + "|" + value["object_id"] + "|" + value["content_hash"]
    raise StoreFailure("noncanonical reference cannot be indexed")

class Store:
    def __init__(
        self, name: str, path: Path, estate_path: Path,
        *, create: bool, source_identity: Mapping[str, Any] | None = None,
        progress: Callable[..., None] | None = None,
        read_only: bool = False,
    ):
        if name not in ARMS:
            raise StoreFailure("unknown physical arm")
        self.name, self.path, self.estate_path = name, Path(path), Path(estate_path)
        self.progress = progress or (lambda **kwargs: None)
        if read_only and create:
            raise StoreFailure("read-only physical store cannot be created")
        if not read_only:
            self.path.parent.mkdir(parents=True, exist_ok=True)
        if create and self.path.exists():
            raise StoreFailure("refusing to overwrite another physical store")
        if not create and not self.path.is_file():
            raise StoreFailure("persistent store is missing")
        # Missing authority metadata must not create an empty database that
        # then blocks a legitimate later attempt with "refusing overwrite".
        if create and source_identity is None:
            raise StoreFailure("source identity required for construction")
        if read_only:
            # Native-only replay must never alter the expensive committed
            # permanent SQLite (including queries/results or journal mode).
            self.db = sqlite3.connect(
                self.path.resolve().as_uri()+"?mode=ro",
                uri=True, timeout=120,
            )
            self.db.execute("PRAGMA query_only=ON")
        else:
            self.db = sqlite3.connect(str(self.path), timeout=120)
            self.db.execute("PRAGMA journal_mode=WAL")
            self.db.execute("PRAGMA synchronous=FULL")
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.execute("PRAGMA temp_store=FILE")
        self.db.execute("PRAGMA cache_size=-16384")
        self.db.execute("PRAGMA busy_timeout=120000")
        self.db.row_factory = sqlite3.Row
        self._ref_cache = OrderedDict()
        self._exact_cache = OrderedDict()
        self._body_cache = OrderedDict()
        self._pq = {}
        self._insert_count = 0
        if create:
            self._schema()
            self._set_meta("schema", SCHEMA)
            self._set_meta("arm", name)
            self._set_meta("source_identity", canonical(source_identity))
            self._set_meta("state", "BUILDING")
            self.db.commit()
        elif self.get_meta("schema") != SCHEMA or self.get_meta("arm") != name:
            raise StoreFailure("wrong persisted physical schema/arm")
        elif self.get_meta("state") != "COMMITTED":
            raise StoreFailure("uncommitted or interrupted physical store")
        elif source_identity is not None and self.get_meta("source_identity") != canonical(source_identity):
            raise StoreFailure("store belongs to another exact source/release")

    @property
    def text_keys(self) -> bool:
        return self.name == "S1"

    @property
    def fingerprint_keys(self) -> bool:
        return self.name in ("H", "S3")

    @property
    def stores_bodies(self) -> bool:
        return self.name != "H"

    def _schema(self) -> None:
        db = self.db
        db.executescript("""
            CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE queries(
                operation_key TEXT PRIMARY KEY, query_json TEXT NOT NULL,
                created_utc TEXT NOT NULL
            );
            CREATE TABLE results(
                operation_key TEXT PRIMARY KEY REFERENCES queries(operation_key),
                status TEXT NOT NULL, result_sha256 TEXT,
                result_json TEXT, elapsed_ms REAL NOT NULL
            );
            CREATE TABLE receipts(
                seq INTEGER PRIMARY KEY AUTOINCREMENT,
                kind TEXT NOT NULL, body_json TEXT NOT NULL,
                sha256 TEXT NOT NULL
            );
            CREATE TABLE family_counts(
                family TEXT PRIMARY KEY, n INTEGER NOT NULL,
                semantic_digest TEXT NOT NULL
            );
        """)
        key = "TEXT" if self.text_keys else "INTEGER"
        if not self.text_keys:
            if self.fingerprint_keys:
                db.executescript("""
                    CREATE TABLE refs(
                        id INTEGER PRIMARY KEY, ref TEXT NOT NULL,
                        fp BLOB NOT NULL UNIQUE CHECK(length(fp)=32)
                    );
                """)
            else:
                db.executescript("""
                    CREATE TABLE refs(
                        id INTEGER PRIMARY KEY,
                        ref TEXT NOT NULL UNIQUE
                    );
                """)
        # oid references canonical reference table in compact arms.
        body_type = "BLOB" if self.stores_bodies else "INTEGER"
        body_column = "body BLOB NOT NULL" if self.stores_bodies else "gid INTEGER NOT NULL, off INTEGER NOT NULL"
        db.execute(
            "CREATE TABLE objects("
            f"oid {key} PRIMARY KEY,"
            "family TEXT NOT NULL, position INTEGER NOT NULL,"
            f"{body_column},"
            f"UNIQUE(family,position))"
        )
        db.execute(
            f"CREATE TABLE respondents(rid {key} PRIMARY KEY)"
        )
        db.execute(
            f"CREATE TABLE questions(qid {key} PRIMARY KEY)"
        )
        db.execute(
            "CREATE TABLE question_bindings("
            f"oid {key} PRIMARY KEY REFERENCES objects(oid),"
            f"native {key} NOT NULL, canonical {key}, component {key})"
        )
        db.execute(
            "CREATE TABLE events("
            f"oid {key} PRIMARY KEY REFERENCES objects(oid),"
            f"rid {key} NOT NULL, native {key}, canonical {key}, component {key},"
            "state TEXT NOT NULL, raw_typed TEXT,"
            "gid INTEGER NOT NULL, off INTEGER NOT NULL)"
        )
        db.execute(
            "CREATE TABLE members("
            f"oid {key} PRIMARY KEY REFERENCES objects(oid),"
            f"rid {key} NOT NULL, family TEXT NOT NULL)"
        )
        db.execute(
            "CREATE TABLE routing("
            f"oid {key} PRIMARY KEY REFERENCES objects(oid),"
            f"rid {key} NOT NULL, target {key} NOT NULL, risk {key} NOT NULL)"
        )
        db.executescript("""
            CREATE INDEX obj_family_pos ON objects(family,position);
            CREATE INDEX ev_by_person ON events(rid,oid);
            CREATE INDEX ev_by_native ON events(native,rid,oid);
            CREATE INDEX ev_by_canonical ON events(canonical,rid,oid);
            CREATE INDEX ev_by_component ON events(component,rid,oid);
            CREATE INDEX members_by_person ON members(family,rid,oid);
            CREATE INDEX routing_by_person ON routing(rid,target,risk,oid);
            CREATE INDEX routing_by_target ON routing(target,risk,rid,oid);
        """)
        # Full canonical bodies retain all 13 families, including source
        # semantic and replay families.  No new scientific tables are minted.
        db.commit()

    def _set_meta(self, key: str, value: str) -> None:
        self.db.execute(
            "INSERT INTO meta(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, value),
        )

    def get_meta(self, key: str) -> str | None:
        row = self.db.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return None if row is None else row[0]

    def intern(self, ref: Any) -> str | int | None:
        raw = _key(ref)
        if not raw:
            return None
        if self.text_keys:
            return raw
        old = self._ref_cache.get(raw)
        if old is not None:
            self._ref_cache.move_to_end(raw)
            return old
        fp = hashlib.sha256(raw.encode("utf-8")).digest() if self.fingerprint_keys else None
        if fp is not None:
            record = self.db.execute("SELECT id,ref FROM refs WHERE fp=?", (fp,)).fetchone()
        else:
            record = self.db.execute("SELECT id,ref FROM refs WHERE ref=?", (raw,)).fetchone()
        if record is not None:
            if record["ref"] != raw:
                raise StoreFailure("fingerprint collision: refusing ambiguous exact reference")
            idx = record["id"]
        else:
            try:
                if fp is None:
                    cur = self.db.execute("INSERT INTO refs(ref) VALUES(?)", (raw,))
                else:
                    cur = self.db.execute("INSERT INTO refs(ref,fp) VALUES(?,?)", (raw, fp))
                idx = cur.lastrowid
            except sqlite3.IntegrityError as exc:
                raise StoreFailure("conflicting or colliding exact-reference dictionary") from exc
        self._ref_cache[raw] = idx
        if len(self._ref_cache) > 30000:
            self._ref_cache.popitem(last=False)
        self._exact_cache[idx] = raw
        if len(self._exact_cache) > 30000:
            self._exact_cache.popitem(last=False)
        return idx

    def find_id(self, ref: Any) -> str | int | None:
        raw = _key(ref)
        if not raw:
            return None
        if self.text_keys:
            return raw
        if raw in self._ref_cache:
            self._ref_cache.move_to_end(raw)
            return self._ref_cache[raw]
        if self.fingerprint_keys:
            row = self.db.execute(
                "SELECT id,ref FROM refs WHERE fp=?",
                (hashlib.sha256(raw.encode()).digest(),),
            ).fetchone()
        else:
            row = self.db.execute("SELECT id,ref FROM refs WHERE ref=?", (raw,)).fetchone()
        if row is None:
            return None
        if row["ref"] != raw:
            raise StoreFailure("full reference mismatch at SHA256 lookup")
        idx = row["id"]
        self._ref_cache[raw] = idx
        if len(self._ref_cache) > 30000:
            self._ref_cache.popitem(last=False)
        self._exact_cache[idx] = raw
        if len(self._exact_cache) > 30000:
            self._exact_cache.popitem(last=False)
        return idx

    def exact_ref(self, idx: str | int) -> str:
        if self.text_keys:
            return str(idx)
        cached = self._exact_cache.get(idx)
        if cached is not None:
            self._exact_cache.move_to_end(idx)
            return cached
        row = self.db.execute("SELECT ref FROM refs WHERE id=?", (idx,)).fetchone()
        if row is None:
            raise StoreFailure("missing canonical exact-reference dictionary entry")
        ref = row["ref"]
        self._exact_cache[idx] = ref
        if len(self._exact_cache) > 30000:
            self._exact_cache.popitem(last=False)
        return ref

    def add_row(
        self, family: str, position: int, row: Mapping[str, Any],
        gid: int, off: int, *, routing: tuple[str, str] | None = None,
        binding: tuple[str, str | None, str | None] | None = None,
    ) -> None:
        if family not in FAMILIES or row.get("family") != family:
            raise StoreFailure("incorrect canonical family")
        ref = row.get("ref")
        if not isinstance(ref, str) or not ref:
            raise StoreFailure("missing exact record reference")
        oid = self.intern(ref)
        if self.stores_bodies:
            body = row["body_json"]
            if not isinstance(body, str):
                raise StoreFailure("missing complete canonical body")
            payload = zlib.compress(body.encode("utf-8"), level=6)
            self.db.execute(
                "INSERT INTO objects(oid,family,position,body) VALUES(?,?,?,?)",
                (oid, family, position, payload),
            )
        else:
            self.db.execute(
                "INSERT INTO objects(oid,family,position,gid,off) VALUES(?,?,?,?,?)",
                (oid, family, position, gid, off),
            )
        rid = self.intern(row.get("respondent"))
        if family == "RespondentIdentity":
            self.db.execute("INSERT INTO respondents(rid) VALUES(?)", (oid,))
        if family == "QuestionVariableBinding":
            native = binding[0] if binding else row.get("native")
            canonical = binding[1] if binding else row.get("canonical")
            component = binding[2] if binding else row.get("component")
            if native:
                native_id=self.intern(native)
                self.db.execute(
                    "INSERT OR IGNORE INTO questions(qid) VALUES(?)", (native_id,)
                )
                self.db.execute(
                    "INSERT INTO question_bindings(oid,native,canonical,component)"
                    " VALUES(?,?,?,?)",
                    (oid,native_id,self.intern(canonical),self.intern(component))
                )
        if family == "RespondentEvent":
            if rid is None:
                raise StoreFailure("event lacks respondent")
            if row.get("native"):
                self.db.execute(
                    "INSERT OR IGNORE INTO questions(qid) VALUES(?)",
                    (self.intern(row["native"]),),
                )
            self.db.execute(
                "INSERT INTO events(oid,rid,native,canonical,component,state,raw_typed,gid,off)"
                " VALUES(?,?,?,?,?,?,?,?,?)",
                (
                    oid, rid, self.intern(row.get("native")),
                    self.intern(row.get("canonical")),
                    self.intern(row.get("component")),
                    row["typed_state"], row.get("raw_typed"), gid, off,
                ),
            )
        elif family in ("EmpiricalCoordinateFact", "RoutingEligibilityFact", "WeightMeasureFact"):
            if rid is not None:
                self.db.execute(
                    "INSERT INTO members(oid,rid,family) VALUES(?,?,?)",
                    (oid, rid, family),
                )
            if family == "RoutingEligibilityFact" and rid is not None:
                if routing is None:
                    raise StoreFailure("routing requires exact decoded target/risk references")
                self.db.execute(
                    "INSERT INTO routing(oid,rid,target,risk) VALUES(?,?,?,?)",
                    (oid, rid, self.intern(routing[0]), self.intern(routing[1])),
                )
        self._insert_count += 1

    def commit_batch(self) -> None:
        self.db.commit()
        self._ref_cache.clear()
        self._exact_cache.clear()

    def finish(self, manifest: Mapping[str, Any], family_records: Mapping[str, Mapping[str, Any]]) -> None:
        if self.get_meta("state") != "BUILDING":
            raise StoreFailure("physical store can only finish an active build")
        if set(family_records) != set(FAMILIES):
            raise StoreFailure("incomplete thirteen-family C11 census")
        for name, item in family_records.items():
            self.db.execute(
                "INSERT INTO family_counts(family,n,semantic_digest) VALUES(?,?,?)",
                (name, item["count"], item["digest"]),
            )
            n = self.db.execute("SELECT COUNT(*) FROM objects WHERE family=?", (name,)).fetchone()[0]
            if n != item["count"]:
                raise StoreFailure("physical C11 family count differs from verified input: " + name)
        # Every event must resolve to one original respondent and one
        # source-native question; no orphan is a valid observation.
        orphan=self.db.execute(
            "SELECT e.oid FROM events e LEFT JOIN respondents r ON e.rid=r.rid"
            " WHERE r.rid IS NULL LIMIT 1"
        ).fetchone()
        if orphan is not None:
            raise StoreFailure("physical event lost respondent identity")
        unbound=self.db.execute(
            "SELECT e.oid FROM events e LEFT JOIN questions q ON e.native=q.qid"
            " WHERE q.qid IS NULL LIMIT 1"
        ).fetchone()
        if unbound is not None:
            raise StoreFailure("physical event lost source-native question identity")
        self._set_meta("expected_family_records", canonical(family_records))
        self._set_meta("original_manifest", canonical(manifest))
        if self.db.execute("PRAGMA foreign_key_check").fetchone() is not None:
            raise StoreFailure("SQLite foreign key check failed")
        if self.db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise StoreFailure("SQLite b-tree integrity check failed")
        # A completed row count is NOT a complete physical release. An
        # interruption before the full canonical-body audit must never leave
        # a database that a fresh reader accepts as COMMITTED.
        self._set_meta("state", "AUDIT_PENDING")
        self.db.commit()

    def audit_families(self, emit: Callable[..., None] | None = None) -> dict[str, dict[str, Any]]:
        emit = emit or self.progress
        result = {}
        for family in FAMILIES:
            h = hashlib.sha256()
            count = 0
            rows = self.db.execute(
                "SELECT oid FROM objects WHERE family=? ORDER BY position", (family,)
            )
            for rec in rows:
                ref, body = self.fetch_body(rec["oid"])
                serial = ref.encode() + b"\x00" + body.encode()
                h.update(len(serial).to_bytes(8,"big"))
                h.update(serial)
                count += 1
                if count % 30000 == 0:
                    emit(stage="audit", family=family, completed=count)
            result[family] = {"count": count, "digest": h.hexdigest()}
        expected = json.loads(self.get_meta("expected_family_records") or "{}")
        if result != expected:
            raise StoreFailure("full thirteen-family canonical body parity FAILED")
        # The body hash alone does not catch a dropped SQL posting. Catch
        # orphan, missing, or wrong-family event/respondent index entries
        # before making a previously incomplete store readable.
        if self.db.execute("SELECT COUNT(*) FROM events").fetchone()[0] != result["RespondentEvent"]["count"]:
            raise StoreFailure("physical event index lost original event rows")
        if self.db.execute("SELECT COUNT(*) FROM respondents").fetchone()[0] != result["RespondentIdentity"]["count"]:
            raise StoreFailure("physical respondent index lost original respondents")
        if self.db.execute(
            "SELECT 1 FROM events e JOIN objects o ON e.oid=o.oid "
            "WHERE o.family!='RespondentEvent' LIMIT 1"
        ).fetchone() is not None:
            raise StoreFailure("physical event index points to wrong family")
        if self.db.execute(
            "SELECT 1 FROM events e LEFT JOIN respondents r ON e.rid=r.rid "
            "WHERE r.rid IS NULL LIMIT 1"
        ).fetchone() is not None:
            raise StoreFailure("physical event index has orphan respondent")
        if self.db.execute("PRAGMA foreign_key_check").fetchone() is not None:
            raise StoreFailure("physical store has broken SQL foreign keys")
        if self.db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise StoreFailure("physical store SQLite integrity check failed")
        state = self.get_meta("state")
        if state == "AUDIT_PENDING":
            self._set_meta("state", "COMMITTED")
            self.db.commit()
            status = self.db.execute("PRAGMA wal_checkpoint(TRUNCATE)").fetchone()
            if status is not None and status[0] != 0:
                raise StoreFailure("physical store WAL checkpoint could not finish")
        elif state != "COMMITTED":
            raise StoreFailure("full audit requested for an unbuilt store")
        return result

    def _file(self, family: str):
        if self.stores_bodies:
            raise StoreFailure("complete SQLite arm must not read Parquet for bodies")
        if family not in self._pq:
            import pyarrow.parquet as pq
            self._pq[family] = pq.ParquetFile(self.estate_path / (family + ".parquet"))
        return self._pq[family]

    def fetch_body(self, oid: str | int) -> tuple[str, str]:
        rec = self.db.execute("SELECT oid,family,body FROM objects WHERE oid=?", (oid,)).fetchone() if self.stores_bodies else self.db.execute(
            "SELECT oid,family,gid,off FROM objects WHERE oid=?", (oid,)
        ).fetchone()
        if rec is None:
            raise StoreFailure("requested body outside persistent canonical corpus")
        ref = self.exact_ref(rec["oid"])
        if self.stores_bodies:
            try:
                body = zlib.decompress(rec["body"]).decode("utf-8")
            except (ValueError, zlib.error, UnicodeError) as exc:
                raise StoreFailure("compressed canonical body corrupt") from exc
            return ref, body
        fam, gid, off = rec["family"], rec["gid"], rec["off"]
        key = (fam,gid)
        if key not in self._body_cache:
            rows = self._file(fam).read_row_group(gid, columns=["ref","body_json"]).to_pylist()
            self._body_cache[key] = rows
            if len(self._body_cache) > 3:
                self._body_cache.popitem(last=False)
        else:
            self._body_cache.move_to_end(key)
        rows = self._body_cache[key]
        if not (0 <= off < len(rows)) or rows[off]["ref"] != ref:
            raise StoreFailure("Parquet body and permanent selector diverged")
        return ref, rows[off]["body_json"]

    def iter_family(self, family: str) -> Iterator[tuple[str,str]]:
        for row in self.db.execute(
            "SELECT oid FROM objects WHERE family=? ORDER BY position", (family,)
        ):
            yield self.fetch_body(row["oid"])

    def event_keys(self, targets: list[str], limit: int | None = None) -> Iterator[tuple[str, str]]:
        if not targets:
            return
        keys = [self.find_id(ref) for ref in targets]
        keys = [key for key in keys if key is not None]
        if not keys:
            return
        markers = ",".join("?" for _ in keys)
        sql = (
            f"SELECT oid,rid FROM events WHERE native IN ({markers}) ORDER BY rid,oid"
        )
        if limit is not None:
            sql += f" LIMIT {int(limit)}"
        for row in self.db.execute(sql, keys):
            yield self.exact_ref(row["oid"]), self.exact_ref(row["rid"])

    def get_question_refs(self, n: int = 100) -> list[str]:
        # Number of distinct native event targets is a *physical* probe choice,
        # never an automatically issued scientific query or source authorization.
        cursor = self.db.execute(
            "SELECT native,COUNT(*) AS n FROM events "
            "WHERE native IS NOT NULL GROUP BY native"
        )
        # Release-local INTEGER ids differ from textual lexicographic order.
        # Tie-breaking MUST be by the complete external exact reference.
        return [ref for _,ref in sorted(
            ((-row["n"],self.exact_ref(row["native"])) for row in cursor)
        )[:n]]

    def select_events(
        self, *, respondent: str, target: str,
        native_only: bool = False, include_component: bool = False,
        states: frozenset[str] | None = None,
    ) -> Iterator[tuple[str, str]]:
        rid = self.find_id(respondent)
        tid = self.find_id(target)
        if rid is None or tid is None or (states is not None and not states):
            return
        columns = ("native",) if native_only else (
            ("native", "canonical", "component") if include_component
            else ("native", "canonical")
        )
        parts = []
        args = []
        for column in columns:
            parts.append(
                f"SELECT oid FROM events WHERE rid=? AND {column}=?"
                + (" AND state IN (" + ",".join("?" for _ in states) + ")"
                   if states is not None else "")
            )
            args.extend([rid, tid])
            if states is not None:
                args.extend(sorted(states))
        sql = " UNION ".join(parts)
        # SQL integer ordering is not semantic ref-key ordering. Caller
        # restores exact reference ordering before native evaluation.
        keys = [r["oid"] for r in self.db.execute(sql, args)]
        for oid in sorted(keys, key=self.exact_ref):
            yield self.fetch_body(oid)

    def side_family(self, *, family: str, respondent: str) -> Iterator[tuple[str,str]]:
        rid = self.find_id(respondent)
        if rid is None:
            return
        rows = self.db.execute(
            "SELECT oid FROM members WHERE family=? AND rid=?", (family,rid)
        )
        keys = [row["oid"] for row in rows]
        for oid in sorted(keys, key=self.exact_ref):
            yield self.fetch_body(oid)

    def routing_facts(self, *, respondent: str, target: str, risk_set: str) -> Iterator[tuple[str,str]]:
        rid, tid, risk = (self.find_id(x) for x in (respondent,target,risk_set))
        if rid is None or tid is None or risk is None:
            return
        rows = self.db.execute(
            "SELECT oid FROM routing WHERE rid=? AND target=? AND risk=?",
            (rid,tid,risk),
        )
        for oid in sorted((row["oid"] for row in rows), key=self.exact_ref):
            yield self.fetch_body(oid)

    def probe_query(self, target: str) -> dict[str, Any]:
        idx = self.find_id(target)
        if idx is None:
            raise StoreFailure("unindexed physical target")
        t = time.perf_counter()
        buckets = list(self.db.execute(
            "SELECT state,raw_typed,COUNT(*) AS n FROM events "
            "WHERE native=? GROUP BY state,raw_typed ORDER BY state,raw_typed",
            (idx,),
        ))
        n = sum(row["n"] for row in buckets)
        return {
            "target_ref": target, "events": n,
            "respondents": self.db.execute(
                "SELECT COUNT(DISTINCT rid) FROM events WHERE native=?", (idx,)
            ).fetchone()[0],
            "groups": len(buckets),
            "digest": digest(canonical([list(row) for row in buckets]).encode()),
            "elapsed_ms": round((time.perf_counter()-t)*1000,3),
            "grade": "PHYSICAL_OBSERVATION_NOT_AN_ISSUED_I03_FACT",
        }

    def joint_probe(self, refs: list[str]) -> dict[str, Any]:
        if len(refs) < 3:
            return {"state": "INSUFFICIENT_THREE_QUESTION_TARGETS"}
        ids = [self.find_id(s) for s in refs[:3]]
        if any(s is None for s in ids):
            return {"state": "TARGET_NOT_INDEXED"}
        # Use EXISTS to avoid multiplying respondents with repeated answers.
        q = """
            SELECT COUNT(DISTINCT a.rid)
            FROM events a WHERE a.native=?
              AND EXISTS(SELECT 1 FROM events b WHERE b.rid=a.rid AND b.native=?)
              AND EXISTS(SELECT 1 FROM events c WHERE c.rid=a.rid AND c.native=?)
        """
        t = time.perf_counter()
        val = self.db.execute(q,ids).fetchone()[0]
        return {
            "state": "PHYSICAL_CO_PRESENCE_ONLY_NOT_A_NATIVE_F4",
            "co_present_respondents": val,
            "elapsed_ms": round((time.perf_counter()-t)*1000,3)
        }

    def store_result(
        self, operation: str, query_record: Mapping[str,Any],
        status: str, result: Mapping[str,Any] | None, elapsed_ms: float,
    ) -> None:
        if not operation:
            raise StoreFailure("operation key required")
        body = canonical(result) if result is not None else None
        self.db.execute(
            "INSERT INTO queries(operation_key,query_json,created_utc) VALUES(?,?,datetime('now'))",
            (operation,canonical(query_record)),
        )
        self.db.execute(
            "INSERT INTO results(operation_key,status,result_sha256,result_json,elapsed_ms)"
            " VALUES(?,?,?,?,?)",
            (operation,status,digest(body.encode()) if body is not None else None,body,elapsed_ms),
        )
        self.db.commit()

    def stats(self) -> dict[str, Any]:
        self.db.execute("PRAGMA wal_checkpoint(PASSIVE)")
        pages = self.db.execute("PRAGMA page_count").fetchone()[0]
        page_size = self.db.execute("PRAGMA page_size").fetchone()[0]
        return {
            "arm": self.name, "db_bytes": self.path.stat().st_size,
            "journal_bytes": sum(Path(str(self.path)+s).stat().st_size
                                 for s in ("-wal","-shm") if Path(str(self.path)+s).exists()),
            "page_count": pages, "page_size": page_size,
            "freelist_count": self.db.execute("PRAGMA freelist_count").fetchone()[0],
            "objects": self.db.execute("SELECT COUNT(*) FROM objects").fetchone()[0],
            "events": self.db.execute("SELECT COUNT(*) FROM events").fetchone()[0],
            "distinct_respondents": self.db.execute(
                "SELECT COUNT(*) FROM respondents").fetchone()[0],
            "distinct_questions": self.db.execute(
                "SELECT COUNT(*) FROM questions").fetchone()[0],
            "question_binding_records": self.db.execute(
                "SELECT COUNT(*) FROM question_bindings").fetchone()[0],
            "routing_facts": self.db.execute(
                "SELECT COUNT(*) FROM routing").fetchone()[0],
            "coordinate_weight_routing_member_records": self.db.execute(
                "SELECT COUNT(*) FROM members").fetchone()[0],
            "dictionary_refs": (
                self.db.execute("SELECT COUNT(*) FROM refs").fetchone()[0]
                if not self.text_keys else 0),
        }

    def close(self) -> None:
        for handle in self._pq.values():
            handle.close()
        self._pq.clear()
        self._body_cache.clear()
        self.db.close()
