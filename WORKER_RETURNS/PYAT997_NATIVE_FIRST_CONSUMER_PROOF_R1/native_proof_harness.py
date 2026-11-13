"""PYAT #997 native P0/P1 proof harness.

Read-only use of the frozen candidate APIs and test-only fixture builders.
This file is authored only under WORKER_RETURNS/...; it does not modify product
code, accepted tests, S2-C/D, or any source/authority issuer.

The harness deliberately distinguishes:

* actual frozen repository APIs / S2-C persisted estate / S2-D saved readers;
* the repository test helpers used only to construct TEST_ONLY SAV bytes;
* known test-harness limitations (regenerated SAV timestamps and a helper that
  selects the first negative I03 query instead of a supported one).

It is native evidence, not an independent G5 and not an accepted #997 bridge.
"""
from __future__ import annotations

import json
import os
from collections.abc import Mapping
from dataclasses import replace
from pathlib import Path
import resource
import subprocess
import sys
import time

from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner, BatchManifest, BatchUnitSpec,
)
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_issued_workload import execute_issued_workload
from rawlsing_next.pre553_native_workload_binding import TestOnlyDecisionResolver
from rawlsing_next.pre553_saved_c11_admission import (
    SavedC11Admission, SavedReleaseIdentity,
)
from rawlsing_next.pre553_saved_workload_integration import (
    execute_saved_batch, execute_saved_i03, execute_saved_i05,
)
from rawlsing_next.pre553_source_postconsumer_receipts import (
    SourceReceiptJoinError, join_saved_source_operation_fates,
)
from rawlsing_next.pre553_source_saved_body_bridge import SourceSavedBodySink
from rawlsing_next.tests.test_pyat960_s1e_native_fact import (
    _NATIVE_HOST, _NATIVE_PURPOSE, _compile_native, _native_fixture,
)
from rawlsing_next.tests.test_pyat960_s1e_support import build
from rawlsing_next.tests.test_pyat_r3_s1c_source_operation_fates import _freeze_packet
from rawlsing_next.tests.test_universal_grammar import _frontier


def _jsonable(value):
    if isinstance(value, Mapping):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if hasattr(value, "as_dict"):
        return _jsonable(value.as_dict())
    return repr(value)


def _fix_fixture(fixture):
    # Keep the scientific inventory identity stable across independently
    # written fixture roots; source_fixture's inventory_id uses id(root).
    inventory = replace(
        fixture["inventory"], inventory_id="PYAT997-S1E-EXACT-RESTORE")
    frontier = _frontier(inventory, fixture["policy"])
    fixture = dict(fixture)
    fixture.update(
        inventory=inventory, frontier=frontier,
        census=_freeze_packet(frontier),
    )
    return fixture


def _materialize(stage: Path, fixture) -> dict:
    stage.mkdir(parents=True, exist_ok=True)
    private = stage / "private"
    private.mkdir(mode=0o700, exist_ok=True)
    sink = SourceSavedBodySink(
        certificate_path=stage / "source-i02.sqlite",
        authorized_private_root=private,
        chunk_rows=2,
    )
    handoff = build(
        stage, fixture, name="source-i02.sqlite",
        body_sink=sink, chunk_size=2,
    )
    estate = sink.receipt
    release_identity = SavedReleaseIdentity(estate.reconstructed_v1_release_ref)
    compilation = _compile_native(
        fixture, handoff, fixture["projection"], release_identity)
    issued = compilation.issued
    admission = SavedC11Admission.open(
        root=private,
        exact_path=estate.path,
        independently_held_manifest_sha256=estate.manifest_sha256,
        independently_held_i02=estate.i02,
        release_ref=estate.reconstructed_v1_release_ref,
        runtime_catalog=issued.workload.catalog,
        current_authorizer=lambda _roots: True,
    )
    resolver = TestOnlyDecisionResolver(issued.record)
    return {
        "fixture": fixture, "handoff": handoff, "estate": estate,
        "sink": sink, "compilation": compilation, "admission": admission,
        "resolver": resolver, "stage": stage,
    }


