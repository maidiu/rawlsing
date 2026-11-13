"""Independent G5 probe for PYAT R3 S1-C at dae66cdf.

Runs outside the pinned source tree; imports the S1-C test helpers but does
not modify code, tests, fixtures or the evidence branch. Scope TEST_ONLY.
"""
from __future__ import annotations

import json
import tempfile
from collections import Counter
from dataclasses import replace
from pathlib import Path

from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.pre553_operation_fate_census import (
    CensusRefusal, execute_censused_sourcefree, verify_frozen_inputs,
)
from rawlsing_next.pre553_universal_workload import (
    compile_governed_frontier, execute_governed_frontier,
)
from rawlsing_next.tests.test_pyat_r3_s1c_source_operation_fates import (
    _fixture, _freeze_packet, _run,
)
from rawlsing_next.tests.test_universal_workload import AS_OF, HOST, PURPOSE
from rawlsing_next.universal_grammar.types import ELIGIBLE, Occurrence


def _refusal(fn):
    opened: list[object] = []
    try:
        fn(opened)
    except CensusRefusal as exc:
        return {
            "refused": True,
            "code": exc.code,
            "detail": exc.detail,
            "source_factory_calls": len(opened),
        }
    return {"refused": False, "source_factory_calls": len(opened)}


def _state_counts(rows):
    return {
        "execution_state": dict(sorted(Counter(
            row["execution_state"] for row in rows).items())),
        "result_state": dict(sorted(Counter(
            row["result_state"] for row in rows).items())),
        "lowering_status": dict(sorted(Counter(
            row["lowering_status"] for row in rows).items())),
    }


def _conservation(result):
    rows = result["operation_fates"]
    received_by_candidate: dict[str, list[str]] = {}
    for row in rows:
        for cid in row["received_candidate_ids"]:
            received_by_candidate.setdefault(cid, []).append(row["operation_id"])
    expected = {
        cid for row in rows
        for cid in (
            tuple(row["received_candidate_ids"])
            + tuple(row["missing_candidate_ids"])
        )
    }
    duplicates = {
        cid: ops for cid, ops in received_by_candidate.items() if len(ops) != 1
    }
    receipt_rows = sum(1 for row in rows if row["received_candidate_ids"])
    fact_rows = sum(1 for row in rows if row["fact_refs"])
    no_receipt = [
        {
            "operation_id": row["operation_id"],
            "disposition": row["scientific_disposition"],
            "lowering_status": row["lowering_status"],
            "execution_state": row["execution_state"],
        }
        for row in rows if not row["received_candidate_ids"]
    ]
    return {
        "declared": result["declared_operation_count"],
        "compiled": result["compiled_operation_count"],
        "receipt_rows": result["received_operation_count"],
        "operation_fate_rows": len(rows),
        "issued_candidates": result["issued_candidate_count"],
        "native_facts": result["native_fact_count"],
        "source_factory_calls": result["source_factory_calls"],
        "distinct_expected_candidate_ids": len(expected),
        "distinct_received_candidate_ids": len(received_by_candidate),
        "missing_expected_candidate_ids": sorted(expected - set(received_by_candidate)),
        "unexpected_received_candidate_ids": sorted(set(received_by_candidate) - expected),
        "candidate_assigned_to_multiple_operations": duplicates,
        "operations_with_receipts": receipt_rows,
        "operations_with_facts": fact_rows,
        "operations_without_receipts": len(no_receipt),
        "operations_without_receipts_detail": no_receipt,
        "candidate_anti_join": result["candidate_anti_join"],
        "operation_anti_join": result["operation_anti_join"],
        "fate_counts": result["fate_counts"],
        "deferred_scope_count": result["deferred_scope_count"],
        "unsupported_runtime_rows": sum(
            row["lowering_status"] == "UNSUPPORTED_RUNTIME" for row in rows),
        "states": _state_counts(rows),
    }


