# v3/psyche/registers.py — public/private/inner expression gates (spec § psyche/).

from __future__ import annotations

from v3.core.state import BackboneState, Registers


def registers(state: BackboneState) -> Registers:
    """Canonical access to expression gates (public_expression_gate, private_expression_gate, inner_load)."""
    return state.registers


def clamp_registers(state: BackboneState) -> None:
    """Clamp register fields 0–100. Normally done via state.clamp_all()."""
    state.registers.clamp_all()
