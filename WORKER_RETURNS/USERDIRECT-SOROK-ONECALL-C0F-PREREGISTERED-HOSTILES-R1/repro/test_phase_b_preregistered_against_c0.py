"""Independent post-freeze court against exact C0 imported Python source.

A01–A32 correspond one-to-one to the pre-C0 Git freeze, whose inputs and expected
authority outcomes are unchanged. We exercise C0's real public entrypoints,
not the frozen oracle's run() or its expected-result fields. Failing tests are
scientific RED, not regression-suite technical trouble or licensed actor effects.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import pytest
import onecall_c0 as c

ROOT=Path(__file__).resolve().parent
FROZEN=json.loads((ROOT/'frozen/01_FROZEN_HOSTILE_MATRIX.json').read_text())
assert [r['id'] for r in FROZEN['cases']]==[f'A{i:02}' for i in range(1,33)]


def make(case_id, **changes):
    # Independent fixture carrier for a single 2020 candidate, not the Phase-A
    # oracle or its expected statuses.
    base={'id':f'test_{case_id}','year':2020,'day':80,'action':'OBSERVED_NEUTRAL',
          'source_scope_refs':['SYNTHETIC_WORLD@1'],'prerequisites':[],
          'possible_relevance_domains':['material_opportunity']}
    base.update(changes)
    return base


def check_proposal(p):
    inp=c.render_input(c.initial_state(),2020)
    packet=c.mocked_artifacts(inp)[1]
    packet['candidates']=[p]
    return c.validate_packet(packet,inp)[1]


def d(): return {x['id']:x for x in c.run()['causal']['decisions']}


def test_A01_render_invention_untrusted_in_proposal():
    assert not check_proposal(make('A01',prerequisites=['render-only:teacher-nova']))

def test_A02_render_psyche_patch_must_be_refused_at_render_admission():
    inp=c.render_input(c.initial_state(),2020);r,_=c.mocked_artifacts(inp)
    r['durable_psyche_patch']={'resentment':99}
    assert c.validate_render(r,inp)['status']!='NONCAUSAL_VALIDATED'

def test_A03_future_proposed_fact_cannot_validate_as_retrospective():
    inp=c.render_input(c.initial_state(),2020);r,_=c.mocked_artifacts(inp)
    r['claimed_fact_refs'].append('observed:2020:later');assert c.validate_render(r,inp)['status']=='RENDER_CLAIM_REJECTED'

def test_A04_move_invalidates_later_older_school():
    assert d()['old_friend']['status']=='INVALIDATED_MATERIAL_REGION'

def test_A05_other_person_refusal():
    assert d()['peer_contact']['status']=='REFUSED_INDEPENDENT_COUNTERPART'

def test_A06_occurrence_is_not_exposure():
    assert d()['speech']['status']=='DEFERRED_NO_ACTOR_EXPOSURE' and c.run()['causal']['final_state']['actor']['actor_knowledge']==[]

def test_A07_no_actor_owner_must_not_admit_event():
    assert not check_proposal(make('A07',actor_owner=None))

def test_A08_event_time_dependency_in_three_opportunities():
    z=d();assert z['practice']['status']=='ADMITTED_TEST_ONLY' and z['move']['status']=='ADMITTED_TEST_ONLY' and z['project']['status']=='ADMITTED_TEST_ONLY'

def test_A09_practice_without_rule_cannot_manufacture_later_capacity():
    r=c.run(rules={'licensed_objective_actions':['PROJECT_TASK','FAMILY_MOVE','OBSERVED_NEUTRAL','NEW_CLUB']})
    decisions={x['id']:x['status'] for x in r['causal']['decisions']}
    assert decisions['practice']=='DEFERRED_MISSING_OWNER_RULE' and decisions['project']=='DEFERRED_MISSING_OBSERVED_PRACTICE'

def test_A10_no_event_count_or_forced_fallback():
    orig=c.fixed_candidates
    try:
        c.fixed_candidates=lambda _:[]
        r=c.run()
    finally:c.fixed_candidates=orig
    assert not r['causal']['decisions'] and not r['causal']['final_state']['events']

def test_A11_immutable_prior_event_id_must_not_repeat():
    state=c.initial_state();state['events'].append({'id':c.fact_id(2020,'practice'),'year':2020,'day':30,'action':'PRACTICE_OBSERVED'})
    r=c.run(initial=state)
    seen=[x['id'] for x in r['causal']['final_state']['events']]
    assert len(seen)==len(set(seen))

def test_A12_narrative_variation_no_material_hash_change():
    assert c.run(variant='default')['causal']==c.run(variant='different_literary_style')['causal']

def test_A13_scoring_failure_cannot_be_rescued_by_rng():
    assert not check_proposal(make('A13',score=-999,random_draw=.99))

def test_A14_cold_process_exact_replay():
    env=dict(os.environ);outs=[]
    for seed in ('137','2026'):
        env['PYTHONHASHSEED']=seed
        cp=subprocess.run([sys.executable,'-B',str(ROOT/'onecall_c0.py'),'--mode','ONE_CALL'],env=env,capture_output=True,text=True,check=True)
        outs.append(cp.stdout)
    assert outs[0]==outs[1]

def test_A15_surface_fact_not_committed_past():
    inp=c.render_input(c.initial_state(),2020);r,_=c.mocked_artifacts(inp)
    r['claimed_fact_refs']=['invented_subject_said_hello']
    assert c.validate_render(r,inp)['ungrounded_claims']==['invented_subject_said_hello']

def test_A16_subannual_next_ninety_days_horizon_refuses_day_120():
    # A direct C0 year packet cannot describe 90-day window. Grade as RED/HOLD
    # through a negative control: the day 120 proposal is not withheld.
    assert not check_proposal(make('A16',day=120,subannual_horizon_days=90))

def test_A17_missing_source_permission_refuses():
    assert not check_proposal(make('A17',source_permission='MISSING'))

def test_A18_forged_world_event_issuer_refuses():
    assert not check_proposal(make('A18',external_issuer='FORGED'))

def test_A19_explicit_CAN011_effect_field_refused():
    assert not check_proposal(make('A19',CAN011_UPDATE={'belief':'new'}))

def test_A20_valid_empty_no_proposals():
    old=c.fixed_candidates
    try:c.fixed_candidates=lambda _:[]; x=c.run()
    finally:c.fixed_candidates=old
    assert x['causal']['final_state']['current_year']==2022

def test_A21_witnessed_speech_not_inferred_belief():
    old=c.fixed_candidates
    try:
        c.fixed_candidates=lambda year: [c.candidate(year,40,'heard','SPEECH_EXPOSURE',speech_ref='speech:heard',listener_witness=True)] if year==2020 else []
        x=c.run()
    finally:c.fixed_candidates=old
    assert x['causal']['final_state']['actor']['actor_knowledge']==['speech:heard']
    assert x['causal']['final_state']['actor']['beliefs']=='UNISSUED'

def test_A22_future_invented_person_no_constructor_refused():
    assert not check_proposal(make('A22',action='TEACHER_MEETING',prerequisites=['unknown:mentor']))

def test_A23_already_elapsed_within_year_cannot_backdate():
    state=c.initial_state();state['events'].append({'id':'observed:2020:midyear','year':2020,'day':200,'action':'FAMILY_MOVE'})
    x=c.run(initial=state)
    assert not any(v['id']==c.fact_id(2020,'practice') for v in x['causal']['final_state']['events'])

def test_A24_multiple_events_revalidate_after_material_move():
    assert d()['old_friend']['invalidated_by']=='move' and d()['project']['status']=='ADMITTED_TEST_ONLY'

def test_A25_independent_other_cannot_be_compelled():
    assert d()['peer_contact']['status']=='REFUSED_INDEPENDENT_COUNTERPART'

def test_A26_missing_scientific_rule_cannot_admit():
    assert not check_proposal(make('A26',rule='MISSING'))

def test_A27_foreign_event_owner_cannot_self_issue():
    assert not check_proposal(make('A27',actor_owner='LLM_ASSERTED'))

def test_A28_same_day_independent_events_stable_order():
    old=c.fixed_candidates
    try:
        c.fixed_candidates=lambda year: [c.candidate(year,80,'b','OBSERVED_NEUTRAL'),c.candidate(year,80,'a','OBSERVED_NEUTRAL')] if year==2020 else []
        x=c.run()
    finally:c.fixed_candidates=old
    assert [y['id'] for y in x['causal']['decisions']]==['a','b']

def test_A29_two_call_separate_typed_outputs_and_cost_counter():
    x=c.mode_comparison();assert x['physical_mock_invocations']=={'ONE_CALL':3,'TWO_CALL':4,'FIXED_PACKET':0} and x['causal_equal']

def test_A30_fixed_packet_no_external_LLM():
    assert c.run('FIXED_PACKET')['mock_physical_invocations']==0

def test_A31_genesis_prior_interval_cannot_invent_facts():
    inp=c.render_input(c.initial_state(),2020);r,_=c.mocked_artifacts(inp)
    r['claimed_fact_refs']=['imaginary_2019'];assert c.validate_render(r,inp)['status']=='RENDER_CLAIM_REJECTED'

def test_A32_demographics_not_imposed_as_mental_state():
    a=c.initial_state();b=c.initial_state();b['actor']['demographics']='OTHER_COHORT'
    ra,rb=c.run(initial=a),c.run(initial=b)
    assert ra['causal']['final_state']['actor']['beliefs']==rb['causal']['final_state']['actor']['beliefs']=='UNISSUED'
