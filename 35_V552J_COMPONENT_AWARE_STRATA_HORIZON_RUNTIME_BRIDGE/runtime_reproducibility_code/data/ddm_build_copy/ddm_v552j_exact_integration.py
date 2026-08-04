#!/usr/bin/env python3
"""Exact V551J-component to V552-pressure integration for V552J.

The authoritative row grain is one exact V552 pressure observation.  V551J
packets attach as certified or review-only context through their component's
V551 empirical-distribution identity.  V552 pressure values and measurement
identities are copied without mutation.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping

import pandas as pd

V552J_EXACT_SCHEMA_VERSION = "v1.0"
V552J_EXACT_COMPILER_VERSION = "v552j_exact_pressure_integration_1.0"

PRESSURE_COPY_FIELDS = [
    "v552_pressure_observation_id",
    "pressure_observation_identity_hash",
    "empirical_distribution_id",
    "component_response_surface_signature",
    "response_surface_completeness_status",
    "pressure_measure_class",
    "pressure_score",
    "pressure_score_status",
    "pressure_formula_id",
    "pressure_formula_version",
    "pressure_scale_id",
    "pressure_measurement_hash",
    "source_intensity_representation_class",
    "source_intensity_representation_status",
    "source_intensity_exact_fit_candidates_json",
    "known_absences_json",
    "forbidden_inference_json",
]

SCOPE_FIELDS = ["source_family", "canonical_wave", "country_code"]

PACKET_CONTEXT_COPY_FIELDS = [
    "packet_contract_hash",
    "joint_support_score",
    "joint_support_status",
    "joint_support_gate_status",
    "joint_confidence_score",
    "joint_evidence_class",
    "joint_semantic_authority_status",
    "joint_directionality_authority_status",
    "joint_family_target_authority_status",
    "joint_structural_authority_status",
    "joint_measurement_authority_status",
    "joint_evidence_authority_status",
    "certification_status",
    "ready_for_v552j_joint_evidence",
    "ready_for_v552j_component_linkage",
    "pressure_anchor_eligible",
    "temporal_pressure_authorized",
    "runtime_use_class",
    "allowed_future_targets_json",
    "forbidden_future_targets_json",
    "forbidden_claim_ids_json",
    "known_absences_json",
    "review_reason_codes_json",
    "blocking_reason_codes_json",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    return str(value).strip()


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return clean(value).lower() in {"1", "true", "t", "yes", "y", "pass", "ready", "certified", "governed"}


def parse_json_array(value: Any) -> list[str]:
    if isinstance(value, (list, tuple, set)):
        return [clean(v) for v in value if clean(v)]
    text = clean(value)
    if not text:
        return []
    try:
        payload = json.loads(text)
        if isinstance(payload, list):
            return [clean(v) for v in payload if clean(v)]
    except Exception:
        pass
    return [text]


def json_array(values: Iterable[Any]) -> str:
    return json.dumps(sorted(dict.fromkeys(clean(v) for v in values if clean(v))), ensure_ascii=False)


def stable_hash(payload: Mapping[str, Any]) -> str:
    body = json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str, separators=(",", ":"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()

def _finite_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if pd.isna(number):
        return None
    return number


def _unanimous_numeric(rows: list[Mapping[str, Any]], field: str) -> tuple[float | None, str]:
    values = [_finite_float(row.get(field)) for row in rows]
    values = [value for value in values if value is not None]
    if not values:
        return None, "NOT_AVAILABLE"
    unique = sorted(set(values))
    if len(unique) == 1:
        return unique[0], "UNANIMOUS_SCALAR_PROJECTION"
    return None, "MULTIPLE_VALUES_PRESERVED_AS_VECTOR"


def _packet_context_json(rows: list[Mapping[str, Any]]) -> str:
    payloads: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in rows:
        packet_id = clean(row.get("packet_id"))
        if not packet_id or packet_id in seen:
            continue
        seen.add(packet_id)
        payload = {
            "packet_id": packet_id,
            "pattern_id": clean(row.get("pattern_id")),
            "family_id": clean(row.get("family_id")),
        }
        for field in PACKET_CONTEXT_COPY_FIELDS:
            value = row.get(field)
            if field in {"joint_support_score", "joint_confidence_score"}:
                payload[field] = _finite_float(value)
            elif field.startswith("ready_for_") or field in {"pressure_anchor_eligible", "temporal_pressure_authorized"}:
                payload[field] = boolish(value)
            else:
                payload[field] = value
        payloads.append(payload)
    return json.dumps(payloads, ensure_ascii=False, sort_keys=True, default=str)



def canonical_source(row: Mapping[str, Any]) -> str:
    return clean(row.get("source_family")) or clean(row.get("source"))


def canonical_wave(row: Mapping[str, Any]) -> str:
    return clean(row.get("canonical_wave")) or clean(row.get("wave"))


def _scope_matches(left: Mapping[str, Any], right: Mapping[str, Any]) -> bool:
    return (
        canonical_source(left).casefold() == canonical_source(right).casefold()
        and canonical_wave(left).casefold() == canonical_wave(right).casefold()
        and clean(left.get("country_code")).casefold() == clean(right.get("country_code")).casefold()
    )


def _packet_status_lookup(certified: pd.DataFrame, review: pd.DataFrame, candidate: pd.DataFrame) -> dict[str, dict[str, Any]]:
    lookup: dict[str, dict[str, Any]] = {}
    for lane, frame in (("candidate", candidate), ("review", review), ("certified", certified)):
        if frame.empty or "packet_id" not in frame.columns:
            continue
        for row in frame.to_dict("records"):
            pid = clean(row.get("packet_id"))
            if not pid:
                continue
            current = lookup.get(pid, {})
            if lane == "certified" or not current:
                current = dict(row)
            current["v552j_joint_context_lane"] = lane
            current["v551j_certification_status"] = clean(row.get("certification_status")) or (
                "CERTIFIED" if lane == "certified" else "REVIEW_REQUIRED" if lane == "review" else "CANDIDATE"
            )
            lookup[pid] = current
    return lookup


def _component_link_status(component: Mapping[str, Any], pressure: Mapping[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    distribution = clean(component.get("v551_empirical_distribution_id"))
    if not distribution or distribution != clean(pressure.get("empirical_distribution_id")):
        reasons.append("empirical_distribution_id_mismatch")
    if not _scope_matches(component, pressure):
        reasons.append("scope_mismatch")

    source_atom_ids = set(parse_json_array(pressure.get("source_atom_ids_json")))
    source_atom_hashes = set(parse_json_array(pressure.get("source_atom_contract_hashes_json")))
    source_measurement_hashes = set(parse_json_array(pressure.get("source_measurement_contract_hashes_json")))
    component_atom_id = clean(component.get("v551_atom_id"))
    component_atom_hash = clean(component.get("v551_atom_contract_hash"))
    component_measurement_hash = clean(component.get("v551_measurement_contract_hash"))
    if source_atom_ids and component_atom_id not in source_atom_ids:
        reasons.append("atom_id_mismatch")
    if source_atom_hashes and component_atom_hash not in source_atom_hashes:
        reasons.append("atom_contract_hash_mismatch")
    if source_measurement_hashes and component_measurement_hash not in source_measurement_hashes:
        reasons.append("measurement_contract_hash_mismatch")
    if not clean(component.get("packet_id")) or not clean(component.get("component_id")):
        reasons.append("missing_packet_or_component_identity")
    if reasons:
        return "NOT_LINKED", reasons
    return "EXACT_COMPONENT_TO_PRESSURE_LINK", []


def _resolve_structural_fact(pressure: Mapping[str, Any], structural_facts: pd.DataFrame) -> tuple[dict[str, Any], str]:
    if structural_facts.empty:
        return {}, "MISSING_STRUCTURAL_FACT_INDEX"
    frame = structural_facts.copy()
    distribution = clean(pressure.get("empirical_distribution_id"))
    if "empirical_distribution_id" in frame.columns:
        frame = frame[frame["empirical_distribution_id"].astype(str).eq(distribution)]
    if not frame.empty:
        frame = frame[
            frame.apply(lambda r: _scope_matches(r.to_dict(), pressure), axis=1)
        ]
    pressure_id = clean(pressure.get("v552_pressure_observation_id"))
    if not frame.empty and "source_pressure_observation_ids_json" in frame.columns and pressure_id:
        exact = frame[frame["source_pressure_observation_ids_json"].map(lambda v: pressure_id in parse_json_array(v))]
        if len(exact) == 1:
            return exact.iloc[0].to_dict(), "EXACT_PRESSURE_OBSERVATION_FACT_MATCH"
        if len(exact) > 1:
            return {}, "AMBIGUOUS_PRESSURE_OBSERVATION_FACT_MATCH"
    if len(frame) == 1:
        return frame.iloc[0].to_dict(), "EXACT_DISTRIBUTION_SCOPE_FACT_MATCH"
    if frame.empty:
        return {}, "NO_STRUCTURAL_FACT_MATCH"
    return {}, "AMBIGUOUS_STRUCTURAL_FACT_MATCH"


def _resolve_temporal_source(fact: Mapping[str, Any], temporal_sources: pd.DataFrame) -> tuple[dict[str, Any], str]:
    fact_id = clean(fact.get("v552_structural_fact_id"))
    if not fact_id:
        return {}, "NO_STRUCTURAL_FACT_ID"
    if temporal_sources.empty or "v552_structural_fact_id" not in temporal_sources.columns:
        return {}, "MISSING_TEMPORAL_KEY_SOURCE_INDEX"
    matched = temporal_sources[temporal_sources["v552_structural_fact_id"].astype(str).eq(fact_id)]
    if len(matched) == 1:
        return matched.iloc[0].to_dict(), "EXACT_STRUCTURAL_FACT_TEMPORAL_KEY_MATCH"
    if matched.empty:
        return {}, "NO_TEMPORAL_KEY_SOURCE_MATCH"
    return {}, "AMBIGUOUS_TEMPORAL_KEY_SOURCE_MATCH"


def build_exact_v552j_integration(
    *,
    run_id: str,
    pressure_handoff: pd.DataFrame,
    components: pd.DataFrame,
    certified_packets: pd.DataFrame,
    review_packets: pd.DataFrame,
    candidate_packets: pd.DataFrame,
    structural_facts: pd.DataFrame,
    temporal_sources: pd.DataFrame,
) -> dict[str, Any]:
    """Build exact pressure-primary V552J outputs from already-loaded artifacts."""
    packet_lookup = _packet_status_lookup(certified_packets, review_packets, candidate_packets)
    link_rows: list[dict[str, Any]] = []
    linkage_audit_rows: list[dict[str, Any]] = []
    pressure_rows: list[dict[str, Any]] = []
    conservation_rows: list[dict[str, Any]] = []

    if pressure_handoff.empty:
        readiness = {
            "run_id": run_id,
            "status": "BLOCKED_V552J_MISSING_V552_PRESSURE_HANDOFF",
            "adapter_preflight_ready": False,
            "ready_for_v553_probe": False,
            "ready_for_v553_temporal_field": False,
            "ready_for_runtime_consumption": False,
            "pressure_observation_rows": 0,
            "exact_link_rows": 0,
            "certified_link_rows": 0,
            "review_link_rows": 0,
            "unlinked_pressure_rows": 0,
            "pressure_conservation_violation_count": 0,
            "missing_required_inputs_json": json.dumps(["v552_to_v552j_pressure_observation_handoff_index"]),
            "created_at": utc_now(),
            "schema_version": V552J_EXACT_SCHEMA_VERSION,
            "compiler_version": V552J_EXACT_COMPILER_VERSION,
        }
        empty = pd.DataFrame()
        return {
            "pressure_observation_index": empty,
            "joint_context_link_index": empty,
            "component_linkage_audit": empty,
            "certified_link_index": empty,
            "review_link_index": empty,
            "unlinked_pressure_index": empty,
            "pressure_conservation_audit": empty,
            "v553_input_index": empty,
            "readiness": readiness,
        }

    component_records = components.to_dict("records") if not components.empty else []
    for pressure in pressure_handoff.to_dict("records"):
        pressure_id = clean(pressure.get("v552_pressure_observation_id"))
        distribution = clean(pressure.get("empirical_distribution_id"))
        candidate_components = [
            comp for comp in component_records
            if clean(comp.get("v551_empirical_distribution_id")) == distribution
        ]
        exact_links: list[dict[str, Any]] = []
        for component in candidate_components:
            link_status, reasons = _component_link_status(component, pressure)
            packet_id = clean(component.get("packet_id"))
            packet = packet_lookup.get(packet_id, {})
            lane = clean(packet.get("v552j_joint_context_lane")) or "candidate"
            certification = clean(packet.get("v551j_certification_status"))
            linkage_audit_rows.append({
                "run_id": run_id,
                "v552_pressure_observation_id": pressure_id,
                "empirical_distribution_id": distribution,
                "packet_id": packet_id,
                "component_id": clean(component.get("component_id")),
                "joint_context_lane": lane,
                "link_status": link_status,
                "reason_codes_json": json_array(reasons),
                "created_at": utc_now(),
                "schema_version": V552J_EXACT_SCHEMA_VERSION,
                "compiler_version": V552J_EXACT_COMPILER_VERSION,
            })
            if link_status != "EXACT_COMPONENT_TO_PRESSURE_LINK":
                continue
            certified = lane == "certified" or certification.upper().startswith("CERTIFIED")
            link_id = "v552jlink__" + stable_hash({
                "pressure": pressure_id,
                "packet": packet_id,
                "component": clean(component.get("component_id")),
            })[:24]
            row = {
                "run_id": run_id,
                "v552j_link_id": link_id,
                "v552_pressure_observation_id": pressure_id,
                "pressure_observation_identity_hash": clean(pressure.get("pressure_observation_identity_hash")),
                "empirical_distribution_id": distribution,
                "packet_id": packet_id,
                "pattern_id": clean(component.get("pattern_id")),
                "family_id": clean(component.get("family_id")),
                "component_id": clean(component.get("component_id")),
                "component_contract_hash": clean(component.get("component_contract_hash")),
                "v551_atom_id": clean(component.get("v551_atom_id")),
                "v551_atom_contract_hash": clean(component.get("v551_atom_contract_hash")),
                "v551_measurement_contract_hash": clean(component.get("v551_measurement_contract_hash")),
                "source_family": canonical_source(pressure),
                "canonical_wave": canonical_wave(pressure),
                "country_code": clean(pressure.get("country_code")),
                "joint_context_lane": "certified" if certified else "review",
                "v551j_certification_status": certification,
                "exact_link_status": link_status,
                "link_reason_codes_json": json_array(reasons),
                "certified_joint_context": certified,
                "review_joint_context": not certified,
                **{field: packet.get(field) for field in PACKET_CONTEXT_COPY_FIELDS},
                "created_at": utc_now(),
                "schema_version": V552J_EXACT_SCHEMA_VERSION,
                "compiler_version": V552J_EXACT_COMPILER_VERSION,
            }
            exact_links.append(row)
            link_rows.append(row)

        fact, fact_status = _resolve_structural_fact(pressure, structural_facts)
        temporal, temporal_status = _resolve_temporal_source(fact, temporal_sources)
        certified_links = [r for r in exact_links if r["certified_joint_context"]]
        review_links = [r for r in exact_links if r["review_joint_context"]]
        pressure_context_id = "v552jpressure__" + stable_hash({
            "run_id": run_id,
            "pressure": pressure_id,
            "measurement": clean(pressure.get("pressure_measurement_hash")),
        })[:24]
        support_score, support_projection_status = _unanimous_numeric(exact_links, "joint_support_score")
        confidence_score, confidence_projection_status = _unanimous_numeric(exact_links, "joint_confidence_score")
        value_status = "PRESERVED_IDENTICALLY"
        pressure_row = {
            "run_id": run_id,
            "v552j_pressure_context_id": pressure_context_id,
            **{field: pressure.get(field) for field in PRESSURE_COPY_FIELDS},
            "source": clean(pressure.get("source")) or canonical_source(pressure),
            "source_family": canonical_source(pressure),
            "wave": clean(pressure.get("wave")) or canonical_wave(pressure),
            "canonical_wave": canonical_wave(pressure),
            "country_code": clean(pressure.get("country_code")),
            "question_id": clean(pressure.get("question_id")),
            "var_code": clean(pressure.get("var_code")),
            "semantic_identity_signature": clean(pressure.get("semantic_identity_signature")),
            "structural_identity_signature": clean(pressure.get("structural_identity_signature")),
            "response_scale_signature": clean(pressure.get("response_scale_signature")),
            "relation_axis_id": clean(fact.get("relation_axis_id")) or clean(pressure.get("relation_axis_id")),
            "target_entity_id": clean(fact.get("target_entity_id")) or clean(pressure.get("target_entity_id")),
            "driver_facet_id": clean(fact.get("driver_facet_id")) or clean(pressure.get("driver_facet_id")),
            "structural_channel_id": clean(fact.get("structural_channel_id")),
            "horizon_constraint_id": clean(fact.get("horizon_constraint_id")),
            "semantic_signature": clean(fact.get("semantic_signature")) or clean(pressure.get("semantic_identity_signature")),
            "source_v552_structural_fact_id": clean(fact.get("v552_structural_fact_id")),
            "source_v552_temporal_key_source_id": clean(temporal.get("v552_temporal_key_source_id")),
            "structural_fact_match_status": fact_status,
            "temporal_key_match_status": temporal_status,
            "certified_joint_packet_count": len({r["packet_id"] for r in certified_links}),
            "certified_joint_component_count": len(certified_links),
            "certified_joint_packet_ids_json": json_array(r["packet_id"] for r in certified_links),
            "certified_joint_component_ids_json": json_array(r["component_id"] for r in certified_links),
            "review_joint_packet_count": len({r["packet_id"] for r in review_links}),
            "review_joint_component_count": len(review_links),
            "review_joint_packet_ids_json": json_array(r["packet_id"] for r in review_links),
            "review_joint_component_ids_json": json_array(r["component_id"] for r in review_links),
            "joint_context_status": (
                "CERTIFIED_JOINT_CONTEXT_ATTACHED" if certified_links
                else "REVIEW_JOINT_CONTEXT_ATTACHED" if review_links
                else "NO_JOINT_CONTEXT_MATCH"
            ),
            "joint_context_packet_contracts_json": _packet_context_json(exact_links),
            "joint_support_scores_json": json.dumps(sorted({
                value for value in (_finite_float(r.get("joint_support_score")) for r in exact_links) if value is not None
            })),
            "joint_confidence_scores_json": json.dumps(sorted({
                value for value in (_finite_float(r.get("joint_confidence_score")) for r in exact_links) if value is not None
            })),
            "joint_evidence_authority_statuses_json": json_array(r.get("joint_evidence_authority_status") for r in exact_links),
            "joint_directionality_authority_statuses_json": json_array(r.get("joint_directionality_authority_status") for r in exact_links),
            "joint_support_score": support_score,
            "joint_support_score_projection_status": support_projection_status,
            "joint_confidence_score": confidence_score,
            "joint_confidence_score_projection_status": confidence_projection_status,
            "pressure_value_conservation_status": value_status,
            "v552j_pressure_linkage_eligible": boolish(pressure.get("v552j_pressure_linkage_eligible")),
            "ready_for_v553_probe": bool(clean(fact.get("v552_structural_fact_id"))) and boolish(pressure.get("v552j_pressure_linkage_eligible")),
            "ready_for_v553_temporal_field": False,
            "ready_for_runtime_consumption": False,
            "created_at": utc_now(),
            "schema_version": V552J_EXACT_SCHEMA_VERSION,
            "compiler_version": V552J_EXACT_COMPILER_VERSION,
        }
        pressure_rows.append(pressure_row)
        for field in PRESSURE_COPY_FIELDS:
            left = pressure.get(field)
            right = pressure_row.get(field)
            same = (pd.isna(left) and pd.isna(right)) if not isinstance(left, (list, dict)) else left == right
            if not same:
                try:
                    same = left == right
                except Exception:
                    same = False
            conservation_rows.append({
                "run_id": run_id,
                "v552_pressure_observation_id": pressure_id,
                "field_name": field,
                "source_value": left,
                "v552j_value": right,
                "conservation_status": "PRESERVED_IDENTICALLY" if bool(same) else "ILLEGITIMATELY_TRANSFORMED",
                "created_at": utc_now(),
                "schema_version": V552J_EXACT_SCHEMA_VERSION,
                "compiler_version": V552J_EXACT_COMPILER_VERSION,
            })

    pressure_df = pd.DataFrame(pressure_rows)
    links_df = pd.DataFrame(link_rows)
    linkage_audit_df = pd.DataFrame(linkage_audit_rows)
    conservation_df = pd.DataFrame(conservation_rows)
    certified_df = links_df[links_df.get("certified_joint_context", pd.Series(dtype=bool)).fillna(False).astype(bool)].copy() if not links_df.empty else links_df.copy()
    review_df = links_df[links_df.get("review_joint_context", pd.Series(dtype=bool)).fillna(False).astype(bool)].copy() if not links_df.empty else links_df.copy()
    unlinked_df = pressure_df[pressure_df.get("joint_context_status", pd.Series(dtype=str)).astype(str).eq("NO_JOINT_CONTEXT_MATCH")].copy()

    v553_rows: list[dict[str, Any]] = []
    for row in pressure_df.to_dict("records"):
        input_id = "v553input__" + stable_hash({
            "pressure": row.get("v552_pressure_observation_id"),
            "measurement": row.get("pressure_measurement_hash"),
        })[:24]
        v553_rows.append({
            "run_id": run_id,
            "v553_input_id": input_id,
            "v552j_packet_id": row.get("v552j_pressure_context_id"),
            "packet_id": (parse_json_array(row.get("certified_joint_packet_ids_json")) or parse_json_array(row.get("review_joint_packet_ids_json")) or [""])[0],
            "packet_class": "v552_pressure_observation_with_joint_context" if row.get("joint_context_status") != "NO_JOINT_CONTEXT_MATCH" else "v552_pressure_observation",
            "source": row.get("source"),
            "wave": row.get("wave"),
            "canonical_wave": row.get("canonical_wave"),
            "country_code": row.get("country_code"),
            "source_v552_artifact": "v552_to_v552j_pressure_observation_handoff_index",
            "source_v552_pressure_observation_id": row.get("v552_pressure_observation_id"),
            "source_v552_pressure_observation_identity_hash": row.get("pressure_observation_identity_hash"),
            "source_v552_structural_fact_id": row.get("source_v552_structural_fact_id"),
            "source_v552_structural_fact_ids_json": json_array([row.get("source_v552_structural_fact_id")]),
            "source_v552_structural_fact_ids_diagnostic_json": json_array([row.get("source_v552_structural_fact_id")]),
            "source_v552_temporal_key_source_id": row.get("source_v552_temporal_key_source_id"),
            "source_v552_temporal_key_source_ids_json": json_array([row.get("source_v552_temporal_key_source_id")]),
            "source_v552_structural_fact_status": row.get("structural_fact_match_status"),
            "source_v552_structural_fact_lane": "primary_pressure_observation",
            "source_v552_structural_fact_grain": "one_exact_v552_pressure_observation",
            "structural_dimension_status": "RESOLVED" if clean(row.get("source_v552_structural_fact_id")) else "BLOCKED",
            "structural_dimension_blocker_reason": "" if clean(row.get("source_v552_structural_fact_id")) else row.get("structural_fact_match_status"),
            "relation_axis_id": row.get("relation_axis_id"),
            "target_entity_id": row.get("target_entity_id"),
            "driver_facet_id": row.get("driver_facet_id"),
            "structural_channel_id": row.get("structural_channel_id"),
            "horizon_constraint_id": row.get("horizon_constraint_id"),
            "semantic_signature": row.get("semantic_signature"),
            "empirical_distribution_id": row.get("empirical_distribution_id"),
            "component_response_surface_signature": row.get("component_response_surface_signature"),
            "response_surface_completeness_status": row.get("response_surface_completeness_status"),
            "pressure_measure_class": row.get("pressure_measure_class"),
            "pressure_score": row.get("pressure_score"),
            "pressure_score_status": row.get("pressure_score_status"),
            "pressure_formula_id": row.get("pressure_formula_id"),
            "pressure_formula_version": row.get("pressure_formula_version"),
            "pressure_scale_id": row.get("pressure_scale_id"),
            "pressure_measurement_hash": row.get("pressure_measurement_hash"),
            "v552_structural_match_status": row.get("structural_fact_match_status"),
            "v552_structural_match_score": 1.0 if clean(row.get("source_v552_structural_fact_id")) else 0.0,
            "v552_structural_match_reason": row.get("structural_fact_match_status"),
            "matched_fact_count": 1 if clean(row.get("source_v552_structural_fact_id")) else 0,
            "broad_match_count": 0,
            "temporal_key_basis": clean(row.get("source_v552_temporal_key_source_id")),
            "temporal_key_candidate_status": row.get("temporal_key_match_status"),
            "temporal_key_blocker_reason": "" if clean(row.get("source_v552_temporal_key_source_id")) else row.get("temporal_key_match_status"),
            "fallback_permission_profile_key": "",
            "packet_ready_for_v553": bool(row.get("ready_for_v553_probe")),
            "structural_dimensions_resolved_for_v553": bool(clean(row.get("source_v552_structural_fact_id"))),
            "ready_for_v553_probe": bool(row.get("ready_for_v553_probe")),
            "ready_for_v553_temporal_field": False,
            "read_permission": "pressure_observation_plus_optional_joint_context",
            "must_temporalize": True,
            "single_wave_probe_allowed": bool(row.get("ready_for_v553_probe")),
            "temporal_field_allowed": False,
            "temporal_anchor_required": True,
            "comparability_required": True,
            "comparability_status": "not_evaluated_by_v552j",
            "certification_score": 1.0 if row.get("certified_joint_packet_count", 0) else 0.0,
            "certification_score_basis": "certified_joint_context_present",
            "support_score": row.get("joint_support_score"),
            "support_score_projection_status": row.get("joint_support_score_projection_status"),
            "directionality_score": 1.0 if row.get("pressure_score_status") in {"OBSERVED_NONZERO", "OBSERVED_ZERO"} else 0.0,
            "directionality_score_basis": "v552_pressure_observation_status",
            "authority_score": 1.0 if bool(row.get("v552j_pressure_linkage_eligible")) else 0.0,
            "authority_score_basis": "v552_pressure_linkage_eligibility",
            "comparability_score": None,
            "confidence_score": row.get("joint_confidence_score"),
            "confidence_score_projection_status": row.get("joint_confidence_score_projection_status"),
            "readiness_score": 1.0 if row.get("ready_for_v553_probe") else 0.0,
            "joint_context_packet_contracts_json": row.get("joint_context_packet_contracts_json"),
            "joint_evidence_authority_statuses_json": row.get("joint_evidence_authority_statuses_json"),
            "joint_directionality_authority_statuses_json": row.get("joint_directionality_authority_statuses_json"),
            "constraint_payload_ref": row.get("v552j_pressure_context_id"),
            "uncertainty_payload_ref": "",
            "absence_payload_ref": "",
            "blocking_reason": "" if row.get("ready_for_v553_probe") else row.get("structural_fact_match_status"),
            "required_temporal_context_json": json.dumps(["cross_wave_comparability", "temporal_key_resolution"]),
            "ready_for_v553": bool(row.get("ready_for_v553_probe")),
            "ready_for_runtime_consumption": False,
            "joint_context_status": row.get("joint_context_status"),
            "certified_joint_packet_ids_json": row.get("certified_joint_packet_ids_json"),
            "review_joint_packet_ids_json": row.get("review_joint_packet_ids_json"),
            "created_at": utc_now(),
            "schema_version": V552J_EXACT_SCHEMA_VERSION,
            "compiler_version": V552J_EXACT_COMPILER_VERSION,
        })
    v553_df = pd.DataFrame(v553_rows)
    violations = int((conservation_df.get("conservation_status", pd.Series(dtype=str)) != "PRESERVED_IDENTICALLY").sum()) if not conservation_df.empty else 0
    structural_gaps = int(pressure_df.get("source_v552_structural_fact_id", pd.Series(dtype=str)).fillna("").astype(str).eq("").sum())
    status = (
        "BLOCKED_V552J_PRESSURE_CONSERVATION_FAILURE" if violations
        else "READY_V552J_EXACT_PRESSURE_HANDOFF" if not structural_gaps
        else "PARTIAL_READY_V552J_EXACT_PRESSURE_HANDOFF_WITH_STRUCTURAL_GAPS"
    )
    readiness = {
        "run_id": run_id,
        "status": status,
        "structural_handoff_status": status,
        "adapter_preflight_ready": bool(len(pressure_df)) and not violations,
        "single_wave_structural_ready": bool(len(pressure_df)) and not violations and structural_gaps == 0,
        "v553_probe_ready": bool(len(v553_df)) and v553_df.get("ready_for_v553_probe", pd.Series(dtype=bool)).fillna(False).astype(bool).any() and not violations,
        "v553_temporal_field_ready": False,
        "v552_context_profile": "exact_pressure_primary",
        "runtime_app_ready": False,
        "ready_for_v553": bool(len(v553_df)) and v553_df.get("ready_for_v553", pd.Series(dtype=bool)).fillna(False).astype(bool).any() and not violations,
        "ready_for_runtime_consumption": False,
        "runtime_safe_for_app": False,
        "ready_for_v553_probe": bool(len(v553_df)) and v553_df.get("ready_for_v553_probe", pd.Series(dtype=bool)).fillna(False).astype(bool).any() and not violations,
        "ready_for_v553_temporal_field": False,
        "pressure_observation_rows": int(len(pressure_df)),
        "packet_rows": int(len(pressure_df)),
        "exact_link_rows": int(len(links_df)),
        "component_linkage_audit_rows": int(len(linkage_audit_df)),
        "rejected_component_link_rows": int((
            linkage_audit_df.get("link_status", pd.Series(dtype=str)).astype(str)
            != "EXACT_COMPONENT_TO_PRESSURE_LINK"
        ).sum()) if not linkage_audit_df.empty else 0,
        "certified_link_rows": int(len(certified_df)),
        "review_link_rows": int(len(review_df)),
        "unlinked_pressure_rows": int(len(unlinked_df)),
        "pressure_conservation_violation_count": violations,
        "structural_fact_gap_count": structural_gaps,
        "missing_required_inputs_json": "[]",
        "optional_inputs_supplied_json": json.dumps(["v551j_joint_context"] if not components.empty else []),
        "optional_inputs_missing_json": json.dumps([] if not components.empty else ["v551j_joint_component_index"]),
        "runtime_packets_written": False,
        "persona_fields_written": False,
        "forbidden_outputs_written": False,
        "created_at": utc_now(),
        "schema_version": V552J_EXACT_SCHEMA_VERSION,
        "compiler_version": V552J_EXACT_COMPILER_VERSION,
    }
    return {
        "pressure_observation_index": pressure_df,
        "joint_context_link_index": links_df,
        "component_linkage_audit": linkage_audit_df,
        "certified_link_index": certified_df,
        "review_link_index": review_df,
        "unlinked_pressure_index": unlinked_df,
        "pressure_conservation_audit": conservation_df,
        "v553_input_index": v553_df,
        "readiness": readiness,
    }


def validate_exact_v552j_integration(outputs: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    pressure = outputs.get("pressure_observation_index", pd.DataFrame())
    conservation = outputs.get("pressure_conservation_audit", pd.DataFrame())
    v553 = outputs.get("v553_input_index", pd.DataFrame())
    readiness = outputs.get("readiness", {})
    if pressure.empty:
        issues.append("missing_pressure_observation_rows")
    if not conservation.empty and conservation["conservation_status"].astype(str).ne("PRESERVED_IDENTICALLY").any():
        issues.append("pressure_value_conservation_failure")
    if len(v553) != len(pressure):
        issues.append(f"v553_row_grain_mismatch:{len(v553)}!={len(pressure)}")
    if not pressure.empty and pressure["v552_pressure_observation_id"].astype(str).duplicated().any():
        issues.append("duplicate_pressure_observation_id")
    if not v553.empty:
        for field in ("pressure_score", "pressure_measurement_hash", "empirical_distribution_id", "source_v552_pressure_observation_id"):
            if field not in v553.columns:
                issues.append(f"missing_v553_field:{field}")
        if "ready_for_runtime_consumption" in v553.columns and v553["ready_for_runtime_consumption"].fillna(False).astype(bool).any():
            issues.append("forbidden_runtime_authorization")
    if readiness.get("ready_for_v553_temporal_field"):
        issues.append("v552j_may_not_grant_temporal_field_authority")
    return issues


__all__ = [
    "build_exact_v552j_integration",
    "validate_exact_v552j_integration",
    "PRESSURE_COPY_FIELDS",
    "V552J_EXACT_SCHEMA_VERSION",
    "V552J_EXACT_COMPILER_VERSION",
]
