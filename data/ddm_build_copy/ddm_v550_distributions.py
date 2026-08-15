#!/usr/bin/env python3
"""Distribution-table helpers for V550."""

from __future__ import annotations

from typing import Any

import pandas as pd

from data.ddm_build_copy.ddm_v550_metrics import classify_weight_status
from data.ddm_build_copy.ddm_v550_response_options import normalize_response_code
from data.ddm_build_copy.ddm_v550_support import support_threshold_from_total
from data.ddm_build_copy.ddm_v550_family_overlay import canonical_family_key, canonical_wave_key, wave_aliases
from data.ddm_build_copy.ddm_v550_source_structure import _normalized_join_key
from data.ddm_build_copy.ddm_v550_io import normalize_family


def _first_nonempty(series: pd.Series, default: Any = "") -> Any:
    if series.empty:
        return default
    cleaned = series.fillna("").astype(str).str.strip()
    cleaned = cleaned[~cleaned.str.lower().isin(["nan", "none"])]
    cleaned = cleaned[cleaned.ne("")]
    if cleaned.empty:
        return default
    return cleaned.iloc[0]


def _to_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)) and not pd.isna(value):
        return value != 0
    text = str(value).strip().lower()
    if text in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "f", "no", "n", "off", "", "nan", "none"}:
        return False
    return default


def _first_bool(series: pd.Series, default: bool = False) -> bool:
    if series.empty:
        return default
    cleaned = series.map(lambda value: _to_bool(value, default))
    if cleaned.empty:
        return default
    return bool(cleaned.any())


def _first_value(series: pd.Series, default: Any = "") -> Any:
    if series.empty:
        return default
    for value in series.tolist():
        if value is None or pd.isna(value):
            continue
        text = str(value).strip()
        if text and text.lower() not in {"nan", "none"}:
            return value
    return default


