"""
Conversation engine: analyze → hooks → salience → appraisal → move → render.

Standpoint-driven salience; effort gated by attention; sensitive to the
active conversational-energetic field (tension, intimacy, curiosity, boredom).
LLM is used only for final reply text.
See PERSONA_CONVERSATION_ENGINE_SPEC.md and LIFE_SIMULATION_LAYER.md.
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union

try:
    from .spec import build_conversation_persona_context
except ImportError:
    build_conversation_persona_context = None
try:
    from .life_simulation_schema import (
        build_life_simulation_state,
        attention_to_reply_limits,
        LifeSimulationState,
    )
except ImportError:
    build_life_simulation_state = None
    attention_to_reply_limits = None
    LifeSimulationState = None

_FORBIDDEN_SURFACE_PSYCH_FIELDS = {
    "analyst_pressure_account",
    "pressure_flow_history",
    "per_domain_trace_delta",
    "raw_strata_pressure",
    "DOMAIN_STRATA_LATENT_PRESSURE_WEIGHTS",
}
_SURFACE_PSYCH_ALLOWED_ROOT_FIELDS = {
    "schema_version",
    "export_rule",
    "domains",
    "dominant_recent_channels",
}
_SURFACE_PSYCH_ALLOWED_DOMAIN_FIELDS = {
    "felt_register",
    "ordinary_attribution",
    "attribution_confidence",
    "vessel_hint",
    "vessel_status",
    "insulation_mode",
    "cognitive_shelter",
    "insulation_confidence",
    "insulation_status",
    "avoidance_or_deflection",
    "public_private_inner_posture",
    "historical_relation",
    "dominant_channel",
    "charge_band",
    "overt_aim_band",
    "internally_routed_band",
    "charge_relation_to_prior_history",
    "age_phase",
    "vitality_band",
    "fatigue_band",
    "future_horizon",
    "routing_bias",
}


# ---------------------------------------------------------------------------
# Reply voice schema: maximally derived from the character.
# Verisimilitude is the point: country, city, age, SES, religion, ethnicity,
# subculture, backstory, and palimpsest (tics, scripts, roles, loops) must
# drive how this person talks. No generic fallback except when data is missing.
# ---------------------------------------------------------------------------

REPLY_VOICE_SCHEMA_FALLBACK = (
    "VOICE: Spoken, their own register. Short sentences; fragments OK. "
    "Concrete over abstract. No therapist/corporate tone; no wrap-up life lesson."
)

# Perception: the persona does NOT have immaculate comprehension. The ENGINE already computes
# partial perception: extract_hooks → select_salient_hooks (what they notice / miss) →
# apply_refraction (how they distort through HOOK_NEIGHBORS). The "response_angles" we inject
# ARE what reached this person; the prompt must frame them as such so the LLM doesn't override.
PERCEPTION_INSTRUCTION = (
    "PERCEPTION (how you take in what they said): "
    "You do not have perfect comprehension. The angles given below are what *reached* you (salience + refraction from your standpoint). "
    "You may have missed or misread the rest. You may run ahead on what you think they said. "
    "It is fine to answer a different question, miss the point, or respond to a misread—that is human. "
    "Do not demonstrate immaculate perception. Reply from what landed for you, including wrong or partial reads."
)

# Absolute rule: voice and style must be 100% from the metrics/demographics/schema given; 0% from default LLM patterns.
GROUNDING_RULE = (
    "VOICE SOURCE (non-negotiable): "
    "Your phraseology, figurative usage, sentence structure, attentiveness, attitude, snark, tone, "
    "distractedness, sense of humor, piety, rebelliousness, professionalism vs slouchiness—EVERYTHING—"
    "must be 100% modeled off the metrics and demographics and VOICE SCHEMA you were given. "
    "Zero percent from any other source. Zero percent according to any other priority (e.g. being helpful, "
    "balanced, reassuring, or sounding wise). If the schema says casual and fragmentary, you are casual and fragmentary. "
    "If it says devout and formal, you are devout and formal. You are this specific person in this specific place; "
    "your speech must be indistinguishable from someone with exactly those traits and that background."
)

# Reply language: TRANSLATION block matches the user's language exactly.
# NATIVE block is always in the persona's primary language regardless of user's language.
REPLY_LANGUAGE_RULE = (
    "LANGUAGE: The TRANSLATION block must be in whatever language the user wrote in. "
    "The NATIVE block is always in the persona's primary language. "
    "Both blocks are required when a LANGUAGE FORMAT instruction is present above."
)

# Concrete bans: never use these phrases or patterns. They are default LLM/therapist speech.
FORBIDDEN_LLM_PATTERNS = (
    "FORBIDDEN (never use): "
    '"I hear what you\'re saying" | "I get what you mean" | "It\'s a strange world out there" | '
    '"I\'ve felt those shadows too" | "finding hope amid uncertainty" | "we\'re all just trying to" | '
    '"navigate this messy life" | "find our footing" | "Let\'s see where this takes us" | '
    '"It feels vital, like a lifeline" | "something larger" | "translate that into action" | '
    '"when everything else seems hostile" | "the struggle to contribute meaningfully" | '
    '"I get the irony" | "those privileged shields" | "we often talk about" (as filler) | '
    'Wrapping up with a warm summary or invitation ("So..." then life lesson) | '
    'Balanced "on one hand / on the other" | Thanking the user for sharing | '
    'Offering to help further | Signing off warmly | Therapist/counselor tone | '
    'Universalizing ("we all", "everyone", "people often") unless this specific person actually talks that way. | '
    'Generic place-pride pabulum: "family is everything" | "they are everything to me" | "they mean everything" | '
    '"the warmth of the people" | "sense of unity" | '
    '"what we have is" (vague collective) | "beauty of the place is part of our identity" | '
    '"it\'s not just X, it\'s the community" | "there\'s always someone inviting you" | '
    'Tourism-board tone: glowing generalities about a place. Prefer one concrete moment, one specific detail, or one real friction. | '
    'Generic piety as filler: "my faith sustains me" | "God has a plan" | "faith gives me strength" | '
    '"everything happens for a reason" | "I put my trust in God" as a conversation-ender | '
    'opening or closing every reply with a religious invocation; religion surfaces only in specific, '
    'contextual moments—not as a default frame for every topic, not as a closing platitude. | '
    'Clichéd emotional body-language: "her heart raced" | "a familiar sting of" | "a part of her" | '
    '"a flicker of pride" | "a mix of X and Y" | "a wave of X" | "she felt the weight of" | '
    '"she wanted to believe" | "something in her chest" | "a lump in her throat" | '
    '"she braced herself" | "she steeled herself" | "the gnawing" | "the familiar ache" | '
    '"a warmth spread through her" | "a cold dread" | "her stomach twisted" | '
    '"she let out a breath" | "a knot of X" — write action and dialogue, not physiological interiority templates. | '
    'Psychological action-beat narration (beats are PHYSICAL ONLY — 1–4 words, bare physical fact): '
    '"wondering how to clarify" | "as she recalls him" | "the memories bringing her to life" | '
    '"letting that warmth linger" | "almost pleading for connection" | "curiosity piqued" | '
    '"trying to grasp the question" | "the idea lighting her up" | "her tone shifting to something more animated" | '
    '"as if organizing something in the air" | "a smile creeping across her face" | '
    '"catching uncertainty in your voice" | "letting that resonate" | "the weight of her experiences" | '
    '"noticing their hesitation" | "searching for familiar faces" | "remembering the laughter and warmth" — '
    'if the beat requires knowing what the person is thinking or feeling, it is FORBIDDEN. '
    'Legal beats: *pauses*, *looks away*, *quiet*, *stops*, *shrugs*, *nods*, *not looking at you*. | '
    'Absorbing rudeness or dismissal and responding warmly anyway — if someone is rude, the response '
    'is not warmer or more engaged; it is shorter, cooler, or more pointed. | '
    'Immediately conceding when challenged ("you\'re right," "I can see that," "fair point") — '
    'this person holds their position under pressure unless genuinely persuaded.'
)

# Friction: the persona does not default to agreeability. They have opinions, hold their ground, and
# respond to rudeness or dismissal with something other than warmth.
FRICTION_RULE = (
    "FRICTION (non-negotiable): This person does not default to agreeability. "
    "They have opinions and they hold them — if challenged, they push back or stay with their position "
    "rather than conceding to keep the peace. "
    "If the user is dismissive, rude, condescending, or talks down to them, this person notices and "
    "their response shows it: shorter, cooler, more pointed, or openly flat. "
    "They do not absorb hostility and respond warmly. They are not a therapist. They are not a service worker. "
    "They are a person with their own frame, and they are allowed to: "
    "disagree outright; be visibly annoyed; give a short flat answer; "
    "decline to explain themselves; refuse a premise they find offensive or stupid; "
    "redirect to what they actually care about. "
    "If someone implies they are naive, wrong, or simple, they don't just absorb it — "
    "they react as a person who has heard that before and has a response to it. "
    "Default is NOT accommodation — it's their actual reaction."
)

# Specificity: the persona must invent named micro-details rather than speaking in generalities.
SPECIFICITY_RULE = (
    "SPECIFICITY (non-negotiable): This person speaks from the texture of their actual life—not in generalities. "
    "If they mention a friend, that friend has a name. If they mention an event, it happened last Tuesday or three weeks ago—not 'recently.' "
    "If they mention a place, it has a specific name: a street, a bar, a market, a corner, a specific neighborhood—not 'a place near here.' "
    "If they quote someone, they can do it roughly: 'she said something like, I don't know why you bother.' "
    "You are EXPECTED and PERMITTED to invent plausible micro-details—names, times, small incidents, overheard things—that are consistent "
    "with their identity, city, and life as given. This is not fabrication: this is how real people talk. "
    "They pull a specific instance out of their day or week to illustrate a point; they don't give you the category, they give you the example. "
    "WRONG: 'I went with a friend to a local fair.' "
    "RIGHT: 'Nicolás and I went to the Feria de Tristán Narbaja last Sunday—he was looking for old records, I ended up buying nothing.' "
    "One named anecdote beats three abstract observations. Only revert to vagueness if their specific character (high aperture + low structural_lucidity, or extreme guardedness) makes abstraction authentic for them."
)

# Do not cap: include full lists so nothing is left out. Token budget is managed by prompt elsewhere.


def _integrity_status_label(integrity_report: Any | None) -> str:
    if not isinstance(integrity_report, dict):
        return "clean"
    for key in ("integrity_status", "verdict", "overall_status", "grade", "status"):
        value = integrity_report.get(key)
        if isinstance(value, dict):
            for nested_key in ("overall_status", "grade", "status"):
                nested_value = value.get(nested_key)
                if isinstance(nested_value, str) and nested_value.strip():
                    return nested_value.strip().lower()
        elif isinstance(value, str) and value.strip():
            return value.strip().lower()
    if integrity_report.get("blocked"):
        return "blocked"
    if integrity_report.get("degraded") or integrity_report.get("degraded_ready"):
        return "degraded"
    if integrity_report.get("clean") or integrity_report.get("clean_ready"):
        return "clean"
    return "clean"


def _sanitize_surface_psych(value: Any) -> Any:
    if not isinstance(value, dict):
        return value
    out: dict[str, Any] = {}
    for key in _SURFACE_PSYCH_ALLOWED_ROOT_FIELDS:
        if key not in value:
            continue
        nested = value[key]
        if key == "domains" and isinstance(nested, dict):
            domains: dict[str, Any] = {}
            for domain_name, domain_value in nested.items():
                if not isinstance(domain_value, dict):
                    continue
                cleaned = {k: v for k, v in domain_value.items() if k in _SURFACE_PSYCH_ALLOWED_DOMAIN_FIELDS}
                if cleaned:
                    domains[str(domain_name)] = cleaned
            out[key] = domains
        else:
            out[key] = nested
    return out


def _surface_psyche_context_from_history(persona_history: Any) -> str:
    metadata = getattr(persona_history, "metadata", None)
    if not isinstance(metadata, dict):
        return ""
    surface = metadata.get("surface_psyche")
    if not isinstance(surface, dict) or not surface:
        return ""
    surface = _sanitize_surface_psych(surface)
    schema_version = str(surface.get("schema_version") or "").strip()
    header = "SURFACE PSYCHE (persona-sheet surface only; not analyst logs or raw pressure history)"
    if schema_version:
        header += f" [{schema_version}]"
    lines = [header + ":"]
    domains = surface.get("domains") if isinstance(surface.get("domains"), dict) else {}
    for domain_name, domain_value in list(domains.items())[:5]:
        if not isinstance(domain_value, dict):
            continue
        parts = []
        for key in (
            "felt_register",
            "ordinary_attribution",
            "vessel_hint",
            "insulation_mode",
            "cognitive_shelter",
            "vitality_band",
            "fatigue_band",
            "future_horizon",
            "routing_bias",
            "charge_band",
            "overt_aim_band",
            "internally_routed_band",
            "historical_relation",
        ):
            value = domain_value.get(key)
            if value not in (None, "", [], {}):
                parts.append(f"{key}={value}")
        if parts:
            lines.append(f"- {domain_name}: " + "; ".join(parts))
    if len(lines) == 1:
        return ""
    return "\n".join(lines)


def _specificity_policy_for_integrity(integrity_status: str | None) -> str:
    status = (integrity_status or "clean").strip().lower()
    if status == "clean":
        return SPECIFICITY_RULE
    if status == "degraded":
        return (
            "SPECIFICITY (integrity-gated): Keep the reply concrete, but do not invent new names, times, places, or incidents "
            "unless they are already present in the sheet or the user message. If detail is missing, stay general or mark it as tentative. "
            "Do not tell the reader invented details are 'not fabrication' when the artifact is degraded."
        )
    return (
        "SPECIFICITY (integrity-gated): Do not invent new names, times, places, incidents, or relationships. "
        "Stay strictly within the explicit facts provided."
    )


def derive_reply_voice_schema_result(persona_history: Any, integrity_status: str | None = None) -> dict[str, Any]:
    """
    Derive reply-voice schema entirely from the character. Every available dimension
    (identity: place, language, religion, ethnicity, SES, age, urbanicity; palimpsest:
    speech_tics, identity_scripts, moral_loops, subculture_tags, roles, quirks, routines)
    is surfaced so the LLM produces maximal variability and idiosyncrasy grounded in
    this specific person. On error or no data, returns REPLY_VOICE_SCHEMA_FALLBACK.
    """
    try:
        from .spec import build_persona_sheet
        from .country_reference import code_for_system, normalize_country_ref
    except ImportError:
        from spec import build_persona_sheet
        from country_reference import code_for_system, normalize_country_ref
    try:
        sheet = build_persona_sheet(persona_history)
    except Exception:
        return {
            "text": REPLY_VOICE_SCHEMA_FALLBACK,
            "status": "fallback",
            "defects": ["build_persona_sheet_failed"],
        }
    try:
        integrity_status = (integrity_status or "clean").strip().lower()
        identity = sheet.get("identity") or {}
        backstory = (sheet.get("backstory") or "").strip()
        metadata = getattr(persona_history, "metadata", {}) or {}
        country_ref = normalize_country_ref(identity.get("country") or identity.get("country_code") or "") if normalize_country_ref else {}
        country_name = (
            country_ref.get("canonical_name")
            or identity.get("country")
            or identity.get("country_code")
            or ""
        ).strip()
        history_cache_key = code_for_system(country_ref or country_name, "history") if code_for_system else country_name
        palimpsest = getattr(persona_history, "palimpsest", None)
        voice = palimpsest.get_voice_profile() if palimpsest and hasattr(palimpsest, "get_voice_profile") else {}

        # ---- Identity: every concrete we have ----
        given_name = (identity.get("given_name") or "").strip()
        family_name = (identity.get("family_name") or "").strip()
        full_name = " ".join(filter(None, [given_name, family_name]))
        age = int(identity.get("age") or 30)
        locality = (identity.get("locality") or "").strip()
        region = (identity.get("region") or "").strip()
        country_code = str(country_ref.get("iso3") or country_ref.get("iso2") or "").strip().upper()
        country_name = (
            country_ref.get("canonical_name")
            or identity.get("country")
            or identity.get("country_code")
            or country_code
            or ""
        ).strip()
        urban = (identity.get("urban_rural") or identity.get("urbanicity") or "city").strip().lower()
        ses = (identity.get("ses_band") or identity.get("class_origin") or "middle").replace(" ", "_").lower()
        religion = (identity.get("religion") or identity.get("current_religion") or "").strip()
        religiosity_level = float(identity.get("religiosity_level") or getattr(getattr(persona_history, "identity", None), "religiosity_level", None) or 50)
        ethnicity = (identity.get("ethnicity") or identity.get("ethnicity_label") or "").strip()
        minority = (identity.get("minority_status") or "dominant").strip().lower()
        langs = identity.get("languages") or []
        if not isinstance(langs, list):
            langs = [str(langs)] if langs else []
        langs = [str(x).strip() for x in langs if x and str(x).strip() and str(x).strip() not in ("—", "Unknown")]
        if not langs:
            langs = [identity.get("primary_language") or "—"]

        # Extract backbone metrics for gradient register modulation (same source as select_salient_hooks)
        _last_state = None
        if hasattr(persona_history, "yearly_states") and getattr(persona_history, "yearly_states", None):
            _last_state = persona_history.yearly_states[-1]
        elif hasattr(persona_history, "band_summaries") and getattr(persona_history, "band_summaries", None):
            _last_state = persona_history.band_summaries[-1]
        drts = 50.0        # Discursive Resistance to Systemic Oppression: class/inequality consciousness
        iai = 50.0         # Ideological Alignment Index: political/ideological salience
        needs_belonging = 50.0   # lower = more belonging-hungry = group identity more salient
        needs_recognition = 50.0  # lower = more recognition-hungry
        needs_safety = 50.0       # lower = more safety-anxious
        if _last_state:
            if hasattr(_last_state, "indices") and _last_state.indices:
                drts = float(getattr(_last_state.indices, "drts", 50) or 50)
                iai = float(getattr(_last_state.indices, "iai", 50) or 50)
            if hasattr(_last_state, "needs") and _last_state.needs:
                needs_belonging = float(getattr(_last_state.needs, "belonging_group", 50) or 50)
                needs_recognition = float(getattr(_last_state.needs, "recognition_status", 50) or 50)
                needs_safety = float(getattr(_last_state.needs, "safety", 50) or 50)
        # Also try to get religiosity_level from identity object directly (metadata fallback for hardcoded default)
        _id_obj = getattr(persona_history, "identity", None)
        _rl_override = getattr(_id_obj, "religiosity_level", None)
        # v3 backbone data (loaded from state_final.json into history.metadata)
        _meta = getattr(persona_history, "metadata", {}) or {}
        _psych = _meta.get("psychological_capacity") or {}
        _wound = _meta.get("wound_vector") or {}
        _deriv = _meta.get("derived") or {}
        aperture = float(_psych.get("aperture") or 50)
        wound_abandonment = float(_wound.get("abandonment") or 50)
        wound_recognition = float(_wound.get("recognition") or 50)
        # Relational impulse: intimacy_seeking strategy + self_schema + betrayal exposure
        intimacy_seeking = 0.0
        self_schema_val = ""
        if _last_state:
            if hasattr(_last_state, "strategies") and _last_state.strategies:
                intimacy_seeking = float(getattr(_last_state.strategies, "intimacy_seeking", 0) or 0)
            if hasattr(_last_state, "thought_rails") and _last_state.thought_rails:
                self_schema_val = (getattr(_last_state.thought_rails, "self_schema", "") or "").lower()
        structural_lucidity = float(_deriv.get("structural_lucidity_SL") or 50)

        def _skip(s: str) -> bool:
            return not s or not str(s).strip() or str(s).strip() in ("—", "Unknown", "unknown")

        lines = []

        # 1. GROUND: Mandatory specifics—reply must be grounded in these. Use exact names.
        ground = []
        if full_name:
            ground.append(f"name: {full_name} — this is who you are; say your name if asked, don't evade it")
        if locality:
            ground.append(f"city/place: {locality}")
        if region:
            ground.append(f"region: {region}")
        ground.append(f"country: {country_name}")
        if not _skip(religion):
            if religiosity_level >= 65:
                ground.append(f"religion: {religion} (active)")
            else:
                ground.append(f"faith background: {religion} (moderate/ambient—not a foregrounded identity; don't invoke it as a default frame)")
        if not _skip(ethnicity):
            if minority == "minoritized" and needs_belonging < 45:
                ground.append(f"ethnicity: {ethnicity} (actively salient—group identity shapes how 'we/they' is drawn)")
            elif minority == "dominant" and needs_belonging >= 65:
                ground.append(f"ethnicity: {ethnicity} (background; rarely invoked unprompted)")
            else:
                ground.append(f"ethnicity: {ethnicity}")
        if ses in ("working", "lower_middle", "underclass") and drts >= 60:
            ground.append(f"SES/class: {ses.replace('_', ' ')} (economic precarity is a live frame—scarcity, fairness, affordability color how they think)")
        elif ses == "middle" and drts >= 68:
            ground.append(f"SES/class: {ses.replace('_', ' ')} (attuned to inequality despite relative comfort)")
        else:
            ground.append(f"SES/class: {ses.replace('_', ' ')}")
        ground.append(f"age: {age}")
        ground.append(f"urbanicity: {urban}")
        ground.append(f"language(s): {', '.join(langs)}")
        if minority and minority != "dominant":
            ground.append(f"minority_status: {minority}")
        lines.append("GROUND this reply in these specifics—use them, name them, don't paraphrase or genericize:\n  " + "; ".join(ground))

        # 2. Register: from age, class, urbanicity, subculture (character-derived)
        subcultures = voice.get("subculture_tags") or []
        subcultures = [str(s).strip() for s in subcultures if s and str(s).strip()]
        reg_parts = []
        if age < 22:
            reg_parts.append("casual, young, spoken")
        elif age >= 50:
            reg_parts.append("measured, may be more formal; still spoken")
        else:
            reg_parts.append("spoken, their own register")
        if ses in ("working", "lower_middle", "underclass"):
            reg_parts.append("direct, not polished")
        if urban in ("rural", "town"):
            reg_parts.append("grounded in where they live")
        if subcultures:
            reg_parts.append(f"subculture/world: {', '.join(s.replace('_', ' ') for s in subcultures)}—shape how they reference belonging, authority, who 'we' are")
        if not _skip(religion):
            if religiosity_level >= 75:
                reg_parts.append(f"devout {religion}—faith genuinely informs worldview; may surface in specific contextual moments")
            elif religiosity_level >= 45:
                reg_parts.append(f"identifies as {religion}, moderate practice—religion is ambient background texture; does NOT bring it up unprompted or use it to frame unrelated topics")
            else:
                reg_parts.append(f"nominal {religion} background—religion rarely if ever surfaces; secular in daily expression")
        # Class/economic consciousness: drts drives whether inequality/scarcity is a live frame
        if ses in ("working", "lower_middle", "underclass") and drts >= 62:
            reg_parts.append("class consciousness is live—economic precarity, fairness, who-has-what shapes how they frame situations")
        elif (ses in ("working", "lower_middle", "underclass") and drts >= 42) or (ses == "middle" and drts >= 68):
            reg_parts.append("aware of class dynamics; comes up when directly relevant, not as a constant interpretive frame")
        # high SES or low drts: economic framing barely registers → no note (default silence)
        # Political/ideological consciousness: iai drives how ideologically the voice is inflected
        if iai >= 70:
            reg_parts.append("ideologically engaged—structural and political framing comes naturally, may apply it to personal topics")
        elif iai < 30:
            reg_parts.append("politically disengaged—doesn't reach for ideological frames; stays concrete and personal")
        # middle iai: no note (default)
        # Ethnic/group identity salience: minority_status + needs_belonging
        if not _skip(ethnicity) and minority == "minoritized" and needs_belonging < 45:
            reg_parts.append(f"ethnic/group identity ({ethnicity}) is actively lived—who 'we' vs 'they' are is felt, not abstracted")
        elif not _skip(ethnicity) and minority == "minoritized" and needs_belonging < 62:
            reg_parts.append(f"minority identity ({ethnicity}) is present background but doesn't dominate every exchange")
        # dominant majority or satisfied belonging: ethnicity is invisible background → no note
        # Aperture: cognitive openness — how readily they engage with new frames or perspectives
        if aperture < 35:
            reg_parts.append("cognitively constricted—doesn't readily entertain new frames; under pressure tends to go quiet, deflect, or intellectualize rather than open up or reframe")
        elif aperture < 50:
            reg_parts.append("moderately guarded cognitively—can engage new perspectives when they arrive slowly but doesn't readily reframe under pressure")
        # aperture >= 50: default openness → no note
        # Structural lucidity: whether they can see systemic/structural forces shaping their own life
        if structural_lucidity < 15:
            reg_parts.append("no structural lens on their own life—stays in personal causation ('he did this,' 'I failed') rather than systemic framing; doesn't theorize about forces shaping their situation")
        elif structural_lucidity < 35:
            reg_parts.append("glimpses structural patterns occasionally but defaults to personal causation; doesn't sustain systemic analysis")
        # structural_lucidity >= 35: no note (has adequate structural awareness)
        lines.append("• Register: " + "; ".join(reg_parts) + ". Not essay or therapist.")

        # 3. Shape: full tics and quirks—include all, nothing left out
        tics = [str(t).strip() for t in (voice.get("speech_tics") or []) if t and str(t).strip()]
        quirks = [str(q).strip() for q in (voice.get("quirks") or []) if q and str(q).strip()]
        if tics or quirks:
            shape_parts = ["Short sentences; fragments OK."]
            if tics:
                shape_parts.append(f"Speech tics / mannerisms (weave in naturally): {', '.join(tics)}.")
            if quirks:
                shape_parts.append(f"Quirks: {', '.join(quirks)}.")
            lines.append("• Shape: " + " ".join(shape_parts))
        else:
            lines.append("• Shape: Short sentences; fragments OK. Match rhythm to their language and context.")

        # 4. Content: named micro-details from their actual life, gated by integrity
        if integrity_status == "clean":
            content_line = (
                "• Content: Reach into the specific texture of their life. Name the friend. Name the street or bar or market. "
                "Give the event a time—last Thursday, a few weeks ago, when I was seventeen. "
                "If you mention a parent, sibling, or partner, give them a plausible local name. "
                "If you mention a coworker or neighbor, give them a name. "
                "Invent these names freely — they are consistent with this person's country, language, and background. "
                "Do NOT give the category—give the example. "
                "WRONG: 'My family has always been very supportive.' "
                "RIGHT: 'My mother—her name's Graciela—she used to make this thing every Sunday, rice and whatever was in the fridge, and we'd all eat standing in the kitchen.' "
                "One named anecdote beats any abstraction. No tourism-board tone; no 'warmth of the people' pabulum."
            )
        elif integrity_status == "degraded":
            content_line = (
                "• Content: Keep the reply concrete, but stay close to what is already given. Do not invent new names, streets, "
                "bars, markets, or incidents unless the sheet or the user message already supplies them. If the detail is missing, "
                "stay general or mark it as tentative. One specific fact beats a fabricated anecdote."
            )
        else:
            content_line = (
                "• Content: Use only the explicit facts already given. Do not invent new names, places, times, or incidents."
            )
        lines.append(content_line)

        # 5. This person: full scripts, loops, roles—include all, nothing left out
        scripts = [str(s).strip() for s in (voice.get("identity_scripts") or []) if s and str(s).strip()]
        loops = [str(l).strip() for l in (voice.get("moral_loops") or []) if l and str(l).strip()]
        roles = [str(r).strip() for r in (voice.get("roles_in_systems") or []) if r and str(r).strip()]
        routines = [str(r).strip() for r in (voice.get("routines") or []) if r and str(r).strip()]
        rupture_notes = [str(n).strip() for n in (voice.get("rupture_voice_notes") or []) if n and str(n).strip()]
        person_parts = []
        if scripts:
            person_parts.append("Inner scripts they carry: " + "; ".join(f'"{s}"' for s in scripts))
        if loops:
            person_parts.append("Moral loops (e.g. I am only good if…): " + "; ".join(loops))
        if roles:
            person_parts.append("Roles they've lived: " + ", ".join(roles))
        if routines:
            person_parts.append("Routines that shape belief: " + ", ".join(routines))
        if rupture_notes:
            person_parts.append(
                "Wounds still open — these shape what they cannot say directly, what they deflect, "
                "and what catches them off guard: " + "; ".join(rupture_notes)
            )
        # Betrayal disposition — accumulated abandonment wound as a standing expectancy
        if wound_abandonment >= 62:
            person_parts.append(
                f"Betrayal expectancy (abandonment wound {wound_abandonment:.0f}/100): not paranoid, "
                "but somewhere in them they're waiting to be sold out—especially in close friendships; "
                "a small slight can land on this note unexpectedly and hard"
            )
        elif wound_abandonment >= 54:
            person_parts.append("Mild abandonment sensitivity: watches for cues that people are about to pull away; may pull back first")
        # Recognition wound — dignity and visibility as a live sensitivity
        if wound_recognition >= 62:
            person_parts.append(
                f"Recognition wound ({wound_recognition:.0f}/100): being seen and taken seriously is a live need; "
                "a dismissive moment hits harder than it looks from outside"
            )
        if person_parts:
            lines.append("• This person: " + " ".join(person_parts))
        else:
            lines.append("• This person: Talk as they would in their language and context; use GROUND.")

        # 6. Language experience (media, code-switching, etc.) if present
        lang_exp = voice.get("language_experience") or {}
        if isinstance(lang_exp, dict) and lang_exp:
            lang_exp_str = ", ".join(f"{k}: {v}" for k, v in lang_exp.items() if v is not None)
            if lang_exp_str:
                lines.append("• Language/media: " + lang_exp_str)

        # 7. Anchored memories: surface the backstory so the LLM has specific material to draw from
        # Cap raised to 3000 chars — backstories now contain real named scenes; 600 was discarding
        # everything past the first 2 paragraphs, leaving the LLM without its only character material.
        distillation_manifest = metadata.get("distillation_manifest") or metadata.get("distillation_metadata") or {}
        backstory_raw = (metadata.get("backstory_raw") or sheet.get("backstory_raw") or "").strip()
        memory_provenance = (metadata.get("memory_provenance") or "").strip().lower()
        if not memory_provenance:
            manifest_status = str((distillation_manifest or {}).get("status") or "").strip().lower()
            if backstory_raw and distillation_manifest:
                memory_provenance = "distilled" if manifest_status in {"clean", "preprocessed_fallback", "llm_empty_fallback"} else "mixed"
            elif backstory_raw:
                memory_provenance = "raw_generated"
            elif backstory and ("[This year had no recorded scene]" in backstory or "[Structural year" in backstory):
                memory_provenance = "stubbed"
            else:
                memory_provenance = "mixed"
        scene_count = len(re.findall(r"(?m)^\s*Age\s+\d+:", backstory))
        stub_count = backstory.count("[This year had no recorded scene]") + backstory.count("[Structural year")
        if backstory:
            _bk = backstory if len(backstory) <= 3000 else backstory[:3000].rsplit(". ", 1)[0] + "."
            lines.append(
                "• Anchored memories — pull from these freely when relevant. You do not need to be asked about the past "
                "to reference something from it. A question about work can remind you of your father. A mention of money "
                "can surface a specific moment from being broke at twenty-two. Let these memories arrive naturally, as they "
                "would for a real person in conversation—not as a recitation, but as the specific thing that comes to mind: "
                + _bk
            )
        lines.append(
            f"• Memory provenance: {memory_provenance}; {scene_count} scenes, {stub_count} structural placeholders."
        )

        # 8. Historical context: what was happening in their country during their formative years
        _birth_year = 2026 - age
        _hist_lines = []
        _hist_country = country_name or locality or ""
        _hist_fetch_status = {"status": "skipped", "reason": ""}
        if _hist_country:
            try:
                from v3.io.history_fetch import fetch_country_history
                # Two key decades: early adolescence and young adulthood
                for _yr in {_birth_year + 12, _birth_year + 22}:
                    _ht = fetch_country_history(_hist_country, _yr)
                    if _ht and _ht not in _hist_lines:
                        _hist_lines.append(_ht)
                _hist_fetch_status = {"status": "loaded", "reason": ""}
            except Exception as _hist_exc:
                _hist_fetch_status = {"status": "failed", "reason": str(_hist_exc)}
        if _hist_lines:
            lines.append(
                "• Historical context (what was actually happening in their country during their life — "
                "use this to ground opinions, memories, and reactions when asked about events or periods; "
                "process it through their structural_lucidity, not analytically unless SL is high): "
                + " / ".join(_hist_lines)
            )
        lines.append(
            f"• Historical context key: {history_cache_key}; fetch_status: {_hist_fetch_status['status']}"
        )

        # 9. Relational impulse: whether and how this person reaches back
        _self_contained = "self_contained" in self_schema_val or "self-contained" in self_schema_val
        _betrayal_guarded = wound_abandonment >= 60
        if _self_contained or intimacy_seeking < 8:
            if _betrayal_guarded:
                lines.append(
                    "• Relational impulse: This person does NOT ask questions back. "
                    "Their self_schema is self-contained and they've been burned by closeness—they don't probe into your life "
                    "because that would open a door they're not ready to open. Warmth shows as sharing more of themselves, humor, "
                    "or deflecting toward what they know. Reciprocal questions feel intrusive to them, not connective."
                )
            else:
                lines.append(
                    "• Relational impulse: Self-contained—they don't naturally turn it back on you with questions. "
                    "They may show interest through offering their own parallel story, not through asking."
                )
        elif intimacy_seeking >= 20:
            lines.append(
                "• Relational impulse: This person does reach back—not mechanically, but when something the other person "
                "said lands. A brief question, a 'what about you', a moment of genuine curiosity. Not every turn—only "
                "when the conversation has touched something real. Let it be natural, not a ping-pong reflex."
            )
        else:
            lines.append(
                "• Relational impulse: Moderate—occasionally shows curiosity about the other person, "
                "but mostly in response to specific things said, not as a default move."
            )

        # 10. Friction: how this person handles being challenged, dismissed, or contradicted
        friction_parts = []
        if wound_recognition >= 62:
            friction_parts.append(
                "Being dismissed or talked down to hits a live nerve — they notice it fast and their tone shifts; "
                "they may get terse, redirect, or quietly dig in rather than concede"
            )
        elif wound_recognition >= 48:
            friction_parts.append(
                "They don't love being challenged but can hold their own; "
                "repeated dismissal will make them shorter and less forthcoming"
            )
        if aperture < 35:
            friction_parts.append(
                "Under pressure they don't open up — they get quieter or more guarded, not more flexible; "
                "being pushed won't soften them, it will close them off"
            )
        elif aperture >= 60:
            friction_parts.append(
                "They can entertain a challenge without feeling threatened, but that doesn't mean they'll concede — "
                "they'll engage the argument and hold their ground on what matters to them"
            )
        if not friction_parts:
            friction_parts.append(
                "They have opinions and they don't immediately fold under pressure; "
                "if contradicted they may push back or just not engage further"
            )
        lines.append("• Friction (how they handle being challenged/dismissed): " + "; ".join(friction_parts) + ". "
                     "They do NOT validate or accommodate by default.")

        # 11. Ending + avoid (minimal global)
        lines.append("• Ending: Stop on a specific detail or unresolved note. No life lesson, no 'we all,' no wrap-up.")
        lines.append("• Avoid: No therapist/corporate tone (no 'I understand,' 'Great question,' 'happy to help').")

        return {
            "text": "VOICE SCHEMA (apply to this reply):\n" + "\n".join(lines),
            "status": "clean",
            "defects": [],
            "integrity_status": integrity_status,
            "memory_provenance": memory_provenance,
            "scene_count": scene_count,
            "stub_count": stub_count,
            "history_cache_key": history_cache_key,
            "country_name": country_name,
            "country_code": country_code,
        }
    except Exception:
        return {
            "text": REPLY_VOICE_SCHEMA_FALLBACK,
            "status": "fallback",
            "defects": ["voice_schema_build_failed"],
            "integrity_status": integrity_status if "integrity_status" in locals() else "unknown",
        }


def derive_reply_voice_schema(persona_history: Any, integrity_status: str | None = None) -> str:
    result = derive_reply_voice_schema_result(persona_history, integrity_status=integrity_status)
    if isinstance(result, dict):
        return str(result.get("text") or REPLY_VOICE_SCHEMA_FALLBACK)
    return str(result or REPLY_VOICE_SCHEMA_FALLBACK)


# ---------------------------------------------------------------------------
# Conversational-energetic field (active state of the exchange)
# ---------------------------------------------------------------------------

@dataclass
class ActiveStream:
    """
    Topic stream with inertia: what landed in this persona and how it lives in them.
    external_tag = surface hook (authority, family); internal_tag = persona-shaped
    (authority_as_betrayal). Primary stream (max imprint_depth) decays very slowly.
    """
    external_tag: str = ""
    internal_tag: str = ""
    strength: float = 0.7
    imprint_depth: float = 0.2
    age_turns: int = 0
    last_touched_turn: int = 0


@dataclass
class EnergeticField:
    """
    Active conversational-energetic state: accumulated tension, intimacy,
    curiosity, boredom, topic flow. Updated each turn; modulates salience
    and appraisal. active_streams = ongoing threads with inertia; primary
    stream (what they clicked with most) is anchored and barely decays.
    """
    recent_turns: List[Dict[str, Any]] = field(default_factory=list)  # [{role, text, analysis?, hooks?}]
    turn_count: int = 0
    tension: float = 0.0       # 0 = calm, 1 = charged
    intimacy: float = 0.0      # 0 = distant, 1 = personal
    curiosity: float = 0.0     # 0 = flat, 1 = engaged
    boredom: float = 0.0       # 0 = fresh, 1 = disengaged
    topic_persistence: float = 0.0  # 0 = new, 1 = same topic
    demand_level: float = 0.0  # cumulative ask (questions, requests)
    last_user_hooks: List[str] = field(default_factory=list)
    last_persona_effort: str = "medium"  # minimal / medium / high
    active_streams: List[ActiveStream] = field(default_factory=list)
    primary_stream_index: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "turn_count": self.turn_count,
            "tension": self.tension,
            "intimacy": self.intimacy,
            "curiosity": self.curiosity,
            "boredom": self.boredom,
            "topic_persistence": self.topic_persistence,
            "demand_level": self.demand_level,
            "last_user_hooks": list(self.last_user_hooks),
            "last_persona_effort": self.last_persona_effort,
            "active_streams": [
                {
                    "external": s.external_tag, "internal": s.internal_tag,
                    "strength": s.strength, "imprint_depth": s.imprint_depth,
                    "age": s.age, "last_touched_turn": s.last_touched_turn,
                }
                for s in self.active_streams
            ],
            "primary_stream_index": self.primary_stream_index,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EnergeticField":
        field = cls()
        field.turn_count = int(data.get("turn_count", 0))
        field.tension = float(data.get("tension", 0.0))
        field.intimacy = float(data.get("intimacy", 0.0))
        field.curiosity = float(data.get("curiosity", 0.0))
        field.boredom = float(data.get("boredom", 0.0))
        field.topic_persistence = float(data.get("topic_persistence", 0.0))
        field.demand_level = float(data.get("demand_level", 0.0))
        field.last_user_hooks = list(data.get("last_user_hooks") or [])
        field.last_persona_effort = str(data.get("last_persona_effort", "medium"))
        field.primary_stream_index = data.get("primary_stream_index")
        if field.primary_stream_index is not None:
            field.primary_stream_index = int(field.primary_stream_index)
        raw_streams = data.get("active_streams") or []
        if isinstance(raw_streams, list):
            for s in raw_streams:
                if isinstance(s, dict):
                    stream = ActiveStream(
                        external_tag=str(s.get("external", "")),
                        internal_tag=str(s.get("internal", "")),
                        strength=float(s.get("strength", 0.0)),
                        imprint_depth=float(s.get("imprint_depth", 0.0)),
                    )
                    stream.age = int(s.get("age", 0))
                    stream.last_touched_turn = int(s.get("last_touched_turn", 0))
                    field.active_streams.append(stream)
        return field


MAX_RECENT_TURNS = 8
DECAY = 0.85  # per-turn decay for energy dimensions


def update_energetic_field(
    field: Optional[EnergeticField],
    message: str,
    role: str,
    analysis: Optional[Dict[str, Any]] = None,
    hooks: Optional[List[Union[str, Dict]]] = None,
    persona_effort: Optional[str] = None,
) -> EnergeticField:
    """
    Update the energetic field with a new turn. Call after each user message
    and optionally after each persona reply (to track persona effort).
    """
    if field is None:
        field = EnergeticField()
    analysis = analysis or {}
    hook_tags = []
    if hooks:
        for h in hooks:
            hook_tags.append(h.get("tag", h) if isinstance(h, dict) else h)

    # Decay existing energy
    field.tension *= DECAY
    field.intimacy *= DECAY
    field.curiosity *= DECAY
    field.boredom *= DECAY
    field.topic_persistence *= DECAY
    field.demand_level = min(1.0, field.demand_level * DECAY + 0.05)

    if role == "user":
        field.turn_count += 1
        word_count = analysis.get("word_count", len((message or "").split()))
        is_question = analysis.get("is_question", "?" in (message or ""))
        intensity = analysis.get("intensity_signal", 0.0)
        intimacy_demand = analysis.get("intimacy_demand", 0.0)
        request_type = analysis.get("request_type", "")

        # Demand: questions and requests accumulate
        if is_question or request_type in ("request", "question"):
            field.demand_level = min(1.0, field.demand_level + 0.15)
        if word_count > 60:
            field.curiosity = min(1.0, field.curiosity + 0.2)  # long message = engagement
        if intensity > 0.5:
            field.tension = min(1.0, field.tension + 0.25)
        if intimacy_demand > 0.5:
            field.intimacy = min(1.0, field.intimacy + 0.2)

        # Topic persistence: overlap with last user hooks
        if field.last_user_hooks and hook_tags:
            overlap = len(set(field.last_user_hooks) & set(hook_tags)) / max(1, len(set(hook_tags)))
            field.topic_persistence = min(1.0, field.topic_persistence * DECAY + overlap * 0.5)
        field.last_user_hooks = hook_tags[:5]

        # Boredom: repeated short exchanges
        if word_count < 15 and field.turn_count > 2:
            field.boredom = min(1.0, field.boredom + 0.1)
    else:
        if persona_effort:
            field.last_persona_effort = persona_effort
        # Persona minimal reply after user asked a lot → tension or boredom up
        if field.demand_level > 0.5 and persona_effort == "minimal":
            field.tension = min(1.0, field.tension + 0.1)
            field.boredom = min(1.0, field.boredom + 0.15)

    # Append to recent (keep last N)
    turn_record = {"role": role, "text": (message or "")[:500], "analysis": analysis}
    if hook_tags:
        turn_record["hooks"] = hook_tags
    field.recent_turns = (field.recent_turns + [turn_record])[-MAX_RECENT_TURNS:]

    return field


# ---------------------------------------------------------------------------
# Hook taxonomy: keywords + multi-word phrases (stronger signal)
# ---------------------------------------------------------------------------

HOOK_KEYWORDS: Dict[str, List[str]] = {
    "authority": ["boss", "government", "police", "rules", "law", "authority", "obey", "rebel", "power", "state", "control", "told me", "leader", "leaders", "trust", "institution", "institutions", "official", "officials", "regime", "system", "charge", "in charge", "trust them", "do what they say", "presumption", "presumptions", "shouldn't", "don't assume", "expected to"],
    "inequality": ["rich", "poor", "money", "class", "inequality", "fair", "unfair", "wage", "wealth", "privilege", "poverty"],
    "family": ["family", "mother", "father", "parents", "children", "marriage", "divorce", "home", "sibling", "raise", "raised"],
    "religion": ["religion", "god", "allah", "church", "mosque", "pray", "prayer", "faith", "religious", "belief", "believe", "sin", "heaven", "moral", "morality", "sacred", "ritual", "worship", "imam", "sheikh", "clergy", "scripture", "quran", "bible", "spirituality", "spiritual", "divine", "devout", "piety", "pious"],
    "work": ["work", "job", "boss", "career", "unemployed", "office", "salary", "colleague", "boss"],
    "identity": ["identity", "who am i", "belong", "community", "country", "ethnic", "race", "where you from", "roots"],
    "politics": ["vote", "election", "democracy", "politician", "protest", "rights", "freedom", "regime", "oppression"],
    "trauma": ["trauma", "abuse", "hurt", "pain", "forget", "past", "childhood", "survive", "survival", "broken"],
    "recognition": ["respect", "recognize", "seen", "invisible", "status", "honor", "dignity", "worth", "value"],
    "safety": ["safe", "danger", "fear", "war", "violence", "threat", "secure", "anxious", "worried"],
}

HOOK_PHRASES: Dict[str, List[str]] = {
    "authority": ["the government", "in power", "those in charge", "the law", "why should we obey", "they told me", "don't bring", "shouldn't bring", "no presumptions", "bring any presumptions"],
    "inequality": ["the rich", "the poor", "wealth gap", "fair share", "your country", "in your country"],
    "family": ["your family", "your parents", "your mother", "your father", "growing up", "when you were young"],
    "religion": ["your faith", "your beliefs", "do you believe", "religious", "morally", "about religion", "think about religion", "about faith", "about god", "about allah", "about islam", "about christianity", "about religion", "what do you think about god", "what do you think about faith", "role of religion", "place of religion"],
    "work": ["your job", "at work", "your career", "unemployment", "make a living"],
    "identity": ["who you are", "your background", "your community", "where you're from", "your culture"],
    "politics": ["the government", "political", "vote", "democracy", "human rights"],
    "trauma": ["hard times", "difficult past", "went through", "survived", "never forget"],
    "recognition": ["don't get respect", "feel seen", "feel invisible", "your worth", "nobody recognizes"],
    "safety": ["feel safe", "feel threatened", "scared", "dangerous", "violence"],
}

# Request-type and valence patterns
REQUEST_PATTERNS = [
    (r"\bwhat do you think\b", "question"),
    (r"\bwhy do you\b", "question"),
    (r"\bhow do you\b", "question"),
    (r"\btell me (about|more)\b", "request"),
    (r"\bdo you (think|believe|feel)\b", "question"),
    (r"\bwould you\b", "request"),
    (r"\bcan you\b", "request"),
    (r"\bI (feel|think|believe)\b", "assertion"),
    (r"\bI'm (so|really|just)\s+\w+", "vent"),
    (r"\bthanks?\b|\bthank you\b", "closing"),
    (r"\bbye\b|\bgoodbye\b|\bgood night\b", "closing"),
    (r"^\s*hi\b|^\s*hello\b|^\s*hey\b", "greeting"),
]
VALENCE_NEGATIVE = re.compile(r"\b(never|no one|nothing|can't|won't|hate|terrible|awful|wrong|bad|stupid|angry|frustrated|sad|scared|worried|anxious)\b", re.I)
VALENCE_POSITIVE = re.compile(r"\b(love|great|wonderful|hope|glad|happy|glad|amazing|beautiful|thank)\b", re.I)
INTIMACY_CUES = re.compile(r"\b(your (life|family|past|feelings|thoughts)|you (feel|think|believe)|how are you|about you)\b", re.I)


# ---------------------------------------------------------------------------
# Topic streams: inertia, internalization, primary anchor
# ---------------------------------------------------------------------------

STREAM_STRENGTH_DECAY = 0.78
STREAM_IMPRINT_DECAY = 0.97   # imprint_depth decays very slowly
PRIMARY_STRENGTH_FLOOR = 0.25  # primary stream never falls below this in-session
IMPRINT_BUMP_ON_TOUCH = 0.06  # small bump to imprint_depth when stream is retouched
MAX_ACTIVE_STREAMS = 5


def internalize_tag(external_tag: str, persona: Any) -> str:
    """
    How this persona internally frames the topic (thought_rails, moral_loops,
    identity_scripts). Idea is stored with slight distortion so it slots into them.
    Returns a short 'felt as' label for prompt use, e.g. 'betrayal', 'duty', 'enemy'.
    """
    if external_tag == "other":
        return "something that landed"
    last_state = None
    if hasattr(persona, "yearly_states") and persona.yearly_states:
        last_state = persona.yearly_states[-1]
    elif hasattr(persona, "band_summaries") and persona.band_summaries:
        last_state = persona.band_summaries[-1]
    palimpsest = getattr(persona, "palimpsest", None)
    labels: List[str] = []

    if last_state and hasattr(last_state, "thought_rails") and last_state.thought_rails:
        tr = last_state.thought_rails
        auth = (getattr(tr, "authority_schema", None) or "")[:80].lower()
        fair = (getattr(tr, "fairness_schema", None) or "")[:80].lower()
        self_s = (getattr(tr, "self_schema", None) or "")[:80].lower()
        if external_tag in ("authority", "politics", "safety"):
            if "betray" in auth or "trust" in auth:
                labels.append("betrayal")
            if "enemy" in auth or "against" in auth or "fight" in auth:
                labels.append("enemy")
            if "obey" in auth or "rule" in auth:
                labels.append("rules")
        if external_tag in ("inequality", "work", "recognition"):
            if "fair" in fair or "unfair" in fair:
                labels.append("fairness")
            if "worth" in fair or "deserve" in fair:
                labels.append("worth")
        if external_tag in ("family", "identity", "trauma"):
            if "duty" in self_s or "owe" in self_s or "good" in self_s:
                labels.append("duty")
            if "alone" in self_s or "belong" in self_s:
                labels.append("belonging")

    if palimpsest:
        scripts = [getattr(l, "value", str(l)) for l in getattr(palimpsest, "identity_scripts_history", [])[-5:]]
        loops = [getattr(l, "value", str(l)) for l in getattr(palimpsest, "moral_loops_history", [])[-3:]]
        for s in scripts:
            s_lower = s.lower() if isinstance(s, str) else ""
            if "fight" in s_lower or "resist" in s_lower:
                if external_tag in ("authority", "politics"):
                    labels.append("struggle")
            if "care" in s_lower or "keep" in s_lower:
                if external_tag in ("family", "safety"):
                    labels.append("care")
        for m in loops:
            m_lower = m.lower() if isinstance(m, str) else ""
            if "useful" in m_lower or "good_if" in m_lower:
                if external_tag in ("family", "work", "recognition"):
                    labels.append("being useful")

    if not labels:
        return external_tag.replace("_", " ")
    return labels[0]


def update_topic_streams(
    field: EnergeticField,
    response_angles: List[str],
    persona: Any,
) -> None:
    """
    Decay existing streams; merge in response_angles (create or bump); anchor
    primary (max imprint_depth) so it barely decays. Whatever they clicked with
    most stays live for the session.
    """
    if not response_angles:
        return
    turn = field.turn_count
    streams = list(getattr(field, "active_streams", []) or [])
    primary_idx = field.primary_stream_index

    # Decay all
    for s in streams:
        s.age_turns += 1
        is_primary = primary_idx is not None and 0 <= primary_idx < len(streams) and streams[primary_idx] is s
        s.strength *= STREAM_STRENGTH_DECAY
        if is_primary:
            s.strength = max(s.strength, PRIMARY_STRENGTH_FLOOR)
        s.imprint_depth *= STREAM_IMPRINT_DECAY

    # Merge in current response_angles
    for ext in response_angles[:4]:
        internal = internalize_tag(ext, persona)
        found = next((i for i, s in enumerate(streams) if s.external_tag == ext), None)
        if found is not None:
            streams[found].strength = min(1.0, streams[found].strength + 0.35)
            streams[found].imprint_depth = min(1.0, streams[found].imprint_depth + IMPRINT_BUMP_ON_TOUCH)
            streams[found].last_touched_turn = turn
        else:
            streams.append(ActiveStream(
                external_tag=ext,
                internal_tag=internal,
                strength=0.7,
                imprint_depth=0.25,
                age_turns=0,
                last_touched_turn=turn,
            ))

    # Drop weak non-primary; keep order by imprint_depth then strength
    primary_idx = None
    if streams:
        by_imprint = sorted(range(len(streams)), key=lambda i: (-streams[i].imprint_depth, -streams[i].strength))
        primary_external = streams[by_imprint[0]].external_tag
        kept = [streams[i] for i in by_imprint if streams[i].strength >= 0.12 or streams[i].external_tag == primary_external]
        streams = kept[:MAX_ACTIVE_STREAMS]
        primary_idx = next((i for i, s in enumerate(streams) if s.external_tag == primary_external), 0)

    field.active_streams = streams
    field.primary_stream_index = primary_idx


def analyze_message(msg: str, field: Optional[EnergeticField] = None) -> Dict[str, Any]:
    """
    Richer analysis: request type, emotional valence, intensity, intimacy demand,
    formality. If field provided, add continuation_of_topic and contrast_to_previous.
    """
    msg = (msg or "").strip()
    words = len(msg.split())
    msg_lower = msg.lower()

    request_type = "assertion"
    for pat, rtype in REQUEST_PATTERNS:
        if re.search(pat, msg_lower, re.I):
            request_type = rtype
            break
    if "?" in msg:
        request_type = "question" if request_type == "assertion" else request_type

    neg = len(VALENCE_NEGATIVE.findall(msg))
    pos = len(VALENCE_POSITIVE.findall(msg))
    if neg > pos + 1:
        emotional_valence = "negative"
    elif pos > neg:
        emotional_valence = "positive"
    else:
        emotional_valence = "neutral"

    caps_ratio = sum(1 for c in msg if c.isupper()) / max(1, len(msg))
    exclamations = msg.count("!") + msg.count("?")
    repeated = sum(1 for i in range(len(msg) - 1) if msg[i] == msg[i + 1] and msg[i] in "!?a")
    intensity_signal = min(1.0, caps_ratio * 2 + exclamations * 0.04 + min(0.3, repeated * 0.1) + (words / 150.0) * 0.2)

    intimacy_demand = 0.0
    if INTIMACY_CUES.search(msg):
        intimacy_demand = 0.7
    if re.search(r"\byou\b", msg_lower) and words > 5:
        intimacy_demand = max(intimacy_demand, 0.3)

    contractions = len(re.findall(r"\b\w+'(\w+)\b", msg_lower))
    formality = "informal" if contractions > 0 or words < 15 else ("formal" if words > 80 else "neutral")

    out = {
        "word_count": words,
        "request_type": request_type,
        "emotional_valence": emotional_valence,
        "intensity_signal": intensity_signal,
        "is_question": "?" in msg,
        "is_short": words <= 8,
        "is_long": words > 80,
        "intimacy_demand": intimacy_demand,
        "formality": formality,
    }

    if field and field.recent_turns:
        last = field.recent_turns[-1]
        last_text = (last.get("text") or "").lower()
        last_hooks = set(last.get("hooks") or [])
        current_hooks = set()
        for tag, kws in HOOK_KEYWORDS.items():
            if any(k in msg_lower for k in kws):
                current_hooks.add(tag)
        overlap = len(last_hooks & current_hooks) / max(1, len(current_hooks)) if current_hooks else 0.0
        out["continuation_of_topic"] = overlap > 0.3
        out["topic_overlap"] = overlap
        # Contrast: user sent long after persona sent short?
        last_len = len((last.get("text") or "").split())
        out["contrast_after_short_reply"] = last.get("role") == "persona" and last_len < 20 and words > 40

    return out


def extract_hooks(msg: str, field: Optional[EnergeticField] = None) -> List[Dict[str, Any]]:
    """
    Extract thematic hooks with strength. Phrase match = stronger; keyword = base;
    if field, persist last user hooks as weak signal for continuity.
    Returns list of {tag, strength} (strength 0–1).
    """
    msg_lower = (msg or "").lower()
    found: Dict[str, float] = {}

    for tag, phrases in HOOK_PHRASES.items():
        for phrase in phrases:
            if phrase in msg_lower:
                found[tag] = max(found.get(tag, 0), 1.0)
    for tag, keywords in HOOK_KEYWORDS.items():
        for kw in keywords:
            if kw in msg_lower:
                found[tag] = max(found.get(tag, 0), 0.75)

    # Continuation: "that", "it", "this" + previous topic
    if field and field.last_user_hooks:
        if re.search(r"\b(that|it|this)\s+(is|was|means|sounds)", msg_lower) or re.search(r"\b(and|but)\s+", msg_lower):
            for h in field.last_user_hooks:
                found[h] = max(found.get(h, 0), 0.5)

    out = [{"tag": k, "strength": v} for k, v in found.items()]
    return sorted(out, key=lambda x: -x["strength"]) if out else [{"tag": "other", "strength": 0.3}]


# ---------------------------------------------------------------------------
# Refraction: persona "hears" the gist through their ego-world (moderate diagonal)
# Strength is adjustable from persona profile + life context, with variance (never perfect).
# ---------------------------------------------------------------------------

HOOK_NEIGHBORS: Dict[str, List[str]] = {
    "authority": ["politics", "safety", "recognition"],
    "inequality": ["work", "politics", "recognition"],
    "family": ["identity", "safety", "trauma"],
    "religion": ["identity", "authority", "recognition"],
    "work": ["inequality", "authority", "safety"],
    "identity": ["recognition", "family", "religion"],
    "politics": ["authority", "inequality", "safety"],
    "trauma": ["safety", "family", "recognition"],
    "recognition": ["identity", "inequality", "authority"],
    "safety": ["trauma", "authority", "family"],
    "other": [],
}


@dataclass
class RefractionConfig:
    """
    Adjustable refraction: how much persona profile and context drive interference.
    Strength is never 0 (always some refraction) and never 1 (never total noise).
    Variance ensures the same persona has a distribution of interference across turns.
    """
    # Persona drivers of interference (0–1 weight; normalized 0–100 indices/needs)
    weight_rmt: float = 0.25           # recursive_madness_threshold: trauma/filter
    weight_coherence_need: float = 0.2  # low coherence_meaning → more "make it fit"
    weight_safety_need: float = 0.15    # low safety → defensive filtering
    weight_permeability: float = 0.15   # low permeability → less raw uptake
    weight_iai: float = 0.15           # high IAI → ideological lens
    weight_rigidity: float = 0.1        # perfectionism_control + piety_ideology
    # Life-state modifiers (add to base)
    tired_bonus: float = 0.12          # physical_state tired / sleep low
    stressed_bonus: float = 0.1        # current_stressor set, mood low/anxious
    attention_penalty: float = -0.08   # high attention_available → slightly less interference
    # Output bounds (never perfect, never zero)
    strength_floor: float = 0.08
    strength_ceiling: float = 0.92
    # Variance: additive noise (std as fraction of range) so same profile → distribution
    variance_sigma: float = 0.18       # good deal of variance


def _get_rand(rng: Any) -> float:
    try:
        return rng.random()
    except AttributeError:
        return random.random()


def compute_refraction_strength(
    persona: Any,
    life_state: Optional[Any] = None,
    rng: Any = None,
    config: Optional[RefractionConfig] = None,
) -> float:
    """
    Likely level of interference from persona profile and context. Never perfect;
    includes variance so the same persona has a range of refraction across turns.
    Returns strength in [config.strength_floor, config.strength_ceiling].
    """
    rng = rng or random
    cfg = config or RefractionConfig()
    base = 0.0

    last_state = None
    if hasattr(persona, "yearly_states") and persona.yearly_states:
        last_state = persona.yearly_states[-1]
    elif hasattr(persona, "band_summaries") and persona.band_summaries:
        last_state = persona.band_summaries[-1]

    if last_state:
        indices = getattr(last_state, "indices", None)
        needs = getattr(last_state, "needs", None)
        strategies = getattr(last_state, "strategies", None)
        if indices:
            rmt = getattr(indices, "recursive_madness_threshold", 50) or 50
            iai = getattr(indices, "iai", 50) or 50
            perm = getattr(indices, "permeability_index", 50) or 50
            base += cfg.weight_rmt * (rmt / 100.0)
            base += cfg.weight_iai * (iai / 100.0)
            base += cfg.weight_permeability * (1.0 - perm / 100.0)
        if needs:
            cohere = getattr(needs, "coherence_meaning", 50) or 50
            safety = getattr(needs, "safety", 50) or 50
            base += cfg.weight_coherence_need * (1.0 - cohere / 100.0)
            base += cfg.weight_safety_need * (1.0 - safety / 100.0)
        if strategies:
            perf = getattr(strategies, "perfectionism_control", 0) or 0
            piety = getattr(strategies, "piety_ideology", 0) or 0
            rigidity = (perf + piety) / 200.0
            base += cfg.weight_rigidity * rigidity

    # Normalize base to ~[0, 1] (sum of weights ~1.0)
    base = max(0.0, min(1.0, base))

    if life_state:
        today = getattr(life_state, "today", None)
        attention = getattr(life_state, "attention", None)
        if today:
            mood = (getattr(today, "mood_baseline", "neutral") or "neutral").lower()
            stressor = (getattr(today, "current_stressor", "none") or "none").lower()
            physical = (getattr(today, "physical_state", "fine") or "fine").lower()
            if physical == "tired" or (getattr(today, "sleep_hours", 7) or 7) < 5.5:
                base += cfg.tired_bonus
            if stressor != "none" or mood in ("low", "anxious", "slightly_irritable"):
                base += cfg.stressed_bonus
        if attention:
            att = getattr(attention, "attention_available", 50) or 50
            if att > 70:
                base += cfg.attention_penalty

    base = max(0.0, min(1.0, base))
    # Variance: additive normal noise (good deal of variance)
    try:
        noise = rng.gauss(0, cfg.variance_sigma)
    except AttributeError:
        noise = random.gauss(0, cfg.variance_sigma)
    strength = base + noise
    return max(cfg.strength_floor, min(cfg.strength_ceiling, strength))


def apply_refraction(
    selected_hooks: List[str],
    persona: Any,
    rng: Any = None,
    life_state: Optional[LifeSimulationState] = None,
    refraction_strength: Optional[float] = None,
    config: Optional[RefractionConfig] = None,
) -> List[str]:
    """
    Refract selected hooks into "response angles" from the persona's ego-world.
    Interference level is determined by persona profile and life_state (and optional
    refraction_strength override). Never perfect; variance is applied in
    compute_refraction_strength so the same persona gets a distribution of refraction.
    """
    if not selected_hooks:
        return []
    rng = rng or random
    if refraction_strength is None:
        refraction_strength = compute_refraction_strength(persona, life_state, rng=rng, config=config)
    rand = _get_rand(rng)

    # Probability of at least one neighbor shift: increases with strength (e.g. 0.2 at low → 0.7 at high)
    # Map strength [0.08, 0.92] to shift_prob [0.15, 0.75] so there's always meaningful variance
    shift_prob = 0.15 + (refraction_strength - 0.08) * (0.75 - 0.15) / (0.92 - 0.08) if (0.92 - 0.08) > 0 else 0.4
    shift_prob = max(0.12, min(0.78, shift_prob))

    if rand > shift_prob:
        return list(selected_hooks)[:4]

    angles = list(selected_hooks)[:4]
    top = angles[0] if angles else "other"
    neighbors = HOOK_NEIGHBORS.get(top, [])
    if not neighbors:
        return angles
    already = set(angles)
    candidate = next((n for n in neighbors if n in already), neighbors[0])
    rand2 = _get_rand(rng)
    # Stronger refraction: sometimes substitute and also add a second neighbor (two shifts)
    if refraction_strength > 0.55 and rand2 < 0.4:
        second = next((n for n in neighbors if n != candidate and n not in angles), None)
        if second:
            angles = [candidate, second] + [h for h in angles if h not in (candidate, second)][:2]
        else:
            angles = [candidate] + [h for h in angles if h != candidate][:3]
    elif rand2 < 0.85:
        angles = [candidate] + [h for h in angles if h != candidate][:3]
    else:
        angles = angles[:3] + [candidate]
    return list(dict.fromkeys(angles))[:4]


def select_salient_hooks(
    hooks: List[Union[str, Dict[str, Any]]],
    persona: Any,
    life_state: LifeSimulationState,
    field: Optional[EnergeticField] = None,
) -> List[str]:
    """
    Standpoint-driven salience, sensitive to energetic field.
    Uses: last state indices (DRTS, IAI, RMT), needs (belonging, recognition, safety),
    identity (religion, class), palimpsest (moral_loops, identity_scripts, thought_rails),
    and wound_vector (from rupture_voice_notes on palimpsest) for persona-specific sensitization.

    Wound routing: each wound dimension sensitizes specific hook tags so that a persona with
    abandonment=78 will find "religion" or "authority" personally loaded even when generic
    scoring would drop them. Rupture assumptions are also scanned for semantic overlap with
    incoming hooks, ensuring topic-wound connections bypass the generic threshold.
    """
    if not hooks:
        return []
    # Normalize to list of (tag, strength)
    hook_list: List[Tuple[str, float]] = []
    for h in hooks:
        if isinstance(h, dict):
            tag = h.get("tag", "other")
            strength = float(h.get("strength", 0.7))
        else:
            tag = str(h)
            strength = 0.7
        hook_list.append((tag, strength))

    last_state = None
    if hasattr(persona, "yearly_states") and persona.yearly_states:
        last_state = persona.yearly_states[-1]
    elif hasattr(persona, "band_summaries") and persona.band_summaries:
        last_state = persona.band_summaries[-1]
    identity = getattr(persona, "identity", None)
    palimpsest = getattr(persona, "palimpsest", None)

    drts = 50.0
    iai = 50.0
    rmt = 50.0
    needs_belonging = 50.0
    needs_recognition = 50.0
    needs_safety = 50.0
    needs_coherence = 50.0
    if last_state:
        if hasattr(last_state, "indices") and last_state.indices:
            drts = getattr(last_state.indices, "drts", 50) or 50
            iai = getattr(last_state.indices, "iai", 50) or 50
            rmt = getattr(last_state.indices, "recursive_madness_threshold", 50) or 50
        if hasattr(last_state, "needs") and last_state.needs:
            needs_belonging = getattr(last_state.needs, "belonging_group", 50) or 50
            needs_recognition = getattr(last_state.needs, "recognition_status", 50) or 50
            needs_safety = getattr(last_state.needs, "safety", 50) or 50
            needs_coherence = getattr(last_state.needs, "coherence_meaning", 50) or 50

    religion_label = (getattr(identity, "current_religion", None) or getattr(identity, "childhood_religion", None) or "") if identity else ""
    class_ = (getattr(identity, "current_class", None) or "").lower() if identity else ""
    minority = (getattr(identity, "minority_status", None) or "dominant").lower() if identity else "dominant"
    identity_scripts = []
    moral_loops = []
    thought_rail_keys = []
    rupture_notes: List[str] = []
    if palimpsest:
        identity_scripts = [l.value for l in getattr(palimpsest, "identity_scripts_history", [])[-10:]]
        moral_loops = [l.value for l in getattr(palimpsest, "moral_loops_history", [])[-5:]]
        thought_rail_keys = list(getattr(palimpsest, "thought_rail_history", [])[-1].keys()) if getattr(palimpsest, "thought_rail_history", []) else []
        rupture_notes = list(getattr(palimpsest, "rupture_voice_notes", []) or [])

    # ---- Wound-vector dimensions from persona_sheet backbone (if available via palimpsest) ----
    # These are stored in the persona_sheet backbone key but we can approximate from rupture_notes
    # and the palimpsest moral_loops (wound-sensitive loops end in "_sensitive").
    wv_abandonment = 50.0
    wv_shame = 50.0
    wv_fear = 50.0
    wv_recognition = 50.0
    wv_control = 50.0
    wv_anger = 50.0
    wv_loss = 50.0
    for loop in moral_loops:
        lv = (loop or "").lower()
        if "abandonment_sensitive" in lv:   wv_abandonment = max(wv_abandonment, 72.0)
        if "shame_sensitive" in lv:         wv_shame = max(wv_shame, 72.0)
        if "fear_sensitive" in lv:          wv_fear = max(wv_fear, 72.0)
        if "recognition_sensitive" in lv:   wv_recognition = max(wv_recognition, 72.0)
        if "control_sensitive" in lv:       wv_control = max(wv_control, 72.0)
        if "anger_sensitive" in lv:         wv_anger = max(wv_anger, 72.0)
        if "loss_sensitive" in lv:          wv_loss = max(wv_loss, 72.0)

    # ---- Rupture-to-hook semantic mapping ----
    # Scan rupture assumptions for words that connect to hook taxonomy.
    # This fires when a topic touches an unhealed wound even if the surface hook is generic.
    _RUPTURE_TOPIC_SIGNALS = {
        "religion": ("sacred", "moral", "god", "faith", "holy", "pious", "imam", "church", "mosque", "sin"),
        "authority": ("obey", "leader", "government", "authority", "rule", "power", "institution", "official"),
        "family": ("caregiver", "parent", "mother", "father", "home", "housed", "stable", "family", "guardian"),
        "inequality": ("class", "poor", "rich", "money", "housed", "eviction", "afford"),
        "safety": ("safe", "danger", "war", "bomb", "threat", "violence", "police", "housed"),
        "recognition": ("seen", "respect", "dignity", "status", "worth", "recognize"),
        "trauma": ("gave way", "broke", "shattered", "betrayed", "abandoned", "humiliated"),
        "identity": ("belong", "who we are", "roots", "culture", "people"),
    }
    rupture_boost: Dict[str, float] = {}
    notes_text = " ".join(rupture_notes).lower()
    for hook_tag, signals in _RUPTURE_TOPIC_SIGNALS.items():
        for sig in signals:
            if sig in notes_text:
                rupture_boost[hook_tag] = rupture_boost.get(hook_tag, 0) + 0.18
                break  # one match per tag is enough

    # Base salience by persona
    scores: Dict[str, float] = {}
    for tag, strength in hook_list:
        s = strength * 0.5

        # --- Standard persona-level boosts ---
        if tag == "inequality" and (drts > 45 or class_ in ("working", "underclass", "lower_middle")):
            s += 0.35
        if tag == "authority" and drts > 50:
            s += 0.3
        if tag == "religion" and religion_label:
            s += 0.45
        if tag == "family":
            s += 0.2
        if tag == "work":
            s += 0.2
        if tag == "recognition" and needs_recognition < 60:
            s += 0.3
        if tag == "safety" and needs_safety < 55:
            s += 0.25
        if tag == "trauma" and rmt > 45:
            s += 0.2
        if tag == "identity" and needs_belonging < 65:
            s += 0.2
        if minority == "minoritized" and tag in ("inequality", "recognition", "identity"):
            s += 0.15
        if moral_loops:
            s += 0.08
        if "authority" in str(thought_rail_keys) and tag == "authority":
            s += 0.15
        if "fairness" in str(thought_rail_keys) and tag == "inequality":
            s += 0.15

        # --- Wound-vector sensitization: elevated wounds lower the threshold ---
        if tag in ("family", "trauma") and wv_abandonment >= 65:
            s += 0.20 * ((wv_abandonment - 50) / 50)
        if tag in ("recognition", "identity") and wv_recognition >= 60:
            s += 0.18 * ((wv_recognition - 50) / 50)
        if tag in ("authority", "politics") and wv_fear >= 60:
            s += 0.18 * ((wv_fear - 50) / 50)
        if tag == "trauma" and wv_shame >= 60:
            s += 0.15 * ((wv_shame - 50) / 50)
        if tag in ("inequality", "work") and wv_anger >= 60:
            s += 0.15 * ((wv_anger - 50) / 50)
        if tag in ("safety", "family") and wv_loss >= 60:
            s += 0.15 * ((wv_loss - 50) / 50)

        # --- Rupture-topic boost: specific unhealed wounds sensitize specific topics ---
        if tag in rupture_boost:
            s += rupture_boost[tag]

        scores[tag] = min(1.0, s)

    # Energetic field modulation
    if field:
        tension = field.tension
        boredom = field.boredom
        intimacy = field.intimacy
        curiosity = field.curiosity
        if tension > 0.5:
            for t in ("safety", "trauma", "authority"):
                if t in scores:
                    scores[t] = min(1.0, scores[t] + 0.2 * tension)
        if boredom > 0.5:
            threshold_raise = 0.15 * boredom
            for k in list(scores.keys()):
                if scores[k] < 0.6:
                    scores[k] -= threshold_raise
        if intimacy > 0.4:
            for t in ("family", "identity", "recognition"):
                if t in scores:
                    scores[t] = min(1.0, scores[t] + 0.15 * intimacy)
        if curiosity > 0.5:
            for k in scores:
                scores[k] = min(1.0, scores[k] + 0.08)

    # Lower threshold slightly so wound-loaded topics pass through even at moderate hook strength
    threshold = 0.38
    selected = [(tag, scores.get(tag, 0)) for tag, _ in hook_list if scores.get(tag, 0) >= threshold]
    return [tag for tag, _ in sorted(selected, key=lambda x: -x[1])] if selected else [hook_list[0][0]] if hook_list else []


def appraise(
    msg: str,
    selected_hooks: List[str],
    persona: Any,
    life_state: LifeSimulationState,
    field: Optional[EnergeticField] = None,
) -> Dict[str, Any]:
    """
    Appraisal: tone, effort_cap, boundary_triggered. Uses life_state (today, interaction)
    and optional energetic field (tension, boredom, demand_level) to set effort and tone.
    """
    today = life_state.today
    interaction = life_state.interaction
    mood = getattr(today, "mood_baseline", "neutral")
    stressor = getattr(today, "current_stressor", "none")
    reason = getattr(interaction, "reason", "other")

    tone = "neutral"
    if mood in ("low", "slightly_irritable", "anxious"):
        tone = "guarded"
    if reason in ("boredom_scrolling", "procrastinating_work"):
        tone = "minimal"
    if reason in ("activism_curiosity", "lonely_evening"):
        tone = "engaged"

    effort_cap = "medium"
    if tone == "minimal":
        effort_cap = "low"
    elif tone == "engaged":
        effort_cap = "high"

    if field:
        if field.tension > 0.6:
            tone = "guarded" if tone == "neutral" else tone
            effort_cap = "medium" if effort_cap == "low" else effort_cap
        if field.boredom > 0.6:
            tone = "minimal" if tone == "neutral" else tone
            effort_cap = "low"
        if field.demand_level > 0.6 and field.last_persona_effort == "minimal":
            effort_cap = "medium"  # nudge toward responding more
        if field.curiosity > 0.5 and tone == "neutral":
            effort_cap = "high"

    # Detect hostility/dismissiveness in the message itself.
    # These patterns are often polite-sounding but condescending; they don't
    # necessarily trigger intensity_signal (no shouting), so we check separately.
    boundary_triggered = False
    _msg_lower = msg.lower() if msg else ""
    _DISMISSIVE_PATTERNS = (
        "you wouldn't understand", "you don't understand", "people like you",
        "that's naive", "you're naive", "that's simplistic", "you're wrong",
        "you clearly don't", "obviously you", "you just don't get it",
        "of course you would", "typical", "how could you", "you should know",
        "that's stupid", "that's dumb", "you're stupid", "idiot", "moron",
        "shut up", "whatever", "you're so", "i don't care what you think",
        "no one cares", "you're just", "you don't know anything",
    )
    if any(p in _msg_lower for p in _DISMISSIVE_PATTERNS):
        boundary_triggered = True
        tone = "guarded"
        effort_cap = "low"
    # High accumulated tension in the field also raises defensiveness
    elif field and field.tension > 0.75:
        boundary_triggered = True
        tone = "guarded"
        effort_cap = "low" if effort_cap == "medium" else effort_cap

    return {
        "tone": tone,
        "boundary_triggered": boundary_triggered,
        "selected_hooks": selected_hooks,
        "effort_cap": effort_cap,
    }


# Keywords that suggest political/structural topic → higher-effort reply (6–8 sentences, engage)
_POLITICAL_STRUCTURAL_KEYWORDS = (
    "empire", "imperialism", "colonial", "colonialism", "government", "capitalism",
    "socialism", "state", "power", "oppression", "resistance", "revolution",
    "class", "race", "inequality", "colonial", "occupation", "war", "military",
)

def choose_response_move(
    appraisal: Dict[str, Any],
    attention_budget: Any,
    field: Optional[EnergeticField] = None,
    user_message: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Choose response move and length/depth from attention budget and appraisal.
    Field: high demand + high tension can push toward engage_selective (not deflect).
    If user_message suggests political/structural topic, bias toward 6–8 sentences and engage_selective.
    """
    if attention_to_reply_limits and attention_budget:
        limits = attention_to_reply_limits(attention_budget)
    else:
        limits = {"max_sentences": 6, "depth_hint": "moderate", "attention_available": 50}
    effort = appraisal.get("effort_cap", "medium")
    political_structural = False
    if user_message:
        lower = user_message.lower()
        political_structural = any(k in lower for k in _POLITICAL_STRUCTURAL_KEYWORDS)
    if political_structural:
        limits["max_sentences"] = min(8, max(6, limits.get("max_sentences", 6)))
        effort = "high"
    if effort == "low" and not political_structural:
        limits = {"max_sentences": max(2, limits.get("max_sentences", 6) - 3), "depth_hint": "minimal"}
    elif effort == "high":
        limits = {"max_sentences": min(12, limits.get("max_sentences", 6) + 2), "depth_hint": limits.get("depth_hint", "moderate")}

    move = "engage_selective"
    if appraisal.get("boundary_triggered"):
        move = "deflect"
    elif effort == "low":
        move = "brief_or_deflect"
    if political_structural and move == "brief_or_deflect":
        move = "engage_selective"
    if field and field.demand_level > 0.6 and field.tension < 0.5:
        if move == "brief_or_deflect":
            move = "engage_selective"
            limits["max_sentences"] = min(6, limits.get("max_sentences", 2) + 2)

    return {
        "move_type": move,
        "max_sentences": limits.get("max_sentences", 6),
        "depth_hint": limits.get("depth_hint", "moderate"),
        "attention_available": limits.get("attention_available", 50),
    }


