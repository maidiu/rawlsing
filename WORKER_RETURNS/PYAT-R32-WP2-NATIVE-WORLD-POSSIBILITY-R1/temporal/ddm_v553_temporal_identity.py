#!/usr/bin/env python3
"""Pure identity and calendar-anchor validation for V553 temporal input.

This module deliberately has no parquet/Arrow dependency, so identity
validation can run before any heavyweight temporal compiler is imported.
"""
from __future__ import annotations

import math
from typing import Any

from data.ddm_build_copy.ddm_survey_identity import (
    SurveyIdentityError,
    canonical_country_code,
    canonical_family_key,
    canonical_family_label,
    require_survey_identity,
)


def _clean(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and math.isnan(value):
        return ""
    text = str(value).strip()
    return "" if text.lower() in {"nan", "none", "null"} else text


def _explicit_temporal_year(
    row: dict[str, Any],
    canonical_wave: str,
) -> int | None:
    """Resolve a real calendar anchor without treating a wave ordinal as a year."""
    for key in (
        "temporal_year",
        "fieldwork_year",
        "survey_year",
        "year",
    ):
        text = _clean(row.get(key))
        if text.isdigit() and 1000 <= int(text) <= 3000:
            return int(text)
    if canonical_wave.isdigit() and 1000 <= int(canonical_wave) <= 3000:
        return int(canonical_wave)
    return None


def normalize_temporal_report_identity(
    report: dict[str, Any],
    *,
    explicit_country_code: str = "",
) -> dict[str, Any]:
    """Return one-source, one-country, calendar-anchored temporal input."""
    wave_rows = report.get("wave_rows", [])
    if not isinstance(wave_rows, list) or not wave_rows:
        raise SurveyIdentityError(
            "V553 temporal input has no explicit wave rows"
        )

    source_values = [
        _clean(report.get("source") or report.get("source_family")),
        *[
            _clean(row.get("source") or row.get("source_family"))
            for row in wave_rows
            if isinstance(row, dict)
        ],
    ]
    source_keys = {
        canonical_family_key(value)
        for value in source_values
        if canonical_family_key(value)
    }
    if len(source_keys) != 1:
        raise SurveyIdentityError(
            "V553 temporal input requires exactly one explicit survey family; "
            f"found {sorted(source_keys)}"
        )
    source_key = next(iter(source_keys))
    source = canonical_family_label(source_key)

    country_values = [
        canonical_country_code(explicit_country_code),
        canonical_country_code(
            report.get("country_code") or report.get("country")
        ),
        *[
            canonical_country_code(
                row.get("country_code") or row.get("country")
            )
            for row in wave_rows
            if isinstance(row, dict)
        ],
    ]
    countries = {value for value in country_values if value}
    if len(countries) != 1:
        raise SurveyIdentityError(
            "V553 temporal input requires exactly one explicit country_code; "
            f"found {sorted(countries)}"
        )
    country_code = next(iter(countries))

    normalized_rows: list[dict[str, Any]] = []
    years_seen: dict[int, str] = {}
    for raw_row in wave_rows:
        if not isinstance(raw_row, dict):
            continue
        row = dict(raw_row)
        wave = _clean(row.get("canonical_wave") or row.get("wave"))
        identity = require_survey_identity(
            row.get("source") or source,
            wave,
            row.get("country_code") or country_code,
            require_country=True,
        )
        if identity.source_key != source_key:
            raise SurveyIdentityError(
                "V553 temporal input mixes survey families: "
                f"{source_key} and {identity.source_key}"
            )
        row_country = canonical_country_code(
            row.get("country_code") or country_code
        )
        if row_country != country_code:
            raise SurveyIdentityError(
                "V553 temporal input mixes countries: "
                f"{country_code} and {row_country}"
            )
        temporal_year = _explicit_temporal_year(
            row,
            identity.canonical_wave,
        )
        if temporal_year is None:
            raise SurveyIdentityError(
                "V553 temporal input requires temporal_year/fieldwork_year/"
                f"survey_year for non-calendar wave {identity.canonical_wave}"
            )
        if temporal_year in years_seen:
            raise SurveyIdentityError(
                "V553 temporal input requires one anchor per calendar year; "
                f"{temporal_year} is used by {years_seen[temporal_year]} and "
                f"{identity.canonical_wave}"
            )
        years_seen[temporal_year] = identity.canonical_wave
        row["source"] = source
        row["source_family"] = source
        row["canonical_wave"] = identity.canonical_wave
        row["country_code"] = country_code
        row["temporal_year"] = temporal_year
        normalized_rows.append(row)

    if not normalized_rows:
        raise SurveyIdentityError(
            "V553 temporal input has no valid wave rows"
        )
    normalized_rows.sort(
        key=lambda row: (
            int(row["temporal_year"]),
            _clean(row["canonical_wave"]),
        )
    )
    normalized = dict(report)
    normalized["source"] = source
    normalized["source_family"] = source
    normalized["country_code"] = country_code
    normalized["wave_rows"] = normalized_rows
    normalized["wave_count"] = len(normalized_rows)
    return normalized


__all__ = ["normalize_temporal_report_identity"]
