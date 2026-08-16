#!/usr/bin/env python3
"""V550-V552 extraction diagnostics bound to the canonical V551 v3.0 contract.

This module is diagnostic infrastructure. It preserves the producer's typed
boundary state, independently verifies the canonical V551 adjudication/atom/
coverage surfaces, and reports observed zero as an observation property rather
than an absence or integrity state.
"""
from __future__ import annotations

import json
from typing import Any, Mapping, Sequence

import pandas as pd

from data.ddm_build_copy.ddm_pipeline_boundary_contract import (
    PIPELINE_BOUNDARY_CONTRACT_VERSION,
)

V551_SCHEMA_VERSION = "v3.0"
V551_COMPILER_VERSION = "v3.0"
V551_CANONICAL_ARTIFACTS = (
    "directional_candidate_adjudication",
    "relation_evidence_atoms",
    "directional_distribution_coverage",
)

RUN_INTEGRITY_STATUSES = {"PASS", "FAIL"}
EVIDENCE_STATUSES = {"PRESENT", "VALID_EMPTY", "NOT_APPLICABLE", "APPLICABLE_UNRESOLVED"}
DOWNSTREAM_PERMISSION_STATUSES = {"ALLOW", "DENY", "NOT_APPLICABLE"}
ADJUDICATION_OUTCOMES = {"PROMOTABLE", "NONPROMOTABLE_REPAIRABLE", "NOT_APPLICABLE"}
COVERAGE_STATUSES = {"COMPLETE", "NO_PROMOTABLE", "PARTIAL_WITH_REPAIR_DEBT"}

COMPILER_FAILURE = "COMPILER_FAILURE"
NO_APPLICABLE_EVIDENCE = "NO_APPLICABLE_EVIDENCE"
APPLICABLE_BUT_UNRESOLVED = "APPLICABLE_BUT_UNRESOLVED"
OBSERVED_ZERO = "OBSERVED_ZERO"
PROMOTABLE_EVIDENCE = "PROMOTABLE_EVIDENCE"
PROMOTABLE_EVIDENCE_WITH_OBSERVED_ZERO = "PROMOTABLE_EVIDENCE_WITH_OBSERVED_ZERO"
VALID_EMPTY = "VALID_EMPTY"

ADJUDICATION_REQUIRED_COLUMNS = {
    "candidate_id",
    "empirical_distribution_id",
    "directional_applicability_status",
    "adjudication_outcome",
    "promotable",
    "schema_version",
    "compiler_version",
}
ATOM_REQUIRED_COLUMNS = {
    "candidate_id",
    "empirical_distribution_id",
    "response_intensity_status",
    "v551_signed_side",
    "v551_signed_intensity",
    "schema_version",
    "compiler_version",
}
COVERAGE_REQUIRED_COLUMNS = {
    "empirical_distribution_id",
    "applicable_candidate_count",
    "promotable_candidate_count",
    "nonpromotable_candidate_count",
    "directional_adjudication_status",
    "candidate_count_conserved",
    "unweighted_mass_conserved",
    "weighted_mass_conserved",
    "schema_version",
    "compiler_version",
}

_LOAD_FAILURE_STATUSES = {
    "MISSING",
    "READ_ERROR",
    "HASH_MISMATCH",
    "ROW_COUNT_MISMATCH",
    "SCHEMA_MISMATCH",
    "DECLARATION_ERROR",
    "CONTRACT_ERROR",
    "IDENTITY_ERROR",
}


def _clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    text = str(value).strip()
    return "" if text.lower() in {"nan", "none", "null"} else text


def _bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return _clean(value).lower() in {"1", "true", "t", "yes", "y", "on"}


def _int_value(mapping: Mapping[str, Any], key: str) -> int | None:
    if key not in mapping:
        return None
    try:
        value = mapping.get(key)
        if value is None or pd.isna(value):
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def _require_columns(frame: pd.DataFrame, required: set[str], artifact: str, issues: list[str]) -> None:
    missing = sorted(required - set(frame.columns))
    if missing:
        issues.append(f"{artifact}:missing_columns={','.join(missing)}")


def _require_v3_versions(frame: pd.DataFrame, artifact: str, issues: list[str]) -> None:
    if "schema_version" in frame.columns and not frame.empty:
        if not frame["schema_version"].fillna("").astype(str).eq(V551_SCHEMA_VERSION).all():
            issues.append(f"{artifact}:schema_version_mismatch")
    if "compiler_version" in frame.columns and not frame.empty:
        if not frame["compiler_version"].fillna("").astype(str).eq(V551_COMPILER_VERSION).all():
            issues.append(f"{artifact}:compiler_version_mismatch")


