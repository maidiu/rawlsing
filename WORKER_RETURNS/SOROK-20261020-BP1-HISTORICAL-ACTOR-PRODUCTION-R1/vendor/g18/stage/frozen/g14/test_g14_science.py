"""Independent G14 falsifiers; failures remain literal RED, never xfail.

All inputs are mutations/severances of existing source-free laboratory fixtures.
No new people, generated actors, biological events, provider calls or owner rules.
F1..F7 are mechanisms, not independent-discovery counts. Stronger tests state the
scientific dependency required for reuse, not a claim that the lab has V3 rights.
"""
from pathlib import Path
import copy, hashlib, hmac, importlib, json, os, sys
import pytest

ROOT=Path(__file__).resolve().parent
LAB=ROOT/'reproduction/03_POSTREPAIR_COURT/sources/sgi1/01_LAB_IMPLEMENTATION'
sys.dont_write_bytecode=True
sys.path.insert(0,str(LAB))
NETWORK=[]
def offline(event,args):
    if event in {'socket.connect','socket.getaddrinfo','socket.__new__'}:
        NETWORK.append(event)
        raise RuntimeError('G14_NETWORK_FORBIDDEN')
sys.addaudithook(offline)
from lab_sgi1.construction import (DadHistoryBuilder, forward_replay_to_endpoint,
    psyche_from_dad_events, stopping_law_check, heldout_independent_probes,
    construct_second_parent)
from lab_sgi1.core import ScopedRNG, h_obj, canon
from lab_sgi1.mother import build_mother_checkpoint
from lab_sgi1.proposal import (build_proposal_prompt, freeze_proposal_record,
    PROPOSAL_SYSTEM_PROMPT, dedup_candidates, frozen_fallback_record)
from lab_sgi1.selection import adp020_select, candidate_replay_hash
from lab_sgi1.relation import reconcile
from lab_sgi1.continuation import (forward_continuation,
    child_developmental_environment_fixture, lab_conception_boundary)
from lab_sgi1.qualification import qualify
from lab_sgi1.world import build_world
from lab_sgi1.pipeline import run_pipeline

SEED='13'*32
STREAM='v3.causal.adp015.conception_scenario_selection'
OBS={}

def observe(name, **data):
    OBS[name]=data
    return data

@pytest.fixture(scope='session',autouse=True)
def persist_observations():
    yield
    imports=[]
    for name in ['__init__','construction','continuation','core','dag','k11_contract',
                 'k11_runner','mother','pipeline','proposal','qualification','relation','selection','world']:
        m=importlib.import_module('lab_sgi1' if name=='__init__' else 'lab_sgi1.'+name)
        p=Path(m.__file__);b=p.read_bytes()
        imports.append(dict(module=m.__name__,module_file=str(p.relative_to(ROOT)),
            git_blob_sha1=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()))
    (ROOT/'execution/g14_observations.json').write_text(json.dumps(dict(observations=OBS,imports=imports,network_attempts=NETWORK,new_provider_calls=0),indent=2,sort_keys=True)+'\n')

def ec(place='INST_WORKSHOP_A',route='ROUTE_LOCAL_CLOSED'):
    return dict(route_kind_id=route,time_or_interval='T_ENCOUNTER_LAB_WINDOW',
        required_state_predicates=[dict(field='place',equals=place),
          dict(field='availability_status',equals='available_for_encounter')])

def history():
    return DadHistoryBuilder('G13_ACTUAL_SECOND_PARENT','G13_FIXED_SEED',ec()).build()

def mother(variant='M0'):
    return build_mother_checkpoint('G13_REL',variant).anchor_dict()

def assess(events,psyche=None):
    p=psyche_from_dad_events(events) if psyche is None else psyche
    r=forward_replay_to_endpoint(events,ec())
    pr=heldout_independent_probes(events,p)
    return dict(replay=r,probes=pr,stopping=stopping_law_check(events,p,ec(),r,pr))

def select(classes,seed=SEED):
    return adp020_select('SIM_UNIFORM_CLASSES',classes,seed,'G13_SCOPE')

def candidates():
    return [dict(class_key='A',representative_id='A',payload='ORIGINAL'),
            dict(class_key='B',representative_id='B',payload='OTHER')]

