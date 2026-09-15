"""PSC02 governed semantic capital -> HQ-adopted T03 intake compiler.

Compiler != semantic interpreter. Only explicit governed refs/states are accepted;
question text, labels, embeddings, statistics, model judgment and similarity are not.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable, Mapping

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    authority_ref,
    exact_ref,
    semantic_hash,
)
from rawlsing_next._prev3_structural_batch_base import (
    BlockerClass,
    CandidateKind,
    CandidateOutcome,
    CandidateStage,
    StructuralBatchControlPlaneError,
)
from rawlsing_next._prev3_structural_batch_records import (
    SemanticCandidateRecord,
    SourceLocalIntakeRecord,
)
from rawlsing_next._prev3_structural_batch_status import (
    CandidateBlockerRecord,
    CandidateStatusRecord,
    SemanticReductionResult,
)
from rawlsing_next._prev3_structural_batch_runtime import reduce_semantic_candidates

PSC02_COMPILER_CONTRACT_ID = (
    "PREV3_GOVERNED_SEMANTIC_CAPITAL_TO_ADOPTED_T03_INTAKE_COMPILER_R1@1.0.0"
)
T03_SEMANTIC_CANDIDATE = "5f90f5b94b76babe37c289840afd89005f67dbfe"
T03_QUALIFIED_EXECUTION_TREE = "545e2827bfdbaf07ffb9e54b4f822ae7db53b510"
T03_G03_COURT = "48 passed"
FINAL_RELEASE_HOLD = "FINAL_RELEASE_AWAITS_HQ_ADOPTED_PSC01_DENOMINATOR"
PREV3_BOUNDARY = "PRE_V3_OBJECTIVE_WORLD_ONLY"
OBL063_BOUNDARY = "OBL063_PERSON_TERMINAL_DRIVER_TYPE_SEMANTICS_QUARANTINED"


class GovernedSemanticCompilerError(StructuralBatchControlPlaneError):
    pass


class CurrentnessBlockedError(GovernedSemanticCompilerError):
    pass


class FixtureSchemaError(GovernedSemanticCompilerError):
    pass


class CarrierKind(str, Enum):
    FQRA = "FQRA"
    QSMV2 = "QSMV2"
    NEGATIVE_BLOCK = "NEGATIVE_BLOCK"
    RESPONSE_SEMANTICS = "RESPONSE_SEMANTICS"
    TYPED_RELATION = "TYPED_RELATION"


class EpistemicClass(str, Enum):
    MANUAL_ADJUDICATED = "MANUAL_ADJUDICATED"
    DETERMINISTIC_DERIVATION = "DETERMINISTIC_DERIVATION"


class SemanticJurisdiction(str, Enum):
    SOURCE_SEMANTIC = "SOURCE_SEMANTIC"
    RAWLSING_SEMANTIC = "RAWLSING_SEMANTIC"


class SemanticAuthorityState(str, Enum):
    POSITIVE = "POSITIVE"
    NEGATIVE_FORBIDDEN = "NEGATIVE_FORBIDDEN"
    BLOCKED = "BLOCKED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    SUPERSEDED = "SUPERSEDED"


class CurrentnessState(str, Enum):
    CURRENT = "CURRENT"
    HISTORICAL_NONCURRENT = "HISTORICAL_NONCURRENT"
    MISSING = "MISSING"
    AMBIGUOUS = "AMBIGUOUS"


class EquivalenceDecision(str, Enum):
    AUTHORIZED = "AUTHORIZED"
    DENIED = "DENIED"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    UNKNOWN_AUTHORITY = "UNKNOWN_AUTHORITY"
    CONFLICTING_AUTHORITY = "CONFLICTING_AUTHORITY"
    EXPIRED_OR_STALE = "EXPIRED_OR_STALE"


def _enum(value: Any, enum_type: type[Enum], name: str) -> Enum:
    try:
        return value if isinstance(value, enum_type) else enum_type(value)
    except (TypeError, ValueError) as exc:
        raise FixtureSchemaError(f"unknown {name}: {value!r}") from exc


def _ref(kind: str, object_id: str, material: Mapping[str, Any]) -> ExactRef:
    return ExactRef(kind, object_id, semantic_hash(material))


def _uniq(refs: Iterable[ExactRef]) -> tuple[ExactRef, ...]:
    by_key = {ref.key: ref for ref in refs}
    return tuple(by_key[key] for key in sorted(by_key))


def _auth_ref(value: AuthorityRef) -> ExactRef:
    return _ref(
        "PSC02_GOVERNED_AUTHORITY_REF",
        f"{value.authority_id}@{value.authority_version}",
        {"contract": PSC02_COMPILER_CONTRACT_ID, "authority_ref": value.as_dict()},
    )


@dataclass(frozen=True, slots=True)
class EquivalenceAuthority:
    relation_ref: ExactRef
    decision: EquivalenceDecision
    decision_ref: ExactRef
    authority_ref: AuthorityRef

    def __post_init__(self) -> None:
        object.__setattr__(self, "relation_ref", exact_ref(self.relation_ref))
        object.__setattr__(
            self,
            "decision",
            _enum(self.decision, EquivalenceDecision, "equivalence decision"),
        )
        object.__setattr__(self, "decision_ref", exact_ref(self.decision_ref))
        object.__setattr__(self, "authority_ref", authority_ref(self.authority_ref))

    @property
    def provenance_refs(self) -> tuple[ExactRef, ...]:
        return (self.relation_ref, self.decision_ref, _auth_ref(self.authority_ref))


@dataclass(frozen=True, slots=True)
class GovernedSemanticCapitalRecord:
    carrier_kind: CarrierKind
    carrier_locator_ref: ExactRef
    carrier_row_ref: ExactRef
    source_family_ref: ExactRef
    source_release_ref: ExactRef
    source_question_ref: ExactRef
    implementation_ref_or_exact_na: ExactRef
    authority_ref: AuthorityRef
    authority_snapshot_ref: ExactRef
    epistemic_class: EpistemicClass
    jurisdiction: SemanticJurisdiction
    authority_state: SemanticAuthorityState
    currentness_state: CurrentnessState
    currentness_ref: ExactRef | None
    noncurrent_disposition_ref: ExactRef | None
    response_category_semantics_ref: ExactRef
    routing_applicability_ref: ExactRef
    structural_use_ceiling_ref: ExactRef
    semantic_core_ref: ExactRef
    semantic_schema_ref: ExactRef
    negative_ceiling_ref: ExactRef
    type_class_ceiling_ref: ExactRef
    evidence_admission_refs: tuple[ExactRef, ...]
    provenance_refs: tuple[ExactRef, ...]
    equivalence_authorities: tuple[EquivalenceAuthority, ...]
    candidate_kind: CandidateKind = CandidateKind.STRUCTURAL_POSITION

    def __post_init__(self) -> None:
        object.__setattr__(self, "carrier_kind", _enum(self.carrier_kind, CarrierKind, "carrier_kind"))
        object.__setattr__(self, "authority_ref", authority_ref(self.authority_ref))
        object.__setattr__(
            self, "epistemic_class", _enum(self.epistemic_class, EpistemicClass, "epistemic_class")
        )
        object.__setattr__(
            self,
            "jurisdiction",
            _enum(self.jurisdiction, SemanticJurisdiction, "jurisdiction"),
        )
        object.__setattr__(
            self,
            "authority_state",
            _enum(self.authority_state, SemanticAuthorityState, "authority_state"),
        )
        object.__setattr__(
            self,
            "currentness_state",
            _enum(self.currentness_state, CurrentnessState, "currentness_state"),
        )
        object.__setattr__(
            self,
            "candidate_kind",
            _enum(self.candidate_kind, CandidateKind, "candidate_kind"),
        )
        for name in (
            "carrier_locator_ref",
            "carrier_row_ref",
            "source_family_ref",
            "source_release_ref",
            "source_question_ref",
            "implementation_ref_or_exact_na",
            "authority_snapshot_ref",
            "response_category_semantics_ref",
            "routing_applicability_ref",
            "structural_use_ceiling_ref",
            "semantic_core_ref",
            "semantic_schema_ref",
            "negative_ceiling_ref",
            "type_class_ceiling_ref",
        ):
            object.__setattr__(self, name, exact_ref(getattr(self, name), name))
        if self.currentness_ref is not None:
            object.__setattr__(self, "currentness_ref", exact_ref(self.currentness_ref))
        if self.noncurrent_disposition_ref is not None:
            object.__setattr__(
                self,
                "noncurrent_disposition_ref",
                exact_ref(self.noncurrent_disposition_ref),
            )
        if not self.evidence_admission_refs or not self.provenance_refs:
            raise FixtureSchemaError(
                "evidence_admission_refs and provenance_refs must be nonempty"
            )
        object.__setattr__(
            self,
            "evidence_admission_refs",
            _uniq(exact_ref(ref) for ref in self.evidence_admission_refs),
        )
        object.__setattr__(
            self,
            "provenance_refs",
            _uniq(exact_ref(ref) for ref in self.provenance_refs),
        )
        object.__setattr__(
            self,
            "equivalence_authorities",
            tuple(sorted(self.equivalence_authorities, key=lambda item: item.relation_ref.key)),
        )

    @property
    def positive_equivalence_refs(self) -> tuple[ExactRef, ...]:
        return tuple(
            item.relation_ref
            for item in self.equivalence_authorities
            if item.decision is EquivalenceDecision.AUTHORIZED
        )

    @property
    def equivalence_provenance_refs(self) -> tuple[ExactRef, ...]:
        return _uniq(
            ref
            for item in self.equivalence_authorities
            for ref in item.provenance_refs
        )


@dataclass(frozen=True, slots=True)
class CompiledT03SemanticIntake:
    carrier_kind: CarrierKind
    authority_ref: AuthorityRef
    epistemic_class: EpistemicClass
    jurisdiction: SemanticJurisdiction
    authority_state: SemanticAuthorityState
    currentness_state: CurrentnessState
    response_category_semantics_ref: ExactRef
    routing_applicability_ref: ExactRef
    structural_use_ceiling_ref: ExactRef
    positive_equivalence_refs: tuple[ExactRef, ...]
    source_local_intake: SourceLocalIntakeRecord
    semantic_candidate: SemanticCandidateRecord
    status: CandidateStatusRecord
    blocker: CandidateBlockerRecord | None = None

    @property
    def ref(self) -> ExactRef:
        material = {
            "contract": PSC02_COMPILER_CONTRACT_ID,
            "carrier": self.carrier_kind.value,
            "authority": self.authority_ref.as_dict(),
            "epistemic": self.epistemic_class.value,
            "jurisdiction": self.jurisdiction.value,
            "state": self.authority_state.value,
            "currentness": self.currentness_state.value,
            "response": self.response_category_semantics_ref.as_dict(),
            "routing": self.routing_applicability_ref.as_dict(),
            "ceiling": self.structural_use_ceiling_ref.as_dict(),
            "positive_equivalence_refs": [
                ref.as_dict() for ref in self.positive_equivalence_refs
            ],
            "source_local": self.source_local_intake.ref.as_dict(),
            "candidate": self.semantic_candidate.ref.as_dict(),
            "status": self.status.ref.as_dict(),
            "blocker": None if self.blocker is None else self.blocker.ref.as_dict(),
            "hold": FINAL_RELEASE_HOLD,
            "prev3": PREV3_BOUNDARY,
            "obl063": OBL063_BOUNDARY,
        }
        return _ref(
            "PSC02_COMPILED_T03_GOVERNED_SEMANTIC_INTAKE",
            self.semantic_candidate.logical_key,
            material,
        )


@dataclass(frozen=True, slots=True)
class GovernedReductionGroup:
    """A T03 reduction partition whose upstream governed semantics are identical."""

    authority_state: SemanticAuthorityState
    currentness_state: CurrentnessState
    jurisdiction: SemanticJurisdiction
    epistemic_class: EpistemicClass
    response_category_semantics_ref: ExactRef
    routing_applicability_ref: ExactRef
    structural_use_ceiling_ref: ExactRef
    reduction: SemanticReductionResult

    @property
    def key(self) -> tuple[str, ...]:
        return (
            self.authority_state.value,
            self.currentness_state.value,
            self.jurisdiction.value,
            self.epistemic_class.value,
            self.response_category_semantics_ref.key,
            self.routing_applicability_ref.key,
            self.structural_use_ceiling_ref.key,
        )


@dataclass(frozen=True, slots=True)
class CompiledBatch:
    compiled: tuple[CompiledT03SemanticIntake, ...]
    reduction_groups: tuple[GovernedReductionGroup, ...]
    reduction: SemanticReductionResult
    final_release_hold: str = FINAL_RELEASE_HOLD


def _validate_currentness(record: GovernedSemanticCapitalRecord) -> None:
    if (
        record.currentness_state in (CurrentnessState.MISSING, CurrentnessState.AMBIGUOUS)
        or record.currentness_ref is None
    ):
        raise CurrentnessBlockedError("missing or ambiguous governed currentness")
    if record.currentness_state is CurrentnessState.CURRENT:
        if (
            record.authority_state is SemanticAuthorityState.SUPERSEDED
            or record.noncurrent_disposition_ref is not None
        ):
            raise CurrentnessBlockedError("contradictory CURRENT/SUPERSEDED currentness")
    elif record.noncurrent_disposition_ref is None:
        raise CurrentnessBlockedError(
            "HISTORICAL_NONCURRENT requires exact noncurrent disposition"
        )


def _source_universe(record: GovernedSemanticCapitalRecord) -> ExactRef:
    return _ref(
        "PSC02_SOURCE_UNIVERSE_IDENTITY",
        f"{record.source_family_ref.object_id}:{record.source_release_ref.object_id}",
        {
            "family": record.source_family_ref.as_dict(),
            "release": record.source_release_ref.as_dict(),
        },
    )


def _source_item(record: GovernedSemanticCapitalRecord) -> ExactRef:
    return _ref(
        "PSC02_SOURCE_QUESTION_IMPLEMENTATION_IDENTITY",
        (
            f"{record.source_question_ref.object_id}:"
            f"{record.implementation_ref_or_exact_na.object_id}"
        ),
        {
            "question": record.source_question_ref.as_dict(),
            "implementation": record.implementation_ref_or_exact_na.as_dict(),
        },
    )


def _state_ref(record: GovernedSemanticCapitalRecord) -> ExactRef:
    return _ref(
        "PSC02_DECLARED_GOVERNED_SEMANTIC_STATE",
        record.carrier_row_ref.object_id,
        {
            "state": record.authority_state.value,
            "currentness": record.currentness_state.value,
            "currentness_ref": record.currentness_ref.as_dict()
            if record.currentness_ref
            else None,
            "epistemic": record.epistemic_class.value,
            "jurisdiction": record.jurisdiction.value,
            "authority": record.authority_ref.as_dict(),
            "snapshot": record.authority_snapshot_ref.as_dict(),
        },
    )


def _claim_ref(record: GovernedSemanticCapitalRecord) -> ExactRef:
    return _ref(
        "PSC02_GOVERNED_SEMANTIC_CAPITAL_CLAIM",
        record.carrier_row_ref.object_id,
        {
            "snapshot": record.authority_snapshot_ref.as_dict(),
            "family": record.source_family_ref.as_dict(),
            "release": record.source_release_ref.as_dict(),
            "question": record.source_question_ref.as_dict(),
            "implementation": record.implementation_ref_or_exact_na.as_dict(),
            "core": record.semantic_core_ref.as_dict(),
            "schema": record.semantic_schema_ref.as_dict(),
            "response": record.response_category_semantics_ref.as_dict(),
            "routing": record.routing_applicability_ref.as_dict(),
            "ceiling": record.structural_use_ceiling_ref.as_dict(),
            "negative_ceiling": record.negative_ceiling_ref.as_dict(),
            "type_ceiling": record.type_class_ceiling_ref.as_dict(),
            "state": record.authority_state.value,
            "currentness": record.currentness_state.value,
            "jurisdiction": record.jurisdiction.value,
            "epistemic": record.epistemic_class.value,
        },
    )


def _replay_ref(record: GovernedSemanticCapitalRecord) -> ExactRef:
    return _ref(
        "PSC02_COMPILER_REPLAY_BASIS",
        record.carrier_row_ref.object_id,
        {
            "contract": PSC02_COMPILER_CONTRACT_ID,
            "carrier": record.carrier_kind.value,
            "locator": record.carrier_locator_ref.as_dict(),
            "row": record.carrier_row_ref.as_dict(),
            "authority": record.authority_ref.as_dict(),
            "snapshot": record.authority_snapshot_ref.as_dict(),
            "currentness": record.currentness_ref.as_dict()
            if record.currentness_ref
            else None,
            "core": record.semantic_core_ref.as_dict(),
            "schema": record.semantic_schema_ref.as_dict(),
            "negative_ceiling": record.negative_ceiling_ref.as_dict(),
            "type_ceiling": record.type_class_ceiling_ref.as_dict(),
        },
    )


def _candidate_id(record: GovernedSemanticCapitalRecord) -> str:
    return semantic_hash(
        {
            "family": record.source_family_ref.as_dict(),
            "release": record.source_release_ref.as_dict(),
            "question": record.source_question_ref.as_dict(),
            "implementation": record.implementation_ref_or_exact_na.as_dict(),
            "authority": record.authority_ref.as_dict(),
            "row": record.carrier_row_ref.as_dict(),
        }
    )


def compile_governed_semantic_capital(
    record: GovernedSemanticCapitalRecord,
) -> CompiledT03SemanticIntake:
    if not isinstance(record, GovernedSemanticCapitalRecord):
        raise GovernedSemanticCompilerError(
            "record must be GovernedSemanticCapitalRecord"
        )
    _validate_currentness(record)

    direct_refs = (
        record.carrier_locator_ref,
        record.carrier_row_ref,
        record.authority_snapshot_ref,
        _auth_ref(record.authority_ref),
        record.source_family_ref,
        record.source_release_ref,
        record.source_question_ref,
        record.implementation_ref_or_exact_na,
        record.response_category_semantics_ref,
        record.routing_applicability_ref,
        record.structural_use_ceiling_ref,
        record.semantic_core_ref,
        record.semantic_schema_ref,
        record.negative_ceiling_ref,
        record.type_class_ceiling_ref,
        record.currentness_ref,
        record.noncurrent_disposition_ref,
    )
    provenance = _uniq(
        ref
        for ref in (
            *record.provenance_refs,
            *direct_refs,
            *record.equivalence_provenance_refs,
        )
        if ref is not None
    )
    evidence = _uniq(
        (
            *record.evidence_admission_refs,
            record.authority_snapshot_ref,
            *record.positive_equivalence_refs,
        )
    )
    state_ref = _state_ref(record)
    source_local = SourceLocalIntakeRecord(
        _source_universe(record),
        _source_item(record),
        state_ref,
        record.routing_applicability_ref,
        (
            _claim_ref(record),
            record.response_category_semantics_ref,
            record.structural_use_ceiling_ref,
        ),
        state_ref,
        provenance,
        _replay_ref(record),
    )
    candidate = SemanticCandidateRecord(
        "PSC02_GOVERNED_SEMANTIC_CAPITAL",
        _candidate_id(record),
        0,
        None,
        record.candidate_kind,
        record.semantic_core_ref,
        record.semantic_schema_ref,
        evidence,
        record.negative_ceiling_ref,
        record.type_class_ceiling_ref,
        CandidateStage.CLAIM_NORMALIZED,
        _uniq((*provenance, source_local.ref)),
    )
    basis = _uniq(
        (record.authority_snapshot_ref, record.currentness_ref, state_ref, source_local.ref)
    )
    blocker = None
    if record.authority_state in (
        SemanticAuthorityState.BLOCKED,
        SemanticAuthorityState.REVIEW_REQUIRED,
    ):
        blocker = CandidateBlockerRecord(
            candidate.ref,
            BlockerClass.AUTHORITY,
            "governed_semantic_capital.authority_state",
            (
                "upstream state must be resolved before downstream routing: "
                f"{record.authority_state.value}"
            ),
            basis,
            "EXACT_UPSTREAM_GOVERNED_AUTHORITY_RESOLUTION_REQUIRED",
        )
        status = CandidateStatusRecord(
            candidate.ref,
            CandidateOutcome.BLOCKED,
            basis,
            blocker_refs=(blocker.ref,),
            current_selection_refs=(record.currentness_ref,),
        )
    elif (
        record.authority_state is SemanticAuthorityState.SUPERSEDED
        or record.currentness_state is CurrentnessState.HISTORICAL_NONCURRENT
    ):
        status = CandidateStatusRecord(
            candidate.ref,
            CandidateOutcome.HISTORICAL_NONCURRENT,
            basis,
            current_selection_refs=(record.currentness_ref,),
            noncurrent_disposition_refs=(record.noncurrent_disposition_ref,),
        )
    else:
        status = CandidateStatusRecord(
            candidate.ref,
            CandidateOutcome.CANDIDATE_ONLY,
            basis,
            current_selection_refs=(record.currentness_ref,),
        )
    return CompiledT03SemanticIntake(
        record.carrier_kind,
        record.authority_ref,
        record.epistemic_class,
        record.jurisdiction,
        record.authority_state,
        record.currentness_state,
        record.response_category_semantics_ref,
        record.routing_applicability_ref,
        record.structural_use_ceiling_ref,
        record.positive_equivalence_refs,
        source_local,
        candidate,
        status,
        blocker,
    )


def _reduction_group_key(item: CompiledT03SemanticIntake) -> tuple[str, ...]:
    return (
        item.authority_state.value,
        item.currentness_state.value,
        item.jurisdiction.value,
        item.epistemic_class.value,
        item.response_category_semantics_ref.key,
        item.routing_applicability_ref.key,
        item.structural_use_ceiling_ref.key,
    )


def compile_governed_semantic_batch(
    records: Iterable[GovernedSemanticCapitalRecord],
) -> CompiledBatch:
    compiled = tuple(compile_governed_semantic_capital(record) for record in records)

    # Run the adopted T03 reducer globally only as a fail-closed conflict guard.
    # Its aggregates are not used because T03 intentionally knows nothing about
    # PSC02-only authority state/jurisdiction/response/routing/use-ceiling fields.
    global_guard = reduce_semantic_candidates(
        item.semantic_candidate for item in compiled
    )
    quarantined_candidate_keys = {
        quarantine.candidate_ref.key for quarantine in global_guard.quarantines
    }

    grouped: dict[tuple[str, ...], list[CompiledT03SemanticIntake]] = {}
    for item in compiled:
        if item.semantic_candidate.ref.key in quarantined_candidate_keys:
            continue
        grouped.setdefault(_reduction_group_key(item), []).append(item)

    reduction_groups: list[GovernedReductionGroup] = []
    aggregate_by_ref = {}
    quarantine_by_ref = {
        quarantine.ref.key: quarantine for quarantine in global_guard.quarantines
    }
    for key in sorted(grouped):
        members = grouped[key]
        first = sorted(members, key=lambda item: item.ref.key)[0]
        reduction = reduce_semantic_candidates(
            item.semantic_candidate for item in members
        )
        group = GovernedReductionGroup(
            first.authority_state,
            first.currentness_state,
            first.jurisdiction,
            first.epistemic_class,
            first.response_category_semantics_ref,
            first.routing_applicability_ref,
            first.structural_use_ceiling_ref,
            reduction,
        )
        reduction_groups.append(group)
        for aggregate in reduction.aggregates:
            aggregate_by_ref[aggregate.ref.key] = aggregate
        for quarantine in reduction.quarantines:
            quarantine_by_ref[quarantine.ref.key] = quarantine

    combined = SemanticReductionResult(
        tuple(aggregate_by_ref[key] for key in sorted(aggregate_by_ref)),
        tuple(quarantine_by_ref[key] for key in sorted(quarantine_by_ref)),
    )
    return CompiledBatch(
        compiled,
        tuple(sorted(reduction_groups, key=lambda group: group.key)),
        combined,
    )


_FIELDS = frozenset(
    "carrier_locator_ref carrier_row_ref source_family_ref source_release_ref "
    "source_question_ref implementation_ref_or_exact_na authority_ref "
    "authority_snapshot_ref epistemic_class jurisdiction authority_state "
    "currentness_state currentness_ref noncurrent_disposition_ref "
    "response_category_semantics_ref routing_applicability_ref "
    "structural_use_ceiling_ref semantic_core_ref semantic_schema_ref "
    "negative_ceiling_ref type_class_ceiling_ref evidence_admission_refs "
    "provenance_refs equivalence_authorities candidate_kind".split()
)


def _parse_equivalence_fixture(value: Mapping[str, Any]) -> EquivalenceAuthority:
    expected = {"relation_ref", "decision", "decision_ref", "authority_ref"}
    if set(value) != expected:
        raise FixtureSchemaError(
            "equivalence fixture fields mismatch; "
            f"missing={sorted(expected - set(value))}, "
            f"extra={sorted(set(value) - expected)}"
        )
    return EquivalenceAuthority(
        exact_ref(value["relation_ref"]),
        _enum(value["decision"], EquivalenceDecision, "equivalence decision"),
        exact_ref(value["decision_ref"]),
        authority_ref(value["authority_ref"]),
    )


def _adapt_fixture(material: Mapping[str, Any], kind: CarrierKind) -> GovernedSemanticCapitalRecord:
    if not isinstance(material, Mapping) or set(material) != _FIELDS:
        missing = sorted(_FIELDS - set(material)) if isinstance(material, Mapping) else sorted(_FIELDS)
        extra = sorted(set(material) - _FIELDS) if isinstance(material, Mapping) else []
        raise FixtureSchemaError(
            f"fixture fields mismatch; missing={missing}, extra={extra}"
        )

    def ref(name: str) -> ExactRef:
        return exact_ref(material[name], name)

    return GovernedSemanticCapitalRecord(
        kind,
        ref("carrier_locator_ref"),
        ref("carrier_row_ref"),
        ref("source_family_ref"),
        ref("source_release_ref"),
        ref("source_question_ref"),
        ref("implementation_ref_or_exact_na"),
        authority_ref(material["authority_ref"]),
        ref("authority_snapshot_ref"),
        _enum(material["epistemic_class"], EpistemicClass, "epistemic_class"),
        _enum(material["jurisdiction"], SemanticJurisdiction, "jurisdiction"),
        _enum(material["authority_state"], SemanticAuthorityState, "authority_state"),
        _enum(material["currentness_state"], CurrentnessState, "currentness_state"),
        None if material["currentness_ref"] is None else ref("currentness_ref"),
        None
        if material["noncurrent_disposition_ref"] is None
        else ref("noncurrent_disposition_ref"),
        ref("response_category_semantics_ref"),
        ref("routing_applicability_ref"),
        ref("structural_use_ceiling_ref"),
        ref("semantic_core_ref"),
        ref("semantic_schema_ref"),
        ref("negative_ceiling_ref"),
        ref("type_class_ceiling_ref"),
        tuple(exact_ref(item) for item in material["evidence_admission_refs"]),
        tuple(exact_ref(item) for item in material["provenance_refs"]),
        tuple(
            _parse_equivalence_fixture(item)
            for item in material["equivalence_authorities"]
        ),
        _enum(material["candidate_kind"], CandidateKind, "candidate_kind"),
    )


def adapt_fqra_fixture(material: Mapping[str, Any]) -> GovernedSemanticCapitalRecord:
    return _adapt_fixture(material, CarrierKind.FQRA)


def adapt_qsmv2_fixture(material: Mapping[str, Any]) -> GovernedSemanticCapitalRecord:
    return _adapt_fixture(material, CarrierKind.QSMV2)


def adapt_negative_block_fixture(material: Mapping[str, Any]) -> GovernedSemanticCapitalRecord:
    return _adapt_fixture(material, CarrierKind.NEGATIVE_BLOCK)


def adapt_response_semantics_fixture(material: Mapping[str, Any]) -> GovernedSemanticCapitalRecord:
    return _adapt_fixture(material, CarrierKind.RESPONSE_SEMANTICS)


def adapt_typed_relation_fixture(material: Mapping[str, Any]) -> GovernedSemanticCapitalRecord:
    return _adapt_fixture(material, CarrierKind.TYPED_RELATION)
