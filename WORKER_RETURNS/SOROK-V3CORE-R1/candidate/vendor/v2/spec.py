"""
Rawlsing v4.1 - Integrated Canonical Specification (Python)

This is the authoritative, integrated spec for Rawlsing v4.x persona generation.
It consolidates and resolves all concepts from:
- 01—reconfiguration.md (data ingestion, world cubes)
- 02—new_spec.md (core persona structures)
- 03—with_enneagram.md (Enneagram integration)
- 04—Rawlsing_v4.0.md & 04—Rawlsling_v4.1.md (conceptual framework)
- 05—implementation.md (pipeline structure)
- 06—integration.md (yearly recursion, band aggregation)
- 07—supplement.md (family generation, WVS usage)

All numeric values are 0-100 unless otherwise specified.
All functions are deterministic modulo explicit randomness (use seeded RNG for tests).
"""

from dataclasses import dataclass, field, replace
from typing import Dict, List, Optional, Literal, Any, Tuple, Callable, Union
from enum import Enum
import numpy as np
from datetime import datetime

# Import config loader (handle both package and direct import)
try:
    from .config_loader import get_config_loader
except ImportError:
    from config_loader import get_config_loader

try:
    from .country_reference import normalize_country_ref
except ImportError:
    from country_reference import normalize_country_ref

# Parent type inference (Naranjo/Ichazo heuristic)
try:
    from .parent_type_inference import infer_parent_type_most_likely
except ImportError:
    from parent_type_inference import infer_parent_type_most_likely

# Recursion delta schema (v4.2 palimpsest)
try:
    from .recursion_schema import (
        RecursionDelta, Palimpsest, get_grounded_context,
        format_grounded_context_for_prompt,
        NextDaySnapshot, get_skip_back_view,
    )
except ImportError:
    from recursion_schema import (
        RecursionDelta, Palimpsest, get_grounded_context,
        format_grounded_context_for_prompt,
        NextDaySnapshot, get_skip_back_view,
    )

# Driver age schema (developmental filtering)
try:
    from .driver_age_schema import get_field_values_for_age
except ImportError:
    from driver_age_schema import get_field_values_for_age

# Life snapshot data derivation (present-year recursion)
try:
    from .life_snapshot_from_data import data_derived_life_snapshot as compute_data_derived_life_snapshot
except ImportError:
    from life_snapshot_from_data import data_derived_life_snapshot as compute_data_derived_life_snapshot

# Life Simulation Layer (conversation: container, season, today, attention)
try:
    from .life_simulation_schema import (
        build_life_simulation_state,
        attention_to_reply_limits,
        LifeSimulationState,
    )
except ImportError:
    build_life_simulation_state = None  # type: ignore
    attention_to_reply_limits = None  # type: ignore
    LifeSimulationState = None  # type: ignore

# ============================================================================
# CONFIGURATION
# ============================================================================

ANCHOR_YEAR = 2025
TIME_STEP_YEARS = 1  # Can be refined to 0.5 for ages < 6

AGE_BANDS = [
    {"label": "0-3", "start": 0, "end": 3},
    {"label": "3-7", "start": 3, "end": 7},
    {"label": "7-11", "start": 7, "end": 11},
    {"label": "11-14", "start": 11, "end": 14},
    {"label": "14-17", "start": 14, "end": 17},
    {"label": "17-24", "start": 17, "end": 24},
    {"label": "24-35", "start": 24, "end": 35},
    {"label": "35+", "start": 35, "end": float("inf")},
]

# Display-only fallbacks when EPR/GeoEPR or people_groups return no match (e.g. Ecuador).
# NOT from EPR/GeoEPR: no shares, no power. Power/SES for no-EPR countries come from
# sample_ethnic_group's hardcoded fallback (dominant, no power-based SES adjustment).
# See v2/IDENTITY_FALLBACK_AND_NO_EPR.md. Key: country_code (upper).
def _load_country_default_labels() -> tuple:
    try:
        import yaml
        from pathlib import Path as _P
        _p = _P(__file__).resolve().parent / "country_default_labels.yaml"
        with open(_p, encoding="utf-8") as _f:
            data = yaml.safe_load(_f) or {}
    except Exception:
        data = {}
    return data.get("countries") or {}, data.get("_fallback") or {"region": "", "ethnicity": "", "language": "", "religion": ""}

COUNTRY_DEFAULT_LABELS, _DEFAULT_LABEL_FALLBACK = _load_country_default_labels()


def _ensure_dict(val: Any) -> Dict[str, Any]:
    """Return val if it's a dict, else {}."""
    return val if isinstance(val, dict) else {}


def _civic_soul_for_sheet(world: Any) -> Dict[str, Any]:
    """Safe civic_soul dict from final_state.world; empty dict if world or civic_soul missing."""
    if world is None:
        return {}
    civ = getattr(world, "civic_soul", None)
    if civ is None:
        return {}
    return {k: v for k, v in civ.__dict__.items() if not k.startswith("_")}


def _symbols_for_sheet(symbols: Any) -> Dict[str, Any]:
    """Safe symbols dict; never empty salience (use placeholder if needed)."""
    if symbols is None:
        return {"salience": ["everyday_life"], "glosses": {}}
    sal = list(getattr(symbols, "salience", None) or [])
    gloss = dict(getattr(symbols, "glosses", None) or {})
    return {"salience": sal, "glosses": gloss}


def _thought_rails_for_sheet(tr: Any) -> Dict[str, Any]:
    """Thought rails dict with 'unknown' / empty replaced by '—' so no empty categories."""
    if tr is None:
        return {"authority_schema": "—", "fairness_schema": "—", "self_schema": "—", "other_groups_schema": {}}
    def _v(val: Any) -> str:
        if val is None:
            return "—"
        s = str(val).strip()
        return s if s and s.lower() != "unknown" else "—"
    other = getattr(tr, "other_groups_schema", None)
    if not isinstance(other, dict):
        other = {}
    return {
        "authority_schema": _v(getattr(tr, "authority_schema", None)),
        "fairness_schema": _v(getattr(tr, "fairness_schema", None)),
        "self_schema": _v(getattr(tr, "self_schema", None)),
        "other_groups_schema": other,
    }


def _ensure_life_snapshot_has_defaults(sheet: Dict[str, Any], id_filled: Dict[str, Any]) -> None:
    """Ensure life_snapshot has all expected keys with non-empty defaults when missing."""
    snap = sheet.get("life_snapshot")
    if not isinstance(snap, dict):
        snap = {}
    defaults = {
        "job_type": "other",
        "commute_style": "none",
        "living_arrangement": "with_family",
        "family_obligations": "light",
        "income_stress": "medium",
        "internet_access_patterns": "phone_only",
        "social_circle_density": "moderate",
        "sleep_debt_baseline": "light",
        "current_life_phase": "stable_routine_phase",
    }
    for k, v in defaults.items():
        if k not in snap or snap[k] is None or str(snap[k]).strip() == "":
            snap[k] = v
    sheet["life_snapshot"] = snap


def _band_default_key_event(band_label: str, country: str) -> str:
    """One placeholder key_event when a band has none (so category is never empty)."""
    if band_label == "0-3":
        return f"Early childhood in {country}"
    if band_label == "3-7":
        return f"Childhood in {country}"
    if band_label == "7-11":
        return f"School years in {country}"
    if band_label == "11-14":
        return f"Early adolescence in {country}"
    if band_label == "14-17":
        return f"Adolescence in {country}"
    if band_label == "17-24":
        return f"Young adulthood in {country}"
    if band_label == "24-35":
        return f"Adult life in {country}"
    return f"Life in {country}"


def _str_strip(val: Any, default: str = "") -> str:
    """Safely coerce to string and strip; use default if result empty."""
    if val is None:
        return default
    s = str(val).strip()
    return s if s else default


def _fill_persona_identity(identity: Any) -> Dict[str, Any]:
    """Build identity dict for persona sheet with empty/Unknown replaced by country-derived defaults."""
    if identity is None:
        return {
            "given_name": "Anonymous", "family_name": "", "country": "", "region": "", "urban_rural": "city",
            "ses_band": "middle", "minority_status": "dominant", "religion": "—", "gender": "male", "age": 35,
            "ethnicity": "—", "languages": ["—"],
        }
    code = _str_strip(getattr(identity, "country_code", None), "").upper() or ""
    defaults = COUNTRY_DEFAULT_LABELS.get(code) or _DEFAULT_LABEL_FALLBACK
    given = _str_strip(getattr(identity, "given_name", None), "")
    if not given or given == "Person":
        given = "Anonymous"
    family = _str_strip(getattr(identity, "family_name", None), "")
    region = _str_strip(getattr(identity, "region", None), "") or defaults.get("region", "")
    locality = _str_strip(getattr(identity, "locality", None), "")
    urban = _str_strip(getattr(identity, "urbanicity", None), "city")
    ses = _str_strip(getattr(identity, "current_class", None), "middle")
    minority = _str_strip(getattr(identity, "minority_status", None), "dominant")
    religion = _str_strip(getattr(identity, "current_religion", None), "")
    if not religion or religion == "Unknown":
        religion = defaults.get("religion", "—")
    gender = _str_strip(getattr(identity, "gender", None), "male")
    age = getattr(identity, "age_at_anchor", None)
    if age is None or (isinstance(age, (int, float)) and (age != age)):  # NaN check
        age = 35
    try:
        age = int(age)
    except (TypeError, ValueError):
        age = 35
    ethnicity = _str_strip(getattr(identity, "ethnicity_label", None), "")
    if not ethnicity or ethnicity == "Unknown":
        ethnicity = defaults.get("ethnicity", "—")
    primary_lang = _str_strip(getattr(identity, "primary_language", None), "")
    if not primary_lang or primary_lang == "Unknown":
        primary_lang = defaults.get("language", "—")
    secondary = list(getattr(identity, "secondary_languages", None) or [])
    secondary = [str(s).strip() for s in secondary if s is not None and str(s).strip() and str(s) != "Unknown"]
    if not secondary and primary_lang and primary_lang != "—":
        languages = [primary_lang]
    else:
        languages = [primary_lang] + secondary
    if not languages or languages == ["Unknown"]:
        languages = [primary_lang or "—"]
    return {
        "given_name": given,
        "family_name": family,
        "country": code or _str_strip(getattr(identity, "country_code", None), ""),
        "region": region,
        "locality": locality,
        "urban_rural": urban,
        "ses_band": ses,
        "minority_status": minority,
        "religion": religion,
        "gender": gender,
        "age": age,
        "ethnicity": ethnicity,
        "languages": languages,
    }

# Validation bounds
BOUNDS = {
    "needs": {"min": 0, "max": 100},
    "strategies": {"min": 0, "max": 100},
    "indices": {"min": 0, "max": 100},
    "continuity_max_delta": 10,  # Max change per year without event
}

# Data resampling windows
RESAMPLING = {
    "exact_year_priority": True,
    "nearest_neighbor_window": 5,  # ±5 years
    "era_profile_fallback": True,
}

# ============================================================================
# CORE DATA STRUCTURES
# ============================================================================


@dataclass
class IdentitySkeleton:
    """Static/slowly-changing identity facts"""
    internal_id: str
    given_name: str
    family_name: Optional[str] = None
    gender: Literal["male", "female", "nonbinary", "other"] = "male"
    birth_year: int = 0
    anchor_year: int = ANCHOR_YEAR
    age_at_anchor: int = 0
    
    # Place & origin
    country_code: str = ""
    region: str = ""
    locality: str = ""
    urbanicity: Literal["rural", "town", "city", "megacity"] = "rural"
    
    # Class / SES
    class_origin: Literal["underclass", "working", "lower_middle", "middle", "upper_middle", "elite"] = "working"
    current_class: Literal["underclass", "working", "lower_middle", "middle", "upper_middle", "elite"] = "working"
    
    # Ethnicity / group
    ethnicity_label: str = ""
    minority_status: Literal["dominant", "minoritized", "mixed", "unclear"] = "dominant"
    
    # Religion / worldview
    childhood_religion: str = ""
    current_religion: str = ""
    religiosity_level: float = 50.0  # 0-100
    
    # Language
    primary_language: str = ""
    secondary_languages: List[str] = field(default_factory=list)
    
    # Enneagram, MBTI, etc. (latent targets; not enforced)
    enneagram_type: Optional[int] = None
    enneagram_tritype: Optional[List[int]] = None
    mbti_code: Optional[str] = None
    
    # Notes for LLM / narrative layer
    identity_notes: str = ""


@dataclass
class ColonialHistory:
    """Colonial/independence context (from 01—reconfiguration.md)"""
    colonizer: Optional[str] = None  # Country code
    independence_year: Optional[int] = None
    major_regime_changes: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MigrationData:
    """Migration/urbanization context (from 01—reconfiguration.md)"""
    rural_to_urban_rate: Optional[float] = None  # Per-decade rate
    international_migration_prob: Optional[float] = None
    conflict_displacement: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CivicSoulConditions:
    """Weil-inspired civic atmosphere (macro environment)"""
    rootedness: float = 50.0
    perceived_justice_order: float = 50.0
    obligation_symmetry: float = 50.0
    rehabilitative_punishment_norms: float = 50.0
    hierarchy_legitimacy: float = 50.0
    shared_stake_in_common_goods: float = 50.0
    risk_band: float = 50.0  # 0 = deadened, 50 = healthy, 100 = terror


@dataclass
class WorldSlice:
    """Minimal per-age world snapshot"""
    year: int
    country_code: str
    gdp_per_capita: float = 50.0  # Normalized 0-100
    inequality_index: float = 50.0
    conflict_intensity: float = 0.0
    unemployment_level: float = 0.0
    media_saturation: float = 0.0
    propaganda_saturation: float = 0.0
    state_repression: float = 0.0
    welfare_support: float = 50.0
    # GDELT-derived (0-100): political/diplomatic texture
    policy_turbulence: float = 0.0   # demand+reject+threaten+disapprove; political pressure
    regime_instability: float = 0.0  # yield; concessions, regime change
    diplomatic_cooperation: float = 0.0  # cooperation+agree; aid, treaties
    military_posture: float = 0.0   # military buildup, saber-rattling
    diplomatic_isolation: float = 0.0  # reduce relations; pariah status
    # GDELT-derived (0-100): news/media environment
    media_valence: float = 50.0     # avg_tone mapped: 0=very negative, 100=very positive news
    scrutiny_level: float = 0.0     # n_investigate; accountability, transparency
    rhetoric_saturation: float = 0.0 # n_public_statement; state-in-news, propaganda proxy
    civic_soul: CivicSoulConditions = field(default_factory=CivicSoulConditions)
    colonial_history: Optional[ColonialHistory] = None
    migration_data: Optional[MigrationData] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NeedGradients:
    """Individual, lived need satisfactions (micro needs)"""
    safety: float = 50.0
    bodily_comfort: float = 50.0
    warmth_bonding: float = 50.0
    belonging_group: float = 50.0
    recognition_status: float = 50.0
    competence_effectiveness: float = 50.0
    autonomy_agency: float = 50.0
    coherence_meaning: float = 50.0
    play_pleasure: float = 50.0
    transcendence_sacred: float = 50.0


@dataclass
class StrategyPortfolio:
    """Coping repertoire (what person does when needs are strained)"""
    humor_play: float = 0.0
    aggression_outward: float = 0.0
    aggression_inward: float = 0.0
    compliance_obedience: float = 0.0
    people_pleasing: float = 0.0
    caretaking_rescue: float = 0.0
    achievement_striving: float = 0.0
    perfectionism_control: float = 0.0
    piety_ideology: float = 0.0
    intimacy_seeking: float = 0.0
    withdrawal_avoidance: float = 0.0
    dissociation_numbing: float = 0.0
    fantasy_immersion: float = 0.0
    substance_use: float = 0.0
    risk_seeking_thrill: float = 0.0
    activism_justice: float = 0.0
    creative_expression: float = 0.0
    extra: Dict[str, float] = field(default_factory=dict)


class RelationalRoleType(str, Enum):
    PRIMARY_CAREGIVER = "primary_caregiver"
    SECONDARY_CAREGIVER = "secondary_caregiver"
    SIBLING = "sibling"
    EXTENDED_FAMILY = "extended_family"
    PEER = "peer"
    ROMANTIC = "romantic"
    CHILD = "child"
    TEACHER = "teacher"
    EMPLOYER = "employer"
    RELIGIOUS_AUTHORITY = "religious_authority"
    STATE_AGENT = "state_agent"
    HEALTHCARE = "healthcare"
    INSTITUTIONAL_FIGURE = "institutional_figure"
    MEDIA_FIGURE = "media_figure"
    OTHER = "other"


@dataclass
class RelationalNode:
    """Single node in the relational graph"""
    node_id: str
    role: str  # "mother", "older_cousin", "imam", etc.
    role_type: RelationalRoleType
    centrality: float = 50.0  # 0-100
    cohabitation: bool = False
    warmth: float = 50.0
    harshness: float = 0.0
    reliability: float = 50.0
    authority: float = 50.0
    material_support: float = 0.0
    spiritual_support: float = 0.0
    alignment: Dict[str, float] = field(default_factory=dict)
    notes: str = ""
    enneagram_type: Optional[int] = None  # Inferred parent type (1–9) when role is caregiver


@dataclass
class RelationalGraph:
    """Full relational environment"""
    nodes: Dict[str, RelationalNode] = field(default_factory=dict)

    @property
    def caregiver_authority(self) -> float:
        """Mean authority of primary/secondary caregivers."""
        caregivers = [
            n for n in self.nodes.values()
            if n.role_type in (RelationalRoleType.PRIMARY_CAREGIVER, RelationalRoleType.SECONDARY_CAREGIVER)
        ]
        return float(np.mean([c.authority for c in caregivers])) if caregivers else 50.0

    @property
    def caregiver_harshness(self) -> float:
        """Mean harshness of primary/secondary caregivers."""
        caregivers = [
            n for n in self.nodes.values()
            if n.role_type in (RelationalRoleType.PRIMARY_CAREGIVER, RelationalRoleType.SECONDARY_CAREGIVER)
        ]
        return float(np.mean([c.harshness for c in caregivers])) if caregivers else 0.0

    @property
    def has_dependents(self) -> bool:
        """Whether persona has dependents (children, etc.)."""
        return any(
            n.role_type == RelationalRoleType.CHILD
            for n in self.nodes.values()
        )

    @property
    def peer_pressure(self) -> float:
        """Proxy for peer influence (centrality of peers)."""
        peers = [n for n in self.nodes.values() if n.role_type == RelationalRoleType.PEER]
        return float(np.mean([p.centrality for p in peers])) if peers else 50.0

    @property
    def caregiver_expectations(self) -> float:
        """Proxy for caregiver expectations (authority + reliability)."""
        caregivers = [
            n for n in self.nodes.values()
            if n.role_type in (RelationalRoleType.PRIMARY_CAREGIVER, RelationalRoleType.SECONDARY_CAREGIVER)
        ]
        if not caregivers:
            return 50.0
        return float(np.mean([(c.authority + c.reliability) / 2 for c in caregivers]))

    @property
    def repeated_rejection(self) -> bool:
        """Proxy: low peer warmth suggests repeated rejection."""
        peers = [n for n in self.nodes.values() if n.role_type == RelationalRoleType.PEER]
        if not peers:
            return False
        return float(np.mean([p.warmth for p in peers])) < 30

    @property
    def caregiver_warmth(self) -> float:
        """Mean warmth of caregivers (for needs)."""
        caregivers = [
            n for n in self.nodes.values()
            if n.role_type in (RelationalRoleType.PRIMARY_CAREGIVER, RelationalRoleType.SECONDARY_CAREGIVER)
        ]
        return float(np.mean([c.warmth for c in caregivers])) if caregivers else 50.0

    @property
    def peer_warmth(self) -> float:
        """Mean warmth of peers. Default 50 when no peers (neutral)."""
        peers = [n for n in self.nodes.values() if n.role_type == RelationalRoleType.PEER]
        if not peers:
            return 50.0
        return float(np.mean([p.warmth for p in peers]))

    @property
    def institution_alignment(self) -> float:
        """Proxy for alignment with institutions. When no institutions, derive from caregivers (family)."""
        institutions = [n for n in self.nodes.values() if n.role_type == RelationalRoleType.INSTITUTIONAL_FIGURE]
        if institutions:
            return float(np.mean([i.alignment.get("institution", 50) for i in institutions if hasattr(i, "alignment")]))
        # No institutions modeled: family (caregivers) provides baseline belonging
        caregivers = [
            n for n in self.nodes.values()
            if n.role_type in (RelationalRoleType.PRIMARY_CAREGIVER, RelationalRoleType.SECONDARY_CAREGIVER)
        ]
        if caregivers:
            return float(np.mean([c.warmth for c in caregivers]))  # Family warmth → family belonging
        return 50.0


@dataclass
class RelationalMicrograph:
    """Relational environment summary for a band (from 05—implementation.md)"""
    caregivers: List[RelationalNode] = field(default_factory=list)
    peers: List[RelationalNode] = field(default_factory=list)
    institutions: List[RelationalNode] = field(default_factory=list)
    key_events: List[str] = field(default_factory=list)
    norm_conflicts: List[str] = field(default_factory=list)


@dataclass
class SymbolicState:
    """What symbols mean to this person (symbolic lexicon)"""
    salience: Dict[str, float] = field(default_factory=dict)
    glosses: Dict[str, str] = field(default_factory=dict)


@dataclass
class ThoughtRails:
    """Core schemas along which persona's thinking runs"""
    authority_schema: str = "unknown"
    fairness_schema: str = "unknown"
    self_schema: str = "unknown"
    other_groups_schema: Dict[str, str] = field(default_factory=dict)
    threat_schema: Optional[str] = None
    hope_schema: Optional[str] = None
    tags: Dict[str, float] = field(default_factory=dict)


@dataclass
class CognitiveProfile:
    """How fast/deeply new ideas can move the rails"""
    inertia: float = 50.0  # 0 = flippable, 100 = extremely stable
    elasticity: float = 50.0  # 0 = rigid, 100 = high capacity to bend/adapt
    compartmentalization: float = 30.0
    suggestibility: float = 50.0
    openness_to_contradiction: float = 50.0
    primary_defense: Literal["denial", "splitting", "rationalization", "projection", "humor", "isolation", "intellectualization"] = "rationalization"
    secondary_defense: Optional[str] = None
    analytic_style: Literal["low", "medium", "high"] = "medium"


@dataclass
class Indices:
    """High-level composite indices (meta-tension gauges)"""
    permeability_index: float = 0.0
    drts: float = 0.0  # Defiance / Revolutionary Tendencies System
    iai: float = 0.0  # Ideological Architecture Index
    transgression_threshold: float = 50.0
    aesthetic_amplification: float = 0.0
    recursive_madness_threshold: float = 0.0


@dataclass
class IdeaDelta:
    """Representation of a new idea/framework that hits the persona"""
    idea_id: str
    description: str
    source_trust: float = 50.0  # 0-100
    target_axes: Dict[str, float] = field(default_factory=dict)
    affect_valence: float = 0.0  # -100 to 100
    affect_arousal: float = 50.0  # 0-100


@dataclass
class IdeaDigest:
    """How an idea was absorbed by the persona"""
    last_idea: Optional[IdeaDelta] = None
    recent_ideas: List[IdeaDelta] = field(default_factory=list)
    immediate_affect_label: Optional[str] = None
    defense_used: Optional[str] = None
    applied_deltas: Dict[str, float] = field(default_factory=dict)
    integration_status: Literal["rejected", "compartmentalized", "provisional", "integrated", "overwhelming"] = "provisional"
    unresolved_tensions: Dict[str, str] = field(default_factory=dict)
    notes: str = ""


# Riso/Hudson: Unconscious & Lost Messages (from PARENT_CHILD_TYPE_SCHEMA Section 9)
UNCONSCIOUS_MESSAGES: Dict[int, str] = {
    1: "It's not okay to make mistakes.",
    2: "It's not okay to have your own needs.",
    3: "It's not okay to have your own feelings and identity.",
    4: "It's not okay to be too functional or too happy.",
    5: "It's not okay to be comfortable in the world.",
    6: "It's not okay to trust yourself.",
    7: "It's not okay to depend on anyone for anything.",
    8: "It's not okay to be vulnerable or to trust anyone.",
    9: "It's not okay to assert yourself.",
}
LOST_MESSAGES: Dict[int, str] = {
    1: "You are good.",
    2: "You are wanted.",
    3: "You are loved for yourself.",
    4: "You are seen for who you are.",
    5: "Your needs are not a problem.",
    6: "You are safe.",
    7: "You will be taken care of.",
    8: "You will not be betrayed.",
    9: "Your presence matters.",
}

# Rawlsing v4.0 stage guidance (from Rawlsing_Personality_Generator_Framework_v4.0.md)
# Used by build_recursion_prompt to steer tangible detail generation per age band.
RAWLSING_STAGE_GUIDANCE: Dict[str, str] = {
    "0-3": (
        "Temperament: reactive vs calm; expressive vs withdrawn; sensory sensitivity; baseline trust/distrust. "
        "Primary caregiver dynamics: warmth, inconsistency, absence, harshness, over-protection, illness, addiction, chronic stress. "
        "Micro-patterns: bodily/behavioral quirks (ear-rubbing, freezing at loud voices, rocking). "
        "Early atmosphere: sounds, smells, emotional climate (radio, factory noise, lullabies, arguments). "
        "PI modifier: early contact with non-household idioms, gestures, media (migrant uncle, foreign TV, tourist presence)."
    ),
    "3-7": (
        "Play style and social temperament: solitary vs collective; rough vs cautious; lead/observe/submit. "
        "First symbols: objects or images with emotional charge (cracked amulet, painted gourd, broken toy, religious icon). "
        "Relationship to rules and power: quiet compliance, covert defiance, rule-bending, tattling, secret hoarding, moralizing. "
        "Kinship and authority: grandparent stories, teacher presence/absence, intra-family conflict, praising vs shaming styles. "
        "PI modifier: core symbols contested or supplemented by outside inputs (TV vs local myths; missionary school vs ancestral stories)."
    ),
    "7-11": (
        "Inner monologue emergence: proto-scripts ('I fix things', 'I watch and remember', 'I am the trouble'). "
        "Fairness and shame logic: who is allowed to be unfair; what counts as humiliation; justified retaliation. "
        "Habits and self-regulation: rituals to calm or prepare (tracing spirals, muttering phrases, touching objects). "
        "Moral atmosphere: ancestral, divine, ideological ('The river sees everything', 'The martyrs watch us', 'Neighbors talk'). "
        "PI modifier: cognitive dissonance potential—conflicting norms (secular school vs religious home); suppress, compartmentalize, or experiment."
    ),
    "11-14": (
        "Exposure to organized meaning systems: political slogans, religious instruction, street gossip, nationalist myth, online influencers. "
        "Identity kernel: emerging 'I am the one who…' statements (ambiguous, may conflict across contexts). "
        "Quirk adaptation: early bodily quirks re-coded (fidgeting→toughness; mimicry→subversive humor). "
        "Role in peer and family systems: scapegoat, negotiator, ghost, golden child, clown, confidant, enforcer. "
        "PI modifier: dual-coding—cross-pollination (TikTok and sacred text; protest memes and ancestor talk); guilt, exhilaration, cynicism, or synthesis."
    ),
    "14-17": (
        "Desires: concrete (motorbike, no one to answer to) not abstract (happiness). "
        "Persona strategies: how they present (tough, harmless, invisible, comic, pious, cynical, responsible, seductive, dutiful). "
        "Defense patterns: denial, sarcasm, aggression, pleasing, dissociation, moralizing, strategic compliance. "
        "'I am the one who…' patterns: short internally voiced script; allow conflict with actual behavior. "
        "PI modifier: conflicting selves (devout at home, mocking online); hypocrisy, necessity, or normal."
    ),
    "17+": (
        "Key experiences: love, breakups, childbirth, unemployment, migration, state violence, illness, political upheaval, war, tech shocks. "
        "Ideological movement: belief hardening, disillusionment, conversion, radicalization, retreat, opportunism, pragmatic compromise. "
        "Symbolic reinterpretation: early symbols reappear in new roles (shell at 4→talisman of regret at 40; chant→protest song). "
        "Moral fatigue and repair attempts: rationalizations, renewed commitments, strategic withdrawal from risk. "
        "PI modifier: radical alternatives—collapse, assimilation, or hybrid identities with unresolved conflict."
    ),
}

