# v3/engine/scoring.py
# Wave 4: Score candidates (age_fit, channel_available, salience_fit, hostage_fit, capacity_fit,
# wound_fit, novelty_penalty, coercion_penalty); select ≤2 major, ≤2 minor, ≤1 surprise.
# Reference: specLLM.txt, OVERVIEW_INTEGRATED.md §13.

from __future__ import annotations

import random
from typing import Any

# Weights per specLLM (sum = 1.0; novelty and coercion are penalties).
WEIGHT_AGE_FIT = 0.20
WEIGHT_CHANNEL_AVAILABLE = 0.15
WEIGHT_SALIENCE_FIT = 0.15
WEIGHT_WOUND_FIT = 0.15
WEIGHT_CAPACITY_FIT = 0.15
WEIGHT_HOSTAGE_FIT = 0.10
WEIGHT_NOVELTY_PENALTY = -0.05
WEIGHT_COERCION_PENALTY = -0.05
# Bonus when event attaches to an active striving (GAP_AND_NEXT_STEPS: 70% attach to strivings)
STRIVING_ATTACH_BONUS = 0.05

MAJOR_MAX = 2
MINOR_MAX = 2
SURPRISE_MAX = 1
SURPRISE_PROBABILITY = 0.10
SHOCK_MAX_PER_SELECTION = 1  # at most one shock in selected set
# 70% of major events should attach to a striving when candidates allow (spec / GAP Tier 3)
STRIVING_ATTACH_MAJOR_FRACTION = 0.70


