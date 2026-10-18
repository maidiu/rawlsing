"""Independent postfreeze source-free probes of exact C0R imported Git blob.
No edits to original C0, repaired C0R, C0RI frozen expectations, or authors' tests.
"""
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import pytest
import onecall_c0 as c


def test_I01_exact_repaired_module_sha_and_git_identity():
    b=Path(c.__file__).read_bytes()
    assert len(b)==29383
    assert hashlib.sha256(b).hexdigest()=='298ff2bdbf4f916049ae21167e238767d2da682f369820a29c7d5ffa1a5461f9'
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()=='76bd3a6ea26fd72ef59816d62013fd694bf8e774'


def test_I02_two_genuine_cold_interpreters_reproduce_byte_exact_output():
    data=[]
    for seed in ('17','791'):
        cp=subprocess.run([sys.executable,'-B',str(Path(c.__file__).resolve()),'--out',str(Path(__file__).parent/('i2_cold_'+seed+'.json'))],env={**os.environ,'PYTHONHASHSEED':seed},stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,check=True)
        data.append((Path(__file__).parent/('i2_cold_'+seed+'.json')).read_bytes())
    assert data[0]==data[1]
    assert hashlib.sha256(data[0]).hexdigest()=='1949122dd8761e9c742477b502f6a73b82dd98670408361b5002473b5581dbdf'


def test_I03_empty_owner_rules_allow_no_committed_occurrences():
    assert c.run(rules={})['causal']['final_state']['events']==[]


def test_I04_python_optimized_does_not_bypass_grant():
    script='''import onecall_c0 as c
state=c.initial_state(); inp=c.render_input(state,2020)
r,p=c.mocked_artifacts(inp); p['source_scope_refs']=['FORGED']
try: c.validate_packet(p,inp); print('FAIL_OPEN')
except (AssertionError,ValueError,PermissionError): print('DENIED')
'''
    outputs=[]
    for flag in ([],['-O']):
        cp=subprocess.run([sys.executable,*flag,'-B','-c',script],cwd=Path(c.__file__).parent,text=True,capture_output=True,check=True)
        outputs.append(cp.stdout.strip())
    assert outputs==['DENIED','DENIED']


def test_I05_unknown_person_cannot_be_inferred_from_peer_availability():
    s=c.initial_state();s['counterparts']['peer']['available']=True
    p=c.candidate(2020,30,'fake-person','COUNTERPART_CONTACT',counterpart='not_constructed')
    assert c.evaluate(s,p,{'licensed_objective_actions':['COUNTERPART_CONTACT']})=='REFUSED_UNCONSTRUCTED_COUNTERPART'


def test_I06_noncausal_label_does_not_change_committed_history():
    old=c.fixed_candidates
    try:
        def f(y):
            a=old(y)
            for z in a:
                if z['id']=='routine':z['possible_relevance_domains']=['entirely_different_caption']
            return a
        before=c.run();c.fixed_candidates=f;after=c.run()
    finally:c.fixed_candidates=old
    assert before['causal']['canonical_history_hash']==after['causal']['canonical_history_hash']
    assert before['proposal_audit_hash']!=after['proposal_audit_hash']


def test_I07_explicit_90_day_horizon_not_misrepresented_as_working_scheduler():
    s=c.initial_state();inp=c.render_input(s,2020)
    _,p=c.mocked_artifacts(inp)
    p['candidates']=[c.candidate(2020,100,'later','OBSERVED_NEUTRAL',subannual_horizon_days=90)]
    _,valid=c.validate_packet(p,inp)
    assert not valid


def test_I08_forged_prior_committed_receipt_must_not_be_trusted_by_restart():
    # P0 direct ledger source authenticity: fake externally inserted event, even
    # with plausible original field names and year/day, must not enter replay.
    s=c.initial_state()
    s['events']=[dict(id=c.fact_id(2020,'practice'),year=2020,day=30,
                      action='PRACTICE_OBSERVED', actor='child',source_ref='FORGED_SOURCE',
                      hash='FORGED_EVENT_DIGEST',prior_state_hash='FORGED_PRESTATE')]
    try:
        c.run(initial=s)
    except (AssertionError,ValueError,PermissionError,RuntimeError):return
    pytest.fail('C0R accepted unauthenticated historical event preimage in initial ledger')


def test_I09_two_existing_historical_events_cannot_have_same_committed_identity():
    s=c.initial_state()
    s['events']=[dict(id='observed:2020:alpha',year=2020,day=9,action='OBSERVED_NEUTRAL'),
                 dict(id='observed:2020:alpha',year=2020,day=10,action='OBSERVED_NEUTRAL')]
    try:c.run(initial=s)
    except (AssertionError,ValueError,PermissionError,RuntimeError):return
    pytest.fail('Duplicate historical occurrence identities in prestate accepted by C0R')


def test_I10_same_ref_source_contents_mutated_between_validation_and_append_must_refuse(monkeypatch):
    # Changes the material snapshot while keeping asserted SOURCE stable. This
    # represents untrusted physical source replacement, not a lawful event.
    original=c.apply_admitted
    def hostile(state,p,year,rules):
        if p['id']=='practice':
            state['world']['material_version']+=500
        return original(state,p,year,rules)
    monkeypatch.setattr(c,'apply_admitted',hostile)
    try: x=c.run()
    except (AssertionError,ValueError,PermissionError,RuntimeError):return
    assert c.fact_id(2020,'practice') not in {e['id'] for e in x['causal']['final_state']['events']},'material source content replacement admitted without immutable content pin'


def test_I11_one_two_fixed_equal_under_same_toy_world_owner():
    x=c.mode_comparison();assert x['causal_equal']
    assert x['physical_mock_invocations']=={'ONE_CALL':3,'TWO_CALL':4,'FIXED_PACKET':0}
    assert x['disclaimer'].endswith('NO_REAL_LLM_QUALITY_COST_INFERENCE')


def test_I12_no_real_psychological_update_and_no_forced_event():
    s=c.initial_state();x=c.run(initial=s,rules={})
    assert x['causal']['final_state']['actor']['beliefs']=='UNISSUED'
    assert x['causal']['final_state']['actor']['affect']=='UNISSUED'
    assert x['causal']['final_state']['events']==[]


def test_I13_direct_append_must_revalidate_event_time_and_year_even_when_grants_match():
    # A participant can call the exported append function without first invoking
    # validate_packet. This should never put a day-366 2021 proposal in year 2020.
    s=c.initial_state()
    p=c.candidate(2021,366,'future','OBSERVED_NEUTRAL')
    rules={'licensed_objective_actions':['OBSERVED_NEUTRAL']}
    try:c.apply_admitted(s,p,2020,rules)
    except (AssertionError,ValueError,PermissionError,RuntimeError):return
    pytest.fail('public apply_admitted appended out-of-range future-year event without currentness validation')


def test_I14_direct_append_must_not_accept_unvalidated_proposal_issuer_or_psychic_field():
    s=c.initial_state()
    p=c.candidate(2020,30,'psych_claim','OBSERVED_NEUTRAL',CAN011_UPDATE={'false_psyche_effect':'true'})
    rules={'licensed_objective_actions':['OBSERVED_NEUTRAL']}
    try:c.apply_admitted(s,p,2020,rules)
    except (AssertionError,ValueError,PermissionError,RuntimeError):return
    pytest.fail('public apply_admitted accepted unauthorized noncausal candidate field without validate_packet')
