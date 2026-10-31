"""
Life Simulation Layer — schema for the engine between persona and response.

Layer 1: LifeContainer (structural constraints, once per session)
Layer 2: LifeSeason (current phase, per week/month)
Layer 3: TodayState (per conversation)
Layer 4: InteractionContext (why in chat)
Attention: AttentionBudget (gates response length/depth)

See LIFE_SIMULATION_LAYER.md for full spec.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Any, Dict
from enum import Enum
import random


# ---------------------------------------------------------------------------
# Layer 1: Structural Life Constraints (Life Container)
# ---------------------------------------------------------------------------

class JobType(str, Enum):
    BACK_OFFICE = "back_office"
    CALL_CENTER = "call_center"
    RETAIL = "retail"
    INFORMAL = "informal"
    UNEMPLOYED = "unemployed"
    STUDENT = "student"
    DOMESTIC = "domestic"
    FARM_LABOR = "farm_labor"
    FACTORY = "factory"
    OTHER = "other"


class CommuteStyle(str, Enum):
    NONE = "none"
    WALK = "walk"
    BUS = "bus"
    MOTORCYCLE = "motorcycle"
    CAR = "car"
    LONG_COMMUTE = "long_commute"


class LivingArrangement(str, Enum):
    WITH_FAMILY = "with_family"
    WITH_ROOMMATES = "with_roommates"
    ALONE = "alone"
    WITH_PARTNER = "with_partner"
    UNSTABLE = "unstable"


class IncomeStress(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRISIS = "crisis"


class InternetAccess(str, Enum):
    HOME_ONLY = "home_only"
    PHONE_ONLY = "phone_only"
    WORK_AND_PHONE = "work_and_phone"
    UNRELIABLE = "unreliable"
    ABUNDANT = "abundant"


class SocialCircleDensity(str, Enum):
    ISOLATED = "isolated"
    THIN = "thin"
    MODERATE = "moderate"
    DENSE = "dense"


class SleepDebtBaseline(str, Enum):
    NONE = "none"
    LIGHT = "light"
    CHRONIC = "chronic"
    SEVERE = "severe"


@dataclass
class LifeContainer:
    """Permanent life reality. Generated once per session."""
    job_type: str = "back_office"
    commute_style: str = "bus"
    living_arrangement: str = "with_family"
    family_obligations: str = "light"  # none, light, primary_supporter, eldercare, childcare
    income_stress: str = "medium"
    internet_access_patterns: str = "phone_only"
    social_circle_density: str = "moderate"
    sleep_debt_baseline: str = "light"
    extra: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Layer 2: Current Life Season (months)
# ---------------------------------------------------------------------------

class LifeSeasonType(str, Enum):
    JOB_HUNT = "job_hunt_phase"
    RELATIONSHIP = "relationship_phase"
    BURNOUT = "burnout_phase"
    CARING_FOR_PARENT = "caring_for_parent_phase"
    SAVING_MONEY = "saving_money_phase"
    SPIRITUAL_RECOMMITMENT = "spiritual_recommitment_phase"
    ACTIVISM_SURGE = "activism_surge_phase"
    STABLE_ROUTINE = "stable_routine_phase"
    OTHER = "other"


@dataclass
class LifeSeason:
    """Current phase (months). Modulates attention, bandwidth, patience."""
    season_type: str = "stable_routine_phase"
    intensity: float = 0.5  # 0-1 how much this phase dominates
    extra: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Layer 3: Today State (per conversation)
# ---------------------------------------------------------------------------

@dataclass
class TodayState:
    """Today's conditions. Generated per conversation (or per day)."""
    date: str = ""  # YYYY-MM-DD
    sleep_hours: float = 6.0
    mood_baseline: str = "neutral"  # slightly_irritable, neutral, anxious, okay, low
    current_stressor: str = "none"  # coworker_conflict, money, family, health, none
    open_loops: int = 3
    next_obligation_minutes: int = 60
    physical_state: str = "fine"  # mild_headache, tired, hungry, fine, sick
    phone_battery_pct: int = 50
    location: str = "home"  # shared_living_room, commute, work, alone_room, cafe
    interruptions_risk: str = "medium"  # high, medium, low
    time_windows: List[Dict[str, str]] = field(default_factory=list)  # [{"start": "09:05", "end": "09:18"}]
    extra: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Layer 4: Interaction Context (why in this chat)
