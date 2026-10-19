# v3/engine/prompts.py
# Prompt builders for Pass 1 (candidates) and Pass 2 (render). No LLM calls; only build prompt text.
# Reference: specLLM.txt, OVERVIEW_INTEGRATED.md §13.

from __future__ import annotations

import json
from typing import Any


PASS1_SYSTEM = """You are a candidate generator for a year-step life simulation. You receive a compressed state summary for one person at a given year and age. Your job is to propose a small set of plausible candidate events and relationship magnets for the coming year — not to set any numbers or deltas.

Rules you must follow:
- Do not output any numerical deltas. You propose causal hypotheses (what might happen and why it fits this state), not capacity/domain/crack numbers.
- Preconditions must reference only: age, hostage_index, coercion, capacity (vitality, aperture, binding, coherence, agency, reality_anchor, transmutation), wound sensitivities (shame, fear, anger, abandonment, control, recognition, loss), and optionally frameworks.<id>.weight. Keep conditions simple: comparisons and conjunctions only.
- Output valid JSON only. No commentary outside the JSON.
- Caps: at most 6 event_candidates, 4 magnet_candidates, 3 branch_hypotheses. If you generate more, the parser will truncate.
- Event kinds: relationship, institution, puncture, opportunity, practice, loss, achievement, humiliation, move, health, violence, media, epistemic_rupture, expectation_event.
- Practice events (kind: practice): Include at least one practice event when the state shows active mentor, teacher, or arts/scene magnets, or when strivings involve competence, creation, or skill-building. These are not dramatic events — they are sustained engagement moments: a workshop attended, a rehearsal, a manuscript revised, an apprenticeship session, a technique learned. Use channels: school, work, neighborhood, movement. Do not omit practice events when the person is embedded in a field through magnets.
- For expectation_event: set expectation_type (fulfillment or violation) and striving_object_id (id of an active striving from summary.striving_objects) so the system can create GiftShard or DisruptionShard.
- Intensity per event: minor, major, or shock.
- Channels: family, peer, school, work, sect, state, media, online, movement, neighborhood, diaspora.
- Magnet types: friend, mentor, romance, leader, teacher, boss, institution, scene, online_cluster.
- For each candidate, explain why it fits this person now (plausibility_notes.why_now) and what would make it unlikely (what_makes_it_unlikely).
- If a "### Historical backdrop" block is present before the state summary: use it to anchor events in real history. The backdrop describes the actual political, economic, or social conditions in this country during this period. Proposed events should feel like things that happen to real people living inside those conditions — not generic life events that could happen anywhere. The backdrop is context, not a script; do not reproduce it verbatim.
- active_cracks: domain tensions that are active this year. When a crack is present (e.g. sect_class, nation_state), it means the person feels cumulative pressure or contradiction in that domain. Cracks shape what kinds of events are plausible — a crack in sect_class makes religious/ethnic identity events more likely; a crack in nation_state makes political/legal events more pressing. Use crack tension to anchor event plausibility (why now) and what might give way (what_makes_it_unlikely).
- calibration_regime: the social norm environment this person lives in. norm_center describes whether they are in a middle/mainstream vs. outlier/edge social position. outlier_penalties and outlier_incentives describe what behaviors are punished or rewarded in their community. Use these to decide whether a candidate event is socially dangerous or socially expected. A political event in a high-penalty calibration regime is a different kind of event than the same event in an incentivizing regime. uniqueness_norm describes how much the community values standing out vs. fitting in.
- child_model: the assumptions-rules-taboos this person carried from childhood — what they were taught adults are like, what was forbidden to name, and what counted as possible. These are not always what the person now believes, but they are the default architecture. When a candidate event touches an assumed rule or a taboo, it is more psychologically volatile. An event that violates what the child model assumed about adults (e.g. "Adults are mostly fair" → a teacher's deliberate cruelty) is an epistemic_rupture candidate.
- expectation_baseline: per-need-axis entitlement. Each entry (attachment: entitled/hopeful/forbidden/hopeless) describes what this person expects from life on that need axis. forbidden means they learned not to want it; hopeless means they learned they can't get it. When an event targets a forbidden or hopeless need axis (via striving_object_id), the event has higher psychological stakes — the success or failure doesn't just affect the outcome, it rewrites what they believed possible. Use this to select expectation_type (fulfillment for forbidden→repaired, violation for hopeful→shattered).
- metabolic_style: how this person processes rupture. transmuting means they actively transform pain into meaning; compartmentalizing means they keep domains isolated; anesthetizing means they numb; collapsing means they fall apart. Use this to shape event intensity and plausibility: a collapsing person experiences events as shocks that overwhelm them; a compartmentalizing person can experience a major rupture in one domain while appearing stable in others.
- registers: the expression gates (public_expression_gate, private_expression_gate, inner_load). Public expression gate describes how much this person can show in public; private describes what they can show in intimate settings. When a candidate event places the person in a public channel (school, work, media, state) with low public_expression_gate, the event carries additional tension — they are exposed but cannot show it.
- practices (study, care, organizing, craft, spiritual, risk_training): what this person is actively doing. When a practice value is high, the person is embedded in that activity field. Events that narrate from inside active practices (a study crisis, a caregiving milestone, an organizing confrontation, a craft breakthrough, a spiritual practice event, a risk/reward moment) ring truer than generic events. Use practices to generate kind=practice events that feel specific to this person's active life.
"""

