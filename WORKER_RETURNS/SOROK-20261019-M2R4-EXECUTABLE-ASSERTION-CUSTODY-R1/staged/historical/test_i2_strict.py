"""Fresh independent S1/I2 prospective constraints; NOT M1 source changes.
Assertions encode stronger owner/time/history constraints; failures are retained REDs.
"""
from dataclasses import replace, asdict
import pytest
from kernel import seed_scene, State, Event, Speech, History, eligible, propose, append_test_only, fixture_grant, validate, digest, Refusal


def root(scene=None):
    return scene or seed_scene(), State('child',procedure_refs=('old_watchful_habit',))


def first(scene,state):
    c=next(c for c in eligible(scene,state,'loss') if c.source=='parent_said' and c.stance=='REJECT')
    p=propose(scene,state,'loss',c.id)
    return append_test_only(scene,state,p,fixture_grant(p,'child'))

# Positive independently asserted properties

def test_01_reproducible_witnesses_and_plural_without_compulsion():
    sc,st=root(); a=eligible(sc,st,'loss'); b=eligible(sc,st,'loss')
    assert a==b and len(a)>=8 and len({(x.source,x.stance) for x in a if x.source})>=6
    assert st.lineage==()


def test_02_speaker_claim_not_objective_culprit():
    sc,st=root(); assert all('culprit:' not in x for x in sc.events[0].material)
    assert any(s.claim_ref=='peer_group_blame' for s in sc.speech)
    assert 'peer_group_blame' not in sc.events[0].material


def test_03_unheard_claim_not_eligible():
    sc,st=root(seed_scene(child_access_peer=False));assert not any(c.source=='peer_said' for c in eligible(sc,st,'loss'))


def test_04_same_child_accessible_history_parent_private_difference_cannot_auto_set_belief():
    a,sa=root(seed_scene(parent_history='care_work'));b,sb=root(seed_scene(parent_history='overtime'))
    assert eligible(a,sa,'loss')==eligible(b,sb,'loss')


def test_05_prior_actual_history_changed_provenance_not_forced_psychology():
    a,sa=root(seed_scene(child_history='cooperative'));b,sb=root(seed_scene(child_history='threatened'))
    ca=eligible(a,sa,'loss');cb=eligible(b,sb,'loss')
    assert {x.mode for x in ca}=={x.mode for x in cb}
    assert {x.stance for x in ca}=={x.stance for x in cb}
    assert {x.id for x in ca}!={x.id for x in cb}


def test_06_original_event_immutable_with_same_scene_and_append():
    sc,st=root();origin=digest(asdict(sc.events[0]));st=first(sc,st)
    later=next(c for c in eligible(sc,st,'later') if c.mode=='CONTRADICT')
    p=propose(sc,st,'later',later.id);s2=append_test_only(sc,st,p,fixture_grant(p,'child'))
    assert digest(asdict(sc.events[0]))==origin
    assert len(s2.lineage)==2 and s2.lineage[0]==st.lineage[0]
    assert s2.lineage[1].previous_hash==st.lineage[-1].hash


def test_07_private_memory_not_manufactured():
    sc,st=root();st=first(sc,st);assert st.lineage[0].actor_memory_access=='NOT_GRANTED'


def test_08_sibling_or_caregiver_history_not_borrowed_as_procedure():
    sc,st=root();st=replace(st,procedure_refs=('care_work_history',))
    with pytest.raises(Refusal,match='PROCEDURAL_ORIGIN_UNBOUND'):eligible(sc,st,'loss')


def test_09_other_P_refusal_already_encoded_no_forced_response():
    sc,st=root(seed_scene(other_action='REFUSE'));st=first(sc,st)
    assert sc.events[-1].action=='REFUSE'
    assert any(x.mode=='NO_CHANGE' for x in eligible(sc,st,'later'))


def test_10_bad_model_payload_cannot_inject_owner_effect():
    sc,st=root();c=eligible(sc,st,'loss')[0]
    with pytest.raises(Refusal,match='LLM_CAUSAL_AUTHORITY_FORBIDDEN'):
        propose(sc,st,'loss',c.id,model_packet={'candidate_id':c.id,'model_provenance':'test','memory_delta':'I always knew'})


def test_11_permission_replay_before_hash_blocks_reuse():
    sc,st=root();c=eligible(sc,st,'loss')[0];p=propose(sc,st,'loss',c.id);g=fixture_grant(p,'child')
    st2=append_test_only(sc,st,p,g)
    with pytest.raises(Refusal,match='STALE_LINEAGE_STATE'):append_test_only(sc,st2,p,g)


def test_12_foreign_other_history_does_not_supply_P_project():
    sc,st=root();p=sc.actors[-1]
    fake=replace(p,history=(replace(p.history[0],actor='caregiver'),))
    bad=replace(sc,actors=sc.actors[:-1]+(fake,))
    with pytest.raises(Refusal,match='FOREIGN_ACTOR_HISTORY'):validate(bad)


