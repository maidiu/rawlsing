#!/usr/bin/env python3
"""Shared V551J v2.2.3 identity, signature, and contract-hash helpers."""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any, Mapping, Sequence

V551J_PACKET_IDENTITY_NAMESPACE = "v551j_packet_identity_v2_2_2"
V551J_COMPONENT_IDENTITY_NAMESPACE = "v551j_component_identity_v2_2_2"
V551J_PACKET_CONTRACT_NAMESPACE = "v551j_packet_contract_v2_2_3"
V551J_STANCE_TO_DIRECTION = {
    "support": "positive",
    "oppose": "negative",
    "neutral": "neutral",
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)


def sha256_contract(namespace: str, payload: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_json({"namespace": namespace, **dict(payload)}).encode("utf-8")).hexdigest()


def clean(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    if text.lower() in {"nan", "none", "null"}:
        return ""
    return text


def scalar(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if math.isnan(value):
            return None
        if value.is_integer():
            return str(int(value))
        return format(value, ".15g")
    text = str(value).strip()
    if text == "" or text.lower() in {"nan", "none", "null"}:
        return None
    try:
        numeric = float(text)
        if numeric.is_integer():
            return str(int(numeric))
    except Exception:
        pass
    return text


def identity_scalar(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, float):
        if math.isnan(value):
            return None
        return float(f"{value:.12g}")
    if isinstance(value, (int, bool)):
        return value
    text = str(value).strip()
    if text == "" or text.lower() in {"nan", "none", "null"}:
        return None
    try:
        numeric = float(text)
        if numeric.is_integer():
            return int(numeric)
        return float(text)
    except Exception:
        pass
    return text


def identity_response_scalar(value: Any) -> Any:
    if value is None:
        return None
    text = str(value).strip()
    if text == "" or text.lower() in {"nan", "none", "null"}:
        return None
    if text.endswith(".0"):
        try:
            numeric = float(text)
            if numeric.is_integer():
                return str(int(numeric))
        except Exception:
            pass
    return text


def bool_value(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def json_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    try:
        parsed = json.loads(value) if isinstance(value, str) and value.strip() else []
    except Exception:
        return []
    return parsed if isinstance(parsed, list) else []


def recompute_v551j_packet_id(packet_or_identity_fields: Mapping[str, Any]) -> str:
    digest = sha256_contract(V551J_PACKET_IDENTITY_NAMESPACE, {
        "source_family": clean(packet_or_identity_fields.get("source_family")) or clean(packet_or_identity_fields.get("source")),
        "canonical_wave": clean(packet_or_identity_fields.get("canonical_wave")) or clean(packet_or_identity_fields.get("wave")),
        "country_code": clean(packet_or_identity_fields.get("country_code")),
        "family_id": clean(packet_or_identity_fields.get("family_id")),
        "pattern_id": clean(packet_or_identity_fields.get("pattern_id")),
    })
    return "v551j__" + digest[:32]


def recompute_v551j_component_id(component_or_identity_fields: Mapping[str, Any]) -> str:
    digest = sha256_contract(V551J_COMPONENT_IDENTITY_NAMESPACE, {
        "source_family": clean(component_or_identity_fields.get("source_family")) or clean(component_or_identity_fields.get("source")),
        "canonical_wave": clean(component_or_identity_fields.get("canonical_wave")) or clean(component_or_identity_fields.get("wave")),
        "country_code": clean(component_or_identity_fields.get("country_code")),
        "family_id": clean(component_or_identity_fields.get("family_id")),
        "pattern_id": clean(component_or_identity_fields.get("pattern_id")),
        "item_order": identity_scalar(component_or_identity_fields.get("item_order")),
        "question_id": clean(component_or_identity_fields.get("question_id")) or clean(component_or_identity_fields.get("v550j_item_question_id")),
        "var_code": clean(component_or_identity_fields.get("var_code")) or clean(component_or_identity_fields.get("v550j_item_var_code")),
        "response_value_normalized": identity_response_scalar(component_or_identity_fields.get("response_value_normalized") if "response_value_normalized" in component_or_identity_fields else component_or_identity_fields.get("v550j_item_response_value_normalized")),
    })
    return "v551jc__" + digest[:32]


def _comparison(left: Any, right: Any) -> str:
    left_value = scalar(left)
    right_value = scalar(right)
    if left_value is None and right_value is None:
        return "BOTH_MISSING"
    if left_value is None or right_value is None:
        return "ONE_SIDE_MISSING"
    return "EXACT_MATCH" if str(left_value).casefold() == str(right_value).casefold() else "CONFLICT"


def recompute_required_component_comparisons(component: Mapping[str, Any]) -> dict[str, str]:
    stance = clean(component.get("v550j_joint_response_stance")).casefold()
    expected_direction = V551J_STANCE_TO_DIRECTION.get(stance)
    actual_direction = clean(component.get("v551_response_direction")).casefold()
    if not expected_direction and not actual_direction:
        stance_status = "BOTH_MISSING"
    elif not expected_direction or not actual_direction:
        stance_status = "ONE_SIDE_MISSING"
    else:
        stance_status = "EXACT_MATCH" if expected_direction == actual_direction else "CONFLICT"
    return {
        "question_identity": _comparison(component.get("v550j_item_question_id"), component.get("v551_question_id")),
        "var_code": _comparison(component.get("v550j_item_var_code"), component.get("v551_var_code")),
        "response_identity": _comparison(component.get("v550j_item_response_value_normalized"), component.get("v551_response_value_normalized")),
        "normalized_response_label": _comparison(component.get("v550j_item_normalized_response_label"), component.get("v551_normalized_response_label")),
        "stance_direction": stance_status,
        "response_semantics_hash": _comparison(component.get("v550j_item_response_semantics_contract_hash"), component.get("v551_response_semantics_contract_hash")),
        "driver_id": _comparison(component.get("v550j_driver_id"), component.get("v551_driver_id")),
        "driver_facet": _comparison(component.get("v550j_driver_facet_id"), component.get("v551_driver_facet_id")),
        "relation_axis": _comparison(component.get("v550j_relation_axis_id"), component.get("v551_relation_axis_id")),
    }


def recompute_v551j_component_contract_hash(component: Mapping[str, Any]) -> str:
    comparisons = recompute_required_component_comparisons(component)
    payload = {
        "component_id": component.get("component_id"),
        "match_status": component.get("v551_atom_match_status"),
        "atom_contract_hash": component.get("v551_atom_contract_hash"),
        "cross_contract_status": component.get("cross_contract_status"),
        "paired_values": {
            "v550j_question_id": component.get("v550j_item_question_id"),
            "v551_question_id": component.get("v551_question_id"),
            "v550j_var_code": component.get("v550j_item_var_code"),
            "v551_var_code": component.get("v551_var_code"),
            "v550j_normalized_response_value": component.get("v550j_item_response_value_normalized"),
            "v551_response_value_normalized": component.get("v551_response_value_normalized"),
            "v550j_normalized_response_label": component.get("v550j_item_normalized_response_label"),
            "v551_normalized_response_label": component.get("v551_normalized_response_label"),
            "v550j_joint_response_stance": component.get("v550j_joint_response_stance"),
            "v551_response_direction": component.get("v551_response_direction"),
            "v550j_item_response_semantics_contract_hash": component.get("v550j_item_response_semantics_contract_hash"),
            "v551_response_semantics_contract_hash": component.get("v551_response_semantics_contract_hash"),
            "v550j_driver_id": component.get("v550j_driver_id"),
            "v551_driver_id": component.get("v551_driver_id"),
            "v550j_driver_facet_id": component.get("v550j_driver_facet_id"),
            "v551_driver_facet_id": component.get("v551_driver_facet_id"),
            "v550j_relation_axis_id": component.get("v550j_relation_axis_id"),
            "v551_relation_axis_id": component.get("v551_relation_axis_id"),
        },
        "stored_statuses": {
            "question_identity_status": component.get("question_identity_status"),
            "var_code_status": component.get("var_code_status"),
            "response_identity_status": component.get("response_identity_status"),
            "normalized_response_label_status": component.get("normalized_response_label_status"),
            "joint_response_stance_alignment_status": component.get("joint_response_stance_alignment_status"),
            "response_semantics_hash_status": component.get("response_semantics_hash_status"),
            "driver_id_status": component.get("driver_id_status"),
            "driver_facet_id_status": component.get("driver_facet_id_status"),
            "relation_axis_id_status": component.get("relation_axis_id_status"),
        },
        "recomputed_comparisons": comparisons,
    }
    return sha256_contract("v551j_component_match_v2_2_3", normalize_contract_value(payload))


def _signature(namespace: str, rows: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> str:
    payload = [{field: scalar(row.get(field)) for field in fields} for row in rows]
    return sha256_contract(namespace, {"ordered_components": payload})


def recompute_joint_response_identity_signature(rows: Sequence[Mapping[str, Any]]) -> str:
    return _signature("v551j_joint_response_identity_v2_2_3", rows, ["v550j_item_question_id", "v550j_item_var_code", "v551_question_id", "v551_var_code", "v550j_item_response_value_normalized", "v550j_item_normalized_response_label", "v550j_item_role", "v550j_item_condition_label"])


def recompute_joint_empirical_distribution_signature(rows: Sequence[Mapping[str, Any]]) -> str:
    return sha256_contract("v551j_joint_empirical_distribution_signature_v2_2_3", {"ordered_empirical_object_ids": [r.get("v551_empirical_object_id") or None for r in rows], "ordered_empirical_distribution_ids": [r.get("v551_empirical_distribution_id") or None for r in rows]})


def recompute_joint_semantic_signature(rows: Sequence[Mapping[str, Any]]) -> str:
    return _signature("v551j_joint_semantic_signature_v2_2_3", rows, ["v550j_item_semantic_response_role", "v550j_item_semantic_role_authority_status", "v550j_item_v551_evidence_role", "v550j_item_response_semantics_contract_hash", "v551_semantic_identity_signature"])


def recompute_joint_orientation_signature(rows: Sequence[Mapping[str, Any]]) -> str:
    return _signature("v551j_joint_orientation_signature_v2_2_3", rows, ["v550j_item_response_direction", "v551_response_direction", "v550j_item_response_intensity", "v551_response_intensity_status", "v550j_semantic_polarity_label", "v551_source_polarity_coordinate", "v550j_item_directionality_authority_status"])


def recompute_joint_topology_signature(packet: Mapping[str, Any], rows: Sequence[Mapping[str, Any]]) -> str:
    return sha256_contract("v551j_joint_topology_signature_v2_2_3", {"components": [{k: scalar(r.get(k)) for k in ["v551_response_scale_signature"]} for r in rows], "boundary_pattern_type": clean(packet.get("boundary_pattern_type")), "family_structure_type": clean(packet.get("family_structure_type"))})


def recompute_joint_target_signature(rows: Sequence[Mapping[str, Any]]) -> str:
    return _signature("v551j_joint_target_signature_v2_2_3", rows, ["v550j_relation_axis_id", "v550j_family_target_entity_id", "v550j_target_domain", "v550j_target_condition_label", "v550j_target_group_label", "v550j_permission_domain", "v550j_driver_id", "v550j_driver_facet_id", "v551_structural_target_entity_id"])


def recompute_joint_structural_signature(packet: Mapping[str, Any], rows: Sequence[Mapping[str, Any]]) -> str:
    return sha256_contract("v551j_joint_structural_signature_v2_2_3", {"component_structural_signatures": [r.get("v551_structural_identity_signature") for r in rows], "family_id": clean(packet.get("pattern_id")) or clean(packet.get("family_id")), "target_structure_status": packet.get("target_structure_status")})


def recompute_joint_component_measurement_signature(rows: Sequence[Mapping[str, Any]]) -> str:
    return sha256_contract("v551j_joint_component_measurement_signature_v2_2_3", {"components": [{k: scalar(r.get(k)) for k in ["v551_atom_id", "v551_atom_contract_hash", "v551_measurement_contract_hash", "v551_empirical_distribution_id", "v551_n_respondents", "component_v552_linkage_class", "v551_temporal_authority_status"]} for r in rows]})


def recompute_joint_measurement_contract_hash(packet: Mapping[str, Any]) -> str:
    fields = ["joint_pattern_count_unweighted", "joint_pattern_count_weighted", "joint_probability_unweighted", "joint_probability_weighted", "joint_probability_basis", "joint_probability", "joint_n_unweighted", "joint_n_weighted", "joint_weighted_count_basis", "joint_support_threshold", "joint_support_ratio", "joint_support_ratio_margin", "joint_support_score", "joint_support_status", "joint_support_gate_status", "joint_prevalence_score", "joint_completion_rate", "joint_missingness_rate", "joint_effective_n", "joint_effective_n_ratio", "joint_confidence_score", "joint_weight_status", "joint_measurement_status"]
    return sha256_contract("v551j_joint_measurement_contract_v2_2_3", {field: scalar(packet.get(field)) for field in fields})


def v551j_v2_2_3_packet_contract_payload(packet: Mapping[str, Any], ordered_components: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    rows = list(ordered_components)
    payload = {
        "packet_id": packet.get("packet_id"),
        "pattern_id": packet.get("pattern_id"),
        "family_id": packet.get("family_id"),
        "family_type": packet.get("family_type"),
        "family_structure_type": packet.get("family_structure_type"),
        "source": packet.get("source"),
        "source_family": packet.get("source_family"),
        "wave": packet.get("wave"),
        "canonical_wave": packet.get("canonical_wave"),
        "country_code": packet.get("country_code"),
        "schema_version": packet.get("schema_version"),
        "compiler_version": packet.get("compiler_version"),
        "certification_status": packet.get("certification_status"),
        "review_required": bool_value(packet.get("review_required")),
        "review_reason_codes_json": packet.get("review_reason_codes_json"),
        "blocking_reason_codes_json": packet.get("blocking_reason_codes_json"),
        "ready_for_v552j_joint_evidence": bool_value(packet.get("ready_for_v552j_joint_evidence")),
        "ready_for_v552j_component_linkage": bool_value(packet.get("ready_for_v552j_component_linkage")),
        "ready_for_v553": bool_value(packet.get("ready_for_v553")),
        "pressure_anchor_eligible": bool_value(packet.get("pressure_anchor_eligible")),
        "temporal_pressure_authorized": bool_value(packet.get("temporal_pressure_authorized")),
        "runtime_use_class": packet.get("runtime_use_class"),
        "allowed_future_targets_json": packet.get("allowed_future_targets_json"),
        "forbidden_future_targets_json": packet.get("forbidden_future_targets_json"),
        "forbidden_claim_ids_json": packet.get("forbidden_claim_ids_json"),
        "component_ids": [r.get("component_id") for r in rows],
        "component_contract_hashes": [r.get("component_contract_hash") for r in rows],
        "v551_atom_ids": [r.get("v551_atom_id") for r in rows],
        "v551_atom_contract_hashes": [r.get("v551_atom_contract_hash") for r in rows],
        "measurement_contract_hashes": [r.get("v551_measurement_contract_hash") for r in rows],
        "empirical_object_ids": [r.get("v551_empirical_object_id") for r in rows],
        "empirical_distribution_ids": [r.get("v551_empirical_distribution_id") for r in rows],
        "question_denominators": [scalar(r.get("v551_n_respondents")) for r in rows],
        "v552_linkage_classes": [r.get("component_v552_linkage_class") for r in rows],
        "joint_response_identity_signature": packet.get("joint_response_identity_signature"),
        "joint_empirical_distribution_signature": packet.get("joint_empirical_distribution_signature"),
        "joint_semantic_signature": packet.get("joint_semantic_signature"),
        "joint_orientation_signature": packet.get("joint_orientation_signature"),
        "joint_topology_signature": packet.get("joint_topology_signature"),
        "joint_target_signature": packet.get("joint_target_signature"),
        "joint_structural_signature": packet.get("joint_structural_signature"),
        "joint_component_measurement_signature": packet.get("joint_component_measurement_signature"),
        "joint_measurement_contract_hash": packet.get("joint_measurement_contract_hash"),
        "joint_pattern_count_unweighted": packet.get("joint_pattern_count_unweighted"),
        "joint_pattern_count_weighted": packet.get("joint_pattern_count_weighted"),
        "joint_probability_unweighted": packet.get("joint_probability_unweighted"),
        "joint_probability_weighted": packet.get("joint_probability_weighted"),
        "joint_probability_basis": packet.get("joint_probability_basis"),
        "joint_probability": packet.get("joint_probability"),
        "joint_n_unweighted": packet.get("joint_n_unweighted"),
        "joint_n_weighted": packet.get("joint_n_weighted"),
        "joint_support_threshold": packet.get("joint_support_threshold"),
        "joint_support_ratio": packet.get("joint_support_ratio"),
        "joint_support_score": packet.get("joint_support_score"),
        "joint_support_status": packet.get("joint_support_status"),
        "joint_support_gate_status": packet.get("joint_support_gate_status"),
        "joint_effective_n": packet.get("joint_effective_n"),
        "joint_effective_n_ratio": packet.get("joint_effective_n_ratio"),
        "v551_input_artifact_hash": packet.get("v551_input_artifact_hash"),
        "v550j_pattern_index_artifact_hash": packet.get("v550j_pattern_index_artifact_hash"),
        "v550j_pattern_item_index_artifact_hash": packet.get("v550j_pattern_item_index_artifact_hash"),
        "v550j_relation_signature_artifact_hash": packet.get("v550j_relation_signature_artifact_hash"),
        "v550j_manifest_hash": packet.get("v550j_manifest_hash"),
        "v550j_readiness_report_hash": packet.get("v550j_readiness_report_hash"),
        "question_family_registry_hash": packet.get("question_family_registry_hash"),
        "joint_semantic_authority_status": packet.get("joint_semantic_authority_status"),
        "joint_directionality_authority_status": packet.get("joint_directionality_authority_status"),
        "joint_family_target_authority_status": packet.get("joint_family_target_authority_status"),
        "joint_structural_authority_status": packet.get("joint_structural_authority_status"),
        "joint_measurement_authority_status": packet.get("joint_measurement_authority_status"),
        "joint_evidence_authority_status": packet.get("joint_evidence_authority_status"),
    }
    return normalize_contract_value(payload)


def normalize_contract_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): normalize_contract_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [normalize_contract_value(v) for v in value]
    if isinstance(value, bool):
        return value
    if value is None:
        return None
    text = scalar(value)
    return text


def recompute_v551j_v2_2_3_packet_contract_hash(packet: Mapping[str, Any], ordered_components: Sequence[Mapping[str, Any]]) -> str:
    return sha256_contract(V551J_PACKET_CONTRACT_NAMESPACE, v551j_v2_2_3_packet_contract_payload(packet, ordered_components))
