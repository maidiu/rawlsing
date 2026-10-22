#!/usr/bin/env python3
"""R02 r2: prove the two normalized-mapping defects now refuse and positives survive."""
from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
TEST = ROOT / "rawlsing_next/tests/test_universal_source_projection.py"
spec = importlib.util.spec_from_file_location("r02_r2_receipt_test", TEST)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def materialize_case(path, rows, mapping):
    module.write_rows(path, rows)
    incidence = module.decode_sav(path)
    source_package = module.package(
        path, incidence.row_count,
        (module.NativeSourceRule("impl.score", "SCORE"),))
    plan = module.occurrence_plan(
        (("SCORE", "REPEATED_EVENT", (
            ("0", "zero", {"kind": "REPEATED_EVENT",
                           "multiplicity_index": 0}),
            ("1", "one", {"kind": "REPEATED_EVENT",
                          "multiplicity_index": 1}),
        )),),
        mapping)
    return source_package, incidence, plan


def refusal(path, rows, mapping):
    source_package, incidence, plan = materialize_case(path, rows, mapping)
    try:
        module.materialize_native_preimages(
            package=source_package, incidence=incidence,
            row_occurrence_plan=plan)
    except module.NativePreimageRefusal as error:
        return {
            "refused": True,
            "code": error.code,
            "detail": error.detail,
            "source_sha256": incidence.source_sha256,
        }
    return {"refused": False, "error": "accepted"}


def positive(path, rows, mapping):
    source_package, incidence, plan = materialize_case(path, rows, mapping)
    domain, tuples = module._r02v_expected_domain_and_tuples(
        source_package, incidence, plan)
    bundle = module.materialize_native_preimages(
        package=source_package, incidence=incidence,
        row_occurrence_plan=plan)
    fact = module._r02v_run_query(
        bundle, domain, "SCORE", "REPEATED_EVENT",
        ("SUBSTANTIVE_RESPONSE",), "r02-r2-receipt")
    return {
        "source_sha256": bundle.source_sha256,
        "release_ref": bundle.release.release_ref.as_dict(),
        "event_count": len(tuples),
        "event_tuples": [list(item) for item in tuples],
        "i03_fact_ref": fact.ref.as_dict(),
        "i03_state": fact.typed_state,
        "i03_raw_denominator": fact.raw_denominator_support,
        "i03_raw_numerator": fact.raw_numerator_support,
    }


with tempfile.TemporaryDirectory(prefix="r02-r2-receipt-") as directory:
    directory = Path(directory)
    base_rows = [
        {"PID": 0.0, "OCCASION": 0.0, "SCORE": 7.0},
        {"PID": 1.0, "OCCASION": 1.0, "SCORE": 9.0},
    ]
    positive_rows = [
        {"PID": 0.0, "OCCASION": 0.0, "SCORE": 0.0},
        {"PID": 0.0, "OCCASION": 1.0, "SCORE": 1.0},
        {"PID": 1.0, "OCCASION": 0.0, "SCORE": 2.0},
        {"PID": 1.0, "OCCASION": 1.0, "SCORE": 3.0},
        {"PID": 2.0, "OCCASION": 0.0, "SCORE": 1.0},
        {"PID": 2.0, "OCCASION": 1.0, "SCORE": 0.0},
    ]
    print(json.dumps({
        "schema": "R02_R2_DEFECT_RESOLUTION_RECEIPT@1",
        "defect_d1_normalized_destination_collision": refusal(
            directory / "d1.sav", base_rows, {0: "1", 1: 1}),
        "defect_d2_normalized_source_key_collision": refusal(
            directory / "d2.sav", base_rows,
            {0: "P0", "0": "P1", 1: "P2"}),
        "near_positive_int_source_keys": positive(
            directory / "p_int.sav", positive_rows,
            {0: "P0", 1: "P1", 2: "P2"}),
        "near_positive_float_source_keys_permuted": positive(
            directory / "p_float.sav", list(reversed(positive_rows)),
            {0.0: "P0", 1.0: "P1", 2.0: "P2"}),
        "near_positive_numeric_destinations": positive(
            directory / "p_numeric_dest.sav", positive_rows,
            {0: 1, 1: 2, 2: 3}),
    }, indent=2, sort_keys=True, default=str))
