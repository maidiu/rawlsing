#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import platform
import sys
import time
from pathlib import Path

import pyreadstat

from rawlsing_next.pre553_physical_decoder import (
    _jsonable,
    _missing_declarations,
    classify_physical_value,
)
from rawlsing_next.pre553_source_backed_c11_facade import raw_physical_value_witness
from rawlsing_next.fiabc_lm2_r1e_browser_prep import (
    CARRIER_QUESTIONS,
    CARRIER_ROWS,
    CARRIER_SCHEMA,
    SOURCE_SHA256,
    STRUCTURAL_IDENTITY,
    validate_frozen_response_carrier,
)

ROOT = Path.cwd().resolve()
SOURCE = Path("/Users/matthewsmith/Desktop/Rawlsing/data/Data/WVS Wave 7.sav")
EXPECTED_SOURCE_BYTES = 185_163_494
STRUCTURAL = ROOT / "WORKER_RETURNS/FIABC-LM2/wvs7_projection_structural_input.json"
MATERIALIZER = ROOT / "WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py"
OUTPUT_DIR = ROOT / "WORKER_RETURNS/FIABC-LM2-R1F-CARRIER-ARCHAEOLOGY/LOCAL_OUTPUT"
OUTPUT = OUTPUT_DIR / "FIABC_LM2_R1E_FROZEN_Q291_PHYSICAL_CELL_CARRIER.json"
RECEIPT = OUTPUT_DIR / "FIABC_LM2_R1F_Q291_EXTRACTION_RECEIPT.json"
TMP = OUTPUT.with_suffix(OUTPUT.suffix + ".tmp")
RECEIPT_TMP = RECEIPT.with_suffix(RECEIPT.suffix + ".tmp")

PINNED_GIT_BLOBS = {
    "rawlsing_next/pre553_physical_decoder.py": "86109c4a0b7ebd9b66e3b531b6334bfb48f03f78",
    "rawlsing_next/pre553_source_backed_c11_facade.py": "8a761119e4a8d68eb291fc4edfadb52e027f8284",
    "rawlsing_next/pre553_r5_codec.py": "72f8f3c03ed065e86fea4e76bb17f8e06c2bf540",
    "rawlsing_next/fiabc_lm2_r1e_browser_prep.py": "165f3259618dfd58526c463f65499a54ff26c29c",
    "WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py": "d1dfe705fa4da56036bd472af18536da1f69d4ad",
    "WORKER_RETURNS/FIABC-LM2/wvs7_projection_structural_input.json": "f46970acfb9a5d1b98caf953354552122562d255",
}
EXPECTED_ORDINALS = {"Q291G5": 388, "Q291P5": 394}
EXPECTED_PACKED_DECLARATIONS = {
    "Q291G5": [{"hi": {"t": "int", "v": -1}, "kind": {"t": "str", "v": "range"}, "lo": {"t": "int", "v": -5}}],
    "Q291P5": [{"hi": {"t": "int", "v": -1}, "kind": {"t": "str", "v": "range"}, "lo": {"t": "int", "v": -5}}],
}

