#!/usr/bin/env python3
"""ANVIL cut2 measurement PREPARATION harness (TEST_ONLY, sourcefree).

Reuses the accepted #1006 sourcefree fixture and the existing country-reuse
runtime instrumentation at exact pinned blobs.  It does not edit product code,
create a store/evaluator/issuer, read original survey data, or claim a
matched/native/100k performance result.

Modes:
  prepare  build a deterministic tiny sourcefree estate + fixture contract
  baseline plain SavedC11Admission, one session per operation
  prepared one PreparedI03Session, distinct operations
  batch    execute_saved_batch with one prepared context
  fresh    parent starts a new process for one prepared Batch
  smoke    one tiny mechanics smoke: baseline/prepared/batch/fresh

Only one tiny fixture is built by `prepare`; no 1/10/100 matrix, no repeats.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import resource
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
VENDOR = HERE / "vendor"
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(VENDOR))

from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_batch_runner import BatchManifest, BatchUnitSpec
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_empirical_objects import canonical_json, exact_ref
from rawlsing_next.pre553_prepared_saved_i03 import PreparedSavedC11Admission
from rawlsing_next.pre553_saved_c11_admission import (
    SavedC11Admission, SavedC11AdmissionError,
)
from rawlsing_next.pre553_saved_workload_integration import execute_saved_batch
from rawlsing_next.pre553_source_direct_parquet_estate import (
    DirectEstateError, write_direct_estate,
)

from court_instrumentation import (
    CourtInstrumentation, cpu_times, current_rss_bytes, directory_bytes,
    maxrss_bytes, process_tree_rss_bytes,
)
from fixture_1006 import ShapeSpec, build_context
from query_1006 import build_query_bundle
from width_fixture import build_width

SCHEMA = "ANVIL_CUT2_MEASUREMENT_PREP@1"
DEFAULT_TAG = "CUT2-MEASURE"
DEFAULT_RESPONDENTS = 16
DEFAULT_ABORT_SECONDS = 120.0
DEFAULT_ABORT_RSS = 2 * 1024**3
DEFAULT_ABORT_SCRATCH = 2 * 1024**3
FIXTURE_PINS = {
    "fixture_1006.py": "74cd928d050ec7a8720e526dea00101e4c0f718a1b2ab72e5677deb64360b827",
    "query_1006.py": "83054ca64b609fbfb647c06e640255b65e701ba7644cdcd3e1443a2d7e6a47a7",
    "court_instrumentation.py": "0bce33bb3c62a9c91b689ef87f50d985fc85639f1f5695c37f0812c0344324ce",
}


def j(value: Any) -> Any:
    return json.loads(canonical_json(value))


def plain(value: Any) -> Any:
    from collections.abc import Mapping
    from fractions import Fraction

    if isinstance(value, Mapping):
        return {str(k): plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [plain(v) for v in value]
    if isinstance(value, Fraction):
        return {"$exact_fraction": [value.numerator, value.denominator]}
    if hasattr(value, "as_dict") and callable(value.as_dict):
        return plain(value.as_dict())
    return value


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def selected_ops(bundle: Any) -> list[tuple[str, Any, Any]]:
    """Five genuinely distinct operations: selected weighted, F2 fwd/rev,
    true same-person k3, and repeated MR occurrence.  No identical-query clones.
    """
    names = (
        ("selected_weighted", "weighted"),
        ("f2_forward_raw", "f2_forward"),
        ("f2_reverse_raw", "f2_reverse"),
        ("f4_three_raw", "f4_three"),
        ("repeated_mr_raw", "repeated"),
    )
    result = []
    for label, key in names:
        query, predicate = bundle.by_name(key)
        result.append((label, query, predicate))
    refs = {q.ref.key for _, q, _ in result}
    if len(refs) != len(result):
        raise AssertionError("fixture selected duplicate query refs")
    return result


def fixture_shape(args: argparse.Namespace) -> ShapeSpec:
    return ShapeSpec(
        "cut2-measurement", args.respondents, include_weights=True,
        tag=args.tag,
    )


def build_fixture(args: argparse.Namespace) -> dict[str, Any]:
    root = Path(args.root).absolute()
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    estate_root = root / "estate"
    if estate_root.exists():
        import shutil
        shutil.rmtree(estate_root)
    estate_root.mkdir(mode=0o700)
    shape = fixture_shape(args)
    ctx = build_context(shape)
    width = build_width(ctx, args.questions)
    bundle = width.query_bundle
    receipt = write_direct_estate(
        width.sections, ctx.universe.ref, estate_root,
        chunk_rows=args.chunk_rows,
    )
    release_dir = Path(receipt.path)
    members = {
        p.name: sha_file(p) for p in sorted(release_dir.iterdir())
    }
    ops = selected_ops(bundle)
    contract = {
        "schema": SCHEMA,
        "grade": "SOURCEFREE_TEST_ONLY_MECHANICS_NOT_PERFORMANCE",
        "fixture_source": "accepted #1006 fixture/query harness at exact pinned blobs",
        "fixture_pins": {
            **FIXTURE_PINS,
            "width_fixture.py": sha_file(HERE / "width_fixture.py"),
        },
        "tag": args.tag,
        "shape": {
            "respondents": shape.respondents,
            "questions": args.questions,
            "include_weights": True,
            "missing_mod": shape.missing_mod,
            "sparse_mod": shape.sparse_mod,
            "repeated_mod": shape.repeated_mod,
            "skew_events": shape.skew_events,
            "width_note": (
                "600-slot geometry is implemented as routing-only extra slots with sparse base events; "
                "it is not a dense 600-event/respondent workload or real-width economics"
                if args.questions > 5 else
                "5 questions is not realistic 600-column width; use --questions 600 for a bounded geometry check, not economics"
            ),
            "event_count_expected": shape.event_count,
            "routing_count_expected": shape.routing_count,
            "weight_count_expected": shape.weight_count,
            "actual_family_counts": dict(receipt.family_counts),
        },
        "estate": {
            "root": str(estate_root),
            "exact_path": receipt.path,
            "manifest_sha256": receipt.manifest_sha256,
            "i02": {
                "logical": receipt.i02.logical, "physical": receipt.i02.physical,
                "release": receipt.i02.release, "source": receipt.i02.source,
                "replay": receipt.i02.replay, "universe": receipt.i02.universe,
                "schema": receipt.i02.schema,
            },
            "reconstructed_v1_release_ref": j(receipt.reconstructed_v1_release_ref),
            "family_counts": dict(receipt.family_counts),
            "retained_bytes": receipt.retained_bytes,
            "members_sha256": members,
        },
        "operations": [
            {
                "label": label,
                "query_ref": j(query.ref),
                "predicate_ref": j(predicate.ref),
                "targets": [j(x) for x in query.target_refs],
                "measure": query.requested_output_grain.get("measure_kind"),
                "semantic_role": {
                    "selected_weighted": "selected weighted estimand",
                    "f2_forward_raw": "F2 forward direction / raw",
                    "f2_reverse_raw": "F2 reverse direction / separate denominator",
                    "f4_three_raw": "true same-person k>=3 joint",
                    "repeated_mr_raw": "repeated/ranked occurrence, not first-value",
                }[label],
            }
            for label, query, predicate in ops
        ],
        "abort_limits": {
            "max_seconds": args.max_seconds,
            "max_process_tree_rss_bytes": args.max_rss_bytes,
            "max_scratch_bytes": args.max_scratch_bytes,
            "enforcement": "checkpoint abort before/after each operation; process-tree RSS and scratch sampled; no mid-call kill",
        },
        "distinct_operation_rule": "different target/predicate/direction/k3/measure/occurrence; no repeated ID-only clones",
    }
    (HERE / "fixture_contract.json").write_text(
        json.dumps(contract, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return contract


def load_contract() -> dict[str, Any]:
    path = HERE / "fixture_contract.json"
    if not path.exists():
        raise SystemExit("fixture contract missing; run --mode prepare first")
    contract = json.loads(path.read_text())
    # Tag is fixed by prepare; recover it from the contract, never re-default it.
    tag = contract.get("tag", DEFAULT_TAG)
    shape = ShapeSpec("cut2-measurement", contract["shape"]["respondents"],
                      include_weights=True, tag=tag)
    ctx = build_context(shape)
    width = build_width(ctx, contract["shape"]["questions"])
    bundle = width.query_bundle
    ops = selected_ops(bundle)
    expected = contract["operations"]
    actual = [
        {"label": label, "query_ref": j(q.ref), "predicate_ref": j(p.ref)}
        for label, q, p in ops
    ]
    if actual != [
        {"label": x["label"], "query_ref": x["query_ref"],
         "predicate_ref": x["predicate_ref"]} for x in expected
    ]:
        raise AssertionError("fixture operation identity drift")
    return contract, ctx, bundle, ops


def roots(estate: dict[str, Any]) -> ExternalI02Roots:
    return ExternalI02Roots(**estate["i02"])


def admission_open(estate: dict[str, Any], catalog: RuntimeObjectCatalog,
                   grant: Any, *, prepared: bool) -> tuple[Any, dict[str, Any]]:
    import rawlsing_next.pre553_source_direct_parquet_estate as estate_module
    calls = {"hash_calls": 0, "hash_bytes": 0}
    original = estate_module._hash

    def counted(path: Path) -> str:
        calls["hash_calls"] += 1
        if path.is_file():
            calls["hash_bytes"] += path.stat().st_size
        return original(path)

    estate_module._hash = counted
    started = time.monotonic()
    try:
        cls = PreparedSavedC11Admission if prepared else SavedC11Admission
        opened = cls.open(
            root=estate["root"], exact_path=estate["exact_path"],
            independently_held_manifest_sha256=estate["manifest_sha256"],
            independently_held_i02=roots(estate),
            release_ref=exact_ref(estate["reconstructed_v1_release_ref"]),
            runtime_catalog=catalog, current_authorizer=grant,
        )
    finally:
        estate_module._hash = original
    elapsed = time.monotonic() - started
    calls["seconds"] = elapsed
    return opened, calls


def fact_snapshot(result: Any) -> dict[str, Any]:
    facts = list(result.facts)
    fact_payload = canonical_json(facts)
    release_payload = canonical_json(list(result.release_refs))
    typed = [getattr(f, "typed_state", None) for f in facts]
    denoms = [getattr(f, "raw_denominator_support", None) for f in facts]
    weighted = [
        getattr(f, "weighted_denominator_support_if_authorized", None)
        for f in facts
    ]
    return {
        "fact_count": len(facts),
        "fact_refs": [j(f.ref) for f in facts],
        "fact_sha256": sha_bytes(fact_payload.encode()),
        "release_refs_sha256": sha_bytes(release_payload.encode()),
        "fact_payload_bytes": len(fact_payload.encode()),
        "release_payload_bytes": len(release_payload.encode()),
        "typed_states": typed,
        "raw_denominator_support": denoms,
        "weighted_denominator_support": weighted,
        "release_refs": j(result.release_refs),
    }


def _timer_patch(module: Any, name: str, bucket: dict[str, Any]):
    original = getattr(module, name)

    def wrapped(*args: Any, **kwargs: Any):
        started = time.monotonic()
        try:
            return original(*args, **kwargs)
        finally:
            bucket["seconds"] = bucket.get("seconds", 0.0) + (
                time.monotonic() - started)
            bucket["calls"] = bucket.get("calls", 0) + 1

    setattr(module, name, wrapped)
    return original


def measure(mode: str, *, negatives: bool = False) -> dict[str, Any]:
    contract, ctx, bundle, ops = load_contract()
    estate = contract["estate"]
    catalog = bundle.catalog
    grant = {"now": True}
    current = lambda _roots: grant["now"]
    prepared = mode in ("prepared", "batch")
    admission, h = admission_open(
        estate, catalog, current, prepared=prepared)
    if mode == "baseline":
        assert type(admission) is SavedC11Admission
    else:
        assert type(admission) is PreparedSavedC11Admission

    budget = contract["abort_limits"]
    started = time.monotonic()
    start_cpu = cpu_times()
    start_tree = process_tree_rss_bytes()
    start_rss = current_rss_bytes()
    scratch_before = directory_bytes(Path(estate["root"]))
    output_bytes = 0
    prepared_receipt = None
    rows: list[dict[str, Any]] = []
    evaluator_timer: dict[str, Any] = {}
    discovery_timer: dict[str, Any] = {}
    instrumentation = CourtInstrumentation()
    import rawlsing_next.pre553_carrier_execution as carrier
    import rawlsing_next.pre553_prepared_saved_i03 as prepared_mod
    original_eval = _timer_patch(carrier, "execute_empirical_query", evaluator_timer)
    original_eval_prepared = _timer_patch(
        prepared_mod, "execute_empirical_query", evaluator_timer)
    original_disc = _timer_patch(
        prepared_mod, "execute_exact_bounded_discovery", discovery_timer)
    try:
        with instrumentation.phase(forbid_c11_repository=True) as counters:
            if mode == "baseline":
                for label, query, predicate in ops:
                    _check_budget(started, budget, counters, estate)
                    op_start = time.monotonic()
                    result = admission.execute_i03(
                        query_ref=query.ref, predicate_ref=predicate.ref)
                    wall = time.monotonic() - op_start
                    serial_start = time.monotonic()
                    snap = fact_snapshot(result)
                    snap["serialize_seconds"] = time.monotonic() - serial_start
                    snap["label"] = label
                    snap["wall_seconds"] = wall
                    output_bytes += snap["fact_payload_bytes"] + snap[
                        "release_payload_bytes"]
                    rows.append(snap)
            elif mode == "prepared":
                with admission.prepared_i03() as session:
                    for label, query, predicate in ops:
                        _check_budget(started, budget, counters, estate)
                        op_start = time.monotonic()
                        result = session.execute_i03(
                            query_ref=query.ref, predicate_ref=predicate.ref)
                        wall = time.monotonic() - op_start
                        serial_start = time.monotonic()
                        snap = fact_snapshot(result)
                        snap["serialize_seconds"] = time.monotonic() - serial_start
                        snap["label"] = label
                        snap["wall_seconds"] = wall
                        output_bytes += snap["fact_payload_bytes"] + snap[
                            "release_payload_bytes"]
                        rows.append(snap)
                    prepared_receipt = session.receipt().as_dict()
            elif mode == "batch":
                units = tuple(
                    BatchUnitSpec("QUERY", query.ref, (admission.release_ref,))
                    for _, query, _ in ops
                )
                manifest = BatchManifest(units)
                predicate_map = {
                    query.ref.key: predicate.ref for _, query, predicate in ops
                }
                batch_start = time.monotonic()
                runner = execute_saved_batch(
                    admission, manifest=manifest,
                    predicate_ref_by_query=predicate_map,
                )
                batch_wall = time.monotonic() - batch_start
                by_unit = {r.unit_ref.key: r for r in runner.receipts}
                for label, query, _ in ops:
                    unit = next(
                        u for u in manifest.units if u.job_ref == query.ref)
                    receipt = by_unit[unit.unit_ref.key]
                    rows.append({
                        "label": label,
                        "unit_ref": j(unit.unit_ref),
                        "result_refs": [j(x) for x in receipt.result_refs],
                        "state": receipt.state,
                        "provenance_refs": [j(x) for x in receipt.provenance_refs],
                    })
                    output_bytes += len(
                        canonical_json([j(x) for x in receipt.result_refs]).encode())
                prepared_receipt = None
            else:
                raise ValueError(mode)

            if negatives:
                neg_before = counters.material()
                neg_eval_before = dict(evaluator_timer)
                neg_disc_before = dict(discovery_timer)
                negative_started = time.monotonic()
                grant["now"] = False
                try:
                    if mode == "batch":
                        execute_saved_batch(
                            admission, manifest=BatchManifest((
                                BatchUnitSpec("QUERY", ops[0][1].ref,
                                              (admission.release_ref,)),
                            )),
                            predicate_ref_by_query={
                                ops[0][1].ref.key: ops[0][2].ref},
                        )
                        refusal = "NO_REFUSAL"
                    else:
                        admission.execute_i03(
                            query_ref=ops[0][1].ref,
                            predicate_ref=ops[0][2].ref)
                        refusal = "NO_REFUSAL"
                except (DirectEstateError, SavedC11AdmissionError) as exc:
                    refusal = f"{type(exc).__name__}: {exc}"
                grant["now"] = True
                restored = admission.execute_i03(
                    query_ref=ops[0][1].ref, predicate_ref=ops[0][2].ref)
                neg_after = counters.material()
                negative = {
                    "revoked_refusal": refusal,
                    "restored_fact_sha256": fact_snapshot(restored)["fact_sha256"],
                    "wall_seconds": time.monotonic() - negative_started,
                    "index_builds": neg_after["session_builds"] - neg_before["session_builds"],
                    "index_build_seconds": neg_after["session_build_seconds"] - neg_before["session_build_seconds"],
                    "evaluator_calls": evaluator_timer.get("calls", 0) - neg_eval_before.get("calls", 0),
                    "evaluator_seconds": evaluator_timer.get("seconds", 0.0) - neg_eval_before.get("seconds", 0.0),
                    "discovery_calls": discovery_timer.get("calls", 0) - neg_disc_before.get("calls", 0),
                    "discovery_seconds": discovery_timer.get("seconds", 0.0) - neg_disc_before.get("seconds", 0.0),
                    "excluded_from_timed_operation_build_count": True,
                }
            else:
                negative = None
    finally:
        carrier.execute_empirical_query = original_eval
        prepared_mod.execute_empirical_query = original_eval_prepared
        prepared_mod.execute_exact_bounded_discovery = original_disc

    wall = time.monotonic() - started
    end_cpu = cpu_times()
    end_tree = process_tree_rss_bytes()
    end_rss = current_rss_bytes()
    scratch_after = directory_bytes(Path(estate["root"]))
    result = {
        "schema": SCHEMA,
        "mode": mode,
        "grade": "SOURCEFREE_TEST_ONLY_MECHANICS_NOT_PERFORMANCE",
        "fixture": contract["shape"],
        "estate_manifest_sha256": estate["manifest_sha256"],
        "operations": len(rows),
        "wall_seconds": wall,
        "cpu_user_seconds": end_cpu["user_seconds"] - start_cpu["user_seconds"],
        "cpu_system_seconds": end_cpu["system_seconds"] - start_cpu["system_seconds"],
        "process_tree_rss_start_bytes": start_tree,
        "process_tree_rss_end_bytes": end_tree,
        "process_tree_rss_peak_observed_bytes": max(start_tree, end_tree, end_cpu["maxrss_bytes"]),
        "self_rss_start_bytes": start_rss,
        "self_rss_end_bytes": end_rss,
        "self_maxrss_bytes": end_cpu["maxrss_bytes"],
        "estate_retained_bytes": directory_bytes(Path(estate["root"])),
        "scratch_before_bytes": scratch_before,
        "scratch_after_bytes": scratch_after,
        "scratch_peak_component_bytes": counters.material()["session_temp_max_bytes"],
        "output_bytes": output_bytes,
        "admission": h,
        "index_build_seconds": counters.material()["session_build_seconds"],
        "index_builds": counters.material()["session_builds"],
        "index_builds_measured_operations": (
            counters.material()["session_builds"]
            - ((negative or {}).get("index_builds", 0))
        ),
        "evaluator_seconds": evaluator_timer.get("seconds", 0.0),
        "evaluator_calls": evaluator_timer.get("calls", 0),
        "evaluator_seconds_measured_operations": (
            evaluator_timer.get("seconds", 0.0)
            - ((negative or {}).get("evaluator_seconds", 0.0))
        ),
        "evaluator_calls_measured_operations": (
            evaluator_timer.get("calls", 0)
            - ((negative or {}).get("evaluator_calls", 0))
        ),
        "discovery_seconds": discovery_timer.get("seconds", 0.0),
        "discovery_calls": discovery_timer.get("calls", 0),
        "row_group_reads": counters.material()["row_group_reads"],
        "row_group_rows": counters.material()["row_group_rows"],
        "row_group_compressed_bytes": counters.material()["row_group_compressed_bytes"],
        "event_object_materializations": counters.material()["event_object_materializations"],
        "family_object_materializations": counters.material()["family_object_materializations"],
        "session_builds": counters.material()["session_builds"],
        "prepared_receipt": prepared_receipt,
        "negative": negative,
        "rows": rows,
        "abort_limits": budget,
        "command": [sys.executable, str(Path(__file__).resolve()), "--mode", mode],
        "process": {
            "pid": os.getpid(), "ppid": os.getppid(),
            "python": sys.version, "platform": platform.platform(),
        },
    }
    return result


def _check_budget(started: float, budget: dict[str, Any], counters: Any,
                  estate: dict[str, Any]) -> None:
    if time.monotonic() - started > budget["max_seconds"]:
        raise SystemExit("ABORT_WALL_LIMIT")
    rss = process_tree_rss_bytes()
    if rss > budget["max_process_tree_rss_bytes"]:
        raise SystemExit(f"ABORT_RSS_LIMIT:{rss}")
    scratch = directory_bytes(Path(estate["root"]))
    if scratch > budget["max_scratch_bytes"]:
        raise SystemExit(f"ABORT_SCRATCH_LIMIT:{scratch}")


def write_result(result: dict[str, Any], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(plain(result), indent=2, sort_keys=True) + "\n")


def run_child(args: argparse.Namespace, mode: str, out: Path) -> dict[str, Any]:
    result = measure(mode, negatives=args.negatives)
    write_result(result, out)
    print(json.dumps({
        "mode": mode, "out": str(out), "operations": result["operations"],
        "wall_seconds": result["wall_seconds"],
        "index_builds": result["index_builds"],
        "rss_peak": result["process_tree_rss_peak_observed_bytes"],
    }, sort_keys=True))
    return result


def fresh(args: argparse.Namespace) -> dict[str, Any]:
    out = HERE / "evidence" / "fresh_batch.json"
    child = HERE / "evidence" / ".fresh_batch.child.json"
    cmd = [sys.executable, str(Path(__file__).resolve()),
           "--mode", "batch", "--root", args.root,
           "--out", str(child)]
    if args.negatives:
        cmd.append("--negatives")
    started = time.monotonic()
    completed = subprocess.run(cmd, cwd=str(REPO), text=True,
                               capture_output=True, timeout=args.max_seconds)
    elapsed = time.monotonic() - started
    child_result = json.loads(child.read_text()) if child.exists() else None
    parent = {
        "schema": SCHEMA,
        "mode": "fresh",
        "grade": "SOURCEFREE_TEST_ONLY_MECHANICS_NOT_PERFORMANCE",
        "fresh_process": True,
        "child_command": cmd,
        "child_exit": completed.returncode,
        "child_stdout": completed.stdout,
        "child_stderr": completed.stderr,
        "parent_wall_seconds": elapsed,
        "parent_rusage_children_maxrss_bytes": int(
            resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss) * (
            1024 if sys.platform != "darwin" else 1),
        "child": child_result,
    }
    write_result(parent, out)
    print(json.dumps({"mode": "fresh", "out": str(out),
                      "child_exit": completed.returncode}, sort_keys=True))
    return parent


def smoke(args: argparse.Namespace) -> dict[str, Any]:
    evidence = HERE / "evidence"
    evidence.mkdir(exist_ok=True)
    build_fixture(args)
    outputs: dict[str, Any] = {}
    for mode in ("baseline", "prepared", "batch"):
        out = evidence / f"{mode}.json"
        cmd = [sys.executable, str(Path(__file__).resolve()),
               "--mode", mode, "--root", args.root, "--out", str(out)]
        if args.negatives:
            cmd.append("--negatives")
        completed = subprocess.run(cmd, cwd=str(REPO), text=True,
                                   capture_output=True, timeout=args.max_seconds)
        if completed.returncode != 0:
            raise SystemExit(
                f"SMOKE_CHILD_FAILED:{mode}:{completed.returncode}:{completed.stderr}")
        outputs[mode] = json.loads(out.read_text())
    fresh_result = fresh(args)
    baseline_rows = {r["label"]: r for r in outputs["baseline"]["rows"]}
    prepared_rows = {r["label"]: r for r in outputs["prepared"]["rows"]}
    batch_rows = {r["label"]: r for r in outputs["batch"]["rows"]}
    parity = {
        "baseline_vs_prepared_fact_sha256": {
            label: baseline_rows[label]["fact_sha256"] ==
                   prepared_rows[label]["fact_sha256"]
            for label in baseline_rows
        },
        "baseline_vs_prepared_exact": all(
            baseline_rows[label]["fact_sha256"] ==
            prepared_rows[label]["fact_sha256"]
            for label in baseline_rows
        ),
        "batch_refs_vs_baseline_fact_refs": {
            label: batch_rows[label]["result_refs"] ==
                   baseline_rows[label]["fact_refs"]
            for label in baseline_rows
        },
        "baseline_labels": sorted(baseline_rows),
        "prepared_labels": sorted(prepared_rows),
        "batch_labels": sorted(batch_rows),
    }
    aggregate = {
        "schema": SCHEMA,
        "mode": "smoke",
        "grade": "SOURCEFREE_TEST_ONLY_MECHANICS_NOT_PERFORMANCE",
        "fixture": outputs["baseline"]["fixture"],
        "parity": parity,
        "modes": outputs,
        "fresh": fresh_result,
        "limit": "tiny 16-respondent/5-question mechanics only; not realistic width, native, 100k, or accepted economics",
    }
    write_result(aggregate, evidence / "smoke_evidence.json")
    print(json.dumps({"smoke": str(evidence / "smoke_evidence.json"),
                      "parity": parity}, sort_keys=True))
    return aggregate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True, choices=(
        "prepare", "baseline", "prepared", "batch", "fresh", "smoke"))
    parser.add_argument("--root", default=str(HERE / ".local-data"))
    parser.add_argument("--out", default=str(HERE / "evidence" / "result.json"))
    parser.add_argument("--respondents", type=int, default=DEFAULT_RESPONDENTS)
    parser.add_argument("--questions", type=int, default=5)
    parser.add_argument("--chunk-rows", type=int, default=16)
    parser.add_argument("--tag", default="CUT2-MEASURE")
    parser.add_argument("--max-seconds", type=float, default=DEFAULT_ABORT_SECONDS)
    parser.add_argument("--max-rss-bytes", type=int, default=DEFAULT_ABORT_RSS)
    parser.add_argument("--max-scratch-bytes", type=int, default=DEFAULT_ABORT_SCRATCH)
    parser.add_argument("--negatives", action="store_true")
    parser.add_argument("--child", action="store_true")
    args = parser.parse_args()
    if args.mode == "prepare":
        contract = build_fixture(args)
        print(json.dumps({"contract": str(HERE / "fixture_contract.json"),
                          "estate": contract["estate"]["exact_path"],
                          "events": contract["shape"]["event_count_expected"]},
                         sort_keys=True))
        return 0
    if args.mode == "fresh":
        fresh(args)
        return 0
    if args.mode == "smoke":
        smoke(args)
        return 0
    out = Path(args.out)
    run_child(args, args.mode, out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
