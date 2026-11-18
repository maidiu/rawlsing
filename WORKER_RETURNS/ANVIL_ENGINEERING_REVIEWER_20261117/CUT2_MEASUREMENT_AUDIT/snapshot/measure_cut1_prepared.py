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
import signal
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
    audit = dict(width.audit)
    for key, family in (
        ("total_events", "RespondentEvent"),
        ("total_routing", "RoutingEligibilityFact"),
        ("total_question_bindings", "QuestionVariableBinding"),
    ):
        if key in audit and int(audit[key]) != int(receipt.family_counts[family]):
            raise AssertionError(
                f"geometry audit vs manifest mismatch: {key}={audit[key]} "
                f"actual={receipt.family_counts[family]}")
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
                "600 native question slots with substantial populated response items: "
                "80% valid, 10% typed MISSING, 10% typed NOT_ASKED; actual events/routing "
                "are audited and this is still not native/original/real-width economics"
                if args.questions > 5 else
                "5 questions is not realistic 600-column width; use --questions 600 for a bounded geometry pilot, not economics"
            ),
            "event_count_expected": int(width.audit.get("total_events", shape.event_count)),
            "routing_count_expected": int(width.audit.get("total_routing", shape.routing_count)),
            "weight_count_expected": shape.weight_count,
            "geometry_audit": dict(width.audit),
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
    contract_path = Path(args.contract)
    if not contract_path.is_absolute():
        contract_path = HERE / contract_path
    contract_path.write_text(
        json.dumps(contract, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return contract


def load_contract(contract_path: str | Path | None = None) -> dict[str, Any]:
    path = Path(contract_path) if contract_path is not None else (
        HERE / "fixture_contract.json")
    if not path.is_absolute():
        path = HERE / path
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


def _collect_refs(value: Any, out: list[str]) -> None:
    from collections.abc import Mapping
    from rawlsing_next.pre553_empirical_objects import ExactRef

    if isinstance(value, ExactRef):
        out.append(value.key)
    elif isinstance(value, Mapping):
        for key in sorted(value):
            _collect_refs(value[key], out)
    elif isinstance(value, (list, tuple, set, frozenset)):
        for item in value:
            _collect_refs(item, out)


def fact_snapshot(result: Any) -> dict[str, Any]:
    from rawlsing_next.pre553_empirical_objects import canonical_json as cj

    facts = list(result.facts)
    semantic_payload = cj([f.semantic_projection() for f in facts])
    identity_payload = cj([f.as_dict() for f in facts])
    ref_only_payload = cj(facts)  # exact defect witness: canonicalize -> ref.as_dict()
    refs_payload = cj([f.ref.as_dict() for f in facts])
    replay_payload = cj([
        exact_ref(f.replay_ref, "fact.replay_ref").as_dict() for f in facts
    ])
    risk_refs: list[str] = []
    denom_refs: list[str] = []
    provenance_refs: list[str] = []
    topology_refs: list[str] = []
    for fact in facts:
        for ref in getattr(fact, "risk_set_member_refs", ()):
            risk_refs.append(exact_ref(ref, "fact.risk_set_member_refs").key)
        for ref in getattr(fact, "denominator_member_refs", ()):
            denom_refs.append(exact_ref(ref, "fact.denominator_member_refs").key)
        for ref in getattr(fact, "source_empirical_provenance_refs", ()):
            provenance_refs.append(exact_ref(ref, "fact.source_empirical_provenance_refs").key)
        _collect_refs(fact.semantic_projection().get("target_topology"), topology_refs)
    risk_payload = cj(sorted(set(risk_refs)))
    denom_payload = cj(sorted(set(denom_refs)))
    provenance_payload = cj(sorted(set(provenance_refs)))
    member_payload = cj(sorted(set(risk_refs) | set(denom_refs) | set(topology_refs)))
    return {
        "fact_count": len(facts),
        "fact_refs": [f.ref.as_dict() for f in facts],
        "replay_refs": [
            exact_ref(f.replay_ref, "fact.replay_ref").as_dict() for f in facts
        ],
        "semantic_sha256": sha_bytes(semantic_payload.encode()),
        "identity_sha256": sha_bytes(identity_payload.encode()),
        "ref_only_sha256": sha_bytes(ref_only_payload.encode()),
        "refs_sha256": sha_bytes(refs_payload.encode()),
        "replay_sha256": sha_bytes(replay_payload.encode()),
        "member_refs_sha256": sha_bytes(member_payload.encode()),
        "risk_member_refs_sha256": sha_bytes(risk_payload.encode()),
        "denominator_member_refs_sha256": sha_bytes(denom_payload.encode()),
        "provenance_refs_sha256": sha_bytes(provenance_payload.encode()),
        "risk_member_ref_count": len(set(risk_refs)),
        "denominator_member_ref_count": len(set(denom_refs)),
        "provenance_ref_count": len(set(provenance_refs)),
        "topology_ref_count": len(set(topology_refs)),
        "semantic_payload_bytes": len(semantic_payload.encode()),
        "identity_payload_bytes": len(identity_payload.encode()),
        "ref_only_payload_bytes": len(ref_only_payload.encode()),
        "refs_payload_bytes": len(refs_payload.encode()),
        "replay_payload_bytes": len(replay_payload.encode()),
        "member_payload_bytes": len(member_payload.encode()),
        "risk_member_payload_bytes": len(risk_payload.encode()),
        "denominator_member_payload_bytes": len(denom_payload.encode()),
        "provenance_payload_bytes": len(provenance_payload.encode()),
        "member_ref_count": len(set(risk_refs) | set(denom_refs) | set(topology_refs)),
        "typed_states": [getattr(f, "typed_state", None) for f in facts],
        "raw_denominator_support": [getattr(f, "raw_denominator_support", None) for f in facts],
        "weighted_denominator_support": [
            getattr(f, "weighted_denominator_support_if_authorized", None)
            for f in facts
        ],
        "release_refs": j(result.release_refs),
        "query_ref": j(result.query_ref),
        "source_scope_mode": result.source_scope_mode,
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


def measure(mode: str, *, contract_path: str | Path | None = None,
            negatives: bool = False) -> dict[str, Any]:
    contract, ctx, bundle, ops = load_contract(contract_path)
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
    observed: list[Any] = []
    rows: list[dict[str, Any]] = []
    evaluator_timer: dict[str, Any] = {}
    discovery_timer: dict[str, Any] = {}
    instrumentation = CourtInstrumentation()
    import rawlsing_next.pre553_carrier_execution as carrier
    import rawlsing_next.pre553_prepared_saved_i03 as prepared_mod
    from rawlsing_next.pre553_prepared_saved_i03 import PreparedI03Session
    original_prepared_exec = PreparedI03Session.execute_i03
    original_saved_exec = SavedC11Admission.execute_i03

    def observing(original):
        def wrapper(self, *args, **kwargs):
            result = original(self, *args, **kwargs)
            observed.append(result)
            return result
        return wrapper

    PreparedI03Session.execute_i03 = observing(original_prepared_exec)
    SavedC11Admission.execute_i03 = observing(original_saved_exec)
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
                    output_bytes += sum(snap[key] for key in (
                        "identity_payload_bytes", "refs_payload_bytes",
                        "replay_payload_bytes", "member_payload_bytes"))
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
                        output_bytes += sum(snap[key] for key in (
                            "identity_payload_bytes", "refs_payload_bytes",
                            "replay_payload_bytes", "member_payload_bytes"))
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
                    "restored_identity_sha256": fact_snapshot(restored)["identity_sha256"],
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
        PreparedI03Session.execute_i03 = original_prepared_exec
        SavedC11Admission.execute_i03 = original_saved_exec

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
        "binding_receipt_bytes": len(canonical_json(
            admission.binding_receipt().as_dict()).encode()),
        "prepared_receipt_bytes": (
            None if prepared_receipt is None else
            len(canonical_json(prepared_receipt).encode())
        ),
        "observer_results": len(observed),
        "observer_identity_sha256": [
            fact_snapshot(result)["identity_sha256"] for result in observed
        ],
        "wrapper_abi_bytes": len(canonical_json({
            "query_ref": rows[0]["query_ref"] if rows else None,
            "release_refs": rows[0]["release_refs"] if rows else [],
            "source_scope_mode": rows[0]["source_scope_mode"] if rows else None,
            "fact_refs": [row.get("fact_refs", []) for row in rows],
        }).encode()),
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




def _supervise(cmd: list[str], *, cap_seconds: float, scratch_root: Path,
               label: str, rss_limit: int, scratch_limit: int) -> dict[str, Any]:
    """External child supervision with 0.25 s process-tree/RSS/scratch sampling."""
    import court_instrumentation as ci

    started = time.monotonic()
    process = subprocess.Popen(
        cmd, cwd=str(REPO), text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, start_new_session=True,
    )
    samples: list[dict[str, Any]] = []
    aborted = None
    last_sample = None
    while process.poll() is None:
        time.sleep(0.25)
        elapsed = time.monotonic() - started
        rss = ci.process_tree_rss_bytes(process.pid)
        scratch = ci.directory_bytes(scratch_root)
        last_sample = {
            "elapsed_seconds": elapsed,
            "process_tree_rss_bytes": rss,
            "scratch_bytes": scratch,
            "pid": process.pid,
        }
        samples.append(last_sample)
        if elapsed > cap_seconds:
            aborted = f"WALL_LIMIT:{cap_seconds}"
            break
        if rss > rss_limit:
            aborted = f"RSS_LIMIT:{rss}>{rss_limit}"
            break
        if scratch > scratch_limit:
            aborted = f"SCRATCH_LIMIT:{scratch}>{scratch_limit}"
            break
    if aborted:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait(timeout=3)
    try:
        stdout, stderr = process.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        stdout, stderr = process.communicate(timeout=5)
    wall = time.monotonic() - started
    rss_peak = max((x["process_tree_rss_bytes"] for x in samples), default=0)
    scratch_peak = max((x["scratch_bytes"] for x in samples), default=0)
    return {
        "label": label,
        "command": cmd,
        "exit": process.returncode,
        "aborted": aborted,
        "wall_seconds": wall,
        "sample_count": len(samples),
        "process_tree_rss_peak_sampled_bytes": rss_peak,
        "scratch_peak_sampled_bytes": scratch_peak,
        "last_sample": last_sample,
        "stdout": stdout,
        "stderr": stderr,
    }


def _write_samples(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def pilot(args: argparse.Namespace) -> dict[str, Any]:
    """One producer build + fresh baseline + fresh prepared; one pair total."""
    outdir = HERE / "R2_PILOT"
    outdir.mkdir(parents=True, exist_ok=True)
    contract_rel = "R2_PILOT/fixture_contract_pilot.json"
    root = HERE / ".local-data-pilot"
    rss_limit = args.max_rss_bytes
    scratch_limit = args.max_scratch_bytes
    build_cap = 300.0
    query_cap = 180.0
    combined_cap = 12 * 60.0
    started = time.monotonic()
    common = [sys.executable, str(Path(__file__).resolve())]
    build_cmd = common + [
        "--mode", "prepare", "--respondents", "16", "--questions", "600",
        "--root", str(root), "--contract", contract_rel,
        "--chunk-rows", "512", "--max-seconds", str(query_cap),
        "--max-rss-bytes", str(rss_limit), "--max-scratch-bytes", str(scratch_limit),
    ]
    build = _supervise(build_cmd, cap_seconds=build_cap, scratch_root=root,
                       label="producer_build", rss_limit=rss_limit,
                       scratch_limit=scratch_limit)
    _write_samples(outdir / "samples_build.json", build)
    if build["exit"] != 0 or build["aborted"]:
        result = {
            "schema": "ANVIL_CUT2_R2_PILOT@1",
            "status": "EXACT_MEASUREMENT_FAILURE",
            "stage": "producer_build",
            "build": build,
            "combined_wall_seconds": time.monotonic() - started,
            "limitations": ["No query pair was run because producer build failed."],
        }
        _write_samples(outdir / "FIRST_PAIR_RESULT.json", result)
        return result
    baseline_cmd = common + [
        "--mode", "baseline", "--root", str(root),
        "--contract", contract_rel, "--out", str(outdir / "baseline.json"),
        "--max-seconds", str(query_cap),
        "--max-rss-bytes", str(rss_limit), "--max-scratch-bytes", str(scratch_limit),
    ]
    baseline = _supervise(baseline_cmd, cap_seconds=query_cap, scratch_root=root,
                          label="fresh_baseline", rss_limit=rss_limit,
                          scratch_limit=scratch_limit)
    _write_samples(outdir / "samples_baseline.json", baseline)
    if baseline["exit"] != 0 or baseline["aborted"]:
        result = {
            "schema": "ANVIL_CUT2_R2_PILOT@1",
            "status": "EXACT_MEASUREMENT_FAILURE",
            "stage": "fresh_baseline",
            "build": build, "baseline": baseline,
            "combined_wall_seconds": time.monotonic() - started,
            "limitations": ["Prepared mode not run because baseline failed."],
        }
        _write_samples(outdir / "FIRST_PAIR_RESULT.json", result)
        return result
    prepared_cmd = common + [
        "--mode", "prepared", "--root", str(root),
        "--contract", contract_rel, "--out", str(outdir / "prepared.json"),
        "--negatives", "--max-seconds", str(query_cap),
        "--max-rss-bytes", str(rss_limit), "--max-scratch-bytes", str(scratch_limit),
    ]
    prepared = _supervise(prepared_cmd, cap_seconds=query_cap, scratch_root=root,
                          label="fresh_prepared", rss_limit=rss_limit,
                          scratch_limit=scratch_limit)
    _write_samples(outdir / "samples_prepared.json", prepared)
    if prepared["exit"] != 0 or prepared["aborted"]:
        result = {
            "schema": "ANVIL_CUT2_R2_PILOT@1",
            "status": "EXACT_MEASUREMENT_FAILURE",
            "stage": "fresh_prepared",
            "build": build, "baseline": baseline, "prepared": prepared,
            "combined_wall_seconds": time.monotonic() - started,
            "limitations": ["Pair incomplete because prepared mode failed."],
        }
        _write_samples(outdir / "FIRST_PAIR_RESULT.json", result)
        return result

    baseline_json = json.loads((outdir / "baseline.json").read_text())
    prepared_json = json.loads((outdir / "prepared.json").read_text())
    contract = json.loads((HERE / contract_rel).read_text())
    b_rows = {r["label"]: r for r in baseline_json["rows"]}
    p_rows = {r["label"]: r for r in prepared_json["rows"]}
    labels = sorted(b_rows)
    parity_fields = ("identity_sha256", "semantic_sha256", "refs_sha256",
                     "member_refs_sha256", "replay_sha256")
    parity = {
        label: {
            field: b_rows[label][field] == p_rows[label][field]
            for field in parity_fields
        } for label in labels
    }
    exact = all(all(v.values()) for v in parity.values())
    negative = prepared_json.get("negative") or {}
    restored = negative.get("restored_identity_sha256")
    negative_label = "selected_weighted" if "selected_weighted" in b_rows else (
        labels[0] if labels else None)
    first_identity = b_rows[negative_label]["identity_sha256"] if negative_label else None
    result = {
        "schema": "ANVIL_CUT2_R2_PILOT@1",
        "status": "MEASURED_FIRST_BOUNDED_HIGHWIDTH_PAIR" if exact else "EXACT_MEASUREMENT_FAILURE",
        "geometry": contract.get("shape", {}),
        "geometry_audit": contract.get("shape", {}).get("geometry_audit"),
        "estate": contract.get("estate", {}),
        "build": build,
        "baseline": baseline_json,
        "prepared": prepared_json,
        "parity": {
            "labels": labels,
            "per_operation": parity,
            "exact_full_semantic_identity_refs_member_replay": exact,
        },
        "negative": {
            "revoked_refusal": negative.get("revoked_refusal"),
            "restored_identity_sha256": restored,
            "baseline_selected_identity_sha256": first_identity,
            "restored_matches_baseline": restored == first_identity,
            "negative_label": negative_label,
            "separate_index_builds": negative.get("index_builds"),
            "separate_evaluator_calls": negative.get("evaluator_calls"),
        },
        "supervision": {
            "build_cap_seconds": build_cap,
            "query_cap_seconds": query_cap,
            "combined_cap_seconds": combined_cap,
            "rss_limit_bytes": rss_limit,
            "scratch_limit_bytes": scratch_limit,
            "combined_wall_seconds": time.monotonic() - started,
            "build_exit": build["exit"],
            "baseline_exit": baseline["exit"],
            "prepared_exit": prepared["exit"],
            "build_aborted": build["aborted"],
            "baseline_aborted": baseline["aborted"],
            "prepared_aborted": prepared["aborted"],
            "sampling_interval_seconds": 0.25,
        },
        "limitations": [
            "One paired baseline-vs-prepared comparison only; no fresh Batch, 1/10/100 or repetitions.",
            "Queries target the accepted base A/B/C/MR roles; the 600 added slots load the writer/index but are not all queried.",
            "The 80/10/10 populated pattern is synthetic TEST_ONLY source geometry, not original eligible QUERY issuance.",
            "H/S/Q/O separation is existing-code instrumentation; Q includes fact construction/hash; O is export serialization and is not added to Q.",
            "Process-tree RSS is 0.25 s ps sampling plus child ru_maxrss; not a continuous sampler; OS file cache is uncontrolled.",
            "No native/original35/science/actor/100k/6GiB/economic acceptance.",
        ],
        "next_decision": "If exact parity and caps hold, qualify the measured H/S/Q/O/cost shape before any 1/10/100 or Batch-forward wiring; do not infer speedup from one pair.",
    }
    _write_samples(outdir / "FIRST_PAIR_RESULT.json", result)
    return result


def run_child(args: argparse.Namespace, mode: str, out: Path) -> dict[str, Any]:
    result = measure(mode, contract_path=args.contract, negatives=args.negatives)
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
           "--contract", args.contract,
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
               "--mode", mode, "--root", args.root,
               "--contract", args.contract, "--out", str(out)]
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
        "baseline_vs_prepared_identity_sha256": {
            label: baseline_rows[label]["identity_sha256"] ==
                   prepared_rows[label]["identity_sha256"]
            for label in baseline_rows
        },
        "baseline_vs_prepared_semantic_sha256": {
            label: baseline_rows[label]["semantic_sha256"] ==
                   prepared_rows[label]["semantic_sha256"]
            for label in baseline_rows
        },
        "baseline_vs_prepared_refs_sha256": {
            label: baseline_rows[label]["refs_sha256"] ==
                   prepared_rows[label]["refs_sha256"]
            for label in baseline_rows
        },
        "baseline_vs_prepared_member_refs_sha256": {
            label: baseline_rows[label]["member_refs_sha256"] ==
                   prepared_rows[label]["member_refs_sha256"]
            for label in baseline_rows
        },
        "baseline_vs_prepared_replay_sha256": {
            label: baseline_rows[label]["replay_sha256"] ==
                   prepared_rows[label]["replay_sha256"]
            for label in baseline_rows
        },
        "baseline_vs_prepared_exact_full": all(
            baseline_rows[label]["identity_sha256"] ==
            prepared_rows[label]["identity_sha256"]
            and baseline_rows[label]["semantic_sha256"] ==
            prepared_rows[label]["semantic_sha256"]
            and baseline_rows[label]["refs_sha256"] ==
            prepared_rows[label]["refs_sha256"]
            and baseline_rows[label]["member_refs_sha256"] ==
            prepared_rows[label]["member_refs_sha256"]
            and baseline_rows[label]["replay_sha256"] ==
            prepared_rows[label]["replay_sha256"]
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
        "prepare", "baseline", "prepared", "batch", "fresh", "smoke", "pilot"))
    parser.add_argument("--root", default=str(HERE / ".local-data"))
    parser.add_argument("--out", default=str(HERE / "evidence" / "result.json"))
    parser.add_argument("--contract", default="fixture_contract.json")
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
        contract_path = Path(args.contract)
        if not contract_path.is_absolute():
            contract_path = HERE / contract_path
        print(json.dumps({"contract": str(contract_path),
                          "estate": contract["estate"]["exact_path"],
                          "events": contract["shape"]["event_count_expected"]},
                         sort_keys=True))
        return 0
    if args.mode == "fresh":
        fresh(args)
        return 0
    if args.mode == "pilot":
        pilot(args)
        return 0
    if args.mode == "smoke":
        smoke(args)
        return 0
    out = Path(args.out)
    run_child(args, args.mode, out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
