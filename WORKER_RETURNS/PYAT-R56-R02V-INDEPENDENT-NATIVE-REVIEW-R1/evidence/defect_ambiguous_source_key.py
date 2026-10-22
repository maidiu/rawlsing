#!/usr/bin/env python3
"""Minimal reproducer: a normalized source-key collision silently selects one label.

Run from the repository root:
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 \
    WORKER_RETURNS/PYAT-R56-R02V-INDEPENDENT-NATIVE-REVIEW-R1/evidence/defect_ambiguous_source_key.py
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from rawlsing_next.pre553_physical_decoder import decode_sav
from rawlsing_next.tests.test_universal_source_projection import (
    NativeSourceRule,
    event_tuples,
    materialize_native_preimages,
    occurrence_plan,
    package,
    write_rows,
)


def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "ambiguous.sav"
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
            {0: "P0", "0": "P1", 1: "P2"})
        bundle = materialize_native_preimages(
            package=source_package, incidence=incidence,
            row_occurrence_plan=plan)
        print(json.dumps({
            "governed_mapping_keys": ["0 (int)", "0 (str)", "1 (int)"],
            "governed_mapping_values": ["P0", "P1", "P2"],
            "expected": "REFUSE_AMBIGUOUS_SOURCE_KEY_MAPPING",
            "actual": "ACCEPTED",
            "source_sha256": bundle.source_sha256,
            "row_evidence": [dict(row) for row in bundle.respondent_rows],
            "event_tuples": [list(item) for item in event_tuples(bundle)],
        }, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
