"""
Rawlsing v4.2 - Recursion Delta Schema

Mechanism-first, additive recursion. Each year outputs structured deltas;
nothing overwrites. The persona is a palimpsest—layers accumulate with provenance.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class AccumulatedLayer:
    """Single layer with provenance (age at which it was added)."""
    age: int
    value: str
    context: Optional[str] = None  # e.g. "when father asked about grades"


@dataclass
class RecursionDelta:
    """
    Structured output from one recursion. Additive only—no overwrites.
    Grounded in time/place via context block.
    """
    age: int
    year: int

    # Time/place specifics (from world_slice, driver_vec, events)
    context: Dict[str, Any] = field(default_factory=dict)
    # e.g. {"location": "Oakland, CA", "decade": "2000s_late", "media_tech": ["early_social_media"],
    #       "political_moment": ["Iraq_war"], "wvs_tags": ["low_trust", "high_authority"]}

    # Numeric deltas (applied to state)
    needs_delta: Dict[str, float] = field(default_factory=dict)
    strategy_spikes: Dict[str, float] = field(default_factory=dict)  # strategy -> delta
    indices_delta: Dict[str, float] = field(default_factory=dict)

    # Additive layers (append to history; never replace)
    identity_scripts: List[str] = field(default_factory=list)  # "one_who_fights", etc.
    symbols_added: List[str] = field(default_factory=list)
    symbols_reinterpreted: List[Dict[str, str]] = field(default_factory=list)  # [{"old": "plastic_cup", "new": "relic_of_usefulness"}]
    moral_atmosphere_tags: List[str] = field(default_factory=list)
    speech_tics: List[str] = field(default_factory=list)
    subculture_tags: List[str] = field(default_factory=list)
    events_hooks: List[str] = field(default_factory=list)
    moral_loops: List[str] = field(default_factory=list)  # "I_am_only_good_if_useful"

    # Daily routines (Section 9): rituals that reinforce AND undermine stated beliefs
    routines: List[str] = field(default_factory=list)  # "morning_prayer_then_guilt", "coffee_before_anyone_sees"

    # Structural thought-rails (TR) deltas—emergent interpretive habits
    thought_rail_updates: Dict[str, str] = field(default_factory=dict)
    # e.g. {"authority_schema": "arbitrary_but_God_above", "fairness_schema": "rigged_game"}

    # Expressive language (Section 7): L1–L3 stack, education, media, abstentions
    language_experience: Dict[str, Any] = field(default_factory=dict)
    # e.g. {"L1": "Vietnamese", "L2": "French_school", "education_years": 8, "media": "radio_only", "abstentions": []}

    # DRTS modifiers applied this year (for audit; indices_delta already encodes result)
    drts_modifiers: List[str] = field(default_factory=list)
    # e.g. ["+10_betrayal", "-10_dependency_load"]

    # Outlier Engine triggers if any (IAI, TT, AAF, RMT)
    outlier_triggers: List[str] = field(default_factory=list)
    # e.g. ["IAI_70_isolation_mythmaking", "AAF_65_creative_resistance"]

    # Self-narrative about shifts (when indices/needs/strategies changed noticeably)
    self_narrative: Dict[str, str] = field(default_factory=dict)
    # e.g. {"DRTS": "I got tired. Or maybe I got smart. I don't know—I used to believe..."}
    # Key = axis that shifted; value = how they tell themselves about it (imperfect, contested)

    # DRTS components (v3.4): emergent profile beyond scalar—latent, activated, suppressed, rewired, etc.
    # Extensible: persona may have different component mix. Examples: {"latent": 20, "activated": 5, "suppressed": 40, "rewired": 10}
    drts_components: Dict[str, float] = field(default_factory=dict)

    # Role in peer/family systems (v3.4): emergent—scapegoat, negotiator, ghost, confidant, enforcer, etc.
    # Extensible: multiple roles across contexts. Examples: ["scapegoat_in_family", "negotiator_with_peers"]
    roles_in_systems: List[str] = field(default_factory=list)

    # Micro-patterns/quirks (v3.4): bodily, behavioral—distinct from identity_scripts.
    # Examples: ["rubs_ears_when_overstimulated", "freezes_at_loud_voices", "traces_spiral_to_calm"]
    quirks: List[str] = field(default_factory=list)

    # Authority/ideology/religion reception (v3.4+): how different sources land—absorb, reject, transform, cling.
    # Influenced by many factors: caregivers, trauma, disillusionment, institutions. Extensible.
    # Examples: disillusionment_with_human_authority → cling_to_God; reject_God → cling_to_secular; trauma_from_parents → resist_religion
    # Each entry: {"source": "God"|"parents"|"state"|..., "stance": "absorb"|"reject"|"intensify"|"transform"|..., "influence": "..."}
    authority_reception_patterns: List[Dict[str, Any]] = field(default_factory=list)

    # Life Simulation Layer: present-life snapshot (for current-year recursion only).
    # Populates Life Container and Life Season; derived at conversation time, not generated then.
    # Keys align with LifeContainer / LifeSeason: job_type, commute_style, living_arrangement,
    # family_obligations, income_stress, internet_access_patterns, social_circle_density,
    # sleep_debt_baseline, current_life_phase (season). Recursion prompt for present year asks for these.
    life_snapshot: Dict[str, Any] = field(default_factory=dict)

    # Optional: short prose for human reading (derived from above, not primary)
    narrative: Optional[str] = None


@dataclass
class Palimpsest:
    """
    Accumulated layers across all ages. Nothing is overwritten.
    Complexity is monotonic—each recursion adds.
    """
    # Histories with provenance
    identity_scripts_history: List[AccumulatedLayer] = field(default_factory=list)
    symbols_history: List[AccumulatedLayer] = field(default_factory=list)
    symbols_reinterpretations: List[Dict[str, Any]] = field(default_factory=list)
    moral_atmosphere_history: List[AccumulatedLayer] = field(default_factory=list)
    speech_tics_history: List[AccumulatedLayer] = field(default_factory=list)
    subculture_history: List[AccumulatedLayer] = field(default_factory=list)
    moral_loops_history: List[AccumulatedLayer] = field(default_factory=list)
    events_hooks_history: List[AccumulatedLayer] = field(default_factory=list)
    routines_history: List[AccumulatedLayer] = field(default_factory=list)
    thought_rail_history: List[Dict[str, Any]] = field(default_factory=list)  # [{"age": 17, "authority_schema": "..."}]
    language_experience_history: List[Dict[str, Any]] = field(default_factory=list)  # [{"age": 17, "L1": "...", ...}]
    drts_components_history: List[Dict[str, Any]] = field(default_factory=list)  # [{"age": 17, "latent": 20, "activated": 5, ...}]
    roles_in_systems_history: List[AccumulatedLayer] = field(default_factory=list)
    quirks_history: List[AccumulatedLayer] = field(default_factory=list)
    authority_reception_history: List[Dict[str, Any]] = field(default_factory=list)  # [{"age": 17, "source": "God", "stance": "...", ...}]

    # Rupture voice notes: surface in voice schema so chat engine knows unresolved wounds
    rupture_voice_notes: List[str] = field(default_factory=list)  # ["unresolved since age 7: «...»", ...]

    # Self-narratives about shifts (axis -> list of narratives across time)
    self_narratives: Dict[str, List[AccumulatedLayer]] = field(default_factory=dict)

    # Present-life snapshot (from present-year RecursionDelta only; used to derive Life Container)
    life_snapshot: Dict[str, Any] = field(default_factory=dict)

    # Deltas applied (for audit)
    deltas_by_age: Dict[int, RecursionDelta] = field(default_factory=dict)

    def apply_delta(self, delta: RecursionDelta) -> "Palimpsest":
        """Apply a recursion delta; append new layers, never overwrite."""
        new = Palimpsest(
            identity_scripts_history=list(self.identity_scripts_history),
            symbols_history=list(self.symbols_history),
            symbols_reinterpretations=list(self.symbols_reinterpretations),
            moral_atmosphere_history=list(self.moral_atmosphere_history),
            speech_tics_history=list(self.speech_tics_history),
            subculture_history=list(self.subculture_history),
            moral_loops_history=list(self.moral_loops_history),
            events_hooks_history=list(self.events_hooks_history),
            routines_history=list(self.routines_history),
            thought_rail_history=list(self.thought_rail_history),
            language_experience_history=list(self.language_experience_history),
            drts_components_history=list(self.drts_components_history),
            roles_in_systems_history=list(self.roles_in_systems_history),
            quirks_history=list(self.quirks_history),
            authority_reception_history=list(self.authority_reception_history),
            rupture_voice_notes=list(self.rupture_voice_notes),
            self_narratives=dict(self.self_narratives),
            life_snapshot=dict(delta.life_snapshot) if delta.life_snapshot else dict(self.life_snapshot),
            deltas_by_age=dict(self.deltas_by_age),
        )
        age = delta.age
        for s in delta.identity_scripts:
            new.identity_scripts_history.append(AccumulatedLayer(age=age, value=s))
        for s in delta.symbols_added:
            new.symbols_history.append(AccumulatedLayer(age=age, value=s))
        for r in delta.symbols_reinterpreted:
            new.symbols_reinterpretations.append({"age": age, **r})
        for t in delta.moral_atmosphere_tags:
            new.moral_atmosphere_history.append(AccumulatedLayer(age=age, value=t))
        for t in delta.speech_tics:
            new.speech_tics_history.append(AccumulatedLayer(age=age, value=t))
        for t in delta.subculture_tags:
            new.subculture_history.append(AccumulatedLayer(age=age, value=t))
        for m in delta.moral_loops:
            new.moral_loops_history.append(AccumulatedLayer(age=age, value=m))
        for e in delta.events_hooks:
            new.events_hooks_history.append(AccumulatedLayer(age=age, value=e))
        for r in delta.routines:
            new.routines_history.append(AccumulatedLayer(age=age, value=r))
        if delta.thought_rail_updates:
            new.thought_rail_history.append({"age": age, **delta.thought_rail_updates})
        if delta.language_experience:
            new.language_experience_history.append({"age": age, **delta.language_experience})
        if delta.drts_components:
            new.drts_components_history.append({"age": age, **delta.drts_components})
        for r in delta.roles_in_systems:
            new.roles_in_systems_history.append(AccumulatedLayer(age=age, value=r))
        for q in delta.quirks:
            new.quirks_history.append(AccumulatedLayer(age=age, value=q))
        for p in delta.authority_reception_patterns:
            new.authority_reception_history.append({"age": age, **p})
        sn = delta.self_narrative
        if isinstance(sn, dict):
            for axis, narrative in sn.items():
                if axis not in new.self_narratives:
                    new.self_narratives[axis] = []
                new.self_narratives[axis].append(AccumulatedLayer(age=age, value=str(narrative)))
        elif isinstance(sn, str) and sn.strip():
            if "narrative" not in new.self_narratives:
                new.self_narratives["narrative"] = []
            new.self_narratives["narrative"].append(AccumulatedLayer(age=age, value=sn.strip()))
        new.deltas_by_age[age] = delta
        return new

    def _normalize_for_dedupe(self, x: Any) -> str:
        """Normalized key for dedupe: strip + lower for strings; else id."""
        if isinstance(x, str):
            return (x.strip().lower() or x)
        return str(id(x))

    def _dedupe_list(self, items: List[Any]) -> List[Any]:
        """Order-preserving dedupe: (1) collapse by normalized key; (2) drop any string that is a proper substring of another so the more specific variant is kept (e.g. keep family_support_primary_caretaker, drop family_support)."""
        seen: set = set()
        out: List[Any] = []
        for x in items:
            k = self._normalize_for_dedupe(x) if isinstance(x, str) else (x if isinstance(x, (int, float, bool)) else id(x))
            if k not in seen:
                seen.add(k)
                out.append(x)
        # Keep only most specific when one string contains another (drop the shorter)
        if not out:
            return out
        kept: List[Any] = []
        for x in out:
            if not isinstance(x, str):
                kept.append(x)
                continue
            nx = self._normalize_for_dedupe(x)
            is_proper_substring = False
            for y in out:
                if y is x or not isinstance(y, str):
                    continue
                ny = self._normalize_for_dedupe(y)
                if nx != ny and nx in ny:
                    is_proper_substring = True
                    break
            if not is_proper_substring:
                kept.append(x)
        return kept

    def get_voice_profile(self) -> Dict[str, Any]:
        """Derive voice/speech profile from accumulated layers for conversation. Lists are deduped (first occurrence kept)."""
        tics = self._dedupe_list([l.value for l in self.speech_tics_history])
        subcultures = self._dedupe_list([l.value for l in self.subculture_history])
        moral_atmosphere = self._dedupe_list([l.value for l in self.moral_atmosphere_history])
        routines = self._dedupe_list([l.value for l in self.routines_history])
        identity_scripts = self._dedupe_list([l.value for l in self.identity_scripts_history])
        moral_loops = self._dedupe_list([l.value for l in self.moral_loops_history])
        roles_in_systems = self._dedupe_list([l.value for l in self.roles_in_systems_history])
        quirks = self._dedupe_list([l.value for l in self.quirks_history])
        # Latest language experience (most recent non-empty)
        lang_exp = {}
        for le in reversed(self.language_experience_history):
            if le and isinstance(le, dict):
                lang_exp = {k: v for k, v in le.items() if k != "age"}
                break
        return {
            "speech_tics": tics,
            "subculture_tags": subcultures,
            "moral_atmosphere_tags": moral_atmosphere,
            "identity_scripts": identity_scripts,
            "moral_loops": moral_loops,
            "routines": routines,
            "language_experience": lang_exp,
            "drts_components": self.drts_components_history[-1] if self.drts_components_history else {},
            "roles_in_systems": roles_in_systems,
            "quirks": quirks,
            "authority_reception_patterns": self.authority_reception_history,
            "rupture_voice_notes": list(self.rupture_voice_notes),
        }


# ============================================================================
# Temporal Systems (Section 8): Next Day, Skip Back
# ============================================================================


@dataclass
class NextDaySnapshot:
    """
    Next Day Trigger (v3.4/v4.0): fine-grain snapshot after a key event.
    Shows how the previous day left imprinted: gesture, dream, feeling/belief shift.
    """
    gesture_shift: str = ""  # e.g. "slower blink", "faster speech"
    dream_intrusion: str = ""  # e.g. "water flowing backwards", "recurring face"
    feeling_shift: str = ""  # e.g. "slightly softened", "hardened", "confused"
    event_context: str = ""  # What triggered this snapshot


def get_skip_back_view(history: Any, target_age: int) -> Optional[Dict[str, Any]]:
    """
    Skip Back (v3.4/v4.0): view persona at earlier age.
    Returns pre-trauma quirks, naive interpretations, early ideological templates.
    Use for explanation, not retro-fitting neat arcs.
    """
    if not history or not getattr(history, "yearly_states", None):
        return None
    if target_age < 0 or target_age >= len(history.yearly_states):
        return None
    state = history.yearly_states[target_age]
    return {
        "age": target_age,
        "year": state.current_year,
        "needs": {k: v for k, v in state.needs.__dict__.items() if not k.startswith("_")},
        "thought_rails": {
            "authority_schema": state.thought_rails.authority_schema,
            "fairness_schema": state.thought_rails.fairness_schema,
            "self_schema": state.thought_rails.self_schema,
        },
        "indices": {
            "PI": state.indices.permeability_index,
            "DRTS": state.indices.drts,
        },
    }


def get_grounded_context(
    year: int,
    country_code: str,
    locality: str,
    world_slice: Any,
    driver_vec: Any,
) -> Dict[str, Any]:
    """
    Build time/place-specific context for recursion. Grounds output in real data.
    """
    decade = (year // 10) * 10
    decade_label = f"{decade}s"
    if year - decade < 3:
        decade_label += "_early"
    elif year - decade >= 7:
        decade_label += "_late"

    # US-specific political/media moments (expand for other countries)
    political_moment = []
    media_tech = []
    if country_code == "US":
        if 1990 <= year < 2000:
            political_moment = ["Clinton", "dot_com_boom", "welfare_reform"]
            media_tech = ["pre_internet", "cable_tv"]
        elif 2000 <= year < 2010:
            political_moment = ["Bush", "Iraq_war", "9_11", "housing_bubble"]
            media_tech = ["early_internet", "early_social_media", "web_forums"]
        elif 2010 <= year < 2020:
            political_moment = ["recession", "Occupy", "Trump_rise"]
            media_tech = ["social_media", "smartphones", "algorithmic_feeds"]
        elif year >= 2020:
            political_moment = ["pandemic", "post_Trump", "collapse_anxiety"]
            media_tech = ["post_truth", "tiktok", "ai_awareness"]

    wvs_tags = []
    if driver_vec:
        trust = getattr(driver_vec, "trust_vs_distrust", 50)
        auth = getattr(driver_vec, "authoritarian_vs_egalitarian", 50)
        ind = getattr(driver_vec, "individualism_vs_collectivism", 50)
        if trust < 40:
            wvs_tags.append("low_trust")
        elif trust > 60:
            wvs_tags.append("high_trust")
        if auth > 60:
            wvs_tags.append("authoritarian_lean")
        elif auth < 40:
            wvs_tags.append("egalitarian_lean")
        if ind > 60:
            wvs_tags.append("individualist")
        elif ind < 40:
            wvs_tags.append("collectivist")

    result = {
        "year": year,
        "country": country_code,
        "location": locality or country_code,
        "decade": decade_label,
        "political_moment": political_moment,
        "media_tech": media_tech,
        "wvs_tags": wvs_tags,
        "gdp": getattr(world_slice, "gdp_per_capita", 50),
        "conflict": getattr(world_slice, "conflict_intensity", 0),
    }
    # Colonial/migration context when available (milieu-specific)
    col = getattr(world_slice, "colonial_history", None)
    if col and getattr(col, "colonizer", None):
        result["colonial_context"] = f"Colonizer: {col.colonizer}; independence: {getattr(col, 'independence_year', '—')}"
    mig = getattr(world_slice, "migration_data", None)
    if mig:
        parts = []
        if getattr(mig, "rural_to_urban_rate", None) is not None:
            parts.append(f"rural→urban: {mig.rural_to_urban_rate:.1%}/decade")
        if getattr(mig, "conflict_displacement", False):
            parts.append("conflict_displacement")
        if parts:
            result["migration_context"] = "; ".join(parts)
    return result


def format_grounded_context_for_prompt(grounded: Dict[str, Any]) -> str:
    """
    Format grounded context dict as readable prompt text.
    Draws from specifics: time, place, political moment, media, WVS, colonial/migration.
    """
    lines = [
        f"Year: {grounded.get('year', '?')} | Country: {grounded.get('country', '')} | Location: {grounded.get('location', '')}",
        f"Decade: {grounded.get('decade', '')}",
    ]
    if grounded.get("political_moment"):
        lines.append(f"Political moment: {', '.join(grounded['political_moment'])}")
    if grounded.get("media_tech"):
        lines.append(f"Media/tech: {', '.join(grounded['media_tech'])}")
    if grounded.get("wvs_tags"):
        lines.append(f"Values (WVS): {', '.join(grounded['wvs_tags'])}")
    lines.append(f"GDP band: {grounded.get('gdp', 50):.0f} | Conflict: {grounded.get('conflict', 0):.0f}")
    if grounded.get("colonial_context"):
        lines.append(f"Colonial: {grounded['colonial_context']}")
    if grounded.get("migration_context"):
        lines.append(f"Migration: {grounded['migration_context']}")
    return "\n".join(lines)