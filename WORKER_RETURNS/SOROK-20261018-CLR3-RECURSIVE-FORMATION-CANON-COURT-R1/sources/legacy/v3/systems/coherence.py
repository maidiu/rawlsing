# v3/systems/coherence.py — update peak_routing.coherence from events; apply delta cap.

from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState, clamp
from v3.core.derived import DerivedIndices

DEFAULT_DELTA_CAP = 10


def _get_delta_cap(config: dict[str, Any]) -> float:
    caps = config.get("delta_caps") or {}
    return float(caps.get("coherence", DEFAULT_DELTA_CAP))


def update_coherence(
    state: BackboneState,
    derived: DerivedIndices,
    config: dict[str, Any],
) -> None:
    """Apply event-driven coherence delta; respect annual cap."""
    cap = _get_delta_cap(config)
    delta_sum = 0.0
    for ev in state.events_this_year:
        if not isinstance(ev, dict):
            continue
        d = ev.get("coherence_delta")
        if isinstance(d, (int, float)):
            delta_sum += float(d)
    delta_sum = max(-cap, min(cap, delta_sum))
    pr = state.peak_routing
    pr.coherence = clamp(pr.coherence + delta_sum)
    pr.clamp_all()
