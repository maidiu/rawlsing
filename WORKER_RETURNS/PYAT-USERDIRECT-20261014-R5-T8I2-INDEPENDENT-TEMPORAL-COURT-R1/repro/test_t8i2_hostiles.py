"""T8I2 frozen-after-commission, separately authored candidate hostiles.
An acceptance assertion that FAILS is a material missing guard; not an xfail.
Must import exact T8F2 blob 9a654b55274b2e8052b1cfaa0eef1a079c079f59.
Independence caveat: reviewer conversation also authored predecessor T8I.
"""
from copy import deepcopy
from dataclasses import replace
from fractions import Fraction as F
import pytest
import t8f2_temporal_custody as t


def setup(authority=t.REGISTRY_AUTHORITY):
    r=t.WaveFactRegistry(authority=authority)
    a,b=t.fixtures()
    ra,rb=r.register(a),r.register(b)
    p=t.compare_registered(r,ra,rb)
    return r,ra,rb,p


def resign(p):
    p['product_digest']=None
    p['product_digest']=t.digest(p)
    return p


def refuse(fn,code=None):
    with pytest.raises(t.Refusal) as e: fn()
    if code is not None: assert e.value.code==code


# Positive control tests

def test_control_author_issuer_ceiling_sourcefree():
    r,ra,rb,p=setup()
    out=t.consume_registered(r,p)
    assert out['consumer']=='T8F2_REGISTERED_HISTORICAL_VALUES_READER__NOT_REAL_N9'
    assert p['issued_EE12'] is False and p['measured_original_data'] is False


def test_control_variance_changes_ref_and_read_variance_not_delta():
    r,ra,rb,p=setup()
    a,b=t.fixtures()
    ra2=r.register(replace(a,variance=F(1,1250)))
    assert ra2!=ra and r.retrieve(ra).variance==F(1,2500)
    p2=t.compare_registered(r,ra2,rb)
    assert p2['delta_later_minus_earlier']==p['delta_later_minus_earlier']
    assert p2['variance_delta_independent']!=p['variance_delta_independent']
    assert p2['wave_refs']['later']==p['wave_refs']['later']


def test_control_native_cell_edit_changes_delta_and_readset():
    r,ra,rb,p=setup(); a,b=t.fixtures()
    b2=replace(b, category_weights=(F(7),F(15),F(30),F(36),F(22)))
    rb2=r.register(b2)
    p2=t.compare_registered(r,ra,rb2)
    c1=t.consume_registered(r,p); c2=t.consume_registered(r,p2)
    assert c1['selected_numeric_temporal_value']!=c2['selected_numeric_temporal_value']
    assert c1['values_read_digest']!=c2['values_read_digest']
    assert p['wave_refs']['earlier']==p2['wave_refs']['earlier']


def test_control_correct_ref_hash_year_and_revoke():
    r,ra,rb,p=setup()
    refuse(lambda:r.retrieve(replace(ra,year=2022)),'FACT_YEAR_MISMATCH')
    refuse(lambda:r.retrieve(replace(ra,content_hash='0'*64)),'FACT_HASH_MISMATCH')
    r.revoke(rb)
    refuse(lambda:t.consume_registered(r,p),'FACT_REVOKED')


def test_control_published_cutoff_2017_gap_and_refusals():
    r,ra,rb,p=setup()
    assert p['earlier']['refusal_native_code']==998
    assert p['later']['refusal_native_code']==8
    assert tuple(p['earlier']['categories'])==('0','1','2','3','4')
    refuse(lambda:t.compare_registered(r,ra,rb,asof='2024-09-30'),'HISTORICAL_ASOF_BEFORE_RELEASE')
    q=t.compare_registered(r,ra,rb,historical_year=2017)
    assert q['historical_intervening']=='UNKNOWN_UNOBSERVED_GAP'
    refuse(lambda:t.compare_registered(r,ra,rb,historical_year=2018),'HISTORICAL_TIME_UNAUTHORIZED')


def test_control_forged_arithmetic_rehash_refused():
    r,ra,rb,p=setup();p['delta_later_minus_earlier']=F(999)
    refuse(lambda:t.consume_registered(r,resign(p)),'TEMPORAL_DELTA_ARITHMETIC_MISMATCH')


def test_control_wrong_publication_clock_and_no_ee12():
    r,ra,rb,p=setup();p['later']['publication']='2000-01-01'
    refuse(lambda:t.consume_registered(r,resign(p)),'SOURCE_PUBLICATION_CLOCK_MISMATCH')
    r,ra,rb,p=setup();p['issued_EE12']=True
    refuse(lambda:t.consume_registered(r,resign(p)),'UNAUTHORIZED_EVIDENCE_GRADE')


# Hostiles expected to refuse; these FAIL on exact T8F2.

def test_red_forged_ref_source_retrieve():
    r,ra,rb,p=setup()
    refuse(lambda:r.retrieve(replace(ra,source='MALICIOUS_DIFFERENT_SOURCE')),'FACT_SOURCE_MISMATCH')


