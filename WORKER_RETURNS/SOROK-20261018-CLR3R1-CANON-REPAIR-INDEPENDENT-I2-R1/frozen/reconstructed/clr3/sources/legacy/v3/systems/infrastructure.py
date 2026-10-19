# v3/systems/infrastructure.py — update collective infrastructure from events; apply delta cap.

from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState, clamp
from v3.core.derived import DerivedIndices

INFRASTRUCTURE_FIELDS = (
    "network_density",
    "org_discipline",
    "resource_pool",
    "repression_pressure",
    "elite_splits",
)
DEFAULT_DELTA_CAP = 15


def _get_delta_cap(config: dict[str, Any]) -> float:
    caps = config.get("delta_caps") or {}
    return float(caps.get("infrastructure_fields", DEFAULT_DELTA_CAP))


def update_collective_infrastructure(
    state: BackboneState,
    derived: DerivedIndices,
    config: dict[str, Any],
) -> None:
    """Apply event-driven deltas to collective_infrastructure; respect annual cap per field."""
    cap = _get_delta_cap(config)
    inf = state.collective_infrastructure
    deltas = {k: 0.0 for k in INFRASTRUCTURE_FIELDS}
    for ev in state.events_this_year:
        if not isinstance(ev, dict):
            continue
        id_ = ev.get("infrastructure_deltas")
        if not isinstance(id_, dict):
            continue
        for k in INFRASTRUCTURE_FIELDS:
            if k in id_ and isinstance(id_[k], (int, float)):
                deltas[k] += float(id_[k])
    for k in INFRASTRUCTURE_FIELDS:
        delta = max(-cap, min(cap, deltas[k]))
        setattr(inf, k, clamp(getattr(inf, k) + delta))
    inf.clamp_all()
