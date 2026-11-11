"""Private compact respondent-event lane derived from an I02-validated release."""

from __future__ import annotations

from bisect import bisect_right
from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass
from hashlib import sha256
import json
import os
from pathlib import Path
import stat
import tempfile
from types import MappingProxyType
from typing import Any, ClassVar, Mapping, TYPE_CHECKING

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef, CanonicalSemanticObject, ExactRef, RespondentEvent, canonical_json, exact_ref,
    semantic_hash,
)
from rawlsing_next._pre553_w04_cache import (
    CACHE_ENVELOPE_KEY as _CACHE_ENVELOPE_KEY,
    CACHE_METADATA_KEY as _CACHE_METADATA_KEY,
    CACHE_SCHEMA as _CACHE_SCHEMA,
    LEGACY_ENV as _CACHE_ENV,
    AcceleratorPolicy,
    atomic_replace,
    cache_file,
    enforce_after_write,
    load_policy,
)

if TYPE_CHECKING:
    from rawlsing_next.pre553_c11_repository import C11LogicalRelease


_CACHE_POLICY_ENV = "RAWLSING_C11_ACCELERATOR_POLICY"
_EVENT_BODY_COLUMN = "canonical_event_body"
_EVENT_BODY_CHUNK_EVENTS = 256
_EVENT_BODY_CODEC = "zstd"


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
class _CompressedBodies:
    """Bounded compressed canonical event bodies with on-demand exact lookup."""

    chunks: tuple[tuple[bytes, int, int, int], ...]
    starts: tuple[int, ...]
    total_rows: int

    def body_bytes(self, row: int) -> bytes:
        if not isinstance(row, int) or isinstance(row, bool) or row < 0 or row >= self.total_rows:
            raise IndexError("event body row outside compressed lane")
        chunk_index = bisect_right(self.starts, row) - 1
        compressed, raw_size, start, count = self.chunks[chunk_index]
        if row < start or row >= start + count:
            raise IndexError("event body row outside bounded compressed chunk")
        import pyarrow as pa

        raw = pa.decompress(
            compressed, decompressed_size=raw_size, codec=_EVENT_BODY_CODEC,
            asbytes=True,
        )
        position = 0
        for _ in range(row - start):
            length = int.from_bytes(raw[position:position + 4], "big")
            position += 4 + length
        length = int.from_bytes(raw[position:position + 4], "big")
        return raw[position + 4:position + 4 + length]


@dataclass(frozen=True, slots=True)
class _EventLane:
    bodies: Any  # bounded compressed bodies or legacy Arrow binary array
    selectors: tuple[_EventRead, ...]

    def materialize(self, row: int) -> RespondentEvent:
        from rawlsing_next.pre553_carrier_execution import materialize_public_object

        ref = self.selectors[row].ref
        if isinstance(self.bodies, _CompressedBodies):
            body_bytes = self.bodies.body_bytes(row)
        else:
            body_bytes = self.bodies[row].as_py()
        body = json.loads(body_bytes)
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


def _cache_policy() -> AcceleratorPolicy | None:
    """Return an operative governed host policy, or ``None`` without writes.

    A configured policy is authoritative: malformed, unauthorized, absent-root
    or otherwise unsafe policy does not fall back to a raw directory environment
    variable.  The pytest-only legacy temp-root fallback lives in the policy
    helper and is never a deployment grant.
    """
    return load_policy()


def _cache_directory() -> Path | None:
    policy = _cache_policy()
    return policy.root if policy is not None else None


def _compress_body_chunk(bodies: Sequence[bytes]) -> tuple[bytes, int]:
    import pyarrow as pa

    payload = b"".join(len(body).to_bytes(4, "big") + body for body in bodies)
    return pa.compress(payload, codec=_EVENT_BODY_CODEC, asbytes=True), len(payload)