def test_f1_clean_and_shuffled_replay_have_same_state():
    a=forward_replay_to_endpoint(history(),ec())
    b=forward_replay_to_endpoint(list(reversed(history())),ec())
    assert a['endpoint_match'] and b['endpoint_match']
    assert a['recomputed_state']==b['recomputed_state']

@pytest.mark.parametrize('attack',['missing_parent','future_parent','self_parent','duplicate_id',
    'duplicate_index','orphan','endpoint_place','endpoint_availability','route_removed'])
def test_f1_dependency_severance_and_forgery_refused(attack):
    e=history()
    if attack=='missing_parent': e[4]['causal_parent_event_ids']=['ABSENT_PARENT']
    elif attack=='future_parent': e[0]['causal_parent_event_ids']=[e[-1]['event_id']]
    elif attack=='self_parent': e[4]['causal_parent_event_ids']=[e[4]['event_id']]
    elif attack=='duplicate_id': e[4]['event_id']=e[3]['event_id']
    elif attack=='duplicate_index': e[4]['effective_index']=e[3]['effective_index']
    elif attack=='orphan': e[4]['causal_parent_event_ids']=[]
    elif attack=='endpoint_place': e[-1]['payload']['place']='IMPOSSIBLE_SITE'
    elif attack=='endpoint_availability': e[-1]['payload']['availability_status']='unavailable'
    else: e=[x for x in e if x['kind']!='COMMISSIONED_WORK']
    r=forward_replay_to_endpoint(e,ec())
    observe('F1_'+attack,input=e,result=r)
    assert not r['endpoint_match']

def test_f1_route_parent_substitution_cannot_replace_work_formation():
    e=history()
    for x in e:
        if x['kind']=='COMMISSIONED_WORK': x['causal_parent_event_ids']=[e[0]['event_id']]
    r=assess(e)
    observe('F1_semantic_parent_substitution',input=e,result=r)
    assert not r['stopping']['sufficient'], 'root existence cannot prove commissioned-work competence'

@pytest.mark.parametrize('domain',['WORK_POSITION','ORGANISMIC_EVENT','PROJECT',
                                 'NONMOTHER_RELATIONSHIP','PRACTICE_FORMATION','MEMORY_TRACE'])
def test_f2_required_domain_severance_refuses_sufficiency(domain):
    e=[x for x in history() if x['kind']!=domain]
    r=assess(e)
    observe('F2_remove_'+domain,result=r)
    assert not r['stopping']['sufficient']

def test_f2_nonempty_but_unresolvable_psyche_refs_refused():
    e=history();p=psyche_from_dad_events(e)
    for items in p.values():
        for item in items: item['causal_event_refs']=['ABSENT_PARENT']
    r=assess(e,p)
    observe('F2_unresolvable_psyche',psyche=p,result=r)
    assert not r['stopping']['sufficient']

def test_f2_memory_experienced_basis_must_resolve():
    e=history()
    for x in e:
        if x['kind']=='MEMORY_TRACE': x['payload']['experienced_basis_event']='ABSENT_PARENT'
    r=assess(e)
    observe('F2_unresolvable_experience',input=e,result=r)
    assert not r['stopping']['sufficient']

def test_f2_empty_psyche_cannot_certify_existing_formation():
    r=assess(history(),dict(attitudes=[],practices=[],strivings=[]))
    observe('F2_empty_psyche',result=r)
    assert not r['stopping']['sufficient']

def test_f3_removing_project_consequence_disables_action():
    e=history()
    for x in e:
        if x['kind']=='PROJECT': x['payload'].pop('durable_effect',None)
    pr=heldout_independent_probes(e,psyche_from_dad_events(e))
    observe('F3_removed_consequence',result=pr)
    assert not pr['probes'][0]['pass']

def test_f3_removing_actor_psyche_disables_motivated_actions():
    e=history();a=heldout_independent_probes(e,psyche_from_dad_events(e))
    b=heldout_independent_probes(e,{})
    observe('F3_psyche_severance',before=a,after=b)
    assert not b['heldout_independence_pass'], 'actions must depend on represented actor motivation/formation'

def test_f3_unrelated_false_consequence_is_not_capability_evidence():
    e=history()
    for x in e:
        if x['kind']=='PROJECT': x['payload']['durable_effect']='NO_SKILL_GAIN_NO_COMPLETED_WORK'
    pr=heldout_independent_probes(e,psyche_from_dad_events(e))
    observe('F3_false_consequence',input=e,result=pr)
    assert not pr['probes'][0]['pass']

