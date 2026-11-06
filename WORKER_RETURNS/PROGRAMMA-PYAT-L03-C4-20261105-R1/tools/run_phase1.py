from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
RETURN_DIR = HERE.parent
REPO_ROOT = RETURN_DIR.parents[1]
WORKER = HERE / "bench_worker.py"
RESULTS = RETURN_DIR / "results"
LOG_ROOT = REPO_ROOT / ".local-logs" / "pyat-l03-c4"


def command_env(*, cache_dir: Path | None = None, tmp_dir: Path | None = None) -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = "0"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    if tmp_dir is not None:
        env["TMPDIR"] = str(tmp_dir)
    if cache_dir is not None:
        env["RAWLSING_C11_ACCELERATOR_DIR"] = str(cache_dir)
    env.pop("PYTHONPATH", None)
    return env


def run_command(label: str, command: list[str], *, env, timeout: int, log_name: str):
    start = time.perf_counter()
    proc = subprocess.run(
        command, cwd=str(REPO_ROOT), env=env, capture_output=True,
        text=True, timeout=timeout,
    )
    elapsed = time.perf_counter() - start
    log_path = LOG_ROOT / "logs" / f"{log_name}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(
        f"$ {' '.join(command)}\nexit={proc.returncode}\nwall_s={elapsed:.6f}\n"
        f"--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}\n",
        encoding="utf-8",
    )
    summary = (proc.stdout.strip().splitlines() or [""])[-1]
    return {
        "label": label,
        "command": command,
        "exit": proc.returncode,
        "wall_s": elapsed,
        "stdout_tail": proc.stdout[-4000:],
        "stderr_tail": proc.stderr[-4000:],
        "summary": summary,
        "log": str(log_path.relative_to(REPO_ROOT)),
    }


def run_worker(
    label: str, scenario: str, *,
    cache_dir: Path | None = None,
    tmp_dir: Path | None = None,
    n: int = 0,
    kind: str = "native",
    pass_mode: str = "clean",
    timeout: int = 1800,
):
    output = RESULTS / f"{label}.json"
    command = [
        sys.executable, str(WORKER), "--scenario", scenario, "--output", str(output),
    ]
    if n:
        command += ["--n", str(n)]
    if scenario == "main":
        command += ["--kind", kind, "--pass-mode", pass_mode]
    if scenario == "issued":
        command += ["--tmp-dir", str(tmp_dir)]
    record = run_command(
        label, command, env=command_env(cache_dir=cache_dir, tmp_dir=tmp_dir),
        timeout=timeout, log_name=label,
    )
    if record["exit"] != 0:
        raise SystemExit(f"scenario {label} failed: {record['stderr_tail']}")
    with output.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    record["payload"] = payload
    return record


def prepare_dir(path: Path, *, clear: bool = False) -> Path:
    if clear and path.exists():
        shutil.rmtree(path)
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.chmod(path, 0o700)
    return path


def numeric_projection(fact: Mapping[str, Any]) -> Mapping[str, Any]:
    return {
        "typed_state": fact["typed_state"],
        "raw_numerator_support": fact["raw_numerator_support"],
        "raw_denominator_support": fact["raw_denominator_support"],
        "raw_resolved_target_support": fact["raw_resolved_target_support"],
        "weighted_numerator_support_if_authorized":
            fact["weighted_numerator_support_if_authorized"],
        "weighted_denominator_support_if_authorized":
            fact["weighted_denominator_support_if_authorized"],
        "complete_cell_semantic_projection": fact["complete_cell_semantic_projection"],
        "risk_set_member_ids": fact["risk_set_member_ids"],
        "denominator_member_ids": fact["denominator_member_ids"],
    }


def jsonline(handle, payload: Mapping[str, Any]) -> None:
    handle.write(json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str))
    handle.write("\n")


