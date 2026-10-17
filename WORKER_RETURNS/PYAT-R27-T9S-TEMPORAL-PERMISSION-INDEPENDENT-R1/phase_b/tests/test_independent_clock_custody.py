"""Independent frozen-oracle court; intentional red assertions remain failures."""
from dataclasses import asdict, fields, replace
from fractions import Fraction
import hashlib
import inspect
import json
import math
from pathlib import Path
import sys

import pytest
import t9b_temporal as T

RET=Path(__file__).resolve().parents[1]
EVENTS=[]
C='SYNTH_COUNTRY_A'
METHODS=[T.METHOD_M0_HOLD,T.METHOD_M1_INTERP,T.METHOD_M2_BACKOFF]

def wave(name,year,value,**kw):
    args=dict(wave_id=name,source_family='SYNTH_FAMILY',country=C,instrument='SYNTH_INSTRUMENT',
              edition='E1',cohort='COHORT_ALL',observation_year=year,published_year=year,value=value)
    args.update(kw)
    return T.Wave(**args)

def case(waves=None,**kw):
    args=dict(case_id='T9I',country=C,waves=tuple(waves if waves is not None else
        [wave('W0',1990,.20),wave('W1',2000,.60)]),target_year=1995)
    args.update(kw)
    return T.TemporalCase(**args)

WORLD=T.StructuralWorld('W_SYNTH_INSTITUTION',
    ('ROUTE_REDUCED_BURDEN','ROUTE_PARTICIPATION','ROUTE_DEFERRED_REVIEW'),
    ('GRANT_YOUNG_PERSON_ACCESS',),'SYNTH_INSTITUTION')

def observe(name,value):
    if hasattr(value,'as_dict'): value=value.as_dict()
    EVENTS.append({'id':name,'actual':value})
    return value

@pytest.fixture(scope='session',autouse=True)
def save_events():
    yield
    (RET/'evidence/independent_observations.json').write_text(json.dumps(EVENTS,indent=2,allow_nan=False)+'\n')

@pytest.mark.parametrize('method',METHODS)
def test_asof_excludes_2000_publication(method):
    x=T.evaluate(case(),method,retrospective=False);observe('C1_'+method,x)
    assert x.value==pytest.approx(.2)
    assert x.basis_wave_ids==('W0',)

@pytest.mark.parametrize('method,expected',[(METHODS[0],.2),(METHODS[1],.4),(METHODS[2],.2)])
def test_retrospective_method_comparison(method,expected):
    x=T.evaluate(case(),method,retrospective=True);observe('C2_'+method,x)
    assert x.value==pytest.approx(expected)
    if method==METHODS[1]:
        assert 'INTERPOLATED_NOT_OBSERVED' in x.uncertainty
        assert x.temporal_key==T.PROBE_ONLY_TEMPORAL_KEY

@pytest.mark.parametrize('method',METHODS)
def test_postclock_publication_excluded_asof_and_flagged_archival(method):
    c=case([wave('DELAYED',1990,.8,published_year=2000)])
    a=T.evaluate(c,method,retrospective=False);b=T.evaluate(c,method,retrospective=True)
    observe('E1_'+method,{'asof':a.as_dict(),'archival':b.as_dict()})
    assert a.value is None and a.refused_code=='NO_TEMPORAL_SUPPORT'
    assert b.value==.8 and 'PUBLICATION_LAG:DELAYED' in b.uncertainty

@pytest.mark.parametrize('method',METHODS)
@pytest.mark.parametrize('retro',[False,True])
@pytest.mark.parametrize('flag',['revoked','archived_nonrenewed'])
def test_current_revocation_and_nonrenewal_not_resurrected(method,retro,flag):
    c=case([wave('DENIED',1990,.8,**{flag:True})])
    x=T.evaluate(c,method,retrospective=retro);observe(f'E2_E3_{method}_{retro}_{flag}',x)
    assert x.value is None and x.temporal_key==T.BLOCKED_TEMPORAL_KEY

