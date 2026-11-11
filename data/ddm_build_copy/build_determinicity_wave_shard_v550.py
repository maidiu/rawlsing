#!/usr/bin/env python3
"""Build one V550 source/wave shard."""

from __future__ import annotations

import argparse
import faulthandler
import hashlib
import json
import os
import re
import sys
import time
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd
import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.build_response_option_map_v550 import build_response_option_map
from data.ddm_build_copy.build_source_structure_validator import canonical_wave_label
from data.ddm_build_copy.ddm_v550_family_overlay import canonical_family_key, canonical_wave_key, load_family_overlay, wave_aliases
from data.ddm_build_copy.build_determinicity_repository_v550 import (
    CHECKPOINT_COMPLETE_SUFFIX,
    CHECKPOINT_ROOT_NAME,
    CHECKPOINT_TABLE_DIR,
    _assert_facet_ready_view_contract,
    _assert_live_contracts,
    _build_question_list,
    _combine_wave_checkpoint_tables,
    _concat_frames,
    _finalize_wave_checkpoint_tables,
    _harmonize_question_frame,
    _load_response_option_map,
    _load_replayed_cloud_tables,
    _load_wave_question_mapping,
    _log_progress,
    _mark_question_complete,
    _question_checkpoint_exists,
    _question_key,
    _question_rows,
    _question_rows_from_cache,
    _prefetch_question_rows_by_country,
    _prepare_v550_question_row_cache,
    _question_checkpoint_complete_path,
    _question_checkpoint_path,
    _resolve_finalize_source,
    _summary_question_meta,
    _wave_report_dir,
    _wave_warning_report,
    _write_json_report,
    _write_question_checkpoint,
)
from data.ddm_build_copy.ddm_v550_bridge import build_bridge_causal_summary, build_bridge_lane_audits, write_v551_bridge_index_for_shard, validate_bridge_df
from data.ddm_build_copy.ddm_v550_manifest import build_shard_manifest
from data.ddm_build_copy.ddm_v550_process_guard import active_readiness_lock_for_shard
from data.ddm_build_copy.ddm_v550_readiness import build_readiness, load_scope_manifest
from data.ddm_build_copy.ddm_v550_source_structure import build_source_structure_population_audit, load_question_structure_register, match_source_structure_row, write_source_structure_population_audit
from data.ddm_build_copy.ddm_v550_source_structure import _normalized_join_key
from data.ddm_build_copy.ddm_v550_clouds import (
    BRANCH_POSITION_SIGNATURE_COLUMNS,
    BRANCH_RELATION_CO_SIGNATURE_COLUMNS,
    QUESTION_RESPONSE_ATTITUDE_CLOUD_COLUMNS,
    build_attitude_cloud_rows,
    build_co_signature_rows,
    build_position_signature_rows,
    reset_attitude_cloud_state,
    should_emit_cloud_tables,
)
from data.ddm_build_copy.ddm_v550_branching import (
    SECONDARY_INDICATOR_SUMMARY_COLUMNS,
    branch_nodes_rows,
    indicator_answer_matrix_rows,
    indicator_summary_rows,
    outlier_cohort_rows,
    prepare_question_frame,
    secondary_indicator_summary_rows,
)
from data.ddm_build_copy.ddm_v550_distributions import build_distribution_tables
from data.ddm_build_copy.ddm_v550_position_distribution import POSITION_DISTRIBUTION_COLUMNS, build_position_distribution_rows
from data.ddm_build_copy.ddm_v550_question_use import build_question_use_contract, build_question_use_contract_row
from data.ddm_build_copy.ddm_v550_response_options import build_response_option_map as build_response_option_map_live, normalize_response_code, response_semantics_contract_hash
from data.ddm_build_copy.ddm_v550_var_aliases import question_var_code_variants
from data.ddm_build_copy.ddm_v550_io import normalize_family
from data.ddm_build_copy.ddm_v550_schema import (
    BRANCH_CO_SIGNATURE_ARROW_SCHEMA,
    BRANCH_POSITION_SIGNATURE_ARROW_SCHEMA,
    BRANCH_RELATION_CO_SIGNATURE_ARROW_SCHEMA,
    V551_BRIDGE_INDEX_SCHEMA,
    forbidden_cloud_feature_row_count,
    validate_bridge_index,
    validate_columns,
    validate_no_forbidden_cloud_features,
    validate_shard_manifest,
)
from data.ddm_build_copy.ddm_v550_storage import V550ShardPaths, atomic_write_json, load_env_database_url, read_table_any, try_connect_database, write_table
from data.ddm_build_copy.ddm_v550_response_relation import (
    AUTO_RESPONSE_RELATION,
    load_scope_manifest_from_response_relation,
    resolve_response_relation,
)
from data.ddm_build_copy.ddm_v550_shared_respondent_substrate import (
    SHARED_SUBSTRATE_EXECUTION_CONTRACT_VERSION,
    SHARED_SUBSTRATE_SCHEMA_VERSION,
    canonicalize_shared_respondent_substrate,
    resolve_shared_substrate_requirements,
    shared_substrate_paths,
    write_shared_respondent_substrate_atomic,
)
from data.ddm_build_copy.ddm_v550_validation import validate_attitude_cloud_rows, validate_position_signature_rows, validate_relation_signature_rows, validate_v551_bridge_rows
from data.ddm_build_copy.ddm_v550_shards import shard_id_for
from data.ddm_build_copy.ddm_v550_support import DEFAULT_SUPPORT_CAP


def _semantic_clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    text = str(value).strip()
    return "" if text.lower() in {"nan", "none"} else text


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _build_authority_receipt(args: argparse.Namespace, question_relation_authority: Any, response_map: pd.DataFrame) -> dict[str, Any]:
    """Record authority decisions made by the real V550 builder."""
    overlay_specs = {
        "first_pass_authority": args.first_pass_authority_dir,
        "semantic_authority": args.semantic_authority_dir,
        "position_conditioning": args.position_conditioning_authority_dir,
        "directionality": args.directionality_authority_dir,
    }
    overlays: dict[str, dict[str, Any]] = {}
    for overlay_type, directory in overlay_specs.items():
        loaded = load_family_overlay(
            args.source,
            args.canonical_wave or args.wave,
            overlay_type,
            required=False,
            search_roots=[Path(directory)] if directory else None,
        )
        detail: dict[str, Any] = {
            "status": loaded.status,
            "path": loaded.path or "",
            "row_count": int(loaded.row_count or 0),
            "columns": list(loaded.columns or []),
            "message": loaded.message or "",
        }
        if loaded.path and Path(loaded.path).is_file():
            detail["sha256"] = _file_sha256(Path(loaded.path))
        overlays[overlay_type] = detail
    response_map_path = Path(args.response_option_map) if args.response_option_map else None
    return {
        "authority_resolution_owner": "v550_shard_builder",
        "source": args.source,
        "wave": args.wave,
        "canonical_wave": args.canonical_wave or args.wave,
        "question_relation_authority": {
            "path": str(question_relation_authority.path),
            "sha256": question_relation_authority.file_sha256,
            "row_count": len(question_relation_authority.rows),
        },
        "overlays": overlays,
        "response_option_map": {
            "path": str(response_map_path) if response_map_path else "built_by_v550",
            "sha256": _file_sha256(response_map_path) if response_map_path and response_map_path.is_file() else "",
            "row_count": int(len(response_map)),
        },
    }


def _ordered_semantic_variants(values: list[Any], *, identifier: bool = False) -> list[str]:
    out: list[str] = []
    for value in values:
        cleaned = _semantic_clean(value)
        if not cleaned:
            continue
        candidates = [cleaned]
        if identifier:
            normalized = _normalized_join_key(cleaned)
            if normalized:
                candidates.append(normalized)
        for candidate in candidates:
            candidate = _semantic_clean(candidate)
            if candidate and candidate not in out:
                out.append(candidate)
    return out


def _sign_safe_response_value_variants(*values: Any) -> list[str]:
    """Normalize numeric response codes without erasing their sign.

    Generic identifier normalization is intentionally forbidden here: `-1`
    and `1` are distinct response codes even though punctuation-stripping join
    helpers collapse both to `1`.
    """
    out: list[str] = []
    for value in values:
        cleaned = _semantic_clean(value)
        if not cleaned:
            continue
        normalized = normalize_response_code(cleaned)
        for candidate in [cleaned, normalized]:
            candidate = _semantic_clean(candidate)
            if candidate and candidate not in out:
                out.append(candidate)
    return out


def _ascii_fold(value: Any) -> str:
    text = unicodedata.normalize("NFKD", _semantic_clean(value))
    return "".join(ch for ch in text if not unicodedata.combining(ch))


@lru_cache(maxsize=16384)
def _source_identity_variants_cached(raw_value: str) -> tuple[str, ...]:
    """Return fail-closed family tokens for governed source matching.

    Authority maps often carry source-native labels such as
    ``Latinobarómetro 1995`` or long WVS/EVS integrated-file names.  These are
    still scoped to one family, but direct equality with the requested family
    label is too narrow.  The variants here intentionally strip wave/year
    decoration only for source-family matching; wave matching remains a
    separate required gate.
    """
    raw = _semantic_clean(raw_value)
    if not raw:
        return ()
    folded = _ascii_fold(raw)
    candidates = [raw, folded, normalize_family(raw), canonical_family_key(raw)]

    stripped = re.sub(r"\([^)]*\)", " ", folded)
    stripped = re.sub(r"\b(?:19|20)\d{2}(?:\s*[-/]\s*(?:19|20)\d{2})?\b", " ", stripped)
    stripped = re.sub(r"\bwave\s*(?:[ivxlcdm]+|\d+)\b", " ", stripped, flags=re.IGNORECASE)
    stripped = re.sub(r"\bround\s*(?:[ivxlcdm]+|\d+)\b", " ", stripped, flags=re.IGNORECASE)
    stripped = re.sub(r"\b(?:integrated|file|survey|study|values|world|european|life|transition)\b", " ", stripped, flags=re.IGNORECASE)
    candidates.extend([stripped, normalize_family(stripped), canonical_family_key(stripped)])

    out = {_normalized_join_key(candidate) for candidate in candidates if _semantic_clean(candidate)}
    out.discard("")
    return tuple(sorted(out))


def _source_identity_variants(value: Any) -> set[str]:
    return set(_source_identity_variants_cached(_semantic_clean(value)))


@lru_cache(maxsize=32768)
def _wave_identity_variants_cached(source: str, values_key: tuple[str, ...]) -> tuple[str, ...]:
    tokens: list[Any] = []
    family_key = canonical_family_key(source)
    for value in values_key:
        cleaned = _semantic_clean(value)
        if not cleaned:
            continue
        tokens.append(cleaned)
        tokens.append(canonical_wave_key(source, cleaned))
        tokens.extend(wave_aliases(source, cleaned))
        if family_key == "wvs":
            wvs_year_by_wave = {"W1": "1981", "W2": "1990", "W3": "1995", "W4": "2000", "W5": "2005", "W6": "2010", "W7": "2017"}
            canonical = canonical_wave_key(source, cleaned)
            if canonical in wvs_year_by_wave:
                tokens.append(wvs_year_by_wave[canonical])
            reverse = {year: wave for wave, year in wvs_year_by_wave.items()}
            if cleaned in reverse:
                tokens.append(reverse[cleaned])
    out = {_normalized_join_key(token) for token in tokens if _semantic_clean(token)}
    out.discard("")
    return tuple(sorted(out))


def _wave_identity_variants(source: str, *values: Any) -> set[str]:
    return set(_wave_identity_variants_cached(_semantic_clean(source), tuple(_semantic_clean(value) for value in values)))


def _terminal_identifier_token(value: Any) -> str:
    text = _ascii_fold(value).strip()
    if not text:
        return ""
    parts = [part for part in re.split(r"[:/|.\\\s]+", text) if part.strip()]
    return parts[-1] if parts else text


@lru_cache(maxsize=262144)
def _identifier_tokens_cached(value: str, source: str, wave: str, exact: bool) -> tuple[str, ...]:
    cleaned = _semantic_clean(value)
    if not cleaned:
        return ()
    variants: list[Any] = [cleaned, cleaned.lower(), cleaned.upper(), _ascii_fold(cleaned)]
    if not exact:
        variants.append(_terminal_identifier_token(cleaned))
    if source and wave:
        for variant in list(variants):
            variants.extend(question_var_code_variants(source, wave, variant))
    out = {_normalized_join_key(variant) for variant in variants if _semantic_clean(variant)}
    out.discard("")
    return tuple(sorted(out))


def _identifier_tokens(value: Any, *, source: str = "", wave: str = "") -> set[str]:
    return set(_identifier_tokens_cached(_semantic_clean(value), _semantic_clean(source), _semantic_clean(wave), False))


def _exact_identifier_tokens(value: Any, *, source: str = "", wave: str = "") -> set[str]:
    return set(_identifier_tokens_cached(_semantic_clean(value), _semantic_clean(source), _semantic_clean(wave), True))


