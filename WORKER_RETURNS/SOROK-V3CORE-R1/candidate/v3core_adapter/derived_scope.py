"""Scoped derived computation over the historical V3 formulas.

The original ``compute_all_derived`` is executed on a working copy for
diagnostic provenance. Only derived values whose complete input set is
source-grounded may be published. Every other index is HELD, not silently
computed from absent defaults.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any

from v3.core.derived import compute_all_derived, derived_to_dict
from v3.core.state import BackboneState

from .contracts import Status
from .provenance import digest, record_to_dict

MATERIAL_CAPACITY_WEIGHTS = {
    "time": 0.20,
    "money": 0.15,
    "health": 0.15,
    "social_support": 0.15,
    "skill": 0.10,
    "mobility": 0.10,
    "risk_tolerance": 0.10,
    "legitimacy": 0.05,
}

DERIVED_DEPENDENCIES = {
    "hostage_index": ("reproduction_constraints",),
    "agency_capacity_AC": ("capacity", "reproduction_constraints"),
    "insulation_score": ("buffers", "capacity.money"),
    "structural_lucidity_SL": ("domains",),
    "mis_aim_risk": ("alienation", "reproduction_constraints", "practice_stack.organizing"),
    "peak_regime": ("domains", "capacity", "reproduction_constraints", "peak_routing.coherence"),
    "che_jesus_eligible": ("domains", "capacity", "reproduction_constraints", "peak_routing"),
    "metabolic_style_current": ("reproduction_constraints", "buffers", "capacity.money", "wound_vector"),
    "metabolic_style_trend": ("reproduction_constraints", "buffers", "capacity.money", "wound_vector"),
    "autonomy_gap": ("autonomy_drive", "autonomy_condition"),
    "safety_gap": ("safety_drive", "safety_condition"),
    "gap_pressure_index": ("autonomy_drive", "autonomy_condition", "safety_drive", "safety_condition"),
    "alignment_vector": ("autonomy_drive", "autonomy_condition", "safety_drive", "safety_condition", "reproduction_constraints", "alienation", "practice_stack.organizing"),
    "stability_threshold": ("gap_pressure_index", "reproduction_constraints", "alienation", "buffers"),
    "health_level": ("capacity", "stability_threshold", "buffers"),
}


@dataclass(frozen=True)
class PublishedDerived:
    """The only derived values the adapter publishes, plus per-index holds."""

    schema: str
    material_capacity_index: float
    material_capacity_fields: dict[str, float]
    material_weights: dict[str, float]
    index_status: dict[str, str]
    held_reasons: dict[str, str]
    diagnostic_only: bool = True
    authority: str = "TEST_ONLY_MATERIAL_SCOPE_NOT_A_PERSON_CLAIM"

    def as_dict(self) -> dict[str, Any]:
        return record_to_dict(self)


@dataclass(frozen=True)
class DerivationOutcome:
    """Result of one scoped derivation."""

    status: Status
    published: PublishedDerived | None
    diagnostic: dict[str, Any]
    diagnostic_hash: str
    live_state_mutated: bool
    live_before: dict[str, Any] = field(default_factory=dict)
    live_after: dict[str, Any] = field(default_factory=dict)
    reason: str = ""


def material_capacity_index(state: BackboneState) -> float:
    """Capacity-only component of the original AC formula, without a hostage penalty."""
    total = 0.0
    for name, weight in MATERIAL_CAPACITY_WEIGHTS.items():
        total += weight * float(getattr(state.capacity, name, 0.0))
    return round(max(0.0, min(100.0, total)), 6)


def material_capacity_fields(state: BackboneState) -> dict[str, float]:
    return {name: float(getattr(state.capacity, name, 0.0)) for name in MATERIAL_CAPACITY_WEIGHTS}


def _live_snapshot(state: BackboneState) -> dict[str, Any]:
    return {
        "metabolic_style": deepcopy(getattr(state, "metabolic_style", {})),
        "registers": record_to_dict(getattr(state, "registers")),
    }


def _field_statuses(state: BackboneState) -> tuple[dict[str, str], dict[str, str]]:
    provenance = (state.initial_state_provenance or {}).get("field_status") or {}
    statuses: dict[str, str] = {}
    reasons: dict[str, str] = {}
    for index, dependencies in DERIVED_DEPENDENCIES.items():
        missing = [
            dep for dep in dependencies
            if str(provenance.get(dep, "ABSENT_NOT_ASSUMED")) != "SOURCE_GROUNDED"
            and not (dep.endswith(".money") and str(provenance.get("capacity.money")) == "SOURCE_GROUNDED")
        ]
        if missing:
            statuses[index] = Status.HELD_MISSING_ISSUED_RULE.value
            reasons[index] = "missing_source_grounding:" + ",".join(missing)
        else:
            statuses[index] = "EVALUATED_SOURCE_GROUNDED"
    return statuses, reasons


def derive_scoped(state: BackboneState) -> DerivationOutcome:
    """Execute the actual V3 derived computation on a copy and scope publication."""
    live_before = _live_snapshot(state)
    working = deepcopy(state)
    try:
        diagnostic_indices = compute_all_derived(working)
    except Exception as exc:
        return DerivationOutcome(
            status=Status.HELD_TRANSACTION_ABORTED,
            published=None,
            diagnostic={},
            diagnostic_hash="",
            live_state_mutated=False,
            live_before=live_before,
            live_after=_live_snapshot(state),
            reason=f"{type(exc).__name__}:{exc}",
        )
    live_after = _live_snapshot(state)
    mutated = live_before != live_after
    diagnostic = derived_to_dict(diagnostic_indices)
    diagnostic.update(
        {
            "autonomy_gap": diagnostic_indices.autonomy_gap,
            "safety_gap": diagnostic_indices.safety_gap,
            "gap_pressure_index": diagnostic_indices.gap_pressure_index,
            "alignment_vector": diagnostic_indices.alignment_vector,
            "stability_threshold": diagnostic_indices.stability_threshold,
            "health_level": diagnostic_indices.health_level,
        }
    )
    statuses, reasons = _field_statuses(state)
    published = PublishedDerived(
        schema="SOROK_V3CORE_R1_PUBLISHED_DERIVED@1",
        material_capacity_index=material_capacity_index(state),
        material_capacity_fields=material_capacity_fields(state),
        material_weights=dict(MATERIAL_CAPACITY_WEIGHTS),
        index_status=statuses,
        held_reasons=reasons,
    )
    return DerivationOutcome(
        status=Status.HELD_DERIVED_MUTATION if mutated else Status.DERIVED_EVALUATED_SCOPED,
        published=None if mutated else published,
        diagnostic=diagnostic,
        diagnostic_hash=digest(diagnostic),
        live_state_mutated=mutated,
        live_before=live_before,
        live_after=live_after,
        reason="derived_computation_mutated_live_state" if mutated else "",
    )
