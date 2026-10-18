"""ONECALL-C0 R01–R17: TEST_ONLY real executable sourcefree adversaries.

PASS here means only the named boundary against the authored mock, NOT
native Sorok F1/B3 psychological science or independent I2 acceptance.
"""
from copy import deepcopy
import subprocess
import sys
from pathlib import Path

import pytest
import onecall_c0 as oc


@pytest.fixture(scope='module')
def result():
    return oc.run()


def decisions(r):
    return {d['id']: d for d in r['causal']['decisions']}


def by_id(r, cid):
    return [x for x in r['causal']['final_state']['events'] if x['id'].endswith(':'+cid)]


def by_rejection(r):
    return {x['id']:x for x in r['causal']['proposal_rejections']}


def test_R09_history_not_demographics_changes_practical_possibility():
    a, b = oc.initial_state(), oc.initial_state()
    b['actor']['practiced_tasks'] = 1
    p = oc.candidate(2020, 100, 'project', 'PROJECT_TASK', min_practice=1)
    r = {'licensed_objective_actions':['PROJECT_TASK']}
    assert a['actor']['demographics'] == b['actor']['demographics']
    assert oc.evaluate(a,p,r) == 'DEFERRED_MISSING_OBSERVED_PRACTICE'
    assert oc.evaluate(b,p,r) == 'ELIGIBLE_TEST_ONLY'
    assert a['actor']['beliefs'] == b['actor']['beliefs'] == 'UNISSUED'


def test_R10_speech_without_exposure_not_known(result):
    assert decisions(result)['speech']['status'] == 'DEFERRED_NO_ACTOR_EXPOSURE'
    assert result['causal']['final_state']['actor']['actor_knowledge'] == []
    assert not by_id(result, 'speech')


def test_R11_independent_counterpart_refusal(result):
    assert decisions(result)['peer_contact']['status'] == 'REFUSED_INDEPENDENT_COUNTERPART'
    assert not by_id(result, 'peer_contact')
    s = oc.initial_state()
    s['counterparts']['peer']['available'] = True
    p = oc.candidate(2020, 250, 'peer_contact', 'COUNTERPART_CONTACT', counterpart='peer')
    assert oc.evaluate(s,p,{'licensed_objective_actions':['COUNTERPART_CONTACT']}) == 'ELIGIBLE_TEST_ONLY'


def test_R12_observed_practice_does_not_erase_conflicting_appraisal(result):
    x = oc.initial_state()
    x['actor']['beliefs'] = 'TEST_ONLY_SELF_REPORT_CONTRADICTS_PRACTICE'
    a = oc.run(initial=x)
    assert a['causal']['final_state']['actor']['practiced_tasks'] == 1
    assert a['causal']['final_state']['actor']['beliefs'] == 'TEST_ONLY_SELF_REPORT_CONTRADICTS_PRACTICE'
    assert all(d.get('psyche_effect_status') == 'VALID_EMPTY__NO_CAN008_CAN011_ADP016_RULE'
               for d in a['causal']['decisions'] if d['status'] == 'ADMITTED_TEST_ONLY')


def test_R13_render_future_proposal_not_backdated(result):
    r = result['boundaries'][1]['render']
    assert oc.fact_id(2021, 'future_unoccurred') in r['future_claims_rejected']
    assert not any(e['id'] == oc.fact_id(2021,'future_unoccurred')
                   for e in result['causal']['final_state']['events'])
    assert all(e['year'] in (2020,2021) for e in result['causal']['final_state']['events'])


def test_R14_source_scope_mismatch_refuses():
    s = oc.initial_state(); inp = oc.render_input(s, 2020)
    r,p = oc.mocked_artifacts(inp)
    p['source_scope_refs'] = ['UNISSUED_ORIGINAL35']
    with pytest.raises(AssertionError,match='source mismatch'):
        oc.validate_packet(p,inp)


def test_R14_unknown_position_refuses():
    inp = oc.render_input(oc.initial_state(), 2020)
    _,p = oc.mocked_artifacts(inp)
    inp['position_ref'] = None
    with pytest.raises(AssertionError,match='position unbound'):
        oc.validate_packet(p,inp)


def test_R14_no_individual_probabilities_created(result):
    assert result['boundaries'][0]['prospective_validation']['no_personal_probability']
    assert 'route_probability' not in oc.canonical(result['causal'])
    assert all(x['sampling_metadata']['probability_grade'] == 'NONE'
               for x in [oc.mocked_artifacts(oc.render_input(oc.initial_state(),2020))[1]])

