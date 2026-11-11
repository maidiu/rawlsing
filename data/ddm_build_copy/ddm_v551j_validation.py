#!/usr/bin/env python3
"""Validation helpers for V551J candidate packets."""

from __future__ import annotations

import json
import hashlib
import re
from pathlib import Path
from typing import Iterable

import pandas as pd

from data.ddm_build_copy.ddm_v551j_schema import (
    V551J_AUTHORITY_STATUSES,
    V551J_CERTIFICATION_AUDIT_SCHEMA,
    V551J_CERTIFICATION_READINESS_REPORT_SCHEMA,
    V551J_CERTIFICATION_REJECTION_AUDIT_SCHEMA,
    V551J_CERTIFIED_PACKET_INDEX_SCHEMA,
    V551J_DIRECTIONALITY_STATUSES,
    V551J_FORBIDDEN_CLAIM_IDS,
    V551J_PACKET_CANDIDATE_TRACE_SCHEMA,
    V551J_PACKET_STATUSES,
    V551J_REVIEW_PRIORITIES,
    V551J_REVIEW_SURFACE_SCHEMA,
    V551J_REVIEW_SURFACE_STATUSES,
    V551J_REVIEWABLE_EVIDENCE_SIDECAR_SCHEMA,
    V551J_EVIDENCE_QUALITY_STATUSES,
    V551J_USE_PERMISSION_CLASSES,
    V551J_RUNTIME_USE_CLASSES,
)
from data.ddm_build_copy.ddm_v551j_contract import (
    bool_value,
    recompute_joint_component_measurement_signature,
    recompute_joint_empirical_distribution_signature,
    recompute_joint_measurement_contract_hash,
    recompute_joint_orientation_signature,
    recompute_joint_response_identity_signature,
    recompute_joint_semantic_signature,
    recompute_joint_structural_signature,
    recompute_joint_target_signature,
    recompute_joint_topology_signature,
    recompute_required_component_comparisons,
    recompute_v551j_component_contract_hash,
    recompute_v551j_component_id,
    recompute_v551j_packet_id,
    recompute_v551j_v2_2_3_packet_contract_hash,
)