def _supported_i03(admission, compilation):
    """Select an actual supported saved I03 result, not the first negative.

    The repository test helper _native_i03 returns the first fact from the
    first supported lowering record, which may be a typed negative country
    query. This harness scans the exact compiled query refs and records both
    the selected positive and the negative queries observed.
    """
    negatives = []
    positives = []
    for record in compilation.plan.records:
        if record.status != "SUPPORTED":
            continue
        for raw in record.query_refs:
            if isinstance(raw, Mapping):
                raw = {k: raw[k] for k in ("kind", "object_id", "content_hash")}
            query_ref = exact_ref(raw, "query")
            query = compilation.issued.workload.catalog.resolve_query_exact(query_ref)
            predicate_ref = exact_ref(query.condition_predicate_ref, "predicate")
            result = execute_saved_i03(
                admission, query_ref=query_ref, predicate_ref=predicate_ref)
            for fact in result.facts:
                row = {
                    "operation_id": record.operation_id,
                    "query_ref": query_ref.as_dict(),
                    "fact_ref": fact.ref.as_dict(),
                    "typed_state": fact.typed_state,
                    "raw_denominator_support": fact.raw_denominator_support,
                    "raw_numerator_support": getattr(
                        fact, "raw_numerator_support", None),
                    "target_topology": _jsonable(fact.target_topology),
                }
                if fact.typed_state == "SUPPORTED":
                    positives.append(row)
                else:
                    negatives.append(row)
    if not positives:
        raise AssertionError("no actual supported saved I03 fact")
    return positives[0], positives, negatives


def _run_once(bundle) -> dict:
    handoff = bundle["handoff"]
    estate = bundle["estate"]
    compilation = bundle["compilation"]
    admission = bundle["admission"]
    resolver = bundle["resolver"]
    sink = bundle["sink"]

    positive_i03, positives, negatives = _supported_i03(admission, compilation)
    authority_ref = compilation.issued.workload.discoveries[0]
    discovery = execute_saved_i05(
        admission, discovery_authority_ref=authority_ref)
    if not discovery.receipts:
        raise AssertionError("no actual I05 receipts")

    units = tuple(
        BatchUnitSpec(
            "QUERY", request.query_ref,
            (admission.release_ref,), (compilation.issued.workload.decision_ref,),
        )
        for request in compilation.issued.workload.requests
    ) + tuple(
        BatchUnitSpec(
            "DISCOVERY", authority,
            (admission.release_ref,), (compilation.issued.workload.decision_ref,),
        )
        for authority in compilation.issued.workload.discoveries
    )
    manifest = BatchManifest(units)
    predicates = {
        request.query_ref.key: request.predicate_ref
        for request in compilation.issued.workload.requests
    }
    batch = execute_saved_batch(
        admission, manifest=manifest, predicate_ref_by_query=predicates,
    )
    if not all(getattr(r, "state", None) == "COMPLETED" for r in batch.receipts):
        raise AssertionError("batch did not complete every issued unit")

    normal = execute_issued_workload(
        compilation.issued.workload, resolver, source_factory=None,
        saved_admission_factory=lambda: admission,
        host=_NATIVE_HOST, purpose=_NATIVE_PURPOSE, allow_test_only=True,
    )
    if not all(getattr(r, "state", None) == "COMPLETED" for r in normal.receipts):
        raise AssertionError("normal saved workload did not complete")

    joined = join_saved_source_operation_fates(
        handoff=handoff, estate_receipt=estate, admission=admission,
        compilation=compilation, workload=compilation.issued.workload,
        resolver=resolver, host=_NATIVE_HOST, purpose=_NATIVE_PURPOSE,
        runner=batch,
    )
    if len(joined.rows) != len(handoff.operation_fates):
        raise AssertionError("postconsumer rows do not conserve operation fates")
    if joined.audit["positive_native_linked_operations"] <= 0:
        raise AssertionError("no positive native linked operation")

    return {
        "source_sha256": handoff.source_sha256,
        "roots": handoff.roots.__dict__,
        "stats": handoff.stats.__dict__,
        "family_counts": dict(estate.family_counts),
        "estate_path": str(estate.path),
        "retained_bytes": getattr(estate, "retained_bytes", None),
        "manifest_sha256": estate.manifest_sha256,
        "reconstructed_release": str(estate.reconstructed_v1_release_ref),
        "i03_positive": positive_i03,
        "i03_positive_count": len(positives),
        "i03_negative_count": len(negatives),
        "i03_negative_examples": negatives[:3],
        "i05_receipt_count": len(discovery.receipts),
        "i05_states": sorted({r.typed_state for r in discovery.receipts}),
        "batch_unit_count": len(batch.receipts),
        "batch_states": sorted({getattr(r, "state", None) for r in batch.receipts}),
        "normal_receipt_count": len(normal.receipts),
        "normal_states": sorted({getattr(r, "state", None) for r in normal.receipts}),
        "join_result_hash": joined.result_hash,
        "join_audit": dict(joined.audit),
        "join_row_count": len(joined.rows),
        "join_positive_rows": sum(
            1 for row in joined.rows
            if str(row.get("postconsumer_state", "")).startswith(
                "TEST_ONLY_SAVED_NATIVE")
        ),
        "original_issued_refs_empty": all(
            row["issued_receipt_refs"] == () for row in handoff.operation_fates),
        "noneligible_rows_without_native_receipts": all(
            not row["postconsumer_receipt_refs"]
            for row in joined.rows if row["disposition"] != "ELIGIBLE"
        ),
        "body_objects": sink.stats["body_objects"],
        "family_yields": dict(sink.stats["family_yields"]),
        "journal_bytes": sink.stats["journal_bytes"],
        "stage_clean": not any(bundle["stage"].rglob(".s1e-body-journal-*"))
        and not any(bundle["stage"].rglob(".s2c-stage-*")),
        "parquet_members": len(list(Path(estate.path).glob("*.parquet"))),
        "parent_maxrss_raw": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "positive_refs": [row["fact_ref"] for row in positives],
        "negative_refs": [row["fact_ref"] for row in negatives],
    }


