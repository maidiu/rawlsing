"""S04 generality court: actual native k-way joint, not a 100-query showpiece.

The baseline is independently computed I03 sourcefree respondent records and
the prior S04 math; this tests arbitrary output/condition roles, zero/held
semantics, on-demand 257 requests and evidence reuse across *different*
questions. It does not claim original survey rights or a scientific rank.
"""
from dataclasses import replace

import pytest

from rawlsing_next.pre553_empirical_objects import (
    EmpiricalFact, canonical_json, semantic_hash,
)
from rawlsing_next.pre553_s04_observed_research import (
    S04ObservedKnowledge, ask_s04_exact_condition, receive_s04_i03_research,
)
from rawlsing_next.pre553_s04_general_joint_algebra import (
    S04GeneralAlgebraError, S04GeneralJointWorkspace, S04Projection,
)
from rawlsing_next.tests.test_pre553_s04_observed_research import _real


def _ready(*, parity=0, tag="S04-GENERAL-JOINT"):
    _, _, _, query, execution = _real(parity, tag=tag)
    knowledge = receive_s04_i03_research(query=query, execution=execution)
    return query, execution, knowledge, S04GeneralJointWorkspace(
        knowledge=knowledge, expected_knowledge_ref=knowledge.ref,
    )


def _counts(answer):
    return {
        tuple(c["output_states"]): c["raw_count"]
        for c in answer.material()["complete_output_cells"]
    }


def test_all_single_axis_conditionals_match_original_s04_over_native_xor_joint():
    _, _, knowledge, workspace = _ready()
    for target in range(3):
        for axis in range(3):
            if target == axis:
                continue
            for value in ("0", "1"):
                original = ask_s04_exact_condition(
                    knowledge=knowledge,
                    target_index=target, conditions={axis: value},
                ).material()
                general = workspace.query(
                    S04Projection((target,), {axis: value})
                ).material()
                assert general["raw_selected_full_case_n"] == original[
                    "raw_conditioned_full_case_n"
                ]
                assert {
                    cell["output_states"][0]: cell["raw_count"]
                    for cell in general["complete_output_cells"]
                } == {
                    cell["target_state"]: cell["raw_count"]
                    for cell in original["complete_target_cells"]
                }
                assert general["source_fact_ref"] == original["source_fact_ref"]
    assert workspace.cache_stats()["filter_cache_hits"] > 0


def test_arbitrary_true_multidimensional_projection_and_inverse_conditioning():
    _, _, knowledge, workspace = _ready()
    joint = workspace.query(S04Projection((1, 2), {0: "0"}))
    assert joint.material()["raw_selected_full_case_n"] == 2
    assert _counts(joint) == {
        ("0", "0"): 1, ("0", "1"): 0,
        ("1", "0"): 0, ("1", "1"): 1,
    }
    inverse = workspace.query(S04Projection((0, 1), {2: "0"}))
    assert inverse.material()["raw_selected_full_case_n"] == 2
    assert _counts(inverse) == {
        ("0", "0"): 1, ("0", "1"): 0,
        ("1", "0"): 0, ("1", "1"): 1,
    }
    unconditioned = workspace.query(S04Projection((2, 1, 0), {}))
    assert unconditioned.material()["raw_selected_full_case_n"] == 4
    assert len(unconditioned.material()["complete_output_cells"]) == 8
    assert sum(_counts(unconditioned).values()) == 4
    assert unconditioned.material()["comparative_predictor_rank"] is None
    assert unconditioned.material()["population_variance_or_causal_estimate"] is None


def test_different_research_questions_share_real_condition_intersections():
    _, _, _, workspace = _ready()
    a = workspace.query(S04Projection((1,), {0: "0"}))
    before = workspace.cache_stats().copy()
    b = workspace.query(S04Projection((1, 2), {0: "0"}))
    after = workspace.cache_stats()
    assert a.ref != b.ref
    assert after["filter_cache_hits"] > before["filter_cache_hits"]
    assert after["intersection_steps"] == before["intersection_steps"]
    assert after["cached_intersections"] >= 1


def test_query_stream_has_no_100_request_semantic_ceiling_or_result_repository():
    _, _, _, workspace = _ready()
    # These are genuine dynamic source-conditioned questions, not an
    # enumeration of synthetic pseudo-respondents or 257 prewritten queries.
    def workload():
        for i in range(257):
            target = i % 3
            yield S04Projection((target,), {(target + 1) % 3: str(i % 2)})
    results = workspace.query_many(workload())
    received = 0
    for result in results:
        received += 1
        assert result.material()["raw_selected_full_case_n"] == 2
    assert received == 257
    assert workspace.cache_stats()["filter_cache_hits"] > 0


