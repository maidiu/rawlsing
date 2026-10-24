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
from rawlsing_next.tests import test_pre553_analytical_composition_higher_order as ho
from rawlsing_next.tests.test_pre553_learned_empirical_adjudication import (
    CLAIM_FAMILY,
    CLAIM_RULE,
)
from rawlsing_next.pre553_recursive_handoff import (
    execute_exact_bounded_discovery_with_handoffs,
)


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
    producer_query_b = _query(
        source, m01["qauth"], predicate, ("Y",), tag="r91-r05-c1-b"
    )
    witness_b = fx.build_witness_for_binding(
        witness_object_id="urn:test:r91-r05:witness-b",
        consumer_query=consumer_query,
        producer_query=producer_query_b,
        producer_predicate=predicate,
        bindings=[conditioner],
        coordinate_value_pairs=[(source["qrefs"]["X"], 1)],
        pairing_authority=pairing,
        source_universe_ref=universe.ref,
        release_ref=release.release_ref,
    )
    composition_b = compose_positioned_subject_possibility(
        repository=repository,
        empirical_query=producer_query_b,
        predicate=predicate,
        authority_registry=registry,
        release_refs=(release.release_ref,),
        consumer_query=consumer_query,
        model_rule=model_rule,
        condition_binding_witness=witness_b,
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
        "composition_b": composition_b,
        "producer_query_b": producer_query_b,
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


def test_typed_status_axes_and_z16_survive_consumer(r05_case):
    case = r05_case
    expectations = (
        ("ZERO_SUPPORT", 0, "ZERO_SUPPORT", False),
        ("VALID_EMPTY", 0, "VALID_EMPTY", False),
        ("UNRESOLVED", 16, "UNKNOWN", True),
    )
    for raw_state, denominator, result_state, z_unresolved in expectations:
        mutated = replace(
            case["composition"],
            analytical_state=raw_state,
            producer_fact_state=raw_state,
            possibility_slice_evidence_or_null=None,
            raw_denominator_support=denominator,
        )
        result = i4.evaluate_learned_world_consumer(
            case["learned"],
            composition=mutated,
            consumer_query=case["consumer_query"],
            model_rule=case["model_rule"],
            producer_query_ref=case["producer_query"].ref,
            producer_predicate_ref=case["predicate"].ref,
        )
        assert result.state != "REFUSED"
        assert result.result_state == result_state
        assert result.denominator == denominator
        assert result.z_unresolved is z_unresolved
        assert result.consumer_values_read["result_state"] == result_state
        assert result.consumer_values_read["denominator"] == denominator


def test_product_graph_and_e41_extension_reach_same_consumer(r05_case):
    case = r05_case
    extension = provide_empirical_possibility_slice_ext(**case["context"])
    graph = i4.NativeProductGraph(
        compositions=(case["composition"],),
        extension_result=extension,
    )
    result = i4.evaluate_learned_world_consumer(
        case["learned"],
        composition=case["composition"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        producer_query_ref=case["producer_query"].ref,
        producer_predicate_ref=case["predicate"].ref,
        product_graph=graph,
    )
    assert result.state == "LEARNED_CONSUMER_EXACT_SUPPORTED"
    values = result.consumer_values_read
    assert values["joint_component_count"] >= 1
    assert "discovery_receipt_refs" in values
    assert "recursive_handoff_refs" in values
    assert "producer_route" in values
    assert values["extension_route"] == extension.producer_route
    assert result.consumer_result.result_hash == (
        case["composition"].consumer_result_or_null.result_hash
    )

    bad_graph = i4.NativeProductGraph(
        compositions=(case["composition"],),
        extension_result=object(),
    )
    refused = i4.evaluate_learned_world_consumer(
        case["learned"],
        composition=case["composition"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        producer_query_ref=case["producer_query"].ref,
        producer_predicate_ref=case["predicate"].ref,
        product_graph=bad_graph,
    )
    assert refused.state == "REFUSED"
    assert refused.reason_code == "E41_EXTENSION_GRAPH_MISMATCH"


def test_actual_multi_component_graph_reaches_same_consumer(r05_case):
    case = r05_case
    graph = i4.NativeProductGraph(
        compositions=(case["composition"], case["composition_b"])
    )
    result = i4.evaluate_learned_world_consumer(
        case["learned"],
        composition=case["composition"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        producer_query_ref=case["producer_query"].ref,
        producer_predicate_ref=case["predicate"].ref,
        product_graph=graph,
    )
    assert result.state == "LEARNED_CONSUMER_EXACT_SUPPORTED"
    assert result.joint_component_count == 2
    assert result.consumer_values_read["component_count"] == 2
    assert len(result.consumer_values_read["component_consumer_result_hashes"]) == 2
    assert result.consumer_result.result_hash == (
        case["composition"].consumer_result_or_null.result_hash
    )

    duplicate = i4.NativeProductGraph(
        compositions=(case["composition"], case["composition"])
    )
    refused = i4.evaluate_learned_world_consumer(
        case["learned"],
        composition=case["composition"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        producer_query_ref=case["producer_query"].ref,
        producer_predicate_ref=case["predicate"].ref,
        product_graph=duplicate,
    )
    assert refused.state != "LEARNED_CONSUMER_EXACT_SUPPORTED"
    assert refused.reason_code == "DUPLICATE_GRAPH_COMPONENT"


def test_trusted_coordinator_retains_original_and_validates_submitted_view(r05_case):
    case = r05_case
    slots = (
        i4.NativeGraphSlot(
            "slot-a",
            case["composition"].source_universe_refs[0],
            case["release"],
            case["composition"].producer_query_ref,
            case["composition"].producer_predicate_ref,
            case["composition"].consumer_query_ref,
            case["composition"].consumer_model_rule_hash,
            case["composition"].producer_route,
        ),
        i4.NativeGraphSlot(
            "slot-b",
            case["composition_b"].source_universe_refs[0],
            case["release"],
            case["composition_b"].producer_query_ref,
            case["composition_b"].producer_predicate_ref,
            case["composition_b"].consumer_query_ref,
            case["composition_b"].consumer_model_rule_hash,
            case["composition_b"].producer_route,
        ),
    )
    request = i4.NativeGraphExecutionRequest(slots)
    coordinator = i4.TrustedNativeGraphCoordinator(
        {
            "slot-a": lambda slot: case["composition"],
            "slot-b": lambda slot: case["composition_b"],
        }
    )
    bound = coordinator.execute(request)
    result = i4.evaluate_learned_world_consumer(
        case["learned"],
        composition=case["composition"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        producer_query_ref=case["producer_query"].ref,
        producer_predicate_ref=case["predicate"].ref,
        product_graph=bound,
        trusted_graph_reader=coordinator,
    )
    assert result.state == "LEARNED_CONSUMER_EXACT_SUPPORTED"
    assert result.joint_component_count == 2

    forged_view = i4.BoundNativeProductGraph(
        original_ref=bound.original_ref,
        view=i4.NativeProductGraph((case["composition"], case["composition"])),
        projection_hash=bound.projection_hash,
    )
    refused = i4.evaluate_learned_world_consumer(
        case["learned"],
        composition=case["composition"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        producer_query_ref=case["producer_query"].ref,
        producer_predicate_ref=case["predicate"].ref,
        product_graph=forged_view,
        trusted_graph_reader=coordinator,
    )
    assert refused.state == "REFUSED"
    assert refused.reason_code == "GRAPH_VIEW_DOES_NOT_MATCH_RETAINED_ORIGINAL"


def _learned_from_discovery(
    source, qauth, dauth, authority, discovery, *, tag: str
):
    validator_auth = _m1_authority(f"r91-r05-{tag}")
    bundle = m1.build_m1_adjudication_input_bundle(
        requested_claim_family_id=CLAIM_FAMILY,
        requested_claim_rule_id=CLAIM_RULE,
        selected_discovery_receipts=discovery.receipts,
        discovery_authority_catalog=(authority,),
        empirical_fact_catalog=discovery.empirical_facts,
        empirical_query_catalog=discovery.executed_queries,
        empirical_predicate_catalog=discovery.executed_predicates,
        authority_snapshots=tuple(source["authorities"]) + (qauth, dauth, validator_auth),
        requested_scope={"fixture": tag},
        prerequisite_channels=(),
        additional_dependency_refs=(source["release_ref"],),
    )
    binding = _binding(validator_auth)
    disposition = m1.adjudicate_learned_empirical(
        bundle,
        binding,
        validator_registry=_registry(binding, _validator(outcome="RULE_SATISFIED")),
    )
    learned = i4.compose_learned_world(
        _contract(route="M1_M2_B5", binding=binding, tag=tag),
        m2_repository=M2Repository(),
        lifecycle_executor=LearnedProductLifecycleExecutor(),
        m1_disposition=disposition,
    )
    return learned, disposition


def test_actual_discovery_route_learned_and_consumer():
    source = ho._at10_source()
    qauth = ho._query_authority("r91-r05-at10")
    dauth = ho._d_auth("r91-r05-at10-discovery")
    registry = ho._registry(source, qauth, dauth)
    all_p = ho._branch_predicate(source, qauth, tag="r91-r05-at10-all")
    x1 = ho._predicate(
        source, qauth, ho._response_leaf(source, qauth, "X", 1), tag="r91-r05-at10-x1"
    )
    yq = ho._query(source, qauth, all_p, ("Y",), tag="r91-r05-at10-y")
    grammar = ho._grammar(
        operation="I03-OP-r91-r05-at10-discovery",
        atoms=[ho._atom("ALL", all_p, "BRANCH"), ho._atom("X1", x1, "RESPONSE")],
        templates=[ho._qt("Y", yq)],
        rules=[
            ho._rule(
                "pair",
                "PAIR_RESPONSE_COTRAVEL",
                "SINGLE_ATOM",
                atom_ids=("X1",),
                baseline_atom_id="ALL",
                query_template_id="Y",
                validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
            )
        ],
    )
    authority = ho._discovery_authority(
        source, grammar, dauth, tag="r91-r05-at10"
    )
    discovery = ho._execute_discovery(
        source,
        qauth,
        dauth,
        grammar,
        (all_p, x1),
        (yq,),
        authority=authority,
    )
    receipt = discovery.receipts[0]
    pred_by_ref = {p.ref: p for p in discovery.executed_predicates}
    query_by_ref = {q.ref: q for q in discovery.executed_queries}
    fact_by_ref = {f.ref: f for f in discovery.empirical_facts}
    produced_predicate = pred_by_ref[ExactRef(**receipt.winning_predicate_ref)]
    produced_fact = fact_by_ref[ExactRef(**receipt.empirical_fact_refs[0])]
    produced_query = query_by_ref[ExactRef(**produced_fact.empirical_query_spec_ref)]
    pairing = fx.make_pairing_authority("r91-r05-at10")
    conditioner = fx.make_conditioner_binding(
        binding_id="x",
        subject_fact_ref=ExactRef(**ho._subject_fact_ref(source, "X", 1)),
        empirical_coordinate_ref=source["qrefs"]["X"],
        comparability_authority_ref=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    consumer_query = fx.make_multi_conditioner_consumer_query(
        query_id="r91-r05-at10-consumer",
        subject_ref=ExactRef(
            "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
            "urn:test:r91-r05:at10:subject",
            semantic_hash({"fixture": "R91_R05_AT10"}),
        ),
        target_ref=source["qrefs"]["Y"],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=[conditioner],
        projection_kind="R91_R05_AT10_DISCOVERY",
    )
    witness = fx.build_witness_for_binding(
        witness_object_id="urn:test:r91-r05:at10:witness",
        consumer_query=consumer_query,
        producer_query=produced_query,
        producer_predicate=produced_predicate,
        bindings=[conditioner],
        coordinate_value_pairs=[(source["qrefs"]["X"], 1)],
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    composition = compose_positioned_subject_possibility(
        repository=source["repo"],
        empirical_query=produced_query,
        predicate=produced_predicate,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
        consumer_query=consumer_query,
        model_rule=fx.make_model_rule(source["universe"].ref, "r91-r05-at10"),
        condition_binding_witness=witness,
        discovery_result=discovery,
        discovery_receipt_ref=receipt.ref,
    )
    assert composition.producer_route == "I05_EXACT_BOUNDED_TO_POSITIONED_SUBJECT"
    learned, disposition = _learned_from_discovery(
        source, qauth, dauth, authority, discovery, tag="r91-r05-at10"
    )
    result = i4.evaluate_learned_world_consumer(
        learned,
        composition=composition,
        consumer_query=consumer_query,
        model_rule=fx.make_model_rule(source["universe"].ref, "r91-r05-at10"),
        producer_query_ref=produced_query.ref,
        producer_predicate_ref=produced_predicate.ref,
    )
    assert result.state == "LEARNED_CONSUMER_EXACT_SUPPORTED"
    assert result.producer_route == "I05_EXACT_BOUNDED_TO_POSITIONED_SUBJECT"
    assert result.discovery_receipt_refs == (receipt.ref,)
    assert result.discovery_frontier_ref == discovery.evaluated_frontier_ref
    assert result.consumer_result.result_state == "EXACT_SUPPORTED"

    joint_query = ho._query(
        source, qauth, produced_predicate, ("X", "Y"), tag="r91-r05-at10-joint"
    )
    joint_pairing = fx.make_pairing_authority("r91-r05-at10-joint")
    joint_conditioner = fx.make_conditioner_binding(
        binding_id="x",
        subject_fact_ref=ExactRef(**ho._subject_fact_ref(source, "X", 1)),
        empirical_coordinate_ref=source["qrefs"]["X"],
        comparability_authority_ref=joint_pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    joint_consumer = fx.make_multi_conditioner_consumer_query(
        query_id="r91-r05-at10-joint-consumer",
        subject_ref=ExactRef(
            "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
            "urn:test:r91-r05:at10:joint-subject",
            semantic_hash({"fixture": "R91_R05_AT10_JOINT"}),
        ),
        target_ref=source["qrefs"]["X"],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=[joint_conditioner],
        projection_kind="R91_R05_AT10_JOINT",
    )
    joint_witness = fx.build_witness_for_binding(
        witness_object_id="urn:test:r91-r05:at10:joint-witness",
        consumer_query=joint_consumer,
        producer_query=joint_query,
        producer_predicate=produced_predicate,
        bindings=[joint_conditioner],
        coordinate_value_pairs=[(source["qrefs"]["X"], 1)],
        pairing_authority=joint_pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    joint_model = fx.make_model_rule(source["universe"].ref, "r91-r05-at10-joint")
    joint_composition = compose_positioned_subject_possibility(
        repository=source["repo"],
        empirical_query=joint_query,
        predicate=produced_predicate,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
        consumer_query=joint_consumer,
        model_rule=joint_model,
        condition_binding_witness=joint_witness,
    )
    assert joint_composition.joint_component_count == 2
    joint_result = i4.evaluate_learned_world_consumer(
        learned,
        composition=joint_composition,
        consumer_query=joint_consumer,
        model_rule=joint_model,
        producer_query_ref=joint_query.ref,
        producer_predicate_ref=produced_predicate.ref,
    )
    assert joint_result.state == "LEARNED_CONSUMER_EXACT_SUPPORTED"
    assert joint_result.joint_component_count == 2
    assert joint_result.consumer_result.result_state == "EXACT_SUPPORTED"


def test_actual_recursive_route_learned_and_consumer():
    source = ho._at11_source()
    qauth = ho._query_authority("r91-r05-at11")
    dauth = ho._d_auth("r91-r05-at11-discovery")
    registry = ho._registry(source, qauth, dauth)
    parent = ho._branch_predicate(
        source,
        qauth,
        members=tuple(source["respondents"][rid] for rid in ("R1", "R2", "R3", "R4", "R5", "R6")),
        tag="r91-r05-at11-parent",
    )
    x1 = ho._predicate(
        source, qauth, ho._response_leaf(source, qauth, "X", 1), tag="r91-r05-at11-x1"
    )
    x_query = ho._query(source, qauth, parent, ("X",), tag="r91-r05-at11-g1-x")
    grammar = ho._grammar(
        operation="I03-OP-r91-r05-at11-discovery",
        atoms=[ho._atom("PARENT", parent, "BRANCH"), ho._atom("X1", x1, "RESPONSE")],
        templates=[ho._qt("X", x_query)],
        rules=[
            ho._rule(
                "child",
                "RECURSIVE_SUBGROUP_FORK",
                "SINGLE_ATOM",
                atom_ids=("X1",),
                baseline_atom_id="PARENT",
                query_template_id="X",
                validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
            )
        ],
        k=2,
    )
    authority = ho._discovery_authority(
        source, grammar, dauth, tag="r91-r05-at11-g1"
    )
    g1 = execute_exact_bounded_discovery_with_handoffs(
        repository=source["repo"],
        discovery_authority=authority,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
        predicate_catalog=(parent, x1),
        query_template_catalog=(x_query,),
    )
    handoff = g1.handoffs[0]
    child_predicate = handoff.winning_predicate
    child_query = ho._query(
        source, qauth, child_predicate, ("Y",), tag="r91-r05-at11-child-to-y"
    )
    pairing = fx.make_pairing_authority("r91-r05-at11")
    conditioner = fx.make_conditioner_binding(
        binding_id="x",
        subject_fact_ref=ExactRef(**ho._subject_fact_ref(source, "X", 1)),
        empirical_coordinate_ref=source["qrefs"]["X"],
        comparability_authority_ref=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    consumer_query = fx.make_multi_conditioner_consumer_query(
        query_id="r91-r05-at11-consumer",
        subject_ref=ExactRef(
            "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
            "urn:test:r91-r05:at11:subject",
            semantic_hash({"fixture": "R91_R05_AT11"}),
        ),
        target_ref=source["qrefs"]["Y"],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=[conditioner],
        projection_kind="R91_R05_AT11_RECURSIVE",
    )
    witness = fx.build_witness_for_binding(
        witness_object_id="urn:test:r91-r05:at11:witness",
        consumer_query=consumer_query,
        producer_query=child_query,
        producer_predicate=child_predicate,
        bindings=[conditioner],
        coordinate_value_pairs=[(source["qrefs"]["X"], 1)],
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    composition = compose_positioned_subject_possibility(
        repository=source["repo"],
        empirical_query=child_query,
        predicate=child_predicate,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
        consumer_query=consumer_query,
        model_rule=fx.make_model_rule(source["universe"].ref, "r91-r05-at11"),
        condition_binding_witness=witness,
        recursive_handoff=handoff,
    )
    assert composition.producer_route == "MX01R2_RECURSIVE_TO_POSITIONED_SUBJECT"
    learned, disposition = _learned_from_discovery(
        source, qauth, dauth, authority, g1.discovery_result, tag="r91-r05-at11"
    )
    result = i4.evaluate_learned_world_consumer(
        learned,
        composition=composition,
        consumer_query=consumer_query,
        model_rule=fx.make_model_rule(source["universe"].ref, "r91-r05-at11"),
        producer_query_ref=child_query.ref,
        producer_predicate_ref=child_predicate.ref,
    )
    assert result.state == "LEARNED_CONSUMER_EXACT_SUPPORTED"
    assert result.producer_route == "MX01R2_RECURSIVE_TO_POSITIONED_SUBJECT"
    assert result.recursive_handoff_refs == (handoff.ref,)
    assert handoff.immediate_parent_branch_ref in result.recursive_lineage_refs
    assert result.consumer_result.result_state == "EXACT_SUPPORTED"
