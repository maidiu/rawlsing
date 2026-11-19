"""PYAT #1009: actual native I03 -> generic FF01 descriptive SOURCEFREE consumer.

The fixture calls the protected C11Repository/I03 owners, not a fabricated
precomputed joint.  It is NOT a persisted cold estate or independent G5 court.
"""
from dataclasses import replace
from itertools import product

import pytest

from rawlsing_next._pre553_query_common import QueryExecutionResult
from rawlsing_next.pre553_empirical_objects import EmpiricalFact, ExactRef, semantic_hash
from rawlsing_next.field_forge_generic_empirical_ingress import (
    FF01GenericIngressError,
    execute_ff01_observed_joint,
    receive_ff01_observed_joint,
    replay_ff01_observed_joint,
)
from rawlsing_next.tests import test_pre553_empirical_query as native


PERMISSIONS = ("FF01_DESCRIPTIVE_SOURCEFREE",)


def _case(parity: int = 0, *, tag="FF01-GENERIC"):
    rows = [
        {"id": f"R{x}{y}", "responses": {"X": x, "Y": y, "Z": x ^ y ^ parity}}
        for x, y in product((0, 1), repeat=2)
    ]
    source = native._build_source(tag, rows, question_namespace="FF01-SHARED")
    qauth = native._query_authority(tag)
    predicate = native._branch_predicate(source, qauth)
    query = native._query(source, qauth, predicate, ("X", "Y", "Z"), tag=tag)
    result = native._run(source, qauth, predicate, query)
    assert len(result.facts) == 1
    assert result.facts[0].typed_state == "SUPPORTED"
    return source, qauth, predicate, query, result


def _receive(query, result, **kw):
    return receive_ff01_observed_joint(
        execution=result, query=query,
        conditioner_index=kw.pop("conditioner_index", 0),
        producer_permission_ceiling=kw.pop("producer_permission_ceiling", PERMISSIONS),
        **kw,
    )


def _replace_fact(fact, **fields):
    material = dict(fact.semantic_fields)
    material.update(fields)
    return EmpiricalFact(
        typed_state=fact.typed_state,
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=fact.dependency_refs,
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
        **material,
    )


def _changed_result(result: QueryExecutionResult, **fields):
    return replace(result, facts=(_replace_fact(result.facts[0], **fields),))


def _cell_count(received, *states):
    material = received.semantic_projection()
    return next(
        row["raw_support"] for row in material["complete_cells"]
        if row["cell"] == list(states)
    )


def test_actual_native_three_way_i03_consumed_without_synthetic_pairwise_joint():
    _, _, _, query, result = _case()
    received = _receive(query, result)
    p = received.semantic_projection()
    assert p["joint_arity"] == 3
    assert len(p["complete_cells"]) == 8
    assert p["raw_eligible_condition_denominator"] == 4
    assert p["raw_fully_resolved_joint_n"] == 4
    assert p["producer_fact_ref"] == result.facts[0].ref.as_dict()
    assert p["source_permission_grade"] == "CALLER_DECLARED__NOT_INDEPENDENTLY_ISSUED"
    assert _cell_count(received, "0", "0", "0") == 1
    assert _cell_count(received, "0", "0", "1") == 0
    assert sum(row["fully_resolved_condition_n"] for row in p["conditioned_complete_case_support"]) == 4
    assert "N10E_V3_ACTOR_NOT_CONSUMED_HERE" in p["not_proven"]


def test_same_pairwise_marginals_but_opposite_triples_survive_at_real_ff01_reader():
    # The parity and anti-parity populations agree on all unary/pairwise
    # marginals while the 3-way joint changes.
    _, _, _, q0, r0 = _case(0, tag="FF01-PARITY")
    _, _, _, q1, r1 = _case(1, tag="FF01-ANTIPARITY")
    left, right = _receive(q0, r0), _receive(q1, r1)
    assert _cell_count(left, "0", "0", "0") == 1
    assert _cell_count(right, "0", "0", "0") == 0
    assert left.ref != right.ref


def test_direct_I03_execution_is_one_real_producer_and_no_learned_gate():
    source, qa, predicate, query, _ = _case()
    observed = execute_ff01_observed_joint(
        repository=source["repo"],
        query=query, predicate=predicate,
        authority_registry=native._registry(source, qa),
        release_refs=(source["release_ref"],),
        conditioner_index=0,
        producer_permission_ceiling=PERMISSIONS,
    )
    assert observed.semantic_projection()["joint_arity"] == 3
    assert observed.semantic_projection()["producer_state"] == "SUPPORTED"


