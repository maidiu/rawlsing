"""Explicit governed physical/native -> validated C11 -> frozen I03 facade.

Physical carriers remain nonsemantic. Every semantic projection decision is an
exact caller-owned input; the module never reads labels/frequencies to infer
meaning and never bypasses C11 validation.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
import hashlib
import math
from typing import Any, Callable, Iterable, Mapping

from rawlsing_next._pre553_c11_execution_view import _compact_public_objects
from rawlsing_next.pre553_c11_ingest import (
    INGEST_CONTRACT_VERSION, C11SourceReleaseCandidate, SourceReleaseManifest,
    build_candidate_replay_manifest, validate_c11_source_release,
)
from rawlsing_next.pre553_c11_integrity import (
    C11InternalRecord, QuestionVariableBinding, RespondentIdentity, TypedAbsence,
)
from rawlsing_next.pre553_c11_repository import C11LogicalRelease, C11Repository
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef, AuthoritySnapshot, EmpiricalCoordinateFact, EmpiricalPredicate,
    EmpiricalQuerySpec, EmpiricalUniverse, ExactRef, RespondentEvent,
    RoutingEligibilityFact, SourceUniverseRelation, WeightMeasureFact,
    authority_ref, canonicalize, exact_ref, semantic_hash,
)
from rawlsing_next._pre553_query_common import QueryExecutionResult
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_physical_c11_bridge import (
    PhysicalSourceAuthorityProjection, build_validated_c11_release,
)
from rawlsing_next.pre553_physical_decoder import (
    DecoderError, PhysicalCell, PhysicalMissingState, PhysicalSourceIncidence,
)
from rawlsing_next.pre553_r5_codec import (
    CODEC_VERSION as R5_CODEC_VERSION,
    R5TypedValueCodec,
    canonical_bytes as r5_canonical_bytes,
)

CONTRACT_ID = "PRE553_SOURCE_BACKED_C11_FACADE@1.0.0"
SLOT_OWNER_SET_CONTRACT_ID = "PRE553_C11_PHYSICAL_SLOT_OWNER_SET@1.0.0"
RESPONSE_OWNER_FAMILY = "RespondentEvent@1.0.0"
COORDINATE_OWNER_FAMILY = "EmpiricalCoordinateFact@1.0.0"
WEIGHT_OWNER_FAMILY = "WeightMeasureFact@1.0.0"
_SUPPORTED_OWNER_FAMILIES = frozenset((RESPONSE_OWNER_FAMILY, COORDINATE_OWNER_FAMILY, WEIGHT_OWNER_FAMILY))

PHYSICAL_VALUE_MATERIAL_SCHEMA = "PRE553_EXACT_PHYSICAL_VALUE_MATERIAL@1.0.0"
PHYSICAL_BINDING_SCHEMA = "PRE553_PHYSICAL_VALUE_BINDING@2.0.0"
RAW_WITNESS_SCHEMA = "PRE553_RAW_PHYSICAL_VALUE_WITNESS@1.0.0"
_PHYSICAL_CODEC = R5TypedValueCodec()


class SourceBackedC11FacadeError(ValueError):
    pass


def _sha(value: str, name: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or value.lower() != value or any(c not in "0123456789abcdef" for c in value):
        raise SourceBackedC11FacadeError(f"{name} must be lowercase sha256")
    return value


def _dref(kind: str, ns: str, material: Any) -> ExactRef:
    h = semantic_hash(material)
    return ExactRef(kind, f"urn:rawlsing:pre553:c05r2a:{ns}:sha256:{h}", h)


def _auths(values: Iterable[AuthorityRef]) -> tuple[AuthorityRef, ...]:
    return tuple(sorted(set(values), key=lambda x: x.key))


def _refs(values: Iterable[ExactRef]) -> tuple[ExactRef, ...]:
    return tuple(sorted(set(values), key=lambda x: x.key))


def _opt_ref(value: Any, name: str) -> ExactRef | None:
    return None if value is None or isinstance(value, TypedAbsence) else exact_ref(value, name)


def exact_physical_value_material(value: Any) -> dict[str, Any]:
    """Return exact candidate-neutral physical material, never semantic material."""
    return {
        "schema": PHYSICAL_VALUE_MATERIAL_SCHEMA,
        "codec": R5_CODEC_VERSION,
        "token": _PHYSICAL_CODEC.encode(value),
    }


def raw_physical_value_witness(value: Any) -> dict[str, Any]:
    """Carry an observed physical value as an opaque C11 witness."""
    return {"$raw_physical_value": exact_physical_value_material(value)}


def physical_value_binding_key(raw_value: Any, missing_state: PhysicalMissingState | str,
                               declaration: Mapping[str, Any] | None = None) -> str:
    state = missing_state.value if isinstance(missing_state, PhysicalMissingState) else missing_state
    if state not in {x.value for x in PhysicalMissingState}:
        raise SourceBackedC11FacadeError("unknown physical missing state")
    material = {
        "schema": PHYSICAL_BINDING_SCHEMA,
        "codec": R5_CODEC_VERSION,
        "raw_value": _PHYSICAL_CODEC.encode(raw_value),
        "physical_state": state,
        "source_missing_declaration": _PHYSICAL_CODEC.encode(declaration),
    }
    return hashlib.sha256(r5_canonical_bytes(material)).hexdigest()


def _cell_key(cell: PhysicalCell) -> str:
    return physical_value_binding_key(cell.raw_value, cell.missing_state, cell.source_missing_declaration)


@dataclass(frozen=True, order=True)
class PhysicalSlot:
    ordinal: int
    name: str

    def __post_init__(self):
        if not isinstance(self.ordinal, int) or isinstance(self.ordinal, bool) or self.ordinal < 1 or not isinstance(self.name, str) or not self.name:
            raise SourceBackedC11FacadeError("invalid exact physical slot")

    @property
    def key(self):
        return (self.ordinal, self.name)


@dataclass(frozen=True)
class PhysicalSlotOwnerAuthorization:
    owner_family: str
    authority_refs: tuple[AuthorityRef, ...]

    def __post_init__(self):
        if self.owner_family not in _SUPPORTED_OWNER_FAMILIES:
            raise SourceBackedC11FacadeError("unsupported physical-slot semantic owner family")
        normalized = _auths(authority_ref(x, "physical-slot owner authority") for x in self.authority_refs)
        if not normalized:
            raise SourceBackedC11FacadeError("physical-slot semantic owner lacks explicit authority")
        if len(normalized) != len(self.authority_refs):
            raise SourceBackedC11FacadeError("duplicate physical-slot owner authority")
        object.__setattr__(self, "authority_refs", normalized)


@dataclass(frozen=True)
class PhysicalSlotOwnerSet:
    slot: PhysicalSlot
    owners: tuple[PhysicalSlotOwnerAuthorization, ...]
    contract_id: str = SLOT_OWNER_SET_CONTRACT_ID

    def __post_init__(self):
        if self.contract_id != SLOT_OWNER_SET_CONTRACT_ID:
            raise SourceBackedC11FacadeError("unsupported physical-slot owner-set contract")
        if not self.owners:
            raise SourceBackedC11FacadeError("physical-slot owner set cannot be empty")
        families = tuple(x.owner_family for x in self.owners)
        if len(families) != len(set(families)):
            raise SourceBackedC11FacadeError("conflicting duplicate physical-slot semantic owners")
        object.__setattr__(self, "owners", tuple(sorted(self.owners, key=lambda x: x.owner_family)))

    @property
    def owner_families(self) -> tuple[str, ...]:
        return tuple(x.owner_family for x in self.owners)

    def authority_refs_for(self, owner_family: str) -> tuple[AuthorityRef, ...]:
        for owner in self.owners:
            if owner.owner_family == owner_family:
                return owner.authority_refs
        return ()


@dataclass(frozen=True)
class RowRespondentBinding:
    row_ordinal: int
    respondent_ref: ExactRef


@dataclass(frozen=True)
class OccurrenceRule:
    key: str
    topology_ref: ExactRef
    multiplicity_order_rank_fields: Mapping[str, Any]
    component_ref: ExactRef | None = None


@dataclass(frozen=True)
class ResponseValueRule:
    physical_key: str
    response_state: str
    occurrences: tuple[OccurrenceRule, ...]
    canonical_value: Any = None
    transform_authority_ref: AuthorityRef | None = None
    extra_authority_refs: tuple[AuthorityRef, ...] = ()


@dataclass(frozen=True)
class ResponseSlotRule:
    slot: PhysicalSlot
    question_binding: QuestionVariableBinding
    values: tuple[ResponseValueRule, ...]


@dataclass(frozen=True)
class CoordinateValueRule:
    physical_key: str
    coordinate_state: str
    canonical_value: Any = None
    extra_authority_refs: tuple[AuthorityRef, ...] = ()


@dataclass(frozen=True)
class CoordinateSlotRule:
    slot: PhysicalSlot
    native_coordinate_ref: ExactRef
    unit_taxonomy_ref: ExactRef
    effective_time: Any
    source_semantic_authority_ref: AuthorityRef
    canonical_coordinate_ref: ExactRef | None = None
    normalization_ref: AuthorityRef | ExactRef | None = None
    values: tuple[CoordinateValueRule, ...] = ()
    copy_observed_raw: bool = False


@dataclass(frozen=True)
class WeightValueRule:
    physical_key: str
    exact_value: Any
    state: str = "WEIGHT_VALID_AUTHORIZED"


@dataclass(frozen=True)
class WeightSlotRule:
    slot: PhysicalSlot
    weight_basis_id: str
    weight_source_ref: ExactRef
    design_authority_ref: AuthorityRef
    estimand_authority_ref: AuthorityRef
    effective_scope_ref: ExactRef
    normalization_ref: AuthorityRef | ExactRef | None = None
    values: tuple[WeightValueRule, ...] = ()
    copy_observed_numeric: bool = False
    extra_authority_refs: tuple[AuthorityRef, ...] = ()


@dataclass(frozen=True)
class ExactPhysicalCellStream:
    source_sha256: str
    row_count: int
    cell_iter_factory: Callable[[], Iterable[PhysicalCell]]
    transport_identity: str = "EXACT_REPLAY_EQUIVALENT_PHYSICAL_CELL_STREAM"
    decoder_metadata_digest: str | None = None

    def __post_init__(self):
        _sha(self.source_sha256, "source_sha256")
        if self.decoder_metadata_digest is not None:
            _sha(self.decoder_metadata_digest, "decoder_metadata_digest")
        if not isinstance(self.row_count, int) or isinstance(self.row_count, bool) or self.row_count < 0 or not callable(self.cell_iter_factory):
            raise SourceBackedC11FacadeError("invalid exact physical-cell stream")

    def iter_cells(self):
        return self.cell_iter_factory()


@dataclass(frozen=True)
class GovernedC11Projection:
    projection_identity_ref: ExactRef
    source_artifact_id: str
    expected_source_sha256: str
    source_family_id: str
    study_product_id: str
    release_id: str
    instrument_release_id: str
    source_snapshot_retention_ref: ExactRef
    universes: tuple[EmpiricalUniverse, ...]
    respondents: tuple[RespondentIdentity, ...]
    row_bindings: tuple[RowRespondentBinding, ...]
    questions: tuple[QuestionVariableBinding, ...]
    response_slots: tuple[ResponseSlotRule, ...]
    coordinate_slots: tuple[CoordinateSlotRule, ...]
    routing: tuple[RoutingEligibilityFact, ...]
    weight_slots: tuple[WeightSlotRule, ...]
    authority_snapshots: tuple[AuthoritySnapshot, ...]
    source_relations: tuple[SourceUniverseRelation, ...] | TypedAbsence
    predicate_replay: tuple[C11InternalRecord, ...] | TypedAbsence
    comparator_replay: tuple[C11InternalRecord, ...] | TypedAbsence
    discovery_replay: tuple[C11InternalRecord, ...] | TypedAbsence
    structural_replay: tuple[C11InternalRecord, ...] | TypedAbsence
    required_authority_refs: tuple[AuthorityRef, ...]
    projection_authority_ref: AuthorityRef
    replay_authority_ref: AuthorityRef
    tie_order_ref: ExactRef
    replay_protocol_version: str
    slot_owner_sets: tuple[PhysicalSlotOwnerSet, ...] = ()

    def __post_init__(self):
        exact_ref(self.projection_identity_ref, "projection_identity_ref")
        _sha(self.expected_source_sha256, "expected_source_sha256")
        if self.source_snapshot_retention_ref.content_hash != self.expected_source_sha256:
            raise SourceBackedC11FacadeError("snapshot ref does not bind expected source SHA")
        if not all((self.universes, self.respondents, self.row_bindings, self.questions,
                    self.response_slots, self.coordinate_slots, self.routing,
                    self.authority_snapshots, self.required_authority_refs)):
            raise SourceBackedC11FacadeError("projection omits mandatory governed semantic input")
        mandatory = {self.projection_authority_ref, self.replay_authority_ref}
        if not mandatory.issubset(set(self.required_authority_refs)):
            raise SourceBackedC11FacadeError("projection/replay authorities must be explicitly required")
        packaged = {a.authority_ref for a in self.authority_snapshots}
        if not set(self.required_authority_refs).issubset(packaged):
            raise SourceBackedC11FacadeError("required authority absent from projection closure")
        if len({x.row_ordinal for x in self.row_bindings}) != len(self.row_bindings):
            raise SourceBackedC11FacadeError("duplicate row replay coordinate")
        respondent_refs = {r.ref for r in self.respondents}
        if any(x.respondent_ref not in respondent_refs for x in self.row_bindings):
            raise SourceBackedC11FacadeError("row binding references absent respondent")

        family_rules = (
            (RESPONSE_OWNER_FAMILY, self.response_slots),
            (COORDINATE_OWNER_FAMILY, self.coordinate_slots),
            (WEIGHT_OWNER_FAMILY, self.weight_slots),
        )
        actual: dict[tuple[int, str], set[str]] = {}
        for family, rules in family_rules:
            keys = [x.slot.key for x in rules]
            if len(keys) != len(set(keys)):
                raise SourceBackedC11FacadeError("conflicting duplicate physical-slot semantic owners")
            for key in keys:
                actual.setdefault(key, set()).add(family)

        owner_sets: dict[tuple[int, str], PhysicalSlotOwnerSet] = {}
        for owner_set in self.slot_owner_sets:
            if owner_set.slot.key in owner_sets:
                raise SourceBackedC11FacadeError("duplicate physical-slot owner set")
            owner_sets[owner_set.slot.key] = owner_set

        for key, families in actual.items():
            declared = owner_sets.get(key)
            if len(families) > 1 and declared is None:
                raise SourceBackedC11FacadeError("implicit/unapproved second physical-slot owner")
            if declared is not None and set(declared.owner_families) != families:
                raise SourceBackedC11FacadeError("physical-slot owner set does not exactly match emitted semantic owners")
        if set(owner_sets) - set(actual):
            raise SourceBackedC11FacadeError("physical-slot owner set references a slot with no emitted semantic owner")

        owner_authorities = {ref for owner_set in owner_sets.values() for owner in owner_set.owners for ref in owner.authority_refs}
        if not owner_authorities.issubset(set(self.required_authority_refs)):
            raise SourceBackedC11FacadeError("physical-slot owner authority must be explicitly required")
        if not owner_authorities.issubset(packaged):
            raise SourceBackedC11FacadeError("physical-slot owner authority absent from projection closure")
        owner_registry = AuthorityRegistry(self.authority_snapshots)
        for owner_set in owner_sets.values():
            for owner in owner_set.owners:
                for ref in owner.authority_refs:
                    owner_registry.require(ref, object_family=owner.owner_family)

    @property
    def cache_identity(self) -> str:
        owner_sets = [
            {
                "contract": x.contract_id,
                "slot": x.slot.key,
                "owners": [
                    {"family": o.owner_family, "authority_refs": [a.as_dict() for a in o.authority_refs]}
                    for o in x.owners
                ],
            }
            for x in sorted(self.slot_owner_sets, key=lambda x: x.slot.key)
        ]
        material = {
            "contract": CONTRACT_ID,
            "projection_identity_ref": self.projection_identity_ref.as_dict(),
            "source_sha256": self.expected_source_sha256,
            "required_authority_refs": [x.as_dict() for x in sorted(self.required_authority_refs, key=lambda r: r.key)],
        }
        if owner_sets:
            material["slot_owner_sets"] = owner_sets
        return semantic_hash(material)


def _owner_material(owner_authority_refs: Iterable[AuthorityRef]) -> tuple[AuthorityRef, ...]:
    return _auths(owner_authority_refs)


def _event(source_sha, row, respondent, slot, cell, value, occ, p, owner_authority_refs=()):
    q = slot.question_binding
    owner_authority_refs = _owner_material(owner_authority_refs)
    material = {"contract": CONTRACT_ID, "projection": p.projection_identity_ref.as_dict(), "source_sha": source_sha,
                "row": row, "respondent": respondent.ref.as_dict(), "question": q.ref.as_dict(),
                "slot": slot.slot.key, "physical_value_key": value.physical_key, "occurrence": occ.key}
    if owner_authority_refs:
        material["slot_owner_authority_refs"] = [x.as_dict() for x in owner_authority_refs]
    group = semantic_hash({**material, "role": "GROUP"})
    eid = semantic_hash({**material, "role": "EVENT"})
    auths = [p.projection_authority_ref, authority_ref(q.semantic_authority_ref, "question semantic authority"),
             authority_ref(q.topology_authority_ref, "question topology authority"), *value.extra_authority_refs,
             *owner_authority_refs]
    if value.transform_authority_ref is not None:
        auths.append(value.transform_authority_ref)
    component = occ.component_ref or _opt_ref(q.component_subitem_ref_or_typed_absence, "component")
    return RespondentEvent(
        typed_state=value.response_state, authority_snapshot_refs=_auths(auths), dependency_refs=_refs((respondent.ref, q.ref)),
        producer_replay_locator_or_reference_root=_dref("PRE553_C05R2A_EVENT_REPLAY_ROOT", "event", material),
        empirical_universe_ref=respondent.empirical_universe_ref, scoped_respondent_ref=respondent.ref,
        native_question_ref=q.native_question_ref,
        canonical_question_ref_if_authorized=_opt_ref(q.canonical_question_ref_or_typed_absence, "canonical question"),
        component_or_subitem_ref=component,
        event_group_id=f"urn:rawlsing:pre553:c05r2a:event-group:sha256:{group}",
        response_event_id_or_deterministic_index=f"urn:rawlsing:pre553:c05r2a:event:sha256:{eid}",
        raw_response_value=raw_physical_value_witness(cell.raw_value), canonical_response_value_if_authorized=canonicalize(value.canonical_value),
        value_transform_authority_ref=value.transform_authority_ref, response_topology_ref=occ.topology_ref,
        multiplicity_order_rank_fields=canonicalize(occ.multiplicity_order_rank_fields), response_state=value.response_state)


def _coordinate(source_sha, row, respondent, slot, cell, rule, p, owner_authority_refs=()):
    owner_authority_refs = _owner_material(owner_authority_refs)
    if rule is None:
        if not slot.copy_observed_raw or cell.missing_state is not PhysicalMissingState.OBSERVED_STORAGE_VALUE:
            raise SourceBackedC11FacadeError("unbound/missing coordinate cannot acquire semantics")
        state = "OBSERVED_COORDINATE"
        canonical = None
        extras = ()
    else:
        state = rule.coordinate_state
        canonical = rule.canonical_value
        extras = rule.extra_authority_refs
    material = {"contract": CONTRACT_ID, "projection": p.projection_identity_ref.as_dict(), "source_sha": source_sha, "row": row,
                "respondent": respondent.ref.as_dict(), "slot": slot.slot.key, "physical_value_key": _cell_key(cell)}
    if owner_authority_refs:
        material["slot_owner_authority_refs"] = [x.as_dict() for x in owner_authority_refs]
    auths = [p.projection_authority_ref, slot.source_semantic_authority_ref, *extras, *owner_authority_refs]
    if isinstance(slot.normalization_ref, AuthorityRef):
        auths.append(slot.normalization_ref)
    return EmpiricalCoordinateFact(
        typed_state=state, authority_snapshot_refs=_auths(auths), dependency_refs=(respondent.ref,),
        producer_replay_locator_or_reference_root=_dref("PRE553_C05R2A_COORDINATE_REPLAY_ROOT", "coordinate", material),
        empirical_universe_ref=respondent.empirical_universe_ref, scoped_respondent_ref=respondent.ref,
        native_coordinate_ref=slot.native_coordinate_ref, canonical_coordinate_ref_if_authorized=slot.canonical_coordinate_ref,
        raw_coordinate_value=raw_physical_value_witness(cell.raw_value), canonical_coordinate_value_if_authorized=canonicalize(canonical),
        unit_category_taxonomy_ref=slot.unit_taxonomy_ref, effective_or_reference_time=canonicalize(slot.effective_time),
        coordinate_state=state, normalization_crosswalk_authority_ref=slot.normalization_ref,
        source_semantic_authority_ref=slot.source_semantic_authority_ref)


def _numeric(value):
    if isinstance(value, bool) or value is None:
        raise SourceBackedC11FacadeError("weight raw copy requires numeric")
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise SourceBackedC11FacadeError("weight cannot be NaN/inf")
        text = repr(value)
        Fraction(text)
        return text
    if isinstance(value, str):
        text = value.strip()
        Fraction(text)
        return text
    raise SourceBackedC11FacadeError("weight raw copy requires exact numeric representation")


def _weight(source_sha, row, respondent, slot, cell, rule, p, owner_authority_refs=()):
    owner_authority_refs = _owner_material(owner_authority_refs)
    if rule is None:
        if not slot.copy_observed_numeric or cell.missing_state is not PhysicalMissingState.OBSERVED_STORAGE_VALUE:
            raise SourceBackedC11FacadeError("unbound/missing weight cannot default or fall back")
        state = "WEIGHT_VALID_AUTHORIZED"
        value = _numeric(cell.raw_value)
    else:
        state = rule.state
        value = rule.exact_value
    material = {"contract": CONTRACT_ID, "projection": p.projection_identity_ref.as_dict(), "source_sha": source_sha, "row": row,
                "respondent": respondent.ref.as_dict(), "slot": slot.slot.key, "physical_value_key": _cell_key(cell), "basis": slot.weight_basis_id}
    if owner_authority_refs:
        material["slot_owner_authority_refs"] = [x.as_dict() for x in owner_authority_refs]
    return WeightMeasureFact(
        typed_state=state, authority_snapshot_refs=_auths((p.projection_authority_ref, slot.design_authority_ref,
                                                           slot.estimand_authority_ref, *slot.extra_authority_refs,
                                                           *owner_authority_refs)),
        dependency_refs=(respondent.ref,), producer_replay_locator_or_reference_root=_dref("PRE553_C05R2A_WEIGHT_REPLAY_ROOT", "weight", material),
        empirical_universe_ref=respondent.empirical_universe_ref, scoped_respondent_ref=respondent.ref,
        weight_basis_id=slot.weight_basis_id, exact_weight_value_representation=canonicalize(value), weight_state=state,
        weight_source_ref=slot.weight_source_ref, design_authority_ref=slot.design_authority_ref,
        estimand_authority_ref=slot.estimand_authority_ref, normalization_or_recalibration_rule_ref=slot.normalization_ref,
        effective_scope_ref=slot.effective_scope_ref)


def _count(x):
    return 0 if isinstance(x, TypedAbsence) else len(x)


def _counts(p, events, coords, weights):
    return {"EmpiricalUniverse": len(p.universes), "RespondentIdentity": len(p.respondents), "QuestionVariableBinding": len(p.questions),
            "RespondentEvent": len(events), "RoutingEligibilityFact": len(p.routing), "EmpiricalCoordinateFact": len(coords),
            "WeightMeasureFact": _count(weights), "AuthoritySnapshot": len(p.authority_snapshots), "SourceUniverseRelation": _count(p.source_relations),
            "EmpiricalPredicateReplayBinding": _count(p.predicate_replay), "ComparatorReplayBinding": _count(p.comparator_replay),
            "DiscoveryBranchReplayBinding": _count(p.discovery_replay), "StructuralAdmissionReplayBinding": _count(p.structural_replay), "ReplayManifest": 1}


def project_c11_candidate_from_physical_cells(*, source_sha256: str, row_count: int,
                                               cells: Iterable[PhysicalCell], projection: GovernedC11Projection | None):
    if not isinstance(projection, GovernedC11Projection):
        raise SourceBackedC11FacadeError("explicit governed projection required; no semantic inference permitted")
    _sha(source_sha256, "source_sha256")
    if source_sha256 != projection.expected_source_sha256:
        raise SourceBackedC11FacadeError("source SHA mismatch")
    respondent_by_ref = {r.ref: r for r in projection.respondents}
    rows = {x.row_ordinal: respondent_by_ref[x.respondent_ref] for x in projection.row_bindings}
    if len(rows) != row_count:
        raise SourceBackedC11FacadeError("row/respondent replay map cardinality differs from exact physical stream")
    rs = {x.slot.key: x for x in projection.response_slots}
    cs = {x.slot.key: x for x in projection.coordinate_slots}
    ws = {x.slot.key: x for x in projection.weight_slots}
    owner_sets = {x.slot.key: x for x in projection.slot_owner_sets}
    projected = set(rs) | set(cs) | set(ws)
    seen = {s: set() for s in projected}
    events = []
    coords = []
    weights = []
    for cell in cells:
        if not isinstance(cell, PhysicalCell):
            raise SourceBackedC11FacadeError("non-PhysicalCell transport member")
        key = (cell.variable_ordinal, cell.variable_name)
        if key not in projected:
            continue
        if cell.row_ordinal not in rows:
            raise SourceBackedC11FacadeError("cell row outside replay map")
        if cell.row_ordinal in seen[key]:
            raise SourceBackedC11FacadeError("duplicate physical row/slot")
        seen[key].add(cell.row_ordinal)
        respondent = rows[cell.row_ordinal]
        pv = _cell_key(cell)
        owner_set = owner_sets.get(key)
        if key in rs:
            slot = rs[key]
            by = {x.physical_key: x for x in slot.values}
            value = by.get(pv)
            if value is None:
                raise SourceBackedC11FacadeError("unbound response value/state; no label/frequency/missingness inference")
            auths = owner_set.authority_refs_for(RESPONSE_OWNER_FAMILY) if owner_set else ()
            events.extend(_event(source_sha256, cell.row_ordinal, respondent, slot, cell, value, o, projection, auths)
                          for o in value.occurrences)
        if key in cs:
            slot = cs[key]
            rule = {x.physical_key: x for x in slot.values}.get(pv)
            auths = owner_set.authority_refs_for(COORDINATE_OWNER_FAMILY) if owner_set else ()
            coords.append(_coordinate(source_sha256, cell.row_ordinal, respondent, slot, cell, rule, projection, auths))
        if key in ws:
            slot = ws[key]
            rule = {x.physical_key: x for x in slot.values}.get(pv)
            auths = owner_set.authority_refs_for(WEIGHT_OWNER_FAMILY) if owner_set else ()
            weights.append(_weight(source_sha256, cell.row_ordinal, respondent, slot, cell, rule, projection, auths))
    expected = set(rows)
    if any(v != expected for v in seen.values()):
        raise SourceBackedC11FacadeError("projected slot incomplete; absent physical cell is not semantic absence")
    events = tuple(sorted(events, key=lambda x: x.ref.key))
    coords = tuple(sorted(coords, key=lambda x: x.ref.key))
    weight_section = tuple(sorted(weights, key=lambda x: x.ref.key)) if projection.weight_slots else TypedAbsence("NOT_APPLICABLE")
    manifest = SourceReleaseManifest(
        source_artifact_id=projection.source_artifact_id, source_artifact_content_hash=source_sha256, source_family_id=projection.source_family_id,
        study_product_id=projection.study_product_id, release_id=projection.release_id, instrument_release_id=projection.instrument_release_id,
        ingest_contract_version=INGEST_CONTRACT_VERSION, declared_universe_refs=tuple(sorted((x.ref for x in projection.universes), key=lambda r: r.key)),
        declared_authority_snapshot_refs=tuple(sorted((x.authority_ref for x in projection.authority_snapshots), key=lambda r: r.key)),
        declared_record_counts_by_logical_family=_counts(projection, events, coords, weight_section), source_snapshot_retention_ref=projection.source_snapshot_retention_ref)
    candidate = C11SourceReleaseCandidate(
        source_release_manifest=manifest, empirical_universes=tuple(sorted(projection.universes, key=lambda x: x.ref.key)),
        respondent_identities=tuple(sorted(projection.respondents, key=lambda x: x.ref.key)), question_variable_bindings=tuple(sorted(projection.questions, key=lambda x: x.ref.key)),
        respondent_events=events, routing_eligibility_facts_or_exact_rules=tuple(sorted(projection.routing, key=lambda x: x.ref.key)), empirical_coordinate_facts=coords,
        weight_measure_facts_or_typed_absence=weight_section, authority_snapshots=tuple(sorted(projection.authority_snapshots, key=lambda x: x.authority_ref.key)),
        source_universe_relations_or_explicit_distinct_default=projection.source_relations, predicate_replay_bindings_when_retained_objects_require_them=projection.predicate_replay,
        comparator_replay_bindings_or_typed_deferred_state=projection.comparator_replay, discovery_branch_replay_bindings_or_typed_deferred_state=projection.discovery_replay,
        structural_admission_replay_bindings_or_typed_not_applicable_state=projection.structural_replay, candidate_replay_manifest=None)
    replay = build_candidate_replay_manifest(candidate, replay_protocol_authority_ref=projection.replay_authority_ref,
                                             deterministic_tie_order_rules_ref=projection.tie_order_ref, replay_protocol_version=projection.replay_protocol_version)
    return replace(candidate, candidate_replay_manifest=replay)


def _verify(candidate, p, sha):
    m = candidate.source_release_manifest
    if m.source_artifact_content_hash != sha or m.source_snapshot_retention_ref.content_hash != sha:
        raise SourceBackedC11FacadeError("candidate/source SHA mismatch")
    required = set(p.required_authority_refs)
    packaged = {x.authority_ref for x in candidate.authority_snapshots}
    declared = set(m.declared_authority_snapshot_refs)
    if not required.issubset(packaged) or not required.issubset(declared):
        raise SourceBackedC11FacadeError("required authority absent from C11 candidate closure")


def build_validated_source_backed_c11_release(incidence: PhysicalSourceIncidence, projection: GovernedC11Projection | None, *, batch_size: int = 10_000):
    if not isinstance(projection, GovernedC11Projection):
        raise SourceBackedC11FacadeError("explicit governed projection required")
    bridge = PhysicalSourceAuthorityProjection(required_authority_refs=projection.required_authority_refs,
        candidate_builder=lambda source, cells, _: project_c11_candidate_from_physical_cells(source_sha256=source.source_sha256,
                                                                                             row_count=source.row_count,
                                                                                             cells=cells, projection=projection))
    return build_validated_c11_release(incidence, bridge, batch_size=batch_size)


def build_validated_source_backed_c11_release_from_stream(stream: ExactPhysicalCellStream, projection: GovernedC11Projection | None):
    if not isinstance(projection, GovernedC11Projection):
        raise SourceBackedC11FacadeError("explicit governed projection required")
    candidate = project_c11_candidate_from_physical_cells(source_sha256=stream.source_sha256, row_count=stream.row_count,
                                                           cells=stream.iter_cells(), projection=projection)
    _verify(candidate, projection, stream.source_sha256)
    return validate_c11_source_release(candidate)


@dataclass(frozen=True)
class SourceBackedFacadeKey:
    source_sha256: str
    projection_identity: str


class SourceBackedC11SessionCache:
    def __init__(self):
        self._entries = {}

    def get(self, key):
        entry = self._entries.get(key)
        if entry is None:
            return None
        stored_key, release = entry
        if stored_key != key or release.source_artifact_ref.content_hash != key.source_sha256:
            raise SourceBackedC11FacadeError("stale/tampered cache")
        return release

    def put(self, key, release):
        if not isinstance(release, C11LogicalRelease) or release.source_artifact_ref.content_hash != key.source_sha256:
            raise SourceBackedC11FacadeError("cache/source mismatch")
        self._entries[key] = (key, release)

    def clear(self):
        self._entries.clear()

    @property
    def entry_count(self):
        return len(self._entries)


def source_backed_facade_key(source, p):
    return SourceBackedFacadeKey(source.source_sha256, p.cache_identity)


def _accelerator_decoder_digest(source: PhysicalSourceIncidence | ExactPhysicalCellStream) -> str | None:
    if isinstance(source, ExactPhysicalCellStream):
        return source.decoder_metadata_digest
    try:
        return source.physical_metadata_digest
    except DecoderError:
        # Legacy in-memory incidence can be valid for I02 without a file decoder receipt.
        return None


def build_source_backed_c11_repository(
    source, projection, *, cache=None, batch_size=10_000, current_authorities=(),
):
    key = source_backed_facade_key(source, projection)
    release = cache.get(key) if cache else None
    if release is None:
        release = (build_validated_source_backed_c11_release(source, projection, batch_size=batch_size)
                   if isinstance(source, PhysicalSourceIncidence)
                   else build_validated_source_backed_c11_release_from_stream(source, projection)
                   if isinstance(source, ExactPhysicalCellStream)
                   else (_ for _ in ()).throw(SourceBackedC11FacadeError("unsupported physical transport")))
        def physical_binding():
            decoder_digest = _accelerator_decoder_digest(source)
            if isinstance(source, PhysicalSourceIncidence) and decoder_digest is None:
                return None
            return {
                "decoder_metadata": decoder_digest,
                "transport": getattr(source, "transport_identity", None),
                "facade_contract": CONTRACT_ID,
                "value_codec": R5_CODEC_VERSION,
                "current_authorities": sorted(snapshot.ref.key for snapshot in current_authorities),
            }

        public = _compact_public_objects(
            release, physical_binding=physical_binding, projection_binding=key.projection_identity,
        )
        if public is not None:
            release = replace(release, public_objects=public)
        if cache:
            cache.put(key, release)
    return C11Repository((release,)), release


def execute_source_backed_empirical_query(*, source, projection, query: EmpiricalQuerySpec, predicate: EmpiricalPredicate,
                                          authority_registry: AuthorityRegistry, cache=None, batch_size=10_000) -> QueryExecutionResult:
    repo, release = build_source_backed_c11_repository(source, projection, cache=cache, batch_size=batch_size)
    return execute_empirical_query(repository=repo, query=query, predicate=predicate, authority_registry=authority_registry,
                                   release_refs=(release.release_ref,))


__all__ = [
    "CONTRACT_ID", "SLOT_OWNER_SET_CONTRACT_ID", "RESPONSE_OWNER_FAMILY", "COORDINATE_OWNER_FAMILY", "WEIGHT_OWNER_FAMILY",
    "SourceBackedC11FacadeError", "PHYSICAL_VALUE_MATERIAL_SCHEMA", "PHYSICAL_BINDING_SCHEMA", "RAW_WITNESS_SCHEMA",
    "exact_physical_value_material", "raw_physical_value_witness", "PhysicalSlot", "PhysicalSlotOwnerAuthorization", "PhysicalSlotOwnerSet",
    "RowRespondentBinding", "OccurrenceRule", "ResponseValueRule", "ResponseSlotRule", "CoordinateValueRule",
    "CoordinateSlotRule", "WeightValueRule", "WeightSlotRule", "ExactPhysicalCellStream", "GovernedC11Projection",
    "SourceBackedFacadeKey", "SourceBackedC11SessionCache", "physical_value_binding_key",
    "project_c11_candidate_from_physical_cells", "build_validated_source_backed_c11_release",
    "build_validated_source_backed_c11_release_from_stream", "source_backed_facade_key",
    "build_source_backed_c11_repository", "execute_source_backed_empirical_query",
]
