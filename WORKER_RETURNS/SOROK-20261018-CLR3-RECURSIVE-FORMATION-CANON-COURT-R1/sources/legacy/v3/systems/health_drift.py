# v3/systems/health_drift.py — composite health drift from stability/support (revision 2026.02.25).

from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState, clamp
from v3.core.derived import DerivedIndices

HEALTH_DRIFT_CAP = 1.5  # max magnitude per year
WOUND_DECAY_RATE = 0.5   # points/year drift toward 50.0 baseline
WOUND_DECAY_CAP = 1.0    # max movement per wound per year


def update_health_drift(
    state: BackboneState,
    derived: DerivedIndices,
    config: dict[str, Any],
) -> None:
    """Apply small drift to Capacity.health: down if stability_threshold high; up if insulation/support high and stability low."""
    stability = getattr(derived, "stability_threshold", 0.0)
    insulation = getattr(derived, "insulation_score", 0.0)
    support = state.capacity.social_support
    health = state.capacity.health

    # Downward pressure from brittleness
    down = stability / 100.0 * 0.8
    # Upward from insulation and support when stability not extreme
    up = 0.0
    if stability < 70.0:
        up = (insulation / 100.0 * 0.5) + (support / 100.0 * 0.4)
    delta = up - down
    delta = max(-HEALTH_DRIFT_CAP, min(HEALTH_DRIFT_CAP, delta))
    state.capacity.health = clamp(health + delta)
    state.capacity.clamp_all()

    # Passive wound decay: wounds drift toward 50.0 each year at WOUND_DECAY_RATE.
    # Elevated wounds (> 50) decay downward; suppressed wounds (< 50) recover upward.
    # Rate is small so that repeated reactivation keeps wounds elevated, but without reactivation
    # wounds slowly heal. social_support and health above baseline accelerate recovery slightly.
    recovery_bonus = 0.0
    if support > 60.0:
        recovery_bonus += (support - 60.0) / 100.0 * 0.3  # up to +0.12 extra decay
    if health > 60.0:
        recovery_bonus += (health - 60.0) / 100.0 * 0.2   # up to +0.08 extra decay

    wv = state.wound_vector
    for field in ("shame", "fear", "anger", "abandonment", "control", "recognition", "loss"):
        if not hasattr(wv, field):
            continue
        cur = float(getattr(wv, field))
        if cur > 50.0:
            decay = min(WOUND_DECAY_CAP, WOUND_DECAY_RATE + recovery_bonus)
            setattr(wv, field, max(50.0, cur - decay))
        elif cur < 50.0:
            recovery = min(WOUND_DECAY_CAP, WOUND_DECAY_RATE * 0.5)
            setattr(wv, field, min(50.0, cur + recovery))
    wv.clamp_all()

    # impunity_access: drifts toward (money * 0.6 + job_security * 0.4).
    # Wealthy, secure personas accumulate structural impunity over time;
    # precarious personas lose it. Enables the to_extractive topology transition at >= 50.
    pr = state.peak_routing
    _job_sec = 100.0 - state.reproduction_constraints.job_insecurity
    _impunity_target = clamp(state.capacity.money * 0.6 + _job_sec * 0.4)
    _impunity_delta = max(-2.0, min(2.0, (_impunity_target - pr.impunity_access) * 0.08))
    pr.impunity_access = max(0.0, min(100.0, pr.impunity_access + _impunity_delta))

    # intensity: engagement depth — drifts toward target driven by active magnet count
    # + social_support. More embedded in a field (magnets) + more connected → higher intensity.
    # No other write path exists; without this intensity stays at init value forever.
    ic = state.intensity_and_capture
    _magnet_count = len(getattr(state, "active_magnets", []) or [])
    _magnet_contribution = min(70.0, 30.0 + _magnet_count * 4.0)
    _intensity_target = clamp(_magnet_contribution * 0.6 + state.capacity.social_support * 0.4)
    _intensity_delta = max(-3.0, min(3.0, (_intensity_target - ic.intensity) * 0.10))
    ic.intensity = clamp(ic.intensity + _intensity_delta)

    # Annual drift for craft_talent and opportunity_access — give them live write paths
    # so attention_field_exposure stays meaningful over the life course.
    ic = state.intensity_and_capture
    # craft_talent drifts toward practice_stack.craft (accumulated craft practice builds talent).
    # One-directional: talent only grows from practice, never degrades because practice_stack.craft
    # temporarily reads below the seeded baseline. Cap raised to 3.0/yr to reduce lag for dedicated practitioners.
    craft_target = float(getattr(state.practice_stack, "craft", 50.0))
    craft_delta = max(0.0, min(3.0, (craft_target - ic.craft_talent) * 0.12))
    ic.craft_talent = clamp(ic.craft_talent + craft_delta)
    # opportunity_access drifts toward composite of field economy and job security
    _economy = 50.0
    if state.field and isinstance(getattr(state.field, "raw", None), dict):
        _economy = float(state.field.raw.get("economy", 50.0))
    _job_security = 100.0 - state.reproduction_constraints.job_insecurity
    opp_target = clamp(_economy * 0.5 + _job_security * 0.5)
    opp_delta = max(-3.0, min(3.0, (opp_target - ic.opportunity_access) * 0.10))
    ic.opportunity_access = clamp(ic.opportunity_access + opp_delta)
    ic.clamp_all()

    # practice_stack: magnet-driven annual floor contribution.
    # Sustained field embedding produces practice accumulation independent of LLM event sampling,
    # which historically under-generates practice events. Each arts/craft magnet contributes
    # 1.0 pt/yr to craft (cap 5/yr); each mentor/teacher magnet 1.0 pt/yr to study (cap 3/yr);
    # each community/organizing magnet 1.0 pt/yr to organizing (cap 3/yr).
    _magnets = getattr(state, "active_magnets", None) or []
    _arts_count = 0
    _mentor_count = 0
    _community_count = 0
    for _m in _magnets:
        _mlabel = str(
            (_m.get("label") or _m.get("id") or "") if isinstance(_m, dict)
            else (getattr(_m, "label", None) or getattr(_m, "id", None) or "")
        ).lower()
        _mtype = str(
            (_m.get("magnet_type") or "") if isinstance(_m, dict)
            else (getattr(_m, "magnet_type", None) or "")
        ).lower()
        if any(kw in _mlabel for kw in (
            "art", "music", "aesthetic", "creative", "culture", "craft",
            "film", "theater", "theatre", "dance", "poetry", "novel", "studio",
        )):
            _arts_count += 1
        if _mtype in ("mentor", "teacher"):
            _mentor_count += 1
        if any(kw in _mlabel for kw in (
            "community", "movement", "organiz", "collective", "union",
            "activist", "campaign", "neighborhood",
        )):
            _community_count += 1

    _care_count = 0
    _risk_count = 0
    for _m in _magnets:
        _mlabel = str(
            (_m.get("label") or _m.get("id") or "") if isinstance(_m, dict)
            else (getattr(_m, "label", None) or getattr(_m, "id", None) or "")
        ).lower()
        _mtype = str(
            (_m.get("magnet_type") or "") if isinstance(_m, dict)
            else (getattr(_m, "magnet_type", None) or "")
        ).lower()
        if any(kw in _mlabel for kw in (
            "famil", "parent", "sibling", "child", "partner", "spouse",
            "caregiv", "elderl", "infant", "baby",
        )) or _mtype == "romance":
            _care_count += 1
        if any(kw in _mlabel for kw in (
            "activist", "protest", "militia", "soldier", "militar", "guerrilla",
            "campaign", "risk", "underground", "resistance",
        )) or (_mtype == "leader" and any(kw in _mlabel for kw in ("movement", "organiz", "campaign"))):
            _risk_count += 1

    ps = state.practice_stack
    if _arts_count > 0:
        ps.craft = min(100.0, ps.craft + min(5.0, _arts_count * 1.0))
    if _mentor_count > 0:
        ps.study = min(100.0, ps.study + min(3.0, _mentor_count * 1.0))
    if _community_count > 0:
        ps.organizing = min(100.0, ps.organizing + min(3.0, _community_count * 1.0))
    if _care_count > 0:
        ps.care = min(100.0, ps.care + min(3.0, _care_count * 1.0))
    if _risk_count > 0:
        ps.risk_training = min(100.0, ps.risk_training + min(3.0, _risk_count * 1.0))
    ps.clamp_all()