def _coverage_status(coverage: pd.DataFrame, producer_evidence_status: str) -> tuple[str, dict[str, int]]:
    if coverage.empty:
        if producer_evidence_status == "NOT_APPLICABLE":
            return "NOT_APPLICABLE", {}
        if producer_evidence_status == "VALID_EMPTY":
            return "VALID_EMPTY", {}
        return "NO_COVERAGE_ROWS", {}
    counts = (
        coverage["directional_adjudication_status"]
        .fillna("")
        .astype(str)
        .value_counts(dropna=False)
        .to_dict()
    )
    cleaned = {str(key): int(value) for key, value in counts.items() if str(key)}
    keys = set(cleaned)
    if len(keys) == 1:
        return next(iter(keys)), cleaned
    if "PARTIAL_WITH_REPAIR_DEBT" in keys:
        return "MIXED_WITH_REPAIR_DEBT", cleaned
    if "NO_PROMOTABLE" in keys:
        return "MIXED_WITH_NO_PROMOTABLE", cleaned
    return "MIXED", cleaned


def _producer_v551_v3_state(
    v551: Mapping[str, pd.DataFrame],
    manifest: Mapping[str, Any],
    loads: pd.DataFrame,
) -> dict[str, Any]:
    adjudication = v551.get("directional_candidate_adjudication", pd.DataFrame())
    atoms = v551.get("relation_evidence_atoms", pd.DataFrame())
    coverage = v551.get("directional_distribution_coverage", pd.DataFrame())

    issues: list[str] = []
    contract_version = _clean(manifest.get("contract_version") or manifest.get("boundary_contract_version"))
    producer_integrity = _clean(manifest.get("run_integrity_status")).upper()
    producer_evidence = _clean(manifest.get("evidence_status")).upper()
    producer_permission = _clean(manifest.get("downstream_permission_status")).upper()

    if contract_version != PIPELINE_BOUNDARY_CONTRACT_VERSION:
        issues.append(f"manifest:contract_version={contract_version or '<missing>'}")
    if _clean(manifest.get("schema_version")) != V551_SCHEMA_VERSION:
        issues.append(f"manifest:schema_version={_clean(manifest.get('schema_version')) or '<missing>'}")
    if _clean(manifest.get("compiler_version")) != V551_COMPILER_VERSION:
        issues.append(f"manifest:compiler_version={_clean(manifest.get('compiler_version')) or '<missing>'}")
    if producer_integrity not in RUN_INTEGRITY_STATUSES:
        issues.append(f"manifest:run_integrity_status={producer_integrity or '<missing>'}")
    if producer_evidence not in EVIDENCE_STATUSES:
        issues.append(f"manifest:evidence_status={producer_evidence or '<missing>'}")
    if producer_permission not in DOWNSTREAM_PERMISSION_STATUSES:
        issues.append(f"manifest:downstream_permission_status={producer_permission or '<missing>'}")
    if producer_integrity == "FAIL" and producer_permission == "ALLOW":
        issues.append("manifest:allow_with_failed_integrity")
    if producer_evidence == "PRESENT" and producer_permission != "ALLOW":
        issues.append("manifest:present_evidence_without_allow")
    if producer_evidence == "APPLICABLE_UNRESOLVED" and producer_permission != "DENY":
        issues.append("manifest:unresolved_evidence_without_deny")
    if producer_evidence == "NOT_APPLICABLE" and producer_permission != "NOT_APPLICABLE":
        issues.append("manifest:not_applicable_permission_mismatch")

    canonical_names = manifest.get("canonical_artifact_names")
    if not isinstance(canonical_names, list) or tuple(canonical_names) != V551_CANONICAL_ARTIFACTS:
        issues.append("manifest:canonical_artifact_names_mismatch")

    _require_columns(adjudication, ADJUDICATION_REQUIRED_COLUMNS, "directional_candidate_adjudication", issues)
    _require_columns(atoms, ATOM_REQUIRED_COLUMNS, "relation_evidence_atoms", issues)
    _require_columns(coverage, COVERAGE_REQUIRED_COLUMNS, "directional_distribution_coverage", issues)
    _require_v3_versions(adjudication, "directional_candidate_adjudication", issues)
    _require_v3_versions(atoms, "relation_evidence_atoms", issues)
    _require_v3_versions(coverage, "directional_distribution_coverage", issues)

    outcomes = (
        adjudication["adjudication_outcome"].fillna("").astype(str)
        if "adjudication_outcome" in adjudication.columns
        else pd.Series(dtype=str)
    )
    invalid_outcomes = sorted(set(outcomes) - ADJUDICATION_OUTCOMES)
    if invalid_outcomes:
        issues.append("directional_candidate_adjudication:invalid_outcomes=" + ",".join(invalid_outcomes))

    promotable_count = int(outcomes.eq("PROMOTABLE").sum())
    repair_debt_count = int(outcomes.eq("NONPROMOTABLE_REPAIRABLE").sum())
    not_applicable_count = int(outcomes.eq("NOT_APPLICABLE").sum())
    candidate_count = int(len(adjudication))
    directionally_applicable_count = promotable_count + repair_debt_count
    producer_nonpromotable_count = repair_debt_count + not_applicable_count

    if "promotable" in adjudication.columns and not adjudication.empty:
        flags = adjudication["promotable"].map(_bool)
        if not flags.equals(outcomes.eq("PROMOTABLE")):
            issues.append("directional_candidate_adjudication:promotable_flag_mismatch")
    if candidate_count != promotable_count + repair_debt_count + not_applicable_count:
        issues.append("directional_candidate_adjudication:candidate_partition_mismatch")
    if len(atoms) != promotable_count:
        issues.append("relation_evidence_atoms:atom_promotable_count_mismatch")

    coverage_conservation_pass = True
    if not coverage.empty:
        coverage_status_values = set(coverage["directional_adjudication_status"].fillna("").astype(str))
        invalid_coverage = sorted(coverage_status_values - COVERAGE_STATUSES)
        if invalid_coverage:
            issues.append("directional_distribution_coverage:invalid_statuses=" + ",".join(invalid_coverage))
        coverage_applicable = int(pd.to_numeric(coverage["applicable_candidate_count"], errors="coerce").fillna(0).sum())
        coverage_promotable = int(pd.to_numeric(coverage["promotable_candidate_count"], errors="coerce").fillna(0).sum())
        coverage_nonpromotable = int(pd.to_numeric(coverage["nonpromotable_candidate_count"], errors="coerce").fillna(0).sum())
        conservation_cols = ("candidate_count_conserved", "unweighted_mass_conserved", "weighted_mass_conserved")
        coverage_conservation_pass = all(coverage[column].map(_bool).all() for column in conservation_cols)
        if not coverage_conservation_pass:
            issues.append("directional_distribution_coverage:conservation_failure")
        if coverage_applicable != candidate_count:
            issues.append("directional_distribution_coverage:applicable_candidate_count_mismatch")
        if coverage_promotable != promotable_count:
            issues.append("directional_distribution_coverage:promotable_candidate_count_mismatch")
        if coverage_nonpromotable != producer_nonpromotable_count:
            issues.append("directional_distribution_coverage:nonpromotable_candidate_count_mismatch")
    elif candidate_count > 0:
        issues.append("directional_distribution_coverage:missing_rows_for_candidates")

    manifest_count_expectations = {
        "candidate_count": candidate_count,
        "promotable_candidate_count": promotable_count,
        "nonpromotable_candidate_count": producer_nonpromotable_count,
        "atom_count": int(len(atoms)),
        "distribution_coverage_rows": int(len(coverage)),
    }
    manifest_count_matches: dict[str, bool] = {}
    for key, expected in manifest_count_expectations.items():
        observed = _int_value(manifest, key)
        match = observed == expected
        manifest_count_matches[key] = match
        if not match:
            issues.append(f"manifest:{key}_mismatch:expected={expected}:actual={observed}")

    load_failures: list[str] = []
    if not loads.empty and {"stage", "load_status"}.issubset(loads.columns):
        v551_loads = loads[loads["stage"].fillna("").astype(str).str.lower().eq("v551")]
        for row in v551_loads.to_dict("records"):
            status = _clean(row.get("load_status")).upper()
            if status in _LOAD_FAILURE_STATUSES:
                load_failures.append(f"{_clean(row.get('artifact_name'))}:{status}")
    if load_failures:
        issues.extend("load:" + failure for failure in load_failures)

    signed = (
        pd.to_numeric(atoms["v551_signed_intensity"], errors="coerce")
        if "v551_signed_intensity" in atoms.columns
        else pd.Series(dtype=float)
    )
    observed_zero_mask = signed.eq(0.0)
    observed_zero_atom_count = int(observed_zero_mask.sum())
    observed_nonzero_atom_count = int(signed.notna().sum() - observed_zero_atom_count)
    neutral_zero_count = 0
    raw_missing_zero_count = 0
    if not atoms.empty and "v551_signed_side" in atoms.columns:
        neutral_zero_count = int((atoms["v551_signed_side"].fillna("").astype(str).eq("neutral") & observed_zero_mask).sum())
    if not atoms.empty and "response_intensity_status" in atoms.columns:
        raw_missing_zero_count = int((atoms["response_intensity_status"].fillna("").astype(str).eq("MISSING") & observed_zero_mask).sum())

    if producer_evidence == "PRESENT" and promotable_count == 0:
        issues.append("manifest:PRESENT_without_promotable_candidate")
    if producer_evidence == "APPLICABLE_UNRESOLVED" and not (candidate_count > 0 and promotable_count == 0 and repair_debt_count > 0):
        issues.append("manifest:APPLICABLE_UNRESOLVED_count_semantics_mismatch")
    if producer_evidence == "NOT_APPLICABLE" and candidate_count != 0:
        issues.append("manifest:NOT_APPLICABLE_with_candidates")

    effective_integrity = "FAIL" if issues else producer_integrity
    effective_permission = "DENY" if effective_integrity != "PASS" else producer_permission
    coverage_status, coverage_status_counts = _coverage_status(coverage, producer_evidence)

    if effective_integrity != "PASS":
        diagnostic = COMPILER_FAILURE
    elif producer_evidence == "NOT_APPLICABLE":
        diagnostic = NO_APPLICABLE_EVIDENCE
    elif producer_evidence == "APPLICABLE_UNRESOLVED":
        diagnostic = APPLICABLE_BUT_UNRESOLVED
    elif producer_evidence == "VALID_EMPTY":
        diagnostic = VALID_EMPTY
    elif producer_evidence == "PRESENT" and observed_zero_atom_count == len(atoms) and len(atoms) > 0:
        diagnostic = OBSERVED_ZERO
    elif producer_evidence == "PRESENT" and observed_zero_atom_count > 0:
        diagnostic = PROMOTABLE_EVIDENCE_WITH_OBSERVED_ZERO
    else:
        diagnostic = PROMOTABLE_EVIDENCE

    return {
        "producer_contract_version": contract_version,
        "producer_schema_version": _clean(manifest.get("schema_version")),
        "producer_compiler_version": _clean(manifest.get("compiler_version")),
        "producer_run_integrity_status": producer_integrity,
        "producer_evidence_status": producer_evidence,
        "producer_downstream_permission_status": producer_permission,
        "run_integrity_status": effective_integrity,
        "evidence_status": producer_evidence,
        "downstream_permission_status": effective_permission,
        "candidate_count": candidate_count,
        "directionally_applicable_count": directionally_applicable_count,
        "promotable_count": promotable_count,
        "nonpromotable_count": repair_debt_count,
        "repair_debt_count": repair_debt_count,
        "not_applicable_count": not_applicable_count,
        "relation_evidence_atom_count": int(len(atoms)),
        "observed_zero_atom_count": observed_zero_atom_count,
        "observed_nonzero_atom_count": observed_nonzero_atom_count,
        "neutral_observed_zero_atom_count": neutral_zero_count,
        "raw_missing_observed_zero_atom_count": raw_missing_zero_count,
        "coverage_status": coverage_status,
        "coverage_status_counts_json": json.dumps(coverage_status_counts, sort_keys=True),
        "coverage_conservation_status": "PASS" if coverage_conservation_pass else "FAIL",
        "manifest_count_matches_json": json.dumps(manifest_count_matches, sort_keys=True),
        "audit_contract_status": "PASS" if not issues else "FAIL",
        "audit_contract_issues_json": json.dumps(issues, sort_keys=True),
        "diagnostic_status": diagnostic,
    }