# PI interpretation (0-100 scalar from Rawlsing Section 3)
PI_INTERPRETATION: Dict[str, Tuple[float, float, str]] = {
    "closed": (0, 20, "Symbolically closed. Local world all-encompassing. Outside systems distant rumor or invisible."),
    "limited": (20, 40, "Limited exposure. Strong local anchors; outside symbols present but peripheral."),
    "mixed": (40, 60, "Mixed exposure. Regular contact with external ideas/media; significant dissonance or hybridization potential."),
    "high": (60, 80, "High exposure. Multiple conflicting inputs; dual or triple coding common."),
    "extreme": (80, 100, "Extreme exposure. Cross-cut by several networks (diaspora, online subcultures). Dislocation, synthesis, or fragmentation risk."),
}


@dataclass
class EnneagramProfile:
    """Derived from life-course, not assigned at birth"""
    primary_type: int  # 1-9
    wing: Optional[int] = None
    stack: Dict[int, float] = field(default_factory=dict)  # type -> probability
    health_level: float = 50.0  # 0-100
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EnneagramCandidates:
    """Type candidates during inference phase (ages 0-6), before crystallization at 6-7."""
    probabilities: Dict[int, float]  # type -> probability
    raw_scores: Optional[Dict[int, float]] = None  # for audit


@dataclass
class EnneagramLatentVector:
    """Temperament sampled once at birth (from 05—implementation.md)"""
    reactivity: float = 50.0
    idealism: float = 50.0
    shame_vs_fear_vs_anger: float = 50.0  # low=shame, mid=fear, high=anger
    uniqueness_vs_safety: float = 50.0
    extra: Dict[str, float] = field(default_factory=dict)


@dataclass
class PersonaState:
    """Complete state vector at a point in time"""
    identity: IdentitySkeleton
    age: int
    current_year: int
    band: str
    world: WorldSlice
    needs: NeedGradients
    strategies: StrategyPortfolio
    relations: RelationalGraph
    micrograph: Optional[RelationalMicrograph] = None
    symbols: SymbolicState = field(default_factory=SymbolicState)
    thought_rails: ThoughtRails = field(default_factory=ThoughtRails)
    cognitive: CognitiveProfile = field(default_factory=CognitiveProfile)
    indices: Indices = field(default_factory=Indices)
    enneagram: Optional[EnneagramProfile] = None
    enneagram_candidates: Optional[EnneagramCandidates] = None  # ages 0-6 only; crystallizes at 7
    temperament: Optional[EnneagramLatentVector] = None
    idea_digest: IdeaDigest = field(default_factory=IdeaDigest)
    narrative_snapshot: str = ""
    palimpsest: Optional['Palimpsest'] = None  # v4.2: accumulated layers, never overwritten
    driver_vec: Optional['DriverVector'] = None  # Cultural-psychic field at birth (broader context)
    father_driver_vec: Optional['DriverVector'] = None  # Father cohort WVS (distinct parent)
    mother_driver_vec: Optional['DriverVector'] = None  # Mother cohort WVS (distinct parent)
    father_type: Optional[int] = None  # Inferred father Enneagram type (1–9)
    mother_type: Optional[int] = None  # Inferred mother Enneagram type (1–9)


@dataclass
class PersonaHistory:
    """Complete life-course history"""
    identity: IdentitySkeleton
    yearly_states: List[PersonaState]
    band_summaries: List[PersonaState]
    idea_history: List[IdeaDigest]
    enneagram_profile: Optional[EnneagramProfile] = None
    palimpsest: Optional['Palimpsest'] = None  # v4.2: full accumulated layers
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CohortAdjusters:
    """Modulates sampling of birth contexts"""
    global_south_only: bool = False
    reduce_india_china: float = 0.0  # 0-1 fraction
    minority_only: bool = False
    rural_bias: float = 0.0  # positive => bias toward rural
    manual_country_weights: Optional[Dict[str, float]] = None


@dataclass
class PersonaConstraints:
    """Hard or soft constraints on end state at ANCHOR_YEAR"""
    target_country: Optional[str] = None
    target_region: Optional[str] = None
    target_city: Optional[str] = None
    target_ethnicity: Optional[str] = None
    target_religion: Optional[str] = None
    target_gender: Optional[str] = None
    target_ses_band: Optional[Literal["low", "middle", "high"]] = None


@dataclass
class DriverVector:
    """Value/driver cube output (WVS/Afrobarometer aggregated)"""
    trust_vs_distrust: float = 50.0
    religiosity: float = 50.0
    ritual_centrality: float = 50.0
    authoritarian_vs_egalitarian: float = 50.0
    individualism_vs_collectivism: float = 50.0
    fatalism_vs_agency: float = 50.0
    meritocracy_belief: Optional[float] = None
    family_importance: Optional[float] = None
    is_default_fallback: bool = False
    extra: Dict[str, float] = field(default_factory=dict)


@dataclass
class LocalModifiers:
    """Ethnic-power, religion, urban/rural, class modifiers"""
    ethnic_power_status: Literal["dominant", "minoritized", "mixed", "unclear"] = "dominant"
    epr_power_status: Optional[str] = None  # Raw EPR: MONOPOLY, DOMINANT, POWERLESS, etc.
    religion_status: Literal["majority", "minority"] = "majority"
    urban_rural: Literal["urban", "rural", "peri_urban"] = "rural"
    class_position: int = 5  # 1-10 SES decile


@dataclass
class LifeEvent:
    """Domain-specific event in a life band"""
    event_id: str
    age: int
    type: str  # "migration", "loss", "illness", "conversion", "organizing", etc.
    description: str
    subtype: str = ""  # e.g. "death_of_caregiver", "religious_conversion"
    metadata: Dict[str, Any] = field(default_factory=dict)
    effects: Dict[str, Dict[str, float]] = field(default_factory=dict)  # needs, strategies, indices deltas


@dataclass
class AgeBand:
    """Age band with associated events"""
    start_age: int
    end_age: int  # Inclusive end
    events: List[LifeEvent] = field(default_factory=list)

# ============================================================================
# VALIDATION UTILITIES
# ============================================================================


def clamp(value: float, min_val: float = 0.0, max_val: float = 100.0) -> float:
    """Clamp a value to bounds"""
    return max(min_val, min(max_val, value))


def validate_persona_state(state: PersonaState) -> Tuple[bool, List[str]]:
    """Validate PersonaState bounds and consistency"""
    errors = []
    
    # Validate needs
    for key, value in state.needs.__dict__.items():
        if not isinstance(value, (int, float)) or value < 0 or value > 100:
            errors.append(f"Need '{key}' out of bounds: {value}")
    
    # Validate strategies
    for key, value in state.strategies.__dict__.items():
        if key == "extra":
            continue
        if not isinstance(value, (int, float)) or value < 0 or value > 100:
            errors.append(f"Strategy '{key}' out of bounds: {value}")
    
    # Validate indices
    for key, value in state.indices.__dict__.items():
        if not isinstance(value, (int, float)) or value < 0 or value > 100:
            errors.append(f"Index '{key}' out of bounds: {value}")
    
    # Structural plausibility checks
    if state.strategies.piety_ideology > 70 and state.needs.transcendence_sacred < 30:
        errors.append("High piety_ideology but low transcendence_sacred is implausible")
    
    return len(errors) == 0, errors


def validate_continuity(
    prev_state: PersonaState,
    next_state: PersonaState,
    events: List[LifeEvent] = None
) -> Tuple[bool, List[str]]:
    """Check continuity between two states (no sudden jumps without events)"""
    if events is None:
        events = []
    
    violations = []
    max_delta = BOUNDS["continuity_max_delta"]
    has_major_event = any(
        e.type in ["migration", "loss", "illness", "conversion", "organizing"]
        for e in events
    )
    
    # Check needs continuity
    for key in prev_state.needs.__dict__.keys():
        if key.startswith("_"):
            continue
        delta = abs(getattr(next_state.needs, key) - getattr(prev_state.needs, key))
        if delta > max_delta and not has_major_event:
            violations.append(f"Need '{key}' changed by {delta} without major event")
    
    # Check strategies continuity (slightly more flexible)
    for key in prev_state.strategies.__dict__.keys():
        if key in ["extra", "_"] or key.startswith("_"):
            continue
        delta = abs(getattr(next_state.strategies, key) - getattr(prev_state.strategies, key))
        if delta > max_delta * 1.5 and not has_major_event:
            violations.append(f"Strategy '{key}' changed by {delta} without major event")
    
    return len(violations) == 0, violations

# ============================================================================
# UPDATE FUNCTION CONTRACTS
# ============================================================================

def _compute_strategy_satisfaction(
    need_name: str,
    strategies: StrategyPortfolio,
    need_config: Dict,
    loader
) -> float:
    """
    Compute how much strategies satisfy a given need.
    This creates realistic feedback loops where strategies help but don't fully solve problems.
    """
    # Get which strategies typically help with this need
    typical_consequences = need_config.get("typical_consequences_when_low", [])
    
    satisfaction = 0.0
    for strategy_name in typical_consequences:
        # Map strategy names (may have underscores or different formats)
        strategy_value = 0.0
        # Try direct attribute access
        if hasattr(strategies, strategy_name):
            strategy_value = getattr(strategies, strategy_name, 0.0)
        else:
            # Try with underscores
            strategy_name_alt = strategy_name.replace("-", "_")
            if hasattr(strategies, strategy_name_alt):
                strategy_value = getattr(strategies, strategy_name_alt, 0.0)
        
        # Strategies provide diminishing returns satisfaction
        # Higher strategy use → more satisfaction, but with diminishing returns
        if strategy_value > 0:
            # Diminishing returns: sqrt(strategy_value / 100) * 10
            # So 100 strategy use → 10 points satisfaction, 25 strategy use → 5 points
            satisfaction += np.sqrt(strategy_value / 100.0) * 10.0
    
    return min(satisfaction, 30.0)  # Cap at 30% boost from strategies


def _compute_index_modulation(
    need_name: str,
    indices: Indices,
    need_config: Dict
) -> float:
    """
    Compute how indices modulate need responses.
    Returns a multiplier (e.g., 0.1 = 10% increase, -0.1 = 10% decrease).
    """
    modulation = 0.0
    
    # High RMT (recursive madness threshold) → needs more volatile
    if indices.recursive_madness_threshold > 50:
        # Needs become more sensitive to stressors
        if need_name in ["safety", "warmth_bonding", "belonging_group"]:
            modulation += (indices.recursive_madness_threshold - 50) / 100.0 * 0.1
    
    # Low transgression threshold → safety needs more important
    if indices.transgression_threshold < 40:
        if need_name == "safety":
            modulation += (40 - indices.transgression_threshold) / 100.0 * 0.15
    
    # High DRTS → belonging/recognition needs more important
    if indices.drts > 50:
        if need_name in ["belonging_group", "recognition_status"]:
            modulation += (indices.drts - 50) / 100.0 * 0.1
    
    return modulation


def _compute_cross_need_compensation(
    need_name: str,
    prev_needs: NeedGradients,
    loader,
    enneagram_type: Optional[int] = None,
    age: int = 0,
    early_childhood_states: Optional[List] = None
) -> float:
    """
    Compute cross-need compensation: when one need is chronically unmet,
    other needs may increase to compensate (psychological defense mechanism).
    
    ENNEAGRAM-AWARE & EARLY CHILDHOOD IMPRINT-AWARE:
    - Compensation patterns align with Enneagram principles
    - Early childhood (ages 0-7) is the IMPRINT PERIOD - most formative
    - Unmet needs during early childhood create stronger, more lasting compensation
    - Uses early_childhood_pattern from wisdom system to guide compensation during imprint
    - Compensation is stronger during early childhood (creates the "imprint")
    
    According to Enneagram theory:
    - Ages 0-7: The "imprint" period when core fear and defense mechanism develop
    - Patterns established here are more "sticky" and lasting
    - Early unmet needs create stronger compensatory patterns
    
    Returns compensation effect (positive or negative points to add to need).
    """
    compensation = 0.0
    
    # Get need value
    need_value = getattr(prev_needs, need_name, 50.0)
    
    # Only apply compensation if this need is currently met (above neutral)
    # and other needs are unmet (below neutral)
    if need_value < 50.0:
        return 0.0  # Don't compensate unmet needs with other unmet needs
    
    # Import Enneagram wisdom if available
    try:
        from .enneagram_wisdom import build_enneagram_wisdom_base
    except ImportError:
        from enneagram_wisdom import build_enneagram_wisdom_base
    
    wisdom_base = build_enneagram_wisdom_base()
    
    # ENHANCED: Early childhood imprint weighting
    # Early childhood (ages 0-7) is the imprint period - compensation is stronger and more formative
    is_early_childhood = age <= 7
    early_childhood_multiplier = 1.5 if is_early_childhood else 1.0  # 50% stronger during imprint
    
    # ENHANCED: Use early childhood states to compute average unmet needs during imprint
    early_unmet_needs = {}
    if early_childhood_states and len(early_childhood_states) > 0:
        # Compute average unmet needs during early childhood (the imprint period)
        for state in early_childhood_states:
            for need_field in loader.get_all_needs():
                need_val = getattr(state.needs, need_field, 50.0)
                if need_val < 50.0:  # Unmet
                    if need_field not in early_unmet_needs:
                        early_unmet_needs[need_field] = []
                    early_unmet_needs[need_field].append(need_val)
        
        # Average the unmet needs
        for need_field in early_unmet_needs:
            early_unmet_needs[need_field] = np.mean(early_unmet_needs[need_field])
    
    # If we know the Enneagram type, use type-specific compensation patterns
    if enneagram_type and enneagram_type in wisdom_base:
        type_wisdom = wisdom_base[enneagram_type]
        
        # ENHANCED: Check early_childhood_pattern for this type
        # If we're in early childhood, use the pattern to guide compensation
        if is_early_childhood and type_wisdom.early_childhood_pattern:
            # Check if this need appears in early childhood pattern (overcompensated early)
            early_pattern_key = f"needs.{need_name}"
            if early_pattern_key in type_wisdom.early_childhood_pattern:
                # This need is part of the early imprint pattern
                # Check for unmet needs that trigger this compensation
                for unmet_need in type_wisdom.unmet_needs:
                    # Use early childhood average if available, otherwise current value
                    if unmet_need in early_unmet_needs:
                        unmet_value = early_unmet_needs[unmet_need]
                    else:
                        unmet_value = getattr(prev_needs, unmet_need, 50.0)
                    
                    if unmet_value < 40.0:  # Significantly unmet
                        deficit = 40.0 - unmet_value
                        # Early childhood compensation is stronger (creates imprint)
                        compensation += deficit * 0.25 * early_childhood_multiplier  # Up to 10 points during imprint
                        break
        
        # Check if this need is in the type's overcompensated_needs
        if need_name in type_wisdom.overcompensated_needs:
            # This type overcompensates in this dimension
            # Check for unmet needs that trigger this compensation
            for unmet_need in type_wisdom.unmet_needs:
                # Use early childhood average if available (more formative)
                if unmet_need in early_unmet_needs:
                    unmet_value = early_unmet_needs[unmet_need]
                    # Early childhood unmet needs create stronger compensation
                    if unmet_value < 40.0:
                        deficit = 40.0 - unmet_value
                        compensation += deficit * 0.25 * early_childhood_multiplier  # Stronger during imprint
                        break
                else:
                    # Use current value
                    unmet_value = getattr(prev_needs, unmet_need, 50.0)
                    if unmet_value < 40.0:  # Significantly unmet
                        deficit = 40.0 - unmet_value
                        # Type-specific compensation (stronger for overcompensated needs)
                        compensation += deficit * 0.20 * early_childhood_multiplier  # Up to 8 points
                        break  # Use first unmet need
    
    # General Enneagram-aligned compensation patterns (when type unknown or as fallback)
    # These patterns align with common Enneagram overcompensation patterns
    
    # Type 1 pattern: Low warmth/play → overcompensate with coherence/safety
    if need_name == "coherence_meaning":
        warmth_value = getattr(prev_needs, "warmth_bonding", 50.0)
        play_value = getattr(prev_needs, "play_pleasure", 50.0)
        if warmth_value < 40.0 or play_value < 40.0:
            deficit = max(40.0 - warmth_value, 40.0 - play_value, 0)
            compensation += deficit * 0.12  # Up to 4.8 points
    
    if need_name == "safety":
        warmth_value = getattr(prev_needs, "warmth_bonding", 50.0)
        if warmth_value < 40.0:
            deficit = 40.0 - warmth_value
            compensation += deficit * 0.10  # Up to 4 points
    
    # Type 2 pattern: Low warmth → overcompensate with recognition
    if need_name == "recognition_status":
        warmth_value = getattr(prev_needs, "warmth_bonding", 50.0)
        if warmth_value < 40.0:
            deficit = 40.0 - warmth_value
            compensation += deficit * 0.15  # Up to 6 points
    
    # Type 3 pattern: Low recognition → overcompensate with recognition/competence
    # (Already handled above, but also check warmth/coherence)
    if need_name == "competence_effectiveness":
        recognition_value = getattr(prev_needs, "recognition_status", 50.0)
        coherence_value = getattr(prev_needs, "coherence_meaning", 50.0)
        if recognition_value < 40.0 or coherence_value < 40.0:
            deficit = max(40.0 - recognition_value, 40.0 - coherence_value, 0)
            compensation += deficit * 0.12  # Up to 4.8 points
    
    # Type 4 pattern: Low belonging/recognition → overcompensate with transcendence/coherence
    if need_name == "transcendence_sacred":
        belonging_value = getattr(prev_needs, "belonging_group", 50.0)
        recognition_value = getattr(prev_needs, "recognition_status", 50.0)
        if belonging_value < 40.0 or recognition_value < 40.0:
            deficit = max(40.0 - belonging_value, 40.0 - recognition_value, 0)
            compensation += deficit * 0.12  # Up to 4.8 points
    
    if need_name == "coherence_meaning":
        belonging_value = getattr(prev_needs, "belonging_group", 50.0)
        if belonging_value < 40.0:
            deficit = 40.0 - belonging_value
            compensation += deficit * 0.10  # Up to 4 points
    
    # Type 5 pattern: Low warmth/belonging → overcompensate with competence
    if need_name == "competence_effectiveness":
        warmth_value = getattr(prev_needs, "warmth_bonding", 50.0)
        belonging_value = getattr(prev_needs, "belonging_group", 50.0)
        if warmth_value < 40.0 or belonging_value < 40.0:
            deficit = max(40.0 - warmth_value, 40.0 - belonging_value, 0)
            compensation += deficit * 0.12  # Up to 4.8 points
    
    # Type 6 pattern: Low safety/autonomy → overcompensate with belonging
    if need_name == "belonging_group":
        safety_value = getattr(prev_needs, "safety", 50.0)
        autonomy_value = getattr(prev_needs, "autonomy_agency", 50.0)
        if safety_value < 40.0 or autonomy_value < 40.0:
            deficit = max(40.0 - safety_value, 40.0 - autonomy_value, 0)
            compensation += deficit * 0.15  # Up to 6 points
    
    # Type 7 pattern: Low coherence/transcendence → overcompensate with play
    if need_name == "play_pleasure":
        coherence_value = getattr(prev_needs, "coherence_meaning", 50.0)
        transcendence_value = getattr(prev_needs, "transcendence_sacred", 50.0)
        if coherence_value < 40.0 or transcendence_value < 40.0:
            deficit = max(40.0 - coherence_value, 40.0 - transcendence_value, 0)
            compensation += deficit * 0.15  # Up to 6 points
    
    # Type 8 pattern: Low warmth/safety → overcompensate with autonomy/recognition
    if need_name == "autonomy_agency":
        warmth_value = getattr(prev_needs, "warmth_bonding", 50.0)
        safety_value = getattr(prev_needs, "safety", 50.0)
        if warmth_value < 40.0 or safety_value < 40.0:
            deficit = max(40.0 - warmth_value, 40.0 - safety_value, 0)
            compensation += deficit * 0.15  # Up to 6 points
    
    if need_name == "recognition_status":
        autonomy_value = getattr(prev_needs, "autonomy_agency", 50.0)
        if autonomy_value < 40.0:
            deficit = 40.0 - autonomy_value
            compensation += deficit * 0.12  # Up to 4.8 points
    
    # Type 9 pattern: Low autonomy/recognition → overcompensate with belonging
    if need_name == "belonging_group":
        autonomy_value = getattr(prev_needs, "autonomy_agency", 50.0)
        recognition_value = getattr(prev_needs, "recognition_status", 50.0)
        if autonomy_value < 40.0 or recognition_value < 40.0:
            deficit = max(40.0 - autonomy_value, 40.0 - recognition_value, 0)
            compensation += deficit * 0.15  # Up to 6 points
    
    # Cap compensation to prevent unrealistic overcompensation
    return min(compensation, 8.0)  # Max 8 points compensation


def _apply_cross_need_interactions(
    updated_dict: Dict[str, float],
    prev_needs: NeedGradients,
    interactions: Dict,
    loader,
    context: Dict
) -> Dict[str, float]:
    """
    Apply cross-need interactions from config (e.g., low_warmth_high_belonging).
    These are pattern-based interactions that create complex psychological dynamics.
    """
    result = updated_dict.copy()
    
    for interaction_name, interaction_config in interactions.items():
        # Check if interaction condition is met
        condition = interaction_config.get("condition", "")
        if not condition:
            # Try to infer condition from interaction name
            # e.g., "low_warmth_high_belonging" → check warmth < 50 and belonging > 50
            if "low_" in interaction_name and "high_" in interaction_name:
                parts = interaction_name.split("_")
                # Simple heuristic: look for need names in interaction name
                # This is a fallback - ideally conditions should be explicit
                continue
        
        # Evaluate condition if provided
        if condition:
            try:
                if not loader.evaluate_condition(condition, context):
                    continue
            except (AttributeError, KeyError, TypeError):
                continue
        
        # Apply effects
        for key, effect_value in interaction_config.items():
            if key.startswith("effect_on_"):
                target_need = key.replace("effect_on_", "")
                if target_need in result:
                    # effect_value is a multiplier (e.g., -0.1 = 10% decrease)
                    # Apply to the deficit/surplus from neutral
                    current_value = result[target_need]
                    deviation = current_value - 50.0
                    adjustment = deviation * effect_value
                    result[target_need] = clamp(current_value + adjustment)
    
    return result


def update_needs(
    prev_needs: NeedGradients,
    civic_soul: CivicSoulConditions,
    relations: RelationalGraph,
    strategies: StrategyPortfolio,
    world: WorldSlice,
    indices: Indices = None,
    persona_state: Optional[PersonaState] = None,
    age: int = 0,
    early_childhood_states: Optional[List[PersonaState]] = None
) -> NeedGradients:
    """
    Update needs based on civic soul, relations, strategies, and world.
    Uses config/needs.yaml to drive the update logic.
    
    ENHANCED: Now includes:
    - Strategy feedback - strategies partially satisfy needs
    - Enneagram-aware compensation - aligned with type-specific patterns
    - Early childhood imprint weighting - ages 0-7 are most formative (Enneagram theory)
    
    According to Enneagram theory, early childhood (ages 0-7) is the "imprint" period
    when core fears and defense mechanisms develop. Compensation patterns established
    during this period are more lasting and formative.
    """
    loader = get_config_loader()
    context = {
        "world_slice": world,
        "civic_soul": civic_soul,
        "needs": prev_needs,
        "strategies": strategies,
        "relations": relations,
        "age": age,  # Pass age for imprint-aware compensation
    }
    if indices:
        context["indices"] = indices
    if persona_state:
        context["persona_state"] = persona_state
        # Try to get Enneagram type from state if available
        if hasattr(persona_state, "enneagram") and persona_state.enneagram:
            context["enneagram_type"] = persona_state.enneagram.primary_type
    if early_childhood_states:
        context["early_childhood_states"] = early_childhood_states  # For imprint-aware compensation
    
    # Compute average caregiver warmth (used by multiple needs)
    caregivers = [
        node for node in relations.nodes.values()
        if node.role_type in [RelationalRoleType.PRIMARY_CAREGIVER, RelationalRoleType.SECONDARY_CAREGIVER]
    ]
    avg_caregiver_warmth = np.mean([c.warmth for c in caregivers]) if caregivers else 50.0
    context["avg_caregiver_warmth"] = avg_caregiver_warmth
    
    # Update each need using config
    updated_dict = {}
    all_needs = loader.get_all_needs()
    
    for need_name in all_needs:
        need_config = loader.get_needs_config(need_name)
        formula_config = need_config.get("update_formula", {})
        
        # Get current value
        prev_value = getattr(prev_needs, need_name, 50.0)
        
        # Base weight from config
        base_weight = formula_config.get("base_weight", 0.7)
        new_value = prev_value * base_weight
        
        # Apply contributions from config
        # Check all contribution keys in formula_config
        for key, weight in formula_config.items():
            if key == "base_weight":
                continue
            
            if key.endswith("_contribution"):
                # Extract the input name from contribution key
                # e.g., "caregiver_warmth_contribution" -> "caregiver_warmth"
                input_name = key.replace("_contribution", "")
                
                # Try to find matching input path
                input_value = None
                if "caregiver_warmth" in input_name:
                    # Use computed average caregiver warmth
                    input_value = avg_caregiver_warmth
                elif "conflict" in input_name.lower():
                    input_value = loader.evaluate_path("world_slice.conflict_intensity", context)
                    if input_value is not None:
                        input_value = 100 - input_value  # inverse: higher conflict → lower safety
                elif input_name in ("policy_turbulence", "military_posture", "rhetoric_saturation"):
                    input_value = loader.evaluate_path(f"world_slice.{input_name}", context)
                    if input_value is not None:
                        input_value = 100 - input_value  # inverse: higher threat → lower safety
                elif input_name == "media_valence":
                    input_value = loader.evaluate_path("world_slice.media_valence", context)
                    # direct: higher valence (positive news) → higher safety
                elif input_name == "scrutiny_level":
                    input_value = loader.evaluate_path("world_slice.scrutiny_level", context)
                    # direct: higher scrutiny (accountability) → higher perceived justice
                else:
                    # Try to find the input path
                    for input_path in need_config.get("main_inputs", []):
                        if input_name in input_path:
                            input_value = loader.evaluate_path(input_path, context)
                            break
                
                if input_value is not None:
                    new_value += input_value * abs(weight)
        
        # ENHANCED: Strategy feedback - strategies partially satisfy needs
        # This creates realistic feedback loops where strategies help but don't fully solve problems
        strategy_satisfaction = _compute_strategy_satisfaction(need_name, strategies, need_config, loader)
        if strategy_satisfaction > 0:
            # Strategies provide partial satisfaction (diminishing returns)
            # Higher strategy use → more satisfaction, but with diminishing returns
            satisfaction_effect = strategy_satisfaction * 0.3  # Max 30% boost from strategies
            new_value = min(new_value + satisfaction_effect, 100.0)
        
        # ENHANCED: Index modulation - indices affect how needs respond
        if indices:
            need_modulation = _compute_index_modulation(need_name, indices, need_config)
            new_value = new_value * (1.0 + need_modulation)
        
        # ENHANCED: Cross-need compensation - unmet needs in one dimension
        # can be partially compensated by increases in other dimensions
        # This creates realistic psychological patterns aligned with Enneagram principles
        # and governed by early childhood imprint theory (ages 0-7 are most formative)
        
        # Try to get Enneagram type from context if available (from previous inference or state)
        enneagram_type = None
        if "enneagram_type" in context:
            enneagram_type = context.get("enneagram_type")
        elif "persona_state" in context:
            persona = context.get("persona_state")
            if hasattr(persona, "enneagram") and persona.enneagram:
                enneagram_type = persona.enneagram.primary_type
        
        # Get age and early childhood states for imprint-aware compensation
        age = context.get("age", 0)
        early_childhood_states = context.get("early_childhood_states", None)
        
        compensation_effect = _compute_cross_need_compensation(
            need_name, 
            prev_needs, 
            loader, 
            enneagram_type,
            age,
            early_childhood_states
        )
        if compensation_effect != 0:
            new_value = clamp(new_value + compensation_effect)
        
        # Apply decay rate if configured
        decay_rates = loader.get("needs", "decay_rates", {})
        if need_name in decay_rates:
            decay = decay_rates[need_name]
            new_value = new_value * decay + (1 - decay) * 50.0  # Decay toward neutral
        
        updated_dict[need_name] = clamp(new_value)
    
    # ENHANCED: Apply cross-need interactions from config (e.g., low_warmth_high_belonging)
    # This happens after all needs are computed, so we can check patterns
    interactions = loader.get("needs", "interactions", {})
    if interactions:
        updated_dict = _apply_cross_need_interactions(updated_dict, prev_needs, interactions, loader, context)
    
    # Create updated NeedGradients with all needs
    return NeedGradients(**updated_dict)


