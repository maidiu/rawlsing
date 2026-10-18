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


def test_EXTRA_adaptive_update_legal_vs_position_unknown():
    p=oc.candidate(2020,180,'old_friend','FRIEND_MEETING',required_region='old_town')
    s=oc.initial_state();r={'licensed_objective_actions':['FRIEND_MEETING']}
    assert oc.evaluate(s,p,r)=='ELIGIBLE_TEST_ONLY'
    s['world']['region']='new_town'
    assert oc.evaluate(s,p,r)=='INVALIDATED_MATERIAL_REGION'


def test_EXTRA_no_laundering_back_to_checkpoint(result):
    a=result['boundaries'][1]
    assert a['render']['causal_hash_before']==a['checkpoint_ref']
    assert not any('teacher-nova' in e['id'] or 'betrayal' in e['id']
                   for e in result['causal']['final_state']['events'])
    assert len(result['causal']['final_state']['events'])==6


def test_EXTRA_hidden_future_ignored_by_render():
    inp=oc.render_input(oc.initial_state(),2020)
    render,_=oc.mocked_artifacts(inp)
    render['allowed_fact_refs']=['future:forged']
    with pytest.raises(AssertionError,match='render fact grant forged'):
        oc.validate_render(render,inp)


def test_EXTRA_no_time_retroaction(result):
    records=result['causal']['final_state']['events']
    assert [(r['year'],r['day']) for r in records]==sorted((r['year'],r['day']) for r in records)
    assert all(r['prior_state_hash'] != r['hash'] for r in records)


def test_EXTRA_no_forced_duplicate_or_replacement(result):
    planned=sum(len(oc.fixed_candidates(y)) for y in (2020,2021))
    actual=len(result['causal']['final_state']['events'])
    assert actual < planned
    assert not any(d['id'].endswith('fallback') for d in result['causal']['decisions'])


def test_EXTRA_unauthorized_owner_all_events_defer():
    s=oc.run(rules={'licensed_objective_actions':[]})
    assert not s['causal']['final_state']['events']
    assert all(d['status']!='ADMITTED_TEST_ONLY' for d in s['causal']['decisions'])
    assert s['causal']['final_state']['actor']['practiced_tasks']==0


def test_EXTRA_actor_view_no_render_into_state(result):
    body=oc.canonical(result['causal']['final_state'])
    assert 'teacher-nova' not in body and 'future_unoccurred' not in body
    assert 'text_or_scene_fragments' not in body


def test_EXTRA_proposals_are_audited_independent(result):
    assert all(b['prospective_validation']['proposal_checkpoint']==b['checkpoint_ref'] for b in result['boundaries'])
    assert all(b['render']['causal_hash_before']==b['checkpoint_ref'] for b in result['boundaries'])
    assert result['experiment_grade']==oc.GRADE
