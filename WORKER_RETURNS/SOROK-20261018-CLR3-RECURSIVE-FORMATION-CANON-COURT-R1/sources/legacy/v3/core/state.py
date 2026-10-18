# v3/core/state.py
# Backbone state dataclasses. Aligned with v3config stored_state_schema.
# All numeric fields 0-100 unless noted. Clamp on set or in codec.

from __future__ import annotations

from dataclasses import dataclass, field as dc_field
from typing import Any

from v3.core.enums import DOMAIN_NAMES, DEFAULT_MAX, DEFAULT_MIN


def clamp(value: float, lo: float = DEFAULT_MIN, hi: float = DEFAULT_MAX) -> float:
    return max(lo, min(hi, value))


@dataclass
class Capacity:
    """Material capacity (0–100). Feeds AC, hostage penalty, insulation."""
    time: float = 50.0
    money: float = 50.0
    health: float = 50.0
    social_support: float = 50.0
    skill: float = 50.0
    mobility: float = 50.0
    risk_tolerance: float = 50.0
    legitimacy: float = 50.0

    def clamp_all(self) -> None:
        for k in ("time", "money", "health", "social_support", "skill", "mobility", "risk_tolerance", "legitimacy"):
            setattr(self, k, clamp(getattr(self, k)))


# Spec psychological capacity (vitality, aperture, …). Stored separately from material; derived from material when missing.
PSYCHOLOGICAL_CAPACITY_KEYS = (
    "vitality", "aperture", "reality_anchor", "binding", "coherence", "agency", "transmutation",
)


@dataclass
class PsychologicalCapacity:
    """Psychological capacity (0–100 each). Chronic shaping substrate; feeds state summary and scoring."""
    vitality: float = 50.0
    aperture: float = 50.0
    reality_anchor: float = 50.0
    binding: float = 50.0
    coherence: float = 50.0
    agency: float = 50.0
    transmutation: float = 50.0

    def clamp_all(self) -> None:
        for k in PSYCHOLOGICAL_CAPACITY_KEYS:
            if hasattr(self, k):
                setattr(self, k, clamp(getattr(self, k)))


@dataclass
class ReproductionConstraints:
    dependents: float = 0.0
    housing_insecurity: float = 0.0
    legal_status: float = 100.0  # 100 = secure
    debt: float = 0.0
    job_insecurity: float = 0.0
    caregiving_load: float = 0.0

    def clamp_all(self) -> None:
        for k in ("dependents", "housing_insecurity", "legal_status", "debt", "job_insecurity", "caregiving_load"):
            setattr(self, k, clamp(getattr(self, k)))


@dataclass
class DomainState:
    """Per-domain A/S/V/Aim; Aim splits into latent (internal) and expressed (gated by registers). Spec §9."""
    A: float = 0.0
    S: float = 0.0
    V: float = 0.0
    Aim: float = 0.0
    latent_aim: float = 0.0   # where blame/clarity sits internally (0-100)
    expressed_aim: float = 0.0  # what shows up; gated by registers + hostage + coercion (0-100)
    baseline_load: float = 0.0
    expression_rate: float = 50.0
    activation_threshold: float = 80.0
    affect_channel: str = "compartmentalization"
    buffer_type: str = ""       # per-domain structural buffer (v5: resignation, guilt, etc.)
    puncture_counter: int = 0   # v5 awareness transition counter
    puncture_years_since_last: int = 0  # consecutive years with zero punctures (for regression)

    def clamp_all(self) -> None:
        for k in ("A", "S", "V", "Aim", "latent_aim", "expressed_aim", "baseline_load", "expression_rate", "activation_threshold"):
            if hasattr(self, k):
                setattr(self, k, clamp(getattr(self, k)))


