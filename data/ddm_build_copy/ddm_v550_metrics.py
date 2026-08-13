#!/usr/bin/env python3
"""Metrics helpers for V550."""

from __future__ import annotations

from collections import Counter
from math import log
import re
from typing import Any, Iterable
import warnings

import numpy as np
import pandas as pd
from sklearn.metrics import mutual_info_score


def safe_series(values: Iterable[Any]) -> pd.Series:
    return pd.Series(list(values), dtype="object").replace({None: np.nan, "": np.nan})


def weighted_counts(values: pd.Series, weights: pd.Series | None = None) -> pd.DataFrame:
    df = pd.DataFrame({"value": values})
    if weights is None:
        counts = df["value"].value_counts(dropna=False).rename_axis("value").reset_index(name="n_unweighted")
        counts["n_weighted"] = pd.NA
        return counts
    df["weight"] = pd.to_numeric(weights, errors="coerce").fillna(0.0)
    grouped = df.groupby("value", dropna=False).agg(n_unweighted=("value", "size"), n_weighted=("weight", "sum")).reset_index()
    return grouped


def classify_weight_status(series: pd.Series | None) -> tuple[str, pd.Series | None]:
    """Return status and a validated positive finite weight series."""
    if series is None:
        return "missing", None
    numeric = pd.to_numeric(series, errors="coerce")
    valid = numeric.where(numeric > 0)
    valid = valid.where(np.isfinite(valid))
    valid_count = int(valid.notna().sum())
    total_count = int(len(series))
    if total_count == 0:
        return "missing", None
    if valid_count == 0:
        if numeric.isna().all():
            return "missing", None
        if (numeric.fillna(0) <= 0).all():
            return "invalid", None
        return "unweighted_only", None
    if valid_count < total_count:
        return "partial", valid
    return "weighted", valid


def entropy_from_counts(counts: Iterable[float]) -> float:
    total = float(sum(counts))
    if total <= 0:
        return 0.0
    ent = 0.0
    for c in counts:
        if c <= 0:
            continue
        p = float(c) / total
        ent -= p * log(p, 2)
    return float(ent)


def distribution_entropy(series: pd.Series, weights: pd.Series | None = None) -> float:
    if series.empty:
        return 0.0
    if weights is None:
        return entropy_from_counts(series.value_counts(dropna=False).tolist())
    df = pd.DataFrame({"value": series, "weight": pd.to_numeric(weights, errors="coerce").fillna(0.0)})
    grouped = df.groupby("value", dropna=False)["weight"].sum().tolist()
    return entropy_from_counts(grouped)


def conditional_entropy(y: pd.Series, x: pd.Series, weights: pd.Series | None = None) -> float:
    if y.empty or x.empty:
        return 0.0
    df = pd.DataFrame({"y": y, "x": x})
    if weights is not None:
        df["w"] = pd.to_numeric(weights, errors="coerce").fillna(0.0)
    total = float(df["w"].sum()) if weights is not None else float(len(df))
    if total <= 0:
        return 0.0
    result = 0.0
    for value, sub in df.groupby("x", dropna=False):
        if weights is not None:
            sub_weight = float(sub["w"].sum())
            if sub_weight <= 0:
                continue
            h = entropy_from_counts(sub.groupby("y")["w"].sum().tolist())
            result += (sub_weight / total) * h
        else:
            h = entropy_from_counts(sub["y"].value_counts(dropna=False).tolist())
            result += (len(sub) / total) * h
    return float(result)


def cramers_v(x: pd.Series, y: pd.Series) -> float:
    table = pd.crosstab(x.fillna(""), y.fillna(""))
    if table.empty:
        return 0.0
    observed = table.to_numpy(dtype=float)
    total = observed.sum()
    if total <= 0:
        return 0.0
    row_totals = observed.sum(axis=1, keepdims=True)
    col_totals = observed.sum(axis=0, keepdims=True)
    expected = row_totals @ col_totals / total
    with np.errstate(divide="ignore", invalid="ignore"):
        chi2 = np.nansum((observed - expected) ** 2 / expected)
    n = observed.sum()
    if n <= 1:
        return 0.0
    r, k = table.shape
    denom = min(r - 1, k - 1)
    if denom <= 0:
        return 0.0
    return float(np.sqrt(chi2 / (n * denom)))


def normalized_mutual_information(x: pd.Series, y: pd.Series) -> float:
    if x.empty or y.empty:
        return 0.0
    # sklearn emits a noisy warning for high-cardinality label sets even when
    # the score is still usable for our bounded ranking purposes.
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message="The number of unique classes is greater than 50% of the number of samples.*",
            category=UserWarning,
        )
        mi = mutual_info_score(x.fillna("").astype(str), y.fillna("").astype(str))
    hx = distribution_entropy(x.astype(str))
    hy = distribution_entropy(y.astype(str))
    denom = max(hx, hy)
    if denom <= 0:
        return 0.0
    return float(mi / denom)