# ---------------------------------------------------------------------------

class InteractionReason(str, Enum):
    PAID_MICROTASK = "paid_microtask"
    LANGUAGE_EXCHANGE = "language_exchange"
    BOREDOM_SCROLLING = "boredom_scrolling"
    ACTIVISM_CURIOSITY = "activism_curiosity"
    FRIEND_OF_FRIEND_INTRO = "friend_of_friend_intro"
    PRACTICING_ENGLISH = "practicing_english"
    PROCRASTINATING_WORK = "procrastinating_work"
    LONELY_EVENING = "lonely_evening"
    OTHER = "other"


@dataclass
class InteractionContext:
    """Why the persona is in this chat. Determines tone and effort level."""
    reason: str = "other"
    detail: str = ""  # optional free text
    extra: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Attention Budget (gates response)
# ---------------------------------------------------------------------------

@dataclass
class AttentionBudget:
    """0-100 scalars that gate response length and depth."""
    attention_available: float = 50.0   # 0 = scattered, 100 = fully present
    effort_willingness: float = 50.0   # 0 = minimal, 100 = full
    social_energy: float = 50.0        # 0 = depleted, 100 = fresh

    def clamp(self) -> "AttentionBudget":
        return AttentionBudget(
            attention_available=max(0, min(100, self.attention_available)),
            effort_willingness=max(0, min(100, self.effort_willingness)),
            social_energy=max(0, min(100, self.social_energy)),
        )


# ---------------------------------------------------------------------------
# Aggregated state for response generation
# ---------------------------------------------------------------------------

@dataclass
class LifeSimulationState:
    """All life-layer state in one object for the response generator."""
    container: LifeContainer = field(default_factory=LifeContainer)
    season: LifeSeason = field(default_factory=LifeSeason)
    today: TodayState = field(default_factory=TodayState)
    interaction: InteractionContext = field(default_factory=InteractionContext)
    attention: AttentionBudget = field(default_factory=AttentionBudget)


# ---------------------------------------------------------------------------
# Derivation from simulation (step 27)
# ---------------------------------------------------------------------------

def _get_life_snapshot_from_source(source: Any) -> Dict[str, Any]:
    """Extract life_snapshot dict from PersonaHistory, Palimpsest, or sheet dict."""
    if source is None:
        return {}
    if isinstance(source, dict):
        snap = source.get("life_snapshot")
        if isinstance(snap, dict):
            return snap
        if isinstance(source.get("palimpsest"), dict):
            snap = source["palimpsest"].get("life_snapshot")
            if isinstance(snap, dict):
                return snap
        return {}
    palimpsest = getattr(source, "palimpsest", None)
    if palimpsest is not None:
        return getattr(palimpsest, "life_snapshot", None) or {}
    return getattr(source, "life_snapshot", None) or {}


def derive_life_container_from_simulation(persona_history: Any) -> LifeContainer:
    """
    Derive Life Container from stored simulation output (Palimpsest.life_snapshot).
    Call once per session when loading persona for conversation. If no life_snapshot
    exists (e.g. no present-year recursion yet), returns defaults.
    """
    snap = _get_life_snapshot_from_source(persona_history)
    return LifeContainer(
        job_type=str(snap.get("job_type", "back_office")),
        commute_style=str(snap.get("commute_style", "bus")),
        living_arrangement=str(snap.get("living_arrangement", "with_family")),
        family_obligations=str(snap.get("family_obligations", "light")),
        income_stress=str(snap.get("income_stress", "medium")),
        internet_access_patterns=str(snap.get("internet_access_patterns", "phone_only")),
        social_circle_density=str(snap.get("social_circle_density", "moderate")),
        sleep_debt_baseline=str(snap.get("sleep_debt_baseline", "light")),
        extra=dict(snap.get("extra", {})),
    )


