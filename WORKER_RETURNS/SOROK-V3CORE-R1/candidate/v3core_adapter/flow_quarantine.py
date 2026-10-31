"""Quarantined access to the historical conserved-charge pressure-flow model."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any

from v3.core.invariants import backbone_hash
from v3.core.state import BackboneState

from .contracts import Status


@dataclass(frozen=True)
class FlowProbe:
    """Result of the optional pressure-flow probe."""

    status: Status
    live_state_mutated: bool
    backbone_hash_before: str
    backbone_hash_after: str
    snapshot: dict[str, Any] = field(default_factory=dict)
    reason: str = ""


def run_conserved_charge_flow_probe(
    state: BackboneState,
    *,
    explicitly_enabled: bool = False,
) -> FlowProbe:
    """Run the actual V3 flow only on a copy and only with explicit opt-in.

    The V3 pressure-flow model treats routed charge as conserved. That is a
    test-only model, not a universal law of needs, wounds or meaning. The live
    state is never mutated by this probe.
    """
    before = backbone_hash(state)
    if not explicitly_enabled:
        return FlowProbe(
            status=Status.HELD_CONSERVED_CHARGE_MODEL,
            live_state_mutated=False,
            backbone_hash_before=before,
            backbone_hash_after=before,
            reason="conserved_charge_model_not_issued",
        )
    from v3.psyche.flow import run_pressure_flow_cycle

    working = deepcopy(state)
    snapshot = run_pressure_flow_cycle(working)
    return FlowProbe(
        status=Status.APPLIED_TEST_ONLY_SOURCEFREE,
        live_state_mutated=backbone_hash(state) != before,
        backbone_hash_before=before,
        backbone_hash_after=backbone_hash(state),
        snapshot=snapshot,
        reason="test_only_conserved_charge_model_not_science",
    )