@dataclass
class AlienationVector:
    """Multi-dimensional alienation (new_version.txt, spec). Aggregate feeds mis_aim_risk; dimensions for future derivation from capacity+domain."""
    distant_others: float = 50.0
    near_others: float = 50.0
    self: float = 50.0
    moral_totality: float = 50.0

    def aggregate(self) -> float:
        """Scalar 0-100 for mis_aim_risk and backward compat."""
        return (self.distant_others + self.near_others + self.self + self.moral_totality) / 4.0

    def clamp_all(self) -> None:
        self.distant_others = clamp(self.distant_others)
        self.near_others = clamp(self.near_others)
        self.self = clamp(self.self)
        self.moral_totality = clamp(self.moral_totality)


@dataclass
class Registers:
    """Expression gates (spec §8): public/private/inner. 0-100; higher = more expression allowed."""
    public_expression_gate: float = 50.0
    private_expression_gate: float = 50.0
    inner_load: float = 50.0  # always present; internal pressure

    def clamp_all(self) -> None:
        for k in ("public_expression_gate", "private_expression_gate", "inner_load"):
            setattr(self, k, clamp(getattr(self, k)))


# Wound sensitivities (specLLM / spec): 0–100 per hook; used for scoring and Pass 1.
WOUND_SENSITIVITY_KEYS = ("shame", "fear", "anger", "abandonment", "control", "recognition", "loss")  # 0-100 each


@dataclass
class WoundVector:
    """Sensitivities per wound hook; default coping channels. All sensitivity values 0–100."""
    shame: float = 50.0
    fear: float = 50.0
    anger: float = 50.0
    abandonment: float = 50.0
    control: float = 50.0
    recognition: float = 50.0
    loss: float = 50.0
    default_coping_channels: list[str] = dc_field(default_factory=lambda: ["withdraw", "intellectualize"])

    def clamp_all(self) -> None:
        for k in WOUND_SENSITIVITY_KEYS:
            if hasattr(self, k):
                setattr(self, k, clamp(getattr(self, k)))

    def to_sensitivities_dict(self) -> dict[str, float]:
        return {k: getattr(self, k, 50.0) for k in WOUND_SENSITIVITY_KEYS if hasattr(self, k)}


@dataclass
class Crack:
    type: str = "shame_core"  # CrackType
    intensity: float = 0.0
    latent_pressure: float = 0.0
    active: bool = False
    origin_year: int = 0

    def clamp_all(self) -> None:
        self.intensity = clamp(self.intensity)
        self.latent_pressure = clamp(self.latent_pressure)


@dataclass
class BufferCostProfile:
    time_cost: float = 0.0
    money_cost: float = 0.0
    relational_cost: float = 0.0
    truth_cost: float = 0.0

    def clamp_all(self) -> None:
        for k in ("time_cost", "money_cost", "relational_cost", "truth_cost"):
            setattr(self, k, clamp(getattr(self, k)))


@dataclass
class Buffer:
    type: str = "craft"  # BufferType
    strength: float = 0.0
    cost_profile: BufferCostProfile = dc_field(default_factory=BufferCostProfile)

    def clamp_all(self) -> None:
        self.strength = clamp(self.strength)
        self.cost_profile.clamp_all()


@dataclass
class Framework:
    """Framework as metabolic operator (spec §6): id, weight, operator fields."""
    id: str = ""
    weight: float = 0.0
    acute_delta: dict[str, Any] = dc_field(default_factory=dict)   # capacity key -> delta (first N years)
    chronic_delta: dict[str, Any] = dc_field(default_factory=dict) # capacity key -> delta after N years
    half_life_years: int = 0       # when benefits decay / costs accumulate; 0 = no decay
    failure_mode: str = ""         # irony_spiral, sectarian_hardening, collapse, etc.
    enemy_requirement: float = 0.0 # 0 = none, 100 = strong
    institutional_affinities: list[str] = dc_field(default_factory=list)  # strata/domains that reward it
    tenure_years: int = 0          # years held (optional)

    def clamp_all(self) -> None:
        self.weight = clamp(self.weight)
        self.enemy_requirement = clamp(self.enemy_requirement)


