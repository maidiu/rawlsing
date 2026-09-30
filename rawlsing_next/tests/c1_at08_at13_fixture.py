"""Synthetic fixtures for C1-02 higher-order / joint / recursive analytical composition (AT08-AT13).

These helpers deliberately reuse the I03/I05/MX01R2 owners; they only build the
witness/query material needed to drive the C1 composition seam.
"""
from __future__ import annotations

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    EmpiricalFact,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    ExactRef,
    semantic_hash,
)
from rawlsing_next.pre553_analytical_composition import ConditionValueBindingWitness
from rawlsing_next.source_backed_positioned_subject_possibility import (
    ConditionerBinding,
    PositionedSubjectPossibilityModelRule,
    PositionedSubjectPossibilityQuery,
)


WITNESS_KIND = "C1_CONDITION_VALUE_BINDING_WITNESS@2"
BINDING_MODE = "EXPLICIT_VALUE_BEARING_RELATION__NO_INFERENCE"


def _ref(kind: str, namespace: str, material: object) -> ExactRef:
    digest = semantic_hash(material)
    return ExactRef(kind, f"urn:test:c1-02:{namespace}:sha256:{digest}", digest)


def make_pairing_authority(tag: str = "c1-02") -> AuthorityRef:
    material = {
        "schema": "C1_SYNTHETIC_PAIRING_AUTHORITY@1",
        "tag": tag,
        "role": "FIXTURE_ONLY_CONDITION_VALUE_PAIRING",
    }
    digest = semantic_hash(material)
    return AuthorityRef(
        authority_id=f"urn:test:c1-02:pairing-authority:{tag}",
        authority_version="1.0.0",
        authority_content_hash=digest,
    )


def make_model_rule(source_universe_ref: ExactRef, tag: str = "c1-02") -> PositionedSubjectPossibilityModelRule:
    model_material = {
        "schema": "C1_SYNTHETIC_MODEL_AUTHORITY@1",
        "tag": tag,
        "role": "FIXTURE_ONLY_POSITIONED_SUBJECT_MODEL",
    }
    walkback_material = {
        "schema": "C1_SYNTHETIC_WALKBACK_AUTHORITY@1",
        "tag": tag,
        "role": "FIXTURE_ONLY_WALKBACK_POLICY",
    }
    model_digest = semantic_hash(model_material)
    walkback_digest = semantic_hash(walkback_material)
    model = AuthorityRef(
        authority_id=f"urn:test:c1-02:model-authority:{tag}",
        authority_version="1.0.0",
        authority_content_hash=model_digest,
    )
    walkback = AuthorityRef(
        authority_id=f"urn:test:c1-02:walkback-authority:{tag}",
        authority_version="1.0.0",
        authority_content_hash=walkback_digest,
    )
    return PositionedSubjectPossibilityModelRule(
        model_authority_ref=model,
        walkback_authority_ref=walkback,
        source_universe_refs=(source_universe_ref,),
        walkback_steps=(),
        positive_proxy_authority_refs=(),
    )


def make_multi_conditioner_consumer_query(
    *,
    query_id: str,
    subject_ref: ExactRef,
    target_ref: ExactRef,
    source_universe_ref: ExactRef,
    release_ref: ExactRef,
    bindings: list[ConditionerBinding],
    projection_kind: str,
    projection_payload: dict | None = None,
) -> PositionedSubjectPossibilityQuery:
    if projection_payload is None:
        projection_payload = {}
    return PositionedSubjectPossibilityQuery(
        query_id=query_id,
        subject_ref=subject_ref,
        target_ref=target_ref,
        source_universe_ref=source_universe_ref,
        release_ref=release_ref,
        conditioner_bindings=tuple(bindings),
        requested_projection={"kind": projection_kind, **projection_payload},
    )


