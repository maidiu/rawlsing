# v3/systems/autonomy_safety.py — micro-drift/micro-repair of autonomy_condition/safety_condition; trace to events (revision 2026.02.25).

from __future__ import annotations

import random
from typing import Any

from v3.core.state import BackboneState, clamp
from v3.core.derived import DerivedIndices

DRIFT_DELTA_RANGE = (-2.0, 0.0)
REPAIR_DELTA_RANGE = (0.0, 2.0)


def _autonomy_gap(state: BackboneState) -> float:
    return max(0.0, state.autonomy_drive - state.autonomy_condition)


def _safety_gap(state: BackboneState) -> float:
    return max(0.0, state.safety_drive - state.safety_condition)


def _gap_pressure(autonomy_gap: float, safety_gap: float) -> float:
    return 0.5 * autonomy_gap + 0.5 * safety_gap


def autonomy_safety_micro_drift(
    state: BackboneState,
    derived: DerivedIndices,
    config: dict[str, Any],
) -> None:
    """
    Small yearly drift/repair on autonomy_condition and safety_condition.
    Drift (down) when gap_pressure and stability high; repair (up) when insulation/support/alignment positive.
    Appends trace entries to state.micro_trace_this_year: kind micro_drift | micro_repair, axis, delta, cue, shaping.
    """
    ag = _autonomy_gap(state)
    sg = _safety_gap(state)
    gap_pressure = _gap_pressure(ag, sg)
    stability = getattr(derived, "stability_threshold", 0.0)
    insulation = getattr(derived, "insulation_score", 0.0)
    alignment = getattr(derived, "alignment_vector", 0.0)
    support = state.capacity.social_support

    # Drift bias: higher gap_pressure + stability -> more downward pressure on conditions
    drift_bias = (gap_pressure / 100.0) * 0.5 + (stability / 100.0) * 0.3
    # Repair bias: insulation, support, positive alignment
    repair_bias = (insulation / 100.0) * 0.3 + (support / 100.0) * 0.2 + (max(0, alignment) / 100.0) * 0.2

    rng = random.Random(config.get("seed") or state.year)
    delta_autonomy = 0.0
    delta_safety = 0.0
    cues: list[str] = []
    shapings: list[str] = []

    # Hit larger gap more
    if ag >= sg and ag > 5:
        d = rng.uniform(DRIFT_DELTA_RANGE[0], DRIFT_DELTA_RANGE[1]) * (0.5 + 0.5 * drift_bias)
        r = rng.uniform(REPAIR_DELTA_RANGE[0], REPAIR_DELTA_RANGE[1]) * repair_bias
        delta_autonomy = d + r
        delta_autonomy = max(-2.0, min(2.0, delta_autonomy))
        state.autonomy_condition = clamp(state.autonomy_condition + delta_autonomy)
        cues.append("autonomy")
        shapings.append("slightly less latitude" if delta_autonomy < 0 else "slightly more latitude")
    if sg > ag and sg > 5:
        d = rng.uniform(DRIFT_DELTA_RANGE[0], DRIFT_DELTA_RANGE[1]) * (0.5 + 0.5 * drift_bias)
        r = rng.uniform(REPAIR_DELTA_RANGE[0], REPAIR_DELTA_RANGE[1]) * repair_bias
        delta_safety = d + r
        delta_safety = max(-2.0, min(2.0, delta_safety))
        state.safety_condition = clamp(state.safety_condition + delta_safety)
        cues.append("safety")
        shapings.append("slightly less stability" if delta_safety < 0 else "slightly more stability")

    if not cues:
        return

    kind = "micro_repair" if (delta_autonomy + delta_safety) > 0 else "micro_drift"
    axis = "both" if len(cues) == 2 else (cues[0] if cues else "autonomy")
    cue_str = " and ".join(cues)
    shaping_str = " and ".join(shapings)
    trace = {
        "id": f"micro_{state.year}_{len(getattr(state, 'micro_trace_this_year', []) or [])}",
        "label": f"{kind.replace('_', ' ')} on {axis}",
        "source": "autonomy_safety_micro_drift",
        "conditioning_inputs": {
            "autonomy_gap": ag,
            "safety_gap": sg,
            "gap_pressure": gap_pressure,
            "stability_threshold": stability,
            "insulation_score": insulation,
            "alignment_vector": alignment,
            "social_support": support,
        },
        "kind": kind,
        "axis": axis,
        "delta": {"autonomy_condition": delta_autonomy, "safety_condition": delta_safety},
        "cue": cue_str,
        "shaping": shaping_str,
    }
    micro_trace = getattr(state, "micro_trace_this_year", None)
    if micro_trace is None:
        state.micro_trace_this_year = []
        micro_trace = state.micro_trace_this_year
    if isinstance(micro_trace, list):
        micro_trace.append(trace)
    yearly = getattr(state, "yearly_integrity", None)
    if isinstance(yearly, dict):
        traces = yearly.setdefault("micro_traces", [])
        if isinstance(traces, list):
            traces.append(trace)
