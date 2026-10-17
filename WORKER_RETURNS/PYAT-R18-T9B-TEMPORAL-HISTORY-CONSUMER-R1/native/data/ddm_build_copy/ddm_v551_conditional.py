#!/usr/bin/env python3
"""Helpers for compiling conditional determinicity outputs from V551 bridge rows."""

from __future__ import annotations

import hashlib
import json
from typing import Any

import pandas as pd

from data.ddm_build_copy.ddm_v550_manifest import utc_now
from data.ddm_build_copy.ddm_v550_schema import (
    CONDITIONAL_DETERMINICITY_INDEX_SCHEMA,
    V551_ATOM_EXCLUSION_AUDIT_SCHEMA,
    validate_columns,
)
from data.ddm_build_copy.ddm_v551_atoms import MIN_ATOM_SUPPORT, SOURCE_TABLE_PRIORITY
from data.ddm_build_copy.ddm_v550_support import support_status_from_count, support_threshold_from_total

CONDITIONAL_DETERMINICITY_SCHEMA_VERSION = "v1"


def _clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    return str(value).strip()


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
    if text in {"0", "false", "f", "no", "n", "off", "", "nan", "none"}:
        return False
    return default


def _safe_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        parsed = float(value)
        if pd.isna(parsed):
            return None
        return parsed
    except Exception:
        return None


