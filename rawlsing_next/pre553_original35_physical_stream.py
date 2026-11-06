"""Bounded replayable physical-cell transport for a permitted original35 incidence.

The caller owns source-read admission and supplies an already decoded
``PhysicalSourceIncidence``.  This module never opens source bytes, grants
source/native/science authority, or invents respondent semantics.  It only
exposes the frozen decoder's exact full row/column grid through the existing
``ExactPhysicalCellStream`` expected by the current source-backed C11 factory.
"""
from __future__ import annotations

from collections.abc import Iterator, Sequence

from rawlsing_next.pre553_physical_decoder import (
    PhysicalCell,
    PhysicalSourceIncidence,
    _physical_value,
    classify_physical_value,
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


def _cell(variable, row: int, value) -> PhysicalCell:
    raw = _physical_value(value)
    state, declaration = classify_physical_value(raw, variable.missing_declarations)
    return PhysicalCell(
        row_ordinal=row,
        variable_ordinal=variable.ordinal,
        variable_name=variable.name,
        raw_value=raw,
        missing_state=state,
        source_missing_declaration=declaration,
        raw_value_label=variable.value_labels.get(str(raw)),
    )


def _selected_frame_cells(
    incidence: PhysicalSourceIncidence, selected: tuple, frame,
) -> Iterator[PhysicalCell]:
    columns = tuple(str(name) for name in frame.columns)
    if len(set(columns)) != len(columns):
        raise Original35PhysicalStreamError("DUPLICATE_SOURCE_COLUMN_NAME")
    index = {name: position for position, name in enumerate(columns)}
    try:
        positions = tuple(index[variable.name] for variable in selected)
    except KeyError as exc:
        raise Original35PhysicalStreamError("SELECTED_PHYSICAL_COLUMN_ABSENT") from exc
    count = 0
    for row_ordinal, values in enumerate(frame.itertuples(index=False, name=None), 1):
        for variable, position in zip(selected, positions):
            yield _cell(variable, row_ordinal, values[position])
            count += 1
    if row_ordinal != incidence.row_count or count != incidence.row_count * len(selected):
        raise Original35PhysicalStreamError("SILENT_PHYSICAL_GRID_TRUNCATION")
    if incidence.verify_source_identity() != incidence.source_sha256:
        raise Original35PhysicalStreamError("SOURCE_IDENTITY_CHANGED_AFTER_SCAN")


def _selected_chunk_cells(
    incidence: PhysicalSourceIncidence, batch_size: int, selected: tuple,
) -> Iterator[PhysicalCell]:
    snapshot = incidence._source_snapshot
    reader_kind = incidence._reader_kind
    encoding = incidence._encoding
    if snapshot is None or reader_kind not in {"SAV", "DTA"}:
        raise Original35PhysicalStreamError("COLUMN_PROJECTED_READER_UNAVAILABLE")
    import pyreadstat

    reader = pyreadstat.read_sav if reader_kind == "SAV" else pyreadstat.read_dta
    rows_per_chunk = max(1, batch_size // len(selected))
    snapshot.rewind()
    chunks = pyreadstat.read_file_in_chunks(
        reader, snapshot.reader_path, chunksize=rows_per_chunk,
        usecols=[variable.name for variable in selected],
        encoding=encoding, apply_value_formats=False, user_missing=True,
    )
    row_offset = 0
    for frame, _metadata in chunks:
        snapshot.check_stable()
        columns = tuple(str(name) for name in frame.columns)
        if set(columns) != {variable.name for variable in selected}:
            raise Original35PhysicalStreamError("SELECTED_PHYSICAL_COLUMN_SET_CHANGED")
        index = {name: position for position, name in enumerate(columns)}
        positions = tuple(index[variable.name] for variable in selected)
        for local_row, values in enumerate(frame.itertuples(index=False, name=None), 1):
            row_ordinal = row_offset + local_row
            for variable, position in zip(selected, positions):
                yield _cell(variable, row_ordinal, values[position])
        row_offset += len(frame)
    if row_offset != incidence.row_count:
        raise Original35PhysicalStreamError("SILENT_PHYSICAL_GRID_TRUNCATION")
    snapshot.verify()


def _selected_cells(
    incidence: PhysicalSourceIncidence, batch_size: int, selected_names: tuple[str, ...],
) -> Iterator[PhysicalCell]:
    _validate_incidence(incidence)
    selected = tuple(
        variable for variable in incidence.variables if variable.name in selected_names
    )
    if len(selected) != len(selected_names):
        raise Original35PhysicalStreamError("SELECTED_PHYSICAL_COLUMN_ABSENT")
    if len({variable.name for variable in selected}) != len(selected):
        raise Original35PhysicalStreamError("DUPLICATE_SOURCE_COLUMN_NAME")
    frame = incidence._frame
    if frame is not None:
        yield from _selected_frame_cells(incidence, selected, frame)
        return
    yield from _selected_chunk_cells(incidence, batch_size, selected)


def bounded_physical_cell_stream(
    incidence: PhysicalSourceIncidence, *, batch_size: int = 10_000,
    include_variables: Sequence[str] | None = None,
) -> ExactPhysicalCellStream:
    """Return a replayable exact stream without materializing the physical grid.

    ``include_variables=None`` exposes the complete row/column grid for the
    source-backed C11 factory.  An explicit exact column selection exposes only
    those columns, still over every declared source row and the same source SHA,
    for D's selected-item native compiler consumer.
    """
    if not isinstance(batch_size, int) or isinstance(batch_size, bool) or batch_size < 1:
        raise Original35PhysicalStreamError("POSITIVE_BATCH_SIZE_REQUIRED")
    _validate_incidence(incidence)
    if include_variables is None:
        factory = lambda: _exact_cells(incidence, batch_size)
    else:
        if (isinstance(include_variables, (str, bytes)) or not include_variables
                or any(not isinstance(name, str) or not name for name in include_variables)
                or len(set(include_variables)) != len(include_variables)):
            raise Original35PhysicalStreamError("EXACT_UNIQUE_COLUMN_SELECTION_REQUIRED")
        selected_names = tuple(include_variables)
        factory = lambda: _selected_cells(incidence, batch_size, selected_names)
    return ExactPhysicalCellStream(
        source_sha256=incidence.source_sha256,
        row_count=incidence.row_count,
        cell_iter_factory=factory,
        transport_identity=STREAM_TRANSPORT,
        decoder_metadata_digest=incidence.physical_metadata_digest,
    )


__all__ = [
    "STREAM_TRANSPORT",
    "Original35PhysicalStreamError",
    "bounded_physical_cell_stream",
]
