# v3/systems/stability_inertia.py — stability_threshold_inertia dissipation (maximal spec).
# Runs after plasticity_and_metabolization_update. Drains inertia from integration, IRR drop, and holding.

from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState
from v3.core.derived import DerivedIndices

CAP_INTEGRATION_DRAIN = 12.0
CAP_IRR_DROP_DRAIN = 3.0
HOLDING_SCALE = 0.6
SEALED_LEAK = 0.15


def stability_inertia_dissipation(
    state: BackboneState,
    derived: DerivedIndices,
    config: dict[str, Any],
) -> None:
    """
    Drain stability_threshold_inertia from: integration (provisionally_narrated/integrated),
    IRR drop (working-through), sustained holding. Clear stability_delta_applied_this_year at end.
    """
    inertia = getattr(state, "stability_threshold_inertia", 0.0)
    delta_applied = getattr(state, "stability_delta_applied_this_year", False)
    ns = getattr(state, "narration_support", None)
    warmth = getattr(ns, "warmth", 50) if ns else 50
    accuracy = getattr(ns, "accuracy", 50) if ns else 50
    coercion = getattr(ns, "coercion", 50) if ns else 50
    availability = getattr(ns, "availability", 50) if ns else 50
    support_quality = max(0, min(100, warmth + accuracy - coercion))

    insulation = getattr(derived, "insulation_score", 0.0)
    social_support = state.capacity.social_support
    coherence = getattr(state.peak_routing, "coherence", 50.0)

    drain_integration = 0.0
    for proc in getattr(state, "metabolization_processes", []) or []:
        if getattr(proc, "status", "") == "integrated":
            drain_integration += 5.0
        elif getattr(proc, "status", "") == "provisionally_narrated":
            drain_integration += 3.0
    drain_integration = min(drain_integration, CAP_INTEGRATION_DRAIN)

    drain_irr = 0.0
    for proc in getattr(state, "metabolization_processes", []) or []:
        if getattr(proc, "status", "") not in ("raw", "working"):
            continue
        prev = getattr(proc, "intrusive_return_rate_prev", proc.intrusive_return_rate)
        curr = getattr(proc, "intrusive_return_rate", 50)
        if curr < prev and (prev - curr) >= 5 and support_quality >= 55:
            drain_irr += 1.5
    drain_irr = min(drain_irr, CAP_IRR_DROP_DRAIN)

    drain_holding = 0.0
    raw_working_high_irr = any(
        getattr(p, "status", "") in ("raw", "working") and getattr(p, "intrusive_return_rate", 0) > 60
        for p in getattr(state, "metabolization_processes", []) or []
    )
    raw_working_mid_irr = any(
        getattr(p, "status", "") in ("raw", "working") and 40 <= getattr(p, "intrusive_return_rate", 0) <= 60
        for p in getattr(state, "metabolization_processes", []) or []
    )
    if not delta_applied and not raw_working_high_irr:
        drain_holding = HOLDING_SCALE * (
            (insulation / 100.0) * 0.35
            + (social_support / 100.0) * 0.35
            + (coherence / 100.0) * 0.30
        )
        if raw_working_mid_irr:
            drain_holding *= 0.5

    drain_sealed = 0.0
    procs = getattr(state, "metabolization_processes", []) or []
    if procs and all(getattr(p, "status", "") in ("sealed", "chronic") for p in procs) and support_quality >= 60:
        drain_sealed = SEALED_LEAK

    total_drain = drain_integration + drain_irr + drain_holding + drain_sealed
    state.stability_threshold_inertia = max(0.0, min(100.0, inertia - total_drain))
    state.stability_delta_applied_this_year = False
    state.clamp_all()
