"""Private compact respondent-event lane derived from an I02-validated release."""

from __future__ import annotations

from collections.abc import Callable, Iterator, Sequence
from array import array
from bisect import bisect_left,bisect_right
from dataclasses import dataclass
from hashlib import sha256
import json
import os
from pathlib import Path
import stat
import tempfile
from types import MappingProxyType
from typing import Any, ClassVar, TYPE_CHECKING

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef, CanonicalSemanticObject, ExactRef, RespondentEvent, canonical_json, exact_ref,
    semantic_hash,
)

if TYPE_CHECKING:
    from rawlsing_next.pre553_c11_repository import C11LogicalRelease


_CACHE_SCHEMA = "PRE553_I02_EVENT_ACCELERATOR@1"
_CACHE_ENV = "RAWLSING_C11_ACCELERATOR_DIR"
_EVENT_BODY_COLUMN = "canonical_event_body"
_CACHE_METADATA_KEY = b"rawlsing.c11.event_accelerator"


def _ref_identity(ref: ExactRef) -> tuple[str, str, str]:
    return ref.kind, ref.object_id, ref.content_hash


@dataclass(frozen=True, slots=True)
class _EventRead:
    """Selector v1 fields; reference exports are detached from immutable backing."""

    schema_id: ClassVar[str] = "RespondentEvent"
    _ref_identity: tuple[str, str, str]
    typed_state: str
    _native_question_identity: tuple[str, str, str]
    _canonical_question_identity: tuple[str, str, str] | None
    _component_identity: tuple[str, str, str] | None
    _authority_identities: tuple[tuple[str, str, str], ...]
    raw_response_value: Any
    canonical_response_value_if_authorized: Any
    multiplicity_order_rank_fields: Any
    response_event_id_or_deterministic_index: Any

    @property
    def ref(self) -> ExactRef:
        return ExactRef(*self._ref_identity)

    @property
    def native_question_ref(self) -> ExactRef:
        return ExactRef(*self._native_question_identity)

    @property
    def canonical_question_ref_if_authorized(self) -> ExactRef | None:
        return ExactRef(*self._canonical_question_identity) if self._canonical_question_identity else None

    @property
    def component_or_subitem_ref(self) -> ExactRef | None:
        return ExactRef(*self._component_identity) if self._component_identity else None

    @property
    def authority_snapshot_refs(self) -> tuple[AuthorityRef, ...]:
        return tuple(AuthorityRef(*identity) for identity in self._authority_identities)


@dataclass(frozen=True,slots=True)
class _RoutingRead:
    """Selected I03 fields from an already I02-validated exact routing body.

    Like _EventRead, this is a private evaluator view, not a public fact or
    a new authority. Full exact objects remain available via the repository.
    All exported references are detached from immutable primitive backing.
    """
    schema_id: ClassVar[str] = "RoutingEligibilityFact"
    _ref_identity: tuple[str,str,str]
    typed_state: str
    routing_state: str
    applicability_state: str
    _question_identity: tuple[str,str,str]
    _risk_identity: tuple[str,str,str]
    _member_identity: tuple[str,str,str]
    _authority_identities: tuple[tuple[str,str,str],...]

    @property
    def ref(self):
        return ExactRef(*self._ref_identity)

    @property
    def question_or_target_ref(self):
        return ExactRef(*self._question_identity)

    @property
    def risk_set_ref(self):
        return ExactRef(*self._risk_identity)

    @property
    def member_set_replay_ref(self):
        return ExactRef(*self._member_identity)

    @property
    def authority_snapshot_refs(self):
        return tuple(AuthorityRef(*identity) for identity in self._authority_identities)


@dataclass(frozen=True, slots=True)
class _CountryEventHeader:
    """Transient private I02 header, never a public semantic object.

    Full source events are validated before this reduction. The exact ref,
    occurrence/scope checks, selectors and reconstruction dependencies
    survive; the canonical body does not remain resident.
    """
    selector: _EventRead
    empirical_universe_ref: ExactRef
    scoped_respondent_ref: ExactRef
    dependency_refs: tuple[ExactRef, ...]
    event_group_id: str

    @property
    def ref(self):
        return self.selector.ref
    @property
    def content_hash(self):
        return self.selector.ref.content_hash
    @property
    def native_question_ref(self):
        return self.selector.native_question_ref
    @property
    def component_or_subitem_ref(self):
        return self.selector.component_or_subitem_ref
    @property
    def response_event_id_or_deterministic_index(self):
        return self.selector.response_event_id_or_deterministic_index