@pytest.mark.parametrize('method',METHODS)
def test_empty_is_unknown_and_observed_zero_is_zero(method):
    empty=T.evaluate(case([]),method);zero=T.evaluate(case([wave('ZERO',1990,0.)]),method)
    observe('C3_'+method,{'empty':empty.as_dict(),'zero':zero.as_dict()})
    assert empty.value is None and empty.refused_code=='NO_TEMPORAL_SUPPORT'
    assert zero.value==0. and zero.refused_code is None

@pytest.mark.parametrize('dimension',['country','instrument','cohort'])
def test_mismatched_population_is_not_support(dimension):
    x=T.evaluate(case([wave('WRONG',1990,.8,**{dimension:'OTHER'})]),METHODS[1],retrospective=True)
    observe('C5_'+dimension,x)
    assert x.value is None and x.refused_code=='NO_TEMPORAL_SUPPORT'

def test_explicit_incompatible_geography_refuses():
    c=case([wave('A',1990,.2),wave('B',2000,.6,country='OTHER')],harmonize_countries=True)
    x=T.evaluate(c,METHODS[1],retrospective=True);observe('C5_explicit',x)
    assert x.refused_code=='NON_HARMONIZABLE_GEOMETRY'

def test_registered_rupture_refuses_interpolation():
    x=T.evaluate(case(ruptures=(1995,)),METHODS[1],retrospective=True);observe('C4',x)
    assert x.value is None and x.refused_code=='RUPTURE_BRACKET_REFUSED'

def test_flat_null_trend_does_not_move():
    c=case([wave('F0',1990,.5),wave('F1',2000,.5)])
    values=[T.evaluate(c,m,retrospective=True).value for m in METHODS]
    observe('TC_NULL_STABILITY',values)
    assert values==[.5,.5,.5]

def test_independent_estimand_and_error_bounds():
    slope=(Fraction(3,5)-Fraction(1,5))/10
    midpoint=Fraction(1,5)+5*slope
    unconditioned=max(midpoint,1-midpoint)
    monotone=max(midpoint-Fraction(1,5),Fraction(3,5)-midpoint)
    observe('INDEPENDENT_UNCERTAINTY',{'slope_per_year':str(slope),'midpoint':str(midpoint),
       'unconditioned_identification_set':[0,1],'max_absolute_error':str(unconditioned),
       'monotonicity_assumed_set':['1/5','3/5'],'monotonicity_max_error':str(monotone),
       'sampling_error':'UNIDENTIFIED; no sample design or variance supplied'})
    assert slope==Fraction(1,25) and midpoint==Fraction(2,5)
    assert unconditioned==Fraction(3,5) and monotone==Fraction(1,5)

def test_two_time_original_consumer_and_numerical_products_reproduced():
    stored=json.loads((RET/'pinned_candidate/evidence/02_real_temporal_to_selected_world_two_times.json').read_text())
    actual={str(y):T.read_selected_world(WORLD,case(),METHODS[1],y,retrospective=True).as_dict() for y in [1990,2000]}
    values={str(y):T.evaluate(case(),METHODS[1],clock_year=y,retrospective=True).value for y in [1990,2000]}
    observe('E6_TWO_TIME',{'reads':actual,'numerical_values':values,'structural_world':asdict(WORLD),
       'structural_preimage_sha256':hashlib.sha256(json.dumps(asdict(WORLD),sort_keys=True).encode()).hexdigest()})
    assert actual==stored['two_time_reads']
    assert values=={'1990':.2,'2000':.6}
    assert actual['1990']['opportunity_ids']==['ROUTE_DEFERRED_REVIEW']
    assert actual['2000']['opportunity_ids']==['ROUTE_PARTICIPATION','ROUTE_DEFERRED_REVIEW']

def test_probe_only_estimate_cannot_be_authorized_open_opportunity():
    x=T.read_selected_world(WORLD,case(),METHODS[1],1995,retrospective=True);observe('RED_PROBE_OPENS_ROUTE',x)
    assert x.temporal_key==T.PROBE_ONLY_TEMPORAL_KEY
    assert not [r for r in x.opportunity_ids if r!='ROUTE_BLOCKED_NO_SUPPORT'], 'probe-only estimate opened a claimed lawful route'

