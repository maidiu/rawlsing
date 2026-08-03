#!/usr/bin/env python3
"""Shared respondent-substrate helpers for V550/V550J co-execution."""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import pandas as pd

from data.ddm_build_copy.ddm_v550_schema import write_schema_json
from data.ddm_build_copy.ddm_survey_identity import canonical_wave_key, family_keys_equal
from data.ddm_build_copy.ddm_v550j_registry_contract import (
    require_executable_registry_status,
    require_joint_configuration_authority_release,
    require_p3_authority_release,
)


SHARED_SUBSTRATE_SCHEMA_VERSION = "v1"
SHARED_SUBSTRATE_EXECUTION_CONTRACT_VERSION = "v550-v550j-coexecution-v1"
SHARED_SUBSTRATE_BASENAME = "v550_shared_respondent_substrate"
REQUIRED_P3_AUTHORITY_RELEASE_ID = "P3-AUTHORITY-2026-08-02-R184"

PREPARED_SUBSTRATE_REQUIRED_COLUMNS = [
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
    "response_direction",
    "polarity",
    "is_missing",
    "is_dk",
    "is_refusal",
    "is_iap",
    "is_valid_substantive_response",
    "semantic_response_role",
    "semantic_response_role_status",
    "response_semantics_authority_source",
    "semantic_response_role_authority",
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
    "semantic_role",
    "v551_evidence_role",
    "mapping_status",
    "source_structure_classification",
    "question_type",
    "handling_rule",
    "recommended_computation",
    "source_structure_basis",
    "source_structure_confidence",
    "source_structure_source",
    "source_structure_fields_joined",
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

SHARED_SUBSTRATE_ADDITIVE_COLUMNS = [
    "shard_id",
    "selection_role",
    "base_fixture_selected",
    "joint_configuration_selected",
    "joint_configuration_ids_json",
]

SHARED_SUBSTRATE_REQUIRED_COLUMNS = PREPARED_SUBSTRATE_REQUIRED_COLUMNS + SHARED_SUBSTRATE_ADDITIVE_COLUMNS

LOGICAL_CONTENT_COLUMNS = SHARED_SUBSTRATE_REQUIRED_COLUMNS


@dataclass(frozen=True)
class SharedSubstratePaths:
    root: Path
    parquet_path: Path
    schema_path: Path
    manifest_path: Path
    validation_path: Path
    complete_path: Path


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


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


def _slug(value: Any) -> str:
    text = _clean(value)
    out = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in text)
    return out.strip("_") or "unknown"


def _normalize_code_series(series: pd.Series) -> pd.Series:
    cleaned = series.fillna("").astype(str).str.strip()
    cleaned = cleaned.mask(cleaned.str.lower().isin({"nan", "none", "null"}), "")
    cleaned = cleaned.str.replace(r"\.0+$", "", regex=True)
    return cleaned