class _CountryHeaderBuilder:
    """Shared immutable field interning at true repeated information grain."""
    def __init__(self):
        self.dimensions={}
        self.refs={}
        self.values=({}, {}, {})
        self.authorities={}

    def ref(self,value):
        ref=exact_ref(value)
        key=_ref_identity(ref)
        # Detach from the producer's ref instance, then share exact strings.
        return self.refs.setdefault(key,ExactRef(*key))

    def dimension(self,value):
        if value is None:
            return None
        key=_ref_identity(exact_ref(value))
        return self.dimensions.setdefault(key,key)

    def value(self,value,pool):
        if len(pool)>=8192:
            return value
        key=canonical_json(value)
        if len(key)>2048:
            return value
        return pool.setdefault(key,value)

    def add(self,obj):
        auth=tuple((ref.authority_id,ref.authority_version,ref.authority_content_hash)
                   for ref in obj.authority_snapshot_refs)
        if len(self.authorities)<8192:
            auth=self.authorities.setdefault(auth,auth)
        selector=_EventRead(
            _ref_identity(obj.ref),obj.typed_state,self.dimension(obj.native_question_ref),
            self.dimension(obj.canonical_question_ref_if_authorized),
            self.dimension(obj.component_or_subitem_ref),auth,
            self.value(obj.raw_response_value,self.values[0]),
            self.value(obj.canonical_response_value_if_authorized,self.values[1]),
            self.value(obj.multiplicity_order_rank_fields,self.values[2]),
            obj.response_event_id_or_deterministic_index,
        )
        return _CountryEventHeader(selector,self.ref(obj.empirical_universe_ref),
            self.ref(obj.scoped_respondent_ref),tuple(self.ref(ref) for ref in obj.dependency_refs),
            obj.event_group_id)


@dataclass(frozen=True, slots=True)
class _EventLane:
    bodies: Any  # Arrow immutable binary array or chunked array
    selectors: tuple[_EventRead, ...]

    def materialize(self, row: int) -> RespondentEvent:
        from rawlsing_next.pre553_carrier_execution import materialize_public_object

        ref = self.selectors[row].ref
        body = json.loads(self.bodies[row].as_py())
        body.update(object_id=ref.object_id, content_hash=ref.content_hash)
        return materialize_public_object(body)


@dataclass(frozen=True, slots=True)
class _EventLocator:
    lane: _EventLane
    row: int

    @property
    def ref(self) -> ExactRef:
        return self.lane.selectors[self.row].ref

    def materialize(self) -> RespondentEvent:
        return self.lane.materialize(self.row)


@dataclass(frozen=True, slots=True)
class _RespondentEvents(Sequence[RespondentEvent]):
    lane: _EventLane
    rows: tuple[int, ...]
    # Optional compact, immutable postings for wide country respondents.
    # Native, canonical and component identities retain separate semantics.
    question_rows: tuple[Any,Any,Any] | None = None

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return tuple(self.lane.materialize(row) for row in self.rows[index])
        return self.lane.materialize(self.rows[index])

    def select(
        self, target: ExactRef, *, native_only: bool = False,
        include_component: bool = False, states: frozenset[str] | None = None,
    ) -> Iterator[_EventRead]:
        target_identity = _ref_identity(target)
        rows=self.rows
        if self.question_rows is not None:
            selectors=self.lane.selectors
            fields=("_native_question_identity","_canonical_question_identity","_component_identity")
            hits=set()
            for i,(field,posting) in enumerate(zip(fields,self.question_rows)):
                if i>0 and (native_only or (i==2 and not include_component)):
                    continue
                if not len(posting):
                    continue
                def key(row):
                    return getattr(selectors[row],field)
                lo=bisect_left(posting,target_identity,key=key)
                hi=bisect_right(posting,target_identity,key=key)
                hits.update(posting[lo:hi])
            # Original selector index order is the preexisting canonical
            # occurrence traversal; do not reorder/multiply matching events.
            rows=sorted(hits)
        for row in rows:
            event = self.lane.selectors[row]
            matches = event._native_question_identity == target_identity or (
                not native_only and (
                    event._canonical_question_identity == target_identity
                    or (include_component and event._component_identity == target_identity)
                )
            )
            if matches and (states is None or event.typed_state in states):
                yield event


