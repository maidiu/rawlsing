from __future__ import annotations

import datetime as dt
import hashlib
import importlib
import pathlib
import struct
import subprocess
import sys
import types

import pandas as pd
import pyreadstat
import pytest

from rawlsing_next import pre553_physical_decoder as decoder
from rawlsing_next.pre553_r5_codec import (
    R5CodecError,
    R5OpaqueValue,
    R5TypedValueCodec,
    normalize_decoder_physical_value,
    opaque_decoder_value,
)


CODEC = R5TypedValueCodec()
ROOT = pathlib.Path(__file__).resolve().parents[2]

PINNED_SEAM_OWNER = "0b96b8de9aac774566f872cf0630ebd4ddeb70e6"
PINNED_SEAM_BLOB = "cef326ebbc40468428378f7fdbe76e4756179f39"
PINNED_SEAM_SHA256 = "626f74200a11dd8f749bead1ebd904eae22b65246636395a16df60d33d2b052f"
PINNED_MODEL_BLOB = "62ce608829c3d9c2fb7c999aefe40188637edf80"
PINNED_MODEL_SHA256 = "cdb8a2581aeed7f24acd668f3b93ca23244f64820266e5d282fb65915c17ac3a"


class _ItemWrapper:
    def __init__(self, value):
        self._value = value

    def item(self):
        return self._value


class _ChainWrapper(_ItemWrapper):
    pass


class _NaiveDT(dt.datetime):
    pass


class _AwareDT(dt.datetime):
    pass


