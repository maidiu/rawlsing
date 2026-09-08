"""OBL059 R4 bounded repair: total malformed-diagnostic projection.

R4 preserves frozen R1/R2/R3 applicability semantics for ordinary packets.
It changes only the commissioned negative-receipt construction boundary after
an exact required binding is already semantically malformed.

For that boundary, R4 decides structural JSON safety using exact built-in
types only. If a malformed binding is not structurally JSON-safe, the receipt
uses a bounded diagnostic projection that traverses only exact built-in
containers. Arbitrary/custom objects are represented by a fixed diagnostic
category and none of their protocol/display/comparison methods are invoked.

No project-current state or runtime effect is created.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Set

_R3_PATH = (
    Path(__file__).resolve().parents[1]
    / "OBL059_POSITIVE_APPLICABILITY_R3"
    / "positive_applicability_authority_r3.py"
)
_spec = importlib.util.spec_from_file_location("_obl059_r3_authority", _R3_PATH)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"cannot load frozen OBL059 R3 authority: {_R3_PATH}")
_r3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_r3)

AUTHORITY_ID = _r3.AUTHORITY_ID
RECEIPT_VERSION = _r3.RECEIPT_VERSION
FIRST_CANARY_SUBJECT_ID = _r3.FIRST_CANARY_SUBJECT_ID
SUBJECT_CLASSIFICATION_PREDICATE = _r3.SUBJECT_CLASSIFICATION_PREDICATE
ADP007_OWNER = _r3.ADP007_OWNER
ADP008_OWNER = _r3.ADP008_OWNER
ADP010_CONSUMER = _r3.ADP010_CONSUMER
SYNTHETIC_SCOPE = _r3.SYNTHETIC_SCOPE
POSITIVE_DECISION = _r3.POSITIVE_DECISION
NEGATIVE_DECISION = _r3.NEGATIVE_DECISION
FORBIDDEN_ALIAS_AUTHORITIES = _r3.FORBIDDEN_ALIAS_AUTHORITIES
_REQUIRED_BINDINGS = tuple(_r3._REQUIRED_BINDINGS)

R4_CANDIDATE_REVISION = "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R4"
_PROJECTION_MAX_DEPTH = 64
_SAFE_SCAN_MAX_DEPTH = 256


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _is_exact_primitive(value: Any) -> bool:
    return type(value) in (type(None), str, bool, int, float)


def _structurally_json_safe(
    value: Any,
    *,
    active_ids: Set[int] | None = None,
    depth: int = 0,
) -> bool:
    """Conservative JSON-safety check without invoking custom object methods."""
    if _is_exact_primitive(value):
        return True

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
                if type(key) not in (str, int, float, bool, type(None)):
                    return False
                if not _structurally_json_safe(
                    item, active_ids=active_ids, depth=depth + 1
                ):
                    return False
            return True

        if value_type is list:
            for item in list.__iter__(value):
                if not _structurally_json_safe(
                    item, active_ids=active_ids, depth=depth + 1
                ):
                    return False
            return True

        for item in tuple.__iter__(value):
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
    """Bounded JSON-safe projection using exact built-in operations only."""
    if _is_exact_primitive(value):
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
                        _project_total(
                            key, active_ids=active_ids, depth=depth + 1
                        ),
                        _project_total(
                            item, active_ids=active_ids, depth=depth + 1
                        ),
                    ]
                    for key, item in dict.items(value)
                ]
                pairs.sort(key=lambda pair: _canonical(pair[0]))
                return {"__mapping__": pairs}

            if value_type is list:
                return {
                    "__sequence_type__": "list",
                    "items": [
                        _project_total(
                            item, active_ids=active_ids, depth=depth + 1
                        )
                        for item in list.__iter__(value)
                    ],
                }

            if value_type is tuple:
                return {
                    "__sequence_type__": "tuple",
                    "items": [
                        _project_total(
                            item, active_ids=active_ids, depth=depth + 1
                        )
                        for item in tuple.__iter__(value)
                    ],
                }

            if value_type is set:
                items = [
                    _project_total(
                        item, active_ids=active_ids, depth=depth + 1
                    )
                    for item in set.__iter__(value)
                ]
                items.sort(key=_canonical)
                return {"__set_type__": "set", "items": items}

            items = [
                _project_total(
                    item, active_ids=active_ids, depth=depth + 1
                )
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
        if not _r3._r2._r1._valid_id(dict.get(packet, key)):
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
    """Evaluate R3 unchanged except at the exact malformed-diagnostic boundary."""
    if type(packet) is not dict:
        return _r3.evaluate_direct_positive_applicability(packet)

    reason = _malformed_required_binding_reason(packet)
    if reason is not None and _requires_total_projection(packet, reason):
        return _serialization_safe_negative_receipt(packet, reason)

    return _r3.evaluate_direct_positive_applicability(packet)
