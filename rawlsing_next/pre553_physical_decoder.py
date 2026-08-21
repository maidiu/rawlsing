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
    reader_configuration: Mapping[str, Any]
    file_metadata: Mapping[str, Any]
    _frame: Any = None
    _variables_by_name: Mapping[str, PhysicalVariable] = None
    _source_path: str | None = None
    _reader_kind: str | None = None
    _encoding: str | None = None

    def iter_batches(self, batch_size: int = 10_000) -> Iterator[tuple[PhysicalCell, ...]]:
        """Yield bounded cell batches with stable source row ordinals.

        The decoder retains only the reader frame when a compatibility reader
        requires a full read; it never retains a complete cell-object universe.
        """
        if not isinstance(batch_size, int) or isinstance(batch_size, bool) or batch_size < 1:
            raise ValueError("batch_size must be a positive integer")
        variables = self.variables
        declarations = {v.name: v.missing_declarations for v in variables}
        rows_per_chunk = max(1, batch_size // max(1, len(variables)))

        def emit(frame: Any, row_offset: int) -> Iterator[tuple[PhysicalCell, ...]]:
            batch: list[PhysicalCell] = []
            for local_row, row in enumerate(frame.itertuples(index=False, name=None), 1):
                for variable, value in zip(variables, row):
                    raw = _jsonable(value)
                    state, declaration = classify_physical_value(raw, declarations[variable.name])
                    batch.append(PhysicalCell(row_offset + local_row, variable.ordinal, variable.name, raw, state,
                                              declaration, variable.value_labels.get(str(raw))))
                    if len(batch) >= batch_size:
                        yield tuple(batch)
                        batch.clear()
            if batch:
                yield tuple(batch)

        if self._frame is not None:
            yield from emit(self._frame, 0)
            return
        if self._source_path is None or self._reader_kind is None:
            return
        import pyreadstat
        reader = pyreadstat.read_sav if self._reader_kind == "SAV" else pyreadstat.read_dta
        row_offset = 0
        chunks = pyreadstat.read_file_in_chunks(
            reader, self._source_path, chunksize=rows_per_chunk, encoding=self._encoding,
            apply_value_formats=False, user_missing=True,
        )
        for frame, _metadata in chunks:
            yield from emit(frame, row_offset)
            row_offset += len(frame)

    def iter_cells(self, batch_size: int = 10_000) -> Iterator[PhysicalCell]:
        for batch in self.iter_batches(batch_size):
            yield from batch


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


def _missing_declarations(metadata: Any, name: str, source_format: str) -> tuple[Mapping[str, Any], ...]:
    ranges = getattr(metadata, "missing_ranges", {}) or {}
    user = getattr(metadata, "missing_user_values", {}) or {}
    result: list[Mapping[str, Any]] = []
    for item in ranges.get(name, ()):
        if isinstance(item, Mapping) and item.get("lo") == item.get("hi"):
            result.append({"kind": "discrete", "value": _jsonable(item.get("lo"))})
        else:
            result.append({"kind": "range", "lo": _jsonable(item.get("lo")), "hi": _jsonable(item.get("hi"))})
    for value in user.get(name, ()):
        token = _jsonable(value)
        if source_format == "DTA" and isinstance(token, str) and len(token) == 1 and token.lower() in "abcdefghijklmnopqrstuvwxyz":
            result.append({"kind": "extended", "reader_token": token, "stata_token": "." + token.lower()})
        elif source_format == "DTA" and isinstance(token, str) and len(token) == 2 and token[0] == "." and token[1].lower() in "abcdefghijklmnopqrstuvwxyz":
            result.append({"kind": "extended", "reader_token": token[1].lower(), "stata_token": token.lower()})
        else:
            result.append({"kind": "discrete", "value": token})
    return tuple(result)


def classify_physical_value(value: Any, declarations: tuple[Mapping[str, Any], ...]) -> tuple[PhysicalMissingState, Mapping[str, Any] | None]:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return PhysicalMissingState.SYSTEM_MISSING, None
    for declaration in declarations:
        if declaration["kind"] == "extended" and value in (declaration.get("reader_token"), declaration.get("stata_token"), declaration.get("token")):
            return PhysicalMissingState.FORMAT_EXTENDED_MISSING, declaration
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
    _metadata_frame, metadata = reader(str(source), metadataonly=True, apply_value_formats=False,
                                       user_missing=True, encoding=encoding)
    source_format = expected_format.upper()
    compatibility_full_read = encoding is not None
    frame = None
    if compatibility_full_read:
        frame, metadata = reader(str(source), apply_value_formats=False, user_missing=True, encoding=encoding)
    names = list(metadata.column_names)
    variables: list[PhysicalVariable] = []
    declarations: dict[str, tuple[Mapping[str, Any], ...]] = {}
    for ordinal, name in enumerate(names, 1):
        decl = _missing_declarations(metadata, name, source_format)
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
    file_meta = {"file_encoding": _jsonable(getattr(metadata, "file_encoding", None)),
                 "file_format": _jsonable(getattr(metadata, "file_format", expected_format)),
                 "number_columns": len(names), "number_rows": int(getattr(metadata, "number_rows", 0))}
    return PhysicalSourceIncidence(source_sha, source_format, int(getattr(metadata, "number_rows", 0)), tuple(variables),
                                   {"reader": "pyreadstat", "reader_version": getattr(pyreadstat, "__version__", None),
                                    "user_missing": True, "apply_value_formats": False, **compatibility}, file_meta,
                                   _frame=frame, _source_path=str(source), _reader_kind=source_format, _encoding=encoding)


def decode_sav(path: str | Path, *, encoding: str | None = None) -> PhysicalSourceIncidence:
    return _decode(path, expected_format="sav", encoding=encoding)


def decode_dta(path: str | Path, *, encoding: str | None = None) -> PhysicalSourceIncidence:
    return _decode(path, expected_format="dta", encoding=encoding)


__all__ = ["COMPATIBILITY_ALLOWLIST", "COMPATIBILITY_ONLY", "DecoderError", "PhysicalMissingState",
           "PhysicalVariable", "PhysicalCell", "PhysicalSourceIncidence", "classify_physical_value",
           "decode_sav", "decode_dta"]
