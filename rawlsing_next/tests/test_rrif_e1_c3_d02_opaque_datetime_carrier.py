from __future__ import annotations

import datetime as dt
import struct

import pytest

from rawlsing_next import pre553_physical_decoder as decoder
from rawlsing_next.pre553_physical_decoder import PhysicalMissingState
from rawlsing_next.pre553_r5_codec import (
    R5CodecError,
    R5OpaqueValue,
    R5TypedValueCodec,
    normalize_decoder_physical_value,
    opaque_decoder_value,
)
from rawlsing_next.pre553_source_backed_c11_facade import physical_value_binding_key


R5 = R5TypedValueCodec()
D01_DECLARED_SHA = "ac0b8bc1ddb2fa6b952417e35b6379ce6a2cf8596776a43282ba44f48e0ae1a2"


class _ItemWrapper:
    def __init__(self, value):
        self._value = value

    def item(self):
        return self._value


class _ChainWrapper:
    def __init__(self, value):
        self._value = value

    def item(self):
        return self._value


@pytest.mark.parametrize(
    "value,type_id",
    [
        (dt.date(2008, 4, 5), "python.datetime.date@1"),
        (dt.time(6, 7, 8, 901234, fold=1), "python.datetime.time@1"),
        (dt.datetime(2008, 4, 5, 6, 7, 8, 901234, fold=1), "python.datetime.datetime@1"),
    ],
)
def test_exact_naive_builtin_types_require_explicit_opaque_carrier(value, type_id):
    with pytest.raises(R5CodecError, match="date/time meaning may not be invented"):
        R5.encode(value)
    opaque = opaque_decoder_value(value)
    assert type(opaque) is R5OpaqueValue
    assert opaque.type_id == type_id
    encoded = R5.encode(opaque)
    assert encoded["t"] == "opaque"
    assert encoded["type_id"] == type_id
    assert R5.decode(encoded) == opaque
    assert str(value).encode() != opaque.payload


def test_carrier_payload_and_fold_are_exact():
    date_value = dt.date(2008, 4, 5)
    time_value = dt.time(6, 7, 8, 901234, fold=1)
    datetime_value = dt.datetime(2008, 4, 5, 6, 7, 8, 901234, fold=1)
    assert struct.unpack(">HBB", opaque_decoder_value(date_value).payload) == (2008, 4, 5)
    assert struct.unpack(">BBBIB", opaque_decoder_value(time_value).payload) == (6, 7, 8, 901234, 1)
    assert struct.unpack(">HBBBBBIB", opaque_decoder_value(datetime_value).payload) == (
        2008, 4, 5, 6, 7, 8, 901234, 1,
    )
    assert opaque_decoder_value(dt.time(6, 7, 8, fold=0)) != opaque_decoder_value(dt.time(6, 7, 8, fold=1))
    assert opaque_decoder_value(dt.datetime(2008, 4, 5, fold=0)) != opaque_decoder_value(dt.datetime(2008, 4, 5, fold=1))


def test_carrier_is_exact_type_and_field_sensitive():
    a = opaque_decoder_value(dt.datetime(2008, 4, 5, 6, 7, 8, 1))
    b = opaque_decoder_value(dt.datetime(2008, 4, 5, 6, 7, 8, 2))
    c = opaque_decoder_value(dt.date(2008, 4, 5))
    assert a != b
    assert a.type_id != c.type_id
    assert R5.typed_key(a) != R5.typed_key(b)
    assert R5.typed_key(a) != R5.typed_key(c)


def test_nested_physical_normalization_preserves_opaque_types_without_semantics():
    value = (
        {"metadata": [dt.datetime(2008, 1, 2, 3, 4, 5), {"date": dt.date(2008, 1, 2)}]},
        [dt.time(6, 7, 8, fold=1)],
        {dt.date(2009, 3, 4): dt.datetime(2009, 3, 4, 5, 6, 7, fold=1)},
    )
    normalized = normalize_decoder_physical_value(value)
    assert isinstance(normalized[0]["metadata"][0], R5OpaqueValue)
    assert isinstance(normalized[0]["metadata"][1]["date"], R5OpaqueValue)
    assert isinstance(normalized[1][0], R5OpaqueValue)
    key = next(iter(normalized[2]))
    assert isinstance(key, R5OpaqueValue)
    assert isinstance(normalized[2][key], R5OpaqueValue)
    assert R5.encode(normalized)["t"] == "tuple"
    assert R5.decode(R5.encode(normalized)) == normalized


def test_current_decoder_routes_direct_and_item_unwrapped_naive_values_only():
    direct = decoder._physical_value(dt.datetime(2008, 4, 5, 6, 7, 8))
    wrapped = decoder._physical_value(_ItemWrapper(dt.date(2008, 4, 5)))
    assert isinstance(direct, R5OpaqueValue)
    assert isinstance(wrapped, R5OpaqueValue)
    assert not isinstance(direct, str)
    assert not isinstance(wrapped, str)
    assert R5.encode(direct)["t"] == "opaque"
    assert R5.encode(wrapped)["t"] == "opaque"