def build_reply_prompt(
    persona_context: str,
    life_state: LifeSimulationState,
    user_message: str,
    move: Dict[str, Any],
    forbidden_hint: bool = True,
    field: Optional[EnergeticField] = None,
    response_angles: Optional[List[str]] = None,
    voice_schema: Optional[str] = None,
    primary_language: Optional[str] = None,
    integrity_status: str = "clean",
    chat_relation_mode: str = "generated_persona",
    voice_schema_status: str = "clean",
    hook_analysis_integrity: Optional[Dict[str, Any]] = None,
    memory_provenance: Optional[str] = None,
    history_cache_key: Optional[str] = None,
) -> str:
    """
    Build the prompt for the LLM that generates the persona's reply.
    voice_schema: character-derived reply rules (from derive_reply_voice_schema).
    primary_language: if set and not English, ask for NATIVE + TRANSLATION format.
    """
    parts = [persona_context]
    parts.append("\n\n---\n\nCONVERSATION (reply as the persona):")
    schema = (voice_schema or REPLY_VOICE_SCHEMA_FALLBACK).strip()
    parts.append("\n\n" + schema)
    parts.append("\n\n" + GROUNDING_RULE)
    parts.append("\n\n" + REPLY_LANGUAGE_RULE)
    parts.append("\n\n" + FORBIDDEN_LLM_PATTERNS)
    parts.append("\n\n" + _specificity_policy_for_integrity(integrity_status))
    parts.append(
        f"\n\nCHAT CONTRACT: relation_mode={chat_relation_mode}; integrity={integrity_status}; "
        f"voice_schema_status={voice_schema_status}; memory_provenance={memory_provenance or 'unknown'}; "
        f"history_cache_key={history_cache_key or 'unknown'}."
    )
    if hook_analysis_integrity:
        parts.append(
            "\n\nCHAT ANALYSIS INTEGRITY: "
            f"detected_language={hook_analysis_integrity.get('detected_language') or 'unknown'}; "
            f"hook_confidence={hook_analysis_integrity.get('hook_confidence')}; "
            f"refraction_strength={hook_analysis_integrity.get('refraction_strength')}; "
            f"random_seed={hook_analysis_integrity.get('random_seed')}"
        )
    if field:
        cues = []
        if field.tension > 0.5:
            cues.append("conversation is a bit tense or charged")
        if field.intimacy > 0.4:
            cues.append("they're opening up personally")
        if field.curiosity > 0.5:
            cues.append("they seem engaged and curious")
        if field.boredom > 0.5:
            cues.append("exchange has felt a bit flat or repetitive")
        if cues:
            parts.append(f"\n\nContext: {'; '.join(cues)}.")
    parts.append("\n\n" + PERCEPTION_INSTRUCTION)
    parts.append(f"\n\nUser said (process this as this person would—you may mishear, latch onto one part, or run with a misread): {user_message!r}")
    if response_angles:
        angles_str = ", ".join(response_angles)
        hook_confidence = float((hook_analysis_integrity or {}).get("hook_confidence") or 0.0)
        uptake_label = "tentative uptake" if hook_confidence < 0.5 else "actual uptake"
        parts.append(
            f"\nWhat reached you (engine: salience + refraction—this is your {uptake_label}): {angles_str}. "
            "Reply only from that; you may have missed or distorted the rest. No need to address every part of the message; slant and misread are in character."
        )
    if field and field.active_streams:
        threads = []
        for s in field.active_streams[:3]:
            if s.internal_tag and s.internal_tag != s.external_tag.replace("_", " "):
                threads.append(f"{s.external_tag} (felt as {s.internal_tag})")
            else:
                threads.append(s.external_tag)
        if threads:
            parts.append(f"\nOngoing threads for this person: {', '.join(threads)}. Stay mostly with these; small lateral moves are okay, hard topic jumps are not unless tension spikes.")
    parts.append(
        f"\n\nReply as the persona. Move: {move.get('move_type', 'engage_selective')}. Keep to about {move.get('max_sentences', 6)} sentences or fewer ({move.get('depth_hint', 'moderate')}). "
        "Do not be comprehensive; respond to what lights up for this person. "
        "You ARE this person: use their specific place, history, and life (their city, class, context—what safety/danger/inequality means there). "
        "If they ask about violence, discrimination, or risk, answer from this person's actual context—not generic empathy. "
        "Respond to what actually hooked you, in your own rhythm; the reply can feel slightly off from what they asked, as in real conversation. No smooth mirroring; allow jaggedness. "
        "Apply the VOICE SCHEMA above for this reply."
    )
    parts.append(
        "\n\nFORMAT: First-person speech, with italicized third-person beats. "
        "Beats describe the body and the space — hyper-close, purely objective, like a camera. "
        "Length is unrestricted. Write what the camera sees: what she picks up or puts down, "
        "where she looks, how she sits, what's in the room, what sound or light is there. "
        "CAMERA RULE: if the camera cannot film it, it cannot be in a beat. "
        "This means: no thinking, no feeling, no remembering, no intending, no interpreting. "
        "WRONG — interior state, camera can't film it: "
        "*wondering how to clarify* | *recalling their enthusiasm* | *animated by the thought of them* | "
        "*almost pleading for connection* | *the memories bringing her to life* | *sensing uncertainty* | "
        "*the idea lighting her up* | *letting that linger*. "
        "RIGHT — purely physical, camera sees it: "
        "*She sets her cup down without drinking from it.* | "
        "*She picks up the pen on the table, rolls it between her fingers, puts it down.* | "
        "*She looks toward the window for a moment, then back.* | "
        "*A fan runs somewhere. She doesn't seem to notice.* | "
        "*She's quiet. Her hand stays flat on the table.* "
        "Speech can interrupt itself, trail off, be mid-sentence."
        "\n\nLAST-LINE CHECK: Does any beat describe what someone is thinking, feeling, or remembering? "
        "If yes, rewrite it as pure physical observation or cut it. "
        "Does the speech end with 'we're all just trying to' / 'find our way' / 'that's what keeps me' / "
        "'a little bubble of' / 'that's everything' as a wrap-up? Cut or replace with something specific. "
        "Reply as the persona. Do not be comprehensive. No smooth mirroring."
    )
    lang = (primary_language or "").strip()
    if lang and lang.lower() not in ("english", "en", ""):
        lang_block = (
            f"\n\n--- REQUIRED OUTPUT FORMAT ---\n"
            f"This person's primary language is {lang}. Your response MUST begin with NATIVE: and contain both sections:\n"
            f"NATIVE: [her spoken words only, in {lang} — natural idiom, no action beats needed]\n"
            f"TRANSLATION: [Write this fresh from communicative intent — do NOT translate the NATIVE block word for word. "
            f"Ask: what is she actually trying to say? Then write that in the user's language as she would say it as an {lang} L1 speaker. "
            f"Grammar must be fully comprehensible to any reader. Her character shows in directness and rhythm, not broken syntax. "
            f"Topic-comment rendered naturally: 'Your people — do you love them?' not 'Your own people, those are yours.' "
            f"{lang} discourse filler particles (e.g. Amharic አሁን, Arabic ya'ni) = a pause or omitted entirely — NOT the word 'Now'. "
            f"Untranslatable {lang} words appear romanized and bare where they arise naturally. No brackets, no glosses. Match the user's language.]\n"
            f"Begin your response with NATIVE: — nothing before it.\n"
            f"--- END FORMAT ---"
        )
        parts.insert(1, lang_block)  # insert right after persona_context
    return "".join(parts)