@dataclass
class Magnet:
    """Persistent relationship/institution magnet (specLLM); yearly step applies intensify/decay."""
    id: str = ""
    magnet_type: str = "friend"
    label: str = ""
    intensity: float = 50.0   # 0-100; decay over time, intensify when reinforced
    tenure_years: int = 0     # years in active list

    def clamp_all(self) -> None:
        self.intensity = clamp(self.intensity)


@dataclass
class CollectiveInfrastructure:
    network_density: float = 0.0
    org_discipline: float = 0.0
    resource_pool: float = 0.0
    repression_pressure: float = 0.0
    elite_splits: float = 0.0

    def clamp_all(self) -> None:
        for k in ("network_density", "org_discipline", "resource_pool", "repression_pressure", "elite_splits"):
            setattr(self, k, clamp(getattr(self, k)))


@dataclass
class PracticeStack:
    study: float = 0.0
    care: float = 0.0
    organizing: float = 0.0
    craft: float = 0.0
    spiritual: float = 0.0
    risk_training: float = 0.0

    def clamp_all(self) -> None:
        for k in ("study", "care", "organizing", "craft", "spiritual", "risk_training"):
            setattr(self, k, clamp(getattr(self, k)))


@dataclass
class AppetiteProfile:
    status: float = 0.0
    control: float = 0.0
    sensuality: float = 0.0
    care: float = 0.0

    def clamp_all(self) -> None:
        for k in ("status", "control", "sensuality", "care"):
            setattr(self, k, clamp(getattr(self, k)))


@dataclass
class PeakRouting:
    loop_topology: str = "self_contained"  # LoopTopology
    solidarity_boundary: str = "in_group"  # SolidarityBoundary
    harm_constraint: float = 50.0
    rage_metabolization: float = 50.0
    theory_of_change_style: str = "institution_building"  # TheoryOfChangeStyle
    coherence: float = 50.0
    impunity_access: float = 0.0
    appetite_profile: AppetiteProfile = dc_field(default_factory=AppetiteProfile)
    # Hysteresis: consecutive years requirements met for topology transitions (persisted for sticky transitions).
    topology_hysteresis_years: dict[str, int] = dc_field(default_factory=dict)  # keys: to_reciprocal, to_extractive, to_self_contained

    def clamp_all(self) -> None:
        for k in ("harm_constraint", "rage_metabolization", "coherence", "impunity_access"):
            setattr(self, k, clamp(getattr(self, k)))
        self.appetite_profile.clamp_all()


@dataclass
class IntensityAndCapture:
    intensity: float = 50.0
    craft_talent: float = 0.0
    opportunity_access: float = 0.0
    attention_field_exposure: float = 0.0
    capture_pressure: float = 0.0

    def clamp_all(self) -> None:
        for k in ("intensity", "craft_talent", "opportunity_access", "attention_field_exposure", "capture_pressure"):
            setattr(self, k, clamp(getattr(self, k)))


@dataclass
class StyleTraits:
    playfulness: float = 50.0
    novelty_seeking: float = 50.0
    conscientiousness: float = 50.0
    social_energy: float = 50.0
    absurdist_humor: float = 50.0
    aesthetic_sensitivity: float = 50.0
    impulsivity: float = 50.0

    def clamp_all(self) -> None:
        for k in ("playfulness", "novelty_seeking", "conscientiousness", "social_energy",
                  "absurdist_humor", "aesthetic_sensitivity", "impulsivity"):
            setattr(self, k, clamp(getattr(self, k)))


# Trace 8: Expectation baselines + striving (starter_engine, need_axis_rules).
NEED_AXES = (
    "attachment", "safety", "belonging", "status", "competence",
    "autonomy", "meaning", "justice", "beauty_play", "eros_intimacy",
)
BASELINE_STATES = ("entitled", "hopeful", "forbidden", "hopeless")


