#!/usr/bin/env python3
"""Cross-stage V550/V551/V552 extraction diagnostics with typed state separation."""
from __future__ import annotations
from typing import Any, Mapping, Sequence
import pandas as pd
from data.ddm_build_copy.ddm_v550_metrics import evidence_stratum_v2_from_row, numeric_wrapper_audit_from_row

PASS, FAIL, UNKNOWN = "PASS", "FAIL", "UNKNOWN"
EVIDENCE_PRESENT = "EVIDENCE_PRESENT"
OBSERVED_ZERO = "OBSERVED_ZERO"
NO_APPLICABLE_EVIDENCE = "NO_APPLICABLE_EVIDENCE"
APPLICABLE_BUT_UNRESOLVED = "APPLICABLE_BUT_UNRESOLVED"
ALLOWED, REVIEW_REQUIRED, BLOCKED = "ALLOWED", "REVIEW_REQUIRED", "BLOCKED"
OUTCOME_COLS = ("terminal_outcome", "adjudication_outcome", "candidate_outcome", "promotability_outcome", "candidate_status", "adjudication_status", "status")
PROMOTABLE = {"PROMOTABLE", "PROMOTED", "CERTIFIED", "ATOM_EMITTED"}
NONPROMOTABLE = {"NONPROMOTABLE", "NONPROMOTABLE_REPAIRABLE", "REPAIR_REQUIRED", "UNRESOLVED", "BLOCKED"}
NOT_APPLICABLE = {"NOT_APPLICABLE", "NON_DIRECTIONAL", "OUTSIDE_DENOMINATOR"}


def _clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    return str(value).strip()


def _norm(value: Any) -> str:
    return _clean(value).upper().replace("-", "_").replace(" ", "_")


def _top_counts(frame: pd.DataFrame, column: str, limit: int = 5) -> list[dict[str, Any]]:
    if frame.empty or column not in frame.columns:
        return []
    counts = frame[column].fillna("").astype(str).value_counts().head(limit)
    return [{"value": str(v), "count": int(n)} for v, n in counts.items() if str(v).strip()]


def _numeric_wrapper_audit(frame: pd.DataFrame, run_id: str = "") -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for raw in frame.to_dict(orient="records"):
        row = pd.Series(raw)
        audit = numeric_wrapper_audit_from_row(row)
        rows.append({
            "run_id": run_id or _clean(row.get("run_id") or row.get("source_run_id")),
            "source": _clean(row.get("source")), "wave": _clean(row.get("wave")),
            "canonical_wave": _clean(row.get("canonical_wave")), "country_code": _clean(row.get("country_code")),
            "question_id": _clean(row.get("question_id")), "var_code": _clean(row.get("var_code")),
            "source_table": _clean(row.get("source_table")), "bridge_evidence_lane": _clean(row.get("bridge_evidence_lane")),
            "semantic_role": _clean(row.get("semantic_role")), "evidence_stratum": _clean(row.get("evidence_stratum")),
            "evidence_stratum_v2": _clean(row.get("evidence_stratum_v2")) or evidence_stratum_v2_from_row(
                bridge_evidence_lane=row.get("bridge_evidence_lane", ""), semantic_role=row.get("semantic_role", ""),
                v551_relation_evidence_eligible=row.get("v551_relation_evidence_eligible")),
            "numeric_like_label": bool(audit.get("numeric_like_label")), "numeric_family_compatible": bool(audit.get("numeric_family_compatible")),
            "numeric_wrapper_status": _clean(audit.get("numeric_wrapper_status")), "numeric_wrapper_reason": _clean(audit.get("numeric_wrapper_reason")),
            "numeric_wrapper_confidence": _clean(audit.get("numeric_wrapper_confidence")), "support_status": _clean(row.get("support_status")),
            "confidence_tier": _clean(row.get("confidence_tier")), "v551_relation_evidence_eligible": bool(row.get("v551_relation_evidence_eligible", False)),
            "v551_exclusion_reason": _clean(row.get("v551_exclusion_reason")), "source_row_hash": _clean(row.get("source_row_hash")), "n_rows": 1,
        })
    return pd.DataFrame(rows)


def _first_value(mapping: Mapping[str, Any], *names: str) -> Any:
    for name in names:
        if name in mapping and _clean(mapping.get(name)):
            return mapping.get(name)
    return None


