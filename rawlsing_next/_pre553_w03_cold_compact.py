"""Cold streaming compact lane for W03/W04.

This helper is a physical-memory optimisation, not a semantic engine.  It builds
the existing private compact event lane from an already-validated event stream
and never creates a second C11 store, selector language or query engine.
"""
from __future__ import annotations

from types import MappingProxyType
from typing import Any, Mapping

from rawlsing_next._pre553_c11_execution_view import (
    _CompressedBodies,
    _CompactPublicObjects,
    _EVENT_BODY_CHUNK_EVENTS,
    _EventLane,
    _EventRead,
    _RespondentEvents,
    _compress_body_chunk,
    _ref_identity,
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


__all__ = ["ColdCompactBuilder"]
