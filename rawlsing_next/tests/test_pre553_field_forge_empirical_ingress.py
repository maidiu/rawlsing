"""Focused ingress tests: current empirical fact -> existing FIELD FORGE owner."""
from __future__ import annotations

from dataclasses import replace

from rawlsing_next.pre553_empirical_objects import EmpiricalFact, ExactRef
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_field_forge_empirical_ingress import (
    BRIDGE_REFUSED,
    REFUSAL_RELATION,
    REFUSAL_TWO_TARGET_REQUIRED,
    STATE_CONDITIONAL_SUPPORT,
    STATE_TYPED_REFUSAL,
    ingest_empirical_fact,
)
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_possibility_provider import (
    provide_empirical_possibility_slice,
)
from rawlsing_next.tests import c1_03_join_fixture as jf
from rawlsing_next.tests.c1_at08_at13_fixture import make_model_rule, xor_fixture
from rawlsing_next.tests.test_field_forge_conditional_support import _fixture
from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate,
    _build_source,
    _predicate,
    _query,
    _query_authority,
    _response_leaf,
)


def _fact_variant(
    fact: EmpiricalFact,
    *,
    cells=None,
    numerator=None,
    denominator=None,
    weighted_numerator=None,
    provenance=None,
    query_ref=None,
) -> EmpiricalFact:
    topology = dict(fact.target_topology)
    if cells is not None:
        topology["complete_cell_semantic_projection"] = cells
    deps = set(fact.dependency_refs)
    if provenance is not None:
        deps.update(provenance)
    return EmpiricalFact(
        typed_state=fact.typed_state,
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=tuple(sorted(deps, key=lambda r: r.key)),
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
        empirical_query_spec_ref=(fact.empirical_query_spec_ref if query_ref is None else query_ref),
        empirical_universe_refs=fact.empirical_universe_refs,
        target_topology=topology,
        condition_predicate_ref=fact.condition_predicate_ref,
        risk_set_ref=fact.risk_set_ref,
        raw_numerator_support=fact.raw_numerator_support if numerator is None else numerator,
        raw_denominator_support=fact.raw_denominator_support if denominator is None else denominator,
        weighted_numerator_support_if_authorized=weighted_numerator,
        weighted_denominator_support_if_authorized=None,
        measure_basis_ref=fact.measure_basis_ref,
        response_state_semantics_ref=fact.response_state_semantics_ref,
        uncertainty_method_or_typed_state=fact.uncertainty_method_or_typed_state,
        source_empirical_provenance_refs=fact.source_empirical_provenance_refs if provenance is None else provenance,
        replay_ref=fact.replay_ref,
        query_execution_contract_id=fact.query_execution_contract_id,
        execution_detail=fact.execution_detail,
        source_scope_mode=fact.source_scope_mode,
        measure_kind=fact.measure_kind,
        risk_set_type=fact.risk_set_type,
        target_domain_identity=fact.target_domain_identity,
        raw_resolved_target_support=(
            fact.raw_resolved_target_support if numerator is None else numerator
        ),
    )


def _base():
    query, fact, conditioner, target = _fixture()
    return query, fact, conditioner, target


def test_exact_two_target_fact_reaches_existing_ff_profile_with_no_structural_grant():
    query, fact, conditioner, target = _base()
    out = ingest_empirical_fact(fact=fact, query=query, conditioner_ref=conditioner, target_ref=target)
    assert out.state == STATE_CONDITIONAL_SUPPORT
    assert out.relation is not None
    assert out.refusal_code == ""
    assert out.structural_grant is False
    assert out.structural_state.startswith("WITHHELD")
    assert out.bridge_state == BRIDGE_REFUSED  # fixture scope is not exact frozen GT2 canary
    assert out.bridge_refusal
    rows = out.relation.conditional_count_profile
    assert [row["condition_denominator_support"] for row in rows] == [3, 3, 0]
    assert rows[0]["target_counts"][0]["joint_support_count"] == 2
    assert rows[0]["target_counts"][1]["joint_support_count"] == 1
    assert rows[0]["target_counts"][2]["joint_support_count"] == 0
    assert rows[0]["target_counts"][2]["cell_state"] == "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"


