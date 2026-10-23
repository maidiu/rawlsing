"""R61-R01V R4 independent reviewer probes (TEST_ONLY)."""
from __future__ import annotations

from dataclasses import replace

import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.tests.test_universal_grammar import (
    _condition_predicates,
    _recurrence_policy,
    _recurrence_source,
    _run_recurrence_generation,
)
from rawlsing_next.universal_grammar.native_map import (
    COMPARATOR_PARENT,
    COMPARATOR_ROOT,
    PARENT_RECEIPT_BOUND,
    PARENT_ROOT,
    RecurrenceParent,
    RecurrencePolicy,
    activate_next_generation,
    build_recurrence_issue_plan,
    execute_recurrence_generation,
    make_root_parent,
)


def _gen1(policy=None):
    source, qauth, root, query = _recurrence_source()
    policy = policy or _recurrence_policy()
    root_parent = make_root_parent(
        predicate=root, source_release_refs=(source["release_ref"],)
    )
    s1 = _condition_predicates(source, qauth, "s1")
    catalog = [root] + [predicate for _, _, predicate in s1]
    plan = build_recurrence_issue_plan(
        policy=policy, generation=1, parents=(root_parent,),
        root_predicate=root, target_label="t", query_ref=query,
        condition_predicates=s1,
    )
    generation = _run_recurrence_generation(source, qauth, plan, 1, catalog)
    assert generation.anti_join["no_drop_ok"], generation.anti_join
    return source, qauth, root, query, policy, root_parent, s1, catalog, generation


def test_B1_severed_receipt_binding_cannot_change_or_refuse_same_consumer():
    source, qauth, root, query, policy, root_parent, s1, catalog, gen1 = _gen1()
    s2 = _condition_predicates(source, qauth, "s2")
    activation = activate_next_generation(
        policy=policy, generation=gen1, parents=(root_parent,),
        root_parent=root_parent, next_generation=2, condition_predicates=s2,
    )
    parent = activation.active_parents[0]
    assert parent.receipt_ref is not None and parent.replay_binding_ref is not None
    catalog2 = list(catalog) + [predicate for _, _, predicate in s2] + [parent.predicate]
    baseline_plan = build_recurrence_issue_plan(
        policy=policy, generation=2, parents=(parent,),
        root_predicate=root, target_label="t", query_ref=query,
        condition_predicates=s2, total_issued_before=4,
    )
    baseline = _run_recurrence_generation(source, qauth, baseline_plan, 2, catalog2)
    assert baseline.anti_join["no_drop_ok"], baseline.anti_join

    bogus = ExactRef("BOGUS_BINDING", "urn:test:r61-r4:bogus-binding", "b" * 64)
    severed = replace(parent, receipt_ref=bogus, replay_binding_ref=bogus, handoff=None)
    severed_plan = build_recurrence_issue_plan(
        policy=policy, generation=2, parents=(severed,),
        root_predicate=root, target_label="t", query_ref=query,
        condition_predicates=s2, total_issued_before=4,
    )
    assert severed_plan.grammar == baseline_plan.grammar
    assert [op.operation_id for op in severed_plan.expected_operations] == [
        op.operation_id for op in baseline_plan.expected_operations
    ]
    severed_gen = _run_recurrence_generation(source, qauth, severed_plan, 2, catalog2)
    assert severed_gen.anti_join["no_drop_ok"], severed_gen.anti_join


def test_B2_generation_label_from_root_is_accepted_as_recurrence():
    source, qauth, root, query, policy, root_parent, s1, catalog, gen1 = _gen1()
    s2 = _condition_predicates(source, qauth, "s2")
    catalog2 = list(catalog) + [predicate for _, _, predicate in s2]
    relabelled = build_recurrence_issue_plan(
        policy=policy, generation=2, parents=(root_parent,),
        root_predicate=root, target_label="t", query_ref=query,
        condition_predicates=s2, total_issued_before=4,
    )
    assert relabelled.generation == 2
    assert all(parent.kind == PARENT_ROOT for parent in relabelled.parents)
    result = _run_recurrence_generation(source, qauth, relabelled, 2, catalog2)
    assert result.anti_join["no_drop_ok"], result.anti_join


def test_B3_total_issued_before_is_caller_declared_not_enforced_ledger():
    source, qauth, root, query, policy, root_parent, s1, catalog, gen1 = _gen1()
    s2 = _condition_predicates(source, qauth, "s2")
    s3 = _condition_predicates(source, qauth, "s3")
    two_conditions = s2 + s3
    activation = activate_next_generation(
        policy=policy, generation=gen1, parents=(root_parent,),
        root_parent=root_parent, next_generation=2, condition_predicates=two_conditions,
    )
    wide = _recurrence_policy(breadth=3, per_generation=8, total=12)
    honest = build_recurrence_issue_plan(
        policy=wide, generation=2, parents=activation.active_parents,
        root_predicate=root, target_label="t", query_ref=query,
        condition_predicates=two_conditions, total_issued_before=8,
    )
    understated = build_recurrence_issue_plan(
        policy=wide, generation=2, parents=activation.active_parents,
        root_predicate=root, target_label="t", query_ref=query,
        condition_predicates=two_conditions, total_issued_before=0,
    )
    assert len(honest.expected_operations) <= 4
    assert len(understated.expected_operations) > len(honest.expected_operations)
    assert "total_issued_before" not in honest.material()


