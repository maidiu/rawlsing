# v3/systems/style.py — style trait drift from events; apply delta cap.

from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState, clamp
from v3.core.derived import DerivedIndices

STYLE_FIELDS = (
    "playfulness", "novelty_seeking", "conscientiousness", "social_energy",
    "absurdist_humor", "aesthetic_sensitivity", "impulsivity",
)
DEFAULT_DELTA_CAP = 10


def _get_delta_cap(config: dict[str, Any]) -> float:
    drift = config.get("style_drift") or {}
    cap = drift.get("max_delta_per_year")
    if isinstance(cap, (int, float)):
        return float(cap)
    return DEFAULT_DELTA_CAP


def update_style_traits(
    state: BackboneState,
    derived: DerivedIndices,
    config: dict[str, Any],
) -> None:
    """Apply event-driven style_trait_deltas; respect annual cap per field."""
    cap = _get_delta_cap(config)
    st = state.style_traits
    deltas = {k: 0.0 for k in STYLE_FIELDS}
    for ev in state.events_this_year:
        if not isinstance(ev, dict):
            continue
        sd = ev.get("style_trait_deltas")
        if not isinstance(sd, dict):
            continue
        for k in STYLE_FIELDS:
            if k in sd and isinstance(sd[k], (int, float)):
                deltas[k] += float(sd[k])
    for k in STYLE_FIELDS:
        delta = max(-cap, min(cap, deltas[k]))
        setattr(st, k, clamp(getattr(st, k) + delta))
    st.clamp_all()
