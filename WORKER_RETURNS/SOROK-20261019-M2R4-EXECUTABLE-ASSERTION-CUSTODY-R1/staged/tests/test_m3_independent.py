"""M3 independently authored sourcefree scientific compatibility/hostile controls.
Does not call M2 author's test functions or F2 oracle.  No production permissions.
"""
from dataclasses import replace, asdict
import pytest
from kernel import (
    Actor, History, HistoryWitness, State, WorldFact, Refusal, Candidate,
    Speech, SpeechAction, Exposure, Event, Scene,
    seed_scene, eligible, propose, fixture_grant, append_test_only,
    audit_no_change, objective_event_hash, digest, validate,
)


def before():
    return seed_scene(), State('child', procedure_refs=('old_watchful_habit',))

def choice(s, st, event='discussion', source='parent_said', stance='REJECT', mode='RECONSIDER'):
    return next(c for c in eligible(s, st, event)
                if c.source == source and c.stance == stance and c.mode == mode)

def committed(s, st, event='discussion', source='parent_said', stance='REJECT', mode='RECONSIDER', **opts):
    c=choice(s,st,event,source,stance,mode)
    p=propose(s,st,event,c.id,**opts)
    return append_test_only(s,st,p,fixture_grant(p,'child'))

def test_M3_01_both_claims_postdate_loss_and_no_t3_reconsideration():
    s,st=before();assert s.events[0].time==3
    assert [(v.speaker,v.time) for v in s.speech]==[('caregiver',4),('peer',5)]
    assert not [c for c in eligible(s,st,'loss') if c.mode=='RECONSIDER']

def test_M3_02_exact_t6_processing_restores_two_plural_accounts():
    s,st=before();x=eligible(s,st,'discussion')
    assert {(c.source,c.stance) for c in x if c.mode=='RECONSIDER'}=={
        (n,t) for n in ('parent_said','peer_said') for t in ('ACCEPT','REJECT','SUSPEND')}
    assert st.lineage==()

def test_M3_03_unknown_culprit_stays_unknown_and_peer_group_accusation_only_speech():
    s,st=before();assert not any('group' in str(z) for z in s.events[0].material)
    assert any(t.claim_ref=='peer_group_blame' for t in s.speech)
    assert choice(s,st,'discussion',source='peer_said',stance='REJECT')

def test_M3_04_t3_refuses_future_affect():
    s,st=before();c=eligible(s,st,'loss')[0]
    with pytest.raises(Refusal,match='FUTURE_AFFECT_REF'):
        propose(s,st,'loss',c.id,affect_ref='first_distress')

def test_M3_05_t6_separate_negative_affect_and_public_practice_with_rejection():
    s,st=before();done=committed(s,st,affect_ref='first_distress',public_action_ref='public_lock_check')
    x=done.lineage[-1];assert (x.belief_stance,x.affect_ref,x.public_action_ref)==('REJECT','first_distress','public_lock_check')
    assert x.actor_memory_access=='NOT_GRANTED'

def test_M3_06_witnessed_caregiver_private_history_swap_does_not_change_child_uptake():
    s,st=before();q=seed_scene(parent_history='a genuinely different labor history')
    assert eligible(s,st,'discussion')==eligible(q,st,'discussion')

def test_M3_07_child_witnessed_history_changes_content_identity_not_forced_belief():
    a,st=before();b=seed_scene(child_history='contrary own witnessed relation')
    ca=eligible(a,st,'discussion');cb=eligible(b,st,'discussion')
    assert {c.stance for c in ca}=={c.stance for c in cb}
    assert {c.id for c in ca if c.mode=='PROCEDURAL_RECRUITMENT'}!={c.id for c in cb if c.mode=='PROCEDURAL_RECRUITMENT'}

def test_M3_08_prior_procedural_habit_survives_conscious_rejection():
    s,st=before();after=committed(s,st)
    assert after.procedure_refs==('old_watchful_habit',)
    assert after.lineage[-1].belief_stance=='REJECT'

def test_M3_09_original_objective_content_hash_survives_later_differentiation():
    s,st=before();origin=objective_event_hash(s.events[0]);s1=committed(s,st)
    c=choice(s,s1,event='later',source=None,stance='SUSPEND',mode='DIFFERENTIATE')
    p=propose(s,s1,'later',c.id);s2=append_test_only(s,s1,p,fixture_grant(p,'child'))
    assert len(s2.lineage)==2 and s2.lineage[-1].previous_hash==s1.lineage[-1].hash
    assert s2.lineage[-1].original_event_hash==origin==s1.lineage[-1].original_event_hash