def _row_identity_tokens(row: pd.Series, columns: list[str], *, source: str = "", wave: str = "", exact: bool = False) -> dict[str, set[str]]:
    token_func = _exact_identifier_tokens if exact else _identifier_tokens
    return {column: token_func(row.get(column), source=source, wave=wave) for column in columns}


def _response_value_identity(row: pd.Series) -> str:
    for column in ("value_code_normalized", "value_code_raw", "response_value_normalized", "response_value", "value_label_clean", "normalized_response_label"):
        token = _semantic_clean(row.get(column))
        if token:
            return normalize_response_code(token) or token
    return ""


def _semantic_signature(row: pd.Series) -> tuple[str, ...]:
    columns = [
        "response_semantics_status",
        "response_direction",
        "polarity",
        "response_intensity",
        "ordinal_rank",
        "directionality_status",
        "option_group",
        "is_substantive",
        "is_missing",
        "is_dk",
        "is_refusal",
        "is_iap",
    ]
    return tuple(_semantic_clean(row.get(column)) for column in columns)


def _authority_identity_signature(row: pd.Series) -> tuple[str, str, str, str]:
    return tuple(_semantic_clean(row.get(column)) for column in ("question_id", "item_id", "var_code", "var_name"))


def _fallback_candidates_are_coherent(frame: pd.DataFrame) -> bool:
    if frame.empty:
        return False
    for _, group in frame.groupby(frame.apply(_response_value_identity, axis=1), dropna=False):
        signatures = {_semantic_signature(row) for _, row in group.iterrows()}
        if len(signatures) > 1:
            return False
    return True


def _coerce_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    text = _semantic_clean(value).lower()
    return text in {"1", "true", "t", "yes", "y", "certified", "allowed"}


def _response_authority_requirement(row: pd.Series) -> tuple[bool, str]:
    semantic_role = _semantic_clean(row.get("semantic_role")).lower()
    topology = _semantic_clean(row.get("response_topology") or row.get("question_type")).lower()
    classification = _semantic_clean(row.get("source_structure_classification")).lower()
    mapping_status = _semantic_clean(row.get("mapping_status")).lower()
    disallowed = _semantic_clean(row.get("disallowed_reason")).lower()
    administrative_tokens = ("admin", "metadata", "weight", "identifier", "context", "sampling", "processing")
    if any(token in "|".join([semantic_role, topology, classification, mapping_status, disallowed]) for token in administrative_tokens):
        return False, "governed_response_semantics_inapplicable_administrative_context_or_weight"
    if _coerce_bool(row.get("allowed_as_v551_relation_evidence")):
        return True, "allowed_as_v551_relation_evidence"
    if _coerce_bool(row.get("current_directional_atom_eligible")):
        return True, "current_directional_atom_eligible"
    if _coerce_bool(row.get("future_evidence_eligible")) or _coerce_bool(row.get("future_topology_evidence_eligible")):
        return True, "future_response_evidence_eligible"
    if _coerce_bool(row.get("allowed_as_response_distribution")) and topology not in {"", "administrative", "metadata", "context_only", "open_text"}:
        return True, "substantive_response_distribution"
    if semantic_role in {"relation_evidence", "substantive_evidence", "subjective_evidence"}:
        return True, "substantive_semantic_role"
    return False, "governed_response_semantics_not_required"


def _response_map_matches_for_question(scoped_response_map: pd.DataFrame, row: pd.Series) -> pd.DataFrame:
    if scoped_response_map.empty:
        return scoped_response_map
    qid = _semantic_clean(row.get("question_id"))
    var_code = _semantic_clean(row.get("var_code"))
    mask = pd.Series(False, index=scoped_response_map.index)
    if qid and "v550_response_map_live_question_id" in scoped_response_map.columns:
        mask |= scoped_response_map["v550_response_map_live_question_id"].fillna("").astype(str).eq(qid)
    if var_code and "v550_response_map_live_var_code" in scoped_response_map.columns:
        mask |= scoped_response_map["v550_response_map_live_var_code"].fillna("").astype(str).eq(var_code)
    return scoped_response_map.loc[mask].copy()


def build_response_authority_match_audit(wave_question_rows: pd.DataFrame, scoped_response_map: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for _, qrow in wave_question_rows.iterrows():
        matches = _response_map_matches_for_question(scoped_response_map, qrow)
        required, reason = _response_authority_requirement(qrow)
        values = matches.apply(_response_value_identity, axis=1).dropna().astype(str).tolist() if not matches.empty else []
        substantive = int(matches.get("is_substantive", pd.Series(dtype=bool)).map(_coerce_bool).sum()) if not matches.empty and "is_substantive" in matches.columns else 0
        special_cols = [c for c in ("is_missing", "is_dk", "is_refusal", "is_no_answer", "is_iap", "is_skipped", "is_not_available", "is_not_asked", "is_inapplicable") if c in matches.columns]
        special = 0
        if special_cols and not matches.empty:
            special = int(matches[special_cols].apply(lambda col: col.map(_coerce_bool)).any(axis=1).sum())
        cardinality = len(set(v for v in values if v))
        topology = _semantic_clean(qrow.get("response_topology") or qrow.get("question_type")).lower()
        admin = not required and _response_authority_requirement(qrow)[1] == "governed_response_semantics_inapplicable_administrative_context_or_weight"
        high_cardinality = cardinality > 50
        blocked = required and matches.empty
        rows.append({
            "source": _semantic_clean(qrow.get("source")),
            "wave": _semantic_clean(qrow.get("wave")),
            "canonical_wave": _semantic_clean(qrow.get("canonical_wave")),
            "country_code": _semantic_clean(qrow.get("country_code")),
            "question_id": _semantic_clean(qrow.get("question_id")),
            "item_id": _semantic_clean(qrow.get("item_id")),
            "var_code": _semantic_clean(qrow.get("var_code")),
            "var_name": _semantic_clean(qrow.get("var_name")),
            "response_authority_required": required,
            "governing_reason": reason,
            "response_map_match_count": int(len(matches)),
            "match_basis": ";".join(sorted(matches.get("v550_response_map_match_basis", pd.Series(dtype=str)).dropna().astype(str).unique())),
            "effective_response_map_row_count": int(len(matches)),
            "substantive_response_row_count": substantive,
            "special_missing_response_row_count": special,
            "distinct_normalized_response_values": cardinality,
            "administrative_or_contextual": admin,
            "high_cardinality_warning": high_cardinality,
            "high_cardinality_disposition": "allowed_administrative_or_contextual" if high_cardinality and admin else ("review_substantive_high_cardinality" if high_cardinality else ""),
            "disposition": "blocked_missing_required_response_authority" if blocked else ("accepted_matched" if not matches.empty else "accepted_governed_inapplicable"),
        })
    return pd.DataFrame(rows)


def assert_response_authority_match_gate(audit: pd.DataFrame) -> None:
    blocked = audit[audit["disposition"].eq("blocked_missing_required_response_authority")] if not audit.empty else audit
    if not blocked.empty:
        sample = blocked[["question_id", "var_code", "governing_reason"]].head(10).to_dict(orient="records")
        raise RuntimeError(f"[V550_REQUIRED_RESPONSE_AUTHORITY_MISSING] {len(blocked)} selected questions require response-option authority but did not match: {sample}")


def _lookup_response_semantics_sign_safe(response_map: pd.DataFrame) -> dict[tuple[str, str, str, str], dict[str, Any]]:
    """Build symmetric family/wave/variable keys while preserving response signs."""
    lookup: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    if response_map.empty:
        return lookup
    for row in response_map.itertuples(index=False):
        row_dict = row._asdict()
        source_label = _semantic_clean(row_dict.get("source_family")) or _semantic_clean(row_dict.get("source"))
        normalized_family = normalize_family(source_label)
        canonical_family = canonical_family_key(source_label)
        source_variants = _ordered_semantic_variants(
            [source_label, normalized_family, canonical_family, canonical_family_key(normalized_family or source_label or canonical_family)],
            identifier=True,
        )

        raw_wave = _semantic_clean(row_dict.get("wave"))
        canonical_wave = _semantic_clean(row_dict.get("canonical_wave"))
        wave_tokens: list[Any] = [raw_wave, canonical_wave]
        for token in [raw_wave, canonical_wave]:
            if not token:
                continue
            wave_tokens.extend([
                canonical_wave_key(normalized_family or source_label or canonical_family, token),
                *wave_aliases(normalized_family or source_label or canonical_family, token),
            ])
        wave_variants = _ordered_semantic_variants(wave_tokens, identifier=True)

        var_name = (
            _semantic_clean(row_dict.get("var_name"))
            or _semantic_clean(row_dict.get("var_code"))
            or _semantic_clean(row_dict.get("question_id"))
            or _semantic_clean(row_dict.get("variable_id"))
        )
        alias_values: list[Any] = [var_name, var_name.lower(), var_name.upper()]
        for wave_variant in wave_variants or [raw_wave, canonical_wave]:
            alias_values.extend(question_var_code_variants(source_label, wave_variant, var_name))
        var_variants = _ordered_semantic_variants(alias_values, identifier=True)

        value_variants = _sign_safe_response_value_variants(
            row_dict.get("value_code_normalized"),
            row_dict.get("value_code"),
            row_dict.get("response_value_normalized"),
            row_dict.get("value_label_clean"),
            row_dict.get("response_label"),
            row_dict.get("normalized_response_label"),
        )
        for source_variant in source_variants:
            for wave_variant in wave_variants:
                for var_variant in var_variants:
                    for value_variant in value_variants:
                        key = (source_variant, wave_variant, var_variant, value_variant)
                        existing = lookup.get(key)
                        if existing is None:
                            lookup[key] = row_dict
                            continue
                        existing_status = _semantic_clean(existing.get("response_semantics_status")).lower()
                        candidate_status = _semantic_clean(row_dict.get("response_semantics_status")).lower()
                        if existing_status in {"", "observed_only"} and candidate_status not in {"", "observed_only"}:
                            lookup[key] = row_dict
    return lookup

DEFAULT_ENV_FILE = ROOT / ".env"
DEFAULT_RESPONDENT_SCHEMA = ROOT / "data" / "ddm_build_copy" / "reports" / "respondent_wave_schema_template.csv"
DEFAULT_REPORTS_DIR = ROOT / "data" / "ddm_build_copy" / "reports"
DEFAULT_DIRECTIONALITY_AUTHORITY_DIR = ROOT / "data" / "ddm_build_copy" / "directionality_authority"
DEFAULT_READINESS_ROOT = ROOT / "data" / "ddm_repository_copy" / "v550" / "readiness_checks"
DEFAULT_VALIDATION_ROOT = ROOT / "data" / "ddm_repository_copy" / "v550" / "validation"
BRIDGE_AUDIT_MAX_ROWS = 250_000
PIPELINE_PROCESS_TOTAL = 51
PIPELINE_PROCESS_LABELS = {
    "question_universe": 32,
    "answer_distribution": 33,
    "country_answer_distribution": 34,
    "position_indicator_summary": 35,
    "indicator_answer_matrix": 36,
    "outlier_cohort_summary": 37,
    "secondary_indicator_summary": 38,
    "recursive_branch_nodes": 39,
    "branch_position_signature": 40,
    "branch_relation_co_signature": 41,
    "branch_co_signature": 42,
    "question_response_attitude_cloud": 43,
    "mapping_gap_report": 44,
    "response_option_manual_review": 45,
    "cloud_exclusion_audit": 46,
    "scope_manifest": 47,
    "substrate_readiness": 48,
    "position_field_coverage": 49,
    "weight_coverage": 50,
    "mapping_status_coverage": 51,
    "legacy_leak_report": 52,
    "underpowered_quarantine": 53,
}



def _filter_response_map_for_wave(
    response_map: pd.DataFrame,
    wave_question_rows: pd.DataFrame,
    *,
    source: str,
    wave: str,
    canonical_wave: str,
) -> pd.DataFrame:
    """Materialize the exact response-semantics contract consumed by this shard.

    The governed master map can span many surveys and waves.  Downstream V550J
    and V551 must consume the same source/wave/question slice V550 used rather
    than independently rebuilding or re-filtering authority.
    """
    if response_map is None or response_map.empty:
        return pd.DataFrame(columns=list(response_map.columns) if response_map is not None else [])

    frame = response_map.copy()
    source_columns = [c for c in ("source_family", "source", "survey_family") if c in frame.columns]
    wave_columns = [c for c in ("canonical_wave", "wave", "wave_id") if c in frame.columns]
    authority_identity_columns = [c for c in ("question_id", "item_id", "var_code", "var_name", "variable_id", "canonical_var_code") if c in frame.columns]
    live_identity_columns = [c for c in ("question_id", "item_id", "var_code", "var_name", "variable_id", "canonical_var_code") if c in wave_question_rows.columns]

    family_tokens = _source_identity_variants(source)
    wave_tokens = _wave_identity_variants(source, wave, canonical_wave)

    source_mask = pd.Series(True, index=frame.index)
    if source_columns and family_tokens:
        source_mask = pd.Series(False, index=frame.index)
        for column in source_columns:
            source_mask |= frame[column].map(lambda value: bool(_source_identity_variants(value) & family_tokens))

    wave_mask = pd.Series(True, index=frame.index)
    if wave_columns and wave_tokens:
        wave_mask = pd.Series(False, index=frame.index)
        for column in wave_columns:
            wave_mask |= frame[column].map(lambda value: bool(_wave_identity_variants(source, value) & wave_tokens))

    scoped = frame.loc[source_mask & wave_mask].copy()
    if scoped.empty or not authority_identity_columns or not live_identity_columns:
        filtered = scoped
    else:
        selected_parts: list[pd.DataFrame] = []
        precedence = [
            ("question_id", False),
            ("item_id", False),
            ("var_code", False),
            ("var_name", False),
            ("governed_normalized_terminal", True),
        ]
        authority_token_cache: dict[tuple[str, bool], pd.Series] = {}
        for column in authority_identity_columns:
            authority_token_cache[(column, False)] = scoped[column].map(lambda value: _identifier_tokens(value, source=source, wave=canonical_wave))
            authority_token_cache[(column, True)] = scoped[column].map(lambda value: _exact_identifier_tokens(value, source=source, wave=canonical_wave))

        for _, live_row in wave_question_rows.iterrows():
            live_tokens_by_column = _row_identity_tokens(live_row, live_identity_columns, source=source, wave=canonical_wave, exact=False)
            live_exact_tokens_by_column = _row_identity_tokens(live_row, live_identity_columns, source=source, wave=canonical_wave, exact=True)
            accepted: pd.DataFrame | None = None
            accepted_basis = ""
            for basis, fallback in precedence:
                candidate_mask = pd.Series(False, index=scoped.index)
                basis_columns = authority_identity_columns if fallback else [basis] if basis in authority_identity_columns and basis in live_tokens_by_column else []
                for column in basis_columns:
                    live_tokens: set[str]
                    if fallback:
                        live_tokens = set().union(*(tokens for tokens in live_tokens_by_column.values()))
                        authority_tokens = authority_token_cache[(column, False)]
                    else:
                        live_tokens = live_exact_tokens_by_column.get(column, set())
                        authority_tokens = authority_token_cache[(column, True)]
                    if not live_tokens:
                        continue
                    candidate_mask |= authority_tokens.map(lambda tokens: bool(tokens & live_tokens))
                candidates = scoped.loc[candidate_mask].copy()
                if candidates.empty:
                    continue
                if fallback:
                    identity_signatures = {_authority_identity_signature(row) for _, row in candidates.iterrows()}
                    if len(identity_signatures) > 1 and not _fallback_candidates_are_coherent(candidates):
                        live_label = _semantic_clean(live_row.get("question_id")) or _semantic_clean(live_row.get("var_code")) or _semantic_clean(live_row.get("var_name"))
                        raise RuntimeError(
                            "[AMBIGUOUS_RESPONSE_OPTION_AUTHORITY_MATCH] "
                            f"{source}/{wave} selected question {live_label} matched conflicting fallback identities: "
                            f"{sorted(identity_signatures)[:10]}"
                        )
                    deduped_rows: list[pd.Series] = []
                    for _, group in candidates.groupby(
                        candidates.apply(lambda row: (_response_value_identity(row), _semantic_signature(row)), axis=1),
                        sort=False,
                    ):
                        row = group.iloc[0].copy()
                        row["v550_response_map_fallback_provenance_identities"] = json.dumps(
                            sorted({_authority_identity_signature(grow) for _, grow in group.iterrows()}),
                            ensure_ascii=False,
                            default=str,
                        )
                        row["v550_response_map_fallback_duplicate_count"] = int(len(group))
                        deduped_rows.append(row)
                    candidates = pd.DataFrame(deduped_rows, columns=list(candidates.columns) + [
                        "v550_response_map_fallback_provenance_identities",
                        "v550_response_map_fallback_duplicate_count",
                    ]).copy()
                accepted = candidates
                accepted_basis = basis
                break
            if accepted is not None and not accepted.empty:
                accepted["v550_response_map_match_basis"] = accepted_basis
                accepted["v550_response_map_live_question_id"] = _semantic_clean(live_row.get("question_id"))
                accepted["v550_response_map_live_var_code"] = _semantic_clean(live_row.get("var_code"))
                selected_parts.append(accepted)
        if selected_parts:
            filtered = pd.concat(selected_parts, ignore_index=False).drop_duplicates().copy()
        else:
            filtered = scoped.iloc[0:0].copy()

    sort_columns = [c for c in ("source_family", "source", "canonical_wave", "wave", "var_code", "var_name", "response_value_normalized", "response_value") if c in filtered.columns]
    if sort_columns:
        filtered = filtered.sort_values(sort_columns, kind="mergesort").reset_index(drop=True)
    return filtered

def _process_label(table_name: str) -> str:
    idx = PIPELINE_PROCESS_LABELS.get(table_name)
    return f" ({idx}/{PIPELINE_PROCESS_TOTAL})" if idx else ""


def _missing_question_checkpoint_keys(shard_paths: V550ShardPaths, question_rows: pd.DataFrame) -> list[str]:
    missing: list[str] = []
    for idx, row in enumerate(question_rows.itertuples(index=False), start=1):
        qrow = pd.Series(row._asdict())
        if not _question_checkpoint_exists(shard_paths, idx, qrow):
            missing.append(_question_key(qrow))
    return missing


def _to_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)) and not pd.isna(value):
        return value != 0
    text = str(value).strip().lower()
    if text in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "f", "no", "n", "off", "", "nan", "none"}:
        return False
    return default


