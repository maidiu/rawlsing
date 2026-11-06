from __future__ import annotations

import argparse
import gc
import json
import os
import platform
import resource
import sys
import time
from pathlib import Path
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

T_START = time.perf_counter()
import bench_common as bc  # noqa: E402
from rawlsing_next.pre553_carrier_execution import CarrierNeutralResearchExecutor  # noqa: E402
from rawlsing_next.pre553_empirical_query import I03GroupedExecutionScope  # noqa: E402
import rawlsing_next._pre553_query_eval as qeval  # noqa: E402

T_IMPORTED = time.perf_counter()


def ref_material(ref):
    return bc.ref_material(ref, True)


def frac(value):
    return bc.frac(value)


def fraction_material(value):
    return bc.fraction_dict(value)


def compact_fact(fact):
    cells = []
    for row in fact.target_topology.get("complete_cell_semantic_projection", ()):
        cells.append({
            "cell": row["cell"],
            "cell_state": row["cell_state"],
            "raw": row["raw_numerator_support"],
            "weighted": row["weighted_numerator_support_if_authorized"],
        })
    provenance = tuple(fact.source_empirical_provenance_refs)
    dependencies = tuple(fact.dependency_refs)
    return {
        "fact_ref": ref_material(fact.ref),
        "replay_ref": ref_material(fact.replay_ref),
        "typed_state": fact.typed_state,
        "p02_failure_state": getattr(fact, "p02_failure_state", None),
        "raw_numerator_support": fact.raw_numerator_support,
        "raw_denominator_support": fact.raw_denominator_support,
        "raw_resolved_target_support": getattr(fact, "raw_resolved_target_support", None),
        "weighted_numerator_support_if_authorized":
            fact.weighted_numerator_support_if_authorized,
        "weighted_denominator_support_if_authorized":
            fact.weighted_denominator_support_if_authorized,
        "cells": cells,
        "risk_member_count": len(getattr(fact, "risk_set_member_refs", ())),
        "denominator_member_count": len(getattr(fact, "denominator_member_refs", ())),
        "risk_member_ids_sha256": bc.refs_digest(tuple(getattr(fact, "risk_set_member_refs", ()))),
        "denominator_member_ids_sha256":
            bc.refs_digest(tuple(getattr(fact, "denominator_member_refs", ()))),
        "provenance_ref_count": len(provenance),
        "provenance_refs_sha256": bc.refs_digest(provenance),
        "dependency_ref_count": len(dependencies),
        "dependency_refs_sha256": bc.refs_digest(dependencies),
        "measure_kind": fact.measure_kind,
        "risk_set_type": fact.risk_set_type,
        "source_scope_mode": fact.source_scope_mode,
        "target_arity": fact.target_topology.get("arity"),
    }


def full_selected(fact):
    return fact.as_dict()


class Counters:
    def __init__(self):
        self.calls = {
            "_routing_fact_for": 0,
            "_eval_predicate": 0,
            "_weight_for": 0,
            "_target_configuration": 0,
            "_evaluate_index_group_core": 0,
            "_build_fact": 0,
            "_make_execution_replay_ref": 0,
        }
        self.times = {
            "_build_fact": 0.0,
            "_make_execution_replay_ref": 0.0,
        }

    def wrap(self):
        import rawlsing_next.pre553_empirical_query as query

        saved = {}
        for module, name in (
            (qeval, "_routing_fact_for"), (qeval, "_eval_predicate"),
            (qeval, "_weight_for"), (qeval, "_target_configuration"),
            (qeval, "_evaluate_index_group_core"),
            (query, "_build_fact"), (qeval, "_make_execution_replay_ref"),
        ):
            original = getattr(module, name)
            saved[(module.__name__, name)] = (module, original)

            def counted(*args, __name=name, __original=original, **kwargs):
                self.calls[__name] += 1
                if __name in self.times:
                    start = time.perf_counter()
                    try:
                        return __original(*args, **kwargs)
                    finally:
                        self.times[__name] += time.perf_counter() - start
                return __original(*args, **kwargs)

            setattr(module, name, counted)
        return saved

    @staticmethod
    def restore(saved):
        for _key, (module, original) in saved.items():
            name = _key[1]
            setattr(module, name, original)