def test_dynamic_branching_can_ask_followup_without_source_reexecution():
    _, _, knowledge, workspace = _ready()
    first = workspace.query(S04Projection((0,), {}))
    chosen = max(
        first.material()["complete_output_cells"],
        key=lambda row: row["raw_count"],
    )["output_states"][0]
    second = workspace.query(S04Projection((1, 2), {0: chosen}))
    assert second.material()["raw_selected_full_case_n"] == 2
    assert second.material()["source_fact_ref"] == knowledge.material()["fact_ref"]
    assert second.material()["no_second_i03_or_source_query"] is True


def test_absent_full_case_condition_is_zero_not_fake_probability():
    _, _, _, workspace = _ready()
    absent = workspace.query(S04Projection((), {0: "0", 1: "0", 2: "1"}))
    payload = absent.material()
    assert payload["state"] == "ZERO_WITHIN_RESOLVED_FULL_CASES"
    assert payload["raw_selected_full_case_n"] == 0
    assert payload["complete_output_cells"] == [{
        "output_states": [],
        "raw_count": 0,
        "raw_fraction_of_selected_full_cases": None,
        "cell_state": "ZERO_WITHIN_RESOLVED_FULL_CASES",
    }]
    present = workspace.query(S04Projection((), {0: "0", 1: "0", 2: "0"}))
    assert present.material()["raw_selected_full_case_n"] == 1
    assert present.material()["complete_output_cells"][0][
        "raw_fraction_of_selected_full_cases"
    ] == {"$exact_fraction": [1, 1]}


def test_held_incomplete_native_fact_does_not_become_an_observed_distribution():
    query, execution, _, _ = _ready()
    fact = execution.facts[0]
    low = EmpiricalFact(
        typed_state="LOW_SUPPORT",
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=fact.dependency_refs,
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
        **dict(fact.semantic_fields),
    )
    held = receive_s04_i03_research(query=query, execution=replace(execution, facts=(low,)))
    workspace = S04GeneralJointWorkspace(
        knowledge=held, expected_knowledge_ref=held.ref,
    )
    payload = workspace.query(S04Projection((0, 1), {2: "0"})).material()
    assert payload["state"] == "UPSTREAM_SCIENCE_OR_SOURCE_HELD"
    assert payload["raw_selected_full_case_n"] is None
    assert payload["complete_output_cells"] == []
    assert payload["raw_original_full_joint_resolved_n"] == 4


def test_foreign_expected_root_and_invalid_conditions_are_refused():
    _, _, knowledge, workspace = _ready()
    other = _ready(parity=1, tag="S04-GENERAL-ALIEN")[2]
    with pytest.raises(S04GeneralAlgebraError, match="expected S04 identity"):
        S04GeneralJointWorkspace(
            knowledge=knowledge, expected_knowledge_ref=other.ref,
        )
    for request, pattern in (
        (S04Projection((0, 0), {}), "duplicated"),
        (S04Projection((True,), {}), "noninteger"),
        (S04Projection((3,), {}), "invalid"),
        (S04Projection((0,), {0: "0"}), "leakage"),
        (S04Projection((0,), {1: "FOREIGN"}), "source domain"),
        (S04Projection((0,), {True: "0"}), "condition axis"),
    ):
        with pytest.raises(S04GeneralAlgebraError, match=pattern):
            workspace.query(request)


def test_bounded_cache_eviction_preserves_exact_outputs_and_replay_identity():
    _, _, knowledge, _ = _ready()
    small = S04GeneralJointWorkspace(
        knowledge=knowledge, expected_knowledge_ref=knowledge.ref,
        max_filter_cache_entries=1, max_cached_row_ids=1,
    )
    full = S04GeneralJointWorkspace(
        knowledge=knowledge, expected_knowledge_ref=knowledge.ref,
    )
    requests = (
        S04Projection((2,), {0: "0", 1: "0"}),
        S04Projection((2,), {0: "1", 1: "1"}),
        S04Projection((2,), {0: "0", 1: "0"}),
    )
    assert [a.ref for a in small.query_many(requests)] == [
        a.ref for a in full.query_many(requests)
    ]
    assert small.cache_stats()["cached_row_ids"] <= 1


def test_original_source_rights_never_promoted_by_arbitrary_requery():
    _, _, knowledge, workspace = _ready()
    x = workspace.query(S04Projection((0, 1, 2), {})).material()
    assert "ORIGINAL_SOURCE_RIGHTS_UNVERIFIED" in x["original_source_authenticity"]
    assert x["independent_original_source_issuer"] is None
    assert x["no_cross_fact_or_cross_risk_pooling"]
    assert "COMPARATIVE_DETERMINICITY_METRIC_NOT_ISSUED" in x["unissued"]
    assert x["source_release_ref"] == knowledge.material()["release_ref"]
