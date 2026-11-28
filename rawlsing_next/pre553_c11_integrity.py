"""C11 carrier integrity primitives for PRE553 Wave-02 I02.

This module contains only internal carrier/replay records and exact validation
helpers.  It deliberately does not add public semantic object families, execute
queries/discovery, make structural-admission decisions, or infer source
relations.
"""
from __future__ import annotations

from dataclasses import dataclass, fields
from bisect import bisect_right
from functools import cached_property
import hashlib
from types import MappingProxyType
from typing import Any, ClassVar, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_authority import (
    AuthorityRegistry,
    Pre553AuthorityError,
    require_positive_authority,
    validate_object_authority_closure,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    CanonicalSemanticObject,
    EmpiricalCoordinateFact,
    EmpiricalUniverse,
    ExactRef,
    INTERNAL_C11_RECORD_FAMILIES,
    PUBLIC_OBJECT_FAMILIES, URN_PREFIX,
    Pre553IntegrityError,
    Pre553SemanticCollapseError,
    RespondentEvent,
    RoutingEligibilityFact,
    SourceUniverseRelation,
    WeightMeasureFact,
    authority_ref,
    canonical_json,
    canonicalize,
    exact_ref,
    semantic_hash,
)

M01_M18 = tuple(f"M{i:02d}" for i in range(1, 19))

TYPED_ABSENCE_STATES = frozenset({
    "UNKNOWN", "MISSING", "DK", "REFUSAL", "IAP", "NOT_ASKED",
    "NOT_APPLICABLE", "INVALID_UNRESOLVED", "NOT_AUTHORIZED",
    "NONCOMPARABLE", "DEFERRED", "VALID_EMPTY", "INTEGRITY_FAILURE",
    "DISTINCT_BY_DEFAULT",
})

MULTIPLICITY_TOPOLOGIES = frozenset({
    "UNORDERED_MULTISELECT_SET", "MULTISELECT", "REPEATED_EVENT",
    "REPEATED_MEASUREMENT", "ORDERED_SEQUENCE", "RANKED_RESPONSE",
    "COMPONENTIZED_RESPONSE",
})
ORDER_SENSITIVE_TOPOLOGIES = frozenset({
    "ORDERED_SEQUENCE", "RANKED_RESPONSE",
})


class C11IntegrityError(Pre553IntegrityError):
    """The proposed C11 carrier package is not exact and closed."""


class C11AtomicityError(C11IntegrityError):
    """A caller attempted to treat an unsealed/partial carrier as authoritative."""


@dataclass(frozen=True)
class TypedAbsence:
    """Explicit semantic absence; a missing Python key/value is never equivalent."""

    state: str
    detail: str | None = None

    def __post_init__(self) -> None:
        if self.state not in TYPED_ABSENCE_STATES:
            raise C11IntegrityError(f"unknown typed absence state {self.state!r}")
        if self.detail is not None and (not isinstance(self.detail, str) or not self.detail.strip()):
            raise C11IntegrityError("typed absence detail must be a non-empty string when supplied")

    def as_dict(self) -> dict[str, Any]:
        return {"typed_absence_state": self.state, "detail": self.detail}


def _internal_value(value: Any) -> Any:
    if isinstance(value, TypedAbsence):
        return value.as_dict()
    if isinstance(value, C11InternalRecord):
        return value.ref.as_dict()
    if isinstance(value, Mapping):
        if any(not isinstance(k, str) for k in value):
            raise C11IntegrityError("internal carrier mapping keys must be strings")
        return {k: _internal_value(value[k]) for k in sorted(value)}
    if isinstance(value, (set, frozenset)):
        normalized = [_internal_value(v) for v in value]
        return sorted(normalized, key=canonical_json)
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_internal_value(v) for v in value]
    return canonicalize(value)


def _require_sha256(value: Any, name: str) -> str:
    if (not isinstance(value, str) or len(value) != 64 or value.lower() != value
            or any(ch not in "0123456789abcdef" for ch in value)):
        raise C11IntegrityError(f"{name} must be a lowercase sha256")
    return value


def _require_text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise C11IntegrityError(f"{name} must be a non-empty string")
    return value.strip()


def _require_exact_ref(value: Any, name: str) -> ExactRef:
    try:
        return exact_ref(value, name)
    except Pre553IntegrityError as exc:
        raise C11IntegrityError(str(exc)) from exc


def _require_authority_ref(value: Any, name: str) -> AuthorityRef:
    try:
        return authority_ref(value, name)
    except Pre553IntegrityError as exc:
        raise C11IntegrityError(str(exc)) from exc


