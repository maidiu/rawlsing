#!/usr/bin/env python3
"""Compile V551J candidate evidence packets."""

from __future__ import annotations

import argparse
from io import StringIO
import json
import re
import shutil
import sys
from pathlib import Path
from time import monotonic
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]


def _contract_csv_text(frame: pd.DataFrame) -> str:
    return frame.to_csv(index=False, float_format="%.13f")


if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_pipeline_boundary_contract import (
    PIPELINE_BOUNDARY_CONTRACT_VERSION,
    BoundaryContractError,
    boundary_state_from_payload,
    verify_exact_identity,
)
from data.ddm_build_copy.ddm_v550_manifest import utc_now
from data.ddm_build_copy.ddm_v551j_io import ensure_output_dirs, file_hash, read_table, write_frame_artifact, write_json_artifact
from data.ddm_build_copy.ddm_v551j_review import (
    build_v551j_review_readiness_report,
    build_v551j_review_surface,
    build_v551j_reviewable_evidence_sidecar,
)
from data.ddm_build_copy.ddm_v551j_certification import build_v551j_certified_packet_index, build_v551j_status_conflict_audit, certify_v551j_v2_2_3
from data.ddm_build_copy.ddm_v551j_packets import (
    build_v551j_candidate_trace,
    build_v551j_join_key_diagnostics,
    build_v551j_joint_outputs_v2,
    build_v551j_readiness_report,
)
from data.ddm_build_copy.ddm_run_provenance import capture_run_provenance
from data.ddm_build_copy.ddm_v551j_schema import (
    V551J_COMPILER_VERSION,
    V551J_FORBIDDEN_INFERENCE_AUDIT_SCHEMA,
    V551J_INPUT_PROVENANCE_AUDIT_SCHEMA,
    V551J_INPUT_PROVENANCE_MANIFEST_SCHEMA,
    V551J_JOIN_KEY_DIAGNOSTICS_SCHEMA,
    V551J_PACKET_CANDIDATE_TRACE_SCHEMA,
    V551J_PACKET_EXCLUSION_AUDIT_SCHEMA,
    V551J_PACKET_READINESS_REPORT_SCHEMA,
    V551J_CERTIFICATION_AUDIT_SCHEMA,
    V551J_CERTIFICATION_READINESS_REPORT_SCHEMA,
    V551J_CERTIFICATION_REJECTION_AUDIT_SCHEMA,
    V551J_CERTIFIED_PACKET_INDEX_SCHEMA,
    V551J_REVIEW_READINESS_REPORT_SCHEMA,
    V551J_REVIEWABLE_EVIDENCE_SIDECAR_SCHEMA,
    V551J_REVIEW_SURFACE_EXCLUSION_AUDIT_SCHEMA,
    V551J_REVIEW_SURFACE_SCHEMA,
    V551J_V552_CONTEXT_JOIN_AUDIT_SCHEMA,
)
from data.ddm_build_copy.ddm_v551j_validation import validate_candidate_trace_schema, validate_review_surface_schema, validate_reviewable_evidence_sidecar_schema, validate_certification_audit_schema, validate_certification_readiness_report_schema, validate_certification_rejection_audit_schema, validate_certified_packet_index_schema, validate_v551j_v2_2_3_outputs, validate_written_v551j_artifacts
from data.ddm_build_copy.ddm_v551j_contract import recompute_joint_measurement_contract_hash, recompute_v551j_component_contract_hash, recompute_v551j_v2_2_3_packet_contract_hash
from data.ddm_build_copy.ddm_v550_schema import write_schema_json


