"""Mechanical browser-prepared preflight/identity CLI for FIABC-LM2-R1E.

No command in this module opens WVS7 source bytes.  The C11 preflight accepts
only a separately frozen exact Q291 physical-cell carrier whose production is
not authorized by this worker.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any, Mapping

from rawlsing_next.fiabc_lm2_r1e_wvs7_mapping_authority import (
    authority_parent_and_scope_ledger,
)

ROOT = Path(__file__).resolve().parents[1]
STRUCTURAL_PATH = ROOT / "WORKER_RETURNS/FIABC-LM2/wvs7_projection_structural_input.json"
PARENTAGE_PATH = ROOT / "WORKER_RETURNS/FIABC-LM2/02_WVS7_STRUCTURAL_PARENTAGE_RECEIPT.json"
PHYSICAL_PATH = ROOT / "WORKER_RETURNS/FIABC-LM2/04_WVS7_CANONICAL_PHYSICAL_EXPECTATION.json"
MATERIALIZER_PATH = ROOT / "WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py"

SOURCE_SHA256 = "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d"
STRUCTURAL_IDENTITY = "151907b3163959d0eb5ebb020fa5253d33447362420e465600035744112fe5bc"
PARENTAGE_IDENTITY = "5037c55bf1a017112c0fe5f18ca5905696d66dfefcc4d8f47dcb0e7fcb13f37c"
PHYSICAL_EXPECTATION_IDENTITY = "9845c24da0c03adb4dfd65118b7c8c39a60a30337f33cc4177ffc6c848d02390"
CARRIER_SCHEMA = "FIABC_LM2_R1E_FROZEN_Q291_PHYSICAL_CELL_CARRIER@1.0.0"
CARRIER_ROWS = 97220
CARRIER_QUESTIONS = ("Q291G5", "Q291P5")
BLOCKED_TERMINAL = "BLOCKED__NO_ACCEPTED_FROZEN_Q291_RESPONSE_CARRIER__RAW_SOURCE_REREAD_FORBIDDEN"

def _materializer():
    spec = importlib.util.spec_from_file_location("fiabc_lm2_r1e_r6s", MATERIALIZER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("R6S materializer import spec unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def _json(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, Mapping):
        raise RuntimeError(f"{path} must contain a JSON object")
    return value

def assert_frozen_repo_inputs() -> Mapping[str, Any]:
    if not STRUCTURAL_PATH.is_file():
        raise RuntimeError("frozen structural input file absent")
    parentage = _json(PARENTAGE_PATH)
    physical = _json(PHYSICAL_PATH)
    if parentage.get("bundle_identity") != PARENTAGE_IDENTITY:
        raise RuntimeError("parentage bundle identity drift")
    derivative = parentage.get("derivative_receipt", {}).get("derivative", {})
    if derivative.get("identity") != STRUCTURAL_IDENTITY:
        raise RuntimeError("structural preimage identity drift")
    if physical.get("expectation_identity") != PHYSICAL_EXPECTATION_IDENTITY:
        raise RuntimeError("physical expectation identity drift")
    return {
        "source_sha256": SOURCE_SHA256,
        "structural_preimage": STRUCTURAL_IDENTITY,
        "parentage_bundle": PARENTAGE_IDENTITY,
        "physical_expectation": PHYSICAL_EXPECTATION_IDENTITY,
        "structural_path": str(STRUCTURAL_PATH.relative_to(ROOT)),
    }

def emit_identities() -> Mapping[str, Any]:
    module = _materializer()
    return {
        "schema": "FIABC_LM2_R1E_BROWSER_PREP_IDENTITY_RECEIPT@1.0.0",
        "frozen": assert_frozen_repo_inputs(),
        "mapping": authority_parent_and_scope_ledger(),
        "r6s": module.authority_identity_receipt(),
    }

def validate_frozen_response_carrier(path: Path) -> Mapping[str, Any]:
    if not path.is_file():
        raise RuntimeError(BLOCKED_TERMINAL)
    doc = _json(path)
    required = {
        "schema": CARRIER_SCHEMA,
        "source_sha256": SOURCE_SHA256,
        "structural_preimage_identity": STRUCTURAL_IDENTITY,
        "row_count": CARRIER_ROWS,
        "question_names": list(CARRIER_QUESTIONS),
        "candidate_neutral": True,
        "contains_candidate_output": False,
    }
    for key, expected in required.items():
        if doc.get(key) != expected:
            raise RuntimeError(f"frozen response carrier mismatch: {key}")
    rows = doc.get("rows")
    if not isinstance(rows, list) or len(rows) != CARRIER_ROWS:
        raise RuntimeError("frozen response carrier must contain exactly 97220 ordered rows")
    for index, row in enumerate(rows, 1):
        if not isinstance(row, Mapping) or row.get("row_ordinal") != index:
            raise RuntimeError("frozen response carrier row ordinal/order drift")
        for question in CARRIER_QUESTIONS:
            cell = row.get(question)
            if not isinstance(cell, Mapping):
                raise RuntimeError(f"frozen response carrier missing exact {question} cell")
            if "raw_physical_value_witness" not in cell or "physical_missing_state" not in cell:
                raise RuntimeError(f"frozen response carrier {question} lacks exact physical witness/state")
    return {
        "status": "PASS__ACCEPTED_FROZEN_RESPONSE_CARRIER_PRESENT",
        "path": str(path),
        "rows": CARRIER_ROWS,
        "questions": list(CARRIER_QUESTIONS),
    }

def preflight_c11(carrier: str | None) -> Mapping[str, Any]:
    receipt = {"frozen": assert_frozen_repo_inputs()}
    if not carrier:
        raise RuntimeError(BLOCKED_TERMINAL)
    receipt["carrier"] = validate_frozen_response_carrier(Path(carrier))
    return receipt

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("emit-identities")
    p = sub.add_parser("preflight-c11")
    p.add_argument("--carrier")
    args = parser.parse_args(argv)
    try:
        if args.command == "emit-identities":
            print(json.dumps(emit_identities(), sort_keys=True, separators=(",", ":")))
            return 0
        if args.command == "preflight-c11":
            print(json.dumps(preflight_c11(args.carrier), sort_keys=True, separators=(",", ":")))
            return 0
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        if str(exc) == BLOCKED_TERMINAL:
            return 42
        return 2
    return 2

if __name__ == "__main__":
    raise SystemExit(main())
