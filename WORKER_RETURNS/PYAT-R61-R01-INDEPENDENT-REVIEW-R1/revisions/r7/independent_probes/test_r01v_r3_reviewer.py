"""R61-R01V R3 reviewer hostile probes (disposable, below own return root).

Oracle: frozen EXPECTATIONS.md, CONTRACTS Revision 2, R01V R3 commission.
Candidate output/receipts never define the expected identity sets.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from rawlsing_next.pre553_discovery_exact import (
    _Atom, _Template, _compile_frontier, execute_exact_bounded_discovery,
)
from rawlsing_next.pre553_empirical_objects import canonicalize, exact_ref
from rawlsing_next.tests.test_pre553_discovery_exact import (
    _d_auth, _discovery_authority, _registry as _i05_registry,
)
from rawlsing_next.tests.test_universal_grammar import (
    _frontier, _inventory, _native_catalog, _native_fixture, _occurrence,
    _policy, _tiny_inventory,
)
from rawlsing_next.universal_grammar.enumerate import enumerate_frontier
from rawlsing_next.universal_grammar.native_map import (
    NATIVE_UNSUPPORTED, SUPPORTED, NativeCatalog, lower_frontier,
    lower_operation, native_receipt_anti_join,
)
from rawlsing_next.universal_grammar.types import (
    ELIGIBLE, DirectionGrant, OccurrenceKey, typed_value_key,
)

REPO_ROOT = Path(__file__).resolve().parents[5]
PROBE_DIR = Path(__file__).resolve().parent


def _join(expected, receipts):
    """Reviewer-owned exact anti-join over actual receipt candidate identities."""
    def material(receipt):
        identity = receipt.candidate_identity
        roles = [
            {
                "role": role["role"],
                "predicate_ref": exact_ref(role["predicate_ref"]).as_dict(),
                "query_ref": exact_ref(role["query_ref"]).as_dict(),
            }
            for role in identity["query_roles"]
        ]
        return {
            "candidate_id": identity["candidate_id"],
            "candidate_hash": identity["candidate_hash"],
            "family": identity["family"],
            "rule_id": identity["rule_id"],
            "winning_predicate_ref": exact_ref(
                receipt.winning_predicate_ref
            ).as_dict(),
            "query_roles": roles,
            "validation": canonicalize(identity["validation"]),
            "ancestry_refs": [
                exact_ref(ref).as_dict()
                for ref in receipt.branch_or_parent_ancestry_refs
            ],
        }

    expected_by_id = {candidate["candidate_id"]: candidate for candidate in expected}
    actual_list = [material(receipt) for receipt in receipts]
    actual_by_id = {}
    duplicates = []
    mismatches = []
    for actual in actual_list:
        cid = actual["candidate_id"]
        if cid in actual_by_id:
            duplicates.append(cid)
            continue
        actual_by_id[cid] = actual
        if cid in expected_by_id and canonicalize(expected_by_id[cid]) != canonicalize(actual):
            mismatches.append(cid)
    return {
        "expected_ids": set(expected_by_id),
        "actual_ids": set(actual_by_id),
        "missing": tuple(sorted(set(expected_by_id) - set(actual_by_id))),
        "unexpected": tuple(sorted(set(actual_by_id) - set(expected_by_id))),
        "duplicates": tuple(sorted(duplicates)),
        "semantic_mismatches": tuple(sorted(mismatches)),
        "ok": (
            set(expected_by_id) == set(actual_by_id)
            and not duplicates and not mismatches
        ),
    }


def _derived_objects(plan):
    result = {}
    for record in plan.records:
        result.update(record.derived_predicates)
    return result


def _compile_expected(plan, catalog):
    grammar = plan.native_grammar()
    derived = _derived_objects(plan)
    atoms = {}
    for item in grammar["atoms"]:
        ref = exact_ref(item["predicate_ref"])
        obj = derived.get(item["atom_id"]) or catalog.predicate_objects[ref.key]
        atoms[item["atom_id"]] = _Atom(item["atom_id"], "RESPONSE", obj, ())
    templates = {}
    for item in grammar["query_templates"]:
        ref = exact_ref(item["query_ref"])
        templates[item["template_id"]] = _Template(
            item["template_id"], catalog.query_objects[ref.key]
        )
    compiled = _compile_frontier(grammar, atoms, templates)
    return grammar, tuple({
        "candidate_id": c.candidate_id,
        "candidate_hash": c.candidate_hash,
        "family": c.family,
        "rule_id": c.rule_id,
        "winning_predicate_ref": c.winning_predicate.ref.as_dict(),
        "query_roles": [
            {
                "role": role.role,
                "predicate_ref": role.predicate.ref.as_dict(),
                "query_ref": role.query.ref.as_dict(),
            }
            for role in c.query_roles
        ],
        "validation": canonicalize(c.validation),
        "ancestry_refs": [ref.as_dict() for ref in c.ancestry_refs],
    } for c in compiled)


def _execute(source, qauth, dauth, predicates, all_predicate, queries, grammar, extra=()):
    catalog = {}
    for predicate in tuple(predicates.values()) + (all_predicate,) + tuple(extra):
        catalog[exact_ref(predicate.ref).key] = predicate
    return execute_exact_bounded_discovery(
        repository=source["repo"],
        discovery_authority=_discovery_authority(source, grammar, dauth),
        authority_registry=_i05_registry(source, qauth, dauth),
        release_refs=(source["release_ref"],),
        predicate_catalog=tuple(catalog.values()),
        query_template_catalog=tuple(queries.values()),
    )


def _conditioned_joint_case():
    source, qauth, dauth, all_predicate, predicates, queries, labels = _native_fixture()
    inventory = _inventory(tuple(_occurrence(label) for label in labels))
    policy = _policy(j=2, k=1, d=0)
    frontier = _frontier(inventory, policy)
    selected = tuple(
        op for op in frontier.operations
        if op.disposition == ELIGIBLE and op.measure_id == "SAMPLE"
        and op.claim_class in {"JOINT", "CO_TRAVEL"}
        and tuple(key.item_id for key in op.targets) == (labels[0], labels[1])
        and len(op.conditions) == 1
        and op.conditions[0][0].item_id in labels[2:4]
    )
    assert len(selected) == 8
    catalog = _native_catalog(
        labels, all_predicate, predicates, queries,
        discovery_authority_ref=dauth.authority_ref,
    )
    plan = lower_frontier(inventory, policy, replace(frontier, operations=selected), catalog)
    grammar, expected = _compile_expected(plan, catalog)
    derived = _derived_objects(plan)
    baseline = _execute(
        source, qauth, dauth, predicates, all_predicate, queries, grammar,
        derived.values(),
    )
    baseline_join = _join(expected, baseline.receipts)
    candidate_join = native_receipt_anti_join(plan, baseline.receipts)

    mutated = deepcopy(grammar)
    atoms = list(mutated["atoms"])
    changed = False
    for index, atom in enumerate(atoms):
        if atom["atom_id"] in derived:
            old = exact_ref(atom["predicate_ref"])
            replacement = next(
                obj.ref for (label, value), obj in predicates.items()
                if (label, value) == (labels[2], 1) and exact_ref(obj.ref).key != old.key
            )
            atoms[index] = {**atom, "predicate_ref": replacement.as_dict()}
            changed = True
            break
    assert changed
    mutated["atoms"] = tuple(atoms)
    mutated_result = _execute(
        source, qauth, dauth, predicates, all_predicate, queries, mutated,
        derived.values(),
    )
    mutated_join = _join(expected, mutated_result.receipts)
    candidate_mutated_join = native_receipt_anti_join(plan, mutated_result.receipts)
    restored_join = _join(expected, baseline.receipts)
    return {
        "expected_ids": sorted(baseline_join["expected_ids"]),
        "baseline_actual_ids": sorted(baseline_join["actual_ids"]),
        "baseline_ok": baseline_join["ok"],
        "candidate_join_no_drop": candidate_join["no_drop_ok"],
        "derived_refs": sorted(
            exact_ref(predicate.ref).key for predicate in derived.values()
        ),
        "all_baseline_ref": all_predicate.ref.key,
        "mutated_ok": mutated_join["ok"],
        "mutated_missing": list(mutated_join["missing"]),
        "mutated_unexpected": list(mutated_join["unexpected"]),
        "candidate_mutated_no_drop": candidate_mutated_join["no_drop_ok"],
        "restored_ok": restored_join["ok"],
    }


# ---------------------------------------------------------------- A1
def test_A1_conditioned_joint_cotravel_bind_exact_condition_roles():
    case = _conditioned_joint_case()
    assert case["baseline_ok"] is True, case
    assert case["candidate_join_no_drop"] is True, case
    assert case["mutated_ok"] is False, case
    assert case["mutated_missing"] or case["mutated_unexpected"]
    assert case["candidate_mutated_no_drop"] is False, case
    assert case["restored_ok"] is True, case
    assert case["all_baseline_ref"] not in case["derived_refs"]


def test_A1_condition_values_differ_in_derived_predicate_and_candidates():
    source, qauth, dauth, all_predicate, predicates, queries, labels = _native_fixture()
    inventory = _inventory(tuple(_occurrence(label) for label in labels))
    policy = _policy(j=2, k=1, d=0)
    frontier = _frontier(inventory, policy)
    selected = tuple(
        op for op in frontier.operations
        if op.disposition == ELIGIBLE and op.measure_id == "SAMPLE"
        and op.claim_class in {"JOINT", "CO_TRAVEL"}
        and tuple(key.item_id for key in op.targets) == (labels[0], labels[1])
        and len(op.conditions) == 1
        and op.conditions[0][0].item_id in labels[2:4]
    )
    catalog = _native_catalog(
        labels, all_predicate, predicates, queries,
        discovery_authority_ref=dauth.authority_ref,
    )
    plan = lower_frontier(inventory, policy, replace(frontier, operations=selected), catalog)
    assert all(record.status == SUPPORTED for record in plan.records)
    by_value = {}
    for record in plan.records:
        operation = next(op for op in selected if op.op_id == record.operation_id)
        value = typed_value_key(operation.conditions[0][1])
        by_value.setdefault(value, set()).update(record.derived_predicates)
    assert set(by_value) == {typed_value_key(0), typed_value_key(1)}
    assert by_value[typed_value_key(0)].isdisjoint(by_value[typed_value_key(1)])
    grammar, expected = _compile_expected(plan, catalog)
    assert len({candidate["candidate_id"] for candidate in expected}) == len(selected)


def test_A1_multiple_conditioners_are_and_bound_and_execute():
    source, qauth, dauth, all_predicate, predicates, queries, labels = _native_fixture()
    inventory = _inventory(tuple(_occurrence(label) for label in labels))
    policy = _policy(j=2, k=2, d=0)
    policy = replace(
        policy,
        direction_grants=policy.direction_grants + (
            DirectionGrant(
                ("OUTCOME", "OUTCOME"), ("EXPOSURE", "EXPOSURE"),
                "JOINT", "DIR-JOINT-COND2-REVIEW",
            ),
        ),
    )
    frontier = _frontier(inventory, policy)
    selected = tuple(
        op for op in frontier.operations
        if op.disposition == ELIGIBLE and op.measure_id == "SAMPLE"
        and op.claim_class == "JOINT"
        and tuple(key.item_id for key in op.targets) == (labels[0], labels[1])
        and len(op.conditions) == 2
        and {key.item_id for key, _ in op.conditions} == {labels[2], labels[3]}
    )
    assert selected
    catalog = _native_catalog(
        labels, all_predicate, predicates, queries,
        discovery_authority_ref=dauth.authority_ref,
    )
    plan = lower_frontier(inventory, policy, replace(frontier, operations=selected), catalog)
    assert all(record.status == SUPPORTED for record in plan.records), [
        (record.operation_id, record.status, record.reason) for record in plan.records
    ]
    for record in plan.records:
        assert len(record.derived_predicates) == 1
        derived_ref = next(iter(record.derived_predicates.values())).ref.key
        assert derived_ref not in {
            predicates[(labels[2], 0)].ref.key,
            predicates[(labels[2], 1)].ref.key,
            predicates[(labels[3], 0)].ref.key,
            predicates[(labels[3], 1)].ref.key,
        }
    grammar, expected = _compile_expected(plan, catalog)
    result = _execute(
        source, qauth, dauth, predicates, all_predicate, queries, grammar,
        _derived_objects(plan).values(),
    )
    assert _join(expected, result.receipts)["ok"] is True
    assert native_receipt_anti_join(plan, result.receipts)["no_drop_ok"] is True


def test_A1_renamed_identities_preserve_condition_logic_without_value_pruning():
    from prior_test_r01v_independent import (
        _frontier as prior_frontier,
        _inventory as prior_inventory,
        _occ as prior_occurrence,
        _policy as prior_policy,
    )

    def shape(frontier, mapping):
        return {
            (
                op.claim_class,
                tuple(mapping[key.item_id] for key in op.targets),
                tuple((mapping[key.item_id], typed_value_key(value))
                      for key, value in op.conditions),
            )
            for op in frontier.operations if op.disposition == ELIGIBLE
        }

    original = prior_frontier(prior_inventory((
        prior_occurrence("alpha", conditioner_role=None),
        prior_occurrence("beta", conditioner_role=None),
        prior_occurrence("gamma", target_role=None),
    )), prior_policy(j=2, k=1, d=0))
    renamed = prior_frontier(prior_inventory((
        prior_occurrence("zeta", conditioner_role=None),
        prior_occurrence("eta", conditioner_role=None),
        prior_occurrence("theta", target_role=None),
    )), prior_policy(j=2, k=1, d=0))
    assert shape(original, {"alpha": "alpha", "beta": "beta", "gamma": "gamma"}) == shape(
        renamed, {"zeta": "alpha", "eta": "beta", "theta": "gamma"}
    )
    import inspect
    parameters = inspect.signature(enumerate_frontier).parameters
    assert "values" not in parameters and "observations" not in parameters


def test_A1_case_is_cold_deterministic():
    local = _conditioned_joint_case()
    code = (
        "import json, sys; sys.path.insert(0, %r);"
        "from test_r01v_r3_reviewer import _conditioned_joint_case;"
        "print(json.dumps(_conditioned_joint_case(), sort_keys=True))"
    ) % str(PROBE_DIR)
    env = dict(
        os.environ, PYTHONPATH=str(REPO_ROOT) + os.pathsep + str(PROBE_DIR),
        PYTHONDONTWRITEBYTECODE="1",
    )
    proc = subprocess.run(
        [sys.executable, "-c", code], cwd=str(REPO_ROOT), env=env,
        capture_output=True, text=True, timeout=180,
    )
    assert proc.returncode == 0, proc.stderr[-3000:]
    cold = json.loads(proc.stdout)
    assert cold == local


# ---------------------------------------------------------------- A2
def _one_dist():
    source, qauth, dauth, all_predicate, predicates, queries, labels = _native_fixture()
    inventory = _inventory((_occurrence(labels[0]),))
    policy = _policy(j=1, k=0, d=0)
    frontier = _frontier(inventory, policy)
    op = next(
        o for o in frontier.operations
        if o.claim_class == "DIST" and o.disposition == ELIGIBLE
        and o.measure_id == "SAMPLE"
    )
    catalog = _native_catalog(
        labels, all_predicate, predicates, queries,
        discovery_authority_ref=dauth.authority_ref,
    )
    return inventory, policy, op, catalog


def test_A2_forged_operation_id_is_typed_refused():
    inventory, policy, op, catalog = _one_dist()
    forged = replace(op, op_id="urn:r61:op:forged-identity")
    record = lower_operation(inventory, policy, forged, catalog)
    assert record.status == NATIVE_UNSUPPORTED
    assert record.typed_refusal is not None
    assert record.reason == "OPERATION_ID_NOT_CANONICAL"


def test_A2_semantic_change_with_stale_id_refused_then_recomputed_positive():
    source, qauth, dauth, all_predicate, predicates, queries, labels = _native_fixture()
    inventory = _inventory(tuple(_occurrence(label) for label in labels))
    policy = _policy(j=2, k=1, d=0)
    frontier = _frontier(inventory, policy)
    op = next(
        o for o in frontier.operations
        if o.disposition == ELIGIBLE and o.claim_class == "JOINT"
        and tuple(key.item_id for key in o.targets) == (labels[0], labels[1])
        and len(o.conditions) == 1 and o.conditions[0][0].item_id == labels[2]
    )
    catalog = _native_catalog(
        labels, all_predicate, predicates, queries,
        discovery_authority_ref=dauth.authority_ref,
    )
    old = op.conditions[0][1]
    new = 1 if old == 0 else 0
    stale = replace(op, conditions=((op.conditions[0][0], new),))
    assert stale.op_id == op.op_id
    stale_record = lower_operation(inventory, policy, stale, catalog)
    assert stale_record.status == NATIVE_UNSUPPORTED, (
        "semantic change with stale op_id was accepted: "
        f"{stale_record.status}/{stale_record.reason}"
    )
    assert stale_record.typed_refusal is not None
    recomputed = replace(stale, op_id="urn:r61:op:" + stale.canonical_hash)
    positive = lower_operation(inventory, policy, recomputed, catalog)
    assert positive.status == SUPPORTED, positive.reason


# ---------------------------------------------------------------- A3
def _empty_catalog():
    return NativeCatalog(
        catalog_ref="urn:r61:review:empty-catalog",
        baseline_predicate_ref=None,
        predicate_refs={}, query_refs={}, joint_query_refs={},
        marginal_query_refs={}, supported_claims=(),
        supported_topologies=("SCALAR_SINGULAR",),
        supported_condition_modes=("AND",), maximum_target_arity=1,
        maximum_conditioner_arity=0,
    )


def test_A3_unsupported_only_and_truly_empty_and_pending_are_distinct():
    source, qauth, dauth, all_predicate, predicates, queries, labels = _native_fixture()
    inventory = _inventory((_occurrence(labels[0]),))
    policy = _policy(j=1, k=0, d=0)
    frontier = _frontier(inventory, policy)
    catalog = replace(
        _native_catalog(labels, all_predicate, predicates, queries),
        supported_claims=(),
    )
    unsupported_plan = lower_frontier(inventory, policy, frontier, catalog)
    assert unsupported_plan.unsupported_operation_ids
    assert unsupported_plan.native_grammar()["allow_empty_frontier"] is False
    assert set(unsupported_plan.unsupported_operation_ids) == {
        op.op_id for op in frontier.operations if op.disposition == ELIGIBLE
    }
    assert {record.operation_id for record in unsupported_plan.records} == {
        op.op_id for op in frontier.operations
    }
    report = unsupported_plan.coverage_report()
    assert report["no_drop_ok"] is True
    assert report["disjoint_partition"] is True

    empty_inventory = _inventory((
        _occurrence("admin_only", target_role=None, conditioner_role=None,
                    administrative_role="IDENTITY"),
    ))
    empty_frontier = _frontier(empty_inventory, policy)
    assert empty_frontier.operations == ()
    empty_plan = lower_frontier(empty_inventory, policy, empty_frontier, _empty_catalog())
    assert empty_plan.native_grammar()["allow_empty_frontier"] is True
    assert empty_plan.records == ()

    pending_frontier = _frontier(_tiny_inventory(), _policy(j=1, k=1, d=0), budget=1)
    assert pending_frontier.pending_operation_ids
    assert pending_frontier.operations
    pending_plan = lower_frontier(
        _tiny_inventory(), _policy(j=1, k=1, d=0), pending_frontier, _empty_catalog()
    )
    assert pending_plan.native_grammar()["allow_empty_frontier"] is False


def test_A3_partitions_conserve_all_operation_identities():
    source, qauth, dauth, all_predicate, predicates, queries, labels = _native_fixture()
    inventory = _inventory(tuple(_occurrence(label) for label in labels))
    policy = _policy(j=2, k=1, d=0)
    frontier = _frontier(inventory, policy)
    catalog = _native_catalog(
        labels, all_predicate, predicates, queries,
        discovery_authority_ref=dauth.authority_ref,
    )
    plan = lower_frontier(inventory, policy, frontier, catalog)
    record_ids = {record.operation_id for record in plan.records}
    assert record_ids == {op.op_id for op in frontier.operations}
    report = plan.coverage_report()
    assert report["record_count"] == len(frontier.operations)
    assert report["supported_count"] + report["unsupported_count"] + report["not_eligible_count"] == len(frontier.operations)
    assert report["disjoint_partition"] is True


# ---------------------------------------------------------------- A4
def test_A4_recursion_and_baseline_are_not_conditioner_depth_alias():
    inventory = _inventory((
        _occurrence("alpha"),
        _occurrence("beta", target_role=None),
        _occurrence("gamma", target_role=None),
        _occurrence("delta", target_role=None),
    ))
    policy = replace(
        _policy(j=1, k=3, d=3),
        recursion_relation_ref="REC-REVIEW-1",
        baseline_policy_ref="BASE-REVIEW-1",
    )
    frontier = _frontier(inventory, policy)
    forks = [op for op in frontier.operations if op.claim_class == "FORK"]
    assert forks
    depths = {(op.branch_depth, op.recursion_depth) for op in forks}
    assert all(recursion == 0 for _, recursion in depths)
    assert {branch for branch, _ in depths} == {1, 2}
    assert all(op.baseline_policy_ref == "BASE-REVIEW-1" for op in forks)
    assert all(op.recursion_relation_ref == "REC-REVIEW-1" for op in forks)
    gaps = [
        item for item in frontier.deferred
        if item.get("kind") == "RECURSION_BASELINE_NOT_ENUMERATED"
    ]
    assert len(gaps) == 1
    assert gaps[0]["state"] == "EXACT_CONTRACT_GAP"
    assert gaps[0]["policy_D"] == 3
    assert gaps[0]["recursion_relation_ref"] == "REC-REVIEW-1"
    assert gaps[0]["baseline_policy_ref"] == "BASE-REVIEW-1"
    assert not any(
        op.disposition == "HELD" and "DEPTH_BEYOND_ISSUED_BOUND" in op.reasons
        for op in frontier.operations
    )


if __name__ == "__main__":
    print(json.dumps(_conditioned_joint_case(), sort_keys=True))
