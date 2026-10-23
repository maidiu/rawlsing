"""R61-R01V R2 reviewer hostile probes (disposable, below own return root).

Oracle: frozen EXPECTATIONS.md, CONTRACTS Revision 2, R01V R2 commission.
Candidate output/receipts are never used to derive the expected identity sets.
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
from rawlsing_next.universal_grammar.enumerate import enumerate_frontier
from rawlsing_next.universal_grammar.native_map import (
    NATIVE_UNSUPPORTED, SUPPORTED, NativeCatalog, lower_frontier,
    lower_operation, native_receipt_anti_join,
)
from rawlsing_next.universal_grammar.types import (
    ELIGIBLE, OccurrenceKey, typed_value_key,
)

REPO_ROOT = Path(__file__).resolve().parents[5]
PROBE_DIR = Path(__file__).resolve().parent


def _author_fixtures():
    from rawlsing_next.tests.test_universal_grammar import (
        _inventory, _native_catalog, _native_fixture,
        _occurrence, _policy,
    )
    return _inventory, _native_catalog, _native_fixture, _occurrence, _policy


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


def _issue_plan(labels):
    _inventory, _native_catalog, _native_fixture, _occurrence, _policy = _author_fixtures()
    source, qauth, dauth, all_predicate, predicates, queries, labels = _native_fixture()
    inv = _inventory(tuple(_occurrence(label) for label in labels))
    policy = _policy(j=2, k=2, d=1)
    frontier = enumerate_frontier(inv, policy)
    selected = tuple(
        op for op in frontier.operations
        if op.disposition == ELIGIBLE and op.measure_id == "SAMPLE"
        and op.claim_class in {"DIST", "CONDITIONAL"}
        and tuple(key.item_id for key in op.targets) == (labels[0],)
        and all(key.item_id in labels for key, _ in op.conditions)
        and len(op.conditions) <= 1
    )
    assert selected
    catalog = _native_catalog(
        labels, all_predicate, predicates, queries,
        discovery_authority_ref=dauth.authority_ref,
    )
    plan = lower_frontier(inv, policy, replace(frontier, operations=selected), catalog)
    return source, qauth, dauth, predicates, queries, all_predicate, plan, catalog


def _compile_expected(plan, catalog):
    grammar = plan.native_grammar()
    atoms = {}
    for item in grammar["atoms"]:
        ref = exact_ref(item["predicate_ref"])
        atoms[item["atom_id"]] = _Atom(
            item["atom_id"], "RESPONSE", catalog.predicate_objects[ref.key], ()
        )
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


def _native_case():
    source, qauth, dauth, predicates, queries, all_predicate, plan, catalog = _issue_plan(
        ("q_alpha", "q_beta", "q_gamma")
    )
    grammar, expected = _compile_expected(plan, catalog)
    baseline = execute_exact_bounded_discovery(
        repository=source["repo"], discovery_authority=_discovery_authority(source, grammar, dauth),
        authority_registry=_i05_registry(source, qauth, dauth),
        release_refs=(source["release_ref"],),
        predicate_catalog=tuple(predicates.values()) + (all_predicate,),
        query_template_catalog=tuple(queries.values()),
    )
    baseline_join = _join(expected, baseline.receipts)

    mutated = deepcopy(grammar)
    atoms = list(mutated["atoms"])
    zero = predicates[("q_beta", 0)].ref.as_dict()
    one = predicates[("q_beta", 1)].ref.as_dict()
    changed = False
    for index, atom in enumerate(atoms):
        if atom["predicate_ref"] == zero:
            atoms[index] = {**atom, "predicate_ref": one}
            changed = True
            break
    assert changed
    mutated["atoms"] = tuple(atoms)
    mutated_result = execute_exact_bounded_discovery(
        repository=source["repo"], discovery_authority=_discovery_authority(source, mutated, dauth),
        authority_registry=_i05_registry(source, qauth, dauth),
        release_refs=(source["release_ref"],),
        predicate_catalog=tuple(predicates.values()) + (all_predicate,),
        query_template_catalog=tuple(queries.values(),),
    )
    mutated_join = _join(expected, mutated_result.receipts)
    candidate_join = native_receipt_anti_join(plan, mutated_result.receipts)
    restored_join = _join(expected, baseline.receipts)
    return {
        "expected_ids": sorted(baseline_join["expected_ids"]),
        "baseline_actual_ids": sorted(baseline_join["actual_ids"]),
        "baseline_ok": baseline_join["ok"],
        "mutated_actual_ids": sorted(mutated_join["actual_ids"]),
        "mutated_missing": list(mutated_join["missing"]),
        "mutated_unexpected": list(mutated_join["unexpected"]),
        "mutated_ok": mutated_join["ok"],
        "candidate_join_no_drop": candidate_join["no_drop_ok"],
        "restored_ok": restored_join["ok"],
    }


def test_native_condition_mutation_refusal_and_restoration_with_own_oracle():
    case = _native_case()
    assert case["baseline_ok"] is True
    assert case["mutated_ok"] is False
    assert case["mutated_missing"] or case["mutated_unexpected"]
    assert case["candidate_join_no_drop"] is False
    assert case["restored_ok"] is True


def test_native_case_is_cold_deterministic():
    local = _native_case()
    code = (
        "import json, sys; sys.path.insert(0, %r);"
        "from test_r01v_r2_reviewer import _native_case;"
        "print(json.dumps(_native_case(), sort_keys=True))"
    ) % str(PROBE_DIR)
    env = dict(os.environ, PYTHONPATH=str(REPO_ROOT) + os.pathsep + str(PROBE_DIR),
               PYTHONDONTWRITEBYTECODE="1")
    proc = subprocess.run(
        [sys.executable, "-c", code], cwd=str(REPO_ROOT), env=env,
        capture_output=True, text=True, timeout=180,
    )
    assert proc.returncode == 0, proc.stderr[-3000:]
    cold = json.loads(proc.stdout)
    assert cold == local


def test_conditional_joint_condition_has_native_semantic_role():
    _inventory, _native_catalog, _native_fixture, _occurrence, _policy = _author_fixtures()
    source, qauth, dauth, all_predicate, predicates, queries, labels = _native_fixture()
    inv = _inventory(tuple(_occurrence(label) for label in labels))
    policy = _policy(j=2, k=1, d=0)
    frontier = enumerate_frontier(inv, policy)
    op = next(
        op for op in frontier.operations
        if op.claim_class == "JOINT" and op.disposition == ELIGIBLE
        and op.measure_id == "SAMPLE"
        and tuple(key.item_id for key in op.targets) == (labels[0], labels[1])
        and len(op.conditions) == 1
    )
    key, value = op.conditions[0]
    catalog = _native_catalog(
        labels, all_predicate, predicates, queries,
        discovery_authority_ref=dauth.authority_ref,
    )
    plan = lower_frontier(inv, policy, replace(frontier, operations=(op,)), catalog)
    record = plan.records[0]
    assert record.status == SUPPORTED, record.reason
    condition_ref = catalog.predicate_ref(key, value).as_dict()
    rule = record.rule or {}
    # Required: if the joint family is claimed supported, the exact condition
    # must be part of the executed candidate semantics, or the record must be a
    # typed refusal.  Merely carrying an unused atom entry is not binding.
    rule_atom_ids = set()
    for name in ("baseline_atom_id", "atom_ids"):
        value_field = rule.get(name)
        if isinstance(value_field, str):
            rule_atom_ids.add(value_field)
        elif isinstance(value_field, (list, tuple)):
            rule_atom_ids.update(value_field)
    for group in rule.get("atom_groups", ()):
        if isinstance(group, (list, tuple)):
            rule_atom_ids.update(group)
        else:
            rule_atom_ids.add(group)
    rule_atom_refs = []
    for atom_id in rule_atom_ids:
        if isinstance(atom_id, str) and atom_id in record.atoms:
            rule_atom_refs.append(canonicalize(dict(record.atoms[atom_id])))
    role_refs = _query_role_predicate_refs(record)
    referenced = condition_ref in rule_atom_refs or condition_ref in role_refs
    assert referenced, (
        "conditional JOINT lowered SUPPORTED but its exact condition value is "
        f"not referenced by the native rule/query roles: status={record.status} "
        f"reason={record.reason} rule_keys={sorted(rule)} "
        f"coverage_roles={record.coverage_roles} "
        f"unused_atoms={sorted(record.atoms)}"
    )


def _query_role_predicate_refs(record):
    refs = []
    for role in record.query_role_refs:
        ref = role.get("predicate_ref")
        if ref is not None:
            refs.append(canonicalize(dict(ref)))
    return refs


def test_forged_operation_id_is_not_accepted_as_exact_identity():
    _inventory, _native_catalog, _native_fixture, _occurrence, _policy = _author_fixtures()
    source, qauth, dauth, all_predicate, predicates, queries, labels = _native_fixture()
    inv = _inventory((_occurrence(labels[0], conditioner_role=None),))
    policy = _policy(j=1, k=0, d=0)
    frontier = enumerate_frontier(inv, policy)
    op = next(
        o for o in frontier.operations
        if o.claim_class == "DIST" and o.disposition == ELIGIBLE
        and o.measure_id == "SAMPLE"
    )
    catalog = _native_catalog(
        labels, all_predicate, predicates, queries,
        discovery_authority_ref=dauth.authority_ref,
    )
    forged = replace(op, op_id="urn:r61:op:forged-identity")
    record = lower_operation(inv, policy, forged, catalog)
    assert record.status == NATIVE_UNSUPPORTED, (
        "lowering accepted an operation whose op_id is not its canonical "
        f"identity: status={record.status} reason={record.reason}"
    )


def test_unsupported_only_frontier_is_not_declared_valid_empty():
    _inventory, _native_catalog, _native_fixture, _occurrence, _policy = _author_fixtures()
    source, qauth, dauth, all_predicate, predicates, queries, labels = _native_fixture()
    inv = _inventory((_occurrence(labels[0], conditioner_role=None),))
    policy = _policy(j=1, k=0, d=0)
    frontier = enumerate_frontier(inv, policy)
    catalog = replace(
        _native_catalog(labels, all_predicate, predicates, queries),
        supported_claims=(),
    )
    plan = lower_frontier(inv, policy, frontier, catalog)
    assert plan.unsupported_operation_ids
    assert plan.native_grammar()["allow_empty_frontier"] is False, (
        "a frontier with unsupported scientific operations was advertised as a "
        "valid empty native frontier"
    )


if __name__ == "__main__":
    print(json.dumps(_native_case(), sort_keys=True))
