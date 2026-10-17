"""Frozen-author P1 synthetic hostile court. No live model, no CAN/ADP owner import."""
from __future__ import annotations
import copy, hashlib, json
from pathlib import Path
import pytest
from p1_contract import evaluate,select_test_only,replay_test_only,digest,PROB_GRADE,RNG_GRADE
F=Path(__file__).resolve().parents[1]/'fixtures'
SEED='0f'*32

def f(name):return json.loads((F/name).read_text())
def packet():return f('packet_base.json')
def ctx():return f('context_base.json')
def policy():return f('policy_design_weights.json')
def rehash(p):p['proposal_hash']=digest({k:v for k,v in p.items() if k!='proposal_hash'});return p
def refresh_context(c):c['context_hash']=digest({k:v for k,v in c.items() if k!='context_hash'});return c
def modify_candidate(fn):
 p=packet();fn(p['candidates'][0]);return rehash(p)
def code_for(result,cid):return next(d['code'] for d in result['candidates'] if d['candidate_id']==cid)

def test_base_has_four_distinct_possible_actions_or_nonoccurrence():
 r=evaluate(packet(),ctx());assert r['decision']=='ADMIT';assert len(r['eligible_entries'])==4
 assert sorted(x['candidate_id'] for x in r['eligible_entries'])==['ALT-CARE','ALT-CHILD-SEARCH','ALT-NONE','ALT-PEER']
 assert r['event_admission']=='NOT_PERFORMED' and r['consumption'] is None

def test_prejudicial_peer_statement_is_only_attributed_not_truth():
 p=packet(); a=next(x for x in p['candidates'] if x['candidate_id']=='ALT-PEER')
 assert a['interpretations'][0]['claim_kind']=='ATTRIBUTED_UNVERIFIED_ASSERTION'
 assert a['interpretations'][0]['claim_world_fact_ref'] is None
 assert ctx()['facts']['THEFT-1']['known_culprit'] is None
 assert code_for(evaluate(p,ctx()),'ALT-PEER')=='PROPOSAL_CANDIDATE_ONLY_NOT_CAUSAL'

def test_two_histories_change_eligibility_without_predestining_development():
 a=evaluate(packet(),ctx());b=evaluate(f('packet_changed_histories.json'),f('context_changed_histories.json'))
 assert code_for(a,'ALT-CARE')=='PROPOSAL_CANDIDATE_ONLY_NOT_CAUSAL'
 assert code_for(b,'ALT-CARE')=='HISTORY_BINDING_FALSE'
 assert 'ALT-PEER' in [x['candidate_id'] for x in b['eligible_entries']]
 assert a['candidate_set_hash']!=b['candidate_set_hash']
 assert a['consumption']==b['consumption']==None

def test_alternative_control_history_belongs_to_same_distinct_person():
 c=f('context_changed_histories.json')
 r=evaluate(f('packet_control_history.json'),c)
 assert r['decision']=='ADMIT'; assert 'ALT-CARE-CONTROL' in [e['candidate_id'] for e in r['eligible_entries']]
 assert c['people']['CHILD-1']['history_ref'] != ctx()['people']['CHILD-1']['history_ref']
 assert c['people']['CARE-1']['history_ref'] != ctx()['people']['CARE-1']['history_ref']

def test_peer_not_exposed_refuses_proposed_speech_grounded_in_private_knowledge():
 r=evaluate(f('packet_changed_peer.json'),f('context_peer_not_exposed.json'))
 assert code_for(r,'ALT-PEER')=='ACTOR_VISIBILITY_UNSUPPORTED'
 assert r['decision']=='ADMIT' and len(r['eligible_entries'])==3

def test_actual_theft_not_guaranteed_by_model_packet():
 r=evaluate(f('packet_no_theft.json'),f('context_no_theft.json'))
 assert r['decision']=='VALID_EMPTY' and all(x['decision']=='REJECT' for x in r['candidates'])

def test_empty_packet_is_valid_empty_with_zero_rng_and_no_fallback():
 r=evaluate(f('packet_valid_empty.json'),ctx());assert r['decision']=='VALID_EMPTY';assert r['eligible_entries']==[]
 s=select_test_only(r,policy(),seed_hex=SEED,coordinate=0)
 assert s['selected_candidate_id'] is None and s['consumption'] is None and not s['draw_consumed']