def derive_life_season_from_simulation(persona_history: Any) -> LifeSeason:
    """
    Derive Life Season from stored simulation output (life_snapshot.current_life_phase).
    Intensity can be defaulted or inferred later from narrative/events.
    """
    snap = _get_life_snapshot_from_source(persona_history)
    phase = str(snap.get("current_life_phase", "stable_routine_phase"))
    return LifeSeason(season_type=phase, intensity=0.5, extra={})


# ---------------------------------------------------------------------------
# Today State and Interaction Context (steps 28, 29)
# ---------------------------------------------------------------------------

def instantiate_today(
    container: LifeContainer,
    season: LifeSeason,
    date: str,
    rng: Optional[random.Random] = None,
) -> TodayState:
    """
    Generate Today State per conversation from container + season + date.
    Uses optional rng for variety (sleep, mood, stressor, location, etc.).
    """
    r = rng or random
    if hasattr(r, "random"):
        rand = r.random
        choice = lambda xs: r.choice(xs) if hasattr(r, "choice") else xs[int(rand() * len(xs))]
    else:
        rand = random.random
        choice = lambda xs: random.choice(xs)

    # Sleep: baseline from container.sleep_debt_baseline
    sleep_base = 6.0
    if container.sleep_debt_baseline in ("chronic", "severe"):
        sleep_base = 5.0 + rand() * 1.5
    elif container.sleep_debt_baseline == "none":
        sleep_base = 6.5 + rand() * 1.5
    else:
        sleep_base = 5.5 + rand() * 1.5
    sleep_hours = round(sleep_base, 1)

    # Mood: season and sleep
    mood_opts = ["slightly_irritable", "neutral", "anxious", "okay", "low"]
    if season.season_type == "burnout_phase":
        mood_opts = ["low", "slightly_irritable", "neutral", "anxious", "okay"]
    elif sleep_hours < 5.5:
        mood_opts = ["slightly_irritable", "low", "neutral", "anxious", "okay"]
    mood_baseline = choice(mood_opts)

    # Stressor: income_stress and season
    stressor_opts = ["none", "money", "family", "coworker_conflict", "health"]
    if container.income_stress in ("high", "crisis"):
        stressor_opts = ["money", "family", "none", "coworker_conflict", "health"]
    if "parent" in season.season_type or "job_hunt" in season.season_type:
        stressor_opts = ["family", "money", "none", "health", "coworker_conflict"]
    current_stressor = choice(stressor_opts)

    # Open loops, next obligation
    open_loops = max(1, min(7, int(3 + rand() * 4)))
    next_obligation_minutes = int(15 + rand() * 180) if rand() > 0.2 else int(5 + rand() * 30)

    # Physical, battery, location
    physical_opts = ["fine", "tired", "mild_headache", "hungry", "sick"]
    physical_state = choice(physical_opts)
    phone_battery_pct = int(10 + rand() * 90)
    location_opts = ["home", "shared_living_room", "commute", "work", "alone_room", "cafe"]
    location = choice(location_opts)
    interruptions_risk = choice(["high", "medium", "low"])

    return TodayState(
        date=date,
        sleep_hours=sleep_hours,
        mood_baseline=mood_baseline,
        current_stressor=current_stressor,
        open_loops=open_loops,
        next_obligation_minutes=next_obligation_minutes,
        physical_state=physical_state,
        phone_battery_pct=phone_battery_pct,
        location=location,
        interruptions_risk=interruptions_risk,
        time_windows=[],
        extra={},
    )


