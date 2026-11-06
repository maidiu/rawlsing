from dataclasses import replace
from pathlib import Path

import pandas as pd
import pytest

from rawlsing_next.pre553_original35_physical_stream import (
    STREAM_TRANSPORT,
    Original35PhysicalStreamError,
    bounded_physical_cell_stream,
)
from rawlsing_next.pre553_physical_decoder import (
    PHYSICAL_METADATA_CONTRACT,
    PhysicalSourceIncidence,
    PhysicalVariable,
    decode_sav,
)
from rawlsing_next.source_configuration.factory import build_validated_c11_release_from_config
from rawlsing_next.source_configuration.schema import load_source_config
from rawlsing_next.tests.test_universal_source_projection import build_s3, s3_rows

CONFIG = Path(__file__).resolve().parents[2] / "source_pre553_validation/foundation/examples/SRC09_q101_fixture.config.json"
FIXTURE = Path(__file__).resolve().parents[2] / "source_pre553_validation/foundation/fixtures/SRC09_q101_nonrespondent.json"


def test_bounded_stream_exact_replay_and_factory_parity(tmp_path):
    path = tmp_path / "bounded.sav"
    bundle = build_s3(path, s3_rows(respondents=5, occasions=2))
    incidence = decode_sav(path, expected_source_sha256=bundle.source_sha256)
    try:
        stream = bounded_physical_cell_stream(incidence, batch_size=7)
        expected = tuple(incidence.iter_cells(5))
        assert tuple(stream.iter_cells()) == expected
        assert tuple(stream.iter_cells()) == expected
        assert stream.source_sha256 == incidence.source_sha256
        assert stream.row_count == incidence.row_count == 10
        assert stream.decoder_metadata_digest == incidence.physical_metadata_digest
        assert stream.transport_identity == STREAM_TRANSPORT
        config = load_source_config(CONFIG)
        frame = pd.DataFrame({
            "country": [1.0, 2.0, 3.0, 4.0, 5.0, 1.0, 2.0, 3.0, 4.0],
            "q101": [1.0, 2.0, 3.0, 4.0, -1.0, 7.0, 8.0, 9.0, None],
        })
        fixture_incidence = PhysicalSourceIncidence(
            source_sha256=config.active_source_sha256,
            source_format="SAV",
            row_count=9,
            variables=(
                PhysicalVariable(1, "country", "double", "Country code", {}, (), {}, {}),
                PhysicalVariable(124, "q101", "double", "q101", {}, (), {}, {}),
            ),
            reader_configuration={"fixture": "R157_P0_NONRESPONDENT"},
            file_metadata={
                "contract_schema": PHYSICAL_METADATA_CONTRACT,
                "raw_layout_declarations": {},
                "normalized_geometry": {},
                "display_metadata": {},
                "decoder_identity": {"implementation": "fixture"},
            },
            _frame=frame,
        )
        fixture_stream = bounded_physical_cell_stream(fixture_incidence, batch_size=2)
        from_incidence = build_validated_c11_release_from_config(
            config, incidence=fixture_incidence, batch_size=2,
        )
        from_stream = build_validated_c11_release_from_config(
            config, stream=fixture_stream, batch_size=3,
        )
        assert from_stream.release_ref == from_incidence.release_ref
        assert from_stream.replay_manifest.ref == from_incidence.replay_manifest.ref
        assert tuple(obj.as_dict() for obj in from_stream.public_objects) == tuple(
            obj.as_dict() for obj in from_incidence.public_objects
        )
    finally:
        incidence.close()


def test_bounded_stream_rejects_wrong_source_or_batch(tmp_path):
    path = tmp_path / "bounded-fault.sav"
    bundle = build_s3(path, s3_rows(respondents=3, occasions=1))
    incidence = decode_sav(path, expected_source_sha256=bundle.source_sha256)
    try:
        with pytest.raises(Original35PhysicalStreamError, match="SOURCE_CUSTODY_SHA_MISMATCH"):
            bounded_physical_cell_stream(replace(incidence, source_sha256="f" * 64))
        for value in (0, -1, True, 1.5):
            with pytest.raises(Original35PhysicalStreamError, match="POSITIVE_BATCH_SIZE_REQUIRED"):
                bounded_physical_cell_stream(incidence, batch_size=value)
        stream = bounded_physical_cell_stream(incidence, batch_size=2)
        assert tuple(stream.iter_cells()) == tuple(incidence.iter_cells(3))
        path.write_bytes(b"changed-after-decoded-snapshot")
        assert tuple(stream.iter_cells()) == tuple(incidence.iter_cells(3))
    finally:
        incidence.close()


def test_bounded_stream_rejects_truncated_or_reordered_grid(tmp_path):
    path = tmp_path / "bounded-order.sav"
    bundle = build_s3(path, s3_rows(respondents=2, occasions=1))
    incidence = decode_sav(path, expected_source_sha256=bundle.source_sha256)
    try:
        stream = bounded_physical_cell_stream(incidence, batch_size=3)
        cells = tuple(stream.iter_cells())
        original = incidence.iter_batches
        object.__setattr__(incidence, "iter_batches", lambda _batch_size=3: iter(((cells[1], cells[0], *cells[2:]),)))
        try:
            with pytest.raises(Original35PhysicalStreamError, match="EXACT_ROW_COLUMN_IDENTITY_LOST"):
                tuple(bounded_physical_cell_stream(incidence, batch_size=3).iter_cells())
        finally:
            object.__setattr__(incidence, "iter_batches", original)
        object.__setattr__(incidence, "iter_batches", lambda _batch_size=3: iter((cells[:-1],)))
        try:
            with pytest.raises(Original35PhysicalStreamError, match="SILENT_PHYSICAL_GRID_TRUNCATION"):
                tuple(bounded_physical_cell_stream(incidence, batch_size=3).iter_cells())
        finally:
            object.__setattr__(incidence, "iter_batches", original)
    finally:
        incidence.close()