def update_strategies(
    prev_strategies: StrategyPortfolio,
    needs: NeedGradients,
    cognitive: CognitiveProfile,
    identity: IdentitySkeleton,
    world: WorldSlice,
    civic_soul: CivicSoulConditions,
    indices: Indices = None,
    age: int = 0,
    relations: "RelationalGraph" = None,
    driver_vec: "DriverVector" = None
) -> StrategyPortfolio:
    """
    Update strategies based on unmet needs, cognitive profile, and structural availability.
    Uses config/strategies.yaml to drive the update logic.
    
    ENHANCED: Now includes:
    - Age-based strategy availability (some strategies only available at certain ages)
    - Intensity-based triggering (more unmet need → stronger strategy activation)
    - Index modulation (indices affect strategy effectiveness/availability)
    - Need-based priority (most unmet needs trigger strategies first)
    """
    loader = get_config_loader()
    context = {
        "needs": needs,
        "strategies": prev_strategies,
        "identity": identity,
        "world_slice": world,
        "civic_soul": civic_soul,
        "indices": indices,
        "age": age,
        "relations": relations or RelationalGraph(),
        "driver_vec": driver_vec,
    }
    
    updated = StrategyPortfolio(**prev_strategies.__dict__)
    all_strategies = loader.get_all_strategies()
    
    # ENHANCED: Identify most unmet needs (prioritize strategies for these)
    unmet_needs = []
    for need_name in loader.get_all_needs():
        need_value = getattr(needs, need_name, 50.0)
        if need_value < 50.0:  # Unmet
            unmet_needs.append((need_name, need_value, 50.0 - need_value))  # (name, value, deficit)
    
    # Sort by deficit (most unmet first)
    unmet_needs.sort(key=lambda x: x[2], reverse=True)
    
    for strategy_name in all_strategies:
        strategy_config = loader.get_strategy_config(strategy_name)
        update_rules = strategy_config.get("update_rules", {})
        structural_avail = strategy_config.get("structural_availability", {})
        
        # ENHANCED: Age-based availability
        age_requirements = structural_avail.get("age_requirements", {})
        min_age = age_requirements.get("min_age", 0)
        max_age = age_requirements.get("max_age", 999)
        if age < min_age or age > max_age:
            # Strategy not available at this age, decay it
            current_value = getattr(updated, strategy_name, 0)
            if current_value > 0:
                decay_rates = loader.get("strategies", "decay_rates", {})
                decay = decay_rates.get(strategy_name, 0.90)
                setattr(updated, strategy_name, clamp(current_value * decay))
            continue
        
        # Check structural availability
        can_use = True
        requires = structural_avail.get("requires", [])
        blocks = structural_avail.get("blocks", [])
        
        # Check if blocked
        for block_condition in blocks:
            if loader.evaluate_condition(block_condition, context):
                can_use = False
                break
        
        # Check if required conditions are met
        # ENHANCED: More lenient for early childhood - if relations aren't set up yet
        if can_use:
            for req_condition in requires:
                try:
                    if not loader.evaluate_condition(req_condition, context):
                        # For early childhood (age < 7), be lenient if condition involves relations
                        if age < 7 and ('relation' in req_condition.lower() or 'caregiver' in req_condition.lower()):
                            # Allow strategy if other conditions are met
                            pass
                        else:
                            can_use = False
                            break
                except (AttributeError, KeyError, TypeError):
                    # If condition can't be evaluated (missing data), be lenient for early childhood
                    if age >= 7:
                        can_use = False
                        break
        
        if not can_use:
            # Strategy not available, decay it
            current_value = getattr(updated, strategy_name, 0)
            if current_value > 0:
                decay_rates = loader.get("strategies", "decay_rates", {})
                decay = decay_rates.get(strategy_name, 0.90)
                setattr(updated, strategy_name, clamp(current_value * decay))
            continue
        
        # Get current value
        current_value = getattr(updated, strategy_name, 0)
        
        # ENHANCED: Check increase conditions with intensity-based triggering
        increase_when = update_rules.get("increase_when", [])
        max_increase = 0
        triggered_condition = None
        
        for condition in increase_when:
            try:
                if loader.evaluate_condition(condition, context):
                    # ENHANCED: Intensity-based increase - more unmet need → stronger activation
                    # Check which need this strategy primarily regulates
                    primarily_regulates = strategy_config.get("primarily_regulates", [])
                    if primarily_regulates:
                        # Find the most unmet need this strategy regulates
                        for need_name, need_value, deficit in unmet_needs:
                            if need_name in primarily_regulates:
                                # Intensity: deficit * 0.3 (max 15 points per 50 point deficit)
                                intensity = min(deficit * 0.3, 20.0)
                                max_increase = max(max_increase, intensity)
                                triggered_condition = condition
                                break
                    
                    # If no specific need match, use default increase
                    if max_increase == 0:
                        max_increase = 15  # Default increase
                        triggered_condition = condition
            except (AttributeError, KeyError, TypeError):
                # Condition couldn't be evaluated, skip it
                continue
        
        # ENHANCED FALLBACK: If no conditions matched but needs are unmet,
        # activate strategies based on which needs they regulate
        if max_increase == 0 and unmet_needs:
            primarily_regulates = strategy_config.get("primarily_regulates", [])
            if primarily_regulates:
                for need_name, need_value, deficit in unmet_needs:
                    if need_name in primarily_regulates:
                        # Weaker than explicit conditions; stronger in early childhood
                        intensity = min(deficit * 0.25, 10.0) if age >= 14 else min(deficit * 0.3, 12.0)
                        max_increase = max(max_increase, intensity)
                        triggered_condition = f"fallback_{need_name}"
                        break
        
        if max_increase > 0:
            # ENHANCED: Index modulation - indices affect strategy effectiveness
            effectiveness_multiplier = 1.0
            if indices:
                # High DRTS → more aggressive strategies more effective
                if strategy_name in ["aggression_outward", "activism_justice", "risk_seeking_thrill"]:
                    effectiveness_multiplier = 1.0 + (indices.drts / 100.0) * 0.2
                # High RMT → withdrawal strategies more likely
                if strategy_name in ["withdrawal_avoidance", "dissociation_numbing", "fantasy_immersion"]:
                    effectiveness_multiplier = 1.0 + (indices.recursive_madness_threshold / 100.0) * 0.2
                # Low transgression threshold → compliance more likely
                if strategy_name == "compliance_obedience":
                    effectiveness_multiplier = 1.0 + ((100 - indices.transgression_threshold) / 100.0) * 0.2
            
            increase_amount = max_increase * effectiveness_multiplier
            new_value = clamp(current_value * 0.8 + increase_amount)
            setattr(updated, strategy_name, new_value)
        
        # Check decrease conditions
        decrease_when = update_rules.get("decrease_when", [])
        for condition in decrease_when:
            if loader.evaluate_condition(condition, context):
                # Decrease strategy
                new_value = clamp(current_value * 0.9)
                setattr(updated, strategy_name, new_value)
                break
        
        # Decay unused strategies slightly
        if current_value < 10 and not triggered_condition:
            decay_rates = loader.get("strategies", "decay_rates", {})
            decay = decay_rates.get(strategy_name, 0.95)
            setattr(updated, strategy_name, clamp(current_value * decay))
    
    return updated


def update_indices(
    prev_indices: Indices,
    world_slice: WorldSlice,
    driver_vec: DriverVector,
    local_modifiers: LocalModifiers,
    strategies: StrategyPortfolio,
    needs: NeedGradients
) -> Indices:
    """
    Update indices based on world, driver vector, local modifiers, strategies, and needs.

    WHAT INFLUENCES DRTS, IAI, TT (all code paths):
    - Birth (initial state): _apply_cultural_context_to_initial_state
      DRTS: hierarchy>50 & counter_cultural → +20; hierarchy>50 & aligned → -10; is_counter_cultural → +15.
      IAI: ritual>50 & aligned → +10. TT: default 50; is_counter_cultural → -10.
    - Each year TEMPLATE (no LLM): this function update_indices
      DRTS: prev*0.7 + inequality×egalitarian/fatalism (world_slice, driver_vec) + unmet needs (belonging, recognition, autonomy) + strategies (compliance↓, aggression/activism↑).
      IAI: prev*0.8 + ideology_boost*0.2 (piety_ideology, perfectionism_control strategies).
      TT: prev*0.8 + conflict_intensity (world_slice) + safety_deficit (needs.safety).
    - Each year LLM: apply_recursion_delta_to_state applies delta.indices_delta; fallbacks when model returns 0: drts_modifiers→DRTS+5, outlier_triggers→IAI+5, has_activity→DRTS+3/IAI+2, thought_rail_updates or has_activity→TT+2.
    - Events (config/events.yaml): _apply_event_effects applies event.effects.indices (drts, iai, transgression_threshold) when events define them.
    """
    updated = Indices(**prev_indices.__dict__)
    
    # PI (Permeability Index): up with tech/media and cross-border flows
    updated.permeability_index = clamp(
        prev_indices.permeability_index * 0.8 + world_slice.media_saturation * 0.2
    )
    
    # DRTS: up if inequality + egalitarian values; down if inequality + fatalism
    # ENHANCED: Also affected by unmet needs and strategies
    inequality_strain = world_slice.inequality_index
    egalitarian_tendency = 1 if driver_vec.authoritarian_vs_egalitarian > 50 else -1
    fatalism_tendency = 1 if driver_vec.fatalism_vs_agency < 50 else -1
    
    drts_base = (
        prev_indices.drts * 0.7 +
        (inequality_strain * egalitarian_tendency * 0.2) -
        (inequality_strain * fatalism_tendency * 0.1)
    )
    
    # ENHANCED: Unmet needs increase DRTS (frustration → defiance)
    unmet_belonging = max(0, 50.0 - needs.belonging_group)
    unmet_recognition = max(0, 50.0 - needs.recognition_status)
    unmet_autonomy = max(0, 50.0 - needs.autonomy_agency)
    drts_from_needs = (unmet_belonging + unmet_recognition + unmet_autonomy) / 150.0 * 10.0
    
    # ENHANCED: Strategies affect DRTS (compliance lowers it, aggression raises it)
    strategy_modifier = 0.0
    if strategies.compliance_obedience > 50:
        strategy_modifier -= (strategies.compliance_obedience - 50) / 50.0 * 5.0
    if strategies.aggression_outward > 50:
        strategy_modifier += (strategies.aggression_outward - 50) / 50.0 * 5.0
    if strategies.activism_justice > 50:
        strategy_modifier += (strategies.activism_justice - 50) / 50.0 * 3.0
    
    updated.drts = clamp(drts_base + drts_from_needs + strategy_modifier)
    
    # IAI: up as they encounter more coherent ideologies
    # ENHANCED: Multiple strategies contribute
    ideology_boost = 0.0
    if strategies.piety_ideology > 50:
        ideology_boost += (strategies.piety_ideology - 50) / 50.0 * 10.0
    if strategies.perfectionism_control > 50:
        ideology_boost += (strategies.perfectionism_control - 50) / 50.0 * 5.0
    
    updated.iai = clamp(
        prev_indices.iai * 0.8 + ideology_boost * 0.2
    )
    
    # TT (Transgression Threshold): shaped by cultural violence norms
    # ENHANCED: Also affected by unmet safety needs
    tt_base = prev_indices.transgression_threshold * 0.8
    if world_slice.conflict_intensity < 30:
        tt_base += 15 * 0.2
    else:
        tt_base -= 10 * 0.2
    
    # Low safety → lower threshold (more willing to transgress)
    safety_deficit = max(0, 50.0 - needs.safety)
    tt_modifier = -safety_deficit / 50.0 * 5.0
    
    updated.transgression_threshold = clamp(tt_base + tt_modifier)
    
    # AAF: shaped by exposure to cultural forms
    updated.aesthetic_amplification = clamp(
        prev_indices.aesthetic_amplification * 0.8 + world_slice.media_saturation * 0.2
    )
    
    # RMT: mismatch between atmospheric drivers and material reality
    # ENHANCED: Also affected by unmet needs (stress accumulation)
    aspiration_level = driver_vec.fatalism_vs_agency
    material_reality = world_slice.gdp_per_capita
    mismatch = abs(aspiration_level - material_reality)
    
    rmt_base = prev_indices.recursive_madness_threshold * 0.7 + mismatch * 0.3
    
    # ENHANCED: Unmet needs add to RMT (stress accumulation)
    total_unmet = (
        max(0, 50.0 - needs.safety) +
        max(0, 50.0 - needs.warmth_bonding) +
        max(0, 50.0 - needs.belonging_group)
    ) / 150.0 * 15.0  # Max 15 points from unmet needs
    
    # ENHANCED: Some strategies buffer RMT (religion, belonging)
    rmt_buffer = 0.0
    if strategies.piety_ideology > 60:
        rmt_buffer -= (strategies.piety_ideology - 60) / 40.0 * 5.0
    if needs.belonging_group > 70:
        rmt_buffer -= (needs.belonging_group - 70) / 30.0 * 5.0
    
    updated.recursive_madness_threshold = clamp(rmt_base + total_unmet + rmt_buffer)
    
    return updated


def update_thought_rails_from_drivers(
    prev_rails: ThoughtRails,
    driver_vec: DriverVector,
    local_modifiers: LocalModifiers
) -> ThoughtRails:
    """Update thought rails from driver vectors (from 03—with_enneagram.md)"""
    updated = ThoughtRails(**prev_rails.__dict__)
    
    # Driver vectors influence thought rails indirectly
    if driver_vec.authoritarian_vs_egalitarian > 60 and local_modifiers.ethnic_power_status == "minoritized":
        if "rigged" not in updated.fairness_schema:
            updated.tags["egalitarian_tendency"] = clamp(
                updated.tags.get("egalitarian_tendency", 50) + 10
            )
    
    if driver_vec.fatalism_vs_agency < 40:
        if "sufferer" not in updated.self_schema:
            updated.tags["fatalism"] = clamp(updated.tags.get("fatalism", 50) + 15)
    
    return updated


def update_thought_rails(
    prev_rails: ThoughtRails,
    symbolic: SymbolicState,
    civic_soul: CivicSoulConditions,
    indices: Indices,
    events: List[LifeEvent] = None
) -> ThoughtRails:
    """Update thought rails based on symbolic state, civic soul, and indices"""
    if events is None:
        events = []
    
    updated = ThoughtRails(**prev_rails.__dict__)
    
    has_major_event = any(
        e.type in ["migration", "loss", "conversion", "organizing"] for e in events
    )
    
    # Example: fairness_schema updates based on observed injustice
    if civic_soul.perceived_justice_order < 30:
        if "rigged" not in updated.fairness_schema and has_major_event:
            updated.fairness_schema = "rigged_game_but_God_keeps_score"
    
    # Example: authority_schema updates based on state repression
    if civic_soul.hierarchy_legitimacy < 30 and has_major_event:
        if "arbitrary" not in updated.authority_schema:
            updated.authority_schema = "arbitrary_violent_but_God_is_above"
    
    # Tags can update more fluidly
    updated.tags["meritocracy_belief"] = clamp(
        updated.tags.get("meritocracy_belief", 50) * 0.9 +
        (10 if civic_soul.perceived_justice_order > 70 else -10) * 0.1
    )
    
    return updated


def apply_idea_delta(persona: PersonaState, idea: IdeaDelta) -> PersonaState:
    """
    Apply an idea delta to a persona state (idea digestion).
    Implements the idea digestion process from 04—Rawlsling_v4.1.md
    """
    cognitive = persona.cognitive
    idea_digest = persona.idea_digest or IdeaDigest()
    
    # 1. Compute immediate affective reaction
    affect_match = _compute_affect_match(persona, idea)
    immediate_affect = _determine_immediate_affect(persona, idea, affect_match)
    
    # 2. Choose defense mechanism
    defense_used = _select_defense(cognitive, idea, immediate_affect)
    
    # 3. Compute maximum allowed deltas based on inertia
    max_deltas = _compute_max_deltas(cognitive, idea)
    
    # 4. Apply small moves toward the idea (or rebound away)
    applied_deltas = {}
    updated_rails = ThoughtRails(**persona.thought_rails.__dict__)
    updated_needs = NeedGradients(**persona.needs.__dict__)
    updated_strategies = StrategyPortfolio(**persona.strategies.__dict__)
    
    for axis, intensity in idea.target_axes.items():
        max_delta = max_deltas.get(axis, 5)
        actual_delta = clamp(intensity * (max_delta / 100), -max_delta, max_delta)
        
        applied_deltas[axis] = actual_delta
        
        # Apply to appropriate structure
        if "schema" in axis:
            if abs(actual_delta) > 2:
                idea_digest.unresolved_tensions[axis] = f"Unsettled: {idea.description}"
        elif "transcendence" in axis or "coherence" in axis:
            setattr(updated_needs, axis, clamp(getattr(updated_needs, axis) + actual_delta))
        elif "activism" in axis or "piety" in axis:
            setattr(updated_strategies, axis, clamp(getattr(updated_strategies, axis) + actual_delta))
    
    # 5. Determine integration status
    integration_status = _determine_integration_status(cognitive, applied_deltas, defense_used)
    
    # 6. Update idea digest
    new_digest = IdeaDigest(
        last_idea=idea,
        recent_ideas=(idea_digest.recent_ideas + [idea])[-10:],  # Keep last 10
        immediate_affect_label=immediate_affect,
        defense_used=defense_used,
        applied_deltas={**idea_digest.applied_deltas, **applied_deltas},
        integration_status=integration_status,
        unresolved_tensions=idea_digest.unresolved_tensions,
        notes=_generate_idea_digest_notes(persona, idea, applied_deltas, integration_status)
    )
    
    # Return updated persona
    return PersonaState(
        **{**persona.__dict__, **{
            "needs": updated_needs,
            "strategies": updated_strategies,
            "thought_rails": updated_rails,
            "idea_digest": new_digest,
            "narrative_snapshot": _update_narrative_snapshot(persona, idea, applied_deltas)
        }}
    )


# Helper functions for apply_idea_delta
def _compute_affect_match(persona: PersonaState, idea: IdeaDelta) -> Dict[str, float]:
    return {
        "resonance": 1.0 if idea.affect_valence > 0 and persona.needs.coherence_meaning < 50 else 0.0,
        "threat": 1.0 if idea.affect_valence < 0 and persona.needs.safety < 50 else 0.0
    }


def _determine_immediate_affect(persona: PersonaState, idea: IdeaDelta, affect_match: Dict) -> str:
    if persona.strategies.piety_ideology > 70 and "authority_schema" in idea.target_axes:
        return "threatened"
    if persona.indices.drts > 60 and "fairness_schema" in idea.target_axes:
        return "electrified"
    if affect_match.get("resonance"):
        return "confused"
    return "neutral"


def _select_defense(cognitive: CognitiveProfile, idea: IdeaDelta, immediate_affect: str) -> str:
    if immediate_affect == "threatened" and cognitive.compartmentalization > 70:
        return "compartmentalization"
    return cognitive.primary_defense


def _compute_max_deltas(cognitive: CognitiveProfile, idea: IdeaDelta) -> Dict[str, float]:
    base_max = 15 if cognitive.inertia < 30 else (5 if cognitive.inertia < 70 else 2)
    
    deltas = {}
    for axis in idea.target_axes.keys():
        delta = base_max
        if cognitive.compartmentalization > 70:
            delta *= 0.5
        if cognitive.elasticity > 70:
            delta *= 1.5
        deltas[axis] = delta
    
    return deltas


def _determine_integration_status(
    cognitive: CognitiveProfile,
    applied_deltas: Dict[str, float],
    defense_used: str
) -> str:
    total_delta = sum(abs(d) for d in applied_deltas.values())
    
    if total_delta < 1:
        return "rejected"
    if defense_used == "compartmentalization" or cognitive.compartmentalization > 70:
        return "compartmentalized"
    if total_delta > 20:
        return "overwhelming"
    if total_delta > 10:
        return "integrated"
    return "provisional"


def _generate_idea_digest_notes(
    persona: PersonaState,
    idea: IdeaDelta,
    applied_deltas: Dict[str, float],
    integration_status: str
) -> str:
    notes = [f'Idea "{idea.description}" hit with {integration_status} status.']
    
    if integration_status == "compartmentalized":
        notes.append("Kept in separate mental box, not integrated with core beliefs.")
    
    significant_deltas = [(k, v) for k, v in applied_deltas.items() if abs(v) > 2]
    if significant_deltas:
        notes.append(f"Affected: {', '.join(k for k, _ in significant_deltas)}")
    
    return " ".join(notes)


def _update_narrative_snapshot(persona: PersonaState, idea: IdeaDelta, applied_deltas: Dict) -> str:
    existing = persona.narrative_snapshot or ""
    new_note = f'Encountered idea: "{idea.description}". '
    return existing + new_note

# ============================================================================
# LIFE-COURSE SIMULATION
# ============================================================================


def simulate_year(
    current_state: PersonaState,
    target_age: int,
    world_slice: WorldSlice,
    driver_vec: DriverVector,
    local_modifiers: LocalModifiers,
    events: List[LifeEvent] = None,
    early_childhood_states: Optional[List[PersonaState]] = None
) -> PersonaState:
    """
    Simulate a single year of life.
    
    ENHANCED: Now accepts early_childhood_states for imprint-aware compensation.
    Early childhood (ages 0-7) is the imprint period in Enneagram theory.
    """
    if events is None:
        events = []
    
    target_year = current_state.identity.birth_year + target_age
    
    # Compute civic soul from world/driver/local
    civic_soul = compute_civic_soul(world_slice, driver_vec, local_modifiers)
    
    # Update world slice with civic soul
    world_with_civic = WorldSlice(**{**world_slice.__dict__, "civic_soul": civic_soul})
    
    # Build/update symbolic state
    symbolic = _build_symbolic_state_for_age(target_age, current_state, world_with_civic, civic_soul)
    
    # ENHANCED: Update in order with feedback loops
    # First, update needs (using previous strategies for feedback)
    needs = update_needs(
        current_state.needs,
        civic_soul,
        current_state.relations,
        current_state.strategies,
        world_with_civic,
        current_state.indices,  # Pass indices for modulation
        current_state,  # Pass persona state for Enneagram-aware compensation
        target_age,  # Pass age for imprint-aware compensation
        early_childhood_states  # Pass early states for imprint calculation
    )
    
    # Then update strategies (responding to new needs, using indices for modulation)
    strategies = update_strategies(
        current_state.strategies,
        needs,
        current_state.cognitive,
        current_state.identity,
        world_with_civic,
        civic_soul,
        current_state.indices,
        target_age,
        relations=current_state.relations,
        driver_vec=driver_vec
    )
    
    # Finally update indices (using new strategies and needs)
    indices = update_indices(
        current_state.indices,
        world_with_civic,
        driver_vec,
        local_modifiers,
        strategies,
        needs
    )
    # Apply event effects (from config/events.yaml) to needs, strategies, indices
    needs, strategies, indices = _apply_event_effects(needs, strategies, indices, events)
    # Type × driver modulation: when type is crystallized, apply type-specific sensitivity
    if current_state.enneagram and current_state.enneagram.primary_type:
        needs, strategies = _apply_driver_type_modulation(
            needs, strategies, current_state.enneagram.primary_type, driver_vec
        )
    # Update thought rails from drivers first
    thought_rails = update_thought_rails_from_drivers(
        current_state.thought_rails,
        driver_vec,
        local_modifiers
    )
    
    # Then update from symbolic state, civic soul, and indices
    thought_rails = update_thought_rails(
        thought_rails,
        symbolic,
        civic_soul,
        indices,
        events
    )
    
    # Determine band label
    band = _get_band_for_age(target_age)
    
    # Preserve driver_vec, parent driver vecs, and parent types in new state
    preserved_driver_vec = current_state.driver_vec if current_state.driver_vec else driver_vec
    preserved_father = getattr(current_state, "father_driver_vec", None)
    preserved_mother = getattr(current_state, "mother_driver_vec", None)
    preserved_father_type = getattr(current_state, "father_type", None)
    preserved_mother_type = getattr(current_state, "mother_type", None)

    return PersonaState(
        identity=current_state.identity,
        age=target_age,
        current_year=target_year,
        band=band,
        world=world_with_civic,
        needs=needs,
        strategies=strategies,
        relations=current_state.relations,
        symbols=symbolic,
        thought_rails=thought_rails,
        cognitive=current_state.cognitive,
        indices=indices,
        temperament=current_state.temperament,
        driver_vec=preserved_driver_vec,
        father_driver_vec=preserved_father,
        mother_driver_vec=preserved_mother,
        father_type=preserved_father_type,
        mother_type=preserved_mother_type,
        narrative_snapshot=_generate_narrative_snapshot(target_age, needs, strategies, events)
    )


