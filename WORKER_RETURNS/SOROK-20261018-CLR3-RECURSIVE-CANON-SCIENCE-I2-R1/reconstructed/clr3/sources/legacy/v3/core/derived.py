# v3/core/derived.py
# Compute derived indices from stored state. Do not mutate state.
# Formulas from v3config derived_indices.

from __future__ import annotations

from dataclasses import dataclass

from v3.core.enums import DOMAIN_NAMES
from v3.core.state import BackboneState, Registers, clamp


@dataclass
class DerivedIndices:
    """Computed each year; not persisted unless cached."""
    hostage_index: float = 0.0
    agency_capacity_AC: float = 0.0
    insulation_score: float = 0.0
    structural_lucidity_SL: float = 0.0
    mis_aim_risk: float = 0.0
    peak_regime: bool = False
    metabolic_style_current: str = "compartmentalizing"
    metabolic_style_trend: str = "deteriorating"
    che_jesus_eligible: bool = False  # peak_regime AND liberatory orientation (starter_engine base-rate gate)
    # Autonomy/safety gaps + alignment (revision 2026.02.25)
    autonomy_gap: float = 0.0
    safety_gap: float = 0.0
    gap_pressure_index: float = 0.0
    alignment_vector: float = 0.0  # -100 = will amplification, +100 = will alignment
    stability_threshold: float = 0.0  # higher = more brittle / closer to breakdown (RMT analogue)
    health_level: float = 50.0  # composite resilience/wear (revision 2026.02.25)


# v3config weights for hostage_index (all fields 0–100; higher = more constraint / insecurity)
HOSTAGE_WEIGHTS = {
    "dependents": 0.25,
    "housing_insecurity": 0.20,
    "legal_insecurity": 0.15,
    "debt": 0.15,
    "job_insecurity": 0.15,
    "caregiving_load": 0.10,
}


def compute_hostage_index(state: BackboneState) -> float:
    """Weighted sum of reproduction constraints (v3config). No inversion: higher field = more hostage."""
    r = state.reproduction_constraints
    # legal_status: 100 = secure → legal_insecurity = 100 - legal_status (0 = secure, 100 = insecure)
    legal_insecurity = 100.0 - r.legal_status
    s = (
        HOSTAGE_WEIGHTS["dependents"] * r.dependents
        + HOSTAGE_WEIGHTS["housing_insecurity"] * r.housing_insecurity
        + HOSTAGE_WEIGHTS["legal_insecurity"] * legal_insecurity
        + HOSTAGE_WEIGHTS["debt"] * r.debt
        + HOSTAGE_WEIGHTS["job_insecurity"] * r.job_insecurity
        + HOSTAGE_WEIGHTS["caregiving_load"] * r.caregiving_load
    )
    return clamp(s)


def compute_agency_capacity_AC(state: BackboneState, hostage_index: float) -> float:
    """Weighted sum of capacity minus hostage penalty. v3config: base_weights, hostage_penalty_multiplier 0.50."""
    c = state.capacity
    base = (
        0.20 * c.time
        + 0.15 * c.money
        + 0.15 * c.health
        + 0.15 * c.social_support
        + 0.10 * c.skill
        + 0.10 * c.mobility
        + 0.10 * c.risk_tolerance
        + 0.05 * c.legitimacy
    )
    penalty = hostage_index * 0.50
    return clamp(base - penalty, 0, 100)


def compute_insulation_score(state: BackboneState) -> float:
    """Top-3 buffer strengths + money. v3config: topk 3, buffers_strength 0.70, money 0.30."""
    strengths = sorted([b.strength for b in state.buffers], reverse=True)[:3]
    buf_sum = sum(strengths) / 3.0 if strengths else 0.0
    money = state.capacity.money
    return clamp(0.70 * buf_sum + 0.30 * money / 100.0 * 100.0)


def _domain_lucidity(A: float, V: float, insulation_score: float) -> float:
    """A_minus_insulation_plus_viscerality: A*1.0 - insulation*0.40 + V*0.20."""
    return clamp(A - 0.40 * insulation_score + 0.20 * V, 0, 100)


