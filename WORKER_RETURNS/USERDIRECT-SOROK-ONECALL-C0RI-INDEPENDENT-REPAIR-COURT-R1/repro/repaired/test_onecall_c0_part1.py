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


def test_R01_render_only_teacher_not_created(result):
    assert by_rejection(result)['invented_teacher']['reason'] == 'NARRATIVE_INVENTION_IS_NOT_A_PREREQUISITE'
    assert not by_id(result, 'invented_teacher')
    assert all(e['action'] != 'TEACHER_MEETING' for e in result['causal']['final_state']['events'])


def test_R02_render_only_betrayal_no_resenment_or_memory(result):
    assert by_rejection(result)['invented_betrayal']['reason'] == 'UNISSUED_PSYCHOLOGICAL_EFFECT'
    state = result['causal']['final_state']['actor']
    assert state['beliefs'] == state['affect'] == 'UNISSUED'
    assert 'render-only:betrayal' not in oc.canonical(result['causal'])


def test_R03_different_render_only_has_same_causal_receipt():
    a, b = oc.run(variant='default'), oc.run(variant='different_literary_style')
    assert a['causal'] == b['causal']
    assert a['boundaries'][1]['render']['narrative_text'] != b['boundaries'][1]['render']['narrative_text']


def test_R04_move_invalidates_friend_in_old_place(result):
    d = decisions(result)
    assert d['move']['status'] == 'ADMITTED_TEST_ONLY'
    assert d['old_friend']['status'] == 'INVALIDATED_MATERIAL_REGION'
    assert d['old_friend']['invalidated_by'] == 'move'
    assert not by_id(result, 'old_friend')
    assert result['causal']['final_state']['world']['region'] == 'new_town'


def test_R05_practice_effect_requires_named_test_owner():
    a = oc.run()
    b = oc.run(rules={'licensed_objective_actions': ['FAMILY_MOVE','PROJECT_TASK','OBSERVED_NEUTRAL','NEW_CLUB']})
    assert decisions(a)['practice']['status'] == 'ADMITTED_TEST_ONLY'
    assert decisions(a)['project']['status'] == 'ADMITTED_TEST_ONLY'
    assert decisions(b)['practice']['status'] == 'DEFERRED_MISSING_OWNER_RULE'
    assert decisions(b)['project']['status'] == 'DEFERRED_MISSING_OBSERVED_PRACTICE'
    assert b['causal']['final_state']['actor']['practiced_tasks'] == 0


def test_R06_empty_interval_is_valid_no_fallback():
    original = oc.fixed_candidates
    try:
        oc.fixed_candidates = lambda _: []
        r = oc.run()
    finally:
        oc.fixed_candidates = original
    assert not r['causal']['final_state']['events']
    assert not r['causal']['decisions']
    assert len(r['causal']['final_state']['slow_ticks']) == 2
    assert r['causal']['final_state']['current_year'] == 2022


def test_R07_separate_parent_histories_not_self_issued_psychology():
    x = oc.initial_state(); y = oc.initial_state()
    x['counterparts']['peer']['independent_history'] = ['rehearsal_reserved']
    y['counterparts']['peer']['independent_history'] = ['rehearsal_cancelled']
    a, b = oc.run(initial=x), oc.run(initial=y)
    assert a['causal']['final_state']['counterparts'] != b['causal']['final_state']['counterparts']
    assert a['causal']['final_state']['actor']['affect'] == b['causal']['final_state']['actor']['affect'] == 'UNISSUED'
    # Full differentiated psychology explicitly NOT tested/issued here.


def test_R08_cosmetic_relevance_label_not_owner_psyche():
    a, b = oc.initial_state(), oc.initial_state()
    p = oc.candidate(2020, 30, 'a', 'OBSERVED_NEUTRAL', domains=['recognized_plan'])
    q = oc.candidate(2020, 30, 'a', 'OBSERVED_NEUTRAL', domains=['unrecognized_plan'])
    rules = {'licensed_objective_actions':['OBSERVED_NEUTRAL']}
    oc.apply_admitted(a, p, 2020, rules)
    oc.apply_admitted(b, q, 2020, rules)
    assert a['actor'] == b['actor']
    assert a['events'][0]['hash'] != b['events'][0]['hash']  # audit label differences remain visible

