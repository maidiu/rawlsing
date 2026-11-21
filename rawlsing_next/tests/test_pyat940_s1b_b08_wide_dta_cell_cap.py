"""B08 repair: the DTA declaration probe must obey the declared cell cap.

The probe pass exists to recover Stata extended-missing declarations.  Its row
window must be bounded by both MAX_READ_ROWS and MAX_READ_CELLS.  A wide file
previously took the MIN_READ_ROWS floor even when that floor exceeded the cell
cap, materialising > MAX_READ_CELLS cells in one reader chunk.
"""
from __future__ import annotations

import hashlib

import pandas as pd
import pyreadstat

import rawlsing_next.pre553_physical_decoder as decoder
from rawlsing_next.pre553_physical_decoder import decode_dta


def test_b08_wide_dta_probe_and_data_chunks_respect_cell_cap(tmp_path, monkeypatch):
    width = 1_001
    rows = 1_050
    frame = pd.DataFrame({
        f"v{column}": [float((row + column) % 7) for row in range(rows)]
        for column in range(width)
    })
    path = tmp_path / "wide.dta"
    pyreadstat.write_dta(frame, str(path))
    source_sha = hashlib.sha256(path.read_bytes()).hexdigest()

    requested_sizes: list[int] = []
    actual_sizes: list[int] = []
    original_chunks = pyreadstat.read_file_in_chunks

    def tracked_chunks(reader, file_path, *args, **kwargs):
        requested_sizes.append(int(kwargs["chunksize"]))

        def tracked_reader(path_arg, **inner_kwargs):
            frame = reader(path_arg, **inner_kwargs)
            if not inner_kwargs.get("metadataonly", False):
                try:
                    actual_sizes.append(len(frame[0]))
                except TypeError:
                    pass
            return frame

        return original_chunks(tracked_reader, file_path, *args, **kwargs)

    monkeypatch.setattr(pyreadstat, "read_file_in_chunks", tracked_chunks)

    incidence = decode_dta(path, expected_source_sha256=source_sha)
    try:
        probe_chunks = list(actual_sizes)
        probe_requests = list(requested_sizes)
        assert probe_chunks, "the DTA declaration probe must actually execute"
        assert len(incidence.variables) == width
        assert incidence.row_count == rows

        requested_sizes.clear()
        actual_sizes.clear()
        cell_count = sum(len(batch) for batch in incidence.iter_batches(128))
        data_chunks = list(actual_sizes)
        data_requests = list(requested_sizes)
        assert data_chunks, "the bounded data pass must actually execute"
        assert cell_count == rows * width
        assert sum(probe_chunks) == rows
        assert sum(data_chunks) == rows

        cap = decoder.MAX_READ_CELLS
        for chunks, requests in (
            (probe_chunks, probe_requests),
            (data_chunks, data_requests),
        ):
            assert all(chunk * width <= cap for chunk in chunks), (
                chunks, width, cap)
            assert all(chunk <= decoder.MAX_READ_ROWS for chunk in chunks)
            assert all(chunk * width <= cap for chunk in requests), (
                requests, width, cap)
            assert all(chunk <= decoder.MAX_READ_ROWS for chunk in requests)
    finally:
        incidence.close()
