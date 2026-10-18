# v3/psyche/metabolism.py — metabolic style + capacity vector update rules (spec § psyche/).

from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState
from v3.core.derived import (
    compute_hostage_index,
    compute_insulation_score,
    compute_metabolic_style,
)


def metabolic_style_from_state(state: BackboneState) -> dict[str, str]:
    """Return state.metabolic_style if set; else compute (current, trend)."""
    if state.metabolic_style and isinstance(state.metabolic_style, dict):
        return dict(state.metabolic_style)
    hostage_index = compute_hostage_index(state)
    insulation_score = compute_insulation_score(state)
    current, trend = compute_metabolic_style(state, hostage_index, insulation_score)
    return {"current": current, "trend": trend}


def update_metabolic_style(state: BackboneState) -> None:
    """Write metabolic_style to state (current, trend). Called from derived step."""
    hostage_index = compute_hostage_index(state)
    insulation_score = compute_insulation_score(state)
    current, trend = compute_metabolic_style(state, hostage_index, insulation_score)
    state.metabolic_style = {"current": current, "trend": trend}
