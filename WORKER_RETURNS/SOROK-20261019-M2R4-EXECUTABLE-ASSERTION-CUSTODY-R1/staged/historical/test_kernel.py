from dataclasses import replace, asdict
from copy import deepcopy
import pytest
from kernel import (seed_scene, State, eligible, propose, append_test_only, fixture_grant,
                    validate, digest, Refusal, Candidate, RULE_HASH)


def start(scene=None):
    scene=scene or seed_scene()
    return scene,State('child',procedure_refs=('old_watchful_habit',))


def choose(scene,state,event='loss',mode='RECONSIDER',stance='ACCEPT',source='parent_said',**kw):
    c=next(c for c in eligible(scene,state,event) if c.mode==mode and c.stance==stance and c.source==source)
    p=propose(scene,state,event,c.id,**kw)
    s=append_test_only(scene,state,p,fixture_grant(p,state.actor))
    return s,p


def test_four_independent_actors_with_histories():
    scene,_=start(); assert len(scene.actors)==4
    assert all(a.history and all(h.actor==a.id for h in a.history) for a in scene.actors)


def test_objective_theft_has_no_culprit_or_ideology():
    scene,_=start(); e=scene.events[0]
    assert e.kind=='LOSS' and 'thief' not in str(asdict(e)) and 'ideology' not in str(asdict(e))


def test_every_accessible_speech_has_multiple_competing_stances():
    scene,state=start(); c=eligible(scene,state,'loss')
    assert {(x.source,x.stance) for x in c if x.mode=='RECONSIDER'}=={(s,mode) for s in ('parent_said','peer_said') for mode in ('ACCEPT','REJECT','SUSPEND')}
    assert any(x.mode=='NO_CHANGE' for x in c)


def test_peer_attribution_never_world_culprit():
    scene,state=start(); new,p=choose(scene,state,source='peer_said')
    assert new.lineage[-1].source=='peer_said' and 'culprit' not in str(scene.events[0].material)
    assert p['possible_owner_effect']=='CAN011_OR_ADP016_017_UNISSUED'


def test_unheard_peer_cannot_influence_candidates():
    scene,state=start(seed_scene(child_access_peer=False))
    assert not any(c.source=='peer_said' for c in eligible(scene,state,'loss'))


def test_missing_peer_speech_cannot_influence_candidates():
    scene,state=start(seed_scene(peer_speech=False))
    assert not any(c.source=='peer_said' for c in eligible(scene,state,'loss'))


def test_changed_child_history_changes_eligible_witnessed_prior_but_not_fixed_output():
    a,s=start(seed_scene(child_history='cooperative'));b,t=start(seed_scene(child_history='threatened'))
    assert a.events[0]==b.events[0] and a.speech[0]==b.speech[0]
    ca={x.id for x in eligible(a,s,'loss') if x.mode=='PROCEDURAL_RECRUITMENT'}
    cb={x.id for x in eligible(b,t,'loss') if x.mode=='PROCEDURAL_RECRUITMENT'}
    assert ca and cb and ca!=cb
    assert {(x.source,x.stance) for x in eligible(a,s,'loss') if x.mode=='RECONSIDER'}=={(x.source,x.stance) for x in eligible(b,t,'loss') if x.mode=='RECONSIDER'}


def test_parent_private_care_history_changes_without_automatic_child_belief():
    a,s=start(seed_scene(parent_history='care_work'));b,t=start(seed_scene(parent_history='overtime'))
    assert a.events==b.events and a.speech==b.speech
    assert eligible(a,s,'loss')==eligible(b,t,'loss')
    assert a.actors[1].history!=b.actors[1].history


def test_factual_acceptance_and_negative_affect_are_independent():
    scene,state=start();state,p=choose(scene,state,stance='ACCEPT',affect_ref='first_distress',public_action_ref='public_lock_check')
    x=state.lineage[-1]
    assert x.belief_stance=='ACCEPT' and x.affect_ref=='first_distress' and x.public_action_ref=='public_lock_check'
    assert x.actor_memory_access=='NOT_GRANTED'


def test_private_rejection_and_public_conformity_do_not_collapse():
    scene,state=start();state,_=choose(scene,state,stance='REJECT',source='peer_said',public_action_ref='public_lock_check')
    assert state.lineage[-1].belief_stance=='REJECT' and state.lineage[-1].public_action_ref=='public_lock_check'


def test_procedural_watchfulness_survives_explicit_rejection():
    scene,state=start();s,_=choose(scene,state,source='parent_said',stance='REJECT')
    assert s.procedure_refs==('old_watchful_habit',)
    assert s.lineage[-1].retained_procedure_refs==('old_watchful_habit',)


@pytest.mark.parametrize('later_mode',('REATTRIBUTE','NARROW','GENERALIZE','REINFORCE','CONTRADICT','DIFFERENTIATE','NO_CHANGE'))
def test_seven_later_alternatives_are_only_candidates(later_mode):
    scene,state=start();state,_=choose(scene,state)
    c=eligible(scene,state,'later')
    assert any(x.mode==later_mode for x in c)
    assert len(state.lineage)==1


def test_later_append_versioned_reinterpretation_without_past_rewrite():
    scene,state=start();e0=digest(asdict(scene.events[0]));state,_=choose(scene,state)
    old=state.lineage[0];state,_=choose(scene,state,'later','NARROW','SUSPEND',None)
    assert len(state.lineage)==2 and state.lineage[1].previous_hash==old.hash
    assert state.lineage[0]==old and digest(asdict(scene.events[0]))==e0
    assert state.lineage[1].actor_memory_access=='NOT_GRANTED'


def test_later_no_change_is_actual_valid_option():
    scene,state=start();state,_=choose(scene,state)
    new,_=choose(scene,state,'later','NO_CHANGE','SUSPEND',None)
    assert new.lineage[-1].mode=='NO_CHANGE' and new.procedure_refs==state.procedure_refs


