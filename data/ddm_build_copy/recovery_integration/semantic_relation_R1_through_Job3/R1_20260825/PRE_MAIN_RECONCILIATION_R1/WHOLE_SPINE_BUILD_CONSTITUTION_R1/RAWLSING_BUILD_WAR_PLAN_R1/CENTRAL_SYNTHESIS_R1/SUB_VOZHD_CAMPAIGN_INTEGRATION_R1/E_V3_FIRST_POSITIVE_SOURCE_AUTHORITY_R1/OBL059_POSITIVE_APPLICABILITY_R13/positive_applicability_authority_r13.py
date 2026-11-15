"""OBL059 R13 canonical-input boundary.

The OBL059 decision layer accepts only an explicit immutable canonical built-in
packet. Arbitrary Mapping objects are representation inputs for an upstream
adapter, not direct positive-authoritative inputs to this decision function.

Once a canonical packet reaches ``evaluate_direct_positive_applicability``, all
input traversal is over exact tuples and exact built-in values only. The
canonical packet is thawed into exact dictionaries and then evaluated by the
previously proven exact-dict applicability core.

The optional adapter in this module is an explicit representation boundary for
producer/source fixtures. The decision function never calls it and therefore
never traverses caller-defined Mapping methods.
"""
from __future__ import annotations

import importlib.util
import struct
from collections.abc import Mapping as ABCMapping
from pathlib import Path
from typing import Any

_R12_PATH = (
    Path(__file__).resolve().parents[1]
    / "OBL059_POSITIVE_APPLICABILITY_R12"
    / "positive_applicability_authority_r12.py"
)
_spec = importlib.util.spec_from_file_location("_obl059_r12_authority_for_r13", _R12_PATH)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"cannot load frozen OBL059 R12 authority: {_R12_PATH}")
_r12 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_r12)

AUTHORITY_ID = _r12.AUTHORITY_ID
RECEIPT_VERSION = _r12.RECEIPT_VERSION
FIRST_CANARY_SUBJECT_ID = _r12.FIRST_CANARY_SUBJECT_ID
SUBJECT_CLASSIFICATION_PREDICATE = _r12.SUBJECT_CLASSIFICATION_PREDICATE
ADP007_OWNER = _r12.ADP007_OWNER
ADP008_OWNER = _r12.ADP008_OWNER
ADP010_CONSUMER = _r12.ADP010_CONSUMER
SYNTHETIC_SCOPE = _r12.SYNTHETIC_SCOPE
POSITIVE_DECISION = _r12.POSITIVE_DECISION
NEGATIVE_DECISION = _r12.NEGATIVE_DECISION
FORBIDDEN_ALIAS_AUTHORITIES = _r12.FORBIDDEN_ALIAS_AUTHORITIES

R13_CANDIDATE_REVISION = "OBL059_POSITIVE_APPLICABILITY_CANONICAL_INPUT_BOUNDARY_R13"
CANONICAL_SCHEMA = "OBL059_CANONICAL_POSITIVE_APPLICABILITY_PACKET@R13"

_REQUIRED_TOP_LEVEL = (
    "execution_scope",
    "actor_id",
    "subject_id",
    "world_id",
    "time_id",
    "adp010_opportunity_id",
    "opportunity",
    "evidence",
)
_EVIDENCE_COMPONENT_KEYS = (
    "subject_classification",
    "actor_activation",
    "developmental_phase",
)
_MAX_DEPTH = 128
_MAX_ITEMS = 16384

# Exposed as a seam for the governed court's programmer-error visibility check.
_evaluate_prepared = _r12._r11._r10._r9._evaluate_prepared


class CanonicalizationError(ValueError):
    pass


def _malformed_receipt():
    return _r12._r11._r10._r9._r7._existing_packet_malformed_receipt()


