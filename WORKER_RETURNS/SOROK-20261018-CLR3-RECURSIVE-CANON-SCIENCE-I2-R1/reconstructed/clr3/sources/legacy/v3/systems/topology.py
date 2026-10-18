# v3/systems/topology.py — update loop_topology with full hysteresis (consecutive years, transition rules from v3config).

from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState
from v3.core.derived import DerivedIndices

VALID_TOPOLOGIES = frozenset({"reciprocal", "extractive", "self_contained"})
HYSTERESIS_KEYS = ("to_reciprocal", "to_extractive", "to_self_contained")


def _eval_requires(state: BackboneState, derived: DerivedIndices, requires: dict[str, Any]) -> bool:
    """True if all requirement keys are satisfied (min/max/in/not)."""
    if not requires:
        return True
    inf = state.collective_infrastructure
    cap = state.capacity
    pr = state.peak_routing
    ps = state.practice_stack
    for k, v in requires.items():
        if k == "network_density_min" and inf.network_density < float(v):
            return False
        if k == "organizing_min" and ps.organizing < float(v):
            return False
        if k == "solidarity_boundary_not":
            if pr.solidarity_boundary in (v if isinstance(v, list) else [v]):
                return False
        if k == "solidarity_boundary_in":
            if pr.solidarity_boundary not in (v if isinstance(v, list) else [v]):
                return False
        if k == "money_min" and cap.money < float(v):
            return False
        if k == "social_support_min" and cap.social_support < float(v):
            return False
        if k == "mis_aim_risk_min" and derived.mis_aim_risk < float(v):
            return False
        if k == "impunity_access_min" and pr.impunity_access < float(v):
            return False
        if k == "craft_or_study_min" and max(ps.craft, ps.study) < float(v):
            return False
        if k == "network_density_max" and inf.network_density > float(v):
            return False
        if k == "hostage_index_min" and derived.hostage_index < float(v):
            return False
    return True


def update_loop_topology(
    state: BackboneState,
    derived: DerivedIndices,
    config: dict[str, Any],
) -> None:
    """Apply hysteresis: transition only after required_consecutive_years of meeting transition requirements."""
    hyst = (config.get("hysteresis") or {}).get("loop_topology")
    if not isinstance(hyst, dict):
        return

    required_years = int(hyst.get("required_consecutive_years", 2))
    transitions = hyst.get("transitions")
    if not isinstance(transitions, dict):
        return

    pr = state.peak_routing
    counters = pr.topology_hysteresis_years
    if not isinstance(counters, dict):
        counters = {}
    pr.topology_hysteresis_years = dict(counters)

    current = pr.loop_topology if pr.loop_topology in VALID_TOPOLOGIES else "self_contained"

    for key in HYSTERESIS_KEYS:
        target = key.replace("to_", "")
        if target not in VALID_TOPOLOGIES:
            continue
        rule = transitions.get(key)
        if not isinstance(rule, dict):
            pr.topology_hysteresis_years[key] = 0
            continue

        requires = rule.get("requires")
        or_if = rule.get("or_if")
        satisfied = _eval_requires(state, derived, requires or {})
        if or_if and isinstance(or_if, dict):
            satisfied = satisfied or _eval_requires(state, derived, or_if)

        if current == target:
            pr.topology_hysteresis_years[key] = 0
            continue
        if satisfied:
            n = pr.topology_hysteresis_years.get(key, 0) + 1
            pr.topology_hysteresis_years[key] = n
            if n >= required_years:
                pr.loop_topology = target
                pr.topology_hysteresis_years = {k: 0 for k in HYSTERESIS_KEYS}
                return
        else:
            pr.topology_hysteresis_years[key] = 0
