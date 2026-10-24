"""R03V R3 independent successor hostile probes (TEST_ONLY)."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import inspect
from pathlib import Path

import pytest

from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.pre553_universal_workload import (
    bind_recursive_workload, compile_governed_frontier, execute_governed_frontier,
    restore_governed_frontier_ledger,
)
from rawlsing_next.tests.test_universal_grammar import _campaign_fixture
from rawlsing_next.tests.test_universal_workload import (
    AS_OF, HOST, PURPOSE, _frontier_bundle, _frontier_fixture,
)
from rawlsing_next.universal_grammar.types import HELD, UNKNOWN


def _governed(tmp_path):
    bundle, _ = _frontier_bundle(tmp_path / "r03v_r3.sav")
    inventory, policy, frontier = _frontier_fixture(bundle)
    compilation = compile_governed_frontier(
        bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
        as_of=AS_OF, host=HOST, purpose=PURPOSE,
    )
    result = execute_governed_frontier(
        compilation=compilation,
        source_factory=lambda _ref: bundle.physical_stream,
    )
    return bundle, inventory, policy, frontier, compilation, result


def _forge(ledger, *, rehash_compilation=False):
    ledger = deepcopy(ledger)
    if rehash_compilation:
        ledger["compilation_hash"] = semantic_hash(ledger["compilation"])
    ledger.pop("ledger_hash", None)
    ledger["ledger_hash"] = semantic_hash(ledger)
    return ledger


def _fact_identity(ref):
    return (ref.get("object_id"), ref.get("content_hash"))


def _remove_fact(ledger, target):
    ledger["native_facts"] = [
        fact for fact in ledger["native_facts"]
        if _fact_identity(fact) != target
    ]
    ledger["fact_refs"] = [
        ref for ref in ledger["fact_refs"] if _fact_identity(ref) != target
    ]
    for receipt in ledger["native_receipts"]:
        semantic = receipt.setdefault("semantic_fields", {})
        semantic["empirical_fact_refs"] = [
            ref for ref in semantic.get("empirical_fact_refs", ())
            if _fact_identity(ref) != target
        ]
    for row in ledger["operation_ledger"]:
        row["fact_refs"] = [
            ref for ref in row.get("fact_refs", ())
            if _fact_identity(ref) != target
        ]


def _duplicate_fact(ledger, target):
    fact = next(
        fact for fact in ledger["native_facts"]
        if _fact_identity(fact) == target
    )
    ref = next(
        ref for ref in ledger["fact_refs"]
        if _fact_identity(ref) == target
    )
    ledger["native_facts"].append(deepcopy(fact))
    ledger["fact_refs"].append(deepcopy(ref))
    for receipt in ledger["native_receipts"]:
        semantic = receipt.setdefault("semantic_fields", {})
        refs = semantic.get("empirical_fact_refs", ())
        if any(_fact_identity(item) == target for item in refs):
            semantic["empirical_fact_refs"] = tuple(refs) + (deepcopy(ref),)
            break
    for row in ledger["operation_ledger"]:
        refs = row.get("fact_refs", ())
        if any(_fact_identity(item) == target for item in refs):
            row["fact_refs"] = tuple(refs) + (deepcopy(ref),)
            break


class _SnapshotWrapper:
    def __init__(self, snapshot):
        self._snapshot = snapshot

    def snapshot(self):
        return self._snapshot


def test_H1_governed_frontier_contract_is_present(tmp_path):
    parameters = set(inspect.signature(compile_governed_frontier).parameters)
    assert {"bundle", "inventory", "policy", "frontier"} <= parameters
    bundle, inventory, policy, frontier, compilation, result = _governed(tmp_path)
    classes = {op.claim_class for op in frontier.eligible()}
    assert {"JOINT", "CO_TRAVEL", "CONDITIONAL", "FORK"} <= classes
    assert result.anti_join["no_drop_ok"]


def test_H2_self_consistent_single_fact_removal_must_refuse(tmp_path):
    bundle, inventory, policy, frontier, compilation, result = _governed(tmp_path)
    ledger = result.ledger()
    assert ledger["native_facts"]
    target = _fact_identity(ledger["native_facts"][0])
    _remove_fact(ledger, target)
    forged = _forge(ledger)
    with pytest.raises(Exception):
        restore_governed_frontier_ledger(forged)


def test_H2_self_consistent_fact_duplicate_must_refuse(tmp_path):
    bundle, inventory, policy, frontier, compilation, result = _governed(tmp_path)
    ledger = result.ledger()
    target = _fact_identity(ledger["native_facts"][0])
    _duplicate_fact(ledger, target)
    forged = _forge(ledger)
    with pytest.raises(Exception):
        restore_governed_frontier_ledger(forged)


def test_H3_self_consistent_expected_job_substitution_must_refuse(tmp_path):
    bundle, inventory, policy, frontier, compilation, result = _governed(tmp_path)
    ledger = result.ledger()
    assert ledger["expected_jobs"]
    forged = deepcopy(ledger)
    job = list(forged["expected_jobs"][0])
    job[1] = "urn:forged:query-ref"
    job[2] = "urn:forged:predicate-ref"
    forged["expected_jobs"] = [job]
    forged["compilation"]["issued"]["expected_jobs"] = [job]
    forged = _forge(forged, rehash_compilation=True)
    with pytest.raises(Exception):
        restore_governed_frontier_ledger(forged)


def test_H4_checkpoint_valid_root_release_severance_must_refuse():
    source, _qauth, _root, query, _policy_obj, s1, s2, s3, campaign = (
        _campaign_fixture()
    )
    issuance = campaign.issue(
        parent_lineage_refs=(campaign.root_lineage_ref,),
        condition_refs=tuple((key, value) for key, value, _ in s1),
    )
    execution = campaign.execute(issuance)
    baseline = bind_recursive_workload(campaign, execution)
    assert baseline.anti_join["no_drop_ok"]
    snapshot = deepcopy(campaign.snapshot())
    snapshot["payload"]["root"]["source_release_refs"] = []
    snapshot["checkpoint_ref"] = semantic_hash(snapshot["payload"])
    with pytest.raises(Exception):
        bind_recursive_workload(_SnapshotWrapper(snapshot), execution)


def test_H5_held_unknown_states_remain_typed(tmp_path):
    bundle, _ = _frontier_bundle(tmp_path / "r03v_held_unknown.sav")
    inventory, policy, frontier = _frontier_fixture(bundle)
    eligible_ops = [op for op in frontier.operations if op.disposition == "ELIGIBLE"]
    held = replace(eligible_ops[0], disposition=HELD, reasons=("R03V_HELD_TEST",))
    unknown = replace(eligible_ops[1], disposition=UNKNOWN, reasons=("R03V_UNKNOWN_TEST",))
    altered = replace(frontier, operations=tuple(
        held if op.op_id == held.op_id else
        unknown if op.op_id == unknown.op_id else op
        for op in frontier.operations
    ))
    compilation = compile_governed_frontier(
        bundle=bundle, inventory=inventory, policy=policy, frontier=altered,
        as_of=AS_OF, host=HOST, purpose=PURPOSE,
    )
    result = execute_governed_frontier(
        compilation=compilation,
        source_factory=lambda _ref: bundle.physical_stream,
    )
    rows = {row["operation_id"]: row for row in result.operation_ledger}
    assert rows[held.op_id]["result_state"] == HELD
    assert rows[unknown.op_id]["result_state"] == UNKNOWN
    restored = restore_governed_frontier_ledger(result.ledger())
    restored_rows = {row["operation_id"]: row for row in restored["operation_ledger"]}
    assert restored_rows[held.op_id]["result_state"] == HELD
    assert restored_rows[unknown.op_id]["result_state"] == UNKNOWN