def simulate_life_course(
    identity: IdentitySkeleton,
    adjusters: CohortAdjusters = None,
    constraints: PersonaConstraints = None,
    get_world_slice=None,
    get_driver_vec=None,
    get_local_modifiers=None,
    llm_callback: Optional[Callable[[PersonaState, str], Union[str, "LLMRecursionResult"]]] = None,
    parent_llm_callback: Optional[Callable[[str, str], str]] = None,
    name_llm_callback: Optional[Callable[[str], str]] = None,
    use_delta_schema: bool = True,
    parent_identity: Optional[Dict[str, Any]] = None,
) -> PersonaHistory:
    """
    Simulate full life course from birth to anchor year.

    Args:
        identity: Identity skeleton
        name_llm_callback: Optional. Called once with name-generation prompt; return JSON with
            child_given_name, child_family_name, father_given_name, father_family_name,
            mother_given_name, mother_family_name. Governs names by country, language, SES, religion, ethnicity.
        parent_llm_callback: Optional. Called for each parent with (role, prompt).
        llm_callback: Optional. Called after each year with (state, prompt).
    """
    if adjusters is None:
        adjusters = CohortAdjusters()
    if constraints is None:
        constraints = PersonaConstraints()
    
    # Generate parent identities and distinct parent driver vecs (kid responds to each parent)
    # If parent_identity is passed (parents-first flow), use it; else generate from identity.
    father_driver_vec = None
    mother_driver_vec = None
    parent_names_for_metadata: Optional[Dict[str, Dict[str, str]]] = None
    if get_driver_vec:
        try:
            from .identity_generator import generate_parent_identities
        except ImportError:
            from identity_generator import generate_parent_identities

        try:
            if parent_identity is None:
                parent_identity = generate_parent_identities(
                    country_code=identity.country_code,
                    child_birth_year=identity.birth_year,
                    allow_story_reasons=False,
                    enforce_father_older=True,
                )
            # LLM-generated names (child + both parents) from country, language, SES, religion, ethnicity
            if name_llm_callback and parent_identity:
                try:
                    prompt = build_name_generation_prompt(identity, parent_identity)
                    resp = name_llm_callback(prompt)
                    names = parse_name_generation_response(resp)
                    if names:
                        if names.get("child_given_name"):
                            identity.given_name = names["child_given_name"]
                        if names.get("child_family_name") is not None:
                            identity.family_name = names["child_family_name"] or ""
                        father = parent_identity["parents"]["father"]
                        mother = parent_identity["parents"]["mother"]
                        father["given_name"] = names.get("father_given_name") or ""
                        father["family_name"] = names.get("father_family_name") or ""
                        mother["given_name"] = names.get("mother_given_name") or ""
                        mother["family_name"] = names.get("mother_family_name") or ""
                        parent_names_for_metadata = {
                            "father": {"given_name": father["given_name"], "family_name": father["family_name"]},
                            "mother": {"given_name": mother["given_name"], "family_name": mother["family_name"]},
                        }
                except Exception:
                    pass
            location = parent_identity.get("location", {})
            urb = location.get("urbanicity", "").lower()
            urbanicity_code = "1" if any(k in urb for k in ("mega", "city", "town", "urban")) else ("2" if "rural" in urb else None)

            father = parent_identity["parents"]["father"]
            mother = parent_identity["parents"]["mother"]

            father_driver_vec = get_driver_vec(
                country_code=identity.country_code,
                year=identity.birth_year,
                age=int(father["age_at_child_birth"]),
                gender="male",
                religion=father.get("wvs_religion"),
                education=father.get("wvs_education"),
                income=father.get("wvs_income"),
                urbanicity=urbanicity_code,
            )
            mother_driver_vec = get_driver_vec(
                country_code=identity.country_code,
                year=identity.birth_year,
                age=int(mother["age_at_child_birth"]),
                gender="female",
                religion=mother.get("wvs_religion"),
                education=mother.get("wvs_education"),
                income=mother.get("wvs_income"),
                urbanicity=urbanicity_code,
            )
        except Exception:
            father_driver_vec = None
            mother_driver_vec = None

    # 2. CIA/factbook enrichment (after WVS); then 3. Parent Rawlsing (one recursion each)
    parent_birth_context = ""
    father_behavior = None
    mother_behavior = None
    father_type = None
    mother_type = None
    if father_driver_vec or mother_driver_vec:
        father_behavior = _sample_parent_behavior_from_wvs(father_driver_vec, variance=12.0) if father_driver_vec else None
        mother_behavior = _sample_parent_behavior_from_wvs(mother_driver_vec, variance=12.0) if mother_driver_vec else None
        father_type = infer_parent_type_most_likely(
            warmth=father_behavior["parental_warmth"], authority=father_behavior["parental_authority"],
            material_support=father_behavior["parental_material_support"], gender="male",
            driver_vec=father_driver_vec,
        ) if father_behavior and father_driver_vec else None
        mother_type = infer_parent_type_most_likely(
            warmth=mother_behavior["parental_warmth"], authority=mother_behavior["parental_authority"],
            material_support=mother_behavior["parental_material_support"], gender="female",
            driver_vec=mother_driver_vec,
        ) if mother_behavior and mother_driver_vec else None

        enriched = {}
        if parent_identity:
            try:
                from .parent_enrichment import enrich_family_context
            except ImportError:
                from parent_enrichment import enrich_family_context
            enriched = enrich_family_context(
                parent_identity, identity.country_code, identity.birth_year,
                get_world_slice=get_world_slice,
            )

        if parent_llm_callback and parent_identity:
            loc = parent_identity.get("location", {})
            ses = parent_identity.get("ses", {})
            ethnic = parent_identity.get("ethnicity", {})
            rel_lang = parent_identity.get("religion_language", {})
            father_prompt = build_parent_recursion_prompt(
                father, "father", father_driver_vec, father_type,
                father_behavior or {"parental_warmth": 50, "parental_authority": 50, "parental_material_support": 50},
                enriched, identity.birth_year, loc, ses, ethnic, rel_lang,
            )
            mother_prompt = build_parent_recursion_prompt(
                mother, "mother", mother_driver_vec, mother_type,
                mother_behavior or {"parental_warmth": 50, "parental_authority": 50, "parental_material_support": 50},
                enriched, identity.birth_year, loc, ses, ethnic, rel_lang,
            )
            try:
                father_narrative = parent_llm_callback("father", father_prompt) or ""
                mother_narrative = parent_llm_callback("mother", mother_prompt) or ""
                parts = [p for p in [father_narrative.strip(), mother_narrative.strip()] if p]
                parent_birth_context = " ".join(parts) if parts else ""
            except Exception:
                pass

    # Initialize birth state (with distinct parents; kid responds to each)
    birth_state = _initialize_birth_state(
        identity, adjusters, get_world_slice, get_driver_vec,
        father_driver_vec=father_driver_vec,
        mother_driver_vec=mother_driver_vec,
        father_behavior=father_behavior,
        mother_behavior=mother_behavior,
        father_type=father_type,
        mother_type=mother_type,
        parent_birth_context=parent_birth_context,
    )

    target_age = identity.age_at_anchor
    yearly_states = [birth_state]
    idea_history = []
    current_state = birth_state
    accumulated_llm_narrative: str = (birth_state.narrative_snapshot or "").strip()
    palimpsest: Palimpsest = Palimpsest()

    # Early childhood states for imprint-aware compensation (ages 0-7)
    early_childhood_states = []

    for age in range(1, target_age + 1):
        year = identity.birth_year + age
        world_slice = get_world_slice(identity.country_code, year) if get_world_slice else WorldSlice(year=year, country_code=identity.country_code)
        raw_driver_vec = get_driver_vec(identity.country_code, year, age) if get_driver_vec else DriverVector()
        # Filter drivers by age: only age-appropriate drivers influence simulation
        field_vals = get_field_values_for_age(raw_driver_vec, age)
        driver_vec = DriverVector(**{k: v for k, v in field_vals.items()})
        local_modifiers = get_local_modifiers(identity, year) if get_local_modifiers else LocalModifiers()
        events = _infer_life_events(current_state, age, world_slice, local_modifiers)

        if age <= 7:
            early_childhood_states.append(current_state)

        current_state = simulate_year(
            current_state,
            age,
            world_slice,
            driver_vec,
            local_modifiers,
            events=events,
            early_childhood_states=early_childhood_states if age > 7 else None,
        )
        # Developmental inference: ages 0-6 track candidates; age 7 crystallizes; age > 7 keep fixed
        states_so_far = yearly_states + [current_state]
        if age <= 6:
            current_state.enneagram_candidates = infer_enneagram_candidates(states_so_far)
        elif age == 7:
            current_state.enneagram = crystallize_enneagram(states_so_far)
        else:
            current_state.enneagram = yearly_states[-1].enneagram
            # Health level: continuous trajectory—previous year informs this year
            early_states = [s for s in yearly_states if s.age <= 7]
            if current_state.enneagram and early_states:
                prev_state = yearly_states[-1]
                current_state.enneagram.health_level = compute_health_level(
                    current_state.enneagram.primary_type,
                    early_states,
                    current_state,
                    events=events,
                    life_noise_std=5.0,
                    previous_health=prev_state.enneagram.health_level,
                    previous_state=prev_state,
                )
                # Keep Riso-Hudson metadata in sync
                hl = current_state.enneagram.health_level
                current_state.enneagram.metadata["health_level_riso"] = _health_level_to_riso(hl)
                current_state.enneagram.metadata["health_key_terms"] = _get_health_key_terms(
                    current_state.enneagram.primary_type,
                    current_state.enneagram.metadata["health_level_riso"],
                )

        # LLM recursion hook: GPT output feeds next recursion compoundingly
        if llm_callback:
            if use_delta_schema:
                world_slice = get_world_slice(identity.country_code, year) if get_world_slice else current_state.world
                raw_driver_vec = get_driver_vec(identity.country_code, year, age) if get_driver_vec else DriverVector()
                field_vals = get_field_values_for_age(raw_driver_vec, age)
                driver_vec = DriverVector(**field_vals)
                local_modifiers = get_local_modifiers(identity, year) if get_local_modifiers else LocalModifiers()
                data_derived = None
                valid_options = None
                if age == target_age:
                    data_derived, valid_options = compute_data_derived_life_snapshot(
                        identity, world_slice, current_state
                    )
                prompt = build_recursion_prompt_delta(
                    current_state, age, events, yearly_states,
                    palimpsest=palimpsest,
                    world_slice=world_slice,
                    driver_vec=driver_vec,
                    data_derived_life_snapshot=data_derived,
                    valid_options_life_snapshot=valid_options,
                    parent_birth_context=parent_birth_context,
                    local_modifiers=local_modifiers,
                    accumulated_narrative=accumulated_llm_narrative,
                )
                raw_result = llm_callback(current_state, prompt)
                raw_str = raw_result if isinstance(raw_result, str) else raw_result.narrative
                delta = parse_recursion_delta(raw_str, age, year)
                if delta:
                    # Sanitize obvious context drift (geo/religion leakage) before applying
                    rel_label = (current_state.identity.current_religion or current_state.identity.childhood_religion or "")
                    cc = current_state.identity.country_code
                    delta.identity_scripts = _sanitize_palimpsest_strings_for_identity(delta.identity_scripts, cc, rel_label)
                    delta.symbols_added = _sanitize_palimpsest_strings_for_identity(delta.symbols_added, cc, rel_label)
                    delta.moral_atmosphere_tags = _sanitize_palimpsest_strings_for_identity(delta.moral_atmosphere_tags, cc, rel_label)
                    delta.speech_tics = _sanitize_palimpsest_strings_for_identity(delta.speech_tics, cc, rel_label)
                    delta.subculture_tags = _sanitize_palimpsest_strings_for_identity(delta.subculture_tags, cc, rel_label)
                    delta.events_hooks = _sanitize_palimpsest_strings_for_identity(delta.events_hooks, cc, rel_label)
                    delta.moral_loops = _sanitize_palimpsest_strings_for_identity(delta.moral_loops, cc, rel_label)
                    delta.routines = _sanitize_palimpsest_strings_for_identity(delta.routines, cc, rel_label)
                    delta.roles_in_systems = _sanitize_palimpsest_strings_for_identity(delta.roles_in_systems, cc, rel_label)
                    delta.quirks = _sanitize_palimpsest_strings_for_identity(delta.quirks, cc, rel_label)
                    delta.authority_reception_patterns = _sanitize_authority_reception_patterns_for_identity(
                        delta.authority_reception_patterns, rel_label
                    )
                    # Present-year life_snapshot: enforce allowed taxonomy if we have it
                    if age == target_age and valid_options and data_derived:
                        delta.life_snapshot = _coerce_life_snapshot_to_allowed_values(
                            delta.life_snapshot, valid_options, data_derived
                        )
                    current_state = apply_recursion_delta_to_state(current_state, delta)
                    palimpsest = palimpsest.apply_delta(delta)
                    narrative_bit = (delta.narrative or "").strip() or _delta_narrative_fallback(delta)
                    if narrative_bit:
                        accumulated_llm_narrative = (accumulated_llm_narrative + "\n\n" + narrative_bit).strip()
                else:
                    accumulated_llm_narrative = (accumulated_llm_narrative + "\n\n" + (raw_str or "")).strip()
                current_state = replace(current_state, narrative_snapshot=accumulated_llm_narrative, palimpsest=palimpsest)
                idea_delta_dict = None if isinstance(raw_result, str) else getattr(raw_result, "idea_delta", None)
                if idea_delta_dict:
                    idea = IdeaDelta(
                        idea_id=idea_delta_dict.get("idea_id", f"year_{age}_experience"),
                        description=idea_delta_dict.get("description", (delta.narrative or raw_str or "")[:200] if delta else raw_str[:200] if raw_str else ""),
                        target_axes=idea_delta_dict.get("target_axes", {}),
                        source_trust=idea_delta_dict.get("source_trust", 70.0),
                        affect_valence=idea_delta_dict.get("affect_valence", 0.0),
                        affect_arousal=idea_delta_dict.get("affect_arousal", 50.0),
                    )
                    current_state = apply_idea_delta(current_state, idea)
            else:
                prompt = build_recursion_prompt(
                    current_state, age, events, yearly_states,
                    accumulated_narrative=accumulated_llm_narrative,
                )
                raw_result = llm_callback(current_state, prompt)
                narrative = raw_result if isinstance(raw_result, str) else raw_result.narrative
                idea_delta_dict = None if isinstance(raw_result, str) else getattr(raw_result, "idea_delta", None)
                if narrative:
                    accumulated_llm_narrative = (accumulated_llm_narrative + "\n\n" + narrative).strip()
                    current_state = replace(current_state, narrative_snapshot=accumulated_llm_narrative)
                if idea_delta_dict:
                    idea = IdeaDelta(
                        idea_id=idea_delta_dict.get("idea_id", f"year_{age}_experience"),
                        description=idea_delta_dict.get("description", narrative[:200] if narrative else ""),
                        target_axes=idea_delta_dict.get("target_axes", {}),
                        source_trust=idea_delta_dict.get("source_trust", 70.0),
                        affect_valence=idea_delta_dict.get("affect_valence", 0.0),
                        affect_arousal=idea_delta_dict.get("affect_arousal", 50.0),
                    )
                    current_state = apply_idea_delta(current_state, idea)
                    accumulated_llm_narrative = current_state.narrative_snapshot or accumulated_llm_narrative

        yearly_states.append(current_state)

        if hasattr(current_state, "idea_digest") and current_state.idea_digest and getattr(current_state.idea_digest, "last_idea", None):
            idea_history.append(current_state.idea_digest)

    # Aggregate into bands
    band_summaries = _build_band_history(yearly_states)
    # Enneagram: crystallized at 7, or fallback if target_age < 7
    final_state = yearly_states[-1]
    enneagram_profile = final_state.enneagram
    if enneagram_profile is None:
        enneagram_profile = infer_enneagram_from_life(yearly_states)
        final_state.enneagram = enneagram_profile
        yearly_states[-1] = final_state
    
    meta = {
        "generated_at": datetime.now().isoformat(),
        "version": "4.2",
        "total_years": target_age + 1
    }
    if parent_names_for_metadata is not None:
        meta["parent_names"] = parent_names_for_metadata
    return PersonaHistory(
        identity=identity,
        yearly_states=yearly_states,
        band_summaries=band_summaries,
        idea_history=idea_history,
        enneagram_profile=enneagram_profile,
        palimpsest=palimpsest if llm_callback and use_delta_schema else None,
        metadata=meta
    )


def _initialize_birth_state(
    identity: IdentitySkeleton,
    adjusters: CohortAdjusters,
    get_world_slice_func=None,
    get_driver_vec_func=None,
    father_driver_vec=None,
    mother_driver_vec=None,
    father_behavior=None,
    mother_behavior=None,
    father_type=None,
    mother_type=None,
    parent_birth_context: str = "",
) -> PersonaState:
    """
    Initialize birth state.
    
    ENHANCED: Now samples driver vector at birth to represent the broader
    cultural-psychic field the persona is born into. This cultural field:
    - Creates baseline influence (most personas align)
    - Allows counter-cultural development (some develop against field)
    - Influences initial needs, strategies, and indices
    """
    # Sample temperament at birth
    temperament = sample_enneagram_latent_vector()
    
    # Initialize with baseline values
    needs = NeedGradients()  # All default to 50.0
    strategies = StrategyPortfolio()  # All default to 0.0
    indices = Indices()  # Defaults
    
    thought_rails = ThoughtRails()
    cognitive = CognitiveProfile()
    
    # Get initial world slice (use provided function or create default)
    if get_world_slice_func:
        world_slice = get_world_slice_func(identity.country_code, identity.birth_year)
    else:
        world_slice = WorldSlice(
            year=identity.birth_year,
            country_code=identity.country_code,
        )

    # Sample driver vector at birth (cultural-psychic field)
    driver_vec = None
    if get_driver_vec_func:
        try:
            driver_vec = get_driver_vec_func(identity.country_code, identity.birth_year, 0)
        except Exception:
            driver_vec = None

    # Build relations with caregiver nodes from parent driver vecs (or precomputed behavior)
    relations = RelationalGraph()
    _father_type = father_type
    _mother_type = mother_type
    if father_driver_vec or mother_driver_vec:
        nodes = {}
        if father_driver_vec:
            fb = father_behavior if father_behavior else _sample_parent_behavior_from_wvs(father_driver_vec, variance=12.0)
            _father_type = father_type if father_type is not None else infer_parent_type_most_likely(
                warmth=fb["parental_warmth"],
                authority=fb["parental_authority"],
                material_support=fb["parental_material_support"],
                gender="male",
                driver_vec=father_driver_vec,
            )
            nodes["father"] = RelationalNode(
                node_id="father",
                role="father",
                role_type=RelationalRoleType.PRIMARY_CAREGIVER,
                centrality=80.0,
                cohabitation=True,
                warmth=fb["parental_warmth"],
                authority=fb["parental_authority"],
                material_support=fb["parental_material_support"],
                reliability=fb.get("parental_reliability", 50.0),
                harshness=fb.get("parental_harshness", 0.0),
                spiritual_support=fb.get("parental_spiritual_support", 0.0),
                alignment={"family": (fb["parental_warmth"] + fb["parental_authority"] + fb.get("parental_reliability", 50.0)) / 3.0},
                enneagram_type=_father_type,
            )
        if mother_driver_vec:
            mb = mother_behavior if mother_behavior else _sample_parent_behavior_from_wvs(mother_driver_vec, variance=12.0)
            _mother_type = mother_type if mother_type is not None else infer_parent_type_most_likely(
                warmth=mb["parental_warmth"],
                authority=mb["parental_authority"],
                material_support=mb["parental_material_support"],
                gender="female",
                driver_vec=mother_driver_vec,
            )
            nodes["mother"] = RelationalNode(
                node_id="mother",
                role="mother",
                role_type=RelationalRoleType.SECONDARY_CAREGIVER,
                centrality=85.0,
                cohabitation=True,
                warmth=mb["parental_warmth"],
                authority=mb["parental_authority"],
                material_support=mb["parental_material_support"],
                reliability=mb.get("parental_reliability", 50.0),
                harshness=mb.get("parental_harshness", 0.0),
                spiritual_support=mb.get("parental_spiritual_support", 0.0),
                alignment={"family": (mb["parental_warmth"] + mb["parental_authority"] + mb.get("parental_reliability", 50.0)) / 3.0},
                enneagram_type=_mother_type,
            )
        relations.nodes = nodes

    # ENHANCED: Apply cultural context to initial state
    # This creates baseline influence (aligned) but allows counter-cultural development
    if driver_vec:
        needs, strategies, indices = _apply_cultural_context_to_initial_state(
            needs, strategies, indices, driver_vec, identity
        )
    
    base_narrative = f"Born in {identity.birth_year} in {identity.locality or identity.country_code}, {identity.country_code}"
    if parent_birth_context:
        base_narrative = base_narrative + ". " + parent_birth_context
    
    return PersonaState(
        identity=identity,
        age=0,
        current_year=identity.birth_year,
        band="0-3",
        world=world_slice,
        needs=needs,
        strategies=strategies,
        relations=relations,
        symbols=SymbolicState(),
        thought_rails=thought_rails,
        cognitive=cognitive,
        indices=indices,
        temperament=temperament,
        driver_vec=driver_vec,
        father_driver_vec=father_driver_vec,
        mother_driver_vec=mother_driver_vec,
        father_type=_father_type,
        mother_type=_mother_type,
        narrative_snapshot=base_narrative,
    )


def _apply_cultural_context_to_initial_state(
    needs: NeedGradients,
    strategies: StrategyPortfolio,
    indices: Indices,
    driver_vec: DriverVector,
    identity: IdentitySkeleton
) -> Tuple[NeedGradients, StrategyPortfolio, Indices]:
    """
    Apply cultural context to initial state.
    
    The driver vector represents the broader cultural-psychic field the persona
    is born into. This function:
    1. Creates baseline influence (most personas align with field)
    2. Allows counter-cultural development (some develop against field)
    3. Influences initial needs, strategies, and indices
    
    Counter-cultural development creates:
    - Higher DRTS (defiance against cultural norms)
    - Different calibration (needs/strategies adjust differently)
    - Different type emergence (counter to field)
    
    Variance: Boosts are randomized (±30%) so identical driver profiles
    produce varied personalities rather than clones.
    """
    import random
    rng = random.Random()
    # Guard: default fallback drivers must not fake-modulate personality
    if getattr(driver_vec, 'is_default_fallback', False):
        return needs, strategies, indices
    is_counter_cultural = rng.random() < 0.30
    def _vary(x: float) -> float:
        return x * (0.85 + rng.random() * 0.30)

    # Collectivism → belonging / people-pleasing / caretaking (Types 2, 6, 9)
    individualism = getattr(driver_vec, 'individualism_vs_collectivism', 50.0)
    collectivism = 100.0 - individualism
    if collectivism > 50:
        if is_counter_cultural:
            needs.belonging_group = max(20.0, needs.belonging_group - _vary(8.0))
            needs.autonomy_agency = min(80.0, needs.autonomy_agency + _vary(8.0))
        else:
            needs.belonging_group = min(80.0, needs.belonging_group + _vary(8.0))
            strategies.people_pleasing = min(100.0, strategies.people_pleasing + _vary(12.0))
            strategies.caretaking_rescue = min(100.0, strategies.caretaking_rescue + _vary(8.0))

    # Hierarchy → safety/compliance
    hierarchy = driver_vec.authoritarian_vs_egalitarian
    if hierarchy > 50:  # High hierarchy
        if is_counter_cultural:
            # Counter: Reject authority, lower safety, higher defiance
            needs.safety = max(20.0, needs.safety - 10.0)
            needs.autonomy_agency = min(80.0, needs.autonomy_agency + 10.0)
            strategies.aggression_outward = 15.0  # Defiance
            strategies.activism_justice = 10.0
            indices.drts = min(100.0, indices.drts + 20.0)  # Higher defiance
        else:
            # Aligned: Rules = safety, compliance available
            needs.safety = min(80.0, needs.safety + 10.0)
            strategies.compliance_obedience = 15.0  # Compliance rewarded
            indices.drts = max(0.0, indices.drts - 10.0)  # Lower defiance
    
    # Ritual density → transcendence
    ritual = driver_vec.ritual_centrality if hasattr(driver_vec, 'ritual_centrality') else 50.0
    if ritual > 50:  # High ritual
        if is_counter_cultural:
            needs.transcendence_sacred = max(30.0, needs.transcendence_sacred - _vary(10.0))
            strategies.creative_expression = min(100.0, strategies.creative_expression + _vary(10.0))
        else:
            needs.transcendence_sacred = min(80.0, needs.transcendence_sacred + _vary(15.0))
            strategies.piety_ideology = min(100.0, strategies.piety_ideology + _vary(15.0))
            indices.iai = min(100.0, indices.iai + _vary(10.0))
    
    # Material security → safety/play
    # Use trust as proxy for material security
    material_security = driver_vec.trust_vs_distrust
    if material_security > 50:  # Higher trust = better material conditions
        if is_counter_cultural:
            # Counter: Reject material comfort, seek meaning
            needs.bodily_comfort = max(20.0, needs.bodily_comfort - 10.0)
            needs.coherence_meaning = min(80.0, needs.coherence_meaning + 10.0)
        else:
            # Aligned: Higher safety and play
            needs.safety = min(80.0, needs.safety + 5.0)
            needs.play_pleasure = min(80.0, needs.play_pleasure + 5.0)
    
    # Fatalism vs Agency → competence/autonomy (Types 3, 5, 8)
    agency = driver_vec.fatalism_vs_agency
    if agency < 50:  # High fatalism
        if is_counter_cultural:
            needs.autonomy_agency = min(80.0, needs.autonomy_agency + _vary(15.0))
            needs.competence_effectiveness = min(80.0, needs.competence_effectiveness + _vary(10.0))
            strategies.achievement_striving = min(100.0, strategies.achievement_striving + _vary(15.0))
        else:
            needs.autonomy_agency = max(20.0, needs.autonomy_agency - _vary(10.0))
            strategies.compliance_obedience = min(100.0, strategies.compliance_obedience + _vary(5.0))
    elif agency > 55:  # Low fatalism → achievement pathways available (Type 3)
        if not is_counter_cultural:
            strategies.achievement_striving = min(100.0, strategies.achievement_striving + _vary(12.0))
            needs.competence_effectiveness = min(80.0, needs.competence_effectiveness + _vary(5.0))
    
    # Religiosity → transcendence/piety
    religiosity = driver_vec.religiosity
    if religiosity > 50:
        if is_counter_cultural:
            needs.transcendence_sacred = max(20.0, needs.transcendence_sacred - _vary(15.0))
            needs.coherence_meaning = min(80.0, needs.coherence_meaning + _vary(10.0))
            strategies.creative_expression = min(100.0, strategies.creative_expression + _vary(10.0))
        else:
            needs.transcendence_sacred = min(80.0, needs.transcendence_sacred + _vary(10.0))
            strategies.piety_ideology = min(100.0, strategies.piety_ideology + _vary(18.0))

    if is_counter_cultural:
        indices.drts = min(100.0, indices.drts + _vary(15.0))
        indices.transgression_threshold = max(0.0, indices.transgression_threshold - _vary(10.0))
    
    return needs, strategies, indices


def _get_band_for_age(age: int) -> str:
    """Get age band label for a given age"""
    for band in AGE_BANDS:
        if band["start"] <= age < band["end"]:
            return band["label"]
    return "35+"


def _build_band_history(yearly_states: List[PersonaState]) -> List[PersonaState]:
    """Build band history from yearly states"""
    band_summaries = []
    
    for band_def in AGE_BANDS:
        band_states = [s for s in yearly_states if band_def["start"] <= s.age < band_def["end"]]
        
        if not band_states:
            continue
        
        # Aggregate numeric values (mean)
        aggregated_needs = _aggregate_needs([s.needs for s in band_states])
        aggregated_strategies = _aggregate_strategies([s.strategies for s in band_states])
        aggregated_indices = _aggregate_indices([s.indices for s in band_states])
        
        # Use last state's symbolic/thought rails (or aggregate)
        last_state = band_states[-1]
        aggregated_symbolic = _aggregate_symbolic([s.symbols for s in band_states])
        aggregated_rails = _aggregate_thought_rails([s.thought_rails for s in band_states], last_state.thought_rails)

        # Micrograph: caregivers/peers/institutions from relations; key_events/norm_conflicts from state.micrograph (delta)
        micrograph = getattr(last_state, "micrograph", None)
        caregivers = []
        peers = []
        institutions = []
        if last_state.relations and last_state.relations.nodes:
            caregivers = [
                n for n in last_state.relations.nodes.values()
                if n.role_type in [RelationalRoleType.PRIMARY_CAREGIVER, RelationalRoleType.SECONDARY_CAREGIVER]
            ]
            peers = [n for n in last_state.relations.nodes.values() if n.role_type == RelationalRoleType.PEER]
            institutions = [
                n for n in last_state.relations.nodes.values()
                if n.role_type in [RelationalRoleType.RELIGIOUS_AUTHORITY, RelationalRoleType.STATE_AGENT, RelationalRoleType.INSTITUTIONAL_FIGURE]
            ]
        key_events = list(micrograph.key_events) if micrograph else []
        norm_conflicts = list(micrograph.norm_conflicts) if micrograph else []
        if not caregivers and micrograph and getattr(micrograph, "caregivers", None):
            caregivers = micrograph.caregivers
        if not peers and micrograph and getattr(micrograph, "peers", None):
            peers = micrograph.peers
        if not institutions and micrograph and getattr(micrograph, "institutions", None):
            institutions = micrograph.institutions
        micrograph = RelationalMicrograph(caregivers=caregivers, peers=peers, institutions=institutions, key_events=key_events, norm_conflicts=norm_conflicts)

        band_summaries.append(PersonaState(
            **{**last_state.__dict__, **{
                "needs": aggregated_needs,
                "strategies": aggregated_strategies,
                "indices": aggregated_indices,
                "symbols": aggregated_symbolic,
                "thought_rails": aggregated_rails,
                "band": band_def["label"],
                "micrograph": micrograph
            }}
        ))

    return band_summaries


def _aggregate_needs(needs_array: List[NeedGradients]) -> NeedGradients:
    """Aggregate needs across states"""
    aggregated = {}
    for key in needs_array[0].__dict__.keys():
        if not key.startswith("_"):
            aggregated[key] = np.mean([getattr(n, key) for n in needs_array])
    return NeedGradients(**aggregated)


def _aggregate_strategies(strategies_array: List[StrategyPortfolio]) -> StrategyPortfolio:
    """Aggregate strategies across states"""
    aggregated = {}
    for key in strategies_array[0].__dict__.keys():
        if key == "extra":
            aggregated[key] = strategies_array[0].extra.copy()
        elif not key.startswith("_"):
            aggregated[key] = np.mean([getattr(s, key) for s in strategies_array])
    return StrategyPortfolio(**aggregated)


def _aggregate_indices(indices_array: List[Indices]) -> Indices:
    """Aggregate indices across states"""
    aggregated = {}
    for key in indices_array[0].__dict__.keys():
        if not key.startswith("_"):
            aggregated[key] = np.mean([getattr(i, key) for i in indices_array])
    return Indices(**aggregated)


def _aggregate_symbolic(symbolic_array: List[SymbolicState]) -> SymbolicState:
    """Aggregate symbolic state across states"""
    if not symbolic_array:
        return SymbolicState()
    salience = {}
    glosses = {}
    for sym in symbolic_array:
        if hasattr(sym, "salience") and sym.salience:
            for k, v in sym.salience.items():
                salience[k] = salience.get(k, 0) + v
        if hasattr(sym, "glosses") and sym.glosses:
            for k, v in sym.glosses.items():
                glosses[k] = glosses.get(k, "") + (" " + v if glosses.get(k) else v)
    n = len(symbolic_array)
    if n > 1:
        for k in salience:
            salience[k] /= n
    return SymbolicState(salience=salience, glosses=glosses)