def _frame_value(frame: pd.DataFrame, *names: str) -> Any:
    if frame.empty:
        return None
    for name in names:
        if name in frame.columns:
            for value in frame[name].tolist():
                if _clean(value):
                    return value
    return None


def _canon_integrity(value: Any) -> str:
    t = _norm(value)
    if t in {"PASS", "PASSED", "VALID", "SUCCESS", "SUCCEEDED", "INTEGRITY_PASS"}: return PASS
    if t in {"FAIL", "FAILED", "INVALID", "ERROR", "BLOCKED", "INTEGRITY_FAIL"}: return FAIL
    return UNKNOWN


def _canon_evidence(value: Any) -> str:
    t = _norm(value)
    if t in {OBSERVED_ZERO, "GENUINE_OBSERVED_ZERO", "OBSERVED_STRUCTURAL_ZERO"}: return OBSERVED_ZERO
    if t in {NO_APPLICABLE_EVIDENCE, "NO_DIRECTIONAL_EVIDENCE", "NOT_APPLICABLE"}: return NO_APPLICABLE_EVIDENCE
    if t in {APPLICABLE_BUT_UNRESOLVED, "UNRESOLVED_APPLICABLE_EVIDENCE", "REPAIR_REQUIRED"}: return APPLICABLE_BUT_UNRESOLVED
    if t in {EVIDENCE_PRESENT, "PRESENT", "OBSERVED", "PROMOTABLE_EVIDENCE"}: return EVIDENCE_PRESENT
    return UNKNOWN


def _canon_permission(value: Any) -> str:
    t = _norm(value)
    if t in {"ALLOWED", "ALLOW", "READY", "PERMITTED"}: return ALLOWED
    if t in {"REVIEW_REQUIRED", "REVIEW", "CONDITIONAL"}: return REVIEW_REQUIRED
    if t in {"BLOCKED", "DENIED", "STOP", "NOT_ALLOWED"}: return BLOCKED
    return UNKNOWN


