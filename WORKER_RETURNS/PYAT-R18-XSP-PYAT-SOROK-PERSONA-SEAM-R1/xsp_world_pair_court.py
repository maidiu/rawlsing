#!/usr/bin/env python3
"""Independent XSP source-free expected-option witness.

NOT a Pyat/Sorok native owner import or an operational interface. It is a bounded
counterfactual sanity court with independently frozen JSON inputs. All outputs
are actor-independent and all distributions are explicitly synthetic.
"""
import copy
import hashlib
import json
from datetime import date
from fractions import Fraction
from pathlib import Path

FROZEN = Path(__file__).with_name('01_frozen_world_pairs.json')
FROZEN_SHA256 = '00b91dd20cf28f44fe473b3abd010552c1190b7cd81388268f233b8fee417c09'


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def load_precommit():
    actual = hashlib.sha256(FROZEN.read_bytes()).hexdigest()
    if actual != FROZEN_SHA256:
        raise ValueError('PRECOMMITTED_EXPECTATION_IDENTITY_MISMATCH')
    return json.loads(FROZEN.read_text())


def world_from(base, changes):
    result = copy.deepcopy(base)
    for k, v in changes.items():
        result[k] = copy.deepcopy(v)
    return result


def _day(text):
    return date.fromisoformat(text)


def decide(world, requested='ACTOR_INDEPENDENT_OPTIONS'):
    if requested == 'GENERATED_PERSON_BIOGRAPHY':
        return {'state':'REFUSE_ACTOR_AUTHORITY', 'person_fact':None}
    if requested == 'PARENT_DYAD_PROBABILITY':
        return {'state':'REFUSE_SAMPLING_UNIT_AUTHORITY', 'person_fact':None}
    if requested == 'OPERATIVE_ORIGINAL_WORLD':
        return {'state':'REFUSE_UNISSUED_SOURCE_AND_N9', 'person_fact':None}
    if not world['world_read']:
        return {'state':'REFUSE_WORLD_READ', 'person_fact':None}
    if _day(world['publication']) > _day(world['as_of']):
        return {'state':'HELD_NOT_KNOWN_ASOF', 'person_fact':None, 'possibility':None}
    if world['institutional_access'] not in ('OPEN','FEE_BLOCKED') or world['care_time'] not in ('LOW','HIGH'):
        return {'state':'REFUSE_UNKNOWN_RULE_OR_PERMISSION', 'person_fact':None}
    empirical = world['empirical']
    yes, no, den = [empirical[k] for k in ('yes','no','denominator')]
    if any(type(z) is not int or z < 0 for z in (yes,no,den)) or den == 0 or yes + no != den:
        return {'state':'REFUSE_INVALID_NATIVE_GEOMETRY', 'person_fact':None}
    # These are TEST_ONLY modeled route categories, NEVER probability estimates.
    school = 'ELIGIBLE_IN_MODELED_CONTEXT' if world['institutional_access']=='OPEN' else 'BLOCKED_BY_MODELED_FEE_RULE'
    time = world['care_time']
    routes = {
        'formal_schooling': school,
        'nonformal_peer_study':'POSSIBLE' if time=='LOW' else 'POSSIBLE_BUT_TIME_CONSTRAINED',
        'paid_apprenticeship':'POSSIBLE' if time=='LOW' else 'POSSIBLE_WITH_HIGHER_TIME_TRADEOFF',
        'mutual_aid_participation':'POSSIBLE',
        'family_care_work':'PRESSURE_POSSIBLE_NOT_ACTUAL_OCCURRENCE'
    }
    possibility = {'yes':[Fraction(yes,den).numerator,Fraction(yes,den).denominator],
                   'no':[Fraction(no,den).numerator,Fraction(no,den).denominator],
                   'sourcefree_fixture_counts':{'yes':yes,'no':no,'denominator':den},
                   'sampling_unit':'SYNTHETIC_RESPONDENT_NOT_HOUSEHOLD_OR_DYAD'}
    return {'state':'TEST_ONLY_CONDITIONED','routes':routes,
            'route_probabilities':None,'empirical':possibility,
            'person_fact':None,'actor_calls':0,'model_calls':0,
            'native_owner_calls':0,'knowledge_as_of':world['as_of'],
            'epistemic_ceiling':'TEST_ONLY_MODELED_ACCESS_AND_FIXTURE_EMPIRICAL_COUNTS'}


def run():
    p = load_precommit()
    outcomes = []
    for pair in p['pairs']:
        original = pair['base']; altered = world_from(original,pair['contrast'])
        a,b = decide(original),decide(altered)
        keys=['routes','empirical','state']
        changes = {k: {'before':a.get(k), 'after':b.get(k)} for k in keys if a.get(k)!=b.get(k)}
        outcomes.append({'id':pair['id'],'observed_baseline':a,'observed_contrast':b,
                         'changed_fields':sorted(changes),'changes':changes,
                         'independent_pair_evidence':'EXECUTED_EST1_XSP_STANDALONE_SOURCEFREE_COUNTERFACTUAL_ONLY'})
    for control in p['negative_controls']:
        source = next(x for x in p['pairs'] if x['id']==control['base_pair'])
        a=decide(source['base']);b=decide(world_from(source['base'],control['contrast']))
        outcomes.append({'id':control['id'],'unchanged':a==b,'before_digest':digest(a),'after_digest':digest(b),
                         'no_person_fact':a.get('person_fact') is None and b.get('person_fact') is None})
    return {'schema':'PYAT_R18_XSP_PHYSICAL_SOURCEFREE_WORLD_PAIR_COURT@1',
            'precommit_sha256':FROZEN_SHA256,'verdict':'STANDALONE_TEST_ONLY_NOT_NATIVE_OWNER_EXECUTION',
            'outcomes':outcomes,'native_pyat_calls':0,'native_sorok_calls':0,
            'original_survey_reads':0,'actor_or_model_calls':0}


if __name__ == '__main__':
    import argparse
    cli=argparse.ArgumentParser();cli.add_argument('--out',required=True); args=cli.parse_args()
    data=run();Path(args.out).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print(data['verdict'],len(data['outcomes']))
