#!/usr/bin/env python3
"""Cross-stage extraction audit sidecar for V550/V551/V552."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import pandas as pd

from data.ddm_build_copy.ddm_v550_metrics import evidence_stratum_v2_from_row, numeric_wrapper_audit_from_row


EXTRACTION_AUDIT_SUMMARY_COLUMNS = [
    "run_id",
    "source",
    "wave",
    "canonical_wave",
    "country_code",
    "artifact_name",
    "evidence_stratum",
    "evidence_stratum_v2",
    "support_status",
    "confidence_tier",
    "row_count",
]


def _clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    return str(value).strip()


def _row_identity(row: pd.Series) -> dict[str, str]:
    return {
        "run_id": _clean(row.get("run_id") or row.get("source_run_id")),
        "source": _clean(row.get("source")),
        "wave": _clean(row.get("wave")),
        "canonical_wave": _clean(row.get("canonical_wave")),
        "country_code": _clean(row.get("country_code")),
    }


def _frame_summary(frame: pd.DataFrame, *, artifact_name: str) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(columns=EXTRACTION_AUDIT_SUMMARY_COLUMNS)
    rows: list[dict[str, Any]] = []
    for row in frame.itertuples(index=False):
        series = pd.Series(row._asdict())
        evidence_v2 = _clean(series.get("evidence_stratum_v2")) or evidence_stratum_v2_from_row(
            bridge_evidence_lane=series.get("bridge_evidence_lane", ""),
            semantic_role=series.get("semantic_role", ""),
            v551_relation_evidence_eligible=series.get("v551_relation_evidence_eligible"),
        )
        rows.append(
            {
                **_row_identity(series),
                "artifact_name": artifact_name,
                "evidence_stratum": _clean(series.get("evidence_stratum")),
                "evidence_stratum_v2": evidence_v2,
                "support_status": _clean(series.get("support_status")),
                "confidence_tier": _clean(series.get("confidence_tier")),
                "row_count": 1,
            }
        )
    frame_out = pd.DataFrame(rows)
    return (
        frame_out.groupby([column for column in EXTRACTION_AUDIT_SUMMARY_COLUMNS if column != "row_count"], dropna=False, observed=True)
        .agg(row_count=("row_count", "sum"))
        .reset_index()
    )


def _numeric_wrapper_audit(frame: pd.DataFrame, *, run_id: str = "") -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame()
    rows = []
    for row in frame.itertuples(index=False):
        series = pd.Series(row._asdict())
        audit = numeric_wrapper_audit_from_row(series)
        rows.append(
            {
                "run_id": run_id or _clean(series.get("run_id") or series.get("source_run_id")),
                "source": _clean(series.get("source")),
                "wave": _clean(series.get("wave")),
                "canonical_wave": _clean(series.get("canonical_wave")),
                "country_code": _clean(series.get("country_code")),
                "question_id": _clean(series.get("question_id")),
                "var_code": _clean(series.get("var_code")),
                "source_table": _clean(series.get("source_table")),
                "bridge_evidence_lane": _clean(series.get("bridge_evidence_lane")),
                "semantic_role": _clean(series.get("semantic_role")),
                "evidence_stratum": _clean(series.get("evidence_stratum")),
                "evidence_stratum_v2": _clean(series.get("evidence_stratum_v2")) or evidence_stratum_v2_from_row(
                    bridge_evidence_lane=series.get("bridge_evidence_lane", ""),
                    semantic_role=series.get("semantic_role", ""),
                    v551_relation_evidence_eligible=series.get("v551_relation_evidence_eligible"),
                ),
                "numeric_like_label": bool(audit.get("numeric_like_label")),
                "numeric_family_compatible": bool(audit.get("numeric_family_compatible")),
                "numeric_wrapper_status": _clean(audit.get("numeric_wrapper_status")),
                "numeric_wrapper_reason": _clean(audit.get("numeric_wrapper_reason")),
                "numeric_wrapper_confidence": _clean(audit.get("numeric_wrapper_confidence")),
                "support_status": _clean(series.get("support_status")),
                "confidence_tier": _clean(series.get("confidence_tier")),
                "v551_relation_evidence_eligible": bool(series.get("v551_relation_evidence_eligible", False)),
                "v551_exclusion_reason": _clean(series.get("v551_exclusion_reason")),
                "source_row_hash": _clean(series.get("source_row_hash")),
                "n_rows": 1,
            }
        )
    return pd.DataFrame(rows)


def _top_counts(frame: pd.DataFrame, column: str, *, limit: int = 5) -> list[dict[str, Any]]:
    if frame.empty or column not in frame.columns:
        return []
    counts = (
        frame[column]
        .fillna("")
        .astype(str)
        .value_counts(dropna=False)
        .head(limit)
    )
    return [{"value": str(index), "count": int(count)} for index, count in counts.items() if str(index).strip()]


def build_v550_552_extraction_audit_package(
    *,
    run_id: str,
    source: str,
    wave: str,
    canonical_wave: str,
    country_code: str,
    v550_outputs: dict[str, pd.DataFrame] | None = None,
    v551_outputs: dict[str, pd.DataFrame] | None = None,
    v552_outputs: dict[str, pd.DataFrame] | None = None,
    v550j_outputs: dict[str, pd.DataFrame] | None = None,
) -> dict[str, pd.DataFrame]:
    v550_outputs = v550_outputs or {}
    v551_outputs = v551_outputs or {}
    v552_outputs = v552_outputs or {}
    v550j_outputs = v550j_outputs or {}

    v551_audit = v551_outputs.get("numeric_wrapper_audit", pd.DataFrame())
    if v551_audit.empty and "bridge" in v551_outputs:
        v551_audit = _numeric_wrapper_audit(v551_outputs["bridge"], run_id=run_id)

    directionality_gap = v552_outputs.get("v552_directionality_gap_surface", pd.DataFrame())
    status_pressure = v552_outputs.get("v552_status_pressure_review_surface", pd.DataFrame())

    carry_forward = v550_outputs.get("question_carry_forward_summary", pd.DataFrame())
    if carry_forward.empty and "question_response_attitude_cloud" in v550_outputs:
        cloud = v550_outputs["question_response_attitude_cloud"]
        if not cloud.empty:
            carry_forward = pd.DataFrame(
                [
                    {
                        "run_id": run_id,
                        "source": source,
                        "wave": wave,
                        "canonical_wave": canonical_wave,
                        "country_code": country_code,
                        "artifact_name": "question_response_attitude_cloud",
                        "carry_forward_rows": int(len(cloud)),
                        "support_status": _clean(cloud.get("support_status", pd.Series(dtype="object")).iloc[0]) if "support_status" in cloud.columns and not cloud.empty else "",
                        "confidence_tier": _clean(cloud.get("confidence_tier", pd.Series(dtype="object")).iloc[0]) if "confidence_tier" in cloud.columns and not cloud.empty else "",
                    }
                ]
            )

    audit_manifest = {
        "run_id": run_id,
        "source": source,
        "wave": wave,
        "canonical_wave": canonical_wave,
        "country_code": country_code,
        "artifact_counts": {
            "v550_carry_forward_summary": int(len(carry_forward)),
            "v551_numeric_wrapper_audit": int(len(v551_audit)),
            "v552_directionality_gap_surface": int(len(directionality_gap)),
            "v552_status_pressure_review_surface": int(len(status_pressure)),
            "v550j_association_review_surface": int(len(v550j_outputs.get("joint_pattern_association_review_surface", pd.DataFrame()))),
        },
    }

    gap_counts: dict[str, int] = {}
    for frame, column in ((directionality_gap, "gap_surface_reason"), (status_pressure, "status_pressure_reason")):
        if not frame.empty and column in frame.columns:
            for value, count in frame[column].fillna("").astype(str).value_counts(dropna=False).items():
                if str(value).strip():
                    gap_counts[str(value)] = gap_counts.get(str(value), 0) + int(count)
    top_recoverable_gaps = [{"value": value, "count": count} for value, count in sorted(gap_counts.items(), key=lambda item: (-item[1], item[0]))[:5]]

    blocked_signal_audit = v551_outputs.get("blocked_signal_audit", pd.DataFrame())
    top_blocking_fields = _top_counts(blocked_signal_audit, "gate_name")
    if not top_blocking_fields:
        top_blocking_fields = _top_counts(blocked_signal_audit, "blocked_signal_reason")

    numeric_wrapper_failures = []
    if not v551_audit.empty and "numeric_wrapper_status" in v551_audit.columns:
        failures = v551_audit[v551_audit["numeric_wrapper_status"].astype(str).ne("wrapped_numeric")]
        numeric_wrapper_failures = _top_counts(failures, "numeric_wrapper_reason")

    readiness = {
        "run_id": run_id,
        "source": source,
        "wave": wave,
        "canonical_wave": canonical_wave,
        "country_code": country_code,
        "overall_status": "ready" if (not v551_audit.empty or not directionality_gap.empty or not status_pressure.empty) else "review_only",
        "certified_count": int(len(v551_outputs.get("relation_evidence_atoms", pd.DataFrame()))),
        "reviewable_count": int(len(v551_outputs.get("relation_review_surface", pd.DataFrame())) + len(status_pressure)),
        "blocked_count": int(len(v551_outputs.get("blocked_signal_audit", pd.DataFrame()))),
        "provisional_count": int(len(directionality_gap)),
        "mapping_pending_count": 0,
        "directionality_pending_count": int(len(directionality_gap)),
        "numeric_only_count": int(len(v551_audit[v551_audit.get("numeric_wrapper_status", pd.Series(dtype="object")).astype(str).eq("wrapped_numeric")])) if not v551_audit.empty and "numeric_wrapper_status" in v551_audit.columns else 0,
        "proxy_only_count": 0,
        "status_only_count": int(len(status_pressure)),
        "carry_forward_context_count": int(len(carry_forward)),
        "unsafe_for_downstream_count": int(len(v551_outputs.get("blocked_signal_audit", pd.DataFrame()))),
        "top_recoverable_gaps": top_recoverable_gaps,
        "top_blocking_fields": top_blocking_fields,
        "numeric_wrapper_failures": numeric_wrapper_failures,
        "recommended_next_repairs": [],
    }

    return {
        "manifest": pd.DataFrame([audit_manifest]),
        "readiness_report": pd.DataFrame([readiness]),
        "v550_carry_forward_summary": carry_forward,
        "v551_numeric_wrapper_audit": v551_audit,
        "v552_directionality_gap_surface": directionality_gap,
        "v552_status_pressure_review_surface": status_pressure,
        "v550_552_numeric_wrapper_audit": _numeric_wrapper_audit(v551_outputs.get("bridge", pd.DataFrame()), run_id=run_id),
    }