def _producer_state(v551: Mapping[str, pd.DataFrame], manifest: Mapping[str, Any], loads: pd.DataFrame) -> dict[str, Any]:
    adjudication = v551.get("directional_candidate_adjudication", pd.DataFrame())
    coverage = v551.get("directional_distribution_coverage", pd.DataFrame())
    atoms = v551.get("relation_evidence_atoms", pd.DataFrame())
    outcomes = pd.Series(dtype=str)
    outcome_col = next((c for c in OUTCOME_COLS if c in adjudication.columns), "")
    if outcome_col:
        outcomes = adjudication[outcome_col].map(_norm)
    promotable = int(outcomes.isin(PROMOTABLE).sum()) if outcome_col else int(len(atoms))
    nonpromotable = int(outcomes.isin(NONPROMOTABLE).sum()) if outcome_col else 0
    not_applicable = int(outcomes.isin(NOT_APPLICABLE).sum()) if outcome_col else 0
    applicable = promotable + nonpromotable if outcome_col else 0
    count_source = f"directional_candidate_adjudication.{outcome_col}" if outcome_col else "legacy_atoms_only_candidate_count_unknown"
    if not coverage.empty:
        aliases = {
            "candidate_count": ("candidate_count", "applicability_candidate_count", "selected_substantive_count"),
            "applicable": ("directionally_applicable_count", "applicable_count", "directional_applicable_count"),
            "promotable": ("promotable_count", "promotable_candidate_count", "promotable_rows"),
            "nonpromotable": ("nonpromotable_count", "nonpromotable_candidate_count", "unresolved_count", "repair_count"),
            "not_applicable": ("not_applicable_count", "outside_denominator_count"),
        }
        vals: dict[str, int] = {}
        for key, names in aliases.items():
            for name in names:
                if name in coverage.columns:
                    nums = pd.to_numeric(coverage[name], errors="coerce").dropna()
                    if not nums.empty: vals[key] = int(nums.sum()); break
        if vals:
            promotable, nonpromotable, not_applicable = vals.get("promotable", promotable), vals.get("nonpromotable", nonpromotable), vals.get("not_applicable", not_applicable)
            applicable = vals.get("applicable", promotable + nonpromotable)
            candidate_count = vals.get("candidate_count", applicable + not_applicable)
            count_source = "directional_distribution_coverage"
        else:
            candidate_count = int(len(adjudication)) if outcome_col else 0
    else:
        candidate_count = int(len(adjudication)) if outcome_col else 0
    integrity = _canon_integrity(_first_value(manifest, "run_integrity_status", "producer_run_integrity_status") or _frame_value(coverage, "run_integrity_status"))
    if not loads.empty and "load_status" in loads.columns:
        relevant = loads[loads["stage"].map(_norm).eq("V551")] if "stage" in loads.columns else loads
        if relevant["load_status"].map(_norm).isin({"READ_ERROR", "CORRUPT", "SCHEMA_ERROR"}).any(): integrity = FAIL
    evidence = _canon_evidence(_first_value(manifest, "evidence_status", "typed_evidence_status", "directional_evidence_status") or _frame_value(coverage, "evidence_status", "typed_evidence_status", "directional_evidence_status") or _frame_value(atoms, "evidence_status", "typed_evidence_status", "directional_evidence_status"))
    authoritative_counts = count_source != "legacy_atoms_only_candidate_count_unknown"
    if evidence == UNKNOWN:
        explicit_zero = any(c in atoms.columns and atoms[c].astype(str).map(_norm).isin({"TRUE", "1", "YES"}).any() for c in ("observed_response_zero", "observed_zero", "is_observed_zero"))
        if explicit_zero: evidence = OBSERVED_ZERO
        elif authoritative_counts and applicable == 0: evidence = NO_APPLICABLE_EVIDENCE
        elif authoritative_counts and applicable > 0 and promotable == 0 and nonpromotable > 0: evidence = APPLICABLE_BUT_UNRESOLVED
        elif promotable > 0: evidence = EVIDENCE_PRESENT
    permission = _canon_permission(_first_value(manifest, "downstream_permission_status", "producer_downstream_permission_status") or _frame_value(coverage, "downstream_permission_status"))
    if integrity == FAIL: permission = BLOCKED
    coverage_status = _clean(_first_value(manifest, "coverage_status", "directional_coverage_status", "directional_adjudication_status") or _frame_value(coverage, "coverage_status", "directional_coverage_status", "directional_adjudication_status")) or "NOT_REPORTED"
    if integrity == FAIL: diagnostic = "compiler_failure"
    elif integrity != PASS: diagnostic = "integrity_unknown"
    elif evidence == NO_APPLICABLE_EVIDENCE: diagnostic = "valid_zero_promotable_no_applicable_evidence"
    elif evidence == APPLICABLE_BUT_UNRESOLVED: diagnostic = "valid_zero_promotable_applicable_but_unresolved"
    elif evidence == OBSERVED_ZERO: diagnostic = "valid_observed_zero"
    elif evidence == EVIDENCE_PRESENT: diagnostic = "valid_promotable_evidence"
    elif promotable == 0: diagnostic = "valid_zero_promotable_evidence_state_unknown"
    else: diagnostic = "valid_evidence_state_unknown"
    return {"run_integrity_status": integrity, "evidence_status": evidence, "downstream_permission_status": permission, "coverage_status": coverage_status,
            "candidate_count": candidate_count, "directionally_applicable_count": applicable, "promotable_count": promotable,
            "nonpromotable_count": nonpromotable, "not_applicable_count": not_applicable, "candidate_count_source": count_source,
            "legacy_relation_evidence_atom_count": int(len(atoms)), "diagnostic_status": diagnostic}


