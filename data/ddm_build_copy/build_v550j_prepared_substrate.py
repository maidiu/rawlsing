#!/usr/bin/env python3
"""Build and cache prepared V550J response substrates."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pandas as pd

from data.ddm_build_copy.build_determinicity_repository_v550 import _harmonize_question_frame
from data.ddm_build_copy.ddm_pipeline_boundary_contract import (
    BoundaryContractError,
    verify_exact_identity,
    verify_frame_source_wave_identity_coherence,
    verify_manifest_source_wave_identity_coherence,
)
from data.ddm_build_copy.ddm_source_wave_identity import load_identity_registry
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
V550J_PREPARED_CACHE_IDENTITY_BINDING_VERSION = "v550j_prepared_cache_identity_v1"

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


def v550j_identity_contract_metadata() -> dict[str, str]:
    """Return the frozen W01 source/wave identity contract metadata."""
    registry = load_identity_registry()
    return {
        "identity_registry_id": str(registry.registry_id),
        "identity_schema_version": str(registry.schema_version),
        "identity_contract_version": str(registry.uid_namespace_version),
        "identity_uid_namespace_version": str(registry.uid_namespace_version),
        "identity_physical_token_version": str(registry.physical_token_version),
    }


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
    # Legacy physical cache path is intentionally frozen/readable. Governed
    # identity is bound inside the manifest rather than silently renaming it.
    return output_root / "cache" / "prepared_response_substrate" / f"source={source}" / f"wave={wave}" / f"country_code={country_code}"


def _prepared_manifest_path(cache_dir: Path) -> Path:
    return cache_dir / "v550j_prepared_response_substrate_manifest.json"


def _prepared_parquet_path(cache_dir: Path) -> Path:
    return cache_dir / "v550j_prepared_response_substrate.parquet"


def _bind_exact_column(out: pd.DataFrame, column: str, expected: str) -> None:
    expected_text = _clean(expected)
    if column not in out.columns:
        out[column] = expected_text
        return
    values = out[column].fillna("").astype(str).str.strip()
    bad = values.ne("") & values.ne(expected_text)
    if bool(bad.any()):
        observed = sorted(set(values.loc[bad].tolist()))
        raise BoundaryContractError(
            f"V550J_PREPARED_IDENTITY_CONTRADICTION:{column}:expected={expected_text}:observed={observed[:8]}"
        )
    out.loc[values.eq(""), column] = expected_text


def _fill_role_column(out: pd.DataFrame, column: str, value: str) -> None:
    value_text = _clean(value)
    if column not in out.columns:
        out[column] = value_text
        return
    existing = out[column].fillna("").astype(str).str.strip()
    out.loc[existing.eq(""), column] = value_text


def _validate_exact_frame_scope(
    frame: pd.DataFrame,
    *,
    run_id: str,
    country_code: str,
    shard_id: str,
    scope_kind: str,
    identity_contract_version: str,
    require_bound_fields: bool,
) -> None:
    if frame.empty:
        return
    expectations = {
        "run_id": run_id,
        "country_code": country_code,
        "scope_kind": scope_kind,
        "identity_contract_version": identity_contract_version,
    }
    if shard_id:
        expectations["shard_id"] = shard_id
    for column, expected in expectations.items():
        if column not in frame.columns:
            if require_bound_fields:
                raise BoundaryContractError(f"V550J_PREPARED_IDENTITY_FIELD_MISSING:{column}")
            continue
        values = {_clean(value) for value in frame[column].tolist() if _clean(value)}
        if require_bound_fields and not values:
            raise BoundaryContractError(f"V550J_PREPARED_IDENTITY_FIELD_MISSING:{column}")
        if values and values != {_clean(expected)}:
            raise BoundaryContractError(
                f"V550J_PREPARED_SCOPE_MISMATCH:{column}:expected={_clean(expected)}:observed={sorted(values)}"
            )


def _validate_prepared_identity(
    frame: pd.DataFrame,
    *,
    source_family_uid: str,
    wave_uid: str,
    run_id: str,
    country_code: str,
    shard_id: str,
    scope_kind: str,
    identity_contract_version: str,
    require_bound_fields: bool,
) -> dict[str, Any]:
    coherence = verify_frame_source_wave_identity_coherence(
        frame,
        expected_source_family_uid=source_family_uid,
        expected_wave_uid=wave_uid,
        allow_empty=True,
    )
    _validate_exact_frame_scope(
        frame,
        run_id=run_id,
        country_code=country_code,
        shard_id=shard_id,
        scope_kind=scope_kind,
        identity_contract_version=identity_contract_version,
        require_bound_fields=require_bound_fields,
    )
    return coherence


def _ensure_prepared_columns(
    frame: pd.DataFrame,
    *,
    run_id: str,
    source: str,
    source_id: str,
    wave: str,
    canonical_wave: str,
    country_code: str,
    source_family_uid: str,
    wave_uid: str,
    identity_contract_version: str,
    raw_source: str = "",
    raw_wave: str = "",
    canonical_display_source: str = "",
    canonical_display_wave: str = "",
    shard_id: str = "",
    scope_kind: str = "country",
) -> pd.DataFrame:
    out = frame.copy()
    verify_frame_source_wave_identity_coherence(
        out,
        expected_source_family_uid=source_family_uid,
        expected_wave_uid=wave_uid,
        allow_empty=True,
    )
    canonical_source_value = _clean(canonical_display_source) or _clean(source)
    canonical_wave_value = _clean(canonical_display_wave) or _clean(canonical_wave)
    raw_source_value = _clean(raw_source) or _clean(source)
    raw_wave_value = _clean(raw_wave) or _clean(wave)
    defaults = {
        "run_id": run_id,
        "source": source,
        "source_id": source_id,
        "wave": wave,
        "canonical_wave": canonical_wave,
        "raw_source": raw_source_value,
        "raw_wave": raw_wave_value,
        "canonical_display_source": canonical_source_value,
        "canonical_display_wave": canonical_wave_value,
        "source_family_uid": source_family_uid,
        "wave_uid": wave_uid,
        "identity_contract_version": identity_contract_version,
        "shard_id": shard_id,
        "scope_kind": scope_kind,
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
    for column, expected in (
        ("run_id", run_id),
        ("country_code", country_code),
        ("source_family_uid", source_family_uid),
        ("wave_uid", wave_uid),
        ("identity_contract_version", identity_contract_version),
        ("shard_id", shard_id),
        ("scope_kind", scope_kind),
        ("raw_source", raw_source_value),
        ("raw_wave", raw_wave_value),
        ("canonical_display_source", canonical_source_value),
        ("canonical_display_wave", canonical_wave_value),
    ):
        _bind_exact_column(out, column, expected)
    _fill_role_column(out, "source", source)
    _fill_role_column(out, "source_id", source_id)
    _fill_role_column(out, "wave", wave)
    _fill_role_column(out, "canonical_wave", canonical_wave)
    verify_frame_source_wave_identity_coherence(
        out,
        expected_source_family_uid=source_family_uid,
        expected_wave_uid=wave_uid,
        allow_empty=True,
    )
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
        "source_family_uid": manifest.get("source_family_uid", ""),
        "wave_uid": manifest.get("wave_uid", ""),
        "identity_contract_version": manifest.get("identity_contract_version", ""),
        "shard_id": manifest.get("shard_id", ""),
        "scope_kind": manifest.get("scope_kind", ""),
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


def _cache_signature_matches(
    manifest: dict[str, Any],
    *,
    authority_compendium_hash: str,
    question_family_registry_hash: str,
    response_semantics_contract_hash: str,
    view_schema_hash: str,
    compiler_version: str,
    run_id: str,
    source_family_uid: str,
    wave_uid: str,
    country_code: str,
    shard_id: str,
    scope_kind: str,
    raw_source: str,
    raw_wave: str,
    canonical_display_source: str,
    canonical_display_wave: str,
    identity_metadata: dict[str, str],
) -> bool:
    expected = {
        "authority_compendium_hash": _resolve_hash(authority_compendium_hash, response_semantics_contract_hash),
        "question_family_registry_hash": _resolve_hash(question_family_registry_hash),
        "response_semantics_contract_hash": _resolve_hash(response_semantics_contract_hash),
        "view_schema_hash": _resolve_hash(view_schema_hash),
        "compiler_version": _resolve_hash(compiler_version),
        "substrate_schema_version": SUBSTRATE_SCHEMA_VERSION,
        "prepared_cache_identity_binding_version": V550J_PREPARED_CACHE_IDENTITY_BINDING_VERSION,
        "run_id": _clean(run_id),
        "source_family_uid": _clean(source_family_uid),
        "wave_uid": _clean(wave_uid),
        "country_code": _clean(country_code),
        "shard_id": _clean(shard_id),
        "scope_kind": _clean(scope_kind),
        "raw_source": _clean(raw_source),
        "raw_wave": _clean(raw_wave),
        "canonical_display_source": _clean(canonical_display_source),
        "canonical_display_wave": _clean(canonical_display_wave),
        "identity_registry_id": identity_metadata["identity_registry_id"],
        "identity_schema_version": identity_metadata["identity_schema_version"],
        "identity_contract_version": identity_metadata["identity_contract_version"],
    }
    for key, expected_value in expected.items():
        actual_value = _resolve_hash(manifest.get(key, ""))
        if actual_value != _resolve_hash(expected_value):
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
    source_family_uid: str,
    wave_uid: str,
    source_frame: pd.DataFrame,
    semantics_lookup: dict[tuple[str, str, str, str], dict[str, Any]] | None,
    response_semantics_contract_hash: str,
    output_root: Path,
    raw_source: str = "",
    raw_wave: str = "",
    canonical_display_source: str = "",
    canonical_display_wave: str = "",
    shard_id: str = "",
    scope_kind: str = "country",
    question_family_registry_hash: str = "",
    authority_compendium_hash: str = "",
    view_schema_hash: str = "",
    compiler_version: str = "v550j_prepared_substrate_v1",
    substrate_mode: str = "prepared_or_build",
    progress: Any | None = None,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    source_family_uid = _clean(source_family_uid)
    wave_uid = _clean(wave_uid)
    if not source_family_uid or not wave_uid:
        raise BoundaryContractError("V550J_PREPARED_UID_IDENTITY_REQUIRED")
    identity_metadata = v550j_identity_contract_metadata()
    identity_contract_version = identity_metadata["identity_contract_version"]
    canonical_source_value = _clean(canonical_display_source) or _clean(source)
    canonical_wave_value = _clean(canonical_display_wave) or _clean(canonical_wave)
    raw_source_value = _clean(raw_source) or _clean(source)
    raw_wave_value = _clean(raw_wave) or _clean(wave)
    cache_dir = _prepared_cache_dir(output_root=output_root, source=source, wave=wave, country_code=country_code)
    parquet_path = _prepared_parquet_path(cache_dir)
    manifest_path = _prepared_manifest_path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)

    manifest: dict[str, Any] = {}
    cache_valid = False
    stale_cache_detected = parquet_path.exists() or manifest_path.exists()
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
                run_id=run_id,
                source_family_uid=source_family_uid,
                wave_uid=wave_uid,
                country_code=country_code,
                shard_id=shard_id,
                scope_kind=scope_kind,
                raw_source=raw_source_value,
                raw_wave=raw_wave_value,
                canonical_display_source=canonical_source_value,
                canonical_display_wave=canonical_wave_value,
                identity_metadata=identity_metadata,
            )
        if cache_valid:
            try:
                verify_manifest_source_wave_identity_coherence(
                    manifest,
                    expected_source_family_uid=source_family_uid,
                    expected_wave_uid=wave_uid,
                )
                verify_exact_identity(
                    manifest,
                    run_id=run_id,
                    country_code=country_code,
                    shard_id=shard_id,
                    source_family_uid=source_family_uid,
                    wave_uid=wave_uid,
                )
            except BoundaryContractError:
                cache_valid = False
        if cache_valid and substrate_mode in {"prepared_required", "prepared_or_build", "prepared_or_forensic_fallback"}:
            prepared_frame = pd.read_parquet(parquet_path)
            _validate_prepared_identity(
                prepared_frame,
                source_family_uid=source_family_uid,
                wave_uid=wave_uid,
                run_id=run_id,
                country_code=country_code,
                shard_id=shard_id,
                scope_kind=scope_kind,
                identity_contract_version=identity_contract_version,
                require_bound_fields=True,
            )
            prepared_frame = _ensure_prepared_columns(
                prepared_frame,
                run_id=run_id,
                source=source,
                source_id=source_id,
                wave=wave,
                canonical_wave=canonical_wave,
                country_code=country_code,
                source_family_uid=source_family_uid,
                wave_uid=wave_uid,
                identity_contract_version=identity_contract_version,
                raw_source=raw_source_value,
                raw_wave=raw_wave_value,
                canonical_display_source=canonical_source_value,
                canonical_display_wave=canonical_wave_value,
                shard_id=shard_id,
                scope_kind=scope_kind,
            )
            manifest["cache_loaded"] = True
            manifest["cache_valid"] = True
            _validate_prepared_substrate(prepared_frame, manifest, cache_dir)
            return prepared_frame, manifest

    if substrate_mode == "prepared_required" and stale_cache_detected and not cache_valid:
        raise RuntimeError(
            "V550J_PREPARED_CACHE_IDENTITY_OR_CONTRACT_MISMATCH: existing cache cannot be rebound in prepared_required mode"
        )
    if substrate_mode == "prepared_required" and not parquet_path.exists():
        raise RuntimeError(f"Prepared substrate missing and substrate_mode=prepared_required: {parquet_path}")
    if source_frame is None or source_frame.empty:
        if substrate_mode == "prepared_or_forensic_fallback":
            prepared_frame = pd.DataFrame()
            manifest = {
                "run_id": run_id,
                "producer_run_id": run_id,
                "source": source,
                "source_id": source_id,
                "wave": wave,
                "canonical_wave": canonical_wave,
                "raw_source": raw_source_value,
                "raw_wave": raw_wave_value,
                "canonical_display_source": canonical_source_value,
                "canonical_display_wave": canonical_wave_value,
                "source_family_uid": source_family_uid,
                "wave_uid": wave_uid,
                "shard_id": shard_id,
                "scope_kind": scope_kind,
                "country_code": country_code,
                **identity_metadata,
                "prepared_cache_identity_binding_version": V550J_PREPARED_CACHE_IDENTITY_BINDING_VERSION,
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
            prepared_frame.to_parquet(parquet_path, index=False)
            _validate_prepared_substrate(prepared_frame, manifest, cache_dir)
            return prepared_frame, manifest
        raise RuntimeError("Prepared substrate build requires a non-empty source frame.")

    _validate_prepared_identity(
        source_frame,
        source_family_uid=source_family_uid,
        wave_uid=wave_uid,
        run_id=run_id,
        country_code=country_code,
        shard_id=shard_id,
        scope_kind=scope_kind,
        identity_contract_version=identity_contract_version,
        require_bound_fields=False,
    )
    prepared_frame = source_frame.copy()
    harmonization_calls = 0
    if _should_harmonize(prepared_frame):
        if progress is not None:
            progress.note(f"Prepared substrate: harmonizing {len(prepared_frame)} rows once")
        if semantics_lookup is None:
            semantics_lookup = {}
        prepared_frame = _harmonize_question_frame(prepared_frame, semantics_lookup, response_semantics_contract_hash=response_semantics_contract_hash)
        harmonization_calls = 1
    prepared_frame = _ensure_prepared_columns(
        prepared_frame,
        run_id=run_id,
        source=source,
        source_id=source_id,
        wave=wave,
        canonical_wave=canonical_wave,
        country_code=country_code,
        source_family_uid=source_family_uid,
        wave_uid=wave_uid,
        identity_contract_version=identity_contract_version,
        raw_source=raw_source_value,
        raw_wave=raw_wave_value,
        canonical_display_source=canonical_source_value,
        canonical_display_wave=canonical_wave_value,
        shard_id=shard_id,
        scope_kind=scope_kind,
    )
    expected_columns = [
        "run_id",
        "source",
        "source_id",
        "wave",
        "canonical_wave",
        "raw_source",
        "raw_wave",
        "canonical_display_source",
        "canonical_display_wave",
        "source_family_uid",
        "wave_uid",
        "identity_contract_version",
        "shard_id",
        "scope_kind",
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
    missing_expected_columns = [column for column in expected_columns if column not in prepared_frame.columns]
    prepared_frame = prepared_frame.reindex(columns=list(dict.fromkeys(list(prepared_frame.columns) + expected_columns)))
    prepared_frame = prepared_frame.reset_index(drop=True)
    prepared_frame.to_parquet(parquet_path, index=False)

    manifest = {
        "run_id": run_id,
        "producer_run_id": run_id,
        "source": source,
        "source_id": source_id,
        "wave": wave,
        "canonical_wave": canonical_wave,
        "raw_source": raw_source_value,
        "raw_wave": raw_wave_value,
        "canonical_display_source": canonical_source_value,
        "canonical_display_wave": canonical_wave_value,
        "source_family_uid": source_family_uid,
        "wave_uid": wave_uid,
        "shard_id": shard_id,
        "scope_kind": scope_kind,
        "country_code": country_code,
        **identity_metadata,
        "prepared_cache_identity_binding_version": V550J_PREPARED_CACHE_IDENTITY_BINDING_VERSION,
        "row_count": int(len(prepared_frame)),
        "respondent_count": int(prepared_frame["respondent_id_norm"].nunique() if "respondent_id_norm" in prepared_frame.columns else prepared_frame["respondent_id"].nunique() if "respondent_id" in prepared_frame.columns else 0),
        "var_count": int(prepared_frame["var_code_norm"].nunique() if "var_code_norm" in prepared_frame.columns else prepared_frame["var_code"].nunique() if "var_code" in prepared_frame.columns else 0),
        "created_at": utc_now(),
        "compiler_version": compiler_version,
        "substrate_schema_version": SUBSTRATE_SCHEMA_VERSION,
        "authority_compendium_hash": _resolve_hash(authority_compendium_hash, response_semantics_contract_hash),
        "question_family_registry_hash": _resolve_hash(question_family_registry_hash),
        "response_semantics_contract_hash": _resolve_hash(response_semantics_contract_hash),
        "view_schema_hash": _resolve_hash(view_schema_hash),
        "input_query_or_source": f"{source}/{wave}/{country_code}",
        "column_list": list(prepared_frame.columns),
        "missing_expected_columns": missing_expected_columns,
        "cache_valid": True,
        "hash_unavailable_reason": "" if authority_compendium_hash or response_semantics_contract_hash else "authority_compendium_hash unavailable in this path",
        "harmonization_calls": harmonization_calls,
        "cache_loaded": False,
    }
    verify_manifest_source_wave_identity_coherence(
        manifest,
        expected_source_family_uid=source_family_uid,
        expected_wave_uid=wave_uid,
    )
    verify_exact_identity(
        manifest,
        run_id=run_id,
        country_code=country_code,
        shard_id=shard_id,
        source_family_uid=source_family_uid,
        wave_uid=wave_uid,
    )
    atomic_write_json(manifest_path, manifest)
    schema_path = cache_dir / "v550j_prepared_response_substrate.schema.json"
    write_schema_json(schema_path, prepared_frame, name="v550j_prepared_response_substrate", run_id=run_id, extra={"layer": "v550j_prepared_substrate"})
    _validate_prepared_substrate(prepared_frame, manifest, cache_dir)
    return prepared_frame, manifest
