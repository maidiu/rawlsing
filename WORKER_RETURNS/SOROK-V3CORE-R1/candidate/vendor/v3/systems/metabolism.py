# v3/systems/metabolism.py — metabolic_style derivation and state update (spec §7).

from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState
from v3.core.derived import DerivedIndices, compute_metabolic_style


def update_metabolic_style(
    state: BackboneState,
    derived: DerivedIndices,
    config: dict[str, Any],
) -> None:
    """
    Derive metabolic_style from capacity + hostage + contradiction + buffers;
    set state.metabolic_style.current and state.metabolic_style.trend.
    """
    current, trend = compute_metabolic_style(
        state,
        derived.hostage_index,
        derived.insulation_score,
    )
    state.metabolic_style.clear()
    state.metabolic_style["current"] = current
    state.metabolic_style["trend"] = trend
