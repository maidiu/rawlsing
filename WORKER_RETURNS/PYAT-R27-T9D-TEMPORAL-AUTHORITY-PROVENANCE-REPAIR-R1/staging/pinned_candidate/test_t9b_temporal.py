"""PYAT R18 T9B — frozen-expectation temporal court.

Asserts only what 01_PREDECLARED_SERIES_CLOCK_ORACLE.json froze before any T9B
experiment. A falsified prediction is reported as falsified, never edited.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

RET = Path(__file__).resolve().parent
sys.path.insert(0, str(RET))
sys.path.insert(0, str(RET / "native"))

import t9b_temporal as T                                   # noqa: E402

ORACLE = json.loads((RET / "01_PREDECLARED_SERIES_CLOCK_ORACLE.json").read_text())
LEDGER = json.loads((RET / "evidence/native_source_ledger.json").read_text())

C = "SYNTH_COUNTRY_A"


def wave(i, year, value, country=C, cohort="COHORT_ALL", published=None,
         instrument="SYNTH_INSTRUMENT", revoked=False, archived=False):
    return T.Wave(wave_id=f"W{i}", source_family="SYNTH_FAMILY", country=country,
                  instrument=instrument, edition="E1", cohort=cohort,
                  observation_year=year,
                  published_year=year if published is None else published,
                  value=value, revoked=revoked, archived_nonrenewed=archived)


TC1 = T.TemporalCase("TC1", C, (wave(0, 1990, 0.20), wave(1, 2000, 0.60)), target_year=1995)
TC2 = T.TemporalCase("TC2", C, (wave(0, 1990, 0.50), wave(1, 2000, 0.50)), target_year=1995)
TC3 = T.TemporalCase("TC3", C, (wave(0, 1990, 0.30), wave(1, 2000, 0.80)),
                     ruptures=(1995,), target_year=1995)
TC4 = T.TemporalCase("TC4", C, (wave(0, 1990, 0.40, country="SYNTH_COUNTRY_B", cohort="C_B"),
                               wave(1, 1990, 0.80, country="SYNTH_COUNTRY_C", cohort="C_C")),
                     target_year=1995, harmonize_countries=True)
TC5 = T.TemporalCase("TC5", C, (wave(0, 2010, 0.90, published=2015),), target_year=2012)

STRUCT = T.StructuralWorld(
    world_id="W_SYNTH_INSTITUTION",
    structural_routes=("ROUTE_REDUCED_BURDEN", "ROUTE_PARTICIPATION", "ROUTE_DEFERRED_REVIEW"),
    access_grants=("GRANT_YOUNG_PERSON_ACCESS",), institution="SYNTH_INSTITUTION")


# ======================================================== custody
def test_native_closure_verified():
    assert len(LEDGER) == 1259
    assert all(r["verified"] for r in LEDGER)


def test_temporal_primitives_are_inherited_verbatim_not_reimplemented():
    import data.ddm_build_copy.ddm_v553_temporal_pressure as v
    assert T._interp is v._interp
    assert T._pressure_band is v._pressure_band
    assert T._bounded_score is v._bounded_score
    assert T.AUTHORIZED_SPARSE_TEMPORAL_KEY == v.AUTHORIZED_SPARSE_TEMPORAL_KEY
    assert T.BLOCKED_TEMPORAL_KEY == v.BLOCKED_TEMPORAL_KEY


def test_imports_land_inside_this_return():
    import data.ddm_build_copy.ddm_v553_temporal_pressure as v
    assert str(RET) in v.__file__, f"AMBIENT IMPORT LEAK: {v.__file__}"


def test_inherited_interpolation_is_exact_linear():
    assert T._interp(0.0, 1.0, 0.25) == 0.25
    assert T._interp(0.20, 0.60, 0.5) == pytest.approx(0.40)


# ======================================================== TP1 trend
def test_tp1_trend_interior_value_and_hold_disagree():
    retro = T.evaluate(TC1, T.METHOD_M1_INTERP, retrospective=True)
    hold = T.evaluate(TC1, T.METHOD_M0_HOLD, retrospective=True)
    assert retro.value == pytest.approx(0.40)
    assert hold.value == pytest.approx(0.20)
    assert retro.value != hold.value
    assert retro.uncertainty.startswith("INTERPOLATED_NOT_OBSERVED")
    assert retro.temporal_key == T.PROBE_ONLY_TEMPORAL_KEY


def test_tp1b_strict_known_at_clock_makes_interpolation_structurally_impossible():
    """A right anchor observed later is published later, so AS_OF cannot interpolate."""
    asof = T.evaluate(TC1, T.METHOD_M1_INTERP)
    assert asof.uncertainty == "TERMINAL_NO_RIGHT_ANCHOR"
    assert asof.value == pytest.approx(0.20)


# ======================================================== TP2 null
def test_tp2_null_path_manufactures_no_trend():
    m0 = T.evaluate(TC2, T.METHOD_M0_HOLD, retrospective=True)
    m1 = T.evaluate(TC2, T.METHOD_M1_INTERP, retrospective=True)
    assert m0.value == m1.value == pytest.approx(0.50)


def test_tp2b_no_fake_high_resolution_signal():
    v = T.evaluate(TC1, T.METHOD_M1_INTERP, retrospective=True)
    assert T._pressure_band(v.value) in {"low", "medium", "high", "none"}
    assert isinstance(v.value, float)
    # the interpolated value is explicitly NOT an observation
    assert "NOT_OBSERVED" in v.uncertainty


# ======================================================== TP3 discontinuity
def test_tp3_rupture_bracket_refuses_smooth_interpolation():
    out = T.evaluate(TC3, T.METHOD_M1_INTERP, retrospective=True)
    assert out.refused_code == "RUPTURE_BRACKET_REFUSED"
    assert out.value is None
    assert out.temporal_key == T.BLOCKED_TEMPORAL_KEY


def test_tp3b_hold_still_works_across_a_rupture():
    out = T.evaluate(TC3, T.METHOD_M0_HOLD, retrospective=True)
    assert out.value == pytest.approx(0.30)
    assert out.refused_code is None


# ======================================================== TP4 geography
def test_tp4_incompatible_geography_is_refused_not_pooled():
    ok, code, _ = T.harmonization_check(TC4)
    assert ok is False and code == "NON_HARMONIZABLE_GEOMETRY"
    out = T.evaluate(TC4, T.METHOD_M0_HOLD)
    assert out.refused_code == "NON_HARMONIZABLE_GEOMETRY"
    assert out.value is None


# ======================================================== TP5 leak
def test_tp5_future_publication_never_enters_an_as_of_historical_read():
    out = T.evaluate(TC5, T.METHOD_M0_HOLD)          # clock 2012, published 2015
    assert out.refused_code == "NO_TEMPORAL_SUPPORT"
    assert out.value is None


def test_tp5b_retrospective_read_flags_publication_lag_rather_than_pretending():
    out = T.evaluate(TC5, T.METHOD_M0_HOLD, retrospective=True)
    assert out.value == pytest.approx(0.90)
    assert "PUBLICATION_LAG" in out.uncertainty
    assert "published AFTER" in out.detail


# ======================================================== TP8 alternatives
def test_tp8_backoff_equals_hold_and_differs_from_interpolation():
    m2 = T.evaluate(TC1, T.METHOD_M2_BACKOFF, retrospective=True)
    m0 = T.evaluate(TC1, T.METHOD_M0_HOLD, retrospective=True)
    m1 = T.evaluate(TC1, T.METHOD_M1_INTERP, retrospective=True)
    assert m2.value == m0.value
    assert m2.value != m1.value
    assert m2.uncertainty.startswith("BACKOFF_")


def test_tp8b_backoff_width_widens_uncertainty():
    wide = T.TemporalCase("W", C, (wave(0, 1990, 0.3), wave(1, 2020, 0.7)), target_year=1995)
    narrow = T.TemporalCase("N", C, (wave(0, 1990, 0.3), wave(1, 1992, 0.7)), target_year=1995)
    assert "WIDE" in T.evaluate(wide, T.METHOD_M2_BACKOFF, retrospective=True).uncertainty
    assert "WIDE" not in T.evaluate(narrow, T.METHOD_M2_BACKOFF, retrospective=True).uncertainty


# ======================================================== TP6 two-time consumer
def test_tp6_two_historical_clocks_give_materially_different_opportunities():
    early = T.read_selected_world(STRUCT, TC1, T.METHOD_M1_INTERP, 1990, retrospective=True)
    late = T.read_selected_world(STRUCT, TC1, T.METHOD_M1_INTERP, 2000, retrospective=True)
    assert T.materially_different(early, late)
    assert early.opportunity_ids != late.opportunity_ids


def test_tp6b_structural_and_access_world_is_provably_unchanged():
    early = T.read_selected_world(STRUCT, TC1, T.METHOD_M1_INTERP, 1990, retrospective=True)
    late = T.read_selected_world(STRUCT, TC1, T.METHOD_M1_INTERP, 2000, retrospective=True)
    assert T.structurally_identical(early, late)
    assert early.provenance["access_grants"] == late.provenance["access_grants"]
    assert early.provenance["grain"] == late.provenance["grain"] == "structural_channel_exact"


def test_tp7_every_value_carries_full_provenance_and_no_calibration_claim():
    for clock in (1990, 2000):
        r = T.read_selected_world(STRUCT, TC1, T.METHOD_M1_INTERP, clock, retrospective=True)
        p = r.provenance
        for k in ("world_id", "institution", "grain", "source_family", "instrument",
                  "cohort", "country", "edition", "query_clock", "clock_question",
                  "synthetic", "observed_temporal_calibration"):
            assert k in p, k
        assert p["synthetic"] is True
        assert p["observed_temporal_calibration"] is False
        assert p["t8f3_assignment_preserved"] == "8079f69778eb4a2e6f30b246e3ec445dc161ae15"


# ======================================================== hostiles
def test_hostile_revoked_source_is_not_used():
    case = T.TemporalCase("REV", C, (wave(0, 1990, 0.8, revoked=True),), target_year=1995)
    assert T.evaluate(case, T.METHOD_M0_HOLD, retrospective=True).refused_code == "NO_TEMPORAL_SUPPORT"


def test_hostile_archived_nonrenewal_is_not_used():
    case = T.TemporalCase("ARC", C, (wave(0, 1990, 0.8, archived=True),), target_year=1995)
    assert T.evaluate(case, T.METHOD_M0_HOLD, retrospective=True).refused_code == "NO_TEMPORAL_SUPPORT"


def test_hostile_wrong_instrument_yields_no_support():
    case = T.TemporalCase("INS", C, (wave(0, 1990, 0.8, instrument="OTHER"),),
                          target_year=1995, instrument="SYNTH_INSTRUMENT")
    assert T.evaluate(case, T.METHOD_M0_HOLD, retrospective=True).refused_code == "NO_TEMPORAL_SUPPORT"


def test_hostile_wrong_cohort_yields_no_support():
    case = T.TemporalCase("COH", C, (wave(0, 1990, 0.8, cohort="OTHER"),),
                          target_year=1995, cohort="COHORT_ALL")
    assert T.evaluate(case, T.METHOD_M0_HOLD, retrospective=True).refused_code == "NO_TEMPORAL_SUPPORT"


def test_hostile_query_before_every_observation_is_refused_as_of_and_probe_only_archival():
    case = T.TemporalCase("EARLY", C, (wave(0, 1990, 0.5),), target_year=1980)
    as_of = T.evaluate(case, T.METHOD_M0_HOLD)
    assert as_of.refused_code == "NO_TEMPORAL_SUPPORT"
    assert as_of.temporal_key == T.BLOCKED_TEMPORAL_KEY
    archival = T.evaluate(case, T.METHOD_M0_HOLD, retrospective=True)
    assert archival.temporal_key == T.PROBE_ONLY_TEMPORAL_KEY
    assert archival.refused_code == "NO_PRIOR_KNOWN_AT_WAVE"


def test_hostile_contradictory_causal_clock_is_refused_not_guessed():
    case = T.TemporalCase("CONTRA", C, (wave(0, 2010, 0.9, published=2015),), target_year=2012)
    assert T.evaluate(case, T.METHOD_M0_HOLD).refused_code == "NO_TEMPORAL_SUPPORT"


def test_hostile_changed_temporal_source_with_same_structural_world_only_moves_the_channel():
    alt = T.TemporalCase("ALT", C, (wave(0, 1990, 0.90), wave(1, 2000, 0.95)), target_year=1995)
    a = T.read_selected_world(STRUCT, TC1, T.METHOD_M1_INTERP, 1995, retrospective=True)
    b = T.read_selected_world(STRUCT, alt, T.METHOD_M1_INTERP, 1995, retrospective=True)
    assert T.structurally_identical(a, b)
    assert a.opportunity_ids != b.opportunity_ids


def test_hostile_ambient_import_shadowing_is_detectable():
    import data.ddm_build_copy as dd
    assert str(dd.__file__).startswith(str(RET / "native"))


def test_t8f3_assignment_is_preserved_not_duplicated():
    assert T.T8F3_ASSIGNMENT == "8079f69778eb4a2e6f30b246e3ec445dc161ae15"
    assert ORACLE["prohibitions"]["T8F3_source_claim_assignment_preserved"].startswith("8079f697")


def test_oracle_is_frozen_and_all_five_cases_present():
    assert ORACLE["status"].startswith("FROZEN_BEFORE")
    assert set(ORACLE["frozen_temporal_cases"]) == {"TC1_TREND", "TC2_NULL_STABILITY",
                                                    "TC3_DISCONTINUITY_COHORT",
                                                    "TC4_INCOMPATIBLE_GEOGRAPHY",
                                                    "TC5_FUTURE_LEAK"}