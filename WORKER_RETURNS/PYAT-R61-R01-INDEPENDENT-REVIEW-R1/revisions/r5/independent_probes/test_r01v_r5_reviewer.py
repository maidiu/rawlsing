"""R61-R01V R5 independent reviewer probes (disposable, below own return root).

Oracle: reviewer-owned EXPECTATIONS.md frozen before candidate inspection.
Candidate output never defines expected identity sets.
"""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import json
import os
import subprocess
import sys

import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash, canonicalize
from rawlsing_next.tests.test_pre553_empirical_query import (
    _build_source, _branch_predicate, _predicate, _query, _query_authority,
    _response_leaf,
)
from rawlsing_next.tests.test_universal_grammar import (
    _condition_predicates, _recurrence_policy, _recurrence_source,
    _run_recurrence_generation,
)
from rawlsing_next.universal_grammar.native_map import (
    COMPARATOR_PARENT, COMPARATOR_ROOT, PARENT_EXPLORATORY,
    PARENT_RECEIPT_BOUND, RecurrenceParent, RecurrenceRefusal,
    _parent_id, activate_next_generation, build_recurrence_issue_plan,
    execute_recurrence_generation, make_recurrence_parent_resolver,
    make_root_parent, RECURRENCE_ISSUED,
)
from rawlsing_next.universal_grammar.types import OccurrenceKey

REPO_ROOT = Path(__file__).resolve().parents[5]
PROBE_DIR = Path(__file__).resolve().parent


def _gen1(policy=None):
    source, qauth, root, query = _recurrence_source()
    policy = policy or _recurrence_policy()
    root_parent = make_root_parent(
        predicate=root, source_release_refs=(source["release_ref"],)
    )
    s1 = _condition_predicates(source, qauth, "s1")
    catalog = [root] + [predicate for _, _, predicate in s1]
    p1 = build_recurrence_issue_plan(
        policy=policy, generation=1, parents=(root_parent,),
        root_predicate=root, target_label="t", query_ref=query,
        condition_predicates=s1, release_refs=(source["release_ref"],),
    )
    g1 = _run_recurrence_generation(source, qauth, p1, 1, catalog)
    assert g1.anti_join["no_drop_ok"], g1.anti_join
    return source, qauth, root, query, policy, root_parent, s1, catalog, p1, g1


def _gen2(policy=None):
    source, qauth, root, query, policy, root_parent, s1, catalog, p1, g1 = _gen1(policy)
    s2 = _condition_predicates(source, qauth, "s2")
    activation1 = activate_next_generation(
        policy=policy, generation=g1, parents=(root_parent,),
        root_parent=root_parent, next_generation=2, condition_predicates=s2,
    )
    resolver = make_recurrence_parent_resolver(g1.execution.handoffs)
    p2 = build_recurrence_issue_plan(
        policy=policy, generation=2, parents=activation1.active_parents,
        root_predicate=root, target_label="t", query_ref=query,
        condition_predicates=s2, previous_plan=p1,
        parent_resolver=resolver, release_refs=(source["release_ref"],),
    )
    catalog2 = catalog + [predicate for _, _, predicate in s2] + [
        parent.predicate for parent in activation1.active_parents
    ]
    g2 = _run_recurrence_generation(source, qauth, p2, 2, catalog2)
    assert g2.anti_join["no_drop_ok"], g2.anti_join
    return (
        source, qauth, root, query, policy, root_parent, s1, catalog, p1, g1,
        s2, activation1, resolver, p2, g2,
    )


# ------------------------------------------------------------------ hostile
def test_H1_receipt_bound_ancestry_is_bound_to_parent_identity():
    source, qauth, root, query, policy, root_parent, s1, catalog, p1, g1 = _gen1()
    s2 = _condition_predicates(source, qauth, "s2")
    activation1 = activate_next_generation(
        policy=policy, generation=g1, parents=(root_parent,),
        root_parent=root_parent, next_generation=2, condition_predicates=s2,
    )
    parent = next(
        candidate for candidate in activation1.active_parents
        if candidate.kind == PARENT_RECEIPT_BOUND
    )
    assert parent.ancestry_conditions
    stripped = replace(parent, ancestry_conditions=(), ancestry_predicates=())
    assert stripped.parent_id == parent.parent_id
    with pytest.raises(RecurrenceRefusal):
        build_recurrence_issue_plan(
            policy=policy, generation=2, parents=(stripped,),
            root_predicate=root, target_label="t", query_ref=query,
            condition_predicates=s2, previous_plan=p1,
            parent_resolver=make_recurrence_parent_resolver(g1.execution.handoffs),
            release_refs=(source["release_ref"],),
        )


