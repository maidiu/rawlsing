#!/usr/bin/env python3
"""Canonical survey identity compatibility helpers shared by V550+.

Governed source/wave identity, stable UIDs, and production membership live in
``ddm_source_wave_identity``.  This module preserves the historical key/label
surface used by existing joins, paths, and hashes.  Compatibility normalization
is not production authorization.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from data.ddm_build_copy.ddm_source_wave_identity import (
    compatibility_family_key,
    compatibility_family_label,
    compatibility_wave_aliases,
    compatibility_wave_key,
    compatibility_wave_ordinal,
)


class SurveyIdentityError(ValueError):
    """Raised when a required source/wave/country identity is unresolved."""


def canonical_family_key(value: Any) -> str:
    return compatibility_family_key(value)


def canonical_family_label(value: Any) -> str:
    return compatibility_family_label(value)


def family_keys_equal(left: Any, right: Any) -> bool:
    left_key = canonical_family_key(left)
    return bool(left_key) and left_key == canonical_family_key(right)


def canonical_wave_key(survey_family: Any, value: Any) -> str:
    return compatibility_wave_key(survey_family, value)


def wave_aliases(survey_family: Any, value: Any) -> list[str]:
    return compatibility_wave_aliases(survey_family, value)


def waves_equivalent(survey_family: Any, left: Any, right: Any) -> bool:
    left_key = canonical_wave_key(survey_family, left)
    right_key = canonical_wave_key(survey_family, right)
    return bool(left_key) and left_key == right_key


def wave_ordinal(survey_family: Any, value: Any) -> int | None:
    """Return a range-comparison ordinal without changing the canonical label."""
    return compatibility_wave_ordinal(survey_family, value)


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
