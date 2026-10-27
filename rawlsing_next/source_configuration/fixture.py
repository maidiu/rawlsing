"""Clearly nonrespondent fixture transport for R157 validation.

A fixture is not an original source package.  Its byte identity is the canonical
hash of the fixture document, and the document must declare the separate original
source identity it is exercising.  No original respondent rows are represented.
"""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_physical_decoder import (
    PhysicalCell,
    PhysicalMissingState,
)
from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream

from .errors import SourceConfigurationEvidenceError

FIXTURE_SCHEMA_ID = "PYAT_R157_NONRESPONDENT_FIXTURE_CELLS@1.0.0"


def _mapping(value: Any, path: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise SourceConfigurationEvidenceError(f"{path} must be an object")
    return value


def _sequence(value: Any, path: str) -> Sequence[Any]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise SourceConfigurationEvidenceError(f"{path} must be an array")
    return value


def _text(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SourceConfigurationEvidenceError(f"{path} must be a non-empty string")
    return value


def _integer(value: Any, path: str, *, minimum: int = 1) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise SourceConfigurationEvidenceError(f"{path} must be an integer >= {minimum}")
    return value


def _fixture_material(document: Mapping[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in document.items() if key != "fixture_source_sha256"}


def fixture_document_sha256(document: Mapping[str, Any]) -> str:
    """Deterministic SHA-256 of the fixture document excluding its own hash field.

    Fixture cells may carry exact numeric source values (including decimals).
    This is a byte-binding identity for the fixture input, not a semantic object
    identity; the native physical-value codec remains authoritative for values.
    """
    material = json.dumps(
        _fixture_material(document), sort_keys=True, separators=(",", ":"),
        ensure_ascii=False, allow_nan=False,
    )
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def _validate_cell(cell: Any, path: str) -> PhysicalCell:
    payload = _mapping(cell, path)
    expected = {
        "row_ordinal", "variable_ordinal", "variable_name", "raw_value",
        "missing_state", "source_missing_declaration",
    }
    missing = sorted(expected - set(payload))
    extra = sorted(set(payload) - expected - {"raw_value_label"})
    if missing:
        raise SourceConfigurationEvidenceError(f"{path} missing keys {missing!r}")
    if extra:
        raise SourceConfigurationEvidenceError(f"{path} unknown keys {extra!r}")
    state = _text(payload["missing_state"], f"{path}.missing_state")
    if state not in {x.value for x in PhysicalMissingState}:
        raise SourceConfigurationEvidenceError(f"{path}.missing_state is not a PhysicalMissingState")
    declaration = payload["source_missing_declaration"]
    if declaration is not None:
        _mapping(declaration, f"{path}.source_missing_declaration")
    return PhysicalCell(
        row_ordinal=_integer(payload["row_ordinal"], f"{path}.row_ordinal"),
        variable_ordinal=_integer(payload["variable_ordinal"], f"{path}.variable_ordinal"),
        variable_name=_text(payload["variable_name"], f"{path}.variable_name"),
        raw_value=payload["raw_value"],
        missing_state=PhysicalMissingState(state),
        source_missing_declaration=declaration,
        raw_value_label=payload.get("raw_value_label"),
    )


def fixture_stream_from_document(document: Mapping[str, Any]) -> ExactPhysicalCellStream:
    """Validate a nonrespondent fixture and return the exact physical stream."""
    document = _mapping(document, "fixture")
    if document.get("schema") != FIXTURE_SCHEMA_ID:
        raise SourceConfigurationEvidenceError(
            f"fixture.schema must be {FIXTURE_SCHEMA_ID!r}")
    if document.get("identity_class") != "NONRESPONDENT_FIXTURE":
        raise SourceConfigurationEvidenceError(
            "fixture.identity_class must be NONRESPONDENT_FIXTURE")
    if document.get("nonrespondent") is not True:
        raise SourceConfigurationEvidenceError("fixture.nonrespondent must be true")
    _text(document.get("fixture_id"), "fixture.fixture_id")
    row_count = _integer(document.get("row_count"), "fixture.row_count")
    cells = tuple(_validate_cell(cell, f"fixture.cells[{index}]")
                  for index, cell in enumerate(_sequence(document.get("cells"), "fixture.cells")))
    if not cells:
        raise SourceConfigurationEvidenceError("fixture.cells must not be empty")
    rows = {cell.row_ordinal for cell in cells}
    if rows != set(range(1, row_count + 1)):
        raise SourceConfigurationEvidenceError(
            "fixture row ordinals must be exactly 1..row_count")
    seen: set[tuple[int, int, str]] = set()
    slot_names: dict[int, str] = {}
    for cell in cells:
        key = (cell.row_ordinal, cell.variable_ordinal, cell.variable_name)
        if key in seen:
            raise SourceConfigurationEvidenceError("duplicate fixture physical cell")
        seen.add(key)
        previous = slot_names.get(cell.variable_ordinal)
        if previous is not None and previous != cell.variable_name:
            raise SourceConfigurationEvidenceError(
                "fixture variable ordinal is reused with a different name")
        slot_names[cell.variable_ordinal] = cell.variable_name
    expected_sha = _text(document.get("fixture_source_sha256"), "fixture.fixture_source_sha256")
    actual_sha = fixture_document_sha256(document)
    if expected_sha != actual_sha:
        raise SourceConfigurationEvidenceError(
            "fixture_source_sha256 does not bind the canonical fixture document")
    return ExactPhysicalCellStream(
        source_sha256=expected_sha,
        row_count=row_count,
        cell_iter_factory=lambda: cells,
        transport_identity="R157_NONRESPONDENT_FIXTURE_EXACT_CELLS@1.0.0",
    )


def load_fixture_stream(path: str | Path) -> ExactPhysicalCellStream:
    path = Path(path)
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SourceConfigurationEvidenceError(f"cannot read fixture {path}: {exc}") from exc
    return fixture_stream_from_document(document)


__all__ = [
    "FIXTURE_SCHEMA_ID", "fixture_document_sha256", "fixture_stream_from_document",
    "load_fixture_stream",
]
