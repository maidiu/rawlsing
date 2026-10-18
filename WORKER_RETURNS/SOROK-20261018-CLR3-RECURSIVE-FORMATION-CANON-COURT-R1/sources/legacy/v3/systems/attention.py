# v3/systems/attention.py — update attention_field_exposure and capture_pressure from config formulas; apply delta caps.

from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState, clamp
from v3.core.derived import DerivedIndices

DEFAULT_ATTENTION_CAP = 15
DEFAULT_CAPTURE_CAP = 15


def _get_attention_cap(config: dict[str, Any]) -> float:
    caps = config.get("delta_caps") or {}
    return float(caps.get("attention_exposure", DEFAULT_ATTENTION_CAP))


def _get_capture_cap(config: dict[str, Any]) -> float:
    caps = config.get("delta_caps") or {}
    return float(caps.get("capture_pressure", DEFAULT_CAPTURE_CAP))


def update_attention_and_capture(
    state: BackboneState,
    derived: DerivedIndices,
    config: dict[str, Any],
) -> None:
    """Update attention_field_exposure from weighted sum (opportunity, craft_talent, intensity) + noise; capture from attention minus infrastructure. Caps limit annual change."""
    att_cfg = (config.get("attention_system") or {}).get("attention_exposure") or {}
    cap_cfg = (config.get("attention_system") or {}).get("capture_pressure") or {}
    weights_att = att_cfg.get("weights") or {"opportunity_access": 0.40, "craft_talent": 0.35, "intensity": 0.25}
    weights_cap = cap_cfg.get("weights") or {"attention_field_exposure": 0.70, "org_discipline": -0.20, "network_density": -0.10}
    noise_range = att_cfg.get("annual_noise_range") or [-5, 5]
    floor_attention = float(cap_cfg.get("floor_at_attention_min", 50))

    ic = state.intensity_and_capture
    inf = state.collective_infrastructure

    # Target attention: weighted sum + noise
    target_att = (
        weights_att.get("opportunity_access", 0) * ic.opportunity_access
        + weights_att.get("craft_talent", 0) * ic.craft_talent
        + weights_att.get("intensity", 0) * ic.intensity
    )
    lo, hi = (noise_range[0], noise_range[1]) if isinstance(noise_range, (list, tuple)) and len(noise_range) >= 2 else (-5, 5)
    # Deterministic noise from state so runs are reproducible
    seed = (state.year * 31 + int(ic.intensity) + int(ic.opportunity_access)) & 0x7FFFFFFF
    t = (seed % 1000) / 1000.0
    target_att += lo + t * (hi - lo)
    target_att = clamp(target_att)

    # Move toward target by cap
    cap_att = _get_attention_cap(config)
    delta_att = max(-cap_att, min(cap_att, target_att - ic.attention_field_exposure))
    ic.attention_field_exposure = clamp(ic.attention_field_exposure + delta_att)

    # Target capture: attention minus infrastructure terms; floor when attention low
    raw_cap = (
        weights_cap.get("attention_field_exposure", 0) * ic.attention_field_exposure
        + weights_cap.get("org_discipline", 0) * inf.org_discipline
        + weights_cap.get("network_density", 0) * inf.network_density
    )
    if ic.attention_field_exposure < floor_attention and floor_attention > 0:
        raw_cap *= max(0.0, ic.attention_field_exposure / floor_attention)
    target_cap = clamp(raw_cap)

    cap_cap = _get_capture_cap(config)
    delta_cap = max(-cap_cap, min(cap_cap, target_cap - ic.capture_pressure))
    ic.capture_pressure = clamp(ic.capture_pressure + delta_cap)
    ic.clamp_all()
