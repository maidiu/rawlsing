# v3/io/calibration_from_identity.py
# Populate state.calibration_regime, state.boundary_map, state.strata_stack from identity (and optional world_slice).
# Spec §5: "per nation/sect_class/school/work". No hard v2 dependency; callers may pass world_slice dict.

from __future__ import annotations

from typing import Any

from v3.core.state import (
    BoundaryMapEntry,
    CalibrationRegime,
    Stratum,
)
from v3.core.enums import DOMAIN_NAMES


# Lookup tables for 9-strata stack
_IMPERIAL_BLOC_MAP = {
    "US": "us_led_core", "GB": "us_led_core", "CA": "us_led_core", "AU": "us_led_core", "NZ": "us_led_core",
    "DE": "eu_core", "FR": "eu_core", "IT": "eu_core", "ES": "eu_core", "NL": "eu_core",
    "CN": "sino_sphere", "RU": "eurasian_periphery", "IN": "non_aligned_major",
    "BR": "non_aligned_major", "ZA": "non_aligned_major", "ID": "southeast_asian",
    "JP": "us_led_core", "KR": "us_led_core", "IR": "resistance_axis",
    "SA": "gulf_monarchy", "AE": "gulf_monarchy", "QA": "gulf_monarchy",
    "NG": "african_periphery", "KE": "african_periphery", "ET": "african_periphery",
    "EG": "mena_periphery", "PK": "south_asian_periphery", "BD": "south_asian_periphery",
    "MX": "latin_american_periphery", "AR": "latin_american_periphery", "CO": "latin_american_periphery",
    "IL": "us_led_core", "TR": "mena_periphery", "UA": "eastern_european",
    "VN": "southeast_asian", "TH": "southeast_asian", "PH": "southeast_asian",
    "MM": "southeast_asian", "MY": "southeast_asian", "SG": "southeast_asian",
}

_PLANETARY_RELATION = {
    "US": "exploiter", "GB": "exploiter", "FR": "exploiter", "DE": "exploiter",
    "CN": "exploiter", "RU": "exploiter", "JP": "exploiter", "KR": "exploiter",
    "IN": "intermediary", "BR": "intermediary", "ZA": "intermediary",
    "CD": "exploited", "ET": "exploited", "HT": "exploited", "YE": "exploited",
    "AF": "exploited", "SO": "exploited", "SD": "exploited", "MM": "exploited",
}

_NATION_RELATION = {
    "underclass": "exploited", "working": "exploited",
    "lower_middle": "buffer", "middle": "intermediary",
    "upper_middle": "exploiter", "elite": "exploiter",
}

_NATION_PROVISION = {
    "underclass": 15.0, "working": 30.0, "lower_middle": 50.0,
    "middle": 65.0, "upper_middle": 80.0, "elite": 90.0,
}

_NEIGHBORHOOD_PROVISION = {
    "rural": 35.0, "town": 45.0, "city": 55.0, "megacity": 50.0,
}

_FAMILY_PROVISION = {
    "underclass": 40.0, "working": 50.0, "lower_middle": 55.0,
    "middle": 65.0, "upper_middle": 75.0, "elite": 85.0,
}


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _clamp100(v: float) -> float:
    return max(0.0, min(100.0, float(v)))


def build_calibration_regime(
    identity: dict[str, Any] | Any,
    world_slice: dict[str, Any] | None = None,
) -> CalibrationRegime:
    """
    Build CalibrationRegime from identity (class, minority_status, region) and optional world_slice.
    norm_center: from class (underclass→marginal, middle→middle, elite→elite).
    uniqueness_norm: 0–100; higher for minoritized/urban; lower for dominant/rural.
    dream_window: empty unless identity or world_slice provides it.
    outlier_penalties/incentives: from repression/legitimacy when world_slice present.
    """
    class_ = (
        (str(_get(identity, "class_origin") or _get(identity, "current_class") or "middle"))
        .replace(" ", "_")
        .lower()
    )
    minority = (str(_get(identity, "minority_status") or "dominant")).lower()
    urbanicity = (str(_get(identity, "urbanicity") or "city")).lower()

    # norm_center: class-based
    if class_ in ("underclass", "working"):
        norm_center = "marginal"
    elif class_ in ("upper_middle", "elite"):
        norm_center = "elite"
    else:
        norm_center = "middle"

    # uniqueness_norm: minoritized/urban → higher expectation to be "special"; dominant/rural → more conform
    uniqueness_norm = 50.0
    if minority in ("minoritized", "mixed"):
        uniqueness_norm += 10.0
    if urbanicity in ("city", "megacity"):
        uniqueness_norm += 5.0
    if minority == "dominant" and urbanicity == "rural":
        uniqueness_norm -= 5.0
    uniqueness_norm = _clamp100(uniqueness_norm)

    dream_window = str(_get(identity, "dream_window") or "")[:500]
    outlier_penalties: list[dict[str, Any]] = []
    outlier_incentives: list[dict[str, Any]] = []

    if isinstance(world_slice, dict):
        rep = world_slice.get("state_repression")
        if rep is not None and float(rep) > 60:
            outlier_penalties.append({"topic": "political dissent", "strength": 70})
            outlier_penalties.append({"topic": "public criticism of state", "strength": 60})
        leg = world_slice.get("legitimacy") or world_slice.get("trust_institutions")
        if leg is not None and float(leg) < 40:
            outlier_incentives.append({"topic": "conformity to local norms", "strength": 50})

    return CalibrationRegime(
        norm_center=norm_center[:200],
        uniqueness_norm=uniqueness_norm,
        outlier_penalties=outlier_penalties[:20],
        outlier_incentives=outlier_incentives[:20],
        dream_window=dream_window,
    )