def test_changed_counts_and_denominator_change_actual_support_profile():
    query, fact, conditioner, target = _base()
    cells = [dict(cell) for cell in fact.target_topology["complete_cell_semantic_projection"]]
    for cell in cells:
        if cell["cell"] == ["0", "1"]:
            cell["raw_numerator_support"] = 3
    changed = _fact_variant(fact, cells=cells, numerator=fact.raw_numerator_support + 1,
                            denominator=fact.raw_denominator_support + 1)
    out = ingest_empirical_fact(fact=changed, query=query, conditioner_ref=conditioner, target_ref=target)
    assert out.state == STATE_CONDITIONAL_SUPPORT
    rows = out.relation.conditional_count_profile
    assert [row["condition_denominator_support"] for row in rows] == [4, 3, 0]
    assert rows[0]["target_counts"][0]["joint_support_count"] == 3
    assert out.relation.ref != _fixture()[1].ref


def test_source_edition_or_provenance_change_changes_relation_identity_not_counts():
    query, fact, conditioner, target = _base()
    first = ingest_empirical_fact(fact=fact, query=query, conditioner_ref=conditioner, target_ref=target)
    changed_provenance = (ExactRef("SOURCE_EDITION", "urn:test:source:edition-b", "a" * 64),)
    changed = _fact_variant(fact, provenance=changed_provenance)
    second = ingest_empirical_fact(fact=changed, query=query, conditioner_ref=conditioner, target_ref=target)
    assert second.state == STATE_CONDITIONAL_SUPPORT
    assert first.relation.ref != second.relation.ref
    assert first.relation.conditional_count_profile == second.relation.conditional_count_profile


def test_reversed_conditional_role_is_typed_refusal():
    query, fact, conditioner, target = _fixture(reverse_targets=True)
    out = ingest_empirical_fact(
        fact=fact, query=query, conditioner_ref=conditioner, target_ref=target
    )
    assert out.state == STATE_TYPED_REFUSAL
    assert out.refusal_code == REFUSAL_RELATION
    assert "role/order" in out.refusal_detail
    assert out.structural_grant is False


def test_three_plus_joint_is_typed_refusal_not_invented_conditional_support():
    query, fact, conditioner, target = _base()
    topology = dict(query.target_arity_and_topology)
    topology["arity"] = 3
    topology["components"] = [*topology["components"], dict(topology["components"][-1])]
    from rawlsing_next.pre553_empirical_objects import EmpiricalQuerySpec

    fields = dict(query.semantic_fields)
    fields["target_arity_and_topology"] = topology
    changed_query = EmpiricalQuerySpec(
        typed_state=query.typed_state,
        authority_snapshot_refs=query.authority_snapshot_refs,
        dependency_refs=query.dependency_refs,
        producer_replay_locator_or_reference_root=(
            query.producer_replay_locator_or_reference_root
        ),
        **fields,
    )
    out = ingest_empirical_fact(
        fact=_fact_variant(fact, query_ref=changed_query.ref),
        query=changed_query,
    )
    assert out.state == STATE_TYPED_REFUSAL
    assert out.refusal_code == REFUSAL_TWO_TARGET_REQUIRED
    assert out.relation is None


def test_missing_joint_cell_is_typed_refusal():
    query, fact, conditioner, target = _base()
    cells = [dict(cell) for cell in fact.target_topology["complete_cell_semantic_projection"]][:-1]
    out = ingest_empirical_fact(fact=_fact_variant(fact, cells=cells), query=query,
                                conditioner_ref=conditioner, target_ref=target)
    assert out.state == STATE_TYPED_REFUSAL
    assert out.refusal_code == REFUSAL_RELATION
    assert "complete native" in out.refusal_detail


def test_raw_weight_change_is_typed_refusal():
    query, fact, conditioner, target = _base()
    out = ingest_empirical_fact(
        fact=_fact_variant(fact, weighted_numerator=fact.raw_numerator_support),
        query=query, conditioner_ref=conditioner, target_ref=target,
    )
    assert out.state == STATE_TYPED_REFUSAL
    assert out.refusal_code == REFUSAL_RELATION
    assert "weighted numerator" in out.refusal_detail


