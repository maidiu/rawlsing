"""R4 D2R separately written, sourcefree checks using exact SHA-verified D2P/N9C modules."""
from copy import deepcopy
from pathlib import Path
import json
import pytest
from d2p.external_fields import GSS, NCA, produce_two_fields, produce_field, FieldProducerError, _hash as producer_hash
from d2p.n9c_reader import TestOnlyRegistry, TestOnlyReadError, read_historical_test_only, fixture_invalidation


@pytest.fixture
def rows():
    return deepcopy(json.loads((Path(__file__).resolve().parents[1] / 'n9c_fields.json').read_text())['fields'])


def assembled(rows, at='2022-07-08', **flags):
    # Exactly D2P's existing two-registry scheme; this does NOT repair it.
    producer = produce_two_fields(rows)
    registry = TestOnlyRegistry(rows)
    refs = registry.refs_by_role()
    relation = {'kind':'TEST_ONLY_NONPOOLED_COPRESENCE', 'fixture_only':True,
                'issued_EE13':False, 'ordered_refs':[refs[GSS],refs[NCA]], 'population_join':False}
    consumer = read_historical_test_only(registry,selected_refs=refs,relation=relation,
                  as_of=at,clock_mode='HISTORICAL_PUBLICATION_AWARE',**flags)
    return producer,registry,refs,relation,consumer


def reject(fn, code):
    with pytest.raises((FieldProducerError,TestOnlyReadError)) as err: fn()
    assert err.value.code==code


def test_01_independently_computed_official_gss_and_nca_fixture_numbers(rows):
    p,_,_,_,r=assembled(rows)
    g=p[GSS]['values']; n=p[NCA]['values']
    assert sum(g['electricity_subtypes'].values())==g['numerator']==2388192
    assert g['denominator']==3288063 and round(100*g['numerator']/g['denominator'],1)==72.6
    assert n['prepaid']+n['postpaid']==n['active_subscriptions']==23414527
    assert r['state']=='TWO_VALUES_READ_TEST_ONLY'


def test_02_producer_internal_content_hash_is_consistent(rows):
    p=produce_two_fields(rows)
    for x in p.values():
        copy=deepcopy(x);ref=copy.pop('field_ref')
        assert ref=='D2P_TESTONLY_FIELD:'+producer_hash(copy)


def test_03_two_roles_have_different_real_native_units(rows):
    p=produce_two_fields(rows)
    assert p[GSS]['native_unit']=='RURAL_OCCUPIED_HOUSEHOLD_MAIN_LIGHTING'
    assert p[NCA]['native_unit']=='ACTIVE_MOBILE_DATA_SUBSCRIPTIONS_NOT_UNIQUE_PERSONS'
    assert p[GSS]['native_geography']=='GHANA_RURAL'
    assert p[NCA]['native_geography']=='GHANA_NATIONAL'


def test_04_actual_produced_and_reader_ref_namespaces_disjoint(rows):
    p,_,refs,_,consumer=assembled(rows)
    assert not ({p[GSS]['field_ref'],p[NCA]['field_ref']} & set(refs.values()))
    assert consumer['dependency_readset']==[refs[GSS],refs[NCA]]
    assert p[GSS]['field_ref'] not in consumer['dependency_readset']


def test_05_real_reader_registry_rejects_produced_field_ref(rows):
    p,r,_,_,_=assembled(rows)
    for role in (GSS,NCA):
        reject(lambda role=role:r.dereference(p[role]['field_ref']),'UNKNOWN_EXACT_FIELD_REF')


def test_06_reader_ref_points_to_row_not_producer_contract(rows):
    p,reg,refs,_,_=assembled(rows)
    row=reg.dereference(refs[GSS])
    assert 'field_version' not in row and 'producer_id' not in row
    assert row==p[GSS]['underlying_row']

@pytest.mark.parametrize('at,state',[
    ('2021-12-31','REFUSED_REQUIRED_FIELD_TEST_ONLY'),
    ('2022-02-23','REFUSED_REQUIRED_FIELD_TEST_ONLY'),
    ('2022-03-01','REFUSED_REQUIRED_FIELD_TEST_ONLY'),
    ('2022-07-07','REFUSED_REQUIRED_FIELD_TEST_ONLY'),
    ('2022-07-08','TWO_VALUES_READ_TEST_ONLY'),
])
def test_07_publication_clock_cutoff(rows,at,state):
    assert assembled(rows,at=at)[4]['state']==state


def test_08_partial_is_nonpositive(rows):
    x=assembled(rows,at='2022-03-01',partial_allowed=True)[4]
    assert x['state']=='PARTIAL_TEST_ONLY_NOT_POSITIVE' and len(x['values_read'])==1
    assert x['dependency_readset'] and len(x['dependency_readset'])==2


def test_09_gss_mutation_isolated_at_reader_row_refs(rows):
    a=assembled(rows)
    changed=deepcopy(rows);changed[0]['values']['numerator']-=1;changed[0]['values']['electricity_subtypes']['mains']-=1
    b=assembled(changed)
    assert a[0][GSS]['field_ref']!=b[0][GSS]['field_ref']
    assert a[0][NCA]['field_ref']==b[0][NCA]['field_ref']
    assert a[2][GSS]!=b[2][GSS] and a[2][NCA]==b[2][NCA]
    assert a[4]['values_read'][1]==b[4]['values_read'][1]
    assert b[4]['values_read'][0]['values']['numerator']==2388191
    assert fixture_invalidation(a[4],b[4])['changed_roles']==[GSS]