def test_f3_missing_peer_identity_cannot_prove_actor_specific_obligation():
    e=history()
    for x in e:
        if x['kind']=='NONMOTHER_RELATIONSHIP': x['payload']['counterpart']=None
    pr=heldout_independent_probes(e,psyche_from_dad_events(e))
    observe('F3_missing_peer',result=pr)
    assert not pr['probes'][1]['pass']

@pytest.mark.parametrize('place',['target','world','psyche','route','tuple','spaced_literal'])
def test_f4_all_visible_prompt_paths_are_embargoed(place):
    a=mother();t={};w={};route=None;secret='G14_FUTURE_CHILD_WOUND_SECRET'
    if place=='target': t['nested']=[{'future_child_personality':secret}]
    elif place=='world': w['nested']=[{'child_outcome':secret}]
    elif place=='psyche': a['psyche']['nested']=[{'future_child_outcome_label':secret}]
    elif place=='route': route=secret
    elif place=='tuple': w['records']=({'future_child_personality':secret},)
    else:
        secret='The future child will develop the selected wound'
        w['note']=secret
    prompt=build_proposal_prompt(a,t,w,route,4)
    observe('F4_prompt_'+place,prompt=json.loads(prompt),secret=secret)
    assert secret not in prompt

def test_f4_clean_older_child_history_preserved():
    a=mother('M2');before=copy.deepcopy(a)
    p=json.loads(build_proposal_prompt(a,{}, {},None,4))
    assert p['mother_anchor_visible_fields']['already_generated_child_refs']==['LAB_OLDER_CHILD_O1']
    assert a==before

def test_f4_embargoed_output_cannot_become_eligible_candidate():
    c=copy.deepcopy(frozen_fallback_record('M0',None).parsed_candidates[0])
    c['future_child_personality']='G14_FUTURE_CHILD_WOUND_SECRET'
    rec=freeze_proposal_record('M0',None,'{}',PROPOSAL_SYSTEM_PROMPT,
        {'raw_output':json.dumps([c])},4)
    q=qualify(rec.parsed_candidates[0],mother(),build_world(False))
    observe('F4_output_admission',candidate=rec.parsed_candidates[0],qualification=q)
    assert not q['eligibility']['eligible'], 'a system-prompt prohibition is not output admission enforcement'

@pytest.mark.parametrize('seed',['short','NOT_A_TOKEN','AB'*32,'00'*31,'gg'*32,SEED+'\n'])
def test_f5_unknown_roots_refuse_without_draw(seed):
    r=select(candidates(),seed)
    observe('F5_invalid_root_'+seed[:10],result=r)
    assert r['status']=='NOT_EXECUTED_AUTHORITY_HOLD' and r['n_draws']==0

@pytest.mark.parametrize('seed',['R0','R1','R2','G12','G12_SEED'])
def test_f5_each_legacy_token_explicitly_not_granted(seed):
    r=select(candidates(),seed)
    observe('F5_legacy_'+seed,result=r)
    assert r['adp020_entitlement']=='NOT_GRANTED'
    assert r['adp020_hold']=='ADP020_REAL_ROOT_SEED_REQUIRED'
    assert r['draw']['scope_seed_sha256']==''

def normative_lineage(scope='G13_SCOPE'):
    domain=b'RAWLSING\0ADP-020\0V3_CAUSAL_HMAC_SHA256_COUNTER_V1\0'
    # Independent encoding, no production KDF helper used.
    enc=lambda o:json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
    ss=hmac.new(bytes.fromhex(SEED),domain+enc(dict(kind='scope',scope_kind='GENEALOGY',scope_id=scope)),hashlib.sha256).digest()
    st=hmac.new(ss,domain+enc(dict(kind='stream',stream_name=STREAM)),hashlib.sha256).digest()
    return domain,enc,ss,st

