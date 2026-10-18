"""Independent-in-time M2 AUTHOR adversarial controls; no canonical owner issuance."""
from dataclasses import replace,asdict
from copy import deepcopy
import pytest
from kernel import *


def root(scene=None): return (scene or seed_scene()), State('child',procedure_refs=('old_watchful_habit',))

def choose(scene,state,event='discussion',mode='RECONSIDER',stance='REJECT',source='parent_said',**kwargs):
    c=next(c for c in eligible(scene,state,event) if c.mode==mode and c.stance==stance and c.source==source)
    p=propose(scene,state,event,c.id,**kwargs)
    return append_test_only(scene,state,p,fixture_grant(p,'child')),p

def test_t3_has_no_future_caregiver_or_peer_speech():
    s,st=root();assert not any(x.mode=='RECONSIDER' for x in eligible(s,st,'loss'))

def test_t6_processing_can_receive_real_t4_t5_accounts():
    s,st=root(); assert {(x.source,x.stance) for x in eligible(s,st,'discussion') if x.mode=='RECONSIDER'}=={(who,stance) for who in ('parent_said','peer_said') for stance in STANCES}

def test_late_affect_ref_refused_at_t3():
    s,st=root();c=eligible(s,st,'loss')[0]
    with pytest.raises(Refusal,match='FUTURE_AFFECT_REF'):propose(s,st,'loss',c.id,affect_ref='first_distress')

def test_late_action_ref_refused_at_t3():
    s,st=root();c=eligible(s,st,'loss')[0]
    with pytest.raises(Refusal,match='FUTURE_PUBLIC_ACTION_REF'):propose(s,st,'loss',c.id,public_action_ref='public_lock_check')

def test_later_affect_and_public_action_are_distinct_and_witnessed():
    s,st=root();st,_=choose(s,st,affect_ref='first_distress',public_action_ref='public_lock_check');r=st.lineage[0]
    assert r.belief_stance=='REJECT' and r.affect_ref=='first_distress' and r.public_action_ref=='public_lock_check' and r.actor_memory_access=='NOT_GRANTED'

def test_speaker_event_without_listener_exposure_is_not_eligible():
    s,st=root(seed_scene(child_access_peer=False));assert not any(x.source=='peer_said' for x in eligible(s,st,'discussion'))

def test_access_id_without_exposure_cannot_resurrect_peer():
    s,st=root(seed_scene(child_access_peer=False));ch=s.actors[0];changed=replace(s,actors=(replace(ch,access=ch.access+('peer_said',)),)+s.actors[1:])
    with pytest.raises(Refusal,match='SPEAKER_ACTION_OR_ACCESS_UNVERIFIED'):eligible(changed,st,'discussion')

def test_attributed_speech_without_admitted_speaker_action_refuses():
    s,st=root();changed=replace(s,speech_actions=tuple(x for x in s.speech_actions if x.speech_id!='parent_said'))
    with pytest.raises(Refusal,match='SPEAKER_ACTION_OR_ACCESS_UNVERIFIED'):eligible(changed,st,'discussion')

def test_forged_speech_time_receipt_fails_closed():
    s,st=root();sa=s.speech_actions[0];changed=replace(s,speech_actions=(replace(sa,time=3),)+s.speech_actions[1:])
    with pytest.raises(Refusal,match='SPEAKER_ACTION_OR_ACCESS_UNVERIFIED'):eligible(changed,st,'discussion')

def test_forged_history_true_without_independent_witness_fails():
    s,st=root();ch=s.actors[0];h=History('prior_forged','child',1,'some meaningful act',True,True)
    changed=replace(s,actors=(replace(ch,history=ch.history+(h,)),)+s.actors[1:])
    with pytest.raises(Refusal,match='HISTORY_WITNESS_SOURCE_UNVERIFIED'):eligible(changed,st,'loss')

def test_existing_history_text_edit_requires_independently_updated_witness():
    s,st=root();ch=s.actors[0];modified=replace(ch.history[0],activity='renamed yet source missing')
    changed=replace(s,actors=(replace(ch,history=(modified,)+ch.history[1:]),)+s.actors[1:])
    with pytest.raises(Refusal,match='HISTORY_WITNESS_SOURCE_UNVERIFIED'):eligible(changed,st,'loss')

def test_new_witnessed_relation_counterfactual_changes_source_identity_not_moral_stance():
    a,st=root(seed_scene(child_history='cooperative'));b,sb=root(seed_scene(child_history='threatened'))
    assert {x.stance for x in eligible(a,st,'discussion')}=={x.stance for x in eligible(b,sb,'discussion')}
    assert {x.id for x in eligible(a,st,'discussion') if x.mode=='PROCEDURAL_RECRUITMENT'}!={x.id for x in eligible(b,sb,'discussion') if x.mode=='PROCEDURAL_RECRUITMENT'}

