"""R61-R01V R5 independent changed-data D=3 positive probe (TEST_ONLY)."""
from __future__ import annotations

from collections import Counter
from pathlib import Path

from rawlsing_next.tests.test_pre553_empirical_query import (
    _build_source, _branch_predicate, _predicate, _query, _query_authority,
    _response_leaf,
)
from rawlsing_next.universal_grammar.native_map import (
    COMPARATOR_PARENT, COMPARATOR_ROOT, PARENT_EXPLORATORY,
    activate_next_generation, build_recurrence_issue_plan,
    make_recurrence_parent_resolver, make_root_parent,
)
from rawlsing_next.universal_grammar.types import OccurrenceKey

REPO_ROOT = Path(__file__).resolve().parents[5]


def _source():
    rows = []

    def add(group, t, q3):
        rows.append({
            "id": f"N{len(rows):02d}",
            "responses": {"q1": int(group[0]), "q2": int(group[1]),
                          "q3": q3, "out": t},
        })

    for t, q3 in ((1, 0), (1, 1), (1, 0), (0, 1)):
        add("00", t, q3)
    for t, q3 in ((1, 0), (0, 1), (0, 0), (0, 1)):
        add("01", t, q3)
    for t, q3 in ((1, 0), (1, 1), (1, 0), (0, 1)):
        add("10", t, q3)
    for t, q3 in ((1, 0), (0, 1), (0, 0), (0, 1)):
        add("11", t, q3)
    source = _build_source("r61-r5-independent", rows)
    source["_rows"] = rows
    qauth = _query_authority("r61-r5-independent")
    root = _branch_predicate(source, qauth, tag="r61-r5-independent-root")
    query = _query(source, qauth, root, ("out",), tag="r61-r5-independent-out")
    return source, qauth, root, query, rows


def _conditions(source, qauth, variable):
    return tuple(
        (OccurrenceKey(variable), value,
         _predicate(source, qauth, _response_leaf(source, qauth, variable, value),
                    tag=f"r61-r5-independent-{variable}-{value}"))
        for value in (0, 1)
    )


def _policy():
    from rawlsing_next.universal_grammar.native_map import RecurrencePolicy
    return RecurrencePolicy(
        policy_id="R61-R5-INDEPENDENT-POLICY", policy_version="r61.r4.1",
        grade="TEST_ONLY", owner_refs=("R61-R5-INDEPENDENT",),
        counting_convention="ANCESTOR_CONDITIONS_COUNT_TOWARD_K",
        bounds={"J": 2, "K": 3, "D": 3}, breadth_cap=2, followup_cap=2,
        protected_exploration_slots=1, per_generation_issued_cap=8,
        total_issued_cap=24, comparators=(COMPARATOR_ROOT, COMPARATOR_PARENT),
    )


def _run(source, qauth, plan, generation, predicates):
    from rawlsing_next.tests.test_universal_grammar import _run_recurrence_generation
    return _run_recurrence_generation(source, qauth, plan, generation, predicates)


def _expected_shape(plan, root):
    shape = []
    for parent in plan.parents:
        for key, value, _ in plan.condition_predicates:
            shape.append((
                parent.parent_id, COMPARATOR_PARENT,
                (key.item_id,), (value,), parent.predicate.content_hash,
            ))
            root_keys = tuple(k.item_id for k, _ in parent.ancestry_conditions) + (
                key.item_id,
            )
            root_values = tuple(v for _, v in parent.ancestry_conditions) + (value,)
            shape.append((
                parent.parent_id, COMPARATOR_ROOT,
                root_keys, root_values, root.content_hash,
            ))
    return Counter(shape)


def _actual_shape(plan):
    return Counter(
        (
            operation.parent_id, operation.comparator,
            tuple(key.item_id for key in operation.condition_keys),
            tuple(operation.condition_values),
            operation.baseline_predicate_ref["content_hash"],
        )
        for operation in plan.expected_operations
    )


def _rate(rows, conditions):
    selected = [
        row for row in rows
        if all(row["responses"][key.item_id] == value
               for key, value in conditions)
    ]
    assert selected, conditions
    return sum(row["responses"]["out"] for row in selected), len(selected)


def _state(rows, parent, operation):
    child_conditions = parent.ancestry_conditions + tuple(
        zip(operation.condition_keys[-1:], operation.condition_values[-1:])
    )
    child_num, child_den = _rate(rows, child_conditions)
    if operation.comparator == COMPARATOR_PARENT:
        base_conditions = parent.ancestry_conditions
    else:
        base_conditions = ()
    base_num, base_den = _rate(rows, base_conditions)
    differs = child_num * base_den != base_num * child_den
    return "DISCOVERED_RESULT_SUPPORTED" if differs else "VALID_EMPTY"


