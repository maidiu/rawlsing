"""Isolated TEST_ONLY N9C reader court; no actual OC05, source or EE13 run."""
from __future__ import annotations
from copy import deepcopy
import json
from pathlib import Path
import sys
import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from rawlsing_next.pre553_hq297_n9c_two_field_reader import (
    TestOnlyRegistry,TestOnlyReadError,GSS,NCA,read_historical_test_only,fixture_invalidation,
)
FIX=ROOT/'WORKER_RETURNS/PYAT-R3-HQ297-N9-TWO-FIELD-VALUES-READER-R1/02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json'

@pytest.fixture
def packet():
    return json.loads(FIX.read_text())

def req(rows, as_of='2022-07-08', partial=False, **kw):
    registry=TestOnlyRegistry(rows)
    refs=registry.refs_by_role()
    relation={'kind':'TEST_ONLY_NONPOOLED_COPRESENCE','fixture_only':True,
              'issued_EE13':False,'ordered_refs':[refs[GSS],refs[NCA]],'population_join':False}
    result=read_historical_test_only(registry,selected_refs=refs,relation=relation,
          as_of=as_of,clock_mode='HISTORICAL_PUBLICATION_AWARE',partial_allowed=partial,**kw)
    return result,registry,refs,relation

def assert_code(code,fn):
    with pytest.raises(TestOnlyReadError) as exc:fn()
    assert exc.value.code==code

def test_two_values_really_dereferenced(packet):
    out,_,refs,_=req(packet['fields']);a,b=out['values_read']
    assert out['state']=='TWO_VALUES_READ_TEST_ONLY'
    assert [x['fixture_ref'] for x in out['values_read']]==[refs[GSS],refs[NCA]]
    assert a['values']['numerator']==2388192 and a['values']['denominator']==3288063
    assert a['values']['published_percent']==72.6
    assert b['values']['active_subscriptions']==23414527
    assert a['native_unit']!=b['native_unit'] and a['source_family']!=b['source_family']
    assert out['dependency_readset']==[refs[GSS],refs[NCA]]
    assert out['operative_OC05'] is False and out['issued_EE13'] is False

def test_cold_replay_deterministic(packet):
    a,_,_,_=req(packet['fields']);b,_,_,_=req(deepcopy(packet['fields']))
    assert a==b

def test_2021_observed_not_published(packet):
    result,_,_,_=req(packet['fields'],as_of='2021-12-31')
    assert result['state']=='REFUSED_REQUIRED_FIELD_TEST_ONLY'
    assert len(result['refusals'])==2 and result['values_read']==[]

def test_gss_only_published_in_march_2022(packet):
    result,_,_,_=req(packet['fields'],as_of='2022-03-01',partial=True)
    assert result['state']=='PARTIAL_TEST_ONLY_NOT_POSITIVE'
    assert [x['role'] for x in result['values_read']]==[GSS]
    assert result['refusals'][0]['reason']=='NOT_PUBLISHED_AT_SELECTED_ASOF'

def test_partial_not_positive_without_explicit_permission(packet):
    result,_,_,_=req(packet['fields'],as_of='2022-03-01')
    assert result['values_read']==[] and result['state']=='REFUSED_REQUIRED_FIELD_TEST_ONLY'

def test_2022_both_published(packet):
    result,_,_,_=req(packet['fields'],as_of='2022-07-07')
    assert result['state']=='REFUSED_REQUIRED_FIELD_TEST_ONLY'
    assert any(x['role']==NCA for x in result['refusals'])

def test_historical_2023_valid_with_two_publications(packet):
    result,_,_,_=req(packet['fields'],as_of='2023-01-01')
    assert result['state']=='TWO_VALUES_READ_TEST_ONLY' and result['world_clock']=='HISTORICAL_PUBLICATION_AWARE'

