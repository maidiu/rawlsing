from copy import deepcopy
import json
from pathlib import Path
import pytest
from d2i_sourcefree import CourtHold, Registry, GSS, NCA, nonpooled_relation, historical_read, diff

DOC=Path(__file__).with_name('01_ORIGINAL_EDITION_BINARY_AND_METHOD.json')
@pytest.fixture
def rows(): return deepcopy(json.loads(DOC.read_text())['sources'])
def run(rows,asof='2022-07-08',**kwargs):
    reg=Registry(rows);return historical_read(reg,nonpooled_relation(reg),asof,**kwargs),reg

def reject(code,f):
    with pytest.raises(CourtHold) as e:f()
    assert e.value.code==code

def test_real_primary_published_numbers_dereferenced_not_only_refs(rows):
    out,reg=run(rows);assert out['status']=='TWO_VALUES_DEREFERENCED_TEST_ONLY'
    assert out['value_slots'][GSS]['values']['rural_electric_total']==2388192
    assert out['value_slots'][GSS]['values']['rural_occupied_total']==3288063
    assert out['value_slots'][GSS]['values']['published_pct']==72.6
    assert out['value_slots'][NCA]['values']['subscriptions']==23414527
    assert out['value_slots'][NCA]['values']['prepaid']==23237338
    assert out['value_slots'][NCA]['values']['postpaid']==177189
    assert not out['operative_OC05'] and not out['N5N6_issued'] and not out['N7_EE13_issued']

def test_distinct_units_and_geographies(rows):
    a,reg=run(rows);assert a['value_slots'][GSS]['unit']!=a['value_slots'][NCA]['unit']
    assert a['value_slots'][GSS]['geography']!='GHANA_NATIONAL'
    assert a['value_slots'][NCA]['geography']=='GHANA_NATIONAL'
    assert not a['same_population'] and not a['person_inference'] and not a['correlation']

def test_all_five_electric_subtypes(rows):
    a=rows[0]['values'];assert sum(a['electric_subtypes'].values())==a['rural_electric_total']
    assert round(a['rural_electric_total']/a['rural_occupied_total']*100,1)==72.6
    assert round(a['electric_subtypes']['mains']/a['rural_occupied_total']*100,1)==69.6

def test_publication_2021_refuses_both(rows):
    a,_=run(rows,'2021-12-31',partial=True);assert a['status']=='REQUIRED_SOURCE_UNAVAILABLE_HOLD'
    assert a['value_slots']=={} and list(a['denials'].values())==['NOT_YET_PUBLISHED']*2

def test_march_2022_partial_only_not_2source_positive(rows):
    a,_=run(rows,'2022-03-01',partial=True);assert a['status']=='PARTIAL_TEST_ONLY_NONPOSITIVE'
    assert list(a['value_slots'])==[GSS] and a['denials']=={NCA:'NOT_YET_PUBLISHED'}

def test_march_2022_nonpartial_holds(rows):
    a,_=run(rows,'2022-03-01');assert a['value_slots']=={} and a['status']=='REQUIRED_SOURCE_UNAVAILABLE_HOLD'

def test_july_7_2022_earlier_than_NCA(rows):
    a,_=run(rows,'2022-07-07');assert a['value_slots']=={} and a['denials']=={NCA:'NOT_YET_PUBLISHED'}

def test_cold_replay_stable_and_numbers_read(rows):
    a,_=run(rows);b,_=run(deepcopy(rows));assert a==b

def test_mutate_GSS_one_only_updates_GSS_slot(rows):
    a,_=run(rows);brows=deepcopy(rows);brows[0]['values']['rural_electric_total']-=1;brows[0]['values']['electric_subtypes']['mains']-=1
    b,_=run(brows);d=diff(a,b);assert d['changed_source_roles']==[GSS] and d['unaffected_source_roles']==[NCA]
    assert a['value_slots'][NCA]==b['value_slots'][NCA] and a['value_slots'][GSS]!=b['value_slots'][GSS]

def test_mutate_NCA_one_only_updates_NCA_slot(rows):
    a,_=run(rows);brows=deepcopy(rows);brows[1]['values']['subscriptions']+=1;brows[1]['values']['prepaid']+=1
    b,_=run(brows);d=diff(a,b);assert d['changed_source_roles']==[NCA] and d['unaffected_source_roles']==[GSS]
    assert a['value_slots'][GSS]==b['value_slots'][GSS] and a['value_slots'][NCA]!=b['value_slots'][NCA]

def test_replayed_previous_source_ref_is_not_new_revision(rows):
    a,old=run(rows);newrows=deepcopy(rows);newrows[1]['values']['subscriptions']+=1;newrows[1]['values']['postpaid']+=1
    b,new=run(newrows);assert old.by_role[NCA]!=new.by_role[NCA] and old.by_role[GSS]==new.by_role[GSS]
    reject('STALE_OR_UNKNOWN_SOURCE_REF',lambda:new.read(old.by_role[NCA]))

