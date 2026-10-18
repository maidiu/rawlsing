# v3/engine/active_magnets.py — yearly update: intensify/decay persistent magnets (specLLM).

from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState, Magnet

DECAY_PER_YEAR = 2.0
INTENSITY_FLOOR_REMOVE = 15.0
MAX_ACTIVE_MAGNETS = 12
NEW_MAGNET_DEFAULT_INTENSITY = 55.0  # newly selected magnets start here; decay step will reduce over time


def _candidate_to_magnet(c: dict[str, Any], default_intensity: float = NEW_MAGNET_DEFAULT_INTENSITY) -> Magnet:
    """Convert a selected magnet_candidate dict (from LLM/parse) to a Magnet. tenure_years=0."""
    mid = str(c.get("id", ""))[:80] or f"mg_{id(c)}"
    mtype = str(c.get("magnet_type", "friend"))[:40]
    label = str(c.get("label", ""))[:200]
    intensity = float(c.get("intensity", default_intensity))
    intensity = max(0.0, min(100.0, intensity))
    return Magnet(id=mid, magnet_type=mtype, label=label, intensity=intensity, tenure_years=0)


def apply_selected_magnets_to_state(
    state: BackboneState,
    selected_magnets: list[dict[str, Any]],
    config: dict[str, Any] | None = None,
) -> None:
    """
    Persist selected magnet_candidates into state.active_magnets so they appear in
    next year's summary and persona and participate in yearly decay.
    Skips candidates whose id is already in state; caps list at max_active_magnets.
    plasticity_window.magnet_susceptibility boosts new magnet intensity when high.
    """
    if not selected_magnets:
        return
    conf = (config or {}).get("active_magnets") or {}
    max_magnets = int(conf.get("max_active_magnets", MAX_ACTIVE_MAGNETS))
    max_magnets = max(2, min(30, max_magnets))
    default_intensity = float(conf.get("new_magnet_intensity", NEW_MAGNET_DEFAULT_INTENSITY))
    default_intensity = max(0.0, min(100.0, default_intensity))
    pw = getattr(state, "plasticity_window", None) or {}
    susceptibility = int(pw.get("magnet_susceptibility", 10))
    intensity_mult = 0.9 + (susceptibility / 100.0) * 0.2
    default_intensity = min(100.0, default_intensity * intensity_mult)
    existing_ids = {m.id for m in state.active_magnets}
    for c in selected_magnets:
        if not isinstance(c, dict):
            continue
        m = _candidate_to_magnet(c, default_intensity)
        if m.id and m.id not in existing_ids:
            state.active_magnets.append(m)
            existing_ids.add(m.id)
    state.active_magnets = state.active_magnets[:max_magnets]


def update_active_magnets_step(
    state: BackboneState,
    derived: Any,
    config: dict[str, Any],
) -> None:
    """
    Yearly step: decay each magnet's intensity; remove if below floor; cap list size.
    plasticity_window.magnet_susceptibility reduces decay when high (magnets persist longer in plastic phase).
    """
    conf = config.get("active_magnets") or {}
    decay = float(conf.get("decay_per_year", DECAY_PER_YEAR))
    floor = float(conf.get("intensity_floor_remove", INTENSITY_FLOOR_REMOVE))
    max_magnets = int(conf.get("max_active_magnets", MAX_ACTIVE_MAGNETS))
    max_magnets = max(2, min(30, max_magnets))
    pw = getattr(state, "plasticity_window", None) or {}
    susceptibility = int(pw.get("magnet_susceptibility", 10))
    # susceptibility 0–100: at 80+ decay is halved; at 20 decay is 1.2x
    decay_mult = 1.2 - (susceptibility / 100.0) * 0.7
    decay_mult = max(0.4, min(1.3, decay_mult))
    effective_decay = decay * decay_mult

    kept: list[Magnet] = []
    for m in state.active_magnets:
        m.intensity -= effective_decay
        m.tenure_years += 1
        m.clamp_all()
        if m.intensity >= floor:
            kept.append(m)
    state.active_magnets = kept[:max_magnets]