def test_structural_route_mutation_is_detected():
    changed=replace(WORLD,structural_routes=('ROUTE_DEFERRED_REVIEW',))
    a=T.read_selected_world(WORLD,case(),METHODS[0],2000)
    b=T.read_selected_world(changed,case(),METHODS[0],2000)
    observe('RED_STRUCTURAL_EQUALITY',{'world_a':asdict(WORLD),'world_b':asdict(changed),
        'read_a':a.as_dict(),'read_b':b.as_dict(),'claims_identical':T.structurally_identical(a,b)})
    assert not T.structurally_identical(a,b), 'different structural route sets falsely certified identical'

def test_consumer_provenance_names_actual_basis_not_excluded_first_wave():
    wrong=wave('EXCLUDED',1980,.1,country='OTHER',source_family='WRONG_SOURCE',edition='WRONG_EDITION')
    valid=wave('VALID',1990,.6,source_family='ACTUAL_SOURCE',edition='ACTUAL_EDITION')
    x=T.read_selected_world(WORLD,case([wrong,valid]),METHODS[0],1995);observe('RED_BASIS_PROVENANCE',x)
    assert x.basis_wave_ids==('VALID',)
    assert x.provenance['source_family']=='ACTUAL_SOURCE'
    assert x.provenance['edition']=='ACTUAL_EDITION'

@pytest.mark.parametrize('method',[METHODS[0],METHODS[2]])
def test_postrupture_carry_is_unknown_or_explicitly_rupture_qualified(method):
    x=T.evaluate(case(ruptures=(1995,)),method,clock_year=1997,retrospective=True)
    observe('RED_POSTRUPTURE_'+method,x)
    assert x.value is None or 'RUPTURE' in x.uncertainty or 'RUPTURE' in x.detail.upper(), 'pre-break population carried past declared rupture without a rupture caveat'

@pytest.mark.parametrize('method',METHODS)
def test_missing_numeric_observation_stays_typed_unknown(method):
    c=case([wave('MISSING',1990,float('nan'))])
    try:
        x=T.evaluate(c,method)
    except Exception as exc:
        observe('RED_NULL_'+method,{'exception':type(exc).__name__,'message':str(exc)})
        pytest.fail('missing observation raised instead of returning a typed unknown')
    observe('RED_NULL_'+method,x)
    assert x.value is None and x.refused_code is not None, 'NaN observation converted into authorized observed zero'

def test_nonbasis_future_wave_does_not_claim_to_be_product_publication_basis():
    x=T.evaluate(case(),METHODS[0],retrospective=True);observe('RED_NONBASIS_PUBLICATION_LAG',x)
    assert set(T.pub_lag_of(x))<=set(x.basis_wave_ids), 'publication provenance falsely names a wave not used by this method'

def test_schema_capability_limits_are_recorded_not_inferred_as_person_memory():
    names=[f.name for f in fields(T.Wave)]
    sig=str(inspect.signature(T.evaluate))
    x=T.read_selected_world(WORLD,case(),METHODS[0],1995)
    observe('CLOCK_RIGHTS_ACTOR_CAPABILITY_LIMIT',{'wave_fields':names,'evaluate_signature':sig,
       'independent_known_at_bound':False,'effective_and_discovered_revocation_timestamps':False,
       'historical_entitlement_vs_current_use_grant':False,'actor_exposure_or_remembered_exposure_evidence':False,
       'consumer_provenance':x.provenance})
    assert 'revoked' in names and 'archived_nonrenewed' in names
    assert not any('memory' in k or 'remembered' in k for k in x.provenance)

