"""Measured country-reuse court: cold saved operations, grouped path, exact barrier.

TEST_ONLY.  All production and accepted-test files are read-only.  The only
writes are this return directory, its evidence, and the disposable `.local-data`
estate scratch.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import time
import traceback
from typing import Any

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
REPO = BASE.parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_carrier_execution import (
    CarrierExecutionBindingError,
    CarrierNeutralResearchExecutor,
)
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_empirical_objects import canonical_json, exact_ref
from rawlsing_next.pre553_empirical_query import (
    EmpiricalQueryExecutionError,
    I03GroupedExecutionScope,
    execute_empirical_query,
)
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_source_direct_parquet_estate import VerifiedDirectEstate

from court_instrumentation import (
    CourtInstrumentation,
    cpu_times,
    current_rss_bytes,
    directory_bytes,
    maxrss_bytes,
    process_tree_rss_bytes,
)
from fixture_1006 import ShapeSpec, build_context
from ops import Battery, Operation

RESPONDENTS = 128
TAG = "PYAT-COUNTRY-REUSE-20261115"
BUDGET_SECONDS = 300.0

START = time.monotonic()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def j(value: Any) -> Any:
    return json.loads(canonical_json(value))


def _plain(value: Any) -> Any:
    from collections.abc import Mapping
    from fractions import Fraction

    if isinstance(value, Mapping):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_plain(item) for item in value]
    if isinstance(value, Fraction):
        return {"$exact_fraction": [value.numerator, value.denominator]}
    if isinstance(value, Path):
        return str(value)
    if hasattr(value, "as_dict") and callable(value.as_dict):
        return _plain(value.as_dict())
    return value


def write_json(path: Path, value: Any) -> None:
    """Strip exact/mappingproxy wrappers before pretty-printing evidence."""
    path.write_text(
        json.dumps(_plain(value), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def fact_hash(result: Any) -> str:
    return hashlib.sha256(canonical_json(result.facts[0]).encode("utf-8")).hexdigest()


def fact_record(op: Operation, result: Any, wall: float) -> dict[str, Any]:
    from collections.abc import Mapping

    fact = result.facts[0]
    topology = fact.target_topology
    cells = (
        topology.get("complete_cell_semantic_projection")
        if isinstance(topology, Mapping) else None
    )
    cell_state_counts: dict[str, int] = {}
    if cells is not None:
        for cell in cells:
            state = str(cell.get("cell_state"))
            cell_state_counts[state] = cell_state_counts.get(state, 0) + 1
    return {
        "op_id": op.op_id,
        "query_ref": j(op.query_ref),
        "predicate_ref": j(op.predicate_ref),
        "measure": op.measure,
        "targets": list(op.targets),
        "family": op.family,
        "core_id": op.core_id,
        "wall_seconds": wall,
        "facts_count": len(result.facts),
        "fact_ref": j(fact.ref),
        "fact_sha256": fact_hash(result),
        "typed_state": fact.typed_state,
        "raw_numerator_support": fact.raw_numerator_support,
        "raw_denominator_support": fact.raw_denominator_support,
        "weighted_numerator_support": getattr(
            fact, "weighted_numerator_support_if_authorized", None
        ),
        "weighted_denominator_support": getattr(
            fact, "weighted_denominator_support_if_authorized", None
        ),
        "measure_basis_ref": j(fact.measure_basis_ref),
        "replay_ref": j(fact.replay_ref),
        "release_refs": [j(ref) for ref in result.release_refs],
        "target_topology_cells": len(cells) if cells is not None else None,
        "cell_state_counts": cell_state_counts,
    }


def load_fixture_and_battery():
    receipt = json.loads((BASE / "evidence" / "estate_receipt.json").read_text())
    ctx = build_context(ShapeSpec(
        "country-reuse", RESPONDENTS, include_weights=True, tag=TAG
    ))
    battery = Battery(ctx)
    ops = battery.build(core_count=80, weighted_count=20)
    catalog = battery.catalog()
    return receipt, ctx, ops, catalog


def verify_op_manifest(ops: list[Operation]) -> None:
    manifest = json.loads((BASE / "evidence" / "ops_manifest.json").read_text())
    if manifest["distinct_operations"] != len(ops):
        raise AssertionError("operation count changed")
    if manifest["core_operations"] != len({op.core_id for op in ops}):
        raise AssertionError("core count changed")
    for row, op in zip(manifest["operations"], ops):
        if row["op_id"] != op.op_id:
            raise AssertionError("operation order/identity changed")
        if row["query_ref"] != j(op.query_ref):
            raise AssertionError(f"query ref changed for {op.op_id}")
        if row["predicate_ref"] != j(op.predicate_ref):
            raise AssertionError(f"predicate ref changed for {op.op_id}")


def verify_estate(receipt: dict[str, Any]) -> None:
    release_dir = Path(receipt["root"]) / receipt["exact_path"]
    for name, digest in receipt["members_sha256"].items():
        actual = hashlib.sha256((release_dir / name).read_bytes()).hexdigest()
        if actual != digest:
            raise AssertionError(f"estate member changed: {name}")
    if directory_bytes(release_dir) != receipt["retained_bytes"]:
        raise AssertionError("estate retained bytes changed")


def cold_one(
    admission: SavedC11Admission, op: Operation
) -> dict[str, Any]:
    before_cpu = cpu_times()
    before_tree = process_tree_rss_bytes()
    before_rss = current_rss_bytes()
    instrument = CourtInstrumentation()
    start = time.monotonic()
    with instrument.phase(forbid_c11_repository=True) as counters:
        result = admission.execute_i03(
            query_ref=op.query_ref, predicate_ref=op.predicate_ref
        )
    wall = time.monotonic() - start
    after_cpu = cpu_times()
    after_tree = process_tree_rss_bytes()
    after_rss = current_rss_bytes()
    record = fact_record(op, result, wall)
    record.update({
        "kind": "COLD_SINGLE_OPERATION_CALIBRATION",
        "counters": counters.material(),
        "cpu_user_seconds": after_cpu["user_seconds"] - before_cpu["user_seconds"],
        "cpu_system_seconds": after_cpu["system_seconds"] - before_cpu["system_seconds"],
        "process_tree_rss_before_bytes": before_tree,
        "process_tree_rss_after_bytes": after_tree,
        "process_tree_rss_peak_bytes": max(before_tree, after_tree, after_cpu["maxrss_bytes"]),
        "self_rss_before_bytes": before_rss,
        "self_rss_after_bytes": after_rss,
        "self_maxrss_bytes": after_cpu["maxrss_bytes"],
    })
    return record


def cold_many(
    admission: SavedC11Admission, ops: list[Operation]
) -> tuple[dict[str, Any], dict[str, Any]]:
    before_cpu = cpu_times()
    before_tree = process_tree_rss_bytes()
    before_rss = current_rss_bytes()
    disk_before = shutil.disk_usage(str(BASE))
    instrument = CourtInstrumentation()
    start = time.monotonic()
    results: dict[str, Any] = {}
    rows: list[dict[str, Any]] = []
    with instrument.phase(forbid_c11_repository=True) as counters:
        for op in ops:
            op_start = time.monotonic()
            result = admission.execute_i03(
                query_ref=op.query_ref, predicate_ref=op.predicate_ref
            )
            op_wall = time.monotonic() - op_start
            results[op.op_id] = result
            rows.append(fact_record(op, result, op_wall))
    wall = time.monotonic() - start
    after_cpu = cpu_times()
    after_tree = process_tree_rss_bytes()
    after_rss = current_rss_bytes()
    disk_after = shutil.disk_usage(str(BASE))
    counters_material = counters.material()
    summary = {
        "schema": "PYAT_COUNTRY_REUSE_COLD_BATCH@1",
        "kind": "COLD_REPEATED_SAVED_EXECUTION",
        "utc_start": utc_now(),
        "operations_requested": len(ops),
        "operations_completed": len(rows),
        "distinct_query_refs": len({op.query_ref.key for op in ops}),
        "distinct_core_operations": len({op.core_id for op in ops}),
        "measure_variants": sum(1 for op in ops if op.measure == "GOVERNED_WEIGHTED"),
        "wall_seconds": wall,
        "operations_per_second": len(rows) / wall if wall else None,
        "cpu_user_seconds": after_cpu["user_seconds"] - before_cpu["user_seconds"],
        "cpu_system_seconds": after_cpu["system_seconds"] - before_cpu["system_seconds"],
        "process_tree_rss_before_bytes": before_tree,
        "process_tree_rss_after_bytes": after_tree,
        "process_tree_rss_peak_bytes": max(before_tree, after_tree, after_cpu["maxrss_bytes"]),
        "self_rss_before_bytes": before_rss,
        "self_rss_after_bytes": after_rss,
        "self_maxrss_bytes": after_cpu["maxrss_bytes"],
        "disk_free_before_bytes": disk_before.free,
        "disk_free_after_bytes": disk_after.free,
        "retained_estate_bytes": directory_bytes(Path(BASE / ".local-data" / "estate-128")),
        "scratch_dir_bytes_after": directory_bytes(BASE / ".local-data"),
        "counters": counters_material,
        "per_operation": rows,
        "typed_state_counts": {
            state: sum(1 for row in rows if row["typed_state"] == state)
            for state in sorted({row["typed_state"] for row in rows})
        },
        "cold_qualification_forecast": {
            "operations": 1000,
            "basis": "measured cold session-per-operation batch",
            "projected_wall_seconds": wall * 10,
            "exceeds_300s_budget": (wall * 10) > BUDGET_SECONDS,
            "grade": "EXTRAPOLATION_NOT_MEASURED",
        },
    }
    return summary, results


def guard_probe(
    receipt: dict[str, Any], ops: list[Operation], catalog: Any
) -> dict[str, Any]:
    release_ref = exact_ref(receipt["reconstructed_v1_release_ref"])
    estate = VerifiedDirectEstate(
        receipt["root"],
        exact_path=Path(receipt["root"]) / receipt["exact_path"],
        independently_held_manifest_sha256=receipt["manifest_sha256"],
        independently_held_i02=ExternalI02Roots(**receipt["i02"]),
        current_authorizer=lambda _roots: True,
    )
    executor = CarrierNeutralResearchExecutor(
        repository=estate, release_refs=(release_ref,), runtime_catalog=catalog,
    )
    scope = executor.grouped_i03_scope(max_groups=256, max_cached_members=500_000)
    carrier_error = None
    start = time.monotonic()
    try:
        executor.execute_i03(
            query_ref=ops[0].query_ref,
            predicate_ref=ops[0].predicate_ref,
            group_scope=scope,
        )
        carrier_guard = "NO_REFUSAL"
    except Exception as exc:  # exact guard evidence, not a swallowed failure
        carrier_error = {
            "type": type(exc).__name__,
            "message": str(exc),
        }
        carrier_guard = "REFUSED"
    carrier_wall = time.monotonic() - start

    evaluator_error = None
    evaluator_guard = "NO_REFUSAL"
    index_contract: dict[str, Any] = {}
    start = time.monotonic()
    with DirectEstateI03Session(estate) as session:
        try:
            execute_empirical_query(
                repository=session,
                query=ops[0].query,
                predicate=ops[0].predicate,
                authority_registry=catalog.authority_registry,
                release_refs=(release_ref,),
                group_scope=I03GroupedExecutionScope(),
            )
        except Exception as exc:
            evaluator_error = {
                "type": type(exc).__name__,
                "message": str(exc),
            }
            evaluator_guard = "REFUSED"
        # Diagnosis only: inspect the exact cold release identity the grouped
        # key would need.  Do NOT call the grouped cache or bypass any guard.
        indices = session.indices_for(query=ops[0].query, release_refs=(release_ref,))
        index = indices[0][1]
        again = session.indices_for(query=ops[0].query, release_refs=(release_ref,))
        index_again = again[0][1]
        release = index.release
        index_contract = {
            "same_index_object_across_two_calls": index is index_again,
            "index_id_first_call": id(index),
            "index_id_second_call": id(index_again),
            "release_type": type(release).__name__,
            "release_has_semantic_release_hash": hasattr(release, "semantic_release_hash"),
            "release_has_source_release_manifest_hash": hasattr(
                release, "source_release_manifest_hash"
            ),
            "index_identity_missing_release_fields": [
                name for name in (
                    "semantic_release_hash", "source_release_manifest_hash",
                ) if not hasattr(release, name)
            ],
            "release_fields": sorted(getattr(release, "__dataclass_fields__", {})),
            "runtime_authorities_is_none": index.runtime_authorities is None,
            "runtime_repository_is_none": index.runtime_repository is None,
            "runtime_predicate_grammar_authority_ref_is_none": (
                index.runtime_predicate_grammar_authority_ref is None
            ),
            "respondents": len(index.respondents),
            "events_by_respondent_type": type(index.events_by_respondent).__name__,
            "events_respondent_count": len(index.events_by_respondent),
            "coordinates_respondent_count": len(index.coordinates_by_respondent),
            "routing_respondent_count": len(index.routing_by_respondent),
            "weights_respondent_count": len(index.weights_by_respondent),
            "source_relations": len(index.source_relations),
        }
    evaluator_wall = time.monotonic() - start
    return {
        "schema": "PYAT_COUNTRY_REUSE_GUARD_PROBE@1",
        "grade": "SOURCEFREE_TEST_ONLY",
        "op_id": ops[0].op_id,
        "carrier_guard": {
            "disposition": carrier_guard,
            "wall_seconds": carrier_wall,
            "error": carrier_error,
            "scope_receipt": dict(scope.receipt()),
        },
        "evaluator_guard": {
            "disposition": evaluator_guard,
            "wall_seconds": evaluator_wall,
            "error": evaluator_error,
        },
        "cold_index_contract": index_contract,
        "notes": [
            "Both public entry points refuse before any grouped core is published.",
            "The index inspection is read-only and does not call the grouped cache.",
        ],
    }


def run_carrier(
    executor: CarrierNeutralResearchExecutor,
    ops: list[Operation],
    *,
    group_scope: Any | None = None,
) -> tuple[dict[str, Any], float, dict[str, Any]]:
    before_cpu = cpu_times()
    start = time.monotonic()
    results: dict[str, Any] = {}
    for op in ops:
        results[op.op_id] = executor.execute_i03(
            query_ref=op.query_ref,
            predicate_ref=op.predicate_ref,
            group_scope=group_scope,
        )
    wall = time.monotonic() - start
    after_cpu = cpu_times()
    receipt = dict(group_scope.receipt()) if group_scope is not None else None
    timing = {
        "wall_seconds": wall,
        "cpu_user_seconds": after_cpu["user_seconds"] - before_cpu["user_seconds"],
        "cpu_system_seconds": after_cpu["system_seconds"] - before_cpu["system_seconds"],
        "self_maxrss_bytes": after_cpu["maxrss_bytes"],
        "group_scope_receipt": receipt,
        "operations_completed": len(results),
    }
    return results, wall, timing


def compare(
    left: dict[str, Any], right: dict[str, Any], *, left_label: str, right_label: str,
) -> dict[str, Any]:
    mismatches = []
    for op_id in sorted(left):
        if op_id not in right:
            mismatches.append({"op_id": op_id, "reason": "missing"})
            continue
        left_fact = canonical_json(left[op_id].facts[0])
        right_fact = canonical_json(right[op_id].facts[0])
        if left_fact != right_fact:
            mismatches.append({
                "op_id": op_id,
                "left_sha256": hashlib.sha256(left_fact.encode()).hexdigest(),
                "right_sha256": hashlib.sha256(right_fact.encode()).hexdigest(),
                "left_ref": j(left[op_id].facts[0].ref),
                "right_ref": j(right[op_id].facts[0].ref),
                "left_state": left[op_id].facts[0].typed_state,
                "right_state": right[op_id].facts[0].typed_state,
            })
    return {
        "left": left_label,
        "right": right_label,
        "operations_compared": len(left),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "exact": not mismatches,
    }


def repeat_probe(
    executor: CarrierNeutralResearchExecutor,
    op: Operation,
    *,
    iterations: int,
) -> dict[str, Any]:
    before_cpu = cpu_times()
    start = time.monotonic()
    for _ in range(iterations):
        executor.execute_i03(query_ref=op.query_ref, predicate_ref=op.predicate_ref)
    wall_ungrouped = time.monotonic() - start
    after_ungrouped_cpu = cpu_times()

    scope = executor.grouped_i03_scope(max_groups=2, max_cached_members=500_000)
    start = time.monotonic()
    per_iteration: list[float] = []
    for _ in range(iterations):
        op_start = time.monotonic()
        executor.execute_i03(
            query_ref=op.query_ref, predicate_ref=op.predicate_ref,
            group_scope=scope,
        )
        per_iteration.append(time.monotonic() - op_start)
    wall_grouped = time.monotonic() - start
    after_grouped_cpu = cpu_times()
    ordered = sorted(per_iteration)
    return {
        "schema": "PYAT_COUNTRY_REUSE_REPEAT_PROBE@1",
        "scope": "REPEAT_INVOCATIONS_NOT_DISTINCT_OPERATIONS",
        "op_id": op.op_id,
        "iterations": iterations,
        "ungrouped_wall_seconds": wall_ungrouped,
        "ungrouped_cpu_user_seconds": after_ungrouped_cpu["user_seconds"] - before_cpu["user_seconds"],
        "grouped_wall_seconds": wall_grouped,
        "grouped_cpu_user_seconds": after_grouped_cpu["user_seconds"] - after_ungrouped_cpu["user_seconds"],
        "grouped_per_iteration_p50_seconds": ordered[len(ordered) // 2],
        "grouped_per_iteration_min_seconds": ordered[0],
        "grouped_per_iteration_max_seconds": ordered[-1],
        "grouped_receipt": dict(scope.receipt()),
        "wall_speedup": (wall_ungrouped / wall_grouped) if wall_grouped else None,
    }


def main() -> int:
    evidence = BASE / "evidence"
    evidence.mkdir(exist_ok=True)
    started_utc = utc_now()
    receipt, ctx, ops, catalog = load_fixture_and_battery()
    verify_op_manifest(ops)
    verify_estate(receipt)

    admission_start = time.monotonic()
    admission = SavedC11Admission.open(
        root=receipt["root"],
        exact_path=Path(receipt["root"]) / receipt["exact_path"],
        independently_held_manifest_sha256=receipt["manifest_sha256"],
        independently_held_i02=ExternalI02Roots(**receipt["i02"]),
        release_ref=exact_ref(receipt["reconstructed_v1_release_ref"]),
        runtime_catalog=catalog,
        current_authorizer=lambda _roots: True,
    )
    admission_seconds = time.monotonic() - admission_start

    one = cold_one(admission, ops[0])
    write_json(evidence / "cold_1op.json", one)

    # Mandatory 1 -> 100 decision point.  The measured 1-op cost has already
    # been paid; run 100 only if its projection fits the remaining budget.
    forecast_100 = one["wall_seconds"] * 100
    remaining = BUDGET_SECONDS - (time.monotonic() - START)
    cold_100_decision = {
        "one_op_seconds": one["wall_seconds"],
        "forecast_100_seconds": forecast_100,
        "remaining_budget_seconds": remaining,
        "run_100": forecast_100 <= max(60.0, remaining - 30.0),
    }
    if not cold_100_decision["run_100"]:
        raise RuntimeError(f"100-op forecast does not fit budget: {cold_100_decision}")

    cold_summary, cold_results = cold_many(admission, ops)
    cold_summary["admission_seconds"] = admission_seconds
    cold_summary["cold_100_decision"] = cold_100_decision
    write_json(evidence / "cold_100ops.json", cold_summary)

    guard = guard_probe(receipt, ops, catalog)
    write_json(evidence / "guard_probe.json", guard)

    # Existing lawful grouped execution requires the sealed in-memory C11
    # repository.  This is NOT the cold saved consumer; it is the exact
    # reference path against which cold facts are compared.
    native_start = time.monotonic()
    repo, native_release = ctx.native_oracle()
    native_seconds = time.monotonic() - native_start
    native_executor = CarrierNeutralResearchExecutor(
        repository=repo, release_refs=(native_release,), runtime_catalog=catalog,
    )
    ungrouped_results, ungrouped_wall, ungrouped_timing = run_carrier(
        native_executor, ops,
    )
    grouped256_results, grouped256_wall, grouped256_timing = run_carrier(
        native_executor, ops,
        group_scope=native_executor.grouped_i03_scope(
            max_groups=256, max_cached_members=500_000
        ),
    )
    grouped64_results, grouped64_wall, grouped64_timing = run_carrier(
        native_executor, ops,
        group_scope=native_executor.grouped_i03_scope(
            max_groups=64, max_cached_members=500_000
        ),
    )

    parity = {
        "schema": "PYAT_COUNTRY_REUSE_PARITY@1",
        "grade": "SOURCEFREE_TEST_ONLY",
        "cold_vs_native_ungrouped": compare(
            cold_results, ungrouped_results,
            left_label="cold_saved_session_per_operation",
            right_label="native_C11Repository_ungrouped",
        ),
        "grouped256_vs_native_ungrouped": compare(
            grouped256_results, ungrouped_results,
            left_label="native_C11Repository_grouped_max256",
            right_label="native_C11Repository_ungrouped",
        ),
        "grouped64_vs_native_ungrouped": compare(
            grouped64_results, ungrouped_results,
            left_label="native_C11Repository_grouped_default64",
            right_label="native_C11Repository_ungrouped",
        ),
        "grouped256_vs_cold": compare(
            grouped256_results, cold_results,
            left_label="native_C11Repository_grouped_max256",
            right_label="cold_saved_session_per_operation",
        ),
    }
    write_json(evidence / "parity.json", parity)

    # Secondary probe: the existing grouped scope on repeat invocations.  This
    # is explicitly not a 1,000-distinct-operation claim.
    elapsed = time.monotonic() - START
    repeat = None
    if elapsed < BUDGET_SECONDS - 60.0:
        repeat = repeat_probe(native_executor, ops[0], iterations=1000)
        repeat["elapsed_before_probe_seconds"] = elapsed
        write_json(evidence / "repeat_1000_grouped.json", repeat)

    summary = {
        "schema": "PYAT_COUNTRY_REUSE_COURT@1",
        "grade": "SOURCEFREE_TEST_ONLY",
        "started_utc": started_utc,
        "finished_utc": utc_now(),
        "total_court_wall_seconds": time.monotonic() - START,
        "budget_seconds": BUDGET_SECONDS,
        "estate": {
            "root": receipt["root"],
            "exact_path": receipt["exact_path"],
            "manifest_sha256": receipt["manifest_sha256"],
            "i02": receipt["i02"],
            "release_ref": receipt["reconstructed_v1_release_ref"],
            "retained_bytes": receipt["retained_bytes"],
            "family_counts": receipt["family_counts"],
        },
        "operations": {
            "distinct_operations": len(ops),
            "distinct_query_refs": len({op.query_ref.key for op in ops}),
            "core_operations": len({op.core_id for op in ops}),
            "measure_variants": sum(1 for op in ops if op.measure == "GOVERNED_WEIGHTED"),
        },
        "cold": {
            "one_op": one,
            "batch": {key: value for key, value in cold_summary.items() if key != "per_operation"},
        },
        "guard": guard,
        "native_oracle": {
            "build_seconds": native_seconds,
            "release_ref": j(native_release),
            "ungrouped": ungrouped_timing,
            "grouped_max256": grouped256_timing,
            "grouped_default64": grouped64_timing,
        },
        "parity": {
            key: {
                "exact": value["exact"],
                "mismatch_count": value["mismatch_count"],
                "operations_compared": value["operations_compared"],
            }
            for key, value in parity.items()
            if isinstance(value, dict) and "exact" in value
        },
        "repeat_probe": repeat,
        "status": "COURT_MEASURED",
    }
    write_json(evidence / "measurements.json", summary)
    print(json.dumps({
        "status": summary["status"],
        "total_court_wall_seconds": summary["total_court_wall_seconds"],
        "cold_1op_seconds": one["wall_seconds"],
        "cold_100_wall_seconds": cold_summary["wall_seconds"],
        "cold_100_ops_per_second": cold_summary["operations_per_second"],
        "cold_session_builds": cold_summary["counters"]["session_builds"],
        "cold_row_group_reads": cold_summary["counters"]["row_group_reads"],
        "cold_c11_tripwire_hits": cold_summary["counters"]["c11_repository_tripwire_hits"],
        "cold_read_table_calls": cold_summary["counters"]["read_table_calls"],
        "guard_carrier": guard["carrier_guard"]["disposition"],
        "guard_evaluator": guard["evaluator_guard"]["disposition"],
        "grouped_max256": grouped256_timing,
        "grouped_default64": grouped64_timing,
        "parity": summary["parity"],
        "repeat_probe": repeat,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
