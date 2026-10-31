# v3/systems/frameworks.py — update framework weights from events; apply delta cap.
# Also applies framework metabolic operators (acute_delta/chronic_delta) to capacity each year (spec §6).

from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState, clamp
from v3.core.derived import DerivedIndices

DEFAULT_DELTA_CAP = 15

# Capacity fields that live on state.psychological_capacity vs state.capacity (material)
_PSYCH_FIELDS = frozenset({
    "vitality", "aperture", "reality_anchor", "binding", "coherence", "agency", "transmutation",
})
_MATERIAL_FIELDS = frozenset({
    "health", "social_support", "skill", "money", "time", "mobility", "risk_tolerance", "legitimacy",
})

# Global damping: prevents any single framework from dominating capacity.
# raw_delta * weight_scale * OPERATOR_SCALE = effective annual pts; e.g. acute agency=5, weight=58 → 5*0.58*0.3 = 0.87/yr
_OPERATOR_SCALE = 0.3
# Hard cap per field per year regardless of weight/delta magnitude
_OPERATOR_CAP = 2.0


def _get_delta_cap(config: dict[str, Any]) -> float:
    caps = config.get("delta_caps") or {}
    return float(caps.get("frameworks_weights", DEFAULT_DELTA_CAP))


def update_framework_weights(
    state: BackboneState,
    derived: DerivedIndices,
    config: dict[str, Any],
) -> None:
    """
    Two jobs each year:
    1. Apply event-driven deltas to framework weights (existing behaviour).
    2. Apply framework metabolic operators (acute_delta before half_life, chronic_delta after)
       to state.psychological_capacity and state.capacity, scaled by weight and damped by
       _OPERATOR_SCALE. Increment tenure_years for every active framework.
    """
    cap = _get_delta_cap(config)
    pw = getattr(state, "plasticity_window", None) or {}
    sensitivity = int(pw.get("framework_switch_sensitivity", 10))
    cap = cap * (1.0 + (sensitivity - 10) / 100.0)
    cap = max(1.0, min(50.0, cap))
    frameworks = state.frameworks
    if not frameworks:
        return
    n = len(frameworks)

    # --- Job 1: event-driven weight deltas ---
    deltas = [0.0] * n
    for ev in state.events_this_year:
        if not isinstance(ev, dict):
            continue
        fd = ev.get("framework_deltas")
        if not isinstance(fd, list):
            continue
        for i, d in enumerate(fd):
            if i < n and isinstance(d, (int, float)):
                deltas[i] += float(d)
    for i, fw in enumerate(frameworks):
        delta = max(-cap, min(cap, deltas[i]))
        fw.weight = clamp(fw.weight + delta)
        fw.clamp_all()

    # --- Job 2: metabolic operator application + tenure increment ---
    pc = state.psychological_capacity
    mc = state.capacity
    for fw in frameworks:
        if fw.weight < 5.0:
            # Dormant frameworks don't apply operators
            fw.tenure_years += 1
            continue
        # Choose acute or chronic based on tenure vs half_life
        hl = fw.half_life_years
        if hl > 0 and fw.tenure_years >= hl:
            operator = fw.chronic_delta or {}
        else:
            operator = fw.acute_delta or {}
        scale = fw.weight / 100.0
        for field, raw_delta in operator.items():
            if not isinstance(raw_delta, (int, float)):
                continue
            effective = max(-_OPERATOR_CAP, min(_OPERATOR_CAP, float(raw_delta) * scale * _OPERATOR_SCALE))
            if effective == 0.0:
                continue
            if field in _PSYCH_FIELDS:
                cur = float(getattr(pc, field, 50.0) or 50.0)
                setattr(pc, field, max(0.0, min(100.0, cur + effective)))
            elif field in _MATERIAL_FIELDS:
                cur = float(getattr(mc, field, 50.0) or 50.0)
                setattr(mc, field, max(0.0, min(100.0, cur + effective)))
        fw.tenure_years += 1
    # Clamp after all mutations
    pc.clamp_all()
    mc.clamp_all()


def enforce_framework_caps(state):
    """Move weight < 5 to dormant. Cap dormant at 10."""
    active = state.frameworks
    dormant = getattr(state, 'frameworks_dormant', [])
    remaining = []
    for fw in active:
        if getattr(fw, 'weight', 0) < 5.0:
            entry = {'id': getattr(fw, 'id', ''), 'label': str(getattr(fw, 'id', fw)),
                     'reason_dormant': 'weight_below_5', 'last_active_year': state.year}
            dormant.append(entry)
        else:
            remaining.append(fw)
    state.frameworks = remaining
    if len(dormant) > 10:
        dormant = dormant[-10:]
    state.frameworks_dormant = dormant
