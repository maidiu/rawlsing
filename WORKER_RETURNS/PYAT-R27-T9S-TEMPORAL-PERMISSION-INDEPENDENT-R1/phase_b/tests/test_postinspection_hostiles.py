"""Additional post-inspection falsifiers, separate from the frozen delta50.

These expectations must not be represented as preimplementation preregistration.
"""
from dataclasses import replace
import json
from pathlib import Path
import pytest
import t9b_temporal as T

EVENTS = []
METHODS = [T.METHOD_M0_HOLD, T.METHOD_M1_INTERP, T.METHOD_M2_BACKOFF]

@pytest.fixture(scope='session', autouse=True)
def save():
    yield
    (Path(__file__).parents[1]/'evidence/postinspection_observations.json').write_text(json.dumps(EVENTS, indent=2)+'\n')

def wave(name, year, value, **kw):
    fields = dict(wave_id=name, source_family='ACTUAL_SOURCE',country='SYNTH_COUNTRY_A',
                  instrument='SYNTH_INSTRUMENT',edition='E1',cohort='COHORT_ALL',
                  observation_year=year,published_year=year,value=value)
    fields.update(kw)
    return T.Wave(**fields)

def case(waves, **kw):
    return T.TemporalCase(case_id='POST_INSPECTION',country='SYNTH_COUNTRY_A',
                          waves=tuple(waves),target_year=1995,**kw)

WORLD = T.StructuralWorld('SAME_WORLD',('ROUTE_PARTICIPATION','ROUTE_DEFERRED_REVIEW'),(), 'INSTITUTION')

@pytest.mark.parametrize('method', METHODS)
def test_two_synthetic_anchors_and_no_actor_grants_cannot_authorize(method):
    c = case([wave('OLD',1980,.2),wave('RECENT',1990,.6)])
    x = T.read_selected_world(WORLD,c,method,1995)
    EVENTS.append(dict(id='TWO_ANCHORS_EMPTY_GRANTS',method=method,actual=x.as_dict(),world=WORLD.__dict__))
    assert not x.authorized_opportunity
    assert not [r for r in x.opportunity_ids if r != 'ROUTE_BLOCKED_NO_SUPPORT']

@pytest.mark.parametrize('method', [T.METHOD_M0_HOLD, T.METHOD_M2_BACKOFF])
def test_unused_future_archive_wave_cannot_upgrade_same_held_product_authority(method):
    old = wave('W0',1990,.2)
    future = wave('W1',2000,.6)
    world = replace(WORLD,access_grants=('GRANT_YOUNG_PERSON_ACCESS',))
    before = T.read_selected_world(world,case([old]),method,1995,retrospective=True)
    after = T.read_selected_world(world,case([old,future]),method,1995,retrospective=True)
    EVENTS.append(dict(id='UNUSED_FUTURE_AUTHORITY_UPGRADE',method=method,
                       before=before.as_dict(),after=after.as_dict(),
                       numeric_before=T.evaluate(case([old]),method,retrospective=True).value,
                       numeric_after=T.evaluate(case([old,future]),method,retrospective=True).value))
    assert after.basis_wave_ids == before.basis_wave_ids == ('W0',)
    assert not after.authorized_opportunity
    assert not [r for r in after.opportunity_ids if r != 'ROUTE_BLOCKED_NO_SUPPORT']

def test_lag_parser_does_not_swallow_rupture_qualifiers_as_wave_identity():
    c = case([wave('DELAYED',1990,.8,published_year=2000)],ruptures=(1995,))
    x = T.evaluate(c,T.METHOD_M0_HOLD,clock_year=1997,retrospective=True)
    EVENTS.append(dict(id='LAG_PLUS_RUPTURE',actual=x.as_dict(),parsed=list(T.pub_lag_of(x))))
    assert set(T.pub_lag_of(x)) <= set(x.basis_wave_ids)

def test_duplicate_wave_id_cannot_rebind_provenance_to_excluded_source():
    c = case([wave('DUPLICATE',1990,.6),
              wave('DUPLICATE',1980,.1,country='OTHER',source_family='WRONG_SOURCE',edition='WRONG_EDITION')])
    x = T.read_selected_world(WORLD,c,T.METHOD_M0_HOLD,1995)
    EVENTS.append(dict(id='DUPLICATE_EXCLUDED_BASIS',actual=x.as_dict()))
    assert x.refused_code is not None or (x.provenance['source_family']=='ACTUAL_SOURCE' and x.provenance['edition']=='E1')
