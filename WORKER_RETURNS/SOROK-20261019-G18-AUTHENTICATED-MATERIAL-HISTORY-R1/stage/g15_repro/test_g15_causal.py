"""Prospective G15 causal contrasts. Oracles frozen in 01_CAUSATION_PREREGISTRATION.

Offline deterministic research; these are author tests, not an independent court.
All source mutations have exact same-node proof witnesses in the sibling contract.
"""
from pathlib import Path
from copy import deepcopy
import base64,hashlib,hmac,json,os,subprocess,sys
import pytest
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'candidate'))
NETWORK=[]
def offline(event,args):
 if event in {'socket.connect','socket.getaddrinfo','socket.__new__'}:
  NETWORK.append(event);raise RuntimeError('G15_NETWORK_FORBIDDEN')
sys.addaudithook(offline)
from lab_sgi1.core import h_obj,canon,ScopedRNG,RngAuthorityError,ADP020_DOMAIN_SEPARATOR
from lab_sgi1.history import PersonHistoryBuilder,replay_history,derive_psyche,validate_psyche
from lab_sgi1.construction import DadHistoryBuilder,forward_replay_to_endpoint,stopping_law_check,heldout_independent_probes,construct_second_parent
from lab_sgi1.mother import build_mother_checkpoint
from lab_sgi1.proposal import dedup_candidates,frozen_fallback_record,build_proposal_prompt,freeze_proposal_record,PROPOSAL_SYSTEM_PROMPT
from lab_sgi1.qualification import qualify
from lab_sgi1.selection import adp020_select,candidate_replay_hash,replay_decision,DecisionJournal,STREAM
from lab_sgi1.world import build_world
from lab_sgi1.joint import material_joint_opportunity,observe_joint_actions,validate_joint
from lab_sgi1.relation import reconcile
from lab_sgi1.continuation import forward_continuation,child_developmental_environment_fixture,lab_conception_boundary
from lab_sgi1.research import inputs,run
OBS={}
@pytest.fixture(scope='session',autouse=True)
def persist():
 yield
 (ROOT/'execution').mkdir(exist_ok=True)
 imports=[]
 for name,m in sorted(sys.modules.items()):
  if name.startswith('lab_sgi1') and getattr(m,'__file__',None):
   path=Path(m.__file__);b=path.read_bytes();imports.append(dict(module=name,path=str(path.relative_to(ROOT)),sha256=hashlib.sha256(b).hexdigest(),git_blob_sha1=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()))
 (ROOT/'execution/prospective_observations.json').write_text(json.dumps(dict(observations=OBS,imports=imports,network_attempts=NETWORK,new_provider_calls=0),indent=2,sort_keys=True)+'\n')

def ec(place='INST_WORKSHOP_A'):
 return dict(route_kind_id='ROUTE_LOCAL_CLOSED',time_or_interval='T_ENCOUNTER_LAB_WINDOW',required_state_predicates=[dict(field='place',equals=place),dict(field='availability_status',equals='available_for_encounter')])
def history():return DadHistoryBuilder('G15_PROSPECTIVE_ADULT','G15_RESEARCH_SEED',ec()).build()
def mother(v='M0'):return build_mother_checkpoint('FIX_'+v,v).anchor_dict()
def st(events,p=None):
 p=derive_psyche(events) if p is None else p
 return stopping_law_check(events,p,ec(),forward_replay_to_endpoint(events,ec()),heldout_independent_probes(events,p))
def relation_packet():
 a=mother();e=history();w=observe_joint_actions(a,e,material_joint_opportunity())
 return a,e,w,reconcile(a,e,dict(candidate_kind='PROVISIONAL_COUNTERPART',joint_evidence=w))