def test_f5_hmac_entropy_matches_independent_reference():
    domain,enc,ss,st=normative_lineage()
    co=dict(scope_kind='GENEALOGY',scope_id='G13_SCOPE',stream_name=STREAM,
        anchor_event_index=-1,anchor_event_id_or_init_checkpoint_hash='INIT:'+ss.hex(),
        rule_invocation_id='LAB_SOROK_G13_REPAIRED',decision_slot='slot',occurrence_index=0,
        draw_index=0,uniform_below_n=7,block_index=0)
    raw=int.from_bytes(hmac.new(st,domain+enc(co),hashlib.sha256).digest()[:8],'big')
    r=ScopedRNG(SEED,STREAM,'G13_SCOPE').draw(7,'slot','set').as_dict()
    observe('F5_reference_hmac',coordinate=co,expected_raw=raw,receipt=r)
    assert r['accepted_raw_u64']==raw and r['draw_value']==raw%7

def test_f5_lineage_digest_fields_are_digests_of_derived_seeds():
    _,_,ss,st=normative_lineage()
    r=ScopedRNG(SEED,STREAM,'G13_SCOPE').draw(7,'slot','set').as_dict()
    observe('F5_lineage_digests',expected_scope_sha256=hashlib.sha256(ss).hexdigest(),expected_stream_sha256=hashlib.sha256(st).hexdigest(),receipt=r)
    assert r['scope_seed_sha256']==hashlib.sha256(ss).hexdigest()
    assert r['stream_seed_sha256']==hashlib.sha256(st).hexdigest()

def test_f5_rejection_control_preserves_one_semantic_draw():
    rng=ScopedRNG(SEED,STREAM,'G13_SCOPE');seq=iter([2**64-1,2**64-1,5])
    rng._raw=lambda *args:next(seq)
    r=rng.draw(3,'slot','set')
    observe('F5_rejection',receipt=r.as_dict())
    assert r.entropy_block_count==3 and r.draw_index==0 and rng.draw_count==1 and r.draw_value==2

def test_f5_fresh_legacy_lineage_receipt_never_claims_adp020():
    try:
        r=ScopedRNG('R0',STREAM,'G13_SCOPE').lineage_receipt()
    except Exception as exc:
        observe('F5_fresh_lineage',exception_type=type(exc).__name__,exception=str(exc))
        raise
    observe('F5_fresh_lineage',result=r)
    assert r['adp020_entitlement']=='NOT_GRANTED'

def test_f5_namespace_pattern_does_not_register_arbitrary_stream():
    with pytest.raises(ValueError):
        ScopedRNG(SEED,'v3.causal.unissued_g14_stream','G13_SCOPE').draw(7,'slot','set')

def test_f5_draw_receipt_binds_actual_full_entropy_coordinate():
    domain,enc,ss,st=normative_lineage()
    co=dict(scope_kind='GENEALOGY',scope_id='G13_SCOPE',stream_name=STREAM,
        anchor_event_index=-1,anchor_event_id_or_init_checkpoint_hash='INIT:'+ss.hex(),
        rule_invocation_id='LAB_SOROK_G13_REPAIRED',decision_slot='slot',occurrence_index=0,
        draw_index=0,uniform_below_n=7,block_index=0)
    r=ScopedRNG(SEED,STREAM,'G13_SCOPE').draw(7,'slot','set').as_dict()
    observe('F5_coordinate_binding',expected=h_obj(co),receipt=r)
    assert r['draw_coordinate_hash']==h_obj(co)

def test_f5_decision_receipt_contains_rule_and_replay_custody():
    r=select(candidates())
    required={'semantic_rule_id','semantic_rule_version','semantic_rule_registry_hash',
              'decision_replay_identity_hash','causal_run_id','stochastic_parameters_hash'}
    observe('F5_decision_custody',missing=sorted(required-r.keys()),result=r)
    assert required<=r.keys()

def test_f5_other_scope_draws_do_not_perturb_existing_parent():
    a=ScopedRNG(SEED,STREAM,'G13_SCOPE');b=ScopedRNG(SEED,STREAM,'OTHER_SCOPE')
    before=a.draw(7,'slot','set').as_dict()
    for _ in range(5): b.draw(7,'slot','set')
    fresh=ScopedRNG(SEED,STREAM,'G13_SCOPE').draw(7,'slot','set').as_dict()
    assert before==fresh

def test_f6_real_endpoint_mutation_changes_identity():
    d=dedup_candidates(frozen_fallback_record('M0',None).parsed_candidates)['classes']
    altered=copy.deepcopy(d)
    altered[0]['candidate']['endpoint_constraints']['required_state_predicates']=[dict(field='place',equals='IMPOSSIBLE_SITE')]
    a=select(d);b=select(altered)
    observe('F6_payload_binding',before=a,after=b)
    assert a['candidate_set_hash']!=b['candidate_set_hash']

