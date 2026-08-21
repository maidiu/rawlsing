"""Frozen-decoder -> R5 decoder-normalized physical batch seam.

The seam preserves physical observations and source metadata without assigning
C11 semantic meaning.  Source-cell locators are explicitly distinct from C11
event-occurrence identity.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_r5_codec import R5TypedValueCodec, canonical_bytes


SEAM_VERSION = "PRE553_R5_DECODER_NORMALIZED_SEAM@1.0.0"


class R5SeamError(ValueError):
    pass


@dataclass(frozen=True)
class R5GeometryCertificate:
    source_sha256: str
    row_count: int
    variable_count: int
    complete_rectangular_row_major: bool
    certificate_id: str

    def source_cell_locator(self, row_ordinal: int, variable_ordinal: int) -> int:
        if not self.complete_rectangular_row_major:
            raise R5SeamError("implicit source-cell geometry is uncertified")
        if not (1 <= row_ordinal <= self.row_count):
            raise R5SeamError("row ordinal outside certified source geometry")
        if not (0 <= variable_ordinal < self.variable_count):
            raise R5SeamError("variable ordinal outside certified source geometry")
        return (row_ordinal - 1) * self.variable_count + variable_ordinal


@dataclass(frozen=True)
class R5PhysicalVariableRecord:
    source_sha256: str
    ordinal: int
    name: str
    storage_type: str | None
    variable_label: Any
    value_labels: Any
    missing_declarations: tuple[Any, ...]
    display_metadata: Any
    topology_metadata: Any


@dataclass(frozen=True)
class R5PhysicalCellRecord:
    source_sha256: str
    row_ordinal: int
    variable_ordinal: int
    variable_name: str
    raw_value: Mapping[str, Any]
    missing_state: str
    source_missing_declaration: Mapping[str, Any] | None
    raw_value_label: Mapping[str, Any]
    explicit_source_coordinates: tuple[int, int]
    source_cell_locator: int | None
    # Never a semantic event occurrence id.  It is deliberately named otherwise.


@dataclass(frozen=True)
class R5NormalizedBatch:
    seam_version: str
    source_sha256: str
    cells: tuple[R5PhysicalCellRecord, ...]
    vector_fast_path_used: bool
    vector_fallback_count: int


def _state_text(state: Any) -> str:
    value = getattr(state, "value", state)
    if not isinstance(value, str) or not value:
        raise R5SeamError("physical missing state must be a non-empty frozen-decoder state")
    return value


def normalize_variables(incidence: Any, *, codec: R5TypedValueCodec | None = None) -> tuple[R5PhysicalVariableRecord, ...]:
    codec = codec or R5TypedValueCodec()
    source_sha = getattr(incidence, "source_sha256", None)
    if not isinstance(source_sha, str) or len(source_sha) != 64:
        raise R5SeamError("exact source SHA-256 is required")
    result = []
    for variable in getattr(incidence, "variables", ()):
        declarations = tuple(codec.encode(v) for v in tuple(getattr(variable, "missing_declarations", ())))
        result.append(R5PhysicalVariableRecord(
            source_sha256=source_sha,
            ordinal=int(variable.ordinal),
            name=str(variable.name),
            storage_type=getattr(variable, "storage_type", None),
            variable_label=codec.encode(getattr(variable, "variable_label", None)),
            value_labels=codec.encode(getattr(variable, "value_labels", {})),
            missing_declarations=declarations,
            display_metadata=codec.encode(getattr(variable, "display_metadata", {})),
            topology_metadata=codec.encode(getattr(variable, "topology_metadata", {})),
        ))
    return tuple(result)


def _scalar_cell(source_sha: str, cell: Any, codec: R5TypedValueCodec,
                 geometry: R5GeometryCertificate | None) -> R5PhysicalCellRecord:
    row = int(getattr(cell, "row_ordinal"))
    var = int(getattr(cell, "variable_ordinal"))
    locator = geometry.source_cell_locator(row, var) if geometry is not None else None
    declaration = getattr(cell, "source_missing_declaration", None)
    return R5PhysicalCellRecord(
        source_sha256=source_sha,
        row_ordinal=row,
        variable_ordinal=var,
        variable_name=str(getattr(cell, "variable_name")),
        raw_value=codec.encode(getattr(cell, "raw_value")),
        missing_state=_state_text(getattr(cell, "missing_state")),
        source_missing_declaration=None if declaration is None else codec.encode(declaration),
        # Store selected label directly.  Do not rederive through host-language
        # equality or a possibly non-injective dictionary key.
        raw_value_label=codec.encode(getattr(cell, "raw_value_label", None)),
        explicit_source_coordinates=(row, var),
        source_cell_locator=locator,
    )


def _all_finite_floats(cells: Sequence[Any]) -> bool:
    import math
    return bool(cells) and all(isinstance(getattr(c, "raw_value", None), float)
                               and math.isfinite(getattr(c, "raw_value")) for c in cells)


def normalize_decoder_batch(source_sha256: str, cells: Iterable[Any], *,
                            codec: R5TypedValueCodec | None = None,
                            geometry: R5GeometryCertificate | None = None,
                            permit_vector_hot_path: bool = True,
                            validate_vector_parity: bool = True) -> R5NormalizedBatch:
    codec = codec or R5TypedValueCodec()
    batch = tuple(cells)
    if geometry is not None and geometry.source_sha256 != source_sha256:
        raise R5SeamError("geometry certificate source identity mismatch")

    # The only R5 V1 vector hot path is exact finite float64 bit extraction.
    # It is deliberately narrow and falls back for every other type/state mix.
    if permit_vector_hot_path and _all_finite_floats(batch):
        try:
            import numpy as np
            values = np.asarray([c.raw_value for c in batch], dtype=">f8")
            raw = values.tobytes()
            bit_hex = [raw[i:i + 8].hex() for i in range(0, len(raw), 8)]
        except Exception:
            # No optional vector backend or unexpected backend behavior: exact fallback.
            bit_hex = None
        if bit_hex is not None:
            records = []
            for cell, bits in zip(batch, bit_hex):
                scalar = _scalar_cell(source_sha256, cell, codec, geometry)
                encoded = {"t": "float64_finite", "bits": bits}
                if validate_vector_parity and canonical_bytes(encoded) != canonical_bytes(scalar.raw_value):
                    raise R5SeamError("vector finite-float encoding diverges from exact scalar codec")
                records.append(R5PhysicalCellRecord(
                    **{**scalar.__dict__, "raw_value": encoded}
                ))
            return R5NormalizedBatch(SEAM_VERSION, source_sha256, tuple(records), True, 0)

    records = tuple(_scalar_cell(source_sha256, cell, codec, geometry) for cell in batch)
    return R5NormalizedBatch(SEAM_VERSION, source_sha256, records, False, len(records))


def iter_normalized_batches(incidence: Any, *, batch_size: int = 10_000,
                            codec: R5TypedValueCodec | None = None,
                            geometry: R5GeometryCertificate | None = None) -> Iterable[R5NormalizedBatch]:
    source_sha = getattr(incidence, "source_sha256", None)
    for batch in incidence.iter_batches(batch_size):
        yield normalize_decoder_batch(source_sha, batch, codec=codec, geometry=geometry)


__all__ = [
    "SEAM_VERSION", "R5SeamError", "R5GeometryCertificate", "R5PhysicalVariableRecord",
    "R5PhysicalCellRecord", "R5NormalizedBatch", "normalize_variables",
    "normalize_decoder_batch", "iter_normalized_batches",
]

# Canonical source-native row projection used by LONG_SHARDED.  These rows are
# physical evidence, not C11 semantic objects.
def _physical_row(relation: str, family: str, object_id: str, payload: Mapping[str, Any]):
    import hashlib
    from rawlsing_next.pre553_r5_model import R5CanonicalRow
    digest = hashlib.sha256(canonical_bytes(payload)).hexdigest()
    return R5CanonicalRow(relation, family, object_id, digest, payload)


def source_metadata_row(incidence: Any, *, codec: R5TypedValueCodec | None = None):
    codec = codec or R5TypedValueCodec()
    source_sha = getattr(incidence, "source_sha256", None)
    payload = {
        "seam_version": SEAM_VERSION,
        "source_sha256": source_sha,
        "source_format": getattr(incidence, "source_format", None),
        "row_count": int(getattr(incidence, "row_count")),
        "variable_count": len(tuple(getattr(incidence, "variables", ()))),
        "reader_configuration": codec.encode(getattr(incidence, "reader_configuration", {})),
        "file_metadata": codec.encode(getattr(incidence, "file_metadata", {})),
    }
    return _physical_row("source_metadata", "R5SourceMetadata@1.0.0", f"source:{source_sha}:metadata", payload)


def variable_record_row(record: R5PhysicalVariableRecord):
    payload = {
        "seam_version": SEAM_VERSION,
        "source_sha256": record.source_sha256,
        "ordinal": record.ordinal,
        "name": record.name,
        "storage_type": record.storage_type,
        "variable_label": record.variable_label,
        "value_labels": record.value_labels,
        "missing_declarations": list(record.missing_declarations),
        "display_metadata": record.display_metadata,
        "topology_metadata": record.topology_metadata,
    }
    return _physical_row("source_variables", "R5PhysicalVariable@1.0.0",
                         f"source:{record.source_sha256}:variable:{record.ordinal}", payload)


def cell_record_row(record: R5PhysicalCellRecord):
    payload = {
        "seam_version": SEAM_VERSION,
        "source_sha256": record.source_sha256,
        "row_ordinal": record.row_ordinal,
        "variable_ordinal": record.variable_ordinal,
        "variable_name": record.variable_name,
        "raw_value": record.raw_value,
        "missing_state": record.missing_state,
        "source_missing_declaration": record.source_missing_declaration,
        "raw_value_label": record.raw_value_label,
        "explicit_source_coordinates": list(record.explicit_source_coordinates),
        "source_cell_locator": record.source_cell_locator,
    }
    return _physical_row("source_physical_cells", "R5PhysicalCell@1.0.0",
                         f"source:{record.source_sha256}:cell:{record.row_ordinal}:{record.variable_ordinal}", payload)


def iter_source_native_rows(incidence: Any, *, batch_size: int = 10_000,
                            codec: R5TypedValueCodec | None = None,
                            geometry: R5GeometryCertificate | None = None):
    """Stream complete frozen-decoder physical truth into canonical R5 rows."""
    codec = codec or R5TypedValueCodec()
    yield source_metadata_row(incidence, codec=codec)
    for variable in normalize_variables(incidence, codec=codec):
        yield variable_record_row(variable)
    for batch in iter_normalized_batches(incidence, batch_size=batch_size, codec=codec, geometry=geometry):
        for cell in batch.cells:
            yield cell_record_row(cell)


__all__.extend([
    "source_metadata_row", "variable_record_row", "cell_record_row", "iter_source_native_rows",
])