def test_typed_history_drives_endpoint():
 e=history();r=forward_replay_to_endpoint(e,ec());OBS['endpoint_positive']=r
 assert r['endpoint_match'] is True
 assert r['recomputed_state']['skill']==6
 assert r['recomputed_state']['completed_units']==3
 attend=next(w for w in r['value_witnesses'] if w['kind']=='COMMISSIONED_WORK')
 assert {x['path'] for x in attend['readset']}=={'effect'}
 assert {x['value']['completed_units'] for x in attend['readset'] if 'completed_units' in x['value']}=={3}
 assert all(next(x['effective_index'] for x in e if x['event_id']==v['event_id'])<attend['effective_index'] for v in attend['readset'])


def test_formation_drives_sufficiency():
 e=history();p=derive_psyche(e);result=st(e,p);OBS['formation_positive']=result
 assert result['sufficient'] is True
 assert len(p['practices'])==len(p['attitudes'])==len(p['strivings'])==1
 assert p['practices'][0]['formed_value']['checks']==3


def test_peer_action_drives_obligation():
 e=history();r=replay_history(e);pr=heldout_independent_probes(e,derive_psyche(e));OBS['independent_actions']=pr
 assert r['state']['debt_units']==2
 assert pr['heldout_independence_pass'] is True
 assert pr['probes'][1]['typed_action']['delta']=={'debt_units':-1,'free_hours':-1}
 assert pr['probes'][0]['typed_action']['after']['completed_units']==4
 assert any(x['kind']=='PEER_ACTION' and x['owner_id']!=r['state']['actor_id'] for x in pr['probes'][1]['supporting_evidence'])


def test_selected_endpoint_drives_terminal():
 result=run();OBS['selected_endpoint_positive']=dict(terminal=result['terminal'],scenario=result['scenario'],selection=result['selection_summary'])
 assert result['terminal']['status']=='COMMITTED'
 assert result['scenario']['endpoint_constraints']['required_state_predicates'][0]['equals']=='INST_WORKSHOP_A' or any(p==dict(field='place',equals='INST_WORKSHOP_A') for p in result['scenario']['endpoint_constraints']['required_state_predicates'])
 assert result['dad_events'][-1]['payload']['place']=='INST_WORKSHOP_A'
 assert result['relation']['objective_relation']['witness']['status']=='WITNESSED'


def test_joint_actions_drive_relation():
 a,e,w,r=relation_packet();OBS['joint_positive']=dict(witness=w,relation=r)
 assert r['relationship_committed'] is True
 assert r['objective_relation']['participants']==[a['actor_id'],'G15_PROSPECTIVE_ADULT']
 assert all(x['status']=='PERFORMED' and x['after']['completed_units']-x['before']['completed_units']==1 for x in w['actions'])
 assert r['reciprocity_inferred'] is False
 assert {x['perceived_state'] for x in r['perceived_states']}=={'UNKNOWN_OR_NONRECIPROCAL'}


def test_parent_history_drives_continuation_context():
 a,e,w,r=relation_packet();cont=forward_continuation(a,e,r);out=child_developmental_environment_fixture(a,e,cont,lab_conception_boundary())
 OBS['continuation_positive']=dict(continuation=cont,context=out)
 assert cont['paternal_continuation_admitted'] is True
 dad=next(x for x in cont['continuation_events'] if x['actor']=='G15_PROSPECTIVE_ADULT')
 assert dad['payload']['after']['cash']-dad['payload']['before']['cash']==dad['payload']['earned']
 assert dad['payload']['earned']>0
 assert len(out['potential_material_contexts'])==2
 assert out['exposures']==[] and out['child_generated_events']==0


def test_entropy_coordinate_drives_receipt():
 receipt=adp020_select('SIM_UNIFORM_CLASSES',[dict(class_key='A',representative_id='A',payload='ORIGINAL'),dict(class_key='B',representative_id='B',payload='OTHER')],'13'*32,'G13_SCOPE')
 d=receipt['draw'];OBS['entropy_positive']=receipt
 assert d['draw_coordinate_hash']==h_obj(d['entropy_coordinate'])
 assert replay_decision(receipt)['status']=='EXACT_REPLAY'
 assert receipt['native_semantic_grant']==receipt['adp020_entitlement']=='NOT_GRANTED'
 scope=hmac.new(bytes.fromhex('13'*32),ADP020_DOMAIN_SEPARATOR+canon(dict(kind='scope',scope_kind='GENEALOGY',scope_id='G13_SCOPE')),hashlib.sha256).digest()
 assert d['scope_seed_sha256']==hashlib.sha256(scope).hexdigest()


