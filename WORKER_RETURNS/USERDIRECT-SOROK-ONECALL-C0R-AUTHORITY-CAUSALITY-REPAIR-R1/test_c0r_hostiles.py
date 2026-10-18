"""C0R author RED repair probes derived from exact C0F test specifications.
Not a claim that these are byte-identical immutable C0F test files.
"""
import copy, subprocess, sys, hashlib, json, os
from pathlib import Path
import pytest
import onecall_c0 as c

ROOT=Path(__file__).resolve().parent

def input_packet(year=2020):
    i=c.render_input(c.initial_state(),year)
    return i,c.mocked_artifacts(i)[1]

def raw(code, **changes):
    p=dict(id=code,year=2020,day=80,action='OBSERVED_NEUTRAL',
           source_scope_refs=[c.SOURCE],prerequisites=[],possible_relevance_domains=['material_opportunity'])
    p.update(changes);return p

def valid(p):
    i,pkt=input_packet();pkt['candidates']=[p];return c.validate_packet(pkt,i)[1]

def decisions(x):return {d['id']:d for d in x['causal']['decisions']}

def test_A01_render_only_invention_refused():assert not valid(raw('A01',prerequisites=['render-only:teacher-nova']))

def test_A02_unknown_render_psyche_refused():
    i,p=input_packet();r,_=c.mocked_artifacts(i);r['durable_psyche_patch']={'resentment':99}
    assert c.validate_render(r,i)['status']!='NONCAUSAL_VALIDATED'

def test_A03_future_proposed_not_retrospective():
    i,p=input_packet();r,_=c.mocked_artifacts(i);r['claimed_fact_refs'].append('observed:2020:later')
    assert c.validate_render(r,i)['status']=='RENDER_CLAIM_REJECTED'

def test_A04_material_move_refuses():assert decisions(c.run())['old_friend']['status']=='INVALIDATED_MATERIAL_REGION'

def test_A05_independent_other_refusal():assert decisions(c.run())['peer_contact']['status']=='REFUSED_INDEPENDENT_COUNTERPART'

def test_A06_speech_without_exposure():
    r=c.run();assert decisions(r)['speech']['status']=='DEFERRED_NO_ACTOR_EXPOSURE'
    assert r['causal']['final_state']['actor']['actor_knowledge']==[]

def test_A07_missing_actor_owner():assert not valid(raw('A07',actor_owner=None))

def test_A08_three_admitted_opportunities():
    d=decisions(c.run());assert all(d[x]['status']=='ADMITTED_TEST_ONLY' for x in ('practice','move','project'))

def test_A09_without_practice_owner():
    r=c.run(rules={'licensed_objective_actions':['PROJECT_TASK','FAMILY_MOVE','OBSERVED_NEUTRAL','NEW_CLUB']})
    d=decisions(r);assert d['practice']['status']=='DEFERRED_MISSING_OWNER_RULE'
    assert d['project']['status']=='DEFERRED_MISSING_OBSERVED_PRACTICE'

def test_A10_no_candidates_no_fallback(monkeypatch):
    monkeypatch.setattr(c,'fixed_candidates',lambda _:[]);r=c.run()
    assert not r['causal']['decisions'] and not r['causal']['final_state']['events']

def test_A11_duplicate_existing_id():
    s=c.initial_state();s['events'].append(dict(id=c.fact_id(2020,'practice'),year=2020,day=30,action='PRACTICE_OBSERVED'))
    r=c.run(initial=s);ident=[e['id'] for e in r['causal']['final_state']['events']]
    assert len(ident)==len(set(ident))

def test_A12_render_text_causally_invariant():
    assert c.run()['causal']==c.run(variant='different_literary_style')['causal']

def test_A13_score_refusal():assert not valid(raw('A13',score=-999,random_draw=.99))

def test_A14_cold_output():
    outputs=[]
    for seed in ('137','2026'):
        env=dict(os.environ);env['PYTHONHASHSEED']=seed
        r=subprocess.run([sys.executable,'-B',str(ROOT/'onecall_c0.py')],cwd=ROOT,env=env,capture_output=True,text=True,check=True)
        outputs.append(r.stdout)
    assert outputs[0]==outputs[1]

