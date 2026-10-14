"""HQ297 T8C SOURCEFREE_STANDALONE_ONLY. Not HQ214, N8E or N9 production."""
from __future__ import annotations
from dataclasses import dataclass, replace
from datetime import date
from fractions import Fraction as F
import hashlib, json
import pytest

GRADE = 'SOURCEFREE_STANDALONE_ONLY'
SPECIAL = ('DK', 'REFUSED', 'MISSING', 'NOT_ASKED')

class Refusal(ValueError):
    def __init__(self, code):
        self.code = code
        super().__init__(code)

def require(ok, code):
    if not ok:
        raise Refusal(code)

@dataclass(frozen=True)
class Wave:
    year: int
    field_start: str
    field_end: str
    publication: str
    question: str
    version: str
    refusal_code: int
    category_weights: tuple
    special_weights: tuple
    eligible_weight: F
    asked_weight: F
    native_category_codes: tuple = (0,1,2,3,4)
    national_weight: str = 'WITHINWT_TEST_ONLY'
    country_selector: str = 'GHA_NATIONAL_CITIZEN_18_PLUS_TEST_ONLY'
    population: str = 'GHA_CITIZEN_18_PLUS_TEST_ONLY'
    variance: F | None = F(1,2500)
    variance_method: str = 'HYPOTHETICAL_DESIGN_TEST_ONLY'
    sample_identity: str = 'INDEPENDENT_CROSS_SECTION_TEST_ONLY'

    def validate(self):
        require(self.year in (2012, 2022), 'UNOBSERVED_ANCHOR')
        expected = (('Q43','GHA_R5_2012_INSTRUMENT_TEST',998,'2012-05-08','2012-05-27','2015-07-16')
                    if self.year == 2012 else
                    ('Q31','GHA_R9_2022_INSTRUMENT_TEST',8,'2022-04-04','2022-04-20','2024-10-01'))
        require((self.question,self.version,self.refusal_code,self.field_start,self.field_end,self.publication)==expected,
                'QUESTION_RELEASE_OR_CLOCK_MISMATCH')
        require(len(self.category_weights)==5 and all(isinstance(x,F) and x>=0 for x in self.category_weights),
                'NATIVE_FIVE_CATEGORY_REQUIRED')
        require(self.native_category_codes == (0,1,2,3,4), 'NATIVE_CATEGORY_ZERO_MISSING')
        require(len(self.special_weights)==4 and all(isinstance(x,F) and x>=0 for x in self.special_weights),
                'NATIVE_SPECIALS_REQUIRED')
        require(self.eligible_weight==self.asked_weight+self.special_weights[3], 'ELIGIBLE_RISK_DENOMINATOR_MISMATCH')
        require(self.asked_weight==sum(self.category_weights)+sum(self.special_weights[:3]),
                'ASKED_DENOMINATOR_MISMATCH')
        require(self.national_weight=='WITHINWT_TEST_ONLY', 'WRONG_WEIGHT_BASIS')
        require(self.country_selector=='GHA_NATIONAL_CITIZEN_18_PLUS_TEST_ONLY', 'WRONG_NATIONAL_SELECTOR')
        require(self.population=='GHA_CITIZEN_18_PLUS_TEST_ONLY', 'POPULATION_MISMATCH')
        require(self.sample_identity=='INDEPENDENT_CROSS_SECTION_TEST_ONLY', 'FALSE_SAME_PERSON_OR_CIRCULAR_ESTIMATOR')
        require(self.variance is not None and isinstance(self.variance,F) and self.variance>=0
                and self.variance_method=='HYPOTHETICAL_DESIGN_TEST_ONLY', 'DESIGN_UNQUANTIFIED')
        require(sum(self.category_weights)>0, 'ZERO_VALID_SUPPORT')
        return self

