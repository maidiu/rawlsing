# v3/systems/field.py — update macro field (economy, repression, etc.) from prior-year events; apply cap.

from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState, clamp
from v3.core.derived import DerivedIndices
from v3.io.v5_field_bridge import build_v5_field_bridge_injection

FIELD_DELTA_CAP_DEFAULT = 10


def update_field(
    state: BackboneState,
    derived: DerivedIndices,
    config: dict[str, Any],
) -> None:
    """Apply event-driven field_deltas to state.field.raw (prior year's events). Does not touch domains/peak_routing.
    If config has field_injection (Wave 5), merge that into raw first (from world_slice/driver_vec when available)."""
    caps = config.get("delta_caps") or {}
    cap = float(caps.get("field_raw", FIELD_DELTA_CAP_DEFAULT))
    raw = state.field.raw
    if not isinstance(raw, dict):
        state.field.raw = {}
        raw = state.field.raw
    provenance = state.field.provenance if isinstance(getattr(state.field, "provenance", None), dict) else {}
    provenance["fields"] = {}
    current_year_provenance: dict[str, Any] = {
        "year": state.year,
        "source": "field_update",
        "injection": {},
        "event_deltas": {},
    }
    # Wave 5: inject from driver_model, civic_soul, imperial_block, world_slice, driver_vec.
    # V538/V18 bridge: optional v5_field_bridge may mediate green trajectory inputs into field.raw
    # with explicit provenance; blocked bridges must not introduce numeric values.
    injection = config.get("field_injection")
    v5_bridge = config.get("v5_field_bridge")
    if isinstance(v5_bridge, dict) and v5_bridge:
        bridge_injection = build_v5_field_bridge_injection(v5_bridge)
        if isinstance(injection, dict) and injection:
            merged = dict(injection)
            for k, v in bridge_injection.items():
                if k not in ("_integrity", "_provenance"):
                    merged[k] = v
            if "_integrity" in bridge_injection:
                merged["_integrity"] = bridge_injection["_integrity"]
            if "_provenance" in bridge_injection:
                merged["_provenance"] = bridge_injection["_provenance"]
            injection = merged
        else:
            injection = bridge_injection
    if isinstance(injection, dict) and injection:
        injection_integrity = injection.get("_integrity") if isinstance(injection.get("_integrity"), dict) else {}
        injection_provenance = injection.get("_provenance") if isinstance(injection.get("_provenance"), dict) else {}
        current_year_provenance["injection"] = {
            "integrity": injection_integrity,
            "provenance": injection_provenance,
        }
        yearly = getattr(state, "yearly_integrity", None)
        if isinstance(yearly, dict):
            yearly["field_injection"] = {
                "status": injection_integrity.get("status", "ok"),
                "confidence": injection_integrity.get("confidence"),
                "reasons": injection_integrity.get("reasons", []),
            }
        for k, v in injection.items():
            if k.startswith("_"):
                continue
            if isinstance(v, (int, float)):
                raw[k] = clamp(float(v))
                provenance.setdefault("fields", {})[k] = {
                    "source": "field_injection",
                    "source_detail": (injection_provenance.get("fields") or {}).get(k, {}) if isinstance(injection_provenance, dict) else {},
                    "value": raw[k],
                    "confidence": (injection_integrity.get("confidence") if isinstance(injection_integrity, dict) else None),
                }
    else:
        # No injection available — record degraded status
        yearly = getattr(state, "yearly_integrity", None)
        if isinstance(yearly, dict):
            yearly["field_injection"] = {
                "status": "degraded",
                "reasons": ["no_field_injection_available"],
            }
    deltas: dict[str, float] = {}
    event_sources: dict[str, list[dict[str, Any]]] = {}
    for ev in state.events_this_year:
        if not isinstance(ev, dict):
            continue
        fd = ev.get("field_deltas")
        if not isinstance(fd, dict):
            continue
        for k, v in fd.items():
            if isinstance(v, (int, float)):
                deltas[k] = deltas.get(k, 0.0) + float(v)
                event_sources.setdefault(k, []).append(
                    {
                        "event_id": ev.get("id") or "",
                        "label": ev.get("label") or "",
                        "source": ev.get("source") or "event_sampling",
                        "delta": float(v),
                    }
                )
    for k, delta in deltas.items():
        delta = max(-cap, min(cap, delta))
        current = float(raw.get(k, 50.0)) if isinstance(raw.get(k), (int, float)) else 50.0
        raw[k] = clamp(current + delta)
        provenance.setdefault("fields", {})[k] = {
            "source": "event_sampling",
            "events": event_sources.get(k, []),
            "delta": delta,
            "value": raw[k],
            "confidence": 75.0 if event_sources.get(k) else 50.0,
        }
    current_year_provenance["event_deltas"] = {
        k: {"delta": delta, "events": event_sources.get(k, [])}
        for k, delta in deltas.items()
    }
    provenance["current_injection"] = current_year_provenance["injection"]
    provenance["current_year"] = current_year_provenance
    state.field.provenance = provenance