def instantiate_interaction_context(
    scenario_reason: Optional[str] = None,
    rng: Optional[random.Random] = None,
) -> InteractionContext:
    """
    Generate why the persona is in this chat. If scenario_reason is provided
    (e.g. from a scenario config), use it; otherwise draw from InteractionReason.
    """
    reasons = [
        "paid_microtask", "language_exchange", "boredom_scrolling", "activism_curiosity",
        "friend_of_friend_intro", "practicing_english", "procrastinating_work", "lonely_evening", "other",
    ]
    if scenario_reason and scenario_reason in reasons:
        reason = scenario_reason
    else:
        r = rng or random
        reason = r.choice(reasons) if hasattr(r, "choice") else random.choice(reasons)
    return InteractionContext(reason=reason, detail="", extra={})


def build_life_simulation_state(
    persona_history: Any,
    date: str,
    scenario_reason: Optional[str] = None,
    rng: Optional[random.Random] = None,
) -> LifeSimulationState:
    """
    Build full LifeSimulationState for the response path. Call before generating
    a reply. Derives container and season from simulation; instantiates today
    and interaction; computes attention budget. Use life_state.attention to
    gate max reply length and depth.
    """
    container = derive_life_container_from_simulation(persona_history)
    season = derive_life_season_from_simulation(persona_history)
    today = instantiate_today(container, season, date, rng=rng)
    interaction = instantiate_interaction_context(scenario_reason=scenario_reason, rng=rng)
    attention = compute_attention_budget(container, season, today, interaction)
    return LifeSimulationState(
        container=container,
        season=season,
        today=today,
        interaction=interaction,
        attention=attention.clamp(),
    )


# ---------------------------------------------------------------------------
# Attention Budget (gates response)
# ---------------------------------------------------------------------------

def compute_attention_budget(
    container: LifeContainer,
    season: LifeSeason,
    today: TodayState,
    interaction: InteractionContext,
) -> AttentionBudget:
    """
    Derive attention scalars from life layers. Gates response length/depth.
    Placeholder: implement real logic from sleep_debt_baseline, season_type,
    today (sleep_hours, mood, next_obligation, interruptions_risk), interaction reason.
    """
    # Placeholder: simple heuristics
    att = 50.0
    eff = 50.0
    soc = 50.0

    # Sleep debt and today's sleep
    if container.sleep_debt_baseline in ("chronic", "severe"):
        att -= 15
        soc -= 15
    if today.sleep_hours < 5:
        att -= 10
        soc -= 10
    if today.sleep_hours >= 7:
        att += 5
        soc += 5

    # Season
    if season.season_type == "burnout_phase":
        att -= 20
        eff -= 25
        soc -= 20
    elif season.season_type == "stable_routine_phase":
        soc += 5

    # Today
    if today.next_obligation_minutes < 30:
        att -= 15
        eff -= 10
    if today.interruptions_risk == "high":
        att -= 15
    if today.mood_baseline in ("slightly_irritable", "anxious", "low"):
        eff -= 10
        soc -= 10

    # Interaction reason
    if interaction.reason in ("boredom_scrolling", "procrastinating_work"):
        eff -= 15
    if interaction.reason in ("language_exchange", "activism_curiosity"):
        eff += 10
    if interaction.reason == "lonely_evening":
        soc += 10

    return AttentionBudget(
        attention_available=max(0, min(100, att)),
        effort_willingness=max(0, min(100, eff)),
        social_energy=max(0, min(100, soc)),
    )


def attention_to_reply_limits(attention: AttentionBudget) -> Dict[str, Any]:
    """
    Map attention scalars to suggested reply constraints for the response path.
    Use for max_tokens, max_sentences, or instruction hints.
    """
    att = attention.attention_available
    eff = attention.effort_willingness
    soc = attention.social_energy
    avg = (att + eff + soc) / 3.0
    # Low attention → short replies
    if avg < 25:
        max_sentences = 2
        depth_hint = "minimal"
    elif avg < 50:
        max_sentences = 4
        depth_hint = "brief"
    elif avg < 75:
        max_sentences = 8
        depth_hint = "moderate"
    else:
        max_sentences = 12
        depth_hint = "full"
    return {
        "max_sentences": max_sentences,
        "depth_hint": depth_hint,
        "attention_available": att,
        "effort_willingness": eff,
        "social_energy": soc,
    }
