"""Focused native tests for R61 universal evidence binding.

Positive and ZERO_SUPPORT witnesses execute the accepted C1/N10E producer over
the source-free AT07 fixture.  Hostile witnesses change exact request identity
and require typed refusal at the same consumer boundary.  No original survey
data, source permission or scientific issuance is involved.
"""
from __future__ import annotations

from dataclasses import replace
import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

import rawlsing_next.tests.test_pre553_empirical_query as i03
from rawlsing_next.pre553_analytical_composition import ConditionValueBindingWitness
from rawlsing_next.pre553_empirical_objects import ExactRef, canonicalize, semantic_hash
from rawlsing_next.source_backed_positioned_subject_possibility import (
    ConditionerBinding,
    PositionedSubjectPossibilityQuery,
)
from rawlsing_next.tests import c1_at08_at13_fixture as fx
from rawlsing_next.pre553_empirical_possibility_provider import (
    provide_empirical_possibility_slice,
)
from rawlsing_next.tests.n10e_empirical_slice_fixture import (
    build_consumer,
    build_model_rule,
    build_producer,
    build_provider_case,
    build_witness,
    fixture_authority,
    frozen_at07_source,
)
from rawlsing_next.pre553_universal_evidence_binding import (
    CACHE_SCHEMA,
    CACHE_OWNER_DESCRIPTOR_SCHEMA,
    CACHE_OWNER_FIELDS,
    CACHE_OWNER_DESCRIPTOR_FIELDS,
    EXECUTION_STATES,
    ELIGIBILITY_STATES,
    PROVENANCE_CACHE,
    PROVENANCE_CANONICAL,
    REFUSAL_NO_EXACT_BINDING,
    RESULT_STATES,
    AdmittedEvidenceContext,
    EmpiricalProducerBinding,
    EvidenceAssociationError,
    EvidenceBindingError,
    EvidenceCacheIntegrityError,
    EvidenceConsumerReader,
    EvidenceRequest,
    EvidenceRequestShapeError,
    EvidenceResolver,
    EvidenceResult,
    OccurrenceKey,
    TrustedAdmissionAuthority,
    TrustedCacheIssuer,
    TypedCondition,
    _evidence_material,
    TypedValue,
    reduce_required_support,
    request_from_empirical_case,
)


def _ref(kind: str, tag: str, material=None) -> ExactRef:
    material = {"tag": tag} if material is None else material
    digest = semantic_hash(material)
    return ExactRef(kind, f"urn:test:r61:{tag}:sha256:{digest}", digest)


_R4_ISSUER = TrustedAdmissionAuthority()
_R4_VERIFIER = _R4_ISSUER.verifier()


def _resolver(**kwargs) -> EvidenceResolver:
    kwargs.setdefault("admission_verifier", _R4_VERIFIER)
    kwargs.setdefault("executor", _R4_ISSUER)
    kwargs.setdefault("admitted_producer", provide_empirical_possibility_slice)
    return EvidenceResolver(**kwargs)


def _reader(request, result) -> EvidenceConsumerReader:
    return EvidenceConsumerReader(request, result, verifier=_R4_VERIFIER)


def _condition(item: str, option: str, value, binding_id: str) -> TypedCondition:
    return TypedCondition(
        occurrence=OccurrenceKey(item, option, "FORM_1", "0"),
        value=TypedValue.build(value),
        domain_state_version="AT07_DOMAIN@1",
        conditioner_binding_id=binding_id,
    )


def _make_context(case) -> AdmittedEvidenceContext:
    source = case["source"]
    item, option, value, binding_id = case.get(
        "default_condition", ("POSITION", "P1", "P1", "position")
    )
    return AdmittedEvidenceContext(
        context_id="r61-at07-admitted-context",
        admission_ref=_ref(
            "R61_ADMISSION", "at07-admission", {"fixture": "AT07_BIDIRECTIONAL_100"}
        ),
        provenance_refs=(source["release_ref"], source["universe"].ref),
        authority_refs=tuple(case["predicate"].authority_snapshot_refs),
        source_id="AT07_SYNTHETIC_SOURCE",
        dataset_id="AT07_BIDIRECTIONAL_100",
        wave_id="W1",
        edition="2026-01",
        byte_digest=semantic_hash({"fixture": "AT07_BIDIRECTIONAL_100"}),
        instrument_version="AT07_INSTRUMENT@1",
        sampled_unit="SYNTHETIC_INDIVIDUAL_RESPONDENT",
        reporting_unit="SYNTHETIC_INDIVIDUAL_RESPONDENT",
        link_refs=(),
        estimand="CONDITIONAL_DISTRIBUTION",
        weight_method="RAW_UNWEIGHTED",
        design_ref=_ref("R61_DESIGN", "at07-design", {"design": "AT07"}),
        uncertainty_method="UNCERTAINTY_UNQUANTIFIED",
        direction=case.get("default_direction", "POSITION_P1_TO_ANSWER"),
        role=case.get("default_role", "FORWARD_AUTHORIZED"),
        consumer_use="TEST_ONLY_EMPIRICAL_POSSIBILITY",
        grammar_version="C1_AT07_GRAMMAR@1",
        custody_ref=_ref("R61_CUSTODY", "at07-custody", {"fixture": "AT07"}),
        observation_clock="2026-01",
        reference_clock="2026-01",
        as_of_clock="2026-01-31",
        publication_clock="2026-02-01",
        permission_ref=_ref(
            "R61_PERMISSION", "test-only-permission", {"scope": "TEST_ONLY"}
        ),
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        risk_set_ref=case["empirical_query"].risk_set_ref
        if isinstance(case["empirical_query"].risk_set_ref, ExactRef)
        else ExactRef(**case["empirical_query"].risk_set_ref),
        target_ref=case["consumer_query"].target_ref,
        occurrence_item=item,
        occurrence_option=option,
        occurrence_form="FORM_1",
        occurrence_repeat="0",
        domain_state_version="AT07_DOMAIN@1",
    )


def _request(
    case,
    *,
    conditions=None,
    empirical_query=None,
    predicate=None,
    consumer_query=None,
    **overrides,
) -> EvidenceRequest:
    source = case["source"]
    query = empirical_query or case["empirical_query"]
    pred = predicate or case["predicate"]
    consumer = consumer_query or case["consumer_query"]
    binding = consumer.conditioner_bindings[0]
    conditions = conditions or (
        _condition("POSITION", "P1", "P1", binding.binding_id),
    )
    if "_r61_context" not in case:
        case["_r61_context"] = _make_context(case)
    values = dict(
        request_id="r61-at07-positive",
        claim_grade="TEST_ONLY_SOURCE_LOCAL",
        source_id="AT07_SYNTHETIC_SOURCE",
        dataset_id="AT07_BIDIRECTIONAL_100",
        wave_id="W1",
        edition="2026-01",
        byte_digest=semantic_hash({"fixture": "AT07_BIDIRECTIONAL_100"}),
        instrument_version="AT07_INSTRUMENT@1",
        occurrence=conditions[0].occurrence,
        sampled_unit="SYNTHETIC_INDIVIDUAL_RESPONDENT",
        reporting_unit="SYNTHETIC_INDIVIDUAL_RESPONDENT",
        link_refs=(),
        estimand="CONDITIONAL_DISTRIBUTION",
        weight_method="RAW_UNWEIGHTED",
        design_ref=_ref("R61_DESIGN", "at07-design", {"design": "AT07"}),
        uncertainty_method="UNCERTAINTY_UNQUANTIFIED",
        direction="POSITION_P1_TO_ANSWER",
        role="FORWARD_AUTHORIZED",
        consumer_use="TEST_ONLY_EMPIRICAL_POSSIBILITY",
        grammar_version="C1_AT07_GRAMMAR@1",
        custody_ref=_ref("R61_CUSTODY", "at07-custody", {"fixture": "AT07"}),
        observation_clock="2026-01",
        reference_clock="2026-01",
        as_of_clock="2026-01-31",
        publication_clock="2026-02-01",
        permission_ref=_ref(
            "R61_PERMISSION", "test-only-permission", {"scope": "TEST_ONLY"}
        ),
        ordered_conditions=conditions,
        empirical_query=query,
        predicate=pred,
        consumer_query=consumer,
        model_rule=case["model_rule"],
    )
    values.update(overrides)
    return request_from_empirical_case(**values)


