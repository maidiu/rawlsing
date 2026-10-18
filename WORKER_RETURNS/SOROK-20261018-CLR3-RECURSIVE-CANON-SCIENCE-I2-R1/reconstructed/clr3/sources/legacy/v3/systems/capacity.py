# v3/systems/capacity.py — update capacity from events; apply delta cap. AC (with hostage penalty) is derived after this step.

from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState, clamp
from v3.core.derived import DerivedIndices

CAPACITY_FIELD_NAMES = (
    "time",
    "money",
    "health",
    "social_support",
    "skill",
    "mobility",
    "risk_tolerance",
    "legitimacy",
)

DEFAULT_DELTA_CAP = 20


def _get_delta_cap(config: dict) -> float:
    """Per-field annual delta cap for capacity (v3config delta_caps)."""
    caps = config.get("delta_caps") or {}
    return float(caps.get("capacity_fields", DEFAULT_DELTA_CAP))


def _apply_deltas(state: BackboneState, config: dict) -> None:
    """Apply event-driven deltas to capacity; respect per-field delta cap. Clamp after."""
    c = state.capacity
    cap = _get_delta_cap(config)

    deltas: dict[str, float] = {k: 0.0 for k in CAPACITY_FIELD_NAMES}
    for ev in state.events_this_year:
        if not isinstance(ev, dict):
            continue
        cd = ev.get("capacity_deltas")
        if not isinstance(cd, dict):
            continue
        for key in CAPACITY_FIELD_NAMES:
            if key in cd and isinstance(cd[key], (int, float)):
                deltas[key] += float(cd[key])

    for key in CAPACITY_FIELD_NAMES:
        current = getattr(c, key)
        delta = deltas[key]
        delta = max(-cap, min(cap, delta))
        setattr(c, key, clamp(current + delta))

    c.clamp_all()


def update_capacity(
    state: BackboneState,
    derived: DerivedIndices,
    config: dict[str, Any],
) -> None:
    """Update capacity from events; apply annual delta cap. Derived (agency_capacity_AC) is recomputed after this step."""
    _apply_deltas(state, config)