def test_M3_10_forged_same_id_changed_loss_refused_after_lineage():
    s,st=before();done=committed(s,st)
    bad=replace(s,events=(replace(s.events[0],material=s.events[0].material+('bicycle_found_undamaged',)),)+s.events[1:])
    with pytest.raises(Refusal,match='OBJECTIVE_EVENT_IDENTITY_COLLISION'):eligible(bad,done,'later')

def test_M3_11_forged_same_id_changed_processing_refused_after_lineage():
    s,st=before();done=committed(s,st)
    bad=replace(s,events=s.events[:3]+(replace(s.events[3],material=('unrelated_work',)),)+s.events[4:])
    with pytest.raises(Refusal,match='OBJECTIVE_EVENT_IDENTITY_COLLISION'):eligible(bad,done,'later')

def test_M3_12_no_effect_retains_state_but_separate_audit_changes_document_identity():
    s,st=before();done=committed(s,st)
    c=choice(s,done,event='later',source=None,stance='SUSPEND',mode='NO_CHANGE')
    p=propose(s,done,'later',c.id);g=fixture_grant(p,'child')
    r=audit_no_change(s,done,p,g)
    assert append_test_only(s,done,p,g) is done and r.state_before_hash==done.hash()
    assert r.hash!=done.hash() and len(done.lineage)==1

def test_M3_13_refusing_other_person_with_real_independent_project_does_not_force_belief():
    s,st=before();done=committed(s,st);options=eligible(s,done,'later')
    assert s.events[-1].action=='REFUSE'
    assert len(options)>1 and any(c.mode=='NO_CHANGE' for c in options)
    assert done.lineage[-1].mode=='RECONSIDER'

def test_M3_14_unrelated_later_material_still_allows_no_change_only():
    s,st=before();done=committed(s,st)
    new=replace(s.events[-1],material=('unrelated_work',))
    bad=replace(s,events=s.events[:-1]+(new,))
    assert {c.mode for c in eligible(bad,done,'later')}=={'NO_CHANGE'}

def test_M3_15_self_attested_history_without_witness_refused_even_if_witnessed_flag_true():
    s,st=before();child=s.actors[0]
    fake=History('prior_fake_child','child',2,'compelling moral story',True,True)
    forged=replace(s,actors=(replace(child,history=child.history+(fake,)),)+s.actors[1:])
    with pytest.raises(Refusal,match='HISTORY_WITNESS_SOURCE_UNVERIFIED'):eligible(forged,st,'discussion')

def test_M3_16_cross_actor_history_witness_cannot_authorize_child_activity():
    s,st=before();child=s.actors[0];w=s.history_witnesses[0]
    bad=replace(s,history_witnesses=(replace(w,actor='caregiver'),)+s.history_witnesses[1:])
    with pytest.raises(Refusal,match='HISTORY_WITNESS_SOURCE_UNVERIFIED'):eligible(bad,st,'discussion')

def test_M3_17_access_id_without_exposure_cannot_create_heard_claim():
    s,st=before();child=s.actors[0]
    bad=replace(s,exposures=tuple(v for v in s.exposures if v.speech_id!='parent_said'))
    with pytest.raises(Refusal,match='SPEAKER_ACTION_OR_ACCESS_UNVERIFIED'):eligible(bad,st,'discussion')

def test_M3_18_missing_speaker_action_event_refused():
    s,st=before();bad=replace(s,speech_actions=tuple(v for v in s.speech_actions if v.speech_id!='parent_said'))
    with pytest.raises(Refusal,match='SPEAKER_ACTION_OR_ACCESS_UNVERIFIED'):eligible(bad,st,'discussion')

def test_M3_19_exposure_from_future_cannot_be_retroactively_heard():
    s,st=before();q=s.exposures[0];bad=replace(s,exposures=(replace(q,heard_time=99),)+s.exposures[1:])
    with pytest.raises(Refusal,match='SPEAKER_ACTION_OR_ACCESS_UNVERIFIED'):eligible(bad,st,'discussion')

def test_M3_20_typed_material_claim_group_as_true_is_refused():
    s,st=before();e=s.events[0];fact=WorldFact('RESOURCE_STATUS','bike','stolen_by:group','source')
    bad=replace(s,events=(replace(e,material=e.material+(fact,)),)+s.events[1:])
    with pytest.raises(Refusal,match='MORAL_FACT_IN_EVENT'):eligible(bad,st,'loss')

