"""Real one-I03→S04→FF01 with context batch, unary and cold replay."""
from dataclasses import replace

import pytest

import rawlsing_next.pre553_s04_first_consumer as service
from rawlsing_next.field_forge_generic_empirical_ingress import (
    FF01GenericIngressError, receive_ff01_observed_joint,
)
from rawlsing_next.pre553_s04_cold_custody import (
    S04ExternalRootPin, freeze_s04_i03_sourcefree, read_s04_cold_preimages,
)
from rawlsing_next.pre553_s04_research_batch import S04ContextRequest
from rawlsing_next.tests import test_pre553_empirical_query as native
from rawlsing_next.tests.test_pyat1009_ff01_generic_ingress import _case


def test_one_real_i03_call_always_precedes_s04_and_value_fed_ff01(monkeypatch):
    source, qa, predicate, query, previously = _case(tag="S04-SINGLE-EXECUTION")
    original_execute = service.execute_empirical_query
    calls = []

    def trace(**kw):
        calls.append(kw["query"].ref)
        return original_execute(**kw)

    monkeypatch.setattr(service, "execute_empirical_query", trace)
    delivered = service.execute_s04_first_consumer_once(
        repository=source["repo"],
        query=query, predicate=predicate,
        authority_registry=native._registry(source, qa),
        release_refs=(source["release_ref"],),
        conditioner_index=0,
        context_requests=(
            S04ContextRequest(2, {0: "0", 1: "0"}),
            S04ContextRequest(2, {0: "0", 1: "0"}),
            S04ContextRequest(2, {0: "1", 1: "0"}),
        ),
    )
    assert len(calls) == 1
    assert delivered.execution.facts[0].ref == previously.facts[0].ref
    assert delivered.knowledge.material()["fact_ref"] == previously.facts[0].ref.as_dict()
    assert delivered.ff01.semantic_projection()["producer_fact_ref"] == previously.facts[0].ref.as_dict()
    assert delivered.receipt.material()["batch_research_ref"] == delivered.batch.ref.as_dict()
    assert delivered.batch.material()["distinct_contextual_computations"] == 2
    oracle = receive_ff01_observed_joint(
        query=query, execution=previously,
        conditioner_index=0, producer_permission_ceiling=("FF01_DESCRIPTIVE_SOURCEFREE",),
    )
    assert delivered.ff01.ref == oracle.ref


def test_existing_i03_result_can_be_received_without_any_second_execute(monkeypatch):
    _, _, _, q, previous = _case(tag="S04-REUSE-ORIGINAL")
    def forbidden(**_):
        raise AssertionError("no second I03 execution admitted")
    monkeypatch.setattr(service, "execute_empirical_query", forbidden)
    delivered = service.receive_s04_first_consumer(
        query=q, execution=previous, conditioner_index=2,
        context_requests=(S04ContextRequest(0, {2: "0"}),),
    )
    assert delivered.ff01.semantic_projection()["conditioner_ref"] == q.target_refs[2]
    assert delivered.receipt.material()["producer_operation"].startswith("ONE_PREEXISTING")


def test_native_unary_f1_can_be_published_without_forced_ff01():
    from itertools import product
    rows = [
        {"id": f"R{x}{y}", "responses": {"X": x, "Y": y, "Z": x ^ y}}
        for x, y in product((0, 1), repeat=2)
    ]
    source = native._build_source(
        "S04-UNARY-INDEPENDENT", rows, question_namespace="S04-UNARY",
    )
    qa = native._query_authority("S04-UNARY-INDEPENDENT")
    predicate = native._branch_predicate(source, qa)
    query = native._query(source, qa, predicate, ("X",), tag="unary")
    result = native._run(source, qa, predicate, query)
    publication = service.receive_s04_first_consumer(query=query, execution=result)
    assert publication.knowledge.material()["target_arity"] == 1
    assert publication.ff01 is None
    assert publication.receipt.material()["consumer_status"] == "UPSTREAM_S04_ONLY"


def test_held_positive_counts_survive_first_consumer_as_typed_not_accepted():
    from rawlsing_next.pre553_empirical_objects import EmpiricalFact
    _, _, _, q, result = _case(tag="S04-ONEPASS-HELD")
    original = result.facts[0]
    held = EmpiricalFact(
        typed_state="LOW_SUPPORT",
        authority_snapshot_refs=original.authority_snapshot_refs,
        dependency_refs=original.dependency_refs,
        producer_replay_locator_or_reference_root=original.producer_replay_locator_or_reference_root,
        **dict(original.semantic_fields),
    )
    delivered = service.receive_s04_first_consumer(
        query=q, execution=replace(result, facts=(held,)),
        conditioner_index=0,
    )
    assert delivered.ff01.semantic_projection()["producer_state"] == "LOW_SUPPORT"
    assert delivered.ff01.semantic_projection()["complete_cells"] == []
    assert delivered.receipt.material()["population_rank_or_uncertainty"] is None


def test_improper_permission_widen_refuses_at_real_first_consumer():
    _, _, _, q, result = _case(tag="S04-ONEPASS-RIGHTS")
    with pytest.raises(FF01GenericIngressError, match="protected use|widen"):
        service.receive_s04_first_consumer(
            query=q, execution=result, conditioner_index=0,
            producer_permission_ceiling=("STRONG_CAUSAL",),
        )


def test_rehydrated_sourcefree_cold_preimages_enter_first_consumer_without_c11():
    _, _, _, query, result = _case(tag="S04-ONEPASS-COLD")
    original = service.receive_s04_first_consumer(
        query=query, execution=result, conditioner_index=0,
    )
    archive = freeze_s04_i03_sourcefree(
        query=query, execution=result, knowledge=original.knowledge,
    )
    read = read_s04_cold_preimages(
        archive, external_root=S04ExternalRootPin(
            query.ref, result.facts[0].ref, result.release_refs[0],
        ),
    )
    restored = service.receive_s04_first_consumer(
        query=read.query, execution=read.execution, conditioner_index=0,
    )
    assert restored.knowledge.ref == original.knowledge.ref
    assert restored.ff01.ref == original.ff01.ref
    assert restored.receipt.ref == original.receipt.ref
