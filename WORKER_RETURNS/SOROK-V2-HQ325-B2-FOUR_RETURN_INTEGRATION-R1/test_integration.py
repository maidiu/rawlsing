from copy import deepcopy
from dataclasses import asdict, replace
import json
from pathlib import Path
import subprocess
import sys
import pytest
from bridge import (Bridge,ROOT,b1,p1,input_pair,capability_fixture,occurrence_witness,
                    rehash,run_two,d1_gate)


def setup(tmp_path,alternative='ALT-CARE',outcome='OCCURRED',history='recognized_plan',other=None):
    initial=b1.initialize(b1.prehistory(history))
    bridge=Bridge(tmp_path/'state.sqlite',initial)
    packet,context,policy=input_pair(initial,alternative=alternative,other=other)
    witness=occurrence_witness(initial,packet,context,alternative=alternative,outcome=outcome,other=other)
    cap,registry=capability_fixture()
    bridge.witnesses={witness['hash']:witness};bridge.capability_witnesses=registry
    return bridge,packet,context,policy,witness,cap


def registered(bridge,witness,**change):
    changed={k:v for k,v in deepcopy(witness).items() if k!='hash'};changed.update(change)
    changed=b1.sealed(changed);bridge.witnesses[changed['hash']]=changed;return changed


def test_connected_two_event_positive_vs_journal_only(tmp_path):
    positive=run_two(tmp_path/'positive');control=run_two(tmp_path/'control',True)
    first=positive['episodes'][0]['receipt'];second=positive['episodes'][1]['receipt']
    assert first['eligibility']['event_admission']=='NOT_PERFORMED'
    assert first['selection']['consumption']['no_world_or_actor_mutation']
    assert first['event_admission']['status']=='ADMITTED_SYNTHETIC_FIXTURE_ONLY'
    assert first['capability_decision']['decision']=='PROPOSABLE_ONLY'
    assert first['joint']['owner_decisions'][0]['decision']=='ALLOW'
    mediator=positive['final_state']['middle'][0]
    assert mediator['middle_state_record_hash'] in second['response']['recruited']
    assert second['response']['practical_activity']==['joint_check:caretaker']
    assert control['episodes'][1]['receipt']['response']['practical_activity']==['inspect_alone:caretaker']
    assert len(positive['final_state']['transitions'])==1
    assert control['final_state']['middle']==[]


def test_cold_replay_in_fresh_python_and_sqlite(tmp_path):
    bundle=run_two(tmp_path/'original')
    run=subprocess.run([sys.executable,str(ROOT/'bridge.py'),'replay',str(tmp_path/'original/trace.json')],
                       text=True,capture_output=True,check=True)
    replay=json.loads(run.stdout)
    assert replay['final_hash']==bundle['final_hash']
    assert replay['receipts']==[e['receipt'] for e in bundle['episodes']]


@pytest.mark.parametrize('outcome,status,reason',[('NONOCCURRENCE','VALID_EMPTY','WITNESSED_NONOCCURRENCE'),('DENIED','DENIED','OBJECTIVE_EVENT_DENIED')])
def test_eligible_alternative_can_fail_to_occur(tmp_path,outcome,status,reason):
    bridge,packet,context,policy,witness,cap=setup(tmp_path,outcome=outcome)
    before=bridge.store.state()
    receipt=bridge.advance(packet,context,policy,witness,cap)
    assert receipt['selection']['selected_candidate_id']=='ALT-CARE'
    assert receipt['status']==status and receipt['reason']==reason
    assert receipt['event_admission']=='NOT_PERFORMED'
    assert bridge.store.db.execute('SELECT count(*) FROM occurrence').fetchone()[0]==0
    assert bridge.store.state()==before


def test_p1_eligibility_alone_cannot_authenticate_witness(tmp_path):
    bridge,packet,context,policy,witness,cap=setup(tmp_path)
    bridge.witnesses={}
    receipt=bridge.advance(packet,context,policy,witness,cap)
    assert receipt['reason']=='INDEPENDENT_OCCURRENCE_WITNESS_REQUIRED'
    assert not receipt['b1_invoked'] and bridge.store.state()['middle']==[]


def test_selected_nonoccurrence_is_not_occurrence(tmp_path):
    bridge,*args=setup(tmp_path,alternative='ALT-NONE',outcome='NONOCCURRENCE')
    assert bridge.advance(*args)['status']=='VALID_EMPTY'