def derive_components(op: Mapping[str, Any]) -> Mapping[str, Any]:
    components = op["components"]["components"]
    total = op["wall_s"]

    def seconds(name):
        return components.get(name, {}).get("seconds", 0.0)

    def calls(name):
        return components.get(name, {}).get("calls", 0)

    resolve = seconds("_resolve_release_indices")
    evaluate = seconds("_evaluate_index_group")
    build_fact = seconds("_build_fact")
    routing = seconds("_routing_fact_for")
    predicate = seconds("_eval_predicate")
    weight = seconds("_weight_for")
    target = seconds("_target_configuration")
    replay = seconds("_make_execution_replay_ref")
    cell_projection = seconds("_cell_projection")
    build_index = seconds("_build_release_index")
    release_index = seconds("_release_index_for")
    authority = seconds("_validate_public_object_authorities")
    evaluate_other = max(0.0, evaluate - routing - predicate - weight - target)
    build_fact_other = max(0.0, build_fact - replay)
    execute_other = max(0.0, total - resolve - evaluate - build_fact)
    return {
        "total_instrumented_s": total,
        "resolve_release_indices_s": resolve,
        "release_index_for_s": release_index,
        "build_release_index_s": build_index,
        "evaluate_index_group_s": evaluate,
        "routing_fact_for_s": routing,
        "eval_predicate_s": predicate,
        "weight_for_s": weight,
        "target_configuration_s": target,
        "evaluate_other_s": evaluate_other,
        "build_fact_s": build_fact,
        "make_execution_replay_ref_s": replay,
        "cell_projection_s": cell_projection,
        "build_fact_other_s": build_fact_other,
        "execute_other_s": execute_other,
        "validate_public_object_authorities_s": authority,
        "evaluate_share": evaluate / total if total else None,
        "build_fact_share": build_fact / total if total else None,
        "shareable_risk_predicate_target_share": (
            (routing + predicate + weight + target) / total if total else None
        ),
        "calls": {
            "resolve_release_indices": calls("_resolve_release_indices"),
            "release_index_for": calls("_release_index_for"),
            "build_release_index": calls("_build_release_index"),
            "evaluate_index_group": calls("_evaluate_index_group"),
            "routing_fact_for": calls("_routing_fact_for"),
            "eval_predicate": calls("_eval_predicate"),
            "weight_for": calls("_weight_for"),
            "target_configuration": calls("_target_configuration"),
            "make_execution_replay_ref": calls("_make_execution_replay_ref"),
            "cell_projection": calls("_cell_projection"),
            "validate_public_object_authorities": calls("_validate_public_object_authorities"),
        },
        "select_respondent_events_calls": op["components"]["counts"].get(
            "_select_respondent_events", 0
        ),
        "nested": {
            "release_index_for_in_resolve": True,
            "build_release_index_in_release_index_for": True,
            "routing_predicate_weight_target_in_evaluate": True,
            "replay_cell_projection_in_build_fact": True,
            "authority_validation_in_routing_predicate_weight_target": True,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-tests", action="store_true")
    parser.add_argument("--skip-p41", action="store_true")
    args = parser.parse_args()
    RESULTS.mkdir(parents=True, exist_ok=True)
    tmp_dir = prepare_dir(LOG_ROOT / "tmp")
    command_records = []

    if not args.skip_tests:
        pytest_env = command_env(tmp_dir=tmp_dir)
        test_commands = [
            ("tests_empirical_query", [
                sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                "--basetemp", str(tmp_dir / "pytest-empirical"),
                "rawlsing_next/tests/test_pre553_empirical_query.py",
            ]),
            ("tests_carrier_execution", [
                sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                "--basetemp", str(tmp_dir / "pytest-carrier"),
                "rawlsing_next/tests/test_pre553_carrier_execution.py",
            ]),
            ("tests_c11_execution_view", [
                sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                "--basetemp", str(tmp_dir / "pytest-view"),
                "rawlsing_next/tests/test_pre553_c11_execution_view.py",
            ]),
            ("tests_query_frontier_hostile", [
                sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                "--basetemp", str(tmp_dir / "pytest-frontier"),
                "rawlsing_next/tests/test_pre553_query_frontier_hostile.py",
            ]),
            ("tests_universal_workload_custody", [
                sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                "--basetemp", str(tmp_dir / "pytest-custody"),
                "rawlsing_next/tests/test_universal_workload_custody.py",
            ]),
        ]
        for label, command in test_commands:
            command_records.append(run_command(
                label, command, env=pytest_env, timeout=1200, log_name=label,
            ))

    scenario_records = []
    frontier = run_worker("frontier", "frontier", tmp_dir=tmp_dir, timeout=600)
    scenario_records.append(frontier)
    invalidation = run_worker("invalidation", "invalidation", tmp_dir=tmp_dir, timeout=600)
    scenario_records.append(invalidation)

    route_cache_dir = prepare_dir(LOG_ROOT / "cache" / "route_b", clear=True)
    route_cache = run_worker(
        "route_b_cache", "route_b_cache", cache_dir=route_cache_dir,
        tmp_dir=tmp_dir, timeout=900,
    )
    scenario_records.append(route_cache)

    issued_cache_dir = prepare_dir(LOG_ROOT / "cache" / "issued", clear=True)
    issued = run_worker(
        "issued", "issued", cache_dir=issued_cache_dir, tmp_dir=tmp_dir, timeout=900,
    )
    scenario_records.append(issued)

    for n in (200, 1000, 3000):
        record = run_worker(
            f"main_native_n{n}_clean", "main", n=n, kind="native",
            pass_mode="clean", tmp_dir=tmp_dir, timeout=1800,
        )
        scenario_records.append(record)
    for n in (200, 1000, 3000):
        record = run_worker(
            f"main_native_n{n}_attrib", "main", n=n, kind="native",
            pass_mode="attrib", tmp_dir=tmp_dir, timeout=1800,
        )
        scenario_records.append(record)

    compact_cache_dir = prepare_dir(LOG_ROOT / "cache" / "main_compact_n1000", clear=True)
    compact_cold = run_worker(
        "main_compact_n1000_cold", "main", n=1000, kind="compact",
        pass_mode="clean", cache_dir=compact_cache_dir, tmp_dir=tmp_dir, timeout=1800,
    )
    scenario_records.append(compact_cold)
    compact_warm = run_worker(
        "main_compact_n1000_warm", "main", n=1000, kind="compact",
        pass_mode="clean", cache_dir=compact_cache_dir, tmp_dir=tmp_dir, timeout=1800,
    )
    scenario_records.append(compact_warm)

    if not args.skip_p41:
        command_records.append(run_command(
            "tests_p41_same_source",
            [
                sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                "--basetemp", str(tmp_dir / "pytest-p41"),
                "rawlsing_next/tests/test_universal_world_binding.py"
                "::test_same_source_r04_partial_resume_reaches_actual_p41",
            ],
            env=command_env(tmp_dir=tmp_dir), timeout=1800,
            log_name="tests_p41_same_source",
        ))

    payloads = {record["label"]: record["payload"] for record in scenario_records}
    clean_ops = {}
    attrib_ops = {}
    for label, payload in payloads.items():
        if payload.get("scenario") != "main":
            continue
        key = (payload["n"], payload["kind"])
        target = clean_ops if payload["pass"] == "clean" else attrib_ops
        target[key] = payload

    commands_path = RESULTS / "commands.jsonl"
    with commands_path.open("w", encoding="utf-8") as handle:
        for record in command_records + [
            {key: value for key, value in item.items() if key != "payload"}
            for item in scenario_records
        ]:
            jsonline(handle, {"schema": "PYAT_L03_C4_PHASE1_COMMAND@1", **record})

    cost_path = RETURN_DIR / "02_EXACT_COST_AND_MEMORY_RESULTS.jsonl"
    parity_path = RETURN_DIR / "03_SAME_FACT_GROUPED_AND_KWAY_PARITY.jsonl"
    with cost_path.open("w", encoding="utf-8") as cost, parity_path.open("w", encoding="utf-8") as parity:
        for label, payload in payloads.items():
            if payload.get("scenario") == "frontier":
                for entry in payload["entries"]:
                    jsonline(parity, {
                        "schema": "PYAT_L03_C4_PHASE1_PARITY@1",
                        "entry_kind": "frontier_fixture_exact_facts",
                        "fixture": entry["fixture"],
                        "exact_facts": entry["facts"],
                        "declared_oracle": entry["oracle"],
                        "event_states": entry.get("event_states"),
                        "routing_states": entry.get("routing_states"),
                        "oracle_test": "rawlsing_next/tests/test_pre553_query_frontier_hostile.py",
                    })
            elif payload.get("scenario") == "invalidation":
                for name, value in sorted(payload["results"].items()):
                    jsonline(parity, {
                        "schema": "PYAT_L03_C4_PHASE1_PARITY@1",
                        "entry_kind": "replay_authority_invalidation",
                        "case": name,
                        "result": value,
                    })
            elif payload.get("scenario") == "route_b_cache":
                for step in payload["steps"]:
                    jsonline(cost, {
                        "schema": "PYAT_L03_C4_PHASE1_COST@1",
                        "entry_kind": "accelerator_cache_behavior",
                        "case": step["label"],
                        "wall_s": step["wall_s"],
                        "cpu_s": step["cpu_s"],
                        "cache_read_hits": step["cache_read_hits"],
                        "cache_read_misses": step["cache_read_misses"],
                        "cache_writes": step["cache_writes"],
                        "cache": step["cache"],
                        "equal_to_baseline": step["equal_to_baseline"],
                    })
                    jsonline(parity, {
                        "schema": "PYAT_L03_C4_PHASE1_PARITY@1",
                        "entry_kind": "accelerator_cache_parity",
                        "case": step["label"],
                        "equal_to_baseline": step["equal_to_baseline"],
                        "facts": step["facts"],
                        "discovery_receipts": step["discovery_receipts"],
                        "release_ref": step["release_ref"],
                    })
            elif payload.get("scenario") == "issued":
                for entry in payload["entries"]:
                    jsonline(cost, {
                        "schema": "PYAT_L03_C4_PHASE1_COST@1",
                        "entry_kind": "issued_workload_execution",
                        **entry,
                    })
                jsonline(cost, {
                    "schema": "PYAT_L03_C4_PHASE1_COST@1",
                    "entry_kind": "issued_revoked_negative",
                    "revoked": payload["revoked"],
                    "replay_output_refs_equal": payload["revoked_replay_output_refs_equal"],
                    "final_cache": payload["final_cache"],
                })
            else:
                scenario = payload.get("scenario")
                if scenario != "main":
                    continue
                n = payload["n"]
                kind = payload["kind"]
                process = payload["process"]
                jsonline(cost, {
                    "schema": "PYAT_L03_C4_PHASE1_COST@1",
                    "entry_kind": "scenario_process",
                    "scenario": "main",
                    "n": n,
                    "kind": kind,
                    "pass": payload["pass"],
                    "parent_wall_s": next(
                        record["wall_s"] for record in scenario_records
                        if record["label"] == label
                    ),
                    "peak_rss_bytes": process["ru_maxrss_bytes"],
                    "ru_utime_s": process["ru_utime_s"],
                    "ru_stime_s": process["ru_stime_s"],
                    "timings": process["timings"],
                    "source": payload["source"],
                    "cache": payload["cache"],
                    "compact_cache_reads": payload.get("compact_cache_reads"),
                    "compact_cache_write_count": payload.get("compact_cache_write_count"),
                    "index_state_initial": payload["index_state_initial"],
                    "index_state_final": payload["index_state_final"],
                    "command": next(
                        record["command"] for record in scenario_records
                        if record["label"] == label
                    ),
                })
                clean = clean_ops.get((n, kind))
                clean_by_id = {op["op_id"]: op for op in clean["ops"]} if clean else {}
                for op in payload["ops"]:
                    base = {
                        "schema": "PYAT_L03_C4_PHASE1_COST@1",
                        "entry_kind": "op_cost" if payload["pass"] == "clean" else "op_attribution",
                        "scenario": "main",
                        "n": n,
                        "kind": kind,
                        "op_id": op["op_id"],
                        "group": op["group"],
                        "targets": op["targets"],
                        "risk": op["risk"],
                        "measure": op["measure"],
                        "wall_s": op["wall_s"],
                        "cpu_s": op["cpu_s"],
                        "peak_rss_bytes_after_op": op["ru_maxrss_bytes_after"],
                        "index_count_after": op["index_after"]["count"],
                        "index_reused_from_previous": op["index_reused_from_previous"],
                        "fact_ref": op["fact"]["fact_ref"],
                        "replay_ref": op["fact"]["replay_ref"],
                        "typed_state": op["fact"]["typed_state"],
                        "raw_numerator_support": op["fact"]["raw_numerator_support"],
                        "raw_denominator_support": op["fact"]["raw_denominator_support"],
                        "oracle_ok": op["oracle_ok"],
                        "oracle_errors": op["oracle_errors"],
                    }
                    if payload["pass"] == "attrib":
                        base["components"] = derive_components(op)
                        base["clean_wall_s"] = clean_by_id.get(op["op_id"], {}).get("wall_s")
                        base["clean_cpu_s"] = clean_by_id.get(op["op_id"], {}).get("cpu_s")
                        if base["clean_wall_s"] is not None:
                            base["instrumentation_overhead_s"] = (
                                op["wall_s"] - base["clean_wall_s"]
                            )
                    else:
                        base["risk_set_member_count"] = op["fact"]["risk_set_member_count"]
                        base["denominator_member_count"] = op["fact"]["denominator_member_count"]
                    jsonline(cost, base)
        jsonline(cost, {
            "schema": "PYAT_L03_C4_PHASE1_COST@1",
            "entry_kind": "implementation_status",
            "P0_P1_current_code_baseline": "MEASURED",
            "P2_minimal_grouped_kernel": "NOT_IMPLEMENTED_IN_PHASE1",
            "P3_dictionary_or_bitmap_posting_index": "NOT_RUN",
            "P4_persistent_zstd_parquet_accelerator_change": "NOT_RUN",
            "production_source_change_authorized": False,
        })
        for record in command_records:
            jsonline(cost, {
                "schema": "PYAT_L03_C4_PHASE1_COST@1",
                "entry_kind": "test_command",
                "label": record["label"],
                "command": record["command"],
                "exit": record["exit"],
                "wall_s": record["wall_s"],
                "summary": record["summary"],
            })

        for (n, kind), payload in sorted(clean_ops.items()):
            ops = {op["op_id"]: op for op in payload["ops"]}
            for op in payload["ops"]:
                jsonline(parity, {
                    "schema": "PYAT_L03_C4_PHASE1_PARITY@1",
                    "entry_kind": "baseline_exact_fact",
                    "n": n,
                    "kind": kind,
                    "op_id": op["op_id"],
                    "group": op["group"],
                    "exact_fact": op["fact"],
                    "oracle_ok": op["oracle_ok"],
                    "oracle_errors": op["oracle_errors"],
                })
            relations = []
            if "all_K_raw" in ops and "all_K_raw_sibling" in ops:
                left, right = ops["all_K_raw"]["fact"], ops["all_K_raw_sibling"]["fact"]
                relations.append({
                    "relation": "sibling_query_identity_same_numbers_distinct_fact",
                    "pass": (
                        numeric_projection(left) == numeric_projection(right)
                        and left["fact_ref"] != right["fact_ref"]
                        and left["replay_ref"] != right["replay_ref"]
                    ),
                    "left_fact_ref": left["fact_ref"],
                    "right_fact_ref": right["fact_ref"],
                    "left_replay_ref": left["replay_ref"],
                    "right_replay_ref": right["replay_ref"],
                })
            if "all_K_raw" in ops and "all_K_weighted" in ops:
                raw, weighted = ops["all_K_raw"]["fact"], ops["all_K_weighted"]["fact"]
                relations.append({
                    "relation": "raw_and_authorized_weighted_share_denominator_not_measure",
                    "pass": (
                        raw["raw_denominator_support"] == weighted["raw_denominator_support"]
                        and raw["denominator_member_ids"] == weighted["denominator_member_ids"]
                        and raw["risk_set_member_ids"] == weighted["risk_set_member_ids"]
                        and raw["weighted_denominator_support_if_authorized"] is None
                        and weighted["weighted_denominator_support_if_authorized"] is not None
                        and raw["fact_ref"] != weighted["fact_ref"]
                    ),
                    "raw_fact_ref": raw["fact_ref"],
                    "weighted_fact_ref": weighted["fact_ref"],
                    "weighted_denominator": weighted[
                        "weighted_denominator_support_if_authorized"
                    ],
                })
            if "all_K_raw" in ops and "all_X_raw" in ops and "all_Z_raw" in ops:
                base = ops["all_K_raw"]["fact"]
                x = ops["all_X_raw"]["fact"]
                z = ops["all_Z_raw"]["fact"]
                relations.append({
                    "relation": "target_siblings_share_risk_predicate_not_cells",
                    "pass": (
                        base["risk_set_member_ids"] == x["risk_set_member_ids"] == z["risk_set_member_ids"]
                        and base["denominator_member_ids"] == x["denominator_member_ids"] == z["denominator_member_ids"]
                        and base["fact_ref"] != x["fact_ref"] != z["fact_ref"]
                    ),
                    "fact_refs": [base["fact_ref"], x["fact_ref"], z["fact_ref"]],
                })
            for op_id, arity, domain in (
                ("all_K_raw", 1, 2), ("all_XY_raw", 2, 4),
                ("all_XYZ_raw", 3, 8), ("all_ABCK_raw", 4, 16),
            ):
                if op_id not in ops:
                    continue
                fact = ops[op_id]["fact"]
                cells = fact["complete_cell_semantic_projection"]
                relations.append({
                    "relation": "k_way_bounded_joint_exact_domain",
                    "op_id": op_id,
                    "arity": arity,
                    "pass": (
                        fact["target_arity"] == arity
                        and len(cells) == domain
                        and sum(row["raw_numerator_support"] for row in cells)
                        == fact["raw_denominator_support"]
                    ),
                    "domain_cells": len(cells),
                    "supported_cells": sum(
                        1 for row in cells if row["raw_numerator_support"] > 0
                    ),
                    "zero_cells": sum(
                        1 for row in cells if row["raw_numerator_support"] == 0
                    ),
                })
            if "cond_X1_target_Y" in ops and "cond_Y1_target_X" in ops:
                forward = ops["cond_X1_target_Y"]["fact"]
                reverse = ops["cond_Y1_target_X"]["fact"]
                relations.append({
                    "relation": "forward_reverse_conditional_distinct_denominators",
                    "pass": (
                        forward["denominator_member_ids"] != reverse["denominator_member_ids"]
                        and forward["fact_ref"] != reverse["fact_ref"]
                        and forward["condition_predicate_ref"] != reverse["condition_predicate_ref"]
                    ),
                    "forward_denominator": forward["raw_denominator_support"],
                    "reverse_denominator": reverse["raw_denominator_support"],
                })
            if "xor_condition_target_Z" in ops:
                fact = ops["xor_condition_target_Z"]["fact"]
                cells = fact["complete_cell_semantic_projection"]
                relations.append({
                    "relation": "xor_condition_no_lower_order_signal_exact_joint",
                    "pass": (
                        fact["raw_denominator_support"] > 0
                        and all(
                            row["raw_numerator_support"] == 0
                            for row in cells if row["cell"] == "0"
                        )
                        and next(
                            row for row in cells if row["cell"] == "1"
                        )["raw_numerator_support"] == fact["raw_denominator_support"]
                    ),
                    "denominator": fact["raw_denominator_support"],
                    "target_Z1": next(
                        row for row in cells if row["cell"] == "1"
                    )["raw_numerator_support"],
                })
            if "minority_branch_target_K" in ops:
                fact = ops["minority_branch_target_K"]["fact"]
                relations.append({
                    "relation": "minority_branch_retained",
                    "pass": (
                        fact["raw_denominator_support"] == max(1, n // 100)
                        and fact["risk_set_member_count"] == n
                    ),
                    "denominator": fact["raw_denominator_support"],
                    "risk_members": fact["risk_set_member_count"],
                })
            if "all_K_raw" in ops and "risk_S_target_K" in ops:
                base = ops["all_K_raw"]["fact"]
                other = ops["risk_S_target_K"]["fact"]
                relations.append({
                    "relation": "incompatible_risk_sets_not_shared",
                    "pass": (
                        base["risk_set_member_ids"] != other["risk_set_member_ids"]
                        and base["denominator_member_ids"] != other["denominator_member_ids"]
                        and base["fact_ref"] != other["fact_ref"]
                    ),
                    "risk_R_count": base["risk_set_member_count"],
                    "risk_S_count": other["risk_set_member_count"],
                })
            for relation in relations:
                jsonline(parity, {
                    "schema": "PYAT_L03_C4_PHASE1_PARITY@1",
                    "entry_kind": "same_fact_relation",
                    "n": n,
                    "kind": kind,
                    **relation,
                })
        for label, payload in sorted(payloads.items()):
            if payload.get("scenario") != "main":
                continue
            jsonline(parity, {
                "schema": "PYAT_L03_C4_PHASE1_PARITY@1",
                "entry_kind": "scenario_oracle_summary",
                "n": payload["n"],
                "kind": payload["kind"],
                "pass": payload["pass"],
                "all_ops_oracle_ok": all(op["oracle_ok"] for op in payload["ops"]),
                "op_count": len(payload["ops"]),
            })
        jsonline(parity, {
            "schema": "PYAT_L03_C4_PHASE1_PARITY@1",
            "entry_kind": "grouped_kernel_status",
            "P2": "NOT_IMPLEMENTED_IN_PHASE1",
            "P3": "NOT_RUN",
            "P4": "NOT_RUN",
            "claim": "baseline per-operation facts only; no grouped or k-way implementation parity claimed",
        })

    summary = {
        "schema": "PYAT_L03_C4_PHASE1_DRIVER_SUMMARY@1",
        "scenario_labels": [record["label"] for record in scenario_records],
        "test_labels": [record["label"] for record in command_records],
        "results_dir": str(RESULTS.relative_to(REPO_ROOT)),
        "cost_jsonl": str(cost_path.relative_to(REPO_ROOT)),
        "parity_jsonl": str(parity_path.relative_to(REPO_ROOT)),
    }
    (RESULTS / "driver_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