@dataclass
class StrivingObject:
    """Stateful investment target; events can attach to striving_object_id (starter_engine)."""
    id: str = ""
    label: str = ""
    need_axis: str = ""
    started_age: int = 0
    investment: int = 50  # 0-100
    identity_load: int = 50  # 0-100
    feasibility_belief: int = 50  # 0-100
    social_support: int = 50  # 0-100
    recent_momentum: int = 0  # -50..+50
    tags: list[str] = dc_field(default_factory=list)  # for event-template matching
    secrecy: int = 0  # 0-100
    costs: list[str] = dc_field(default_factory=list)  # narrative costs
    active: bool = True  # False = retired (faded)

    def clamp_all(self) -> None:
        self.investment = max(0, min(100, self.investment))
        self.identity_load = max(0, min(100, self.identity_load))
        self.feasibility_belief = max(0, min(100, self.feasibility_belief))
        self.social_support = max(0, min(100, self.social_support))
        self.recent_momentum = max(-50, min(50, self.recent_momentum))
        self.secrecy = max(0, min(100, self.secrecy))


@dataclass
class GiftShard:
    """Positive prediction-error shard: new possibility installed (starter_engine). Same shape as DisruptionShard."""
    id: str = ""
    year: int = 0
    age: int = 0
    need_axis: str = ""
    striving_object_id: str = ""
    label: str = ""
    valence: str = "positive"
    prediction_error: str = "medium"
    opacity: str = "low"


@dataclass
class DisruptionShard:
    """Negative/mixed prediction-error shard (starter_engine). Same shape as GiftShard."""
    id: str = ""
    year: int = 0
    age: int = 0
    need_axis: str = ""
    striving_object_id: str = ""
    label: str = ""
    valence: str = "negative"
    prediction_error: str = "medium"
    opacity: str = "medium"
    malheur_risk: bool = False  # True when violation targets a striving with high identity_load (Tier 3)


# Rupture / metabolization (specLLM): epistemic rupture shards and multi-year metabolization.
@dataclass
class RuptureShard:
    """Persisted after an epistemic_rupture event; drives plasticity and framework selection."""
    id: str = ""
    year: int = 0
    age: int = 0
    violated_assumption: str = ""
    domain: str = ""
    opacity: str = "medium"  # low, medium, high
    prediction_error: str = "medium"  # low, medium, high
    current_status: str = "raw"  # raw, narrativized, sealed, integrated, mis_aimed
    intrusive_return_rate: int = 50  # 0-100
    meaning_attempts: list[str] = dc_field(default_factory=list)

    def clamp_all(self) -> None:
        self.intrusive_return_rate = max(0, min(100, self.intrusive_return_rate))


METABOLIZATION_SEVERITY = ("micro", "major", "malheur")
METABOLIZATION_MODE = ("assimilation", "accommodation", "sealing", "collapse", "transmutation", "mis_aim")
METABOLIZATION_STATUS = ("raw", "working", "provisionally_narrated", "integrated", "sealed", "chronic")


@dataclass
class MetabolizationProcess:
    """Multi-year metabolization after epistemic rupture; persists until resolved."""
    id: str = ""
    start_year: int = 0
    start_age: int = 0
    domain: str = ""
    violated_assumption: str = ""
    severity: str = "major"  # micro, major, malheur
    opacity: str = "medium"
    prediction_error: str = "medium"
    mode: str = "accommodation"  # assimilation, accommodation, collapse, sealing, transmutation, mis_aim
    status: str = "raw"  # raw, working, provisionally_narrated, integrated, sealed, chronic
    cluster: str = ""  # reconfiguration cluster from template: hardening_protection, sensitivity_exposure, etc.
    plasticity_years_left: int = 0
    intrusive_return_rate: int = 50  # 0-100
    intrusive_return_rate_prev: int = 50  # for IRR-drop drain in dissipation step
    narrators: list[str] = dc_field(default_factory=list)  # parent, peer, religion, movement, therapy, art, none
    provisional_frame: str | None = None  # framework_id if adopted
    downstream_biases: dict[str, Any] = dc_field(default_factory=dict)
    reactivation_triggers: list[str] = dc_field(default_factory=list)
    sealed_candidate_years: int = 0  # consecutive years coercion high + availability low
    post_plasticity_years: int = 0   # years since plasticity_years_left hit 0 without reaching provisionally_narrated
    start_plasticity_years: int = 0  # set at creation for raw→working transition

    def clamp_all(self) -> None:
        self.intrusive_return_rate = max(0, min(100, self.intrusive_return_rate))
        self.intrusive_return_rate_prev = max(0, min(100, self.intrusive_return_rate_prev))


