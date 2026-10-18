from __future__ import annotations

from typing import Any

from v3.core.derived import compute_insulation_score
from v3.core.state import BackboneState, clamp

_BUFFER_TO_MODE = {
    "guilt": "self_blame",
    "colonial_justification": "denial_normalization",
    "resignation": "compartmentalization",
    "not_my_concern": "denial_normalization",
    "liberal_utopian_blur": "cynical_partial_breakthrough",
    "piety": "religious_surrender",
    "ideology": "nationalism_or_state_identification",
    "craft": "career_identity",
    "intimacy": "family_duty",
    "work": "career_identity",
    "intoxication": "consumer_sedation",
    "status": "career_identity",
    "family_role": "family_duty",
    "health_regimen": "wellness_privatization",
    "escapism": "consumer_sedation",
}

_CHANNEL_TO_MODE = {
    "humor_irony": "compartmentalization",
    "hyper_competence": "career_identity",
    "caretaking_warmth": "family_duty",
    "piety_ritual": "religious_surrender",
    "aesthetic_intensification": "aestheticized_malaise",
    "withdrawal_numbness": "compartmentalization",
    "micro_authoritarianism": "reactionary_displacement",
    "conspiracy_symbolic": "reactionary_displacement",
    "quiet_organizing": "collective_holding",
    "somatic_irritability": "wellness_privatization",
}

_MODE_TO_SHELTER = {
    "denial_normalization": "sealed_normality",
    "self_blame": "self_accusing_frame",
    "family_duty": "family_role_container",
    "religious_surrender": "ritual_prayer_surrender",
    "spiritual_bypass": "ritual_escape",
    "consumer_sedation": "sedation_loop",
    "career_identity": "role_performance_frame",
    "wellness_privatization": "body_management_frame",
    "nationalism_or_state_identification": "state_allegiance_frame",
    "reactionary_displacement": "enemy_projection_frame",
    "aestheticized_malaise": "aesthetic_private_world",
    "cynical_partial_breakthrough": "partial_breakthrough_frame",
    "compartmentalization": "sealed_compartment",
    "collective_holding": "mutual_aid_container",
}


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


def derive_insulation_profile(
    state: BackboneState,
    domain_name: str,
    charge_item: dict[str, Any],
    vessel_profile: dict[str, Any],
    memory: dict[str, Any],
) -> dict[str, str]:
    domain = state.domains.get(domain_name)
    buffer_type = str(getattr(domain, "buffer_type", "") or "")
    channel = str(charge_item.get("primary_channel") or vessel_profile.get("vessel_hint") or "fallback_channel_container")
    mode = _BUFFER_TO_MODE.get(buffer_type) or _CHANNEL_TO_MODE.get(channel, "compartmentalization")

    insulation_score = compute_insulation_score(state)
    practice = state.practice_stack
    collective = _safe_float(getattr(state.collective_infrastructure, "network_density", 0.0), 0.0)
    organizing = _safe_float(getattr(practice, "organizing", 0.0), 0.0)
    care = _safe_float(getattr(practice, "care", 0.0), 0.0)
    spiritual = _safe_float(getattr(practice, "spiritual", 0.0), 0.0)
    study = _safe_float(getattr(practice, "study", 0.0), 0.0)
    health = _safe_float(getattr(state.capacity, "health", 0.0), 0.0)

    if channel == "piety_ritual" and spiritual >= 35.0:
        mode = "religious_surrender"
    elif mode == "religious_surrender" and spiritual < 35.0:
        mode = "spiritual_bypass"
    if channel == "quiet_organizing" and (collective >= 35.0 or organizing >= 35.0):
        mode = "collective_holding"
    elif mode == "collective_holding" and collective < 35.0 and organizing < 35.0:
        mode = "compartmentalization"
    if mode == "family_duty" and care < 20.0:
        mode = "compartmentalization"
    if mode == "career_identity" and max(study, organizing) < 25.0:
        mode = "compartmentalization"
    if channel == "conspiracy_symbolic" and mode == "nationalism_or_state_identification":
        mode = "reactionary_displacement"

    if buffer_type or channel != "fallback_channel_container":
        confidence_seed = 0.20
    else:
        confidence_seed = 0.05
    confidence_seed += min(0.30, insulation_score / 200.0)
    confidence_seed += min(0.20, (organizing + collective + care + spiritual + health) / 500.0)
    if mode == "religious_surrender" and spiritual >= 70.0:
        confidence_seed += 0.35
    if mode == "collective_holding" and max(collective, organizing) >= 70.0:
        confidence_seed += 0.35
    if mode == "career_identity" and max(study, organizing) >= 70.0:
        confidence_seed += 0.20
    if mode == "family_duty" and care >= 70.0:
        confidence_seed += 0.20
    if memory.get("recent_dominant_channel_by_domain", {}).get(domain_name) == channel:
        confidence_seed += 0.10
    if memory.get("dominant_channel_by_domain", {}).get(domain_name) == channel:
        confidence_seed += 0.05
    if mode == "compartmentalization" and not buffer_type and channel == "fallback_channel_container":
        confidence_seed = 0.10

    confidence_seed = clamp(confidence_seed, 0.0, 1.0)
    confidence = _confidence_label(confidence_seed)
    if confidence == "high":
        status = "high_confidence"
    elif confidence == "medium":
        status = "medium_confidence"
    else:
        status = "low_confidence_fallback"

    cognitive_shelter = _MODE_TO_SHELTER.get(mode, "sealed_compartment")
    if confidence == "low" and mode == "compartmentalization":
        cognitive_shelter = "fallback_channel_container"

    return {
        "insulation_mode": mode,
        "cognitive_shelter": cognitive_shelter,
        "insulation_confidence": confidence,
        "insulation_status": status,
    }