def validate_v551j_v2_2_3_outputs(
    *,
    candidate: pd.DataFrame,
    certified: pd.DataFrame,
    review_surface: pd.DataFrame,
    certification_audit: pd.DataFrame,
    component: pd.DataFrame,
    expected_registry_hash: str = "",
    execution_mode: str = "acceptance",
) -> list[str]:
    candidate = candidate.copy()
    certified = certified.copy()
    review_surface = review_surface.copy()
    certification_audit = certification_audit.copy()
    component = component.copy()
    issues: list[str] = []
    hash_re = re.compile(r"^[0-9a-f]{64}$")
    if execution_mode not in {"acceptance", "diagnostic", "strict_blocked"}:
        issues.append("invalid_execution_mode")

    def _truthy(series: pd.Series) -> pd.Series:
        return series.fillna(False).astype(str).str.lower().isin({"true", "1", "yes", "y"})

    def _json_list(value: object) -> list[object]:
        try:
            parsed = json.loads(value) if isinstance(value, str) and value.strip() else []
        except Exception:
            return ["__INVALID_JSON__"]
        return parsed if isinstance(parsed, list) else ["__NOT_LIST__"]

    required_candidate = [
        "packet_id",
        "packet_contract_hash",
        "pattern_item_count",
        "component_contract_hashes_ordered_json",
        "matched_atom_ids_json",
        "matched_atom_contract_hashes_json",
        "component_empirical_distribution_ids_ordered_json",
        "component_question_denominators_ordered_json",
        "component_order_integrity_status",
        "denominator_separation_status",
        "certification_status",
        "ready_for_v552j_joint_evidence",
        "ready_for_v552j_component_linkage",
        "ready_for_v553",
        "pressure_anchor_eligible",
        "temporal_pressure_authorized",
        "runtime_use_class",
        "allowed_future_targets_json",
        "v551_input_artifact_hash",
        "v550j_pattern_index_artifact_hash",
        "v550j_pattern_item_index_artifact_hash",
        "v550j_relation_signature_artifact_hash",
        "v550j_manifest_hash",
        "v550j_readiness_report_hash",
        "question_family_registry_hash",
    ]
    for column in required_candidate:
        if column not in candidate.columns:
            issues.append(f"missing_candidate_column:{column}")
    required_component = [
        "packet_id",
        "component_id",
        "component_contract_hash",
        "item_order",
        "v551_atom_match_status",
        "v551_atom_contract_hash",
        "v551_empirical_distribution_id",
        "v551_n_respondents",
        "question_identity_status",
        "var_code_status",
        "response_identity_status",
        "normalized_response_label_status",
        "semantic_response_role_status",
        "response_direction_status",
        "response_intensity_status",
        "semantic_polarity_status",
        "response_semantics_hash_status",
        "driver_facet_id_status",
        "relation_axis_id_status",
        "target_layer_relation_status",
        "cross_contract_status",
    ]
    for column in required_component:
        if column not in component.columns:
            issues.append(f"missing_component_column:{column}")
    if issues:
        return issues

    certified_candidates = candidate[candidate.get("certification_status", pd.Series(dtype=str)).astype(str).str.startswith("CERTIFIED")]
    review_candidates = candidate[candidate.get("certification_status", pd.Series(dtype=str)).astype(str).eq("REVIEW_REQUIRED_COMPONENT_GAP")]
    blocked_candidates = candidate[candidate.get("certification_status", pd.Series(dtype=str)).astype(str).str.startswith("BLOCKED")]
    if len(candidate) != len(certified_candidates) + len(review_candidates) + len(blocked_candidates):
        issues.append("candidate_partition_mismatch")
    if execution_mode == "diagnostic":
        if len(certified) != 0:
            issues.append("certified_subset_mismatch")
    elif len(certified) != len(certified_candidates):
        issues.append("certified_subset_mismatch")
    if len(review_surface) != len(review_candidates):
        issues.append("review_surface_mismatch")
    expected_audit_certified = 0 if execution_mode in {"diagnostic", "strict_blocked"} else len(certified)
    if not certification_audit.empty and int(_truthy(certification_audit.get("certified", pd.Series(dtype=bool))).sum()) != expected_audit_certified:
        issues.append("certification_audit_certified_mismatch")
    noncert = candidate[~candidate.get("certification_status", pd.Series(dtype=str)).astype(str).str.startswith("CERTIFIED")]
    if not noncert.empty and _truthy(noncert.get("ready_for_v552j_joint_evidence", pd.Series(dtype=bool))).any():
        issues.append("noncertified_v552j_permission")
    if not noncert.empty and _truthy(noncert.get("ready_for_v552j_component_linkage", pd.Series(dtype=bool))).any():
        issues.append("noncertified_v552j_permission")
    if execution_mode == "diagnostic":
        if _truthy(candidate.get("ready_for_v552j_joint_evidence", pd.Series(dtype=bool))).any() or _truthy(candidate.get("ready_for_v552j_component_linkage", pd.Series(dtype=bool))).any():
            issues.append("diagnostic_downstream_permission_present")
    elif not certified.empty and not _truthy(certified.get("ready_for_v552j_joint_evidence", pd.Series(dtype=bool))).all():
        issues.append("certified_missing_v552j_permission")
    if execution_mode != "diagnostic" and not certified.empty and not _truthy(certified.get("ready_for_v552j_component_linkage", pd.Series(dtype=bool))).all():
        issues.append("certified_missing_v552j_permission")
    if _truthy(candidate.get("ready_for_v553", pd.Series(dtype=bool))).any():
        issues.append("direct_v553_authorization")
    if _truthy(candidate.get("pressure_anchor_eligible", pd.Series(dtype=bool))).any():
        issues.append("pressure_anchor_authorization")
    if _truthy(candidate.get("temporal_pressure_authorized", pd.Series(dtype=bool))).any():
        issues.append("temporal_authorization")
    if not candidate["runtime_use_class"].fillna("").astype(str).eq("not_runtime_consumable").all():
        issues.append("runtime_authorization")
    bad_allowed = []
    for idx, value in enumerate(candidate["allowed_future_targets_json"].tolist()):
        allowed = _json_list(value)
        ready = bool_value(candidate.iloc[idx].get("ready_for_v552j_joint_evidence"))
        if ready and allowed != ["v552j"]:
            bad_allowed.append(idx)
        if not ready and allowed != []:
            bad_allowed.append(idx)
    if bad_allowed:
        issues.append(f"allowed_future_targets_mismatch:{len(bad_allowed)}")
    observed_registry = set(candidate["question_family_registry_hash"].fillna("").astype(str))
    if expected_registry_hash:
        if observed_registry != {expected_registry_hash}:
            issues.append("registry_hash_mismatch")
    elif len(observed_registry) != 1:
        issues.append("registry_hash_mismatch")

    allowed_component_statuses = {
        "EXACT_MATCH",
        "BOTH_MISSING",
        "ONE_SIDE_MISSING",
        "NOT_COMPARABLE_PARALLEL_CONTRACT",
        "CONFLICT",
        "PARALLEL_SOURCE_COORDINATE_PRESERVED",
        "SOURCE_COORDINATE_MISSING",
        "PARALLEL_GOVERNED_TARGET_LAYERS",
        "FAMILY_TARGET_CONTRACT_GAP",
        "STRUCTURAL_TARGET_CONTRACT_GAP",
        "CROSS_CONTRACT_CONSISTENT",
        "CROSS_CONTRACT_GAP",
        "CROSS_CONTRACT_RESPONSE_CONFLICT",
        "CROSS_CONTRACT_AUTHORITY_HASH_CONFLICT",
        "CROSS_CONTRACT_DIRECTIONALITY_CONFLICT",
        "CROSS_CONTRACT_SOURCE_INTENSITY_CONFLICT",
        "CROSS_CONTRACT_SHARED_STRUCTURAL_CONFLICT",
    }
    for column in [
        "question_identity_status",
        "var_code_status",
        "response_identity_status",
        "normalized_response_label_status",
        "semantic_response_role_status",
        "response_direction_status",
        "response_intensity_status",
        "semantic_polarity_status",
        "source_polarity_representation_status",
        "response_semantics_hash_status",
        "driver_facet_id_status",
        "relation_axis_id_status",
        "target_layer_relation_status",
        "cross_contract_status",
    ]:
        if column in component.columns:
            bad = sorted(set(component[column].fillna("").astype(str)) - allowed_component_statuses)
            if bad:
                issues.append(f"invalid_component_status:{column}:{bad[:5]}")
    if component["cross_contract_status"].astype(str).eq("CROSS_CONTRACT_GAP").any():
        issues.append("unexpected_cross_contract_gap")
    if component["v551_atom_match_status"].astype(str).eq("AMBIGUOUS_V551_ATOM_MATCH").any():
        issues.append("ambiguous_v551_atom_match")
    if component["v551_empirical_distribution_id"].fillna("").astype(str).eq("").any():
        issues.append("missing_empirical_distribution_id")
    denominators = pd.to_numeric(component["v551_n_respondents"], errors="coerce")
    if denominators.isna().any() or (denominators <= 0).any():
        issues.append("invalid_component_denominator")
    if not candidate["component_order_integrity_status"].astype(str).eq("PASS").all():
        issues.append("duplicate_item_order")
    if not candidate["denominator_separation_status"].astype(str).eq("PASS").all():
        issues.append("denominator_separation_failure")

    for packet_id, rows in component.groupby("packet_id", sort=False):
        if rows["item_order"].duplicated().any():
            issues.append("duplicate_item_order")
        parent = candidate[candidate["packet_id"].astype(str).eq(str(packet_id))]
        if len(parent) != 1:
            issues.append("component_item_cardinality_mismatch")
            continue
        expected_count = int(parent.iloc[0].get("pattern_item_count") or -1)
        if expected_count != len(rows):
            issues.append("component_item_cardinality_mismatch")
        for column, json_column in [
            ("component_id", "component_ids_ordered_json"),
            ("component_contract_hash", "component_contract_hashes_ordered_json"),
            ("v551_atom_id", "matched_atom_ids_json"),
            ("v551_atom_contract_hash", "matched_atom_contract_hashes_json"),
            ("v551_measurement_contract_hash", "component_measurement_contract_hashes_ordered_json"),
            ("v551_empirical_object_id", "component_empirical_object_ids_ordered_json"),
            ("v551_empirical_distribution_id", "component_empirical_distribution_ids_ordered_json"),
            ("v551_n_respondents", "component_question_denominators_ordered_json"),
            ("component_v552_linkage_class", "component_v552_linkage_classes_ordered_json"),
        ]:
            if json_column not in parent.columns:
                if json_column in {"component_ids_ordered_json", "component_v552_linkage_classes_ordered_json"}:
                    continue
                issues.append("ordered_array_cardinality_mismatch")
                continue
            expected = [_stringify_value(x) for x in rows.sort_values("item_order", kind="mergesort")[column].tolist()]
            actual = [_stringify_value(x) for x in _json_list(parent.iloc[0].get(json_column))]
            if expected != actual:
                issues.append("ordered_array_cardinality_mismatch")
    if execution_mode == "diagnostic":
        if len(certified) != 0:
            issues.append("certified_subset_identity_mismatch")
    elif set(certified["packet_id"].astype(str)) != set(certified_candidates["packet_id"].astype(str)):
        issues.append("certified_subset_identity_mismatch")
    if set(review_surface["packet_id"].astype(str)) != set(review_candidates["packet_id"].astype(str)):
        issues.append("review_surface_identity_mismatch")
        issues.append("review_surface_coverage_mismatch")

    if not certified.empty:
        shared = [column for column in certified.columns if column in certified_candidates.columns]
        left = certified[shared].sort_values("packet_id", kind="mergesort").reset_index(drop=True).fillna("").astype(str)
        right = certified_candidates[shared].sort_values("packet_id", kind="mergesort").reset_index(drop=True).fillna("").astype(str)
        if left.shape != right.shape or not left.equals(right):
            issues.append("certified_projection_mismatch")
    if not review_surface.empty:
        shared = [column for column in review_surface.columns if column in review_candidates.columns]
        left = review_surface[shared].sort_values("packet_id", kind="mergesort").reset_index(drop=True).fillna("").astype(str)
        right = review_candidates[shared].sort_values("packet_id", kind="mergesort").reset_index(drop=True).fillna("").astype(str)
        if left.shape != right.shape or not left.equals(right):
            issues.append("review_surface_projection_mismatch")

    if certification_audit.empty and not candidate.empty:
        issues.append("certification_audit_coverage_mismatch")
    elif not certification_audit.empty:
        audit_ids = certification_audit["packet_id"].fillna("").astype(str)
        candidate_ids = candidate["packet_id"].fillna("").astype(str)
        if audit_ids.duplicated().any() or set(audit_ids) != set(candidate_ids):
            issues.append("certification_audit_coverage_mismatch")
        audit_certified = set(certification_audit[_truthy(certification_audit.get("certified", pd.Series(dtype=bool)))]["packet_id"].astype(str))
        candidate_certified = set(certified_candidates["packet_id"].astype(str))
        expected_certified = set() if execution_mode in {"diagnostic", "strict_blocked"} else candidate_certified
        if audit_certified != expected_certified:
            issues.append("candidate_certification_mismatch")

    for _, row in component.iterrows():
        if "pressure_score" in component.columns:
            issues.append("direct_pressure_field_present")
        if recompute_v551j_component_id(row) != str(row.get("component_id")):
            issues.append("component_id_recomputation_mismatch")
        stored_statuses = {
            "question_identity": str(row.get("question_identity_status") or ""),
            "var_code": str(row.get("var_code_status") or ""),
            "response_identity": str(row.get("response_identity_status") or ""),
            "normalized_response_label": str(row.get("normalized_response_label_status") or ""),
            "stance_direction": str(row.get("joint_response_stance_alignment_status") or ""),
            "response_semantics_hash": str(row.get("response_semantics_hash_status") or ""),
            "driver_id": str(row.get("driver_id_status") or ""),
            "driver_facet": str(row.get("driver_facet_id_status") or ""),
            "relation_axis": str(row.get("relation_axis_id_status") or ""),
        }
        recomputed_comparisons = recompute_required_component_comparisons(row)
        for field_name, actual_status in recomputed_comparisons.items():
            stored_status = stored_statuses.get(field_name, "")
            stored_exact = stored_status in {"EXACT_MATCH", "EXACT_GOVERNED_ALIGNMENT"}
            if actual_status == "CONFLICT":
                if stored_status == "CONFLICT":
                    issues.append("cross_contract_semantic_conflict")
                else:
                    issues.append("comparison_status_inconsistent_with_values")
            elif actual_status == "EXACT_MATCH" and not stored_exact:
                issues.append("comparison_status_inconsistent_with_values")
            elif actual_status in {"BOTH_MISSING", "ONE_SIDE_MISSING"} and stored_status not in {actual_status, "NOT_COMPARABLE_PARALLEL_CONTRACT"}:
                issues.append("comparison_status_inconsistent_with_values")
        if recompute_v551j_component_contract_hash(row) != str(row.get("component_contract_hash") or ""):
            issues.append("component_contract_hash_mismatch")
        comparison_pairs = [
            ("v550j_item_question_id", "v551_question_id", "question_identity_status"),
            ("v550j_item_var_code", "v551_var_code", "var_code_status"),
            ("v550j_item_response_value_normalized", "v551_response_value_normalized", "response_identity_status"),
            ("v550j_item_normalized_response_label", "v551_normalized_response_label", "normalized_response_label_status"),
            ("v550j_item_response_direction", "v551_response_direction", "response_direction_status"),
            ("v550j_item_response_intensity", "v551_response_intensity", "response_intensity_status"),
            ("v550j_driver_facet_id", "v551_driver_facet_id", "driver_facet_id_status"),
            ("v550j_relation_axis_id", "v551_relation_axis_id", "relation_axis_id_status"),
        ]
        for left_col, right_col, status_col in comparison_pairs:
            left = _stringify_value(row.get(left_col)).casefold()
            right = _stringify_value(row.get(right_col)).casefold()
            status = str(row.get(status_col) or "")
            if left and right and left != right and status == "EXACT_MATCH":
                issues.append("comparison_status_inconsistent_with_values")
            if left and right and left == right and status == "CONFLICT":
                issues.append("comparison_status_inconsistent_with_values")
        stance = str(row.get("v550j_joint_response_stance") or "").strip().lower()
        direction = str(row.get("v551_response_direction") or "").strip().lower()
        expected_direction = {"support": "positive", "oppose": "negative", "neutral": "neutral"}.get(stance)
        if expected_direction and direction and expected_direction != direction:
            issues.append("stance_direction_conflict")
        if str(row.get("v551_evidence_role") or "").strip() != "RELATION_EVIDENCE":
            issues.append("invalid_v551_evidence_role")
        left_hash = str(row.get("v550j_item_response_semantics_contract_hash") or "")
        right_hash = str(row.get("v551_response_semantics_contract_hash") or "")
        if left_hash and right_hash and left_hash != right_hash:
            issues.append("response_semantics_hash_conflict")
        if row.get("cross_contract_status") == "CROSS_CONTRACT_GAP":
            issues.append("unexpected_cross_contract_gap")
        if not _stringify_value(row.get("v551_atom_id")) or not _stringify_value(row.get("v551_empirical_object_id")):
            issues.append("comparison_status_inconsistent_with_values")
    if component["component_id"].duplicated().any():
        issues.append("duplicate_component_id")

    for _, row in candidate.iterrows():
        status = str(row.get("certification_status") or "")
        review_reasons = _json_list(row.get("review_reason_codes_json"))
        blockers = _json_list(row.get("blocking_reason_codes_json"))
        if status == "REVIEW_REQUIRED_COMPONENT_GAP":
            if not bool_value(row.get("review_required")) or review_reasons != ["pattern_support_gate"] or blockers != []:
                issues.append("candidate_status_permission_mismatch")
            if bool_value(row.get("ready_for_v552j_joint_evidence")) or bool_value(row.get("ready_for_v552j_component_linkage")):
                issues.append("candidate_status_permission_mismatch")
        if status == "CERTIFIED_JOINT_RELATION_EVIDENCE":
            if bool_value(row.get("review_required")) or review_reasons != [] or blockers != []:
                issues.append("candidate_status_permission_mismatch")
            if execution_mode != "diagnostic" and (not bool_value(row.get("ready_for_v552j_joint_evidence")) or not bool_value(row.get("ready_for_v552j_component_linkage"))):
                issues.append("candidate_status_permission_mismatch")
        if execution_mode == "strict_blocked":
            if not status.startswith("BLOCKED") or bool_value(row.get("review_required")) or review_reasons != []:
                issues.append("strict_blocked_status_mismatch")
        if recompute_v551j_packet_id(row) != str(row.get("packet_id")):
            issues.append("packet_id_recomputation_mismatch")
        for column in [
            "packet_contract_hash",
            "v551_input_artifact_hash",
            "v550j_pattern_index_artifact_hash",
            "v550j_pattern_item_index_artifact_hash",
            "v550j_relation_signature_artifact_hash",
            "v550j_manifest_hash",
            "v550j_readiness_report_hash",
            "question_family_registry_hash",
        ]:
            value = str(row.get(column) or "")
            if not hash_re.match(value):
                issues.append(f"invalid_hash:{column}")
                break
        packet_components = component[component["packet_id"].astype(str).eq(str(row.get("packet_id")))].sort_values("item_order", kind="mergesort").to_dict("records")
        recomputed = recompute_v551j_v2_2_3_packet_contract_hash(row, packet_components)
        if recomputed != str(row.get("packet_contract_hash")):
            issues.append("packet_contract_hash_mismatch")
        sigs = {
            "joint_response_identity_signature": recompute_joint_response_identity_signature(packet_components),
            "joint_empirical_distribution_signature": recompute_joint_empirical_distribution_signature(packet_components),
            "joint_semantic_signature": recompute_joint_semantic_signature(packet_components),
            "joint_orientation_signature": recompute_joint_orientation_signature(packet_components),
            "joint_topology_signature": recompute_joint_topology_signature(row, packet_components),
            "joint_target_signature": recompute_joint_target_signature(packet_components),
            "joint_structural_signature": recompute_joint_structural_signature(row, packet_components),
            "joint_component_measurement_signature": recompute_joint_component_measurement_signature(packet_components),
        }
        for name, value in sigs.items():
            stored = str(row.get(name) or "")
            if not hash_re.match(stored):
                issues.append("invalid_joint_signature")
            elif stored != value:
                issues.append("joint_signature_recomputation_mismatch")
        if str(row.get("joint_measurement_contract_hash")) != recompute_joint_measurement_contract_hash(row):
            issues.append("joint_measurement_hash_mismatch")
    return list(dict.fromkeys(issues))


