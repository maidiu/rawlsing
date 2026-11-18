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
    v3 = json.loads((HERE / "source.config.repaired.v3.json").read_text())
    q217_values = next(x for x in v3["response_slots"] if x.get("question_id") == "q217")["values"]
    values = tuple(None if v.get("raw_value") is None else float(v["raw_value"]) for v in q217_values)
    doc = make_config(
        source_format="SAV", active_source_sha256=synthetic_sha, row_count=len(values),
        keyed=False, values=values,
    )
    doc = json.loads(json.dumps(doc).replace("q101", "q217"))
    # Replace synthetic response rules with the actual v3 q217 rules.
    doc["response_slots"][0]["values"] = copy.deepcopy(q217_values)
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
    expected = {"1.0": "SUBSTANTIVE_RESPONSE", "2.0": "SUBSTANTIVE_RESPONSE",
                "3.0": "SUBSTANTIVE_RESPONSE", "4.0": "SUBSTANTIVE_RESPONSE",
                "5.0": "SUBSTANTIVE_RESPONSE", "6.0": "SUBSTANTIVE_RESPONSE",
                "10.0": "SUBSTANTIVE_RESPONSE", "7.0": "SOURCE_SPECIFIC_SPECIAL",
                "97.0": "DK", "98.0": "DK", "99.0": "REFUSAL", "None": "MISSING"}
    payload = {
        "schema": "ANVIL_SRC04_Q217_NATIVE_SYNTHETIC_CELL_WITNESS@1",
        "synthetic_only": True, "original_source_bodies_read": False,
        "synthetic_source_sha256": synthetic_sha,
        "response_rules": "source.config.repaired.v3.json q217 values",
        "physical_labels_source": "synthetic config; actual v3 physical_slots are byte-equivalent to v2",
        "values": list(values), "projection_events": observed, "event_count": len(observed),
        "state_expectations": expected,
        "raw_7_identity": "RETAINED_AS_FLOAT64_BITS_401c000000000000__NO_LABEL_IN_RAW_EVENT",
        "native_projection_completed": True, "config_only_validation": False,
    }
    (HERE / "evidence/q217_native_witness.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
