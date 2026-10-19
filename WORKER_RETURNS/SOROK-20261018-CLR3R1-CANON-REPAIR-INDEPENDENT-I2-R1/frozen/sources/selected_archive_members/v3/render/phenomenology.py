# v3/render/phenomenology.py — write rendered_output only; must not mutate backbone.
# Wave 4: optional Pass 2 LLM render when render_packet + llm_callback provided.

from __future__ import annotations

import logging
from typing import Any, Callable

from v3.core.state import BackboneState
from v3.core.derived import DerivedIndices
from v3.engine.llm_contract import parse_render_output
from v3.engine.prompts import build_pass2_prompt, pass2_response_instruction, pass2_corrective_instruction
from v3.engine.validators import validate_render_output

logger = logging.getLogger(__name__)
_PASS2_LOG_MAX_RAW = 800  # truncate raw response in logs

# Developmental gating (revision 2026.02.25): no adult-cognitive overlays in early childhood.
AGE_TIER_0_3 = "age_0_3"
AGE_TIER_4_10 = "age_4_10"
AGE_TIER_11_18 = "age_11_18"
AGE_TIER_19_PLUS = "age_19_plus"


def developmental_age_tier(age: int) -> str:
    """Return age tier for gating: 0-3 sensory/attachment, 4-10 fairness no political, 11-18 ideology/status, 19+ full."""
    if age <= 3:
        return AGE_TIER_0_3
    if age <= 10:
        return AGE_TIER_4_10
    if age <= 18:
        return AGE_TIER_11_18
    return AGE_TIER_19_PLUS


def developmental_gating_rule(age: int) -> str:
    """Short rule string for prompt or fallback: what is allowed at this age."""
    tier = developmental_age_tier(age)
    if tier == AGE_TIER_0_3:
        return (
            "Use sensory/attachment language only. Avoid abstract moral categories (justice, order, legitimacy). "
            "Express as felt predictability, warmth, danger, bodily comfort, proximity, routine."
        )
    if tier == AGE_TIER_4_10:
        return (
            "Allow fairness instincts and concrete rules; still avoid political abstractions."
        )
    if tier == AGE_TIER_11_18:
        return (
            "Introduce ideology seeds, humiliation/status, authority meanings."
        )
    return "Full abstraction allowed."


def render_year(
    state: BackboneState,
    derived: DerivedIndices | None,
    config: dict,
    render_packet: dict[str, Any] | None = None,
    llm_callback: Callable[[str, str], str] | None = None,
) -> None:
    """
    Set state.rendered_output to year, age, derived. Must not change other state.
    If render_packet and llm_callback are provided, run Pass 2: build prompt, call LLM,
    parse RenderOutput, merge narrative_snapshot, dialogue_snippets, consistency_check into output.
    """
    base: dict[str, Any] = {
        "year": state.year,
        "age": state.age,
        "derived": (
            {
                "hostage_index": derived.hostage_index,
                "agency_capacity_AC": derived.agency_capacity_AC,
                "structural_lucidity_SL": derived.structural_lucidity_SL,
                "peak_regime": derived.peak_regime,
            }
            if derived
            else {}
        ),
    }
    if render_packet and llm_callback:
        raw = None
        try:
            prompt = build_pass2_prompt(render_packet) + pass2_response_instruction()
            # Stage label used by server/app logging; simple callbacks may ignore it.
            stage_label = f"llm_band_pass2_age_{state.age}"
            raw = llm_callback(stage_label, prompt)
            if not raw or not raw.strip():
                logger.warning(
                    "Pass 2 (age=%s): empty LLM response; narrative_snapshot will be empty.",
                    state.age,
                )
                base["narrative_snapshot"] = {"scene": "", "pass2_empty_response": True}
            else:
                parsed = parse_render_output(raw)
                validation_history = config.get("render_validation_history") or []
                all_ok, failures = validate_render_output(parsed, history=validation_history)
                if not all_ok and failures:
                    corrective = pass2_corrective_instruction(failures)
                    try:
                        prompt_retry = build_pass2_prompt(render_packet) + pass2_response_instruction() + "\n\n" + corrective
                        raw2 = llm_callback(stage_label + "_retry", prompt_retry)
                        if raw2 and raw2.strip():
                            parsed2 = parse_render_output(raw2)
                            ok2, _ = validate_render_output(parsed2, history=validation_history)
                            if ok2:
                                parsed = parsed2
                                raw = raw2
                                all_ok = True
                    except Exception:
                        pass
                    if not all_ok:
                        logger.warning("Pass 2 (age=%s): validation failures %s; using first parse.", state.age, failures[:3])
                _ns_raw = parsed.get("narrative_snapshot") or {}
                # Normalize: LLM sometimes returns narrative_snapshot as a plain string
                # instead of the expected {"scene": "...", ...} dict.
                if isinstance(_ns_raw, str):
                    _ns_raw = {"scene": _ns_raw}
                base["narrative_snapshot"] = _ns_raw
                base["dialogue_snippets"] = parsed.get("dialogue_snippets") or []
                base["consistency_check"] = parsed.get("consistency_check") or {}
                base["particularity"] = parsed.get("particularity") or {}
                base["jaggedness"] = parsed.get("jaggedness") or []
                base["micro_causality"] = parsed.get("micro_causality") or []
                base["person_stubs"] = parsed.get("person_stubs") or []
                # Propagate parse/render integrity from llm_contract into rendered output
                if isinstance(_ns_raw, dict) and _ns_raw.get("_integrity"):
                    base["_integrity"] = _ns_raw["_integrity"]
                elif isinstance(_ns_raw, dict) and _ns_raw.get("_scene_fallback"):
                    base["_integrity"] = {"status": "degraded", "reason": "pass2_scene_fallback"}
                scene = (base["narrative_snapshot"] or {}).get("scene", "")
                if not (scene and isinstance(scene, str) and scene.strip()):
                    logger.warning(
                        "Pass 2 (age=%s): parsed OK but scene empty or missing; raw excerpt: %s",
                        state.age,
                        raw[: _PASS2_LOG_MAX_RAW].replace("\n", " "),
                    )
                    base["narrative_snapshot"]["scene"] = "[This year had no recorded scene.]"
                    base["narrative_snapshot"]["pass2_scene_fallback"] = True
                    base["_integrity"] = {"status": "degraded", "reason": "pass2_scene_fallback"}
        except Exception as e:
            try:
                raw_preview = (raw[: _PASS2_LOG_MAX_RAW] + "…").replace("\n", " ") if raw else "(no raw)"
            except Exception:
                raw_preview = "(no raw)"
            logger.warning(
                "Pass 2 (age=%s): parse or LLM failed: %s; raw excerpt: %s",
                state.age,
                e,
                raw_preview,
            )
            base["narrative_snapshot"] = {
                "scene": "[This year had no recorded scene.]",
                "pass2_parse_error": str(e),
            }
    state.rendered_output = base
