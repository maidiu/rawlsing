# v3/psyche/wound.py — wound vector + coping directionality (spec § psyche/).

from __future__ import annotations

from v3.core.state import BackboneState, WoundVector

WOUND_SENSITIVITY_KEYS = ("shame", "fear", "anger", "abandonment", "control", "recognition", "loss")


def wound_vector(state: BackboneState) -> WoundVector:
    """Canonical access to wound vector (sensitivities + default_coping_channels)."""
    return state.wound_vector


def sensitivities_dict(state: BackboneState) -> dict[str, float]:
    """Sensitivities per hook for scoring/summary."""
    return state.wound_vector.to_sensitivities_dict()
