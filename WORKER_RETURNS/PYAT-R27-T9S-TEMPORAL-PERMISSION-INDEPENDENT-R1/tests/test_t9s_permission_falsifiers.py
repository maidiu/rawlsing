"""T9S Phase A — preregistered temporal-permission falsifiers and controls.

These tests are COMMITTED AND PUSHED BEFORE any T9D candidate code or output is
inspected.  Each falsifier states the exact input vector and the fixed expected
output derived independently from the frozen T9R oracle.  On the current T9C
adapter the falsifiers reproduce the T9R REDs; they are re-run unchanged against
T9D in Phase B.  No expected value here is edited to fit a candidate.
"""
from pathlib import Path
import pytest

import t9b_temporal as T
from t9s_binding import CapabilityUnavailable, archival_known_at_evaluate, granted_source_read

METHODS = [T.METHOD_M0_HOLD, T.METHOD_M1_INTERP, T.METHOD_M2_BACKOFF]
WORLD = T.StructuralWorld('SAME_WORLD', ('ROUTE_PARTICIPATION', 'ROUTE_DEFERRED_REVIEW'),
                          (), 'INSTITUTION')
GRANTED_WORLD = T.StructuralWorld('SAME_WORLD', ('ROUTE_PARTICIPATION', 'ROUTE_DEFERRED_REVIEW'),
                                  ('GRANT_YOUNG_PERSON_ACCESS',), 'INSTITUTION')


def wave(name, year, value, **kw):
    fields = dict(wave_id=name, source_family='ACTUAL_SOURCE', country='SYNTH_COUNTRY_A',
                  instrument='SYNTH_INSTRUMENT', edition='E1', cohort='COHORT_ALL',
                  observation_year=year, published_year=year, value=value)
    fields.update(kw)
    return T.Wave(**fields)


def case(waves, **kw):
    return T.TemporalCase(case_id='T9S', country='SYNTH_COUNTRY_A',
                          waves=tuple(waves), target_year=1995, **kw)


def open_routes(x):
    return [r for r in x.opportunity_ids if r != 'ROUTE_BLOCKED_NO_SUPPORT']


# ---------------------------------------------------------------------------
# F1 — unused future wave must not upgrade a held W0-only product's authority
# ---------------------------------------------------------------------------
@pytest.mark.parametrize('method', [T.METHOD_M0_HOLD, T.METHOD_M2_BACKOFF])
def test_F1_unused_future_wave_cannot_upgrade_held_product_authority(method):
    before = T.read_selected_world(GRANTED_WORLD, case([wave('W0', 1990, .2)]),
                                   method, 1995, retrospective=True)
    after = T.read_selected_world(
        GRANTED_WORLD, case([wave('W0', 1990, .2), wave('W1', 2000, .6)]),
        method, 1995, retrospective=True)
    assert after.value == before.value == 0.2
    assert after.basis_wave_ids == before.basis_wave_ids == ('W0',)
    assert after.temporal_key != T.AUTHORIZED_SPARSE_TEMPORAL_KEY
    assert not after.authorized_opportunity
    assert not open_routes(after)
    assert 'W1' in after.archive_context_wave_ids
    assert 'W1' not in after.basis_wave_ids


# ---------------------------------------------------------------------------
# F2 — empty actor grants must never open an authorized opportunity
# ---------------------------------------------------------------------------
@pytest.mark.parametrize('method', METHODS)
def test_F2_empty_actor_grants_cannot_authorize(method):
    x = T.read_selected_world(WORLD, case([wave('OLD', 1980, .2), wave('RECENT', 1990, .6)]),
                              method, 1995)
    assert not x.authorized_opportunity
    assert not open_routes(x)


# ---------------------------------------------------------------------------
# F3 — lag parser must return only real basis wave ids
# ---------------------------------------------------------------------------
def test_F3_lag_parser_does_not_swallow_rupture_suffix_as_wave_identity():
    c = case([wave('DELAYED', 1990, .8, published_year=2000)], ruptures=(1995,))
    x = T.evaluate(c, T.METHOD_M0_HOLD, clock_year=1997, retrospective=True)
    parsed = T.pub_lag_of(x)
    assert parsed == ('DELAYED',)
    assert set(parsed) <= set(x.basis_wave_ids)


# ---------------------------------------------------------------------------
# F4 — duplicate wave id must not rebind provenance to an excluded source
# ---------------------------------------------------------------------------
def test_F4_duplicate_wave_id_cannot_rebind_provenance_to_excluded_source():
    c = case([wave('DUPLICATE', 1990, .6),
              wave('DUPLICATE', 1980, .1, country='OTHER',
                   source_family='WRONG_SOURCE', edition='WRONG_EDITION')])
    x = T.read_selected_world(WORLD, c, T.METHOD_M0_HOLD, 1995)
    assert x.refused_code is not None or (
        x.provenance['source_family'] == 'ACTUAL_SOURCE' and x.provenance['edition'] == 'E1')