def run_pass(executor, ops, scope):
    records = {}
    for op in ops:
        gc.collect()
        start_wall = time.perf_counter()
        start_cpu = time.process_time()
        result = executor.execute_i03(
            query_ref=op["query"].ref,
            predicate_ref=op["predicate"].ref,
            group_scope=scope,
        )
        wall = time.perf_counter() - start_wall
        cpu = time.process_time() - start_cpu
        facts = tuple(result.facts)
        records[op["op_id"]] = {
            "wall_s": wall,
            "cpu_s": cpu,
            "fact_count": len(facts),
            "fact_refs": [ref_material(fact.ref) for fact in facts],
            "replay_refs": [ref_material(fact.replay_ref) for fact in facts],
            "exact_fact_material_sha256": bc.semantic_hash(
                [fact.as_dict() for fact in facts]
            ),
            "facts": [compact_fact(fact) for fact in facts],
        }
    return records


def new_executor(source, catalog):
    release = source["repo"].resolve_release_exact(source["release_ref"])
    return CarrierNeutralResearchExecutor(
        bc.fresh_repository(release), (release.release_ref,), catalog,
    )


def exact_equal(left, right):
    if set(left) != set(right):
        return False
    return all(
        left[op_id]["exact_fact_material_sha256"] == right[op_id]["exact_fact_material_sha256"]
        and left[op_id]["fact_refs"] == right[op_id]["fact_refs"]
        and left[op_id]["replay_refs"] == right[op_id]["replay_refs"]
        for op_id in left
    )


def sums(records):
    return {
        "wall_s": sum(item["wall_s"] for item in records.values()),
        "cpu_s": sum(item["cpu_s"] for item in records.values()),
    }