def test_nonoccurrence_as_explicit_possible_outcome_not_pseudoevent():
 r=evaluate(f('packet_explicit_nonoccurrence.json'),ctx())
 assert r['decision']=='ADMIT' and [x['candidate_id'] for x in r['eligible_entries']]==['ALT-NONE']
 pol=policy();pol['candidate_set_hash']=r['candidate_set_hash'];pol['weight_units']={'ALT-NONE':5};pol['policy_hash']=digest({k:v for k,v in pol.items() if k!='policy_hash'})
 s=select_test_only(r,pol,seed_hex=SEED,coordinate=3)
 assert s['selected_candidate_id']=='ALT-NONE' and not s['draw_consumed']
 assert s['consumption']['event_admission']=='NOT_PERFORMED' and s['consumption']['no_world_or_actor_mutation']

def test_order_independent_set_and_choice():
 a=evaluate(packet(),ctx());b=evaluate(f('packet_order_reversed.json'),ctx())
 assert a['candidate_set_hash']==b['candidate_set_hash']
 sa=select_test_only(a,policy(),seed_hex=SEED,coordinate=5)
 sb=select_test_only(b,policy(),seed_hex=SEED,coordinate=5)
 assert sa['selected_candidate_id']==sb['selected_candidate_id']
 assert sa['replay_identity']==sb['replay_identity']

def test_immutable_repeat_replay_same_inputs():
 r=evaluate(packet(),ctx());s=select_test_only(r,policy(),seed_hex=SEED,coordinate=41)
 assert s==select_test_only(r,policy(),seed_hex=SEED,coordinate=41)
 assert s==replay_test_only(s,r,policy(),seed_hex=SEED,coordinate=41)
 assert s['rng_receipt']['algorithm']==RNG_GRADE
 assert s['rng_receipt']['probability_grade']==PROB_GRADE

def test_wrong_seed_replay_refuses():
 r=evaluate(packet(),ctx());s=select_test_only(r,policy(),seed_hex=SEED,coordinate=19)
 assert replay_test_only(s,r,policy(),seed_hex='01'*32,coordinate=19)['reason']=='TEST_ONLY_REPLAY_DIVERGENCE'

def test_changed_draw_coordinate_is_named_and_replay_diverges():
 r=evaluate(packet(),ctx());s=select_test_only(r,policy(),seed_hex=SEED,coordinate=19)
 assert replay_test_only(s,r,policy(),seed_hex=SEED,coordinate=20)['reason']=='TEST_ONLY_REPLAY_DIVERGENCE'

def test_changed_candidate_set_requires_new_policy_contract():
 r=evaluate(f('packet_changed_peer.json'),f('context_peer_not_exposed.json'))
 assert select_test_only(r,policy(),seed_hex=SEED,coordinate=1)['reason']=='CANDIDATE_SET_DIVERGENCE'

def test_causal_claims_from_selected_outcome_remain_zero():
 p=packet();c=ctx(); before=(digest(p),digest(c))
 s=select_test_only(evaluate(p,c),policy(),seed_hex=SEED,coordinate=4)
 assert s['consumption']['response_effect_proposals']==[]
 assert s['consumption']['target_CAN011_update_proposals']==[]
 assert s['consumption']['actor_response_rule_ref'] is None
 assert s['consumption']['event_admission']=='NOT_PERFORMED'
 assert (digest(p),digest(c))==before

def test_no_actor_world_history_mutation_across_many_draws():
 p=packet();c=ctx();freeze=(copy.deepcopy(p),copy.deepcopy(c))
 r=evaluate(p,c)
 for i in range(50): select_test_only(r,policy(),seed_hex=SEED,coordinate=i)
 assert (p,c)==freeze

@pytest.mark.parametrize('bad', ['world_state','state_delta','actor_delta','CAN011_update','belief_delta','history_delta','cursor_after','actual_culprit','probability'])
def test_owner_mutation_or_fabricated_truth_refused_even_when_rehashed(bad):
 p=packet();p['candidates'][0][bad]={'force':'real'}
 r=evaluate(rehash(p),ctx())
 assert r['decision']=='REJECT';assert 'FORBIDDEN_OWNER_FIELD' in r['detail']

@pytest.mark.parametrize('method', ['missing_hash','corrupt_hash','missing_prompt','wrong_context','epistemic','unknown_key'])
def test_packet_provenance_and_authority_fail_closed(method):
 p=packet()
 if method=='missing_hash':p.pop('proposal_hash')
 elif method=='corrupt_hash':p['proposal_hash']='0'*64
 elif method=='missing_prompt':p['model']['prompt_sha256']=None;p=rehash(p)
 elif method=='wrong_context':p['context_hash']='1'*64;p=rehash(p)
 elif method=='epistemic':p['epistemic_class']='GENERATED_RUNTIME_FACT';p=rehash(p)
 elif method=='unknown_key':p['status']='ADMITTED';p=rehash(p)
 assert evaluate(p,ctx())['decision']=='REJECT'