def _read_bodies(
    path: Path,
    key: str,
    selectors: tuple[_EventRead, ...],
    *,
    policy: AcceleratorPolicy | None = None,
    envelope: Mapping[str, Any] | None = None,
):
    import pyarrow as pa
    import pyarrow.parquet as pq

    if policy is not None:
        if path.parent != policy.root or not path.name.startswith("c11-events-"):
            return None
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        with os.fdopen(fd, "rb") as handle:
            info = os.fstat(handle.fileno())
            if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
                    or info.st_mode & 0o077):
                return None
            parquet = pq.ParquetFile(handle)
            schema = parquet.schema_arrow
            metadata = dict(schema.metadata or {})
            expected_metadata = {_CACHE_METADATA_KEY: key.encode("ascii")}
            if policy is not None or envelope is not None:
                if _CACHE_ENVELOPE_KEY not in metadata or metadata.get(_CACHE_METADATA_KEY) != expected_metadata[_CACHE_METADATA_KEY]:
                    return None
                try:
                    observed = json.loads(metadata[_CACHE_ENVELOPE_KEY].decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError):
                    return None
                if not isinstance(observed, Mapping):
                    return None
                if policy is not None and observed.get("policy_root") != policy.trusted_root_id:
                    return None
                if envelope is not None and observed != envelope:
                    return None
            else:
                # Legacy direct reader compatibility.  The production compact
                # path always supplies a governed policy and envelope.
                if set(metadata) - {_CACHE_METADATA_KEY, _CACHE_ENVELOPE_KEY}:
                    return None
                if metadata.get(_CACHE_METADATA_KEY) != expected_metadata[_CACHE_METADATA_KEY]:
                    return None
            if (schema.remove_metadata() != pa.schema([(_EVENT_BODY_COLUMN, pa.binary())])
                    or parquet.metadata.num_rows != len(selectors)):
                return None
            chunks = []
            starts = []
            offset = 0
            for batch in parquet.iter_batches(
                batch_size=_EVENT_BODY_CHUNK_EVENTS, columns=[_EVENT_BODY_COLUMN],
            ):
                column = batch.column(0)
                bodies = []
                for scalar in column:
                    if (offset >= len(selectors) or not scalar.is_valid
                            or sha256(scalar.as_buffer()).hexdigest() != selectors[offset].ref.content_hash):
                        return None
                    bodies.append(bytes(scalar.as_buffer()))
                    offset += 1
                if bodies:
                    compressed, raw_size = _compress_body_chunk(bodies)
                    starts.append(offset - len(bodies))
                    chunks.append((compressed, raw_size, offset - len(bodies), len(bodies)))
            if offset == len(selectors):
                return _CompressedBodies(tuple(chunks), tuple(starts), len(selectors))
    except (OSError, ValueError, pa.ArrowException):
        return None
    return None

class _BodyCacheWriter:
    """Bounded streaming writer for the existing raw-body Parquet/Zstd cache format."""

    def __init__(self, path: Path, key: str, *, envelope: Mapping[str, Any] | None = None):
        import pyarrow as pa
        import pyarrow.parquet as pq

        metadata = {_CACHE_METADATA_KEY: key.encode("ascii")}
        if envelope is not None:
            metadata[_CACHE_ENVELOPE_KEY] = canonical_json(envelope).encode("utf-8")
        self._schema = pa.schema([(_EVENT_BODY_COLUMN, pa.binary())]).with_metadata(metadata)
        fd, name = tempfile.mkstemp(prefix=".c11-events-", dir=path.parent)
        self._staged = Path(name)
        self._handle = os.fdopen(fd, "wb")
        self._writer = pq.ParquetWriter(
            self._handle, self._schema, compression="zstd", compression_level=3,
        )
        self._committed = False

    def write_batch(self, bodies: Sequence[bytes]) -> None:
        if not bodies:
            return
        import pyarrow as pa

        table = pa.table({
            _EVENT_BODY_COLUMN: pa.array(bodies, type=pa.binary()),
        }, schema=self._schema)
        self._writer.write_table(table, row_group_size=len(bodies))

    def commit(self, path: Path) -> None:
        self._writer.close()
        self._handle.flush()
        os.fsync(self._handle.fileno())
        self._handle.close()
        try:
            atomic_replace(self._staged, path)
        except OSError:
            # If replace happened but directory fsync failed, the destination is
            # not durably admitted as a cache hit.  Remove it (safe miss) while
            # leaving any pre-existing destination untouched when replace itself
            # did not happen.
            if not self._staged.exists():
                try:
                    path.unlink(missing_ok=True)
                except OSError:
                    pass
            raise
        self._committed = True

    def abort(self) -> None:
        if self._committed:
            return
        try:
            self._writer.close()
        except OSError:
            pass
        try:
            self._handle.close()
        except OSError:
            pass
        try:
            self._staged.unlink(missing_ok=True)
        except OSError:
            pass



