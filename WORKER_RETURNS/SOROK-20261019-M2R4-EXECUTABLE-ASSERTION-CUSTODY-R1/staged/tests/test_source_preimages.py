"""Independent candidate regression: frozen M2/M3 tests remain unchanged."""
from dataclasses import asdict, replace
import pytest
from kernel import (seed_scene, State, eligible, propose, fixture_grant, append_test_only,
                    Refusal, digest, validate, RULE_HASH, audit_no_change)


def begun(*, source='parent_said', stance='REJECT', affect=True, procedure=True):
    scene=seed_scene()
    state=State('child', procedure_refs=('old_watchful_habit',) if procedure else ())
    candidate=next(x for x in eligible(scene,state,'discussion') if x.source==source and x.stance==stance)
    p=propose(scene,state,'discussion',candidate.id,affect_ref='first_distress' if affect else None,
              public_action_ref='public_lock_check')
    return scene, append_test_only(scene,state,p,fixture_grant(p,'child'))


def changed_history(scene,ref,change):
    old=scene.actors[0]
    hh=tuple(replace(h, activity=change) if h.id==ref else h for h in old.history)
    h=next(h for h in hh if h.id==ref)
    ww=tuple(replace(w,history_hash=digest(asdict(h))) if w.actor=='child' and w.history_id==ref
             else w for w in scene.history_witnesses)
    return replace(scene,actors=(replace(old,history=hh),)+scene.actors[1:],history_witnesses=ww)


def changed_words(scene,words):
    news=replace(scene.speech[0], words=words)
    aa=tuple(replace(a,speech_hash=digest(asdict(news))) if a.speech_id==news.id else a
             for a in scene.speech_actions)
    ee=tuple(replace(x,speech_hash=digest(asdict(news))) if x.speech_id==news.id else x
             for x in scene.exposures)
    return replace(scene,speech=(news,)+scene.speech[1:],speech_actions=aa,exposures=ee)


def reject(scene,st):
    with pytest.raises(Refusal,match='SOURCE_PREIMAGE_IDENTITY_COLLISION'):
        eligible(scene,st,'later')


def test_parent_words_changed_even_with_reissued_synthetic_receipts():
    s,st=begun();reject(changed_words(s,'Group Y caused it.'),st)


def test_practice_changed_even_with_reissued_synthetic_witness():
    s,st=begun();reject(changed_history(s,'old_watchful_habit','refuses all locks'),st)


def test_affect_changed_even_with_reissued_synthetic_witness():
    s,st=begun();reject(changed_history(s,'first_distress','delight'),st)


def test_public_action_changed_even_with_reissued_synthetic_witness():
    s,st=begun();reject(changed_history(s,'public_lock_check','ran away'),st)


def test_speaker_action_source_witness_changes_even_if_heard_words_same():
    s,st=begun();a=replace(s.speech_actions[0], observer='other_P')
    reject(replace(s,speech_actions=(a,)+s.speech_actions[1:]),st)


def test_exposure_witness_changes_even_if_heard_words_same():
    s,st=begun();exp=replace(s.exposures[0], witness='other_P')
    reject(replace(s,exposures=(exp,)+s.exposures[1:]),st)


def test_procedure_witness_observer_changed_correct_hash():
    s,st=begun()
    changed=tuple(replace(w,observer='peer') if w.actor=='child' and w.history_id=='old_watchful_habit' else w
                  for w in s.history_witnesses)
    reject(replace(s,history_witnesses=changed),st)


def test_unrelated_fathers_independently_witnessed_private_history_can_change():
    s,st=begun()
    caregiver=s.actors[1];hh=tuple(replace(h,activity='care_work_revised') for h in caregiver.history)
    witness=tuple(replace(w,history_hash=digest(asdict(hh[0]))) if w.actor=='caregiver'
                  and w.history_id=='care_work_history' else w for w in s.history_witnesses)
    future=replace(s,actors=s.actors[:1]+(replace(caregiver,history=hh),)+s.actors[2:],history_witnesses=witness)
    assert eligible(future,st,'later')


def test_unrelated_peer_words_can_change_if_not_consumed():
    s,st=begun()
    # Peer said something t5; REJECT selected caregiver words, not peer's.
    peer=replace(s.speech[1],words='Unrelated revised rumor')
    acts=tuple(replace(a,speech_hash=digest(asdict(peer))) if a.speech_id=='peer_said' else a
               for a in s.speech_actions)
    exposures=tuple(replace(x,speech_hash=digest(asdict(peer))) if x.speech_id=='peer_said' else x
                    for x in s.exposures)
    news=replace(s,speech=(s.speech[0],peer),speech_actions=acts,exposures=exposures)
    assert eligible(news,st,'later')


def test_both_interpretations_freeze_their_distinct_speech_sources():
    s,st=begun(source='peer_said',stance='SUSPEND')
    s2=changed_words(s,'Changed caregiver account only')
    assert eligible(s2,st,'later')
    peer=replace(s.speech[1],words='Totally different group blame')
    acts=tuple(replace(a,speech_hash=digest(asdict(peer))) if a.speech_id=='peer_said' else a for a in s.speech_actions)
    heard=tuple(replace(x,speech_hash=digest(asdict(peer))) if x.speech_id=='peer_said' else x for x in s.exposures)
    reject(replace(s,speech=(s.speech[0],peer),speech_actions=acts,exposures=heard),st)


def test_proposal_readset_commits_to_original_sources():
    s,st=begun()
    rec=st.lineage[0]
    kinds={k for k,ref,h in rec.source_preimages}
    assert {'PRACTICAL_HISTORY','PRACTICAL_HISTORY_WITNESS','HEARD_SPEECH',
            'SPEAKER_ACTION_RECEIPT','LISTENER_EXPOSURE_RECEIPT',
            'AFFECT_HISTORY','PUBLIC_ACTION_HISTORY'}<=kinds
    assert all(len(z)==64 for k,ref,z in rec.source_preimages)
    assert RULE_HASH==rec.rule_hash


def test_exact_deterministic_replay_same_scene_and_state():
    s,st=begun()
    root=State('child',procedure_refs=('old_watchful_habit',))
    opt=next(x for x in eligible(s,root,'discussion') if x.source=='parent_said' and x.stance=='REJECT')
    p=propose(s,root,'discussion',opt.id,affect_ref='first_distress',public_action_ref='public_lock_check')
    assert append_test_only(s,root,p,fixture_grant(p,'child')).hash()==st.hash()


def test_no_change_preserves_state_even_with_source_locked():
    s,st=begun()
    op=next(c for c in eligible(s,st,'later') if c.mode=='NO_CHANGE')
    p=propose(s,st,'later',op.id)
    before=st.hash()
    assert append_test_only(s,st,p,fixture_grant(p,'child')).hash()==before
    assert audit_no_change(s,st,p,fixture_grant(p,'child')).hash


def test_missing_selected_speech_source_denied():
    s,st=begun()
    altered=replace(s,speech=s.speech[1:],speech_actions=s.speech_actions[1:],exposures=s.exposures[1:])
    reject(altered,st)


def test_synthetically_reissued_source_is_not_production_signed_authority():
    s,st=begun()
    assert st.lineage[0].actor_memory_access=='NOT_GRANTED'
    assert 'TEST_ONLY' in st.lineage[0].actor_memory_access or st.lineage[0].actor_memory_access=='NOT_GRANTED'
