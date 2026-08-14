#!/usr/bin/env python3
"""Helpers for compiling V552 structural DDM outputs from V551 atoms."""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import dataclass
from typing import Any, Mapping

import pandas as pd

from data.ddm_build_copy.ddm_v550_support import confidence_tier_from_support, support_status_from_count, support_threshold_from_total
from data.ddm_build_copy.ddm_v552_contract import (
    recompute_v552_dominant_orientation,
    recompute_v552_observation_state,
    recompute_v552_pressure_component_id,
    recompute_v552_pressure_observation_id,
    recompute_v552_response_surface_signature,
    recompute_v552_v2_1_4_component_measurement_hash,
    recompute_v552_v2_1_4_pressure_measurement_hash,
    v552_component_identity_payload,
    v552_observation_identity_payload,
    v552_response_surface_payload,
)
from data.ddm_build_copy.ddm_v550_schema import (
    V552_CONDITIONAL_DETERMINICITY_STATUS_AUDIT_SCHEMA,
    V552_PRESSURE_COMPONENT_INDEX_SCHEMA,
    V552_PRESSURE_OBSERVATION_AUDIT_SCHEMA,
    V552_PRESSURE_OBSERVATION_INDEX_SCHEMA,
    V552_CONTRADICTION_TENSOR_SCHEMA,
    V552_CONTRADICTION_SURFACE_SCHEMA,
    V552_COUNTRY_WAVE_PRESSURE_PROFILE_SCHEMA,
    V552_AGGREGATE_PROJECTION_SURFACE_SCHEMA,
    V552_DRIVER_FACET_PRESSURE_SCHEMA,
    V552_DRIVER_SEMANTIC_PROFILE_SCHEMA,
    V552_HORIZON_CONSTRAINT_INDEX_SCHEMA,
    V552_HORIZON_SEMANTIC_PROFILE_SCHEMA,
    V552_POSITION_CONDITIONING_PROFILE_SCHEMA,
    V552_PARENT_ATTITUDE_PRIOR_SCHEMA,
    V552_PARENT_BEHAVIOR_TENDENCY_PRIOR_SCHEMA,
    V552_PARENT_CONTRADICTION_PRIOR_SCHEMA,
    V552_PARENT_POSITION_PRIOR_SCHEMA,
    V552_PARENT_PRIOR_MANIFEST_SCHEMA,
    V552_READINESS_REPORT_SCHEMA,
    V552_STRUCTURAL_FACT_INDEX_SCHEMA,
    V552_TEMPORAL_KEY_SOURCE_INDEX_SCHEMA,
    V552_TO_V552J_HANDOFF_INDEX_SCHEMA,
    V552_RELATION_AXIS_PRESSURE_SCHEMA,
    V552_DIRECTIONALITY_COVERAGE_AUDIT_SCHEMA,
    V552_DIRECTIONALITY_GAP_SURFACE_SCHEMA,
    V552_STATUS_AUDIT_SCHEMA,
    V552_STATUS_PRESSURE_REVIEW_SCHEMA,
    V552_FACET_SEMANTIC_PROFILE_SCHEMA,
    V552_ARTIFACT_AUTHORITY_INDEX_SCHEMA,
    V552_KNOWN_ABSENCE_REGISTER_SCHEMA,
    V552_STRUCTURAL_CHANNEL_INDEX_SCHEMA,
    V552_QUESTION_SEMANTIC_HIERARCHY_SCHEMA,
    V552_STRATUM_SEMANTIC_PROFILE_SCHEMA,
    V552_TARGET_ENTITY_PRESSURE_SCHEMA,
    validate_columns,
)

V552_SCHEMA_VERSION = "v1"
V552_HANOFF_SCHEMA_VERSION = "v552_structural_handoff_v1"
V552_ALLOWED_FINAL_STATUSES = {
    "STATUS: READY_V552_STRUCTURAL_HANDOFF",
    "STATUS: READY_V552_STATUS_ONLY_INSUFFICIENT_DIRECTIONALITY",
    "STATUS: READY_V552_EMPTY_NO_ATOMS",
    "STATUS: NOT_READY_MISSING_ATOMS_PATH",
    "STATUS: NOT_READY_ATOMS_UNREADABLE",
    "STATUS: NOT_READY_REQUIRED_COLUMNS_MISSING",
    "STATUS: NOT_READY_STRUCTURAL_GROUPING_MISSING",
    "STATUS: NOT_READY_OUTPUT_SCHEMA_VIOLATION",
    "STATUS: NOT_READY_SCOPE_CONFLICT_REQUIRES_UPSTREAM_CHANGE",
    "STATUS: NOT_READY_TEST_FAILURES",
    "STATUS: NOT_READY_IMPLEMENTATION_INCOMPLETE",
}
V552_ALLOWED_ARTIFACT_STATUSES = {
    "populated",
    "empty_no_relation_evidence_atoms",
    "insufficient_directionality",
    "support_summary_only",
    "insufficient_grouping",
    "insufficient_opposing_directionality",
    "status_only_conditional_input",
    "not_applicable",
    "error_missing_required_columns",
    "error_unreadable_input",
    "review_required",
}
V552_ALLOWED_DIRECTIONALITY_ROLLUPS = {
    "full_directionality",
    "partial_directionality",
    "no_directionality",
    "not_applicable",
}
V552_ALLOWED_DIRECTIONALITY_GAP_REASONS = {
    "no_directionality",
    "partial_directionality",
}
V552_ALLOWED_STATUS_PRESSURE_REASONS = {
    "support_without_directionality",
    "status_pressure_with_partial_directionality",
    "support_gap_no_directionality",
    "support_gap_partial_directionality",
}
V552_ALLOWED_STATUS_PRESSURE_STATUSES = {
    "review_required",
    "support_summary_only",
}


def _clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    return str(value).strip()


def _to_float(value: Any) -> float | None:
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


def _json_text(value: Any) -> str:
    if value is None:
        return "[]"
    if isinstance(value, str):
        token = value.strip()
        return token if token else "[]"
    try:
        if pd.isna(value):
            return "[]"
    except Exception:
        pass
    if isinstance(value, (list, tuple, set)):
        return json.dumps([item for item in value], sort_keys=True, ensure_ascii=False, default=str)
    if isinstance(value, dict):
        return json.dumps(value, sort_keys=True, ensure_ascii=False, default=str)
    return json.dumps([value], sort_keys=True, ensure_ascii=False, default=str)


