"""EE1 temporal owner.

Bridges the inherited sealed V553 temporal methods and the accepted T35
two-epoch historical selected-world consumer into one source-free two-period
comparability contract, keeping distinct: observation date, rule effective
date, rule publication date, requested as-of time, current selection and
archival validity.

The one genuinely new connection here (see EE1 genealogy): the inherited
ecosystem has no component that compares two periods' respondent population,
estimand, response topology, wording and design signatures before permitting
a historical delta.  `population_estimand_gate` supplies exactly that check,
following the exact-key discipline of the inherited V553 comparable temporal
key (ADAPT, not a new engine).
"""
from __future__ import annotations

import pandas as pd

from data.ddm_build_copy.ddm_v553_temporal_identity import (
    normalize_temporal_report_identity,
)
from data.ddm_build_copy.ddm_v553_harmonization import (
    build_v553_wave_harmonization_report,
)
from data.ddm_build_copy.ddm_v553_temporal_pressure import (
    _authorize_v553_multi_wave_key,
    _build_absence_noncomparability_register,
    _build_v553_cross_wave_delta_index,
    validate_v553_temporal_pressure_readiness,
)

COMPARABLE_AUTHORIZED = "COMPARABLE_AUTHORIZED"
COMPARABLE_PROBE_ONLY = "COMPARABLE_PROBE_ONLY"
NONCOMPARABLE_SOURCE_FAMILY = "NONCOMPARABLE_SOURCE_FAMILY"
NONCOMPARABLE_COUNTRY = "NONCOMPARABLE_COUNTRY"
NONCOMPARABLE_POPULATION_OR_ESTIMAND = "NONCOMPARABLE_POPULATION_OR_ESTIMAND"
NONCOMPARABLE_SOURCE_STRUCTURE = "NONCOMPARABLE_SOURCE_STRUCTURE"
FUTURE_RULE_AT_HISTORICAL_AS_OF = "FUTURE_RULE_AT_HISTORICAL_AS_OF"
FUTURE_EVIDENCE_AT_HISTORICAL_AS_OF = "FUTURE_EVIDENCE_AT_HISTORICAL_AS_OF"
OBSERVATION_AFTER_AS_OF = "OBSERVATION_AFTER_AS_OF"
MISSING_GAP_UNKNOWN = "MISSING_GAP_UNKNOWN"
DUPLICATE_YEAR_ANCHOR = "DUPLICATE_YEAR_ANCHOR"
ARCHIVAL_COMPARISON_ONLY__NOT_FRESH_USE = "ARCHIVAL_COMPARISON_ONLY__NOT_FRESH_USE"
CLOCK_OK = "CLOCK_OK"

IDENTITY_FIELDS = ("target_population", "estimand", "response_topology",
                   "wording_signature", "design_signature")


def identity_report(periods):
    """REUSE: the inherited V553 one-family/one-country/one-anchor-per-year law."""
    report = {
        "wave_rows": [
            dict(source=p["source"], canonical_wave=p["wave"],
                 country_code=p["country_code"], temporal_year=p["temporal_year"])
            for p in periods
        ]
    }
    try:
        normalized = normalize_temporal_report_identity(report)
    except Exception as exc:  # SurveyIdentityError subclasses ValueError
        message = str(exc)
        if "survey famil" in message:
            return dict(state=NONCOMPARABLE_SOURCE_FAMILY, reason=message)
        if "countr" in message:
            return dict(state=NONCOMPARABLE_COUNTRY, reason=message)
        if "anchor per calendar year" in message:
            return dict(state=DUPLICATE_YEAR_ANCHOR, reason=message)
        raise
    years = [int(row["temporal_year"]) for row in normalized["wave_rows"]]
    return dict(state="IDENTITY_OK", wave_count=normalized["wave_count"],
                years=sorted(years))