def test_H2_receipt_bound_generation_relabel_cannot_skip_a_generation():
    (source, qauth, root, query, policy, root_parent, s1, catalog, p1, g1,
     s2, activation1, resolver, p2, g2) = _gen2()
    source_parent = activation1.active_parents[0]
    assert source_parent.generation == 1
    relabelled = replace(
        source_parent,
        generation=2,
        parent_id=_parent_id(
            PARENT_RECEIPT_BOUND, source_parent.predicate, 2,
            (source_parent.receipt_ref, source_parent.replay_binding_ref),
        ),
    )
    assert relabelled.parent_id != source_parent.parent_id
    s3 = _condition_predicates(source, qauth, "s3")
    with pytest.raises(RecurrenceRefusal):
        build_recurrence_issue_plan(
            policy=policy, generation=3, parents=(relabelled,),
            root_predicate=root, target_label="t", query_ref=query,
            condition_predicates=s3, previous_plan=p2,
            parent_resolver=make_recurrence_parent_resolver(
                g1.execution.handoffs + g2.execution.handoffs
            ),
            release_refs=(source["release_ref"],),
        )


def test_H3_execution_revalidates_embedded_parent_binding():
    (source, qauth, root, query, policy, root_parent, s1, catalog, p1, g1,
     s2, activation1, resolver, p2, g2) = _gen2()
    parent = next(
        candidate for candidate in p2.parents
        if candidate.kind == PARENT_RECEIPT_BOUND
    )
    other = next(
        handoff for handoff in g1.execution.handoffs + g2.execution.handoffs
        if handoff.ref != parent.replay_binding_ref
    )
    tampered = replace(parent, handoff=other)
    assert tampered.receipt_ref == parent.receipt_ref
    assert tampered.replay_binding_ref == parent.replay_binding_ref
    assert other.receipt_ref != tampered.receipt_ref
    tampered_plan = replace(p2, parents=(tampered,))
    with pytest.raises(RecurrenceRefusal):
        _run_recurrence_generation(
            source, qauth, tampered_plan, 2,
            catalog + [predicate for _, _, predicate in s2]
            + [candidate.predicate for candidate in p2.parents],
        )


def test_H4_replaced_predecessor_plan_cannot_undercount_issued_work():
    policy = _recurrence_policy(total=5, per_generation=4)
    (source, qauth, root, query, policy, root_parent, s1, catalog, p1, g1) = _gen1(policy)
    assert len(p1.expected_operations) == 4
    assert p1.cumulative_issued_count == 4
    fake_p1 = replace(
        p1,
        expected_operations=p1.expected_operations[:2],
        cumulative_issued_count=2,
    )
    assert fake_p1.cumulative_issued_count == (
        fake_p1.predecessor_issued_count + len(fake_p1.expected_operations)
    )
    s2 = _condition_predicates(source, qauth, "s2")
    activation1 = activate_next_generation(
        policy=policy, generation=g1, parents=(root_parent,),
        root_parent=root_parent, next_generation=2, condition_predicates=s2,
    )
    common = dict(
        policy=policy, generation=2, parents=activation1.active_parents,
        root_predicate=root, target_label="t", query_ref=query,
        condition_predicates=s2,
        parent_resolver=make_recurrence_parent_resolver(g1.execution.handoffs),
        release_refs=(source["release_ref"],),
    )
    honest = build_recurrence_issue_plan(**common, previous_plan=p1)
    assert len(honest.expected_operations) == 1
    with pytest.raises(RecurrenceRefusal):
        build_recurrence_issue_plan(**common, previous_plan=fake_p1)


def test_H5_zero_per_generation_cap_is_stopped_budget_not_a_crash():
    policy = _recurrence_policy(per_generation=0)
    source, qauth, root, query = _recurrence_source()
    root_parent = make_root_parent(
        predicate=root, source_release_refs=(source["release_ref"],)
    )
    s1 = _condition_predicates(source, qauth, "s1")
    plan = build_recurrence_issue_plan(
        policy=policy, generation=1, parents=(root_parent,),
        root_predicate=root, target_label="t", query_ref=query,
        condition_predicates=s1, release_refs=(source["release_ref"],),
    )
    assert plan.state == "STOPPED_BUDGET"
    assert plan.expected_operations == ()
    assert plan.unissued


def test_H6_root_parent_must_be_the_declared_source_root():
    source, qauth, root, query = _recurrence_source()
    policy = _recurrence_policy()
    s1 = _condition_predicates(source, qauth, "s1")
    wrong_root_parent = make_root_parent(
        predicate=s1[0][2], source_release_refs=(source["release_ref"],)
    )
    with pytest.raises(RecurrenceRefusal):
        build_recurrence_issue_plan(
            policy=policy, generation=1, parents=(wrong_root_parent,),
            root_predicate=root, target_label="t", query_ref=query,
            condition_predicates=s1, release_refs=(source["release_ref"],),
        )


def test_H7_activation_requires_the_actual_next_generation_label():
    source, qauth, root, query, policy, root_parent, s1, catalog, p1, g1 = _gen1()
    s2 = _condition_predicates(source, qauth, "s2")
    with pytest.raises(RecurrenceRefusal):
        activate_next_generation(
            policy=policy, generation=g1, parents=(root_parent,),
            root_parent=root_parent, next_generation=1,
            condition_predicates=s2,
        )
