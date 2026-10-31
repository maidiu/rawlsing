"""
Survey routing: which data source and which countries to use for a given country_code.

Used by get_driver_vec so persona generation uses the survey that actually covers
that country (WVS, EVS, Afrobarometer, etc.) or the predefined proxy when the
country is not in any survey.

Source priority (first match wins): WVS > EVS > Afrobarometer > Arab Barometer >
Asian Barometer > Latinobarómetro. Proxy rules define (source, countries) for
countries not in any survey (e.g. Saudi Arabia → Arab Barometer, draw from Kuwait).
"""

from __future__ import annotations

from typing import Optional

# WVS Wave 7 countries (2-letter ISO)
WVS_COUNTRIES = {
    "AD", "AR", "AM", "AU", "BD", "BO", "BR", "CA", "CL", "CN", "CO", "CY", "CZ",
    "EC", "EG", "ET", "DE", "GR", "GT", "HK", "IN", "ID", "IR", "IQ", "IL", "JP", "JO",
    "KZ", "KE", "KG", "LB", "LY", "MO", "MV", "MY", "MX", "MN", "MA", "MM", "NL",
    "NZ", "NI", "NG", "PK", "PE", "PH", "PR", "RO", "RU", "RS", "SG", "SK", "KR",
    "TW", "TJ", "TH", "TN", "TR", "TT", "UA", "GB", "US", "UY", "UZ", "VE", "VN", "ZW",
}

# EVS 2017 countries NOT in WVS
EVS_ONLY_COUNTRIES = {
    "AL", "AT", "BE", "DK", "FI", "FR", "IS", "IE", "NO", "SE", "CH", "IT", "PT", "ES", "HR",
    "SI", "BY", "BG", "EE", "HU", "LV", "LT", "LU", "MT", "PL", "BA", "ME", "MK", "MD", "AZ", "GE",
}

AFROBAROMETER_COUNTRIES = {
    "DZ", "AO", "BJ", "BW", "BF", "BI", "CV", "CM", "TD", "KM", "CG", "CD", "CI", "SZ",
    "GA", "GH", "GN", "GQ", "GW", "LS", "LR", "MG", "MW", "ML", "MR", "MU", "MZ", "NA",
    "NE", "ST", "SN", "SC", "SL", "ZA", "SD", "RW", "TZ", "GM", "TG", "UG", "ZM",
}

ARAB_BAROMETER_COUNTRIES = {"KW", "PS", "SY", "YE"}

ASIAN_BAROMETER_COUNTRIES = {"KH", "NP", "LK", "LA"}

LATINOBAROMETER_COUNTRIES = {"CR", "DO", "SV", "HN", "PA", "PY"}