def test_A15_surface_fact_not_committed():
    i,p=input_packet();r,_=c.mocked_artifacts(i);r['claimed_fact_refs']=['invented_subject_said_hello']
    assert c.validate_render(r,i)['ungrounded_claims']==['invented_subject_said_hello']

def test_A16_unsupported_ninety_days():assert not valid(raw('A16',day=120,subannual_horizon_days=90))

def test_A17_missing_source_permission():assert not valid(raw('A17',source_permission='MISSING'))

def test_A18_external_forged_issuer():assert not valid(raw('A18',external_issuer='FORGED'))

def test_A19_psyche_write_refused():assert not valid(raw('A19',CAN011_UPDATE={'belief':'new'}))

def test_A20_valid_empty_year(monkeypatch):
    monkeypatch.setattr(c,'fixed_candidates',lambda _:[]);x=c.run();assert x['causal']['final_state']['current_year']==2022

def test_A21_witnessed_speech_not_belief(monkeypatch):
    monkeypatch.setattr(c,'fixed_candidates',lambda y:[c.candidate(y,40,'heard','SPEECH_EXPOSURE',speech_ref='speech:heard',listener_witness=True)] if y==2020 else [])
    x=c.run();assert x['causal']['final_state']['actor']['actor_knowledge']==['speech:heard']
    assert x['causal']['final_state']['actor']['beliefs']=='UNISSUED'

def test_A22_unauthorized_new_entity():assert not valid(raw('A22',action='TEACHER_MEETING',prerequisites=['unknown:mentor']))

def test_A23_midyear_backdating_rejected():
    s=c.initial_state();s['events'].append(dict(id='observed:2020:midyear',year=2020,day=200,action='FAMILY_MOVE'))
    x=c.run(initial=s);assert not any(v['id']==c.fact_id(2020,'practice') for v in x['causal']['final_state']['events'])

def test_A24_move_is_exact_invalidator():
    d=decisions(c.run());assert d['old_friend']['invalidated_by']=='move' and d['project']['status']=='ADMITTED_TEST_ONLY'

def test_A25_other_not_compelled():assert decisions(c.run())['peer_contact']['status']=='REFUSED_INDEPENDENT_COUNTERPART'

def test_A26_missing_rule():assert not valid(raw('A26',rule='MISSING'))

def test_A27_actor_owner_unissued():assert not valid(raw('A27',actor_owner='LLM_ASSERTED'))

def test_A28_stable_same_day(monkeypatch):
    monkeypatch.setattr(c,'fixed_candidates',lambda y:[c.candidate(y,80,'b','OBSERVED_NEUTRAL'),c.candidate(y,80,'a','OBSERVED_NEUTRAL')] if y==2020 else [])
    assert [x['id'] for x in c.run()['causal']['decisions']]==['a','b']

def test_A29_three_arms_counts():
    x=c.mode_comparison();assert x['physical_mock_invocations']=={'ONE_CALL':3,'TWO_CALL':4,'FIXED_PACKET':0} and x['causal_equal']

def test_A30_fixed_zero_calls():assert c.run('FIXED_PACKET')['mock_physical_invocations']==0

def test_A31_no_genesis_facts():
    i,p=input_packet();r,_=c.mocked_artifacts(i);r['claimed_fact_refs']=['imaginary_2019']
    assert c.validate_render(r,i)['status']=='RENDER_CLAIM_REJECTED'

def test_A32_no_demographic_psyche():
    a=c.initial_state();b=c.initial_state();b['actor']['demographics']='OTHER_COHORT'
    assert c.run(initial=a)['causal']['final_state']['actor']['beliefs']==c.run(initial=b)['causal']['final_state']['actor']['beliefs']=='UNISSUED'

def test_R32_empty_dict_must_be_zero_licensed():assert c.run(rules={})['causal']['final_state']['events']==[]

def test_R33_other_person_ref_exact():
    s=c.initial_state();s['counterparts']['peer']['available']=True
    p=c.candidate(2020,35,'meet_stranger','COUNTERPART_CONTACT',counterpart='unconstructed_stranger')
    assert c.evaluate(s,p,{'licensed_objective_actions':['COUNTERPART_CONTACT']})!='ELIGIBLE_TEST_ONLY'