def compute_structural_lucidity_SL(state: BackboneState, insulation_score: float) -> float:
    """Average domain lucidity over empire_occupation, nation_state, sect_class_ethnicity."""
    total = 0.0
    n = 0
    for name in DOMAIN_NAMES:
        if name in state.domains:
            d = state.domains[name]
            total += _domain_lucidity(d.A, d.V, insulation_score)
            n += 1
    return clamp(total / n) if n else 0.0


def compute_mis_aim_risk(state: BackboneState, hostage_index: float) -> float:
    """alienation 0.40 + hostage_index 0.30 + organizing_deficit 0.30."""
    organizing_deficit = 100.0 - state.practice_stack.organizing
    return clamp(
        0.40 * state.alienation
        + 0.30 * hostage_index
        + 0.30 * organizing_deficit / 100.0 * 100.0
    )


def compute_peak_regime(
    state: BackboneState,
    SL: float,
    AC: float,
    hostage_index: float,
    coherence_min_years: int = 2,
    coherence_min_value: float = 70.0,
    SL_min: float = 75.0,
    AC_min: float = 75.0,
    hostage_index_max: float = 40.0,
) -> bool:
    """True if eligible for peak regime (v3config peak_gates). We don't track consecutive years here; caller may."""
    if SL < SL_min or AC < AC_min or hostage_index > hostage_index_max:
        return False
    if state.peak_routing.coherence < coherence_min_value:
        return False
    return True


def orientation_liberatory(state: BackboneState) -> bool:
    """Liberatory (Che/Jesus) vs dominative (predatory). starter_engine: loop reciprocal, solidarity beyond in_group, theory_of_change not predatory."""
    pr = state.peak_routing
    loop = getattr(pr, "loop_topology", "self_contained")
    solidarity = getattr(pr, "solidarity_boundary", "in_group")
    toc = getattr(pr, "theory_of_change_style", "institution_building")
    if loop != "reciprocal":
        return False
    if solidarity == "in_group":
        return False
    if toc in ("predation", "extractive", "dominative"):
        return False
    return True


def compute_che_jesus_eligible(
    state: BackboneState,
    SL: float,
    AC: float,
    hostage_index: float,
    SL_min: float = 75.0,
    AC_min: float = 75.0,
    hostage_index_max: float = 40.0,
    coherence_min: float = 70.0,
    require_liberatory_orientation: bool = True,
) -> bool:
    """True only if peak conditions (SL+AC+hostage+coherence) AND liberatory orientation. Base-rate gate: extremely uncommon."""
    if not compute_peak_regime(state, SL, AC, hostage_index, coherence_min_value=coherence_min, SL_min=SL_min, AC_min=AC_min, hostage_index_max=hostage_index_max):
        return False
    if require_liberatory_orientation and not orientation_liberatory(state):
        return False
    return True


def compute_metabolic_style(
    state: BackboneState,
    hostage_index: float,
    insulation_score: float,
) -> tuple[str, str]:
    """
    Return (current, trend). Current: transmuting | compartmentalizing | anesthetizing | collapsing.
    Trend: stabilizing | deteriorating. Uses capacity vector, hostage, contradiction load, buffers.
    """
    pc = state.psychological_capacity
    vitality = getattr(pc, "vitality", 50.0)
    aperture = getattr(pc, "aperture", 50.0)
    coherence = getattr(state.peak_routing, "coherence", 50.0)
    # Contradiction load: inverse of coherence + crack pressure
    crack_load = sum(getattr(c, "intensity", 0) + getattr(c, "latent_pressure", 0) for c in state.cracks) / max(len(state.cracks) * 100.0, 1.0)
    contradiction_load = (100.0 - coherence) * 0.6 + crack_load * 0.4
    buf_avg = insulation_score  # 0-100
    # Heuristic: high hostage + low buffers + high contradiction → collapsing
    if hostage_index >= 55 and buf_avg < 35 and (contradiction_load >= 50 or coherence < 40):
        current = "collapsing"
    # Low vitality + decent buffers → anesthetizing
    elif vitality < 40 and buf_avg >= 40:
        current = "anesthetizing"
    # High vitality + aperture + low hostage → transmuting
    elif vitality >= 55 and aperture >= 50 and hostage_index < 50:
        current = "transmuting"
    else:
        current = "compartmentalizing"
    # Trend: stabilizing if coherence and vitality above 50 and hostage not extreme
    if coherence >= 50 and vitality >= 50 and hostage_index < 60:
        trend = "stabilizing"
    else:
        trend = "deteriorating"
    return (current, trend)


