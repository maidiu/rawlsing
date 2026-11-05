"""Private compact respondent-event lane derived from an I02-validated release."""

from __future__ import annotations

from collections.abc import Callable, Iterator, Sequence
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
        for row in self.rows:
            event = self.lane.selectors[row]
            matches = event._native_question_identity == target_identity or (
                not native_only and (
                    event._canonical_question_identity == target_identity
                    or (include_component and event._component_identity == target_identity)
                )
            )
            if matches and (states is None or event.typed_state in states):
                yield event


@dataclass(frozen=True, slots=True, eq=False, repr=False)
class _CompactPublicObjects(Sequence[CanonicalSemanticObject]):
    release_ref: ExactRef
    replay_ref: ExactRef
    lane: _EventLane
    entries: tuple[CanonicalSemanticObject | int, ...]
    non_events: tuple[CanonicalSemanticObject, ...]
    by_respondent: MappingProxyType
    event_states: frozenset[str]

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
        return self.lane.materialize(entry) if isinstance(entry, int) else entry

    def exact_entries(self) -> Iterator[CanonicalSemanticObject | _EventLocator]:
        for entry in self.entries:
            yield _EventLocator(self.lane, entry) if isinstance(entry, int) else entry


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
        selectors.append(_EventRead(
            _ref_identity(obj.ref), obj.typed_state, dimension(obj, "native_question_ref"),
            dimension(obj, "canonical_question_ref_if_authorized"),
            dimension(obj, "component_or_subitem_ref"),
            tuple((ref.authority_id, ref.authority_version, ref.authority_content_hash)
                  for ref in obj.authority_snapshot_refs),
            obj.raw_response_value, obj.canonical_response_value_if_authorized,
            obj.multiplicity_order_rank_fields, obj.response_event_id_or_deterministic_index,
        ))
        universe = dimension(obj, "empirical_universe_ref")
        respondent = dimension(obj, "scoped_respondent_ref")
        groups.setdefault((ExactRef(*universe), ExactRef(*respondent).key), []).append(row)

    if not events:
        return None
    selectors = tuple(selectors)
    directory = _cache_directory()
    bodies = None
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
    return _CompactPublicObjects(
        release.release_ref, release.replay_manifest.ref, lane, tuple(entries), tuple(non_events),
        MappingProxyType({key: _RespondentEvents(lane, tuple(rows)) for key, rows in groups.items()}),
        frozenset(selector.typed_state for selector in selectors),
    )