def _slugify(value: str) -> str:
    out = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in str(value))
    out = out.strip("_")
    return out or "item"


def _dedupe_nonblank(values: list[Any]) -> list[str]:
    out: list[str] = []
    for value in values:
        text = _semantic_clean(value)
        if text and text not in out:
            out.append(text)
    return out


def _load_question_filter(path: str | None) -> list[str]:
    """Load requested identifiers without destroying case or punctuation."""
    if not path:
        return []
    filter_path = Path(path)
    if not filter_path.exists():
        raise FileNotFoundError(filter_path)
    values: list[Any]
    if filter_path.suffix.lower() == ".json":
        payload = json.loads(filter_path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            values = payload.get("question_ids") or payload.get("var_codes") or payload.get("selected_question_ids") or []
        else:
            values = payload if isinstance(payload, list) else []
    elif filter_path.suffix.lower() == ".csv":
        df = pd.read_csv(filter_path)
        values = []
        for candidate in ["question_id", "var_code", "variable_id", "question_name", "name"]:
            if candidate in df.columns:
                values = df[candidate].dropna().astype(str).tolist()
                break
    else:
        values = [
            line for line in filter_path.read_text(encoding="utf-8").splitlines()
            if _semantic_clean(line) and not _semantic_clean(line).startswith("#")
        ]
    return _dedupe_nonblank(values)


def _question_filter_candidate_names(frame: pd.DataFrame, indexes: list[Any], columns: list[str]) -> list[str]:
    names: list[str] = []
    for idx in indexes:
        row = frame.loc[idx]
        for column in columns:
            value = _semantic_clean(row.get(column))
            if value and value not in names:
                names.append(value)
    return names


def _question_filter_token_variants(token: str, source: str = "", wave: str = "") -> list[str]:
    variants = [token]
    if source and wave:
        variants.extend(question_var_code_variants(source, wave, token))
    out: list[str] = []
    for value in variants:
        cleaned = _semantic_clean(value)
        if cleaned and cleaned not in out:
            out.append(cleaned)
    return out


def _apply_question_filter_exact_first(
    mapping: pd.DataFrame,
    requested: list[str],
    *,
    source: str = "",
    wave: str = "",
) -> pd.DataFrame:
    """Resolve each filter token exactly first; unique normalized fallback only.

    This prevents legitimate identifiers such as ``Duration1`` and ``DURATION1``
    from collapsing into one request. Missing and ambiguous filters fail closed;
    full-wave fallback is forbidden.
    """
    if not requested:
        return mapping
    filter_cols = [
        col for col in ["question_id", "var_code", "variable_id", "question_name", "name"]
        if col in mapping.columns
    ]
    if not filter_cols:
        raise RuntimeError("question filter supplied but no recognizable question columns were present")
    selected_indexes: list[Any] = []
    for token in requested:
        token_variants = _question_filter_token_variants(token, source, wave)
        exact_mask = pd.Series(False, index=mapping.index)
        for variant in token_variants:
            for column in filter_cols:
                exact_mask |= mapping[column].fillna("").astype(str).str.strip().eq(variant)
        exact_indexes = mapping.index[exact_mask].tolist()
        if exact_indexes:
            if len(exact_indexes) != 1:
                candidates = _question_filter_candidate_names(mapping, exact_indexes, filter_cols)
                raise RuntimeError(
                    f"ambiguous exact question filter match for identifier={token}: candidates={candidates}"
                )
            selected_indexes.append(exact_indexes[0])
            continue

        normalized_mask = pd.Series(False, index=mapping.index)
        for variant in token_variants:
            normalized_token = _normalized_join_key(variant)
            for column in filter_cols:
                normalized_mask |= mapping[column].fillna("").astype(str).map(_normalized_join_key).eq(normalized_token)
        fallback_indexes = mapping.index[normalized_mask].tolist()
        if not fallback_indexes:
            raise RuntimeError(f"question filter identifier not found: {token}")
        if len(fallback_indexes) != 1:
            candidates = _question_filter_candidate_names(mapping, fallback_indexes, filter_cols)
            raise RuntimeError(
                f"ambiguous normalized question filter match for identifier={token}: candidates={candidates}"
            )
        selected_indexes.append(fallback_indexes[0])

    if len(set(selected_indexes)) != len(requested):
        raise RuntimeError(
            f"question filter identifiers did not resolve one-to-one: requested={requested} indexes={selected_indexes}"
        )
    return mapping.loc[selected_indexes].copy()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build one V550 source/wave shard. This is the production shard runner.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--shard-id", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--wave", required=True)
    parser.add_argument("--canonical-wave", default=None)
    parser.add_argument("--country", action="append", default=[])
    parser.add_argument("--db-url", default=None)
    parser.add_argument("--authority-root", default=os.getenv("DDM_AUTHORITY_ROOT", ""), help="Installed authority root containing bindings/ and reports/.")
    parser.add_argument("--env-file", default=str(DEFAULT_ENV_FILE))
    parser.add_argument(
        "--response-long-relation",
        default=os.environ.get("DDM_RESPONSE_LONG_RELATION", AUTO_RESPONSE_RELATION),
        help="Respondent-long view to consume. Use auto to prefer the authority-enriched view when present.",
    )
    parser.add_argument("--response-option-map", default=None)
    parser.add_argument("--respondent-schema-template", default=str(DEFAULT_RESPONDENT_SCHEMA))
    parser.add_argument("--output-root", default=str(ROOT / "data" / "ddm_repository_copy" / "v550"))
    parser.add_argument("--reports-dir", default=str(DEFAULT_REPORTS_DIR))
    parser.add_argument("--min-cell-n", type=int, default=50)
    parser.add_argument("--min-branch-n", type=int, default=DEFAULT_SUPPORT_CAP)
    parser.add_argument("--min-answer-n", type=int, default=DEFAULT_SUPPORT_CAP)
    parser.add_argument("--max-depth", type=int, default=3)
    parser.add_argument(
        "--cloud-mode",
        default="auto",
        choices=("auto", "full", "off", "share"),
        help="How to emit cloud tables. 'auto' preserves the current threshold, 'full' always emits, 'off' never emits, 'share' uses a wave-respondent share gate.",
    )
    parser.add_argument(
        "--cloud-max-branch-rows",
        type=int,
        default=1000,
        help="Maximum branch-frame rows allowed for cloud emission in auto/share mode.",
    )
    parser.add_argument(
        "--cloud-max-branch-share",
        type=float,
        default=None,
        help="Optional wave-respondent share threshold for cloud emission in share mode.",
    )
    parser.add_argument("--limit-questions", type=int, default=None)
    parser.add_argument(
        "--question-filter-file",
        default=None,
        help="Optional JSON/CSV/text file listing question_ids/var_codes to retain for a micro-slice run.",
    )
    parser.add_argument("--resume", action="store_true")
    parser.add_argument(
        "--resume-from-checkpoints-only",
        action="store_true",
        help="When resuming, verify that every per-question checkpoint already exists and skip the per-question execution loop entirely, finalizing directly from checkpoints.",
    )
    parser.add_argument(
        "--v550-prepared-substrate-mode",
        default="off",
        choices=("off", "country", "chunked"),
        help="Pre-harmonize the shared question cache once per country or in chunks before the question loop. 'off' preserves the legacy hot path.",
    )
    parser.add_argument(
        "--shared-respondent-substrate-mode",
        default="off",
        choices=("off", "write"),
        help="Write a permission-restricted shared V550/V550J respondent substrate from the one-query V550 extraction cache.",
    )
    parser.add_argument(
        "--joint-configuration-registry-path",
        default=None,
        help="Bounded V550J registry used to extend the V550 extraction set with joint-required variables.",
    )
    parser.add_argument(
        "--joint-configuration-id",
        action="append",
        default=[],
        help="Optional joint configuration id filter; may be repeated.",
    )
    parser.add_argument(
        "--finalize-source",
        default="auto",
        choices=("auto", "memory", "checkpoint"),
        help="How to finalize wave tables: 'auto' uses memory on fresh runs and checkpoint reloads on resume, 'memory' never reloads final tables from disk, and 'checkpoint' always reloads final tables from disk.",
    )
    parser.add_argument("--overwrite-shard", action="store_true")
    parser.add_argument(
        "--full-readiness",
        action="store_true",
        default=False,
        help="Compute the full readiness/coverage payload before question processing. Disabled by default so shards can start quickly.",
    )
    parser.add_argument(
        "--readiness-only",
        action="store_true",
        default=False,
        help="Build and write readiness artifacts, then exit before question processing.",
    )
    parser.add_argument(
        "--readiness-artifact",
        default=None,
        help="Path to a previously written readiness artifact directory to reuse instead of recomputing readiness.",
    )
    parser.add_argument(
        "--first-pass-authority-dir",
        default=str(ROOT / "data" / "ddm_build_copy" / "reports"),
        help="Directory containing family/wave first-pass authority tables.",
    )
    parser.add_argument(
        "--semantic-authority-dir",
        default=str(ROOT / "data" / "ddm_build_copy" / "reports"),
        help="Directory containing family/wave semantic authority overlays.",
    )
    parser.add_argument(
        "--position-conditioning-authority-dir",
        default=str(ROOT / "data" / "ddm_build_copy" / "reports"),
        help="Directory containing family/wave position-conditioning authority overlays.",
    )
    parser.add_argument(
        "--directionality-authority-dir",
        default=str(DEFAULT_DIRECTIONALITY_AUTHORITY_DIR),
        help="Directory containing directionality authority CSVs. If present, authority files are preferred over legacy overlays.",
    )
    parser.add_argument(
        "--allow-launch-ready-fallback",
        action="store_true",
        default=False,
        help="Allow the lightweight launch-ready fallback when no readiness artifact is supplied. Disabled by default for promotion safety.",
    )
    parser.add_argument(
        "--readiness-output-root",
        default=str(ROOT / "data" / "ddm_repository_copy" / "v550" / "readiness_checks"),
        help="Root directory where readiness-only artifacts should be written.",
    )
    parser.add_argument("--write-csv", action="store_true", default=True)
    parser.add_argument("--no-write-csv", dest="write_csv", action="store_false")
    parser.add_argument("--write-parquet", action="store_true", default=True)
    parser.add_argument("--no-write-parquet", dest="write_parquet", action="store_false")
    parser.add_argument("--write-postgres", action="store_true", default=False)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument(
        "--traceback-timeout-seconds",
        type=float,
        default=0.0,
        help="If set above zero, dump a traceback when verbose execution stays in one frame longer than this many seconds.",
    )
    parser.add_argument(
        "--stop-after-stage",
        type=int,
        default=0,
        help="Stop after the requested pipeline stage. Currently only stage 4 is supported, which exits after question processing and before combining checkpoint tables.",
    )
    return parser.parse_args()


