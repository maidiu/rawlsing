"""Explicit quarantine of illegitimate psychological defaults and synthetic life.

The adapter can use the historical computational skeleton, but it cannot use
identity-seeded wounds, missing-parent midpoint defaults, hopeful parent
baselines, Enneagram/type determinism, synthetic fallback practices,
placeholder cracks/frameworks or random age-band rupture.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, fields, is_dataclass
from pathlib import Path
from typing import Any

from v3.core.enums import DOMAIN_NAMES
from v3.core.state import BackboneState, DomainState

from .contracts import SourceActorSnapshot
from .provenance import record_to_dict

VENDOR = Path(__file__).resolve().parent.parent / "vendor"


class ForbiddenDefaultError(RuntimeError):
    """Raised when a state contains a default the adapter refuses to carry."""

    def __init__(self, reasons: list[str]) -> None:
        super().__init__("; ".join(reasons))
        self.reasons = tuple(reasons)


@dataclass(frozen=True)
class QuarantineEntry:
    """One excluded historical mechanism and its exact source evidence."""

    mechanism: str
    source_path: str
    symbol: str
    rationale: str
    active_path: str = "EXCLUDED_FROM_ADAPTER"
    test: str = "tests/test_quarantine_and_defaults.py"

    def source_sha256(self) -> str:
        path = VENDOR / self.source_path
        if not path.exists():
            return ""
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def as_dict(self) -> dict[str, str]:
        return {
            "mechanism": self.mechanism,
            "source_path": self.source_path,
            "symbol": self.symbol,
            "rationale": self.rationale,
            "active_path": self.active_path,
            "test": self.test,
            "source_sha256": self.source_sha256(),
        }


QUARANTINE: tuple[QuarantineEntry, ...] = (
    QuarantineEntry(
        mechanism="M08_IDENTITY_SEEDED_WOUND",
        source_path="v3/psyche/channels.py",
        symbol="seed_wound_vector_from_identity",
        rationale=(
            "Class, minority status, religiosity and age cannot manufacture wound "
            "sensitivity. Wound history requires warranted situations and responses."
        ),
    ),
    QuarantineEntry(
        mechanism="M15_M36_MISSING_PARENT_MIDPOINT_AND_HOPEFUL_DEFAULTS",
        source_path="v3/io/parent_baseline_from_behavior.py",
        symbol="parent_baseline_from_behavior",
        rationale=(
            "Absent parent axes must remain unknown. 50/50/50 and hopeful labels "
            "convert missing care into a fabricated developmental baseline."
        ),
    ),
    QuarantineEntry(
        mechanism="M15_M36_HOPEFUL_EXPECTATION_DEFAULT",
        source_path="v3/engine/expectation_baseline.py",
        symbol="DEFAULT_HOPEFUL_BASELINE",
        rationale=(
            "An unobserved need axis cannot be seeded as hopeful. The adapter "
            "keeps expectation_baseline empty and records a held state."
        ),
    ),
    QuarantineEntry(
        mechanism="M31_ENNEAGRAM_TYPE_DETERMINISM",
        source_path="v2/parent_type_inference.py",
        symbol="infer_parent_type_most_likely",
        rationale=(
            "Type inference is not an issued developmental rule and cannot "
            "determine the person. The adapter refuses type keys in source state."
        ),
    ),
    QuarantineEntry(
        mechanism="M34_SYNTHETIC_FALLBACK_PRACTICE",
        source_path="v3/engine/llm_contract.py",
        symbol="fallback practice/relationship event",
        rationale=(
            "An empty candidate packet is not a lived year. No fallback event or "
            "first-candidate practice may be manufactured."
        ),
    ),
    QuarantineEntry(
        mechanism="M34_SCORING_BYPASS_FALLBACK",
        source_path="v3/engine/run_llm_band.py",
        symbol="first-candidate fallback",
        rationale=(
            "Selecting the first candidate when scoring selects nothing fabricates "
            "an occurrence. The adapter accepts only actual source event records."
        ),
    ),
    QuarantineEntry(
        mechanism="M35_PLACEHOLDER_CRACKS_AND_FRAMEWORKS",
        source_path="v3/core/invariants.py",
        symbol="ensure_min_cracks / ensure_min_frameworks",
        rationale=(
            "Placeholder cracks and frameworks are not lived content. Degraded "
            "diagnosis is preserved; placeholder repair is never executed."
        ),
    ),
    QuarantineEntry(
        mechanism="M39_RANDOM_AGE_BAND_RUPTURE",
        source_path="v3/engine/effects/metabolization_effects.py",
        symbol="random.random / random.choices rupture injection",
        rationale=(
            "Rupture requires an admitted event ledger. A module-global random "
            "age-band ritual cannot create a developmental occurrence."
        ),
    ),
)


def quarantine_manifest() -> list[dict[str, str]]:
    """Return the quarantine table with current source hashes."""
    return [entry.as_dict() for entry in QUARANTINE]


def _zero(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, bool):
        return False
    if isinstance(value, float):
        return 0.0
    if isinstance(value, int):
        return 0
    if isinstance(value, str):
        return ""
    if isinstance(value, list):
        return []
    if isinstance(value, dict):
        return {}
    if is_dataclass(value):
        zero_dataclass(value)
        return value
    return value


def zero_dataclass(value: Any) -> None:
    """Set every defaulted field to an explicit empty value."""
    for item in fields(value):
        current = getattr(value, item.name)
        setattr(value, item.name, _zero(current))


def _zero_domain() -> DomainState:
    domain = DomainState()
    zero_dataclass(domain)
    return domain


def build_projection_state(
    *,
    annual_year: int,
    age: int | None,
    snapshot: SourceActorSnapshot,
) -> BackboneState:
    """Create a BackboneState with all ungrounded defaults explicitly emptied."""
    state = BackboneState()
    zero_dataclass(state)
    state.year = int(annual_year)
    state.age = 0 if age is None else int(age)
    state.domains = {name: _zero_domain() for name in DOMAIN_NAMES}
    state.capacity.time = float(snapshot.free_hours)
    state.capacity.money = float(snapshot.cash)
    state.capacity.skill = float(snapshot.skill)
    state.reproduction_constraints.legal_status = 0.0
    state.v5_bridge_status = "not_attached"
    state.initial_state_provenance = {
        "schema": "SOROK_V3CORE_R1_INITIAL_PROVENANCE@1",
        "source_snapshot": record_to_dict(snapshot),
        "field_status": {
            "capacity.time": "SOURCE_GROUNDED",
            "capacity.money": "SOURCE_GROUNDED",
            "capacity.skill": "SOURCE_GROUNDED",
            "capacity.health": "ABSENT_NOT_ASSUMED",
            "capacity.social_support": "ABSENT_NOT_ASSUMED",
            "capacity.mobility": "ABSENT_NOT_ASSUMED",
            "capacity.risk_tolerance": "ABSENT_NOT_ASSUMED",
            "capacity.legitimacy": "ABSENT_NOT_ASSUMED",
            "reproduction_constraints": "ABSENT_NOT_ASSUMED",
            "wound_vector": "QUARANTINED_UNSET",
            "psychological_capacity": "QUARANTINED_UNSET",
            "domains": "QUARANTINED_UNSET",
            "expectation_baseline": "QUARANTINED_UNSET",
            "cracks": "QUARANTINED_UNSET",
            "frameworks": "QUARANTINED_UNSET",
            "striving_objects": "QUARANTINED_UNSET",
            "metabolization_processes": "QUARANTINED_UNSET",
            "rupture_shards": "QUARANTINED_UNSET",
            "style_traits": "QUARANTINED_UNSET",
        },
        "forbidden_defaults_quarantined": [entry.mechanism for entry in QUARANTINE],
        "authority": "TEST_ONLY_SOURCEFREE",
        "native": False,
    }
    state.yearly_integrity = {
        "quarantine_status": "CLEAN_NO_FORBIDDEN_DEFAULT",
        "source_clock_domain": snapshot.source_clock_domain.value,
        "source_clock": snapshot.source_clock,
    }
    return state


def restore_unset_after_codec(state: BackboneState) -> None:
    """Undo codec midpoint coercions that would reintroduce a default.

    ``v3.io.json_codec.state_from_dict`` maps ``legal_status=0`` to ``100``.
    The projection uses 0 as "not source-grounded"; restore that sentinel.
    """
    state.reproduction_constraints.legal_status = 0.0


def forbidden_default_reasons(state: BackboneState) -> list[str]:
    """Return every forbidden default currently present in ``state``."""
    reasons: list[str] = []
    wound = state.wound_vector
    if any(getattr(wound, key) != 0 for key in ("shame", "fear", "anger", "abandonment", "control", "recognition", "loss")):
        reasons.append("wound_vector_nonzero_identity_or_default")
    if wound.default_coping_channels:
        reasons.append("wound_vector_default_coping_channels")
    psych = state.psychological_capacity
    if any(getattr(psych, key) != 0 for key in ("vitality", "aperture", "reality_anchor", "binding", "coherence", "agency", "transmutation")):
        reasons.append("psychological_capacity_default_or_inferred")
    for name, domain in state.domains.items():
        if any(getattr(domain, key) != 0 for key in ("A", "S", "V", "Aim", "latent_aim", "expressed_aim", "baseline_load", "expression_rate", "activation_threshold")):
            reasons.append(f"domain_unissued_value:{name}")
        if domain.affect_channel:
            reasons.append(f"domain_default_affect_channel:{name}")
        if domain.buffer_type:
            reasons.append(f"domain_default_buffer_type:{name}")
    if any(getattr(state.alienation_vector, key) != 0 for key in ("distant_others", "near_others", "self", "moral_totality")):
        reasons.append("alienation_default_or_inferred")
    if state.alienation != 0:
        reasons.append("alienation_scalar_default_or_inferred")
    if state.expectation_baseline:
        reasons.append("expectation_baseline_present")
    if state.cracks:
        reasons.append("cracks_present")
    if state.buffers:
        reasons.append("buffers_present")
    if state.frameworks:
        reasons.append("frameworks_present")
    if state.striving_objects:
        reasons.append("striving_objects_present")
    if state.metabolization_processes:
        reasons.append("metabolization_processes_present")
    if state.rupture_shards:
        reasons.append("rupture_shards_present")
    if state.gift_shards or state.disruption_shards:
        reasons.append("gift_or_disruption_shards_present")
    if state.active_magnets:
        reasons.append("active_magnets_present")
    if state.style_traits and any(
        getattr(state.style_traits, key) != 0
        for key in ("playfulness", "novelty_seeking", "conscientiousness", "social_energy", "absurdist_humor", "aesthetic_sensitivity", "impulsivity")
    ):
        reasons.append("style_traits_default_or_inferred")
    if state.registers and any(
        getattr(state.registers, key) != 0
        for key in ("public_expression_gate", "private_expression_gate", "inner_load")
    ):
        reasons.append("registers_default_or_inferred")
    if any(
        getattr(state, key) != 0
        for key in ("autonomy_drive", "safety_drive", "autonomy_condition", "safety_condition")
    ):
        reasons.append("autonomy_or_safety_default_or_inferred")
    if state.stability_threshold_inertia != 0:
        reasons.append("stability_threshold_inertia_default_or_inferred")
    peak = state.peak_routing
    if any(
        getattr(peak, key) != 0
        for key in ("harm_constraint", "rage_metabolization", "coherence", "impunity_access")
    ):
        reasons.append("peak_routing_default_or_inferred")
    if peak.loop_topology or peak.solidarity_boundary or peak.theory_of_change_style:
        reasons.append("peak_routing_default_strings")
    if state.intensity_and_capture and any(
        getattr(state.intensity_and_capture, key) != 0
        for key in ("intensity", "craft_talent", "opportunity_access", "attention_field_exposure", "capture_pressure")
    ):
        reasons.append("intensity_and_capture_default_or_inferred")
    if state.practice_stack and any(
        getattr(state.practice_stack, key) != 0
        for key in ("study", "care", "organizing", "craft", "spiritual", "risk_training")
    ):
        reasons.append("practice_stack_default_or_inferred")
    if state.collective_infrastructure and any(
        getattr(state.collective_infrastructure, key) != 0
        for key in ("network_density", "org_discipline", "resource_pool", "repression_pressure", "elite_splits")
    ):
        reasons.append("collective_infrastructure_default_or_inferred")
    if state.child_model:
        lowered = {str(k).lower() for k in state.child_model}
        if any("enneagram" in key or "personality_type" in key or key == "type" for key in lowered):
            reasons.append("enneagram_or_type_determinism")
        else:
            reasons.append("child_model_present")
    if state.narration_support is not None:
        reasons.append("narration_support_default_or_inferred")
    if state.narration_support is not None and any(
        getattr(state.narration_support, key) != 0
        for key in ("availability", "accuracy", "warmth", "coercion")
    ):
        reasons.append("narration_support_midpoint_default")
    if state.reproduction_constraints.legal_status != 0:
        reasons.append("reproduction_legal_status_defaulted")
    payload_record = record_to_dict(state)
    payload_record.pop("initial_state_provenance", None)
    payload_record.pop("yearly_integrity", None)
    payload = str(payload_record).lower()
    for token in ("placeholder", "hopeful", "enneagram", "random_rupture"):
        if token in payload:
            reasons.append(f"forbidden_token:{token}")
    return reasons


def assert_no_forbidden_defaults(state: BackboneState) -> None:
    """Raise if any illegitimate default is present."""
    reasons = forbidden_default_reasons(state)
    if reasons:
        raise ForbiddenDefaultError(sorted(set(reasons)))