def test_output_membrane_drives_eligibility():
 c=deepcopy(frozen_fallback_record('M0','ROUTE_LOCAL_CLOSED').parsed_candidates[0]);bad=deepcopy(c);bad['future_child_personality']='LATER_WOUND'
 good=qualify(c,mother(),build_world(False));q=qualify(bad,mother(),build_world(False));OBS['output_membrane']=dict(clean=good,tainted=q)
 assert good['eligibility']['eligible'] is True
 assert q['eligibility']['eligible'] is False
 assert q['hard_feasibility']['status']=='NOT_EXECUTED_AUTHORITY_HOLD'


@pytest.mark.parametrize('attack',['root_parent','cross_actor','owner','empty_psyche','dangling_psyche','wrong_formation_value','denial_effect','null_peer','future_experience','peer_action_absent'])
def test_source_severances_refuse_same_sufficiency(attack):
 e=history();p=derive_psyche(e)
 assert st(e,p)['sufficient'] is True
 if attack=='root_parent':
  next(x for x in e if x['kind']=='COMMISSIONED_WORK')['causal_parent_event_ids']=[e[0]['event_id']]
 elif attack=='cross_actor':next(x for x in e if x['kind']=='WORK_POSITION')['actors']=['OTHER_ACTOR']
 elif attack=='owner':next(x for x in e if x['kind']=='PROJECT')['owner_id']='UNISSUED'
 elif attack=='empty_psyche':p={}
 elif attack=='dangling_psyche':p['practices'][0]['causal_event_refs']=['ABSENT']
 elif attack=='wrong_formation_value':p['practices'][0]['formed_value']['checks']=999
 elif attack=='denial_effect':next(x for x in e if x['kind']=='PROJECT')['payload']['durable_effect']='NO_SKILL_GAIN_NO_COMPLETED_WORK'
 elif attack=='null_peer':next(x for x in e if x['kind']=='NONMOTHER_RELATIONSHIP')['payload']['counterpart']=None
 elif attack=='future_experience':next(x for x in e if x['kind']=='MEMORY_TRACE')['payload']['experienced_basis_event']=e[-1]['event_id']
 else:e=[x for x in e if x['kind']!='PEER_ACTION']
 after=st(e,p);OBS['source_severance_'+attack]=after
 assert after['sufficient'] is False


def test_endpoint_demand_never_authors_the_past():
 a=DadHistoryBuilder('A','G15_RESEARCH_SEED',ec()).build();b=DadHistoryBuilder('A','G15_RESEARCH_SEED',ec('IMPOSSIBLE_SITE')).build()
 assert a==b
 assert forward_replay_to_endpoint(a,ec())['endpoint_match'] is True
 assert forward_replay_to_endpoint(b,ec('IMPOSSIBLE_SITE'))['endpoint_match'] is False


def test_real_material_opportunity_changes_endpoint_without_retrofit():
 clean=history();world=deepcopy(next(x['payload'] for x in clean if x['kind']=='WORLD_MATERIAL'))
 world['offers']['ROUTE_LOCAL_CLOSED']['permit']=False
 changed=PersonHistoryBuilder('G15_PROSPECTIVE_ADULT','G15_RESEARCH_SEED',material=world).build()
 r=replay_history(changed);OBS['world_permission_counterfactual']=r
 assert r['valid'] is True
 assert r['state']['place']=='INST_COMMUNITY_D'
 assert forward_replay_to_endpoint(changed,ec())['endpoint_match'] is False
 assert r['state']['projects']==replay_history(clean)['state']['projects']