def _hash_payload(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _support_status(value: Any) -> str:
    return support_status_from_count(value, support_cap=MIN_ATOM_SUPPORT)


def _row_value(series: pd.Series, name: str, default: Any = "") -> Any:
    if name not in series.index:
        return default
    value = series.get(name, default)
    if pd.isna(value):
        return default
    return value


def _exclusion_row(series: pd.Series, gate_name: str, exclusion_reason: str) -> dict[str, Any]:
    return {
        "source": _clean(series.get("source")),
        "canonical_wave": _clean(series.get("canonical_wave")),
        "country_code": _clean(series.get("country_code")),
        "question_id": _clean(series.get("question_id")),
        "var_code": _clean(series.get("var_code")),
        "source_table": _clean(series.get("source_table")),
        "gate_name": gate_name,
        "exclusion_reason": exclusion_reason,
        "n_rows": 1,
        "sample_source_row_hash": _clean(series.get("source_row_hash")),
    }


def _conditional_row(series: pd.Series, *, source_run_id: str = "") -> dict[str, Any]:
    support_value = _safe_float(series.get("n_unweighted"))
    if support_value is None:
        support_value = 0.0
    directional_mask = _clean(series.get("response_direction")) != "" and _safe_float(series.get("response_intensity")) is not None
    support_basis = "directional_intensity" if directional_mask else "support_only"
    compiler_status = "populated" if directional_mask else "insufficient_directionality"
    return {
        "conditional_id": _hash_payload({
            "source": _clean(series.get("source")),
            "wave": _clean(series.get("wave")),
            "country_code": _clean(series.get("country_code")),
            "question_id": _clean(series.get("question_id")),
            "var_code": _clean(series.get("var_code")),
            "source_row_hash": _clean(series.get("source_row_hash")),
        }),
        "source": _clean(series.get("source")),
        "wave": _clean(series.get("wave")),
        "canonical_wave": _clean(series.get("canonical_wave")),
        "country_code": _clean(series.get("country_code")),
        "question_id": _clean(series.get("question_id")),
        "var_code": _clean(series.get("var_code")),
        "source_table": _clean(series.get("source_table")),
        "bridge_evidence_lane": _clean(series.get("bridge_evidence_lane")),
        "semantic_role": _clean(series.get("semantic_role")),
        "response_value_normalized": _clean(series.get("response_value_normalized")),
        "response_label": _clean(series.get("response_label")),
        "normalized_response_label": _clean(series.get("normalized_response_label")),
        "response_family": _clean(series.get("response_family")),
        "response_direction": _clean(series.get("response_direction")),
        "response_intensity": _row_value(series, "response_intensity", default=None),
        "directionality_status": _clean(series.get("directionality_status")) or "unknown",
        "response_semantics_status": _clean(series.get("response_semantics_status")) or "observed_only",
        "response_semantics_source": _clean(series.get("response_semantics_source")) or "observed_response_row",
        "response_semantics_contract_hash": _clean(series.get("response_semantics_contract_hash")),
        "support_status": _clean(series.get("support_status")) or _support_status(series.get("n_unweighted")),
        "v551_conditional_determinicity_eligible": True,
        "question_type": _clean(series.get("question_type")),
        "handling_rule": _clean(series.get("handling_rule")),
        "recommended_computation": _clean(series.get("recommended_computation")),
        "source_structure_classification": _clean(series.get("source_structure_classification")),
        "source_structure_basis": _clean(series.get("source_structure_basis")),
        "source_structure_confidence": _clean(series.get("source_structure_confidence")),
        "source_structure_source": _clean(series.get("source_structure_source")),
        "source_structure_fields_joined": _to_bool(series.get("source_structure_fields_joined"), False),
        "question_use_contract_joined": _to_bool(series.get("question_use_contract_joined"), False),
        "relation_axis_id": _clean(series.get("relation_axis_id")),
        "target_entity_id": _clean(series.get("target_entity_id")),
        "driver_facet_id": _clean(series.get("driver_facet_id")),
        "n_unweighted": support_value,
        "n_weighted": _safe_float(series.get("n_weighted")) or support_value,
        "pct_unweighted": _safe_float(series.get("pct_unweighted")) or 0.0,
        "pct_weighted": _safe_float(series.get("pct_weighted")) or 0.0,
        "support_basis": support_basis,
        "compiler_status": compiler_status,
        "source_row_hash": _clean(series.get("source_row_hash")),
        "source_run_id": _clean(source_run_id or series.get("run_id")),
        "compiled_at": utc_now(),
        "schema_version": CONDITIONAL_DETERMINICITY_SCHEMA_VERSION,
    }


def build_conditional_determinicity_index(
    bridge: pd.DataFrame,
    *,
    source_run_id: str = "",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if bridge.empty:
        return (
            pd.DataFrame(columns=CONDITIONAL_DETERMINICITY_INDEX_SCHEMA["required_columns"]),
            pd.DataFrame(columns=V551_ATOM_EXCLUSION_AUDIT_SCHEMA["required_columns"]),
        )
    if "bridge_evidence_lane" not in bridge.columns:
        exclusions = [
            _exclusion_row(row if isinstance(row, pd.Series) else pd.Series(row._asdict()), "bridge_evidence_lane", "missing_bridge_evidence_lane")
            for row in bridge.itertuples(index=False)
        ]
        return (
            pd.DataFrame(columns=CONDITIONAL_DETERMINICITY_INDEX_SCHEMA["required_columns"]),
            pd.DataFrame(exclusions, columns=V551_ATOM_EXCLUSION_AUDIT_SCHEMA["required_columns"]),
        )
    if "v551_conditional_determinicity_eligible" not in bridge.columns:
        exclusions = [
            _exclusion_row(row if isinstance(row, pd.Series) else pd.Series(row._asdict()), "v551_eligibility", "missing_bridge_conditional_determinicity_eligibility_field")
            for row in bridge.itertuples(index=False)
        ]
        return (
            pd.DataFrame(columns=CONDITIONAL_DETERMINICITY_INDEX_SCHEMA["required_columns"]),
            pd.DataFrame(exclusions, columns=V551_ATOM_EXCLUSION_AUDIT_SCHEMA["required_columns"]),
        )

    bridge = bridge.copy()
    bridge["_source_table_priority"] = bridge.get("source_table", pd.Series([""] * len(bridge), index=bridge.index)).map(lambda value: SOURCE_TABLE_PRIORITY.get(_clean(value), 99))
    prioritized = bridge.sort_values(["_source_table_priority", "source", "canonical_wave", "country_code", "question_id", "var_code", "source_row_hash"], kind="mergesort").reset_index(drop=True)

    rows: list[dict[str, Any]] = []
    exclusions: list[dict[str, Any]] = []
    seen_keys: set[str] = set()

    for row in prioritized.itertuples(index=False):
        series = pd.Series(row._asdict())
        if not _to_bool(series.get("v551_conditional_determinicity_eligible"), False):
            exclusions.append(_exclusion_row(series, "v551_eligibility", _clean(series.get("v551_exclusion_reason")) or "not_conditional_determinicity_eligible"))
            continue
        if _clean(series.get("bridge_evidence_lane")) != "derived_determinicity":
            exclusions.append(_exclusion_row(series, "bridge_evidence_lane", "not_derived_determinicity_lane"))
            continue
        if not _to_bool(series.get("question_use_contract_joined"), False):
            exclusions.append(_exclusion_row(series, "question_use_contract", "question_use_contract_not_joined"))
            continue
        if not _to_bool(series.get("source_structure_fields_joined"), False):
            exclusions.append(_exclusion_row(series, "source_structure_fields", "source_structure_fields_not_joined"))
            continue
        bridge_support_status = _clean(series.get("support_status")) or support_status_from_count(
            series.get("n_unweighted"),
            total_respondents=series.get("n_respondents"),
            support_cap=MIN_ATOM_SUPPORT,
        )
        if bridge_support_status != "sufficient_support":
            exclusions.append(_exclusion_row(series, "support_status", f"{bridge_support_status or 'missing_support'}_not_sufficient"))
            continue
        conditional_key = "|".join([
            _clean(series.get("source")),
            _clean(series.get("wave")),
            _clean(series.get("canonical_wave")),
            _clean(series.get("country_code")),
            _clean(series.get("question_id")),
            _clean(series.get("var_code")),
            _clean(series.get("source_row_hash")),
        ])
        if conditional_key in seen_keys:
            exclusions.append(_exclusion_row(series, "conditional_dedupe", "duplicate_conditional_determinicity"))
            continue
        seen_keys.add(conditional_key)
        rows.append(_conditional_row(series, source_run_id=source_run_id))

    index_df = pd.DataFrame(rows, columns=CONDITIONAL_DETERMINICITY_INDEX_SCHEMA["required_columns"])
    exclusion_df = pd.DataFrame(exclusions, columns=V551_ATOM_EXCLUSION_AUDIT_SCHEMA["required_columns"])
    if not index_df.empty:
        index_df = index_df.sort_values(["source", "canonical_wave", "country_code", "question_id", "var_code", "conditional_id"], kind="mergesort").reset_index(drop=True)
    return index_df, exclusion_df


def validate_conditional_determinicity_index(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, CONDITIONAL_DETERMINICITY_INDEX_SCHEMA["required_columns"], "conditional_determinicity_index")


def validate_conditional_determinicity_exclusion_audit(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V551_ATOM_EXCLUSION_AUDIT_SCHEMA["required_columns"], "conditional_determinicity_exclusion_audit")