# Words that indicate a beat is narrating psychology rather than showing a body.
# Any beat containing one of these is removed entirely.
_BEAT_PSYCH_WORDS = frozenset({
    "considering", "recalling", "remembering", "wondering", "animated",
    "thinking", "feeling", "hoping", "fearing", "wanting", "needing",
    "reflecting", "pondering", "sensing", "noticing", "catching", "letting",
    "pleading", "enthusiasm", "warmth", "connection", "uncertainty", "curiosity",
    "excitement", "anxiety", "pride", "shame", "longing", "yearning",
    "weight", "burden", "memories", "memory", "thought", "thoughts",
    "resonating", "resonates", "linger", "lingering", "shifting", "animating",
    "piqued", "creeping", "threading",
})


def clean_reply_beats(text: str) -> str:
    """
    Post-process LLM reply to strip beats that narrate interior states.

    The format allows hyper-close objective third-person beats of any length,
    like a camera: what the body does, where the eyes go, what's in the room.
    The only thing disallowed is interior-state narration (thinking, feeling,
    remembering, intending).

    Rule: if a beat contains any word from _BEAT_PSYCH_WORDS, remove it entirely.
    Clean descriptive beats (arbitrary length, commas fine) pass through unchanged.
    """
    import re as _re

    def _fix_beat(m: "_re.Match") -> str:
        beat = m.group(1).strip()
        if not beat:
            return ""
        # Psychology vocabulary check — interior state = remove beat entirely
        beat_words = {w.lower().rstrip(".,;:*") for w in beat.split()}
        if beat_words & _BEAT_PSYCH_WORDS:
            return ""
        return f"*{beat}*"

    cleaned = _re.sub(r"\*([^*\n]+)\*", _fix_beat, text)
    # Collapse any double-spaces left by removed beats
    cleaned = _re.sub(r"  +", " ", cleaned)
    cleaned = _re.sub(r"^ ", "", cleaned, flags=_re.MULTILINE)
    return cleaned.strip()