def test_gss_value_change_invalidates_snapshot_not_nca(packet):
    a,_,_,_=req(packet['fields'])
    mutated=deepcopy(packet['fields']);mutated[0]['values']['numerator']-=1
    mutated[0]['values']['electricity_subtypes']['mains']-=1
    b,_,_,_=req(mutated)
    diff=fixture_invalidation(a,b)
    assert diff['changed_roles']==[GSS] and diff['unaffected_roles']==[NCA]
    assert a['values_read'][1]==b['values_read'][1] and a['test_snapshot_ref']!=b['test_snapshot_ref']

def test_nca_change_invalidates_snapshot_not_gss(packet):
    a,_,_,_=req(packet['fields'])
    mutated=deepcopy(packet['fields']);mutated[1]['values']['active_subscriptions']+=1
    mutated[1]['values']['prepaid']+=1
    b,_,_,_=req(mutated)
    diff=fixture_invalidation(a,b)
    assert diff['changed_roles']==[NCA] and diff['unaffected_roles']==[GSS]
    assert a['values_read'][0]==b['values_read'][0]

def test_unchanged_replay_no_invalidation(packet):
    a,_,_,_=req(packet['fields']);b,_,_,_=req(packet['fields'])
    d=fixture_invalidation(a,b)
    assert not d['invalidate_previous_snapshot'] and not d['changed_roles']

def test_exact_old_ref_after_revision_refused(packet):
    original,_,refs,rel=req(packet['fields'])
    changed=deepcopy(packet['fields']);changed[1]['values']['active_subscriptions']+=1;changed[1]['values']['prepaid']+=1
    newreg=TestOnlyRegistry(changed)
    result=read_historical_test_only(newreg,selected_refs=refs,relation=rel,as_of='2022-07-08',clock_mode='HISTORICAL_PUBLICATION_AWARE')
    assert result['state']=='REFUSED_REQUIRED_FIELD_TEST_ONLY'
    assert result['refusals'][0]['reason']=='UNKNOWN_EXACT_FIELD_REF'

def test_revoked_field_fail_closed(packet):
    altered=deepcopy(packet['fields']);altered[1]['status']='REVOKED_TEST_ONLY'
    out,_,_,_=req(altered)
    assert out['state']=='REFUSED_REQUIRED_FIELD_TEST_ONLY'
    assert out['refusals'][0]['reason']=='SOURCE_REVOKED'

def test_revoked_partial_explicit_only(packet):
    altered=deepcopy(packet['fields']);altered[1]['status']='REVOKED_TEST_ONLY'
    out,_,_,_=req(altered,partial=True)
    assert out['state']=='PARTIAL_TEST_ONLY_NOT_POSITIVE'
    assert [x['role'] for x in out['values_read']]==[GSS]

@pytest.mark.parametrize('mode',["CURRENT","ASOF_UNSPECIFIED","OPERATIVE_OC05"])
def test_current_and_operative_clocks_refused(packet,mode):
    r=TestOnlyRegistry(packet['fields']);refs=r.refs_by_role()
    rel={'kind':'TEST_ONLY_NONPOOLED_COPRESENCE','fixture_only':True,'issued_EE13':False,
         'ordered_refs':[refs[GSS],refs[NCA]],'population_join':False}
    assert_code('CURRENT_OR_OTHER_CLOCK_NOT_AUTHORIZED',lambda:read_historical_test_only(
         r,selected_refs=refs,relation=rel,as_of='2022-07-08',clock_mode=mode))

@pytest.mark.parametrize('flag',["requested_person_exposure","requested_pooling","requested_model_use"])
def test_ecological_or_model_inference_refused(packet,flag):
    assert_code('PERSON_POOLING_OR_MODEL_PROMOTION_FORBIDDEN',lambda:req(packet['fields'],**{flag:True}))

