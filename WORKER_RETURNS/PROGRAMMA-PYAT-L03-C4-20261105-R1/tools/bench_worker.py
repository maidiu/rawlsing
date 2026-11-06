from __future__ import annotations

import argparse
import contextlib
import gc
import json
import os
import platform
import resource
import sys
import time
from dataclasses import replace
from types import MappingProxyType
from fractions import Fraction
from pathlib import Path
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

T_START = time.perf_counter()
import bench_common as bc  # noqa: E402

T_IMPORTED = time.perf_counter()


def jsonable(value):
    if isinstance(value, Mapping):
        return {str(key): jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    if isinstance(value, Fraction):
        return {"$exact_fraction": [value.numerator, value.denominator]}
    if isinstance(value, set):
        return sorted(jsonable(item) for item in value)
    return value


def env_snapshot():
    keys = (
        "PYTHONHASHSEED", "PYTHONDONTWRITEBYTECODE", "TMPDIR",
        "RAWLSING_C11_ACCELERATOR_DIR", "OMP_NUM_THREADS",
        "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
    )
    return {key: os.environ.get(key) for key in keys}


def process_metadata(timings):
    return {
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
        "env": env_snapshot(),
        "timings": timings,
    }


def cache_probe():
    from rawlsing_next import _pre553_c11_execution_view as compact

    original_read = compact._read_bodies
    original_write = compact._write_bodies

    @contextlib.contextmanager
    def probe():
        state = {"reads": [], "writes": 0}

        def read(path, key, selectors):
            value = original_read(path, key, selectors)
            state["reads"].append(value is not None)
            return value

        def write(path, key, bodies):
            state["writes"] += 1
            return original_write(path, key, bodies)

        compact._read_bodies = read
        compact._write_bodies = write
        try:
            yield state
        finally:
            compact._read_bodies = original_read
            compact._write_bodies = original_write

    return probe

def ensure_cache_dir():
    configured = os.environ.get("RAWLSING_C11_ACCELERATOR_DIR")
    if not configured:
        return None
    path = Path(configured)
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.chmod(path, 0o700)
    return path


def scenario_main(args):
    n = args.n
    kind = args.kind
    attribution = args.pass_mode == "attrib"
    cache_dir = ensure_cache_dir()
    timings = {}
    fixture_start = time.perf_counter()
    data = bc.build_main_source(n)
    timings["fixture_build_s"] = time.perf_counter() - fixture_start
    source = data["source"]
    native_release = source["repo"].resolve_release_exact(source["release_ref"])
    compact_reads = []
    compact_writes = []
    if kind == "compact":
        if cache_dir is None:
            raise RuntimeError("compact kind requires RAWLSING_C11_ACCELERATOR_DIR")
        probe = cache_probe()
        with probe() as state:
            compact_start = time.perf_counter()
            release = bc.compact_release(native_release, str(cache_dir))
            timings["compact_build_s"] = time.perf_counter() - compact_start
        compact_reads = list(state["reads"])
        compact_writes = [1] * state["writes"]
    else:
        release = native_release
    repo_start = time.perf_counter()
    repository = bc.fresh_repository(release)
    timings["repository_commit_s"] = time.perf_counter() - repo_start
    catalog_start = time.perf_counter()
    catalog = data["catalog"]
    executor = bc.CarrierNeutralResearchExecutor(
        repository=repository,
        release_refs=(release.release_ref,),
        runtime_catalog=catalog,
    )
    timings["catalog_and_executor_s"] = time.perf_counter() - catalog_start
    recorder = bc.Recorder() if attribution else None
    if recorder is not None:
        bc.install_recorder(recorder)
    op_records = []
    index_before_first = bc.index_state(repository)
    first_op = True
    repeats = max(1, args.repeats)
    for repeat in range(repeats):
        for op in data["ops"]:
            gc.collect()
            if recorder is not None:
                recorder.begin(op["op_id"])
            before = bc.index_state(repository)
            start_wall = bc.perf()
            start_cpu = bc.cpu()
            result = bc.execute_op(executor, op)
            end_wall = bc.perf()
            end_cpu = bc.cpu()
            after = bc.index_state(repository)
            if first_op:
                timings["first_op_wall_s"] = end_wall - start_wall
                timings["first_op_cpu_s"] = end_cpu - start_cpu
                first_op = False
            fact = result.facts[0]
            if repeat == 0:
                expected = bc.oracle_for(data["rows"], op, data["weights"])
                errors = bc.compare_fact(fact, expected, data["ref_to_id"])
                oracle_ok = not errors
            else:
                errors = []
                oracle_ok = None
            full_refs = n <= 200 or (repeat == 0 and n <= 1000)
            full_provenance = (
                n <= 200 or
                (repeat == 0 and (n <= 1000 or op["op_id"] in {"all_K_raw", "all_ABCK_raw"}))
            )
            record = {
                "repeat": repeat,
                "op_id": op["op_id"],
                "group": op["group"],
                "targets": list(op["targets"]),
                "risk": op["risk"],
                "measure": op["measure"],
                "result_fact_count": len(result.facts),
                "wall_s": end_wall - start_wall,
                "cpu_s": end_cpu - start_cpu,
                "ru_maxrss_bytes_after": bc.maxrss_bytes(),
                "oracle_errors": errors,
                "oracle_ok": oracle_ok,
                "oracle_skipped": repeat > 0,
                "fact": bc.fact_projection(
                    fact, data["ref_to_id"],
                    full_refs=full_refs, full_provenance=full_provenance,
                ),
                "index_before": before,
                "index_after": after,
                "index_reused_from_previous": bool(
                    op_records and before["token"] == op_records[-1]["index_after"]["token"]
                ),
                "components": recorder.records[op["op_id"]] if recorder is not None else None,
            }
            op_records.append(record)
    stats_start = time.perf_counter()
    stats = bc.source_stats(source, release)
    timings["source_stats_s"] = time.perf_counter() - stats_start
    payload = {
        "schema": "PROGRAMMA_PYAT_L03_C4_PHASE1_RAW@1",
        "scenario": "main",
        "n": n,
        "kind": kind,
        "pass": args.pass_mode,
        "index_state_initial": index_before_first,
        "index_state_final": bc.index_state(repository),
        "source": stats,
        "cache": bc.cache_stats(cache_dir if kind == "compact" else None),
        "compact_cache_reads": compact_reads,
        "compact_cache_write_count": len(compact_writes),
        "ops": op_records,
        "process": process_metadata(timings),
    }
    bc.dump_json(Path(args.output), payload)


def _fact_payload(fact, ref_to_id):
    return bc.fact_projection(fact, ref_to_id, full_refs=True, full_provenance=True)


def scenario_frontier(args):
    from rawlsing_next.tests import pre553_query_frontier_fixtures as fx

    entries = []
    start = time.perf_counter()

    def add(name, facts, ref_to_id, source=None):
        if not isinstance(facts, (list, tuple)):
            facts = [facts]
        entries.append({
            "fixture": name,
            "facts": [_fact_payload(fact, ref_to_id) for fact in facts],
            "oracle": jsonable(fx.FIXTURE_ORACLES.get(name).__dict__ if name in fx.FIXTURE_ORACLES else {}),
            "source_present": source is not None,
        })

    def ref_map(source):
        return {r.ref.object_id: rid for rid, r in source["respondents"].items()}

    source, qa, facts, xor_fact, joint = fx.xor_zero_unary_fixture()
    add("XOR_ZERO_UNARY", [facts["X0"], facts["X1"], facts["Y0"], facts["Y1"], xor_fact, joint], ref_map(source), source)
    source, facts = fx.simpson_reversal_fixture()
    add("SIMPSON_REVERSAL", list(facts.values()), ref_map(source), source)
    left, right, left_fact, right_fact = fx.same_marginals_different_joint_fixture()
    combined = {**ref_map(left), **ref_map(right)}
    add("SAME_MARGINALS_DIFFERENT_JOINT", [left_fact, right_fact], combined)
    source, fact = fx.response_position_fixture()
    add("RESPONSE_POSITION_CONJUNCTION", [fact], ref_map(source), source)
    source, fact = fx.response_response_cotravel_fixture()
    add("RESPONSE_RESPONSE_COTRAVEL", [fact], ref_map(source), source)
    source, xfact, yfact, joint = fx.routing_risk_asymmetry_fixture()
    add("ROUTING_RISK_ASYMMETRY", [xfact, yfact, joint], ref_map(source), source)
    source, raw, weighted = fx.raw_weighted_divergence_fixture()
    add("RAW_WEIGHTED_DIVERGENCE", [raw, weighted], ref_map(source), source)
    observed, zero_support = fx.observed_zero_zero_support_fixture()
    add("OBSERVED_ZERO_VS_ZERO_SUPPORT", [observed, zero_support], {})
    source, fact, event_states, routing_states = fx.special_state_fixture()
    add("SPECIAL_STATE_NONCOLLAPSE", [fact], ref_map(source), source)
    add("SPECIAL_STATE_CARRIER_STATES", [], {})
    entries[-1]["event_states"] = list(event_states)
    entries[-1]["routing_states"] = list(routing_states)
    left, right, left_fact, right_fact = fx.source_indexed_disagreement_fixture()
    combined = {**ref_map(left), **ref_map(right)}
    add("SOURCE_INDEXED_DISAGREEMENT", [left_fact, right_fact], combined)
    fact = fx.multi_universe_noncomparable_fixture()
    add("MULTI_UNIVERSE_NONCOMPARABLE", [fact], {})
    source, facts = fx.topology_fixture()
    add("ORDERED_RANKED_MULTIPLICITY", list(facts.values()), ref_map(source), source)
    source, fact = fx.k_way_bounded_joint_fixture()
    add("K_WAY_BOUNDED_JOINT", [fact], ref_map(source), source)
    payload = {
        "schema": "PROGRAMMA_PYAT_L03_C4_PHASE1_RAW@1",
        "scenario": "frontier",
        "fixture_inventory": list(fx.FIXTURE_INVENTORY),
        "elapsed_s": time.perf_counter() - start,
        "entries": entries,
        "process": process_metadata({}),
    }
    bc.dump_json(Path(args.output), payload)


def scenario_invalidation(args):
    from rawlsing_next.tests.test_pre553_empirical_query import (
        _astra_query_authority,
        _build_source,
        _branch_predicate,
        _query,
        _query_authority,
    )
    from rawlsing_next.tests.pre553_query_frontier_fixtures import _multi_source_predicate
    from rawlsing_next.pre553_carrier_execution import CarrierExecutionBindingError
    from rawlsing_next.pre553_empirical_query import (
        EmpiricalQueryExecutionError,
        execute_empirical_query,
        replay_empirical_query,
    )
    from rawlsing_next.pre553_empirical_authority import AuthorityRegistry

    results = {}
    data = bc.build_main_source(200)
    source = data["source"]
    release = source["repo"].resolve_release_exact(source["release_ref"])
    repository = bc.fresh_repository(release)
    executor = bc.CarrierNeutralResearchExecutor(
        repository=repository,
        release_refs=(release.release_ref,),
        runtime_catalog=data["catalog"],
    )
    op = data["ops"][0]
    first = bc.execute_op(executor, op)
    second = bc.execute_op(executor, op)
    first_fact = first.facts[0]
    second_fact = second.facts[0]
    results["identical_replay"] = {
        "fact_ref_equal": bc.ref_material(first_fact.ref) == bc.ref_material(second_fact.ref),
        "replay_ref_equal": bc.ref_material(first_fact.replay_ref) == bc.ref_material(second_fact.replay_ref),
        "fact_ref": bc.ref_material(first_fact.ref),
        "replay_ref": bc.ref_material(first_fact.replay_ref),
    }
    replay_start = bc.perf()
    replayed = replay_empirical_query(
        repository=repository,
        query=op["query"],
        predicate=op["predicate"],
        authority_registry=data["catalog"].authority_registry,
        release_refs=(release.release_ref,),
        expected_fact_refs=(first_fact.ref,),
    )
    results["replay_positive"] = {
        "elapsed_s": bc.perf() - replay_start,
        "fact_ref_equal": bc.ref_material(replayed.facts[0].ref) == bc.ref_material(first_fact.ref),
    }
    wrong_op = data["ops"][4]
    wrong = bc.execute_op(executor, wrong_op).facts[0]
    try:
        replay_empirical_query(
            repository=repository,
            query=op["query"],
            predicate=op["predicate"],
            authority_registry=data["catalog"].authority_registry,
            release_refs=(release.release_ref,),
            expected_fact_refs=(wrong.ref,),
        )
    except EmpiricalQueryExecutionError as exc:
        results["replay_negative"] = {"raised": type(exc).__name__, "message": str(exc)}
    else:
        results["replay_negative"] = {"raised": None, "message": None}
    key = next(iter(repository._i03_release_indices))
    before_index = repository._i03_release_indices[key]
    dropped = min(before_index.respondents)
    repository._i03_release_indices[key] = replace(
        before_index,
        respondents=MappingProxyType({
            item: value for item, value in before_index.respondents.items() if item != dropped
        }),
    )
    repaired = bc.execute_op(executor, op).facts[0]
    results["index_fault_repair"] = {
        "fact_ref_equal": bc.ref_material(repaired.ref) == bc.ref_material(first_fact.ref),
        "respondents_restored": (
            repository._i03_release_indices[key].respondents == before_index.respondents
        ),
        "index_entries": bc.index_state(repository),
    }

    deny_tag = "c4-auth-deny"
    deny_source = _build_source(deny_tag, [
        {"id": "R1", "responses": {"Y": 1}},
        {"id": "R2", "responses": {"Y": 0}},
    ])
    deny_qa = _astra_query_authority(deny_tag, state="DENY")
    deny_pred = _branch_predicate(deny_source, deny_qa, tag=deny_tag)
    deny_query = _query(deny_source, deny_qa, deny_pred, ("Y",), tag=deny_tag)
    deny_catalog = bc.RuntimeObjectCatalog(
        authorities=tuple((*deny_source["authorities"], deny_qa)),
        predicates=(deny_pred,),
        queries=(deny_query,),
        discovery_authorities=(),
    )
    deny_release = deny_source["repo"].resolve_release_exact(deny_source["release_ref"])
    deny_repo = bc.fresh_repository(deny_release)
    deny_executor = bc.CarrierNeutralResearchExecutor(
        repository=deny_repo,
        release_refs=(deny_release.release_ref,),
        runtime_catalog=deny_catalog,
    )
    deny_fact = deny_executor.execute_i03(
        query_ref=deny_query.ref, predicate_ref=deny_pred.ref
    ).facts[0]
    results["authority_deny"] = {
        "typed_state": deny_fact.typed_state,
        "p02_failure_state": getattr(deny_fact, "p02_failure_state", None),
        "execution_detail": deny_fact.execution_detail,
    }

    other_tag = "c4-other-release"
    other_source = _build_source(other_tag, [
        {"id": "R1", "responses": {"Y": 1}},
        {"id": "R2", "responses": {"Y": 0}},
    ])
    other_release = other_source["repo"].resolve_release_exact(other_source["release_ref"])
    try:
        bc.CarrierNeutralResearchExecutor(
            repository=repository,
            release_refs=(other_release.release_ref,),
            runtime_catalog=data["catalog"],
        )
    except CarrierExecutionBindingError as exc:
        results["missing_release_binding"] = {
            "raised": type(exc).__name__, "message": str(exc),
        }
    else:
        results["missing_release_binding"] = {"raised": None, "message": None}
    missing = execute_empirical_query(
        repository=repository,
        query=op["query"],
        predicate=op["predicate"],
        authority_registry=data["catalog"].authority_registry,
        release_refs=(other_release.release_ref,),
    ).facts[0]
    results["missing_release_direct_i03"] = {
        "typed_state": missing.typed_state,
        "p02_failure_state": getattr(missing, "p02_failure_state", None),
        "execution_detail": missing.execution_detail,
    }

    bad_tag = "c4-bad-weight"
    bad_source = _build_source(
        bad_tag,
        [{"id": "R1", "responses": {"Y": 1}}, {"id": "R2", "responses": {"Y": 0}}],
        weights={"R1": ("WEIGHT_VALID_AUTHORIZED", "1"), "R2": ("WEIGHT_MISSING", "0")},
    )
    bad_qa = _query_authority(bad_tag)
    bad_pred = _branch_predicate(bad_source, bad_qa, tag=bad_tag)
    bad_query = _query(bad_source, bad_qa, bad_pred, ("Y",), measure="GOVERNED_WEIGHTED", tag=bad_tag)
    bad_catalog = bc.RuntimeObjectCatalog(
        authorities=tuple((*bad_source["authorities"], bad_qa)),
        predicates=(bad_pred,), queries=(bad_query,), discovery_authorities=(),
    )
    bad_release = bad_source["repo"].resolve_release_exact(bad_source["release_ref"])
    bad_repo = bc.fresh_repository(bad_release)
    bad_executor = bc.CarrierNeutralResearchExecutor(
        repository=bad_repo, release_refs=(bad_release.release_ref,), runtime_catalog=bad_catalog,
    )
    bad_fact = bad_executor.execute_i03(
        query_ref=bad_query.ref, predicate_ref=bad_pred.ref
    ).facts[0]
    results["weight_invalidation"] = {
        "typed_state": bad_fact.typed_state,
        "p02_failure_state": getattr(bad_fact, "p02_failure_state", None),
        "execution_detail": bad_fact.execution_detail,
    }

    risk_r = bc.execute_op(executor, data["ops"][0]).facts[0]
    risk_s = bc.execute_op(executor, data["ops"][12]).facts[0]
    results["risk_set_separation"] = {
        "index_state": bc.index_state(repository),
        "risk_r_ids": sorted(bc.ref_value(r, "object_id") for r in risk_r.risk_set_member_refs),
        "risk_s_ids": sorted(bc.ref_value(r, "object_id") for r in risk_s.risk_set_member_refs),
        "denominator_r_count": len(risk_r.denominator_member_refs),
        "denominator_s_count": len(risk_s.denominator_member_refs),
        "fact_ref_equal": bc.ref_material(risk_r.ref) == bc.ref_material(risk_s.ref),
    }

    sep_a = _build_source("c4-sep-a", [{"id": "R1", "responses": {"Y": 1}}])
    sep_b = _build_source("c4-sep-b", [{"id": "R1", "responses": {"Y": 0}}])
    sep_qa = _query_authority("c4-sep")
    sep_preds = []
    sep_queries = []
    for index, sep in enumerate((sep_a, sep_b)):
        pred = _branch_predicate(sep, sep_qa, tag=f"c4-sep-{index}")
        query = _query(sep, sep_qa, pred, ("Y",), tag=f"c4-sep-{index}")
        sep_preds.append(pred)
        sep_queries.append(query)
    sep_release_a = sep_a["repo"].resolve_release_exact(sep_a["release_ref"])
    sep_release_b = sep_b["repo"].resolve_release_exact(sep_b["release_ref"])
    sep_repo = bc.C11Repository((sep_release_a, sep_release_b))
    sep_catalog = bc.RuntimeObjectCatalog(
        authorities=tuple((*sep_a["authorities"], *sep_b["authorities"], sep_qa)),
        predicates=tuple(sep_preds), queries=tuple(sep_queries), discovery_authorities=(),
    )
    sep_executor_a = bc.CarrierNeutralResearchExecutor(
        repository=sep_repo, release_refs=(sep_release_a.release_ref,), runtime_catalog=sep_catalog,
    )
    sep_executor_b = bc.CarrierNeutralResearchExecutor(
        repository=sep_repo, release_refs=(sep_release_b.release_ref,), runtime_catalog=sep_catalog,
    )
    sep_fact_a = sep_executor_a.execute_i03(
        query_ref=sep_queries[0].ref, predicate_ref=sep_preds[0].ref
    ).facts[0]
    sep_fact_b = sep_executor_b.execute_i03(
        query_ref=sep_queries[1].ref, predicate_ref=sep_preds[1].ref
    ).facts[0]
    results["release_separation"] = {
        "index_state": bc.index_state(sep_repo),
        "fact_ref_equal": bc.ref_material(sep_fact_a.ref) == bc.ref_material(sep_fact_b.ref),
        "release_a": bc.ref_material(sep_release_a.release_ref),
        "release_b": bc.ref_material(sep_release_b.release_ref),
    }

    left = _build_source(
        "c4-univ-left", [{"id": "L1", "responses": {"X": 0, "Y": 0}},
                         {"id": "L2", "responses": {"X": 0, "Y": 0}}],
        question_namespace="c4-univ-shared", risk_namespace="c4-univ-shared",
    )
    right = _build_source(
        "c4-univ-right", [{"id": "R1", "responses": {"X": 1, "Y": 1}},
                          {"id": "R2", "responses": {"X": 1, "Y": 1}}],
        question_namespace="c4-univ-shared", risk_namespace="c4-univ-shared",
    )
    univ_qa = _query_authority("c4-univ")
    univ_pred = _multi_source_predicate(left, right, univ_qa, tag="c4-univ")
    univ_query = _query(
        left, univ_qa, univ_pred, ("X", "Y"),
        source_mode="SOURCE_INDEXED_MULTI_UNIVERSE",
        universe_refs=(left["universe"].ref, right["universe"].ref),
        tag="c4-univ",
        target_authority_refs=(
            left["source_auth"].authority_ref, right["source_auth"].authority_ref,
        ),
    )
    univ_release_left = left["repo"].resolve_release_exact(left["release_ref"])
    univ_release_right = right["repo"].resolve_release_exact(right["release_ref"])
    univ_repo = bc.C11Repository((univ_release_left, univ_release_right))
    univ_registry = AuthorityRegistry((*left["authorities"], *right["authorities"], univ_qa))
    univ_result = execute_empirical_query(
        repository=univ_repo, query=univ_query, predicate=univ_pred,
        authority_registry=univ_registry,
        release_refs=(univ_release_left.release_ref, univ_release_right.release_ref),
    )
    results["universe_separation"] = {
        "index_state": bc.index_state(univ_repo),
        "fact_count": len(univ_result.facts),
        "fact_refs": [bc.ref_material(fact.ref) for fact in univ_result.facts],
        "universe_refs": [
            fact.empirical_universe_refs[0]["object_id"] for fact in univ_result.facts
        ],
    }
    payload = {
        "schema": "PROGRAMMA_PYAT_L03_C4_PHASE1_RAW@1",
        "scenario": "invalidation",
        "results": results,
        "process": process_metadata({}),
    }
    bc.dump_json(Path(args.output), payload)


def scenario_route_b_cache(args):
    from rawlsing_next.tests.test_pre553_route_b_production import _fixture, _execute
    from rawlsing_next.tests.test_pre553_c11_execution_view import _material
    import pyarrow as pa
    import pyarrow.parquet as pq
    from rawlsing_next import _pre553_c11_execution_view as compact

    directory = ensure_cache_dir()
    if directory is None:
        raise RuntimeError("route_b_cache requires RAWLSING_C11_ACCELERATOR_DIR")
    for path in directory.glob("*.parquet"):
        path.unlink()
    fx = _fixture()
    steps = []
    baseline_material = None
    baseline_path = None
    baseline_bytes = None
    probe = cache_probe()

    def run(label, fixture, expect_equal=True):
        nonlocal baseline_material, baseline_path, baseline_bytes
        gc.collect()
        with probe() as state:
            start_wall = bc.perf()
            start_cpu = bc.cpu()
            observed = _execute(fixture)
            wall = bc.perf() - start_wall
            cpu = bc.cpu() - start_cpu
        material = _material(observed)
        if baseline_material is None:
            baseline_material = material
        facts = tuple(fact.as_dict() for fact in observed.object_graph.empirical_facts)
        receipts = tuple(receipt.as_dict() for receipt in observed.object_graph.discovery_receipts)
        paths = sorted(directory.glob("*.parquet"))
        step = {
            "label": label,
            "wall_s": wall,
            "cpu_s": cpu,
            "equal_to_baseline": material == baseline_material,
            "expected_equal": expect_equal,
            "cache_read_hits": sum(1 for hit in state["reads"] if hit),
            "cache_read_misses": sum(1 for hit in state["reads"] if not hit),
            "cache_writes": state["writes"],
            "cache": bc.cache_stats(directory),
            "cache_paths": [path.name for path in paths],
            "facts": facts,
            "discovery_receipts": receipts,
            "replay_receipt": jsonable(observed.replay_receipt),
            "release_ref": bc.ref_material(observed.c11_release.release_ref),
        }
        steps.append(step)
        return step, material, paths

    first, material, paths = run("cold_empty_cache", fx)
    path, = paths
    baseline_path = path
    baseline_bytes = path.read_bytes()
    run("warm_cache_hit", fx)
    path.unlink()
    run("deleted_cache_rebuild", fx)
    if path.read_bytes() != baseline_bytes:
        raise AssertionError("delete rebuild did not restore exact cache bytes")
    table = pq.read_table(path)
    bodies = table.column(compact._EVENT_BODY_COLUMN).to_pylist()
    changed = json.loads(bodies[0])
    changed["semantic_fields"]["raw_response_value"] = "forged-phase1"
    changed["semantic_fields"]["canonical_response_value_if_authorized"] = "forged-phase1"
    bodies[0] = compact.canonical_json(changed).encode("utf-8")
    forged = pa.table({compact._EVENT_BODY_COLUMN: pa.array(bodies, type=pa.binary())})
    pq.write_table(forged.replace_schema_metadata(table.schema.metadata), path, compression="zstd")
    run("corrupt_cache_rebuild", fx)
    if path.read_bytes() != baseline_bytes:
        raise AssertionError("corrupt rebuild did not restore exact cache bytes")
    stale_fixture = {**fx, "stream": replace(fx["stream"], decoder_metadata_digest="e" * 64)}
    run("stale_key_new_slot", stale_fixture)
    before_original = path.read_bytes()
    run("original_after_stale", fx)
    if path.read_bytes() != baseline_bytes:
        raise AssertionError("original cache slot changed after stale-key visit")
    payload = {
        "schema": "PROGRAMMA_PYAT_L03_C4_PHASE1_RAW@1",
        "scenario": "route_b_cache",
        "steps": steps,
        "final_cache": bc.cache_stats(directory),
        "original_slot_bytes_before_stale": len(before_original),
        "process": process_metadata({}),
    }
    bc.dump_json(Path(args.output), payload)


def scenario_issued(args):
    from rawlsing_next.pre553_issued_workload import WorkloadAdmissionError
    from rawlsing_next.pre553_native_workload_binding import execute_test_only_workload
    from rawlsing_next.tests.test_universal_workload_custody import HOST, PURPOSE, _issued_workloads
    from rawlsing_next import _pre553_c11_execution_view as compact

    workdir = Path(args.tmp_dir) / "issued"
    workdir.mkdir(parents=True, exist_ok=True)
    bundle, issued = _issued_workloads(workdir)
    probe = cache_probe()
    entries = []

    def execute(item):
        return execute_test_only_workload(
            issued=item, source_factory=lambda _ref: bundle.physical_stream,
            host=HOST, purpose=PURPOSE,
        )

    def summarize(item, result, wall, cpu, state):
        return {
            "issued_index": len(entries),
            "scope": getattr(result, "scope", None),
            "envelope_sha256": getattr(result, "envelope_sha256", None),
            "output_refs": [bc.ref_material(ref) for ref in getattr(result, "output_refs", ())],
            "manifest_unit_count": len(getattr(result, "manifest", ()).units)
                if getattr(result, "manifest", None) is not None else None,
            "receipt_states": [receipt.state for receipt in getattr(result, "receipts", ())],
            "wall_s": wall,
            "cpu_s": cpu,
            "cache_read_hits": sum(1 for hit in state["reads"] if hit),
            "cache_read_misses": sum(1 for hit in state["reads"] if not hit),
            "cache_writes": state["writes"],
            "cache": bc.cache_stats(ensure_cache_dir()),
            "workload_requests": len(getattr(item.workload, "requests", ())),
            "workload_discoveries": len(getattr(item.workload, "discoveries", ())),
        }

    first_outputs = None
    for item in issued:
        gc.collect()
        with probe() as state:
            start_wall = bc.perf()
            start_cpu = bc.cpu()
            result = execute(item)
            wall = bc.perf() - start_wall
            cpu = bc.cpu() - start_cpu
        entries.append(summarize(item, result, wall, cpu, state))
        if first_outputs is None:
            first_outputs = tuple(bc.ref_material(ref) for ref in result.output_refs)
    revoked = replace(issued[0], record=replace(issued[0].record, currentness="REVOKED"))
    original_read = compact._read_bodies

    def forbidden(*_args, **_kwargs):
        raise AssertionError("revoked issuance opened the warmed accelerator")

    compact._read_bodies = forbidden
    try:
        execute(revoked)
    except WorkloadAdmissionError as exc:
        revoked_result = {"raised": type(exc).__name__, "message": str(exc)}
    else:
        revoked_result = {"raised": None, "message": None}
    finally:
        compact._read_bodies = original_read
    replay = execute(issued[0])
    payload = {
        "schema": "PROGRAMMA_PYAT_L03_C4_PHASE1_RAW@1",
        "scenario": "issued",
        "issued_count": len(issued),
        "entries": entries,
        "revoked": revoked_result,
        "revoked_replay_output_refs_equal":
            tuple(bc.ref_material(ref) for ref in replay.output_refs) == first_outputs,
        "final_cache": bc.cache_stats(ensure_cache_dir()),
        "process": process_metadata({}),
    }
    bc.dump_json(Path(args.output), payload)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True,
                        choices=("main", "frontier", "invalidation", "route_b_cache", "issued"))
    parser.add_argument("--output", required=True)
    parser.add_argument("--n", type=int, default=0)
    parser.add_argument("--kind", default="native", choices=("native", "compact"))
    parser.add_argument("--pass-mode", default="clean", choices=("clean", "attrib"))
    parser.add_argument("--tmp-dir", default="")
    parser.add_argument("--repeats", type=int, default=1)
    args = parser.parse_args()
    start = time.perf_counter()
    if args.scenario == "main":
        scenario_main(args)
    elif args.scenario == "frontier":
        scenario_frontier(args)
    elif args.scenario == "invalidation":
        scenario_invalidation(args)
    elif args.scenario == "route_b_cache":
        scenario_route_b_cache(args)
    elif args.scenario == "issued":
        scenario_issued(args)
    elapsed = time.perf_counter() - start
    path = Path(args.output)
    payload = bc.load_json(path)
    payload.setdefault("process", {})["worker_total_s"] = elapsed
    payload["process"]["import_s"] = T_IMPORTED - T_START
    bc.dump_json(path, payload)


if __name__ == "__main__":
    main()