def _negative_witnesses(bundle) -> dict:
    handoff = bundle["handoff"]
    estate = bundle["estate"]
    compilation = bundle["compilation"]
    admission = bundle["admission"]
    resolver = bundle["resolver"]
    workload = compilation.issued.workload
    units = tuple(
        BatchUnitSpec("QUERY", request.query_ref,
                      (admission.release_ref,), (workload.decision_ref,))
        for request in workload.requests
    ) + tuple(
        BatchUnitSpec("DISCOVERY", authority,
                      (admission.release_ref,), (workload.decision_ref,))
        for authority in workload.discoveries
    )
    batch = BatchExecutionRunner(
        manifest=BatchManifest(units), repository=admission, saved_mode=True)
    out = {}

    held_target = next(
        row for row in handoff.operation_fates if row["disposition"] == "HELD")
    altered = tuple(
        {**row, "disposition": "ELIGIBLE"}
        if row["operation_id"] == held_target["operation_id"] else row
        for row in handoff.operation_fates
    )
    forged = replace(handoff, operation_fates=altered)
    try:
        join_saved_source_operation_fates(
            handoff=forged, estate_receipt=estate, admission=admission,
            compilation=compilation, workload=workload, resolver=resolver,
            host=_NATIVE_HOST, purpose=_NATIVE_PURPOSE, runner=batch,
        )
    except SourceReceiptJoinError as exc:
        out["held_promotion_refusal"] = str(exc)
    else:
        raise AssertionError("forged HELD promotion was not refused")

    audit = dict(handoff.census_audit)
    audit["frontier_hash"] = "0" * 64
    forged_frontier = replace(handoff, census_audit=audit)
    try:
        join_saved_source_operation_fates(
            handoff=forged_frontier, estate_receipt=estate,
            admission=admission, compilation=compilation, workload=workload,
            resolver=resolver, host=_NATIVE_HOST, purpose=_NATIVE_PURPOSE,
            runner=batch,
        )
    except SourceReceiptJoinError as exc:
        out["frontier_drift_refusal"] = str(exc)
    else:
        raise AssertionError("forged Q2 frontier was not refused")

    return out


