"""REMONT RMT-Q015 sourcefree falsifiers: continuing PYAT determinicity.

Uses REAL inherited C11→I03→S04 fixtures; no independent original35
source/science authority, population variance, causal ranking or actors.
Author does not run this module; REMONT owns first-fault execution/repair.
"""
import pytest

from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_s04_country_refinement import (
    CountryRequest, RefinementBudget,
)
from rawlsing_next.pre553_s04_determinicity_cycle import (
    CyclePolicy, DeterminicityCycleError, ObservationChannel,
    advance_country_determinicity, consume_determinicity_context_for_prev3,
)
from rawlsing_next.pre553_s04_observed_research import receive_s04_i03_research
from rawlsing_next.pre553_s04_general_joint_algebra import S04GeneralJointWorkspace
from rawlsing_next.tests.test_pre553_s04_country_refinement import _real_joint
from rawlsing_next.tests.test_pre553_empirical_query import (
    _build_source, _branch_predicate, _query, _query_authority, _registry, _ref,
)


def _policy(**kwargs):
    d = dict(
        target_axis=0, predictor_axes=(1, 2), fixed_context=(),
        min_branch_n=2, max_depth=2, max_total_nodes=16,
        max_pending_nodes=16, max_new_nodes_per_call=1,
        max_receipt_bytes=250_000, max_pair_order=2,
        bootstrap_replicates=0, min_signal_bits="0.00001",
    )
    d.update(kwargs)
    return CyclePolicy(**d)


def _resources(**kwargs):
    d = dict(
        max_input_cells=16384, max_cell_visits=100_000,
        max_output_cells=10_000, max_candidates=8, wall_seconds=60,
    )
    d.update(kwargs)
    return RefinementBudget(**d)


def _advance(real, *, policy=None, resources=None, previous=None,
             pinned=None, observations=()):
    return advance_country_determinicity(
        universe=real["universe"], query=real["query"],
        predicate=real["predicate"], execution=real["execution"],
        registry=real["registry"],
        country=CountryRequest(country="US", source_family="SURVEY", wave="W1"),
        policy=policy or _policy(), resources=resources or _resources(),
        observation_channels=observations, prior=previous,
        independently_pinned_prior_ref=pinned,
    )


def test_actual_i03_source_country_root_selects_informative_predictor_and_conserves_minorities():
    real = _real_joint("cycle-root")
    receipt = _advance(real)
    m = receipt.material()
    assert m["status"] == "PARTIAL_RESUMABLE"
    assert m["source"]["country"] == "US"
    assert m["source"]["knowledge_ref"]["content_hash"]
    assert m["base_same_case_n"] == 8
    assert sum(x["n"] for x in m["base_target_distribution"]) == 8
    assert len(m["nodes"]) == 1
    root = m["nodes"][0]
    assert root["selected_split_axis"] == 1
    assert root["raw_same_case_n"] == 8
    assert len(root["predictor_screens"]) == 2
    assert root["predictor_screens"][0]["information_bits"] == 1
    assert root["predictor_screens"][1]["information_bits"] == 0
    assert m["remaining_budgeted_work"]
    assert m["new_I03_queries"] == 0
    assert not m["independent_original_source_rights"]
    assert not m["exact_I05_frontier_modified"]


def test_continuation_replays_same_knowledge_and_finishes_without_new_i03():
    real = _real_joint("cycle-resume")
    policy = _policy(max_depth=1)
    receipt = _advance(real, policy=policy)
    for _ in range(8):
        if not receipt.material()["remaining_budgeted_work"]:
            break
        receipt = _advance(real, policy=policy, previous=receipt,
                           pinned=receipt.ref)
    m = receipt.material()
    assert m["status"] == "COMPLETE_WITHIN_SOURCE_JOINT_NOT_EXHAUSTIVE_HUMAN"
    assert len(m["nodes"]) == 3
    assert m["new_I03_queries"] == 0
    assert {x["depth"] for x in m["nodes"]} == {0, 1}
    assert all(x["raw_same_case_n"] is not None for x in m["nodes"])
    assert not m["remaining_budgeted_work"]


def test_no_predictor_left_still_reports_genuine_leaf_distribution():
    real = _real_joint("cycle-leaf")
    policy = _policy(predictor_axes=(1,), max_depth=1)
    first = _advance(real, policy=policy)
    second = _advance(real, policy=policy, previous=first, pinned=first.ref)
    assert len(second.material()["nodes"]) == 2
    leaf = second.material()["nodes"][1]
    assert leaf["raw_same_case_n"] == 4
    assert sum(x["n"] for x in leaf["target_distribution"]) == 4
    assert leaf["selected_split_axis"] is None