def build_boundary_map(
    identity: dict[str, Any] | Any,
    domain_names: tuple[str, ...] = DOMAIN_NAMES,
    world_slice: dict[str, Any] | None = None,
) -> dict[str, BoundaryMapEntry]:
    """
    Build one BoundaryMapEntry per domain. Position labels: conform, partial, defy, withdraw.
    High repression → discourage "defy"; low legitimacy → incentivize "conform".
    """
    rep = 50.0
    if isinstance(world_slice, dict):
        r = world_slice.get("state_repression")
        if r is not None:
            rep = _clamp100(float(r))
    high_repression = rep > 55

    permitted = ["conform", "partial"]
    discouraged: list[str] = []
    incentivized = ["conform"]
    if high_repression:
        discouraged.append("defy")
        permitted = [p for p in permitted if p != "defy"]
    else:
        permitted.append("defy")

    result: dict[str, BoundaryMapEntry] = {}
    for name in domain_names:
        result[name] = BoundaryMapEntry(
            discouraged=list(discouraged)[:20],
            permitted=list(permitted)[:20],
            incentivized=list(incentivized)[:20],
            trigger_conditions=[],
        )
    return result


def build_strata_stack(
    identity: dict[str, Any] | Any,
    field_raw: dict[str, Any] | None = None,
) -> list[Stratum]:
    """
    Build strata stack: planetary → nation → sect_class → family (spec: provision, coercion, contradiction, visibility, salience).
    field_raw (e.g. state.field.raw) can drive coercion/provision/contradiction per level.
    """
    # Build 9-strata stack (v5: 0=planetary through 8=self)
    country_code = _get(identity, "country_code") or _get(identity, "country") or "US"
    country = str(country_code).strip().upper()[:3]
    current_class = _get(identity, "class_origin") or _get(identity, "current_class") or "middle"
    ses = str(current_class).strip().lower()
    minority_raw = str(_get(identity, "minority_status") or "dominant").strip().lower()
    imper_bloc = _IMPERIAL_BLOC_MAP.get(country, "global_periphery")

    strata_stack: list[Stratum] = []

    # Level 0: planetary
    strata_stack.append(Stratum(level=0, name="planetary",
        description="Global extraction order",
        material_relation=_PLANETARY_RELATION.get(country, "intermediary"),
        hegemonic_story="The global economy is natural; some nations lead, others follow; development is linear progress.",
        loyalty_demand="Accept the global order as given; aspiration is individual, not structural.",
        provision_strength=50.0, coercion_strength=30.0, contradiction_load=40.0))
    # Level 1: imperial_block
    strata_stack.append(Stratum(level=1, name="imperial_block",
        description=imper_bloc,
        material_relation="intermediary" if imper_bloc in ("us_led_core",) else "exploited",
        hegemonic_story="We are part of the [bloc]; our security and prosperity depend on bloc membership.",
        loyalty_demand="Align with bloc interests; do not question bloc foreign policy.",
        provision_strength=60.0 if imper_bloc in ("us_led_core",) else 30.0,
        coercion_strength=20.0 if imper_bloc in ("us_led_core",) else 50.0,
        contradiction_load=30.0))
    # Level 2: nation_state
    strata_stack.append(Stratum(level=2, name="nation_state",
        description=country,
        material_relation=_NATION_RELATION.get(ses, "intermediary"),
        hegemonic_story="The nation protects its citizens; laws are fair; hard work is rewarded.",
        loyalty_demand="Obey the law; pay taxes; serve if called; do not question the nation's legitimacy.",
        provision_strength=_NATION_PROVISION.get(ses, 50.0),
        coercion_strength=15.0 if "dominant" in minority_raw else 40.0,
        contradiction_load=25.0 if "dominant" in minority_raw else 55.0))
    # Level 3: sub_national_region
    region_name = str(_get(identity, "region") or "").strip()
    strata_stack.append(Stratum(level=3, name="sub_national_region",
        description=region_name or "local region",
        material_relation="intermediary",
        hegemonic_story="This is how things are done here; our community has its own way.",
        loyalty_demand="Participate in local norms; don't stand out too much.",
        provision_strength=50.0, coercion_strength=20.0, contradiction_load=20.0))
    # Level 4: sect_ethno_class
    strata_stack.append(Stratum(level=4, name="sect_ethno_class",
        description=f"{_get(identity, 'ethnicity_label') or _get(identity, 'ethnicity') or ''} {ses}",
        material_relation="intermediary" if "dominant" in minority_raw else "exploited",
        hegemonic_story="People like us succeed through [merit/family/faith]; others have different paths.",
        loyalty_demand="Stay within community norms; don't betray your people.",
        provision_strength=70.0 if "dominant" in minority_raw else 40.0,
        coercion_strength=10.0 if "dominant" in minority_raw else 35.0,
        contradiction_load=15.0 if "dominant" in minority_raw else 50.0))
    # Level 5: party_movement
    strata_stack.append(Stratum(level=5, name="party_movement",
        description="civic/religious participation",
        material_relation="intermediary",
        hegemonic_story="Participation gives voice; institutions carry tradition and continuity.",
        loyalty_demand="Show up; contribute; don't undermine from within.",
        provision_strength=40.0, coercion_strength=15.0, contradiction_load=20.0))
    # Level 6: neighborhood_household
    strata_stack.append(Stratum(level=6, name="neighborhood_household",
        description=_get(identity, "locality") or region_name or "neighborhood",
        material_relation="intermediary",
        hegemonic_story="This is home; neighbors look out for each other; keep things orderly.",
        loyalty_demand="Be a good neighbor; maintain the property; don't cause trouble.",
        provision_strength=_NEIGHBORHOOD_PROVISION.get(str(_get(identity, "urbanicity") or "city").lower(), 50.0),
        coercion_strength=10.0, contradiction_load=15.0))
    # Level 7: family
    strata_stack.append(Stratum(level=7, name="family",
        description="family of origin",
        material_relation="intermediary",
        hegemonic_story="Family is your foundation; blood is thicker than water; we take care of our own.",
        loyalty_demand="Honor your parents; support your siblings; marry within the community.",
        provision_strength=_FAMILY_PROVISION.get(ses, 60.0),
        coercion_strength=25.0, contradiction_load=30.0))
    # Level 8: self
    strata_stack.append(Stratum(level=8, name="self",
        description=f"age {_get(identity, 'age') or 0}, {_get(identity, 'gender') or 'person'}",
        material_relation="intermediary",
        hegemonic_story="I am who I am; my worth comes from my actions and character.",
        loyalty_demand="Be true to yourself; don't betray your own values.",
        provision_strength=50.0, coercion_strength=10.0, contradiction_load=40.0))

    for s in strata_stack:
        s.clamp_all()
    return strata_stack


