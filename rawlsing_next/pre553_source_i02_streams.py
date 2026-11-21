"""Bounded synchronous body transport for the Q2 source→direct-I02 handoff.

The existing S2-B ``build_sourcefree_direct_i02`` consumes each of the 13 typed
family iterables exactly once and writes a metadata/selector certificate.  It
does not retain the canonical bodies: the selected native reader later needs a
separate sealed body repository.

This helper adds the missing Q2 producer ABI without creating a second source
read, a second authoritative body corpus, or a new semantic engine.  A caller
supplies a sink; while the existing direct builder consumes the one-shot family
streams, the same exact objects are synchronously delivered to that sink.  The
sink is a body-transport proof/consumer seam (for example a future Q3 estate
writer), not a mocked native I03 or Q3 acceptance.

Lifetime contract:

* ``begin`` happens before the source is opened and before any body is read.
* ``emit``/``absence`` happen inside the producer's one bounded pass.
* ``finish`` happens only after the direct certificate has been published and
  its external roots are fixed; the sink receives those exact roots.
* ``abort`` happens on any producer/sink failure and must discard staged sink
  output.  The producer also invalidates its certificate if it was published.

The sink must stage until ``finish`` and must not publish partial bodies.  The
adapter never retains the sink after the handoff call.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Protocol, runtime_checkable

from rawlsing_next._pre553_direct_i02_sourcefree import (
    SourcefreeDirectI02Sections,
)
from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_c11_ingest import SourceReleaseManifest
from rawlsing_next.pre553_c11_integrity import TypedAbsence
from rawlsing_next.pre553_empirical_objects import ExactRef

BODY_TRANSPORT_SCHEMA = "PYAT960_S1E_SOURCE_I02_BODY_TRANSPORT@1.0.0"

# The exact 13 original C11 logical families.  This is the same set the S2-B
# direct builder requires; order is not semantically significant.
ALL_FAMILIES = (
    "EmpiricalUniverse",
    "RespondentIdentity",
    "QuestionVariableBinding",
    "RespondentEvent",
    "RoutingEligibilityFact",
    "EmpiricalCoordinateFact",
    "WeightMeasureFact",
    "AuthoritySnapshot",
    "SourceUniverseRelation",
    "EmpiricalPredicateReplayBinding",
    "ComparatorReplayBinding",
    "DiscoveryBranchReplayBinding",
    "StructuralAdmissionReplayBinding",
)

_SINK_METHODS = ("begin", "emit", "absence", "finish", "abort")


class SourceI02BodyTransportRefusal(ValueError):
    """The body transport is absent, misused, incomplete, or failed closed."""

    def __init__(self, code: str, detail: Any = None):
        super().__init__(code if detail is None else f"{code}: {detail}")
        self.code = code
        self.detail = detail


@runtime_checkable
class SourceI02BodySink(Protocol):
    """Caller-owned bounded body consumer with an explicit staging lifecycle."""

    def begin(
        self,
        *,
        source_sha256: str,
        source_id: str,
        universe_ref: ExactRef,
        projection_identity_ref: ExactRef,
    ) -> None:
        """Start staging before any source byte is opened."""

    def emit(self, family: str, obj: object) -> None:
        """Stage one exact canonical/internal body from the one-shot stream."""

    def absence(self, family: str, absence: TypedAbsence) -> None:
        """Record one lawfully typed absence; no body will be emitted."""

    def finish(
        self,
        *,
        roots: ExternalI02Roots,
        manifest: SourceReleaseManifest,
        counts: Mapping[str, int],
        transport: Mapping[str, Any],
    ) -> None:
        """Commit the staged bodies against the already-published exact roots."""

    def abort(self, exc: BaseException) -> None:
        """Discard staged bodies after any producer/sink failure."""


@dataclass(frozen=True)
class SourceI02BodyTransportStats:
    schema: str
    sink_class: str
    families: Mapping[str, int]
    absences: Mapping[str, str]
    empty_families: tuple[str, ...]
    object_count: int
    complete: bool
    finished: bool
    aborted: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "sink_class": self.sink_class,
            "families": dict(self.families),
            "absences": dict(self.absences),
            "empty_families": list(self.empty_families),
            "object_count": self.object_count,
            "complete": self.complete,
            "finished": self.finished,
            "aborted": self.aborted,
        }


def _require_sink(sink: Any) -> None:
    if sink is None:
        raise SourceI02BodyTransportRefusal("BODY_SINK_REQUIRED")
    for name in _SINK_METHODS:
        if not callable(getattr(sink, name, None)):
            raise SourceI02BodyTransportRefusal(
                "BODY_SINK_METHOD_MISSING", name)


def _sink_class(sink: Any) -> str:
    cls = type(sink)
    return f"{cls.__module__}.{cls.__qualname__}"


class SourceI02BodyTee:
    """Tee the one-shot Q2 family streams into a caller-owned sink.

    The original ``SourcefreeDirectI02Sections`` is never consumed by this
    object.  Only the resulting teed sections are passed to the direct builder,
    so the builder and the sink observe the same single materialization.
    """

    def __init__(
        self,
        sink: Any,
        *,
        source_sha256: str,
        source_id: str,
        universe_ref: ExactRef,
        projection_identity_ref: ExactRef,
    ) -> None:
        _require_sink(sink)
        if not isinstance(source_sha256, str) or len(source_sha256) != 64:
            raise SourceI02BodyTransportRefusal("BODY_SOURCE_SHA_REQUIRED")
        if not isinstance(source_id, str) or not source_id.strip():
            raise SourceI02BodyTransportRefusal("BODY_SOURCE_ID_REQUIRED")
        if not isinstance(universe_ref, ExactRef):
            raise SourceI02BodyTransportRefusal("BODY_UNIVERSE_REF_REQUIRED")
        if not isinstance(projection_identity_ref, ExactRef):
            raise SourceI02BodyTransportRefusal(
                "BODY_PROJECTION_IDENTITY_REF_REQUIRED")
        self._sink = sink
        self._source_sha256 = source_sha256
        self._source_id = source_id
        self._universe_ref = universe_ref
        self._projection_identity_ref = projection_identity_ref
        self._state = "new"
        self._source: SourcefreeDirectI02Sections | None = None
        self._teed: SourcefreeDirectI02Sections | None = None
        self._counts: Counter[str] = Counter()
        self._absences: dict[str, str] = {}
        self._object_count = 0

    @property
    def state(self) -> str:
        return self._state

    @property
    def source(self) -> SourcefreeDirectI02Sections:
        if self._teed is None:
            raise SourceI02BodyTransportRefusal("BODY_SOURCE_NOT_ATTACHED")
        return self._teed

    def begin(self) -> None:
        if self._state != "new":
            raise SourceI02BodyTransportRefusal(
                "BODY_SINK_BEGIN_INVALID_STATE", self._state)
        self._sink.begin(
            source_sha256=self._source_sha256,
            source_id=self._source_id,
            universe_ref=self._universe_ref,
            projection_identity_ref=self._projection_identity_ref,
        )
        self._state = "open"

    def attach(self, source: SourcefreeDirectI02Sections) -> SourcefreeDirectI02Sections:
        if self._state != "open":
            raise SourceI02BodyTransportRefusal(
                "BODY_SOURCE_ATTACH_INVALID_STATE", self._state)
        if type(source) is not SourcefreeDirectI02Sections:
            raise SourceI02BodyTransportRefusal("BODY_SOURCE_TYPE_INVALID")
        if set(source.sections) != set(ALL_FAMILIES):
            raise SourceI02BodyTransportRefusal(
                "BODY_SOURCE_FAMILY_SET_MISMATCH",
                sorted(set(source.sections) ^ set(ALL_FAMILIES)),
            )
        if not set(source.typed_absences).issubset(set(ALL_FAMILIES)):
            raise SourceI02BodyTransportRefusal(
                "BODY_SOURCE_ABSENCE_FAMILY_INVALID")
        self._source = source
        for family in ALL_FAMILIES:
            absence = source.typed_absences.get(family)
            if absence is None:
                continue
            if type(absence) is not TypedAbsence:
                raise SourceI02BodyTransportRefusal(
                    "BODY_SOURCE_ABSENCE_TYPE_INVALID", family)
            self._sink.absence(family, absence)
            self._absences[family] = absence.state
        sections = {
            family: self._tee(family, source.sections[family])
            for family in ALL_FAMILIES
        }
        self._teed = SourcefreeDirectI02Sections(
            manifest=source.manifest,
            sections=MappingProxyType(sections),
            typed_absences=source.typed_absences,
            replay_protocol_authority_ref=source.replay_protocol_authority_ref,
            replay_protocol_version=source.replay_protocol_version,
            deterministic_tie_order_rules_ref=(
                source.deterministic_tie_order_rules_ref),
        )
        self._state = "streaming"
        return self._teed

    def _tee(self, family: str, iterable: Iterable[object]) -> Iterable[object]:
        for obj in iterable:
            if self._state != "streaming":
                raise SourceI02BodyTransportRefusal(
                    "BODY_SINK_NOT_STREAMING", self._state)
            if type(obj).__name__ != family:
                raise SourceI02BodyTransportRefusal(
                    "BODY_TRANSPORT_FAMILY_MISMATCH",
                    {"expected": family, "actual": type(obj).__name__},
                )
            self._sink.emit(family, obj)
            self._counts[family] += 1
            self._object_count += 1
            yield obj

    def finish(
        self,
        *,
        roots: ExternalI02Roots,
        manifest: SourceReleaseManifest,
        counts: Mapping[str, int],
    ) -> Mapping[str, Any]:
        if self._state != "streaming":
            raise SourceI02BodyTransportRefusal(
                "BODY_SINK_FINISH_INVALID_STATE", self._state)
        if not isinstance(roots, ExternalI02Roots):
            raise SourceI02BodyTransportRefusal("BODY_ROOT_TYPE_INVALID")
        if type(manifest) is not SourceReleaseManifest:
            raise SourceI02BodyTransportRefusal("BODY_MANIFEST_TYPE_INVALID")
        actual = {family: int(self._counts.get(family, 0))
                  for family in ALL_FAMILIES}
        expected = {family: int(counts.get(family, 0))
                    for family in ALL_FAMILIES}
        if actual != expected:
            raise SourceI02BodyTransportRefusal(
                "BODY_TRANSPORT_CENSUS_MISMATCH",
                {"actual": actual, "expected": expected},
            )
        transport = self._stats(finished=True, aborted=False)
        self._sink.finish(
            roots=roots,
            manifest=manifest,
            counts=MappingProxyType(expected),
            transport=transport.as_dict(),
        )
        self._state = "finished"
        return transport.as_dict()

    def abort(self, exc: BaseException) -> None:
        if self._state in ("finished", "aborted"):
            return
        self._state = "aborted"
        try:
            self._sink.abort(exc)
        except Exception:
            # The producer's primary failure must not be masked by a sink
            # cleanup failure.  The producer still invalidates its own output.
            pass

    def _stats(self, *, finished: bool, aborted: bool) -> SourceI02BodyTransportStats:
        families = {family: int(self._counts.get(family, 0))
                    for family in ALL_FAMILIES}
        empty_families = tuple(
            family for family in ALL_FAMILIES
            if families[family] == 0 and family not in self._absences
        )
        complete = set(families) == set(ALL_FAMILIES)
        return SourceI02BodyTransportStats(
            schema=BODY_TRANSPORT_SCHEMA,
            sink_class=_sink_class(self._sink),
            families=MappingProxyType(families),
            absences=MappingProxyType(dict(sorted(self._absences.items()))),
            empty_families=empty_families,
            object_count=int(self._object_count),
            complete=complete,
            finished=finished,
            aborted=aborted,
        )

    def stats(self) -> Mapping[str, Any]:
        return self._stats(
            finished=self._state == "finished",
            aborted=self._state == "aborted",
        ).as_dict()


__all__ = [
    "BODY_TRANSPORT_SCHEMA",
    "ALL_FAMILIES",
    "SourceI02BodyTransportRefusal",
    "SourceI02BodySink",
    "SourceI02BodyTransportStats",
    "SourceI02BodyTee",
]
