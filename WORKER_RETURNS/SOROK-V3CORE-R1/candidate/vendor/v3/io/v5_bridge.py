"""Explicit v5-to-v3 bridge carrier helpers.

Stage 1 only: store v5 authority bundle metadata on BackboneState without mutating
any runtime numerics or persona/surface fields.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from v3.core.state import BackboneState

BRIDGE_STATUS_NOT_ATTACHED = "not_attached"
BRIDGE_STATUS_ATTACHED = "attached"
BRIDGE_STATUS_DEGRADED = "degraded"
BRIDGE_STATUS_BLOCKED = "blocked"
BRIDGE_STATUS_GREEN = "green"

VALID_BRIDGE_STATUSES = {
    BRIDGE_STATUS_NOT_ATTACHED,
    BRIDGE_STATUS_ATTACHED,
    BRIDGE_STATUS_DEGRADED,
    BRIDGE_STATUS_BLOCKED,
    BRIDGE_STATUS_GREEN,
}


def normalize_bridge_status(status: str | None) -> str:
    value = str(status or BRIDGE_STATUS_NOT_ATTACHED).strip().lower()
    return value if value in VALID_BRIDGE_STATUSES else BRIDGE_STATUS_NOT_ATTACHED


def _coerce_refs(refs: Sequence[Any] | None) -> list[str]:
    if not refs:
        return []
    return [str(ref).strip() for ref in refs if str(ref).strip()]


def normalize_v5_runtime_input_bundle(
    bundle: Mapping[str, Any] | None,
    *,
    status: str | None = None,
    refs: Sequence[Any] | None = None,
    notes: Sequence[Any] | None = None,
) -> dict[str, Any]:
    """Return an inert bridge bundle with explicit status/ref provenance."""
    raw_bundle = dict(bundle) if isinstance(bundle, Mapping) else {}
    normalized_status = normalize_bridge_status(status or raw_bundle.get("status"))
    raw_refs = refs if refs is not None else raw_bundle.get("refs")
    raw_notes = notes if notes is not None else raw_bundle.get("notes")
    if isinstance(raw_refs, (str, bytes, bytearray)):
        normalized_refs = _coerce_refs([raw_refs])
    else:
        normalized_refs = _coerce_refs(raw_refs if isinstance(raw_refs, Sequence) else [])
    if isinstance(raw_notes, (str, bytes, bytearray)):
        normalized_notes = _coerce_refs([raw_notes])
    else:
        normalized_notes = _coerce_refs(raw_notes if isinstance(raw_notes, Sequence) else [])
    payload = raw_bundle.get("payload", raw_bundle.get("data", raw_bundle.get("value", {})))
    if isinstance(payload, Mapping):
        payload = dict(payload)
    elif isinstance(payload, Sequence) and not isinstance(payload, (str, bytes, bytearray)):
        payload = list(payload)
    bundle_out: dict[str, Any] = {
        "status": normalized_status,
        "refs": normalized_refs,
        "notes": normalized_notes,
        "payload": payload,
    }
    if "source" in raw_bundle:
        bundle_out["source"] = raw_bundle["source"]
    if "provenance" in raw_bundle and isinstance(raw_bundle["provenance"], Mapping):
        bundle_out["provenance"] = dict(raw_bundle["provenance"])
    return bundle_out


def attach_v5_runtime_input_bundle(
    state: BackboneState,
    bundle: Mapping[str, Any] | None,
    *,
    status: str | None = None,
    refs: Sequence[Any] | None = None,
    notes: Sequence[Any] | None = None,
) -> BackboneState:
    """Attach v5 bridge metadata to an existing BackboneState without changing runtime numerics."""
    normalized = normalize_v5_runtime_input_bundle(bundle, status=status, refs=refs, notes=notes)
    state.v5_runtime_input_bundle = normalized
    state.v5_runtime_input_refs = list(normalized.get("refs") or [])
    state.v5_bridge_status = normalize_bridge_status(normalized.get("status"))
    return state


def v5_bridge_snapshot(state: BackboneState) -> dict[str, Any]:
    """Read-only snapshot of bridge metadata."""
    return {
        "status": normalize_bridge_status(getattr(state, "v5_bridge_status", None)),
        "refs": list(getattr(state, "v5_runtime_input_refs", []) or []),
        "bundle": dict(getattr(state, "v5_runtime_input_bundle", {}) or {}),
    }
