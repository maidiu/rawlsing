"""Cut2: actual sourcefree joined path, base admission vs prepared admission.

Read-only public API probe. It does not patch product, construct an issuer, or
replace compiler issuance. The first positive uses the existing exact base
SavedC11Admission and v2 issued workload. The second reopens the same persisted
estate as PreparedSavedC11Admission, executes the same actual issued Batch via
the cut1 wrappers, and then exercises the existing postconsumer join boundary.
"""
from __future__ import annotations

import json
from pathlib import Path
import tempfile

import pytest

from rawlsing_next.pre553_batch_runner import BatchManifest, BatchUnitSpec
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_governed_query_issuer_v2 import (
    _issue_compiled_governed_queries_v2,
)
from rawlsing_next.pre553_native_workload_binding import TestOnlyDecisionResolver
from rawlsing_next.pre553_prepared_saved_i03 import PreparedSavedC11Admission
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_saved_workload_integration import execute_saved_batch
from rawlsing_next.pre553_source_postconsumer_receipts import (
    SourceReceiptJoinError, join_saved_source_operation_fates,
)
from rawlsing_next.tests import test_pyat997_s1e_saved_native_first_consumer as s1e
from rawlsing_next.tests.test_pyat997_r03_governed_query_issuer_v2 import _v2_admission


def main() -> int:
    evidence = Path("/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/"
                    "IMPLEMENTER/WORKER_RETURNS/ANVIL_ENGINEERING_CUT2_JOINED_20261117/"
                    "evidence")
    tmp_parent = Path("/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/"
                      "IMPLEMENTER/WORKER_RETURNS/ANVIL_ENGINEERING_CUT2_JOINED_20261117/"
                      "tmp")
    tmp_parent.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix="joined_probe_", dir=tmp_parent))
    handoff, estate, base_original, v1, _resolver, _sink = s1e._full(
        root / "sourcefree-q2",
    )
    issue = _issue_compiled_governed_queries_v2(v1)
    workload = issue.issued.workload
    base = _v2_admission(base_original, workload.catalog)
    manifest, predicates = s1e._issued_manifest(workload, base)
    base_runner = execute_saved_batch(
        base, manifest=manifest, predicate_ref_by_query=predicates,
    )
    base_join = join_saved_source_operation_fates(
        handoff=handoff, estate_receipt=estate, admission=base,
        compilation=v1, workload=workload,
        resolver=TestOnlyDecisionResolver(issue.issued.record),
        host=s1e._NATIVE_HOST, purpose=s1e._NATIVE_PURPOSE,
        runner=base_runner, issuer_v2=issue,
    )

    prepared = PreparedSavedC11Admission.open(
        root=Path(base.estate_path).parents[1],
        exact_path=base.estate_path,
        independently_held_manifest_sha256=base.manifest_sha256,
        independently_held_i02=base.i02,
        release_ref=base.release_ref,
        runtime_catalog=base._runtime_catalog,
        current_authorizer=lambda _roots: True,
    )
    builds = []
    original_build = DirectEstateI03Session._build

    def counted(self):
        builds.append(1)
        return original_build(self)

    monkey = pytest.MonkeyPatch()
    try:
        monkey.setattr(DirectEstateI03Session, "_build", counted)
        prepared_runner = execute_saved_batch(
            prepared, manifest=manifest, predicate_ref_by_query=predicates,
        )
    finally:
        monkey.undo()
    assert len(builds) == 1
    assert len(prepared_runner.receipts) == len(manifest.units)
    assert {r.state for r in prepared_runner.receipts} == {"COMPLETED"}

    prepared_join_error = None
    try:
        join_saved_source_operation_fates(
            handoff=handoff, estate_receipt=estate, admission=prepared,
            compilation=v1, workload=workload,
            resolver=TestOnlyDecisionResolver(issue.issued.record),
            host=s1e._NATIVE_HOST, purpose=s1e._NATIVE_PURPOSE,
            runner=prepared_runner, issuer_v2=issue,
        )
    except SourceReceiptJoinError as exc:
        prepared_join_error = str(exc)
    else:
        raise AssertionError("prepared join unexpectedly accepted")

    result = {
        "schema": "ANVIL_CUT2_JOINED_PROBE@1",
        "sourcefree": True,
        "fixture": "existing sourcefree Q2/native TEST_ONLY fixture",
        "source_sha256": handoff.source_sha256,
        "estate_manifest_sha256": estate.manifest_sha256,
        "roots": handoff.roots.__dict__,
        "family_counts": dict(handoff.counts),
        "source_stats": handoff.stats.__dict__,
        "compiler": {
            "v1_requests": len(v1.issued.workload.requests),
            "v1_discoveries": len(v1.issued.workload.discoveries),
            "v2_requests": len(workload.requests),
            "v2_discoveries": len(workload.discoveries),
            "v2_original_u_root": issue.issued.record.original_u_root,
            "v2_envelope_sha256": issue.issued.record.envelope_sha256,
        },
        "base_positive": {
            "admission_class": type(base).__name__,
            "batch_units": len(base_runner.receipts),
            "batch_states": sorted({r.state for r in base_runner.receipts}),
            "join_hash": base_join.result_hash,
            "join_audit": dict(base_join.audit),
            "positive_rows": sum(
                1 for row in base_join.rows
                if str(row.get("postconsumer_state", "")).startswith(
                    "TEST_ONLY_SAVED_NATIVE")
            ),
        },
        "prepared_positive": {
            "admission_class": type(prepared).__name__,
            "batch_units": len(prepared_runner.receipts),
            "batch_states": sorted({r.state for r in prepared_runner.receipts}),
            "prepared_index_builds": len(builds),
            "join_error": prepared_join_error,
            "join_result": "GAP" if prepared_join_error else "ACCEPTED",
        },
        "required_result": (
            "JOINED_BASE_PASS__PREPARED_JOIN_GAP"
            if base_join.audit.get("positive_native_linked_operations", 0) > 0
            and prepared_join_error
            else "UNEXPECTED"
        ),
        "prepared_join_boundary": {
            "file": "rawlsing_next/pre553_source_postconsumer_receipts.py",
            "function": "join_saved_source_operation_fates",
            "condition": "type(admission) is not SavedC11Admission",
            "current_owner": "S1-E/postconsumer receipt owner",
            "minimum_grant": "exact PreparedSavedC11Admission whitelist in the postconsumer join while preserving unchanged compiler/workload/receipt/fate checks",
        },
    }
    out = evidence / "joined_probe.json"
    out.write_text(json.dumps(result, indent=2, default=str) + "\n")
    print(json.dumps(result, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
