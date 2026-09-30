"""C1-02 higher-order / joint / recursive analytical composition courts (AT08-AT13)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from rawlsing_next.pre553_analytical_composition import (
    AnalyticalCompositionError,
    ConditionValueRelationMismatch,
    DiscoveryConsumptionMismatch,
    JointTargetMismatch,
    RecursiveLineageMismatch,
    _validate_joint_grain,
    compose_positioned_subject_possibility,
)
from rawlsing_next.pre553_empirical_objects import EmpiricalQuerySpec, ExactRef, semantic_hash
from rawlsing_next.pre553_recursive_handoff import execute_exact_bounded_discovery_with_handoffs
from rawlsing_next.tests import c1_at08_at13_fixture as fx
from rawlsing_next.tests.test_pre553_discovery_exact import (
    _atom,
    _d_auth,
    _discovery_authority,
    _execute as _execute_discovery,
    _grammar,
    _qt,
    _rule,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _auth,
    _branch_predicate,
    _build_source,
    _coordinate_leaf,
    _predicate,
    _query,
    _query_authority,
    _registry,
    _response_leaf,
    _run,
)


# ---------------------------------------------------------------------------
# AT08: direct multi-conditioner composition (consumer query with >1 binding)
# ---------------------------------------------------------------------------


def _at08_source():
    rows = [
        {"id": f"R{x}{y}", "responses": {"X": x, "Y": y, "Z": int(x == 1 and y == 1)}}
        for x in (0, 1) for y in (0, 1)
    ]
    return _build_source("c1-at08", rows)


def test_at08_direct_two_conditioner_composition_requires_joint_predicate():
    source = _at08_source()
    qauth = _query_authority("c1-at08")
    pairing = fx.make_pairing_authority("at08")
    registry = _registry(source, qauth)

    all_p = _branch_predicate(source, qauth, tag="c1-at08-all")
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="c1-at08-x1")
    y1 = _predicate(source, qauth, _response_leaf(source, qauth, "Y", 1), tag="c1-at08-y1")

    # Joint predicate: X=1 AND Y=1
    joint_predicate = _predicate(
        source,
        qauth,
        {"op": "AND", "children": [x1.predicate_ast, y1.predicate_ast]},
        tag="c1-at08-x1-and-y1",
    )

    producer_query = _query(
        source,
        qauth,
        joint_predicate,
        ("Z",),
        tag="c1-at08-x1y1-to-z",
    )

    subject_ref = ExactRef(
        "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
        "urn:test:c1-02:at08:subject",
        semantic_hash({"fixture_id": "AT08"}),
    )

    bx = fx.make_conditioner_binding(
        binding_id="x",
        subject_fact_ref=ExactRef(**_subject_fact_ref(source, "X", 1)),
        empirical_coordinate_ref=source["qrefs"]["X"],
        comparability_authority_ref=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    by = fx.make_conditioner_binding(
        binding_id="y",
        subject_fact_ref=ExactRef(**_subject_fact_ref(source, "Y", 1)),
        empirical_coordinate_ref=source["qrefs"]["Y"],
        comparability_authority_ref=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )

    consumer_query = fx.make_multi_conditioner_consumer_query(
        query_id="c1-at08-consumer",
        subject_ref=subject_ref,
        target_ref=source["qrefs"]["Z"],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=[bx, by],
        projection_kind="C1_AT08_MULTI_CONDITIONER_CONDITIONAL_DISTRIBUTION",
    )

    witness = fx.build_witness_for_binding(
        witness_object_id="urn:test:c1-02:at08:witness",
        consumer_query=consumer_query,
        producer_query=producer_query,
        producer_predicate=joint_predicate,
        bindings=[bx, by],
        coordinate_value_pairs=[(source["qrefs"]["X"], 1), (source["qrefs"]["Y"], 1)],
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )

    result = compose_positioned_subject_possibility(
        repository=source["repo"],
        empirical_query=producer_query,
        predicate=joint_predicate,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
        consumer_query=consumer_query,
        model_rule=fx.make_model_rule(source["universe"].ref, "at08"),
        condition_binding_witness=witness,
    )

    assert result.producer_route == "DIRECT_I03_TO_POSITIONED_SUBJECT"
    assert result.analytical_state == "SUPPORTED"
    assert result.raw_denominator_support == 1
    assert result.joint_component_count == 1
    cells = {cell["cell"]: cell["raw_numerator_support"] for cell in result.complete_cell_geometry}
    assert cells["1"] == 1
    assert result.consumer_result_or_null.result_state == "EXACT_SUPPORTED"


def _subject_fact_ref(source, question, value):
    material = {
        "schema": "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
        "empirical_semantic_ref": source["qrefs"][question].as_dict(),
        "exact_value": str(value),
    }
    ref = ExactRef(
        "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
        f"urn:test:c1-02:subject-fact:{question}:{value}",
        semantic_hash(material),
    )
    return ref.as_dict()


# ---------------------------------------------------------------------------
# AT09: joint-target consumer query matches joint producer topology
# ---------------------------------------------------------------------------


def _at09_source():
    rows = [
        {"id": f"R{a}{b}", "responses": {"A": a, "B": b, "C": a ^ b}}
        for a in (0, 1) for b in (0, 1)
    ]
    return _build_source("c1-at09", rows)


def test_at09_joint_target_geometry_preserved_in_evidence():
    source = _at09_source()
    qauth = _query_authority("c1-at09")
    pairing = fx.make_pairing_authority("at09")
    registry = _registry(source, qauth)

    all_p = _branch_predicate(source, qauth, tag="c1-at09-all")
    # Conditioner predicate: A=0
    cond = _predicate(source, qauth, _response_leaf(source, qauth, "A", 0), tag="c1-at09-a0")
    # Joint target: (B, C)
    producer_query = _query(source, qauth, cond, ("B", "C"), tag="c1-at09-a0-to-bc")

    subject_ref = ExactRef(
        "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
        "urn:test:c1-02:at09:subject",
        semantic_hash({"fixture_id": "AT09"}),
    )
    binding = fx.make_conditioner_binding(
        binding_id="a",
        subject_fact_ref=ExactRef(**_subject_fact_ref(source, "A", 0)),
        empirical_coordinate_ref=source["qrefs"]["A"],
        comparability_authority_ref=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    consumer_query = fx.make_multi_conditioner_consumer_query(
        query_id="c1-at09-consumer",
        subject_ref=subject_ref,
        target_ref=source["qrefs"]["B"],  # canonical first target
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=[binding],
        projection_kind="C1_AT09_JOINT_TARGET_CONDITIONAL_DISTRIBUTION",
    )

    witness = fx.build_witness_for_binding(
        witness_object_id="urn:test:c1-02:at09:witness",
        consumer_query=consumer_query,
        producer_query=producer_query,
        producer_predicate=cond,
        bindings=[binding],
        coordinate_value_pairs=[(source["qrefs"]["A"], 0)],
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )

    result = compose_positioned_subject_possibility(
        repository=source["repo"],
        empirical_query=producer_query,
        predicate=cond,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
        consumer_query=consumer_query,
        model_rule=fx.make_model_rule(source["universe"].ref, "at09"),
        condition_binding_witness=witness,
    )

    assert result.producer_route == "DIRECT_I03_TO_POSITIONED_SUBJECT"
    assert result.joint_component_count == 2
    assert result.joint_order_semantics == "SEMANTIC_ORDERED"
    assert result.target_arity_and_topology["arity"] == 2
    geometry = result.possibility_slice_evidence_or_null.geometry
    assert geometry["target"]["arity"] == 2
    assert len(geometry["target"]["components"]) == 2


def _target_component(source, question, domain):
    return {
        "target_ref": source["qrefs"][question].as_dict(),
        "topology": "SCALAR_SINGULAR",
        "domain": [str(v) for v in domain],
        "target_domain_replay_ref": _ref(
            "TARGET_DOMAIN", f"{question}-{'-'.join(str(v) for v in domain)}"
        ),
        "topology_authority_refs": [source["source_auth"].authority_ref.as_dict()],
        "response_semantic_authority_refs": [source["source_auth"].authority_ref.as_dict()],
        "included_states": ["SUBSTANTIVE_RESPONSE"],
    }


def _ref(kind, namespace):
    material = {"kind": kind, "namespace": namespace}
    digest = semantic_hash(material)
    return ExactRef(kind, f"urn:test:c1-02:target-domain:{namespace}", digest)


def _replay_root(tag):
    material = {"tag": tag}
    digest = semantic_hash(material)
    return ExactRef("REPLAY_ROOT", f"urn:test:c1-02:replay-root:{tag}", digest)


def _measure_basis_ref(source):
    material = {"source": source["universe"].ref.object_id}
    digest = semantic_hash(material)
    return ExactRef("MEASURE_BASIS", f"urn:test:c1-02:measure-basis:{digest}", digest)


# ---------------------------------------------------------------------------
# AT10: discovery-route consumption (I05 exact bounded -> C1 composition)
# ---------------------------------------------------------------------------


def _at10_source():
    rows = [
        {"id": "R1", "responses": {"X": 1, "Y": 1}},
        {"id": "R2", "responses": {"X": 1, "Y": 1}},
        {"id": "R3", "responses": {"X": 0, "Y": 0}},
        {"id": "R4", "responses": {"X": 0, "Y": 0}},
    ]
    return _build_source("c1-at10", rows)


def test_at10_discovery_route_consumes_supported_receipt():
    source = _at10_source()
    qauth = _query_authority("c1-at10")
    dauth = _d_auth("c1-at10-discovery")
    pairing = fx.make_pairing_authority("at10")
    registry = _registry(source, qauth, dauth)

    all_p = _branch_predicate(source, qauth, tag="c1-at10-all")
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="c1-at10-x1")
    yq = _query(source, qauth, all_p, ("Y",), tag="c1-at10-y")

    grammar = _grammar(
        operation="I03-OP-c1-at10-discovery",
        atoms=[_atom("ALL", all_p, "BRANCH"), _atom("X1", x1, "RESPONSE")],
        templates=[_qt("Y", yq)],
        rules=[_rule(
            "pair", "PAIR_RESPONSE_COTRAVEL", "SINGLE_ATOM",
            atom_ids=("X1",), baseline_atom_id="ALL", query_template_id="Y",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
    )
    discovery = _execute_discovery(
        source, qauth, dauth, grammar, (all_p, x1), (yq,), authority=_discovery_authority(source, grammar, dauth, tag="at10")
    )
    receipt = discovery.receipts[0]
    assert receipt.typed_state == "DISCOVERED_RESULT_SUPPORTED"

    # Build a C1 consumer for the discovered X=1 -> Y relation
    subject_ref = ExactRef(
        "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
        "urn:test:c1-02:at10:subject",
        semantic_hash({"fixture_id": "AT10"}),
    )
    binding = fx.make_conditioner_binding(
        binding_id="x",
        subject_fact_ref=ExactRef(**_subject_fact_ref(source, "X", 1)),
        empirical_coordinate_ref=source["qrefs"]["X"],
        comparability_authority_ref=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    consumer_query = fx.make_multi_conditioner_consumer_query(
        query_id="c1-at10-consumer",
        subject_ref=subject_ref,
        target_ref=source["qrefs"]["Y"],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=[binding],
        projection_kind="C1_AT10_DISCOVERY_ROUTE_CONDITIONAL_DISTRIBUTION",
    )

    # The supplied empirical_query/predicate for discovery route are overridden
    # by the discovery result; derive the exact producer objects from the receipt.
    pred_by_ref = {p.ref: p for p in discovery.executed_predicates}
    query_by_ref = {q.ref: q for q in discovery.executed_queries}
    fact_by_ref = {f.ref: f for f in discovery.empirical_facts}
    produced_predicate = pred_by_ref[ExactRef(**receipt.winning_predicate_ref)]
    produced_fact = fact_by_ref[ExactRef(**receipt.empirical_fact_refs[0])]
    produced_query = query_by_ref[ExactRef(**produced_fact.empirical_query_spec_ref)]

    witness = fx.build_witness_for_binding(
        witness_object_id="urn:test:c1-02:at10:witness",
        consumer_query=consumer_query,
        producer_query=produced_query,
        producer_predicate=produced_predicate,
        bindings=[binding],
        coordinate_value_pairs=[(source["qrefs"]["X"], 1)],
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )

    result = compose_positioned_subject_possibility(
        repository=source["repo"],
        empirical_query=produced_query,
        predicate=produced_predicate,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
        consumer_query=consumer_query,
        model_rule=fx.make_model_rule(source["universe"].ref, "at10"),
        condition_binding_witness=witness,
        discovery_result=discovery,
        discovery_receipt_ref=receipt.ref,
    )

    assert result.producer_route == "I05_EXACT_BOUNDED_TO_POSITIONED_SUBJECT"
    assert result.analytical_state == "SUPPORTED"
    assert result.discovery_receipt_refs == (receipt.ref,)
    assert result.discovery_frontier_ref == discovery.evaluated_frontier_ref
    assert result.consumer_result_or_null.result_state == "EXACT_SUPPORTED"


def test_at10_discovery_route_rejects_wrong_receipt_ref():
    source = _at10_source()
    qauth = _query_authority("c1-at10")
    dauth = _d_auth("c1-at10-discovery")
    pairing = fx.make_pairing_authority("at10")
    registry = _registry(source, qauth, dauth)

    all_p = _branch_predicate(source, qauth, tag="c1-at10-all")
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="c1-at10-x1")
    yq = _query(source, qauth, all_p, ("Y",), tag="c1-at10-y")

    grammar = _grammar(
        operation="I03-OP-c1-at10-discovery",
        atoms=[_atom("ALL", all_p, "BRANCH"), _atom("X1", x1, "RESPONSE")],
        templates=[_qt("Y", yq)],
        rules=[_rule(
            "pair", "PAIR_RESPONSE_COTRAVEL", "SINGLE_ATOM",
            atom_ids=("X1",), baseline_atom_id="ALL", query_template_id="Y",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
    )
    discovery = _execute_discovery(
        source, qauth, dauth, grammar, (all_p, x1), (yq,), authority=_discovery_authority(source, grammar, dauth, tag="at10")
    )
    produced_query = discovery.executed_queries[0]
    produced_predicate = discovery.executed_predicates[0]

    subject_ref = ExactRef(
        "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
        "urn:test:c1-02:at10:subject-wrong",
        semantic_hash({"fixture_id": "AT10-WRONG"}),
    )
    binding = fx.make_conditioner_binding(
        binding_id="x",
        subject_fact_ref=ExactRef(**_subject_fact_ref(source, "X", 1)),
        empirical_coordinate_ref=source["qrefs"]["X"],
        comparability_authority_ref=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    consumer_query = fx.make_multi_conditioner_consumer_query(
        query_id="c1-at10-consumer-wrong",
        subject_ref=subject_ref,
        target_ref=source["qrefs"]["Y"],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=[binding],
        projection_kind="C1_AT10_DISCOVERY_ROUTE_CONDITIONAL_DISTRIBUTION",
    )
    witness = fx.build_witness_for_binding(
        witness_object_id="urn:test:c1-02:at10:witness-wrong",
        consumer_query=consumer_query,
        producer_query=produced_query,
        producer_predicate=produced_predicate,
        bindings=[binding],
        coordinate_value_pairs=[(source["qrefs"]["X"], 1)],
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )

    wrong_receipt_ref = ExactRef(
        "PRE553_I05_DISCOVERY_RESULT_RECEIPT",
        "urn:test:c1-02:at10:wrong-receipt",
        "0" * 64,
    )
    with pytest.raises(DiscoveryConsumptionMismatch, match="receipt not found"):
        compose_positioned_subject_possibility(
            repository=source["repo"],
            empirical_query=produced_query,
            predicate=produced_predicate,
            authority_registry=registry,
            release_refs=(source["release_ref"],),
            consumer_query=consumer_query,
            model_rule=fx.make_model_rule(source["universe"].ref, "at10"),
            condition_binding_witness=witness,
            discovery_result=discovery,
            discovery_receipt_ref=wrong_receipt_ref,
        )


# ---------------------------------------------------------------------------
# AT11: recursive handoff consumption (MX01R2 -> C1 composition)
# ---------------------------------------------------------------------------


def _at11_source():
    rows = [
        {"id": "R1", "responses": {"X": 1, "H": 1, "Y": 1}},
        {"id": "R2", "responses": {"X": 1, "H": 1, "Y": 0}},
        {"id": "R3", "responses": {"X": 1, "H": 0, "Y": 1}},
        {"id": "R4", "responses": {"X": 1, "H": 0, "Y": 0}},
        {"id": "R5", "responses": {"X": 0, "H": 1, "Y": 1}},
        {"id": "R6", "responses": {"X": 0, "H": 0, "Y": 0}},
    ]
    return _build_source("c1-at11", rows)


def test_at11_recursive_handoff_composition_continues_lineage():
    source = _at11_source()
    qauth = _query_authority("c1-at11")
    dauth = _d_auth("c1-at11-discovery")
    pairing = fx.make_pairing_authority("at11")
    registry = _registry(source, qauth, dauth)

    parent = _branch_predicate(
        source,
        qauth,
        members=tuple(source["respondents"][rid] for rid in ("R1", "R2", "R3", "R4", "R5", "R6")),
        tag="c1-at11-parent",
    )
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="c1-at11-x1")
    x_query = _query(source, qauth, parent, ("X",), tag="c1-at11-g1-x")

    grammar = _grammar(
        operation="I03-OP-c1-at11-discovery",
        atoms=[_atom("PARENT", parent, "BRANCH"), _atom("X1", x1, "RESPONSE")],
        templates=[_qt("X", x_query)],
        rules=[_rule(
            "child", "RECURSIVE_SUBGROUP_FORK", "SINGLE_ATOM",
            atom_ids=("X1",), baseline_atom_id="PARENT", query_template_id="X",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
        k=2,
    )
    authority = _discovery_authority(source, grammar, dauth, tag="c1-at11-g1")
    g1 = execute_exact_bounded_discovery_with_handoffs(
        repository=source["repo"],
        discovery_authority=authority,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
        predicate_catalog=(parent, x1),
        query_template_catalog=(x_query,),
    )
    handoff = g1.handoffs[0]
    assert g1.discovery_result.receipts[0].typed_state == "DISCOVERED_RESULT_SUPPORTED"

    # Compose the child handoff into a positioned-subject possibility for Y
    child_predicate = handoff.winning_predicate
    child_query = _query(
        source,
        qauth,
        child_predicate,
        ("Y",),
        tag="c1-at11-child-to-y",
    )

    subject_ref = ExactRef(
        "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
        "urn:test:c1-02:at11:subject",
        semantic_hash({"fixture_id": "AT11"}),
    )
    binding = fx.make_conditioner_binding(
        binding_id="x",
        subject_fact_ref=ExactRef(**_subject_fact_ref(source, "X", 1)),
        empirical_coordinate_ref=source["qrefs"]["X"],
        comparability_authority_ref=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    consumer_query = fx.make_multi_conditioner_consumer_query(
        query_id="c1-at11-consumer",
        subject_ref=subject_ref,
        target_ref=source["qrefs"]["Y"],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=[binding],
        projection_kind="C1_AT11_RECURSIVE_HANDOFF_CONDITIONAL_DISTRIBUTION",
    )
    witness = fx.build_witness_for_binding(
        witness_object_id="urn:test:c1-02:at11:witness",
        consumer_query=consumer_query,
        producer_query=child_query,
        producer_predicate=child_predicate,
        bindings=[binding],
        coordinate_value_pairs=[(source["qrefs"]["X"], 1)],
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )

    result = compose_positioned_subject_possibility(
        repository=source["repo"],
        empirical_query=child_query,
        predicate=child_predicate,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
        consumer_query=consumer_query,
        model_rule=fx.make_model_rule(source["universe"].ref, "at11"),
        condition_binding_witness=witness,
        recursive_handoff=handoff,
    )

    assert result.producer_route == "MX01R2_RECURSIVE_TO_POSITIONED_SUBJECT"
    assert result.analytical_state == "SUPPORTED"
    assert result.recursive_handoff_refs == (handoff.ref,)
    assert handoff.immediate_parent_branch_ref in result.recursive_lineage_refs
    assert result.coverage_state == "RECURSIVE_DEPTH_CONTINUATION"
    assert result.consumer_result_or_null.result_state == "EXACT_SUPPORTED"


def test_at11_recursive_handoff_rejects_predicate_mismatch():
    source = _at11_source()
    qauth = _query_authority("c1-at11")
    dauth = _d_auth("c1-at11-discovery")
    pairing = fx.make_pairing_authority("at11")
    registry = _registry(source, qauth, dauth)

    parent = _branch_predicate(
        source,
        qauth,
        members=tuple(source["respondents"][rid] for rid in ("R1", "R2", "R3", "R4", "R5", "R6")),
        tag="c1-at11-parent",
    )
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="c1-at11-x1")
    x_query = _query(source, qauth, parent, ("X",), tag="c1-at11-g1-x")

    grammar = _grammar(
        operation="I03-OP-c1-at11-discovery",
        atoms=[_atom("PARENT", parent, "BRANCH"), _atom("X1", x1, "RESPONSE")],
        templates=[_qt("X", x_query)],
        rules=[_rule(
            "child", "RECURSIVE_SUBGROUP_FORK", "SINGLE_ATOM",
            atom_ids=("X1",), baseline_atom_id="PARENT", query_template_id="X",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
        k=2,
    )
    authority = _discovery_authority(source, grammar, dauth, tag="c1-at11-g1")
    g1 = execute_exact_bounded_discovery_with_handoffs(
        repository=source["repo"],
        discovery_authority=authority,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
        predicate_catalog=(parent, x1),
        query_template_catalog=(x_query,),
    )
    handoff = g1.handoffs[0]

    # Use a different predicate than the handoff's winning predicate
    wrong_predicate = _predicate(source, qauth, _response_leaf(source, qauth, "X", 0), tag="c1-at11-x0")
    wrong_query = _query(source, qauth, wrong_predicate, ("Y",), tag="c1-at11-wrong-to-y")

    subject_ref = ExactRef(
        "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
        "urn:test:c1-02:at11:subject-mismatch",
        semantic_hash({"fixture_id": "AT11-MISMATCH"}),
    )
    binding = fx.make_conditioner_binding(
        binding_id="x",
        subject_fact_ref=ExactRef(**_subject_fact_ref(source, "X", 1)),
        empirical_coordinate_ref=source["qrefs"]["X"],
        comparability_authority_ref=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    consumer_query = fx.make_multi_conditioner_consumer_query(
        query_id="c1-at11-consumer-mismatch",
        subject_ref=subject_ref,
        target_ref=source["qrefs"]["Y"],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=[binding],
        projection_kind="C1_AT11_RECURSIVE_HANDOFF_CONDITIONAL_DISTRIBUTION",
    )
    witness = fx.build_witness_for_binding(
        witness_object_id="urn:test:c1-02:at11:witness-mismatch",
        consumer_query=consumer_query,
        producer_query=wrong_query,
        producer_predicate=wrong_predicate,
        bindings=[binding],
        coordinate_value_pairs=[(source["qrefs"]["X"], 1)],
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )

    with pytest.raises(RecursiveLineageMismatch, match="handoff winning predicate"):
        compose_positioned_subject_possibility(
            repository=source["repo"],
            empirical_query=wrong_query,
            predicate=wrong_predicate,
            authority_registry=registry,
            release_refs=(source["release_ref"],),
            consumer_query=consumer_query,
            model_rule=fx.make_model_rule(source["universe"].ref, "at11"),
            condition_binding_witness=witness,
            recursive_handoff=handoff,
        )


# ---------------------------------------------------------------------------
# AT12/AT13: fail-closed guards for joint/recursive mismatches
# ---------------------------------------------------------------------------


def test_at12_joint_target_count_mismatch_fails_closed():
    source = _at09_source()
    qauth = _query_authority("c1-at09")
    pairing = fx.make_pairing_authority("at12")

    cond = _predicate(source, qauth, _response_leaf(source, qauth, "A", 0), tag="c1-at12-a0")
    # Producer topology declares two targets (B, C) but consumer query has one binding.
    producer_query = _query(source, qauth, cond, ("B", "C"), tag="c1-at12-a0-to-bc")

    subject_ref = ExactRef(
        "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
        "urn:test:c1-02:at12:subject",
        semantic_hash({"fixture_id": "AT12"}),
    )
    binding = fx.make_conditioner_binding(
        binding_id="a",
        subject_fact_ref=ExactRef(**_subject_fact_ref(source, "A", 0)),
        empirical_coordinate_ref=source["qrefs"]["A"],
        comparability_authority_ref=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    consumer_query = fx.make_multi_conditioner_consumer_query(
        query_id="c1-at12-consumer",
        subject_ref=subject_ref,
        target_ref=source["qrefs"]["B"],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=[binding],
        projection_kind="C1_AT12_JOINT_MISMATCH",
    )

    with pytest.raises(JointTargetMismatch):
        _validate_joint_grain(
            empirical_query=producer_query,
            consumer_query=consumer_query,
            release_refs=(source["release_ref"],),
        )


def test_at13_witness_binding_count_mismatch_fails_closed():
    source = _at08_source()
    qauth = _query_authority("c1-at08")
    pairing = fx.make_pairing_authority("at13")
    registry = _registry(source, qauth)

    all_p = _branch_predicate(source, qauth, tag="c1-at13-all")
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="c1-at13-x1")
    y1 = _predicate(source, qauth, _response_leaf(source, qauth, "Y", 1), tag="c1-at13-y1")
    joint_predicate = _predicate(
        source,
        qauth,
        {"op": "AND", "children": [x1.predicate_ast, y1.predicate_ast]},
        tag="c1-at13-x1-and-y1",
    )
    producer_query = _query(
        source,
        qauth,
        joint_predicate,
        ("Z",),
        tag="c1-at13-x1y1-to-z",
    )

    subject_ref = ExactRef(
        "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
        "urn:test:c1-02:at13:subject",
        semantic_hash({"fixture_id": "AT13"}),
    )
    bx = fx.make_conditioner_binding(
        binding_id="x",
        subject_fact_ref=ExactRef(**_subject_fact_ref(source, "X", 1)),
        empirical_coordinate_ref=source["qrefs"]["X"],
        comparability_authority_ref=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    by = fx.make_conditioner_binding(
        binding_id="y",
        subject_fact_ref=ExactRef(**_subject_fact_ref(source, "Y", 1)),
        empirical_coordinate_ref=source["qrefs"]["Y"],
        comparability_authority_ref=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    consumer_query = fx.make_multi_conditioner_consumer_query(
        query_id="c1-at13-consumer",
        subject_ref=subject_ref,
        target_ref=source["qrefs"]["Z"],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=[bx, by],
        projection_kind="C1_AT13_BINDING_MISMATCH",
    )

    # Witness only contains one binding material but consumer query has two
    bad_witness = fx.build_witness_for_binding(
        witness_object_id="urn:test:c1-02:at13:witness-bad",
        consumer_query=consumer_query,
        producer_query=producer_query,
        producer_predicate=joint_predicate,
        bindings=[bx],  # only one
        coordinate_value_pairs=[(source["qrefs"]["X"], 1)],
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )

    with pytest.raises(ConditionValueRelationMismatch):
        compose_positioned_subject_possibility(
            repository=source["repo"],
            empirical_query=producer_query,
            predicate=joint_predicate,
            authority_registry=registry,
            release_refs=(source["release_ref"],),
            consumer_query=consumer_query,
            model_rule=fx.make_model_rule(source["universe"].ref, "at13"),
            condition_binding_witness=bad_witness,
        )


def test_at11_fresh_process_runner_reproduces_recursive_composition(tmp_path):
    source = _at11_source()
    qauth = _query_authority("c1-at11-fresh-runner")
    dauth = _d_auth("c1-at11-fresh-runner-discovery")
    pairing = fx.make_pairing_authority("at11-fresh-runner")
    registry = _registry(source, qauth, dauth)

    parent = _branch_predicate(
        source,
        qauth,
        members=tuple(source["respondents"][rid] for rid in ("R1", "R2", "R3", "R4", "R5", "R6")),
        tag="c1-at11-fresh-runner-parent",
    )
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="c1-at11-fresh-runner-x1")
    x_query = _query(source, qauth, parent, ("X",), tag="c1-at11-fresh-runner-g1-x")

    grammar = _grammar(
        operation="I03-OP-c1-at11-fresh-runner-discovery",
        atoms=[_atom("PARENT", parent, "BRANCH"), _atom("X1", x1, "RESPONSE")],
        templates=[_qt("X", x_query)],
        rules=[_rule(
            "child", "RECURSIVE_SUBGROUP_FORK", "SINGLE_ATOM",
            atom_ids=("X1",), baseline_atom_id="PARENT", query_template_id="X",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
        k=2,
    )
    authority = _discovery_authority(source, grammar, dauth, tag="c1-at11-fresh-runner-g1")
    g1 = execute_exact_bounded_discovery_with_handoffs(
        repository=source["repo"],
        discovery_authority=authority,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
        predicate_catalog=(parent, x1),
        query_template_catalog=(x_query,),
    )
    handoff = g1.handoffs[0]

    bundle_path = tmp_path / "child.bundle.json"
    from rawlsing_next.pre553_recursive_handoff import write_recursive_handoff_bundle
    write_recursive_handoff_bundle(bundle_path, g1.handoffs)

    outputs = []
    repo_root = Path(__file__).resolve().parents[2]
    for index in (1, 2):
        out = tmp_path / f"fresh-{index}.json"
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "rawlsing_next.tests.c1_at08_at13_fresh_process_runner",
                str(bundle_path),
                str(out),
            ],
            cwd=repo_root,
            check=True,
            text=True,
            capture_output=True,
        )
        assert completed.returncode == 0, completed.stderr
        outputs.append(json.loads(out.read_text(encoding="utf-8")))

    assert outputs[0] == outputs[1]
    replay = outputs[0]
    assert replay["producer_route"] == "MX01R2_RECURSIVE_TO_POSITIONED_SUBJECT"
    assert replay["analytical_state"] == "SUPPORTED"
    assert replay["coverage_state"] == "RECURSIVE_DEPTH_CONTINUATION"
    assert replay["handoff_ref"] == handoff.ref.as_dict()
    assert replay["consumer_result_state"] == "EXACT_SUPPORTED"
