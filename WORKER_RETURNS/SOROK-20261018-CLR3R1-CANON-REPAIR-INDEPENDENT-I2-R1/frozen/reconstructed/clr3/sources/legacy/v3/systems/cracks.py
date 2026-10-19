# v3/systems/cracks.py — update crack intensity/latent_pressure from events; apply delta caps.
# Mis_aim_risk (derived) depends on alienation; cracks affect downstream steps. Limits from config.

from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState, clamp
from v3.core.derived import DerivedIndices

# Default per-crack annual delta cap for intensity and latent_pressure (no single key in v3config; use intensify_range max).
DEFAULT_CRACK_DELTA_CAP = 20


def _get_crack_delta_cap(config: dict[str, Any]) -> float:
    """Cap for per-crack intensity/latent_pressure deltas from events."""
    rules = config.get("cracks_rules") or {}
    annual = rules.get("annual_update") or {}
    ir = annual.get("intensify_range")
    if isinstance(ir, (list, tuple)) and len(ir) >= 2:
        return float(ir[1])  # max of range
    return DEFAULT_CRACK_DELTA_CAP


def update_cracks(
    state: BackboneState,
    derived: DerivedIndices,
    config: dict[str, Any],
) -> None:
    """Apply event-driven deltas to crack intensity and latent_pressure; respect caps and list limits. plasticity_window.crack_rewrite_probability scales cap (higher = larger allowed deltas)."""
    cap = _get_crack_delta_cap(config)
    pw = getattr(state, "plasticity_window", None) or {}
    rewrite_prob = int(pw.get("crack_rewrite_probability", 10))
    cap = cap * (0.8 + (rewrite_prob / 100.0) * 0.4)
    cap = max(5.0, min(40.0, cap))
    cracks = state.cracks
    if not cracks:
        return
    # Sum deltas per index from events. Event: {"crack_deltas": [{"intensity": 5, "latent_pressure": 10}, ...]}
    n = len(cracks)
    intensity_deltas = [0.0] * n
    latent_deltas = [0.0] * n
    for ev in state.events_this_year:
        if not isinstance(ev, dict):
            continue
        cd = ev.get("crack_deltas")
        if not isinstance(cd, list):
            continue
        for i, item in enumerate(cd):
            if i >= n or not isinstance(item, dict):
                continue
            if "intensity" in item and isinstance(item["intensity"], (int, float)):
                intensity_deltas[i] += float(item["intensity"])
            if "latent_pressure" in item and isinstance(item["latent_pressure"], (int, float)):
                latent_deltas[i] += float(item["latent_pressure"])
    for i, c in enumerate(cracks):
        di = max(-cap, min(cap, intensity_deltas[i]))
        dl = max(-cap, min(cap, latent_deltas[i]))
        c.intensity = clamp(c.intensity + di)
        c.latent_pressure = clamp(c.latent_pressure + dl)
        c.clamp_all()
