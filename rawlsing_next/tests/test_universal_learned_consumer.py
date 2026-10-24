"""R91 R05 actual learned-product -> unchanged N10E consumer integration."""
from __future__ import annotations

from dataclasses import replace

import pytest

import rawlsing_next.pre553_learned_empirical_adjudication as m1
import rawlsing_next.pre553_learned_world_composition as i4
from rawlsing_next.pre553_analytical_composition import compose_positioned_subject_possibility
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_learned_product_lifecycle import LearnedProductLifecycleExecutor
from rawlsing_next.pre553_learned_product_release import M2Repository
from rawlsing_next.pre553_source_backed_c11_facade import build_source_backed_c11_repository
from rawlsing_next.pre553_universal_empirical_extension import (
    EXT_ROUTE_DIRECT_VIA_ACCEPTED_PROVIDER,
    provide_empirical_possibility_slice_ext,
)
from rawlsing_next.tests import c1_at08_at13_fixture as fx
from rawlsing_next.tests.test_pre553_empirical_query import _query
from rawlsing_next.tests.test_pre553_learned_empirical_adjudication import (
    _binding,
    _bundle,
    _m1_authority,
    _registry,
    _validator,
)
from rawlsing_next.tests.test_pre553_learned_world_composition import _contract
from rawlsing_next.tests.test_pre553_route_b_production import _execute, _fixture


def _build_case(*, valid_empty: bool = False):
    m01 = _fixture(valid_empty=valid_empty)
    m01_result = _execute(m01)
    validator_auth = _m1_authority("r91-r05" + ("-empty" if valid_empty else ""))
    _, _, bundle = _bundle(
        valid_empty=valid_empty,
        validator_authorities=(validator_auth,),
    )
    binding = _binding(validator_auth)
    disposition = m1.adjudicate_learned_empirical(
        bundle,
        binding,
        validator_registry=_registry(binding, _validator(outcome="RULE_SATISFIED")),
    )
    contract = _contract(
        route="M1_M2_B5",
        binding=binding,
        tag="r91-r05" + ("-empty" if valid_empty else ""),
    )
    learned = i4.compose_learned_world(
        contract,
        m2_repository=M2Repository(),
        lifecycle_executor=LearnedProductLifecycleExecutor(),
        m1_disposition=disposition,
    )
    repository, release = build_source_backed_c11_repository(
        m01["stream"], m01["projection"]
    )
    universe = m01["projection"].universes[0]
    source_auth = m01["projection"].authority_snapshots[0]
    source = {
        "repo": repository,
        "release_ref": release.release_ref,
        "universe": universe,
        "qrefs": m01["qrefs"],
        "risk_refs": {"R": m01["risk"]},
        "source_auth": source_auth,
        "authorities": tuple(m01["projection"].authority_snapshots),
    }
    registry = AuthorityRegistry((*source["authorities"], m01["qauth"]))
    predicate = m01_result.object_graph.executed_predicates[1]
    producer_query = _query(
        source, m01["qauth"], predicate, ("Y",), tag="r91-r05-c1"
    )
    pairing = fx.make_pairing_authority("r91-r05")
    conditioner = fx.make_conditioner_binding(
        binding_id="x",
        subject_fact_ref=ExactRef(**fx.subject_fact_ref(source, "X", 1)),
        empirical_coordinate_ref=source["qrefs"]["X"],
        comparability_authority_ref=pairing,
        source_universe_ref=universe.ref,
        release_ref=release.release_ref,
    )
    consumer_query = fx.make_multi_conditioner_consumer_query(
        query_id="r91-r05-consumer",
        subject_ref=ExactRef(
            "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
            "urn:test:r91-r05:subject",
            semantic_hash({"fixture": "R91_R05"}),
        ),
        target_ref=source["qrefs"]["Y"],
        source_universe_ref=universe.ref,
        release_ref=release.release_ref,
        bindings=[conditioner],
        projection_kind="R91_R05_LEARNED_CONSUMER",
    )
    witness = fx.build_witness_for_binding(
        witness_object_id="urn:test:r91-r05:witness",
        consumer_query=consumer_query,
        producer_query=producer_query,
        producer_predicate=predicate,
        bindings=[conditioner],
        coordinate_value_pairs=[(source["qrefs"]["X"], 1)],
        pairing_authority=pairing,
        source_universe_ref=universe.ref,
        release_ref=release.release_ref,
    )
    model_rule = fx.make_model_rule(universe.ref, "r91-r05")
    composition = compose_positioned_subject_possibility(
        repository=repository,
        empirical_query=producer_query,
        predicate=predicate,
        authority_registry=registry,
        release_refs=(release.release_ref,),
        consumer_query=consumer_query,
        model_rule=model_rule,
        condition_binding_witness=witness,
    )
    return {
        "m01": m01,
        "m01_result": m01_result,
        "bundle": bundle,
        "disposition": disposition,
        "learned": learned,
        "repository": repository,
        "release": release.release_ref,
        "consumer_query": consumer_query,
        "model_rule": model_rule,
        "producer_query": producer_query,
        "predicate": predicate,
        "witness": witness,
        "registry": registry,
        "composition": composition,
        "context": {
            "repository": repository,
            "empirical_query": producer_query,
            "predicate": predicate,
            "authority_registry": registry,
            "release_refs": (release.release_ref,),
            "consumer_query": consumer_query,
            "model_rule": model_rule,
            "condition_binding_witness": witness,
        },
    }


