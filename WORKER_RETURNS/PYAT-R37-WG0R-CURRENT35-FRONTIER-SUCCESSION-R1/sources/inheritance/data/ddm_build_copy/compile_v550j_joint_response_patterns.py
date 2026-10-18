#!/usr/bin/env python3
"""Compile V550J joint-response pattern outputs for one V550 shard."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import threading
from collections import Counter
from pathlib import Path
from contextlib import contextmanager
from time import monotonic
from typing import Any

import pandas as pd
import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.build_determinicity_repository_v550 import _harmonize_question_frame, _lookup_response_semantics, _prefetch_question_rows_by_country, _question_rows_from_cache
from data.ddm_build_copy.build_v550j_prepared_substrate import load_or_build_v550j_prepared_substrate
from data.ddm_build_copy.build_response_option_map_v550 import build_response_option_map
from data.ddm_build_copy.ddm_pipeline_boundary_contract import PIPELINE_BOUNDARY_CONTRACT_VERSION
from data.ddm_build_copy.ddm_v550_manifest import utc_now
from data.ddm_build_copy.ddm_v550_response_options import response_semantics_contract_hash
from data.ddm_build_copy.ddm_v550_schema import write_schema_json
from data.ddm_build_copy.ddm_v550_shared_cache import cache_entry, cache_signature, load_cached_frame, shared_cache_root, write_cached_frame
from data.ddm_build_copy.ddm_v550_storage import atomic_write_json, connect_from_env, read_table_any
from data.ddm_build_copy.ddm_v550_shared_respondent_substrate import (
    logical_shared_substrate_hash,
    validate_shared_respondent_substrate,
)
from data.ddm_build_copy.ddm_run_provenance import capture_run_provenance
from data.ddm_build_copy.ddm_v550j_joint_patterns import (
    V550J_ASSOCIATION_CANDIDATE_TRACE_COLUMNS,
    V550J_ASSOCIATION_INDEX_COLUMNS,
    V550J_ASSOCIATION_FUNNEL_COLUMNS,
    V550J_ASSOCIATION_REVIEW_SURFACE_COLUMNS,
    V550J_MEANING_SUMMARY_COLUMNS,
    V550J_SCHEMA_VERSION,
    _association_eligibility_funnel,
    compile_v550j_family_tables,
    _association_authority_status,
    _family_item_map,
    _to_bool,
)
from data.ddm_build_copy.ddm_v550j_registry_classifier import AssociationLaneRegistry
from data.ddm_build_copy.ddm_v550j_registry_contract import (
    EXECUTABLE_JOINT_REGISTRY_STATUSES,
    registry_status_is_executable,
    require_executable_registry_status,
)
from data.ddm_build_copy.ddm_survey_identity import (
    SurveyIdentityError,
    canonical_family_key,
    canonical_wave_key,
    family_keys_equal,
    require_survey_identity,
)


DEFAULT_OUTPUT_ROOT = ROOT / "data" / "ddm_repository_copy" / "v550j"
DEFAULT_REPORTS_DIR = ROOT / "data" / "ddm_build_copy" / "reports"
DEFAULT_ENV_FILE = ROOT / ".env"
DEFAULT_RESPONSE_OPTION_MAP = DEFAULT_REPORTS_DIR / "V550_response_option_map.csv"
DEFAULT_ASSOCIATION_THRESHOLD_PROFILES = (
    ROOT / "data" / "ddm_registries" / "association_threshold_profiles.yaml"
)
V550J_PRODUCER_SCHEMA_VERSION = V550J_SCHEMA_VERSION
V550J_PRODUCER_COMPILER_VERSION = "v550j_joint_response_patterns_producer_v1"
V550J_V551J_GOVERNED_TABLES = (
    "joint_response_pattern_index",
    "joint_response_pattern_item_index",
    "joint_pattern_relation_signature",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile V550J joint-response pattern outputs for one V550 shard.")
    parser.add_argument("--v550-shard-dir", required=True, help="Path to an existing V550 shard directory.")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument(
        "--registry-path",
        required=True,
        help="Explicit question-family registry for this survey family; no GSS or other family default is permitted.",
    )
    parser.add_argument("--association-lane-registry-path", default=None, help="Path to association_lane_registry.yaml. Defaults to data/ddm_registries/association_lane_registry.yaml relative to project root.")
    parser.add_argument(
        "--association-threshold-profiles-path",
        default=str(DEFAULT_ASSOCIATION_THRESHOLD_PROFILES),
        help="Source/effective-N threshold profile registry.",
    )
    parser.add_argument("--response-option-map", default=str(DEFAULT_RESPONSE_OPTION_MAP))
    parser.add_argument("--db-url", default=None)
    parser.add_argument("--env-file", default=str(DEFAULT_ENV_FILE))
    progress_group = parser.add_mutually_exclusive_group()
    progress_group.add_argument("--progress", dest="progress", action="store_true", default=True, help="Emit numbered progress updates to stderr.")
    progress_group.add_argument("--no-progress", dest="progress", action="store_false", help="Disable numbered progress updates.")
    parser.add_argument("--write-csv", action="store_true", default=False)
    parser.add_argument("--no-write-csv", dest="write_csv", action="store_false")
    parser.add_argument("--write-parquet", action="store_true", default=True)
    parser.add_argument("--no-write-parquet", dest="write_parquet", action="store_false")
    parser.add_argument("--with-diagnostics", action="store_true", default=False, help="Enable candidate trace, funnel, audit, and validation report outputs.")
    parser.add_argument(
        "--association-mode",
        default="publishable",
        choices=("off", "funnel_only", "candidate_trace", "publishable"),
        help="Control association candidate work in V550J.",
    )
    parser.add_argument(
        "--publish-association-lanes",
        default="substantive_attitude_association",
        help="Comma-separated association lanes that may be published to the main association index.",
    )
    parser.add_argument(
        "--association-support-threshold",
        type=int,
        default=None,
        help="Optional minimum overlap required for publishable association rows.",
    )
    parser.add_argument(
        "--question-filter-file",
        default=None,
        help="Optional JSON/CSV/text file listing question_ids or var_codes to retain for a micro-slice run.",
    )
    parser.add_argument(
        "--v550j-substrate-mode",
        default="prepared_or_build",
        choices=("prepared_required", "prepared_or_build", "prepared_or_forensic_fallback", "forensic_reharmonize"),
        help="Control prepared-substrate behavior for V550J.",
    )
    parser.add_argument("--prepared-substrate-path", default=None, help="Explicit shared/prepared respondent substrate Parquet path.")
    parser.add_argument("--prepared-substrate-manifest-path", default=None, help="Explicit shared/prepared respondent substrate manifest path.")
    parser.add_argument("--forbid-database-access", action="store_true", help="Reject every code path that would open PostgreSQL.")
    parser.add_argument("--association-fetch-chunk-size", type=int, default=25000, help="Chunk size for association-context SQL fetches; set <=0 to disable chunking.")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def _load_question_filter(path: str | None) -> set[str]:
    if not path:
        return set()
    filter_path = Path(path)
    if not filter_path.exists():
        raise FileNotFoundError(filter_path)
    if filter_path.suffix.lower() == ".json":
        payload = json.loads(filter_path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            values = payload.get("question_ids") or payload.get("var_codes") or payload.get("selected_question_ids") or []
        else:
            values = payload
        return {str(value).strip().upper() for value in values if str(value).strip()}
    if filter_path.suffix.lower() == ".csv":
        df = pd.read_csv(filter_path)
        for candidate in ["question_id", "var_code", "variable_id", "question_name", "name"]:
            if candidate in df.columns:
                return {str(value).strip().upper() for value in df[candidate].dropna().astype(str) if str(value).strip()}
        return set()
    return {
        str(line).strip().upper()
        for line in filter_path.read_text(encoding="utf-8").splitlines()
        if str(line).strip() and not str(line).strip().startswith("#")
    }


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError(f"Invalid registry payload: {path}")
    return payload


def _safe_clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    text = str(value).strip()
    return "" if text.lower() in {"nan", "none"} else text


def _registry_status_is_executable(value: Any) -> bool:
    return registry_status_is_executable(value)


def _validate_bounded_authority_registry(registry: dict[str, Any]) -> dict[str, int]:
    """Fail closed on bounded R184-to-V550J authority metadata."""
    scope_id = _safe_clean(registry.get("scope_id"))
    if not scope_id:
        return {"bounded_family_count": 0, "bounded_item_count": 0, "p3_bound_item_count": 0}
    status = _safe_clean(registry.get("status")).lower()
    if status != "governed":
        raise RuntimeError(f"Bounded authority registry must be governed, got {status or 'missing'}")
    if _safe_clean(registry.get("production_completeness_claim")) != "NO_PRODUCTION_COMPLETENESS_CLAIM":
        raise RuntimeError("Bounded authority registry must explicitly deny production completeness")
    if _safe_clean(registry.get("response_portability_status")) != "NOT_AUTHORIZED_BY_P3":
        raise RuntimeError("P3 proposition identity does not authorize response portability")
    release_id = _safe_clean(registry.get("p3_authority_release_id"))
    if not release_id:
        raise RuntimeError("Bounded authority registry is missing p3_authority_release_id")
    joint_release_id = _safe_clean(registry.get("joint_configuration_authority_release_id"))
    if not joint_release_id:
        raise RuntimeError("Bounded authority registry is missing joint_configuration_authority_release_id")
    if not _safe_clean(registry.get("joint_configuration_adjudication_set_hash")):
        raise RuntimeError("Bounded authority registry is missing its adjudication-set hash")
    families = registry.get("families") or []
    seen_configuration_ids: set[str] = set()
    item_count = 0
    p3_bound_count = 0
    for family in families:
        if not isinstance(family, dict):
            raise RuntimeError("Bounded authority registry family entries must be mappings")
        configuration_id = _safe_clean(family.get("joint_configuration_id"))
        if not configuration_id or configuration_id != _safe_clean(family.get("family_id")):
            raise RuntimeError("Bounded family_id must equal a non-empty joint_configuration_id")
        if configuration_id in seen_configuration_ids:
            raise RuntimeError(f"Duplicate joint_configuration_id: {configuration_id}")
        seen_configuration_ids.add(configuration_id)
        metadata = family.get("authority_metadata") or {}
        if _safe_clean(metadata.get("configuration_authority_status")) != "GOVERNED_BOUNDED_CANARY_ONLY":
            raise RuntimeError(f"{configuration_id}: missing governed bounded authority status")
        adjudication_id = _safe_clean(metadata.get("joint_configuration_adjudication_id"))
        if not adjudication_id:
            raise RuntimeError(f"{configuration_id}: missing bounded joint-configuration adjudication")
        if _safe_clean(metadata.get("joint_configuration_authority_release_id")) != joint_release_id:
            raise RuntimeError(f"{configuration_id}: stale or mismatched joint-configuration authority release")
        if _safe_clean(metadata.get("joint_configuration_decision_status")) not in {"ACCEPTED_BOUNDED_SOURCE_NATIVE_CONFIGURATION", "ACCEPTED_EXISTING_GSS_EXECUTABLE_CONTROL"}:
            raise RuntimeError(f"{configuration_id}: unaccepted joint-configuration decision")
        if _safe_clean(metadata.get("authority_basis_status")) != "HUMAN_ADJUDICATED_FROM_EXACT_SOURCE_EVIDENCE":
            raise RuntimeError(f"{configuration_id}: discovery structure was not separately adjudicated")
        p2_effect = _safe_clean(metadata.get("p2_authority_effect"))
        if p2_effect not in {"P2_DISCOVERY_EVIDENCE_ONLY_NOT_J_FAMILY_AUTHORITY", "EXISTING_GSS_IMPLEMENTATION_REFERENCE"}:
            raise RuntimeError(f"{configuration_id}: P2 discovery evidence was improperly promoted to authority")
        if _safe_clean(metadata.get("p2_source_structure_id")) == "":
            raise RuntimeError(f"{configuration_id}: missing P2 source structure provenance")
        if _safe_clean(metadata.get("p3_authority_release_id")) != release_id:
            raise RuntimeError(f"{configuration_id}: stale or mismatched P3 release")
        if _safe_clean(metadata.get("response_portability_status")) != "NOT_AUTHORIZED_BY_P3":
            raise RuntimeError(f"{configuration_id}: unauthorized response portability")
        seen_vars: set[str] = set()
        for item in _family_item_map(family):
            var_code = _safe_clean(item.get("var_code")).upper()
            if var_code in seen_vars:
                raise RuntimeError(f"{configuration_id}: duplicate var_code {var_code}")
            seen_vars.add(var_code)
            item_count += 1
            if not _safe_clean(item.get("p2_lineage_id")) or not _safe_clean(item.get("question_implementation_id")):
                raise RuntimeError(f"{configuration_id}/{var_code}: missing source-local lineage provenance")
            if _safe_clean(item.get("joint_configuration_adjudication_id")) != adjudication_id:
                raise RuntimeError(f"{configuration_id}/{var_code}: adjudication provenance mismatch")
            if _safe_clean(item.get("joint_configuration_authority_release_id")) != joint_release_id:
                raise RuntimeError(f"{configuration_id}/{var_code}: joint-authority release mismatch")
            if _safe_clean(item.get("p2_source_structure_id")) != _safe_clean(metadata.get("p2_source_structure_id")):
                raise RuntimeError(f"{configuration_id}/{var_code}: source-structure provenance mismatch")
            membership_status = _safe_clean(item.get("p3_membership_status"))
            if membership_status == "BOUND_TO_CURRENT_CANONICAL_FAMILY":
                required = ("p3_canonical_family_id", "p3_current_family_revision_id", "p3_variant_revision_id")
                if any(not _safe_clean(item.get(field)) for field in required):
                    raise RuntimeError(f"{configuration_id}/{var_code}: incomplete current P3 membership")
                if _safe_clean(item.get("p3_authority_release_id")) != release_id:
                    raise RuntimeError(f"{configuration_id}/{var_code}: stale P3 item release")
                p3_bound_count += 1
            elif membership_status != "SOURCE_LOCAL_ONLY_NOT_ON_P3_CANONICAL_SURFACE":
                raise RuntimeError(f"{configuration_id}/{var_code}: ungoverned P3 membership status {membership_status or 'missing'}")
            if _safe_clean(item.get("response_portability_status")) != "NOT_AUTHORIZED_BY_P3":
                raise RuntimeError(f"{configuration_id}/{var_code}: unauthorized item response portability")
    return {"bounded_family_count": len(seen_configuration_ids), "bounded_item_count": item_count, "p3_bound_item_count": p3_bound_count}


def _single_scope_value(frame: pd.DataFrame, columns: tuple[str, ...], label: str) -> str:
    values: list[str] = []
    for column in columns:
        if column not in frame.columns:
            continue
        values.extend(
            value
            for value in frame[column].dropna().astype(str).map(str.strip).tolist()
            if value and value.lower() not in {"nan", "none", "null", "unknown"}
        )
    unique = list(dict.fromkeys(values))
    if len(unique) > 1:
        raise SurveyIdentityError(f"V550J shard has multiple {label} values: {unique[:8]}")
    return unique[0] if unique else ""


def _select_threshold_profile(
    payload: dict[str, Any],
    *,
    source: str,
    effective_n: int,
) -> tuple[str, dict[str, Any]]:
    profiles = payload.get("profiles", {})
    if not isinstance(profiles, dict):
        raise RuntimeError("association threshold profile registry must contain a profiles mapping")
    matches: list[tuple[str, dict[str, Any]]] = []
    for profile_id, profile in profiles.items():
        if not isinstance(profile, dict):
            continue
        applies = profile.get("applies_to", {})
        applies = applies if isinstance(applies, dict) else {}
        profile_source = _safe_clean(applies.get("source"))
        if profile_source and not family_keys_equal(profile_source, source):
            continue
        minimum = int(applies.get("effective_n_min") or 0)
        maximum_raw = applies.get("effective_n_max")
        maximum = int(maximum_raw) if maximum_raw not in {None, ""} else None
        if effective_n < minimum or (maximum is not None and effective_n > maximum):
            continue
        matches.append((str(profile_id), profile))
    if matches:
        matches.sort(
            key=lambda item: bool(
                _safe_clean((item[1].get("applies_to") or {}).get("source"))
            ),
            reverse=True,
        )
        return matches[0]

    restrictive: dict[str, Any] = {"publishable_attitude": {"min_overlap": 0}}
    for profile in profiles.values():
        if not isinstance(profile, dict):
            continue
        candidate = profile.get("publishable_attitude", {})
        if int((candidate or {}).get("min_overlap") or 0) > int(
            restrictive["publishable_attitude"]["min_overlap"]
        ):
            restrictive = profile
    return "safe_restrictive_no_matching_profile", restrictive


def _json_safe_value(value: Any) -> Any:
    if isinstance(value, (dict, list, tuple, set)):
        if isinstance(value, set):
            value = sorted(value)
        elif isinstance(value, tuple):
            value = list(value)
        return json.dumps(value, sort_keys=True, ensure_ascii=False, default=str)
    return value


def _stable_hash(payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _file_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _derive_v550j_producer_boundary_state(
    *,
    governed_family_count: int,
    core_table_row_counts: dict[str, int],
    validation_status: str,
) -> tuple[str, str, str, str]:
    if str(validation_status).strip().lower() not in {"pass", "not_applicable"}:
        return "FAIL", "APPLICABLE_UNRESOLVED", "DENY", "V550J_OUTPUT_VALIDATION_FAILED"
    counts = [int(core_table_row_counts.get(name, 0)) for name in V550J_V551J_GOVERNED_TABLES]
    if governed_family_count == 0:
        if any(counts):
            return "FAIL", "APPLICABLE_UNRESOLVED", "DENY", "V550J_OUTPUT_WITHOUT_GOVERNED_FAMILY"
        return "PASS", "NOT_APPLICABLE", "NOT_APPLICABLE", "NO_GOVERNED_JOINT_FAMILY_APPLICABLE"
    if all(count == 0 for count in counts):
        return "PASS", "VALID_EMPTY", "NOT_APPLICABLE", "VALID_EMPTY_NO_JOINT_PATTERN_EVIDENCE"
    if all(count > 0 for count in counts):
        return "PASS", "PRESENT", "ALLOW", "COMPLETE_V550J_JOINT_PATTERN_EVIDENCE"
    return "PASS", "APPLICABLE_UNRESOLVED", "DENY", "INCOMPLETE_V550J_CORE_PRODUCER_SURFACE"


def _response_value_series(values: pd.Series) -> pd.Series:
    cleaned = values.fillna("").astype(str).str.strip()
    cleaned = cleaned.mask(cleaned.str.lower().isin({"nan", "none"}), "")
    if cleaned.empty:
        return cleaned
    numeric_like = cleaned.str.match(r"^[+-]?\d+(?:\.0+)?$")
    if numeric_like.any():
        cleaned.loc[numeric_like] = cleaned.loc[numeric_like].str.replace(r"\.0+$", "", regex=True)
    return cleaned


def _facet_ready_view_name(db_conn=None) -> str:
    if db_conn is None:
        return "v_ddm_response_long_facet_ready"
    try:
        exists = pd.read_sql_query(
            """
            SELECT 1
            FROM information_schema.views
            WHERE table_schema = 'public'
              AND table_name = 'v_ddm_response_long_facet_ready_authority'
            LIMIT 1
            """,
            db_conn,
        )
        if not exists.empty:
            return "v_ddm_response_long_facet_ready_authority"
    except Exception:
        return "v_ddm_response_long_facet_ready"
    return "v_ddm_response_long_facet_ready"


def _family_waves(family_cfg: dict[str, Any], source: str) -> set[str]:
    waves = family_cfg.get("eligible_waves", []) or []
    return {
        canonical_wave_key(source, value)
        for value in waves
        if canonical_wave_key(source, value)
    }


def _family_wave_values(family_questions: pd.DataFrame, source: str) -> set[str]:
    if family_questions.empty:
        return set()
    wave_columns = []
    if "wave" in family_questions.columns:
        wave_columns.append(family_questions["wave"])
    if "canonical_wave" in family_questions.columns:
        wave_columns.append(family_questions["canonical_wave"])
    if not wave_columns:
        return set()
    combined = pd.concat(wave_columns, ignore_index=True)
    return {
        canonical_wave_key(source, value)
        for value in combined.dropna().astype(str).tolist()
        if canonical_wave_key(source, value)
    }


def _family_wave_is_eligible(family_cfg: dict[str, Any], family_questions: pd.DataFrame, source: str) -> bool:
    eligible_waves = _family_waves(family_cfg, source)
    if not eligible_waves:
        return True
    question_wave_values = _family_wave_values(family_questions, source)
    return bool(question_wave_values and not question_wave_values.isdisjoint(eligible_waves))


def _write_table(
    df: pd.DataFrame,
    *,
    out_dir: Path,
    table_name: str,
    write_csv: bool,
    write_parquet: bool,
) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    parquet_path = out_dir / f"{table_name}.parquet"
    csv_path = out_dir / f"{table_name}.csv"
    schema_path = out_dir / f"{table_name}.schema.json"
    serializable_df = df.copy()
    for column in serializable_df.columns:
        serializable_df[column] = serializable_df[column].map(_json_safe_value)
    if write_parquet:
        serializable_df.to_parquet(parquet_path, index=False)
    if write_csv:
        serializable_df.to_csv(csv_path, index=False)
    write_schema_json(schema_path, serializable_df, name=table_name, run_id=out_dir.parent.name if out_dir.parent else "", extra={"layer": "v550j"})
    return {
        "table_name": table_name,
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "parquet_path": str(parquet_path) if write_parquet else "",
        "csv_path": str(csv_path) if write_csv else "",
        "schema_path": str(schema_path),
        "artifact_kind": "canonical" if write_parquet else "diagnostic_only",
        "artifact_file_sha256": _file_sha256(parquet_path) if write_parquet else "",
        "schema_version": V550J_PRODUCER_SCHEMA_VERSION,
        "compiler_version": V550J_PRODUCER_COMPILER_VERSION,
    }


# NOTE: The remainder of this module intentionally preserves the pre-amendment
# V550J compiler implementation byte-for-byte in behavior. Only the producer
# boundary at serialization/publication is amended below.


def _load_sql_query_in_chunks(
    sql: str,
    db_conn,
    *,
    chunk_size: int,
    cache_entry_obj,
    cache_payload: dict[str, Any],
    progress: ProgressReporter | None = None,
    progress_title: str = "SQL chunked fetch",
    bypass_existing_cache: bool = False,
) -> pd.DataFrame | None:
    if db_conn is None:
        return None
    chunk_size = int(chunk_size)
    if chunk_size <= 0:
        queried = pd.read_sql_query(sql, db_conn)
        if queried.empty:
            return None
        return queried

    cache_dir = cache_entry_obj.entry_dir
    final_data_path = cache_entry_obj.data_path
    final_meta_path = cache_entry_obj.meta_path
    chunk_dir = cache_dir / "chunks"
    manifest_path = cache_dir / "chunk_manifest.json"
    if not bypass_existing_cache and final_data_path.exists() and final_meta_path.exists():
        cached = load_cached_frame(cache_entry_obj, expected_signature=cache_payload.get("query_signature"))
        if cached is not None:
            return cached.reset_index(drop=True)
    if not bypass_existing_cache and chunk_dir.exists():
        existing_chunks = sorted(chunk_dir.glob("chunk_*.parquet"))
        if existing_chunks and manifest_path.exists():
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            except Exception:
                manifest = {}
            if manifest.get("complete") is True:
                frames = [pd.read_parquet(path) for path in existing_chunks]
                if frames:
                    frame = pd.concat(frames, ignore_index=True, sort=False)
                    write_cached_frame(frame, cache_entry_obj, {"query_signature": cache_payload.get("query_signature", ""), "query_payload": cache_payload})
                    return frame.reset_index(drop=True)

    chunk_dir.mkdir(parents=True, exist_ok=True)
    frames: list[pd.DataFrame] = []
    chunk_count = 0
    total_rows = 0
    try:
        iterator = pd.read_sql_query(sql, db_conn, chunksize=chunk_size)
    except TypeError:
        queried = pd.read_sql_query(sql, db_conn)
        if queried.empty:
            return None
        if "var_code" in queried.columns:
            queried = queried.copy()
            queried["var_code"] = queried["var_code"].astype(str).str.upper()
            queried = queried.set_index("var_code", drop=False)
        write_cached_frame(
            queried.reset_index(drop=True),
            cache_entry_obj,
            {
                "query_signature": cache_payload.get("query_signature", ""),
                "query_payload": cache_payload,
                "chunk_size": 0,
                "chunk_count": 1,
                "row_count": int(len(queried)),
                "complete": True,
                "created_at": utc_now(),
            },
        )
        return queried.reset_index(drop=True)
    for chunk_count, chunk in enumerate(iterator, start=1):
        if chunk.empty:
            continue
        chunk_path = chunk_dir / f"chunk_{chunk_count:06d}.parquet"
        chunk.to_parquet(chunk_path, index=False)
        total_rows += int(len(chunk))
        frames.append(chunk)
        if progress is not None:
            progress.note(f"{progress_title}: wrote chunk {chunk_count} rows={len(chunk)} total_rows={total_rows}")
        atomic_write_json(
            manifest_path,
            {
                "query_signature": cache_payload.get("query_signature", ""),
                "query_payload": cache_payload,
                "chunk_size": chunk_size,
                "chunk_count": chunk_count,
                "row_count": total_rows,
                "complete": False,
                "created_at": utc_now(),
            },
        )
    if not frames:
        atomic_write_json(
            manifest_path,
            {
                "query_signature": cache_payload.get("query_signature", ""),
                "query_payload": cache_payload,
                "chunk_size": chunk_size,
                "chunk_count": 0,
                "row_count": 0,
                "complete": True,
                "created_at": utc_now(),
            },
        )
        return None
    frame = pd.concat(frames, ignore_index=True, sort=False)
    if "var_code" in frame.columns:
        frame = frame.copy()
        frame["var_code"] = frame["var_code"].astype(str).str.upper()
        frame = frame.set_index("var_code", drop=False)
    write_cached_frame(
        frame.reset_index(drop=True),
        cache_entry_obj,
        {
            "query_signature": cache_payload.get("query_signature", ""),
            "query_payload": cache_payload,
            "chunk_size": chunk_size,
            "chunk_count": chunk_count,
            "row_count": total_rows,
            "complete": True,
            "created_at": utc_now(),
        },
    )
    atomic_write_json(
        manifest_path,
        {
            "query_signature": cache_payload.get("query_signature", ""),
            "query_payload": cache_payload,
            "chunk_size": chunk_size,
            "chunk_count": chunk_count,
            "row_count": total_rows,
            "complete": True,
            "created_at": utc_now(),
        },
    )
    return frame.reset_index(drop=True)


def _append_family_table_frames(
    run_tables: dict[str, list[pd.DataFrame]],
    family_tables_for_frames: dict[str, pd.DataFrame],
) -> None:
    for table_name, table_frame in family_tables_for_frames.items():
        if table_name in run_tables and not table_frame.empty:
            run_tables[table_name].append(table_frame.copy())


def _enforce_governed_association_lane_authority(
    family_tables_for_frames: dict[str, pd.DataFrame],
    *,
    registry: AssociationLaneRegistry,
    source: str,
    wave: str,
    country_code: str,
) -> dict[str, pd.DataFrame]:
    """Reconcile compiler outputs to governed lane/publishability authority.

    The joint-pattern implementation may apply stricter operational gates, but
    it may never promote a row that the governed registry marks non-publishable.
    Missing registry coverage is an authority failure, not permission to fall
    back to a hard-coded lane state machine.
    """
    governed_fields = {
        "association_lane": "lane",
        "association_lane_publishability": "publishability",
        "association_lane_rule_id": "rule_id",
        "association_lane_authority_source": "authority_source",
        "association_lane_authority_status": "authority_status",
    }
    reconciled = dict(family_tables_for_frames)
    for table_name, frame in family_tables_for_frames.items():
        if frame.empty or "associated_var_code" not in frame.columns:
            continue
        updated = frame.copy()
        keep_mask = pd.Series(True, index=updated.index, dtype=bool)
        for row_index, raw_var_code in updated["associated_var_code"].items():
            var_code = _safe_clean(raw_var_code).upper()
            if not var_code:
                raise RuntimeError(
                    f"V550J_ASSOCIATION_AUTHORITY_INVALID: blank associated_var_code in {table_name}"
                )
            result = registry.classify_required(
                var_code=var_code,
                source=source,
                wave=wave,
                country_code=country_code,
            )
            for column, attribute in governed_fields.items():
                if column in updated.columns:
                    updated.at[row_index, column] = getattr(result, attribute)
            if "association_lane_resolution_type" in updated.columns:
                updated.at[row_index, "association_lane_resolution_type"] = f"{result.match_type}_registry"
            registry_allows_publication = result.publishability == "publishable_lane"
            if not registry_allows_publication:
                keep_mask.at[row_index] = False
                if "would_emit_as_publishable" in updated.columns:
                    updated.at[row_index, "would_emit_as_publishable"] = False
                if "association_publication_status" in updated.columns:
                    updated.at[row_index, "association_publication_status"] = "blocked_registry_publishability"
                if "association_publication_reason" in updated.columns:
                    updated.at[row_index, "association_publication_reason"] = (
                        f"governed_registry_publishability={result.publishability};rule_id={result.rule_id}"
                    )
        if table_name == "joint_pattern_association_index":
            updated = updated.loc[keep_mask].reset_index(drop=True)
        reconciled[table_name] = updated
    return reconciled


class ProgressReporter:
    def __init__(self, *, enabled: bool, label: str = "V550J", stream=None) -> None:
        self.enabled = enabled
        self.label = label
        self.stream = stream if stream is not None else sys.stderr
        self.started_at = monotonic()
        self._active_stage_key: tuple[int, int, str] | None = None
        self._stage_started_at = self.started_at

    @staticmethod
    def _format_elapsed(seconds: float) -> str:
        seconds = max(0.0, float(seconds))
        minutes, secs = divmod(int(seconds), 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def stage(self, step: int, total: int, title: str, detail: str | None = None) -> None:
        if not self.enabled:
            return
        now = monotonic()
        stage_key = (int(step), int(total), str(title))
        if stage_key != self._active_stage_key:
            self._active_stage_key = stage_key
            self._stage_started_at = now
        total_elapsed = self._format_elapsed(now - self.started_at)
        stage_elapsed = self._format_elapsed(now - self._stage_started_at)
        suffix = f" | {detail}" if detail else ""
        print(
            f"[{self.label}] Stage {step}/{total}: {title} | total={total_elapsed} | stage={stage_elapsed}{suffix}",
            file=self.stream,
            flush=True,
        )

    def note(self, message: str) -> None:
        if not self.enabled:
            return
        elapsed = self._format_elapsed(monotonic() - self.started_at)
        print(f"[{self.label}] {elapsed} | {message}", file=self.stream, flush=True)

    @contextmanager
    def heartbeat(self, step: int, total: int, title: str, detail: str | None = None, *, every: float = 5.0):
        if not self.enabled:
            yield
            return
        stop_event = threading.Event()

        def _pulse() -> None:
            while not stop_event.wait(max(0.5, float(every))):
                self.stage(step, total, title, f"{detail} | still working" if detail else "still working")

        thread = threading.Thread(target=_pulse, name=f"{self.label}-heartbeat", daemon=True)
        thread.start()
        try:
            yield
        finally:
            stop_event.set()
            thread.join(timeout=1.0)


def _family_ids_from_frames(df: pd.DataFrame) -> list[str]:
    if df.empty or "family_id" not in df.columns:
        return []
    return sorted({_safe_clean(value) for value in df["family_id"].dropna().astype(str).tolist() if _safe_clean(value)})


def _semantic_extraction_metrics(item_index: pd.DataFrame, boundary_index: pd.DataFrame, funnel_index: pd.DataFrame) -> dict[str, Any]:
    if item_index.empty:
        return {
            "semantic_response_role_unknown_rate": 0.0,
            "semantic_response_role_resolved_rate": 0.0,
            "directionality_authority_missing_rate": 0.0,
            "family_registry_fallback_rate": 0.0,
            "upstream_response_option_authority_rate": 0.0,
            "target_registry_resolved_rate": 0.0,
            "target_condition_label_rate": 0.0,
            "target_group_rate": 0.0,
            "target_unresolved_rate": 0.0,
            "boundary_rule_matched_rate": 0.0,
            "mixed_unclassified_rate": 0.0,
            "association_context_available_rate": 0.0,
            "association_eligible_row_count": 0,
        }
    semantic_role = item_index["semantic_response_role"].astype(str).str.lower() if "semantic_response_role" in item_index.columns else pd.Series(["unknown"] * len(item_index))
    semantic_status = item_index["semantic_response_role_status"].astype(str).str.lower() if "semantic_response_role_status" in item_index.columns else pd.Series(["missing_or_unsigned_directionality_authority"] * len(item_index))
    response_semantics_source = item_index["response_semantics_authority_source"].astype(str).str.lower() if "response_semantics_authority_source" in item_index.columns else pd.Series(["none"] * len(item_index))
    target_grain = item_index["target_resolution_grain"].astype(str).str.lower() if "target_resolution_grain" in item_index.columns else pd.Series(["unresolved"] * len(item_index))
    target_status = item_index["target_resolution_status"].astype(str).str.lower() if "target_resolution_status" in item_index.columns else pd.Series(["unresolved"] * len(item_index))
    boundary_type = boundary_index["boundary_pattern_type"].astype(str).str.lower() if not boundary_index.empty and "boundary_pattern_type" in boundary_index.columns else pd.Series(dtype="object")
    funnel_status = funnel_index["association_context_status"].astype(str).str.lower() if not funnel_index.empty and "association_context_status" in funnel_index.columns else pd.Series(dtype="object")
    return {
        "semantic_response_role_unknown_rate": float((semantic_role == "unknown").mean()),
        "semantic_response_role_resolved_rate": float((semantic_role != "unknown").mean()),
        "directionality_authority_missing_rate": float(semantic_status.astype(str).str.contains("missing_or_unsigned|not_validated|label_mismatch|missing_label_guard", regex=True).mean()),
        "family_registry_fallback_rate": float(response_semantics_source.eq("question_family_registry.response_role_rules").mean()),
        "upstream_response_option_authority_rate": float(response_semantics_source.eq("response_option_map").mean()),
        "target_registry_resolved_rate": float(target_grain.eq("canonical_target_entity").mean()),
        "target_condition_label_rate": float(target_grain.eq("condition_label").mean()),
        "target_group_rate": float(target_grain.eq("target_group").mean()),
        "target_unresolved_rate": float(target_status.isin(["unresolved", "no_target_items"]).mean()),
        "boundary_rule_matched_rate": float((boundary_type != "mixed_unclassified").mean()) if not boundary_type.empty else 0.0,
        "mixed_unclassified_rate": float((boundary_type == "mixed_unclassified").mean()) if not boundary_type.empty else 0.0,
        "association_context_available_rate": float(funnel_status.isin(["outside_family_context_authorized", "not_empty"]).mean()) if not funnel_status.empty else 0.0,
        "association_eligible_row_count": int(funnel_index["eligible_association_rows"].sum()) if not funnel_index.empty and "eligible_association_rows" in funnel_index.columns else 0,
    }


def _validate_v550j_run_outputs(
    *,
    run_id: str,
    shard_id: str,
    family_summaries: list[dict[str, Any]],
    written_tables: dict[str, dict[str, Any]],
    table_frames: dict[str, pd.DataFrame],
    output_dir: Path,
    association_support_threshold: int,
) -> dict[str, Any]:
    compiled_family_ids = sorted({_safe_clean(item.get("family_id")) for item in family_summaries if _safe_clean(item.get("family_id"))})
    expected_family_set = set(compiled_family_ids)
    table_checks: list[dict[str, Any]] = []
    failures: list[str] = []
    source_id = shard_id.split("__")[0] if "__" in shard_id else "UNKNOWN"

    def _check_table(table_name: str, *, require_family_coverage: bool, allow_empty: bool = False) -> None:
        frame = table_frames.get(table_name, pd.DataFrame())
        actual_row_count = int(len(frame))
        manifest_row_count = int(written_tables.get(table_name, {}).get("rows", 0))
        family_ids_present = _family_ids_from_frames(frame)
        missing_family_ids = sorted(expected_family_set - set(family_ids_present)) if require_family_coverage and expected_family_set else []
        schema_valid = bool(written_tables.get(table_name, {}).get("schema_path"))
        row_count_valid = actual_row_count == manifest_row_count
        family_coverage_valid = True if allow_empty and actual_row_count == 0 else (not missing_family_ids if require_family_coverage else True)
        validation_status = "pass"
        validation_message = "ok"
        if not schema_valid:
            validation_status = "fail"
            validation_message = "missing schema path"
        elif not row_count_valid:
            validation_status = "fail"
            validation_message = f"row count mismatch: manifest={manifest_row_count}, actual={actual_row_count}"
        elif not family_coverage_valid:
            validation_status = "fail"
            validation_message = f"missing family_ids: {', '.join(missing_family_ids)}"
        elif actual_row_count == 0 and allow_empty:
            validation_status = "not_applicable"
            validation_message = "empty artifact is allowed"
        table_checks.append(
            {
                "run_id": run_id,
                "source_id": source_id or "UNKNOWN",
                "wave": shard_id.split("__")[-1] if "__" in shard_id else "",
                "country_code": "",
                "compiled_family_count": len(compiled_family_ids),
                "compiled_family_ids": compiled_family_ids,
                "artifact_name": table_name,
                "manifest_row_count": manifest_row_count,
                "actual_row_count": actual_row_count,
                "family_ids_expected": compiled_family_ids,
                "family_ids_present": family_ids_present,
                "family_ids_missing": missing_family_ids,
                "schema_valid": schema_valid,
                "row_count_valid": row_count_valid,
                "family_coverage_valid": family_coverage_valid,
                "validation_status": validation_status,
                "validation_message": validation_message,
            }
        )
        if validation_status == "fail":
            failures.append(f"{table_name}: {validation_message}")

    _check_table("joint_response_pattern_index", require_family_coverage=True)
    _check_table("question_family_boundary_pattern_index", require_family_coverage=True)
    _check_table("joint_pattern_relation_signature", require_family_coverage=True)
    _check_table("joint_pattern_position_signature", require_family_coverage=True)
    _check_table("joint_pattern_association_candidate_trace", require_family_coverage=True, allow_empty=True)
    _check_table("joint_pattern_association_review_surface", require_family_coverage=True, allow_empty=True)
    _check_table("joint_pattern_association_eligibility_funnel", require_family_coverage=True)
    _check_table("joint_pattern_meaning_summary", require_family_coverage=True, allow_empty=True)
    _check_table("joint_pattern_audit", require_family_coverage=True)
    _check_table("joint_response_pattern_item_index", require_family_coverage=True)
    _check_table("joint_pattern_respondent_membership", require_family_coverage=True, allow_empty=True)
    _check_table("joint_pattern_association_index", require_family_coverage=True, allow_empty=True)

    association_index_frame = table_frames.get("joint_pattern_association_index", pd.DataFrame())
    candidate_trace_frame = table_frames.get("joint_pattern_association_candidate_trace", pd.DataFrame())
    review_surface_frame = table_frames.get("joint_pattern_association_review_surface", pd.DataFrame())
    if not association_index_frame.empty and "association_publication_status" in association_index_frame.columns:
        invalid_publishable = association_index_frame[~association_index_frame["association_publication_status"].astype(str).eq("publishable")]
        if not invalid_publishable.empty:
            failures.append(f"joint_pattern_association_index: contains non-publishable rows ({len(invalid_publishable)})")
    if not association_index_frame.empty:
        blank_identity_mask = (
            association_index_frame[[column for column in ["run_id", "source_id", "source", "wave", "canonical_wave", "country_code", "family_id", "pattern_id"] if column in association_index_frame.columns]]
            .fillna("")
            .astype(str)
            .eq("")
            .any(axis=1)
        )
        if bool(blank_identity_mask.any()):
            failures.append(f"joint_pattern_association_index: blank identity fields ({int(blank_identity_mask.sum())})")
    if not candidate_trace_frame.empty and "association_lane" in candidate_trace_frame.columns:
        lane_count = int(candidate_trace_frame["association_lane"].astype(str).nunique(dropna=True))
        if lane_count == 1 and candidate_trace_frame["association_lane"].astype(str).eq("substantive_attitude_association").all():
            failures.append("joint_pattern_association_candidate_trace: association lane collapse detected")
    if not candidate_trace_frame.empty and {"associated_var_code", "association_lane"}.issubset(candidate_trace_frame.columns):
        known_bad = candidate_trace_frame[
            candidate_trace_frame["associated_var_code"].astype(str).str.upper().isin({"RACE", "OCC", "OCC10", "ISCO08", "PAEDUC", "MAEDUC", "SPEDUC", "REG16", "SIZE", "AGEWED"})
            & candidate_trace_frame["association_lane"].astype(str).eq("substantive_attitude_association")
        ]
        if not known_bad.empty:
            failures.append(f"joint_pattern_association_candidate_trace: known context/status vars misclassified as substantive attitude ({len(known_bad)})")
    if not review_surface_frame.empty and "association_lane_publishability" in review_surface_frame.columns:
        blocked_in_review = review_surface_frame[review_surface_frame["association_lane_publishability"].astype(str).eq("blocked_lane")]
        if not blocked_in_review.empty:
            failures.append(f"joint_pattern_association_review_surface: blocked lanes leaked into review surface ({len(blocked_in_review)})")

    if not association_index_frame.empty:
        overlap = pd.to_numeric(association_index_frame.get("n_overlap_unweighted", pd.Series(0)), errors="coerce").fillna(0)
        below_threshold = int((overlap < int(association_support_threshold)).sum())
        if below_threshold > 0:
            failures.append(
                "joint_pattern_association_index: contains "
                f"{below_threshold} rows with n_overlap < governed threshold {association_support_threshold}"
            )
        occ_rows = int((association_index_frame.get("is_raw_occupational_status_code", pd.Series(False)).map(lambda v: _to_bool(v, False))).sum())
        if occ_rows > 0:
            failures.append(f"joint_pattern_association_index: contains {occ_rows} raw occupational/status code rows")
        high_card_rows = int((association_index_frame.get("is_high_cardinality_associated_var", pd.Series(False)).map(lambda v: _to_bool(v, False))).sum())
        if high_card_rows > 0:
            failures.append(f"joint_pattern_association_index: contains {high_card_rows} high-cardinality rows")
        sparse_rows = int((association_index_frame.get("is_sparse_associated_response", pd.Series(False)).map(lambda v: _to_bool(v, False))).sum())
        if sparse_rows > 0:
            failures.append(f"joint_pattern_association_index: contains {sparse_rows} sparse response rows")
        same_fam_rows = int((association_index_frame.get("is_same_family_association", pd.Series(False)).map(lambda v: _to_bool(v, False))).sum())
        if same_fam_rows > 0:
            failures.append(f"joint_pattern_association_index: contains {same_fam_rows} same-family leakage rows")
        same_var_rows = int((association_index_frame.get("is_same_variable_association", pd.Series(False)).map(lambda v: _to_bool(v, False))).sum())
        if same_var_rows > 0:
            failures.append(f"joint_pattern_association_index: contains {same_var_rows} same-variable leakage rows")

    overall_status = "pass" if not failures else "fail"
    report = {
        "run_id": run_id,
        "source_id": source_id or "UNKNOWN",
        "wave": shard_id.split("__")[-1] if "__" in shard_id else "",
        "country_code": "",
        "compiled_family_count": len(compiled_family_ids),
        "compiled_family_ids": compiled_family_ids,
        "artifact_name": "v550j_run",
        "manifest_row_count": sum(int(item.get("rows", 0)) for item in written_tables.values()),
        "actual_row_count": sum(int(len(frame)) for frame in table_frames.values()),
        "family_ids_expected": compiled_family_ids,
        "family_ids_present": sorted({family_id for frame in table_frames.values() for family_id in _family_ids_from_frames(frame)}),
        "family_ids_missing": sorted(expected_family_set - {family_id for frame in table_frames.values() for family_id in _family_ids_from_frames(frame)}),
        "schema_valid": True,
        "row_count_valid": not failures,
        "family_coverage_valid": not failures,
        "validation_status": overall_status,
        "validation_message": "ok" if not failures else "; ".join(failures),
        "association_support_threshold": int(association_support_threshold),
        "table_checks": table_checks,
    }
    atomic_write_json(output_dir / "v550j_output_validation_report.json", report)
    return report


def _load_response_map(path: Path, db_conn) -> pd.DataFrame:
    if path.exists():
        return read_table_any(path)
    if db_conn is None:
        raise RuntimeError(f"Missing response option map and no database connection was provided: {path}")
    response_map, _, _ = build_response_option_map(db_conn=db_conn)
    return response_map


def _normalize_semantics_key_value(value: Any) -> str:
    text = _safe_clean(value)
    if not text:
        return ""
    if text.endswith(".0"):
        prefix = text[:-2]
        if prefix.replace("-", "", 1).isdigit():
            return prefix
    return text


def _expand_response_semantics_lookup(response_map: pd.DataFrame, base_lookup: dict[tuple[str, str, str, str], dict[str, Any]]) -> dict[tuple[str, str, str, str], dict[str, Any]]:
    if response_map.empty:
        return base_lookup
    expanded = dict(base_lookup)
    for row in response_map.itertuples(index=False):
        row_dict = row._asdict()
        source = _normalize_semantics_key_value(row_dict.get("source"))
        wave_values = {
            _normalize_semantics_key_value(row_dict.get("wave")),
            _normalize_semantics_key_value(row_dict.get("canonical_wave")),
        }
        var_values = {
            _normalize_semantics_key_value(row_dict.get("var_name")),
            _normalize_semantics_key_value(row_dict.get("var_code")),
        }
        candidate_values = {
            _normalize_semantics_key_value(row_dict.get("value_code_normalized")),
            _normalize_semantics_key_value(row_dict.get("value_label_clean")),
            _normalize_semantics_key_value(row_dict.get("normalized_response_label")),
        }
        candidate_values = {value for value in candidate_values if value}
        for wave in wave_values:
            if not wave:
                continue
            for var_name in var_values:
                if not var_name:
                    continue
                for candidate in candidate_values:
                    expanded[(source, wave, var_name, candidate)] = row_dict
    return expanded


def _load_cached_country_slice(
    *,
    source: str,
    waves: list[str],
    country_code: str,
    response_semantics_contract_hash: str = "",
    db_conn=None,
    force_db: bool = False,
    view_name: str = "v_ddm_response_long_facet_ready",
    chunk_size: int = 25000,
    progress: ProgressReporter | None = None,
    var_codes: list[str] | None = None,
) -> pd.DataFrame | None:
    scoped_var_codes = sorted({str(value).strip().upper() for value in (var_codes or []) if str(value).strip()})
    payload_variants = [
        {
            "query": f"{view_name}_country_slice",
            "source": source,
            "waves": waves,
            "country_code": country_code,
            "var_codes": scoped_var_codes,
            "response_semantics_contract_hash": response_semantics_contract_hash,
        },
        {
            "query": f"{view_name}_country_slice",
            "source": source,
            "waves": waves,
            "country_code": country_code,
            "var_codes": scoped_var_codes,
            "response_semantics_contract_hash": "",
        },
        {
            "query": f"{view_name}_country_slice",
            "source": source,
            "waves": waves,
            "country_code": country_code,
            "var_codes": scoped_var_codes,
        },
        {
            "query": f"{view_name}_slice",
            "source": source,
            "waves": waves,
            "country_code": country_code,
            "projection": "*",
            "var_codes": scoped_var_codes,
            "response_semantics_contract_hash": response_semantics_contract_hash,
        },
        {
            "query": f"{view_name}_slice",
            "source": source,
            "waves": waves,
            "country_code": country_code,
            "projection": "*",
            "var_codes": scoped_var_codes,
        },
    ]
    if not force_db:
        for payload in payload_variants:
            signature = cache_signature({"cache_format_version": "v2", "payload": payload})
            entry = cache_entry("responses", signature, cache_root=shared_cache_root())
            cached = load_cached_frame(entry, expected_signature=signature)
            if cached is not None and not cached.empty:
                return cached.reset_index(drop=True)
    if db_conn is None:
        return None

    def _sql_literal(value: Any) -> str:
        return "'" + str(value).replace("'", "''") + "'"

    wave_literals = [f"canonical_wave = {_sql_literal(value)}" for value in waves if str(value).strip()]
    wave_clause = " OR ".join(wave_literals)
    if not wave_clause:
        wave_clause = "1=1"
    var_clause = ""
    if scoped_var_codes:
        var_literals = ", ".join(_sql_literal(value) for value in scoped_var_codes)
        var_clause = f"\n          AND upper(var_code) IN ({var_literals})"
    country_sql = """
        SELECT *
        FROM {view_name}
        WHERE source = '{source}'
          AND ({wave_clause})
          AND country_code = '{country_code}'
          {var_clause}
        ORDER BY var_code, respondent_id
    """.format(
        view_name=view_name,
        source=str(source).replace("'", "''"),
        wave_clause=wave_clause,
        country_code=str(country_code).replace("'", "''"),
        var_clause=var_clause,
    )
    payload = {
        "query": f"{view_name}_country_slice",
        "source": source,
        "waves": waves,
        "country_code": country_code,
        "var_codes": scoped_var_codes,
        "response_semantics_contract_hash": response_semantics_contract_hash,
    }
    signature = cache_signature({"cache_format_version": "v2", "payload": payload})
    entry = cache_entry("responses", signature, cache_root=shared_cache_root())
    queried = _load_sql_query_in_chunks(
        country_sql,
        db_conn,
        chunk_size=chunk_size,
        cache_entry_obj=entry,
        cache_payload={**payload, "query_signature": signature},
        progress=progress,
        progress_title=f"{view_name} country slice",
        bypass_existing_cache=force_db,
    )
    if queried is None or queried.empty:
        return None
    return queried.reset_index(drop=True)


def _load_all_countries_context_slice(
    *,
    source: str,
    waves: list[str],
    response_semantics_contract_hash: str = "",
    db_conn=None,
    view_name: str = "v_ddm_response_long_facet_ready",
    chunk_size: int = 25000,
    progress: ProgressReporter | None = None,
) -> pd.DataFrame | None:
    payload_variants = [
        {
            "query": f"{view_name}_all_countries",
            "source": source,
            "waves": waves,
            "response_semantics_contract_hash": response_semantics_contract_hash,
        },
        {
            "query": f"{view_name}_all_countries",
            "source": source,
            "waves": waves,
        },
    ]
    for payload in payload_variants:
        signature = cache_signature({"cache_format_version": "v2", "payload": payload})
        entry = cache_entry("responses", signature, cache_root=shared_cache_root())
        cached = load_cached_frame(entry, expected_signature=signature)
        if cached is not None and not cached.empty:
            if "var_code" in cached.columns:
                cached = cached.copy()
                cached["var_code"] = cached["var_code"].astype(str).str.upper()
                cached = cached.set_index("var_code", drop=False)
            return cached.reset_index(drop=True)
    if db_conn is None:
        return None

    def _sql_literal(value: Any) -> str:
        return "'" + str(value).replace("'", "''") + "'"

    wave_literals = [f"canonical_wave = {_sql_literal(value)}" for value in waves if str(value).strip()]
    wave_clause = " OR ".join(wave_literals) if wave_literals else "1=1"
    country_sql = """
        SELECT *
        FROM {view_name}
        WHERE source = {source}
          AND ({wave_clause})
        ORDER BY country_code, var_code, respondent_id
    """.format(
        view_name=view_name,
        source=_sql_literal(source),
        wave_clause=wave_clause,
    )
    payload = {
        "query": f"{view_name}_all_countries",
        "source": source,
        "waves": waves,
        "response_semantics_contract_hash": response_semantics_contract_hash,
    }
    signature = cache_signature({"cache_format_version": "v2", "payload": payload})
    entry = cache_entry("responses", signature, cache_root=shared_cache_root())
    queried = _load_sql_query_in_chunks(
        country_sql,
        db_conn,
        chunk_size=chunk_size,
        cache_entry_obj=entry,
        cache_payload={**payload, "query_signature": signature},
        progress=progress,
        progress_title=f"{view_name} all countries slice",
        bypass_existing_cache=False,
    )
    if queried is None or queried.empty:
        return None
    return queried.reset_index(drop=True)


def main() -> int:
    args = parse_args()
    if not args.write_parquet:
        raise RuntimeError("V550J_CANONICAL_PARQUET_REQUIRED")
    explicit_prepared_frame: pd.DataFrame | None = None
    explicit_prepared_manifest: dict[str, Any] = {}
    if args.forbid_database_access:
        if args.db_url:
            raise RuntimeError("V550J_DATABASE_ACCESS_FORBIDDEN: --db-url is not allowed")
        if os.environ.get("DATABASE_URL"):
            raise RuntimeError("V550J_DATABASE_ACCESS_FORBIDDEN: DATABASE_URL is not allowed")
        if args.v550j_substrate_mode != "prepared_required":
            raise RuntimeError("V550J_DATABASE_ACCESS_FORBIDDEN: prepared_required is mandatory")
        if not args.prepared_substrate_path or not args.prepared_substrate_manifest_path:
            raise RuntimeError("V550J_DATABASE_ACCESS_FORBIDDEN: explicit prepared substrate path and manifest are required")
        if not Path(args.prepared_substrate_path).exists():
            raise RuntimeError(f"V550J_DATABASE_ACCESS_FORBIDDEN: prepared substrate missing: {args.prepared_substrate_path}")
        if not Path(args.prepared_substrate_manifest_path).exists():
            raise RuntimeError(f"V550J_DATABASE_ACCESS_FORBIDDEN: prepared substrate manifest missing: {args.prepared_substrate_manifest_path}")
        if not Path(args.response_option_map).exists():
            raise RuntimeError("V550J_DATABASE_ACCESS_FORBIDDEN: response-option map artifact is required")
        explicit_prepared_manifest = json.loads(Path(args.prepared_substrate_manifest_path).read_text(encoding="utf-8"))
        explicit_prepared_frame = pd.read_parquet(Path(args.prepared_substrate_path))
        explicit_validation = validate_shared_respondent_substrate(explicit_prepared_frame, explicit_prepared_manifest)
        if explicit_validation["validation_status"] != "pass":
            raise RuntimeError(f"V550J_DATABASE_ACCESS_FORBIDDEN: prepared substrate validation failed: {explicit_validation['validation_message']}")
        manifest_hash = str(explicit_prepared_manifest.get("content_hash", "")).strip()
        if manifest_hash and logical_shared_substrate_hash(explicit_prepared_frame) != manifest_hash:
            raise RuntimeError("V550J_DATABASE_ACCESS_FORBIDDEN: prepared substrate content hash mismatch")
    diagnostics_enabled = bool(args.with_diagnostics)
    publish_association_lanes = {lane.strip() for lane in str(args.publish_association_lanes or "").split(",") if lane.strip()}
    association_support_threshold_override = (
        int(args.association_support_threshold)
        if args.association_support_threshold is not None
        else None
    )
    association_support_threshold = 0
    threshold_profile_id = "unresolved"
    threshold_profile: dict[str, Any] = {}
    progress = ProgressReporter(enabled=bool(args.progress), label="V550J")
    performance_stages: list[dict[str, Any]] = []
    harmonization_stats: Counter[str] = Counter()

    def _record_stage(stage_name: str, started_at: float, *, input_rows: int = 0, output_rows: int = 0, extra: dict[str, Any] | None = None) -> None:
        elapsed_seconds = max(0.0, monotonic() - started_at)
        rows_per_second = (float(output_rows) / elapsed_seconds) if elapsed_seconds > 0 and output_rows >= 0 else None
        stage_payload = {
            "stage_name": stage_name,
            "elapsed_seconds": elapsed_seconds,
            "input_rows": int(input_rows),
            "output_rows": int(output_rows),
            "rows_per_second": rows_per_second if rows_per_second is not None else 0.0,
        }
        if extra:
            stage_payload.update(extra)
        performance_stages.append(stage_payload)

    load_inputs_started = monotonic()
    progress.stage(1, 6, "Load shard inputs", "starting")
    if not args.forbid_database_access:
        load_dotenv(Path(args.env_file))
    shard_dir = Path(args.v550_shard_dir)
    if not shard_dir.exists():
        raise RuntimeError(f"Shard directory does not exist: {shard_dir}")
    shard_id = shard_dir.name
    run_id = shard_dir.parent.name

    question_use_contract_path = shard_dir / "core" / "question_use_contract.parquet"
    shard_scope_path = shard_dir / "shard_scope.parquet"
    if not question_use_contract_path.exists():
        raise RuntimeError(f"Missing question_use_contract parquet: {question_use_contract_path}")
    if not shard_scope_path.exists():
        raise RuntimeError(f"Missing shard_scope parquet: {shard_scope_path}")

    question_use_contract = pd.read_parquet(question_use_contract_path)
    shard_scope = pd.read_parquet(shard_scope_path)
    source_raw = _single_scope_value(shard_scope, ("source", "source_family"), "source")
    if not source_raw:
        source_raw = _single_scope_value(
            question_use_contract, ("source", "source_family"), "source"
        )
    wave_raw = _single_scope_value(
        shard_scope, ("canonical_wave", "wave"), "wave"
    )
    if not wave_raw:
        wave_raw = _single_scope_value(
            question_use_contract, ("canonical_wave", "wave"), "wave"
        )
    country_codes = list(
        dict.fromkeys(
            _safe_clean(value).upper()
            for value in shard_scope.get(
                "country_code", pd.Series(dtype="object")
            ).dropna()
            if _safe_clean(value)
        )
    )
    if not country_codes:
        raise SurveyIdentityError(
            "V550J shard country_code is required; no country fallback is allowed"
        )
    identity = require_survey_identity(
        source_raw,
        wave_raw,
        country_codes[0],
        require_country=True,
    )
    source = identity.source
    canonical_wave = identity.canonical_wave
    progress.stage(
        1,
        6,
        "Load shard inputs",
        f"question_use_contract_rows={len(question_use_contract)} shard_scope_rows={len(shard_scope)}",
    )
    _record_stage(
        "load_shard_inputs",
        load_inputs_started,
        input_rows=0,
        output_rows=len(question_use_contract) + len(shard_scope),
        extra={"question_use_contract_rows": int(len(question_use_contract)), "shard_scope_rows": int(len(shard_scope))},
    )
    load_registries_started = monotonic()
    progress.stage(2, 6, "Load registries and response semantics", "starting")
    registry = _load_yaml(Path(args.registry_path))
    families = registry.get("families", [])
    if not isinstance(families, list):
        raise RuntimeError("question_family_registry.yaml is malformed: families must be a list")
    bounded_authority_validation = _validate_bounded_authority_registry(registry)

    association_mode_enabled = args.association_mode != "off"
    association_lane_registry = AssociationLaneRegistry(
        path=Path(args.association_lane_registry_path) if args.association_lane_registry_path else None
    )
    if association_mode_enabled:
        association_lane_registry.load()

    threshold_payload = (
        _load_yaml(Path(args.association_threshold_profiles_path))
        if association_mode_enabled
        else {"profiles": {}}
    )
    effective_n_values: list[float] = []
    for frame in (shard_scope, question_use_contract):
        if "n_respondents" in frame.columns:
            effective_n_values.extend(
                pd.to_numeric(frame["n_respondents"], errors="coerce")
                .dropna()
                .astype(float)
                .tolist()
            )
    effective_n = int(max(effective_n_values)) if effective_n_values else 0
    if association_mode_enabled:
        threshold_profile_id, threshold_profile = _select_threshold_profile(
            threshold_payload,
            source=source,
            effective_n=effective_n,
        )
        profile_min_overlap = int(
            (threshold_profile.get("publishable_attitude") or {}).get("min_overlap")
            or 0
        )
    else:
        threshold_profile_id, threshold_profile, profile_min_overlap = (
            "not_applicable_association_mode_off",
            {},
            0,
        )
    association_support_threshold = (
        association_support_threshold_override
        if association_support_threshold_override is not None
        else profile_min_overlap
    )

    response_map_path = Path(args.response_option_map)
    conn = None if response_map_path.exists() else connect_from_env(args.db_url, Path(args.env_file))
    response_map = _load_response_map(response_map_path, conn)
    semantics_lookup = _expand_response_semantics_lookup(response_map, _lookup_response_semantics(response_map) if not response_map.empty else {})
    semantics_contract = response_semantics_contract_hash(response_map) if not response_map.empty else ""
    progress.stage(
        2,
        6,
        "Load registries and response semantics",
        f"families={len(families)} response_map_rows={len(response_map)}",
    )
    _record_stage(
        "load_registries_and_response_semantics",
        load_registries_started,
        input_rows=len(question_use_contract),
        output_rows=len(response_map),
        extra={"families": int(len(families))},
    )

    def _ensure_db_conn():
        nonlocal conn
        if args.forbid_database_access:
            raise RuntimeError("V550J_DATABASE_ACCESS_FORBIDDEN: attempted PostgreSQL connection after no-DB gate")
        if conn is not None:
            return conn
        try:
            conn = connect_from_env(args.db_url, Path(args.env_file))
        except Exception:
            conn = None
        return conn

    def _prepare_association_context_frame(frame: pd.DataFrame | None, *, full_harmonization: bool = False) -> pd.DataFrame | None:
        if frame is None or frame.empty:
            return frame
        prepared = frame.copy()
        if full_harmonization and any(column in prepared.columns for column in ("value_text", "value_raw", "response_label", "normalized_response_label")):
            try:
                prepared = _harmonize_question_frame(
                    prepared,
                    semantics_lookup,
                    response_semantics_contract_hash=semantics_contract,
                )
                harmonization_stats["forensic_harmonized_rows"] += int(len(prepared))
                harmonization_stats["forensic_harmonization_calls"] += 1
            except Exception:
                pass
        if "response_value_normalized" not in prepared.columns:
            prepared["response_value_normalized"] = ""
        prepared["response_value_normalized"] = prepared["response_value_normalized"].fillna("").astype(str).str.strip()
        if "response_label" not in prepared.columns:
            prepared["response_label"] = ""
        prepared["response_label"] = prepared["response_label"].fillna("").astype(str).str.strip()
        if "normalized_response_label" not in prepared.columns:
            prepared["normalized_response_label"] = ""
        prepared["normalized_response_label"] = prepared["normalized_response_label"].fillna("").astype(str).str.strip()
        if prepared["response_value_normalized"].eq("").any():
            fallback_series = pd.Series("", index=prepared.index, dtype="object")
            for column in ("response_value_normalized", "normalized_response_label", "response_label", "value_raw", "value_text"):
                if column not in prepared.columns:
                    continue
                candidate_values = _response_value_series(prepared[column])
                if candidate_values.ne("").any():
                    missing_mask = prepared["response_value_normalized"].eq("")
                    fallback_series = fallback_series.where(~missing_mask, candidate_values)
            missing_mask = prepared["response_value_normalized"].eq("")
            if fallback_series.ne("").any():
                prepared.loc[missing_mask, "response_value_normalized"] = fallback_series[missing_mask]
        if prepared["response_label"].eq("").any():
            missing_mask = prepared["response_label"].eq("")
            prepared.loc[missing_mask, "response_label"] = prepared.loc[missing_mask, "response_value_normalized"]
        if prepared["normalized_response_label"].eq("").any():
            missing_mask = prepared["normalized_response_label"].eq("")
            prepared.loc[missing_mask, "normalized_response_label"] = prepared.loc[missing_mask, "response_value_normalized"]
        return prepared.reset_index(drop=True)

    tables: dict[str, list[pd.DataFrame]] = {
        "joint_response_pattern_index": [],
        "joint_response_pattern_item_index": [],
        "question_family_boundary_pattern_index": [],
        "joint_pattern_position_signature": [],
        "joint_pattern_relation_signature": [],
        "joint_pattern_respondent_membership": [],
        "joint_pattern_audit": [],
        "joint_pattern_association_index": [],
        "joint_pattern_association_review_surface": [],
        "joint_pattern_meaning_summary": [],
    }
    if diagnostics_enabled:
        tables["joint_pattern_association_candidate_trace"] = []
        tables["joint_pattern_association_eligibility_funnel"] = []
    run_tables: dict[str, list[pd.DataFrame]] = {
        key: []
        for key in tables
        if diagnostics_enabled or key not in {"joint_pattern_association_candidate_trace", "joint_pattern_association_eligibility_funnel", "joint_pattern_audit"}
    }
    family_summaries: list[dict[str, Any]] = []
    prepared_validation_report_path = ""
    registry_source = _safe_clean(registry.get("source_family"))
    registry_governance_status = _safe_clean(registry.get("status"))
    canonical_scope_wave = canonical_wave_key(source, canonical_wave)
    active_families = [
        family_cfg
        for family_cfg in families
        if isinstance(family_cfg, dict)
        and _safe_clean(family_cfg.get("family_id"))
        and family_keys_equal(
            _safe_clean(family_cfg.get("source_family")) or registry_source,
            source,
        )
        and (
            not _family_waves(family_cfg, source)
            or canonical_scope_wave in _family_waves(family_cfg, source)
        )
    ]
    if active_families:
        require_executable_registry_status(
            registry_governance_status,
            authority_name="V550J question-family registry",
            path=args.registry_path,
        )
        registry_scope_status = "applicable"
    else:
        registry_scope_status = "not_applicable"
    active_family_total = len(active_families)
    active_family_index = 0
    family_lookup_rows: list[dict[str, Any]] = []
    for family_cfg in active_families:
        family_id = _safe_clean(family_cfg.get("family_id"))
        for family_item_order, item in enumerate(_family_item_map(family_cfg), start=1):
            var_code = _safe_clean(item.get("var_code")).upper()
            if not var_code:
                continue
            family_lookup_rows.append(
                {
                    "family_id": family_id,
                    "var_code_norm": var_code,
                    "item_role": _safe_clean(item.get("item_role")) or "target_case",
                    "condition_label": _safe_clean(item.get("condition_label")),
                    "family_item_order": family_item_order,
                    "minimum_items_answered": int(_safe_clean(family_cfg.get("minimum_items_answered")) or 1),
                    "family_label": _safe_clean(family_cfg.get("family_label", family_id)),
                    "family_type": _safe_clean(family_cfg.get("family_type", "")),
                }
            )
    active_family_lookup_df = pd.DataFrame(family_lookup_rows) if family_lookup_rows else pd.DataFrame(columns=["family_id", "var_code_norm", "item_role", "condition_label", "family_item_order", "minimum_items_answered", "family_label", "family_type"])
    country_prepared_state: dict[tuple[str, str, str], dict[str, Any]] = {}
    progress.stage(3, 6, "Process families", f"families={active_family_total}")

    for family_cfg in active_families:
        active_family_index += 1
        family_id = _safe_clean(family_cfg.get("family_id"))
        family_var_codes = [item["var_code"].upper() for item in _family_item_map(family_cfg)]
        if not family_var_codes:
            continue
        progress.stage(3, 6, "Process families", f"family {active_family_index}/{active_family_total}: {family_id} loading questions")

        family_questions = question_use_contract[
            question_use_contract["var_code"].astype(str).str.upper().isin(family_var_codes)
        ].copy()
        if "source" not in family_questions.columns:
            family_questions = family_questions.iloc[0:0].copy()
        elif not family_questions.empty:
            family_questions = family_questions[
                family_questions["source"].map(
                    lambda value: family_keys_equal(value, source)
                )
            ].copy()
        question_filter = _load_question_filter(args.question_filter_file)
        if question_filter and not family_questions.empty:
            question_filter_cols = [column for column in ["question_id", "var_code", "var_name", "name"] if column in family_questions.columns]
            if question_filter_cols:
                filter_mask = pd.Series(False, index=family_questions.index)
                for column in question_filter_cols:
                    filter_mask = filter_mask | family_questions[column].fillna("").astype(str).str.upper().isin(question_filter)
                filtered_rows = int(filter_mask.sum())
                if filtered_rows > 0:
                    family_questions = family_questions.loc[filter_mask].copy()
                else:
                    family_questions = family_questions.iloc[0:0].copy()
        if family_questions.empty:
            tables["joint_pattern_audit"].append(
                pd.DataFrame(
                    [
                        {
                            "family_id": family_id,
                            "issue_type": "family_not_found_in_contract",
                            "severity": "high",
                            "item_count": 0,
                            "respondent_count": 0,
                            "detail": "No approved family questions were present in the shard contract.",
                            "action": "family skipped",
                            "created_at": utc_now(),
                            "schema_version": V550J_SCHEMA_VERSION,
                        }
                    ]
                )
            )
            continue
        if "canonical_wave" not in family_questions.columns:
            family_questions["canonical_wave"] = family_questions.get("wave", "")
        if "source" not in family_questions.columns:
            family_questions["source"] = ""

        eligible_waves = _family_waves(family_cfg, source)
        question_wave_values = _family_wave_values(family_questions, source)
        if eligible_waves and question_wave_values and question_wave_values.isdisjoint(eligible_waves):
            tables["joint_pattern_audit"].append(
                pd.DataFrame(
                    [
                        {
                            "family_id": family_id,
                            "issue_type": "family_wave_not_eligible",
                            "severity": "high",
                            "item_count": int(len(family_questions)),
                            "respondent_count": 0,
                            "detail": f"Family waves {sorted(question_wave_values)} are not in eligible_waves {sorted(eligible_waves)}.",
                            "action": "family skipped",
                            "created_at": utc_now(),
                            "schema_version": V550J_SCHEMA_VERSION,
                        }
                    ]
                )
            )
            continue

        for country_code in country_codes:
            progress.stage(
                3,
                6,
                "Process families",
                f"family {active_family_index}/{active_family_total}: {family_id} country={country_code} loading context",
            )
            association_db_conn = None if explicit_prepared_frame is not None else _ensure_db_conn()
            facet_ready_view_name = "" if association_db_conn is None else _facet_ready_view_name(association_db_conn)
            country_questions = family_questions.copy()
            country_questions["country_code"] = country_code
            country_questions["raw_wave"] = country_questions.get("wave", "").astype(str)
            country_questions["canonical_wave"] = country_questions.get("canonical_wave", country_questions.get("wave", "")).astype(str)
            country_var_codes = (
                country_questions["var_code"].dropna().astype(str).str.upper().drop_duplicates().tolist()
                if "var_code" in country_questions.columns
                else family_var_codes
            )
            source_value = (
                _safe_clean(country_questions["source"].iloc[0])
                if "source" in country_questions.columns and not country_questions.empty
                else ""
            )
            require_survey_identity(
                source_value,
                canonical_wave,
                country_code,
                require_country=True,
            )
            wave_values = sorted(
                {
                    value
                    for value in (
                        country_questions["raw_wave"].iloc[0] if "raw_wave" in country_questions.columns and not country_questions.empty else "",
                        country_questions["canonical_wave"].iloc[0] if "canonical_wave" in country_questions.columns and not country_questions.empty else "",
                    )
                    if str(value).strip()
                }
            )
            with progress.heartbeat(
                3,
                6,
                "Association context",
                f"family {active_family_index}/{active_family_total}: {family_id} country={country_code} loading cached country slice",
                every=5.0,
            ):
                if explicit_prepared_frame is not None:
                    prepared_scope = explicit_prepared_frame.copy()
                    if "country_code_norm" in prepared_scope.columns:
                        prepared_scope = prepared_scope[prepared_scope["country_code_norm"].fillna("").astype(str).str.upper() == str(country_code).upper()].copy()
                    if "var_code_norm" in prepared_scope.columns:
                        prepared_scope = prepared_scope[prepared_scope["var_code_norm"].fillna("").astype(str).str.upper().isin({code.upper() for code in country_var_codes})].copy()
                    cached_country_frame = prepared_scope.reset_index(drop=True)
                else:
                    cached_country_frame = _load_cached_country_slice(
                        source=source_value,
                        waves=wave_values or [""],
                        country_code=country_code,
                        response_semantics_contract_hash=semantics_contract,
                        db_conn=association_db_conn,
                        view_name=facet_ready_view_name,
                        chunk_size=int(args.association_fetch_chunk_size),
                        progress=progress,
                        var_codes=country_var_codes,
                    )
            if cached_country_frame is not None:
                progress.stage(
                    3,
                    6,
                    "Association context",
                    f"family {active_family_index}/{active_family_total}: {family_id} country={country_code} cached_context_rows={len(cached_country_frame)}",
                )
            else:
                progress.stage(
                    3,
                    6,
                    "Association context",
                    f"family {active_family_index}/{active_family_total}: {family_id} country={country_code} cached_context_rows=0",
                )
            if cached_country_frame is not None:
                cached_country_frame = cached_country_frame.copy()
                if "var_code" in cached_country_frame.columns:
                    cached_country_frame["var_code"] = cached_country_frame["var_code"].astype(str).str.upper()
                    cached_country_frame = cached_country_frame.set_index("var_code", drop=False)
                question_row_cache = {country_code: cached_country_frame}
            else:
                if args.forbid_database_access:
                    raise RuntimeError(f"V550J_DATABASE_ACCESS_FORBIDDEN: no prepared substrate rows for {family_id} {country_code}")
                with progress.heartbeat(
                    3,
                    6,
                    "Association context",
                    f"family {active_family_index}/{active_family_total}: {family_id} country={country_code} prefetching question rows",
                    every=5.0,
                ):
                    question_row_cache = _prefetch_question_rows_by_country(
                        conn,
                        country_questions,
                        response_semantics_contract_hash=semantics_contract,
                    )

            prepared_country_frame: pd.DataFrame | None = None
            all_family_rows: pd.DataFrame | None = None
            cache_key = (source_value, "|".join(wave_values or [""]), country_code)
            country_state = country_prepared_state.get(cache_key)
            if country_state is None:
                if (cached_country_frame is not None and not cached_country_frame.empty) or args.v550j_substrate_mode == "prepared_required":
                    source_frame_for_loader = cached_country_frame.reset_index(drop=True) if cached_country_frame is not None and not cached_country_frame.empty else pd.DataFrame()
                    prepared_started = monotonic()
                    if explicit_prepared_frame is not None:
                        prepared_country_frame = source_frame_for_loader
                        prepared_manifest = {
                            **explicit_prepared_manifest,
                            "cache_loaded": True,
                            "explicit_prepared_substrate_path": str(args.prepared_substrate_path),
                            "explicit_prepared_substrate_manifest_path": str(args.prepared_substrate_manifest_path),
                        }
                    else:
                        prepared_country_frame, prepared_manifest = load_or_build_v550j_prepared_substrate(
                            run_id=run_id,
                            source=source_value,
                            source_id=source_value,
                            wave=wave_values[0] if wave_values else "",
                            canonical_wave=wave_values[-1] if wave_values else "",
                            country_code=country_code,
                            source_frame=source_frame_for_loader,
                            semantics_lookup=semantics_lookup,
                            response_semantics_contract_hash=semantics_contract,
                            output_root=Path(args.output_root),
                            question_family_registry_hash=_stable_hash(registry),
                            authority_compendium_hash=semantics_contract,
                            view_schema_hash=_stable_hash({"columns": list(cached_country_frame.columns)}),
                            compiler_version=V550J_SCHEMA_VERSION,
                            substrate_mode=args.v550j_substrate_mode,
                            progress=progress,
                        )
                    if args.v550j_substrate_mode == "prepared_required" and prepared_country_frame.empty:
                        raise RuntimeError(f"Prepared substrate is required but empty for {family_id} {country_code}")
                    _record_stage(
                        "load_or_build_prepared_substrate",
                        prepared_started,
                        input_rows=len(cached_country_frame),
                        output_rows=len(prepared_country_frame),
                        extra={
                            "family_id": family_id,
                            "country_code": country_code,
                            "cache_loaded": bool(prepared_manifest.get("cache_loaded", False)),
                            **({} if bool(prepared_manifest.get("cache_loaded", False)) else {"harmonization_calls": int(prepared_manifest.get("harmonization_calls", 0) or 0)}),
                            **({"cache_validation_calls": 1} if bool(prepared_manifest.get("cache_loaded", False)) else {}),
                        },
                    )
                    if not bool(prepared_manifest.get("cache_loaded", False)):
                        harmonization_stats["substrate_harmonization_calls"] += int(prepared_manifest.get("harmonization_calls", 0) or 0)
                    prepared_validation_report_path = str(
                        Path(args.output_root)
                        / "cache"
                        / "prepared_response_substrate"
                        / f"source={source_value}"
                        / f"wave={wave_values[0] if wave_values else ''}"
                        / f"country_code={country_code}"
                        / "v550j_prepared_substrate_validation_report.json"
                    )
                    cache_was_loaded = bool(prepared_manifest.get("cache_loaded", False))
                    progress.stage(
                        3,
                        6,
                        "Association context",
                        f"family {active_family_index}/{active_family_total}: {family_id} country={country_code} prepared substrate rows={len(prepared_country_frame)} {'cache_loaded' if cache_was_loaded else 'harmonization_calls=' + str(prepared_manifest.get('harmonization_calls', 0))}",
                    )
                    if not active_family_lookup_df.empty:
                        all_family_rows = prepared_country_frame.merge(
                            active_family_lookup_df,
                            on="var_code_norm",
                            how="inner",
                            suffixes=("", "_family"),
                        )
                    else:
                        all_family_rows = pd.DataFrame(columns=list(prepared_country_frame.columns) + list(active_family_lookup_df.columns))
                    country_state = {
                        "prepared_country_frame": prepared_country_frame,
                        "prepared_manifest": prepared_manifest,
                        "all_family_rows": all_family_rows,
                    }
                    country_prepared_state[cache_key] = country_state
                else:
                    family_frames: list[pd.DataFrame] = []
                    hot_path_harmonization_count = 0
                    for qrow in country_questions.itertuples(index=False):
                        qser = pd.Series(qrow._asdict())
                        raw_rows = _question_rows_from_cache(qser, question_row_cache)
                        if raw_rows.empty:
                            continue
                        harmonized = _harmonize_question_frame(raw_rows, semantics_lookup, response_semantics_contract_hash=semantics_contract)
                        hot_path_harmonization_count += 1
                        if harmonized.empty:
                            continue
                        item_meta = next((item for item in _family_item_map(family_cfg) if item["var_code"].upper() == _safe_clean(qser.get("var_code")).upper()), None)
                        if item_meta is not None:
                            harmonized["family_id"] = family_id
                            harmonized["family_label"] = _safe_clean(family_cfg.get("family_label", family_id))
                            harmonized["family_type"] = _safe_clean(family_cfg.get("family_type", ""))
                            harmonized["item_role"] = item_meta.get("item_role", "target_case")
                            harmonized["condition_label"] = item_meta.get("condition_label", "")
                        harmonized["source"] = source_value
                        harmonized["wave"] = _safe_clean(qser.get("raw_wave")) or _safe_clean(qser.get("canonical_wave"))
                        harmonized["canonical_wave"] = _safe_clean(qser.get("canonical_wave")) or _safe_clean(qser.get("raw_wave"))
                        harmonized["country_code"] = country_code
                        family_frames.append(harmonized)
                    harmonization_stats["hot_path_harmonization_calls"] += hot_path_harmonization_count
                    if not family_frames:
                        continue
                    country_family_frame = pd.concat(family_frames, ignore_index=True, sort=False)
                    prepared_country_frame = country_family_frame.copy()
                    all_family_rows = country_family_frame.copy()
                    country_state = {
                        "prepared_country_frame": prepared_country_frame,
                        "all_family_rows": all_family_rows,
                    }
                    country_prepared_state[cache_key] = country_state
            else:
                prepared_country_frame = country_state["prepared_country_frame"]
                all_family_rows = country_state["all_family_rows"]

            if prepared_country_frame is None or prepared_country_frame.empty or all_family_rows is None:
                continue
            family_var_codes_norm = {code.upper() for code in family_var_codes}
            country_family_frame = all_family_rows[all_family_rows["family_id"].astype(str).eq(family_id)].copy() if not all_family_rows.empty else pd.DataFrame()
            if country_family_frame.empty:
                tables["joint_pattern_audit"].append(
                    pd.DataFrame(
                        [
                            {
                                "family_id": family_id,
                                "issue_type": "family_rows_missing_in_prepared_substrate",
                                "severity": "high",
                                "item_count": int(len(family_var_codes)),
                                "respondent_count": int(prepared_country_frame["respondent_id_norm"].nunique() if "respondent_id_norm" in prepared_country_frame.columns else prepared_country_frame["respondent_id"].nunique() if "respondent_id" in prepared_country_frame.columns else 0),
                                "detail": "Prepared substrate did not contain any family rows for this country slice.",
                                "action": "family skipped",
                                "created_at": utc_now(),
                                "schema_version": V550J_SCHEMA_VERSION,
                            }
                        ]
                    )
                )
                continue
            association_context_frame = prepared_country_frame[
                ~prepared_country_frame["var_code_norm"].astype(str).str.upper().isin(family_var_codes_norm)
            ].copy()
            if "is_substantive" in country_family_frame.columns:
                substantive_mask = country_family_frame["is_substantive"].fillna(False)
                if substantive_mask.any():
                    country_family_frame = country_family_frame[substantive_mask].copy()
                else:
                    tables["joint_pattern_audit"].append(
                        pd.DataFrame(
                            [
                                {
                                    "family_id": family_id,
                                    "issue_type": "response_semantics_missing",
                                    "severity": "medium",
                                    "item_count": int(len(family_var_codes)),
                                    "respondent_count": int(country_family_frame["respondent_id"].nunique() if "respondent_id" in country_family_frame.columns else 0),
                                    "detail": "No substantive rows were marked by the harmonized cache slice; compiling from observed rows.",
                                    "action": "fallback to observed response rows",
                                    "created_at": utc_now(),
                                    "schema_version": V550J_SCHEMA_VERSION,
                                }
                            ]
                        )
                    )
            if country_family_frame.empty:
                continue
            association_context_frame = None
            family_var_codes_norm = {code.upper() for code in family_var_codes}
            outside_family_context = prepared_country_frame[
                ~prepared_country_frame["var_code_norm"].astype(str).str.upper().isin(family_var_codes_norm)
            ].copy()
            progress.stage(
                6,
                8,
                f"{family_id}: association context",
                f"prepared outside-family rows={len(outside_family_context)}",
            )
            association_context_status = _association_authority_status(outside_family_context)
            if outside_family_context.empty:
                tables["joint_pattern_audit"].append(
                    pd.DataFrame(
                        [
                            {
                                "family_id": family_id,
                                "issue_type": "association_context_unavailable",
                                "association_context_status": "association_context_unavailable",
                                "severity": "low",
                                "item_count": int(len(family_var_codes)),
                                "respondent_count": int(prepared_country_frame["respondent_id_norm"].nunique() if "respondent_id_norm" in prepared_country_frame.columns else prepared_country_frame["respondent_id"].nunique() if "respondent_id" in prepared_country_frame.columns else 0),
                                "detail": "No outside-family context rows were available in the prepared substrate.",
                                "action": "association index suppressed for this country slice",
                                "created_at": utc_now(),
                                "schema_version": V550J_SCHEMA_VERSION,
                            }
                        ]
                    )
                )
                association_context_frame = None
            elif association_context_status == "has_association_authority":
                association_context_frame = outside_family_context
            else:
                tables["joint_pattern_audit"].append(
                    pd.DataFrame(
                        [
                            {
                                "family_id": family_id,
                                "issue_type": "association_context_authority_missing",
                                "association_context_status": "association_context_authority_missing",
                                "severity": "medium",
                                "item_count": int(len(family_var_codes)),
                                "respondent_count": int(prepared_country_frame["respondent_id_norm"].nunique() if "respondent_id_norm" in prepared_country_frame.columns else prepared_country_frame["respondent_id"].nunique() if "respondent_id" in prepared_country_frame.columns else 0),
                                "detail": "Prepared outside-family context was present but lacked association authority columns.",
                                "action": "association index suppressed for this country slice",
                                "created_at": utc_now(),
                                "schema_version": V550J_SCHEMA_VERSION,
                            }
                        ]
                    )
                )
                association_context_frame = None

            progress.stage(
                4,
                6,
                "Compile family tables",
                f"family {active_family_index}/{active_family_total}: {family_id} country={country_code} starting",
            )
            family_compile_started = monotonic()
            family_tables_for_frames = compile_v550j_family_tables(
                family_cfg,
                family_questions,
                country_family_frame,
                context_frame=association_context_frame,
                emit_diagnostics=diagnostics_enabled,
                association_mode=args.association_mode,
                association_support_threshold=association_support_threshold,
                publish_association_lanes=publish_association_lanes,
                association_lane_overrides=family_cfg.get("association_lane_overrides") or {},
                run_id=run_id,
                source_id=source_value,
                source=source_value,
                wave=wave_values[0] if wave_values else "",
                canonical_wave=wave_values[-1] if wave_values else "",
                country_code=country_code,
                progress=progress,
                registry=association_lane_registry,
            )
            if association_mode_enabled:
                family_tables_for_frames = _enforce_governed_association_lane_authority(
                    family_tables_for_frames,
                    registry=association_lane_registry,
                    source=source_value,
                    wave=wave_values[-1] if wave_values else canonical_wave,
                    country_code=country_code,
                )
            _record_stage(
                "compile_family_tables",
                family_compile_started,
                input_rows=len(country_family_frame),
                output_rows=sum(len(frame) for frame in family_tables_for_frames.values()),
                extra={
                    "family_id": family_id,
                    "country_code": country_code,
                    "pattern_rows": int(len(family_tables_for_frames.get("joint_response_pattern_index", pd.DataFrame()))),
                    "association_rows": int(len(family_tables_for_frames.get("joint_pattern_association_index", pd.DataFrame()))),
                    "membership_rows": int(len(family_tables_for_frames.get("joint_pattern_respondent_membership", pd.DataFrame()))),
                },
            )
            progress.stage(
                4,
                6,
                "Compile family tables",
                f"family {active_family_index}/{active_family_total}: {family_id} country={country_code} pattern_rows={len(family_tables_for_frames['joint_response_pattern_index'])} association_rows={len(family_tables_for_frames['joint_pattern_association_index'])}",
            )
            if diagnostics_enabled:
                progress.stage(
                    5,
                    6,
                    "Build funnel and append",
                    f"family {active_family_index}/{active_family_total}: {family_id} country={country_code} starting",
                )
                funnel_frame = _association_eligibility_funnel(
                    family_cfg=family_cfg,
                    respondent_df=country_family_frame,
                    context_frame=association_context_frame if association_context_frame is not None else None,
                    family_var_codes=set(family_var_codes),
                    association_index=family_tables_for_frames["joint_pattern_association_index"],
                    candidate_trace=family_tables_for_frames["joint_pattern_association_candidate_trace"],
                    run_id=run_id,
                    source_id=source_value,
                    source=source_value,
                    wave=wave_values[0] if wave_values else "",
                    canonical_wave=wave_values[0] if wave_values else "",
                    country_code=country_code,
                )
                family_tables_for_frames["joint_pattern_association_eligibility_funnel"] = funnel_frame
                progress.stage(
                    5,
                    6,
                    "Build funnel and append",
                    f"family {active_family_index}/{active_family_total}: {family_id} country={country_code} funnel_rows={len(funnel_frame)}",
                )
            else:
                family_tables_for_frames["joint_pattern_association_candidate_trace"] = pd.DataFrame(columns=V550J_ASSOCIATION_CANDIDATE_TRACE_COLUMNS)
                family_tables_for_frames["joint_pattern_association_eligibility_funnel"] = pd.DataFrame(columns=V550J_ASSOCIATION_FUNNEL_COLUMNS)
                family_tables_for_frames["joint_pattern_audit"] = pd.DataFrame(columns=[
                    "family_id",
                    "issue_type",
                    "association_context_status",
                    "severity",
                    "item_count",
                    "respondent_count",
                    "detail",
                    "action",
                    "created_at",
                    "schema_version",
                ])
                progress.stage(
                    5,
                    6,
                    "Build funnel and append",
                    f"family {active_family_index}/{active_family_total}: {family_id} country={country_code} skipped diagnostics",
                )
            _append_family_table_frames(run_tables, family_tables_for_frames)

            family_summaries.append(
                {
                    "family_id": family_id,
                    "family_label": _safe_clean(family_cfg.get("family_label", family_id)),
                    "family_type": _safe_clean(family_cfg.get("family_type", "")),
                    "question_rows": int(len(family_questions)),
                    "respondent_rows": int(len(country_family_frame)),
                    "pattern_rows": int(len(family_tables_for_frames["joint_response_pattern_index"])),
                    "boundary_rows": int(len(family_tables_for_frames["question_family_boundary_pattern_index"])),
                }
            )

    out_root = Path(args.output_root) / "runs" / run_id / shard_id / "joint_patterns"
    out_root.mkdir(parents=True, exist_ok=True)
    written_tables: dict[str, dict[str, Any]] = {}
    final_frames: dict[str, pd.DataFrame] = {}
    write_started = monotonic()
    progress.stage(6, 6, "Write outputs", f"tables={len(run_tables)}")
    total_tables = len(run_tables)
    for table_index, (table_name, frames) in enumerate(run_tables.items(), start=1):
        progress.stage(6, 6, "Write outputs", f"table {table_index}/{total_tables}: {table_name}")
        if frames:
            frame = pd.concat(frames, ignore_index=True, sort=False)
            if table_name in {"joint_response_pattern_index", "question_family_boundary_pattern_index"} and "support_score" in frame.columns:
                frame = frame.sort_values(["family_id", "country_code", "support_score", "pattern_count_unweighted"], ascending=[True, True, False, False], kind="mergesort").reset_index(drop=True)
            elif table_name in {"joint_pattern_relation_signature", "joint_pattern_item_index", "joint_pattern_association_index", "joint_pattern_position_signature", "joint_pattern_association_candidate_trace", "joint_pattern_association_review_surface", "joint_pattern_meaning_summary", "joint_pattern_respondent_membership"}:
                sort_cols = [col for col in ["family_id", "pattern_id", "var_code", "indicator_name", "associated_var_code"] if col in frame.columns]
                if sort_cols:
                    frame = frame.sort_values(sort_cols, kind="mergesort").reset_index(drop=True)
        else:
            if table_name == "joint_pattern_association_index":
                frame = pd.DataFrame(columns=V550J_ASSOCIATION_INDEX_COLUMNS)
            elif table_name == "joint_pattern_association_candidate_trace":
                frame = pd.DataFrame(columns=V550J_ASSOCIATION_CANDIDATE_TRACE_COLUMNS)
            elif table_name == "joint_pattern_association_review_surface":
                frame = pd.DataFrame(columns=V550J_ASSOCIATION_REVIEW_SURFACE_COLUMNS)
            elif table_name == "joint_pattern_meaning_summary":
                frame = pd.DataFrame(columns=V550J_MEANING_SUMMARY_COLUMNS)
            elif table_name == "joint_pattern_association_eligibility_funnel":
                frame = pd.DataFrame(columns=V550J_ASSOCIATION_FUNNEL_COLUMNS)
            else:
                frame = pd.DataFrame()
        final_frames[table_name] = frame
        written_tables[table_name] = _write_table(frame, out_dir=out_root, table_name=table_name, write_csv=args.write_csv, write_parquet=args.write_parquet)
    progress.stage(6, 6, "Write outputs", f"completed {total_tables} tables")
    _record_stage(
        "write_outputs",
        write_started,
        input_rows=sum(len(frame) for frame in final_frames.values()),
        output_rows=sum(item.get("rows", 0) for item in written_tables.values()),
        extra={"tables": int(total_tables)},
    )

    if diagnostics_enabled:
        validate_started = monotonic()
        progress.stage(6, 6, "Validate outputs", "starting")
        validation_report = _validate_v550j_run_outputs(
            run_id=run_id,
            shard_id=shard_id,
            family_summaries=family_summaries,
            written_tables=written_tables,
            table_frames=final_frames,
            output_dir=out_root,
            association_support_threshold=association_support_threshold,
        )
        semantic_overall = _semantic_extraction_metrics(
            final_frames.get("joint_response_pattern_item_index", pd.DataFrame()),
            final_frames.get("question_family_boundary_pattern_index", pd.DataFrame()),
            final_frames.get("joint_pattern_association_eligibility_funnel", pd.DataFrame()),
        )
        semantic_by_family: list[dict[str, Any]] = []
        family_ids = sorted({item.get("family_id") for item in family_summaries if item.get("family_id")})
        for family_id in family_ids:
            family_item_index = final_frames.get("joint_response_pattern_item_index", pd.DataFrame())
            family_boundary_index = final_frames.get("question_family_boundary_pattern_index", pd.DataFrame())
            family_funnel_index = final_frames.get("joint_pattern_association_eligibility_funnel", pd.DataFrame())
            if not family_item_index.empty and "family_id" in family_item_index.columns:
                family_item_index = family_item_index[family_item_index["family_id"].astype(str).eq(str(family_id))]
            if not family_boundary_index.empty and "family_id" in family_boundary_index.columns:
                family_boundary_index = family_boundary_index[family_boundary_index["family_id"].astype(str).eq(str(family_id))]
            if not family_funnel_index.empty and "family_id" in family_funnel_index.columns:
                family_funnel_index = family_funnel_index[family_funnel_index["family_id"].astype(str).eq(str(family_id))]
            family_metrics = _semantic_extraction_metrics(family_item_index, family_boundary_index, family_funnel_index)
            family_metrics["family_id"] = family_id
            semantic_by_family.append(family_metrics)
        validation_report["semantic_extraction_metrics_overall"] = semantic_overall
        validation_report["semantic_extraction_metrics_by_family"] = semantic_by_family
        atomic_write_json(out_root / "v550j_output_validation_report.json", validation_report)
        progress.stage(6, 6, "Validate outputs", f"validation_status={validation_report['validation_status']}")
        _record_stage(
            "validate_outputs",
            validate_started,
            input_rows=sum(len(frame) for frame in final_frames.values()),
            output_rows=1,
            extra={"validation_status": validation_report["validation_status"]},
        )
        if validation_report["validation_status"] != "pass":
            raise RuntimeError(f"V550J_OUTPUT_VALIDATION_FAILED: {validation_report['validation_message']}")
    else:
        validation_report = {
            "run_id": run_id,
            "shard_id": shard_id,
            "validation_status": "not_applicable",
            "validation_message": "diagnostics disabled",
        }
        semantic_overall = {}
        semantic_by_family = []

    producer_scope_identity = {
        "run_id": run_id,
        "source": source,
        "wave": canonical_wave,
        "canonical_wave": canonical_wave,
        "country_code": "",
        "country_codes": country_codes,
        "shard_id": shard_id,
        "scope_kind": "shard",
    }
    core_table_row_counts = {
        table_name: int(written_tables.get(table_name, {}).get("rows", 0))
        for table_name in V550J_V551J_GOVERNED_TABLES
    }
    run_integrity_status, evidence_status, downstream_permission_status, producer_state_detail = _derive_v550j_producer_boundary_state(
        governed_family_count=active_family_total,
        core_table_row_counts=core_table_row_counts,
        validation_status=validation_report["validation_status"],
    )
    for table_name in V550J_V551J_GOVERNED_TABLES:
        declaration = written_tables.get(table_name)
        if not isinstance(declaration, dict):
            raise RuntimeError(f"V550J_GOVERNED_TABLE_DECLARATION_MISSING:{table_name}")
        declared_hash = str(declaration.get("artifact_file_sha256") or "").strip().lower()
        if len(declared_hash) != 64 or any(ch not in "0123456789abcdef" for ch in declared_hash):
            raise RuntimeError(f"V550J_GOVERNED_TABLE_SHA256_MISSING_OR_INVALID:{table_name}")

    finalize_started = monotonic()
    progress.stage(6, 6, "Finalize manifest", "starting")
    provenance = capture_run_provenance(
        input_documents={
            "v550_shard_dir": args.v550_shard_dir,
            "registry_path": args.registry_path,
            "association_lane_registry_path": args.association_lane_registry_path or "",
            "response_option_map": args.response_option_map,
            "env_file": args.env_file,
            "db_url": args.db_url or "",
        }
    )
    manifest = {
        "contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
        "boundary_contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
        "producer_run_id": run_id,
        "run_id": run_id,
        "shard_id": shard_id,
        "source": source or "UNKNOWN",
        "wave": canonical_wave,
        "canonical_wave": canonical_wave,
        "country_code": "",
        "country_codes": country_codes,
        "producer_scope_identity": producer_scope_identity,
        "schema_version": V550J_PRODUCER_SCHEMA_VERSION,
        "compiler_version": V550J_PRODUCER_COMPILER_VERSION,
        "run_integrity_status": run_integrity_status,
        "evidence_status": evidence_status,
        "downstream_permission_status": downstream_permission_status,
        "producer_state_detail": producer_state_detail,
        "canonical_artifact_names": list(V550J_V551J_GOVERNED_TABLES),
        "created_at": utc_now(),
        "completed_at": utc_now(),
        "success": run_integrity_status == "PASS",
        "registry_path": str(Path(args.registry_path)),
        "association_lane_registry_path": str(association_lane_registry.path),
        "association_lane_registry_rule_count": len(association_lane_registry._all_rules),
        "response_option_map_path": str(Path(args.response_option_map)),
        "tables": written_tables,
        "families": family_summaries,
        "validation_report_path": str(out_root / "v550j_output_validation_report.json") if diagnostics_enabled else "",
        "validation_status": validation_report["validation_status"],
        **provenance,
    }
    atomic_write_json(out_root / "v550j_manifest.json", manifest)
    association_index_frame = final_frames.get("joint_pattern_association_index", pd.DataFrame())
    association_candidate_frame = final_frames.get("joint_pattern_association_candidate_trace", pd.DataFrame())
    association_review_frame = final_frames.get("joint_pattern_association_review_surface", pd.DataFrame())
    meaning_summary_frame = final_frames.get("joint_pattern_meaning_summary", pd.DataFrame())
    association_summary = {
        "association_candidate_rows": int(len(association_candidate_frame)),
        "association_publishable_rows": int(len(association_index_frame)) if not association_index_frame.empty else 0,
        "association_reviewable_rows": int(len(association_review_frame)),
        "association_blocked_rows": int(
            (
                association_candidate_frame["association_publication_status"].astype(str).str.startswith("blocked")
            ).sum()
        )
        if not association_candidate_frame.empty and "association_publication_status" in association_candidate_frame.columns
        else 0,
        "association_blank_identity_rows": int(
            (
                association_index_frame[
                    [
                        column
                        for column in ["run_id", "source_id", "source", "wave", "canonical_wave", "country_code", "family_id"]
                        if column in association_index_frame.columns
                    ]
                ]
                .fillna("")
                .astype(str)
                .eq("")
                .all(axis=1)
            ).sum()
        )
        if not association_index_frame.empty
        else 0,
        "association_n_overlap_min": int(association_index_frame["n_overlap_unweighted"].min()) if not association_index_frame.empty and "n_overlap_unweighted" in association_index_frame.columns else 0,
        "association_n_overlap_median": float(association_index_frame["n_overlap_unweighted"].median()) if not association_index_frame.empty and "n_overlap_unweighted" in association_index_frame.columns else 0.0,
        "association_n_overlap_max": int(association_index_frame["n_overlap_unweighted"].max()) if not association_index_frame.empty and "n_overlap_unweighted" in association_index_frame.columns else 0,
        "association_n_overlap_lt_3_count": int((association_index_frame["n_overlap_unweighted"] < 3).sum()) if not association_index_frame.empty and "n_overlap_unweighted" in association_index_frame.columns else 0,
        "association_n_overlap_lt_5_count": int((association_index_frame["n_overlap_unweighted"] < 5).sum()) if not association_index_frame.empty and "n_overlap_unweighted" in association_index_frame.columns else 0,
        "association_n_overlap_lt_10_count": int((association_index_frame["n_overlap_unweighted"] < 10).sum()) if not association_index_frame.empty and "n_overlap_unweighted" in association_index_frame.columns else 0,
        "association_n_overlap_lt_30_count": int((association_index_frame["n_overlap_unweighted"] < 30).sum()) if not association_index_frame.empty and "n_overlap_unweighted" in association_index_frame.columns else 0,
        "association_index_high_cardinality_rows": int((association_index_frame["is_high_cardinality_associated_var"].map(lambda v: _to_bool(v, False))).sum()) if not association_index_frame.empty and "is_high_cardinality_associated_var" in association_index_frame.columns else 0,
        "association_index_sparse_response_rows": int((association_index_frame["is_sparse_associated_response"].map(lambda v: _to_bool(v, False))).sum()) if not association_index_frame.empty and "is_sparse_associated_response" in association_index_frame.columns else 0,
        "association_index_raw_occupational_status_rows": int((association_index_frame["is_raw_occupational_status_code"].map(lambda v: _to_bool(v, False))).sum()) if not association_index_frame.empty and "is_raw_occupational_status_code" in association_index_frame.columns else 0,
        "association_index_same_family_rows": int((association_index_frame["is_same_family_association"].map(lambda v: _to_bool(v, False))).sum()) if not association_index_frame.empty and "is_same_family_association" in association_index_frame.columns else 0,
        "association_index_same_variable_rows": int((association_index_frame["is_same_variable_association"].map(lambda v: _to_bool(v, False))).sum()) if not association_index_frame.empty and "is_same_variable_association" in association_index_frame.columns else 0,
        "association_candidate_by_lane": dict(Counter(association_candidate_frame["association_lane"].astype(str))) if not association_candidate_frame.empty and "association_lane" in association_candidate_frame.columns else {},
        "association_publishable_by_lane": dict(Counter(association_index_frame["association_lane"].astype(str))) if not association_index_frame.empty and "association_lane" in association_index_frame.columns else {},
        "association_reviewable_by_lane": dict(Counter(association_review_frame["association_lane"].astype(str))) if not association_review_frame.empty and "association_lane" in association_review_frame.columns else {},
        "association_candidate_by_family": dict(Counter(association_candidate_frame["family_id"].astype(str))) if not association_candidate_frame.empty and "family_id" in association_candidate_frame.columns else {},
        "association_publishable_by_family": dict(Counter(association_index_frame["family_id"].astype(str))) if not association_index_frame.empty and "family_id" in association_index_frame.columns else {},
        "association_reviewable_by_family": dict(Counter(association_review_frame["family_id"].astype(str))) if not association_review_frame.empty and "family_id" in association_review_frame.columns else {},
        "association_lane_distinct_count": int(association_candidate_frame["association_lane"].astype(str).nunique()) if not association_candidate_frame.empty and "association_lane" in association_candidate_frame.columns else 0,
        "association_lane_collapse_detected": bool(
            not association_candidate_frame.empty
            and "association_lane" in association_candidate_frame.columns
            and association_candidate_frame["association_lane"].astype(str).nunique(dropna=True) == 1
            and association_candidate_frame["association_lane"].astype(str).eq("substantive_attitude_association").all()
        ),
        "association_known_var_misclassification_count": int(
            association_candidate_frame[
                association_candidate_frame["associated_var_code"].astype(str).str.upper().isin({"RACE", "OCC", "OCC10", "ISCO08", "PAEDUC", "MAEDUC", "SPEDUC", "REG16", "SIZE", "AGEWED"})
                & association_candidate_frame["association_lane"].astype(str).eq("substantive_attitude_association")
            ].shape[0]
        )
        if not association_candidate_frame.empty and {"associated_var_code", "association_lane"}.issubset(association_candidate_frame.columns)
        else 0,
        "meaning_summary_rows": int(len(meaning_summary_frame)),
        "meaning_summary_by_status": dict(Counter(meaning_summary_frame["meaning_summary_status"].astype(str))) if not meaning_summary_frame.empty and "meaning_summary_status" in meaning_summary_frame.columns else {},
        "meaning_summary_by_confidence": dict(Counter(meaning_summary_frame["meaning_summary_confidence"].astype(str))) if not meaning_summary_frame.empty and "meaning_summary_confidence" in meaning_summary_frame.columns else {},
        "meaning_summary_warning_flag_counts": dict(Counter(
            flag
            for flags in meaning_summary_frame["meaning_summary_warning_flags_json"].dropna().astype(str)
            for flag in (json.loads(flags) if flags not in {"[]", "", "null"} else [])
        )) if not meaning_summary_frame.empty and "meaning_summary_warning_flags_json" in meaning_summary_frame.columns else {},
    }
    atomic_write_json(
        out_root / "v550j_summary.json",
        {
            "families": family_summaries,
            "rows_by_table": {k: v["rows"] for k, v in written_tables.items()},
            "association_summary": association_summary,
            "command_provenance": provenance,
        },
    )
    if args.verbose:
        print(json.dumps(manifest, indent=2, ensure_ascii=False))
    progress.stage(6, 6, "Finalize manifest", f"success={manifest['success']} run_id={run_id}")
    _record_stage(
        "finalize_manifest",
        finalize_started,
        input_rows=len(family_summaries),
        output_rows=1,
        extra={"success": bool(manifest["success"])},
    )

    final_country_code = country_codes[0] if len(country_codes) == 1 else "MULTI"

    performance_profile = {
        "run_id": run_id,
        "shard_id": shard_id,
        "source": source,
        "wave": canonical_wave,
        "country_code": final_country_code,
        "country_codes": country_codes,
        "substrate_mode": args.v550j_substrate_mode,
        "stages": performance_stages,
        "harmonization_call_count_total": int(
            harmonization_stats.get("hot_path_harmonization_calls", 0)
            + harmonization_stats.get("forensic_harmonization_calls", 0)
            + harmonization_stats.get("substrate_harmonization_calls", 0)
        ),
        "harmonization_call_count_hot_path": int(harmonization_stats.get("hot_path_harmonization_calls", 0)),
        "harmonization_call_count_forensic": int(harmonization_stats.get("forensic_harmonization_calls", 0)),
        "substrate_harmonization_calls": int(harmonization_stats.get("substrate_harmonization_calls", 0)),
        "forensic_harmonized_rows": int(harmonization_stats.get("forensic_harmonized_rows", 0)),
        "prepared_substrate_validation_report_path": prepared_validation_report_path,
        **provenance,
    }
    atomic_write_json(out_root / "v550j_performance_profile.json", performance_profile)

    _candidate = association_candidate_frame
    _resolution_types = [
        "exact_registry",
        "prefix_registry",
        "manual_override_review_only",
        "legacy_family_adapter",
        "source_structure",
        "semantic_role",
        "fallback",
        "blocked",
        "cardinality_gate",
        "semantic_role_insufficient",
    ]

    resolution_counts = {}
    if not _candidate.empty and "association_lane_resolution_type" in _candidate.columns:
        resolution_counts = {rt: int((_candidate["association_lane_resolution_type"].astype(str) == rt).sum()) for rt in _resolution_types}

    publishable_rows_from = {}
    if not association_index_frame.empty and "association_lane_resolution_type" in association_index_frame.columns:
        for rt in _resolution_types:
            publishable_rows_from[f"publishable_rows_from_{rt}"] = int((association_index_frame["association_lane_resolution_type"].astype(str) == rt).sum())

    top_semantic_role_variables_list = []
    if not _candidate.empty and "association_lane_resolution_type" in _candidate.columns and "associated_var_code" in _candidate.columns:
        sr_mask = _candidate["association_lane_resolution_type"].astype(str).isin(["semantic_role"])
        if sr_mask.any():
            top_semantic_role_variables_list = sorted(
                _candidate[sr_mask]["associated_var_code"].astype(str).value_counts().head(10).to_dict().items()
            )
    top_semantic_role_publishable_variables_list = []
    if not association_index_frame.empty and "association_lane_resolution_type" in association_index_frame.columns and "associated_var_code" in association_index_frame.columns:
        srp_mask = association_index_frame["association_lane_resolution_type"].astype(str).isin(["semantic_role"])
        if srp_mask.any():
            top_semantic_role_publishable_variables_list = sorted(
                association_index_frame[srp_mask]["associated_var_code"].astype(str).value_counts().head(20).to_dict().items()
            )
    top_fallback_variables_list = []
    if not _candidate.empty and "association_lane_resolution_type" in _candidate.columns and "associated_var_code" in _candidate.columns:
        fb_mask = _candidate["association_lane_resolution_type"].astype(str).isin(["fallback", "semantic_role_insufficient"])
        if fb_mask.any():
            top_fallback_variables_list = sorted(
                _candidate[fb_mask]["associated_var_code"].astype(str).value_counts().head(10).to_dict().items()
            )

    publishability_counts = {}
    if not _candidate.empty and "association_gate_status" in _candidate.columns:
        publishability_counts = dict(Counter(_candidate["association_gate_status"].astype(str)))

    registry_coverage = {
        "run_id": run_id,
        "source": source,
        "wave": canonical_wave,
        "country_code": final_country_code,
        "country_codes": country_codes,
        "total_associated_variables": int(_candidate["associated_var_code"].astype(str).nunique()) if not _candidate.empty and "associated_var_code" in _candidate.columns else 0,
        "total_candidate_rows": int(len(_candidate)),
        "publishable_rows": int(len(association_index_frame)) if not association_index_frame.empty else 0,
        "unknown_candidate_row_count": int((_candidate["association_lane"].astype(str).eq("unknown_association_lane")).sum()) if not _candidate.empty and "association_lane" in _candidate.columns else 0,
        "unknown_candidate_row_share": float(round((_candidate["association_lane"].astype(str).eq("unknown_association_lane")).mean(), 4)) if not _candidate.empty and "association_lane" in _candidate.columns else 0.0,
        "unknown_in_index": int((association_index_frame["association_lane"].astype(str).eq("unknown_association_lane")).sum()) if not association_index_frame.empty and "association_lane" in association_index_frame.columns else 0,
        "lane_counts": dict(Counter(_candidate["association_lane"].astype(str))) if not _candidate.empty and "association_lane" in _candidate.columns else {},
        "resolution_counts": resolution_counts,
        "publishable_rows_from": publishable_rows_from,
        "publishability_counts": publishability_counts,
        "top_unknown_variables": sorted(_candidate[_candidate["association_lane"].astype(str).eq("unknown_association_lane")]["associated_var_code"].astype(str).value_counts().head(10).to_dict().items()) if not _candidate.empty and "association_lane" in _candidate.columns and "associated_var_code" in _candidate.columns else [],
        "top_semantic_role_variables": top_semantic_role_variables_list,
        "top_semantic_role_publishable_variables": top_semantic_role_publishable_variables_list,
        "top_fallback_variables": top_fallback_variables_list,
        "top_publishable_variables": sorted(association_index_frame["associated_var_code"].astype(str).value_counts().head(20).to_dict().items()) if not association_index_frame.empty and "associated_var_code" in association_index_frame.columns else [],
        "coverage_status": (
            "registry_coverage_pass"
            if len(_candidate) > 0
            else "not_tested_no_candidates"
        ),
    }
    if len(_candidate) == 0:
        pass
    elif registry_coverage["unknown_in_index"] > 0:
        registry_coverage["coverage_status"] = "registry_coverage_failed_unknown_publishable"
    elif registry_coverage["unknown_candidate_row_share"] > 0.05:
        registry_coverage["coverage_status"] = "registry_coverage_pass_with_warnings"
    if publishable_rows_from.get("publishable_rows_from_unknown", 0) > 0 or publishable_rows_from.get("publishable_rows_from_fallback", 0) > 0 or publishable_rows_from.get("publishable_rows_from_semantic_role", 0) > 0:
        registry_coverage["coverage_status"] = "registry_coverage_failed_unknown_or_fallback_publishable"
    atomic_write_json(out_root / "v550j_registry_coverage_report.json", registry_coverage)

    _unknown_row_count = registry_coverage["unknown_candidate_row_count"]
    _semantic_role_publishable = publishable_rows_from.get("publishable_rows_from_semantic_role", 0)
    _has_warnings = bool(
        registry_coverage.get("coverage_status", "").startswith("registry_coverage_pass_with_warnings")
        or registry_coverage.get("coverage_status", "") == "registry_coverage_failed_unknown_or_fallback_publishable"
        or _unknown_row_count > 0
        or _semantic_role_publishable > 0
    )
    _blocking_issues = []
    if registry_scope_status not in {"applicable", "not_applicable"}:
        _blocking_issues.append(f"question_family_registry_{registry_scope_status}")
    if args.association_mode != "off" and registry_coverage["coverage_status"] == "not_tested_no_candidates":
        _blocking_issues.append("registry_coverage_not_tested_no_candidates")
    if registry_coverage["unknown_in_index"] > 0:
        _blocking_issues.append("unknown_lane_rows_in_association_index")
    if registry_coverage.get("coverage_status", "") == "registry_coverage_failed_unknown_or_fallback_publishable":
        _blocking_issues.append("unknown_or_fallback_publishable_rows")
    if _semantic_role_publishable > 0:
        _blocking_issues.append("semantic_role_publishable_rows_present")
    if not meaning_summary_frame.empty and "publishable_attitude_signal_count" in meaning_summary_frame.columns:
        _publishable_empty = (meaning_summary_frame["publishable_attitude_signal_count"].astype(int) == 0).all()
    else:
        _publishable_empty = True
    _readiness = "diagnostic_only"
    if _publishable_empty and not _blocking_issues:
        _readiness = "diagnostic_only_no_publishable_rows"
    elif not _publishable_empty and not _blocking_issues:
        _readiness = "validated_for_internal_analysis"
    if _blocking_issues:
        _readiness = "failed_validation"
    _warnings = []
    if _unknown_row_count > 0:
        _warnings.append("unknown_candidate_rows_present")
    if _semantic_role_publishable > 0:
        _warnings.append("publishable_rows_from_semantic_role_present")
    if _has_warnings:
        _warnings.append("review_recommended")
    _manual_review = []
    if _unknown_row_count > 0:
        _top_unknown = registry_coverage.get("top_unknown_variables", [])
        _manual_review.append({"issue": "unknown_candidate_rows", "variables": [v for v, _ in _top_unknown]})
    if _semantic_role_publishable > 0:
        _top_semantic_pub = registry_coverage.get("top_semantic_role_publishable_variables", [])
        _manual_review.append({"issue": "review_semantic_role_publishable_variables", "count": _semantic_role_publishable, "variables": [v for v, _ in _top_semantic_pub]})
    readiness_report = {
        "contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
        "boundary_contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
        "producer_run_id": run_id,
        "run_id": run_id,
        "source": source,
        "wave": canonical_wave,
        "canonical_wave": canonical_wave,
        "country_code": "",
        "country_codes": country_codes,
        "shard_id": shard_id,
        "producer_scope_identity": producer_scope_identity,
        "schema_version": V550J_PRODUCER_SCHEMA_VERSION,
        "compiler_version": V550J_PRODUCER_COMPILER_VERSION,
        "run_integrity_status": run_integrity_status,
        "evidence_status": evidence_status,
        "downstream_permission_status": downstream_permission_status,
        "producer_state_detail": producer_state_detail,
        "readiness_status": _readiness,
        "family_registry_status": registry_scope_status,
        "family_registry_governance_status": registry_governance_status,
        "family_registry_source": registry_source,
        "response_semantics_status": "present" if args.v550j_substrate_mode else "missing",
        "association_lane_registry_path": str(association_lane_registry.path),
        "association_lane_registry_status": "present" if association_mode_enabled else "not_applicable_association_mode_off",
        "association_lane_registry_rule_count": len(association_lane_registry._all_rules),
        "threshold_profile_status": threshold_profile_id,
        "threshold_profile_path": str(args.association_threshold_profiles_path) if association_mode_enabled else "",
        "threshold_effective_n": effective_n,
        "association_support_threshold": association_support_threshold,
        "association_support_threshold_basis": (
            "explicit_cli_override"
            if association_support_threshold_override is not None
            else "selected_profile_publishable_attitude_min_overlap"
        ),
        "meaning_summary_status": "coherent" if not _blocking_issues else "incoherent",
        "blocking_issues": _blocking_issues,
        "warnings": _warnings,
        "manual_review_required": _manual_review,
        "next_required_actions": ["review_registry_coverage", "validate_with_additional_waves"] if _blocking_issues else ["extend_to_additional_waves"],
    }
    atomic_write_json(out_root / "v550j_source_wave_readiness_report.json", readiness_report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
