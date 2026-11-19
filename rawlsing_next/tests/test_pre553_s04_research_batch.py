"""S04 one-producer 1/10/100 query reuse, exact source and held science."""
from dataclasses import replace

import pytest

from rawlsing_next.pre553_empirical_objects import (
    EmpiricalFact, canonical_json, semantic_hash,
)
from rawlsing_next.pre553_s04_cold_custody import (
    S04ExternalRootPin, freeze_s04_i03_sourcefree, read_s04_cold_preimages,
)
from rawlsing_next.pre553_s04_observed_research import receive_s04_i03_research
from rawlsing_next.pre553_s04_research_batch import (
    MAX_REQUESTS, S04BatchError, S04ContextRequest, run_s04_context_batch,
)
from rawlsing_next.tests.test_pyat1009_ff01_generic_ingress import _case


def _fixture():
    _, _, _, query, result = _case(tag="S04-BATCH-ONE-JOINT")
    s04 = receive_s04_i03_research(query=query, execution=result)
    return query, result, s04


@pytest.mark.parametrize("asked,expected_compute", [
    (1, 1), (10, 2), (100, 2),
])
def test_1_10_100_sourcefree_repeated_requests_share_one_native_i03(
    monkeypatch, asked, expected_compute,
):
    import rawlsing_next.pre553_s04_research_batch as mod
    query, result, knowledge = _fixture()
    original = mod.ask_s04_exact_condition
    calls = []

    def trace(*, knowledge, target_index, conditions):
        calls.append((target_index, canonical_json(conditions)))
        return original(knowledge=knowledge, target_index=target_index, conditions=conditions)

    monkeypatch.setattr(mod, "ask_s04_exact_condition", trace)
    requests = [
        S04ContextRequest(
            target_index=2, conditions={0: "0" if i % 2 == 0 else "1"}
        ) for i in range(asked)
    ]
    receipt, outputs = run_s04_context_batch(
        knowledge=knowledge, requests=requests,
    )
    m = receipt.material()
    assert len(calls) == expected_compute
    assert m["requests_total"] == asked
    assert m["distinct_contextual_computations"] == expected_compute
    assert m["reused_exact_requests"] == asked - expected_compute
    assert len(outputs) == asked
    assert m["source_fact_ref"] == result.facts[0].ref.as_dict()
    assert m["source_release_ref"] == result.release_refs[0].as_dict()
    assert m["scientific_rank"] is None
    assert m["new_population_claim"] is None
    assert outputs[0].ref == outputs[-1].ref if asked % 2 else outputs[0].ref != outputs[-1].ref


def test_order_of_context_keys_does_not_recompute_or_change_exact_receipt():
    _, _, knowledge = _fixture()
    a = S04ContextRequest(2, {0: "0", 1: "1"})
    b = S04ContextRequest(2, {1: "1", 0: "0"})
    receipt, outputs = run_s04_context_batch(knowledge=knowledge, requests=(a, b))
    assert outputs[0].ref == outputs[1].ref
    assert receipt.material()["distinct_contextual_computations"] == 1
    assert receipt.material()["ordered_research"][1]["cache_reused"]


def test_bad_target_state_and_bool_axis_fail_closed_no_fabricated_zero():
    _, _, knowledge = _fixture()
    with pytest.raises((ValueError, S04BatchError), match="domain"):
        run_s04_context_batch(
            knowledge=knowledge,
            requests=(S04ContextRequest(2, {0: "UNADMINISTERED"}),),
        )
    with pytest.raises(S04BatchError, match="exact integer"):
        run_s04_context_batch(
            knowledge=knowledge,
            requests=(S04ContextRequest(2, {True: "0"}),),
        )
    with pytest.raises((ValueError, S04BatchError), match="leakage"):
        run_s04_context_batch(
            knowledge=knowledge,
            requests=(S04ContextRequest(2, {2: "0"}),),
        )


def test_batch_rejects_zero_or_over_max_work_without_c11_requery():
    _, _, knowledge = _fixture()
    with pytest.raises(S04BatchError, match="1–100"):
        run_s04_context_batch(knowledge=knowledge, requests=())
    with pytest.raises(S04BatchError, match="1–100"):
        run_s04_context_batch(
            knowledge=knowledge,
            requests=tuple(S04ContextRequest(2, {0: "0"}) for _ in range(MAX_REQUESTS + 1)),
        )


def test_held_low_support_returns_typed_held_for_all_requests():
    q, result, _ = _fixture()
    orig = result.facts[0]
    low = EmpiricalFact(
        typed_state="LOW_SUPPORT",
        authority_snapshot_refs=orig.authority_snapshot_refs,
        dependency_refs=orig.dependency_refs,
        producer_replay_locator_or_reference_root=orig.producer_replay_locator_or_reference_root,
        **dict(orig.semantic_fields),
    )
    held = receive_s04_i03_research(query=q, execution=replace(result, facts=(low,)))
    receipt, answers = run_s04_context_batch(
        knowledge=held,
        requests=(S04ContextRequest(2, {0: "0"}), S04ContextRequest(2, {0: "1"})),
    )
    assert all(a.material()["state"] == "UPSTREAM_SCIENCE_OR_SOURCE_HELD" for a in answers)
    assert all(a.material()["raw_conditioned_full_case_n"] is None for a in answers)
    assert receipt.material()["new_population_claim"] is None


def test_cold_rehydrated_source_answers_identically_with_one_source_root():
    q, r, s04 = _fixture()
    bundle = freeze_s04_i03_sourcefree(query=q, execution=r, knowledge=s04)
    cold = read_s04_cold_preimages(
        bundle, external_root=S04ExternalRootPin(q.ref, r.facts[0].ref, r.release_refs[0]),
    )
    selections = (
        S04ContextRequest(2, {0: "0"}),
        S04ContextRequest(2, {0: "1"}),
        S04ContextRequest(2, {0: "0"}),
    )
    hot, outputs_hot = run_s04_context_batch(knowledge=s04, requests=selections)
    restored, outputs_cold = run_s04_context_batch(
        knowledge=cold.knowledge, requests=selections,
    )
    assert hot.ref == restored.ref
    assert [a.ref for a in outputs_hot] == [a.ref for a in outputs_cold]