V551_V3_SCHEMA_VERSION = "v3.0"
V551_V3_COMPILER_VERSION = "v3.0"
V551_V3_CANONICAL_ARTIFACTS = (
    "directional_candidate_adjudication",
    "relation_evidence_atoms",
    "directional_distribution_coverage",
)
V551_V3_REQUIRED_COLUMNS = {
    "directional_candidate_adjudication": {
        "run_id",
        "candidate_id",
        "empirical_distribution_id",
        "source",
        "source_family",
        "canonical_wave",
        "country_code",
        "question_id",
        "var_code",
        "response_value_normalized",
        "directional_applicability_status",
        "adjudication_outcome",
        "adjudication_reason",
        "promotable",
        "schema_version",
        "compiler_version",
    },
    "relation_evidence_atoms": {
        "run_id",
        "atom_id",
        "candidate_id",
        "empirical_distribution_id",
        "source",
        "source_family",
        "canonical_wave",
        "country_code",
        "question_id",
        "var_code",
        "response_value_normalized",
        "response_intensity",
        "v551_signed_side",
        "v551_signed_intensity",
        "support_status",
        "atom_contract_hash",
        "schema_version",
        "compiler_version",
    },
    "directional_distribution_coverage": {
        "run_id",
        "empirical_distribution_id",
        "source",
        "source_family",
        "canonical_wave",
        "country_code",
        "question_id",
        "var_code",
        "applicable_candidate_count",
        "promotable_candidate_count",
        "nonpromotable_candidate_count",
        "directional_adjudication_status",
        "candidate_count_conserved",
        "unweighted_mass_conserved",
        "weighted_mass_conserved",
        "schema_version",
        "compiler_version",
    },
}
V550J_PRODUCER_SCHEMA_VERSION = "v1"
V550J_PRODUCER_COMPILER_VERSION = "v550j_joint_response_patterns_producer_v1"
V550J_TABLE_INPUTS = {
    "joint_response_pattern_index": "v550j_pattern_index_path",
    "joint_response_pattern_item_index": "v550j_pattern_item_index_path",
    "joint_pattern_relation_signature": "v550j_relation_signature_path",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compile V551J candidate evidence packets.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--v551-atoms-path", required=True)
    parser.add_argument(
        "--v551-manifest-path",
        default=None,
        help="V551 v3 producer manifest. Defaults to manifest.json beside --v551-atoms-path.",
    )
    parser.add_argument("--v550j-pattern-index-path", required=True)
    parser.add_argument("--v550j-pattern-item-index-path", required=True)
    parser.add_argument("--v550j-relation-signature-path", required=True)
    parser.add_argument("--v550j-manifest-path", required=True)
    parser.add_argument("--v550j-readiness-report-path", required=True)
    parser.add_argument("--registry-path", required=True)
    parser.add_argument("--v550j-meaning-summary-path", default=None)
    parser.add_argument("--output-root", default=str(ROOT / "data" / "ddm_repository_copy" / "v551j" / "runs"))
    parser.add_argument("--v550j-position-signature-path", default=None)
    parser.add_argument("--v550j-association-index-path", default=None)
    parser.add_argument("--v550j-review-surface-path", default=None)
    parser.add_argument("--v552-question-semantic-hierarchy-path", default=None, help="Deprecated in V551J v2; recorded only as noncertifying legacy context.")
    parser.add_argument("--v552-structural-channel-index-path", default=None, help="Deprecated in V551J v2; recorded only as noncertifying legacy context.")
    parser.add_argument("--v552-relation-axis-pressure-path", default=None, help="Deprecated in V551J v2; recorded only as noncertifying legacy context.")
    parser.add_argument("--v552-target-entity-pressure-path", default=None, help="Deprecated in V551J v2; recorded only as noncertifying legacy context.")
    parser.add_argument("--v552-driver-facet-pressure-path", default=None, help="Deprecated in V551J v2; recorded only as noncertifying legacy context.")
    parser.add_argument("--v552-contradiction-surface-path", default=None, help="Deprecated in V551J v2; recorded only as noncertifying legacy context.")
    parser.add_argument("--v552-horizon-constraint-index-path", default=None, help="Deprecated in V551J v2; recorded only as noncertifying legacy context.")
    parser.add_argument("--v552-parent-prior-manifest-path", default=None, help="Deprecated in V551J v2; recorded only as noncertifying legacy context.")
    parser.add_argument("--emit-review-surface", action="store_true", default=False)
    parser.add_argument("--emit-certified-index", action="store_true", default=False)
    parser.add_argument("--write-csv", action="store_true", default=False)
    parser.add_argument("--no-write-csv", dest="write_csv", action="store_false")
    parser.add_argument("--write-parquet", action="store_true", default=True)
    parser.add_argument("--no-write-parquet", dest="write_parquet", action="store_false")
    parser.add_argument("--strict", action="store_true", default=True)
    parser.add_argument("--no-strict", dest="strict", action="store_false")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def _load(path: str | None) -> pd.DataFrame:
    return read_table(path) if path else pd.DataFrame()


def _row_count(frame: pd.DataFrame) -> int:
    return int(len(frame)) if frame is not None else 0


def _log_stage(enabled: bool, label: str, detail: str = "") -> None:
    if not enabled:
        return
    message = f"[V551J] {label}"
    if detail:
        message = f"{message}: {detail}"
    print(message, flush=True)


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


def _truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def _scope_values(frames: tuple[pd.DataFrame, ...], columns: tuple[str, ...]) -> list[str]:
    for column in columns:
        values: list[str] = []
        for frame in frames:
            if frame.empty or column not in frame.columns:
                continue
            values.extend(_clean(value) for value in frame[column].tolist() if _clean(value))
        unique = sorted(set(values))
        if unique:
            return unique
    return []


def _single_scope_value(frames: tuple[pd.DataFrame, ...], columns: tuple[str, ...], label: str) -> str:
    unique = _scope_values(frames, columns)
    if not unique:
        raise RuntimeError(f"V551J_V550J_SCOPE_MISSING:{label}")
    if len(unique) != 1:
        raise RuntimeError(f"V551J_V550J_SCOPE_NOT_SINGULAR:{label}:{unique[:8]}")
    return unique[0]


def _read_json_object(path: str | Path, label: str) -> dict[str, Any]:
    path_obj = Path(path)
    try:
        payload = json.loads(path_obj.read_text(encoding="utf-8"))
    except Exception as exc:
        raise BoundaryContractError(f"{label}_UNREADABLE:{path_obj}:{type(exc).__name__}:{exc}") from exc
    if not isinstance(payload, dict):
        raise BoundaryContractError(f"{label}_NOT_OBJECT:{path_obj}")
    return payload


def _scope_from_producer_payload(payload: dict[str, Any], label: str) -> dict[str, Any]:
    scope = payload.get("producer_scope_identity")
    if not isinstance(scope, dict):
        raise BoundaryContractError(f"{label}_PRODUCER_SCOPE_IDENTITY_MISSING")
    countries_raw = scope.get("country_codes") or payload.get("country_codes") or []
    if not isinstance(countries_raw, list):
        raise BoundaryContractError(f"{label}_COUNTRY_CODES_MALFORMED")
    return {
        "run_id": _clean(scope.get("run_id") or payload.get("producer_run_id") or payload.get("run_id")),
        "source": _clean(scope.get("source") or payload.get("source")),
        "wave": _clean(scope.get("canonical_wave") or scope.get("wave") or payload.get("canonical_wave") or payload.get("wave")),
        "canonical_wave": _clean(scope.get("canonical_wave") or scope.get("wave") or payload.get("canonical_wave") or payload.get("wave")),
        "country_code": _clean(scope.get("country_code") or payload.get("country_code")),
        "country_codes": sorted({_clean(value) for value in countries_raw if _clean(value)}),
        "shard_id": _clean(scope.get("shard_id") or payload.get("shard_id")),
        "scope_kind": _clean(scope.get("scope_kind")) or ("shard" if _clean(scope.get("shard_id") or payload.get("shard_id")) else "country"),
    }


def _expected_v551_scope(
    run_id: str,
    pattern_index: pd.DataFrame,
    pattern_item_index: pd.DataFrame,
    v550j_manifest_path: str | Path | None = None,
) -> dict[str, Any]:
    frames = (pattern_index, pattern_item_index)
    manifest_scope: dict[str, Any] = {}
    if v550j_manifest_path:
        manifest = _read_json_object(v550j_manifest_path, "V550J_MANIFEST")
        raw_scope = manifest.get("producer_scope_identity")
        if isinstance(raw_scope, dict):
            manifest_scope = _scope_from_producer_payload(manifest, "V550J_MANIFEST")
        else:
            manifest_scope = {
                "run_id": _clean(manifest.get("run_id")),
                "source": _clean(manifest.get("source")),
                "wave": _clean(manifest.get("canonical_wave") or manifest.get("wave")),
                "canonical_wave": _clean(manifest.get("canonical_wave") or manifest.get("wave")),
                "country_code": _clean(manifest.get("country_code")),
                "country_codes": sorted({_clean(value) for value in (manifest.get("country_codes") or []) if _clean(value)}) if isinstance(manifest.get("country_codes") or [], list) else [],
                "shard_id": _clean(manifest.get("shard_id")),
                "scope_kind": "shard" if _clean(manifest.get("shard_id")) else "country",
            }
        if manifest_scope["run_id"] and manifest_scope["run_id"] != run_id:
            raise BoundaryContractError(
                f"V550J_MANIFEST_RUN_ID_MISMATCH:expected={run_id}:actual={manifest_scope['run_id']}"
            )

    for frame in frames:
        if frame.empty or "run_id" not in frame.columns:
            continue
        observed = sorted({_clean(value) for value in frame["run_id"].tolist() if _clean(value)})
        if observed and observed != [run_id]:
            raise RuntimeError(f"V551J_V550J_RUN_IDENTITY_MISMATCH:expected={run_id}:observed={observed}")

    source_values = _scope_values(frames, ("source_family", "source", "source_id"))
    wave_values = _scope_values(frames, ("canonical_wave", "wave"))
    country_values = _scope_values(frames, ("country_code",))
    if len(source_values) > 1:
        raise RuntimeError(f"V551J_V550J_SCOPE_NOT_SINGULAR:source:{source_values[:8]}")
    if len(wave_values) > 1:
        raise RuntimeError(f"V551J_V550J_SCOPE_NOT_SINGULAR:wave:{wave_values[:8]}")

    source = source_values[0] if source_values else _clean(manifest_scope.get("source"))
    wave = wave_values[0] if wave_values else _clean(manifest_scope.get("wave"))
    country_codes = country_values or list(manifest_scope.get("country_codes") or [])
    if not country_codes and _clean(manifest_scope.get("country_code")):
        country_codes = [_clean(manifest_scope.get("country_code"))]
    shard_id = _clean(manifest_scope.get("shard_id"))
    if not source:
        raise RuntimeError("V551J_V550J_SCOPE_MISSING:source")
    if not wave:
        raise RuntimeError("V551J_V550J_SCOPE_MISSING:wave")
    if source_values and manifest_scope.get("source") and source != manifest_scope["source"]:
        raise BoundaryContractError("V550J_FRAME_MANIFEST_SOURCE_MISMATCH")
    if wave_values and manifest_scope.get("wave") and wave != manifest_scope["wave"]:
        raise BoundaryContractError("V550J_FRAME_MANIFEST_WAVE_MISMATCH")
    manifest_countries = sorted(manifest_scope.get("country_codes") or [])
    if country_values and manifest_countries and sorted(country_values) != manifest_countries:
        raise BoundaryContractError(
            f"V550J_FRAME_MANIFEST_COUNTRY_SCOPE_MISMATCH:frames={sorted(country_values)}:manifest={manifest_countries}"
        )
    country_codes = sorted(country_codes)
    manifest_country_code = _clean(manifest_scope.get("country_code"))
    if manifest_country_code:
        if len(country_codes) != 1:
            raise BoundaryContractError(
                f"V550J_MANIFEST_MULTI_COUNTRY_SCALAR_COUNTRY_FORBIDDEN:country_code={manifest_country_code}:countries={country_codes}"
            )
        if manifest_country_code != country_codes[0]:
            raise BoundaryContractError(
                f"V550J_MANIFEST_COUNTRY_CODE_SCOPE_MISMATCH:country_code={manifest_country_code}:countries={country_codes}"
            )
    if len(country_codes) > 1 and not shard_id:
        raise BoundaryContractError(
            f"V551J_MULTI_COUNTRY_SCOPE_REQUIRES_V550J_SHARD_ID:countries={country_codes}"
        )
    return {
        "run_id": run_id,
        "source": source,
        "wave": wave,
        "canonical_wave": wave,
        "country_code": country_codes[0] if len(country_codes) == 1 else "",
        "country_codes": country_codes,
        "shard_id": shard_id,
        "scope_kind": "shard" if shard_id else "country",
    }


def _resolve_v551_manifest_path(v551_atoms_path: str, explicit_manifest_path: str | None) -> Path:
    if explicit_manifest_path:
        return Path(explicit_manifest_path)
    return Path(v551_atoms_path).resolve().parent / "manifest.json"


def _manifest_artifact_map(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    raw = manifest.get("artifacts") or []
    if not isinstance(raw, list):
        raise BoundaryContractError("V551_ARTIFACT_DECLARATIONS_MALFORMED")
    result: dict[str, dict[str, Any]] = {}
    for row in raw:
        if not isinstance(row, dict):
            continue
        name = _clean(row.get("artifact") or row.get("name"))
        if not name:
            continue
        if name in result:
            raise BoundaryContractError(f"V551_ARTIFACT_DECLARATION_DUPLICATE:{name}")
        result[name] = dict(row)
    return result


def _resolve_declared_artifact(manifest_path: Path, declaration: dict[str, Any], artifact_name: str) -> Path:
    relative = _clean(declaration.get("path") or declaration.get("relative_path"))
    if not relative:
        raise BoundaryContractError(f"V551_ARTIFACT_PATH_MISSING:{artifact_name}")
    relative_path = Path(relative)
    if relative_path.is_absolute():
        raise BoundaryContractError(f"V551_ARTIFACT_PATH_MUST_BE_RELATIVE:{artifact_name}:{relative}")
    base = manifest_path.resolve().parent
    resolved = (base / relative_path).resolve()
    try:
        resolved.relative_to(base)
    except ValueError as exc:
        raise BoundaryContractError(f"V551_ARTIFACT_PATH_ESCAPES_PRODUCER_ROOT:{artifact_name}:{relative}") from exc
    if resolved.suffix.lower() != ".parquet":
        raise BoundaryContractError(f"V551_CANONICAL_ARTIFACT_NOT_PARQUET:{artifact_name}:{resolved}")
    return resolved


def _require_frame_columns(frame: pd.DataFrame, artifact_name: str) -> None:
    required = V551_V3_REQUIRED_COLUMNS[artifact_name]
    missing = sorted(required - set(frame.columns))
    if missing:
        raise BoundaryContractError(f"V551_ARTIFACT_SCHEMA_MISSING_COLUMNS:{artifact_name}:{','.join(missing)}")


def _verify_frame_scope(frame: pd.DataFrame, artifact_name: str, expected_scope: dict[str, Any]) -> None:
    _require_frame_columns(frame, artifact_name)
    if frame.empty:
        return
    checks = {
        "run_id": ("run_id",),
        "source": ("source_family", "source"),
        "wave": ("canonical_wave", "wave"),
    }
    for label, columns in checks.items():
        expected = expected_scope[label]
        matched_column = next((column for column in columns if column in frame.columns), None)
        if matched_column is None:
            raise BoundaryContractError(f"V551_ARTIFACT_IDENTITY_COLUMN_MISSING:{artifact_name}:{label}")
        observed = sorted({_clean(value) for value in frame[matched_column].tolist() if _clean(value)})
        if observed != [expected]:
            raise BoundaryContractError(
                f"V551_ARTIFACT_IDENTITY_MISMATCH:{artifact_name}:{label}:expected={expected}:observed={observed}"
            )
    observed_countries = sorted({_clean(value) for value in frame["country_code"].tolist() if _clean(value)})
    if observed_countries != list(expected_scope["country_codes"]):
        raise BoundaryContractError(
            f"V551_ARTIFACT_IDENTITY_MISMATCH:{artifact_name}:country_codes:"
            f"expected={expected_scope['country_codes']}:observed={observed_countries}"
        )
    schema_values = sorted({_clean(value) for value in frame["schema_version"].tolist() if _clean(value)})
    compiler_values = sorted({_clean(value) for value in frame["compiler_version"].tolist() if _clean(value)})
    if schema_values != [V551_V3_SCHEMA_VERSION]:
        raise BoundaryContractError(f"V551_ARTIFACT_SCHEMA_VERSION_MISMATCH:{artifact_name}:{schema_values}")
    if compiler_values != [V551_V3_COMPILER_VERSION]:
        raise BoundaryContractError(f"V551_ARTIFACT_COMPILER_VERSION_MISMATCH:{artifact_name}:{compiler_values}")


def _validate_v551_candidate_conservation(
    adjudication: pd.DataFrame,
    atoms: pd.DataFrame,
    coverage: pd.DataFrame,
) -> dict[str, Any]:
    outcomes = adjudication["adjudication_outcome"].fillna("").astype(str) if not adjudication.empty else pd.Series(dtype=str)
    valid_outcomes = {"PROMOTABLE", "NONPROMOTABLE_REPAIRABLE", "NOT_APPLICABLE"}
    invalid_outcomes = sorted(set(outcomes) - valid_outcomes)
    if invalid_outcomes:
        raise BoundaryContractError(f"V551_ADJUDICATION_OUTCOME_INVALID:{invalid_outcomes}")
    if not adjudication.empty and adjudication["candidate_id"].astype(str).duplicated().any():
        raise BoundaryContractError("V551_ADJUDICATION_DUPLICATE_CANDIDATE_ID")
    if not atoms.empty and atoms["candidate_id"].astype(str).duplicated().any():
        raise BoundaryContractError("V551_ATOMS_DUPLICATE_CANDIDATE_ID")

    promotable = adjudication.loc[outcomes.eq("PROMOTABLE")].copy() if not adjudication.empty else adjudication.copy()
    repair_debt = adjudication.loc[outcomes.eq("NONPROMOTABLE_REPAIRABLE")].copy() if not adjudication.empty else adjudication.copy()
    not_applicable = adjudication.loc[outcomes.eq("NOT_APPLICABLE")].copy() if not adjudication.empty else adjudication.copy()
    promotable_ids = set(promotable["candidate_id"].fillna("").astype(str)) if not promotable.empty else set()
    atom_candidate_ids = set(atoms["candidate_id"].fillna("").astype(str)) if not atoms.empty else set()
    missing_promotable = sorted(promotable_ids - atom_candidate_ids)
    unexpected_atoms = sorted(atom_candidate_ids - promotable_ids)
    if missing_promotable:
        raise BoundaryContractError(
            "V551_UNEXPLAINED_MISSING_PROMOTABLE_ATOM:" + ",".join(missing_promotable[:20])
        )
    if unexpected_atoms:
        raise BoundaryContractError(
            "V551_UNEXPECTED_ATOM_WITHOUT_PROMOTABLE_ADJUDICATION:" + ",".join(unexpected_atoms[:20])
        )

    if adjudication.empty:
        if not atoms.empty or not coverage.empty:
            raise BoundaryContractError("V551_EMPTY_ADJUDICATION_WITH_NONEMPTY_ATOMS_OR_COVERAGE")
    else:
        adjudication_distributions = set(adjudication["empirical_distribution_id"].fillna("").astype(str))
        coverage_distributions = set(coverage["empirical_distribution_id"].fillna("").astype(str)) if not coverage.empty else set()
        if adjudication_distributions != coverage_distributions:
            raise BoundaryContractError(
                "V551_COVERAGE_DISTRIBUTION_SET_MISMATCH:"
                f"adjudication={sorted(adjudication_distributions)}:coverage={sorted(coverage_distributions)}"
            )
        for distribution_id, rows in adjudication.groupby("empirical_distribution_id", dropna=False, sort=False):
            coverage_row = coverage[coverage["empirical_distribution_id"].astype(str).eq(str(distribution_id))]
            if len(coverage_row) != 1:
                raise BoundaryContractError(f"V551_COVERAGE_CARDINALITY_INVALID:{distribution_id}:{len(coverage_row)}")
            coverage_record = coverage_row.iloc[0]
            expected_promotable = int(rows["adjudication_outcome"].astype(str).eq("PROMOTABLE").sum())
            expected_nonpromotable = int(len(rows) - expected_promotable)
            if int(coverage_record.get("applicable_candidate_count") or 0) != len(rows):
                raise BoundaryContractError(f"V551_COVERAGE_APPLICABLE_COUNT_MISMATCH:{distribution_id}")
            if int(coverage_record.get("promotable_candidate_count") or 0) != expected_promotable:
                raise BoundaryContractError(f"V551_COVERAGE_PROMOTABLE_COUNT_MISMATCH:{distribution_id}")
            if int(coverage_record.get("nonpromotable_candidate_count") or 0) != expected_nonpromotable:
                raise BoundaryContractError(f"V551_COVERAGE_NONPROMOTABLE_COUNT_MISMATCH:{distribution_id}")
            for conservation_field in ("candidate_count_conserved", "unweighted_mass_conserved", "weighted_mass_conserved"):
                if not _truthy(coverage_record.get(conservation_field)):
                    raise BoundaryContractError(f"V551_COVERAGE_CONSERVATION_FAILURE:{distribution_id}:{conservation_field}")

    coverage_statuses = (
        sorted(set(coverage["directional_adjudication_status"].fillna("").astype(str)))
        if not coverage.empty
        else []
    )
    if adjudication.empty or (promotable.empty and repair_debt.empty and not not_applicable.empty):
        effective_evidence_status = "NOT_APPLICABLE"
        effective_permission_status = "NOT_APPLICABLE"
        effective_detail = "NO_APPLICABLE_DIRECTIONAL_EVIDENCE"
    elif not repair_debt.empty or any(status != "COMPLETE" for status in coverage_statuses):
        effective_evidence_status = "APPLICABLE_UNRESOLVED"
        effective_permission_status = "DENY"
        effective_detail = "KNOWN_V551_REPAIR_DEBT_OR_INCOMPLETE_COVERAGE"
    elif not promotable.empty:
        effective_evidence_status = "PRESENT"
        effective_permission_status = "ALLOW"
        effective_detail = "COMPLETE_PROMOTABLE_V551_V3_EVIDENCE"
    else:
        effective_evidence_status = "APPLICABLE_UNRESOLVED"
        effective_permission_status = "DENY"
        effective_detail = "UNRESOLVED_V551_ADJUDICATION_STATE"

    reason_counts: dict[str, int] = {}
    if not repair_debt.empty:
        for value in repair_debt["adjudication_reason"].fillna("").astype(str):
            reasons = [part.strip() for part in value.split("|") if part.strip()]
            if not reasons:
                reasons = ["UNSPECIFIED_REPAIR_DEBT"]
            for reason in reasons:
                reason_counts[reason] = reason_counts.get(reason, 0) + 1

    return {
        "candidate_count": int(len(adjudication)),
        "promotable_candidate_count": int(len(promotable)),
        "repair_debt_candidate_count": int(len(repair_debt)),
        "not_applicable_candidate_count": int(len(not_applicable)),
        "atom_count": int(len(atoms)),
        "coverage_row_count": int(len(coverage)),
        "coverage_statuses": coverage_statuses,
        "repair_debt_reason_counts": dict(sorted(reason_counts.items())),
        "effective_evidence_status": effective_evidence_status,
        "effective_downstream_permission_status": effective_permission_status,
        "effective_state_detail": effective_detail,
        "missing_promotable_atom_count": 0,
        "unexpected_atom_count": 0,
    }


def _verify_v551_v3_bundle(
    *,
    run_id: str,
    manifest_path: str | Path,
    atoms_path: str | Path,
    expected_scope: dict[str, Any],
) -> dict[str, Any]:
    manifest_path_obj = Path(manifest_path)
    if not manifest_path_obj.exists():
        raise BoundaryContractError(f"V551_MANIFEST_MISSING:{manifest_path_obj}")
    manifest = _read_json_object(manifest_path_obj, "V551_MANIFEST")
    if _clean(manifest.get("contract_version")) != PIPELINE_BOUNDARY_CONTRACT_VERSION:
        raise BoundaryContractError(
            f"V551_CONTRACT_VERSION_MISMATCH:expected={PIPELINE_BOUNDARY_CONTRACT_VERSION}:actual={_clean(manifest.get('contract_version')) or '<missing>'}"
        )
    if _clean(manifest.get("schema_version")) != V551_V3_SCHEMA_VERSION:
        raise BoundaryContractError(
            f"V551_SCHEMA_VERSION_MISMATCH:expected={V551_V3_SCHEMA_VERSION}:actual={_clean(manifest.get('schema_version')) or '<missing>'}"
        )
    if _clean(manifest.get("compiler_version")) != V551_V3_COMPILER_VERSION:
        raise BoundaryContractError(
            f"V551_COMPILER_VERSION_MISMATCH:expected={V551_V3_COMPILER_VERSION}:actual={_clean(manifest.get('compiler_version')) or '<missing>'}"
        )
    producer_state = boundary_state_from_payload(manifest)
    if producer_state.run_integrity_status != "PASS":
        raise BoundaryContractError(f"V551_RUN_INTEGRITY_NOT_PASS:{producer_state.run_integrity_status}")
    verify_exact_identity(
        manifest,
        run_id=run_id,
        source=expected_scope["source"],
        wave=expected_scope["wave"],
        country_code=expected_scope["country_code"],
        shard_id=expected_scope["shard_id"],
    )

    declarations = _manifest_artifact_map(manifest)
    declared_canonical = set(manifest.get("canonical_artifact_names") or [])
    missing_canonical = sorted(set(V551_V3_CANONICAL_ARTIFACTS) - declared_canonical)
    if missing_canonical:
        raise BoundaryContractError("V551_CANONICAL_ARTIFACT_SET_INCOMPLETE:" + ",".join(missing_canonical))

    frames: dict[str, pd.DataFrame] = {}
    paths: dict[str, Path] = {}
    for artifact_name in V551_V3_CANONICAL_ARTIFACTS:
        declaration = declarations.get(artifact_name)
        if declaration is None:
            raise BoundaryContractError(f"V551_ARTIFACT_DECLARATION_MISSING:{artifact_name}")
        declared_hash = _clean(declaration.get("artifact_file_sha256")).lower()
        if not re.fullmatch(r"[0-9a-f]{64}", declared_hash):
            raise BoundaryContractError(f"V551_ARTIFACT_FILE_SHA256_MISSING_OR_INVALID:{artifact_name}")
        if _clean(declaration.get("artifact_kind")) != "canonical":
            raise BoundaryContractError(f"V551_ARTIFACT_KIND_NOT_CANONICAL:{artifact_name}")
        if _clean(declaration.get("schema_version")) != V551_V3_SCHEMA_VERSION:
            raise BoundaryContractError(f"V551_ARTIFACT_DECLARED_SCHEMA_MISMATCH:{artifact_name}")
        artifact_path = _resolve_declared_artifact(manifest_path_obj, declaration, artifact_name)
        if not artifact_path.exists():
            raise BoundaryContractError(f"V551_ARTIFACT_MISSING:{artifact_name}:{artifact_path}")
        actual_hash = file_hash(artifact_path)
        if actual_hash != declared_hash:
            raise BoundaryContractError(
                f"V551_ARTIFACT_FILE_SHA256_MISMATCH:{artifact_name}:expected={declared_hash}:actual={actual_hash}"
            )
        frame = read_table(artifact_path)
        _verify_frame_scope(frame, artifact_name, expected_scope)
        declared_rows = declaration.get("row_count")
        if declared_rows is None or int(declared_rows) != len(frame):
            raise BoundaryContractError(
                f"V551_ARTIFACT_ROW_COUNT_MISMATCH:{artifact_name}:declared={declared_rows}:actual={len(frame)}"
            )
        frames[artifact_name] = frame
        paths[artifact_name] = artifact_path

    declared_atoms_path = paths["relation_evidence_atoms"].resolve()
    supplied_atoms_path = Path(atoms_path).resolve()
    if supplied_atoms_path != declared_atoms_path:
        raise BoundaryContractError(
            f"V551_ATOMS_PATH_NOT_PRODUCER_DECLARED:declared={declared_atoms_path}:supplied={supplied_atoms_path}"
        )

    semantic_report = _validate_v551_candidate_conservation(
        frames["directional_candidate_adjudication"],
        frames["relation_evidence_atoms"],
        frames["directional_distribution_coverage"],
    )
    effective_evidence = semantic_report["effective_evidence_status"]
    effective_permission = semantic_report["effective_downstream_permission_status"]
    if producer_state.evidence_status == "NOT_APPLICABLE" and effective_evidence != "NOT_APPLICABLE":
        raise BoundaryContractError(
            f"V551_PRODUCER_NOT_APPLICABLE_CONTRADICTS_ARTIFACTS:effective={effective_evidence}"
        )
    if producer_state.downstream_permission_status == "NOT_APPLICABLE" and effective_permission != "NOT_APPLICABLE":
        raise BoundaryContractError("V551_PRODUCER_PERMISSION_NOT_APPLICABLE_CONTRADICTS_ARTIFACTS")
    if producer_state.evidence_status == "APPLICABLE_UNRESOLVED" or producer_state.downstream_permission_status == "DENY":
        if effective_evidence == "PRESENT":
            effective_evidence = "APPLICABLE_UNRESOLVED"
            effective_permission = "DENY"
            semantic_report["effective_evidence_status"] = effective_evidence
            semantic_report["effective_downstream_permission_status"] = effective_permission
            semantic_report["effective_state_detail"] = "PRODUCER_TYPED_UNRESOLVED_STATE"
    if producer_state.downstream_permission_status != "ALLOW" and effective_permission == "ALLOW":
        effective_evidence = "APPLICABLE_UNRESOLVED"
        effective_permission = "DENY"
        semantic_report["effective_evidence_status"] = effective_evidence
        semantic_report["effective_downstream_permission_status"] = effective_permission
        semantic_report["effective_state_detail"] = "CONSUMER_CANNOT_WIDEN_PRODUCER_PERMISSION"

    semantic_report.update(
        {
            "producer_contract_version": _clean(manifest.get("contract_version")),
            "producer_schema_version": _clean(manifest.get("schema_version")),
            "producer_compiler_version": _clean(manifest.get("compiler_version")),
            "producer_run_integrity_status": producer_state.run_integrity_status,
            "producer_evidence_status": producer_state.evidence_status,
            "producer_downstream_permission_status": producer_state.downstream_permission_status,
            "producer_manifest_path": str(manifest_path_obj),
            "producer_manifest_sha256": file_hash(manifest_path_obj),
            "producer_artifact_paths": {name: str(path) for name, path in paths.items()},
            "producer_artifact_file_sha256": {name: file_hash(path) for name, path in paths.items()},
            "expected_scope": expected_scope,
        }
    )
    return {
        "manifest": manifest,
        "manifest_path": manifest_path_obj,
        "state": producer_state,
        "report": semantic_report,
        "atoms": frames["relation_evidence_atoms"],
        "adjudication": frames["directional_candidate_adjudication"],
        "coverage": frames["directional_distribution_coverage"],
        "paths": paths,
    }


def _verify_v550j_producer_surface(
    *,
    run_id: str,
    manifest_path: str | Path,
    readiness_path: str | Path,
    expected_scope: dict[str, Any],
    table_inputs: dict[str, tuple[str | Path, pd.DataFrame]],
) -> dict[str, Any]:
    manifest = _read_json_object(manifest_path, "V550J_MANIFEST")
    readiness = _read_json_object(readiness_path, "V550J_READINESS")

    states = {}
    scopes = {}
    for label, payload in (("V550J_MANIFEST", manifest), ("V550J_READINESS", readiness)):
        contract_version = _clean(payload.get("contract_version"))
        boundary_version = _clean(payload.get("boundary_contract_version"))
        if contract_version != PIPELINE_BOUNDARY_CONTRACT_VERSION or boundary_version != PIPELINE_BOUNDARY_CONTRACT_VERSION:
            raise BoundaryContractError(
                f"{label}_CONTRACT_VERSION_MISMATCH:expected={PIPELINE_BOUNDARY_CONTRACT_VERSION}:contract={contract_version or '<missing>'}:boundary={boundary_version or '<missing>'}"
            )
        if _clean(payload.get("schema_version")) != V550J_PRODUCER_SCHEMA_VERSION:
            raise BoundaryContractError(
                f"{label}_SCHEMA_VERSION_MISMATCH:expected={V550J_PRODUCER_SCHEMA_VERSION}:actual={_clean(payload.get('schema_version')) or '<missing>'}"
            )
        if _clean(payload.get("compiler_version")) != V550J_PRODUCER_COMPILER_VERSION:
            raise BoundaryContractError(
                f"{label}_COMPILER_VERSION_MISMATCH:expected={V550J_PRODUCER_COMPILER_VERSION}:actual={_clean(payload.get('compiler_version')) or '<missing>'}"
            )
        state = boundary_state_from_payload(payload)
        if state.run_integrity_status != "PASS":
            raise BoundaryContractError(f"{label}_RUN_INTEGRITY_NOT_PASS:{state.run_integrity_status}")
        states[label] = state
        scopes[label] = _scope_from_producer_payload(payload, label)

    manifest_state = states["V550J_MANIFEST"]
    readiness_state = states["V550J_READINESS"]
    if (
        manifest_state.evidence_status != readiness_state.evidence_status
        or manifest_state.downstream_permission_status != readiness_state.downstream_permission_status
    ):
        raise BoundaryContractError(
            "V550J_PRODUCER_STATE_DISAGREEMENT:"
            f"manifest={manifest_state.evidence_status}/{manifest_state.downstream_permission_status}:"
            f"readiness={readiness_state.evidence_status}/{readiness_state.downstream_permission_status}"
        )

    for label, scope in scopes.items():
        if scope["run_id"] != run_id:
            raise BoundaryContractError(f"{label}_RUN_ID_MISMATCH:expected={run_id}:actual={scope['run_id'] or '<missing>'}")
        if scope["source"] != expected_scope["source"]:
            raise BoundaryContractError(f"{label}_SOURCE_MISMATCH:expected={expected_scope['source']}:actual={scope['source'] or '<missing>'}")
        if scope["wave"] != expected_scope["wave"]:
            raise BoundaryContractError(f"{label}_WAVE_MISMATCH:expected={expected_scope['wave']}:actual={scope['wave'] or '<missing>'}")
        if expected_scope["shard_id"] and scope["shard_id"] != expected_scope["shard_id"]:
            raise BoundaryContractError(f"{label}_SHARD_ID_MISMATCH:expected={expected_scope['shard_id']}:actual={scope['shard_id'] or '<missing>'}")
        if expected_scope["country_codes"] and scope["country_codes"] and scope["country_codes"] != expected_scope["country_codes"]:
            raise BoundaryContractError(
                f"{label}_COUNTRY_SCOPE_MISMATCH:expected={expected_scope['country_codes']}:actual={scope['country_codes']}"
            )

    declared_tables = manifest.get("tables") or {}
    if not isinstance(declared_tables, dict):
        raise BoundaryContractError("V550J_MANIFEST_TABLE_DECLARATIONS_MALFORMED")
    canonical_names = manifest.get("canonical_artifact_names") or []
    if not isinstance(canonical_names, list):
        raise BoundaryContractError("V550J_CANONICAL_ARTIFACT_NAMES_MALFORMED")
    missing_canonical = sorted(set(table_inputs) - {str(value) for value in canonical_names})
    if missing_canonical:
        raise BoundaryContractError("V550J_CANONICAL_ARTIFACT_SET_INCOMPLETE:" + ",".join(missing_canonical))

    table_report: dict[str, Any] = {}
    for table_name, (supplied_path, frame) in table_inputs.items():
        declaration = declared_tables.get(table_name)
        if not isinstance(declaration, dict):
            raise BoundaryContractError(f"V550J_TABLE_DECLARATION_MISSING:{table_name}")
        declared_path = _clean(declaration.get("parquet_path"))
        if not declared_path:
            raise BoundaryContractError(f"V550J_TABLE_PARQUET_PATH_MISSING:{table_name}")
        if Path(declared_path).suffix.lower() != ".parquet":
            raise BoundaryContractError(f"V550J_TABLE_CANONICAL_PARQUET_REQUIRED:{table_name}:{declared_path}")
        if Path(declared_path).resolve() != Path(supplied_path).resolve():
            raise BoundaryContractError(
                f"V550J_TABLE_PATH_MISMATCH:{table_name}:declared={declared_path}:supplied={supplied_path}"
            )
        if _clean(declaration.get("artifact_kind")) != "canonical":
            raise BoundaryContractError(f"V550J_TABLE_ARTIFACT_KIND_NOT_CANONICAL:{table_name}")
        if _clean(declaration.get("schema_version")) != V550J_PRODUCER_SCHEMA_VERSION:
            raise BoundaryContractError(f"V550J_TABLE_SCHEMA_VERSION_MISMATCH:{table_name}")
        if _clean(declaration.get("compiler_version")) != V550J_PRODUCER_COMPILER_VERSION:
            raise BoundaryContractError(f"V550J_TABLE_COMPILER_VERSION_MISMATCH:{table_name}")
        declared_hash = _clean(declaration.get("artifact_file_sha256")).lower()
        if not re.fullmatch(r"[0-9a-f]{64}", declared_hash):
            raise BoundaryContractError(f"V550J_TABLE_ARTIFACT_FILE_SHA256_MISSING_OR_INVALID:{table_name}")
        actual_hash = file_hash(supplied_path)
        if actual_hash != declared_hash:
            raise BoundaryContractError(
                f"V550J_TABLE_ARTIFACT_FILE_SHA256_MISMATCH:{table_name}:expected={declared_hash}:actual={actual_hash}"
            )
        declared_rows = declaration.get("rows")
        if declared_rows is None or int(declared_rows) != len(frame):
            raise BoundaryContractError(
                f"V550J_TABLE_ROW_COUNT_MISMATCH:{table_name}:declared={declared_rows}:actual={len(frame)}"
            )
        table_report[table_name] = {
            "path": str(Path(supplied_path)),
            "row_count": int(len(frame)),
            "artifact_file_sha256": actual_hash,
            "producer_declared_artifact_file_sha256": declared_hash,
            "hash_status": "MATCHED_PRODUCER_DECLARATION",
        }

    row_counts = [int(item["row_count"]) for item in table_report.values()]
    evidence = manifest_state.evidence_status
    permission = manifest_state.downstream_permission_status
    if evidence == "PRESENT":
        if permission != "ALLOW" or any(count <= 0 for count in row_counts):
            raise BoundaryContractError(
                f"V550J_PRESENT_STATE_INCOMPLETE_OR_NOT_ALLOWED:rows={row_counts}:permission={permission}"
            )
    elif evidence in {"VALID_EMPTY", "NOT_APPLICABLE"}:
        if any(count != 0 for count in row_counts):
            raise BoundaryContractError(f"V550J_EMPTY_STATE_CONTRADICTS_NONEMPTY_TABLES:rows={row_counts}")
        if permission not in {"NOT_APPLICABLE", "DENY"}:
            raise BoundaryContractError(f"V550J_EMPTY_STATE_INVALID_PERMISSION:{permission}")
    elif evidence == "APPLICABLE_UNRESOLVED":
        if permission != "DENY":
            raise BoundaryContractError(f"V550J_UNRESOLVED_STATE_INVALID_PERMISSION:{permission}")
    else:
        raise BoundaryContractError(f"V550J_PRODUCER_EVIDENCE_STATUS_UNSUPPORTED:{evidence}")

    return {
        "run_id": run_id,
        "source": expected_scope["source"],
        "wave": expected_scope["wave"],
        "country_codes": expected_scope["country_codes"],
        "shard_id": expected_scope["shard_id"],
        "manifest_sha256": file_hash(manifest_path),
        "readiness_sha256": file_hash(readiness_path),
        "producer_contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
        "producer_schema_version": V550J_PRODUCER_SCHEMA_VERSION,
        "producer_compiler_version": V550J_PRODUCER_COMPILER_VERSION,
        "producer_run_integrity_status": manifest_state.run_integrity_status,
        "producer_evidence_status": evidence,
        "producer_downstream_permission_status": permission,
        "producer_state_detail": _clean(manifest.get("producer_state_detail")),
        "manifest_validation_status": _clean(manifest.get("validation_status")),
        "readiness_status": _clean(readiness.get("readiness_status")),
        "producer_artifact_hash_contract_status": "PRODUCER_DECLARED_ARTIFACT_FILE_SHA256_VERIFIED",
        "tables": table_report,
    }


def _clear_v551j_stage_outputs(output_dirs: dict[str, Path]) -> None:
    for key in ("packets", "audits", "schemas", "manifest"):
        directory = output_dirs[key]
        directory.mkdir(parents=True, exist_ok=True)
        for child in directory.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    sidecar_dir = output_dirs["root"] / "sidecars"
    if sidecar_dir.exists():
        shutil.rmtree(sidecar_dir)
    sidecar_dir.mkdir(parents=True, exist_ok=True)


def _write_v550j_typed_stop(
    *,
    args: argparse.Namespace,
    output_dirs: dict[str, Path],
    surface_report: dict[str, Any],
    started: float,
) -> int:
    upstream_evidence = surface_report["producer_evidence_status"]
    upstream_permission = surface_report["producer_downstream_permission_status"]
    if upstream_evidence in {"VALID_EMPTY", "NOT_APPLICABLE"}:
        final_status = "VALID_EMPTY_V551J_NO_V550J_JOINT_EVIDENCE"
        evidence_status = "VALID_EMPTY"
        downstream_permission_status = "NOT_APPLICABLE"
        exit_code = 0
        blockers: list[str] = []
    else:
        final_status = "BLOCKED_V550J_APPLICABLE_UNRESOLVED"
        evidence_status = "APPLICABLE_UNRESOLVED"
        downstream_permission_status = "DENY"
        exit_code = 1 if args.strict else 0
        blockers = ["v550j_applicable_but_unresolved"]
    readiness = {
        "contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
        "run_id": args.run_id,
        "schema_version": "v2.2.3",
        "compiler_version": V551J_COMPILER_VERSION,
        "final_status": final_status,
        "run_integrity_status": "PASS",
        "evidence_status": evidence_status,
        "downstream_permission_status": downstream_permission_status,
        "candidate_packet_count": 0,
        "certified_packet_count": 0,
        "review_required_packet_count": 0,
        "blocked_packet_count": 0,
        "ready_for_review": upstream_evidence == "APPLICABLE_UNRESOLVED",
        "ready_for_v552j_joint_evidence": False,
        "ready_for_v553": False,
        "v550j_upstream_contract_status": surface_report.get("producer_state_detail"),
        "blockers_json": json.dumps(blockers, sort_keys=True),
        "created_at": utc_now(),
    }
    provenance = {
        "run_id": args.run_id,
        "schema_version": "v2.2.3",
        "compiler_version": V551J_COMPILER_VERSION,
        "row_counts": {
            "candidate": 0,
            "component": 0,
            "certified": 0,
            "review_surface": 0,
        },
        "final_status": final_status,
        "v550j_producer_surface_report": surface_report,
        "elapsed_seconds": round(monotonic() - started, 3),
        "output_artifacts": {},
    }
    write_json_artifact(output_dirs["manifest"] / "v550j_upstream_contract_report.json", surface_report)
    write_json_artifact(output_dirs["manifest"] / "v551j_input_contract_report.json", {
        "run_id": args.run_id,
        "schema_version": "v2.2.3",
        "compiler_version": V551J_COMPILER_VERSION,
        "required_inputs_status": "PASS",
        "v550j_input_contract_status": final_status,
        "v550j_producer_surface_report": surface_report,
    })
    write_json_artifact(output_dirs["manifest"] / "v551j_packet_contract_validation_report.json", {
        "run_id": args.run_id,
        "candidate_contract_valid": upstream_evidence in {"VALID_EMPTY", "NOT_APPLICABLE"},
        "component_contract_valid": upstream_evidence in {"VALID_EMPTY", "NOT_APPLICABLE"},
        "issue_count": len(blockers),
        "issues_json": json.dumps(blockers, sort_keys=True),
        "validation_status": "valid_empty_upstream" if not blockers else "blocked_upstream_unresolved",
    })
    write_json_artifact(output_dirs["manifest"] / "v551j_readiness_report.json", readiness)
    write_json_artifact(output_dirs["manifest"] / "v551j_input_provenance_manifest.json", provenance)
    write_json_artifact(output_dirs["manifest"] / "manifest.json", {
        "contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
        "boundary_contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
        "producer_run_id": args.run_id,
        "run_id": args.run_id,
        "source": surface_report.get("source", ""),
        "wave": surface_report.get("wave", ""),
        "canonical_wave": surface_report.get("wave", ""),
        "country_code": "",
        "shard_id": surface_report.get("shard_id", ""),
        "schema_version": "v2.2.3",
        "compiler_version": V551J_COMPILER_VERSION,
        "final_status": final_status,
        "run_integrity_status": "PASS",
        "evidence_status": evidence_status,
        "downstream_permission_status": downstream_permission_status,
        "ready_for_v552j_joint_evidence": False,
        "ready_for_v553": False,
        "row_counts": provenance["row_counts"],
        "artifacts": [],
        "output_artifacts": {},
        "v550j_upstream_manifest_sha256": surface_report.get("manifest_sha256"),
        "v550j_upstream_hash_contract_status": surface_report.get("producer_artifact_hash_contract_status"),
        "created_at": utc_now(),
    })
    print(final_status)
    return exit_code


def _write_v551_typed_stop(
    *,
    args: argparse.Namespace,
    output_dirs: dict[str, Path],
    bundle: dict[str, Any],
    required_paths: dict[str, str],
    required_input_hashes: dict[str, str],
    started: float,
) -> int:
    report = dict(bundle["report"])
    evidence_status = report["effective_evidence_status"]
    permission_status = report["effective_downstream_permission_status"]
    if evidence_status == "NOT_APPLICABLE":
        final_status = "NOT_APPLICABLE_V551_NO_DIRECTIONAL_EVIDENCE"
        exit_code = 0
    else:
        final_status = "BLOCKED_V551_APPLICABLE_UNRESOLVED"
        exit_code = 1 if args.strict else 0
    blockers = [] if evidence_status == "NOT_APPLICABLE" else [
        "v551_applicable_but_unresolved",
        *[f"v551_repair_debt:{reason}" for reason in report.get("repair_debt_reason_counts", {})],
    ]
    readiness = {
        "contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
        "run_id": args.run_id,
        "schema_version": "v2.2.3",
        "compiler_version": V551J_COMPILER_VERSION,
        "final_status": final_status,
        "run_integrity_status": "PASS",
        "evidence_status": evidence_status,
        "downstream_permission_status": permission_status,
        "v551_upstream_contract_status": report.get("effective_state_detail"),
        "v551_candidate_count": report.get("candidate_count", 0),
        "v551_promotable_candidate_count": report.get("promotable_candidate_count", 0),
        "v551_repair_debt_candidate_count": report.get("repair_debt_candidate_count", 0),
        "v551_repair_debt_reason_counts": report.get("repair_debt_reason_counts", {}),
        "candidate_packet_count": 0,
        "certified_packet_count": 0,
        "review_required_packet_count": 0,
        "blocked_packet_count": 0,
        "ready_for_review": evidence_status == "APPLICABLE_UNRESOLVED",
        "ready_for_v552j_joint_evidence": False,
        "ready_for_v553": False,
        "blockers_json": json.dumps(blockers, sort_keys=True),
        "created_at": utc_now(),
    }
    provenance = {
        "run_id": args.run_id,
        "schema_version": "v2.2.3",
        "compiler_version": V551J_COMPILER_VERSION,
        "input_hashes": required_input_hashes,
        "row_counts": {
            "v551_atoms": int(len(bundle["atoms"])),
            "v551_directional_candidate_adjudication": int(len(bundle["adjudication"])),
            "v551_directional_distribution_coverage": int(len(bundle["coverage"])),
            "candidate": 0,
            "component": 0,
            "certified": 0,
            "review_surface": 0,
        },
        "final_status": final_status,
        "v551_upstream_contract_report": report,
        **capture_run_provenance(input_documents=required_paths),
        "output_artifacts": {},
        "elapsed_seconds": round(monotonic() - started, 3),
    }
    write_json_artifact(output_dirs["manifest"] / "v551_upstream_contract_report.json", report)
    write_json_artifact(output_dirs["manifest"] / "v551j_input_contract_report.json", {
        "run_id": args.run_id,
        "schema_version": "v2.2.3",
        "compiler_version": V551J_COMPILER_VERSION,
        "required_inputs_status": "PASS",
        "v551_input_contract_status": final_status,
        "v551_upstream_contract_report": report,
    })
    write_json_artifact(output_dirs["manifest"] / "v551j_packet_contract_validation_report.json", {
        "run_id": args.run_id,
        "candidate_contract_valid": False,
        "component_contract_valid": False,
        "issue_count": 0 if evidence_status == "NOT_APPLICABLE" else len(blockers),
        "issues_json": json.dumps(blockers, sort_keys=True),
        "validation_status": "not_applicable" if evidence_status == "NOT_APPLICABLE" else "blocked_upstream_unresolved",
    })
    write_json_artifact(output_dirs["manifest"] / "v551j_readiness_report.json", readiness)
    write_json_artifact(output_dirs["manifest"] / "v551j_input_provenance_manifest.json", provenance)
    write_json_artifact(output_dirs["manifest"] / "manifest.json", {
        "contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
        "boundary_contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
        "producer_run_id": args.run_id,
        "run_id": args.run_id,
        "source": report.get("expected_scope", {}).get("source", ""),
        "wave": report.get("expected_scope", {}).get("wave", ""),
        "canonical_wave": report.get("expected_scope", {}).get("wave", ""),
        "country_code": report.get("expected_scope", {}).get("country_code", ""),
        "shard_id": report.get("expected_scope", {}).get("shard_id", ""),
        "schema_version": "v2.2.3",
        "compiler_version": V551J_COMPILER_VERSION,
        "final_status": final_status,
        "run_integrity_status": "PASS",
        "evidence_status": evidence_status,
        "downstream_permission_status": permission_status,
        "ready_for_v552j_joint_evidence": False,
        "ready_for_v553": False,
        "row_counts": provenance["row_counts"],
        "artifacts": [],
        "output_artifacts": {},
        "v551_upstream_manifest_sha256": report.get("producer_manifest_sha256"),
        "created_at": utc_now(),
    })
    print(final_status)
    return exit_code


def _derive_v551j_boundary_state(
    *,
    candidate_count: int,
    certified_count: int,
    review_count: int,
    validation_issues: list[str],
    strict: bool,
) -> tuple[str, str, str, str]:
    if validation_issues:
        return "FAIL", "APPLICABLE_UNRESOLVED", "DENY", "BLOCKED_V551J_OUTPUT_CONTRACT"
    if certified_count > 0 and strict:
        return "PASS", "PRESENT", "ALLOW", "READY_V551J_JOINT_EVIDENCE_CONTRACT"
    if not strict:
        evidence = "PRESENT" if candidate_count > 0 else "VALID_EMPTY"
        return "PASS", evidence, "DENY", "DIAGNOSTIC_V551J_NO_STRICT_NOT_READY"
    if candidate_count == 0:
        return "PASS", "VALID_EMPTY", "NOT_APPLICABLE", "VALID_EMPTY_V551J_NO_JOINT_EVIDENCE"
    if review_count > 0:
        return "PASS", "PRESENT", "DENY", "VALID_V551J_REVIEW_ONLY_NOT_DOWNSTREAM"
    return "PASS", "VALID_EMPTY", "NOT_APPLICABLE", "VALID_EMPTY_V551J_NO_CERTIFIED_JOINT_EVIDENCE"


def _enrich_output_artifacts(
    artifact_info: dict[str, dict[str, object]],
    *,
    output_root: Path,
) -> list[dict[str, Any]]:
    declarations: list[dict[str, Any]] = []
    for key, info in artifact_info.items():
        path_text = _clean(info.get("path"))
        if not path_text:
            continue
        path = Path(path_text)
        if not path.exists():
            raise BoundaryContractError(f"V551J_OUTPUT_ARTIFACT_MISSING_AFTER_WRITE:{key}:{path}")
        artifact_hash = file_hash(path)
        info["artifact_file_sha256"] = artifact_hash
        info["artifact_kind"] = "compatibility" if key.startswith("compatibility_") else "canonical"
        try:
            rel = path.resolve().relative_to(output_root.resolve())
        except ValueError as exc:
            raise BoundaryContractError(f"V551J_OUTPUT_ARTIFACT_ESCAPES_RUN_ROOT:{key}:{path}") from exc
        declarations.append({
            "artifact": key,
            "path": str(Path("..") / rel),
            "artifact_kind": info["artifact_kind"],
            "row_count": int(info.get("rows") or 0),
            "artifact_file_sha256": artifact_hash,
            "schema_version": "v2.2.3",
        })
    return declarations


def main() -> int:
    args = parse_args()
    if not args.write_parquet:
        raise BoundaryContractError("PARQUET_CANONICAL_OUTPUT_REQUIRED")
    if args.emit_certified_index and not args.emit_review_surface:
        raise RuntimeError("V551J_C_CERTIFICATION_REQUIRES_REVIEW_SURFACE: pass --emit-review-surface with --emit-certified-index")
    output_dirs = ensure_output_dirs(args.output_root, args.run_id)
    _clear_v551j_stage_outputs(output_dirs)
    sidecar_dir = output_dirs["root"] / "sidecars"
    v551_manifest_path = _resolve_v551_manifest_path(args.v551_atoms_path, args.v551_manifest_path)
    required_paths = {
        "v551_atoms_path": args.v551_atoms_path,
        "v551_manifest_path": str(v551_manifest_path),
        "v550j_pattern_index_path": args.v550j_pattern_index_path,
        "v550j_pattern_item_index_path": args.v550j_pattern_item_index_path,
        "v550j_relation_signature_path": args.v550j_relation_signature_path,
        "v550j_manifest_path": args.v550j_manifest_path,
        "v550j_readiness_report_path": args.v550j_readiness_report_path,
        "registry_path": args.registry_path,
    }
    v550j_required_paths = {
        name: path
        for name, path in required_paths.items()
        if name.startswith("v550j_")
    }
    missing_required = [name for name, path in v550j_required_paths.items() if not path or not Path(path).exists()]
    if missing_required:
        write_json_artifact(output_dirs["manifest"] / "v551j_readiness_report.json", {
            "contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
            "run_id": args.run_id,
            "schema_version": "v2.2.3",
            "compiler_version": V551J_COMPILER_VERSION,
            "final_status": "BLOCKED_V551J_MISSING_REQUIRED_INPUTS",
            "run_integrity_status": "FAIL",
            "evidence_status": "APPLICABLE_UNRESOLVED",
            "downstream_permission_status": "DENY",
            "blockers_json": missing_required,
            "ready_for_v552j_joint_evidence": False,
            "ready_for_v553": False,
            "created_at": utc_now(),
        })
        print("BLOCKED_V551J_MISSING_REQUIRED_INPUTS")
        return 1
    started = monotonic()
    pattern_index = _load(args.v550j_pattern_index_path)
    pattern_item_index = _load(args.v550j_pattern_item_index_path)
    relation_signature = _load(args.v550j_relation_signature_path)
    association_index = _load(args.v550j_association_index_path)
    position_signature = _load(args.v550j_position_signature_path)
    meaning_summary = _load(args.v550j_meaning_summary_path)
    expected_scope = _expected_v551_scope(
        args.run_id,
        pattern_index,
        pattern_item_index,
        args.v550j_manifest_path,
    )
    v550j_surface_report = _verify_v550j_producer_surface(
        run_id=args.run_id,
        manifest_path=args.v550j_manifest_path,
        readiness_path=args.v550j_readiness_report_path,
        expected_scope=expected_scope,
        table_inputs={
            "joint_response_pattern_index": (args.v550j_pattern_index_path, pattern_index),
            "joint_response_pattern_item_index": (args.v550j_pattern_item_index_path, pattern_item_index),
            "joint_pattern_relation_signature": (args.v550j_relation_signature_path, relation_signature),
        },
    )
    if (
        v550j_surface_report["producer_evidence_status"] != "PRESENT"
        or v550j_surface_report["producer_downstream_permission_status"] != "ALLOW"
    ):
        return _write_v550j_typed_stop(
            args=args,
            output_dirs=output_dirs,
            surface_report=v550j_surface_report,
            started=started,
        )

    remaining_required = {
        name: path
        for name, path in required_paths.items()
        if not name.startswith("v550j_")
    }
    missing_required = [name for name, path in remaining_required.items() if not path or not Path(path).exists()]
    if missing_required:
        write_json_artifact(output_dirs["manifest"] / "v551j_readiness_report.json", {
            "contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
            "run_id": args.run_id,
            "schema_version": "v2.2.3",
            "compiler_version": V551J_COMPILER_VERSION,
            "final_status": "BLOCKED_V551J_MISSING_REQUIRED_INPUTS",
            "run_integrity_status": "FAIL",
            "evidence_status": "APPLICABLE_UNRESOLVED",
            "downstream_permission_status": "DENY",
            "blockers_json": missing_required,
            "ready_for_v552j_joint_evidence": False,
            "ready_for_v553": False,
            "created_at": utc_now(),
        })
        print("BLOCKED_V551J_MISSING_REQUIRED_INPUTS")
        return 1

    v551_bundle = _verify_v551_v3_bundle(
        run_id=args.run_id,
        manifest_path=v551_manifest_path,
        atoms_path=args.v551_atoms_path,
        expected_scope=expected_scope,
    )
    atoms = v551_bundle["atoms"]
    required_paths.update({
        "v551_directional_candidate_adjudication_path": str(v551_bundle["paths"]["directional_candidate_adjudication"]),
        "v551_directional_distribution_coverage_path": str(v551_bundle["paths"]["directional_distribution_coverage"]),
    })
    deprecated_v552_inputs = {
        "v552_question_semantic_hierarchy_path": args.v552_question_semantic_hierarchy_path,
        "v552_structural_channel_index_path": args.v552_structural_channel_index_path,
        "v552_relation_axis_pressure_path": args.v552_relation_axis_pressure_path,
        "v552_target_entity_pressure_path": args.v552_target_entity_pressure_path,
        "v552_driver_facet_pressure_path": args.v552_driver_facet_pressure_path,
        "v552_contradiction_surface_path": args.v552_contradiction_surface_path,
        "v552_horizon_constraint_index_path": args.v552_horizon_constraint_index_path,
        "v552_parent_prior_manifest_path": args.v552_parent_prior_manifest_path,
    }
    required_input_hashes = {
        "v551_atoms_artifact_hash": file_hash(args.v551_atoms_path),
        "v551_manifest_hash": file_hash(v551_manifest_path),
        "v551_directional_candidate_adjudication_artifact_hash": file_hash(v551_bundle["paths"]["directional_candidate_adjudication"]),
        "v551_directional_distribution_coverage_artifact_hash": file_hash(v551_bundle["paths"]["directional_distribution_coverage"]),
        "v550j_pattern_index_artifact_hash": file_hash(args.v550j_pattern_index_path),
        "v550j_pattern_item_index_artifact_hash": file_hash(args.v550j_pattern_item_index_path),
        "v550j_relation_signature_artifact_hash": file_hash(args.v550j_relation_signature_path),
        "v550j_manifest_hash": file_hash(args.v550j_manifest_path),
        "v550j_readiness_report_hash": file_hash(args.v550j_readiness_report_path),
        "question_family_registry_hash": file_hash(args.registry_path),
    }

    if v551_bundle["report"]["effective_evidence_status"] != "PRESENT" or v551_bundle["report"]["effective_downstream_permission_status"] != "ALLOW":
        return _write_v551_typed_stop(
            args=args,
            output_dirs=output_dirs,
            bundle=v551_bundle,
            required_paths=required_paths,
            required_input_hashes=required_input_hashes,
            started=started,
        )

    def _input_provenance_audit(scope_audit: pd.DataFrame) -> pd.DataFrame:
        scope_status = dict(zip(scope_audit.get("artifact_name", pd.Series(dtype=str)).astype(str), scope_audit.get("scope_contract_status", pd.Series(dtype=str)).astype(str))) if not scope_audit.empty else {}
        rows = []
        specs = [
            ("v551_atoms", args.v551_atoms_path, required_input_hashes["v551_atoms_artifact_hash"]),
            ("v551_manifest", str(v551_manifest_path), required_input_hashes["v551_manifest_hash"]),
            ("v551_directional_candidate_adjudication", str(v551_bundle["paths"]["directional_candidate_adjudication"]), required_input_hashes["v551_directional_candidate_adjudication_artifact_hash"]),
            ("v551_directional_distribution_coverage", str(v551_bundle["paths"]["directional_distribution_coverage"]), required_input_hashes["v551_directional_distribution_coverage_artifact_hash"]),
            ("v550j_pattern_index", args.v550j_pattern_index_path, required_input_hashes["v550j_pattern_index_artifact_hash"]),
            ("v550j_pattern_item_index", args.v550j_pattern_item_index_path, required_input_hashes["v550j_pattern_item_index_artifact_hash"]),
            ("v550j_relation_signature", args.v550j_relation_signature_path, required_input_hashes["v550j_relation_signature_artifact_hash"]),
            ("v550j_manifest", args.v550j_manifest_path, required_input_hashes["v550j_manifest_hash"]),
            ("v550j_readiness_report", args.v550j_readiness_report_path, required_input_hashes["v550j_readiness_report_hash"]),
            ("question_family_registry", args.registry_path, required_input_hashes["question_family_registry_hash"]),
        ]
        for artifact_name, input_path, expected_hash in specs:
            path = Path(input_path)
            exists = path.exists()
            actual_hash = file_hash(path)
            rows.append({
                "run_id": args.run_id,
                "artifact_name": artifact_name,
                "input_path": str(path),
                "size_bytes": path.stat().st_size if exists else "",
                "sha256": actual_hash,
                "exists": exists,
                "hash_format_valid": bool(re.fullmatch(r"[0-9a-f]{64}", actual_hash)),
                "hash_matches_file": exists and actual_hash == file_hash(path),
                "expected_governed_hash": expected_hash,
                "governed_hash_matches": actual_hash == expected_hash,
                "scope_status": scope_status.get(artifact_name, "PASS"),
                "created_at": utc_now(),
                "schema_version": "v2.2.3",
                "compiler_version": V551J_COMPILER_VERSION,
            })
        return pd.DataFrame(rows).reindex(columns=V551J_INPUT_PROVENANCE_AUDIT_SCHEMA["required_columns"])

    outputs = build_v551j_joint_outputs_v2(
        run_id=args.run_id,
        atoms=atoms,
        pattern_index=pattern_index,
        pattern_item_index=pattern_item_index,
        relation_signature=relation_signature,
        registry_path=args.registry_path,
        v550j_manifest_path=args.v550j_manifest_path,
        v550j_readiness_report_path=args.v550j_readiness_report_path,
        association_index=association_index,
        position_signature=position_signature,
        meaning_summary=meaning_summary,
        deprecated_v552_inputs_supplied=sum(1 for value in deprecated_v552_inputs.values() if value),
        input_hashes=required_input_hashes,
    )
    outputs["input_provenance_audit"] = _input_provenance_audit(outputs["input_scope_audit"])
    finalized_candidate, certified, certification_audit, certification_rejection = certify_v551j_v2_2_3(
        outputs["candidate"],
        outputs["component"],
        outputs["packet_contract_validation_report"],
    )
    outputs["candidate"] = finalized_candidate
    outputs["certified"] = certified
    outputs["certification_audit"] = certification_audit
    outputs["certification_rejection_audit"] = certification_rejection

    def _refresh_packet_hashes() -> None:
        csv_component = pd.read_csv(StringIO(_contract_csv_text(outputs["component"])), dtype=str, keep_default_na=False) if not outputs["component"].empty else outputs["component"].copy()
        if not csv_component.empty:
            component_hashes = [recompute_v551j_component_contract_hash(row) for _, row in csv_component.iterrows()]
            outputs["component"]["component_contract_hash"] = component_hashes
            csv_component["component_contract_hash"] = component_hashes
        csv_candidate = pd.read_csv(StringIO(_contract_csv_text(outputs["candidate"])), dtype=str, keep_default_na=False) if not outputs["candidate"].empty else outputs["candidate"].copy()
        if not csv_candidate.empty:
            measurement_hashes = [recompute_joint_measurement_contract_hash(row) for _, row in csv_candidate.iterrows()]
            outputs["candidate"]["joint_measurement_contract_hash"] = measurement_hashes
        csv_candidate = pd.read_csv(StringIO(_contract_csv_text(outputs["candidate"])), dtype=str, keep_default_na=False) if not outputs["candidate"].empty else outputs["candidate"].copy()
        if not csv_candidate.empty:
            packet_hashes = []
            for _, packet_row in csv_candidate.iterrows():
                component_rows = csv_component[csv_component["packet_id"].astype(str).eq(str(packet_row.get("packet_id")))].sort_values("item_order", kind="mergesort").to_dict("records")
                packet_hashes.append(recompute_v551j_v2_2_3_packet_contract_hash(packet_row, component_rows))
            outputs["candidate"]["packet_contract_hash"] = packet_hashes
        if not outputs["certified"].empty:
            hash_map = dict(zip(outputs["candidate"]["packet_id"].astype(str), outputs["candidate"]["packet_contract_hash"].astype(str)))
            measure_map = dict(zip(outputs["candidate"]["packet_id"].astype(str), outputs["candidate"]["joint_measurement_contract_hash"].astype(str)))
            outputs["certified"]["packet_contract_hash"] = outputs["certified"]["packet_id"].astype(str).map(hash_map)
            outputs["certified"]["joint_measurement_contract_hash"] = outputs["certified"]["packet_id"].astype(str).map(measure_map)

    def _rebuild_review_surface() -> None:
        from data.ddm_build_copy.ddm_v551j_schema import V551J_JOINT_PACKET_REVIEW_SURFACE_SCHEMA
        review_rows = outputs["candidate"][outputs["candidate"]["review_required"].fillna(False).astype(bool)].copy()
        if review_rows.empty:
            outputs["review_surface"] = pd.DataFrame(columns=V551J_JOINT_PACKET_REVIEW_SURFACE_SCHEMA["required_columns"])
            return
        review_rows["review_priority"] = "medium"
        review_rows["review_triage_priority_score"] = 0.5
        outputs["review_surface"] = review_rows.reindex(columns=V551J_JOINT_PACKET_REVIEW_SURFACE_SCHEMA["required_columns"])

    for frame_name in ("candidate", "certified"):
        frame = outputs[frame_name].copy()
        if not frame.empty:
            hashes = []
            for _, packet_row in frame.iterrows():
                component_rows = outputs["component"][outputs["component"]["packet_id"].astype(str).eq(str(packet_row.get("packet_id")))].sort_values("item_order", kind="mergesort").to_dict("records")
                hashes.append(recompute_v551j_v2_2_3_packet_contract_hash(packet_row, component_rows))
            frame["packet_contract_hash"] = hashes
            outputs[frame_name] = frame
    _refresh_packet_hashes()
    _rebuild_review_surface()
    outputs["readiness_report"]["candidate_packet_count"] = int(len(finalized_candidate))
    outputs["readiness_report"]["certified_packet_count"] = int(len(certified))
    outputs["readiness_report"]["review_required_packet_count"] = int(finalized_candidate["review_required"].fillna(False).astype(bool).sum())
    outputs["readiness_report"]["blocked_packet_count"] = int(finalized_candidate["certification_status"].astype(str).str.startswith("BLOCKED").sum())
    outputs["readiness_report"]["ready_for_review"] = bool(outputs["readiness_report"]["review_required_packet_count"])
    outputs["readiness_report"]["v551_upstream_run_integrity_status"] = v551_bundle["report"]["producer_run_integrity_status"]
    outputs["readiness_report"]["v551_upstream_evidence_status"] = v551_bundle["report"]["effective_evidence_status"]
    outputs["readiness_report"]["v551_upstream_downstream_permission_status"] = v551_bundle["report"]["effective_downstream_permission_status"]
    outputs["readiness_report"]["v551_upstream_manifest_sha256"] = v551_bundle["report"]["producer_manifest_sha256"]
    outputs["readiness_report"]["v550j_producer_surface_status"] = "VERIFIED_TYPED_PRODUCER_BOUNDARY"
    validation_issues = []
    if str(outputs["readiness_report"].get("registry_contract_status")) != "MATCHED_GOVERNED_REGISTRY_HASH":
        validation_issues.append("registry_hash_mismatch")
    if str(outputs["readiness_report"].get("scope_contract_status")) != "PASS":
        validation_issues.append("scope_contract_mismatch")
    provenance_failures = outputs["input_provenance_audit"]
    if not provenance_failures.empty:
        bad_provenance = provenance_failures[
            ~provenance_failures["exists"].astype(bool)
            | ~provenance_failures["hash_format_valid"].astype(bool)
            | ~provenance_failures["hash_matches_file"].astype(bool)
            | ~provenance_failures["governed_hash_matches"].astype(bool)
            | provenance_failures["scope_status"].astype(str).ne("PASS")
        ]
        if not bad_provenance.empty:
            validation_issues.append("input_provenance_failure")
    strict_failed = False
    if validation_issues:
        outputs["packet_contract_validation_report"]["candidate_contract_valid"] = False
        outputs["packet_contract_validation_report"]["component_contract_valid"] = False
        outputs["packet_contract_validation_report"]["issue_count"] = len(validation_issues)
        outputs["packet_contract_validation_report"]["issues_json"] = json.dumps(validation_issues, sort_keys=True)
        outputs["readiness_report"]["candidate_contract_valid"] = False
        outputs["readiness_report"]["component_contract_valid"] = False
        outputs["readiness_report"]["ready_for_v552j_joint_evidence"] = False
        outputs["readiness_report"]["final_status"] = "BLOCKED_V551J_OUTPUT_CONTRACT"
        outputs["readiness_report"]["blockers_json"] = json.dumps(validation_issues, sort_keys=True)
        if args.strict:
            strict_failed = True
            frame = outputs.get("candidate")
            if frame is not None and not frame.empty:
                for column in ("ready_for_v552j_joint_evidence", "ready_for_v552j_component_linkage", "ready_for_v553", "pressure_anchor_eligible", "temporal_pressure_authorized"):
                    if column in frame.columns:
                        frame[column] = False
                frame["certification_status"] = "BLOCKED_PACKET_CONTRACT"
                frame["review_required"] = False
                frame["review_reason_codes_json"] = "[]"
                if "blocking_reason_codes_json" in frame.columns:
                    frame["blocking_reason_codes_json"] = json.dumps(validation_issues, sort_keys=True)
                if "allowed_future_targets_json" in frame.columns:
                    frame["allowed_future_targets_json"] = "[]"
                if "runtime_use_class" in frame.columns:
                    frame["runtime_use_class"] = "not_runtime_consumable"
            outputs["candidate"] = frame
            if not outputs["certification_audit"].empty:
                outputs["certification_audit"]["certified"] = False
                outputs["certification_audit"]["certification_blockers_json"] = json.dumps(validation_issues, sort_keys=True)
            outputs["certified"] = outputs["certified"].iloc[0:0].copy()
            outputs["review_surface"] = outputs["review_surface"].iloc[0:0].copy()
            _refresh_packet_hashes()
            _rebuild_review_surface()
            for frame_name in ("candidate", "certified", "review_surface"):
                frame = outputs.get(frame_name)
                if frame is None or frame.empty:
                    continue
                for column in ("ready_for_v552j_joint_evidence", "ready_for_v552j_component_linkage", "ready_for_v553", "pressure_anchor_eligible", "temporal_pressure_authorized"):
                    if column in frame.columns:
                        frame[column] = False
                if "allowed_future_targets_json" in frame.columns:
                    frame["allowed_future_targets_json"] = "[]"
                if "runtime_use_class" in frame.columns:
                    frame["runtime_use_class"] = "not_runtime_consumable"
                outputs[frame_name] = frame
    if not args.strict:
        for frame_name in ("candidate", "certified", "review_surface"):
            frame = outputs.get(frame_name)
            if frame is None or frame.empty:
                continue
            for column in ("ready_for_v552j_joint_evidence", "ready_for_v552j_component_linkage"):
                if column in frame.columns:
                    frame[column] = False
            if "allowed_future_targets_json" in frame.columns:
                frame["allowed_future_targets_json"] = "[]"
            for column in ("ready_for_v553", "pressure_anchor_eligible", "temporal_pressure_authorized"):
                if column in frame.columns:
                    frame[column] = False
            if "runtime_use_class" in frame.columns:
                frame["runtime_use_class"] = "not_runtime_consumable"
            outputs[frame_name] = frame
        if not outputs["certification_audit"].empty:
            outputs["certification_audit"]["certified"] = False
            outputs["certification_audit"]["certification_notes_json"] = "[\"diagnostic_no_strict\"]"
        outputs["certified"] = outputs["certified"].iloc[0:0].copy()
        _refresh_packet_hashes()
        _rebuild_review_surface()
    outputs["readiness_report"]["candidate_packet_count"] = int(len(outputs["candidate"]))
    outputs["readiness_report"]["certified_packet_count"] = int(len(outputs["certified"]))
    outputs["readiness_report"]["review_required_packet_count"] = int(outputs["candidate"].get("review_required", pd.Series(dtype=str)).astype(str).str.lower().eq("true").sum()) if not outputs["candidate"].empty else 0
    outputs["readiness_report"]["blocked_packet_count"] = int(outputs["candidate"].get("certification_status", pd.Series(dtype=str)).astype(str).str.startswith("BLOCKED").sum()) if not outputs["candidate"].empty else 0
    outputs["readiness_report"]["ready_for_review"] = bool(len(outputs["review_surface"]))
    boundary_integrity, boundary_evidence, boundary_permission, boundary_final = _derive_v551j_boundary_state(
        candidate_count=int(len(outputs["candidate"])),
        certified_count=int(len(outputs["certified"])),
        review_count=int(len(outputs["review_surface"])),
        validation_issues=validation_issues,
        strict=bool(args.strict),
    )
    outputs["readiness_report"]["contract_version"] = PIPELINE_BOUNDARY_CONTRACT_VERSION
    outputs["readiness_report"]["run_integrity_status"] = boundary_integrity
    outputs["readiness_report"]["evidence_status"] = boundary_evidence
    outputs["readiness_report"]["downstream_permission_status"] = boundary_permission
    outputs["readiness_report"]["ready_for_v552j_joint_evidence"] = boundary_permission == "ALLOW"
    outputs["readiness_report"]["final_status"] = boundary_final
    outputs["input_provenance_manifest"]["row_counts"]["candidate"] = int(len(outputs["candidate"]))
    outputs["input_provenance_manifest"]["row_counts"]["component"] = int(len(outputs["component"]))
    outputs["input_provenance_manifest"]["row_counts"]["certified"] = int(len(outputs["certified"]))
    outputs["input_provenance_manifest"]["row_counts"]["review_surface"] = int(len(outputs["review_surface"]))
    outputs["input_provenance_manifest"]["row_counts"]["v551_directional_candidate_adjudication"] = int(len(v551_bundle["adjudication"]))
    outputs["input_provenance_manifest"]["row_counts"]["v551_directional_distribution_coverage"] = int(len(v551_bundle["coverage"]))
    outputs["input_provenance_manifest"]["v551_upstream_contract_report"] = v551_bundle["report"]
    outputs["input_provenance_manifest"]["v550j_producer_surface_report"] = v550j_surface_report
    outputs["input_provenance_manifest"]["final_status"] = outputs["readiness_report"]["final_status"]
    frame_targets = {
        "candidate": (output_dirs["packets"] / "v551j_joint_packet_candidate_index.parquet", "v551j_joint_packet_candidate_index"),
        "component": (output_dirs["packets"] / "v551j_joint_component_index.parquet", "v551j_joint_component_index"),
        "certified": (output_dirs["packets"] / "v551j_certified_joint_packet_index.parquet", "v551j_certified_joint_packet_index"),
        "review_surface": (output_dirs["packets"] / "v551j_review_surface.parquet", "v551j_review_surface"),
        "pattern_context_sidecar": (sidecar_dir / "v551j_pattern_context_sidecar.parquet", "v551j_pattern_context_sidecar"),
        "association_context_sidecar": (sidecar_dir / "v551j_association_context_sidecar.parquet", "v551j_association_context_sidecar"),
        "position_context_sidecar": (sidecar_dir / "v551j_position_context_sidecar.parquet", "v551j_position_context_sidecar"),
        "meaning_summary_sidecar": (sidecar_dir / "v551j_meaning_summary_sidecar.parquet", "v551j_meaning_summary_sidecar"),
        "component_match_audit": (output_dirs["audits"] / "v551j_component_match_audit.parquet", "v551j_component_match_audit"),
        "cross_contract_comparison_audit": (output_dirs["audits"] / "v551j_cross_contract_comparison_audit.parquet", "v551j_cross_contract_comparison_audit"),
        "target_layer_audit": (output_dirs["audits"] / "v551j_target_layer_audit.parquet", "v551j_target_layer_audit"),
        "denominator_separation_audit": (output_dirs["audits"] / "v551j_denominator_separation_audit.parquet", "v551j_denominator_separation_audit"),
        "measurement_separation_audit": (output_dirs["audits"] / "v551j_measurement_separation_audit.parquet", "v551j_measurement_separation_audit"),
        "certification_audit": (output_dirs["audits"] / "v551j_certification_audit.parquet", "v551j_certification_audit"),
        "certification_rejection_audit": (output_dirs["audits"] / "v551j_certification_rejection_audit.parquet", "v551j_certification_rejection_audit"),
        "input_scope_audit": (output_dirs["audits"] / "v551j_input_scope_audit.parquet", "v551j_input_scope_audit"),
        "input_provenance_audit": (output_dirs["audits"] / "v551j_input_provenance_audit.parquet", "v551j_input_provenance_audit"),
        "registry_contract_audit": (output_dirs["audits"] / "v551j_registry_contract_audit.parquet", "v551j_registry_contract_audit"),
    }
    artifact_info: dict[str, dict[str, object]] = {}
    for key, (path, name) in frame_targets.items():
        frame = outputs[key]
        artifact_info[key] = write_frame_artifact(
            frame,
            path=path,
            schema_path=output_dirs["schemas"] / f"{name}.schema.json",
            name=name,
            run_id=args.run_id,
            write_csv=args.write_csv,
            write_parquet=args.write_parquet,
        )
    compatibility = outputs["candidate"].copy()
    compatibility["compatibility_projection_only"] = True
    compatibility["not_authoritative_v2_artifact"] = True
    compatibility["v551_v3_completeness_status"] = "COMPLETE"
    compatibility["v551_v3_manifest_sha256"] = v551_bundle["report"]["producer_manifest_sha256"]
    artifact_info["compatibility_candidate_trace"] = write_frame_artifact(
        compatibility,
        path=output_dirs["packets"] / "v551j_packet_candidate_trace.parquet",
        schema_path=output_dirs["schemas"] / "v551j_packet_candidate_trace.schema.json",
        name="v551j_packet_candidate_trace",
        run_id=args.run_id,
        write_csv=args.write_csv,
        write_parquet=args.write_parquet,
    )
    artifact_info["compatibility_certified_packet_index"] = write_frame_artifact(
        outputs["certified"],
        path=output_dirs["packets"] / "v551j_certified_packet_index.parquet",
        schema_path=output_dirs["schemas"] / "v551j_certified_packet_index.schema.json",
        name="v551j_certified_packet_index",
        run_id=args.run_id,
        write_csv=args.write_csv,
        write_parquet=args.write_parquet,
    )
    if args.write_csv:
        execution_mode = "strict_blocked" if strict_failed else "diagnostic" if not args.strict else "acceptance"
        written_issues = validate_written_v551j_artifacts(
            candidate_path=output_dirs["packets"] / "v551j_joint_packet_candidate_index.csv",
            component_path=output_dirs["packets"] / "v551j_joint_component_index.csv",
            certified_path=output_dirs["packets"] / "v551j_certified_joint_packet_index.csv",
            review_path=output_dirs["packets"] / "v551j_review_surface.csv",
            certification_audit_path=output_dirs["audits"] / "v551j_certification_audit.csv",
            expected_registry_hash=required_input_hashes["question_family_registry_hash"],
            execution_mode=execution_mode,
        )
        if written_issues:
            outputs["packet_contract_validation_report"]["candidate_contract_valid"] = False
            outputs["packet_contract_validation_report"]["component_contract_valid"] = False
            outputs["packet_contract_validation_report"]["issue_count"] = len(written_issues)
            outputs["packet_contract_validation_report"]["issues_json"] = json.dumps(written_issues, sort_keys=True)
            outputs["readiness_report"]["candidate_contract_valid"] = False
            outputs["readiness_report"]["component_contract_valid"] = False
            validation_issues.extend(issue for issue in written_issues if issue not in validation_issues)
            strict_failed = bool(args.strict)
            boundary_integrity, boundary_evidence, boundary_permission, boundary_final = _derive_v551j_boundary_state(
                candidate_count=int(len(outputs["candidate"])),
                certified_count=int(len(outputs["certified"])),
                review_count=int(len(outputs["review_surface"])),
                validation_issues=validation_issues,
                strict=bool(args.strict),
            )
            outputs["readiness_report"]["run_integrity_status"] = boundary_integrity
            outputs["readiness_report"]["evidence_status"] = boundary_evidence
            outputs["readiness_report"]["downstream_permission_status"] = boundary_permission
            outputs["readiness_report"]["ready_for_v552j_joint_evidence"] = boundary_permission == "ALLOW"
            outputs["readiness_report"]["final_status"] = boundary_final
    boundary_artifacts = _enrich_output_artifacts(artifact_info, output_root=output_dirs["root"])
    provenance = outputs["input_provenance_manifest"]
    provenance.update({
        **capture_run_provenance(input_documents={**required_paths, **{k: v or "" for k, v in deprecated_v552_inputs.items()}}),
        "output_artifacts": artifact_info,
        "v550j_producer_surface_report": v550j_surface_report,
        "elapsed_seconds": round(monotonic() - started, 3),
    })
    write_json_artifact(output_dirs["manifest"] / "v551_upstream_contract_report.json", v551_bundle["report"])
    write_json_artifact(output_dirs["manifest"] / "v550j_upstream_contract_report.json", v550j_surface_report)
    write_json_artifact(output_dirs["manifest"] / "v551j_input_contract_report.json", outputs["input_contract_report"])
    write_json_artifact(output_dirs["manifest"] / "v551j_packet_contract_validation_report.json", outputs["packet_contract_validation_report"])
    write_json_artifact(output_dirs["manifest"] / "v551j_readiness_report.json", outputs["readiness_report"])
    write_json_artifact(output_dirs["manifest"] / "v551j_input_provenance_manifest.json", provenance)
    write_json_artifact(output_dirs["manifest"] / "manifest.json", {
        "contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
        "boundary_contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
        "producer_run_id": args.run_id,
        "run_id": args.run_id,
        "source": expected_scope["source"],
        "wave": expected_scope["wave"],
        "canonical_wave": expected_scope["wave"],
        "country_code": expected_scope["country_code"],
        "shard_id": expected_scope["shard_id"],
        "schema_version": "v2.2.3",
        "compiler_version": V551J_COMPILER_VERSION,
        "final_status": outputs["readiness_report"].get("final_status"),
        "run_integrity_status": outputs["readiness_report"].get("run_integrity_status"),
        "evidence_status": outputs["readiness_report"].get("evidence_status"),
        "downstream_permission_status": outputs["readiness_report"].get("downstream_permission_status"),
        "ready_for_v552j_joint_evidence": outputs["readiness_report"].get("ready_for_v552j_joint_evidence"),
        "ready_for_v553": False,
        "row_counts": outputs["input_provenance_manifest"].get("row_counts", {}),
        "artifacts": boundary_artifacts,
        "output_artifacts": artifact_info,
        "v551_upstream_contract_version": v551_bundle["report"]["producer_contract_version"],
        "v551_upstream_schema_version": v551_bundle["report"]["producer_schema_version"],
        "v551_upstream_run_integrity_status": v551_bundle["report"]["producer_run_integrity_status"],
        "v551_upstream_evidence_status": v551_bundle["report"]["effective_evidence_status"],
        "v551_upstream_downstream_permission_status": v551_bundle["report"]["effective_downstream_permission_status"],
        "v551_upstream_manifest_sha256": v551_bundle["report"]["producer_manifest_sha256"],
        "v550j_upstream_contract_version": v550j_surface_report["producer_contract_version"],
        "v550j_upstream_schema_version": v550j_surface_report["producer_schema_version"],
        "v550j_upstream_compiler_version": v550j_surface_report["producer_compiler_version"],
        "v550j_upstream_run_integrity_status": v550j_surface_report["producer_run_integrity_status"],
        "v550j_upstream_evidence_status": v550j_surface_report["producer_evidence_status"],
        "v550j_upstream_downstream_permission_status": v550j_surface_report["producer_downstream_permission_status"],
        "v550j_upstream_manifest_sha256": v550j_surface_report["manifest_sha256"],
        "v550j_upstream_hash_contract_status": v550j_surface_report["producer_artifact_hash_contract_status"],
        "created_at": utc_now(),
    })
    print(outputs["readiness_report"]["final_status"])
    return 1 if strict_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