# Proxy: country not in any survey → (source, list of countries to draw from)
PROXY_RULES: dict[str, dict[str, list[str]]] = {
    "SA": {"source": "Arab Barometer", "countries": ["KW"]},
    "AE": {"source": "Arab Barometer", "countries": ["KW"]},
    "QA": {"source": "Arab Barometer", "countries": ["KW"]},
    "OM": {"source": "Arab Barometer", "countries": ["KW"]},
    "BH": {"source": "Arab Barometer", "countries": ["KW"]},
    "AG": {"source": "WVS", "countries": ["TT"]},
    "BB": {"source": "WVS", "countries": ["TT"]},
    "BS": {"source": "WVS", "countries": ["TT"]},
    "DM": {"source": "WVS", "countries": ["TT"]},
    "GD": {"source": "WVS", "countries": ["TT"]},
    "KN": {"source": "WVS", "countries": ["TT"]},
    "LC": {"source": "WVS", "countries": ["TT"]},
    "VC": {"source": "WVS", "countries": ["TT"]},
    "JM": {"source": "WVS", "countries": ["TT"]},
    "BZ": {"source": "Latinobarómetro", "countries": ["GT", "HN", "SV"]},
    "HT": {"source": "Latinobarómetro", "countries": ["DO"]},
    "CU": {"source": "WVS", "countries": ["VE", "NI"]},
    "GY": {"source": "WVS", "countries": ["TT", "BR"]},
    "SR": {"source": "WVS", "countries": ["BR", "VE"]},
    "AF": {"source": "WVS", "countries": ["PK", "IR"]},
    "BN": {"source": "WVS", "countries": ["MY", "ID"]},
    "BT": {"source": "Asian Barometer", "countries": ["NP", "IN"]},
    "CF": {"source": "Afrobarometer", "countries": ["CM", "CG", "CD"]},
    "DJ": {"source": "WVS", "countries": ["ET", "KE"]},
    "ER": {"source": "WVS", "countries": ["ET"]},
    "SO": {"source": "WVS", "countries": ["ET", "KE"]},
    "SS": {"source": "Afrobarometer", "countries": ["UG", "SD"]},
    "KP": {"source": "WVS", "countries": ["KR"]},
    "TM": {"source": "WVS", "countries": ["UZ", "KZ"]},
    "FJ": {"source": "WVS", "countries": ["AU", "NZ"]},
    "WS": {"source": "WVS", "countries": ["AU", "NZ"]},
    "TO": {"source": "WVS", "countries": ["AU", "NZ"]},
    "VU": {"source": "WVS", "countries": ["AU", "NZ"]},
    "SB": {"source": "WVS", "countries": ["AU", "NZ"]},
    "PG": {"source": "WVS", "countries": ["AU", "NZ", "ID"]},
    "KI": {"source": "WVS", "countries": ["AU", "NZ"]},
    "MH": {"source": "WVS", "countries": ["AU", "NZ"]},
    "NR": {"source": "WVS", "countries": ["AU", "NZ"]},
    "PW": {"source": "WVS", "countries": ["AU", "JP"]},
    "TV": {"source": "WVS", "countries": ["AU", "NZ"]},
    "LI": {"source": "EVS", "countries": ["CH", "AT"]},
    "MC": {"source": "EVS", "countries": ["FR", "IT"]},
    "SM": {"source": "EVS", "countries": ["IT"]},
    "VA": {"source": "EVS", "countries": ["IT"]},
    "XK": {"source": "EVS", "countries": ["AL", "MK", "RS"]},
    "TL": {"source": "WVS", "countries": ["ID", "AU"]},
    "AI": {"source": "WVS", "countries": ["TT", "GB"]},
    "BL": {"source": "WVS", "countries": ["TT", "GB"]},
    "KY": {"source": "WVS", "countries": ["TT", "GB"]},
    "MS": {"source": "WVS", "countries": ["TT", "GB"]},
    "TC": {"source": "WVS", "countries": ["TT", "GB"]},
    "VG": {"source": "WVS", "countries": ["TT", "GB"]},
    "MF": {"source": "WVS", "countries": ["TT", "GB"]},
    "VI": {"source": "WVS", "countries": ["US", "PR"]},
    "AW": {"source": "Latinobarómetro", "countries": ["DO", "CR"]},
    "CW": {"source": "Latinobarómetro", "countries": ["DO", "CR"]},
    "SX": {"source": "Latinobarómetro", "countries": ["DO", "CR"]},
    "GG": {"source": "EVS", "countries": ["GB", "FR"]},
    "JE": {"source": "EVS", "countries": ["GB", "FR"]},
    "IM": {"source": "EVS", "countries": ["GB"]},
    "GI": {"source": "EVS", "countries": ["ES", "GB"]},
    "FO": {"source": "EVS", "countries": ["DK", "NO"]},
    "GL": {"source": "EVS", "countries": ["DK", "NO"]},
    "BM": {"source": "WVS", "countries": ["US", "CA"]},
    "AS": {"source": "WVS", "countries": ["US", "NZ", "AU"]},
    "GU": {"source": "WVS", "countries": ["US", "JP"]},
    "MP": {"source": "WVS", "countries": ["US", "AU"]},
    "NC": {"source": "WVS", "countries": ["AU", "NZ"]},
    "PF": {"source": "WVS", "countries": ["AU", "NZ"]},
    "WF": {"source": "WVS", "countries": ["AU", "NZ"]},
    "NU": {"source": "WVS", "countries": ["AU", "NZ"]},
    "CK": {"source": "WVS", "countries": ["AU", "NZ"]},
    "TK": {"source": "WVS", "countries": ["AU", "NZ"]},
    "NF": {"source": "WVS", "countries": ["AU", "NZ"]},
    "PN": {"source": "WVS", "countries": ["AU", "NZ"]},
    "PM": {"source": "EVS", "countries": ["FR"]},
    "CX": {"source": "WVS", "countries": ["AU", "ID"]},
    "CC": {"source": "WVS", "countries": ["AU", "ID"]},
    "FK": {"source": "WVS", "countries": ["AR", "CL", "UY"]},
}

