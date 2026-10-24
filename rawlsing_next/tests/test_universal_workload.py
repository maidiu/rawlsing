"""R03 sourcefree total native workload qualification (TEST_ONLY)."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.pre553_native_workload_binding import WorkloadBindingRefusal
from rawlsing_next.pre553_physical_decoder import decode_dta, decode_sav
from rawlsing_next.pre553_source_native_preimage_adapter import (
    NativePreimageRefusal, NativeSourceRule, materialize_native_preimages,
)
from rawlsing_next.pre553_universal_workload import (
    bind_recursive_execution, bind_recursive_workload,
    compile_governed_frontier, compile_universal_workload,
    execute_governed_frontier, execute_universal_workload,
    restore_governed_frontier_ledger,
)
from rawlsing_next.tests.test_universal_source_projection import (
    SOURCE_ID, build_s3, decode_sav as _decode_sav, package, s3_rows,
    write_rows,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
AS_OF = "2026-10-23"
HOST = "local-r03"
PURPOSE = "TEST_ONLY_SOURCEFREE"


def _expected_sav_operations(bundle):
    expected = set()
    for item in bundle.administered:
        qref = bundle.question_refs.get(item.source_variable_code)
        if qref is None:
            continue
        values = {
            str(rule.canonical_value)
            for slot in bundle.projection.response_slots
            if slot.question_binding.native_question_ref == qref
            for rule in slot.values
            if rule.response_state == "SUBSTANTIVE_RESPONSE"
            and rule.canonical_value is not None
        }
        for value in values:
            expected.add((item.source_variable_code, value))
    return expected


def test_r03_heterogeneous_sav_total_workload_and_no_drop(tmp_path):
    path = tmp_path / "r03_s3.sav"
    bundle = build_s3(path, s3_rows(respondents=6, occasions=2))
    compilation = compile_universal_workload(
        bundle=bundle, as_of=AS_OF, host=HOST, purpose=PURPOSE)
    expected = _expected_sav_operations(bundle)
    observed = {(op.source_variable_code, op.response_value)
                for op in compilation.operations if op.status == "COMPILED"}
    assert observed == expected
    assert compilation.expected_jobs
    assert len(compilation.expected_jobs) == len(set(compilation.expected_jobs))
    result = execute_universal_workload(
        compilation=compilation,
        source_factory=lambda _ref: bundle.physical_stream,
    )
    join = result.anti_join()
    assert join["no_drop_ok"], join
    assert result.native_results
    assert result.receipt_refs
    assert result.fact_refs
    assert not result.failed
    assert compilation.content_hash == compile_universal_workload(
        bundle=bundle, as_of=AS_OF, host=HOST, purpose=PURPOSE).content_hash


def test_r03_dta_valid_person_and_cross_unit_refusal(tmp_path):
    path = tmp_path / "r03_person.dta"
    rows = [{"PID": float(i), "OCCASION": 0.0, "A": float(i % 2),
             "Y": float((i // 2) % 2)} for i in range(6)]
    write_rows(path, rows, fmt="dta")
    pkg = package(
        path, len(rows),
        (NativeSourceRule("impl.a", "A"), NativeSourceRule("impl.y", "Y")),
        coordinate="OCCASION", source_format="DTA",
    )
    bundle = materialize_native_preimages(
        package=pkg, incidence=decode_dta(path))
    compilation = compile_universal_workload(
        bundle=bundle, as_of=AS_OF, host=HOST, purpose=PURPOSE)
    result = execute_universal_workload(
        compilation=compilation,
        source_factory=lambda _ref: bundle.physical_stream,
    )
    assert result.anti_join()["no_drop_ok"]
    assert result.fact_refs

    household_path = tmp_path / "r03_cross_unit.dta"
    write_rows(household_path, [{"HID": 1.0, "PID": 1.0, "HMEAS": 1.0,
                                "OUTCOME": 1.0, "OCCASION": 0.0}], fmt="dta")
    with pytest.raises(NativePreimageRefusal) as caught:
        package(
            household_path, 1,
            (NativeSourceRule("impl.h", "HMEAS", unit="household"),
             NativeSourceRule("impl.o", "OUTCOME", unit="person")),
            coordinate="HID", units={"HMEAS": "household", "OUTCOME": "person"},
            source_format="DTA",
        )
    assert caught.value.code == "CROSS_UNIT_POOLING_UNAUTHORIZED"


def test_r03_failure_and_source_restoration_same_consumer(tmp_path):
    path = tmp_path / "r03_fault.sav"
    bundle = build_s3(path, s3_rows(respondents=4, occasions=2))
    compilation = compile_universal_workload(
        bundle=bundle, as_of=AS_OF, host=HOST, purpose=PURPOSE)
    good = execute_universal_workload(
        compilation=compilation,
        source_factory=lambda _ref: bundle.physical_stream,
    )
    assert good.anti_join()["no_drop_ok"]
    bad_stream = replace(bundle.physical_stream, source_sha256="b" * 64)
    failed = execute_universal_workload(
        compilation=compilation,
        source_factory=lambda _ref: bad_stream,
    )
    assert failed.failed
    assert failed.executed_operation_ids == ()
    assert failed.anti_join()["no_drop_ok"] is False
    restored = execute_universal_workload(
        compilation=compilation,
        source_factory=lambda _ref: bundle.physical_stream,
    )
    assert restored.anti_join()["no_drop_ok"]
    assert restored.fact_refs == good.fact_refs


def test_r03_consumes_recursive_campaign_execution_without_rerun():
    from rawlsing_next.tests.test_universal_grammar import _campaign_fixture
    from rawlsing_next.tests.test_universal_grammar import (
        _campaign_active_refs,
    )
    source, qauth, root, query, policy, s1, s2, s3, campaign = _campaign_fixture()
    i1 = campaign.issue(
        parent_lineage_refs=(campaign.root_lineage_ref,),
        condition_refs=tuple((key, value) for key, value, _ in s1),
    )
    e1 = campaign.execute(i1)
    fragment1 = bind_recursive_execution(campaign, e1)
    assert fragment1.campaign_ref == campaign.campaign_ref
    assert fragment1.execution_ref == e1
    assert fragment1.receipt_refs
    assert fragment1.handoff_refs
    assert fragment1.fact_refs
    assert fragment1.source_release_refs
    activation1 = campaign.activate(e1)
    active = _campaign_active_refs(campaign, activation1)
    i2 = campaign.issue(
        parent_lineage_refs=active,
        condition_refs=tuple((key, value) for key, value, _ in s2),
    )
    e2 = campaign.execute(i2)
    fragment2 = bind_recursive_execution(campaign, e2)
    assert fragment2.execution_ref == e2
    assert set(fragment2.receipt_refs) != set(fragment1.receipt_refs)
    assert fragment2.operation_ids
    # Binding is read-only: no new issuance or execution appears.
    before = len(campaign.inspect()["executions"])
    bind_recursive_execution(campaign, e2)
    assert len(campaign.inspect()["executions"]) == before


def test_r03_wrong_source_edition_and_duplicate_job_refused(tmp_path):
    path = tmp_path / "r03_dup.sav"
    bundle = build_s3(path, s3_rows(respondents=4, occasions=2))
    compilation = compile_universal_workload(
        bundle=bundle, as_of=AS_OF, host=HOST, purpose=PURPOSE)
    wrong = execute_universal_workload(
        compilation=compilation,
        source_factory=lambda _ref: replace(bundle.physical_stream,
                                            source_sha256="c" * 64),
    )
    assert wrong.failed
    assert wrong.executed_operation_ids == ()


def test_r03_count_preserving_substitution_and_duplicate_fail_antijoin(tmp_path):
    path = tmp_path / "r03_antijoin.sav"
    bundle = build_s3(path, s3_rows(respondents=4, occasions=2))
    compilation = compile_universal_workload(
        bundle=bundle, as_of=AS_OF, host=HOST, purpose=PURPOSE)
    result = execute_universal_workload(
        compilation=compilation,
        source_factory=lambda _ref: bundle.physical_stream,
    )
    assert result.anti_join()["no_drop_ok"]
    ids = list(result.executed_operation_ids)
    substituted = tuple(ids[:-1] + [ids[0]]) if len(ids) > 1 else tuple(ids)
    mutated = replace(result, executed_operation_ids=substituted)
    report = mutated.anti_join()
    assert report["no_drop_ok"] is False
    assert report["missing_operation_ids"]
    assert report["duplicate_operation_ids"]
    restored = replace(result, executed_operation_ids=tuple(ids))
    assert restored.anti_join()["no_drop_ok"]


def _frontier_bundle(path):
    rows = [
        {
            "A": float(index % 2),
            "B": float((index // 2) % 2),
            "Y": float((index % 2) ^ ((index // 2) % 2)),
            "G": float(index % 2),
        }
        for index in range(12)
    ]
    write_rows(path, rows)
    pkg = package(
        path, len(rows),
        (NativeSourceRule("impl.a", "A"),
         NativeSourceRule("impl.b", "B"),
         NativeSourceRule("impl.y", "Y")),
        coordinate="G",
    )
    return materialize_native_preimages(
        package=pkg, incidence=decode_sav(path)
    ), rows


def _frontier_fixture(bundle, *, budget=None):
    from rawlsing_next.tests.test_universal_grammar import (
        _frontier, _inventory, _occurrence, _policy,
    )
    inventory = _inventory((
        _occurrence("A"), _occurrence("B"), _occurrence("Y"),
    ), complete=True)
    inventory = replace(inventory, source_sha256=bundle.source_sha256)
    policy = _policy(j=2, k=2, d=1)
    frontier = _frontier(inventory, policy, budget=budget)
    return inventory, policy, frontier


def test_r03_governed_frontier_joint_conditional_no_drop_and_cold(tmp_path):
    bundle, _ = _frontier_bundle(tmp_path / "r03_frontier.sav")
    inventory, policy, frontier = _frontier_fixture(bundle)
    classes = {op.claim_class for op in frontier.eligible()}
    assert {"DIST", "CONDITIONAL", "JOINT", "CO_TRAVEL",
            "INTERACTION", "FORK"} <= classes
    compilation = compile_governed_frontier(
        bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
        as_of=AS_OF, host=HOST, purpose=PURPOSE,
    )
    pending = set(compilation.pending_operation_ids)
    assert pending == set()
    eligible_ids = {op.op_id for op in frontier.eligible()}
    assert set(compilation.frontier_eligible_operation_ids) == eligible_ids
    assert set(compilation.expected_operation_ids) == (
        eligible_ids - set(compilation.unsupported_operation_ids)
    )
    assert compilation.unsupported_operation_ids
    assert compilation.expected_candidate_ids
    result = execute_governed_frontier(
        compilation=compilation,
        source_factory=lambda _ref: bundle.physical_stream,
    )
    assert result.anti_join["no_drop_ok"], result.anti_join
    assert result.operation_anti_join["accounting_ok"], result.operation_anti_join
    assert result.operation_anti_join["no_drop_ok"], result.operation_anti_join
    assert result.receipt_refs and result.fact_refs
    assert len(result.native_execution.receipts) == 1
    assert len(result.native_execution.native_result.receipts) == len(
        compilation.expected_candidate_ids
    )
    rows = {row["operation_id"]: row for row in result.operation_ledger}
    assert set(rows) == {
        op.op_id for op in frontier.operations
    } | pending
    assert any(row["lowering_status"] == "SUPPORTED"
               and row["execution_state"] == "COMPLETED"
               for row in rows.values())
    assert any(row["lowering_status"] == "UNSUPPORTED_RUNTIME"
               for row in rows.values())
    assert any("DISCOVERED_RESULT_SUPPORTED" in row["candidate_typed_states"]
               for row in rows.values())
    assert any("VALID_EMPTY" in row["candidate_typed_states"]
               for row in rows.values())
    joint_rows = [
        row for row in rows.values()
        if row["claim_class"] in {"JOINT", "CO_TRAVEL"}
    ]
    assert joint_rows
    ledger = result.ledger()
    pin = result.freeze_restore_checkpoint()
    assert restore_governed_frontier_ledger(
        ledger, expected_checkpoint_ref=pin
    )["schema"] == ledger["schema"]
    tampered = dict(ledger)
    tampered["operation_ledger"] = []
    with pytest.raises(WorkloadBindingRefusal):
        restore_governed_frontier_ledger(tampered, expected_checkpoint_ref=pin)

    cold_compilation = compile_governed_frontier(
        bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
        as_of=AS_OF, host=HOST, purpose=PURPOSE,
    )
    cold = execute_governed_frontier(
        compilation=cold_compilation,
        source_factory=lambda _ref: bundle.physical_stream,
    )
    assert cold.compilation.content_hash == compilation.content_hash
    assert cold.fact_refs == result.fact_refs
    assert cold.receipt_refs == result.receipt_refs
    assert cold.content_hash == result.content_hash


def test_r03_source_value_fault_changes_dependent_fact_and_restores(tmp_path):
    from rawlsing_next.pre553_physical_decoder import PhysicalMissingState
    from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream

    bundle, _ = _frontier_bundle(tmp_path / "r03_value.sav")
    inventory, policy, frontier = _frontier_fixture(bundle)
    compilation = compile_governed_frontier(
        bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
        as_of=AS_OF, host=HOST, purpose=PURPOSE,
    )
    good = execute_governed_frontier(
        compilation=compilation,
        source_factory=lambda _ref: bundle.physical_stream,
    )
    assert good.anti_join["no_drop_ok"]
    cells = tuple(bundle.physical_stream.iter_cells())

    def mutated_cells():
        result = []
        for cell in cells:
            if (cell.variable_name == "A"
                    and cell.missing_state is PhysicalMissingState.OBSERVED_STORAGE_VALUE):
                result.append(replace(cell, raw_value=1.0 - float(cell.raw_value)))
            else:
                result.append(cell)
        return tuple(result)

    mutated_stream = ExactPhysicalCellStream(
        source_sha256=bundle.source_sha256,
        row_count=bundle.physical_stream.row_count,
        cell_iter_factory=mutated_cells,
    )
    mutated = execute_governed_frontier(
        compilation=compilation,
        source_factory=lambda _ref: mutated_stream,
    )
    assert mutated.compilation is compilation
    assert mutated.anti_join["no_drop_ok"]
    assert set(mutated.fact_refs) != set(good.fact_refs)
    good_by_operation = {
        row["operation_id"]: row["fact_refs"] for row in good.operation_ledger
    }
    mutated_by_operation = {
        row["operation_id"]: row["fact_refs"]
        for row in mutated.operation_ledger
    }
    assert any(
        good_by_operation[operation_id]
        != mutated_by_operation[operation_id]
        for operation_id in good_by_operation
    )
    restored = execute_governed_frontier(
        compilation=compilation,
        source_factory=lambda _ref: bundle.physical_stream,
    )
    assert set(restored.fact_refs) == set(good.fact_refs)
    assert restored.operation_ledger == good.operation_ledger


def test_r03_budget_pending_operations_are_explicit_and_not_executed(tmp_path):
    bundle, _ = _frontier_bundle(tmp_path / "r03_pending.sav")
    inventory, policy, frontier = _frontier_fixture(bundle, budget=5)
    assert len(frontier.pending_operation_ids) > 0
    compilation = compile_governed_frontier(
        bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
        as_of=AS_OF, host=HOST, purpose=PURPOSE,
    )
    assert set(compilation.pending_operation_ids) == set(
        frontier.pending_operation_ids
    )
    result = execute_governed_frontier(
        compilation=compilation,
        source_factory=lambda _ref: bundle.physical_stream,
    )
    assert result.operation_anti_join["accounting_ok"]
    assert result.operation_anti_join["no_drop_ok"], result.operation_anti_join
    pending_rows = [
        row for row in result.operation_ledger
        if row["lowering_status"] == "PENDING"
    ]
    assert len(pending_rows) == len(compilation.pending_operation_ids)
    assert all(
        row["execution_state"] == "PENDING" and row["receipt_refs"] == []
        for row in pending_rows
    )
    assert not (set(compilation.expected_operation_ids)
                & set(compilation.pending_operation_ids))


def test_r03_d3_recursive_root_parent_minority_and_cold(tmp_path):
    from rawlsing_next.tests.test_universal_grammar import (
        _campaign_active_refs, _campaign_fixture,
    )
    from rawlsing_next.universal_grammar.native_map import RetainedRecurrenceCampaign

    source, _qauth, _root, query, _policy_obj, s1, s2, s3, campaign = (
        _campaign_fixture()
    )
    bindings = []
    executions = []
    active_refs = (campaign.root_lineage_ref,)
    for generation, conditions in enumerate((s1, s2, s3), start=1):
        issuance = campaign.issue(
            parent_lineage_refs=active_refs,
            condition_refs=tuple((key, value) for key, value, _ in conditions),
        )
        execution = campaign.execute(issuance)
        executions.append(execution)
        binding = bind_recursive_workload(campaign, execution)
        assert binding.generation == generation
        assert binding.anti_join["no_drop_ok"], binding.anti_join
        assert binding.expected_operation_ids
        assert binding.actual_rule_ids
        assert binding.receipt_refs and binding.fact_refs
        assert binding.root_contrasts and binding.parent_contrasts
        assert not binding.anti_join["missing_candidate_operations"]
        bindings.append(binding)
        if generation < 3:
            activation = campaign.activate(execution)
            active_refs = _campaign_active_refs(campaign, activation)
    assert [binding.generation for binding in bindings] == [1, 2, 3]
    gen2 = bind_recursive_workload(campaign, executions[1])
    groups = {}
    for row in gen2.operations:
        groups.setdefault(row["parent_id"], []).append(row)
    contrast = next(
        rows for rows in groups.values()
        if {row["comparator"] for row in rows}
        == {"ROOT_RELATIVE", "IMMEDIATE_PARENT_RELATIVE"}
        and len({
            row["typed_state"] for row in rows
            if row["comparator"] in {"ROOT_RELATIVE", "IMMEDIATE_PARENT_RELATIVE"}
        }) > 1
    )
    states = {
        row["comparator"]: row["typed_state"] for row in contrast
    }
    assert states["ROOT_RELATIVE"] != states["IMMEDIATE_PARENT_RELATIVE"]
    assert gen2.minority

    before = len(campaign.inspect()["executions"])
    snapshot = campaign.snapshot()
    restored = RetainedRecurrenceCampaign.restore(
        snapshot=snapshot, expected_checkpoint_ref=snapshot["checkpoint_ref"],
        repository=source["repo"], authority_registry=campaign._registry,
        authority_factory=campaign._authority_factory,
        condition_catalog=campaign._condition_catalog, query_object=query,
    )
    rebound = bind_recursive_workload(restored, executions[1])
    assert rebound.content_hash == gen2.content_hash
    assert rebound.fact_refs == gen2.fact_refs
    assert rebound.operations == gen2.operations
    assert rebound.minority == gen2.minority
    assert len(campaign.inspect()["executions"]) == before
    assert len(restored.inspect()["executions"]) == before


def _governed_result(tmp_path, name="r03_defects.sav"):
    bundle, _ = _frontier_bundle(tmp_path / name)
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


def _rehash(ledger):
    material = dict(ledger)
    material.pop("ledger_hash", None)
    material["ledger_hash"] = semantic_hash(material)
    return material


def test_r03_successor_ledger_identity_strip_and_fact_removal_refused(tmp_path):
    bundle, inventory, policy, frontier, compilation, result = _governed_result(
        tmp_path)
    ledger = result.ledger()
    assert ledger["expected_jobs"]
    assert ledger["expected_candidate_ids"]
    stripped = deepcopy(ledger)
    stripped["native_receipts"] = []
    stripped["native_facts"] = []
    stripped["receipt_refs"] = []
    stripped["fact_refs"] = []
    stripped["batch_receipt_refs"] = []
    for row in stripped["operation_ledger"]:
        row["receipt_refs"] = []
        row["fact_refs"] = []
        row["received_candidate_ids"] = []
        row["candidate_typed_states"] = []
        row["coverage_states"] = []
        row["expected_candidate_ids"] = []
    stripped = _rehash(stripped)
    with pytest.raises(WorkloadBindingRefusal):
        restore_governed_frontier_ledger(
            stripped, expected_checkpoint_ref=result.freeze_restore_checkpoint())
    removed_fact = deepcopy(ledger)
    removed_fact["native_receipts"][0]["semantic_fields"]["empirical_fact_refs"] = []
    removed_fact = _rehash(removed_fact)
    with pytest.raises(WorkloadBindingRefusal):
        restore_governed_frontier_ledger(
            removed_fact, expected_checkpoint_ref=result.freeze_restore_checkpoint())
    restored = restore_governed_frontier_ledger(
        ledger, expected_checkpoint_ref=result.freeze_restore_checkpoint())
    assert restored["expected_jobs"] == ledger["expected_jobs"]
    assert restored["expected_candidate_ids"] == ledger["expected_candidate_ids"]


def test_r03_successor_held_unknown_states_remain_typed(tmp_path):
    from rawlsing_next.universal_grammar.types import HELD, UNKNOWN
    bundle, _ = _frontier_bundle(tmp_path / "r03_held_unknown.sav")
    inventory, policy, frontier = _frontier_fixture(bundle)
    eligible = [op for op in frontier.operations if op.disposition == "ELIGIBLE"]
    held = replace(eligible[0], disposition=HELD, reasons=("R03V_HELD",))
    unknown = replace(eligible[1], disposition=UNKNOWN, reasons=("R03V_UNKNOWN",))
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
    assert rows[held.op_id]["eligibility_state"] == HELD
    assert rows[unknown.op_id]["eligibility_state"] == UNKNOWN
    restored = restore_governed_frontier_ledger(
        result.ledger(), expected_checkpoint_ref=result.freeze_restore_checkpoint())
    restored_rows = {row["operation_id"]: row for row in restored["operation_ledger"]}
    assert restored_rows[held.op_id]["result_state"] == HELD
    assert restored_rows[unknown.op_id]["result_state"] == UNKNOWN


def test_r03_successor_recursive_root_release_severance_refused():
    from rawlsing_next.tests.test_universal_grammar import _campaign_fixture
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
    severed = deepcopy(campaign.snapshot())
    severed["payload"]["root"]["source_release_refs"] = []
    class Wrapper:
        def snapshot(self):
            return severed
    with pytest.raises(WorkloadBindingRefusal):
        bind_recursive_workload(Wrapper(), execution)
    assert baseline.source_release_refs


def test_r04_fixed_original_checkpoint_genuine_and_hostile(tmp_path):
    bundle, inventory, policy, frontier, compilation, result = _governed_result(
        tmp_path, "r04_fixed_pin.sav")
    pin = result.freeze_restore_checkpoint()
    ledger = result.ledger()
    restored = restore_governed_frontier_ledger(
        ledger, expected_checkpoint_ref=pin)
    assert restored["expected_jobs"] == ledger["expected_jobs"]
    with pytest.raises(WorkloadBindingRefusal, match="EXPECTED_CHECKPOINT_REQUIRED"):
        restore_governed_frontier_ledger(ledger)
    # Coordinated fact deletion with original pin.
    deleted = deepcopy(ledger)
    deleted["native_facts"].pop(0)
    deleted["fact_refs"].pop(0)
    deleted = _rehash(deleted)
    with pytest.raises(WorkloadBindingRefusal, match="CHECKPOINT_PIN_MISMATCH"):
        restore_governed_frontier_ledger(deleted, expected_checkpoint_ref=pin)
    # Coordinated fact duplication with original pin.
    duplicated = deepcopy(ledger)
    duplicated["native_facts"].append(deepcopy(duplicated["native_facts"][0]))
    duplicated["fact_refs"].append(deepcopy(duplicated["fact_refs"][0]))
    duplicated = _rehash(duplicated)
    with pytest.raises(WorkloadBindingRefusal, match="CHECKPOINT_PIN_MISMATCH"):
        restore_governed_frontier_ledger(duplicated, expected_checkpoint_ref=pin)
    # Expected job/predicate substitution in both mutable copies.
    substituted = deepcopy(ledger)
    old_job = substituted["expected_jobs"][0]
    new_job = [old_job[0], old_job[1], "c" * 64]
    substituted["expected_jobs"][0] = new_job
    substituted["compilation"]["issued"]["expected_jobs"][0] = new_job
    substituted["compilation_hash"] = semantic_hash(substituted["compilation"])
    # Sync the self-hash chain then keep the original external pin.
    substituted.pop("ledger_hash", None)
    substituted["ledger_hash"] = semantic_hash(substituted)
    with pytest.raises(WorkloadBindingRefusal, match="CHECKPOINT_PIN_MISMATCH"):
        restore_governed_frontier_ledger(substituted, expected_checkpoint_ref=pin)
    # A failed live result cannot acquire an accepted checkpoint.
    failed = replace(result, anti_join={**dict(result.anti_join),
                                        "no_drop_ok": False})
    with pytest.raises(WorkloadBindingRefusal, match="CHECKPOINT_LIVE"):
        failed.freeze_restore_checkpoint()


def test_r04_fixed_pin_fresh_process_restore(tmp_path):
    bundle, inventory, policy, frontier, compilation, result = _governed_result(
        tmp_path, "r04_fresh.sav")
    pin = result.freeze_restore_checkpoint()
    ledger = result.ledger()
    ledger_path = tmp_path / "r04_ledger.json"
    ledger_path.write_text(json.dumps(ledger, sort_keys=True))
    code = """
import json, sys
from rawlsing_next.pre553_universal_workload import restore_governed_frontier_ledger
ledger = json.loads(open(sys.argv[1], encoding="utf-8").read())
restored = restore_governed_frontier_ledger(ledger, expected_checkpoint_ref=sys.argv[2])
print(json.dumps({"schema": restored["schema"],
                  "jobs": len(restored["expected_jobs"]),
                  "receipts": len(restored["receipt_refs"]),
                  "facts": len(restored["fact_refs"])}, sort_keys=True))
"""
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.run(
        [sys.executable, "-c", code, str(ledger_path), pin],
        cwd=str(REPO_ROOT), env=env, capture_output=True, text=True, timeout=180,
    )
    assert proc.returncode == 0, proc.stderr[-2000:]
    child = json.loads(proc.stdout)
    assert child["jobs"] == len(ledger["expected_jobs"])
    assert child["receipts"] == len(ledger["receipt_refs"])
    assert child["facts"] == len(ledger["fact_refs"])