def canonical(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {k:canonical(v) for k,v in sorted(x.items())}
    if isinstance(x,(list,tuple)): return [canonical(v) for v in x]
    return x

def digest(x):
    return hashlib.sha256(json.dumps(canonical(x),sort_keys=True,separators=(',',':')).encode()).hexdigest()

def compare(a,b, *, ee12='TEST_DOUBLE_ONLY', asof='2025-01-01', historical_year=2022):
    require(ee12=='TEST_DOUBLE_ONLY', 'UNISSUED_EE12')
    a.validate(); b.validate()
    require((a.year,b.year)==(2012,2022), 'TEMPORAL_INVERSION')
    require(a.population==b.population, 'POPULATION_MISMATCH')
    require(historical_year in (2012,2017,2022), 'HISTORICAL_TIME_UNAUTHORIZED')
    require(date.fromisoformat(asof)>=date.fromisoformat(b.publication), 'HISTORICAL_ASOF_BEFORE_RELEASE')
    def fact(w):
        den=sum(w.category_weights)
        return {'year':w.year,'field':[w.field_start,w.field_end], 'publication':w.publication,
                'question':w.question,'version':w.version,'categories':dict(zip(['0','1','2','3','4'],w.category_weights)),
                'specials':dict(zip(SPECIAL,w.special_weights)),'refusal_native_code':w.refusal_code,
                'eligible_weight':w.eligible_weight,'asked_weight':w.asked_weight,
                'valid_weight':den,'satisfied_share':(w.category_weights[3]+w.category_weights[4])/den,
                'variance':w.variance,'variance_method':w.variance_method,
                'population':w.population,'weight_basis':w.national_weight}
    p,q=fact(a),fact(b)
    out={'grade':GRADE,'issued_EE12':False,'measured_original_data':False,
         'fixture_authorization':'TEST_DOUBLE_ONLY_NOT_ISSUED',
         'time_order':[2012,2022], 'query_asof':asof, 'historical_requested':historical_year,
         'historical_intervening': 'UNKNOWN_UNOBSERVED_GAP' if historical_year==2017 else 'NATIVE_ANCHOR_ONLY',
         'earlier':p,'later':q,'delta_later_minus_earlier':q['satisfied_share']-p['satisfied_share'],
         'variance_delta_independent':p['variance']+q['variance'],
         'design_uncertainty':'HYPOTHETICAL_DESIGN_TEST_ONLY__NOT_ACTUAL_SURVEY_SE',
         'N8S':'NOT_APPLICABLE_SUBJECTIVE_REPORTS'}
    out['product_digest']=digest(out)
    return out

def consume(product, *, asof='2025-01-01', claim_same_person=False, selected_context='HISTORICAL_ATTITUDE_ONLY'):
    require(not claim_same_person, 'FALSE_SAME_PERSON_INFERENCE')
    require(selected_context=='HISTORICAL_ATTITUDE_ONLY', 'N8S_OR_CAUSAL_LAUNDERING')
    require(product['grade']==GRADE and product['issued_EE12'] is False, 'UNAUTHORIZED_EVIDENCE_GRADE')
    require(asof==product['query_asof'], 'MIXED_ASOF_POLICY')
    require(date.fromisoformat(asof)>=date.fromisoformat(product['later']['publication']),
            'HISTORICAL_ASOF_BEFORE_RELEASE')
    reads={'earlier':product['earlier'],'later':product['later'],
           'delta':product['delta_later_minus_earlier'], 'variance_delta':product['variance_delta_independent']}
    return {'consumer':'STANDALONE_HISTORICAL_ASOF_TEST_READER__NOT_REAL_N9', 'grade':GRADE,
            'query_asof':asof, 'historical_requested':product['historical_requested'],
            'historical_intervening':product['historical_intervening'],
            'values_read':reads, 'values_read_digest':digest(reads),
            'selected_numeric_temporal_value':reads['delta']}

def fixtures():
    a=Wave(2012,'2012-05-08','2012-05-27','2015-07-16','Q43','GHA_R5_2012_INSTRUMENT_TEST',998,
           tuple(F(x) for x in (10,20,25,30,15)),tuple(F(x) for x in (3,2,1,4)),F(110),F(106))
    b=Wave(2022,'2022-04-04','2022-04-20','2024-10-01','Q31','GHA_R9_2022_INSTRUMENT_TEST',8,
           tuple(F(x) for x in (12,18,20,35,25)),tuple(F(x) for x in (2,1,2,5)),F(120),F(115),variance=F(1,3000))
    return a,b

def expect(code, f):
    with pytest.raises(Refusal) as exc: f()
    assert exc.value.code == code

def test_positive_and_changed_consumer():
    a,b=fixtures(); x=compare(a,b); c=consume(x)
    assert x['earlier']['satisfied_share']==F(9,20)
    assert x['later']['satisfied_share']==F(6,11)
    assert x['delta_later_minus_earlier']==F(21,220)
    assert x['variance_delta_independent']==F(11,15000)
    assert c['selected_numeric_temporal_value']==F(21,220)
    assert x['earlier']['categories']['0']==10 and x['later']['categories']['0']==12
    assert x['earlier']['refusal_native_code']==998 and x['later']['refusal_native_code']==8
    altered=replace(b,category_weights=(F(12),F(18),F(19),F(35),F(26)))
    c2=consume(compare(a,altered))
    assert c2['selected_numeric_temporal_value']==F(23,220)
    assert c2['values_read_digest']!=c['values_read_digest']

def test_zero_drop():
    a,b=fixtures(); expect('NATIVE_FIVE_CATEGORY_REQUIRED',lambda:compare(replace(a,category_weights=a.category_weights[1:]),b))

def test_category_zero_as_missing():
    a,b=fixtures(); expect('NATIVE_CATEGORY_ZERO_MISSING',lambda:compare(replace(a,native_category_codes=(None,1,2,3,4)),b))

def test_question_version_swap():
    a,b=fixtures(); expect('QUESTION_RELEASE_OR_CLOCK_MISMATCH',lambda:compare(replace(a,version=b.version),b))

def test_denominator_risk():
    a,b=fixtures(); expect('ELIGIBLE_RISK_DENOMINATOR_MISMATCH',lambda:compare(replace(a,eligible_weight=F(100)),b))

def test_wrong_weights():
    a,b=fixtures(); expect('WRONG_WEIGHT_BASIS',lambda:compare(a,replace(b,national_weight='COMBINWT')))

def test_non_national_selector():
    a,b=fixtures(); expect('WRONG_NATIONAL_SELECTOR',lambda:compare(a,replace(b,country_selector='GHA_PLUS_OVERSAMPLE')))

def test_temporal_inversion():
    a,b=fixtures(); expect('TEMPORAL_INVERSION',lambda:compare(b,a))

def test_mixed_asof():
    a,b=fixtures(); x=compare(a,b);expect('MIXED_ASOF_POLICY',lambda:consume(x,asof='2026-01-01'))

def test_asof_earlier_than_publication():
    a,b=fixtures();expect('HISTORICAL_ASOF_BEFORE_RELEASE',lambda:compare(a,b,asof='2022-05-01'))

def test_same_person_claim():
    a,b=fixtures();expect('FALSE_SAME_PERSON_INFERENCE',lambda:consume(compare(a,b),claim_same_person=True))

def test_dependent_source_circular_estimator():
    a,b=fixtures();expect('FALSE_SAME_PERSON_OR_CIRCULAR_ESTIMATOR',lambda:compare(a,replace(b,sample_identity='SAME_RESPONDENTS')))

def test_unissued_EE12():
    a,b=fixtures();expect('UNISSUED_EE12',lambda:compare(a,b,ee12=None))

def test_2017_not_observed():
    a,b=fixtures();p=compare(a,b,historical_year=2017);c=consume(p)
    assert c['historical_intervening']=='UNKNOWN_UNOBSERVED_GAP'
    assert '2017' not in [str(x['year']) for x in [p['earlier'],p['later']]]

def test_false_2017_anchor():
    a,b=fixtures();expect('UNOBSERVED_ANCHOR',lambda:compare(replace(a,year=2017),b))

def test_missing_design_uncertainty():
    a,b=fixtures();expect('DESIGN_UNQUANTIFIED',lambda:compare(a,replace(b,variance=None)))

def test_structural_causal_laundering():
    a,b=fixtures();expect('N8S_OR_CAUSAL_LAUNDERING',lambda:consume(compare(a,b),selected_context='N8S_OBJECTIVE_RULE'))

def test_wrong_population():
    a,b=fixtures();expect('POPULATION_MISMATCH',lambda:compare(a,replace(b,population='SOME_VOTERS')))

def test_refusal_is_not_substantive():
    a,b=fixtures();expect('ASKED_DENOMINATOR_MISMATCH',lambda:compare(a,replace(b,special_weights=(F(2),F(0),F(2),F(5))),))

if __name__ == '__main__':
    a,b=fixtures(); x=compare(a,b); y=consume(x)
    print(json.dumps(canonical({'product':x,'consumer':y}),sort_keys=True,indent=2))