def dominant_response(series: pd.Series, weights: pd.Series | None = None) -> tuple[str, float]:
    if series.empty:
        return "", 0.0
    if weights is None:
        counts = series.fillna("").astype(str).value_counts(dropna=False)
        total = counts.sum()
        if total <= 0:
            return "", 0.0
        top = counts.index[0]
        return str(top), float(counts.iloc[0] / total)
    df = pd.DataFrame({"value": series.fillna("").astype(str), "weight": pd.to_numeric(weights, errors="coerce").fillna(0.0)})
    grouped = df.groupby("value")["weight"].sum().sort_values(ascending=False)
    if grouped.empty:
        return "", 0.0
    top = grouped.index[0]
    total = float(grouped.sum())
    return str(top), float(grouped.iloc[0] / total) if total > 0 else 0.0


def uplift_vs_baseline(branch_pct: float, baseline_pct: float) -> float:
    return float(branch_pct - baseline_pct)


def evidence_stratum_from_row(
    *,
    bridge_evidence_lane: Any = "",
    semantic_role: Any = "",
    v551_relation_evidence_eligible: Any = None,
) -> str:
    lane = str(bridge_evidence_lane or "").strip().lower()
    role = str(semantic_role or "").strip().upper()
    eligible = False
    try:
        if v551_relation_evidence_eligible is not None and not pd.isna(v551_relation_evidence_eligible):
            eligible = bool(v551_relation_evidence_eligible)
    except Exception:
        eligible = False
    if lane == "direct_relation_response" or role == "RELATION_EVIDENCE":
        return "relation_evidence"
    if lane == "derived_determinicity":
        return "conditional_determinicity"
    if lane == "position_context" or role == "POSITION_COORDINATE":
        return "position_context"
    if lane in {"structural_context", "audit_quarantine", "disabled_artifact"}:
        return lane
    if eligible:
        return "eligible_context"
    return "blocked_context"


def evidence_stratum_v2_from_row(
    *,
    bridge_evidence_lane: Any = "",
    semantic_role: Any = "",
    v551_relation_evidence_eligible: Any = None,
) -> str:
    stratum = evidence_stratum_from_row(
        bridge_evidence_lane=bridge_evidence_lane,
        semantic_role=semantic_role,
        v551_relation_evidence_eligible=v551_relation_evidence_eligible,
    )
    return {
        "relation_evidence": "certified",
        "conditional_determinicity": "provisional",
        "position_context": "reviewable",
        "eligible_context": "reviewable",
        "blocked_context": "blocked",
        "structural_context": "reviewable",
        "audit_quarantine": "blocked",
        "disabled_artifact": "blocked",
    }.get(stratum, "reviewable")


def numeric_wrapper_audit_from_row(row: Any) -> dict[str, Any]:
    label = str(getattr(row, "get", lambda key, default=None: default)("response_label", "") or "").strip()
    family = str(getattr(row, "get", lambda key, default=None: default)("response_family", "") or "").strip().lower()
    response_value = getattr(row, "get", lambda key, default=None: default)("response_value_normalized", "")
    response_direction = str(getattr(row, "get", lambda key, default=None: default)("response_direction", "") or "").strip()
    response_intensity = getattr(row, "get", lambda key, default=None: default)("response_intensity", None)
    numeric_like_label = bool(label) and bool(re.fullmatch(r"[+-]?(?:\d+(?:\.\d+)?|\.\d+)", label))
    numeric_family_compatible = bool(family) and (
        family in {"yes_no", "agreement_scale", "trust_scale", "satisfaction_scale", "importance_scale", "frequency_scale", "ordinal_scale", "left_right_scale", "numeric_quantity", "numeric_scale", "count", "count_scale"}
        or family.endswith("_scale")
        or any(token in family for token in {"numeric", "quantity", "count"})
    )
    if not numeric_like_label:
        wrapper_status = "not_numeric"
        wrapper_reason = "textual_label_no_numeric_wrapper_needed"
        wrapper_confidence = "high"
    elif numeric_family_compatible:
        wrapper_status = "wrapped_numeric"
        wrapper_reason = "numeric_only_label_supported_by_numeric_family"
        wrapper_confidence = "high" if response_direction or response_intensity is not None else "medium"
    else:
        wrapper_status = "blocked_numeric_wrapper"
        wrapper_reason = "numeric_only_label_requires_numeric_scale_family"
        wrapper_confidence = "low"
    return {
        "numeric_like_label": numeric_like_label,
        "numeric_family_compatible": numeric_family_compatible,
        "numeric_wrapper_status": wrapper_status,
        "numeric_wrapper_reason": wrapper_reason,
        "numeric_wrapper_confidence": wrapper_confidence,
        "response_value_normalized": response_value,
    }
