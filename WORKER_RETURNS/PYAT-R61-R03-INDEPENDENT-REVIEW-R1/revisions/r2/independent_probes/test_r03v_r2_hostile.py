"""R03V R2 independent successor hostile probes (TEST_ONLY)."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import inspect
from pathlib import Path

import pytest

from rawlsing_next.pre553_empirical_objects import DiscoveryResultReceipt, semantic_hash
from rawlsing_next.pre553_universal_workload import (
    bind_recursive_workload, compile_governed_frontier, execute_governed_frontier,
    restore_governed_frontier_ledger,
)
from rawlsing_next.tests.test_universal_grammar import _campaign_fixture
from rawlsing_next.tests.test_universal_workload import (
    AS_OF, HOST, PURPOSE, _frontier_bundle, _frontier_fixture,
)
from rawlsing_next.universal_grammar.native_map import native_receipt_anti_join
from rawlsing_next.universal_grammar.types import HELD, UNKNOWN

SNAPSHOT_WRAPPER_MARKER = object()


def _governed(tmp_path):
    bundle, _ = _frontier_bundle(tmp_path / "r03v_r2.sav")
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


def _forge(material):
    material = deepcopy(material)
    material.pop("ledger_hash", None)
    material["ledger_hash"] = semantic_hash(material)
    return material


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


def test_H2_self_consistent_ledger_stripping_must_refuse(tmp_path):
    bundle, inventory, policy, frontier, compilation, result = _governed(tmp_path)
    ledger = result.ledger()
    forged = deepcopy(ledger)
    forged["fact_refs"] = []
    forged["native_facts"] = []
    forged["receipt_refs"] = []
    forged["native_receipts"] = []
    forged["batch_receipt_refs"] = []
    for row in forged["operation_ledger"]:
        row["fact_refs"] = []
        row["receipt_refs"] = []
        row["received_candidate_ids"] = []
        row["candidate_typed_states"] = []
        row["expected_candidate_ids"] = []
    forged = _forge(forged)
    with pytest.raises(Exception):
        restore_governed_frontier_ledger(forged)


def test_H2_live_receipt_fact_removal_must_break_anti_join(tmp_path):
    bundle, inventory, policy, frontier, compilation, result = _governed(tmp_path)
    receipts = result.native_execution.native_result.receipts
    assert native_receipt_anti_join(compilation.plan, receipts)["no_drop_ok"]
    receipt = receipts[0]
    semantic = dict(receipt.semantic_fields)
    semantic["empirical_fact_refs"] = []
    mutated = DiscoveryResultReceipt(
        typed_state=receipt.typed_state,
        authority_snapshot_refs=receipt.authority_snapshot_refs,
        dependency_refs=receipt.dependency_refs,
        producer_replay_locator_or_reference_root=(
            receipt.producer_replay_locator_or_reference_root
        ),
        **semantic,
    )
    altered = (mutated,) + tuple(receipts[1:])
    assert native_receipt_anti_join(compilation.plan, altered)["no_drop_ok"] is False, (
        "removing a native receipt's empirical fact refs did not break the same anti-join"
    )


def test_H3_ledger_must_bind_expected_native_job_identity(tmp_path):
    bundle, inventory, policy, frontier, compilation, result = _governed(tmp_path)
    ledger = result.ledger()
    material = deepcopy(ledger)
    material.pop("ledger_hash", None)
    assert "expected_jobs" in material or any(
        "expected_jobs" in row for row in material["operation_ledger"]
    ), "governed result ledger does not expose expected native job identities"
    assert "expected_candidate_ids" in material["operation_ledger"][0]


def test_H4_recursive_root_release_severance_must_refuse():
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
    snapshot = campaign.snapshot()
    severed = deepcopy(snapshot)
    severed["payload"]["root"]["source_release_refs"] = []
    wrapped = _SnapshotWrapper(severed)
    try:
        binding = bind_recursive_workload(wrapped, execution)
    except Exception:
        return
    assert binding.anti_join["no_drop_ok"] is False, (
        "recursive binding accepted a snapshot with the root source release set removed"
    )


def test_H5_held_unknown_states_remain_typed(tmp_path):
    bundle, inventory, policy, frontier = None, None, None, None
    bundle, _ = _frontier_bundle(tmp_path / "r03v_held.sav")
    inventory, policy, frontier = _frontier_fixture(bundle)
    eligible_ops = [op for op in frontier.operations if op.disposition == "ELIGIBLE"]
    assert len(eligible_ops) >= 2
    held = replace(eligible_ops[0], disposition=HELD, reasons=("R03V_HELD_TEST",))
    unknown = replace(eligible_ops[1], disposition=UNKNOWN, reasons=("R03V_UNKNOWN_TEST",))
    altered_ops = tuple(
        held if op.op_id == held.op_id
        else unknown if op.op_id == unknown.op_id
        else op
        for op in frontier.operations
    )
    altered = replace(frontier, operations=altered_ops)
    compilation = compile_governed_frontier(
        bundle=bundle, inventory=inventory, policy=policy, frontier=altered,
        as_of=AS_OF, host=HOST, purpose=PURPOSE,
    )
    result = execute_governed_frontier(
        compilation=compilation,
        source_factory=lambda _ref: bundle.physical_stream,
    )
    rows = {row["operation_id"]: row for row in result.operation_ledger}
    held_row = rows[held.op_id]
    unknown_row = rows[unknown.op_id]
    assert held_row["reason"] == "FRONTIER_ELIGIBILITY_HELD"
    assert unknown_row["reason"] == "FRONTIER_ELIGIBILITY_UNKNOWN"
    assert held_row["result_state"] == HELD, (
        "held operation is collapsed to a non-held result state"
    )
    assert unknown_row["result_state"] == UNKNOWN, (
        "unknown operation is collapsed to a non-unknown result state"
    )
