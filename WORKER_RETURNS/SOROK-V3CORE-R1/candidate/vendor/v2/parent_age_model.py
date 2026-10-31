"""
Parent age + age-gap generator.

Goal: produce "human-feeling" parents at a child's birth year without faking
global precision. This is a two-layer system:
- global priors that always work
- optional overrides (country/cohort/urbanicity/etc.) when available

Outputs are *ages at child's birth* + metadata (gap component, story flags).
"""

from __future__ import annotations

import json
import os
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, List


_DEFAULT_MODEL_PATH = Path(__file__).parent / "config" / "parent_age_model.json"


def _clamp(x: float, lo: float, hi: float) -> float:
    return lo if x < lo else hi if x > hi else x


def _weighted_choice(components: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = sum(float(c.get("weight", 0)) for c in components)
    if total <= 0:
        return components[0]
    r = random.random() * total
    acc = 0.0
    for c in components:
        acc += float(c.get("weight", 0))
        if r <= acc:
            return c
    return components[-1]


def _sample_trunc_normal(mean: float, sd: float, lo: float, hi: float, max_tries: int = 200) -> float:
    # Basic rejection sampling is fine at this scale.
    for _ in range(max_tries):
        x = random.gauss(mean, sd)
        if lo <= x <= hi:
            return x
    return _clamp(mean, lo, hi)


def _sample_dist(dist: Dict[str, Any]) -> float:
    typ = dist.get("type")
    if typ == "normal":
        mean = float(dist["mean"])
        sd = float(dist["sd"])
        lo, hi = dist.get("clip", [-1e9, 1e9])
        return _sample_trunc_normal(mean, sd, float(lo), float(hi))
    if typ == "uniform":
        lo = float(dist["min"])
        hi = float(dist["max"])
        return random.uniform(lo, hi)
    raise ValueError(f"Unknown dist type: {typ}")


def _load_model(path: Optional[str] = None) -> Dict[str, Any]:
    p = Path(path) if path else _DEFAULT_MODEL_PATH
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def _override_key(country_code: str, child_birth_year: int, urbanicity: Optional[str] = None) -> str:
    # Minimal: exact year + urbanicity if provided.
    # (You can later add cohort bins / decade keys here.)
    if urbanicity:
        return f"{country_code}_{child_birth_year}_{urbanicity}"
    return f"{country_code}_{child_birth_year}"


@dataclass(frozen=True)
class ParentAgeSample:
    parent_a_age_at_birth: int
    parent_b_age_at_birth: int
    gap_b_minus_a: int
    a_component: str
    gap_component: str
    resamples: int
    story_reason_required: bool
    story_reason_hint: Optional[str]


def sample_parent_ages_at_birth(
    *,
    country_code: str,
    child_birth_year: int,
    urbanicity: Optional[str] = None,
    model_path: Optional[str] = None,
    allow_story_reasons: bool = False,
    rng_seed: Optional[int] = None,
) -> ParentAgeSample:
    """
    Sample (Parent A age at child's birth) + (Parent B - Parent A gap), with plausibility gates.

    Parent A is the "gestational/younger-typical" anchor by default; Parent B is derived from gap.
    Caller can map A/B to mother/father based on roles.
    """
    if rng_seed is not None:
        random.seed(rng_seed)

    model = _load_model(model_path)
    gates = model.get("plausibility_gates", {})

    min_parent_age = int(gates.get("min_parent_age", 19))
    min_father_age = int(gates.get("min_father_age", 21))
    max_gap_without_story = int(gates.get("max_gap_without_story", 15))
    lifestage_min_young = int(gates.get("lifestage_min_young", 22))
    lifestage_max_old = int(gates.get("lifestage_max_old", 40))
    max_resamples = int(gates.get("max_resamples", 50))
    fallback_gap_clip = gates.get("fallback_gap_clip", [-6, 10])
    fallback_gap_lo, fallback_gap_hi = int(fallback_gap_clip[0]), int(fallback_gap_clip[1])

    key = _override_key(country_code, child_birth_year, urbanicity)

    a_cfg = model.get("age_at_birth_model", {}).get("default", {})
    a_overrides = model.get("age_at_birth_model", {}).get("overrides", {})
    if key in a_overrides:
        a_cfg = a_overrides[key]

    gap_cfg = model.get("age_gap_model", {}).get("default", {})
    gap_overrides = model.get("age_gap_model", {}).get("overrides", {})
    if key in gap_overrides:
        gap_cfg = gap_overrides[key]

    a_components = a_cfg.get("components", [])
    gap_components = gap_cfg.get("components", [])
    if not a_components or not gap_components:
        raise ValueError("parent_age_model.json missing required components")

    def check_story_flags(a_age: int, b_age: int, gap: int) -> Tuple[bool, Optional[str]]:
        # Large gaps should not appear as "random flavor" unless caller allows story reasons.
        if abs(gap) > max_gap_without_story:
            return True, "large_gap_outside_default_social_band"
        # Life-stage mismatch: very young with much older.
        young = min(a_age, b_age)
        old = max(a_age, b_age)
        if young < lifestage_min_young and old > lifestage_max_old:
            return True, "life_stage_mismatch"
        return False, None

    resamples = 0
    last_a_component = "typical"
    last_gap_component = "near_peers"

    while resamples <= max_resamples:
        a_comp = _weighted_choice(a_components)
        last_a_component = str(a_comp.get("name", "unknown"))
        a_age = int(round(_sample_dist(a_comp["dist"])))

        gap_comp = _weighted_choice(gap_components)
        last_gap_component = str(gap_comp.get("name", "unknown"))
        gap = int(round(_sample_dist(gap_comp["dist"])))

        b_age = a_age + gap

        # Hard gates: minimum parenting age (mother >= min_parent_age, father >= min_father_age).
        if a_age < min_parent_age or b_age < min_father_age:
            resamples += 1
            continue

        story_required, story_hint = check_story_flags(a_age, b_age, gap)
        if story_required and not allow_story_reasons:
            # Resample unless caller explicitly allows "weird with scaffolding".
            resamples += 1
            continue

        return ParentAgeSample(
            parent_a_age_at_birth=a_age,
            parent_b_age_at_birth=b_age,
            gap_b_minus_a=gap,
            a_component=last_a_component,
            gap_component=last_gap_component,
            resamples=resamples,
            story_reason_required=story_required,
            story_reason_hint=story_hint,
        )

    # Fallback: safe clip gap, keep a_age from typical component.
    a_comp = next((c for c in a_components if c.get("name") == "typical"), a_components[0])
    a_age = int(round(_sample_dist(a_comp["dist"])))
    gap = int(round(_clamp(random.gauss(1, 2.5), fallback_gap_lo, fallback_gap_hi)))
    b_age = max(min_parent_age, a_age + gap)
    story_required, story_hint = check_story_flags(a_age, b_age, gap)
    return ParentAgeSample(
        parent_a_age_at_birth=a_age,
        parent_b_age_at_birth=b_age,
        gap_b_minus_a=gap,
        a_component=str(a_comp.get("name", "unknown")),
        gap_component="fallback_safe_clip",
        resamples=max_resamples,
        story_reason_required=story_required,
        story_reason_hint=story_hint,
    )