def test_f6_candidate_permutation_and_exact_replay():
    c=candidates();a=select(c);b=select(list(reversed(c)));d=select(copy.deepcopy(c))
    assert a==b==d

def test_f6_multiplicity_bookkeeping_does_not_change_payload_identity():
    a=candidates()[0];b=dict(a,member_ids=['one','two'],member_count=2)
    assert candidate_replay_hash(a)==candidate_replay_hash(b)

def test_f6_new_lower_id_paraphrase_preserves_selection_identity():
    c=copy.deepcopy(frozen_fallback_record('M0',None).parsed_candidates)
    alias=copy.deepcopy(c[0]);alias['candidate_local_id']='A_PARAPHRASE'
    alias['assumptions']=['same workplace adjacency in different wording']
    d1=dedup_candidates(c);d2=dedup_candidates(c+[alias])
    a=select(d1['classes']);b=select(d2['classes'])
    observe('F6_paraphrase_representative',dedup_same=d1['class_set_hash']==d2['class_set_hash'],before=a,after=b)
    assert a['candidate_set_hash']==b['candidate_set_hash']

def test_f6_conflicting_required_endpoint_states_do_not_dedup():
    c=copy.deepcopy(frozen_fallback_record('M0',None).parsed_candidates[:1])
    other=copy.deepcopy(c[0]);other['candidate_local_id']='A_CONTRADICTION'
    other['endpoint_constraints']['required_state_predicates']=[dict(field='place',equals='IMPOSSIBLE_SITE')]
    d=dedup_candidates(c+[other])
    observe('F6_conflicting_endpoint_dedup',result=d)
    assert d['n_classes']==2

def test_f6_duplicate_class_keys_refuse_instead_of_order_dependent_winner():
    c=candidates();c[1]['class_key']=c[0]['class_key']
    a=select(c);b=select(list(reversed(c)))
    observe('F6_duplicate_class_keys',before=a,after=b)
    assert a['status']!='COMMITTED' and b['status']!='COMMITTED'

def test_f6_pipeline_preserves_selected_candidate_required_endpoint_state():
    rec=frozen_fallback_record('M0','ROUTE_LOCAL_CLOSED')
    rec.parsed_candidates[0]['endpoint_constraints']['required_state_predicates']=[dict(field='place',equals='IMPOSSIBLE_SITE')]
    rec.dedup=dedup_candidates(rec.parsed_candidates)
    result=run_pipeline(fixture_variant='M0',causal_run_id='G13_SCOPE',root_seed=SEED,
        policy_name='SIM_UNIFORM_CLASSES',proposal_record=rec,model_enabled=False)
    observe('F6_pipeline_endpoint_drop',scenario=result['scenario'],construction=result['construction_summary'],terminal=result['terminal'])
    assert result['terminal']['status']!='COMMITTED'

def test_f7_empty_history_refuses_relation_and_paternal_continuation():
    a=mother();r=reconcile(a,[],dict(candidate_kind='PROVISIONAL_COUNTERPART'))
    c=forward_continuation(a,[],r)
    assert r['status']!='COMMITTED' and not c['paternal_continuation_admitted']

def test_f7_witness_for_different_actor_cannot_admit_relation():
    a=mother();e=history()
    for x in e:
        if x['kind']=='COMMISSIONED_WORK': x['actors']=[a['actor_id']]
    r=reconcile(a,e,dict(candidate_kind='PROVISIONAL_COUNTERPART'))
    observe('F7_cross_actor_witness',input=e,result=r)
    assert r['status']!='COMMITTED'

def test_f7_own_work_without_shared_maternal_encounter_cannot_form_relation():
    a=mother();e=history()
    r=reconcile(a,e,dict(candidate_kind='PROVISIONAL_COUNTERPART'))
    observe('F7_solo_work_witness',witnesses=r.get('objective_relation',{}),result=r)
    assert r['status']!='COMMITTED', 'work at a site is not a joint relationship-forming witness'

