#!/usr/bin/env python3
"""V551 directionality expectation and response-row stamp coverage.

The denominator is defined by V550's variable/question-level directional
authority.  Row-level stamping success must never be used to decide whether a
row belongs in that denominator, because that would hide exactly the failures
V551 must detect before promotion.
"""
from __future__ import annotations

from typing import Any

import pandas as pd

APPROVED_DIRECT_RELATION_SOURCE_TABLES = {
    "answer_distribution",
    "country_answer_distribution",
}

# Keep aligned with the response directions accepted by V551 atom compilation.
CERTIFIED_RESPONSE_DIRECTIONS = {
    "agree",
    "disagree",
    "graded",
    "intermediate",
    "negative",
    "neutral",
    "oppose",
    "positive",
    "support",
}

DIRECTIONAL_EXPECTATION_REQUIRED_COLUMNS = [
    "bridge_evidence_lane",
    "source_table",
    "current_directional_atom_eligible",
    "is_substantive",
    "is_missing",
    "is_special",
]

DIRECTIONAL_STAMP_REQUIRED_COLUMNS = [
    "response_option_map_matched",
    "response_direction",
    "response_intensity",
]

DIRECTIONAL_STAMP_AUDIT_COLUMNS = [
    "source",
    "source_family",
    "wave",
    "canonical_wave",
    "country_code",
    "question_id",
    "var_code",
    "source_table",
    "response_value_raw",
    "response_value_normalized",
    "response_label",
    "source_row_hash",
    "current_directional_atom_eligible",
    "directional_certification_status",
    "directionality_authority_status",
    "response_option_map_matched",
    "response_direction",
    "response_intensity",
    "directionality_stamp_status",
    "directionality_stamp_failure_reason",
]


def _clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    text = str(value).strip()
    return "" if text.lower() in {"nan", "none", "null"} else text


def _to_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)) and not pd.isna(value):
        return value != 0
    text = _clean(value).lower()
    if text in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "f", "no", "n", "off", ""}:
        return False
    return default


def _safe_float(value: Any) -> float | None:
    try:
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return None
        parsed = float(value)
        return None if pd.isna(parsed) else parsed
    except Exception:
        return None


def build_v551_directionality_expected_bridge(bridge: pd.DataFrame) -> pd.DataFrame:
    """Return substantive response rows that owe V551 a directional stamp.

    ``current_directional_atom_eligible`` is the canonical variable/question-
    level authority decision.  This function deliberately does not rebuild
    that authority from downstream status columns: if the governing contract
    says a variable is currently directional, each substantive response row
    in the direct relation lane owes V551 a stamp.

    This is an applicability denominator, not a promotability filter.  It
    intentionally does NOT gate on row-level stamping fields such as
    ``response_option_map_matched``, ``response_direction``,
    ``response_intensity``, signed projection fields, support, or the existing
    ``v551_relation_evidence_eligible`` flag.
    """
    if bridge.empty:
        out = bridge.copy()
        out["v551_directionality_expected"] = pd.Series(dtype=bool)
        return out

    missing = [
        column for column in DIRECTIONAL_EXPECTATION_REQUIRED_COLUMNS
        if column not in bridge.columns
    ]
    if missing:
        raise ValueError(
            "BLOCKED_V551_MISSING_DIRECTIONAL_EXPECTATION_CONTRACT: "
            + ", ".join(sorted(missing))
        )

    frame = bridge.copy()
    current_directional = frame["current_directional_atom_eligible"].map(
        lambda value: _to_bool(value, False)
    )
    direct_lane = (
        frame["bridge_evidence_lane"]
        .fillna("")
        .astype(str)
        .str.strip()
        .eq("direct_relation_response")
    )
    approved_source = (
        frame["source_table"]
        .fillna("")
        .astype(str)
        .str.strip()
        .isin(APPROVED_DIRECT_RELATION_SOURCE_TABLES)
    )
    substantive = frame["is_substantive"].map(lambda value: _to_bool(value, False))
    missing_response = frame["is_missing"].map(lambda value: _to_bool(value, False))
    special_response = frame["is_special"].map(lambda value: _to_bool(value, False))

    mask = (
        current_directional
        & direct_lane
        & approved_source
        & substantive
        & ~missing_response
        & ~special_response
    )

    expected = frame.loc[mask].copy().reset_index(drop=True)
    expected["v551_directionality_expected"] = True
    return expected


