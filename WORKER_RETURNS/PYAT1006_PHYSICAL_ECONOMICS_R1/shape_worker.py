"""One measured shape for PYAT #1006.

Run inside the task-local environment.  This module writes only under the
caller-provided workdir and never modifies accepted production/test files.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
import json
import os
from pathlib import Path
import shutil
import statistics
import sys
import threading
import time
from types import SimpleNamespace
from typing import Any

from rawlsing_next.pre553_batch_runner import BatchManifest, BatchUnitSpec
from rawlsing_next.pre553_issued_workload import (
    IssuedWorkloadRecord,
    NativeWorkload,
    capture_joined_checkpoint,
    execute_issued_workload,
    operation_jobs,
    resume_joined_workloads,
)
from rawlsing_next.pre553_native_workload_binding import TestOnlyDecisionResolver
from rawlsing_next.pre553_route_b_production import I03ExecutionRequest
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_saved_workload_integration import execute_saved_batch
from rawlsing_next.pre553_empirical_objects import (
    ExactRef,
    canonical_json,
    semantic_hash,
)
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_source_direct_parquet_estate import (
    VerifiedDirectEstate,
    write_direct_estate,
)

import rawlsing_next.pre553_source_direct_parquet_estate as estate_module
import rawlsing_next.pre553_direct_estate_i03 as direct_module

from fixture_1006 import ShapeSpec, build_context
from instrument_1006 import (
    TimerBank,
    directory_bytes,
    install_estate_instrumentation,
    install_object_materialization_counter,
    install_session_instrumentation,
    parquet_audit,
    replace_sections,
    restore_estate_instrumentation,
    restore_object_materialization_counter,
    restore_session_instrumentation,
    stats,
)
from query_1006 import build_query_bundle
from resources_1006 import disk, rss_self_bytes

HOST = "pyat1006-local-sourcefree"
PURPOSE = "TEST_ONLY_SOURCEFREE"


class StageMonitor:
    def __init__(self, root: Path, interval: float = 0.01):
        self.root = root
        self.interval = interval
        self.peak_stage = 0
        self.peak_proof = 0
        self.peak_root = 0
        self.samples = 0
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def _run(self) -> None:
        while not self._stop.is_set():
            try:
                for path in self.root.glob(".s2c-stage-*"):
                    if path.is_dir():
                        self.peak_stage = max(self.peak_stage, directory_bytes(path))
                        proof = path / ".i02-proof.sqlite"
                        if proof.exists():
                            self.peak_proof = max(self.peak_proof, proof.stat().st_size)
                self.peak_root = max(self.peak_root, directory_bytes(self.root))
                self.samples += 1
            except FileNotFoundError:
                pass
            time.sleep(self.interval)

    def __enter__(self) -> "StageMonitor":
        self._thread.start()
        return self

    def __exit__(self, *_args: Any) -> None:
        self._stop.set()
        self._thread.join(timeout=2)

    def material(self) -> dict[str, Any]:
        return {
            "stage_peak_bytes": self.peak_stage,
            "proof_sqlite_peak_bytes": self.peak_proof,
            "root_peak_bytes": self.peak_root,
            "samples": self.samples,
            "sampling_interval_seconds": self.interval,
        }


@dataclass(frozen=True)
class ProjectionStub:
    release_id: str
    expected_source_sha256: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": "PYAT1006_TEST_ONLY_PROJECTION@1",
            "release_id": self.release_id,
            "expected_source_sha256": self.expected_source_sha256,
            "source_scope": "SYNTHETIC_SOURCEFREE",
        }


def _jsonable(value: Any) -> Any:
    if value is None:
        return None
    return json.loads(canonical_json(value))


def _build_capsule(ctx: Any, bundle: Any, receipt: Any, root: Path) -> dict[str, Any]:
    return {
        "root": str(root),
        "exact_path": receipt.path,
        "manifest_sha256": receipt.manifest_sha256,
        "i02": asdict(receipt.i02),
        "release": receipt.reconstructed_v1_release_ref.as_dict(),
        "query": bundle.selected.as_dict(),
        "predicate": bundle.selected_predicate.as_dict(),
        "catalog": {
            "authorities": [a.as_dict() for a in bundle.catalog.authorities],
            "predicates": [p.as_dict() for p in bundle.catalog.predicates],
            "queries": [q.as_dict() for q in bundle.catalog.queries],
            "discovery_authorities": [
                d.as_dict() for d in bundle.catalog.discovery_authorities
            ],
        },
        "query_refs": {
            name: {
                "query": _jsonable(bundle.by_name(name)[0].ref),
                "predicate": _jsonable(bundle.by_name(name)[1].ref),
            }
            for name in (
                "selected", "f2_forward", "f2_reverse", "f4_three",
                "f4_four", "weighted", "repeated",
            )
            if (name == "selected" or name in {
                "f2_forward", "f2_reverse", "f4_three", "f4_four"
            } or (name == "weighted" and bundle.weighted is not None)
               or (name == "repeated" and bundle.repeated is not None))
        },
    }


def _fact_row(fact: Any) -> dict[str, Any]:
    projection = _jsonable(fact.semantic_projection())
    return {
        "ref": _jsonable(fact.ref),
        "typed_state": fact.typed_state,
        "raw_denominator_support": getattr(fact, "raw_denominator_support", None),
        "cell_count": len(projection.get("target_topology", {}).get(
            "complete_cell_semantic_projection", ()
        )) if isinstance(projection.get("target_topology"), dict) else None,
        "replay_ref": _jsonable(getattr(fact, "replay_ref", None)),
        "projection": projection,
    }


def _save_partial(path: Path, result: dict[str, Any]) -> None:
    path.write_text(json.dumps(result, indent=2, sort_keys=True, default=str) + "\n")


def _stop_after(args: Any, stage: str) -> bool:
    return getattr(args, "stop_after", None) == stage


def _timed_call(timers: TimerBank, name: str, fn: Any) -> Any:
    with timers.measure(name):
        return fn()


def _selected_repeats(
    admission: SavedC11Admission, query: Any, predicate: Any, count: int,
    timers: TimerBank,
) -> dict[str, Any]:
    values: list[float] = []
    fact_refs: list[list[dict[str, Any]]] = []
    for _ in range(count):
        start = time.monotonic()
        result = admission.execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
        values.append(time.monotonic() - start)
        fact_refs.append([_jsonable(f.ref) for f in result.facts])
    timers.add("selected_repeat_total", sum(values), len(values))
    return {
        "seconds": values,
        "stats": stats(values),
        "fact_refs_equal": len({json.dumps(v, sort_keys=True) for v in fact_refs}) == 1,
        "fact_refs": fact_refs[0] if fact_refs else [],
    }


def _batch_read(
    admission: SavedC11Admission, bundle: Any, release_ref: ExactRef,
    *, decision_ref: ExactRef, units: tuple[str, ...], timers: TimerBank,
) -> dict[str, Any]:
    unit_specs = []
    predicate_by_query = {}
    discovery_by_key = {}
    for name in units:
        if name == "i05":
            discovery_by_key[bundle.discovery_authority.ref.key] = (
                bundle.discovery_authority.ref
            )
            unit_specs.append(BatchUnitSpec(
                "DISCOVERY", bundle.discovery_authority.ref, (release_ref,),
                (decision_ref,),
            ))
            continue
        query, predicate = bundle.by_name(name)
        predicate_by_query[query.ref.key] = predicate.ref
        unit_specs.append(BatchUnitSpec(
            "QUERY", query.ref, (release_ref,), (predicate.ref, decision_ref),
        ))
    manifest = BatchManifest(tuple(unit_specs))
    start = time.monotonic()
    runner = execute_saved_batch(
        admission, manifest=manifest,
        predicate_ref_by_query=predicate_by_query,
        discovery_authority_ref_by_key=discovery_by_key,
    )
    elapsed = time.monotonic() - start
    timers.add("batch_total", elapsed)
    return {
        "seconds": elapsed,
        "units": units,
        "states": [receipt.state for receipt in runner.receipts],
        "receipt_refs": [
            {
                "unit_ref": receipt.unit_ref.as_dict(),
                "result_refs": [ref.as_dict() for ref in receipt.result_refs],
            }
            for receipt in runner.receipts
        ],
        "manifest_hash": runner.manifest.manifest_hash
        if hasattr(runner.manifest, "manifest_hash") else None,
    }


def _issued_workload(ctx: Any, bundle: Any) -> tuple[NativeWorkload, Any, Any]:
    projection = ProjectionStub(
        release_id=ctx.manifest.release_id,
        expected_source_sha256=ctx.source_sha256,
    )
    descriptor = {
        "source_edition": ctx.source_sha256,
        "native_item_ids": sorted(ctx.qrefs),
        "release_tag": ctx.manifest.release_id,
        "routing_and_risk": {"routing": "EXPLICIT", "risk_tag": "PYAT1006-R"},
        "carrier": {"source_format": "SYNTHETIC_SOURCEFREE", "source_artifact_id": ctx.manifest.source_artifact_id},
        "country_and_population": {"country": "US", "population": "ADULTS"},
        "weight_design_estimand": {
            "weight_basis": "W" if ctx.shape.include_weights else "NONE",
            "estimand": "TEST_ONLY",
        },
        "missing_and_occurrence_policy": {
            "missing": "EXPLICIT_TYPED_STATES",
            "occurrence": "SCALAR_AND_REPEATED",
        },
        "target_conditioner_roles": {
            "target": "C", "conditioner": "A", "measure_kind": "BOTH",
        },
    }
    descriptor_bytes = json.dumps(
        descriptor, sort_keys=True, separators=(",", ":")
    ).encode()
    decision_ref = ExactRef(
        "TEST_ONLY_DECISION", f"urn:test:pyat1006:{ctx.tag}", "9" * 64
    )
    requests = bundle.requests
    discoveries = (bundle.discovery_authority.ref,)
    workload = NativeWorkload(
        decision_ref=decision_ref,
        source_factory_ref=ExactRef(
            "SOURCE_FACTORY", f"urn:test:pyat1006:{ctx.tag}:source", "b" * 64
        ),
        descriptor=descriptor_bytes,
        projection=projection,
        catalog=bundle.catalog,
        requests=requests,
        discoveries=discoveries,
        original_u_root="c" * 64,
        expected_frontier_root="d" * 64,
    )
    record = IssuedWorkloadRecord(
        decision_ref=decision_ref,
        source_permission_ref=ExactRef(
            "TEST_ONLY_SOURCE_PERMISSION",
            f"urn:test:pyat1006:{ctx.tag}:source-permission", "e" * 64,
        ),
        scientific_permission_refs=(
            ExactRef(
                "TEST_ONLY_SCIENTIFIC_PERMISSION",
                f"urn:test:pyat1006:{ctx.tag}:science-permission", "f" * 64,
            ),
        ),
        host=HOST,
        purpose=PURPOSE,
        source_sha256=ctx.source_sha256,
        envelope_sha256=semantic_hash(workload.envelope()),
        original_u_root=workload.original_u_root,
        expected_frontier_root=workload.expected_frontier_root,
        expected_jobs=operation_jobs(requests, discoveries),
        currentness="CURRENT_GRANTED",
        scope="TEST_ONLY_SOURCEFREE",
    )
    return workload, record, TestOnlyDecisionResolver(record)


def _native_readers(
    ctx: Any, bundle: Any, admission: SavedC11Admission, timers: TimerBank,
) -> dict[str, Any]:
    workload, record, resolver = _issued_workload(ctx, bundle)
    result: dict[str, Any] = {}
    start = time.monotonic()
    full = execute_issued_workload(
        workload, resolver, saved_admission_factory=lambda: admission,
        source_factory=None, host=HOST, purpose=PURPOSE,
        allow_test_only=True,
    )
    result["normal_seconds"] = time.monotonic() - start
    result["normal_receipt_states"] = [r.state for r in full.receipts]
    result["normal_output_refs"] = [r.as_dict() for r in full.output_refs]
    binding = admission.binding_receipt()
    start = time.monotonic()
    partial = execute_issued_workload(
        workload, resolver, saved_admission_factory=lambda: admission,
        source_factory=None, host=HOST, purpose=PURPOSE,
        allow_test_only=True, max_units=1,
    )
    result["partial_seconds"] = time.monotonic() - start
    result["partial_receipt_states"] = [r.state for r in partial.receipts]
    completed_checkpoint = capture_joined_checkpoint(
        (full,), saved_binding=binding,
    )
    partial_checkpoint = capture_joined_checkpoint(
        (partial,), saved_binding=binding,
    )
    absent_checkpoint = capture_joined_checkpoint((), saved_binding=binding)
    for name, checkpoint in (
        ("completed", completed_checkpoint),
        ("partial", partial_checkpoint),
        ("absent", absent_checkpoint),
    ):
        start = time.monotonic()
        resumed = resume_joined_workloads(
            workloads=(SimpleNamespace(workload=workload, record=record),),
            resolver=resolver, saved_admission_factory=lambda: admission,
            source_factory=None, host=HOST, purpose=PURPOSE,
            checkpoint=checkpoint,
            expected_checkpoint_ref=checkpoint.checkpoint_hash,
            allow_test_only=True,
        )
        result[f"resume_{name}_seconds"] = time.monotonic() - start
        result[f"resume_{name}_output_refs"] = [
            ref.as_dict() for ref in resumed.output_refs
        ]
    timers.add("native_readers_total", result["normal_seconds"])
    return result


def run(args: argparse.Namespace) -> dict[str, Any]:
    workdir = Path(args.workdir).absolute()
    workdir.mkdir(parents=True, exist_ok=True)
    root = workdir / "estate"
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(mode=0o700)
    timers = TimerBank()
    started = time.monotonic()
    host = {
        "hostname": os.uname().nodename,
        "platform": sys.platform,
        "machine": os.uname().machine,
        "python": sys.version,
        "python_executable": sys.executable,
        "disk_at_start": disk(workdir),
    }
    out_path = Path(args.out)
    result: dict[str, Any] = {
        "schema": "PYAT1006_SHAPE_METRICS@1",
        "shape": {
            "name": args.name,
            "respondents": args.respondents,
            "include_weights": args.include_weights,
            "skew_events": args.skew_events,
            "chunk_rows": args.chunk_rows,
        },
        "host": host,
        "permission_grade": "SOURCEFREE_TEST_ONLY_NO_ORIGINAL35_RIGHTS",
        "status": "PARTIAL_RUNNING",
        "stage": "prepared",
    }
    ctx = build_context(ShapeSpec(
        name=args.name, respondents=args.respondents,
        include_weights=args.include_weights, skew_events=args.skew_events,
        tag=f"PYAT1006-{args.name}",
    ))
    bundle = build_query_bundle(ctx)
    result["declared_counts"] = dict(ctx.manifest.declared_record_counts_by_logical_family)
    result["respondents_vs_events"] = {
        "respondents": args.respondents,
        "events": ctx.shape.event_count,
        "events_minus_respondents": ctx.shape.event_count - args.respondents,
    }
    _save_partial(out_path, result)
    source = ctx.direct_sections()
    if args.time_sections:
        source = replace_sections(source, timers)
    estate_state = install_estate_instrumentation(estate_module, timers)
    object_state = install_object_materialization_counter(direct_module)
    session_state = install_session_instrumentation(direct_module, timers)
    monitor = StageMonitor(root)
    monitor.__enter__()
    try:
        start = time.monotonic()
        receipt = write_direct_estate(
            source, ctx.universe.ref, root, chunk_rows=args.chunk_rows,
        )
        result["write_seconds"] = time.monotonic() - start
        result["stage"] = "write_complete"
        result["receipt"] = {
            "path": receipt.path,
            "manifest_sha256": receipt.manifest_sha256,
            "i02": asdict(receipt.i02),
            "reconstructed_v1_release_ref": receipt.reconstructed_v1_release_ref.as_dict(),
            "family_counts": dict(receipt.family_counts),
            "retained_bytes": receipt.retained_bytes,
        }
        result["writer_instrumentation"] = {
            "row_calls": dict(estate_state["row_calls"]),
            "row_body_bytes": dict(estate_state["row_body_bytes"]),
            "row_seconds": estate_state["row_seconds"],
            "sink_add_calls": dict(estate_state["sink_add_calls"]),
            "sink_flush_calls": dict(estate_state["sink_flush_calls"]),
            "hash_calls": estate_state["hash_calls"],
            "hash_bytes": estate_state["hash_bytes"],
            "object_materializations": object_state["count"],
        }
        result["parquet_audit"] = parquet_audit(Path(receipt.path))
        result["capsule"] = _build_capsule(ctx, bundle, receipt, root)
        result["stage_monitor"] = monitor.material()
        result["disk_after_write"] = disk(workdir)
        result["timers"] = timers.material()
        _save_partial(out_path, result)
        if _stop_after(args, "write"):
            result["status"] = "MEASURED_PARTIAL_STOPPED_AFTER_WRITE"
            _save_partial(out_path, result)
            return result
        admission_start = time.monotonic()
        admission = SavedC11Admission.open(
            root=root, exact_path=receipt.path,
            independently_held_manifest_sha256=receipt.manifest_sha256,
            independently_held_i02=receipt.i02,
            release_ref=receipt.reconstructed_v1_release_ref,
            runtime_catalog=bundle.catalog,
            current_authorizer=lambda _roots: True,
        )
        result["cold_admission_seconds"] = time.monotonic() - admission_start
        result["cold_admission_hash_calls"] = estate_state["hash_calls"]
        result["cold_admission_object_materializations"] = object_state["count"]
        result["stage"] = "admission_complete"
        _save_partial(out_path, result)
        if _stop_after(args, "admission"):
            result["status"] = "MEASURED_PARTIAL_STOPPED_AFTER_ADMISSION"
            _save_partial(out_path, result)
            return result
        result["queries"] = {}
        for name in args.query_names:
            query, predicate = bundle.by_name(name)
            start = time.monotonic()
            observed = admission.execute_i03(
                query_ref=query.ref, predicate_ref=predicate.ref,
            )
            elapsed = time.monotonic() - start
            result["queries"][name] = {
                "seconds": elapsed,
                "facts": [_fact_row(f) for f in observed.facts],
                "release_refs": [_jsonable(r) for r in observed.release_refs],
                "query_ref": _jsonable(observed.query_ref),
            }
            result["stage"] = f"query:{name}"
            result["timers"] = timers.material()
            _save_partial(out_path, result)
        if _stop_after(args, "queries"):
            result["status"] = "MEASURED_PARTIAL_STOPPED_AFTER_QUERIES"
            _save_partial(out_path, result)
            return result
        result["selected_repeat"] = _selected_repeats(
            admission, bundle.selected, bundle.selected_predicate,
            args.repeat, timers,
        )
        result["stage"] = "selected_repeat_complete"
        result["timers"] = timers.material()
        _save_partial(out_path, result)
        if _stop_after(args, "repeat"):
            result["status"] = "MEASURED_PARTIAL_STOPPED_AFTER_REPEAT"
            _save_partial(out_path, result)
            return result
        start = time.monotonic()
        discovery = admission.execute_i05(
            discovery_authority_ref=bundle.discovery_authority.ref,
        )
        result["i05"] = {
            "seconds": time.monotonic() - start,
            "candidate_count": discovery.candidate_count,
            "covered_candidate_count": discovery.covered_candidate_count,
            "fact_refs": [_jsonable(f.ref) for f in discovery.empirical_facts],
            "receipt_refs": [_jsonable(r.ref) for r in discovery.receipts],
            "replay_ref": _jsonable(discovery.replay_ref),
        }
        result["stage"] = "i05_complete"
        result["timers"] = timers.material()
        _save_partial(out_path, result)
        if _stop_after(args, "i05"):
            result["status"] = "MEASURED_PARTIAL_STOPPED_AFTER_I05"
            _save_partial(out_path, result)
            return result
        if args.batch_units:
            result["batch"] = _batch_read(
                admission, bundle, receipt.reconstructed_v1_release_ref,
                decision_ref=ExactRef(
                    "TEST_ONLY_DECISION",
                    f"urn:test:pyat1006:{ctx.tag}:batch", "8" * 64,
                ),
                units=tuple(args.batch_units), timers=timers,
            )
            result["stage"] = "batch_complete"
            result["timers"] = timers.material()
            _save_partial(out_path, result)
        if _stop_after(args, "batch"):
            result["status"] = "MEASURED_PARTIAL_STOPPED_AFTER_BATCH"
            _save_partial(out_path, result)
            return result
        if args.native_readers:
            result["native_readers"] = _native_readers(
                ctx, bundle, admission, timers,
            )
            result["stage"] = "native_readers_complete"
            result["timers"] = timers.material()
            _save_partial(out_path, result)
        result["session_instrumentation"] = {
            "enter_calls": session_state["enter_calls"],
            "build_calls": session_state["build_calls"],
        }
        result["object_materializations_total"] = object_state["count"]
        result["retained_bytes"] = directory_bytes(root)
        result["disk_after_readers"] = disk(workdir)
        result["timers"] = timers.material()
        result["rss_self_peak_bytes"] = rss_self_bytes()
        result["seconds_total"] = time.monotonic() - started
        result["status"] = "MEASURED"
        result["stage"] = "complete"
        result["capsule"] = _build_capsule(ctx, bundle, receipt, root)
        return result
    except BaseException as exc:
        result["status"] = "FAILED"
        result["error"] = f"{type(exc).__name__}: {exc}"
        result["timers"] = timers.material()
        result["stage_monitor"] = monitor.material()
        result["disk_after_failure"] = disk(workdir)
        result["rss_self_peak_bytes"] = rss_self_bytes()
        result["seconds_total"] = time.monotonic() - started
        _save_partial(out_path, result)
        return result
    finally:
        monitor.__exit__(None, None, None)
        restore_session_instrumentation(direct_module, session_state)
        restore_object_materialization_counter(direct_module, object_state)
        restore_estate_instrumentation(estate_module, estate_state)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--respondents", type=int, required=True)
    parser.add_argument("--workdir", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--chunk-rows", type=int, default=512)
    parser.add_argument("--include-weights", action="store_true")
    parser.add_argument("--skew-events", type=int, default=0)
    parser.add_argument("--repeat", type=int, default=10)
    parser.add_argument("--query-names", default="selected,f2_forward,f2_reverse,f4_three,f4_four")
    parser.add_argument("--batch-units", default="selected,f2_reverse,f4_three,i05")
    parser.add_argument("--no-native-readers", action="store_true")
    parser.add_argument("--time-sections", action="store_true")
    parser.add_argument(
        "--stop-after",
        choices=("write", "admission", "queries", "repeat", "i05", "batch", "native"),
        default=None,
    )
    args = parser.parse_args(argv)
    args.query_names = [
        value for value in args.query_names.split(",") if value
    ]
    args.batch_units = [
        value for value in args.batch_units.split(",") if value
    ]
    args.native_readers = not args.no_native_readers
    out = Path(args.out)
    result = run(args)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "shape": result["shape"],
        "write_seconds": result["write_seconds"],
        "cold_admission_seconds": result["cold_admission_seconds"],
        "selected_repeat": result["selected_repeat"]["stats"],
        "retained_bytes": result["retained_bytes"],
    }, indent=2, sort_keys=True))
    return 0 if result["status"] == "MEASURED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