def test_broader_distribution_survives_when_no_predictor_batch_affordable():
    real = _real_joint("cycle-coarse")
    receipt = _advance(real, resources=_resources(max_cell_visits=8))
    m = receipt.material()
    assert m["status"] == "PARTIAL_RESUMABLE"
    assert m["nodes"] == []
    assert m["base_same_case_n"] == 8
    assert sum(x["n"] for x in m["base_target_distribution"]) == 8
    assert m["remaining_budgeted_work"]
    knowledge = receive_s04_i03_research(
        query=real["query"], execution=real["execution"])
    workspace = S04GeneralJointWorkspace(
        knowledge=knowledge, expected_knowledge_ref=knowledge.ref)
    consumed = consume_determinicity_context_for_prev3(
        receipt=receipt, independently_pinned_receipt_ref=receipt.ref,
        workspace=workspace,
    )
    assert consumed["raw_same_case_n"] == 8
    assert consumed["must_use_existing_independently_pinned_c4_c5_before_v3"]
    assert consumed["does_not_issue_actor_or_person"]


def test_host_budget_can_change_on_resume_without_changing_empirical_policy():
    real = _real_joint("cycle-throttle")
    policy = _policy(max_depth=0)
    first = _advance(real, policy=policy, resources=_resources(max_candidates=1))
    assert first.material()["active"]["next_predictor_offset"] == 1
    next_ = _advance(real, policy=policy, resources=_resources(max_candidates=8),
                     previous=first, pinned=first.ref)
    assert next_.material()["status"] == "COMPLETE_WITHIN_SOURCE_JOINT_NOT_EXHAUSTIVE_HUMAN"
    assert len(next_.material()["nodes"][0]["predictor_screens"]) == 2


def test_wrong_or_missing_external_pin_refuses_resumption():
    real = _real_joint("cycle-pin")
    first = _advance(real)
    with pytest.raises(DeterminicityCycleError, match="INDEPENDENT_PREVIOUS"):
        _advance(real, previous=first)
    with pytest.raises(DeterminicityCycleError, match="INDEPENDENT_PREVIOUS"):
        _advance(real, previous=first, pinned=_ref("FRAUD", "other"))


def test_source_observation_meaning_cannot_be_invented_by_caller():
    real = _real_joint("cycle-missingness")
    spec = ObservationChannel(
        value_axis=1, status_axis=2, observed_status="1",
        unobserved_placeholder="0",
        semantics_authority_ref=real["source"]["coord_auth"].authority_ref,
    )
    with pytest.raises(DeterminicityCycleError,
                       match="OBSERVATION_STATUS_SEMANTICS_NOT_ISSUED"):
        _advance(real, observations=(spec,))


def test_low_support_is_not_a_person_or_negative_population_truth():
    real = _real_joint("cycle-low-n")
    receipt = _advance(real, policy=_policy(min_branch_n=16))
    m = receipt.material()
    assert m["base_same_case_n"] == 8
    assert m["base_target_distribution"] == []
    assert not m["independent_original_source_rights"]


def _xor():
    rows = []
    for i in range(16):
        a, b = (i // 2) % 2, i % 2
        rows.append({"id": f"X{i}", "responses": {
            "Y": str(a ^ b), "X1": str(a), "X2": str(b),
        }})
    src = _build_source("cycle-xor", rows)
    auth = _query_authority("cycle-xor-query")
    predicate = _branch_predicate(src, auth, tag="cycle-xor-all")
    query = _query(src, auth, predicate, ("Y", "X1", "X2"), tag="cycle-xor-joint")
    registry = _registry(src, auth)
    execution = execute_empirical_query(
        repository=src["repo"], query=query, predicate=predicate,
        authority_registry=registry, release_refs=(src["release_ref"],),
    )
    return dict(
        universe=src["universe"], source=src,
        predicate=predicate, query=query, registry=registry,
        execution=execution,
    )


def test_xor_interaction_recruits_a_zero_marginal_axis_then_recovers_conditional_information():
    real = _xor()
    policy = _policy(max_depth=1, min_signal_bits="0.1")
    first = _advance(real, policy=policy)
    root = first.material()["nodes"][0]
    assert root["predictor_screens"][0]["information_bits"] == 0
    assert root["predictor_screens"][1]["information_bits"] == 0
    assert root["selected_split_axis"] == 1
    assert root["selected_split_score_bits"]["$exact_decimal"] == "0.5" or root["selected_split_score_bits"] == 0.5
    followup = _advance(real, policy=policy, previous=first, pinned=first.ref)
    child = followup.material()["nodes"][1]
    assert child["selected_split_axis"] is None
    assert child["predictor_screens"][0]["information_bits"] == 1
    assert child["raw_same_case_n"] == 8
    assert followup.material()["new_I03_queries"] == 0