def build_strata_salience_from_stack(strata_stack: list[Stratum]) -> dict[str, Any]:
    """
    Build state.strata_salience from strata_stack for state_summary (llm_contract expects
    level -> {level, name, coercion, provision, contradiction}).
    """
    out: dict[str, Any] = {}
    for s in strata_stack:
        key = str(s.level)
        out[key] = s.to_salient_dict()
    return out


def apply_calibration_to_state(
    state: Any,
    identity: dict[str, Any] | Any,
    world_slice: dict[str, Any] | None = None,
    relational_field: dict[str, Any] | None = None,
) -> None:
    """
    Populate state.calibration_regime, state.boundary_map, state.strata_stack, state.strata_salience
    from identity and optional world_slice. Mutates state in place.
    """
    state.calibration_regime = build_calibration_regime(identity, world_slice)
    state.boundary_map = build_boundary_map(identity, DOMAIN_NAMES, world_slice)
    state.strata_stack = build_strata_stack(identity, getattr(state.field, "raw", None) or {})
    state.strata_salience = build_strata_salience_from_stack(state.strata_stack)
    if relational_field is not None:
        try:
            from v3.systems.relational_field import apply_relational_field_to_state

            apply_relational_field_to_state(state, relational_field)
        except Exception as _rel_exc:
            state.generation_diagnostics.append({
                "stage": "v5_relational_field",
                "status": "degraded",
                "exception_type": _rel_exc.__class__.__name__,
                "exception_message": str(_rel_exc)[:200],
                "fallback_behavior": "relational_field_skipped",
                "fields_impacted": ["strata_salience"],
                "chat_surface_impact": "none",
            })
    if not state.strata_stack:
        state.generation_diagnostics.append({
            "stage": "v5_strata_stack",
            "status": "blocked",
            "fallback_used": True,
            "fallback_reason": "strata_stack_missing_or_empty",
            "fields_impacted": ["strata_stack", "strata_salience"],
            "exception_type": None,
            "exception_message": "",
        })