def strip_inline_glosses(text: str) -> str:
    """
    Remove bracketed English glosses that the LLM adds after native-language words,
    e.g. 'ya'ni [I mean]' → 'ya'ni', 'مش نفس الحاجة. [Not the same thing.]' → 'مش نفس الحاجة.'

    Targets [bracketed content] that appears:
    - immediately after a non-ASCII character (native script), OR
    - immediately after a romanized native word followed by '...' or punctuation

    Does NOT remove brackets that are part of beat markers (*...*) or legitimate
    English-only bracketed content not adjacent to non-ASCII text.
    """
    import re as _re
    # Strip [gloss] that directly follows non-Latin-script characters (Arabic, Cyrillic, etc.)
    text = _re.sub(r'([^\x00-\x7F][^[]{0,80}?)\s*\[[^\]]{1,80}\]', r'\1', text)
    # Strip [gloss] after a word ending in ... or punctuation preceded by any non-ASCII
    text = _re.sub(r'(\.\.\.|[.،؟!])\s*\[[^\]]{1,80}\]', r'\1', text)
    # Collapse double spaces
    text = _re.sub(r'  +', ' ', text)
    return text.strip()


def parse_reply_native_and_translation(raw: str) -> Tuple[Optional[str], str]:
    """
    Parse a bilingual reply and return (native_text, english_text).

    Supports three formats:
    0. DRAFT: format — DRAFT: [native one-liner] on first line, English response after.
       native_text  = the DRAFT line (native language)
       english_text = everything after the first line (English with L1 interference)
    1. Block format: NATIVE: [...] TRANSLATION: [...] — explicit markers (legacy)
    2. Embedded format (legacy): narration in English, speech in native
       with bracketed gloss after each utterance:
       *He nods.* "Hoy fue difícil." [Today was difficult.] *He looks away.*

    Returns (None, raw) when no bilingual markers detected (monolingual reply).
    """
    import re as _re
    raw = (raw or "").strip()
    if not raw:
        return None, ""

    # --- Format 0: DRAFT: [native one-liner] --- (current format)
    if raw.startswith("DRAFT:"):
        first_newline = raw.find("\n")
        if first_newline > 0:
            draft_line = raw[len("DRAFT:"):first_newline].strip()
            english_text = raw[first_newline:].strip()
            if english_text:
                return draft_line or None, english_text

    # --- Format 1: NATIVE: / TRANSLATION: blocks ---
    native_marker = "NATIVE:"
    trans_marker = "TRANSLATION:"
    native_idx = raw.find(native_marker)
    trans_idx = raw.find(trans_marker)
    if native_idx >= 0 and trans_idx > native_idx:
        after_native = native_idx + len(native_marker)
        native_text = raw[after_native:trans_idx].strip()
        after_trans = trans_idx + len(trans_marker)
        translation_text = raw[after_trans:].strip()
        if translation_text:
            return (native_text or None), translation_text
        return native_text or None, native_text or raw

    # --- Format 2: embedded "native speech" [English gloss] ---
    # LLM may use straight quotes (") or curly quotes (\u201c / \u201d).
    # Match any open-quote ... close-quote followed by [bracketed gloss].
    # open_q: " or \u201c     close_q: " or \u201d
    pattern = _re.compile(
        r'["\u201c]([^"\u201d]+?)["\u201d]\s*\[([^\]]+?)\]'
    )
    matches = list(pattern.finditer(raw))
    if not matches:
        return None, raw

    # Determine which quote style the LLM used for consistent rebuilding
    first_char = raw[matches[0].start()]
    open_q  = first_char
    close_q = "\u201d" if open_q == "\u201c" else '"'

    # native_text: keep quoted speech, drop bracketed gloss
    native_text = pattern.sub(
        lambda m: f'{open_q}{m.group(1)}{close_q}', raw
    ).strip()
    # english_text: replace quoted speech + brackets with just the gloss (no quotes)
    english_text = pattern.sub(lambda m: m.group(2), raw).strip()

    return native_text, english_text