def test_empty_world_and_no_relation_are_lawful_alternatives():
 world=deepcopy(next(x['payload'] for x in history() if x['kind']=='WORLD_MATERIAL'))
 world['offers']={}
 e=PersonHistoryBuilder('G15_PROSPECTIVE_ADULT','G15_RESEARCH_SEED',material=world).build();r=replay_history(e)
 assert r['valid'] is True
 assert r['state']['place'] is None
 assert not reconcile(mother(),e,dict(candidate_kind='PROVISIONAL_COUNTERPART'))['relationship_committed']
 empty=adp020_select('SIM_UNIFORM_CLASSES',[],'13'*32,'G13_SCOPE')
 assert empty['status']=='SCENARIOS_VALID_EMPTY' and empty['n_draws']==0


@pytest.mark.parametrize('attack',['solo','self_owner','missing_second_action','reused_actor','wrong_history','revoked_material','future_clock'])
def test_joint_relation_source_refusals(attack):
 a,e,w,r=relation_packet();assert r['relationship_committed'] is True
 if attack=='solo':w=None
 elif attack=='self_owner':w['owner_id']=a['actor_id']
 elif attack=='missing_second_action':w['actions']=w['actions'][:1]
 elif attack=='reused_actor':w['actions'][1]['owner_id']=a['actor_id']
 elif attack=='wrong_history':w['paternal_history_hash']='sha256:'+'00'*32
 elif attack=='revoked_material':w=observe_joint_actions(a,e,material_joint_opportunity(permit=False))
 else:w=observe_joint_actions(a,e,material_joint_opportunity(effective_index=1))
 out=reconcile(a,e,dict(candidate_kind='PROVISIONAL_COUNTERPART',joint_evidence=w));OBS['joint_refusal_'+attack]=out
 assert out['status']!='COMMITTED'
 assert out['relationship_committed'] is False


def test_paternal_history_removal_suppresses_its_context_only():
 a,e,w,r=relation_packet();full=forward_continuation(a,e,r);cut=forward_continuation(a,[],r)
 assert full['paternal_continuation_admitted'] is True
 assert cut['paternal_continuation_admitted'] is False
 assert cut['maternal_continuation_admitted'] is True
 out=child_developmental_environment_fixture(a,[],cut,lab_conception_boundary())
 assert [x['actor'] for x in out['potential_material_contexts']]==[a['actor_id']]
 assert out['exposures']==[]


def test_project_removed_has_no_fixed_future():
 a,e,w,r=relation_packet();cut=[x for x in e if x['kind'] not in {'PROJECT','STRIVING','PRACTICE_FORMATION','ATTITUDE_FORMATION'}]
 out=forward_continuation(a,cut,r)
 assert out['paternal_continuation_admitted'] is False
 assert all(x['actor']!=e[0]['actors'][0] for x in out['continuation_events'])


@pytest.mark.parametrize('value',[{'future_child_outcome':'secret'},({'future_child_outcome':'secret'},),['The future child will develop a wound'],{'note':base64.b64encode(b'future child wound').decode()},{'opaque_hex':'667574757265206368696c6420776f756e64'}])
def test_unclassified_prompt_input_never_becomes_visible(value):
 t={'unknown_container':value};w={'note':value}
 p=build_proposal_prompt(mother(),t,w,value,4)
 assert 'secret' not in p and '667574757265206368696c6420776f756e64' not in p
 assert 'ZnV0dXJlIGNoaWxkIHdvdW5k' not in p
 assert json.loads(p)['boundary_status']=='HOLD_UNCLASSIFIED_INPUT'