def _require_readiness_artifact(args: argparse.Namespace) -> None:
    if args.readiness_artifact or args.full_readiness or args.readiness_only or args.allow_launch_ready_fallback:
        return
    raise SystemExit(
        "This shard runner now requires explicit readiness input. Provide --readiness-artifact, "
        "--full-readiness, or --readiness-only. Use --allow-launch-ready-fallback only for exploratory runs."
    )


def _launch_readiness_from_scope(scope_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    readiness = scope_df.copy()
    if readiness.empty:
        empty = pd.DataFrame(columns=["source", "wave", "country_code"])
        return empty, empty, empty, empty, empty, empty
    readiness["readiness_status"] = "launchable_scope"
    readiness["weight_status"] = "unknown"
    readiness["position_status"] = "unknown"
    readiness["mapped_rows"] = 0
    readiness["weight_rows"] = 0
    readiness["legacy_leak_rows"] = 0
    empty = pd.DataFrame(columns=readiness.columns)
    return readiness, empty.copy(), empty.copy(), empty.copy(), empty.copy(), empty.copy()


def _readiness_bundle_paths(root: Path, run_id: str, shard_id: str) -> V550ShardPaths:
    paths = V550ShardPaths(root=root, run_id=run_id, shard_id=shard_id)
    paths.ensure()
    return paths


def _write_readiness_bundle(
    paths: V550ShardPaths,
    scope_df: pd.DataFrame,
    readiness_df: pd.DataFrame,
    pos_df: pd.DataFrame,
    weight_df: pd.DataFrame,
    mapping_df: pd.DataFrame,
    legacy_df: pd.DataFrame,
    underpowered_df: pd.DataFrame,
    *,
    source: str,
    wave: str,
    min_cell_n: int,
    progress_started: float,
) -> dict[str, object]:
    outputs = []
    for table_name, frame, layer in [
        ("readiness_scope", scope_df, "core"),
        ("substrate_readiness", readiness_df, "core"),
        ("position_field_coverage", pos_df, "core"),
        ("weight_coverage", weight_df, "core"),
        ("mapping_status_coverage", mapping_df, "core"),
        ("legacy_leak_report", legacy_df, "audit"),
        ("underpowered_quarantine", underpowered_df, "audit"),
    ]:
        _log_progress(progress_started, f"writing readiness artifact {layer}/{table_name} ({len(frame)} rows)")
        meta = write_table(
            frame,
            paths=paths,
            table_name=table_name,
            layer=layer,
            write_csv=False,
            write_parquet=True,
            report_name=f"V550_{table_name}.csv",
            reports_dir=None,
        )
        outputs.append(meta["parquet_path"])
    readiness_manifest = {
        "run_id": paths.run_id,
        "shard_id": paths.shard_id,
        "source": source,
        "wave": wave,
        "min_cell_n": min_cell_n,
        "scope_rows": int(len(scope_df)),
        "readiness_rows": int(len(readiness_df)),
        "position_rows": int(len(pos_df)),
        "weight_rows": int(len(weight_df)),
        "mapping_rows": int(len(mapping_df)),
        "legacy_rows": int(len(legacy_df)),
        "underpowered_rows": int(len(underpowered_df)),
        "outputs": outputs,
        "success": True,
    }
    atomic_write_json(paths.shard_path / "readiness_manifest.json", readiness_manifest)
    atomic_write_json(
        paths.shard_path / "readiness_status.json",
        {
            "run_id": paths.run_id,
            "shard_id": paths.shard_id,
            "status": "success",
            "success": True,
            "updated_at": pd.Timestamp.utcnow().isoformat(),
            "manifest": str(paths.shard_path / "readiness_manifest.json"),
        },
    )
    return readiness_manifest


def _load_readiness_bundle(readiness_root: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    readiness_path = readiness_root / "core" / "substrate_readiness.parquet"
    scope_path = readiness_root / "core" / "readiness_scope.parquet"
    pos_path = readiness_root / "core" / "position_field_coverage.parquet"
    weight_path = readiness_root / "core" / "weight_coverage.parquet"
    mapping_path = readiness_root / "core" / "mapping_status_coverage.parquet"
    legacy_path = readiness_root / "audit" / "legacy_leak_report.parquet"
    underpowered_path = readiness_root / "audit" / "underpowered_quarantine.parquet"
    missing = [str(path) for path in [readiness_path, scope_path, pos_path, weight_path, mapping_path, legacy_path, underpowered_path] if not path.exists()]
    if missing:
        raise RuntimeError(f"[V550_READINESS_ARTIFACT_MISSING] Missing readiness artifact files: {missing}")
    scope_df = read_table_any(scope_path)
    readiness_df = read_table_any(readiness_path)
    pos_df = read_table_any(pos_path)
    weight_df = read_table_any(weight_path)
    mapping_df = read_table_any(mapping_path)
    legacy_df = read_table_any(legacy_path)
    underpowered_df = read_table_any(underpowered_path)
    return readiness_df, pos_df, weight_df, mapping_df, legacy_df, underpowered_df, scope_df


def main() -> int:
    args = parse_args()
    if args.authority_root:
        os.environ["DDM_AUTHORITY_ROOT"] = str(Path(args.authority_root).expanduser().resolve())
    _require_readiness_artifact(args)
    canonical_wave = str(args.canonical_wave or canonical_wave_label(args.source, args.wave))
    question_filter = _load_question_filter(args.question_filter_file)
    if args.verbose:
        faulthandler.enable()
        if args.traceback_timeout_seconds > 0:
            faulthandler.dump_traceback_later(args.traceback_timeout_seconds, repeat=True)
    if args.stop_after_stage not in (0, 4):
        raise SystemExit("--stop-after-stage currently only supports 0 (run all stages) or 4 (stop after question processing).")
    load_dotenv(Path(args.env_file))
    output_root = Path(args.output_root)
    shard_paths = V550ShardPaths(root=output_root, run_id=args.run_id, shard_id=args.shard_id)
    if args.overwrite_shard:
        shard_paths.clean()
    else:
        shard_paths.ensure()
    active_lock = active_readiness_lock_for_shard(DEFAULT_READINESS_ROOT, args.shard_id)
    if active_lock is not None:
        raise SystemExit(f"[V550_READINESS_LOCKED] Active readiness lock present for {args.shard_id}: {active_lock}. Wait for readiness to finish before launching the shard.")

    status_path = shard_paths.status_path
    atomic_write_json(status_path, {"run_id": args.run_id, "shard_id": args.shard_id, "status": "running", "updated_at": pd.Timestamp.utcnow().isoformat()})
    progress_started = time.monotonic()

    conn = None
    try:
        readiness_bundle = None
        readiness_scope_df = pd.DataFrame()
        if args.readiness_artifact:
            readiness_root = Path(args.readiness_artifact)
            _log_progress(progress_started, f"loading readiness artifact from {readiness_root}")
            readiness_bundle = _load_readiness_bundle(readiness_root)
            wave_readiness_df, wave_pos_df, wave_weight_df, wave_mapping_coverage_df, wave_legacy_df, wave_underpowered_df, readiness_scope_df = readiness_bundle
            _log_progress(progress_started, f"loaded readiness artifact: readiness_rows={len(wave_readiness_df)}")
        db_url = load_env_database_url(Path(args.env_file), args.db_url)
        conn, err = try_connect_database(db_url)
        if conn is None:
            raise RuntimeError(f"[V550_SHARD_DB_UNAVAILABLE] Could not connect to Postgres using {args.env_file} or --db-url. Original error: {err}")

        response_relation_contract = resolve_response_relation(conn, args.response_long_relation)
        os.environ["DDM_RESPONSE_LONG_RELATION"] = str(response_relation_contract["relation"])
        _log_progress(
            progress_started,
            "respondent relation resolved: "
            f"{response_relation_contract['relation']} mode={response_relation_contract['selection_mode']}",
        )

        _log_progress(progress_started, "loading scope manifest")
        if readiness_bundle is not None and not readiness_scope_df.empty:
            scope_df = readiness_scope_df.copy()
            _log_progress(progress_started, f"scope manifest reused from readiness artifact: {len(scope_df)} scope rows")
        else:
            scope_df = load_scope_manifest(
                conn,
                [args.source],
                [args.wave],
                [c for c in args.country if c],
                progress_started=progress_started,
                log_prefix=f"scope[{args.source}/{args.wave}]",
            )
            if scope_df.empty:
                _log_progress(
                    progress_started,
                    "base respondent scope lookup returned zero rows; retrying against resolved respondent relation",
                )
                scope_df = load_scope_manifest_from_response_relation(
                    conn,
                    str(response_relation_contract["relation"]),
                    requested_source=args.source,
                    requested_wave=args.wave,
                    countries=[c for c in args.country if c],
                )
        if scope_df.empty:
            raise RuntimeError(
                f"[V550_NO_SHARDS_DISCOVERED] No source/wave rows matched {args.source}/{args.wave} "
                f"in survey_microdata_respondents or {response_relation_contract['relation']}."
            )
        if canonical_wave != args.wave:
            scope_df = scope_df.copy()
            # Do not rename scope wave to canonical_wave: the facet-ready view
            # stores canonical_wave = COALESCE(r.wave, '') (the raw respondent
            # wave), not the canonical_family_label output.  Renaming would
            # cause the prefetch query to search for the canonical value while
            # the view stores the raw value, returning zero rows.
            # scope_df["wave"] = canonical_wave
        _log_progress(progress_started, f"writing shard scope parquet: {shard_paths.shard_path / 'shard_scope.parquet'}")
        scope_df.to_parquet(shard_paths.shard_path / "shard_scope.parquet", index=False)
        atomic_write_json(shard_paths.audit / "respondent_relation_binding.json", response_relation_contract)
        _log_progress(progress_started, "shard scope parquet written")
        _log_progress(progress_started, f"scope manifest loaded: {len(scope_df)} scope rows")
        _log_progress(progress_started, "verifying facet-ready view contract")
        facet_check_started = time.monotonic()
        _assert_facet_ready_view_contract(conn)
        _log_progress(progress_started, f"facet-ready view contract verified in {time.monotonic() - facet_check_started:0.1f}s")

        wave_country_filters = sorted({str(value) for value in scope_df["country_code"].dropna().astype(str) if str(value).strip()})
        if args.readiness_artifact:
            assert readiness_bundle is not None
        elif args.full_readiness or args.readiness_only:
            _log_progress(progress_started, "building full readiness coverage")
            wave_readiness_df, wave_pos_df, wave_weight_df, wave_mapping_coverage_df, wave_legacy_df, wave_underpowered_df = build_readiness(
                conn,
                scope_df,
                min_cell_n=args.min_cell_n,
                source_filters=[args.source],
                wave_filters=[canonical_wave],
                country_filters=wave_country_filters,
                var_filters=question_filter,
                progress_started=progress_started,
                log_prefix=f"full_readiness[{args.source}/{args.wave}]",
            )
        else:
            _log_progress(progress_started, "using launch-ready scope only")
            wave_readiness_df, wave_pos_df, wave_weight_df, wave_mapping_coverage_df, wave_legacy_df, wave_underpowered_df = _launch_readiness_from_scope(scope_df)

        if args.readiness_only:
            readiness_root = Path(args.readiness_output_root)
            readiness_paths = _readiness_bundle_paths(readiness_root, args.run_id, args.shard_id)
            readiness_manifest = _write_readiness_bundle(
                readiness_paths,
                scope_df,
                wave_readiness_df,
                wave_pos_df,
                wave_weight_df,
                wave_mapping_coverage_df,
                wave_legacy_df,
                wave_underpowered_df,
                source=args.source,
                wave=args.wave,
                min_cell_n=args.min_cell_n,
                progress_started=progress_started,
            )
            _log_progress(progress_started, f"readiness-only bundle written: outputs={len(readiness_manifest['outputs'])}")
            atomic_write_json(
                status_path,
                {
                    "run_id": args.run_id,
                    "shard_id": args.shard_id,
                    "status": "success",
                    "success": True,
                    "readiness_only": True,
                    "updated_at": pd.Timestamp.utcnow().isoformat(),
                },
            )
            return 0
        _log_progress(progress_started, "loading question mappings")
        mapping_started = time.monotonic()
        wave_question_mapping_df = _load_wave_question_mapping(conn, args.source, args.wave)
        _log_progress(progress_started, f"question mappings loaded: {len(wave_question_mapping_df)} rows in {time.monotonic() - mapping_started:0.1f}s")
        if question_filter:
            wave_question_mapping_df = _apply_question_filter_exact_first(
                wave_question_mapping_df,
                question_filter,
                source=args.source,
                wave=canonical_wave,
            )
            filtered_rows = int(len(wave_question_mapping_df))
            _log_progress(progress_started, f"question filter applied: retained {filtered_rows} mapped questions from filter file")
        _assert_live_contracts(scope_df, wave_readiness_df, wave_question_mapping_df)

        response_map = _load_response_option_map(args.response_option_map) if args.response_option_map else pd.DataFrame()
        if response_map.empty:
            response_map_build_inputs = {
                "codebook_root": ROOT / "data" / "FINAL CODEBOOKS" / "FINAL FINAL CODEBOOKS",
                "questions_master_drivers": ROOT / "chatgpt_v550_readiness_addendum" / "codebooks" / "questions_master_drivers.csv",
                "questions_master_semantic": ROOT / "chatgpt_v550_readiness_addendum" / "codebooks" / "questions_master_semantic.csv",
                "question_structure_register": ROOT / "chatgpt_v550_readiness_addendum" / "manifests" / "question_structure_register.csv",
                "question_type_taxonomy": ROOT / "chatgpt_v550_readiness_addendum" / "manifests" / "question_type_taxonomy.yaml",
            }
            missing_response_map_inputs = [f"{label}={path}" for label, path in response_map_build_inputs.items() if not path.exists()]
            if missing_response_map_inputs:
                raise FileNotFoundError(
                    "[V550_RESPONSE_OPTION_MAP_BUILD_INPUTS_MISSING] Supply --response-option-map or restore: "
                    + "; ".join(missing_response_map_inputs)
                )
            _log_progress(progress_started, "building response option map from repository codebooks")
            response_map_started = time.monotonic()
            response_map, response_review, response_manifest = build_response_option_map_live(
                codebook_roots=[response_map_build_inputs["codebook_root"]],
                questions_master_drivers=response_map_build_inputs["questions_master_drivers"],
                questions_master_semantic=response_map_build_inputs["questions_master_semantic"],
                question_structure_register=response_map_build_inputs["question_structure_register"],
                question_type_taxonomy=response_map_build_inputs["question_type_taxonomy"],
                db_conn=conn,
                limit_questions=args.limit_questions,
            )
            _log_progress(progress_started, f"live response option map built: {len(response_map)} rows in {time.monotonic() - response_map_started:0.1f}s")
        else:
            response_review = pd.DataFrame()
            response_manifest = {"option_rows": len(response_map), "manual_review_rows": 0, "warnings": ["Loaded response option map from supplied path."]}
        response_semantics_contract = response_semantics_contract_hash(response_map) if not response_map.empty else ""
        # Use the repository's symmetric response-semantics indexer.  It
        # indexes both raw and canonical wave columns, plus family/wave/var/value
        # aliases, so EVS 1981 authority (canonical W1) cannot degrade to
        # observed-only semantics when live rows carry W1.
        semantics_lookup = _lookup_response_semantics_sign_safe(response_map)
        source_structure_register = load_question_structure_register()

        _log_progress(progress_started, "building question list 1/1")
        wave_question_rows = _build_question_list(scope_df, wave_question_mapping_df, args.limit_questions)
        shared_selection: dict[str, Any] = {
            "base_question_rows": wave_question_rows,
            "joint_required_question_rows": pd.DataFrame(),
            "union_question_rows": wave_question_rows,
            "base_var_codes": wave_question_rows["var_code"].dropna().astype(str).str.upper().drop_duplicates().tolist() if "var_code" in wave_question_rows.columns else [],
            "joint_required_var_codes": [],
            "union_var_codes": wave_question_rows["var_code"].dropna().astype(str).str.upper().drop_duplicates().tolist() if "var_code" in wave_question_rows.columns else [],
            "base_only_var_codes": wave_question_rows["var_code"].dropna().astype(str).str.upper().drop_duplicates().tolist() if "var_code" in wave_question_rows.columns else [],
            "joint_only_var_codes": [],
            "overlap_var_codes": [],
            "joint_configuration_ids_by_var": {},
            "applicable_joint_configuration_ids": [],
        }
        extraction_question_rows = wave_question_rows
        joint_registry_hash = ""
        joint_authority_release_id = ""
        p3_authority_release_id = ""
        if args.shared_respondent_substrate_mode != "off":
            if args.v550_prepared_substrate_mode == "off":
                raise RuntimeError("[V550_SHARED_SUBSTRATE_REQUIRES_PREPARED_CACHE] Use --v550-prepared-substrate-mode country or chunked.")
            if args.joint_configuration_registry_path:
                registry_path = Path(args.joint_configuration_registry_path)
                registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
                if not isinstance(registry, dict):
                    raise RuntimeError(f"Invalid joint configuration registry: {registry_path}")
                joint_registry_hash = hashlib.sha256(json.dumps(registry, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str).encode("utf-8")).hexdigest()
                shared_selection = resolve_shared_substrate_requirements(
                    wave_question_rows,
                    registry,
                    source=args.source,
                    canonical_wave=canonical_wave,
                    selected_configuration_ids=args.joint_configuration_id,
                )
                extraction_question_rows = shared_selection["union_question_rows"]
                joint_authority_release_id = str(shared_selection.get("joint_configuration_authority_release_id", ""))
                p3_authority_release_id = str(shared_selection.get("p3_authority_release_id", ""))
                _log_progress(
                    progress_started,
                    "shared substrate selection: "
                    f"base={len(shared_selection['base_var_codes'])} "
                    f"joint_required={len(shared_selection['joint_required_var_codes'])} "
                    f"union={len(shared_selection['union_var_codes'])}",
                )
        scoped_response_map = _filter_response_map_for_wave(
            response_map,
            extraction_question_rows,
            source=args.source,
            wave=args.wave,
            canonical_wave=canonical_wave,
        )
        response_match_audit = build_response_authority_match_audit(wave_question_rows, scoped_response_map)
        assert_response_authority_match_gate(response_match_audit)
        if scoped_response_map.empty:
            raise RuntimeError(
                f"[V550_RESPONSE_SEMANTICS_EMPTY] No response-option authority rows matched "
                f"{args.source}/{args.wave} after exact question filtering."
            )
        scoped_response_semantics_contract = response_semantics_contract_hash(scoped_response_map)
        if scoped_response_semantics_contract != response_semantics_contract:
            response_semantics_contract = scoped_response_semantics_contract
            semantics_lookup = _lookup_response_semantics_sign_safe(scoped_response_map)
        wave_source_structure_audit = build_source_structure_population_audit(wave_question_rows, source_structure_register)
        validation_dir = DEFAULT_VALIDATION_ROOT / f"{_slugify(args.source)}_{_slugify(args.wave)}"
        write_source_structure_population_audit(wave_source_structure_audit, validation_dir / "source_structure_population_audit.csv")
        _assert_live_contracts(scope_df, wave_readiness_df, wave_question_mapping_df, wave_question_rows)
        readiness_lookup = {(str(r.source), str(r.wave), str(r.country_code)): r._asdict() for r in wave_readiness_df.itertuples(index=False)}
        if args.verbose:
            print(f"[v550shard +{time.monotonic() - progress_started:0.0f}s] questions={len(wave_question_rows)} countries={len(wave_country_filters)}", flush=True)
        _log_progress(progress_started, "processing questions 1/1")
        question_row_cache = _prefetch_question_rows_by_country(conn, extraction_question_rows, progress_started)
        _log_progress(progress_started, f"using shared response-country cache for question rows: countries={len(question_row_cache)}")
        question_row_cache, prepared_cache_stats = _prepare_v550_question_row_cache(
            question_row_cache,
            semantics_lookup,
            response_semantics_contract_hash=response_semantics_contract,
            mode=args.v550_prepared_substrate_mode,
            progress_started=progress_started,
        )
        prepared_substrate_mode = args.v550_prepared_substrate_mode != "off"
        shared_substrate_outputs: list[dict[str, Any]] = []
        if args.shared_respondent_substrate_mode == "write":
            for country_code, country_frame in question_row_cache.items():
                frame_for_substrate = country_frame.reset_index(drop=True) if hasattr(country_frame, "reset_index") else pd.DataFrame()
                canonical_frame = canonicalize_shared_respondent_substrate(
                    frame_for_substrate,
                    run_id=args.run_id,
                    shard_id=args.shard_id,
                    source=args.source,
                    source_id=args.source,
                    wave=args.wave,
                    canonical_wave=canonical_wave,
                    country_code=str(country_code),
                    base_var_codes=shared_selection["base_var_codes"],
                    joint_required_var_codes=shared_selection["joint_required_var_codes"],
                    joint_configuration_ids_by_var=shared_selection.get("joint_configuration_ids_by_var", {}),
                )
                paths = shared_substrate_paths(
                    shard_paths.respondent_substrate,
                    source=args.source,
                    canonical_wave=canonical_wave,
                    country_code=str(country_code),
                )
                manifest = write_shared_respondent_substrate_atomic(
                    canonical_frame,
                    paths,
                    manifest_fields={
                        "run_id": args.run_id,
                        "shard_id": args.shard_id,
                        "source": args.source,
                        "source_id": args.source,
                        "wave": args.wave,
                        "canonical_wave": canonical_wave,
                        "country_code": str(country_code),
                        "response_semantics_contract_hash": response_semantics_contract,
                        "question_family_registry_hash": joint_registry_hash,
                        "joint_configuration_authority_release_id": joint_authority_release_id,
                        "p3_authority_release_id": p3_authority_release_id,
                        "respondent_relation_schema_hash": "",
                        "schema_version": SHARED_SUBSTRATE_SCHEMA_VERSION,
                        "execution_contract_version": SHARED_SUBSTRATE_EXECUTION_CONTRACT_VERSION,
                    },
                    base_var_codes=shared_selection["base_var_codes"],
                    joint_required_var_codes=shared_selection["joint_required_var_codes"],
                )
                shared_substrate_outputs.append(
                    {
                        "country_code": str(country_code),
                        "parquet_path": str(paths.parquet_path),
                        "manifest_path": str(paths.manifest_path),
                        "validation_path": str(paths.validation_path),
                        "complete_path": str(paths.complete_path),
                        "content_hash": manifest.get("content_hash"),
                        "row_count": manifest.get("row_count"),
                    }
                )
            _write_json_report(
                shard_paths.respondent_substrate / "shared_respondent_substrate_selection_audit.json",
                {
                    "run_id": args.run_id,
                    "shard_id": args.shard_id,
                    "base_var_codes": shared_selection["base_var_codes"],
                    "joint_required_var_codes": shared_selection["joint_required_var_codes"],
                    "union_var_codes": shared_selection["union_var_codes"],
                    "overlap_var_codes": shared_selection["overlap_var_codes"],
                    "joint_only_var_codes": shared_selection["joint_only_var_codes"],
                    "outputs": shared_substrate_outputs,
                },
            )
        reset_attitude_cloud_state()

        completed_questions = 0
        skipped_questions = 0
        wave_resume_skipped_questions = 0
        harmonization_call_count_hot_path = 0
        harmonization_row_count_hot_path = 0
        harmonization_call_count_fallback = 0
        harmonization_row_count_fallback = 0
        wave_warnings: list[dict[str, Any]] = []
        table_names = [
            "question_universe",
            "question_use_contract",
            "position_distribution",
            "answer_distribution",
            "country_answer_distribution",
            "position_indicator_summary",
            "indicator_answer_matrix",
            "outlier_cohort_summary",
            "secondary_indicator_summary",
            "recursive_branch_nodes",
            "branch_position_signature",
            "branch_relation_co_signature",
            "question_response_attitude_cloud",
            "mapping_gap_report",
            "underpowered_quarantine",
        ]
        wave_table_accumulators: dict[str, list[pd.DataFrame]] = {name: [] for name in table_names}
        skip_question_loop = bool(args.resume and args.resume_from_checkpoints_only)
        if skip_question_loop:
            missing_checkpoints = _missing_question_checkpoint_keys(shard_paths, wave_question_rows)
            if missing_checkpoints:
                raise RuntimeError(
                    "resume-from-checkpoints-only requested, but some question checkpoints are missing: "
                    + ", ".join(missing_checkpoints[:10])
                    + ("" if len(missing_checkpoints) <= 10 else f" ... (+{len(missing_checkpoints) - 10} more)")
                )
            skipped_questions = len(wave_question_rows)
            wave_resume_skipped_questions = len(wave_question_rows)
            _log_progress(
                progress_started,
                f"resume-from-checkpoints-only: verified {len(wave_question_rows)} checkpoints; skipping question execution",
            )
            question_iterable = ()
        else:
            question_iterable = wave_question_rows.itertuples(index=False)

        for idx, q in enumerate(question_iterable, start=1):
            qrow = pd.Series(q._asdict())
            qkey = _question_key(qrow)
            if args.resume and _question_checkpoint_exists(shard_paths, idx, qrow):
                skipped_questions += 1
                wave_resume_skipped_questions += 1
                continue
            fetch_started = time.monotonic()
            if args.verbose:
                print(
                    f"[v550shard +{time.monotonic() - progress_started:0.0f}s] question {idx}/{len(wave_question_rows)} {qkey}: fetching responses",
                    flush=True,
                )
            df = _question_rows_from_cache(qrow, question_row_cache)
            if df.empty:
                fallback_df = _question_rows(
                    conn,
                    qrow,
                    {},
                    response_semantics_contract_hash=response_semantics_contract,
                )
                if fallback_df.empty:
                    # A no-row question is usually a country-level not-asked or otherwise empty cell.
                    # Count it as handled so the shard can finish cleanly without fabricating rows.
                    skipped_questions += 1
                    _mark_question_complete(shard_paths, idx, qrow)
                    if args.verbose:
                        print(f"[v550shard +{time.monotonic() - progress_started:0.0f}s] question {idx}/{len(wave_question_rows)} {qkey}: no rows returned; counted as skipped in {time.monotonic() - fetch_started:0.1f}s", flush=True)
                    continue
                if prepared_substrate_mode:
                    harmonization_call_count_fallback += 1
                    harmonization_row_count_fallback += len(fallback_df)
                else:
                    harmonization_call_count_hot_path += 1
                    harmonization_row_count_hot_path += len(fallback_df)
                df = _harmonize_question_frame(
                    fallback_df,
                    semantics_lookup,
                    response_semantics_contract_hash=response_semantics_contract,
                )
            elif not prepared_substrate_mode:
                harmonization_call_count_hot_path += 1
                harmonization_row_count_hot_path += len(df)
                df = _harmonize_question_frame(df, semantics_lookup, response_semantics_contract_hash=response_semantics_contract)
            if args.verbose:
                print(
                    f"[v550shard +{time.monotonic() - progress_started:0.0f}s] question {idx}/{len(wave_question_rows)} {qkey}: fetched {len(df)} rows in {time.monotonic() - fetch_started:0.1f}s",
                    flush=True,
                )
            qmeta = _summary_question_meta(df, qrow, readiness_lookup.get((qrow["source"], qrow["canonical_wave"], qrow["country_code"])))
            qmeta["run_id"] = args.run_id
            qmeta["shard_id"] = args.shard_id
            source_structure_row, source_structure_join_key, source_structure_join_confidence = match_source_structure_row({**qrow.to_dict(), **qmeta}, source_structure_register)
            qrow = qrow.copy()
            for key, value in source_structure_row.items():
                qrow[key] = value
                qmeta[key] = value
            qrow["source_structure_join_key"] = source_structure_join_key
            qrow["source_structure_join_confidence"] = source_structure_join_confidence
            qmeta["source_structure_join_key"] = source_structure_join_key
            qmeta["source_structure_join_confidence"] = source_structure_join_confidence
            question_use_contract_frame = build_question_use_contract(
                pd.DataFrame(
                    [
                        {
                            **qmeta,
                            "source_structure_fields_joined": bool(qmeta.get("source_structure_fields_joined", False)),
                            "question_type": qrow.get("question_type", qmeta.get("question_type", "")),
                            "handling_rule": qrow.get("handling_rule", qmeta.get("handling_rule", "")),
                            "recommended_computation": qrow.get("recommended_computation", qmeta.get("recommended_computation", "")),
                            "final_driver_scope": qrow.get("final_driver_scope", qmeta.get("final_driver_scope", "")),
                            "source_structure_classification": qrow.get("source_structure_classification", qmeta.get("source_structure_classification", "")),
                        }
                    ]
                ),
                gss_first_pass_authority_path=Path(args.first_pass_authority_dir) if args.first_pass_authority_dir else None,
                gss_semantic_authority_path=Path(args.semantic_authority_dir) if args.semantic_authority_dir else None,
                gss_position_conditioning_path=Path(args.position_conditioning_authority_dir) if args.position_conditioning_authority_dir else None,
                directionality_authority_path=Path(args.directionality_authority_dir) if args.directionality_authority_dir else None,
                survey_family=args.source,
                canonical_wave=canonical_wave,
            )
            question_use_contract_row = question_use_contract_frame.iloc[0].to_dict() if not question_use_contract_frame.empty else {}
            qmeta.update(question_use_contract_row)
            qmeta["question_use_contract_joined"] = True
            weight_status, weights, answer_df, country_answer_df, mapping_gap_df, underpowered_df = build_distribution_tables(
                df,
                qmeta,
                min_answer_n=args.min_answer_n,
                min_cell_n=args.min_cell_n,
                semantics_lookup=semantics_lookup,
            )
            if not _to_bool(qmeta.get("allowed_as_response_distribution", False)):
                answer_df = answer_df.iloc[0:0].copy()
                country_answer_df = country_answer_df.iloc[0:0].copy()
            qmeta["weight_status"] = weight_status
            question_universe_df = pd.DataFrame([qmeta])
            _write_question_checkpoint(shard_paths, "question_universe", idx, qrow, question_universe_df)
            wave_table_accumulators["question_universe"].append(question_universe_df)
            question_use_contract_df = pd.DataFrame([question_use_contract_row])
            _write_question_checkpoint(shard_paths, "question_use_contract", idx, qrow, question_use_contract_df)
            wave_table_accumulators["question_use_contract"].append(question_use_contract_df)
            if not mapping_gap_df.empty:
                _write_question_checkpoint(shard_paths, "mapping_gap_report", idx, qrow, mapping_gap_df)
                wave_table_accumulators["mapping_gap_report"].append(mapping_gap_df)
            if not underpowered_df.empty:
                wave_table_accumulators.setdefault("underpowered_quarantine", []).append(underpowered_df)
            _write_question_checkpoint(shard_paths, "answer_distribution", idx, qrow, answer_df)
            wave_table_accumulators["answer_distribution"].append(answer_df)
            _write_question_checkpoint(shard_paths, "country_answer_distribution", idx, qrow, country_answer_df)
            wave_table_accumulators["country_answer_distribution"].append(country_answer_df)
            from data.ddm_build_copy.ddm_v550_clouds import build_attitude_cloud_rows, build_co_signature_rows, build_position_signature_rows
            branch_df = prepare_question_frame(df)
            question_meta = {
                **qmeta,
                "source_structure_fields_joined": bool(qmeta.get("source_structure_fields_joined", False)),
                "question_type": qrow.get("question_type", qmeta.get("question_type", "")),
                "handling_rule": qrow.get("handling_rule", qmeta.get("handling_rule", "")),
                "recommended_computation": qrow.get("recommended_computation", qmeta.get("recommended_computation", "")),
            }
            position_summary_df = pd.DataFrame(indicator_summary_rows(branch_df, question_meta, weights))
            secondary_summary_df = pd.DataFrame(
                secondary_indicator_summary_rows(branch_df, question_meta, weights),
                columns=SECONDARY_INDICATOR_SUMMARY_COLUMNS,
            )
            indicator_matrix_df = pd.DataFrame(indicator_answer_matrix_rows(branch_df, question_meta, weights))
            outlier_summary_df = pd.DataFrame(outlier_cohort_rows(branch_df, question_meta))
            recursive_nodes_df = pd.DataFrame(branch_nodes_rows(branch_df, question_meta, max_depth=args.max_depth, min_branch_n=args.min_branch_n))
            _write_question_checkpoint(shard_paths, "position_indicator_summary", idx, qrow, position_summary_df)
            _write_question_checkpoint(shard_paths, "secondary_indicator_summary", idx, qrow, secondary_summary_df)
            _write_question_checkpoint(shard_paths, "indicator_answer_matrix", idx, qrow, indicator_matrix_df)
            _write_question_checkpoint(shard_paths, "outlier_cohort_summary", idx, qrow, outlier_summary_df)
            _write_question_checkpoint(shard_paths, "recursive_branch_nodes", idx, qrow, recursive_nodes_df)
            wave_table_accumulators["position_indicator_summary"].append(position_summary_df)
            wave_table_accumulators["secondary_indicator_summary"].append(secondary_summary_df)
            wave_table_accumulators["indicator_answer_matrix"].append(indicator_matrix_df)
            wave_table_accumulators["outlier_cohort_summary"].append(outlier_summary_df)
            wave_table_accumulators["recursive_branch_nodes"].append(recursive_nodes_df)
            wave_respondents = int(qmeta.get("n_respondents", 0) or 0)
            if should_emit_cloud_tables(
                len(branch_df),
                cloud_mode=args.cloud_mode,
                cloud_max_branch_rows=args.cloud_max_branch_rows,
                cloud_max_branch_share=args.cloud_max_branch_share,
                wave_respondents=wave_respondents,
            ):
                branch_position_signature_df = pd.DataFrame(build_position_signature_rows(branch_df, question_meta))
                branch_relation_co_signature_df = pd.DataFrame(build_co_signature_rows(branch_df, question_meta))
                question_response_attitude_cloud_df = pd.DataFrame(build_attitude_cloud_rows(branch_df, question_meta))
                _write_question_checkpoint(shard_paths, "question_response_attitude_cloud", idx, qrow, question_response_attitude_cloud_df)
                _write_question_checkpoint(shard_paths, "branch_position_signature", idx, qrow, branch_position_signature_df)
                _write_question_checkpoint(shard_paths, "branch_relation_co_signature", idx, qrow, branch_relation_co_signature_df)
                wave_table_accumulators["branch_position_signature"].append(branch_position_signature_df)
                wave_table_accumulators["branch_relation_co_signature"].append(branch_relation_co_signature_df)
                wave_table_accumulators["question_response_attitude_cloud"].append(question_response_attitude_cloud_df)
            _mark_question_complete(shard_paths, idx, qrow)
            completed_questions += 1
            if args.verbose and (idx == 1 or idx % 50 == 0 or idx == len(wave_question_rows)):
                print(f"[v550shard +{time.monotonic() - progress_started:0.0f}s] question {idx}/{len(wave_question_rows)} {qkey}: rows={len(df)} completed={completed_questions} skipped={skipped_questions}", flush=True)

        finalize_source = _resolve_finalize_source(
            args.finalize_source,
            resume_requested=bool(args.resume),
            resume_skipped_questions=wave_resume_skipped_questions,
        )
        _log_progress(progress_started, f"combining checkpoint tables 1/1 via {finalize_source}")
        if args.stop_after_stage == 4:
            _log_progress(progress_started, "stopping after stage 4 as requested")
            return 0
        all_questions_completed = len(wave_question_rows) > 0 and (completed_questions + skipped_questions == len(wave_question_rows))
        if not all_questions_completed:
            wave_warnings.append(
                {
                    "wave_source": args.source,
                    "wave": args.wave,
                    "code": "incomplete_question_coverage",
                    "severity": "high",
                    "message": (
                        f"Only {completed_questions + skipped_questions} of {len(wave_question_rows)} questions were completed or resumed for this shard."
                    ),
                    "details": {
                        "completed_questions": completed_questions,
                        "skipped_questions": skipped_questions,
                        "planned_questions": len(wave_question_rows),
                    },
                }
            )
        position_row_cache = question_row_cache
        position_distribution_df = build_position_distribution_rows(
            position_row_cache,
            run_id=args.run_id,
            shard_id=args.shard_id,
            source=args.source,
            source_family=args.source,
            wave=args.wave,
            canonical_wave=str(args.canonical_wave or args.wave),
        )
        wave_tables, finalize_profile = _finalize_wave_checkpoint_tables(
            shard_paths,
            finalize_source=finalize_source,
            wave_question_rows=wave_question_rows,
            wave_table_accumulators=wave_table_accumulators,
            wave_progress_started=progress_started,
        )
        wave_tables["position_distribution"] = position_distribution_df if not position_distribution_df.empty else pd.DataFrame(columns=POSITION_DISTRIBUTION_COLUMNS)
        underpowered_base = wave_tables.get("underpowered_quarantine", pd.DataFrame())
        if wave_underpowered_df is not None and not wave_underpowered_df.empty:
            combined_underpowered = pd.concat([wave_underpowered_df, underpowered_base], ignore_index=True, sort=False)
        else:
            combined_underpowered = underpowered_base
        wave_tables["underpowered_quarantine"] = combined_underpowered
        if wave_tables["question_response_attitude_cloud"].empty:
            wave_warnings.append(
                {
                    "wave_source": args.source,
                    "wave": args.wave,
                    "code": "question_response_attitude_cloud_disabled_until_cross_question_engine",
                    "severity": "medium",
                    "message": "question_response_attitude_cloud is disabled until true cross-question cloud generation is implemented.",
                    "details": {},
                }
            )
        question_response_attitude_cloud_status = "disabled_until_cross_question_engine" if wave_tables["question_response_attitude_cloud"].empty else "prototype_diagnostic"
        branch_position_signature_status = "empty_no_position_features" if wave_tables["branch_position_signature"].empty else "enabled_diagnostic"
        if wave_tables["branch_relation_co_signature"].empty:
            contract_rows = wave_tables.get("question_use_contract", pd.DataFrame())
            allowlisted = False
            if not contract_rows.empty and "allowed_as_branch_relation_cosignature" in contract_rows.columns:
                allowlisted = contract_rows["allowed_as_branch_relation_cosignature"].map(lambda value: _to_bool(value, False)).any()
            if not allowlisted:
                wave_warnings.append(
                    {
                        "wave_source": args.source,
                        "wave": args.wave,
                        "code": "branch_relation_co_signature_empty_no_contract_allowlist",
                        "severity": "medium",
                    "message": "branch_relation_co_signature is empty because no contract allowlist enabled relation cosignature generation.",
                    "details": {},
                }
            )
        branch_relation_cosignature_status = "disabled_no_contract_allowlist" if wave_tables["branch_relation_co_signature"].empty else "enabled_contract_gated"
        wave_tables["branch_co_signature"] = wave_tables["branch_relation_co_signature"].copy()
        branch_co_signature_status = "compatibility_relation_only_alias_or_disabled" if wave_tables["branch_co_signature"].empty else "relation_only_compatibility_alias"
        replayed_cloud_tables = _load_replayed_cloud_tables(shard_paths, progress_started)
        if replayed_cloud_tables is not None:
            replayed_attitude_cloud = replayed_cloud_tables
            wave_tables["question_response_attitude_cloud"] = replayed_attitude_cloud
            wave_tables["branch_co_signature"] = wave_tables["branch_relation_co_signature"].copy()
            _log_progress(
                progress_started,
                f"using replayed cloud outputs: question_response_attitude_cloud={len(replayed_attitude_cloud)} branch_co_signature=relation_alias",
            )
        question_response_attitude_cloud_status = "disabled_until_cross_question_engine" if wave_tables["question_response_attitude_cloud"].empty else "prototype_diagnostic"
        branch_position_signature_status = "empty_no_position_features" if wave_tables["branch_position_signature"].empty else "enabled_diagnostic"
        branch_relation_cosignature_status = "disabled_no_contract_allowlist" if wave_tables["branch_relation_co_signature"].empty else "enabled_contract_gated"
        branch_co_signature_status = "compatibility_relation_only_alias_or_disabled" if wave_tables["branch_co_signature"].empty else "relation_only_compatibility_alias"
        # Ensure branch tables have consistent typed schema via static canonical Arrow schemas
        BRANCH_META = ["country_code","created_at","directionality_status","dominant_response_pct",
            "dominant_response_value","has_response_option_map","legacy_driver_leak_flag",
            "legacy_final_driver_id","n_countries","n_respondents","n_response_rows","ordinal_rank",
            "polarity","question_text","question_type_structural_role","question_use_contract_joined",
            "readiness_status","response_direction","response_family","response_intensity",
            "response_option_confidence_max","response_option_confidence_min",
            "response_semantics_contract_hash","response_semantics_source","response_semantics_status",
            "scale_direction","scale_max","scale_min","shard_id","source_family",
            "source_structure_join_confidence","source_structure_join_key","survey_year","var_name","weight_status"]
        
        branch_schemas = {
            "branch_position_signature": BRANCH_POSITION_SIGNATURE_ARROW_SCHEMA,
            "branch_relation_co_signature": BRANCH_RELATION_CO_SIGNATURE_ARROW_SCHEMA,
            "branch_co_signature": BRANCH_CO_SIGNATURE_ARROW_SCHEMA,
        }
        
        for br_tbl, br_cols in [
            ("branch_position_signature", BRANCH_POSITION_SIGNATURE_COLUMNS),
            ("branch_relation_co_signature", BRANCH_RELATION_CO_SIGNATURE_COLUMNS),
        ]:
            tbl = wave_tables[br_tbl]
            if tbl.empty:
                quc = wave_tables.get("question_use_contract", pd.DataFrame())
                quc_cols = [c for c in quc.columns if c not in ("question_id", "var_code")]
                ref_cols = ["question_id", "var_code"] + quc_cols + BRANCH_META + br_cols
                seen = set(); dedup = []
                for c in ref_cols:
                    if c not in seen: seen.add(c); dedup.append(c)
                wave_tables[br_tbl] = pd.DataFrame(columns=dedup)
        if wave_tables["question_use_contract"].empty:
            wave_tables["question_use_contract"] = pd.DataFrame(columns=[
                "question_id",
                "var_code",
                "semantic_role",
                "v551_evidence_role",
                "gss2010_structural_overlay_used",
                "gss2010_structural_overlay_basis",
                "gss2010_structural_overlay_review_required",
                "allowed_as_response_distribution",
                "allowed_as_position_distribution",
                "allowed_as_context_distribution",
                "allowed_as_demographic_predictor",
                "allowed_as_branch_splitter",
                "allowed_as_branch_position_signature",
                "allowed_as_branch_relation_cosignature",
                "allowed_as_attitude_cloud_anchor",
                "allowed_as_attitude_cloud_feature",
                "allowed_as_v551_relation_evidence",
                "allowed_as_parent_prior_coordinate",
                "allowed_as_temporal_pressure_indicator",
                "allowed_as_runtime_persona_evidence",
                "question_type",
                "handling_rule",
                "mapping_status",
                "question_block_id",
                "structural_domain_id",
                "relation_axis_id",
                "target_entity_id",
                "driver_id",
                "driver_facet_id",
                "target_entity_rule",
                "final_driver_scope",
                "source_structure_classification",
                "source_structure_basis",
                "source_structure_confidence",
                "source_structure_source",
                "source_structure_fields_joined",
            ])
        if wave_tables["position_distribution"].empty:
            wave_tables["position_distribution"] = pd.DataFrame(columns=POSITION_DISTRIBUTION_COLUMNS)
        if wave_tables["branch_relation_co_signature"].empty:
            quc = wave_tables.get("question_use_contract", pd.DataFrame())
            quc_cols = [c for c in quc.columns if c not in ("question_id", "var_code")]
            ref_cols = ["question_id", "var_code"] + quc_cols + BRANCH_META + BRANCH_RELATION_CO_SIGNATURE_COLUMNS
            seen = set(); dedup = []
            for c in ref_cols:
                if c not in seen: seen.add(c); dedup.append(c)
            wave_tables["branch_relation_co_signature"] = pd.DataFrame(columns=dedup)
        if wave_tables["question_response_attitude_cloud"].empty:
            wave_tables["question_response_attitude_cloud"] = pd.DataFrame(columns=QUESTION_RESPONSE_ATTITUDE_CLOUD_COLUMNS)

        wave_tables["branch_co_signature"] = wave_tables["branch_relation_co_signature"].copy()

        _log_progress(
            progress_started,
            "bridge inputs ready 1/11: "
            + ", ".join(f"{name}={len(frame)}" for name, frame in wave_tables.items() if name in {"question_universe", "answer_distribution", "country_answer_distribution", "position_indicator_summary", "indicator_answer_matrix", "outlier_cohort_summary", "secondary_indicator_summary", "recursive_branch_nodes", "branch_position_signature", "branch_relation_co_signature", "branch_co_signature", "question_response_attitude_cloud", "mapping_gap_report"}),
        )
        bridge_started = time.monotonic()
        _log_progress(progress_started, "building bridge index")

        bridge_path = shard_paths.bridge / "v551_bridge_index.parquet"
        bridge_meta = write_v551_bridge_index_for_shard(
            wave_tables,
            run_id=args.run_id,
            shard_id=args.shard_id,
            bridge_path=bridge_path,
            csv_path=shard_paths.csv_mirrors / "v551_bridge_index.csv",
            write_csv=args.write_csv,
            progress_started=progress_started,
            directionality_authority_dir=Path(args.directionality_authority_dir),
            survey_family=args.source,
            canonical_wave=canonical_wave,
        )
        _log_progress(progress_started, f"bridge index built: {bridge_meta['bridge_rows']} rows in {time.monotonic() - bridge_started:0.1f}s")
        (shard_paths.bridge / "v551_bridge_index.schema.json").write_text(
            json.dumps({"row_count": bridge_meta["bridge_rows"], "columns": list(V551_BRIDGE_INDEX_SCHEMA["required_columns"])}, indent=2),
            encoding="utf-8",
        )
        _log_progress(progress_started, "bridge parquet/csv/schema written")
        validation_started = time.monotonic()
        bridge_frame = pd.read_parquet(bridge_path) if bridge_path.exists() else pd.DataFrame(columns=V551_BRIDGE_INDEX_SCHEMA["required_columns"])
        bridge_issues = validate_bridge_df(bridge_frame)
        _log_progress(progress_started, f"bridge validation finished in {time.monotonic() - validation_started:0.1f}s with {len(bridge_issues)} issue(s)")
        bridge_warnings = {
            "run_id": args.run_id,
            "shard_id": args.shard_id,
            "bridge_rows": int(bridge_meta["bridge_rows"]),
            "eligible_rows": int(bridge_meta["eligible_rows"]),
            "excluded_rows": int(bridge_meta["excluded_rows"]),
            "numeric_only_label_excluded_rows": int(bridge_meta.get("numeric_only_label_excluded_rows", 0)),
            "source_structure_fields_populated": bool(
                bridge_frame[["question_type", "handling_rule", "recommended_computation", "source_structure_classification"]]
                .fillna("")
                .astype(str)
                .apply(lambda col: col.str.strip().ne("")).any().any()
            )
            if all(col in bridge_frame.columns for col in ["question_type", "handling_rule", "recommended_computation", "source_structure_classification"])
            else False,
            "source_structure_blank_blocked_rows": int(
                (bridge_frame["v551_exclusion_reason"].fillna("").astype(str) == "blank_source_structure_high_risk_block").sum()
            )
            if "v551_exclusion_reason" in bridge_frame.columns
            else 0,
            "issues": bridge_issues,
        }
        _write_json_report(shard_paths.bridge / "v551_bridge_warnings.json", bridge_warnings)
        (shard_paths.bridge / "v551_bridge_validation_report.json").write_text(json.dumps({"issues": bridge_issues}, indent=2), encoding="utf-8")
        bridge_causal_summary = build_bridge_causal_summary(bridge_frame)
        _write_json_report(shard_paths.bridge / "v551_bridge_causal_summary.json", bridge_causal_summary)
        _log_progress(
            progress_started,
            "bridge causal summary written: "
            f"direct rows={bridge_causal_summary.get('direct_relation_response', {}).get('row_count', 0)} "
            f"multi-gate={bridge_causal_summary.get('direct_relation_response', {}).get('rows_with_multiple_failed_gates', 0)}",
        )
        bridge_audit_mode = "summary_only" if int(bridge_meta["bridge_rows"]) > BRIDGE_AUDIT_MAX_ROWS else "full"
        if bridge_audit_mode == "full":
            bridge_audits = build_bridge_lane_audits(bridge_frame)
            for audit_name, audit_frame in bridge_audits.items():
                audit_path = shard_paths.bridge / f"{audit_name}.csv"
                audit_frame.to_csv(audit_path, index=False)
                _log_progress(progress_started, f"bridge audit written: {audit_name} ({len(audit_frame)} rows)")
        else:
            bridge_audit_summary = {
                "run_id": args.run_id,
                "shard_id": args.shard_id,
                "bridge_rows": int(bridge_meta["bridge_rows"]),
                "eligible_rows": int(bridge_meta["eligible_rows"]),
                "excluded_rows": int(bridge_meta["excluded_rows"]),
                "numeric_only_label_excluded_rows": int(bridge_meta.get("numeric_only_label_excluded_rows", 0)),
                "bridge_audit_mode": bridge_audit_mode,
                "bridge_audit_threshold": BRIDGE_AUDIT_MAX_ROWS,
                "bridge_validation_issues": bridge_issues,
                "note": "Row-level bridge audits skipped because the bridge exceeded the audit threshold; summary-only mode preserves validation and manifest outputs without materializing the large audit tables.",
            }
            _write_json_report(shard_paths.bridge / "v551_bridge_audit_summary.json", bridge_audit_summary)
            _log_progress(progress_started, f"bridge audits skipped in summary-only mode ({int(bridge_meta['bridge_rows'])} rows > {BRIDGE_AUDIT_MAX_ROWS})")

        cloud_exclusion_rows: list[dict[str, Any]] = []
        validator_map = {
            "branch_position_signature": validate_position_signature_rows,
            "branch_relation_co_signature": validate_relation_signature_rows,
            "branch_co_signature": validate_relation_signature_rows,
            "question_response_attitude_cloud": validate_attitude_cloud_rows,
        }
        for table_name, validator in validator_map.items():
            frame = wave_tables.get(table_name, pd.DataFrame())
            _log_progress(progress_started, f"validating cloud exclusions for {table_name}: {len(frame)} rows")
            for issue in validator(frame):
                affected_rows = forbidden_cloud_feature_row_count(frame, issue)
                cloud_exclusion_rows.append(
                    {
                        "run_id": args.run_id,
                        "shard_id": args.shard_id,
                        "table_name": table_name,
                        "issue": issue,
                        "severity": "high",
                        "row_count": int(affected_rows),
                    }
                )
        cloud_exclusion_audit = pd.DataFrame(cloud_exclusion_rows, columns=["run_id", "shard_id", "table_name", "issue", "severity", "row_count"])
        wave_tables["cloud_exclusion_audit"] = cloud_exclusion_audit
        _log_progress(progress_started, f"cloud exclusion audit rows: {len(cloud_exclusion_audit)}")

        wave_warnings, wave_summary = _wave_warning_report(
            run_id=args.run_id,
            wave_index=1,
            wave_total=1,
            wave_source=args.source,
            wave_wave=args.wave,
            wave_question_rows=wave_question_rows,
            wave_readiness_df=wave_readiness_df,
            wave_weight_df=wave_weight_df,
            wave_mapping_df=wave_mapping_coverage_df,
            wave_legacy_df=wave_legacy_df,
            wave_underpowered_df=wave_underpowered_df,
            wave_tables=wave_tables,
            response_review=response_review,
        )
        _write_json_report(shard_paths.warnings_path, wave_summary)
        _log_progress(progress_started, "assembling final output tables 32/51")
        outputs = []
        row_counts = {}
        output_tables = [
            ("question_universe", wave_tables["question_universe"], "core"),
            ("question_use_contract", wave_tables["question_use_contract"], "core"),
            ("response_option_map", scoped_response_map, "core"),
            ("position_distribution", wave_tables["position_distribution"], "determinicity"),
            ("answer_distribution", wave_tables["answer_distribution"], "distributions"),
            ("country_answer_distribution", wave_tables["country_answer_distribution"], "distributions"),
            ("position_indicator_summary", wave_tables["position_indicator_summary"], "determinicity"),
            ("indicator_answer_matrix", wave_tables["indicator_answer_matrix"], "determinicity"),
            ("outlier_cohort_summary", wave_tables["outlier_cohort_summary"], "determinicity"),
            ("secondary_indicator_summary", wave_tables["secondary_indicator_summary"], "determinicity"),
            ("recursive_branch_nodes", wave_tables["recursive_branch_nodes"], "determinicity"),
            ("branch_position_signature", wave_tables["branch_position_signature"], "clouds"),
            ("branch_relation_co_signature", wave_tables["branch_relation_co_signature"], "clouds"),
            ("branch_co_signature", wave_tables["branch_co_signature"], "clouds"),
            ("question_response_attitude_cloud", wave_tables["question_response_attitude_cloud"], "clouds"),
            ("mapping_gap_report", wave_tables["mapping_gap_report"], "audit"),
            ("response_option_manual_review", response_review, "audit"),
            ("response_authority_match_audit", response_match_audit, "audit"),
            ("cloud_exclusion_audit", wave_tables["cloud_exclusion_audit"], "audit"),
            ("scope_manifest", scope_df, "core"),
            ("substrate_readiness", wave_readiness_df, "core"),
            ("position_field_coverage", wave_pos_df, "core"),
            ("weight_coverage", wave_weight_df, "core"),
            ("mapping_status_coverage", wave_mapping_coverage_df, "core"),
            ("legacy_leak_report", wave_legacy_df, "audit"),
            ("underpowered_quarantine", wave_tables["underpowered_quarantine"], "audit"),
        ]
        total_outputs = len(output_tables)
        for output_idx, (table_name, frame, layer) in enumerate(output_tables, start=1):
            if frame is None:
                continue
            write_started = time.monotonic()
            _log_progress(progress_started, f"writing {output_idx}/{total_outputs} {layer}/{table_name}{_process_label(table_name)} ({len(frame)} rows)")
            meta = write_table(frame, paths=shard_paths, table_name=table_name, layer=layer, write_csv=args.write_csv, write_parquet=args.write_parquet, report_name=f"V550_{table_name}.csv", reports_dir=Path(args.reports_dir), extra_schema={"description": f"V550 shard {table_name} output."}, arrow_schema=branch_schemas.get(table_name))
            outputs.append(meta["parquet_path"])
            row_counts[table_name] = len(frame)
            _log_progress(progress_started, f"finished writing {output_idx}/{total_outputs} {layer}/{table_name}{_process_label(table_name)} in {time.monotonic() - write_started:0.1f}s")

        _log_progress(progress_started, "writing shard manifest")
        high_severity_warning = any(str(item.get("severity", "")).lower() == "high" for item in wave_warnings)
        manifest = build_shard_manifest(
            run_id=args.run_id,
            shard_id=args.shard_id,
            source=args.source,
            source_family=args.source,
            wave=args.wave,
            canonical_wave=str(args.canonical_wave or args.wave),
            created_at=pd.Timestamp.utcnow().isoformat(),
            completed_at=pd.Timestamp.utcnow().isoformat(),
            success=all_questions_completed,
            output_root=output_root,
            inputs={"db_used": True, "response_option_map": args.response_option_map or "built", "filters": {"country": args.country}},
            rows_by_table=row_counts,
            warnings=[f"{w['wave_source']} {w['wave']}: {w['code']} - {w['message']}" for w in wave_warnings],
            errors=[],
            outputs=outputs,
            bridge_rows=int(bridge_meta["bridge_rows"]),
            v551_eligible_count=int(bridge_meta["eligible_rows"]),
            v551_excluded_count=int(bridge_meta["excluded_rows"]),
            promotable=all_questions_completed and not bridge_issues and cloud_exclusion_audit.empty and not high_severity_warning,
        )
        manifest["response_semantics_contract_hash"] = response_semantics_contract
        manifest["response_option_map_row_count"] = int(len(scoped_response_map))
        manifest["response_option_map_artifact"] = str(shard_paths.core / "response_option_map.parquet")
        manifest["v550_prepared_substrate_mode"] = args.v550_prepared_substrate_mode
        manifest["shared_respondent_substrate_mode"] = args.shared_respondent_substrate_mode
        manifest["shared_respondent_substrate_outputs"] = shared_substrate_outputs
        manifest["shared_respondent_substrate_base_var_codes"] = shared_selection["base_var_codes"]
        manifest["shared_respondent_substrate_joint_required_var_codes"] = shared_selection["joint_required_var_codes"]
        manifest["shared_respondent_substrate_union_var_codes"] = shared_selection["union_var_codes"]
        manifest["shared_respondent_substrate_overlap_var_codes"] = shared_selection["overlap_var_codes"]
        manifest["shared_respondent_substrate_joint_only_var_codes"] = shared_selection["joint_only_var_codes"]
        manifest["v550_harmonization_call_count_prepared"] = int(prepared_cache_stats["v550_harmonization_call_count_prepared"])
        manifest["v550_harmonization_row_count_prepared"] = int(prepared_cache_stats["v550_harmonization_row_count_prepared"])
        manifest["v550_harmonization_call_count_per_question"] = int(prepared_cache_stats["v550_harmonization_call_count_per_question"] + harmonization_call_count_hot_path)
        manifest["v550_harmonization_row_count_per_question"] = int(prepared_cache_stats["v550_harmonization_row_count_per_question"] + harmonization_row_count_hot_path)
        manifest["v550_harmonization_call_count_fallback"] = int(prepared_cache_stats["v550_harmonization_call_count_fallback"] + harmonization_call_count_fallback)
        manifest["v550_harmonization_row_count_fallback"] = int(prepared_cache_stats["v550_harmonization_row_count_fallback"] + harmonization_row_count_fallback)
        manifest["question_response_attitude_cloud_status"] = question_response_attitude_cloud_status
        manifest["branch_position_signature_status"] = branch_position_signature_status
        manifest["branch_relation_cosignature_status"] = branch_relation_cosignature_status
        manifest["branch_co_signature_status"] = branch_co_signature_status
        manifest["bridge_audit_mode"] = bridge_audit_mode
        manifest["promotability_override"] = False
        manifest["promotability_override_reason"] = ""
        manifest_issues = validate_shard_manifest(manifest)
        if manifest_issues:
            manifest["promotable"] = False
            manifest.setdefault("warnings", []).extend(manifest_issues)
        if not all_questions_completed:
            manifest["promotable"] = False
        atomic_write_json(shard_paths.manifest_path, manifest)
        _log_progress(progress_started, "writing shard status")
        atomic_write_json(
            status_path,
            {
                "run_id": args.run_id,
                "shard_id": args.shard_id,
                "status": "success" if all_questions_completed else "partial",
                "started_at": pd.Timestamp.utcnow().isoformat(),
                "finished_at": pd.Timestamp.utcnow().isoformat(),
                "source": args.source,
                "wave": args.wave,
                "canonical_wave": str(args.canonical_wave or args.wave),
                "row_counts": row_counts,
                "errors": [],
                "warnings": manifest.get("warnings", []),
                "promotable": bool(manifest.get("promotable", False)),
                "updated_at": pd.Timestamp.utcnow().isoformat(),
            },
        )
        if args.verbose:
            _log_progress(
                progress_started,
                f"final manifest ready: success={manifest.get('success')} promotable={manifest.get('promotable')} outputs={len(outputs)}",
            )
        return 0 if all_questions_completed else 1
    except Exception as exc:
        failure = {"run_id": args.run_id, "shard_id": args.shard_id, "status": "failed", "error": str(exc), "updated_at": pd.Timestamp.utcnow().isoformat()}
        atomic_write_json(status_path, failure)
        atomic_write_json(shard_paths.warnings_path, {"error": str(exc)})
        raise
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
