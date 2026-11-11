from __future__ import annotations

import hashlib
from pathlib import Path
import types

import pandas as pd
import pyreadstat
import pytest

import rawlsing_next.ee_p2x_darwin_stage_backend as backend
from rawlsing_next import pre553_physical_decoder as decoder
from rawlsing_next.pre553_r5_codec import R5TypedValueCodec


CODEC = R5TypedValueCodec()


def _write_sav(path: Path) -> Path:
    pyreadstat.write_sav(
        pd.DataFrame({"score": [1.5, -2.25, 0.0], "label": ["a", "b", "c"]}),
        str(path),
    )
    return path


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_current_pr526_custody_and_sav_float_representation_survive_repair(tmp_path: Path):
    path = _write_sav(tmp_path / "custody-float.sav")
    source_sha = _sha(path)
    incidence = decoder.decode_sav(path, expected_source_sha256=source_sha)
    try:
        custody = incidence.source_custody
        assert custody["contract"] == decoder.SOURCE_CUSTODY_CONTRACT
        assert custody["source_sha256"] == source_sha
        assert custody["snapshot_sha256"] == source_sha
        assert custody["reader_binding"] == "OPEN_FD_VIA_POSIX_DEV_FD"
        assert custody["reader_access_mode"] == "O_RDONLY"
        assert custody["snapshot_path_unlinked"] is True
        assert custody["content_bound"] is True
        assert incidence.verify_source_identity() == source_sha
        cells = [cell for cell in incidence.iter_cells(2) if cell.variable_name == "score"]
        assert [cell.raw_value for cell in cells] == [1.5, -2.25, 0.0]
        assert all(type(cell.raw_value) is float for cell in cells)
        assert [CODEC.encode(cell.raw_value)["t"] for cell in cells] == [
            "float64_finite", "float64_finite", "float64_finite",
        ]
        assert incidence._source_snapshot.access_mode == "O_RDONLY"
        assert incidence._source_snapshot.reader_path.startswith("/dev/fd/")
        assert not incidence._source_snapshot.path.exists()
    finally:
        incidence.close()
    assert incidence._source_snapshot.access_mode == "CLOSED"


def test_pr526_snapshot_survives_original_path_tamper(tmp_path: Path):
    path = _write_sav(tmp_path / "custody-tamper-after.sav")
    source_sha = _sha(path)
    incidence = decoder.decode_sav(path)
    try:
        path.write_bytes(b"tampered after content-bound snapshot acquisition")
        assert _sha(path) != source_sha
        assert incidence.verify_source_identity() == source_sha
        cells = [cell for cell in incidence.iter_cells(2) if cell.variable_name == "score"]
        assert [cell.raw_value for cell in cells] == [1.5, -2.25, 0.0]
    finally:
        incidence.close()


def test_fault_source_tamper_before_decode_is_refused(tmp_path: Path):
    path = _write_sav(tmp_path / "tamper-before.sav")
    source_sha = _sha(path)
    damaged = bytearray(path.read_bytes())
    damaged[-1] ^= 0x01
    path.write_bytes(bytes(damaged))
    assert _sha(path) != source_sha
    with pytest.raises(decoder.DecoderError, match="source sha256 mismatch before governed decode"):
        decoder.decode_sav(path, expected_source_sha256=source_sha)


def test_actual_decoder_consumer_decode_regression(tmp_path: Path, monkeypatch):
    path = _write_sav(tmp_path / "actual-consumer.sav")
    source_sha = _sha(path)
    monkeypatch.setitem(backend.EXPECTED_SOURCE, "WVS7", source_sha)
    ctx = types.SimpleNamespace(
        stage=types.SimpleNamespace(source="WVS7", address="TEST/S00_SOURCE_PREFLIGHT_IDENTITY"),
        source_path=path,
        source_sha256=source_sha,
    )
    state = {"source_access": {"open": 0, "decode": 0, "reread": 0, "bytes": 0}}
    incidence = backend._decode(ctx, state)
    try:
        assert incidence.source_sha256 == source_sha
        assert [variable.name for variable in incidence.variables] == ["score", "label"]
        assert state["source_access"] == {
            "open": 1,
            "decode": 1,
            "reread": 0,
            "bytes": path.stat().st_size,
        }
        assert state["_t4_source_events"] == ["open", "decode"]
        assert state["_t4_io_events"][-1]["operation"] == "READ"
        assert state["_t4_io_events"][-1]["object_id"] == "CANONICAL_SOURCE::" + source_sha
        cells = [cell for cell in incidence.iter_cells(2) if cell.variable_name == "score"]
        assert [cell.raw_value for cell in cells] == [1.5, -2.25, 0.0]
    finally:
        incidence.close()