def build_v550_552_extraction_audit_package(
    *,
    run_id: str,
    source: str,
    wave: str,
    canonical_wave: str,
    country_code: str,
    v550_outputs: dict[str, pd.DataFrame] | None = None,
    v551_outputs: dict[str, pd.DataFrame] | None = None,
    v552_outputs: dict[str, pd.DataFrame] | None = None,
    v550j_outputs: dict[str, pd.DataFrame] | None = None,
    v551_manifest: Mapping[str, Any] | None = None,
    artifact_load_diagnostics: pd.DataFrame | Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, pd.DataFrame]:
    v550 = v550_outputs or {}
    v551 = v551_outputs or {}
    v552 = v552_outputs or {}
    v550j = v550j_outputs or {}
    loads = (
        artifact_load_diagnostics.copy()
        if isinstance(artifact_load_diagnostics, pd.DataFrame)
        else pd.DataFrame(list(artifact_load_diagnostics or []))
    )

    carry = v550.get("question_carry_forward_summary", pd.DataFrame())
    if carry.empty:
        cloud = v550.get("question_response_attitude_cloud", pd.DataFrame())
        if not cloud.empty:
            carry = pd.DataFrame(
                [{
                    "run_id": run_id,
                    "source": source,
                    "wave": wave,
                    "canonical_wave": canonical_wave,
                    "country_code": country_code,
                    "artifact_name": "question_response_attitude_cloud",
                    "carry_forward_rows": int(len(cloud)),
                }]
            )

    directionality_gap = v552.get("v552_directionality_gap_surface", pd.DataFrame())
    status_pressure = v552.get("v552_status_pressure_review_surface", pd.DataFrame())
    state = _producer_v551_v3_state(v551, v551_manifest or {}, loads)

    gap_counts: dict[str, int] = {}
    for frame, column in (
        (directionality_gap, "gap_surface_reason"),
        (status_pressure, "status_pressure_reason"),
    ):
        if column in frame.columns:
            for value, count in frame[column].fillna("").astype(str).value_counts().items():
                if str(value).strip():
                    gap_counts[str(value)] = gap_counts.get(str(value), 0) + int(count)

    common = {
        "run_id": run_id,
        "source": source,
        "wave": wave,
        "canonical_wave": canonical_wave,
        "country_code": country_code,
    }
    artifact_counts = {
        "v550_carry_forward_summary": int(len(carry)),
        "v551_directional_candidate_adjudication": int(len(v551.get("directional_candidate_adjudication", pd.DataFrame()))),
        "v551_relation_evidence_atoms": int(len(v551.get("relation_evidence_atoms", pd.DataFrame()))),
        "v551_directional_distribution_coverage": int(len(v551.get("directional_distribution_coverage", pd.DataFrame()))),
        "v552_directionality_gap_surface": int(len(directionality_gap)),
        "v552_status_pressure_review_surface": int(len(status_pressure)),
        "v550j_association_review_surface": int(len(v550j.get("joint_pattern_association_review_surface", pd.DataFrame()))),
    }

    readiness = {
        **common,
        **state,
        "overall_status": state["diagnostic_status"],
        "top_recoverable_gaps_json": json.dumps(
            [
                {"value": value, "count": count}
                for value, count in sorted(gap_counts.items(), key=lambda item: (-item[1], item[0]))[:5]
            ],
            sort_keys=True,
        ),
    }
    manifest_row = {
        **common,
        **state,
        "artifact_counts_json": json.dumps(artifact_counts, sort_keys=True),
    }

    adjudication = v551.get("directional_candidate_adjudication", pd.DataFrame())
    if not adjudication.empty and "adjudication_outcome" in adjudication.columns:
        candidate_summary = (
            adjudication.groupby("adjudication_outcome", dropna=False)
            .size()
            .reset_index(name="candidate_count")
        )
    else:
        candidate_summary = pd.DataFrame(columns=["adjudication_outcome", "candidate_count"])

    coverage = v551.get("directional_distribution_coverage", pd.DataFrame())
    if not coverage.empty and "directional_adjudication_status" in coverage.columns:
        coverage_summary = (
            coverage.groupby("directional_adjudication_status", dropna=False)
            .agg(
                distribution_count=("empirical_distribution_id", "size"),
                applicable_candidate_count=("applicable_candidate_count", "sum"),
                promotable_candidate_count=("promotable_candidate_count", "sum"),
                nonpromotable_candidate_count=("nonpromotable_candidate_count", "sum"),
            )
            .reset_index()
        )
    else:
        coverage_summary = pd.DataFrame(
            columns=[
                "directional_adjudication_status",
                "distribution_count",
                "applicable_candidate_count",
                "promotable_candidate_count",
                "nonpromotable_candidate_count",
            ]
        )

    return {
        "manifest": pd.DataFrame([manifest_row]),
        "readiness_report": pd.DataFrame([readiness]),
        "artifact_load_audit": loads,
        "v551_candidate_adjudication_summary": candidate_summary,
        "v551_distribution_coverage_summary": coverage_summary,
        "v550_carry_forward_summary": carry,
        "v552_directionality_gap_surface": directionality_gap,
        "v552_status_pressure_review_surface": status_pressure,
    }
