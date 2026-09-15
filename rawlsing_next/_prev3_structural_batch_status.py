"""Candidate status, blocker, quarantine, and reduction records."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next._prev3_structural_batch_base import (
    CONTROL_PLANE_CONTRACT_ID,
    BLOCKER_REF_KIND,
    QUARANTINE_REF_KIND,
    STATUS_REF_KIND,
    SEMANTIC_CORE_AGGREGATE_REF_KIND,
    CandidateKind,
    CandidateOutcome,
    BlockerClass,
    QuarantineReason,
    StructuralBatchControlPlaneError,
    _text,
    _exact_ref,
    _exact_ref_tuple,
    _optional_exact_ref,
    _enum,
    _ref,
)

@dataclass(frozen=True, slots=True)
class CandidateBlockerRecord:
    candidate_ref: ExactRef
    blocker_class: BlockerClass
    field_path: str
    requirement: str
    basis_refs: tuple[ExactRef, ...]
    closure_requirement: str
    shared_contract_blocker_ref: ExactRef | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "candidate_ref", _exact_ref(self.candidate_ref, "candidate_ref"))
        object.__setattr__(
            self, "blocker_class", _enum(self.blocker_class, BlockerClass, "blocker_class")
        )
        object.__setattr__(self, "field_path", _text(self.field_path, "field_path"))
        object.__setattr__(self, "requirement", _text(self.requirement, "requirement"))
        object.__setattr__(
            self,
            "basis_refs",
            _exact_ref_tuple(self.basis_refs, "basis_refs", require_nonempty=True),
        )
        object.__setattr__(
            self,
            "closure_requirement",
            _text(self.closure_requirement, "closure_requirement"),
        )
        object.__setattr__(
            self,
            "shared_contract_blocker_ref",
            _optional_exact_ref(self.shared_contract_blocker_ref, "shared_contract_blocker_ref"),
        )

    def as_material(self) -> Mapping[str, Any]:
        return {
            "contract_id": CONTROL_PLANE_CONTRACT_ID,
            "candidate_ref": self.candidate_ref.as_dict(),
            "blocker_class": self.blocker_class.value,
            "field_path": self.field_path,
            "requirement": self.requirement,
            "basis_refs": [ref.as_dict() for ref in self.basis_refs],
            "closure_requirement": self.closure_requirement,
            "shared_contract_blocker_ref": (
                None
                if self.shared_contract_blocker_ref is None
                else self.shared_contract_blocker_ref.as_dict()
            ),
        }

    @property
    def ref(self) -> ExactRef:
        return _ref(BLOCKER_REF_KIND, self.candidate_ref.content_hash, self.as_material())


@dataclass(frozen=True, slots=True)
class CandidateQuarantineRecord:
    candidate_ref: ExactRef
    reason: QuarantineReason
    basis_refs: tuple[ExactRef, ...]
    conflict_refs: tuple[ExactRef, ...] = ()
    shared_contract_blocker_ref: ExactRef | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "candidate_ref", _exact_ref(self.candidate_ref, "candidate_ref"))
        object.__setattr__(self, "reason", _enum(self.reason, QuarantineReason, "quarantine reason"))
        object.__setattr__(
            self,
            "basis_refs",
            _exact_ref_tuple(
                self.basis_refs,
                "basis_refs",
                require_nonempty=True,
                allow_logical_conflicts=True,
            ),
        )
        object.__setattr__(
            self,
            "conflict_refs",
            _exact_ref_tuple(
                self.conflict_refs,
                "conflict_refs",
                require_nonempty=False,
                allow_logical_conflicts=True,
            ),
        )
        object.__setattr__(
            self,
            "shared_contract_blocker_ref",
            _optional_exact_ref(self.shared_contract_blocker_ref, "shared_contract_blocker_ref"),
        )

    def as_material(self) -> Mapping[str, Any]:
        return {
            "contract_id": CONTROL_PLANE_CONTRACT_ID,
            "candidate_ref": self.candidate_ref.as_dict(),
            "reason": self.reason.value,
            "basis_refs": [ref.as_dict() for ref in self.basis_refs],
            "conflict_refs": [ref.as_dict() for ref in self.conflict_refs],
            "shared_contract_blocker_ref": (
                None
                if self.shared_contract_blocker_ref is None
                else self.shared_contract_blocker_ref.as_dict()
            ),
        }

    @property
    def ref(self) -> ExactRef:
        return _ref(QUARANTINE_REF_KIND, self.candidate_ref.content_hash, self.as_material())


@dataclass(frozen=True, slots=True)
class CandidateStatusRecord:
    candidate_ref: ExactRef
    outcome: CandidateOutcome
    basis_refs: tuple[ExactRef, ...]
    blocker_refs: tuple[ExactRef, ...] = ()
    quarantine_refs: tuple[ExactRef, ...] = ()
    na_basis_refs: tuple[ExactRef, ...] = ()
    current_selection_refs: tuple[ExactRef, ...] = ()
    noncurrent_disposition_refs: tuple[ExactRef, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "candidate_ref", _exact_ref(self.candidate_ref, "candidate_ref"))
        object.__setattr__(self, "outcome", _enum(self.outcome, CandidateOutcome, "candidate outcome"))
        object.__setattr__(
            self,
            "basis_refs",
            _exact_ref_tuple(self.basis_refs, "basis_refs", require_nonempty=True),
        )
        for name in (
            "blocker_refs",
            "quarantine_refs",
            "na_basis_refs",
            "current_selection_refs",
            "noncurrent_disposition_refs",
        ):
            object.__setattr__(
                self,
                name,
                _exact_ref_tuple(getattr(self, name), name, require_nonempty=False),
            )

        if self.outcome is CandidateOutcome.BLOCKED and not self.blocker_refs:
            raise StructuralBatchControlPlaneError("BLOCKED status requires exact blocker_refs")
        if self.outcome is CandidateOutcome.QUARANTINED and not self.quarantine_refs:
            raise StructuralBatchControlPlaneError(
                "QUARANTINED status requires exact quarantine_refs"
            )
        if self.outcome is CandidateOutcome.NOT_APPLICABLE and not self.na_basis_refs:
            raise StructuralBatchControlPlaneError(
                "NOT_APPLICABLE requires exact N/A basis; omission is never N/A"
            )
        if self.outcome is CandidateOutcome.CURRENT:
            if not self.current_selection_refs or self.noncurrent_disposition_refs:
                raise StructuralBatchControlPlaneError(
                    "CURRENT requires exact current-selection refs and no noncurrent disposition"
                )
        if self.outcome is CandidateOutcome.HISTORICAL_NONCURRENT:
            if not self.current_selection_refs or not self.noncurrent_disposition_refs:
                raise StructuralBatchControlPlaneError(
                    "HISTORICAL_NONCURRENT requires prior selection and noncurrent disposition refs"
                )

    def as_material(self) -> Mapping[str, Any]:
        return {
            "contract_id": CONTROL_PLANE_CONTRACT_ID,
            "candidate_ref": self.candidate_ref.as_dict(),
            "outcome": self.outcome.value,
            "basis_refs": [ref.as_dict() for ref in self.basis_refs],
            "blocker_refs": [ref.as_dict() for ref in self.blocker_refs],
            "quarantine_refs": [ref.as_dict() for ref in self.quarantine_refs],
            "na_basis_refs": [ref.as_dict() for ref in self.na_basis_refs],
            "current_selection_refs": [ref.as_dict() for ref in self.current_selection_refs],
            "noncurrent_disposition_refs": [
                ref.as_dict() for ref in self.noncurrent_disposition_refs
            ],
        }

    @property
    def ref(self) -> ExactRef:
        return _ref(STATUS_REF_KIND, self.candidate_ref.content_hash, self.as_material())


@dataclass(frozen=True, slots=True)
class SemanticCoreAggregate:
    """Deterministic many-to-one reduction result preserving every evidence edge."""

    candidate_kind: CandidateKind
    semantic_core_ref: ExactRef
    semantic_schema_ref: ExactRef
    negative_ceiling_ref: ExactRef
    type_class_ceiling_ref: ExactRef
    candidate_refs: tuple[ExactRef, ...]
    evidence_admission_refs: tuple[ExactRef, ...]
    provenance_refs: tuple[ExactRef, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "candidate_kind", _enum(self.candidate_kind, CandidateKind, "candidate_kind")
        )
        for name in (
            "semantic_core_ref",
            "semantic_schema_ref",
            "negative_ceiling_ref",
            "type_class_ceiling_ref",
        ):
            object.__setattr__(self, name, _exact_ref(getattr(self, name), name))
        for name in ("candidate_refs", "evidence_admission_refs", "provenance_refs"):
            object.__setattr__(
                self,
                name,
                _exact_ref_tuple(getattr(self, name), name, require_nonempty=True),
            )

    def as_material(self) -> Mapping[str, Any]:
        return {
            "contract_id": CONTROL_PLANE_CONTRACT_ID,
            "candidate_kind": self.candidate_kind.value,
            "semantic_core_ref": self.semantic_core_ref.as_dict(),
            "semantic_schema_ref": self.semantic_schema_ref.as_dict(),
            "negative_ceiling_ref": self.negative_ceiling_ref.as_dict(),
            "type_class_ceiling_ref": self.type_class_ceiling_ref.as_dict(),
            "candidate_refs": [ref.as_dict() for ref in self.candidate_refs],
            "evidence_admission_refs": [
                ref.as_dict() for ref in self.evidence_admission_refs
            ],
            "provenance_refs": [ref.as_dict() for ref in self.provenance_refs],
        }

    @property
    def ref(self) -> ExactRef:
        return _ref(
            SEMANTIC_CORE_AGGREGATE_REF_KIND,
            self.semantic_core_ref.content_hash,
            self.as_material(),
        )


@dataclass(frozen=True, slots=True)
class SemanticReductionResult:
    aggregates: tuple[SemanticCoreAggregate, ...]
    quarantines: tuple[CandidateQuarantineRecord, ...]

    @property
    def aggregate_refs(self) -> tuple[ExactRef, ...]:
        return tuple(item.ref for item in self.aggregates)

    @property
    def quarantine_refs(self) -> tuple[ExactRef, ...]:
        return tuple(item.ref for item in self.quarantines)


__all__ = [
    "CandidateBlockerRecord",
    "CandidateQuarantineRecord",
    "CandidateStatusRecord",
    "SemanticCoreAggregate",
    "SemanticReductionResult",
]