@dataclass(frozen=True,slots=True)
class _InsertedRoutingEntries(Sequence):
    """Insert one contiguous canonical-family lane without per-row objects."""
    base: tuple
    start: int
    routing: Any
    guard: Any = None

    def __len__(self):
        return len(self.base)+len(self.routing)

    def __getitem__(self,i):
        if isinstance(i,slice):
            return tuple(self[j] for j in range(*i.indices(len(self))))
        if i<0:
            i+=len(self)
        if not 0<=i<len(self):
            raise IndexError(i)
        offset=i-self.start
        if offset<0:
            return self.base[i]
        if offset<len(self.routing):
            if self.guard is None:
                return -offset-1
            self.guard.check_live()
            return self.routing[offset]
        return self.base[i-len(self.routing)]


@dataclass(frozen=True, slots=True, eq=False, repr=False)
class _CompactPublicObjects(Sequence[CanonicalSemanticObject]):
    release_ref: ExactRef
    replay_ref: ExactRef
    lane: _EventLane
    entries: Sequence[CanonicalSemanticObject | int]
    non_events: Sequence[CanonicalSemanticObject]
    by_respondent: MappingProxyType
    event_states: frozenset[str]
    routing: Any = None
    nonrouting: tuple | None = None

    def __len__(self) -> int:
        return len(self.entries)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return tuple(self._materialize(entry) for entry in self.entries[index])
        return self._materialize(self.entries[index])

    def __eq__(self, other):
        if not isinstance(other, (tuple, _CompactPublicObjects)):
            return NotImplemented
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))

    def _materialize(self, entry: CanonicalSemanticObject | int) -> CanonicalSemanticObject:
        if isinstance(entry,int) and entry<0 and self.routing is not None:
            self.lane.bodies.check_live()
            return self.routing[-entry-1]
        return self.lane.materialize(entry) if isinstance(entry,int) else entry

    def exact_entries(self) -> Iterator[CanonicalSemanticObject | _EventLocator]:
        for entry in self.entries:
            if isinstance(entry,int) and entry<0 and self.routing is not None:
                yield self._materialize(entry)
            else:
                yield _EventLocator(self.lane,entry) if isinstance(entry,int) else entry


def _country_respondent_events(lane,rows):
    original=tuple(rows)
    if len(original)<32:
        return _RespondentEvents(lane,original)
    selectors=lane.selectors
    tag="I" if len(selectors)<2**32 else "Q"
    postings=[]
    for field in ("_native_question_identity","_canonical_question_identity","_component_identity"):
        selected=sorted((row for row in original if getattr(selectors[row],field) is not None),
                        key=lambda row:getattr(selectors[row],field))
        postings.append(memoryview(array(tag,selected).tobytes()).cast(tag))
    return _RespondentEvents(lane,original,tuple(postings))


def _compact_country_headers(release_ref,replay_ref,non_events,headers,bodies,routing=None):
    """Assemble the existing compact public view directly, with no event bodies."""
    if not headers or len(bodies)!=len(headers):
        raise ValueError("country compact event census mismatch")
    selectors=tuple(header.selector for header in headers)
    lane=_EventLane(bodies,selectors)
    groups={}
    for row,header in enumerate(headers):
        groups.setdefault((header.empirical_universe_ref,header.scoped_respondent_ref.key),[]).append(row)
    entries=tuple(sorted((*non_events,*range(len(headers))),
        key=lambda entry:selectors[entry].ref.key if isinstance(entry,int) else entry.ref.key))
    non_events=tuple(non_events)
    nonrouting=None
    if routing is not None:
        family="RoutingEligibilityFact@1.0.0"
        nonrouting=non_events
        insertion=bisect_left(entries,family,key=lambda e:selectors[e].ref.kind if isinstance(e,int) else e.ref.kind)
        entries=_InsertedRoutingEntries(entries,insertion,routing)
        insertion=bisect_left(nonrouting,family,key=lambda e:e.ref.kind)
        non_events=_InsertedRoutingEntries(nonrouting,insertion,routing,bodies)
    return _CompactPublicObjects(release_ref,replay_ref,lane,entries,non_events,
        MappingProxyType({key:_country_respondent_events(lane,rows) for key,rows in groups.items()}),
        frozenset(selector.typed_state for selector in selectors),routing,nonrouting)


