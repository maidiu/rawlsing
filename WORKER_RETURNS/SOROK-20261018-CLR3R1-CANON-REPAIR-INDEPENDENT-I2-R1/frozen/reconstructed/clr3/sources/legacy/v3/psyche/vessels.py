from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState, clamp

_BOUNDED_VESSEL_HINTS = {
    "humor_irony": ("joke_style_social_distance", "i_use_distance_or_jokes_to_hold_this"),
    "hyper_competence": ("work_study_mastery", "i_need_to_get_better_and_stay_ahead"),
    "caretaking_warmth": ("family_duty_care_role", "people_need_me_and_this_is_what_one_does"),
    "piety_ritual": ("ritual_prayer_surrender", "i_need_ritual_or_surrender_to_hold_this"),
    "aesthetic_intensification": ("aesthetic_private_world", "beauty_or_art_is_where_the_pressure_can_breathe"),
    "withdrawal_numbness": ("bedroom_silence_fantasy", "i_am_tired_negative_or_need_to_be_left_alone"),
    "micro_authoritarianism": ("local_order_control_container", "someone_has_to_keep_order_or_people_will_ruin_things"),
    "conspiracy_symbolic": ("online_enemy_pattern_container", "something_hidden_feels_like_it_is_arranging_this"),
    "quiet_organizing": ("collective_practical_container", "this_can_be_changed_if_we_move_carefully_together"),
    "somatic_irritability": ("wellness_or_body_management", "my_body_is_off_or_everything_gets_under_my_skin"),
}

_FALLBACK_HINT = "fallback_channel_container"
_FALLBACK_ATTRIBUTION = "i_do_not_have_a_clear_read_yet"


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _confidence_label(score: float) -> str:
    if score >= 0.70:
        return "high"
    if score >= 0.40:
        return "medium"
    return "low"


def _practice_signal(state: BackboneState, channel: str) -> float:
    practice = getattr(state, "practice_stack", None)
    if practice is None:
        return 0.0
    signals = {
        "piety_ritual": _safe_float(getattr(practice, "spiritual", 0.0), 0.0),
        "quiet_organizing": max(
            _safe_float(getattr(practice, "organizing", 0.0), 0.0),
            _safe_float(getattr(getattr(state, "collective_infrastructure", None), "network_density", 0.0), 0.0),
        ),
        "hyper_competence": max(
            _safe_float(getattr(practice, "study", 0.0), 0.0),
            _safe_float(getattr(practice, "craft", 0.0), 0.0),
        ),
        "caretaking_warmth": _safe_float(getattr(practice, "care", 0.0), 0.0),
        "withdrawal_numbness": _safe_float(getattr(practice, "risk_training", 0.0), 0.0),
        "micro_authoritarianism": _safe_float(getattr(getattr(state, "peak_routing", None), "coherence", 0.0), 0.0),
        "conspiracy_symbolic": _safe_float(getattr(getattr(state, "psychological_capacity", None), "reality_anchor", 0.0), 0.0),
        "aesthetic_intensification": _safe_float(getattr(getattr(state, "style_traits", None), "aesthetic_sensitivity", 0.0), 0.0),
        "somatic_irritability": _safe_float(getattr(getattr(state, "capacity", None), "health", 0.0), 0.0),
        "humor_irony": _safe_float(getattr(getattr(state, "style_traits", None), "absurdist_humor", 0.0), 0.0),
    }
    return signals.get(channel, 0.0)


def derive_attribution_and_vessel_hint(
    state: BackboneState,
    domain_name: str,
    channel: str,
    charge_item: dict[str, Any],
    memory: dict[str, Any],
) -> dict[str, str]:
    """Derive a bounded attribution/vessel surface from repo-grounded signals."""
    channel = str(channel or "fallback_channel_container")
    base_hint, base_attribution = _BOUNDED_VESSEL_HINTS.get(channel, (_FALLBACK_HINT, _FALLBACK_ATTRIBUTION))
    current_charge = clamp(_safe_float(charge_item.get("current_charge"), 0.0), 0.0, 100.0)
    overt_aim_charge = clamp(_safe_float(charge_item.get("overt_aim_charge"), 0.0), 0.0, 100.0)
    internally_routed_charge = clamp(_safe_float(charge_item.get("internally_routed_charge"), 0.0), 0.0, 100.0)

    score = 0.18
    if current_charge > 0.0:
        score += 0.18
    if internally_routed_charge > 0.0:
        score += 0.10
    if overt_aim_charge > 0.0:
        score += 0.05

    practice_signal = _practice_signal(state, channel)
    score += min(0.30, practice_signal / 200.0)

    recent = memory.get("recent_dominant_channel_by_domain") if isinstance(memory.get("recent_dominant_channel_by_domain"), dict) else {}
    dominant = memory.get("dominant_channel_by_domain") if isinstance(memory.get("dominant_channel_by_domain"), dict) else {}
    if recent.get(domain_name) == channel:
        score += 0.12
    if dominant.get(domain_name) == channel:
        score += 0.08

    if channel == "conspiracy_symbolic":
        score = min(score, 0.55)
        base_attribution = "something_hidden_feels_like_it_is_arranging_this"

    if current_charge <= 0.0 and internally_routed_charge <= 0.0 and practice_signal <= 0.0:
        base_hint = _FALLBACK_HINT
        base_attribution = _FALLBACK_ATTRIBUTION
        score = 0.10

    score = clamp(score, 0.0, 1.0)
    confidence = _confidence_label(score)
    if confidence == "high":
        vessel_status = "high_confidence"
    elif confidence == "medium":
        vessel_status = "medium_confidence"
    else:
        vessel_status = "low_confidence_fallback"

    return {
        "vessel_hint": base_hint,
        "ordinary_attribution": base_attribution,
        "attribution_confidence": confidence,
        "vessel_status": vessel_status,
    }