def test_nonoccurrence_candidate_with_forged_positive_observation_is_denied(tmp_path):
    bridge,*args=setup(tmp_path,alternative='ALT-NONE')
    assert bridge.advance(*args)['reason']=='SELECTION_WITNESS_CONTRADICTION'


@pytest.mark.parametrize('status,code',[('CAPABILITY_UNKNOWN','CAPABILITY_UNKNOWN'),('CAPABILITY_ABSENT','ABSENCE_EVIDENCE_MISSING')])
def test_unknown_and_unwitnessed_absence_defer_response(tmp_path,status,code):
    bridge,packet,context,policy,witness,cap=setup(tmp_path)
    cap['actor']['capabilities']['C07']['status']=status
    receipt=bridge.advance(packet,context,policy,witness,cap)
    assert receipt['status']=='DEFERRED' and receipt['reason']==code
    assert receipt['event_admission']['status']=='ADMITTED_SYNTHETIC_FIXTURE_ONLY'
    assert not receipt['b1_invoked'] and bridge.store.state()['middle']==[]


def test_comparable_absence_counterwitness_blocks_without_diagnosis(tmp_path):
    bridge,packet,context,policy,witness,cap=setup(tmp_path)
    record=deepcopy(bridge.capability_witnesses[0]);record.pop('hash')
    record.update(outcome='OBSERVED_INABILITY',witness_id='independent_failed_task')
    record=b1.sealed(record);bridge.capability_witnesses=[record]
    capability=cap['actor']['capabilities']['C07']
    capability.update(status='CAPABILITY_ABSENT',witness_refs=[record['hash']],counterevidence_refs=[record['hash']])
    cap['world']['witnesses']=[record['hash']]
    receipt=bridge.advance(packet,context,policy,witness,cap)
    assert receipt['reason']=='CAPABILITY_ABSENT'
    assert receipt['status']=='DENIED' and not receipt['b1_invoked']
    assert bridge.store.state()['capabilities']==['compare_enacted_plans'] # no permanent diagnosis inferred


@pytest.mark.parametrize('change,code',[
    ({'until':'2026-10-17'},'CAPABILITY_ACTOR_SCOPE_OR_TIME'),
    ({'actor':'caretaker'},'CAPABILITY_ACTOR_SCOPE_OR_TIME'),
    ({'scope':'elsewhere'},'CAPABILITY_ACTOR_SCOPE_OR_TIME'),
    ({'from':'2026-10-18'},'CAPABILITY_ACTOR_SCOPE_OR_TIME'),
    ({'witness_refs':['invented']},'INDEPENDENT_COMPARABLE_WITNESS_MISSING')])
def test_capability_scope_time_and_witness_are_real_constraints(tmp_path,change,code):
    bridge,packet,context,policy,witness,cap=setup(tmp_path)
    cap['actor']['capabilities']['C07'].update(change)
    receipt=bridge.advance(packet,context,policy,witness,cap)
    assert receipt['reason']==code and not receipt['b1_invoked']
    assert bridge.store.state()['middle']==[]


def test_false_absence_cannot_use_positive_witness(tmp_path):
    bridge,packet,context,policy,witness,cap=setup(tmp_path)
    capability=cap['actor']['capabilities']['C07'];capability['status']='CAPABILITY_ABSENT'
    capability['counterevidence_refs']=capability['witness_refs']
    assert bridge.advance(packet,context,policy,witness,cap)['reason']=='ABSENCE_COUNTERWITNESS_NOT_COMPARABLE'


def test_caps_cannot_be_omitted_to_bypass_d1(tmp_path):
    bridge,packet,context,policy,witness,cap=setup(tmp_path)
    cap['candidate']['capabilities']=[]
    assert bridge.advance(packet,context,policy,witness,cap)['reason']=='CAPABILITY_EVENT_BINDING_INVALID'


def test_conditioned_capability_requires_current_fact(tmp_path):
    bridge,packet,context,policy,witness,cap=setup(tmp_path)
    cap['actor']['capabilities']['C07'].update(status='CAPABILITY_CONDITIONED',conditions=['learned_comparison'])
    assert bridge.advance(packet,context,policy,witness,cap)['reason']=='CONDITION_UNPROVED'
    cap['actor']['current_facts']=['learned_comparison']
    # Same admitted event can be retried after separately supplied capability condition changes.
    assert bridge.advance(packet,context,policy,witness,cap)['status']=='COMMITTED'