def _dir_bytes(path: Path) -> int:
    return sum(p.stat().st_size for p in path.rglob("*") if p.is_file())


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    root.mkdir(parents=True, exist_ok=True)
    started = time.time()
    baseline_fixture = _fix_fixture(
        _native_fixture(root / "baseline", values=(0., 1., 0., 1., 0.)))
    baseline = _materialize(root / "baseline", baseline_fixture)
    baseline_run = _run_once(baseline)

    changed_fixture = _fix_fixture(
        _native_fixture(root / "changed", values=(0., 1., 1., 1., 0.)))
    changed = _materialize(root / "changed", changed_fixture)
    changed_run = _run_once(changed)

    # Restore exactly the baseline SAV bytes: reuse the baseline fixture path
    # and config, only changing the destination/staging root.
    restored = _materialize(root / "restored", baseline_fixture)
    restored_run = _run_once(restored)

    baseline_fact = baseline_run["i03_positive"]["fact_ref"]
    changed_fact = changed_run["i03_positive"]["fact_ref"]
    restored_fact = restored_run["i03_positive"]["fact_ref"]
    if baseline_run["source_sha256"] == changed_run["source_sha256"]:
        raise AssertionError("changed source SHA did not change")
    if baseline_run["roots"]["logical"] != restored_run["roots"]["logical"]:
        raise AssertionError("restored source logical root differs")
    if baseline_fact == changed_fact:
        raise AssertionError("changed value did not change actual I03 fact")
    if baseline_fact != restored_fact:
        raise AssertionError("restored actual I03 fact differs")
    if baseline_run["join_result_hash"] != restored_run["join_result_hash"]:
        raise AssertionError("restored fate join hash differs")

    negatives = _negative_witnesses(baseline)
    elapsed = time.time() - started
    result = {
        "schema": "PYAT997_NATIVE_P0_P1_PROOF@1",
        "candidate_sha": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True).strip(),
        "sourcefree": True,
        "fixture": "TEST_ONLY generated SAV; no original35/source bytes",
        "baseline": baseline_run,
        "changed": changed_run,
        "restored": restored_run,
        "change_restore": {
            "baseline_fact": baseline_fact,
            "changed_fact": changed_fact,
            "restored_fact": restored_fact,
            "baseline_source_sha": baseline_run["source_sha256"],
            "changed_source_sha": changed_run["source_sha256"],
            "baseline_logical_root": baseline_run["roots"]["logical"],
            "restored_logical_root": restored_run["roots"]["logical"],
            "join_hash_baseline": baseline_run["join_result_hash"],
            "join_hash_restored": restored_run["join_result_hash"],
        },
        "negative_witnesses": negatives,
        "resource": {
            "elapsed_seconds": elapsed,
            "retained_bytes_baseline": baseline_run["retained_bytes"],
            "retained_bytes_changed": changed_run["retained_bytes"],
            "retained_bytes_restored": restored_run["retained_bytes"],
            "stage_bytes_baseline": _dir_bytes(root / "baseline"),
            "stage_bytes_changed": _dir_bytes(root / "changed"),
            "stage_bytes_restored": _dir_bytes(root / "restored"),
            "source_reads_baseline": baseline_run["stats"]["source_reads"],
            "decode_calls_baseline": baseline_run["stats"]["decode_calls"],
            "cell_passes_baseline": baseline_run["stats"]["cell_passes"],
            "full_c11_builds_baseline": baseline_run["stats"]["full_c11_builds"],
            "parent_maxrss_raw": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "full_100k_6gib": "NOT_RUN",
        },
        "limits": [
            "Small TEST_ONLY SAV fixture, not original35 or 100k.",
            "One native process; not an independent G5.",
            "No new source/current/actor/scientific authority.",
        ],
    }
    out = root / "native_proof.json"
    out.write_text(json.dumps(result, indent=2, default=str) + "\n")
    print(json.dumps({
        "status": "PASS",
        "native_proof": str(out),
        "baseline_fact": baseline_fact,
        "changed_fact": changed_fact,
        "restored_fact": restored_fact,
        "join_hash": baseline_run["join_result_hash"],
        "i03_supported": baseline_run["i03_positive_count"],
        "i03_negative": baseline_run["i03_negative_count"],
        "batch_units": baseline_run["batch_unit_count"],
        "negatives": negatives,
    }, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