def fail(message: str) -> None:
    raise SystemExit("FIABC_LM2_R1F_LOCAL_EXTRACTION_STOP__" + message)

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(8 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def git_blob_sha1(path: Path) -> str:
    body = path.read_bytes()
    header = b"blob " + str(len(body)).encode("ascii") + b"\x00"
    return hashlib.sha1(header + body).hexdigest()

def load_materializer():
    spec = importlib.util.spec_from_file_location("fiabc_lm2_r1f_r6s", MATERIALIZER)
    if spec is None or spec.loader is None:
        fail("R6S_MATERIALIZER_IMPORT_UNAVAILABLE")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main() -> int:
    started = time.monotonic()

    if not (ROOT / ".git").exists():
        fail("RUN_FROM_REPOSITORY_ROOT_REQUIRED")
    for rel, expected in PINNED_GIT_BLOBS.items():
        path = ROOT / rel
        if not path.is_file():
            fail("PINNED_REPO_FILE_MISSING__" + rel)
        observed = git_blob_sha1(path)
        if observed != expected:
            fail("PINNED_REPO_BLOB_DRIFT__" + rel)

    if not SOURCE.is_file():
        fail("SOURCE_PATH_MISSING")
    if SOURCE.stat().st_size != EXPECTED_SOURCE_BYTES:
        fail("SOURCE_BYTE_LENGTH_MISMATCH")

    if OUTPUT.exists() or RECEIPT.exists() or TMP.exists() or RECEIPT_TMP.exists():
        fail("OUTPUT_OR_TEMP_ALREADY_EXISTS__NO_OVERWRITE_NO_RETRY")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    hash_started = time.monotonic()
    source_sha = sha256_file(SOURCE)
    hash_seconds = time.monotonic() - hash_started
    if source_sha != SOURCE_SHA256:
        fail("SOURCE_SHA256_MISMATCH")

    structural = json.loads(STRUCTURAL.read_text(encoding="utf-8"))
    if structural.get("source_sha256") != SOURCE_SHA256:
        fail("STRUCTURAL_SOURCE_SHA_DRIFT")
    if structural.get("structural_input_identity") != STRUCTURAL_IDENTITY:
        fail("STRUCTURAL_IDENTITY_DRIFT")
    if structural.get("rows") != CARRIER_ROWS or structural.get("variables") != 613:
        fail("STRUCTURAL_GEOMETRY_DRIFT")
    selected_structural = {
        item["name"]: item
        for item in structural["physical_variables"]
        if item.get("name") in CARRIER_QUESTIONS
    }
    if set(selected_structural) != set(CARRIER_QUESTIONS):
        fail("Q291_STRUCTURAL_VARIABLE_SET_DRIFT")
    for question in CARRIER_QUESTIONS:
        item = selected_structural[question]
        if item.get("ordinal") != EXPECTED_ORDINALS[question]:
            fail("Q291_ORDINAL_DRIFT__" + question)
        if item.get("missing_declarations") != EXPECTED_PACKED_DECLARATIONS[question]:
            fail("Q291_FROZEN_MISSING_DECLARATION_DRIFT__" + question)

    # Exactly one application-level SAV decoder call follows the hash-only pass.
    decoder_started = time.monotonic()
    frame, metadata = pyreadstat.read_sav(
        str(SOURCE),
        usecols=list(CARRIER_QUESTIONS),
        apply_value_formats=False,
        user_missing=True,
    )
    decoder_seconds = time.monotonic() - decoder_started

    if tuple(getattr(metadata, "column_names", ()) or ()) != CARRIER_QUESTIONS:
        fail("DECODER_COLUMN_IDENTITY_OR_ORDER_DRIFT")
    if tuple(str(x) for x in frame.columns) != CARRIER_QUESTIONS:
        fail("FRAME_COLUMN_IDENTITY_OR_ORDER_DRIFT")
    if len(frame) != CARRIER_ROWS:
        fail("DECODER_ROW_COUNT_MISMATCH")
    if int(getattr(metadata, "number_rows", 0) or 0) != CARRIER_ROWS:
        fail("DECODER_METADATA_ROW_COUNT_MISMATCH")

    r6s = load_materializer()
    declarations = {}
    packed_declarations = {}
    for question in CARRIER_QUESTIONS:
        fresh = _missing_declarations(metadata, question, "SAV")
        packed = [r6s._pack_missing_declaration(x) for x in fresh]
        if packed != EXPECTED_PACKED_DECLARATIONS[question]:
            fail("FRESH_MISSING_DECLARATION_MISMATCH__" + question)
        declarations[question] = fresh
        packed_declarations[question] = packed

    rows = []
    serialization_started = time.monotonic()
    for row_ordinal, values in enumerate(frame.itertuples(index=False, name=None), 1):
        row = {"row_ordinal": row_ordinal}
        for question, observed in zip(CARRIER_QUESTIONS, values):
            raw = _jsonable(observed)
            state, declaration = classify_physical_value(raw, declarations[question])
            packed_declaration = None if declaration is None else r6s._pack_missing_declaration(declaration)
            row[question] = {
                "variable_ordinal": EXPECTED_ORDINALS[question],
                "variable_name": question,
                "raw_physical_value_witness": raw_physical_value_witness(raw),
                "physical_missing_state": state.value,
                "source_missing_declaration": packed_declaration,
            }
        rows.append(row)

    if len(rows) != CARRIER_ROWS or rows[0]["row_ordinal"] != 1 or rows[-1]["row_ordinal"] != CARRIER_ROWS:
        fail("ORDERED_ROW_ASSEMBLY_MISMATCH")

    carrier = {
        "schema": CARRIER_SCHEMA,
        "source_sha256": SOURCE_SHA256,
        "structural_preimage_identity": STRUCTURAL_IDENTITY,
        "row_count": CARRIER_ROWS,
        "question_names": list(CARRIER_QUESTIONS),
        "candidate_neutral": True,
        "contains_candidate_output": False,
        "rows": rows,
    }
    payload = (
        json.dumps(
            carrier,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("ascii")
    TMP.write_bytes(payload)
    serialization_seconds = time.monotonic() - serialization_started

    validation_started = time.monotonic()
    validate_frozen_response_carrier(TMP)
    carrier_sha = sha256_file(TMP)
    carrier_bytes = TMP.stat().st_size
    validation_seconds = time.monotonic() - validation_started

    if OUTPUT.exists():
        fail("OUTPUT_APPEARED_DURING_EXECUTION__NO_OVERWRITE")
    os.rename(TMP, OUTPUT)

    total_seconds = time.monotonic() - started
    receipt = {
        "schema": "FIABC_LM2_R1F_Q291_EXTRACTION_RECEIPT@1.0.0",
        "status": "PASS__EXACT_FROZEN_Q291_CARRIER_PERSISTED__STOP",
        "source_path": str(SOURCE),
        "source_sha256": source_sha,
        "source_bytes": EXPECTED_SOURCE_BYTES,
        "decoder": "pyreadstat.read_sav",
        "decoder_call_count": 1,
        "decoder_usecols": list(CARRIER_QUESTIONS),
        "apply_value_formats": False,
        "user_missing": True,
        "encoding_override": None,
        "observed_rows": CARRIER_ROWS,
        "physical_cell_count": CARRIER_ROWS * len(CARRIER_QUESTIONS),
        "question_ordinals": EXPECTED_ORDINALS,
        "fresh_missing_declarations": packed_declarations,
        "carrier_path": str(OUTPUT.relative_to(ROOT)),
        "carrier_sha256": carrier_sha,
        "carrier_bytes": carrier_bytes,
        "carrier_schema": CARRIER_SCHEMA,
        "candidate_neutral": True,
        "contains_candidate_output": False,
        "pyreadstat_version": getattr(pyreadstat, "__version__", None),
        "python_version": sys.version,
        "platform": platform.platform(),
        "hash_seconds": hash_seconds,
        "decoder_seconds": decoder_seconds,
        "serialization_seconds": serialization_seconds,
        "validation_seconds": validation_seconds,
        "total_seconds": total_seconds,
        "repo_blob_pins": PINNED_GIT_BLOBS,
        "downstream_work_executed": False,
        "stop_after_persistence": True,
        "terminal": "LOCAL_Q291_EXTRACTION_PASS__EXACT_FROZEN_CARRIER_PERSISTED__STOP_BEFORE_COMMON_C11",
    }
    RECEIPT_TMP.write_text(
        json.dumps(receipt, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False) + "\n",
        encoding="ascii",
    )
    if RECEIPT.exists():
        fail("RECEIPT_APPEARED_DURING_EXECUTION__NO_OVERWRITE")
    os.rename(RECEIPT_TMP, RECEIPT)

    print(receipt["terminal"])
    print(json.dumps({
        "carrier_path": receipt["carrier_path"],
        "carrier_sha256": receipt["carrier_sha256"],
        "carrier_bytes": receipt["carrier_bytes"],
        "observed_rows": receipt["observed_rows"],
        "physical_cell_count": receipt["physical_cell_count"],
    }, sort_keys=True, separators=(",", ":")))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

