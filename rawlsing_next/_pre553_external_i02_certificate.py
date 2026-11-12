"""S2-B bounded, externally anchored I02 *sourcefree* corpus/index certificate.

Produces a disk-sorted, byte-verified *derived* certificate from an existing
genuinely I02-sealed release. It never creates an I02 validation seal or issues
P01-P20/T01-T18 source equivalence/current rights. Historical v1 I02 remains
the input oracle until source-direct S1-B/S2-C physical input is qualified.

The full corpus and *complete* native/canonical/component selector posting
multimap participate in one deterministic logical root. A distinct physical
SHA256 identifies the SQLite bytes. Neither is trusted when read back from the
file itself: the caller MUST supply BOTH roots from an independent authority.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from collections.abc import Sequence
from hashlib import sha256
from heapq import merge
from pathlib import Path
from types import MappingProxyType
from typing import Iterator, Mapping
import os
import re
import sqlite3
import tempfile

from rawlsing_next.pre553_c11_repository import (
    C11LogicalRelease, C11Repository, _C11_VALIDATION_SEAL,
)
from rawlsing_next.pre553_c11_integrity import (
    M01_M18, RespondentIdentity, QuestionVariableBinding, C11IntegrityError,
    C11InternalRecord, TypedAbsence,
)
from rawlsing_next.pre553_empirical_objects import (
    CanonicalSemanticObject, ExactRef, RespondentEvent, canonical_json,
    exact_ref, semantic_hash,
)
from rawlsing_next._pre553_verified_semantic_range import (
    SemanticRangeIntegrityError,
)

SCHEMA = "PYAT_S2B_EXTERNAL_I02_LOGICAL_SELECTOR_CERT@1"
HEX = re.compile(r"[0-9a-f]{64}\Z")


class ExternalI02IntegrityError(C11IntegrityError):
    """Untrusted corpus, index, source binding, physical bytes or root."""


def _fail(message: str) -> None:
    raise ExternalI02IntegrityError(message)


def _digest_file(path: Path) -> str:
    h = sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _ref_fields(ref: ExactRef) -> tuple[str, str, str, str]:
    if type(ref) is not ExactRef:
        _fail("non-exact source ref")
    return ref.key, ref.kind, ref.object_id, ref.content_hash


def _schema(db: sqlite3.Connection) -> None:
    db.executescript("""
        CREATE TABLE header(name TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE TABLE objects(
          ref TEXT PRIMARY KEY, family TEXT NOT NULL,
          ref_kind TEXT NOT NULL, object_id TEXT NOT NULL, digest TEXT NOT NULL,
          universe TEXT NOT NULL, respondent TEXT NOT NULL,
          native TEXT NOT NULL, canonical TEXT NOT NULL, component TEXT NOT NULL,
          state TEXT NOT NULL
        );
        CREATE TABLE closure(ref TEXT PRIMARY KEY);
        CREATE TABLE bindings(
          universe TEXT NOT NULL, native TEXT NOT NULL,
          version TEXT NOT NULL, canonical TEXT NOT NULL, component TEXT NOT NULL,
          PRIMARY KEY(universe,native,version,canonical,component)
        );
        CREATE TABLE selectors(
          respondent TEXT NOT NULL, kind TEXT NOT NULL, target TEXT NOT NULL,
          event_ref TEXT NOT NULL,
          PRIMARY KEY(respondent,kind,target,event_ref)
        );
        CREATE INDEX obj_family_scope ON objects(family,universe,respondent,ref);
        CREATE INDEX selector_key ON selectors(respondent,kind,target,event_ref);
    """)


def _insert_object(db: sqlite3.Connection, obj: object, *, family: str) -> None:
    if not isinstance(obj, (CanonicalSemanticObject, C11InternalRecord)):
        _fail("unsupported I02 corpus member")
    ref, kind, object_id, digest = _ref_fields(obj.ref)
    if semantic_hash(obj.semantic_projection()) != digest:
        _fail("object content changed beneath original I02 ExactRef")
    def value(name: str) -> str:
        raw = getattr(obj, name, None)
        if raw is None or isinstance(raw, TypedAbsence):
            return ""
        # Public canonical objects expose their source refs as serialized
        # mappings in semantic_fields, while I02 internal records often
        # expose real ExactRef instances. Both are legally exact references.
        # Never silently call a mapping an absent respondent/alias.
        return exact_ref(raw, name).key
    db.execute("INSERT INTO objects VALUES(?,?,?,?,?,?,?,?,?,?,?)", (
        ref, family, kind, object_id, digest,
        value("empirical_universe_ref"), value("scoped_respondent_ref"),
        value("native_question_ref"),
        value("canonical_question_ref_if_authorized"),
        value("component_or_subitem_ref"),
        str(getattr(obj, "typed_state", "")),
    ))
    if isinstance(obj, QuestionVariableBinding):
        canonical = obj.canonical_question_ref_or_typed_absence
        component = obj.component_subitem_ref_or_typed_absence
        db.execute("INSERT INTO bindings VALUES(?,?,?,?,?)", (
            obj.empirical_universe_ref.key, obj.native_question_ref.key,
            obj.instrument_question_version,
            canonical.key if isinstance(canonical, ExactRef) else "",
            component.key if isinstance(component, ExactRef) else "",
        ))
    if isinstance(obj, RespondentIdentity):
        # The respondent's canonical key is its I02 internal record ref.
        db.execute(
            "UPDATE objects SET respondent=? WHERE ref=?",
            (ref, ref),
        )


def _check_relations(db: sqlite3.Connection, *, source: str) -> None:
    # Closure identity is the old genuinely validated I02's independent
    # ReplayManifest enumeration, NOT the builder's self-invented row count.
    extras = [x[0] for x in db.execute("""
        SELECT c.ref FROM main.closure c LEFT JOIN main.objects o ON c.ref=o.ref
        WHERE o.ref IS NULL ORDER BY c.ref
    """)]
    absent = db.execute("""
        SELECT o.ref FROM main.objects o LEFT JOIN main.closure c ON o.ref=c.ref
        WHERE c.ref IS NULL LIMIT 1
    """).fetchone()
    if absent or len(extras) != 2 or source not in extras:
        _fail("M01-M18 closure disagrees with witnessed whole I02 corpus")
    # Two exceptional v1 closure refs are the source artifact and the
    # source-snapshot retention ref, neither a public/internal C11 object.
    if db.execute("""
        SELECT 1 FROM main.objects e LEFT JOIN main.objects r
          ON r.ref=e.respondent AND r.family='RespondentIdentity'
          AND r.universe=e.universe
        WHERE e.family='RespondentEvent' AND r.ref IS NULL LIMIT 1
    """).fetchone():
        _fail("event has missing/wrong-universe respondent identity")
    if db.execute("""
        SELECT 1 FROM main.objects e LEFT JOIN main.bindings q
          ON q.universe=e.universe AND q.native=e.native
        WHERE e.family='RespondentEvent' AND q.native IS NULL LIMIT 1
    """).fetchone():
        _fail("event has no universe-qualified original question binding")
    # Original S2-A conjunction: matching alias row must exist in *every*
    # instrument version, not the Cartesian product of separately observed
    # canonical/component aliases or a union across different versions.
    events = db.execute("""
        SELECT ref,universe,native,canonical,component FROM main.objects
        WHERE family='RespondentEvent' ORDER BY ref
    """)
    for ref, universe, native, canonical, component in events:
        versions = db.execute("""
            SELECT DISTINCT version FROM main.bindings
            WHERE universe=? AND native=? ORDER BY version
        """, (universe, native))
        for (version,) in versions:
            if (canonical or component) and not db.execute("""
                SELECT 1 FROM main.bindings WHERE universe=? AND native=?
                  AND version=? AND (?='' OR canonical=?)
                  AND (?='' OR component=?) LIMIT 1
            """, (universe, native, version,
                  canonical, canonical, component, component)).fetchone():
                _fail("forged or cross-version canonical/component alias")
        for kind, target in (
            ("native", native), ("canonical", canonical),
            ("component", component),
        ):
            if target:
                db.execute("INSERT INTO selectors VALUES(?,?,?,?)",
                           (db.execute("SELECT respondent FROM main.objects WHERE ref=?",
                                       (ref,)).fetchone()[0], kind, target, ref))
    if db.execute("""
        SELECT 1 FROM main.selectors s LEFT JOIN main.objects o ON s.event_ref=o.ref
        WHERE o.family!='RespondentEvent' OR o.ref IS NULL LIMIT 1
    """).fetchone():
        _fail("selector posting points outside full I02 event corpus")


def _logical_root(db: sqlite3.Connection) -> str:
    """Canonical streaming commitment, independent of insertion and run sizes."""
    h = sha256()
    def absorb(fields: object) -> None:
        material = canonical_json(fields).encode("utf-8")
        h.update(len(material).to_bytes(8, "big"))
        h.update(material)
    absorb(SCHEMA)
    for name, query in (
        ("header", "SELECT name,value FROM header ORDER BY name"),
        ("objects", "SELECT * FROM main.objects ORDER BY ref"),
        ("closure", "SELECT ref FROM main.closure ORDER BY ref"),
        ("bindings", "SELECT * FROM main.bindings ORDER BY universe,native,version,canonical,component"),
        ("selectors", "SELECT * FROM main.selectors ORDER BY respondent,kind,target,event_ref"),
    ):
        absorb(name)
        for row in db.execute(query):
            absorb(list(row))
    return h.hexdigest()


@dataclass(frozen=True)
class ExternalI02Roots:
    logical: str
    physical: str
    release: str
    source: str
    replay: str
    universe: str

    def __post_init__(self) -> None:
        if not HEX.fullmatch(self.logical) or not HEX.fullmatch(self.physical):
            _fail("complete independent sha256 logical and physical roots required")


def build_sourcefree_external_i02(
    release: C11LogicalRelease, universe_ref: ExactRef, destination: str | Path,
    *, chunk_size: int = 512,
) -> ExternalI02Roots:
    """Build whole-corpus+selector certificate, with SQLite as a disk sorter.

    Input still depends on historical I02 in-memory validation; it is not a
    source-direct bounded I02 replacement. No inventory_refs()->tuple,
    all-ref list or selector postings list is constructed by THIS builder.
    """
    if (not isinstance(release, C11LogicalRelease)
            or release._validation_seal is not _C11_VALIDATION_SEAL):
        _fail("no genuine existing I02-sealed input")
    if set(release.m01_m18_coverage) != set(M01_M18) or any(
        not release.m01_m18_coverage[k] for k in M01_M18
    ):
        _fail("original M01-M18 coverage incomplete")
    if not isinstance(universe_ref, ExactRef):
        _fail("exact source universe required")
    if not 1 <= chunk_size <= 16384:
        raise ValueError("chunk_size must be 1..16384")
    target = Path(destination).absolute()
    if target.is_symlink() or target.exists() or target.suffix != ".sqlite":
        _fail("destination must be a new unlinked .sqlite artifact")
    if not target.parent.is_dir() or target.parent.is_symlink():
        _fail("trusted existing output directory required")
    fd, staged = tempfile.mkstemp(prefix=".s2b-stage-", suffix=".tmp", dir=target.parent)
    os.close(fd)
    db = None
    try:
        db = sqlite3.connect(staged)
        db.execute("PRAGMA journal_mode=DELETE")
        db.execute("PRAGMA synchronous=FULL")
        db.execute("PRAGMA temp_store=FILE")
        db.execute("PRAGMA cache_size=-2048")
        _schema(db)
        headers = {
            "schema": SCHEMA, "release": release.release_ref.key,
            "source": release.source_artifact_ref.key,
            "replay": release.replay_manifest.ref.key,
            "universe": universe_ref.key,
            "coverage": canonical_json({k: list(release.m01_m18_coverage[k])
                                        for k in M01_M18}),
            "chunk_size_is_nonsemantic": "true",
        }
        for k, v in headers.items():
            db.execute("INSERT INTO header VALUES(?,?)", (k, v))
        count = 0
        for obj in release.public_objects:
            _insert_object(db, obj, family=type(obj).__name__)
            count += 1
            if count % chunk_size == 0:
                db.commit()
        for obj in release.internal_records:
            _insert_object(db, obj, family=type(obj).__name__)
            count += 1
            if count % chunk_size == 0:
                db.commit()
        for ref in release.replay_manifest.closure_refs:
            db.execute("INSERT INTO closure VALUES(?)", (ref.key,))
            count += 1
            if count % chunk_size == 0:
                db.commit()
        _check_relations(db, source=release.source_artifact_ref.key)
        if not db.execute(
            "SELECT 1 FROM main.objects WHERE family='EmpiricalUniverse' AND ref=?",
            (universe_ref.key,),
        ).fetchone():
            _fail("selected universe absent from the complete I02 source")
        db.commit()
        root = _logical_root(db)
        if db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            _fail("external I02 SQLite structure inconsistent")
        db.close()
        db = None
        with open(staged, "rb") as f:
            os.fsync(f.fileno())
        # No seal or manifest publication before all global checks succeed.
        # A second writer can claim the final name after the exists() probe.
        # os.replace() silently destroys that writer's output; publishing a
        # certificate is a one-time CAS claim, not last-writer-wins. Link the
        # fully fsynced same-directory inode under an exclusively NEW name.
        # On a collision fail closed and discard only OUR staged artifact.
        # A crash between link and unlink can leave a duplicate stage orphan,
        # never an incomplete published artifact or a silently lost rival.
        try:
            os.link(staged, target, follow_symlinks=False)
        except FileExistsError as exc:
            raise ExternalI02IntegrityError(
                "destination collision: another writer claimed certificate name"
            ) from exc
        except OSError as exc:
            raise ExternalI02IntegrityError(
                "atomic no-clobber certificate publication unavailable"
            ) from exc
        os.unlink(staged)
        dirfd = os.open(target.parent, os.O_RDONLY)
        try:
            os.fsync(dirfd)
        finally:
            os.close(dirfd)
        return ExternalI02Roots(root, _digest_file(target),
                               release.release_ref.key, release.source_artifact_ref.key,
                               release.replay_manifest.ref.key, universe_ref.key)
    finally:
        if db is not None:
            db.close()
        if os.path.exists(staged):
            os.unlink(staged)


class _VerifiedSqlRows:
    """Iteration/fetch-only view; never release the backing SQLite cursor.

    sqlite3.Cursor.connection is a mutable escape hatch. A public certificate
    cannot return raw cursors even if its execute method rejects writes.
    """
    __slots__ = ("__cursor",)

    def __setattr__(self, name: str, value: object) -> None:
        raise ExternalI02IntegrityError(
            "immutable verified external I02 cursor cannot be reassigned"
        )

    def __init__(self, cursor: sqlite3.Cursor) -> None:
        object.__setattr__(self, "_VerifiedSqlRows__cursor", cursor)

    def fetchone(self) -> tuple | None:
        try:
            return self.__cursor.fetchone()
        except sqlite3.Error as exc:
            raise ExternalI02IntegrityError(
                "verified external I02 read cursor closed or invalidated"
            ) from exc

    def fetchall(self) -> list[tuple]:
        try:
            return self.__cursor.fetchall()
        except sqlite3.Error as exc:
            raise ExternalI02IntegrityError(
                "verified external I02 read cursor closed or invalidated"
            ) from exc

    def __iter__(self):
        return self

    def __next__(self) -> tuple:
        result = self.fetchone()
        if result is None:
            raise StopIteration
        return result


class _VerifiedSelectOnlyDatabase:
    """Certified-query facade: no PRAGMA, collation, TEMP table or raw cursor.

    Changing SQLite session state can falsify WHERE equality even for
    main-qualified rows. The raw connection is encapsulated after cold
    verification, and the only public operation is a SELECT-only cursor.
    Arbitrary co-resident private Python introspection is not a security
    domain; this protects the actual native I03 certificate API boundary.
    """
    __slots__ = ("__connection",)

    def __setattr__(self, name: str, value: object) -> None:
        raise ExternalI02IntegrityError(
            "immutable verified external I02 SQL session cannot be reassigned"
        )

    def __init__(self, connection: sqlite3.Connection) -> None:
        object.__setattr__(self, "_VerifiedSelectOnlyDatabase__connection", connection)

    def execute(self, statement: str, params: tuple = ()) -> _VerifiedSqlRows:
        if (not isinstance(statement, str)
                or not statement.lstrip().upper().startswith("SELECT ")
                or ";" in statement):
            raise ExternalI02IntegrityError(
                "verified external I02 database only permits SELECT queries"
            )
        try:
            return _VerifiedSqlRows(self.__connection.execute(statement, params))
        except sqlite3.Error as exc:
            raise ExternalI02IntegrityError(
                "verified external I02 SQL session closed or invalidated"
            ) from exc

    def close(self) -> None:
        self.__connection.close()


class VerifiedExternalI02:
    """Fresh independent cold verifier; never trusts self-declared roots.

    Exact class and slots are part of the native I03 trust boundary: neither a
    lookalike Protocol nor an overrideable child/instance selector is certified.
    """
    __slots__ = ("path", "db", "roots", "_closed", "_sealed")

    def __setattr__(self, name: str, value: object) -> None:
        # Certificate bytes and externally verified identity must not be
        # replaced between cold validation and ordinary native I03 selection.
        # The only permitted post-seal transition is close(), handled below.
        if getattr(self, "_sealed", False):
            _fail("immutable verified external I02 certificate cannot be reassigned")
        object.__setattr__(self, name, value)

    def __init__(self, path: str | Path, *, roots: ExternalI02Roots) -> None:
        if not isinstance(roots, ExternalI02Roots):
            _fail("externally supplied roots required")
        self._closed = True
        self.path = Path(path).absolute()
        if (self.path.is_symlink() or not self.path.is_file()
                or self.path.suffix != ".sqlite"
                or self.path.name.startswith(".s2b-stage-")):
            _fail("orphan, symlink, missing or non-final certificate")
        if _digest_file(self.path) != roots.physical:
            _fail("cold physical bytes differ from held external root")
        self.db = sqlite3.connect(self.path.as_uri() + "?mode=ro", uri=True)
        self.db.execute("PRAGMA query_only=ON")
        self.db.execute("BEGIN")
        try:
            if self.db.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                _fail("cold certificate physical integrity error")
            h = dict(self.db.execute("SELECT name,value FROM header"))
            if h.get("schema") != SCHEMA or any(
                h.get(name) != getattr(roots, name)
                for name in ("release", "source", "replay", "universe")
            ):
                _fail("external I02 identity, replay or universe mismatched")
            if set(__import__("json").loads(h["coverage"])) != set(M01_M18):
                _fail("M01-M18 missing in certified header")
            # Revalidate semantic closure and keyspace before allowing EMPTY.
            _check_relations_readonly(self.db, roots.source)
            if _logical_root(self.db) != roots.logical:
                _fail("logical corpus/selector map differs from external root")
        except Exception:
            self.db.close()
            raise
        # Seal not only attribute assignment but the SQL session's semantics.
        # The previous raw .db leaked PRAGMA query_only, TEMP table shadowing,
        # create_collation('BINARY', ...), and raw Cursor.connection; any could
        # alter normal native I03 facts after both held roots were checked.
        self.db = _VerifiedSelectOnlyDatabase(self.db)
        self.roots = roots
        self._closed = False
        self._sealed = True

    def _ensure_open(self) -> None:
        if self._closed:
            _fail("closed external I02 certificate cannot authorize native selection")

    def _rows(self, statement: str, params: tuple = ()) -> Iterator[tuple]:
        """Never serve a row from a dead verified snapshot.

        Live selection reads explicitly qualified main tables; SQLite TEMP
        shadow tables must not replace I02-verified corpus or postings.
        A cursor may be invalidated between two streamed rows, including
        when close() is called during a native query.
        """
        self._ensure_open()
        try:
            cursor = self.db.execute(statement, params)
            while True:
                self._ensure_open()
                row = cursor.fetchone()
                if row is None:
                    return
                self._ensure_open()
                yield row
        except sqlite3.Error as exc:
            raise ExternalI02IntegrityError(
                "verified external I02 SQLite cursor closed or invalidated"
            ) from exc

    def _first(self, statement: str, params: tuple = ()) -> tuple | None:
        self._ensure_open()
        try:
            return self.db.execute(statement, params).fetchone()
        except sqlite3.Error as exc:
            raise ExternalI02IntegrityError(
                "verified external I02 SQLite cursor closed or invalidated"
            ) from exc

    def close(self) -> None:
        object.__setattr__(self, "_closed", True)
        self.db.close()

    def __enter__(self) -> "VerifiedExternalI02":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def respondent_refs(self) -> Iterator[str]:
        for (ref,) in self._rows("""
            SELECT ref FROM main.objects WHERE family='RespondentIdentity'
              AND universe=? ORDER BY ref
        """, (self.roots.universe,)):
            yield ref

    def event_refs(self, respondent: str) -> Iterator[ExactRef]:
        for row in self._rows("""
            SELECT o.ref_kind,o.object_id,o.digest FROM main.objects o
            WHERE o.family='RespondentEvent'
              AND o.universe=? AND o.respondent=? ORDER BY o.ref
        """, (self.roots.universe, respondent)):
            yield ExactRef(*row)

    def selector_refs(self, respondent: str, target: ExactRef, *,
                      native_only: bool = False, include_component: bool = False,
                      states: frozenset[str] | None = None) -> Iterator[ExactRef]:
        self._ensure_open()
        kinds = ["native"]
        if not native_only:
            kinds.append("canonical")
            if include_component:
                kinds.append("component")
        def part(kind: str):
            sql = """
                SELECT o.ref,o.ref_kind,o.object_id,o.digest,o.state
                FROM main.selectors s JOIN main.objects o ON o.ref=s.event_ref
                WHERE s.respondent=? AND s.kind=? AND s.target=?
                ORDER BY o.ref
            """
            yield from self._rows(sql, (respondent, kind, target.key))
        last = None
        for key, kind, object_id, digest, state in merge(
            *(part(kind) for kind in kinds), key=lambda row: row[0]
        ):
            if key == last:
                continue
            last = key
            self._ensure_open()
            if states is None or state in states:
                yield ExactRef(kind, object_id, digest)


def _check_relations_readonly(db: sqlite3.Connection, source: str) -> None:
    # This read-only check uses no self-generated selection postings. A forged
    # posting can be rehashed locally but cannot reproduce held logical root.
    extras = [x[0] for x in db.execute("""
        SELECT c.ref FROM main.closure c LEFT JOIN main.objects o ON c.ref=o.ref
        WHERE o.ref IS NULL ORDER BY c.ref
    """)]
    if len(extras) != 2 or source not in extras or db.execute("""
        SELECT 1 FROM main.objects o LEFT JOIN main.closure c ON o.ref=c.ref
        WHERE c.ref IS NULL LIMIT 1
    """).fetchone():
        _fail("cold source closure mismatch")
    if db.execute("""
        SELECT 1 FROM main.selectors s LEFT JOIN main.objects o ON s.event_ref=o.ref
        WHERE o.ref IS NULL OR o.family!='RespondentEvent' LIMIT 1
    """).fetchone():
        _fail("orphan selector posting")
    # Full complement, including otherwise unselected states and aliases.
    for ref, respondent, native, canonical, component in db.execute("""
        SELECT ref,respondent,native,canonical,component FROM main.objects
        WHERE family='RespondentEvent' ORDER BY ref
    """):
        for kind, target in (("native", native), ("canonical", canonical),
                             ("component", component)):
            if target and not db.execute("""
                SELECT 1 FROM main.selectors WHERE respondent=? AND kind=?
                AND target=? AND event_ref=?
            """, (respondent, kind, target, ref)).fetchone():
                _fail("cold index omits real I02 semantic selector posting")
    if db.execute("""
        SELECT 1 FROM main.selectors s JOIN main.objects o ON s.event_ref=o.ref
        WHERE s.respondent!=o.respondent OR
          (s.kind='native' AND s.target!=o.native) OR
          (s.kind='canonical' AND s.target!=o.canonical) OR
          (s.kind='component' AND s.target!=o.component) OR
          s.kind NOT IN ('native','canonical','component') LIMIT 1
    """).fetchone():
        _fail("counterfeit/extra/mismatched selector index")


class _DiskSelectedRespondent(Sequence[RespondentEvent]):
    """Honest native I03 sequence, never a forged S2-A in-memory witness.

    Its elements come from independently verified disk selectors, not an
    intentionally empty `CertifiedRespondentEvents.all_events` payload.
    This concrete owned type is allowlisted in the native selector dispatcher.
    """
    __slots__ = ("respondent_key", "_certificate", "_repository")

    def __init__(self, respondent: str, reader: VerifiedExternalI02,
                 repository: C11Repository):
        self.respondent_key = respondent
        self._certificate = reader
        self._repository = repository

    def _load(self, ref: ExactRef) -> RespondentEvent:
        self._certificate._ensure_open()
        obj = self._repository.resolve_object_exact(ref)
        if not isinstance(obj, RespondentEvent) or obj.ref != ref:
            raise SemanticRangeIntegrityError("certified disk event is not exact native I02")
        if semantic_hash(obj.semantic_projection()) != ref.content_hash:
            raise SemanticRangeIntegrityError("native event body changed since certification")
        return obj

    def select(self, target: ExactRef, *, native_only: bool = False,
               include_component: bool = False,
               states: frozenset[str] | None = None) -> Iterator[RespondentEvent]:
        for ref in self._certificate.selector_refs(
            self.respondent_key, target, native_only=native_only,
            include_component=include_component, states=states,
        ):
            yield self._load(ref)

    def __len__(self) -> int:
        self._certificate._ensure_open()
        return self._certificate._first("""
            SELECT COUNT(*) FROM main.objects WHERE family='RespondentEvent'
              AND universe=? AND respondent=?
        """, (self._certificate.roots.universe, self.respondent_key))[0]

    def __iter__(self) -> Iterator[RespondentEvent]:
        for ref in self._certificate.event_refs(self.respondent_key):
            yield self._load(ref)

    def __getitem__(self, index: int) -> RespondentEvent:
        self._certificate._ensure_open()
        if not isinstance(index, int):
            raise TypeError("bounded certified reader supports integer indexing only")
        if index < 0:
            index += len(self)
        if index < 0:
            raise IndexError(index)
        row = self._certificate._first("""
            SELECT ref_kind,object_id,digest FROM main.objects
            WHERE family='RespondentEvent' AND universe=? AND respondent=?
            ORDER BY ref LIMIT 1 OFFSET ?
        """, (self._certificate.roots.universe,self.respondent_key,index))
        if row is None:
            raise IndexError(index)
        return self._load(ExactRef(*row))


def install_sourcefree_external_i02_i03(
    repository: C11Repository, release_ref: ExactRef, universe_ref: ExactRef,
    certificate: VerifiedExternalI02,
) -> None:
    """Native I03 *sourcefree* execution under externally held whole root.

    Existing sealed release and other I03 scientific structures are still
    materialized by the legacy owner. No cold physical C11 carrier or S2-C
    rights are issued. Caller must retain the verified reader for query life.
    """
    if type(repository) is not C11Repository:
        _fail("requires exact original I02 repository")
    if type(certificate) is not VerifiedExternalI02:
        _fail("exact cold-verified external I02 certificate required")
    certificate._ensure_open()
    release = repository.resolve_release_exact(release_ref)
    roots = certificate.roots
    if (roots.release != release.release_ref.key
            or roots.source != release.source_artifact_ref.key
            or roots.replay != release.replay_manifest.ref.key
            or roots.universe != universe_ref.key):
        _fail("wrong sealed I02 source/release/authority binding")
    from rawlsing_next._pre553_query_predicate import _build_release_index
    from rawlsing_next.pre553_empirical_query import _i03_index_attestation
    native = _build_release_index(release, universe_ref)
    if set(certificate.respondent_refs()) != set(native.respondents):
        _fail("cold respondent identity set differs from native I02")
    selector = MappingProxyType({
        key: _DiskSelectedRespondent(key, certificate, repository)
        for key in native.respondents
    })
    index = replace(native, events_by_respondent=selector)
    key = (release_ref, universe_ref)
    with repository._i03_index_lock:
        if repository.resolve_release_exact(release_ref) is not release:
            _fail("source moved during actual native I03 index installation")
        repository._i03_release_indices[key] = index
        repository._i03_index_attestations[key] = _i03_index_attestation(index)
