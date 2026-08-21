"""Thin, format-neutral source-byte decoders for the PRE553 substrate.

This module deliberately stops at physical incidence.  It never maps a raw
value to a C11 response state or interprets a label.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import math
from pathlib import Path
from typing import Any, Iterator, Mapping


COMPATIBILITY_ONLY = "COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY"
COMPATIBILITY_ALLOWLIST: Mapping[str, str] = {
    "6058644a9308aad574b95fa0afd1b026fedea289c6c95aca043aefb41ae0ab8a": "latin1",
    "5469e3b39cbbb6d7230ff9894426cc75fe074541d284633235df4af3442ac379": "latin1",
    "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09": "latin1",
    "c43d0e1821c51398817d7dfdfad2c0a4a5bb0d492f6a58096670e623bb6130e9": "latin1",
    "368ae5d07a44975a2f0a9ce3b1e564988a966b2632e28075c56a24d60065bcc8": "latin1",
    "14e1032755c4f42d8d3dc61647097ccd7605ba281551e53953c76d22a223cd1c": "latin1",
}


class PhysicalMissingState(str, Enum):
    OBSERVED_STORAGE_VALUE = "OBSERVED_STORAGE_VALUE"
    SYSTEM_MISSING = "SYSTEM_MISSING"
    FORMAT_USER_MISSING_VALUE = "FORMAT_USER_MISSING_VALUE"
    FORMAT_USER_MISSING_RANGE = "FORMAT_USER_MISSING_RANGE"
    FORMAT_EXTENDED_MISSING = "FORMAT_EXTENDED_MISSING"
    SOURCE_CELL_ABSENT_OR_UNREPRESENTED = "SOURCE_CELL_ABSENT_OR_UNREPRESENTED"
    PHYSICAL_STATE_UNKNOWN = "PHYSICAL_STATE_UNKNOWN"


@dataclass(frozen=True)
class PhysicalVariable:
    ordinal: int
    name: str
    storage_type: str | None
    variable_label: str | None
    value_labels: Mapping[str, Any]
    missing_declarations: tuple[Mapping[str, Any], ...]
    display_metadata: Mapping[str, Any]
    topology_metadata: Mapping[str, Any]


@dataclass(frozen=True)
class PhysicalCell:
    row_ordinal: int
    variable_ordinal: int
    variable_name: str
    raw_value: Any
    missing_state: PhysicalMissingState
    source_missing_declaration: Mapping[str, Any] | None
    raw_value_label: Any = None


@dataclass(frozen=True)
class PhysicalSourceIncidence:
    source_sha256: str
    source_format: str
    row_count: int
    variables: tuple[PhysicalVariable, ...]
    cells: tuple[PhysicalCell, ...]
    reader_configuration: Mapping[str, Any]
    file_metadata: Mapping[str, Any]

    def iter_cells(self) -> Iterator[PhysicalCell]:
        return iter(self.cells)


class DecoderError(ValueError):
    pass


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if math.isnan(value):
            return None
        if math.isinf(value):
            return str(value)
        return value
    if hasattr(value, "item"):
        try:
            return _jsonable(value.item())
        except Exception:
            pass
    if isinstance(value, Mapping):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    return str(value)


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _compatibility_config(source_sha: str, encoding: str | None) -> dict[str, Any]:
    if encoding in ("auto", "guess", "fallback"):
        raise DecoderError("automatic encoding guessing/fallback is forbidden")
    if encoding is None:
        return {"encoding": None, "authority_status": None}
    expected = COMPATIBILITY_ALLOWLIST.get(source_sha)
    if expected != encoding:
        raise DecoderError("encoding override is not in the frozen exact SHA/config allowlist")
    return {"encoding": encoding, "authority_status": COMPATIBILITY_ONLY}


def _missing_declarations(metadata: Any, name: str) -> tuple[Mapping[str, Any], ...]:
    ranges = getattr(metadata, "missing_ranges", {}) or {}
    user = getattr(metadata, "missing_user_values", {}) or {}
    result: list[Mapping[str, Any]] = []
    for item in ranges.get(name, ()):
        if isinstance(item, Mapping) and item.get("lo") == item.get("hi"):
            result.append({"kind": "discrete", "value": _jsonable(item.get("lo"))})
        else:
            result.append({"kind": "range", "lo": _jsonable(item.get("lo")), "hi": _jsonable(item.get("hi"))})
    for value in user.get(name, ()):
        result.append({"kind": "discrete", "value": _jsonable(value)})
    return tuple(result)


def _classify(value: Any, declarations: tuple[Mapping[str, Any], ...]) -> tuple[PhysicalMissingState, Mapping[str, Any] | None]:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return PhysicalMissingState.SYSTEM_MISSING, None
    for declaration in declarations:
        if declaration["kind"] == "discrete" and value == declaration.get("value"):
            return PhysicalMissingState.FORMAT_USER_MISSING_VALUE, declaration
        if declaration["kind"] == "range" and declaration.get("lo") <= value <= declaration.get("hi"):
            return PhysicalMissingState.FORMAT_USER_MISSING_RANGE, declaration
    return PhysicalMissingState.OBSERVED_STORAGE_VALUE, None


def _decode(path: str | Path, *, expected_format: str, encoding: str | None = None) -> PhysicalSourceIncidence:
    import pyreadstat

    source = Path(path)
    if not source.is_file():
        raise DecoderError(f"source bytes unavailable: {source}")
    source_sha = _sha(source)
    compatibility = _compatibility_config(source_sha, encoding)
    reader = pyreadstat.read_sav if expected_format == "sav" else pyreadstat.read_dta
    frame, metadata = reader(str(source), apply_value_formats=False, user_missing=True,
                             encoding=encoding)
    names = list(metadata.column_names)
    variables: list[PhysicalVariable] = []
    declarations: dict[str, tuple[Mapping[str, Any], ...]] = {}
    for ordinal, name in enumerate(names, 1):
        decl = _missing_declarations(metadata, name)
        declarations[name] = decl
        labels = (getattr(metadata, "variable_value_labels", {}) or {}).get(name, {}) or {}
        display = {
            "storage_width": (getattr(metadata, "variable_storage_width", {}) or {}).get(name),
            "display_width": (getattr(metadata, "variable_display_width", {}) or {}).get(name),
            "alignment": (getattr(metadata, "variable_alignment", {}) or {}).get(name),
            "measure": (getattr(metadata, "variable_measure", {}) or {}).get(name),
            "format": (getattr(metadata, "original_variable_types", {}) or {}).get(name),
        }
        variables.append(PhysicalVariable(
            ordinal, name, (getattr(metadata, "readstat_variable_types", {}) or {}).get(name),
            (getattr(metadata, "column_names_to_labels", {}) or {}).get(name),
            {str(_jsonable(k)): _jsonable(v) for k, v in labels.items()}, decl, display,
            {"multiple_response_sets": _jsonable((getattr(metadata, "mr_sets", {}) or {}))},
        ))
    cells: list[PhysicalCell] = []
    for row_ordinal, row in enumerate(frame.itertuples(index=False, name=None), 1):
        for variable, value in zip(variables, row):
            raw = _jsonable(value)
            state, declaration = _classify(raw, declarations[variable.name])
            selected = variable.value_labels.get(str(raw))
            cells.append(PhysicalCell(row_ordinal, variable.ordinal, variable.name, raw, state, declaration, selected))
    file_meta = {"file_encoding": _jsonable(getattr(metadata, "file_encoding", None)),
                 "file_format": _jsonable(getattr(metadata, "file_format", expected_format)),
                 "number_columns": len(names), "number_rows": len(frame)}
    return PhysicalSourceIncidence(source_sha, expected_format.upper(), len(frame), tuple(variables), tuple(cells),
                                   {"reader": "pyreadstat", "reader_version": getattr(pyreadstat, "__version__", None),
                                    "user_missing": True, "apply_value_formats": False, **compatibility}, file_meta)


def decode_sav(path: str | Path, *, encoding: str | None = None) -> PhysicalSourceIncidence:
    return _decode(path, expected_format="sav", encoding=encoding)


def decode_dta(path: str | Path, *, encoding: str | None = None) -> PhysicalSourceIncidence:
    return _decode(path, expected_format="dta", encoding=encoding)


__all__ = ["COMPATIBILITY_ALLOWLIST", "COMPATIBILITY_ONLY", "DecoderError", "PhysicalMissingState",
           "PhysicalVariable", "PhysicalCell", "PhysicalSourceIncidence", "decode_sav", "decode_dta"]
