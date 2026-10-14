"""Independent T8R sourcefree review, tests exact pinned T8C imported module unchanged."""
from dataclasses import replace
from fractions import Fraction as F
from copy import deepcopy
import test_hq297_t8c as candidate
import pytest

def test_baseline_replayed_hash_and_value():
    a,b=candidate.fixtures(); p=candidate.compare(a,b); c=candidate.consume(p)
    assert p['product_digest']=='c74fc711131c355c85e84f87adde6709789180b69bef8f0634a636ba64dbe0a4'
    assert c['values_read_digest']=='f43a2abac609ae25810dcbb2cddc5350f5d74b770772ef3b1da5a758b9471138'

def test_independent_0_to_positive_move_changes_value():
    a,b=candidate.fixtures()
    revised=replace(b,category_weights=(F(11),F(18),F(20),F(36),F(25)))
    old=candidate.consume(candidate.compare(a,b)); new=candidate.consume(candidate.compare(a,revised))
    assert new['selected_numeric_temporal_value']-old['selected_numeric_temporal_value']==F(1,110)
    assert new['values_read']['later']['categories']['0']==11
    assert new['values_read_digest']!=old['values_read_digest']

def test_independent_0_to_1_move_changes_digest_but_not_satisfied_share():
    a,b=candidate.fixtures(); revised=replace(b,category_weights=(F(13),F(17),F(20),F(35),F(25)))
    old=candidate.consume(candidate.compare(a,b)); new=candidate.consume(candidate.compare(a,revised))
    assert new['selected_numeric_temporal_value']==old['selected_numeric_temporal_value']
    assert new['values_read_digest']!=old['values_read_digest']

def test_no_2017_anchor_and_no_measured_2017():
    a,b=candidate.fixtures();p=candidate.compare(a,b,historical_year=2017)
    assert p['historical_intervening']=='UNKNOWN_UNOBSERVED_GAP'
    assert set(p['time_order'])=={2012,2022}

def test_wrong_population_and_weight_both_refuse():
    a,b=candidate.fixtures()
    with pytest.raises(candidate.Refusal,match='WRONG_WEIGHT_BASIS'):
        candidate.compare(a,replace(b,national_weight='COMBINWT'))
    with pytest.raises(candidate.Refusal,match='POPULATION_MISMATCH'):
        candidate.compare(a,replace(b,population='GHA_ADULT_RESIDENT_NONCITIZENS'))

def test_publication_asof_not_observation_year():
    a,b=candidate.fixtures()
    with pytest.raises(candidate.Refusal,match='HISTORICAL_ASOF_BEFORE_RELEASE'):
        candidate.compare(a,b,asof='2022-12-31')
    assert candidate.consume(candidate.compare(a,b,asof='2025-01-01'))['query_asof']=='2025-01-01'

def test_swapped_question_and_issuer_none_refuse():
    a,b=candidate.fixtures()
    with pytest.raises(candidate.Refusal,match='QUESTION_RELEASE_OR_CLOCK_MISMATCH'):
        candidate.compare(a,replace(b,question='Q43'))
    with pytest.raises(candidate.Refusal,match='UNISSUED_EE12'):
        candidate.compare(a,b,ee12=None)

def test_refusal_routing_counts_remain_distinct():
    a,b=candidate.fixtures(); x=candidate.compare(a,b)
    assert x['earlier']['specials']=={'DK':F(3),'REFUSED':F(2),'MISSING':F(1),'NOT_ASKED':F(4)}
    assert x['later']['specials']=={'DK':F(2),'REFUSED':F(1),'MISSING':F(2),'NOT_ASKED':F(5)}
    assert x['earlier']['valid_weight']+sum(x['earlier']['specials'].values())==x['earlier']['eligible_weight']

# Explicit contract REDs: these should pass as review when demonstrating unsafe acceptance.
def test_red_tampered_delta_accepted_with_stale_digest():
    a,b=candidate.fixtures(); p=candidate.compare(a,b)
    bad=deepcopy(p); bad['delta_later_minus_earlier']=F(999)
    # A safe consumer MUST refuse stale digest and inconsistency; present consumer does not.
    actual=candidate.consume(bad)
    assert actual['selected_numeric_temporal_value']==F(999)
    assert bad['product_digest']==p['product_digest']

def test_red_mutated_native_zero_accepted_with_stale_digest():
    a,b=candidate.fixtures();p=candidate.compare(a,b)
    bad=deepcopy(p); bad['later']['categories']['0']=F(999)
    actual=candidate.consume(bad)
    assert actual['values_read']['later']['categories']['0']==F(999)
    assert bad['product_digest']==p['product_digest']

def test_red_invalid_asof_raises_untyped_value_error():
    a,b=candidate.fixtures()
    with pytest.raises(ValueError) as exc:
        candidate.compare(a,b,asof='not-a-date')
    assert not isinstance(exc.value,candidate.Refusal)