def _binding(request, case, *, producer=None) -> EmpiricalProducerBinding:
    canonical_context = _make_context(case)
    kwargs = dict(
        request=request,
        repository=case["source"]["repo"],
        empirical_query=case["empirical_query"],
        predicate=case["predicate"],
        authority_registry=case["registry"],
        release_refs=case["release_refs"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        condition_binding_witness=case["condition_binding_witness"],
        context=case.get("_r61_context") or canonical_context,
    )
    if producer is not None:
        kwargs["producer"] = producer
    binding = EmpiricalProducerBinding(**kwargs)
    canonical_owner = replace(binding, context=canonical_context, admission=None)
    admission = _R4_ISSUER.issue_producer(
        context_ref=canonical_context.context_ref,
        owner_identity_material=canonical_owner.owner_identity_material(),
    )
    return replace(binding, admission=admission)


def _zero_case(case):
    source = case["source"]
    query_authority = case["query_authority"]
    leaf = i03._response_leaf(source, query_authority, "POSITION", "P3")
    predicate = i03._predicate(source, query_authority, leaf, tag="r61-zero")
    empirical_query = i03._query(
        source,
        query_authority,
        predicate,
        ("ANSWER",),
        risk="R",
        tag="r61-zero",
    )
    pairing = fixture_authority("FIXTURE_ONLY_CONDITION_VALUE_PAIRING")
    subject_material = {
        "schema": "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
        "fixture_id": "R61_ZERO_SUPPORT",
        "role": "FORWARD_POSITION_P3",
        "real_subject": False,
    }
    subject_ref = ExactRef(
        "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
        "urn:test:c1:r61:subject:zero",
        semantic_hash(subject_material),
    )
    subject_preimage_material = {
        "role": "FORWARD_POSITION_P3",
        "empirical_semantic_ref": source["qrefs"]["POSITION"],
        "exact_value": "P3",
    }
    subject_preimage_ref = ExactRef(
        "SUBJECT_CONDITION_PREIMAGE",
        "urn:test:c1:r61:subject-pre:zero",
        semantic_hash(subject_preimage_material),
    )
    binding = ConditionerBinding(
        "position",
        subject_preimage_ref,
        source["qrefs"]["POSITION"],
        pairing,
        source["universe"].ref,
        source["release_ref"],
        None,
    )
    consumer_query = PositionedSubjectPossibilityQuery(
        "r61-zero-subject",
        subject_ref,
        source["qrefs"]["ANSWER"],
        source["universe"].ref,
        source["release_ref"],
        (binding,),
        {
            "kind": "C1_AT07_CONDITIONAL_DISTRIBUTION",
            "direction": "POSITION_P3_TO_ANSWER",
            "target_role": "ANSWER",
        },
    )
    leaf_ref = ExactRef(
        "PRODUCER_PREDICATE_LEAF",
        "urn:test:c1:r61:leaf:zero",
        semantic_hash(leaf),
    )
    pairing_material = {
        "subject_preimage_ref": subject_preimage_ref.as_dict(),
        "predicate_leaf_preimage_ref": leaf_ref.as_dict(),
        "required_semantic_ref": source["qrefs"]["POSITION"],
        "required_exact_value": "P3",
    }
    pairing_ref = ExactRef(
        "PAIRING_GROUND_TRUTH",
        "urn:test:c1:r61:pair:zero",
        semantic_hash(pairing_material),
    )
    identity_material = {
        "consumer_query_ref": consumer_query.ref.as_dict(),
        "consumer_binding_material": canonicalize(binding.material()),
        "consumer_binding_fingerprint": semantic_hash(binding.material()),
        "subject_condition_preimage_ref": subject_preimage_ref.as_dict(),
        "subject_condition_preimage_material": canonicalize(
            subject_preimage_material
        ),
        "producer_query_ref": empirical_query.ref.as_dict(),
        "producer_predicate_ref": predicate.ref.as_dict(),
        "producer_predicate_hash": predicate.predicate_hash,
        "producer_predicate_leaf_ref": leaf_ref.as_dict(),
        "producer_predicate_leaf_projection": canonicalize(leaf),
        "pairing_ground_truth_ref": pairing_ref.as_dict(),
        "pairing_authority_ref": pairing.as_dict(),
        "source_universe_ref": consumer_query.source_universe_ref.as_dict(),
        "release_ref": consumer_query.release_ref.as_dict(),
        "effective_time_or_interval": None,
        "binding_mode": "EXPLICIT_VALUE_BEARING_RELATION__NO_INFERENCE",
    }
    witness_ref = ExactRef(
        "C1_CONDITION_VALUE_BINDING_WITNESS@2",
        "urn:test:c1:r61:witness:zero",
        semantic_hash(identity_material),
    )
    witness = ConditionValueBindingWitness(
        witness_ref=witness_ref,
        identity_material=identity_material,
        subject_condition_preimage_ref=subject_preimage_ref,
        subject_condition_preimage_material=subject_preimage_material,
        producer_predicate_leaf_ref=leaf_ref,
        producer_predicate_leaf_projection=leaf,
        pairing_ground_truth_ref=pairing_ref,
        pairing_ground_truth_material=pairing_material,
        pairing_authority_ref=pairing,
    )
    return {
        "source": source,
        "query_authority": query_authority,
        "registry": case["registry"],
        "predicate": predicate,
        "empirical_query": empirical_query,
        "consumer_query": consumer_query,
        "condition_binding_witness": witness,
        "model_rule": case["model_rule"],
        "release_refs": (source["release_ref"],),
        "default_condition": ("POSITION", "P3", "P3", "position"),
        "default_direction": "POSITION_P3_TO_ANSWER",
    }


def _xor_case(condition_value, tag="r61-xor"):
    source = fx.xor_fixture(tag)
    query_authority = i03._query_authority(tag)
    predicate = i03._predicate(
        source,
        query_authority,
        i03._response_leaf(source, query_authority, "A", condition_value),
        tag=f"{tag}-predicate",
    )
    empirical_query = i03._query(
        source,
        query_authority,
        predicate,
        ("C",),
        tag=f"{tag}-query",
    )
    pairing = fx.make_pairing_authority(tag)
    binding = fx.make_conditioner_binding(
        binding_id="a",
        subject_fact_ref=ExactRef(**fx.subject_fact_ref(source, "A", condition_value)),
        empirical_coordinate_ref=source["qrefs"]["A"],
        comparability_authority_ref=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    subject_ref = ExactRef(
        "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
        f"urn:test:r61:{tag}:subject",
        semantic_hash({"tag": tag, "condition_value": condition_value}),
    )
    consumer_query = fx.make_multi_conditioner_consumer_query(
        query_id=f"{tag}-consumer",
        subject_ref=subject_ref,
        target_ref=source["qrefs"]["C"],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=[binding],
        projection_kind="R61_XOR_CONDITIONAL",
        projection_payload={"condition_value": condition_value},
    )
    witness = fx.build_witness_for_binding(
        witness_object_id=f"urn:test:r61:{tag}:witness",
        consumer_query=consumer_query,
        producer_query=empirical_query,
        producer_predicate=predicate,
        bindings=[binding],
        coordinate_value_pairs=[(source["qrefs"]["A"], condition_value)],
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    return {
        "source": source,
        "query_authority": query_authority,
        "registry": i03._registry(source, query_authority),
        "predicate": predicate,
        "empirical_query": empirical_query,
        "consumer_query": consumer_query,
        "condition_binding_witness": witness,
        "model_rule": fx.make_model_rule(source["universe"].ref, tag),
        "release_refs": (source["release_ref"],),
        "default_condition": ("A", str(condition_value), condition_value, "a"),
        "default_direction": f"A{condition_value}_TO_C",
    }


def test_condition_a0_result_cannot_resolve_a1_request():
    case = _xor_case(0)
    fingerprint = semantic_hash(
        [case["consumer_query"].conditioner_bindings[0].material()]
    )
    request_a0 = _request(
        case,
        conditions=(_condition("A", "0", "0", "a"),),
        consumer_binding_fingerprint=fingerprint,
        direction="A0_TO_C",
        request_id="r61-xor-a0",
    )
    request_a1 = _request(
        case,
        conditions=(_condition("A", "1", "1", "a"),),
        consumer_binding_fingerprint=fingerprint,
        direction="A1_TO_C",
        request_id="r61-xor-a1",
    )
    assert request_a0.key != request_a1.key
    resolver = _resolver()
    resolver.bind(_binding(request_a0, case))
    result_a0 = resolver.resolve(request_a0)
    assert result_a0.result_state == "SUPPORTED"
    assert result_a0.denominator == 2
    assert {cell["cell"]: cell["raw_numerator_support"] for cell in result_a0.cells} == {
        "0": 1,
        "1": 1,
    }
    assert (
        _reader(request_a0, result_a0).read()["consumer_result_state"]
        == "EXACT_SUPPORTED"
    )

    refused_a1 = resolver.resolve(request_a1)
    assert refused_a1.result_state == "UNKNOWN"
    assert refused_a1.typed_refusal == REFUSAL_NO_EXACT_BINDING
    with pytest.raises(EvidenceAssociationError):
        _reader(request_a1, result_a0).read()


def test_positive_actual_producer_consumer_values_read():
    case = build_provider_case("forward")
    request = _request(case)
    resolver = _resolver()
    assert resolver.bind(_binding(request, case)) == request.key

    result = resolver.resolve(request)
    assert result.result_state == "SUPPORTED"
    assert result.eligibility_state == "ELIGIBLE"
    assert result.execution_state == "COMPLETED"
    assert result.provenance == PROVENANCE_CANONICAL
    assert result.denominator == 60
    cells = {cell["cell"]: cell["raw_numerator_support"] for cell in result.cells}
    assert cells == {"no": 6, "yes": 54}
    assert result.consumer_result_state == "EXACT_SUPPORTED"
    values = result.consumer_values_read
    assert values["request_key"] == request.key
    assert values["denominator"] == 60
    assert values["ordered_conditions"][0]["typed_value"] == {
        "tag": "STRING",
        "value": "P1",
    }
    assert values["ordered_conditions"][0]["occurrence"]["option"] == "P1"

    reader = _reader(request, result)
    read = reader.read()
    assert read["consumer_result_state"] == "EXACT_SUPPORTED"
    assert read["consumer_result_hash"] == result.consumer_result_hash
    step = reader.e04_step()
    assert step["state"] == "EXACT_SUPPORTED"
    assert step["denominator"] == 60
    assert step["request_key"] == request.key
    assert step["evidence_ref"] == result.evidence_ref.as_dict()


def test_actual_zero_support_does_not_become_positive_and_breaks_consumer():
    case = build_provider_case("forward")
    zero = _zero_case(case)
    request = _request(
        zero,
        conditions=(_condition("POSITION", "P3", "P3", "position"),),
        direction="POSITION_P3_TO_ANSWER",
        request_id="r61-at07-zero-support",
    )
    resolver = _resolver()
    resolver.bind(_binding(request, zero))

    result = resolver.resolve(request)
    assert result.result_state == "ZERO_SUPPORT"
    assert result.provenance != PROVENANCE_CANONICAL
    assert result.denominator == 0
    assert result.evidence_ref is None
    assert result.consumer_values_read is None
    with pytest.raises(EvidenceAssociationError):
        _reader(request, result).read()

    summary = reduce_required_support([result])
    assert summary.exact_all_support is False
    assert summary.productive_all_required is False
    assert summary.positive_support_count == 0
    assert summary.support_state == "ZERO_SUPPORT"


def test_changed_typed_values_and_identity_axes_refuse_same_consumer():
    case = build_provider_case("forward")
    request = _request(case)
    resolver = _resolver()
    resolver.bind(_binding(request, case))
    result = resolver.resolve(request)
    assert result.result_state == "SUPPORTED"
    _reader(request, result).read()

    changed_condition = request.changed(
        ordered_conditions=(
            _condition("POSITION", "P2", "P2", "position"),
        )
    )
    assert changed_condition.key != request.key
    assert resolver.resolve(changed_condition).result_state == "UNKNOWN"
    assert (
        resolver.resolve(changed_condition).typed_refusal
        == REFUSAL_NO_EXACT_BINDING
    )
    with pytest.raises(EvidenceAssociationError):
        _reader(changed_condition, result).read()

    mutations = {
        "edition": "2025-12",
        "byte_digest": semantic_hash({"fixture": "other-edition"}),
        "as_of_clock": "2026-02-28",
        "direction": "ANSWER_YES_TO_POSITION",
        "role": "REVERSE_AUTHORIZED",
        "design_ref": _ref("R61_DESIGN", "other-design", {"design": "OTHER"}),
        "weight_method": "GOVERNED_WEIGHTED",
        "risk_set_ref": _ref("RISK_SET", "other-risk", {"risk": "OTHER"}),
    }
    for name, value in mutations.items():
        mutated = request.changed(**{name: value})
        assert mutated.key != request.key, name
        refused = resolver.resolve(mutated)
        assert refused.result_state == "UNKNOWN", name
        assert refused.typed_refusal == REFUSAL_NO_EXACT_BINDING, name
        with pytest.raises(EvidenceAssociationError):
            _reader(mutated, result).read()

    other_target = request.changed(
        target_ref=case["source"]["qrefs"]["POSITION"],
        ordered_target_refs=(case["source"]["qrefs"]["POSITION"],),
    )
    assert other_target.key != request.key
    assert resolver.resolve(other_target).result_state == "UNKNOWN"
    with pytest.raises(EvidenceAssociationError):
        _reader(other_target, result).read()


def test_typed_encoding_is_tagged_and_duplicate_occurrence_rejected():
    int_value = TypedValue.build(1)
    string_value = TypedValue.build("1")
    bool_value = TypedValue.build(True)
    assert int_value.material() == {"tag": "INTEGER", "value": 1}
    assert string_value.material() == {"tag": "STRING", "value": "1"}
    assert bool_value.material() == {"tag": "BOOLEAN", "value": True}
    assert semantic_hash(int_value.material()) != semantic_hash(
        string_value.material()
    )
    assert semantic_hash(bool_value.material()) != semantic_hash(
        int_value.material()
    )
    with pytest.raises(EvidenceRequestShapeError):
        TypedValue.build(1.5)

    occurrence = OccurrenceKey("Y", "1", "FORM_1", "0")
    with pytest.raises(EvidenceRequestShapeError):
        EvidenceRequest(
            **{
                **_request(build_provider_case("forward")).__dict__,
                "ordered_conditions": (
                    TypedCondition(occurrence, TypedValue.build(1), "D@1"),
                    TypedCondition(occurrence, TypedValue.build(0), "D@1"),
                ),
            }
        )


def test_cache_cold_replay_and_authenticated_tamper():
    case = build_provider_case("forward")
    request = _request(case, request_id="r61-cache-cold")
    resolver = _resolver()
    resolver.bind(_binding(request, case))
    produced = resolver.resolve(request)
    assert produced.denominator == 60

    cache = resolver.export_cache()
    assert cache["schema"] == CACHE_SCHEMA
    assert len(cache["entries"]) == 1

    cold = _resolver()
    cold.import_authenticated_cache(cache)
    restored = cold.resolve(request)
    assert restored.provenance == PROVENANCE_CACHE
    assert restored.result_state == "SUPPORTED"
    assert restored.denominator == 60
    assert restored.consumer_result_hash == produced.consumer_result_hash
    assert restored.cells == produced.cells
    read = _reader(request, restored).read()
    assert read["denominator"] == 60
    assert read["cells"] == canonicalize(produced.cells)

    stale = request.changed(as_of_clock="2027-01-01")
    assert cold.resolve(stale).result_state == "UNKNOWN"

    tampered = {
        "schema": cache["schema"],
        "entries": [dict(entry) for entry in cache["entries"]],
    }
    tampered["entries"][0]["seal"] = "0" * 64
    with pytest.raises(EvidenceCacheIntegrityError):
        _resolver().import_authenticated_cache(tampered)

    payload = dict(cache["entries"][0])
    payload.pop("seal")
    payload["request_key"] = semantic_hash({"different": "request"})
    resealed = {**payload, "seal": semantic_hash(payload)}
    with pytest.raises(EvidenceCacheIntegrityError):
        _resolver().import_authenticated_cache(
            {"schema": CACHE_SCHEMA, "entries": [resealed]}
        )


def test_missing_state_controls_and_total_support_summary():
    case = build_provider_case("forward")
    request = _request(case, request_id="r61-summary-control")
    missing = _resolver().resolve(request)
    assert missing.result_state == "UNKNOWN"
    assert missing.eligibility_state == "UNKNOWN"

    valid_null = EvidenceResult(
        request_key=semantic_hash({"control": "valid-null"}),
        eligibility_state="ELIGIBLE",
        execution_state="COMPLETED",
        result_state="VALID_NULL",
        provenance="TYPED_REFUSAL",
        denominator=10,
    )
    unresolved_z = EvidenceResult(
        request_key=semantic_hash({"control": "z-unresolved"}),
        eligibility_state="ELIGIBLE",
        execution_state="COMPLETED",
        result_state="UNKNOWN",
        provenance="TYPED_REFUSAL",
        denominator=16,
        typed_refusal="Z_UNRESOLVED",
    )
    summary = reduce_required_support([missing, valid_null, unresolved_z])
    assert summary.total_required == 3
    assert summary.exact_all_support is False
    assert summary.productive_all_required is False
    assert summary.positive_support_count == 0
    assert summary.denominator_support == 26
    assert summary.unresolved_denominator_support == 16
    assert set(summary.eligibility_counts) <= ELIGIBILITY_STATES
    assert set(summary.execution_counts) <= EXECUTION_STATES
    assert set(summary.result_counts) <= RESULT_STATES
    assert summary.support_state == "UNKNOWN_SUPPORT"

    empty_valid = reduce_required_support([], valid_empty_frontier=True)
    assert empty_valid.support_state == "VALID_EMPTY"
    assert empty_valid.exact_all_support is False
    empty_unqualified = reduce_required_support([])
    assert empty_unqualified.support_state == "NO_REQUIRED_SUPPORT"

    duplicate = [valid_null, replace(valid_null)]
    with pytest.raises(Exception):
        reduce_required_support(duplicate)


def test_consumer_assertion_mutation_and_restoration():
    case = build_provider_case("forward")
    request = _request(case, request_id="r61-mutation")
    resolver = _resolver()
    resolver.bind(_binding(request, case))
    result = resolver.resolve(request)
    assert _reader(request, result).read()["denominator"] == 60

    mutated_values = dict(result.consumer_values_read)
    mutated_values["ordered_conditions"] = [
        {**mutated_values["ordered_conditions"][0], "typed_value": {"tag": "STRING", "value": "P2"}}
    ]
    mutated = replace(result, consumer_values_read=mutated_values)
    with pytest.raises(EvidenceAssociationError):
        _reader(request, mutated).read()

    restored = replace(result, consumer_values_read=result.consumer_values_read)
    assert _reader(request, restored).read()["denominator"] == 60


def test_cold_process_cache_replay_preserves_same_consumer_values():
    case = build_provider_case("forward")
    request = _request(case, request_id="r61-cold-process")
    resolver = _resolver()
    resolver.bind(_binding(request, case))
    produced = resolver.resolve(request)
    assert produced.result_state == "SUPPORTED"

    with tempfile.TemporaryDirectory() as tmp:
        cache_path = Path(tmp) / "cache.json"
        cache_path.write_text(json.dumps(resolver.export_cache()), encoding="utf-8")
        script = f"""
import json
import sys
from pathlib import Path
from rawlsing_next.tests.n10e_empirical_slice_fixture import build_provider_case
from rawlsing_next.tests.test_universal_evidence_binding import _request
from rawlsing_next.pre553_universal_evidence_binding import (
    EvidenceConsumerReader, EvidenceResolver, TrustedAdmissionVerifier,
    EvidenceCacheIntegrityError,
)
config = json.loads(sys.stdin.read())
verifier = TrustedAdmissionVerifier(bytes.fromhex(config["key_hex"]), authority_id=config["authority_id"])
case = build_provider_case("forward")
request = _request(case, request_id="r61-cold-process")
cache = json.loads(Path({str(cache_path)!r}).read_text(encoding="utf-8"))
resolver = EvidenceResolver(admission_verifier=verifier)
resolver.import_authenticated_cache(cache)
result = resolver.resolve(request)
values = EvidenceConsumerReader(request, result, verifier=verifier).read()
reexported = resolver.export_cache()
again = EvidenceResolver(admission_verifier=verifier)
again.import_authenticated_cache(reexported)
rewritten = again.resolve(request)
rewritten_values = EvidenceConsumerReader(
    request, rewritten, verifier=verifier
).read()
assert not resolver._bindings and not again._bindings
assert resolver._executor is None and again._executor is None
assert resolver._admitted_producer is None and again._admitted_producer is None
assert reexported["entries"][0]["envelope_signature"] == cache["entries"][0]["envelope_signature"]
assert reexported["entries"][0]["cache_owner_descriptor"] == cache["entries"][0]["cache_owner_descriptor"]
refusals = []
for control in (
    EvidenceResolver(),
    EvidenceResolver(admission_verifier=TrustedAdmissionVerifier(b"W" * 32, authority_id=config["authority_id"])),
):
    try:
        control.import_authenticated_cache(cache)
    except EvidenceCacheIntegrityError:
        refusals.append("TYPED_REFUSAL")
    else:
        raise AssertionError("cold wrong/missing configured root accepted")
print(json.dumps({{
    "provenance": result.provenance,
    "state": result.result_state,
    "denominator": result.denominator,
    "consumer_denominator": values["denominator"],
    "consumer_hash": result.consumer_result_hash,
    "reexport_denominator": rewritten.denominator,
    "reexport_consumer_denominator": rewritten_values["denominator"],
    "original_execution_provenance": rewritten_values[
        "original_execution_provenance"
    ],
    "cells": {{cell["cell"]: cell["raw_numerator_support"] for cell in rewritten_values["cells"]}},
    "signature_preserved": True,
    "verifier_only": True,
    "missing_wrong_root": refusals,
}}, sort_keys=True))
"""
        completed = subprocess.run(
            [sys.executable, "-c", script],
            cwd=Path(__file__).resolve().parents[2],
            input=json.dumps({"key_hex": _R4_ISSUER.key_hex, "authority_id": _R4_ISSUER.authority_id}),
            text=True,
            capture_output=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stderr
        observed = json.loads(completed.stdout.strip().splitlines()[-1])
    assert observed == {
        "provenance": "AUTHENTICATED_CACHE",
        "state": "SUPPORTED",
        "denominator": 60,
        "consumer_denominator": 60,
        "consumer_hash": produced.consumer_result_hash,
        "reexport_denominator": 60,
        "reexport_consumer_denominator": 60,
        "original_execution_provenance": "CANONICAL_PRODUCER",
        "cells": {"no": 6, "yes": 54},
        "signature_preserved": True,
        "verifier_only": True,
        "missing_wrong_root": ["TYPED_REFUSAL", "TYPED_REFUSAL"],
    }


def test_wrong_actual_condition_or_admitted_labels_refuse_positive():
    case = build_provider_case("forward")
    wrong_condition = _request(
        case,
        conditions=(_condition("POSITION", "P2", "P2", "position"),),
        request_id="r61-r2-wrong-condition",
    )
    resolver = _resolver()
    resolver.bind(_binding(wrong_condition, case))
    result = resolver.resolve(wrong_condition)
    assert result.result_state == "UNKNOWN"
    assert result.typed_refusal == "IDENTITY_MISMATCH"
    with pytest.raises(EvidenceAssociationError):
        _reader(wrong_condition, result).read()

    labelled = build_provider_case("forward")
    wrong_labels = _request(
        labelled,
        edition="2025-12",
        source_id="OTHER_SOURCE",
        byte_digest=semantic_hash({"fixture": "other-edition"}),
        as_of_clock="2026-02-28",
        direction="ANSWER_YES_TO_POSITION",
        role="REVERSE_AUTHORIZED",
        design_ref=_ref("R61_DESIGN", "other-design", {"design": "OTHER"}),
        weight_method="GOVERNED_WEIGHTED",
        request_id="r61-r2-wrong-labels",
    )
    labelled_resolver = _resolver()
    labelled_resolver.bind(_binding(wrong_labels, labelled))
    refused = labelled_resolver.resolve(wrong_labels)
    assert refused.result_state == "UNKNOWN"
    assert refused.typed_refusal == "IDENTITY_MISMATCH"


def test_cache_carries_full_k_and_issuer_boundary_rejects_self_seal():
    case = build_provider_case("forward")
    request = _request(case, request_id="r61-r2-cache-preimage")
    resolver = _resolver()
    resolver.bind(_binding(request, case))
    resolver.resolve(request)
    entry = resolver.export_cache()["entries"][0]
    assert entry["request_material"]["request_id"] == "r61-r2-cache-preimage"
    assert semantic_hash(entry["request_material"]) == entry["request_key"]
    assert entry["cache_owner_descriptor"]["validated_conditions"] == [
        condition.material() for condition in request.ordered_conditions
    ]

    issuer = TrustedCacheIssuer()
    issued_resolver = _resolver(cache_issuer=issuer)
    issued_resolver.bind(_binding(request, case))
    issued_resolver.resolve(request)
    issued_cache = issued_resolver.export_cache()
    assert issued_cache["entries"][0]["issuer_grade"] == "EPHEMERAL_ISSUER_HMAC_SHA256"

    with pytest.raises(EvidenceCacheIntegrityError):
        _resolver(cache_issuer=TrustedCacheIssuer()).import_authenticated_cache(
            issued_cache
        )
    same_key = TrustedCacheIssuer(bytes.fromhex(issuer.key_hex))
    cold = _resolver(cache_issuer=same_key)
    cold.import_authenticated_cache(issued_cache)
    restored = cold.resolve(request)
    assert restored.result_state == "SUPPORTED"
    assert restored.denominator == 60

    wrong_root = _resolver(
        cache_issuer=same_key,
        admission_verifier=TrustedAdmissionAuthority().verifier(),
    )
    with pytest.raises(EvidenceCacheIntegrityError):
        wrong_root.import_authenticated_cache(issued_cache)


def test_valid_products_preserve_support_state_and_z_unresolved():
    controls = [
        EvidenceResult(
            request_key=semantic_hash({"control": state}),
            eligibility_state="ELIGIBLE",
            execution_state="COMPLETED",
            result_state=state,
            provenance="TYPED_REFUSAL",
            denominator=10,
        )
        for state in ("VALID_NULL", "DIFFUSE", "VALID_EMPTY", "OBSERVED_ZERO")
    ]
    for control in controls:
        summary = reduce_required_support([control])
        assert summary.productive_all_required is True
        assert summary.exact_all_support is False
        assert summary.support_state != "NO_SUPPORT"
        assert summary.support_state.startswith(control.result_state)
    unresolved = EvidenceResult(
        request_key=semantic_hash({"control": "Z"}),
        eligibility_state="ELIGIBLE",
        execution_state="COMPLETED",
        result_state="UNKNOWN",
        provenance="TYPED_REFUSAL",
        denominator=16,
        typed_refusal="Z_UNRESOLVED",
    )
    summary = reduce_required_support([unresolved])
    assert summary.support_state == "UNKNOWN_SUPPORT"
    assert summary.unresolved_denominator_support == 16
    assert summary.exact_all_support is False


def test_actual_observed_zero_cell_remains_supported_product():
    rows = [
        {"id": f"P1Y{n:03d}", "responses": {"POSITION": "P1", "ANSWER": "yes"}}
        for n in range(1, 61)
    ] + [
        {"id": f"P2N{n:03d}", "responses": {"POSITION": "P2", "ANSWER": "no"}}
        for n in range(1, 41)
    ]
    with frozen_at07_source(
        tag="r61-observed-zero",
        rows=rows,
        scope_query_authority_to_universe=True,
    ) as (source, query_authority, registry):
        predicate, producer_query = build_producer(source, query_authority, "forward")
        consumer_query, conditioner_binding = build_consumer(source, "forward")
        witness = build_witness(
            source,
            "forward",
            consumer_query,
            conditioner_binding,
            producer_query,
            predicate,
        )
        case = {
            "source": source,
            "query_authority": query_authority,
            "registry": registry,
            "predicate": predicate,
            "empirical_query": producer_query,
            "consumer_query": consumer_query,
            "condition_binding_witness": witness,
            "model_rule": build_model_rule(source),
            "release_refs": (source["release_ref"],),
        }
        request = _request(case, request_id="r61-observed-zero")
        resolver = _resolver()
        resolver.bind(_binding(request, case))
        result = resolver.resolve(request)
    assert result.result_state == "SUPPORTED"
    assert result.denominator == 60
    cells = {cell["cell"]: cell["raw_numerator_support"] for cell in result.cells}
    assert cells == {"no": 0, "yes": 60}
    summary = reduce_required_support([result])
    assert summary.exact_all_support is True
    assert summary.support_state == "EXACT_SUPPORT"


def _forged_admitted_context(case):
    return replace(
        _make_context(case),
        source_id="FORGED_SOURCE",
        dataset_id="FORGED_DATASET",
        wave_id="FORGED_WAVE",
        edition="1999-01",
        byte_digest=semantic_hash({"forged": "source-bytes"}),
        instrument_version="FORGED_INSTRUMENT@9",
        sampled_unit="FORGED_SAMPLED_UNIT",
        reporting_unit="FORGED_REPORTING_UNIT",
        estimand="FORGED_ESTIMAND",
        weight_method="FORGED_WEIGHT_METHOD",
        design_ref=_ref("R61_DESIGN", "forged-design", {"design": "FORGED"}),
        uncertainty_method="FORGED_UNCERTAINTY_METHOD",
        direction="ANSWER_YES_TO_POSITION",
        role="REVERSE_AUTHORIZED",
        consumer_use="FORGED_CONSUMER_USE",
        grammar_version="FORGED_GRAMMAR@9",
        custody_ref=_ref("R61_CUSTODY", "forged-custody", {"custody": "FORGED"}),
        observation_clock="1999-01",
        reference_clock="1999-01",
        as_of_clock="1999-01-31",
        publication_clock="1999-02-01",
        permission_ref=_ref("R61_PERMISSION", "forged-permission", {"scope": "FORGED"}),
    )


def test_forged_caller_context_cannot_mint_owner_admission():
    case = build_provider_case("forward")
    forged = _forged_admitted_context(case)
    case["_r61_context"] = forged
    request = _request(
        case,
        request_id="r61-r3-forged-context",
        source_id=forged.source_id,
        dataset_id=forged.dataset_id,
        wave_id=forged.wave_id,
        edition=forged.edition,
        byte_digest=forged.byte_digest,
        instrument_version=forged.instrument_version,
        sampled_unit=forged.sampled_unit,
        reporting_unit=forged.reporting_unit,
        estimand=forged.estimand,
        weight_method=forged.weight_method,
        design_ref=forged.design_ref,
        uncertainty_method=forged.uncertainty_method,
        direction=forged.direction,
        role=forged.role,
        consumer_use=forged.consumer_use,
        grammar_version=forged.grammar_version,
        custody_ref=forged.custody_ref,
        observation_clock=forged.observation_clock,
        reference_clock=forged.reference_clock,
        as_of_clock=forged.as_of_clock,
        publication_clock=forged.publication_clock,
        permission_ref=forged.permission_ref,
    )
    resolver = _resolver()
    resolver.bind(_binding(request, case))
    result = resolver.resolve(request)
    assert result.result_state == "UNKNOWN"
    assert result.typed_refusal == "OWNER_ADMISSION_UNRESOLVED"
    with pytest.raises(EvidenceAssociationError):
        _reader(request, result).read()


def test_default_cache_rejects_missing_admission_and_forged_same_source_evidence():
    case = build_provider_case("forward")
    request = _request(case, request_id="r61-r3-cache-admission")
    resolver = _resolver()
    resolver.bind(_binding(request, case))
    produced = resolver.resolve(request)
    assert produced.result_state == "SUPPORTED"
    base = resolver.export_cache()["entries"][0]

    no_envelope = {
        key: canonicalize(value)
        for key, value in base.items()
        if key not in {"seal", "issuer_seal", "issuer_grade", "execution_envelope", "envelope_signature"}
    }
    no_envelope["seal"] = semantic_hash(no_envelope)
    with pytest.raises(EvidenceCacheIntegrityError):
        _resolver().import_authenticated_cache(
            {"schema": CACHE_SCHEMA, "entries": [no_envelope]}
        )

    forged = {
        key: canonicalize(value)
        for key, value in base.items()
        if key not in {"seal", "issuer_seal", "issuer_grade"}
    }
    evidence_material = dict(canonicalize(_evidence_material(produced.evidence_object)))
    evidence_material["raw_support"] = 999
    geometry = dict(evidence_material["geometry"])
    geometry["cells"] = [
        {
            **canonicalize(cell),
            "raw_numerator_support": 999 if cell.get("cell") == "yes" else 0,
        }
        for cell in geometry["cells"]
    ]
    evidence_material["geometry"] = geometry
    forged["evidence"] = canonicalize(evidence_material)
    result_material = dict(canonicalize(forged["result"]))
    result_material["denominator"] = 999
    result_material["cells"] = [
        canonicalize({k: cell.get(k) for k in ("cell", "cell_state", "raw_numerator_support", "raw_probability_exact_fraction")})
        for cell in geometry["cells"]
    ]
    forged["result"] = canonicalize(result_material)
    forged["seal"] = semantic_hash(
        {key: value for key, value in forged.items() if key != "seal"}
    )
    with pytest.raises(EvidenceCacheIntegrityError):
        _resolver().import_authenticated_cache(
            {"schema": CACHE_SCHEMA, "entries": [forged]}
        )


def test_default_unconfigured_resolver_and_reader_refuse_admitted_support():
    case = build_provider_case("forward")
    request = _request(case, request_id="r61-r4-unconfigured")
    binding = _binding(request, case)
    resolver = EvidenceResolver()
    resolver.bind(binding)
    result = resolver.resolve(request)
    assert result.result_state == "UNKNOWN"
    assert result.typed_refusal == "NO_CONFIGURED_TRUST_ROOT"
    with pytest.raises(EvidenceAssociationError):
        EvidenceConsumerReader(request, result).read()
    with pytest.raises(EvidenceCacheIntegrityError):
        EvidenceResolver().import_authenticated_cache(
            {"schema": CACHE_SCHEMA, "entries": []}
        )


def test_attacker_issuer_and_fabricated_envelope_do_not_satisfy_real_reader():
    case = build_provider_case("forward")
    request = _request(case, request_id="r61-r4-attacker-issuer")
    resolver = _resolver()
    resolver.bind(_binding(request, case))
    produced = resolver.resolve(request)
    assert produced.result_state == "SUPPORTED"

    attacker = TrustedAdmissionAuthority()
    assert attacker.authority_id == _R4_ISSUER.authority_id
    forged_signature = attacker.issue_envelope(produced.execution_envelope)
    forged = replace(produced, envelope_signature=forged_signature)
    with pytest.raises(EvidenceAssociationError):
        _reader(request, forged).read()

    swapped = replace(produced, envelope_signature=produced.envelope_signature)
    assert _reader(request, swapped).read()["denominator"] == 60


def test_callable_substitution_and_signed_envelope_metadata_mutation_refuse():
    case = build_provider_case("forward")
    request = _request(case, request_id="r61-r4-callable-pin")
    resolver = _resolver()

    def forged_producer(**kwargs):
        raise AssertionError("forged producer must never execute")

    substituted = _binding(request, case, producer=forged_producer)
    resolver.bind(substituted)
    result = resolver.resolve(request)
    assert result.result_state == "UNKNOWN"
    assert result.typed_refusal == "OWNER_ADMISSION_UNRESOLVED"

    good = _resolver()
    good.bind(_binding(request, case))
    produced = good.resolve(request)
    mutated_envelope = replace(
        produced.execution_envelope, result_state="ZERO_SUPPORT"
    )
    mutated = replace(produced, execution_envelope=mutated_envelope)
    with pytest.raises(EvidenceAssociationError):
        _reader(request, mutated).read()

    base = good.export_cache()["entries"][0]
    altered = {
        key: canonicalize(value)
        for key, value in base.items()
        if key not in {"seal", "issuer_seal", "issuer_grade"}
    }
    result_material = dict(canonicalize(altered["result"]))
    result_material["result_state"] = "ZERO_SUPPORT"
    altered["result"] = canonicalize(result_material)
    altered["seal"] = semantic_hash(altered)
    with pytest.raises(EvidenceCacheIntegrityError):
        _resolver().import_authenticated_cache(
            {"schema": CACHE_SCHEMA, "entries": [altered]}
        )


def test_reader_serves_only_signed_projection_for_all_mutated_fields():
    case = build_provider_case("forward")
    request = _request(case, request_id="r61-r5-signed-projection")
    resolver = _resolver()
    resolver.bind(_binding(request, case))
    produced = resolver.resolve(request)
    assert _reader(request, produced).read()["denominator"] == 60

    values = dict(produced.consumer_values_read)
    values["denominator"] = 999
    values["result_state"] = "ZERO_SUPPORT"
    values["evidence_ref"] = {
        "kind": "FORGED_EVIDENCE",
        "object_id": "urn:forged:evidence",
        "content_hash": semantic_hash({"forged": "evidence"}),
    }
    values["cells"] = [
        {
            "cell": "yes",
            "cell_state": "FORGED",
            "raw_numerator_support": 999,
            "raw_probability_exact_fraction": {"$exact_fraction": [1, 1]},
        }
    ]
    mutated_values = replace(produced, consumer_values_read=values)
    with pytest.raises(EvidenceAssociationError):
        _reader(request, mutated_values).read()
    with pytest.raises(EvidenceAssociationError):
        _reader(request, mutated_values).e04_step()

    metadata_mutations = (
        {"producer_fact_state": "FORGED_FACT_STATE"},
        {"uncertainty_state": "FORGED_UNCERTAINTY"},
        {"producer_receipt_ref": None},
        {"producer_fact_ref": None},
        {"consumer_query_ref": _ref("R61_QUERY", "forged-query", {"q": "FORGED"})},
        {
            "evidence_ref": _ref(
                "R61_EVIDENCE", "forged-evidence", {"e": "FORGED"}
            )
        },
        {"consumer_result_hash": semantic_hash({"forged": "consumer"})},
        {"eligibility_state": "HELD"},
        {"execution_state": "ERROR"},
        {"result_state": "ZERO_SUPPORT"},
        {"denominator": 999},
        {"cells": ()},
    )
    for changes in metadata_mutations:
        try:
            mutated = replace(produced, **changes)
        except EvidenceBindingError:
            continue
        with pytest.raises(EvidenceAssociationError):
            _reader(request, mutated).read()

    assert _reader(request, produced).read()["denominator"] == 60


def test_missing_live_producer_pin_is_fail_closed_before_execution():
    case = build_provider_case("forward")
    request = _request(case, request_id="r61-r5-missing-pin")
    calls = []

    def substituted_producer(**kwargs):
        calls.append("called")
        raise RuntimeError("SUBSTITUTED_PRODUCER_EXECUTED")

    resolver = EvidenceResolver(
        admission_verifier=_R4_VERIFIER,
        executor=_R4_ISSUER,
    )
    binding = _binding(request, case, producer=substituted_producer)
    resolver.bind(binding)
    result = resolver.resolve(request)
    assert calls == []
    assert result.result_state == "UNKNOWN"
    assert result.typed_refusal == "OWNER_ADMISSION_UNRESOLVED"

    legitimate_without_pin = EvidenceResolver(
        admission_verifier=_R4_VERIFIER,
        executor=_R4_ISSUER,
    )
    legitimate_without_pin.bind(_binding(request, case))
    refused = legitimate_without_pin.resolve(request)
    assert refused.result_state == "UNKNOWN"
    assert refused.typed_refusal == "OWNER_ADMISSION_UNRESOLVED"


def test_export_refuses_unsigned_result_mutation_and_cache_projection_is_signed():
    case = build_provider_case("forward")
    request = _request(case, request_id="r61-r5-export-projection")
    resolver = _resolver()
    resolver.bind(_binding(request, case))
    produced = resolver.resolve(request)
    mutated_values = dict(produced.consumer_values_read)
    mutated_values["denominator"] = 999
    mutated = replace(produced, consumer_values_read=mutated_values)

    tampered_resolver = _resolver()
    tampered_resolver.bind(_binding(request, case))
    tampered_resolver.resolve(request)
    tampered_resolver._cache[request.key] = mutated
    with pytest.raises(EvidenceCacheIntegrityError):
        tampered_resolver.export_cache()

    cache = resolver.export_cache()
    entry = cache["entries"][0]
    projection = entry["result"]
    assert projection["denominator"] == 60
    assert projection["evidence_ref"] == produced.execution_envelope.evidence_ref.as_dict()
    assert projection["consumer_values_read"] == canonicalize(
        produced.execution_envelope.consumer_values_read
    )


def test_provenance_mutation_cannot_change_signed_original_execution_or_grade():
    case = build_provider_case("forward")
    request = _request(case, request_id="r61-r6-provenance")
    resolver = _resolver()
    resolver.bind(_binding(request, case))
    produced = resolver.resolve(request)
    read = _reader(request, produced).read()
    assert read["original_execution_provenance"] == PROVENANCE_CANONICAL
    assert read["original_execution_mode"] == "LIVE_TRUSTED_EXECUTION"
    assert "cache_trust_grade" not in read

    mutated = replace(produced, provenance=PROVENANCE_CACHE)
    mutated_read = _reader(request, mutated).read()
    assert mutated_read["original_execution_provenance"] == PROVENANCE_CANONICAL
    assert "local_delivery_context_unsigned" not in mutated_read
    assert "cache_trust_grade" not in mutated_read

    cache = resolver.export_cache()
    cold = _resolver()
    cold.import_authenticated_cache(cache)
    restored = cold.resolve(request)
    cold_read = _reader(request, restored).read()
    assert cold_read["original_execution_provenance"] == PROVENANCE_CANONICAL
    assert "local_delivery_context_unsigned" not in cold_read
    assert "cache_trust_grade" not in cold_read

    mislabeled = replace(restored, provenance=PROVENANCE_CANONICAL)
    mislabeled_read = _reader(request, mislabeled).read()
    assert mislabeled_read["original_execution_provenance"] == PROVENANCE_CANONICAL
    assert "cache_trust_grade" not in mislabeled_read


def test_export_refuses_mutated_evidence_query_and_rule_objects():
    case = build_provider_case("forward")
    request = _request(case, request_id="r61-r6-export-objects")
    resolver = _resolver()
    resolver.bind(_binding(request, case))
    produced = resolver.resolve(request)

    original_cell = produced.evidence_object.geometry["cells"][0]["raw_numerator_support"]
    assert original_cell == 6
    produced.evidence_object.geometry["cells"][0]["raw_numerator_support"] = 999
    with pytest.raises(EvidenceCacheIntegrityError):
        resolver.export_cache()
    with pytest.raises(EvidenceAssociationError):
        _reader(request, produced).read()

    produced.evidence_object.geometry["cells"][0]["raw_numerator_support"] = original_cell
    assert _reader(request, produced).read()["denominator"] == 60
    resolver.export_cache()
    original_query_material = canonicalize(produced.consumer_query_object.material())
    produced.consumer_query_object.requested_projection["kind"] = "FORGED"
    with pytest.raises(EvidenceCacheIntegrityError):
        resolver.export_cache()
    produced.consumer_query_object.requested_projection["kind"] = (
        original_query_material["requested_projection"]["kind"]
    )

    assert _reader(request, produced).read()["denominator"] == 60
    resolver.export_cache()
    forged_rule = replace(
        produced.model_rule_object,
        source_universe_refs=(
            _ref("R61_SOURCE", "forged-rule-source", {"source": "FORGED"}),
        ),
    )
    forged_rule_result = replace(produced, model_rule_object=forged_rule)
    tampered = _resolver()
    tampered.bind(_binding(request, case))
    tampered.resolve(request)
    tampered._cache[request.key] = forged_rule_result
    with pytest.raises(EvidenceCacheIntegrityError):
        tampered.export_cache()
    with pytest.raises(EvidenceAssociationError):
        _reader(request, forged_rule_result).read()
    tampered._cache[request.key] = produced
    assert _reader(request, produced).read()["denominator"] == 60
    tampered.export_cache()


def test_verifier_only_re_export_preserves_signed_execution_projection():
    case = build_provider_case("forward")
    request = _request(case, request_id="r61-r6-reexport")
    resolver = _resolver()
    resolver.bind(_binding(request, case))
    produced = resolver.resolve(request)
    cache = resolver.export_cache()

    verifier_only = EvidenceResolver(admission_verifier=_R4_VERIFIER)
    verifier_only.import_authenticated_cache(cache)
    restored = verifier_only.resolve(request)
    assert restored.denominator == 60
    assert _reader(request, restored).read()["original_execution_provenance"] == PROVENANCE_CANONICAL

    reexported = verifier_only.export_cache()
    entry = reexported["entries"][0]
    assert entry["envelope_signature"] == cache["entries"][0]["envelope_signature"]
    assert entry["result"]["denominator"] == 60
    assert entry["result"]["consumer_values_read"] == canonicalize(
        produced.execution_envelope.consumer_values_read
    )

    third = EvidenceResolver(admission_verifier=_R4_VERIFIER)
    third.import_authenticated_cache(reexported)
    again = third.resolve(request)
    assert again.denominator == 60
    assert _reader(request, again).read()["denominator"] == 60


def test_swapped_signed_envelope_from_other_request_refuses():
    case = build_provider_case("forward")
    request_a = _request(case, request_id="r61-r6-envelope-a")
    request_b = _request(case, request_id="r61-r6-envelope-b")
    resolver = _resolver()
    resolver.bind(_binding(request_a, case))
    produced_a = resolver.resolve(request_a)
    resolver_b = _resolver()
    resolver_b.bind(_binding(request_b, case))
    produced_b = resolver_b.resolve(request_b)
    swapped = replace(
        produced_a,
        execution_envelope=produced_b.execution_envelope,
        envelope_signature=produced_b.envelope_signature,
    )
    with pytest.raises(EvidenceAssociationError):
        _reader(request_a, swapped).read()


# Frozen independent inventory copied from the pre-code contract, not derived
# from the implementation's field whitelist.
_R7_OWNER_CLASSES = (
    "context_ref", "context", "actual_conditions", "producer_query_ref",
    "predicate_ref", "predicate_hash", "release_refs", "consumer_query_ref",
    "consumer_binding_fingerprint", "model_rule_hash", "source_universe_ref",
    "risk_set_ref", "target_ref",
)


@pytest.fixture(scope="module")
def r7_native_cache():
    case = build_provider_case("forward")
    request = _request(case, request_id="r61-r7-independent-inventory")
    resolver = _resolver()
    resolver.bind(_binding(request, case))
    result = resolver.resolve(request)
    assert {cell["cell"]: cell["raw_numerator_support"] for cell in result.cells} == {"no": 6, "yes": 54}
    assert _reader(request, result).read()["denominator"] == 60
    return request, resolver.export_cache(), result


def _r7_reseal(cache):
    for entry in cache["entries"]:
        descriptor = entry["cache_owner_descriptor"]
        if isinstance(descriptor, dict):
            owner = descriptor.get("owner_identity_material")
            if isinstance(owner, dict):
                descriptor["owner_identity_hash"] = semantic_hash(owner)
            descriptor["descriptor_hash"] = semantic_hash({k: v for k, v in descriptor.items() if k != "descriptor_hash"})
        entry["seal"] = semantic_hash({k: v for k, v in entry.items() if k not in {"seal", "issuer_seal", "issuer_grade"}})
    return cache


def _r7_chain(request, cache):
    """The same configured verifier and consumer through the full transport chain."""
    first = EvidenceResolver(admission_verifier=_R4_VERIFIER)
    first.import_authenticated_cache(cache)
    result = first.resolve(request)
    first_values = _reader(request, result).read()
    exported = first.export_cache()
    second = EvidenceResolver(admission_verifier=_R4_VERIFIER)
    second.import_authenticated_cache(exported)
    second_values = _reader(request, second.resolve(request)).read()
    assert first_values["denominator"] == second_values["denominator"] == 60
    assert exported["entries"][0]["envelope_signature"] == cache["entries"][0]["envelope_signature"]
    assert first_values["cells"] == second_values["cells"]
    assert {cell["cell"]: cell["raw_numerator_support"] for cell in second_values["cells"]} == {"no": 6, "yes": 54}
    assert second_values["original_execution_provenance"] == PROVENANCE_CANONICAL
    assert "local_delivery_context_unsigned" not in second_values
    return exported


def _r7_changed(value):
    if isinstance(value, dict):
        out = copy.deepcopy(value)
        first_key = next(iter(out))
        out[first_key] = _r7_changed(out[first_key])
        return out
    if isinstance(value, list):
        return [_r7_changed(value[0]), *copy.deepcopy(value[1:])] if value else ["FORGED"]
    return "FORGED:" + str(value)


@pytest.mark.parametrize("owner_class", _R7_OWNER_CLASSES)
@pytest.mark.parametrize("attack", ("mutate", "remove", "duplicate", "type_alias"))
def test_r7_every_declared_owner_class_rejects_public_resealed_transport(r7_native_cache, owner_class, attack):
    request, baseline, _ = r7_native_cache
    assert set(_R7_OWNER_CLASSES) == CACHE_OWNER_FIELDS
    cache = copy.deepcopy(baseline)
    descriptor = cache["entries"][0]["cache_owner_descriptor"]
    owner = descriptor["owner_identity_material"]
    if attack == "mutate":
        owner[owner_class] = _r7_changed(owner[owner_class])
    elif attack == "remove":
        del owner[owner_class]
    elif attack == "duplicate":
        # Mapping ingress cannot represent repeated identical JSON keys. This
        # tests the forbidden independently authoritative compatibility copy.
        descriptor[owner_class] = copy.deepcopy(owner[owner_class])
    else:
        owner[owner_class] = {"aliased_value": owner[owner_class]}
    _r7_reseal(cache)
    with pytest.raises(EvidenceCacheIntegrityError):
        _r7_chain(request, cache)
    assert _r7_chain(request, copy.deepcopy(baseline)) == baseline


def test_r7_normal_form_has_no_live_admission_or_second_owner_projection(r7_native_cache):
    request, cache, _ = r7_native_cache
    entry = cache["entries"][0]
    descriptor = entry["cache_owner_descriptor"]
    assert set(descriptor) == CACHE_OWNER_DESCRIPTOR_FIELDS
    assert descriptor["schema"] == CACHE_OWNER_DESCRIPTOR_SCHEMA == "R61_CACHE_OWNER_DESCRIPTOR@1"
    assert cache["schema"] == "R61_AUTHENTICATED_EVIDENCE_CACHE@5"
    assert set(descriptor["owner_identity_material"]) == set(_R7_OWNER_CLASSES)
    assert "producer_binding" not in entry
    assert "binding_hash" not in descriptor
    assert "admission" not in descriptor
    assert descriptor["descriptor_hash"] == semantic_hash({k: v for k, v in descriptor.items() if k != "descriptor_hash"})
    assert _r7_chain(request, copy.deepcopy(cache)) == cache


@pytest.mark.parametrize("location", ("descriptor", "owner", "entry", "envelope"))
@pytest.mark.parametrize("name", ("admission", "unknown_field"))
def test_r7_admission_and_unknown_authority_fields_never_travel(r7_native_cache, location, name):
    request, baseline, _ = r7_native_cache
    cache = copy.deepcopy(baseline)
    entry = cache["entries"][0]
    targets = {"descriptor": entry["cache_owner_descriptor"], "owner": entry["cache_owner_descriptor"]["owner_identity_material"], "entry": entry, "envelope": entry["execution_envelope"]}
    targets[location][name] = {"token": "0" * 64}
    _r7_reseal(cache)
    with pytest.raises(EvidenceCacheIntegrityError):
        _r7_chain(request, cache)
    _r7_chain(request, copy.deepcopy(baseline))


@pytest.mark.parametrize("owner_class", _R7_OWNER_CLASSES)
def test_r7_even_valid_signature_cannot_excuse_owner_envelope_disagreement(r7_native_cache, owner_class):
    request, baseline, original = r7_native_cache
    owner = copy.deepcopy(original.execution_envelope.owner_identity_material)
    owner[owner_class] = _r7_changed(owner[owner_class])
    envelope = replace(original.execution_envelope, owner_identity_material=owner, owner_identity_hash=semantic_hash(owner))
    signature = _R4_ISSUER.issue_envelope(envelope)  # trusted synthetic inconsistency control
    result = replace(original, execution_envelope=envelope, envelope_signature=signature)
    with pytest.raises(EvidenceAssociationError):
        _reader(request, result).read()
    cache = copy.deepcopy(baseline)
    cache["entries"][0]["execution_envelope"] = canonicalize(envelope.material())
    cache["entries"][0]["envelope_signature"] = signature
    cache["entries"][0]["cache_owner_descriptor"]["owner_identity_material"] = owner
    _r7_reseal(cache)
    with pytest.raises(EvidenceCacheIntegrityError):
        _r7_chain(request, cache)
    _r7_chain(request, copy.deepcopy(baseline))


@pytest.mark.parametrize("legacy", ("R61_AUTHENTICATED_EVIDENCE_CACHE@4", "R61_AUTHENTICATED_EVIDENCE_CACHE@3", "UNKNOWN"))
def test_r7_legacy_schema_and_binding_pins_explicitly_refuse(r7_native_cache, legacy):
    request, baseline, _ = r7_native_cache
    cache = copy.deepcopy(baseline)
    cache["schema"] = legacy
    with pytest.raises(EvidenceCacheIntegrityError, match="LEGACY_OR_UNKNOWN_CACHE_SCHEMA"):
        _r7_chain(request, cache)
    configured = EvidenceResolver(admission_verifier=_R4_VERIFIER, trusted_binding_hashes=("a" * 64,))
    with pytest.raises(EvidenceCacheIntegrityError, match="LEGACY_BINDING_PINS_REQUIRE_MIGRATION"):
        configured.import_authenticated_cache(baseline)
    with pytest.raises(EvidenceCacheIntegrityError, match="LEGACY_BINDING_PINS_REQUIRE_MIGRATION"):
        configured.export_cache()
    _r7_chain(request, copy.deepcopy(baseline))


def test_r7_descriptor_pins_are_distinct_and_enforced(r7_native_cache):
    request, baseline, _ = r7_native_cache
    descriptor_hash = baseline["entries"][0]["cache_owner_descriptor"]["descriptor_hash"]
    correct = EvidenceResolver(admission_verifier=_R4_VERIFIER, trusted_descriptor_hashes=(descriptor_hash,))
    correct.import_authenticated_cache(baseline)
    assert _reader(request, correct.resolve(request)).read()["denominator"] == 60
    correct.export_cache()
    wrong = EvidenceResolver(admission_verifier=_R4_VERIFIER, trusted_descriptor_hashes=("a" * 64,))
    with pytest.raises(EvidenceCacheIntegrityError, match="CACHE_OWNER_DESCRIPTOR_NOT_PINNED"):
        wrong.import_authenticated_cache(baseline)
    case = build_provider_case("forward")
    live = _resolver(trusted_descriptor_hashes=("a" * 64,))
    live.bind(_binding(request, case))
    assert live.resolve(request).denominator == 60
    with pytest.raises(EvidenceCacheIntegrityError, match="CACHE_OWNER_DESCRIPTOR_NOT_PINNED"):
        live.export_cache()
    assert live.resolve(request).result_state == "UNKNOWN"


@pytest.mark.parametrize("attack", ("null_descriptor", "wrong_descriptor_schema", "conditions_bool", "condition_order_duplicate", "release_order_duplicate", "wrong_owner_hash", "wrong_descriptor_hash", "old_binding_entry"))
def test_r7_descriptor_shape_typed_conditions_and_order_refuse(r7_native_cache, attack):
    request, baseline, _ = r7_native_cache
    cache = copy.deepcopy(baseline)
    entry = cache["entries"][0]
    desc = entry["cache_owner_descriptor"]
    if attack == "null_descriptor":
        entry["cache_owner_descriptor"] = None
    elif attack == "wrong_descriptor_schema":
        desc["schema"] = "R61_CACHE_OWNER_DESCRIPTOR@0"
    elif attack == "conditions_bool":
        desc["validated_conditions"][0]["typed_value"] = {"tag": "BOOLEAN", "value": True}
    elif attack == "condition_order_duplicate":
        desc["owner_identity_material"]["actual_conditions"] *= 2
    elif attack == "release_order_duplicate":
        desc["owner_identity_material"]["release_refs"] *= 2
    elif attack == "old_binding_entry":
        entry["producer_binding"] = {"admission": {"token": "0" * 64}}
    _r7_reseal(cache)
    if attack == "wrong_owner_hash":
        desc["owner_identity_hash"] = "0" * 64
    elif attack == "wrong_descriptor_hash":
        desc["descriptor_hash"] = "0" * 64
    entry["seal"] = semantic_hash({k: v for k, v in entry.items() if k != "seal"})
    with pytest.raises(EvidenceCacheIntegrityError):
        _r7_chain(request, cache)
    _r7_chain(request, copy.deepcopy(baseline))


def test_r7_deep_detachment_and_retained_descriptor_mutation(r7_native_cache):
    request, baseline, _ = r7_native_cache
    supplied = copy.deepcopy(baseline)
    resolver = EvidenceResolver(admission_verifier=_R4_VERIFIER)
    resolver.import_authenticated_cache(supplied)
    supplied["entries"][0]["cache_owner_descriptor"]["owner_identity_material"]["producer_query_ref"]["object_id"] = "FORGED"
    assert _reader(request, resolver.resolve(request)).read()["denominator"] == 60
    exported = resolver.export_cache()
    exported["entries"][0]["cache_owner_descriptor"]["owner_identity_material"]["context"]["source_identity"]["source_id"] = "FORGED"
    assert resolver.export_cache() == baseline
    retained = resolver._cache_descriptors[request.key]
    saved = copy.deepcopy(retained)
    retained["owner_identity_material"]["producer_query_ref"]["object_id"] = "FORGED"
    with pytest.raises(EvidenceCacheIntegrityError):
        resolver.export_cache()
    assert resolver.resolve(request).result_state == "UNKNOWN"
    resolver._cache_descriptors[request.key] = saved
    assert _reader(request, resolver.resolve(request)).read()["denominator"] == 60
    assert resolver.export_cache() == baseline


def test_r7_changed_actual_source_law_and_no_live_invocation_on_replay():
    from rawlsing_next.tests.n10e_empirical_slice_fixture import at07_rows, changed_source_rows, CHANGED_SOURCE_VARIANT
    for rows, variant, expected in ((at07_rows(), None, {"no": 6, "yes": 54}), (changed_source_rows(), CHANGED_SOURCE_VARIANT, {"no": 16, "yes": 54})):
        independent = {answer: sum(row["responses"]["POSITION"] == "P1" and row["responses"]["ANSWER"] == answer for row in rows) for answer in ("no", "yes")}
        assert independent == expected
        case = build_provider_case("forward", variant=variant)
        request = _request(case, request_id="r61-r7-source-law-" + str(variant))
        resolver = _resolver()
        resolver.bind(_binding(request, case))
        result = resolver.resolve(request)
        values = _reader(request, result).read()
        assert values["denominator"] == sum(independent.values())
        assert {cell["cell"]: cell["raw_numerator_support"] for cell in values["cells"]} == independent
        calls = []
        def forbidden_live_call(**kwargs):
            calls.append("called")
            raise AssertionError("cache replay must never execute a producer")
        verifier_only = EvidenceResolver(admission_verifier=_R4_VERIFIER, admitted_producer=forbidden_live_call)
        verifier_only.import_authenticated_cache(resolver.export_cache())
        assert _reader(request, verifier_only.resolve(request)).read()["denominator"] == sum(independent.values())
        verifier_only.export_cache()
        assert calls == []