def test_independent_guard_rejects_untrusted_path_and_changed_preimage(tmp_path):
    runner=sys.modules['__main__']
    rogue=tmp_path/'rogue.py';rogue.write_text('x=1\n')
    with pytest.raises(ImportError,match='UNPINNED_PROJECT_MODULE'):
        runner.verify('data.rogue',rogue)
    # No sealed source is mutated: place a counterfeit only in scratch and a
    # deliberately inconsistent local expected-map record for this guard test.
    runner.EXPECTED[rogue.resolve()]={'sha256':'0'*64,'git_blob_sha1':'0'*40}
    try:
        with pytest.raises(ImportError,match='PREIMAGE_MISMATCH'):
            runner.verify('data.rogue',rogue)
    finally:
        del runner.EXPECTED[rogue.resolve()]
    observe('GUARD_NEGATIVE_CONTROL',{'untrusted_path':'rejected','changed_preimage':'rejected','sealed_source_mutated':False})

def native_group(count=2):
    import pandas as pd
    return pd.DataFrame([{'wave_id':f'N{i}','structural_dimension_status':'resolved',
       'probe_ready_input_count':1,'source_v552j_packet_ids_json':json.dumps([f'packet-{i}']),
       'structural_pressure_value':.2+.4*i,'comparable_key_grain':'structural_channel_exact',
       'source_v552_structural_fact_lane':'temporal_fact','canonical_semantic_signature':'known-signature'}
       for i in range(count)])

def native_report():
    return {'ready_for_v553':True,'comparison_authority_status':'multi_wave_authorized',
       'shared_semantic_columns':['sem'],'shared_directionality_columns':['dir'],
       'shared_position_columns':['pos']}

@pytest.mark.parametrize('count,expected,ready',[
    (2,T.AUTHORIZED_SPARSE_TEMPORAL_KEY,True),(1,T.PROBE_ONLY_TEMPORAL_KEY,False)])
def test_actual_native_authorization_positive_and_probe_controls(count,expected,ready):
    x=T.V553._authorize_v553_multi_wave_key(native_report(),native_group(count))
    observe('NATIVE_AUTHORIZATION_'+str(count),x)
    assert x['multi_wave_authorization_status']==expected and x['ready_for_v554']==ready

def test_actual_native_authorization_blocked_control():
    import pandas as pd
    x=T.V553._authorize_v553_multi_wave_key({},pd.DataFrame())
    observe('NATIVE_AUTHORIZATION_BLOCKED',x)
    assert x['multi_wave_authorization_status']==T.BLOCKED_TEMPORAL_KEY
    assert x['ready_for_v554'] is False

def test_actual_native_gap_preserves_unknown_even_when_flag_enabled():
    import pandas as pd
    obs=pd.DataFrame([{'temporal_pressure_key':'native-key','country':'US','survey_year':y,
        'wave_id':str(y),'multi_wave_authorization_status':T.AUTHORIZED_SPARSE_TEMPORAL_KEY,
        'temporal_status':'observed_authorized_anchor'} for y in [1990,2000]])
    x=T.V553._build_v553_interpolation_segment_index({},obs,'t9i-control',allow_interpolation=True)
    row=x.iloc[0].to_dict();row['interpolation_allowed']=bool(row['interpolation_allowed'])
    row['anchor_count']=int(row['anchor_count']);row['gap_length_years']=int(row['gap_length_years'])
    row['segment_start_year']=int(row['segment_start_year']);row['segment_end_year']=int(row['segment_end_year'])
    observe('NATIVE_GAP_CONTROL',row)
    assert row['interpolation_status']=='unknown_gap_preserved'
    assert row['interpolation_allowed'] is False

def test_adapted_single_anchor_does_not_claim_inherited_native_grant():
    native=T.V553._authorize_v553_multi_wave_key(native_report(),native_group(1))
    adapted=T.evaluate(case([wave('ONE',1990,.2)]),METHODS[0])
    observe('RED_NATIVE_VS_ADAPTED_AUTHORITY',{'native':native,'adapted':adapted.as_dict(),
        'limit':'Different APIs; this challenges the claim of inherited authorization semantics, not arithmetic equivalence.'})
    assert native['multi_wave_authorization_status']==T.PROBE_ONLY_TEMPORAL_KEY
    assert adapted.temporal_key!=T.AUTHORIZED_SPARSE_TEMPORAL_KEY, 'adapter authorizes a single synthetic wave without native grant inputs'