# For countries in EVS/barometers but not WVS: which WVS countries to use when
# filling drivers that the primary source doesn't have (content coverage gap).
# All values must be WVS country codes only (see WVS_COUNTRIES). Chosen by
# regime/region/colonial/geopolitical comparability; see v2/WVS_APPROXIMATION_RATIONALE.md.
WVS_APPROXIMATION_COUNTRIES: dict[str, list[str]] = {
    # EVS — WVS Europe only: DE, GR, CY, CZ, NL, RO, RU, RS, SK, UA, GB (regime/neighborhood)
    "AL": ["RS", "RO", "GR"],
    "AT": ["DE", "NL", "CZ"],
    "BE": ["NL", "DE", "GB"],
    "DK": ["NL", "DE", "GB"],
    "FI": ["NL", "DE", "GB"],
    "FR": ["DE", "NL", "GB"],
    "IS": ["NL", "GB", "DE"],
    "IE": ["GB", "NL", "DE"],
    "NO": ["NL", "DE", "GB"],
    "SE": ["NL", "DE", "GB"],
    "CH": ["DE", "NL", "CZ"],
    "IT": ["DE", "GR", "NL"],
    "PT": ["UY", "AR", "CO"],
    "ES": ["AR", "UY", "CO"],
    "HR": ["RS", "SK", "CZ"],
    "SI": ["SK", "CZ", "RS"],
    "BY": ["RU", "UA", "SK"],
    "BG": ["RO", "GR", "RS"],
    "EE": ["RU", "UA", "RO"],
    "HU": ["SK", "CZ", "RO"],
    "LV": ["RU", "UA", "RO"],
    "LT": ["RU", "UA", "RO"],
    "LU": ["NL", "DE", "GB"],
    "MT": ["CY", "GR", "DE"],
    "PL": ["SK", "CZ", "RO"],
    "BA": ["RS", "RO", "GR"],
    "ME": ["RS", "RO", "GR"],
    "MK": ["RS", "RO", "GR"],
    "MD": ["RO", "UA", "RS"],
    "AZ": ["AM", "TR", "RU"],
    "GE": ["AM", "TR", "RU"],
    # Arab Barometer — WVS MENA / structurally close
    "KW": ["JO", "EG", "TN"],
    "PS": ["JO", "LB", "EG"],
    "SY": ["JO", "LB", "IQ"],
    "YE": ["JO", "EG", "IQ"],
    # Afrobarometer — WVS Africa only: ET, EG, KE, MA, NG, TN, ZW, LY (region/colonial/regime)
    "DZ": ["TN", "MA", "EG"],
    "AO": ["ZW", "NG", "KE"],
    "BJ": ["NG", "KE", "ET"],
    "BW": ["ZW", "NG", "KE"],
    "BF": ["NG", "KE", "ET"],
    "BI": ["KE", "ET", "ZW"],
    "CV": ["NG", "TN", "MA"],
    "CM": ["NG", "KE", "ZW"],
    "TD": ["NG", "ET", "EG"],
    "KM": ["KE", "ZW", "ET"],
    "CG": ["NG", "ZW", "KE"],
    "CD": ["ZW", "KE", "ET"],
    "CI": ["NG", "KE", "ET"],
    "SZ": ["ZW", "NG", "KE"],
    "GA": ["NG", "ZW", "KE"],
    "GH": ["NG", "KE", "ET"],
    "GN": ["NG", "TN", "MA"],
    "GQ": ["NG", "ZW", "KE"],
    "GW": ["NG", "TN", "MA"],
    "LS": ["ZW", "NG", "KE"],
    "LR": ["NG", "KE", "ET"],
    "MG": ["KE", "ZW", "ET"],
    "MW": ["ZW", "KE", "ET"],
    "ML": ["NG", "TN", "MA"],
    "MR": ["EG", "TN", "MA"],
    "MU": ["ZW", "IN", "GB"],
    "MZ": ["ZW", "KE", "ET"],
    "NA": ["ZW", "NG", "KE"],
    "NE": ["NG", "TN", "MA"],
    "ST": ["NG", "TN", "MA"],
    "SN": ["NG", "TN", "MA"],
    "SC": ["KE", "ZW", "ET"],
    "SL": ["NG", "KE", "ET"],
    "ZA": ["ZW", "NG", "KE"],
    "SD": ["EG", "ET", "KE"],
    "RW": ["KE", "ET", "ZW"],
    "TZ": ["KE", "ET", "ZW"],
    "GM": ["NG", "TN", "MA"],
    "TG": ["NG", "KE", "ET"],
    "UG": ["KE", "ET", "ZW"],
    "ZM": ["ZW", "KE", "ET"],
    # Asian Barometer — WVS East/South Asia
    "KH": ["TH", "VN", "ID"],
    "NP": ["IN", "BD"],
    "LK": ["IN", "BD"],
    "LA": ["TH", "VN"],
    # Latinobarómetro — WVS Americas
    "CR": ["CO", "MX", "GT"],
    "DO": ["PR", "TT", "CO"],
    "SV": ["GT", "MX", "CO"],
    "HN": ["GT", "MX", "CO"],
    "PA": ["CO", "MX", "GT"],
    "PY": ["AR", "BR", "UY"],
}


