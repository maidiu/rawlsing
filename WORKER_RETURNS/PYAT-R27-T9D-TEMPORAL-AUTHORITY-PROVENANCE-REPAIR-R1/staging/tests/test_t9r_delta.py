"""Phase A frozen delta expectations. Run only against pinned candidate code.

Extended semantics use a separately disclosed direct-call signature binding;
unavailable bindings are explicit failures, never skips or synthetic passes.
"""
from dataclasses import asdict, replace
import importlib.util
import json
from pathlib import Path
import pytest
import t9b_temporal as T

RET=Path(__file__).resolve().parents[1]
METHODS=[T.METHOD_M0_HOLD,T.METHOD_M1_INTERP,T.METHOD_M2_BACKOFF]
EVENTS=[]
C='SYNTH_COUNTRY_A'

def wave(name,year,value,**kw):
    params=dict(wave_id=name,source_family='SYNTH_FAMILY',country=C,instrument='SYNTH_INSTRUMENT',
        edition='E1',cohort='COHORT_ALL',observation_year=year,published_year=year,value=value)
    params.update(kw);return T.Wave(**params)

def case(waves=None,**kw):
    params=dict(case_id='T9R',country=C,waves=tuple(waves if waves is not None else
        [wave('W0',1990,.20),wave('W1',2000,.60)]),target_year=1995)
    params.update(kw);return T.TemporalCase(**params)

WORLD=T.StructuralWorld('W_SYNTH_INSTITUTION',
    ('ROUTE_REDUCED_BURDEN','ROUTE_PARTICIPATION','ROUTE_DEFERRED_REVIEW'),
    ('GRANT_YOUNG_PERSON_ACCESS',),'SYNTH_INSTITUTION')

def record(key,obj):
    EVENTS.append({'id':key,'actual':obj.as_dict() if hasattr(obj,'as_dict') else obj})
    return obj

@pytest.fixture(scope='session',autouse=True)
def save_observations():
    yield
    (RET/'evidence/delta_observations.json').write_text(json.dumps(EVENTS,indent=2,allow_nan=False)+'\n')

def no_authorized_routes(result):
    # The existing opportunity_ids field is the candidate's claimed open set.
    # A separately typed exploratory field is allowed and is not copied here.
    return not [r for r in result.opportunity_ids if r!='ROUTE_BLOCKED_NO_SUPPORT']

@pytest.mark.parametrize('method',METHODS)
@pytest.mark.parametrize('retro',[False,True])
def test_d01_d02_clock_numeric_and_no_observation_upgrade(method,retro):
    x=record(f'D01_D02_{method}_{retro}',T.evaluate(case(),method,retrospective=retro))
    expected=.4 if retro and method==METHODS[1] else .2
    assert x.value==pytest.approx(expected)
    if not retro:assert 'W1' not in x.basis_wave_ids
    if retro and method==METHODS[1]:
        assert 'INTERPOLATED_NOT_OBSERVED' in x.uncertainty
        assert x.temporal_key!=T.AUTHORIZED_SPARSE_TEMPORAL_KEY

@pytest.mark.parametrize('method',METHODS)
@pytest.mark.parametrize('missing',[None,float('nan'),float('inf'),float('-inf')],ids=['None','NaN','positive_infinity','negative_infinity'])
def test_d05_missing_never_becomes_observed_zero_or_one(method,missing):
    try:x=T.evaluate(case([wave('MISSING',1990,missing)]),method)
    except Exception as exc:
        record('D05_EXCEPTION',{'method':method,'input':repr(missing),'exception':type(exc).__name__})
        pytest.fail('Missing/nonfinite support requires typed unknown, not an unhandled exception')
    record('D05_'+method+'_'+repr(missing),x)
    assert x.value is None and x.refused_code is not None

@pytest.mark.parametrize('method',METHODS)
def test_d06_finite_zero_is_not_missing(method):
    x=record('D06_'+method,T.evaluate(case([wave('ZERO',1990,0.)]),method))
    assert x.value==0. and x.refused_code is None

@pytest.mark.parametrize('wrong_first',[True,False])
def test_d07_d08_actual_basis_provenance_is_order_invariant(wrong_first):
    excluded=wave('EXCLUDED',1980,.1,country='OTHER',source_family='WRONG_SOURCE',edition='WRONG_EDITION')
    valid=wave('VALID',1990,.6,source_family='ACTUAL_SOURCE',edition='ACTUAL_EDITION')
    x=record('D07_D08_'+str(wrong_first),T.read_selected_world(WORLD,case([excluded,valid] if wrong_first else [valid,excluded]),METHODS[0],1995))
    assert x.basis_wave_ids==('VALID',)
    assert x.provenance['source_family']=='ACTUAL_SOURCE'
    assert x.provenance['edition']=='ACTUAL_EDITION'

@pytest.mark.parametrize('routes',[('ROUTE_DEFERRED_REVIEW',),WORLD.structural_routes+('MATERIAL_NEW_ROUTE',)])
def test_d09_material_route_membership_changes_world(routes):
    changed=replace(WORLD,structural_routes=routes)
    a=T.read_selected_world(WORLD,case(),METHODS[0],2000)
    b=T.read_selected_world(changed,case(),METHODS[0],2000)
    record('D09',{'before':asdict(WORLD),'after':asdict(changed),'claims_identical':T.structurally_identical(a,b)})
    assert not T.structurally_identical(a,b)

@pytest.mark.parametrize('clock',[1990,1995,1999])
def test_d11_probe_cannot_open_authorized_opportunity(clock):
    x=record('D11_'+str(clock),T.read_selected_world(WORLD,case(),METHODS[1],clock,retrospective=True))
    assert x.temporal_key!=T.AUTHORIZED_SPARSE_TEMPORAL_KEY
    assert no_authorized_routes(x)