def compute_autonomy_gap(state: BackboneState) -> float:
    """max(0, drive - condition)."""
    return clamp(max(0.0, getattr(state, "autonomy_drive", 50) - getattr(state, "autonomy_condition", 50)), 0, 100)


def compute_safety_gap(state: BackboneState) -> float:
    """max(0, drive - condition)."""
    return clamp(max(0.0, getattr(state, "safety_drive", 50) - getattr(state, "safety_condition", 50)), 0, 100)


def compute_gap_pressure_index(autonomy_gap: float, safety_gap: float) -> float:
    """0.5 * autonomy_gap + 0.5 * safety_gap."""
    return clamp(0.5 * autonomy_gap + 0.5 * safety_gap, 0, 100)


def compute_stability_threshold(
    gap_pressure_index: float,
    hostage_index: float,
    mis_aim_risk: float,
    insulation_score: float,
    state: BackboneState,
) -> float:
    """Higher = more brittle / closer to breakdown. Positive: gap_pressure, hostage, mis_aim; negative: insulation, health, coherence."""
    health = state.capacity.health
    coherence = getattr(state.peak_routing, "coherence", 50.0)
    raw = (
        gap_pressure_index * 0.25
        + hostage_index * 0.25
        + mis_aim_risk * 0.25
        - insulation_score * 0.15
        - (100.0 - health) * 0.05
        - coherence * 0.05
    )
    raw += getattr(state, "stability_threshold_inertia", 0.0)
    return clamp(raw, 0.0, 100.0)


def compute_alignment_vector(
    state: BackboneState,
    gap_pressure_index: float,
    hostage_index: float,
    mis_aim_risk: float,
) -> float:
    """Positive from organizing/spiritual, social_support, network_density, org_discipline; negative from gap_pressure, hostage, mis_aim. Clamp [-100, 100]."""
    pos = 0.0
    ps = state.practice_stack
    pos += getattr(ps, "organizing", 0) / 100.0 * 15.0
    pos += getattr(ps, "spiritual", 0) / 100.0 * 10.0
    pos += state.capacity.social_support / 100.0 * 25.0
    ci = state.collective_infrastructure
    pos += getattr(ci, "network_density", 0) / 100.0 * 15.0
    pos += getattr(ci, "org_discipline", 0) / 100.0 * 10.0
    neg = gap_pressure_index / 100.0 * 30.0 + hostage_index / 100.0 * 25.0 + mis_aim_risk / 100.0 * 25.0
    raw = (pos - neg) * 2.0  # scale so typical range maps to [-100, 100]
    return clamp(raw, -100.0, 100.0)


def compute_health_level(
    state: BackboneState,
    stability_threshold: float,
    insulation_score: float,
) -> float:
    """Composite resilience/wear: capacity.health primary; stability (neg), insulation/support (pos). Clamp [0, 100]."""
    health = state.capacity.health
    support = state.capacity.social_support / 100.0 * 20.0
    net_density = getattr(state.collective_infrastructure, "network_density", 0) / 100.0 * 10.0
    raw = health - stability_threshold * 0.2 + insulation_score * 0.15 + support + net_density
    return clamp(raw, 0.0, 100.0)