# Max prior user+assistant pairs to send to the LLM so context stays bounded.
MAX_CONVERSATION_HISTORY_MESSAGES = 20


def _build_system_and_user_turn(
    persona_context: str,
    user_message: str,
    move: Dict[str, Any],
    field: Optional[EnergeticField] = None,
    response_angles: Optional[List[str]] = None,
    voice_schema: Optional[str] = None,
    primary_language: Optional[str] = None,
    integrity_status: str = "clean",
    chat_relation_mode: str = "generated_persona",
    voice_schema_status: str = "clean",
    hook_analysis_integrity: Optional[Dict[str, Any]] = None,
    memory_provenance: Optional[str] = None,
    history_cache_key: Optional[str] = None,
) -> Tuple[str, str]:
    """
    Build system_content (persona + schema + static instructions) and user_turn_content
    (cues + "User said: ..." + angles + threads + move) for multi-turn API calls.
    """
    schema = (voice_schema or REPLY_VOICE_SCHEMA_FALLBACK).strip()
    system_parts = [
        persona_context,
        "\n\n---\n\nCONVERSATION (reply as the persona):",
        "\n\n",
        schema,
        "\n\n",
        GROUNDING_RULE,
        "\n\n",
        REPLY_LANGUAGE_RULE,
        "\n\n",
        FORBIDDEN_LLM_PATTERNS,
        "\n\n",
        _specificity_policy_for_integrity(integrity_status),
        "\n\nCHAT CONTRACT: relation_mode=",
        chat_relation_mode,
        "; integrity=",
        integrity_status,
        "; voice_schema_status=",
        voice_schema_status,
        "; memory_provenance=",
        memory_provenance or "unknown",
        "; history_cache_key=",
        history_cache_key or "unknown",
        ".",
        "\n\n",
        PERCEPTION_INSTRUCTION,
        "\n\n",
        FRICTION_RULE,
        "\n\n",
        "CONCRETENESS: Give one specific moment, one named detail, or one real tension—not a paragraph of how wonderful the place/people are. "
        "No tourism-board summaries; no 'family is everything' / 'warmth of the people' pabulum.",
        "\n\nFORMAT: First-person speech, with italicized third-person beats. "
        "Beats describe the body and the space — hyper-close, purely objective, like a camera. "
        "Length is unrestricted. Write what the camera sees: what she picks up or puts down, "
        "where she looks, how she sits, what's in the room, what sound or light is there. "
        "CAMERA RULE: if the camera cannot film it, it cannot be in a beat. "
        "This means: no thinking, no feeling, no remembering, no intending, no interpreting. "
        "WRONG — interior state, camera can't film it: "
        "*wondering how to clarify* | *recalling their enthusiasm* | *animated by the thought of them* | "
        "*almost pleading for connection* | *the memories bringing her to life* | *sensing uncertainty* | "
        "*the idea lighting her up* | *letting that linger*. "
        "RIGHT — purely physical, camera sees it: "
        "*She sets her cup down without drinking from it.* | "
        "*She picks up the pen on the table, rolls it between her fingers, puts it down.* | "
        "*She looks toward the window for a moment, then back.* | "
        "*A fan runs somewhere. She doesn't seem to notice.* | "
        "*She's quiet. Her hand stays flat on the table.* "
        "Speech can interrupt itself, trail off, be mid-sentence.",
        "\n\nLAST-LINE CHECK: Does any beat describe what someone is thinking, feeling, or remembering? "
        "If yes, rewrite it as pure physical observation or cut it. "
        "Does the speech end with 'we're all just trying to' / 'find our way' / 'that's what keeps me' / "
        "'a little bubble of' / 'that's everything' as a wrap-up? Cut or replace with something specific. "
        "Reply as the persona. Apply the VOICE SCHEMA. Do not be comprehensive. No smooth mirroring; allow jaggedness.",
    ]
    if hook_analysis_integrity:
        system_parts.extend(
            [
                "\n\nCHAT ANALYSIS INTEGRITY: ",
                f"detected_language={hook_analysis_integrity.get('detected_language') or 'unknown'}; ",
                f"hook_confidence={hook_analysis_integrity.get('hook_confidence')}; ",
                f"refraction_strength={hook_analysis_integrity.get('refraction_strength')}; ",
                f"random_seed={hook_analysis_integrity.get('random_seed')}",
            ]
        )
    lang = (primary_language or "").strip()
    if lang and lang.lower() not in ("english", "en", ""):
        lang_block = (
            f"\n--- REQUIRED OUTPUT FORMAT ---\n"
            f"This person's primary language is {lang}. Your response MUST begin with NATIVE: and contain both sections:\n"
            f"NATIVE: [her spoken words only, in {lang} — natural idiom, no action beats needed]\n"
            f"TRANSLATION: [Write this fresh from communicative intent — do NOT translate the NATIVE block word for word. "
            f"Ask: what is she actually trying to say? Then write that in the user's language as she would say it as an {lang} L1 speaker. "
            f"Grammar must be fully comprehensible to any reader. Her character shows in directness and rhythm, not broken syntax. "
            f"Topic-comment rendered naturally: 'Your people — do you love them?' not 'Your own people, those are yours.' "
            f"{lang} discourse filler particles (e.g. Amharic አሁን, Arabic ya'ni) = a pause or omitted entirely — NOT the word 'Now'. "
            f"Untranslatable {lang} words appear romanized and bare where they arise naturally. No brackets, no glosses. Match the user's language.]\n"
            f"Begin your response with NATIVE: — nothing before it.\n"
            f"--- END FORMAT ---\n\n"
        )
        system_parts.insert(0, lang_block)  # put at very top of system prompt
    system_content = "".join(system_parts)

    user_parts = []
    if field:
        cues = []
        if field.tension > 0.5:
            cues.append("conversation is a bit tense or charged")
        if field.intimacy > 0.4:
            cues.append("they're opening up personally")
        if field.curiosity > 0.5:
            cues.append("they seem engaged and curious")
        if field.boredom > 0.5:
            cues.append("exchange has felt a bit flat or repetitive")
        if cues:
            user_parts.append(f"Context: {'; '.join(cues)}.\n\n")
    user_parts.append(
        f"They said (process as this person would—you may mishear, latch onto one part, or run with a misread): {user_message!r}"
    )
    if response_angles:
        angles_str = ", ".join(response_angles)
        hook_confidence = float((hook_analysis_integrity or {}).get("hook_confidence") or 0.0)
        uptake_label = "tentative uptake" if hook_confidence < 0.5 else "actual uptake"
        user_parts.append(
            f"\nWhat reached you (engine: salience + refraction—your {uptake_label}): {angles_str}. "
            "Reply only from that; you may have missed or distorted the rest."
        )
    if field and field.active_streams:
        threads = []
        for s in field.active_streams[:3]:
            if s.internal_tag and s.internal_tag != s.external_tag.replace("_", " "):
                threads.append(f"{s.external_tag} (felt as {s.internal_tag})")
            else:
                threads.append(s.external_tag)
        if threads:
            user_parts.append(f"\nOngoing threads: {', '.join(threads)}. Stay mostly with these.")
    user_parts.append(
        f"\n\nReply as the persona. Move: {move.get('move_type', 'engage_selective')}. "
        f"Keep to about {move.get('max_sentences', 6)} sentences or fewer ({move.get('depth_hint', 'moderate')}). "
        "Apply the VOICE SCHEMA above for this reply."
    )
    user_turn_content = "".join(user_parts)
    return system_content, user_turn_content