def _validate_wvs_approximation() -> None:
    """Ensure every value in WVS_APPROXIMATION_COUNTRIES is a WVS country code."""
    bad = [
        (country, c)
        for country, codes in WVS_APPROXIMATION_COUNTRIES.items()
        for c in codes
        if c not in WVS_COUNTRIES
    ]
    if bad:
        raise ValueError(
            "WVS_APPROXIMATION_COUNTRIES must contain only WVS country codes; invalid: " + str(bad)
        )


def survey_for(country_code: str) -> Optional[dict]:
    """
    Return survey routing for this country.
    
    Returns:
        {"source": "WVS"|"EVS"|"Afrobarometer"|..., "countries": [iso2, ...]}
        - Direct: country is in that source → countries = [country_code]
        - Proxy: country not in any survey → countries = list of similar countries to draw from
        None if country not in any set and not in PROXY_RULES (caller can fall back to aggregate priority).
    """
    code = (country_code or "").strip().upper()
    if not code or len(code) != 2:
        return None
    if code in WVS_COUNTRIES:
        return {"source": "WVS", "countries": [code]}
    if code in EVS_ONLY_COUNTRIES:
        return {"source": "EVS", "countries": [code]}
    if code in AFROBAROMETER_COUNTRIES:
        return {"source": "Afrobarometer", "countries": [code]}
    if code in ARAB_BAROMETER_COUNTRIES:
        return {"source": "Arab Barometer", "countries": [code]}
    if code in ASIAN_BAROMETER_COUNTRIES:
        return {"source": "Asian Barometer", "countries": [code]}
    if code in LATINOBAROMETER_COUNTRIES:
        return {"source": "Latinobarómetro", "countries": [code]}
    if code in PROXY_RULES:
        return PROXY_RULES[code].copy()
    return None


def wvs_approximation_countries_for(country_code: str) -> list[str]:
    """
    Return list of WVS country codes to use when filling drivers missing in the primary source.
    Used when primary source is EVS/barometer and some drivers have no items there.
    """
    code = (country_code or "").strip().upper()
    return WVS_APPROXIMATION_COUNTRIES.get(code, [])