def test_B4_profile_configuration_refuses_typed_not_defaulted():
    base = dict(
        policy_id="R61-R4-B4", policy_version="r61.r4.1", grade="TEST_ONLY",
        owner_refs=("R61-R4-B4",),
        counting_convention="ANCESTOR_CONDITIONS_COUNT_TOWARD_K",
        bounds={"J": 2, "K": 3, "D": 3}, breadth_cap=2, followup_cap=2,
        protected_exploration_slots=1, per_generation_issued_cap=4,
        total_issued_cap=12, comparators=(COMPARATOR_ROOT, COMPARATOR_PARENT),
    )
    RecurrencePolicy(**base)
    with pytest.raises(ValueError, match="BOUND_K"):
        RecurrencePolicy(**{**base, "bounds": {"J": 2, "D": 3}})
    with pytest.raises(ValueError, match="BOUND_D"):
        RecurrencePolicy(**{**base, "bounds": {"J": 2, "K": 3}})
    with pytest.raises(ValueError, match="COUNTING"):
        RecurrencePolicy(**{**base, "counting_convention": "UNKNOWN"})
    with pytest.raises(ValueError, match="GRADE"):
        RecurrencePolicy(**{**base, "grade": "PRODUCTION"})
    with pytest.raises(ValueError, match="COMPARATORS"):
        RecurrencePolicy(**{**base, "comparators": (COMPARATOR_ROOT,)})
    with pytest.raises(ValueError, match="nonnegative"):
        RecurrencePolicy(**{**base, "per_generation_issued_cap": -1})


def test_B5_receipt_bound_parent_without_receipt_or_handoff_is_accepted():
    source, qauth, root, query, policy, root_parent, s1, catalog, gen1 = _gen1()
    s2 = _condition_predicates(source, qauth, "s2")
    bare = RecurrenceParent(
        parent_id="caller-invented-parent",
        predicate=root,
        kind=PARENT_RECEIPT_BOUND,
        generation=1,
        source_release_refs=(source["release_ref"],),
        receipt_ref=None,
        replay_binding_ref=None,
        handoff=None,
    )
    plan = build_recurrence_issue_plan(
        policy=policy, generation=2, parents=(bare,),
        root_predicate=root, target_label="t", query_ref=query,
        condition_predicates=s2, total_issued_before=4,
    )
    result = _run_recurrence_generation(source, qauth, plan, 2, catalog + [p for _, _, p in s2])
    assert result.anti_join["no_drop_ok"], result.anti_join


def test_B6_gen2_comparator_baselines_are_distinct_views():
    source, qauth, root, query, policy, root_parent, s1, catalog, gen1 = _gen1()
    s2 = _condition_predicates(source, qauth, "s2")
    activation = activate_next_generation(
        policy=policy, generation=gen1, parents=(root_parent,),
        root_parent=root_parent, next_generation=2, condition_predicates=s2,
    )
    parent = activation.active_parents[0]
    assert parent.predicate.ref != root.ref
    plan = build_recurrence_issue_plan(
        policy=policy, generation=2, parents=(parent,),
        root_predicate=root, target_label="t", query_ref=query,
        condition_predicates=s2, total_issued_before=4,
    )
    ops = {op.comparator: op for op in plan.expected_operations}
    assert set(ops) == {COMPARATOR_ROOT, COMPARATOR_PARENT}
    assert ops[COMPARATOR_ROOT].baseline_predicate_ref["content_hash"] == root.content_hash
    assert ops[COMPARATOR_PARENT].baseline_predicate_ref["content_hash"] == parent.predicate.content_hash
    assert ops[COMPARATOR_ROOT].operation_id != ops[COMPARATOR_PARENT].operation_id
    assert ops[COMPARATOR_ROOT].condition_keys != ops[COMPARATOR_PARENT].condition_keys


def test_B7_total_budget_exhaustion_refuses_without_explicit_unissued_record():
    source, qauth, root, query, policy, root_parent, s1, catalog, gen1 = _gen1()
    s2 = _condition_predicates(source, qauth, "s2")
    with pytest.raises(ValueError, match="ISSUED_NO_OPERATIONS"):
        build_recurrence_issue_plan(
            policy=policy, generation=2, parents=(root_parent,),
            root_predicate=root, target_label="t", query_ref=query,
            condition_predicates=s2, total_issued_before=12,
        )