def population_estimand_gate(periods):
    """ADAPT: exact-key population/estimand identity (the missing connection)."""
    signatures = {tuple(str(p.get(field, "")) for field in IDENTITY_FIELDS)
                  for p in periods}
    if len(signatures) == 1:
        return dict(state="POPULATION_OK")
    first = periods[0]
    differing = sorted(
        field for field in IDENTITY_FIELDS
        if len({str(p.get(field, "")) for p in periods}) > 1
    )
    return dict(state=NONCOMPARABLE_POPULATION_OR_ESTIMAND,
                differing_fields=differing,
                reason="period populations/estimands/designs are not exact-key identical")


def clock_gate(period, comparison_asof):
    """Future knowledge may never enter an earlier historical comparison."""
    asof = str(comparison_asof)
    if str(period.get("rule_publication", "")) > asof and \
            period.get("rule_vintage") != "rev1_selected":
        return dict(state=FUTURE_RULE_AT_HISTORICAL_AS_OF,
                    rule_publication=period["rule_publication"], asof=asof)
    if str(period.get("evidence_publication", "")) > asof:
        return dict(state=FUTURE_EVIDENCE_AT_HISTORICAL_AS_OF,
                    evidence_publication=period["evidence_publication"], asof=asof)
    if int(period["observation_year"]) > int(asof[:4]):
        return dict(state=OBSERVATION_AFTER_AS_OF,
                    observation_year=period["observation_year"], asof=asof)
    return dict(state=CLOCK_OK)


def build_overlay_table(periods, overlays_dir):
    """Synthetic TEST_ONLY overlay CSVs + the harmonization table rows."""
    from pathlib import Path
    rows = []
    for period in periods:
        directory = Path(overlays_dir) / str(period["wave"])
        directory.mkdir(parents=True, exist_ok=True)
        semantic = directory / "semantic.csv"
        directionality = directory / "directionality.csv"
        position = directory / "position.csv"
        if period.get("disjoint_semantic"):
            semantic.write_text("other_column\nX\n")
            semantic_columns = ["other_column"]
        else:
            semantic.write_text(
                "semantic_role,semantic_lane,evidence_lane\n"
                "TARGET,RR,STRUCTURAL\n")
            semantic_columns = ["semantic_role", "semantic_lane", "evidence_lane"]
        directionality.write_text(
            "directionality_policy,signed_polarity_status\nSIGNED,SIGNED\n")
        position.write_text(
            "position_conditioning,structural_mapping_status\nSTANDALONE,RESOLVED\n")
        rows.append({
            "wave": str(period["wave"]),
            "canonical_wave": str(period["wave"]),
            "source": period["source"],
            "country_code": period["country_code"],
            "temporal_year": int(period["temporal_year"]),
            "wave_status": "complete",
            "overlay_paths": {
                "semantic": str(semantic),
                "directionality": str(directionality),
                "position": str(position)},
            "overlay_columns": {
                "semantic": semantic_columns,
                "directionality": ["directionality_policy", "signed_polarity_status"],
                "position": ["position_conditioning", "structural_mapping_status"]},
            "wave_relation_axis_ids": ["AXIS_EE1"],
            "wave_target_entity_ids": ["TARGET_EE1"],
            "wave_driver_facet_ids": ["DRIVER_EE1"],
            "wave_structural_channel_ids": ["CHANNEL_EE1"],
            "wave_horizon_constraint_ids": ["HORIZON_EE1"],
            "missing_authority_kinds": [],
        })
    return rows


def harmonization(table_rows):
    """REUSE: the inherited V553 harmonization report builder."""
    try:
        report = build_v553_wave_harmonization_report(pd.DataFrame(table_rows))
    except RuntimeError as exc:
        return dict(state="REPORT_REFUSED", reason=str(exc))
    return dict(state="REPORT_OK", report=report)


def multi_wave_authorization(report, wave_rows):
    """REUSE: the inherited V553 multi-wave key authorizer."""
    rows = []
    for period in wave_rows:
        rows.append({
            "wave_id": str(period["wave"]),
            "probe_ready_input_count": 1,
            "structural_dimension_status": "resolved",
            "comparable_key_grain": "relation_target_driver_semantic",
            "source_v552_structural_fact_lane": "structural_fact",
            "canonical_semantic_signature": "sem_canonical_ee1_v1",
            "structural_pressure_value": float(period["probe_value"]),
            "source_v552j_packet_ids_json": f'["pkt_{period["wave"]}"]',
        })
    return _authorize_v553_multi_wave_key(report, pd.DataFrame(rows))