def scenario_main(n, rounds):
    timings = {}
    fixture_start = time.perf_counter()
    data = bc.build_main_source(n)
    timings["fixture_build_s"] = time.perf_counter() - fixture_start
    source = data["source"]
    catalog = data["catalog"]
    ops = data["ops"]

    cold_base = new_executor(source, catalog)
    cold_scope = I03GroupedExecutionScope()
    cold_cand = new_executor(source, catalog)
    cold_base_records = run_pass(cold_base, ops, None)
    cold_cand_records = run_pass(cold_cand, ops, cold_scope)
    cold = {
        "baseline": {"ops": cold_base_records, **sums(cold_base_records)},
        "candidate": {"ops": cold_cand_records, **sums(cold_cand_records)},
        "all_facts_equal": exact_equal(cold_base_records, cold_cand_records),
        "scope": cold_scope.receipt(),
    }

    warm_base = new_executor(source, catalog)
    warm_scope = I03GroupedExecutionScope()
    warm_cand = new_executor(source, catalog)
    run_pass(warm_base, ops, None)
    run_pass(warm_cand, ops, warm_scope)
    warm_rounds = []
    for round_index in range(1, rounds + 1):
        baseline = run_pass(warm_base, ops, None)
        candidate = run_pass(warm_cand, ops, warm_scope)
        warm_rounds.append({
            "round": round_index,
            "baseline": {"ops": baseline, **sums(baseline)},
            "candidate": {"ops": candidate, **sums(candidate)},
            "all_facts_equal": exact_equal(baseline, candidate),
            "scope": warm_scope.receipt(),
        })

    single_op = ops[0]
    single_base = new_executor(source, catalog)
    single_cand = new_executor(source, catalog)
    single_scope = I03GroupedExecutionScope()
    single = {
        "op_id": single_op["op_id"],
        "baseline": run_pass(single_base, [single_op], None),
        "candidate": run_pass(single_cand, [single_op], single_scope),
        "scope": single_scope.receipt(),
    }
    single["all_facts_equal"] = exact_equal(single["baseline"], single["candidate"])

    by_id = {op["op_id"]: op for op in ops}
    incompatible_ops = [
        by_id[name] for name in (
            "all_K_raw", "all_X_raw", "risk_S_target_K", "cond_X1_target_Y",
            "cond_Y1_target_X", "xor_condition_target_Z", "all_XY_raw",
        )
    ]
    incompatible_base = new_executor(source, catalog)
    incompatible_cand = new_executor(source, catalog)
    incompatible_scope = I03GroupedExecutionScope()
    incompatible_first_base = run_pass(incompatible_base, incompatible_ops, None)
    incompatible_first_cand = run_pass(incompatible_cand, incompatible_ops, incompatible_scope)
    scope_first_pass = incompatible_scope.receipt()
    incompatible_second_base = run_pass(incompatible_base, incompatible_ops, None)
    incompatible_second_cand = run_pass(incompatible_cand, incompatible_ops, incompatible_scope)
    incompatible = {
        "op_ids": [op["op_id"] for op in incompatible_ops],
        "first_pass": {
            "baseline": {"ops": incompatible_first_base, **sums(incompatible_first_base)},
            "candidate": {"ops": incompatible_first_cand, **sums(incompatible_first_cand)},
            "all_facts_equal": exact_equal(incompatible_first_base, incompatible_first_cand),
            "scope": scope_first_pass,
        },
        "second_pass": {
            "baseline": {"ops": incompatible_second_base, **sums(incompatible_second_base)},
            "candidate": {"ops": incompatible_second_cand, **sums(incompatible_second_cand)},
            "all_facts_equal": exact_equal(incompatible_second_base, incompatible_second_cand),
            "scope": incompatible_scope.receipt(),
        },
    }

    counter_base = new_executor(source, catalog)
    counter_cand = new_executor(source, catalog)
    counter_scope = I03GroupedExecutionScope()
    run_pass(counter_base, ops, None)
    run_pass(counter_cand, ops, counter_scope)
    baseline_counters = Counters()
    saved = baseline_counters.wrap()
    try:
        run_pass(counter_base, ops, None)
    finally:
        Counters.restore(saved)
    candidate_counters = Counters()
    saved = candidate_counters.wrap()
    try:
        run_pass(counter_cand, ops, counter_scope)
    finally:
        Counters.restore(saved)

    selected = {
        "all_K_raw": ops[0],
        "all_K_weighted": ops[1],
        "all_ABCK_raw": by_id["all_ABCK_raw"],
        "xor_condition_target_Z": by_id["xor_condition_target_Z"],
        "minority_branch_target_K": by_id["minority_branch_target_K"],
        "cond_X1_target_Y": by_id["cond_X1_target_Y"],
    }
    selected_full = {}
    for op_id, op in selected.items():
        base_result = counter_base.execute_i03(
            query_ref=op["query"].ref, predicate_ref=op["predicate"].ref,
        )
        cand_result = counter_cand.execute_i03(
            query_ref=op["query"].ref, predicate_ref=op["predicate"].ref,
            group_scope=counter_scope,
        )
        selected_full[op_id] = {
            "baseline": [full_selected(fact) for fact in base_result.facts],
            "candidate": [full_selected(fact) for fact in cand_result.facts],
            "equal": [fact.as_dict() for fact in base_result.facts]
                == [fact.as_dict() for fact in cand_result.facts],
        }

    stats = bc.source_stats(source, source["repo"].resolve_release_exact(source["release_ref"]))
    payload = {
        "schema": "PROGRAMMA_PYAT_L03_C4_PHASE2_GROUPED@1",
        "scenario": "main_grouped",
        "n": n,
        "rounds": rounds,
        "timings": timings,
        "cold": cold,
        "warm_rounds": warm_rounds,
        "single_operation": single,
        "incompatible": incompatible,
        "counters": {
            "baseline": {
                "calls": baseline_counters.calls,
                "times_s": baseline_counters.times,
            },
            "candidate": {
                "calls": candidate_counters.calls,
                "times_s": candidate_counters.times,
            },
            "scope": counter_scope.receipt(),
        },
        "selected_full_facts": selected_full,
        "source": stats,
        "cache": bc.cache_stats(None),
        "process": {
            "pid": os.getpid(),
            "python": sys.version,
            "executable": sys.executable,
            "platform": platform.platform(),
            "machine": platform.machine(),
            "cpu_count": os.cpu_count(),
            "ru_maxrss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
            "ru_utime_s": resource.getrusage(resource.RUSAGE_SELF).ru_utime,
            "ru_stime_s": resource.getrusage(resource.RUSAGE_SELF).ru_stime,
            "argv": sys.argv,
            "env": {
                key: os.environ.get(key) for key in (
                    "PYTHONHASHSEED", "PYTHONDONTWRITEBYTECODE", "TMPDIR",
                    "RAWLSING_C11_ACCELERATOR_DIR",
                )
            },
            "worker_total_s": time.perf_counter() - T_START,
            "import_s": T_IMPORTED - T_START,
        },
    }
    bc.dump_json(Path(args.output), payload)


