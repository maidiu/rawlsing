from __future__ import annotations

from pathlib import Path
import subprocess
import sys

import pytest

import rawlsing_next.pre553_physical_decoder as decoder
from rawlsing_next.pre553_physical_decoder import (
    DecoderError,
    compute_physical_metadata_digest,
    decode_dta,
    decode_sav,
)
from rawlsing_next.tests.test_pyat940_s1b_support import write_fixture


ROOT = Path(__file__).resolve().parents[2]
EXISTING_REGRESSION_TESTS = (
    "rawlsing_next/tests/test_pre553_source_backed_c11_facade.py",
    "rawlsing_next/tests/test_wave1_r5_q86_c11_projection.py",
    "rawlsing_next/tests/test_universal_source_byte_custody.py",
    "rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py",
    "rawlsing_next/tests/test_pre553_sr06_decoder_carrier.py",
)


@pytest.mark.parametrize("source_format", ("SAV", "DTA"))
def test_b09_decoder_metadata_and_custody_surface_preserved(tmp_path, source_format):
    path, source_sha, rows = write_fixture(
        tmp_path / source_format,
        source_format=source_format,
        values=(1.0, 2.0, 7.0, None),
    )
    decoder_fn = decode_sav if source_format == "SAV" else decode_dta
    first = decoder_fn(path, expected_source_sha256=source_sha)
    try:
        assert first.source_sha256 == source_sha
        assert first.row_count == rows == 4
        assert [variable.name for variable in first.variables] == ["q101", "country"]
        q101 = first.variables[0]
        assert q101.storage_type == "double"
        labels = q101.value_labels
        assert labels.get("1.0", labels.get("1")) == "one"
        assert labels.get("7.0", labels.get("7")) == "DK"
        assert first.reader_configuration["user_missing"] is True
        assert first.reader_configuration["apply_value_formats"] is False
        expected_digest = compute_physical_metadata_digest(
            source_sha256=first.source_sha256,
            source_format=first.source_format,
            reader_configuration=first.reader_configuration,
            file_metadata=first.file_metadata,
            variables=first.variables,
        )
        assert first.physical_metadata_digest == expected_digest
        first.require_physical_metadata_digest(expected_digest)

        cells = list(first.iter_cells(4))
        assert len(cells) == rows * 2
        assert {(cell.row_ordinal, cell.variable_name) for cell in cells} == {
            (row, name) for row in range(1, rows + 1) for name in ("q101", "country")
        }
        custody = first.source_custody
        assert custody["contract"] == decoder.SOURCE_CUSTODY_CONTRACT
        assert custody["content_bound"] is True
        assert custody["reader_binding"] == "OPEN_FD_VIA_POSIX_DEV_FD"
        assert custody["reader_access_mode"] == "O_RDONLY"
        assert custody["source_sha256"] == source_sha
        assert custody["snapshot_sha256"] == source_sha
    finally:
        first.close()
    with pytest.raises(DecoderError, match="source snapshot is closed"):
        list(first.iter_cells())


def test_b09_existing_decoder_facade_and_custody_regressions_pass():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", *EXISTING_REGRESSION_TESTS],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT), "PATH": "/usr/bin:/bin:/usr/local/bin"},
    )
    assert result.returncode == 0, (
        "existing decoder/facade regression suite failed:\n"
        f"stdout={result.stdout[-4000:]}\nstderr={result.stderr[-4000:]}"
    )
    assert " failed" not in result.stdout.lower()