def build_v550_552_extraction_audit_package(*, run_id: str, source: str, wave: str, canonical_wave: str, country_code: str,
    v550_outputs: dict[str, pd.DataFrame] | None=None, v551_outputs: dict[str, pd.DataFrame] | None=None,
    v552_outputs: dict[str, pd.DataFrame] | None=None, v550j_outputs: dict[str, pd.DataFrame] | None=None,
    v551_manifest: Mapping[str, Any] | None=None, artifact_load_diagnostics: pd.DataFrame | Sequence[Mapping[str, Any]] | None=None) -> dict[str, pd.DataFrame]:
    v550, v551, v552, v550j = v550_outputs or {}, v551_outputs or {}, v552_outputs or {}, v550j_outputs or {}
    loads = artifact_load_diagnostics.copy() if isinstance(artifact_load_diagnostics, pd.DataFrame) else pd.DataFrame(list(artifact_load_diagnostics or []))
    v551_audit = v551.get("numeric_wrapper_audit", pd.DataFrame())
    if v551_audit.empty and "bridge" in v551: v551_audit = _numeric_wrapper_audit(v551["bridge"], run_id)
    directionality_gap = v552.get("v552_directionality_gap_surface", pd.DataFrame())
    status_pressure = v552.get("v552_status_pressure_review_surface", pd.DataFrame())
    carry = v550.get("question_carry_forward_summary", pd.DataFrame())
    if carry.empty and not v550.get("question_response_attitude_cloud", pd.DataFrame()).empty:
        cloud = v550["question_response_attitude_cloud"]
        carry = pd.DataFrame([{"run_id": run_id, "source": source, "wave": wave, "canonical_wave": canonical_wave, "country_code": country_code,
            "artifact_name": "question_response_attitude_cloud", "carry_forward_rows": int(len(cloud)),
            "support_status": _clean(cloud["support_status"].iloc[0]) if "support_status" in cloud.columns else "",
            "confidence_tier": _clean(cloud["confidence_tier"].iloc[0]) if "confidence_tier" in cloud.columns else ""}])
    state = _producer_state(v551, v551_manifest or {}, loads)
    gap_counts: dict[str, int] = {}
    for frame, col in ((directionality_gap, "gap_surface_reason"), (status_pressure, "status_pressure_reason")):
        if col in frame.columns:
            for value, count in frame[col].fillna("").astype(str).value_counts().items():
                if str(value).strip(): gap_counts[str(value)] = gap_counts.get(str(value), 0) + int(count)
    blocked_audit = v551.get("blocked_signal_audit", pd.DataFrame())
    top_blocking = _top_counts(blocked_audit, "gate_name") or _top_counts(blocked_audit, "blocked_signal_reason")
    failures = []
    if "numeric_wrapper_status" in v551_audit.columns:
        failures = _top_counts(v551_audit[v551_audit["numeric_wrapper_status"].astype(str).ne("wrapped_numeric")], "numeric_wrapper_reason")
    common = {"run_id": run_id, "source": source, "wave": wave, "canonical_wave": canonical_wave, "country_code": country_code}
    manifest_row = {**common, **state, "artifact_counts": {
        "v550_carry_forward_summary": len(carry), "v551_numeric_wrapper_audit": len(v551_audit),
        "v551_directional_candidate_adjudication": len(v551.get("directional_candidate_adjudication", pd.DataFrame())),
        "v551_relation_evidence_atoms": len(v551.get("relation_evidence_atoms", pd.DataFrame())),
        "v551_directional_distribution_coverage": len(v551.get("directional_distribution_coverage", pd.DataFrame())),
        "v552_directionality_gap_surface": len(directionality_gap), "v552_status_pressure_review_surface": len(status_pressure),
        "v550j_association_review_surface": len(v550j.get("joint_pattern_association_review_surface", pd.DataFrame()))}}
    readiness = {**common, "overall_status": state["diagnostic_status"], **{k:v for k,v in state.items() if k != "diagnostic_status"},
        "certified_count": state["promotable_count"], "reviewable_count": len(v551.get("relation_review_surface", pd.DataFrame())) + len(status_pressure),
        "blocked_count": len(blocked_audit), "provisional_count": len(directionality_gap), "mapping_pending_count": 0,
        "directionality_pending_count": len(directionality_gap), "numeric_only_count": int(v551_audit["numeric_wrapper_status"].astype(str).eq("wrapped_numeric").sum()) if "numeric_wrapper_status" in v551_audit.columns else 0,
        "proxy_only_count": 0, "status_only_count": len(status_pressure), "carry_forward_context_count": len(carry),
        "unsafe_for_downstream_count": len(blocked_audit), "top_recoverable_gaps": [{"value":v,"count":n} for v,n in sorted(gap_counts.items(), key=lambda x:(-x[1],x[0]))[:5]],
        "top_blocking_fields": top_blocking, "numeric_wrapper_failures": failures, "recommended_next_repairs": []}
    return {"manifest": pd.DataFrame([manifest_row]), "readiness_report": pd.DataFrame([readiness]), "artifact_load_audit": loads,
        "v550_carry_forward_summary": carry, "v551_numeric_wrapper_audit": v551_audit,
        "v552_directionality_gap_surface": directionality_gap, "v552_status_pressure_review_surface": status_pressure,
        "v550_552_numeric_wrapper_audit": _numeric_wrapper_audit(v551.get("bridge", pd.DataFrame()), run_id)}