def _freeze_exact(value: Any, depth: int = 0) -> tuple:
    if depth > _MAX_DEPTH:
        raise CanonicalizationError("canonical depth exceeded")
    t = type(value)
    if value is None:
        return ("N",)
    if t is bool:
        return ("Q", value)
    if t is str:
        return ("S", value)
    if t is int:
        magnitude = value if value >= 0 else -value
        bits = int.bit_length(magnitude)
        raw = int.to_bytes(magnitude, max(1, (bits + 7) // 8), "big", signed=False)
        return ("I", -1 if value < 0 else 1, raw.hex())
    if t is float:
        return ("F", struct.pack("!d", value).hex())
    if t is bytes:
        return ("B", value.hex())
    if t is dict:
        if len(value) > _MAX_ITEMS:
            raise CanonicalizationError("canonical breadth exceeded")
        entries = []
        for key, item in dict.items(value):
            if type(key) is not str:
                raise CanonicalizationError("canonical dictionary key is not exact str")
            entries.append((key, _freeze_exact(item, depth + 1)))
        entries.sort(key=lambda pair: pair[0])
        return ("D", tuple(entries))
    if t is list:
        if len(value) > _MAX_ITEMS:
            raise CanonicalizationError("canonical breadth exceeded")
        return ("L", tuple(_freeze_exact(item, depth + 1) for item in list.__iter__(value)))
    if t is tuple:
        if len(value) > _MAX_ITEMS:
            raise CanonicalizationError("canonical breadth exceeded")
        return ("T", tuple(_freeze_exact(item, depth + 1) for item in tuple.__iter__(value)))
    raise CanonicalizationError("unsupported canonical value type")


def _thaw_exact(token: Any, depth: int = 0) -> Any:
    if depth > _MAX_DEPTH or type(token) is not tuple or not token:
        raise CanonicalizationError("invalid canonical token")
    tag = tuple.__getitem__(token, 0)
    if type(tag) is not str:
        raise CanonicalizationError("invalid canonical tag")
    if tag == "N" and len(token) == 1:
        return None
    if tag == "Q" and len(token) == 2 and type(token[1]) is bool:
        return token[1]
    if tag == "S" and len(token) == 2 and type(token[1]) is str:
        return token[1]
    if tag == "I" and len(token) == 3 and type(token[1]) is int and type(token[2]) is str:
        if token[1] not in (-1, 1):
            raise CanonicalizationError("invalid integer sign")
        try:
            magnitude = int.from_bytes(bytes.fromhex(token[2]), "big", signed=False)
        except Exception as exc:
            raise CanonicalizationError("invalid integer encoding") from exc
        return -magnitude if token[1] < 0 else magnitude
    if tag == "F" and len(token) == 2 and type(token[1]) is str:
        try:
            return struct.unpack("!d", bytes.fromhex(token[1]))[0]
        except Exception as exc:
            raise CanonicalizationError("invalid float encoding") from exc
    if tag == "B" and len(token) == 2 and type(token[1]) is str:
        try:
            return bytes.fromhex(token[1])
        except Exception as exc:
            raise CanonicalizationError("invalid bytes encoding") from exc
    if tag == "D" and len(token) == 2 and type(token[1]) is tuple:
        if len(token[1]) > _MAX_ITEMS:
            raise CanonicalizationError("canonical breadth exceeded")
        out = {}
        for entry in tuple.__iter__(token[1]):
            if type(entry) is not tuple or len(entry) != 2 or type(entry[0]) is not str:
                raise CanonicalizationError("invalid canonical dictionary entry")
            key = entry[0]
            if dict.__contains__(out, key):
                raise CanonicalizationError("duplicate canonical dictionary key")
            dict.__setitem__(out, key, _thaw_exact(entry[1], depth + 1))
        return out
    if tag in ("L", "T") and len(token) == 2 and type(token[1]) is tuple:
        if len(token[1]) > _MAX_ITEMS:
            raise CanonicalizationError("canonical breadth exceeded")
        values = tuple(_thaw_exact(item, depth + 1) for item in tuple.__iter__(token[1]))
        return list(values) if tag == "L" else values
    raise CanonicalizationError("unknown or malformed canonical token")


def _validate_exact_packet_shape(packet: Any) -> bool:
    if type(packet) is not dict:
        return False
    for key in _REQUIRED_TOP_LEVEL:
        if not dict.__contains__(packet, key):
            return False
    opportunity = dict.__getitem__(packet, "opportunity")
    evidence = dict.__getitem__(packet, "evidence")
    if type(opportunity) is not dict or type(evidence) is not dict:
        return False
    for key in _EVIDENCE_COMPONENT_KEYS:
        if not dict.__contains__(evidence, key):
            return False
        if type(dict.__getitem__(evidence, key)) is not dict:
            return False
    return True


def canonicalize_exact_packet(packet: dict[str, Any]) -> tuple | None:
    """Canonicalize an already exact built-in semantic packet.

    This is the narrowest canonical producer: no custom Mapping traversal is
    performed here. Returns ``None`` for malformed/non-exact input.
    """
    if not _validate_exact_packet_shape(packet):
        return None
    try:
        frozen = _freeze_exact(packet)
    except CanonicalizationError:
        return None
    return (CANONICAL_SCHEMA, frozen)


def _materialize_source(value: Any, active: set[int], depth: int = 0) -> Any:
    """Upstream/source-side representation adapter helper.

    This function is intentionally outside the decision boundary. Source owners
    are responsible for the semantic meaning of representations passed here.
    """
    if depth > _MAX_DEPTH:
        raise CanonicalizationError("adapter depth exceeded")
    t = type(value)
    if value is None or t in (bool, str, int, float, bytes):
        return value
    marker = id(value)
    if marker in active:
        raise CanonicalizationError("adapter cycle")
    if isinstance(value, ABCMapping):
        active.add(marker)
        try:
            materialized = dict(value)
            if len(materialized) > _MAX_ITEMS:
                raise CanonicalizationError("adapter breadth exceeded")
            out = {}
            for key, item in dict.items(materialized):
                if type(key) is not str:
                    raise CanonicalizationError("adapter key is not exact str")
                out[key] = _materialize_source(item, active, depth + 1)
            return out
        finally:
            active.remove(marker)
    if t is list:
        active.add(marker)
        try:
            return [_materialize_source(item, active, depth + 1) for item in list.__iter__(value)]
        finally:
            active.remove(marker)
    if t is tuple:
        active.add(marker)
        try:
            return tuple(_materialize_source(item, active, depth + 1) for item in tuple.__iter__(value))
        finally:
            active.remove(marker)
    raise CanonicalizationError("unsupported adapter value type")


def adapt_source_mapping_to_canonical(source: Any) -> tuple | None:
    """Explicit upstream representation adapter.

    The OBL059 decision function never invokes this function. A source-specific
    caller may use it to convert a lawful representation into the canonical
    packet contract before calling the decision layer.
    """
    try:
        materialized = _materialize_source(source, set())
    except BaseException:
        return None
    if type(materialized) is not dict:
        return None
    return canonicalize_exact_packet(materialized)


def evaluate_direct_positive_applicability(canonical_packet: Any):
    """Evaluate OBL059 only from the explicit immutable R13 canonical packet."""
    # Mechanically distinguish the authority boundary before any caller-defined
    # protocol can be consulted. Raw dicts and all custom Mapping objects are not
    # direct decision inputs.
    if type(canonical_packet) is not tuple or len(canonical_packet) != 2:
        return _malformed_receipt()
    schema = tuple.__getitem__(canonical_packet, 0)
    payload = tuple.__getitem__(canonical_packet, 1)
    if type(schema) is not str or schema != CANONICAL_SCHEMA or type(payload) is not tuple:
        return _malformed_receipt()
    try:
        prepared = _thaw_exact(payload)
    except CanonicalizationError:
        return _malformed_receipt()
    if not _validate_exact_packet_shape(prepared):
        return _malformed_receipt()
    return _evaluate_prepared(prepared)
