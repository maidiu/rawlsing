#!/usr/bin/env python3
"""Cross-wave comparability and semantic diff helpers for V551J.

This is a provisional V551J-D layer. It compares two V551J runs and makes
differences explicit without emitting runtime-facing outputs.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

import pandas as pd
from pandas.errors import EmptyDataError

try:
    from data.ddm_build_copy.ddm_v550_manifest import utc_now
except ModuleNotFoundError:  # pragma: no cover - keeps patch tests runnable outside the full repo
    from datetime import datetime, timezone

    def utc_now() -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


V551J_SEMANTIC_DIFF_SCHEMA_VERSION = "v0.1"
V551J_SEMANTIC_DIFF_COMPILER_VERSION = "v551j_semantic_diff_0.1"

EXPECTED_V551J_TABLES = {
    "candidate_trace": "packets/v551j_packet_candidate_trace",
    "review_surface": "packets/v551j_packet_review_surface",
    "certified_packet_index": "packets/v551j_certified_packet_index",
    "reviewable_sidecar": "packets/v551j_reviewable_evidence_sidecar",
    "exclusion_audit": "audits/v551j_packet_exclusion_audit",
    "join_key_diagnostics": "audits/v551j_join_key_diagnostics",
    "forbidden_inference_audit": "audits/v551j_forbidden_inference_audit",
    "review_surface_exclusion_audit": "audits/v551j_review_surface_exclusion_audit",
    "v552_context_join_audit": "audits/v551j_v552_context_join_audit",
    "certification_audit": "audits/v551j_certification_audit",
    "certification_rejection_audit": "audits/v551j_certification_rejection_audit",
    "readiness_report": "manifest/v551j_packet_readiness_report",
    "review_readiness_report": "manifest/v551j_review_readiness_report",
    "certification_readiness_report": "manifest/v551j_certification_readiness_report",
    "input_provenance_manifest": "manifest/v551j_input_provenance_manifest",
}

PACKET_COMPARE_FIELDS = [
    "packet_type",
    "packet_status",
    "source",
    "wave",
    "canonical_wave",
    "country_code",
    "confidence_tier",
    "support_status",
    "support_gate_status",
    "authority_status",
    "authority_basis",
    "directionality_status",
    "directionality_basis",
    "directionality_coverage_status",
    "meaning_summary_status",
    "meaning_summary_confidence",
    "association_context_status",
    "association_publication_status",
    "association_lane",
    "association_lane_status",
    "association_lane_authority_source",
    "association_lane_publishability",
    "evidence_stratum",
    "evidence_stratum_v2",
    "runtime_use_class",
    "review_required",
    "known_absences_json",
    "forbidden_claim_ids_json",
    "diagnostic_only_reason",
    "blocked_reason",
    "v552_structural_refs_json",
    "v552_context_status",
    "v552_question_semantic_hierarchy_join_status",
    "v552_contradiction_context_status",
    "v552_parent_prior_context_status",
]

AUTHORITY_FIELDS = [
    "authority_status",
    "authority_basis",
    "authority_source_fields_json",
    "association_lane_authority_source",
    "association_lane_publishability",
    "v552_context_status",
    "v552_question_semantic_hierarchy_join_status",
    "v552_contradiction_context_status",
    "v552_parent_prior_context_status",
]

AFFORDANCE_FIELDS = [
    "runtime_use_class",
    "future_target_affordances_json",
    "allowed_future_targets_json",
    "forbidden_future_targets_json",
    "person_level_allowed",
    "household_level_allowed",
    "carrier_level_allowed",
    "structural_level_only",
    "temporal_level_allowed",
    "requires_temporalization",
    "requires_household_mediation",
    "requires_carrier_mediation",
    "requires_orientation_resolution",
    "requires_pressureflow_mediation",
    "requires_enneagram_runtime",
]

KNOWN_ABSENCE_FIELDS = [
    "known_absences_json",
    "forbidden_claim_ids_json",
    "diagnostic_only_reason",
    "blocked_reason",
    "v552_structural_refs_json",
]

IDENTITY_FIELDS = [
    "packet_id",
    "source",
    "wave",
    "canonical_wave",
    "country_code",
    "source_artifact_ids_json",
]


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


def _json_array(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [_clean(item) for item in value if _clean(item)]
    if isinstance(value, (tuple, set)):
        return [_clean(item) for item in value if _clean(item)]
    text = _clean(value)
    if not text:
        return []
    try:
        parsed = json.loads(text)
    except Exception:
        return [part.strip() for part in text.split("|") if part.strip()]
    if isinstance(parsed, list):
        return [_clean(item) for item in parsed if _clean(item)]
    if parsed in {"", None}:
        return []
    return [_clean(parsed)]


def _normalize_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    if isinstance(value, (list, tuple, set, dict)):
        return json.dumps(value, sort_keys=True, ensure_ascii=False, default=str)
    return _clean(value)


def _normalize_for_compare(value: Any) -> str:
    if isinstance(value, (list, tuple, set, dict)):
        return json.dumps(value, sort_keys=True, ensure_ascii=False, default=str)
    text = _clean(value)
    if not text:
        return ""
    try:
        parsed = json.loads(text)
    except Exception:
        return text
    if isinstance(parsed, list):
        return json.dumps(sorted(_clean(item) for item in parsed if _clean(item)), sort_keys=True, ensure_ascii=False)
    if isinstance(parsed, dict):
        return json.dumps(parsed, sort_keys=True, ensure_ascii=False, default=str)
    return _clean(parsed)


def _first_existing_table_path(run_root: Path, rel_base: str) -> Path | None:
    base = run_root / rel_base
    for candidate in (
        base.with_suffix(".parquet"),
        base.with_suffix(".csv"),
        base.with_suffix(".json"),
    ):
        if candidate.exists():
            return candidate
    return None


def _read_table(path: Path | None) -> pd.DataFrame:
    if path is None or not path.exists():
        return pd.DataFrame()
    if path.suffix.lower() == ".parquet":
        try:
            return pd.read_parquet(path)
        except Exception:
            return pd.DataFrame()
    if path.suffix.lower() == ".csv":
        try:
            return pd.read_csv(path, low_memory=False)
        except EmptyDataError:
            return pd.DataFrame()
        except Exception:
            return pd.DataFrame()
    if path.suffix.lower() == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            return pd.DataFrame(payload)
        if isinstance(payload, dict):
            return pd.DataFrame([payload])
    return pd.DataFrame()


def _frame_to_rows(frame: pd.DataFrame) -> dict[str, dict[str, Any]]:
    if frame.empty or "packet_id" not in frame.columns:
        return {}
    rows: dict[str, dict[str, Any]] = {}
    for row in frame.to_dict(orient="records"):
        packet_id = _clean(row.get("packet_id"))
        if packet_id:
            rows[packet_id] = row
    return rows


def _diff_fields(left_row: dict[str, Any] | None, right_row: dict[str, Any] | None, fields: Iterable[str]) -> list[str]:
    changed: list[str] = []
    left_row = left_row or {}
    right_row = right_row or {}
    for field in fields:
        left_value = _normalize_for_compare(left_row.get(field))
        right_value = _normalize_for_compare(right_row.get(field))
        if left_value != right_value:
            changed.append(field)
    return changed


def _pack_table_rows(
    *,
    comparison_id: str,
    left_bundle: dict[str, Any],
    right_bundle: dict[str, Any],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    left_rows = _frame_to_rows(left_bundle["candidate_trace"])
    right_rows = _frame_to_rows(right_bundle["candidate_trace"])
    packet_ids = sorted(set(left_rows) | set(right_rows))

    packet_diff_rows: list[dict[str, Any]] = []
    authority_diff_rows: list[dict[str, Any]] = []
    affordance_diff_rows: list[dict[str, Any]] = []
    known_absence_diff_rows: list[dict[str, Any]] = []

    for packet_id in packet_ids:
        left_row = left_rows.get(packet_id)
        right_row = right_rows.get(packet_id)
        presence = "shared"
        if left_row is None:
            presence = "right_only"
        elif right_row is None:
            presence = "left_only"

        changed_fields = _diff_fields(left_row, right_row, PACKET_COMPARE_FIELDS + IDENTITY_FIELDS)
        left_packet_type = _clean((left_row or {}).get("packet_type"))
        right_packet_type = _clean((right_row or {}).get("packet_type"))
        left_support = _clean((left_row or {}).get("support_status"))
        right_support = _clean((right_row or {}).get("support_status"))
        left_confidence = _clean((left_row or {}).get("confidence_tier"))
        right_confidence = _clean((right_row or {}).get("confidence_tier"))
        left_absence = _json_array((left_row or {}).get("known_absences_json"))
        right_absence = _json_array((right_row or {}).get("known_absences_json"))
        diff_class = "identical" if not changed_fields and presence == "shared" else "structural_gap" if presence != "shared" else "semantic_diff"
        diff_summary = "no change" if diff_class == "identical" else ", ".join(changed_fields[:6]) or presence
        packet_diff_rows.append(
            {
                "comparison_id": comparison_id,
                "left_run_id": left_bundle["run_id"],
                "right_run_id": right_bundle["run_id"],
                "left_wave": left_bundle.get("wave", ""),
                "right_wave": right_bundle.get("wave", ""),
                "left_run_root": left_bundle["run_root"],
                "right_run_root": right_bundle["run_root"],
                "packet_id": packet_id,
                "packet_type_left": left_packet_type,
                "packet_type_right": right_packet_type,
                "packet_presence_status": presence,
                "diff_class": diff_class,
                "changed_fields_json": json.dumps(changed_fields, sort_keys=True),
                "diff_summary": diff_summary,
                "left_support_status": left_support,
                "right_support_status": right_support,
                "left_confidence_tier": left_confidence,
                "right_confidence_tier": right_confidence,
                "left_authority_status": _clean((left_row or {}).get("authority_status")),
                "right_authority_status": _clean((right_row or {}).get("authority_status")),
                "left_directionality_status": _clean((left_row or {}).get("directionality_status")),
                "right_directionality_status": _clean((right_row or {}).get("directionality_status")),
                "left_evidence_stratum": _clean((left_row or {}).get("evidence_stratum")),
                "right_evidence_stratum": _clean((right_row or {}).get("evidence_stratum")),
                "left_known_absences_json": json.dumps(left_absence, ensure_ascii=False),
                "right_known_absences_json": json.dumps(right_absence, ensure_ascii=False),
                "created_at": utc_now(),
                "schema_version": V551J_SEMANTIC_DIFF_SCHEMA_VERSION,
            }
        )
        if changed_fields and any(field in AUTHORITY_FIELDS for field in changed_fields):
            authority_diff_rows.append(
                {
                    "comparison_id": comparison_id,
                    "left_run_id": left_bundle["run_id"],
                    "right_run_id": right_bundle["run_id"],
                    "packet_id": packet_id,
                    "packet_presence_status": presence,
                    "authority_diff_fields_json": json.dumps([field for field in changed_fields if field in AUTHORITY_FIELDS], sort_keys=True),
                    "left_authority_status": _clean((left_row or {}).get("authority_status")),
                    "right_authority_status": _clean((right_row or {}).get("authority_status")),
                    "left_authority_basis": _clean((left_row or {}).get("authority_basis")),
                    "right_authority_basis": _clean((right_row or {}).get("authority_basis")),
                    "left_authority_source_fields_json": _normalize_scalar((left_row or {}).get("authority_source_fields_json")),
                    "right_authority_source_fields_json": _normalize_scalar((right_row or {}).get("authority_source_fields_json")),
                    "authority_diff_reason": "authority or context selection changed",
                    "created_at": utc_now(),
                    "schema_version": V551J_SEMANTIC_DIFF_SCHEMA_VERSION,
                }
            )
        if changed_fields and any(field in AFFORDANCE_FIELDS for field in changed_fields):
            affordance_diff_rows.append(
                {
                    "comparison_id": comparison_id,
                    "left_run_id": left_bundle["run_id"],
                    "right_run_id": right_bundle["run_id"],
                    "packet_id": packet_id,
                    "packet_presence_status": presence,
                    "affordance_diff_fields_json": json.dumps([field for field in changed_fields if field in AFFORDANCE_FIELDS], sort_keys=True),
                    "left_runtime_use_class": _clean((left_row or {}).get("runtime_use_class")),
                    "right_runtime_use_class": _clean((right_row or {}).get("runtime_use_class")),
                    "left_person_level_allowed": bool((left_row or {}).get("person_level_allowed", False)),
                    "right_person_level_allowed": bool((right_row or {}).get("person_level_allowed", False)),
                    "left_household_level_allowed": bool((left_row or {}).get("household_level_allowed", False)),
                    "right_household_level_allowed": bool((right_row or {}).get("household_level_allowed", False)),
                    "left_carrier_level_allowed": bool((left_row or {}).get("carrier_level_allowed", False)),
                    "right_carrier_level_allowed": bool((right_row or {}).get("carrier_level_allowed", False)),
                    "left_structural_level_only": bool((left_row or {}).get("structural_level_only", False)),
                    "right_structural_level_only": bool((right_row or {}).get("structural_level_only", False)),
                    "affordance_diff_reason": "runtime-use or permission boundary changed",
                    "created_at": utc_now(),
                    "schema_version": V551J_SEMANTIC_DIFF_SCHEMA_VERSION,
                }
            )
        if changed_fields and any(field in KNOWN_ABSENCE_FIELDS for field in changed_fields):
            known_absence_diff_rows.append(
                {
                    "comparison_id": comparison_id,
                    "left_run_id": left_bundle["run_id"],
                    "right_run_id": right_bundle["run_id"],
                    "packet_id": packet_id,
                    "packet_presence_status": presence,
                    "known_absence_diff_fields_json": json.dumps([field for field in changed_fields if field in KNOWN_ABSENCE_FIELDS], sort_keys=True),
                    "left_known_absences_json": json.dumps(left_absence, ensure_ascii=False),
                    "right_known_absences_json": json.dumps(right_absence, ensure_ascii=False),
                    "left_blocked_reason": _clean((left_row or {}).get("blocked_reason")),
                    "right_blocked_reason": _clean((right_row or {}).get("blocked_reason")),
                    "left_diagnostic_only_reason": _clean((left_row or {}).get("diagnostic_only_reason")),
                    "right_diagnostic_only_reason": _clean((right_row or {}).get("diagnostic_only_reason")),
                    "known_absence_diff_reason": "absence register changed",
                    "created_at": utc_now(),
                    "schema_version": V551J_SEMANTIC_DIFF_SCHEMA_VERSION,
                }
            )

    packet_df = pd.DataFrame(packet_diff_rows)
    authority_df = pd.DataFrame(authority_diff_rows)
    affordance_df = pd.DataFrame(affordance_diff_rows)
    absence_df = pd.DataFrame(known_absence_diff_rows)
    return packet_df, authority_df, affordance_df, absence_df


def _bundle_status(bundle: dict[str, Any]) -> str:
    if bundle["candidate_trace"].empty:
        return "missing_candidate_trace"
    if bundle["packet_count"] == 0:
        return "empty_candidate_trace"
    return "ready"


def _load_bundle(run_root: str | Path) -> dict[str, Any]:
    root = Path(run_root)
    tables: dict[str, pd.DataFrame] = {}
    table_paths: dict[str, str] = {}
    for name, rel_base in EXPECTED_V551J_TABLES.items():
        path = _first_existing_table_path(root, rel_base)
        table_paths[name] = str(path) if path else ""
        tables[name] = _read_table(path)

    bundle = {
        "run_root": str(root),
        "run_id": root.name,
        "table_paths": table_paths,
        "candidate_trace": tables["candidate_trace"],
        "review_surface": tables["review_surface"],
        "certified_packet_index": tables["certified_packet_index"],
        "reviewable_sidecar": tables["reviewable_sidecar"],
        "readiness_report": tables["readiness_report"],
        "review_readiness_report": tables["review_readiness_report"],
        "certification_readiness_report": tables["certification_readiness_report"],
        "input_provenance_manifest": tables["input_provenance_manifest"],
        "packet_count": int(len(tables["candidate_trace"])),
        "review_count": int(len(tables["review_surface"])),
        "certified_count": int(len(tables["certified_packet_index"])),
        "sidecar_count": int(len(tables["reviewable_sidecar"])),
        "wave": _clean(
            tables["candidate_trace"].iloc[0].get("wave")
            if not tables["candidate_trace"].empty and "wave" in tables["candidate_trace"].columns
            else (tables["readiness_report"].iloc[0].get("wave") if not tables["readiness_report"].empty and "wave" in tables["readiness_report"].columns else "")
        ),
        "readiness_status": _clean(tables["readiness_report"].iloc[0].get("final_status") if not tables["readiness_report"].empty else ""),
        "review_readiness_status": _clean(tables["review_readiness_report"].iloc[0].get("final_status") if not tables["review_readiness_report"].empty else ""),
        "certification_readiness_status": _clean(tables["certification_readiness_report"].iloc[0].get("final_status") if not tables["certification_readiness_report"].empty else ""),
        "input_status": "ready" if tables["candidate_trace"].shape[0] else "missing_candidate_trace",
        "created_at": utc_now(),
    }
    bundle["status"] = _bundle_status(bundle)
    return bundle


def build_v551j_cross_wave_semantic_diff(
    *,
    comparison_id: str,
    left_run_root: str | Path,
    right_run_root: str | Path,
) -> dict[str, Any]:
    left_bundle = _load_bundle(left_run_root)
    right_bundle = _load_bundle(right_run_root)
    packet_df, authority_df, affordance_df, absence_df = _pack_table_rows(
        comparison_id=comparison_id,
        left_bundle=left_bundle,
        right_bundle=right_bundle,
    )

    packet_change_count = int((packet_df.get("diff_class", pd.Series(dtype="object")).astype(str) != "identical").sum()) if not packet_df.empty else 0
    packet_presence_counts: dict[str, int] = {}
    if not packet_df.empty and "packet_presence_status" in packet_df.columns:
        packet_presence_counts = {
            key: int(count)
            for key, count in packet_df["packet_presence_status"].astype(str).value_counts().to_dict().items()
        }
    diff_field_counter: dict[str, int] = {}
    if not packet_df.empty and "changed_fields_json" in packet_df.columns:
        for text in packet_df["changed_fields_json"].astype(str):
            try:
                fields = json.loads(text)
            except Exception:
                fields = []
            for field in fields:
                diff_field_counter[field] = diff_field_counter.get(field, 0) + 1

    comparability_status = "READY_V551J_CROSS_WAVE_DIFF"
    if left_bundle["status"] != "ready" or right_bundle["status"] != "ready":
        comparability_status = "READY_V551J_CROSS_WAVE_DIFF_WITH_INPUT_GAPS"

    readiness_summary = {
        "comparison_id": comparison_id,
        "left_run_id": left_bundle["run_id"],
        "right_run_id": right_bundle["run_id"],
        "left_run_root": left_bundle["run_root"],
        "right_run_root": right_bundle["run_root"],
        "status": comparability_status,
        "implementation_kind": "reviewable",
        "provisionality": "provisional",
        "scaffold_level": "cross_wave_semantic_diff",
        "continuity_checked_full": False,
        "upstream_continuity_scope": "candidate_trace_and_review_surface_presence",
        "upstream_continuity_result": "pass" if left_bundle["status"] == "ready" and right_bundle["status"] == "ready" else "partial",
        "downstream_continuity_scope": "not_checked_in_v551j_d",
        "downstream_continuity_result": "not_checked",
        "full_upstream_and_downstream_continuity_checked": False,
        "packet_count_left": left_bundle["packet_count"],
        "packet_count_right": right_bundle["packet_count"],
        "review_count_left": left_bundle["review_count"],
        "review_count_right": right_bundle["review_count"],
        "certified_count_left": left_bundle["certified_count"],
        "certified_count_right": right_bundle["certified_count"],
        "sidecar_count_left": left_bundle["sidecar_count"],
        "sidecar_count_right": right_bundle["sidecar_count"],
        "packet_diff_rows": int(len(packet_df)),
        "authority_diff_rows": int(len(authority_df)),
        "affordance_diff_rows": int(len(affordance_df)),
        "known_absence_diff_rows": int(len(absence_df)),
        "packet_change_count": packet_change_count,
        "packet_presence_counts_json": json.dumps(packet_presence_counts, sort_keys=True),
        "top_changed_fields_json": json.dumps(
            dict(sorted(diff_field_counter.items(), key=lambda item: (-item[1], item[0]))[:20]),
            sort_keys=True,
        ),
        "created_at": utc_now(),
        "schema_version": V551J_SEMANTIC_DIFF_SCHEMA_VERSION,
        "compiler_version": V551J_SEMANTIC_DIFF_COMPILER_VERSION,
        "left_status": left_bundle["status"],
        "right_status": right_bundle["status"],
    }

    comparability_report = {
        "comparison_id": comparison_id,
        "status": comparability_status,
        "left": {
            "run_id": left_bundle["run_id"],
            "run_root": left_bundle["run_root"],
            "status": left_bundle["status"],
            "candidate_trace_rows": left_bundle["packet_count"],
            "review_surface_rows": left_bundle["review_count"],
            "certified_rows": left_bundle["certified_count"],
            "sidecar_rows": left_bundle["sidecar_count"],
            "table_paths": left_bundle["table_paths"],
        },
        "right": {
            "run_id": right_bundle["run_id"],
            "run_root": right_bundle["run_root"],
            "status": right_bundle["status"],
            "candidate_trace_rows": right_bundle["packet_count"],
            "review_surface_rows": right_bundle["review_count"],
            "certified_rows": right_bundle["certified_count"],
            "sidecar_rows": right_bundle["sidecar_count"],
            "table_paths": right_bundle["table_paths"],
        },
        "packet_diff_rows": int(len(packet_df)),
        "authority_diff_rows": int(len(authority_df)),
        "affordance_diff_rows": int(len(affordance_df)),
        "known_absence_diff_rows": int(len(absence_df)),
        "packet_presence_counts": packet_presence_counts,
        "top_changed_fields": dict(sorted(diff_field_counter.items(), key=lambda item: (-item[1], item[0]))[:20]),
        "created_at": utc_now(),
        "schema_version": V551J_SEMANTIC_DIFF_SCHEMA_VERSION,
    }

    return {
        "comparison_id": comparison_id,
        "left_bundle": left_bundle,
        "right_bundle": right_bundle,
        "packet_diff": packet_df,
        "authority_diff": authority_df,
        "affordance_diff": affordance_df,
        "known_absence_diff": absence_df,
        "readiness_summary": readiness_summary,
        "comparability_report": comparability_report,
    }


def validate_v551j_cross_wave_semantic_diff(summary: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not summary.get("comparison_id"):
        errors.append("missing comparison_id")
    if summary.get("packet_diff") is None or summary.get("authority_diff") is None:
        errors.append("missing diff tables")
    if summary.get("readiness_summary", {}).get("status") not in {
        "READY_V551J_CROSS_WAVE_DIFF",
        "READY_V551J_CROSS_WAVE_DIFF_WITH_INPUT_GAPS",
    }:
        errors.append("unexpected readiness status")
    if summary.get("readiness_summary", {}).get("full_upstream_and_downstream_continuity_checked"):
        errors.append("full continuity cannot be claimed in provisional cross-wave diff")
    return errors


__all__ = [
    "V551J_SEMANTIC_DIFF_SCHEMA_VERSION",
    "V551J_SEMANTIC_DIFF_COMPILER_VERSION",
    "build_v551j_cross_wave_semantic_diff",
    "validate_v551j_cross_wave_semantic_diff",
]
