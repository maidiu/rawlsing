"""Evaluate the historical V553 temporal/harmonization implementation.

This is a candidate-method assessment only.  It executes the exact sealed V553
modules against empty inputs to observe their typed refusal and their structural
scope; it does not compile a Ghana product, read source rows, or issue EE12.
"""
from __future__ import annotations

import bootstrap

bootstrap.install()

import pandas as pd

from data.ddm_build_copy import ddm_v553_harmonization as harmonization
from data.ddm_build_copy import ddm_v553_temporal_pressure as pressure


def evaluate():
    errors = pressure.validate_v553_temporal_pressure_readiness({})
    report = harmonization.build_v553_wave_harmonization_report(pd.DataFrame())
    deterministic_report = {
        key: report.get(key) for key in (
            "overall_status", "comparability_status",
            "comparison_authority_status", "harmonization_scope",
            "multiple_waves_present", "wave_count", "harmonization_score",
            "overlay_presence_score", "blocking_conditions")
    }
    return dict(
        schema="R35_T35_V553_CANDIDATE_METHOD_EVALUATION@1",
        modules=[
            dict(path="data/ddm_build_copy/ddm_v553_temporal_pressure.py",
                 contract="V553 thin temporal pressure / structural wave harmonization"),
            dict(path="data/ddm_build_copy/ddm_v553_harmonization.py",
                 contract="V553 wave descriptor harmonization table/report"),
        ],
        empty_readiness_error_count=len(errors),
        empty_readiness_first_error=errors[0] if errors else None,
        empty_readiness_last_error=errors[-1] if errors else None,
        empty_readiness_has_structural_missing_paths=any(
            "missing source wave anchor manifest path" in error or
            "missing v553 cross-wave delta index path" in error for error in errors),
        empty_harmonization_report=deterministic_report,
        has_structural_multiwave_key=hasattr(pressure, "_authorize_v553_multi_wave_key"),
        has_structural_cross_wave_delta=hasattr(pressure, "_build_v553_cross_wave_delta_index"),
        consumes_respondent_survey_rows=False,
        consumes_five_category_satisfaction=False,
        consumes_design_weights_psu=False,
        produces_survey_delta=False,
        candidate_verdict=(
            "V553_STRUCTURAL_TEMPORAL_HARMONIZATION_CANDIDATE__NOT_N8E_SURVEY_COMPARATOR"),
        reuse_decision=(
            "REUSE_AS_STRUCTURAL_TEMPORAL_CANDIDATE_ONLY__NO_GHANA_OR_N8E_USE"),
        n8e_authority_created=False,
        ghana_use=False,
        source_rows_read=False,
    )
