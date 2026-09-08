"""OBL059 R6 bounded repair: stable malformed-int receipt construction.

R6 preserves frozen R5 behavior for ordinary inputs. It changes only the
malformed-required-binding path where an exact built-in integer could be
classified under one mutable ``sys.get_int_max_str_digits()`` setting and then
encoded after that process-global setting changed.

R6 does not make correctness depend on the current mutable conversion setting.
Instead, exact integers are considered safe for later canonical JSON encoding
only when they are below CPython's immutable minimum supported nonzero decimal
conversion limit. Values that could fail under any legal later setting are
projected immediately to the existing bounded binary diagnostic.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Dict, Mapping, Set

_R5_PATH = (
    Path(__file__).resolve().parents[1]
    / "OBL059_POSITIVE_APPLICABILITY_R5"
    / "positive_applicability_authority_r5.py"
)
_spec = importlib.util.spec_from_file_location("_obl059_r5_authority_for_r6", _R5_PATH)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"cannot load frozen OBL059 R5 authority: {_R5_PATH}")
_r5 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_r5)

AUTHORITY_ID = _r5.AUTHORITY_ID
RECEIPT_VERSION = _r5.RECEIPT_VERSION
FIRST_CANARY_SUBJECT_ID = _r5.FIRST_CANARY_SUBJECT_ID
SUBJECT_CLASSIFICATION_PREDICATE = _r5.SUBJECT_CLASSIFICATION_PREDICATE
ADP007_OWNER = _r5.ADP007_OWNER
ADP008_OWNER = _r5.ADP008_OWNER
ADP010_CONSUMER = _r5.ADP010_CONSUMER
SYNTHETIC_SCOPE = _r5.SYNTHETIC_SCOPE
POSITIVE_DECISION = _r5.POSITIVE_DECISION
NEGATIVE_DECISION = _r5.NEGATIVE_DECISION
FORBIDDEN_ALIAS_AUTHORITIES = _r5.FORBIDDEN_ALIAS_AUTHORITIES
_REQUIRED_BINDINGS = tuple(_r5._REQUIRED_BINDINGS)

R6_CANDIDATE_REVISION = "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R6"
_PROJECTION_MAX_DEPTH = _r5._PROJECTION_MAX_DEPTH
_SAFE_SCAN_MAX_DEPTH = _r5._SAFE_SCAN_MAX_DEPTH

# CPython exposes the immutable floor accepted by set_int_max_str_digits().
# A value that is renderable below this floor is renderable under every legal
# nonzero setting; 0 means unlimited. This avoids any time-separated decision
# based on mutable process-global encoder configuration.
_MIN_SUPPORTED_NONZERO_INT_STR_DIGITS = int(sys.int_info.str_digits_check_threshold)
if _MIN_SUPPORTED_NONZERO_INT_STR_DIGITS <= 0:
    raise RuntimeError("invalid immutable integer conversion threshold")
_STABLE_DECIMAL_THRESHOLD = 10 ** _MIN_SUPPORTED_NONZERO_INT_STR_DIGITS


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _exact_int_stable_for_all_supported_limits(value: int) -> bool:
    """True only when exact int stays decimal-renderable under every legal setting."""
    if type(value) is not int:
        raise TypeError("exact int required")
    return -_STABLE_DECIMAL_THRESHOLD < value < _STABLE_DECIMAL_THRESHOLD


def _is_stably_json_primitive(value: Any) -> bool:
    value_type = type(value)
    if value_type is int:
        return _exact_int_stable_for_all_supported_limits(value)
    return value_type in (type(None), str, bool, float)


def _binary_magnitude_sha256(value: int) -> str:
    if type(value) is not int:
        raise TypeError("exact int required")
    magnitude = value if value >= 0 else -value
    bit_length = int.bit_length(magnitude)
    byte_length = max(1, (bit_length + 7) // 8)
    payload = int.to_bytes(magnitude, byte_length, "big", signed=False)
    return hashlib.sha256(payload).hexdigest()


def _project_unstable_int(value: int) -> Dict[str, Any]:
    """Use the R5 diagnostic shape without consulting mutable runtime state."""
    return {
        "__non_json_int__": "decimal_conversion_limit_exceeded",
        "sign": -1 if value < 0 else 1,
        "bit_length": int.bit_length(value),
        "binary_magnitude_sha256": _binary_magnitude_sha256(value),
    }


def _structurally_json_safe_across_supported_limits(
    value: Any,
    *,
    active_ids: Set[int] | None = None,
    depth: int = 0,
) -> bool:
    """Exact-built-in scan whose answer cannot change with int conversion config."""
    if _is_stably_json_primitive(value):
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
                    if not _exact_int_stable_for_all_supported_limits(key):
                        return False
                elif key_type not in (str, float, bool, type(None)):
                    return False
                if not _structurally_json_safe_across_supported_limits(
                    item, active_ids=active_ids, depth=depth + 1
                ):
                    return False
            return True

        iterator = list.__iter__(value) if value_type is list else tuple.__iter__(value)
        for item in iterator:
            if not _structurally_json_safe_across_supported_limits(
                item, active_ids=active_ids, depth=depth + 1
            ):
                return False
        return True
    finally:
        active_ids.remove(marker)


def _project_total_stable(
    value: Any,
    *,
    active_ids: Set[int] | None = None,
    depth: int = 0,
) -> Any:
    """Bounded projection independent of mutable integer conversion configuration."""
    if type(value) is int and not _exact_int_stable_for_all_supported_limits(value):
        return _project_unstable_int(value)

    if _is_stably_json_primitive(value):
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
                        _project_total_stable(key, active_ids=active_ids, depth=depth + 1),
                        _project_total_stable(item, active_ids=active_ids, depth=depth + 1),
                    ]
                    for key, item in dict.items(value)
                ]
                pairs.sort(key=lambda pair: _canonical(pair[0]))
                return {"__mapping__": pairs}

            if value_type is list:
                return {
                    "__sequence_type__": "list",
                    "items": [
                        _project_total_stable(item, active_ids=active_ids, depth=depth + 1)
                        for item in list.__iter__(value)
                    ],
                }

            if value_type is tuple:
                return {
                    "__sequence_type__": "tuple",
                    "items": [
                        _project_total_stable(item, active_ids=active_ids, depth=depth + 1)
                        for item in tuple.__iter__(value)
                    ],
                }

            if value_type is set:
                items = [
                    _project_total_stable(item, active_ids=active_ids, depth=depth + 1)
                    for item in set.__iter__(value)
                ]
                items.sort(key=_canonical)
                return {"__set_type__": "set", "items": items}

            items = [
                _project_total_stable(item, active_ids=active_ids, depth=depth + 1)
                for item in frozenset.__iter__(value)
            ]
            items.sort(key=_canonical)
            return {"__set_type__": "frozenset", "items": items}
        finally:
            active_ids.remove(marker)

    return {"__non_json_type__": "custom_object"}


def _malformed_required_binding_reason(packet: dict[str, Any]) -> str | None:
    return _r5._malformed_required_binding_reason(packet)


def _requires_total_projection_stable(packet: dict[str, Any], reason: str) -> bool:
    key = reason.split(":", 1)[1]
    binding = dict.get(packet, key)
    if not _structurally_json_safe_across_supported_limits(binding):
        return True
    return not _structurally_json_safe_across_supported_limits(packet)


def _serialization_safe_negative_receipt_stable(
    packet: dict[str, Any],
    reason: str,
) -> Dict[str, Any]:
    projected_packet = _project_total_stable(packet)
    proof = hashlib.sha256(_canonical(projected_packet).encode("utf-8")).hexdigest()
    return {
        "receipt_version": RECEIPT_VERSION,
        "authority_id": AUTHORITY_ID,
        "execution_scope": _project_total_stable(dict.get(packet, "execution_scope")),
        "decision": NEGATIVE_DECISION,
        "reason": reason,
        "bindings": {
            key: _project_total_stable(dict.get(packet, key))
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
    """Evaluate R5 unchanged except for the exact R6 stable malformed-int boundary."""
    if type(packet) is not dict:
        return _r5.evaluate_direct_positive_applicability(packet)

    reason = _malformed_required_binding_reason(packet)
    if reason is not None and _requires_total_projection_stable(packet, reason):
        return _serialization_safe_negative_receipt_stable(packet, reason)

    return _r5.evaluate_direct_positive_applicability(packet)