def score_event_candidate(
    event: dict[str, Any],
    state_summary: dict[str, Any],
) -> float:
    """Score one event candidate 0..1. Uses state_summary (Pass 1 input shape)."""
    age = state_summary.get("age", 30)
    field = state_summary.get("field") or {}
    affordances = field.get("affordances") or {}
    available = set((affordances.get("available_channels") or []))
    unlikely = set((affordances.get("unlikely_channels") or []))
    hostage_index = field.get("hostage_index") or 0
    capacity = state_summary.get("capacity") or {}
    wound = state_summary.get("wound") or {}

    channels = set((event.get("channels") or []))
    intensity = (event.get("intensity") or "minor").strip().lower()
    kind = (event.get("kind") or "relationship").strip().lower()

    # Age fit: shock and violence less plausible for very young/old; opportunity/relationship spread
    age_fit = 1.0
    if intensity == "shock" and (age < 10 or age > 70):
        age_fit = 0.3
    elif kind in ("violence", "humiliation") and age < 14:
        age_fit = 0.5
    elif kind in ("opportunity", "achievement") and 18 <= age <= 55:
        age_fit = 1.0

    # Channel available: 1 if all in available, 0.5 if any in unlikely, 0.2 if not in available (shock can override)
    channel_available = 1.0
    if channels:
        in_available = sum(1 for c in channels if c in available)
        in_unlikely = sum(1 for c in channels if c in unlikely)
        if in_available == len(channels):
            channel_available = 1.0
        elif in_unlikely > 0 and intensity != "shock":
            channel_available = 0.5
        else:
            channel_available = 0.7 if intensity == "shock" else 0.3

    # Salience fit: frameworks_active and implicated domains overlap (simplified)
    frameworks_active = state_summary.get("frameworks_active") or []
    implicated = event.get("implicated") or {}
    implicated_domains = set((implicated.get("domains") or []))
    salience_fit = 1.0 if not implicated_domains else 0.7  # no domain list in summary; neutral

    # Hostage fit: high hostage → prefer low-cost events
    hostage_fit = 1.0
    if hostage_index > 60:
        hostage_fit = 0.6
    elif hostage_index > 40:
        hostage_fit = 0.85

    # Capacity fit: use vitality, agency, coherence from summary
    vitality = (capacity.get("vitality") or 50) / 100.0
    agency = (capacity.get("agency") or 50) / 100.0
    coherence = (capacity.get("coherence") or 50) / 100.0
    capacity_fit = (vitality + agency + coherence) / 3.0
    if intensity == "shock" and (vitality < 0.4 or coherence < 0.4):
        capacity_fit *= 0.7

    # Wound fit: event wound_hooks vs wound sensitivities; hook match + high sensitivity => more plausible for this person
    wound_hooks = (event.get("hooks") or {}).get("wound_hooks") or []
    if not isinstance(wound_hooks, list):
        wound_hooks = []
    wound_hooks = [str(h).strip().lower() for h in wound_hooks if isinstance(h, (str, int, float))]
    wound_fit = 0.7  # neutral when no hooks
    if wound_hooks and wound:
        sensitivities = {k: (wound.get(k) or 50) / 100.0 for k in wound if k != "default_channels"}
        matches = [sensitivities.get(h, 0.5) for h in wound_hooks if h in sensitivities]
        if matches:
            wound_fit = 0.5 + 0.5 * (sum(matches) / len(matches))  # higher sensitivity => higher fit

    # Novelty penalty: we have no "recent events" here; use 0
    novelty_penalty = 0.0

    # Coercion penalty: if repression/coercion high, some events less plausible
    coercion_penalty = 0.0
    salient_strata = field.get("salient_strata") or []
    if salient_strata:
        avg_coercion = sum(s.get("coercion", 50) for s in salient_strata if isinstance(s, dict)) / max(len(salient_strata), 1)
        if avg_coercion > 70 and kind in ("opportunity", "achievement"):
            coercion_penalty = 0.2

    # Boundary fit: event positions vs boundary_map discouraged/permitted/incentivized (spec §5)
    boundary_fit = 1.0
    boundary_map = state_summary.get("boundary_map") or {}
    event_positions = (
        event.get("implicated") or {}
    ).get("positions") or event.get("boundary_positions") or []
    if isinstance(event_positions, list):
        event_positions = [str(p).strip().lower() for p in event_positions if p][:20]
    else:
        event_positions = []
    if boundary_map and event_positions:
        in_discouraged = False
        in_incentivized = False
        for domain_key, entry in boundary_map.items():
            if not isinstance(entry, dict):
                continue
            discouraged = [str(x).strip().lower() for x in (entry.get("discouraged") or []) if x][:30]
            incentivized = [str(x).strip().lower() for x in (entry.get("incentivized") or []) if x][:30]
            for pos in event_positions:
                if pos in discouraged:
                    in_discouraged = True
                    break
                if pos in incentivized:
                    in_incentivized = True
            if in_discouraged:
                break
        if in_discouraged:
            boundary_fit = 0.4
        elif in_incentivized:
            boundary_fit = 1.1

    # Rupture assumption fit (specLLM): epistemic_rupture must violate a declared assumed_rule
    rupture_assumption_fit = 1.0
    if kind == "epistemic_rupture":
        rupture = event.get("rupture") or {}
        violated = str(rupture.get("violated_assumption") or "").strip().lower()
        child = state_summary.get("child_model") or {}
        assumed = list(child.get("assumed_rules") or [])
        if violated and assumed:
            assumed_norm = [str(r).strip().lower() for r in assumed if r]
            match = any(violated in a or a in violated for a in assumed_norm)
            if not match:
                rupture_assumption_fit = 0.35  # down-rank if rupture doesn't match any assumed rule
        elif violated and not assumed:
            rupture_assumption_fit = 0.7  # no child_model rules => mild penalty

    # Striving attachment: boost events that reference an active striving (LLM may set striving_object_id)
    striving_ids = {s.get("id") for s in (state_summary.get("striving_objects") or []) if s.get("id")}
    striving_bonus = STRIVING_ATTACH_BONUS if (event.get("striving_object_id") in striving_ids) else 0.0

    score = (
        WEIGHT_AGE_FIT * age_fit
        + WEIGHT_CHANNEL_AVAILABLE * channel_available
        + WEIGHT_SALIENCE_FIT * salience_fit
        + WEIGHT_HOSTAGE_FIT * hostage_fit
        + WEIGHT_CAPACITY_FIT * capacity_fit
        + WEIGHT_WOUND_FIT * wound_fit
        + WEIGHT_NOVELTY_PENALTY * novelty_penalty
        + WEIGHT_COERCION_PENALTY * coercion_penalty
    )
    score += striving_bonus
    score *= boundary_fit
    score *= rupture_assumption_fit
    return max(0.0, min(1.0, score))


def score_magnet_candidate(
    magnet: dict[str, Any],
    state_summary: dict[str, Any],
) -> float:
    """Score one magnet candidate 0..1. Higher plasticity_window.magnet_susceptibility boosts score (more likely to adopt magnets)."""
    capacity = state_summary.get("capacity") or {}
    binding = (capacity.get("binding") or 50) / 100.0
    agency = (capacity.get("agency") or 50) / 100.0
    base = 0.6 + 0.2 * binding + 0.2 * agency
    rp = state_summary.get("rupture_plasticity") or {}
    susceptibility = int(rp.get("magnet_susceptibility", 10))
    # 0–100 scale: susceptibility 50 → +0.05, 100 → +0.10
    base += (susceptibility / 100.0) * 0.10
    return max(0.0, min(1.0, base))


