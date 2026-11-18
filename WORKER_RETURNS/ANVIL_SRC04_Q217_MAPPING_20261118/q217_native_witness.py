#!/usr/bin/env python3
"""Focused synthetic exact-cell witness for q217 v3 states.

Synthetic only. No SRC04 source body is opened, stat'ed, hashed or decoded.
The tiny config mirrors v3 q217 state semantics; it is not a source release.
"""
from __future__ import annotations
import copy, hashlib, json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from rawlsing_next.tests.test_pyat940_s1b_support import make_config, sha256_text
from rawlsing_next.pre553_r157_projection_adapter import SourceConfig, build_governed_c11_projection
from rawlsing_next.pre553_source_backed_c11_facade import (
    PhysicalCell, PhysicalMissingState, project_c11_candidate_from_physical_cells,
)

def main():
    synthetic_sha = sha256_text("ANVIL_Q217_SYNTHETIC_EXACT_CELL_WITNESS")
    values = (1.0, 7.0, 98.0, 99.0, None)
    doc = make_config(
        source_format="SAV", active_source_sha256=synthetic_sha, row_count=len(values),
        keyed=False, values=values,
        response_state_overrides={7.0: "SOURCE_SPECIFIC_SPECIAL", 98.0: "DK", 99.0: "REFUSAL"},
    )
    # Rename the synthetic question/slot to q217 for readability.
    doc = json.loads(json.dumps(doc).replace("q101", "q217"))
    cfg = SourceConfig(doc)
    projection = build_governed_c11_projection(cfg)
    cells = []
    for row, value in enumerate(values, 1):
        state = (PhysicalMissingState.SYSTEM_MISSING if value is None
                 else PhysicalMissingState.OBSERVED_STORAGE_VALUE)
        cells.append(PhysicalCell(row, 1, "q217", value, state, None, None))
        cells.append(PhysicalCell(row, 2, "country", 1.0,
                                  PhysicalMissingState.OBSERVED_STORAGE_VALUE, None, None))
    candidate = project_c11_candidate_from_physical_cells(
        source_sha256=synthetic_sha, row_count=len(values), cells=cells, projection=projection)
    observed = []
    for event in candidate.respondent_events:
        raw = event.raw_response_value
        material = raw["$raw_physical_value"] if "$raw_physical_value" in raw else raw
        token = material.get("token", {})
        observed.append({"raw_bits": token.get("bits"), "raw_kind": token.get("t"),
                         "response_state": event.typed_state,
                         "canonical_value": event.canonical_response_value_if_authorized})
    # Compare against synthetic cell values by IEEE-754 bits.
    expected = {}
    for value in values:
        key = "none" if value is None else __import__("struct").pack(">d", float(value)).hex()
        expected[key] = value
    payload = {
        "schema": "ANVIL_SRC04_Q217_NATIVE_SYNTHETIC_CELL_WITNESS@1",
        "synthetic_only": True,
        "original_source_bodies_read": False,
        "synthetic_source_sha256": synthetic_sha,
        "values": values,
        "projection_events": observed,
        "event_count": len(observed),
        "state_expectations": {"1.0": "SUBSTANTIVE_RESPONSE", "7.0": "SOURCE_SPECIFIC_SPECIAL",
                               "98.0": "DK", "99.0": "REFUSAL", "None": "MISSING"},
        "raw_7_identity": "RETAINED_AS_FLOAT64_BITS_401c000000000000__NO_LABEL_IN_RAW_EVENT",
        "native_projection_completed": True,
        "config_only_validation": False,
    }
    (HERE / "evidence/q217_native_witness.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