def test_current_i03_produced_one_target_fact_enters_ingress_and_refuses_ff_arity():
    rows = [
        {
            "id": f"R{i:03d}",
            "responses": {
                "POSITION": "P1" if i <= 6 else "P2",
                "ANSWER": "1" if i <= 4 else "0",
            },
        }
        for i in range(1, 11)
    ]
    source = _build_source(
        "ingress-i03",
        rows,
        risk_sets={
            "R": {
                "POSITION": {row["id"] for row in rows},
                "ANSWER": {row["id"] for row in rows},
            }
        },
    )
    qauth = _query_authority("ingress-i03")
    predicate = _predicate(
        source, qauth, _response_leaf(source, qauth, "POSITION", "P1"),
        tag="ingress-i03",
    )
    query = _query(source, qauth, predicate, ("ANSWER",), risk="R", tag="ingress-i03")
    registry = AuthorityRegistry((*source["authorities"], qauth))
    result = execute_empirical_query(
        repository=source["repo"],
        query=query,
        predicate=predicate,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
    )
    assert len(result.facts) == 1
    fact = result.facts[0]
    out = ingest_empirical_fact(fact=fact, query=query)
    assert out.state == STATE_TYPED_REFUSAL
    assert out.refusal_code == REFUSAL_TWO_TARGET_REQUIRED
    assert out.fact_ref == fact.ref
    assert out.query_ref == query.ref


def test_current_n10e_provider_fact_reaches_ingress_and_ff_arity_refusal():
    built = jf.a_forward_composition()
    provider = provide_empirical_possibility_slice(
        repository=built["source"]["repo"],
        empirical_query=built["query"],
        predicate=built["predicate"],
        authority_registry=built["registry"],
        release_refs=(built["source"]["release_ref"],),
        consumer_query=built["consumer_query"],
        model_rule=make_model_rule(built["source"]["universe"].ref, "ingress-n10e"),
        condition_binding_witness=built["witness"],
    )
    assert provider.provider_state == "EXACT_SUPPORTED_SLICE_PRODUCED"
    composition = provider.composition_result
    assert composition.producer_result is not None
    fact = composition.producer_result.facts[0]
    out = ingest_empirical_fact(fact=fact, query=built["query"])
    assert out.state == STATE_TYPED_REFUSAL
    assert out.refusal_code == REFUSAL_TWO_TARGET_REQUIRED
    assert out.fact_ref == fact.ref
    assert out.query_ref == built["query"].ref


def test_exact_dependency_sever_red_then_restore_same_relation():
    query, fact, conditioner, target = _base()
    first = ingest_empirical_fact(fact=fact, query=query, conditioner_ref=conditioner, target_ref=target)
    assert first.state == STATE_CONDITIONAL_SUPPORT
    cells = [dict(cell) for cell in fact.target_topology["complete_cell_semantic_projection"]][:-1]
    severed = ingest_empirical_fact(
        fact=_fact_variant(fact, cells=cells), query=query,
        conditioner_ref=conditioner, target_ref=target,
    )
    assert severed.state == STATE_TYPED_REFUSAL
    assert severed.refusal_code == REFUSAL_RELATION
    restored = ingest_empirical_fact(fact=fact, query=query, conditioner_ref=conditioner, target_ref=target)
    assert restored.state == STATE_CONDITIONAL_SUPPORT
    assert restored.relation.ref == first.relation.ref


def test_current_i03_three_target_joint_reaches_ingress_and_refuses_two_target_owner():
    source = xor_fixture("ingress-3target")
    qauth = _query_authority("ingress-3target")
    predicate = _branch_predicate(source, qauth, tag="ingress-3target")
    query = _query(source, qauth, predicate, ("A", "B", "C"), tag="ingress-3target")
    registry = AuthorityRegistry((*source["authorities"], qauth))
    result = execute_empirical_query(
        repository=source["repo"], query=query, predicate=predicate,
        authority_registry=registry, release_refs=(source["release_ref"],),
    )
    assert query.target_arity_and_topology["arity"] == 3
    assert len(result.facts) == 1
    fact = result.facts[0]
    out = ingest_empirical_fact(fact=fact, query=query)
    assert out.state == STATE_TYPED_REFUSAL
    assert out.refusal_code == REFUSAL_TWO_TARGET_REQUIRED
    assert out.fact_ref == fact.ref