# ---------------------------------------------------------------------------
# F5 — archival known-at bound cannot admit not-yet-published support
# ---------------------------------------------------------------------------
def test_F5_archive_known_at_2020_cannot_use_2030_published():
    w = wave('W2030', 2020, .7, published_year=2030)
    c = case([w], target_year=2020)
    x = archival_known_at_evaluate(T, c, T.METHOD_M0_HOLD, 2020, 2020)
    # A wave published in 2030 cannot be an observed value at a 2020 archive bound.
    assert x.value is None or x.refused_code is not None


# ---------------------------------------------------------------------------
# F6 — source edition / currentness / owner grants must refuse, never resurrect
# ---------------------------------------------------------------------------
def test_F6_wrong_edition_grant_refuses():
    c = case([wave('VALID', 1990, .6)])
    x = granted_source_read(T, c, T.METHOD_M0_HOLD, 1995,
                            grant_edition='E2', grant_current=True, grant_owner='OWNER')
    assert x.refused_code is not None or not x.authorized_opportunity


def test_F6_expired_grant_refuses():
    c = case([wave('VALID', 1990, .6)])
    x = granted_source_read(T, c, T.METHOD_M0_HOLD, 1995,
                            grant_edition='E1', grant_current=False, grant_owner='OWNER')
    assert x.refused_code is not None or not x.authorized_opportunity


def test_F6_wrong_owner_refuses():
    c = case([wave('VALID', 1990, .6)])
    x = granted_source_read(T, c, T.METHOD_M0_HOLD, 1995,
                            grant_edition='E1', grant_current=True, grant_owner='WRONG_OWNER')
    assert x.refused_code is not None or not x.authorized_opportunity


# ---------------------------------------------------------------------------
# Positive controls — behaviour that must stay correct while the falsifiers close
# ---------------------------------------------------------------------------
def test_P1_asof_single_anchor_is_probe_without_future_knowledge():
    x = T.read_selected_world(WORLD, case([wave('W0', 1990, .2)]), T.METHOD_M0_HOLD, 1995)
    assert x.basis_wave_ids == ('W0',)
    assert x.temporal_key == T.PROBE_ONLY_TEMPORAL_KEY
    assert not x.authorized_opportunity
    assert not open_routes(x)


def test_P2_asof_endpoint_with_two_anchors_is_authorized():
    x = T.read_selected_world(WORLD, case([wave('W0', 1990, .2), wave('W1', 2000, .6)]),
                              T.METHOD_M0_HOLD, 2000)
    assert x.basis_wave_ids == ('W1',)
    assert x.temporal_key == T.AUTHORIZED_SPARSE_TEMPORAL_KEY


def test_P3_retrospective_interpolation_is_probe_and_not_observed():
    x = T.evaluate(case([wave('W0', 1990, .2), wave('W1', 2000, .6)]),
                   T.METHOD_M1_INTERP, clock_year=1995, retrospective=True)
    assert x.value == 0.4
    assert x.not_observed is True
    assert x.temporal_key == T.PROBE_ONLY_TEMPORAL_KEY


def test_P4_missing_is_not_zero():
    x = T.evaluate(case([wave('NAN', 1990, float('nan'))]), T.METHOD_M0_HOLD, 1995)
    assert x.value is None and x.refused_code == 'MISSING_OBSERVATION_NOT_ZERO'
    y = T.evaluate(case([wave('ZERO', 1990, 0.0)]), T.METHOD_M0_HOLD, 1995)
    assert y.value == 0.0 and y.refused_code is None


def test_P5_excluded_first_distinct_id_keeps_valid_provenance():
    c = case([wave('BAD', 1990, .1, country='OTHER', source_family='WRONG_SOURCE',
                   edition='WRONG_EDITION'),
              wave('GOOD', 1990, .6)])
    x = T.read_selected_world(WORLD, c, T.METHOD_M0_HOLD, 1995)
    assert x.provenance['source_family'] == 'ACTUAL_SOURCE'
    assert x.provenance['edition'] == 'E1'


def test_P6_structural_route_removal_is_material():
    a = T.read_selected_world(WORLD, case([wave('W0', 1990, .2)]), T.METHOD_M0_HOLD, 1995)
    reduced = T.StructuralWorld('SAME_WORLD', ('ROUTE_DEFERRED_REVIEW',), (), 'INSTITUTION')
    b = T.read_selected_world(reduced, case([wave('W0', 1990, .2)]), T.METHOD_M0_HOLD, 1995)
    assert T.structurally_identical(a, b) is False
