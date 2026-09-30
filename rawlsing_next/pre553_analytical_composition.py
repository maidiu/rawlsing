"""C1-01 direct analytical composition: public I03 -> exact possibility slice -> consumer.

This module is intentionally narrow. It owns no survey semantics, comparability
meaning, model authority, or structural admission. It composes already-authoritative
objects while preserving their exact identities.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Iterable, Mapping

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
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
from rawlsing_next.source_backed_positioned_subject_possibility import (
    ConditionerBinding,
    PositionedSubjectPossibilityModelRule,
    PositionedSubjectPossibilityQuery,
    PositionedSubjectPossibilityResult,
    PossibilitySliceEvidence,
    evaluate_positioned_subject_possibility,
)

SLICE_PROJECTION_SCHEMA = "C1_POSSIBILITY_SLICE_PROJECTION@1"
SLICE_PROJECTION_SCHEMA_HASH = "c00e038dd2c1177bfc7842f12febef7b3e30b92bc421df244e2a8e3c4a20b17a"
SLICE_GEOMETRY_SCHEMA = "C1_POSSIBILITY_SLICE_GEOMETRY@1"
EVIDENCE_PREIMAGE_SCHEMA = "C1_POSITIONED_SUBJECT_SLICE_EVIDENCE_PREIMAGE@1"
EVIDENCE_CONTRACT_ID = "C1_POSITIONED_SUBJECT_SLICE_EVIDENCE@1"
WITNESS_KIND = "C1_CONDITION_VALUE_BINDING_WITNESS@2"
WITNESS_BINDING_MODE = "EXPLICIT_VALUE_BEARING_RELATION__NO_INFERENCE"
PRODUCER_ROUTE = "DIRECT_I03_TO_POSITIONED_SUBJECT"


class AnalyticalCompositionError(Pre553IntegrityError):
    """Typed C1-01 composition failure; upstream owner errors are not laundered."""


class ConditionValueRelationMismatch(AnalyticalCompositionError):
    code = "CONDITION_VALUE_RELATION_MISMATCH"

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


def _exact_fraction(numerator: int, denominator: int) -> Mapping[str, list[int]] | None:
    if denominator == 0:
        return None
    value = Fraction(numerator, denominator)
    return {"$exact_fraction": [value.numerator, value.denominator]}


def _binding_fingerprint(binding: ConditionerBinding) -> str:
    return semantic_hash(binding.material())


def _single_binding(query: PositionedSubjectPossibilityQuery) -> ConditionerBinding:
    if len(query.conditioner_bindings) != 1:
        raise AnalyticalCompositionError(
            "C1-01_DIRECT_SCALAR_REQUIRES_EXACTLY_ONE_CONDITIONER_BINDING"
        )
    return query.conditioner_bindings[0]


def _actual_leaf(predicate: EmpiricalPredicate) -> Mapping[str, Any]:
    ast = canonicalize(predicate.predicate_ast)
    if ast.get("op") != "LEAF":
        raise ConditionValueRelationMismatch(
            "C1-01 scalar direct path requires one value-bearing producer leaf"
        )
    if ast.get("leaf_type") != "SURVEY_RESPONSE_EVENT":
        raise ConditionValueRelationMismatch(
            "C1-01 AT07 requires SURVEY_RESPONSE_EVENT condition leaf"
        )
    if ast.get("operator") != "EQ" or "exact_value" not in ast:
        raise ConditionValueRelationMismatch("producer condition must be exact EQ")
    return ast


@dataclass(frozen=True)
class ConditionValueBindingWitness:
    """Exact custody witness; never a source of new comparability semantics."""

    witness_ref: ExactRef
    identity_material: Mapping[str, Any]
    subject_condition_preimage_ref: ExactRef
    subject_condition_preimage_material: Mapping[str, Any]
    producer_predicate_leaf_ref: ExactRef
    producer_predicate_leaf_projection: Mapping[str, Any]
    pairing_ground_truth_ref: ExactRef
    pairing_ground_truth_material: Mapping[str, Any]
    pairing_authority_ref: AuthorityRef

    def __post_init__(self) -> None:
        if self.witness_ref.kind != WITNESS_KIND:
            raise AnalyticalCompositionError("unexpected condition witness kind")
        canonicalize(self.identity_material)
        canonicalize(self.subject_condition_preimage_material)
        canonicalize(self.producer_predicate_leaf_projection)
        canonicalize(self.pairing_ground_truth_material)

    def verify_identity(self) -> None:
        if semantic_hash(self.identity_material) != self.witness_ref.content_hash:
            raise ConditionValueRelationMismatch("witness identity preimage hash mismatch")
        if (
            semantic_hash(self.subject_condition_preimage_material)
            != self.subject_condition_preimage_ref.content_hash
        ):
            raise ConditionValueRelationMismatch("subject-condition preimage hash mismatch")
        if (
            semantic_hash(self.producer_predicate_leaf_projection)
            != self.producer_predicate_leaf_ref.content_hash
        ):
            raise ConditionValueRelationMismatch("producer predicate-leaf preimage hash mismatch")
        if (
            semantic_hash(self.pairing_ground_truth_material)
            != self.pairing_ground_truth_ref.content_hash
        ):
            raise ConditionValueRelationMismatch("pairing ground-truth preimage hash mismatch")


@dataclass(frozen=True)
class AnalyticalCompositionResult:
    analytical_state: str
    producer_route: str
    producer_query_ref: ExactRef
    producer_predicate_ref: ExactRef
    producer_fact_ref: ExactRef
    producer_fact_state: str
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

    def identity_material(self) -> Mapping[str, Any]:
        return {
            "analytical_state": self.analytical_state,
            "producer_route": self.producer_route,
            "producer_query_ref": self.producer_query_ref.as_dict(),
            "producer_predicate_ref": self.producer_predicate_ref.as_dict(),
            "producer_fact_ref": self.producer_fact_ref.as_dict(),
            "producer_fact_state": self.producer_fact_state,
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
        }


def _verify_witness(
    *,
    witness: ConditionValueBindingWitness,
    consumer_query: PositionedSubjectPossibilityQuery,
    binding: ConditionerBinding,
    empirical_query: EmpiricalQuerySpec,
    predicate: EmpiricalPredicate,
    release_ref: ExactRef,
) -> str:
    witness.verify_identity()
    actual_leaf = _actual_leaf(predicate)
    identity = canonicalize(witness.identity_material)
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
    if not required.issubset(identity):
        raise ConditionValueRelationMismatch("witness missing frozen required field")

    fingerprint = _binding_fingerprint(binding)
    expected_fields = {
        "consumer_query_ref": consumer_query.ref.as_dict(),
        "consumer_binding_material": canonicalize(binding.material()),
        "consumer_binding_fingerprint": fingerprint,
        "subject_condition_preimage_ref": witness.subject_condition_preimage_ref.as_dict(),
        "subject_condition_preimage_material": canonicalize(
            witness.subject_condition_preimage_material
        ),
        "producer_query_ref": empirical_query.ref.as_dict(),
        "producer_predicate_ref": predicate.ref.as_dict(),
        "producer_predicate_hash": predicate.predicate_hash,
        "producer_predicate_leaf_ref": witness.producer_predicate_leaf_ref.as_dict(),
        "producer_predicate_leaf_projection": canonicalize(
            witness.producer_predicate_leaf_projection
        ),
        "pairing_ground_truth_ref": witness.pairing_ground_truth_ref.as_dict(),
        "pairing_authority_ref": witness.pairing_authority_ref.as_dict(),
        "source_universe_ref": consumer_query.source_universe_ref.as_dict(),
        "release_ref": release_ref.as_dict(),
        "effective_time_or_interval": canonicalize(binding.effective_time_or_interval),
        "binding_mode": WITNESS_BINDING_MODE,
    }
    for key, value in expected_fields.items():
        if canonicalize(identity[key]) != canonicalize(value):
            raise ConditionValueRelationMismatch(f"witness field mismatch: {key}")

    subject = canonicalize(witness.subject_condition_preimage_material)
    if subject.get("empirical_semantic_ref") != binding.empirical_coordinate_ref.as_dict():
        raise ConditionValueRelationMismatch(
            "subject semantic ref != consumer binding coordinate"
        )
    if binding.subject_fact_ref != witness.subject_condition_preimage_ref:
        raise ConditionValueRelationMismatch(
            "consumer subject fact != frozen subject preimage"
        )
    if binding.comparability_authority_ref != witness.pairing_authority_ref:
        raise ConditionValueRelationMismatch(
            "consumer comparability authority != pairing authority"
        )
    if binding.source_universe_ref != consumer_query.source_universe_ref:
        raise ConditionValueRelationMismatch("binding source universe mismatch")
    if binding.release_ref != release_ref:
        raise ConditionValueRelationMismatch("binding release mismatch")

    frozen_leaf = canonicalize(witness.producer_predicate_leaf_projection)
    for key in ("leaf_type", "question_semantic_ref", "operator", "exact_value"):
        if frozen_leaf.get(key) != actual_leaf.get(key):
            raise ConditionValueRelationMismatch(
                f"actual producer leaf mismatch: {key}"
            )
    if frozen_leaf.get("question_semantic_ref") != subject.get("empirical_semantic_ref"):
        raise ConditionValueRelationMismatch("producer/subject semantic ref mismatch")
    if frozen_leaf.get("exact_value") != subject.get("exact_value"):
        raise ConditionValueRelationMismatch("producer/subject exact value mismatch")

    pair = canonicalize(witness.pairing_ground_truth_material)
    if pair.get("subject_preimage_ref") != witness.subject_condition_preimage_ref.as_dict():
        raise ConditionValueRelationMismatch("pairing subject ref mismatch")
    if pair.get("predicate_leaf_preimage_ref") != witness.producer_predicate_leaf_ref.as_dict():
        raise ConditionValueRelationMismatch("pairing predicate leaf ref mismatch")
    if pair.get("required_semantic_ref") != subject.get("empirical_semantic_ref"):
        raise ConditionValueRelationMismatch("pairing semantic ref mismatch")
    if pair.get("required_exact_value") != subject.get("exact_value"):
        raise ConditionValueRelationMismatch("pairing exact value mismatch")
    return fingerprint


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
    if len(targets) != 1 or targets[0] != consumer_query.target_ref:
        raise AnalyticalCompositionError("TARGET_TOPOLOGY_OR_DOMAIN_MISMATCH")
    topology = canonicalize(empirical_query.target_arity_and_topology)
    if topology.get("arity") != 1 or len(topology.get("components", ())) != 1:
        raise AnalyticalCompositionError("C1-01 requires scalar arity=1 target")
    if topology["components"][0].get("target_ref") != consumer_query.target_ref.as_dict():
        raise AnalyticalCompositionError("TARGET_TOPOLOGY_OR_DOMAIN_MISMATCH")


def _supported_geometry(
    *,
    fact: EmpiricalFact,
    empirical_query: EmpiricalQuerySpec,
    predicate: EmpiricalPredicate,
    witness: ConditionValueBindingWitness,
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
    component = topology["components"][0]
    target_ref = _exact(empirical_query.target_refs[0], "target_ref")
    measure_kind = fact.measure_kind
    weight_basis = empirical_query.requested_output_grain.get("weight_basis_id")
    if measure_kind != "RAW" or weight_basis is not None:
        raise AnalyticalCompositionError(
            "MEASURE_IDENTITY_MISMATCH: C1-01 frozen AT07 direct path is RAW"
        )

    return {
        "schema": SLICE_GEOMETRY_SCHEMA,
        "source_fact_ref": fact.ref.as_dict(),
        "producer_query_ref": empirical_query.ref.as_dict(),
        "condition_predicate_ref": predicate.ref.as_dict(),
        "condition_value_witness_ref": witness.witness_ref.as_dict(),
        "target": {
            "target_ref": target_ref.as_dict(),
            "arity": topology["arity"],
            "joint_order_semantics": topology["joint_order_semantics"],
            "component_material": component,
            "target_domain_identity": fact.target_domain_identity,
        },
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
) -> PossibilitySliceEvidence:
    geometry = _supported_geometry(
        fact=fact,
        empirical_query=empirical_query,
        predicate=predicate,
        witness=witness,
    )
    provenance = _refs(
        (
            fact.ref,
            empirical_query.ref,
            predicate.ref,
            _exact(fact.replay_ref, "replay_ref"),
            witness.witness_ref,
            witness.subject_condition_preimage_ref,
            witness.pairing_ground_truth_ref,
        ),
        "evidence_provenance",
    )
    authorities = _auths(
        (*fact.authority_snapshot_refs, witness.pairing_authority_ref),
        "evidence_authorities",
    )
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
        raise AnalyticalCompositionError("C1-01 requires exactly one producer fact")
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
) -> AnalyticalCompositionResult:
    """Execute the exact C1-01 vertical slice without accepting a prebuilt slice."""

    release_refs = _refs(release_refs, "release_refs")
    _validate_direct_grain(
        empirical_query=empirical_query,
        consumer_query=consumer_query,
        release_refs=release_refs,
    )
    binding = _single_binding(consumer_query)

    producer_result = execute_empirical_query(
        repository=repository,
        query=empirical_query,
        predicate=predicate,
        authority_registry=authority_registry,
        release_refs=release_refs,
    )
    fact = _selected_fact(producer_result, empirical_query)

    fingerprint = _verify_witness(
        witness=condition_binding_witness,
        consumer_query=consumer_query,
        binding=binding,
        empirical_query=empirical_query,
        predicate=predicate,
        release_ref=release_refs[0],
    )

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
    authorities = _auths(
        (*fact.authority_snapshot_refs, condition_binding_witness.pairing_authority_ref),
        "authority_refs",
    )
    ordered_targets = _refs(empirical_query.target_refs, "target_refs")
    measure_kind = getattr(
        fact, "measure_kind", empirical_query.requested_output_grain.get("measure_kind")
    )
    weight_basis = empirical_query.requested_output_grain.get("weight_basis_id")

    kwargs = dict(
        analytical_state=fact.typed_state,
        producer_route=PRODUCER_ROUTE,
        producer_query_ref=producer_result.query_ref,
        producer_predicate_ref=predicate.ref,
        producer_fact_ref=fact.ref,
        producer_fact_state=fact.typed_state,
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
        coverage_state="DIRECT_EXACT_SINGLE_QUERY",
        ancestry_refs=(),
        authority_refs=authorities,
        provenance_refs=provenance,
        dependency_refs=dependencies,
        replay_refs=replay_refs,
        possibility_slice_evidence_or_null=evidence,
        consumer_result_or_null=consumer_result,
        consumer_model_rule_hash=model_rule.rule_hash,
        subject_condition_preimage_refs=(
            condition_binding_witness.subject_condition_preimage_ref,
        ),
        producer_predicate_leaf_refs=(
            condition_binding_witness.producer_predicate_leaf_ref,
        ),
        pairing_ground_truth_refs=(
            condition_binding_witness.pairing_ground_truth_ref,
        ),
        slice_projection_schema_hash=SLICE_PROJECTION_SCHEMA_HASH,
    )
    provisional = AnalyticalCompositionResult(
        **kwargs, composed_result_identity_hash="0" * 64
    )
    return AnalyticalCompositionResult(
        **kwargs,
        composed_result_identity_hash=semantic_hash(provisional.identity_material()),
    )


__all__ = [
    "AnalyticalCompositionError",
    "ConditionValueRelationMismatch",
    "ConditionValueBindingWitness",
    "AnalyticalCompositionResult",
    "SLICE_PROJECTION_SCHEMA",
    "SLICE_PROJECTION_SCHEMA_HASH",
    "SLICE_GEOMETRY_SCHEMA",
    "EVIDENCE_PREIMAGE_SCHEMA",
    "EVIDENCE_CONTRACT_ID",
    "compose_positioned_subject_possibility",
]
