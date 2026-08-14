"""Validation for V552 structural-pressure contract v2.1.4 outputs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import pandas as pd

from data.ddm_build_copy.ddm_v552_contract import (
    recompute_v552_observation_state,
    recompute_v552_distribution_contract,
    recompute_v552_pressure_component_id,
    recompute_v552_pressure_observation_id,
    recompute_v552_response_surface_signature,
    recompute_v552_v2_1_4_component_measurement_hash,
    recompute_v552_v2_1_4_pressure_measurement_hash,
    v552_canonical_value,
)
from data.ddm_build_copy.ddm_v552_structural import (
V552_EPSILON,
    V552_HANDOFF_SCHEMA_VERSION,
    V552_NORMALIZED_INTENSITY_MAX,
    V552_NORMALIZED_INTENSITY_MIN,
    V552_PRESSURE_FORMULA_ID,
    V552_PRESSURE_FORMULA_VERSION,
    V552_PRESSURE_SCALE_ID,
    V552_SCHEMA_VERSION,
    _component_identity,
    _component_response_surface_signature,
    _id,
    _json_dumps,
    _observation_identity,
    _pressure_measure_class_for_status,
    _response_surface_completeness,
    _stable_hash_v21,
    _temporal_key_index,
    resolve_v552_distribution_intensity_representation,
    resolve_v552_signed_component,
    select_v552_distribution_weight_basis,
    validate_v552_v551_input_contract,
)

# Persisted V552 inputs can carry source-authorized normalized coordinates at
# six-decimal precision.  Validation may therefore compare a persisted
# reconstruction within one source-coordinate micro-unit, while the compiler
# itself retains the stricter contract epsilon for classification decisions.
V552_PERSISTED_NUMERIC_EPSILON = 1e-6

EXPECTED_PRESSURE_SCALE_MIN = "-1"
EXPECTED_PRESSURE_SCALE_MAX = "1"


@dataclass(frozen=True)
class ValidationIssue:
    token: str
    detail: str = ""


def _issue(issues: list[ValidationIssue], token: str, detail: str = "") -> None:
    issues.append(ValidationIssue(token, detail))


def _canon(value: Any) -> str:
    return str(v552_canonical_value(value))


def _close(a: Any, b: Any, eps: float = V552_PERSISTED_NUMERIC_EPSILON) -> bool:
    av = pd.to_numeric(pd.Series([a]), errors="coerce").iloc[0]
    bv = pd.to_numeric(pd.Series([b]), errors="coerce").iloc[0]
    if pd.isna(av) and pd.isna(bv):
        return True
    if pd.isna(av) or pd.isna(bv):
        return False
    return abs(float(av) - float(bv)) <= eps


def recompute_v552_structural_fact_id(row: Mapping[str, Any]) -> str:
    return _id("v552sf__", {"po": row.get("source_row_id")})


def recompute_v552_temporal_key_source_id(row: Mapping[str, Any]) -> str:
    return _id("v552tks__", {"fact": row.get("v552_structural_fact_id")})


def recompute_v552_pressure_handoff_id(row: Mapping[str, Any]) -> str:
    return _id("v552poh__", {"po": row.get("v552_pressure_observation_id")})


def read_v552_contract_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def read_v552_contract_parquet(path: Path) -> pd.DataFrame:
    return pd.read_parquet(path)


def _boolish(value: Any) -> bool:
    return _canon(value).casefold() in {"1", "true", "t", "yes", "y"}


def _set(values: pd.Series) -> set[str]:
    return set(values.map(_canon).tolist())


def validate_v552_readiness_projection(
    *,
    readiness: pd.DataFrame,
    components: pd.DataFrame,
    observations: pd.DataFrame,
    facts: pd.DataFrame,
    temporal_sources: pd.DataFrame,
    pressure_handoff: pd.DataFrame,
    validation_issues: list[ValidationIssue],
    execution_mode: str,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if readiness.empty:
        _issue(issues, "readiness_status_mismatch", "missing_readiness")
        return issues
    row = readiness.iloc[0].to_dict()
    expected_status = "READY_V552_STRUCTURAL_PRESSURE_CONTRACT"
    if execution_mode == "diagnostic":
        expected_status = "DIAGNOSTIC_V552_NO_STRICT_NOT_READY"
    elif execution_mode == "strict_blocked":
        expected_status = "BLOCKED_V552_OUTPUT_CONTRACT"
    for field in ["status", "final_status", "v552_compile_status"]:
        if field in row and _canon(row.get(field)) != expected_status:
            _issue(issues, "readiness_status_mismatch", field)
    count_expectations = {
        "input_atom_rows": len(components),
        "input_atom_count": len(components),
        "unique_empirical_object_count": components.get("empirical_object_id", pd.Series(dtype=str)).map(_canon).nunique(),
        "category_empirical_object_count": len(components),
        "unique_empirical_distribution_count": observations.get("empirical_distribution_id", pd.Series(dtype=str)).map(_canon).nunique(),
        "pressure_observation_candidate_count": len(observations),
        "observed_pressure_count": int(observations.get("pressure_score_status", pd.Series(dtype=str)).map(_canon).eq("OBSERVED_NONZERO").sum()),
        "observed_zero_pressure_count": int(observations.get("pressure_score_status", pd.Series(dtype=str)).map(_canon).eq("OBSERVED_ZERO").sum()),
        "noncomputable_pressure_count": int((~observations.get("pressure_score_status", pd.Series(dtype=str)).map(_canon).isin(["OBSERVED_NONZERO", "OBSERVED_ZERO"])).sum()),
        "review_required_pressure_count": int(observations.get("pressure_score_status", pd.Series(dtype=str)).map(_canon).eq("REVIEW_REQUIRED").sum()),
        "pressure_linkage_eligible_count": int(observations.get("v552j_pressure_linkage_eligible", pd.Series(False, index=observations.index)).map(_boolish).sum()),
        "handoff_index_rows": len(pressure_handoff),
        "comparability_key_count": len(observations),
        "allowed_for_v553_temporal_field_count": int(observations.get("allowed_for_v553_temporal_field", pd.Series(False, index=observations.index)).map(_boolish).sum()),
    }
    for field, expected in count_expectations.items():
        if field not in row:
            continue
        got = pd.to_numeric(pd.Series([row.get(field)]), errors="coerce").iloc[0]
        if pd.isna(got) or int(got) != int(expected):
            if field in {"input_atom_rows", "input_atom_count"}:
                _issue(issues, "readiness_input_count_mismatch", field)
            elif field in {"unique_empirical_distribution_count", "unique_empirical_object_count", "category_empirical_object_count", "pressure_observation_candidate_count"}:
                _issue(issues, "readiness_distribution_count_mismatch", field)
            elif field in {"handoff_index_rows", "comparability_key_count"}:
                _issue(issues, "readiness_handoff_count_mismatch", field)
            else:
                _issue(issues, "readiness_count_mismatch", field)
    for field, expected in [("schema_version", V552_SCHEMA_VERSION), ("compiler_version", V552_HANDOFF_SCHEMA_VERSION)]:
        if field in row and _canon(row.get(field)) != _canon(expected):
            _issue(issues, "readiness_version_mismatch", field)
    if "ready_for_v552j_pressure_linkage" in row:
        expected_ready = count_expectations["pressure_linkage_eligible_count"] > 0 and execution_mode == "acceptance"
        if _boolish(row.get("ready_for_v552j_pressure_linkage")) != expected_ready:
            _issue(issues, "readiness_permission_mismatch", "ready_for_v552j_pressure_linkage")
    for field in ["ready_for_v553_direct", "ready_for_v553_after_v552j"]:
        if field in row and _boolish(row.get(field)):
            _issue(issues, "readiness_permission_mismatch", field)
    if execution_mode != "acceptance":
        for field in ["ready_for_v552j_structural_inspection", "ready_for_v552j_pressure_linkage", "ready_for_v552j_inspection"]:
            if field in row and _boolish(row.get(field)):
                token = "diagnostic_readiness_v552j_authorization" if execution_mode == "diagnostic" else "strict_blocked_readiness_v552j_authorization"
                _issue(issues, token, field)
        if _canon(row.get("v552_v552j_handoff_readiness")) not in {"", "not_authorized"}:
            token = "diagnostic_readiness_v552j_authorization" if execution_mode == "diagnostic" else "strict_blocked_readiness_v552j_authorization"
            _issue(issues, token, "v552_v552j_handoff_readiness")
    return issues


def _validate_governed_metadata(issues: list[ValidationIssue], frame: pd.DataFrame, artifact: str) -> None:
    if frame.empty:
        return
    checks = [
        ("schema_version", V552_SCHEMA_VERSION, "schema_version_mismatch"),
        ("compiler_version", V552_HANDOFF_SCHEMA_VERSION, "compiler_version_mismatch"),
        ("pressure_formula_id", V552_PRESSURE_FORMULA_ID, "pressure_formula_id_mismatch"),
        ("pressure_formula_version", V552_PRESSURE_FORMULA_VERSION, "pressure_formula_version_mismatch"),
        ("pressure_scale_id", V552_PRESSURE_SCALE_ID, "pressure_scale_id_mismatch"),
    ]
    for field, expected, token in checks:
        if field in frame.columns:
            bad = frame[~frame[field].map(_canon).eq(_canon(expected))]
            if not bad.empty:
                _issue(issues, token, f"{artifact}:{field}")
    if "pressure_scale_min" in frame.columns:
        bad = frame[~frame["pressure_scale_min"].map(_canon).eq(EXPECTED_PRESSURE_SCALE_MIN)]
        if not bad.empty:
            _issue(issues, "pressure_scale_bounds_mismatch", f"{artifact}:pressure_scale_min")
    if "pressure_scale_max" in frame.columns:
        bad = frame[~frame["pressure_scale_max"].map(_canon).eq(EXPECTED_PRESSURE_SCALE_MAX)]
        if not bad.empty:
            _issue(issues, "pressure_scale_bounds_mismatch", f"{artifact}:pressure_scale_max")
    if "normalized_intensity_min" in frame.columns:
        bad = frame[~frame["normalized_intensity_min"].map(_canon).eq(_canon(V552_NORMALIZED_INTENSITY_MIN))]
        if not bad.empty:
            _issue(issues, "normalized_intensity_contract_bounds_mismatch", f"{artifact}:normalized_intensity_min")
    if "normalized_intensity_max" in frame.columns:
        bad = frame[~frame["normalized_intensity_max"].map(_canon).eq(_canon(V552_NORMALIZED_INTENSITY_MAX))]
        if not bad.empty:
            _issue(issues, "normalized_intensity_contract_bounds_mismatch", f"{artifact}:normalized_intensity_max")


def validate_v552_pressure_handoff_projection(
    observations: pd.DataFrame,
    components: pd.DataFrame,
    pressure_handoff: pd.DataFrame,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if len(pressure_handoff) != len(observations):
        _issue(issues, "pressure_handoff_coverage_mismatch")
    hand_by_obs = pressure_handoff.groupby("v552_pressure_observation_id", dropna=False) if "v552_pressure_observation_id" in pressure_handoff else {}
    fields = [
        "v552_pressure_observation_id", "pressure_observation_identity_hash", "empirical_distribution_id",
        "source", "source_family", "wave", "canonical_wave", "country_code", "question_id", "var_code",
        "semantic_identity_signature", "structural_identity_signature", "response_scale_signature",
        "source_atom_ids_json", "source_atom_contract_hashes_json", "source_measurement_contract_hashes_json",
        "source_intensity_representation_class", "source_intensity_representation_status",
        "source_intensity_exact_fit_candidates_json", "component_response_surface_signature",
        "response_surface_completeness_status", "pressure_measure_class", "pressure_score",
        "pressure_score_status", "pressure_formula_id", "pressure_formula_version", "pressure_scale_id",
        "pressure_measurement_hash", "v552j_pressure_linkage_eligible", "known_absences_json",
        "forbidden_inference_json",
    ]
    for _, obs in observations.iterrows():
        obs_id = str(obs.get("v552_pressure_observation_id"))
        if not isinstance(hand_by_obs, dict):
            try:
                hand = hand_by_obs.get_group(obs_id)
            except KeyError:
                hand = pd.DataFrame()
        else:
            hand = pd.DataFrame()
        if len(hand) != 1:
            _issue(issues, "pressure_handoff_coverage_mismatch", obs_id)
            continue
        h = hand.iloc[0].to_dict()
        if recompute_v552_pressure_handoff_id(h) != h.get("handoff_id"):
            _issue(issues, "pressure_handoff_id_mismatch", obs_id)
        comp_group = components[components["v552_pressure_observation_id"].astype(str).eq(obs_id)]
        expected_component_ids = _json_dumps(sorted(comp_group.get("v552_pressure_component_id", pd.Series(dtype=str)).fillna("").astype(str).tolist()))
        expected_component_hashes = _json_dumps(sorted(comp_group.get("component_measurement_hash", pd.Series(dtype=str)).fillna("").astype(str).tolist()))
        if _canon(h.get("v552_pressure_component_ids_json")) != _canon(expected_component_ids):
            _issue(issues, "pressure_handoff_projection_mismatch", f"{obs_id}:component_ids")
        if _canon(h.get("v552_component_measurement_hashes_json")) != _canon(expected_component_hashes):
            _issue(issues, "pressure_handoff_projection_mismatch", f"{obs_id}:component_hashes")
        for field in fields:
            if _canon(h.get(field)) != _canon(obs.get(field)):
                _issue(issues, "pressure_handoff_projection_mismatch", f"{obs_id}:{field}")
                break
        for field in ["direct_v553_authorization", "temporal_authority", "runtime_authority"]:
            if _boolish(h.get(field)):
                _issue(issues, field.replace("_", "_"))
    return issues


def validate_v552_v2_1_4_outputs(
    *,
    input_atoms: pd.DataFrame,
    components: pd.DataFrame,
    observations: pd.DataFrame,
    structural_facts: pd.DataFrame,
    temporal_sources: pd.DataFrame,
    pressure_handoff: pd.DataFrame,
    readiness: pd.DataFrame,
    execution_mode: str = "acceptance",
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for artifact, frame in [
        ("components", components),
        ("observations", observations),
        ("structural_facts", structural_facts),
        ("temporal_sources", temporal_sources),
        ("pressure_handoff", pressure_handoff),
        ("readiness", readiness),
    ]:
        _validate_governed_metadata(issues, frame, artifact)
    input_contract = validate_v552_v551_input_contract(input_atoms)
    if input_contract.get("status") != "PASS":
        _issue(issues, str(input_contract.get("status")), ",".join(input_contract.get("missing_columns", [])))
    if len(components) != len(input_atoms):
        _issue(issues, "component_count_mismatch")
    dist_count = input_atoms["empirical_distribution_id"].nunique() if "empirical_distribution_id" in input_atoms else 0
    if len(observations) != dist_count:
        _issue(issues, "observation_distribution_count_mismatch")
    if "atom_id" in input_atoms and input_atoms["atom_id"].duplicated().any():
        _issue(issues, "duplicate_atom_id")
    if "source_atom_id" in components:
        if components["source_atom_id"].map(_canon).duplicated().any():
            _issue(issues, "duplicate_component_source_atom")
        if "atom_id" in input_atoms and _set(input_atoms["atom_id"]) != _set(components["source_atom_id"]):
            _issue(issues, "component_atom_coverage_mismatch")
    if "empirical_distribution_id" in observations:
        if observations["empirical_distribution_id"].map(_canon).duplicated().any():
            _issue(issues, "duplicate_pressure_observation_distribution")
        if "empirical_distribution_id" in input_atoms and _set(input_atoms["empirical_distribution_id"]) != _set(observations["empirical_distribution_id"]):
            _issue(issues, "observation_distribution_coverage_mismatch")

    atom_by_id = input_atoms.set_index("atom_id").to_dict("index") if "atom_id" in input_atoms else {}
    for _, comp in components.iterrows():
        d = comp.to_dict()
        expected_id = recompute_v552_pressure_component_id(d)
        if expected_id and expected_id != d.get("v552_pressure_component_id"):
            _issue(issues, "stable_component_id_mismatch", str(d.get("source_atom_id")))
        expected_hash = recompute_v552_v2_1_4_component_measurement_hash(d)
        if expected_hash != d.get("component_measurement_hash"):
            _issue(issues, "component_measurement_hash_mismatch", str(d.get("v552_pressure_component_id")))

    for dist, atom_group in input_atoms.groupby("empirical_distribution_id", dropna=False, sort=True):
        comp_group = components[components["empirical_distribution_id"].astype(str).eq(str(dist))].copy()
        if comp_group.empty:
            continue
        recomputed = recompute_v552_distribution_contract(atom_group, comp_group)
        for token in recomputed.root_issue_tokens:
            _issue(issues, token, str(dist))
        rep = resolve_v552_distribution_intensity_representation(atom_group)
        stored_rep = set(comp_group["source_intensity_representation_class"].fillna("").astype(str))
        stored_status = set(comp_group["source_intensity_representation_status"].fillna("").astype(str))
        if stored_rep != {rep.representation_class}:
            _issue(issues, "representation_class_mismatch", str(dist))
        if stored_status != {rep.resolution_status}:
            _issue(issues, "representation_status_inconsistent_with_values", str(dist))
        expected_candidates = _canon(_json_dumps(list(rep.exact_fit_candidates)))
        stored_candidates = set(comp_group.get("source_intensity_exact_fit_candidates_json", pd.Series(dtype=str)).map(_canon))
        if stored_candidates and stored_candidates != {expected_candidates}:
            _issue(issues, "representation_exact_fit_candidates_mismatch", str(dist))
        expected_tokens = set(atom_group.get("scale_direction", pd.Series(dtype=str)).map(_canon))
        stored_tokens = set(comp_group.get("source_scale_direction_token", pd.Series(dtype=str)).map(_canon))
        if expected_tokens and stored_tokens != expected_tokens:
            _issue(issues, "source_scale_direction_token_mismatch", str(dist))
        for _, atom in atom_group.iterrows():
            comp = comp_group[comp_group["source_atom_id"].astype(str).eq(str(atom.get("atom_id")))]
            if comp.empty:
                continue
            transform = resolve_v552_signed_component(atom.to_dict(), rep)
            cd = comp.iloc[0].to_dict()
            if _canon(cd.get("direction_scale_consistency_status")) != _canon(transform.direction_scale_consistency_status):
                _issue(issues, "direction_scale_consistency_mismatch", str(atom.get("atom_id")))
            got = pd.to_numeric(pd.Series([cd.get("canonical_signed_component")]), errors="coerce").iloc[0]
            exp = transform.canonical_signed_component
            if exp is not None and (pd.isna(got) or abs(float(got) - float(exp)) > V552_PERSISTED_NUMERIC_EPSILON):
                _issue(issues, "canonical_signed_component_mismatch", str(atom.get("atom_id")))
        for _, comp in comp_group.iterrows():
            atom_id = str(comp.get("source_atom_id"))
            if _canon(comp.get("distribution_weight_basis")) != _canon(recomputed.distribution_weight_basis):
                _issue(issues, "distribution_weight_basis_mismatch", atom_id)
            if atom_id in recomputed.distribution_weight_raw_by_atom and not _close(comp.get("distribution_weight_raw"), recomputed.distribution_weight_raw_by_atom[atom_id]):
                _issue(issues, "distribution_weight_raw_mismatch", atom_id)
            if atom_id in recomputed.distribution_weight_normalized_by_atom and not _close(comp.get("distribution_weight_normalized"), recomputed.distribution_weight_normalized_by_atom[atom_id]):
                _issue(issues, "distribution_weight_normalized_mismatch", atom_id)

    for _, obs in observations.iterrows():
        d = obs.to_dict()
        obs_id = d.get("v552_pressure_observation_id")
        comp_group = components[components["v552_pressure_observation_id"].astype(str).eq(str(obs_id))].copy()
        atom_group = input_atoms[input_atoms["atom_id"].astype(str).isin(comp_group["source_atom_id"].astype(str))].copy()
        first = atom_group.iloc[0].to_dict() if not atom_group.empty else {}
        expected_obs_id = recompute_v552_pressure_observation_id(first) if first else ""
        if expected_obs_id and expected_obs_id != obs_id:
            _issue(issues, "stable_observation_id_mismatch", str(obs_id))
        if _component_response_surface_signature(comp_group) != d.get("component_response_surface_signature"):
            _issue(issues, "response_surface_signature_mismatch", str(obs_id))
        surface_status, _, _ = _response_surface_completeness(comp_group)
        if surface_status != d.get("response_surface_completeness_status"):
            _issue(issues, "response_surface_completeness_mismatch", str(obs_id))
        basis, weights_raw, reason = select_v552_distribution_weight_basis(comp_group)
        if basis != d.get("distribution_weight_basis"):
            _issue(issues, "distribution_weight_basis_mismatch", str(obs_id))
        if weights_raw is not None:
            weights_norm = weights_raw / float(weights_raw.sum())
            signed = pd.to_numeric(comp_group["canonical_signed_component"], errors="coerce")
            recomputed = float((weights_norm.reset_index(drop=True) * signed.reset_index(drop=True)).sum())
            if abs(recomputed) <= V552_EPSILON:
                recomputed = 0.0
            got = pd.to_numeric(pd.Series([d.get("pressure_score")]), errors="coerce").iloc[0]
            if pd.isna(got) or abs(float(got) - recomputed) > V552_PERSISTED_NUMERIC_EPSILON:
                _issue(issues, "pressure_score_recomputation_mismatch", str(obs_id))
        expected_class = _pressure_measure_class_for_status(d.get("pressure_score"), surface_status)
        if expected_class != d.get("pressure_measure_class"):
            _issue(issues, "pressure_measure_class_mismatch", str(obs_id))
        recomputed = recompute_v552_distribution_contract(atom_group, comp_group)
        checks = [
            ("distribution_mass_raw", "distribution_mass_raw_mismatch", recomputed.distribution_mass_raw),
            ("distribution_mass_used", "distribution_mass_used_mismatch", recomputed.distribution_mass_used),
            ("substantive_response_coverage", "substantive_response_coverage_mismatch", recomputed.substantive_response_coverage),
            ("respondent_denominator_unweighted", "respondent_denominator_mismatch", recomputed.respondent_denominator_unweighted),
            ("weighted_response_mass", "weighted_response_mass_mismatch", recomputed.weighted_response_mass),
            ("response_surface_component_count", "response_surface_component_count_mismatch", recomputed.response_surface_component_count),
            ("response_surface_respondent_coverage", "response_surface_respondent_coverage_mismatch", recomputed.response_surface_respondent_coverage),
            ("positive_component_share", "component_share_mismatch", recomputed.positive_component_share),
            ("negative_component_share", "component_share_mismatch", recomputed.negative_component_share),
            ("neutral_component_share", "component_share_mismatch", recomputed.neutral_component_share),
            ("directional_entropy", "directional_entropy_mismatch", recomputed.directional_entropy),
            ("polarization_index", "polarization_index_mismatch", recomputed.polarization_index),
            ("dominant_orientation_share", "dominant_orientation_mismatch", recomputed.dominant_orientation_share),
            ("component_signed_intensity_min", "signed_intensity_summary_mismatch", recomputed.component_signed_intensity_min),
            ("component_signed_intensity_max", "signed_intensity_summary_mismatch", recomputed.component_signed_intensity_max),
            ("component_signed_intensity_std", "signed_intensity_summary_mismatch", recomputed.component_signed_intensity_std),
        ]
        for field, token, expected in checks:
            if not _close(d.get(field), expected):
                _issue(issues, token, f"{obs_id}:{field}")
        if _canon(d.get("response_surface_completeness_status")) != _canon(recomputed.response_surface_completeness_status):
            _issue(issues, "response_surface_completeness_mismatch", str(obs_id))
        if _canon(d.get("response_surface_completeness_basis")) != _canon(recomputed.response_surface_completeness_basis):
            _issue(issues, "response_surface_completeness_basis_mismatch", str(obs_id))
        if _canon(d.get("dominant_orientation")) != _canon(recomputed.dominant_orientation):
            _issue(issues, "dominant_orientation_mismatch", str(obs_id))
        state = recompute_v552_observation_state(
            pressure_score=recomputed.pressure_score,
            components=comp_group,
            response_surface_status=recomputed.response_surface_completeness_status,
            root_issue_tokens=recomputed.root_issue_tokens,
        )
        state_checks = [
            ("pressure_score_status", "pressure_score_status_mismatch", state.pressure_score_status),
            ("observed_pressure_zero", "observed_pressure_zero_mismatch", state.observed_pressure_zero),
            ("pressure_magnitude", "pressure_magnitude_mismatch", state.pressure_magnitude),
            ("pressure_orientation", "pressure_orientation_mismatch", state.pressure_orientation),
            ("component_permission_status", "component_permission_status_mismatch", state.component_permission_status),
            ("pressure_observation_status", "pressure_observation_status_mismatch", state.pressure_observation_status),
            ("pressure_observation_ineligibility_reason", "pressure_observation_ineligibility_reason_mismatch", state.pressure_observation_ineligibility_reason),
            ("v552j_structural_context_eligible", "v552j_structural_context_eligibility_mismatch", state.v552j_structural_context_eligible if execution_mode == "acceptance" else False),
            ("v553_probe_candidate_after_v552j", "v553_probe_candidate_status_mismatch", state.v553_probe_candidate_after_v552j if execution_mode == "acceptance" else False),
        ]
        for field, token, expected in state_checks:
            if field in {"pressure_magnitude"}:
                if not _close(d.get(field), expected):
                    _issue(issues, token, str(obs_id))
            elif field in {"v552j_structural_context_eligible", "v553_probe_candidate_after_v552j"}:
                if _boolish(d.get(field)) != bool(expected):
                    _issue(issues, token, str(obs_id))
            elif _canon(d.get(field)) != _canon(expected):
                _issue(issues, token, str(obs_id))
        expected_link = state.v552j_pressure_linkage_eligible and execution_mode == "acceptance"
        stored_link = _boolish(d.get("v552j_pressure_linkage_eligible"))
        if expected_link and not stored_link:
            _issue(issues, "eligible_pressure_missing_v552j_linkage", str(obs_id))
        if not expected_link and stored_link:
            token = "diagnostic_pressure_linkage_authorization" if execution_mode == "diagnostic" else ("strict_blocked_pressure_linkage_authorization" if execution_mode == "strict_blocked" else "ineligible_pressure_v552j_linkage_authorization")
            _issue(issues, token, str(obs_id))
        if (recomputed.pressure_score is None) != pd.isna(d.get("pressure_score")):
            _issue(issues, "pressure_zero_null_mismatch", str(obs_id))
        expected_hash = recompute_v552_v2_1_4_pressure_measurement_hash(d, comp_group.to_dict("records"))
        if expected_hash != d.get("pressure_measurement_hash"):
            _issue(issues, "pressure_measurement_hash_mismatch", str(obs_id))

    contract_fields = [
        "empirical_distribution_id", "component_response_surface_signature", "response_surface_completeness_status",
        "pressure_measure_class", "pressure_formula_id", "pressure_formula_version", "pressure_scale_id",
        "pressure_measurement_hash", "semantic_identity_signature", "structural_identity_signature",
        "response_scale_signature", "directionality_policy", "response_topology",
        "source_intensity_representation_class", "source_intensity_representation_status", "pressure_score",
        "pressure_score_status",
        "source_intensity_exact_fit_candidates_json", "normalized_intensity_min", "normalized_intensity_max",
        "source_scale_direction_token",
    ]
    facts_by_obs = structural_facts[structural_facts.get("source_artifact", pd.Series(dtype=str)).astype(str).eq("v552_pressure_observation_index")]
    if not observations.empty:
        obs_ids = _set(observations["v552_pressure_observation_id"])
        fact_obs_ids = _set(facts_by_obs.get("source_row_id", pd.Series(dtype=str)))
        hand_obs_ids = _set(pressure_handoff.get("v552_pressure_observation_id", pd.Series(dtype=str)))
        if obs_ids != fact_obs_ids or facts_by_obs.get("source_row_id", pd.Series(dtype=str)).map(_canon).duplicated().any():
            _issue(issues, "structural_fact_coverage_mismatch")
        if obs_ids != hand_obs_ids:
            _issue(issues, "pressure_handoff_coverage_mismatch")
        temporal_fact_ids = _set(temporal_sources.get("v552_structural_fact_id", pd.Series(dtype=str)))
        fact_ids = _set(facts_by_obs.get("v552_structural_fact_id", pd.Series(dtype=str)))
        if fact_ids != temporal_fact_ids or temporal_sources.get("v552_structural_fact_id", pd.Series(dtype=str)).map(_canon).duplicated().any():
            _issue(issues, "temporal_source_coverage_mismatch")
    for _, fact in structural_facts.iterrows():
        if _canon(fact.get("v552_structural_fact_id")) != _canon(recompute_v552_structural_fact_id(fact.to_dict())):
            _issue(issues, "stable_structural_fact_id_mismatch", str(fact.get("v552_structural_fact_id")))
    for _, temporal in temporal_sources.iterrows():
        if _canon(temporal.get("v552_temporal_key_source_id")) != _canon(recompute_v552_temporal_key_source_id(temporal.to_dict())):
            _issue(issues, "stable_temporal_source_id_mismatch", str(temporal.get("v552_temporal_key_source_id")))
    issues.extend(validate_v552_pressure_handoff_projection(observations, components, pressure_handoff))
    if execution_mode != "acceptance":
        obs_struct = observations.get("v552j_structural_context_eligible", pd.Series(False, index=observations.index)).map(_boolish)
        obs_probe = observations.get("v553_probe_candidate_after_v552j", pd.Series(False, index=observations.index)).map(_boolish)
        if obs_struct.any():
            token = "diagnostic_v552j_structural_context_authorization" if execution_mode == "diagnostic" else "strict_blocked_v552j_structural_context_authorization"
            _issue(issues, token)
        if obs_probe.any():
            token = "diagnostic_v553_probe_candidate_authorization" if execution_mode == "diagnostic" else "strict_blocked_v553_probe_candidate_authorization"
            _issue(issues, token)
        fact_bad = pd.Series(False, index=structural_facts.index)
        for field in ["v552j_pressure_linkage_eligible", "v552j_structural_context_eligible", "v553_probe_candidate_after_v552j", "allowed_for_v553_temporal_field", "pressure_anchor_candidate_after_v552j"]:
            if field in structural_facts.columns:
                fact_bad = fact_bad | structural_facts[field].map(_boolish)
        if "allowed_v552j_use" in structural_facts.columns:
            fact_bad = fact_bad | ~structural_facts["allowed_v552j_use"].map(_canon).isin(["", "not_authorized"])
        if fact_bad.any():
            token = "diagnostic_fact_v552j_authorization" if execution_mode == "diagnostic" else "strict_blocked_fact_v552j_authorization"
            _issue(issues, token)
        temporal_bad = pd.Series(False, index=temporal_sources.index)
        for field in ["allowed_for_v552j", "allowed_for_v553_probe", "allowed_for_v553_temporal_field"]:
            if field in temporal_sources.columns:
                temporal_bad = temporal_bad | temporal_sources[field].map(_boolish)
        if temporal_bad.any():
            token = "diagnostic_fact_v552j_authorization" if execution_mode == "diagnostic" else "strict_blocked_fact_v552j_authorization"
            _issue(issues, token)
    for _, obs in observations.iterrows():
        fact = facts_by_obs[facts_by_obs["source_row_id"].astype(str).eq(str(obs.get("v552_pressure_observation_id")))]
        hand = pressure_handoff[pressure_handoff["v552_pressure_observation_id"].astype(str).eq(str(obs.get("v552_pressure_observation_id")))] if "v552_pressure_observation_id" in pressure_handoff else pd.DataFrame()
        if len(fact) != 1 or len(hand) != 1:
            _issue(issues, "pressure_contract_propagation_mismatch", str(obs.get("v552_pressure_observation_id")))
            continue
        f = fact.iloc[0].to_dict()
        h = hand.iloc[0].to_dict()
        temp = temporal_sources[temporal_sources["v552_structural_fact_id"].astype(str).eq(str(f.get("v552_structural_fact_id")))] if "v552_structural_fact_id" in temporal_sources else pd.DataFrame()
        if len(temp) != 1:
            _issue(issues, "pressure_contract_propagation_mismatch", str(obs.get("v552_pressure_observation_id")))
            continue
        t = temp.iloc[0].to_dict()
        for field in contract_fields:
            if _canon(obs.get(field)) != _canon(f.get(field)) or _canon(f.get(field)) != _canon(t.get(field)):
                _issue(issues, "pressure_contract_propagation_mismatch", f"{obs.get('v552_pressure_observation_id')}:{field}")
                break
        if _boolish(h.get("direct_v553_authorization")):
            _issue(issues, "direct_v553_authorization")
        if _boolish(h.get("temporal_authority")):
            _issue(issues, "temporal_authorization")
        if _boolish(h.get("runtime_authority")):
            _issue(issues, "runtime_authorization")

    issues.extend(validate_v552_readiness_projection(
        readiness=readiness,
        components=components,
        observations=observations,
        facts=structural_facts,
        temporal_sources=temporal_sources,
        pressure_handoff=pressure_handoff,
        validation_issues=issues,
        execution_mode=execution_mode,
    ))
    return issues


def _load_written_frames(run_directory: Path, reader) -> dict[str, pd.DataFrame]:
    structural = run_directory / "structural"
    manifest = run_directory / "manifest"
    suffix = ".csv" if reader is read_v552_contract_csv else ".parquet"
    return {
        "components": reader(structural / f"v552_pressure_component_index{suffix}"),
        "observations": reader(structural / f"v552_pressure_observation_index{suffix}"),
        "structural_facts": reader(structural / f"v552_structural_fact_index{suffix}"),
        "temporal_sources": reader(structural / f"v552_temporal_key_source_index{suffix}"),
        "pressure_handoff": reader(structural / f"v552_to_v552j_pressure_observation_handoff_index{suffix}"),
        "readiness": reader(manifest / f"v552_readiness_report{suffix}"),
    }


def validate_written_v552_artifacts(
    *,
    run_directory: Path,
    atoms_csv_path: Path,
    atoms_parquet_path: Path,
    execution_mode: str,
) -> tuple[list[ValidationIssue], pd.DataFrame]:
    issues: list[ValidationIssue] = []
    csv_atoms = read_v552_contract_csv(atoms_csv_path)
    parquet_atoms = read_v552_contract_parquet(atoms_parquet_path)
    csv_frames = _load_written_frames(run_directory, read_v552_contract_csv)
    parquet_frames = _load_written_frames(run_directory, read_v552_contract_parquet)
    csv_issues = validate_v552_v2_1_4_outputs(input_atoms=csv_atoms, execution_mode=execution_mode, **csv_frames)
    parquet_issues = validate_v552_v2_1_4_outputs(input_atoms=parquet_atoms, execution_mode=execution_mode, **parquet_frames)
    issues.extend(ValidationIssue(f"csv_{issue.token}", issue.detail) for issue in csv_issues)
    issues.extend(ValidationIssue(f"parquet_{issue.token}", issue.detail) for issue in parquet_issues)
    rows: list[dict[str, Any]] = []
    csv_comp = csv_frames["components"]
    pq_comp = parquet_frames["components"]
    for _, csv_row in csv_comp.iterrows():
        key = _canon(csv_row.get("source_atom_id"))
        pq = pq_comp[pq_comp.get("source_atom_id", pd.Series(dtype=str)).map(_canon).eq(key)]
        pq_row = pq.iloc[0].to_dict() if len(pq) == 1 else {}
        csv_re = recompute_v552_pressure_component_id(csv_row.to_dict())
        pq_re = recompute_v552_pressure_component_id(pq_row) if pq_row else ""
        rows.append({
            "band": "",
            "scope": "",
            "artifact_type": "component_id",
            "stable_semantic_key": key,
            "csv_stored_value": csv_row.get("v552_pressure_component_id", ""),
            "csv_recomputed_value": csv_re,
            "parquet_stored_value": pq_row.get("v552_pressure_component_id", ""),
            "parquet_recomputed_value": pq_re,
            "csv_match": _canon(csv_row.get("v552_pressure_component_id")) == _canon(csv_re),
            "parquet_match": _canon(pq_row.get("v552_pressure_component_id")) == _canon(pq_re),
            "cross_format_match": _canon(csv_row.get("v552_pressure_component_id")) == _canon(pq_row.get("v552_pressure_component_id")),
        })
    csv_obs = csv_frames["observations"]
    pq_obs = parquet_frames["observations"]
    for _, csv_row in csv_obs.iterrows():
        key = _canon(csv_row.get("empirical_distribution_id"))
        pq = pq_obs[pq_obs.get("empirical_distribution_id", pd.Series(dtype=str)).map(_canon).eq(key)]
        pq_row = pq.iloc[0].to_dict() if len(pq) == 1 else {}
        csv_re = recompute_v552_pressure_observation_id(csv_row.to_dict())
        pq_re = recompute_v552_pressure_observation_id(pq_row) if pq_row else ""
        rows.append({
            "band": "",
            "scope": "",
            "artifact_type": "observation_id",
            "stable_semantic_key": key,
            "csv_stored_value": csv_row.get("v552_pressure_observation_id", ""),
            "csv_recomputed_value": csv_re,
            "parquet_stored_value": pq_row.get("v552_pressure_observation_id", ""),
            "parquet_recomputed_value": pq_re,
            "csv_match": _canon(csv_row.get("v552_pressure_observation_id")) == _canon(csv_re),
            "parquet_match": _canon(pq_row.get("v552_pressure_observation_id")) == _canon(pq_re),
            "cross_format_match": _canon(csv_row.get("v552_pressure_observation_id")) == _canon(pq_row.get("v552_pressure_observation_id")),
        })
        csv_group = csv_comp[csv_comp.get("empirical_distribution_id", pd.Series(dtype=str)).map(_canon).eq(key)]
        pq_group = pq_comp[pq_comp.get("empirical_distribution_id", pd.Series(dtype=str)).map(_canon).eq(key)]
        csv_sig = recompute_v552_response_surface_signature(csv_group.to_dict("records"))
        pq_sig = recompute_v552_response_surface_signature(pq_group.to_dict("records"))
        rows.append({
            "band": "",
            "scope": "",
            "artifact_type": "response_surface_signature",
            "stable_semantic_key": key,
            "csv_stored_value": csv_row.get("component_response_surface_signature", ""),
            "csv_recomputed_value": csv_sig,
            "parquet_stored_value": pq_row.get("component_response_surface_signature", ""),
            "parquet_recomputed_value": pq_sig,
            "csv_match": _canon(csv_row.get("component_response_surface_signature")) == _canon(csv_sig),
            "parquet_match": _canon(pq_row.get("component_response_surface_signature")) == _canon(pq_sig),
            "cross_format_match": _canon(csv_row.get("component_response_surface_signature")) == _canon(pq_row.get("component_response_surface_signature")),
        })
    audit = pd.DataFrame(rows)
    if not audit.empty:
        for field in ["csv_match", "parquet_match", "cross_format_match"]:
            bad = audit[~audit[field].astype(bool)]
            for _, row in bad.iterrows():
                _issue(issues, f"written_artifact_{field}_mismatch", f"{row.get('artifact_type')}:{row.get('stable_semantic_key')}")
    return issues, audit