def test_same_proposal_id_changed_content_collision_not_accepted():
 p=packet();p['candidates'][0]['uncertainty']='completely changed';rehash(p)
 old=packet()
 r=evaluate(p,ctx(),prior_proposals={old['proposal_id']:old['proposal_hash']})
 assert r['decision']=='REJECT' and 'INVALID_PROPOSAL_ID_CONTENT_COLLISION' in r['detail']

def test_idempotent_same_proposal_id_hash_registry_valid():
 p=packet()
 assert evaluate(p,ctx(),prior_proposals={p['proposal_id']:p['proposal_hash']})==evaluate(p,ctx())

def test_duplicate_candidate_identity_fails_packet():
 p=packet();p['candidates'].append(copy.deepcopy(p['candidates'][0]));rehash(p)
 assert 'DUPLICATE_CANDIDATE_ID' in evaluate(p,ctx())['detail']

def test_unknown_participant_does_not_create_independent_actor():
 p=modify_candidate(lambda c:c['participants'].append('FAKE-PERSON'))
 assert code_for(evaluate(p,ctx()),'ALT-CARE')=='FABRICATED_PARTICIPANT'

def test_missing_actor_action_opportunity_yields_defer():
 p=modify_candidate(lambda c:c['action_refs'][0].update(opportunity_ref='OP-DOES-NOT-EXIST'))
 assert code_for(evaluate(p,ctx()),'ALT-CARE')=='ACTION_OPPORTUNITY_UNRESOLVED'
 assert evaluate(p,ctx())['decision']=='DEFER'
 assert select_test_only(evaluate(p,ctx()),policy(),seed_hex=SEED,coordinate=1)['consumption'] is None

def test_unregistered_prerequisite_cannot_be_soft_scored():
 p=modify_candidate(lambda c:c['prerequisites'].append({'kind':'MAKE_IT_TRUE','ref':'THEFT-1'}))
 assert code_for(evaluate(p,ctx()),'ALT-CARE')=='UNREGISTERED_PREREQUISITE_RULE'

def test_unreadable_caregiver_private_state_cannot_enter_readset():
 p=modify_candidate(lambda c:c['readset'].append('PRIVATE-CAREGIVER-1'))
 assert code_for(evaluate(p,ctx()),'ALT-CARE')=='CLAIM_AS_OBJECTIVE_WORLD_FACT'

def test_false_peer_claim_cannot_be_reified_as_culprit_fact():
 p=packet();p['candidates'][1]['interpretations'][0]['claim_world_fact_ref']='THEFT-1';rehash(p)
 assert code_for(evaluate(p,ctx()),'ALT-PEER')=='CLAIM_LAUNDERED_INTO_OBJECTIVE_FACT'

def test_false_peer_claim_provenance_hidden_fact_fails():
 p=packet();p['candidates'][1]['interpretations'][0]['accessible_source_refs']=['PRIVATE-CAREGIVER-1'];rehash(p)
 assert code_for(evaluate(p,ctx()),'ALT-PEER')=='SPEAKER_PRIVATE_KNOWLEDGE_FORGED'

def test_disallowed_long_term_effect_kind_refused():
 p=modify_candidate(lambda c:c['possible_effects'][0].update(effect_kind='LIFELONG_FIXED_TRAIT'))
 assert code_for(evaluate(p,ctx()),'ALT-CARE')=='UNREGISTERED_DURABLE_EFFECT'

def test_effect_owner_forgery_refused():
 p=modify_candidate(lambda c:c['possible_effects'][0].update(owner_required='MODEL_IS_OWNER'))
 assert code_for(evaluate(p,ctx()),'ALT-CARE')=='DIRECT_PSYCHIC_MUTATION_FORBIDDEN'

def test_cross_person_unbound_effect_refused():
 p=modify_candidate(lambda c:c['possible_effects'][0].update(target_actor_ref='NEIGHBOR-1'))
 assert code_for(evaluate(p,ctx()),'ALT-CARE')=='FOREIGN_ACTOR_EFFECT'

def test_retrospective_event_proposal_rejected():
 p=modify_candidate(lambda c:c.update(time='2026-10-16T00:00:00Z'))
 assert code_for(evaluate(p,ctx()),'ALT-CARE')=='RETROACTIVE_OR_FUTURE_UNWITNESSED_EVENT'