def test_P1_changed_data_d3_positive_hidden_minority_and_arithmetic():
    source, qauth, root, query, rows = _source()
    policy = _policy()
    root_parent = make_root_parent(
        predicate=root, source_release_refs=(source["release_ref"],)
    )
    q1 = _conditions(source, qauth, "q1")
    q2 = _conditions(source, qauth, "q2")
    q3 = _conditions(source, qauth, "q3")
    catalog = [root] + [p for _, _, p in q1]
    p1 = build_recurrence_issue_plan(
        policy=policy, generation=1, parents=(root_parent,),
        root_predicate=root, target_label="out", query_ref=query,
        condition_predicates=q1, release_refs=(source["release_ref"],),
    )
    assert _actual_shape(p1) == _expected_shape(p1, root)
    g1 = _run(source, qauth, p1, 1, catalog)
    assert g1.anti_join["no_drop_ok"]

    activation1 = activate_next_generation(
        policy=policy, generation=g1, parents=(root_parent,),
        root_parent=root_parent, next_generation=2, condition_predicates=q2,
    )
    assert any(p.kind == PARENT_EXPLORATORY for p in activation1.active_parents)
    p2 = build_recurrence_issue_plan(
        policy=policy, generation=2, parents=activation1.active_parents,
        root_predicate=root, target_label="out", query_ref=query,
        condition_predicates=q2, previous_plan=p1,
        parent_resolver=make_recurrence_parent_resolver(g1.execution.handoffs),
        release_refs=(source["release_ref"],),
    )
    assert _actual_shape(p2) == _expected_shape(p2, root)
    catalog2 = catalog + [p for _, _, p in q2] + [
        parent.predicate for parent in activation1.active_parents
    ]
    g2 = _run(source, qauth, p2, 2, catalog2)
    assert g2.anti_join["no_drop_ok"]
    parent_by_id = {parent.parent_id: parent for parent in p2.parents}
    for operation in p2.expected_operations:
        expected = _state(rows, parent_by_id[operation.parent_id], operation)
        actual = g2.receipt_by_rule[operation.rule_id].typed_state
        assert actual == expected, (
            operation.parent_id, operation.comparator,
            operation.condition_keys, operation.condition_values,
            expected, actual,
        )

    activation2 = activate_next_generation(
        policy=policy, generation=g2, parents=p2.parents,
        root_parent=root_parent, next_generation=3, condition_predicates=q3,
    )
    assert activation2.active_parents
    p3 = build_recurrence_issue_plan(
        policy=policy, generation=3, parents=activation2.active_parents,
        root_predicate=root, target_label="out", query_ref=query,
        condition_predicates=q3, previous_plan=p2,
        parent_resolver=make_recurrence_parent_resolver(
            g1.execution.handoffs + g2.execution.handoffs
        ),
        release_refs=(source["release_ref"],),
    )
    assert _actual_shape(p3) == _expected_shape(p3, root)
    catalog3 = catalog2 + [p for _, _, p in q3] + [
        parent.predicate for parent in activation2.active_parents
    ]
    g3 = _run(source, qauth, p3, 3, catalog3)
    assert g3.anti_join["no_drop_ok"]
    parent_by_id3 = {parent.parent_id: parent for parent in p3.parents}
    for operation in p3.expected_operations:
        expected = _state(rows, parent_by_id3[operation.parent_id], operation)
        actual = g3.receipt_by_rule[operation.rule_id].typed_state
        assert actual == expected, (
            operation.parent_id, operation.comparator,
            operation.condition_keys, operation.condition_values,
            expected, actual,
        )

    assert [g1.plan.generation, g2.plan.generation, g3.plan.generation] == [1, 2, 3]
    assert p1.cumulative_issued_count == len(p1.expected_operations)
    assert p2.cumulative_issued_count == (
        len(p1.expected_operations) + len(p2.expected_operations)
    )
    assert p3.cumulative_issued_count == p2.cumulative_issued_count + len(
        p3.expected_operations
    )

    # Neutral-aggregate parent: q1=0 is 50% at the root and 50% inside q1=0,
    # while its q2 subgroups split to 75% and 25% in opposite directions.
    neutral = next(
        parent for parent in p2.parents
        if parent.kind == PARENT_EXPLORATORY
    )
    neutral_ops = [
        operation for operation in p2.expected_operations
        if operation.parent_id == neutral.parent_id
        and operation.comparator == COMPARATOR_PARENT
    ]
    states = {
        operation.condition_values[-1]: g2.receipt_by_rule[operation.rule_id].typed_state
        for operation in neutral_ops
    }
    assert states == {0: "DISCOVERED_RESULT_SUPPORTED", 1: "DISCOVERED_RESULT_SUPPORTED"}
    child_rates = {
        operation.condition_values[-1]: _rate(rows, neutral.ancestry_conditions + (
            (OccurrenceKey("q2"), operation.condition_values[-1]),
        ))
        for operation in neutral_ops
    }
    assert child_rates[0][0] * child_rates[1][1] > child_rates[1][0] * child_rates[0][1]
    parent_rate = _rate(rows, neutral.ancestry_conditions)
    root_rate = _rate(rows, ())
    assert parent_rate[0] * root_rate[1] == root_rate[0] * parent_rate[1]
    assert child_rates[0][0] * parent_rate[1] > parent_rate[0] * child_rates[0][1]
    assert child_rates[1][0] * parent_rate[1] < parent_rate[0] * child_rates[1][1]

    # Root-relative and parent-relative views of the same neutral parent differ.
    for operation in neutral_ops:
        root_op = next(
            candidate for candidate in p2.expected_operations
            if candidate.parent_id == neutral.parent_id
            and candidate.comparator == COMPARATOR_ROOT
            and candidate.condition_values[-1] == operation.condition_values[-1]
        )
        assert root_op.operation_id != operation.operation_id
        assert root_op.baseline_predicate_ref["content_hash"] != (
            operation.baseline_predicate_ref["content_hash"]
        )