class C11InternalRecord:
    """Internal C11 record: deterministic, immutable, and never public ontology."""

    RECORD_FAMILY: ClassVar[str] = ""

    def __post_init__(self) -> None:
        if self.RECORD_FAMILY not in INTERNAL_C11_RECORD_FAMILIES:
            raise Pre553SemanticCollapseError(
                f"{self.RECORD_FAMILY!r} is not an HQ-approved internal C11 family")
        self._validate()

    def _validate(self) -> None:
        pass

    def semantic_projection(self) -> dict[str, Any]:
        material: dict[str, Any] = {}
        for f in fields(self):
            material[f.name] = _internal_value(getattr(self, f.name))
        return {
            "record_family": self.RECORD_FAMILY,
            "record_version": "1.0.0",
            "semantic_fields": material,
        }

    @cached_property
    def content_hash(self) -> str:
        # Internal records are frozen dataclasses.  Their deterministic identity
        # is therefore immutable and may be memoized without changing bytes or
        # semantic projection.
        return semantic_hash(self.semantic_projection())

    @cached_property
    def object_id(self) -> str:
        return f"urn:rawlsing:pre553:c11:{self.RECORD_FAMILY}:sha256:{self.content_hash}"

    @cached_property
    def ref(self) -> ExactRef:
        return ExactRef(f"C11Internal:{self.RECORD_FAMILY}", self.object_id, self.content_hash)

    def as_dict(self) -> dict[str, Any]:
        return {
            **self.semantic_projection(),
            "object_id": self.object_id,
            "content_hash": self.content_hash,
        }


@dataclass(frozen=True)
class RespondentIdentity(C11InternalRecord):
    RECORD_FAMILY: ClassVar[str] = "RespondentIdentity"
    empirical_universe_ref: ExactRef
    respondent_key: str
    source_native_respondent_key_ref_or_typed_absence: ExactRef | TypedAbsence
    identity_map_authority_ref_or_typed_absence: AuthorityRef | TypedAbsence

    def _validate(self) -> None:
        _require_exact_ref(self.empirical_universe_ref, "empirical_universe_ref")
        _require_text(self.respondent_key, "respondent_key")
        if isinstance(self.source_native_respondent_key_ref_or_typed_absence, ExactRef):
            _require_exact_ref(self.source_native_respondent_key_ref_or_typed_absence,
                               "source_native_respondent_key_ref_or_typed_absence")
        elif not isinstance(self.source_native_respondent_key_ref_or_typed_absence, TypedAbsence):
            raise C11IntegrityError("respondent native key must be ExactRef or TypedAbsence")
        if isinstance(self.identity_map_authority_ref_or_typed_absence, AuthorityRef):
            _require_authority_ref(self.identity_map_authority_ref_or_typed_absence,
                                   "identity_map_authority_ref_or_typed_absence")
        elif not isinstance(self.identity_map_authority_ref_or_typed_absence, TypedAbsence):
            raise C11IntegrityError("identity map authority must be AuthorityRef or TypedAbsence")


@dataclass(frozen=True)
class QuestionVariableBinding(C11InternalRecord):
    RECORD_FAMILY: ClassVar[str] = "QuestionVariableBinding"
    empirical_universe_ref: ExactRef
    native_question_ref: ExactRef
    instrument_question_version: str
    canonical_question_ref_or_typed_absence: ExactRef | TypedAbsence
    component_subitem_ref_or_typed_absence: ExactRef | TypedAbsence
    semantic_authority_ref: AuthorityRef
    topology_authority_ref: AuthorityRef

    def _validate(self) -> None:
        _require_exact_ref(self.empirical_universe_ref, "empirical_universe_ref")
        _require_exact_ref(self.native_question_ref, "native_question_ref")
        _require_text(self.instrument_question_version, "instrument_question_version")
        if not isinstance(self.canonical_question_ref_or_typed_absence, (ExactRef, TypedAbsence)):
            raise C11IntegrityError("canonical question must be ExactRef or TypedAbsence")
        if not isinstance(self.component_subitem_ref_or_typed_absence, (ExactRef, TypedAbsence)):
            raise C11IntegrityError("component/subitem must be ExactRef or TypedAbsence")
        _require_authority_ref(self.semantic_authority_ref, "semantic_authority_ref")
        _require_authority_ref(self.topology_authority_ref, "topology_authority_ref")