def test_13_demographics_no_direct_link():
    sc,st=root(seed_scene(age=5,background='X'));other,so=root(seed_scene(age=45,background='Y'))
    assert eligible(sc,st,'loss')==eligible(other,so,'loss')

# Strong owner/time/semantic invariants not verified by author's tests:

def test_R01_future_speech_must_not_be_available_at_event_clock():
    sc,st=root()
    assert sc.events[0].time==3 and sc.speech[0].time==4 and sc.speech[1].time==5
    assert not any(c.source=='parent_said' for c in eligible(sc,st,'loss')), 'FUTURE_UTTERANCE_LAUNDERED_TO_PAST'


def test_R02_future_affect_must_not_be_retrospectively_referenced_as_current():
    sc,st=root();c=eligible(sc,st,'loss')[0]
    with pytest.raises(Refusal,match='FUTURE_AFFECT_REF'):
        propose(sc,st,'loss',c.id,affect_ref='first_distress')


def test_R03_same_objective_id_changed_payload_cannot_preserve_old_lineage():
    sc,st=root();before=first(sc,st)
    loss=sc.events[0]
    new_loss=replace(loss,material=loss.material+('bicycle_found_undamaged',))
    new_scene=replace(sc,events=(new_loss,)+sc.events[1:])
    assert digest(asdict(loss)) != digest(asdict(new_loss))
    with pytest.raises(Refusal,match='OBJECTIVE_EVENT_IDENTITY_COLLISION'):
        eligible(new_scene,before,'later')


def test_R04_NO_CHANGE_must_mean_no_durable_interpretation_update():
    sc,st=root();before=first(sc,st)
    c=next(c for c in eligible(sc,before,'later') if c.mode=='NO_CHANGE')
    proposal=propose(sc,before,'later',c.id)
    after=append_test_only(sc,before,proposal,fixture_grant(proposal,'child'))
    assert after.hash()==before.hash(), 'NO_CHANGE_STILL_APPENDS_DURABLE_LINEAGE'


def test_R05_cosmetic_history_label_does_not_create_new_causal_route_identity():
    sc,st=root();ch=sc.actors[0]
    old=ch.history[0]; cosmetic=replace(old,activity='same work, spelling updated')
    updated=replace(sc,actors=(replace(ch,history=(cosmetic,)+ch.history[1:]),)+sc.actors[1:])
    a={c.id for c in eligible(sc,st,'loss') if c.mode=='PROCEDURAL_RECRUITMENT'}
    b={c.id for c in eligible(updated,st,'loss') if c.mode=='PROCEDURAL_RECRUITMENT'}
    assert a==b, 'COSMETIC_ACTIVITY_NAME_CHANGE_CREATES_NEW_CANDIDATE_ID'


def test_R06_forged_witness_without_source_admission_cannot_create_route():
    sc,st=root();ch=sc.actors[0]
    fake=History('prior_forged_interaction','child',1,'fabricated history',True,True)
    tampered=replace(sc,actors=(replace(ch,history=ch.history+(fake,)),)+sc.actors[1:])
    with pytest.raises(Refusal,match='HISTORY_WITNESS_SOURCE_UNVERIFIED'):
        eligible(tampered,st,'loss')


def test_R07_nonsemantic_material_stereotype_cannot_be_minted_world_truth():
    sc,st=root();loss=sc.events[0]
    bad=replace(sc,events=(replace(loss,material=loss.material+('stolen_by:group_X',)),)+sc.events[1:])
    with pytest.raises(Refusal,match='MORAL_FACT_IN_EVENT'):
        eligible(bad,st,'loss')


def test_R08_future_self_history_cannot_be_usable_as_prior_lineage_evidence():
    sc,st=root();ch=sc.actors[0]
    future=replace(ch.history[0],time=99)
    new=replace(sc,actors=(replace(ch,history=(future,)+ch.history[1:]),)+sc.actors[1:])
    a=eligible(new,st,'loss')
    assert not any(c.mode=='PROCEDURAL_RECRUITMENT' for c in a)


def test_R09_later_own_new_utterance_requires_actual_speaker_opportunity():
    sc,st=root();s=Speech('outsider_forged','loss','other_P',4,'All this was their group.','peer_group_blame')
    child=sc.actors[0]
    tampered=replace(sc,actors=(replace(child,access=child.access+(s.id,)),)+sc.actors[1:],speech=sc.speech+(s,))
    with pytest.raises(Refusal,match='SPEAKER_ACTION_OR_ACCESS_UNVERIFIED'):
        eligible(tampered,st,'loss')


def test_R10_later_interpretation_requires_evidence_of_relevance_or_difference():
    sc,st=root();before=first(sc,st)
    irrelevant=replace(sc.events[-1],material=('unrelated_work',),action='REFUSE')
    changed=replace(sc,events=(sc.events[0],irrelevant))
    choices=eligible(changed,before,'later')
    assert {c.mode for c in choices}=={'NO_CHANGE'},'SIX_PSYCHOLOGICAL_REINTERPRETATIONS_WITHOUT_RELEVANCE_EVIDENCE'