@pytest.mark.parametrize('field',['uses_age_as_gate','private_other_state','rewrites_history'])
def test_d1_forbids_shortcuts_and_private_mind_inference(tmp_path,field):
    bridge,packet,context,policy,witness,cap=setup(tmp_path)
    cap['candidate'][field]=True
    receipt=bridge.advance(packet,context,policy,witness,cap)
    assert receipt['status']=='DENIED' and not receipt['b1_invoked']


def test_actual_peer_speech_is_attributed_without_truth_or_compulsory_uptake(tmp_path):
    bridge,packet,context,policy,witness,cap=setup(tmp_path,alternative='ALT-PEER')
    before=deepcopy(bridge.store.state()['epistemic'])
    receipt=bridge.advance(packet,context,policy,witness,cap)
    assert receipt['status']=='COMMITTED'
    assert receipt['event_admission']['attributed_claims'][0]['claim_world_fact_ref'] is None
    assert receipt['event_admission']['objective_world_facts']['known_thief'] is None
    assert receipt['event_admission']['objective_world_facts']['group_criminality']=='NOT_ESTABLISHED'
    assert receipt['response']['uptake'][0]['propositional']=='UNDECIDED_ATTRIBUTED_ASSERTION'
    assert bridge.store.state()['epistemic']==before and bridge.store.state()['middle']==[]


def test_registered_witness_cannot_launder_peer_blame_into_objective_fact(tmp_path):
    bridge,packet,context,policy,witness,cap=setup(tmp_path,alternative='ALT-PEER')
    witness=registered(bridge,witness,world_facts=dict(known_thief='a_group',group_criminality='TRUE'))
    assert bridge.advance(packet,context,policy,witness,cap)['reason']=='PEER_PREJUDICE_LAUNDERED_AS_FACT'


def test_proposition_can_be_accepted_while_affect_is_unrecognized(tmp_path):
    bridge,packet,context,policy,witness,cap=setup(tmp_path,history='imposed_plan')
    # Existing independently authorized belief, not a new belief effect inferred from speech.
    state=bridge.store.state();state['epistemic']['beliefs'].append('A careful response could reduce future loss; I am worried.')
    bridge.store.db.execute('UPDATE checkpoint SET body=? WHERE id=1',(b1.canonical(state),))
    witness=occurrence_witness(state,packet,context);bridge.witnesses={witness['hash']:witness}
    receipt=bridge.advance(packet,context,policy,witness,cap)
    assert packet['candidates'][0]['interpretations'][0]['claim'] in bridge.store.state()['epistemic']['beliefs']
    assert receipt['response']['uptake'][0]['affective']==['constrained']
    assert receipt['response']['practical_activity']==['compare_current_plan:caretaker']
    assert bridge.store.state()['middle'][0]['governed_payload']['mode']=='private_check'


@pytest.mark.parametrize('outcome,expected',[('tools_available',1),('deadline_due',0),('unavailable',0)])
def test_independent_caregiver_history_controls_actual_offered_action(tmp_path,outcome,expected):
    bridge,*args=setup(tmp_path,other={'CARE-1':b1.participant(outcome=outcome)})
    receipt=bridge.advance(*args)
    assert receipt['status']=='COMMITTED'
    assert len(bridge.store.state()['middle'])==expected


def test_forged_other_action_not_accepted_even_if_registered(tmp_path):
    bridge,packet,context,policy,witness,cap=setup(tmp_path)
    facts=deepcopy(witness['other_actions']);facts[0]['action']='secure_alone'
    witness=registered(bridge,witness,other_actions=facts)
    assert bridge.advance(packet,context,policy,witness,cap)['reason']=='INDEPENDENT_ACTOR_ACTION_FORGED'


def test_focal_child_history_cannot_become_caregiver_history(tmp_path):
    bridge,packet,context,policy,witness,cap=setup(tmp_path)
    facts=deepcopy(witness['other_actions']);person=facts[0]['participant']
    person['history'][0]['actor_id']='child'
    facts[0]['source_history_hash']=b1.digest(person)
    witness=registered(bridge,witness,other_actions=facts)
    assert bridge.advance(packet,context,policy,witness,cap)['reason']=='INDEPENDENT_ACTOR_HISTORY_FORGED'


