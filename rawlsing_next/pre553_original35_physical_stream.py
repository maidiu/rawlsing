"""Bounded replayable physical-cell transport for a permitted original35 incidence.

The caller owns source-read admission and supplies an already decoded
``PhysicalSourceIncidence``.  This module never opens source bytes, grants
source/native/science authority, or invents respondent semantics.  It only
exposes the frozen decoder's exact full row/column grid through the existing
``ExactPhysicalCellStream`` expected by the current source-backed C11 factory.
"""
from __future__ import annotations

from collections.abc import Iterator

from rawlsing_next.pre553_physical_decoder import (
    PhysicalCell,
    PhysicalSourceIncidence,
)
from rawlsing_next.pre553_source_backed_c11_facade import ExactPhysicalCellStream

STREAM_TRANSPORT = "BOUNDED_REPLAYABLE_ORIGINAL35_PHYSICAL_SOURCE_INCIDENCE@1"


class Original35PhysicalStreamError(ValueError):
    pass


def _validate_incidence(incidence: PhysicalSourceIncidence) -> None:
    if not isinstance(incidence, PhysicalSourceIncidence):
        raise Original35PhysicalStreamError("PERMITTED_PHYSICAL_SOURCE_INCIDENCE_REQUIRED")
    if incidence.row_count < 0 or not incidence.variables:
        raise Original35PhysicalStreamError("EXACT_PHYSICAL_GRID_REQUIRED")
    custody = incidence.source_custody
    if custody is not None and custody.get("snapshot_sha256") != incidence.source_sha256:
        raise Original35PhysicalStreamError("SOURCE_CUSTODY_SHA_MISMATCH")
    try:
        if incidence.verify_source_identity() != incidence.source_sha256:
            raise Original35PhysicalStreamError("SOURCE_IDENTITY_CHANGED")
    except Exception as exc:
        if isinstance(exc, Original35PhysicalStreamError):
            raise
        raise Original35PhysicalStreamError("SOURCE_IDENTITY_UNAVAILABLE") from exc


def _exact_cells(
    incidence: PhysicalSourceIncidence, batch_size: int,
) -> Iterator[PhysicalCell]:
    _validate_incidence(incidence)
    columns = tuple((variable.ordinal, variable.name) for variable in incidence.variables)
    column_index = {key: index for index, key in enumerate(columns)}
    if len(column_index) != len(columns):
        raise Original35PhysicalStreamError("DUPLICATE_PHYSICAL_COLUMN_IDENTITY")
    expected = incidence.row_count * len(columns)
    position = 0
    for batch in incidence.iter_batches(batch_size):
        if not isinstance(batch, tuple) or not batch:
            raise Original35PhysicalStreamError("NONEMPTY_PHYSICAL_BATCH_REQUIRED")
        for cell in batch:
            if not isinstance(cell, PhysicalCell):
                raise Original35PhysicalStreamError("PHYSICAL_CELL_REQUIRED")
            expected_row, expected_column = divmod(position, len(columns))
            if (cell.row_ordinal != expected_row + 1
                    or column_index.get((cell.variable_ordinal, cell.variable_name))
                    != expected_column):
                raise Original35PhysicalStreamError("EXACT_ROW_COLUMN_IDENTITY_LOST")
            position += 1
            yield cell
    if position != expected:
        raise Original35PhysicalStreamError("SILENT_PHYSICAL_GRID_TRUNCATION")
    if incidence.verify_source_identity() != incidence.source_sha256:
        raise Original35PhysicalStreamError("SOURCE_IDENTITY_CHANGED_AFTER_SCAN")


def bounded_physical_cell_stream(
    incidence: PhysicalSourceIncidence, *, batch_size: int = 10_000,
) -> ExactPhysicalCellStream:
    """Return a replayable exact stream without materializing the physical grid."""
    if not isinstance(batch_size, int) or isinstance(batch_size, bool) or batch_size < 1:
        raise Original35PhysicalStreamError("POSITIVE_BATCH_SIZE_REQUIRED")
    _validate_incidence(incidence)
    return ExactPhysicalCellStream(
        source_sha256=incidence.source_sha256,
        row_count=incidence.row_count,
        cell_iter_factory=lambda: _exact_cells(incidence, batch_size),
        transport_identity=STREAM_TRANSPORT,
        decoder_metadata_digest=incidence.physical_metadata_digest,
    )


__all__ = [
    "STREAM_TRANSPORT",
    "Original35PhysicalStreamError",
    "bounded_physical_cell_stream",
]
