#!/usr/bin/env python3
"""V551J certification helpers for phase C."""

from __future__ import annotations

import json
import hashlib
from collections import Counter
from typing import Any

import pandas as pd

from data.ddm_build_copy.ddm_v550_manifest import utc_now
from data.ddm_build_copy.ddm_v551j_schema import (
    V551J_CERTIFICATION_AUDIT_SCHEMA,
    V551J_CERTIFICATION_READINESS_REPORT_SCHEMA,
    V551J_CERTIFICATION_REJECTION_AUDIT_SCHEMA,
    V551J_CERTIFIED_PACKET_INDEX_SCHEMA,
)
from data.ddm_build_copy.ddm_v551j_contract import recompute_v551j_v2_2_3_packet_contract_hash


def certify_v551j_v2_2_3(
    candidate: pd.DataFrame,
    component: pd.DataFrame,
    validation_report: dict[str, Any],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Apply V551J v2.2.3 certification gates to candidate packets."""
    rows: list[dict[str, Any]] = []
    rejection_rows: list[dict[str, Any]] = []
    finalized_rows: list[dict[str, Any]] = []
    valid = bool(validation_report.get("candidate_contract_valid")) and bool(validation_report.get("component_contract_valid"))
    components_by_packet = {packet_id: frame for packet_id, frame in component.groupby("packet_id")} if not component.empty and "packet_id" in component.columns else {}
    for row in candidate.to_dict("records"):
        packet_id = _clean(row.get("packet_id"))
        comps = components_by_packet.get(packet_id, pd.DataFrame())
        gates = {
            "pattern_identity_gate": bool(packet_id and _clean(row.get("pattern_id"))),
            "item_order_gate": bool(_clean(row.get("component_order_integrity_status")) == "PASS"),
            "component_match_completeness_gate": bool(int(row.get("unmatched_unexplained_component_count") or 0) == 0 and int(row.get("ambiguous_component_count") or 0) == 0),
            "empirical_distribution_identity_gate": bool(not comps.empty and comps.get("v551_empirical_distribution_id", pd.Series(dtype=str)).fillna("").astype(str).ne("").all()),
            "component_denominator_contract_gate": bool(_clean(row.get("denominator_separation_status")) == "PASS"),
            "question_identity_gate": bool(not comps.empty and comps.get("question_identity_status", pd.Series(dtype=str)).astype(str).eq("EXACT_MATCH").all() and comps.get("var_code_status", pd.Series(dtype=str)).astype(str).eq("EXACT_MATCH").all()),
            "response_identity_gate": bool(not comps.empty and comps.get("response_identity_status", pd.Series(dtype=str)).astype(str).eq("EXACT_MATCH").all()),
            "response_semantics_authority_gate": bool(_clean(row.get("joint_semantic_authority_status")) == "CERTIFIED"),
            "directionality_authority_gate": bool(_clean(row.get("joint_directionality_authority_status")) == "CERTIFIED"),
            "semantic_polarity_gate": bool(not comps.empty and comps.get("semantic_polarity_status", pd.Series(dtype=str)).astype(str).eq("EXACT_MATCH").all()),
            "shared_structural_contract_gate": bool(_clean(row.get("shared_structural_status")) == "CERTIFIED"),
            "family_target_registry_gate": bool(_clean(row.get("family_target_status")) == "CERTIFIED"),
            "target_layer_relation_gate": bool(not comps.empty and comps.get("target_layer_relation_status", pd.Series(dtype=str)).astype(str).eq("PARALLEL_GOVERNED_TARGET_LAYERS").all()),
            "measurement_separation_gate": bool(_clean(row.get("joint_measurement_status")) == "COMPLETE_PATTERN_MEASUREMENT_CONTRACT"),
            "pattern_support_gate": bool(_clean(row.get("joint_support_status")) in {"sufficient_support", "supported"}),
            "pattern_measurement_gate": bool(_clean(row.get("joint_measurement_authority_status")) == "CERTIFIED"),
            "joint_evidence_class_gate": bool(_clean(row.get("joint_evidence_class")) not in {"blocked_joint_pattern", "joint_pattern_context_only"}),
            "minimum_relation_component_gate": bool(int(row.get("matched_relation_component_count") or 0) >= 2),
            "registry_hash_gate": bool(_clean(row.get("question_family_registry_status")) == "MATCHED_GOVERNED_REGISTRY_HASH"),
            "forbidden_inference_gate": True,
            "permission_boundary_gate": bool(not bool(row.get("ready_for_v553")) and not bool(row.get("pressure_anchor_eligible")) and not bool(row.get("temporal_pressure_authorized")) and _clean(row.get("runtime_use_class")) == "not_runtime_consumable"),
            "packet_contract_validation_gate": valid,
        }
        certified = all(gates.values())
        blockers = [name for name, passed in gates.items() if not passed]
        support_only_review = blockers == ["pattern_support_gate"]
        final_row = dict(row)
        if certified:
            final_row.update({
                "certification_status": "CERTIFIED_JOINT_RELATION_EVIDENCE",
                "review_required": False,
                "review_reason_codes_json": "[]",
                "blocking_reason_codes_json": "[]",
                "ready_for_v552j_joint_evidence": True,
                "ready_for_v552j_component_linkage": True,
                "allowed_future_targets_json": json.dumps(["v552j"]),
            })
        elif support_only_review:
            final_row.update({
                "certification_status": "REVIEW_REQUIRED_COMPONENT_GAP",
                "review_required": True,
                "review_reason_codes_json": json.dumps(["pattern_support_gate"]),
                "blocking_reason_codes_json": "[]",
                "ready_for_v552j_joint_evidence": False,
                "ready_for_v552j_component_linkage": False,
                "allowed_future_targets_json": "[]",
            })
        else:
            final_row.update({
                "certification_status": "BLOCKED_PACKET_CONTRACT",
                "review_required": True,
                "review_reason_codes_json": "[]",
                "blocking_reason_codes_json": json.dumps(blockers, ensure_ascii=False),
                "ready_for_v552j_joint_evidence": False,
                "ready_for_v552j_component_linkage": False,
                "allowed_future_targets_json": "[]",
            })
        ordered_components = comps.sort_values("item_order", kind="mergesort").to_dict("records") if not comps.empty else []
        final_row["packet_contract_hash"] = recompute_v551j_v2_2_3_packet_contract_hash(final_row, ordered_components)
        finalized_rows.append(final_row)
        audit_row = {
            "run_id": row.get("run_id"),
            "packet_id": packet_id,
            "packet_type": row.get("joint_evidence_class"),
            "source": row.get("source"),
            "wave": row.get("wave"),
            "canonical_wave": row.get("canonical_wave"),
            "country_code": row.get("country_code"),
            "gate_identity_pass": gates["pattern_identity_gate"] and gates["question_identity_gate"],
            "gate_lifecycle_pass": gates["item_order_gate"] and gates["component_match_completeness_gate"],
            "gate_authority_pass": gates["response_semantics_authority_gate"] and gates["family_target_registry_gate"],
            "gate_support_pass": gates["pattern_support_gate"],
            "gate_directionality_pass": gates["directionality_authority_gate"] and gates["semantic_polarity_gate"],
            "gate_forbidden_claims_pass": gates["forbidden_inference_gate"],
            "gate_mediation_flags_pass": gates["permission_boundary_gate"],
            "gate_no_downstream_leakage_pass": gates["permission_boundary_gate"],
            "certified": certified,
            "certification_blockers_json": json.dumps(blockers, ensure_ascii=False),
            "certification_notes_json": json.dumps(gates, sort_keys=True, ensure_ascii=False),
            "created_at": utc_now(),
            "schema_version": "v2.2.3",
            "compiler_version": "v551j_joint_evidence_contract_v2_2_3",
        }
        rows.append(audit_row)
        if not certified:
            rejection = {k: audit_row.get(k) for k in ["run_id", "packet_id", "packet_type", "source", "wave", "canonical_wave", "country_code", "gate_identity_pass", "gate_lifecycle_pass", "gate_authority_pass", "gate_support_pass", "gate_directionality_pass", "gate_forbidden_claims_pass", "gate_mediation_flags_pass", "gate_no_downstream_leakage_pass", "created_at", "schema_version"]}
            rejection.update({"certification_blocker_code": "REVIEW_REQUIRED_COMPONENT_GAP" if support_only_review else "BLOCKED_PACKET_CONTRACT", "certification_blocker_detail": json.dumps(blockers, ensure_ascii=False)})
            rejection_rows.append(rejection)
    audit = pd.DataFrame(rows).reindex(columns=V551J_CERTIFICATION_AUDIT_SCHEMA["required_columns"])
    finalized = pd.DataFrame(finalized_rows).reindex(columns=candidate.columns)
    certified_ids = {r["packet_id"] for r in rows if r["certified"]}
    certified = finalized[finalized["packet_id"].astype(str).isin(certified_ids)].copy()
    certified["certification_status"] = "CERTIFIED_JOINT_RELATION_EVIDENCE"
    rejection = pd.DataFrame(rejection_rows).reindex(columns=V551J_CERTIFICATION_REJECTION_AUDIT_SCHEMA["required_columns"])
    return finalized, certified, audit, rejection


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


def _to_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)) and not pd.isna(value):
        return value != 0
    text = _clean(value).lower()
    if text in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "f", "no", "n", "off", "", "nan", "none"}:
        return False
    return default


def _json_array(values: list[Any] | tuple[Any, ...] | set[Any] | None) -> str:
    if not values:
        return "[]"
    cleaned: list[str] = []
    for value in values:
        token = _clean(value)
        if token and token not in cleaned:
            cleaned.append(token)
    return json.dumps(cleaned, ensure_ascii=False)


def _parse_json_array(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
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


def _row_lookup(frame: pd.DataFrame, packet_id: str) -> pd.Series | None:
    if frame.empty or "packet_id" not in frame.columns:
        return None
    subset = frame[frame["packet_id"].astype(str).str.strip().eq(packet_id)]
    if subset.empty:
        return None
    return subset.iloc[0]


def _gate_results(row: pd.Series) -> dict[str, bool]:
    allowed_lifecycle = {"reviewable", "reviewable_with_context_gap", "reviewable_with_directionality_gap"}
    allowed_authority = {"exact_registry", "prefix_registry"}
    allowed_directionality = {"known_directional"}
    allowed_support = {"sufficient_support", "supported"}
    allowed_confidence = {"medium", "high", "very_high"}
    forbidden_leak_fields = {
        "identity_with",
        "alienation_from",
        "lens_capture",
        "object_visibility",
        "carrier_language",
        "implicit_legitimated_strata",
        "actor_absorption",
        "parent_orientation",
        "coparent_orientation",
        "expectation_baseline",
        "striving_affordance",
        "pressureflow_route",
        "enneagram_type",
        "enneagram_attractor",
    }
    forbidden_claims = _parse_json_array(row.get("forbidden_claim_ids_json"))
    return {
        "gate_identity_pass": bool(_clean(row.get("packet_id")) and _clean(row.get("source")) and _clean(row.get("wave")) and _clean(row.get("country_code")) and _clean(row.get("source_artifact_ids_json")) and (_parse_json_array(row.get("input_atom_ids_json")) or _parse_json_array(row.get("input_pattern_ids_json")))),
        "gate_lifecycle_pass": _clean(row.get("review_surface_status")) in allowed_lifecycle,
        "gate_authority_pass": _clean(row.get("authority_status")) in allowed_authority,
        "gate_support_pass": (
            _clean(row.get("support_status")) in allowed_support
            and _clean(row.get("confidence_tier")) in allowed_confidence
        ),
        "gate_directionality_pass": _clean(row.get("directionality_status")) in allowed_directionality if _clean(row.get("packet_type")) == "joint_relation_evidence_packet" else _clean(row.get("directionality_status")) in allowed_directionality or _clean(row.get("directionality_status")) in {"not_applicable", "undirected_association", "unknown"},
        "gate_forbidden_claims_pass": bool(forbidden_claims) and {"do_not_render_as_person_belief", "do_not_render_as_causal_relation", "do_not_render_as_runtime_psyche"}.issubset(set(forbidden_claims)),
        "gate_mediation_flags_pass": _to_bool(row.get("requires_temporalization"), False) and _to_bool(row.get("requires_orientation_resolution"), False) and _to_bool(row.get("requires_pressureflow_mediation"), False) and not _to_bool(row.get("person_level_allowed"), True) and not _to_bool(row.get("household_level_allowed"), True) and not _to_bool(row.get("carrier_level_allowed"), True) and _to_bool(row.get("structural_level_only"), False),
        "gate_no_downstream_leakage_pass": not any(_clean(row.get(field)) for field in forbidden_leak_fields),
    }


def _certification_blockers(row: pd.Series, gate_results: dict[str, bool]) -> list[str]:
    blockers: list[str] = []
    if not gate_results["gate_identity_pass"]:
        blockers.append("identity")
    if not gate_results["gate_lifecycle_pass"]:
        blockers.append("lifecycle")
    if not gate_results["gate_authority_pass"]:
        blockers.append("authority")
    if not gate_results["gate_support_pass"]:
        blockers.append("support")
    if not gate_results["gate_directionality_pass"]:
        blockers.append("directionality")
    if not gate_results["gate_forbidden_claims_pass"]:
        blockers.append("forbidden_claims")
    if not gate_results["gate_mediation_flags_pass"]:
        blockers.append("mediation_flags")
    if not gate_results["gate_no_downstream_leakage_pass"]:
        blockers.append("downstream_leakage")
    return blockers


def _certification_notes(row: pd.Series, gate_results: dict[str, bool], blockers: list[str]) -> list[str]:
    notes = [
        f"review_surface_status={_clean(row.get('review_surface_status'))}",
        f"authority_status={_clean(row.get('authority_status'))}",
        f"directionality_status={_clean(row.get('directionality_status'))}",
        f"support_status={_clean(row.get('support_status'))}",
    ]
    if blockers:
        notes.append(f"blockers={','.join(blockers)}")
    return notes


def _directionality_limited(row: pd.Series) -> bool:
    if _clean(row.get("packet_type")) == "joint_relation_evidence_packet":
        return False
    return _clean(row.get("directionality_status")) in {"not_applicable", "undirected_association", "unknown"}


def _status_conflict_reasons(row: pd.Series) -> list[str]:
    reasons: list[str] = []
    if _clean(row.get("status_conflict_flag")) in {"true", "1", "yes", "y"}:
        detail = _clean(row.get("status_conflict_reason"))
        reasons.append(detail or "status_conflict")
    return reasons


def build_v551j_status_conflict_audit(review_surface: pd.DataFrame, *, run_id: str = "") -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if review_surface.empty:
        return pd.DataFrame(
            columns=[
                "run_id",
                "v552j_packet_id",
                "packet_id",
                "source_fields_json",
                "observed_values_json",
                "normalized_status",
                "normalization_rule_id",
                "conflict_severity",
                "blocking_effect",
                "resolution_required",
                "created_at",
                "schema_version",
                "compiler_version",
            ]
        )
    for row in review_surface.itertuples(index=False):
        series = pd.Series(row._asdict())
        if not _to_bool(series.get("status_conflict_flag"), False) and not _clean(series.get("status_conflict_reason")):
            continue
        observed = {
            "v551j_evidence_certification_status": _clean(series.get("v551j_evidence_certification_status")),
            "v551j_review_surface_status": _clean(series.get("v551j_review_surface_status")),
            "normalized_v551j_certification_status": _clean(series.get("normalized_v551j_certification_status")),
            "normalized_v551j_review_status": _clean(series.get("normalized_v551j_review_status")),
            "normalized_v551j_lane": _clean(series.get("normalized_v551j_lane")),
            "normalized_authority_status": _clean(series.get("normalized_authority_status")),
            "normalized_directionality_status": _clean(series.get("normalized_directionality_status")),
            "normalized_support_status": _clean(series.get("normalized_support_status")),
            "permission_class": _clean(series.get("permission_class")),
        }
        rows.append(
            {
                "run_id": run_id,
                "v552j_packet_id": _clean(series.get("packet_id")),
                "packet_id": _clean(series.get("packet_id")),
                "source_fields_json": _json_array(
                    [
                        "v551j_evidence_certification_status",
                        "v551j_review_surface_status",
                        "normalized_v551j_certification_status",
                        "normalized_v551j_review_status",
                        "normalized_v551j_lane",
                        "normalized_authority_status",
                        "normalized_directionality_status",
                        "normalized_support_status",
                        "permission_class",
                    ]
                ),
                "observed_values_json": json.dumps(observed, sort_keys=True, ensure_ascii=False),
                "normalized_status": _clean(series.get("normalized_v551j_lane")) or "conflict",
                "normalization_rule_id": "V551J_STATUS_NORMALIZATION_V1",
                "conflict_severity": "high" if _clean(series.get("status_conflict_reason")) else "medium",
                "blocking_effect": "blocks_v552j_adapter",
                "resolution_required": True,
                "created_at": utc_now(),
                "schema_version": "v0.1",
                "compiler_version": "v551j_bc_skeleton_0.2",
            }
        )
    return pd.DataFrame(rows, columns=[
        "run_id",
        "v552j_packet_id",
        "packet_id",
        "source_fields_json",
        "observed_values_json",
        "normalized_status",
        "normalization_rule_id",
        "conflict_severity",
        "blocking_effect",
        "resolution_required",
        "created_at",
        "schema_version",
        "compiler_version",
    ])


def build_v551j_certified_packet_index(
    candidate_trace: pd.DataFrame,
    review_surface: pd.DataFrame,
    *,
    run_id: str = "",
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if review_surface.empty:
        empty_certified = pd.DataFrame(columns=V551J_CERTIFIED_PACKET_INDEX_SCHEMA["required_columns"])
        empty_audit = pd.DataFrame(columns=V551J_CERTIFICATION_AUDIT_SCHEMA["required_columns"])
        empty_rejection = pd.DataFrame(columns=V551J_CERTIFICATION_REJECTION_AUDIT_SCHEMA["required_columns"])
        empty_readiness = pd.DataFrame(columns=V551J_CERTIFICATION_READINESS_REPORT_SCHEMA["required_columns"])
        return empty_certified, empty_audit, empty_rejection, empty_readiness

    certified_rows: list[dict[str, Any]] = []
    audit_rows: list[dict[str, Any]] = []
    rejection_rows: list[dict[str, Any]] = []

    for row in review_surface.itertuples(index=False):
        series = pd.Series(row._asdict())
        evidence_status_input = _clean(series.get("v551j_evidence_certification_status")) or _clean(series.get("certification_status")) or _clean(series.get("packet_status"))
        candidate_row = _row_lookup(candidate_trace, _clean(series.get("packet_id"))) if not candidate_trace.empty else None
        if candidate_row is not None:
            for column in ["run_id", "source", "wave", "canonical_wave", "country_code", "source_artifact_ids_json", "input_atom_ids_json", "input_pattern_ids_json"]:
                if column in candidate_row.index and not _clean(series.get(column)):
                    series[column] = candidate_row.get(column)
        gate_results = _gate_results(series)
        blockers = _certification_blockers(series, gate_results)
        blockers.extend(_status_conflict_reasons(series))
        certified = not blockers
        notes = _certification_notes(series, gate_results, blockers)
        normalized_review_status = _clean(series.get("normalized_v551j_review_status")) or _clean(series.get("review_surface_status")) or "unknown"
        normalized_certification_status = "certified" if certified else _clean(series.get("normalized_v551j_certification_status")) or "reviewable"
        normalized_lane = "certified_spine" if certified else _clean(series.get("normalized_v551j_lane")) or ("reviewable_context" if normalized_review_status.startswith("reviewable") else "blocked")
        normalized_authority_status = _clean(series.get("normalized_authority_status")) or _clean(series.get("authority_status")) or "unknown"
        normalized_directionality_status = _clean(series.get("normalized_directionality_status")) or _clean(series.get("directionality_status")) or "unknown"
        normalized_support_status = _clean(series.get("normalized_support_status")) or _clean(series.get("support_status")) or "unknown"
        normalized_v552_context_status = _clean(series.get("normalized_v552_context_status")) or _clean(series.get("v552_context_status")) or "not_supplied"
        normalized_comparability_status = _clean(series.get("normalized_comparability_status")) or _clean(series.get("comparability_status")) or "not_supplied"
        permission_class = "v553_constraint_candidate" if certified else _clean(series.get("permission_class")) or ("v553_context_only" if normalized_lane == "reviewable_context" else "blocked")
        audit_rows.append(
            {
                "run_id": run_id,
                "packet_id": _clean(series.get("packet_id")),
                "packet_type": _clean(series.get("packet_type")),
                "source": _clean(series.get("source")),
                "wave": _clean(series.get("wave")),
                "canonical_wave": _clean(series.get("canonical_wave")),
                "country_code": _clean(series.get("country_code")),
                **gate_results,
                "certified": certified,
                "certification_blockers_json": _json_array(blockers),
                "certification_notes_json": _json_array(notes),
                "created_at": utc_now(),
                "schema_version": "v0.1",
            }
        )
        if certified:
            series = series.copy()
            series["normalized_v551j_lane"] = normalized_lane
            series["normalized_v551j_certification_status"] = normalized_certification_status
            series["normalized_v551j_review_status"] = normalized_review_status
            series["normalized_authority_status"] = normalized_authority_status
            series["normalized_directionality_status"] = normalized_directionality_status
            series["normalized_support_status"] = normalized_support_status
            series["normalized_v552_context_status"] = normalized_v552_context_status
            series["normalized_comparability_status"] = normalized_comparability_status
            series["permission_class"] = permission_class
            series["constraint_eligibility"] = normalized_lane == "certified_spine"
            series["context_eligibility"] = normalized_lane in {"certified_spine", "reviewable_context"}
            series["forensic_eligibility"] = normalized_lane in {"diagnostic_forensic", "blocked", "conflict"}
            series["blocked_from_downstream"] = normalized_lane in {"blocked", "conflict"}
            series["v551j_evidence_certification_status_input"] = evidence_status_input
            series["status_conflict_flag"] = False
            series["status_conflict_reason"] = ""
            series["v551j_evidence_certification_status"] = "certified"
            certified_rows.append(
                {
                    **series.to_dict(),
                    "packet_status": "certified",
                    "certification_status": "certified",
                    "status_resolution_provenance_json": json.dumps(
                        {
                            "input_v551j_evidence_certification_status": evidence_status_input,
                            "resolved_v551j_evidence_certification_status": "certified",
                            "normalized_v551j_certification_status": normalized_certification_status,
                            "normalized_v551j_lane": normalized_lane,
                            "resolution_rule": "strict_certification_gates",
                        },
                        sort_keys=True,
                        ensure_ascii=False,
                    ),
                    "certification_basis_json": _json_array(
                        [
                            "strict_review_surface",
                            "identity",
                            "authority",
                            "support",
                            "directionality" if not _directionality_limited(series) else "directionality_limited",
                        ]
                    ),
                    "certification_gate_results_json": json.dumps(gate_results, sort_keys=True),
                    "certified_at": utc_now(),
                    "certification_schema_version": "v0.1",
                    "directionality_limited": _directionality_limited(series),
                }
            )
        else:
            rejection_rows.append(
                {
                    "run_id": run_id,
                    "packet_id": _clean(series.get("packet_id")),
                    "packet_type": _clean(series.get("packet_type")),
                    "source": _clean(series.get("source")),
                    "wave": _clean(series.get("wave")),
                    "canonical_wave": _clean(series.get("canonical_wave")),
                    "country_code": _clean(series.get("country_code")),
                    "certification_blocker_code": blockers[0] if blockers else "unknown",
                    "certification_blocker_detail": "; ".join(notes),
                    **gate_results,
                    "created_at": utc_now(),
                    "schema_version": "v0.1",
                }
            )

    certified_df = pd.DataFrame(certified_rows, columns=V551J_CERTIFIED_PACKET_INDEX_SCHEMA["required_columns"])
    if not certified_df.empty:
        certified_df = certified_df.fillna("").reset_index(drop=True)
    audit_df = pd.DataFrame(audit_rows, columns=V551J_CERTIFICATION_AUDIT_SCHEMA["required_columns"])
    rejection_df = pd.DataFrame(rejection_rows, columns=V551J_CERTIFICATION_REJECTION_AUDIT_SCHEMA["required_columns"])

    readiness_row = {
        "run_id": run_id,
        "review_surface_rows": int(len(review_surface)),
        "certified_packet_rows": int(len(certified_df)),
        "rejection_rows": int(len(rejection_df)),
        "gate_identity_pass_rows": int(audit_df["gate_identity_pass"].astype(bool).sum()) if not audit_df.empty else 0,
        "gate_lifecycle_pass_rows": int(audit_df["gate_lifecycle_pass"].astype(bool).sum()) if not audit_df.empty else 0,
        "gate_authority_pass_rows": int(audit_df["gate_authority_pass"].astype(bool).sum()) if not audit_df.empty else 0,
        "gate_support_pass_rows": int(audit_df["gate_support_pass"].astype(bool).sum()) if not audit_df.empty else 0,
        "gate_directionality_pass_rows": int(audit_df["gate_directionality_pass"].astype(bool).sum()) if not audit_df.empty else 0,
        "gate_forbidden_claims_pass_rows": int(audit_df["gate_forbidden_claims_pass"].astype(bool).sum()) if not audit_df.empty else 0,
        "gate_mediation_flags_pass_rows": int(audit_df["gate_mediation_flags_pass"].astype(bool).sum()) if not audit_df.empty else 0,
        "gate_no_downstream_leakage_pass_rows": int(audit_df["gate_no_downstream_leakage_pass"].astype(bool).sum()) if not audit_df.empty else 0,
        "certification_status_counts": json.dumps(dict(Counter(["certified" if val else "rejected" for val in audit_df["certified"].tolist()] if not audit_df.empty and "certified" in audit_df.columns else [])), sort_keys=True),
        "v552_context_status_counts": json.dumps(dict(Counter(certified_df["v552_context_status"].astype(str))) if not certified_df.empty and "v552_context_status" in certified_df.columns else {}, sort_keys=True),
        "evidence_certification_status_counts": json.dumps(dict(Counter(review_surface["v551j_evidence_certification_status"].astype(str))) if not review_surface.empty and "v551j_evidence_certification_status" in review_surface.columns else {}, sort_keys=True),
        "authority_status_counts": json.dumps(dict(Counter(certified_df["authority_status"].astype(str))) if not certified_df.empty and "authority_status" in certified_df.columns else {}, sort_keys=True),
        "directionality_status_counts": json.dumps(dict(Counter(certified_df["directionality_status"].astype(str))) if not certified_df.empty and "directionality_status" in certified_df.columns else {}, sort_keys=True),
        "review_surface_status_counts": json.dumps(dict(Counter(review_surface["review_surface_status"].astype(str))) if not review_surface.empty and "review_surface_status" in review_surface.columns else {}, sort_keys=True),
        "final_status": (
            "READY_V551J_EVIDENCE_CERTIFIED_WITH_CONTEXT_GAPS"
            if len(certified_df) and not certified_df.empty and "review_surface_status" in certified_df.columns and certified_df["review_surface_status"].astype(str).eq("reviewable_with_context_gap").any()
            else "READY_V551J_EVIDENCE_CERTIFIED"
            if len(certified_df)
            else "NOT_READY_NO_CERTIFIED_ROWS"
        ),
        "created_at": utc_now(),
        "schema_version": "v0.1",
    }
    readiness_df = pd.DataFrame([readiness_row], columns=V551J_CERTIFICATION_READINESS_REPORT_SCHEMA["required_columns"])
    return certified_df, audit_df, rejection_df, readiness_df