def test_M3_21_valid_typed_resource_status_on_new_observation_is_allowed():
    s,st=before();e=s.events[0];p=s.events[3]
    f=WorldFact('RESOURCE_STATUS','bike','MISSING','test-only-resource-ledger')
    newer=replace(e,material=e.material+(f,))
    newerp=replace(p,parent_event_hash=objective_event_hash(newer))
    newer_scene=replace(s,events=(newer,)+s.events[1:3]+(newerp,)+s.events[4:])
    assert eligible(newer_scene,st,'loss')

def test_M3_22_stale_mutating_grant_replay_refused():
    s,st=before();c=choice(s,st);p=propose(s,st,'discussion',c.id);g=fixture_grant(p,'child')
    done=append_test_only(s,st,p,g)
    with pytest.raises(Refusal,match='STALE_LINEAGE_STATE'):append_test_only(s,done,p,g)

def test_M3_23_two_event_exact_replay_hash_same():
    s,st=before();d1=committed(s,st);d2=committed(s,st)
    f1=committed(s,d1,'later',None,'SUSPEND','CONTRADICT')
    f2=committed(s,d2,'later',None,'SUSPEND','CONTRADICT')
    assert f1.hash()==f2.hash() and f1.lineage==f2.lineage

def test_M3_24_age_background_swaps_cannot_impose_stance():
    a,st=before();b=seed_scene(age=56,background='different class or culture')
    assert eligible(a,st,'discussion')==eligible(b,st,'discussion')

def test_M3_25_other_person_project_without_actual_prior_witness_is_refused():
    s,st=before();other=s.actors[-1];bad=replace(s,actors=s.actors[:-1]+(replace(other,history=()),))
    with pytest.raises(Refusal,match='INDEPENDENT_ACTION_HISTORY_REQUIRED'):eligible(bad,st,'later')

def test_M3_26_actor_cannot_claim_other_history_as_own_procedure():
    s,st=before();bad=replace(st,procedure_refs=('other_project',))
    with pytest.raises(Refusal,match='PROCEDURAL_ORIGIN_UNBOUND'):eligible(s,bad,'discussion')

def test_M3_27_model_payload_cannot_write_immediate_memory_or_belief():
    s,st=before();c=choice(s,st)
    with pytest.raises(Refusal,match='LLM_CAUSAL_AUTHORITY_FORBIDDEN'):
        propose(s,st,'discussion',c.id,model_packet={'candidate_id':c.id,'model_provenance':'synthetic','effect':'belief'})

def test_M3_28_changed_witness_operation_affect_vs_public_is_refused():
    s,st=before();ref=choice(s,st)
    with pytest.raises(Refusal,match='HISTORY_WITNESS_WRONG_OPERATION'):
        propose(s,st,'discussion',ref.id,affect_ref='public_lock_check')

def test_M3_29_uncontrolled_forged_speaker_motive_cannot_be_objective():
    s,st=before();e=s.events[0]
    new=replace(e,material=e.material+('speaker_intent:caregiver_good',))
    with pytest.raises(Refusal,match='MORAL_FACT_IN_EVENT'):eligible(replace(s,events=(new,)+s.events[1:]),st,'loss')

def test_M3_30_lineage_tamper_after_sourcefree_update_refused():
    s,st=before();done=committed(s,st)
    tampered=replace(done,lineage=(replace(done.lineage[0],belief_stance='ACCEPT'),))
    with pytest.raises(Refusal,match='LINEAGE_INTEGRITY_FAILURE'):eligible(s,tampered,'later')

# Source-issuance limitations are represented explicitly, not made pass by semantic assertion.
def test_M3_31_registered_fixtures_remain_self_authored_not_true_external_signatures():
    s,st=before()
    assert s.history_witnesses[0].issuer=='M2_TEST_ONLY_INDEPENDENT_HISTORY_REGISTRY'
    assert s.exposures[0].witness=='child'  # listener reports its own access; no independent attestation
    assert not hasattr(s.exposures[0],'signature')
    assert not hasattr(s.history_witnesses[0],'owner_signature')

def test_M3_32_speech_contents_not_proof_of_speaker_private_intent():
    s,st=before();claims={x.claim_ref for x in s.speech}
    assert 'peer_group_blame' in claims
    assert all('culprit' not in str(x).lower() for x in s.events[0].material)
    assert st.lineage==()