def test_10_nca_mutation_isolated_at_reader_row_refs(rows):
    a=assembled(rows)
    changed=deepcopy(rows);changed[1]['values']['active_subscriptions']+=1;changed[1]['values']['prepaid']+=1
    b=assembled(changed)
    assert a[0][GSS]['field_ref']==b[0][GSS]['field_ref']
    assert a[0][NCA]['field_ref']!=b[0][NCA]['field_ref']
    assert a[4]['values_read'][0]==b[4]['values_read'][0]
    assert b[4]['values_read'][1]['values']['active_subscriptions']==23414528
    assert fixture_invalidation(a[4],b[4])['changed_roles']==[NCA]


def test_11_revocation_refused_preserves_attempted_readset(rows):
    rows[1]['status']='REVOKED_TEST_ONLY'
    p,reg,refs,rel,out=assembled(rows)
    assert out['state']=='REFUSED_REQUIRED_FIELD_TEST_ONLY' and out['values_read']==[]
    assert out['dependency_readset']==[refs[GSS],refs[NCA]]
    assert any(v['reason']=='SOURCE_REVOKED' for v in out['refusals'])

@pytest.mark.parametrize('field,value,code',[
    ('issuer_signature','fake signer','ISSUER_FORGERY'),
    ('issued',True,'ISSUER_FORGERY'),
    ('source_pdf_sha256','fakepdfsha','UNVERIFIED_BINARY_CUSTODY'),
    ('issuer_ref','fake-source-grant','EXTERNAL_CUSTODY_OR_ISSUER_FORGERY'),
    ('permission','REAL_USE_GRANT','REAL_USE_PERMISSION_NOT_ISSUED'),
    ('fixture_only',False,'FIELD_ISSUANCE_LAUNDERING'),
])
def test_12_producer_forgery_refusal(rows,field,value,code):
    rows[0][field]=value
    reject(lambda:produce_two_fields(rows),code)

@pytest.mark.parametrize('field,value,code',[
    ('native_unit','RURAL_PHONE_PEOPLE','NCA_NATIVE_UNIT_GEOGRAPHY_MEASURE_CONFLICT'),
    ('native_geography','GHANA_RURAL','NCA_NATIVE_UNIT_GEOGRAPHY_MEASURE_CONFLICT'),
    ('native_measure','UNIQUE_PERSONS_WITH_PHONE','NCA_NATIVE_UNIT_GEOGRAPHY_MEASURE_CONFLICT'),
    ('unique_persons',True,'NCA_RURAL_OR_UNIQUE_PERSON_INFERENCE'),
    ('rural_split',27,'NCA_RURAL_OR_UNIQUE_PERSON_INFERENCE'),
])
def test_13_nca_wrong_unit_and_individual_inference_refuses_reader(rows,field,value,code):
    rows[1][field]=value
    reject(lambda:TestOnlyRegistry(rows),code)


def test_14_gss_wrong_individual_unit_refuses_reader(rows):
    rows[0]['native_unit']='PERSON_HAS_ELECTRICITY'
    reject(lambda:TestOnlyRegistry(rows),'GSS_NATIVE_UNIT_GEOGRAPHY_MEASURE_CONFLICT')


def test_15_mains_only_numerator_refused_as_all_electricity(rows):
    rows[0]['values']['numerator']=2288193
    reject(lambda:TestOnlyRegistry(rows),'GSS_VALUE_DENOMINATOR_OR_SUBTYPE_INTEGRITY')


def test_16_missing_exclusions_refused(rows):
    rows[0]['exclusions']=['VACANT_DWELLINGS']
    reject(lambda:TestOnlyRegistry(rows),'GSS_EXCLUSION_DROPPED')

@pytest.mark.parametrize('flag', ['requested_person_exposure','requested_pooling','requested_model_use'])
def test_17_individual_pooling_model_inference_refused(rows,flag):
    p,reg,refs,rel,_=assembled(rows)
    reject(lambda:read_historical_test_only(reg,selected_refs=refs,relation=rel,
              as_of='2022-07-08',clock_mode='HISTORICAL_PUBLICATION_AWARE',**{flag:True}),
           'PERSON_POOLING_OR_MODEL_PROMOTION_FORBIDDEN')


def test_18_claim_issued_EE13_is_refused(rows):
    p,reg,refs,rel,_=assembled(rows);rel['issued_EE13']=True
    reject(lambda:read_historical_test_only(reg,selected_refs=refs,relation=rel,
              as_of='2022-07-08',clock_mode='HISTORICAL_PUBLICATION_AWARE'),
           'INDEPENDENT_EE13_NOT_ISSUED_OR_RELATION_CHANGED')


def test_19_wrong_asof_and_current_refused(rows):
    p,reg,refs,rel,_=assembled(rows)
    reject(lambda:read_historical_test_only(reg,selected_refs=refs,relation=rel,
              as_of='yesterday',clock_mode='HISTORICAL_PUBLICATION_AWARE'),
           'INVALID_ASOF_OR_PUBLICATION_DATE')
    reject(lambda:read_historical_test_only(reg,selected_refs=refs,relation=rel,
              as_of='2022-07-08',clock_mode='CURRENT'),
           'CURRENT_OR_OTHER_CLOCK_NOT_AUTHORIZED')


def test_20_deterministic_replay_selected_snapshot(rows):
    a=assembled(rows)[4];b=assembled(deepcopy(rows))[4]
    assert a==b and a['test_snapshot_ref']==b['test_snapshot_ref']
