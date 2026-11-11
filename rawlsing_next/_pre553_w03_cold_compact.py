"""Cold streaming compact lane for W03/W04.

This helper is a physical-memory optimisation, not a semantic engine.  It builds
the existing private compact event lane from an already-validated event stream
and never creates a second C11 store, selector language or query engine.
"""
from __future__ import annotations

from dataclasses import replace
from types import MappingProxyType
from typing import Any, Mapping

from rawlsing_next._pre553_c11_execution_view import (
    _BodyCacheWriter,
    _CompressedBodies,
    _CompactPublicObjects,
    _EVENT_BODY_CHUNK_EVENTS,
    _EVENT_BODY_CODEC,
    _EventLane,
    _EventRead,
    _RespondentEvents,
    _cache_identity,
    _cache_policy,
    _compress_body_chunk,
    _read_bodies,
    _ref_identity,
    enforce_after_write,
)
from rawlsing_next.pre553_empirical_objects import (
    CanonicalSemanticObject,
    ExactRef,
    RespondentEvent,
    canonical_json,
    exact_ref,
)


class ColdCompactBuilder:
    """Build ``_CompactPublicObjects`` in one streaming pass.

    Only selectors, compressed event bodies and non-event objects are retained.
    Full ``RespondentEvent`` objects are dropped immediately after their exact
    body and selector are extracted.
    """

    def __init__(self) -> None:
        self.entries: list[CanonicalSemanticObject | int] = []
        self.event_keys: list[str] = []
        self.non_events: list[CanonicalSemanticObject] = []
        self.selectors: list[_EventRead] = []
        self.groups: dict[tuple[ExactRef, str], list[int]] = {}
        self.dimensions: dict[tuple[str, str, str], tuple[str, str, str]] = {}
        self.event_states: set[str] = set()
        self.chunks: list[tuple[bytes, int, int, int]] = []
        self.starts: list[int] = []
        self._batch: list[bytes] = []
        self.event_count = 0

    def add_non_event(self, obj: CanonicalSemanticObject) -> None:
        self.entries.append(obj)
        self.non_events.append(obj)

    def _dimension(self, event: RespondentEvent, field: str):
        value = getattr(event, field)
        if value is None:
            return None
        identity = _ref_identity(exact_ref(value, field))
        return self.dimensions.setdefault(identity, identity)

    def add_event(
        self,
        event: RespondentEvent,
        projection: Mapping[str, Any] | None = None,
        *,
        body: bytes | None = None,
    ) -> None:
        row = self.event_count
        self.entries.append(row)
        self.event_keys.append(event.ref.key)
        self.selectors.append(_EventRead(
            _ref_identity(event.ref),
            event.typed_state,
            self._dimension(event, "native_question_ref"),
            self._dimension(event, "canonical_question_ref_if_authorized"),
            self._dimension(event, "component_or_subitem_ref"),
            tuple(
                (ref.authority_id, ref.authority_version, ref.authority_content_hash)
                for ref in event.authority_snapshot_refs
            ),
            event.raw_response_value,
            event.canonical_response_value_if_authorized,
            event.multiplicity_order_rank_fields,
            event.response_event_id_or_deterministic_index,
        ))
        universe = self._dimension(event, "empirical_universe_ref")
        respondent = self._dimension(event, "scoped_respondent_ref")
        self.groups.setdefault(
            (ExactRef(*universe), ExactRef(*respondent).key), []
        ).append(row)
        self.event_states.add(event.typed_state)
        if body is None:
            material = projection if projection is not None else event.semantic_projection()
            body = canonical_json(material).encode("utf-8")
        self._batch.append(body)
        self.event_count += 1
        if len(self._batch) >= _EVENT_BODY_CHUNK_EVENTS:
            self._flush()

    def _flush(self) -> None:
        if not self._batch:
            return
        compressed, raw_size = _compress_body_chunk(self._batch)
        start = self.event_count - len(self._batch)
        self.starts.append(start)
        self.chunks.append((compressed, raw_size, start, len(self._batch)))
        self._batch.clear()

    def finish(
        self,
        release_ref: ExactRef,
        replay_ref: ExactRef,
    ) -> _CompactPublicObjects:
        self._flush()
        bodies = _CompressedBodies(
            tuple(self.chunks), tuple(self.starts), self.event_count)
        lane = _EventLane(bodies, tuple(self.selectors))
        ordered_entries = sorted(
            self.entries,
            key=lambda entry: (
                self.event_keys[entry] if isinstance(entry, int) else entry.ref.key
            ),
        )
        return _CompactPublicObjects(
            release_ref,
            replay_ref,
            lane,
            tuple(ordered_entries),
            tuple(sorted(self.non_events, key=lambda obj: obj.ref.key)),
            MappingProxyType({
                key: _RespondentEvents(lane, tuple(rows))
                for key, rows in self.groups.items()
            }),
            frozenset(self.event_states),
        )