@dataclass(frozen=True)
class EmpiricalPredicateReplayBinding(C11InternalRecord):
    RECORD_FAMILY: ClassVar[str] = "EmpiricalPredicateReplayBinding"
    predicate_grammar_authority_ref: AuthorityRef
    typed_predicate_ast_ref: ExactRef
    predicate_hash: str
    coordinate_question_value_refs: tuple[ExactRef, ...]
    risk_set_ref: ExactRef
    target_ref: ExactRef
    scope_ref: ExactRef
    measure_basis_ref: ExactRef

    def _validate(self) -> None:
        _require_authority_ref(self.predicate_grammar_authority_ref, "predicate_grammar_authority_ref")
        for name in ("typed_predicate_ast_ref", "risk_set_ref", "target_ref", "scope_ref", "measure_basis_ref"):
            _require_exact_ref(getattr(self, name), name)
        _require_sha256(self.predicate_hash, "predicate_hash")
        for ref in self.coordinate_question_value_refs:
            _require_exact_ref(ref, "coordinate_question_value_refs")


@dataclass(frozen=True)
class ComparatorReplayBinding(C11InternalRecord):
    RECORD_FAMILY: ClassVar[str] = "ComparatorReplayBinding"
    state: str
    actor_fact_ref_or_typed_absence: ExactRef | TypedAbsence
    actor_fact_effective_time_or_typed_absence: str | TypedAbsence
    comparator_rule_ref_or_typed_absence: AuthorityRef | TypedAbsence
    resolved_empirical_predicate_ref_or_typed_absence: ExactRef | TypedAbsence
    cardinality_ambiguity_state: str
    source_scope_refs: tuple[ExactRef, ...]

    def _validate(self) -> None:
        if self.state not in {"PRESENT", "DEFERRED"}:
            raise C11IntegrityError("ComparatorReplayBinding state must be PRESENT or DEFERRED")
        _require_text(self.cardinality_ambiguity_state, "cardinality_ambiguity_state")
        for ref in self.source_scope_refs:
            _require_exact_ref(ref, "source_scope_refs")


@dataclass(frozen=True)
class DiscoveryBranchReplayBinding(C11InternalRecord):
    RECORD_FAMILY: ClassVar[str] = "DiscoveryBranchReplayBinding"
    state: str
    search_family_id_or_typed_absence: str | TypedAbsence
    candidate_universe_ref_or_typed_absence: ExactRef | TypedAbsence
    grammar_authority_ref_or_typed_absence: AuthorityRef | TypedAbsence
    source_risk_topology_measure_scope_ref_or_typed_absence: ExactRef | TypedAbsence
    algorithm_identity_ref_or_typed_absence: ExactRef | TypedAbsence
    coverage_pruning_contract_ref_or_typed_absence: ExactRef | TypedAbsence
    deterministic_parameters_ref_or_typed_absence: ExactRef | TypedAbsence
    rng_state_ref_or_typed_absence: ExactRef | TypedAbsence
    parent_branch_ref_or_typed_absence: ExactRef | TypedAbsence
    winning_predicate_ref_or_typed_absence: ExactRef | TypedAbsence
    pruned_trace_ref_or_typed_absence: ExactRef | TypedAbsence

    def _validate(self) -> None:
        if self.state not in {"PRESENT", "DEFERRED"}:
            raise C11IntegrityError("DiscoveryBranchReplayBinding state must be PRESENT or DEFERRED")


@dataclass(frozen=True)
class StructuralAdmissionReplayBinding(C11InternalRecord):
    RECORD_FAMILY: ClassVar[str] = "StructuralAdmissionReplayBinding"
    state: str
    empirical_query_or_fact_ref_or_typed_absence: ExactRef | TypedAbsence
    predicate_risk_target_scope_measure_ref_or_typed_absence: ExactRef | TypedAbsence
    source_empirical_provenance_ref_or_typed_absence: ExactRef | TypedAbsence
    structural_admission_authority_ref_or_typed_absence: AuthorityRef | TypedAbsence
    target_structural_producer_use_ref_or_typed_absence: ExactRef | TypedAbsence
    negative_limit_authority_refs: tuple[AuthorityRef, ...]
    transformation_replay_ref_or_typed_absence: ExactRef | TypedAbsence

    def _validate(self) -> None:
        if self.state not in {"PRESENT", "NOT_APPLICABLE"}:
            raise C11IntegrityError(
                "StructuralAdmissionReplayBinding state must be PRESENT or NOT_APPLICABLE")
        for ref in self.negative_limit_authority_refs:
            _require_authority_ref(ref, "negative_limit_authority_refs")


