#!/usr/bin/env python3
"""Record exact per-run identities for the independent R02V positive cases."""
from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TEST = ROOT / "rawlsing_next/tests/test_universal_source_projection.py"
spec = importlib.util.spec_from_file_location("r02v_receipt_test", TEST)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def repeated_case(path, rows, respondents, occasions, include_missing):
    module.write_rows(path, rows)
    incidence = module.decode_sav(path)
    source_package = module.package(
        path, incidence.row_count,
        (module.NativeSourceRule("impl.score", "SCORE"),))
    plan = module._r02v_plan(respondents, occasions)
    domain, tuples = module._r02v_expected_domain_and_tuples(
        source_package, incidence, plan)
    bundle = module.materialize_native_preimages(
        package=source_package, incidence=incidence,
        row_occurrence_plan=plan)
    included = ["SUBSTANTIVE_RESPONSE"]
    if include_missing:
        included.append("MISSING")
    fact = module._r02v_run_query(
        bundle, domain, "SCORE", "REPEATED_EVENT", tuple(included),
        "r02v-receipt")
    return {
        "source_sha256": bundle.source_sha256,
        "package_hash": bundle.package_hash,
        "projection_ref": bundle.projection.projection_identity_ref.as_dict(),
        "release_ref": bundle.release.release_ref.as_dict(),
        "event_count": len(tuples),
        "event_tuples": [list(item) for item in tuples],
        "query_domain": domain,
        "i03_fact_ref": fact.ref.as_dict(),
        "i03_state": fact.typed_state,
        "i03_raw_denominator": fact.raw_denominator_support,
        "i03_raw_numerator": fact.raw_numerator_support,
        "i03_cell_count": len(fact.target_topology.get(
            "complete_cell_semantic_projection", [])),
    }


with tempfile.TemporaryDirectory(prefix="r02v-receipt-") as directory:
    directory = Path(directory)
    permuted_rows = []
    for respondent in range(4):
        for occasion in range(3):
            permuted_rows.append({
                "PID": float(respondent),
                "OCCASION": float(occasion),
                "SCORE": float((respondent * 5 + occasion * 2) % 4),
            })
    permuted = repeated_case(
        directory / "permuted_4x3.sav",
        permuted_rows[1::2] + permuted_rows[0::2],
        4, 3, include_missing=False)
    missing_rows = [
        {"PID": float(respondent), "OCCASION": float(occasion),
         "SCORE": float(respondent % 3)}
        for respondent in range(3) for occasion in range(2)
    ]
    missing_rows[1]["SCORE"] = None
    missing = repeated_case(
        directory / "missing_3x2.sav", missing_rows, 3, 2,
        include_missing=True)
    print(json.dumps({
        "schema": "R02V_INDEPENDENT_RECEIPT@1",
        "permuted_4x3": permuted,
        "missing_3x2": missing,
    }, indent=2, sort_keys=True, default=dict))