def test_choice_of_actual_conditioner_changes_profile_without_requerying_source():
    _, _, _, query, result = _case()
    a = _receive(query, result, conditioner_index=0)
    b = _receive(query, result, conditioner_index=2)
    assert a.ref != b.ref
    assert a.semantic_projection()["conditioner_ref"] == query.target_refs[0]
    assert b.semantic_projection()["conditioner_ref"] == query.target_refs[2]
    assert all(
        sum(row["raw_support"] for row in group["remaining_joint_cells"])
        == group["fully_resolved_condition_n"]
        for group in b.semantic_projection()["conditioned_complete_case_support"]
    )


def test_source_mutation_changes_ff01_result_and_exact_replay_refuses_old():
    _, _, _, q0, r0 = _case(0, tag="FF01-SOURCE-CHANGE")
    _, _, _, q1, r1 = _case(1, tag="FF01-SOURCE-CHANGE")
    old = _receive(q0, r0)
    changed = _receive(q1, r1)
    assert old.ref != changed.ref
    assert replay_ff01_observed_joint(
        old.ref, execution=r0, query=q0, conditioner_index=0,
        producer_permission_ceiling=PERMISSIONS,
    ).ref == old.ref
    with pytest.raises(FF01GenericIngressError, match="replay|changed"):
        replay_ff01_observed_joint(
            old.ref, execution=r1, query=q1, conditioner_index=0,
            producer_permission_ceiling=PERMISSIONS,
        )


def test_untrusted_export_cannot_mutate_hash_identified_ff01_result():
    _, _, _, query, result = _case()
    original = _receive(query, result)
    out = original.semantic_projection()
    out["complete_cells"][0]["raw_support"] = 1_000_000
    assert original.semantic_projection()["complete_cells"][0]["raw_support"] != 1_000_000
    assert original.ref == _receive(query, result).ref


def test_permission_ceiling_cannot_widen_into_causal_use():
    _, _, _, query, result = _case()
    with pytest.raises(FF01GenericIngressError, match="widen"):
        _receive(query, result, relation_permission_ceiling=("STRONG_CAUSAL",))
    accepted = _receive(query, result, relation_permission_ceiling=PERMISSIONS)
    assert accepted.semantic_projection()["relation_permission_ceiling"] == list(PERMISSIONS)


def test_fact_query_risk_and_universe_substitutions_are_rejected():
    _, _, _, query, result = _case()
    wrong = ExactRef("RISK_SET", "urn:test:foreign-risk", semantic_hash("foreign-risk"))
    bad = _changed_result(result, risk_set_ref=wrong)
    with pytest.raises(FF01GenericIngressError, match="risk"):
        _receive(query, bad)
    bad = _changed_result(result, empirical_universe_refs=(wrong,))
    with pytest.raises(FF01GenericIngressError, match="universe"):
        _receive(query, bad)


def test_complete_cell_omission_and_zero_as_positive_are_rejected():
    _, _, _, query, result = _case()
    fact = result.facts[0]
    topology = dict(fact.target_topology)
    cells = [dict(row) for row in topology["complete_cell_semantic_projection"]]
    topology["complete_cell_semantic_projection"] = cells[:-1]
    with pytest.raises(FF01GenericIngressError, match="incomplete"):
        _receive(query, _changed_result(result, target_topology=topology))
    cells = [dict(row) for row in fact.target_topology["complete_cell_semantic_projection"]]
    zero = next(row for row in cells if row["raw_numerator_support"] == 0)
    zero["cell_state"] = "OBSERVED_POSITIVE"
    topology["complete_cell_semantic_projection"] = cells
    with pytest.raises(FF01GenericIngressError, match="cell status"):
        _receive(query, _changed_result(result, target_topology=topology))


def test_missing_producer_provenance_and_release_are_not_accepted():
    _, _, _, query, result = _case()
    wrong = ExactRef("RELEASE", "urn:test:foreign-release", semantic_hash("release"))
    with pytest.raises(FF01GenericIngressError, match="release"):
        _receive(query, replace(result, release_refs=(wrong,)))
    with pytest.raises(FF01GenericIngressError, match="evidence"):
        _receive(query, _changed_result(result, source_empirical_provenance_refs=()))


def test_raw_measurement_cannot_carry_weighted_joint_cell():
    _, _, _, query, result = _case()
    topology = dict(result.facts[0].target_topology)
    cells = [dict(row) for row in topology["complete_cell_semantic_projection"]]
    cells[0]["weighted_numerator_support_if_authorized"] = {"$exact_fraction": [1, 1]}
    topology["complete_cell_semantic_projection"] = cells
    with pytest.raises(FF01GenericIngressError, match="RAW weight"):
        _receive(query, _changed_result(result, target_topology=topology))


def test_ordered_scalar_components_only_not_implicit_repetition_collapse():
    _, _, _, query, result = _case()
    assert _receive(query, result).semantic_projection()["joint_order_semantics"] == "SEMANTIC_ORDERED"
    assert tuple(ref["object_id"] for ref in _receive(query, result).semantic_projection()["target_refs"]) == tuple(
        ref["object_id"] for ref in query.target_refs
    )