@pytest.mark.parametrize('where',['unknown_field','assumptions','tuple','encoded_endpoint','known_id_literal','known_id_encoded','rank_object'])
def test_opaque_output_fields_hold_before_any_selection(where):
 c=deepcopy(frozen_fallback_record('M0','ROUTE_LOCAL_CLOSED').parsed_candidates[0])
 if where=='unknown_field':c['opaque']={'x':'FUTURE_CHILD_SECRET'}
 elif where=='assumptions':c['assumptions']=['The future child will develop a wound']
 elif where=='tuple':c['endpoint_constraints']['unknown']=({'opaque':'FUTURE_CHILD_SECRET'},)
 elif where=='encoded_endpoint':c['endpoint_constraints']['time_or_interval']='ZnV0dXJlIGNoaWxkIHdvdW5k'
 elif where=='known_id_literal':c['candidate_local_id']='FUTURE_CHILD_SECRET'
 elif where=='known_id_encoded':c['candidate_local_id']='ZnV0dXJlIGNoaWxkIHdvdW5k'
 else:c['plausibility_rank_ordinal']={'unclassified':'future child wound'}
 q=qualify(c,mother(),build_world(False))
 assert q['eligibility']['eligible'] is False


def test_duplicate_ids_nfc_aliases_and_permutations_refuse():
 classes=[dict(class_key='é',representative_id='A',payload='ORIGINAL'),dict(class_key='e\u0301',representative_id='B',payload='OTHER')]
 for cs in [classes,list(reversed(classes))]:
  r=adp020_select('SIM_UNIFORM_CLASSES',cs,'13'*32,'G13_SCOPE')
  assert r['status']=='DEDUP_UNDERDETERMINED' and r['n_draws']==0
 c=deepcopy(frozen_fallback_record('M0',None).parsed_candidates);c[1]['candidate_local_id']=c[0]['candidate_local_id']
 assert dedup_candidates(c)['status']=='DEDUP_UNDERDETERMINED'


def test_semantic_paraphrase_and_exact_raw_custody():
 c=deepcopy(frozen_fallback_record('M0','ROUTE_LOCAL_CLOSED').parsed_candidates[0]);alias=deepcopy(c)
 alias['candidate_local_id']='A_PARAPHRASE';alias['assumptions']=['same workplace adjacency in different wording']
 a=dedup_candidates([c]);b=dedup_candidates([alias,c]);d=dedup_candidates([c,alias])
 assert a['class_set_hash']==b['class_set_hash']==d['class_set_hash']
 assert a['classes'][0]['candidate']==b['classes'][0]['candidate']==d['classes'][0]['candidate']
 assert candidate_replay_hash(a['classes'][0])==candidate_replay_hash(b['classes'][0])
 assert len(b['classes'][0]['raw_proposals'])==2
 assert h_obj(b['classes'][0]['raw_proposals'])!=h_obj(a['classes'][0]['raw_proposals'])


def test_selected_impossible_endpoint_denies_same_terminal():
 data=inputs();good=run(deepcopy(data));assert good['terminal']['status']=='COMMITTED'
 for c in data['proposal_record'].parsed_candidates:c['endpoint_constraints']['required_state_predicates']=[dict(field='place',equals='IMPOSSIBLE_SITE')]
 bad=run(data);OBS['selected_endpoint_counterfactual']=dict(terminal=bad['terminal'],construction=bad['construction_summary'])
 assert bad['terminal']['status']=='HISTORY_SEARCH_EXHAUSTED'
 assert bad['construction_summary']['n_attempts']==4
 assert all(x['replay']['recomputed_state']['place']=='INST_WORKSHOP_A' for x in bad['construction_summary']['attempts'])
 assert all(x['endpoint_match'] is False for x in bad['construction_summary']['attempts'])


@pytest.mark.parametrize('root',[None,123,{},[],True,'13'*32+'\n','AA'*32,'short'])
def test_malformed_rng_roots_are_typed_without_draw(root):
 r=adp020_select('SIM_UNIFORM_CLASSES',[dict(class_key='A',representative_id='A'),dict(class_key='B',representative_id='B')],root,'G13_SCOPE')
 assert r['status']=='NOT_EXECUTED_AUTHORITY_HOLD' and r['n_draws']==0