def _rebind_compact(compact: _CompactPublicObjects, bodies) -> _CompactPublicObjects:
    lane = _EventLane(bodies, compact.lane.selectors)
    by_respondent = MappingProxyType({
        key: _RespondentEvents(lane, tuple(events.rows))
        for key, events in compact.by_respondent.items()
    })
    return _CompactPublicObjects(
        compact.release_ref,
        compact.replay_ref,
        lane,
        compact.entries,
        compact.non_events,
        by_respondent,
        compact.event_states,
    )


def _iter_compressed_bodies(bodies):
    import pyarrow as pa

    if not isinstance(bodies, _CompressedBodies):
        return
    for compressed, raw_size, _start, count in bodies.chunks:
        raw = pa.decompress(
            compressed,
            decompressed_size=raw_size,
            codec=_EVENT_BODY_CODEC,
            asbytes=True,
        )
        position = 0
        for _ in range(count):
            length = int.from_bytes(raw[position:position + 4], "big")
            position += 4
            yield raw[position:position + length]
            position += length


def _write_compact_bodies(path, key: str, envelope: Mapping[str, Any], bodies) -> bool:
    import pyarrow as pa

    if not isinstance(bodies, _CompressedBodies):
        return False
    writer = None
    committed = False
    try:
        writer = _BodyCacheWriter(path, key, envelope=envelope)
        batch = []
        for body in _iter_compressed_bodies(bodies):
            batch.append(body)
            if len(batch) >= _EVENT_BODY_CHUNK_EVENTS:
                writer.write_batch(batch)
                batch.clear()
        if batch:
            writer.write_batch(batch)
        writer.commit(path)
        committed = True
    except (OSError, ValueError, pa.ArrowException):
        if writer is not None:
            writer.abort()
    finally:
        if writer is not None and not committed:
            writer.abort()
    return committed


def attach_governed_cache(
    release,
    *,
    physical_binding,
    projection_binding: str,
):
    """Attach the existing governed cache to a cold compact release.

    A valid cache hit replaces the in-memory compressed bodies with the exact
    authenticated cached lane.  A miss writes the same bodies through the
    existing atomic ``_BodyCacheWriter`` under the explicit host policy.  Any
    policy/write failure is a safe miss; the validated in-memory release is
    returned unchanged.
    """
    from rawlsing_next.pre553_c11_repository import C11LogicalRelease

    if not isinstance(release, C11LogicalRelease):
        return release
    compact = release.public_objects
    if not isinstance(compact, _CompactPublicObjects):
        return release
    policy = _cache_policy()
    if policy is None:
        return release
    binding = physical_binding()
    if binding is None:
        return release
    key, envelope, path = _cache_identity(
        release,
        compact.lane.selectors,
        binding=binding,
        projection_binding=projection_binding,
        policy=policy,
    )
    cached = _read_bodies(
        path, key, compact.lane.selectors, policy=policy, envelope=envelope)
    if cached is not None:
        return replace(release, public_objects=_rebind_compact(compact, cached))
    if _write_compact_bodies(path, key, envelope, compact.lane.bodies):
        enforce_after_write(policy, path)
    return release


__all__ = ["ColdCompactBuilder", "attach_governed_cache"]