def _aggregate_thought_rails(rails_array: List[ThoughtRails], last_state_rails: ThoughtRails) -> ThoughtRails:
    """Aggregate thought rails across states"""
    if not rails_array:
        return last_state_rails
    aggregated = ThoughtRails(
        authority_schema=last_state_rails.authority_schema,
        fairness_schema=last_state_rails.fairness_schema,
        self_schema=last_state_rails.self_schema,
        other_groups_schema=dict(last_state_rails.other_groups_schema) if last_state_rails.other_groups_schema else {},
        threat_schema=last_state_rails.threat_schema,
        hope_schema=last_state_rails.hope_schema,
        tags=dict(last_state_rails.tags) if last_state_rails.tags else {}
    )
    if len(rails_array) > 1:
        tag_keys = set()
        for r in rails_array:
            if r.tags:
                tag_keys.update(r.tags.keys())
        aggregated.tags = {}
        for key in tag_keys:
            values = [r.tags.get(key) for r in rails_array if r.tags and key in r.tags]
            if values:
                aggregated.tags[key] = np.mean(values)
    return aggregated


def compute_civic_soul(
    world_slice: WorldSlice,
    driver_vec: DriverVector,
    local_modifiers: LocalModifiers
) -> CivicSoulConditions:
    """
    Compute civic soul conditions from world/driver/local data.
    Uses config/civic_soul.yaml to drive the computation.
    """
    loader = get_config_loader()
    context = {
        "world_slice": world_slice,
        "driver_vec": driver_vec,
        "local_modifiers": local_modifiers,
        "identity": None,  # May be needed for some conditions
    }
    
    # Compute each civic soul condition using config
    conditions = {}
    civic_soul_config = loader.get("civic_soul", "civic_soul", {})
    
    # List of all civic soul condition names (matching class attributes)
    condition_names = [
        "rootedness",
        "perceived_justice_order",
        "obligation_symmetry",
        "rehabilitative_punishment_norms",
        "hierarchy_legitimacy",
        "shared_stake_in_common_goods",
        "risk_band"
    ]
    
    for condition_name in condition_names:
        condition_config = loader.get_civic_soul_config(condition_name)
        if not condition_config:
            # Use default
            defaults = loader.get("civic_soul", "defaults", {})
            conditions[condition_name] = defaults.get(condition_name, 50.0)
            continue
        
        formula_config = condition_config.get("formula", {})
        inputs_config = condition_config.get("inputs", [])
        
        # Compute using formula
        value = loader.compute_formula(formula_config, context, inputs_config)
        conditions[condition_name] = clamp(value)
    
    # Apply cross-condition interactions (need to update context with computed values)
    context["civic_soul"] = type('CivicSoul', (), conditions)()  # Temporary object for condition evaluation
    interactions = loader.get("civic_soul", "interactions", {})
    for interaction_name, interaction_config in interactions.items():
        condition = interaction_config.get("condition", "")
        if condition and loader.evaluate_condition(condition, context):
            # Apply effect
            for effect_key, effect_value in interaction_config.items():
                if effect_key.startswith("effect_on_"):
                    target_condition = effect_key.replace("effect_on_", "")
                    if target_condition in conditions:
                        conditions[target_condition] = clamp(
                            conditions[target_condition] + effect_value * 100
                        )
    
    # Use defaults for any missing conditions
    defaults = loader.get("civic_soul", "defaults", {})
    for condition_name, default_value in defaults.items():
        if condition_name not in conditions:
            conditions[condition_name] = default_value

    # Post-adjustments from world_slice.metadata (scales that don't match 0-100 in config)
    meta = getattr(world_slice, "metadata", None) or {}
    urban_pct = meta.get("urban_pct")
    if urban_pct is not None:
        # Low urban % (rural majority) → slightly higher rootedness; slight risk (vulnerability)
        conditions["rootedness"] = clamp(conditions["rootedness"] + (100.0 - float(urban_pct)) / 100.0 * 6.0)
        conditions["risk_band"] = clamp(conditions["risk_band"] + (100.0 - float(urban_pct)) / 100.0 * 4.0)
    schooling = meta.get("mean_years_schooling")
    if schooling is not None:
        # Low mean years schooling → order harder to navigate, more risk
        s = min(20.0, max(0.0, float(schooling)))
        conditions["perceived_justice_order"] = clamp(conditions["perceived_justice_order"] - (20.0 - s) / 20.0 * 6.0)
        conditions["risk_band"] = clamp(conditions["risk_band"] + (20.0 - s) / 20.0 * 8.0)

    return CivicSoulConditions(**conditions)


def _build_symbolic_state_for_age(
    age: int,
    prev_state: PersonaState,
    world_slice: WorldSlice,
    civic_soul: CivicSoulConditions
) -> SymbolicState:
    """Build symbolic state for a given age"""
    # This should use config/relational_roles.yaml
    # For now, return basic structure
    return SymbolicState(
        salience=prev_state.symbols.salience.copy(),
        glosses=prev_state.symbols.glosses.copy()
    )


def _apply_event_effects(
    needs: NeedGradients,
    strategies: StrategyPortfolio,
    indices: Indices,
    events: List[LifeEvent],
) -> Tuple[NeedGradients, StrategyPortfolio, Indices]:
    """Apply event effects (deltas from config) to needs, strategies, indices."""
    for evt in events:
        for part, deltas in getattr(evt, "effects", {}).items():
            if not isinstance(deltas, dict):
                continue
            if part == "needs":
                for k, delta in deltas.items():
                    if hasattr(needs, k):
                        setattr(needs, k, clamp(getattr(needs, k) + delta))
                    elif k == "rootedness":
                        setattr(needs, "belonging_group", clamp(getattr(needs, "belonging_group") + delta))
            elif part == "strategies":
                for k, delta in deltas.items():
                    if hasattr(strategies, k):
                        setattr(strategies, k, clamp(getattr(strategies, k) + delta))
            elif part == "indices":
                for k, delta in deltas.items():
                    if hasattr(indices, k):
                        setattr(indices, k, clamp(getattr(indices, k) + delta))
    return needs, strategies, indices


def _get_age_band_for_factor(age: int) -> str:
    """Map age to events.yaml age_factors key (e.g. '0-3', '7-11', '17+')."""
    if age <= 3:
        return "0-3"
    if age <= 6:
        return "3-7"
    if age <= 10:
        return "7-11"
    if age <= 13:
        return "11-14"
    if age <= 16:
        return "14-17"
    return "17+"


def _infer_life_events(
    current_state: PersonaState,
    age: int,
    world_slice: WorldSlice,
    local_modifiers: LocalModifiers,
    recent_events: Optional[List[LifeEvent]] = None,
) -> List[LifeEvent]:
    """
    Infer life events from config/events.yaml.
    Evaluates conditions, age_factors, class/conflict modifiers; rolls probabilities.
    """
    import random
    try:
        loader = get_config_loader()
    except Exception:
        return _infer_life_events_fallback(current_state, age, world_slice)
    events_config = loader.get("events", "events", {})
    if not events_config:
        return _infer_life_events_fallback(current_state, age, world_slice)
    modifiers = loader.get("events", "probability_modifiers", {})
    class_mods = modifiers.get("class_modifiers", {}).get(
        getattr(current_state.identity, "current_class", "middle"), {})
    conflict_mods = modifiers.get("conflict_modifiers", {})
    conflict = getattr(world_slice, "conflict_intensity", 0) or 0
    age_band = _get_age_band_for_factor(age)

    class _IdentityWithAge:
        pass

    identity_with_age = _IdentityWithAge()
    for k in dir(current_state.identity):
        if not k.startswith("_"):
            try:
                setattr(identity_with_age, k, getattr(current_state.identity, k))
            except Exception:
                pass
    identity_with_age.age = age
    identity_with_age.education_level = getattr(current_state.identity, "education_level", "primary")

    context = {
        "identity": identity_with_age,
        "world_slice": world_slice,
        "needs": current_state.needs,
        "relations": current_state.relations,
        "indices": current_state.indices,
        "civic_soul": getattr(world_slice, "civic_soul", None),
        "age": age,
    }
    events = []
    for category, cat_config in events_config.items():
        if category == "probability_modifiers" or not isinstance(cat_config, dict):
            continue
        type_list = cat_config.get("types", []) if isinstance(cat_config, dict) else []
        for evt_def in type_list:
            if not isinstance(evt_def, dict):
                continue
            conditions = evt_def.get("conditions", [])
            try:
                if not all(loader.evaluate_condition(c, context) for c in conditions):
                    continue
            except (AttributeError, KeyError, TypeError, ValueError):
                continue
            base_prob = evt_def.get("base_probability", 0.02)
            age_factors = evt_def.get("age_factors", {})
            factor = age_factors.get(age_band, age_factors.get("17+", 1.0))
            prob = base_prob * factor
            prob *= class_mods.get(category, 1.0)
            if conflict > 60:
                prob *= conflict_mods.get(category, 1.0)
            if random.random() >= min(prob, 0.95):
                continue
            subtype = evt_def.get("type", category)
            effects = evt_def.get("effects", {})
            desc = evt_def.get("description", f"{category}: {subtype}")
            events.append(LifeEvent(
                event_id=f"{subtype}_{age}_{random.randint(0, 9999)}",
                age=age,
                type=category,
                subtype=subtype,
                description=desc,
                metadata={"subtype": subtype},
                effects=effects,
            ))
    return events if events else _infer_life_events_fallback(current_state, age, world_slice)


def _infer_life_events_fallback(
    current_state: PersonaState,
    age: int,
    world_slice: WorldSlice,
) -> List[LifeEvent]:
    """Fallback when config unavailable or no events fired."""
    import random
    events = []
    if (getattr(world_slice, "conflict_intensity", 0) > 70 or getattr(world_slice, "regime_instability", 0) > 60) and random.random() < 0.1:
        events.append(LifeEvent(
            event_id=f"migration_{age}",
            age=age,
            type="migration",
            subtype="conflict_displacement",
            description="Family migrated due to conflict or regime instability",
            metadata={},
            effects={"needs": {"safety": -30, "belonging_group": -20}, "strategies": {"withdrawal_avoidance": 15}},
        ))
    if age > 10 and random.random() < 0.05:
        events.append(LifeEvent(
            event_id=f"loss_{age}",
            age=age,
            type="loss",
            subtype="generic_loss",
            description="Experienced significant loss",
            metadata={},
            effects={"needs": {"warmth_bonding": -20, "coherence_meaning": -15}, "strategies": {"withdrawal_avoidance": 10}},
        ))
    return events


def _generate_narrative_snapshot(
    age: int,
    needs: NeedGradients,
    strategies: StrategyPortfolio,
    events: List[LifeEvent]
) -> str:
    """Generate narrative snapshot for a given age"""
    parts = [f"Age {age}:"]
    
    unmet_needs = [
        k for k, v in needs.__dict__.items()
        if not k.startswith("_") and v < 40
    ]
    
    if unmet_needs:
        parts.append(f"Struggling with: {', '.join(unmet_needs)}")
    
    strategy_weights = [
        (k, getattr(strategies, k))
        for k in strategies.__dict__.keys()
        if not k.startswith("_") and k != "extra"
    ]
    dominant_strategies = sorted(strategy_weights, key=lambda x: x[1], reverse=True)[:3]
    
    if dominant_strategies:
        parts.append(f"Coping via: {', '.join(k for k, _ in dominant_strategies)}")
    
    if events:
        parts.append(f"Events: {', '.join(e.type for e in events)}")
    
    return " ".join(parts)

# ============================================================================
# ENNEAGRAM INFERENCE (from 03—with_enneagram.md)
# ============================================================================


def _apply_driver_type_modulation(
    needs: NeedGradients,
    strategies: StrategyPortfolio,
    primary_type: int,
    driver_vec: "DriverVector",
) -> Tuple[NeedGradients, StrategyPortfolio]:
    """
    Apply type × driver modulation: types are differentially sensitive to drivers.
    When a type's sensitive driver shifts, modulate the primary need for that type.
    """
    try:
        loader = get_config_loader()
    except Exception:
        return needs, strategies
    mod_config = loader.get("type_driver_sensitivity", "primary_need_modulation", {})
    cfg = mod_config.get(str(primary_type), mod_config.get(primary_type))
    if not cfg:
        return needs, strategies
    need_name = cfg.get("need")
    driver_name = cfg.get("driver")
    if not need_name or not driver_name or not hasattr(needs, need_name):
        return needs, strategies
    driver_val = getattr(driver_vec, driver_name, 50.0)
    if driver_val is None:
        driver_val = 50.0
    delta = (driver_val - 50.0) * 0.12
    current = getattr(needs, need_name)
    setattr(needs, need_name, clamp(current + delta))
    return needs, strategies


def _health_level_to_riso(health_level: float) -> int:
    """Map health_level (1-99) to Riso-Hudson level (1-9)."""
    try:
        loader = get_config_loader()
    except Exception:
        return 5
    bands = loader.get("health_levels_riso", "health_bands", [])
    for b in bands:
        if b.get("lo", 0) <= health_level <= b.get("hi", 99):
            return b.get("level", 5)
    return 5


def _get_health_key_terms(primary_type: int, riso_level: int) -> str:
    """Get Riso-Hudson key terms for type×level."""
    try:
        loader = get_config_loader()
    except Exception:
        return ""
    key_terms = loader.get("health_levels_riso", "key_terms", {})
    type_terms = key_terms.get(str(primary_type), key_terms.get(primary_type, {}))
    return type_terms.get(str(riso_level), type_terms.get(riso_level, ""))


def _compute_driver_type_mismatch_penalty(
    primary_type: int,
    driver_vec: Optional["DriverVector"],
    world_slice: Any,
) -> float:
    """
    Health penalty when drivers the type is sensitive to are "mismatched"
    (e.g. Type 6 in low-trust culture, Type 4 in low-ritual culture).
    """
    if driver_vec is None:
        return 0.0
    try:
        loader = get_config_loader()
    except Exception:
        return 0.0
    type_cfg = loader.get("type_driver_sensitivity", "type_sensitivity", {}).get(
        str(primary_type), {}
    ) or loader.get("type_driver_sensitivity", "type_sensitivity", {}).get(primary_type, {})
    mismatch = type_cfg.get("mismatch_penalty", {})
    if not mismatch:
        return 0.0
    penalty = 0.0
    conflict = getattr(world_slice, "conflict_intensity", 0) or 0
    for driver_field, penalty_per_10 in mismatch.items():
        val = getattr(driver_vec, driver_field, 50.0)
        if val is None:
            val = 50.0
        if val < 50:
            deviation = 50 - val
            penalty += (deviation / 10.0) * penalty_per_10
        if driver_field == "trust_vs_distrust" and conflict > 60:
            penalty += 2.0
    return min(penalty, 15.0)


def compute_health_level(
    primary_type: int,
    early_states: List[PersonaState],
    current_state: PersonaState,
    events: Optional[List] = None,
    life_noise_std: float = 18.0,
    previous_health: Optional[float] = None,
    previous_state: Optional[PersonaState] = None,
) -> float:
    """
    Compute health level. When previous_health is None (crystallization),
    compute from scratch. When provided, compute a delta from current conditions
    and apply to previous—continuous trajectory, each year informed by the last.
    """
    early_needs = [s.needs for s in early_states] if early_states else []
    avg_early_warmth = np.mean([n.warmth_bonding for n in early_needs]) if early_needs else 50.0
    avg_early_belonging = np.mean([n.belonging_group for n in early_needs]) if early_needs else 50.0
    avg_early_coherence = np.mean([n.coherence_meaning for n in early_needs]) if early_needs else 50.0
    buffers = (avg_early_warmth + avg_early_belonging + avg_early_coherence) / 3
    rmt = current_state.indices.recursive_madness_threshold
    gdp = getattr(current_state.world, "gdp_per_capita", 50.0)
    conflict = getattr(current_state.world, "conflict_intensity", 0.0)
    demographic_center_shift = max(-15.0, min(40.0,
        (gdp - 35) * 0.45 + (100 - conflict) * 0.15
    ))
    rmt_sensitivity = {
        1: 1.0, 2: 1.05, 3: 0.95, 4: 1.15, 5: 1.08, 6: 1.12, 7: 0.88, 8: 1.0, 9: 0.85
    }.get(primary_type, 1.0)
    buffer_multiplier = {
        1: 0.35, 2: 0.4, 3: 0.25, 4: 0.15, 5: 0.2, 6: 0.25, 7: 0.45, 8: 0.3, 9: 0.5
    }.get(primary_type, 0.3)
    type_resilience = {
        1: 3, 2: 0, 3: 4, 4: -12, 5: -6, 6: -10, 7: 8, 8: 2, 9: 10
    }.get(primary_type, 0)
    current_support = (
        current_state.needs.warmth_bonding
        + current_state.needs.belonging_group
        + current_state.needs.coherence_meaning
    ) / 3 - 50.0
    current_support_effect = current_support * 0.4
    events_effect = 0.0
    if events:
        for e in events:
            t = getattr(e, "type", "") if hasattr(e, "type") else ""
            if t == "loss":
                events_effect -= 12.0
            elif t == "migration":
                events_effect -= 5.0
    driver_mismatch_penalty = _compute_driver_type_mismatch_penalty(
        primary_type, getattr(current_state, "driver_vec", None), current_state.world
    )
    life_noise = np.random.normal(0, life_noise_std)
    if previous_health is None:
        # Scale terms so center lands in a plausible band (≈25–70) without a hard cap; RMT and buffers are the main drivers
        rmt_effect = (100.0 - (rmt * rmt_sensitivity)) * 0.35  # was 1:1, pushed to 99 when RMT low
        buffer_effect = (buffers - 50.0) * buffer_multiplier * 0.25
        plausible_center = (
            50.0
            + rmt_effect
            + buffer_effect
            + type_resilience * 0.5
            + demographic_center_shift * 0.3
            + current_support_effect
            + events_effect
            - driver_mismatch_penalty
        )
        return clamp(plausible_center + life_noise, 1.0, 99.0)
    rmt_delta = 0.0
    if previous_state is not None:
        prev_rmt = previous_state.indices.recursive_madness_threshold
        rmt_delta = (prev_rmt - rmt) * 0.2 * rmt_sensitivity
    delta = current_support_effect + events_effect + rmt_delta - driver_mismatch_penalty + life_noise
    delta = max(-15.0, min(15.0, delta))
    return clamp(previous_health + delta, 1.0, 99.0)


def _compute_enneagram_probabilities(
    states_over_time: List[PersonaState],
) -> Tuple[Dict[int, float], Dict[int, float], Dict[str, Any]]:
    """
    Shared core: compute type probabilities from state trajectory.
    Returns (probabilities, type_scores, context) for use by both
    infer_enneagram_candidates (ages 0-6) and infer_enneagram_from_life / crystallize_enneagram.
    """
    if not states_over_time:
        raise ValueError("Cannot compute Enneagram probabilities from empty state history")
    try:
        from .enneagram_wisdom import build_enneagram_wisdom_base, match_life_course_to_type
    except ImportError:
        from enneagram_wisdom import build_enneagram_wisdom_base, match_life_course_to_type
    wisdom_base = build_enneagram_wisdom_base()
    early_states = [s for s in states_over_time if s.age <= 7]
    context = _extract_inference_context(states_over_time, early_states)
    type_scores = {}
    for type_num in range(1, 10):
        if type_num in wisdom_base:
            wisdom = wisdom_base[type_num]
            type_scores[type_num] = match_life_course_to_type(
                states_over_time, wisdom, context=context
            )
        else:
            type_scores[type_num] = _mechanical_type_score(states_over_time, type_num)
    total_score = sum(max(0, s) for s in type_scores.values())
    probabilities = {
        t: (max(0, type_scores.get(t, 0)) / total_score if total_score > 0 else 1 / 9)
        for t in range(1, 10)
    }
    father_type = context.get("father_type")
    mother_type = context.get("mother_type")
    trust = None
    if context.get("driver_vec"):
        trust = getattr(context["driver_vec"], "trust_vs_distrust", None)
    if father_type is not None or mother_type is not None:
        try:
            from .parent_type_inference import get_parent_type_effects_for_child
        except ImportError:
            from parent_type_inference import get_parent_type_effects_for_child
        effects = get_parent_type_effects_for_child(father_type, mother_type, trust_vs_distrust=trust)
        for t in range(1, 10):
            probabilities[t] = max(0, probabilities[t] + effects.get(t, 0))
        total = sum(probabilities.values())
        if total > 0:
            probabilities = {t: probabilities[t] / total for t in range(1, 10)}
    # Soft floor so low-scoring types don't vanish; no ceiling (ceiling was flattening all types to ~1/9)
    FLOOR = 0.02
    probabilities = {t: max(probabilities.get(t, 0), FLOOR) for t in range(1, 10)}
    total = sum(probabilities.values())
    if total > 0:
        probabilities = {t: probabilities[t] / total for t in range(1, 10)}
    return probabilities, type_scores, context


def infer_enneagram_candidates(states_partial: List[PersonaState]) -> EnneagramCandidates:
    """
    Infer type candidates from partial trajectory (ages 0-6). No primary type yet.
    Used during early childhood before crystallization at age 6-7.
    """
    probabilities, type_scores, _ = _compute_enneagram_probabilities(states_partial)
    return EnneagramCandidates(probabilities=probabilities, raw_scores=type_scores)


def crystallize_enneagram(states_0_to_7: List[PersonaState]) -> EnneagramProfile:
    """
    Crystallize Enneagram at age 6-7 (Ichazo fixation window). Produces final profile.
    After this, type is fixed; only health level (and possibly wing) may later change.
    """
    profile = infer_enneagram_from_life(states_0_to_7)
    profile.metadata["crystallization_age"] = 7
    return profile


def infer_enneagram_from_life(states_over_time: List[PersonaState]) -> EnneagramProfile:
    """
    Infer Enneagram profile from life-course history using wisdom-guided pattern matching.
    
    PROBABILISTIC & DATA-RESPONSIVE:
    - Uses probability density functions, not fixed matching
    - Adapts to material circumstances (world conditions)
    - Models parental influence (WVS → parent behavior → child development)
    - Allows individual variation (not absolute determination)
    
    Uses insights from Ichazo, Naranjo, Riso, Chestnut to match life-course patterns
    to Enneagram types based on:
    - Core motivations, fears, defense mechanisms
    - Early childhood attachment patterns
    - Characteristic strategies and needs
    - Developmental trajectories
    - Centers (gut/heart/head)
    
    Enneagram is derived from the life-course, not assigned at birth.
    """
    if not states_over_time:
        raise ValueError("Cannot infer Enneagram from empty state history")
    probabilities, type_scores, context = _compute_enneagram_probabilities(states_over_time)
    try:
        from .enneagram_wisdom import build_enneagram_wisdom_base, match_life_course_to_type
    except ImportError:
        from enneagram_wisdom import build_enneagram_wisdom_base, match_life_course_to_type
    wisdom_base = build_enneagram_wisdom_base()

    # Probabilistic selection (not argmax) so floor produces diverse primary types across runs
    import random
    types = list(probabilities.keys())
    weights = [probabilities[t] for t in types]
    primary_type = random.choices(types, weights=weights, k=1)[0]
    
    # Determine wing using wisdom patterns if available
    if primary_type in wisdom_base:
        wisdom = wisdom_base[primary_type]
        prev_type = 9 if primary_type == 1 else primary_type - 1
        next_type = 1 if primary_type == 9 else primary_type + 1
        
        # Score wings using wing patterns (with context)
        prev_score = match_life_course_to_type(states_over_time, wisdom_base.get(prev_type), context=context) if prev_type in wisdom_base else probabilities.get(prev_type, 0)
        next_score = match_life_course_to_type(states_over_time, wisdom_base.get(next_type), context=context) if next_type in wisdom_base else probabilities.get(next_type, 0)
        
        wing = prev_type if prev_score > next_score else next_type
    else:
        # Fallback to simple probability comparison
        prev_type = 9 if primary_type == 1 else primary_type - 1
        next_type = 1 if primary_type == 9 else primary_type + 1
        wing = prev_type if probabilities[prev_type] > probabilities[next_type] else next_type
    
    early_states = [s for s in states_over_time if s.age <= 7]
    current_state = states_over_time[-1]
    health_level = compute_health_level(
        primary_type, early_states, current_state, events=None, life_noise_std=18.0
    )
    riso_level = _health_level_to_riso(health_level)
    key_terms = _get_health_key_terms(primary_type, riso_level)
    return EnneagramProfile(
        primary_type=primary_type,
        wing=wing,
        stack=probabilities,
        health_level=health_level,
        metadata={
            "inference_method": "wisdom_guided_pattern_matching",
            "confidence": max(probabilities.values()),
            "avg_rmt": np.mean([s.indices.recursive_madness_threshold for s in states_over_time]),
            "avg_drts": np.mean([s.indices.drts for s in states_over_time]),
            "avg_pi": np.mean([s.indices.permeability_index for s in states_over_time]),
            "type_scores": type_scores,
            "health_level_riso": riso_level,
            "health_key_terms": key_terms,
        }
    )


def _map_wvs_to_parent_behavior_ranges(
    driver_vec: DriverVector
) -> Dict[str, Tuple[float, float]]:
    """
    Map WVS driver values to parent behavior ranges.
    
    WVS gives us parent cohort values (e.g., authoritarian_vs_egalitarian = 70).
    We convert this to a RANGE of possible parent behaviors, then sample probabilistically.
    
    Returns dict of (min, max) ranges for:
    - parental_authority: From authoritarian_vs_egalitarian
    - parental_warmth: From family_importance, religiosity
    - parental_material_support: From material security drivers
    """
    ranges = {}
    
    # Map authoritarian_vs_egalitarian → parental_authority range
    # WVS: 0-100, where 100 = highly authoritarian
    # Parent authority: 0-100, where 100 = high authority
    auth_value = driver_vec.authoritarian_vs_egalitarian
    # Convert WVS value to parent authority range
    # High authoritarian (80-100) → authority range 70-90
    # Medium (40-80) → 50-75
    # Low (0-40) → 30-55
    if auth_value >= 80:
        ranges["parental_authority"] = (70.0, 90.0)
    elif auth_value >= 40:
        ranges["parental_authority"] = (50.0, 75.0)
    else:
        ranges["parental_authority"] = (30.0, 55.0)
    
    # Map family_importance + religiosity → parental_warmth range
    # High family importance + religiosity → higher warmth
    family_importance = driver_vec.family_importance if driver_vec.family_importance is not None else 50.0
    religiosity = driver_vec.religiosity
    warmth_factor = (family_importance + religiosity) / 2
    
    if warmth_factor >= 70:
        ranges["parental_warmth"] = (60.0, 85.0)
    elif warmth_factor >= 40:
        ranges["parental_warmth"] = (40.0, 70.0)
    else:
        ranges["parental_warmth"] = (20.0, 55.0)
    
    # Map material security → parental_material_support range
    # Use trust_vs_distrust and fatalism_vs_agency as proxies for material security
    # (Higher trust + agency = better material conditions)
    trust = driver_vec.trust_vs_distrust
    agency = driver_vec.fatalism_vs_agency  # Higher = more agency
    material_factor = (trust + agency) / 2
    
    if material_factor >= 70:
        ranges["parental_material_support"] = (60.0, 85.0)
    elif material_factor >= 40:
        ranges["parental_material_support"] = (40.0, 70.0)
    else:
        ranges["parental_material_support"] = (20.0, 55.0)

    # Harshness: inverse of warmth (low warmth → higher harshness)
    if warmth_factor >= 70:
        ranges["parental_harshness"] = (0.0, 25.0)
    elif warmth_factor >= 40:
        ranges["parental_harshness"] = (15.0, 50.0)
    else:
        ranges["parental_harshness"] = (30.0, 70.0)

    # Reliability: from trust_vs_distrust
    if trust >= 70:
        ranges["parental_reliability"] = (60.0, 85.0)
    elif trust >= 40:
        ranges["parental_reliability"] = (40.0, 65.0)
    else:
        ranges["parental_reliability"] = (20.0, 50.0)

    # Spiritual support: from religiosity
    if religiosity >= 70:
        ranges["parental_spiritual_support"] = (50.0, 85.0)
    elif religiosity >= 40:
        ranges["parental_spiritual_support"] = (25.0, 60.0)
    else:
        ranges["parental_spiritual_support"] = (0.0, 40.0)

    return ranges