def probe_or_authorized_delta(observation_rows):
    """REUSE: the inherited V553 cross-wave delta permission semantics."""
    frame = _build_v553_cross_wave_delta_index({}, pd.DataFrame(observation_rows),
                                               "ee1_run")
    if frame.empty:
        return None
    row = frame.iloc[0].to_dict()
    return {key: (value.item() if hasattr(value, "item") else value)
            for key, value in row.items()}


def delta_observation_rows(periods, *, authorized):
    rows = []
    for period in periods:
        rows.append({
            "wave_id": str(period["wave"]),
            "survey_year": int(period["temporal_year"]),
            "country": "ZZ",
            "comparable_temporal_key": "v553ck_ee1_demo",
            "authorized_structural_pressure_value": float(period["probe_value"]) if authorized else None,
            "probe_pressure_value": float(period["probe_value"]),
            "evidence_coverage_score": 0.7 + 0.1 * (int(period["temporal_year"]) - 2020) / 2.0,
            "confidence_score": 0.7,
            "authority_score": 0.5,
            "temporal_status": "observed_authorized_anchor" if authorized else "observed_probe_only",
        })
    return rows


def missing_gap_rows(years, *, allow_interpolation=False):
    """REUSE: the inherited V553 absence/noncomparability register."""
    pressure = pd.DataFrame({"temporal_year": [int(y) for y in years]})
    report = {
        "source": "TESTONLY_EE1_PANEL",
        "source_family": "TESTONLY_EE1_PANEL",
        "country_code": "ZZ",
        "required_authority_kinds": ["semantic", "directionality", "position"],
        "cross_wave_noncomparability_matrix": [],
        "wave_rows": [],
    }
    frame = _build_absence_noncomparability_register(
        report, pressure, pd.DataFrame(), allow_interpolation, "ee1_run")
    return frame.to_dict(orient="records")


def readiness_errors():
    """REUSE: the inherited V553 thin-layer readiness validation."""
    return validate_v553_temporal_pressure_readiness({})


def compare_periods(periods, comparison_asof, overlays_dir, *,
                    authorized_control=False):
    """The EE1 two-period verdict: identity -> population -> clock -> report."""
    identity = identity_report(periods)
    if identity["state"] != "IDENTITY_OK":
        return dict(state=identity["state"], identity=identity)
    population = population_estimand_gate(periods)
    if population["state"] != "POPULATION_OK":
        return dict(state=population["state"], identity=identity,
                    population=population)
    for period in periods:
        clock = clock_gate(period, comparison_asof)
        if clock["state"] != CLOCK_OK:
            return dict(state=clock["state"], identity=identity, clock=clock)
    gaps = missing_gap_rows([p["temporal_year"] for p in periods])
    gap_annotation = [int(row["year"]) for row in gaps]
    if gaps and any(p.get("annual_anchors_required") for p in periods):
        return dict(state=MISSING_GAP_UNKNOWN, identity=identity, gaps=gaps)
    table = build_overlay_table(periods, overlays_dir)
    report_result = harmonization(table)
    if report_result["state"] != "REPORT_OK":
        return dict(state=NONCOMPARABLE_SOURCE_STRUCTURE, identity=identity,
                    report_refusal=report_result["reason"])
    report = report_result["report"]
    if report["ready_for_v553"] and not report["cross_wave_noncomparability_matrix"]:
        authorization = multi_wave_authorization(report, periods)
        delta = probe_or_authorized_delta(
            delta_observation_rows(periods, authorized=authorized_control))
        state = (COMPARABLE_AUTHORIZED if authorized_control
                 else COMPARABLE_PROBE_ONLY)
        return dict(state=state, identity=identity, report=report,
                    authorization=authorization, delta=delta,
                    gap_annotation=gap_annotation)
    return dict(state=NONCOMPARABLE_SOURCE_STRUCTURE, identity=identity,
                report=report, gap_annotation=gap_annotation)