@pytest.fixture(scope="module")
def r05_case():
    case = _build_case()
    assert case["learned"].receipt.terminal_state == "RULE_SATISFIED"
    assert case["learned"].m1_disposition is not None
    assert case["learned"].m2_artifacts is not None
    assert case["composition"].analytical_state == "SUPPORTED"
    return case


def test_actual_learned_product_reaches_unchanged_consumer(r05_case):
    case = r05_case
    result = i4.evaluate_learned_world_consumer(
        case["learned"],
        composition=case["composition"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        producer_query_ref=case["producer_query"].ref,
        producer_predicate_ref=case["predicate"].ref,
    )
    assert result.state == "LEARNED_CONSUMER_EXACT_SUPPORTED"
    assert result.consumer_result.result_state == "EXACT_SUPPORTED"
    assert result.consumer_values_read["consumer_result_hash"] == (
        result.consumer_result.result_hash
    )
    assert result.consumer_values_read["consumer_values_read"] == (
        result.consumer_result.material()
    )
    assert result.m1_disposition_ref == case["disposition"].ref
    assert result.m2_release_ref == case["learned"].m2_artifacts.release.ref
    assert result.evidence_ref == case["composition"].possibility_slice_evidence_or_null.evidence_ref
    assert result.producer_predicate_ref == case["predicate"].ref


def test_severed_learned_product_or_empirical_determinant_refuses_and_restores(r05_case):
    case = r05_case
    empty_auth = _m1_authority("r91-r05-empty-only")
    _, _, empty_bundle = _bundle(validator_authorities=(empty_auth,))
    empty_binding = _binding(empty_auth)
    empty_disposition = m1.adjudicate_learned_empirical(
        empty_bundle,
        empty_binding,
        validator_registry=_registry(
            empty_binding, _validator(outcome="BLOCKED")
        ),
    )
    empty_learned = i4.compose_learned_world(
        _contract(route="M1_M2_B5", binding=empty_binding, tag="r91-r05-empty-only"),
        m2_repository=M2Repository(),
        lifecycle_executor=LearnedProductLifecycleExecutor(),
        m1_disposition=empty_disposition,
    )
    refused = i4.evaluate_learned_world_consumer(
        empty_learned,
        composition=case["composition"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        producer_query_ref=case["producer_query"].ref,
        producer_predicate_ref=case["predicate"].ref,
    )
    assert refused.state == "REFUSED"
    assert refused.reason_code == "LEARNED_PRODUCT_NOT_PRODUCTIVE"

    wrong_predicate = i4.evaluate_learned_world_consumer(
        case["learned"],
        composition=case["composition"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        producer_query_ref=case["producer_query"].ref,
        producer_predicate_ref=case["m01"]["all_p"].ref,
    )
    assert wrong_predicate.state == "REFUSED"
    assert wrong_predicate.reason_code == "EMPIRICAL_COMPOSITION_DETERMINANT_MISMATCH"

    wrong_query = i4.evaluate_learned_world_consumer(
        case["learned"],
        composition=case["composition"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        producer_query_ref=case["m01"]["raw_query"].ref,
        producer_predicate_ref=case["predicate"].ref,
    )
    assert wrong_query.state == "REFUSED"
    assert wrong_query.reason_code == "EMPIRICAL_COMPOSITION_DETERMINANT_MISMATCH"

    restored = i4.evaluate_learned_world_consumer(
        case["learned"],
        composition=case["composition"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        producer_query_ref=case["producer_query"].ref,
        producer_predicate_ref=case["predicate"].ref,
    )
    assert restored.state == "LEARNED_CONSUMER_EXACT_SUPPORTED"
    original = i4.evaluate_learned_world_consumer(
        case["learned"],
        composition=case["composition"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        producer_query_ref=case["producer_query"].ref,
        producer_predicate_ref=case["predicate"].ref,
    )
    assert restored.consumer_result.result_hash == original.consumer_result.result_hash


def test_e41_extension_direct_route_uses_actual_native_composition(r05_case):
    extension = provide_empirical_possibility_slice_ext(**r05_case["context"])
    assert extension.provider_state == "EXACT_SUPPORTED_SLICE_PRODUCED"
    assert extension.producer_route == EXT_ROUTE_DIRECT_VIA_ACCEPTED_PROVIDER
    assert extension.generated_evidence_or_null is not None
    assert extension.consumer_result_or_null.result_state == "EXACT_SUPPORTED"
    assert extension.consumer_result_or_null.result_hash == (
        r05_case["composition"].consumer_result_or_null.result_hash
    )


def test_learned_current_selection_requirement_is_explicit(r05_case):
    case = r05_case
    refused = i4.evaluate_learned_world_consumer(
        case["learned"],
        composition=case["composition"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        producer_query_ref=case["producer_query"].ref,
        producer_predicate_ref=case["predicate"].ref,
        require_current_selection=True,
    )
    assert refused.state == "REFUSED"
    assert refused.reason_code == "LEARNED_CURRENT_SELECTION_ABSENT"
