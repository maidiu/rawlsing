"""SDTF R4 externalized-occurrence/world-response admission and redrive seam.

The seam is deliberately narrow.  It never admits an event, authors a world
response, writes a world, or mints D1' facts.  It only conserves exact,
content-addressed identities for already-admitted external sources and turns an
externally-authored objective change into an ordinary R4
invalidation/rederivation *request*.
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
R4_OCCURRENCE_SOURCE_SCHEMA = "SDTF_R4_EXTERNALIZED_OCCURRENCE_SOURCE_BINDING@1.0.0"
R4_WORLD_RESPONSE_SOURCE_SCHEMA = "SDTF_R4_EXTERNAL_WORLD_RESPONSE_SOURCE_BINDING@1.0.0"
R4_REQUEST_SCHEMA = "SDTF_R4_INVALIDATION_REDERIVATION_REQUEST@1.0.0"
R4_CURRENT_RESPONSE_SCHEMA = "SDTF_R4_CURRENT_RESPONSE_CONSEQUENCE@1.0.0"
R4_REDRIVE_STAGE_ID = "SDTF_R4_EXTERNAL_WORLD_RESPONSE_REDRIVE_REQUEST"
NON_DURABLE_DISPOSITION = "NON_DURABLE_CURRENT_RESPONSE_CONSEQUENCE"
OBJECTIVE_CHANGED_DETERMINANT_KIND = "OBJECTIVE_CHANGED_DETERMINANT"

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_MUTABLE_RE = re.compile(
    r"(^|[:/@._-])(latest|default|fuzzy|nearest|semver(?:_fallback)?|\*)(?:$|[:/@._-])",
    re.IGNORECASE,
)


class R4SourceError(ValueError):
    """Base error for an invalid R4 source binding."""


class R4OccurrenceStateError(R4SourceError):
    """The artifact has not become an admitted externalized occurrence."""


class R4WorldResponseStateError(R4SourceError):
    """The alleged world response lacks competent external objective admission."""


class R4BindingMismatchError(R4SourceError):
    """Actor/scope/world-context binding does not match the consuming context."""


class R4RedriveError(R4SourceError):
    """The exact source required for deterministic redrive is missing or stale."""


class ExternalizationState(str, Enum):
    DRAFT = "DRAFT"
    REJECTED = "REJECTED"
    UNEMITTED = "UNEMITTED"
    EMITTED_UNADMITTED = "EMITTED_UNADMITTED"
    ADMITTED_EXTERNAL_OCCURRENCE = "ADMITTED_EXTERNAL_OCCURRENCE"


class WorldResponseAdmissionState(str, Enum):
    DRAFT = "DRAFT"
    REJECTED = "REJECTED"
    UNEMITTED = "UNEMITTED"
    EMITTED_UNADMITTED = "EMITTED_UNADMITTED"
    ADMITTED_OBJECTIVE_WORLD_RESPONSE = "ADMITTED_OBJECTIVE_WORLD_RESPONSE"


class WorldResponseSourceKind(str, Enum):
    COMPETENT_EXTERNAL_OBJECTIVE_SOURCE = "COMPETENT_EXTERNAL_OBJECTIVE_SOURCE"
    PRIVATE_V3_STATE = "PRIVATE_V3_STATE"
    GENERIC_WORLD_SIMULATION = "GENERIC_WORLD_SIMULATION"
    INTERPRETATION_EXPECTATION_STRIVING = "INTERPRETATION_EXPECTATION_STRIVING"
    OEE_ENCOUNTER_DERIVATION = "OEE_ENCOUNTER_DERIVATION"


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


def _enum(value: Any, enum_type: type[Enum], name: str, error_type: type[R4SourceError]) -> Enum:
    if isinstance(value, enum_type):
        return value
    try:
        return enum_type(_exact_text(value, name))
    except ValueError as exc:
        raise error_type(f"unknown {name} {value!r}") from exc


def _ref(value: Any, name: str, *, require_hash: bool = False) -> GT0ExactRef:
    try:
        ref = validate_exact_upstream_ref(value, name)
    except (ValueError, TypeError) as exc:
        raise R4SourceError(str(exc)) from exc
    if require_hash and ref.content_hash is None:
        raise R4SourceError(f"{name} must be content-addressed")
    return ref


def _refs(
    values: Iterable[Any],
    name: str,
    *,
    nonempty: bool = False,
    require_hash: bool = False,
) -> tuple[GT0ExactRef, ...]:
    out: dict[str, GT0ExactRef] = {}
    for value in values:
        ref = _ref(value, name, require_hash=require_hash)
        out[ref.key] = ref
    refs = tuple(out[key] for key in sorted(out))
    if nonempty and not refs:
        raise R4SourceError(f"{name}s must not be empty")
    return refs


def _merge_refs(*groups: Iterable[GT0ExactRef]) -> tuple[GT0ExactRef, ...]:
    by_key: dict[str, GT0ExactRef] = {}
    for group in groups:
        for ref in group:
            by_key[ref.key] = ref
    return tuple(by_key[key] for key in sorted(by_key))


@dataclass(frozen=True, slots=True)
class ExternalizedOccurrenceCandidate:
    """Exact material offered to R4; construction does not admit an event."""

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
        object.__setattr__(
            self,
            "state",
            _enum(self.state, ExternalizationState, "externalization_state", R4OccurrenceStateError),
        )
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
    candidate: ExternalizedOccurrenceCandidate
    envelope: GT0ConservationEnvelope

    @property
    def source_hash(self) -> str:
        return self.envelope.content_hash

    @property
    def content_hash(self) -> str:
        c = self.candidate
        return gt0_content_hash(
            {
                "schema": R4_OCCURRENCE_SOURCE_SCHEMA,
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
        )


@dataclass(frozen=True, slots=True)
class ExternalWorldResponseCandidate:
    """Externally-authored objective response; R4 may reference but never author it."""

    state: WorldResponseAdmissionState | str
    source_kind: WorldResponseSourceKind | str
    response_id: str
    response_hash: str
    authority_id: str
    authority_version: str
    authority_hash: str
    effective_time_ref: GT0ExactRef | Any
    counterpart_ref: GT0ExactRef | Any
    scope_ref: GT0ExactRef | Any
    world_context_ref: GT0ExactRef | Any
    admission_receipt_ref: GT0ExactRef | Any
    objective_source_permission_ref: GT0ExactRef | Any
    changed_determinant_refs: tuple[GT0ExactRef | Any, ...]
    provenance_refs: tuple[GT0ExactRef | Any, ...]
    replay_refs: tuple[GT0ExactRef | Any, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "state",
            _enum(self.state, WorldResponseAdmissionState, "world_response_state", R4WorldResponseStateError),
        )
        object.__setattr__(
            self,
            "source_kind",
            _enum(self.source_kind, WorldResponseSourceKind, "world_response_source_kind", R4WorldResponseStateError),
        )
        object.__setattr__(self, "response_id", _exact_text(self.response_id, "response_id"))
        object.__setattr__(self, "response_hash", _sha256(self.response_hash, "response_hash"))
        object.__setattr__(self, "authority_id", _exact_text(self.authority_id, "world_response_authority_id"))
        object.__setattr__(self, "authority_version", _exact_text(self.authority_version, "world_response_authority_version"))
        object.__setattr__(self, "authority_hash", _sha256(self.authority_hash, "world_response_authority_hash"))
        object.__setattr__(self, "effective_time_ref", _ref(self.effective_time_ref, "world_response_effective_time_ref", require_hash=True))
        object.__setattr__(self, "counterpart_ref", _ref(self.counterpart_ref, "counterpart_ref", require_hash=True))
        object.__setattr__(self, "scope_ref", _ref(self.scope_ref, "world_response_scope_ref", require_hash=True))
        object.__setattr__(self, "world_context_ref", _ref(self.world_context_ref, "world_response_world_context_ref", require_hash=True))
        object.__setattr__(self, "admission_receipt_ref", _ref(self.admission_receipt_ref, "world_response_admission_receipt_ref", require_hash=True))
        object.__setattr__(self, "objective_source_permission_ref", _ref(self.objective_source_permission_ref, "objective_source_permission_ref", require_hash=True))
        determinants = _refs(self.changed_determinant_refs, "changed_determinant_ref", nonempty=True, require_hash=True)
        if any(ref.kind != OBJECTIVE_CHANGED_DETERMINANT_KIND for ref in determinants):
            raise R4WorldResponseStateError(
                "changed determinants must be externally-authored OBJECTIVE_CHANGED_DETERMINANT refs; R4 does not mint D1' facts"
            )
        object.__setattr__(self, "changed_determinant_refs", determinants)
        object.__setattr__(self, "provenance_refs", _refs(self.provenance_refs, "world_response_provenance_ref", nonempty=True, require_hash=True))
        object.__setattr__(self, "replay_refs", _refs(self.replay_refs, "world_response_replay_ref", nonempty=True, require_hash=True))

    @property
    def response_ref(self) -> GT0ExactRef:
        return GT0ExactRef("EXTERNAL_OBJECTIVE_WORLD_RESPONSE", self.response_id, self.response_hash)

    @property
    def authority_ref(self) -> GT0ExactRef:
        return GT0ExactRef(
            "EXTERNAL_OBJECTIVE_SOURCE_AUTHORITY",
            f"{self.authority_id}@{self.authority_version}",
            self.authority_hash,
        )


@dataclass(frozen=True, slots=True)
class ExternalWorldResponseSourceBinding:
    candidate: ExternalWorldResponseCandidate
    envelope: GT0ConservationEnvelope

    @property
    def source_hash(self) -> str:
        return self.envelope.content_hash

    @property
    def content_hash(self) -> str:
        c = self.candidate
        return gt0_content_hash(
            {
                "schema": R4_WORLD_RESPONSE_SOURCE_SCHEMA,
                "contract": R4_CONTRACT_ID,
                "state": c.state.value,
                "source_kind": c.source_kind.value,
                "response_ref": c.response_ref,
                "authority_ref": c.authority_ref,
                "effective_time_ref": c.effective_time_ref,
                "counterpart_ref": c.counterpart_ref,
                "scope_ref": c.scope_ref,
                "world_context_ref": c.world_context_ref,
                "admission_receipt_ref": c.admission_receipt_ref,
                "objective_source_permission_ref": c.objective_source_permission_ref,
                "changed_determinant_refs": c.changed_determinant_refs,
                "provenance_refs": c.provenance_refs,
                "replay_refs": c.replay_refs,
                "envelope_hash": self.envelope.content_hash,
            }
        )


@dataclass(frozen=True, slots=True)
class CurrentResponseConsequence:
    """Private/current response handoff; durable person mutation is forbidden here."""

    occurrence_source_hash: str
    world_response_source_hash: str
    actor_ref: GT0ExactRef | Any
    scope_ref: GT0ExactRef | Any
    consequence_refs: tuple[GT0ExactRef | Any, ...] = ()
    durability: str = NON_DURABLE_DISPOSITION

    def __post_init__(self) -> None:
        object.__setattr__(self, "occurrence_source_hash", _sha256(self.occurrence_source_hash, "occurrence_source_hash"))
        object.__setattr__(self, "world_response_source_hash", _sha256(self.world_response_source_hash, "world_response_source_hash"))
        object.__setattr__(self, "actor_ref", _ref(self.actor_ref, "actor_ref"))
        object.__setattr__(self, "scope_ref", _ref(self.scope_ref, "scope_ref"))
        object.__setattr__(self, "consequence_refs", _refs(self.consequence_refs, "consequence_ref"))
        if self.durability != NON_DURABLE_DISPOSITION:
            raise R4SourceError("current response consequence cannot be promoted to durable person state")

    @property
    def content_hash(self) -> str:
        return gt0_content_hash(
            {
                "schema": R4_CURRENT_RESPONSE_SCHEMA,
                "occurrence_source_hash": self.occurrence_source_hash,
                "world_response_source_hash": self.world_response_source_hash,
                "actor_ref": self.actor_ref,
                "scope_ref": self.scope_ref,
                "consequence_refs": self.consequence_refs,
                "durability": self.durability,
            }
        )


@dataclass(frozen=True, slots=True)
class R4InvalidationRederivationRequest:
    """Pure request object; it does not perform invalidation or rederivation itself."""

    occurrence_source_hash: str
    world_response_source_hash: str
    changed_determinant_refs: tuple[GT0ExactRef, ...]
    request_envelope: GT0ConservationEnvelope
    receipt: GT0StageReceipt

    def __post_init__(self) -> None:
        object.__setattr__(self, "occurrence_source_hash", _sha256(self.occurrence_source_hash, "occurrence_source_hash"))
        object.__setattr__(self, "world_response_source_hash", _sha256(self.world_response_source_hash, "world_response_source_hash"))
        determinants = _refs(self.changed_determinant_refs, "changed_determinant_ref", nonempty=True, require_hash=True)
        if any(ref.kind != OBJECTIVE_CHANGED_DETERMINANT_KIND for ref in determinants):
            raise R4SourceError("R4 request may contain only externally-authored objective changed determinant refs")
        object.__setattr__(self, "changed_determinant_refs", determinants)
        if tuple(self.request_envelope.object_refs) != determinants:
            raise R4SourceError("request envelope object refs must exactly equal changed determinant refs")
        if self.receipt.output_envelope.content_hash != self.request_envelope.content_hash:
            raise R4SourceError("redrive receipt must identify the exact request envelope")

    @property
    def content_hash(self) -> str:
        return gt0_content_hash(
            {
                "schema": R4_REQUEST_SCHEMA,
                "contract": R4_CONTRACT_ID,
                "occurrence_source_hash": self.occurrence_source_hash,
                "world_response_source_hash": self.world_response_source_hash,
                "changed_determinant_refs": self.changed_determinant_refs,
                "request_envelope_hash": self.request_envelope.content_hash,
                "receipt_hash": self.receipt.content_hash,
            }
        )


@dataclass(frozen=True, slots=True)
class R4WorldResponseRedriveResult:
    occurrence_source: ExternalizedOccurrenceSourceBinding
    world_response_source: ExternalWorldResponseSourceBinding
    invalidation_rederivation_request: R4InvalidationRederivationRequest
    current_response_consequence: CurrentResponseConsequence


def bind_admitted_externalized_occurrence_source(
    candidate: ExternalizedOccurrenceCandidate,
    *,
    expected_actor_ref: GT0ExactRef | Any,
    expected_scope_ref: GT0ExactRef | Any,
    expected_world_context_ref: GT0ExactRef | Any | None = None,
) -> ExternalizedOccurrenceSourceBinding:
    """Conserve one *already admitted* occurrence as a precipitating source."""
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
    if expected_world_context_ref is not None:
        expected_world = _ref(expected_world_context_ref, "expected_world_context_ref", require_hash=True)
        if candidate.world_context_ref != expected_world:
            raise R4BindingMismatchError("externalized occurrence world-context binding mismatch")

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


def bind_admitted_external_world_response_source(
    candidate: ExternalWorldResponseCandidate,
    *,
    expected_scope_ref: GT0ExactRef | Any,
    expected_world_context_ref: GT0ExactRef | Any,
) -> ExternalWorldResponseSourceBinding:
    """Conserve an externally-owned competent objective response; never author one."""
    if not isinstance(candidate, ExternalWorldResponseCandidate):
        raise R4SourceError("candidate must be ExternalWorldResponseCandidate")
    if candidate.state is not WorldResponseAdmissionState.ADMITTED_OBJECTIVE_WORLD_RESPONSE:
        raise R4WorldResponseStateError(
            f"{candidate.state.value} is not an admitted objective world response"
        )
    if candidate.source_kind is not WorldResponseSourceKind.COMPETENT_EXTERNAL_OBJECTIVE_SOURCE:
        raise R4WorldResponseStateError(
            f"{candidate.source_kind.value} cannot author objective world response for R4"
        )

    expected_scope = _ref(expected_scope_ref, "expected_scope_ref")
    expected_world = _ref(expected_world_context_ref, "expected_world_context_ref", require_hash=True)
    if candidate.scope_ref != expected_scope:
        raise R4BindingMismatchError("world response scope binding mismatch")
    if candidate.world_context_ref != expected_world:
        raise R4BindingMismatchError("world response world-context binding mismatch")

    envelope = GT0ConservationEnvelope(
        semantic_owner_ref=candidate.authority_ref,
        object_refs=(candidate.response_ref, *candidate.changed_determinant_refs),
        authority_refs=(candidate.authority_ref, candidate.admission_receipt_ref, candidate.objective_source_permission_ref),
        current_selection_refs=(candidate.effective_time_ref,),
        scope_refs=(candidate.counterpart_ref, candidate.scope_ref, candidate.world_context_ref),
        permission_ceiling=("OBJECTIVE_CHANGED_DETERMINANT_SOURCE", "REDRIVE_REPLAY"),
        dependency_refs=(candidate.admission_receipt_ref, candidate.objective_source_permission_ref),
        provenance_refs=candidate.provenance_refs,
        replay_refs=candidate.replay_refs,
        status=GT0StageStatus.PASS,
        information_loss="NONE__EXTERNAL_WORLD_RESPONSE_AND_DETERMINANTS_REFERENCE_PRESERVED",
    )
    return ExternalWorldResponseSourceBinding(candidate=candidate, envelope=envelope)


def request_r4_invalidation_rederivation(
    occurrence_source: ExternalizedOccurrenceSourceBinding | None,
    world_response_source: ExternalWorldResponseSourceBinding | None,
    *,
    expected_occurrence_source_hash: str,
    expected_world_response_source_hash: str,
    expected_actor_ref: GT0ExactRef | Any,
    expected_scope_ref: GT0ExactRef | Any,
    expected_world_context_ref: GT0ExactRef | Any,
    current_response_consequence_refs: Iterable[GT0ExactRef | Any] = (),
) -> R4WorldResponseRedriveResult:
    """Request ordinary R4 invalidation/rederivation from exact admitted sources."""
    if occurrence_source is None:
        raise R4RedriveError("redrive requires the exact admitted externalized occurrence source")
    if world_response_source is None:
        raise R4RedriveError("redrive requires the exact admitted external objective world-response source")
    if not isinstance(occurrence_source, ExternalizedOccurrenceSourceBinding):
        raise R4RedriveError("occurrence redrive source has the wrong type")
    if not isinstance(world_response_source, ExternalWorldResponseSourceBinding):
        raise R4RedriveError("world-response redrive source has the wrong type")

    occurrence_hash = _sha256(expected_occurrence_source_hash, "expected_occurrence_source_hash")
    world_response_hash = _sha256(expected_world_response_source_hash, "expected_world_response_source_hash")
    if occurrence_source.source_hash != occurrence_hash:
        raise R4RedriveError("externalized occurrence source is stale or hash-mismatched")
    if world_response_source.source_hash != world_response_hash:
        raise R4RedriveError("external world-response source is stale or hash-mismatched")

    expected_world = _ref(expected_world_context_ref, "expected_world_context_ref", require_hash=True)
    occurrence = bind_admitted_externalized_occurrence_source(
        occurrence_source.candidate,
        expected_actor_ref=expected_actor_ref,
        expected_scope_ref=expected_scope_ref,
        expected_world_context_ref=expected_world,
    )
    world_response = bind_admitted_external_world_response_source(
        world_response_source.candidate,
        expected_scope_ref=expected_scope_ref,
        expected_world_context_ref=expected_world,
    )
    if occurrence.source_hash != occurrence_source.source_hash:
        raise R4RedriveError("occurrence source failed deterministic reconstruction")
    if world_response.source_hash != world_response_source.source_hash:
        raise R4RedriveError("world-response source failed deterministic reconstruction")

    oc = occurrence.candidate
    wc = world_response.candidate
    authority_refs = _merge_refs(
        (oc.authority_ref, oc.admission_receipt_ref, oc.causal_use_permission_ref),
        (wc.authority_ref, wc.admission_receipt_ref, wc.objective_source_permission_ref),
    )
    dependency_refs = _merge_refs(
        (oc.occurrence_ref, oc.admission_receipt_ref, oc.causal_use_permission_ref, oc.stream_ref),
        (wc.response_ref, wc.admission_receipt_ref, wc.objective_source_permission_ref),
    )
    provenance_refs = _merge_refs(oc.provenance_refs, wc.provenance_refs)
    replay_refs = _merge_refs(oc.replay_refs, wc.replay_refs)

    request_envelope = GT0ConservationEnvelope(
        semantic_owner_ref=wc.authority_ref,
        object_refs=wc.changed_determinant_refs,
        authority_refs=authority_refs,
        current_selection_refs=(oc.effective_time_ref, wc.effective_time_ref),
        scope_refs=(oc.actor_ref, wc.counterpart_ref, oc.scope_ref, expected_world),
        permission_ceiling=("REQUEST_R4_INVALIDATION_REDERIVATION",),
        dependency_refs=dependency_refs,
        provenance_refs=provenance_refs,
        replay_refs=replay_refs,
        status=GT0StageStatus.PASS,
        information_loss="NONE__EXACT_CHANGED_DETERMINANTS_REQUEST_ONLY__NO_D1_FACT_MINTING",
    )
    receipt = GT0StageReceipt(
        stage_id=R4_REDRIVE_STAGE_ID,
        status=GT0StageStatus.PASS,
        input_envelope_hashes=(occurrence.source_hash, world_response.source_hash),
        output_envelope=request_envelope,
        upstream_refs=(oc.occurrence_ref, wc.response_ref, *dependency_refs),
        authority_refs=authority_refs,
        replay_refs=replay_refs,
        detail_code="EXACT_EXTERNAL_OCCURRENCE_PLUS_OBJECTIVE_WORLD_RESPONSE__REQUEST_R4_INVALIDATION_REDERIVATION",
    )
    request = R4InvalidationRederivationRequest(
        occurrence_source_hash=occurrence.source_hash,
        world_response_source_hash=world_response.source_hash,
        changed_determinant_refs=wc.changed_determinant_refs,
        request_envelope=request_envelope,
        receipt=receipt,
    )
    consequence = CurrentResponseConsequence(
        occurrence_source_hash=occurrence.source_hash,
        world_response_source_hash=world_response.source_hash,
        actor_ref=oc.actor_ref,
        scope_ref=oc.scope_ref,
        consequence_refs=tuple(current_response_consequence_refs),
    )
    return R4WorldResponseRedriveResult(
        occurrence_source=occurrence,
        world_response_source=world_response,
        invalidation_rederivation_request=request,
        current_response_consequence=consequence,
    )


__all__ = [
    "R4_CONTRACT_ID",
    "R4_OCCURRENCE_SOURCE_SCHEMA",
    "R4_WORLD_RESPONSE_SOURCE_SCHEMA",
    "R4_REQUEST_SCHEMA",
    "R4_CURRENT_RESPONSE_SCHEMA",
    "R4_REDRIVE_STAGE_ID",
    "NON_DURABLE_DISPOSITION",
    "OBJECTIVE_CHANGED_DETERMINANT_KIND",
    "R4SourceError",
    "R4OccurrenceStateError",
    "R4WorldResponseStateError",
    "R4BindingMismatchError",
    "R4RedriveError",
    "ExternalizationState",
    "WorldResponseAdmissionState",
    "WorldResponseSourceKind",
    "ExternalizedOccurrenceCandidate",
    "ExternalizedOccurrenceSourceBinding",
    "ExternalWorldResponseCandidate",
    "ExternalWorldResponseSourceBinding",
    "CurrentResponseConsequence",
    "R4InvalidationRederivationRequest",
    "R4WorldResponseRedriveResult",
    "bind_admitted_externalized_occurrence_source",
    "bind_admitted_external_world_response_source",
    "request_r4_invalidation_rederivation",
]
