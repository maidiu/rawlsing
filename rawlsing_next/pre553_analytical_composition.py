"""C1 analytical composition: public I03/I05 -> exact possibility slice -> consumer.

This module composes already-authoritative objects while preserving their exact identities.
C1-01: direct scalar path (AT07).
C1-02: higher-order/joint/recursive extension (AT08-AT13).
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    DiscoveryResultReceipt,
    EmpiricalFact,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    ExactRef,
    Pre553IntegrityError,
    authority_ref,
    canonicalize,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_discovery_exact import ExactBoundedDiscoveryResult
from rawlsing_next.pre553_recursive_handoff import RecursiveBranchHandoff
from rawlsing_next.source_backed_positioned_subject_possibility import (
    ConditionerBinding,
    PositionedSubjectPossibilityModelRule,
    PositionedSubjectPossibilityQuery,
    PositionedSubjectPossibilityResult,
    PossibilitySliceEvidence,
    evaluate_positioned_subject_possibility,
    SpecificityLoss,
)

SLICE_PROJECTION_SCHEMA = "C1_POSSIBILITY_SLICE_PROJECTION@1"
SLICE_PROJECTION_SCHEMA_HASH = "c00e038dd2c1177bfc7842f12febef7b3e30b92bc421df244e2a8e3c4a20b17a"
SLICE_GEOMETRY_SCHEMA = "C1_POSSIBILITY_SLICE_GEOMETRY@1"
EVIDENCE_PREIMAGE_SCHEMA = "C1_POSITIONED_SUBJECT_SLICE_EVIDENCE_PREIMAGE@1"
EVIDENCE_CONTRACT_ID = "C1_POSITIONED_SUBJECT_SLICE_EVIDENCE@1"
WITNESS_KIND = "C1_CONDITION_VALUE_BINDING_WITNESS@2"
WITNESS_BINDING_MODE = "EXPLICIT_VALUE_BEARING_RELATION__NO_INFERENCE"
PRODUCER_ROUTE_DIRECT = "DIRECT_I03_TO_POSITIONED_SUBJECT"
PRODUCER_ROUTE_DISCOVERY = "I05_EXACT_BOUNDED_TO_POSITIONED_SUBJECT"
PRODUCER_ROUTE_RECURSIVE = "MX01R2_RECURSIVE_TO_POSITIONED_SUBJECT"

# Trusted in-process execution custody: populated only by the accepted compose
# boundary after actual owner validation. A subject view is compared to this
# retained original; it cannot obtain provenance by rehashing its own fields.
_NATIVE_COMPOSITION_CUSTODY: dict[str, tuple[Mapping[str, Any], Any]] = {}


def native_composition_original(composition_ref_or_hash: Any) -> Mapping[str, Any] | None:
    """Return the retained canonical original for an actual composed result."""
    key = (
        composition_ref_or_hash
        if isinstance(composition_ref_or_hash, str)
        else getattr(composition_ref_or_hash, "composed_result_identity_hash", None)
    )
    entry = _NATIVE_COMPOSITION_CUSTODY.get(key)
    return None if entry is None else entry[0]


def _retain_native_composition(result: "AnalyticalCompositionResult") -> None:
    material = canonicalize(result.identity_material())
    _NATIVE_COMPOSITION_CUSTODY[result.composed_result_identity_hash] = (material, result)


class AnalyticalCompositionError(Pre553IntegrityError):
    """Typed C1 composition failure; upstream owner errors are not laundered."""


class ConditionValueRelationMismatch(AnalyticalCompositionError):
    code = "CONDITION_VALUE_RELATION_MISMATCH"

    def __init__(self, detail: str) -> None:
        super().__init__(f"{self.code}: {detail}")


class JointTargetMismatch(AnalyticalCompositionError):
    code = "JOINT_TARGET_MISMATCH"

    def __init__(self, detail: str) -> None:
        super().__init__(f"{self.code}: {detail}")


class RecursiveLineageMismatch(AnalyticalCompositionError):
    code = "RECURSIVE_LINEAGE_MISMATCH"

    def __init__(self, detail: str) -> None:
        super().__init__(f"{self.code}: {detail}")


class DiscoveryConsumptionMismatch(AnalyticalCompositionError):
    code = "DISCOVERY_CONSUMPTION_MISMATCH"

    def __init__(self, detail: str) -> None:
        super().__init__(f"{self.code}: {detail}")


def _exact(value: ExactRef | Mapping[str, Any], name: str) -> ExactRef:
    return exact_ref(value, name)


def _authority(value: AuthorityRef | Mapping[str, Any], name: str) -> AuthorityRef:
    return authority_ref(value, name)


def _refs(values: Iterable[ExactRef | Mapping[str, Any]], name: str = "refs") -> tuple[ExactRef, ...]:
    out = tuple(_exact(value, name) for value in values)
    return tuple(sorted(set(out), key=lambda value: value.key))


def _auths(
    values: Iterable[AuthorityRef | Mapping[str, Any]], name: str = "authority_refs"
) -> tuple[AuthorityRef, ...]:
    out = tuple(_authority(value, name) for value in values)
    return tuple(sorted(set(out), key=lambda value: value.key))


def _binding_fingerprint(binding: ConditionerBinding) -> str:
    return semantic_hash(binding.material())


def _multi_binding_fingerprint(bindings: Sequence[ConditionerBinding]) -> str:
    return semantic_hash([canonicalize(b.material()) for b in bindings])


def _exact_fraction(numerator: int, denominator: int) -> Mapping[str, list[int]] | None:
    if denominator == 0:
        return None
    value = Fraction(numerator, denominator)
    return {"$exact_fraction": [value.numerator, value.denominator]}


def _all_bindings(query: PositionedSubjectPossibilityQuery) -> tuple[ConditionerBinding, ...]:
    return query.conditioner_bindings


def _actual_leaf(predicate: EmpiricalPredicate) -> Mapping[str, Any]:
    ast = canonicalize(predicate.predicate_ast)
    if ast.get("op") != "LEAF":
        raise ConditionValueRelationMismatch(
            "C1 direct path requires one value-bearing producer leaf"
        )
    if ast.get("leaf_type") != "SURVEY_RESPONSE_EVENT":
        raise ConditionValueRelationMismatch(
            "C1 requires SURVEY_RESPONSE_EVENT condition leaf"
        )
    if ast.get("operator") != "EQ" or "exact_value" not in ast:
        raise ConditionValueRelationMismatch("producer condition must be exact EQ")
    return ast


def _leaf_semantic_ref(node: Mapping[str, Any]) -> Any:
    """Exact semantic ref of a value-bearing leaf, keyed by its leaf type."""
    if node.get("leaf_type") == "EMPIRICAL_POSITION_COORDINATE":
        return node.get("coordinate_semantic_ref")
    return node.get("question_semantic_ref")


VALUE_BEARING_LEAF_TYPES = frozenset(
    {"SURVEY_RESPONSE_EVENT", "EMPIRICAL_POSITION_COORDINATE"}
)


def _actual_leaves(predicate: EmpiricalPredicate) -> list[Mapping[str, Any]]:
    """Extract all value-bearing leaves from a compound predicate.

    Governed empirical-position coordinates are value-bearing conditioners in
    their own right (the discovery owner exposes RESPONSE_X_COORDINATE
    families), so they participate in the same relation law as response leaves.
    """
    ast = canonicalize(predicate.predicate_ast)
    leaves: list[Mapping[str, Any]] = []

    def collect(node: Mapping[str, Any]) -> None:
        if node.get("op") == "LEAF" and node.get("leaf_type") in VALUE_BEARING_LEAF_TYPES:
            if node.get("operator") == "EQ" and "exact_value" in node:
                leaves.append(node)
        elif node.get("op") in {"AND", "OR", "NOT"}:
            for child in node.get("children", ()):
                collect(child)

    collect(ast)
    return leaves


class ConditionValueBindingWitness:
    """Exact custody witness; never a source of new comparability semantics.

    Supports both legacy single-conditioner format (C1-01 AT07) and 
    new multi-conditioner format (C1-02 AT08-AT13).
    """

    witness_ref: ExactRef
    identity_material: Mapping[str, Any]
    subject_condition_preimage_refs: tuple[ExactRef, ...]
    subject_condition_preimage_materials: tuple[Mapping[str, Any], ...]
    producer_predicate_leaf_refs: tuple[ExactRef, ...]
    producer_predicate_leaf_projections: tuple[Mapping[str, Any], ...]
    pairing_ground_truth_refs: tuple[ExactRef, ...]
    pairing_ground_truth_materials: tuple[Mapping[str, Any], ...]
    pairing_authority_refs: tuple[AuthorityRef, ...]

    def __init__(
        self,
        witness_ref: ExactRef,
        identity_material: Mapping[str, Any],
        # Legacy single-conditioner format (deprecated but supported)
        subject_condition_preimage_ref: ExactRef | None = None,
        subject_condition_preimage_material: Mapping[str, Any] | None = None,
        producer_predicate_leaf_ref: ExactRef | None = None,
        producer_predicate_leaf_projection: Mapping[str, Any] | None = None,
        pairing_ground_truth_ref: ExactRef | None = None,
        pairing_ground_truth_material: Mapping[str, Any] | None = None,
        pairing_authority_ref: AuthorityRef | None = None,
        # New multi-conditioner format
        subject_condition_preimage_refs: tuple[ExactRef, ...] | None = None,
        subject_condition_preimage_materials: tuple[Mapping[str, Any], ...] | None = None,
        producer_predicate_leaf_refs: tuple[ExactRef, ...] | None = None,
        producer_predicate_leaf_projections: tuple[Mapping[str, Any], ...] | None = None,
        pairing_ground_truth_refs: tuple[ExactRef, ...] | None = None,
        pairing_ground_truth_materials: tuple[Mapping[str, Any], ...] | None = None,
        pairing_authority_refs: tuple[AuthorityRef, ...] | None = None,
    ) -> None:
        # Detect legacy format
        if subject_condition_preimage_ref is not None:
            # Legacy format - convert to new format
            self.witness_ref = witness_ref
            self.identity_material = identity_material
            self.subject_condition_preimage_refs = (subject_condition_preimage_ref,)
            self.subject_condition_preimage_materials = (subject_condition_preimage_material,)
            self.producer_predicate_leaf_refs = (producer_predicate_leaf_ref,)
            self.producer_predicate_leaf_projections = (producer_predicate_leaf_projection,)
            self.pairing_ground_truth_refs = (pairing_ground_truth_ref,)
            self.pairing_ground_truth_materials = (pairing_ground_truth_material,)
            self.pairing_authority_refs = (pairing_authority_ref,)
        else:
            # New format
            self.witness_ref = witness_ref
            self.identity_material = identity_material
            self.subject_condition_preimage_refs = subject_condition_preimage_refs or ()
            self.subject_condition_preimage_materials = subject_condition_preimage_materials or ()
            self.producer_predicate_leaf_refs = producer_predicate_leaf_refs or ()
            self.producer_predicate_leaf_projections = producer_predicate_leaf_projections or ()
            self.pairing_ground_truth_refs = pairing_ground_truth_refs or ()
            self.pairing_ground_truth_materials = pairing_ground_truth_materials or ()
            self.pairing_authority_refs = pairing_authority_refs or ()

        # Validation
        if self.witness_ref.kind != WITNESS_KIND:
            raise AnalyticalCompositionError("unexpected condition witness kind")
        canonicalize(self.identity_material)
        for m in self.subject_condition_preimage_materials:
            canonicalize(m)
        for m in self.producer_predicate_leaf_projections:
            canonicalize(m)
        for m in self.pairing_ground_truth_materials:
            canonicalize(m)
        if len(self.subject_condition_preimage_refs) != len(self.subject_condition_preimage_materials):
            raise AnalyticalCompositionError("subject preimage ref/material count mismatch")
        if len(self.producer_predicate_leaf_refs) != len(self.producer_predicate_leaf_projections):
            raise AnalyticalCompositionError("producer leaf ref/projection count mismatch")
        if len(self.pairing_ground_truth_refs) != len(self.pairing_ground_truth_materials):
            raise AnalyticalCompositionError("pairing ground-truth ref/material count mismatch")
        if len(self.pairing_authority_refs) != len(self.subject_condition_preimage_refs):
            raise AnalyticalCompositionError("pairing authority count mismatch")

    # Legacy property accessors for backward compatibility
    @property
    def subject_condition_preimage_ref(self) -> ExactRef:
        return self.subject_condition_preimage_refs[0] if self.subject_condition_preimage_refs else None

    @property
    def subject_condition_preimage_material(self) -> Mapping[str, Any]:
        return self.subject_condition_preimage_materials[0] if self.subject_condition_preimage_materials else None

    @property
    def producer_predicate_leaf_ref(self) -> ExactRef:
        return self.producer_predicate_leaf_refs[0] if self.producer_predicate_leaf_refs else None

    @property
    def producer_predicate_leaf_projection(self) -> Mapping[str, Any]:
        return self.producer_predicate_leaf_projections[0] if self.producer_predicate_leaf_projections else None

    @property
    def pairing_ground_truth_ref(self) -> ExactRef:
        return self.pairing_ground_truth_refs[0] if self.pairing_ground_truth_refs else None

    @property
    def pairing_ground_truth_material(self) -> Mapping[str, Any]:
        return self.pairing_ground_truth_materials[0] if self.pairing_ground_truth_materials else None

    @property
    def pairing_authority_ref(self) -> AuthorityRef:
        return self.pairing_authority_refs[0] if self.pairing_authority_refs else None

    def verify_identity(self) -> None:
        if semantic_hash(self.identity_material) != self.witness_ref.content_hash:
            raise ConditionValueRelationMismatch("witness identity preimage hash mismatch")
        for ref, mat in zip(self.subject_condition_preimage_refs, self.subject_condition_preimage_materials):
            if semantic_hash(mat) != ref.content_hash:
                raise ConditionValueRelationMismatch("subject-condition preimage hash mismatch")
        for ref, proj in zip(self.producer_predicate_leaf_refs, self.producer_predicate_leaf_projections):
            if semantic_hash(proj) != ref.content_hash:
                raise ConditionValueRelationMismatch("producer predicate-leaf preimage hash mismatch")
        for ref, mat in zip(self.pairing_ground_truth_refs, self.pairing_ground_truth_materials):
            if semantic_hash(mat) != ref.content_hash:
                raise ConditionValueRelationMismatch("pairing ground-truth preimage hash mismatch")

    @classmethod
    def from_legacy(
        cls,
        witness_ref: ExactRef,
        identity_material: Mapping[str, Any],
        subject_condition_preimage_ref: ExactRef,
        subject_condition_preimage_material: Mapping[str, Any],
        producer_predicate_leaf_ref: ExactRef,
        producer_predicate_leaf_projection: Mapping[str, Any],
        pairing_ground_truth_ref: ExactRef,
        pairing_ground_truth_material: Mapping[str, Any],
        pairing_authority_ref: AuthorityRef,
    ) -> "ConditionValueBindingWitness":
        """Create witness from legacy single-conditioner format."""
        return cls(
            witness_ref=witness_ref,
            identity_material=identity_material,
            subject_condition_preimage_ref=subject_condition_preimage_ref,
            subject_condition_preimage_material=subject_condition_preimage_material,
            producer_predicate_leaf_ref=producer_predicate_leaf_ref,
            producer_predicate_leaf_projection=producer_predicate_leaf_projection,
            pairing_ground_truth_ref=pairing_ground_truth_ref,
            pairing_ground_truth_material=pairing_ground_truth_material,
            pairing_authority_ref=pairing_authority_ref,
        )

    def verify_identity(self) -> None:
        if semantic_hash(self.identity_material) != self.witness_ref.content_hash:
            raise ConditionValueRelationMismatch("witness identity preimage hash mismatch")
        for ref, mat in zip(self.subject_condition_preimage_refs, self.subject_condition_preimage_materials):
            if semantic_hash(mat) != ref.content_hash:
                raise ConditionValueRelationMismatch("subject-condition preimage hash mismatch")
        for ref, proj in zip(self.producer_predicate_leaf_refs, self.producer_predicate_leaf_projections):
            if semantic_hash(proj) != ref.content_hash:
                raise ConditionValueRelationMismatch("producer predicate-leaf preimage hash mismatch")
        for ref, mat in zip(self.pairing_ground_truth_refs, self.pairing_ground_truth_materials):
            if semantic_hash(mat) != ref.content_hash:
                raise ConditionValueRelationMismatch("pairing ground-truth preimage hash mismatch")


@dataclass(frozen=True)
class AnalyticalCompositionResult:
    analytical_state: str
    producer_route: str
    producer_query_ref: ExactRef
    producer_predicate_ref: ExactRef
    producer_fact_ref: ExactRef
    producer_fact_state: str
    producer_result: Any
    source_universe_refs: tuple[ExactRef, ...]
    release_refs: tuple[ExactRef, ...]
    consumer_query_ref: ExactRef
    consumer_binding_fingerprint: str
    condition_binding_witness_ref_or_hash: ExactRef
    ordered_target_refs: tuple[ExactRef, ...]
    target_arity_and_topology: Mapping[str, Any]
    target_domain_identity: str | None
    risk_set_ref: ExactRef
    risk_set_member_refs: tuple[ExactRef, ...]
    denominator_member_refs: tuple[ExactRef, ...]
    raw_denominator_support: int
    measure_kind: str
    measure_basis_ref: ExactRef
    weight_basis_id_or_null: str | None
    weight_design_estimand_context: Mapping[str, Any] | None
    complete_cell_geometry: tuple[Mapping[str, Any], ...]
    uncertainty_state: str
    coverage_state: str
    ancestry_refs: tuple[ExactRef, ...]
    authority_refs: tuple[AuthorityRef, ...]
    provenance_refs: tuple[ExactRef, ...]
    dependency_refs: tuple[ExactRef, ...]
    replay_refs: tuple[ExactRef, ...]
    possibility_slice_evidence_or_null: PossibilitySliceEvidence | None
    consumer_result_or_null: PositionedSubjectPossibilityResult | None
    consumer_model_rule_hash: str
    subject_condition_preimage_refs: tuple[ExactRef, ...]
    producer_predicate_leaf_refs: tuple[ExactRef, ...]
    pairing_ground_truth_refs: tuple[ExactRef, ...]
    slice_projection_schema_hash: str
    composed_result_identity_hash: str
    # C1-02 extensions
    discovery_receipt_refs: tuple[ExactRef, ...] = ()
    discovery_frontier_ref: ExactRef | None = None
    recursive_handoff_refs: tuple[ExactRef, ...] = ()
    recursive_lineage_refs: tuple[ExactRef, ...] = ()
    joint_component_count: int = 1
    joint_order_semantics: str = "SEMANTIC_ORDERED"

    def identity_material(self) -> Mapping[str, Any]:
        material = {
            "analytical_state": self.analytical_state,
            "producer_route": self.producer_route,
            "producer_query_ref": self.producer_query_ref.as_dict(),
            "producer_predicate_ref": self.producer_predicate_ref.as_dict(),
            "producer_fact_ref": self.producer_fact_ref.as_dict(),
            "producer_fact_state": self.producer_fact_state,
            "producer_result_envelope": (
                None
                if self.producer_result is None
                else {
                    "query_ref": self.producer_result.query_ref.as_dict(),
                    "source_scope_mode": self.producer_result.source_scope_mode,
                    "release_refs": [x.as_dict() for x in self.producer_result.release_refs],
                    "fact_refs": [x.ref.as_dict() for x in self.producer_result.facts],
                }
            ),
            "source_universe_refs": [x.as_dict() for x in self.source_universe_refs],
            "release_refs": [x.as_dict() for x in self.release_refs],
            "consumer_query_ref": self.consumer_query_ref.as_dict(),
            "consumer_binding_fingerprint": self.consumer_binding_fingerprint,
            "condition_binding_witness_ref_or_hash": self.condition_binding_witness_ref_or_hash.as_dict(),
            "ordered_target_refs": [x.as_dict() for x in self.ordered_target_refs],
            "target_arity_and_topology": canonicalize(self.target_arity_and_topology),
            "target_domain_identity": self.target_domain_identity,
            "risk_set_ref": self.risk_set_ref.as_dict(),
            "risk_set_member_refs": [x.as_dict() for x in self.risk_set_member_refs],
            "denominator_member_refs": [x.as_dict() for x in self.denominator_member_refs],
            "raw_denominator_support": self.raw_denominator_support,
            "measure_kind": self.measure_kind,
            "measure_basis_ref": self.measure_basis_ref.as_dict(),
            "weight_basis_id_or_null": self.weight_basis_id_or_null,
            "weight_design_estimand_context": canonicalize(self.weight_design_estimand_context),
            "complete_cell_geometry": [canonicalize(x) for x in self.complete_cell_geometry],
            "uncertainty_state": self.uncertainty_state,
            "coverage_state": self.coverage_state,
            "ancestry_refs": [x.as_dict() for x in self.ancestry_refs],
            "authority_refs": [x.as_dict() for x in self.authority_refs],
            "provenance_refs": [x.as_dict() for x in self.provenance_refs],
            "dependency_refs": [x.as_dict() for x in self.dependency_refs],
            "replay_refs": [x.as_dict() for x in self.replay_refs],
            "possibility_slice_evidence_ref_or_null": (
                None
                if self.possibility_slice_evidence_or_null is None
                else self.possibility_slice_evidence_or_null.evidence_ref.as_dict()
            ),
            "consumer_result_hash_or_null": (
                None
                if self.consumer_result_or_null is None
                else self.consumer_result_or_null.result_hash
            ),
            "consumer_model_rule_hash": self.consumer_model_rule_hash,
            "subject_condition_preimage_refs": [
                x.as_dict() for x in self.subject_condition_preimage_refs
            ],
            "producer_predicate_leaf_refs": [
                x.as_dict() for x in self.producer_predicate_leaf_refs
            ],
            "pairing_ground_truth_refs": [
                x.as_dict() for x in self.pairing_ground_truth_refs
            ],
            "slice_projection_schema_hash": self.slice_projection_schema_hash,
            # C1-02 extensions
            "discovery_receipt_refs": [x.as_dict() for x in self.discovery_receipt_refs],
            "discovery_frontier_ref": self.discovery_frontier_ref.as_dict() if self.discovery_frontier_ref else None,
            "recursive_handoff_refs": [x.as_dict() for x in self.recursive_handoff_refs],
            "recursive_lineage_refs": [x.as_dict() for x in self.recursive_lineage_refs],
            "joint_component_count": self.joint_component_count,
            "joint_order_semantics": self.joint_order_semantics,
        }
        return material


def _verify_witness(
    *,
    witness: ConditionValueBindingWitness,
    consumer_query: PositionedSubjectPossibilityQuery,
    bindings: Sequence[ConditionerBinding],
    empirical_query: EmpiricalQuerySpec,
    predicate: EmpiricalPredicate,
    release_ref: ExactRef,
) -> str:
    """Verify witness for multiple conditioners (new format) or single conditioner (legacy format)."""
    witness.verify_identity()
    actual_leaves = _actual_leaves(predicate)
    identity = canonicalize(witness.identity_material)

    # Detect legacy vs new format by identity material keys
    is_legacy = "consumer_binding_material" in identity
    
    if is_legacy:
        # Legacy format verification
        required = {
            "consumer_query_ref",
            "consumer_binding_material",
            "consumer_binding_fingerprint",
            "subject_condition_preimage_ref",
            "subject_condition_preimage_material",
            "producer_query_ref",
            "producer_predicate_ref",
            "producer_predicate_hash",
            "producer_predicate_leaf_ref",
            "producer_predicate_leaf_projection",
            "pairing_ground_truth_ref",
            "pairing_authority_ref",
            "source_universe_ref",
            "release_ref",
            "effective_time_or_interval",
            "binding_mode",
        }
        identity_keys = set(identity)
        if identity_keys != required:
            missing = sorted(required - identity_keys)
            extra = sorted(identity_keys - required)
            raise ConditionValueRelationMismatch(
                f"witness identity field set mismatch: missing={missing!r}; extra={extra!r}"
            )

        fingerprint = _binding_fingerprint(bindings[0])
        expected_fields = {
            "consumer_query_ref": consumer_query.ref.as_dict(),
            "consumer_binding_material": canonicalize(bindings[0].material()),
            "consumer_binding_fingerprint": fingerprint,
            "subject_condition_preimage_ref": witness.subject_condition_preimage_refs[0].as_dict(),
            "subject_condition_preimage_material": canonicalize(
                witness.subject_condition_preimage_materials[0]
            ),
            "producer_query_ref": empirical_query.ref.as_dict(),
            "producer_predicate_ref": predicate.ref.as_dict(),
            "producer_predicate_hash": predicate.predicate_hash,
            "producer_predicate_leaf_ref": witness.producer_predicate_leaf_refs[0].as_dict(),
            "producer_predicate_leaf_projection": canonicalize(
                witness.producer_predicate_leaf_projections[0]
            ),
            "pairing_ground_truth_ref": witness.pairing_ground_truth_refs[0].as_dict(),
            "pairing_authority_ref": witness.pairing_authority_refs[0].as_dict(),
            "source_universe_ref": consumer_query.source_universe_ref.as_dict(),
            "release_ref": release_ref.as_dict(),
            "effective_time_or_interval": canonicalize(bindings[0].effective_time_or_interval),
            "binding_mode": WITNESS_BINDING_MODE,
        }
        for key, value in expected_fields.items():
            if canonicalize(identity[key]) != canonicalize(value):
                raise ConditionValueRelationMismatch(f"witness field mismatch: {key}")

        subject = canonicalize(witness.subject_condition_preimage_materials[0])
        if subject.get("empirical_semantic_ref") != bindings[0].empirical_coordinate_ref.as_dict():
            raise ConditionValueRelationMismatch(
                "subject semantic ref != consumer binding coordinate"
            )
        if bindings[0].subject_fact_ref != witness.subject_condition_preimage_refs[0]:
            raise ConditionValueRelationMismatch(
                "consumer subject fact != frozen subject preimage"
            )
        if bindings[0].comparability_authority_ref != witness.pairing_authority_refs[0]:
            raise ConditionValueRelationMismatch(
                "consumer comparability authority != pairing authority"
            )
        if bindings[0].source_universe_ref != consumer_query.source_universe_ref:
            raise ConditionValueRelationMismatch("binding source universe mismatch")
        if bindings[0].release_ref != release_ref:
            raise ConditionValueRelationMismatch("binding release mismatch")

        frozen_leaf = canonicalize(witness.producer_predicate_leaf_projections[0])
        for key in ("leaf_type", "question_semantic_ref", "operator", "exact_value"):
            if frozen_leaf.get(key) != actual_leaves[0].get(key):
                raise ConditionValueRelationMismatch(
                    f"actual producer leaf mismatch: {key}"
                )
        if frozen_leaf.get("question_semantic_ref") != subject.get("empirical_semantic_ref"):
            raise ConditionValueRelationMismatch("producer/subject semantic ref mismatch")
        if frozen_leaf.get("exact_value") != subject.get("exact_value"):
            raise ConditionValueRelationMismatch("producer/subject exact value mismatch")

        pair = canonicalize(witness.pairing_ground_truth_materials[0])
        if pair.get("subject_preimage_ref") != witness.subject_condition_preimage_refs[0].as_dict():
            raise ConditionValueRelationMismatch("pairing subject ref mismatch")
        if pair.get("predicate_leaf_preimage_ref") != witness.producer_predicate_leaf_refs[0].as_dict():
            raise ConditionValueRelationMismatch("pairing predicate leaf ref mismatch")
        if pair.get("required_semantic_ref") != subject.get("empirical_semantic_ref"):
            raise ConditionValueRelationMismatch("pairing semantic ref mismatch")
        if pair.get("required_exact_value") != subject.get("exact_value"):
            raise ConditionValueRelationMismatch("pairing exact value mismatch")
    else:
        # New multi-conditioner format verification
        required_base = {
            "consumer_query_ref",
            "consumer_binding_materials",
            "consumer_binding_fingerprint",
            "producer_query_ref",
            "producer_predicate_ref",
            "producer_predicate_hash",
            "producer_predicate_leaf_refs",
            "producer_predicate_leaf_projections",
            "pairing_ground_truth_refs",
            "pairing_ground_truth_materials",
            "pairing_authority_refs",
            "source_universe_ref",
            "release_ref",
            "effective_time_or_intervals",
            "binding_mode",
        }
        identity_keys = set(identity)
        if identity_keys != required_base:
            missing = sorted(required_base - identity_keys)
            extra = sorted(identity_keys - required_base)
            raise ConditionValueRelationMismatch(
                f"witness identity field set mismatch: missing={missing!r}; extra={extra!r}"
            )

        fingerprint = _multi_binding_fingerprint(bindings)
        expected_fields = {
            "consumer_query_ref": consumer_query.ref.as_dict(),
            "consumer_binding_materials": [canonicalize(b.material()) for b in bindings],
            "consumer_binding_fingerprint": fingerprint,
            "producer_query_ref": empirical_query.ref.as_dict(),
            "producer_predicate_ref": predicate.ref.as_dict(),
            "producer_predicate_hash": predicate.predicate_hash,
            "producer_predicate_leaf_refs": [ref.as_dict() for ref in witness.producer_predicate_leaf_refs],
            "producer_predicate_leaf_projections": [canonicalize(p) for p in witness.producer_predicate_leaf_projections],
            "pairing_ground_truth_refs": [ref.as_dict() for ref in witness.pairing_ground_truth_refs],
            "pairing_ground_truth_materials": [canonicalize(m) for m in witness.pairing_ground_truth_materials],
            "pairing_authority_refs": [ref.as_dict() for ref in witness.pairing_authority_refs],
            "source_universe_ref": consumer_query.source_universe_ref.as_dict(),
            "release_ref": release_ref.as_dict(),
            "effective_time_or_intervals": [canonicalize(b.effective_time_or_interval) for b in bindings],
            "binding_mode": WITNESS_BINDING_MODE,
        }
        for key, value in expected_fields.items():
            if canonicalize(identity[key]) != canonicalize(value):
                raise ConditionValueRelationMismatch(f"witness field mismatch: {key}")

        if len(bindings) != len(witness.subject_condition_preimage_refs):
            raise ConditionValueRelationMismatch("binding/subject preimage count mismatch")
        if len(bindings) != len(witness.producer_predicate_leaf_refs):
            raise ConditionValueRelationMismatch("binding/producer leaf count mismatch")
        if len(bindings) != len(witness.pairing_ground_truth_refs):
            raise ConditionValueRelationMismatch("binding/pairing count mismatch")
        if len(bindings) != len(witness.pairing_authority_refs):
            raise ConditionValueRelationMismatch("binding/pairing authority count mismatch")

        for i, binding in enumerate(bindings):
            subject = canonicalize(witness.subject_condition_preimage_materials[i])
            if subject.get("empirical_semantic_ref") != binding.empirical_coordinate_ref.as_dict():
                raise ConditionValueRelationMismatch(f"conditioner {i}: subject semantic ref != consumer binding coordinate")
            if binding.subject_fact_ref != witness.subject_condition_preimage_refs[i]:
                raise ConditionValueRelationMismatch(f"conditioner {i}: consumer subject fact != frozen subject preimage")
            if binding.comparability_authority_ref != witness.pairing_authority_refs[i]:
                raise ConditionValueRelationMismatch(f"conditioner {i}: consumer comparability authority != pairing authority")
            if binding.source_universe_ref != consumer_query.source_universe_ref:
                raise ConditionValueRelationMismatch(f"conditioner {i}: binding source universe mismatch")
            if binding.release_ref != release_ref:
                raise ConditionValueRelationMismatch(f"conditioner {i}: binding release mismatch")

        for i, binding in enumerate(bindings):
            frozen_leaf = canonicalize(witness.producer_predicate_leaf_projections[i])
            frozen_ref = frozen_leaf.get("coordinate_semantic_ref") if (
                frozen_leaf.get("leaf_type") == "EMPIRICAL_POSITION_COORDINATE"
            ) else frozen_leaf.get("question_semantic_ref")
            match_found = False
            for actual_leaf in actual_leaves:
                if (frozen_ref == _leaf_semantic_ref(actual_leaf) and
                    frozen_leaf.get("exact_value") == actual_leaf.get("exact_value")):
                    match_found = True
                    for key in ("leaf_type", "operator", "exact_value"):
                        if frozen_leaf.get(key) != actual_leaf.get(key):
                            raise ConditionValueRelationMismatch(f"conditioner {i}: actual producer leaf mismatch: {key}")
                    if _leaf_semantic_ref(frozen_leaf) != _leaf_semantic_ref(actual_leaf):
                        raise ConditionValueRelationMismatch(
                            f"conditioner {i}: actual producer leaf semantic ref mismatch"
                        )
                    break
            if not match_found:
                raise ConditionValueRelationMismatch(f"conditioner {i}: no matching producer leaf found")

            # Pairing-ground-truth semantics must be checked on the SUCCESSFUL
            # path. These four comparisons were previously indented under the
            # raise above, which made them unreachable and let a hash-consistent
            # but semantically false pairing relation pass verification.
            # `subject` is re-bound here deliberately: the earlier loop variable
            # would otherwise leak the last conditioner's subject material.
            subject = canonicalize(witness.subject_condition_preimage_materials[i])
            pair = canonicalize(witness.pairing_ground_truth_materials[i])
            if pair.get("subject_preimage_ref") != witness.subject_condition_preimage_refs[i].as_dict():
                raise ConditionValueRelationMismatch(f"conditioner {i}: pairing subject ref mismatch")
            if pair.get("predicate_leaf_preimage_ref") != witness.producer_predicate_leaf_refs[i].as_dict():
                raise ConditionValueRelationMismatch(f"conditioner {i}: pairing predicate leaf ref mismatch")
            if pair.get("required_semantic_ref") != subject.get("empirical_semantic_ref"):
                raise ConditionValueRelationMismatch(f"conditioner {i}: pairing semantic ref mismatch")
            if pair.get("required_exact_value") != subject.get("exact_value"):
                raise ConditionValueRelationMismatch(f"conditioner {i}: pairing exact value mismatch")
    return fingerprint


def _validate_joint_grain(
    *,
    empirical_query: EmpiricalQuerySpec,
    consumer_query: PositionedSubjectPossibilityQuery,
    release_refs: tuple[ExactRef, ...],
) -> None:
    """Validate joint/multi-component target configuration."""
    universes = _refs(empirical_query.empirical_universe_refs, "empirical_universe_refs")
    targets = _refs(empirical_query.target_refs, "target_refs")
    if len(universes) != 1:
        raise AnalyticalCompositionError("C1 joint path requires SINGLE_UNIVERSE producer scope")
    if universes[0] != consumer_query.source_universe_ref:
        raise AnalyticalCompositionError("SOURCE_UNIVERSE_MISMATCH")
    if len(release_refs) != 1 or release_refs[0] != consumer_query.release_ref:
        raise AnalyticalCompositionError("SOURCE_RELEASE_MISMATCH")
    if len(targets) != len(consumer_query.conditioner_bindings):
        raise JointTargetMismatch("target component count must match conditioner count")
    topology = canonicalize(empirical_query.target_arity_and_topology)
    if topology.get("arity") != len(targets):
        raise JointTargetMismatch("target arity mismatch")
    components = topology.get("components", ())
    if len(components) != len(targets):
        raise JointTargetMismatch("component count mismatch")
    for i, (target_ref, component) in enumerate(zip(targets, components)):
        if component.get("target_ref") != target_ref.as_dict():
            raise JointTargetMismatch(f"component {i} target_ref mismatch")


def _validate_discovery_consumption(
    *,
    discovery_result: ExactBoundedDiscoveryResult,
    consumer_query: PositionedSubjectPossibilityQuery,
    receipt_ref: ExactRef,
) -> tuple[EmpiricalFact, EmpiricalPredicate, EmpiricalQuerySpec]:
    """Validate and extract producer objects from a discovery receipt."""
    # Find the receipt
    receipt = None
    for r in discovery_result.receipts:
        if r.ref == receipt_ref:
            receipt = r
            break
    if receipt is None:
        raise DiscoveryConsumptionMismatch("receipt not found in discovery result")
    if receipt.typed_state != "DISCOVERED_RESULT_SUPPORTED":
        raise DiscoveryConsumptionMismatch("receipt is not supported")

    pred_by_ref = {p.ref: p for p in discovery_result.executed_predicates}
    query_by_ref = {q.ref: q for q in discovery_result.executed_queries}
    fact_by_ref = {f.ref: f for f in discovery_result.empirical_facts}

    predicate_ref = _exact(receipt.winning_predicate_ref, "winning_predicate_ref")
    predicate = pred_by_ref.get(predicate_ref)
    if predicate is None:
        raise DiscoveryConsumptionMismatch("winning predicate not found in discovery result")

    if not receipt.empirical_fact_refs:
        raise DiscoveryConsumptionMismatch("receipt has no empirical facts")
    # Joint receipts also carry marginal facts under the winning predicate.
    # Select the producer-declared primary query, never the fact-list order.
    roles = receipt.candidate_identity.get("query_roles", ())
    primary_queries = {
        _exact(role["query_ref"], "primary query_ref")
        for role in roles
        if role.get("role") in {"JOINT", "CONDITION", "BASE"}
        and _exact(role["predicate_ref"], "primary predicate_ref") == predicate.ref
    }
    if len(primary_queries) > 1:
        raise DiscoveryConsumptionMismatch("ambiguous primary discovery query")
    matches = []
    for fact_ref in receipt.empirical_fact_refs:
        candidate = fact_by_ref.get(exact_ref(fact_ref))
        if candidate is None:
            continue
        if _exact(candidate.condition_predicate_ref, "condition_predicate_ref") != predicate.ref:
            continue
        query_ref = _exact(candidate.empirical_query_spec_ref, "empirical_query_spec_ref")
        if primary_queries and query_ref not in primary_queries:
            continue
        matches.append(candidate)
    if len(matches) != 1:
        raise DiscoveryConsumptionMismatch("missing or ambiguous discovery fact/query association")
    fact = matches[0]
    query_ref = _exact(fact.empirical_query_spec_ref, "empirical_query_spec_ref")
    query = query_by_ref.get(query_ref)
    if query is None:
        raise DiscoveryConsumptionMismatch("query not found for fact")
    if _exact(query.condition_predicate_ref, "query condition_predicate_ref") != predicate.ref:
        raise DiscoveryConsumptionMismatch("discovery query predicate mismatch")

    return fact, predicate, query


def _validate_recursive_lineage(
    *,
    handoff: RecursiveBranchHandoff,
    consumer_query: PositionedSubjectPossibilityQuery,
) -> tuple[ExactRef, ...]:
    """Validate recursive lineage and return the full owner-native ancestry.

    A depth-two continuation reaches its generation through the persisted branch,
    so the ancestry is not only the immediate parent: the discovered grammar atom
    carries the exact ancestor refs of every earlier generation. Those refs are
    part of the retained custody material and are closed here.
    """
    lineage: list[ExactRef] = [handoff.ref, handoff.immediate_parent_branch_ref]
    seen = {ref.key for ref in lineage}

    def absorb(values: Any) -> None:
        if not isinstance(values, (list, tuple)):
            return
        for value in values:
            try:
                ref = exact_ref(value)
            except AnalyticalCompositionError:
                continue
            if ref.key not in seen:
                seen.add(ref.key)
                lineage.append(ref)

    scope = handoff.scope_context
    if isinstance(scope, Mapping):
        absorb(scope.get("parent_branch_refs"))
    definition = handoff.candidate_universe_definition
    if isinstance(definition, Mapping):
        for atom in definition.get("atoms", ()):
            if isinstance(atom, Mapping):
                absorb(atom.get("ancestry_refs"))
    return tuple(lineage)


def _validate_direct_grain(
    *,
    empirical_query: EmpiricalQuerySpec,
    consumer_query: PositionedSubjectPossibilityQuery,
    release_refs: tuple[ExactRef, ...],
) -> None:
    universes = _refs(empirical_query.empirical_universe_refs, "empirical_universe_refs")
    targets = _refs(empirical_query.target_refs, "target_refs")
    if len(universes) != 1:
        raise AnalyticalCompositionError("C1-01 requires SINGLE_UNIVERSE producer scope")
    if universes[0] != consumer_query.source_universe_ref:
        raise AnalyticalCompositionError("SOURCE_UNIVERSE_MISMATCH")
    if len(release_refs) != 1 or release_refs[0] != consumer_query.release_ref:
        raise AnalyticalCompositionError("SOURCE_RELEASE_MISMATCH")
    if len(targets) < 1 or targets[0] != consumer_query.target_ref:
        raise AnalyticalCompositionError("TARGET_TOPOLOGY_OR_DOMAIN_MISMATCH")
    topology = canonicalize(empirical_query.target_arity_and_topology)
    if topology.get("arity") != len(targets) or len(topology.get("components", ())) != len(targets):
        raise AnalyticalCompositionError("TARGET_TOPOLOGY_OR_DOMAIN_MISMATCH")
    if topology["components"][0].get("target_ref") != consumer_query.target_ref.as_dict():
        raise AnalyticalCompositionError("TARGET_TOPOLOGY_OR_DOMAIN_MISMATCH")


def _supported_geometry(
    *,
    fact: EmpiricalFact,
    empirical_query: EmpiricalQuerySpec,
    predicate: EmpiricalPredicate,
    witness: ConditionValueBindingWitness,
    consumer_query: PositionedSubjectPossibilityQuery,
    is_joint: bool = False,
) -> Mapping[str, Any]:
    denominator = fact.raw_denominator_support
    if denominator <= 0:
        raise AnalyticalCompositionError("SUPPORTED fact must retain positive denominator")

    cells = []
    for cell in canonicalize(fact.target_topology)["complete_cell_semantic_projection"]:
        raw = cell["raw_numerator_support"]
        cells.append(
            {
                "cell": cell["cell"],
                "cell_state": cell["cell_state"],
                "raw_numerator_support": raw,
                "weighted_numerator_support_if_authorized": cell.get(
                    "weighted_numerator_support_if_authorized"
                ),
                "raw_probability_exact_fraction": _exact_fraction(raw, denominator),
                "weighted_probability_exact_fraction_if_authorized": None,
            }
        )

    topology = canonicalize(empirical_query.target_arity_and_topology)
    measure_kind = fact.measure_kind
    weight_basis = empirical_query.requested_output_grain.get("weight_basis_id")

    if is_joint:
        # For joint targets, preserve all component materials
        components = []
        for component in topology["components"]:
            components.append(component)
        target_info = {
            "target_refs": [t.as_dict() for t in _refs(empirical_query.target_refs, "target_refs")],
            "arity": topology["arity"],
            "joint_order_semantics": topology["joint_order_semantics"],
            "components": components,
            "target_domain_identity": fact.target_domain_identity,
        }
    else:
        component = topology["components"][0]
        target_ref = _exact(empirical_query.target_refs[0], "target_ref")
        target_info = {
            "target_ref": target_ref.as_dict(),
            "arity": topology["arity"],
            "joint_order_semantics": topology["joint_order_semantics"],
            "component_material": component,
            "target_domain_identity": fact.target_domain_identity,
        }

    return {
        "schema": SLICE_GEOMETRY_SCHEMA,
        "source_fact_ref": fact.ref.as_dict(),
        "producer_query_ref": empirical_query.ref.as_dict(),
        "condition_predicate_ref": predicate.ref.as_dict(),
        "condition_value_witness_ref": witness.witness_ref.as_dict(),
        "target": target_info,
        "denominator": {
            "risk_set_ref": _exact(fact.risk_set_ref, "risk_set_ref").as_dict(),
            "risk_set_type": fact.risk_set_type,
            "risk_set_member_refs": [
                x.as_dict() for x in _refs(fact.risk_set_member_refs, "risk_set_member_refs")
            ],
            "denominator_member_refs": [
                x.as_dict()
                for x in _refs(fact.denominator_member_refs, "denominator_member_refs")
            ],
            "raw_denominator_support": denominator,
            "weighted_denominator_support_if_authorized": fact.weighted_denominator_support_if_authorized,
        },
        "measure": {
            "measure_kind": measure_kind,
            "measure_basis_ref": _exact(
                fact.measure_basis_ref, "measure_basis_ref"
            ).as_dict(),
            "weight_basis_id_or_null": weight_basis,
            "weight_design_estimand_context": None,
        },
        "cells": cells,
    }


def _build_evidence(
    *,
    fact: EmpiricalFact,
    empirical_query: EmpiricalQuerySpec,
    predicate: EmpiricalPredicate,
    consumer_query: PositionedSubjectPossibilityQuery,
    witness: ConditionValueBindingWitness,
    is_joint: bool = False,
    discovery_receipt_refs: tuple[ExactRef, ...] = (),
    recursive_handoff_refs: tuple[ExactRef, ...] = (),
) -> PossibilitySliceEvidence:
    geometry = _supported_geometry(
        fact=fact,
        empirical_query=empirical_query,
        predicate=predicate,
        witness=witness,
        consumer_query=consumer_query,
        is_joint=is_joint,
    )

    # Detect legacy format by identity material keys
    is_legacy = "subject_condition_preimage_ref" in canonicalize(witness.identity_material)
    
    if is_legacy:
        # Legacy provenance format for C1-01 backward compatibility
        provenance_items = [
            fact.ref,
            empirical_query.ref,
            predicate.ref,
            _exact(fact.replay_ref, "replay_ref"),
            witness.witness_ref,
            witness.subject_condition_preimage_refs[0],
            witness.pairing_ground_truth_refs[0],
        ]
    else:
        # New format provenance
        provenance_items = [
            fact.ref,
            empirical_query.ref,
            predicate.ref,
            _exact(fact.replay_ref, "replay_ref"),
            witness.witness_ref,
        ]
        provenance_items.extend(witness.subject_condition_preimage_refs)
        provenance_items.extend(witness.producer_predicate_leaf_refs)
        provenance_items.extend(witness.pairing_ground_truth_refs)
        provenance_items.extend(discovery_receipt_refs)
        provenance_items.extend(recursive_handoff_refs)
    
    provenance = _refs(provenance_items, "evidence_provenance")
    auth_items = list(fact.authority_snapshot_refs)
    auth_items.extend(witness.pairing_authority_refs)
    authorities = _auths(auth_items, "evidence_authorities")
    preimage = {
        "schema": EVIDENCE_PREIMAGE_SCHEMA,
        "contract_id": EVIDENCE_CONTRACT_ID,
        "source_universe_ref": consumer_query.source_universe_ref.as_dict(),
        "release_ref": consumer_query.release_ref.as_dict(),
        "target_ref": consumer_query.target_ref.as_dict(),
        "retained_conditioner_ids": list(consumer_query.conditioner_ids),
        "evidence_state": "SUPPORTED",
        "geometry": geometry,
        "raw_support": fact.raw_denominator_support,
        "uncertainty_state": fact.uncertainty_method_or_typed_state,
        "provenance_refs": [x.as_dict() for x in provenance],
        "authority_refs": [x.as_dict() for x in authorities],
    }
    digest = semantic_hash(preimage)
    evidence_ref = ExactRef(
        EVIDENCE_CONTRACT_ID,
        f"urn:rawlsing:c1:positioned-subject-slice-evidence:sha256:{digest}",
        digest,
    )
    return PossibilitySliceEvidence(
        evidence_ref=evidence_ref,
        source_universe_ref=consumer_query.source_universe_ref,
        release_ref=consumer_query.release_ref,
        target_ref=consumer_query.target_ref,
        retained_conditioner_ids=consumer_query.conditioner_ids,
        evidence_state="SUPPORTED",
        geometry=geometry,
        raw_support=fact.raw_denominator_support,
        uncertainty_state=fact.uncertainty_method_or_typed_state,
        provenance_refs=provenance,
        authority_refs=authorities,
    )


def _selected_fact(result: Any, empirical_query: EmpiricalQuerySpec) -> EmpiricalFact:
    if result.query_ref != empirical_query.ref:
        raise AnalyticalCompositionError(
            "producer QueryExecutionResult query_ref mismatch"
        )
    facts = tuple(result.facts)
    if len(facts) != 1:
        raise AnalyticalCompositionError("C1 direct path requires exactly one producer fact")
    fact = facts[0]
    if _exact(fact.empirical_query_spec_ref, "empirical_query_spec_ref") != empirical_query.ref:
        raise AnalyticalCompositionError("producer fact/query identity mismatch")
    return fact


def compose_positioned_subject_possibility(
    *,
    repository: Any,
    empirical_query: EmpiricalQuerySpec,
    predicate: EmpiricalPredicate,
    authority_registry: Any,
    release_refs: Iterable[ExactRef],
    consumer_query: PositionedSubjectPossibilityQuery,
    model_rule: PositionedSubjectPossibilityModelRule,
    condition_binding_witness: ConditionValueBindingWitness,
    # C1-02 optional parameters
    discovery_result: ExactBoundedDiscoveryResult | None = None,
    discovery_receipt_ref: ExactRef | None = None,
    recursive_handoff: RecursiveBranchHandoff | None = None,
) -> AnalyticalCompositionResult:
    """Execute the C1 analytical composition slice.

    Supports three producer routes:
    - DIRECT_I03_TO_POSITIONED_SUBJECT (C1-01, AT07)
    - I05_EXACT_BOUNDED_TO_POSITIONED_SUBJECT (C1-02, AT08-AT10)
    - MX01R2_RECURSIVE_TO_POSITIONED_SUBJECT (C1-02, AT11)
    """

    release_refs = _refs(release_refs, "release_refs")
    bindings = _all_bindings(consumer_query)

    # Determine producer route
    if recursive_handoff is not None:
        producer_route = PRODUCER_ROUTE_RECURSIVE
        _validate_recursive_consumption(recursive_handoff, consumer_query, predicate, empirical_query)
        producer_result = execute_empirical_query(
            repository=repository,
            query=empirical_query,
            predicate=predicate,
            authority_registry=authority_registry,
            release_refs=release_refs,
        )
        fact = _selected_fact(producer_result, empirical_query)
        discovery_receipt_refs = ()
        recursive_handoff_refs = (recursive_handoff.ref,)
        recursive_lineage_refs = _validate_recursive_lineage(handoff=recursive_handoff, consumer_query=consumer_query)
        coverage_state = "RECURSIVE_DEPTH_CONTINUATION"
        joint_component_count = len(empirical_query.target_refs)
        joint_order_semantics = canonicalize(empirical_query.target_arity_and_topology).get("joint_order_semantics", "SEMANTIC_ORDERED")

    elif discovery_result is not None and discovery_receipt_ref is not None:
        producer_route = PRODUCER_ROUTE_DISCOVERY
        fact, predicate, empirical_query = _validate_discovery_consumption(
            discovery_result=discovery_result,
            consumer_query=consumer_query,
            receipt_ref=discovery_receipt_ref,
        )
        discovery_receipt_refs = (discovery_receipt_ref,)
        recursive_handoff_refs = ()
        recursive_lineage_refs = ()
        coverage_state = "DISCOVERY_EXACT_FRONTIER"
        joint_component_count = len(empirical_query.target_refs)
        joint_order_semantics = canonicalize(empirical_query.target_arity_and_topology).get("joint_order_semantics", "SEMANTIC_ORDERED")

    else:
        producer_route = PRODUCER_ROUTE_DIRECT
        _validate_direct_grain(
            empirical_query=empirical_query,
            consumer_query=consumer_query,
            release_refs=release_refs,
        )
        producer_result = execute_empirical_query(
            repository=repository,
            query=empirical_query,
            predicate=predicate,
            authority_registry=authority_registry,
            release_refs=release_refs,
        )
        fact = _selected_fact(producer_result, empirical_query)
        discovery_receipt_refs = ()
        recursive_handoff_refs = ()
        recursive_lineage_refs = ()
        coverage_state = "DIRECT_EXACT_SINGLE_QUERY"
        topology = canonicalize(empirical_query.target_arity_and_topology)
        joint_component_count = len(topology.get("components", ()))
        joint_order_semantics = topology.get("joint_order_semantics", "SEMANTIC_ORDERED")

    fingerprint = _verify_witness(
        witness=condition_binding_witness,
        consumer_query=consumer_query,
        bindings=bindings,
        empirical_query=empirical_query,
        predicate=predicate,
        release_ref=release_refs[0],
    )

    # Validate fact identity
    if _exact(fact.condition_predicate_ref, "condition_predicate_ref") != predicate.ref:
        raise AnalyticalCompositionError("producer fact predicate mismatch")
    if _exact(fact.risk_set_ref, "risk_set_ref") != _exact(
        empirical_query.risk_set_ref, "query.risk_set_ref"
    ):
        raise AnalyticalCompositionError("DENOMINATOR_IDENTITY_MISMATCH")
    if _exact(fact.measure_basis_ref, "measure_basis_ref") != _exact(
        empirical_query.measure_basis_ref, "query.measure_basis_ref"
    ):
        raise AnalyticalCompositionError("MEASURE_IDENTITY_MISMATCH")
    if _refs(fact.empirical_universe_refs, "fact.empirical_universe_refs") != _refs(
        empirical_query.empirical_universe_refs, "query.empirical_universe_refs"
    ):
        raise AnalyticalCompositionError("SOURCE_UNIVERSE_MISMATCH")

    is_joint = joint_component_count > 1
    evidence = None
    consumer_result = None
    geometry = ()
    if fact.typed_state == "SUPPORTED":
        evidence = _build_evidence(
            fact=fact,
            empirical_query=empirical_query,
            predicate=predicate,
            consumer_query=consumer_query,
            witness=condition_binding_witness,
            is_joint=is_joint,
            discovery_receipt_refs=discovery_receipt_refs,
            recursive_handoff_refs=recursive_handoff_refs,
        )
        geometry = tuple(canonicalize(evidence.geometry)["cells"])
        consumer_result = evaluate_positioned_subject_possibility(
            query=consumer_query,
            rule=model_rule,
            evidence=(evidence,),
        )

    fact_risk_ref = _exact(fact.risk_set_ref, "risk_set_ref")
    fact_measure_ref = _exact(fact.measure_basis_ref, "measure_basis_ref")
    risk_members = _refs(
        getattr(fact, "risk_set_member_refs", ()), "risk_set_member_refs"
    )
    denominator_members = _refs(
        getattr(fact, "denominator_member_refs", ()), "denominator_member_refs"
    )
    replay_refs = _refs((_exact(fact.replay_ref, "replay_ref"),), "replay_refs")
    provenance = _refs(
        fact.source_empirical_provenance_refs, "source_empirical_provenance_refs"
    )
    dependencies = _refs(fact.dependency_refs, "dependency_refs")
    auth_items = list(fact.authority_snapshot_refs)
    auth_items.extend(condition_binding_witness.pairing_authority_refs)
    authorities = _auths(auth_items, "authority_refs")
    ordered_targets = _refs(empirical_query.target_refs, "target_refs")
    measure_kind = getattr(
        fact, "measure_kind", empirical_query.requested_output_grain.get("measure_kind")
    )
    weight_basis = empirical_query.requested_output_grain.get("weight_basis_id")

    kwargs = dict(
        analytical_state=fact.typed_state,
        producer_route=producer_route,
        producer_query_ref=producer_result.query_ref if producer_route == PRODUCER_ROUTE_DIRECT else empirical_query.ref,
        producer_predicate_ref=predicate.ref,
        producer_fact_ref=fact.ref,
        producer_fact_state=fact.typed_state,
        producer_result=producer_result if producer_route == PRODUCER_ROUTE_DIRECT else None,
        source_universe_refs=_refs(
            fact.empirical_universe_refs, "fact.empirical_universe_refs"
        ),
        release_refs=release_refs,
        consumer_query_ref=consumer_query.ref,
        consumer_binding_fingerprint=fingerprint,
        condition_binding_witness_ref_or_hash=condition_binding_witness.witness_ref,
        ordered_target_refs=ordered_targets,
        target_arity_and_topology=canonicalize(empirical_query.target_arity_and_topology),
        target_domain_identity=getattr(fact, "target_domain_identity", None),
        risk_set_ref=fact_risk_ref,
        risk_set_member_refs=risk_members,
        denominator_member_refs=denominator_members,
        raw_denominator_support=fact.raw_denominator_support,
        measure_kind=measure_kind,
        measure_basis_ref=fact_measure_ref,
        weight_basis_id_or_null=weight_basis,
        weight_design_estimand_context=None,
        complete_cell_geometry=geometry,
        uncertainty_state=fact.uncertainty_method_or_typed_state,
        coverage_state=coverage_state,
        ancestry_refs=recursive_lineage_refs,
        authority_refs=authorities,
        provenance_refs=provenance,
        dependency_refs=dependencies,
        replay_refs=replay_refs,
        possibility_slice_evidence_or_null=evidence,
        consumer_result_or_null=consumer_result,
        consumer_model_rule_hash=model_rule.rule_hash,
        subject_condition_preimage_refs=condition_binding_witness.subject_condition_preimage_refs,
        producer_predicate_leaf_refs=condition_binding_witness.producer_predicate_leaf_refs,
        pairing_ground_truth_refs=condition_binding_witness.pairing_ground_truth_refs,
        slice_projection_schema_hash=SLICE_PROJECTION_SCHEMA_HASH,
        discovery_receipt_refs=discovery_receipt_refs,
        discovery_frontier_ref=discovery_result.evaluated_frontier_ref if discovery_result else None,
        recursive_handoff_refs=recursive_handoff_refs,
        recursive_lineage_refs=recursive_lineage_refs,
        joint_component_count=joint_component_count,
        joint_order_semantics=joint_order_semantics,
    )
    provisional = AnalyticalCompositionResult(
        **kwargs, composed_result_identity_hash="0" * 64
    )
    result = AnalyticalCompositionResult(
        **kwargs,
        composed_result_identity_hash=semantic_hash(provisional.identity_material()),
    )
    _retain_native_composition(result)
    return result


def _validate_recursive_consumption(
    handoff: RecursiveBranchHandoff,
    consumer_query: PositionedSubjectPossibilityQuery,
    predicate: EmpiricalPredicate,
    empirical_query: EmpiricalQuerySpec,
) -> None:
    """Validate that the recursive handoff matches the consumer query and producer objects."""
    if handoff.winning_predicate.ref != predicate.ref:
        raise RecursiveLineageMismatch("handoff winning predicate != supplied predicate")
    if handoff.winning_predicate.predicate_hash != predicate.predicate_hash:
        raise RecursiveLineageMismatch("handoff winning predicate hash mismatch")
    # Verify source/release match
    if handoff.source_release_refs != (consumer_query.release_ref,):
        raise RecursiveLineageMismatch("handoff source releases != consumer release")


__all__ = [
    "AnalyticalCompositionError",
    "ConditionValueRelationMismatch",
    "JointTargetMismatch",
    "RecursiveLineageMismatch",
    "DiscoveryConsumptionMismatch",
    "ConditionValueBindingWitness",
    "AnalyticalCompositionResult",
    "SLICE_PROJECTION_SCHEMA",
    "SLICE_PROJECTION_SCHEMA_HASH",
    "SLICE_GEOMETRY_SCHEMA",
    "EVIDENCE_PREIMAGE_SCHEMA",
    "EVIDENCE_CONTRACT_ID",
    "compose_positioned_subject_possibility",
    "native_composition_original",
    "PRODUCER_ROUTE_DIRECT",
    "PRODUCER_ROUTE_DISCOVERY",
    "PRODUCER_ROUTE_RECURSIVE",
]
