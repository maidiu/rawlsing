# v3/systems/reproduction.py — update reproduction constraints from events; apply delta cap.

from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState, clamp
from v3.core.derived import DerivedIndices

# State field names that may be updated from events (and capped).
REPRODUCTION_FIELD_NAMES = (
    "dependents",
    "housing_insecurity",
    "legal_status",
    "debt",
    "job_insecurity",
    "caregiving_load",
)

DEFAULT_DELTA_CAP = 20


def _get_delta_cap(config: dict[str, Any]) -> float:
    """Per-field annual delta cap for reproduction constraints (v3config delta_caps)."""
    caps = config.get("delta_caps") or {}
    return float(caps.get("reproduction_constraints_fields", DEFAULT_DELTA_CAP))


def _apply_deltas(
    state: BackboneState,
    config: dict[str, Any],
) -> None:
    """Apply event-driven deltas to reproduction_constraints; respect per-field delta cap. Clamp after."""
    r = state.reproduction_constraints
    cap = _get_delta_cap(config)

    # Sum deltas from all events. Event payload: {"reproduction_deltas": {"job_insecurity": 10, "debt": 5, ...}}
    deltas: dict[str, float] = {k: 0.0 for k in REPRODUCTION_FIELD_NAMES}
    for ev in state.events_this_year:
        if not isinstance(ev, dict):
            continue
        rd = ev.get("reproduction_deltas")
        if not isinstance(rd, dict):
            continue
        for key in REPRODUCTION_FIELD_NAMES:
            if key in rd and isinstance(rd[key], (int, float)):
                deltas[key] += float(rd[key])

    # Apply each field: current + capped delta, then clamp.
    for key in REPRODUCTION_FIELD_NAMES:
        current = getattr(r, key)
        delta = deltas[key]
        # Clamp delta to [-cap, +cap] so one year's total change is bounded.
        delta = max(-cap, min(cap, delta))
        setattr(r, key, clamp(current + delta))

    r.clamp_all()


def update_reproduction_constraints(
    state: BackboneState,
    derived: DerivedIndices,
    config: dict[str, Any],
) -> None:
    """Update reproduction constraints from events; apply annual delta cap. Derived (hostage_index) is recomputed after this step by the runner."""
    _apply_deltas(state, config)