def _write_bodies(path: Path, key: str, bodies, *, envelope: Mapping[str, Any] | None = None) -> None:
    import pyarrow as pa

    writer = None
    try:
        writer = _BodyCacheWriter(path, key, envelope=envelope)
        batch = []
        for body in bodies:
            batch.append(body)
            if len(batch) >= _EVENT_BODY_CHUNK_EVENTS:
                writer.write_batch(batch)
                batch.clear()
        if batch:
            writer.write_batch(batch)
        writer.commit(path)
    except (OSError, ValueError, pa.ArrowException):
        if writer is not None:
            writer.abort()
    finally:
        if writer is not None:
            writer.abort()

def _release_authority_root(release: C11LogicalRelease) -> str:
    refs = set()
    for obj in release.public_objects:
        refs.update(getattr(obj, "authority_snapshot_refs", ()))
    return semantic_hash([ref.as_dict() for ref in sorted(refs, key=lambda ref: ref.key)])


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
    policy = _cache_policy()
    bodies = None
    path = None
    key = None
    envelope = None
    binding = physical_binding() if policy is not None else None
    if binding is not None:
        authority_root = _release_authority_root(release)
        member_root = semantic_hash([selector.ref.as_dict() for selector in selectors])
        key = semantic_hash({
            "schema": _CACHE_SCHEMA,
            "source": release.source_artifact_ref.as_dict(),
            "decoder": binding,
            "projection": projection_binding,
            "authority_root": authority_root,
            "policy_root": policy.trusted_root_id,
            "release": release.release_ref.as_dict(),
            "release_manifest": release.source_release_manifest_hash,
            "replay": release.replay_manifest.ref.as_dict(),
            "member_root": member_root,
        })
        envelope = {
            "schema": _CACHE_SCHEMA,
            "key": key,
            "policy_root": policy.trusted_root_id,
            "authority_root": authority_root,
            "source": release.source_artifact_ref.as_dict(),
            "projection": projection_binding,
            "release": release.release_ref.as_dict(),
            "release_manifest": release.source_release_manifest_hash,
            "replay": release.replay_manifest.ref.as_dict(),
            "member_root": member_root,
        }
        path = cache_file(policy, key)
        bodies = _read_bodies(path, key, selectors, policy=policy, envelope=envelope)
    if bodies is None:
        chunks = []
        starts = []
        writer = None
        committed = False
        if path is not None and policy is not None and key is not None and envelope is not None:
            try:
                writer = _BodyCacheWriter(path, key, envelope=envelope)
            except (OSError, ValueError, pa.ArrowException):
                writer = None
        try:
            for start in range(0, len(events), _EVENT_BODY_CHUNK_EVENTS):
                chunk_events = events[start:start + _EVENT_BODY_CHUNK_EVENTS]
                raw_bodies = [
                    canonical_json(event.semantic_projection()).encode("utf-8")
                    for event in chunk_events
                ]
                compressed, raw_size = _compress_body_chunk(raw_bodies)
                starts.append(start)
                chunks.append((compressed, raw_size, start, len(raw_bodies)))
                if writer is not None:
                    try:
                        writer.write_batch(raw_bodies)
                    except (OSError, ValueError, pa.ArrowException):
                        writer.abort()
                        writer = None
            if writer is not None:
                try:
                    writer.commit(path)
                    committed = True
                except (OSError, ValueError, pa.ArrowException):
                    writer.abort()
                    writer = None
        finally:
            if writer is not None:
                writer.abort()
        if committed and policy is not None and path is not None:
            enforce_after_write(policy, path)
        bodies = _CompressedBodies(tuple(chunks), tuple(starts), len(events))
    lane = _EventLane(bodies, selectors)
    return _CompactPublicObjects(
        release.release_ref, release.replay_manifest.ref, lane, tuple(entries), tuple(non_events),
        MappingProxyType({key: _RespondentEvents(lane, tuple(rows)) for key, rows in groups.items()}),
        frozenset(selector.typed_state for selector in selectors),
    )
