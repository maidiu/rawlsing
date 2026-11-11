#!/usr/bin/env python3
"""Completion-grade V554 seed affordance contract builder.

This layer turns V553 temporal pressure and harmonization evidence into bounded
seed affordance ledgers, explicit absence/blocker/prohibition registers, and a
lawful V555 handoff index. It does not generate persona content.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from data.ddm_build_copy.ddm_v550_manifest import utc_now
from data.ddm_build_copy.ddm_v551j_io import ensure_output_dirs, read_table, write_frame_artifact, write_json_artifact
from data.ddm_build_copy.ddm_v5_build_standard import build_layer_build_record
from data.ddm_build_copy.ddm_path_utils import repo_relative_path_text
from data.ddm_build_copy.ddm_survey_identity import (
    canonical_country_code,
    canonical_family_key,
    canonical_family_label,
    require_survey_identity,
)

V554_SCHEMA_VERSION = "v0.1"
V554_COMPILER_VERSION = "v554_seed_contract_0.1"

_FORBIDDEN_PERSONA_TERMS = [
    "name",
    "voice",
    "dialogue",
    "quote",
    "memory",
    "autobiography",
    "childhood_event",
    "parent_belief_as_fact",
    "household_story",
    "carrier_membership_as_fact",
    "enneagram_type",
    "wound_vector",
    "striving_object",
    "pressureflow_route",
    "chat_prompt",
]


def _clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    return str(value).strip()


def _bounded_score(value: float, default: float = 0.0) -> float:
    try:
        score = float(value)
    except Exception:
        score = default
    if pd.isna(score):
        score = default
    return max(0.0, min(1.0, score))


def _json_list(values: list[Any]) -> str:
    return json.dumps([_clean(value) for value in values if _clean(value)], sort_keys=True)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _load_optional_frame(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return read_table(path)
    except Exception:
        return pd.DataFrame()


def _json_object(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    text = _clean(value)
    if not text:
        return {}
    try:
        payload = json.loads(text)
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _first_nonempty(values: list[Any], default: str = "") -> str:
    for value in values:
        text = _clean(value)
        if text:
            return text
    return default


def _wave_year_from_row(row: dict[str, Any]) -> int:
    for key in ("year", "temporal_year", "wave_year", "wave"):
        text = _clean(row.get(key))
        if text:
            try:
                return int(text)
            except Exception:
                continue
    return 0


def _seed_permission(seed_readiness_status: str) -> str:
    if seed_readiness_status == "ready_for_v555_mediation":
        return "positive_mediation_required"
    if seed_readiness_status == "ready_with_constraints":
        return "reviewable_mediation_context"
    if seed_readiness_status == "reviewable_only":
        return "reviewable_mediation_context"
    if seed_readiness_status == "conflict":
        return "conflict_stop"
    if seed_readiness_status == "blocker_only":
        return "blocker_only"
    return "absence_only"


def _forbidden_uses() -> list[str]:
    return [
        "full_person",
        "voice",
        "autobiography",
        "parent_story",
        "household_story",
        "carrier_ideology",
        "enneagram_type",
        "belief_as_fact",
        "pressureflow_route",
        "runtime_prompt",
        "wound",
        "striving_object",
    ]


def _seed_row(
    *,
    run_id: str,
    source_family: str,
    source_country: str,
    source_wave_set: str,
    seed_type: str,
    seed_domain: str,
    seed_scope: str,
    seed_target_layer: str,
    source_pressure_ids: list[str],
    source_absence_ids: list[str],
    source_contradiction_ids: list[str],
    source_authority_lanes: list[str],
    temporal_status: str,
    interpolation_status: str,
    seed_strength_score: float,
    seed_confidence_score: float,
    seed_specificity_score: float,
    seed_certifiability_score: float,
    seed_readiness_status: str,
    requires_demographic_resolution: bool,
    requires_regional_resolution: bool,
    requires_household_mediation: bool,
    requires_family_mediation: bool,
    requires_carrier_mediation: bool,
    requires_orientation_resolution: bool,
    requires_pressureflow_mediation: bool,
    known_absences: list[str],
    stop_reasons: list[str],
    generated_content_status: str = "no_generated_person_content",
) -> dict[str, Any]:
    return {
        "seed_affordance_id": f"{run_id}__{seed_type}__{seed_scope}".replace(" ", "_"),
        "run_id": run_id,
        "source_family": source_family,
        "source_country": source_country,
        "source_wave_set": source_wave_set,
        "seed_type": seed_type,
        "seed_domain": seed_domain,
        "seed_scope": seed_scope,
        "seed_target_layer": seed_target_layer,
        "source_pressure_ids_json": _json_list(source_pressure_ids),
        "source_absence_ids_json": _json_list(source_absence_ids),
        "source_contradiction_ids_json": _json_list(source_contradiction_ids),
        "source_authority_lanes_json": _json_list(source_authority_lanes),
        "temporal_status": temporal_status,
        "interpolation_status": interpolation_status,
        "seed_strength_score": _bounded_score(seed_strength_score),
        "seed_confidence_score": _bounded_score(seed_confidence_score),
        "seed_specificity_score": _bounded_score(seed_specificity_score),
        "seed_certifiability_score": _bounded_score(seed_certifiability_score),
        "seed_readiness_status": seed_readiness_status,
        "seed_use_permission": _seed_permission(seed_readiness_status),
        "requires_demographic_resolution": bool(requires_demographic_resolution),
        "requires_regional_resolution": bool(requires_regional_resolution),
        "requires_household_mediation": bool(requires_household_mediation),
        "requires_family_mediation": bool(requires_family_mediation),
        "requires_carrier_mediation": bool(requires_carrier_mediation),
        "requires_orientation_resolution": bool(requires_orientation_resolution),
        "requires_pressureflow_mediation": bool(requires_pressureflow_mediation),
        "forbidden_downstream_uses_json": _json_list(_forbidden_uses()),
        "known_absences_json": _json_list(known_absences),
        "stop_reasons_json": _json_list(stop_reasons),
        "generated_content_status": generated_content_status,
        "runtime_use_class": "bounded_seed_affordance_only_not_persona",
        "created_at": utc_now(),
        "schema_version": V554_SCHEMA_VERSION,
        "compiler_version": V554_COMPILER_VERSION,
    }


def _build_seed_affordance_index(
    *,
    run_id: str,
    source_family: str,
    source_country: str,
    source_wave_set: str,
    v553_temporal_readiness: dict[str, Any],
    v553_harmonization_report: dict[str, Any],
    country_year_pressure_df: pd.DataFrame,
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    readiness_score = _bounded_score(float(v553_temporal_readiness.get("readiness_score", 0.0) or 0.0))
    harmonization_score = _bounded_score(float(v553_temporal_readiness.get("harmonization_score", 0.0) or 0.0))
    shared_lanes = [
        "v553_temporal_pressure_field",
        "v553_wave_harmonization_report",
        "v553_temporal_readiness_report",
    ]
    pressure_records = country_year_pressure_df.to_dict(orient="records") if not country_year_pressure_df.empty else []
    pressure_ids = []
    for row in pressure_records:
        year = _wave_year_from_row(row)
        pressure_ids.append(f"{source_country or source_family}:{year}")
        pressure_status = _clean(row.get("pressure_status")) or "ready_with_gaps"
        interpolation_method = _clean(row.get("interpolation_method")) or "unknown"
        pressure_distribution = _json_object(row.get("pressure_value_distribution"))
        pressure_value = _bounded_score(float(pressure_distribution.get("point_estimate", 0.0) or 0.0))
        confidence_penalty = _bounded_score(float(row.get("confidence_penalty", 0.0) or 0.0))
        if pressure_status == "anchor_derived":
            readiness = "ready_for_v555_mediation"
        elif pressure_status == "linear_interpolated":
            readiness = "ready_with_constraints"
        elif pressure_status == "cautious_interpolation_allowed":
            readiness = "reviewable_only"
        else:
            readiness = "blocker_only"
        rows.append(
            _seed_row(
                run_id=run_id,
                source_family=source_family,
                source_country=source_country,
                source_wave_set=source_wave_set,
                seed_type="regional_pressure_seed",
                seed_domain="country_year_structural_pressure",
                seed_scope=f"{source_country or source_family}:{year}",
                seed_target_layer="v555",
                source_pressure_ids=[f"{source_country or source_family}:{year}"],
                source_absence_ids=[f"absence::{year}"] if readiness != "ready_for_v555_mediation" else [],
                source_contradiction_ids=[f"contradiction::{year}"] if pressure_status != "anchor_derived" else [],
                source_authority_lanes=shared_lanes,
                temporal_status=pressure_status,
                interpolation_status=interpolation_method,
                seed_strength_score=pressure_value,
                seed_confidence_score=1.0 - confidence_penalty,
                seed_specificity_score=0.75,
                seed_certifiability_score=_bounded_score(pressure_value * (1.0 - confidence_penalty)),
                seed_readiness_status=readiness,
                requires_demographic_resolution=False,
                requires_regional_resolution=True,
                requires_household_mediation=False,
                requires_family_mediation=False,
                requires_carrier_mediation=False,
                requires_orientation_resolution=True,
                requires_pressureflow_mediation=False,
                known_absences=[
                    "household_signal_not_evidenced",
                    "carrier_signal_not_evidenced",
                ]
                if readiness != "ready_for_v555_mediation"
                else ["household_signal_not_evidenced", "carrier_signal_not_evidenced"],
                stop_reasons=[] if readiness == "ready_for_v555_mediation" else ["interpolated_or_reviewable_pressure"],
            )
        )

    seed_strength = _bounded_score(readiness_score * 0.75 + harmonization_score * 0.25)
    source_wave_pair_ids = [
        f"{_clean(item.get('prior_wave'))}->{_clean(item.get('current_wave'))}"
        for item in (v553_harmonization_report.get("wave_pair_evidence", []) or [])
        if isinstance(item, dict)
    ]
    seed_rows = [
        _seed_row(
            run_id=run_id,
            source_family=source_family,
            source_country=source_country,
            source_wave_set=source_wave_set,
            seed_type="demographic_position_seed",
            seed_domain="demographic_slice",
            seed_scope="demographic_slice_pending",
            seed_target_layer="v555",
            source_pressure_ids=pressure_ids,
            source_absence_ids=["missing_demographic_resolution"],
            source_contradiction_ids=[],
            source_authority_lanes=shared_lanes,
            temporal_status="structural",
            interpolation_status="not_applicable",
            seed_strength_score=seed_strength * 0.65,
            seed_confidence_score=seed_strength * 0.55,
            seed_specificity_score=0.30,
            seed_certifiability_score=seed_strength * 0.40,
            seed_readiness_status="reviewable_only",
            requires_demographic_resolution=True,
            requires_regional_resolution=False,
            requires_household_mediation=False,
            requires_family_mediation=False,
            requires_carrier_mediation=False,
            requires_orientation_resolution=True,
            requires_pressureflow_mediation=False,
            known_absences=["demographic_slice_not_resolved"],
            stop_reasons=["demographic_resolution_pending"],
        ),
        _seed_row(
            run_id=run_id,
            source_family=source_family,
            source_country=source_country,
            source_wave_set=source_wave_set,
            seed_type="national_pressure_seed",
            seed_domain="national_structural_pressure",
            seed_scope=source_country or "country_pending",
            seed_target_layer="v555",
            source_pressure_ids=pressure_ids,
            source_absence_ids=[],
            source_contradiction_ids=source_wave_pair_ids,
            source_authority_lanes=shared_lanes,
            temporal_status="harmonized",
            interpolation_status="mixed",
            seed_strength_score=seed_strength,
            seed_confidence_score=_bounded_score(harmonization_score * 0.9 + readiness_score * 0.1),
            seed_specificity_score=0.60,
            seed_certifiability_score=_bounded_score(seed_strength * 0.85),
            seed_readiness_status="ready_for_v555_mediation" if bool(v553_temporal_readiness.get("ready_for_v554")) else "ready_with_constraints",
            requires_demographic_resolution=False,
            requires_regional_resolution=True,
            requires_household_mediation=False,
            requires_family_mediation=False,
            requires_carrier_mediation=False,
            requires_orientation_resolution=True,
            requires_pressureflow_mediation=False,
            known_absences=[],
            stop_reasons=[] if bool(v553_temporal_readiness.get("ready_for_v554")) else ["v553_temporal_readiness_not_ready"],
        ),
        _seed_row(
            run_id=run_id,
            source_family=source_family,
            source_country=source_country,
            source_wave_set=source_wave_set,
            seed_type="class_status_seed",
            seed_domain="class_status_pressure",
            seed_scope="class_status_pending",
            seed_target_layer="v555",
            source_pressure_ids=pressure_ids,
            source_absence_ids=["missing_class_status_resolution"],
            source_contradiction_ids=source_wave_pair_ids,
            source_authority_lanes=shared_lanes,
            temporal_status="reviewable",
            interpolation_status="not_applicable",
            seed_strength_score=seed_strength * 0.55,
            seed_confidence_score=seed_strength * 0.45,
            seed_specificity_score=0.35,
            seed_certifiability_score=seed_strength * 0.35,
            seed_readiness_status="reviewable_only",
            requires_demographic_resolution=True,
            requires_regional_resolution=True,
            requires_household_mediation=False,
            requires_family_mediation=False,
            requires_carrier_mediation=False,
            requires_orientation_resolution=True,
            requires_pressureflow_mediation=False,
            known_absences=["class_status_not_resolved"],
            stop_reasons=["class_status_pending"],
        ),
        _seed_row(
            run_id=run_id,
            source_family=source_family,
            source_country=source_country,
            source_wave_set=source_wave_set,
            seed_type="household_mediation_requirement_seed",
            seed_domain="household_mediation",
            seed_scope="household_pending",
            seed_target_layer="v555",
            source_pressure_ids=pressure_ids,
            source_absence_ids=["missing_household_signal"],
            source_contradiction_ids=[],
            source_authority_lanes=shared_lanes,
            temporal_status="missing",
            interpolation_status="not_applicable",
            seed_strength_score=0.15,
            seed_confidence_score=0.10,
            seed_specificity_score=0.10,
            seed_certifiability_score=0.05,
            seed_readiness_status="blocker_only",
            requires_demographic_resolution=False,
            requires_regional_resolution=False,
            requires_household_mediation=True,
            requires_family_mediation=True,
            requires_carrier_mediation=False,
            requires_orientation_resolution=False,
            requires_pressureflow_mediation=False,
            known_absences=["household_signal_not_evidenced"],
            stop_reasons=["missing_household_signal"],
        ),
        _seed_row(
            run_id=run_id,
            source_family=source_family,
            source_country=source_country,
            source_wave_set=source_wave_set,
            seed_type="carrier_mediation_requirement_seed",
            seed_domain="carrier_mediation",
            seed_scope="carrier_pending",
            seed_target_layer="v555",
            source_pressure_ids=pressure_ids,
            source_absence_ids=["missing_carrier_signal"],
            source_contradiction_ids=[],
            source_authority_lanes=shared_lanes,
            temporal_status="missing",
            interpolation_status="not_applicable",
            seed_strength_score=0.12,
            seed_confidence_score=0.08,
            seed_specificity_score=0.10,
            seed_certifiability_score=0.05,
            seed_readiness_status="blocker_only",
            requires_demographic_resolution=False,
            requires_regional_resolution=False,
            requires_household_mediation=False,
            requires_family_mediation=False,
            requires_carrier_mediation=True,
            requires_orientation_resolution=False,
            requires_pressureflow_mediation=False,
            known_absences=["carrier_signal_not_evidenced"],
            stop_reasons=["missing_carrier_signal"],
        ),
        _seed_row(
            run_id=run_id,
            source_family=source_family,
            source_country=source_country,
            source_wave_set=source_wave_set,
            seed_type="temporal_contradiction_seed",
            seed_domain="temporal_contradiction",
            seed_scope=source_wave_set or "multi_wave_pending",
            seed_target_layer="v555",
            source_pressure_ids=pressure_ids,
            source_absence_ids=[],
            source_contradiction_ids=source_wave_pair_ids,
            source_authority_lanes=shared_lanes,
            temporal_status="contradictory" if source_wave_pair_ids else "unresolved",
            interpolation_status="not_applicable",
            seed_strength_score=0.40 if source_wave_pair_ids else 0.20,
            seed_confidence_score=0.35 if source_wave_pair_ids else 0.15,
            seed_specificity_score=0.30,
            seed_certifiability_score=0.25,
            seed_readiness_status="reviewable_only" if source_wave_pair_ids else "blocker_only",
            requires_demographic_resolution=False,
            requires_regional_resolution=True,
            requires_household_mediation=False,
            requires_family_mediation=False,
            requires_carrier_mediation=False,
            requires_orientation_resolution=True,
            requires_pressureflow_mediation=False,
            known_absences=["temporal_contradiction_not_resolved"] if not source_wave_pair_ids else [],
            stop_reasons=["temporal_contradiction_pending"] if not source_wave_pair_ids else [],
        ),
        _seed_row(
            run_id=run_id,
            source_family=source_family,
            source_country=source_country,
            source_wave_set=source_wave_set,
            seed_type="known_absence_seed",
            seed_domain="known_absence",
            seed_scope="upstream_absence_register",
            seed_target_layer="v555",
            source_pressure_ids=pressure_ids,
            source_absence_ids=["missing_demographic_resolution", "missing_household_signal", "missing_carrier_signal"],
            source_contradiction_ids=[],
            source_authority_lanes=shared_lanes,
            temporal_status="absence_preserved",
            interpolation_status="not_applicable",
            seed_strength_score=0.05,
            seed_confidence_score=0.05,
            seed_specificity_score=0.05,
            seed_certifiability_score=0.0,
            seed_readiness_status="blocker_only",
            requires_demographic_resolution=False,
            requires_regional_resolution=False,
            requires_household_mediation=False,
            requires_family_mediation=False,
            requires_carrier_mediation=False,
            requires_orientation_resolution=False,
            requires_pressureflow_mediation=False,
            known_absences=["known_absence_preserved"],
            stop_reasons=["absence_must_remain_visible"],
        ),
        _seed_row(
            run_id=run_id,
            source_family=source_family,
            source_country=source_country,
            source_wave_set=source_wave_set,
            seed_type="blocked_seed",
            seed_domain="blocked",
            seed_scope="upstream_blocked",
            seed_target_layer="v555",
            source_pressure_ids=pressure_ids,
            source_absence_ids=["upstream_conflict", "blocked_upstream_lane"],
            source_contradiction_ids=source_wave_pair_ids,
            source_authority_lanes=shared_lanes,
            temporal_status="blocked",
            interpolation_status="not_applicable",
            seed_strength_score=0.0,
            seed_confidence_score=0.0,
            seed_specificity_score=0.0,
            seed_certifiability_score=0.0,
            seed_readiness_status="blocker_only",
            requires_demographic_resolution=False,
            requires_regional_resolution=False,
            requires_household_mediation=False,
            requires_family_mediation=False,
            requires_carrier_mediation=False,
            requires_orientation_resolution=False,
            requires_pressureflow_mediation=False,
            known_absences=["blocked_upstream_lane"],
            stop_reasons=["upstream_conflict", "blocked_upstream_lane"],
        ),
    ]
    rows.extend(seed_rows)
    return pd.DataFrame(rows)


def _build_demographic_slice_contract(seed_df: pd.DataFrame, run_id: str) -> pd.DataFrame:
    fields = [
        "age",
        "sex",
        "race_ethnicity",
        "class_status",
        "education",
        "religious_affiliation",
        "region",
        "country",
    ]
    rows = []
    positive_ids = seed_df.loc[seed_df["seed_use_permission"] == "positive_mediation_required", "seed_affordance_id"].tolist()
    for field in fields:
        rows.append(
            {
                "slice_contract_id": f"{run_id}__demographic__{field}",
                "run_id": run_id,
                "slice_kind": "demographic",
                "slice_scope": field,
                "required_fields_json": _json_list([field]),
                "source_authority_lanes_json": _json_list(["v554_seed_affordance_index"]),
                "seed_affordance_ids_json": _json_list(positive_ids),
                "slice_readiness_status": "required",
                "slice_confidence_score": 0.75 if field in {"age", "sex", "region", "country"} else 0.55,
                "known_absences_json": _json_list([f"missing_{field}"]),
                "created_at": utc_now(),
                "schema_version": V554_SCHEMA_VERSION,
                "compiler_version": V554_COMPILER_VERSION,
            }
        )
    return pd.DataFrame(rows)


def _build_regional_slice_contract(seed_df: pd.DataFrame, run_id: str) -> pd.DataFrame:
    rows = []
    slices = [
        ("national", "national consensus slice"),
        ("subnational", "subnational/regional slice"),
        ("regional", "regional comparability slice"),
        ("urban_rural", "urban-rural slice"),
        ("locality_pending", "locality pending slice"),
    ]
    positive_ids = seed_df.loc[seed_df["seed_use_permission"] == "positive_mediation_required", "seed_affordance_id"].tolist()
    for key, label in slices:
        rows.append(
            {
                "slice_contract_id": f"{run_id}__regional__{key}",
                "run_id": run_id,
                "slice_kind": "regional",
                "slice_scope": key,
                "required_fields_json": _json_list([label]),
                "source_authority_lanes_json": _json_list(["v553_wave_harmonization_report", "v553_temporal_pressure_field"]),
                "seed_affordance_ids_json": _json_list(positive_ids),
                "slice_readiness_status": "required" if key != "locality_pending" else "unresolved",
                "slice_confidence_score": 0.70 if key in {"national", "regional"} else 0.45,
                "known_absences_json": _json_list([f"missing_{key}_resolution"]),
                "created_at": utc_now(),
                "schema_version": V554_SCHEMA_VERSION,
                "compiler_version": V554_COMPILER_VERSION,
            }
        )
    return pd.DataFrame(rows)


def _build_required_mediation_slot_index(seed_df: pd.DataFrame, run_id: str) -> pd.DataFrame:
    slots = [
        ("family_mediation", "family_mediation", False),
        ("household_mediation", "household_mediation", False),
        ("parent_transmission", "parent_transmission", True),
        ("co_parent_transmission", "co_parent_transmission", True),
        ("child_absorption_resistance", "child_absorption_resistance", True),
        ("carrier_institutional_mediation", "carrier_institutional_mediation", True),
        ("regional_locality_mediation", "regional_locality_mediation", True),
        ("school_work_church_neighborhood_media_party_mediation", "school_work_church_neighborhood_media_party_mediation", True),
    ]
    rows = []
    for slot, channel, may_generate_later in slots:
        rows.append(
            {
                "required_mediation_slot_id": f"{run_id}__slot__{slot}",
                "run_id": run_id,
                "slot_name": slot,
                "required_channel": channel,
                "required_channel_status": "unresolved",
                "source_seed_authority": "v554_seed_affordance_index",
                "source_temporal_authority": "v553_temporal_pressure_field",
                "known_absences_json": _json_list([f"missing_{channel}"]),
                "forbidden_v555_uses_json": _json_list(_forbidden_uses()),
                "requires_generation_ledger": True,
                "may_generate_later": may_generate_later,
                "created_at": utc_now(),
                "schema_version": V554_SCHEMA_VERSION,
                "compiler_version": V554_COMPILER_VERSION,
            }
        )
    return pd.DataFrame(rows)


def _build_absence_register(seed_df: pd.DataFrame, run_id: str) -> pd.DataFrame:
    absences = [
        ("missing_demographic_resolution", "demographic_slice", "v554_seed_affordance_index", "absence becomes blocker_only seed", "reviewable_mediation_context"),
        ("missing_regional_slice", "regional_slice", "v554_seed_affordance_index", "regional reduction stays unresolved", "reviewable_mediation_context"),
        ("missing_household_signal", "household_mediation", "v554_seed_affordance_index", "family mediation remains unresolved", "blocker_only"),
        ("missing_carrier_signal", "carrier_mediation", "v554_seed_affordance_index", "carrier mediation remains unresolved", "blocker_only"),
        ("missing_family_mediation_signal", "family_mediation", "v554_seed_affordance_index", "family mediation remains unresolved", "blocker_only"),
        ("missing_orientation_authority", "orientation_authority", "v554_seed_affordance_index", "orientation resolution cannot be invented", "reviewable_mediation_context"),
        ("missing_pressureflow_authority", "pressureflow_authority", "v554_seed_affordance_index", "pressure-flow not yet lawful", "reviewable_mediation_context"),
        ("interpolation_not_authorized", "interpolation", "v553_wave_harmonization_report", "interpolation preserved only as review context", "reviewable_mediation_context"),
    ]
    rows = []
    for absence_type, absence_scope, source_artifact, impact_seed, impact_v555 in absences:
        rows.append(
            {
                "absence_id": f"{run_id}__absence__{absence_type}",
                "run_id": run_id,
                "absence_domain": absence_type,
                "absence_scope": absence_scope,
                "source_layer": "v553/v554",
                "source_artifact": source_artifact,
                "absence_type": absence_type,
                "impact_on_seed": impact_seed,
                "impact_on_v555": impact_v555,
                "impact_on_v556": "pressureflow_authority_pending" if "pressureflow" in absence_type else "not_applicable",
                "impact_on_v557": "no_prompt_shape_change" if "voice" not in absence_type else "forbidden",
                "may_be_generated_later": absence_type not in {"missing_household_signal", "missing_carrier_signal", "interpolation_not_authorized"},
                "requires_generation_ledger": True,
                "created_at": utc_now(),
                "schema_version": V554_SCHEMA_VERSION,
                "compiler_version": V554_COMPILER_VERSION,
            }
        )
    return pd.DataFrame(rows)


def _build_blocker_ledger(seed_df: pd.DataFrame, run_id: str) -> pd.DataFrame:
    rows = []
    blocked = seed_df[seed_df["seed_use_permission"] == "blocker_only"].to_dict(orient="records")
    for row in blocked:
        rows.append(
            {
                "blocker_id": f"{run_id}__blocker__{row['seed_affordance_id']}",
                "run_id": run_id,
                "seed_candidate_id": row["seed_affordance_id"],
                "blocker_type": row["seed_type"],
                "blocker_reason": _first_nonempty(json.loads(row.get("stop_reasons_json", "[]")), "blocked"),
                "source_stop_gate": "v553_to_v554_seed_contract",
                "upstream_artifacts": _json_list([
                    "manifest/v553_temporal_readiness_report.json",
                    "manifest/v553_wave_harmonization_report.json",
                ]),
                "blocked_downstream_layers": _json_list(["v555", "v556", "v557"]),
                "created_at": utc_now(),
                "schema_version": V554_SCHEMA_VERSION,
                "compiler_version": V554_COMPILER_VERSION,
            }
        )
    return pd.DataFrame(rows)


def _build_prohibition_ledger(seed_df: pd.DataFrame, run_id: str) -> pd.DataFrame:
    rows = []
    uses = [
        ("no_biography", "v555", "V554 may not become biography"),
        ("no_parent_story", "v555", "V554 may not become parent story"),
        ("no_household_story", "v555", "V554 may not become household story"),
        ("no_voice", "v557", "V554 may not become voice"),
        ("no_dialogue", "v557", "V554 may not become dialogue"),
        ("no_belief_as_fact", "v555", "V554 may not become belief-as-fact"),
        ("no_wound", "v556", "V554 may not become wound vector"),
        ("no_expectation_baseline", "v556", "V554 may not become expectation baseline"),
        ("no_striving_object", "v556", "V554 may not become striving object"),
        ("no_pressureflow_route", "v556", "V554 may not become pressureflow route"),
        ("no_enneagram_type", "v556", "V554 may not become enneagram type"),
        ("no_runtime_prompt", "v557", "V554 may not become runtime prompt"),
    ]
    for seed in seed_df.to_dict(orient="records"):
        for forbidden_use, forbidden_layer, reason in uses:
            rows.append(
                {
                    "prohibition_id": f"{run_id}__prohibition__{seed['seed_affordance_id']}__{forbidden_use}",
                    "run_id": run_id,
                    "seed_affordance_id": seed["seed_affordance_id"],
                    "forbidden_use": forbidden_use,
                    "forbidden_layer": forbidden_layer,
                    "reason": reason,
                    "must_fail_test": True,
                    "created_at": utc_now(),
                    "schema_version": V554_SCHEMA_VERSION,
                    "compiler_version": V554_COMPILER_VERSION,
                }
            )
    return pd.DataFrame(rows)


def _build_v555_handoff_index(seed_df: pd.DataFrame, run_id: str) -> pd.DataFrame:
    rows = []
    for seed in seed_df.to_dict(orient="records"):
        lane = seed["seed_use_permission"]
        rows.append(
            {
                "v555_handoff_id": f"{run_id}__handoff__{seed['seed_affordance_id']}",
                "run_id": run_id,
                "seed_affordance_id": seed["seed_affordance_id"],
                "handoff_lane": lane,
                "allowed_v555_use": lane == "positive_mediation_required",
                "required_channel": (
                    "regional_locality_mediation"
                    if seed["seed_type"] in {"regional_pressure_seed", "national_pressure_seed"}
                    else "household_mediation"
                    if seed["seed_type"] == "household_mediation_requirement_seed"
                    else "carrier_institutional_mediation"
                    if seed["seed_type"] == "carrier_mediation_requirement_seed"
                    else "orientation_resolution"
                    if seed["seed_type"] in {"temporal_contradiction_seed", "demographic_position_seed"}
                    else "generation_ledger_only"
                ),
                "required_channel_status": "unresolved",
                "source_seed_authority": "v554_seed_affordance_index",
                "source_temporal_authority": "v553_temporal_pressure_field",
                "known_absences_json": seed["known_absences_json"],
                "forbidden_v555_uses_json": seed["forbidden_downstream_uses_json"],
                "requires_generation_ledger": True,
                "may_generate_later": lane != "blocker_only",
                "created_at": utc_now(),
                "schema_version": V554_SCHEMA_VERSION,
                "compiler_version": V554_COMPILER_VERSION,
            }
        )
    return pd.DataFrame(rows)


def _build_audits(
    *,
    run_id: str,
    seed_df: pd.DataFrame,
    absence_df: pd.DataFrame,
    handoff_df: pd.DataFrame,
    input_inspection: dict[str, Any],
    v553_readiness: dict[str, Any],
    v553_harmonization_report: dict[str, Any],
) -> dict[str, pd.DataFrame]:
    forbidden_rows = []
    packet_strings = json.dumps([seed_df.head(3).to_dict(orient="records"), absence_df.head(3).to_dict(orient="records")])
    for term in _FORBIDDEN_PERSONA_TERMS:
        forbidden_rows.append(
            {
                "run_id": run_id,
                "forbidden_term": term,
                "found": term in packet_strings,
                "location": "v554 seed contract outputs",
                "severity": "high" if term in {"voice", "autobiography", "chat_prompt", "pressureflow_route"} else "medium",
                "created_at": utc_now(),
                "schema_version": V554_SCHEMA_VERSION,
                "compiler_version": V554_COMPILER_VERSION,
            }
        )

    seed_authority_rows = []
    for seed in seed_df.to_dict(orient="records"):
        seed_authority_rows.append(
            {
                "run_id": run_id,
                "seed_affordance_id": seed["seed_affordance_id"],
                "seed_type": seed["seed_type"],
                "authority_status": "lawful" if seed["seed_use_permission"] != "blocker_only" else "blocked",
                "use_permission": seed["seed_use_permission"],
                "source_authority_lanes_json": seed["source_authority_lanes_json"],
                "seed_certifiability_score": seed["seed_certifiability_score"],
                "created_at": utc_now(),
                "schema_version": V554_SCHEMA_VERSION,
                "compiler_version": V554_COMPILER_VERSION,
            }
        )

    upstream_rows = [
        {
            "run_id": run_id,
            "artifact": "manifest/v553_temporal_readiness_report.json",
            "status": _clean(v553_readiness.get("status")),
            "ready_for_v554": bool(v553_readiness.get("ready_for_v554", False)),
            "wave_count": int(v553_readiness.get("wave_count", 0) or 0),
            "harmonization_evidence_exists": bool(v553_readiness.get("harmonization_evidence_path"))
            and Path(str(v553_readiness.get("harmonization_evidence_path"))).exists(),
            "created_at": utc_now(),
            "schema_version": V554_SCHEMA_VERSION,
            "compiler_version": V554_COMPILER_VERSION,
        },
        {
            "run_id": run_id,
            "artifact": "manifest/v553_wave_harmonization_report.json",
            "status": _clean(v553_harmonization_report.get("overall_status")),
            "ready_for_v553": bool(v553_harmonization_report.get("ready_for_v553", False)),
            "wave_count": int(v553_harmonization_report.get("wave_count", 0) or 0),
            "wave_pair_count": int(v553_harmonization_report.get("wave_pair_count", 0) or 0),
            "created_at": utc_now(),
            "schema_version": V554_SCHEMA_VERSION,
            "compiler_version": V554_COMPILER_VERSION,
        },
    ]

    absence_prop_rows = []
    for absence in absence_df.to_dict(orient="records"):
        absence_prop_rows.append(
            {
                "run_id": run_id,
                "absence_id": absence["absence_id"],
                "absence_type": absence["absence_type"],
                "propagates_to_v555": True,
                "propagates_to_v556": "pressureflow" in absence["absence_type"] or "orientation" in absence["absence_type"],
                "propagates_to_v557": "voice" in absence["absence_type"] or "prompt" in absence["absence_type"],
                "created_at": utc_now(),
                "schema_version": V554_SCHEMA_VERSION,
                "compiler_version": V554_COMPILER_VERSION,
            }
        )

    permission_rows = []
    for handoff in handoff_df.to_dict(orient="records"):
        permission_rows.append(
            {
                "run_id": run_id,
                "v555_handoff_id": handoff["v555_handoff_id"],
                "seed_affordance_id": handoff["seed_affordance_id"],
                "handoff_lane": handoff["handoff_lane"],
                "may_generate_positive_mediation": handoff["allowed_v555_use"],
                "forbidden_v555_uses_json": handoff["forbidden_v555_uses_json"],
                "created_at": utc_now(),
                "schema_version": V554_SCHEMA_VERSION,
                "compiler_version": V554_COMPILER_VERSION,
            }
        )

    return {
        "forbidden_persona_audit": pd.DataFrame(forbidden_rows),
        "seed_authority_audit": pd.DataFrame(seed_authority_rows),
        "upstream_readiness_audit": pd.DataFrame(upstream_rows),
        "absence_propagation_audit": pd.DataFrame(absence_prop_rows),
        "v555_permission_audit": pd.DataFrame(permission_rows),
    }


def build_v554_seed_contract(
    *,
    run_id: str,
    input_root: str | Path,
    output_root: str | Path,
    input_inspection: dict[str, Any],
    write_csv: bool = False,
    write_parquet: bool = True,
) -> dict[str, Any]:
    root = ensure_output_dirs(output_root, run_id)
    input_root = Path(input_root)

    v553_temporal_readiness_path = input_root / "manifest" / "v553_temporal_readiness_report.json"
    v553_harmonization_report_path = input_root / "manifest" / "v553_wave_harmonization_report.json"
    v553_harmonization_evidence_path = input_root / "v553_wave_harmonization" / "v553_wave_harmonization_evidence.parquet"
    v553_year_indexed_path = input_root / "packets" / "v553_year_indexed_pressure_over_time.parquet"
    v553_interpolated_path = input_root / "packets" / "v553_interpolated_pressure_over_time.parquet"
    v553_country_year_path = input_root / "packets" / "v553_country_year_pressure_field.parquet"
    v553_source_anchor_path = input_root / "packets" / "v553_source_wave_anchor_manifest.parquet"
    v553_pressure_component_path = input_root / "packets" / "v553_pressure_component_breakdown.parquet"
    v553_temporal_authority_path = input_root / "audits" / "v553_temporal_authority_ledger.parquet"
    v553_comparability_path = input_root / "audits" / "v553_cross_wave_comparability_audit.parquet"
    v553_noncomparability_path = input_root / "audits" / "v553_cross_wave_noncomparability_audit.parquet"
    v553_rupture_path = input_root / "audits" / "v553_rupture_block_audit.parquet"
    v553_handoff_path = input_root / "packets" / "v553_downstream_v554_handoff_index.parquet"

    v553_readiness = _load_json(v553_temporal_readiness_path)
    v553_harmonization_report = _load_json(v553_harmonization_report_path)
    country_year_pressure_df = _load_optional_frame(v553_country_year_path)
    if country_year_pressure_df.empty:
        country_year_pressure_df = _load_optional_frame(v553_year_indexed_path)
    harmonization_evidence_exists = v553_harmonization_evidence_path.exists()
    harmonization_evidence_row_count = -1
    if harmonization_evidence_exists:
        try:
            harmonization_evidence_row_count = int(len(read_table(v553_harmonization_evidence_path)))
        except Exception:
            harmonization_evidence_row_count = -1

    source_family = _first_nonempty([
        v553_harmonization_report.get("source_family"),
        v553_readiness.get("source_family"),
        v553_harmonization_report.get("source"),
    ])
    source_country = _first_nonempty([
        v553_harmonization_report.get("country_code"),
        v553_readiness.get("country_code"),
    ])
    wave_names = [str(row.get("wave", "")) for row in (v553_harmonization_report.get("wave_rows", []) or []) if _clean(row.get("wave"))]
    if not canonical_family_key(source_family):
        raise RuntimeError("V554 seed contract requires explicit source_family")
    source_family = canonical_family_label(source_family)
    source_country = canonical_country_code(source_country)
    if not source_country:
        raise RuntimeError("V554 seed contract requires explicit country_code")
    if not wave_names:
        raise RuntimeError("V554 seed contract requires explicit source waves")
    for wave_name in wave_names:
        require_survey_identity(
            source_family,
            wave_name,
            source_country,
            require_country=True,
        )
    source_wave_set = ",".join(sorted(set(wave_names))) if wave_names else _clean(v553_readiness.get("wave_count", "")) or "unknown"

    seed_df = _build_seed_affordance_index(
        run_id=run_id,
        source_family=source_family,
        source_country=source_country,
        source_wave_set=source_wave_set,
        v553_temporal_readiness=v553_readiness,
        v553_harmonization_report=v553_harmonization_report,
        country_year_pressure_df=country_year_pressure_df,
    )
    demographic_slice_df = _build_demographic_slice_contract(seed_df, run_id)
    regional_slice_df = _build_regional_slice_contract(seed_df, run_id)
    mediation_slot_df = _build_required_mediation_slot_index(seed_df, run_id)
    absence_df = _build_absence_register(seed_df, run_id)
    blocker_df = _build_blocker_ledger(seed_df, run_id)
    prohibition_df = _build_prohibition_ledger(seed_df, run_id)
    handoff_df = _build_v555_handoff_index(seed_df, run_id)
    audit_frames = _build_audits(
        run_id=run_id,
        seed_df=seed_df,
        absence_df=absence_df,
        handoff_df=handoff_df,
        input_inspection=input_inspection,
        v553_readiness=v553_readiness,
        v553_harmonization_report=v553_harmonization_report,
    )

    packet_path = root["packets"] / "v554_bounded_seed_affordance_contract_packet.json"
    readiness_path = root["manifest"] / "v554_readiness_report.json"
    input_manifest_path = root["manifest"] / "v554_input_manifest.json"
    seed_contract_manifest_path = root["manifest"] / "v554_seed_contract_manifest.json"
    v555_handoff_manifest_path = root["manifest"] / "v554_v555_handoff_manifest.json"

    seed_affordance_path = root["packets"] / "v554_seed_affordance_index.parquet"
    demographic_slice_path = root["packets"] / "v554_demographic_slice_contract.parquet"
    regional_slice_path = root["packets"] / "v554_regional_slice_contract.parquet"
    mediation_slot_path = root["packets"] / "v554_required_mediation_slot_index.parquet"
    absence_path = root["packets"] / "v554_seed_absence_register.parquet"
    blocker_path = root["packets"] / "v554_seed_blocker_ledger.parquet"
    prohibition_path = root["packets"] / "v554_seed_prohibition_ledger.parquet"
    handoff_index_path = root["packets"] / "v554_v555_handoff_index.parquet"

    forbidden_audit_path = root["audits"] / "v554_forbidden_persona_audit.parquet"
    seed_authority_audit_path = root["audits"] / "v554_seed_authority_audit.parquet"
    upstream_readiness_audit_path = root["audits"] / "v554_upstream_readiness_audit.parquet"
    absence_propagation_audit_path = root["audits"] / "v554_absence_propagation_audit.parquet"
    v555_permission_audit_path = root["audits"] / "v554_v555_permission_audit.parquet"

    seed_artifact_info = write_frame_artifact(
        seed_df,
        path=seed_affordance_path,
        schema_path=root["schemas"] / "v554_seed_affordance_index.schema.json",
        name="v554_seed_affordance_index",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    demographic_artifact_info = write_frame_artifact(
        demographic_slice_df,
        path=demographic_slice_path,
        schema_path=root["schemas"] / "v554_demographic_slice_contract.schema.json",
        name="v554_demographic_slice_contract",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    regional_artifact_info = write_frame_artifact(
        regional_slice_df,
        path=regional_slice_path,
        schema_path=root["schemas"] / "v554_regional_slice_contract.schema.json",
        name="v554_regional_slice_contract",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    mediation_artifact_info = write_frame_artifact(
        mediation_slot_df,
        path=mediation_slot_path,
        schema_path=root["schemas"] / "v554_required_mediation_slot_index.schema.json",
        name="v554_required_mediation_slot_index",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    absence_artifact_info = write_frame_artifact(
        absence_df,
        path=absence_path,
        schema_path=root["schemas"] / "v554_seed_absence_register.schema.json",
        name="v554_seed_absence_register",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    blocker_artifact_info = write_frame_artifact(
        blocker_df,
        path=blocker_path,
        schema_path=root["schemas"] / "v554_seed_blocker_ledger.schema.json",
        name="v554_seed_blocker_ledger",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    prohibition_artifact_info = write_frame_artifact(
        prohibition_df,
        path=prohibition_path,
        schema_path=root["schemas"] / "v554_seed_prohibition_ledger.schema.json",
        name="v554_seed_prohibition_ledger",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    handoff_artifact_info = write_frame_artifact(
        handoff_df,
        path=handoff_index_path,
        schema_path=root["schemas"] / "v554_v555_handoff_index.schema.json",
        name="v554_v555_handoff_index",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )

    write_frame_artifact(
        audit_frames["forbidden_persona_audit"],
        path=forbidden_audit_path,
        schema_path=root["schemas"] / "v554_forbidden_persona_audit.schema.json",
        name="v554_forbidden_persona_audit",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    write_frame_artifact(
        audit_frames["seed_authority_audit"],
        path=seed_authority_audit_path,
        schema_path=root["schemas"] / "v554_seed_authority_audit.schema.json",
        name="v554_seed_authority_audit",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    write_frame_artifact(
        audit_frames["upstream_readiness_audit"],
        path=upstream_readiness_audit_path,
        schema_path=root["schemas"] / "v554_upstream_readiness_audit.schema.json",
        name="v554_upstream_readiness_audit",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    write_frame_artifact(
        audit_frames["absence_propagation_audit"],
        path=absence_propagation_audit_path,
        schema_path=root["schemas"] / "v554_absence_propagation_audit.schema.json",
        name="v554_absence_propagation_audit",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )
    write_frame_artifact(
        audit_frames["v555_permission_audit"],
        path=v555_permission_audit_path,
        schema_path=root["schemas"] / "v554_v555_permission_audit.schema.json",
        name="v554_v555_permission_audit",
        run_id=run_id,
        write_csv=write_csv,
        write_parquet=write_parquet,
    )

    positive_seed_count = int((seed_df["seed_use_permission"] == "positive_mediation_required").sum()) if not seed_df.empty else 0
    reviewable_seed_count = int((seed_df["seed_use_permission"] == "reviewable_mediation_context").sum()) if not seed_df.empty else 0
    blocker_seed_count = int((seed_df["seed_use_permission"] == "blocker_only").sum()) if not seed_df.empty else 0
    absence_count = int(len(absence_df))
    prohibition_count = int(len(prohibition_df))

    v553_boundary_input_present = bool(v553_readiness) and harmonization_evidence_exists
    v553_ready = bool(v553_readiness.get("ready_for_v554", False)) and _clean(v553_readiness.get("status")).startswith("READY")
    ready_for_v555 = v553_ready and positive_seed_count > 0 and blocker_seed_count < len(seed_df)
    readiness_status = "READY_V554_SEED_CONTRACT_WITH_LIMITATIONS" if ready_for_v555 else "SCAFFOLD_ONLY_V554"
    if not v553_boundary_input_present:
        readiness_status = "BLOCKED_MISSING_V553_READINESS"
    elif not harmonization_evidence_exists:
        readiness_status = "BLOCKED_MISSING_V553_TEMPORAL_PRESSURE"

    limitations_kind = "boundary_only_not_runtime"
    limitations_reason = [
        "seed_contract_is_a_boundary_contract_not_runtime_generation",
        "ready_for_runtime_consumption_is_false",
    ]

    packet = {
        "run_id": run_id,
        "source_v553_run_id": _clean(v553_readiness.get("run_id")) or run_id,
        "layer": "v554",
        "title": "Runtime seed affordance contract",
        "artifact_type": "v554_bounded_seed_affordance_contract_packet",
        "schema_version": V554_SCHEMA_VERSION,
        "compiler_version": V554_COMPILER_VERSION,
        "layer_status": readiness_status,
        "readiness_status": readiness_status,
        "seed_affordance_count": int(len(seed_df)),
        "positive_seed_count": positive_seed_count,
        "reviewable_seed_count": reviewable_seed_count,
        "blocker_seed_count": blocker_seed_count,
        "absence_count": absence_count,
        "prohibition_count": prohibition_count,
        "ready_for_v555": ready_for_v555,
        "ready_for_runtime_consumption": False,
        "boundary_only_limitations": True,
        "limitations_kind": limitations_kind,
        "limitations_reason": limitations_reason,
        "forbidden_outputs_written": False,
        "persona_fields_written": False,
        "voice_fields_written": False,
        "biography_fields_written": False,
        "created_at": utc_now(),
        "input_root": repo_relative_path_text(input_root),
        "input_inspection": input_inspection,
        "runtime_use_class": "bounded_seed_affordance_only_not_persona",
        "payload": {
            "upstream_authority_context": {
                "consumes_layer": "v553",
                "consumes_artifact": "v553_temporal_pressure_field_packet",
                "input_status": _clean(input_inspection.get("input_status")),
            },
            "readiness_report_statuses": input_inspection.get("readiness_report_statuses", {}),
            "v553_authority_context": {
                "temporal_readiness_report": v553_readiness,
                "wave_harmonization_report": v553_harmonization_report,
                "authority_requires_multi_wave_harmonization": True,
                "authority_preserves_cross_wave_differences": True,
                "authority_requires_harmonization_evidence_parquet": True,
                "wave_harmonization_evidence": {
                    "path": repo_relative_path_text(v553_harmonization_evidence_path),
                    "row_count": harmonization_evidence_row_count,
                    "exists": harmonization_evidence_exists,
                },
            },
            "seed_contract": {
                "status": readiness_status,
                "limitations_kind": limitations_kind,
                "limitations_reason": limitations_reason,
                "seed_affordance_index_rows": int(len(seed_df)),
                "positive_seed_rows": positive_seed_count,
                "reviewable_seed_rows": reviewable_seed_count,
                "blocker_seed_rows": blocker_seed_count,
                "absence_rows": absence_count,
                "prohibition_rows": prohibition_count,
                "v553_temporal_readiness_status": _clean(v553_readiness.get("status")),
                "v553_wave_harmonization_status": _clean(v553_harmonization_report.get("overall_status")),
                "v553_harmonization_evidence_exists": harmonization_evidence_exists,
                "v553_harmonization_evidence_row_count": harmonization_evidence_row_count,
            },
            "seed_affordance_index_preview": seed_df.head(25).to_dict(orient="records"),
            "demographic_slice_requirements": demographic_slice_df.to_dict(orient="records"),
            "regional_slice_requirements": regional_slice_df.to_dict(orient="records"),
            "required_mediation_slots": mediation_slot_df.to_dict(orient="records"),
            "absence_register_summary": {
                "count": absence_count,
                "domains": absence_df["absence_domain"].tolist() if not absence_df.empty else [],
            },
            "prohibition_ledger_summary": {
                "count": prohibition_count,
                "forbidden_terms": _FORBIDDEN_PERSONA_TERMS,
            },
            "v555_handoff_summary": {
                "handoff_rows": int(len(handoff_df)),
                "positive_handoff_rows": positive_seed_count,
                "reviewable_handoff_rows": reviewable_seed_count,
                "blocker_handoff_rows": blocker_seed_count,
                "ready_for_v555": ready_for_v555,
            },
        },
        "seed_contract": {
            "status": readiness_status,
            "seed_affordance_index_rows": int(len(seed_df)),
            "positive_seed_rows": positive_seed_count,
            "reviewable_seed_rows": reviewable_seed_count,
            "blocker_seed_rows": blocker_seed_count,
            "absence_rows": absence_count,
            "prohibition_rows": prohibition_count,
            "v553_temporal_readiness_status": _clean(v553_readiness.get("status")),
            "v553_wave_harmonization_status": _clean(v553_harmonization_report.get("overall_status")),
            "v553_harmonization_evidence_exists": harmonization_evidence_exists,
            "v553_harmonization_evidence_row_count": harmonization_evidence_row_count,
        },
        "prohibition_ledger_summary": {
            "count": prohibition_count,
            "forbidden_terms": _FORBIDDEN_PERSONA_TERMS,
        },
        "absence_register_summary": {
            "count": absence_count,
            "domains": absence_df["absence_domain"].tolist() if not absence_df.empty else [],
        },
        "v555_handoff_summary": {
            "handoff_rows": int(len(handoff_df)),
            "positive_handoff_rows": positive_seed_count,
            "reviewable_handoff_rows": reviewable_seed_count,
            "blocker_handoff_rows": blocker_seed_count,
            "ready_for_v555": ready_for_v555,
        },
        "v553_authority_context": {
            "temporal_readiness_report": v553_readiness,
            "wave_harmonization_report": v553_harmonization_report,
            "authority_requires_multi_wave_harmonization": True,
            "authority_preserves_cross_wave_differences": True,
            "authority_requires_harmonization_evidence_parquet": True,
        },
        "bounded_seed_envelope": {
            "seed_is_not_persona": True,
            "seed_is_not_autobiography": True,
            "seed_is_not_voice": True,
            "seed_carries_absence": True,
            "seed_carries_prohibition": True,
        },
        "demographic_slice_requirements": demographic_slice_df.to_dict(orient="records"),
        "regional_slice_requirements": regional_slice_df.to_dict(orient="records"),
        "required_mediation_slots": mediation_slot_df.to_dict(orient="records"),
        "seed_affordance_index_preview": seed_df.head(25).to_dict(orient="records"),
        "seed_readiness_score": _bounded_score(positive_seed_count / max(1, len(seed_df))),
        "v553_temporal_score": _bounded_score(float(v553_readiness.get("readiness_score", 0.0) or 0.0)),
        "v553_harmonization_score": _bounded_score(float(v553_readiness.get("harmonization_score", 0.0) or 0.0)),
    }

    packet["seed_contract"]["packet_source"] = repo_relative_path_text(seed_affordance_path)
    packet["seed_contract"]["handoff_index_path"] = repo_relative_path_text(handoff_index_path)

    write_json_artifact(packet_path, packet)
    write_json_artifact(input_manifest_path, input_inspection)
    write_json_artifact(seed_contract_manifest_path, {"run_id": run_id, "created_at": utc_now(), "seed_affordance_index_rows": int(len(seed_df)), "positive_seed_rows": positive_seed_count, "reviewable_seed_rows": reviewable_seed_count, "blocker_seed_rows": blocker_seed_count, "absence_rows": absence_count, "prohibition_rows": prohibition_count})
    write_json_artifact(v555_handoff_manifest_path, {"run_id": run_id, "created_at": utc_now(), "handoff_rows": int(len(handoff_df)), "positive_handoff_rows": positive_seed_count, "reviewable_handoff_rows": reviewable_seed_count, "blocker_handoff_rows": blocker_seed_count})

    build_record = build_layer_build_record(
        spec=type("Spec", (), {"layer": "v554", "title": "Runtime seed affordance contract", "artifact_slug": "v554_bounded_seed_affordance_contract_packet"})(),
        input_inspection=input_inspection,
        status="THIN_READY" if ready_for_v555 else "THIN_READY_WITH_INPUT_GAPS" if v553_ready else "THIN_BLOCKED_MISSING_REQUIRED_INPUT",
        packet_path=repo_relative_path_text(packet_path),
        schema_path=repo_relative_path_text(root["schemas"] / "v554_bounded_seed_affordance_contract_packet.schema.json"),
        audit_path=repo_relative_path_text(forbidden_audit_path),
        readiness_path=repo_relative_path_text(readiness_path),
        input_manifest_path=repo_relative_path_text(input_manifest_path),
        run_id=run_id,
    )

    readiness = {
        "run_id": run_id,
        "layer": "v554",
        "status": readiness_status,
        "ready_for_v555": ready_for_v555,
        "ready_for_runtime_consumption": False,
        "seed_contract_status": readiness_status,
        "source_v553_run_id": packet["source_v553_run_id"],
        "seed_affordance_count": int(len(seed_df)),
        "positive_seed_count": positive_seed_count,
        "reviewable_seed_count": reviewable_seed_count,
        "blocker_seed_count": blocker_seed_count,
        "absence_count": absence_count,
        "prohibition_count": prohibition_count,
        "v553_temporal_readiness_status": _clean(v553_readiness.get("status")),
        "v553_wave_harmonization_status": _clean(v553_harmonization_report.get("overall_status")),
        "v553_harmonization_evidence_exists": harmonization_evidence_exists,
        "v553_harmonization_evidence_row_count": harmonization_evidence_row_count,
        "runtime_readiness": False,
        "semantic_deepening_allowed": False,
        "boundary_only_limitations": True,
        "limitations_kind": limitations_kind,
        "limitations_reason": limitations_reason,
        "forbidden_outputs_written": False,
        "persona_fields_written": False,
        "voice_fields_written": False,
        "biography_fields_written": False,
        "packet_path": repo_relative_path_text(packet_path),
        "readiness_path": repo_relative_path_text(readiness_path),
        "input_manifest_path": repo_relative_path_text(input_manifest_path),
        "seed_contract_manifest_path": repo_relative_path_text(seed_contract_manifest_path),
        "v555_handoff_manifest_path": repo_relative_path_text(v555_handoff_manifest_path),
        "seed_affordance_path": repo_relative_path_text(seed_affordance_path),
        "demographic_slice_contract_path": repo_relative_path_text(demographic_slice_path),
        "regional_slice_contract_path": repo_relative_path_text(regional_slice_path),
        "required_mediation_slot_index_path": repo_relative_path_text(mediation_slot_path),
        "seed_absence_register_path": repo_relative_path_text(absence_path),
        "seed_blocker_ledger_path": repo_relative_path_text(blocker_path),
        "seed_prohibition_ledger_path": repo_relative_path_text(prohibition_path),
        "v555_handoff_index_path": repo_relative_path_text(handoff_index_path),
        "forbidden_persona_audit_path": repo_relative_path_text(forbidden_audit_path),
        "seed_authority_audit_path": repo_relative_path_text(seed_authority_audit_path),
        "upstream_readiness_audit_path": repo_relative_path_text(upstream_readiness_audit_path),
        "absence_propagation_audit_path": repo_relative_path_text(absence_propagation_audit_path),
        "v555_permission_audit_path": repo_relative_path_text(v555_permission_audit_path),
        "build_record": build_record,
        "seed_artifact_info": seed_artifact_info,
        "demographic_slice_artifact_info": demographic_artifact_info,
        "regional_slice_artifact_info": regional_artifact_info,
        "mediation_slot_artifact_info": mediation_artifact_info,
        "absence_artifact_info": absence_artifact_info,
        "blocker_artifact_info": blocker_artifact_info,
        "prohibition_artifact_info": prohibition_artifact_info,
        "handoff_artifact_info": handoff_artifact_info,
        "forbidden_persona_audit_artifact_info": write_frame_artifact(
            audit_frames["forbidden_persona_audit"],
            path=forbidden_audit_path,
            schema_path=root["schemas"] / "v554_forbidden_persona_audit.schema.json",
            name="v554_forbidden_persona_audit",
            run_id=run_id,
            write_csv=write_csv,
            write_parquet=write_parquet,
        ),
    }
    write_json_artifact(readiness_path, readiness)
    return {
        "packet_updates": packet,
        "readiness": readiness,
        "artifact_paths": {
            "packet_path": repo_relative_path_text(packet_path),
            "readiness_path": repo_relative_path_text(readiness_path),
            "input_manifest_path": repo_relative_path_text(input_manifest_path),
            "seed_contract_manifest_path": repo_relative_path_text(seed_contract_manifest_path),
            "v555_handoff_manifest_path": repo_relative_path_text(v555_handoff_manifest_path),
            "seed_affordance_path": repo_relative_path_text(seed_affordance_path),
            "demographic_slice_contract_path": repo_relative_path_text(demographic_slice_path),
            "regional_slice_contract_path": repo_relative_path_text(regional_slice_path),
            "required_mediation_slot_index_path": repo_relative_path_text(mediation_slot_path),
            "seed_absence_register_path": repo_relative_path_text(absence_path),
            "seed_blocker_ledger_path": repo_relative_path_text(blocker_path),
            "seed_prohibition_ledger_path": repo_relative_path_text(prohibition_path),
            "v555_handoff_index_path": repo_relative_path_text(handoff_index_path),
            "forbidden_persona_audit_path": repo_relative_path_text(forbidden_audit_path),
            "seed_authority_audit_path": repo_relative_path_text(seed_authority_audit_path),
            "upstream_readiness_audit_path": repo_relative_path_text(upstream_readiness_audit_path),
            "absence_propagation_audit_path": repo_relative_path_text(absence_propagation_audit_path),
            "v555_permission_audit_path": repo_relative_path_text(v555_permission_audit_path),
        },
        "artifact_infos": {
            "seed_artifact_info": seed_artifact_info,
            "demographic_slice_artifact_info": demographic_artifact_info,
            "regional_slice_artifact_info": regional_artifact_info,
            "mediation_slot_artifact_info": mediation_artifact_info,
            "absence_artifact_info": absence_artifact_info,
            "blocker_artifact_info": blocker_artifact_info,
            "prohibition_artifact_info": prohibition_artifact_info,
            "handoff_artifact_info": handoff_artifact_info,
        },
    }


def validate_v554_seed_contract_readiness(readiness: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if readiness.get("ready_for_runtime_consumption"):
        errors.append("V554 seed contract must not be runtime consumable")
    for key in (
        "packet_path",
        "readiness_path",
        "seed_affordance_path",
        "demographic_slice_contract_path",
        "regional_slice_contract_path",
        "required_mediation_slot_index_path",
        "seed_absence_register_path",
        "seed_blocker_ledger_path",
        "seed_prohibition_ledger_path",
        "v555_handoff_index_path",
        "forbidden_persona_audit_path",
        "seed_authority_audit_path",
        "upstream_readiness_audit_path",
        "absence_propagation_audit_path",
        "v555_permission_audit_path",
    ):
        if not _clean(readiness.get(key)):
            errors.append(f"V554 seed contract missing {key}")
        elif not Path(str(readiness.get(key))).exists():
            errors.append(f"V554 seed contract missing artifact {key}")
    if int(readiness.get("seed_affordance_count", -1) or -1) < 0:
        errors.append("V554 seed contract missing seed affordance count")
    if int(readiness.get("prohibition_count", -1) or -1) < 0:
        errors.append("V554 seed contract missing prohibition count")
    return errors


__all__ = [
    "build_v554_seed_contract",
    "validate_v554_seed_contract_readiness",
]