@pytest.mark.parametrize('idx,key,value,expected',[
 (0,'native_unit','INDIVIDUAL_PERSON_ACCESS','GSS_NATIVE_UNIT_GEOGRAPHY_MEASURE_CONFLICT'),
 (0,'native_geography','GHANA_NATIONAL','GSS_NATIVE_UNIT_GEOGRAPHY_MEASURE_CONFLICT'),
 (0,'native_measure','MAINS_ELECTRICITY_ONLY','GSS_NATIVE_UNIT_GEOGRAPHY_MEASURE_CONFLICT'),
 (1,'native_unit','UNIQUE_MOBILE_USERS','NCA_NATIVE_UNIT_GEOGRAPHY_MEASURE_CONFLICT'),
 (1,'native_geography','GHANA_RURAL','NCA_NATIVE_UNIT_GEOGRAPHY_MEASURE_CONFLICT'),
 (1,'unique_persons',True,'NCA_RURAL_OR_UNIQUE_PERSON_INFERENCE'),
 (1,'rural_split',100,'NCA_RURAL_OR_UNIQUE_PERSON_INFERENCE'),
 (0,'issuer_ref','FAKE_ISSUED','EXTERNAL_CUSTODY_OR_ISSUER_FORGERY'),
 (0,'source_pdf_sha256','FAKE_SHA','EXTERNAL_CUSTODY_OR_ISSUER_FORGERY'),
 (1,'permission','AUTHORIZED_REAL_WORLD','REAL_USE_PERMISSION_NOT_ISSUED'),
 (1,'issued',True,'FIELD_ISSUANCE_LAUNDERING'),
 (1,'status','UNKNOWN','UNKNOWN_SOURCE_STATE')])
def test_mutant_field_metadata_rejected(packet,idx,key,value,expected):
    mutated=deepcopy(packet['fields']);mutated[idx][key]=value
    assert_code(expected,lambda:TestOnlyRegistry(mutated))

def test_false_gss_numerator_denominator(packet):
    altered=deepcopy(packet['fields']);altered[0]['values']['numerator']=1
    assert_code('GSS_VALUE_DENOMINATOR_OR_SUBTYPE_INTEGRITY',lambda:TestOnlyRegistry(altered))

def test_false_nca_subscriptions_split(packet):
    altered=deepcopy(packet['fields']);altered[1]['values']['postpaid']=1
    assert_code('NCA_VALUE_SPLIT_INTEGRITY',lambda:TestOnlyRegistry(altered))

def test_false_gss_missing_exclusions(packet):
    altered=deepcopy(packet['fields']);altered[0]['exclusions']=[]
    assert_code('GSS_EXCLUSION_DROPPED',lambda:TestOnlyRegistry(altered))

def test_mislabeled_publisher_families(packet):
    altered=deepcopy(packet['fields']);altered[1]['family']=altered[0]['family']
    assert_code('NCA_NATIVE_UNIT_GEOGRAPHY_MEASURE_CONFLICT',lambda:TestOnlyRegistry(altered))

def test_registry_not_supplied_as_trusted_object(packet):
    assert_code('INDEPENDENT_REGISTRY_REQUIRED',lambda:read_historical_test_only(
       {},selected_refs={GSS:'X',NCA:'Y'},relation={},as_of='2022-07-08',clock_mode='HISTORICAL_PUBLICATION_AWARE'))

def test_relation_self_issued_rejected(packet):
    r=TestOnlyRegistry(packet['fields']);refs=r.refs_by_role()
    rel={'kind':'TEST_ONLY_NONPOOLED_COPRESENCE','fixture_only':True,'issued_EE13':True,
         'ordered_refs':[refs[GSS],refs[NCA]],'population_join':False}
    assert_code('INDEPENDENT_EE13_NOT_ISSUED_OR_RELATION_CHANGED',lambda:read_historical_test_only(
        r,selected_refs=refs,relation=rel,as_of='2022-07-08',clock_mode='HISTORICAL_PUBLICATION_AWARE'))

def test_relation_misordered_rejected(packet):
    r=TestOnlyRegistry(packet['fields']);refs=r.refs_by_role()
    rel={'kind':'TEST_ONLY_NONPOOLED_COPRESENCE','fixture_only':True,'issued_EE13':False,
         'ordered_refs':[refs[NCA],refs[GSS]],'population_join':False}
    assert_code('INDEPENDENT_EE13_NOT_ISSUED_OR_RELATION_CHANGED',lambda:read_historical_test_only(
        r,selected_refs=refs,relation=rel,as_of='2022-07-08',clock_mode='HISTORICAL_PUBLICATION_AWARE'))

