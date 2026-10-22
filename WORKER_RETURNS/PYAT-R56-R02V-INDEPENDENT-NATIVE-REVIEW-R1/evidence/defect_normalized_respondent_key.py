#!/usr/bin/env python3
"""Minimal reproducer: normalized duplicate respondent keys collapse two source respondents.

Run from the repository root:
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 \
    WORKER_RETURNS/PYAT-R56-R02V-INDEPENDENT-NATIVE-REVIEW-R1/evidence/defect_normalized_respondent_key.py
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from rawlsing_next.pre553_physical_decoder import decode_sav
from rawlsing_next.tests.test_universal_source_projection import (
    NativeSourceRule,
    domain_from_bundle,
    event_tuples,
    materialize_native_preimages,
    occurrence_plan,
    package,
    run_repeated,
    write_rows,
)


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "collision.sav"
        rows = [
            {"PID": 0.0, "OCCASION": 0.0, "SCORE": 7.0},
            {"PID": 1.0, "OCCASION": 1.0, "SCORE": 9.0},
        ]
        write_rows(path, rows)
        incidence = decode_sav(path)
        source_package = package(
            path, incidence.row_count,
            (NativeSourceRule("impl.score", "SCORE"),))
        plan = occurrence_plan(
            (("SCORE", "REPEATED_EVENT", (
                ("0", "zero", {"kind": "REPEATED_EVENT",
                               "multiplicity_index": 0}),
                ("1", "one", {"kind": "REPEATED_EVENT",
                              "multiplicity_index": 1}),
            )),),
            {0: "1", 1: 1})
        bundle = materialize_native_preimages(
            package=source_package, incidence=incidence,
            row_occurrence_plan=plan)
        fact = run_repeated(bundle, domain_from_bundle(bundle))
        print(json.dumps({
            "governed_mapping": {"0": "1", "1": 1},
            "source_respondent_tokens": [
                "0", "1"],
            "source_sha256": bundle.source_sha256,
            "expected_c11_respondents": 2,
            "actual_c11_respondents": len(bundle.projection.respondents),
            "actual_c11_respondent_keys": [
                respondent.respondent_key
                for respondent in bundle.projection.respondents],
            "event_tuples": [list(item) for item in event_tuples(bundle)],
            "row_evidence": [dict(row) for row in bundle.respondent_rows],
            "i03_fact_state": fact.typed_state,
            "i03_raw_denominator": fact.raw_denominator_support,
            "i03_raw_numerator": fact.raw_numerator_support,
        }, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