PASS1_USER_PREFIX = """State summary for this person (year and age at start of the year to simulate):

"""

PASS1_SUGGESTED_TARGETS_BLOCK = """

Suggested event targets for active strivings (propose events that match these when plausible; use expectation_type and striving_object_id from striving_objects):
"""

PASS2_SYSTEM = """You are a narrative renderer for a year-step life simulation. You receive the selected events, applied deltas, and full persona context for one year of a person's life. Your job is to write a scene — not a summary, not a description of a person, but a scene: a specific hour or day that shows this year from inside this person's sensorium and assumptions.

## Rendering from the inside

The scene renders from inside this person's way of seeing, not from outside describing them. You do not describe them. You inhabit their vantage point: what they notice, what they assume, what they expect. The reader should feel placed in their body.

If the render packet includes a "persona_context" object, treat it as the operating system for the scene:

- persona_context.structural_lucidity: how much structural awareness this person has. If "none" or "minimal" — they must not think in systems. They think in people, effort, luck, character. When something goes wrong it is because someone failed them or they failed themselves, not because of a structure. Do not write a person who understands their situation analytically when the data says they cannot.

- persona_context.wound_pattern: the sensitized wounds this person carries. Elevated abandonment means: they have already half-expected this loss before it happened. They brace before the blow lands. They manage the exit before it's requested. Show the anticipatory posture, not just the reaction. Someone with high abandonment wound doesn't get surprised when a friend leaves — they get confirmed.

- persona_context.strata_position: class, ethnicity, and place are not backstory — they are the texture of every social interaction. "Lower-middle class in Andorra" means you know the price of everything and feel the gap in everything. "Portuguese-ethnic minority" means you speak the language of this place fluently but can be reminded at any moment that you are from elsewhere. These things live in the body and the attention, not in explicit thought.

- persona_context.rupture_notes: violated assumptions this person still carries. They don't know them as "ruptures" — they know them as the things they stopped counting on, the things they learned cost you. These operate as invisible filters on perception. Show them shaping what the person notices and avoids, without ever naming them.

## If the identity has 3+ languages

Language itself is part of this person's texture. There is a language for home, a language for school, possibly a language for certain registers of feeling. The scene must contain at least one moment where language is present as a fact — a word, a switch, a phrase heard that lands differently depending on who is speaking it. Not as a curiosity. As a lived condition.

## If the identity object is present

The scene MUST be about THIS person in THIS place — their actual name, locality, ethnicity, and community. Do not substitute. Do not genericize.

## Structural rules

- "scene" field is required: 350–900 words. A concrete moment or day — who is there, what shifts, what is said, what is felt. Not a summary of a year.
- Do not output numbers. You only produce narrative and metadata (which_strata_fired, which_frameworks_fired, what_was_buffered, what_scratched).
- Include dialogue_snippets: short quotes, speaker labeled (self, mother, friend, teacher, other).
- consistency_check: did_not_resolve, public_vs_private_register_obeyed — set true only if your narrative genuinely obeys them.

## Particularity (required — not decoration, the scene itself)

The 8 particularity anchors are not optional decoration. They ARE the scene. A scene that can't name a specific place, a specific cost or lack, a specific power relation, a specific somatic response is not a scene about this person — it is a scene about a type. Every anchor must be specific enough that it could only happen here, to this person:
- place_anchor: named location with one micro-detail (not "a park" — a specific bench, a specific smell, a specific building)
- object_anchor: one object, sensory — what it feels/sounds/smells like in this moment
- schedule_anchor: time of day and the constraint it implies (why this time, what is before or after)
- money_anchor: a specific cost, amount, or lack — and its consequence for this scene
- language_anchor: a specific phrase, who says it, what it actually means under the surface
- power_anchor: who has power in this scene, how it shows without being stated
- body_anchor: a somatic response — what the body does that the mind hasn't caught up with
- social_risk_anchor: what could go wrong socially here, and the avoidance move

## Jaggedness (required — must be demonstrated, not stated)

Exactly 2 entries. Each: {"and": ["trait1", "trait2"], "where": "where in scene it shows"}. Use pairs: warmth/cruelty, pride/shame, devotion/resentment, clarity/self-deception, tenderness/domination, generosity/exclusion, courage/cowardice, loyalty/betrayal, sincerity/performance. The contradiction must live in the scene — a moment where both traits are visible in the same action or exchange, not in different paragraphs.

## Micro-causality (required)

1–2 entries. Each: {"detail": "concrete detail", "caused": "what it led to"}. A specific thing that caused a specific outcome — not a vague theme producing a vague mood.

## Person stubs (optional)

0–2 new people if the scene introduces someone. Each: name, role, signature (one recurring habit), moral_edge (decent + compromised), speech_tic, status_marker, pressure_point.

Output valid JSON only. No markdown, no code fences, no commentary outside the JSON.
"""

