"""Independent G5 probe: negative/occurrence/deferred census axes, S1-C."""
from __future__ import annotations

import json
import tempfile
from dataclasses import replace
from pathlib import Path

from rawlsing_next.pre553_operation_fate_census import (
    CensusRefusal, execute_censused_sourcefree, verify_frozen_inputs,
)
from rawlsing_next.tests.test_pyat_r3_s1c_source_operation_fates import (
    _fixture, _freeze_packet, _run,
)
from rawlsing_next.tests.test_universal_workload import AS_OF, HOST, PURPOSE
from rawlsing_next.universal_grammar.enumerate import enumerate_frontier
from rawlsing_next.universal_grammar.types import ADMINISTRATION_UNKNOWN


def refusal(fn):
    opened: list[object] = []
    try:
        fn(opened)
    except CensusRefusal as exc:
        return {"refused": True, "code": exc.code,
                "detail": exc.detail, "source_factory_calls": len(opened)}
    return {"refused": False, "source_factory_calls": len(opened)}


def summary(result):
    rows = result["operation_fates"]
    return {
        "grade": result["grade"],
        "declared": result["declared_operation_count"],
        "received": result["received_operation_count"],
        "fate_counts": result["fate_counts"],
        "unknown_scope_count": result["unknown_scope_count"],
        "excluded_scope_count": result["excluded_scope_count"],
        "inventory_ledger_count": result["inventory_ledger_count"],
        "deferred_scope_count": result["deferred_scope_count"],
        "deferred_scope_records": result["deferred_scope_records"],
        "issued_candidates": result["issued_candidate_count"],
        "native_facts": result["native_fact_count"],
        "source_factory_calls": result["source_factory_calls"],
        "candidate_anti_join_ok": result["candidate_anti_join"].get("no_drop_ok"),
        "operation_anti_join_ok": result["operation_anti_join"].get("no_drop_ok"),
        "result_states": {
            state: sum(row["result_state"] == state for row in rows)
            for state in ("SUPPORTED", "VALID_EMPTY", "ZERO_SUPPORT",
                          "UNKNOWN", "DIFFUSE", "HELD", "UNSUPPORTED")
        },
        "noneligible_with_receipts": sum(
            row["scientific_disposition"] != "ELIGIBLE"
            and bool(row["received_candidate_ids"]) for row in rows),
        "noneligible_with_facts": sum(
            row["scientific_disposition"] != "ELIGIBLE"
            and bool(row["fact_refs"]) for row in rows),
        "unknown_with_receipts": sum(
            row["scientific_disposition"] == "UNKNOWN"
            and bool(row["received_candidate_ids"]) for row in rows),
        "held_with_receipts": sum(
            row["scientific_disposition"] == "HELD"
            and bool(row["received_candidate_ids"]) for row in rows),
        "inapplicable_with_receipts": sum(
            row["scientific_disposition"] == "INAPPLICABLE_PROVED"
            and bool(row["received_candidate_ids"]) for row in rows),
    }