def test_independent_other_can_refuse_without_forced_romance():
    scene,state=start(seed_scene(other_action='REFUSE'))
    assert scene.events[-1].action_owner=='other_P' and scene.events[-1].action=='REFUSE'
    state,_=choose(scene,state)
    assert any(c.mode=='NO_CHANGE' for c in eligible(scene,state,'later'))
    assert not any('romance' in str(asdict(c)).lower() for c in eligible(scene,state,'later'))


def test_other_act_must_have_own_history():
    scene,state=start();other=scene.actors[-1]
    bad=replace(scene,actors=scene.actors[:-1]+(replace(other,history=()),))
    with pytest.raises(Refusal,match='INDEPENDENT_ACTION_HISTORY_REQUIRED'):validate(bad)


def test_child_cannot_write_caregiver_state():
    scene,state=start();wrong=replace(state,actor='caregiver')
    with pytest.raises(Refusal):choose(scene,wrong)


def test_unheard_parent_is_not_permitted_source():
    scene,state=start();kid=scene.actors[0];bad=replace(scene,actors=(replace(kid,access=('loss','later')),)+scene.actors[1:])
    assert not any(c.source=='parent_said' for c in eligible(bad,state,'loss'))


def test_malicious_llm_extra_effect_field_fails_closed():
    scene,state=start();c=eligible(scene,state,'loss')[1]
    with pytest.raises(Refusal,match='LLM_CAUSAL_AUTHORITY_FORBIDDEN'):
        propose(scene,state,'loss',c.id,model_packet={'candidate_id':c.id,'model_provenance':'synthetic','CAN011_delta':{'trust':1}})


def test_llm_valid_minimal_packet_still_noncausal():
    scene,state=start();c=eligible(scene,state,'loss')[1]
    p=propose(scene,state,'loss',c.id,model_packet={'candidate_id':c.id,'model_provenance':'synthetic'})
    assert p['no_actor_or_world_mutation'] and p['possible_owner_effect'].endswith('UNISSUED') and not state.lineage


def test_owner_fixture_permission_is_required():
    scene,state=start();c=eligible(scene,state,'loss')[1];p=propose(scene,state,'loss',c.id)
    with pytest.raises(Refusal,match='OWNER_PERMISSION_NOT_GRANTED'):append_test_only(scene,state,p,{'issuer':'fake'})


def test_permission_actor_binds():
    scene,state=start();c=eligible(scene,state,'loss')[1];p=propose(scene,state,'loss',c.id)
    with pytest.raises(Refusal,match='GRANT_ACTOR_SCOPE_INVALID'):fixture_grant(p,'caregiver')


def test_replay_is_exact_under_same_seal():
    scene,state=start();one,_=choose(scene,state);two,_=choose(scene,state)
    one,_=choose(scene,one,'later','CONTRADICT','SUSPEND',None)
    two,_=choose(scene,two,'later','CONTRADICT','SUSPEND',None)
    assert one.hash()==two.hash() and one.lineage==two.lineage


def test_permission_replay_from_stale_state_is_refused():
    scene,state=start();c=eligible(scene,state,'loss')[1];p=propose(scene,state,'loss',c.id);grant=fixture_grant(p,'child')
    changed=append_test_only(scene,state,p,grant)
    with pytest.raises(Refusal,match='STALE_LINEAGE_STATE'):append_test_only(scene,changed,p,grant)


def test_ordering_fails_closed_on_second_loss_after_later():
    scene,state=start();state,_=choose(scene,state)
    state,_=choose(scene,state,'later','NARROW','SUSPEND',None)
    with pytest.raises(Refusal,match='HISTORICAL_TIME_ORDER'):eligible(scene,state,'loss')


def test_unsupported_actor_procedure_fails():
    scene,state=start();state=replace(state,procedure_refs=('care_work_history',))
    with pytest.raises(Refusal,match='PROCEDURAL_ORIGIN_UNBOUND'):eligible(scene,state,'loss')


def test_demographic_only_counterfactual_invariance():
    a,s=start(seed_scene(age=12,background='A'));b,t=start(seed_scene(age=19,background='B'))
    assert eligible(a,s,'loss')==eligible(b,t,'loss')


def test_fake_objective_culprit_rejected():
    scene,state=start();loss=scene.events[0]
    bad=replace(scene,events=(replace(loss,material=loss.material+('culprit:group',)),)+scene.events[1:])
    with pytest.raises(Refusal,match='MORAL_FACT_IN_EVENT'):eligible(bad,state,'loss')


def test_witnessed_own_affect_cannot_be_borrowed():
    scene,state=start();c=eligible(scene,state,'loss')[1]
    with pytest.raises(Refusal,match='AFFECT_EVIDENCE_MISSING'):propose(scene,state,'loss',c.id,affect_ref='care_work_history')


def test_untampered_lineage_hash_is_required():
    scene,state=start();state,_=choose(scene,state)
    bad=replace(state,lineage=(replace(state.lineage[0],belief_stance='ACCEPT' if state.lineage[0].belief_stance!='ACCEPT' else 'REJECT'),))
    with pytest.raises(Refusal,match='LINEAGE_INTEGRITY_FAILURE'):eligible(scene,bad,'later')


def test_future_habit_cannot_be_causal_past_of_loss():
    scene,state=start();child=scene.actors[0]
    future=replace(child.history[1],time=99)
    modified=replace(scene,actors=(replace(child,history=(child.history[0],future)+child.history[2:]),)+scene.actors[1:])
    with pytest.raises(Refusal,match='PROCEDURAL_ORIGIN_UNBOUND'):eligible(modified,state,'loss')