def test_red_forged_ref_version_retrieve():
    r,ra,rb,p=setup()
    refuse(lambda:r.retrieve(replace(rb,version='MALICIOUS_DIFFERENT_VERSION')),'FACT_VERSION_MISMATCH')


def test_red_blank_source_version_in_ref_retrieve():
    r,ra,rb,p=setup()
    refuse(lambda:r.retrieve(replace(ra,source='',version='')),'REF_SCHEMA_VIOLATION')


def test_red_consumer_source_forgery_resigned():
    r,ra,rb,p=setup()
    p['wave_refs']['later']['source']='OTHER_UNISSUED_ORIGINAL_SOURCE'
    refuse(lambda:t.consume_registered(r,resign(p)),'FACT_SOURCE_MISMATCH')


def test_red_consumer_version_forgery_resigned():
    r,ra,rb,p=setup()
    p['wave_refs']['earlier']['version']='OLD_OR_UNRELEASED_VERSION'
    refuse(lambda:t.consume_registered(r,resign(p)),'FACT_VERSION_MISMATCH')


def test_red_consumer_ref_unknown_extra_field_resigned():
    r,ra,rb,p=setup()
    p['wave_refs']['earlier']['source_issuer_permission']='FAKE_GRANTED'
    refuse(lambda:t.consume_registered(r,resign(p)),'REF_SCHEMA_VIOLATION')


def test_red_arbitrary_registry_authority_constructor():
    r,ra,rb,p=setup('ARBITRARY_SELF_GRANTED_REAL_AUTHORITY')
    refuse(lambda:t.consume_registered(r,p),'UNVERIFIED_REGISTRY_AUTHORITY')


def test_red_self_rehashed_time_order_inversion():
    r,ra,rb,p=setup(); p['time_order']=[2022,2012]
    refuse(lambda:t.consume_registered(r,resign(p)),'TEMPORAL_INVERSION')


def test_red_self_rehashed_historical_request_outside_allowed():
    r,ra,rb,p=setup();p['historical_requested']=2018
    refuse(lambda:t.consume_registered(r,resign(p)),'HISTORICAL_TIME_UNAUTHORIZED')


def test_red_forged_2017_gap_resigned():
    r,ra,rb,p=setup()
    p['historical_requested']=2017
    p['historical_intervening']='OBSERVED_2017_PROVEN'
    refuse(lambda:t.consume_registered(r,resign(p)),'HISTORICAL_INTERVENING_MISMATCH')


def test_red_self_rehashed_measured_original_data_upgrade():
    r,ra,rb,p=setup();p['measured_original_data']=True
    refuse(lambda:t.consume_registered(r,resign(p)),'REAL_SOURCE_ISSUANCE_LAUNDERING')


def test_red_self_rehashed_fixture_authorization_upgrade():
    r,ra,rb,p=setup();p['fixture_authorization']='ACTUAL_EE12_GRANTED'
    refuse(lambda:t.consume_registered(r,resign(p)),'FIXTURE_AUTHORIZATION_MISMATCH')


def test_red_self_rehashed_n8s_objective_claim():
    r,ra,rb,p=setup();p['N8S']='AUTHORIZED_CAUSAL_OBJECTIVE_INSTITUTION'
    refuse(lambda:t.consume_registered(r,resign(p)),'N8S_OR_CAUSAL_LAUNDERING')


def test_red_revocation_invalid_ref_must_not_revoke_authentic():
    r,ra,rb,p=setup()
    bad=replace(ra,content_hash='0'*64,source='ALTERNATIVE',version='COUNTERFEIT')
    refuse(lambda:r.revoke(bad),'FACT_HASH_MISMATCH')
    assert r.retrieve(ra).year==2012


def test_red_consumer_different_valid_registry_same_authority_must_be_bound():
    r,ra,rb,p=setup()
    other=t.WaveFactRegistry()
    a,b=t.fixtures();other.register(a);other.register(b)
    refuse(lambda:t.consume_registered(other,p),'REGISTRY_INSTANCE_OR_SNAPSHOT_MISMATCH')


def test_red_cold_replay_unissued_authority_is_not_cryptographic_signature():
    r,ra,rb,p=setup()
    # Separate unissued registry and byte-for-byte identical fixture data
    # do not supply issuer authorization or authenticated durable source custody.
    copied=t.WaveFactRegistry(authority=r.authority)
    a,b=t.fixtures();copied.register(a);copied.register(b)
    refuse(lambda:t.consume_registered(copied,deepcopy(p)),'REGISTRY_INSTANCE_OR_SNAPSHOT_MISMATCH')


def test_red_malformed_history_authority_metadata_not_validated():
    r,ra,rb,p=setup()
    p['design_uncertainty']='REAL_DESIGN_UNCERTAINTY_QUANTIFIED_AND_ISSUED'
    refuse(lambda:t.consume_registered(r,resign(p)),'DESIGN_UNCERTAINTY_GRADE_MISMATCH')