def _cache_directory() -> Path | None:
    """Use only a caller-configured private storage root."""
    configured = os.environ.get(_CACHE_ENV)
    if not configured:
        return None
    directory = Path(configured)
    if not directory.is_absolute():
        return None
    try:
        directory.mkdir(mode=0o700, parents=True, exist_ok=True)
        info = directory.lstat()
        if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
            return None
    except OSError:
        return None
    return directory


def _read_bodies(path: Path, key: str, selectors: tuple[_EventRead, ...]):
    import pyarrow as pa
    import pyarrow.parquet as pq

    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        with os.fdopen(fd, "rb") as handle:
            info = os.fstat(handle.fileno())
            if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
                    or info.st_mode & 0o077):
                return None
            parquet = pq.ParquetFile(handle)
            schema = parquet.schema_arrow
            if (schema.metadata != {_CACHE_METADATA_KEY: key.encode("ascii")}
                    or schema.remove_metadata() != pa.schema([(_EVENT_BODY_COLUMN, pa.binary())])
                    or parquet.metadata.num_rows != len(selectors)):
                return None
            batches = []
            offset = 0
            for batch in parquet.iter_batches(columns=[_EVENT_BODY_COLUMN]):
                column = batch.column(0)
                for scalar in column:
                    if (offset >= len(selectors) or not scalar.is_valid
                            or sha256(scalar.as_buffer()).hexdigest() != selectors[offset].ref.content_hash):
                        return None
                    offset += 1
                batches.append(column)
            if offset == len(selectors):
                return pa.chunked_array(batches, type=pa.binary())
    except (OSError, ValueError, pa.ArrowException):
        return None
    return None


def _write_bodies(path: Path, key: str, bodies) -> None:
    import pyarrow as pa
    import pyarrow.parquet as pq

    staged = None
    try:
        fd, name = tempfile.mkstemp(prefix=".c11-events-", dir=path.parent)
        staged = Path(name)
        table = pa.table({_EVENT_BODY_COLUMN: bodies}).replace_schema_metadata(
            {_CACHE_METADATA_KEY: key.encode("ascii")}
        )
        with os.fdopen(fd, "wb") as handle:
            pq.write_table(table, handle, compression="zstd", compression_level=3)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(staged, path)
    except (OSError, ValueError, pa.ArrowException):
        # Storage is disposable. The live view still comes from the sealed release.
        pass
    finally:
        if staged is not None:
            try:
                staged.unlink(missing_ok=True)
            except OSError:
                pass