def test_revocation_holds_both(rows):
    rows[1]['status']='REVOKED_TEST_ONLY';a,_=run(rows)
    assert a['status']=='REQUIRED_SOURCE_UNAVAILABLE_HOLD' and a['denials']=={NCA:'SOURCE_REVOKED'}

def test_revocation_explicit_partial_not_positive(rows):
    rows[1]['status']='REVOKED_TEST_ONLY';a,_=run(rows,partial=True)
    assert list(a['value_slots'])==[GSS] and a['status']=='PARTIAL_TEST_ONLY_NONPOSITIVE'

@pytest.mark.parametrize('mutation,code',[
    (('unit','UNIQUE_PEOPLE'),'NCA_SOURCE_OR_UNIT'),
    (('geography','GHANA_RURAL'),'NCA_SOURCE_OR_UNIT'),
    (('unique_persons',True),'NCA_ECOLOGICAL_FALLACY'),
    (('rural_breakout',42),'NCA_ECOLOGICAL_FALLACY'),
    (('published_at','2021-12-31'),'NCA_SOURCE_OR_UNIT'),
    (('issuer_signature','FORGED'),'ISSUER_FORGERY'),
    (('source_pdf_sha256','FAKE'),'UNVERIFIED_BINARY_CUSTODY'),
    (('pdf_bytes_captured',True),'UNVERIFIED_BINARY_CUSTODY'),
    (('issued',True),'ISSUER_FORGERY'),
    (('permission','GRANTED'),'PERMISSION_FORGERY'),
])
def test_NCA_hostile_metadata(rows,mutation,code):
    k,v=mutation;rows[1][k]=v;reject(code,lambda:Registry(rows))

@pytest.mark.parametrize('mutation,code',[
    (('unit','PERSON_HAS_ELECTRICITY'),'GSS_SOURCE_OR_UNIT'),
    (('geography','GHANA_NATIONAL'),'GSS_SOURCE_OR_UNIT'),
    (('excluded',[]),'GSS_DENOMINATOR_SCOPE'),
    (('issuer_signature','FAKE'),'ISSUER_FORGERY'),
])
def test_GSS_hostile_metadata(rows,mutation,code):
    k,v=mutation;rows[0][k]=v;reject(code,lambda:Registry(rows))

def test_false_GSS_numerator(rows):
    rows[0]['values']['rural_electric_total']+=42;reject('GSS_NUMERIC_INTEGRITY',lambda:Registry(rows))
def test_false_NCA_split(rows):
    rows[1]['values']['subscriptions']+=3;reject('NCA_NUMERIC_INTEGRITY',lambda:Registry(rows))

def test_relation_forgery_rejected(rows):
    reg=Registry(rows);r=nonpooled_relation(reg);r['issued_EE13']=True
    reject('EE13_FORGERY_OR_POOLING',lambda:historical_read(reg,r,'2022-07-08'))

def test_relation_pooling_rejected(rows):
    reg=Registry(rows);r=nonpooled_relation(reg);r['same_population']=True
    reject('EE13_FORGERY_OR_POOLING',lambda:historical_read(reg,r,'2022-07-08'))

def test_relation_stale_after_source_revision(rows):
    reg=Registry(rows);r=nonpooled_relation(reg);r['refs'][1]='STALE'
    reject('STALE_RELATION_REFERENCES',lambda:historical_read(reg,r,'2022-07-08'))

@pytest.mark.parametrize('flag',['requested_person','requested_pool','requested_correlation','requested_model'])
def test_inference_or_model_use_refused(rows,flag):
    reg=Registry(rows);reject('ECOLOGICAL_OR_CAUSAL_USE_FORBIDDEN',lambda:historical_read(reg,nonpooled_relation(reg),'2022-07-08',**{flag:True}))

def test_current_OC05_claim_rejected(rows):
    reg=Registry(rows);reject('OC05_OR_CURRENT_UNISSUED',lambda:historical_read(reg,nonpooled_relation(reg),'2022-07-08',mode='CURRENT'))

def test_bad_asof_rejected(rows):
    reg=Registry(rows);reject('INVALID_CLOCK',lambda:historical_read(reg,nonpooled_relation(reg),'nonsense'))

def test_duplicate_source_role_refused(rows):
    rows[1]['role']=GSS;reject('GSS_SOURCE_OR_UNIT',lambda:Registry(rows))

def test_no_unverified_archive_sha_claim(rows):
    a,reg=run(rows);assert all(reg.read(ref)['source_pdf_sha256'] is None for ref in a['attempted_refs'])