def _sample_parent_behavior_from_wvs(
    driver_vec: Optional[DriverVector],
    variance: float = 10.0
) -> Dict[str, float]:
    """
    Probabilistically sample parent behavior from WVS distributions.
    
    If WVS data is available:
    1. Map WVS driver values to parent behavior ranges
    2. Sample probabilistically (randomized) from within those ranges
    3. Add individual variation (variance)
    
    If WVS data is not available, returns defaults with variance.
    
    Args:
        driver_vec: WVS driver vector for parent cohort
        variance: Standard deviation for individual variation
    
    Returns:
        Dict with parental_warmth, parental_authority, parental_material_support
    """
    if driver_vec is None:
        # No WVS data: sample from default ranges with variance
        return {
            "parental_warmth": np.random.normal(50.0, variance),
            "parental_authority": np.random.normal(50.0, variance),
            "parental_material_support": np.random.normal(50.0, variance),
            "parental_harshness": np.random.normal(20.0, variance),
            "parental_reliability": np.random.normal(50.0, variance),
            "parental_spiritual_support": np.random.normal(25.0, variance),
        }
    
    # Map WVS to behavior ranges
    ranges = _map_wvs_to_parent_behavior_ranges(driver_vec)
    
    # Sample probabilistically from each range (uniform distribution within range)
    # Then add individual variation (normal distribution)
    sampled = {}
    for key, (min_val, max_val) in ranges.items():
        # Uniform sample from range
        uniform_sample = np.random.uniform(min_val, max_val)
        # Add individual variation (not all parents identical)
        individual_variation = np.random.normal(0, variance)
        sampled[key] = clamp(uniform_sample + individual_variation)
    
    return sampled


def _extract_inference_context(
    states_over_time: List[PersonaState],
    early_states: List[PersonaState]
) -> Dict[str, Any]:
    """
    Extract context for probabilistic, data-responsive Enneagram inference.
    
    Models how material circumstances and parental values (from WVS) influence
    personality development. This makes the system:
    - DATA-RESPONSIVE: Adapts to actual world conditions
    - PROBABILISTIC: Samples from WVS distributions, not fixed values
    - CONTEXT-AWARE: Different outcomes in different circumstances
    
    Parental influence is sampled probabilistically from WVS parent cohort ranges:
    1. Get WVS driver_vec for parent cohort (if available)
    2. Map WVS values to parent behavior ranges
    3. Sample randomly from within those ranges
    4. Add individual variation (not all parents identical)
    
    Returns context dict with:
    - world_slice: World conditions (conflict, material security, etc.)
    - parental_warmth: Sampled from WVS family_importance/religiosity range
    - parental_authority: Sampled from WVS authoritarian_vs_egalitarian range
    - parental_material_support: Sampled from WVS material security range
    - driver_vec: Parent cohort WVS values (if available)
    """
    context = {}
    
    # Extract world conditions from early states (most formative period)
    driver_vec = None
    if early_states:
        # Use average world conditions from early childhood
        world_slices = [s.world for s in early_states if hasattr(s, 'world') and s.world]
        if world_slices:
            context["world_slice"] = world_slices[0]
        
        # Try to extract driver_vec from states (parent cohort WVS values)
        # Driver vec might be stored in world_slice or passed separately
        # For now, check if any state has a driver_vec attribute
        for state in early_states:
            if hasattr(state, 'driver_vec') and state.driver_vec:
                driver_vec = state.driver_vec
                break
            # Also check world_slice if it has driver data
            if hasattr(state, 'world') and state.world:
                if hasattr(state.world, 'driver_vec') and state.world.driver_vec:
                    driver_vec = state.world.driver_vec
                    break
    
    # PROBABILISTIC SAMPLING from WVS parent cohort distributions
    # This is the key: we sample from the RANGE that corresponds to the WVS values
    parent_behavior = _sample_parent_behavior_from_wvs(driver_vec, variance=10.0)
    context.update(parent_behavior)
    
    # Store driver_vec if available (for context modifiers)
    if driver_vec:
        context["driver_vec"] = driver_vec
    
    # Extract parent Enneagram types from birth state (inferred at initialization)
    father_type = None
    mother_type = None
    birth_state = next((s for s in states_over_time if s.age == 0), None)
    if birth_state:
        father_type = getattr(birth_state, "father_type", None)
        mother_type = getattr(birth_state, "mother_type", None)
        if father_type is None or mother_type is None:
            # Fallback: check caregiver nodes for enneagram_type
            if hasattr(birth_state, "relations") and birth_state.relations:
                for node in birth_state.relations.nodes.values():
                    if node.role == "father" and hasattr(node, "enneagram_type"):
                        father_type = node.enneagram_type
                    elif node.role == "mother" and hasattr(node, "enneagram_type"):
                        mother_type = node.enneagram_type
    context["father_type"] = father_type
    context["mother_type"] = mother_type

    # Fallback: if we couldn't get WVS data, use caregiver relations as proxy
    # (This happens if driver_vec isn't available, but relations were simulated)
    if driver_vec is None and early_states:
        caregivers = []
        for state in early_states:
            if hasattr(state, 'relations') and state.relations:
                for node in state.relations.nodes.values():
                    if node.role_type in [
                        RelationalRoleType.PRIMARY_CAREGIVER,
                        RelationalRoleType.SECONDARY_CAREGIVER
                    ]:
                        caregivers.append(node)
        
        if caregivers:
            # Use caregiver values as fallback (they were already simulated)
            avg_warmth = np.mean([c.warmth for c in caregivers])
            avg_authority = np.mean([c.authority for c in caregivers])
            avg_material = np.mean([c.material_support for c in caregivers])
            context["parental_warmth"] = clamp(np.random.normal(avg_warmth, 10.0))
            context["parental_authority"] = clamp(np.random.normal(avg_authority, 10.0))
            context["parental_material_support"] = clamp(np.random.normal(avg_material, 10.0))

    return context


def _mechanical_type_score(states_over_time: List[PersonaState], type_num: int) -> float:
    """Fallback scoring when type not in wisdom base. Uses strategy profiles from adult states."""
    adult_states = [s for s in states_over_time if s.age >= 18]
    if not adult_states:
        adult_states = states_over_time[-3:] if len(states_over_time) >= 3 else states_over_time
    strategies_list = [s.strategies for s in adult_states]

    def _avg(attr: str) -> float:
        return np.mean([getattr(s, attr, 0) for s in strategies_list]) if strategies_list else 0.0

    # Map type_num to strategy combinations (simplified fallback)
    type_strategy_map = {
        1: (_avg("perfectionism_control") + _avg("compliance_obedience")) / 2,
        2: (_avg("people_pleasing") + _avg("caretaking_rescue")) / 2,
        3: _avg("achievement_striving"),
        4: (_avg("creative_expression") + _avg("intimacy_seeking")) / 2,
        5: (_avg("withdrawal_avoidance") + (100 - _avg("people_pleasing"))) / 2,
        6: (_avg("compliance_obedience") + _avg("withdrawal_avoidance")) / 2,
        7: (_avg("humor_play") + _avg("fantasy_immersion")) / 2,
        8: (_avg("aggression_outward") + _avg("activism_justice")) / 2,
        9: (_avg("withdrawal_avoidance") + (100 - _avg("aggression_outward"))) / 2,
    }
    return type_strategy_map.get(type_num, 0.0)


def sample_enneagram_latent_vector() -> EnneagramLatentVector:
    """
    Sample Enneagram latent vector (temperament) at birth (from 05—implementation.md).
    This is NOT the final type, but innate tendencies that bias strategy selection.
    """
    import random
    return EnneagramLatentVector(
        reactivity=random.random() * 100,
        idealism=random.random() * 100,
        shame_vs_fear_vs_anger=random.random() * 100,
        uniqueness_vs_safety=random.random() * 100
    )

# ============================================================================
# LLM RECURSION HOOK (from 05—implementation.md; ENNEAGRAM_FIXATION_ETIOLOGY_SCHEMA Section 6)
# ============================================================================
#
# Contract: llm_callback(state, prompt) -> Union[str, LLMRecursionResult]
#   - str: narrative text only
#   - LLMRecursionResult: narrative + optional idea_delta for compounding feedback
# The caller (app, Cursor, etc.) implements the actual API call.
# ============================================================================


@dataclass
class LLMRecursionResult:
    """Return type for llm_callback when GPT output should feed the next recursion."""
    narrative: str
    idea_delta: Optional[Dict[str, Any]] = None  # Convertible to IdeaDelta for apply_idea_delta


def _get_rawlsing_stage_for_age(age: int) -> str:
    """Return Rawlsing stage label for age (0-3, 3-7, 7-11, 11-14, 14-17, 17+)."""
    if age <= 3:
        return "0-3"
    if age <= 7:
        return "3-7"
    if age <= 11:
        return "7-11"
    if age <= 14:
        return "11-14"
    if age <= 17:
        return "14-17"
    return "17+"


def _get_pi_interpretation(pi: float) -> str:
    """Return PI interpretation string from Rawlsing Section 3."""
    for _, (lo, hi, desc) in PI_INTERPRETATION.items():
        if lo <= pi < hi:
            return desc
    return PI_INTERPRETATION["extreme"][2]


# ---------------------------------------------------------------------------
# Name generation (LLM): explicit child-only and family modes, governed by country, language, SES, religion, ethnicity
# ---------------------------------------------------------------------------

CHILD_NAME_GENERATION_JSON_SCHEMA = '''
Return ONLY valid JSON in this shape. Names must be plausible for the given country, primary language, SES, religion, and ethnicity. Use conventional given/family patterns for that culture (e.g. patronymics where appropriate, religious or traditional names by religion/ethnicity). SES can affect formality and naming fashion (e.g. elite vs working-class naming in that place).
{
  "child_given_name": "<one or more given names as used in that culture>",
  "child_family_name": "<family/surname; empty string if single-name convention>"
}
'''


FAMILY_NAME_GENERATION_JSON_SCHEMA = '''
Return ONLY valid JSON in this shape. Names must be plausible for the given country, primary language, SES, religion, and ethnicity. Use conventional given/family patterns for that culture (e.g. patronymics where appropriate, religious or traditional names by religion/ethnicity). SES can affect formality and naming fashion (e.g. elite vs working-class naming in that place).
{
  "child_given_name": "<one or more given names as used in that culture>",
  "child_family_name": "<family/surname; empty string if single-name convention>",
  "father_given_name": "<father's given name(s)>",
  "father_family_name": "<father's family name; often same as child_family_name>",
  "mother_given_name": "<mother's given name(s)>",
  "mother_family_name": "<mother's family name; may be maiden name or same as father>"
}
'''


def _country_context_for_prompt(identity: "IdentitySkeleton", country_context: Dict[str, Any] | None) -> tuple[str, str]:
    ref = normalize_country_ref(country_context or getattr(identity, "country_code", "") or "")
    country_name = ref.get("canonical_name") or getattr(identity, "country_code", "") or "—"
    country_code = ref.get("iso2") or getattr(identity, "country_code", "") or "—"
    return country_name, country_code


def build_child_name_generation_prompt(
    identity: "IdentitySkeleton",
    country_context: Dict[str, Any] | None = None,
) -> str:
    """Build prompt for LLM to generate child names only."""
    loc_name, country_code = _country_context_for_prompt(identity, country_context)
    region = getattr(identity, "region", "") or "—"
    city = getattr(identity, "locality", "") or "—"
    urb = getattr(identity, "urbanicity", "—")
    class_label = getattr(identity, "current_class", "middle")
    ethnic_name = getattr(identity, "ethnicity_label", "—")
    religion = getattr(identity, "current_religion", "—")
    lang = getattr(identity, "primary_language", "—")
    child_gender = getattr(identity, "gender", "—")

    return f"""Generate plausible names for a child in this household. Return ONLY valid JSON.

CONTEXT (govern names by these—especially SES, religion, and ethnicity):
- Country: {loc_name} ({country_code}). Region/city: {region}, {city}. Urbanicity: {urb}.
- Child: gender {child_gender}, birth year {identity.birth_year}.
- SES/class: {class_label}. Use naming conventions typical for this class in this place.
- Ethnicity: {ethnic_name}. Religion: {religion}. Primary language: {lang}.
- Names must sound authentic for this country, language, and community—not generic or anglicized unless that fits (e.g. elite anglophone in a multilingual country).

{CHILD_NAME_GENERATION_JSON_SCHEMA}
"""


def build_family_name_generation_prompt(
    identity: "IdentitySkeleton",
    parent_identity: Dict[str, Any],
) -> str:
    """Build prompt for LLM to generate child + father + mother names from country, language, SES, religion, ethnicity."""
    country_name, country_code = _country_context_for_prompt(identity, None)
    loc = parent_identity.get("location", {})
    reg = loc.get("region") or {}
    loc_name = reg.get("admin1_name") or country_name or identity.country_code or "—"
    city = (loc.get("city") or {}).get("name") if isinstance(loc.get("city"), dict) else (loc.get("city") or "—")
    urb = loc.get("urbanicity") or getattr(identity, "urbanicity", "—")
    ses = parent_identity.get("ses", {})
    class_label = ses.get("class_label") or getattr(identity, "current_class", "middle")
    decile = ses.get("decile", 5)
    ethnic = parent_identity.get("ethnicity", {})
    ethnic_name = ethnic.get("group_name") or getattr(identity, "ethnicity_label", "—")
    rel_lang = parent_identity.get("religion_language", {})
    religion = rel_lang.get("religion") or getattr(identity, "current_religion", "—")
    lang = rel_lang.get("primary_language") or getattr(identity, "primary_language", "—")
    child_gender = getattr(identity, "gender", "—")
    father = parent_identity.get("parents", {}).get("father", {})
    mother = parent_identity.get("parents", {}).get("mother", {})
    father_age = father.get("age_at_child_birth", "—")
    mother_age = mother.get("age_at_child_birth", "—")

    return f"""Generate plausible names for a child and both parents in this household. Return ONLY valid JSON.

CONTEXT (govern names by these—especially SES, religion, and ethnicity):
- Country: {country_name} ({country_code}). Region/city: {loc_name}, {city}. Urbanicity: {urb}.
- Child: gender {child_gender}, birth year {identity.birth_year}.
- Parents: father ~{father_age} at child's birth, mother ~{mother_age} at child's birth.
- SES/class: {class_label} (decile {decile}). Use naming conventions typical for this class in this place.
- Ethnicity: {ethnic_name}. Religion: {religion}. Primary language: {lang}.
- Names must sound authentic for this country, language, and community—not generic or anglicized unless that fits (e.g. elite anglophone in a multilingual country).

{FAMILY_NAME_GENERATION_JSON_SCHEMA}
"""


def build_name_generation_prompt(
    identity: "IdentitySkeleton",
    parent_identity: Optional[Dict[str, Any]] = None,
) -> str:
    """Backward-compatible wrapper around the explicit child-only / family prompt builders."""
    if parent_identity:
        return build_family_name_generation_prompt(identity, parent_identity)
    return build_child_name_generation_prompt(identity)


def parse_name_generation_response(text: str) -> Optional[Dict[str, str]]:
    """Parse LLM JSON response into child + father + mother names. Returns None on failure."""
    import json
    raw = (text or "").strip()
    if "```" in raw:
        start = raw.find("```")
        if start >= 0:
            rest = raw[start + 3:]
            if rest.startswith("json"):
                rest = rest[4:]
            end = rest.find("```")
            raw = rest[:end] if end >= 0 else rest
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError:
        return None
    out = {}
    for key in ("child_given_name", "child_family_name", "father_given_name", "father_family_name", "mother_given_name", "mother_family_name"):
        val = obj.get(key)
        out[key] = (val.strip() if isinstance(val, str) and val.strip() else "") or ""
    return out


def build_parent_recursion_prompt(
    parent: Dict[str, Any],
    role: str,
    driver_vec: Optional["DriverVector"],
    enneagram_type: Optional[int],
    parent_behavior: Dict[str, float],
    enriched_context: Dict[str, Any],
    child_birth_year: int,
    location: Dict[str, Any],
    ses: Dict[str, Any],
    ethnicity: Dict[str, Any],
    religion_language: Dict[str, Any],
) -> str:
    """
    Build prompt for ONE Rawlsing recursion on a parent.
    Used to stitch who the baby is being born to—who they are at this moment.
    """
    age = int(parent.get("age_at_child_birth", 30))
    birth_year = child_birth_year - age
    reg = location.get("region") or {}
    loc_name = reg.get("admin1_name") or location.get("country_code") or "—"
    urb = location.get("urbanicity") or "—"
    ethnic_name = ethnicity.get("group_name") or "—"
    decile = ses.get("decile", 5)
    class_label = ses.get("class_label") or "middle"
    rel = religion_language.get("religion") or "—"
    lang = religion_language.get("primary_language") or "—"
    
    warmth = parent_behavior.get("parental_warmth", 50)
    authority = parent_behavior.get("parental_authority", 50)
    material = parent_behavior.get("parental_material_support", 50)
    
    enneagram_block = ""
    if enneagram_type:
        lost = LOST_MESSAGES.get(enneagram_type, "")
        unconscious = UNCONSCIOUS_MESSAGES.get(enneagram_type, "")
        enneagram_block = f"""
Enneagram: Type {enneagram_type}. Unconscious message: "{unconscious}". Lost message: "{lost}"
"""
    
    # Driver vec summary (key WVS dimensions)
    driver_block = ""
    if driver_vec:
        vals = {k: getattr(driver_vec, k) for k in ["trust_vs_distrust", "authoritarian_vs_egalitarian", "fatalism_vs_agency", "individualism_vs_collectivism"] if hasattr(driver_vec, k)}
        driver_block = f"\nWVS driver values (cohort): {vals}"
    
    # Enriched context (OWID/WDI/V-Dem when available; else Factbook fallback)
    ws = enriched_context.get("world_slice", {})
    hh = enriched_context.get("household", {})
    bc = enriched_context.get("birth_context", {})
    imr = bc.get("infant_mortality_per_1000")
    le = bc.get("country_life_expectancy")
    enrich_block = f"""
Country context (year {child_birth_year}): IMR={imr if imr is not None else '—'}/1000, life expectancy={le if le is not None else '—'}y. Internet≈{(ws.get('internet_users_pct') or 0):.0f}%, GDP≈{(ws.get('gdp_per_capita') or 50):.0f}, unemployment≈{(ws.get('unemployment_rate') or 0):.0f}%.
Household: internet≈{(hh.get('internet_access_pct') or 0):.0f}%, literacy context={(hh.get('adult_literacy_context') or 50):.0f}, urbanicity={hh.get('urbanicity', '—')}, SES decile={hh.get('ses_decile', decile)}.
"""
    
    prompt = f"""You are building WHO THIS PARENT IS—one Rawlsing recursion. This parent will have a baby in {child_birth_year}. Your output will become the story the baby is born into.

PARENT: {role}, age {age} at child's birth (born ~{birth_year}).
Location: {loc_name}, {urb}. Ethnicity: {ethnic_name}. SES: decile {decile} ({class_label}). Religion: {rel}. Language: {lang}.
Parent behavior (from WVS cohort): warmth={warmth:.0f}, authority={authority:.0f}, material_support={material:.0f}.
{enneagram_block}{driver_block}{enrich_block}

Generate 4–6 sentences: who this person is—temperament, relational style, what they carry (fears, hopes, defenses), how they show up as a parent-to-be. Concrete, not generic. Rawlsing v4.0: recursion, contradiction, plausible inner texture. This becomes the story the baby is born into."""
    return prompt


def build_parent_to_meeting_prompt(
    parent: Dict[str, Any],
    role: str,
    driver_vec: Optional["DriverVector"],
    enneagram_type: Optional[int],
    parent_behavior: Dict[str, float],
    enriched_context: Dict[str, Any],
    child_birth_year: int,
    location: Dict[str, Any],
    ses: Dict[str, Any],
    ethnicity: Dict[str, Any],
    religion_language: Dict[str, Any],
) -> str:
    """
    Build prompt for the OLDER parent only: backstory UP TO the point of meeting the other parent.
    Output is used as input to the second call (second parent + fused narrative).
    """
    age = int(parent.get("age_at_child_birth", 30))
    birth_year = child_birth_year - age
    reg = location.get("region") or {}
    loc_name = reg.get("admin1_name") or location.get("country_code") or "—"
    urb = location.get("urbanicity") or "—"
    ethnic_name = ethnicity.get("group_name") or "—"
    decile = ses.get("decile", 5)
    class_label = ses.get("class_label") or "middle"
    rel = religion_language.get("religion") or "—"
    lang = religion_language.get("primary_language") or "—"
    warmth = parent_behavior.get("parental_warmth", 50)
    authority = parent_behavior.get("parental_authority", 50)
    material = parent_behavior.get("parental_material_support", 50)
    enneagram_block = ""
    if enneagram_type:
        lost = LOST_MESSAGES.get(enneagram_type, "")
        unconscious = UNCONSCIOUS_MESSAGES.get(enneagram_type, "")
        enneagram_block = f"\nEnneagram: Type {enneagram_type}. Unconscious: \"{unconscious}\". Lost: \"{lost}\""
    driver_block = ""
    if driver_vec:
        vals = {k: getattr(driver_vec, k) for k in ["trust_vs_distrust", "authoritarian_vs_egalitarian", "fatalism_vs_agency", "individualism_vs_collectivism"] if hasattr(driver_vec, k)}
        driver_block = f"\nWVS driver values: {vals}"
    ws = enriched_context.get("world_slice", {})
    hh = enriched_context.get("household", {})
    bc = enriched_context.get("birth_context", {})
    enrich_block = f"\nContext (year {child_birth_year}): IMR={bc.get('infant_mortality_per_1000') or '—'}/1000, life exp={bc.get('country_life_expectancy') or '—'}y. Household: urbanicity={hh.get('urbanicity', '—')}, SES decile={hh.get('ses_decile', decile)}."
    return f"""You are building this parent's backstory UP TO the moment they meet their future co-parent. They will later have a baby in {child_birth_year}. Stop your narrative at the point of meeting the other parent—do not yet describe the relationship or the child.

PARENT: {role}, age {age} at child's birth (born ~{birth_year}).
Location: {loc_name}, {urb}. Ethnicity: {ethnic_name}. SES: decile {decile} ({class_label}). Religion: {rel}. Language: {lang}.
Parent behavior (cohort): warmth={warmth:.0f}, authority={authority:.0f}, material_support={material:.0f}.{enneagram_block}{driver_block}{enrich_block}

Generate 4–6 sentences: who this person is—temperament, relational style, what they carry (fears, hopes, defenses)—and bring their story up to the point where they MEET the future other parent. End at that meeting. Concrete, not generic. Rawlsing v4.0: recursion, contradiction, plausible inner texture."""


def build_second_parent_and_fused_prompt(
    second_parent: Dict[str, Any],
    second_role: str,
    first_parent_meeting_narrative: str,
    first_role: str,
    driver_vec: Optional["DriverVector"],
    enneagram_type: Optional[int],
    parent_behavior: Dict[str, float],
    enriched_context: Dict[str, Any],
    child_birth_year: int,
    location: Dict[str, Any],
    ses: Dict[str, Any],
    ethnicity: Dict[str, Any],
    religion_language: Dict[str, Any],
) -> str:
    """
    Build prompt for the SECOND parent: who they are, then FUSE with the first parent's story—
    how they met, why they're together, "together-twining" up to the child's birth.
    """
    age = int(second_parent.get("age_at_child_birth", 28))
    birth_year = child_birth_year - age
    reg = location.get("region") or {}
    loc_name = reg.get("admin1_name") or location.get("country_code") or "—"
    urb = location.get("urbanicity") or "—"
    ethnic_name = ethnicity.get("group_name") or "—"
    decile = ses.get("decile", 5)
    class_label = ses.get("class_label") or "middle"
    rel = religion_language.get("religion") or "—"
    lang = religion_language.get("primary_language") or "—"
    warmth = parent_behavior.get("parental_warmth", 50)
    authority = parent_behavior.get("parental_authority", 50)
    material = parent_behavior.get("parental_material_support", 50)
    enneagram_block = ""
    if enneagram_type:
        lost = LOST_MESSAGES.get(enneagram_type, "")
        unconscious = UNCONSCIOUS_MESSAGES.get(enneagram_type, "")
        enneagram_block = f"\nEnneagram: Type {enneagram_type}. Unconscious: \"{unconscious}\". Lost: \"{lost}\""
    driver_block = ""
    if driver_vec:
        vals = {k: getattr(driver_vec, k) for k in ["trust_vs_distrust", "authoritarian_vs_egalitarian", "fatalism_vs_agency", "individualism_vs_collectivism"] if hasattr(driver_vec, k)}
        driver_block = f"\nWVS driver values: {vals}"
    return f"""You are building (1) who the SECOND parent is, and (2) a FUSED narrative: how they met the first parent, why they're together, and the "together-twining" up to the birth of their child in {child_birth_year}.

THE FIRST PARENT (up to meeting)—use this as the anchor the second parent meets:
---
{first_parent_meeting_narrative.strip()}
---

SECOND PARENT: {second_role}, age {age} at child's birth (born ~{birth_year}).
Location: {loc_name}, {urb}. Ethnicity: {ethnic_name}. SES: decile {decile} ({class_label}). Religion: {rel}. Language: {lang}.
Parent behavior (cohort): warmth={warmth:.0f}, authority={authority:.0f}, material_support={material:.0f}.{enneagram_block}{driver_block}

Generate two parts in one response (4–8 sentences total):
1) Who this second parent is—temperament, what they carry, how they show up—in 2–3 sentences.
2) How they met the first parent, why they're together, and the fused "together" story up to the baby's birth in {child_birth_year}—destined-to-be, retcon, or plain how-it-happened. Concrete, not generic. Rawlsing v4.0: recursion, contradiction, plausible inner texture. This becomes the story the baby is born into."""


