"""OBL059 R2 bounded repair: serialization-safe negative receipts.

This module preserves the frozen OBL059 R1 authority semantics for every
JSON-serializable packet. It adds only a fail-closed fallback for the R1
negative-receipt construction defect discovered after freeze: if R1 reaches
receipt hashing with a packet that contains a non-JSON-serializable value, R2
returns a deterministic JSON-serializable negative receipt instead of raising.

No project-current state is created and no runtime side effect is performed.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple, List

_R1_PATH = (
    Path(__file__).resolve().parents[1]
    / "OBL059_POSITIVE_APPLICABILITY_R1"
    / "positive_applicability_authority.py"
)
_spec = importlib.util.spec_from_file_location("_obl059_r1_authority", _R1_PATH)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"cannot load frozen OBL059 R1 authority: {_R1_PATH}")
_r1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_r1)

AUTHORITY_ID = _r1.AUTHORITY_ID
RECEIPT_VERSION = _r1.RECEIPT_VERSION
FIRST_CANARY_SUBJECT_ID = _r1.FIRST_CANARY_SUBJECT_ID
SUBJECT_CLASSIFICATION_PREDICATE = _r1.SUBJECT_CLASSIFICATION_PREDICATE
ADP007_OWNER = _r1.ADP007_OWNER
ADP008_OWNER = _r1.ADP008_OWNER
ADP010_CONSUMER = _r1.ADP010_CONSUMER
SYNTHETIC_SCOPE = _r1.SYNTHETIC_SCOPE
POSITIVE_DECISION = _r1.POSITIVE_DECISION
NEGATIVE_DECISION = _r1.NEGATIVE_DECISION
FORBIDDEN_ALIAS_AUTHORITIES = _r1.FORBIDDEN_ALIAS_AUTHORITIES
_REQUIRED_BINDINGS = tuple(_r1._REQUIRED_BINDINGS)

R2_CANDIDATE_REVISION = "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R2"


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _json_projection(value: Any) -> Any:
    """Deterministically project non-JSON values into JSON-safe diagnostics."""
    if value is None or isinstance(value, (str, bool, int, float)):
        return value

    if isinstance(value, bytes):
        return {
            "__non_json_type__": "bytes",
            "length": len(value),
            "sha256": hashlib.sha256(value).hexdigest(),
        }

    if isinstance(value, Mapping):
        projected = [
            [_json_projection(key), _json_projection(item)]
            for key, item in value.items()
        ]
        projected.sort(key=lambda pair: _canonical(pair[0]))
        return {"__mapping__": projected}

    if isinstance(value, (list, tuple)):
        return {
            "__sequence_type__": type(value).__name__,
            "items": [_json_projection(item) for item in value],
        }

    if isinstance(value, (set, frozenset)):
        items = [_json_projection(item) for item in value]
        items.sort(key=_canonical)
        return {
            "__set_type__": type(value).__name__,
            "items": items,
        }

    return {
        "__non_json_type__": f"{type(value).__module__}.{type(value).__qualname__}"
    }


def _receipt_safe(value: Any) -> Any:
    """Preserve ordinary JSON-safe values; project only values JSON cannot encode."""
    try:
        _canonical(value)
    except (TypeError, ValueError):
        return _json_projection(value)
    return deepcopy(value)


def _fallback_proof_sha256(packet: Mapping[str, Any]) -> str:
    projected = _json_projection(packet)
    return hashlib.sha256(_canonical(projected).encode("utf-8")).hexdigest()


def _derive_negative_reason_and_ownership(
    packet: Mapping[str, Any],
) -> Tuple[str, List[Dict[str, str]]]:
    """Repeat the frozen R1 checks without invoking receipt serialization."""
    scope_error = _r1._check_exact_scope(packet)
    if scope_error:
        return scope_error, []

    evidence, evidence_error = _r1._require_evidence_mapping(packet)
    if evidence_error:
        return evidence_error, []

    proof_error, ownership = _r1._check_evidence(packet, evidence)
    if proof_error:
        return proof_error, ownership

    return "NON_JSON_SERIALIZABLE_PACKET", ownership


def _serialization_safe_negative_receipt(
    packet: Mapping[str, Any],
    reason: str,
    ownership: List[Dict[str, str]],
) -> Dict[str, Any]:
    return {
        "receipt_version": RECEIPT_VERSION,
        "authority_id": AUTHORITY_ID,
        "execution_scope": _receipt_safe(packet.get("execution_scope")),
        "decision": NEGATIVE_DECISION,
        "reason": reason,
        "bindings": {
            key: _receipt_safe(packet.get(key))
            for key in _REQUIRED_BINDINGS
        },
        "consumer_rule": ADP010_CONSUMER,
        "proof_sha256": _fallback_proof_sha256(packet),
        "evidence_ownership": deepcopy(ownership),
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
    """Evaluate R1 unchanged, repairing only its JSON-serialization failure path."""
    try:
        return _r1.evaluate_direct_positive_applicability(packet)
    except TypeError as exc:
        if "is not JSON serializable" not in str(exc):
            raise
        if not isinstance(packet, Mapping):
            raise
        copied = deepcopy(dict(packet))
        reason, ownership = _derive_negative_reason_and_ownership(copied)
        return _serialization_safe_negative_receipt(copied, reason, ownership)