def make_conditioner_binding(
    *,
    binding_id: str,
    subject_fact_ref: ExactRef,
    empirical_coordinate_ref: ExactRef,
    comparability_authority_ref: AuthorityRef,
    source_universe_ref: ExactRef,
    release_ref: ExactRef,
    effective_time_or_interval: object = None,
) -> ConditionerBinding:
    return ConditionerBinding(
        binding_id=binding_id,
        subject_fact_ref=subject_fact_ref,
        empirical_coordinate_ref=empirical_coordinate_ref,
        comparability_authority_ref=comparability_authority_ref,
        source_universe_ref=source_universe_ref,
        release_ref=release_ref,
        effective_time_or_interval=effective_time_or_interval,
    )


def _subject_material(binding_id: str, coordinate_ref: ExactRef, exact_value: object) -> dict:
    # Keep material minimal and stable; binding_id is intentionally not part of the
    # preimage so callers can construct matching subject_fact_refs independently.
    return {
        "schema": "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
        "empirical_semantic_ref": coordinate_ref.as_dict(),
        "exact_value": str(exact_value),
    }


def _leaf_projection(leaf_id: str, coordinate_ref: ExactRef, exact_value: object) -> dict:
    return {
        "schema": "C1_CONDITION_VALUE_LEAF_PROJECTION@1",
        "leaf_id": leaf_id,
        "leaf_type": "SURVEY_RESPONSE_EVENT",
        "question_semantic_ref": coordinate_ref.as_dict(),
        "operator": "EQ",
        "exact_value": str(exact_value),
    }


def _pairing_material(
    subject_ref: ExactRef,
    leaf_ref: ExactRef,
    coordinate_ref: ExactRef,
    exact_value: object,
) -> dict:
    return {
        "schema": "C1_CONDITION_VALUE_PAIRING_GROUND_TRUTH@1",
        "subject_preimage_ref": subject_ref.as_dict(),
        "predicate_leaf_preimage_ref": leaf_ref.as_dict(),
        "required_semantic_ref": coordinate_ref.as_dict(),
        "required_exact_value": str(exact_value),
    }


def make_multi_conditioner_witness(
    *,
    witness_object_id: str,
    consumer_query: PositionedSubjectPossibilityQuery,
    producer_query: EmpiricalQuerySpec,
    producer_predicate: EmpiricalPredicate,
    bindings: list[ConditionerBinding],
    subject_materials: list[dict],
    leaf_projections: list[dict],
    pairing_materials: list[dict],
    pairing_authority: AuthorityRef,
    source_universe_ref: ExactRef,
    release_ref: ExactRef,
    subject_preimage_refs: list[ExactRef] | None = None,
) -> ConditionValueBindingWitness:
    """Build a C1-02 multi-conditioner witness.

    The caller must supply one subject material, leaf projection and pairing
    material per binding, in the same order as ``bindings``.
    """
    if not (len(bindings) == len(subject_materials) == len(leaf_projections) == len(pairing_materials)):
        raise ValueError("binding and witness material counts must match")

    if subject_preimage_refs is None:
        subject_preimage_refs = []
        for i, subject in enumerate(subject_materials):
            subject_preimage_refs.append(_ref("C1_SYNTHETIC_POSITIONED_SUBJECT@1", f"subject-{i}", subject))
    producer_leaf_refs = []
    pairing_refs = []
    for i, (leaf, pair) in enumerate(zip(leaf_projections, pairing_materials)):
        producer_leaf_refs.append(_ref("C1_CONDITION_VALUE_LEAF_PROJECTION@1", f"leaf-{i}", leaf))
        pairing_refs.append(_ref("C1_CONDITION_VALUE_PAIRING_GROUND_TRUTH@1", f"pair-{i}", pair))

    identity_material = {
        "consumer_query_ref": consumer_query.ref.as_dict(),
        "consumer_binding_materials": [b.material() for b in bindings],
        "consumer_binding_fingerprint": semantic_hash([b.material() for b in bindings]),
        "producer_query_ref": producer_query.ref.as_dict(),
        "producer_predicate_ref": producer_predicate.ref.as_dict(),
        "producer_predicate_hash": producer_predicate.predicate_hash,
        "producer_predicate_leaf_refs": [ref.as_dict() for ref in producer_leaf_refs],
        "producer_predicate_leaf_projections": leaf_projections,
        "pairing_ground_truth_refs": [ref.as_dict() for ref in pairing_refs],
        "pairing_ground_truth_materials": pairing_materials,
        "pairing_authority_refs": [pairing_authority.as_dict()] * len(bindings),
        "source_universe_ref": source_universe_ref.as_dict(),
        "release_ref": release_ref.as_dict(),
        "effective_time_or_intervals": [b.effective_time_or_interval for b in bindings],
        "binding_mode": BINDING_MODE,
    }
    witness_ref = ExactRef(WITNESS_KIND, witness_object_id, semantic_hash(identity_material))
    return ConditionValueBindingWitness(
        witness_ref=witness_ref,
        identity_material=identity_material,
        subject_condition_preimage_refs=tuple(subject_preimage_refs),
        subject_condition_preimage_materials=tuple(subject_materials),
        producer_predicate_leaf_refs=tuple(producer_leaf_refs),
        producer_predicate_leaf_projections=tuple(leaf_projections),
        pairing_ground_truth_refs=tuple(pairing_refs),
        pairing_ground_truth_materials=tuple(pairing_materials),
        pairing_authority_refs=tuple([pairing_authority] * len(bindings)),
    )