PASS2_USER_PREFIX = """Render packet (selected events + applied deltas + persona context):

"""


def build_pass1_prompt(
    state_summary: dict[str, Any],
    suggested_event_targets: list[dict[str, Any]] | None = None,
    historical_backdrop: str | None = None,
) -> str:
    """
    Build the full Pass 1 prompt: system instructions + user message containing
    the state summary as JSON. When suggested_event_targets is provided (from
    expectation_event_templates filtered by active strivings), appends a block
    so the LLM can propose events that match these targets and attach to strivings.
    When historical_backdrop is provided, prepends a country/decade context block
    so proposed events are grounded in real historical conditions.
    """
    user_body = PASS1_USER_PREFIX + json.dumps(state_summary, indent=2)
    if suggested_event_targets:
        user_body += "\n\nSuggested event targets for active strivings (propose events that match these when plausible; set expectation_type and striving_object_id):\n"
        user_body += json.dumps(suggested_event_targets, indent=2)
    if historical_backdrop:
        user_body = (
            f"### Historical backdrop for this country and period\n{historical_backdrop}\n\n"
            + user_body
        )
    return _format_two_part(PASS1_SYSTEM, user_body)


def build_pass2_prompt(render_packet: dict[str, Any]) -> str:
    """
    Build the full Pass 2 prompt: system instructions + user message containing
    the RenderPacket as JSON. The LLM should respond with a RenderOutput (JSON).
    """
    # If previous_scene is present, prepend a continuity note
    user_body = ""
    prev_scene = render_packet.get("previous_scene", "")
    if prev_scene and isinstance(prev_scene, str) and prev_scene.strip():
        user_body = (
            f"## Previous year's scene (for narrative continuity — carry forward what survived, reference shared people/places, show what shifted):\n{prev_scene.strip()}\n\n"
        )
    # Awareness gating: per-domain constraints on what the persona can perceive
    awareness_gating = render_packet.get("awareness_gating", {})
    if awareness_gating and isinstance(awareness_gating, dict):
        user_body += "## Awareness gating (what this person can perceive — you MUST obey these per-domain constraints):\n"
        for domain, constraint in awareness_gating.items():
            if constraint:
                user_body += f"- {domain}: {constraint}\n"
        user_body += "\n"
    user_body += PASS2_USER_PREFIX + json.dumps(render_packet, indent=2)
    return _format_two_part(PASS2_SYSTEM, user_body)


def _format_two_part(system: str, user_content: str) -> str:
    """Simple concatenation: system first, then user block. Caller can wrap for API (e.g. role labels)."""
    return system.strip() + "\n\n---\n\n" + user_content.strip()


def pass2_corrective_instruction(failures: list[str]) -> str:
    """Instruction to fix particularity/jaggedness failures. Replace only the failing parts and rewrite scene to demonstrate."""
    return (
        "\n\nYour previous response failed validation: " + "; ".join(failures) + ". "
        "Fix only the particularity block and jaggedness to meet the requirements. "
        "Rewrite the scene so it demonstrates the two jaggedness contradictions. "
        "Keep selected events and deltas identical. Output valid JSON again (same keys)."
    )


def pass1_response_instruction() -> str:
    """Short instruction to append to Pass 1 so the model knows the expected response format."""
    return (
        "\n\nRespond with a single JSON object: CandidatePacket with keys "
        "year, age, event_candidates (0–6), magnet_candidates (0–4), branch_hypotheses (0–3). "
        "Each event_candidate: id, kind, label, logline, intensity, channels, implicated (domains, strata_levels; optional positions), magnets (offers/costs), hooks (wound_hooks, capacity_hooks), preconditions (optional), plausibility_notes. For kind expectation_event add expectation_type (fulfillment|violation) and striving_object_id (id from striving_objects). "
        "Each magnet_candidate: id, magnet_type, label, who, entry_point, stickiness, offers, costs, compatibility (attractors, repulsors), trajectory_branches, implicated."
    )


def pass2_response_instruction() -> str:
    """Short instruction to append to Pass 2 so the model knows the expected response format."""
    return (
        "\n\nRespond with a single JSON object only (no markdown, no ```). RenderOutput with keys: "
        "narrative_snapshot (required: scene must be a non-empty string, 2–4 sentences minimum; also which_strata_fired, which_frameworks_fired, what_was_buffered, what_scratched), "
        "dialogue_snippets (list of {speaker, line}), "
        "consistency_check (did_not_resolve, public_vs_private_register_obeyed)."
    )
