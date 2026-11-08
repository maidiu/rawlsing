#!/usr/bin/env python3
"""Minimum sourcefree nonrespondent witness for the existing universal workload API.

Uses the existing synthetic nonrespondent SAV fixture helper, compile_universal_workload,
execute_universal_workload, and the existing C11/I03/Batch consumer. It does not read
original respondent/SAV/DTA/DB data or create a new engine.
"""
from __future__ import annotations

import json
import hashlib
import tempfile
from dataclasses import replace
from pathlib import Path

from rawlsing_next.pre553_native_workload_binding import execute_test_only_workload
from rawlsing_next.pre553_universal_workload import (
    compile_universal_workload,
    execute_universal_workload,
)
from rawlsing_next.tests.test_universal_source_projection import write_rows, package, materialize_native_preimages
from rawlsing_next.pre553_source_native_preimage_adapter import NativeSourceRule
from rawlsing_next.pre553_physical_decoder import decode_dta

ROOT = Path("/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat777-source-consumer")
OUT = ROOT / "WORKER_RETURNS/PROGRAMMA_PYAT_FUNCTION_AUTHORITY_SEVERANCE_AND_ADEQUACY_20261107_R1/C9_WORKLOAD_AUTHORITY_FIRST_CONSUMER"
AS_OF = "2026-11-07"
HOST = "c9-local-sourcefree"
PURPOSE = "TEST_ONLY_SOURCEFREE"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    with tempfile.TemporaryDirectory(dir=OUT / "tmp") as td:
        path = Path(td) / "c9_nonrespondent.dta"
        rows = [{"PID": float(i), "OCCASION": 0.0, "A": float(i % 2),
                 "Y": float((i // 2) % 2)} for i in range(6)]
        write_rows(path, rows, fmt="dta")
        pkg = package(
            path, len(rows),
            (NativeSourceRule("impl.a", "A"), NativeSourceRule("impl.y", "Y")),
            coordinate="OCCASION", source_format="DTA",
        )
        bundle = materialize_native_preimages(package=pkg, incidence=decode_dta(path))
        compilation = compile_universal_workload(
            bundle=bundle, as_of=AS_OF, host=HOST, purpose=PURPOSE
        )
        positive = execute_universal_workload(
            compilation=compilation,
            source_factory=lambda _ref: bundle.physical_stream,
        )
        good_facts = tuple(ref.key for ref in positive.fact_refs)
        first = next(item.issued for item in compilation.compiled if item.issued is not None)
        query = first.workload.catalog.queries[0]
        target_use = [
            a.authority_id for a in first.workload.catalog.authorities
            if getattr(a, "authority_kind", "") == "TARGET_USE_PERMISSION"
        ]
        query_auth = [
            a.authority_id for a in first.workload.catalog.authorities
            if getattr(a, "authority_kind", "") == "PREDICATE_GRAMMAR"
        ]
        bad = execute_universal_workload(
            compilation=compilation,
            source_factory=lambda _ref: replace(bundle.physical_stream, source_sha256="b" * 64),
        )
        host_scope = {"case": "wrong_host_purpose", "result": "NO_EXCEPTION"}
        try:
            execute_test_only_workload(
                issued=first, source_factory=lambda _ref: bundle.physical_stream,
                host="wrong-host", purpose="wrong-purpose",
            )
        except Exception as exc:  # expected typed refusal
            host_scope = {
                "case": "wrong_host_purpose",
                "result": "TYPED_REFUSAL",
                "exception": type(exc).__name__,
                "message": str(exc)[:300],
            }
        restored = execute_universal_workload(
            compilation=compilation,
            source_factory=lambda _ref: bundle.physical_stream,
        )
        result = {
            "schema": "C9_WORKLOAD_SOURCEFREE_PROBE_V1",
            "fixture": "nonrespondent synthetic DTA from existing test package/materialize helper",
            "sourcefree_only": True,
            "response": {
                "operations": len(compilation.operations),
                "compiled_operations": sum(1 for op in compilation.operations if op.status == "COMPILED"),
                "expected_jobs": [list(x) for x in compilation.expected_jobs],
                "executed_operation_ids": list(positive.executed_operation_ids),
                "native_result_count": len(positive.native_results),
                "receipt_count": len(positive.receipt_refs),
                "fact_count": len(positive.fact_refs),
                "fact_refs": [r.as_dict() for r in positive.fact_refs],
                "anti_join": positive.anti_join(),
                "fact_typed_states": [f.typed_state for result in positive.native_results for output in result.native_outputs for f in getattr(output, "facts", ())],
                "fact_support": [{"typed_state": f.typed_state, "raw_denominator_support": f.raw_denominator_support, "raw_numerator_support": f.raw_numerator_support} for result in positive.native_results for output in result.native_outputs for f in getattr(output, "facts", ())],
                "source_sha256": bundle.source_sha256,
                "authority_scope": first.record.scope,
                "authority_currentness": first.record.currentness,
                "query_authority_ids": query_auth,
                "target_use_permission_ids": target_use,
                "query_target_count": len(query.target_refs),
                "query_measure_kind": query.requested_output_grain.get("measure_kind"),
                "query_risk_set_type": query.requested_output_grain.get("risk_set_type"),
                "query_uncertainty": query.requested_output_grain.get("uncertainty_method_or_typed_state"),
                "query_has_selected_target_use": bool(target_use),
            },
            "wrong_source_sha": {
                "executed_operation_ids": list(bad.executed_operation_ids),
                "failed_count": len(bad.failed),
                "anti_join": bad.anti_join(),
            },
            "wrong_host_purpose": host_scope,
            "restoration": {
                "fact_refs_match": good_facts == tuple(ref.key for ref in restored.fact_refs),
                "anti_join": restored.anti_join(),
            },
            "limits": [
                "SOURCEFREE_TEST_ONLY_SCOPE, not original issuer/native/science",
                "no original respondent/SAV/DTA/DB read",
                "the fixture is not a shared35 source/wave and does not prove shared35 demand",
                "no production installation or new engine",
            ],
        }
        out_json = OUT / "probes/workload_probe.json"
        out_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
