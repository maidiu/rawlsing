"""T8I frozen independent acceptance hostiles (sourcefree; deliberately RED on missing guards).

PIN: T8F implementation Git blob 0108947afcec5797581e7c0d062c9aa655e6d6e1.
Frozen hypotheses committed at T8I 04_FROZEN_INDEPENDENT_EXPECTATIONS.json,
commit ccc7e539edf643be6c94d40a3fa3005e3bc0191c, BEFORE these tests.
A failing test is a reproduced acceptance violation; not an external source claim.
"""
from dataclasses import replace
from fractions import Fraction as F
import pytest
import t8f_temporal_integrity as m


def resign(p):
    p = dict(p)
    p['product_digest'] = None
    p['product_digest'] = m.digest(p)
    return p


def pair():
    return m.fixtures()


def product():
    return m.compare(*pair())


def must_refuse(fn, expected=None):
    with pytest.raises(m.Refusal) as exc:
        fn()
    if expected:
        assert exc.value.code == expected


def test_control_original_valid_product_consumes():
    p = product()
    c = m.consume(p)
    assert c['selected_numeric_temporal_value'] == p['delta_later_minus_earlier']
    assert c['historical_intervening'] == 'NATIVE_ANCHOR_ONLY'


def test_control_stale_delta_digest_refused():
    p = product()
    p['delta_later_minus_earlier'] = F(999)
    must_refuse(lambda: m.consume(p), 'PRODUCT_DIGEST_MISMATCH')


def test_control_stale_native_category_digest_refused():
    p = product()
    p['later']['categories']['3'] += F(5)
    must_refuse(lambda: m.consume(p), 'PRODUCT_DIGEST_MISMATCH')


def test_control_rehashed_native_category_unbalanced_share_refused():
    p = product()
    p['later']['categories']['3'] += F(5)
    must_refuse(lambda: m.consume(resign(p)), 'SATISFIED_SHARE_ARITHMETIC_MISMATCH_LATER')


def test_control_malformed_asof_typed():
    must_refuse(lambda: m.compare(*pair(), asof='not-a-date'), 'INVALID_ASOF_DATE')
    must_refuse(lambda: m.consume(product(), asof='not-a-date'), 'MIXED_ASOF_POLICY')
    p = product()
    p['query_asof'] = 'not-a-date'
    must_refuse(lambda: m.consume(resign(p), asof='not-a-date'), 'INVALID_ASOF_DATE')


def test_control_native_category_zero_and_nonresponse_and_gap():
    a,b=pair()
    p=m.compare(a,b,historical_year=2017)
    assert sorted(p['earlier']['categories']) == ['0','1','2','3','4']
    assert sorted(p['earlier']['specials']) == ['DK','MISSING','NOT_ASKED','REFUSED']
    assert p['earlier']['refusal_native_code']==998 and p['later']['refusal_native_code']==8
    assert p['earlier']['eligible_weight'] == p['earlier']['asked_weight'] + p['earlier']['specials']['NOT_ASKED']
    assert p['later']['eligible_weight'] == p['later']['asked_weight'] + p['later']['specials']['NOT_ASKED']
    assert m.consume(p)['historical_intervening'] == 'UNKNOWN_UNOBSERVED_GAP'
    must_refuse(lambda: m.compare(a,b, asof='2024-09-30'), 'HISTORICAL_ASOF_BEFORE_RELEASE')
    must_refuse(lambda: m.compare(a,b,ee12='ACTUAL_ISSUED'), 'UNISSUED_EE12')
    must_refuse(lambda: m.consume(p,claim_same_person=True), 'FALSE_SAME_PERSON_INFERENCE')


# Hostile acceptance assertions: these should raise a typed Refusal; current T8F doesn't.

def test_red_registry_distinct_valid_variance_no_identity_collision():
    a,_=pair()
    altered=replace(a, variance=F(1,1250))
    assert a.variance != altered.variance
    assert a.content_hash() != altered.content_hash(), 'Two distinct scientifically material variance inputs hash identically'


def test_red_registry_old_ref_retains_original_fact():
    a,_=pair()
    reg=m.WaveFactRegistry()
    old=reg.register(a)
    newer=reg.register(replace(a,variance=F(1,1250)))
    assert old != newer, 'Registry reuses a colliding content ref'
    assert reg.retrieve(old).variance == a.variance, 'Old immutable ref now reads substituted variance'


def test_red_wave_ref_year_bound_to_fact():
    a,_=pair();reg=m.WaveFactRegistry();ref=reg.register(a)
    forged=replace(ref,year=2022)
    must_refuse(lambda:reg.retrieve(forged), 'FACT_YEAR_MISMATCH')


def test_red_mutable_category_list_defensively_copied_on_registration():
    a,_=pair(); aliased=list(a.category_weights)
    mutable=replace(a,category_weights=aliased)
    reg=m.WaveFactRegistry();ref=reg.register(mutable)
    aliased[0] += F(1)
    assert reg.retrieve(ref).category_weights[0] == a.category_weights[0], 'External list mutation polluted stored fact'


def test_red_self_resigned_forged_delta_refused():
    p=product();p['delta_later_minus_earlier']=F(999)
    must_refuse(lambda:m.consume(resign(p)), 'TEMPORAL_DELTA_ARITHMETIC_MISMATCH')


def test_red_self_resigned_forged_variance_delta_refused():
    p=product();p['variance_delta_independent']=F(999)
    must_refuse(lambda:m.consume(resign(p)), 'VARIANCE_DELTA_ARITHMETIC_MISMATCH')


def test_red_consistent_numerical_source_rewrite_refused_without_verified_refs():
    p=product(); q=p['later'];q['categories']['3']+=F(5)
    q['valid_weight']+=F(5);q['asked_weight']+=F(5);q['eligible_weight']+=F(5)
    q['satisfied_share']=(q['categories']['3']+q['categories']['4'])/sum(q['categories'].values())
    p['delta_later_minus_earlier']=q['satisfied_share']-p['earlier']['satisfied_share']
    must_refuse(lambda:m.consume(resign(p)), 'UNVERIFIED_SOURCE_VALUE_OR_REF')


def test_red_rewritten_historical_publication_and_asof_refused():
    p=product();p['later']['publication']='2000-01-01';p['query_asof']='2001-01-01'
    must_refuse(lambda:m.consume(resign(p),asof='2001-01-01'),'SOURCE_PUBLICATION_CLOCK_MISMATCH')


def test_red_rewritten_eligible_risk_refused():
    p=product();p['later']['eligible_weight']+=F(30)
    must_refuse(lambda:m.consume(resign(p)), 'ELIGIBLE_RISK_DENOMINATOR_MISMATCH')


def test_red_forged_semantics_native_code_omission_refused():
    p=product()
    del p['earlier']['categories']['0']
    p['earlier']['satisfied_share']=(p['earlier']['categories']['3']+p['earlier']['categories']['4'])/sum(p['earlier']['categories'].values())
    p['delta_later_minus_earlier']=p['later']['satisfied_share']-p['earlier']['satisfied_share']
    must_refuse(lambda:m.consume(resign(p)), 'NATIVE_CATEGORY_ZERO_MISSING')
