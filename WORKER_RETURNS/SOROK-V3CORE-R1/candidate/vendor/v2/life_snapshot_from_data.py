"""
Data-governed life_snapshot derivation for present-year (17+) recursion.

Uses identity, world_slice, and current state (needs, strategies, indices) to compute
as much of life_snapshot as possible from config and formulas. The recursion prompt
receives data_derived + valid_options so the LLM confirms or picks from constrained
choices rather than inventing.

Config: v2/config/life_snapshot.yaml
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, Tuple
import yaml


def _load_config() -> Dict[str, Any]:
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "config", "life_snapshot.yaml")
    if not os.path.isfile(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _get(obj: Any, *keys: str, default: Any = None) -> Any:
    for k in keys:
        if obj is None:
            return default
        if isinstance(obj, dict):
            obj = obj.get(k)
        else:
            obj = getattr(obj, k, None)
    return obj if obj is not None else default


def _age_band(age: int) -> str:
    if age < 25:
        return "17-24"
    if age < 35:
        return "25-34"
    if age < 50:
        return "35-49"
    return "50+"


def _class_stress_weight(current_class: str) -> float:
    w = {
        "underclass": 1.0,
        "working": 0.8,
        "lower_middle": 0.5,
        "middle": 0.2,
        "upper_middle": 0.1,
        "elite": 0.0,
    }
    return w.get((current_class or "").lower(), 0.5)


def compute_income_stress(
    world_slice: Any,
    identity: Any,
    needs: Any,
    config: Dict[str, Any],
) -> str:
    """Fully data-derived from gdp, inequality, class, needs.safety."""
    formula = config.get("income_stress", {}).get("formula", {})
    bands = config.get("income_stress", {}).get("bands", {})
    gdp = _get(world_slice, "gdp_per_capita", default=50.0)
    if not isinstance(gdp, (int, float)):
        gdp = 50.0
    gdp = max(0, min(100, float(gdp)))
    ineq = _get(world_slice, "inequality_index", default=50.0)
    ineq = max(0, min(100, float(ineq)))
    current_class = _get(identity, "current_class", default="working") or "working"
    safety = _get(needs, "safety", default=50.0)
    safety = max(0, min(100, float(safety)))

    gw = formula.get("gdp_weight", 0.3)
    iw = formula.get("inequality_weight", 0.25)
    cw = formula.get("class_weight", 0.25)
    sw = formula.get("safety_weight", 0.2)

    # Higher GDP → less stress; higher inequality → more stress
    gdp_component = (100 - gdp) / 100.0
    ineq_component = ineq / 100.0
    class_component = _class_stress_weight(current_class)
    safety_component = (100 - safety) / 100.0

    score = (
        gdp_component * gw
        + ineq_component * iw
        + class_component * cw
        + safety_component * sw
    ) * 100.0
    score = max(0, min(100, score))

    for level, (lo, hi) in bands.items():
        if lo <= score < hi:
            return level
    return "medium"


def compute_internet_access_patterns(
    world_slice: Any,
    identity: Any,
    config: Dict[str, Any],
) -> str:
    """From media_saturation (country internet %), SES, urbanicity."""
    formula = config.get("internet_access_patterns", {}).get("formula", {})
    band_list = formula.get("bands", [])
    country_pct = _get(world_slice, "media_saturation", default=0.0)
    country_pct = max(0, min(100, float(country_pct)))
    current_class = (_get(identity, "current_class", default="middle") or "middle").lower()
    urbanicity = (_get(identity, "urbanicity", default="town") or "town").lower()

    # Find band index: first band where country_pct <= max_country_pct (0=worst, len-1=best)
    idx = 0
    for i, b in enumerate(band_list):
        max_pct = b.get("max_country_pct", 100)
        if country_pct <= max_pct:
            idx = i
            break
        idx = i + 1
    idx = min(idx, len(band_list) - 1)

    # SES/urban: lower class or rural → worse access (lower index)
    if formula.get("ses_modifier"):
        if current_class in ("underclass", "working", "lower_middle"):
            idx = max(0, idx - 1)
    if formula.get("urban_modifier") and "rural" in urbanicity:
        idx = max(0, idx - 1)

    if band_list and 0 <= idx < len(band_list):
        return band_list[idx].get("default", "work_and_phone")
    return "work_and_phone"


def compute_social_circle_density(needs: Any, config: Dict[str, Any]) -> str:
    """From needs.belonging_group bands."""
    bands = config.get("social_circle_density", {}).get("formula", {}).get("bands", {})
    belonging = _get(needs, "belonging_group", default=50.0)
    belonging = max(0, min(100, float(belonging)))
    for level, (lo, hi) in bands.items():
        if lo <= belonging < hi:
            return level
    return "moderate"


def compute_sleep_debt_baseline(
    indices: Any,
    strategies: Any,
    config: Dict[str, Any],
) -> str:
    """From RMT and dissociation/withdrawal strategies."""
    bands = config.get("sleep_debt_baseline", {}).get("bands", {})
    formula = config.get("sleep_debt_baseline", {}).get("formula", {})
    rmt = _get(indices, "recursive_madness_threshold", default=0.0)
    rmt = max(0, min(100, float(rmt)))
    diss = _get(strategies, "dissociation_numbing", default=0.0)
    withd = _get(strategies, "withdrawal_avoidance", default=0.0)
    strategy_score = (float(diss) + float(withd)) / 2.0

    rw = formula.get("rmt_weight", 0.5)
    sw = formula.get("strategy_weight", 0.3)
    score = (rmt / 100.0) * rw * 100.0 + (strategy_score / 100.0) * sw * 100.0
    score = max(0, min(100, score * 1.2))  # scale so we hit bands

    for level, (lo, hi) in bands.items():
        if lo <= score < hi:
            return level
    return "light"


def _narrow_job_types(
    job_weights: Dict[str, float],
    identity: Any,
    config: Dict[str, Any],
) -> Tuple[Dict[str, float], List[str]]:
    """
    Plausibly narrow job_type to those allowed by urbanicity and (optionally) country.
    Returns (filtered_weights, allowed_values_list) for sampling and valid_options.
    """
    narrow = config.get("job_type", {}).get("narrow_by", {})
    if not narrow:
        return job_weights, list(job_weights.keys()) if job_weights else []

    allowed: Optional[List[str]] = None
    urbanicity = (_get(identity, "urbanicity", default="town") or "town").lower()
    # Map to config key: rural, town, city, megacity
    urb_key = "rural" if "rural" in urbanicity else "town"
    if "city" in urbanicity or "urban" in urbanicity:
        urb_key = "city"
    if "mega" in urbanicity:
        urb_key = "megacity"
    urbanicity_allowed = narrow.get("urbanicity_allowed", {})
    urb_list = urbanicity_allowed.get(urb_key)
    if urb_list is not None and isinstance(urb_list, list):
        allowed = list(urb_list)

    country = (_get(identity, "country_code", default="") or "").upper()
    country_allowed = narrow.get("country_allowed", {})
    if country and country in country_allowed:
        country_list = country_allowed.get(country)
        if isinstance(country_list, list):
            allowed = country_list if allowed is None else [k for k in allowed if k in country_list]

    if allowed is not None:
        filtered = {k: w for k, w in job_weights.items() if k in allowed and (w or 0) > 0}
        if not filtered:
            # Fallback: keep at least the top 3 by weight from original
            top = sorted(job_weights.keys(), key=lambda x: job_weights.get(x, 0), reverse=True)[:5]
            filtered = {k: job_weights[k] for k in top if k in job_weights}
        allowed_values = list(filtered.keys())
        return filtered, allowed_values
    return job_weights, list(job_weights.keys()) if job_weights else []


def sample_from_weights(weights: Dict[str, float], rng: Any = None) -> str:
    """Pick one key by weight. If rng is None, pick highest weight."""
    if not weights:
        return "other"
    if rng is not None and hasattr(rng, "choice"):
        import random
        choices = list(weights.keys())
        probs = [weights.get(k, 0) for k in choices]
        total = sum(probs)
        if total <= 0:
            return max(weights, key=weights.get)
        probs = [p / total for p in probs]
        return rng.choice(choices, p=probs)
    return max(weights, key=lambda k: weights.get(k, 0))


def data_derived_life_snapshot(
    identity: Any,
    world_slice: Any,
    state: Any,
    *,
    config: Optional[Dict[str, Any]] = None,
    rng: Any = None,
) -> Tuple[Dict[str, Any], Dict[str, List[str]]]:
    """
    Compute life_snapshot from pipeline data. Returns (data_derived, valid_options).

    - data_derived: dict with all life_snapshot keys; values are either computed
      (income_stress, internet_access_patterns, social_circle_density, sleep_debt_baseline)
      or sampled from config priors (job_type, commute_style, living_arrangement,
      family_obligations) so the LLM can confirm or override.
    - valid_options: for each key, list of allowed values to pass into the recursion
      prompt so the LLM only picks from these.
    """
    cfg = config or _load_config()
    needs = _get(state, "needs")
    strategies = _get(state, "strategies")
    indices = _get(state, "indices")
    age = _get(state, "age", default=25)
    if not age and identity:
        age = _get(identity, "age_at_anchor", default=25)
    age = age or 25
    band = _age_band(age)
    current_class = (_get(identity, "current_class", default="working") or "working").lower()
    urbanicity = (_get(identity, "urbanicity", default="town") or "town").lower()

    # Fully formula-derived
    income_stress = compute_income_stress(world_slice, identity, needs, cfg)
    internet_access_patterns = compute_internet_access_patterns(world_slice, identity, cfg)
    social_circle_density = compute_social_circle_density(needs, cfg)
    sleep_debt_baseline = compute_sleep_debt_baseline(indices, strategies, cfg)

    # Sampled from config priors (data-constrained); blend in country-year structure when available
    by_ses = cfg.get("job_type", {}).get("by_ses", {})
    job_weights = dict(by_ses.get(current_class, by_ses.get("working", {"other": 1.0})))
    meta = _get(world_slice, "metadata") or {}
    ag_pct = meta.get("employment_agriculture_pct")
    schooling = meta.get("mean_years_schooling")
    if ag_pct is not None and ag_pct > 0:
        # Higher agriculture employment → more farm_labor (and slightly informal)
        boost = min(0.4, (float(ag_pct) / 100.0) * 0.6)
        job_weights["farm_labor"] = job_weights.get("farm_labor", 0) + boost
        job_weights["informal_vendor"] = job_weights.get("informal_vendor", 0) + boost * 0.3
    if schooling is not None and float(schooling) < 6:
        # Low mean years schooling → more informal/farm_labor, less back_office
        job_weights["informal_vendor"] = job_weights.get("informal_vendor", 0) + 0.2
        job_weights["farm_labor"] = job_weights.get("farm_labor", 0) + 0.15
        job_weights["back_office"] = max(0, (job_weights.get("back_office", 0) - 0.2))
    # Narrow to plausible set by urbanicity (and optional country); then sample
    job_weights, job_type_allowed = _narrow_job_types(job_weights, identity, cfg)
    job_type = sample_from_weights(job_weights, rng)

    commute_by = cfg.get("commute_style", {}).get("by_job_urban", {})
    commute_weights = commute_by.get(job_type)
    if not commute_weights:
        # Fallback: map new job_type names to legacy keys (unemployed_* -> unemployed, student_* -> student)
        if job_type and ("unemployed" in job_type):
            commute_weights = commute_by.get("unemployed")
        elif job_type and ("student" in job_type):
            commute_weights = commute_by.get("student")
        else:
            commute_weights = None
    if not commute_weights:
        commute_weights = (
            cfg.get("commute_style", {}).get("urban_default")
            if "rural" not in urbanicity
            else cfg.get("commute_style", {}).get("rural_default")
        ) or {"bus": 0.4, "car": 0.3, "walk": 0.2, "none": 0.1}
    commute_style = sample_from_weights(commute_weights, rng)

    living_by_age = cfg.get("living_arrangement", {}).get("by_age_band", {})
    living_weights = living_by_age.get(band, {"with_family": 0.3, "alone": 0.3, "with_partner": 0.3})
    living_arrangement = sample_from_weights(living_weights, rng)

    family_by_age = cfg.get("family_obligations", {}).get("by_age_band", {})
    family_weights = family_by_age.get(band, {"light": 0.4, "none": 0.3})
    family_obligations = sample_from_weights(family_weights, rng)

    # current_life_phase: taxonomy; data can suggest from events/strategies, LLM picks
    phase_values = cfg.get("current_life_phase", {}).get("values", ["stable_routine_phase", "other"])
    current_life_phase = "stable_routine_phase"  # default; LLM refines from narrative

    data_derived = {
        "job_type": job_type,
        "commute_style": commute_style,
        "living_arrangement": living_arrangement,
        "family_obligations": family_obligations,
        "income_stress": income_stress,
        "internet_access_patterns": internet_access_patterns,
        "social_circle_density": social_circle_density,
        "sleep_debt_baseline": sleep_debt_baseline,
        "current_life_phase": current_life_phase,
    }

    valid_options = {
        "job_type": job_type_allowed if job_type_allowed else cfg.get("job_type", {}).get("values", list(job_weights.keys())),
        "commute_style": cfg.get("commute_style", {}).get("values", ["none", "walk", "bus", "motorcycle", "car", "long_commute"]),
        "living_arrangement": cfg.get("living_arrangement", {}).get("values", ["with_family", "with_roommates", "alone", "with_partner", "unstable"]),
        "family_obligations": cfg.get("family_obligations", {}).get("values", ["none", "light", "primary_supporter", "eldercare", "childcare"]),
        "income_stress": [income_stress],  # already computed; LLM only confirms
        "internet_access_patterns": [internet_access_patterns],
        "social_circle_density": [social_circle_density],
        "sleep_debt_baseline": [sleep_debt_baseline],
        "current_life_phase": phase_values,
    }

    return data_derived, valid_options
