# v3/psyche/vitality.py — vitality capacity + regulation cost (spec § psyche/).

from __future__ import annotations

from typing import Any

from v3.core.derived import compute_insulation_score
from v3.core.state import BackboneState


def vitality_value(state: BackboneState) -> float:
    """Usable life-force from psychological capacity (0–100). Not conserved."""
    return getattr(state.psychological_capacity, "vitality", 50.0)


def regulation_cost(state: BackboneState, config: dict[str, Any] | None = None) -> float:
    """Cost of regulating (e.g. buffers, coherence maintenance). 0–100; stub for future rules."""
    _ = config
    # Stub: could derive from buffers cost_profile, coherence, crack load
    return 0.0


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _age_phase(age: int) -> str:
    if age < 13:
        return "child"
    if age < 20:
        return "adolescent"
    if age < 35:
        return "early_adult"
    if age < 50:
        return "midlife"
    if age < 65:
        return "late_adult"
    return "elder"


def _vitality_band(vitality: float) -> str:
    if vitality < 25.0:
        return "low"
    if vitality < 50.0:
        return "moderate"
    if vitality < 75.0:
        return "high"
    return "vivid"


def _fatigue_band(fatigue: float) -> str:
    if fatigue < 25.0:
        return "light"
    if fatigue < 50.0:
        return "moderate"
    if fatigue < 75.0:
        return "heavy"
    return "severe"


def _future_horizon_band(years: int) -> str:
    if years <= 2:
        return "narrow"
    if years <= 4:
        return "short"
    if years <= 7:
        return "moderate"
    if years <= 10:
        return "extended"
    return "broad"


def _channel_routing_bias(channel: str, vitality: float, fatigue: float) -> str:
    if vitality <= 35.0 or fatigue >= 65.0:
        if channel in ("withdrawal_numbness", "somatic_irritability"):
            return "somatic_or_withdrawal"
    if channel in ("piety_ritual", "quiet_organizing", "hyper_competence"):
        return "active"
    return "balanced"


def derive_vitality_profile(
    state: BackboneState,
    charge_ledger: dict[str, Any],
    memory: dict[str, Any],
) -> dict[str, Any]:
    vitality = max(0.0, min(100.0, _safe_float(getattr(state.psychological_capacity, "vitality", 50.0), 50.0)))
    age = max(0, int(getattr(state, "age", 0) or 0))
    insulation_score = compute_insulation_score(state)
    age_phase = _age_phase(age)
    age_penalty = max(0.0, (age - 30) * 0.25)
    base_fatigue = max(0.0, 100.0 - vitality)

    domains: dict[str, Any] = {}
    total_horizon = 0.0
    total_recovery = 0.0
    total_multiplier = 0.0
    for name, item in charge_ledger.items():
        if not isinstance(item, dict):
            continue
        channel = str(item.get("primary_channel") or "fallback_channel_container")
        current_charge = _safe_float(item.get("current_charge"), 0.0)
        internally_routed_charge = _safe_float(item.get("internally_routed_charge"), 0.0)
        overt_aim_charge = _safe_float(item.get("overt_aim_charge"), 0.0)
        fatigue = max(
            0.0,
            min(
                100.0,
                base_fatigue
                + age_penalty
                + current_charge * 0.04
                + internally_routed_charge * 0.03
                - insulation_score * 0.08,
            ),
        )
        conductance_multiplier = max(
            0.65,
            min(
                1.25,
                1.0
                - fatigue / 240.0
                + insulation_score / 500.0
                + (0.08 if channel in ("withdrawal_numbness", "somatic_irritability") and vitality <= 35.0 else 0.0)
                - (0.05 if channel in ("quiet_organizing", "hyper_competence", "aesthetic_intensification") and vitality <= 35.0 else 0.0),
            ),
        )
        recovery_cost = max(
            0.0,
            min(
                100.0,
                fatigue * 0.65
                + (100.0 - insulation_score) * 0.15
                + current_charge * 0.05
                + overt_aim_charge * 0.03,
            ),
        )
        future_horizon_years = int(
            max(
                1,
                min(
                    12,
                    round(
                        12.0
                        - fatigue / 12.0
                        - age_penalty / 3.0
                        + insulation_score / 20.0,
                    ),
                ),
            )
        )
        future_horizon = _future_horizon_band(future_horizon_years)
        routing_bias = _channel_routing_bias(channel, vitality, fatigue)
        fatigue_band = _fatigue_band(fatigue)
        vitality_band = _vitality_band(vitality)
        domains[name] = {
            "age_phase": age_phase,
            "vitality_band": vitality_band,
            "fatigue_band": fatigue_band,
            "future_horizon": future_horizon,
            "future_horizon_years": future_horizon_years,
            "recovery_cost": round(recovery_cost, 1),
            "conductance_multiplier": round(conductance_multiplier, 3),
            "routing_bias": routing_bias,
        }
        total_horizon += future_horizon_years
        total_recovery += recovery_cost
        total_multiplier += conductance_multiplier

    domain_count = max(1, len(domains))
    global_profile = {
        "age_phase": age_phase,
        "vitality_band": _vitality_band(vitality),
        "fatigue_band": _fatigue_band(base_fatigue),
        "future_horizon": _future_horizon_band(int(round(total_horizon / domain_count)) if domains else 4),
        "future_horizon_years": int(round(total_horizon / domain_count)) if domains else 4,
        "recovery_cost": round(total_recovery / domain_count if domains else base_fatigue, 1),
        "conductance_multiplier": round(total_multiplier / domain_count if domains else 1.0, 3),
        "routing_bias": "somatic_or_withdrawal" if vitality <= 35.0 else "balanced",
    }
    return {
        "schema_version": "v519_vitality_fatigue_age_phase_future_horizon",
        "global": global_profile,
        "domains": domains,
        "memory_view": {
            "recent_dominant_channel_by_domain": dict(memory.get("recent_dominant_channel_by_domain") or {}),
            "dominant_channel_by_domain": dict(memory.get("dominant_channel_by_domain") or {}),
        },
    }
