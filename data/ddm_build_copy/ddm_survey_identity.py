#!/usr/bin/env python3
"""Canonical survey identity helpers shared by V550+.

The execution contract is intentionally small and fail-closed:

* a survey family and wave are always explicit;
* aliases normalize to one stable family key;
* wave labels remain labels (``II``, ``W6``, ``ROUND9``, ``2017``);
* an ordinal is derived only for registry range matching;
* country is never silently replaced with ``US``.

These helpers contain no survey-specific semantic rules.  Family-specific
adapters may normalize naming, but they may not create authority.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Any


class SurveyIdentityError(ValueError):
    """Raised when a required source/wave/country identity is unresolved."""


def _ascii_text(value: Any) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def _token(value: Any) -> str:
    text = _ascii_text(value).lower().strip()
    if text in {"", "nan", "none", "null", "unknown", "unresolved"}:
        return ""
    return re.sub(r"[^a-z0-9]+", "_", text).strip("_")


FAMILY_ALIASES = {
    "gss": "gss",
    "general_social_survey": "gss",
    "wvs": "wvs",
    "world_values_survey": "wvs",
    "evs": "evs",
    "european_values_study": "evs",
    "afrobarometer": "afrobarometer",
    "afro_barometer": "afrobarometer",
    "arabbarometer": "arab_barometer",
    "arab_barometer": "arab_barometer",
    "asianbarometer": "asian_barometer",
    "asian_barometer": "asian_barometer",
    "asian_barometer_survey": "asian_barometer",
    "latinobarometer": "latinobarometro",
    "latinobar_metro": "latinobarometro",
    "latinobarometro": "latinobarometro",
    "lits": "lits",
    "life_in_transition_survey": "lits",
    "southasia": "south_asia",
    "south_asia": "south_asia",
    "south_asia_barometer": "south_asia",
}

FAMILY_LABELS = {
    "gss": "GSS",
    "wvs": "WVS",
    "evs": "EVS",
    "afrobarometer": "Afrobarometer",
    "arab_barometer": "Arab Barometer",
    "asian_barometer": "Asian Barometer",
    "latinobarometro": "Latinobarómetro",
    "lits": "LiTS",
    "south_asia": "South Asia",
}

ARAB_ROMAN_BY_NUMBER = {
    "1": "I",
    "2": "II",
    "3": "III",
    "4": "IV",
    "5": "V",
    "6": "VI",
    "7": "VII",
    "8": "VIII",
    "9": "IX",
    "10": "X",
    "11": "XI",
    "12": "XII",
}
EVS_WAVE_BY_YEAR = {"1981": "W1", "1990": "W2", "1999": "W3", "2008": "W4", "2017": "W5"}
EVS_YEAR_BY_WAVE = {wave: year for year, wave in EVS_WAVE_BY_YEAR.items()}

_ROMAN_VALUES = {
    "I": 1,
    "II": 2,
    "III": 3,
    "IV": 4,
    "V": 5,
    "VI": 6,
    "VII": 7,
    "VIII": 8,
    "IX": 9,
    "X": 10,
    "XI": 11,
    "XII": 12,
}


def canonical_family_key(value: Any) -> str:
    token = _token(value)
    return FAMILY_ALIASES.get(token, token)


def canonical_family_label(value: Any) -> str:
    key = canonical_family_key(value)
    return FAMILY_LABELS.get(key, str(value or "").strip())


def family_keys_equal(left: Any, right: Any) -> bool:
    left_key = canonical_family_key(left)
    return bool(left_key) and left_key == canonical_family_key(right)


def canonical_wave_key(survey_family: Any, value: Any) -> str:
    family = canonical_family_key(survey_family)
    raw = str(value or "").strip()
    if not raw:
        return ""
    compact = re.sub(r"[^A-Za-z0-9]+", "", raw).upper()

    if family == "arab_barometer":
        number = ""
        if compact.startswith("WAVE"):
            number = compact[4:]
        elif compact.startswith("W") and compact[1:].isdigit():
            number = compact[1:]
        elif compact.isdigit():
            number = compact
        elif compact in _ROMAN_VALUES:
            return compact
        if number in ARAB_ROMAN_BY_NUMBER:
            return ARAB_ROMAN_BY_NUMBER[number]

    if family == "evs":
        if compact in EVS_WAVE_BY_YEAR:
            return EVS_WAVE_BY_YEAR[compact]
        if compact in EVS_YEAR_BY_WAVE:
            return compact
        if compact.startswith("WAVE") and compact[4:].isdigit():
            return f"W{compact[4:]}"

    if compact.startswith("ROUND") and compact[5:].isdigit():
        return f"ROUND{int(compact[5:])}"
    if compact.startswith("R") and compact[1:].isdigit():
        return f"ROUND{int(compact[1:])}"
    if compact.startswith("WAVE") and compact[4:].isdigit():
        return f"W{int(compact[4:])}"
    if compact.startswith("W") and compact[1:].isdigit():
        return f"W{int(compact[1:])}"
    return compact


def wave_aliases(survey_family: Any, value: Any) -> list[str]:
    family = canonical_family_key(survey_family)
    canonical = canonical_wave_key(family, value)
    if not canonical:
        return []
    aliases: list[str] = [canonical]
    if family == "arab_barometer":
        reverse = {roman: number for number, roman in ARAB_ROMAN_BY_NUMBER.items()}
        number = reverse.get(canonical)
        if number:
            aliases.extend([f"W{number}", number, f"WAVE{number}"])
    elif family == "evs":
        year = EVS_YEAR_BY_WAVE.get(canonical)
        if year:
            aliases.extend([year, canonical.replace("W", "Wave ")])
    elif canonical.startswith("ROUND"):
        number = canonical[5:]
        aliases.extend([f"R{number}", number, f"Round {number}"])
    elif canonical.startswith("W") and canonical[1:].isdigit():
        number = canonical[1:]
        aliases.extend([number, f"Wave {number}"])
    elif canonical in _ROMAN_VALUES:
        aliases.append(str(_ROMAN_VALUES[canonical]))
    else:
        aliases.append(str(value or "").strip())

    out: list[str] = []
    seen: set[str] = set()
    for alias in aliases:
        token = str(alias).strip()
        if token and token.upper() not in seen:
            seen.add(token.upper())
            out.append(token)
    return out


def waves_equivalent(survey_family: Any, left: Any, right: Any) -> bool:
    left_key = canonical_wave_key(survey_family, left)
    right_key = canonical_wave_key(survey_family, right)
    return bool(left_key) and left_key == right_key


def wave_ordinal(survey_family: Any, value: Any) -> int | None:
    """Return a range-comparison ordinal without changing the canonical label."""
    canonical = canonical_wave_key(survey_family, value)
    if not canonical:
        return None
    if canonical.isdigit():
        return int(canonical)
    if canonical.startswith("ROUND") and canonical[5:].isdigit():
        return int(canonical[5:])
    if canonical.startswith("W") and canonical[1:].isdigit():
        return int(canonical[1:])
    return _ROMAN_VALUES.get(canonical)


def canonical_country_code(value: Any) -> str:
    """Normalize an explicit country token without guessing its country."""
    text = str(value or "").strip().upper()
    if text in {"", "NAN", "NONE", "NULL", "UNKNOWN", "UNRESOLVED"}:
        return ""
    return text


@dataclass(frozen=True)
class SurveyIdentity:
    source: str
    source_key: str
    canonical_wave: str
    country_code: str = ""


def require_survey_identity(
    source: Any,
    wave: Any,
    country_code: Any = "",
    *,
    require_country: bool = False,
) -> SurveyIdentity:
    source_key = canonical_family_key(source)
    canonical_wave = canonical_wave_key(source_key, wave)
    country = canonical_country_code(country_code)
    missing: list[str] = []
    if not source_key:
        missing.append("source")
    if not canonical_wave:
        missing.append("wave")
    if require_country and not country:
        missing.append("country_code")
    if missing:
        raise SurveyIdentityError(
            "required survey identity unresolved: " + ", ".join(missing)
        )
    return SurveyIdentity(
        source=canonical_family_label(source),
        source_key=source_key,
        canonical_wave=canonical_wave,
        country_code=country,
    )