def _stringify_scalar(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    text = str(value).strip()
    return "" if text.lower() == "nan" else text


def _semantics_lookup_key(
    qmeta: dict[str, Any],
    response_value_normalized: str,
    response_label: str,
    normalized_response_label: str,
) -> list[tuple[str, str, str, str]]:
    source_label = str(qmeta.get("source", ""))
    source_family = normalize_family(source_label)
    source = canonical_family_key(source_label)
    source_variants = [source_label, source_family, source, canonical_family_key(source_family or source_label or source)]
    wave_candidates: list[str] = []
    for value in [qmeta.get("wave", ""), qmeta.get("canonical_wave", "")]:
        for token in [value, canonical_wave_key(source_family or source_label or source, value), *wave_aliases(source_family or source_label or source, value)]:
            token_text = str(token or "").strip()
            if token_text and token_text not in wave_candidates:
                wave_candidates.append(token_text)
            normalized = str(token_text or "").strip()
            if normalized:
                lowered = normalized.lower()
                if lowered not in [candidate.lower() for candidate in wave_candidates]:
                    wave_candidates.append(normalized)
    var_name = str(qmeta.get("var_code", "") or qmeta.get("var_name", ""))
    var_name_variants = [var_name]
    normalized_var = _normalized_join_key(var_name)
    raw_candidates = [
        str(response_value_normalized or ""),
        str(response_label or ""),
        str(normalized_response_label or ""),
    ]
    value_candidates: list[str] = []
    for candidate in raw_candidates:
        if not candidate:
            continue
        normalized_candidate = normalize_response_code(candidate)
        for value in [candidate, normalized_candidate or ""]:
            cleaned = str(value or "").strip()
            if cleaned and cleaned.lower() not in {"nan", "none"} and cleaned not in value_candidates:
                value_candidates.append(cleaned)
    keys: list[tuple[str, str, str, str]] = []
    for wave in wave_candidates:
        for var in var_name_variants:
            for value in value_candidates:
                for source_variant in source_variants:
                    if source_variant and wave and var and value:
                        keys.append((source_variant, wave, var, value))
                    if source_variant and wave and normalized_var and value:
                        keys.append((source_variant, wave, normalized_var, value))
    return keys




def _first_scalar_text(*values: Any) -> str:
    for value in values:
        cleaned = _stringify_scalar(value)
        if cleaned:
            return cleaned
    return ""


def _semantic_row_value(sem: dict[str, Any], group: pd.DataFrame, field: str, default: Any = "") -> Any:
    if sem:
        value = sem.get(field, default)
        return default if value is None else value
    if field in group.columns:
        return _first_value(group[field], default)
    return default


def _semantic_row_bool(sem: dict[str, Any], group: pd.DataFrame, field: str, default: bool = False) -> bool:
    if sem:
        return _to_bool(sem.get(field, default), default)
    if field in group.columns:
        return _first_bool(group[field], default)
    return default


def _resolved_response_semantics(
    *,
    sem: dict[str, Any],
    group: pd.DataFrame,
    value: str,
    fallback_label: str,
) -> dict[str, Any]:
    matched = bool(sem)
    response_label = _first_scalar_text(
        sem.get("response_label"),
        sem.get("normalized_response_label"),
        sem.get("value_label_clean"),
        fallback_label,
        value,
    ) if matched else _first_nonempty(group.get("response_label", pd.Series(dtype="object")), fallback_label or value)
    normalized_label = _first_scalar_text(
        sem.get("normalized_response_label"), sem.get("value_label_clean"), response_label
    ) if matched else _first_nonempty(group.get("normalized_response_label", pd.Series(dtype="object")), response_label)

    default_missing = value.strip().lower() in {"", "nan", "none"}
    is_substantive = _semantic_row_bool(sem, group, "is_substantive", False)
    is_missing = _semantic_row_bool(sem, group, "is_missing", default_missing)
    is_dk = _semantic_row_bool(sem, group, "is_dk", False)
    is_refusal = _semantic_row_bool(sem, group, "is_refusal", False)
    is_iap = _semantic_row_bool(sem, group, "is_iap", False)
    is_not_asked = _semantic_row_bool(sem, group, "is_not_asked", False)
    is_inapplicable = _semantic_row_bool(sem, group, "is_inapplicable", False)
    explicit_special = _semantic_row_bool(sem, group, "is_special", False)
    is_special = explicit_special or is_missing or is_dk or is_refusal or is_iap or is_not_asked or is_inapplicable

    payload = {
        "response_label": response_label,
        "normalized_response_label": normalized_label,
        "response_family": _stringify_scalar(_semantic_row_value(sem, group, "response_family", "")),
        "response_direction": _stringify_scalar(_semantic_row_value(sem, group, "response_direction", "")),
        "response_intensity": _semantic_row_value(sem, group, "response_intensity", None),
        "polarity": _stringify_scalar(_semantic_row_value(sem, group, "polarity", "")),
        "ordinal_rank": _semantic_row_value(sem, group, "ordinal_rank", None),
        "scale_min": _semantic_row_value(sem, group, "scale_min", None),
        "scale_max": _semantic_row_value(sem, group, "scale_max", None),
        "scale_direction": _stringify_scalar(_semantic_row_value(sem, group, "scale_direction", "")),
        "directionality_status": _stringify_scalar(_semantic_row_value(sem, group, "directionality_status", "unknown")) or "unknown",
        "is_substantive": is_substantive,
        "is_missing": is_missing,
        "is_special": is_special,
        "is_dk": is_dk,
        "is_refusal": is_refusal,
        "is_iap": is_iap,
        "is_not_asked": is_not_asked,
        "is_inapplicable": is_inapplicable,
        "response_option_map_matched": matched or _semantic_row_bool({}, group, "response_option_map_matched", False),
        "response_semantics_status": _stringify_scalar(_semantic_row_value(sem, group, "response_semantics_status", "observed_only")) or "observed_only",
        "response_semantics_source": _stringify_scalar(_semantic_row_value(sem, group, "response_semantics_source", "observed_response_row")) or "observed_response_row",
        "response_semantics_contract_hash": _stringify_scalar(_semantic_row_value(sem, group, "response_semantics_contract_hash", "")),
        "normalization_confidence": _stringify_scalar(_semantic_row_value(sem, group, "normalization_confidence", "observed_only")) or "observed_only",
    }
    if is_special:
        payload.update(
            {
                "response_direction": "",
                "response_intensity": None,
                "polarity": "",
                "ordinal_rank": None,
                "scale_min": None,
                "scale_max": None,
                "scale_direction": "",
                "directionality_status": "NOT_CERTIFIED_SPECIAL",
            }
        )
    return payload

def build_distribution_tables(
    df: pd.DataFrame,
    qmeta: dict[str, Any],
    *,
    min_answer_n: int,
    min_cell_n: int,
    semantics_lookup: dict[tuple[str, str, str, str], dict[str, Any]] | None = None,
) -> tuple[str, pd.Series | None, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Build response distributions while preserving packet response authority."""
    effective_min_answer_n = support_threshold_from_total(qmeta.get("n_respondents"), support_cap=min_answer_n)
    effective_min_cell_n = support_threshold_from_total(qmeta.get("n_respondents"), support_cap=min_cell_n)
    weight_status, weights = classify_weight_status(df["weight_value"] if "weight_value" in df.columns else None)
    work = df.copy()
    if weights is not None:
        work["_valid_weight"] = weights
        total_weighted = float(pd.to_numeric(work["_valid_weight"], errors="coerce").fillna(0.0).sum())
    else:
        total_weighted = None
    total_unweighted = float(len(work)) or 1.0

    def resolve(group: pd.DataFrame, value: str) -> dict[str, Any]:
        fallback_label = _first_nonempty(group.get("response_label", pd.Series(dtype="object")), value)
        normalized_label = _first_nonempty(group.get("normalized_response_label", pd.Series(dtype="object")), fallback_label)
        sem: dict[str, Any] = {}
        if semantics_lookup:
            for key in _semantics_lookup_key(qmeta, value, fallback_label, normalized_label):
                candidate = semantics_lookup.get(key)
                if candidate:
                    sem = candidate
                    break
        return _resolved_response_semantics(sem=sem, group=group, value=value, fallback_label=fallback_label)

    answer_rows: list[dict[str, Any]] = []
    mapping_gap_rows: list[dict[str, Any]] = []
    underpowered_rows: list[dict[str, Any]] = []
    for value, group in work.groupby(["response_value_normalized"], dropna=False, sort=False):
        if isinstance(value, tuple) and len(value) == 1:
            value = value[0]
        value = str(value)
        semantics = resolve(group, value)
        n_unweighted = int(len(group))
        n_weighted = float(pd.to_numeric(group["_valid_weight"], errors="coerce").fillna(0.0).sum()) if "_valid_weight" in group.columns else None
        if n_unweighted < effective_min_answer_n:
            underpowered_rows.append({**qmeta, "gap_type": "underpowered_answer", "response_value": value, "n_unweighted": n_unweighted})
        answer_rows.append(
            {
                **qmeta,
                "analysis_scope": "country",
                "response_value_raw": value,
                "response_value_normalized": value,
                **semantics,
                "semantic_role": _first_nonempty(group.get("semantic_role", pd.Series(dtype="object")), qmeta.get("semantic_role", "")),
                "n_unweighted": n_unweighted,
                "n_weighted": n_weighted,
                "pct_unweighted": float(n_unweighted / total_unweighted) if total_unweighted else 0.0,
                "pct_weighted": float(n_weighted / total_weighted) if (total_weighted and n_weighted is not None) else None,
                "weight_status": weight_status,
                "confidence_tier": "usable" if (n_unweighted >= effective_min_cell_n and semantics["normalization_confidence"] != "observed_only") else "weak",
            }
        )

    country_rows: list[dict[str, Any]] = []
    for country_code, country_frame in work.groupby(["country_code"], dropna=False, sort=False):
        if isinstance(country_code, tuple) and len(country_code) == 1:
            country_code = country_code[0]
        country_code = str(country_code)
        country_total_unweighted = float(len(country_frame)) or 1.0
        country_total_weighted = None
        if "_valid_weight" in country_frame.columns:
            weighted = float(pd.to_numeric(country_frame["_valid_weight"], errors="coerce").fillna(0.0).sum())
            country_total_weighted = weighted if weighted > 0 else None
        for value, group in country_frame.groupby(["response_value_normalized"], dropna=False, sort=False):
            if isinstance(value, tuple) and len(value) == 1:
                value = value[0]
            value = str(value)
            semantics = resolve(group, value)
            group_weight = float(pd.to_numeric(group["_valid_weight"], errors="coerce").fillna(0.0).sum()) if "_valid_weight" in group.columns else None
            country_rows.append(
                {
                    **qmeta,
                    "country_code": country_code,
                    "response_value_raw": value,
                    "response_value_normalized": value,
                    **semantics,
                    "semantic_role": _first_nonempty(group.get("semantic_role", pd.Series(dtype="object")), qmeta.get("semantic_role", "")),
                    "n_unweighted": int(len(group)),
                    "n_weighted": group_weight,
                    "pct_unweighted": float(len(group) / country_total_unweighted) if country_total_unweighted else 0.0,
                    "pct_weighted": float(group_weight / country_total_weighted) if (country_total_weighted and group_weight is not None) else None,
                    "weight_status": weight_status,
                    "confidence_tier": "usable" if (len(group) >= effective_min_cell_n and semantics["normalization_confidence"] != "observed_only") else "weak",
                }
            )

    return (
        weight_status,
        weights,
        pd.DataFrame(answer_rows),
        pd.DataFrame(country_rows),
        pd.DataFrame(mapping_gap_rows),
        pd.DataFrame(underpowered_rows),
    )
