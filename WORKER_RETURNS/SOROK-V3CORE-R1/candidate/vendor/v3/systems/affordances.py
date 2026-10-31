# v3/systems/affordances.py — affordances from CalibrationRegime + BoundaryMap (spec §5).
# Used by state summary and selection; "Homo Canadus/Homo Palestinianus" shaping without stereotypes.

from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState

# Default channel bands when no calibration
DEFAULT_AVAILABLE_CHANNELS = ["family", "peer", "school", "work", "media", "neighborhood"]
DEFAULT_UNLIKELY_CHANNELS = ["movement", "diaspora", "online"]


def affordances_from_state(state: BackboneState) -> dict[str, Any]:
    """
    Build affordances dict from state.calibration_regime and state.boundary_map.
    Returns: available_channels, unlikely_channels, dream_window, calibration_summary, boundary_per_domain.
    """
    available = list(DEFAULT_AVAILABLE_CHANNELS)
    unlikely = list(DEFAULT_UNLIKELY_CHANNELS)
    dream_window = ""
    calibration_summary: dict[str, Any] = {}
    boundary_per_domain: dict[str, Any] = {}

    cal = getattr(state, "calibration_regime", None)
    if cal is not None:
        calibration_summary = {
            "norm_center": getattr(cal, "norm_center", "middle"),
            "uniqueness_norm": round(getattr(cal, "uniqueness_norm", 50), 1),
            "outlier_penalties": (getattr(cal, "outlier_penalties", None) or [])[:15],
            "outlier_incentives": (getattr(cal, "outlier_incentives", None) or [])[:15],
            "dream_window": (getattr(cal, "dream_window", None) or "")[:300],
        }
        dream_window = calibration_summary.get("dream_window", "") or ""
        for p in (getattr(cal, "outlier_penalties", None) or [])[:20]:
            if isinstance(p, dict):
                topic = (p.get("topic") or p.get("behavior") or "").lower()
                if any(x in topic for x in ("political", "activism", "protest", "state")):
                    if "movement" not in unlikely:
                        unlikely.append("movement")
                    if "state" not in unlikely:
                        unlikely.append("state")
                    break

    bmap = getattr(state, "boundary_map", None) or {}
    if isinstance(bmap, dict):
        for domain_key, entry in list(bmap.items())[:12]:
            if hasattr(entry, "discouraged"):
                boundary_per_domain[str(domain_key)[:80]] = {
                    "discouraged": list(getattr(entry, "discouraged", None) or [])[:20],
                    "permitted": list(getattr(entry, "permitted", None) or [])[:20],
                    "incentivized": list(getattr(entry, "incentivized", None) or [])[:20],
                    "trigger_conditions": list(getattr(entry, "trigger_conditions", None) or [])[:5],
                }

    return {
        "available_channels": available,
        "unlikely_channels": unlikely,
        "dream_window": dream_window,
        "calibration_summary": calibration_summary,
        "boundary_per_domain": boundary_per_domain,
    }