@pytest.mark.parametrize(
    "value",
    [
        dt.datetime(2008, 4, 5, tzinfo=dt.timezone.utc),
        dt.time(6, 7, tzinfo=dt.timezone.utc),
    ],
)
def test_timezone_aware_values_fail_closed_at_carrier_and_decoder_route(value):
    with pytest.raises(R5CodecError, match="separate explicit decoder carrier authority"):
        opaque_decoder_value(value)
    with pytest.raises(R5CodecError, match="separate explicit decoder carrier authority"):
        decoder._physical_value(value)


@pytest.mark.parametrize(
    "value",
    [
        dt.datetime(2008, 4, 5, tzinfo=dt.timezone.utc),
        dt.time(6, 7, tzinfo=dt.timezone.utc),
    ],
)
def test_item_unwrapped_timezone_aware_values_fail_closed(value):
    wrapped = _ItemWrapper(value)
    with pytest.raises(R5CodecError, match="separate explicit decoder carrier authority"):
        decoder._physical_value(wrapped)


def test_fault_date_as_string_is_not_reinterpreted_as_date():
    texts = ("2008-04-05", "06:07:08", "2008-04-05T06:07:08", "2008/04/05")
    for text in texts:
        assert normalize_decoder_physical_value(text) == text
        assert decoder._physical_value(text) == text
        assert R5.encode(text)["t"] == "str"
        assert not isinstance(decoder._physical_value(text), R5OpaqueValue)
    date_key = opaque_decoder_value(dt.date(2008, 4, 5))
    assert physical_value_binding_key(
        "2008-04-05", PhysicalMissingState.OBSERVED_STORAGE_VALUE
    ) != physical_value_binding_key(
        date_key, PhysicalMissingState.OBSERVED_STORAGE_VALUE
    )


def test_fault_recursive_item_unwrapping_does_not_manufacture_opaque_carrier():
    wrapped = _ChainWrapper(_ChainWrapper(dt.date(2008, 4, 5)))
    observed = decoder._physical_value(wrapped)
    assert not isinstance(observed, R5OpaqueValue)
    assert observed == "2008-04-05"


def test_fault_codec_normalization_does_not_expand_item_wrappers():
    wrapped = _ItemWrapper(dt.date(2008, 4, 5))
    assert normalize_decoder_physical_value(wrapped) is wrapped
    nested = normalize_decoder_physical_value([wrapped])
    assert nested[0] is wrapped
    assert not isinstance(nested[0], R5OpaqueValue)


def test_fault_original_current_jsonable_and_scalar_lanes_are_unchanged():
    assert decoder._jsonable(dt.date(2008, 4, 5)) == "2008-04-05"
    assert decoder._physical_value(None) is None
    assert decoder._physical_value(True) is True
    assert decoder._physical_value(7) == 7
    assert decoder._physical_value(1.5) == 1.5
    assert decoder._physical_value("2008-04-05") == "2008-04-05"
    assert decoder._physical_value((1, "a")) == [1, "a"]
    assert decoder._physical_value({"a": 1}) == {"a": 1}
    assert R5.encode(1) != R5.encode(1.0)
    assert R5.encode(True) != R5.encode(1)
    with pytest.raises(R5CodecError, match="date/time meaning may not be invented"):
        R5.encode(dt.date(2008, 4, 5))


def test_string_masquerade_and_unrelated_scalar_lanes_remain_distinct():
    text = "2008-04-05"
    assert normalize_decoder_physical_value(text) == text
    assert decoder._physical_value(text) == text
    assert R5.encode(text)["t"] == "str"
    assert normalize_decoder_physical_value(1) == 1
    assert normalize_decoder_physical_value(1.0) == 1.0
    assert R5.encode(1) != R5.encode(1.0)
    assert physical_value_binding_key(
        text, PhysicalMissingState.OBSERVED_STORAGE_VALUE
    ) != physical_value_binding_key(
        opaque_decoder_value(dt.date(2008, 4, 5)),
        PhysicalMissingState.OBSERVED_STORAGE_VALUE,
    )


def test_unchanged_facade_can_bind_opaque_decoder_carrier_directly():
    opaque_a = opaque_decoder_value(dt.datetime(2008, 4, 5, 6, 7, 8, 1))
    opaque_b = opaque_decoder_value(dt.datetime(2008, 4, 5, 6, 7, 8, 2))
    key_a = physical_value_binding_key(opaque_a, PhysicalMissingState.OBSERVED_STORAGE_VALUE)
    key_b = physical_value_binding_key(opaque_b, PhysicalMissingState.OBSERVED_STORAGE_VALUE)
    assert len(key_a) == 64
    assert len(key_b) == 64
    assert key_a != key_b


def test_d01_and_d02_compose_on_the_same_current_decoder_without_cross_authority():
    config = decoder._compatibility_config(D01_DECLARED_SHA, "BIG5")
    physical = decoder._physical_value(dt.datetime(2008, 4, 5, 6, 7, 8))
    assert config == {
        "encoding": "BIG5",
        "authority_status": decoder.SOURCE_DECLARED_ENCODING_ONLY,
    }
    assert isinstance(physical, R5OpaqueValue)
    assert "PHYSICAL_DECODING_ONLY" in config["authority_status"]
    with pytest.raises(decoder.DecoderError):
        decoder._compatibility_config(D01_DECLARED_SHA, "WINDOWS-1252")