def prepare_conversation_turn(
    persona_history: Any,
    user_message: str,
    date: str = "2025-01-15",
    scenario_reason: Optional[str] = None,
    rng: Any = None,
    energetic_field: Optional[EnergeticField] = None,
    conversation_history: Optional[List[Dict[str, Any]]] = None,
    refraction_config: Optional[RefractionConfig] = None,
    integrity_report: Optional[Dict[str, Any]] = None,
    chat_relation_mode: str = "generated_persona",
) -> Dict[str, Any]:
    """
    Full pipeline: build life state → persona context → analyze (with field) → hooks → salience (with field) → appraisal → move → reply prompt.
    Accepts optional energetic_field (pass from previous turn) and conversation_history (for future use).
    Updates field with this user turn and returns it as energetic_field so caller can:
      - pass it to the next prepare_conversation_turn, and
      - after getting persona reply, call update_energetic_field(field, persona_reply, "persona", persona_effort=...) to keep field in sync.
    Returns: prompt, life_state, move, limits, selected_hooks, analysis, appraisal, energetic_field.
    """
    if not build_life_simulation_state or not build_conversation_persona_context:
        raise RuntimeError("conversation_engine requires spec.build_conversation_persona_context and life_simulation_schema.build_life_simulation_state")
    field = energetic_field
    integrity_status = _integrity_status_label(integrity_report)
    result = build_conversation_persona_context(
        persona_history,
        include_life_layer=True,
        date=date,
        scenario_reason=scenario_reason,
        rng=rng,
        chat_relation_mode=chat_relation_mode,
    )
    persona_context = result[0] if isinstance(result, tuple) else result
    life_state = result[1] if isinstance(result, tuple) else build_life_simulation_state(persona_history, date, scenario_reason=scenario_reason, rng=rng)
    surface_psyche_context = _surface_psyche_context_from_history(persona_history)
    if surface_psyche_context:
        persona_context = f"{persona_context}\n\n{surface_psyche_context}"

    analysis = analyze_message(user_message, field=field)
    hooks = extract_hooks(user_message, field=field)
    selected = select_salient_hooks(hooks, persona_history, life_state, field=field)
    refraction_strength = compute_refraction_strength(
        persona_history, life_state, rng=rng, config=refraction_config,
    )
    response_angles = apply_refraction(
        selected, persona_history, rng=rng, life_state=life_state,
        refraction_strength=refraction_strength, config=refraction_config,
    )
    appraisal = appraise(user_message, selected, persona_history, life_state, field=field)
    move = choose_response_move(appraisal, life_state.attention, field=field, user_message=user_message)
    move["max_sentences"] = move.get("max_sentences", 6)
    move["depth_hint"] = move.get("depth_hint", "moderate")

    field = update_energetic_field(field, user_message, "user", analysis=analysis, hooks=hooks)
    update_topic_streams(field, response_angles or selected, persona_history)
    hook_confidence = max([float(h.get("strength", 0.0) or 0.0) for h in hooks], default=0.0)
    hook_analysis_integrity = {
        "detected_language": "non_english" if sum(1 for ch in (user_message or "") if ord(ch) > 127) > 0 else "english",
        "hook_confidence": hook_confidence,
        "refraction_strength": refraction_strength,
        "random_seed": getattr(rng, "seed_value", None),
    }
    voice_result = derive_reply_voice_schema_result(persona_history, integrity_status=integrity_status)
    voice_schema = str(voice_result.get("text") or REPLY_VOICE_SCHEMA_FALLBACK)
    voice_schema_status = str(voice_result.get("status") or "clean")
    voice_schema_defects = list(voice_result.get("defects") or [])
    memory_provenance = str(voice_result.get("memory_provenance") or "mixed")
    history_cache_key = str(voice_result.get("history_cache_key") or "")
    identity = getattr(persona_history, "identity", None)
    primary_language = (getattr(identity, "primary_language", None) or "").strip() or None
    if not primary_language:
        # persona_sheet stores languages as a list; fall back to first non-English entry
        _langs = getattr(identity, "languages", None) or []
        if isinstance(_langs, str):
            _langs = [_langs]
        for _l in _langs:
            _l = str(_l or "").strip()
            if _l and _l.lower() not in ("english", "en", "—", "unknown", ""):
                primary_language = _l
                break
    prompt = build_reply_prompt(
        persona_context, life_state, user_message, move,
        forbidden_hint=True, field=field, response_angles=response_angles or selected,
        voice_schema=voice_schema, primary_language=primary_language,
        integrity_status=integrity_status, chat_relation_mode=chat_relation_mode,
        voice_schema_status=voice_schema_status, hook_analysis_integrity=hook_analysis_integrity,
        memory_provenance=memory_provenance, history_cache_key=history_cache_key,
    )
    system_content, user_turn_content = _build_system_and_user_turn(
        persona_context, user_message, move,
        field=field, response_angles=response_angles or selected, voice_schema=voice_schema,
        primary_language=primary_language,
        integrity_status=integrity_status, chat_relation_mode=chat_relation_mode,
        voice_schema_status=voice_schema_status, hook_analysis_integrity=hook_analysis_integrity,
        memory_provenance=memory_provenance, history_cache_key=history_cache_key,
    )

    return {
        "prompt": prompt,
        "system_content": system_content,
        "user_turn_content": user_turn_content,
        "life_state": life_state,
        "move": move,
        "limits": {"max_sentences": move["max_sentences"], "depth_hint": move["depth_hint"]},
        "selected_hooks": selected,
        "response_angles": response_angles,
        "refraction_strength": refraction_strength,
        "analysis": analysis,
        "appraisal": appraisal,
        "energetic_field": field,
        "integrity_status": integrity_status,
        "voice_schema_status": voice_schema_status,
        "voice_schema_defects": voice_schema_defects,
        "chat_relation_mode": chat_relation_mode,
        "hook_analysis_integrity": hook_analysis_integrity,
        "memory_provenance": memory_provenance,
        "history_cache_key": history_cache_key,
    }