def test_role_swap_is_rejected_even_valid_ref(packet):
    r=TestOnlyRegistry(packet['fields']);refs=r.refs_by_role()
    selected={GSS:refs[NCA],NCA:refs[GSS]}
    rel={'kind':'TEST_ONLY_NONPOOLED_COPRESENCE','fixture_only':True,'issued_EE13':False,
         'ordered_refs':[selected[GSS],selected[NCA]],'population_join':False}
    out=read_historical_test_only(r,selected_refs=selected,relation=rel,as_of='2022-07-08',clock_mode='HISTORICAL_PUBLICATION_AWARE')
    assert out['state']=='REFUSED_REQUIRED_FIELD_TEST_ONLY'
    assert len(out['refusals'])==2

def test_duplicate_field_ref_is_rejected(packet):
    r=TestOnlyRegistry(packet['fields']);refs=r.refs_by_role()
    rel={'kind':'TEST_ONLY_NONPOOLED_COPRESENCE','fixture_only':True,'issued_EE13':False,
         'ordered_refs':[refs[GSS],refs[GSS]],'population_join':False}
    assert_code('TWO_DISTINCT_ROLE_REFS_REQUIRED',lambda:read_historical_test_only(
        r,selected_refs={GSS:refs[GSS],NCA:refs[GSS]},relation=rel,
        as_of='2022-07-08',clock_mode='HISTORICAL_PUBLICATION_AWARE'))

def test_no_caller_supplied_values_interface(packet):
    r=TestOnlyRegistry(packet['fields']);refs=r.refs_by_role()
    rel={'kind':'TEST_ONLY_NONPOOLED_COPRESENCE','fixture_only':True,'issued_EE13':False,
         'ordered_refs':[refs[GSS],refs[NCA]],'population_join':False}
    with pytest.raises(TypeError):
        read_historical_test_only(r,selected_refs=refs,relation=rel,as_of='2022-07-08',
                                   clock_mode='HISTORICAL_PUBLICATION_AWARE',values=[999,999])

def test_unsupported_asof_bad_date(packet):
    assert_code('INVALID_ASOF_OR_PUBLICATION_DATE',lambda:req(packet['fields'],as_of='2022-99-99'))

def test_sourcefree_output_cannot_claim_real_current(packet):
    out,_,_,_=req(packet['fields'])
    assert out['operative_OC05'] is False and out['real_N9_consumer'] is False
    assert out['issued_N5N6'] is False and out['issued_EE13'] is False
    assert out['model_use'] is False and out['person_exposure'] is False


def test_publication_backdate_fails_before_read(packet):
    x=deepcopy(packet['fields']);x[1]['publication_date']='2021-12-31'
    assert_code('PUBLICATION_OR_OBSERVATION_CLOCK_SUBSTITUTION',lambda:TestOnlyRegistry(x))

def test_observation_epoch_substitution_fails(packet):
    x=deepcopy(packet['fields']);x[0]['observation_period']='2022 PHC'
    assert_code('PUBLICATION_OR_OBSERVATION_CLOCK_SUBSTITUTION',lambda:TestOnlyRegistry(x))

def test_refused_mandatory_field_still_in_dependency_readset(packet):
    result,_,refs,_=req(packet['fields'],as_of='2022-03-01',partial=True)
    assert result['dependency_readset']==[refs[GSS],refs[NCA]]
    assert result['successful_value_refset']==[refs[GSS]]
    assert result['state']=='PARTIAL_TEST_ONLY_NOT_POSITIVE'

def test_revocation_still_in_dependency_readset(packet):
    x=deepcopy(packet['fields']);x[0]['status']='REVOKED_TEST_ONLY'
    result,_,refs,_=req(x,partial=True)
    assert result['dependency_readset']==[refs[GSS],refs[NCA]]
    assert result['successful_value_refset']==[refs[NCA]]