def build_witness_for_binding(
    *,
    witness_object_id: str,
    consumer_query: PositionedSubjectPossibilityQuery,
    producer_query: EmpiricalQuerySpec,
    producer_predicate: EmpiricalPredicate,
    bindings: list[ConditionerBinding],
    coordinate_value_pairs: list[tuple[ExactRef, object]],
    pairing_authority: AuthorityRef,
    source_universe_ref: ExactRef,
    release_ref: ExactRef,
) -> ConditionValueBindingWitness:
    """Convenience builder when each binding is a simple EQ response value.

    Uses each binding's own ``subject_fact_ref`` as the frozen subject preimage,
    so the witness matches the consumer query exactly.
    """
    subject_materials = []
    leaf_projections = []
    pairing_materials = []
    subject_preimage_refs = []
    for i, (binding, (coordinate_ref, value)) in enumerate(zip(bindings, coordinate_value_pairs)):
        subject = _subject_material(binding.binding_id, coordinate_ref, value)
        leaf = _leaf_projection(binding.binding_id, coordinate_ref, value)
        leaf_ref = _ref("C1_CONDITION_VALUE_LEAF_PROJECTION@1", f"leaf-{i}", leaf)
        pair = _pairing_material(
            binding.subject_fact_ref,
            leaf_ref,
            coordinate_ref,
            value,
        )
        subject_materials.append(subject)
        leaf_projections.append(leaf)
        pairing_materials.append(pair)
        subject_preimage_refs.append(binding.subject_fact_ref)
    return make_multi_conditioner_witness(
        witness_object_id=witness_object_id,
        consumer_query=consumer_query,
        producer_query=producer_query,
        producer_predicate=producer_predicate,
        bindings=bindings,
        subject_materials=subject_materials,
        leaf_projections=leaf_projections,
        pairing_materials=pairing_materials,
        pairing_authority=pairing_authority,
        source_universe_ref=source_universe_ref,
        release_ref=release_ref,
        subject_preimage_refs=subject_preimage_refs,
    )


__all__ = [
    "make_pairing_authority",
    "make_model_rule",
    "make_multi_conditioner_consumer_query",
    "make_conditioner_binding",
    "make_multi_conditioner_witness",
    "build_witness_for_binding",
    "WITNESS_KIND",
    "BINDING_MODE",
]