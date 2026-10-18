# v3/systems/buffers.py — update buffer strengths from events; pay buffer costs into capacity; apply delta caps.

from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState, clamp
from v3.core.derived import DerivedIndices

DEFAULT_BUFFER_STRENGTH_CAP = 20
DEFAULT_CAPACITY_FIELDS_CAP = 20


def _get_buffer_strength_cap(config: dict) -> float:
    caps = config.get("delta_caps") or {}
    return float(caps.get("buffer_strength", DEFAULT_BUFFER_STRENGTH_CAP))


def _get_capacity_cap(config: dict) -> float:
    caps = config.get("delta_caps") or {}
    return float(caps.get("capacity_fields", DEFAULT_CAPACITY_FIELDS_CAP))


def _apply_strength_deltas(state: BackboneState, config: dict) -> None:
    """Apply event-driven deltas to buffer strengths (by index). Cap per-buffer change."""
    cap = _get_buffer_strength_cap(config)
    buffers = state.buffers
    if not buffers:
        return
    for ev in state.events_this_year:
        if not isinstance(ev, dict):
            continue
        deltas = ev.get("buffer_strength_deltas")
        if not isinstance(deltas, list):
            continue
        for i, d in enumerate(deltas):
            if i >= len(buffers) or not isinstance(d, (int, float)):
                continue
            delta = max(-cap, min(cap, float(d)))
            buffers[i].strength = clamp(buffers[i].strength + delta)
    for b in buffers:
        b.clamp_all()


def _pay_buffer_costs(state: BackboneState, config: dict) -> None:
    """Reduce capacity by buffer costs (strength * cost_profile / 100). Cap total reduction per field."""
    cap = _get_capacity_cap(config)
    c = state.capacity
    # Map cost_profile keys to capacity fields.
    time_ded = 0.0
    money_ded = 0.0
    social_ded = 0.0
    legit_ded = 0.0
    for b in state.buffers:
        p = b.cost_profile
        s = b.strength / 100.0
        time_ded += s * p.time_cost
        money_ded += s * p.money_cost
        social_ded += s * p.relational_cost
        legit_ded += s * p.truth_cost
    # Cap total deduction per field so annual change is bounded.
    time_ded = min(time_ded, cap)
    money_ded = min(money_ded, cap)
    social_ded = min(social_ded, cap)
    legit_ded = min(legit_ded, cap)
    c.time = clamp(c.time - time_ded)
    c.money = clamp(c.money - money_ded)
    c.social_support = clamp(c.social_support - social_ded)
    c.legitimacy = clamp(c.legitimacy - legit_ded)
    c.clamp_all()


def update_buffers(
    state: BackboneState,
    derived: DerivedIndices,
    config: dict[str, Any],
) -> None:
    """Update buffer strengths from events; pay buffer costs into capacity. Insulation (derived) recomputed after this step."""
    _apply_strength_deltas(state, config)
    _pay_buffer_costs(state, config)