def _preferred_text(source_row: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = _clean(source_row.get(key))
        if value:
            return value
    return ""


def _row_absences(source_row: dict[str, Any], required_keys: list[str]) -> list[str]:
    missing: list[str] = []
    for key in required_keys:
        if not _preferred_text(source_row, key):
            missing.append(key)
    return missing


def _source_row_hash(source_row: dict[str, Any]) -> str:
    return _hash_payload({"source_row": {key: source_row.get(key) for key in sorted(source_row.keys())}})


def _stable_source_row_id(source_artifact: str, source_row: dict[str, Any], source_row_index: int) -> str:
    source_row_id = _preferred_text(
        source_row,
        "source_row_id",
        "row_id",
        "atom_id",
        "question_id",
        "var_code",
        "question_use_contract_id",
    )
    if not source_row_id:
        source_row_id = f"{source_artifact}__row_{source_row_index}"
    return source_row_id


def _structural_fact_lane_and_grain(source_artifact: str, source_row: dict[str, Any]) -> tuple[str, str]:
    artifact = _clean(source_artifact)
    if artifact in {"question_semantic_hierarchy", "relation_axis_pressure", "target_entity_pressure", "driver_facet_pressure", "structural_channel_index", "horizon_constraint_index"}:
        lane = "row_level_structural_fact"
    elif artifact == "position_conditioning_profile":
        lane = "profile_context_fact"
    elif artifact == "country_wave_pressure_profile":
        lane = "country_wave_context_fact"
    elif artifact in {"contradiction_surface", "aggregate_projection_surface"}:
        lane = "audit_fact"
    else:
        lane = "not_temporal_key_source"

    if artifact == "relation_axis_pressure":
        grain = "relation_axis_level"
    elif artifact == "target_entity_pressure":
        grain = "target_entity_level"
    elif artifact == "driver_facet_pressure":
        grain = "driver_facet_level"
    elif artifact == "structural_channel_index":
        grain = "structural_channel_level"
    elif artifact == "horizon_constraint_index":
        grain = "horizon_constraint_level"
    elif artifact == "position_conditioning_profile":
        grain = "profile_context"
    elif artifact == "country_wave_pressure_profile":
        grain = "country_wave_context"
    elif artifact in {"contradiction_surface", "aggregate_projection_surface"}:
        grain = "audit"
    elif artifact == "question_semantic_hierarchy":
        grain = "question_level"
    else:
        grain = "not_temporal_key_source"
    return lane, grain


def _structural_temporal_key_candidate_status(
    *,
    structural_fact_lane: str,
    structural_fact_grain: str,
    relation_axis_id: str,
    target_entity_id: str,
    driver_facet_id: str,
    structural_channel_id: str,
    horizon_constraint_id: str,
    question_id: str,
) -> tuple[str, str, str, bool, bool]:
    resolved_dims = [value for value in [relation_axis_id, target_entity_id, driver_facet_id, structural_channel_id, horizon_constraint_id] if value]
    if structural_fact_lane == "audit_fact" or structural_fact_lane == "not_temporal_key_source":
        return "blocked", "not_temporal_key_source", "not_temporal_key_source", False, False
    if structural_fact_grain == "horizon_constraint_level" and all([relation_axis_id, target_entity_id, driver_facet_id, structural_channel_id, horizon_constraint_id]):
        return "resolved", "resolved_temporal_key", "horizon_constraint_level", True, False
    if structural_fact_grain == "structural_channel_level" and all([relation_axis_id, target_entity_id, driver_facet_id, structural_channel_id]):
        return "resolved", "resolved_temporal_key", "structural_channel_level", True, False
    if structural_fact_grain == "relation_axis_level" and relation_axis_id:
        return "resolved", "resolved_temporal_key", "relation_axis_level", True, False
    if structural_fact_grain == "target_entity_level" and target_entity_id:
        return "resolved", "resolved_temporal_key", "target_entity_level", True, False
    if structural_fact_grain == "driver_facet_level" and driver_facet_id:
        return "resolved", "resolved_temporal_key", "driver_facet_level", True, False
    if structural_fact_grain == "question_level" and question_id:
        return "probe_only", "question_level_probe", "question_level", bool(resolved_dims), False
    if resolved_dims:
        return "probe_only", "fallback_probe_only", structural_fact_grain or "unknown_grain", True, False
    return "blocked", "missing_structural_dimensions", structural_fact_grain or "missing", False, False


def compute_input_hash(path: str | Path | None) -> str:
    if not path:
        return "empty"
    path_obj = Path(path)
    if not path_obj.exists():
        return "missing"
    try:
        return hashlib.sha256(path_obj.read_bytes()).hexdigest()
    except Exception:
        return "unreadable"


def normalize_v552_status(status: Any) -> str:
    text = _clean(status)
    if not text:
        return ""
    upper = text.upper().replace(" ", "_")
    if not upper.startswith("STATUS:"):
        upper = f"STATUS: {upper}"
    if upper in V552_ALLOWED_FINAL_STATUSES:
        return upper
    lowered = text.lower()
    if lowered in V552_ALLOWED_ARTIFACT_STATUSES:
        return lowered
    if lowered in V552_ALLOWED_DIRECTIONALITY_ROLLUPS:
        return lowered
    return text


def empty_v552_artifact(required_columns: list[str]) -> pd.DataFrame:
    return pd.DataFrame(columns=required_columns)


def _confidence_tier_from_support(n_unweighted: float, total_respondents: Any = None) -> str:
    return confidence_tier_from_support(n_unweighted, total_respondents=total_respondents)


def _support_status_from_support(n_unweighted: float, total_respondents: Any = None) -> str:
    return support_status_from_count(n_unweighted, total_respondents=total_respondents)


def _entropy(values: pd.Series) -> float:
    if values.empty:
        return 0.0
    counts = values.value_counts(dropna=True)
    total = float(counts.sum())
    if total <= 0:
        return 0.0
    ent = 0.0
    for count in counts.tolist():
        p = float(count) / total
        if p > 0:
            ent -= p * math.log(p, 2)
    return float(ent)


def _dominant_orientation(values: pd.Series) -> tuple[str, float]:
    cleaned = values.fillna("").astype(str).str.strip()
    cleaned = cleaned[cleaned.ne("")]
    if cleaned.empty:
        return "", 0.0
    counts = cleaned.value_counts()
    top = counts.index[0]
    share = float(counts.iloc[0]) / float(counts.sum())
    return str(top), share


def _mean_numeric(series: pd.Series) -> float | None:
    parsed = pd.to_numeric(series, errors="coerce")
    if parsed.notna().any():
        return float(parsed.mean())
    return None


def _direction_sign(value: Any) -> int:
    text = _clean(value).lower()
    if not text:
        return 0
    if text in {"positive", "ascending", "high", "up", "increase", "more", "pro", "yes", "agree", "support"}:
        return 1
    if text in {"negative", "descending", "low", "down", "decrease", "less", "contra", "no", "disagree", "oppose"}:
        return -1
    if "positive" in text or "ascending" in text or "agree" in text or "high" in text:
        return 1
    if "negative" in text or "descending" in text or "disagree" in text or "low" in text:
        return -1
    return 0


def _directionality_frame(group: pd.DataFrame) -> tuple[pd.Series, pd.Series, float]:
    directions = _direction_mask(group.get("response_direction", pd.Series(dtype=object)))
    intensities = pd.to_numeric(group.get("response_intensity", pd.Series(dtype=object)), errors="coerce")
    usable = directions.ne("") & intensities.notna()
    coverage = float(usable.mean()) if len(group) else 0.0
    return directions, intensities, coverage


def _parse_weighted_strata(value: Any) -> list[str]:
    text = _clean(value)
    if not text:
        return []
    entries: list[tuple[str, float, int]] = []
    for idx, part in enumerate(text.split("|")):
        piece = _clean(part)
        if not piece:
            continue
        label, _, weight_text = piece.partition(":")
        label = _clean(label)
        if not label:
            continue
        weight = _to_float(weight_text)
        entries.append((label, float(weight) if weight is not None else 0.0, idx))
    entries.sort(key=lambda item: (-item[1], item[2], item[0]))
    ordered: list[str] = []
    for label, _, _ in entries:
        if label and label not in ordered:
            ordered.append(label)
    return ordered


def _conditional_strata_path(value: Any) -> str:
    return "|".join(_parse_weighted_strata(value))


def _position_conditioning_profile_id(row: dict[str, Any]) -> str:
    payload = {
        "source": row.get("source", ""),
        "wave": row.get("wave", ""),
        "canonical_wave": row.get("canonical_wave", ""),
        "country_code": row.get("country_code", ""),
        "position_conditioning": row.get("position_conditioning", ""),
        "position_modifiers": row.get("position_modifiers", ""),
        "strata_path": row.get("strata_path", ""),
        "horizon_affordance": row.get("horizon_affordance", ""),
        "position_conditioning_confidence": row.get("position_conditioning_confidence", ""),
    }
    return _hash_payload(payload)


def _first_nonempty(values: pd.Series | list[Any] | tuple[Any, ...]) -> str:
    if isinstance(values, pd.Series):
        iterable = values.fillna("").astype(str).tolist()
    else:
        iterable = [str(value).strip() if value is not None else "" for value in values]
    for value in iterable:
        cleaned = _clean(value)
        if cleaned:
            return cleaned
    return ""


def _join_unique(values: pd.Series | list[Any] | tuple[Any, ...], *, separator: str = "|") -> str:
    if isinstance(values, pd.Series):
        iterable = values.fillna("").astype(str).tolist()
    else:
        iterable = [str(value).strip() if value is not None else "" for value in values]
    ordered: list[str] = []
    for value in iterable:
        cleaned = _clean(value)
        if cleaned and cleaned not in ordered:
            ordered.append(cleaned)
    return separator.join(ordered)


def _infer_horizon_type(horizon_affordance: Any, semantic_subrole: Any = "", semantic_tags: Any = "", strata_path: Any = "") -> str:
    text = " ".join([_clean(horizon_affordance), _clean(semantic_subrole), _clean(semantic_tags), _clean(strata_path)]).lower()
    if not text or text in {"none", "no", "na", "n/a"}:
        return "local"
    if any(token in text for token in ["collapse", "collapse_risk", "futility", "despair", "absence"]):
        return "collapse"
    if any(token in text for token in ["absolute", "ultimate", "universal", "transcend", "redempt", "salvation", "all"]):
        return "absolute"
    if any(token in text for token in ["bounded", "elect", "exclusive", "exclusion", "sect", "party", "family", "self", "household", "nation", "neighborhood"]):
        return "bounded"
    return "local"


def _infer_horizon_scope(strata_path: Any, position_modifiers: Any = "", horizon_affordance: Any = "") -> str:
    text = " ".join([_clean(strata_path), _clean(position_modifiers), _clean(horizon_affordance)]).lower()
    if not text:
        return ""
    for scope in ["self", "family", "neighborhood_household", "neighborhood", "household", "nation_state", "nation", "sect_ethno_class", "party_movement", "planetary", "imperial_block", "sub_national_region"]:
        if scope in text:
            return scope
    return ""


def _infer_horizon_openness(horizon_type: str, horizon_affordance: Any = "") -> str:
    text = _clean(horizon_affordance).lower()
    if horizon_type == "absolute":
        return "open"
    if horizon_type == "collapse":
        return "collapsed"
    if any(token in text for token in ["elect", "exclusive", "exclusion"]):
        return "elect-only" if "elect" in text else "exclusionary"
    if any(token in text for token in ["bounded", "family", "self", "household", "nation", "sect", "party", "neighborhood"]):
        return "bounded"
    return "open" if horizon_affordance else "collapsed"


def _infer_horizon_valence(horizon_affordance: Any, semantic_tags: Any = "") -> str:
    text = " ".join([_clean(horizon_affordance), _clean(semantic_tags)]).lower()
    if any(token in text for token in ["collapse", "despair", "futility", "absence"]):
        return "collapsed"
    if any(token in text for token in ["hope", "redempt", "solidarity", "compassion", "futur", "repair", "durable"]):
        return "hopeful"
    if any(token in text for token in ["resilien", "endur", "steadfast", "surviv"]):
        return "resilient"
    return "neutral"


def _infer_translation_status(horizon_affordance: Any, semantic_tags: Any = "") -> str:
    text = " ".join([_clean(horizon_affordance), _clean(semantic_tags)]).lower()
    if any(token in text for token in ["god", "salvation", "elect", "theological", "christ", "religious"]):
        return "requires_translation"
    return "translated"


def _direction_mask(series: pd.Series) -> pd.Series:
    cleaned = series.fillna("").astype(str).str.strip()
    cleaned = cleaned.mask(cleaned.str.lower().isin(["nan", "none"]), "")
    return cleaned


def _group_frame(df: pd.DataFrame, group_cols: list[str]) -> pd.core.groupby.DataFrameGroupBy:
    return df.groupby(group_cols, dropna=False, sort=True)


def _group_total_respondents(group: pd.DataFrame) -> float | None:
    if "n_respondents" not in group.columns:
        return None
    parsed = pd.to_numeric(group["n_respondents"], errors="coerce").dropna()
    if parsed.empty:
        return None
    return float(parsed.iloc[0])


def _common_group_columns(df: pd.DataFrame) -> list[str]:
    cols = [column for column in ["source", "wave", "canonical_wave", "country_code"] if column in df.columns]
    return cols


def _has_columns(df: pd.DataFrame, columns: list[str]) -> bool:
    return all(column in df.columns for column in columns)


def _group_label(value: Any) -> str:
    return _clean(value)


def _group_context(group: pd.DataFrame) -> dict[str, str]:
    first = group.iloc[0].to_dict()
    return {
        "run_id": _clean(first.get("run_id") or first.get("source_run_id")),
        "source": _clean(first.get("source")),
        "wave": _clean(first.get("wave")),
        "canonical_wave": _clean(first.get("canonical_wave")),
        "country_code": _clean(first.get("country_code")),
    }


def _base_group_row(
    group: pd.DataFrame,
    *,
    group_cols: list[str],
    basis: str,
    status: str,
    run_id: str = "",
) -> dict[str, Any]:
    first = group.iloc[0].to_dict()
    n_atoms = int(len(group))
    n_unweighted = float(pd.to_numeric(group.get("n_unweighted", pd.Series([0] * len(group), index=group.index)), errors="coerce").fillna(0).sum())
    n_weighted = pd.to_numeric(group.get("n_weighted", pd.Series([0.0] * len(group), index=group.index)), errors="coerce").fillna(0).sum()
    total_respondents = _group_total_respondents(group)
    directions, intensities, directionality_coverage = _directionality_frame(group)
    directional_mask = directions.ne("") & intensities.notna()
    if directional_mask.any():
        signed = intensities.loc[directional_mask] * directions.loc[directional_mask].map(_direction_sign).astype(float)
        pressure_score = float(signed.mean()) if not signed.empty else None
        support_basis = "directional_intensity"
        compiler_status = status
    else:
        pressure_score = None
        support_basis = "support_only"
        compiler_status = "insufficient_directionality"
    orientation, orientation_share = _dominant_orientation(group.get("response_direction", pd.Series(dtype=object)))
    entropy = _entropy(group.get("response_direction", pd.Series(dtype=object)))
    return {
        "run_id": run_id or _clean(first.get("run_id") or first.get("source_run_id")),
        **{col: _clean(first.get(col)) for col in group_cols},
        "n_atoms": n_atoms,
        "n_unweighted_total": float(n_unweighted),
        "n_weighted_total": float(n_weighted),
        "pressure_score": pressure_score,
        "entropy": float(entropy),
        "polarization_index": float(max(0.0, 1.0 - orientation_share)),
        "dominant_orientation": orientation,
        "support_status": _support_status_from_support(n_unweighted, total_respondents=total_respondents),
        "confidence_tier": _confidence_tier_from_support(n_unweighted, total_respondents=total_respondents),
        "basis": basis,
        "status": compiler_status,
        "pressure_computation_status": compiler_status,
        "directionality_coverage": float(directionality_coverage),
        "support_basis": support_basis,
        "compiler_status": compiler_status,
        "input_atom_count": int(len(group)),
        "eligible_atom_count": int(len(group)),
        "input_atom_hash": _hash_payload({"rows": group.get("atom_id", pd.Series(dtype=str)).fillna("").astype(str).tolist()}),
        "input_hash": _hash_payload({
            "run_id": run_id or _clean(first.get("run_id") or first.get("source_run_id")),
            "basis": basis,
            "rows": group.get("atom_id", pd.Series(dtype=str)).fillna("").astype(str).tolist(),
        }),
        "created_at": pd.Timestamp.utcnow().isoformat(),
        "schema_version": V552_SCHEMA_VERSION,
    }


def build_relation_axis_pressure(atoms: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    if atoms.empty or not _has_columns(atoms, ["relation_axis_id"]):
        return pd.DataFrame(columns=V552_RELATION_AXIS_PRESSURE_SCHEMA["required_columns"])
    group_cols = _common_group_columns(atoms) + ["relation_axis_id"]
    rows = []
    for _, group in _group_frame(atoms, group_cols):
        row = _base_group_row(group, group_cols=group_cols, basis="v551_atoms", status="populated", run_id=run_id)
        row["input_hash"] = row["input_atom_hash"]
        row["run_id"] = run_id or row["run_id"]
        rows.append(row)
    return pd.DataFrame(rows, columns=V552_RELATION_AXIS_PRESSURE_SCHEMA["required_columns"])


def build_target_entity_pressure(atoms: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    if atoms.empty or not _has_columns(atoms, ["target_entity_id"]):
        return pd.DataFrame(columns=V552_TARGET_ENTITY_PRESSURE_SCHEMA["required_columns"])
    group_cols = _common_group_columns(atoms) + ["target_entity_id"]
    rows = []
    for _, group in _group_frame(atoms, group_cols):
        row = _base_group_row(group, group_cols=group_cols, basis="v551_atoms", status="populated", run_id=run_id)
        row["input_hash"] = row["input_atom_hash"]
        row["run_id"] = run_id or row["run_id"]
        rows.append(row)
    return pd.DataFrame(rows, columns=V552_TARGET_ENTITY_PRESSURE_SCHEMA["required_columns"])


def build_driver_facet_pressure(atoms: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    if atoms.empty or not _has_columns(atoms, ["driver_facet_id"]):
        return pd.DataFrame(columns=V552_DRIVER_FACET_PRESSURE_SCHEMA["required_columns"])
    group_cols = _common_group_columns(atoms) + ["driver_facet_id"]
    rows = []
    for _, group in _group_frame(atoms, group_cols):
        row = _base_group_row(group, group_cols=group_cols, basis="v551_atoms", status="populated", run_id=run_id)
        row["input_hash"] = row["input_atom_hash"]
        row["run_id"] = run_id or row["run_id"]
        rows.append(row)
    return pd.DataFrame(rows, columns=V552_DRIVER_FACET_PRESSURE_SCHEMA["required_columns"])


def build_country_wave_pressure_profile(atoms: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    if atoms.empty:
        return pd.DataFrame(columns=V552_COUNTRY_WAVE_PRESSURE_PROFILE_SCHEMA["required_columns"])
    group_cols = _common_group_columns(atoms)
    rows = []
    for _, group in _group_frame(atoms, group_cols):
        base = _base_group_row(group, group_cols=group_cols, basis="v551_atoms", status="populated", run_id=run_id)
        directional_mask = _direction_mask(group.get("response_direction", pd.Series(dtype=object))).ne("") & pd.to_numeric(group.get("response_intensity", pd.Series(dtype=object)), errors="coerce").notna()
        base["n_relation_axes"] = int(group["relation_axis_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "relation_axis_id" in group.columns else 0
        base["n_target_entities"] = int(group["target_entity_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "target_entity_id" in group.columns else 0
        base["n_driver_facets"] = int(group["driver_facet_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "driver_facet_id" in group.columns else 0
        base["overall_directionality_coverage"] = float(directional_mask.mean()) if len(group) else 0.0
        base["pressure_computation_status"] = "populated" if directional_mask.any() else "support_summary_only"
        base["status"] = base["pressure_computation_status"]
        base["compiler_status"] = base["pressure_computation_status"]
        base["run_id"] = run_id or base["run_id"]
        base["input_hash"] = base["input_atom_hash"]
        rows.append(base)
    return pd.DataFrame(rows, columns=V552_COUNTRY_WAVE_PRESSURE_PROFILE_SCHEMA["required_columns"])


def _dominant_stratum_from_path(strata_path: Any) -> str:
    text = _clean(strata_path)
    if not text:
        return ""
    first = [part.strip() for part in text.split("|") if part.strip()]
    return first[0] if first else ""


def build_aggregate_projection_surface(atoms: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    required = ["strata_path", "semantic_subrole", "semantic_tags", "horizon_affordance", "position_conditioning", "position_modifiers"]
    if atoms.empty or not _has_columns(atoms, required):
        return pd.DataFrame(columns=V552_AGGREGATE_PROJECTION_SURFACE_SCHEMA["required_columns"])
    group_cols = _common_group_columns(atoms) + ["strata_path"]
    rows: list[dict[str, Any]] = []
    for _, group in _group_frame(atoms, group_cols):
        first = group.iloc[0].to_dict()
        base = _base_group_row(group, group_cols=group_cols, basis="strata_path_projection_rollup", status="populated", run_id=run_id)
        directional_mask = _direction_mask(group.get("response_direction", pd.Series(dtype=object))).ne("") & pd.to_numeric(group.get("response_intensity", pd.Series(dtype=object)), errors="coerce").notna()
        dominant_semantic_subrole, _ = _dominant_orientation(group.get("semantic_subrole", pd.Series(dtype=object)))
        projection_scope = "country_wave_strata_path"
        projection_mode = "signed_projection_proxy" if directional_mask.any() else "support_summary_only"
        base["projection_surface_id"] = _hash_payload(
            {
                "run_id": run_id or _clean(first.get("run_id") or first.get("source_run_id")),
                "source": _clean(first.get("source")),
                "wave": _clean(first.get("wave")),
                "canonical_wave": _clean(first.get("canonical_wave")),
                "country_code": _clean(first.get("country_code")),
                "strata_path": _clean(first.get("strata_path")),
                "dominant_orientation": base.get("dominant_orientation", ""),
                "projection_mode": projection_mode,
            }
        )
        base["strata_path"] = _clean(first.get("strata_path"))
        base["projection_scope"] = projection_scope
        base["projection_mode"] = projection_mode
        base["dominant_stratum_id"] = _dominant_stratum_from_path(first.get("strata_path"))
        base["dominant_semantic_subrole"] = dominant_semantic_subrole
        base["dominant_horizon_type"] = _infer_horizon_type(
            group.get("horizon_affordance", pd.Series(dtype=object)).astype(str).str.cat(sep=" "),
            group.get("semantic_subrole", pd.Series(dtype=object)).astype(str).str.cat(sep=" "),
            group.get("semantic_tags", pd.Series(dtype=object)).astype(str).str.cat(sep=" "),
            group.get("strata_path", pd.Series(dtype=object)).astype(str).str.cat(sep=" "),
        )
        base["dominant_horizon_scope"] = _infer_horizon_scope(
            _join_unique(group.get("strata_path", pd.Series(dtype=object))),
            _join_unique(group.get("position_modifiers", pd.Series(dtype=object))),
            _join_unique(group.get("horizon_affordance", pd.Series(dtype=object))),
        )
        base["dominant_horizon_valence"] = _infer_horizon_valence(
            _join_unique(group.get("horizon_affordance", pd.Series(dtype=object))),
            _join_unique(group.get("semantic_tags", pd.Series(dtype=object))),
        )
        base["n_questions"] = int(group["question_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "question_id" in group.columns else 0
        base["projection_score"] = base.get("pressure_score")
        base["field_pressure_score"] = base.get("pressure_score")
        base["support_basis"] = "directional_intensity" if directional_mask.any() else "support_only"
        base["compiler_status"] = "populated" if directional_mask.any() else "support_summary_only"
        base["status"] = base["compiler_status"]
        base["pressure_computation_status"] = base["compiler_status"]
        base["basis"] = "strata_path_projection_rollup"
        base["input_hash"] = base["input_atom_hash"]
        base["run_id"] = run_id or base["run_id"]
        rows.append(base)
    return pd.DataFrame(rows, columns=V552_AGGREGATE_PROJECTION_SURFACE_SCHEMA["required_columns"])


def build_position_conditioning_profile(atoms: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    required = ["position_conditioning", "position_modifiers", "conditional_strata_weights", "horizon_affordance", "position_conditioning_confidence"]
    if atoms.empty or not _has_columns(atoms, required):
        return pd.DataFrame(columns=V552_POSITION_CONDITIONING_PROFILE_SCHEMA["required_columns"])
    rows: list[dict[str, Any]] = []
    group_cols = _common_group_columns(atoms) + required
    for _, group in _group_frame(atoms, group_cols):
        first = group.iloc[0].to_dict()
        n_atoms = int(len(group))
        n_unweighted = float(pd.to_numeric(group.get("n_unweighted", pd.Series([0] * len(group), index=group.index)), errors="coerce").fillna(0).sum())
        n_weighted = float(pd.to_numeric(group.get("n_weighted", pd.Series([0.0] * len(group), index=group.index)), errors="coerce").fillna(0).sum())
        directional_mask = _direction_mask(group.get("response_direction", pd.Series(dtype=object))).ne("") & pd.to_numeric(group.get("response_intensity", pd.Series(dtype=object)), errors="coerce").notna()
        profile_support_status = _support_status_from_support(n_unweighted, total_respondents=_group_total_respondents(group))
        profile_confidence = _confidence_tier_from_support(n_unweighted, total_respondents=_group_total_respondents(group))
        position_conditioning = _clean(first.get("position_conditioning"))
        conditional_strata_weights = _clean(first.get("conditional_strata_weights"))
        rows.append(
            {
                "run_id": run_id or _clean(first.get("run_id") or first.get("source_run_id")),
                "source": _clean(first.get("source")),
                "wave": _clean(first.get("wave")),
                "canonical_wave": _clean(first.get("canonical_wave")),
                "country_code": _clean(first.get("country_code")),
                "input_atom_count": n_atoms,
                "eligible_atom_count": n_atoms,
                "directionality_coverage": float(directional_mask.mean()) if len(group) else 0.0,
                "support_basis": "directional_intensity" if directional_mask.any() else "support_only",
                "compiler_status": "populated" if directional_mask.any() else "support_summary_only",
                "pressure_computation_status": "populated" if directional_mask.any() else "support_summary_only",
                "input_atom_hash": _hash_payload({"rows": group.get("atom_id", pd.Series(dtype=str)).fillna("").astype(str).tolist()}),
                "input_hash": _hash_payload({
                    "artifact": "position_conditioning_profile",
                    "rows": group.get("atom_id", pd.Series(dtype=str)).fillna("").astype(str).tolist(),
                }),
                "schema_version": V552_SCHEMA_VERSION,
                "created_at": pd.Timestamp.utcnow().isoformat(),
                "position_conditioning_profile_id": _position_conditioning_profile_id(
                    {
                        "source": _clean(first.get("source")),
                        "wave": _clean(first.get("wave")),
                        "canonical_wave": _clean(first.get("canonical_wave")),
                        "country_code": _clean(first.get("country_code")),
                        "position_conditioning": position_conditioning,
                        "position_modifiers": _clean(first.get("position_modifiers")),
                        "strata_path": _conditional_strata_path(conditional_strata_weights),
                        "horizon_affordance": _clean(first.get("horizon_affordance")),
                        "position_conditioning_confidence": _clean(first.get("position_conditioning_confidence")),
                    }
                ),
                "position_conditioning": position_conditioning,
                "position_modifiers": _clean(first.get("position_modifiers")),
                "strata_path": _conditional_strata_path(conditional_strata_weights),
                "conditional_strata_path": _conditional_strata_path(conditional_strata_weights),
                "conditional_strata_weights": conditional_strata_weights,
                "horizon_affordance": _clean(first.get("horizon_affordance")),
                "position_conditioning_note": _clean(first.get("position_conditioning_note")),
                "position_conditioning_confidence": _clean(first.get("position_conditioning_confidence")),
                "n_questions": int(group["question_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "question_id" in group.columns else 0,
                "n_relation_axes": int(group["relation_axis_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "relation_axis_id" in group.columns else 0,
                "n_target_entities": int(group["target_entity_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "target_entity_id" in group.columns else 0,
                "n_driver_facets": int(group["driver_facet_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "driver_facet_id" in group.columns else 0,
                "n_unweighted_total": n_unweighted,
                "n_weighted_total": n_weighted,
                "support_status": profile_support_status,
                "confidence_tier": profile_confidence,
                "basis": "v551_atoms",
                "status": "populated" if position_conditioning != "no" or conditional_strata_weights else "support_summary_only",
            }
        )
    return pd.DataFrame(rows, columns=V552_POSITION_CONDITIONING_PROFILE_SCHEMA["required_columns"])


def build_question_semantic_hierarchy(atoms: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    required = [
        "question_id",
        "var_code",
        "semantic_role",
        "semantic_subrole",
        "semantic_tags",
        "directionality_policy",
        "semantic_confidence",
        "semantic_note",
        "driver_id",
        "driver_facet_id",
        "relation_axis_id",
        "target_entity_id",
        "strata_relevance",
        "strata_path",
        "conditional_strata_weights",
        "position_conditioning",
        "position_modifiers",
        "position_conditioning_confidence",
        "horizon_affordance",
        "question_text",
    ]
    if atoms.empty or not _has_columns(atoms, required):
        return pd.DataFrame(columns=V552_QUESTION_SEMANTIC_HIERARCHY_SCHEMA["required_columns"])
    rows: list[dict[str, Any]] = []
    group_cols = _common_group_columns(atoms) + ["question_id", "var_code"]
    for _, group in _group_frame(atoms, group_cols):
        first = group.iloc[0].to_dict()
        n_atoms = int(len(group))
        n_unweighted = float(pd.to_numeric(group.get("n_unweighted", pd.Series([0] * len(group), index=group.index)), errors="coerce").fillna(0).sum())
        n_weighted = float(pd.to_numeric(group.get("n_weighted", pd.Series([0.0] * len(group), index=group.index)), errors="coerce").fillna(0).sum())
        total_respondents = _group_total_respondents(group)
        support_status = _support_status_from_support(n_unweighted, total_respondents=total_respondents)
        confidence_tier = _confidence_tier_from_support(n_unweighted, total_respondents=total_respondents)
        semantic_role = _first_nonempty(group.get("semantic_role", pd.Series(dtype=object)))
        semantic_subrole = _first_nonempty(group.get("semantic_subrole", pd.Series(dtype=object)))
        semantic_tags = _join_unique(group.get("semantic_tags", pd.Series(dtype=object)))
        directionality_policy = _first_nonempty(group.get("directionality_policy", pd.Series(dtype=object)))
        semantic_confidence = _first_nonempty(group.get("semantic_confidence", pd.Series(dtype=object)))
        semantic_note = _join_unique(group.get("semantic_note", pd.Series(dtype=object)))
        driver_id = _first_nonempty(group.get("driver_id", pd.Series(dtype=object)))
        driver_facet_id = _first_nonempty(group.get("driver_facet_id", pd.Series(dtype=object)))
        relation_axis_id = _first_nonempty(group.get("relation_axis_id", pd.Series(dtype=object)))
        target_entity_id = _first_nonempty(group.get("target_entity_id", pd.Series(dtype=object)))
        strata_relevance = _join_unique(group.get("strata_relevance", pd.Series(dtype=object)))
        strata_path = _first_nonempty(group.get("strata_path", pd.Series(dtype=object))) or _conditional_strata_path(_first_nonempty(group.get("conditional_strata_weights", pd.Series(dtype=object))))
        conditional_strata_weights = _join_unique(group.get("conditional_strata_weights", pd.Series(dtype=object)))
        position_conditioning = _first_nonempty(group.get("position_conditioning", pd.Series(dtype=object)))
        position_modifiers = _join_unique(group.get("position_modifiers", pd.Series(dtype=object)))
        position_conditioning_confidence = _first_nonempty(group.get("position_conditioning_confidence", pd.Series(dtype=object)))
        horizon_affordance = _first_nonempty(group.get("horizon_affordance", pd.Series(dtype=object)))
        horizon_type = _infer_horizon_type(horizon_affordance, semantic_subrole, semantic_tags, strata_path)
        horizon_scope = _infer_horizon_scope(strata_path, position_modifiers, horizon_affordance)
        horizon_openness = _infer_horizon_openness(horizon_type, horizon_affordance)
        horizon_reach = _join_unique([horizon_scope, strata_path, position_modifiers]) or horizon_scope or strata_path
        horizon_durability = "durable" if horizon_type in {"absolute", "bounded"} or position_conditioning == "yes" else ("conditional" if horizon_affordance else "unavailable")
        horizon_enemy_relation = "none"
        enemy_text = " ".join([horizon_affordance, semantic_tags, semantic_note]).lower()
        if any(token in enemy_text for token in ["reconcile", "coexist", "defeat", "exclude", "annihilat", "enemy"]):
            if "reconcile" in enemy_text:
                horizon_enemy_relation = "reconciliation"
            elif "coexist" in enemy_text:
                horizon_enemy_relation = "coexistence"
            elif "defeat" in enemy_text:
                horizon_enemy_relation = "defeat"
            elif "annihilat" in enemy_text:
                horizon_enemy_relation = "annihilation"
            else:
                horizon_enemy_relation = "exclusion"
        horizon_valence = _infer_horizon_valence(horizon_affordance, semantic_tags)
        horizon_sustaining_power = "sustaining" if horizon_type != "collapse" and horizon_valence in {"hopeful", "resilient"} else "limited"
        translation_status = _infer_translation_status(horizon_affordance, semantic_tags)
        question_semantic_hierarchy_id = _hash_payload(
            {
                "source": _clean(first.get("source")),
                "wave": _clean(first.get("wave")),
                "canonical_wave": _clean(first.get("canonical_wave")),
                "country_code": _clean(first.get("country_code")),
                "question_id": _clean(first.get("question_id")),
                "var_code": _clean(first.get("var_code")),
                "semantic_role": semantic_role,
                "semantic_subrole": semantic_subrole,
                "driver_id": driver_id,
                "driver_facet_id": driver_facet_id,
                "relation_axis_id": relation_axis_id,
                "target_entity_id": target_entity_id,
                "strata_path": strata_path,
                "horizon_type": horizon_type,
                "horizon_scope": horizon_scope,
                "horizon_openness": horizon_openness,
            }
        )
        rows.append(
            {
                "run_id": run_id or _clean(first.get("run_id") or first.get("source_run_id")),
                "source": _clean(first.get("source")),
                "wave": _clean(first.get("wave")),
                "canonical_wave": _clean(first.get("canonical_wave")),
                "country_code": _clean(first.get("country_code")),
                "input_atom_count": n_atoms,
                "eligible_atom_count": n_atoms,
                "directionality_coverage": float((_direction_mask(group.get("response_direction", pd.Series(dtype=object))).ne("") & pd.to_numeric(group.get("response_intensity", pd.Series(dtype=object)), errors="coerce").notna()).mean()) if len(group) else 0.0,
                "support_basis": "directional_intensity" if _direction_mask(group.get("response_direction", pd.Series(dtype=object))).ne("").any() else "support_only",
                "compiler_status": "populated" if (semantic_role or semantic_subrole or horizon_affordance or position_conditioning != "no") else "support_summary_only",
                "pressure_computation_status": "populated" if (semantic_role or semantic_subrole or horizon_affordance or position_conditioning != "no") else "support_summary_only",
                "input_atom_hash": _hash_payload({"rows": group.get("atom_id", pd.Series(dtype=str)).fillna("").astype(str).tolist()}),
                "input_hash": _hash_payload({"artifact": "question_semantic_hierarchy", "rows": group.get("atom_id", pd.Series(dtype=str)).fillna("").astype(str).tolist()}),
                "schema_version": V552_SCHEMA_VERSION,
                "created_at": pd.Timestamp.utcnow().isoformat(),
                "question_semantic_hierarchy_id": question_semantic_hierarchy_id,
                "question_id": _clean(first.get("question_id")),
                "var_code": _clean(first.get("var_code")),
                "question_text": _first_nonempty(group.get("question_text", pd.Series(dtype=object))),
                "facet_id": driver_facet_id,
                "facet_label": semantic_subrole or driver_facet_id,
                "driver_id": driver_id,
                "driver_label": driver_id,
                "stratum_id": horizon_scope or (strata_path.split("|", 1)[0] if strata_path else ""),
                "stratum_label": horizon_scope or (strata_path.split("|", 1)[0] if strata_path else ""),
                "semantic_role": semantic_role,
                "semantic_subrole": semantic_subrole,
                "semantic_tags": semantic_tags,
                "directionality_policy": directionality_policy,
                "semantic_confidence": semantic_confidence,
                "semantic_note": semantic_note,
                "relation_axis_id": relation_axis_id,
                "target_entity_id": target_entity_id,
                "relation_axes": _join_unique(group.get("relation_axis_id", pd.Series(dtype=object))),
                "target_entities": _join_unique(group.get("target_entity_id", pd.Series(dtype=object))),
                "facet_ids": _join_unique(group.get("driver_facet_id", pd.Series(dtype=object))),
                "driver_ids": _join_unique(group.get("driver_id", pd.Series(dtype=object))),
                "strata_relevance": strata_relevance,
                "strata_path": strata_path,
                "conditional_strata_weights": conditional_strata_weights,
                "position_conditioning": position_conditioning,
                "position_modifiers": position_modifiers,
                "position_conditioning_confidence": position_conditioning_confidence,
                "horizon_affordance": horizon_affordance,
                "horizon_type": horizon_type,
                "horizon_scope": horizon_scope,
                "horizon_openness": horizon_openness,
                "horizon_reach": horizon_reach,
                "horizon_durability": horizon_durability,
                "horizon_enemy_relation": horizon_enemy_relation,
                "horizon_valence": horizon_valence,
                "horizon_sustaining_power": horizon_sustaining_power,
                "translation_status": translation_status,
                "question_count": 1,
                "n_relation_axes": int(group["relation_axis_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "relation_axis_id" in group.columns else 0,
                "n_target_entities": int(group["target_entity_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "target_entity_id" in group.columns else 0,
                "n_driver_facets": int(group["driver_facet_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "driver_facet_id" in group.columns else 0,
                "n_atoms": n_atoms,
                "n_unweighted_total": n_unweighted,
                "n_weighted_total": n_weighted,
                "support_status": support_status,
                "confidence_tier": confidence_tier,
                "basis": "v551_atoms",
                "status": "populated" if (semantic_role or semantic_subrole or horizon_affordance or position_conditioning != "no") else "support_summary_only",
            }
    )
    return pd.DataFrame(rows, columns=V552_QUESTION_SEMANTIC_HIERARCHY_SCHEMA["required_columns"])


def _semantic_profile_support(group: pd.DataFrame) -> tuple[float, float, str, str]:
    n_unweighted = float(pd.to_numeric(group.get("n_unweighted_total", pd.Series([0] * len(group), index=group.index)), errors="coerce").fillna(0).sum())
    n_weighted = float(pd.to_numeric(group.get("n_weighted_total", pd.Series([0.0] * len(group), index=group.index)), errors="coerce").fillna(0).sum())
    total_respondents = _group_total_respondents(group)
    support_status = _support_status_from_support(n_unweighted, total_respondents=total_respondents)
    confidence_tier = _confidence_tier_from_support(n_unweighted, total_respondents=total_respondents)
    return n_unweighted, n_weighted, support_status, confidence_tier


def build_facet_semantic_profile(question_hierarchy: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    if question_hierarchy.empty or not _has_columns(question_hierarchy, ["facet_id", "facet_label"]):
        return pd.DataFrame(columns=V552_FACET_SEMANTIC_PROFILE_SCHEMA["required_columns"])
    rows: list[dict[str, Any]] = []
    group_cols = _common_group_columns(question_hierarchy) + ["facet_id", "facet_label"]
    for _, group in _group_frame(question_hierarchy, group_cols):
        first = group.iloc[0].to_dict()
        n_unweighted, n_weighted, support_status, confidence_tier = _semantic_profile_support(group)
        n_questions = int(group["question_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "question_id" in group.columns else 0
        n_relation_axes = int(group["relation_axis_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "relation_axis_id" in group.columns else 0
        n_target_entities = int(group["target_entity_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "target_entity_id" in group.columns else 0
        n_driver_facets = int(group["driver_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "driver_id" in group.columns else 0
        facet_semantic_profile_id = _hash_payload({
            "source": _clean(first.get("source")),
            "canonical_wave": _clean(first.get("canonical_wave")),
            "country_code": _clean(first.get("country_code")),
            "facet_id": _clean(first.get("facet_id")),
            "facet_label": _clean(first.get("facet_label")),
        })
        rows.append(
            {
                "run_id": run_id or _clean(first.get("run_id") or first.get("source_run_id")),
                "source": _clean(first.get("source")),
                "wave": _clean(first.get("wave")),
                "canonical_wave": _clean(first.get("canonical_wave")),
                "country_code": _clean(first.get("country_code")),
                "input_atom_count": int(group["n_atoms"].fillna(0).sum()) if "n_atoms" in group.columns else int(len(group)),
                "eligible_atom_count": int(group["n_atoms"].fillna(0).sum()) if "n_atoms" in group.columns else int(len(group)),
                "directionality_coverage": float(pd.to_numeric(group.get("directionality_coverage", pd.Series(dtype=object)), errors="coerce").fillna(0).mean()) if len(group) else 0.0,
                "support_basis": "directional_intensity" if n_unweighted > 0 else "support_only",
                "compiler_status": "populated" if n_unweighted > 0 else "support_summary_only",
                "pressure_computation_status": "populated" if n_unweighted > 0 else "support_summary_only",
                "input_atom_hash": _hash_payload({"rows": group.get("question_semantic_hierarchy_id", pd.Series(dtype=str)).fillna("").astype(str).tolist()}),
                "input_hash": _hash_payload({"artifact": "facet_semantic_profile", "rows": group.get("question_semantic_hierarchy_id", pd.Series(dtype=str)).fillna("").astype(str).tolist()}),
                "schema_version": V552_SCHEMA_VERSION,
                "created_at": pd.Timestamp.utcnow().isoformat(),
                "facet_semantic_profile_id": facet_semantic_profile_id,
                "facet_id": _clean(first.get("facet_id")),
                "facet_label": _clean(first.get("facet_label")),
                "driver_id": _clean(first.get("driver_id")),
                "driver_label": _clean(first.get("driver_label")),
                "stratum_id": _clean(first.get("stratum_id")),
                "stratum_label": _clean(first.get("stratum_label")),
                "semantic_subrole": _join_unique(group.get("semantic_subrole", pd.Series(dtype=object))),
                "semantic_tags": _join_unique(group.get("semantic_tags", pd.Series(dtype=object))),
                "directionality_policy": _first_nonempty(group.get("directionality_policy", pd.Series(dtype=object))),
                "horizon_type": _first_nonempty(group.get("horizon_type", pd.Series(dtype=object))),
                "horizon_scope": _first_nonempty(group.get("horizon_scope", pd.Series(dtype=object))),
                "horizon_openness": _first_nonempty(group.get("horizon_openness", pd.Series(dtype=object))),
                "horizon_valence": _first_nonempty(group.get("horizon_valence", pd.Series(dtype=object))),
                "horizon_sustaining_power": _first_nonempty(group.get("horizon_sustaining_power", pd.Series(dtype=object))),
                "n_questions": n_questions,
                "n_relation_axes": n_relation_axes,
                "n_target_entities": n_target_entities,
                "n_driver_facets": n_driver_facets,
                "n_atoms": int(group["n_atoms"].fillna(0).sum()) if "n_atoms" in group.columns else int(len(group)),
                "n_unweighted_total": n_unweighted,
                "n_weighted_total": n_weighted,
                "support_status": support_status,
                "confidence_tier": confidence_tier,
                "basis": "question_semantic_hierarchy",
                "status": "populated" if n_unweighted > 0 else "support_summary_only",
            }
        )
    return pd.DataFrame(rows, columns=V552_FACET_SEMANTIC_PROFILE_SCHEMA["required_columns"])


def build_driver_semantic_profile(question_hierarchy: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    if question_hierarchy.empty or not _has_columns(question_hierarchy, ["driver_id"]):
        return pd.DataFrame(columns=V552_DRIVER_SEMANTIC_PROFILE_SCHEMA["required_columns"])
    rows: list[dict[str, Any]] = []
    group_cols = _common_group_columns(question_hierarchy) + ["driver_id"]
    for _, group in _group_frame(question_hierarchy, group_cols):
        first = group.iloc[0].to_dict()
        n_unweighted, n_weighted, support_status, confidence_tier = _semantic_profile_support(group)
        driver_semantic_profile_id = _hash_payload({
            "source": _clean(first.get("source")),
            "canonical_wave": _clean(first.get("canonical_wave")),
            "country_code": _clean(first.get("country_code")),
            "driver_id": _clean(first.get("driver_id")),
        })
        rows.append(
            {
                "run_id": run_id or _clean(first.get("run_id") or first.get("source_run_id")),
                "source": _clean(first.get("source")),
                "wave": _clean(first.get("wave")),
                "canonical_wave": _clean(first.get("canonical_wave")),
                "country_code": _clean(first.get("country_code")),
                "input_atom_count": int(group["n_atoms"].fillna(0).sum()) if "n_atoms" in group.columns else int(len(group)),
                "eligible_atom_count": int(group["n_atoms"].fillna(0).sum()) if "n_atoms" in group.columns else int(len(group)),
                "directionality_coverage": float(pd.to_numeric(group.get("directionality_coverage", pd.Series(dtype=object)), errors="coerce").fillna(0).mean()) if len(group) else 0.0,
                "support_basis": "directional_intensity" if n_unweighted > 0 else "support_only",
                "compiler_status": "populated" if n_unweighted > 0 else "support_summary_only",
                "pressure_computation_status": "populated" if n_unweighted > 0 else "support_summary_only",
                "input_atom_hash": _hash_payload({"rows": group.get("question_semantic_hierarchy_id", pd.Series(dtype=str)).fillna("").astype(str).tolist()}),
                "input_hash": _hash_payload({"artifact": "driver_semantic_profile", "rows": group.get("question_semantic_hierarchy_id", pd.Series(dtype=str)).fillna("").astype(str).tolist()}),
                "schema_version": V552_SCHEMA_VERSION,
                "created_at": pd.Timestamp.utcnow().isoformat(),
                "driver_semantic_profile_id": driver_semantic_profile_id,
                "driver_id": _clean(first.get("driver_id")),
                "driver_label": _clean(first.get("driver_label")),
                "stratum_id": _clean(first.get("stratum_id")),
                "stratum_label": _clean(first.get("stratum_label")),
                "facet_ids": _join_unique(group.get("facet_id", pd.Series(dtype=object))),
                "semantic_subrole": _join_unique(group.get("semantic_subrole", pd.Series(dtype=object))),
                "semantic_tags": _join_unique(group.get("semantic_tags", pd.Series(dtype=object))),
                "directionality_policy": _first_nonempty(group.get("directionality_policy", pd.Series(dtype=object))),
                "horizon_type": _first_nonempty(group.get("horizon_type", pd.Series(dtype=object))),
                "horizon_scope": _first_nonempty(group.get("horizon_scope", pd.Series(dtype=object))),
                "horizon_openness": _first_nonempty(group.get("horizon_openness", pd.Series(dtype=object))),
                "horizon_valence": _first_nonempty(group.get("horizon_valence", pd.Series(dtype=object))),
                "horizon_sustaining_power": _first_nonempty(group.get("horizon_sustaining_power", pd.Series(dtype=object))),
                "n_questions": int(group["question_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "question_id" in group.columns else 0,
                "n_relation_axes": int(group["relation_axis_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "relation_axis_id" in group.columns else 0,
                "n_target_entities": int(group["target_entity_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "target_entity_id" in group.columns else 0,
                "n_driver_facets": int(group["facet_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "facet_id" in group.columns else 0,
                "n_atoms": int(group["n_atoms"].fillna(0).sum()) if "n_atoms" in group.columns else int(len(group)),
                "n_unweighted_total": n_unweighted,
                "n_weighted_total": n_weighted,
                "support_status": support_status,
                "confidence_tier": confidence_tier,
                "basis": "question_semantic_hierarchy",
                "status": "populated" if n_unweighted > 0 else "support_summary_only",
            }
        )
    return pd.DataFrame(rows, columns=V552_DRIVER_SEMANTIC_PROFILE_SCHEMA["required_columns"])


def build_stratum_semantic_profile(question_hierarchy: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    if question_hierarchy.empty or not _has_columns(question_hierarchy, ["stratum_id"]):
        return pd.DataFrame(columns=V552_STRATUM_SEMANTIC_PROFILE_SCHEMA["required_columns"])
    rows: list[dict[str, Any]] = []
    group_cols = _common_group_columns(question_hierarchy) + ["stratum_id"]
    for _, group in _group_frame(question_hierarchy, group_cols):
        first = group.iloc[0].to_dict()
        n_unweighted, n_weighted, support_status, confidence_tier = _semantic_profile_support(group)
        stratum_semantic_profile_id = _hash_payload({
            "source": _clean(first.get("source")),
            "canonical_wave": _clean(first.get("canonical_wave")),
            "country_code": _clean(first.get("country_code")),
            "stratum_id": _clean(first.get("stratum_id")),
        })
        rows.append(
            {
                "run_id": run_id or _clean(first.get("run_id") or first.get("source_run_id")),
                "source": _clean(first.get("source")),
                "wave": _clean(first.get("wave")),
                "canonical_wave": _clean(first.get("canonical_wave")),
                "country_code": _clean(first.get("country_code")),
                "input_atom_count": int(group["n_atoms"].fillna(0).sum()) if "n_atoms" in group.columns else int(len(group)),
                "eligible_atom_count": int(group["n_atoms"].fillna(0).sum()) if "n_atoms" in group.columns else int(len(group)),
                "directionality_coverage": float(pd.to_numeric(group.get("directionality_coverage", pd.Series(dtype=object)), errors="coerce").fillna(0).mean()) if len(group) else 0.0,
                "support_basis": "directional_intensity" if n_unweighted > 0 else "support_only",
                "compiler_status": "populated" if n_unweighted > 0 else "support_summary_only",
                "pressure_computation_status": "populated" if n_unweighted > 0 else "support_summary_only",
                "input_atom_hash": _hash_payload({"rows": group.get("question_semantic_hierarchy_id", pd.Series(dtype=str)).fillna("").astype(str).tolist()}),
                "input_hash": _hash_payload({"artifact": "stratum_semantic_profile", "rows": group.get("question_semantic_hierarchy_id", pd.Series(dtype=str)).fillna("").astype(str).tolist()}),
                "schema_version": V552_SCHEMA_VERSION,
                "created_at": pd.Timestamp.utcnow().isoformat(),
                "stratum_semantic_profile_id": stratum_semantic_profile_id,
                "stratum_id": _clean(first.get("stratum_id")),
                "stratum_label": _clean(first.get("stratum_label")),
                "driver_ids": _join_unique(group.get("driver_id", pd.Series(dtype=object))),
                "facet_ids": _join_unique(group.get("facet_id", pd.Series(dtype=object))),
                "semantic_subrole": _join_unique(group.get("semantic_subrole", pd.Series(dtype=object))),
                "semantic_tags": _join_unique(group.get("semantic_tags", pd.Series(dtype=object))),
                "horizon_type": _first_nonempty(group.get("horizon_type", pd.Series(dtype=object))),
                "horizon_scope": _first_nonempty(group.get("horizon_scope", pd.Series(dtype=object))),
                "horizon_openness": _first_nonempty(group.get("horizon_openness", pd.Series(dtype=object))),
                "horizon_reach": _join_unique(group.get("horizon_reach", pd.Series(dtype=object))) or _first_nonempty(group.get("horizon_reach", pd.Series(dtype=object))),
                "horizon_valence": _first_nonempty(group.get("horizon_valence", pd.Series(dtype=object))),
                "horizon_sustaining_power": _first_nonempty(group.get("horizon_sustaining_power", pd.Series(dtype=object))),
                "n_questions": int(group["question_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "question_id" in group.columns else 0,
                "n_relation_axes": int(group["relation_axis_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "relation_axis_id" in group.columns else 0,
                "n_target_entities": int(group["target_entity_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "target_entity_id" in group.columns else 0,
                "n_driver_facets": int(group["facet_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "facet_id" in group.columns else 0,
                "n_atoms": int(group["n_atoms"].fillna(0).sum()) if "n_atoms" in group.columns else int(len(group)),
                "n_unweighted_total": n_unweighted,
                "n_weighted_total": n_weighted,
                "support_status": support_status,
                "confidence_tier": confidence_tier,
                "basis": "question_semantic_hierarchy",
                "status": "populated" if n_unweighted > 0 else "support_summary_only",
            }
        )
    return pd.DataFrame(rows, columns=V552_STRATUM_SEMANTIC_PROFILE_SCHEMA["required_columns"])


def build_horizon_semantic_profile(question_hierarchy: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    if question_hierarchy.empty or not _has_columns(question_hierarchy, ["horizon_type"]):
        return pd.DataFrame(columns=V552_HORIZON_SEMANTIC_PROFILE_SCHEMA["required_columns"])
    rows: list[dict[str, Any]] = []
    group_cols = _common_group_columns(question_hierarchy) + ["horizon_type", "horizon_scope", "horizon_openness", "horizon_reach", "horizon_valence", "horizon_sustaining_power", "translation_status"]
    for _, group in _group_frame(question_hierarchy, group_cols):
        first = group.iloc[0].to_dict()
        n_unweighted, n_weighted, support_status, confidence_tier = _semantic_profile_support(group)
        horizon_semantic_profile_id = _hash_payload({
            "source": _clean(first.get("source")),
            "canonical_wave": _clean(first.get("canonical_wave")),
            "country_code": _clean(first.get("country_code")),
            "horizon_type": _clean(first.get("horizon_type")),
            "horizon_scope": _clean(first.get("horizon_scope")),
            "horizon_openness": _clean(first.get("horizon_openness")),
        })
        rows.append(
            {
                "run_id": run_id or _clean(first.get("run_id") or first.get("source_run_id")),
                "source": _clean(first.get("source")),
                "wave": _clean(first.get("wave")),
                "canonical_wave": _clean(first.get("canonical_wave")),
                "country_code": _clean(first.get("country_code")),
                "input_atom_count": int(group["n_atoms"].fillna(0).sum()) if "n_atoms" in group.columns else int(len(group)),
                "eligible_atom_count": int(group["n_atoms"].fillna(0).sum()) if "n_atoms" in group.columns else int(len(group)),
                "directionality_coverage": float(pd.to_numeric(group.get("directionality_coverage", pd.Series(dtype=object)), errors="coerce").fillna(0).mean()) if len(group) else 0.0,
                "support_basis": "directional_intensity" if n_unweighted > 0 else "support_only",
                "compiler_status": "populated" if n_unweighted > 0 else "support_summary_only",
                "pressure_computation_status": "populated" if n_unweighted > 0 else "support_summary_only",
                "input_atom_hash": _hash_payload({"rows": group.get("question_semantic_hierarchy_id", pd.Series(dtype=str)).fillna("").astype(str).tolist()}),
                "input_hash": _hash_payload({"artifact": "horizon_semantic_profile", "rows": group.get("question_semantic_hierarchy_id", pd.Series(dtype=str)).fillna("").astype(str).tolist()}),
                "schema_version": V552_SCHEMA_VERSION,
                "created_at": pd.Timestamp.utcnow().isoformat(),
                "horizon_semantic_profile_id": horizon_semantic_profile_id,
                "horizon_type": _clean(first.get("horizon_type")),
                "horizon_scope": _clean(first.get("horizon_scope")),
                "horizon_openness": _clean(first.get("horizon_openness")),
                "horizon_reach": _clean(first.get("horizon_reach")),
                "horizon_durability": _first_nonempty(group.get("horizon_durability", pd.Series(dtype=object))),
                "horizon_enemy_relation": _first_nonempty(group.get("horizon_enemy_relation", pd.Series(dtype=object))),
                "horizon_valence": _clean(first.get("horizon_valence")),
                "horizon_sustaining_power": _clean(first.get("horizon_sustaining_power")),
                "translation_status": _clean(first.get("translation_status")),
                "driver_ids": _join_unique(group.get("driver_id", pd.Series(dtype=object))),
                "facet_ids": _join_unique(group.get("facet_id", pd.Series(dtype=object))),
                "stratum_ids": _join_unique(group.get("stratum_id", pd.Series(dtype=object))),
                "semantic_tags": _join_unique(group.get("semantic_tags", pd.Series(dtype=object))),
                "n_questions": int(group["question_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "question_id" in group.columns else 0,
                "n_relation_axes": int(group["relation_axis_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "relation_axis_id" in group.columns else 0,
                "n_target_entities": int(group["target_entity_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "target_entity_id" in group.columns else 0,
                "n_driver_facets": int(group["facet_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if "facet_id" in group.columns else 0,
                "n_atoms": int(group["n_atoms"].fillna(0).sum()) if "n_atoms" in group.columns else int(len(group)),
                "n_unweighted_total": n_unweighted,
                "n_weighted_total": n_weighted,
                "support_status": support_status,
                "confidence_tier": confidence_tier,
                "basis": "question_semantic_hierarchy",
                "status": "populated" if n_unweighted > 0 else "support_summary_only",
            }
        )
    return pd.DataFrame(rows, columns=V552_HORIZON_SEMANTIC_PROFILE_SCHEMA["required_columns"])


_PARENT_DOMAIN_KEYWORDS: dict[str, tuple[str, ...]] = {
    "institutional_trust": ("trust", "courts", "police", "army", "government", "state", "institution"),
    "state_fear": ("fear", "threat", "distrust", "danger", "repress", "authorit"),
    "family_obligation": ("family", "household", "mother", "father", "child", "children", "spouse", "marriage", "oblig"),
    "gender_order": ("gender", "women", "men", "female", "male", "abortion", "fepres", "sex role", "role order"),
    "religious_salience": ("relig", "church", "mosque", "faith", "god", "pray", "sect"),
    "authority_style": ("authority", "obedience", "discipline", "control", "rule", "leadership"),
    "warmth_care": ("care", "kind", "warm", "help", "support", "sympathy", "solidarity"),
    "discipline_control": ("discipline", "control", "punish", "law", "order", "crime", "cappun"),
    "economic_security_expectation": ("income", "econom", "money", "work", "job", "security", "welfare", "class"),
    "migration_aspiration": ("migr", "move", "leave", "travel", "immigr", "emigrate"),
    "neighbor_trust": ("neighbor", "community", "local", "neighborhood"),
    "outgroup_boundary": ("race", "rac", "ethnic", "immigr", "other", "boundary", "outgroup", "segreg", "minority"),
    "agency_fatalism": ("fatal", "helpless", "powerless", "control", "agency", "hopeless", "can't", "cannot"),
    "justice_mercy_orientation": ("justice", "mercy", "fair", "courts", "law", "rights", "compassion"),
    "absolute_horizon_pressure": ("absolute", "ultimate", "redempt", "salvation", "futur", "hope", "collapse", "despair", "endure", "steadfast"),
    "general_pressure": (),
}

_BEHAVIOR_TENDENCY_DOMAINS = {
    "authority_style",
    "warmth_care",
    "discipline_control",
    "agency_fatalism",
    "economic_security_expectation",
    "migration_aspiration",
    "family_obligation",
}


def _domain_score_map(*values: Any) -> dict[str, float]:
    text = " ".join(_clean(value).lower() for value in values if _clean(value))
    scores: dict[str, float] = {}
    for domain, keywords in _PARENT_DOMAIN_KEYWORDS.items():
        score = 0.0
        for keyword in keywords:
            if keyword and keyword in text:
                score += 1.0
        if score > 0:
            scores[domain] = score
    if not scores:
        scores["general_pressure"] = 1.0
    return scores


def _dominant_domain(scores: dict[str, float]) -> str:
    if not scores:
        return "general_pressure"
    return sorted(scores.items(), key=lambda item: (-item[1], item[0]))[0][0]


def _normalized_distribution(scores: dict[str, float]) -> dict[str, float]:
    total = float(sum(scores.values()))
    if total <= 0:
        return {"general_pressure": 1.0}
    return {key: float(value) / total for key, value in sorted(scores.items(), key=lambda item: (-item[1], item[0]))}


def _parent_signature_from_group(group: pd.DataFrame) -> str:
    return _first_nonempty(
        [
            *group.get("subject_position_signature", pd.Series(dtype=object)).tolist(),
            *group.get("position_conditioning", pd.Series(dtype=object)).tolist(),
            *group.get("position_modifiers", pd.Series(dtype=object)).tolist(),
            *group.get("strata_path", pd.Series(dtype=object)).tolist(),
        ]
    )


def _parent_absence_note() -> str:
    return "birth_year_range, formative_year_range, child_birth_year, and full household genealogy are absent from the available V551 atom surface"


def _parent_forbidden_inference() -> str:
    return "Do not infer parental essence, parenting style, or absolute horizon from this prior alone."


def _parent_channel_ids(group: pd.DataFrame) -> str:
    combos: list[str] = []
    for _, row in group.iterrows():
        parts = [
            _clean(row.get("relation_axis_id")),
            _clean(row.get("target_entity_id")),
            _clean(row.get("driver_facet_id")),
        ]
        combo = "::".join(part for part in parts if part)
        if combo and combo not in combos:
            combos.append(combo)
    return _join_unique(combos)


def _build_parent_prior_rows(
    source_frame: pd.DataFrame,
    *,
    prior_type: str,
    run_id: str = "",
    behavior_only: bool = False,
    source_kind: str = "atoms",
) -> pd.DataFrame:
    required = ["subject_position_signature", "semantic_subrole", "semantic_tags", "horizon_affordance", "position_conditioning", "position_modifiers", "strata_path"]
    if source_frame.empty or not _has_columns(source_frame, required):
        return pd.DataFrame(columns=V552_PARENT_POSITION_PRIOR_SCHEMA["required_columns"])

    rows: list[dict[str, Any]] = []
    group_cols = _common_group_columns(source_frame) + ["subject_position_signature"]
    for _, group in _group_frame(source_frame, group_cols):
        first = group.iloc[0].to_dict()
        position_signature = _parent_signature_from_group(group)
        domain_scores: dict[str, float] = {}
        for _, row in group.iterrows():
            row_scores = _domain_score_map(
                row.get("semantic_subrole", ""),
                row.get("semantic_tags", ""),
                row.get("horizon_affordance", ""),
                row.get("position_conditioning", ""),
                row.get("position_modifiers", ""),
                row.get("strata_path", ""),
                row.get("driver_id", ""),
                row.get("driver_facet_id", ""),
                row.get("target_entity_id", ""),
            )
            for domain, score in row_scores.items():
                if behavior_only and domain not in _BEHAVIOR_TENDENCY_DOMAINS:
                    continue
                domain_scores[domain] = domain_scores.get(domain, 0.0) + float(score)
        if not domain_scores:
            domain_scores = {"general_pressure": 1.0}
        dominant_domain = _dominant_domain(domain_scores)
        n_atoms = int(len(group))
        n_unweighted = float(pd.to_numeric(group.get("n_unweighted", pd.Series([0] * len(group), index=group.index)), errors="coerce").fillna(0).sum())
        n_weighted = float(pd.to_numeric(group.get("n_weighted", pd.Series([0.0] * len(group), index=group.index)), errors="coerce").fillna(0).sum())
        total_respondents = _group_total_respondents(group)
        directions, intensities, directionality_coverage = _directionality_frame(group)
        directional_mask = directions.ne("") & intensities.notna()
        pressure_score = None
        if directional_mask.any():
            signed = intensities.loc[directional_mask] * directions.loc[directional_mask].map(_direction_sign).astype(float)
            pressure_score = float(signed.mean()) if not signed.empty else None
        support_status = _support_status_from_support(n_unweighted, total_respondents=total_respondents)
        confidence_tier = _confidence_tier_from_support(n_unweighted, total_respondents=total_respondents)
        prior_distribution = {
            "prior_type": prior_type,
            "source_kind": source_kind,
            "position_signature": position_signature,
            "dominant_domain": dominant_domain,
            "domain_weights": _normalized_distribution(domain_scores),
            "n_atoms": n_atoms,
            "n_unweighted_total": n_unweighted,
            "n_weighted_total": n_weighted,
            "directionality_coverage": float(directionality_coverage),
            "pressure_score": pressure_score,
            "support_status": support_status,
            "confidence_tier": confidence_tier,
            "horizon_type": _infer_horizon_type(group.get("horizon_affordance", pd.Series(dtype=object)).astype(str).str.cat(sep=" "), group.get("semantic_subrole", pd.Series(dtype=object)).astype(str).str.cat(sep=" "), group.get("semantic_tags", pd.Series(dtype=object)).astype(str).str.cat(sep=" "), group.get("strata_path", pd.Series(dtype=object)).astype(str).str.cat(sep=" ")),
            "horizon_scope": _infer_horizon_scope(_join_unique(group.get("strata_path", pd.Series(dtype=object))), _join_unique(group.get("position_modifiers", pd.Series(dtype=object))), _join_unique(group.get("horizon_affordance", pd.Series(dtype=object)))),
            "horizon_openness": _infer_horizon_openness(_infer_horizon_type(group.get("horizon_affordance", pd.Series(dtype=object)).astype(str).str.cat(sep=" "), group.get("semantic_subrole", pd.Series(dtype=object)).astype(str).str.cat(sep=" "), group.get("semantic_tags", pd.Series(dtype=object)).astype(str).str.cat(sep=" "), group.get("strata_path", pd.Series(dtype=object)).astype(str).str.cat(sep=" ")), _join_unique(group.get("horizon_affordance", pd.Series(dtype=object)))),
            "horizon_valence": _infer_horizon_valence(_join_unique(group.get("horizon_affordance", pd.Series(dtype=object))), _join_unique(group.get("semantic_tags", pd.Series(dtype=object)))),
        }
        if behavior_only and dominant_domain not in _BEHAVIOR_TENDENCY_DOMAINS:
            dominant_domain = "general_pressure"
        prior_id = _hash_payload({
            "run_id": run_id or _clean(first.get("run_id") or first.get("source_run_id")),
            "prior_type": prior_type,
            "source": _clean(first.get("source")),
            "wave": _clean(first.get("wave")),
            "canonical_wave": _clean(first.get("canonical_wave")),
            "country_code": _clean(first.get("country_code")),
            "position_signature": position_signature,
            "attitude_domain": dominant_domain,
            "packet_ids": group.get("atom_id", pd.Series(dtype=str)).fillna("").astype(str).tolist(),
        })
        rows.append(
            {
                "run_id": run_id or _clean(first.get("run_id") or first.get("source_run_id")),
                "source": _clean(first.get("source")),
                "wave": _clean(first.get("wave")),
                "canonical_wave": _clean(first.get("canonical_wave")),
                "country_code": _clean(first.get("country_code")),
                "prior_id": prior_id,
                "prior_type": prior_type,
                "position_signature": position_signature,
                "attitude_domain": dominant_domain,
                "prior_distribution": json.dumps(prior_distribution, sort_keys=True, ensure_ascii=False, default=str),
                "confidence_tier": confidence_tier,
                "basis": "structurally_inferred" if not behavior_only else "low_confidence_proxy",
                "known_absences": _parent_absence_note(),
                "forbidden_inference": _parent_forbidden_inference(),
                "created_at": pd.Timestamp.utcnow().isoformat(),
                "birth_year_range": "",
                "formative_year_range": "",
                "child_birth_year": "",
                "sex_gender": _clean(first.get("sex_gender")),
                "age_group_at_child_birth": "",
                "education_level": _clean(first.get("education_level")),
                "income_level": _clean(first.get("income_level")),
                "religion_label": _clean(first.get("religion_label")),
                "urban_rural": _clean(first.get("urban_rural")),
                "region": _clean(first.get("region")),
                "ethnicity": _clean(first.get("ethnicity")),
                "language": _clean(first.get("language")),
                "packet_ids": _join_unique(group.get("atom_id", pd.Series(dtype=object))),
                "channel_ids": _parent_channel_ids(group),
            }
        )
    return pd.DataFrame(rows, columns=V552_PARENT_POSITION_PRIOR_SCHEMA["required_columns"])


def build_parent_position_prior(atoms: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    return _build_parent_prior_rows(atoms, prior_type="parent_position_prior", run_id=run_id, source_kind="v551_atoms", behavior_only=False)


def build_parent_attitude_prior(atoms: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    if atoms.empty:
        return pd.DataFrame(columns=V552_PARENT_ATTITUDE_PRIOR_SCHEMA["required_columns"])
    base = _build_parent_prior_rows(atoms, prior_type="parent_attitude_prior", run_id=run_id, source_kind="v551_atoms", behavior_only=False)
    return pd.DataFrame(base, columns=V552_PARENT_ATTITUDE_PRIOR_SCHEMA["required_columns"])


def build_parent_behavior_tendency_prior(atoms: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    if atoms.empty:
        return pd.DataFrame(columns=V552_PARENT_BEHAVIOR_TENDENCY_PRIOR_SCHEMA["required_columns"])
    base = _build_parent_prior_rows(atoms, prior_type="parent_behavior_tendency_prior", run_id=run_id, source_kind="v551_atoms", behavior_only=True)
    return pd.DataFrame(base, columns=V552_PARENT_BEHAVIOR_TENDENCY_PRIOR_SCHEMA["required_columns"])


def build_parent_contradiction_prior(atoms: pd.DataFrame, contradiction_tensor: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    if contradiction_tensor.empty or atoms.empty:
        return pd.DataFrame(columns=V552_PARENT_CONTRADICTION_PRIOR_SCHEMA["required_columns"])
    rows: list[dict[str, Any]] = []
    required = ["subject_position_signature", "semantic_subrole", "semantic_tags", "horizon_affordance", "position_conditioning", "position_modifiers", "strata_path"]
    if not _has_columns(atoms, required):
        return pd.DataFrame(columns=V552_PARENT_CONTRADICTION_PRIOR_SCHEMA["required_columns"])
    for _, contradiction in contradiction_tensor.iterrows():
        axis_a = _clean(contradiction.get("axis_a"))
        axis_b = _clean(contradiction.get("axis_b"))
        target_entity_id = _clean(contradiction.get("target_entity_id"))
        driver_facet_id = _clean(contradiction.get("driver_facet_id"))
        matching = atoms[
            atoms["target_entity_id"].fillna("").astype(str).str.strip().eq(target_entity_id)
            & atoms["driver_facet_id"].fillna("").astype(str).str.strip().eq(driver_facet_id)
            & atoms["relation_axis_id"].fillna("").astype(str).str.strip().isin([axis_a, axis_b])
        ].copy()
        if matching.empty:
            continue
        signatures = _join_unique(matching.get("subject_position_signature", pd.Series(dtype=object)))
        domain_scores: dict[str, float] = {}
        for _, row in matching.iterrows():
            row_scores = _domain_score_map(
                row.get("semantic_subrole", ""),
                row.get("semantic_tags", ""),
                row.get("horizon_affordance", ""),
                row.get("position_conditioning", ""),
                row.get("position_modifiers", ""),
                row.get("strata_path", ""),
                row.get("driver_id", ""),
                row.get("driver_facet_id", ""),
                row.get("target_entity_id", ""),
            )
            for domain, score in row_scores.items():
                domain_scores[domain] = domain_scores.get(domain, 0.0) + float(score)
        if not domain_scores:
            domain_scores = {"contradiction_pressure": 1.0}
        dominant_domain = _dominant_domain(domain_scores)
        first = matching.iloc[0].to_dict()
        n_unweighted = float(pd.to_numeric(matching.get("n_unweighted", pd.Series([0] * len(matching), index=matching.index)), errors="coerce").fillna(0).sum())
        n_weighted = float(pd.to_numeric(matching.get("n_weighted", pd.Series([0.0] * len(matching), index=matching.index)), errors="coerce").fillna(0).sum())
        prior_distribution = {
            "prior_type": "parent_contradiction_prior",
            "contradiction_id": _clean(contradiction.get("contradiction_id")),
            "axis_a": axis_a,
            "axis_b": axis_b,
            "target_entity_id": target_entity_id,
            "driver_facet_id": driver_facet_id,
            "position_signatures": signatures,
            "domain_weights": _normalized_distribution(domain_scores),
            "positive_atom_count": int(float(contradiction.get("positive_atom_count") or 0)),
            "negative_atom_count": int(float(contradiction.get("negative_atom_count") or 0)),
            "contradiction_score": float(contradiction.get("contradiction_score") or 0),
            "opposing_directionality_present": bool(contradiction.get("opposing_directionality_present")),
        }
        rows.append(
            {
                "run_id": run_id or _clean(first.get("run_id") or first.get("source_run_id")),
                "source": _clean(first.get("source")),
                "wave": _clean(first.get("wave")),
                "canonical_wave": _clean(first.get("canonical_wave")),
                "country_code": _clean(first.get("country_code")),
                "prior_id": _hash_payload({
                    "prior_type": "parent_contradiction_prior",
                    "source": _clean(first.get("source")),
                    "wave": _clean(first.get("wave")),
                    "canonical_wave": _clean(first.get("canonical_wave")),
                    "country_code": _clean(first.get("country_code")),
                    "axis_a": axis_a,
                    "axis_b": axis_b,
                    "target_entity_id": target_entity_id,
                    "driver_facet_id": driver_facet_id,
                    "position_signatures": signatures,
                }),
                "prior_type": "parent_contradiction_prior",
                "position_signature": signatures,
                "attitude_domain": dominant_domain,
                "prior_distribution": json.dumps(prior_distribution, sort_keys=True, ensure_ascii=False, default=str),
                "confidence_tier": _confidence_tier_from_support(n_unweighted, total_respondents=_group_total_respondents(matching)),
                "basis": "structurally_inferred",
                "known_absences": _parent_absence_note(),
                "forbidden_inference": _parent_forbidden_inference(),
                "created_at": pd.Timestamp.utcnow().isoformat(),
                "birth_year_range": "",
                "formative_year_range": "",
                "child_birth_year": "",
                "sex_gender": _clean(first.get("sex_gender")),
                "age_group_at_child_birth": "",
                "education_level": _clean(first.get("education_level")),
                "income_level": _clean(first.get("income_level")),
                "religion_label": _clean(first.get("religion_label")),
                "urban_rural": _clean(first.get("urban_rural")),
                "region": _clean(first.get("region")),
                "ethnicity": _clean(first.get("ethnicity")),
                "language": _clean(first.get("language")),
                "packet_ids": _join_unique(matching.get("atom_id", pd.Series(dtype=object))),
                "channel_ids": _parent_channel_ids(matching),
            }
        )
    return pd.DataFrame(rows, columns=V552_PARENT_CONTRADICTION_PRIOR_SCHEMA["required_columns"])


def build_parent_prior_manifest(
    *,
    run_id: str,
    source: str,
    wave: str,
    canonical_wave: str,
    country_code: str,
    parent_position_prior: pd.DataFrame,
    parent_attitude_prior: pd.DataFrame,
    parent_behavior_tendency_prior: pd.DataFrame,
    parent_contradiction_prior: pd.DataFrame,
) -> pd.DataFrame:
    prior_frames = [parent_position_prior, parent_attitude_prior, parent_behavior_tendency_prior, parent_contradiction_prior]
    packet_ids = []
    channel_ids = []
    position_signatures = []
    attitude_domains = []
    for frame in prior_frames:
        if frame.empty:
            continue
        if "packet_ids" in frame.columns:
            packet_ids.extend(_clean(value) for value in frame["packet_ids"].fillna("").astype(str).tolist() if _clean(value))
        if "channel_ids" in frame.columns:
            channel_ids.extend(_clean(value) for value in frame["channel_ids"].fillna("").astype(str).tolist() if _clean(value))
        if "position_signature" in frame.columns:
            position_signatures.extend(_clean(value) for value in frame["position_signature"].fillna("").astype(str).tolist() if _clean(value))
        if "attitude_domain" in frame.columns:
            attitude_domains.extend(_clean(value) for value in frame["attitude_domain"].fillna("").astype(str).tolist() if _clean(value))
    row = {
        "run_id": run_id,
        "parent_prior_manifest_id": _hash_payload(
            {
                "run_id": run_id,
                "source": source,
                "wave": wave,
                "canonical_wave": canonical_wave,
                "country_code": country_code,
                "parent_position_prior_rows": int(len(parent_position_prior)),
                "parent_attitude_prior_rows": int(len(parent_attitude_prior)),
                "parent_behavior_tendency_prior_rows": int(len(parent_behavior_tendency_prior)),
                "parent_contradiction_prior_rows": int(len(parent_contradiction_prior)),
            }
        ),
        "source": source,
        "wave": wave,
        "canonical_wave": canonical_wave,
        "country_code": country_code,
        "position_signature_count": int(pd.Series(position_signatures, dtype=object).replace("", pd.NA).dropna().nunique()) if position_signatures else 0,
        "attitude_domain_count": int(pd.Series(attitude_domains, dtype=object).replace("", pd.NA).dropna().nunique()) if attitude_domains else 0,
        "parent_position_prior_rows": int(len(parent_position_prior)),
        "parent_attitude_prior_rows": int(len(parent_attitude_prior)),
        "parent_behavior_tendency_prior_rows": int(len(parent_behavior_tendency_prior)),
        "parent_contradiction_prior_rows": int(len(parent_contradiction_prior)),
        "basis": "structurally_inferred",
        "confidence_tier": "low" if (parent_position_prior.empty and parent_attitude_prior.empty and parent_behavior_tendency_prior.empty and parent_contradiction_prior.empty) else "medium",
        "status": "populated" if (len(parent_position_prior) or len(parent_attitude_prior) or len(parent_behavior_tendency_prior) or len(parent_contradiction_prior)) else "support_summary_only",
        "known_absences": _parent_absence_note(),
        "forbidden_inference": _parent_forbidden_inference(),
        "created_at": pd.Timestamp.utcnow().isoformat(),
    }
    if packet_ids:
        row["packet_ids"] = _join_unique(packet_ids)
    if channel_ids:
        row["channel_ids"] = _join_unique(channel_ids)
    return pd.DataFrame([row], columns=V552_PARENT_PRIOR_MANIFEST_SCHEMA["required_columns"])


def build_structural_channel_index(atoms: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    if atoms.empty or not _has_columns(atoms, ["relation_axis_id", "target_entity_id", "driver_facet_id"]):
        return pd.DataFrame(columns=V552_STRUCTURAL_CHANNEL_INDEX_SCHEMA["required_columns"])
    rows = []
    group_cols = _common_group_columns(atoms) + ["relation_axis_id", "target_entity_id", "driver_facet_id"]
    for _, group in _group_frame(atoms, group_cols):
        first = group.iloc[0].to_dict()
        n_atoms = int(len(group))
        n_unweighted = float(pd.to_numeric(group.get("n_unweighted", pd.Series([0] * len(group), index=group.index)), errors="coerce").fillna(0).sum())
        n_weighted = float(pd.to_numeric(group.get("n_weighted", pd.Series([0.0] * len(group), index=group.index)), errors="coerce").fillna(0).sum())
        total_respondents = _group_total_respondents(group)
        directions, intensities, directionality_coverage = _directionality_frame(group)
        directional_mask = directions.ne("") & intensities.notna()
        if directional_mask.any():
            signed = intensities.loc[directional_mask] * directions.loc[directional_mask].map(_direction_sign).astype(float)
            pressure_score = float(signed.mean()) if not signed.empty else None
            support_basis = "directional_intensity"
            compiler_status = "populated"
        else:
            pressure_score = None
            support_basis = "support_only"
            compiler_status = "insufficient_directionality"
        channel_id = _hash_payload({
            "source": _clean(first.get("source")),
            "canonical_wave": _clean(first.get("canonical_wave")),
            "country_code": _clean(first.get("country_code")),
            "relation_axis_id": _clean(first.get("relation_axis_id")),
            "target_entity_id": _clean(first.get("target_entity_id")),
            "driver_facet_id": _clean(first.get("driver_facet_id")),
        })
        rows.append(
            {
                "run_id": run_id or _clean(first.get("run_id") or first.get("source_run_id")),
                "source": _clean(first.get("source")),
                "wave": _clean(first.get("wave")),
                "canonical_wave": _clean(first.get("canonical_wave")),
                "country_code": _clean(first.get("country_code")),
                "input_atom_count": n_atoms,
                "eligible_atom_count": n_atoms,
                "directionality_coverage": float(directionality_coverage),
                "support_basis": support_basis,
                "compiler_status": compiler_status,
                "input_atom_hash": _hash_payload({"rows": group.get("atom_id", pd.Series(dtype=str)).fillna("").astype(str).tolist()}),
                "input_hash": _hash_payload({"artifact": "structural_channel_index", "rows": group.get("atom_id", pd.Series(dtype=str)).fillna("").astype(str).tolist()}),
                "schema_version": V552_SCHEMA_VERSION,
                "created_at": pd.Timestamp.utcnow().isoformat(),
                "channel_id": channel_id,
                "channel_type": "relation_axis_target_driver_facet",
                "anchor_axis_id": _clean(first.get("relation_axis_id")),
                "anchor_target_id": _clean(first.get("target_entity_id")),
                "anchor_driver_facet_id": _clean(first.get("driver_facet_id")),
                "n_atoms": n_atoms,
                "n_unweighted_total": n_unweighted,
                "n_weighted_total": n_weighted,
                "pressure_score": pressure_score,
                "support_status": _support_status_from_support(n_unweighted, total_respondents=total_respondents),
                "confidence_tier": _confidence_tier_from_support(n_unweighted, total_respondents=total_respondents),
                "basis": "v551_atoms",
                "status": compiler_status,
            }
        )
    return pd.DataFrame(rows, columns=V552_STRUCTURAL_CHANNEL_INDEX_SCHEMA["required_columns"])


def build_contradiction_tensor(atoms: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    if atoms.empty or not _has_columns(atoms, ["response_direction", "response_intensity", "relation_axis_id", "target_entity_id", "driver_facet_id"]):
        return pd.DataFrame(columns=V552_CONTRADICTION_TENSOR_SCHEMA["required_columns"])
    directional = atoms.copy()
    directional["response_direction"] = directional["response_direction"].fillna("").astype(str).str.strip()
    directional["response_intensity"] = pd.to_numeric(directional.get("response_intensity", pd.Series(dtype=object)), errors="coerce")
    directional = directional[directional["response_direction"].ne("") & directional["response_intensity"].notna()]
    if directional.empty:
        return pd.DataFrame(columns=V552_CONTRADICTION_TENSOR_SCHEMA["required_columns"])
    rows: list[dict[str, Any]] = []
    group_cols = _common_group_columns(directional) + ["target_entity_id", "driver_facet_id"]
    for _, group in _group_frame(directional, group_cols):
        if "relation_axis_id" not in group.columns:
            continue
        axis_summary: list[dict[str, Any]] = []
        for axis_id, axis_group in group.groupby("relation_axis_id", dropna=False, sort=True):
            axis_directions, axis_intensities, axis_directionality_coverage = _directionality_frame(axis_group)
            axis_mask = axis_directions.ne("") & axis_intensities.notna()
            if not axis_mask.any():
                continue
            signed = axis_intensities.loc[axis_mask] * axis_directions.loc[axis_mask].map(_direction_sign).astype(float)
            axis_mean = float(signed.mean()) if not signed.empty else None
            positive_count = int((axis_directions.loc[axis_mask].map(_direction_sign) > 0).sum())
            negative_count = int((axis_directions.loc[axis_mask].map(_direction_sign) < 0).sum())
            if positive_count > negative_count:
                orientation = 1
            elif negative_count > positive_count:
                orientation = -1
            elif (axis_mean or 0.0) > 0:
                orientation = 1
            elif (axis_mean or 0.0) < 0:
                orientation = -1
            else:
                orientation = 0
            axis_summary.append(
                {
                    "axis_id": _clean(axis_id),
                    "positive_count": positive_count,
                    "negative_count": negative_count,
                    "orientation": orientation,
                    "axis_group": axis_group,
                    "axis_mean": axis_mean,
                }
            )
        if len(axis_summary) < 2:
            continue
        first = group.iloc[0].to_dict()
        total_respondents = _group_total_respondents(group)
        group_support = _support_status_from_support(float(group.get("n_unweighted", pd.Series([0] * len(group), index=group.index)).fillna(0).sum()), total_respondents=total_respondents)
        group_confidence = _confidence_tier_from_support(float(group.get("n_unweighted", pd.Series([0] * len(group), index=group.index)).fillna(0).sum()), total_respondents=total_respondents)
        for i, axis_a in enumerate(axis_summary):
            for axis_b in axis_summary[i + 1 :]:
                if axis_a["orientation"] == 0 or axis_b["orientation"] == 0 or axis_a["orientation"] == axis_b["orientation"]:
                    continue
                positive_axis = axis_a if axis_a["orientation"] > 0 else axis_b
                negative_axis = axis_b if positive_axis is axis_a else axis_a
                contradiction_id = _hash_payload({
                    "source": _clean(first.get("source")),
                    "canonical_wave": _clean(first.get("canonical_wave")),
                    "country_code": _clean(first.get("country_code")),
                    "target_entity_id": _clean(first.get("target_entity_id")),
                    "driver_facet_id": _clean(first.get("driver_facet_id")),
                    "axis_a": _clean(axis_a["axis_id"]),
                    "axis_b": _clean(axis_b["axis_id"]),
                })
                rows.append(
                    {
                        "run_id": run_id or _clean(first.get("run_id") or first.get("source_run_id")),
                        "source": _clean(first.get("source")),
                        "wave": _clean(first.get("wave")),
                        "canonical_wave": _clean(first.get("canonical_wave")),
                        "country_code": _clean(first.get("country_code")),
                        "input_atom_count": int(len(group)),
                        "eligible_atom_count": int(len(group)),
                        "directionality_coverage": float(_directionality_frame(group)[2]),
                        "support_basis": "directional_intensity",
                        "compiler_status": "populated",
                        "input_atom_hash": _hash_payload({"rows": group.get("atom_id", pd.Series(dtype=str)).fillna("").astype(str).tolist()}),
                "input_hash": _hash_payload({"artifact": "contradiction_tensor", "rows": group.get("atom_id", pd.Series(dtype=str)).fillna("").astype(str).tolist()}),
                "schema_version": V552_SCHEMA_VERSION,
                "created_at": pd.Timestamp.utcnow().isoformat(),
                "contradiction_id": contradiction_id,
                "axis_a": _clean(axis_a["axis_id"]),
                        "axis_b": _clean(axis_b["axis_id"]),
                        "target_entity_id": _clean(first.get("target_entity_id")),
                        "driver_facet_id": _clean(first.get("driver_facet_id")),
                        "positive_atom_count": int(positive_axis["positive_count"]),
                "negative_atom_count": int(negative_axis["negative_count"]),
                "opposing_directionality_present": True,
                "contradiction_score": float(min(positive_axis["positive_count"], negative_axis["negative_count"]) / max(positive_axis["positive_count"], negative_axis["negative_count"], 1)),
                "support_status": group_support,
                "confidence_tier": group_confidence,
                "basis": "v551_atoms",
                "status": "populated",
                "pressure_computation_status": "populated",
            }
        )
    return pd.DataFrame(rows, columns=V552_CONTRADICTION_TENSOR_SCHEMA["required_columns"])


def build_contradiction_surface(atoms: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    if atoms.empty or not _has_columns(atoms, ["response_direction", "response_intensity", "relation_axis_id", "target_entity_id", "driver_facet_id"]):
        return pd.DataFrame(columns=V552_CONTRADICTION_SURFACE_SCHEMA["required_columns"])
    directional = atoms.copy()
    directional["response_direction"] = directional["response_direction"].fillna("").astype(str).str.strip()
    directional["response_intensity"] = pd.to_numeric(directional.get("response_intensity", pd.Series(dtype=object)), errors="coerce")
    rows: list[dict[str, Any]] = []
    group_cols = _common_group_columns(directional) + ["target_entity_id", "driver_facet_id"]
    for _, group in _group_frame(directional, group_cols):
        if "relation_axis_id" not in group.columns:
            continue
        axis_summary: list[dict[str, Any]] = []
        for axis_id, axis_group in group.groupby("relation_axis_id", dropna=False, sort=True):
            axis_directions = _direction_mask(axis_group.get("response_direction", pd.Series(dtype=object)))
            axis_intensities = pd.to_numeric(axis_group.get("response_intensity", pd.Series(dtype=object)), errors="coerce")
            axis_mask = axis_directions.ne("") & axis_intensities.notna()
            axis_unsigned = int(len(axis_group) - int(axis_mask.sum()))
            if not axis_mask.any():
                continue
            signed_directions = axis_directions.loc[axis_mask].map(_direction_sign).astype(int)
            signed_intensities = axis_intensities.loc[axis_mask] * signed_directions.astype(float)
            axis_pressure = float(signed_intensities.mean()) if not signed_intensities.empty else None
            positive_count = int((signed_directions > 0).sum())
            negative_count = int((signed_directions < 0).sum())
            neutral_count = int((signed_directions == 0).sum())
            if positive_count > negative_count:
                orientation = 1
            elif negative_count > positive_count:
                orientation = -1
            elif (axis_pressure or 0.0) > 0:
                orientation = 1
            elif (axis_pressure or 0.0) < 0:
                orientation = -1
            else:
                orientation = 0
            axis_summary.append(
                {
                    "axis_id": _clean(axis_id),
                    "n_atoms": int(len(axis_group)),
                    "n_directional_atoms": int(axis_mask.sum()),
                    "n_positive_atoms": positive_count,
                    "n_negative_atoms": negative_count,
                    "n_neutral_atoms": neutral_count,
                    "n_unsigned_atoms": axis_unsigned,
                    "orientation": orientation,
                    "mixed_sign": bool(positive_count > 0 and negative_count > 0),
                    "pressure_score": axis_pressure,
                }
            )
        if not axis_summary:
            continue
        first = group.iloc[0].to_dict()
        total_respondents = _group_total_respondents(group)
        directional_mask = _direction_mask(group.get("response_direction", pd.Series(dtype=object))).ne("") & pd.to_numeric(group.get("response_intensity", pd.Series(dtype=object)), errors="coerce").notna()
        signed_directions = group.loc[directional_mask, "response_direction"].map(_direction_sign).astype(int) if directional_mask.any() else pd.Series(dtype=int)
        signed_intensities = pd.to_numeric(group.loc[directional_mask, "response_intensity"], errors="coerce") * signed_directions.astype(float) if directional_mask.any() else pd.Series(dtype=float)
        dominant_axis = max(axis_summary, key=lambda item: (int(item["n_directional_atoms"]), abs(float(item["pressure_score"] or 0.0))))
        n_axes_positive = int(sum(1 for axis in axis_summary if int(axis["orientation"]) > 0))
        n_axes_negative = int(sum(1 for axis in axis_summary if int(axis["orientation"]) < 0))
        n_axes_neutral = int(sum(1 for axis in axis_summary if int(axis["orientation"]) == 0))
        n_axes_mixed_sign = int(sum(1 for axis in axis_summary if bool(axis["mixed_sign"])))
        pocket_mixed_sign = n_axes_mixed_sign > 0
        cross_axis_opposition_present = n_axes_positive > 0 and n_axes_negative > 0
        contradiction_potential = pocket_mixed_sign or cross_axis_opposition_present
        rows.append(
            {
                "run_id": run_id or _clean(first.get("run_id") or first.get("source_run_id")),
                "source": _clean(first.get("source")),
                "wave": _clean(first.get("wave")),
                "canonical_wave": _clean(first.get("canonical_wave")),
                "country_code": _clean(first.get("country_code")),
                "input_atom_count": int(len(group)),
                "eligible_atom_count": int(len(group)),
                "directionality_coverage": float(directional_mask.mean()) if len(group) else 0.0,
                "support_basis": "directional_intensity" if directional_mask.any() else "support_only",
                "compiler_status": "populated" if directional_mask.any() else "support_summary_only",
                "pressure_computation_status": "populated" if directional_mask.any() else "support_summary_only",
                "input_atom_hash": _hash_payload({"rows": group.get("atom_id", pd.Series(dtype=str)).fillna("").astype(str).tolist()}),
                "input_hash": _hash_payload({"artifact": "contradiction_surface", "rows": group.get("atom_id", pd.Series(dtype=str)).fillna("").astype(str).tolist()}),
                "schema_version": V552_SCHEMA_VERSION,
                "created_at": pd.Timestamp.utcnow().isoformat(),
                "contradiction_surface_id": _hash_payload(
                    {
                        "source": _clean(first.get("source")),
                        "canonical_wave": _clean(first.get("canonical_wave")),
                        "country_code": _clean(first.get("country_code")),
                        "target_entity_id": _clean(first.get("target_entity_id")),
                        "driver_facet_id": _clean(first.get("driver_facet_id")),
                        "axes": [axis["axis_id"] for axis in axis_summary],
                    }
                ),
                "target_entity_id": _clean(first.get("target_entity_id")),
                "driver_facet_id": _clean(first.get("driver_facet_id")),
                "n_relation_axes": int(group["relation_axis_id"].fillna("").astype(str).str.strip().replace("", pd.NA).dropna().nunique()),
                "n_axes_positive": n_axes_positive,
                "n_axes_negative": n_axes_negative,
                "n_axes_neutral": n_axes_neutral,
                "n_axes_mixed_sign": n_axes_mixed_sign,
                "n_atoms": int(len(group)),
                "n_unweighted_total": float(pd.to_numeric(group.get("n_unweighted", pd.Series([0] * len(group), index=group.index)), errors="coerce").fillna(0).sum()),
                "n_weighted_total": float(pd.to_numeric(group.get("n_weighted", pd.Series([0.0] * len(group), index=group.index)), errors="coerce").fillna(0).sum()),
                "n_directional_atoms": int(directional_mask.sum()),
                "n_positive_atoms": int((signed_directions > 0).sum()) if not signed_directions.empty else 0,
                "n_negative_atoms": int((signed_directions < 0).sum()) if not signed_directions.empty else 0,
                "n_neutral_atoms": int((signed_directions == 0).sum()) if not signed_directions.empty else 0,
                "n_unsigned_atoms": int(len(group) - int(directional_mask.sum())),
                "pressure_score": float(signed_intensities.mean()) if not signed_intensities.empty else None,
                "entropy": _entropy(group.get("response_direction", pd.Series(dtype=object))),
                "polarization_index": float(max(0.0, 1.0 - (_dominant_orientation(group.get("response_direction", pd.Series(dtype=object)))[1] if len(group) else 0.0))),
                "dominant_orientation": _dominant_orientation(group.get("response_direction", pd.Series(dtype=object)))[0],
                "dominant_relation_axis_id": dominant_axis["axis_id"],
                "cross_axis_opposition_present": cross_axis_opposition_present,
                "contradiction_potential": contradiction_potential,
                "axis_summary_json": json.dumps(axis_summary, sort_keys=True, default=str),
                "axis_orientation_counts_json": json.dumps(
                    {
                        "positive": n_axes_positive,
                        "negative": n_axes_negative,
                        "neutral": n_axes_neutral,
                        "mixed_sign": n_axes_mixed_sign,
                    },
                    sort_keys=True,
                ),
                "support_status": _support_status_from_support(float(pd.to_numeric(group.get("n_unweighted", pd.Series([0] * len(group), index=group.index)), errors="coerce").fillna(0).sum()), total_respondents=total_respondents),
                "confidence_tier": _confidence_tier_from_support(float(pd.to_numeric(group.get("n_unweighted", pd.Series([0] * len(group), index=group.index)), errors="coerce").fillna(0).sum()), total_respondents=total_respondents),
                "basis": "v551_atoms",
                "status": "populated" if directional_mask.any() else "support_summary_only",
            }
        )
    return pd.DataFrame(rows, columns=V552_CONTRADICTION_SURFACE_SCHEMA["required_columns"])


def build_horizon_constraint_index(atoms: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    if atoms.empty or not _has_columns(atoms, ["relation_axis_id", "target_entity_id", "driver_facet_id"]):
        return pd.DataFrame(columns=V552_HORIZON_CONSTRAINT_INDEX_SCHEMA["required_columns"])
    rows: list[dict[str, Any]] = []
    group_cols = _common_group_columns(atoms) + ["relation_axis_id", "target_entity_id", "driver_facet_id"]
    for _, group in _group_frame(atoms, group_cols):
        first = group.iloc[0].to_dict()
        n_atoms = int(len(group))
        total_respondents = _group_total_respondents(group)
        n_unweighted = float(pd.to_numeric(group.get("n_unweighted", pd.Series([0] * len(group), index=group.index)), errors="coerce").fillna(0).sum())
        n_weighted = float(pd.to_numeric(group.get("n_weighted", pd.Series([0.0] * len(group), index=group.index)), errors="coerce").fillna(0).sum())
        support_status = _support_status_from_support(n_unweighted, total_respondents=total_respondents)
        directional_mask = _direction_mask(group.get("response_direction", pd.Series(dtype=object))).ne("") & pd.to_numeric(group.get("response_intensity", pd.Series(dtype=object)), errors="coerce").notna()
        support_threshold = support_threshold_from_total(total_respondents)
        has_directionality = bool(directional_mask.any())
        insufficient_atom_count = n_atoms < support_threshold
        if not insufficient_atom_count and has_directionality:
            continue
        sufficient_support = support_status == "sufficient_support"
        if insufficient_atom_count or not sufficient_support:
            horizon_dimension = "support_gap"
            if not sufficient_support and insufficient_atom_count:
                constraint_reason = "insufficient support and insufficient atom count for conservative horizon summary"
            elif insufficient_atom_count:
                constraint_reason = "insufficient atom count for conservative horizon summary"
            else:
                constraint_reason = "insufficient support for conservative horizon summary"
        else:
            horizon_dimension = "directionality_gap"
            constraint_reason = "sufficient support exists, but signed directionality is absent; conservative horizon summary only"
        if has_directionality:
            signed = pd.to_numeric(group.loc[directional_mask, "response_intensity"], errors="coerce") * group.loc[directional_mask, "response_direction"].map(_direction_sign).astype(float)
            constraint_signal_score = float(abs(signed.mean())) if not signed.empty else None
            compiler_status = "support_summary_only"
            support_basis = "directional_intensity" if sufficient_support else "support_only"
        else:
            constraint_signal_score = None
            compiler_status = "support_summary_only"
            support_basis = "support_only"
        rows.append(
            {
                "run_id": run_id or _clean(first.get("run_id") or first.get("source_run_id")),
                "source": _clean(first.get("source")),
                "wave": _clean(first.get("wave")),
                "canonical_wave": _clean(first.get("canonical_wave")),
                "country_code": _clean(first.get("country_code")),
                "input_atom_count": n_atoms,
                "eligible_atom_count": n_atoms,
                "directionality_coverage": float(directional_mask.mean()) if len(group) else 0.0,
                "support_basis": support_basis,
                "compiler_status": compiler_status,
                "input_atom_hash": _hash_payload({"rows": group.get("atom_id", pd.Series(dtype=str)).fillna("").astype(str).tolist()}),
                "input_hash": _hash_payload({"artifact": "horizon_constraint_index", "rows": group.get("atom_id", pd.Series(dtype=str)).fillna("").astype(str).tolist()}),
                "schema_version": V552_SCHEMA_VERSION,
                "created_at": pd.Timestamp.utcnow().isoformat(),
                "horizon_constraint_id": _hash_payload({
                    "source": _clean(first.get("source")),
                    "canonical_wave": _clean(first.get("canonical_wave")),
                    "country_code": _clean(first.get("country_code")),
                    "relation_axis_id": _clean(first.get("relation_axis_id")),
                    "target_entity_id": _clean(first.get("target_entity_id")),
                    "driver_facet_id": _clean(first.get("driver_facet_id")),
                    "horizon_dimension": horizon_dimension,
                }),
                "horizon_dimension": horizon_dimension,
                "basis_relation_axis_id": _clean(first.get("relation_axis_id")),
                "basis_target_entity_id": _clean(first.get("target_entity_id")),
                "basis_driver_facet_id": _clean(first.get("driver_facet_id")),
                "n_atoms": n_atoms,
                "n_unweighted_total": n_unweighted,
                "n_weighted_total": n_weighted,
                "constraint_signal_score": constraint_signal_score,
                "support_status": support_status,
                "confidence_tier": _confidence_tier_from_support(n_unweighted, total_respondents=total_respondents),
                "basis": "v551_atoms",
                "status": compiler_status,
                "pressure_computation_status": compiler_status,
                "constraint_reason": constraint_reason,
            }
        )
    return pd.DataFrame(rows, columns=V552_HORIZON_CONSTRAINT_INDEX_SCHEMA["required_columns"])


def _build_conditional_determinicity_status_audit(
    conditional_determinicity: pd.DataFrame | None,
    *,
    run_id: str = "",
    conditional_input_path: str = "",
    conditional_input_hash: str = "",
) -> pd.DataFrame:
    if conditional_determinicity is None:
        created_at = pd.Timestamp.utcnow().isoformat()
        return pd.DataFrame(
            [
                {
                    "run_id": run_id,
                    "artifact_name": "conditional_determinicity_status_audit",
                    "supplied": False,
                    "input_row_count": 0,
                    "row_count": 0,
                    "compiler_status": "conditional_determinicity_not_supplied",
                    "status_reason": "no conditional determinicity input supplied to V552",
                    "conditional_input_path": conditional_input_path,
                    "conditional_input_hash": conditional_input_hash or "",
                    "input_hash": _hash_payload({"artifact": "conditional_determinicity_status_audit", "supplied": False, "rows": []}),
                    "conditional_row_count": 0,
                    "status": "conditional_determinicity_not_supplied",
                    "used_as_direct_pressure": False,
                    "used_as_status_context": True,
                    "created_at": created_at,
                }
            ]
        )

    frame = conditional_determinicity.copy()
    used_as_status_context = True
    if frame.empty:
        status = "status_only_conditional_input"
        status_reason = "conditional determinicity input supplied but empty"
        conditional_row_count = 0
        supplied = True
        conditional_input_hash = conditional_input_hash or _hash_payload({"rows": []})
        input_hash = _hash_payload({"artifact": "conditional_determinicity_status_audit", "supplied": True, "rows": []})
    else:
        status = "status_only_conditional_input"
        status_reason = "conditional determinicity input supplied as status/context only"
        conditional_row_count = int(len(frame))
        supplied = True
        conditional_input_hash = conditional_input_hash or _hash_payload({"rows": frame.get("conditional_id", pd.Series(dtype=str)).fillna("").astype(str).tolist()})
        input_hash = _hash_payload({"artifact": "conditional_determinicity_status_audit", "supplied": True, "rows": frame.get("conditional_id", pd.Series(dtype=str)).fillna("").astype(str).tolist()})
    return pd.DataFrame(
        [
            {
                "run_id": run_id,
                "artifact_name": "conditional_determinicity_status_audit",
                "supplied": supplied,
                "input_row_count": conditional_row_count,
                "row_count": conditional_row_count,
                "conditional_input_path": conditional_input_path,
                "conditional_input_hash": conditional_input_hash,
                "input_hash": input_hash,
                "conditional_row_count": conditional_row_count,
                "compiler_status": status if supplied else "conditional_determinicity_not_supplied",
                "status": status if supplied else "conditional_determinicity_not_supplied",
                "status_reason": status_reason,
                "used_as_direct_pressure": False,
                "used_as_status_context": used_as_status_context,
                "created_at": pd.Timestamp.utcnow().isoformat(),
            }
        ],
    )


def build_v552_directionality_coverage_audit(atoms: pd.DataFrame, *, run_id: str = "") -> pd.DataFrame:
    created_at = pd.Timestamp.utcnow().isoformat()
    input_atom_hash = _hash_payload({"rows": atoms.get("atom_id", pd.Series(dtype=str)).fillna("").astype(str).tolist()}) if not atoms.empty else _hash_payload({"rows": []})
    input_hash = _hash_payload({"artifact": "v552_directionality_coverage_audit", "rows": atoms.get("atom_id", pd.Series(dtype=str)).fillna("").astype(str).tolist()}) if not atoms.empty else _hash_payload({"artifact": "v552_directionality_coverage_audit", "rows": []})
    rows: list[dict[str, Any]] = []

    def _row(grouping_level: str, grouping_key: str, frame: pd.DataFrame) -> dict[str, Any]:
        direction_mask = _direction_mask(frame.get("response_direction", pd.Series(dtype=object))).ne("")
        intensity = pd.to_numeric(frame.get("response_intensity", pd.Series(dtype=object)), errors="coerce")
        both_mask = direction_mask & intensity.notna()
        atom_count = int(len(frame))
        return {
            "run_id": run_id,
            "grouping_level": grouping_level,
            "grouping_key": grouping_key,
            "source": _clean(frame.iloc[0].get("source")) if not frame.empty and "source" in frame.columns else "",
            "wave": _clean(frame.iloc[0].get("wave")) if not frame.empty and "wave" in frame.columns else "",
            "canonical_wave": _clean(frame.iloc[0].get("canonical_wave")) if not frame.empty and "canonical_wave" in frame.columns else "",
            "country_code": _clean(frame.iloc[0].get("country_code")) if not frame.empty and "country_code" in frame.columns else "",
            "atom_count": atom_count,
            "atoms_with_response_direction": int(direction_mask.sum()),
            "atoms_with_response_intensity": int(intensity.notna().sum()),
            "atoms_with_both_direction_and_intensity": int(both_mask.sum()),
            "directionality_coverage": float(direction_mask.mean()) if atom_count else 0.0,
            "intensity_coverage": float(intensity.notna().mean()) if atom_count else 0.0,
            "both_coverage": float(both_mask.mean()) if atom_count else 0.0,
            "directionality_status": "full_directionality" if atom_count and both_mask.all() else "partial_directionality" if both_mask.any() else "no_directionality" if atom_count else "not_applicable",
            "input_atom_hash": input_atom_hash,
            "input_hash": input_hash,
            "created_at": created_at,
        }

    if atoms.empty:
        for level in ["global", "relation_axis_id", "target_entity_id", "driver_facet_id", "country_wave"]:
            rows.append(_row(level, level, atoms))
        return pd.DataFrame(rows, columns=V552_DIRECTIONALITY_COVERAGE_AUDIT_SCHEMA["required_columns"])

    rows.append(_row("global", "global", atoms))
    for level, cols in [
        ("relation_axis_id", ["relation_axis_id"]),
        ("target_entity_id", ["target_entity_id"]),
        ("driver_facet_id", ["driver_facet_id"]),
        ("country_wave", [c for c in ["source", "wave", "canonical_wave", "country_code"] if c in atoms.columns]),
    ]:
        if not cols:
            continue
        group_cols = cols
        for key, group in atoms.groupby(group_cols, dropna=False, sort=True):
            if not isinstance(key, tuple):
                key = (key,)
            key_text = "|".join(_clean(value) for value in key)
            rows.append(_row(level, key_text, group))
    return pd.DataFrame(rows, columns=V552_DIRECTIONALITY_COVERAGE_AUDIT_SCHEMA["required_columns"])


def _directionality_gap_surface_row(group: pd.DataFrame, *, run_id: str = "", scope: str = "axis_group") -> dict[str, Any]:
    first = group.iloc[0].to_dict()
    n_atoms = int(len(group))
    directional_mask = _direction_mask(group.get("response_direction", pd.Series(dtype=object))).ne("") & pd.to_numeric(group.get("response_intensity", pd.Series(dtype=object)), errors="coerce").notna()
    n_directional_atoms = int(directional_mask.sum())
    n_unsigned_atoms = int(n_atoms - n_directional_atoms)
    n_signed_atoms = int(n_directional_atoms)
    n_unweighted = float(pd.to_numeric(group.get("n_unweighted", pd.Series([0] * len(group), index=group.index)), errors="coerce").fillna(0).sum())
    n_weighted = float(pd.to_numeric(group.get("n_weighted", pd.Series([0.0] * len(group), index=group.index)), errors="coerce").fillna(0).sum())
    total_respondents = _group_total_respondents(group)
    directionality_coverage = float(directional_mask.mean()) if n_atoms else 0.0
    gap_score = float(1.0 - directionality_coverage)
    support_status = _support_status_from_support(n_unweighted, total_respondents=total_respondents)
    confidence_tier = _confidence_tier_from_support(n_unweighted, total_respondents=total_respondents)
    if n_directional_atoms == 0:
        reason = "no_directionality"
        priority = "high" if support_status == "sufficient_support" else "medium"
        compiler_status = "support_summary_only"
    elif n_directional_atoms < n_atoms:
        reason = "partial_directionality"
        priority = "medium"
        compiler_status = "support_summary_only"
    else:
        reason = "full_directionality"
        priority = "low"
        compiler_status = "populated"
    return {
        "run_id": run_id or _clean(first.get("run_id") or first.get("source_run_id")),
        "source": _clean(first.get("source")),
        "wave": _clean(first.get("wave")),
        "canonical_wave": _clean(first.get("canonical_wave")),
        "country_code": _clean(first.get("country_code")),
        "relation_axis_id": _clean(first.get("relation_axis_id")),
        "target_entity_id": _clean(first.get("target_entity_id")),
        "driver_facet_id": _clean(first.get("driver_facet_id")),
        "gap_surface_id": _hash_payload(
            {
                "source": _clean(first.get("source")),
                "wave": _clean(first.get("wave")),
                "canonical_wave": _clean(first.get("canonical_wave")),
                "country_code": _clean(first.get("country_code")),
                "relation_axis_id": _clean(first.get("relation_axis_id")),
                "target_entity_id": _clean(first.get("target_entity_id")),
                "driver_facet_id": _clean(first.get("driver_facet_id")),
                "scope": scope,
                "reason": reason,
            }
        ),
        "gap_surface_scope": scope,
        "gap_surface_reason": reason,
        "gap_surface_priority": priority,
        "n_atoms": n_atoms,
        "n_directional_atoms": n_directional_atoms,
        "n_unsigned_atoms": n_unsigned_atoms,
        "n_unweighted_total": n_unweighted,
        "n_weighted_total": n_weighted,
        "directionality_coverage": directionality_coverage,
        "directionality_gap_score": gap_score,
        "support_status": support_status,
        "confidence_tier": confidence_tier,
        "pressure_computation_status": compiler_status,
        "basis": "v551_atoms",
        "status": compiler_status,
        "created_at": pd.Timestamp.utcnow().isoformat(),
    }


def build_v552_directionality_gap_surface(atoms: pd.DataFrame, *, run_id: str = "") -> pd.DataFrame:
    required = ["relation_axis_id", "target_entity_id", "driver_facet_id"]
    if atoms.empty or not _has_columns(atoms, required):
        return pd.DataFrame(columns=V552_DIRECTIONALITY_GAP_SURFACE_SCHEMA["required_columns"])
    rows: list[dict[str, Any]] = []
    group_cols = _common_group_columns(atoms) + required
    for _, group in _group_frame(atoms, group_cols):
        row = _directionality_gap_surface_row(group, run_id=run_id, scope="axis_group")
        if row["gap_surface_reason"] != "full_directionality":
            rows.append(row)
    frame = pd.DataFrame(rows, columns=V552_DIRECTIONALITY_GAP_SURFACE_SCHEMA["required_columns"])
    if not frame.empty:
        frame = frame.sort_values(["gap_surface_priority", "source", "canonical_wave", "country_code", "relation_axis_id", "target_entity_id", "driver_facet_id"], ascending=[False, True, True, True, True, True, True], kind="mergesort").reset_index(drop=True)
    return frame


def build_v552_status_pressure_review_surface(atoms: pd.DataFrame, *, run_id: str = "") -> pd.DataFrame:
    required = ["relation_axis_id", "target_entity_id", "driver_facet_id"]
    if atoms.empty or not _has_columns(atoms, required):
        return pd.DataFrame(columns=V552_STATUS_PRESSURE_REVIEW_SCHEMA["required_columns"])
    rows: list[dict[str, Any]] = []
    group_cols = _common_group_columns(atoms) + required
    for _, group in _group_frame(atoms, group_cols):
        first = group.iloc[0].to_dict()
        n_atoms = int(len(group))
        directional_mask = _direction_mask(group.get("response_direction", pd.Series(dtype=object))).ne("") & pd.to_numeric(group.get("response_intensity", pd.Series(dtype=object)), errors="coerce").notna()
        n_directional_atoms = int(directional_mask.sum())
        n_unsigned_atoms = int(n_atoms - n_directional_atoms)
        n_signed_atoms = int(directional_mask.sum())
        n_unweighted = float(pd.to_numeric(group.get("n_unweighted", pd.Series([0] * len(group), index=group.index)), errors="coerce").fillna(0).sum())
        n_weighted = float(pd.to_numeric(group.get("n_weighted", pd.Series([0.0] * len(group), index=group.index)), errors="coerce").fillna(0).sum())
        total_respondents = _group_total_respondents(group)
        support_status = _support_status_from_support(n_unweighted, total_respondents=total_respondents)
        confidence_tier = _confidence_tier_from_support(n_unweighted, total_respondents=total_respondents)
        if support_status == "sufficient_support" and n_directional_atoms == 0:
            reason = "support_without_directionality"
            priority = "high"
            compiler_status = "review_required"
        elif support_status == "sufficient_support" and n_unsigned_atoms > 0:
            reason = "status_pressure_with_partial_directionality"
            priority = "medium"
            compiler_status = "review_required"
        elif support_status != "sufficient_support" and n_directional_atoms == 0:
            reason = "support_gap_no_directionality"
            priority = "low"
            compiler_status = "support_summary_only"
        elif support_status != "sufficient_support" and n_unsigned_atoms > 0:
            reason = "support_gap_partial_directionality"
            priority = "low"
            compiler_status = "support_summary_only"
        else:
            reason = "support_gap_no_directionality"
            priority = "low"
            compiler_status = "support_summary_only"
        rows.append(
            {
                "run_id": run_id or _clean(first.get("run_id") or first.get("source_run_id")),
                "source": _clean(first.get("source")),
                "wave": _clean(first.get("wave")),
                "canonical_wave": _clean(first.get("canonical_wave")),
                "country_code": _clean(first.get("country_code")),
                "relation_axis_id": _clean(first.get("relation_axis_id")),
                "target_entity_id": _clean(first.get("target_entity_id")),
                "driver_facet_id": _clean(first.get("driver_facet_id")),
                "status_pressure_id": _hash_payload(
                    {
                        "source": _clean(first.get("source")),
                        "wave": _clean(first.get("wave")),
                        "canonical_wave": _clean(first.get("canonical_wave")),
                        "country_code": _clean(first.get("country_code")),
                        "relation_axis_id": _clean(first.get("relation_axis_id")),
                        "target_entity_id": _clean(first.get("target_entity_id")),
                        "driver_facet_id": _clean(first.get("driver_facet_id")),
                        "reason": reason,
                    }
                ),
                "status_pressure_scope": "axis_group",
                "status_pressure_reason": reason,
                "status_pressure_priority": priority,
                "n_atoms": n_atoms,
                "n_directional_atoms": n_directional_atoms,
                "n_signed_atoms": n_signed_atoms,
                "n_unsigned_atoms": n_unsigned_atoms,
                "n_unweighted_total": n_unweighted,
                "n_weighted_total": n_weighted,
                "directionality_coverage": float(directional_mask.mean()) if n_atoms else 0.0,
                "support_status": support_status,
                "confidence_tier": confidence_tier,
                "pressure_computation_status": "support_summary_only" if support_status != "sufficient_support" or n_directional_atoms == 0 else "populated",
                "basis": "v551_atoms",
                "status": compiler_status,
                "created_at": pd.Timestamp.utcnow().isoformat(),
            }
        )
    frame = pd.DataFrame(rows, columns=V552_STATUS_PRESSURE_REVIEW_SCHEMA["required_columns"])
    if not frame.empty:
        frame = frame.sort_values(["status_pressure_priority", "source", "canonical_wave", "country_code", "relation_axis_id", "target_entity_id", "driver_facet_id"], ascending=[False, True, True, True, True, True, True], kind="mergesort").reset_index(drop=True)
    return frame


def build_v552_status_audit(
    artifact_specs: list[dict[str, Any]],
    *,
    run_id: str,
    input_atom_hash: str,
    input_atom_count: int,
    eligible_atom_count: int,
    support_basis: str,
    has_sufficient_directionality: bool,
    final_status: str,
    context: dict[str, Any] | None = None,
    created_at: str | None = None,
) -> pd.DataFrame:
    created_at = created_at or pd.Timestamp.utcnow().isoformat()
    context = context or {}
    rows: list[dict[str, Any]] = []
    for spec in artifact_specs:
        rows.append(
            {
                "run_id": run_id,
                "artifact_name": spec.get("artifact_name", ""),
                "artifact_path_csv": spec.get("artifact_path_csv", ""),
                "artifact_path_parquet": spec.get("artifact_path_parquet", ""),
                "row_count": int(spec.get("row_count", 0)),
                "input_atom_count": int(input_atom_count),
                "eligible_atom_count": int(eligible_atom_count),
                "compiler_status": normalize_v552_status(spec.get("compiler_status", "not_applicable")),
                "status_reason": _clean(spec.get("status_reason")),
                "requires_directionality": bool(spec.get("requires_directionality", False)),
                "has_sufficient_directionality": bool(has_sufficient_directionality),
                "support_basis": support_basis,
                "input_atom_hash": input_atom_hash,
                "input_hash": _hash_payload({"artifact": spec.get("artifact_name", ""), "input_atom_hash": input_atom_hash, "row_count": int(spec.get("row_count", 0))}),
                "schema_version": V552_SCHEMA_VERSION,
                "created_at": created_at,
                "response_semantics_status": _clean(context.get("response_semantics_status")),
                "response_semantics_source": _clean(context.get("response_semantics_source")),
                "response_semantics_contract_hash": _clean(context.get("response_semantics_contract_hash")),
                "source_structure_source": _clean(context.get("source_structure_source")),
                "source_structure_basis": _clean(context.get("source_structure_basis")),
                "source_structure_confidence": _clean(context.get("source_structure_confidence")),
                "source": _clean(context.get("source")),
                "wave": _clean(context.get("wave")),
                "canonical_wave": _clean(context.get("canonical_wave")),
                "country_code": _clean(context.get("country_code")),
                "lane": _clean(spec.get("lane", "structural")),
                "final_status": normalize_v552_status(final_status),
            }
        )
    return pd.DataFrame(rows)


def build_v552_input_provenance_manifest(
    *,
    run_id: str,
    atoms_path: str,
    atoms_input_hash: str,
    atoms_row_count: int,
    atoms_required_columns_present: bool,
    atoms_missing_required_columns: list[str],
    conditional_determinicity_path: str | None,
    conditional_determinicity_hash: str | None,
    conditional_determinicity_row_count: int | None,
    output_root: str,
    output_dir: str,
    final_status: str,
    conditional_determinicity_supplied: bool,
    command_provenance: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload = {
        "run_id": run_id,
        "created_at": pd.Timestamp.utcnow().isoformat(),
        "compiler": "compile_v552_structural_ddm.py",
        "compiler_scope": "v552_structural_handoff_only",
        "atoms_path": atoms_path,
        "atoms_input_hash": atoms_input_hash,
        "atoms_row_count": int(atoms_row_count),
        "atoms_required_columns_present": bool(atoms_required_columns_present),
        "atoms_missing_required_columns": atoms_missing_required_columns,
        "conditional_determinicity_path": conditional_determinicity_path,
        "conditional_determinicity_hash": conditional_determinicity_hash,
        "conditional_determinicity_row_count": conditional_determinicity_row_count,
        "output_root": output_root,
        "output_dir": output_dir,
        "schema_version": V552_HANOFF_SCHEMA_VERSION,
        "upstream_boundary_frozen": True,
        "upstream_files_modified": False,
        "v553_implemented": False,
        "parent_persona_implemented": False,
        "final_status": normalize_v552_status(final_status),
        "conditional_determinicity_supplied": bool(conditional_determinicity_supplied),
    }
    if command_provenance:
        payload.update(command_provenance)
    return payload


def build_v552_artifact_authority_index(
    artifact_specs: list[dict[str, Any]],
    *,
    run_id: str = "",
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for spec in artifact_specs:
        artifact_name = _clean(spec.get("artifact_name"))
        compiler_status = _clean(spec.get("compiler_status"))
        lane = _clean(spec.get("lane")) or "structural"
        structural_level_only = lane in {"structural", "audit", "manifest"}
        not_runtime_consumable = True
        if lane == "manifest":
            allowed_v552j_use = "v552j_manifest_context_only"
        elif lane == "audit":
            allowed_v552j_use = "v552j_audit_context_only"
        else:
            allowed_v552j_use = "v552j_structural_context_only"
        rows.append(
            {
                "run_id": run_id,
                "artifact_name": artifact_name,
                "artifact_path_csv": _clean(spec.get("artifact_path_csv")),
                "artifact_path_parquet": _clean(spec.get("artifact_path_parquet")),
                "lane": lane,
                "compiler_status": compiler_status,
                "status_reason": _clean(spec.get("status_reason")),
                "requires_directionality": bool(spec.get("requires_directionality", False)),
                "structural_level_only": structural_level_only,
                "not_runtime_consumable": not_runtime_consumable,
                "allowed_v552j_use": allowed_v552j_use,
                "forbidden_downstream_use": "runtime_persona_generation|prompt_generation|biography_generation",
                "created_at": pd.Timestamp.utcnow().isoformat(),
                "schema_version": V552_SCHEMA_VERSION,
            }
        )
    return pd.DataFrame(rows, columns=V552_ARTIFACT_AUTHORITY_INDEX_SCHEMA["required_columns"])


def build_v552_known_absence_register(
    artifact_specs: list[dict[str, Any]],
    *,
    run_id: str = "",
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for spec in artifact_specs:
        compiler_status = _clean(spec.get("compiler_status"))
        artifact_name = _clean(spec.get("artifact_name"))
        if compiler_status in {"populated", "not_applicable"}:
            continue
        absence_type = "directionality_gap" if "directionality" in compiler_status else ("grouping_gap" if "grouping" in compiler_status else ("support_only" if "support" in compiler_status else "missing_context"))
        rows.append(
            {
                "run_id": run_id,
                "absence_id": _hash_payload(
                    {
                        "run_id": run_id,
                        "artifact_name": artifact_name,
                        "compiler_status": compiler_status,
                        "status_reason": _clean(spec.get("status_reason")),
                    }
                ),
                "artifact_name": artifact_name,
                "absence_type": absence_type,
                "absence_status": "recorded",
                "absence_reason": _clean(spec.get("status_reason")) or compiler_status,
                "missing_condition_json": json.dumps(
                    {
                        "requires_directionality": bool(spec.get("requires_directionality", False)),
                        "lane": _clean(spec.get("lane")) or "structural",
                        "compiler_status": compiler_status,
                    },
                    sort_keys=True,
                    ensure_ascii=False,
                ),
                "lane": _clean(spec.get("lane")) or "structural",
                "compiler_status": compiler_status,
                "requires_directionality": bool(spec.get("requires_directionality", False)),
                "created_at": pd.Timestamp.utcnow().isoformat(),
                "schema_version": V552_SCHEMA_VERSION,
            }
        )
    return pd.DataFrame(rows, columns=V552_KNOWN_ABSENCE_REGISTER_SCHEMA["required_columns"])


def build_v552_readiness_report(
    *,
    run_id: str,
    atoms_row_count: int,
    artifact_authority_index: pd.DataFrame,
    known_absence_register: pd.DataFrame,
    handoff_index: pd.DataFrame,
    final_status: str,
) -> pd.DataFrame:
    compile_status = normalize_v552_status(final_status)
    structural_ready = compile_status == "STATUS: READY_V552_STRUCTURAL_HANDOFF"
    directionality_ready = compile_status in {"STATUS: READY_V552_STRUCTURAL_HANDOFF", "STATUS: READY_V552_STATUS_ONLY_INSUFFICIENT_DIRECTIONALITY"}
    horizon_ready = structural_ready or directionality_ready
    contradiction_ready = structural_ready or directionality_ready
    parent_prior_ready = structural_ready or directionality_ready
    v552j_handoff_ready = not handoff_index.empty
    v553_comparability_ready = bool(handoff_index.get("v553_comparability_key", pd.Series(dtype=object)).astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if not handoff_index.empty else False
    runtime_ready = "NOT_RUNTIME_READY_REQUIRES_V552J"
    ready_for_v552j_inspection = bool(v552j_handoff_ready and artifact_authority_index is not None)
    ready_for_v553_after_v552j = bool(v553_comparability_ready and v552j_handoff_ready and structural_ready)
    now = pd.Timestamp.utcnow().isoformat()
    row = {
        "run_id": run_id,
        "v552_compile_status": compile_status,
        "v552_structural_readiness": "ready" if structural_ready else "ready_with_gaps" if atoms_row_count else "empty",
        "v552_directionality_readiness": "ready" if directionality_ready else "gapped",
        "v552_horizon_readiness": "ready" if horizon_ready else "gapped",
        "v552_contradiction_readiness": "ready" if contradiction_ready else "gapped",
        "v552_parent_prior_readiness": "ready" if parent_prior_ready else "gapped",
        "v552_v552j_handoff_readiness": "ready" if v552j_handoff_ready else "gapped",
        "v552_v553_comparability_readiness": "ready" if v553_comparability_ready else "gapped",
        "v552_runtime_readiness": runtime_ready,
        "ready_for_v552j_inspection": ready_for_v552j_inspection,
        "ready_for_v553_after_v552j": ready_for_v553_after_v552j,
        "input_atom_count": int(atoms_row_count),
        "output_artifact_count": int(len(artifact_authority_index)),
        "artifact_authority_rows": int(len(artifact_authority_index)),
        "known_absence_rows": int(len(known_absence_register)),
        "handoff_index_rows": int(len(handoff_index)),
        "comparability_key_count": int(handoff_index["v553_comparability_key"].astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if not handoff_index.empty and "v553_comparability_key" in handoff_index.columns else 0,
        "temporal_anchor_hint_count": int(handoff_index["temporal_anchor_hint"].astype(str).str.strip().replace("", pd.NA).dropna().nunique()) if not handoff_index.empty and "temporal_anchor_hint" in handoff_index.columns else 0,
        "final_status": compile_status,
        "created_at": now,
        "schema_version": V552_SCHEMA_VERSION,
    }
    return pd.DataFrame([row], columns=V552_READINESS_REPORT_SCHEMA["required_columns"])


def _artifact_runtime_use_class(lane: str, compiler_status: str) -> str:
    lane = _clean(lane) or "structural"
    compiler_status = _clean(compiler_status)
    if lane == "audit":
        return "review_only"
    if lane == "manifest":
        return "not_runtime_consumable"
    if compiler_status in {"support_summary_only", "insufficient_directionality", "insufficient_grouping", "insufficient_opposing_directionality"}:
        return "structural_handoff_only"
    return "structural_handoff_only"


def _artifact_downstream_permission_class(lane: str) -> str:
    lane = _clean(lane) or "structural"
    if lane == "audit":
        return "v552j_audit_context_only"
    if lane == "manifest":
        return "v552j_manifest_context_only"
    return "v552j_structural_context_only"


def _artifact_temporal_anchor_hint(row: dict[str, Any]) -> str:
    parts = [
        _clean(row.get("source")),
        _clean(row.get("wave")),
        _clean(row.get("canonical_wave")),
        _clean(row.get("country_code")),
    ]
    return "|".join(part for part in parts if part)


def _artifact_v553_comparability_key(row: dict[str, Any]) -> str:
    payload = {
        "source": _clean(row.get("source")),
        "wave": _clean(row.get("wave")),
        "canonical_wave": _clean(row.get("canonical_wave")),
        "country_code": _clean(row.get("country_code")),
        "artifact_name": _clean(row.get("artifact_name")),
        "artifact_lane": _clean(row.get("lane")),
        "compiler_status": _clean(row.get("compiler_status")),
        "requires_directionality": bool(row.get("requires_directionality", False)),
    }
    return _hash_payload(payload)


def build_v552_to_v552j_handoff_index(
    artifact_specs: list[dict[str, Any]],
    *,
    run_id: str = "",
    source: str = "",
    wave: str = "",
    canonical_wave: str = "",
    country_code: str = "",
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for spec in artifact_specs:
        lane = _clean(spec.get("lane")) or "structural"
        compiler_status = _clean(spec.get("compiler_status"))
        artifact_name = _clean(spec.get("artifact_name"))
        artifact_row = {
            "run_id": run_id,
            "handoff_index_id": _hash_payload(
                {
                    "run_id": run_id,
                    "artifact_name": artifact_name,
                    "lane": lane,
                    "status": compiler_status,
                    "source": source,
                    "wave": wave,
                    "canonical_wave": canonical_wave,
                    "country_code": country_code,
                }
            ),
            "artifact_name": artifact_name,
            "artifact_lane": lane,
            "artifact_status": compiler_status,
            "artifact_path_csv": _clean(spec.get("artifact_path_csv")),
            "artifact_path_parquet": _clean(spec.get("artifact_path_parquet")),
            "source": _clean(spec.get("source")) or source,
            "wave": _clean(spec.get("wave")) or wave,
            "canonical_wave": _clean(spec.get("canonical_wave")) or canonical_wave,
            "country_code": _clean(spec.get("country_code")) or country_code,
            "runtime_use_class": _artifact_runtime_use_class(lane, compiler_status),
            "downstream_permission_class": _artifact_downstream_permission_class(lane),
            "downstream_consumer_layer": "V552J",
            "requires_directionality": bool(spec.get("requires_directionality", False)),
            "ready_for_v552j_inspection": compiler_status not in {"error_missing_required_columns", "error_unreadable_input"},
            "ready_for_v553_after_v552j": lane == "structural" and compiler_status not in {"error_missing_required_columns", "error_unreadable_input", "blocked"},
            "known_absences_json": json.dumps(
                [] if compiler_status in {"populated", "not_applicable"} else [artifact_name, compiler_status],
                sort_keys=True,
                ensure_ascii=False,
            ),
            "v553_comparability_key": _artifact_v553_comparability_key({**spec, "source": source, "wave": wave, "canonical_wave": canonical_wave, "country_code": country_code}),
            "temporal_anchor_hint": _artifact_temporal_anchor_hint({**spec, "source": source, "wave": wave, "canonical_wave": canonical_wave, "country_code": country_code}),
            "comparability_status": "ready" if lane == "structural" and compiler_status in {"populated", "support_summary_only"} else "not_ready",
            "created_at": pd.Timestamp.utcnow().isoformat(),
            "schema_version": V552_SCHEMA_VERSION,
        }
        rows.append(artifact_row)
    return pd.DataFrame(rows, columns=V552_TO_V552J_HANDOFF_INDEX_SCHEMA["required_columns"])


def _build_v552_structural_fact_index(outputs: dict[str, pd.DataFrame], run_id: str) -> pd.DataFrame:
    artifact_specs: list[tuple[str, str]] = [
        ("question_semantic_hierarchy", "question_semantic_hierarchy"),
        ("relation_axis_pressure", "relation_axis_pressure"),
        ("target_entity_pressure", "target_entity_pressure"),
        ("driver_facet_pressure", "driver_facet_pressure"),
        ("structural_channel_index", "structural_channel_index"),
        ("horizon_constraint_index", "horizon_constraint_index"),
        ("contradiction_surface", "contradiction_surface"),
        ("aggregate_projection_surface", "aggregate_projection_surface"),
        ("position_conditioning_profile", "position_conditioning_profile"),
        ("country_wave_pressure_profile", "country_wave_pressure_profile"),
    ]
    rows: list[dict[str, Any]] = []
    # Build channel lookup from structural_channel_index for rows that lack direct structural_channel_id
    channel_lookup: dict[tuple[str, str, str], str] = {}
    channel_index_df = outputs.get("structural_channel_index", pd.DataFrame())
    if channel_index_df is not None and not channel_index_df.empty:
        for _, ci_row in channel_index_df.iterrows():
            ci_axis = _clean(ci_row.get("anchor_axis_id"))
            ci_target = _clean(ci_row.get("anchor_target_id"))
            ci_facet = _clean(ci_row.get("anchor_driver_facet_id"))
            ci_channel = _clean(ci_row.get("channel_id"))
            if ci_axis and ci_target and ci_facet and ci_channel:
                channel_lookup[(ci_axis, ci_target, ci_facet)] = ci_channel
    for source_artifact, structural_fact_type in artifact_specs:
        source_df = outputs.get(source_artifact, pd.DataFrame())
        if source_df is None or source_df.empty:
            continue
        ordered = source_df.reset_index(drop=True)
        for source_row_index in range(len(ordered)):
            source_row = ordered.iloc[source_row_index].to_dict()
            source_row_id = _stable_source_row_id(source_artifact, source_row, source_row_index)
            source_row_hash = _source_row_hash(source_row)
            relation_axis_id = _preferred_text(source_row, "relation_axis_id", "anchor_axis_id", "basis_relation_axis_id")
            target_entity_id = _preferred_text(source_row, "target_entity_id", "anchor_target_id", "basis_target_entity_id")
            driver_facet_id = _preferred_text(source_row, "driver_facet_id", "facet_id", "anchor_driver_facet_id", "basis_driver_facet_id")
            structural_channel_id = _preferred_text(source_row, "structural_channel_id", "channel_id", "basis_structural_channel_id")
            # Look up structural_channel_id from channel_index if not directly present but triple is available
            if not structural_channel_id and relation_axis_id and target_entity_id and driver_facet_id:
                channel_key = (relation_axis_id, target_entity_id, driver_facet_id)
                if channel_key in channel_lookup:
                    structural_channel_id = channel_lookup[channel_key]
            horizon_constraint_id = _preferred_text(source_row, "horizon_constraint_id", "basis_horizon_constraint_id")
            question_id = _preferred_text(source_row, "question_id")
            semantic_signature = _preferred_text(source_row, "semantic_signature", "strata_path", "question_use_contract_id", "position_conditioning")
            if not semantic_signature:
                semantic_signature = "|".join(
                    token
                    for token in [
                        relation_axis_id,
                        target_entity_id,
                        driver_facet_id,
                        structural_channel_id,
                        horizon_constraint_id,
                        question_id,
                    ]
                    if token
                )
            structural_fact_lane, structural_fact_grain = _structural_fact_lane_and_grain(source_artifact, source_row)
            pressure_score = _to_float(
                source_row.get("pressure_score")
                or source_row.get("projection_score")
                or source_row.get("constraint_signal_score")
                or source_row.get("field_pressure_score")
                or source_row.get("support_score")
                or 0.0
            )
            entropy = _to_float(source_row.get("entropy")) or 0.0
            polarization_index = _to_float(source_row.get("polarization_index")) or 0.0
            dominant_orientation = _preferred_text(source_row, "dominant_orientation")
            n_atoms = int(_to_float(source_row.get("n_atoms")) or _to_float(source_row.get("atom_count")) or 0)
            n_unweighted_total = int(_to_float(source_row.get("n_unweighted_total")) or _to_float(source_row.get("n_unweighted")) or 0)
            n_weighted_total = int(_to_float(source_row.get("n_weighted_total")) or _to_float(source_row.get("n_weighted")) or 0)
            support_status = _preferred_text(source_row, "support_status")
            confidence_tier = _preferred_text(source_row, "confidence_tier")
            directionality_coverage = _to_float(source_row.get("directionality_coverage")) or _to_float(source_row.get("overall_directionality_coverage")) or 0.0
            pressure_computation_status = _preferred_text(source_row, "pressure_computation_status", "status", "compiler_status")
            compiler_status = _preferred_text(source_row, "compiler_status", "status") or "populated"
            structural_fact_status = "resolved" if structural_fact_lane == "row_level_structural_fact" else "context_only"
            missing_absences = _row_absences(source_row, ["relation_axis_id", "target_entity_id", "driver_facet_id", "structural_channel_id", "horizon_constraint_id"])
            allowed_v552j_use = "v552j_structural_dimension_source" if structural_fact_lane == "row_level_structural_fact" else ("v552j_context_only" if structural_fact_lane in {"profile_context_fact", "country_wave_context_fact"} else "v552j_audit_context_only")
            forbidden_downstream_use = _json_text(["runtime_persona", "v553_fallback_only"])
            rows.append(
                {
                    "run_id": run_id,
                    "v552_structural_fact_id": f"v552sf__{_hash_payload({'run_id': run_id, 'source_artifact': source_artifact, 'source_row_id': source_row_id, 'source_row_hash': source_row_hash, 'relation_axis_id': relation_axis_id, 'target_entity_id': target_entity_id, 'driver_facet_id': driver_facet_id, 'structural_channel_id': structural_channel_id, 'horizon_constraint_id': horizon_constraint_id, 'semantic_signature': semantic_signature})[:20]}",
                    "source_run_id": run_id,
                    "source_artifact": source_artifact,
                    "source_row_index": int(source_row_index),
                    "source_row_id": source_row_id,
                    "source_row_hash": source_row_hash,
                    "source": _preferred_text(source_row, "source"),
                    "wave": _preferred_text(source_row, "wave"),
                    "canonical_wave": _preferred_text(source_row, "canonical_wave") or _preferred_text(source_row, "wave"),
                    "country_code": _preferred_text(source_row, "country_code"),
                    "structural_fact_type": structural_fact_type,
                    "structural_fact_lane": structural_fact_lane,
                    "structural_fact_grain": structural_fact_grain,
                    "question_id": question_id,
                    "relation_axis_id": relation_axis_id,
                    "target_entity_id": target_entity_id,
                    "driver_facet_id": driver_facet_id,
                    "structural_channel_id": structural_channel_id,
                    "horizon_constraint_id": horizon_constraint_id,
                    "semantic_signature": semantic_signature,
                    "pressure_score": pressure_score if pressure_score is not None else 0.0,
                    "entropy": entropy,
                    "polarization_index": polarization_index,
                    "dominant_orientation": dominant_orientation,
                    "n_atoms": n_atoms,
                    "n_unweighted_total": n_unweighted_total,
                    "n_weighted_total": n_weighted_total,
                    "support_status": support_status,
                    "confidence_tier": confidence_tier,
                    "directionality_coverage": directionality_coverage,
                    "pressure_computation_status": pressure_computation_status,
                    "compiler_status": compiler_status,
                    "structural_fact_status": structural_fact_status,
                    "allowed_v552j_use": allowed_v552j_use,
                    "forbidden_downstream_use": forbidden_downstream_use,
                    "known_absences_json": _json_text(missing_absences),
                    "source_trace_json": json.dumps(
                        {
                            "source_row_id": source_row_id,
                            "source_row_index": int(source_row_index),
                            "source_row_hash": source_row_hash,
                            "source_row": {key: source_row.get(key) for key in sorted(source_row.keys())},
                            "resolved_dimensions": {
                                "relation_axis_id": relation_axis_id,
                                "target_entity_id": target_entity_id,
                                "driver_facet_id": driver_facet_id,
                                "structural_channel_id": structural_channel_id,
                                "horizon_constraint_id": horizon_constraint_id,
                                "semantic_signature": semantic_signature,
                            },
                            "structural_fact_lane": structural_fact_lane,
                            "structural_fact_grain": structural_fact_grain,
                        },
                        sort_keys=True,
                        ensure_ascii=False,
                        default=str,
                    ),
                    "source_artifact_row_count": int(len(source_df)),
                    "created_at": pd.Timestamp.utcnow().isoformat(),
                    "schema_version": V552_SCHEMA_VERSION,
                    "compiler_version": V552_HANOFF_SCHEMA_VERSION,
                }
            )
    return pd.DataFrame(rows, columns=V552_STRUCTURAL_FACT_INDEX_SCHEMA["required_columns"])


def _build_v552_temporal_key_source_index(structural_fact_index: pd.DataFrame, run_id: str) -> pd.DataFrame:
    if structural_fact_index.empty:
        return pd.DataFrame(columns=V552_TEMPORAL_KEY_SOURCE_INDEX_SCHEMA["required_columns"])
    rows: list[dict[str, Any]] = []
    for idx, row in structural_fact_index.reset_index(drop=True).iterrows():
        row_dict = row.to_dict()
        core_dims = {
            "relation_axis_id": _clean(row_dict.get("relation_axis_id")),
            "target_entity_id": _clean(row_dict.get("target_entity_id")),
            "driver_facet_id": _clean(row_dict.get("driver_facet_id")),
            "structural_channel_id": _clean(row_dict.get("structural_channel_id")),
            "horizon_constraint_id": _clean(row_dict.get("horizon_constraint_id")),
            "semantic_signature": _clean(row_dict.get("semantic_signature")),
        }
        structural_fact_lane = _clean(row_dict.get("structural_fact_lane")) or "not_temporal_key_source"
        structural_fact_grain = _clean(row_dict.get("structural_fact_grain")) or "not_temporal_key_source"
        temporal_key_basis = json.dumps(
            {
                "source_run_id": _clean(row_dict.get("source_run_id")),
                "source_artifact": _clean(row_dict.get("source_artifact")),
                "source_row_id": _clean(row_dict.get("source_row_id")),
                "source_row_hash": _clean(row_dict.get("source_row_hash")),
                "source_artifact_row_count": int(row_dict.get("source_artifact_row_count", 0) or 0),
                "relation_axis_id": core_dims["relation_axis_id"],
                "target_entity_id": core_dims["target_entity_id"],
                "driver_facet_id": core_dims["driver_facet_id"],
                "structural_channel_id": core_dims["structural_channel_id"],
                "horizon_constraint_id": core_dims["horizon_constraint_id"],
                "semantic_signature": core_dims["semantic_signature"],
                "structural_fact_lane": structural_fact_lane,
                "structural_fact_grain": structural_fact_grain,
            },
            sort_keys=True,
        )
        allowed_for_v552j = structural_fact_lane == "row_level_structural_fact"
        allowed_for_v553_probe = structural_fact_lane in {"row_level_structural_fact", "profile_context_fact", "country_wave_context_fact"} and bool(
            core_dims["relation_axis_id"] or core_dims["target_entity_id"] or core_dims["driver_facet_id"] or core_dims["structural_channel_id"] or core_dims["horizon_constraint_id"] or _clean(row_dict.get("question_id"))
        )
        allowed_for_v553_temporal_field = False
        temporal_key_candidate_status, temporal_key_grain, temporal_key_blocker_reason, allowed_for_v553_probe, allowed_for_v553_temporal_field = _structural_temporal_key_candidate_status(
            structural_fact_lane=structural_fact_lane,
            structural_fact_grain=structural_fact_grain,
            relation_axis_id=core_dims["relation_axis_id"],
            target_entity_id=core_dims["target_entity_id"],
            driver_facet_id=core_dims["driver_facet_id"],
            structural_channel_id=core_dims["structural_channel_id"],
            horizon_constraint_id=core_dims["horizon_constraint_id"],
            question_id=_clean(row_dict.get("question_id")),
        )
        fallback_used = not allowed_for_v553_temporal_field
        resolution_status = "resolved" if allowed_for_v553_temporal_field else ("fallback_shared_column_profile" if fallback_used else "unknown")
        fallback_permission_profile_key = "" if allowed_for_v553_temporal_field else f"{_clean(row_dict.get('allowed_v552j_use'))}::{_clean(row_dict.get('structural_fact_status'))}::{structural_fact_grain}"
        source_trace = {
            "source_run_id": _clean(row_dict.get("source_run_id")),
            "source_artifact": _clean(row_dict.get("source_artifact")),
            "source_row_id": _clean(row_dict.get("source_row_id")),
            "temporal_key_basis": json.loads(temporal_key_basis),
            "structural_fact_status": _clean(row_dict.get("structural_fact_status")),
            "structural_fact_lane": structural_fact_lane,
            "structural_fact_grain": structural_fact_grain,
            "source_row_hash": _clean(row_dict.get("source_row_hash")),
        }
        temporal_key_source_id = f"v552tks__{_hash_payload({'run_id': run_id, 'source_v552_structural_fact_id': _clean(row_dict.get('v552_structural_fact_id')), 'temporal_key_basis': json.loads(temporal_key_basis)})[:20]}"
        rows.append(
            {
                "run_id": run_id,
                "v552_temporal_key_source_id": temporal_key_source_id,
                "v552_structural_fact_id": _clean(row_dict.get("v552_structural_fact_id")),
                "source_run_id": _clean(row_dict.get("source_run_id")),
                "source_artifact": _clean(row_dict.get("source_artifact")),
                "source_row_index": int(row_dict.get("source_row_index", idx) or idx),
                "source_row_id": _clean(row_dict.get("source_row_id")),
                "source_row_hash": _clean(row_dict.get("source_row_hash")),
                "source": _clean(row_dict.get("source")),
                "wave": _clean(row_dict.get("wave")),
                "canonical_wave": _clean(row_dict.get("canonical_wave")),
                "country_code": _clean(row_dict.get("country_code")),
                "structural_fact_type": _clean(row_dict.get("structural_fact_type")),
                "structural_fact_lane": structural_fact_lane,
                "structural_fact_grain": structural_fact_grain,
                "question_id": _clean(row_dict.get("question_id")),
                "relation_axis_id": core_dims["relation_axis_id"],
                "target_entity_id": core_dims["target_entity_id"],
                "driver_facet_id": core_dims["driver_facet_id"],
                "structural_channel_id": core_dims["structural_channel_id"],
                "horizon_constraint_id": core_dims["horizon_constraint_id"],
                "semantic_signature": core_dims["semantic_signature"],
                "temporal_key_grain": temporal_key_grain,
                "temporal_key_basis": temporal_key_basis,
                "temporal_key_candidate_status": temporal_key_candidate_status,
                "temporal_key_blocker_reason": temporal_key_blocker_reason,
                "fallback_permission_profile_key": fallback_permission_profile_key,
                "fallback_used": fallback_used,
                "resolution_status": resolution_status,
                "allowed_downstream_use": bool(allowed_for_v553_temporal_field),
                "pressure_score": _to_float(row_dict.get("pressure_score")) or 0.0,
                "support_status": _clean(row_dict.get("support_status")),
                "confidence_tier": _clean(row_dict.get("confidence_tier")),
                "directionality_coverage": _to_float(row_dict.get("directionality_coverage")) or 0.0,
                "allowed_for_v552j": bool(allowed_for_v552j),
                "allowed_for_v553_probe": bool(allowed_for_v553_probe),
                "allowed_for_v553_temporal_field": bool(allowed_for_v553_temporal_field),
                "known_absences_json": _clean(row_dict.get("known_absences_json")) or "[]",
                "source_trace_json": _json_text(source_trace),
                "source_artifact_row_count": int(row_dict.get("source_artifact_row_count", 0) or 0),
                "created_at": pd.Timestamp.utcnow().isoformat(),
                "schema_version": V552_SCHEMA_VERSION,
                "compiler_version": V552_HANOFF_SCHEMA_VERSION,
            }
        )
    return pd.DataFrame(rows, columns=V552_TEMPORAL_KEY_SOURCE_INDEX_SCHEMA["required_columns"])


def build_v552_structural_outputs(
    atoms: pd.DataFrame,
    conditional_determinicity: pd.DataFrame | None = None,
    *,
    run_id: str = "",
) -> dict[str, pd.DataFrame]:
    directional_mask = pd.Series(dtype=bool)
    if atoms.empty:
        status = "empty_no_relation_evidence_atoms"
        directionality_coverage = 0.0
        support_basis = "none"
        input_atom_hash = _hash_payload({"rows": []})
        source = ""
        wave = ""
        canonical_wave = ""
        country_code = ""
        response_semantics_status = ""
        response_semantics_source = ""
        response_semantics_contract_hash = ""
        source_structure_source = ""
        source_structure_basis = ""
        source_structure_confidence = ""
        has_sufficient_directionality = False
    else:
        directional_mask = _direction_mask(atoms.get("response_direction", pd.Series(dtype=object))).ne("") & pd.to_numeric(atoms.get("response_intensity", pd.Series(dtype=object)), errors="coerce").notna()
        directionality_coverage = float(directional_mask.mean()) if len(atoms) else 0.0
        has_sufficient_directionality = bool(directional_mask.any())
        status = "populated" if has_sufficient_directionality else "insufficient_directionality"
        support_basis = "directional_intensity" if has_sufficient_directionality else "support_only"
        input_atom_hash = _hash_payload({"rows": atoms.get("atom_id", pd.Series(dtype=str)).fillna("").astype(str).tolist()})
        first = atoms.iloc[0].to_dict()
        source = _clean(first.get("source"))
        wave = _clean(first.get("wave"))
        canonical_wave = _clean(first.get("canonical_wave"))
        country_code = _clean(first.get("country_code"))
        response_semantics_status = _clean(first.get("response_semantics_status"))
        response_semantics_source = _clean(first.get("response_semantics_source"))
        response_semantics_contract_hash = _clean(first.get("response_semantics_contract_hash"))
        source_structure_source = _clean(first.get("source_structure_source"))
        source_structure_basis = _clean(first.get("source_structure_basis"))
        source_structure_confidence = _clean(first.get("source_structure_confidence"))

    context = {
        "source": source,
        "wave": wave,
        "canonical_wave": canonical_wave,
        "country_code": country_code,
        "response_semantics_status": response_semantics_status,
        "response_semantics_source": response_semantics_source,
        "response_semantics_contract_hash": response_semantics_contract_hash,
        "source_structure_source": source_structure_source,
        "source_structure_basis": source_structure_basis,
        "source_structure_confidence": source_structure_confidence,
    }

    relation_axis_pressure = build_relation_axis_pressure(atoms, run_id=run_id)
    target_entity_pressure = build_target_entity_pressure(atoms, run_id=run_id)
    driver_facet_pressure = build_driver_facet_pressure(atoms, run_id=run_id)
    question_semantic_hierarchy = build_question_semantic_hierarchy(atoms, run_id=run_id)
    facet_semantic_profile = build_facet_semantic_profile(question_semantic_hierarchy, run_id=run_id)
    driver_semantic_profile = build_driver_semantic_profile(question_semantic_hierarchy, run_id=run_id)
    stratum_semantic_profile = build_stratum_semantic_profile(question_semantic_hierarchy, run_id=run_id)
    horizon_semantic_profile = build_horizon_semantic_profile(question_semantic_hierarchy, run_id=run_id)
    contradiction_tensor = build_contradiction_tensor(atoms, run_id=run_id)
    contradiction_surface = build_contradiction_surface(atoms, run_id=run_id)
    aggregate_projection_surface = build_aggregate_projection_surface(atoms, run_id=run_id)
    parent_position_prior = build_parent_position_prior(atoms, run_id=run_id)
    parent_attitude_prior = build_parent_attitude_prior(atoms, run_id=run_id)
    parent_behavior_tendency_prior = build_parent_behavior_tendency_prior(atoms, run_id=run_id)
    parent_contradiction_prior = build_parent_contradiction_prior(atoms, contradiction_tensor, run_id=run_id)
    parent_prior_manifest = build_parent_prior_manifest(
        run_id=run_id,
        source=source,
        wave=wave,
        canonical_wave=canonical_wave,
        country_code=country_code,
        parent_position_prior=parent_position_prior,
        parent_attitude_prior=parent_attitude_prior,
        parent_behavior_tendency_prior=parent_behavior_tendency_prior,
        parent_contradiction_prior=parent_contradiction_prior,
    )
    structural_channel_index = build_structural_channel_index(atoms, run_id=run_id)
    country_wave_pressure_profile = build_country_wave_pressure_profile(atoms, run_id=run_id)
    position_conditioning_profile = build_position_conditioning_profile(atoms, run_id=run_id)
    horizon_constraint_index = build_horizon_constraint_index(atoms, run_id=run_id)
    directional_audit = build_v552_directionality_coverage_audit(atoms, run_id=run_id)
    directionality_gap_surface = build_v552_directionality_gap_surface(atoms, run_id=run_id)
    status_pressure_review_surface = build_v552_status_pressure_review_surface(atoms, run_id=run_id)
    conditional_audit = _build_conditional_determinicity_status_audit(
        conditional_determinicity,
        run_id=run_id,
        conditional_input_path="",
        conditional_input_hash="",
    )
    missing_relation_axis = not _has_columns(atoms, ["relation_axis_id"])
    missing_target_entity = not _has_columns(atoms, ["target_entity_id"])
    missing_driver_facet = not _has_columns(atoms, ["driver_facet_id"])
    missing_structural_grouping = missing_relation_axis or missing_target_entity or missing_driver_facet
    structural_dir = Path("data/ddm_repository_copy") / "v552" / "runs" / run_id / "structural"

    artifact_specs = [
        {
            "artifact_name": "relation_axis_pressure",
            "artifact_path_csv": "",
            "artifact_path_parquet": "",
            "row_count": len(relation_axis_pressure),
            "compiler_status": "insufficient_grouping" if missing_relation_axis and not atoms.empty else status,
            "status_reason": "direct structural relation-axis handoff",
            "requires_directionality": True,
            "lane": "structural",
        },
        {
            "artifact_name": "target_entity_pressure",
            "artifact_path_csv": "",
            "artifact_path_parquet": "",
            "row_count": len(target_entity_pressure),
            "compiler_status": "insufficient_grouping" if missing_target_entity and not atoms.empty else status,
            "status_reason": "direct structural target-entity handoff",
            "requires_directionality": True,
            "lane": "structural",
        },
        {
            "artifact_name": "driver_facet_pressure",
            "artifact_path_csv": "",
            "artifact_path_parquet": "",
            "row_count": len(driver_facet_pressure),
            "compiler_status": "insufficient_grouping" if missing_driver_facet and not atoms.empty else status,
            "status_reason": "direct structural driver-facet handoff",
            "requires_directionality": True,
            "lane": "structural",
        },
        {
            "artifact_name": "question_semantic_hierarchy",
            "artifact_path_csv": "",
            "artifact_path_parquet": "",
            "row_count": len(question_semantic_hierarchy),
            "compiler_status": "support_summary_only" if question_semantic_hierarchy.empty else ("insufficient_directionality" if not has_sufficient_directionality else status),
            "status_reason": "question -> facet -> driver -> stratum -> horizon hierarchy",
            "requires_directionality": False,
            "lane": "structural",
        },
        {
            "artifact_name": "facet_semantic_profile",
            "artifact_path_csv": "",
            "artifact_path_parquet": "",
            "row_count": len(facet_semantic_profile),
            "compiler_status": "support_summary_only" if facet_semantic_profile.empty else ("insufficient_directionality" if not has_sufficient_directionality else status),
            "status_reason": "facet semantic profile",
            "requires_directionality": False,
            "lane": "structural",
        },
        {
            "artifact_name": "driver_semantic_profile",
            "artifact_path_csv": "",
            "artifact_path_parquet": "",
            "row_count": len(driver_semantic_profile),
            "compiler_status": "support_summary_only" if driver_semantic_profile.empty else ("insufficient_directionality" if not has_sufficient_directionality else status),
            "status_reason": "driver semantic profile",
            "requires_directionality": False,
            "lane": "structural",
        },
        {
            "artifact_name": "stratum_semantic_profile",
            "artifact_path_csv": "",
            "artifact_path_parquet": "",
            "row_count": len(stratum_semantic_profile),
            "compiler_status": "support_summary_only" if stratum_semantic_profile.empty else ("insufficient_directionality" if not has_sufficient_directionality else status),
            "status_reason": "stratum semantic profile",
            "requires_directionality": False,
            "lane": "structural",
        },
        {
            "artifact_name": "horizon_semantic_profile",
            "artifact_path_csv": "",
            "artifact_path_parquet": "",
            "row_count": len(horizon_semantic_profile),
            "compiler_status": "support_summary_only" if horizon_semantic_profile.empty else ("support_summary_only" if not has_sufficient_directionality else status),
            "status_reason": "horizon semantic profile",
            "requires_directionality": False,
            "lane": "structural",
        },
        {
            "artifact_name": "country_wave_pressure_profile",
            "artifact_path_csv": "",
            "artifact_path_parquet": "",
            "row_count": len(country_wave_pressure_profile),
            "compiler_status": "support_summary_only" if not has_sufficient_directionality else status,
            "status_reason": "country-wave structural profile",
            "requires_directionality": False,
            "lane": "structural",
        },
        {
            "artifact_name": "aggregate_projection_surface",
            "artifact_path_csv": "",
            "artifact_path_parquet": "",
            "row_count": len(aggregate_projection_surface),
            "compiler_status": "support_summary_only" if aggregate_projection_surface.empty else ("support_summary_only" if not has_sufficient_directionality else status),
            "status_reason": "aggregate projection surface for strata_path rollups",
            "requires_directionality": False,
            "lane": "structural",
        },
        {
            "artifact_name": "position_conditioning_profile",
            "artifact_path_csv": "",
            "artifact_path_parquet": "",
            "row_count": len(position_conditioning_profile),
            "compiler_status": "support_summary_only" if position_conditioning_profile.empty else ("support_summary_only" if not has_sufficient_directionality else status),
            "status_reason": "position-conditioning structural profile",
            "requires_directionality": False,
            "lane": "structural",
        },
        {
            "artifact_name": "structural_channel_index",
            "artifact_path_csv": "",
            "artifact_path_parquet": "",
            "row_count": len(structural_channel_index),
            "compiler_status": "insufficient_grouping" if missing_structural_grouping and not atoms.empty else status,
            "status_reason": "structural channel handoff",
            "requires_directionality": True,
            "lane": "structural",
        },
        {
            "artifact_name": "contradiction_tensor",
            "artifact_path_csv": "",
            "artifact_path_parquet": "",
            "row_count": len(contradiction_tensor),
            "compiler_status": "insufficient_grouping" if missing_structural_grouping and not atoms.empty else ("insufficient_opposing_directionality" if contradiction_tensor.empty else "populated"),
            "status_reason": "contradiction requires opposing directional evidence",
            "requires_directionality": True,
            "lane": "structural",
        },
        {
            "artifact_name": "contradiction_surface",
            "artifact_path_csv": "",
            "artifact_path_parquet": "",
            "row_count": len(contradiction_surface),
            "compiler_status": "insufficient_grouping" if missing_structural_grouping and not atoms.empty else ("support_summary_only" if contradiction_surface.empty else "populated"),
            "status_reason": "aggregate contradiction surface retaining within-axis mixed sign and pocket-level split summary",
            "requires_directionality": True,
            "lane": "structural",
        },
        {
            "artifact_name": "horizon_constraint_index",
            "artifact_path_csv": "",
            "artifact_path_parquet": "",
            "row_count": len(horizon_constraint_index),
            "compiler_status": "insufficient_grouping" if missing_structural_grouping and not atoms.empty else ("support_summary_only" if not horizon_constraint_index.empty else "not_applicable"),
            "status_reason": "conservative horizon constraint summary",
            "requires_directionality": False,
            "lane": "structural",
        },
        {
            "artifact_name": "parent_position_prior",
            "artifact_path_csv": "",
            "artifact_path_parquet": "",
            "row_count": len(parent_position_prior),
            "compiler_status": "support_summary_only" if parent_position_prior.empty else ("insufficient_directionality" if not has_sufficient_directionality else status),
            "status_reason": "parent position prior scaffold",
            "requires_directionality": False,
            "lane": "structural",
        },
        {
            "artifact_name": "parent_attitude_prior",
            "artifact_path_csv": "",
            "artifact_path_parquet": "",
            "row_count": len(parent_attitude_prior),
            "compiler_status": "support_summary_only" if parent_attitude_prior.empty else ("insufficient_directionality" if not has_sufficient_directionality else status),
            "status_reason": "parent attitude prior scaffold",
            "requires_directionality": False,
            "lane": "structural",
        },
        {
            "artifact_name": "parent_behavior_tendency_prior",
            "artifact_path_csv": "",
            "artifact_path_parquet": "",
            "row_count": len(parent_behavior_tendency_prior),
            "compiler_status": "support_summary_only" if parent_behavior_tendency_prior.empty else ("insufficient_directionality" if not has_sufficient_directionality else status),
            "status_reason": "parent behavior tendency prior scaffold",
            "requires_directionality": False,
            "lane": "structural",
        },
        {
            "artifact_name": "parent_contradiction_prior",
            "artifact_path_csv": "",
            "artifact_path_parquet": "",
            "row_count": len(parent_contradiction_prior),
            "compiler_status": "support_summary_only" if parent_contradiction_prior.empty else ("insufficient_directionality" if not has_sufficient_directionality else status),
            "status_reason": "parent contradiction prior scaffold",
            "requires_directionality": False,
            "lane": "structural",
        },
        {
            "artifact_name": "v552_directionality_coverage_audit",
            "artifact_path_csv": "",
            "artifact_path_parquet": "",
            "row_count": len(directional_audit),
            "compiler_status": "populated" if has_sufficient_directionality else "support_summary_only",
            "status_reason": "directionality coverage audit",
            "requires_directionality": False,
            "lane": "audit",
        },
        {
            "artifact_name": "v552_directionality_gap_surface",
            "artifact_path_csv": "",
            "artifact_path_parquet": "",
            "row_count": len(directionality_gap_surface),
            "compiler_status": "populated" if not directionality_gap_surface.empty else "support_summary_only",
            "status_reason": "directionality gap review surface",
            "requires_directionality": False,
            "lane": "audit",
        },
        {
            "artifact_name": "v552_status_pressure_review_surface",
            "artifact_path_csv": "",
            "artifact_path_parquet": "",
            "row_count": len(status_pressure_review_surface),
            "compiler_status": "populated" if not status_pressure_review_surface.empty else "support_summary_only",
            "status_reason": "status pressure review surface",
            "requires_directionality": False,
            "lane": "audit",
        },
        {
            "artifact_name": "v552_input_provenance_manifest",
            "artifact_path_csv": "",
            "artifact_path_parquet": "",
            "row_count": 1,
            "compiler_status": "populated",
            "status_reason": "input provenance manifest",
            "requires_directionality": False,
            "lane": "manifest",
        },
        {
            "artifact_name": "parent_position_prior_manifest",
            "artifact_path_csv": "",
            "artifact_path_parquet": "",
            "row_count": len(parent_prior_manifest),
            "compiler_status": "support_summary_only" if parent_prior_manifest.empty else "populated",
            "status_reason": "parent position prior manifest scaffold",
            "requires_directionality": False,
            "lane": "manifest",
        },
    ]
    if conditional_determinicity is not None:
        artifact_specs.insert(
            7,
            {
                "artifact_name": "conditional_determinicity_status_audit",
                "artifact_path_csv": "",
                "artifact_path_parquet": "",
                "row_count": len(conditional_audit),
                "compiler_status": conditional_audit.iloc[0]["status"] if not conditional_audit.empty else "status_only_conditional_input",
                "status_reason": conditional_audit.iloc[0]["status_reason"] if not conditional_audit.empty else "conditional determinicity not supplied",
                "requires_directionality": False,
                "lane": "audit",
            },
        )

    fact_outputs = {
        "relation_axis_pressure": relation_axis_pressure,
        "target_entity_pressure": target_entity_pressure,
        "driver_facet_pressure": driver_facet_pressure,
        "question_semantic_hierarchy": question_semantic_hierarchy,
        "facet_semantic_profile": facet_semantic_profile,
        "driver_semantic_profile": driver_semantic_profile,
        "stratum_semantic_profile": stratum_semantic_profile,
        "horizon_semantic_profile": horizon_semantic_profile,
        "contradiction_tensor": contradiction_tensor,
        "contradiction_surface": contradiction_surface,
        "structural_channel_index": structural_channel_index,
        "country_wave_pressure_profile": country_wave_pressure_profile,
        "aggregate_projection_surface": aggregate_projection_surface,
        "position_conditioning_profile": position_conditioning_profile,
        "horizon_constraint_index": horizon_constraint_index,
        "parent_position_prior": parent_position_prior,
        "parent_attitude_prior": parent_attitude_prior,
        "parent_behavior_tendency_prior": parent_behavior_tendency_prior,
        "parent_contradiction_prior": parent_contradiction_prior,
        "parent_prior_manifest": parent_prior_manifest,
        "parent_position_prior_manifest": parent_prior_manifest,
        "conditional_determinicity_status_audit": conditional_audit,
        "v552_directionality_coverage_audit": directional_audit,
        "v552_directionality_gap_surface": directionality_gap_surface,
        "v552_status_pressure_review_surface": status_pressure_review_surface,
    }
    v552_structural_fact_index = _build_v552_structural_fact_index(fact_outputs, run_id=run_id)
    v552_temporal_key_source_index = _build_v552_temporal_key_source_index(v552_structural_fact_index, run_id=run_id)
    artifact_specs.extend(
        [
            {
                "artifact_name": "v552_structural_fact_index",
                "artifact_path_csv": "",
                "artifact_path_parquet": str(structural_dir / "v552_structural_fact_index.parquet"),
                "row_count": len(v552_structural_fact_index),
                "compiler_status": "populated" if not v552_structural_fact_index.empty else "support_summary_only",
                "status_reason": "row-level structural fact index preserving source artifact grain",
                "requires_directionality": False,
                "lane": "structural",
            },
            {
                "artifact_name": "v552_temporal_key_source_index",
                "artifact_path_csv": "",
                "artifact_path_parquet": str(structural_dir / "v552_temporal_key_source_index.parquet"),
                "row_count": len(v552_temporal_key_source_index),
                "compiler_status": "populated" if not v552_temporal_key_source_index.empty else "support_summary_only",
                "status_reason": "row-level temporal key source index preserving structural dimensions",
                "requires_directionality": False,
                "lane": "structural",
            },
        ]
    )

    v552_artifact_authority_index = build_v552_artifact_authority_index(artifact_specs, run_id=run_id)
    v552_known_absence_register = build_v552_known_absence_register(artifact_specs, run_id=run_id)
    v552_to_v552j_handoff_index = build_v552_to_v552j_handoff_index(
        artifact_specs,
        run_id=run_id,
        source=source,
        wave=wave,
        canonical_wave=canonical_wave,
        country_code=country_code,
    )
    v552_readiness_report = build_v552_readiness_report(
        run_id=run_id,
        atoms_row_count=len(atoms),
        artifact_authority_index=v552_artifact_authority_index,
        known_absence_register=v552_known_absence_register,
        handoff_index=v552_to_v552j_handoff_index,
        final_status=status,
    )

    artifact_specs.extend(
        [
            {
                "artifact_name": "v552_artifact_authority_index",
                "artifact_path_csv": "",
                "artifact_path_parquet": "",
                "row_count": len(v552_artifact_authority_index),
                "compiler_status": "populated" if not v552_artifact_authority_index.empty else "support_summary_only",
                "status_reason": "artifact authority index",
                "requires_directionality": False,
                "lane": "manifest",
            },
            {
                "artifact_name": "v552_known_absence_register",
                "artifact_path_csv": "",
                "artifact_path_parquet": "",
                "row_count": len(v552_known_absence_register),
                "compiler_status": "populated" if not v552_known_absence_register.empty else "support_summary_only",
                "status_reason": "known absence register",
                "requires_directionality": False,
                "lane": "manifest",
            },
            {
                "artifact_name": "v552_to_v552j_handoff_index",
                "artifact_path_csv": "",
                "artifact_path_parquet": "",
                "row_count": len(v552_to_v552j_handoff_index),
                "compiler_status": "populated" if not v552_to_v552j_handoff_index.empty else "support_summary_only",
                "status_reason": "V552 to V552J handoff contract",
                "requires_directionality": False,
                "lane": "manifest",
            },
        ]
    )
    artifact_specs.append(
        {
            "artifact_name": "v552_readiness_report",
            "artifact_path_csv": "",
            "artifact_path_parquet": "",
            "row_count": len(v552_readiness_report),
            "compiler_status": "populated" if not v552_readiness_report.empty else "support_summary_only",
            "status_reason": "V552 readiness report for V553 handoff",
            "requires_directionality": False,
            "lane": "manifest",
        }
    )

    for spec in artifact_specs:
        if spec.get("artifact_name") == "v552_status_audit":
            spec["row_count"] = len(artifact_specs)
            spec["compiler_status"] = "populated" if not atoms.empty else "empty_no_relation_evidence_atoms"

    status_audit = build_v552_status_audit(
        artifact_specs,
        run_id=run_id,
        input_atom_hash=input_atom_hash,
        input_atom_count=len(atoms),
        eligible_atom_count=len(atoms),
        support_basis=support_basis,
        has_sufficient_directionality=has_sufficient_directionality,
        final_status=normalize_v552_status(status),
        context=context,
    )
    directionality_coverage_audit = directional_audit
    manifest = build_v552_input_provenance_manifest(
        run_id=run_id,
        atoms_path="",
        atoms_input_hash=input_atom_hash,
        atoms_row_count=len(atoms),
        atoms_required_columns_present=True,
        atoms_missing_required_columns=[],
        conditional_determinicity_path=None,
        conditional_determinicity_hash=None,
        conditional_determinicity_row_count=None,
        output_root="",
        output_dir="",
        final_status=status,
        conditional_determinicity_supplied=conditional_determinicity is not None,
    )
    return {
        "relation_axis_pressure": relation_axis_pressure,
        "target_entity_pressure": target_entity_pressure,
        "driver_facet_pressure": driver_facet_pressure,
        "question_semantic_hierarchy": question_semantic_hierarchy,
        "facet_semantic_profile": facet_semantic_profile,
        "driver_semantic_profile": driver_semantic_profile,
        "stratum_semantic_profile": stratum_semantic_profile,
        "horizon_semantic_profile": horizon_semantic_profile,
        "contradiction_tensor": contradiction_tensor,
        "contradiction_surface": contradiction_surface,
        "structural_channel_index": structural_channel_index,
        "country_wave_pressure_profile": country_wave_pressure_profile,
        "aggregate_projection_surface": aggregate_projection_surface,
        "position_conditioning_profile": position_conditioning_profile,
        "horizon_constraint_index": horizon_constraint_index,
        "parent_position_prior": parent_position_prior,
        "parent_attitude_prior": parent_attitude_prior,
        "parent_behavior_tendency_prior": parent_behavior_tendency_prior,
        "parent_contradiction_prior": parent_contradiction_prior,
        "parent_prior_manifest": parent_prior_manifest,
        "parent_position_prior_manifest": parent_prior_manifest,
        "conditional_determinicity_status_audit": conditional_audit,
        "v552_status_audit": status_audit,
        "v552_directionality_coverage_audit": directionality_coverage_audit,
        "v552_directionality_gap_surface": directionality_gap_surface,
        "v552_status_pressure_review_surface": status_pressure_review_surface,
        "v552_input_provenance_manifest": manifest,
        "v552_artifact_authority_index": v552_artifact_authority_index,
        "v552_known_absence_register": v552_known_absence_register,
        "v552_to_v552j_handoff_index": v552_to_v552j_handoff_index,
        "v552_readiness_report": v552_readiness_report,
        "v552_structural_fact_index": v552_structural_fact_index,
        "v552_temporal_key_source_index": v552_temporal_key_source_index,
    }


def validate_v552_relation_axis_pressure(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_RELATION_AXIS_PRESSURE_SCHEMA["required_columns"], "v552_relation_axis_pressure")


def validate_v552_target_entity_pressure(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_TARGET_ENTITY_PRESSURE_SCHEMA["required_columns"], "v552_target_entity_pressure")


def validate_v552_driver_facet_pressure(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_DRIVER_FACET_PRESSURE_SCHEMA["required_columns"], "v552_driver_facet_pressure")


def validate_v552_question_semantic_hierarchy(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_QUESTION_SEMANTIC_HIERARCHY_SCHEMA["required_columns"], "v552_question_semantic_hierarchy")


def validate_v552_facet_semantic_profile(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_FACET_SEMANTIC_PROFILE_SCHEMA["required_columns"], "v552_facet_semantic_profile")


def validate_v552_driver_semantic_profile(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_DRIVER_SEMANTIC_PROFILE_SCHEMA["required_columns"], "v552_driver_semantic_profile")


def validate_v552_stratum_semantic_profile(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_STRATUM_SEMANTIC_PROFILE_SCHEMA["required_columns"], "v552_stratum_semantic_profile")


def validate_v552_horizon_semantic_profile(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_HORIZON_SEMANTIC_PROFILE_SCHEMA["required_columns"], "v552_horizon_semantic_profile")


def validate_v552_position_conditioning_profile(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_POSITION_CONDITIONING_PROFILE_SCHEMA["required_columns"], "v552_position_conditioning_profile")


def validate_v552_parent_position_prior(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_PARENT_POSITION_PRIOR_SCHEMA["required_columns"], "v552_parent_position_prior")


def validate_v552_parent_attitude_prior(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_PARENT_ATTITUDE_PRIOR_SCHEMA["required_columns"], "v552_parent_attitude_prior")


def validate_v552_parent_behavior_tendency_prior(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_PARENT_BEHAVIOR_TENDENCY_PRIOR_SCHEMA["required_columns"], "v552_parent_behavior_tendency_prior")


def validate_v552_parent_contradiction_prior(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_PARENT_CONTRADICTION_PRIOR_SCHEMA["required_columns"], "v552_parent_contradiction_prior")


def validate_v552_parent_prior_manifest(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_PARENT_PRIOR_MANIFEST_SCHEMA["required_columns"], "v552_parent_prior_manifest")


def validate_v552_contradiction_tensor(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_CONTRADICTION_TENSOR_SCHEMA["required_columns"], "v552_contradiction_tensor")


def validate_v552_contradiction_surface(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_CONTRADICTION_SURFACE_SCHEMA["required_columns"], "v552_contradiction_surface")


def validate_v552_structural_channel_index(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_STRUCTURAL_CHANNEL_INDEX_SCHEMA["required_columns"], "v552_structural_channel_index")


def validate_v552_country_wave_pressure_profile(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_COUNTRY_WAVE_PRESSURE_PROFILE_SCHEMA["required_columns"], "v552_country_wave_pressure_profile")


def validate_v552_aggregate_projection_surface(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_AGGREGATE_PROJECTION_SURFACE_SCHEMA["required_columns"], "v552_aggregate_projection_surface")


def validate_v552_horizon_constraint_index(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_HORIZON_CONSTRAINT_INDEX_SCHEMA["required_columns"], "v552_horizon_constraint_index")


def validate_v552_directionality_gap_surface(df: pd.DataFrame) -> list[str]:
    errors = validate_columns(df, V552_DIRECTIONALITY_GAP_SURFACE_SCHEMA["required_columns"], "v552_directionality_gap_surface")
    if not errors and not df.empty:
        bad = sorted(set(df["gap_surface_reason"].astype(str)) - V552_ALLOWED_DIRECTIONALITY_GAP_REASONS)
        if bad:
            errors.append(f"v552_directionality_gap_surface: invalid gap_surface_reason values: {bad}")
    return errors


def validate_v552_status_pressure_review_surface(df: pd.DataFrame) -> list[str]:
    errors = validate_columns(df, V552_STATUS_PRESSURE_REVIEW_SCHEMA["required_columns"], "v552_status_pressure_review_surface")
    if not errors and not df.empty:
        bad_reasons = sorted(set(df["status_pressure_reason"].astype(str)) - V552_ALLOWED_STATUS_PRESSURE_REASONS)
        if bad_reasons:
            errors.append(f"v552_status_pressure_review_surface: invalid status_pressure_reason values: {bad_reasons}")
        bad_statuses = sorted(set(df["status"].astype(str)) - V552_ALLOWED_STATUS_PRESSURE_STATUSES)
        if bad_statuses:
            errors.append(f"v552_status_pressure_review_surface: invalid status values: {bad_statuses}")
    return errors


def validate_v552_artifact_authority_index(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_ARTIFACT_AUTHORITY_INDEX_SCHEMA["required_columns"], "v552_artifact_authority_index")


def validate_v552_known_absence_register(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_KNOWN_ABSENCE_REGISTER_SCHEMA["required_columns"], "v552_known_absence_register")


def validate_v552_to_v552j_handoff_index(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_TO_V552J_HANDOFF_INDEX_SCHEMA["required_columns"], "v552_to_v552j_handoff_index")


def validate_v552_readiness_report(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_READINESS_REPORT_SCHEMA["required_columns"], "v552_readiness_report")


def validate_v552_structural_fact_index(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_STRUCTURAL_FACT_INDEX_SCHEMA["required_columns"], "v552_structural_fact_index")


def validate_v552_temporal_key_source_index(df: pd.DataFrame) -> list[str]:
    return validate_columns(df, V552_TEMPORAL_KEY_SOURCE_INDEX_SCHEMA["required_columns"], "v552_temporal_key_source_index")


# V552 structural-pressure contract v2.1 overrides.
V552_SCHEMA_VERSION = "v2.1"
V552_PRESSURE_FORMULA_VERSION = "v2.1.4"
V552_HANDOFF_SCHEMA_VERSION = "v552_structural_handoff_v2_1_4"
V552_HANOFF_SCHEMA_VERSION = V552_HANDOFF_SCHEMA_VERSION
V552_PRESSURE_FORMULA_ID = "v552_certified_intensity_representation_signed_distribution_mean"
V552_PRESSURE_FORMULA_EXACT_VERSION = V552_PRESSURE_FORMULA_VERSION
V552_PRESSURE_SCALE_ID = "canonical_signed_component_-1_1"
V552_EPSILON = 1e-12
V552_NORMALIZED_INTENSITY_MIN = 0.0
V552_NORMALIZED_INTENSITY_MAX = 1.0
V552_SCALE_DIRECTION_TO_ENCODING = {
    "negative_to_positive": "AXIS_COORDINATE_LINEAR",
    "negative_to_positive_construct_relative": "CONSTRUCT_RELATIVE_MAGNITUDE",
}
V552_INTENSITY_REPRESENTATION_FIELDS = [
    "source_intensity_representation_class",
    "source_intensity_representation_status",
    "source_intensity_exact_fit_candidates_json",
    "normalized_intensity_min",
    "normalized_intensity_max",
    "source_scale_direction_token",
]
for _schema in [
    V552_PRESSURE_COMPONENT_INDEX_SCHEMA,
    V552_PRESSURE_OBSERVATION_INDEX_SCHEMA,
    V552_STRUCTURAL_FACT_INDEX_SCHEMA,
    V552_TEMPORAL_KEY_SOURCE_INDEX_SCHEMA,
    V552_TO_V552J_HANDOFF_INDEX_SCHEMA,
]:
    for _column in V552_INTENSITY_REPRESENTATION_FIELDS:
        if _column not in _schema["required_columns"]:
            _schema["required_columns"].append(_column)
V552_PRESSURE_OBSERVATION_GROUP_COLUMNS = [
    "source", "source_family", "wave", "canonical_wave", "country_code", "survey_year", "analysis_scope",
    "empirical_object_type", "empirical_distribution_id", "question_id", "var_code", "position_field", "position_value",
    "semantic_identity_signature", "structural_identity_signature", "response_scale_signature",
]
V552_REQUIRED_V551_V2_1_COLUMNS = [
    "atom_id", "atom_contract_hash", "source_run_id", "shard_id", "source_family", "source", "wave", "canonical_wave",
    "country_code", "survey_year", "analysis_scope", "empirical_object_type", "empirical_object_id", "empirical_distribution_id", "source_table",
    "source_row_hash", "question_id", "var_code", "position_field", "position_value", "response_value_raw",
    "response_value_normalized", "normalized_response_label", "response_family", "response_direction",
    "response_direction_status", "response_intensity", "response_intensity_status", "observed_response_zero", "polarity",
    "ordinal_rank", "scale_min", "scale_max", "scale_direction", "directionality_policy", "response_topology",
    "response_scale_signature", "n_unweighted", "n_respondents", "n_weighted", "pct_unweighted", "pct_weighted",
    "weight_status", "support_status", "confidence_tier", "support_score", "prevalence_score", "support_measure_role",
    "prevalence_measure_role", "support_may_be_used_as_pressure", "prevalence_may_be_used_as_pressure", "semantic_role",
    "semantic_subrole", "semantic_tags", "semantic_identity_signature", "driver_id", "driver_facet_id", "relation_axis_id",
    "target_entity_id", "strata_relevance", "strata_path", "subject_position_signature", "position_conditioning",
    "position_modifiers", "conditional_strata_weights", "horizon_affordance", "structural_identity_signature",
    "empirical_observation_class", "source_measure_kind", "source_measure_status", "directional_measure_kind",
    "pressure_evidence_class", "v552_pressure_component_eligible", "v552_pressure_component_status",
    "v552_pressure_component_ineligibility_reason", "measurement_contract_hash", "semantic_role_authority_status",
    "response_semantics_authority_status", "directionality_authority_status", "structural_mapping_status",
    "manual_review_flag", "manual_review_reason", "source_structure_review_required", "allowed_as_temporal_pressure_indicator",
    "forbidden_inference", "known_absences", "evidence_basis", "provenance_basis", "schema_version",
]
V552_PRESSURE_CONTRACT_CHAIN_FIELDS = [
    "empirical_distribution_id",
    "component_response_surface_signature",
    "response_surface_completeness_status",
    "pressure_measure_class",
    "pressure_formula_id",
    "pressure_formula_version",
    "pressure_scale_id",
    "pressure_measurement_hash",
    "semantic_identity_signature",
    "structural_identity_signature",
    "response_scale_signature",
    "directionality_policy",
    "response_topology",
    "source_intensity_representation_class",
    "source_intensity_representation_status",
    "pressure_score",
    "pressure_score_status",
]


def _canon(value: Any) -> Any:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    if isinstance(value, bool):
        return bool(value)
    if isinstance(value, int):
        return int(value)
    if isinstance(value, float):
        return format(value, ".12g")
    return str(value).strip()


def _json_dumps(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _stable_hash_v21(payload: Any) -> str:
    return hashlib.sha256(_json_dumps(payload).encode("utf-8")).hexdigest()


def _id(prefix: str, payload: Any, length: int = 20) -> str:
    return f"{prefix}{_stable_hash_v21(payload)[:length]}"


def _bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    text = _clean(value).casefold()
    return text in {"1", "true", "t", "yes", "y", "on"}


def _finite_float(value: Any) -> float | None:
    parsed = _to_float(value)
    if parsed is None or not math.isfinite(parsed):
        return None
    return float(parsed)


def _nullable(value: Any) -> Any:
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass
    return value


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_v552_v551_input_contract(atoms: pd.DataFrame) -> dict[str, Any]:
    missing = [column for column in V552_REQUIRED_V551_V2_1_COLUMNS if column not in atoms.columns]
    report = {
        "status": "PASS",
        "atom_rows": int(len(atoms)),
        "required_column_count": int(len(V552_REQUIRED_V551_V2_1_COLUMNS)),
        "present_required_column_count": int(len(V552_REQUIRED_V551_V2_1_COLUMNS) - len(missing)),
        "missing_columns": missing,
        "non_v2_schema_rows": 0,
        "duplicate_atom_id_rows": 0,
        "duplicate_atom_contract_rows": 0,
        "invalid_atom_contract_rows": 0,
        "schema_version": "v2.1",
    }
    if missing:
        report["status"] = "BLOCKED_V552_MISSING_V551_V2_CONTRACT"
        return report
    if atoms.empty:
        return report
    schema_values = atoms["schema_version"].fillna("").astype(str)
    non_v2 = ~schema_values.isin({"v2.1", "2.1"})
    report["non_v2_schema_rows"] = int(non_v2.sum())
    dup_atom = atoms["atom_id"].fillna("").astype(str).duplicated(keep=False)
    report["duplicate_atom_id_rows"] = int(dup_atom.sum())
    blank_contract = atoms["atom_contract_hash"].fillna("").astype(str).str.strip().eq("")
    required_nonblank = [
        "atom_id", "atom_contract_hash", "source", "canonical_wave", "country_code", "empirical_object_type",
        "empirical_object_id", "empirical_distribution_id", "source_table", "response_value_normalized", "response_direction_status",
        "response_intensity_status", "response_scale_signature", "semantic_identity_signature", "structural_identity_signature",
        "relation_axis_id", "target_entity_id", "driver_id", "driver_facet_id", "pressure_evidence_class",
        "v552_pressure_component_status", "measurement_contract_hash", "evidence_basis", "provenance_basis",
    ]
    invalid = blank_contract.copy()
    for column in required_nonblank:
        invalid = invalid | atoms[column].fillna("").astype(str).str.strip().eq("")
    invalid = invalid | atoms[["question_id", "var_code"]].fillna("").astype(str).agg("".join, axis=1).str.strip().eq("")
    report["invalid_atom_contract_rows"] = int(invalid.sum())
    if report["non_v2_schema_rows"]:
        report["status"] = "BLOCKED_V552_NON_V2_ATOMS"
    elif report["duplicate_atom_id_rows"]:
        report["status"] = "BLOCKED_V552_DUPLICATE_ATOM_IDENTITY"
    elif report["invalid_atom_contract_rows"]:
        report["status"] = "BLOCKED_V552_INVALID_ATOM_CONTRACT"
    return report


POSITIVE_DIRECTION_TOKENS = {"positive", "support", "agree", "approve", "favor", "favour", "yes"}
NEGATIVE_DIRECTION_TOKENS = {"negative", "oppose", "disagree", "disapprove", "against", "no"}
NEUTRAL_DIRECTION_TOKENS = {"neutral", "neither", "balanced"}


def v552_direction_sign(value: Any) -> int | None:
    token = _clean(value).casefold()
    if token in POSITIVE_DIRECTION_TOKENS:
        return 1
    if token in NEGATIVE_DIRECTION_TOKENS:
        return -1
    if token in NEUTRAL_DIRECTION_TOKENS:
        return 0
    return None


@dataclass(frozen=True)
class V552ScaleTransformResult:
    direction_sign: int | None
    scale_encoding_class: str
    scale_transform_id: str
    scale_encoding_status: str
    direction_scale_consistency_status: str
    normalized_source_coordinate: float | None
    normalized_construct_magnitude: float | None
    canonical_signed_component: float | None
    source_intensity_zero: bool | None
    canonical_signed_component_zero: bool | None
    reason: str


@dataclass(frozen=True)
class V552IntensityRepresentationResolution:
    representation_class: str
    resolution_status: str
    exact_fit_candidates: tuple[str, ...]
    component_count: int
    reason: str


def _source_response_intensity(row: Mapping[str, Any]) -> tuple[float | None, str]:
    """Return the governed source-scale value and the field/derivation that supplied it.

    V551 v2.1 historically overwrote explicit neutral coordinates with zero.  The
    original ordinal contract is still sufficient to reconstruct the axis coordinate
    exactly, so old artifacts remain replayable while new artifacts carry
    `authority_response_intensity` directly.
    """
    authority_intensity = _finite_float(row.get("authority_response_intensity"))
    if authority_intensity is not None:
        return authority_intensity, "authority_response_intensity"
    # A supplied response_intensity is already the governed source-scale
    # coordinate.  The ordinal reconstruction is only a compatibility
    # fallback for inherited atoms that do not carry that coordinate.
    legacy_intensity = _finite_float(row.get("response_intensity"))
    # Some inherited v2.1 atoms encoded neutral categories as a legacy zero
    # magnitude.  If an ordinal source coordinate is available, recover the
    # neutral midpoint rather than turning that legacy zero into canonical -1.
    if legacy_intensity is not None and not (
        _clean(row.get("response_direction")).casefold() == "neutral"
        and abs(legacy_intensity) <= V552_EPSILON
    ):
        return legacy_intensity, "response_intensity"
    rank = _finite_float(row.get("ordinal_rank"))
    scale_min = _finite_float(row.get("scale_min"))
    scale_max = _finite_float(row.get("scale_max"))
    direction = _clean(row.get("scale_direction")).casefold()
    if rank is not None and scale_min is not None and scale_max is not None and scale_max > scale_min and direction in {"ascending", "descending"}:
        coordinate = (rank - scale_min) / (scale_max - scale_min)
        if direction == "descending":
            coordinate = 1.0 - coordinate
        return max(0.0, min(1.0, float(coordinate))), "ordinal_scale_coordinate"
    return None, "missing"


def _normalized_response_intensity(row: Mapping[str, Any]) -> tuple[float | None, str]:
    intensity, _ = _source_response_intensity(row)
    if intensity is None:
        return None, "missing_response_intensity"
    if intensity < V552_NORMALIZED_INTENSITY_MIN - V552_EPSILON or intensity > V552_NORMALIZED_INTENSITY_MAX + V552_EPSILON:
        return None, "normalized_intensity_out_of_bounds"
    if abs(intensity - V552_NORMALIZED_INTENSITY_MIN) <= V552_EPSILON:
        intensity = V552_NORMALIZED_INTENSITY_MIN
    if abs(intensity - V552_NORMALIZED_INTENSITY_MAX) <= V552_EPSILON:
        intensity = V552_NORMALIZED_INTENSITY_MAX
    return float(intensity), ""


def _candidate_signed_value(row: Mapping[str, Any], representation_class: str) -> tuple[float | None, str]:
    direction_sign = v552_direction_sign(row.get("response_direction"))
    if direction_sign is None:
        return None, "unknown_response_direction"
    intensity, reason = _normalized_response_intensity(row)
    if reason:
        return None, reason
    assert intensity is not None
    if representation_class == "NORMALIZED_AXIS_COORDINATE_0_1":
        signed = 2.0 * intensity - 1.0
    elif representation_class == "NORMALIZED_UNSIGNED_MAGNITUDE_0_1":
        signed = float(direction_sign) * intensity
    else:
        return None, "unresolved_intensity_representation"
    if signed < -1.0 - V552_EPSILON or signed > 1.0 + V552_EPSILON:
        return None, "canonical_signed_component_out_of_bounds"
    if direction_sign > 0 and signed <= V552_EPSILON:
        return None, "direction_scale_inconsistency"
    if direction_sign < 0 and signed >= -V552_EPSILON:
        return None, "direction_scale_inconsistency"
    if direction_sign == 0 and abs(signed) > V552_EPSILON:
        return None, "direction_scale_inconsistency"
    if direction_sign != 0 and abs(signed) <= V552_EPSILON:
        return None, "direction_scale_inconsistency"
    if abs(signed) <= V552_EPSILON:
        signed = 0.0
    return float(signed), ""


def _candidate_passes_distribution(group: pd.DataFrame, representation_class: str) -> tuple[bool, str]:
    for row in group.to_dict("records"):
        _, reason = _candidate_signed_value(row, representation_class)
        if reason:
            return False, reason
    return True, ""


def resolve_v552_distribution_intensity_representation(group: pd.DataFrame) -> V552IntensityRepresentationResolution:
    exact_candidates: list[str] = []
    reasons: list[str] = []
    for candidate in ["NORMALIZED_AXIS_COORDINATE_0_1", "NORMALIZED_UNSIGNED_MAGNITUDE_0_1"]:
        passes, reason = _candidate_passes_distribution(group, candidate)
        if passes:
            exact_candidates.append(candidate)
        elif reason and reason not in reasons:
            reasons.append(reason)
    if len(exact_candidates) == 1:
        return V552IntensityRepresentationResolution(
            exact_candidates[0],
            "EXACT_UNIQUE_DISTRIBUTION_RESOLUTION",
            tuple(exact_candidates),
            int(len(group)),
            "",
        )
    if len(exact_candidates) > 1:
        return V552IntensityRepresentationResolution(
            "UNRESOLVED",
            "BLOCKED_AMBIGUOUS_INTENSITY_REPRESENTATION",
            tuple(exact_candidates),
            int(len(group)),
            "ambiguous_intensity_representation",
        )
    reason = reasons[0] if reasons else "unresolved_intensity_representation"
    status_map = {
        "normalized_intensity_out_of_bounds": "BLOCKED_INVALID_NORMALIZED_INTENSITY",
        "unknown_response_direction": "BLOCKED_UNKNOWN_RESPONSE_DIRECTION",
        "direction_scale_inconsistency": "BLOCKED_INCONSISTENT_DISTRIBUTION_CONTRACT",
    }
    return V552IntensityRepresentationResolution(
        "UNRESOLVED",
        status_map.get(reason, "BLOCKED_UNRESOLVED_INTENSITY_REPRESENTATION"),
        tuple(),
        int(len(group)),
        reason,
    )


def resolve_v552_signed_component(
    row: Mapping[str, Any],
    representation: V552IntensityRepresentationResolution | None = None,
) -> V552ScaleTransformResult:
    direction_sign = v552_direction_sign(row.get("response_direction"))
    if direction_sign is None:
        return V552ScaleTransformResult(None, "UNKNOWN", "none", "BLOCKED_UNKNOWN_RESPONSE_DIRECTION", "NOT_EVALUATED", None, None, None, None, None, "unknown_response_direction")
    if representation is None:
        representation = resolve_v552_distribution_intensity_representation(pd.DataFrame([dict(row)]))
    if not representation.resolution_status.endswith("_RESOLUTION"):
        return V552ScaleTransformResult(direction_sign, "UNRESOLVED", "none", representation.resolution_status, "NOT_EVALUATED", None, None, None, None, None, representation.reason)
    intensity, reason = _normalized_response_intensity(row)
    if reason:
        status = "BLOCKED_NORMALIZED_INTENSITY_OUT_OF_BOUNDS" if reason == "normalized_intensity_out_of_bounds" else "BLOCKED_MISSING_RESPONSE_INTENSITY"
        return V552ScaleTransformResult(direction_sign, representation.representation_class, "none", status, "NOT_EVALUATED", None, None, None, None, None, reason)
    assert intensity is not None
    source_zero = bool(abs(intensity) <= V552_EPSILON)
    if representation.representation_class == "NORMALIZED_AXIS_COORDINATE_0_1":
        signed = 2.0 * intensity - 1.0
        transform_id = "normalized_axis_coordinate_to_canonical_signed_component"
        status = "RESOLVED_NORMALIZED_AXIS_COORDINATE"
        coordinate = intensity
        magnitude = None
    else:
        signed = float(direction_sign) * intensity
        transform_id = "normalized_unsigned_magnitude_with_certified_direction_sign"
        status = "RESOLVED_NORMALIZED_UNSIGNED_MAGNITUDE"
        coordinate = None
        magnitude = intensity
    signed_zero = bool(abs(signed) <= V552_EPSILON)
    if direction_sign > 0 and signed <= V552_EPSILON:
        consistency = "BLOCKED_DIRECTION_SCALE_INCONSISTENCY"
    elif direction_sign < 0 and signed >= -V552_EPSILON:
        consistency = "BLOCKED_DIRECTION_SCALE_INCONSISTENCY"
    elif direction_sign == 0 and abs(signed) > V552_EPSILON:
        consistency = "BLOCKED_DIRECTION_SCALE_INCONSISTENCY"
    else:
        consistency = "CONSISTENT_CANONICAL_ZERO" if signed_zero else "CONSISTENT"
    if consistency == "BLOCKED_DIRECTION_SCALE_INCONSISTENCY":
        return V552ScaleTransformResult(direction_sign, representation.representation_class, transform_id, "BLOCKED_DIRECTION_SCALE_INCONSISTENCY", consistency, coordinate, magnitude, None, source_zero, None, "direction_scale_inconsistency")
    return V552ScaleTransformResult(direction_sign, representation.representation_class, transform_id, status, consistency, coordinate, magnitude, signed, source_zero, signed_zero, "")


def select_v552_distribution_weight_basis(group: pd.DataFrame) -> tuple[str, pd.Series | None, str]:
    frame = group.copy()
    def numeric_series(column: str) -> pd.Series | None:
        if column not in frame.columns:
            return None
        values = pd.to_numeric(frame[column], errors="coerce")
        if values.isna().any() or (values < -V552_EPSILON).any() or (values > 1.0 + V552_EPSILON).any() or values.sum() <= 0:
            return None
        return values.astype(float)
    weighted = numeric_series("pct_weighted")
    weight_status = frame.get("weight_status", pd.Series([""] * len(frame))).fillna("").astype(str).str.casefold()
    if weighted is not None and not weight_status.str.contains("missing|unavailable|invalid|unweighted_only|not_weighted", regex=True).any():
        return "pct_weighted", weighted, ""
    unweighted = numeric_series("pct_unweighted")
    if unweighted is not None:
        return "pct_unweighted", unweighted, ""
    pop = numeric_series("population_share")
    if pop is not None:
        return "population_share", pop, ""
    counts = pd.to_numeric(frame.get("n_unweighted", pd.Series(dtype=float)), errors="coerce")
    if len(counts) == len(frame) and not counts.isna().any() and (counts >= 0).all() and counts.sum() > 0:
        return "normalized_n_unweighted", counts.astype(float), ""
    return "none", None, "missing_distribution_weight_basis"


def _observation_identity(row: Mapping[str, Any]) -> dict[str, Any]:
    return v552_observation_identity_payload(row)


def _component_identity(row: Mapping[str, Any]) -> dict[str, Any]:
    return v552_component_identity_payload(row)


def _component_response_surface_payload(component_group: pd.DataFrame) -> dict[str, Any]:
    return v552_response_surface_payload(component_group.to_dict("records"))


def _component_response_surface_signature(component_group: pd.DataFrame) -> str:
    return recompute_v552_response_surface_signature(component_group.to_dict("records"))


def _response_surface_completeness(component_group: pd.DataFrame) -> tuple[str, float | None, str]:
    denom_values = sorted(set(pd.to_numeric(component_group["n_respondents"], errors="coerce").dropna().astype(float).tolist()))
    positive_denoms = [value for value in denom_values if value > 0]
    if len(positive_denoms) != 1:
        return "UNKNOWN_RESPONSE_CATEGORY_COVERAGE", None, "denominator_unavailable"
    denominator = positive_denoms[0]
    sum_n = float(pd.to_numeric(component_group["n_unweighted"], errors="coerce").fillna(0).sum())
    coverage = sum_n / denominator
    basis = "unweighted_component_count_over_unique_respondent_denominator"
    if sum_n > denominator:
        return "BLOCKED_RESPONSE_CATEGORY_COUNT_EXCEEDS_DENOMINATOR", coverage, basis
    if sum_n == denominator:
        return "COMPLETE_SELECTED_RESPONSE_CATEGORY_COVERAGE", coverage, basis
    return "PARTIAL_SELECTED_RESPONSE_CATEGORY_COVERAGE", coverage, basis


def _pressure_measure_class_for_status(pressure_score: float | None, completeness_status: str) -> str:
    if pressure_score is None:
        return "single_question_scale_aware_directional_distribution_not_computable"
    if completeness_status == "COMPLETE_SELECTED_RESPONSE_CATEGORY_COVERAGE":
        return "single_question_scale_aware_directional_distribution_pressure"
    if completeness_status == "PARTIAL_SELECTED_RESPONSE_CATEGORY_COVERAGE":
        return "single_question_scale_aware_conditional_selected_response_surface_pressure"
    if completeness_status == "UNKNOWN_RESPONSE_CATEGORY_COVERAGE":
        return "single_question_scale_aware_observed_response_surface_pressure_unknown_denominator"
    return "single_question_scale_aware_directional_distribution_not_computable"


def build_v552_pressure_component_index(atoms: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    if atoms.empty:
        return pd.DataFrame(columns=V552_PRESSURE_COMPONENT_INDEX_SCHEMA["required_columns"])
    rows: list[dict[str, Any]] = []
    grouped = atoms.copy().groupby(V552_PRESSURE_OBSERVATION_GROUP_COLUMNS, dropna=False, sort=True)
    now = _utc_now()
    for _, group in grouped:
        first = group.iloc[0].to_dict()
        obs_id = recompute_v552_pressure_observation_id(first)
        representation = resolve_v552_distribution_intensity_representation(group)
        for _, atom in group.iterrows():
            base = atom.to_dict()
            transform = resolve_v552_signed_component(base, representation)
            upstream_status = _clean(base.get("v552_pressure_component_status"))
            upstream_eligible = _bool(base.get("v552_pressure_component_eligible")) and upstream_status == "ELIGIBLE"
            if upstream_status == "REVIEW_REQUIRED":
                comp_status, reason = "REVIEW_REQUIRED_UPSTREAM", _clean(base.get("v552_pressure_component_ineligibility_reason")) or "review_required_component"
            elif upstream_status == "COVERAGE_ONLY_NEUTRAL":
                # Neutral categories are not directional evidence, but they are a lawful
                # zero-valued part of the response distribution and must remain in the
                # denominator/mass.  Treating them as an ineligible component made every
                # otherwise valid odd-point scale non-computable.
                if transform.reason:
                    comp_status, reason = "BLOCKED_INVALID_NEUTRAL_COMPONENT", transform.reason
                else:
                    comp_status, reason = "COVERAGE_ONLY_NEUTRAL_COMPONENT", ""
            elif not upstream_eligible:
                comp_status, reason = "INELIGIBLE_UPSTREAM_PERMISSION", _clean(base.get("v552_pressure_component_ineligibility_reason")) or "ineligible_component_present"
            elif transform.reason:
                reason_map = {
                    "unknown_response_direction": "BLOCKED_UNKNOWN_RESPONSE_DIRECTION",
                    "missing_response_intensity": "BLOCKED_MISSING_RESPONSE_INTENSITY",
                    "normalized_intensity_out_of_bounds": "BLOCKED_NORMALIZED_INTENSITY_OUT_OF_BOUNDS",
                    "ambiguous_intensity_representation": "BLOCKED_AMBIGUOUS_INTENSITY_REPRESENTATION",
                    "unresolved_intensity_representation": "BLOCKED_UNRESOLVED_INTENSITY_REPRESENTATION",
                    "direction_scale_inconsistency": "BLOCKED_DIRECTION_SCALE_INCONSISTENCY",
                }
                comp_status, reason = reason_map.get(transform.reason, "BLOCKED_INVALID_COMPONENT_CONTRACT"), transform.reason
            else:
                comp_status, reason = "ELIGIBLE_TRANSFORMED_COMPONENT", ""
            row = {
                "run_id": run_id,
                "v552_pressure_component_id": recompute_v552_pressure_component_id({**base, "source_atom_id": base.get("atom_id")}),
                "v552_pressure_observation_id": obs_id,
                "source_atom_id": _clean(base.get("atom_id")),
                "source_atom_contract_hash": _clean(base.get("atom_contract_hash")),
                "source_measurement_contract_hash": _clean(base.get("measurement_contract_hash")),
                "source_v551_run_id": _clean(base.get("source_run_id")),
                "source": _clean(base.get("source")),
                "source_family": _clean(base.get("source_family")),
                "wave": _clean(base.get("wave")),
                "canonical_wave": _clean(base.get("canonical_wave")),
                "country_code": _clean(base.get("country_code")),
                "survey_year": _nullable(base.get("survey_year")),
                "analysis_scope": _clean(base.get("analysis_scope")),
                "empirical_object_type": _clean(base.get("empirical_object_type")),
                "empirical_object_id": _clean(base.get("empirical_object_id")),
                "empirical_distribution_id": _clean(base.get("empirical_distribution_id")),
                "question_id": _clean(base.get("question_id")),
                "var_code": _clean(base.get("var_code")),
                "position_field": _clean(base.get("position_field")),
                "position_value": _clean(base.get("position_value")),
                "response_value_raw": _clean(base.get("response_value_raw")),
                "response_value_normalized": _clean(base.get("response_value_normalized")),
                "normalized_response_label": _clean(base.get("normalized_response_label")),
                "response_family": _clean(base.get("response_family")),
                "response_direction": _clean(base.get("response_direction")),
                "response_direction_sign": transform.direction_sign,
                "response_intensity": _finite_float(base.get("response_intensity")),
                "authority_response_intensity": _finite_float(base.get("authority_response_intensity")),
                "source_intensity_field": _source_response_intensity(base)[1],
                "source_intensity_zero": transform.source_intensity_zero,
                "scale_min": _finite_float(base.get("scale_min")),
                "scale_max": _finite_float(base.get("scale_max")),
                "scale_direction": _clean(base.get("scale_direction")),
                "directionality_policy": _clean(base.get("directionality_policy")),
                "response_topology": _clean(base.get("response_topology")),
                "response_scale_signature": _clean(base.get("response_scale_signature")),
                "scale_encoding_class": transform.scale_encoding_class,
                "scale_transform_id": transform.scale_transform_id,
                "scale_encoding_status": transform.scale_encoding_status,
                "source_intensity_representation_class": representation.representation_class,
                "source_intensity_representation_status": representation.resolution_status,
                "source_intensity_exact_fit_candidates_json": _json_dumps(list(representation.exact_fit_candidates)),
                "normalized_intensity_min": V552_NORMALIZED_INTENSITY_MIN,
                "normalized_intensity_max": V552_NORMALIZED_INTENSITY_MAX,
                "source_scale_direction_token": _clean(base.get("scale_direction")),
                "normalized_source_coordinate": transform.normalized_source_coordinate,
                "normalized_construct_magnitude": transform.normalized_construct_magnitude,
                "canonical_signed_component": transform.canonical_signed_component,
                "canonical_signed_component_zero": transform.canonical_signed_component_zero,
                "direction_scale_consistency_status": transform.direction_scale_consistency_status,
                "n_unweighted": _finite_float(base.get("n_unweighted")),
                "n_respondents": _finite_float(base.get("n_respondents")),
                "n_weighted": _finite_float(base.get("n_weighted")),
                "pct_unweighted": _finite_float(base.get("pct_unweighted")),
                "pct_weighted": _finite_float(base.get("pct_weighted")),
                "population_share": _finite_float(base.get("population_share")),
                "weight_status": _clean(base.get("weight_status")),
                "distribution_weight_basis": "none",
                "distribution_weight_raw": None,
                "distribution_weight_normalized": None,
                "component_pressure_eligible": comp_status in {"ELIGIBLE_TRANSFORMED_COMPONENT", "COVERAGE_ONLY_NEUTRAL_COMPONENT"},
                "component_pressure_status": comp_status,
                "component_pressure_ineligibility_reason": reason,
                "semantic_identity_signature": _clean(base.get("semantic_identity_signature")),
                "structural_identity_signature": _clean(base.get("structural_identity_signature")),
                "measurement_contract_hash": _clean(base.get("measurement_contract_hash")),
                "evidence_basis_json": _clean(base.get("evidence_basis")),
                "provenance_basis_json": _clean(base.get("provenance_basis")),
                "created_at": now,
                "schema_version": V552_SCHEMA_VERSION,
                "compiler_version": V552_HANDOFF_SCHEMA_VERSION,
            }
            row["component_measurement_hash"] = "PROVISIONAL_NOT_FINALIZED"
            rows.append(row)
    return pd.DataFrame(rows).reindex(columns=V552_PRESSURE_COMPONENT_INDEX_SCHEMA["required_columns"])


def _status_from_reasons(reasons: list[str]) -> str:
    order = [
        ("review_required_component", "REVIEW_REQUIRED"),
        ("ineligible_component_present", "NOT_COMPUTABLE_MIXED_COMPONENT_PERMISSION"),
        ("no_eligible_components", "NOT_COMPUTABLE_NO_ELIGIBLE_COMPONENTS"),
        ("unknown_response_direction", "NOT_COMPUTABLE_MISSING_DIRECTION"),
        ("missing_response_intensity", "NOT_COMPUTABLE_MISSING_INTENSITY"),
        ("normalized_intensity_out_of_bounds", "NOT_COMPUTABLE_NORMALIZED_INTENSITY_OUT_OF_BOUNDS"),
        ("ambiguous_intensity_representation", "NOT_COMPUTABLE_AMBIGUOUS_INTENSITY_REPRESENTATION"),
        ("unresolved_intensity_representation", "NOT_COMPUTABLE_UNRESOLVED_INTENSITY_REPRESENTATION"),
        ("direction_scale_inconsistency", "NOT_COMPUTABLE_DIRECTION_SCALE_INCONSISTENCY"),
        ("missing_distribution_weight_basis", "NOT_COMPUTABLE_MISSING_WEIGHT_BASIS"),
        ("invalid_distribution_mass", "NOT_COMPUTABLE_INVALID_DISTRIBUTION_MASS"),
        ("inconsistent_respondent_denominator", "NOT_COMPUTABLE_INVALID_DISTRIBUTION_MASS"),
        ("category_count_exceeds_respondent_denominator", "NOT_COMPUTABLE_INVALID_DISTRIBUTION_MASS"),
    ]
    present = set(reasons)
    for token, status in order:
        if token in present:
            return status
    return "NOT_COMPUTABLE_NO_ELIGIBLE_COMPONENTS"


def build_v552_pressure_observation_index(atoms: pd.DataFrame, component_index: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    if atoms.empty:
        return pd.DataFrame(columns=V552_PRESSURE_OBSERVATION_INDEX_SCHEMA["required_columns"])
    rows: list[dict[str, Any]] = []
    now = _utc_now()
    for obs_id, comp_group in component_index.groupby("v552_pressure_observation_id", dropna=False, sort=True):
        atom_group = atoms[atoms["atom_id"].astype(str).isin(comp_group["source_atom_id"].astype(str))].copy()
        first = atom_group.iloc[0].to_dict() if not atom_group.empty else comp_group.iloc[0].to_dict()
        identity_hash = _stable_hash_v21(_observation_identity(first))
        reasons: list[str] = []
        review_count = int(comp_group["component_pressure_status"].eq("REVIEW_REQUIRED_UPSTREAM").sum())
        computable_statuses = {"ELIGIBLE_TRANSFORMED_COMPONENT", "COVERAGE_ONLY_NEUTRAL_COMPONENT"}
        eligible_count = int(comp_group["component_pressure_status"].isin(computable_statuses).sum())
        ineligible_count = int(len(comp_group) - eligible_count - review_count)
        if review_count:
            reasons.append("review_required_component")
            permission = "REVIEW_REQUIRED_COMPONENTS"
        elif eligible_count == 0:
            reasons.append("no_eligible_components")
            permission = "NO_ELIGIBLE_COMPONENTS"
        elif ineligible_count:
            reasons.append("ineligible_component_present")
            permission = "MIXED_COMPONENT_PERMISSION"
        else:
            permission = "ALL_COMPONENTS_ELIGIBLE"
        for reason in comp_group["component_pressure_ineligibility_reason"].fillna("").astype(str):
            for token in reason.split("|"):
                if token and token not in reasons:
                    reasons.append(token)
        basis, weights_raw, weight_reason = select_v552_distribution_weight_basis(comp_group)
        pressure_score = None
        weights_norm = None
        mass_raw = None
        coverage = None
        pressure_status = "NOT_COMPUTABLE"
        obs_status = _status_from_reasons(reasons)
        if not reasons:
            if weights_raw is None:
                reasons.append(weight_reason)
                obs_status = "NOT_COMPUTABLE_MISSING_WEIGHT_BASIS"
            else:
                mass_raw = float(weights_raw.sum())
                if basis in {"pct_weighted", "pct_unweighted", "population_share"}:
                    coverage = mass_raw
                    if mass_raw > 1.000001:
                        reasons.append("invalid_distribution_mass")
                        obs_status = "NOT_COMPUTABLE_INVALID_DISTRIBUTION_MASS"
                if not reasons:
                    denom_values = sorted(set(pd.to_numeric(comp_group["n_respondents"], errors="coerce").dropna().astype(float).tolist()))
                    positive_denoms = [v for v in denom_values if v > 0]
                    if len(positive_denoms) > 1:
                        reasons.append("inconsistent_respondent_denominator")
                        obs_status = "NOT_COMPUTABLE_INVALID_DISTRIBUTION_MASS"
                    elif len(positive_denoms) == 1:
                        n_resp = positive_denoms[0]
                        sum_n = float(pd.to_numeric(comp_group["n_unweighted"], errors="coerce").fillna(0).sum())
                        if sum_n > n_resp:
                            reasons.append("category_count_exceeds_respondent_denominator")
                            obs_status = "NOT_COMPUTABLE_INVALID_DISTRIBUTION_MASS"
                    if not reasons:
                        weights_norm = weights_raw / mass_raw
                        signed = pd.to_numeric(comp_group["canonical_signed_component"], errors="coerce")
                        pressure_score = float((weights_norm.reset_index(drop=True) * signed.reset_index(drop=True)).sum())
                        pressure_score = 0.0 if abs(pressure_score) <= V552_EPSILON else pressure_score
                        pressure_status = "OBSERVED_ZERO" if pressure_score == 0.0 else "OBSERVED_NONZERO"
                        obs_status = "OBSERVED_ZERO_PRESSURE" if pressure_score == 0.0 else "OBSERVED_PRESSURE"
                        component_index.loc[comp_group.index, "distribution_weight_basis"] = basis
                        component_index.loc[comp_group.index, "distribution_weight_raw"] = weights_raw.values
                        component_index.loc[comp_group.index, "distribution_weight_normalized"] = weights_norm.values
                        comp_group = component_index.loc[comp_group.index].copy()
        if pressure_score is None and obs_status == "REVIEW_REQUIRED":
            pressure_status = "REVIEW_REQUIRED"
        comp_group = component_index.loc[comp_group.index].copy()
        for comp_idx, comp_row in comp_group.iterrows():
            component_index.loc[comp_idx, "component_measurement_hash"] = recompute_v552_v2_1_4_component_measurement_hash(comp_row.to_dict())
        comp_group = component_index.loc[comp_group.index].copy()
        signed_values = pd.to_numeric(comp_group["canonical_signed_component"], errors="coerce").dropna()
        if weights_norm is not None and len(signed_values) == len(comp_group):
            weight_list = weights_norm.reset_index(drop=True)
            pos_share = float(weight_list[signed_values.reset_index(drop=True) > V552_EPSILON].sum())
            neg_share = float(weight_list[signed_values.reset_index(drop=True) < -V552_EPSILON].sum())
            neu_share = float(weight_list[signed_values.reset_index(drop=True).abs() <= V552_EPSILON].sum())
            dominant, dominant_share = recompute_v552_dominant_orientation(pos_share, neg_share, neu_share)
            mu = pressure_score or 0.0
            std = math.sqrt(float((weight_list * (signed_values.reset_index(drop=True) - mu) ** 2).sum()))
        else:
            pos_share = neg_share = neu_share = dominant_share = std = None
            dominant = ""
        opposed_mass = (pos_share or 0.0) + (neg_share or 0.0)
        if opposed_mass > 0:
            p = (pos_share or 0.0) / opposed_mass
            n = (neg_share or 0.0) / opposed_mass
            polarization = 2 * min(p, n)
            entropy = -sum(v * math.log(v, 2) for v in [p, n] if v > 0)
        else:
            polarization = 0.0 if pressure_score is not None else None
            entropy = 0.0 if pressure_score is not None else None
        denominator_values = sorted(set(pd.to_numeric(comp_group["n_respondents"], errors="coerce").dropna().astype(float).tolist()))
        denominator = denominator_values[0] if len([v for v in denominator_values if v > 0]) == 1 else None
        atom_ids = sorted(comp_group["source_atom_id"].fillna("").astype(str).tolist())
        atom_hashes = sorted(comp_group["source_atom_contract_hash"].fillna("").astype(str).tolist())
        measurement_hashes = sorted(comp_group["source_measurement_contract_hash"].fillna("").astype(str).tolist())
        component_empirical_object_ids = sorted(comp_group["empirical_object_id"].fillna("").astype(str).tolist())
        surface_signature = _component_response_surface_signature(comp_group)
        surface_status, surface_coverage, surface_basis = _response_surface_completeness(comp_group)
        state = recompute_v552_observation_state(
            pressure_score=pressure_score,
            components=comp_group,
            response_surface_status=surface_status,
            root_issue_tokens=reasons,
        )
        row = {
            "run_id": run_id, "v552_pressure_observation_id": obs_id, "pressure_observation_identity_hash": identity_hash,
            "source_v551_run_id": _clean(first.get("source_run_id")), "source_atom_ids_json": _json_dumps(atom_ids),
            "source_atom_contract_hashes_json": _json_dumps(atom_hashes), "source_measurement_contract_hashes_json": _json_dumps(measurement_hashes),
            "source": _clean(first.get("source")), "source_family": _clean(first.get("source_family")), "wave": _clean(first.get("wave")),
            "canonical_wave": _clean(first.get("canonical_wave")), "country_code": _clean(first.get("country_code")),
            "survey_year": _nullable(first.get("survey_year")), "analysis_scope": _clean(first.get("analysis_scope")),
            "empirical_object_type": _clean(first.get("empirical_object_type")), "empirical_object_id": _clean(first.get("empirical_object_id")),
            "empirical_object_id_role": "NON_AUTHORITATIVE_REPRESENTATIVE_COMPONENT_ONLY",
            "empirical_distribution_id": _clean(first.get("empirical_distribution_id")),
            "empirical_parent_identity_class": "empirical_distribution_id",
            "component_empirical_object_ids_json": _json_dumps(component_empirical_object_ids),
            "component_response_surface_signature": surface_signature,
            "response_surface_completeness_status": surface_status,
            "response_surface_component_count": int(len(comp_group)),
            "response_surface_respondent_coverage": surface_coverage,
            "response_surface_completeness_basis": surface_basis,
            "question_id": _clean(first.get("question_id")), "var_code": _clean(first.get("var_code")),
            "position_field": _clean(first.get("position_field")), "position_value": _clean(first.get("position_value")),
            "semantic_identity_signature": _clean(first.get("semantic_identity_signature")), "structural_identity_signature": _clean(first.get("structural_identity_signature")),
            "response_scale_signature": _clean(first.get("response_scale_signature")), "semantic_role": _clean(first.get("semantic_role")),
            "semantic_subrole": _clean(first.get("semantic_subrole")), "semantic_tags": _clean(first.get("semantic_tags")),
            "directionality_policy": _clean(first.get("directionality_policy")), "response_topology": _clean(first.get("response_topology")),
            "relation_axis_id": _clean(first.get("relation_axis_id")), "target_entity_id": _clean(first.get("target_entity_id")),
            "driver_id": _clean(first.get("driver_id")), "driver_facet_id": _clean(first.get("driver_facet_id")),
            "strata_relevance": _clean(first.get("strata_relevance")), "strata_path": _clean(first.get("strata_path")),
            "subject_position_signature": _clean(first.get("subject_position_signature")), "position_conditioning": _clean(first.get("position_conditioning")),
            "position_modifiers": _clean(first.get("position_modifiers")), "conditional_strata_weights": _clean(first.get("conditional_strata_weights")),
            "horizon_affordance": _clean(first.get("horizon_affordance")),
            "pressure_measure_class": _pressure_measure_class_for_status(pressure_score, surface_status),
            "pressure_formula_id": V552_PRESSURE_FORMULA_ID, "pressure_formula_version": V552_PRESSURE_FORMULA_EXACT_VERSION,
            "pressure_scale_id": V552_PRESSURE_SCALE_ID, "pressure_scale_min": -1.0, "pressure_scale_max": 1.0,
            "source_scale_min": comp_group["scale_min"].dropna().iloc[0] if comp_group["scale_min"].notna().any() else None,
            "source_scale_max": comp_group["scale_max"].dropna().iloc[0] if comp_group["scale_max"].notna().any() else None,
            "source_scale_direction": _clean(comp_group["scale_direction"].dropna().astype(str).iloc[0]) if not comp_group["scale_direction"].dropna().empty else "",
            "scale_encoding_class": _clean(comp_group["scale_encoding_class"].dropna().astype(str).iloc[0]) if not comp_group["scale_encoding_class"].dropna().empty else "UNKNOWN",
            "scale_transform_id": _clean(comp_group["scale_transform_id"].dropna().astype(str).iloc[0]) if not comp_group["scale_transform_id"].dropna().empty else "none",
            "scale_encoding_status": _clean(comp_group["scale_encoding_status"].dropna().astype(str).iloc[0]) if not comp_group["scale_encoding_status"].dropna().empty else "BLOCKED_UNKNOWN_SCALE_DIRECTION",
            "source_intensity_representation_class": _clean(comp_group["source_intensity_representation_class"].dropna().astype(str).iloc[0]) if not comp_group["source_intensity_representation_class"].dropna().empty else "UNRESOLVED",
            "source_intensity_representation_status": _clean(comp_group["source_intensity_representation_status"].dropna().astype(str).iloc[0]) if not comp_group["source_intensity_representation_status"].dropna().empty else "BLOCKED_UNRESOLVED_INTENSITY_REPRESENTATION",
            "source_intensity_exact_fit_candidates_json": _clean(comp_group["source_intensity_exact_fit_candidates_json"].dropna().astype(str).iloc[0]) if not comp_group["source_intensity_exact_fit_candidates_json"].dropna().empty else "[]",
            "normalized_intensity_min": V552_NORMALIZED_INTENSITY_MIN,
            "normalized_intensity_max": V552_NORMALIZED_INTENSITY_MAX,
            "source_scale_direction_token": _clean(comp_group["source_scale_direction_token"].dropna().astype(str).iloc[0]) if not comp_group["source_scale_direction_token"].dropna().empty else "",
            "direction_scale_consistency_status": _clean(comp_group["direction_scale_consistency_status"].dropna().astype(str).iloc[0]) if not comp_group["direction_scale_consistency_status"].dropna().empty else "NOT_EVALUATED",
            "distribution_weight_basis": basis, "component_atom_count": int(len(comp_group)), "eligible_component_atom_count": eligible_count,
            "unique_response_component_count": int(comp_group["response_value_normalized"].fillna("").astype(str).nunique()),
            "source_intensity_zero_component_count": int(comp_group["source_intensity_zero"].fillna(False).astype(bool).sum()),
            "canonical_signed_zero_component_count": int(comp_group["canonical_signed_component_zero"].fillna(False).astype(bool).sum()),
            "distribution_mass_raw": mass_raw, "distribution_mass_used": 1.0 if pressure_score is not None else None,
            "substantive_response_coverage": coverage, "respondent_denominator_unweighted": denominator,
            "weighted_response_mass": float(pd.to_numeric(comp_group["n_weighted"], errors="coerce").dropna().sum()) if comp_group["n_weighted"].notna().any() else None,
            "pressure_score": pressure_score, "pressure_magnitude": state.pressure_magnitude,
            "pressure_orientation": state.pressure_orientation,
            "pressure_score_status": state.pressure_score_status, "observed_pressure_zero": state.observed_pressure_zero,
            "positive_component_share": pos_share, "negative_component_share": neg_share, "neutral_component_share": neu_share,
            "directional_entropy": entropy, "polarization_index": polarization, "dominant_orientation": dominant,
            "dominant_orientation_share": dominant_share, "component_signed_intensity_min": float(signed_values.min()) if not signed_values.empty else None,
            "component_signed_intensity_max": float(signed_values.max()) if not signed_values.empty else None,
            "component_signed_intensity_std": std, "support_status_rollup": _clean(first.get("support_status")),
            "confidence_tier_rollup": _clean(first.get("confidence_tier")), "component_permission_status": state.component_permission_status,
            "pressure_observation_status": state.pressure_observation_status, "v552j_pressure_linkage_eligible": state.v552j_pressure_linkage_eligible,
            "v552j_structural_context_eligible": state.v552j_structural_context_eligible, "v553_probe_candidate_after_v552j": state.v553_probe_candidate_after_v552j,
            "allowed_for_v553_temporal_field": False, "pressure_observation_ineligibility_reason": state.pressure_observation_ineligibility_reason,
            "known_absences_json": _json_dumps(sorted(set(atom_group.get("known_absences", pd.Series(dtype=str)).fillna("").astype(str).tolist()))),
            "forbidden_inference_json": _json_dumps(sorted(set(atom_group.get("forbidden_inference", pd.Series(dtype=str)).fillna("").astype(str).tolist()))),
            "evidence_basis_json": _json_dumps(sorted(set(atom_group.get("evidence_basis", pd.Series(dtype=str)).fillna("").astype(str).tolist()))),
            "provenance_basis_json": _json_dumps(sorted(set(atom_group.get("provenance_basis", pd.Series(dtype=str)).fillna("").astype(str).tolist()))),
            "pressure_measurement_hash": "",
            "input_atom_hash": _stable_hash_v21(atom_hashes), "created_at": now, "schema_version": V552_SCHEMA_VERSION,
            "compiler_version": V552_HANDOFF_SCHEMA_VERSION,
        }
        row["pressure_measurement_hash"] = recompute_v552_v2_1_4_pressure_measurement_hash(row, component_index.loc[comp_group.index].to_dict("records"))
        rows.append(row)
    return pd.DataFrame(rows).reindex(columns=V552_PRESSURE_OBSERVATION_INDEX_SCHEMA["required_columns"])


def build_v552_pressure_observation_audit(observations: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in observations.iterrows():
        d = row.to_dict()
        rows.append({
            "run_id": d.get("run_id", ""), "candidate_group_id": d.get("v552_pressure_observation_id", ""),
            "source": d.get("source", ""), "canonical_wave": d.get("canonical_wave", ""), "country_code": d.get("country_code", ""),
            "empirical_object_id": d.get("empirical_object_id", ""), "empirical_distribution_id": d.get("empirical_distribution_id", ""),
            "question_id": d.get("question_id", ""), "var_code": d.get("var_code", ""),
            "component_atom_count": d.get("component_atom_count", 0), "eligible_component_atom_count": d.get("eligible_component_atom_count", 0),
            "ineligible_component_atom_count": int(d.get("component_atom_count") or 0) - int(d.get("eligible_component_atom_count") or 0),
            "review_required_component_atom_count": 1 if d.get("component_permission_status") == "REVIEW_REQUIRED_COMPONENTS" else 0,
            "component_permission_status": d.get("component_permission_status", ""), "identity_validation_status": "PASS",
            "direction_validation_status": d.get("direction_scale_consistency_status", ""), "intensity_validation_status": d.get("scale_encoding_status", ""),
            "weight_basis_status": d.get("distribution_weight_basis", ""), "distribution_mass_status": "PASS" if d.get("pressure_score") is not None else "NOT_COMPUTABLE",
            "pressure_observation_status": d.get("pressure_observation_status", ""), "pressure_score_status": d.get("pressure_score_status", ""),
            "pressure_score": d.get("pressure_score"), "ineligibility_reasons": d.get("pressure_observation_ineligibility_reason", ""),
            "source_atom_ids_json": d.get("source_atom_ids_json", "[]"), "source_atom_contract_hashes_json": d.get("source_atom_contract_hashes_json", "[]"),
            "created_at": d.get("created_at", _utc_now()), "schema_version": V552_SCHEMA_VERSION,
        })
    return pd.DataFrame(rows).reindex(columns=V552_PRESSURE_OBSERVATION_AUDIT_SCHEMA["required_columns"])


def build_v552_intensity_representation_resolution_audit(component_index: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "source", "source_family", "canonical_wave", "country_code", "empirical_distribution_id",
        "question_id", "var_code", "component_count", "source_scale_direction_tokens_json",
        "directionality_policies_json", "response_topologies_json", "axis_candidate_exact_fit",
        "magnitude_candidate_exact_fit", "exact_fit_candidates_json", "selected_representation_class",
        "representation_resolution_status", "resolution_reason", "schema_version", "compiler_version",
    ]
    if component_index.empty:
        return pd.DataFrame(columns=columns)
    rows = []
    for _, group in component_index.groupby("empirical_distribution_id", dropna=False, sort=True):
        first = group.iloc[0].to_dict()
        exact = json.loads(_clean(first.get("source_intensity_exact_fit_candidates_json")) or "[]")
        rows.append({
            "source": first.get("source", ""),
            "source_family": first.get("source_family", ""),
            "canonical_wave": first.get("canonical_wave", ""),
            "country_code": first.get("country_code", ""),
            "empirical_distribution_id": first.get("empirical_distribution_id", ""),
            "question_id": first.get("question_id", ""),
            "var_code": first.get("var_code", ""),
            "component_count": int(len(group)),
            "source_scale_direction_tokens_json": _json_dumps(sorted(set(group["scale_direction"].fillna("").astype(str).tolist()))),
            "directionality_policies_json": _json_dumps(sorted(set(group["directionality_policy"].fillna("").astype(str).tolist()))),
            "response_topologies_json": _json_dumps(sorted(set(group["response_topology"].fillna("").astype(str).tolist()))),
            "axis_candidate_exact_fit": "NORMALIZED_AXIS_COORDINATE_0_1" in exact,
            "magnitude_candidate_exact_fit": "NORMALIZED_UNSIGNED_MAGNITUDE_0_1" in exact,
            "exact_fit_candidates_json": _json_dumps(exact),
            "selected_representation_class": first.get("source_intensity_representation_class", ""),
            "representation_resolution_status": first.get("source_intensity_representation_status", ""),
            "resolution_reason": "" if first.get("source_intensity_representation_status") == "EXACT_UNIQUE_DISTRIBUTION_RESOLUTION" else first.get("component_pressure_ineligibility_reason", ""),
            "schema_version": V552_SCHEMA_VERSION,
            "compiler_version": V552_HANDOFF_SCHEMA_VERSION,
        })
    return pd.DataFrame(rows).reindex(columns=columns)


def _observed(observations: pd.DataFrame) -> pd.DataFrame:
    if observations.empty:
        return observations.copy()
    return observations[observations["pressure_score_status"].isin(["OBSERVED_NONZERO", "OBSERVED_ZERO"])].copy()


def _rollup_identity_status(group: pd.DataFrame) -> str:
    counts = [group[c].fillna("").astype(str).nunique() for c in ["semantic_identity_signature", "structural_identity_signature", "response_scale_signature"]]
    if counts == [1, 1, 1]:
        return "EXACT_IDENTITY_ROLLUP"
    labels = []
    if counts[0] > 1:
        labels.append("SEMANTIC")
    if counts[1] > 1:
        labels.append("STRUCTURAL")
    if counts[2] > 1:
        labels.append("SCALE")
    return "HETEROGENEOUS_MULTI_DIMENSION_SUMMARY" if len(labels) > 1 else f"HETEROGENEOUS_{labels[0]}_SUMMARY"


def _build_pressure_rollup_row(group: pd.DataFrame, keys: dict[str, Any], run_id: str) -> dict[str, Any]:
    scores = pd.to_numeric(group["pressure_score"], errors="coerce").dropna()
    identity_status = _rollup_identity_status(group)
    ids = sorted(group["v552_pressure_observation_id"].astype(str).tolist())
    sample = pd.to_numeric(group["respondent_denominator_unweighted"], errors="coerce").dropna()
    row = {**keys}
    row.update({
        "run_id": run_id, "source": keys.get("source", group.iloc[0].get("source", "")), "wave": keys.get("wave", group.iloc[0].get("wave", "")),
        "canonical_wave": keys.get("canonical_wave", group.iloc[0].get("canonical_wave", "")), "country_code": keys.get("country_code", group.iloc[0].get("country_code", "")),
        "n_atoms": int(group["component_atom_count"].sum()), "n_unweighted_total": float(sample.iloc[0]) if len(group) == 1 and not sample.empty else None,
        "n_weighted_total": float(pd.to_numeric(group["weighted_response_mass"], errors="coerce").sum()) if len(group) == 1 else None,
        "pressure_score": float(scores.mean()) if not scores.empty else None, "entropy": None,
        "polarization_index": None, "dominant_orientation": group["pressure_orientation"].mode().iloc[0] if not group.empty else "",
        "support_status": group["support_status_rollup"].mode().iloc[0] if "support_status_rollup" in group and not group.empty else "",
        "confidence_tier": group["confidence_tier_rollup"].mode().iloc[0] if "confidence_tier_rollup" in group and not group.empty else "",
        "basis": "primary_pressure_observation_equal_weight_mean", "status": "observed_pressure_rollup" if not scores.empty else "not_computable",
        "n_pressure_observations": int(len(group)), "n_unique_empirical_objects": int(group["empirical_object_id"].nunique()),
        "sample_n_min": float(sample.min()) if not sample.empty else None, "sample_n_max": float(sample.max()) if not sample.empty else None,
        "sample_n_median": float(sample.median()) if not sample.empty else None, "summed_component_atom_count": int(group["component_atom_count"].sum()),
        "summed_category_n_unweighted_audit": None, "semantic_identity_count": int(group["semantic_identity_signature"].nunique()),
        "structural_identity_count": int(group["structural_identity_signature"].nunique()), "response_scale_signature_count": int(group["response_scale_signature"].nunique()),
        "rollup_identity_status": identity_status, "v552j_pressure_linkage_eligible": identity_status == "EXACT_IDENTITY_ROLLUP",
        "allowed_for_v553_temporal_field": False, "source_pressure_observation_ids_json": _json_dumps(ids),
        "schema_version": V552_SCHEMA_VERSION, "created_at": _utc_now(),
    })
    return row


def _rollup(observations: pd.DataFrame, group_cols: list[str], id_col: str, run_id: str, schema: dict[str, Any]) -> pd.DataFrame:
    obs = _observed(observations)
    if obs.empty:
        return pd.DataFrame(columns=schema["required_columns"])
    rows = []
    for key, group in obs.groupby(group_cols, dropna=False, sort=True):
        if not isinstance(key, tuple):
            key = (key,)
        keys = dict(zip(group_cols, key))
        row = _build_pressure_rollup_row(group, keys, run_id)
        row[id_col] = _id("v552ru__", keys)
        rows.append(row)
    return pd.DataFrame(rows).reindex(columns=schema["required_columns"])


def build_relation_axis_pressure_from_observations(observations: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    return _rollup(observations, ["source", "wave", "canonical_wave", "country_code", "relation_axis_id"], "relation_axis_pressure_id", run_id, V552_RELATION_AXIS_PRESSURE_SCHEMA)


def build_target_entity_pressure_from_observations(observations: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    return _rollup(observations, ["source", "wave", "canonical_wave", "country_code", "target_entity_id"], "target_entity_pressure_id", run_id, V552_TARGET_ENTITY_PRESSURE_SCHEMA)


def build_driver_facet_pressure_from_observations(observations: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    return _rollup(observations, ["source", "wave", "canonical_wave", "country_code", "driver_facet_id"], "driver_facet_pressure_id", run_id, V552_DRIVER_FACET_PRESSURE_SCHEMA)


def build_country_wave_pressure_profile_from_observations(observations: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    frame = _rollup(observations, ["source", "wave", "canonical_wave", "country_code"], "country_wave_pressure_profile_id", run_id, V552_COUNTRY_WAVE_PRESSURE_PROFILE_SCHEMA)
    if not frame.empty:
        frame["fact_measure_class"] = "country_wave_pressure_summary"
        frame["v552j_pressure_linkage_eligible"] = False
        frame["allowed_for_v553_temporal_field"] = False
    return frame


def build_structural_channel_index_from_observations(observations: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    obs = _observed(observations)
    if obs.empty:
        return pd.DataFrame(columns=V552_STRUCTURAL_CHANNEL_INDEX_SCHEMA["required_columns"])
    routed = obs[(obs["strata_path"].fillna("").astype(str).str.strip() != "") | (obs["subject_position_signature"].fillna("").astype(str).str.strip() != "") | (obs["position_conditioning"].fillna("").astype(str).str.strip() != "") | ((obs["position_field"].fillna("").astype(str).str.strip() != "") & (obs["position_value"].fillna("").astype(str).str.strip() != ""))]
    if routed.empty:
        return pd.DataFrame(columns=V552_STRUCTURAL_CHANNEL_INDEX_SCHEMA["required_columns"])
    cols = ["source", "wave", "canonical_wave", "country_code", "structural_identity_signature", "relation_axis_id", "target_entity_id", "driver_id", "driver_facet_id", "strata_path", "subject_position_signature", "position_conditioning", "position_modifiers", "conditional_strata_weights"]
    frame = _rollup(routed, cols, "channel_id", run_id, V552_STRUCTURAL_CHANNEL_INDEX_SCHEMA)
    if not frame.empty:
        frame["channel_type"] = "observed_structural_route"
    return frame


def build_position_conditioning_profile_from_observations(observations: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    obs = _observed(observations)
    if obs.empty:
        return pd.DataFrame(columns=V552_POSITION_CONDITIONING_PROFILE_SCHEMA["required_columns"])
    pos = obs[(obs["subject_position_signature"].fillna("").astype(str).str.strip() != "") | ((obs["position_field"].fillna("").astype(str).str.strip() != "") & (obs["position_value"].fillna("").astype(str).str.strip() != "")) | (obs["position_conditioning"].fillna("").astype(str).str.strip() != "")]
    if pos.empty:
        return pd.DataFrame(columns=V552_POSITION_CONDITIONING_PROFILE_SCHEMA["required_columns"])
    return _rollup(pos, ["source", "wave", "canonical_wave", "country_code", "structural_identity_signature", "subject_position_signature", "position_conditioning", "position_modifiers", "strata_path"], "position_conditioning_profile_id", run_id, V552_POSITION_CONDITIONING_PROFILE_SCHEMA)


def build_contradiction_tensor_from_observations(observations: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    obs = _observed(observations)
    if obs.empty:
        return pd.DataFrame(columns=V552_CONTRADICTION_TENSOR_SCHEMA["required_columns"])
    rows = []
    cols = ["source", "wave", "canonical_wave", "country_code", "relation_axis_id", "target_entity_id", "driver_id", "driver_facet_id", "semantic_identity_signature", "structural_identity_signature", "response_scale_signature"]
    for key, group in obs.groupby(cols, dropna=False, sort=True):
        pos = group[group["pressure_score"] > V552_EPSILON]
        neg = group[group["pressure_score"] < -V552_EPSILON]
        if group["empirical_object_id"].nunique() < 2 or pos.empty or neg.empty:
            continue
        pos_mass = float(pos["pressure_score"].abs().sum())
        neg_mass = float(neg["pressure_score"].abs().sum())
        score = 2 * min(pos_mass, neg_mass) / (pos_mass + neg_mass)
        keydict = dict(zip(cols, key if isinstance(key, tuple) else (key,)))
        rows.append({**keydict, "run_id": run_id, "contradiction_id": _id("v552ct__", keydict), "axis_a": keydict["relation_axis_id"], "axis_b": keydict["relation_axis_id"], "positive_atom_count": int(len(pos)), "negative_atom_count": int(len(neg)), "opposing_directionality_present": True, "contradiction_score": score, "support_status": "", "confidence_tier": "", "basis": "opposed_comparable_primary_pressure_observations", "status": "OBSERVED_CONTRADICTION", "positive_pressure_observation_count": int(len(pos)), "negative_pressure_observation_count": int(len(neg)), "positive_pressure_mass": pos_mass, "negative_pressure_mass": neg_mass, "positive_pressure_observation_ids_json": _json_dumps(sorted(pos["v552_pressure_observation_id"].astype(str).tolist())), "negative_pressure_observation_ids_json": _json_dumps(sorted(neg["v552_pressure_observation_id"].astype(str).tolist())), "contradiction_basis": "opposed_comparable_primary_pressure_observations", "fact_measure_class": "observed_within_wave_structural_contradiction", "created_at": _utc_now(), "schema_version": V552_SCHEMA_VERSION})
    return pd.DataFrame(rows).reindex(columns=V552_CONTRADICTION_TENSOR_SCHEMA["required_columns"])


def _empty(schema: dict[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(columns=schema["required_columns"])


def _fact_index(observations: pd.DataFrame, rollups: dict[str, pd.DataFrame], contradiction: pd.DataFrame, run_id: str) -> pd.DataFrame:
    rows = []
    for _, obs in observations.iterrows():
        d = obs.to_dict()
        rows.append({
            "run_id": run_id, "v552_structural_fact_id": _id("v552sf__", {"po": d["v552_pressure_observation_id"]}), "source_run_id": d.get("source_v551_run_id", ""),
            "source_artifact": "v552_pressure_observation_index", "source_row_index": len(rows), "source_row_id": d["v552_pressure_observation_id"],
            "source_row_hash": d.get("pressure_measurement_hash", ""), "source": d.get("source", ""), "wave": d.get("wave", ""), "canonical_wave": d.get("canonical_wave", ""),
            "country_code": d.get("country_code", ""), "structural_fact_type": "primary_pressure_observation", "structural_fact_lane": "primary_pressure",
            "structural_fact_grain": "empirical_distribution_pressure_observation", "empirical_distribution_id": d.get("empirical_distribution_id", ""),
            "component_response_surface_signature": d.get("component_response_surface_signature", ""),
            "response_surface_completeness_status": d.get("response_surface_completeness_status", ""),
            "pressure_measurement_hash": d.get("pressure_measurement_hash", ""),
            "question_id": d.get("question_id", ""), "relation_axis_id": d.get("relation_axis_id", ""),
            "target_entity_id": d.get("target_entity_id", ""), "driver_facet_id": d.get("driver_facet_id", ""), "structural_channel_id": "",
            "horizon_constraint_id": "", "semantic_signature": d.get("semantic_identity_signature", ""), "pressure_score": d.get("pressure_score"),
            "pressure_score_status": d.get("pressure_score_status"), "fact_measure_class": "primary_pressure_observation",
            "pressure_measure_class": d.get("pressure_measure_class", ""), "pressure_formula_id": d.get("pressure_formula_id"),
            "pressure_formula_version": d.get("pressure_formula_version"), "pressure_scale_id": d.get("pressure_scale_id"),
            "source_intensity_representation_class": d.get("source_intensity_representation_class", ""),
            "source_intensity_representation_status": d.get("source_intensity_representation_status", ""),
            "source_intensity_exact_fit_candidates_json": d.get("source_intensity_exact_fit_candidates_json", "[]"),
            "normalized_intensity_min": d.get("normalized_intensity_min"),
            "normalized_intensity_max": d.get("normalized_intensity_max"),
            "source_scale_direction_token": d.get("source_scale_direction_token", ""),
            "source_pressure_observation_ids_json": _json_dumps([d["v552_pressure_observation_id"]]), "semantic_identity_signature": d.get("semantic_identity_signature", ""),
            "structural_identity_signature": d.get("structural_identity_signature", ""), "response_scale_signature": d.get("response_scale_signature", ""),
            "directionality_policy": d.get("directionality_policy", ""), "response_topology": d.get("response_topology", ""), "strata_path": d.get("strata_path", ""),
            "subject_position_signature": d.get("subject_position_signature", ""), "position_conditioning": d.get("position_conditioning", ""),
            "pressure_anchor_candidate_after_v552j": bool(d.get("v552j_pressure_linkage_eligible")), "v552j_pressure_linkage_eligible": bool(d.get("v552j_pressure_linkage_eligible")),
            "v552j_structural_context_eligible": bool(d.get("v552j_structural_context_eligible")), "v553_probe_candidate_after_v552j": bool(d.get("v553_probe_candidate_after_v552j")),
            "allowed_for_v553_temporal_field": bool(d.get("allowed_for_v553_temporal_field")), "entropy": d.get("directional_entropy"), "polarization_index": d.get("polarization_index"),
            "dominant_orientation": d.get("dominant_orientation"), "n_atoms": d.get("component_atom_count"), "n_unweighted_total": d.get("respondent_denominator_unweighted"),
            "n_weighted_total": d.get("weighted_response_mass"), "support_status": d.get("support_status_rollup", ""), "confidence_tier": d.get("confidence_tier_rollup", ""),
            "directionality_coverage": "", "pressure_computation_status": d.get("pressure_observation_status", ""), "compiler_status": d.get("pressure_observation_status", ""),
            "structural_fact_status": "resolved" if d.get("pressure_score") is not None else "context_only", "allowed_v552j_use": "v552j_pressure_linkage_source" if d.get("v552j_pressure_linkage_eligible") else ("v552j_structural_context_only" if d.get("v552j_structural_context_eligible") else "not_authorized"),
            "forbidden_downstream_use": "direct_v553_temporal_field", "known_absences_json": d.get("known_absences_json", "[]"), "source_trace_json": _json_dumps({"source_pressure_observation_id": d["v552_pressure_observation_id"]}),
            "source_artifact_row_count": 1, "created_at": _utc_now(), "schema_version": V552_SCHEMA_VERSION, "compiler_version": V552_HANDOFF_SCHEMA_VERSION,
        })
    return pd.DataFrame(rows).reindex(columns=V552_STRUCTURAL_FACT_INDEX_SCHEMA["required_columns"])


def _temporal_key_index(facts: pd.DataFrame, run_id: str) -> pd.DataFrame:
    if facts.empty:
        return _empty(V552_TEMPORAL_KEY_SOURCE_INDEX_SCHEMA)
    rows = []
    for _, row in facts.iterrows():
        d = row.to_dict()
        candidate = bool(d.get("v552j_pressure_linkage_eligible")) and _clean(d.get("pressure_score_status")) in {"OBSERVED_NONZERO", "OBSERVED_ZERO"}
        rows.append({
            "run_id": run_id, "v552_temporal_key_source_id": _id("v552tks__", {"fact": d.get("v552_structural_fact_id")}), "v552_structural_fact_id": d.get("v552_structural_fact_id"),
            "source_run_id": d.get("source_run_id", ""), "source_artifact": d.get("source_artifact", ""), "source_row_index": d.get("source_row_index", 0),
            "source_row_id": d.get("source_row_id", ""), "source_row_hash": d.get("source_row_hash", ""), "source": d.get("source", ""), "wave": d.get("wave", ""),
            "canonical_wave": d.get("canonical_wave", ""), "country_code": d.get("country_code", ""), "structural_fact_type": d.get("structural_fact_type", ""),
            "structural_fact_lane": d.get("structural_fact_lane", ""), "structural_fact_grain": d.get("structural_fact_grain", ""),
            "empirical_distribution_id": d.get("empirical_distribution_id", ""),
            "component_response_surface_signature": d.get("component_response_surface_signature", ""),
            "response_surface_completeness_status": d.get("response_surface_completeness_status", ""),
            "pressure_measure_class": d.get("pressure_measure_class", ""),
            "pressure_formula_id": d.get("pressure_formula_id", ""),
            "pressure_formula_version": d.get("pressure_formula_version", ""),
            "pressure_scale_id": d.get("pressure_scale_id", ""),
            "pressure_measurement_hash": d.get("pressure_measurement_hash", ""),
            "semantic_identity_signature": d.get("semantic_identity_signature", ""),
            "structural_identity_signature": d.get("structural_identity_signature", ""),
            "response_scale_signature": d.get("response_scale_signature", ""),
            "directionality_policy": d.get("directionality_policy", ""),
            "response_topology": d.get("response_topology", ""),
            "source_intensity_representation_class": d.get("source_intensity_representation_class", ""),
            "source_intensity_representation_status": d.get("source_intensity_representation_status", ""),
            "source_intensity_exact_fit_candidates_json": d.get("source_intensity_exact_fit_candidates_json", "[]"),
            "normalized_intensity_min": d.get("normalized_intensity_min"),
            "normalized_intensity_max": d.get("normalized_intensity_max"),
            "source_scale_direction_token": d.get("source_scale_direction_token", ""),
            "question_id": d.get("question_id", ""),
            "relation_axis_id": d.get("relation_axis_id", ""), "target_entity_id": d.get("target_entity_id", ""), "driver_facet_id": d.get("driver_facet_id", ""),
            "structural_channel_id": d.get("structural_channel_id", ""), "horizon_constraint_id": d.get("horizon_constraint_id", ""), "semantic_signature": d.get("semantic_signature", ""),
            "temporal_key_grain": "v552j_pressure_linkage_candidate" if candidate else "context_only", "temporal_key_basis": _json_dumps({"fact": d.get("v552_structural_fact_id")}),
            "temporal_key_candidate_status": "CANDIDATE_FOR_V552J_PRESSURE_LINKAGE" if candidate else "BLOCKED_NO_OBSERVED_PRESSURE",
            "temporal_key_blocker_reason": "" if candidate else "no_observed_pressure", "fallback_permission_profile_key": "", "fallback_used": False,
            "resolution_status": "candidate_after_v552j" if candidate else "context_only", "allowed_downstream_use": "v552j_pressure_linkage_source" if candidate else "v552j_structural_context_only",
            "pressure_score": d.get("pressure_score"), "pressure_score_status": d.get("pressure_score_status"),
            "support_status": d.get("support_status", ""), "confidence_tier": d.get("confidence_tier", ""), "directionality_coverage": d.get("directionality_coverage", ""),
            "allowed_for_v552j": candidate, "allowed_for_v553_probe": False, "allowed_for_v553_temporal_field": False,
            "known_absences_json": d.get("known_absences_json", "[]"), "source_trace_json": d.get("source_trace_json", "{}"), "source_artifact_row_count": 1,
            "created_at": _utc_now(), "schema_version": V552_SCHEMA_VERSION, "compiler_version": V552_HANDOFF_SCHEMA_VERSION,
        })
    return pd.DataFrame(rows).reindex(columns=V552_TEMPORAL_KEY_SOURCE_INDEX_SCHEMA["required_columns"])


def _handoff(outputs: dict[str, pd.DataFrame], run_id: str) -> pd.DataFrame:
    rows = []
    lane_map = {
        "v552_pressure_component_index": ("artifact_inventory_only", "not_pressure_observation_linkage"),
        "v552_pressure_observation_index": ("artifact_inventory_only", "not_pressure_observation_linkage"),
        "v552_structural_fact_index": ("artifact_inventory_only", "not_pressure_observation_linkage"),
        "v552_temporal_key_source_index": ("artifact_inventory_only", "not_pressure_observation_linkage"),
        "relation_axis_pressure": ("pressure_rollup", "v552j_structural_context_input"),
        "target_entity_pressure": ("pressure_rollup", "v552j_structural_context_input"),
        "driver_facet_pressure": ("pressure_rollup", "v552j_structural_context_input"),
        "structural_channel_index": ("pressure_rollup", "v552j_structural_context_input"),
        "position_conditioning_profile": ("pressure_rollup", "v552j_structural_context_input"),
        "contradiction_tensor": ("contradiction_context", "v552j_contradiction_context_input"),
    }
    for name, (lane, perm) in lane_map.items():
        frame = outputs.get(name, pd.DataFrame())
        rows.append({
            "run_id": run_id, "handoff_index_id": _id("v552hi__", {"artifact": name, "run": run_id}), "artifact_name": name,
            "artifact_lane": lane, "artifact_status": "populated" if not frame.empty else "not_applicable",
            "artifact_path_csv": f"structural/{name}.csv", "artifact_path_parquet": f"structural/{name}.parquet",
            "source": _clean(frame.iloc[0].get("source")) if not frame.empty and "source" in frame.columns else "",
            "wave": _clean(frame.iloc[0].get("wave")) if not frame.empty and "wave" in frame.columns else "",
            "canonical_wave": _clean(frame.iloc[0].get("canonical_wave")) if not frame.empty and "canonical_wave" in frame.columns else "",
            "country_code": _clean(frame.iloc[0].get("country_code")) if not frame.empty and "country_code" in frame.columns else "",
            "runtime_use_class": "not_runtime_authorized", "downstream_permission_class": perm, "downstream_consumer_layer": "V552J",
            "requires_directionality": lane in {"primary_pressure", "pressure_rollup", "contradiction_context"},
            "ready_for_v552j_inspection": not frame.empty, "ready_for_v553_after_v552j": False, "known_absences_json": "[]",
            "v553_comparability_key": "", "temporal_anchor_hint": "candidate_after_v552j" if perm == "v552j_pressure_linkage_input" else "context_only",
            "source_intensity_representation_class": _clean(frame.iloc[0].get("source_intensity_representation_class")) if not frame.empty and "source_intensity_representation_class" in frame.columns else "",
            "source_intensity_representation_status": _clean(frame.iloc[0].get("source_intensity_representation_status")) if not frame.empty and "source_intensity_representation_status" in frame.columns else "",
            "source_intensity_exact_fit_candidates_json": _clean(frame.iloc[0].get("source_intensity_exact_fit_candidates_json")) if not frame.empty and "source_intensity_exact_fit_candidates_json" in frame.columns else "[]",
            "normalized_intensity_min": frame.iloc[0].get("normalized_intensity_min") if not frame.empty and "normalized_intensity_min" in frame.columns else None,
            "normalized_intensity_max": frame.iloc[0].get("normalized_intensity_max") if not frame.empty and "normalized_intensity_max" in frame.columns else None,
            "source_scale_direction_token": _clean(frame.iloc[0].get("source_scale_direction_token")) if not frame.empty and "source_scale_direction_token" in frame.columns else "",
            "comparability_status": "not_evaluated_at_v552", "created_at": _utc_now(), "schema_version": V552_SCHEMA_VERSION,
        })
    return pd.DataFrame(rows).reindex(columns=V552_TO_V552J_HANDOFF_INDEX_SCHEMA["required_columns"])


def _pressure_observation_handoff(observations: pd.DataFrame, components: pd.DataFrame, run_id: str) -> pd.DataFrame:
    columns = [
        "run_id", "handoff_id", "v552_pressure_observation_id", "pressure_observation_identity_hash",
        "empirical_distribution_id", "source", "source_family", "wave", "canonical_wave", "country_code",
        "question_id", "var_code", "semantic_identity_signature", "structural_identity_signature",
        "response_scale_signature", "source_atom_ids_json", "source_atom_contract_hashes_json",
        "source_measurement_contract_hashes_json", "v552_pressure_component_ids_json",
        "v552_component_measurement_hashes_json", "source_intensity_representation_class",
        "source_intensity_representation_status", "source_intensity_exact_fit_candidates_json",
        "component_response_surface_signature", "response_surface_completeness_status",
        "pressure_measure_class", "pressure_score", "pressure_score_status", "pressure_formula_id",
        "pressure_formula_version", "pressure_scale_id", "pressure_measurement_hash",
        "v552j_pressure_linkage_eligible", "known_absences_json", "forbidden_inference_json",
        "direct_v553_authorization", "temporal_authority", "runtime_authority", "created_at",
        "schema_version", "compiler_version",
    ]
    if observations.empty:
        return pd.DataFrame(columns=columns)
    rows = []
    for _, obs in observations.iterrows():
        d = obs.to_dict()
        comp_group = components[components["v552_pressure_observation_id"].fillna("").astype(str).eq(str(d.get("v552_pressure_observation_id", "")))]
        rows.append({
            "run_id": run_id,
            "handoff_id": _id("v552poh__", {"po": d.get("v552_pressure_observation_id")}),
            "v552_pressure_observation_id": d.get("v552_pressure_observation_id", ""),
            "pressure_observation_identity_hash": d.get("pressure_observation_identity_hash", ""),
            "empirical_distribution_id": d.get("empirical_distribution_id", ""),
            "source": d.get("source", ""),
            "source_family": d.get("source_family", ""),
            "wave": d.get("wave", ""),
            "canonical_wave": d.get("canonical_wave", ""),
            "country_code": d.get("country_code", ""),
            "question_id": d.get("question_id", ""),
            "var_code": d.get("var_code", ""),
            "semantic_identity_signature": d.get("semantic_identity_signature", ""),
            "structural_identity_signature": d.get("structural_identity_signature", ""),
            "response_scale_signature": d.get("response_scale_signature", ""),
            "source_atom_ids_json": d.get("source_atom_ids_json", "[]"),
            "source_atom_contract_hashes_json": d.get("source_atom_contract_hashes_json", "[]"),
            "source_measurement_contract_hashes_json": d.get("source_measurement_contract_hashes_json", "[]"),
            "v552_pressure_component_ids_json": _json_dumps(sorted(comp_group.get("v552_pressure_component_id", pd.Series(dtype=str)).fillna("").astype(str).tolist())),
            "v552_component_measurement_hashes_json": _json_dumps(sorted(comp_group.get("component_measurement_hash", pd.Series(dtype=str)).fillna("").astype(str).tolist())),
            "source_intensity_representation_class": d.get("source_intensity_representation_class", ""),
            "source_intensity_representation_status": d.get("source_intensity_representation_status", ""),
            "source_intensity_exact_fit_candidates_json": d.get("source_intensity_exact_fit_candidates_json", "[]"),
            "component_response_surface_signature": d.get("component_response_surface_signature", ""),
            "response_surface_completeness_status": d.get("response_surface_completeness_status", ""),
            "pressure_measure_class": d.get("pressure_measure_class", ""),
            "pressure_score": d.get("pressure_score"),
            "pressure_score_status": d.get("pressure_score_status", ""),
            "pressure_formula_id": d.get("pressure_formula_id", ""),
            "pressure_formula_version": d.get("pressure_formula_version", ""),
            "pressure_scale_id": d.get("pressure_scale_id", ""),
            "pressure_measurement_hash": d.get("pressure_measurement_hash", ""),
            "v552j_pressure_linkage_eligible": bool(d.get("v552j_pressure_linkage_eligible")),
            "known_absences_json": d.get("known_absences_json", "[]"),
            "forbidden_inference_json": d.get("forbidden_inference_json", "[]"),
            "direct_v553_authorization": False,
            "temporal_authority": False,
            "runtime_authority": False,
            "created_at": _utc_now(),
            "schema_version": V552_SCHEMA_VERSION,
            "compiler_version": V552_HANDOFF_SCHEMA_VERSION,
        })
    return pd.DataFrame(rows).reindex(columns=columns)


def validate_v552_v2_1_output_contract(outputs: Mapping[str, pd.DataFrame]) -> list[str]:
    issues: list[str] = []
    atoms = outputs.get("_input_atoms", pd.DataFrame())
    components = outputs.get("v552_pressure_component_index", pd.DataFrame())
    observations = outputs.get("v552_pressure_observation_index", pd.DataFrame())
    facts = outputs.get("v552_structural_fact_index", pd.DataFrame())
    temporal = outputs.get("v552_temporal_key_source_index", pd.DataFrame())
    # The current readiness contract counts the exact pressure-observation handoff,
    # not the older aggregate structural handoff.  Comparing different grains made
    # otherwise valid V552 outputs self-block at final validation.
    handoff = outputs.get(
        "v552_to_v552j_pressure_observation_handoff_index",
        outputs.get("v552_to_v552j_handoff_index", pd.DataFrame()),
    )
    readiness = outputs.get("v552_readiness_report", pd.DataFrame())
    allowed_pressure_measure_classes = {
        "single_question_scale_aware_directional_distribution_pressure",
        "single_question_scale_aware_conditional_selected_response_surface_pressure",
        "single_question_scale_aware_observed_response_surface_pressure_unknown_denominator",
        "single_question_scale_aware_directional_distribution_not_computable",
    }

    if not atoms.empty and len(components) != len(atoms):
        issues.append("component_count_not_equal_input_atom_count")
    if not atoms.empty and "empirical_distribution_id" in atoms.columns and len(observations) != atoms["empirical_distribution_id"].nunique():
        issues.append("observation_count_not_equal_empirical_distribution_count")
    if not observations.empty and "empirical_distribution_id" in observations.columns:
        if observations["empirical_distribution_id"].fillna("").astype(str).str.strip().eq("").any():
            issues.append("pressure_observation_missing_empirical_distribution_id")
    if "empirical_object_id_role" in observations.columns and ~observations["empirical_object_id_role"].eq("NON_AUTHORITATIVE_REPRESENTATIVE_COMPONENT_ONLY").all():
        issues.append("singular_category_id_used_as_authoritative_parent")
    if "empirical_parent_identity_class" in observations.columns and ~observations["empirical_parent_identity_class"].eq("empirical_distribution_id").all():
        issues.append("invalid_empirical_parent_identity_class")
    if "component_response_surface_signature" not in observations.columns or observations["component_response_surface_signature"].fillna("").astype(str).str.strip().eq("").any():
        issues.append("pressure_observation_missing_response_surface_signature")
    if "pressure_formula_version" in observations.columns and ~observations["pressure_formula_version"].fillna("").astype(str).eq(V552_PRESSURE_FORMULA_VERSION).all():
        issues.append("formula_version_not_v2_1")
    if "allowed_for_v553_temporal_field" in observations.columns and observations["allowed_for_v553_temporal_field"].fillna(False).astype(bool).any():
        issues.append("direct_v553_authorization_present")
    if "pressure_score" in observations.columns and "pressure_score_status" in observations.columns:
        blocked = ~observations["pressure_score_status"].isin(["OBSERVED_NONZERO", "OBSERVED_ZERO"])
        null_as_zero = blocked & pd.to_numeric(observations["pressure_score"], errors="coerce").eq(0.0)
        if null_as_zero.any():
            issues.append("null_pressure_serialized_as_zero")
        bad_linkage = blocked & observations.get("v552j_pressure_linkage_eligible", pd.Series(False, index=observations.index)).fillna(False).astype(bool)
        if bad_linkage.any():
            issues.append("blocked_pressure_marked_linkage_eligible")
    if "pressure_measure_class" in observations.columns:
        invalid_classes = ~observations["pressure_measure_class"].fillna("").astype(str).isin(allowed_pressure_measure_classes)
        if invalid_classes.any():
            issues.append("invalid_pressure_measure_class")

    if not components.empty and not observations.empty:
        for _, obs in observations.iterrows():
            obs_id = str(obs.get("v552_pressure_observation_id", ""))
            comp_group = components[components["v552_pressure_observation_id"].astype(str).eq(obs_id)]
            if comp_group.empty:
                continue
            if comp_group["empirical_distribution_id"].fillna("").astype(str).nunique() != 1:
                issues.append("pressure_observation_multiple_distribution_ids")
                break
            expected_signature = _component_response_surface_signature(comp_group)
            if str(obs.get("component_response_surface_signature", "")) != expected_signature:
                issues.append("response_surface_signature_disagreement")
                break
            status, coverage, _ = _response_surface_completeness(comp_group)
            if str(obs.get("response_surface_completeness_status", "")) != status:
                issues.append("response_surface_completeness_status_inconsistent")
                break
            measure_class = str(obs.get("pressure_measure_class", ""))
            if status == "PARTIAL_SELECTED_RESPONSE_CATEGORY_COVERAGE" and measure_class == "single_question_scale_aware_directional_distribution_pressure":
                issues.append("partial_surface_mislabeled_complete_distribution_pressure")
                break
            if status == "BLOCKED_RESPONSE_CATEGORY_COUNT_EXCEEDS_DENOMINATOR" and str(obs.get("pressure_score_status", "")).startswith("OBSERVED"):
                issues.append("blocked_surface_marked_observed")
                break

    if observations.empty:
        primary_facts = pd.DataFrame()
    elif facts.empty or not {"source_artifact", "source_row_id"}.issubset(facts.columns):
        primary_facts = pd.DataFrame()
        issues.append("missing_primary_structural_fact_for_pressure_observation")
        issues.append("primary_structural_fact_count_not_equal_pressure_observation_count")
    else:
        primary_facts = facts[facts["source_artifact"].astype(str).eq("v552_pressure_observation_index")]
        fact_counts = primary_facts["source_row_id"].fillna("").astype(str).value_counts().to_dict()
        for obs_id in observations["v552_pressure_observation_id"].fillna("").astype(str).tolist():
            if fact_counts.get(obs_id, 0) == 0:
                issues.append("missing_primary_structural_fact_for_pressure_observation")
                break
            if fact_counts.get(obs_id, 0) > 1:
                issues.append("duplicate_primary_structural_fact_for_pressure_observation")
                break
        if len(primary_facts) != len(observations):
            issues.append("primary_structural_fact_count_not_equal_pressure_observation_count")

    if not facts.empty:
        if "empirical_distribution_id" not in facts.columns or facts["empirical_distribution_id"].fillna("").astype(str).str.strip().eq("").any():
            issues.append("structural_fact_missing_distribution_id")
        if "structural_fact_grain" in facts.columns and ~facts["structural_fact_grain"].eq("empirical_distribution_pressure_observation").all():
            issues.append("invalid_structural_fact_grain")
        if "pressure_measure_class" not in facts.columns or facts["pressure_measure_class"].fillna("").astype(str).str.strip().eq("").any():
            issues.append("structural_fact_missing_pressure_measure_class")
        if {"source_row_id", "pressure_measure_class"}.issubset(facts.columns) and {"v552_pressure_observation_id", "pressure_measure_class"}.issubset(observations.columns):
            obs_class = observations.set_index("v552_pressure_observation_id")["pressure_measure_class"].astype(str).to_dict()
            for row in facts.to_dict("records"):
                expected = obs_class.get(str(row.get("source_row_id")), "")
                if expected and str(row.get("pressure_measure_class", "")) != expected:
                    issues.append("structural_fact_pressure_measure_class_mismatch")
                    break
        if not observations.empty and {"source_artifact", "source_row_id"}.issubset(facts.columns):
            obs_by_id = observations.set_index("v552_pressure_observation_id").to_dict("index") if "v552_pressure_observation_id" in observations.columns else {}
            for row in primary_facts.to_dict("records"):
                obs_row = obs_by_id.get(str(row.get("source_row_id")))
                if not obs_row:
                    continue
                for field in V552_PRESSURE_CONTRACT_CHAIN_FIELDS:
                    if _canon(row.get(field)) != _canon(obs_row.get(field)):
                        issues.append(f"observation_fact_pressure_contract_mismatch={field}")
                        break
                if any(item.startswith("observation_fact_pressure_contract_mismatch=") for item in issues):
                    break
    if facts.empty or "v552j_pressure_linkage_eligible" not in facts.columns:
        eligible_facts = pd.DataFrame()
    else:
        eligible_facts = facts[facts["v552j_pressure_linkage_eligible"].fillna(False).astype(bool)]

    if not eligible_facts.empty and (temporal.empty or "v552_structural_fact_id" not in temporal.columns):
        issues.append("missing_temporal_key_source_for_eligible_primary_fact")

    if not temporal.empty:
        if "pressure_measurement_hash" not in temporal.columns or temporal["pressure_measurement_hash"].fillna("").astype(str).str.strip().eq("").any():
            issues.append("temporal_source_missing_pressure_measurement_hash")
        if "pressure_measure_class" not in temporal.columns or temporal["pressure_measure_class"].fillna("").astype(str).str.strip().eq("").any():
            issues.append("temporal_source_missing_pressure_measure_class")
        if {"v552_structural_fact_id", "pressure_measure_class"}.issubset(temporal.columns) and {"v552_structural_fact_id", "pressure_measure_class"}.issubset(facts.columns):
            fact_class = facts.set_index("v552_structural_fact_id")["pressure_measure_class"].astype(str).to_dict()
            for row in temporal.to_dict("records"):
                expected = fact_class.get(str(row.get("v552_structural_fact_id")), "")
                if expected and str(row.get("pressure_measure_class", "")) != expected:
                    issues.append("temporal_source_pressure_measure_class_mismatch")
                    break
        if not eligible_facts.empty:
            temporal_counts = temporal["v552_structural_fact_id"].fillna("").astype(str).value_counts().to_dict() if "v552_structural_fact_id" in temporal.columns else {}
            for fact_id in eligible_facts["v552_structural_fact_id"].fillna("").astype(str).tolist():
                if temporal_counts.get(fact_id, 0) == 0:
                    issues.append("missing_temporal_key_source_for_eligible_primary_fact")
                    break
                if temporal_counts.get(fact_id, 0) > 1:
                    issues.append("duplicate_temporal_key_source_for_eligible_primary_fact")
                    break
            duplicate_temporal_ids = {key for key, count in temporal_counts.items() if count > 1}
            temporal_by_fact = {}
            if "v552_structural_fact_id" in temporal.columns:
                temporal_by_fact = {
                    str(row.get("v552_structural_fact_id")): row
                    for row in temporal.to_dict("records")
                    if str(row.get("v552_structural_fact_id")) not in duplicate_temporal_ids
                }
            for row in eligible_facts.to_dict("records"):
                temporal_row = temporal_by_fact.get(str(row.get("v552_structural_fact_id")))
                if not temporal_row:
                    continue
                for field in V552_PRESSURE_CONTRACT_CHAIN_FIELDS:
                    if _canon(temporal_row.get(field)) != _canon(row.get(field)):
                        issues.append(f"fact_temporal_pressure_contract_mismatch={field}")
                        break
                if any(item.startswith("fact_temporal_pressure_contract_mismatch=") for item in issues):
                    break
        if "allowed_for_v553_temporal_field" in temporal.columns and temporal["allowed_for_v553_temporal_field"].fillna(False).astype(bool).any():
            issues.append("direct_v553_authorization_present")

    if not readiness.empty:
        row = readiness.iloc[0]
        emitted_artifact_count = sum(
            1 for name, frame in outputs.items()
            if isinstance(frame, pd.DataFrame) and not name.startswith("_") and name != "v552_readiness_report"
        )
        comparability_count = int(temporal.get("temporal_key_candidate_status", pd.Series(dtype=str)).eq("CANDIDATE_FOR_V552J_PRESSURE_LINKAGE").sum()) if not temporal.empty else 0
        if int(row.get("output_artifact_count", -1)) != emitted_artifact_count:
            issues.append("readiness_output_count_mismatch")
        if int(row.get("handoff_index_rows", -1)) != len(handoff):
            issues.append("readiness_handoff_row_mismatch")
        if int(row.get("comparability_key_count", -1)) != comparability_count:
            issues.append("readiness_comparability_key_mismatch")
    return sorted(set(issues))


def build_v552_structural_outputs(atoms: pd.DataFrame, conditional_determinicity: pd.DataFrame | None = None, *, run_id: str = "v552_run") -> dict[str, pd.DataFrame]:
    atoms = atoms.copy()
    input_contract = validate_v552_v551_input_contract(atoms)
    component_index = build_v552_pressure_component_index(atoms, run_id=run_id) if input_contract["status"] == "PASS" else _empty(V552_PRESSURE_COMPONENT_INDEX_SCHEMA)
    representation_audit = build_v552_intensity_representation_resolution_audit(component_index)
    observation_index = build_v552_pressure_observation_index(atoms, component_index, run_id=run_id) if input_contract["status"] == "PASS" else _empty(V552_PRESSURE_OBSERVATION_INDEX_SCHEMA)
    observation_audit = build_v552_pressure_observation_audit(observation_index)
    relation_axis = build_relation_axis_pressure_from_observations(observation_index, run_id=run_id)
    target_entity = build_target_entity_pressure_from_observations(observation_index, run_id=run_id)
    driver_facet = build_driver_facet_pressure_from_observations(observation_index, run_id=run_id)
    country_wave = build_country_wave_pressure_profile_from_observations(observation_index, run_id=run_id)
    structural_channel = build_structural_channel_index_from_observations(observation_index, run_id=run_id)
    position_profile = build_position_conditioning_profile_from_observations(observation_index, run_id=run_id)
    contradiction = build_contradiction_tensor_from_observations(observation_index, run_id=run_id)
    outputs = {
        "v552_pressure_component_index": component_index,
        "v552_intensity_representation_resolution_audit": representation_audit,
        "v552_pressure_observation_index": observation_index,
        "v552_pressure_observation_audit": observation_audit,
        "relation_axis_pressure": relation_axis,
        "target_entity_pressure": target_entity,
        "driver_facet_pressure": driver_facet,
        "country_wave_pressure_profile": country_wave,
        "structural_channel_index": structural_channel,
        "position_conditioning_profile": position_profile,
        "contradiction_tensor": contradiction,
        "contradiction_surface": _empty(V552_CONTRADICTION_SURFACE_SCHEMA),
        "question_semantic_hierarchy": _empty(V552_QUESTION_SEMANTIC_HIERARCHY_SCHEMA),
        "facet_semantic_profile": _empty(V552_FACET_SEMANTIC_PROFILE_SCHEMA),
        "driver_semantic_profile": _empty(V552_DRIVER_SEMANTIC_PROFILE_SCHEMA),
        "stratum_semantic_profile": _empty(V552_STRATUM_SEMANTIC_PROFILE_SCHEMA),
        "horizon_semantic_profile": _empty(V552_HORIZON_SEMANTIC_PROFILE_SCHEMA),
        "aggregate_projection_surface": _empty(V552_AGGREGATE_PROJECTION_SURFACE_SCHEMA),
        "horizon_constraint_index": _empty(V552_HORIZON_CONSTRAINT_INDEX_SCHEMA),
        "parent_position_prior": _empty(V552_PARENT_POSITION_PRIOR_SCHEMA),
        "parent_attitude_prior": _empty(V552_PARENT_ATTITUDE_PRIOR_SCHEMA),
        "parent_behavior_tendency_prior": _empty(V552_PARENT_BEHAVIOR_TENDENCY_PRIOR_SCHEMA),
        "parent_contradiction_prior": _empty(V552_PARENT_CONTRADICTION_PRIOR_SCHEMA),
        "parent_prior_manifest": _empty(V552_PARENT_PRIOR_MANIFEST_SCHEMA),
        "parent_position_prior_manifest": _empty(V552_PARENT_PRIOR_MANIFEST_SCHEMA),
        "v552_directionality_coverage_audit": _empty(V552_DIRECTIONALITY_COVERAGE_AUDIT_SCHEMA),
        "v552_directionality_gap_surface": _empty(V552_DIRECTIONALITY_GAP_SURFACE_SCHEMA),
        "v552_status_pressure_review_surface": _empty(V552_STATUS_PRESSURE_REVIEW_SCHEMA),
        "v552_artifact_authority_index": _empty(V552_ARTIFACT_AUTHORITY_INDEX_SCHEMA),
        "v552_known_absence_register": _empty(V552_KNOWN_ABSENCE_REGISTER_SCHEMA),
    }
    fact_index = _fact_index(observation_index, outputs, contradiction, run_id)
    temporal_key = _temporal_key_index(fact_index, run_id)
    outputs["v552_structural_fact_index"] = fact_index
    outputs["v552_temporal_key_source_index"] = temporal_key
    outputs["v552_to_v552j_handoff_index"] = _handoff(outputs, run_id)
    outputs["v552_to_v552j_pressure_observation_handoff_index"] = _pressure_observation_handoff(observation_index, component_index, run_id)
    outputs["_input_atoms"] = atoms
    observed_count = int(observation_index["pressure_score_status"].isin(["OBSERVED_NONZERO", "OBSERVED_ZERO"]).sum()) if not observation_index.empty else 0
    status = "READY_V552_STRUCTURAL_PRESSURE_CONTRACT" if input_contract["status"] == "PASS" and len(atoms) > 0 and observed_count > 0 else ("BLOCKED_V552_NO_RELATION_ATOMS" if len(atoms) == 0 else input_contract["status"] if input_contract["status"] != "PASS" else "PARTIAL_READY_V552_STRUCTURE_ONLY_NO_PRESSURE")
    output_artifact_count = sum(1 for name, frame in outputs.items() if isinstance(frame, pd.DataFrame) and not name.startswith("_"))
    comparability_key_count = int(temporal_key.get("temporal_key_candidate_status", pd.Series(dtype=str)).eq("CANDIDATE_FOR_V552J_PRESSURE_LINKAGE").sum()) if not temporal_key.empty else 0
    temporal_anchor_hint_count = int(outputs["v552_to_v552j_handoff_index"].get("temporal_anchor_hint", pd.Series(dtype=str)).eq("candidate_after_v552j").sum()) if not outputs["v552_to_v552j_handoff_index"].empty else 0
    category_empirical_object_count = int(atoms.get("empirical_object_id", pd.Series(dtype=str)).nunique()) if not atoms.empty else 0
    unique_empirical_distribution_count = int(atoms.get("empirical_distribution_id", pd.Series(dtype=str)).nunique()) if not atoms.empty else 0
    readiness = pd.DataFrame([{
        "run_id": run_id, "status": status, "input_contract_status": input_contract["status"],
        "ready_for_v552j_structural_inspection": input_contract["status"] == "PASS" and len(atoms) > 0,
        "ready_for_v552j_pressure_linkage": observed_count > 0, "ready_for_v553_direct": False,
        "input_atom_rows": int(len(atoms)), "unique_empirical_object_count": category_empirical_object_count,
        "category_empirical_object_count": category_empirical_object_count,
        "unique_empirical_distribution_count": unique_empirical_distribution_count,
        "unique_empirical_object_grain": "response_category",
        "pressure_observation_candidate_count": int(len(observation_index)), "observed_pressure_count": int((observation_index["pressure_score_status"].eq("OBSERVED_NONZERO")).sum()) if not observation_index.empty else 0,
        "observed_zero_pressure_count": int((observation_index["pressure_score_status"].eq("OBSERVED_ZERO")).sum()) if not observation_index.empty else 0,
        "noncomputable_pressure_count": int((observation_index["pressure_score_status"].eq("NOT_COMPUTABLE")).sum()) if not observation_index.empty else 0,
        "review_required_pressure_count": int((observation_index["pressure_score_status"].eq("REVIEW_REQUIRED")).sum()) if not observation_index.empty else 0,
        "pressure_linkage_eligible_count": int(observation_index.get("v552j_pressure_linkage_eligible", pd.Series(dtype=bool)).fillna(False).astype(bool).sum()) if not observation_index.empty else 0,
        "exact_pressure_rollup_count": int(relation_axis.get("rollup_identity_status", pd.Series(dtype=str)).eq("EXACT_IDENTITY_ROLLUP").sum()) if not relation_axis.empty else 0,
        "heterogeneous_pressure_summary_count": int(relation_axis.get("rollup_identity_status", pd.Series(dtype=str)).str.startswith("HETEROGENEOUS").sum()) if not relation_axis.empty else 0,
        "contradiction_row_count": int(len(contradiction)), "structural_channel_count": int(len(structural_channel)),
        "invalid_output_contract_rows": 0, "allowed_for_v553_temporal_field_count": 0, "schema_version": V552_SCHEMA_VERSION,
        "v552_compile_status": status, "v552_structural_readiness": "ready" if observed_count > 0 else "partial",
        "v552_directionality_readiness": "not_applicable", "v552_horizon_readiness": "context_only",
        "v552_contradiction_readiness": "ready_empty" if contradiction.empty else "ready",
        "v552_parent_prior_readiness": "context_scaffold_only", "v552_v552j_handoff_readiness": "ready",
        "v552_v553_comparability_readiness": "not_authorized_at_v552", "v552_runtime_readiness": "not_runtime_authorized",
        "ready_for_v552j_inspection": input_contract["status"] == "PASS", "ready_for_v553_after_v552j": False,
        "input_atom_count": int(len(atoms)), "output_artifact_count": output_artifact_count,
        "artifact_authority_rows": int(len(outputs["v552_artifact_authority_index"])),
        "known_absence_rows": int(len(outputs["v552_known_absence_register"])),
        "handoff_index_rows": int(len(outputs.get("v552_to_v552j_pressure_observation_handoff_index", pd.DataFrame()))),
        "comparability_key_count": comparability_key_count,
        "temporal_anchor_hint_count": temporal_anchor_hint_count, "final_status": status, "created_at": _utc_now(),
        "compiler_version": V552_HANDOFF_SCHEMA_VERSION,
    }])
    outputs["v552_readiness_report"] = readiness
    output_contract_issues = validate_v552_v2_1_output_contract(outputs)
    if output_contract_issues:
        status = "BLOCKED_V552_OUTPUT_CONTRACT_INVALID"
        outputs["v552_readiness_report"].loc[:, "status"] = status
        outputs["v552_readiness_report"].loc[:, "v552_compile_status"] = status
        outputs["v552_readiness_report"].loc[:, "final_status"] = status
        outputs["v552_readiness_report"].loc[:, "invalid_output_contract_rows"] = len(output_contract_issues)
        outputs["_v552_output_contract_issues"] = pd.DataFrame({"issue": output_contract_issues})
    outputs["_v552_input_contract_report"] = pd.DataFrame([input_contract])
    return outputs
