# v3/io/identity_from_v2.py
# Wire v2 probabilistic identity generator (generate_identity_context) into v3.
# Optional: requires v2 and DB; returns None if unavailable.
# Pipeline: country (random from WVS pool if not given) → generate_identity_context → region → ethnicity → SES → religion/language.

from __future__ import annotations

import random
from typing import Any


def sample_country_from_wvs_pool() -> str | None:
    """
    Population-weighted country selection from WVS/barometer survey pool.

    Weights by approximate real-world population so large countries (India, China,
    USA, Indonesia, Brazil, Nigeria, Bangladesh, ...) are proportionally more likely
    than small ones (Cyprus, Andorra, Maldives, Macao, ...).

    Falls back to uniform random.choice if weights unavailable.
    """
    try:
        from v2.data_access import list_survey_countries
    except ImportError:
        return None
    countries = list_survey_countries()
    if not countries:
        return None
    countries = [c for c in countries if str(c or "").strip().upper() != "NIR"]

    # Approximate populations (millions) for every country in the WVS/barometer pool.
    # Unknown countries default to 20M (mid-sized) so they stay in the draw.
    _POP_M: dict[str, float] = {
        "AND": 0.08,   "ARG": 46,    "ARM": 3,     "AUS": 26,
        "BGD": 173,    "BOL": 12,    "BRA": 215,   "CAN": 38,
        "CHL": 19,     "CHN": 1412,  "COL": 52,    "CYP": 1.2,
        "CZE": 11,     "DEU": 84,    "ECU": 18,    "EGY": 105,
        "ETH": 126,    "GBR": 68,    "GRC": 11,    "GTM": 17,
        "HKG": 7.5,    "IDN": 277,   "IND": 1428,  "IRN": 87,
        "IRQ": 42,     "JOR": 10,    "JPN": 125,   "KAZ": 19,
        "KEN": 55,     "KGZ": 7,     "KOR": 52,    "LBN": 5,
        "LBY": 7,      "MAC": 0.7,   "MAR": 37,    "MDV": 0.5,
        "MEX": 128,    "MMR": 54,    "MNG": 3.4,   "MYS": 33,
        "NGA": 220,    "NIC": 7,     "NLD": 17,
        "NZL": 5,      "PAK": 231,   "PER": 33,    "PHL": 115,
        "PRI": 3.2,    "ROU": 19,    "RUS": 144,   "SGP": 5.9,
        "SRB": 7,      "SVK": 5.5,   "THA": 71,    "TJK": 10,
        "TUN": 12,     "TUR": 85,    "TWN": 23,    "UKR": 44,
        "URY": 3.5,    "USA": 335,   "UZB": 36,    "VEN": 29,
        "VNM": 98,     "ZWE": 16,
    }

    # Square-root weighting: biases toward populous countries without making
    # India/China (44% of world) dominate. China ~6%, Cyprus ~0.2%, Andorra ~0.05%.
    import math
    weights = [math.sqrt(_POP_M.get(c, 20.0)) for c in countries]
    return random.choices(countries, weights=weights, k=1)[0]


def identity_skeleton_to_dict(skeleton: Any) -> dict[str, Any]:
    """
    Convert v2 IdentitySkeleton (or similar) to dict for backbone_state_from_identity and persona_sheet.
    """
    out: dict[str, Any] = {}
    for key in (
        "given_name", "family_name", "gender", "birth_year", "anchor_year", "age_at_anchor",
        "country_code", "region", "locality", "urbanicity",
        "class_origin", "current_class", "ethnicity_label", "minority_status",
        "childhood_religion", "current_religion", "religiosity_level",
        "primary_language", "secondary_languages",
        "parent_expectation_baseline", "transmission_regime",
    ):
        if hasattr(skeleton, key):
            v = getattr(skeleton, key)
            if v is not None:
                out[key] = v
    # Alias for persona_sheet / run_conversation_chat (identity.religion, identity.ethnicity)
    if "country_code" in out and "country" not in out:
        out["country"] = out["country_code"]
    if "current_class" in out and "ses_band" not in out:
        out["ses_band"] = out["current_class"].replace("_", " ")
    if "primary_language" in out:
        out["languages"] = [out["primary_language"]] + list(out.get("secondary_languages") or [])
    if "religion" not in out:
        out["religion"] = out.get("current_religion") or out.get("childhood_religion") or ""
    if "ethnicity" not in out:
        out["ethnicity"] = out.get("ethnicity_label") or ""
    if "urbanicity" in out and "urban_rural" not in out:
        out["urban_rural"] = out["urbanicity"]
    return out


def identity_from_data_layer(
    country_code: str | None,
    year: int,
    age: int,
    gender: str | None = None,
) -> dict[str, Any] | None:
    """
    Call v2 generate_identity_context(country_code, year, age, gender); return identity as dict
    for v3 backbone_state_from_identity and persona_sheet. Returns None if v2/DB unavailable.
    If country_code is None, samples a random country from list_survey_countries() (WVS + EVS + barometers; full pipeline:
    country → region → ethnicity → SES → religion/language).
    """
    if country_code is None or not str(country_code).strip():
        country_code = sample_country_from_wvs_pool()
    if not country_code:
        return None
    try:
        from v2.country_reference import require_country_ref
        from v2.identity_generator import generate_identity_context
    except ImportError:
        return None
    country_ref = require_country_ref(country_code)
    country_code = country_ref.get("iso3") or country_ref.get("iso2") or str(country_code).strip().upper()
    identity_sk, context = generate_identity_context(
        country_code=country_code,
        year=year,
        age=age,
        gender=gender,
    )
    result = identity_skeleton_to_dict(identity_sk)
    result["_source_provenance"] = {
        "ethnic": (context.get("ethnic") or {}).get("_provenance", {}),
        "religion_language": context.get("_rel_lang_provenance", {}),
        "location": (context.get("location") or {}).get("_provenance", {}),
    }
    return result


# Alias for run_and_print / callers that expect this name
identity_dict_from_v2_generator = identity_from_data_layer
