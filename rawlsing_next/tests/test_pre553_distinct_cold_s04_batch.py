"""Adversarial proof: DISTINCT native I03 in ONE cold index -> distinct S04 products.

Sourcefree test fixtures only. An SRC16 original-source C11 construction grant
is not an I03 analysis grant; this adapter admits only VerifiedDirectEstate
and delegates all query authority to the existing original runtime catalog.
"""
from dataclasses import replace
from pathlib import Path

import pytest

pytest.importorskip("pyarrow")

import rawlsing_next.pre553_distinct_cold_s04_batch as subject
from rawlsing_next.pre553_carrier_execution import (
    CarrierNeutralResearchExecutor, RuntimeObjectCatalog,
)
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_source_direct_parquet_estate import DirectEstateError
from rawlsing_next.field_forge_generic_empirical_ingress import (
    FF01GenericIngressError, receive_ff01_observed_joint,
)
from rawlsing_next.pre553_s04_research_batch import S04ContextRequest
from rawlsing_next.tests.test_pre553_distinct_cold_i03_batch import _case
from rawlsing_next.tests import test_pre553_empirical_query as native


@pytest.mark.parametrize("distinct", (1, 10, 100))
def test_distinct_queries_run_one_native_index_and_produce_each_real_s04(
    tmp_path, monkeypatch, distinct,
):
    source, qa, predicate, queries, executor, original, root = _case(
        tmp_path, monkeypatch, distinct, name=f"S04-NATIVE-DISTINCT-{distinct}",
    )
    entered = []
    enter = DirectEstateI03Session.__enter__

    def counted(self):
        entered.append(self.estate.i02.release)
        return enter(self)

    requests = tuple(
        subject.S04DistinctOperation(q.ref, predicate.ref) for q in queries
    )
    with monkeypatch.context() as patch:
        patch.setattr(DirectEstateI03Session, "__enter__", counted)
        result = subject.execute_distinct_native_s04_research(
            executor=executor, operations=requests,
        )
    assert len(entered) == 1
    assert result.original_i03_batch.prepared_session_count == 1
    assert len(result.first_consumers) == distinct
    grade = result.receipt.material()
    assert grade["distinct_original_i03_operations"] == distinct
    assert grade["prepared_postings_sessions"] == 1
    assert grade["distinct_source_risks_kept_separate"] is True
    assert grade["one_existing_native_source_release_ref"] == source["release_ref"].as_dict()
    assert len(grade["ordered_research_products"]) == distinct
    assert all(item["ff01_ref"] is None for item in grade["ordered_research_products"])
    assert all(
        item["s04_knowledge_ref"] == product.knowledge.ref.as_dict()
        for item, product in zip(grade["ordered_research_products"], result.first_consumers)
    )
    assert all(product.ff01 is None for product in result.first_consumers)
    assert all(product.knowledge.material()["target_arity"] == 1
               for product in result.first_consumers)
    assert all(
        product.knowledge.material()["fact_ref"] == actual.facts[0].ref.as_dict()
        for product, actual in zip(result.first_consumers, result.original_i03_batch.results)
    )
    assert not list(Path(root).glob(".s2c-native-i03-*"))


def _mixed(tmp_path, monkeypatch, *, current=None, tag="S04-COLD-FF-JOINED"):
    source, qa, predicate, queries, executor, original, root = _case(
        tmp_path, monkeypatch, 2, current=current, name=tag,
    )
    pair = native._query(
        source, qa, predicate, ("Q000", "Q001"), tag="pair-actual-native",
    )
    catalog = RuntimeObjectCatalog(
        authorities=executor.runtime_catalog.authorities,
        predicates=executor.runtime_catalog.predicates,
        queries=(pair, queries[0]),
        discovery_authorities=(),
    )
    reused = CarrierNeutralResearchExecutor(
        repository=executor.repository,
        release_refs=executor.release_refs,
        runtime_catalog=catalog,
    )
    instructions = (
        subject.S04DistinctOperation(
            pair.ref, predicate.ref,
            conditioner_index=0,
            context_requests=(
                S04ContextRequest(target_index=1, conditions={0: "0"}),
                S04ContextRequest(target_index=1, conditions={0: "0"}),
            ),
        ),
        subject.S04DistinctOperation(queries[0].ref, predicate.ref),
    )
    return source, qa, predicate, pair, queries[0], reused, instructions, root