def select_candidates(
    candidate_packet: dict[str, Any],
    state_summary: dict[str, Any],
    rng: random.Random | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    Score event and magnet candidates; select ≤2 major, ≤2 minor, ≤1 surprise.
    70% of major slots prefer events with striving_object_id when available (GAP Tier 3).
    Returns (selected_events, selected_magnets).
    """
    rng = rng or random.Random()
    events = list(candidate_packet.get("event_candidates") or [])
    magnets = list(candidate_packet.get("magnet_candidates") or [])

    scored_events: list[tuple[float, dict[str, Any]]] = []
    for ev in events:
        s = score_event_candidate(ev, state_summary)
        scored_events.append((s, ev))
    scored_events.sort(key=lambda x: -x[0])

    striving_ids = {s.get("id") for s in (state_summary.get("striving_objects") or []) if s.get("id")}
    target_attached_major = max(1, round(STRIVING_ATTACH_MAJOR_FRACTION * MAJOR_MAX)) if striving_ids else 0

    # Split by intensity
    major_pool: list[tuple[float, dict[str, Any]]] = []
    minor_pool: list[tuple[float, dict[str, Any]]] = []
    for s, ev in scored_events:
        intensity = (ev.get("intensity") or "minor").strip().lower()
        if intensity in ("major", "shock"):
            major_pool.append((s, ev))
        else:
            minor_pool.append((s, ev))

    attached_major = [(s, e) for s, e in major_pool if (e.get("striving_object_id") or "") in striving_ids]
    unattached_major = [(s, e) for s, e in major_pool if (e.get("striving_object_id") or "") not in striving_ids]
    attached_major.sort(key=lambda x: -x[0])
    unattached_major.sort(key=lambda x: -x[0])

    selected_events: list[dict[str, Any]] = []
    shock_count = 0
    attached_major_count = 0

    # Fill major slots: first up to target_attached_major from attached, then rest from unattached, then any remaining attached
    for _ in range(target_attached_major):
        if attached_major_count >= target_attached_major:
            break
        took = False
        for s, ev in attached_major:
            if ev in selected_events:
                continue
            if (ev.get("intensity") or "").strip().lower() == "shock" and shock_count >= SHOCK_MAX_PER_SELECTION:
                continue
            if len(selected_events) >= MAJOR_MAX:
                break
            selected_events.append(ev)
            shock_count += 1 if (ev.get("intensity") or "").strip().lower() == "shock" else 0
            attached_major_count += 1
            took = True
            break
        if not took:
            break
    for s, ev in unattached_major:
        if len(selected_events) >= MAJOR_MAX:
            break
        if ev in selected_events:
            continue
        if (ev.get("intensity") or "").strip().lower() == "shock" and shock_count >= SHOCK_MAX_PER_SELECTION:
            continue
        selected_events.append(ev)
        shock_count += 1 if (ev.get("intensity") or "").strip().lower() == "shock" else 0
    for s, ev in attached_major:
        if len(selected_events) >= MAJOR_MAX:
            break
        if ev in selected_events:
            continue
        if (ev.get("intensity") or "").strip().lower() == "shock" and shock_count >= SHOCK_MAX_PER_SELECTION:
            continue
        selected_events.append(ev)
        shock_count += 1 if (ev.get("intensity") or "").strip().lower() == "shock" else 0

    minor_count = 0
    surprise_candidates: list[tuple[float, dict[str, Any]]] = []
    for score, ev in minor_pool:
        if minor_count < MINOR_MAX:
            selected_events.append(ev)
            minor_count += 1
        else:
            surprise_candidates.append((score, ev))

    if surprise_candidates and rng.random() < SURPRISE_PROBABILITY and len(selected_events) < MAJOR_MAX + MINOR_MAX + SURPRISE_MAX:
        _, surprise_ev = rng.choice(surprise_candidates)
        selected_events.append(surprise_ev)

    # Magnets: take up to 2 by score
    scored_magnets: list[tuple[float, dict[str, Any]]] = []
    for mg in magnets:
        s = score_magnet_candidate(mg, state_summary)
        scored_magnets.append((s, mg))
    scored_magnets.sort(key=lambda x: -x[0])
    selected_magnets = [mg for _, mg in scored_magnets[:2]]

    return selected_events, selected_magnets