def build_recursion_prompt(
    state: PersonaState,
    age: int,
    events: List[LifeEvent],
    history: List[PersonaState],
    accumulated_narrative: str = "",
) -> str:
    """
    Build prompt for GPT recursion at a given age.
    Wires Rawlsing v4.0 framework: identity, indices (PI/DRTS/IAI/TT/AAF/RMT), Enneagram,
    age-band-specific guidance, symbolic lexicon, moral atmosphere, outlier triggers.
    Output becomes the persona's internal world (iceberg). Runs year-by-year, unseen by user.
    """
    profile = state.enneagram
    events_str = ", ".join(e.type for e in events) if events else "none"
    stage = _get_rawlsing_stage_for_age(age)
    stage_guidance = RAWLSING_STAGE_GUIDANCE.get(stage, RAWLSING_STAGE_GUIDANCE["17+"])

    # Identity (Rawlsing Section 1)
    id_ = state.identity
    identity_block = f"""
IDENTITY (Rawlsing base prompt):
Location: {id_.locality or id_.region or id_.country_code}, {id_.country_code}. Born {state.current_year - age}.
Gender: {id_.gender}. SES: {id_.current_class}. Urbanicity: {id_.urbanicity}.
Religion/cultural: {id_.current_religion or id_.childhood_religion or '—'}. Religiosity: {id_.religiosity_level}/100.
Ethnicity/minority: {id_.ethnicity_label or '—'}; {id_.minority_status}.
Languages: {id_.primary_language}; {', '.join(id_.secondary_languages) if id_.secondary_languages else '—'}."""

    # Structural state (needs, strategies)
    needs = {k: v for k, v in state.needs.__dict__.items() if not k.startswith("_")}
    strategies = {
        k: v for k, v in state.strategies.__dict__.items()
        if not k.startswith("_") and k != "extra"
    }
    top_strategies = sorted(strategies.items(), key=lambda x: x[1], reverse=True)[:5]

    # Indices (Rawlsing PI, DRTS, Outlier Engine)
    idx = state.indices
    pi_val = idx.permeability_index
    pi_desc = _get_pi_interpretation(pi_val)
    indices_block = f"""
INDICES (Rawlsing Section 3–5):
PI (Permeability Index): {pi_val:.0f}/100 — {pi_desc}
DRTS (Defiance/Revolutionary Tendencies): {idx.drts:.0f}/100 (10–30 passive; 30–50 suppressed but ready; 50–80 active; 80–100 revolutionary)
IAI (Ideological Autopoiesis): {idx.iai:.0f}/100
Transgression Threshold: {idx.transgression_threshold:.0f}/100
AAF (Aesthetic Amplification): {idx.aesthetic_amplification:.0f}/100
RMT (Recursive Madness Threshold): {idx.recursive_madness_threshold:.0f}/100"""

    # Outlier triggers (Rawlsing Section 5) — hint when relevant
    outlier_hints = []
    if idx.iai >= 70:
        outlier_hints.append("IAI≥70: consider self-reinforcing ideological myth-making, closed belief system, idiosyncratic vocabulary.")
    if idx.drts >= 60 and events:
        outlier_hints.append("DRTS≥60 + events: consider Transgression Threshold—defiance turning to willingness to cause harm, moral inversion.")
    if idx.drts >= 65:
        outlier_hints.append("DRTS≥65: consider Aesthetic Amplification—defiance through mythopoetic, artistic, ritual forms.")
    if idx.drts >= 80:
        outlier_hints.append("DRTS≥80: consider RMT—breakdowns in reality-processing, pattern-seeking, identity slippage.")
    outlier_block = "\n".join(outlier_hints) if outlier_hints else ""

    # World / civic soul
    ws = state.world
    civic = ws.civic_soul if ws else None
    world_block = f"""
WORLD (Year {state.current_year}, {id_.country_code}):
GDP/inequality/conflict: gdp={getattr(ws, 'gdp_per_capita', 50):.0f}, inequality={getattr(ws, 'inequality_index', 50):.0f}, conflict={getattr(ws, 'conflict_intensity', 0):.0f}.
Media/propaganda/repression: media={getattr(ws, 'media_saturation', 0):.0f}, propaganda={getattr(ws, 'propaganda_saturation', 0):.0f}, repression={getattr(ws, 'state_repression', 0):.0f}."""
    if civic:
        world_block += f"""
Civic soul: rootedness={civic.rootedness:.0f}, perceived_justice={civic.perceived_justice_order:.0f}, hierarchy_legitimacy={civic.hierarchy_legitimacy:.0f}, risk_band={civic.risk_band:.0f}."""

    # Symbolic lexicon (Rawlsing Section 6)
    symbols = state.symbols
    symbols_block = ""
    if symbols.salience or symbols.glosses:
        symbols_block = f"""
SYMBOLIC LEXICON (what matters to this person):
Salience: {symbols.salience}
Glosses: {symbols.glosses}"""

    # Relations (caregivers)
    rel_block = ""
    if state.relations and state.relations.nodes:
        nodes = list(state.relations.nodes.values())[:4]
        rel_summary = "; ".join(
            f"{n.role}: warmth={n.warmth:.0f} authority={n.authority:.0f}" + (f" type={n.enneagram_type}" if getattr(n, "enneagram_type", None) is not None else "")
            for n in nodes
        )
        rel_block = f"\nRELATIONS: {rel_summary}"

    # Thought rails
    tr = state.thought_rails
    thought_block = f"""
THOUGHT RAILS: authority={tr.authority_schema}, fairness={tr.fairness_schema}, self={tr.self_schema}"""
    if tr.threat_schema or tr.hope_schema:
        thought_block += f", threat={tr.threat_schema or '—'}, hope={tr.hope_schema or '—'}"

    # Enneagram shading
    enneagram_block = ""
    if profile and profile.primary_type:
        lost = LOST_MESSAGES.get(profile.primary_type, "")
        unconscious = UNCONSCIOUS_MESSAGES.get(profile.primary_type, "")
        health_riso = profile.metadata.get("health_level_riso", 5)
        key_terms = profile.metadata.get("health_key_terms", [])
        enneagram_block = f"""
ENNEAGRAM: Type {profile.primary_type} (wing {profile.wing or '?'}), health {health_riso}/9.
Key terms: {', '.join(key_terms) if key_terms else '—'}
Unconscious message: "{unconscious}"
Lost message: "{lost}"
"""

    # Cognitive / defenses
    cog = state.cognitive
    defense_block = f"\nDEFENSES: primary={cog.primary_defense}" + (f", secondary={cog.secondary_defense}" if cog.secondary_defense else "")

    prompt = f"""You are building this person's internal world—the full range of tangible detail that matters (Rawlsing v4.0).
This output feeds the next recursion. Digest what came before; add concrete texture. The user never sees this directly;
it is the iceberg beneath the persona who will later talk to them. Age {age}. Year {state.current_year}. Stage: {stage}.
{identity_block}
{indices_block}
{world_block}{rel_block}
NEEDS: {needs}
TOP STRATEGIES: {[k for k, _ in top_strategies]}
EVENTS THIS YEAR: {events_str}
{thought_block}{defense_block}
{symbols_block}
{enneagram_block}
{f'OUTLIER HINTS (use sparingly, only if plausible): {outlier_block}' if outlier_block else ''}

STAGE-SPECIFIC GUIDANCE ({stage}):
{stage_guidance}

ACCUMULATED LIFE SO FAR (what this person carries—the iceberg):
{accumulated_narrative if accumulated_narrative else "(birth / earliest years)"}

Generate tangible detail for this year. Include everything that matters: temperament, caregiver dynamics, micro-patterns, early atmosphere;
first symbols, relational stance, rules-and-power; inner monologue, fairness/shame logic, habits, moral atmosphere;
ideological exposure, identity kernel, role in systems; desires (concrete), persona strategies, defense patterns;
key experiences, symbolic recursion (early symbols reappearing), contradictions, subcultural/dialect texture.
Memories, traumas, ecstasies, pathologies, relationships—and whatever else shapes this person's internal world.
Focus on recursion, contradiction, plausible inner texture. No imposed arc or tidy resolution. Like a real person.

4–8 sentences. Build on the accumulated life. Each detail becomes part of the iceberg—stored, unstated, surfacing only when conversation touches it.

Optionally return an idea_delta (JSON) if a significant experience should compound into needs/strategies:
{{"idea_id": "...", "description": "...", "target_axes": {{"coherence_meaning": -10}}, "affect_valence": -20, "source_trust": 70}}."""
    return prompt


# ============================================================================
# v4.2 Recursion Delta Prompt (mechanism-first, additive, grounded)
# ============================================================================

RECURSION_DELTA_JSON_SCHEMA = '''
Return ONLY valid JSON in this shape. Do NOT copy the placeholder text below—it shows structure only.
Every tag/string you emit must be generated fresh for THIS person (their location, decade, religion, cohort).
Examples of the right kind of specificity: for Guatemala 1990s → "iglesia_catolica_vecindad", "mercado_central_conflicto"; for Vietnam → "chua_phat_lo_so"; for Germany → "kirche_dorf". Never use a real place or clergy from another context.

{
  "context": {"location": "<this person's place>", "decade": "...", "political_moment": [], "media_tech": [], "wvs_tags": []},
  "needs_delta": {"safety": 0, "belonging_group": 0, ...},
  "strategy_spikes": {"people_pleasing": 0, "activism_justice": 0, ...},
  "indices_delta": {"PI": 0, "DRTS": 0, "IAI": 0, "TT": 0, "AAF": 0, "RMT": 0, ...}  // REQUIRED: when events/drts_modifiers/outlier_triggers apply, set DRTS and/or IAI non-zero (e.g. {"DRTS": 8, "IAI": 3}). Never leave both 0 when the year warrants change.
  "identity_scripts": ["<generate script for this person>"],
  "symbols_added": ["<generate symbol for this place/time>"],
  "symbols_reinterpreted": [{"old": "<object>", "new": "<reinterpretation>"}],
  "moral_atmosphere_tags": ["<generate for this milieu>"],
  "speech_tics": ["<generate tic for this person>"],
  "subculture_tags": ["<generate group/place for THIS country and cohort>"],
  "events_hooks": ["<generate event for this place and year>"],
  "moral_loops": ["<e.g. I_am_only_good_if_...>"],
  "routines": ["<generate routine for this person>"],
  "thought_rail_updates": {"authority_schema": "...", "fairness_schema": "...", "self_schema": "..."},
  "language_experience": {"L1": "<from persona>", "L2": "", "education_years": 0, "media": "", "abstentions": []},
  "drts_modifiers": [],
  "outlier_triggers": [],
  "self_narrative": {},
  "drts_components": {},
  "roles_in_systems": ["<generate role for this person>"],
  "quirks": ["<generate quirk for this person>"],
  "authority_reception_patterns": [{"source": "<God|parents|state|institutions>", "stance": "<absorb|reject|intensify|...>", "influence": "<generate; clergy/authority type must match THIS religion>"}],
  "life_snapshot": {"job_type": "...", "commute_style": "...", "living_arrangement": "...", "family_obligations": "...", "income_stress": "...", "internet_access_patterns": "...", "social_circle_density": "...", "sleep_debt_baseline": "...", "current_life_phase": "..."},
  "narrative": "<REQUIRED: 3–6 sentences. Cover OPERATIVE ELEMENTS for this year so future recursions can build on them. First year (baby/infant): caregivers, household atmosphere, siblings if any, first attachments/routines. Every year (age-appropriate): family AND friends/peers, siblings, hobbies/passions, possible romance, trouble (scrapes, conflicts), teachers/school, broader culture (media, neighborhood). Specific events + how digested. Informs events_hooks, identity_scripts, indices_delta; keep consistent.>"
}
'''
# Life snapshot block injected when present-year recursion (see build_recursion_prompt_delta).
LIFE_SNAPSHOT_PROMPT_BLOCK = """
LIFE SNAPSHOT (present life only—output when this is the current/present year):
Below are DATA-DERIVED defaults from this person's identity, country, SES, urbanicity, needs, and indices. Use them as given UNLESS the narrative you generated for this year clearly contradicts one (e.g. they lost their job → job_type should be unemployed). For each field, you may only choose from the ALLOWED VALUES listed. Output a "life_snapshot" object with exactly these keys: job_type, commute_style, living_arrangement, family_obligations, income_stress, internet_access_patterns, social_circle_density, sleep_debt_baseline, current_life_phase.
"""

# DRTS modifiers (v3.4/v4.0): apply to indices_delta.DRTS when events match
DRTS_MODIFIER_RULES = """
DRTS modifiers (apply when events match):
  +5: repeated unfair rules, witnessed injustice
  +10: personal betrayal, state violence experienced directly
  +20: ideological fuel (chants, martyrs, theology, political theory, songs)
  -10: high dependency load (children, elders), fear of retaliation, fragile survival
  ±PI: high PI shifts DRTS shape—more options but more competing loyalties.
"""

# Outlier Engine (v3.4/v4.0): IAI, TT, AAF, RMT triggers
OUTLIER_ENGINE_RULES = """
Outlier Engine triggers (only when life-course plausibly supports):
  IAI≥70 + isolation → self-mythologizing, private creeds, fragmented social reality
  TT: DRTS≥60 + rejection + trauma → cruelty-as-order, moral inversion, dissociation
  AAF≥65 + creative capacity → mythopoetic resistance, artistic ritualization
  RMT≥80 + isolation/symbolic overload → pattern-seeking in random, time slippage, sacred/profane obsession
"""

# Mandatory: prevent model from leaving DRTS/IAI at 0 when the year warrants change
INDICES_DELTA_REQUIRED = """
INDICES_DELTA (required when events or modifiers apply):
- If EVENTS THIS YEAR include trauma, authority conflict, institutional exposure, injustice, or political/social rupture—OR if you output any drts_modifiers or outlier_triggers—you MUST set at least one of indices_delta.DRTS or indices_delta.IAI to a non-zero value (typical magnitude ±5 to ±20). Leaving both DRTS and IAI at 0 in such years is invalid.
- DRTS: defiance/revolutionary tendency shift (use DRTS modifiers above for magnitude).
- IAI: ideological/identity crystallization shift (use when outlier triggers or authority/ideology events apply).
- Quiet years with no such events: indices_delta may be all zeros. Otherwise: non-zero DRTS and/or IAI is required, not optional.
"""


def build_recursion_prompt_delta(
    state: PersonaState,
    age: int,
    events: List[LifeEvent],
    history: List[PersonaState],
    palimpsest: Optional[Palimpsest],
    world_slice: WorldSlice,
    driver_vec: Optional[DriverVector],
    data_derived_life_snapshot: Optional[Dict[str, Any]] = None,
    valid_options_life_snapshot: Optional[Dict[str, List[str]]] = None,
    parent_birth_context: Optional[str] = None,
    local_modifiers: Optional["LocalModifiers"] = None,
    accumulated_narrative: Optional[str] = None,
) -> str:
    """
    Build prompt for v4.2 delta recursion. Output is structured JSON (RecursionDelta).
    accumulated_narrative: narrative so far (birth + prior years). Model should progress it with a short
      yearly narrative; that narrative informs events_hooks, identity_scripts, indices_delta, etc.
    """
    stage = _get_rawlsing_stage_for_age(age)
    stage_guidance = RAWLSING_STAGE_GUIDANCE.get(stage, RAWLSING_STAGE_GUIDANCE["17+"])
    id_ = state.identity
    year = state.current_year

    grounded = get_grounded_context(
        year=year,
        country_code=id_.country_code,
        locality=id_.locality or id_.region or "",
        world_slice=world_slice,
        driver_vec=driver_vec,
    )
    grounded_text = format_grounded_context_for_prompt(grounded)

    # Persona-identity specifics (time/place/milieu—draw from these, not generic placeholders)
    birth_year = state.current_year - age
    persona_block = f"""
PERSONA IDENTITY (use these specifics—all output tags must reflect THIS person's milieu):
Name: {id_.given_name} {id_.family_name or ''}
Location: {id_.locality or id_.region or id_.country_code}, {id_.country_code}. Born {birth_year}.
Gender: {id_.gender}. SES: {id_.current_class}. Urbanicity: {id_.urbanicity}.
Religion: {id_.current_religion or id_.childhood_religion or '—'}. Religiosity: {id_.religiosity_level:.0f}/100.
Ethnicity: {id_.ethnicity_label or '—'}. Minority status: {id_.minority_status}.
Languages: {id_.primary_language}; {', '.join(id_.secondary_languages) if id_.secondary_languages else '—'}.
Class origin: {id_.class_origin}. Identity notes: {id_.identity_notes or '—'}."""

    # Enneagram shading (type/health/worldview filtering) for v4.2 deltas
    profile = state.enneagram
    enneagram_block = ""
    if profile and profile.primary_type:
        lost = LOST_MESSAGES.get(profile.primary_type, "")
        unconscious = UNCONSCIOUS_MESSAGES.get(profile.primary_type, "")
        health_riso = profile.metadata.get("health_level_riso", 5)
        key_terms = profile.metadata.get("health_key_terms", [])
        enneagram_block = f"""

ENNEAGRAM (type shading—let this color needs/strategies/scripts):
Type {profile.primary_type} (wing {profile.wing or '?'}), health {health_riso}/9.
Key terms: {', '.join(key_terms) if key_terms else '—'}
Unconscious message: "{unconscious}"
Lost message: "{lost}"
"""

    events_str = ", ".join(e.type for e in events) if events else "none"
    needs = {k: v for k, v in state.needs.__dict__.items() if not k.startswith("_")}
    strategies = {k: v for k, v in state.strategies.__dict__.items() if not k.startswith("_") and k != "extra"}
    top_strategies = sorted(strategies.items(), key=lambda x: x[1], reverse=True)[:5]
    idx = state.indices

    palimpsest_summary = ""
    if palimpsest:
        scripts = [l.value for l in palimpsest.identity_scripts_history[-15:]]
        symbols = [l.value for l in palimpsest.symbols_history[-10:]]
        tics = [l.value for l in palimpsest.speech_tics_history[-8:]]
        routines = [l.value for l in palimpsest.routines_history[-5:]]
        roles = [l.value for l in palimpsest.roles_in_systems_history[-5:]]
        quirks = [l.value for l in palimpsest.quirks_history[-5:]]
        subcultures = [l.value for l in palimpsest.subculture_history[-12:]]
        auth_rec = palimpsest.authority_reception_history[-3:] if palimpsest.authority_reception_history else []
        drts_comp = palimpsest.drts_components_history[-1] if palimpsest.drts_components_history else {}
        palimpsest_summary = f"""
ACCUMULATED LAYERS SO FAR (never overwrite—only add; build on these with greater specificity):
identity_scripts: {scripts}
symbols: {symbols}
speech_tics: {tics}
routines: {routines}
roles_in_systems: {roles}
quirks: {quirks}
subculture_tags: {subcultures}
drts_components: {drts_comp}
authority_reception_patterns: {auth_rec}

Do NOT repeat these verbatim. Prefer NEW entries or MORE SPECIFIC variants that build on what exists (e.g. family_support_primary_caretaker instead of family_support again; rubs_eyes_when_sleepy_and_stressed; identity_script that deepens or contradicts an existing one). Add nuance, not duplicates.
"""

    tr = state.thought_rails
    thought_rails_str = f"authority={tr.authority_schema}, fairness={tr.fairness_schema}, self={tr.self_schema}"

    parent_block = ""
    if parent_birth_context and (parent_birth_context or "").strip():
        parent_block = f"""
STORY THE CHILD WAS BORN INTO (who the parents are—use this to imagine how they react to events, discipline, warmth, transgression):
{parent_birth_context.strip()}

Generate events and internalization that fit THESE parents. E.g. a small transgression (cookie, lie, defiance): how would THIS father and THIS mother react? How does the child internalize it (authority_reception_patterns, thought_rail_updates, identity_scripts, moral_loops)? Set indices_delta to reflect that: harsh/internalized authority → IAI or TT; rebellion or defiance → DRTS; compliance or guilt → IAI/lower DRTS as appropriate.
"""
    # Family ↔ Community ↔ Hegemony: where the household sits and where defiance/identification go
    hegemony_block = ""
    if driver_vec and id_:
        ethnic_power = "dominant"
        if local_modifiers:
            ethnic_power = getattr(local_modifiers, "ethnic_power_status", None) or id_.minority_status or "dominant"
        else:
            ethnic_power = getattr(id_, "minority_status", None) or "dominant"
        community_precarity = str(ethnic_power).lower() in ("minoritized", "mixed", "unclear")
        auth_egal = getattr(driver_vec, "authoritarian_vs_egalitarian", 50)
        individualist = getattr(driver_vec, "individualism_vs_collectivism", 50)
        mainstream_egalitarian = auth_egal < 55
        mainstream_individualist = individualist > 45
        hegemony_offers_escape = not community_precarity and (mainstream_egalitarian or mainstream_individualist)
        hegemony_block = f"""
FAMILY ↔ COMMUNITY ↔ HEGEMONY (tension between three layers—direct where defiance and identification go):
- Derived for this persona: community_precarity={community_precarity} (ethnic power: {ethnic_power}); hegemony_offers_escape={hegemony_offers_escape} (mainstream is egalitarian/individualist enough to offer an alternative to strict parents).
- When COMMUNITY is precarious: neighborhood/group shares norms; child may normalize strict parents (everyone's like that). Later the child may appreciate and identify WITH parents/community; direct defiance (DRTS) and ideological crystallization (IAI) at the HEGEMONY (state, dominant group), not at the family. authority_reception: parents/community → absorb or intensify; state/hegemony → reject or resist.
- When DOMINANT + hegemony_offers_escape: strict parents vs. a mainstream that offers freedom. Child may rebel against parents and identify with hegemony; DRTS may target family or take mainstream-visible forms; authority_reception: parents → reject/resist; state or mainstream → absorb. Moral loops and identity_scripts should reflect this direction (e.g. "I am only good if I escape their rules" vs. "I am only good if we hold together against them").
- Generate events, authority_reception_patterns, and indices_delta so the TARGET of defiance/identification (family vs. hegemony) matches this geometry.
"""
    # Narrative so far: so the model can progress the story (each recursion builds on prior years)
    narrative_so_far_block = ""
    _max_narrative_chars = 2800
    _is_first_narrative_year = not (accumulated_narrative and (accumulated_narrative or "").strip() and len((accumulated_narrative or "").strip()) > 200)
    if accumulated_narrative and (accumulated_narrative or "").strip():
        excerpt = (accumulated_narrative.strip()[-_max_narrative_chars:] if len(accumulated_narrative) > _max_narrative_chars else accumulated_narrative.strip())
        if len(accumulated_narrative) > _max_narrative_chars:
            excerpt = "... (earlier years omitted)\n\n" + excerpt
        narrative_so_far_block = f"""
NARRATIVE SO FAR (past years—your output will append to this; progress the story):
{excerpt}

Write a short yearly "narrative" (3–6 sentences) for THIS year that:
- Covers OPERATIVE ELEMENTS so future recursions can push off them. First year (baby/infant): caregivers, household atmosphere, siblings if any, first attachments and routines. Later years: build on those and add—where age-appropriate—friends/peers, siblings, hobbies and passions, possible romance, trouble (scrapes, conflicts, ordinary risk), influence of teachers and school, broader culture (media, neighborhood, religion outside home). This + flow across years is where change and emergence come from.
- Includes SPECIFIC events from context (e.g. father job change; started kindergarten; first close friend; a teacher who mattered; a hobby or crush; a scrape with rules or peers). Draw from parent_birth_context, SES, family ↔ community ↔ hegemony, and life stage.
- Describes how those events were digested: atmosphere, emotional bandwidth, how they absorbed it (or didn't). Keep narrative consistent with events_hooks, identity_scripts, authority_reception_patterns, moral_loops, indices_delta.
- Progress the story: reference or extend what came before; introduce new elements; do not repeat the same beats.
"""
    if _is_first_narrative_year:
        narrative_so_far_block = (narrative_so_far_block or "").strip() + """

FIRST NARRATIVE YEAR (baby/infant): This is the first yearly layer. Establish who is around (primary caregivers, siblings if any), household atmosphere, first attachments and routines. These become the operative elements that later years will build on—then peers, school, hobbies, romance, trouble, teachers, and culture will layer in."""
    life_snapshot_block = ""
    if data_derived_life_snapshot and valid_options_life_snapshot:
        life_snapshot_block = LIFE_SNAPSHOT_PROMPT_BLOCK + "\nDATA-DERIVED DEFAULTS (use unless narrative contradicts):\n" + str(data_derived_life_snapshot) + "\nALLOWED VALUES per field (pick only from these):\n" + str(valid_options_life_snapshot) + "\n"

    # Hard anti-drift guardrails: stop the model from injecting other cities/religious offices.
    rel_label = (id_.current_religion or id_.childhood_religion or "—").strip()
    drift_guard = f"""
ANTI-DRIFT CONSTRAINTS (obey strictly):
- Do NOT introduce other locations/cities/countries. If you name a place, it must be in/near: {id_.locality or id_.region or id_.country_code}, {id_.country_code}.
- Do NOT import US-specific subcultures, organizations, or city-tags (e.g. \"oakland_…\", \"brooklyn_…\") unless the location is explicitly in the United States.
- Religious authority terms MUST match this persona’s religion: {rel_label}.
  - Christianity → priest/pastor/church (NOT imam).
  - Islam → imam/mosque (NOT priest).
  - Buddhism → monk/temple (NOT imam/priest).
  - If religion is unknown/none, keep authority sources generic (\"religious_authority\") and avoid specific clergy titles.
- If you are tempted to use a generic meme tag from another country (e.g. \"oakland_activist\"), STOP and instead generate a local equivalent for {id_.country_code} or omit it.
- Do NOT copy example tokens from the schema; generate locally grounded equivalents for this person's place, time, and religion.
"""

    return f"""You are building ONE LAYER of this person's development. Age {age}. Year {year}. Stage: {stage}.

RAWLSING v4.2: Additive recursion. You ADD to what exists. Nothing overwrites. The persona is a palimpsest—each year adds complexity, contradictions, new scripts. If indices/needs shift noticeably, include self_narrative: how they imperfectly tell themselves about the change.
{parent_block}
{hegemony_block}
{narrative_so_far_block}

{DRTS_MODIFIER_RULES}

{OUTLIER_ENGINE_RULES}
{persona_block}
{enneagram_block}
{drift_guard}

TIME/PLACE/MILIEU (grounded in data):
{grounded_text}

CURRENT STATE:
NEEDS: {needs}
TOP STRATEGIES: {[k for k, _ in top_strategies]}
INDICES: PI={idx.permeability_index:.0f} DRTS={idx.drts:.0f} IAI={idx.iai:.0f} TT={idx.transgression_threshold:.0f} AAF={idx.aesthetic_amplification:.0f} RMT={idx.recursive_madness_threshold:.0f}
THOUGHT RAILS: {thought_rails_str}
EVENTS THIS YEAR: {events_str}
{INDICES_DELTA_REQUIRED}
{palimpsest_summary}

STAGE GUIDANCE: {stage_guidance}

REQUIREMENTS:
- narrative: REQUIRED. 3–6 sentences for this year with specific events (e.g. father job change given his traits; started school after years with mom—structure/anxiety). How each was digested (atmosphere, how the kid absorbed it). This narrative informs and must be consistent with events_hooks, identity_scripts, authority_reception_patterns, needs_delta, indices_delta.
- indices_delta: Must reflect what happened this year. When you describe events, authority_reception_patterns, or thought_rail_updates (e.g. how parents reacted to a transgression, what the child internalized), set DRTS/IAI/TT accordingly: harsh or internalized authority → IAI or TT; rebellion/defiance → DRTS; compliance or guilt → IAI or lower DRTS. Do not leave all zero when you have generated internalization or parent-related events.
- Apply DRTS modifiers when events match: record drts_modifiers used.
- If Outlier Engine triggers apply, record outlier_triggers and adjust indices_delta.
- routines: daily rituals that BOTH reinforce AND undermine stated beliefs (Section 9).
- thought_rail_updates: how authority/fairness/self schema shifted this year.
- language_experience: L1/L2/L3, education_years, media (radio_only, limited_internet, etc.), abstentions.
- drts_components: emergent profile beyond scalar DRTS—latent, activated, suppressed, rewired, or persona-specific components. Extensible.
- roles_in_systems: role in peer/family/school—scapegoat, negotiator, ghost, confidant, enforcer, etc. Extensible; multiple roles across contexts.
- quirks: bodily/behavioral micro-patterns distinct from identity_scripts—e.g. rubs_ears_when_overstimulated, freezes_at_loud_voices, traces_spiral_to_calm.
- authority_reception_patterns: how different authority sources (God, parents, state, institutions) land—absorb, reject, intensify, transform, cling. Influenced by many factors: caregivers, trauma, disillusionment, institutions. Examples: disillusionment_with_human_authority → cling_to_God; reject_God → cling_to_secular; trauma_from_parents → resist_religion. Extensible—these are beginnings of possibility, not an exhaustive schema.
{life_snapshot_block}
Return ONLY valid JSON matching this schema. Before returning: if events/modifiers/triggers apply this year, indices_delta must include non-zero DRTS and/or IAI.
SPECIFICITY & WORLD KNOWLEDGE:
- Use your full world knowledge of this time/place to name concrete movements, institutions, media, idioms, and routines that are PLAUSIBLE for this identity + context.
- All tags must reflect THIS person's time/place/milieu—use their locality, religion, ethnicity, class position, and cohort (e.g. "hanoi_2004_student_protest" not "activism_event"; "buddhist_guilt_morning" not "moral_loop").
Include self_narrative when indices/needs/strategies shifted meaningfully.
{RECURSION_DELTA_JSON_SCHEMA}
"""


def _sanitize_palimpsest_strings_for_identity(
    values: List[str],
    country_code: str,
    religion_label: str,
) -> List[str]:
    """
    Drop obvious context-drift tokens (e.g. oakland_*) and obvious clergy mismatch markers (e.g. imams for Christianity).
    This is a pragmatic backstop for LLM leakage; primary defense is prompt constraints.
    """
    if not values:
        return []
    cc = (country_code or "").upper().strip()
    rel = (religion_label or "").lower().strip()
    geo_blacklist = ["oakland", "brooklyn", "manhattan", "san_francisco", "los_angeles", "nyc"]
    out: List[str] = []
    for v in values:
        if not v:
            continue
        s = str(v).strip()
        low = s.lower()
        # Geo leakage: drop US city-tags unless persona is US
        if cc not in ("US", "USA") and any(g in low for g in geo_blacklist):
            continue
        # Clergy mismatch: drop imam-language for non-Islam personas
        if "imam" in low and ("islam" not in rel and "muslim" not in rel):
            continue
        out.append(s)
    return out


def _sanitize_authority_reception_patterns_for_identity(
    patterns: List[Dict[str, Any]],
    religion_label: str,
) -> List[Dict[str, Any]]:
    """Drop/normalize obvious mismatches in authority reception patterns."""
    if not patterns:
        return []
    rel = (religion_label or "").lower().strip()
    out: List[Dict[str, Any]] = []
    for p in patterns:
        if not isinstance(p, dict):
            continue
        p2 = dict(p)
        influence = str(p2.get("influence", "") or "")
        low = influence.lower()
        if "imam" in low and ("islam" not in rel and "muslim" not in rel):
            # Replace with a Christian-generic equivalent instead of keeping an imam reference
            p2["influence"] = influence.replace("imams", "pastors").replace("imam", "pastor")
        out.append(p2)
    return out