def test_unissued_scope_or_stream_is_not_namespace_permission():
 with pytest.raises(RngAuthorityError):ScopedRNG('13'*32,STREAM,'UNISSUED_SCOPE').draw(7,'slot','set')
 with pytest.raises(RngAuthorityError):ScopedRNG('13'*32,'v3.causal.unissued', 'G13_SCOPE').draw(7,'slot','set')


def test_coordinate_reuse_and_tamper_refuse():
 a=adp020_select('SIM_UNIFORM_CLASSES',[dict(class_key='A',representative_id='A',payload='ORIGINAL'),dict(class_key='B',representative_id='B',payload='OTHER')],'13'*32,'G13_SCOPE')
 j=DecisionJournal();assert j.record(a)['status']=='RECORDED_RESEARCH_ONLY';assert j.record(a)['status']=='IDEMPOTENT_REPLAY'
 b=deepcopy(a);b['draw']['accepted_raw_u64']^=1
 assert replay_decision(b)['status']=='EXACT_REPLAY_DIVERGENCE'
 c=adp020_select('SIM_UNIFORM_CLASSES',[dict(class_key='A',representative_id='A',payload='CHANGED'),dict(class_key='B',representative_id='B',payload='OTHER')],'13'*32,'G13_SCOPE')
 assert j.record(c)['status']=='RNG_DRAW_COORDINATE_REUSE_CONFLICT'


def test_cold_complete_causal_replay_and_lawful_shadow_invariance(tmp_path):
 output=tmp_path/'positive.json';cold=tmp_path/'replayed.json'
 cmd=[sys.executable,'-B',str(ROOT/'candidate/run_candidate.py')]
 p=subprocess.run(cmd+['--output',str(output)],capture_output=True,text=True)
 q=subprocess.run(cmd+['--replay',str(output),'--output',str(cold)],capture_output=True,text=True)
 assert p.returncode==q.returncode==0,(p.stdout+p.stderr,q.stdout+q.stderr)
 a=json.loads(output.read_text());b=json.loads(cold.read_text())
 assert a['result']['terminal']['status']=='COMMITTED'
 assert b['complete_causal_record_equal'] is True
 assert a['result']['causal_replay_record']==b['result']['causal_replay_record']
 data=inputs();data['future_child_shadow']={'future_child_outcome':'secret'}
 shadow=run(data)
 assert shadow['causal_replay_hash']==a['result']['causal_replay_hash']
 assert NETWORK==[]


def test_original_m2_history_and_older_child_stream_are_preserved():
 packet=json.loads((ROOT/'candidate/data/frozen_maternal_archives.json').read_text());a=mother('M2')
 assert a==packet['archives']['M2']
 assert h_obj(a)==packet['expected_anchor_hashes']['M2']
 assert a['already_generated_child_refs']==['LAB_OLDER_CHILD_O1']
 prior=[e for e in a['history_events'] if e['kind'] in {'CHILD_GENERATED','CARE_ROUTINE','HOUSEHOLD_STATE'}]
 assert len(prior)==4
 assert json.loads(build_proposal_prompt(a,{}, {},None,4))['mother_anchor_visible_fields']['already_generated_child_refs']==['LAB_OLDER_CHILD_O1']



def test_joint_payment_flows_to_continuing_resources():
 a,e,w,r=relation_packet();out=forward_continuation(a,e,r)
 dad=next(x for x in out['continuation_events'] if x['actor']=='G15_PROSPECTIVE_ADULT')
 prior=replay_history(e)['state']
 assert dad['payload']['before']['cash']==prior['cash']+2
 assert dad['payload']['before']['free_hours']==prior['free_hours']-1
 assert w['actions'][1]['event_id'] in dad['causal_parent_event_ids']
 assert any(x.get('path')=='after' and x['value']['cash']==prior['cash']+2 for x in dad['payload']['values_read'])