def read_v551j_contract_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def validate_written_v551j_artifacts(
    *,
    candidate_path: Path,
    component_path: Path,
    certified_path: Path,
    review_path: Path,
    certification_audit_path: Path,
    expected_registry_hash: str,
    execution_mode: str = "acceptance",
) -> list[str]:
    return validate_v551j_v2_2_3_outputs(
        candidate=read_v551j_contract_csv(candidate_path),
        certified=read_v551j_contract_csv(certified_path),
        review_surface=read_v551j_contract_csv(review_path),
        certification_audit=read_v551j_contract_csv(certification_audit_path),
        component=read_v551j_contract_csv(component_path),
        expected_registry_hash=expected_registry_hash,
        execution_mode=execution_mode,
    )


def _stringify_value(value: object) -> str:
    if pd.isna(value):
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def _canonical_bool(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def validate_required_columns(frame: pd.DataFrame, required_columns: list[str], table_name: str) -> list[str]:
    missing = [column for column in required_columns if column not in frame.columns]
    return [f"{table_name}: missing columns {missing}"] if missing else []


def _column_values(frame: pd.DataFrame, column: str) -> pd.Series:
    if column not in frame.columns:
        return pd.Series(dtype=object)
    return frame[column].fillna("").astype(str).str.strip()


def validate_packet_lifecycle_statuses(frame: pd.DataFrame) -> list[str]:
    if frame.empty or "packet_status" not in frame.columns:
        return []
    bad = sorted(set(value for value in _column_values(frame, "packet_status").tolist() if value and value not in V551J_PACKET_STATUSES))
    return [f"packet_status: invalid values {bad}"] if bad else []


def validate_no_certified_packets_in_phase_a(frame: pd.DataFrame) -> list[str]:
    if frame.empty or "packet_status" not in frame.columns:
        return []
    bad = frame[frame["packet_status"].astype(str).eq("certified")]
    return [f"packet_status: certified rows present {len(bad)}"] if not bad.empty else []


def validate_runtime_use_classes(frame: pd.DataFrame) -> list[str]:
    if frame.empty or "runtime_use_class" not in frame.columns:
        return []
    bad = sorted(set(value for value in _column_values(frame, "runtime_use_class").tolist() if value and value not in V551J_RUNTIME_USE_CLASSES))
    return [f"runtime_use_class: invalid values {bad}"] if bad else []


def validate_authority_statuses(frame: pd.DataFrame) -> list[str]:
    if frame.empty or "authority_status" not in frame.columns:
        return []
    bad = sorted(set(value for value in _column_values(frame, "authority_status").tolist() if value and value not in V551J_AUTHORITY_STATUSES))
    return [f"authority_status: invalid values {bad}"] if bad else []


def validate_directionality_statuses(frame: pd.DataFrame) -> list[str]:
    if frame.empty or "directionality_status" not in frame.columns:
        return []
    bad = sorted(set(value for value in _column_values(frame, "directionality_status").tolist() if value and value not in V551J_DIRECTIONALITY_STATUSES))
    return [f"directionality_status: invalid values {bad}"] if bad else []


def validate_forbidden_claim_ids(frame: pd.DataFrame) -> list[str]:
    if frame.empty:
        return []
    if "forbidden_claim_ids_json" not in frame.columns:
        return ["forbidden_claim_ids_json: missing"]
    bad_rows: list[int] = []
    for idx, value in enumerate(frame["forbidden_claim_ids_json"].tolist()):
        try:
            parsed = json.loads(value) if isinstance(value, str) and value else []
        except Exception:
            bad_rows.append(idx)
            continue
        if not isinstance(parsed, list) or not parsed or any(str(item).strip() not in V551J_FORBIDDEN_CLAIM_IDS for item in parsed):
            bad_rows.append(idx)
    return [f"forbidden_claim_ids_json: invalid rows {bad_rows[:10]}"] if bad_rows else []


def validate_no_runtime_safe_packets_in_phase_a(frame: pd.DataFrame) -> list[str]:
    if frame.empty or "runtime_use_class" not in frame.columns:
        return []
    bad = frame[frame["runtime_use_class"].astype(str).isin({"runtime_safe_after_v552j", "runtime_safe_after_v553"})]
    return [f"runtime_use_class: runtime-safe rows present {len(bad)}"] if not bad.empty else []


def validate_future_affordances_are_coarse(frame: pd.DataFrame) -> list[str]:
    if frame.empty or "future_target_affordances_json" not in frame.columns:
        return []
    bad_rows: list[int] = []
    for idx, value in enumerate(frame["future_target_affordances_json"].tolist()):
        try:
            parsed = json.loads(value) if isinstance(value, str) and value else []
        except Exception:
            bad_rows.append(idx)
            continue
        if not isinstance(parsed, list):
            bad_rows.append(idx)
    return [f"future_target_affordances_json: invalid rows {bad_rows[:10]}"] if bad_rows else []


def validate_review_surface_statuses(frame: pd.DataFrame) -> list[str]:
    if frame.empty or "review_surface_status" not in frame.columns:
        return []
    bad = sorted(set(value for value in _column_values(frame, "review_surface_status").tolist() if value and value not in V551J_REVIEW_SURFACE_STATUSES))
    return [f"review_surface_status: invalid values {bad}"] if bad else []


def validate_review_priorities(frame: pd.DataFrame) -> list[str]:
    if frame.empty or "review_priority" not in frame.columns:
        return []
    bad = sorted(set(value for value in _column_values(frame, "review_priority").tolist() if value and value not in V551J_REVIEW_PRIORITIES))
    return [f"review_priority: invalid values {bad}"] if bad else []


def validate_reliability_numeric_columns(frame: pd.DataFrame) -> list[str]:
    if frame.empty:
        return []
    errors: list[str] = []
    columns = [
        "support_score_numeric",
        "confidence_score_numeric",
        "authority_score_numeric",
        "directionality_score_numeric",
        "join_strength_score_numeric",
        "semantic_specificity_score_numeric",
        "evidence_completeness_score_numeric",
        "certifiability_score_numeric",
        "review_priority_score_numeric",
    ]
    for column in columns:
        if column not in frame.columns:
            errors.append(f"{column}: missing")
            continue
        try:
            values = pd.to_numeric(frame[column], errors="coerce")
        except Exception:
            errors.append(f"{column}: not numeric")
            continue
        bad = values[(values < 0) | (values > 1) | values.isna()]
        if not bad.empty:
            errors.append(f"{column}: values outside [0,1] or missing")
    return errors


def validate_evidence_quality_statuses(frame: pd.DataFrame) -> list[str]:
    if frame.empty or "evidence_quality_status" not in frame.columns:
        return []
    bad = sorted(set(value for value in _column_values(frame, "evidence_quality_status").tolist() if value and value not in V551J_EVIDENCE_QUALITY_STATUSES))
    return [f"evidence_quality_status: invalid values {bad}"] if bad else []


def validate_use_permission_classes(frame: pd.DataFrame) -> list[str]:
    if frame.empty or "use_permission_class" not in frame.columns:
        return []
    bad = sorted(set(value for value in _column_values(frame, "use_permission_class").tolist() if value and value not in V551J_USE_PERMISSION_CLASSES))
    return [f"use_permission_class: invalid values {bad}"] if bad else []


def validate_review_surface_schema(frame: pd.DataFrame) -> list[str]:
    errors = validate_required_columns(frame, V551J_REVIEW_SURFACE_SCHEMA["required_columns"], "v551j_packet_review_surface")
    errors.extend(validate_review_surface_statuses(frame))
    errors.extend(validate_review_priorities(frame))
    errors.extend(validate_reliability_numeric_columns(frame))
    errors.extend(validate_evidence_quality_statuses(frame))
    errors.extend(validate_use_permission_classes(frame))
    if "certification_candidate" in frame.columns and frame["certification_candidate"].astype(str).str.lower().isin({"true", "1", "yes", "y"}).any():
        errors.append("certification_candidate: true values not allowed in phase B")
    return errors


def validate_reviewable_evidence_sidecar_schema(frame: pd.DataFrame) -> list[str]:
    errors = validate_required_columns(frame, V551J_REVIEWABLE_EVIDENCE_SIDECAR_SCHEMA["required_columns"], "v551j_reviewable_evidence_sidecar")
    errors.extend(validate_reliability_numeric_columns(frame))
    errors.extend(validate_evidence_quality_statuses(frame))
    errors.extend(validate_use_permission_classes(frame))
    if not frame.empty and "use_permission_class" in frame.columns:
        runtime_bad = frame[frame["use_permission_class"].astype(str).str.contains("runtime", case=False, na=False)]
        if not runtime_bad.empty:
            errors.append(f"use_permission_class: runtime permission present in sidecar rows={len(runtime_bad)}")
    if not frame.empty and "runtime_use_class" in frame.columns:
        runtime_bad = frame[frame["runtime_use_class"].astype(str).isin({"runtime_safe_after_v552j", "runtime_safe_after_v553"})]
        if not runtime_bad.empty:
            errors.append(f"runtime_use_class: runtime-safe sidecar rows present {len(runtime_bad)}")
    return errors


def validate_certified_packet_index_schema(frame: pd.DataFrame) -> list[str]:
    errors = validate_required_columns(frame, V551J_CERTIFIED_PACKET_INDEX_SCHEMA["required_columns"], "v551j_certified_packet_index")
    errors.extend(validate_packet_lifecycle_statuses(frame))
    if "certification_status" in frame.columns and not frame["certification_status"].astype(str).str.strip().eq("certified").all():
        errors.append("certification_status: non-certified values present")
    if "packet_status" in frame.columns and not frame["packet_status"].astype(str).str.strip().eq("certified").all():
        errors.append("packet_status: non-certified values present")
    return errors


def validate_certification_audit_schema(frame: pd.DataFrame) -> list[str]:
    return validate_required_columns(frame, V551J_CERTIFICATION_AUDIT_SCHEMA["required_columns"], "v551j_certification_audit")


def validate_certification_rejection_audit_schema(frame: pd.DataFrame) -> list[str]:
    return validate_required_columns(frame, V551J_CERTIFICATION_REJECTION_AUDIT_SCHEMA["required_columns"], "v551j_certification_rejection_audit")


def validate_certification_readiness_report_schema(frame: pd.DataFrame) -> list[str]:
    return validate_required_columns(frame, V551J_CERTIFICATION_READINESS_REPORT_SCHEMA["required_columns"], "v551j_certification_readiness_report")


def validate_json_array_columns(frame: pd.DataFrame) -> list[str]:
    if frame.empty:
        return []
    problems: list[str] = []
    json_cols = [column for column in frame.columns if column.endswith("_json")]
    for column in json_cols:
        for idx, value in enumerate(frame[column].tolist()):
            if value in {"", None}:
                continue
            try:
                parsed = json.loads(value) if isinstance(value, str) else value
            except Exception:
                problems.append(f"{column}: row {idx} not json")
                break
            if not isinstance(parsed, list):
                problems.append(f"{column}: row {idx} not list")
                break
    return problems


def validate_no_actor_orientation_fields(frame: pd.DataFrame) -> list[str]:
    forbidden = [column for column in frame.columns if column in {"identity_with", "actor_orientation", "parent_orientation", "coparent_orientation", "actor_absorption", "lens_capture", "object_visibility"}]
    return [f"actor_orientation_fields_present: {forbidden}"] if forbidden else []


def validate_no_carrier_mediation_fields(frame: pd.DataFrame) -> list[str]:
    forbidden = [column for column in frame.columns if column in {"carrier_language", "carrier_membership", "carrier_mediation"}]
    return [f"carrier_mediation_fields_present: {forbidden}"] if forbidden else []


def validate_no_enneagram_fields(frame: pd.DataFrame) -> list[str]:
    forbidden = [column for column in frame.columns if column in {"enneagram_type", "enneagram_attractor", "enneagram_mediation"}]
    return [f"enneagram_fields_present: {forbidden}"] if forbidden else []


def validate_candidate_trace_schema(frame: pd.DataFrame) -> list[str]:
    errors = validate_required_columns(frame, V551J_PACKET_CANDIDATE_TRACE_SCHEMA["required_columns"], "v551j_packet_candidate_trace")
    errors.extend(validate_packet_lifecycle_statuses(frame))
    errors.extend(validate_no_certified_packets_in_phase_a(frame))
    errors.extend(validate_runtime_use_classes(frame))
    errors.extend(validate_authority_statuses(frame))
    errors.extend(validate_directionality_statuses(frame))
    errors.extend(validate_forbidden_claim_ids(frame))
    errors.extend(validate_no_runtime_safe_packets_in_phase_a(frame))
    errors.extend(validate_future_affordances_are_coarse(frame))
    errors.extend(validate_json_array_columns(frame))
    errors.extend(validate_no_actor_orientation_fields(frame))
    errors.extend(validate_no_carrier_mediation_fields(frame))
    errors.extend(validate_no_enneagram_fields(frame))
    return errors
