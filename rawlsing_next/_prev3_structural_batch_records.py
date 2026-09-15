"""Typed source/candidate records for the generic PRE-V3 control plane."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, semantic_hash
from rawlsing_next._prev3_structural_batch_base import (
    CONTROL_PLANE_CONTRACT_ID,
    SOURCE_LOCAL_INTAKE_REF_KIND,
    POSITION_SEMANTIC_CORE_REF_KIND,
    SEMANTIC_CANDIDATE_REF_KIND,
    POSITION_MATERIALIZATION_REQUEST_REF_KIND,
    CandidateKind,
    CandidateStage,
    StructuralBatchControlPlaneError,
    IdentityConflictError,
    PositionOccupantLeakError,
    _FORBIDDEN_POSITION_CORE_KEYS,
    _reject_mutable_selector_text,
    _exact_ref,
    _authority_ref,
    _exact_ref_tuple,
    _optional_exact_ref,
    _enum,
    _ref,
    require_replay,
)

@dataclass(frozen=True, slots=True)
class SourceLocalIntakeRecord:
    """Exact source-local evidence node; normalization never replaces this identity."""

    source_universe_ref: ExactRef
    source_item_ref: ExactRef
    source_local_state_ref: ExactRef
    routing_or_applicability_ref_or_exact_na: ExactRef
    claim_refs: tuple[ExactRef, ...]
    evidence_status_ref: ExactRef
    provenance_refs: tuple[ExactRef, ...]
    producer_replay_ref: ExactRef

    def __post_init__(self) -> None:
        for name in (
            "source_universe_ref",
            "source_item_ref",
            "source_local_state_ref",
            "routing_or_applicability_ref_or_exact_na",
            "evidence_status_ref",
            "producer_replay_ref",
        ):
            object.__setattr__(self, name, _exact_ref(getattr(self, name), name))
        object.__setattr__(
            self,
            "claim_refs",
            _exact_ref_tuple(self.claim_refs, "claim_refs", require_nonempty=True),
        )
        object.__setattr__(
            self,
            "provenance_refs",
            _exact_ref_tuple(self.provenance_refs, "provenance_refs", require_nonempty=True),
        )

    def as_material(self) -> Mapping[str, Any]:
        return {
            "contract_id": CONTROL_PLANE_CONTRACT_ID,
            "source_universe_ref": self.source_universe_ref.as_dict(),
            "source_item_ref": self.source_item_ref.as_dict(),
            "source_local_state_ref": self.source_local_state_ref.as_dict(),
            "routing_or_applicability_ref_or_exact_na":
                self.routing_or_applicability_ref_or_exact_na.as_dict(),
            "claim_refs": [ref.as_dict() for ref in self.claim_refs],
            "evidence_status_ref": self.evidence_status_ref.as_dict(),
            "provenance_refs": [ref.as_dict() for ref in self.provenance_refs],
            "producer_replay_ref": self.producer_replay_ref.as_dict(),
        }

    @property
    def ref(self) -> ExactRef:
        object_id = f"{self.source_universe_ref.object_id}:{self.source_item_ref.object_id}"
        return _ref(SOURCE_LOCAL_INTAKE_REF_KIND, object_id, self.as_material())

    def require_replay(self, expected_ref: ExactRef) -> SourceLocalIntakeRecord:
        require_replay(expected_ref, self.ref, "source-local intake")
        return self


@dataclass(frozen=True, slots=True)
class PositionSemanticCore:
    """Reusable occupant-independent structural-position meaning."""

    semantic_class_ref: ExactRef
    canonical_structural_meaning_ref: ExactRef
    constitutive_objective_relation_refs: tuple[ExactRef, ...]
    required_counterpart_or_context_role_refs: tuple[ExactRef, ...]
    semantic_negative_ceiling_ref: ExactRef

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "semantic_class_ref", _exact_ref(self.semantic_class_ref, "semantic_class_ref")
        )
        object.__setattr__(
            self,
            "canonical_structural_meaning_ref",
            _exact_ref(self.canonical_structural_meaning_ref, "canonical_structural_meaning_ref"),
        )
        object.__setattr__(
            self,
            "constitutive_objective_relation_refs",
            _exact_ref_tuple(
                self.constitutive_objective_relation_refs,
                "constitutive_objective_relation_refs",
                require_nonempty=True,
            ),
        )
        object.__setattr__(
            self,
            "required_counterpart_or_context_role_refs",
            _exact_ref_tuple(
                self.required_counterpart_or_context_role_refs,
                "required_counterpart_or_context_role_refs",
                require_nonempty=True,
            ),
        )
        object.__setattr__(
            self,
            "semantic_negative_ceiling_ref",
            _exact_ref(self.semantic_negative_ceiling_ref, "semantic_negative_ceiling_ref"),
        )

    @classmethod
    def from_material(cls, material: Mapping[str, Any]) -> PositionSemanticCore:
        if not isinstance(material, Mapping):
            raise StructuralBatchControlPlaneError("position semantic core material must be a mapping")
        leaked = _FORBIDDEN_POSITION_CORE_KEYS.intersection(material)
        if leaked:
            raise PositionOccupantLeakError(
                "occupant identity is forbidden from reusable position-semantic-core identity: "
                + ", ".join(sorted(leaked))
            )
        expected = {
            "semantic_class_ref",
            "canonical_structural_meaning_ref",
            "constitutive_objective_relation_refs",
            "required_counterpart_or_context_role_refs",
            "semantic_negative_ceiling_ref",
        }
        if set(material) != expected:
            missing = sorted(expected - set(material))
            extra = sorted(set(material) - expected)
            raise StructuralBatchControlPlaneError(
                f"position semantic core fields mismatch; missing={missing}, extra={extra}"
            )
        return cls(**material)  # type: ignore[arg-type]

    def as_material(self) -> Mapping[str, Any]:
        return {
            "contract_id": CONTROL_PLANE_CONTRACT_ID,
            "semantic_class_ref": self.semantic_class_ref.as_dict(),
            "canonical_structural_meaning_ref": self.canonical_structural_meaning_ref.as_dict(),
            "constitutive_objective_relation_refs": [
                ref.as_dict() for ref in self.constitutive_objective_relation_refs
            ],
            "required_counterpart_or_context_role_refs": [
                ref.as_dict() for ref in self.required_counterpart_or_context_role_refs
            ],
            "semantic_negative_ceiling_ref": self.semantic_negative_ceiling_ref.as_dict(),
        }

    @property
    def ref(self) -> ExactRef:
        digest = semantic_hash(self.as_material())
        return ExactRef(
            POSITION_SEMANTIC_CORE_REF_KIND,
            f"position-semantic-core:{digest}",
            digest,
        )


@dataclass(frozen=True, slots=True)
class PositionMaterializationRequest:
    """Later actor-indexed request identity; this is not an objective-position fact."""

    position_semantic_core_ref: ExactRef
    occupant_actor_or_entity_ref: ExactRef
    applicability_ref: ExactRef
    permission_authority_ref: AuthorityRef
    valid_time_currentness_ref: ExactRef
    provenance_dependency_refs: tuple[ExactRef, ...]
    replay_authority_ref: ExactRef

    def __post_init__(self) -> None:
        for name in (
            "position_semantic_core_ref",
            "occupant_actor_or_entity_ref",
            "applicability_ref",
            "valid_time_currentness_ref",
            "replay_authority_ref",
        ):
            object.__setattr__(self, name, _exact_ref(getattr(self, name), name))
        object.__setattr__(
            self,
            "permission_authority_ref",
            _authority_ref(self.permission_authority_ref, "permission_authority_ref"),
        )
        object.__setattr__(
            self,
            "provenance_dependency_refs",
            _exact_ref_tuple(
                self.provenance_dependency_refs,
                "provenance_dependency_refs",
                require_nonempty=True,
            ),
        )

    def as_material(self) -> Mapping[str, Any]:
        return {
            "contract_id": CONTROL_PLANE_CONTRACT_ID,
            "position_semantic_core_ref": self.position_semantic_core_ref.as_dict(),
            "occupant_actor_or_entity_ref": self.occupant_actor_or_entity_ref.as_dict(),
            "applicability_ref": self.applicability_ref.as_dict(),
            "permission_authority_ref": self.permission_authority_ref.as_dict(),
            "valid_time_currentness_ref": self.valid_time_currentness_ref.as_dict(),
            "provenance_dependency_refs": [
                ref.as_dict() for ref in self.provenance_dependency_refs
            ],
            "replay_authority_ref": self.replay_authority_ref.as_dict(),
            "boundary": "REQUEST_ONLY__NO_ACTOR_FACT_MATERIALIZED",
        }

    @property
    def ref(self) -> ExactRef:
        object_id = (
            f"{self.position_semantic_core_ref.content_hash}:"
            f"{self.occupant_actor_or_entity_ref.content_hash}"
        )
        return _ref(POSITION_MATERIALIZATION_REQUEST_REF_KIND, object_id, self.as_material())


@dataclass(frozen=True, slots=True)
class SemanticCandidateRecord:
    """One governed candidate snapshot pointing at a reusable semantic core."""

    candidate_namespace: str
    candidate_id: str
    snapshot_generation: int
    predecessor_candidate_ref: ExactRef | None
    candidate_kind: CandidateKind
    semantic_core_ref: ExactRef
    semantic_schema_ref: ExactRef
    evidence_admission_refs: tuple[ExactRef, ...]
    negative_ceiling_ref: ExactRef
    type_class_ceiling_ref: ExactRef
    candidate_stage: CandidateStage
    provenance_refs: tuple[ExactRef, ...]

    def __post_init__(self) -> None:
        namespace = _reject_mutable_selector_text(self.candidate_namespace, "candidate_namespace")
        candidate_id = _reject_mutable_selector_text(self.candidate_id, "candidate_id")
        object.__setattr__(self, "candidate_namespace", namespace)
        object.__setattr__(self, "candidate_id", candidate_id)
        if isinstance(self.snapshot_generation, bool) or not isinstance(self.snapshot_generation, int):
            raise StructuralBatchControlPlaneError("snapshot_generation must be an integer")
        if self.snapshot_generation < 0:
            raise StructuralBatchControlPlaneError("snapshot_generation must be nonnegative")

        predecessor = _optional_exact_ref(self.predecessor_candidate_ref, "predecessor_candidate_ref")
        if self.snapshot_generation == 0 and predecessor is not None:
            raise IdentityConflictError("generation zero may not carry predecessor_candidate_ref")
        if self.snapshot_generation > 0:
            if predecessor is None:
                raise IdentityConflictError("successor candidate generation requires exact predecessor")
            expected_object_id = f"{namespace}:{candidate_id}:g{self.snapshot_generation - 1}"
            if (
                predecessor.kind != SEMANTIC_CANDIDATE_REF_KIND
                or predecessor.object_id != expected_object_id
            ):
                raise IdentityConflictError(
                    "predecessor_candidate_ref must be the immediately prior governed generation"
                )
        object.__setattr__(self, "predecessor_candidate_ref", predecessor)

        object.__setattr__(
            self,
            "candidate_kind",
            _enum(self.candidate_kind, CandidateKind, "candidate_kind"),
        )
        object.__setattr__(
            self, "semantic_core_ref", _exact_ref(self.semantic_core_ref, "semantic_core_ref")
        )
        object.__setattr__(
            self, "semantic_schema_ref", _exact_ref(self.semantic_schema_ref, "semantic_schema_ref")
        )
        object.__setattr__(
            self,
            "evidence_admission_refs",
            _exact_ref_tuple(
                self.evidence_admission_refs,
                "evidence_admission_refs",
                require_nonempty=True,
            ),
        )
        object.__setattr__(
            self, "negative_ceiling_ref", _exact_ref(self.negative_ceiling_ref, "negative_ceiling_ref")
        )
        object.__setattr__(
            self,
            "type_class_ceiling_ref",
            _exact_ref(self.type_class_ceiling_ref, "type_class_ceiling_ref"),
        )
        object.__setattr__(
            self,
            "candidate_stage",
            _enum(self.candidate_stage, CandidateStage, "candidate_stage"),
        )
        object.__setattr__(
            self,
            "provenance_refs",
            _exact_ref_tuple(self.provenance_refs, "provenance_refs", require_nonempty=True),
        )

    @property
    def logical_key(self) -> str:
        return f"{self.candidate_namespace}:{self.candidate_id}:g{self.snapshot_generation}"

    def governance_signature(self) -> tuple[str, ...]:
        return (
            self.candidate_kind.value,
            self.semantic_core_ref.key,
            self.semantic_schema_ref.key,
            self.negative_ceiling_ref.key,
            self.type_class_ceiling_ref.key,
            self.candidate_stage.value,
        )

    def as_material(self) -> Mapping[str, Any]:
        return {
            "contract_id": CONTROL_PLANE_CONTRACT_ID,
            "candidate_namespace": self.candidate_namespace,
            "candidate_id": self.candidate_id,
            "snapshot_generation": self.snapshot_generation,
            "predecessor_candidate_ref": (
                None
                if self.predecessor_candidate_ref is None
                else self.predecessor_candidate_ref.as_dict()
            ),
            "candidate_kind": self.candidate_kind.value,
            "semantic_core_ref": self.semantic_core_ref.as_dict(),
            "semantic_schema_ref": self.semantic_schema_ref.as_dict(),
            "evidence_admission_refs": [ref.as_dict() for ref in self.evidence_admission_refs],
            "negative_ceiling_ref": self.negative_ceiling_ref.as_dict(),
            "type_class_ceiling_ref": self.type_class_ceiling_ref.as_dict(),
            "candidate_stage": self.candidate_stage.value,
            "provenance_refs": [ref.as_dict() for ref in self.provenance_refs],
        }

    @property
    def ref(self) -> ExactRef:
        return _ref(SEMANTIC_CANDIDATE_REF_KIND, self.logical_key, self.as_material())

    def require_replay(self, expected_ref: ExactRef) -> SemanticCandidateRecord:
        require_replay(expected_ref, self.ref, "semantic candidate")
        return self


__all__ = [
    "SourceLocalIntakeRecord",
    "PositionSemanticCore",
    "PositionMaterializationRequest",
    "SemanticCandidateRecord",
]