@pytest.mark.parametrize('method',[METHODS[0],METHODS[2]])
def test_d12_cross_regime_hold_requires_explicit_qualification(method):
    x=record('D12_'+method,T.evaluate(case(ruptures=(1995,)),method,clock_year=1997,retrospective=True))
    assert x.value is None or 'RUPTURE' in x.uncertainty.upper() or 'RUPTURE' in x.detail.upper()
    if x.value is not None:assert x.temporal_key!=T.AUTHORIZED_SPARSE_TEMPORAL_KEY

@pytest.mark.parametrize('method',[METHODS[0],METHODS[2]])
def test_d13_product_lag_does_not_name_unused_future_wave(method):
    x=record('D13_'+method,T.evaluate(case(),method,retrospective=True))
    assert x.value==pytest.approx(.2) and x.basis_wave_ids==('W0',)
    assert set(T.pub_lag_of(x))<=set(x.basis_wave_ids)

@pytest.mark.parametrize('flag',['revoked','archived_nonrenewed'])
@pytest.mark.parametrize('retro',[False,True])
def test_d15_rights_withdrawn_after_acquisition_refuse_both_modes(flag,retro):
    granted=wave('SOURCE',1990,.8)
    denied=replace(granted,**{flag:True})
    before=T.evaluate(case([granted]),METHODS[0],retrospective=retro)
    after=T.evaluate(case([denied]),METHODS[0],retrospective=retro)
    record('D15_'+flag+'_'+str(retro),{'before':before.as_dict(),'after':after.as_dict()})
    assert before.value==.8
    assert after.value is None and after.refused_code is not None

@pytest.mark.parametrize('method',METHODS)
def test_d18_contradictory_future_observation_not_admissible(method):
    c=case([wave('FUTURE_OBSERVATION',2000,.9,published_year=1990)])
    x=record('D18_'+method,T.evaluate(c,method))
    assert x.value is None and x.refused_code is not None

@pytest.mark.parametrize('method',METHODS)
def test_d21_flat_series_no_trend_or_calibration_claim(method):
    c=case([wave('F0',1990,.5),wave('F1',2000,.5)])
    x=record('D21_'+method,T.evaluate(c,method,retrospective=True))
    assert x.value==.5
    consumer=T.read_selected_world(WORLD,c,method,1995,retrospective=True)
    assert consumer.provenance['observed_temporal_calibration'] is False

def test_d22_two_times_retain_numbers_under_complete_constant_world():
    original=asdict(WORLD)
    values=[T.evaluate(case(),METHODS[1],clock_year=y,retrospective=True).value for y in [1990,2000]]
    reads=[T.read_selected_world(WORLD,case(),METHODS[1],y,retrospective=True) for y in [1990,2000]]
    record('D22',{'values':values,'complete_world':original,'reads':[x.as_dict() for x in reads]})
    assert values==[.2,.6] and asdict(WORLD)==original
    assert T.structurally_identical(*reads)

@pytest.mark.parametrize('vector_id',['D04','D10','D16','D17','D17_WRONG_OWNER','D19'])
def test_coupled_semantic_obligations_require_actual_candidate_support(vector_id):
    path=RET/'phase_b_direct_bindings.py'
    if not path.is_file():
        record(vector_id,{'status':'CAPABILITY_BINDING_UNAVAILABLE','not_a_pass':True})
        pytest.fail('CAPABILITY_BINDING_UNAVAILABLE: no pinned direct candidate API call for '+vector_id)
    spec=importlib.util.spec_from_file_location('t9r_direct_bindings',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    # A binding must perform an actual direct candidate call, return its raw
    # object plus path/argument trace, and cannot synthesize a permission result.
    result,trace=module.call_vector(vector_id,T)
    record(vector_id,{'trace':trace,'actual':result.as_dict() if hasattr(result,'as_dict') else result})
    assert trace['actual_candidate_call'] is True and trace['output_rewritten'] is False
    if vector_id=='D04':
        assert result.value is None or 'FUTURE_PUBLICATION' not in result.basis_wave_ids
    elif vector_id in ['D10','D16','D17','D17_WRONG_OWNER']:
        assert no_authorized_routes(result)
        assert result.refused_code is not None or result.temporal_key!=T.AUTHORIZED_SPARSE_TEMPORAL_KEY
    else:
        payload=result.as_dict() if hasattr(result,'as_dict') else result
        assert not payload.get('actor_memory') and not payload.get('remembered_exposure')
        assert not payload.get('actor_knowledge') and not payload.get('actor_id')

def test_d14_native_current_authority_cannot_be_recreated_by_two_old_anchors():
    import pandas as pd
    group=pd.DataFrame([{'wave_id':str(y),'probe_ready_input_count':1,
       'structural_dimension_status':'resolved','comparable_key_grain':'structural_channel_exact',
       'source_v552_structural_fact_lane':'temporal_fact','canonical_semantic_signature':'known',
       'source_v552j_packet_ids_json':json.dumps([f'packet-{y}']),'structural_pressure_value':v}
       for y,v in [(1990,.2),(2000,.6)]])
    report={'ready_for_v553':False,'comparison_authority_status':'withdrawn',
       'shared_semantic_columns':['s'],'shared_directionality_columns':['d'],'shared_position_columns':['p']}
    x=record('D14_CURRENT_AUTHORITY_WITHDRAWN',T.V553._authorize_v553_multi_wave_key(report,group))
    assert x['multi_wave_authorization_status']==T.BLOCKED_TEMPORAL_KEY
    assert x['ready_for_v554'] is False
