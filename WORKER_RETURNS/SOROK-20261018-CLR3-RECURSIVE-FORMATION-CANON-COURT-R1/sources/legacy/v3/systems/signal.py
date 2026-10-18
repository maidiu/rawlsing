# v3/systems/signal.py — apply signal effects from theory_of_change_style profile; write into field.raw and small capacity/peak nudges.

from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState, clamp
from v3.core.derived import DerivedIndices

SIGNAL_VECTOR_FIELDS = ("morale", "recruitment", "legitimacy", "fear", "defections", "repression_justification")
DEFAULT_MAX_ABS_DELTA = 15


def apply_signal_effects(
    state: BackboneState,
    derived: DerivedIndices,
    config: dict[str, Any],
) -> None:
    """Apply signal profile for current theory_of_change_style (in_group audience); add capped deltas to field.raw and capacity.legitimacy."""
    sig = config.get("strategy_and_signal") or {}
    caps_cfg = sig.get("signal_caps") or {}
    max_delta = float(caps_cfg.get("max_abs_delta_per_field", DEFAULT_MAX_ABS_DELTA))
    profiles = sig.get("default_profiles") or {}
    style = getattr(state.peak_routing, "theory_of_change_style", "institution_building")
    if not isinstance(style, str):
        style = "institution_building"
    profile = profiles.get(style, {}).get("in_group")
    if not isinstance(profile, dict):
        return

    raw = state.field.raw if isinstance(state.field.raw, dict) else {}
    for k, v in profile.items():
        if k not in SIGNAL_VECTOR_FIELDS or not isinstance(v, (int, float)):
            continue
        delta = max(-max_delta, min(max_delta, float(v)))
        current = float(raw.get(k, 50.0)) if isinstance(raw.get(k), (int, float)) else 50.0
        raw[k] = clamp(current + delta)
    state.field.raw = raw

    # Optional: nudge capacity.legitimacy by profile legitimacy (capped)
    if "legitimacy" in profile and isinstance(profile["legitimacy"], (int, float)):
        delta = max(-max_delta, min(max_delta, float(profile["legitimacy"]) * 0.3))
        state.capacity.legitimacy = clamp(state.capacity.legitimacy + delta)
        state.capacity.clamp_all()
