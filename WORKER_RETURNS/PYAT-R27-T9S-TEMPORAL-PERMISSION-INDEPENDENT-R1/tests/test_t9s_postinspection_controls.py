"""T9S Phase B — additional post-inspection adversarial controls.

These are authored AFTER inspecting the T9D repair (they are NOT part of the
Phase A preregistration) and probe the attack surfaces the T9D wake named:
unused-future authority at other clocks/methods, the entitlement gate on
held/interpolated products, duplicate identity with both copies admissible,
capability honesty under partial/empty SourceGrant claims, and the
lag/rupture/missing identity invariant.
"""
import pytest
import t9b_temporal as T


def wave(name, year, value, **kw):
    f = dict(wave_id=name, source_family='ACTUAL_SOURCE', country='SYNTH_COUNTRY_A',
             instrument='SYNTH_INSTRUMENT', edition='E1', cohort='COHORT_ALL',
             observation_year=year, published_year=year, value=value)
    f.update(kw)
    return T.Wave(**f)


def case(waves, **kw):
    return T.TemporalCase(case_id='T9S_B', country='SYNTH_COUNTRY_A',
                          waves=tuple(waves), **kw)


WORLD = T.StructuralWorld('W', ('ROUTE_PARTICIPATION', 'ROUTE_DEFERRED_REVIEW'),
                          (), 'INSTITUTION')
GRANTED = T.StructuralWorld('W', ('ROUTE_PARTICIPATION', 'ROUTE_DEFERRED_REVIEW'),
                            ('GRANT',), 'INSTITUTION')
METHODS = [T.METHOD_M0_HOLD, T.METHOD_M1_INTERP, T.METHOD_M2_BACKOFF]


def open_routes(x):
    return [r for r in x.opportunity_ids if r != 'ROUTE_BLOCKED_NO_SUPPORT']


# 1. unused future at other HELD clocks (M0/M2 only) --------------------------
# A HELD product is a query at a non-anchor year.  M1 is excluded here because a
# later right anchor legitimately switches M1 from terminal-hold to interpolation,
# which is a real change of estimate, not an authority upgrade.
@pytest.mark.parametrize('clock', [1995, 2005])
@pytest.mark.parametrize('method', [T.METHOD_M0_HOLD, T.METHOD_M2_BACKOFF])
def test_unused_future_wave_never_changes_held_product(method, clock):
    base = [w for w in (wave('W0', 1990, .2), wave('W1', 2000, .6))
            if w.observation_year <= clock]
    extended = [wave('W0', 1990, .2), wave('W1', 2000, .6), wave('W2', 2010, .7)]
    before = T.read_selected_world(GRANTED, case(base), method, clock, retrospective=True)
    after = T.read_selected_world(GRANTED, case(extended), method, clock, retrospective=True)
    assert after.basis_wave_ids == before.basis_wave_ids
    assert after.temporal_key == before.temporal_key == T.PROBE_ONLY_TEMPORAL_KEY
    assert after.authorized_opportunity == before.authorized_opportunity == False
    assert after.opportunity_ids == before.opportunity_ids == ('ROUTE_BLOCKED_NO_SUPPORT',)


# 2. a present grant on a held/interpolated product still opens nothing --------
@pytest.mark.parametrize('method', METHODS)
def test_entitlement_grant_on_interpolated_product_opens_nothing(method):
    x = T.read_selected_world(GRANTED,
                              case([wave('W0', 1990, .2), wave('W1', 2000, .6)]),
                              method, 1995, retrospective=True)
    # retrospective 1995 is interpolated (M1) or held (M0/M2): never an observed
    # anchor, so even a present actor grant must not open a permission-valid route.
    assert not x.authorized_opportunity
    assert not open_routes(x)


# 3. duplicate ids where BOTH copies are otherwise admissible ------------------
def test_duplicate_id_both_admissible_refuses():
    c = case([wave('DUP', 1990, .2), wave('DUP', 2000, .6)])  # same country/edition
    x = T.evaluate(c, T.METHOD_M0_HOLD, clock_year=2000, retrospective=True)
    assert x.refused_code == T.REFUSED_DUPLICATE_WAVE_ID


# 4. capability honesty under partial/empty SourceGrant claims -----------------
def _grant_read(edition='E1', current=True, owner='ACTUAL_SOURCE', family='ACTUAL_SOURCE'):
    c = case([wave('VALID', 1990, .6)])
    g = T.SourceGrant(grant_source_family=family, grant_edition=edition,
                      grant_current=current, grant_source_owner=owner)
    return T.read_selected_world(WORLD, c, T.METHOD_M0_HOLD, 1995,
                                 source_grant=g, require_source_grant=True)


def test_source_grant_empty_family_refuses():
    x = _grant_read(family='')
    assert x.refused_code is not None


def test_source_grant_empty_edition_refuses():
    x = _grant_read(edition='')
    assert x.refused_code is not None


def test_source_grant_missing_claim_refuses():
    c = case([wave('VALID', 1990, .6)])
    x = T.read_selected_world(WORLD, c, T.METHOD_M0_HOLD, 1995, require_source_grant=True)
    assert x.refused_code == T.REFUSED_SOURCE_GRANT_MISSING


# 5. lag/rupture/missing identity invariant -----------------------------------
def test_lag_rupture_missing_identity_invariant():
    c = case([wave('DELAYED', 1990, .8, published_year=2000),
              wave('MISS', 1995, float('nan'))], ruptures=(1995,))
    x = T.evaluate(c, T.METHOD_M0_HOLD, clock_year=1997, retrospective=True)
    assert set(T.pub_lag_of(x)) <= set(x.basis_wave_ids)
    # missing support is excluded and named, never a basis wave or a lag wave
    assert 'MISS' not in x.basis_wave_ids
    assert 'MISS' not in set(T.pub_lag_of(x))
    assert 'MISS' in set(getattr(x, 'missing_excluded_wave_ids', ()))