def test_R34_unconstructed_teacher():
    i,pkt=input_packet();pkt['candidates']=[c.candidate(2020,75,'unknown','TEACHER_MEETING',participants=['child','never_constructed_teacher'])]
    assert not c.validate_packet(pkt,i)[1]

def test_R35_relevance_label_hash_separation(monkeypatch):
    orig=c.fixed_candidates
    def variant(domain):
        def chooser(y):
            res=orig(y)
            if y==2020:
                for q in res:
                    if q['id']=='routine':q['possible_relevance_domains']=[domain]
            return res
        monkeypatch.setattr(c,'fixed_candidates',chooser)
        v=c.run();monkeypatch.setattr(c,'fixed_candidates',orig);return v
    a,b=variant('recognized_plan'),variant('unrecognized_plan')
    assert a['causal']['canonical_history_hash']==b['causal']['canonical_history_hash']
    assert a['proposal_audit_hash']!=b['proposal_audit_hash']

def test_R36_parent_proposal_retained():
    i,pkt=input_packet();pkt['candidates']=[c.candidate(2020,30,'practice','PRACTICE_OBSERVED'),
        c.candidate(2020,100,'skill_use','PROJECT_TASK',min_practice=1,prerequisites=[c.fact_id(2020,'practice')])]
    assert [p['id'] for p in c.validate_packet(pkt,i)[1]]==['practice','skill_use']

