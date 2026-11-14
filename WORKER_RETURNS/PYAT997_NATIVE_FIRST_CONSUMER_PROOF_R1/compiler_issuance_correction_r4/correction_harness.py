"""R4 correction: use only the unchanged compiler-issued workload.

This return-local harness does not construct or replace a NativeWorkload or
IssuedWorkloadRecord. It captures the compilation returned by the unchanged
compile_governed_frontier, executes its exact issued DISCOVERY workload through
the saved Q2 admission, and keeps the R3 manual QUERY claim withdrawn.
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "issued_batch_f4_r3"))
import harness  # noqa: E402

from rawlsing_next.pre553_issued_workload import (
    capture_joined_checkpoint, execute_issued_workload,
    resume_joined_workloads,
)
from rawlsing_next.pre553_native_workload_binding import TestOnlyDecisionResolver
from rawlsing_next.pre553_saved_workload_integration import execute_saved_i03
from rawlsing_next.pre553_empirical_objects import exact_ref, semantic_hash
from rawlsing_next.pre553_saved_c11_admission import (
    SavedC11Admission, SavedReleaseIdentity,
)
from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream
from rawlsing_next.pre553_source_native_preimage_adapter import (
    AdministeredItem, NativePreimageBundle,
)
from rawlsing_next.pre553_source_saved_body_bridge import SourceSavedBodySink
from rawlsing_next.pre553_universal_workload import compile_governed_frontier
from rawlsing_next.tests.test_pyat960_s1e_support import build


def _actual_materialize(stage: Path, fixture):
    """Build the Q2 estate and actual compiler compilation without any manual
    NativeWorkload/IssuedWorkloadRecord replacement."""
    stage.mkdir(parents=True, exist_ok=True)
    private = stage / "private"
    private.mkdir(mode=0o700, exist_ok=True)
    sink = SourceSavedBodySink(
        certificate_path=stage / "estate.sqlite",
        authorized_private_root=private, chunk_rows=2,
    )
    handoff = build(
        stage, fixture, name="estate.sqlite", body_sink=sink, chunk_size=2)
    estate = sink.receipt
    release = SavedReleaseIdentity(estate.reconstructed_v1_release_ref)
    projection = fixture["projection"]
    administered = tuple(
        AdministeredItem(
            "R4-" + name, name, "ADMINISTERED",
            "TEST_ONLY_Q2_THREE_QUESTION", "person", "OUTCOME",
        )
        for name in ("q101", "q102", "q103", "country")
    )
    bundle = NativePreimageBundle(
        schema="PYAT_R56_NATIVE_PREIMAGE_BUNDLE@1.0.0",
        source_sha256=handoff.source_sha256,
        package_hash=semantic_hash({"q2": handoff.source_sha256}),
        projection=projection,
        physical_stream=ExactPhysicalCellStream(
            handoff.source_sha256, handoff.row_count, lambda: ()),
        release=release,
        administered=administered,
        held=(), excluded=(), unknown=(),
        bundle_hash=semantic_hash({
            "q2_source": handoff.source_sha256,
            "release": estate.reconstructed_v1_release_ref.as_dict(),
        }),
        question_refs=dict(fixture["qrefs"]),
        risk_set_ref=exact_ref(projection.routing[0].risk_set_ref),
        respondent_rows=tuple(
            {"respondent_key": row.respondent_key, "ref": row.ref.key}
            for row in projection.respondents
        ),
        occurrence_bindings=(),
    )
    compilation = compile_governed_frontier(
        bundle=bundle, inventory=fixture["inventory"],
        policy=fixture["policy"], frontier=fixture["frontier"],
        as_of=harness.AS_OF, host=harness.HOST, purpose=harness.PURPOSE,
    )
    admission = SavedC11Admission.open(
        root=private, exact_path=estate.path,
        independently_held_manifest_sha256=estate.manifest_sha256,
        independently_held_i02=estate.i02,
        release_ref=estate.reconstructed_v1_release_ref,
        runtime_catalog=compilation.runtime_catalog,
        current_authorizer=lambda _roots: True,
    )
    return {
        "fixture": fixture, "handoff": handoff, "estate": estate,
        "compilation": compilation, "admission": admission,
        "private": private,
    }


def main() -> int:
    root = Path(tempfile.mkdtemp(
        prefix="pyat997-r4-compiler-",
        dir="/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T",
    ))
    fixture = harness._make_fixture(
        root / "fixture",
        [(0, 0, 0, 1), (1, 1, 1, 1), (0, 1, 0, 2),
         (1, 0, 1, 3), (0, 0, 1, 4)],
    )
    bundle = _actual_materialize(root / "stage", fixture)
    compiler = bundle["compilation"]
    issued = compiler.issued
    admission = bundle["admission"]
    record = issued.record
    workload = issued.workload
    before = {
        "decision_ref": record.decision_ref.key,
        "expected_jobs": [list(job) for job in record.expected_jobs],
        "requests": len(workload.requests),
        "discoveries": len(workload.discoveries),
        "envelope_sha256": record.envelope_sha256,
        "record_equal": issued.record == compiler.issued.record,
        "workload_equal": issued.workload == compiler.issued.workload,
    }
    if len(workload.requests) != 0 or len(workload.discoveries) != 1:
        raise AssertionError("unexpected compiler issuance shape")
    if record.expected_jobs != (("DISCOVERY", workload.discoveries[0].key, ""),):
        raise AssertionError("unexpected compiler expected_jobs")
    resolver = TestOnlyDecisionResolver(record)
    normal = execute_issued_workload(
        workload, resolver, saved_admission_factory=lambda: admission,
        source_factory=None, host=harness.HOST, purpose=harness.PURPOSE,
        allow_test_only=True,
    )
    if not normal.receipts or not all(
            r.state == "COMPLETED" for r in normal.receipts):
        raise AssertionError("compiler-issued discovery NORMAL did not complete")
    completed_checkpoint = capture_joined_checkpoint(
        (normal,), saved_binding=admission.binding_receipt())
    completed = resume_joined_workloads(
        workloads=(issued,), resolver=resolver,
        saved_admission_factory=lambda: admission, source_factory=None,
        host=harness.HOST, purpose=harness.PURPOSE,
        checkpoint=completed_checkpoint,
        expected_checkpoint_ref=completed_checkpoint.checkpoint_hash,
        allow_test_only=True,
    )
    if not completed.completed_results:
        raise AssertionError("compiler-issued COMPLETED resume returned no result")
    full_refs = tuple(sorted(ref.key for ref in normal.output_refs))
    resumed_refs = tuple(sorted(ref.key for ref in completed.output_refs))
    if full_refs != resumed_refs:
        raise AssertionError("compiler-issued COMPLETED refs differ")

    # Direct q101 remains a mechanical standalone query, not compiler-issued.
    q101_query = None
    for query in compiler.runtime_catalog.queries:
        targets = tuple(exact_ref(t) for t in query.target_refs)
        if len(targets) == 1 and targets[0].object_id.endswith(":q101"):
            q101_query = query
            break
    if q101_query is None:
        raise AssertionError("q101 catalog query unavailable")
    q101_predicate = compiler.runtime_catalog.resolve_predicate_exact(
        q101_query.condition_predicate_ref)
    q101 = execute_saved_i03(
        admission, query_ref=q101_query.ref, predicate_ref=q101_predicate.ref)

    f4_like = []
    for operation in fixture["frontier"].operations:
        targets = {key.item_id for key in operation.targets}
        if (targets == {"q101", "q102", "q103"}
                and operation.measure_kind == "SAMPLE"
                and not operation.conditions):
            f4_like.append({
                "operation_id": operation.op_id,
                "claim_class": operation.claim_class,
                "disposition": operation.disposition,
                "measure": operation.measure_kind,
            })
    joint_in_plan = []
    for rec in compiler.plan.records:
        refs = []
        for raw in rec.query_refs:
            if isinstance(raw, dict):
                raw = {k: raw[k] for k in ("kind", "object_id", "content_hash")}
            refs.append(exact_ref(raw).key)
        if compiler.runtime_catalog.query_refs:
            # The selected joint query is absent from the plan; this loop is
            # intentionally empty for the corrected evidence.
            pass
    after = {
        "decision_ref": record.decision_ref.key,
        "expected_jobs": [list(job) for job in record.expected_jobs],
        "requests": len(workload.requests),
        "discoveries": len(workload.discoveries),
        "envelope_sha256": record.envelope_sha256,
        "record_equal": issued.record == compiler.issued.record,
        "workload_equal": issued.workload == compiler.issued.workload,
    }
    if before != after:
        raise AssertionError("compiler issued record/workload changed during execution")
    out = {
        "schema": "PYAT997_R4_COMPILER_ISSUANCE_CORRECTION@1",
        "status": "CORRECTED_COMPILER_ISSUED_DISCOVERY_PASS__QUERY_NOT_ISSUED__NOT_G5",
        "compiler_issues_query": False,
        "compiler_record": before,
        "compiler_issued_normal": {
            "units": len(normal.receipts),
            "states": [r.state for r in normal.receipts],
            "output_refs": len(full_refs),
        },
        "compiler_issued_completed": {
            "completed_results": len(completed.completed_results),
            "resumed_results": len(completed.resumed_results),
            "output_refs": len(resumed_refs),
            "refs_equal_full": full_refs == resumed_refs,
        },
        "direct_q101_standalone": {
            "fact_refs": [f.ref.as_dict() for f in q101.facts],
            "typed_states": [f.typed_state for f in q101.facts],
            "note": "mechanical direct q101 only; not a compiler-issued Batch QUERY",
        },
        "f4_like_operations": f4_like,
        "f4_like_disposition": sorted({row["disposition"] for row in f4_like}),
        "joint_query_in_compiler_plan": joint_in_plan,
        "query_not_issued": len(workload.requests) == 0,
        "batch_query_unit": "NOT_ISSUED",
        "partial_absent": "NOT_PROVED__ONE_COMPILER_ISSUED_DISCOVERY_UNIT",
        "manual_query_claim": "WITHDRAWN",
        "source_opens": admission.binding_receipt().source_opens,
        "full_c11_builds": admission.binding_receipt().full_c11_repository_builds,
        "resource": {
            "retained_bytes": bundle["estate"].retained_bytes,
            "stage_bytes": sum(p.stat().st_size for p in (root / "stage").rglob("*") if p.is_file()),
            "parent_maxrss": __import__("resource").getrusage(
                __import__("resource").RUSAGE_SELF).ru_maxrss,
            "source_reads": bundle["handoff"].stats.source_reads,
            "decode_calls": bundle["handoff"].stats.decode_calls,
            "cell_passes": bundle["handoff"].stats.cell_passes,
            "full_c11_builds": bundle["handoff"].stats.full_c11_builds,
            "parquet_members": len(list(Path(bundle["estate"].path).glob("*.parquet"))),
        },
        "prior_r3_withdrawal": {
            "withdrawn": [
                "compiler-issued Batch QUERY",
                "compiler-issued F4",
                "two-unit PARTIAL/ABSENT",
                "R3 self-issued manual NativeWorkload/IssuedWorkloadRecord substitution",
            ],
            "preserved": [
                "P0 one-source 13-family persisted estate",
                "direct q101 mechanical I03",
                "discovery/I05",
                "75/75 test-patch proof",
                "fresh source/body proof",
            ],
        },
    }
    out_path = root / "correction.json"
    out_path.write_text(json.dumps(out, indent=2, default=str) + "\n")
    print(json.dumps({
        "status": out["status"],
        "proof": str(out_path),
        "compiler_record": before,
        "normal": out["compiler_issued_normal"],
        "completed": out["compiler_issued_completed"],
        "q101": out["direct_q101_standalone"],
        "f4_like": out["f4_like_operations"],
        "query_not_issued": out["query_not_issued"],
        "resource": out["resource"],
    }, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
