#!/usr/bin/env python3
"""Candidate-neutral LiTS physical-representation diagnostic.

This script does not authorize semantics and does not repair the projection.
It records the exact decoder-observed R5 typed physical tokens for the two
governed LiTS response slots and compares them with the current governed
ResponseValueRule physical keys.

Forbidden uses: labels/frequencies as semantic authority, candidate output,
oracle construction, T3 freeze, measured P2X, or generic numeric coercion.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import types

from rawlsing_next.pre553_physical_decoder import decode_dta
from rawlsing_next.pre553_r5_codec import R5TypedValueCodec, canonical_bytes
from rawlsing_next.pre553_source_backed_c11_facade import physical_value_binding_key
import rawlsing_next.ee_p2x_darwin_stage_backend as backend


SOURCE_SHA256 = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
EXPECTED_ROWS = 29002
EXPECTED_VARIABLES = 1198
TARGET_SLOTS = {
    "q301_2": 194,
    "q301_7": 199,
}
CURRENT_FACADE_BLOB = "8a761119e4a8d68eb291fc4edfadb52e027f8284"
ACCEPTED_ROUTE_B_OWNER_BLOB = "7c509c2098d0030f253344eb3f682471378812a8"
ACCEPTED_ROUTE_B_STAGE = "WORKER_RETURNS/EE-P2X/03_LITS_I_B_CACHELESS_C11_STAGE.json"
BANKED_PROJECTION_BUILDER_BLOB = "c51b56779ab9d79126619b7733d41f5253c8150f"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def stable_json(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def class_key(doc: dict) -> str:
    return hashlib.sha256(stable_json(doc).encode("utf-8")).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, type=Path)
    ap.add_argument("--repo-root", required=True, type=Path)
    ap.add_argument("--work-root", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()

    source = args.source.resolve()
    repo = args.repo_root.resolve()
    work = args.work_root.resolve()
    output = args.output.resolve()

    if not source.is_file():
        raise SystemExit(f"LiTS source missing: {source}")
    got = sha256_file(source)
    if got != SOURCE_SHA256:
        raise SystemExit(f"LiTS SHA mismatch: {got}")
    if "cells" in output.parts:
        raise SystemExit("diagnostic output may not be written under candidate-owned cells/")

    incidence = decode_dta(source, encoding="latin1")
    if incidence.source_sha256 != SOURCE_SHA256:
        raise SystemExit("decoder source identity drift")
    if incidence.row_count != EXPECTED_ROWS or len(incidence.variables) != EXPECTED_VARIABLES:
        raise SystemExit("decoder source shape drift")

    ctx = types.SimpleNamespace(work_root=work / "court" / "representation_diagnostic")
    services = types.SimpleNamespace(repo_root=repo)
    projection, _projection_context, banked = backend._lits_projection(ctx, services, {}, incidence)

    response_slots = {slot.slot.name: slot for slot in projection.response_slots}
    if {name: response_slots[name].slot.ordinal for name in TARGET_SLOTS} != TARGET_SLOTS:
        raise SystemExit("governed LiTS response-slot identity drift")

    current_rules = {}
    for name in TARGET_SLOTS:
        slot = response_slots[name]
        current_rules[name] = [
            {
                "physical_key": rule.physical_key,
                "response_state": rule.response_state,
            }
            for rule in slot.values
        ]

    codec = R5TypedValueCodec()
    classes: dict[str, dict] = {}
    total = 0
    matched = 0
    banked_exact_matched = 0

    rule_maps = {
        name: {rule.physical_key: rule.response_state for rule in response_slots[name].values}
        for name in TARGET_SLOTS
    }

    for cell in incidence.iter_cells(batch_size=20_000):
        if TARGET_SLOTS.get(cell.variable_name) != cell.variable_ordinal:
            continue
        total += 1
        current_key = physical_value_binding_key(
            cell.raw_value, cell.missing_state, cell.source_missing_declaration
        )
        rule_state = rule_maps[cell.variable_name].get(current_key)
        if rule_state is not None:
            matched += 1

        replayed = banked.exact_cell(cell)
        replayed_key = physical_value_binding_key(
            replayed.raw_value,
            replayed.missing_state,
            replayed.source_missing_declaration,
        )
        replayed_rule_state = rule_maps[cell.variable_name].get(replayed_key)
        if replayed_rule_state is not None:
            banked_exact_matched += 1

        material = {
            "variable_name": cell.variable_name,
            "variable_ordinal": cell.variable_ordinal,
            "physical_state": cell.missing_state.value,
            "raw_python_type": type(cell.raw_value).__name__,
            "raw_r5_token": codec.encode(cell.raw_value),
            "source_missing_declaration_r5_token": codec.encode(cell.source_missing_declaration),
            "current_physical_key": current_key,
            "current_rule_match": rule_state is not None,
            "current_rule_state_if_matched": rule_state,
            "banked_exact_python_type": type(replayed.raw_value).__name__,
            "banked_exact_r5_token": codec.encode(replayed.raw_value),
            "banked_exact_physical_key": replayed_key,
            "banked_exact_rule_match": replayed_rule_state is not None,
            "banked_exact_rule_state_if_matched": replayed_rule_state,
        }
        key = class_key(material)
        row = classes.get(key)
        if row is None:
            classes[key] = {
                "class_identity": key,
                "count": 1,
                "first_row_ordinal": cell.row_ordinal,
                **material,
            }
        else:
            row["count"] += 1

    expected_cells = EXPECTED_ROWS * len(TARGET_SLOTS)
    if total != expected_cells:
        raise SystemExit(f"diagnostic response-cell count drift: {total} != {expected_cells}")

    class_rows = sorted(
        classes.values(),
        key=lambda x: (
            x["variable_ordinal"],
            x["physical_state"],
            stable_json(x["raw_r5_token"]),
            stable_json(x["source_missing_declaration_r5_token"]),
        ),
    )

    doc = {
        "schema": "FIABC_LITS_I_DECODER_REPRESENTATION_DIAGNOSTIC@1.0.0",
        "status": "REPRESENTATION_FACTS_ONLY__NO_AUTHORITY_MINTED",
        "source": {
            "sha256": SOURCE_SHA256,
            "rows": incidence.row_count,
            "variables": len(incidence.variables),
            "format": incidence.source_format,
        },
        "runtime": {
            "python": __import__("platform").python_version(),
            "pyreadstat": importlib.metadata.version("pyreadstat"),
            "decoder": 'decode_dta(source, encoding="latin1")',
            "reader_configuration": dict(incidence.reader_configuration),
        },
        "authority_context": {
            "current_facade_blob": CURRENT_FACADE_BLOB,
            "accepted_route_b_owner_blob": ACCEPTED_ROUTE_B_OWNER_BLOB,
            "accepted_route_b_stage": ACCEPTED_ROUTE_B_STAGE,
            "banked_projection_builder_blob": BANKED_PROJECTION_BUILDER_BLOB,
            "projection_identity": projection.cache_identity,
        },
        "target_slots": TARGET_SLOTS,
        "governed_current_response_rules": current_rules,
        "physical_representation_classes": class_rows,
        "summary": {
            "response_cells": total,
            "unique_representation_classes": len(class_rows),
            "current_rule_matched_cells": matched,
            "current_rule_unmatched_cells": total - matched,
            "banked_exact_rule_matched_cells": banked_exact_matched,
            "banked_exact_rule_unmatched_cells": total - banked_exact_matched,
        },
        "negative_limits": [
            "NO_LABEL_SEMANTIC_INFERENCE",
            "NO_FREQUENCY_SEMANTIC_INFERENCE",
            "NO_MISSINGNESS_SEMANTIC_INFERENCE",
            "NO_GENERIC_NUMERIC_COERCION_AUTHORITY",
            "NO_CANDIDATE_OUTPUT",
            "NO_ORACLE_CONSTRUCTION",
            "NO_T3_FREEZE",
            "NO_MEASURED_P2X",
        ],
    }
    payload = (json.dumps(doc, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(payload)
    print(
        "FIABC_LITS_REPRESENTATION_DIAGNOSTIC_WRITTEN",
        hashlib.sha256(payload).hexdigest(),
        output,
    )
    print("FIABC_LITS_REPRESENTATION_SUMMARY", stable_json(doc["summary"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
