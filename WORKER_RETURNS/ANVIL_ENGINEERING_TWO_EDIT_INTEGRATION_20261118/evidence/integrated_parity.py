"""Bounded production postconsumer witness for the grant.

Calls the actual sourcefree Q2 fixture, R03 v2 issuer, saved Batch and
postconsumer join. No product patch or synthetic admission is used.
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_governed_query_issuer_v2 import (
    _issue_compiled_governed_queries_v2,
)
from rawlsing_next.pre553_native_workload_binding import TestOnlyDecisionResolver
from rawlsing_next.pre553_prepared_saved_i03 import PreparedSavedC11Admission
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_saved_workload_integration import execute_saved_batch
from rawlsing_next.pre553_source_postconsumer_receipts import (
    join_saved_source_operation_fates,
)
from rawlsing_next.tests import test_pyat997_s1e_saved_native_first_consumer as s1e
from rawlsing_next.tests.test_pyat997_r03_governed_query_issuer_v2 import (
    _v2_admission,
)


def main() -> int:
    evidence = Path(
        "/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/"
        "IMPLEMENTER/WORKER_RETURNS/"
        "ANVIL_ENGINEERING_TWO_EDIT_INTEGRATION_20261118/evidence"
    )
    parent = evidence.parent / "tmp"
    parent.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix="postconsumer_witness_", dir=parent))
    handoff, estate, base0, v1, _resolver, _sink = s1e._full(
        root / "sourcefree-q2"
    )
    issue = _issue_compiled_governed_queries_v2(v1)
    workload = issue.issued.workload
    base = _v2_admission(base0, workload.catalog)
    prepared = PreparedSavedC11Admission.open(
        root=Path(base.estate_path).parents[1],
        exact_path=base.estate_path,
        independently_held_manifest_sha256=base.manifest_sha256,
        independently_held_i02=base.i02,
        release_ref=base.release_ref,
        runtime_catalog=workload.catalog,
        current_authorizer=lambda _roots: True,
    )
    manifest, predicates = s1e._issued_manifest(workload, base)

    def run(admission, count_builds=False):
        builds = []
        original = DirectEstateI03Session._build

        def counted(self):
            builds.append(1)
            return original(self)

        if count_builds:
            DirectEstateI03Session._build = counted
        try:
            runner = execute_saved_batch(
                admission, manifest=manifest,
                predicate_ref_by_query=predicates,
            )
        finally:
            if count_builds:
                DirectEstateI03Session._build = original
        return runner, len(builds)

    base_runner, _ = run(base)
    prepared_runner, builds = run(prepared, count_builds=True)

    def join(admission, runner):
        return join_saved_source_operation_fates(
            handoff=handoff, estate_receipt=estate, admission=admission,
            compilation=v1, workload=workload,
            resolver=TestOnlyDecisionResolver(issue.issued.record),
            host=s1e._NATIVE_HOST, purpose=s1e._NATIVE_PURPOSE,
            runner=runner, issuer_v2=issue,
        )

    base_joined = join(base, base_runner)
    prepared_joined = join(prepared, prepared_runner)
    result = {
        "schema": "ANVIL_PRODUCTION_POSTCONSUMER_WITNESS@1",
        "sourcefree": True,
        "fixture": {
            "source_sha256": handoff.source_sha256,
            "estate_manifest_sha256": estate.manifest_sha256,
            "roots": dict(handoff.roots.__dict__),
            "family_counts": dict(handoff.counts),
            "stats": dict(handoff.stats.__dict__),
        },
        "compiler": {
            "v1_queries": len(v1.issued.workload.requests),
            "v1_discoveries": len(v1.issued.workload.discoveries),
            "v2_queries": len(workload.requests),
            "v2_discoveries": len(workload.discoveries),
            "v2_original_u_root": issue.issued.record.original_u_root,
            "v2_envelope_sha256": issue.issued.record.envelope_sha256,
        },
        "base": {
            "admission_class": type(base).__name__,
            "batch_units": len(base_runner.receipts),
            "batch_states": sorted({r.state for r in base_runner.receipts}),
            "join_hash": base_joined.result_hash,
            "join_audit": dict(base_joined.audit),
        },
        "prepared": {
            "admission_class": type(prepared).__name__,
            "batch_units": len(prepared_runner.receipts),
            "batch_states": sorted({r.state for r in prepared_runner.receipts}),
            "prepared_index_builds": builds,
            "join_hash": prepared_joined.result_hash,
            "join_audit": dict(prepared_joined.audit),
        },
        "parity": {
            "rows": len(base_joined.rows) == len(prepared_joined.rows) == 22,
            "rows_equal": base_joined.rows == prepared_joined.rows,
            "audit_equal": base_joined.audit == prepared_joined.audit,
            "result_hash_equal": (
                base_joined.result_hash == prepared_joined.result_hash
            ),
            "batch_provenance_equal": all(
                a.provenance_refs == b.provenance_refs
                for a, b in zip(
                    prepared_runner.receipts, base_runner.receipts,
                )
            ),
        },
    }
    (evidence / "integrated_parity.json").write_text(
        json.dumps(result, indent=2, default=str) + "\n"
    )
    print(json.dumps(result, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