@dataclass
class NarrationSupport:
    """Derived per year: availability/accuracy/warmth/coercion of narrators (0-100)."""
    availability: int = 50
    accuracy: int = 50
    warmth: int = 50
    coercion: int = 50

    def clamp_all(self) -> None:
        for k in ("availability", "accuracy", "warmth", "coercion"):
            setattr(self, k, max(0, min(100, getattr(self, k, 50))))


# Placeholder for macro field (economy, repression, movement heat, etc.)
@dataclass
class MacroField:
    """Macro field conditions. Contents TBD; step order expects state.field."""
    raw: dict[str, Any] = dc_field(default_factory=dict)
    provenance: dict[str, Any] = dc_field(default_factory=dict)


# CalibrationRegime: societal "normal" per nation/sect_class/school/work (spec §5).
@dataclass
class CalibrationRegime:
    """Norm center, uniqueness expectation, outlier penalties/incentives, dream window."""
    norm_center: str = "middle"  # or identifier for center of acceptable band
    uniqueness_norm: float = 50.0  # 0–100 how much "special individual" is expected
    outlier_penalties: list[dict[str, Any]] = dc_field(default_factory=list)  # [{topic/behavior, strength}]
    outlier_incentives: list[dict[str, Any]] = dc_field(default_factory=list)  # what becomes rewarded under conditions
    dream_window: str = ""  # available futures description or key

    def clamp_all(self) -> None:
        self.uniqueness_norm = clamp(self.uniqueness_norm)


# BoundaryMap entry per domain: discouraged/permitted/incentivized positions + trigger conditions.
@dataclass
class BoundaryMapEntry:
    """Per-domain: which positions are discouraged, permitted, incentivized; trigger conditions."""
    discouraged: list[str] = dc_field(default_factory=list)  # position labels
    permitted: list[str] = dc_field(default_factory=list)
    incentivized: list[str] = dc_field(default_factory=list)
    trigger_conditions: list[dict[str, Any]] = dc_field(default_factory=list)  # [{condition, effect}]


# First-class stratum (spec: provision_strength, coercion_strength, contradiction_load, visibility_of_complicity, salience).
@dataclass
class Stratum:
    """One stratum in the stack (planetary → … → self). All strength/load values 0–100."""
    level: int = 0
    name: str = ""
    description: str = ""
    material_relation: str = "intermediary"  # exploiter|exploited|intermediary|buffer|superfluous
    hegemonic_story: str = ""               # narrative this stratum tells about who "we" are
    loyalty_demand: str = ""                # what obedience this stratum demands
    provision_strength: float = 50.0
    coercion_strength: float = 50.0
    contradiction_load: float = 50.0
    visibility_of_complicity: float = 50.0
    salience: float = 50.0

    def clamp_all(self) -> None:
        for k in ("provision_strength", "coercion_strength", "contradiction_load", "visibility_of_complicity", "salience"):
            if hasattr(self, k):
                setattr(self, k, clamp(getattr(self, k)))

    def to_salient_dict(self) -> dict[str, Any]:
        """For state summary: coercion/provision/contradiction (legacy keys) + visibility."""
        return {
            "level": self.level,
            "name": self.name[:80] if self.name else str(self.level),
            "coercion": self.coercion_strength,
            "provision": self.provision_strength,
            "contradiction": self.contradiction_load,
            "visibility_of_complicity": self.visibility_of_complicity,
            "salience": self.salience,
        }