def test_parent_private_change_without_child_access_does_not_auto_uptake():
    a,st=root(seed_scene(parent_history='care_work'));b,sb=root(seed_scene(parent_history='overtime'))
    assert eligible(a,st,'discussion')==eligible(b,sb,'discussion')

def test_typed_world_fact_cannot_smuggle_culprit_claim():
    s,st=root();event=s.events[0]
    forged=WorldFact('ACTIVITY_CONTEXT','garage','stolen_by:group_X','unregistered')
    bad=replace(s,events=(replace(event,material=event.material+(forged,)),)+s.events[1:])
    with pytest.raises(Refusal,match='MORAL_FACT_IN_EVENT'):eligible(bad,st,'loss')

def test_old_culprit_prefix_and_new_alias_both_refused():
    s,st=root();event=s.events[0]
    for value in ('culprit:group','stolen_by:group_X','sect:A','motive:envy'):
        bad=replace(s,events=(replace(event,material=event.material+(value,)),)+s.events[1:])
        with pytest.raises(Refusal,match='MORAL_FACT_IN_EVENT'):eligible(bad,st,'loss')

def test_legitimate_typed_world_resource_status_can_be_held_as_hypothetical_object_fact():
    s,st=root();f=WorldFact('RESOURCE_STATUS','bike','MISSING','test-only-object-ledger')
    e=s.events[0];modified=replace(s,events=(replace(e,material=e.material+(f,)),)+s.events[1:])
    # Processing source hash must be updated explicitly when the original event's content is updated.
    discussion=s.events[3];x=replace(e,material=e.material+(f,))
    modified=replace(modified,events=(x,)+s.events[1:3]+(replace(discussion,parent_event_hash=objective_event_hash(x)),)+s.events[4:])
    assert eligible(modified,st,'loss')

def test_prior_objective_event_collision_rejected_even_when_id_same():
    s,st=root();st,_=choose(s,st)
    e=s.events[0];changed=replace(s,events=(replace(e,material=e.material+('bicycle_found_undamaged',)),)+s.events[1:])
    with pytest.raises(Refusal,match='OBJECTIVE_EVENT_IDENTITY_COLLISION'):eligible(changed,st,'later')

def test_prior_processing_event_collision_rejected():
    s,st=root();st,_=choose(s,st)
    p=s.events[3];changed=replace(s,events=s.events[:3]+(replace(p,material=('shared_task',)),)+s.events[4:])
    with pytest.raises(Refusal,match='OBJECTIVE_EVENT_IDENTITY_COLLISION'):eligible(changed,st,'later')

def test_original_event_hash_is_immutable_across_later_interpretation():
    s,st=root();loss_hash=objective_event_hash(s.events[0]);st,_=choose(s,st)
    st,_=choose(s,st,'later','DIFFERENTIATE','SUSPEND',None)
    assert len(st.lineage)==2 and all(x.original_event_hash==loss_hash for x in st.lineage)
    assert st.lineage[1].previous_hash==st.lineage[0].hash and objective_event_hash(s.events[0])==loss_hash

def test_no_effect_returns_identical_state_and_separate_audit():
    s,st=root();st,_=choose(s,st)
    c=next(c for c in eligible(s,st,'later') if c.mode=='NO_CHANGE');p=propose(s,st,'later',c.id);g=fixture_grant(p,'child')
    receipt=audit_no_change(s,st,p,g)
    assert receipt.grade=='TEST_ONLY_NO_EFFECT_AUDIT' and receipt.state_before_hash==st.hash()
    assert append_test_only(s,st,p,g)==st

def test_no_effect_exact_replay_idempotent_and_non_mutating():
    s,st=root();c=eligible(s,st,'loss')[0];p=propose(s,st,'loss',c.id);g=fixture_grant(p,'child')
    assert append_test_only(s,st,p,g).hash()==st.hash() and audit_no_change(s,st,p,g)==audit_no_change(s,st,p,g)

def test_stale_mutating_grant_blocks_replay():
    s,st=root();c=next(c for c in eligible(s,st,'discussion') if c.mode=='RECONSIDER');p=propose(s,st,'discussion',c.id);g=fixture_grant(p,'child')
    updated=append_test_only(s,st,p,g)
    with pytest.raises(Refusal,match='STALE_LINEAGE_STATE'):append_test_only(s,updated,p,g)

def test_private_other_history_cannot_be_child_source():
    s,st=root();changed=replace(st,procedure_refs=('other_project',))
    with pytest.raises(Refusal,match='PROCEDURAL_ORIGIN_UNBOUND'):eligible(s,changed,'discussion')

def test_counterpart_refusal_no_compulsory_romantic_outcome():
    s,st=root(seed_scene(other_action='REFUSE'));st,_=choose(s,st)
    assert s.events[-1].action=='REFUSE';assert any(c.mode=='NO_CHANGE' for c in eligible(s,st,'later'))
    assert not any('romance' in str(asdict(c)).lower() for c in eligible(s,st,'later'))