def compute_registers_from_state(state: BackboneState, hostage_index: float) -> Registers:
    """
    Compute expression gates and inner load from psychological capacity, wounds, and constraint.

    public_expression_gate:
        Driven by aperture (cognitive openness) minus hostage pressure.
        Low aperture → cognitively constricted, goes quiet under pressure.
        High hostage_index → external constraints limit freedom to express publicly.
        Formula: aperture - hostage_index * 0.4

    private_expression_gate:
        Driven by binding (internal coherence) and vitality (aliveness).
        Both are needed for internal expression capacity.
        Formula: (binding + vitality) / 2.0

    inner_load:
        Accumulated wound pressure above baseline (50.0).
        Sum of excess activation across all 7 wound dimensions, scaled.
        Formula: 50 + sum(max(0, w - 50) for each wound) / 4.0
        At baseline (all wounds = 50) → inner_load = 50 (neutral).
        As wounds accumulate above 50 → inner_load rises proportionally.
    """
    pc = state.psychological_capacity
    aperture = float(getattr(pc, "aperture", 50.0))
    binding = float(getattr(pc, "binding", 50.0))
    vitality = float(getattr(pc, "vitality", 50.0))

    wv = state.wound_vector
    wound_fields = [
        float(getattr(wv, "shame", 50.0)),
        float(getattr(wv, "fear", 50.0)),
        float(getattr(wv, "anger", 50.0)),
        float(getattr(wv, "abandonment", 50.0)),
        float(getattr(wv, "control", 50.0)),
        float(getattr(wv, "recognition", 50.0)),
        float(getattr(wv, "loss", 50.0)),
    ]
    wound_excess = sum(max(0.0, w - 50.0) for w in wound_fields)

    public_gate = clamp(aperture - hostage_index * 0.4)
    private_gate = clamp((binding + vitality) / 2.0)
    inner_load = clamp(50.0 + wound_excess / 4.0)

    return Registers(
        public_expression_gate=public_gate,
        private_expression_gate=private_gate,
        inner_load=inner_load,
    )


def compute_all_derived(state: BackboneState) -> DerivedIndices:
    """Compute all derived indices from current state. Writes metabolic_style to state (spec §7)."""
    hostage_index = compute_hostage_index(state)
    agency_capacity_AC = compute_agency_capacity_AC(state, hostage_index)
    insulation_score = compute_insulation_score(state)
    structural_lucidity_SL = compute_structural_lucidity_SL(state, insulation_score)
    mis_aim_risk = compute_mis_aim_risk(state, hostage_index)
    peak_regime = compute_peak_regime(state, structural_lucidity_SL, agency_capacity_AC, hostage_index)
    che_jesus_eligible = compute_che_jesus_eligible(state, structural_lucidity_SL, agency_capacity_AC, hostage_index)
    metabolic_current, metabolic_trend = compute_metabolic_style(state, hostage_index, insulation_score)
    state.metabolic_style = {"current": metabolic_current, "trend": metabolic_trend}
    # Compute expression gates + inner load and write to state (spec §8)
    state.registers = compute_registers_from_state(state, hostage_index)
    autonomy_gap = compute_autonomy_gap(state)
    safety_gap = compute_safety_gap(state)
    gap_pressure_index = compute_gap_pressure_index(autonomy_gap, safety_gap)
    alignment_vector = compute_alignment_vector(state, gap_pressure_index, hostage_index, mis_aim_risk)
    stability_threshold = compute_stability_threshold(
        gap_pressure_index, hostage_index, mis_aim_risk, insulation_score, state
    )
    health_level = compute_health_level(state, stability_threshold, insulation_score)
    return DerivedIndices(
        hostage_index=hostage_index,
        agency_capacity_AC=agency_capacity_AC,
        insulation_score=insulation_score,
        structural_lucidity_SL=structural_lucidity_SL,
        mis_aim_risk=mis_aim_risk,
        peak_regime=peak_regime,
        metabolic_style_current=metabolic_current,
        metabolic_style_trend=metabolic_trend,
        che_jesus_eligible=che_jesus_eligible,
        autonomy_gap=autonomy_gap,
        safety_gap=safety_gap,
        gap_pressure_index=gap_pressure_index,
        alignment_vector=alignment_vector,
        stability_threshold=stability_threshold,
        health_level=health_level,
    )


def derived_to_dict(d: DerivedIndices) -> dict:
    """Serialize DerivedIndices to a JSON-serializable dict (for store/logs)."""
    out = {
        "hostage_index": d.hostage_index,
        "agency_capacity_AC": d.agency_capacity_AC,
        "insulation_score": d.insulation_score,
        "structural_lucidity_SL": d.structural_lucidity_SL,
        "mis_aim_risk": d.mis_aim_risk,
        "peak_regime": d.peak_regime,
        "metabolic_style_current": d.metabolic_style_current,
        "metabolic_style_trend": d.metabolic_style_trend,
        "che_jesus_eligible": d.che_jesus_eligible,
    }
    for key in ("autonomy_gap", "safety_gap", "gap_pressure_index", "alignment_vector", "stability_threshold", "health_level"):
        if hasattr(d, key):
            out[key] = getattr(d, key)
    return out