def _json_hash(payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _set_file_private(path: Path) -> None:
    try:
        path.chmod(0o600)
    except OSError:
        pass


def _set_dir_private(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    try:
        path.chmod(0o700)
    except OSError:
        pass


def shared_substrate_paths(root: Path, *, source: str, canonical_wave: str, country_code: str) -> SharedSubstratePaths:
    base = (
        Path(root)
        / f"source={_slug(source)}"
        / f"wave={_slug(canonical_wave)}"
        / f"country_code={_slug(country_code)}"
    )
    return SharedSubstratePaths(
        root=base,
        parquet_path=base / f"{SHARED_SUBSTRATE_BASENAME}.parquet",
        schema_path=base / f"{SHARED_SUBSTRATE_BASENAME}.schema.json",
        manifest_path=base / f"{SHARED_SUBSTRATE_BASENAME}_manifest.json",
        validation_path=base / f"{SHARED_SUBSTRATE_BASENAME}_validation.json",
        complete_path=base / "COMPLETE",
    )


def _ordered_unique(values: Iterable[Any]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        text = _clean(value)
        if text and text not in seen:
            seen.add(text)
            out.append(text)
    return out


def _selection_role(var_code: str, base_vars: set[str], joint_vars: set[str]) -> str:
    key = var_code.upper()
    in_base = key in base_vars
    in_joint = key in joint_vars
    if in_base and in_joint:
        return "BASE_AND_JOINT"
    if in_joint:
        return "JOINT_ONLY"
    return "BASE_ONLY"


def _registry_family_waves(family_cfg: dict[str, Any], source: str) -> set[str]:
    values = family_cfg.get("eligible_waves") or family_cfg.get("waves") or []
    if isinstance(values, str):
        values = [values]
    return {canonical_wave_key(source, value) for value in values if _clean(value)}


def _registry_item_rows(family_cfg: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    groups = family_cfg.get("item_role_groups")
    if isinstance(groups, dict):
        for role, group_payload in groups.items():
            if isinstance(group_payload, list):
                group_items = group_payload
            elif isinstance(group_payload, dict):
                group_items = group_payload.get("items") or [group_payload]
            else:
                group_items = []
            for item in group_items:
                if isinstance(item, dict):
                    rows.append({"item_role": _clean(item.get("item_role")) or _clean(role), **item})
    for item in family_cfg.get("items") or family_cfg.get("variables") or []:
        if isinstance(item, dict):
            rows.append(item)
    return rows


def _row_identity_key(row: pd.Series | dict[str, Any]) -> str:
    for column in ("var_code", "var_name", "variable_id", "question_id", "question_implementation_id"):
        value = _clean(row.get(column, "") if isinstance(row, dict) else row.get(column, ""))
        if value:
            return value.upper()
    return ""


def resolve_shared_substrate_requirements(
    base_question_rows: pd.DataFrame,
    registry: dict[str, Any],
    *,
    source: str,
    canonical_wave: str,
    selected_configuration_ids: Iterable[Any] | None = None,
) -> dict[str, Any]:
    """Resolve base and bounded-V550J joint-required extraction surfaces."""
    require_executable_registry_status(registry.get("status"))
    p3_release = require_p3_authority_release(registry.get("p3_authority_release_id"))
    joint_release = require_joint_configuration_authority_release(registry.get("joint_configuration_authority_release_id"))

    selected = {str(value).strip() for value in selected_configuration_ids or [] if _clean(value)}
    base_rows = base_question_rows.copy()
    if "var_code" not in base_rows.columns:
        base_rows["var_code"] = ""
    base_rows["var_code_norm"] = _normalize_code_series(base_rows["var_code"]).str.upper()
    base_var_codes = _ordered_unique(base_rows["var_code_norm"])
    base_by_key = {_row_identity_key(row): row.to_dict() for _, row in base_rows.iterrows() if _row_identity_key(row)}

    scope_wave = canonical_wave_key(source, canonical_wave)
    registry_source = _clean(registry.get("source_family"))
    joint_rows: list[dict[str, Any]] = []
    joint_ids_by_var: dict[str, list[str]] = {}
    for family_cfg in registry.get("families", []):
        if not isinstance(family_cfg, dict):
            continue
        family_source = _clean(family_cfg.get("source_family")) or registry_source
        if family_source and not family_keys_equal(family_source, source):
            continue
        family_waves = _registry_family_waves(family_cfg, source)
        if family_waves and scope_wave not in family_waves:
            continue
        family_id = _clean(family_cfg.get("joint_configuration_id")) or _clean(family_cfg.get("family_id"))
        if selected and family_id not in selected:
            continue
        for item in _registry_item_rows(family_cfg):
            var_code = _clean(item.get("var_code") or item.get("var_name") or item.get("variable_id")).upper()
            if not var_code:
                continue
            source_row = dict(base_by_key.get(var_code, {}))
            source_row.update(
                {
                    "var_code": source_row.get("var_code") or var_code,
                    "var_code_norm": var_code,
                    "question_id": source_row.get("question_id") or _clean(item.get("question_id") or item.get("question_implementation_id")),
                    "question_implementation_id": source_row.get("question_implementation_id") or _clean(item.get("question_implementation_id")),
                    "source": source_row.get("source") or source,
                    "wave": source_row.get("wave") or canonical_wave,
                    "canonical_wave": source_row.get("canonical_wave") or canonical_wave,
                    "joint_configuration_id": family_id,
                    "joint_item_role": _clean(item.get("item_role")) or "target_case",
                    "joint_condition_label": _clean(item.get("condition_label")),
                }
            )
            joint_rows.append(source_row)
            joint_ids_by_var.setdefault(var_code, [])
            if family_id and family_id not in joint_ids_by_var[var_code]:
                joint_ids_by_var[var_code].append(family_id)

    joint_df = pd.DataFrame(joint_rows)
    joint_required_var_codes = _ordered_unique(joint_df["var_code_norm"] if "var_code_norm" in joint_df.columns else [])
    union_rows = base_rows.copy()
    if not joint_df.empty:
        base_keys = {value.upper() for value in base_var_codes}
        joint_only = joint_df[~joint_df["var_code_norm"].astype(str).str.upper().isin(base_keys)].copy()
        union_rows = pd.concat([base_rows, joint_only.reindex(columns=list(dict.fromkeys(list(base_rows.columns) + list(joint_only.columns))))], ignore_index=True, sort=False)
    selection = _selection_surfaces(base_var_codes, joint_required_var_codes)
    return {
        **selection,
        "base_question_rows": base_rows.reset_index(drop=True),
        "joint_required_question_rows": joint_df.reset_index(drop=True),
        "union_question_rows": union_rows.reset_index(drop=True),
        "joint_configuration_ids_by_var": joint_ids_by_var,
        "applicable_joint_configuration_ids": _ordered_unique(
            joint_df["joint_configuration_id"] if "joint_configuration_id" in joint_df.columns else []
        ),
        "p3_authority_release_id": p3_release,
        "joint_configuration_authority_release_id": joint_release,
    }


def canonicalize_shared_respondent_substrate(
    frame: pd.DataFrame,
    *,
    run_id: str,
    shard_id: str,
    source: str,
    source_id: str = "",
    wave: str,
    canonical_wave: str,
    country_code: str,
    base_var_codes: Iterable[Any] = (),
    joint_required_var_codes: Iterable[Any] = (),
    joint_configuration_ids_by_var: dict[str, Iterable[Any]] | None = None,
) -> pd.DataFrame:
    """Return a V550J-compatible shared substrate without reharmonizing rows."""
    out = frame.copy()
    defaults: dict[str, Any] = {
        "run_id": run_id,
        "source": source,
        "source_id": source_id or source,
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
        "response_direction": "",
        "polarity": "",
        "is_missing": False,
        "is_dk": False,
        "is_refusal": False,
        "is_iap": False,
        "is_valid_substantive_response": False,
        "semantic_response_role": "unknown",
        "semantic_response_role_status": "unknown",
        "response_semantics_authority_source": "none",
        "semantic_response_role_authority": "none",
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
    }
    for column, default in defaults.items():
        if column not in out.columns:
            out[column] = default

    out["run_id"] = out["run_id"].fillna(run_id).astype(str).str.strip()
    out["source"] = out["source"].fillna(source).astype(str).str.strip()
    out["source_id"] = out["source_id"].fillna(source_id or source).astype(str).str.strip()
    out["wave"] = out["wave"].fillna(wave).astype(str).str.strip()
    out["canonical_wave"] = out["canonical_wave"].fillna(canonical_wave).astype(str).str.strip()
    out["country_code"] = out["country_code"].fillna(country_code).astype(str).str.strip()
    out["respondent_id"] = out["respondent_id"].fillna("").astype(str).str.strip()
    out["respondent_id_norm"] = _normalize_code_series(out["respondent_id"])
    out["var_code"] = out["var_code"].fillna("").astype(str).str.strip()
    out["var_code_norm"] = _normalize_code_series(out["var_code"]).str.upper()
    out["question_id"] = out["question_id"].fillna("").astype(str).str.strip()
    out["question_text"] = out["question_text"].fillna("").astype(str).str.strip()
    out["response_value_normalized"] = out["response_value_normalized"].fillna("").astype(str).str.strip()
    out["response_value"] = out["response_value"].fillna("").astype(str).str.strip()
    empty_response = out["response_value"].eq("")
    out.loc[empty_response, "response_value"] = out.loc[empty_response, "response_value_normalized"]
    out["response_value_norm"] = _normalize_code_series(out["response_value_normalized"])
    out["response_label"] = out["response_label"].fillna("").astype(str).str.strip()
    out["normalized_response_label"] = out["normalized_response_label"].fillna("").astype(str).str.strip()
    empty_label = out["response_label"].eq("")
    out.loc[empty_label, "response_label"] = out.loc[empty_label, "response_value_normalized"]
    empty_norm_label = out["normalized_response_label"].eq("")
    out.loc[empty_norm_label, "normalized_response_label"] = out.loc[empty_norm_label, "response_label"]
    for column in [
        "is_missing",
        "is_dk",
        "is_refusal",
        "is_iap",
        "is_valid_substantive_response",
        "source_structure_fields_joined",
        "is_substantive",
        "not_direct_evidence",
        "allowed_as_association_feature",
        "allowed_as_attitude_cloud_feature",
    ]:
        out[column] = out[column].fillna(False).map(bool)
    out["source_norm"] = _normalize_code_series(out["source"]).str.upper()
    out["wave_norm"] = _normalize_code_series(out["wave"]).str.upper()
    out["canonical_wave_norm"] = _normalize_code_series(out["canonical_wave"]).str.upper()
    out["country_code_norm"] = _normalize_code_series(out["country_code"]).str.upper()

    base_vars = {str(value).strip().upper() for value in base_var_codes if _clean(value)}
    joint_vars = {str(value).strip().upper() for value in joint_required_var_codes if _clean(value)}
    joint_ids = {key.upper(): _ordered_unique(values) for key, values in (joint_configuration_ids_by_var or {}).items()}
    out["shard_id"] = shard_id
    out["selection_role"] = out["var_code_norm"].map(lambda value: _selection_role(value, base_vars, joint_vars))
    out["base_fixture_selected"] = out["var_code_norm"].map(lambda value: value in base_vars)
    out["joint_configuration_selected"] = out["var_code_norm"].map(lambda value: value in joint_vars)
    out["joint_configuration_ids_json"] = out["var_code_norm"].map(lambda value: json.dumps(joint_ids.get(value, []), sort_keys=True))
    return out.reindex(columns=list(dict.fromkeys(SHARED_SUBSTRATE_REQUIRED_COLUMNS + list(out.columns)))).reset_index(drop=True)


def logical_shared_substrate_hash(frame: pd.DataFrame) -> str:
    canonical = frame.reindex(columns=LOGICAL_CONTENT_COLUMNS).copy()
    for column in canonical.columns:
        canonical[column] = canonical[column].map(lambda value: "" if value is None else value)
    row_hashes = [
        _json_hash({column: _clean(row[column]) for column in canonical.columns})
        for _, row in canonical.iterrows()
    ]
    return _json_hash(
        {
            "schema_version": SHARED_SUBSTRATE_SCHEMA_VERSION,
            "execution_contract_version": SHARED_SUBSTRATE_EXECUTION_CONTRACT_VERSION,
            "row_hashes": sorted(row_hashes),
        }
    )


def _selection_payload_hash(values: Iterable[Any]) -> str:
    return _json_hash(sorted({_clean(value) for value in values if _clean(value)}))


def _selection_surfaces(base_var_codes: Iterable[Any], joint_required_var_codes: Iterable[Any]) -> dict[str, Any]:
    base = sorted({str(value).strip() for value in base_var_codes if _clean(value)})
    joint = sorted({str(value).strip() for value in joint_required_var_codes if _clean(value)})
    base_keys = {value.upper(): value for value in base}
    joint_keys = {value.upper(): value for value in joint}
    union_keys = sorted(set(base_keys) | set(joint_keys))
    overlap_keys = sorted(set(base_keys) & set(joint_keys))
    base_only_keys = sorted(set(base_keys) - set(joint_keys))
    joint_only_keys = sorted(set(joint_keys) - set(base_keys))
    return {
        "base_var_codes": [base_keys[key] for key in sorted(base_keys)],
        "joint_required_var_codes": [joint_keys[key] for key in sorted(joint_keys)],
        "union_var_codes": [base_keys.get(key) or joint_keys[key] for key in union_keys],
        "base_only_var_codes": [base_keys[key] for key in base_only_keys],
        "joint_only_var_codes": [joint_keys[key] for key in joint_only_keys],
        "overlap_var_codes": [base_keys[key] for key in overlap_keys],
    }


def _duplicate_scalar_response_key_count(frame: pd.DataFrame) -> int:
    required = ["source_norm", "canonical_wave_norm", "country_code_norm", "respondent_id_norm", "var_code_norm"]
    if any(column not in frame.columns for column in required):
        return 0
    substantive = frame
    if "is_substantive" in frame.columns:
        substantive = frame[frame["is_substantive"].fillna(False).map(bool)]
    if substantive.empty:
        return 0
    duplicated = substantive.duplicated(required, keep=False)
    return int(duplicated.sum())


def validate_shared_respondent_substrate(
    frame: pd.DataFrame,
    manifest: dict[str, Any],
    *,
    fail_on_duplicate_scalar_keys: bool = True,
) -> dict[str, Any]:
    missing_columns = [column for column in SHARED_SUBSTRATE_REQUIRED_COLUMNS if column not in frame.columns]
    substantive = frame[frame["is_substantive"].fillna(False).map(bool)] if "is_substantive" in frame.columns else frame.iloc[0:0]
    problems: list[str] = []
    if missing_columns:
        problems.append("missing_required_columns")
    for column in ["respondent_id_norm", "var_code_norm", "response_value_norm"]:
        if column not in frame.columns:
            continue
        target = substantive if column in {"respondent_id_norm", "response_value_norm"} else frame
        if not target.empty and target[column].fillna("").astype(str).str.strip().eq("").any():
            problems.append(f"missing_{column}")
    for column, expected_key in [("source", "source"), ("canonical_wave", "canonical_wave"), ("country_code", "country_code")]:
        expected = _clean(manifest.get(expected_key))
        if expected and column in frame.columns:
            actual = {_clean(value) for value in frame[column].dropna().astype(str)}
            if actual and actual != {expected}:
                problems.append(f"{column}_scope_mismatch")
    duplicate_count = _duplicate_scalar_response_key_count(frame)
    if duplicate_count and fail_on_duplicate_scalar_keys:
        problems.append("unauthorized_duplicate_scalar_response_keys")
    logical_hash = logical_shared_substrate_hash(frame)
    manifest_hash = _clean(manifest.get("content_hash"))
    if manifest_hash and manifest_hash != logical_hash:
        problems.append("logical_content_hash_mismatch")
    validation_status = "pass" if not problems else "fail"
    return {
        "schema_version": SHARED_SUBSTRATE_SCHEMA_VERSION,
        "execution_contract_version": SHARED_SUBSTRATE_EXECUTION_CONTRACT_VERSION,
        "validation_status": validation_status,
        "validation_message": "ok" if not problems else ";".join(problems),
        "missing_columns": missing_columns,
        "row_count": int(len(frame)),
        "respondent_count": int(frame["respondent_id_norm"].nunique() if "respondent_id_norm" in frame.columns else 0),
        "var_count": int(frame["var_code_norm"].nunique() if "var_code_norm" in frame.columns else 0),
        "substantive_row_count": int(len(substantive)),
        "missing_row_count": int(frame["is_missing"].fillna(False).map(bool).sum() if "is_missing" in frame.columns else 0),
        "duplicate_scalar_response_key_count": duplicate_count,
        "content_hash": logical_hash,
        "cache_valid": validation_status == "pass",
    }


def write_shared_respondent_substrate_atomic(
    frame: pd.DataFrame,
    paths: SharedSubstratePaths,
    *,
    manifest_fields: dict[str, Any],
    base_var_codes: Iterable[Any] = (),
    joint_required_var_codes: Iterable[Any] = (),
) -> dict[str, Any]:
    _set_dir_private(paths.root)
    tmp_parquet = paths.root / f".{paths.parquet_path.name}.tmp"
    tmp_schema = paths.root / f".{paths.schema_path.name}.tmp"
    tmp_manifest = paths.root / f".{paths.manifest_path.name}.tmp"
    tmp_validation = paths.root / f".{paths.validation_path.name}.tmp"
    tmp_complete = paths.root / ".COMPLETE.tmp"
    for tmp in [tmp_parquet, tmp_schema, tmp_manifest, tmp_validation, tmp_complete]:
        if tmp.exists():
            tmp.unlink()

    frame.to_parquet(tmp_parquet, index=False)
    _set_file_private(tmp_parquet)
    write_schema_json(tmp_schema, frame, name=SHARED_SUBSTRATE_BASENAME, run_id=_clean(manifest_fields.get("run_id")), extra={"schema_version": SHARED_SUBSTRATE_SCHEMA_VERSION})
    _set_file_private(tmp_schema)

    validation_seed = validate_shared_respondent_substrate(frame, {}, fail_on_duplicate_scalar_keys=True)
    selection = _selection_surfaces(base_var_codes, joint_required_var_codes)
    manifest = {
        "schema_version": SHARED_SUBSTRATE_SCHEMA_VERSION,
        "execution_contract_version": SHARED_SUBSTRATE_EXECUTION_CONTRACT_VERSION,
        **selection,
        "base_selection_hash": _selection_payload_hash(selection["base_var_codes"]),
        "joint_selection_hash": _selection_payload_hash(selection["joint_required_var_codes"]),
        "union_selection_hash": _selection_payload_hash(selection["union_var_codes"]),
        "created_at_utc": utc_now(),
        "row_count": validation_seed["row_count"],
        "respondent_count": validation_seed["respondent_count"],
        "var_count": validation_seed["var_count"],
        "substantive_row_count": validation_seed["substantive_row_count"],
        "missing_row_count": validation_seed["missing_row_count"],
        "duplicate_scalar_response_key_count": validation_seed["duplicate_scalar_response_key_count"],
        "content_hash": validation_seed["content_hash"],
        "parquet_file_sha256": _file_sha256(tmp_parquet),
        "schema_hash": _file_sha256(tmp_schema),
        "cache_valid": False,
        "validation_status": "pending",
        **manifest_fields,
    }
    validation = validate_shared_respondent_substrate(frame, manifest, fail_on_duplicate_scalar_keys=True)
    manifest["validation_status"] = validation["validation_status"]
    manifest["cache_valid"] = validation["validation_status"] == "pass"
    if validation["validation_status"] != "pass":
        tmp_validation.write_text(json.dumps(validation, indent=2, ensure_ascii=False), encoding="utf-8")
        _set_file_private(tmp_validation)
        raise RuntimeError(f"shared respondent substrate validation failed: {validation['validation_message']}")

    tmp_manifest.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp_validation.write_text(json.dumps(validation, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp_complete.write_text(json.dumps({"completed_at_utc": utc_now(), "content_hash": manifest["content_hash"]}, sort_keys=True) + "\n", encoding="utf-8")
    for tmp in [tmp_manifest, tmp_validation, tmp_complete]:
        _set_file_private(tmp)

    reloaded = pd.read_parquet(tmp_parquet)
    reloaded_hash = logical_shared_substrate_hash(reloaded)
    if reloaded_hash != manifest["content_hash"]:
        raise RuntimeError("shared respondent substrate reload hash mismatch before promotion")

    tmp_parquet.replace(paths.parquet_path)
    tmp_schema.replace(paths.schema_path)
    tmp_manifest.replace(paths.manifest_path)
    tmp_validation.replace(paths.validation_path)
    tmp_complete.replace(paths.complete_path)
    for path in [paths.parquet_path, paths.schema_path, paths.manifest_path, paths.validation_path, paths.complete_path]:
        _set_file_private(path)
    return manifest


def load_shared_respondent_substrate(paths: SharedSubstratePaths) -> tuple[pd.DataFrame, dict[str, Any], dict[str, Any]]:
    if not paths.complete_path.exists():
        raise RuntimeError(f"shared respondent substrate COMPLETE marker missing: {paths.complete_path}")
    for path in [paths.parquet_path, paths.manifest_path, paths.validation_path, paths.schema_path]:
        if not path.exists():
            raise RuntimeError(f"shared respondent substrate artifact missing: {path}")
    manifest = json.loads(paths.manifest_path.read_text(encoding="utf-8"))
    validation = json.loads(paths.validation_path.read_text(encoding="utf-8"))
    if _file_sha256(paths.parquet_path) != _clean(manifest.get("parquet_file_sha256")):
        raise RuntimeError("shared respondent substrate parquet SHA mismatch")
    frame = pd.read_parquet(paths.parquet_path)
    current_validation = validate_shared_respondent_substrate(frame, manifest)
    if current_validation["validation_status"] != "pass":
        raise RuntimeError(f"shared respondent substrate validation failed: {current_validation['validation_message']}")
    if validation.get("validation_status") != "pass":
        raise RuntimeError("shared respondent substrate stored validation is not pass")
    return frame, manifest, current_validation


def shared_substrate_cache_signature_matches(manifest: dict[str, Any], expected: dict[str, Any]) -> bool:
    required_keys = [
        "schema_version",
        "execution_contract_version",
        "source",
        "canonical_wave",
        "country_code",
        "union_selection_hash",
        "response_semantics_contract_hash",
        "question_family_registry_hash",
        "joint_configuration_authority_release_id",
        "p3_authority_release_id",
        "respondent_relation_schema_hash",
    ]
    if manifest.get("validation_status") != "pass" or not manifest.get("cache_valid"):
        return False
    for key in required_keys:
        expected_value = _clean(expected.get(key))
        if expected_value and _clean(manifest.get(key)) != expected_value:
            return False
    return True