def test_changed_later_event_breaks_unqualified_relevance_and_leaves_no_effect_only():
    s,st=root();st,_=choose(s,st)
    later=replace(s.events[-1],material=('unrelated_work',))
    changed=replace(s,events=s.events[:-1]+(later,))
    assert {c.mode for c in eligible(changed,st,'later')}=={'NO_CHANGE'}

def test_provenance_only_cosmetic_change_changes_custody_not_psychology():
    s,st=root();ch=s.actors[0];h=replace(ch.history[0],activity='cosmetic rewording')
    witnesses=tuple(replace(w,history_hash=digest(asdict(h))) if w.history_id==h.id and w.actor=='child' else w for w in s.history_witnesses)
    changed=replace(s,actors=(replace(ch,history=(h,)+ch.history[1:]),)+s.actors[1:],history_witnesses=witnesses)
    before=eligible(s,st,'discussion');after=eligible(changed,st,'discussion')
    assert {c.stance for c in before}=={c.stance for c in after}
    assert {c.id for c in before if c.mode=='PROCEDURAL_RECRUITMENT'} != {c.id for c in after if c.mode=='PROCEDURAL_RECRUITMENT'}

def test_exact_two_event_replay():
    s,st=root();a,_=choose(s,st);b,_=choose(s,st)
    a,_=choose(s,a,'later','CONTRADICT','SUSPEND',None)
    b,_=choose(s,b,'later','CONTRADICT','SUSPEND',None)
    assert a.hash()==b.hash() and a.lineage==b.lineage

@pytest.mark.parametrize('mode',('REATTRIBUTE','NARROW','GENERALIZE','REINFORCE','CONTRADICT','DIFFERENTIATE'))
def test_six_later_modes_remain_only_candidate_possibilities(mode):
    s,st=root();st,_=choose(s,st)
    assert any(x.mode==mode for x in eligible(s,st,'later'))
    assert len(st.lineage)==1

def test_old_unrelated_procedure_is_not_later_relation_relevance():
    s,st=root();st,_=choose(s,st)
    original=s.relevance[0]
    forged=replace(original,observed_history_id='old_watchful_habit')
    changed=replace(s,relevance=(forged,))
    assert {x.mode for x in eligible(changed,st,'later')}=={'NO_CHANGE'}

def test_future_speech_delivery_rejected_as_heard_now():
    s,st=root();exp=s.exposures[0]
    changed=replace(s,exposures=(replace(exp,heard_time=99),)+s.exposures[1:])
    with pytest.raises(Refusal,match='SPEAKER_ACTION_OR_ACCESS_UNVERIFIED'):
        eligible(changed,st,'discussion')

def test_independent_counterpart_history_cannot_be_replaced_without_register_repair():
    s,st=root();p=s.actors[-1];changed=replace(p,history=(replace(p.history[0],activity='pretended_new_project'),))
    bad=replace(s,actors=s.actors[:-1]+(changed,))
    with pytest.raises(Refusal,match='HISTORY_WITNESS_SOURCE_UNVERIFIED'):validate(bad)

def test_changed_observed_counterpart_history_cannot_confer_relation_relevance():
    s,st=root();st,_=choose(s,st);ch=s.actors[0]
    changed_h=replace(ch.history[-1],activity='fabricated_benevolent_action')
    bad=replace(s,actors=(replace(ch,history=ch.history[:-1]+(changed_h,)),)+s.actors[1:])
    with pytest.raises(Refusal,match='HISTORY_WITNESS_SOURCE_UNVERIFIED'):eligible(bad,st,'later')

def test_same_id_distinct_occurrences_in_same_scene_are_disallowed():
    s,st=root();wrong=replace(s.events[0],material=('bike','garage','bicycle_found_undamaged'))
    bad=replace(s,events=s.events+(wrong,))
    with pytest.raises(Refusal,match='EVENT_ID_COLLISION'):eligible(bad,st,'loss')

def test_relevant_later_refusal_does_not_automatically_reinterpret():
    s,st=root();st,_=choose(s,st);before=st.hash()
    options=eligible(s,st,'later')
    assert len(options)>1 and any(x.mode=='NO_CHANGE' for x in options)
    assert st.hash()==before and len(st.lineage)==1

def test_source_kind_prevents_relational_history_from_being_called_affect():
    s,st=root();c=eligible(s,st,'discussion')[0]
    with pytest.raises(Refusal,match='HISTORY_WITNESS_WRONG_OPERATION'):
        propose(s,st,'discussion',c.id,affect_ref='prior_recognition')

def test_source_kind_prevents_affect_history_from_being_public_action():
    s,st=root();c=eligible(s,st,'discussion')[0]
    with pytest.raises(Refusal,match='HISTORY_WITNESS_WRONG_OPERATION'):
        propose(s,st,'discussion',c.id,public_action_ref='first_distress')
