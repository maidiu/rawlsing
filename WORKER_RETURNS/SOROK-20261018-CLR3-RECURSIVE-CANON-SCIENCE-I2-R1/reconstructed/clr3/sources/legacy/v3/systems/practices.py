# v3/systems/practices.py — update practice stack from events; apply delta cap.

from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState, clamp
from v3.core.derived import DerivedIndices

PRACTICE_FIELDS = ("study", "care", "organizing", "craft", "spiritual", "risk_training")
DEFAULT_DELTA_CAP = 15


def _get_delta_cap(config: dict[str, Any]) -> float:
    caps = config.get("delta_caps") or {}
    return float(caps.get("practice_fields", DEFAULT_DELTA_CAP))


def update_practice_stack(
    state: BackboneState,
    derived: DerivedIndices,
    config: dict[str, Any],
) -> None:
    """Apply event-driven deltas to practice stack; respect annual cap per field."""
    cap = _get_delta_cap(config)
    p = state.practice_stack
    deltas = {k: 0.0 for k in PRACTICE_FIELDS}
    for ev in state.events_this_year:
        if not isinstance(ev, dict):
            continue
        pd = ev.get("practice_deltas")
        if not isinstance(pd, dict):
            continue
        for k in PRACTICE_FIELDS:
            if k in pd and isinstance(pd[k], (int, float)):
                deltas[k] += float(pd[k])
    for k in PRACTICE_FIELDS:
        delta = max(-cap, min(cap, deltas[k]))
        setattr(p, k, clamp(getattr(p, k) + delta))
    p.clamp_all()