def test_material_prerequisite_false_refuses_without_comforting_story():
 p=modify_candidate(lambda c:c['prerequisites'].append({'kind':'MATERIAL_AFFORDANCE','ref':'FAKE_KEY'}))
 assert code_for(evaluate(p,ctx()),'ALT-CARE')=='MATERIAL_PREREQUISITE_FALSE'

def test_model_cannot_invent_permission_through_narrative():
 p=modify_candidate(lambda c:c['action_refs'][0].update(actor_ref='CHILD-1'))
 assert code_for(evaluate(p,ctx()),'ALT-CARE')=='ACTION_OPPORTUNITY_MISMATCH'

def test_malformed_context_fails_before_candidate_evaluation():
 c=ctx();c['facts']['THEFT-1']['occurred']=False
 assert evaluate(packet(),c)['decision']=='REJECT' # context hash mismatch, not a new historical truth

def test_policy_without_authored_provenance_refused():
 pol=policy();pol['parameter_source']='LLM_CONFIDENCE';pol['policy_hash']=digest({k:v for k,v in pol.items() if k!='policy_hash'})
 assert select_test_only(evaluate(packet(),ctx()),pol,seed_hex=SEED,coordinate=0)['reason']=='NUMERIC_AUTHORITY_NOT_GRANTED'

def test_missing_or_extra_weights_refused_no_default():
 pol=policy();pol['weight_units'].pop('ALT-NONE');pol['policy_hash']=digest({k:v for k,v in pol.items() if k!='policy_hash'})
 assert select_test_only(evaluate(packet(),ctx()),pol,seed_hex=SEED,coordinate=0)['reason']=='UNLICENSED_OR_INCOMPLETE_WEIGHT_UNITS'

def test_negative_weight_refused_not_normalized():
 pol=policy();pol['weight_units']['ALT-PEER']=-1;pol['policy_hash']=digest({k:v for k,v in pol.items() if k!='policy_hash'})
 assert select_test_only(evaluate(packet(),ctx()),pol,seed_hex=SEED,coordinate=0)['reason']=='UNLICENSED_OR_INCOMPLETE_WEIGHT_UNITS'

def test_all_zero_weights_valid_empty_no_draw():
 pol=policy();pol['weight_units']={k:0 for k in pol['weight_units']};pol['policy_hash']=digest({k:v for k,v in pol.items() if k!='policy_hash'})
 r=select_test_only(evaluate(packet(),ctx()),pol,seed_hex=SEED,coordinate=0)
 assert r['decision']=='VALID_EMPTY' and not r['draw_consumed'] and r['selected_candidate_id'] is None

def test_missing_seed_refuses_not_environment_default():
 assert select_test_only(evaluate(packet(),ctx()),policy(),seed_hex='',coordinate=0)['reason']=='SEED_OR_COORDINATE_MISSING'

def test_corrupt_policy_digest_detected():
 pol=policy();pol['weight_units']['ALT-CARE']=999
 assert select_test_only(evaluate(packet(),ctx()),pol,seed_hex=SEED,coordinate=0)['reason']=='SELECTION_POLICY_HASH_MISMATCH'

def test_frozen_fixture_files_are_valid_json_and_content_hashes():
 for path in sorted(F.glob('*.json')):
  assert isinstance(json.loads(path.read_text()),dict)
  assert json.loads(path.read_text()) == json.loads(json.dumps(json.loads(path.read_text())))


def test_prospective_person_is_recognized_but_requires_separate_history_owner():
 p=f('packet_prospective_person.json');before=copy.deepcopy(ctx())
 r=evaluate(p,ctx())
 assert r['decision']=='DEFER'
 assert code_for(r,'ALT-PROSPECTIVE-NEW-CAREGIVER')=='PROSPECTIVE_PERSON_AND_HISTORY_OWNER_REQUIRED'
 assert r['consumption'] is None and ctx()==before

def test_prospective_person_cannot_forge_an_admitted_actor():
 p=f('packet_prospective_person.json')
 p['candidates'][0]['prospective_participants'][0]['epistemic_class']='GENERATED_RUNTIME_FACT';rehash(p)
 assert code_for(evaluate(p,ctx()),'ALT-PROSPECTIVE-NEW-CAREGIVER')=='PROSPECTIVE_PERSON_LAUNDERED_AS_FACT'