def _compact_public_objects(
    release: C11LogicalRelease, *, physical_binding: Callable[[], Any],
    projection_binding: str,
    country_body_factory=None,
) -> _CompactPublicObjects | None:
    """Derive selectors from current I02 objects and authenticate cached bodies to their refs."""
    try:
        import pyarrow as pa
    except ModuleNotFoundError as exc:
        if exc.name != "pyarrow":
            raise
        return None

    entries: list[CanonicalSemanticObject | int] = []
    events: list[RespondentEvent] = []
    non_events = []
    selectors = []
    groups: dict[tuple[ExactRef, str], list[int]] = {}
    dimensions: dict[tuple[str, str, str], tuple[str, str, str]] = {}
    # In country lanes share true-grain repeated immutable metadata rather
    # than retaining the unique event object's copy. Bound intern tables;
    # high-cardinality values fall back to original exact immutable objects.
    value_pools=({}, {}, {})
    authority_pool={}
    def shared(value,pool):
        if country_body_factory is None or len(pool)>=8192:
            return value
        key=canonical_json(value)
        if len(key)>2048:
            return value
        return pool.setdefault(key,value)

    def dimension(event: RespondentEvent, field: str) -> tuple[str, str, str] | None:
        value = getattr(event, field)
        if value is None:
            return None
        identity = _ref_identity(exact_ref(value, field))
        return dimensions.setdefault(identity, identity)

    for obj in release.public_objects:
        if not isinstance(obj, RespondentEvent):
            entries.append(obj)
            non_events.append(obj)
            continue
        row = len(events)
        entries.append(row)
        events.append(obj)
        auth=tuple((ref.authority_id, ref.authority_version, ref.authority_content_hash)
                   for ref in obj.authority_snapshot_refs)
        if country_body_factory is not None and len(authority_pool)<8192:
            auth=authority_pool.setdefault(auth,auth)
        selectors.append(_EventRead(
            _ref_identity(obj.ref), obj.typed_state, dimension(obj, "native_question_ref"),
            dimension(obj, "canonical_question_ref_if_authorized"),
            dimension(obj, "component_or_subitem_ref"), auth,
            shared(obj.raw_response_value,value_pools[0]),
            shared(obj.canonical_response_value_if_authorized,value_pools[1]),
            shared(obj.multiplicity_order_rank_fields,value_pools[2]),
            obj.response_event_id_or_deterministic_index,
        ))
        universe = dimension(obj, "empirical_universe_ref")
        respondent = dimension(obj, "scoped_respondent_ref")
        groups.setdefault((ExactRef(*universe), ExactRef(*respondent).key), []).append(row)

    if not events:
        return None
    selectors = tuple(selectors)
    # The explicitly bound country transport resolves exact bodies from its
    # persistent numeric lanes. Do not write a duplicate canonical-body cache.
    directory = _cache_directory() if country_body_factory is None else None
    bodies = country_body_factory(release, events) if country_body_factory is not None else None
    path = None
    binding = physical_binding() if directory is not None else None
    if binding is not None:
        key = semantic_hash({
            "schema": _CACHE_SCHEMA,
            "source": release.source_artifact_ref.as_dict(),
            "decoder": binding,
            "projection": projection_binding,
            "release": release.release_ref.as_dict(),
            "release_manifest": release.source_release_manifest_hash,
            "replay": release.replay_manifest.ref.as_dict(),
            "member_root": semantic_hash([selector.ref.as_dict() for selector in selectors]),
        })
        # Sixteen direct-mapped slots bound retention while keeping distinct
        # current projections in separate files. A collision is a cache miss.
        path = directory / f"c11-events-{key[0]}.parquet"
        bodies = _read_bodies(path, key, selectors)
    if bodies is None:
        batch_size = 4096
        bodies = pa.chunked_array([
            pa.array(
                (canonical_json(event.semantic_projection()).encode("utf-8")
                 for event in events[start:start + batch_size]),
                type=pa.binary(),
            )
            for start in range(0, len(events), batch_size)
        ], type=pa.binary())
        if path is not None:
            _write_bodies(path, key, bodies)
    lane = _EventLane(bodies, selectors)
    def respondent_events(rows):
        original=tuple(rows)
        if country_body_factory is None or len(original)<32:
            return _RespondentEvents(lane,original)
        # Four bytes/occurrence per populated posting (8 if truly necessary),
        # not a Python dictionary per respondent/variable.
        tag="I" if len(selectors)<2**32 else "Q"
        postings=[]
        for field in ("_native_question_identity","_canonical_question_identity","_component_identity"):
            selected=sorted((row for row in original if getattr(selectors[row],field) is not None),
                            key=lambda row:getattr(selectors[row],field))
            postings.append(memoryview(array(tag,selected).tobytes()).cast(tag))
        return _RespondentEvents(lane,original,tuple(postings))
    return _CompactPublicObjects(
        release.release_ref, release.replay_manifest.ref, lane, tuple(entries), tuple(non_events),
        MappingProxyType({key: respondent_events(rows) for key, rows in groups.items()}),
        frozenset(selector.typed_state for selector in selectors),
    )