def test_one_preparation_feeds_real_k2_s04_ff01_and_unary_native_f1(
    tmp_path, monkeypatch,
):
    source, qa, predicate, pair, scalar, executor, instructions, root = _mixed(
        tmp_path, monkeypatch,
    )
    entered = []
    original_enter = DirectEstateI03Session.__enter__

    def capture(self):
        entered.append(True)
        return original_enter(self)

    with monkeypatch.context() as patch:
        patch.setattr(DirectEstateI03Session, "__enter__", capture)
        result = subject.execute_distinct_native_s04_research(
            executor=executor, operations=instructions,
        )
    assert len(entered) == 1
    assert result.first_consumers[0].knowledge.material()["target_arity"] == 2
    assert result.first_consumers[1].knowledge.material()["target_arity"] == 1
    assert result.first_consumers[0].ff01 is not None
    assert result.first_consumers[1].ff01 is None
    assert result.first_consumers[0].batch.material()["distinct_contextual_computations"] == 1
    assert result.receipt.material()["ordered_research_products"][0][
        "first_consumer_status"
    ] == "S04_TO_FF01_WITH_CONTEXT_BATCH"
    # Independently compute the accepted direct FF01 oracle, including all
    # source/risk/respondent totals; don't accept solely self-consistent S04.
    independent_i03 = native._run(source, qa, predicate, pair)
    oracle = receive_ff01_observed_joint(
        query=pair, execution=independent_i03, conditioner_index=0,
        producer_permission_ceiling=("FF01_DESCRIPTIVE_SOURCEFREE",),
    )
    assert result.first_consumers[0].ff01.ref == oracle.ref
    assert result.original_i03_batch.results[0].facts[0].ref == independent_i03.facts[0].ref
    assert not list(Path(root).glob(".s2c-native-i03-*"))


def test_source_revoked_during_s04_reception_returns_no_partial_batch(
    tmp_path, monkeypatch,
):
    permitted = {"yes": True}
    source, qa, predicate, q0, q1, executor, instructions, root = _mixed(
        tmp_path, monkeypatch,
        current=lambda _: permitted["yes"], tag="S04-REVOKE-DURING-CONSUMER",
    )
    original_receive = subject.receive_s04_first_consumer
    count = {"n": 0}

    def withdraw_after_one(**kwargs):
        result = original_receive(**kwargs)
        count["n"] += 1
        if count["n"] == 1:
            permitted["yes"] = False
        return result

    with monkeypatch.context() as patch:
        patch.setattr(subject, "receive_s04_first_consumer", withdraw_after_one)
        with pytest.raises(DirectEstateError, match="current source"):
            subject.execute_distinct_native_s04_research(
                executor=executor, operations=instructions,
            )
    assert count["n"] == 1
    assert not list(Path(root).glob(".s2c-native-i03-*"))


def test_duplicate_wrong_predicate_unary_ff01_and_causal_text_refuse_before_index(
    tmp_path, monkeypatch,
):
    source, qa, predicate, q0, q1, executor, instructions, root = _mixed(
        tmp_path, monkeypatch, tag="S04-PREFLIGHT-REFUSE",
    )
    entered = []
    original_enter = DirectEstateI03Session.__enter__

    def detect(self):
        entered.append(True)
        return original_enter(self)

    with monkeypatch.context() as patch:
        patch.setattr(DirectEstateI03Session, "__enter__", detect)
        with pytest.raises(subject.S04DistinctBatchError, match="duplicate"):
            subject.execute_distinct_native_s04_research(
                executor=executor,
                operations=(instructions[0], instructions[0]),
            )
        with pytest.raises(subject.S04DistinctBatchError, match="genuine k>=2"):
            subject.execute_distinct_native_s04_research(
                executor=executor,
                operations=(replace(instructions[1], conditioner_index=0),),
            )
        with pytest.raises(FF01GenericIngressError, match="protected use"):
            subject.execute_distinct_native_s04_research(
                executor=executor,
                operations=(replace(
                    instructions[0],
                    producer_permission_ceiling=("STRONG_CAUSAL",),
                ),),
            )
        with pytest.raises(subject.S04DistinctBatchError, match="context axes"):
            subject.execute_distinct_native_s04_research(
                executor=executor,
                operations=(replace(
                    instructions[0],
                    context_requests=(S04ContextRequest(1, {1: "0"}),),
                ),),
            )
    assert entered == []  # invalid authority/meaning never pays for source read


def test_original_construction_grant_is_not_a_qualified_i03_repository():
    # In Codex 00ebc4a16, SRC16 is a C11-construction-only source decision,
    # not a VerifiedDirectEstate or an I03 analysis authorization.
    with pytest.raises(subject.S04DistinctBatchError, match="CarrierNeutralResearchExecutor"):
        subject.execute_distinct_native_s04_research(
            executor={"source_id": "SRC16", "purpose": "FULL_SRC16_ORIGINAL_C11_CONSTRUCTION_ONLY"},
            operations=(subject.S04DistinctOperation(
                query_ref=object(), predicate_ref=object(),
            ),),
        )
