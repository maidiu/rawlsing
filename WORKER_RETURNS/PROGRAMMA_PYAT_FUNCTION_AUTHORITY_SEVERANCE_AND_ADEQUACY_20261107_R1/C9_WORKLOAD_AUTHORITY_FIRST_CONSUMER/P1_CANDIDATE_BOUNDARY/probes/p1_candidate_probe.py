#!/usr/bin/env python3
"""C9 P1 candidate boundary probe.

Stages the exact P1 candidate module and exact candidate test fixture under the
C9 sublease. The test fixture is used only for its sourcefree 35-wave input
builder; no production module is copied or modified.
"""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from dataclasses import replace
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from rawlsing_next.pre553_batch_runner import BatchIntegrityError, BatchExecutionRunner
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_issued_workload import execute_issued_workload
import inspect

ROOT = Path("/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-source-consumer")
OUT = ROOT / "WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C9_WORKLOAD_AUTHORITY_FIRST_CONSUMER/P1_CANDIDATE_BOUNDARY"
CAND = OUT / "vendor/programma_pyat_original35_constructor.py"
TEST = OUT / "vendor/test_programma_pyat_original35_constructor.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_candidate():
    spec = spec_from_file_location("rawlsing_next.programma_pyat_original35_constructor", CAND)
    module = module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_fixture(candidate):
    sys.modules["rawlsing_next.programma_pyat_original35_constructor"] = candidate
    spec = spec_from_file_location("c9_p1_candidate_fixture", TEST)
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def ref_summary(ref) -> dict:
    return {"kind": ref.kind, "object_id": ref.object_id, "content_hash": ref.content_hash}