def test_f7_severed_project_cannot_continue_as_fixed_repair_project():
    a=mother();e=history();rel=reconcile(a,e,dict(candidate_kind='PROVISIONAL_COUNTERPART'))
    full=forward_continuation(a,e,rel)
    cut=[x for x in e if x['kind'] not in {'PROJECT','STRIVING','PRACTICE_FORMATION','ATTITUDE_FORMATION'}]
    reduced=forward_continuation(a,cut,rel)
    observe('F7_project_severance',before=full,after=reduced)
    paternal=[x for x in reduced['continuation_events'] if x.get('actor')=='G13_ACTUAL_SECOND_PARENT']
    assert not paternal or all('repair_bench' not in json.dumps(x) for x in paternal)

def test_f7_absent_paternal_continuation_cannot_emit_positive_paternal_exposure():
    a=mother();c=forward_continuation(a,[],{})
    out=child_developmental_environment_fixture(a,[],c,lab_conception_boundary())
    observe('F7_absent_paternal_exposure',continuation=c,environment=out)
    bad=[x for x in out['exposures'] if 'PATERNAL' in x['exposure_id']]
    assert not bad or all(not x.get('effective_after_admission') for x in bad)

def test_f7_no_household_admission_cannot_justify_combined_income_exposure():
    a=mother();e=history();r=reconcile(a,e,dict(candidate_kind='PROVISIONAL_COUNTERPART'))
    c=forward_continuation(a,e,r)
    out=child_developmental_environment_fixture(a,e,c,lab_conception_boundary())
    observe('F7_household_exposure',relation=r,environment=out)
    assert not any(x['material_context']=='combined_wage_artisan_income_band' for x in out['exposures'])

def test_f7_distinct_full_candidate_keys_cannot_alias_parent_identity():
    # Hash-valued perturbations of the existing candidate fixture; no actor creation.
    key=dedup_candidates(frozen_fallback_record('M0',None).parsed_candidates)['classes'][0]['class_key']
    seen={}
    for i in range(10000):
        digest=h_obj(dict(original_class=key,fixture_perturbation=i))
        if digest[:10] in seen:
            ka,kb=seen[digest[:10]],digest
            break
        seen[digest[:10]]=digest
    else: raise AssertionError('deterministic fixture collision not found')
    a=construct_second_parent({'class_key':ka},ec(),['G13_FIXED_SEED'])
    b=construct_second_parent({'class_key':kb},ec(),['G13_FIXED_SEED'])
    aid=a['selected_events'][0]['actors'][0];bid=b['selected_events'][0]['actors'][0]
    observe('F7_parent_identity_alias',class_a=ka,class_b=kb,actor_a=aid,actor_b=bid)
    assert aid!=bid

def test_ceilings_mother_older_child_and_impossible_endpoint_preserved():
    m=mother('M2');before=copy.deepcopy(m)
    out=construct_second_parent({'class_key':'G13_IMPOSSIBLE'},ec('IMPOSSIBLE_SITE'),['S1','S2','S3','S4'])
    assert out['terminal_status']=='HISTORY_SEARCH_EXHAUSTED' and out['n_attempts']==4
    assert out['selected_events'] is None and m==before
    assert m['already_generated_child_refs']==['LAB_OLDER_CHILD_O1']
    b=lab_conception_boundary()
    assert b['child_generated_events']==0 and not b['birth_alias']

def test_ceilings_offline_pipeline_hidden_future_noninterference():
    rec=frozen_fallback_record('M0',None)
    kwargs=dict(fixture_variant='M0',causal_run_id='G13_SCOPE',root_seed=SEED,
        policy_name='SIM_UNIFORM_CLASSES',proposal_record=rec,model_enabled=False)
    a=run_pipeline(**kwargs,future_child_shadow={'label':'A'})
    b=run_pipeline(**kwargs,future_child_shadow={'label':'B'})
    def without_timing(x):
        if isinstance(x,dict): return {k:without_timing(v) for k,v in x.items() if not k.endswith('seconds') and k not in {'ledger','costs','ledger_hash'}}
        if isinstance(x,list): return [without_timing(v) for v in x]
        return x
    # Only compare actual selection/history, never an authored equality flag.
    keys=['selection_summary','construction_summary','dad_events','dad_psyche','relation','continuation','child_fixture']
    observe('CEILING_pipeline',keys=keys,selected={k:without_timing(a[k]) for k in keys},other={k:without_timing(b[k]) for k in keys})
    assert keys
    assert all(without_timing(a[k])==without_timing(b[k]) for k in keys)
    assert NETWORK==[]
