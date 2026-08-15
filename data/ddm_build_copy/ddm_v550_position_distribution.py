#!/usr/bin/env python3
"""Respondent position-distribution helpers for V550."""

from __future__ import annotations

from typing import Any

import pandas as pd

from data.ddm_build_copy.ddm_v550_branching import INDICATOR_FIELDS
from data.ddm_build_copy.ddm_v550_manifest import utc_now
from data.ddm_build_copy.ddm_v550_metrics import classify_weight_status


POSITION_DISTRIBUTION_COLUMNS = [
    "run_id",
    "shard_id",
    "source",
    "source_family",
    "wave",
    "canonical_wave",
    "country_code",
    "position_field",
    "position_value",
    "n_unweighted",
    "n_weighted",
    "pct_unweighted",
    "pct_weighted",
    "weight_status",
    "semantic_role",
    "created_at",
]


def _respondent_slice(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return frame
    ordered = frame.copy().reset_index(drop=True)
    sort_columns = [column for column in ["respondent_id", "country_code", "var_code", "question_id"] if column in ordered.columns]
    if sort_columns:
        ordered = ordered.sort_values(sort_columns, kind="mergesort")
    dedupe_columns = [column for column in ["respondent_id", "country_code"] if column in ordered.columns]
    if dedupe_columns:
        ordered = ordered.drop_duplicates(subset=dedupe_columns, keep="first")
    else:
        ordered = ordered.drop_duplicates()
    return ordered.reset_index(drop=True)


def _first_text(frame: pd.DataFrame, column: str, default: str = "") -> str:
    if column not in frame.columns or frame[column].empty:
        return default
    series = frame[column].dropna().astype(str)
    if series.empty:
        return default
    value = str(series.iloc[0]).strip()
    return value or default


def build_position_distribution_rows(
    country_frames: dict[str, pd.DataFrame],
    *,
    run_id: str,
    shard_id: str,
    source: str,
    source_family: str,
    wave: str,
    canonical_wave: str,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for country_code, frame in country_frames.items():
        if frame is None or frame.empty:
            continue
        respondent_frame = _respondent_slice(frame)
        if respondent_frame.empty:
            continue
        weight_status, weight_series = classify_weight_status(respondent_frame["weight_value"] if "weight_value" in respondent_frame.columns else None)
        validated_weights = weight_series if weight_status == "weighted" else None
        for position_field in INDICATOR_FIELDS:
            if position_field not in respondent_frame.columns:
                continue
            values = respondent_frame[position_field].fillna("").astype(str).str.strip()
            values = values.where(values.str.lower().ne("nan"), "")
            mask = values.ne("")
            if not mask.any():
                continue
            field_values = values[mask]
            total_unweighted = int(field_values.shape[0])
            total_weight = None
            if validated_weights is not None:
                total_weight = float(pd.to_numeric(validated_weights.loc[mask], errors="coerce").fillna(0.0).sum())
                if total_weight <= 0:
                    total_weight = None
            subset = respondent_frame.loc[mask].copy()
            subset["_position_value"] = field_values.to_numpy()
            grouped = subset.groupby("_position_value", dropna=False)
            for position_value, subframe in grouped:
                n_unweighted = int(len(subframe))
                if validated_weights is None or total_weight is None:
                    n_weighted = pd.NA
                    pct_weighted = pd.NA
                else:
                    w = float(pd.to_numeric(validated_weights.loc[subframe.index], errors="coerce").fillna(0.0).sum())
                    n_weighted = w
                    pct_weighted = float(w / total_weight) if total_weight else pd.NA
                rows.append(
                    {
                        "run_id": run_id,
                        "shard_id": shard_id,
                        "source": source or _first_text(respondent_frame, "source"),
                        "source_family": source_family or _first_text(respondent_frame, "source_family", default=source),
                        "wave": wave or _first_text(respondent_frame, "wave"),
                        "canonical_wave": canonical_wave or _first_text(respondent_frame, "canonical_wave"),
                        "country_code": str(country_code),
                        "position_field": position_field,
                        "position_value": str(position_value),
                        "n_unweighted": n_unweighted,
                        "n_weighted": n_weighted,
                        "pct_unweighted": float(n_unweighted / total_unweighted) if total_unweighted else 0.0,
                        "pct_weighted": pct_weighted,
                        "weight_status": weight_status,
                        "semantic_role": "POSITION_COORDINATE",
                        "created_at": utc_now(),
                    }
                )
    if not rows:
        out = pd.DataFrame(columns=POSITION_DISTRIBUTION_COLUMNS)
        for col in ["n_weighted", "pct_weighted"]:
            if col in out.columns:
                out[col] = out[col].astype("float64")
        return out
    out = pd.DataFrame(rows)
    for column in POSITION_DISTRIBUTION_COLUMNS:
        if column not in out.columns:
            out[column] = pd.NA
    out = out[POSITION_DISTRIBUTION_COLUMNS]
    for col in ["n_weighted", "pct_weighted"]:
        if col in out.columns and out[col].dtype == "object":
            out[col] = pd.to_numeric(out[col], errors="coerce").astype("float64")
    return out