@pytest.mark.parametrize('fault,grant,reason',[('after_checkpoint',True,'INJECTED_STORAGE_FAILURE'),(None,False,'FOREIGN_OWNER_PERMISSION_DENIED')])
def test_target_rollback_preserves_objective_admission(tmp_path,fault,grant,reason):
    bridge,*args=setup(tmp_path);before=bridge.store.state()
    receipt=bridge.advance(*args,fault=fault,grant=grant)
    assert receipt['joint']['reason']==reason and receipt['status']=='TRANSACTION_ABORTED_ROLLBACK'
    assert bridge.store.state()==before
    assert bridge.store.db.execute('SELECT count(*) FROM occurrence').fetchone()[0]==1
    assert bridge.store.db.execute('SELECT count(*) FROM joint_receipt').fetchone()[0]==0
    bridge.close();reopened=Bridge(tmp_path/'state.sqlite')
    assert reopened.store.state()==before


def test_stale_witness_cannot_be_rebound_to_new_actor_history(tmp_path):
    bridge,*args=setup(tmp_path)
    assert bridge.advance(*args)['status']=='COMMITTED'
    before=bridge.store.state()
    assert bridge.advance(*args)['reason']=='WITNESS_BINDING_OR_STALE_STATE'
    assert bridge.store.state()==before


def test_model_possible_effects_never_directly_update_owner(tmp_path):
    bridge,packet,context,policy,witness,cap=setup(tmp_path)
    for candidate in packet['candidates']:
        for effect in candidate['possible_effects']:effect['description']='force global trust forever'
    packet=rehash(packet,'proposal_hash')
    ev=p1.evaluate(packet,context);policy['candidate_set_hash']=ev['candidate_set_hash'];policy=rehash(policy,'policy_hash')
    witness=occurrence_witness(bridge.store.state(),packet,context);bridge.witnesses={witness['hash']:witness}
    receipt=bridge.advance(packet,context,policy,witness,cap)
    assert receipt['status']=='COMMITTED'
    payload=bridge.store.state()['middle'][0]['governed_payload']
    assert payload['mode']=='joint_check' and 'trust' not in json.dumps(payload)


def test_actor_safe_output_excludes_hidden_history_and_other_private_data(tmp_path):
    bridge,*args=setup(tmp_path)
    result=bridge.advance(*args)
    safe=json.dumps(result['actor_safe'])
    assert result['actor_safe']['origin_explanation']=='NOT_ACCESSIBLE'
    for secret in ['shared_task','caregiver-private','UNREADABLE_CAREGIVER_CONCERN','source_history_hash','recognized_plan']:
        assert secret not in safe
    assert bridge.store.state()['epistemic']['inaccessible']==['shared_task']


def test_historical_binding_mismatch_rejected_by_actual_p1(tmp_path):
    bridge,packet,context,policy,witness,cap=setup(tmp_path)
    context['people']['CHILD-1']['history_ref']='H-CHILD-2'
    context=rehash(context,'context_hash');packet['context_hash']=context['context_hash'];packet=rehash(packet,'proposal_hash')
    evaluation=p1.evaluate(packet,context)
    assert not any(e['candidate_id']=='ALT-CARE' for e in evaluation['eligible_entries'])
    receipt=bridge.advance(packet,context,policy,witness,cap)
    assert not receipt['b1_invoked'] and bridge.store.state()['middle']==[]


def test_private_fact_cannot_become_p1_world_prerequisite(tmp_path):
    bridge,packet,context,policy,witness,cap=setup(tmp_path)
    packet['candidates'][0]['prerequisites'].append(dict(kind='WORLD_FACT_TRUE',ref='PRIVATE-CAREGIVER-1'))
    packet=rehash(packet,'proposal_hash')
    receipt=bridge.advance(packet,context,policy,witness,cap)
    assert not receipt['b1_invoked'] and receipt['event_admission']=='NOT_PERFORMED'


def test_probability_policy_is_test_only_and_outside_model(tmp_path):
    bridge,*args=setup(tmp_path)
    result=bridge.advance(*args)
    assert result['selection']['rng_receipt']['probability_grade']=='PROVISIONAL_NOT_CALIBRATED'
    assert result['selection']['rng_receipt']['algorithm']=='ADP020_COMPATIBILITY_MOCK_TEST_ONLY'
    assert result['joint']['rng_draws']==0


