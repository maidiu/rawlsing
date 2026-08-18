#!/usr/bin/env python3
"""Fail-closed metadata adapter for governed V550J joint-only variables.

This module does not create question-use authority.  It supplies only the
question-level coordinates V550J needs for registry-authorized variables that
travel through the validated shared respondent substrate but are intentionally
absent from the base V550/QSM question-use surface.
"""

from __future__ import annotations

import json
from typing import Any, Iterable, Mapping

import pandas as pd


class V550JJointOnlyMetadataError(RuntimeError):
    pass


def _clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    text = str(value).strip()
    return "" if text.lower() in {"", "nan", "none", "null"} else text


def _truthy(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return _clean(value).lower() in {"1", "true", "t", "yes", "y"}


def _configuration_ids(value: Any) -> set[str]:
    if isinstance(value, (list, tuple, set)):
        return {_clean(item) for item in value if _clean(item)}
    text = _clean(value)
    if not text:
        return set()
    try:
        payload = json.loads(text)
    except Exception:
        payload = None
    if isinstance(payload, list):
        return {_clean(item) for item in payload if _clean(item)}
    return {part.strip() for part in text.split(",") if part.strip()}


def _stable_value(frame: pd.DataFrame, column: str, *, var_code: str) -> str:
    if column not in frame.columns:
        return ""
    values = list(
        dict.fromkeys(
            _clean(value)
            for value in frame[column].tolist()
            if _clean(value)
        )
    )
    if len(values) > 1:
        raise V550JJointOnlyMetadataError(
            f"V550J_JOINT_ONLY_METADATA_CONTRADICTION:{var_code}:{column}:{values[:8]}"
        )
    return values[0] if values else ""


def augment_family_questions_from_prepared(
    family_questions: pd.DataFrame,
    prepared_frame: pd.DataFrame | None,
    *,
    family_id: str,
    family_var_codes: Iterable[Any],
    registry_items: Iterable[Mapping[str, Any]] = (),
    source: str,
    canonical_wave: str,
) -> pd.DataFrame:
    """Add metadata-only rows for validated, registry-selected J-only variables.

    Existing question-use-contract rows always win.  New rows are admitted only
    when the prepared substrate says the variable was selected for this exact
    joint configuration.  The caller has already authenticated the prepared
    frame by UID, so source/wave spellings here remain provenance rather than a
    second identity authority.  No question-use-contract hash or V551 permission
    is invented.
    """
    base = family_questions.copy()
    if prepared_frame is None or prepared_frame.empty:
        return base

    configured = [str(value).strip().upper() for value in family_var_codes if str(value).strip()]
    existing = set()
    if "var_code" in base.columns:
        existing = {
            _clean(value).upper()
            for value in base["var_code"].tolist()
            if _clean(value)
        }
    missing = [code for code in configured if code not in existing]
    if not missing:
        return base

    prepared = prepared_frame.copy()
    var_column = "var_code_norm" if "var_code_norm" in prepared.columns else "var_code"
    if var_column not in prepared.columns:
        return base
    prepared["__pg8_var_code"] = prepared[var_column].fillna("").astype(str).str.strip().str.upper()

    if "joint_configuration_selected" not in prepared.columns:
        return base
    prepared = prepared[prepared["joint_configuration_selected"].map(_truthy)].copy()
    if prepared.empty:
        return base
    if "joint_configuration_ids_json" not in prepared.columns:
        return base
    prepared = prepared[
        prepared["joint_configuration_ids_json"].map(
            lambda value: family_id in _configuration_ids(value)
        )
    ].copy()
    if prepared.empty:
        return base

    registry_by_var: dict[str, Mapping[str, Any]] = {}
    for item in registry_items:
        code = _clean(item.get("var_code")).upper()
        if code:
            registry_by_var[code] = item

    additions: list[dict[str, Any]] = []
    for code in missing:
        rows = prepared[prepared["__pg8_var_code"].eq(code)].copy()
        if rows.empty:
            continue
        item = registry_by_var.get(code, {})
        question_id = _stable_value(rows, "question_id", var_code=code) or _clean(item.get("question_implementation_id"))
        question_text = _stable_value(rows, "question_text", var_code=code)
        prepared_source = _stable_value(rows, "source", var_code=code)
        prepared_wave = _stable_value(rows, "wave", var_code=code)
        prepared_canonical_wave = _stable_value(rows, "canonical_wave", var_code=code)
        additions.append(
            {
                "var_code": code,
                "question_id": question_id,
                "question_text": question_text,
                "source": source,
                "wave": prepared_wave or canonical_wave,
                "canonical_wave": canonical_wave,
                "joint_only_prepared_source": prepared_source,
                "joint_only_prepared_wave": prepared_wave,
                "joint_only_prepared_canonical_wave": prepared_canonical_wave,
                "joint_only_metadata_source": "validated_prepared_substrate",
            }
        )

    if not additions:
        return base
    return pd.concat([base, pd.DataFrame(additions)], ignore_index=True, sort=False)