def scenario_small_fixtures():
    from rawlsing_next.tests import pre553_query_frontier_fixtures as fx
    from rawlsing_next.tests.test_pre553_empirical_query import _query_authority
    from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog

    entries = []
    source, qa, facts, xor_fact, joint = fx.xor_zero_unary_fixture()
    facts2, zero = fx.observed_zero_zero_support_fixture()
    source3, xfact, yfact, risk_joint = fx.routing_risk_asymmetry_fixture()
    source4, raw_fact, weighted_fact = fx.raw_weighted_divergence_fixture()
    source5, kway_fact = fx.k_way_bounded_joint_fixture()
    for label, items in (
        ("XOR_ZERO_UNARY", [facts["X0"], facts["X1"], facts["Y0"], facts["Y1"], xor_fact, joint]),
        ("OBSERVED_ZERO_VS_ZERO_SUPPORT", [facts2, zero]),
        ("ROUTING_RISK_ASYMMETRY", [xfact, yfact, risk_joint]),
        ("RAW_WEIGHTED_DIVERGENCE", [raw_fact, weighted_fact]),
        ("K_WAY_BOUNDED_JOINT", [kway_fact]),
    ):
        entries.append({
            "fixture": label,
            "typed_states": [fact.typed_state for fact in items],
            "raw": [[fact.raw_numerator_support, fact.raw_denominator_support] for fact in items],
            "cells": [
                [
                    [row["cell"], row["raw_numerator_support"], row["cell_state"]]
                    for row in fact.target_topology.get("complete_cell_semantic_projection", ())
                ]
                for fact in items
            ],
            "exact_fact_material_sha256": bc.semantic_hash([fact.as_dict() for fact in items]),
        })
    payload = {
        "schema": "PROGRAMMA_PYAT_L03_C4_PHASE2_GROUPED@1",
        "scenario": "small_fixtures",
        "entries": entries,
        "not_administered_contract": (
            "C11/I03 has no NOT_ADMINISTERED response/routing state; "
            "pre553_native_workload_binding uses FIXTURE_TARGET_NOT_ADMINISTERED "
            "only for a fixture target absent from the projection; universal grammar "
            "has a separate administration vocabulary. No I03 state was invented."
        ),
        "process": {
            "pid": os.getpid(),
            "ru_maxrss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
            "worker_total_s": time.perf_counter() - T_START,
        },
    }
    bc.dump_json(Path(args.output), payload)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True, choices=("main", "small_fixtures"))
    parser.add_argument("--n", type=int, default=200)
    parser.add_argument("--rounds", type=int, default=3)
    parser.add_argument("--output", required=True)
    global args
    args = parser.parse_args()
    if args.scenario == "main":
        scenario_main(args.n, args.rounds)
    else:
        scenario_small_fixtures()


if __name__ == "__main__":
    main()