def test_P2_cold_fresh_process_persisted_handoff_replay(tmp_path):
    import json
    import os
    import subprocess
    import sys

    from rawlsing_next.pre553_recursive_handoff import write_recursive_handoff_bundle

    source, qauth, root, query, rows = _source()
    policy = _policy()
    root_parent = make_root_parent(
        predicate=root, source_release_refs=(source["release_ref"],)
    )
    q1 = _conditions(source, qauth, "q1")
    p1 = build_recurrence_issue_plan(
        policy=policy, generation=1, parents=(root_parent,),
        root_predicate=root, target_label="out", query_ref=query,
        condition_predicates=q1, release_refs=(source["release_ref"],),
    )
    g1 = _run(source, qauth, p1, 1, [root] + [p for _, _, p in q1])
    path = tmp_path / "r61_r5_independent_handoffs.json"
    bundle_ref = write_recursive_handoff_bundle(path, g1.execution.handoffs)
    code = """
import json, sys
from dataclasses import replace
from rawlsing_next.pre553_recursive_handoff import load_recursive_handoff_bundle
from rawlsing_next.universal_grammar.native_map import (
    activate_next_generation, build_recurrence_issue_plan,
    make_recurrence_parent_resolver, make_root_parent,
)
from test_r01v_r5_positive import _source, _conditions, _policy, _run

bundle_path, expected_predecessor = sys.argv[1], sys.argv[2]
source, qauth, root, query, rows = _source()
policy = _policy()
root_parent = make_root_parent(
    predicate=root, source_release_refs=(source["release_ref"],)
)
q1 = _conditions(source, qauth, "q1")
q2 = _conditions(source, qauth, "q2")
p1 = build_recurrence_issue_plan(
    policy=policy, generation=1, parents=(root_parent,),
    root_predicate=root, target_label="out", query_ref=query,
    condition_predicates=q1, release_refs=(source["release_ref"],),
)
g1 = _run(source, qauth, p1, 1, [root] + [p for _, _, p in q1])
activation = activate_next_generation(
    policy=policy, generation=g1, parents=(root_parent,),
    root_parent=root_parent, next_generation=2, condition_predicates=q2,
)
bundle_ref, loaded = load_recursive_handoff_bundle(bundle_path)
refs = {handoff.ref.key for handoff in loaded}
assert all(
        parent.replay_binding_ref.key in refs
        for parent in activation.active_parents
        if parent.replay_binding_ref is not None
    )
resolver = make_recurrence_parent_resolver(loaded, bundle_ref=bundle_ref)
p2 = build_recurrence_issue_plan(
    policy=policy, generation=2, parents=activation.active_parents,
    root_predicate=root, target_label="out", query_ref=query,
    condition_predicates=q2, previous_plan=p1,
    parent_resolver=resolver, release_refs=(source["release_ref"],),
)
assert p2.predecessor_plan_ref == expected_predecessor
g2 = _run(source, qauth, p2, 2, [root] + [p for _, _, p in q1]
          + [p for _, _, p in q2]
          + [parent.predicate for parent in activation.active_parents])
print(json.dumps({
    "bundle_ref": bundle_ref.as_dict(),
    "loaded_count": len(loaded),
    "predecessor_plan_ref": p2.predecessor_plan_ref,
    "no_drop_ok": g2.anti_join["no_drop_ok"],
}, sort_keys=True))
"""
    env = dict(os.environ)
    env["PYTHONPATH"] = (
        str(REPO_ROOT) + os.pathsep + str(Path(__file__).resolve().parent)
        + os.pathsep + env.get("PYTHONPATH", "")
    )
    proc = subprocess.run(
        [sys.executable, "-c", code, str(path), p1.content_hash],
        cwd=str(REPO_ROOT), env=env, capture_output=True, text=True, timeout=180,
    )
    assert proc.returncode == 0, proc.stderr[-3000:]
    child = json.loads(proc.stdout)
    assert child["bundle_ref"] == bundle_ref.as_dict()
    assert child["loaded_count"] == len(g1.execution.handoffs)
    assert child["predecessor_plan_ref"] == p1.content_hash
    assert child["no_drop_ok"] is True
