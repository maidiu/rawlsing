"""Derive the compact court metrics used in the return documents."""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
E = BASE / "evidence"


def pct(values, p):
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    pos = (len(ordered) - 1) * p
    lo = int(pos)
    hi = min(lo + 1, len(ordered) - 1)
    frac = pos - lo
    return ordered[lo] * (1 - frac) + ordered[hi] * frac


def main() -> int:
    estate = json.loads((E / "estate_receipt.json").read_text())
    ops = json.loads((E / "ops_manifest.json").read_text())
    cold = json.loads((E / "cold_100ops.json").read_text())
    one = json.loads((E / "cold_1op.json").read_text())
    guard = json.loads((E / "guard_probe.json").read_text())
    parity = json.loads((E / "parity.json").read_text())
    meas = json.loads((E / "measurements.json").read_text())
    repeat = json.loads((E / "repeat_1000_grouped.json").read_text()) if (E / "repeat_1000_grouped.json").exists() else None

    walls = [row["wall_seconds"] for row in cold["per_operation"]]
    raw_denoms = [row["raw_denominator_support"] for row in cold["per_operation"]]
    def numeric(value):
        if isinstance(value, dict) and "$exact_fraction" in value:
            numerator, denominator = value["$exact_fraction"]
            return numerator / denominator
        return value

    weighted = [
        numeric(row["weighted_denominator_support"])
        for row in cold["per_operation"]
        if row["weighted_denominator_support"] is not None
    ]
    ungrouped = meas["native_oracle"]["ungrouped"]
    grouped = meas["native_oracle"]["grouped_max256"]
    g64 = meas["native_oracle"]["grouped_default64"]
    counters = cold["counters"]
    estate_rows = sum(estate["family_counts"].values())
    cell_states: dict[str, int] = {}
    for row in cold["per_operation"]:
        for state, count in row.get("cell_state_counts", {}).items():
            cell_states[state] = cell_states.get(state, 0) + count
    derived = {
        "schema": "PYAT_COUNTRY_REUSE_DERIVED@1",
        "estate": {
            "respondents": estate["fixture"]["respondents"],
            "events": estate["fixture"]["events"],
            "routing": estate["fixture"]["routing"],
            "weights": estate["fixture"]["weights"],
            "family_rows": estate_rows,
            "retained_bytes": estate["retained_bytes"],
        },
        "operations": {
            "distinct": ops["distinct_operations"],
            "cores": ops["core_operations"],
            "weighted_variants": ops["measure_variants"],
            "typed_states": cold["typed_state_counts"],
            "raw_denominator_min": min(raw_denoms),
            "raw_denominator_max": max(raw_denoms),
            "raw_denominator_p50": pct(raw_denoms, 0.5),
            "weighted_denominator_min": min(weighted),
            "weighted_denominator_max": max(weighted),
            "cell_state_counts": cell_states,
        },
        "cold": {
            "one_op_seconds": one["wall_seconds"],
            "batch_wall_seconds": cold["wall_seconds"],
            "ops_per_second": cold["operations_per_second"],
            "per_op_min": min(walls),
            "per_op_p50": pct(walls, 0.5),
            "per_op_p95": pct(walls, 0.95),
            "per_op_max": max(walls),
            "per_op_mean": sum(walls) / len(walls),
            "cpu_user_seconds": cold["cpu_user_seconds"],
            "cpu_system_seconds": cold["cpu_system_seconds"],
            "session_build_seconds": counters["session_build_seconds"],
            "session_enter_seconds": counters["session_enter_seconds"],
            "session_build_share": counters["session_build_seconds"] / cold["wall_seconds"],
            "session_enter_share": counters["session_enter_seconds"] / cold["wall_seconds"],
            "row_group_reads": counters["row_group_reads"],
            "row_group_reads_per_op": counters["row_group_reads"] / cold["operations_completed"],
            "row_group_rows": counters["row_group_rows"],
            "row_group_rows_per_op": counters["row_group_rows"] / cold["operations_completed"],
            "row_group_compressed_bytes": counters["row_group_compressed_bytes"],
            "row_group_uncompressed_bytes": counters["row_group_uncompressed_bytes"],
            "compressed_read_amplification_vs_estate": counters["row_group_compressed_bytes"] / estate["retained_bytes"],
            "uncompressed_read_amplification_vs_estate": counters["row_group_uncompressed_bytes"] / estate["retained_bytes"],
            "family_rows_yielded": counters["family_rows_yielded"],
            "family_rows_per_op": counters["family_rows_yielded"] / cold["operations_completed"],
            "event_object_materializations": counters["event_object_materializations"],
            "event_materializations_per_op": counters["event_object_materializations"] / cold["operations_completed"],
            "family_object_materializations": counters["family_object_materializations"],
            "session_temp_max_bytes": counters["session_temp_max_bytes"],
            "process_tree_rss_peak_bytes": cold["process_tree_rss_peak_bytes"],
            "self_maxrss_bytes": cold["self_maxrss_bytes"],
            "c11_repository_tripwire_hits": counters["c11_repository_tripwire_hits"],
            "read_table_calls": counters["read_table_calls"],
            "forecast_1000_seconds": cold["cold_qualification_forecast"]["projected_wall_seconds"],
            "forecast_1000_exceeds_budget": cold["cold_qualification_forecast"]["exceeds_300s_budget"],
        },
        "grouped_in_memory": {
            "ungrouped_wall_seconds": ungrouped["wall_seconds"],
            "grouped_max256_wall_seconds": grouped["wall_seconds"],
            "grouped_default64_wall_seconds": g64["wall_seconds"],
            "wall_reduction_fraction": (ungrouped["wall_seconds"] - grouped["wall_seconds"]) / ungrouped["wall_seconds"],
            "speedup": ungrouped["wall_seconds"] / grouped["wall_seconds"],
            "max256_receipt": grouped["group_scope_receipt"],
            "default64_receipt": g64["group_scope_receipt"],
            "core_hit_fraction": grouped["group_scope_receipt"]["core_hits"] / ops["distinct_operations"],
            "saved_seconds_per_core_hit": (ungrouped["wall_seconds"] - grouped["wall_seconds"]) / max(1, grouped["group_scope_receipt"]["core_hits"]),
            "substrate_note": "in-memory C11Repository, not cold saved consumer",
        },
        "repeat_invocations": None if repeat is None else {
            "iterations": repeat["iterations"],
            "scope": repeat["scope"],
            "ungrouped_wall_seconds": repeat["ungrouped_wall_seconds"],
            "grouped_wall_seconds": repeat["grouped_wall_seconds"],
            "wall_speedup": repeat["wall_speedup"],
            "grouped_receipt": repeat["grouped_receipt"],
            "p50_seconds": repeat["grouped_per_iteration_p50_seconds"],
        },
        "guard": {
            "carrier": guard["carrier_guard"],
            "evaluator": guard["evaluator_guard"],
            "cold_index_contract": guard["cold_index_contract"],
        },
        "parity": {
            key: {"exact": value["exact"], "mismatches": value["mismatch_count"]}
            for key, value in parity.items() if isinstance(value, dict) and "exact" in value
        },
        "court_wall_seconds": meas["total_court_wall_seconds"],
    }
    (E / "summary_derived.json").write_text(
        json.dumps(derived, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(derived, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