def test_model_changed_utterance_is_not_automatically_witnessed(tmp_path):
    bridge,packet,context,policy,witness,cap=setup(tmp_path)
    packet['candidates'][0]['interpretations'][0]['utterance']='The model invented a different speech.'
    packet=rehash(packet,'proposal_hash');evaluation=p1.evaluate(packet,context)
    policy['candidate_set_hash']=evaluation['candidate_set_hash'];policy=rehash(policy,'policy_hash')
    witness=occurrence_witness(bridge.store.state(),packet,context)
    bridge.witnesses={witness['hash']:witness}
    result=bridge.advance(packet,context,policy,witness,cap)
    assert result['reason']=='UTTERANCE_NOT_INDEPENDENTLY_WITNESSED'
    assert result['event_admission']=='NOT_PERFORMED'


def test_context_cannot_claim_an_unrelated_typed_child_history(tmp_path):
    bridge,packet,context,policy,witness,cap=setup(tmp_path)
    context['histories']['H-CHILD-1']['summary']='typed history digest invented'
    context=rehash(context,'context_hash');packet['context_hash']=context['context_hash'];packet=rehash(packet,'proposal_hash')
    evaluation=p1.evaluate(packet,context);policy['candidate_set_hash']=evaluation['candidate_set_hash'];policy=rehash(policy,'policy_hash')
    witness=occurrence_witness(bridge.store.state(),packet,context);bridge.witnesses={witness['hash']:witness}
    assert bridge.advance(packet,context,policy,witness,cap)['reason']=='CONDITIONING_HISTORY_PROJECTION_MISMATCH'


def test_seed_policy_choice_never_overrides_a_different_occurrence_witness(tmp_path):
    bridge,packet,context,policy,witness,cap=setup(tmp_path)
    policy['weight_units']={key:int(key=='ALT-PEER') for key in policy['weight_units']}
    policy=rehash(policy,'policy_hash')
    result=bridge.advance(packet,context,policy,witness,cap)
    assert result['selection']['selected_candidate_id']=='ALT-PEER'
    assert result['reason']=='WITNESS_BINDING_OR_STALE_STATE'


def test_capability_cannot_promote_hidden_history_to_conscious_access(tmp_path):
    bridge,packet,context,policy,witness,cap=setup(tmp_path)
    cap['actor']['access'].append('shared_task')
    assert bridge.advance(packet,context,policy,witness,cap)['reason']=='CAPABILITY_EVENT_BINDING_INVALID'


def test_selection_defer_is_not_mislabeled_as_event_admission(tmp_path):
    bridge,*args=setup(tmp_path)
    result=bridge.advance(*args,seed='')
    assert result['selection']['decision']=='DEFER'
    assert result['status']=='DEFERRED' and result['event_admission']=='NOT_PERFORMED'


def test_no_actor_safe_actions_published_after_target_rollback(tmp_path):
    bridge,*args=setup(tmp_path)
    result=bridge.advance(*args,grant=False)
    assert result['status']=='TRANSACTION_ABORTED_ROLLBACK'
    assert result['actor_safe']['actions']==[] and result['actor_safe']['status']=='RESPONSE_ABORTED'


def test_proposal_cannot_supply_a_canonical_target_update(tmp_path):
    bridge,packet,context,policy,witness,cap=setup(tmp_path)
    packet['candidates'][0]['CAN011_update']={'mode':'global_trust'}
    packet=rehash(packet,'proposal_hash')
    result=bridge.advance(packet,context,policy,witness,cap)
    assert result['eligibility']['decision']=='REJECT'
    assert not result['b1_invoked'] and result['event_admission']=='NOT_PERFORMED'


def test_p1_wrong_clock_blocks_before_witness_or_b1(tmp_path):
    bridge,packet,context,policy,witness,cap=setup(tmp_path)
    packet['candidates'][0]['time']='2027-01-01T10:00:00Z';packet=rehash(packet,'proposal_hash')
    result=bridge.advance(packet,context,policy,witness,cap)
    assert not result['b1_invoked'] and result['event_admission']=='NOT_PERFORMED'
