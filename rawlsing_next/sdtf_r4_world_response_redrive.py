"""SDTF R4 externalized-occurrence source binding and deterministic redrive seam.

This module does not admit events.  It validates and conserves an already-admitted
externalized occurrence as an exact source for later world/response consumers.
Drafts, rejected/unemitted artifacts and emitted-but-unadmitted artifacts fail
closed.  The current-response consequence exposed here is explicitly non-durable.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re
from typing import Any, Iterable

from rawlsing_next.wsc_gt0_protocol import (
    GT0ConservationEnvelope,
    GT0ExactRef,
    GT0StageReceipt,
    GT0StageStatus,
    gt0_content_hash,
    validate_exact_upstream_ref,
)

R4_CONTRACT_ID = "SDTF_R4_EXTERNALIZED_OCCURRENCE_WORLD_RESPONSE_REDRIVE@1.0.0"
R4_SOURCE_SCHEMA = "SDTF_R4_EXTERNALIZED_OCCURRENCE_SOURCE_BINDING@1.0.0"
R4_CURRENT_RESPONSE_SCHEMA = "SDTF_R4_CURRENT_RESPONSE_CONSEQUENCE@1.0.0"
R4_REDRIVE_STAGE_ID = "SDTF_R4_EXTERNALIZED_OCCURRENCE_REDRIVE"
NON_DURABLE_DISPOSITION = "NON_DURABLE_CURRENT_RESPONSE_CONSEQUENCE"

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_MUTABLE_RE = re.compile(
    r"(^|[:/@._-])(latest|default|fuzzy|nearest|semver(?:_fallback)?|\*)(?:$|[:/@._-])",
    re.IGNORECASE,
)


class R4SourceError(ValueError):
    """Base error for an invalid R4 source binding."""


class R4OccurrenceStateError(R4SourceError):
    """The artifact has not become an admitted externalized occurrence."""


class R4BindingMismatchError(R4SourceError):
    """Actor/scope binding does not match the consuming context."""


class R4RedriveError(R4SourceError):
    """The exact source required for deterministic redrive is missing or stale."""


class ExternalizationState(str, Enum):
    DRAFT = "DRAFT"
    REJECTED = "REJECTED"
    UNEMITTED = "UNEMITTED"
    EMITTED_UNADMITTED = "EMITTED_UNADMITTED"
    ADMITTED_EXTERNAL_OCCURRENCE = "ADMITTED_EXTERNAL_OCCURRENCE"


def _exact_text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise R4SourceError(f"{name} must be a non-empty string")
    out = value.strip()
    if _MUTABLE_RE.search(out):
        raise R4SourceError(f"{name} must be exact; mutable selection is forbidden")
    return out


def _sha256(value: Any, name: str) -> str:
    out = _exact_text(value, name)
    if not _SHA256_RE.fullmatch(out):
        raise R4SourceError(f"{name} must be an exact lowercase sha256")
    return out


def _state(value: ExternalizationState | str) -> ExternalizationState:
    if isinstance(value, ExternalizationState):
        return value
    try:
        return ExternalizationState(_exact_text(value, "externalization_state"))
    except ValueError as exc:
        raise R4OccurrenceStateError(f"unknown externalization state {value!r}") from exc


def _ref(value: Any, name: str, *, require_hash: bool = False) -> GT0ExactRef:
    try:
        ref = validate_exact_upstream_ref(value, name)
    except (ValueError, TypeError) as exc:
        raise R4SourceError(str(exc)) from exc
    if require_hash and ref.content_hash is None:
        raise R4SourceError(f"{name} must be content-addressed")
    return ref


def _refs(values: Iterable[Any], name: str, *, nonempty: bool = False, require_hash: bool = False) -> tuple[GT0ExactRef, ...]:
    out: dict[str, GT0ExactRef] = {}
    for value in values:
        ref = _ref(value, name, require_hash=require_hash)
        out[ref.key] = ref
    refs = tuple(out[key] for key in sorted(out))
    if nonempty and not refs:
        raise R4SourceError(f"{name}s must not be empty")
    return refs


@dataclass(frozen=True, slots=True)
class ExternalizedOccurrenceCandidate:
    """Exact material offered to R4; this object itself does not admit an event."""

    state: ExternalizationState | str
    occurrence_id: str
    occurrence_hash: str
    authority_id: str
    authority_version: str
    authority_hash: str
    effective_time_ref: GT0ExactRef | Any
    actor_ref: GT0ExactRef | Any
    scope_ref: GT0ExactRef | Any
    world_context_ref: GT0ExactRef | Any
    stream_ref: GT0ExactRef | Any
    admission_receipt_ref: GT0ExactRef | Any
    causal_use_permission_ref: GT0ExactRef | Any
    provenance_refs: tuple[GT0ExactRef | Any, ...]
    replay_refs: tuple[GT0ExactRef | Any, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "state", _state(self.state))
        object.__setattr__(self, "occurrence_id", _exact_text(self.occurrence_id, "occurrence_id"))
        object.__setattr__(self, "occurrence_hash", _sha256(self.occurrence_hash, "occurrence_hash"))
        object.__setattr__(self, "authority_id", _exact_text(self.authority_id, "authority_id"))
        object.__setattr__(self, "authority_version", _exact_text(self.authority_version, "authority_version"))
        object.__setattr__(self, "authority_hash", _sha256(self.authority_hash, "authority_hash"))
        object.__setattr__(self, "effective_time_ref", _ref(self.effective_time_ref, "effective_time_ref", require_hash=True))
        object.__setattr__(self, "actor_ref", _ref(self.actor_ref, "actor_ref", require_hash=True))
        object.__setattr__(self, "scope_ref", _ref(self.scope_ref, "scope_ref", require_hash=True))
        object.__setattr__(self, "world_context_ref", _ref(self.world_context_ref, "world_context_ref", require_hash=True))
        object.__setattr__(self, "stream_ref", _ref(self.stream_ref, "stream_ref", require_hash=True))
        object.__setattr__(self, "admission_receipt_ref", _ref(self.admission_receipt_ref, "admission_receipt_ref", require_hash=True))
        object.__setattr__(self, "causal_use_permission_ref", _ref(self.causal_use_permission_ref, "causal_use_permission_ref", require_hash=True))
        object.__setattr__(self, "provenance_refs", _refs(self.provenance_refs, "provenance_ref", nonempty=True, require_hash=True))
        object.__setattr__(self, "replay_refs", _refs(self.replay_refs, "replay_ref", nonempty=True, require_hash=True))

    @property
    def occurrence_ref(self) -> GT0ExactRef:
        return GT0ExactRef("EXTERNALIZED_OCCURRENCE", self.occurrence_id, self.occurrence_hash)

    @property
    def authority_ref(self) -> GT0ExactRef:
        return GT0ExactRef(
            "EXTERNAL_EVENT_AUTHORITY",
            f"{self.authority_id}@{self.authority_version}",
            self.authority_hash,
        )


@dataclass(frozen=True, slots=True)
class ExternalizedOccurrenceSourceBinding:
    """Reference-preserving source binding for one already-admitted occurrence."""

    candidate: ExternalizedOccurrenceCandidate
    envelope: GT0ConservationEnvelope

    @property
    def source_hash(self) -> str:
        return self.envelope.content_hash

    def identity_material(self) -> dict[str, Any]:
        c = self.candidate
        return {
            "schema": R4_SOURCE_SCHEMA,
            "contract": R4_CONTRACT_ID,
            "state": c.state.value,
            "occurrence_ref": c.occurrence_ref,
            "authority_ref": c.authority_ref,
            "effective_time_ref": c.effective_time_ref,
            "actor_ref": c.actor_ref,
            "scope_ref": c.scope_ref,
            "world_context_ref": c.world_context_ref,
            "stream_ref": c.stream_ref,
            "admission_receipt_ref": c.admission_receipt_ref,
            "causal_use_permission_ref": c.causal_use_permission_ref,
            "provenance_refs": c.provenance_refs,
            "replay_refs": c.replay_refs,
            "envelope_hash": self.envelope.content_hash,
        }

    @property
    def content_hash(self) -> str:
        return gt0_content_hash(self.identity_material())


@dataclass(frozen=True, slots=True)
class CurrentResponseConsequence:
    """Non-durable handoff. Persistence/durable mutation is intentionally absent."""

    source_binding_hash: str
    actor_ref: GT0ExactRef | Any
    scope_ref: GT0ExactRef | Any
    consequence_refs: tuple[GT0ExactRef | Any, ...] = ()
    durability: str = NON_DURABLE_DISPOSITION

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_binding_hash", _sha256(self.source_binding_hash, "source_binding_hash"))
        object.__setattr__(self, "actor_ref", _ref(self.actor_ref, "actor_ref"))
        object.__setattr__(self, "scope_ref", _ref(self.scope_ref, "scope_ref"))
        object.__setattr__(self, "consequence_refs", _refs(self.consequence_refs, "consequence_ref"))
        if self.durability != NON_DURABLE_DISPOSITION:
            raise R4SourceError("current response consequence cannot be promoted to durable state")

    @property
    def content_hash(self) -> str:
        return gt0_content_hash({
            "schema": R4_CURRENT_RESPONSE_SCHEMA,
            "source_binding_hash": self.source_binding_hash,
            "actor_ref": self.actor_ref,
            "scope_ref": self.scope_ref,
            "consequence_refs": self.consequence_refs,
            "durability": self.durability,
        })


@dataclass(frozen=True, slots=True)
class RedriveResult:
    source: ExternalizedOccurrenceSourceBinding
    receipt: GT0StageReceipt
    current_response_consequence: CurrentResponseConsequence


def bind_admitted_externalized_occurrence_source(
    candidate: ExternalizedOccurrenceCandidate,
    *,
    expected_actor_ref: GT0ExactRef | Any,
    expected_scope_ref: GT0ExactRef | Any,
) -> ExternalizedOccurrenceSourceBinding:
    """Conserve one *already admitted* occurrence as an R4 source; never admit it here."""
    if not isinstance(candidate, ExternalizedOccurrenceCandidate):
        raise R4SourceError("candidate must be ExternalizedOccurrenceCandidate")
    if candidate.state is not ExternalizationState.ADMITTED_EXTERNAL_OCCURRENCE:
        raise R4OccurrenceStateError(
            f"{candidate.state.value} is not an admitted externalized occurrence"
        )

    expected_actor = _ref(expected_actor_ref, "expected_actor_ref")
    expected_scope = _ref(expected_scope_ref, "expected_scope_ref")
    if candidate.actor_ref != expected_actor:
        raise R4BindingMismatchError("externalized occurrence actor binding mismatch")
    if candidate.scope_ref != expected_scope:
        raise R4BindingMismatchError("externalized occurrence scope binding mismatch")

    envelope = GT0ConservationEnvelope(
        semantic_owner_ref=candidate.authority_ref,
        object_refs=(candidate.occurrence_ref,),
        authority_refs=(candidate.authority_ref, candidate.admission_receipt_ref, candidate.causal_use_permission_ref),
        current_selection_refs=(candidate.effective_time_ref,),
        scope_refs=(candidate.actor_ref, candidate.scope_ref, candidate.world_context_ref),
        permission_ceiling=("PRECIPITATING_EVENT_SOURCE", "REDRIVE_REPLAY"),
        dependency_refs=(candidate.admission_receipt_ref, candidate.causal_use_permission_ref, candidate.stream_ref),
        provenance_refs=candidate.provenance_refs,
        replay_refs=candidate.replay_refs,
        status=GT0StageStatus.PASS,
        information_loss="NONE__EXACT_EXTERNALIZED_OCCURRENCE_REFERENCE_PRESERVED",
    )
    return ExternalizedOccurrenceSourceBinding(candidate=candidate, envelope=envelope)


def redrive_externalized_occurrence(
    source: ExternalizedOccurrenceSourceBinding | None,
    *,
    expected_source_hash: str,
    expected_actor_ref: GT0ExactRef | Any,
    expected_scope_ref: GT0ExactRef | Any,
    consequence_refs: Iterable[GT0ExactRef | Any] = (),
) -> RedriveResult:
    """Replay from the exact bound occurrence, or fail closed if the source is missing/stale."""
    if source is None:
        raise R4RedriveError("redrive requires the exact externalized occurrence source")
    if not isinstance(source, ExternalizedOccurrenceSourceBinding):
        raise R4RedriveError("redrive source has the wrong type")
    expected_hash = _sha256(expected_source_hash, "expected_source_hash")
    if source.source_hash != expected_hash:
        raise R4RedriveError("externalized occurrence source is stale or hash-mismatched")

    rebound = bind_admitted_externalized_occurrence_source(
        source.candidate,
        expected_actor_ref=expected_actor_ref,
        expected_scope_ref=expected_scope_ref,
    )
    if rebound.source_hash != source.source_hash:
        raise R4RedriveError("externalized occurrence source failed deterministic reconstruction")

    consequence = CurrentResponseConsequence(
        source_binding_hash=source.source_hash,
        actor_ref=source.candidate.actor_ref,
        scope_ref=source.candidate.scope_ref,
        consequence_refs=tuple(consequence_refs),
    )
    receipt = GT0StageReceipt(
        stage_id=R4_REDRIVE_STAGE_ID,
        status=GT0StageStatus.PASS,
        input_envelope_hashes=(source.envelope.content_hash,),
        output_envelope=rebound.envelope,
        upstream_refs=(source.candidate.occurrence_ref, source.candidate.admission_receipt_ref, source.candidate.causal_use_permission_ref, source.candidate.stream_ref, source.candidate.world_context_ref),
        authority_refs=(source.candidate.authority_ref, source.candidate.causal_use_permission_ref),
        replay_refs=source.candidate.replay_refs,
        detail_code="EXACT_EXTERNALIZED_OCCURRENCE_REDRIVE__NON_DURABLE_CONSEQUENCE",
    )
    return RedriveResult(source=rebound, receipt=receipt, current_response_consequence=consequence)


__all__ = [
    "R4_CONTRACT_ID",
    "R4_SOURCE_SCHEMA",
    "R4_CURRENT_RESPONSE_SCHEMA",
    "R4_REDRIVE_STAGE_ID",
    "NON_DURABLE_DISPOSITION",
    "R4SourceError",
    "R4OccurrenceStateError",
    "R4BindingMismatchError",
    "R4RedriveError",
    "ExternalizationState",
    "ExternalizedOccurrenceCandidate",
    "ExternalizedOccurrenceSourceBinding",
    "CurrentResponseConsequence",
    "RedriveResult",
    "bind_admitted_externalized_occurrence_source",
    "redrive_externalized_occurrence",
]