def build_v551_directionality_stamp_audit(bridge: pd.DataFrame) -> pd.DataFrame:
    """Audit whether every authority-expected response row is actually stamped."""
    expected = build_v551_directionality_expected_bridge(bridge)
    if expected.empty:
        return pd.DataFrame(columns=DIRECTIONAL_STAMP_AUDIT_COLUMNS)

    missing = [
        column for column in DIRECTIONAL_STAMP_REQUIRED_COLUMNS
        if column not in expected.columns
    ]
    if missing:
        raise ValueError(
            "BLOCKED_V551_MISSING_DIRECTIONAL_STAMP_CONTRACT: "
            + ", ".join(sorted(missing))
        )

    rows: list[dict[str, Any]] = []
    for row in expected.to_dict("records"):
        failures: list[str] = []
        map_matched = _to_bool(row.get("response_option_map_matched"), False)
        direction = _clean(row.get("response_direction")).lower()
        intensity = _safe_float(row.get("response_intensity"))

        if not map_matched:
            failures.append("response_option_map_unmatched")
        if direction not in CERTIFIED_RESPONSE_DIRECTIONS:
            failures.append("missing_certified_response_direction")
        if intensity is None:
            failures.append("missing_response_intensity")

        rows.append(
            {
                "source": _clean(row.get("source")),
                "source_family": _clean(row.get("source_family")),
                "wave": _clean(row.get("wave")),
                "canonical_wave": _clean(row.get("canonical_wave")),
                "country_code": _clean(row.get("country_code")),
                "question_id": _clean(row.get("question_id")),
                "var_code": _clean(row.get("var_code")),
                "source_table": _clean(row.get("source_table")),
                "response_value_raw": _clean(row.get("response_value_raw")),
                "response_value_normalized": _clean(row.get("response_value_normalized")),
                "response_label": _clean(row.get("response_label")),
                "source_row_hash": _clean(row.get("source_row_hash")),
                "current_directional_atom_eligible": _to_bool(
                    row.get("current_directional_atom_eligible"), False
                ),
                "directional_certification_status": _clean(
                    row.get("directional_certification_status")
                ),
                "directionality_authority_status": _clean(
                    row.get("directionality_authority_status")
                ),
                "response_option_map_matched": map_matched,
                "response_direction": _clean(row.get("response_direction")),
                "response_intensity": intensity,
                "directionality_stamp_status": (
                    "STAMPED" if not failures else "MISSING_OR_INCOMPLETE_STAMP"
                ),
                "directionality_stamp_failure_reason": "|".join(failures),
            }
        )

    audit = pd.DataFrame(rows, columns=DIRECTIONAL_STAMP_AUDIT_COLUMNS)
    return audit.sort_values(
        [
            "directionality_stamp_status",
            "source",
            "canonical_wave",
            "country_code",
            "question_id",
            "var_code",
            "source_row_hash",
        ],
        ascending=[True, True, True, True, True, True, True],
        kind="mergesort",
    ).reset_index(drop=True)


def summarize_v551_directionality_stamp_coverage(
    stamp_audit: pd.DataFrame,
) -> dict[str, Any]:
    """Summarize row-level directional stamping completeness."""
    expected_rows = int(len(stamp_audit))
    if expected_rows == 0:
        return {
            "directionality_expected_rows": 0,
            "directionality_stamped_rows": 0,
            "directionality_missing_stamp_rows": 0,
            "directionality_stamp_coverage": 1.0,
            "directionality_stamp_coverage_complete": True,
        }

    stamped_rows = int(
        stamp_audit["directionality_stamp_status"]
        .fillna("")
        .astype(str)
        .eq("STAMPED")
        .sum()
    )
    missing_rows = expected_rows - stamped_rows
    return {
        "directionality_expected_rows": expected_rows,
        "directionality_stamped_rows": stamped_rows,
        "directionality_missing_stamp_rows": missing_rows,
        "directionality_stamp_coverage": float(stamped_rows / expected_rows),
        "directionality_stamp_coverage_complete": bool(missing_rows == 0),
    }