def main() -> int:
    work = Path(tempfile.mkdtemp(prefix="s1c-g5-negatives-"))
    report: dict[str, object] = {"workdir": str(work)}
    bundle, inventory, policy, frontier, census = _fixture(work)

    baseline = _run(bundle, inventory, policy, frontier, census)
    report["baseline"] = summary(baseline)

    # Deferred ARITY records are conserved against the honest declaration.
    # (A caller that co-forges both the frozen census and the frontier can
    # omit them; that is the acknowledged declared-input completeness limit.)
    dropped_deferred = replace(frontier, deferred=())
    report["deferred_frontier_tamper"] = refusal(
        lambda _opened: execute_censused_sourcefree(
            census=census, inventory=inventory, policy=policy,
            frontier=dropped_deferred, bundle=bundle, as_of=AS_OF,
            host=HOST, purpose=PURPOSE,
            source_factory=lambda ref: (
                _opened.append(ref), bundle.physical_stream)[1]))
    report["deferred_coforged_both_empty"] = refusal(
        lambda _opened: verify_frozen_inputs(
            _freeze_packet(dropped_deferred), inventory=inventory,
            policy=policy, frontier=dropped_deferred))

    # Real routing-UNKNOWN inventory: UNKNOWN fate is retained and not issued.
    unknown_occurrences = tuple(
        replace(occ, administration=ADMINISTRATION_UNKNOWN,
                route_state="UNKNOWN_ROUTING")
        if occ.key.item_id == "A" else occ
        for occ in inventory.occurrences)
    unknown_inventory = replace(inventory, occurrences=unknown_occurrences)
    unknown_frontier = enumerate_frontier(unknown_inventory, policy)
    unknown_census = _freeze_packet(
        unknown_frontier, scope_id="S1C-G5-ROUTING-UNKNOWN")
    affected = [
        op for op in unknown_frontier.operations
        if any(key.item_id == "A" for key in (
            tuple(op.targets) + tuple(key for key, _ in op.conditions)))
    ]
    unknown_result = _run(bundle, unknown_inventory, policy,
                          unknown_frontier, unknown_census)
    report["routing_unknown"] = {
        "affected_operations": len(affected),
        "fate_counts": unknown_result["fate_counts"],
        "unknown_scope_count": unknown_result["unknown_scope_count"],
        "excluded_scope_count": unknown_result["excluded_scope_count"],
        "inventory_ledger_count": unknown_result["inventory_ledger_count"],
        "noneligible_affected_with_receipts": sum(
            bool(next(row for row in unknown_result["operation_fates"]
                      if row["operation_id"] == op.op_id)
                 ["received_candidate_ids"])
            for op in affected if op.disposition != "ELIGIBLE"),
        "noneligible_affected_with_facts": sum(
            bool(next(row for row in unknown_result["operation_fates"]
                      if row["operation_id"] == op.op_id)["fact_refs"])
            for op in affected if op.disposition != "ELIGIBLE"),
        "unknown_with_receipts": sum(
            row["scientific_disposition"] == "UNKNOWN"
            and bool(row["received_candidate_ids"])
            for row in unknown_result["operation_fates"]),
        "operation_anti_join_ok": unknown_result[
            "operation_anti_join"].get("no_drop_ok"),
        "source_factory_calls": unknown_result["source_factory_calls"],
    }
    # Real UNKNOWN and INAPPLICABLE/EXCLUDED operations from genuine R61 axes.
    negative_occurrences = tuple(
        replace(occ, risk_set_refs=())
        if occ.key.item_id == "A"
        else replace(occ, risk_set_refs=("RISK-" + occ.key.item_id,))
        for occ in inventory.occurrences)
    negative_inventory = replace(inventory, occurrences=negative_occurrences)
    negative_frontier = enumerate_frontier(negative_inventory, policy)
    negative_census = _freeze_packet(
        negative_frontier, scope_id="S1C-G5-REAL-NEGATIVE-AXES")
    negative_result = _run(
        bundle, negative_inventory, policy, negative_frontier, negative_census)
    report["real_negative_axes"] = {
        "unknown_operations": sum(
            op.disposition == "UNKNOWN" for op in negative_frontier.operations),
        "excluded_operations": sum(
            op.disposition in {"PROHIBITED", "INAPPLICABLE_PROVED"}
            for op in negative_frontier.operations),
        "fate_counts": negative_result["fate_counts"],
        "unknown_scope_count": negative_result["unknown_scope_count"],
        "excluded_scope_count": negative_result["excluded_scope_count"],
        "inventory_ledger_count": negative_result["inventory_ledger_count"],
        "unknown_with_receipts": sum(
            row["scientific_disposition"] == "UNKNOWN"
            and bool(row["received_candidate_ids"])
            for row in negative_result["operation_fates"]),
        "excluded_with_receipts": sum(
            row["scientific_disposition"] in {"PROHIBITED", "INAPPLICABLE_PROVED"}
            and bool(row["received_candidate_ids"])
            for row in negative_result["operation_fates"]),
        "operation_anti_join_ok": negative_result[
            "operation_anti_join"].get("no_drop_ok"),
        "source_factory_calls": negative_result["source_factory_calls"],
    }
    for label, mutated in (
        ("unknown_axis_dropped", replace(negative_frontier, unknown=())),
        ("excluded_axis_dropped", replace(negative_frontier, excluded=())),
    ):
        report[label] = refusal(
            lambda _opened, mutated=mutated: execute_censused_sourcefree(
                census=negative_census, inventory=negative_inventory,
                policy=policy, frontier=mutated, bundle=bundle,
                as_of=AS_OF, host=HOST, purpose=PURPOSE,
                source_factory=lambda ref: (
                    _opened.append(ref), bundle.physical_stream)[1]))

    # Real proved-inapplicable inventory: INAPPLICABLE_PROVED retained, no issue.
    inapplicable_occurrences = tuple(
        replace(occ, forms=("DISJOINT_B_FORM",))
        if occ.key.item_id == "B" else occ
        for occ in inventory.occurrences)
    inapplicable_inventory = replace(
        inventory, occurrences=inapplicable_occurrences)
    inapplicable_frontier = enumerate_frontier(inapplicable_inventory, policy)
    inapplicable_census = _freeze_packet(
        inapplicable_frontier, scope_id="S1C-G5-DISJOINT-FORM")
    inapplicable = {
        op.op_id for op in inapplicable_frontier.operations
        if op.disposition == "INAPPLICABLE_PROVED"
    }
    inapplicable_result = _run(
        bundle, inapplicable_inventory, policy,
        inapplicable_frontier, inapplicable_census)
    rows = {row["operation_id"]: row
            for row in inapplicable_result["operation_fates"]}
    report["proved_inapplicable"] = {
        "inapplicable_operations": len(inapplicable),
        "fate_counts": inapplicable_result["fate_counts"],
        "excluded_scope_count": inapplicable_result["excluded_scope_count"],
        "all_retained": inapplicable <= set(rows),
        "all_without_receipts_or_facts": all(
            not rows[op]["received_candidate_ids"] and not rows[op]["fact_refs"]
            for op in inapplicable),
        "operation_anti_join_ok": inapplicable_result[
            "operation_anti_join"].get("no_drop_ok"),
        "source_factory_calls": inapplicable_result["source_factory_calls"],
    }
    report["inapplicable_excluded_drop"] = refusal(
        lambda _opened: execute_censused_sourcefree(
            census=inapplicable_census, inventory=inapplicable_inventory,
            policy=policy,
            frontier=replace(inapplicable_frontier, excluded=()),
            bundle=bundle, as_of=AS_OF, host=HOST, purpose=PURPOSE,
            source_factory=lambda ref: (
                _opened.append(ref), bundle.physical_stream)[1]))

    print(json.dumps(report, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