def _git_blob(spec: str) -> bytes:
    try:
        completed = subprocess.run(
            ["git", "-C", str(ROOT), "cat-file", "-p", spec],
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        pytest.fail(f"local git object database unavailable for pinned seam: {exc}")
    if completed.returncode != 0:
        pytest.fail(
            "pinned R5 seam objects are absent from the local git object database; "
            f"cannot execute the actual first seam consumer ({spec})"
        )
    return completed.stdout


def _load_pinned_module(name: str, path: str, expected_blob: str, expected_sha256: str):
    source = _git_blob(f"{PINNED_SEAM_OWNER}:{path}")
    observed_blob = subprocess.run(
        ["git", "-C", str(ROOT), "hash-object", "--stdin"],
        input=source,
        capture_output=True,
        check=True,
    ).stdout.decode("ascii").strip()
    assert observed_blob == expected_blob
    assert hashlib.sha256(source).hexdigest() == expected_sha256
    module = types.ModuleType(name)
    module.__package__ = "rawlsing_next"
    sys.modules[name] = module
    exec(compile(source, f"<{name}@{PINNED_SEAM_OWNER}>", "exec"), module.__dict__)
    return module


def _pinned_seam():
    name = "rawlsing_next.pre553_r5_seam"
    if name in sys.modules:
        return sys.modules[name]
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as exc:
        if exc.name != name:
            raise
    _load_pinned_module(
        "rawlsing_next.pre553_r5_model",
        "rawlsing_next/pre553_r5_model.py",
        PINNED_MODEL_BLOB,
        PINNED_MODEL_SHA256,
    )
    return _load_pinned_module(
        name,
        "rawlsing_next/pre553_r5_seam.py",
        PINNED_SEAM_BLOB,
        PINNED_SEAM_SHA256,
    )


def _write_frame(path: pathlib.Path, writer) -> pathlib.Path:
    frame = pd.DataFrame(
        {
            "dtm": pd.to_datetime(["2008-04-05 06:07:08", "2009-05-06 07:08:09"]),
            "score": [1.5, -2.25],
            "label": ["a", "b"],
        }
    )
    writer(frame, str(path))
    return path


def _sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.mark.parametrize(
    "suffix,writer,reader",
    [
        ("sav", pyreadstat.write_sav, decoder.decode_sav),
        ("dta", pyreadstat.write_dta, decoder.decode_dta),
    ],
)
def test_real_sav_and_dta_datetime_cells_are_opaque_at_cells_and_first_seam(
    tmp_path: pathlib.Path, suffix, writer, reader
):
    path = _write_frame(tmp_path / f"real-datetime.{suffix}", writer)
    incidence = reader(path)
    try:
        cells = [cell for cell in incidence.iter_cells(2) if cell.variable_name == "dtm"]
        assert len(cells) == 2
        expected = (
            (2008, 4, 5, 6, 7, 8, 0, 0),
            (2009, 5, 6, 7, 8, 9, 0, 0),
        )
        for cell, civil in zip(cells, expected):
            assert type(cell.raw_value) is R5OpaqueValue
            assert not isinstance(cell.raw_value, str)
            assert cell.raw_value.type_id == "python.datetime.datetime@1"
            assert struct.unpack(">HBBBBBIB", cell.raw_value.payload) == civil
            encoded = CODEC.encode(cell.raw_value)
            assert encoded["t"] == "opaque"
            assert encoded["type_id"] == "python.datetime.datetime@1"

        float_cells = [cell for cell in incidence.iter_cells(2) if cell.variable_name == "score"]
        assert [cell.raw_value for cell in float_cells] == [1.5, -2.25]
        assert all(type(cell.raw_value) is float for cell in float_cells)
        assert [CODEC.encode(cell.raw_value)["bits"] for cell in float_cells] == [
            struct.pack(">d", 1.5).hex(),
            struct.pack(">d", -2.25).hex(),
        ]

        seam = _pinned_seam()
        rows = list(seam.iter_source_native_rows(incidence, batch_size=2))
        datetime_rows = [
            row for row in rows
            if row.relation == "source_physical_cells"
            and row.payload.get("variable_name") == "dtm"
        ]
        assert len(datetime_rows) == 2
        for row in datetime_rows:
            assert row.payload["raw_value"]["t"] == "opaque"
            assert row.payload["raw_value"]["type_id"] == "python.datetime.datetime@1"
            assert row.payload["raw_value"]["t"] != "str"
    finally:
        incidence.close()


def test_real_datetime_custody_and_wrong_source_tamper_remain_content_bound(tmp_path: pathlib.Path):
    path = _write_frame(tmp_path / "datetime-custody.sav", pyreadstat.write_sav)
    source_sha = _sha(path)
    incidence = decoder.decode_sav(path, expected_source_sha256=source_sha)
    try:
        path.write_bytes(b"tampered after content-bound snapshot acquisition")
        assert _sha(path) != source_sha
        assert incidence.verify_source_identity() == source_sha
        cells = [cell for cell in incidence.iter_cells(2) if cell.variable_name == "dtm"]
        assert len(cells) == 2
        assert all(isinstance(cell.raw_value, R5OpaqueValue) for cell in cells)
    finally:
        incidence.close()
    assert incidence._source_snapshot.access_mode == "CLOSED"

    damaged_path = _write_frame(tmp_path / "datetime-tamper-before.sav", pyreadstat.write_sav)
    damaged_sha = _sha(damaged_path)
    damaged = bytearray(damaged_path.read_bytes())
    damaged[-1] ^= 0x01
    damaged_path.write_bytes(bytes(damaged))
    assert _sha(damaged_path) != damaged_sha
    with pytest.raises(decoder.DecoderError, match="source sha256 mismatch before governed decode"):
        decoder.decode_sav(damaged_path, expected_source_sha256=damaged_sha)


def test_naive_timestamp_and_subclasses_canonicalize_to_exact_carrier():
    fold_one = _NaiveDT(2008, 4, 5, 6, 7, 8, 901234, fold=1)
    timestamp = pd.Timestamp(dt.datetime(2008, 4, 5, 6, 7, 8, 901234, fold=1))
    expected_payload = struct.pack(">HBBBBBIB", 2008, 4, 5, 6, 7, 8, 901234, 1)
    for value in (fold_one, timestamp):
        direct = decoder._physical_value(value)
        carried = opaque_decoder_value(value)
        normalized = normalize_decoder_physical_value([value])[0]
        wrapped = decoder._physical_value(_ItemWrapper(value))
        for observed in (direct, carried, normalized, wrapped):
            assert type(observed) is R5OpaqueValue
            assert observed.type_id == "python.datetime.datetime@1"
            assert observed.payload == expected_payload
            assert CODEC.encode(observed)["t"] == "opaque"
        assert not isinstance(direct, str)
        assert not isinstance(wrapped, str)


def test_naive_date_time_subclasses_and_nested_fold_are_preserved():
    class _NaiveDate(dt.date):
        pass

    class _NaiveTime(dt.time):
        pass

    date_value = _NaiveDate(2008, 4, 5)
    time_value = _NaiveTime(6, 7, 8, 901234, fold=1)
    assert opaque_decoder_value(date_value).payload == struct.pack(">HBB", 2008, 4, 5)
    assert opaque_decoder_value(time_value).payload == struct.pack(">BBBIB", 6, 7, 8, 901234, 1)
    fold_key = dt.date(2009, 1, 2)
    nested = normalize_decoder_physical_value(
        {"date": date_value, "time": [time_value], fold_key: dt.datetime(2008, 4, 5, fold=1)}
    )
    assert nested["date"] == opaque_decoder_value(date_value)
    assert nested["time"][0] == opaque_decoder_value(time_value)
    key = next(k for k in nested if isinstance(k, R5OpaqueValue))
    assert key == opaque_decoder_value(fold_key)
    assert nested[key] == opaque_decoder_value(dt.datetime(2008, 4, 5, fold=1))


def test_recursive_item_chasing_is_not_manufactured_into_a_carrier():
    observed = decoder._physical_value(_ChainWrapper(_ChainWrapper(dt.date(2008, 4, 5))))
    assert not isinstance(observed, R5OpaqueValue)
    assert observed == "2008-04-05"


@pytest.mark.parametrize(
    "value",
    [
        _AwareDT(2008, 4, 5, 6, 7, 8, tzinfo=dt.timezone.utc),
        pd.Timestamp("2008-04-05 06:07:08", tz="UTC"),
    ],
)
def test_aware_datetime_subclasses_and_item_wrappers_refuse_explicitly(value):
    with pytest.raises(R5CodecError, match="separate explicit decoder carrier authority"):
        decoder._physical_value(value)
    with pytest.raises(R5CodecError, match="separate explicit decoder carrier authority"):
        opaque_decoder_value(value)
    with pytest.raises(R5CodecError, match="separate explicit decoder carrier authority"):
        decoder._physical_value(_ItemWrapper(value))
    with pytest.raises(R5CodecError, match="separate explicit decoder carrier authority"):
        normalize_decoder_physical_value([value])


def test_aware_time_subclass_refuses_explicitly():
    class _AwareTime(dt.time):
        pass

    value = _AwareTime(6, 7, 8, tzinfo=dt.timezone.utc)
    with pytest.raises(R5CodecError, match="separate explicit decoder carrier authority"):
        decoder._physical_value(value)
    with pytest.raises(R5CodecError, match="separate explicit decoder carrier authority"):
        decoder._physical_value(_ItemWrapper(value))


def test_lossy_date_like_subclasses_refuse_before_any_string_fallback():
    class _BrokenTzinfo(dt.datetime):
        @property
        def tzinfo(self):
            raise RuntimeError("hostile tzinfo")

    class _BrokenCivilField(dt.datetime):
        @property
        def year(self):
            raise RuntimeError("hostile civil field")

    with pytest.raises(R5CodecError, match="sub-microsecond precision"):
        decoder._physical_value(pd.Timestamp("2008-04-05 06:07:08.123456789"))
    with pytest.raises(R5CodecError, match="cannot be safely canonicalized"):
        decoder._physical_value(pd.NaT)
    with pytest.raises(R5CodecError, match="cannot be safely canonicalized"):
        decoder._physical_value(_ItemWrapper(pd.NaT))
    with pytest.raises(R5CodecError, match="cannot expose tzinfo safely"):
        decoder._physical_value(_BrokenTzinfo(2008, 4, 5, 6, 7, 8))
    with pytest.raises(R5CodecError, match="cannot be safely canonicalized"):
        decoder._physical_value(_BrokenCivilField(2008, 4, 5, 6, 7, 8))


def test_opaque_datetime_range_declaration_refuses_with_typed_decoder_error():
    opaque = opaque_decoder_value(dt.datetime(2008, 4, 5, 6, 7, 8))
    with pytest.raises(decoder.DecoderError, match="declared missing range") as exc_info:
        decoder.classify_physical_value(opaque, ({"kind": "range", "lo": 1, "hi": 2},))
    assert not isinstance(exc_info.value, TypeError)
    assert "R5OpaqueValue" in str(exc_info.value)


def test_private_physical_value_is_not_exported_but_public_classifier_remains():
    assert "_physical_value" not in decoder.__all__
    assert "classify_physical_value" in decoder.__all__
