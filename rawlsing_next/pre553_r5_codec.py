"""Exact versioned typed-value codec for the PRE553 R5 shadow carrier.

This module owns physical representation only.  It never infers C11 semantics,
missingness, routing, date/time meaning, labels, or source authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
import datetime as _dt
import base64
import json
import math
import struct
from typing import Any, Mapping


CODEC_VERSION = "PRE553_R5_TYPED_VALUE_CODEC@1.0.0"


class R5CodecError(ValueError):
    pass


@dataclass(frozen=True)
class R5OpaqueValue:
    """Exact escape hatch for a decoder-normalized value not covered by a native lane."""

    type_id: str
    payload: bytes

    def __post_init__(self) -> None:
        if not isinstance(self.type_id, str) or not self.type_id:
            raise R5CodecError("opaque type_id must be a non-empty string")
        if not isinstance(self.payload, bytes):
            raise R5CodecError("opaque payload must be bytes")


def opaque_decoder_value(value: Any) -> R5OpaqueValue:
    """Preserve exact built-in naive decoder date/time objects as opaque bytes only."""
    if type(value) is _dt.datetime:
        if value.tzinfo is not None:
            raise R5CodecError("timezone-aware datetime requires a separate explicit decoder carrier authority")
        payload = struct.pack(
            ">HBBBBBIB",
            value.year, value.month, value.day, value.hour, value.minute,
            value.second, value.microsecond, value.fold,
        )
        return R5OpaqueValue("python.datetime.datetime@1", payload)
    if type(value) is _dt.date:
        return R5OpaqueValue(
            "python.datetime.date@1",
            struct.pack(">HBB", value.year, value.month, value.day),
        )
    if type(value) is _dt.time:
        if value.tzinfo is not None:
            raise R5CodecError("timezone-aware time requires a separate explicit decoder carrier authority")
        payload = struct.pack(
            ">BBBIB", value.hour, value.minute, value.second, value.microsecond, value.fold
        )
        return R5OpaqueValue("python.datetime.time@1", payload)
    raise R5CodecError(f"unsupported opaque decoder value type {type(value).__name__}")


def normalize_decoder_physical_value(value: Any) -> Any:
    """Recursively replace supported decoder date/time objects with opaque carriers."""
    if type(value) in {_dt.datetime, _dt.date, _dt.time}:
        return opaque_decoder_value(value)
    if isinstance(value, tuple):
        return tuple(normalize_decoder_physical_value(v) for v in value)
    if isinstance(value, list):
        return [normalize_decoder_physical_value(v) for v in value]
    if isinstance(value, Mapping):
        return {
            normalize_decoder_physical_value(k): normalize_decoder_physical_value(v)
            for k, v in value.items()
        }
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def canonical_bytes(value: Any) -> bytes:
    return canonical_json(value).encode("ascii")


def _float64_bits(value: float) -> str:
    return struct.pack(">d", value).hex()


def _bits_float64(bits: str) -> float:
    if not isinstance(bits, str) or len(bits) != 16:
        raise R5CodecError("float64 bits must be sixteen hex characters")
    try:
        raw = bytes.fromhex(bits)
    except ValueError as exc:
        raise R5CodecError("invalid float64 bits") from exc
    return struct.unpack(">d", raw)[0]


def _decimal_tuple(value: Decimal) -> dict[str, Any]:
    item = value.as_tuple()
    return {"sign": item.sign, "digits": list(item.digits), "exponent": item.exponent}


def _from_decimal_tuple(item: Mapping[str, Any]) -> Decimal:
    try:
        sign = int(item["sign"])
        digits = tuple(int(x) for x in item["digits"])
        exponent = item["exponent"]
        if isinstance(exponent, str):
            exponent = exponent  # Decimal permits 'F', 'n', 'N' specials in tuple construction.
        else:
            exponent = int(exponent)
        return Decimal((sign, digits, exponent))
    except Exception as exc:
        raise R5CodecError("invalid decimal tuple") from exc


class R5TypedValueCodec:
    """Total inverse for the supported decoder-normalized domain plus opaque escape.

    Python integers are arbitrary precision.  ``inline_integer_bits`` controls only
    the representation lane; values outside it are encoded in an exact escape and
    are never narrowed, wrapped, or sampled for width.
    """

    version = CODEC_VERSION

    def __init__(self, *, inline_integer_bits: int = 63) -> None:
        if not isinstance(inline_integer_bits, int) or isinstance(inline_integer_bits, bool) or inline_integer_bits < 2:
            raise R5CodecError("inline_integer_bits must be an integer >= 2")
        self.inline_integer_bits = inline_integer_bits

    def encode(self, value: Any) -> dict[str, Any]:
        if value is None:
            return {"t": "none"}
        if isinstance(value, bool):
            return {"t": "bool", "v": value}
        if isinstance(value, int):
            tag = "int" if value.bit_length() <= self.inline_integer_bits else "int_escape"
            return {"t": tag, "v": str(value)}
        if isinstance(value, float):
            # At the frozen decoder boundary NaN payload bits may already have been
            # destroyed.  We therefore encode only the decoder-observed NaN state,
            # never fabricate a payload.  Actual text "inf" remains a str lane.
            if math.isnan(value):
                return {"t": "float64_nan_decoder_state"}
            if math.isinf(value):
                return {"t": "float64_pos_inf" if value > 0 else "float64_neg_inf"}
            return {"t": "float64_finite", "bits": _float64_bits(value)}
        if isinstance(value, str):
            # JSON escaping preserves the exact Python Unicode code-point sequence,
            # including empty strings, controls, NULs, and normalization-sensitive text.
            return {"t": "str", "v": value}
        if isinstance(value, bytes):
            return {"t": "bytes", "b64": base64.b64encode(value).decode("ascii")}
        if isinstance(value, Decimal):
            return {"t": "decimal", "v": _decimal_tuple(value)}
        if isinstance(value, R5OpaqueValue):
            return {"t": "opaque", "type_id": value.type_id,
                    "b64": base64.b64encode(value.payload).decode("ascii")}
        # Date/time objects are intentionally NOT interpreted from display formats.
        # A source-authorized native date/time may cross this seam only as an opaque
        # exact decoder value with an explicit type id.
        import datetime as _dt
        if isinstance(value, (_dt.date, _dt.time, _dt.datetime)):
            raise R5CodecError("date/time meaning may not be invented by the R5 codec; use an explicit opaque decoder value")
        if isinstance(value, tuple):
            return {"t": "tuple", "v": [self.encode(v) for v in value]}
        if isinstance(value, list):
            return {"t": "list", "v": [self.encode(v) for v in value]}
        if isinstance(value, Mapping):
            items = [(self.encode(k), self.encode(v)) for k, v in value.items()]
            items.sort(key=lambda kv: canonical_bytes(kv[0]))
            return {"t": "map", "v": [[k, v] for k, v in items]}
        raise R5CodecError(f"unsupported value type {type(value).__name__}; explicit R5OpaqueValue escape required")

    def decode(self, encoded: Mapping[str, Any]) -> Any:
        if not isinstance(encoded, Mapping):
            raise R5CodecError("encoded value must be a mapping")
        tag = encoded.get("t")
        if tag == "none":
            return None
        if tag == "bool":
            value = encoded.get("v")
            if not isinstance(value, bool):
                raise R5CodecError("invalid bool payload")
            return value
        if tag in {"int", "int_escape"}:
            value = encoded.get("v")
            if not isinstance(value, str):
                raise R5CodecError("invalid integer payload")
            try:
                result = int(value, 10)
            except ValueError as exc:
                raise R5CodecError("invalid integer payload") from exc
            if str(result) != value and not (value == "-0" and result == 0):
                raise R5CodecError("noncanonical integer payload")
            return result
        if tag == "float64_finite":
            value = _bits_float64(encoded.get("bits"))
            if not math.isfinite(value):
                raise R5CodecError("finite float lane contains non-finite payload")
            return value
        if tag == "float64_nan_decoder_state":
            return float("nan")
        if tag == "float64_pos_inf":
            return float("inf")
        if tag == "float64_neg_inf":
            return float("-inf")
        if tag == "str":
            value = encoded.get("v")
            if not isinstance(value, str):
                raise R5CodecError("invalid str payload")
            return value
        if tag == "bytes":
            try:
                return base64.b64decode(encoded.get("b64"), validate=True)
            except Exception as exc:
                raise R5CodecError("invalid bytes payload") from exc
        if tag == "decimal":
            return _from_decimal_tuple(encoded.get("v"))
        if tag == "opaque":
            try:
                return R5OpaqueValue(str(encoded["type_id"]), base64.b64decode(encoded["b64"], validate=True))
            except Exception as exc:
                raise R5CodecError("invalid opaque payload") from exc
        if tag == "tuple":
            return tuple(self.decode(v) for v in encoded.get("v", ()))
        if tag == "list":
            return [self.decode(v) for v in encoded.get("v", ())]
        if tag == "map":
            result = {}
            previous = None
            for pair in encoded.get("v", ()):
                if not isinstance(pair, list) or len(pair) != 2:
                    raise R5CodecError("invalid map entry")
                key_encoded, value_encoded = pair
                key_sort = canonical_bytes(key_encoded)
                if previous is not None and key_sort <= previous:
                    raise R5CodecError("map entries must be strictly canonical-sorted")
                previous = key_sort
                key = self.decode(key_encoded)
                try:
                    if key in result:
                        raise R5CodecError("decoded map key collision")
                    result[key] = self.decode(value_encoded)
                except TypeError as exc:
                    raise R5CodecError("decoded map key is unhashable") from exc
            return result
        raise R5CodecError(f"unknown codec tag {tag!r}")

    def typed_key(self, value: Any) -> bytes:
        """Equality key that never conflates bool/int/float/str host-language equality."""
        return canonical_bytes(self.encode(value))

    def roundtrip_equal(self, value: Any) -> bool:
        encoded = self.encode(value)
        decoded = self.decode(encoded)
        if isinstance(value, float):
            if math.isnan(value):
                return math.isnan(decoded)
            return _float64_bits(value) == _float64_bits(decoded)
        return type(value) is type(decoded) and value == decoded


__all__ = [
    "CODEC_VERSION", "R5CodecError", "R5OpaqueValue", "R5TypedValueCodec",
    "opaque_decoder_value", "normalize_decoder_physical_value",
    "canonical_json", "canonical_bytes",
]
