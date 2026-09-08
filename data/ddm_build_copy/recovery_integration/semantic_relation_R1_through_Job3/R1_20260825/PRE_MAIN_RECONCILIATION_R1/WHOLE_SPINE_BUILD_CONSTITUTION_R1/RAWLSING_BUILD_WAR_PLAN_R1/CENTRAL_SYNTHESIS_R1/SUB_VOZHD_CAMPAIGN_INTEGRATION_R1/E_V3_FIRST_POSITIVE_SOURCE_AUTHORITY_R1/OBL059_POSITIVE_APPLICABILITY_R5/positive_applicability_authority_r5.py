"""OBL059 R5 bounded repair: exact large-integer malformed receipt closure.

R5 preserves frozen R4 behavior for ordinary inputs. It changes only the
malformed-required-binding diagnostic boundary when an exact built-in integer
cannot be safely rendered by the runtime's configured decimal conversion
limit used by canonical JSON encoding.

The decision uses integer-only structural operations. Oversized malformed
integers are projected to a bounded JSON-safe diagnostic containing sign,
bit length, and a SHA-256 digest of the exact binary magnitude; the decimal
integer itself is never rendered. No project-current state or runtime effect
is created.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Mapping, Set

_R4_PATH = (
    Path(__file__).resolve().parents[1]
    / "OBL059_POSITIVE_APPLICABILITY_R4"
    / "positive_applicability_authority_r4.py"
)
_spec = importlib.util.spec_from_file_location("_obl059_r4_authority_for_r5", _R4_PATH)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"cannot load frozen OBL059 R4 authority: {_R4_PATH}")
_r4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_r4)

AUTHORITY_ID = _r4.AUTHORITY_ID
RECEIPT_VERSION = _r4.RECEIPT_VERSION
FIRST_CANARY_SUBJECT_ID = _r4.FIRST_CANARY_SUBJECT_ID
SUBJECT_CLASSIFICATION_PREDICATE = _r4.SUBJECT_CLASSIFICATION_PREDICATE
ADP007_OWNER = _r4.ADP007_OWNER
ADP008_OWNER = _r4.ADP008_OWNER
ADP010_CONSUMER = _r4.ADP010_CONSUMER
SYNTHETIC_SCOPE = _r4.SYNTHETIC_SCOPE
POSITIVE_DECISION = _r4.POSITIVE_DECISION
NEGATIVE_DECISION = _r4.NEGATIVE_DECISION
FORBIDDEN_ALIAS_AUTHORITIES = _r4.FORBIDDEN_ALIAS_AUTHORITIES
_REQUIRED_BINDINGS = tuple(_r4._REQUIRED_BINDINGS)

R5_CANDIDATE_REVISION = "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R5"
_PROJECTION_MAX_DEPTH = _r4._PROJECTION_MAX_DEPTH
_SAFE_SCAN_MAX_DEPTH = _r4._SAFE_SCAN_MAX_DEPTH


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


@lru_cache(maxsize=8)
def _decimal_safe_threshold(limit: int) -> int | None:
    """Return 10**limit without decimal conversion; None means unlimited."""
    if limit == 0:
        return None
    return 10 ** limit


def _exact_int_decimal_conversion_safe(value: int) -> bool:
    """Whether an exact int is within the runtime decimal rendering ceiling."""
    if type(value) is not int:
        raise TypeError("exact int required")
    limit = sys.get_int_max_str_digits()
    threshold = _decimal_safe_threshold(limit)
    if threshold is None:
        return True
    return -threshold < value < threshold


def _is_exact_json_primitive(value: Any) -> bool:
    value_type = type(value)
    if value_type is int:
        return _exact_int_decimal_conversion_safe(value)
    return value_type in (type(None), str, bool, float)


def _binary_magnitude_sha256(value: int) -> str:
    """Digest an exact integer magnitude in binary, never in decimal."""
    if type(value) is not int:
        raise TypeError("exact int required")
    magnitude = value if value >= 0 else -value
    bit_length = int.bit_length(magnitude)
    byte_length = max(1, (bit_length + 7) // 8)
    payload = int.to_bytes(magnitude, byte_length, "big", signed=False)
    return hashlib.sha256(payload).hexdigest()


def _project_oversized_int(value: int) -> Dict[str, Any]:
    return {
        "__non_json_int__": "decimal_conversion_limit_exceeded",
        "sign": -1 if value < 0 else 1,
        "bit_length": int.bit_length(value),
        "binary_magnitude_sha256": _binary_magnitude_sha256(value),
    }


def _structurally_json_safe(
    value: Any,
    *,
    active_ids: Set[int] | None = None,
    depth: int = 0,
) -> bool:
    """R4 exact-built-in scan plus exact-int decimal-rendering safety."""
    if _is_exact_json_primitive(value):
        return True

    if type(value) is int:
        return False

    if depth >= _SAFE_SCAN_MAX_DEPTH:
        return False

    if active_ids is None:
        active_ids = set()

    value_type = type(value)
    if value_type not in (dict, list, tuple):
        return False

    marker = id(value)
    if marker in active_ids:
        return False

    active_ids.add(marker)
    try:
        if value_type is dict:
            for key, item in dict.items(value):
                key_type = type(key)
                if key_type is int:
                    if not _exact_int_decimal_conversion_safe(key):
                        return False
                elif key_type not in (str, float, bool, type(None)):
                    return False
                if not _structurally_json_safe(
                    item, active_ids=active_ids, depth=depth + 1
                ):
                    return False
            return True

        iterator = list.__iter__(value) if value_type is list else tuple.__iter__(value)
        for item in iterator:
            if not _structurally_json_safe(
                item, active_ids=active_ids, depth=depth + 1
            ):
                return False
        return True
    finally:
        active_ids.remove(marker)


def _project_total(
    value: Any,
    *,
    active_ids: Set[int] | None = None,
    depth: int = 0,
) -> Any:
    """R4 bounded projection plus safe oversized-int diagnostic projection."""
    if type(value) is int and not _exact_int_decimal_conversion_safe(value):
        return _project_oversized_int(value)

    if _is_exact_json_primitive(value):
        return value

    value_type = type(value)

    if value_type is bytes:
        return {
            "__non_json_type__": "bytes",
            "length": bytes.__len__(value),
            "sha256": hashlib.sha256(value).hexdigest(),
        }

    if depth >= _PROJECTION_MAX_DEPTH:
        return {
            "__projection_depth_limit__": True,
            "max_depth": _PROJECTION_MAX_DEPTH,
        }

    if active_ids is None:
        active_ids = set()

    if value_type in (dict, list, tuple, set, frozenset):
        marker = id(value)
        if marker in active_ids:
            return {"__cycle__": True}

        active_ids.add(marker)
        try:
            if value_type is dict:
                pairs = [
                    [
                        _project_total(key, active_ids=active_ids, depth=depth + 1),
                        _project_total(item, active_ids=active_ids, depth=depth + 1),
                    ]
                    for key, item in dict.items(value)
                ]
                pairs.sort(key=lambda pair: _canonical(pair[0]))
                return {"__mapping__": pairs}

            if value_type is list:
                return {
                    "__sequence_type__": "list",
                    "items": [
                        _project_total(item, active_ids=active_ids, depth=depth + 1)
                        for item in list.__iter__(value)
                    ],
                }

            if value_type is tuple:
                return {
                    "__sequence_type__": "tuple",
                    "items": [
                        _project_total(item, active_ids=active_ids, depth=depth + 1)
                        for item in tuple.__iter__(value)
                    ],
                }

            if value_type is set:
                items = [
                    _project_total(item, active_ids=active_ids, depth=depth + 1)
                    for item in set.__iter__(value)
                ]
                items.sort(key=_canonical)
                return {"__set_type__": "set", "items": items}

            items = [
                _project_total(item, active_ids=active_ids, depth=depth + 1)
                for item in frozenset.__iter__(value)
            ]
            items.sort(key=_canonical)
            return {"__set_type__": "frozenset", "items": items}
        finally:
            active_ids.remove(marker)

    return {"__non_json_type__": "custom_object"}


def _malformed_required_binding_reason(packet: dict[str, Any]) -> str | None:
    for key in _REQUIRED_BINDINGS:
        if key not in packet:
            return None
        if not _r4._r3._r2._r1._valid_id(dict.get(packet, key)):
            return f"MALFORMED_BINDING:{key}"
    return None


def _requires_total_projection(packet: dict[str, Any], reason: str) -> bool:
    key = reason.split(":", 1)[1]
    binding = dict.get(packet, key)
    if not _structurally_json_safe(binding):
        return True
    return not _structurally_json_safe(packet)


def _serialization_safe_negative_receipt(
    packet: dict[str, Any],
    reason: str,
) -> Dict[str, Any]:
    projected_packet = _project_total(packet)
    proof = hashlib.sha256(_canonical(projected_packet).encode("utf-8")).hexdigest()
    return {
        "receipt_version": RECEIPT_VERSION,
        "authority_id": AUTHORITY_ID,
        "execution_scope": _project_total(dict.get(packet, "execution_scope")),
        "decision": NEGATIVE_DECISION,
        "reason": reason,
        "bindings": {
            key: _project_total(dict.get(packet, key))
            for key in _REQUIRED_BINDINGS
        },
        "consumer_rule": ADP010_CONSUMER,
        "proof_sha256": proof,
        "evidence_ownership": [],
        "project_current_state_created": False,
        "actor_created_or_activated": False,
        "adp008_phase_transition_executed": False,
        "adp019_occurrence_admitted": False,
        "causal_use_permission_owned": False,
        "contact_witness_independence_owned": False,
        "encounter_created": False,
        "oee_realized": False,
        "obl055_executed": False,
        "current_positive_obl056_installed": False,
    }


def evaluate_direct_positive_applicability(packet: Mapping[str, Any]) -> Dict[str, Any]:
    """Evaluate R4 unchanged except at the exact R5 large-int boundary."""
    if type(packet) is not dict:
        return _r4.evaluate_direct_positive_applicability(packet)

    reason = _malformed_required_binding_reason(packet)
    if reason is not None and _requires_total_projection(packet, reason):
        return _serialization_safe_negative_receipt(packet, reason)

    return _r4.evaluate_direct_positive_applicability(packet)
