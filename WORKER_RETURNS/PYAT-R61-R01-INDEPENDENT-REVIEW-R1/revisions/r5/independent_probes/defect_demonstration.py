"""Record exact candidate behavior for the reviewer's failing refusal probes.

Read-only against candidate code; writes only the reviewer evidence JSON.
"""
from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import sys

PROBE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROBE_DIR))

from test_r01v_r5_reviewer import (  # noqa: E402
    _gen1, _gen2,
)
from rawlsing_next.pre553_empirical_objects import ExactRef  # noqa: E402
from rawlsing_next.tests.test_universal_grammar import (  # noqa: E402
    _condition_predicates,
)
from rawlsing_next.universal_grammar.native_map import (  # noqa: E402
    PARENT_RECEIPT_BOUND, RecurrenceRefusal, _parent_id,
    activate_next_generation, build_recurrence_issue_plan,
    make_recurrence_parent_resolver, make_root_parent,
)

OUT = Path(__file__).resolve().parents[1] / "evidence" / "defect_demonstrations.json"


def _unique(predicates):
    by_key = {}
    for predicate in predicates:
        by_key[predicate.ref.key] = predicate
    return tuple(by_key.values())


def main() -> None:
    result = {}

    # H1: caller strips all ancestry from a canonical receipt-bound parent.
    source, qauth, root, query, policy, root_parent, s1, catalog, p1, g1 = _gen1()
    s2 = _condition_predicates(source, qauth, "s2")
    activation1 = activate_next_generation(
        policy=policy, generation=g1, parents=(root_parent,),
        root_parent=root_parent, next_generation=2, condition_predicates=s2,
    )
    parent = next(
        p for p in activation1.active_parents if p.kind == PARENT_RECEIPT_BOUND
    )
    stripped = replace(parent, ancestry_conditions=(), ancestry_predicates=())
    p2_stripped = build_recurrence_issue_plan(
        policy=policy, generation=2, parents=(stripped,),
        root_predicate=root, target_label="t", query_ref=query,
        condition_predicates=s2, previous_plan=p1,
        parent_resolver=make_recurrence_parent_resolver(g1.execution.handoffs),
        release_refs=(source["release_ref"],),
    )
    g2_stripped = _gen2.__globals__["_run_recurrence_generation"](
        source, qauth, p2_stripped, 2,
        _unique(catalog + [p for _, _, p in s2] + [stripped.predicate]),
    )
    result["H1_ancestry_strip"] = {
        "parent_id_preserved": stripped.parent_id == parent.parent_id,
        "original_ancestry_conditions": len(parent.ancestry_conditions),
        "stripped_ancestry_conditions": len(stripped.ancestry_conditions),
        "issue_accepted": True,
        "execution_anti_join_no_drop_ok": g2_stripped.anti_join["no_drop_ok"],
        "expected_operations": len(p2_stripped.expected_operations),
    }

    # H2: a generation-1 receipt-bound parent relabelled as generation 2.
    (source, qauth, root, query, policy, root_parent, s1, catalog, p1, g1,
     s2, activation1, resolver, p2, g2) = _gen2()
    source_parent = activation1.active_parents[0]
    relabelled = replace(
        source_parent,
        generation=2,
        parent_id=_parent_id(
            PARENT_RECEIPT_BOUND, source_parent.predicate, 2,
            (source_parent.receipt_ref, source_parent.replay_binding_ref),
        ),
    )
    s3 = _condition_predicates(source, qauth, "s3")
    p3 = build_recurrence_issue_plan(
        policy=policy, generation=3, parents=(relabelled,),
        root_predicate=root, target_label="t", query_ref=query,
        condition_predicates=s3, previous_plan=p2,
        parent_resolver=make_recurrence_parent_resolver(
            g1.execution.handoffs + g2.execution.handoffs
        ),
        release_refs=(source["release_ref"],),
    )
    g3 = _gen2.__globals__["_run_recurrence_generation"](
        source, qauth, p3, 3,
        _unique(catalog + [p for _, _, p in s2] + [p for _, _, p in s3]
                + [candidate.predicate for candidate in p2.parents]
                + [relabelled.predicate]),
    )
    result["H2_generation_relabel"] = {
        "actual_producer_generation": 1,
        "relabelled_generation": relabelled.generation,
        "canonical_parent_id_changed": relabelled.parent_id != source_parent.parent_id,
        "issue_accepted_for_generation_3": True,
        "execution_anti_join_no_drop_ok": g3.anti_join["no_drop_ok"],
        "expected_operations": len(p3.expected_operations),
    }

    # H3: execution accepts a plan whose embedded handoff is not the parent binding.
    (source, qauth, root, query, policy, root_parent, s1, catalog, p1, g1,
     s2, activation1, resolver, p2, g2) = _gen2()
    parent = next(
        p for p in p2.parents if p.kind == PARENT_RECEIPT_BOUND
    )
    other = next(
        handoff for handoff in g1.execution.handoffs + g2.execution.handoffs
        if handoff.ref != parent.replay_binding_ref
    )
    tampered = replace(parent, handoff=other)
    tampered_plan = replace(p2, parents=(tampered,))
    g2_tampered = _gen2.__globals__["_run_recurrence_generation"](
        source, qauth, tampered_plan, 2,
        _unique(catalog + [p for _, _, p in s2]
                + [candidate.predicate for candidate in p2.parents]),
    )
    result["H3_execution_binding"] = {
        "declared_replay_binding_matches_embedded_handoff": (
            tampered.replay_binding_ref == other.ref
        ),
        "declared_receipt_matches_embedded_handoff": (
            tampered.receipt_ref == other.receipt_ref
        ),
        "execution_accepted": True,
        "execution_anti_join_no_drop_ok": g2_tampered.anti_join["no_drop_ok"],
    }

    # H4: replace predecessor plan with a self-consistent undercount.
    policy5 = _gen2.__globals__["_recurrence_policy"](total=5, per_generation=4)
    source, qauth, root, query, policy5, root_parent, s1, catalog, p1, g1 = _gen1(policy5)
    fake = replace(
        p1,
        expected_operations=p1.expected_operations[:2],
        cumulative_issued_count=2,
    )
    s2 = _condition_predicates(source, qauth, "s2")
    activation1 = activate_next_generation(
        policy=policy5, generation=g1, parents=(root_parent,),
        root_parent=root_parent, next_generation=2, condition_predicates=s2,
    )
    common = dict(
        policy=policy5, generation=2, parents=activation1.active_parents,
        root_predicate=root, target_label="t", query_ref=query,
        condition_predicates=s2,
        parent_resolver=make_recurrence_parent_resolver(g1.execution.handoffs),
        release_refs=(source["release_ref"],),
    )
    honest = build_recurrence_issue_plan(**common, previous_plan=p1)
    forged = build_recurrence_issue_plan(**common, previous_plan=fake)
    result["H4_predecessor_undercount"] = {
        "real_gen1_issued_operations": len(p1.expected_operations),
        "real_gen1_cumulative": p1.cumulative_issued_count,
        "forged_gen1_declared_cumulative": fake.cumulative_issued_count,
        "forged_predecessor_accepted": True,
        "honest_gen2_issued_operations": len(honest.expected_operations),
        "forged_gen2_issued_operations": len(forged.expected_operations),
        "forged_gen2_predecessor_issued_count": forged.predecessor_issued_count,
    }

    # H5: a zero per-generation cap is not an explicit stopped-budget plan.
    zero_policy = _gen2.__globals__["_recurrence_policy"](per_generation=0)
    source, qauth, root, query = _gen2.__globals__["_recurrence_source"]()
    root_parent = make_root_parent(
        predicate=root, source_release_refs=(source["release_ref"],)
    )
    s1 = _condition_predicates(source, qauth, "s1")
    try:
        build_recurrence_issue_plan(
            policy=zero_policy, generation=1, parents=(root_parent,),
            root_predicate=root, target_label="t", query_ref=query,
            condition_predicates=s1, release_refs=(source["release_ref"],),
        )
        result["H5_zero_per_generation_cap"] = {"returned": "plan"}
    except Exception as exc:  # noqa: BLE001 - record exact candidate behavior
        result["H5_zero_per_generation_cap"] = {
            "returned": type(exc).__name__,
            "message": str(exc),
        }

    # H6: root parent need not be the declared source root.
    source, qauth, root, query = _gen2.__globals__["_recurrence_source"]()
    policy = _gen2.__globals__["_recurrence_policy"]()
    s1 = _condition_predicates(source, qauth, "s1")
    wrong_root_parent = make_root_parent(
        predicate=s1[0][2], source_release_refs=(source["release_ref"],)
    )
    p1_wrong = build_recurrence_issue_plan(
        policy=policy, generation=1, parents=(wrong_root_parent,),
        root_predicate=root, target_label="t", query_ref=query,
        condition_predicates=s1, release_refs=(source["release_ref"],),
    )
    g1_wrong = _gen2.__globals__["_run_recurrence_generation"](
        source, qauth, p1_wrong, 1, [root] + [p for _, _, p in s1]
    )
    result["H6_root_parent_mismatch"] = {
        "root_parent_predicate_matches_declared_root": (
            wrong_root_parent.predicate.ref == root.ref
        ),
        "issue_accepted": True,
        "execution_anti_join_no_drop_ok": g1_wrong.anti_join["no_drop_ok"],
        "expected_operations": len(p1_wrong.expected_operations),
    }

    # H7: activation accepts a next-generation label that is not the next label.
    source, qauth, root, query, policy, root_parent, s1, catalog, p1, g1 = _gen1()
    s2 = _condition_predicates(source, qauth, "s2")
    wrong_activation = activate_next_generation(
        policy=policy, generation=g1, parents=(root_parent,),
        root_parent=root_parent, next_generation=1, condition_predicates=s2,
    )
    p2_from_wrong = build_recurrence_issue_plan(
        policy=policy, generation=2, parents=wrong_activation.active_parents,
        root_predicate=root, target_label="t", query_ref=query,
        condition_predicates=s2, previous_plan=p1,
        parent_resolver=make_recurrence_parent_resolver(g1.execution.handoffs),
        release_refs=(source["release_ref"],),
    )
    result["H7_activation_label"] = {
        "requested_next_generation": 1,
        "activation_generation_returned": wrong_activation.generation,
        "children_labeled_generation": sorted({
            p.generation for p in wrong_activation.active_parents
        }),
        "children_usable_for_generation_2": bool(p2_from_wrong.expected_operations),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
