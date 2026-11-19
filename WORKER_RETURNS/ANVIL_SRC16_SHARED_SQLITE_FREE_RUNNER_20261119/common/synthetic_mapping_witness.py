#!/usr/bin/env python3
"""Synthetic yes/no witnesses for the mapped-slot precheck.

No source is opened.  The pinned SRC16 config is inspected as metadata, and
synthetic PhysicalCells exercise only the exact decision function used by the
controller census.  This proves that a known top-code is bound, typed missing
values are bound, and an arbitrary unconfigured numeric code is not silently
accepted.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from rawlsing_next.pre553_physical_decoder import PhysicalCell, PhysicalMissingState
from rawlsing_next.pre553_r157_projection_adapter import load_source_config
from mapped_slot_precheck import aggregate_mapped_slots

CONFIG_FILE_SHA256 = "1106de3e086032f5ac0b26fee0b56a147722399c80ac2841b70f0b851dea93b7"
CAND = Path(os.environ["ANVIL_CANDIDATE_TREE"])
CFG = Path(os.environ.get(
    "ANVIL_SRC16_CONFIG",
    CAND / "rawlsing_next/source_configuration/data/SRC16/SRC16.source.config.json",
)).absolute()


def cell(row: int, raw, state=PhysicalMissingState.OBSERVED_STORAGE_VALUE) -> PhysicalCell:
    return PhysicalCell(row, 11, "age", raw, state, None)


def main() -> int:
    if hashlib.sha256(CFG.read_bytes()).hexdigest() != CONFIG_FILE_SHA256:
        raise SystemExit("PINNED_CONFIG_MISMATCH")
    config = load_source_config(CFG)
    age = next(
        section for section in config.document["response_slots"]
        if section["slot"] == {"ordinal": 11, "name": "age"}
    )
    doc = {
        "binding": {"row_count": 1},
        "response_slots": [age],
        "coordinate_slots": [],
        "weight_slots": [],
    }

    def result(cells):
        return aggregate_mapped_slots(doc, cells)

    topcode = result([cell(1, 89.0)])
    refused_missing = result([cell(1, -99.0)])
    refused_dk = result([cell(1, -98.0)])
    system_missing = result([cell(1, None, PhysicalMissingState.SYSTEM_MISSING)])
    substantive = result([cell(1, 18.0)])
    arbitrary = result([cell(1, 3.0)])
    several = result([cell(1, 18.0), cell(2, 30.0)])
    several_doc = dict(doc, binding={"row_count": 2})
    several = aggregate_mapped_slots(several_doc, [cell(1, 18.0), cell(2, 30.0)])

    checks = {
        "topcode_89_bound_yes": topcode["precheck_passed"] is True,
        "typed_missing_minus99_bound_yes": refused_missing["precheck_passed"] is True,
        "typed_missing_minus98_bound_yes": refused_dk["precheck_passed"] is True,
        "system_missing_bound_yes": system_missing["precheck_passed"] is True,
        "unconfigured_age_18_refused_yes": substantive["precheck_passed"] is False,
        "arbitrary_code_3_not_made_valid_yes": arbitrary["precheck_passed"] is False,
        "one_pass_collects_multiple_tokens_yes": (
            len(several["unresolved_slots"]) == 1
            and several["unresolved_slot_count"] == 1
            and several["unresolved_slots"][0]["distinct_unresolved_tokens"] == 2
            and several["unresolved_slots"][0]["unresolved_count"] == 2
        ),
    }
    if not all(checks.values()):
        print(json.dumps({"status": "SYNTHETIC_WITNESS_FAILED", "checks": checks}, sort_keys=True))
        return 2
    print(json.dumps({
        "status": "SYNTHETIC_WITNESS_PASS",
        "config_file_sha256": CONFIG_FILE_SHA256,
        "age_response_configured_values": len(age["values"]),
        "topcode": "89.0",
        "unknown_age_18_token": substantive["unresolved_slots"][0]["tokens"],
        "arbitrary_code_3_token": arbitrary["unresolved_slots"][0]["tokens"],
        "multiple_unresolved_tokens": several["unresolved_slots"][0]["tokens"],
        "respondent_rows_emitted": False,
        "source_read_performed": False,
        "checks": checks,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