@dataclass
class BackboneState:
    """Full backbone state. Persisted year-to-year."""
    year: int = 0
    age: int = 0
    field: MacroField = dc_field(default_factory=MacroField)
    calibration_regime: CalibrationRegime | None = None  # spec §5; per nation/sect/school/work
    boundary_map: dict[str, BoundaryMapEntry] = dc_field(default_factory=dict)  # per domain
    strata_salience: dict[str, Any] = dc_field(default_factory=dict)
    strata_stack: list[Stratum] = dc_field(default_factory=list)
    events_this_year: list[dict[str, Any]] = dc_field(default_factory=list)
    micro_trace_this_year: list[dict[str, Any]] = dc_field(default_factory=list)
    capacity: Capacity = dc_field(default_factory=Capacity)
    psychological_capacity: PsychologicalCapacity = dc_field(default_factory=PsychologicalCapacity)
    reproduction_constraints: ReproductionConstraints = dc_field(default_factory=ReproductionConstraints)
    domains: dict[str, DomainState] = dc_field(default_factory=dict)
    alienation: float = 0.0  # scalar for mis_aim_risk; kept in sync with alienation_vector.aggregate()
    alienation_vector: AlienationVector = dc_field(default_factory=AlienationVector)  # multi-dimensional (new_version, spec)
    wound_vector: WoundVector = dc_field(default_factory=WoundVector)
    cracks: list[Crack] = dc_field(default_factory=list)
    buffers: list[Buffer] = dc_field(default_factory=list)
    frameworks: list[Framework] = dc_field(default_factory=list)
    frameworks_dormant: list = dc_field(default_factory=list)
    collective_infrastructure: CollectiveInfrastructure = dc_field(default_factory=CollectiveInfrastructure)
    practice_stack: PracticeStack = dc_field(default_factory=PracticeStack)
    peak_routing: PeakRouting = dc_field(default_factory=PeakRouting)
    intensity_and_capture: IntensityAndCapture = dc_field(default_factory=IntensityAndCapture)
    style_traits: StyleTraits = dc_field(default_factory=StyleTraits)
    rendered_output: dict[str, Any] | None = None
    rupture_shards: list[RuptureShard] = dc_field(default_factory=list)
    metabolization_processes: list[MetabolizationProcess] = dc_field(default_factory=list)
    initial_state_provenance: dict[str, Any] = dc_field(default_factory=dict)
    yearly_integrity: dict[str, Any] = dc_field(default_factory=dict)
    # V515b.2 PressureFlow: current/trace/memory membrane.
    # These fields are runtime evidence, not persona voice, and analyst_pressure_account
    # must not be passed to render/chat/persona surfaces except in debug/state artifacts.
    pressure_flow_history: list[dict[str, Any]] = dc_field(default_factory=list)
    pressure_flow_memory: dict[str, Any] = dc_field(default_factory=dict)
    surface_psyche_profile: dict[str, Any] = dc_field(default_factory=dict)
    analyst_pressure_account: dict[str, Any] = dc_field(default_factory=dict)
    generation_diagnostics: list[dict[str, Any]] = dc_field(default_factory=list)  # backbone-init failures indexed here
    plasticity_window: dict[str, Any] = dc_field(default_factory=dict)  # years_left, framework_switch_sensitivity, etc.
    narration_support: NarrationSupport | None = None  # derived per year from metabolization narrators (availability, accuracy, warmth, coercion)
    metabolic_style: dict[str, Any] = dc_field(default_factory=dict)  # spec §7: current (transmuting|compartmentalizing|anesthetizing|collapsing), trend (stabilizing|deteriorating)
    expectation_baseline: dict[str, str] = dc_field(default_factory=dict)  # NeedAxis -> entitled|hopeful|forbidden|hopeless
    striving_objects: list[StrivingObject] = dc_field(default_factory=list)
    gift_shards: list[GiftShard] = dc_field(default_factory=list)
    disruption_shards: list[DisruptionShard] = dc_field(default_factory=list)
    registers: Registers = dc_field(default_factory=Registers)  # spec §8: public/private expression gates, inner_load
    child_model: dict[str, Any] = dc_field(default_factory=dict)  # specLLM: assumed_rules, taboos, what_counts_as_possible (Pass 1)
    active_magnets: list[Magnet] = dc_field(default_factory=list)  # specLLM: persistent magnets; yearly intensify/decay
    v5_runtime_input_bundle: dict[str, Any] = dc_field(default_factory=dict)  # v5 bridge carrier/ref bundle; inert until explicit bridge use
    v5_runtime_input_refs: list[str] = dc_field(default_factory=list)  # optional identifiers/provenance refs for the v5 bridge
    v5_bridge_status: str = "not_attached"  # not_attached|attached|degraded|blocked
    # Autonomy/safety drives + lived conditions (0–100); revision 2026.02.25
    autonomy_drive: float = 50.0      # demand for agency
    safety_drive: float = 50.0        # demand for protection
    autonomy_condition: float = 50.0  # actual latitude
    safety_condition: float = 50.0    # actual stability
    # Stability-threshold inertia (maximal): trauma sticks until integrated/held
    stability_threshold_inertia: float = 0.0   # 0–100, clamped
    stability_delta_applied_this_year: bool = False

    def __post_init__(self) -> None:
        if not self.domains:
            for name in DOMAIN_NAMES:
                self.domains[name] = DomainState()

    def clamp_all(self) -> None:
        self.alienation_vector.clamp_all()
        self.alienation = clamp(self.alienation_vector.aggregate())
        if self.calibration_regime is not None:
            self.calibration_regime.clamp_all()
        for entry in (self.boundary_map or {}).values():
            if hasattr(entry, "clamp_all"):
                entry.clamp_all()
        self.wound_vector.clamp_all()
        self.capacity.clamp_all()
        self.psychological_capacity.clamp_all()
        self.reproduction_constraints.clamp_all()
        for d in self.domains.values():
            d.clamp_all()
        for s in self.strata_stack:
            s.clamp_all()
        for c in self.cracks:
            c.clamp_all()
        for b in self.buffers:
            b.clamp_all()
        for f in self.frameworks:
            f.clamp_all()
        self.collective_infrastructure.clamp_all()
        self.practice_stack.clamp_all()
        self.peak_routing.clamp_all()
        self.intensity_and_capture.clamp_all()
        self.style_traits.clamp_all()
        for r in self.rupture_shards:
            r.clamp_all()
        for m in self.metabolization_processes:
            m.clamp_all()
        for s in self.striving_objects:
            s.clamp_all()
        self.registers.clamp_all()
        for m in self.active_magnets:
            m.clamp_all()
        self.v5_bridge_status = str(self.v5_bridge_status or "not_attached")
        self.v5_runtime_input_refs = [str(x) for x in self.v5_runtime_input_refs if str(x)]
        if isinstance(self.v5_runtime_input_bundle, dict):
            self.v5_runtime_input_bundle = dict(self.v5_runtime_input_bundle)
        else:
            self.v5_runtime_input_bundle = {}
        self.autonomy_drive = clamp(self.autonomy_drive, 0.0, 100.0)
        self.safety_drive = clamp(self.safety_drive, 0.0, 100.0)
        self.autonomy_condition = clamp(self.autonomy_condition, 0.0, 100.0)
        self.safety_condition = clamp(self.safety_condition, 0.0, 100.0)
        self.stability_threshold_inertia = clamp(self.stability_threshold_inertia, 0.0, 100.0)
