"""Stage-3 bridge helpers for feeding v5 trajectory evidence into the v3 field."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from v3.core.state import clamp
from v3.io.v5_bridge import normalize_bridge_status

GREEN_BRIDGE_STATUSES = {"ok", "green", "attached"}
FIELD_KEYS = {
    "economy",
    "repression_baseline",
    "morale",
    "legitimacy",
    "fear",
    "repression_justification",
    "recruitment",
    "defections",
}


def _extract_numeric_fields(source: Mapping[str, Any] | None) -> dict[str, float]:
    out: dict[str, float] = {}
    if not isinstance(source, Mapping):
        return out
    for key in FIELD_KEYS:
        value = source.get(key)
        if isinstance(value, (int, float)):
            out[key] = clamp(float(value), 0.0, 100.0)
    return out


def build_v5_field_bridge_injection(v5_bridge: Mapping[str, Any] | None) -> dict[str, Any]:
    """Convert a v5 trajectory bridge artifact into field injection with provenance."""
    raw = dict(v5_bridge) if isinstance(v5_bridge, Mapping) else {}
    status = normalize_bridge_status(raw.get("status"))
    payload = raw.get("field")
    if not isinstance(payload, Mapping):
        payload = raw.get("raw")
    if not isinstance(payload, Mapping):
        payload = raw.get("trajectory")
    if not isinstance(payload, Mapping):
        payload = raw.get("payload")
    numeric = _extract_numeric_fields(payload if isinstance(payload, Mapping) else None)
    if status not in GREEN_BRIDGE_STATUSES:
        numeric = {}
    provenance = {
        "source": "v5_field_bridge",
        "status": status,
        "refs": [str(ref).strip() for ref in (raw.get("refs") or []) if str(ref).strip()] if isinstance(raw.get("refs"), list) else [],
        "notes": [str(note).strip() for note in (raw.get("notes") or []) if str(note).strip()] if isinstance(raw.get("notes"), list) else [],
        "payload_keys": sorted(list(payload.keys())) if isinstance(payload, Mapping) else [],
    }
    integrity = {
        "status": "ok" if numeric and status in GREEN_BRIDGE_STATUSES else ("blocked" if status == "blocked" else "degraded"),
        "reasons": [] if numeric and status in GREEN_BRIDGE_STATUSES else (
            ["blocked_v5_trajectory_bridge"] if status == "blocked" else ["no_green_trajectory_values"]
        ),
        "confidence": 100.0 if numeric and status in GREEN_BRIDGE_STATUSES else 0.0,
        "conflicts": [],
    }
    out: dict[str, Any] = dict(numeric)
    out["_integrity"] = integrity
    out["_provenance"] = {
        "fields": {
            key: {"source": "v5_field_bridge", "status": status, "value": value, "confidence": 100.0}
            for key, value in numeric.items()
        },
        "bridge": provenance,
    }
    return out
