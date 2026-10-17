"""Source-free common-C11 rematerializer for FIABC-LM2-R1E.

This module cannot manufacture its missing Q291 input.  Given a separately
accepted frozen Q291 physical-cell carrier, it combines that carrier with the
already-frozen structural preimage and the prepared R6S projection.  It never
opens the WVS7 source artifact.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any, Iterator, Mapping, Sequence

from rawlsing_next.fiabc_lm2_r1e_browser_prep import (
    CARRIER_QUESTIONS,
    CARRIER_ROWS,
    SOURCE_SHA256,
    STRUCTURAL_IDENTITY,
    STRUCTURAL_PATH,
    validate_frozen_response_carrier,
)
from rawlsing_next.pre553_physical_decoder import (
    PhysicalCell,
    PhysicalMissingState,
    PhysicalVariable,
    classify_physical_value,
)
from rawlsing_next.pre553_r5_codec import R5TypedValueCodec
from rawlsing_next.pre553_source_backed_c11_facade import (
    ExactPhysicalCellStream,
    PHYSICAL_VALUE_MATERIAL_SCHEMA,
    build_validated_source_backed_c11_release_from_stream,
    raw_physical_value_witness,
)

ROOT = Path(__file__).resolve().parents[1]
MATERIALIZER_PATH = ROOT / "WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py"
CODEC = R5TypedValueCodec()

def _materializer():
    spec = importlib.util.spec_from_file_location("fiabc_lm2_r1e_r6s_common", MATERIALIZER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("R6S materializer import spec unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def _read_json(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, Mapping):
        raise RuntimeError(f"{path} must contain a JSON object")
    return value

def _structural_material(module) -> tuple[Mapping[str, Any], tuple[PhysicalVariable, ...], tuple[Any, ...]]:
    doc = _read_json(STRUCTURAL_PATH)
    if doc.get("structural_input_identity") != STRUCTURAL_IDENTITY:
        raise RuntimeError("structural input exact identity drift")
    unsigned = {k: v for k, v in doc.items() if k != "structural_input_identity"}
    if module.semantic_hash(unsigned) != STRUCTURAL_IDENTITY:
        raise RuntimeError("structural input content hash drift")
    variables = tuple(
        PhysicalVariable(
            int(v["ordinal"]),
            str(v["name"]),
            None,
            None,
            {},
            tuple(module._unpack_missing_declaration(x) for x in v["missing_declarations"]),
            {},
            {},
        )
        for v in doc["physical_variables"]
    )
    country = tuple(module._unpack_exact_scalar(x) for x in doc["b_country_values"])
    if len(country) != CARRIER_ROWS:
        raise RuntimeError("structural B_COUNTRY row count drift")
    return doc, variables, country

def _variable_by_name(variables: Sequence[PhysicalVariable], name: str) -> PhysicalVariable:
    matches = [v for v in variables if v.name == name]
    if len(matches) != 1:
        raise RuntimeError(f"exact physical variable {name} not unique")
    return matches[0]

def _decode_witness(value: Any) -> Any:
    if not isinstance(value, Mapping) or set(value) != {"$raw_physical_value"}:
        raise RuntimeError("carrier raw witness wrapper mismatch")
    material = value["$raw_physical_value"]
    if not isinstance(material, Mapping):
        raise RuntimeError("carrier raw witness material must be mapping")
    if material.get("schema") != PHYSICAL_VALUE_MATERIAL_SCHEMA:
        raise RuntimeError("carrier physical witness schema mismatch")
    token = material.get("token")
    if not isinstance(token, Mapping):
        raise RuntimeError("carrier physical witness token missing")
    decoded = CODEC.decode(token)
    if raw_physical_value_witness(decoded) != value:
        raise RuntimeError("carrier physical witness is not canonical/reversible")
    return decoded

def _cells(
    carrier: Mapping[str, Any],
    variables: Sequence[PhysicalVariable],
    country: Sequence[Any],
    module: Any,
) -> Iterator[PhysicalCell]:
    qvars = {q: _variable_by_name(variables, q) for q in CARRIER_QUESTIONS}
    cvar = _variable_by_name(variables, "B_COUNTRY")
    rows = carrier["rows"]
    for row_ordinal, row in enumerate(rows, 1):
        for question in CARRIER_QUESTIONS:
            variable = qvars[question]
            cell = row[question]
            raw = _decode_witness(cell["raw_physical_value_witness"])
            state, declaration = classify_physical_value(raw, variable.missing_declarations)
            if cell.get("physical_missing_state") != state.value:
                raise RuntimeError(f"{question} physical missing-state drift at row {row_ordinal}")
            expected_declaration = (
                None if declaration is None else module._pack_missing_declaration(declaration)
            )
            if cell.get("source_missing_declaration") != expected_declaration:
                raise RuntimeError(f"{question} source missing-declaration drift at row {row_ordinal}")
            yield PhysicalCell(
                row_ordinal,
                variable.ordinal,
                variable.name,
                raw,
                state,
                declaration,
            )
        raw_country = country[row_ordinal - 1]
        state, declaration = classify_physical_value(raw_country, cvar.missing_declarations)
        yield PhysicalCell(
            row_ordinal,
            cvar.ordinal,
            cvar.name,
            raw_country,
            state,
            declaration,
        )

def build_common_c11_release(carrier_path: Path):
    validate_frozen_response_carrier(carrier_path)
    carrier = _read_json(carrier_path)
    module = _materializer()
    structural_doc, variables, country = _structural_material(module)
    projection = module.materialize_from_structural_input(structural_doc)
    stream = ExactPhysicalCellStream(
        SOURCE_SHA256,
        CARRIER_ROWS,
        lambda: _cells(carrier, variables, country, module),
    )
    release = build_validated_source_backed_c11_release_from_stream(stream, projection)
    return release, projection

def common_c11_receipt(carrier_path: Path) -> Mapping[str, Any]:
    release, projection = build_common_c11_release(carrier_path)
    candidate_markers = ("CANDIDATE_A", "CANDIDATE_B", "CANDIDATE_C")
    serialized_refs = json.dumps(
        [obj.ref.as_dict() for obj in release.public_objects],
        sort_keys=True,
        separators=(",", ":"),
    )
    if any(marker in serialized_refs for marker in candidate_markers):
        raise RuntimeError("candidate-owned output leaked into common C11")
    return {
        "schema": "FIABC_LM2_R1E_COMMON_C11_RECEIPT@1.0.0",
        "source_sha256": SOURCE_SHA256,
        "structural_preimage_identity": STRUCTURAL_IDENTITY,
        "projection_identity_ref": projection.projection_identity_ref.as_dict(),
        "projection_authority_ref": projection.projection_authority_ref.as_dict(),
        "release_ref": release.release_ref.as_dict(),
        "source_release_manifest_hash": release.source_release_manifest_hash,
        "semantic_release_hash": release.semantic_release_hash,
        "replay_manifest_ref": release.replay_manifest.ref.as_dict(),
        "public_object_count": len(release.public_objects),
        "internal_record_count": len(release.internal_records),
        "candidate_neutral": True,
        "candidate_outputs_exposed": 0,
    }

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--carrier", required=True)
    parser.add_argument("--receipt", required=True)
    args = parser.parse_args(argv)
    receipt = common_c11_receipt(Path(args.carrier))
    out = Path(args.receipt)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n")
    print("FIABC_LM2_R1E_COMMON_C11_PASS__CANDIDATE_NEUTRAL__ZERO_CANDIDATE_OUTPUT")
    print(json.dumps(receipt, sort_keys=True, separators=(",", ":")))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
