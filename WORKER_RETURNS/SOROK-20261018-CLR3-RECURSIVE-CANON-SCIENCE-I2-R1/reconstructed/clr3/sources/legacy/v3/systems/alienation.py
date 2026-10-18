# v3/systems/alienation.py — update alienation from events; apply delta cap.
# Mis_aim_risk (derived) is recomputed after cracks_and_alienation step.

from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState, clamp
from v3.core.derived import DerivedIndices

DEFAULT_DELTA_CAP = 15


def _get_delta_cap(config: dict[str, Any]) -> float:
    """Annual delta cap for alienation (v3config delta_caps.alienation)."""
    caps = config.get("delta_caps") or {}
    return float(caps.get("alienation", DEFAULT_DELTA_CAP))


def update_alienation(
    state: BackboneState,
    derived: DerivedIndices,
    config: dict[str, Any],
) -> None:
    """Update state.alienation_vector from event-driven deltas (distribute to all dimensions); respect annual cap. Sync state.alienation from vector aggregate."""
    cap = _get_delta_cap(config)
    delta_sum = 0.0
    for ev in state.events_this_year:
        if not isinstance(ev, dict):
            continue
        d = ev.get("alienation_delta")
        if isinstance(d, (int, float)):
            delta_sum += float(d)
    delta_sum = max(-cap, min(cap, delta_sum))
    # New aggregate; set all dimensions to it (event deltas shift overall alienation; dimensions can diverge via future capacity/domain derivation)
    new_agg = clamp(state.alienation_vector.aggregate() + delta_sum)
    v = state.alienation_vector
    v.structural = v.affective = v.institutional = new_agg
    state.alienation = new_agg