def main() -> int:
    candidate = load_candidate()
    fixture = load_fixture(candidate)
    assert candidate.__dict__["CONSTRUCTOR_STATUS"] == "NONISSUING_SOURCEFREE_PROSPECTIVE_CONSTRUCTION_ONLY"

    base_waves = fixture._input().waves
    plan = candidate.construct_original35_epre(fixture._input())
    first_unit = plan.batch_units[0]
    first_operation = plan.operations[0]
    manifest_admission = plan.batch_manifest is not None and plan.batch_manifest.units == plan.batch_units

    release_error = None
    try:
        BatchExecutionRunner(manifest=plan.batch_manifest, repository=C11Repository())
    except Exception as exc:
        release_error = {
            "exception": type(exc).__name__,
            "message": str(exc),
            "first_unit_ref": ref_summary(first_unit.unit_ref),
            "first_release_ref": ref_summary(first_unit.release_refs[0]),
            "first_job_ref": ref_summary(first_unit.job_ref),
        }

    # Current execute_issued_workload is the I03 receiving entry point; it takes
    # NativeWorkload, not a BatchManifest, and resolves unit job refs only through
    # its internal requests_by_query map.
    issued_sig = str(inspect.signature(execute_issued_workload))
    issued_src = inspect.getsource(execute_issued_workload)
    request_lookup = "requests_by_query[unit.job_ref.key]" in issued_src

    # Candidate's own negative/restoration fixture: wrong source identity on wave 0.
    wrong_hash = fixture._h("wrong-c9-source-sha")
    bad_grant = replace(base_waves[0].source_grant, source_sha256=wrong_hash)
    bad_waves = (replace(base_waves[0], source_grant=bad_grant),) + tuple(base_waves[1:])
    bad_plan = candidate.construct_original35_epre(fixture._input(waves=bad_waves))
    restored_plan = candidate.construct_original35_epre(fixture._input(waves=base_waves))

    result = {
        "schema": "C9_P1_CANDIDATE_BOUNDARY_PROBE_V1",
        "candidate": {
            "commit": "d1278613e9e1a5d986ccce15782a697f19cbd722",
            "blob_sha1": "c8352c5ab0fbc1a817c38d8ef99d64beef628230",
            "staged_sha256": sha256(CAND),
            "staged_test_sha256": sha256(TEST),
            "test_blob_sha1": "1f96aca99543acf9ec496f31f2c43969220f74bf",
            "constructor_id": candidate.CONSTRUCTOR_ID,
            "constructor_status": candidate.CONSTRUCTOR_STATUS,
            "scope": candidate.SCOPE_TEST_ONLY,
        },
        "declared_scope": {
            "fixture_waves": len(plan.roster),
            "family": sorted({wave.identity.source_family for wave in plan.waves}),
            "roster_ref": plan.roster_ref,
            "plan_ref": plan.plan_ref,
            "source_qualification": plan.source_qualification,
            "all35_populated_claim": plan.all35_populated_claim,
            "sourced_results_claim": plan.sourced_results_claim,
            "wave_ids": [w.identity.atlas_id for w in plan.waves],
            "expected_items": plan.no_drop_manifest["expected_item_count"],
            "processed_items": plan.no_drop_manifest["processed_item_count"],
            "operations": len(plan.operations),
            "batch_units": len(plan.batch_units),
            "holds": len(plan.holds),
            "abstentions": len(plan.abstentions),
            "no_drop_ok": plan.no_drop_ok,
        },
        "first_unit": {
            "unit_ref": ref_summary(first_unit.unit_ref),
            "job_kind": first_unit.job_kind,
            "job_ref": ref_summary(first_unit.job_ref),
            "release_refs": [ref_summary(ref) for ref in first_unit.release_refs],
            "semantic_input_refs": [ref_summary(ref) for ref in first_unit.semantic_input_refs],
        },
        "first_operation": {
            "operation_ref": ref_summary(first_operation.operation_ref),
            "status": first_operation.status,
            "operation_kind": first_operation.operation_kind,
            "target_value": first_operation.target_value,
            "batch_job_ref": ref_summary(first_operation.batch_job_ref) if first_operation.batch_job_ref else None,
        },
        "current_batch_manifest_admission": {
            "manifest_ref": ref_summary(plan.batch_manifest.manifest_ref),
            "units": len(plan.batch_manifest.units),
            "accepted_units_equal_plan": manifest_admission,
            "manifest_semantic_projection_hash": hashlib.sha256(
                json.dumps(plan.batch_manifest.semantic_projection(), sort_keys=True).encode()
            ).hexdigest(),
        },
        "current_batch_first_consumer_attempt": {
            "call": "BatchExecutionRunner(manifest=plan.batch_manifest, repository=C11Repository())",
            "result": release_error,
            "interpretation": "The current BatchExecutionRunner starts with exact C11 release resolution before any executor call; candidate C11LogicalRelease refs are synthetic test refs and are absent from the repository.",
        },
        "current_i03_receiving_entry": {
            "function": "pre553_issued_workload.execute_issued_workload",
            "signature": issued_sig,
            "takes_batch_manifest": "manifest" in issued_sig,
            "internal_request_lookup": request_lookup,
            "lookup_key_type": "unit.job_ref.key -> requests_by_query (NativeWorkload.requests)",
            "candidate_job_ref_kind": first_unit.job_ref.kind,
            "candidate_job_ref_has_query_request": False,
        },
        "negative_restoration": {
            "wrong_source_sha": wrong_hash,
            "wrong_plan_ref": bad_plan.plan_ref,
            "wrong_batch_units": len(bad_plan.batch_units),
            "wrong_abstentions": len(bad_plan.abstentions),
            "wrong_reasons": sorted({op.reason for op in bad_plan.abstentions}),
            "restored_plan_ref": restored_plan.plan_ref,
            "restored_batch_units": len(restored_plan.batch_units),
            "restored_matches_baseline": restored_plan.plan_ref == plan.plan_ref,
            "wrong_differs_baseline": bad_plan.plan_ref != plan.plan_ref,
        },
        "limits": [
            "Candidate fixture is synthetic TEST_ONLY_SOURCEFREE, not the actual original35 source roster.",
            "35 waves/70 items/840 operations are candidate-plan identity, not actual all35 execution or occupancy.",
            "No source bytes, respondent rows, native I03/I05 execution or scientific result.",
            "No source/current issuer, original target use, C11 release, or I03 request mapping was minted.",
            "The current BatchExecutionRunner first call fails on exact synthetic C11 release resolution; no new resolver was added.",
        ],
    }
    (OUT / "probes/p1_candidate_probe.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
