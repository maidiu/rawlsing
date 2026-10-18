"""Additional independent NEW hostiles; distinct from preregistered A01--A32.

Run on exact Git SHA imported C0, not its author tests. Failures are scientific
RED/limitation findings; these controls NEVER authorize production use.
"""
import copy
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import json
import pytest
import onecall_c0 as c

ROOT=Path(__file__).resolve().parent

def test_R32_empty_rules_object_should_mean_no_issued_owner_actions():
    x=c.run(rules={})
    assert x['causal']['final_state']['events']==[]


def test_R33_other_person_id_matters_even_when_peer_is_available():
    s=c.initial_state();s['counterparts']['peer']['available']=True
    p=c.candidate(2020,35,'meet_stranger','COUNTERPART_CONTACT',counterpart='unconstructed_stranger')
    r={'licensed_objective_actions':['COUNTERPART_CONTACT']}
    assert c.evaluate(s,p,r)!='ELIGIBLE_TEST_ONLY'


def test_R34_unconstructed_new_actor_without_prerequisites_refused():
    s=c.initial_state();inp=c.render_input(s,2020)
    pkt=c.mocked_artifacts(inp)[1]
    pkt['candidates']=[c.candidate(2020,75,'meet_labeled_unborn_teacher','TEACHER_MEETING',
                                   participants=['child','never_constructed_teacher'])]
    _,valid=c.validate_packet(pkt,inp)
    assert not valid


def test_R35_relevance_only_label_cannot_change_canonical_causal_history():
    def variant(domain):
        original=c.fixed_candidates
        try:
            def chooser(y):
                result=original(y)
                if y==2020:
                    for q in result:
                        if q['id']=='routine':q['possible_relevance_domains']=[domain]
                return result
            c.fixed_candidates=chooser
            return c.run()
        finally:c.fixed_candidates=original
    a,b=variant('recognized_plan'),variant('unrecognized_plan')
    assert a['causal']['final_state']['world']==b['causal']['final_state']['world']
    assert a['causal']['final_state']['actor']==b['causal']['final_state']['actor']
    assert a['causal']['canonical_history_hash']==b['causal']['canonical_history_hash']


def test_R36_intra_year_parent_proposal_retained_until_prerequisite_committed():
    s=c.initial_state();inp=c.render_input(s,2020)
    packet=c.mocked_artifacts(inp)[1]
    packet['candidates']=[c.candidate(2020,30,'practice','PRACTICE_OBSERVED'),
                          c.candidate(2020,100,'skill_use','PROJECT_TASK',
                          min_practice=1,prerequisites=[c.fact_id(2020,'practice')])]
    _,valid=c.validate_packet(packet,inp)
    assert [q['id'] for q in valid]==['practice','skill_use']


def test_R37_python_optimized_runtime_must_not_disable_permission_checks():
    payload='''import onecall_c0 as c
s=c.initial_state();i=c.render_input(s,2020)
r,p=c.mocked_artifacts(i)
p['source_scope_refs']=['UNISSUED_ORIGINAL35']
try:
 c.validate_packet(p,i)
 print('FAIL_OPEN')
except (AssertionError,PermissionError,ValueError):
 print('REFUSED')
'''
    optimized=subprocess.run([sys.executable,'-O','-c',payload],cwd=ROOT,capture_output=True,text=True,check=True)
    ordinary=subprocess.run([sys.executable,'-c',payload],cwd=ROOT,capture_output=True,text=True,check=True)
    assert ordinary.stdout.strip()=='REFUSED'
    assert optimized.stdout.strip()=='REFUSED'


def test_R38_render_unchecked_unissued_actor_access_patch_must_refuse():
    inp=c.render_input(c.initial_state(),2020);rend,_=c.mocked_artifacts(inp)
    rend['actor_private_memory_access']={'foreign_person':'secret'}
    assert c.validate_render(rend,inp)['status']!='NONCAUSAL_VALIDATED'


def test_R39_asserted_unauthorized_provenance_is_not_independently_certified():
    inp=c.render_input(c.initial_state(),2020)
    _,pkt=c.mocked_artifacts(inp)
    pkt['model_version']='GROUNDED_PROVIDER_LIVE_NO_AUTHORITY'
    pkt['sampling_metadata']={'rng_stream':'FORGED','seed':1,'random_draws':99,'probability_grade':'TRUE'}
    _,valid=c.validate_packet(pkt,inp)
    assert not valid


def test_R40_render_prose_can_change_but_actor_state_not():
    assert c.run(variant='default')['causal']==c.run(variant='different_literary_style')['causal']


def test_R41_unqualified_rule_forbids_observed_practice_update():
    r=c.run(rules={'licensed_objective_actions':['OBSERVED_NEUTRAL']})
    assert not r['causal']['final_state']['events'] or all(e['action']=='OBSERVED_NEUTRAL' for e in r['causal']['final_state']['events'])
    assert r['causal']['final_state']['actor']['practiced_tasks']==0


def test_R42_real_author_source_file_hash_and_runtime_import_path():
    b=Path(c.__file__).resolve().read_bytes()
    assert Path(c.__file__).resolve()==ROOT/'onecall_c0.py'
    assert len(b)==18378
    assert hashlib.sha256(b).hexdigest()=='3f0da92095f8355c7512d49ac546c846b6026d3775533ba56be7e148e11abfa1'
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()=='f45e4f5573495f060503f92b7630ec83531ced4d'


def test_R43_mock_invocation_count_is_only_mock_not_actual_provider_token_cost():
    x=c.mode_comparison()
    assert x['physical_mock_invocations']=={'ONE_CALL':3,'TWO_CALL':4,'FIXED_PACKET':0}
    assert 'NO_REAL_LLM' in x['disclaimer']
