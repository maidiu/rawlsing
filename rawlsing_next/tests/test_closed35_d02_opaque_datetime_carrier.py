from __future__ import annotations

import datetime as dt

import pytest

from rawlsing_next import closed35_representation_census_harness as census
from rawlsing_next import pre553_physical_decoder as decoder
from rawlsing_next.pre553_r5_codec import (
    R5CodecError,
    R5OpaqueValue,
    R5TypedValueCodec,
    normalize_decoder_physical_value,
    opaque_decoder_value,
)


R5 = R5TypedValueCodec()


@pytest.mark.parametrize(
    "value,type_id",
    [
        (dt.date(2008, 4, 5), "python.datetime.date@1"),
        (dt.time(6, 7, 8, 901234, fold=1), "python.datetime.time@1"),
        (dt.datetime(2008, 4, 5, 6, 7, 8, 901234, fold=1), "python.datetime.datetime@1"),
    ],
)
def test_datetime_objects_require_explicit_opaque_decoder_carrier(value, type_id):
    with pytest.raises(R5CodecError, match="date/time meaning may not be invented"):
        R5.encode(value)
    opaque = opaque_decoder_value(value)
    assert isinstance(opaque, R5OpaqueValue)
    assert opaque.type_id == type_id
    encoded = R5.encode(opaque)
    assert encoded["t"] == "opaque"
    assert encoded["type_id"] == type_id
    assert R5.decode(encoded) == opaque
    assert str(value).encode() != opaque.payload


def test_datetime_carrier_is_exact_type_and_field_sensitive():
    a = opaque_decoder_value(dt.datetime(2008, 4, 5, 6, 7, 8, 1))
    b = opaque_decoder_value(dt.datetime(2008, 4, 5, 6, 7, 8, 2))
    c = opaque_decoder_value(dt.date(2008, 4, 5))
    assert a != b
    assert a.type_id != c.type_id
    assert R5.typed_key(a) != R5.typed_key(b)
    assert R5.typed_key(a) != R5.typed_key(c)


def test_nested_decoder_metadata_normalization_preserves_opaque_type():
    value = {
        "metadata": [
            dt.datetime(2008, 1, 2, 3, 4, 5),
            {"date": dt.date(2008, 1, 2)},
        ]
    }
    normalized = normalize_decoder_physical_value(value)
    assert isinstance(normalized["metadata"][0], R5OpaqueValue)
    assert isinstance(normalized["metadata"][1]["date"], R5OpaqueValue)
    encoded = R5.encode(normalized)
    assert encoded["t"] == "map"
    # The census metadata fingerprint seam must now accept the same structure.
    assert len(census._typed_r5_digest(value)) == 64


def test_physical_decoder_does_not_convenience_stringify_datetime():
    value = dt.datetime(2008, 4, 5, 6, 7, 8)
    physical = decoder._physical_value(value)
    assert isinstance(physical, R5OpaqueValue)
    assert not isinstance(physical, str)
    assert R5.encode(physical)["t"] == "opaque"


@pytest.mark.parametrize(
    "value",
    [
        dt.datetime(2008, 4, 5, tzinfo=dt.timezone.utc),
        dt.time(6, 7, tzinfo=dt.timezone.utc),
    ],
)
def test_timezone_aware_values_fail_closed_pending_separate_authority(value):
    with pytest.raises(R5CodecError, match="separate explicit decoder carrier authority"):
        opaque_decoder_value(value)


def test_unrelated_scalar_lanes_are_unchanged():
    assert normalize_decoder_physical_value(1) == 1
    assert normalize_decoder_physical_value(1.0) == 1.0
    assert normalize_decoder_physical_value("2008-04-05") == "2008-04-05"
    assert R5.encode(1) != R5.encode(1.0)