def test_later_relationship_contact_requires_second_material_witness():
 a,e,w,r=relation_packet();material=material_joint_opportunity(effective_index=1100)
 good=forward_continuation(a,e,r,contact_material=material)
 assert good['relationship_continuation_admitted'] is True
 later=good['research_relation_continuation']
 assert later['status']=='WITNESSED'
 assert later['previous_relation_ref']==r['objective_relation']['relation_id']
 assert all(a['after']['cash']-a['before']['cash']==2 for a in later['actions'])
 bad=forward_continuation(a,e,r,contact_material=material_joint_opportunity(effective_index=1100,permit=False))
 assert bad['relationship_continuation_admitted'] is False
 assert bad['research_relation_continuation']['status']=='NO_CHANGE'
 absent=forward_continuation(a,e,r)
 assert absent['relationship_continuation_admitted'] is False
 assert absent['research_relation_continuation'] is None



def test_every_joint_and_continuation_parent_resolves_strictly_earlier():
 result=run();dag=result['dag_validation'];closure=dag['complete_event_closure'];events=closure['events']
 assert result['terminal']['status']=='COMMITTED'
 assert closure['complete_parent_closure'] is True
 assert closure['errors']==[]
 assert len(events)>len(result['anchor']['history_events'])+len(result['dad_events'])
 for edge in closure['edges']:
  assert edge['from'] in events
  assert events[edge['from']]['effective_index']<events[edge['to']]['effective_index']
 assert result['continuation']['research_relation_continuation']['status']=='WITNESSED'
 assert dag['status']=='LAB_PASS_AT_DECLARED_GRAIN'


def test_graph_rejects_missing_source_and_equal_clock():
 from lab_sgi1.dag import build_causal_graph
 e=history();good=build_causal_graph([],e,[])
 assert good['complete_parent_closure'] is True
 cut=[x for x in e if x['kind']!='WORLD_MATERIAL']
 missing=build_causal_graph([],cut,[])
 assert missing['complete_parent_closure'] is False
 assert any(x['code']=='UNRESOLVED_CAUSAL_PARENT' for x in missing['errors'])
 e[-1]['effective_index']=e[-2]['effective_index']
 tied=build_causal_graph([],e,[])
 assert tied['complete_parent_closure'] is False
 assert any(x['code']=='NONFORWARD_CAUSAL_CLOCK' for x in tied['errors'])


@pytest.mark.parametrize('bad',[{'payload':'ZnV0dXJlIGNoaWxkIHdvdW5k'},{'unknown':('hidden',)}, {'class_key':'ZnV0dXJlIGNoaWxkIHdvdW5k'}])
def test_generic_diagnostic_envelope_does_not_admit_opaque_output(bad):
 entry=dict(class_key='A',representative_id='A',payload='ORIGINAL');entry.update(bad)
 result=adp020_select('SIM_UNIFORM_CLASSES',[entry],'13'*32,'G13_SCOPE')
 assert result['status']=='NOT_EXECUTED_AUTHORITY_HOLD'
 assert result['n_draws']==0



def test_draw_receipt_full_identity_and_journal_copy_custody():
 a=ScopedRNG('13'*32,STREAM,'G13_SCOPE').draw(7,'slot','setA',0).as_dict()
 b=ScopedRNG('29'*32,STREAM,'G13_SCOPE').draw(7,'slot','setA',0).as_dict()
 c=ScopedRNG('13'*32,STREAM,'G13_SCOPE').draw(7,'slot','setA',1).as_dict()
 d=ScopedRNG('13'*32,STREAM,'G13_SCOPE').draw(7,'slot','setB',0).as_dict()
 assert len({x['receipt_id'] for x in [a,b,c,d]})==4
 assert a['accepted_raw_u64']==d['accepted_raw_u64']
 assert a['draw_replay_hash']!=d['draw_replay_hash']
 for x in [a,b,c,d]:assert x['receipt_id']==h_obj({k:v for k,v in x.items() if k!='receipt_id'})
 receipt=adp020_select('SIM_UNIFORM_CLASSES',[dict(class_key='A',representative_id='A',payload='ORIGINAL'),dict(class_key='B',representative_id='B',payload='OTHER')],'13'*32,'G13_SCOPE')
 journal=DecisionJournal();assert journal.record(receipt)['status']=='RECORDED_RESEARCH_ONLY'
 original=deepcopy(journal.records);receipt['selected_class_key']='FORGED'
 assert journal.records==original
 assert replay_decision(receipt)['status']=='EXACT_REPLAY_DIVERGENCE'


