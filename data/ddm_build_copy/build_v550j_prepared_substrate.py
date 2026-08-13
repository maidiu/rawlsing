#!/usr/bin/env python3
"""Build and cache prepared V550J response substrates."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pandas as pd

from data.ddm_build_copy.build_determinicity_repository_v550 import _harmonize_question_frame
from data.ddm_build_copy.ddm_v550_manifest import utc_now
from data.ddm_build_copy.ddm_v550_schema import write_schema_json
from data.ddm_build_copy.ddm_v550_storage import atomic_write_json
from data.ddm_build_copy.ddm_v550_shared_respondent_substrate import (
    PREPARED_SUBSTRATE_REQUIRED_COLUMNS as SHARED_PREPARED_SUBSTRATE_REQUIRED_COLUMNS,
    SHARED_SUBSTRATE_REQUIRED_COLUMNS,
    SHARED_SUBSTRATE_SCHEMA_VERSION,
    canonicalize_shared_respondent_substrate,
    load_shared_respondent_substrate,
    logical_shared_substrate_hash,
    shared_substrate_cache_signature_matches,
    shared_substrate_paths,
    validate_shared_respondent_substrate,
    write_shared_respondent_substrate_atomic,
)
from data.ddm_build_copy.ddm_v550j_joint_patterns import _family_item_map


SUBSTRATE_SCHEMA_VERSION = SHARED_SUBSTRATE_SCHEMA_VERSION
DEFAULT_PREPARED_CACHE_ROOT = Path("data/ddm_repository_copy/v550j/cache/prepared_response_substrate")

PREPARED_SUBSTRATE_REQUIRED_COLUMNS = SHARED_PREPARED_SUBSTRATE_REQUIRED_COLUMNS


def _clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    text = str(value).strip()
    return "" if text.lower() in {"nan", "none"} else text


def _stable_hash(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _normalize_code_series(series: pd.Series) -> pd.Series:
    cleaned = series.fillna("").astype(str).str.strip()
    cleaned = cleaned.mask(cleaned.str.lower().isin({"nan", "none"}), "")
    cleaned = cleaned.str.replace(r"\.0+$", "", regex=True)
    return cleaned


def build_family_item_lookup(family_cfg: dict[str, Any]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for family_item_order, item in enumerate(_family_item_map(family_cfg), start=1):
        var_code = _clean(item.get("var_code")).upper()
        if not var_code:
            continue
        rows.append(
            {
                "family_id": _clean(family_cfg.get("family_id")),
                "var_code": var_code,
                "var_code_norm": var_code,
                "item_role": _clean(item.get("item_role")) or "target_case",
                "condition_label": _clean(item.get("condition_label")),
                "family_item_order": family_item_order,
                "minimum_items_answered": int(_clean(family_cfg.get("minimum_items_answered")) or 1),
            }
        )
    return pd.DataFrame(rows)


def _prepared_cache_dir(*, output_root: Path, source: str, wave: str, country_code: str) -> Path:
    return output_root / "cache" / "prepared_response_substrate" / f"source={source}" / f"wave={wave}" / f"country_code={country_code}"


def _prepared_manifest_path(cache_dir: Path) -> Path:
    return cache_dir / "v550j_prepared_response_substrate_manifest.json"


def _prepared_parquet_path(cache_dir: Path) -> Path:
    return cache_dir / "v550j_prepared_response_substrate.parquet"


def _ensure_prepared_columns(
    frame: pd.DataFrame,
    *,
    run_id: str,
    source: str,
    source_id: str,
    wave: str,
    canonical_wave: str,
    country_code: str,
) -> pd.DataFrame:
    out = frame.copy()
    defaults = {
        "run_id": run_id,
        "source": source,
        "source_id": source_id,
        "wave": wave,
        "canonical_wave": canonical_wave,
        "country_code": country_code,
        "respondent_id": "",
        "respondent_id_norm": "",
        "weight_value": 1.0,
        "weight_status": "",
        "var_code": "",
        "var_code_norm": "",
        "question_id": "",
        "question_text": "",
        "response_value": "",
        "response_value_normalized": "",
        "response_value_norm": "",
        "response_label": "",
        "normalized_response_label": "",
        "is_missing": False,
        "is_dk": False,
        "is_refusal": False,
        "is_iap": False,
        "is_valid_substantive_response": False,
        "semantic_response_role": "unknown",
        "semantic_response_role_status": "unknown",
        "response_semantics_authority_source": "none",
        "semantic_response_role_authority": "none",
        "response_direction": "",
        "polarity": "",
        "directionality_status": "unknown",
        "directionality_authority_source": "none",
        "directionality_basis_source": "observed_response_row",
        "target_entity_id": "",
        "target_domain": "",
        "target_condition_label": "",
        "target_group_label": "",
        "permission_domain": "",
        "target_resolution_grain": "unresolved",
        "target_resolution_status": "unresolved",
        "target_resolution_authority_source": "",
        "target_resolution_basis_source": "",
        "driver_id": "",
        "driver_facet_id": "",
        "relation_axis_id": "",
        "semantic_role": "",
        "v551_evidence_role": "",
        "mapping_status": "",
        "source_structure_classification": "",
        "question_type": "",
        "handling_rule": "",
        "recommended_computation": "",
        "source_structure_basis": "",
        "source_structure_confidence": "",
        "source_structure_source": "",
        "source_structure_fields_joined": False,
        "is_substantive": False,
        "not_direct_evidence": False,
        "allowed_as_association_feature": False,
        "allowed_as_attitude_cloud_feature": False,
        "association_lane": "unknown_association_lane",
        "source_norm": source.upper(),
        "wave_norm": wave.upper(),
        "canonical_wave_norm": canonical_wave.upper(),
        "country_code_norm": country_code.upper(),
        "var_code_norm": "",
    }
    for column, default in defaults.items():
        if column not in out.columns:
            out[column] = default
    out["run_id"] = out["run_id"].fillna(run_id).astype(str).str.strip()
    out["source"] = out["source"].fillna(source).astype(str).str.strip()
    out["source_id"] = out["source_id"].fillna(source_id).astype(str).str.strip()
    out["wave"] = out["wave"].fillna(wave).astype(str).str.strip()
    out["canonical_wave"] = out["canonical_wave"].fillna(canonical_wave).astype(str).str.strip()
    out["country_code"] = out["country_code"].fillna(country_code).astype(str).str.strip()
    out["respondent_id"] = out["respondent_id"].fillna("").astype(str).str.strip()
    out["respondent_id_norm"] = _normalize_code_series(out["respondent_id"])
    out["var_code"] = out["var_code"].fillna("").astype(str).str.strip()
    out["var_code_norm"] = _normalize_code_series(out["var_code"]).str.upper()
    out["question_id"] = out["question_id"].fillna("").astype(str).str.strip()
    out["question_text"] = out["question_text"].fillna("").astype(str).str.strip()
    if "response_value_normalized" not in out.columns:
        out["response_value_normalized"] = ""
    out["response_value_normalized"] = out["response_value_normalized"].fillna("").astype(str).str.strip()
    if "response_value" not in out.columns:
        out["response_value"] = ""
    out["response_value"] = out["response_value"].fillna("").astype(str).str.strip()
    if out["response_value"].eq("").all():
        out["response_value"] = out["response_value_normalized"]
    if "response_value_norm" not in out.columns:
        out["response_value_norm"] = ""
    out["response_value_norm"] = _normalize_code_series(out["response_value_normalized"])
    if "response_label" not in out.columns:
        out["response_label"] = ""
    out["response_label"] = out["response_label"].fillna("").astype(str).str.strip()
    if "normalized_response_label" not in out.columns:
        out["normalized_response_label"] = ""
    out["normalized_response_label"] = out["normalized_response_label"].fillna("").astype(str).str.strip()
    if out["response_label"].eq("").any():
        missing_mask = out["response_label"].eq("")
        out.loc[missing_mask, "response_label"] = out.loc[missing_mask, "response_value_normalized"]
    if out["normalized_response_label"].eq("").any():
        missing_mask = out["normalized_response_label"].eq("")
        out.loc[missing_mask, "normalized_response_label"] = out.loc[missing_mask, "response_value_normalized"]
    for column in ("is_missing", "is_dk", "is_refusal", "is_iap", "is_valid_substantive_response", "is_substantive", "not_direct_evidence", "allowed_as_association_feature", "allowed_as_attitude_cloud_feature"):
        out[column] = out[column].fillna(False).map(bool)
    if "association_lane" not in out.columns or out["association_lane"].fillna("").astype(str).str.strip().eq("").all():
        out["association_lane"] = out.apply(
            lambda row: "diagnostic_only_association"
            if bool(row.get("not_direct_evidence", False)) and not bool(row.get("allowed_as_association_feature", False))
            else "unknown_association_lane",
            axis=1,
        )
    out["source_norm"] = _normalize_code_series(out["source"]).str.upper()
    out["wave_norm"] = _normalize_code_series(out["wave"]).str.upper()
    out["canonical_wave_norm"] = _normalize_code_series(out["canonical_wave"]).str.upper()
    out["country_code_norm"] = _normalize_code_series(out["country_code"]).str.upper()
    return out.reset_index(drop=True)


def _should_harmonize(frame: pd.DataFrame) -> bool:
    required = [
        "semantic_response_role",
        "semantic_response_role_status",
        "response_semantics_authority_source",
        "directionality_status",
        "directionality_authority_source",
        "target_resolution_status",
        "target_resolution_grain",
        "allowed_as_association_feature",
        "not_direct_evidence",
        "is_substantive",
    ]
    if frame.empty:
        return False
    for column in required:
        if column not in frame.columns:
            return True
        if frame[column].fillna("").astype(str).str.strip().eq("").all():
            return True
    return False


def _resolve_hash(value: str | None, fallback: str = "") -> str:
    text = _clean(value)
    return text or fallback


def _validate_prepared_substrate(prepared: pd.DataFrame, manifest: dict[str, Any], cache_dir: Path) -> dict[str, Any]:
    missing_columns = [column for column in PREPARED_SUBSTRATE_REQUIRED_COLUMNS if column not in prepared.columns]
    normalized_columns = [column for column in ("respondent_id_norm", "var_code_norm", "response_value_norm", "source_norm", "wave_norm", "canonical_wave_norm", "country_code_norm") if column in prepared.columns]
    non_null_normalized = {column: int(prepared[column].fillna("").astype(str).str.strip().ne("").sum()) for column in normalized_columns}
    substantive_rows = prepared[prepared["is_substantive"].fillna(False)] if "is_substantive" in prepared.columns else prepared.iloc[0:0]
    validation_status = "pass"
    validation_message = "ok"
    if missing_columns:
        validation_status = "fail"
        validation_message = f"missing required columns: {', '.join(missing_columns)}"
    elif not prepared.empty and "respondent_id_norm" in prepared.columns and substantive_rows["respondent_id_norm"].fillna("").astype(str).str.strip().eq("").any():
        validation_status = "fail"
        validation_message = "substantive rows missing respondent_id_norm"
    elif not prepared.empty and "var_code_norm" in prepared.columns and prepared["var_code_norm"].fillna("").astype(str).str.strip().eq("").any():
        validation_status = "fail"
        validation_message = "missing var_code_norm values"
    elif not prepared.empty and "response_value_norm" in prepared.columns and substantive_rows["response_value_norm"].fillna("").astype(str).str.strip().eq("").any():
        validation_status = "fail"
        validation_message = "substantive rows missing response_value_norm"
    report = {
        "run_id": manifest.get("run_id", ""),
        "source": manifest.get("source", ""),
        "source_id": manifest.get("source_id", ""),
        "wave": manifest.get("wave", ""),
        "canonical_wave": manifest.get("canonical_wave", ""),
        "country_code": manifest.get("country_code", ""),
        "row_count": int(len(prepared)),
        "respondent_count": int(prepared["respondent_id_norm"].nunique() if "respondent_id_norm" in prepared.columns else prepared["respondent_id"].nunique() if "respondent_id" in prepared.columns else 0),
        "var_count": int(prepared["var_code_norm"].nunique() if "var_code_norm" in prepared.columns else prepared["var_code"].nunique() if "var_code" in prepared.columns else 0),
        "required_columns": PREPARED_SUBSTRATE_REQUIRED_COLUMNS,
        "missing_columns": missing_columns,
        "normalized_columns_non_null_counts": non_null_normalized,
        "cache_valid": bool(manifest.get("cache_valid", False)),
        "validation_status": validation_status,
        "validation_message": validation_message,
        "manifest_row_count": int(manifest.get("row_count", len(prepared)) or len(prepared)),
        "manifest_respondent_count": int(manifest.get("respondent_count", 0) or 0),
        "manifest_var_count": int(manifest.get("var_count", 0) or 0),
    }
    atomic_write_json(cache_dir / "v550j_prepared_substrate_validation_report.json", report)
    return report


def _cache_signature_matches(manifest: dict[str, Any], *, authority_compendium_hash: str, question_family_registry_hash: str, response_semantics_contract_hash: str, view_schema_hash: str, compiler_version: str) -> bool:
    expected = {
        "authority_compendium_hash": _resolve_hash(authority_compendium_hash, response_semantics_contract_hash),
        "question_family_registry_hash": _resolve_hash(question_family_registry_hash),
        "response_semantics_contract_hash": _resolve_hash(response_semantics_contract_hash),
        "view_schema_hash": _resolve_hash(view_schema_hash),
        "compiler_version": _resolve_hash(compiler_version),
        "substrate_schema_version": SUBSTRATE_SCHEMA_VERSION,
    }
    for key, expected_value in expected.items():
        actual_value = _resolve_hash(manifest.get(key, ""))
        if expected_value and actual_value and actual_value != expected_value:
            return False
        if expected_value and not actual_value:
            return False
    return True


def load_or_build_v550j_prepared_substrate(
    *,
    run_id: str,
    source: str,
    source_id: str,
    wave: str,
    canonical_wave: str,
    country_code: str,
    source_frame: pd.DataFrame,
    semantics_lookup: dict[tuple[str, str, str, str], dict[str, Any]] | None,
    response_semantics_contract_hash: str,
    output_root: Path,
    question_family_registry_hash: str = "",
    authority_compendium_hash: str = "",
    view_schema_hash: str = "",
    compiler_version: str = "v550j_prepared_substrate_v1",
    substrate_mode: str = "prepared_or_build",
    progress: Any | None = None,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    cache_dir = _prepared_cache_dir(output_root=output_root, source=source, wave=wave, country_code=country_code)
    parquet_path = _prepared_parquet_path(cache_dir)
    manifest_path = _prepared_manifest_path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)

    manifest: dict[str, Any] = {}
    cache_valid = False
    if parquet_path.exists() and manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            cache_valid = bool(manifest.get("cache_valid", False))
        except Exception:
            cache_valid = False
        if cache_valid:
            cache_valid = _cache_signature_matches(
                manifest,
                authority_compendium_hash=authority_compendium_hash,
                question_family_registry_hash=question_family_registry_hash,
                response_semantics_contract_hash=response_semantics_contract_hash,
                view_schema_hash=view_schema_hash,
                compiler_version=compiler_version,
            )
        if cache_valid and substrate_mode in {"prepared_required", "prepared_or_build", "prepared_or_forensic_fallback"}:
            prepared = pd.read_parquet(parquet_path)
            prepared = _ensure_prepared_columns(
                prepared,
                run_id=run_id,
                source=source,
                source_id=source_id,
                wave=wave,
                canonical_wave=canonical_wave,
                country_code=country_code,
            )
            manifest["cache_loaded"] = True
            manifest["cache_valid"] = True
            _validate_prepared_substrate(prepared, manifest, cache_dir)
            return prepared, manifest

    if substrate_mode == "prepared_required" and not parquet_path.exists():
        raise RuntimeError(f"Prepared substrate missing and substrate_mode=prepared_required: {parquet_path}")
    if source_frame is None or source_frame.empty:
        if substrate_mode == "prepared_or_forensic_fallback":
            prepared = pd.DataFrame()
            manifest = {
                "run_id": run_id,
                "source": source,
                "source_id": source_id,
                "wave": wave,
                "canonical_wave": canonical_wave,
                "country_code": country_code,
                "row_count": 0,
                "respondent_count": 0,
                "var_count": 0,
                "created_at": utc_now(),
                "compiler_version": compiler_version,
                "substrate_schema_version": SUBSTRATE_SCHEMA_VERSION,
                "authority_compendium_hash": _resolve_hash(authority_compendium_hash, response_semantics_contract_hash),
                "question_family_registry_hash": _resolve_hash(question_family_registry_hash),
                "response_semantics_contract_hash": _resolve_hash(response_semantics_contract_hash),
                "view_schema_hash": _resolve_hash(view_schema_hash),
                "input_query_or_source": f"{source}/{wave}/{country_code}",
                "column_list": [],
                "missing_expected_columns": [],
                "cache_valid": False,
                "hash_unavailable_reason": "source_frame_empty",
                "harmonization_calls": 0,
            }
            atomic_write_json(manifest_path, manifest)
            prepared.to_parquet(parquet_path, index=False)
            _validate_prepared_substrate(prepared, manifest, cache_dir)
            return prepared, manifest
        raise RuntimeError("Prepared substrate build requires a non-empty source frame.")

    prepared = source_frame.copy()
    harmonization_calls = 0
    if _should_harmonize(prepared):
        if progress is not None:
            progress.note(f"Prepared substrate: harmonizing {len(prepared)} rows once")
        if semantics_lookup is None:
            semantics_lookup = {}
        prepared = _harmonize_question_frame(prepared, semantics_lookup, response_semantics_contract_hash=response_semantics_contract_hash)
        harmonization_calls = 1
    prepared = _ensure_prepared_columns(
        prepared,
        run_id=run_id,
        source=source,
        source_id=source_id,
        wave=wave,
        canonical_wave=canonical_wave,
        country_code=country_code,
    )
    expected_columns = [
        "run_id",
        "source",
        "source_id",
        "wave",
        "canonical_wave",
        "country_code",
        "respondent_id",
        "respondent_id_norm",
        "weight_value",
        "weight_status",
        "var_code",
        "var_code_norm",
        "question_id",
        "question_text",
        "response_value",
        "response_value_normalized",
        "response_value_norm",
        "response_label",
        "normalized_response_label",
        "is_missing",
        "is_dk",
        "is_refusal",
        "is_iap",
        "is_valid_substantive_response",
        "semantic_response_role",
        "semantic_response_role_status",
        "response_semantics_authority_source",
        "semantic_response_role_authority",
        "response_direction",
        "polarity",
        "directionality_status",
        "directionality_authority_source",
        "directionality_basis_source",
        "target_entity_id",
        "target_domain",
        "target_condition_label",
        "target_group_label",
        "permission_domain",
        "target_resolution_grain",
        "target_resolution_status",
        "target_resolution_authority_source",
        "target_resolution_basis_source",
        "driver_id",
        "driver_facet_id",
        "relation_axis_id",
        "semantic_role",
        "v551_evidence_role",
        "mapping_status",
        "source_structure_classification",
        "question_type",
        "handling_rule",
        "recommended_computation",
        "is_substantive",
        "not_direct_evidence",
        "allowed_as_association_feature",
        "allowed_as_attitude_cloud_feature",
        "association_lane",
        "source_norm",
        "wave_norm",
        "canonical_wave_norm",
        "country_code_norm",
    ]
    missing_expected_columns = [column for column in expected_columns if column not in prepared.columns]
    prepared = prepared.reindex(columns=list(dict.fromkeys(list(prepared.columns) + expected_columns)))
    prepared = prepared.reset_index(drop=True)
    prepared.to_parquet(parquet_path, index=False)

    manifest = {
        "run_id": run_id,
        "source": source,
        "source_id": source_id,
        "wave": wave,
        "canonical_wave": canonical_wave,
        "country_code": country_code,
        "row_count": int(len(prepared)),
        "respondent_count": int(prepared["respondent_id_norm"].nunique() if "respondent_id_norm" in prepared.columns else prepared["respondent_id"].nunique() if "respondent_id" in prepared.columns else 0),
        "var_count": int(prepared["var_code_norm"].nunique() if "var_code_norm" in prepared.columns else prepared["var_code"].nunique() if "var_code" in prepared.columns else 0),
        "created_at": utc_now(),
        "compiler_version": compiler_version,
        "substrate_schema_version": SUBSTRATE_SCHEMA_VERSION,
        "authority_compendium_hash": _resolve_hash(authority_compendium_hash, response_semantics_contract_hash),
        "question_family_registry_hash": _resolve_hash(question_family_registry_hash),
        "response_semantics_contract_hash": _resolve_hash(response_semantics_contract_hash),
        "view_schema_hash": _resolve_hash(view_schema_hash),
        "input_query_or_source": f"{source}/{wave}/{country_code}",
        "column_list": list(prepared.columns),
        "missing_expected_columns": missing_expected_columns,
        "cache_valid": True,
        "hash_unavailable_reason": "" if authority_compendium_hash or response_semantics_contract_hash else "authority_compendium_hash unavailable in this path",
        "harmonization_calls": harmonization_calls,
        "cache_loaded": False,
    }
    atomic_write_json(manifest_path, manifest)
    schema_path = cache_dir / "v550j_prepared_response_substrate.schema.json"
    write_schema_json(schema_path, prepared, name="v550j_prepared_response_substrate", run_id=run_id, extra={"layer": "v550j_prepared_substrate"})
    _validate_prepared_substrate(prepared, manifest, cache_dir)
    return prepared, manifest
