"""Validation for the canonical V552 v3 structural-pressure contract.

The validator checks compiler-emitted V552 v3 fields against V551 v3 producer
surfaces.  It does not invoke the obsolete v2.1.4 scale engine and does not
make compiler-version strings or ghost contract signatures semantic authority.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from data.ddm_build_copy.ddm_v552_structural import (
    OBSERVED_PRESSURE_STATUSES,
    V551_COMPLETE,
    V551_REPAIR_DEBT,
    V552_COMPILER_VERSION,
    V552_EPSILON,
    V552_PRESSURE_FORMULA_ID,
    V552_PRESSURE_FORMULA_VERSION,
    V552_PRESSURE_SCALE_ID,
    V552_SCHEMA_VERSION,
    recompute_v552_component_measurement_hash,
    recompute_v552_pressure_measurement_hash,
    resolve_v552_signed_component,
    select_v552_distribution_weight_basis,
    validate_v552_v551_input_contract,
)


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str = ""


def _issue(code: str, message: str = "") -> ValidationIssue:
    return ValidationIssue(code, message)


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


def _num(value: Any) -> float | None:
    try:
        if value is None or pd.isna(value):
            return None
        return float(value)
    except Exception:
        return None


def _bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return _clean(value).casefold() in {"1", "true", "yes", "y", "on"}


def _json_list(value: Any) -> list[Any]:
    try:
        parsed = json.loads(_clean(value) or "[]")
        return parsed if isinstance(parsed, list) else []
    except Exception:
        return []


def _frame(outputs: dict[str, pd.DataFrame], name: str) -> pd.DataFrame:
    value = outputs.get(name)
    return value if isinstance(value, pd.DataFrame) else pd.DataFrame()


def _validate_component_projection(
    atoms: pd.DataFrame,
    components: pd.DataFrame,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if len(components) != len(atoms):
        issues.append(_issue("component_count_not_equal_promotable_atom_count"))
        return issues
    if atoms.empty:
        return issues
    by_atom = atoms.set_index("atom_id", drop=False).to_dict("index")
    observed_ids = components.get("source_atom_id", pd.Series(dtype=str)).fillna("").astype(str)
    if observed_ids.duplicated().any():
        issues.append(_issue("duplicate_v552_component_source_atom"))
    for row in components.to_dict("records"):
        atom_id = _clean(row.get("source_atom_id"))
        atom = by_atom.get(atom_id)
        if atom is None:
            issues.append(_issue("component_source_atom_missing", atom_id))
            continue
        transform = resolve_v552_signed_component(atom)
        actual = _num(row.get("canonical_signed_component"))
        expected = transform.canonical_signed_component
        if transform.reason:
            issues.append(_issue("v551_canonical_projection_rejected_by_v552", transform.reason))
            continue
        if expected is None or actual is None or abs(actual - expected) > V552_EPSILON:
            issues.append(_issue("component_signed_value_not_v551_canonical", atom_id))
        if _clean(row.get("v551_signed_side")).casefold() != _clean(atom.get("v551_signed_side")).casefold():
            issues.append(_issue("component_v551_signed_side_mismatch", atom_id))
        if abs((_num(row.get("v551_signed_intensity")) or 0.0) - (_num(atom.get("v551_signed_intensity")) or 0.0)) > V552_EPSILON:
            issues.append(_issue("component_v551_signed_intensity_mismatch", atom_id))
        if _clean(atom.get("v551_signed_side")).casefold() == "neutral":
            if actual is None or abs(actual) > V552_EPSILON:
                issues.append(_issue("neutral_component_not_zero", atom_id))
            if _clean(row.get("component_pressure_status")) != "V551_CANONICAL_COMPONENT":
                issues.append(_issue("neutral_component_illegally_blocked_by_raw_intensity", atom_id))
        if _clean(row.get("scale_encoding_class")) != "V551_CANONICAL_SIGNED_PROJECTION":
            issues.append(_issue("v552_scale_reinterpretation_detected", atom_id))
        if _clean(row.get("scale_encoding_status")) != "CONSUMED_V551_CANONICAL_PROJECTION":
            issues.append(_issue("v552_scale_projection_status_invalid", atom_id))
        expected_hash = recompute_v552_component_measurement_hash(row)
        if _clean(row.get("component_measurement_hash")) != expected_hash:
            issues.append(_issue("component_measurement_hash_mismatch", atom_id))
    return issues


def _validate_distribution_observations(
    coverage: pd.DataFrame,
    adjudication: pd.DataFrame,
    components: pd.DataFrame,
    observations: pd.DataFrame,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if len(observations) != len(coverage):
        issues.append(_issue("pressure_observation_count_not_equal_v551_coverage_count"))
    if coverage.empty:
        if not observations.empty:
            issues.append(_issue("observations_present_without_v551_coverage"))
        return issues
    obs_by_dist = observations.set_index("empirical_distribution_id", drop=False).to_dict("index") if not observations.empty else {}
    comp_groups = {str(k): g.copy() for k, g in components.groupby("empirical_distribution_id", dropna=False, sort=True)} if not components.empty else {}
    adj_counts = adjudication.groupby("empirical_distribution_id", dropna=False).size().to_dict() if not adjudication.empty else {}
    for cov in coverage.to_dict("records"):
        dist = _clean(cov.get("empirical_distribution_id"))
        obs = obs_by_dist.get(dist)
        if obs is None:
            issues.append(_issue("missing_pressure_observation_for_v551_distribution", dist))
            continue
        applicable = int(_num(cov.get("applicable_candidate_count")) or 0)
        promotable = int(_num(cov.get("promotable_candidate_count")) or 0)
        nonpromotable = int(_num(cov.get("nonpromotable_candidate_count")) or 0)
        comp = comp_groups.get(dist, pd.DataFrame())
        if int(adj_counts.get(dist, 0)) != applicable:
            issues.append(_issue("adjudication_count_not_conserved_at_v552", dist))
        if len(comp) != promotable:
            issues.append(_issue("promotable_component_count_not_conserved_at_v552", dist))
        for field in [
            "selected_surface_status", "directional_adjudication_status", "applicable_candidate_count",
            "promotable_candidate_count", "nonpromotable_candidate_count", "selected_substantive_n_unweighted",
            "promotable_n_unweighted", "nonpromotable_n_unweighted", "neutral_n_unweighted",
        ]:
            if field in obs and field in cov:
                a, b = obs.get(field), cov.get(field)
                if field.endswith("count"):
                    if int(_num(a) or 0) != int(_num(b) or 0):
                        issues.append(_issue(f"coverage_field_mismatch:{field}", dist))
                elif field.endswith("unweighted"):
                    if abs((_num(a) or 0.0) - (_num(b) or 0.0)) > V552_EPSILON:
                        issues.append(_issue(f"coverage_field_mismatch:{field}", dist))
                elif _clean(a) != _clean(b):
                    issues.append(_issue(f"coverage_field_mismatch:{field}", dist))
        directional_status = _clean(cov.get("directional_adjudication_status"))
        repair_debt = directional_status in V551_REPAIR_DEBT or nonpromotable > 0
        score = _num(obs.get("pressure_score"))
        score_status = _clean(obs.get("pressure_score_status"))
        permission = _clean(obs.get("downstream_permission_status"))
        if repair_debt:
            if score is not None:
                issues.append(_issue("repair_debt_pressure_must_be_null", dist))
            if score_status != "APPLICABLE_BUT_UNRESOLVED":
                issues.append(_issue("repair_debt_not_typed_unresolved", dist))
            if permission != "DENY":
                issues.append(_issue("repair_debt_permission_not_denied", dist))
            unresolved_u = _num(obs.get("unresolved_n_unweighted")) or 0.0
            expected_u = _num(cov.get("nonpromotable_n_unweighted")) or 0.0
            if abs(unresolved_u - expected_u) > V552_EPSILON:
                issues.append(_issue("unresolved_unweighted_mass_not_preserved", dist))
            if not comp.empty and pd.to_numeric(comp.get("distribution_weight_normalized", pd.Series(dtype=float)), errors="coerce").notna().any():
                issues.append(_issue("repair_debt_components_were_renormalized", dist))
        elif directional_status == V551_COMPLETE and promotable > 0:
            if score_status not in OBSERVED_PRESSURE_STATUSES:
                issues.append(_issue("complete_adjudication_not_observed", dist))
            if score is None:
                issues.append(_issue("complete_adjudication_pressure_missing", dist))
            if permission not in {"ALLOW", "DENY"}:
                issues.append(_issue("complete_adjudication_permission_invalid", dist))
            basis, raw_weights, reason = select_v552_distribution_weight_basis(comp)
            if raw_weights is None:
                issues.append(_issue("validator_missing_weight_basis_for_observed_pressure", dist + ":" + reason))
            else:
                weights = raw_weights / float(raw_weights.sum())
                signed = pd.to_numeric(comp["canonical_signed_component"], errors="coerce")
                expected = float((weights.reset_index(drop=True) * signed.reset_index(drop=True)).sum())
                expected = 0.0 if abs(expected) <= V552_EPSILON else expected
                if score is None or abs(score - expected) > V552_EPSILON:
                    issues.append(_issue("pressure_score_recompute_mismatch", dist))
                neutral_mask = signed.reset_index(drop=True).abs() <= V552_EPSILON
                neutral_share = float(weights.reset_index(drop=True)[neutral_mask].sum())
                if abs((_num(obs.get("neutral_component_share")) or 0.0) - neutral_share) > V552_EPSILON:
                    issues.append(_issue("neutral_mass_not_in_pressure_denominator", dist))
                if score == 0.0 and score_status != "OBSERVED_ZERO":
                    issues.append(_issue("true_zero_not_typed_observed_zero", dist))
                if score != 0.0 and score_status != "OBSERVED_NONZERO":
                    issues.append(_issue("nonzero_pressure_status_mismatch", dist))
                selected_status = _clean(obs.get("response_surface_completeness_status"))
                if selected_status == "PARTIAL_SELECTED_RESPONSE_CATEGORY_COVERAGE" and _clean(obs.get("pressure_measure_class")) != "conditional_selected_response_surface_pressure":
                    issues.append(_issue("selected_surface_partiality_not_labeled_conditional", dist))
        expected_hash = recompute_v552_pressure_measurement_hash(obs, comp)
        if _clean(obs.get("pressure_measurement_hash")) != expected_hash:
            issues.append(_issue("pressure_measurement_hash_mismatch", dist))
    return issues


def _expected_run_state(observations: pd.DataFrame, coverage: pd.DataFrame) -> tuple[str, str, str]:
    if not observations.empty and observations["pressure_score_status"].isin(OBSERVED_PRESSURE_STATUSES).any():
        return "PASS", "PRESENT", "ALLOW"
    if not observations.empty and observations["pressure_score_status"].eq("APPLICABLE_BUT_UNRESOLVED").any():
        return "PASS", "APPLICABLE_UNRESOLVED", "DENY"
    if not coverage.empty:
        return "PASS", "APPLICABLE_UNRESOLVED", "DENY"
    return "PASS", "NOT_APPLICABLE", "NOT_APPLICABLE"


def _validate_readiness(
    outputs: dict[str, pd.DataFrame],
    coverage: pd.DataFrame,
    execution_mode: str,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    readiness = _frame(outputs, "v552_readiness_report")
    observations = _frame(outputs, "v552_pressure_observation_index")
    if len(readiness) != 1:
        return [_issue("v552_readiness_report_must_have_one_row")]
    row = readiness.iloc[0].to_dict()
    integrity, evidence, capability_permission = _expected_run_state(observations, coverage)
    effective_permission = capability_permission
    if execution_mode == "diagnostic" and capability_permission == "ALLOW":
        effective_permission = "DENY"
    if _clean(row.get("run_integrity_status")) != integrity:
        issues.append(_issue("run_integrity_status_mismatch"))
    if _clean(row.get("evidence_status")) != evidence:
        issues.append(_issue("evidence_status_mismatch"))
    if _clean(row.get("downstream_permission_status")) != effective_permission:
        issues.append(_issue("downstream_permission_status_mismatch"))
    if evidence == "NOT_APPLICABLE" and integrity != "PASS":
        issues.append(_issue("valid_empty_wrongly_failed_run_integrity"))
    if evidence == "APPLICABLE_UNRESOLVED" and effective_permission != "DENY":
        issues.append(_issue("unresolved_run_permission_not_denied"))
    return issues


def _validate_no_direct_v553(outputs: dict[str, pd.DataFrame]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for name in ["v552_pressure_observation_index", "v552_structural_fact_index", "v552_temporal_key_source_index", "v552_to_v552j_pressure_observation_handoff_index"]:
        frame = _frame(outputs, name)
        if frame.empty:
            continue
        for column in ["allowed_for_v553_temporal_field", "direct_v553_authorization"]:
            if column in frame.columns and frame[column].fillna(False).map(_bool).any():
                issues.append(_issue("direct_v553_authorization_present", name + ":" + column))
    return issues


def validate_v552_v2_1_4_outputs(
    outputs: dict[str, pd.DataFrame],
    *,
    input_atoms: pd.DataFrame,
    directional_coverage: pd.DataFrame | None = None,
    directional_adjudication: pd.DataFrame | None = None,
    execution_mode: str = "acceptance",
    written_artifacts: dict[str, Any] | None = None,
    **_: Any,
) -> list[ValidationIssue]:
    """Compatibility name for the live v3 validator."""
    coverage = directional_coverage if directional_coverage is not None else pd.DataFrame()
    adjudication = directional_adjudication if directional_adjudication is not None else pd.DataFrame()
    issues: list[ValidationIssue] = []
    contract = validate_v552_v551_input_contract(input_atoms, coverage, adjudication)
    if contract["status"] != "PASS":
        issues.extend(_issue("v551_input_contract_invalid", error) for error in contract["errors"])
        return sorted(set(issues), key=lambda item: (item.code, item.message))
    components = _frame(outputs, "v552_pressure_component_index")
    observations = _frame(outputs, "v552_pressure_observation_index")
    issues.extend(_validate_component_projection(input_atoms, components))
    issues.extend(_validate_distribution_observations(coverage, adjudication, components, observations))
    issues.extend(_validate_readiness(outputs, coverage, execution_mode))
    issues.extend(_validate_no_direct_v553(outputs))
    if written_artifacts:
        issues.extend(validate_written_artifacts(written_artifacts))
    unique = {(issue.code, issue.message): issue for issue in issues}
    return [unique[key] for key in sorted(unique)]


def validate_v552_outputs(*args: Any, **kwargs: Any) -> list[ValidationIssue]:
    return validate_v552_v2_1_4_outputs(*args, **kwargs)


def validate_written_artifacts(written_artifacts: dict[str, Any]) -> list[ValidationIssue]:
    """Validate only actual serialized artifacts; no ghost contract fields."""
    issues: list[ValidationIssue] = []
    for name, spec in written_artifacts.items():
        if not isinstance(spec, dict):
            continue
        parquet = spec.get("parquet") or spec.get("path")
        if parquet:
            path = Path(parquet)
            if path.suffix.lower() != ".parquet":
                issues.append(_issue("canonical_artifact_not_parquet", name))
            elif not path.exists():
                issues.append(_issue("canonical_artifact_missing", name))
    return issues


def issues_to_strings(issues: list[ValidationIssue]) -> list[str]:
    return [issue.code + (":" + issue.message if issue.message else "") for issue in issues]