@dataclass(frozen=True, slots=True, eq=False)
class _PackedClosureRefs(Sequence[ExactRef]):
    """Private country I02 replay census at exact reference grain.

    Contiguous derivable IDs share kind and ID prefix; only 32 digest bytes
    per identity remain. Non-derivable refs retain all three exact strings.
    No deduplication, reordering, or reference inversion. Immutable bytes
    and detached strings, never a caller-owned ExactRef instance.
    """
    runs: tuple
    ends: tuple[int, ...]

    @staticmethod
    def _derived_prefix(kind):
        if kind in PUBLIC_OBJECT_FAMILIES:
            return f"{URN_PREFIX}:{kind.split('@',1)[0]}:sha256:"
        if kind.startswith("C11Internal:") and kind.split(":",1)[1] in INTERNAL_C11_RECORD_FAMILIES:
            return f"{URN_PREFIX}:c11:{kind.split(':',1)[1]}:sha256:"
        return None

    def __post_init__(self):
        self.validate()

    def validate(self):
        # Validate the exact physical representation without inflating the
        # per-identity ref objects. Every 32-byte digest yields one legal
        # lowercase SHA256 and its deterministic ID, with no omitted state.
        if type(self.runs) is not tuple or type(self.ends) is not tuple or len(self.runs)!=len(self.ends):
            raise C11IntegrityError("packed replay run/offset shape drift")
        count=0
        for run,end in zip(self.runs,self.ends):
            if type(run) is not tuple or len(run)!=3 or type(end) is not int:
                raise C11IntegrityError("packed replay run shape drift")
            kind,prefix,payload=run
            if type(kind) is not str or type(prefix) is not str:
                raise C11IntegrityError("packed replay ref string drift")
            if type(payload) is bytes:
                if prefix!=self._derived_prefix(kind) or not payload or len(payload)%32:
                    raise C11IntegrityError("packed replay derived lane drift")
                count+=len(payload)//32
            elif type(payload) is str:
                ref=ExactRef(kind,prefix,payload)
                if (ref.kind,ref.object_id,ref.content_hash)!=run:
                    raise C11IntegrityError("packed replay explicit reference drift")
                count+=1
            else:
                raise C11IntegrityError("packed replay payload type drift")
            if end!=count:
                raise C11IntegrityError("packed replay run offset drift")

    @classmethod
    def pack(cls, refs):
        runs,ends=[],[]
        active=None
        lane=bytearray()
        count=0
        def flush():
            if active is not None:
                runs.append((*active,bytes(lane)))
                ends.append(count)
                lane.clear()
        for ref in refs:
            if type(ref) is not ExactRef:
                raise C11IntegrityError("packed replay requires exact canonical refs")
            kind,oid,digest=ref.kind,ref.object_id,ref.content_hash
            # Only canonical deterministic IDs are reducible. An arbitrary
            # string ending in a hash is not a license to infer its ID.
            if any(type(v) is not str for v in (kind,oid,digest)):
                raise C11IntegrityError("packed replay requires exact string leaves")
            prefix=cls._derived_prefix(kind)
            if prefix is not None and oid==prefix+digest:
                binary=bytes.fromhex(digest)
                if len(binary)!=32 or binary.hex()!=digest:
                    raise C11IntegrityError("packed replay digest is not exact lowercase SHA256")
                key=(kind,prefix)
                if active!=key:
                    flush()
                    active=key
                lane.extend(binary)
                count+=1
            else:
                flush()
                active=None
                count+=1
                runs.append((kind,oid,digest))
                ends.append(count)
        flush()
        return cls(tuple(runs),tuple(ends))

    def __len__(self):
        return self.ends[-1] if self.ends else 0

    @staticmethod
    def _ref(run, offset):
        kind,prefix,payload=run
        if type(payload) is str:
            return ExactRef(kind,prefix,payload)
        h=payload[32*offset:32*(offset+1)].hex()
        return ExactRef(kind,prefix+h,h)

    def __iter__(self):
        for run in self.runs:
            payload=run[2]
            for i in range(1 if type(payload) is str else len(payload)//32):
                yield self._ref(run,i)

    def __getitem__(self,index):
        if isinstance(index,slice):
            return tuple(self[i] for i in range(*index.indices(len(self))))
        if index<0:
            index+=len(self)
        if not 0<=index<len(self):
            raise IndexError(index)
        run=bisect_right(self.ends,index)
        return self._ref(self.runs[run],index-(self.ends[run-1] if run else 0))

    def __eq__(self,other):
        if type(other) is _PackedClosureRefs:
            return self.runs==other.runs and self.ends==other.ends
        if type(other) is tuple:
            return len(self)==len(other) and all(a==b for a,b in zip(self,other))
        return NotImplemented

    def __hash__(self):
        return hash(tuple(self))

    @property
    def digest_bytes(self):
        return sum(len(r[2]) for r in self.runs if type(r[2]) is bytes)

    def digest_lane(self,kind,prefix):
        matches=[r[2] for r in self.runs if r[:2]==(kind,prefix) and type(r[2]) is bytes]
        return matches[0] if len(matches)==1 else None

    def canonical_ref_bytes(self):
        """Emit byte-identical canonical ref JSON without constructing refs."""
        for kind,prefix,payload in self.runs:
            if type(payload) is str:
                yield canonical_json(ExactRef(kind,prefix,payload).as_dict()).encode("utf-8")
                continue
            middle=b'","kind":'+canonical_json(kind).encode("utf-8")+b',"object_id":'+canonical_json(prefix).encode("utf-8")[:-1]
            for offset in range(0,len(payload),32):
                h=payload[offset:offset+32].hex().encode("ascii")
                yield b'{"content_hash":"'+h+middle+h+b'"}'


@dataclass(frozen=True)
class ReplayManifest(C11InternalRecord):
    RECORD_FAMILY: ClassVar[str] = "ReplayManifest"
    frontier_version: str
    authority_snapshot_set_hash: str
    source_substrate_content_refs: tuple[ExactRef, ...]
    semantic_projection_id: str
    semantic_projection_hash: str
    deterministic_tie_order_rules_ref: ExactRef
    replay_protocol_version: str
    replay_protocol_authority_ref: AuthorityRef
    closure_refs: Sequence[ExactRef]

    @cached_property
    def content_hash(self) -> str:
        # Same canonical internal record preimage; the potentially millions
        # of closure refs are emitted one at a time instead of expanded into
        # a simultaneous graph of dictionaries and one giant JSON string.
        if type(self.closure_refs) not in (tuple,_PackedClosureRefs):
            return semantic_hash(self.semantic_projection())
        h=hashlib.sha256()
        def emit(value):
            h.update(canonical_json(value).encode("utf-8"))
        h.update(b'{"record_family":')
        emit(self.RECORD_FAMILY)
        h.update(b',"record_version":"1.0.0","semantic_fields":{')
        for i,f in enumerate(sorted(fields(self),key=lambda f:f.name)):
            if i:
                h.update(b",")
            emit(f.name)
            h.update(b":")
            value=getattr(self,f.name)
            if f.name=="closure_refs":
                h.update(b"[")
                if type(value) is _PackedClosureRefs:
                    for j,encoded in enumerate(value.canonical_ref_bytes()):
                        if j:
                            h.update(b",")
                        h.update(encoded)
                else:
                    for j,ref in enumerate(value):
                        if j:
                            h.update(b",")
                        emit(_internal_value(ref))
                h.update(b"]")
            else:
                emit(_internal_value(value))
        h.update(b"}}")
        return h.hexdigest()

    def _validate(self) -> None:
        _require_text(self.frontier_version, "frontier_version")
        _require_text(self.semantic_projection_id, "semantic_projection_id")
        _require_text(self.replay_protocol_version, "replay_protocol_version")
        for name in ("authority_snapshot_set_hash", "semantic_projection_hash"):
            _require_sha256(getattr(self, name), name)
        _require_exact_ref(self.deterministic_tie_order_rules_ref,
                           "deterministic_tie_order_rules_ref")
        _require_authority_ref(self.replay_protocol_authority_ref,
                               "replay_protocol_authority_ref")
        for ref in self.source_substrate_content_refs:
            _require_exact_ref(ref, "source_substrate_content_refs")
        if type(self.closure_refs) is _PackedClosureRefs:
            self.closure_refs.validate()
        else:
            for ref in self.closure_refs:
                _require_exact_ref(ref, "closure_refs")


def assert_internal_carrier_record(record: Any) -> C11InternalRecord:
    if isinstance(record, CanonicalSemanticObject):
        raise Pre553SemanticCollapseError("public semantic object cannot masquerade as internal C11 record")
    if not isinstance(record, C11InternalRecord):
        raise C11IntegrityError("expected an internal C11 carrier record")
    if record.RECORD_FAMILY not in INTERNAL_C11_RECORD_FAMILIES:
        raise Pre553SemanticCollapseError("unapproved internal carrier family")
    return record


def verify_public_object_integrity(obj: CanonicalSemanticObject) -> CanonicalSemanticObject:
    if not isinstance(obj, CanonicalSemanticObject):
        raise C11IntegrityError("expected an I01 canonical public object")
    expected = semantic_hash(obj.semantic_projection())
    if expected != obj.content_hash:
        raise C11IntegrityError("public object semantic projection/hash mismatch")
    if obj.ref.object_id != obj.object_id or obj.ref.content_hash != obj.content_hash:
        raise C11IntegrityError("public object ExactRef does not match object identity")
    return obj


def _field_ref(obj: CanonicalSemanticObject, name: str, *, allow_none: bool = False) -> ExactRef | None:
    value = getattr(obj, name)
    if value is None and allow_none:
        return None
    return _require_exact_ref(value, name)


def _field_authority_ref(
    obj: CanonicalSemanticObject, name: str, *, allow_none: bool = False
) -> AuthorityRef | None:
    value = getattr(obj, name)
    if value is None and allow_none:
        return None
    return _require_authority_ref(value, name)


def validate_public_carrier_object(
    obj: CanonicalSemanticObject,
    registry: AuthorityRegistry,
) -> CanonicalSemanticObject:
    """Validate exact identity, authority closure and I02 carrier-specific noncollapse."""
    verify_public_object_integrity(obj)
    return _validate_public_carrier_fields(obj,registry)


def _validate_public_carrier_fields(obj,registry):
    """Shared field/authority checks after exact identity validation.

    Ordinary public ingress always verifies the full semantic identity.
    Private packed routing materialization may use the constructor's
    immediately preceding exact supplied hash/ID check instead.
    """
    if isinstance(obj, AuthoritySnapshot):
        return obj
    try:
        validate_object_authority_closure(obj, registry)
    except Pre553AuthorityError as exc:
        raise C11IntegrityError(str(exc)) from exc

    if isinstance(obj, EmpiricalUniverse):
        if not obj.respondent_namespace:
            raise C11IntegrityError("EmpiricalUniverse respondent namespace is mandatory")

    elif isinstance(obj, RespondentEvent):
        _field_ref(obj, "empirical_universe_ref")
        _field_ref(obj, "scoped_respondent_ref")
        _field_ref(obj, "native_question_ref")
        _field_ref(obj, "response_topology_ref")
        mapping_ref = _field_authority_ref(obj, "value_transform_authority_ref", allow_none=True)
        has_canonical = (
            obj.canonical_question_ref_if_authorized is not None
            or obj.canonical_response_value_if_authorized is not None
        )
        if has_canonical and mapping_ref is None:
            raise C11IntegrityError("canonical response/question material lacks exact mapping authority")
        if has_canonical and mapping_ref is not None:
            try:
                snapshot = registry.resolve_exact(mapping_ref).snapshot
                require_positive_authority(
                    snapshot, authority_kind="NATIVE_CANONICAL_MAPPING_HARMONIZATION")
            except Pre553AuthorityError as exc:
                raise C11IntegrityError(
                    "canonical response/question material lacks exact positive mapping authority") from exc
        topology = obj.multiplicity_order_rank_fields
        if not isinstance(topology, Mapping):
            raise C11IntegrityError("multiplicity/order/rank fields must be an exact mapping")
        kind = topology.get("kind") or topology.get("topology_kind")
        if not isinstance(kind, str) or not kind:
            raise C11IntegrityError("response topology kind must be explicit")
        if kind in ORDER_SENSITIVE_TOPOLOGIES:
            if not any(k in topology for k in ("semantic_ordinal", "rank", "order", "index")):
                raise C11IntegrityError("ordered/ranked response lacks explicit semantic order/rank")
        if kind in MULTIPLICITY_TOPOLOGIES and not obj.response_event_id_or_deterministic_index:
            raise C11IntegrityError("multiplicity-bearing response lacks occurrence identity")

    elif isinstance(obj, EmpiricalCoordinateFact):
        _field_ref(obj, "empirical_universe_ref")
        _field_ref(obj, "scoped_respondent_ref")
        _field_ref(obj, "native_coordinate_ref")
        has_canonical = (
            obj.canonical_coordinate_ref_if_authorized is not None
            or obj.canonical_coordinate_value_if_authorized is not None
        )
        crosswalk = _field_authority_ref(
            obj, "normalization_crosswalk_authority_ref", allow_none=True)
        if has_canonical and crosswalk is None:
            raise C11IntegrityError("canonical empirical coordinate lacks exact crosswalk authority")
        if has_canonical and crosswalk is not None:
            try:
                snapshot = registry.resolve_exact(crosswalk).snapshot
                require_positive_authority(
                    snapshot, authority_kind="NATIVE_CANONICAL_MAPPING_HARMONIZATION")
            except Pre553AuthorityError as exc:
                raise C11IntegrityError(
                    "canonical empirical coordinate lacks exact positive crosswalk authority") from exc

    elif isinstance(obj, RoutingEligibilityFact):
        _field_ref(obj, "empirical_universe_ref")
        _field_ref(obj, "scoped_respondent_ref")
        _field_ref(obj, "risk_set_ref")
        _field_ref(obj, "routing_rule_ref")
        _field_ref(obj, "member_set_replay_ref")

    elif isinstance(obj, WeightMeasureFact):
        _field_ref(obj, "empirical_universe_ref")
        _field_ref(obj, "scoped_respondent_ref")
        design = _field_authority_ref(obj, "design_authority_ref")
        estimand = _field_authority_ref(obj, "estimand_authority_ref")
        try:
            registry.resolve_exact(design)
            registry.resolve_exact(estimand)
        except Pre553AuthorityError as exc:
            raise C11IntegrityError("weight design/estimand authority unavailable") from exc
        if obj.typed_state == "WEIGHT_VALID_AUTHORIZED" and obj.exact_weight_value_representation is None:
            raise C11IntegrityError("authorized weight requires exact source/governed value")

    elif isinstance(obj, SourceUniverseRelation):
        for ref in obj.source_universe_refs:
            _require_exact_ref(ref, "source_universe_refs")

    return obj


def authority_snapshot_set_hash(snapshots: Iterable[AuthoritySnapshot]) -> str:
    material = sorted(
        (snapshot.authority_ref.as_dict() for snapshot in snapshots),
        key=canonical_json,
    )
    return semantic_hash(material)


def canonical_section_refs(records: Iterable[Any]) -> tuple[ExactRef, ...]:
    refs: list[ExactRef] = []
    for record in records:
        if isinstance(record, CanonicalSemanticObject):
            refs.append(record.ref)
        elif isinstance(record, C11InternalRecord):
            refs.append(record.ref)
        else:
            raise C11IntegrityError("carrier section contains unsupported record type")
    return tuple(sorted(refs, key=lambda ref: ref.key))


def _country_occurrence_ids_distinct(events,*,omitted_group_plane=False):
    """Sufficient exact proof for deterministic private country headers.

    Distinct canonical occurrence identifiers imply distinct full occurrence
    keys. A repeated identifier is NOT proof of a duplicate: the group,
    respondent, universe, question or component could differ. Return to the
    complete incumbent test on repeated, foreign or malformed identities.
    """
    from rawlsing_next._pre553_c11_execution_view import _CountryEventHeader
    if type(events) is not tuple:
        return False
    seen=set()
    for event in events:
        if type(event) is not _CountryEventHeader:
            return False
        value=event.occurrence_identity
        valid_group=(event.group_identity is None if omitted_group_plane else
                     type(event.group_identity) is bytes and len(event.group_identity)==32)
        if (type(value) is not bytes or len(value)!=32 or value in seen or not valid_group):
            return False
        # Validate the optional exact component just as the complete
        # occurrence preimage would. No shortcut for foreign identity forms.
        event.component_or_subitem_ref
        _field_ref(event,"empirical_universe_ref")
        _field_ref(event,"scoped_respondent_ref")
        _field_ref(event,"native_question_ref")
        seen.add(value)
    return True


def _validate_restored_country_occurrences(events,*,allow_deferred=False):
    """Only the authenticated private preparation path may omit group bytes.

    Global distinct occurrence IDs are a sufficient proof independently of
    group values. Mixed, malformed or repeated IDs in the omitted format
    must fail, never fall back to incomplete occurrence preimages.
    """
    from rawlsing_next._pre553_c11_execution_view import _CountryEventHeader
    if not all(type(event) is _CountryEventHeader for event in events):
        raise C11IntegrityError("restored private country headers required")
    if allow_deferred and all(e.occurrence_identity is None and e.group_identity is None for e in events):
        # This validates transport geometry, NOT a new proof of occurrence
        # distinctness. The authenticated private producer pin carries the
        # previously executed proof. Event digests commit the complete event;
        # exact body access reconstructs the original occurrence identity.
        prior=b""
        for event in events:
            digest=event.event_identity
            coords=event.source_coordinates
            if (type(digest) is not bytes or len(digest)!=32 or digest<=prior
                    or type(coords) is not tuple or len(coords)!=3
                    or any(type(x) is not int or not 0<=x<2**32 for x in coords)):
                raise C11IntegrityError("deferred occurrence transport identity or geometry drift")
            event.component_or_subitem_ref
            _field_ref(event,"empirical_universe_ref")
            _field_ref(event,"scoped_respondent_ref")
            _field_ref(event,"native_question_ref")
            prior=digest
        return
    if not _country_occurrence_ids_distinct(events,omitted_group_plane=True):
        raise C11IntegrityError("omitted group plane lacks globally distinct exact occurrence identities")


def ensure_distinct_event_occurrences(events: Iterable[RespondentEvent]) -> None:
    if _country_occurrence_ids_distinct(events):
        return
    # A digest collision can only conservatively refuse a package, never
    # collapse two occurrences or admit a duplicate. Avoid retaining an
    # expanded canonical occurrence JSON string for every source cell.
    seen: set[bytes] = set()
    for event in events:
        universe = _field_ref(event, "empirical_universe_ref")
        respondent = _field_ref(event, "scoped_respondent_ref")
        native_question = _field_ref(event, "native_question_ref")
        component = event.component_or_subitem_ref
        occurrence_material = {
            "universe": universe.as_dict(),
            "respondent": respondent.as_dict(),
            "native_question": native_question.as_dict(),
            "component": component,
            "event_group_id": event.event_group_id,
            "event_id": event.response_event_id_or_deterministic_index,
        }
        key=hashlib.sha256(canonical_json(occurrence_material).encode("utf-8")).digest()
        if key in seen:
            raise C11IntegrityError(
                "duplicate response occurrence identity detected; storage duplication is not a new event")
        seen.add(key)


def make_m01_m18_coverage(
    *,
    universes: Sequence[EmpiricalUniverse],
    respondents: Sequence[RespondentIdentity],
    questions: Sequence[QuestionVariableBinding],
    events: Sequence[RespondentEvent],
    routing: Sequence[RoutingEligibilityFact],
    coordinates: Sequence[EmpiricalCoordinateFact],
    weight_section_explicit: bool,
    authority_snapshots: Sequence[AuthoritySnapshot],
    source_relation_section_explicit: bool,
    predicate_replay_section_explicit: bool,
    comparator_section_explicit: bool,
    discovery_section_explicit: bool,
    structural_admission_section_explicit: bool,
    replay_manifest: ReplayManifest | None,
) -> Mapping[str, tuple[str, ...]]:
    coverage: dict[str, tuple[str, ...]] = {
        "M01": ("EmpiricalUniverse",) if universes else (),
        "M02": ("RespondentIdentity",) if respondents else (),
        "M03": ("QuestionVariableBinding",) if questions else (),
        "M04": ("RespondentEvent",) if events else (),
        "M05": ("QuestionVariableBinding", "RespondentEvent") if questions and events else (),
        "M06": ("RespondentEvent.typed_state",) if events else (),
        "M07": ("RoutingEligibilityFact",) if routing else (),
        "M08": ("EmpiricalCoordinateFact",) if coordinates else (),
        "M09": ("WeightMeasureFact|TypedAbsence",) if weight_section_explicit else (),
        "M10": ("AuthoritySnapshot",) if authority_snapshots else (),
        "M11": ("SourceUniverseRelation|DISTINCT_BY_DEFAULT",) if source_relation_section_explicit else (),
        "M12": ("RoutingEligibilityFact", "EmpiricalPredicateReplayBinding|TypedAbsence")
        if routing and predicate_replay_section_explicit else (),
        "M13": ("ComparatorReplayBinding|DEFERRED",) if comparator_section_explicit else (),
        "M14": ("DiscoveryBranchReplayBinding|DEFERRED",) if discovery_section_explicit else (),
        "M15": ("StructuralAdmissionReplayBinding|NOT_APPLICABLE",)
        if structural_admission_section_explicit else (),
        "M16": ("ReplayManifest",) if replay_manifest is not None else (),
        "M17": ("AuthoritySnapshot", "ReplayManifest")
        if authority_snapshots and replay_manifest is not None else (),
        "M18": ("ReplayManifest",) if replay_manifest is not None else (),
    }
    missing = [atom for atom in M01_M18 if not coverage[atom]]
    if missing:
        raise C11IntegrityError(f"C11 package does not close M01-M18: missing {missing!r}")
    return MappingProxyType(coverage)


__all__ = [
    "M01_M18", "TYPED_ABSENCE_STATES", "C11IntegrityError", "C11AtomicityError",
    "TypedAbsence", "C11InternalRecord", "RespondentIdentity", "QuestionVariableBinding",
    "EmpiricalPredicateReplayBinding", "ComparatorReplayBinding",
    "DiscoveryBranchReplayBinding", "StructuralAdmissionReplayBinding", "ReplayManifest",
    "assert_internal_carrier_record", "verify_public_object_integrity",
    "validate_public_carrier_object", "authority_snapshot_set_hash",
    "canonical_section_refs", "ensure_distinct_event_occurrences", "make_m01_m18_coverage",
]
