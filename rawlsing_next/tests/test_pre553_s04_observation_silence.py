"""S01-S04: exact observation/silence and multi-question cohort diagnostics.

SOURCEFREE ONLY. These tests use the inherited native I03 evaluator and its
real respondent membership; they do not issue survey frame, scientific design,
causal interpretation, or any Field Forge object.
"""
from dataclasses import replace
from json import loads

import pytest

from rawlsing_next.pre553_empirical_objects import canonical_json, semantic_hash
from rawlsing_next.pre553_s04_observed_research import (
    S04KnowledgeError,
    S04ObservationScope,
    compare_s04_observation_scopes,
    receive_s04_i03_research,
    receive_s04_observation_scope,
)
from rawlsing_next.tests import test_pre553_empirical_query as native
from rawlsing_next.tests.test_pre553_s04_observed_research import _real


def _scope(query, execution):
    knowledge = receive_s04_i03_research(query=query, execution=execution)
    return receive_s04_observation_scope(
        query=query, execution=execution, knowledge=knowledge,
    )


def test_observation_scope_preserves_actual_i03_counts_but_refuses_silence_inference():
    _, _, _, query, execution = _real()
    scope = _scope(query, execution)
    evidence = scope.material()

    assert evidence["state"] == "OBSERVED_FULL_CASE_COHORT__DESCRIPTIVE_ONLY"
    assert evidence["i03_risk_member_extent_n"] == 4
    assert evidence["i03_known_true_condition_n"] == 4
    assert evidence["i03_resolved_joint_n"] == 4
    assert len(evidence["verified_eligible_member_set_sha256"]) == 64
    assert evidence["source_frame_population_n"] is None
    assert evidence["survey_design_weight_or_variance"] is None
    assert evidence["observed_route_and_nonresponse_cause"] is None
    assert evidence["interview_mode_language_and_translation"] is None
    assert evidence["condition_membership_unknown_n"] is None
    assert evidence["no_new_i03_or_source_read"] is True
    assert scope.ref.content_hash == semantic_hash(evidence)


def test_different_actual_questions_can_share_the_same_observed_respondent_set():
    source, qa, predicate, query, execution = _real()
    unary = native._query(source, qa, predicate, ("X",), tag="same-people-unary")
    unary_execution = native._run(source, qa, predicate, unary)

    first = _scope(query, execution)
    second = _scope(unary, unary_execution)
    assert first.material()["fact_ref"] != second.material()["fact_ref"]
    assert first.material()["verified_eligible_member_set_sha256"] == (
        second.material()["verified_eligible_member_set_sha256"]
    )
    comparison = compare_s04_observation_scopes(first, second).material()
    assert comparison["state"] == "SAME_ACTUAL_I03_COHORT__SAMPLE_DESCRIPTIVE_ONLY"
    assert comparison["identical_known_true_respondent_set"] is True
    assert comparison["population_or_survey_design_comparability"] is None
    assert comparison["scientific_estimator_or_causal_comparison"] is None


def test_same_source_and_measure_but_different_member_sets_are_not_automatically_comparable():
    source, qa, predicate, query, execution = _real()
    two = tuple(source["respondents"].values())[:2]
    subset_predicate = native._branch_predicate(
        source, qa, members=two, tag="two-actual-respondents",
    )
    subset_query = native._query(
        source, qa, subset_predicate, ("X", "Y", "Z"), tag="subset-query",
    )
    subset_execution = native._run(source, qa, subset_predicate, subset_query)
    assert subset_execution.facts[0].typed_state == "SUPPORTED"

    left = _scope(query, execution)
    right = _scope(subset_query, subset_execution)
    compared = compare_s04_observation_scopes(left, right).material()
    assert compared["source_release_same"] is True
    assert compared["source_measure_and_response_semantics_same"] is True
    assert compared["identical_known_true_respondent_set"] is False
    assert compared["state"] == (
        "DIFFERENT_ACTUAL_RESPONDENT_COHORTS__NO_NAIVE_RATE_COMPARISON"
    )


def test_different_source_releases_never_acquire_a_synthetic_joint():
    _, _, _, query_a, execution_a = _real(tag="S04-OBS-SOURCE-A")
    _, _, _, query_b, execution_b = _real(tag="S04-OBS-SOURCE-B")
    compared = compare_s04_observation_scopes(
        _scope(query_a, execution_a), _scope(query_b, execution_b),
    ).material()
    assert compared["state"] == "DISTINCT_SOURCE_UNIVERSES__NO_RESPONDENT_POOLING"
    assert compared["source_release_same"] is False
    assert compared["scientific_estimator_or_causal_comparison"] is None


def test_source_fact_identity_substitution_and_rehashed_scope_drift_refuse():
    _, _, _, query, execution = _real()
    scope = _scope(query, execution)
    evidence = scope.material()
    fake = {**evidence, "i03_known_true_condition_n": 999}
    with pytest.raises(S04KnowledgeError, match="identity"):
        S04ObservationScope(canonical_json(fake), scope.content_hash)

    _, _, _, other_query, other_execution = _real(tag="S04-OBS-SOURCE-C")
    other_knowledge = receive_s04_i03_research(
        query=other_query, execution=other_execution,
    )
    with pytest.raises(S04KnowledgeError, match="mismatch|drift"):
        receive_s04_observation_scope(
            query=query, execution=execution, knowledge=other_knowledge,
        )


def test_native_held_risk_does_not_create_supported_sample_comparison():
    source, qa, _, query, execution = _real()
    empty = native._branch_predicate(
        source, qa, members=(), tag="verified-empty-risk",
    )
    empty_query = native._query(
        source, qa, empty, ("X", "Y", "Z"), tag="empty-query",
    )
    held = native._run(source, qa, empty, empty_query)
    assert held.facts[0].typed_state != "SUPPORTED"
    held_scope = _scope(empty_query, held)
    assert held_scope.material()["verified_eligible_member_set_sha256"] is None
    comparison = compare_s04_observation_scopes(
        _scope(query, execution), held_scope,
    ).material()
    assert comparison["state"] == "UNRESOLVED_OR_HELD_COHORT__NO_MEMBERSHIP_COMPARISON"
    assert comparison["identical_known_true_respondent_set"] is None