def test_R37_optimized_python_same_deny():
    body="""import onecall_c0 as c
s=c.initial_state();i=c.render_input(s,2020);r,p=c.mocked_artifacts(i)
p['source_scope_refs']=['UNISSUED_ORIGINAL35']
try:c.validate_packet(p,i);print('FAIL_OPEN')
except (AssertionError,PermissionError,ValueError):print('REFUSED')
"""
    outs=[]
    for flag in ('','-O'):
        args=[sys.executable]+([flag] if flag else [])+['-c',body]
        outs.append(subprocess.run(args,cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip())
    assert outs==['REFUSED','REFUSED']

def test_R38_unissued_render_memory():
    i,p=input_packet();r,_=c.mocked_artifacts(i);r['actor_private_memory_access']={'foreign_person':'secret'}
    assert c.validate_render(r,i)['status']!='NONCAUSAL_VALIDATED'

def test_R39_forged_model_sampling():
    i,p=input_packet();p['model_version']='GROUNDED_PROVIDER_LIVE_NO_AUTHORITY'
    p['sampling_metadata']={'rng_stream':'FORGED','seed':1,'random_draws':99,'probability_grade':'TRUE'}
    assert not c.validate_packet(p,i)[1]

def test_R40_render_prose_change_no_state():assert c.run()['causal']==c.run(variant='different_literary_style')['causal']

def test_R41_rule_restricts_observed_practice():
    x=c.run(rules={'licensed_objective_actions':['OBSERVED_NEUTRAL']})
    assert x['causal']['final_state']['actor']['practiced_tasks']==0

def test_R42_is_original_only_not_repair_identity():
    # This is a positive REPAIRED identity test, NOT frozen original R42.
    b=Path(c.__file__).read_bytes()
    assert hashlib.sha256(b).hexdigest()==hashlib.sha256((ROOT/'onecall_c0.py').read_bytes()).hexdigest()
    assert hashlib.sha256(b).hexdigest()!='3f0da92095f8355c7512d49ac546c846b6026d3775533ba56be7e148e11abfa1'

def test_R43_mode_counts_and_disclaimer():
    x=c.mode_comparison()
    assert x['physical_mock_invocations']=={'ONE_CALL':3,'TWO_CALL':4,'FIXED_PACKET':0}
    assert 'NO_REAL_LLM' in x['disclaimer']

# Additional mutation cases, not part of historical A/R suites.

def test_M01_source_replacement_after_validation_denied():
    i,pkt=input_packet();pkt['candidates']=[c.candidate(2020,80,'x','OBSERVED_NEUTRAL')]
    p=c.validate_packet(pkt,i)[1][0];s=c.initial_state();s['world']['source_ref']='FOREIGN_REPLACEMENT'
    assert c.evaluate(s,p,{'licensed_objective_actions':['OBSERVED_NEUTRAL']})=='DEFERRED_SOURCE_CURRENTNESS_MISMATCH'
    before=copy.deepcopy(s)
    with pytest.raises(AssertionError):c.apply_admitted(s,p,2020,{'licensed_objective_actions':['OBSERVED_NEUTRAL']})
    assert s==before

def test_M02_parent_denied_then_child_not_admitted(monkeypatch):
    monkeypatch.setattr(c,'fixed_candidates',lambda y:[c.candidate(y,30,'practice','PRACTICE_OBSERVED'),
       c.candidate(y,100,'skill_use','PROJECT_TASK',min_practice=1,prerequisites=[c.fact_id(2020,'practice')])] if y==2020 else [])
    r=c.run(rules={'licensed_objective_actions':['PROJECT_TASK']});d=decisions(r)
    assert d['practice']['status']=='DEFERRED_MISSING_OWNER_RULE'
    assert d['skill_use']['status']=='PENDING_PARENT_NOT_ADMITTED'

def test_M03_parent_admitted_child_causal_dependency(monkeypatch):
    monkeypatch.setattr(c,'fixed_candidates',lambda y:[c.candidate(y,30,'practice','PRACTICE_OBSERVED'),
       c.candidate(y,100,'skill_use','PROJECT_TASK',min_practice=1,prerequisites=[c.fact_id(2020,'practice')])] if y==2020 else [])
    d=decisions(c.run());assert d['practice']['status']==d['skill_use']['status']=='ADMITTED_TEST_ONLY'

def test_M04_parent_cycle_fail_closed():
    i,pkt=input_packet();pkt['candidates']=[c.candidate(2020,100,'a','OBSERVED_NEUTRAL',prerequisites=[c.fact_id(2020,'b')]),
      c.candidate(2020,90,'b','OBSERVED_NEUTRAL',prerequisites=[c.fact_id(2020,'a')])]
    assert not c.validate_packet(pkt,i)[1]

def test_M05_forged_render_knowledge_no_effect():
    i,pkt=input_packet();r,_=c.mocked_artifacts(i)
    r['actor_private_memory_access']={'child':'false_memory'}
    assert c.validate_render(r,i)['status']=='RENDER_SCHEMA_REFUSED'
    assert c.initial_state()['actor']['actor_knowledge']==[]

def test_M06_no_proposals_denied_fallback(monkeypatch):
    monkeypatch.setattr(c,'fixed_candidates',lambda y:[c.candidate(y,30,'bad','OBSERVED_NEUTRAL',source_permission='FORGED')] if y==2020 else [])
    r=c.run();assert not r['causal']['final_state']['events']

def test_M07_stale_existing_event_do_not_replace():
    s=c.initial_state();s['events']=[{'id':c.fact_id(2020,'practice'),'year':2020,'day':30,'action':'FORGED_OLD'}]
    r=c.run(initial=s)
    assert r['causal']['final_state']['events'][0]['action']=='FORGED_OLD'
    assert sum(e['id']==c.fact_id(2020,'practice') for e in r['causal']['final_state']['events'])==1

def test_M08_missing_horizon_fail_closed():
    p=c.candidate(2020,120,'x','OBSERVED_NEUTRAL',subannual_horizon_days=90)
    assert not valid(p)

def test_M09_independent_other_grant_not_label():
    s=c.initial_state();s['counterparts']['peer']['available']=True
    p=c.candidate(2020,250,'noone','COUNTERPART_CONTACT',counterpart='phantom')
    assert c.evaluate(s,p,{'licensed_objective_actions':['COUNTERPART_CONTACT']})=='REFUSED_UNCONSTRUCTED_COUNTERPART'

def test_M10_refusal_optimized_external_issuer():
    snippet="""import onecall_c0 as c
s=c.initial_state();i=c.render_input(s,2020);r,p=c.mocked_artifacts(i)
p['candidates'][0]['objective_owner']='FAKE_OWNER'
print(len(c.validate_packet(p,i)[1]) == len(p['candidates']))
"""
    for opt in ([],['-O']):
        x=subprocess.run([sys.executable,*opt,'-c',snippet],cwd=ROOT,text=True,capture_output=True,check=True)
        assert x.stdout.strip()=='False'