@pytest.mark.parametrize('container',[None,{},[None],('A','B')])
def test_unclassifiable_candidate_container_is_hold(container):
 r=adp020_select('SIM_UNIFORM_CLASSES',container,'13'*32,'G13_SCOPE')
 assert r['status']=='NOT_EXECUTED_AUTHORITY_HOLD'
 assert r['n_draws']==0


@pytest.mark.parametrize('material_units',[2,3,7])
def test_actual_material_values_change_formation_and_later_work(material_units):
 world=deepcopy(next(x['payload'] for x in history() if x['kind']=='WORLD_MATERIAL'));world['material_units']=material_units
 e=PersonHistoryBuilder('G15_PROSPECTIVE_ADULT','G15_RESEARCH_SEED',material=world).build()
 r=replay_history(e);p=derive_psyche(e)
 assert r['valid'] is True
 assert forward_replay_to_endpoint(e,ec())['endpoint_match'] is True
 assert p['practices'][0]['formed_value']['checks']==min(3,material_units)
 cont=forward_continuation(mother(),e,{})
 assert cont['paternal_continuation_admitted']==(material_units>3)
 if material_units>3:
  event=next(x for x in cont['continuation_events'] if x['actor']=='G15_PROSPECTIVE_ADULT')
  assert event['payload']['units_performed']==material_units-3
 else:
  assert all(x['actor']!='G15_PROSPECTIVE_ADULT' for x in cont['continuation_events'])



def test_actual_pipeline_entropy_anchor_uses_frozen_history_cut():
 result=run();receipt=result['causal_replay_record']['selected_decision_receipt']
 coordinate=receipt['draw']['entropy_coordinate'];prior=result['anchor']['history_events'][-1]
 assert result['terminal']['status']=='COMMITTED'
 assert coordinate['anchor_event_id_or_init_checkpoint_hash']==prior['event_id']
 assert coordinate['anchor_event_index']==prior['effective_index']
 assert receipt['causal_run_id']==inputs()['causal_run_id']
 assert receipt['coordinate_profile']=='G15_EXACT_HISTORY_CUT_RESEARCH_ONLY'
 assert replay_decision(receipt)['status']=='EXACT_REPLAY'



def test_selected_structure_constraints_reach_actual_replay():
 data=inputs();good=run(deepcopy(data));assert good['terminal']['status']=='COMMITTED'
 for c in data['proposal_record'].parsed_candidates:
  c['endpoint_constraints']['second_parent_structure_and_position_constraints']=['evening_class_attendee']
 bad=run(data)
 assert bad['terminal']['status']!='COMMITTED'
 assert bad['construction_summary']['n_attempts']==4
 assert all(any(m.get('reason')=='SELECTED_STRUCTURE_NOT_ENACTED' for m in a['replay']['mismatches']) for a in bad['construction_summary']['attempts'])


def test_selected_clock_rejects_otherwise_valid_late_joint_event():
 data=inputs();good=run(deepcopy(data));assert good['terminal']['status']=='COMMITTED'
 data['joint_material_opportunity']=material_joint_opportunity(effective_index=300)
 bad=run(data)
 assert bad['terminal']['status']=='ENDPOINT_INFEASIBLE'
 assert any(e['reason']=='JOINT_EVENT_OUTSIDE_SELECTED_CLOCK' for e in bad['terminal']['selected_endpoint_obligations']['errors'])
 assert bad['relation']['relationship_committed'] is True
