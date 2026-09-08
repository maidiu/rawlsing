"""OBL059 R3 bounded repair: cycle-safe malformed-binding negative receipts.

This module preserves frozen R1/R2 applicability semantics for ordinary JSON-safe
packets.  It changes only the commissioned malformed required-binding receipt
construction boundary.

Once a required binding is already semantically malformed, R3 probes the copied
packet's JSON serializability in a bounded helper. If the packet cannot be
serialized, R3 constructs the negative receipt directly using a deterministic,
cycle-safe diagnostic projection. No exception-message matching is used.

No project-current state or runtime effect is created.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Mapping, Set

_R2_PATH = (
    Path(__file__).resolve().parents[1]
    / "OBL059_POSITIVE_APPLICABILITY_R2"
    / "positive_applicability_authority_r2.py"
)
_spec = importlib.util.spec_from_file_location("_obl059_r2_authority", _R2_PATH)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"cannot load frozen OBL059 R2 authority: {_R2_PATH}")
_r2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_r2)

AUTHORITY_ID = _r2.AUTHORITY_ID
RECEIPT_VERSION = _r2.RECEIPT_VERSION
FIRST_CANARY_SUBJECT_ID = _r2.FIRST_CANARY_SUBJECT_ID
SUBJECT_CLASSIFICATION_PREDICATE = _r2.SUBJECT_CLASSIFICATION_PREDICATE
ADP007_OWNER = _r2.ADP007_OWNER
ADP008_OWNER = _r2.ADP008_OWNER
ADP010_CONSUMER = _r2.ADP010_CONSUMER
SYNTHETIC_SCOPE = _r2.SYNTHETIC_SCOPE
POSITIVE_DECISION = _r2.POSITIVE_DECISION
NEGATIVE_DECISION = _r2.NEGATIVE_DECISION
FORBIDDEN_ALIAS_AUTHORITIES = _r2.FORBIDDEN_ALIAS_AUTHORITIES
_REQUIRED_BINDINGS = tuple(_r2._REQUIRED_BINDINGS)

R3_CANDIDATE_REVISION = "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R3"
_PROJECTION_MAX_DEPTH = 64
_SERIALIZATION_BOUNDARY_ERRORS = (TypeError, ValueError, RecursionError, OverflowError)


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _type_name(value: Any) -> str:
    return f"{type(value).__module__}.{type(value).__qualname__}"


def _project_json_safe(
    value: Any,
    *,
    active_ids: Set[int] | None = None,
    depth: int = 0,
) -> Any:
    """Project diagnostics deterministically without following cycles forever.

    The projection intentionally never turns a malformed binding into a string
    identifier. Container projections remain structured diagnostic objects.
    """
    if active_ids is None:
        active_ids = set()

    if value is None or isinstance(value, (str, bool, int, float)):
        return value

    if isinstance(value, bytes):
        return {
            "__non_json_type__": "bytes",
            "length": len(value),
            "sha256": hashlib.sha256(value).hexdigest(),
        }

    if depth >= _PROJECTION_MAX_DEPTH:
        return {
            "__projection_depth_limit__": _type_name(value),
            "max_depth": _PROJECTION_MAX_DEPTH,
        }

    is_container = isinstance(value, (Mapping, list, tuple, set, frozenset))
    marker = id(value)
    if is_container and marker in active_ids:
        return {"__cycle__": _type_name(value)}

    if isinstance(value, Mapping):
        active_ids.add(marker)
        try:
            pairs = [
                [
                    _project_json_safe(key, active_ids=active_ids, depth=depth + 1),
                    _project_json_safe(item, active_ids=active_ids, depth=depth + 1),
                ]
                for key, item in value.items()
            ]
        finally:
            active_ids.remove(marker)
        pairs.sort(key=_canonical)
        return {"__mapping__": pairs}

    if isinstance(value, (list, tuple)):
        active_ids.add(marker)
        try:
            items = [
                _project_json_safe(item, active_ids=active_ids, depth=depth + 1)
                for item in value
            ]
        finally:
            active_ids.remove(marker)
        return {
            "__sequence_type__": type(value).__name__,
            "items": items,
        }

    if isinstance(value, (set, frozenset)):
        active_ids.add(marker)
        try:
            items = [
                _project_json_safe(item, active_ids=active_ids, depth=depth + 1)
                for item in value
            ]
        finally:
            active_ids.remove(marker)
        items.sort(key=_canonical)
        return {
            "__set_type__": type(value).__name__,
            "items": items,
        }

    return {"__non_json_type__": _type_name(value)}


def _diagnostic_safe(value: Any) -> Any:
    """Preserve ordinary JSON-safe values; project only serialization failures."""
    try:
        _canonical(value)
    except _SERIALIZATION_BOUNDARY_ERRORS:
        return _project_json_safe(value)
    return deepcopy(value)


def _fallback_proof_sha256(packet: Mapping[str, Any]) -> str:
    projected = _project_json_safe(packet)
    return hashlib.sha256(_canonical(projected).encode("utf-8")).hexdigest()


def _malformed_required_binding_reason(packet: Mapping[str, Any]) -> str | None:
    """Return only the commissioned malformed-binding semantic reason.

    Missing bindings remain delegated to frozen R2/R1 so their ordinary behavior
    stays byte-for-byte unchanged.
    """
    for key in _REQUIRED_BINDINGS:
        if key not in packet:
            return None
        if not _r2._r1._valid_id(packet.get(key)):
            return f"MALFORMED_BINDING:{key}"
    return None


def _packet_needs_safe_receipt(packet: Mapping[str, Any]) -> bool:
    """Probe JSON serialization in isolation from semantic evaluation."""
    try:
        _canonical(packet)
    except _SERIALIZATION_BOUNDARY_ERRORS:
        return True
    return False


def _serialization_safe_negative_receipt(
    packet: Mapping[str, Any],
    reason: str,
) -> Dict[str, Any]:
    return {
        "receipt_version": RECEIPT_VERSION,
        "authority_id": AUTHORITY_ID,
        "execution_scope": _diagnostic_safe(packet.get("execution_scope")),
        "decision": NEGATIVE_DECISION,
        "reason": reason,
        "bindings": {
            key: _diagnostic_safe(packet.get(key))
            for key in _REQUIRED_BINDINGS
        },
        "consumer_rule": ADP010_CONSUMER,
        "proof_sha256": _fallback_proof_sha256(packet),
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
    """Evaluate R2 unchanged except at the exact malformed-binding boundary."""
    if not isinstance(packet, Mapping):
        return _r2.evaluate_direct_positive_applicability(packet)

    copied = deepcopy(dict(packet))
    reason = _malformed_required_binding_reason(copied)

    if reason is not None and _packet_needs_safe_receipt(copied):
        return _serialization_safe_negative_receipt(copied, reason)

    return _r2.evaluate_direct_positive_applicability(packet)
