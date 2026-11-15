"""C1-02 higher-order / joint / recursive analytical composition courts (AT08-AT13)."""
from __future__ import annotations

import json
import subprocess
import sys
from collections.abc import Mapping
from fractions import Fraction
from pathlib import Path

import pytest

from rawlsing_next.pre553_analytical_composition import (
    AnalyticalCompositionError,
    AnalyticalCompositionResult,
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


# ===========================================================================
# C1-02 correction pass.
#
# The courts below close the acceptance gaps identified in the receipt audit.
# Every oracle here is hand-derived from the frozen fixture tables recorded in
# c1_at08_at13_fixture.py (ATTITUDE_ORACLE, XOR_ORACLE, EQUAL_MARGINALS_ORACLE,
# MINORITY_ORACLE, COTRAVEL_ORACLE, RANKED_ORACLE). No oracle is copied from
# candidate output.
# ===========================================================================


def _atom_values(node, coordinate_ref):
    """Collect exact values of every predicate leaf bound to one coordinate ref.

    ``EmpiricalPredicate.predicate_ast`` materializes as a read-only mappingproxy,
    so this walks the ``Mapping`` ABC rather than ``dict``.
    """
    if isinstance(node, (list, tuple)):
        found = []
        for item in node:
            found.extend(_atom_values(item, coordinate_ref))
        return tuple(found)
    if not isinstance(node, Mapping):
        return ()
    found = []
    if node.get("leaf_type") == "EMPIRICAL_POSITION_COORDINATE":
        if node.get("coordinate_semantic_ref") == coordinate_ref:
            found.append(node.get("exact_value"))
    for value in node.values():
        found.extend(_atom_values(value, coordinate_ref))
    return tuple(found)


def _cells(result):
    return {
        cell["cell"]: cell["raw_numerator_support"]
        for cell in result.complete_cell_geometry
    }


# ---------------------------------------------------------------------------
# AT08 - attitude/value conditioning onto a different attitude target
# ---------------------------------------------------------------------------


def _attitude_source_and_authority(tag="at08"):
    source = fx.attitude_fixture(f"c1-at08-{tag}")
    qauth = _query_authority(f"c1-at08-{tag}")
    return source, qauth, _registry(source, qauth)


def _attitude_domain():
    return [["support", "oppose"]]


def test_at08_attitude_condition_drives_different_attitude_target():
    """AT08(1): an attitude/value condition -> a different attitude target."""
    source, qauth, registry = _attitude_source_and_authority("attitude")

    result, _, _, _, _ = fx.direct_condition_composition(
        source=source,
        qauth=qauth,
        registry=registry,
        conditions=[("RESPONSE", "ATT1", "agree")],
        target_question="ATT2",
        tag="at08-agree",
        target_domain=_attitude_domain(),
    )

    oracle = fx.ATTITUDE_ORACLE
    assert result.analytical_state == "SUPPORTED"
    assert result.raw_denominator_support == oracle["denominator_when_agree"]
    cells = _cells(result)
    assert cells["support"] == oracle["P(support | agree)"][0]
    assert cells["oppose"] == oracle["P(oppose | agree)"][0]
    assert result.consumer_result_or_null.result_state == "EXACT_SUPPORTED"

    disagree, _, _, _, _ = fx.direct_condition_composition(
        source=source,
        qauth=qauth,
        registry=registry,
        conditions=[("RESPONSE", "ATT1", "disagree")],
        target_question="ATT2",
        tag="at08-disagree",
        target_domain=_attitude_domain(),
    )
    assert disagree.raw_denominator_support == oracle["denominator_when_disagree"]
    disagree_cells = _cells(disagree)
    assert disagree_cells["support"] == oracle["P(support | disagree)"][0]
    assert disagree_cells["oppose"] == oracle["P(oppose | disagree)"][0]
    # The two attitude conditions do not share a denominator member set.
    assert disagree.composed_result_identity_hash != result.composed_result_identity_hash


def test_at08_exact_conditioner_values_are_in_identity_not_labels_only():
    """AT08(3)+(4): exact conditioner values, and value change reidentifies."""
    source, qauth, registry = _attitude_source_and_authority("values")

    def compose(value, tag):
        return fx.direct_condition_composition(
            source=source,
            qauth=qauth,
            registry=registry,
            conditions=[("RESPONSE", "ATT1", value)],
            target_question="ATT2",
            tag=tag,
            target_domain=_attitude_domain(),
        )

    agree_result, agree_query, agree_witness, _, _ = compose("agree", "at08-val-agree")
    disagree_result, disagree_query, disagree_witness, _, _ = compose("disagree", "at08-val-disagree")

    # The binding carries the exact value, not only a display label.
    agree_material = dict(agree_witness.identity_material)
    disagree_material = dict(disagree_witness.identity_material)
    assert "agree" in str(agree_material["producer_predicate_leaf_projections"])
    assert "disagree" in str(disagree_material["producer_predicate_leaf_projections"])

    # Changing exactly one conditioner value changes the consumer query identity.
    assert agree_query.ref != disagree_query.ref
    # ...and changes the composed identity.
    assert agree_result.composed_result_identity_hash != disagree_result.composed_result_identity_hash
    assert agree_result.consumer_binding_fingerprint != disagree_result.consumer_binding_fingerprint


def test_at08_incompatible_release_context_fails_closed():
    """AT08(5): incompatible release context fails closed rather than coerced."""
    source, qauth, registry = _attitude_source_and_authority("release-hostile")
    other = fx.attitude_fixture("c1-at08-release-hostile-other")

    predicate = _predicate(source, qauth, _response_leaf(source, qauth, "ATT1", "agree"), tag="at08-rh-p")
    query = fx.with_target_domains(
        _query(source, qauth, predicate, ("ATT2",), tag="at08-rh-q"), _attitude_domain()
    )
    pairing = fx.make_pairing_authority("at08-release-hostile")
    binding = fx.make_conditioner_binding(
        binding_id="att1",
        subject_fact_ref=ExactRef(**fx.subject_fact_ref(source, "ATT1", "agree")),
        empirical_coordinate_ref=source["qrefs"]["ATT1"],
        comparability_authority_ref=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=other["release_ref"],
    )
    consumer_query = fx.make_multi_conditioner_consumer_query(
        query_id="at08-release-hostile-consumer",
        subject_ref=ExactRef("C1_SYNTHETIC_POSITIONED_SUBJECT@1", "urn:test:c1-02:at08-rh", semantic_hash({"f": 1})),
        target_ref=source["qrefs"]["ATT2"],
        source_universe_ref=source["universe"].ref,
        release_ref=other["release_ref"],
        bindings=[binding],
        projection_kind="C1_AT08_RELEASE_HOSTILE",
    )
    witness = fx.build_witness_for_binding(
        witness_object_id="urn:test:c1-02:at08-rh:witness",
        consumer_query=consumer_query,
        producer_query=query,
        producer_predicate=predicate,
        bindings=[binding],
        coordinate_value_pairs=[(source["qrefs"]["ATT1"], "agree")],
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )

    with pytest.raises(AnalyticalCompositionError, match="SOURCE_RELEASE_MISMATCH"):
        compose_positioned_subject_possibility(
            repository=source["repo"],
            empirical_query=query,
            predicate=predicate,
            authority_registry=registry,
            release_refs=(source["release_ref"],),
            consumer_query=consumer_query,
            model_rule=fx.make_model_rule(source["universe"].ref, "at08-release-hostile"),
            condition_binding_witness=witness,
        )


def test_at08_incompatible_universe_context_fails_closed():
    """AT08(5): incompatible source universe fails closed."""
    source, qauth, registry = _attitude_source_and_authority("universe-hostile")
    other = fx.attitude_fixture("c1-at08-universe-hostile-other")

    predicate = _predicate(source, qauth, _response_leaf(source, qauth, "ATT1", "agree"), tag="at08-uh-p")
    query = fx.with_target_domains(
        _query(source, qauth, predicate, ("ATT2",), tag="at08-uh-q"), _attitude_domain()
    )
    pairing = fx.make_pairing_authority("at08-universe-hostile")
    binding = fx.make_conditioner_binding(
        binding_id="att1",
        subject_fact_ref=ExactRef(**fx.subject_fact_ref(source, "ATT1", "agree")),
        empirical_coordinate_ref=source["qrefs"]["ATT1"],
        comparability_authority_ref=pairing,
        source_universe_ref=other["universe"].ref,
        release_ref=source["release_ref"],
    )
    consumer_query = fx.make_multi_conditioner_consumer_query(
        query_id="at08-universe-hostile-consumer",
        subject_ref=ExactRef("C1_SYNTHETIC_POSITIONED_SUBJECT@1", "urn:test:c1-02:at08-uh", semantic_hash({"f": 2})),
        target_ref=source["qrefs"]["ATT2"],
        source_universe_ref=other["universe"].ref,
        release_ref=source["release_ref"],
        bindings=[binding],
        projection_kind="C1_AT08_UNIVERSE_HOSTILE",
    )
    witness = fx.build_witness_for_binding(
        witness_object_id="urn:test:c1-02:at08-uh:witness",
        consumer_query=consumer_query,
        producer_query=query,
        producer_predicate=predicate,
        bindings=[binding],
        coordinate_value_pairs=[(source["qrefs"]["ATT1"], "agree")],
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )

    with pytest.raises(AnalyticalCompositionError, match="SOURCE_UNIVERSE_MISMATCH"):
        compose_positioned_subject_possibility(
            repository=source["repo"],
            empirical_query=query,
            predicate=predicate,
            authority_registry=registry,
            release_refs=(source["release_ref"],),
            consumer_query=consumer_query,
            model_rule=fx.make_model_rule(source["universe"].ref, "at08-universe-hostile"),
            condition_binding_witness=witness,
        )


def test_at08_incompatible_measure_context_fails_closed():
    """AT08(5): RAW/weighted measure identity is never bridged."""
    source, qauth, registry = _attitude_source_and_authority("measure-hostile")
    predicate = _predicate(source, qauth, _response_leaf(source, qauth, "ATT1", "agree"), tag="at08-mh-p")
    raw_query = fx.with_target_domains(
        _query(source, qauth, predicate, ("ATT2",), tag="at08-mh-raw"), _attitude_domain()
    )
    weighted_query = fx.with_target_domains(
        _query(source, qauth, predicate, ("ATT2",), tag="at08-mh-w", measure="GOVERNED_WEIGHTED"),
        _attitude_domain(),
    )
    pairing = fx.make_pairing_authority("at08-measure-hostile")
    binding = fx.make_conditioner_binding(
        binding_id="att1",
        subject_fact_ref=ExactRef(**fx.subject_fact_ref(source, "ATT1", "agree")),
        empirical_coordinate_ref=source["qrefs"]["ATT1"],
        comparability_authority_ref=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    consumer_query = fx.make_multi_conditioner_consumer_query(
        query_id="at08-measure-hostile-consumer",
        subject_ref=ExactRef("C1_SYNTHETIC_POSITIONED_SUBJECT@1", "urn:test:c1-02:at08-mh", semantic_hash({"f": 3})),
        target_ref=source["qrefs"]["ATT2"],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=[binding],
        projection_kind="C1_AT08_MEASURE_HOSTILE",
    )
    witness = fx.build_witness_for_binding(
        witness_object_id="urn:test:c1-02:at08-mh:witness",
        consumer_query=consumer_query,
        producer_query=weighted_query,
        producer_predicate=predicate,
        bindings=[binding],
        coordinate_value_pairs=[(source["qrefs"]["ATT1"], "agree")],
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )

    # The witness is bound to the weighted query, but the composition is driven by
    # the RAW query, so the exact measure basis must not be silently bridged.
    with pytest.raises(AnalyticalCompositionError):
        compose_positioned_subject_possibility(
            repository=source["repo"],
            empirical_query=raw_query,
            predicate=predicate,
            authority_registry=registry,
            release_refs=(source["release_ref"],),
            consumer_query=consumer_query,
            model_rule=fx.make_model_rule(source["universe"].ref, "at08-measure-hostile"),
            condition_binding_witness=witness,
        )


# ---------------------------------------------------------------------------
# AT09 - higher-order XOR signal and equal-marginals / different-joints
# ---------------------------------------------------------------------------


def _xor_rate(source, qauth, ast, tag):
    predicate = _branch_predicate(source, qauth, tag=tag) if ast is None else _predicate(source, qauth, ast, tag=tag)
    fact = _run(source, qauth, predicate, _query(source, qauth, predicate, ("C",), tag=tag)).facts[0]
    assert fact.typed_state == "SUPPORTED"
    rows = {r["cell"]: r["raw_numerator_support"] for r in fact.target_topology["complete_cell_semantic_projection"]}
    return rows["1"], fact.raw_denominator_support


def test_at09_xor_unary_marginals_flat_but_joint_configuration_decisive():
    """AT09 XOR: individual marginal signal is flat; the joint carries the rule."""
    source = fx.xor_fixture()
    qauth = _query_authority("c1-at09-xor")
    leaf = lambda name, value: _response_leaf(source, qauth, name, value)
    oracle = fx.XOR_ORACLE

    unary = {
        "P(C=1)": _xor_rate(source, qauth, None, "xor-none"),
        "P(C=1|A=0)": _xor_rate(source, qauth, leaf("A", 0), "xor-a0"),
        "P(C=1|A=1)": _xor_rate(source, qauth, leaf("A", 1), "xor-a1"),
        "P(C=1|B=0)": _xor_rate(source, qauth, leaf("B", 0), "xor-b0"),
        "P(C=1|B=1)": _xor_rate(source, qauth, leaf("B", 1), "xor-b1"),
    }
    for label, actual in unary.items():
        assert actual == oracle["unary_marginal_flat"][label], label

    joint = {
        "P(C=1|A=0,B=0)": _xor_rate(source, qauth, {"op": "AND", "children": [leaf("A", 0), leaf("B", 0)]}, "xor-j00"),
        "P(C=1|A=0,B=1)": _xor_rate(source, qauth, {"op": "AND", "children": [leaf("A", 0), leaf("B", 1)]}, "xor-j01"),
        "P(C=1|A=1,B=0)": _xor_rate(source, qauth, {"op": "AND", "children": [leaf("A", 1), leaf("B", 0)]}, "xor-j10"),
        "P(C=1|A=1,B=1)": _xor_rate(source, qauth, {"op": "AND", "children": [leaf("A", 1), leaf("B", 1)]}, "xor-j11"),
    }
    for label, actual in joint.items():
        assert actual == oracle["joint_decisive"][label], label

    # The joint rule is decisive where every unary marginal is flat. The frozen
    # oracle rates are 1/2 for all five unary views; only the denominators differ.
    assert {Fraction(*value) for value in unary.values()} == {Fraction(1, 2)}
    assert {Fraction(*value) for value in joint.values()} == {Fraction(0, 1), Fraction(1, 1)}
    # A marginal-only view cannot distinguish the two joint outcomes.
    assert len(unary) == 5 and len(joint) == 4


def test_at09_xor_joint_composition_preserves_higher_order_signal():
    """AT09: the composed/consumer path carries the joint XOR outcome."""
    source = fx.xor_fixture()
    qauth = _query_authority("c1-at09-xor")
    registry = _registry(source, qauth)

    result, consumer_query, _, _, _ = fx.direct_condition_composition(
        source=source,
        qauth=qauth,
        registry=registry,
        conditions=[("RESPONSE", "A", 1), ("RESPONSE", "B", 0)],
        target_question="C",
        tag="at09-joint",
    )
    assert result.analytical_state == "SUPPORTED"
    assert result.raw_denominator_support == fx.XOR_ORACLE["joint_decisive"]["P(C=1|A=1,B=0)"][1]
    assert _cells(result)["1"] == fx.XOR_ORACLE["joint_decisive"]["P(C=1|A=1,B=0)"][0]
    assert result.consumer_result_or_null.result_state == "EXACT_SUPPORTED"
    # Both conditioners survive into the consumer-facing identity.
    assert len(consumer_query.conditioner_bindings) == 2


def test_at09_equal_marginals_different_joints_reidentify():
    """AT09: equal relevant marginals, different joint structure/outcome."""
    left, right = fx.equal_marginals_fixtures()
    qauth = _query_authority("c1-at09-equal")
    oracle = fx.EQUAL_MARGINALS_ORACLE

    def joint_geometry(source, tag):
        registry = _registry(source, qauth)
        predicate = _branch_predicate(source, qauth, tag=f"{tag}-branch")
        fact = _run(
            source,
            qauth,
            predicate,
            _query(source, qauth, predicate, ("A", "B"), tag=f"{tag}-joint"),
        ).facts[0]
        assert fact.typed_state == "SUPPORTED"
        cells = {
            tuple(row["cell"]): row["raw_numerator_support"]
            for row in fact.target_topology["complete_cell_semantic_projection"]
        }
        assert fact.raw_denominator_support == oracle["denominator"]
        # Univariate marginals are identical across both configurations.
        for question in ("A", "B"):
            ones = sum(count for cell, count in cells.items() if cell[("A", "B").index(question)] == "1")
            assert ones == oracle["shared_marginals"]["P(A=1)"][0]
        return cells

    left_cells = joint_geometry(left, "left")
    right_cells = joint_geometry(right, "right")

    # Identical marginals, different joint structure.
    assert left_cells != right_cells
    assert left_cells[("0", "0")] == oracle["left_joint"]["0,0"]
    assert right_cells[("0", "1")] == oracle["right_joint"]["0,1"]

    # The composed path preserves the distinction rather than collapsing to marginals.
    left_result, _, _, _, _ = fx.direct_condition_composition(
        source=left, qauth=qauth, registry=_registry(left, qauth),
        conditions=[("RESPONSE", "A", 1)], target_question="B", tag="at09-left",
    )
    right_result, _, _, _, _ = fx.direct_condition_composition(
        source=right, qauth=qauth, registry=_registry(right, qauth),
        conditions=[("RESPONSE", "A", 1)], target_question="B", tag="at09-right",
    )
    assert left_result.raw_denominator_support == right_result.raw_denominator_support
    assert _cells(left_result) != _cells(right_result)
    assert left_result.composed_result_identity_hash != right_result.composed_result_identity_hash


def test_at09_marginal_only_shortcut_cannot_represent_the_joint_outcome():
    """AT09 hostile: a marginal-only or pairwise shortcut fails the court."""
    source = fx.xor_fixture()
    qauth = _query_authority("c1-at09-shortcut")
    registry = _registry(source, qauth)
    leaf = lambda name, value: _response_leaf(source, qauth, name, value)

    unary, _, _, _, _ = fx.direct_condition_composition(
        source=source, qauth=qauth, registry=registry,
        conditions=[("RESPONSE", "A", 1)], target_question="C", tag="at09-shortcut-unary",
    )
    joint, _, _, _, _ = fx.direct_condition_composition(
        source=source, qauth=qauth, registry=registry,
        conditions=[("RESPONSE", "A", 1), ("RESPONSE", "B", 1)], target_question="C", tag="at09-shortcut-joint",
    )

    # The frozen marginal oracle is 1/2; the frozen joint oracle is 0/1. A
    # marginal-only shortcut therefore cannot reproduce the joint outcome.
    assert unary.raw_denominator_support == 2
    assert _cells(unary)["1"] == fx.XOR_ORACLE["unary_marginal_flat"]["P(C=1|A=1)"][0]
    assert joint.raw_denominator_support == 1
    assert _cells(joint)["1"] == fx.XOR_ORACLE["joint_decisive"]["P(C=1|A=1,B=1)"][0]
    assert _cells(unary) != _cells(joint)
    assert unary.composed_result_identity_hash != joint.composed_result_identity_hash
    assert joint.consumer_binding_fingerprint != unary.consumer_binding_fingerprint
    assert unary.consumer_result_or_null.result_state == "EXACT_SUPPORTED"
    assert joint.consumer_result_or_null.result_state == "EXACT_SUPPORTED"


# ---------------------------------------------------------------------------
# AT10 - minority / counterpattern survival
# ---------------------------------------------------------------------------


def test_at10_minority_and_counterpattern_branches_are_supported():
    """AT10: a modal branch and a supported minority/counterpattern branch exist."""
    source = fx.minority_fixture()
    qauth = _query_authority("c1-at10-minority")
    oracle = fx.MINORITY_ORACLE
    for group, size in oracle["group_sizes"].items():
        predicate = _predicate(source, qauth, _coordinate_leaf(source, "G", group), tag=f"at10-g{group}")
        fact = _run(source, qauth, predicate, _query(source, qauth, predicate, ("Y",), tag=f"at10-q{group}")).facts[0]
        rows = {r["cell"]: r["raw_numerator_support"] for r in fact.target_topology["complete_cell_semantic_projection"]}
        assert fact.typed_state == "SUPPORTED", group
        assert fact.raw_denominator_support == size, group
        assert rows["1"] == oracle["support_counts"][group], group
    assert oracle["modal_supported"] and oracle["minority_supported"] and oracle["counterpattern_supported"]


def test_at10_minority_branch_survives_c1_composition():
    """AT10: the composed result preserves the supported minority alternative."""
    source = fx.minority_fixture()
    qauth = _query_authority("c1-at10-minority")
    registry = _registry(source, qauth)

    composed = {}
    for group in ("A", "B", "C"):
        result, _, _, _, _ = fx.direct_condition_composition(
            source=source, qauth=qauth, registry=registry,
            conditions=[("COORDINATE", "G", group)], target_question="Y", tag=f"at10-comp-{group}",
        )
        assert result.analytical_state == "SUPPORTED"
        assert result.consumer_result_or_null.result_state == "EXACT_SUPPORTED"
        composed[group] = result

    # The minority (8) and counterpattern (2) branches keep their own denominators.
    assert composed["A"].raw_denominator_support == fx.MINORITY_ORACLE["group_sizes"]["A"]
    assert composed["B"].raw_denominator_support == fx.MINORITY_ORACLE["group_sizes"]["B"]
    assert composed["C"].raw_denominator_support == fx.MINORITY_ORACLE["group_sizes"]["C"]
    # No branch is collapsed into the modal one.
    assert len({r.composed_result_identity_hash for r in composed.values()}) == 3
    # Ranking the modal branch first does not delete the alternatives.
    ranked = sorted(composed.values(), key=lambda r: -r.raw_denominator_support)
    assert [r.raw_denominator_support for r in ranked] == [10, 8, 2]
    assert all(r.consumer_result_or_null.result_state == "EXACT_SUPPORTED" for r in ranked)


def test_at10_no_supported_discovery_branch_is_silently_deleted():
    """AT10: enumeration of every supported discovery receipt preserves all branches."""
    source = fx.minority_fixture()
    qauth = _query_authority("c1-at10-minority")
    dauth = _d_auth("at10-minority-discovery")
    registry = _registry(source, qauth, dauth)

    all_p = _branch_predicate(source, qauth, tag="at10-all")
    groups = {
        group: _predicate(source, qauth, _coordinate_leaf(source, "G", group), tag=f"at10-atom-{group}")
        for group in ("A", "B", "C")
    }
    yq = _query(source, qauth, all_p, ("Y",), tag="at10-y")
    grammar = _grammar(
        operation="I03-OP-at10-minority-discovery",
        atoms=[_atom("ALL", all_p, "BRANCH")] + [
            _atom(group, predicate, "COORDINATE") for group, predicate in groups.items()
        ],
        templates=[_qt("Y", yq)],
        rules=[
            _rule(
                f"minority-{group}", "MINORITY_OR_NONMODAL_DEPARTURE", "SINGLE_ATOM",
                atom_ids=(group,), baseline_atom_id="ALL", query_template_id="Y",
                validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
            )
            for group in ("A", "B", "C")
        ],
        k=2,
    )
    discovery = _execute_discovery(
        source, qauth, dauth, grammar,
        (all_p, *groups.values()), (yq,),
        authority=_discovery_authority(source, grammar, dauth, tag="at10-minority"),
    )
    supported = [r for r in discovery.receipts if r.typed_state == "DISCOVERED_RESULT_SUPPORTED"]
    assert len(supported) == 3, [r.typed_state for r in discovery.receipts]

    pred_by_ref = {p.ref: p for p in discovery.executed_predicates}
    query_by_ref = {q.ref: q for q in discovery.executed_queries}
    fact_by_ref = {f.ref: f for f in discovery.empirical_facts}

    identities = set()
    denominators = []
    for receipt in supported:
        predicate = pred_by_ref[ExactRef(**receipt.winning_predicate_ref)]
        # The receipt carries the baseline fact alongside the candidate fact; the
        # candidate fact is the one conditioned by the winning predicate.
        fact = next(
            fact_by_ref[ExactRef(**ref)]
            for ref in receipt.empirical_fact_refs
            if ExactRef(**ref) in fact_by_ref
            and ExactRef(**fact_by_ref[ExactRef(**ref)].condition_predicate_ref) == predicate.ref
        )
        query = query_by_ref[ExactRef(**fact.empirical_query_spec_ref)]
        denominators.append(fact.raw_denominator_support)

        pairing = fx.make_pairing_authority("at10-minority")
        atom_values = _atom_values(predicate.predicate_ast, source["crefs"]["G"].as_dict())
        assert len(atom_values) == 1, predicate.predicate_ast
        atom_group = atom_values[0]
        binding = fx.make_conditioner_binding(
            binding_id="g",
            subject_fact_ref=ExactRef(**fx.subject_fact_ref(source, "G", atom_group)),
            empirical_coordinate_ref=source["crefs"]["G"],
            comparability_authority_ref=pairing,
            source_universe_ref=source["universe"].ref,
            release_ref=source["release_ref"],
        )
        consumer_query = fx.make_multi_conditioner_consumer_query(
            query_id=f"at10-consumer-{atom_group}",
            subject_ref=ExactRef(
                "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
                f"urn:test:c1-02:at10-subject-{atom_group}",
                semantic_hash({"fixture_id": f"AT10-{atom_group}"}),
            ),
            target_ref=source["qrefs"]["Y"],
            source_universe_ref=source["universe"].ref,
            release_ref=source["release_ref"],
            bindings=[binding],
            projection_kind="C1_AT10_MINORITY_BRANCH",
        )
        witness = fx.build_witness_for_binding(
            witness_object_id=f"urn:test:c1-02:at10-witness-{atom_group}",
            consumer_query=consumer_query,
            producer_query=query,
            producer_predicate=predicate,
            bindings=[binding],
            coordinate_value_pairs=[(source["crefs"]["G"], atom_group)],
            pairing_authority=pairing,
            source_universe_ref=source["universe"].ref,
            release_ref=source["release_ref"],
            leaf_type="EMPIRICAL_POSITION_COORDINATE",
        )
        result = compose_positioned_subject_possibility(
            repository=source["repo"],
            empirical_query=query,
            predicate=predicate,
            authority_registry=registry,
            release_refs=(source["release_ref"],),
            consumer_query=consumer_query,
            model_rule=fx.make_model_rule(source["universe"].ref, "at10-minority"),
            condition_binding_witness=witness,
            discovery_result=discovery,
            discovery_receipt_ref=receipt.ref,
        )
        assert result.producer_route == "I05_EXACT_BOUNDED_TO_POSITIONED_SUBJECT"
        assert result.analytical_state == "SUPPORTED"
        assert result.consumer_result_or_null.result_state == "EXACT_SUPPORTED"
        identities.add(result.composed_result_identity_hash)

    # Every supported branch produced its own distinct composed result.
    assert len(identities) == len(supported) == 3
    assert sorted(denominators) == sorted(fx.MINORITY_ORACLE["group_sizes"].values())


# ---------------------------------------------------------------------------
# AT11 - true depth-two continuation and lineage anti-aliasing
# ---------------------------------------------------------------------------

_DEPTH2_ROWS = [
    {"id": "R1", "responses": {"X": 1, "H": 1, "Y": 1}},
    {"id": "R2", "responses": {"X": 1, "H": 1, "Y": 0}},
    {"id": "R3", "responses": {"X": 1, "H": 0, "Y": 1}},
    {"id": "R4", "responses": {"X": 1, "H": 0, "Y": 0}},
    {"id": "R5", "responses": {"X": 0, "H": 1, "Y": 1}},
    {"id": "R6", "responses": {"X": 0, "H": 0, "Y": 0}},
]


def _depth2_source(tag="at11-depth2"):
    from rawlsing_next.tests.test_pre553_empirical_query import _build_source

    return _build_source(f"c1-{tag}", _DEPTH2_ROWS)


def _recursive_generation(
    source, qauth, parent_atom, parent_predicate, fork_atom, fork_kind,
    template_query, *, tag, operation,
):
    from rawlsing_next.pre553_recursive_handoff import execute_exact_bounded_discovery_with_handoffs

    dauth = _d_auth(tag)
    registry = _registry(source, qauth, dauth)
    grammar = _grammar(
        operation=operation,
        atoms=[parent_atom, _atom(f"FORK-{tag}", fork_atom, fork_kind)],
        templates=[_qt(f"T-{tag}", template_query)],
        rules=[_rule(
            f"fork-{tag}", "RECURSIVE_SUBGROUP_FORK", "SINGLE_ATOM",
            atom_ids=(f"FORK-{tag}",), baseline_atom_id=parent_atom["atom_id"],
            query_template_id=f"T-{tag}",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        )],
        k=2,
    )
    result = execute_exact_bounded_discovery_with_handoffs(
        repository=source["repo"],
        discovery_authority=_discovery_authority(source, grammar, dauth, tag=tag),
        authority_registry=registry,
        release_refs=(source["release_ref"],),
        predicate_catalog=(parent_predicate, fork_atom),
        query_template_catalog=(template_query,),
    )
    return result, registry


def test_at11_depth_two_continuation_reaches_the_recursive_owner_twice():
    """AT11(1)-(6): generation two is produced by the recursive owner, not simulated."""
    from rawlsing_next.pre553_recursive_handoff import (
        replay_recursive_branch_membership,
        recursive_parent_atom,
    )

    source = _depth2_source("at11-depth2")
    qauth = _query_authority("c1-at11-depth2")

    parent = _branch_predicate(source, qauth, tag="gen1-parent")
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="depth2-x1")
    h1_leaf = _predicate(source, qauth, _response_leaf(source, qauth, "H", 1), tag="depth2-h1")
    gen1_query = _query(source, qauth, parent, ("X",), tag="depth2-gen1-query")

    gen1, registry1 = _recursive_generation(
        source, qauth, _atom("PARENT", parent, "BRANCH"), parent,
        x1, "RESPONSE", gen1_query, tag="depth2gen1", operation="I03-OP-depth2gen1",
    )
    assert [r.typed_state for r in gen1.discovery_result.receipts] == ["DISCOVERED_RESULT_SUPPORTED"]
    handoff1 = gen1.handoffs[0]

    # Generation two re-enters the recursive owner, using the exact public
    # recursive parent atom for the persisted discovered branch.
    child_atom = recursive_parent_atom(handoff1, "CHILD")
    gen2_query = _query(source, qauth, handoff1.winning_predicate, ("H",), tag="depth2-gen2-query")
    gen2, registry2 = _recursive_generation(
        source, qauth, child_atom, handoff1.winning_predicate,
        h1_leaf, "RESPONSE", gen2_query, tag="depth2gen2", operation="I03-OP-depth2gen2",
    )
    assert [r.typed_state for r in gen2.discovery_result.receipts] == ["DISCOVERED_RESULT_SUPPORTED"]
    handoff2 = gen2.handoffs[0]

    # Depth two is a genuinely different branch, not a relabelled depth one.
    assert handoff2.ref != handoff1.ref
    assert handoff2.winning_predicate.ref != handoff1.winning_predicate.ref
    # The immediate parent is the discovered generation-one branch...
    assert handoff2.immediate_parent_branch_ref == handoff1.winning_predicate.ref
    # ...and the full owner-native ancestor chain still names generation one.
    assert handoff1.ref.as_dict() in handoff2.candidate_universe_definition["atoms"][0]["ancestry_refs"]

    # The cohorts are strictly nested rather than aliased.
    cohort1 = replay_recursive_branch_membership(
        repository=source["repo"], handoff=handoff1, authority_registry=registry2
    )
    cohort2 = replay_recursive_branch_membership(
        repository=source["repo"], handoff=handoff2, authority_registry=registry2
    )
    assert len(cohort1) == 4
    assert len(cohort2) == 2
    assert {ref.key for ref in cohort2} < {ref.key for ref in cohort1}

    # The depth-two result is consumed through the C1 analytical/consumer path.
    depth2_query = _query(source, qauth, handoff2.winning_predicate, ("Y",), tag="depth2-consume")
    pairing = fx.make_pairing_authority("at11-depth2")
    binding = fx.make_conditioner_binding(
        binding_id="h",
        subject_fact_ref=ExactRef(**fx.subject_fact_ref(source, "H", 1)),
        empirical_coordinate_ref=source["qrefs"]["H"],
        comparability_authority_ref=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    consumer_query = fx.make_multi_conditioner_consumer_query(
        query_id="at11-depth2-consumer",
        subject_ref=ExactRef(
            "C1_SYNTHETIC_POSITIONED_SUBJECT@1", "urn:test:c1-02:at11-depth2", semantic_hash({"fixture_id": "AT11-D2"})
        ),
        target_ref=source["qrefs"]["Y"],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=[binding],
        projection_kind="C1_AT11_DEPTH_TWO_CONDITIONAL_DISTRIBUTION",
    )
    witness = fx.build_witness_for_binding(
        witness_object_id="urn:test:c1-02:at11-depth2:witness",
        consumer_query=consumer_query,
        producer_query=depth2_query,
        producer_predicate=handoff2.winning_predicate,
        bindings=[binding],
        coordinate_value_pairs=[(source["qrefs"]["H"], 1)],
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    result = compose_positioned_subject_possibility(
        repository=source["repo"],
        empirical_query=depth2_query,
        predicate=handoff2.winning_predicate,
        authority_registry=registry2,
        release_refs=(source["release_ref"],),
        consumer_query=consumer_query,
        model_rule=fx.make_model_rule(source["universe"].ref, "at11-depth2"),
        condition_binding_witness=witness,
        recursive_handoff=handoff2,
    )
    assert result.producer_route == "MX01R2_RECURSIVE_TO_POSITIONED_SUBJECT"
    assert result.analytical_state == "SUPPORTED"
    assert result.raw_denominator_support == 2
    assert result.recursive_handoff_refs == (handoff2.ref,)
    # The consumed lineage carries generation one as well as generation two.
    assert handoff1.ref in result.recursive_lineage_refs
    assert handoff2.immediate_parent_branch_ref in result.recursive_lineage_refs
    assert result.consumer_result_or_null.result_state == "EXACT_SUPPORTED"


def test_at11_lookalike_child_under_different_lineage_does_not_alias():
    """AT11 hostile: same visible child text, different lineage, must not alias."""
    from rawlsing_next.pre553_recursive_handoff import (
        execute_exact_bounded_discovery_with_handoffs,
    )

    source = _depth2_source("at11-lookalike")
    qauth = _query_authority("c1-at11-lookalike")

    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="look-x1")
    parent_six = _branch_predicate(source, qauth, tag="look-parent-six")
    parent_five = _branch_predicate(
        source, qauth,
        members=tuple(source["respondents"][rid] for rid in ("R1", "R2", "R3", "R4", "R5")),
        tag="look-parent-five",
    )

    def run(parent, tag):
        dauth = _d_auth(tag)
        registry = _registry(source, qauth, dauth)
        template = _query(source, qauth, parent, ("X",), tag=f"{tag}-query")
        grammar = _grammar(
            operation=f"I03-OP-{tag}",
            atoms=[_atom("PARENT", parent, "BRANCH"), _atom("X1", x1, "RESPONSE")],
            templates=[_qt("X", template)],
            rules=[_rule(
                f"fork-{tag}", "RECURSIVE_SUBGROUP_FORK", "SINGLE_ATOM",
                atom_ids=("X1",), baseline_atom_id="PARENT", query_template_id="X",
                validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
            )],
            k=2,
        )
        return execute_exact_bounded_discovery_with_handoffs(
            repository=source["repo"],
            discovery_authority=_discovery_authority(source, grammar, dauth, tag=tag),
            authority_registry=registry,
            release_refs=(source["release_ref"],),
            predicate_catalog=(parent, x1),
            query_template_catalog=(template,),
        )

    six = run(parent_six, "looksix").handoffs[0]
    five = run(parent_five, "lookfive").handoffs[0]

    # Both children fork on the identical response atom X=1 -- lookalike text.
    assert six.winning_predicate.predicate_hash != five.winning_predicate.predicate_hash
    # Different lineage must yield different identities at every level.
    assert six.ref != five.ref
    assert six.immediate_parent_branch_ref != five.immediate_parent_branch_ref
    assert six.evaluated_frontier_ref != five.evaluated_frontier_ref

    # Consuming one lineage under the other's predicate fails closed.
    pairing = fx.make_pairing_authority("at11-lookalike")
    foreign_query = _query(source, qauth, six.winning_predicate, ("Y",), tag="look-foreign")
    binding = fx.make_conditioner_binding(
        binding_id="x",
        subject_fact_ref=ExactRef(**fx.subject_fact_ref(source, "X", 1)),
        empirical_coordinate_ref=source["qrefs"]["X"],
        comparability_authority_ref=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    consumer_query = fx.make_multi_conditioner_consumer_query(
        query_id="at11-lookalike-consumer",
        subject_ref=ExactRef(
            "C1_SYNTHETIC_POSITIONED_SUBJECT@1", "urn:test:c1-02:at11-look", semantic_hash({"fixture_id": "AT11-LOOK"})
        ),
        target_ref=source["qrefs"]["Y"],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=[binding],
        projection_kind="C1_AT11_LOOKALIKE_HOSTILE",
    )
    witness = fx.build_witness_for_binding(
        witness_object_id="urn:test:c1-02:at11-look:witness",
        consumer_query=consumer_query,
        producer_query=foreign_query,
        producer_predicate=six.winning_predicate,
        bindings=[binding],
        coordinate_value_pairs=[(source["qrefs"]["X"], 1)],
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    with pytest.raises(RecursiveLineageMismatch, match="winning predicate"):
        compose_positioned_subject_possibility(
            repository=source["repo"],
            empirical_query=foreign_query,
            predicate=six.winning_predicate,
            authority_registry=_registry(source, qauth),
            release_refs=(source["release_ref"],),
            consumer_query=consumer_query,
            model_rule=fx.make_model_rule(source["universe"].ref, "at11-lookalike"),
            condition_binding_witness=witness,
            recursive_handoff=five,
        )


# ---------------------------------------------------------------------------
# AT12 - empirical co-travel with no semantic-relation authority present
# ---------------------------------------------------------------------------


def test_at12_cotravel_reaches_consumer_at_its_direct_empirical_grade():
    """AT12: empirical co-travel evidence stays available to the consumer."""
    source = fx.cotravel_fixture()
    qauth = _query_authority("c1-at12-cotravel")
    registry = _registry(source, qauth)

    result, _, _, _, _ = fx.direct_condition_composition(
        source=source, qauth=qauth, registry=registry,
        conditions=[("RESPONSE", "X", 1)], target_question="Y", tag="at12-cotravel",
    )
    oracle = fx.COTRAVEL_ORACLE
    assert result.analytical_state == "SUPPORTED"
    assert result.raw_denominator_support == oracle["denominator_when_x1"]
    cells = _cells(result)
    assert cells["1"] == oracle["Y1"]
    assert cells["0"] == oracle["Y0"]

    # The exact same-respondent co-travel cohort is retained, not an aggregate.
    ids = sorted(ref.object_id for ref in result.denominator_member_refs)
    by_object_id = {respondent.ref.object_id: rid for rid, respondent in source["respondents"].items()}
    assert sorted(by_object_id[object_id] for object_id in ids) == sorted(oracle["member_ids"])
    # R4 does not travel with X=1 and is therefore outside the cohort.
    assert "R4" not in [by_object_id[object_id] for object_id in ids]

    assert result.consumer_result_or_null.result_state == "EXACT_SUPPORTED"
    assert result.producer_route == "DIRECT_I03_TO_POSITIONED_SUBJECT"


def test_at12_lack_of_semantic_relation_authority_does_not_erase_cotravel():
    """AT12: only the semantic interpretation is absent; the empirical fact is not."""
    source = fx.cotravel_fixture()
    qauth = _query_authority("c1-at12-cotravel")
    registry = _registry(source, qauth)

    result, consumer_query, witness, _, _ = fx.direct_condition_composition(
        source=source, qauth=qauth, registry=registry,
        conditions=[("RESPONSE", "X", 1)], target_question="Y", tag="at12-noerase",
    )

    # Exactly what the C1 analytical path declares as an authority closure.
    resolved_kinds = set()
    fixture_only = []
    for authority_ref in result.authority_refs:
        if authority_ref.authority_id.startswith("urn:test:"):
            # Synthetic fixture-only custody refs are not registry authorities; they
            # exist to bind condition values at the source-free court and carry no
            # semantic-relation authority either.
            fixture_only.append(authority_ref)
            continue
        snapshot = registry.resolve_exact(authority_ref).snapshot
        resolved_kinds.add(snapshot.authority_kind)
        for operation in snapshot.governed_operations:
            assert "SEMANTIC_RELATION" not in operation.upper()

    # The owner-native closure is entirely empirical: source semantics, routing/risk,
    # coordinate semantics, replay and predicate grammar.
    assert resolved_kinds <= {
        "SOURCE_SEMANTICS_TOPOLOGY",
        "ROUTING_RISK_SET",
        "COORDINATE_SEMANTICS",
        "REPLAY_PROTOCOL",
        "PREDICATE_GRAMMAR",
    }
    assert resolved_kinds, "no owner-native empirical authority was retained"
    assert fixture_only, "fixture-only condition-value pairing authority must be present"

    # Absence of any semantic-relation authority leaves the co-travel result intact.
    assert result.analytical_state == "SUPPORTED"
    assert result.consumer_result_or_null.result_state == "EXACT_SUPPORTED"
    assert _cells(result)["1"] == fx.COTRAVEL_ORACLE["Y1"]
    # The consumer receives empirical configuration evidence, not a semantic claim.
    assert result.consumer_model_rule_hash == fx.make_model_rule(
        source["universe"].ref, "at12-noerase"
    ).rule_hash
    assert consumer_query.requested_projection["kind"] == "C1_at12-noerase_CONDITIONAL_DISTRIBUTION"


def test_at12_composition_surface_exposes_no_semantic_relation_authority():
    """AT12: empirical co-travel is not relabelled as semantic relation authority."""
    import inspect

    parameters = set(inspect.signature(compose_positioned_subject_possibility).parameters)
    assert not any(
        token in name.lower() for name in parameters for token in ("semantic_relation", "s14")
    ), parameters

    fields = set(AnalyticalCompositionResult.__dataclass_fields__)
    assert not any(
        token in name.lower() for name in fields for token in ("semantic_relation", "s14")
    ), fields

    # The empirical route the co-travel result travels is a direct empirical grade.
    from rawlsing_next.pre553_analytical_composition import PRODUCER_ROUTE_DIRECT

    assert PRODUCER_ROUTE_DIRECT == "DIRECT_I03_TO_POSITIONED_SUBJECT"
    assert "SEMANTIC" not in PRODUCER_ROUTE_DIRECT


# ---------------------------------------------------------------------------
# AT13 - genuinely non-scalar component morphology
# ---------------------------------------------------------------------------


def _ranked_query(source, qauth, predicate, *, topology, tag):
    from rawlsing_next.tests.pre553_query_frontier_fixtures import _custom_query

    return _custom_query(
        source, qauth, predicate, "RANK",
        topology=topology,
        domain=[["HIGH", "LOW"], ["LOW", "HIGH"]],
        included_states=("SUBSTANTIVE_RESPONSE",),
        tag=tag,
    )


def _ranked_composition(source, qauth, registry, tag):
    from rawlsing_next.tests.pre553_query_frontier_fixtures import _custom_query

    predicate = _predicate(
        source, qauth, _response_leaf(source, qauth, "ATT", "1"), tag=f"{tag}-predicate"
    )
    producer_query = _custom_query(
        source, qauth, predicate, "RANK",
        topology="RANKED_RESPONSE",
        domain=[["HIGH", "LOW"], ["LOW", "HIGH"]],
        included_states=("SUBSTANTIVE_RESPONSE",),
        tag=f"{tag}-query",
    )
    pairing = fx.make_pairing_authority(tag)
    binding = fx.make_conditioner_binding(
        binding_id="att",
        subject_fact_ref=ExactRef(**fx.subject_fact_ref(source, "ATT", "1")),
        empirical_coordinate_ref=source["qrefs"]["ATT"],
        comparability_authority_ref=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    consumer_query = fx.make_multi_conditioner_consumer_query(
        query_id=f"{tag}-consumer",
        subject_ref=ExactRef(
            "C1_SYNTHETIC_POSITIONED_SUBJECT@1", f"urn:test:c1-02:{tag}", semantic_hash({"fixture_id": tag})
        ),
        target_ref=source["qrefs"]["RANK"],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=[binding],
        projection_kind=f"C1_{tag.upper()}_NONSCALAR_COMPONENT_VECTOR",
    )
    witness = fx.build_witness_for_binding(
        witness_object_id=f"urn:test:c1-02:{tag}:witness",
        consumer_query=consumer_query,
        producer_query=producer_query,
        producer_predicate=predicate,
        bindings=[binding],
        coordinate_value_pairs=[(source["qrefs"]["ATT"], "1")],
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    result = compose_positioned_subject_possibility(
        repository=source["repo"],
        empirical_query=producer_query,
        predicate=predicate,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
        consumer_query=consumer_query,
        model_rule=fx.make_model_rule(source["universe"].ref, tag),
        condition_binding_witness=witness,
    )
    return result


def test_at13_ranked_component_order_and_topology_are_preserved():
    """AT13: source-native order, arity/topology, component and target identity survive."""
    source = fx.ranked_fixture("c1-at13-ranked-modal")
    qauth = _query_authority("c1-at13-ranked-modal")
    result = _ranked_composition(source, qauth, _registry(source, qauth), "at13rankmodal")

    assert result.analytical_state == "SUPPORTED"
    assert result.raw_denominator_support == fx.RANKED_ORACLE["denominator"]

    # Arity/topology: one non-scalar ranked component, not a scalarized value.
    assert result.target_arity_and_topology["arity"] == fx.RANKED_ORACLE["arity"]
    assert result.target_arity_and_topology["components"][0]["topology"] == fx.RANKED_ORACLE["topology"]

    # Source-native component order survives into the consumer-facing geometry.
    geometry = result.possibility_slice_evidence_or_null.geometry
    component_material = geometry["target"]["component_material"]
    assert component_material["topology"] == "RANKED_RESPONSE"
    assert component_material["domain"] == [["HIGH", "LOW"], ["LOW", "HIGH"]]
    assert "target_domain_replay_ref" in component_material
    assert component_material["topology_authority_refs"]
    assert component_material["response_semantic_authority_refs"]
    assert component_material["included_states"] == ["SUBSTANTIVE_RESPONSE"]

    # The cell value is the ordered vector itself, in source-native rank order.
    assert result.ordered_target_refs[0] == source["qrefs"]["RANK"]
    cells = {
        tuple(cell["cell"]) if isinstance(cell["cell"], list) else cell["cell"]: cell["raw_numerator_support"]
        for cell in result.complete_cell_geometry
    }
    assert cells[tuple(fx.RANKED_ORACLE["modal_value_vector"])] == fx.RANKED_ORACLE["denominator"]
    assert result.consumer_result_or_null.result_state == "EXACT_SUPPORTED"


def test_at13_reordered_components_reidentify_lawfully():
    """AT13 hostile: reordered components reidentify rather than being normalised."""
    modal = fx.ranked_fixture("c1-at13-reorder-modal")
    reordered = fx.ranked_fixture("c1-at13-reorder-flipped", reverse_rank=True)

    modal_result = _ranked_composition(
        modal, _query_authority("c1-at13-reorder-modal"), _registry(modal, _query_authority("c1-at13-reorder-modal")),
        "at13reordermodal",
    )
    reordered_qauth = _query_authority("c1-at13-reorder-flipped")
    reordered_result = _ranked_composition(
        reordered, reordered_qauth, _registry(reordered, reordered_qauth), "at13reorderflipped",
    )

    # Same arity, same denominator, different ordered value vector.
    assert modal_result.target_arity_and_topology["arity"] == reordered_result.target_arity_and_topology["arity"]
    assert modal_result.raw_denominator_support == reordered_result.raw_denominator_support
    modal_cells = {tuple(c["cell"]): c["raw_numerator_support"] for c in modal_result.complete_cell_geometry}
    reordered_cells = {tuple(c["cell"]): c["raw_numerator_support"] for c in reordered_result.complete_cell_geometry}
    assert modal_cells[tuple(fx.RANKED_ORACLE["modal_value_vector"])] == 3
    assert reordered_cells[tuple(fx.RANKED_ORACLE["reidentified_value_vector"])] == 3
    assert modal_cells != reordered_cells
    # The reordering is preserved as a distinct identity rather than normalised away.
    assert modal_result.composed_result_identity_hash != reordered_result.composed_result_identity_hash


def test_at13_missing_component_vector_may_not_be_scalarized():
    """AT13 hostile: a ranked vector may not be collapsed into a scalar."""
    source = fx.ranked_fixture("c1-at13-nonscalarize")
    qauth = _query_authority("c1-at13-nonscalarize")
    predicate = _predicate(source, qauth, _response_leaf(source, qauth, "ATT", "1"), tag="at13-ns-p")
    scalar_query = _ranked_query(source, qauth, predicate, topology="SCALAR_SINGULAR", tag="at13-ns-scalar")

    fact = _run(source, qauth, predicate, scalar_query).facts[0]
    # The owner refuses the collapse instead of emitting a scalar value.
    assert fact.typed_state != "SUPPORTED"
    assert fact.raw_denominator_support == 0
    assert "UNSUPPORTED_RESPONSE_TOPOLOGY" in str(fact.target_topology.get("p02_failure_state"))


def test_at13_heterogeneous_component_authority_is_fail_closed_not_universal():
    """AT13 hostile: heterogeneous component authority must not become universal."""
    source = fx.ranked_fixture("c1-at13-authority")
    qauth = _query_authority("c1-at13-authority")
    registry = _registry(source, qauth)
    predicate = _predicate(source, qauth, _response_leaf(source, qauth, "ATT", "1"), tag="at13-auth-p")

    ranked_query = _ranked_query(source, qauth, predicate, topology="RANKED_RESPONSE", tag="at13-auth-ranked")
    assert _run(source, qauth, predicate, ranked_query, registry=registry).facts[0].typed_state == "SUPPORTED"

    # A component citing an authority that does not bind the response event must
    # not silently inherit universal topology authority.
    components = [dict(component) for component in ranked_query.target_arity_and_topology["components"]]
    components[0]["topology_authority_refs"] = [source["coord_auth"].authority_ref]
    foreign_query = fx.with_components(ranked_query, components)
    foreign_fact = _run(source, qauth, predicate, foreign_query, registry=registry).facts[0]
    assert foreign_fact.typed_state != "SUPPORTED"
    assert foreign_fact.raw_denominator_support == 0


def test_at11_depth_two_continuation_is_reproducible_in_a_fresh_process(tmp_path):
    """AT11(4)+(5)+(6): fresh process reaches depth two through the recursive owner."""
    from rawlsing_next.pre553_recursive_handoff import write_recursive_handoff_bundle
    from rawlsing_next.tests.c1_at08_at13_fresh_process_runner import gen1_material

    # The parent court persists a bundle from the runner's exact generation-one
    # material, so writer and fresh-process replayer share one identity source.
    material = gen1_material()
    gen1 = material["gen1"]
    assert len(gen1.handoffs) == 1

    bundle_path = tmp_path / "depth2.bundle.json"
    write_recursive_handoff_bundle(bundle_path, gen1.handoffs)

    outputs = []
    repo_root = Path(__file__).resolve().parents[2]
    for index in (1, 2):
        out = tmp_path / f"depth2-fresh-{index}.json"
        completed = subprocess.run(
            [
                sys.executable, "-m",
                "rawlsing_next.tests.c1_at08_at13_fresh_process_runner",
                "--depth-two", str(bundle_path), str(out),
            ],
            cwd=repo_root, check=True, text=True, capture_output=True,
        )
        assert completed.returncode == 0, completed.stderr
        outputs.append(json.loads(out.read_text(encoding="utf-8")))

    # Two independent fresh processes agree byte for byte.
    assert outputs[0] == outputs[1]
    replay = outputs[0]

    assert replay["mode"] == "DEPTH_TWO"
    assert replay["gen1_handoff_ref"] == gen1.handoffs[0].ref.as_dict()
    assert replay["gen2_handoff_ref"] != replay["gen1_handoff_ref"]
    assert replay["gen1_ref_present_in_gen2_ancestry"] is True
    assert len(replay["gen1_child_member_refs"]) == 4
    assert len(replay["gen2_child_member_refs"]) == 2
    # The depth-two cohort is strictly nested inside the depth-one cohort.
    assert {ref["content_hash"] for ref in replay["gen2_child_member_refs"]} < {
        ref["content_hash"] for ref in replay["gen1_child_member_refs"]
    }

    assert replay["producer_route"] == "MX01R2_RECURSIVE_TO_POSITIONED_SUBJECT"
    assert replay["analytical_state"] == "SUPPORTED"
    assert replay["raw_denominator_support"] == 2
    assert replay["consumer_result_state"] == "EXACT_SUPPORTED"
    # The consumed lineage carries generation one as well as generation two.
    lineage = {ref["content_hash"] for ref in replay["recursive_lineage_refs"]}
    assert gen1.handoffs[0].ref.content_hash in lineage


# ===========================================================================
# C1-02-REVIEW-BLOCK-WITNESS-PAIR-001 -- witness pairing-ground-truth repair
#
# The four per-conditioner pairing-ground-truth semantic comparisons were
# unreachable behind an unconditional raise. These courts construct a pairing
# relation that is structurally valid, hash-consistent and freshly
# re-content-addressed, yet semantically false, and require fail-closed
# rejection BEFORE evidence construction and BEFORE consumer invocation.
# ===========================================================================


def _pairing_hostile_material(tag="at08-pairing-hostile"):
    """Valid two-conditioner composition material, returned without composing."""
    from rawlsing_next.pre553_analytical_composition import compose_positioned_subject_possibility
    from rawlsing_next.tests.test_pre553_empirical_query import (
        _coordinate_leaf,
        _predicate,
        _query,
    )

    source = fx.xor_fixture(f"c1-{tag}")
    qauth = _query_authority(f"c1-{tag}")
    registry = _registry(source, qauth)

    a1 = _response_leaf(source, qauth, "A", 1)
    b0 = _response_leaf(source, qauth, "B", 0)
    joint_predicate = _predicate(
        source, qauth, {"op": "AND", "children": [a1, b0]}, tag=f"{tag}-predicate"
    )
    producer_query = _query(source, qauth, joint_predicate, ("C",), tag=f"{tag}-query")

    pairing = fx.make_pairing_authority(tag)
    bindings = []
    pairs = []
    for binding_id, question, value in (("a", "A", 1), ("b", "B", 0)):
        bindings.append(
            fx.make_conditioner_binding(
                binding_id=binding_id,
                subject_fact_ref=ExactRef(**fx.subject_fact_ref(source, question, value)),
                empirical_coordinate_ref=source["qrefs"][question],
                comparability_authority_ref=pairing,
                source_universe_ref=source["universe"].ref,
                release_ref=source["release_ref"],
            )
        )
        pairs.append((source["qrefs"][question], value))

    consumer_query = fx.make_multi_conditioner_consumer_query(
        query_id=f"{tag}-consumer",
        subject_ref=ExactRef(
            "C1_SYNTHETIC_POSITIONED_SUBJECT@1",
            f"urn:test:c1-02:{tag}:subject",
            semantic_hash({"fixture_id": tag}),
        ),
        target_ref=source["qrefs"]["C"],
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
        bindings=bindings,
        projection_kind=f"C1_{tag.upper()}_PAIRING_HOSTILE",
    )
    witness = fx.build_witness_for_binding(
        witness_object_id=f"urn:test:c1-02:{tag}:witness",
        consumer_query=consumer_query,
        producer_query=producer_query,
        producer_predicate=joint_predicate,
        bindings=bindings,
        coordinate_value_pairs=pairs,
        pairing_authority=pairing,
        source_universe_ref=source["universe"].ref,
        release_ref=source["release_ref"],
    )
    return {
        "source": source,
        "registry": registry,
        "predicate": joint_predicate,
        "producer_query": producer_query,
        "consumer_query": consumer_query,
        "witness": witness,
        "pairing": pairing,
    }


def _compose_with(material, witness):
    from rawlsing_next.pre553_analytical_composition import compose_positioned_subject_possibility

    source = material["source"]
    return compose_positioned_subject_possibility(
        repository=source["repo"],
        empirical_query=material["producer_query"],
        predicate=material["predicate"],
        authority_registry=material["registry"],
        release_refs=(source["release_ref"],),
        consumer_query=material["consumer_query"],
        model_rule=fx.make_model_rule(source["universe"].ref, "pairing-hostile"),
        condition_binding_witness=witness,
    )


def test_pairing_hostile_baseline_witness_is_accepted():
    """Control: the unmutated witness composes, so the hostiles below isolate
    the pairing semantics rather than an unrelated breakage."""
    material = _pairing_hostile_material("at08-pairing-control")
    result = _compose_with(material, material["witness"])
    assert result.analytical_state == "SUPPORTED"
    assert result.consumer_result_or_null.result_state == "EXACT_SUPPORTED"
    assert result.pairing_ground_truth_refs == material["witness"].pairing_ground_truth_refs


def test_pairing_hostile_false_required_semantic_ref_is_rejected():
    """C1-02-REVIEW-BLOCK-WITNESS-PAIR-001: false required_semantic_ref.

    The hostile keeps the consumer binding, subject preimage and producer leaf
    untouched. It lies only about which semantic ref the pairing relation
    requires, and re-content-addresses the pairing ref and the enclosing witness
    ref so every hash-integrity check still holds.
    """
    material = _pairing_hostile_material("at08-pairing-false-ref")
    honest = material["witness"]

    # A real, structurally valid coordinate ref that is simply the WRONG one.
    false_semantic_ref = ExactRef(
        "QUESTION_NATIVE",
        "urn:test:c1-02:at08-pairing-false-ref:not-the-real-condition",
        semantic_hash({"deliberately": "wrong semantic ref"}),
    )
    hostile = fx.readdress_witness_with_false_pairing(
        honest, conditioner_index=0, false_semantic_ref=false_semantic_ref
    )

    # The hostile is internally hash-consistent: no hash or ref was corrupted.
    hostile.verify_identity()
    assert hostile.witness_ref.content_hash != honest.witness_ref.content_hash
    assert hostile.pairing_ground_truth_refs[0].content_hash != honest.pairing_ground_truth_refs[0].content_hash
    # The binding / subject / producer-leaf truth is provably unchanged.
    assert hostile.subject_condition_preimage_refs == honest.subject_condition_preimage_refs
    assert hostile.producer_predicate_leaf_refs == honest.producer_predicate_leaf_refs
    assert hostile.pairing_authority_refs == honest.pairing_authority_refs
    assert hostile.producer_predicate_leaf_projections == honest.producer_predicate_leaf_projections
    # And the lie is real: the pairing no longer names the subject's own ref.
    assert hostile.pairing_ground_truth_materials[0]["required_semantic_ref"] != (
        honest.pairing_ground_truth_materials[0]["required_semantic_ref"]
    )

    with pytest.raises(ConditionValueRelationMismatch) as excinfo:
        _compose_with(material, hostile)

    message = str(excinfo.value)
    assert "pairing" in message
    # Rejected before evidence construction and before the consumer is invoked.
    assert "evidence" not in message
    assert excinfo.value.__cause__ is None


def test_pairing_hostile_false_required_exact_value_is_rejected():
    """C1-02-REVIEW-BLOCK-WITNESS-PAIR-001: false required_exact_value.

    Same construction, mutating the required exact value instead of the semantic
    ref: the pairing claims the relation holds for a different value than the one
    the unchanged subject preimage carries.
    """
    material = _pairing_hostile_material("at08-pairing-false-value")
    honest = material["witness"]

    # Conditioner 1 is B=0, so the truthful required value is "0"; claim "1".
    hostile = fx.readdress_witness_with_false_pairing(
        honest, conditioner_index=1, false_exact_value="1"
    )
    hostile.verify_identity()
    assert honest.pairing_ground_truth_materials[1]["required_exact_value"] == "0"
    assert hostile.pairing_ground_truth_materials[1]["required_exact_value"] == "1"
    assert hostile.pairing_ground_truth_materials[1]["required_exact_value"] != (
        honest.pairing_ground_truth_materials[1]["required_exact_value"]
    )
    assert hostile.subject_condition_preimage_materials == honest.subject_condition_preimage_materials

    with pytest.raises(ConditionValueRelationMismatch) as excinfo:
        _compose_with(material, hostile)

    assert "pairing" in str(excinfo.value)


def test_pairing_hostile_rejection_precedes_evidence_and_consumer():
    """Explicit ordering proof: the hostile never reaches evidence or consumer.

    The consumer and the evidence builder are both replaced with sentinels that
    raise if touched. Because the composition raises first, neither sentinel can
    fire, which demonstrates fail-closed ordering rather than merely an error.
    """
    import rawlsing_next.pre553_analytical_composition as composition_module

    material = _pairing_hostile_material("at08-pairing-ordering")
    hostile = fx.readdress_witness_with_false_pairing(
        material["witness"],
        conditioner_index=0,
        false_exact_value="definitely-not-the-bound-value",
    )

    touched = []

    def forbidden_evidence(*args, **kwargs):
        touched.append("evidence")
        raise AssertionError("possibility evidence must not be constructed")

    def forbidden_consumer(*args, **kwargs):
        touched.append("consumer")
        raise AssertionError("the consumer must not be invoked")

    original_builder = composition_module._build_evidence
    original_consumer = composition_module.evaluate_positioned_subject_possibility
    composition_module._build_evidence = forbidden_evidence
    composition_module.evaluate_positioned_subject_possibility = forbidden_consumer
    try:
        with pytest.raises(ConditionValueRelationMismatch):
            _compose_with(material, hostile)
    finally:
        composition_module._build_evidence = original_builder
        composition_module.evaluate_positioned_subject_possibility = original_consumer

    assert touched == [], f"composition reached {touched} before rejecting"
