"""KUDA GF1: actual current native I03 -> S04 -> separate GF1 read, no rerun."""
from dataclasses import replace

import pytest

from rawlsing_next._gf1_candidate.s04_pair_support_bridge import (
    GF1S04FirstConsumerError, receive_gf1_pair_from_s04,
)
from rawlsing_next.pre553_s04_first_consumer import receive_s04_first_consumer
from rawlsing_next.tests import test_pre553_empirical_query as native


def _actual(mode):
    rows = (
        [{"id": "R00", "responses": {"X": 0, "Y": 0}},
         {"id": "R11", "responses": {"X": 1, "Y": 1}}]
        if mode == "diagonal" else
        [{"id": "R00", "responses": {"X": 0, "Y": 0}},
         {"id": "R01", "responses": {"X": 0, "Y": 1}},
         {"id": "R10", "responses": {"X": 1, "Y": 0}},
         {"id": "R11", "responses": {"X": 1, "Y": 1}}]
    )
    source = native._build_source(
        "kuda-s04-gf1-" + mode, rows, question_namespace="gf1-kuda-nonq86"
    )
    qa = native._query_authority("kuda-s04-gf1-" + mode)
    predicate = native._branch_predicate(source, qa)
    query = native._query(source, qa, predicate, ("X", "Y"), tag="kuda-" + mode)
    executed = native._run(source, qa, predicate, query)
    assert executed.facts[0].typed_state == "SUPPORTED"
    s04 = receive_s04_first_consumer(query=query, execution=executed)
    assert s04.ff01 is None
    return query, executed, s04


def test_actual_existing_i03_s04_to_nonq86_gf1_signature_no_second_query(monkeypatch):
    import rawlsing_next.pre553_empirical_query as original_i03
    def forbidden(*_a, **_k):
        raise AssertionError("GF1 cannot rerun an original I03")
    for mode, expected, total in (
        ("diagonal", "EXACT_PAIR_SEPARATION", 2),
        ("mixed", "NO_PAIR_SEPARATION", 4),
    ):
        query, execution, s04 = _actual(mode)
        with monkeypatch.context() as m:
            m.setattr(original_i03, "execute_empirical_query", forbidden)
            result = receive_gf1_pair_from_s04(s04=s04, query=query)
        assert result.signature["separation_class"] == expected
        assert result.signature["joint_support_total"] == total
        assert result.s04_knowledge_ref == s04.knowledge.ref
        assert result.source_fact_ref == execution.facts[0].ref
        assert result.source_query_ref == query.ref
        assert result.signature["generic_native_semantics_hold"] == "RETAINED"
        assert result.signature["production_owner_commit"] is False
        assert "Q86" not in result.relation.conditioner_source_native_variable


def test_s04_gf1_wrong_query_and_wrong_receipt_refuse_before_generic_value():
    q, executed, s04 = _actual("diagonal")
    alien_q, _, _ = _actual("mixed")
    with pytest.raises(GF1S04FirstConsumerError, match="native execution"):
        receive_gf1_pair_from_s04(s04=s04, query=alien_q)
    with pytest.raises(GF1S04FirstConsumerError, match="exact two-target native"):
        receive_gf1_pair_from_s04(
            s04=replace(s04, execution=replace(executed, facts=())),
            query=q,
        )