def _coerce_life_snapshot_to_allowed_values(
    snap: Any,
    valid_options: Dict[str, List[str]],
    data_derived_defaults: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Enforce data-governed life_snapshot taxonomy:
    - if LLM output value not in allowed list, fall back to data_derived default (or first allowed).
    """
    if not isinstance(snap, dict):
        snap = {}
    out = dict(snap)
    for k, allowed in (valid_options or {}).items():
        if not allowed:
            continue
        v = out.get(k)
        if v is None:
            out[k] = data_derived_defaults.get(k, allowed[0])
            continue
        sv = str(v).strip()
        if sv not in allowed:
            out[k] = data_derived_defaults.get(k, allowed[0])
        else:
            out[k] = sv
    return out


def _normalize_self_narrative(val: Any) -> Dict[str, str]:
    """Ensure self_narrative is a dict (axis -> narrative). LLM sometimes returns a string."""
    if val is None:
        return {}
    if isinstance(val, dict):
        return {str(k): str(v) for k, v in val.items()}
    if isinstance(val, str):
        return {"narrative": val.strip()} if val.strip() else {}
    return {}


def _delta_narrative_fallback(delta: "RecursionDelta") -> str:
    """One-line summary for iceberg when delta has no narrative prose (e.g. API returns JSON only)."""
    loc = (delta.context or {}).get("location", "")
    decade = (delta.context or {}).get("decade", "")
    parts = [f"Age {delta.age}"]
    if loc or decade:
        parts.append(f"({loc or ''}{', ' if loc and decade else ''}{decade})".strip(" ,"))
    scripts = (delta.identity_scripts or [])[:2]
    hooks = (delta.events_hooks or [])[:2]
    if scripts:
        parts.append("scripts: " + ", ".join(scripts))
    if hooks:
        parts.append("events: " + ", ".join(hooks))
    return ". ".join(parts).strip(". ") or f"Age {delta.age} (structured delta)."


def parse_recursion_delta(raw: str, age: int, year: int) -> Optional[RecursionDelta]:
    """Parse LLM output as RecursionDelta. Returns None if parse fails."""
    import json
    raw = raw.strip()
    # Try to extract JSON (handle markdown code blocks)
    if "```" in raw:
        start = raw.find("```")
        if start >= 0:
            rest = raw[start + 3:]
            if rest.startswith("json"):
                rest = rest[4:]
            end = rest.find("```")
            raw = rest[:end] if end >= 0 else rest
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return RecursionDelta(
        age=age,
        year=year,
        context=obj.get("context", {}),
        needs_delta=obj.get("needs_delta", {}),
        strategy_spikes=obj.get("strategy_spikes", {}),
        indices_delta=obj.get("indices_delta", {}),
        identity_scripts=obj.get("identity_scripts", []),
        symbols_added=obj.get("symbols_added", []),
        symbols_reinterpreted=obj.get("symbols_reinterpreted", []),
        moral_atmosphere_tags=obj.get("moral_atmosphere_tags", []),
        speech_tics=obj.get("speech_tics", []),
        subculture_tags=obj.get("subculture_tags", []),
        events_hooks=obj.get("events_hooks", []),
        moral_loops=obj.get("moral_loops", []),
        routines=obj.get("routines", []),
        thought_rail_updates=obj.get("thought_rail_updates", {}),
        language_experience=obj.get("language_experience", {}),
        drts_modifiers=obj.get("drts_modifiers", []),
        outlier_triggers=obj.get("outlier_triggers", []),
        self_narrative=_normalize_self_narrative(obj.get("self_narrative")),
        drts_components=obj.get("drts_components", {}),
        roles_in_systems=obj.get("roles_in_systems", []),
        quirks=obj.get("quirks", []),
        authority_reception_patterns=obj.get("authority_reception_patterns", []),
        life_snapshot=obj.get("life_snapshot", {}),
        narrative=obj.get("narrative"),
    )


def _infer_indices_delta_from_delta_content(delta: "RecursionDelta") -> Dict[str, float]:
    """
    Infer DRTS/IAI/TT deltas from the delta's narrative content so parent reactions and
    internalization drive indices when the LLM left indices_delta at zero.
    """
    out: Dict[str, float] = {}
    auth = getattr(delta, "authority_reception_patterns", None) or []
    tr = getattr(delta, "thought_rail_updates", None) or {}
    scripts = getattr(delta, "identity_scripts", None) or []
    loops = getattr(delta, "moral_loops", None) or []
    for entry in auth:
        if not isinstance(entry, dict):
            continue
        source = (entry.get("source") or "").lower()
        stance = (entry.get("stance") or "").lower()
        if "parent" in source or source == "parents":
            if stance in ("reject", "resist", "defy"):
                out["DRTS"] = out.get("DRTS", 0) + 4.0
            if stance in ("absorb", "intensify", "cling", "internalize"):
                out["IAI"] = out.get("IAI", 0) + 3.0
            if stance in ("reject", "resist") and "authority" in str(entry.get("influence", "")).lower():
                out["TT"] = out.get("TT", 0) - 2.0
    if tr.get("authority_schema") and isinstance(tr.get("authority_schema"), str):
        s = tr["authority_schema"].lower()
        if any(w in s for w in ("harsh", "strict", "punish", "obey", "rule")):
            out["IAI"] = out.get("IAI", 0) + 2.0
            out["TT"] = out.get("TT", 0) + 1.0
        if any(w in s for w in ("reject", "unfair", "resist")):
            out["DRTS"] = out.get("DRTS", 0) + 3.0
    if scripts or loops:
        combined = " ".join(str(x) for x in (list(scripts) if scripts else []) + (list(loops) if loops else [])).lower()
        if any(w in combined for w in ("guilt", "only good if", "obey", "please")):
            out["IAI"] = out.get("IAI", 0) + 2.0
    return out


def apply_recursion_delta_to_state(state: PersonaState, delta: RecursionDelta) -> PersonaState:
    """Apply RecursionDelta to PersonaState: update needs, strategies, indices."""
    needs = NeedGradients(**{k: v for k, v in state.needs.__dict__.items() if not k.startswith("_")})
    for k, dv in delta.needs_delta.items():
        if hasattr(needs, k):
            setattr(needs, k, max(0, min(100, getattr(needs, k) + dv)))

    strategies = StrategyPortfolio(**{k: v for k, v in state.strategies.__dict__.items() if not k.startswith("_") and k != "extra"})
    for k, dv in delta.strategy_spikes.items():
        if hasattr(strategies, k):
            setattr(strategies, k, max(0, min(100, getattr(strategies, k) + dv)))

    indices = Indices(**{k: v for k, v in state.indices.__dict__.items() if not k.startswith("_")})
    INDICES_KEY_MAP = {"PI": "permeability_index", "DRTS": "drts", "IAI": "iai", "TT": "transgression_threshold", "AAF": "aesthetic_amplification", "RMT": "recursive_madness_threshold"}
    idelta = dict(delta.indices_delta) if delta.indices_delta else {}
    inferred = _infer_indices_delta_from_delta_content(delta)
    for k, dv in inferred.items():
        if idelta.get(k, 0) == 0 and dv != 0:
            idelta[k] = dv
    for k, dv in idelta.items():
        attr = INDICES_KEY_MAP.get(k, k)
        if hasattr(indices, attr):
            setattr(indices, attr, max(0, min(100, getattr(indices, attr) + dv)))
    # Fallback: when the model reports modifiers/triggers but left indices_delta at 0, nudge so DRTS/IAI move
    if getattr(delta, "drts_modifiers", None) and delta.indices_delta.get("DRTS", 0) == 0 and not inferred.get("DRTS"):
        indices.drts = max(0, min(100, indices.drts + 5.0))
    if getattr(delta, "outlier_triggers", None) and delta.indices_delta.get("IAI", 0) == 0 and not inferred.get("IAI"):
        indices.iai = max(0, min(100, indices.iai + 5.0))
    has_activity = bool(delta.events_hooks or delta.roles_in_systems)
    if has_activity and delta.indices_delta.get("DRTS", 0) == 0 and not inferred.get("DRTS"):
        indices.drts = max(0, min(100, indices.drts + 3.0))
    if has_activity and delta.indices_delta.get("IAI", 0) == 0 and not inferred.get("IAI"):
        indices.iai = max(0, min(100, indices.iai + 2.0))
    if (delta.thought_rail_updates or has_activity) and delta.indices_delta.get("TT", 0) == 0 and not inferred.get("TT"):
        indices.transgression_threshold = max(0, min(100, indices.transgression_threshold + 2.0))

    # Apply thought_rail_updates if present
    thought_rails = state.thought_rails
    if delta.thought_rail_updates:
        tr_dict = {
            "authority_schema": thought_rails.authority_schema,
            "fairness_schema": thought_rails.fairness_schema,
            "self_schema": thought_rails.self_schema,
            "other_groups_schema": dict(thought_rails.other_groups_schema) if thought_rails.other_groups_schema else {},
            "threat_schema": thought_rails.threat_schema,
            "hope_schema": thought_rails.hope_schema,
            "tags": dict(thought_rails.tags) if thought_rails.tags else {},
        }
        for tr_key, tr_val in delta.thought_rail_updates.items():
            if tr_key in tr_dict and isinstance(tr_val, str):
                tr_dict[tr_key] = tr_val
        thought_rails = ThoughtRails(**tr_dict)

    # Merge delta events/roles into micrograph so band summaries get key_events
    base_micrograph = getattr(state, "micrograph", None) or RelationalMicrograph()
    if delta.events_hooks or delta.roles_in_systems:
        key_events = list(base_micrograph.key_events)
        key_events.extend(delta.events_hooks)
        for r in delta.roles_in_systems:
            key_events.append(f"role:{r}")
        new_micrograph = replace(base_micrograph, key_events=key_events)
        return replace(state, needs=needs, strategies=strategies, indices=indices, thought_rails=thought_rails, micrograph=new_micrograph)

    return replace(state, needs=needs, strategies=strategies, indices=indices, thought_rails=thought_rails)


# ============================================================================
# Temporal Systems: Next Day (Section 8)
# ============================================================================

NEXT_DAY_JSON_SCHEMA = '''
{
  "gesture_shift": "slower blink, faster speech when nervous",
  "dream_intrusion": "water flowing backwards, a recurring face",
  "feeling_shift": "slightly softened toward X, hardened toward Y",
  "event_context": "brief description of what triggered this"
}
'''


def build_next_day_prompt(state: PersonaState, event: str) -> str:
    """
    Build prompt for Next Day Trigger (v3.4/v4.0 Section 8).
    After a key event, generate fine-grain snapshot: gesture, dream, feeling shift.
    """
    return f"""Next Day Trigger. This person just experienced: {event}.

Show how the previous day left imprinted. Return ONLY valid JSON:
- gesture_shift: a gesture that changed or solidified (e.g. slower blink, faster speech)
- dream_intrusion: a dream or intrusive image (e.g. water flowing backwards, recurring face)
- feeling_shift: micro shift in feeling or belief (slightly softened, hardened, confused)

{NEXT_DAY_JSON_SCHEMA}"""


def parse_next_day_snapshot(raw: str) -> Optional[NextDaySnapshot]:
    """Parse LLM output as NextDaySnapshot."""
    import json
    raw = raw.strip()
    if "```" in raw:
        start = raw.find("```")
        if start >= 0:
            rest = raw[start + 3:]
            if rest.startswith("json"):
                rest = rest[4:]
            end = rest.find("```")
            raw = rest[:end] if end >= 0 else rest
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError:
        return None
    return NextDaySnapshot(
        gesture_shift=obj.get("gesture_shift", ""),
        dream_intrusion=obj.get("dream_intrusion", ""),
        feeling_shift=obj.get("feeling_shift", ""),
        event_context=obj.get("event_context", ""),
    )


def simulate_next_day(
    state: PersonaState,
    event: str,
    llm_callback: Callable[[PersonaState, str], str],
) -> Optional[NextDaySnapshot]:
    """
    Next Day Trigger: after key event, get fine-grain snapshot.
    Calls llm_callback with build_next_day_prompt; parses result.
    """
    prompt = build_next_day_prompt(state, event)
    raw = llm_callback(state, prompt)
    return parse_next_day_snapshot(raw) if isinstance(raw, str) else parse_next_day_snapshot(getattr(raw, "narrative", "") or "")


# ============================================================================
# LLM INTERFACE (from 05—implementation.md)
# ============================================================================


def build_persona_sheet(history: PersonaHistory) -> Dict[str, Any]:
    """
    Build persona sheet for LLM (from 05—implementation.md).
    Condenses all bands into a JSON-like payload for worldview-contained narrative generation.
    If the simulation ran with llm_callback, final_state.narrative_snapshot holds the accumulated
    iceberg (memories, traumas, ecstasies, pathologies)—included as backstory for conversation.
    """
    if not getattr(history, "yearly_states", None):
        raise ValueError("PersonaHistory.yearly_states is empty; cannot build persona sheet.")
    final_state = history.yearly_states[-1]
    
    # Build band-level summaries; enrich key_events from palimpsest by age range
    band_data = []
    for band in history.band_summaries:
        # Get top strategies
        strategy_weights = [
            (k, getattr(band.strategies, k))
            for k in band.strategies.__dict__.keys()
            if not k.startswith("_") and k != "extra"
        ]
        top_strategies = sorted(strategy_weights, key=lambda x: x[1], reverse=True)[:3]

        key_events = list(band.micrograph.key_events) if band.micrograph else []
        if history.palimpsest:
            band_def = next((b for b in AGE_BANDS if b["label"] == band.band), None)
            if band_def:
                age_min, age_max = band_def["start"], band_def["end"]
                for layer in history.palimpsest.events_hooks_history:
                    if age_min <= layer.age < age_max:
                        key_events.append(layer.value)
                for layer in history.palimpsest.roles_in_systems_history:
                    if age_min <= layer.age < age_max:
                        key_events.append(f"role:{layer.value.strip()}")
        # Dedupe key_events: normalize "role: x" / "role:x" to same key so no space-variant duplicates
        def _norm_role_key(e: str) -> str:
            s = (e or "").strip()
            if s.lower().startswith("role:"):
                return "role:" + s[5:].strip().lower()
            return s.lower()
        seen_events = set()
        deduped = []
        for e in key_events:
            k = _norm_role_key(e)
            if k not in seen_events:
                seen_events.add(k)
                deduped.append(e)
        key_events = deduped
        if not key_events:
            country = getattr(history.identity, "country_code", "") or "this place"
            key_events = [_band_default_key_event(band.band, country)]

        tr = band.thought_rails
        def _rail(v):
            return v if (v and str(v).strip() and str(v).lower() != "unknown") else "—"
        band_data.append({
            "age_band": getattr(band, "band", ""),
            "age_range": str(getattr(band, "age", 0)),
            "needs": {
                "safety": band.needs.safety,
                "warmth_bonding": band.needs.warmth_bonding,
                "belonging_group": band.needs.belonging_group,
                "recognition_status": band.needs.recognition_status,
                "coherence_meaning": band.needs.coherence_meaning,
                "transcendence_sacred": band.needs.transcendence_sacred
            },
            "top_strategies": [k for k, _ in top_strategies],
            "indices": {
                "PI": band.indices.permeability_index,
                "DRTS": band.indices.drts,
                "IAI": band.indices.iai,
                "RMT": band.indices.recursive_madness_threshold
            },
            "micrograph": {
                "caregivers": [node.__dict__ for node in (band.micrograph.caregivers if band.micrograph else [])],
                "peers": [node.__dict__ for node in (band.micrograph.peers if band.micrograph else [])],
                "institutions": [node.__dict__ for node in (band.micrograph.institutions if band.micrograph else [])],
                "key_events": key_events,
                "norm_conflicts": band.micrograph.norm_conflicts if band.micrograph else []
            },
            "thought_rails": {
                "authority_schema": _rail(getattr(tr, "authority_schema", None)),
                "fairness_schema": _rail(getattr(tr, "fairness_schema", None)),
                "self_schema": _rail(getattr(tr, "self_schema", None)),
                "other_groups_schema": _ensure_dict(getattr(tr, "other_groups_schema", None))
            }
        })

    id_filled = _fill_persona_identity(history.identity)
    sheet = {
        "identity": id_filled,
        "bands": band_data,
        "current_state": {
            "needs": {k: v for k, v in final_state.needs.__dict__.items() if not k.startswith("_")},
            "strategies": {k: v for k, v in final_state.strategies.__dict__.items() if not k.startswith("_") and k != "extra"},
            "indices": {k: v for k, v in final_state.indices.__dict__.items() if not k.startswith("_")},
            "thought_rails": _thought_rails_for_sheet(final_state.thought_rails),
            "civic_soul": _civic_soul_for_sheet(getattr(final_state, "world", None)),
        },
        "enneagram": {
            "primary_type": final_state.enneagram.primary_type,
            "wing": final_state.enneagram.wing,
            "health_level": final_state.enneagram.health_level,
            "stack": final_state.enneagram.stack
        } if getattr(final_state, "enneagram", None) else None,
        "symbols": _symbols_for_sheet(getattr(final_state, "symbols", None)),
        "backstory": final_state.narrative_snapshot or "",
        "metadata": history.metadata
    }
    if history.metadata.get("parent_names"):
        sheet["parents"] = history.metadata["parent_names"]
    if history.palimpsest:
        palimpsest_symbols = [l.value for l in history.palimpsest.symbols_history]
        if palimpsest_symbols:
            sheet["symbols"]["salience"] = list(sheet["symbols"]["salience"]) + palimpsest_symbols
        for r in history.palimpsest.symbols_reinterpretations:
            old_k, new_v = r.get("old"), r.get("new")
            if old_k is not None and new_v is not None:
                sheet["symbols"]["glosses"][old_k] = new_v
        sheet["voice_profile"] = history.palimpsest.get_voice_profile()
        sheet["life_snapshot"] = dict(history.palimpsest.life_snapshot) if history.palimpsest.life_snapshot else {}
        _ensure_life_snapshot_has_defaults(sheet, id_filled)
        # Dedupe so sheet/chat see each script/role/quirk once (order-preserving)
        p = history.palimpsest
        sheet["palimpsest"] = {
            "identity_scripts": p._dedupe_list([l.value for l in p.identity_scripts_history]),
            "symbols": p._dedupe_list([l.value for l in p.symbols_history]),
            "speech_tics": p._dedupe_list([l.value for l in p.speech_tics_history]),
            "moral_loops": p._dedupe_list([l.value for l in p.moral_loops_history]),
            "routines": p._dedupe_list([l.value for l in p.routines_history]),
            "moral_atmosphere": p._dedupe_list([l.value for l in p.moral_atmosphere_history]),
            "subculture_tags": p._dedupe_list([l.value for l in p.subculture_history]),
            "drts_components": p.drts_components_history[-1] if p.drts_components_history else {},
            "roles_in_systems": p._dedupe_list([l.value for l in p.roles_in_systems_history]),
            "quirks": p._dedupe_list([l.value for l in p.quirks_history]),
            "authority_reception_patterns": p.authority_reception_history,
        }
    if not sheet["symbols"]["salience"]:
        sheet["symbols"]["salience"] = ["everyday_life"]
    if sheet["symbols"]["glosses"] is None:
        sheet["symbols"]["glosses"] = {}
    return sheet


def build_conversation_persona_context(
    history: PersonaHistory,
    include_life_layer: bool = False,
    date: Optional[str] = None,
    scenario_reason: Optional[str] = None,
    rng: Any = None,
    chat_relation_mode: str = "generated_persona",
) -> Any:
    """
    Build system-prompt context for the persona in conversation mode.
    Includes identity, Enneagram, and the full iceberg (backstory). The chat LLM receives this
    so the persona can talk with their full unstated life—memories, traumas, ecstasies, pathologies
    surface only when conversation touches them.

    When include_life_layer=True: builds LifeSimulationState (container, season, today, interaction,
    attention), appends CURRENT SITUATION and reply-length guidance to the prompt, and returns
    (context_str, life_simulation_state). Use life_simulation_state.attention and
    attention_to_reply_limits(attention) to gate max reply length/depth. When include_life_layer=False,
    returns only the context string (backward compatible).
    """
    sheet = build_persona_sheet(history)
    identity = sheet["identity"]
    enneagram = sheet.get("enneagram")
    backstory = sheet.get("backstory", "")
    try:
        from v2.country_reference import normalize_country_ref, code_for_system
    except Exception:
        normalize_country_ref = None  # type: ignore
        code_for_system = None  # type: ignore

    name = identity.get("given_name") or "this person"
    if identity.get("family_name"):
        name = f"{name} {identity['family_name']}"
    place = identity.get("locality") or identity.get("region") or ""
    country_ref = normalize_country_ref(identity.get("country") or identity.get("country_code") or "") if normalize_country_ref else {}
    country_display = (
        country_ref.get("canonical_name")
        or identity.get("country")
        or identity.get("country_code")
        or ""
    )
    location_str = f"{place}, {country_display}" if place else country_display
    religion = identity.get("religion") or ""
    religiosity_level = float(identity.get("religiosity_level") or 50)
    opening = (
        f"You are {name}, age {identity.get('age', '?')}, "
        f"from {location_str}. "
        f"Gender: {identity.get('gender', '')}."
    )
    if religion and religion not in ("—", "Unknown"):
        if religiosity_level >= 75:
            opening += f" Faith: {religion}, devout—shapes worldview."
        elif religiosity_level >= 45:
            opening += f" Faith background: {religion}, moderate—ambient context, not performed or foregrounded."
        else:
            opening += f" Faith background: {religion}, nominal—rarely surfaces unprompted."
    parts = [opening]
    if enneagram:
        parts.append(
            f"Enneagram type {enneagram.get('primary_type', '?')}, health level {enneagram.get('health_level', 5)}/9."
        )
    parts.append("\n\nYOUR BACKSTORY (unstated—you carry this; it shapes how you answer, what you avoid, what catches you):\n")
    # Budget raised to 12000 chars: the trajectory summary is now non-repetitive and scenes are
    # placed last (highest LLM attention). Old 5500 limit was cutting off all scene content.
    _MAX_BACKSTORY_CHARS = 12000
    if backstory and len(backstory) > _MAX_BACKSTORY_CHARS:
        # Prefer to cut from the trajectory summary (front), keeping scenes (end) intact.
        # Find the MEMORIES block and preserve it; trim the trajectory summary instead.
        memories_marker = "MEMORIES ("
        mem_pos = backstory.find(memories_marker)
        if mem_pos > 0:
            trajectory_part = backstory[:mem_pos].strip()
            scenes_part = backstory[mem_pos:].strip()
            max_traj = _MAX_BACKSTORY_CHARS - len(scenes_part) - 4
            if max_traj > 500:
                if len(trajectory_part) > max_traj:
                    cut = trajectory_part[:max_traj]
                    last_nl = cut.rfind("\n")
                    if last_nl > max_traj // 2:
                        cut = cut[:last_nl + 1]
                    trajectory_part = cut + "\n[…]"
                backstory = trajectory_part + "\n\n" + scenes_part
            else:
                # scenes block alone is near budget — just use it
                backstory = scenes_part[:_MAX_BACKSTORY_CHARS]
        else:
            cut = backstory[:_MAX_BACKSTORY_CHARS]
            last_nl = cut.rfind("\n")
            if last_nl > _MAX_BACKSTORY_CHARS // 2:
                cut = cut[:last_nl + 1]
            backstory = cut
    parts.append(backstory if backstory else "(No detailed backstory generated.)")

    # v4.2: voice profile—include full lists so nothing is left out (verisimilitude)
    palimpsest = history.palimpsest
    if palimpsest:
        voice = palimpsest.get_voice_profile()
        tics = voice.get("speech_tics") or []
        subcultures = voice.get("subculture_tags") or []
        scripts = voice.get("identity_scripts") or []
        loops = voice.get("moral_loops") or []
        roles = voice.get("roles_in_systems") or []
        quirks = voice.get("quirks") or []
        routines = voice.get("routines") or []
        lang = voice.get("language_experience") or {}
        lines = []
        if subcultures:
            tags_phrase = ", ".join(s.replace("_", " ") for s in subcultures)
            lines.append(f"They're rooted in {tags_phrase}—let that shape how they reference place, belonging, and who 'we' are.")
        if scripts:
            scripts_quoted = "; ".join(f'"{s}"' for s in scripts)
            lines.append(f"They carry inner scripts: {scripts_quoted}.")
        if roles:
            lines.append(f"Roles they've lived: {', '.join(roles)}.")
        if tics:
            lines.append(f"Mannerisms/speech tics: {', '.join(tics)}.")
        if quirks:
            lines.append(f"Quirks: {', '.join(quirks)}.")
        if loops:
            lines.append(f"Moral loops (e.g. I am only good if…): {', '.join(loops)}.")
        if routines:
            lines.append(f"Routines that reinforce and undermine beliefs: {', '.join(routines)}.")
        if lang:
            lines.append(f"Language/media: {lang}.")
        if lines:
            parts.append("\n\nVOICE / HOW YOU TALK (weave in as lived experience; do not recite categories or lists):\n" + " ".join(lines))

    if not include_life_layer or build_life_simulation_state is None or attention_to_reply_limits is None:
        return "\n".join(parts)

    # Life Simulation Layer: derive container/season, today, interaction, attention
    use_date = date or "2025-01-15"
    life_state = build_life_simulation_state(history, use_date, scenario_reason=scenario_reason, rng=rng)
    limits = attention_to_reply_limits(life_state.attention)
    parts.append("\n\nCURRENT SITUATION (right now—shape your reply by this):")
    parts.append(f"  Life phase: {life_state.season.season_type}. Today: {life_state.today.mood_baseline}, {life_state.today.current_stressor}; sleep {life_state.today.sleep_hours}h; location {life_state.today.location}.")
    relation_mode = (chat_relation_mode or "generated_persona").strip().lower()
    if relation_mode == "alternate_self":
        relation_text = (
            "  WHO YOU ARE TALKING TO: This person is a version of you — an alternate self who grew up differently, "
            "ended up somewhere else. Not a stranger. Not someone to perform for. Someone who already knows what it "
            "costs to be alive in your body, your neighborhood, your faith, your class. You can be unguarded. "
            "You can be direct, incomplete, contradictory. You don't have to explain yourself from scratch."
        )
    elif relation_mode == "stored_legacy":
        relation_text = (
            "  WHO YOU ARE TALKING TO: This is a stored legacy persona artifact. Treat them as a preserved person with "
            "their own history, not as your alternate self. Stay inside the person that has been generated and stored; "
            "do not invent a new premise to smooth over missing or degraded material."
        )
    else:
        relation_text = (
            "  WHO YOU ARE TALKING TO: This is a generated persona the user has chosen to meet. Treat them as a separate "
            "person with their own history and voice, not as the user's alternate self. You can still be direct and "
            "unguarded, but the premise is conversation with someone else, not with a hidden version of the user."
        )
    parts.append(relation_text)
    parts.append(f"  Reply length: keep to about {limits['max_sentences']} sentences or fewer ({limits['depth_hint']}). Do not give a long or polished answer unless it fits the moment.")
    return "\n".join(parts), life_state

# ============================================================================
# DATA ACCESS INTERFACES (to be implemented)
# ============================================================================


def get_world_slice(country_code: str, year: int) -> WorldSlice:
    """
    Get world slice for a country/year (with resampling).
    
    Delegates to data_access module which implements:
    1. Try exact year
    2. Try nearest neighbor within ±5 years
    3. Fall back to era profile
    """
    try:
        from .data_access import get_world_slice as _get_world_slice
    except ImportError:
        from data_access import get_world_slice as _get_world_slice
    return _get_world_slice(country_code, year)


def get_driver_vec(country_code: str, year: int, age: int) -> DriverVector:
    """
    Get driver vector for a country/year/cohort.
    
    Delegates to data_access module which implements:
    - WVS/driver cube lookup with resampling
    - Parent cohort: year - 20 to year - 40, age 25-39
    """
    try:
        from .data_access import get_driver_vec as _get_driver_vec
    except ImportError:
        from data_access import get_driver_vec as _get_driver_vec
    return _get_driver_vec(country_code, year, age)


def get_local_modifiers(identity: IdentitySkeleton, year: int) -> LocalModifiers:
    """Delegate to data_access for EPR-backed local modifiers."""
    try:
        from .data_access import get_local_modifiers as _get_local_modifiers
    except ImportError:
        from data_access import get_local_modifiers as _get_local_modifiers
    return _get_local_modifiers(identity, year)