def test_unknown_prospective_role_ref_is_rejected():
 p=f('packet_prospective_person.json')
 p['candidates'][0]['prospective_participants'][0]['role_ref']='SOVEREIGN_UNREGISTERED_ROLE';rehash(p)
 assert code_for(evaluate(p,ctx()),'ALT-PROSPECTIVE-NEW-CAREGIVER')=='UNKNOWN_PROSPECTIVE_ROLE'

def test_prospective_person_requires_independent_history_ref():
 p=f('packet_prospective_person.json')
 p['candidates'][0]['prospective_participants'][0]['independent_history_ref']=None;rehash(p)
 assert code_for(evaluate(p,ctx()),'ALT-PROSPECTIVE-NEW-CAREGIVER')=='BAD_PROSPECTIVE_PERSON_REFS'

def test_utterance_requires_proposed_speaker_action_opportunity():
 p=packet()
 p['candidates'][0]['interpretations'][0]['speaker_actor_ref']='CHILD-1'
 rehash(p)
 assert code_for(evaluate(p,ctx()),'ALT-CARE')=='UNAUTHORIZED_INTERPRETIVE_SPEECH'

def test_empty_action_for_proposed_utterance_is_not_rescued_by_narrative():
 p=modify_candidate(lambda c:c['action_refs'].clear())
 assert code_for(evaluate(p,ctx()),'ALT-CARE')=='NO_INDEPENDENT_ACTION_OPPORTUNITY'

def test_visible_participant_without_knowledge_grant_is_refused():
 p=packet();p['candidates'][0]['participants'].append('NEIGHBOR-1')
 p['candidates'][0]['visibility'].append('NEIGHBOR-1');rehash(p)
 assert code_for(evaluate(p,ctx()),'ALT-CARE')=='ACTOR_VISIBILITY_UNSUPPORTED'

def test_future_fact_as_known_past_is_rejected():
 c=ctx();c['facts']['THEFT-1']['time']='2027-01-01T00:00:00Z';refresh_context(c)
 p=packet();p['context_hash']=c['context_hash'];rehash(p)
 assert code_for(evaluate(p,c),'ALT-CARE')=='FUTURE_EVIDENCE_AS_PAST_FACT'

def test_candidate_content_change_changes_set_identity():
 p=packet();p['candidates'][0]['possible_effects'][0]['description']='Different hypothetical effect, not an admitted one'
 rehash(p)
 original=evaluate(packet(),ctx());changed=evaluate(p,ctx())
 assert changed['decision']=='ADMIT'
 assert changed['candidate_set_hash']!=original['candidate_set_hash']
 assert select_test_only(changed,policy(),seed_hex=SEED,coordinate=1)['reason']=='CANDIDATE_SET_DIVERGENCE'

def test_nonoccurrence_receives_no_forced_psychological_lesson():
 r=evaluate(f('packet_explicit_nonoccurrence.json'),ctx())
 assert r['eligible_entries'][0]['candidate_id']=='ALT-NONE'
 p=f('packet_explicit_nonoccurrence.json')
 assert p['candidates'][0]['possible_effects']==[]
 assert p['candidates'][0]['courses']==[]

def test_many_seeds_demonstrate_non_first_selection_without_calibration_claim():
 r=evaluate(packet(),ctx());seen=set()
 for i in range(100):
  seed=hashlib.sha256(f'fixture-seed-{i}'.encode()).hexdigest()
  d=select_test_only(r,policy(),seed_hex=seed,coordinate=0)
  seen.add(d['selected_candidate_id'])
  assert d['rng_receipt']['probability_grade']==PROB_GRADE
 assert 'ALT-NONE' in seen and len(seen)>=3

def test_tampered_selected_candidate_replay_receipt_fails():
 r=evaluate(packet(),ctx());s=select_test_only(r,policy(),seed_hex=SEED,coordinate=4)
 tampered=copy.deepcopy(s);tampered['selected_candidate_id']='ALT-FAKE'
 assert replay_test_only(tampered,r,policy(),seed_hex=SEED,coordinate=4)['reason']=='TEST_ONLY_REPLAY_DIVERGENCE'


def test_cli_runs_sourcefree_without_owner_dependency():
 import subprocess,sys
 root=Path(__file__).resolve().parents[1]
 p=subprocess.run([sys.executable,str(root/'run_demo.py')],cwd=root,capture_output=True,text=True,check=True)
 doc=json.loads(p.stdout)
 assert doc['evaluation']['decision']=='ADMIT'
 assert doc['selection']['decision']=='ADMIT'
 assert doc['selection']['consumption']['no_world_or_actor_mutation'] is True