def main() -> int:
    work = Path(tempfile.mkdtemp(prefix="s1c-g5-independent-"))
    report: dict[str, object] = {"workdir": str(work)}
    bundle, inventory, policy, frontier, census = _fixture(work)

    # ---- G2: positive 309-operation sourcefree case ----
    baseline = _run(bundle, inventory, policy, frontier, census)
    report["G2_positive"] = _conservation(baseline)

    # Optional-weight RAW nonloss vs population/weighted HELD.
    eligible = [op for op in frontier.operations if op.disposition == ELIGIBLE]
    sample_ids = {
        op.op_id for op in eligible if op.measure_kind == "SAMPLE"
    }
    population_ids = {
        op.op_id for op in eligible if op.measure_kind == "POPULATION"
    }
    row_by_id = {row["operation_id"]: row for row in baseline["operation_fates"]}
    report["G3_optional_weight"] = {
        "declared_eligible": len(eligible),
        "eligible_sample_raw": len(sample_ids),
        "eligible_population": len(population_ids),
        "sample_raw_with_receipts": sum(
            bool(row_by_id[op]["received_candidate_ids"]) for op in sample_ids),
        "sample_raw_without_receipts": sorted(
            op for op in sample_ids if not row_by_id[op]["received_candidate_ids"]),
        "population_with_receipts": sorted(
            op for op in population_ids if row_by_id[op]["received_candidate_ids"]),
        "held_population_without_weight": sum(
            1 for op in frontier.operations
            if op.measure_kind == "POPULATION"
            and op.disposition == "HELD"
            and "POPULATION_WITHOUT_WEIGHT_OR_DESIGN" in op.reasons),
        "invented_eligibility": [
            op.op_id for op in frontier.operations
            if op.disposition == ELIGIBLE and op.measure_kind != "SAMPLE"
            and op.measure_kind != "POPULATION"
        ],
    }

    # ---- G2: changed physical value and exact restoration ----
    from rawlsing_next.pre553_physical_decoder import PhysicalMissingState
    from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream
    cells = tuple(bundle.physical_stream.iter_cells())

    def altered_cells():
        return tuple(
            replace(c, raw_value=1.0 - float(c.raw_value))
            if c.variable_name == "A"
            and c.missing_state is PhysicalMissingState.OBSERVED_STORAGE_VALUE
            else c for c in cells
        )

    altered = ExactPhysicalCellStream(
        source_sha256=bundle.source_sha256,
        row_count=bundle.physical_stream.row_count,
        cell_iter_factory=altered_cells,
    )
    changed = _run(bundle, inventory, policy, frontier, census,
                   lambda _ref: altered)
    restored = _run(bundle, inventory, policy, frontier, census)

    def facts(result):
        return {
            row["operation_id"]: tuple(
                x["content_hash"] for x in row["fact_refs"])
            for row in result["operation_fates"]
        }

    changed_ops = sorted(
        op for op in facts(baseline)
        if facts(baseline)[op] != facts(changed)[op]
    )
    report["G2_changed_value_restore"] = {
        "baseline_checkpoint": baseline["checkpoint_hash"],
        "changed_checkpoint": changed["checkpoint_hash"],
        "restored_checkpoint": restored["checkpoint_hash"],
        "checkpoint_changed": (
            baseline["checkpoint_hash"] != changed["checkpoint_hash"]),
        "checkpoint_restored_exactly": (
            baseline["checkpoint_hash"] == restored["checkpoint_hash"]),
        "frozen_census_restored_exactly": (
            baseline["frozen_census_hash"] == restored["frozen_census_hash"]),
        "fact_identity_changed": facts(baseline) != facts(changed),
        "fact_identity_restored": facts(baseline) == facts(restored),
        "operations_with_changed_fact_identity": changed_ops,
        "changed_issued_candidates": changed["issued_candidate_count"],
        "baseline_issued_candidates": baseline["issued_candidate_count"],
        "changed_native_facts": changed["native_fact_count"],
        "baseline_native_facts": baseline["native_fact_count"],
        "changed_source_factory_calls": changed["source_factory_calls"],
        "changed_anti_join": changed["candidate_anti_join"],
        "changed_operation_anti_join": changed["operation_anti_join"],
    }

    # ---- G3 attack 1: false HELD drops a valid RAW ----
    eligible_raw = next(
        op for op in frontier.operations
        if op.disposition == ELIGIBLE and op.measure_kind == "SAMPLE"
        and op.claim_class == "DIST"
    )
    baseline_raw_row = next(
        row for row in baseline["operation_fates"]
        if row["operation_id"] == eligible_raw.op_id)
    forged_op = replace(
        eligible_raw, disposition="HELD", reasons=("UNISSUED_FALSE_HOLD",))
    changed_ops_tuple = tuple(
        forged_op if op.op_id == eligible_raw.op_id else op
        for op in frontier.operations)
    dispositions = dict(frontier.disposition_counts)
    dispositions["ELIGIBLE"] -= 1
    dispositions["HELD"] = dispositions.get("HELD", 0) + 1
    class_counts = dict(frontier.class_counts)
    class_counts[eligible_raw.claim_class] -= 1
    if class_counts[eligible_raw.claim_class] == 0:
        del class_counts[eligible_raw.claim_class]
    forged_frontier = replace(
        frontier, operations=changed_ops_tuple,
        disposition_counts=dispositions, class_counts=class_counts)
    forged_census = _freeze_packet(forged_frontier)
    forged_comp = compile_governed_frontier(
        bundle=bundle, inventory=inventory, policy=policy,
        frontier=forged_frontier, as_of=AS_OF, host=HOST, purpose=PURPOSE)
    forged_native = execute_governed_frontier(
        compilation=forged_comp,
        source_factory=lambda _ref: bundle.physical_stream)
    forged_row = next(
        row for row in forged_native.operation_ledger
        if row["operation_id"] == eligible_raw.op_id)
    report["G3_false_held"] = {
        "target_operation_id": eligible_raw.op_id,
        "baseline_execution_state": baseline_raw_row["execution_state"],
        "baseline_received_candidates": baseline_raw_row["received_candidate_ids"],
        "forged_native_receipts": len(forged_native.receipt_refs),
        "baseline_receipts": baseline["issued_candidate_count"],
        "receipt_loss": (
            baseline["issued_candidate_count"] - len(forged_native.receipt_refs)),
        "forged_row_result_state": forged_row["result_state"],
        "forged_row_received_candidates": forged_row["received_candidate_ids"],
        "forged_native_candidate_anti_join_ok": (
            forged_native.anti_join.get("no_drop_ok")),
        "forged_native_operation_anti_join_ok": (
            forged_native.operation_anti_join.get("no_drop_ok")),
        "source_census_equal": (
            forged_census.source_census_ref == census.source_census_ref),
        "science_census_differs": (
            forged_census.science_census_ref != census.science_census_ref),
        "adapter": _refusal(
            lambda opened: execute_censused_sourcefree(
                census=forged_census, inventory=inventory, policy=policy,
                frontier=forged_frontier, bundle=bundle, as_of=AS_OF,
                host=HOST, purpose=PURPOSE,
                source_factory=lambda ref: opened.append(ref))),
    }

    # Variant: a fake reason on a genuine HELD operation.
    actual_held = next(
        op for op in frontier.operations if op.disposition == "HELD")
    reason_changed = tuple(
        replace(op, reasons=("UNISSUED_AUTHORITY_OVERRIDE",))
        if op.op_id == actual_held.op_id else op
        for op in frontier.operations)
    reason_frontier = replace(frontier, operations=reason_changed)
    reason_census = _freeze_packet(reason_frontier)
    report["G3_false_held_reason_variant"] = {
        "target_operation_id": actual_held.op_id,
        "disposition_unchanged": (
            next(op for op in reason_frontier.operations
                 if op.op_id == actual_held.op_id).disposition
            == actual_held.disposition),
        "verifier": _refusal(
            lambda _opened: verify_frozen_inputs(
                reason_census, inventory=inventory, policy=policy,
                frontier=reason_frontier)),
    }

    # ---- G3 attack 2: pending-list severance / false COMPLETE ----
    budget_dir = work / "budget=5"
    budget_dir.mkdir(parents=True, exist_ok=True)
    budget_bundle, budget_inventory, budget_policy, budget_frontier, budget_census = (
        _fixture(budget_dir, budget=5))
    honest = _run(budget_bundle, budget_inventory, budget_policy,
                  budget_frontier, budget_census)
    honest_rows = {row["operation_id"]: row
                   for row in honest["operation_fates"]}
    pending_ids = set(budget_frontier.pending_operation_ids)
    report["G3_pending_honest"] = {
        "budget_state": budget_frontier.budget_state,
        "pending_count": len(pending_ids),
        "execution_counts": dict(budget_frontier.execution_counts),
        "issued_candidates": honest["issued_candidate_count"],
        "native_facts": honest["native_fact_count"],
        "source_factory_calls": honest["source_factory_calls"],
        "pending_rows_with_receipts": sum(
            bool(honest_rows[op]["received_candidate_ids"]) for op in pending_ids),
        "pending_rows_with_facts": sum(
            bool(honest_rows[op]["fact_refs"]) for op in pending_ids),
        "pending_rows_all_pending": all(
            honest_rows[op]["execution_state"] == "PENDING" for op in pending_ids),
    }

    severed = replace(budget_frontier, pending_operation_ids=())
    severed_census = _freeze_packet(severed)
    severed_comp = compile_governed_frontier(
        bundle=budget_bundle, inventory=budget_inventory,
        policy=budget_policy, frontier=severed,
        as_of=AS_OF, host=HOST, purpose=PURPOSE)
    severed_native = execute_governed_frontier(
        compilation=severed_comp,
        source_factory=lambda _ref: budget_bundle.physical_stream)
    severed_rows = {row["operation_id"]: row
                    for row in severed_native.operation_ledger}
    report["G3_pending_severance_native"] = {
        "pending_ids_removed": len(pending_ids),
        "budget_state_after": severed.budget_state,
        "frontier_pending_rows_still_pending": all(
            next(op for op in severed.operations
                 if op.op_id == op_id).execution_state == "PENDING"
            for op_id in pending_ids),
        "source_census_equal": (
            severed_census.source_census_ref == budget_census.source_census_ref),
        "science_census_equal": (
            severed_census.science_census_ref == budget_census.science_census_ref),
        "unknown_scope_equal": (
            severed_census.unknown_scope_records
            == budget_census.unknown_scope_records),
        "excluded_scope_equal": (
            severed_census.excluded_scope_records
            == budget_census.excluded_scope_records),
        "inventory_ledger_equal": (
            severed_census.inventory_ledger_records
            == budget_census.inventory_ledger_records),
        "baseline_receipts": honest["issued_candidate_count"],
        "tampered_native_receipts": len(severed_native.receipt_refs),
        "overissued": (
            len(severed_native.receipt_refs)
            > honest["issued_candidate_count"]),
        "pending_ids_with_receipts": sum(
            bool(severed_rows[op]["received_candidate_ids"])
            for op in pending_ids),
        "candidate_anti_join_ok": (
            severed_native.anti_join.get("no_drop_ok")),
        "operation_anti_join_ok": (
            severed_native.operation_anti_join.get("no_drop_ok")),
        "adapter": _refusal(
            lambda opened: execute_censused_sourcefree(
                census=severed_census, inventory=budget_inventory,
                policy=budget_policy, frontier=severed,
                bundle=budget_bundle, as_of=AS_OF, host=HOST,
                purpose=PURPOSE,
                source_factory=lambda ref: opened.append(ref))),
    }

    false_complete = replace(budget_frontier, budget_state="COMPLETE")
    false_complete_census = _freeze_packet(false_complete)
    report["G3_false_complete"] = {
        "declared_budget_state": false_complete.budget_state,
        "pending_count": len(false_complete.pending_operation_ids),
        "verifier": _refusal(
            lambda _opened: verify_frozen_inputs(
                false_complete_census, inventory=budget_inventory,
                policy=budget_policy, frontier=false_complete)),
    }

    # Variants: partial pending-list loss, duplicate ID, unmarked pending row.
    subset = replace(
        budget_frontier,
        pending_operation_ids=budget_frontier.pending_operation_ids[:-1])
    duplicate = replace(
        budget_frontier,
        pending_operation_ids=(
            budget_frontier.pending_operation_ids
            + (budget_frontier.pending_operation_ids[0],)))
    nonpending = next(
        op for op in budget_frontier.operations
        if op.op_id not in pending_ids and op.disposition == ELIGIBLE)
    executions = dict(budget_frontier.execution_counts)
    executions["NOT_STARTED"] -= 1
    executions["PENDING"] = executions.get("PENDING", 0) + 1
    unmarked_ops = tuple(
        replace(op, execution_state="PENDING")
        if op.op_id == nonpending.op_id else op
        for op in budget_frontier.operations)
    unmarked = replace(
        budget_frontier, operations=unmarked_ops,
        execution_counts=executions)
    report["G3_pending_variants"] = {
        "partial_list_loss": {
            "removed": 1,
            "verifier": _refusal(
                lambda _opened: verify_frozen_inputs(
                    _freeze_packet(subset), inventory=budget_inventory,
                    policy=budget_policy, frontier=subset)),
        },
        "duplicate_pending_id": {
            "verifier": _refusal(
                lambda _opened: verify_frozen_inputs(
                    _freeze_packet(duplicate), inventory=budget_inventory,
                    policy=budget_policy, frontier=duplicate)),
        },
        "unmarked_pending_row": {
            "operation_id": nonpending.op_id,
            "verifier": _refusal(
                lambda _opened: verify_frozen_inputs(
                    _freeze_packet(unmarked), inventory=budget_inventory,
                    policy=budget_policy, frontier=unmarked)),
        },
    }

    honest_restored = _run(budget_bundle, budget_inventory, budget_policy,
                           budget_frontier, budget_census)
    report["G3_pending_restoration"] = {
        "checkpoint_restored_exactly": (
            honest_restored["checkpoint_hash"] == honest["checkpoint_hash"]),
        "frozen_census_restored_exactly": (
            honest_restored["frozen_census_hash"]
            == honest["frozen_census_hash"]),
        "operation_fates_identical": (
            honest_restored["operation_fates"] == honest["operation_fates"]),
        "issued_candidates_equal": (
            honest_restored["issued_candidate_count"]
            == honest["issued_candidate_count"]),
        "native_facts_equal": (
            honest_restored["native_fact_count"]
            == honest["native_fact_count"]),
    }

    print(json.dumps(report, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
