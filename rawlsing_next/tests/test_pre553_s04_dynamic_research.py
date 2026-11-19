"""Dynamic native sourcefree I03 -> S04 -> general joint research without 100 cap."""
from pathlib import Path

import pytest

pytest.importorskip("pyarrow")

from rawlsing_next.pre553_carrier_execution import CarrierExecutionBindingError
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_source_direct_parquet_estate import DirectEstateError
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_s04_dynamic_research import (
    S04DynamicQuestion, S04DynamicResearchSession, S04DynamicResearchError,
)
from rawlsing_next.pre553_s04_general_joint_algebra import S04Projection
from rawlsing_next.pre553_distinct_cold_s04_batch import SOURCEFREE_ONLY_ASSERTION
from rawlsing_next.tests.test_pre553_distinct_cold_i03_batch import _case


def _source(tmp_path, monkeypatch, size=2, *, current=None, tag="DYNAMIC-S04"):
    return _case(tmp_path, monkeypatch, size, current=current, name=tag)


def test_prepared_native_session_serves_distinct_original_questions_then_indefinite_joint_followups(
    tmp_path, monkeypatch,
):
    source, qa, pred, queries, executor, _, root = _source(
        tmp_path, monkeypatch, size=2,
    )
    entered = []
    original_enter = DirectEstateI03Session.__enter__

    def trace(self):
        entered.append(True)
        return original_enter(self)

    with monkeypatch.context() as patch:
        patch.setattr(DirectEstateI03Session, "__enter__", trace)
        with S04DynamicResearchSession(
            executor=executor,
            sourcefree_origin_assertion=SOURCEFREE_ONLY_ASSERTION,
        ) as dynamic:
            first = dynamic.ask(S04DynamicQuestion(queries[0].ref, pred.ref))
            assert first.original.execution.query_ref == queries[0].ref
            assert first.original.knowledge.material()["fact_ref"] == first.original.execution.facts[0].ref.as_dict()
            assert first.joint_workspace.query(
                S04Projection((0,), {})
            ).material()["raw_selected_full_case_n"] == 4
            # The second I03 operation is distinct, but shares one actual
            # physical postings preparation. The first joint remains useful.
            second = dynamic.ask(S04DynamicQuestion(queries[1].ref, pred.ref))
            assert second.original.knowledge.ref != first.original.knowledge.ref
            assert second.original.execution.facts[0].ref != first.original.execution.facts[0].ref
            assert dynamic.stats()["original_native_i03_queries_executed"] == 2
            assert dynamic.stats()["batch_cardinality_limit"] is None
            followups = (
                S04Projection((0,), {})
                for _ in range(257)
            )
            values = first.joint_workspace.query_many(followups)
            assert sum(
                result.material()["raw_selected_full_case_n"] == 4
                for result in values
            ) == 257
            assert first.joint_workspace.cache_stats()["stored_positive_joint_cells"] == 2
    assert len(entered) == 1
    assert not list(Path(root).glob(".s2c-native-i03-*"))


def test_native_catalog_query_count_above_one_hundred_has_no_query_quota(
    tmp_path, monkeypatch,
):
    _, _, pred, queries, executor, _, root = _source(
        tmp_path, monkeypatch, size=103, tag="DYNAMIC-103-ORIGINAL-QUESTIONS",
    )
    entered = []
    original_enter = DirectEstateI03Session.__enter__

    def trace(self):
        entered.append(True)
        return original_enter(self)

    with monkeypatch.context() as patch:
        patch.setattr(DirectEstateI03Session, "__enter__", trace)
        with S04DynamicResearchSession(
            executor=executor,
            sourcefree_origin_assertion=SOURCEFREE_ONLY_ASSERTION,
        ) as dynamic:
            dynamic_questions = (
                S04DynamicQuestion(query.ref, pred.ref)
                for query in queries
            )
            actual = list(dynamic.ask_many(dynamic_questions))
            assert len(actual) == 103
            assert [x.original.execution.query_ref for x in actual] == [
                query.ref for query in queries
            ]
            assert len({x.original.knowledge.ref.key for x in actual}) == 103
            assert dynamic.stats()["original_native_i03_queries_executed"] == 103
    assert len(entered) == 1
    assert not list(Path(root).glob(".s2c-native-i03-*"))


def test_current_revoked_between_dynamic_questions_refuses_stale_science(
    tmp_path, monkeypatch,
):
    current = {"yes": True}
    _, _, pred, queries, executor, _, root = _source(
        tmp_path, monkeypatch, size=2,
        current=lambda _: current["yes"], tag="DYNAMIC-REVOKED",
    )
    with S04DynamicResearchSession(
        executor=executor,
        sourcefree_origin_assertion=SOURCEFREE_ONLY_ASSERTION,
    ) as dynamic:
        first = dynamic.ask(S04DynamicQuestion(queries[0].ref, pred.ref))
        assert first.original.knowledge.material()["producer_typed_state"] == "SUPPORTED"
        current["yes"] = False
        with pytest.raises(DirectEstateError, match="current source"):
            dynamic.ask(S04DynamicQuestion(queries[1].ref, pred.ref))
        assert dynamic.stats()["original_native_i03_queries_executed"] == 1
    assert not list(Path(root).glob(".s2c-native-i03-*"))


def test_rejects_original_survey_construction_grant_and_bad_catalog_query(
    tmp_path, monkeypatch,
):
    _, _, pred, queries, executor, _, _ = _source(tmp_path, monkeypatch)
    with pytest.raises(S04DynamicResearchError, match="construction grants"):
        S04DynamicResearchSession(
            executor=executor,
            sourcefree_origin_assertion="SRC16_ORIGINAL_C11_CONSTRUCTION_ONLY",
        )
    dynamic = S04DynamicResearchSession(
        executor=executor,
        sourcefree_origin_assertion=SOURCEFREE_ONLY_ASSERTION,
    )
    with pytest.raises(S04DynamicResearchError, match="open verified"):
        dynamic.ask(S04DynamicQuestion(queries[0].ref, pred.ref))
    with dynamic:
        # Query issued by the original catalog must match its original
        # predicate; unissued query IDs and forged bindings are unavailable.
        foreign = ExactRef("EmpiricalQuerySpec@1.0.0", "urn:test:alien-query", semantic_hash("alien"))
        with pytest.raises(CarrierExecutionBindingError, match="unavailable"):
            dynamic.ask(S04DynamicQuestion(foreign, pred.ref))
