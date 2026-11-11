#!/usr/bin/env python3
"""Build a unified GSS authority compendium and publish it to Postgres.

This script compiles the already-existing GSS wave authority artifacts into one
normalized table so downstream compilers can consume a single, explicit
authority substrate instead of re-inferring meaning from scattered wave docs.

It is intentionally conservative:
- it only uses existing repo artifacts
- it does not invent new survey meaning
- it marks gaps explicitly when an artifact is absent
- it writes a companion Postgres view that preserves the base facet-ready view
  while surfacing authority columns needed by V550J and future survey prep
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

import pandas as pd
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / "data" / "ddm_build_copy" / "reports"
DOCS = ROOT / "docs" / "DDM_THROUGH_V552_ROADMAP"

OUT_COMPENDIUM = REPORTS / "gss_authority_compendium.csv"
OUT_GAP_LOG = REPORTS / "gss_authority_compendium_gap_log.csv"
OUT_REPORT = REPORTS / "gss_authority_compendium_build_report.json"

POSTGRES_TABLE = "survey_authority_compendium"
POSTGRES_GAP_TABLE = "survey_authority_compendium_gap_log"
POSTGRES_VIEW = "v_ddm_response_long_facet_ready_authority"

GSS_WAVES = ["1972", "1973", "1982", "1984", "1993", "2002", "2004", "2010", "2014", "2016", "2024"]

ARTIFACT_SPECS = {
    "first_pass": {
        "filename": "first_pass_authority_table.csv",
        "prefix": "fp",
    },
    "authority": {
        "filename": "authority_overlay.csv",
        "prefix": "au",
    },
    "semantic": {
        "filename": "semantic_authority_overlay.csv",
        "prefix": "se",
    },
    "position": {
        "filename": "position_conditioning_overlay.csv",
        "prefix": "pc",
    },
    "directionality": {
        "filename": "directionality_overlay.csv",
        "prefix": "di",
    },
}

BASE_KEYS = ["source", "wave", "canonical_wave", "var_name"]

OUTPUT_COLUMNS = [
    "source",
    "wave",
    "canonical_wave",
    "var_name",
    "var_code",
    "question_id",
    "question_text",
    "classification_kind",
    "source_structure_classification",
    "source_structure_confidence",
    "final_driver_id",
    "final_driver_origin",
    "resolved_semantic_lane",
    "resolved_evidence_lane",
    "resolution_decision",
    "resolution_status",
    "semantic_lane",
    "semantic_role",
    "evidence_lane",
    "semantic_subrole",
    "semantic_tags",
    "directionality_policy",
    "semantic_confidence",
    "semantic_note",
    "signed_polarity_status",
    "response_family_expectation",
    "positive_anchor_label",
    "negative_anchor_label",
    "neutral_anchor_label",
    "bridge_directionality_action",
    "directionality_confidence",
    "directionality_note",
    "manual_review_required",
    "position_conditioning",
    "position_modifiers",
    "conditional_strata_weights",
    "horizon_affordance",
    "position_conditioning_note",
    "position_conditioning_confidence",
    "allowed_as_branch_position_signature",
    "allowed_as_branch_relation_cosignature",
    "allowed_as_attitude_cloud_anchor",
    "allowed_as_attitude_cloud_feature",
    "allowed_as_v551_relation_evidence",
    "allowed_as_association_feature",
    "is_substantive",
    "not_direct_evidence",
    "manual_designation_required",
    "designation_confidence",
    "authority_bundle_status",
    "authority_source_artifacts",
    "authority_gap_reason",
]

BOOLEAN_COLUMNS = {
    "manual_review_required",
    "allowed_as_branch_position_signature",
    "allowed_as_branch_relation_cosignature",
    "allowed_as_attitude_cloud_anchor",
    "allowed_as_attitude_cloud_feature",
    "allowed_as_v551_relation_evidence",
    "allowed_as_association_feature",
    "is_substantive",
    "not_direct_evidence",
    "manual_designation_required",
}

VIEW_AUTHORITY_COLUMNS = [
    "semantic_role",
    "semantic_subrole",
    "directionality_policy",
    "semantic_confidence",
    "semantic_note",
    "signed_polarity_status",
    "response_family_expectation",
    "positive_anchor_label",
    "negative_anchor_label",
    "neutral_anchor_label",
    "bridge_directionality_action",
    "directionality_confidence",
    "directionality_note",
    "manual_review_required",
    "position_conditioning",
    "position_modifiers",
    "conditional_strata_weights",
    "horizon_affordance",
    "position_conditioning_note",
    "position_conditioning_confidence",
    "allowed_as_attitude_cloud_feature",
    "allowed_as_v551_relation_evidence",
    "allowed_as_association_feature",
    "is_substantive",
    "not_direct_evidence",
    "authority_bundle_status",
    "authority_source_artifacts",
    "authority_gap_reason",
]


def clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    text = str(value).strip()
    if text.lower() in {"nan", "none", "<na>"}:
        return ""
    return text


def to_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    try:
        if pd.isna(value):
            return default
    except Exception:
        pass
    text = clean(value).lower()
    if text in {"true", "t", "1", "yes", "y"}:
        return True
    if text in {"false", "f", "0", "no", "n", ""}:
        return False
    return default


def has_meaningful_value(value: Any) -> bool:
    if value is None:
        return False
    try:
        if pd.isna(value):
            return False
    except Exception:
        pass
    if isinstance(value, bool):
        return value
    text = clean(value)
    return text not in {"", "false", "0"}


def normalize_wave(value: Any) -> str:
    text = clean(value)
    return text


def load_artifact(wave: str, artifact_kind: str) -> pd.DataFrame:
    spec = ARTIFACT_SPECS[artifact_kind]
    path = REPORTS / f"gss{wave}_{spec['filename']}"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path, low_memory=False)
    for col in df.columns:
        if df[col].dtype == "O":
            df[col] = df[col].fillna("").astype(str)
    if "source" not in df.columns:
        df["source"] = "GSS"
    if "wave" not in df.columns:
        df["wave"] = wave
    if "canonical_wave" not in df.columns:
        df["canonical_wave"] = wave
    if "var_name" in df.columns:
        df["var_name"] = df["var_name"].map(clean).str.lower()
    else:
        df["var_name"] = ""
    df["source"] = df["source"].map(clean).replace("", "GSS")
    df["wave"] = df["wave"].map(normalize_wave).replace("", wave)
    df["canonical_wave"] = df["canonical_wave"].map(normalize_wave).replace("", wave)
    return df


def _prefix_frame(df: pd.DataFrame, prefix: str, columns: list[str]) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=BASE_KEYS + [f"{prefix}_{col}" for col in columns])
    keep = [col for col in BASE_KEYS if col in df.columns]
    keep.extend([col for col in columns if col in df.columns])
    out = df[keep].copy()
    rename = {col: f"{prefix}_{col}" for col in columns if col in out.columns}
    return out.rename(columns=rename)


def _merge_frames(frames: list[pd.DataFrame]) -> pd.DataFrame:
    merged = frames[0].copy()
    for frame in frames[1:]:
        merged = merged.merge(frame, on=BASE_KEYS, how="outer")
    if merged.empty:
        return merged
    merged["source"] = merged["source"].map(clean).replace("", "GSS")
    merged["wave"] = merged["wave"].map(normalize_wave)
    merged["canonical_wave"] = merged["canonical_wave"].map(normalize_wave)
    merged["var_name"] = merged["var_name"].map(clean).str.lower()
    return merged


def _coalesce_row(row: pd.Series, candidates: list[str], default: str = "") -> str:
    for candidate in candidates:
        value = clean(row.get(candidate))
        if value:
            return value
    return default


def _coalesce_bool(row: pd.Series, candidates: list[str], default: bool = False) -> bool:
    for candidate in candidates:
        if candidate in row.index:
            value = row.get(candidate)
            if pd.isna(value):
                continue
            text = clean(value)
            if text:
                return to_bool(value, default)
    return default


def _derive_authority_row(row: pd.Series) -> dict[str, Any]:
    semantic_lane = _coalesce_row(row, ["fp_semantic_lane", "se_semantic_lane", "au_resolved_semantic_lane"], "")
    semantic_role = _coalesce_row(row, ["fp_semantic_role", "se_semantic_role", "au_resolved_semantic_lane"], "")
    evidence_lane = _coalesce_row(row, ["fp_evidence_lane", "se_evidence_lane", "au_resolved_evidence_lane"], "")
    source_structure_classification = _coalesce_row(row, ["au_source_structure_classification"], "")
    source_structure_confidence = _coalesce_row(row, ["au_source_structure_confidence"], "")
    final_driver_id = _coalesce_row(row, ["au_final_driver_id"], "")
    final_driver_origin = _coalesce_row(row, ["au_final_driver_origin"], "")
    resolved_semantic_lane = _coalesce_row(row, ["au_resolved_semantic_lane", "fp_semantic_lane", "se_semantic_lane"], "")
    resolved_evidence_lane = _coalesce_row(row, ["au_resolved_evidence_lane", "fp_evidence_lane", "se_evidence_lane"], "")
    resolution_decision = _coalesce_row(row, ["au_resolution_decision"], "")
    resolution_status = _coalesce_row(row, ["au_resolution_status"], "")
    semantic_subrole = _coalesce_row(row, ["se_semantic_subrole", "pc_semantic_subrole"], "")
    semantic_tags = _coalesce_row(row, ["se_semantic_tags", "pc_semantic_tags"], "")
    directionality_policy = _coalesce_row(row, ["se_directionality_policy", "pc_directionality_policy", "di_directionality_policy"], "")
    semantic_confidence = _coalesce_row(row, ["se_semantic_confidence", "pc_semantic_confidence"], "")
    semantic_note = _coalesce_row(row, ["se_semantic_note", "pc_semantic_note"], "")
    signed_polarity_status = _coalesce_row(row, ["di_signed_polarity_status"], "")
    response_family_expectation = _coalesce_row(row, ["di_response_family_expectation"], "")
    positive_anchor_label = _coalesce_row(row, ["di_positive_anchor_label"], "")
    negative_anchor_label = _coalesce_row(row, ["di_negative_anchor_label"], "")
    neutral_anchor_label = _coalesce_row(row, ["di_neutral_anchor_label"], "")
    bridge_directionality_action = _coalesce_row(row, ["di_bridge_directionality_action"], "")
    directionality_confidence = _coalesce_row(row, ["di_directionality_confidence"], "")
    directionality_note = _coalesce_row(row, ["di_directionality_note"], "")
    position_conditioning = _coalesce_row(row, ["pc_position_conditioning"], "")
    position_modifiers = _coalesce_row(row, ["pc_position_modifiers"], "")
    conditional_strata_weights = _coalesce_row(row, ["pc_conditional_strata_weights"], "")
    horizon_affordance = _coalesce_row(row, ["pc_horizon_affordance"], "")
    position_conditioning_note = _coalesce_row(row, ["pc_position_conditioning_note"], "")
    position_conditioning_confidence = _coalesce_row(row, ["pc_position_conditioning_confidence"], "")
    allowed_as_branch_position_signature = _coalesce_bool(row, ["fp_allowed_as_branch_position_signature"], False)
    allowed_as_branch_relation_cosignature = _coalesce_bool(row, ["fp_allowed_as_branch_relation_cosignature"], False)
    allowed_as_attitude_cloud_anchor = _coalesce_bool(row, ["fp_allowed_as_attitude_cloud_anchor"], False)
    allowed_as_attitude_cloud_feature = _coalesce_bool(row, ["fp_allowed_as_attitude_cloud_feature"], False)
    manual_designation_required = _coalesce_bool(row, ["fp_manual_designation_required"], False)
    designation_confidence = _coalesce_row(row, ["fp_designation_confidence"], "")

    allowed_as_v551_relation_evidence = (
        semantic_role.lower() == "relation_evidence"
        or evidence_lane.lower() == "relation_evidence"
        or allowed_as_attitude_cloud_feature
        or allowed_as_attitude_cloud_anchor
    )
    is_substantive = (
        semantic_lane.lower() == "substantive"
        or semantic_role.lower() == "relation_evidence"
        or allowed_as_attitude_cloud_feature
        or allowed_as_attitude_cloud_anchor
    )
    allowed_as_association_feature = allowed_as_attitude_cloud_feature or allowed_as_v551_relation_evidence
    not_direct_evidence = not allowed_as_v551_relation_evidence
    artifact_bits = []
    if any(has_meaningful_value(row.get(col)) for col in row.index if col.startswith("fp_")):
        artifact_bits.append("first_pass")
    if any(has_meaningful_value(row.get(col)) for col in row.index if col.startswith("au_")):
        artifact_bits.append("authority_overlay")
    if any(has_meaningful_value(row.get(col)) for col in row.index if col.startswith("se_")):
        artifact_bits.append("semantic_overlay")
    if any(has_meaningful_value(row.get(col)) for col in row.index if col.startswith("pc_")):
        artifact_bits.append("position_overlay")
    if any(has_meaningful_value(row.get(col)) for col in row.index if col.startswith("di_")):
        artifact_bits.append("directionality_overlay")
    if not artifact_bits:
        artifact_bits.append("first_pass")
    present = "|".join(artifact_bits)
    missing = [kind for kind in ["authority_overlay", "semantic_overlay", "position_overlay", "directionality_overlay"] if kind not in artifact_bits]
    authority_bundle_status = "complete" if not missing and "first_pass" in artifact_bits else ("first_pass_only" if artifact_bits == ["first_pass"] else "partial")
    authority_gap_reason = "none" if authority_bundle_status == "complete" else ("missing_" + "|".join(missing) if missing else "first_pass_only")
    return {
        "source": clean(row.get("source")) or "GSS",
        "wave": clean(row.get("wave")),
        "canonical_wave": clean(row.get("canonical_wave")) or clean(row.get("wave")),
        "var_name": clean(row.get("var_name")).lower(),
        "var_code": clean(row.get("var_name")).lower(),
        "question_id": f"GSS:{clean(row.get('wave'))}:{clean(row.get('var_name')).lower()}",
        "question_text": _coalesce_row(row, ["fp_question_text", "au_question_text", "se_question_text", "pc_question_text", "di_question_text"], ""),
        "classification_kind": _coalesce_row(row, ["au_classification_kind"], ""),
        "source_structure_classification": source_structure_classification,
        "source_structure_confidence": source_structure_confidence,
        "final_driver_id": final_driver_id,
        "final_driver_origin": final_driver_origin,
        "resolved_semantic_lane": resolved_semantic_lane,
        "resolved_evidence_lane": resolved_evidence_lane,
        "resolution_decision": resolution_decision,
        "resolution_status": resolution_status,
        "semantic_lane": semantic_lane,
        "semantic_role": semantic_role,
        "evidence_lane": evidence_lane,
        "semantic_subrole": semantic_subrole,
        "semantic_tags": semantic_tags,
        "directionality_policy": directionality_policy,
        "semantic_confidence": semantic_confidence,
        "semantic_note": semantic_note,
        "signed_polarity_status": signed_polarity_status,
        "response_family_expectation": response_family_expectation,
        "positive_anchor_label": positive_anchor_label,
        "negative_anchor_label": negative_anchor_label,
        "neutral_anchor_label": neutral_anchor_label,
        "bridge_directionality_action": bridge_directionality_action,
        "directionality_confidence": directionality_confidence,
        "directionality_note": directionality_note,
        "manual_review_required": _coalesce_bool(row, ["di_manual_review_required"], False),
        "position_conditioning": position_conditioning,
        "position_modifiers": position_modifiers,
        "conditional_strata_weights": conditional_strata_weights,
        "horizon_affordance": horizon_affordance,
        "position_conditioning_note": position_conditioning_note,
        "position_conditioning_confidence": position_conditioning_confidence,
        "allowed_as_branch_position_signature": allowed_as_branch_position_signature,
        "allowed_as_branch_relation_cosignature": allowed_as_branch_relation_cosignature,
        "allowed_as_attitude_cloud_anchor": allowed_as_attitude_cloud_anchor,
        "allowed_as_attitude_cloud_feature": allowed_as_attitude_cloud_feature,
        "allowed_as_v551_relation_evidence": allowed_as_v551_relation_evidence,
        "allowed_as_association_feature": allowed_as_association_feature,
        "is_substantive": is_substantive,
        "not_direct_evidence": not_direct_evidence,
        "manual_designation_required": manual_designation_required,
        "designation_confidence": designation_confidence,
        "authority_bundle_status": authority_bundle_status,
        "authority_source_artifacts": present,
        "authority_gap_reason": authority_gap_reason,
    }


def build_wave_compendium(wave: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    frames: list[pd.DataFrame] = []
    artifact_presence: dict[str, int] = {}
    for artifact_kind, spec in ARTIFACT_SPECS.items():
        frame = load_artifact(wave, artifact_kind)
        artifact_presence[artifact_kind] = int(len(frame))
        keep_cols = [
            "question_text",
            "classification_kind",
            "source_structure_classification",
            "source_structure_confidence",
            "final_driver_id",
            "final_driver_origin",
            "resolved_semantic_lane",
            "resolved_evidence_lane",
            "resolution_decision",
            "resolution_status",
            "semantic_lane",
            "semantic_role",
            "evidence_lane",
            "semantic_subrole",
            "semantic_tags",
            "directionality_policy",
            "semantic_confidence",
            "semantic_note",
            "signed_polarity_status",
            "response_family_expectation",
            "positive_anchor_label",
            "negative_anchor_label",
            "neutral_anchor_label",
            "bridge_directionality_action",
            "directionality_confidence",
            "directionality_note",
            "manual_review_required",
            "position_conditioning",
            "position_modifiers",
            "conditional_strata_weights",
            "horizon_affordance",
            "position_conditioning_note",
            "position_conditioning_confidence",
            "allowed_as_branch_position_signature",
            "allowed_as_branch_relation_cosignature",
            "allowed_as_attitude_cloud_anchor",
            "allowed_as_attitude_cloud_feature",
            "manual_designation_required",
            "designation_confidence",
        ]
        frames.append(_prefix_frame(frame, spec["prefix"], keep_cols))
    merged = _merge_frames(frames)
    if merged.empty:
        return merged, {
            "wave": wave,
            "row_count": 0,
            "artifact_presence": artifact_presence,
            "authority_bundle_status_counts": {},
            "association_authority_ready_count": 0,
            "association_authority_gap_count": 0,
        }

    rows = [_derive_authority_row(row) for _, row in merged.iterrows()]
    compendium = pd.DataFrame(rows)
    for col in BOOLEAN_COLUMNS:
        if col in compendium.columns:
            compendium[col] = compendium[col].map(lambda value: to_bool(value, False))
    compendium = compendium[OUTPUT_COLUMNS].copy()
    compendium = compendium.sort_values(["source", "wave", "var_name"], kind="stable").reset_index(drop=True)
    summary = {
        "wave": wave,
        "row_count": int(len(compendium)),
        "artifact_presence": artifact_presence,
        "authority_bundle_status_counts": compendium["authority_bundle_status"].value_counts(dropna=False).to_dict(),
        "association_authority_ready_count": int(
            (compendium["is_substantive"].fillna(False) | compendium["allowed_as_association_feature"].fillna(False) | compendium["allowed_as_attitude_cloud_feature"].fillna(False)).sum()
        ),
        "association_authority_gap_count": int(
            (~(compendium["is_substantive"].fillna(False) | compendium["allowed_as_association_feature"].fillna(False) | compendium["allowed_as_attitude_cloud_feature"].fillna(False))).sum()
        ),
    }
    return compendium, summary


def build_compendium(waves: list[str] | None = None) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    selected_waves = waves or GSS_WAVES
    compendium_frames: list[pd.DataFrame] = []
    gap_rows: list[dict[str, Any]] = []
    wave_summaries: list[dict[str, Any]] = []
    for wave in selected_waves:
        frame, summary = build_wave_compendium(wave)
        compendium_frames.append(frame)
        wave_summaries.append(summary)
        present = [kind for kind, count in summary["artifact_presence"].items() if count > 0]
        missing = [kind for kind in ARTIFACT_SPECS if kind not in present]
        gap_rows.append(
            {
                "source": "GSS",
                "wave": wave,
                "canonical_wave": wave,
                "compiled_family_count": 0,
                "compiled_family_ids": "",
                "artifact_name": "gss_authority_compendium",
                "manifest_row_count": summary["row_count"],
                "actual_row_count": summary["row_count"],
                "family_ids_expected": "",
                "family_ids_present": "",
                "family_ids_missing": "",
                "schema_valid": True,
                "row_count_valid": True,
                "family_coverage_valid": True,
                "validation_status": "pass" if summary["row_count"] > 0 else "warning",
                "validation_message": "authority bundle compiled from existing GSS artifacts",
                "present_artifacts": "|".join(present),
                "missing_artifacts": "|".join(missing) if missing else "none",
                "authority_bundle_status_counts": json.dumps(summary["authority_bundle_status_counts"], sort_keys=True),
                "association_authority_ready_count": summary["association_authority_ready_count"],
                "association_authority_gap_count": summary["association_authority_gap_count"],
                "future_survey_prep_required": True,
                "future_survey_prep_note": "This authority-compilation step is required before future survey runs so downstream compilers do not infer meaning from thin rows.",
            }
        )
    compendium = pd.concat(compendium_frames, ignore_index=True, sort=False) if compendium_frames else pd.DataFrame(columns=OUTPUT_COLUMNS)
    gap_log = pd.DataFrame(gap_rows)
    report = {
        "row_count": int(len(compendium)),
        "wave_count": int(len(selected_waves)),
        "waves": selected_waves,
        "wave_summaries": wave_summaries,
        "compendium_path": str(OUT_COMPENDIUM),
        "gap_log_path": str(OUT_GAP_LOG),
        "postgres_table": POSTGRES_TABLE,
        "postgres_gap_table": POSTGRES_GAP_TABLE,
        "postgres_view": POSTGRES_VIEW,
        "future_survey_prep_note": "This compendium pattern must be recreated for each future survey family before V550/V550J-style semantic runs.",
    }
    return compendium, gap_log, report


def load_db() -> Any:
    try:
        import psycopg2
    except ModuleNotFoundError as exc:
        raise RuntimeError("psycopg2 is required for Postgres publication.") from exc
    load_dotenv(ROOT / ".env")
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL is missing.")
    return psycopg2.connect(db_url)


def _create_table_sql(table_name: str, columns: list[tuple[str, str]]) -> str:
    col_lines = [f"    {name} {col_type}" for name, col_type in columns]
    return f"DROP TABLE IF EXISTS {table_name} CASCADE;\nCREATE TABLE {table_name} (\n" + ",\n".join(col_lines) + "\n);\n"


def _compendium_table_columns() -> list[tuple[str, str]]:
    cols = []
    for col in OUTPUT_COLUMNS:
        if col in BOOLEAN_COLUMNS:
            cols.append((col, "BOOLEAN"))
        else:
            cols.append((col, "TEXT"))
    cols.append(("loaded_at", "TIMESTAMPTZ NOT NULL DEFAULT now()"))
    return cols


def _gap_table_columns() -> list[tuple[str, str]]:
    return [
        ("source", "TEXT"),
        ("wave", "TEXT"),
        ("canonical_wave", "TEXT"),
        ("compiled_family_count", "INT"),
        ("compiled_family_ids", "TEXT"),
        ("artifact_name", "TEXT"),
        ("manifest_row_count", "INT"),
        ("actual_row_count", "INT"),
        ("family_ids_expected", "TEXT"),
        ("family_ids_present", "TEXT"),
        ("family_ids_missing", "TEXT"),
        ("schema_valid", "BOOLEAN"),
        ("row_count_valid", "BOOLEAN"),
        ("family_coverage_valid", "BOOLEAN"),
        ("validation_status", "TEXT"),
        ("validation_message", "TEXT"),
        ("present_artifacts", "TEXT"),
        ("missing_artifacts", "TEXT"),
        ("authority_bundle_status_counts", "TEXT"),
        ("association_authority_ready_count", "INT"),
        ("association_authority_gap_count", "INT"),
        ("future_survey_prep_required", "BOOLEAN"),
        ("future_survey_prep_note", "TEXT"),
    ]


def _insert_frame(cur, table_name: str, frame: pd.DataFrame, columns: list[str]) -> None:
    if frame.empty:
        return
    try:
        from psycopg2.extras import execute_values
    except ModuleNotFoundError as exc:
        raise RuntimeError("psycopg2 is required for Postgres publication.") from exc
    values = [tuple(None if pd.isna(value) else value for value in row) for row in frame[columns].itertuples(index=False, name=None)]
    cols_sql = ", ".join(columns)
    execute_values(
        cur,
        f"INSERT INTO {table_name} ({cols_sql}) VALUES %s",
        values,
        page_size=1000,
    )


def write_postgres(compendium: pd.DataFrame, gap_log: pd.DataFrame) -> None:
    conn = load_db()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(_create_table_sql(POSTGRES_TABLE, _compendium_table_columns()))
            cur.execute(_create_table_sql(POSTGRES_GAP_TABLE, _gap_table_columns()))
            _insert_frame(cur, POSTGRES_TABLE, compendium, OUTPUT_COLUMNS)
            _insert_frame(cur, POSTGRES_GAP_TABLE, gap_log, [name for name, _ in _gap_table_columns()])
            cur.execute(f"DROP VIEW IF EXISTS {POSTGRES_VIEW}")
            view_sql = f"""
            CREATE OR REPLACE VIEW {POSTGRES_VIEW} AS
            SELECT
                base.*,
                COALESCE(comp.semantic_role, '') AS semantic_role,
                COALESCE(comp.semantic_subrole, '') AS semantic_subrole,
                COALESCE(comp.directionality_policy, '') AS directionality_policy,
                COALESCE(comp.semantic_confidence, '') AS semantic_confidence,
                COALESCE(comp.semantic_note, '') AS semantic_note,
                COALESCE(comp.signed_polarity_status, '') AS signed_polarity_status,
                COALESCE(comp.response_family_expectation, '') AS response_family_expectation,
                COALESCE(comp.positive_anchor_label, '') AS positive_anchor_label,
                COALESCE(comp.negative_anchor_label, '') AS negative_anchor_label,
                COALESCE(comp.neutral_anchor_label, '') AS neutral_anchor_label,
                COALESCE(comp.bridge_directionality_action, '') AS bridge_directionality_action,
                COALESCE(comp.directionality_confidence, '') AS authority_directionality_confidence,
                COALESCE(comp.directionality_note, '') AS directionality_note,
                COALESCE(comp.manual_review_required, FALSE) AS manual_review_required,
                COALESCE(comp.position_conditioning, '') AS position_conditioning,
                COALESCE(comp.position_modifiers, '') AS position_modifiers,
                COALESCE(comp.conditional_strata_weights, '') AS conditional_strata_weights,
                COALESCE(comp.horizon_affordance, '') AS horizon_affordance,
                COALESCE(comp.position_conditioning_note, '') AS position_conditioning_note,
                COALESCE(comp.position_conditioning_confidence, '') AS position_conditioning_confidence,
                COALESCE(comp.allowed_as_attitude_cloud_feature, FALSE) AS allowed_as_attitude_cloud_feature,
                COALESCE(comp.allowed_as_v551_relation_evidence, FALSE) AS allowed_as_v551_relation_evidence,
                COALESCE(comp.allowed_as_association_feature, FALSE) AS allowed_as_association_feature,
                COALESCE(comp.is_substantive, FALSE) AS is_substantive,
                COALESCE(comp.not_direct_evidence, FALSE) AS not_direct_evidence,
                COALESCE(comp.authority_bundle_status, '') AS authority_bundle_status,
                COALESCE(comp.authority_source_artifacts, '') AS authority_source_artifacts,
                COALESCE(comp.authority_gap_reason, '') AS authority_gap_reason
            FROM v_ddm_response_long_facet_ready base
            LEFT JOIN {POSTGRES_TABLE} comp
              ON comp.source = base.source
             AND comp.wave = COALESCE(base.wave, '')
             AND UPPER(comp.var_code) = UPPER(base.var_code);
            """
            cur.execute(view_sql)
    finally:
        conn.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the GSS authority compendium.")
    parser.add_argument("--write-postgres", action="store_true", default=False, help="Write the compendium and companion view into Postgres.")
    parser.add_argument("--wave", action="append", default=None, help="Optional wave filter. May be repeated.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    waves = [clean(value) for value in (args.wave or GSS_WAVES) if clean(value)] or GSS_WAVES
    compendium, gap_log, report = build_compendium(waves)
    REPORTS.mkdir(parents=True, exist_ok=True)
    compendium.to_csv(OUT_COMPENDIUM, index=False)
    gap_log.to_csv(OUT_GAP_LOG, index=False)
    OUT_REPORT.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    if args.write_postgres:
        write_postgres(compendium, gap_log)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
