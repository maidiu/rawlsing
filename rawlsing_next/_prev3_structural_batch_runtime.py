"""Deterministic receipts, routing, and semantic reduction for PRE-V3 batches."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef
from rawlsing_next._prev3_structural_batch_base import (
    CONTROL_PLANE_CONTRACT_ID,
    STAGE_RECEIPT_REF_KIND,
    POSITION_ROUTE_REF_KIND,
    MECHANISM_ROUTE_REF_KIND,
    CandidateKind,
    CandidateOutcome,
    BatchStage,
    QuarantineReason,
    SpecializedRouteKind,
    StructuralBatchControlPlaneError,
    IdentityConflictError,
    QuarantinedCandidateError,
    _STAGE_ORDER,
    _text,
    _reject_mutable_selector_text,
    _exact_ref,
    _authority_ref_tuple,
    _exact_ref_tuple,
    _optional_exact_ref,
    _enum,
    _ref,
    _same_ref,
    _reject_topology_ref,
    require_replay,
)
from rawlsing_next._prev3_structural_batch_records import SemanticCandidateRecord
from rawlsing_next._prev3_structural_batch_status import (
    CandidateBlockerRecord,
    CandidateQuarantineRecord,
    CandidateStatusRecord,
    SemanticCoreAggregate,
    SemanticReductionResult,
)

@dataclass(frozen=True, slots=True)
class StageReceipt:
    batch_item_ref: ExactRef
    stage: BatchStage
    object_kind: str
    outcome: CandidateOutcome
    input_refs: tuple[ExactRef, ...]
    output_refs: tuple[ExactRef, ...]
    authority_refs: tuple[AuthorityRef, ...]
    basis_refs: tuple[ExactRef, ...]
    predecessor_receipt_ref: ExactRef | None = None
    predecessor_stage: BatchStage | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "batch_item_ref", _exact_ref(self.batch_item_ref, "batch_item_ref"))
        object.__setattr__(self, "stage", _enum(self.stage, BatchStage, "batch stage"))
        object.__setattr__(self, "object_kind", _text(self.object_kind, "object_kind"))
        object.__setattr__(self, "outcome", _enum(self.outcome, CandidateOutcome, "outcome"))
        for name, required in (
            ("input_refs", True),
            ("output_refs", False),
            ("basis_refs", True),
        ):
            object.__setattr__(
                self,
                name,
                _exact_ref_tuple(getattr(self, name), name, require_nonempty=required),
            )
        object.__setattr__(
            self,
            "authority_refs",
            _authority_ref_tuple(self.authority_refs, "authority_refs"),
        )
        predecessor = _optional_exact_ref(self.predecessor_receipt_ref, "predecessor_receipt_ref")
        object.__setattr__(self, "predecessor_receipt_ref", predecessor)
        if predecessor is None:
            if self.predecessor_stage is not None:
                raise IdentityConflictError(
                    "predecessor_stage may not exist without predecessor_receipt_ref"
                )
        else:
            if self.predecessor_stage is None:
                raise IdentityConflictError(
                    "predecessor_receipt_ref requires exact predecessor_stage"
                )
            previous = _enum(self.predecessor_stage, BatchStage, "predecessor_stage")
            object.__setattr__(self, "predecessor_stage", previous)
            if _STAGE_ORDER[previous] >= _STAGE_ORDER[self.stage]:
                raise IdentityConflictError(
                    "receipt predecessor must be from an earlier pipeline stage"
                )

    def as_material(self) -> Mapping[str, Any]:
        return {
            "contract_id": CONTROL_PLANE_CONTRACT_ID,
            "batch_item_ref": self.batch_item_ref.as_dict(),
            "stage": self.stage.value,
            "object_kind": self.object_kind,
            "outcome": self.outcome.value,
            "input_refs": [ref.as_dict() for ref in self.input_refs],
            "output_refs": [ref.as_dict() for ref in self.output_refs],
            "authority_refs": [ref.as_dict() for ref in self.authority_refs],
            "basis_refs": [ref.as_dict() for ref in self.basis_refs],
            "predecessor_receipt_ref": (
                None
                if self.predecessor_receipt_ref is None
                else self.predecessor_receipt_ref.as_dict()
            ),
            "predecessor_stage": (
                None if self.predecessor_stage is None else self.predecessor_stage.value
            ),
        }

    @property
    def ref(self) -> ExactRef:
        object_id = f"{self.batch_item_ref.content_hash}:{self.stage.value}"
        return _ref(STAGE_RECEIPT_REF_KIND, object_id, self.as_material())

    def require_replay(self, expected_ref: ExactRef) -> StageReceipt:
        require_replay(expected_ref, self.ref, "stage receipt")
        return self


@dataclass(frozen=True, slots=True)
class PositionQualificationRoute:
    candidate_ref: ExactRef
    downstream_contract_ref: ExactRef
    routing_basis_refs: tuple[ExactRef, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "candidate_ref", _exact_ref(self.candidate_ref, "candidate_ref"))
        object.__setattr__(
            self,
            "downstream_contract_ref",
            _reject_topology_ref(self.downstream_contract_ref, "downstream_contract_ref"),
        )
        object.__setattr__(
            self,
            "routing_basis_refs",
            _exact_ref_tuple(
                self.routing_basis_refs, "routing_basis_refs", require_nonempty=True
            ),
        )

    def as_material(self) -> Mapping[str, Any]:
        return {
            "contract_id": CONTROL_PLANE_CONTRACT_ID,
            "route_kind": SpecializedRouteKind.POSITION_QUALIFICATION.value,
            "candidate_ref": self.candidate_ref.as_dict(),
            "downstream_contract_ref": self.downstream_contract_ref.as_dict(),
            "routing_basis_refs": [ref.as_dict() for ref in self.routing_basis_refs],
            "boundary": "ROUTE_ONLY__NO_OCCUPANT_FACT",
        }

    @property
    def ref(self) -> ExactRef:
        return _ref(POSITION_ROUTE_REF_KIND, self.candidate_ref.content_hash, self.as_material())


@dataclass(frozen=True, slots=True)
class MechanismRuleCandidateRoute:
    """Route a mechanism candidate to a specialized envelope contract, not a rule."""

    candidate_ref: ExactRef
    normalized_mechanism_ref: ExactRef
    type_class_ceiling_ref: ExactRef
    mechanism_class_values: tuple[str, ...]
    downstream_contract_ref: ExactRef
    routing_basis_refs: tuple[ExactRef, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "candidate_ref", _exact_ref(self.candidate_ref, "candidate_ref"))
        object.__setattr__(
            self,
            "normalized_mechanism_ref",
            _exact_ref(self.normalized_mechanism_ref, "normalized_mechanism_ref"),
        )
        object.__setattr__(
            self,
            "type_class_ceiling_ref",
            _exact_ref(self.type_class_ceiling_ref, "type_class_ceiling_ref"),
        )
        if isinstance(self.mechanism_class_values, (str, bytes, bytearray)):
            raise StructuralBatchControlPlaneError(
                "mechanism_class_values must be an iterable of exact class values"
            )
        classes = {
            _reject_mutable_selector_text(value, "mechanism_class_value")
            for value in self.mechanism_class_values
        }
        if not classes:
            raise StructuralBatchControlPlaneError(
                "mechanism candidate route requires at least one mechanism class value"
            )
        object.__setattr__(self, "mechanism_class_values", tuple(sorted(classes)))
        object.__setattr__(
            self,
            "downstream_contract_ref",
            _reject_topology_ref(self.downstream_contract_ref, "downstream_contract_ref"),
        )
        object.__setattr__(
            self,
            "routing_basis_refs",
            _exact_ref_tuple(
                self.routing_basis_refs, "routing_basis_refs", require_nonempty=True
            ),
        )

    def as_material(self) -> Mapping[str, Any]:
        return {
            "contract_id": CONTROL_PLANE_CONTRACT_ID,
            "route_kind": SpecializedRouteKind.R4_GENERIC_BATCH_ENVELOPE.value,
            "candidate_ref": self.candidate_ref.as_dict(),
            "normalized_mechanism_ref": self.normalized_mechanism_ref.as_dict(),
            "type_class_ceiling_ref": self.type_class_ceiling_ref.as_dict(),
            "mechanism_class_values": list(self.mechanism_class_values),
            "downstream_contract_ref": self.downstream_contract_ref.as_dict(),
            "routing_basis_refs": [ref.as_dict() for ref in self.routing_basis_refs],
            "boundary": "ROUTE_ONLY__NO_CONCRETE_RULE_OR_CURRENTNESS",
        }

    @property
    def ref(self) -> ExactRef:
        return _ref(MECHANISM_ROUTE_REF_KIND, self.candidate_ref.content_hash, self.as_material())


def _routable(candidate: SemanticCandidateRecord, status: CandidateStatusRecord) -> None:
    if not _same_ref(candidate.ref, status.candidate_ref):
        raise IdentityConflictError("candidate status does not bind the candidate snapshot being routed")
    if status.outcome in {
        CandidateOutcome.BLOCKED,
        CandidateOutcome.UNAVAILABLE,
        CandidateOutcome.NOT_APPLICABLE,
        CandidateOutcome.QUARANTINED,
    }:
        raise QuarantinedCandidateError(
            f"candidate outcome {status.outcome.value} is not routable"
        )


def route_position_candidate(
    candidate: SemanticCandidateRecord,
    status: CandidateStatusRecord,
    downstream_contract_ref: ExactRef,
    routing_basis_refs: Iterable[ExactRef],
) -> PositionQualificationRoute:
    _routable(candidate, status)
    if candidate.candidate_kind is not CandidateKind.STRUCTURAL_POSITION:
        raise StructuralBatchControlPlaneError(
            "position qualification route requires STRUCTURAL_POSITION candidate"
        )
    return PositionQualificationRoute(
        candidate_ref=candidate.ref,
        downstream_contract_ref=downstream_contract_ref,
        routing_basis_refs=tuple(routing_basis_refs),
    )


def route_mechanism_candidate(
    candidate: SemanticCandidateRecord,
    status: CandidateStatusRecord,
    normalized_mechanism_ref: ExactRef,
    mechanism_class_values: Iterable[str],
    downstream_contract_ref: ExactRef,
    routing_basis_refs: Iterable[ExactRef],
) -> MechanismRuleCandidateRoute:
    _routable(candidate, status)
    if candidate.candidate_kind is not CandidateKind.MECHANISM_RULE:
        raise StructuralBatchControlPlaneError(
            "mechanism route requires MECHANISM_RULE candidate"
        )
    normalized = _exact_ref(normalized_mechanism_ref, "normalized_mechanism_ref")
    if not _same_ref(normalized, candidate.semantic_core_ref):
        raise IdentityConflictError(
            "mechanism route may not replace or widen the admitted semantic core"
        )
    return MechanismRuleCandidateRoute(
        candidate_ref=candidate.ref,
        normalized_mechanism_ref=normalized,
        type_class_ceiling_ref=candidate.type_class_ceiling_ref,
        mechanism_class_values=tuple(mechanism_class_values),
        downstream_contract_ref=downstream_contract_ref,
        routing_basis_refs=tuple(routing_basis_refs),
    )


def blocker_applies_to(
    blocker: CandidateBlockerRecord,
    candidate_ref: ExactRef,
    *,
    exact_shared_contract_refs: Iterable[ExactRef] = (),
) -> bool:
    candidate = _exact_ref(candidate_ref, "candidate_ref")
    if _same_ref(blocker.candidate_ref, candidate):
        return True
    if blocker.shared_contract_blocker_ref is None:
        return False
    shared = _exact_ref_tuple(
        tuple(exact_shared_contract_refs),
        "exact_shared_contract_refs",
        require_nonempty=False,
    )
    return any(_same_ref(blocker.shared_contract_blocker_ref, ref) for ref in shared)


def quarantine_applies_to(
    quarantine: CandidateQuarantineRecord,
    candidate_ref: ExactRef,
    *,
    exact_shared_contract_refs: Iterable[ExactRef] = (),
) -> bool:
    candidate = _exact_ref(candidate_ref, "candidate_ref")
    if _same_ref(quarantine.candidate_ref, candidate):
        return True
    if quarantine.shared_contract_blocker_ref is None:
        return False
    shared = _exact_ref_tuple(
        tuple(exact_shared_contract_refs),
        "exact_shared_contract_refs",
        require_nonempty=False,
    )
    return any(_same_ref(quarantine.shared_contract_blocker_ref, ref) for ref in shared)


def _quarantine_group(
    records: Sequence[SemanticCandidateRecord],
    reason: QuarantineReason,
) -> list[CandidateQuarantineRecord]:
    refs = tuple(sorted((record.ref for record in records), key=lambda ref: ref.key))
    result: list[CandidateQuarantineRecord] = []
    for record in records:
        conflict_refs = tuple(ref for ref in refs if ref.key != record.ref.key)
        basis = refs if refs else (record.ref,)
        result.append(
            CandidateQuarantineRecord(
                candidate_ref=record.ref,
                reason=reason,
                basis_refs=basis,
                conflict_refs=conflict_refs,
            )
        )
    return result


def reduce_semantic_candidates(
    candidates: Iterable[SemanticCandidateRecord],
) -> SemanticReductionResult:
    if isinstance(candidates, (str, bytes, bytearray)):
        raise StructuralBatchControlPlaneError(
            "candidates must be an iterable of SemanticCandidateRecord"
        )
    raw = tuple(candidates)
    if any(not isinstance(candidate, SemanticCandidateRecord) for candidate in raw):
        raise StructuralBatchControlPlaneError(
            "candidates must contain only SemanticCandidateRecord"
        )

    # Retry/duplicate presentation of the exact same snapshot is idempotent.
    exact_by_ref: dict[str, SemanticCandidateRecord] = {candidate.ref.key: candidate for candidate in raw}
    records = tuple(exact_by_ref[key] for key in sorted(exact_by_ref))

    quarantined_keys: set[str] = set()
    quarantines: list[CandidateQuarantineRecord] = []

    # Same logical candidate snapshot key with different governed material is a conflict.
    by_logical: dict[str, list[SemanticCandidateRecord]] = {}
    for record in records:
        by_logical.setdefault(record.logical_key, []).append(record)
    for group in by_logical.values():
        if len({record.ref.content_hash for record in group}) > 1:
            quarantines.extend(_quarantine_group(group, QuarantineReason.IDENTITY_CONFLICT))
            quarantined_keys.update(record.ref.key for record in group)

    # Same semantic-core logical ref with different content hashes is never winner-selected.
    by_core_logical: dict[tuple[str, str], list[SemanticCandidateRecord]] = {}
    for record in records:
        if record.ref.key in quarantined_keys:
            continue
        logical = (record.semantic_core_ref.kind, record.semantic_core_ref.object_id)
        by_core_logical.setdefault(logical, []).append(record)
    for group in by_core_logical.values():
        if len({record.semantic_core_ref.content_hash for record in group}) > 1:
            quarantines.extend(
                _quarantine_group(group, QuarantineReason.SEMANTIC_CORE_CONFLICT)
            )
            quarantined_keys.update(record.ref.key for record in group)

    # Exact core equality may reduce only when the surrounding governed semantic
    # schema/ceilings agree. Evidence/provenance are deliberately not in this signature.
    by_core_exact: dict[str, list[SemanticCandidateRecord]] = {}
    for record in records:
        if record.ref.key in quarantined_keys:
            continue
        by_core_exact.setdefault(record.semantic_core_ref.key, []).append(record)
    for group in by_core_exact.values():
        signatures = {
            (
                record.candidate_kind.value,
                record.semantic_schema_ref.key,
                record.negative_ceiling_ref.key,
                record.type_class_ceiling_ref.key,
            )
            for record in group
        }
        if len(signatures) > 1:
            quarantines.extend(
                _quarantine_group(group, QuarantineReason.SEMANTIC_CORE_CONFLICT)
            )
            quarantined_keys.update(record.ref.key for record in group)

    aggregates: list[SemanticCoreAggregate] = []
    for core_key in sorted(by_core_exact):
        group = [
            record
            for record in by_core_exact[core_key]
            if record.ref.key not in quarantined_keys
        ]
        if not group:
            continue
        first = sorted(group, key=lambda item: item.ref.key)[0]
        candidate_refs = tuple(record.ref for record in group)
        evidence_refs = tuple(
            ref for record in group for ref in record.evidence_admission_refs
        )
        provenance_refs = tuple(ref for record in group for ref in record.provenance_refs)
        aggregates.append(
            SemanticCoreAggregate(
                candidate_kind=first.candidate_kind,
                semantic_core_ref=first.semantic_core_ref,
                semantic_schema_ref=first.semantic_schema_ref,
                negative_ceiling_ref=first.negative_ceiling_ref,
                type_class_ceiling_ref=first.type_class_ceiling_ref,
                candidate_refs=candidate_refs,
                evidence_admission_refs=evidence_refs,
                provenance_refs=provenance_refs,
            )
        )

    aggregates.sort(key=lambda item: item.ref.key)
    quarantine_by_ref = {item.ref.key: item for item in quarantines}
    sorted_quarantines = tuple(
        quarantine_by_ref[key] for key in sorted(quarantine_by_ref)
    )
    return SemanticReductionResult(tuple(aggregates), sorted_quarantines)


def process_semantic_batch(
    candidates: Iterable[SemanticCandidateRecord],
    *,
    shard_count: int = 1,
    retry_ordinal: int = 0,
    worker_identity: str | None = None,
) -> SemanticReductionResult:
    """Reduce a candidate batch while treating execution metadata as nonsemantic."""
    if isinstance(shard_count, bool) or not isinstance(shard_count, int) or shard_count < 1:
        raise StructuralBatchControlPlaneError("shard_count must be a positive integer")
    if isinstance(retry_ordinal, bool) or not isinstance(retry_ordinal, int) or retry_ordinal < 0:
        raise StructuralBatchControlPlaneError("retry_ordinal must be a nonnegative integer")
    if worker_identity is not None:
        _text(worker_identity, "worker_identity")
    # Intentionally do not pass execution metadata into semantic reduction.
    return reduce_semantic_candidates(candidates)


__all__ = [
    "StageReceipt",
    "PositionQualificationRoute",
    "MechanismRuleCandidateRoute",
    "route_position_candidate",
    "route_mechanism_candidate",
    "blocker_applies_to",
    "quarantine_applies_to",
    "reduce_semantic_candidates",
    "process_semantic_batch",
]
