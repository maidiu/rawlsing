#!/usr/bin/env python3
"""Wave-relative support threshold helpers for V550/V551/V552."""

from __future__ import annotations

import math
from typing import Any

import numpy as np
import pandas as pd

DEFAULT_SUPPORT_RATE = 0.005
DEFAULT_SUPPORT_CAP = 30
DEFAULT_SUPPORT_FLOOR = 2

STRUCTURAL_LANES = {"structural_context", "audit_quarantine", "disabled_artifact", "unknown"}


def _coerce_support_total(value: Any) -> float | None:
    try:
        if value is None:
            return None
        parsed = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
        if pd.isna(parsed):
            return None
        total = float(parsed)
        if total <= 0:
            return None
        return total
    except Exception:
        return None


def support_threshold_from_total(
    total_respondents: Any,
    *,
    support_rate: float = DEFAULT_SUPPORT_RATE,
    support_cap: int = DEFAULT_SUPPORT_CAP,
    support_floor: int = DEFAULT_SUPPORT_FLOOR,
) -> int:
    total = _coerce_support_total(total_respondents)
    if total is None:
        return int(support_cap)
    threshold = int(math.ceil(float(total) * float(support_rate)))
    threshold = max(int(support_floor), threshold)
    threshold = min(int(support_cap), threshold)
    return threshold


def support_threshold_series(
    total_respondents: Any,
    *,
    support_rate: float = DEFAULT_SUPPORT_RATE,
    support_cap: int = DEFAULT_SUPPORT_CAP,
    support_floor: int = DEFAULT_SUPPORT_FLOOR,
) -> pd.Series:
    series = pd.to_numeric(total_respondents, errors="coerce")
    if isinstance(series, pd.Series):
        thresholds = pd.Series(np.ceil(series.astype(float) * float(support_rate)), index=series.index, dtype="float64")
        thresholds = thresholds.where(series.notna(), float(support_cap))
        thresholds = thresholds.fillna(float(support_cap)).clip(lower=float(support_floor), upper=float(support_cap)).astype(int)
        return thresholds
    return pd.Series([], dtype="int64")


def support_status_from_count(
    support_count: Any,
    *,
    total_respondents: Any = None,
    lane: str = "relation",
    support_rate: float = DEFAULT_SUPPORT_RATE,
    support_cap: int = DEFAULT_SUPPORT_CAP,
    support_floor: int = DEFAULT_SUPPORT_FLOOR,
) -> str:
    parsed = pd.to_numeric(pd.Series([support_count]), errors="coerce").iloc[0]
    if pd.isna(parsed):
        return "not_applicable" if str(lane or "").strip().lower() in STRUCTURAL_LANES else "missing_support"
    support = float(parsed)
    if support <= 0:
        return "zero_support"
    threshold = support_threshold_from_total(
        total_respondents,
        support_rate=support_rate,
        support_cap=support_cap,
        support_floor=support_floor,
    )
    if support < threshold:
        return "underpowered"
    return "sufficient_support"


def confidence_tier_from_support(
    support_count: Any,
    *,
    total_respondents: Any = None,
    high_floor: int = 100,
    support_rate: float = DEFAULT_SUPPORT_RATE,
    support_cap: int = DEFAULT_SUPPORT_CAP,
    support_floor: int = DEFAULT_SUPPORT_FLOOR,
) -> str:
    parsed = pd.to_numeric(pd.Series([support_count]), errors="coerce").iloc[0]
    if pd.isna(parsed):
        return "low"
    support = float(parsed)
    if support <= 0:
        return "low"
    threshold = support_threshold_from_total(
        total_respondents,
        support_rate=support_rate,
        support_cap=support_cap,
        support_floor=support_floor,
    )
    if support < threshold:
        return "low"
    if support >= max(float(high_floor), float(threshold) * 3.0):
        return "high"
    return "medium"
