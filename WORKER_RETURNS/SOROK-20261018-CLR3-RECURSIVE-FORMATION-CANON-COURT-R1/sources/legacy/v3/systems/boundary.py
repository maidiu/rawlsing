# v3/systems/boundary.py — update solidarity_boundary with hysteresis (order, max_step_per_year, reversal_requires_any).

from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState
from v3.core.derived import DerivedIndices

DEFAULT_ORDER = ("none", "transactional", "in_group", "expanding", "universal")


def _boundary_index(b: str, order: tuple[str, ...]) -> int:
    for i, v in enumerate(order):
        if v == b:
            return i
    return 2


def _reversal_allowed(state: BackboneState, derived: DerivedIndices, config: dict[str, Any]) -> bool:
    """True if any of reversal_requires_any is satisfied (or shock in events)."""
    rules = (config.get("hysteresis") or {}).get("solidarity_boundary")
    if not isinstance(rules, dict):
        return False
    reversal = rules.get("reversal_requires_any")
    if not isinstance(reversal, list):
        return False
    for r in reversal:
        if not isinstance(r, dict):
            continue
        if r.get("shock_override") is True:
            for ev in state.events_this_year:
                if isinstance(ev, dict) and ev.get("shock_override") is True:
                    return True
            continue
        if r.get("repression_pressure_min") is not None and state.collective_infrastructure.repression_pressure >= float(r["repression_pressure_min"]):
            return True
        if r.get("hostage_index_min") is not None and derived.hostage_index >= float(r["hostage_index_min"]):
            return True
    return False


def update_solidarity_boundary(
    state: BackboneState,
    derived: DerivedIndices,
    config: dict[str, Any],
) -> None:
    """Move at most max_step_per_year steps along order; reversal only if reversal_requires_any satisfied."""
    hyst = (config.get("hysteresis") or {}).get("solidarity_boundary")
    if not isinstance(hyst, dict):
        return

    order_list = hyst.get("order")
    if not isinstance(order_list, list) or len(order_list) < 2:
        order = DEFAULT_ORDER
    else:
        order = tuple(str(x) for x in order_list)
    max_step = int(hyst.get("max_step_per_year", 1))
    max_step = max(0, min(4, max_step))

    current_idx = _boundary_index(state.peak_routing.solidarity_boundary, order)
    target_idx = current_idx

    # Event-requested target (last event wins)
    for ev in reversed(state.events_this_year):
        if not isinstance(ev, dict):
            continue
        v = ev.get("solidarity_boundary")
        if isinstance(v, str) and v in order:
            target_idx = _boundary_index(v, order)
            break

    if target_idx == current_idx:
        return
    step = 1 if target_idx > current_idx else -1
    if step < 0 and not _reversal_allowed(state, derived, config):
        return  # reversal not allowed this year
    new_idx = current_idx + step * min(max_step, abs(target_idx - current_idx))
    new_idx = max(0, min(len(order) - 1, new_idx))
    state.peak_routing.solidarity_boundary = order[new_idx]
