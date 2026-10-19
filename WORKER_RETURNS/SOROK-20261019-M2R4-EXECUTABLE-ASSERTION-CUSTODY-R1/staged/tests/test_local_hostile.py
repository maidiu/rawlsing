"""New local verification, not an independent acceptance court."""
from dataclasses import replace,asdict
from copy import deepcopy
import json
import pytest
from kernel import (seed_scene,State,eligible,propose,fixture_grant,append_test_only,
                    audit_no_change,Refusal,digest,Event,objective_event_hash)

def begin():
    scene=seed_scene();state=State('child',procedure_refs=('old_watchful_habit',))
    c=next(c for c in eligible(scene,state,'discussion') if c.source=='parent_said' and c.stance=='REJECT')
    p=propose(scene,state,'discussion',c.id,affect_ref='first_distress',public_action_ref='public_lock_check')
    return scene,append_test_only(scene,state,p,fixture_grant(p,'child'))

def rewrite_history(scene,who,ref,**changes):
    actors=[];target=None
    for person in scene.actors:
        history=[]
        for h in person.history:
            if person.id==who and h.id==ref:h=replace(h,**changes);target=h
            history.append(h)
        actors.append(replace(person,history=tuple(history)))
    assert target
    witnesses=tuple(replace(w,history_hash=digest(asdict(target)),time=target.time)
        if w.actor==who and w.history_id==ref else w for w in scene.history_witnesses)
    return replace(scene,actors=tuple(actors),history_witnesses=witnesses)

@pytest.mark.parametrize('ref',['old_watchful_habit','first_distress','public_lock_check'])
def test_reissued_old_history_sources_refused_without_state_change(ref):
    scene,state=begin();before=state.hash()
    bad=rewrite_history(scene,'child',ref,activity='malicious replacement')
    with pytest.raises(Refusal,match='SOURCE_PREIMAGE'):eligible(bad,state,'later')
    assert state.hash()==before

def test_reissued_speech_action_exposure_cannot_replace_prior_words():
    scene,state=begin();new=replace(scene.speech[0],words='a contradictory retrospective claim')
    bad=replace(scene,speech=(new,)+scene.speech[1:],
       speech_actions=tuple(replace(a,speech_hash=digest(asdict(new))) if a.speech_id==new.id else a for a in scene.speech_actions),
       exposures=tuple(replace(x,speech_hash=digest(asdict(new))) if x.speech_id==new.id else x for x in scene.exposures))
    with pytest.raises(Refusal,match='SOURCE_PREIMAGE'):eligible(bad,state,'later')

def test_unconsumed_private_history_change_does_not_change_later_options():
    scene,state=begin();bad=rewrite_history(scene,'caregiver','care_work_history',activity='unrelated private work')
    assert eligible(bad,state,'later')==eligible(scene,state,'later')

def test_renewed_future_exposure_does_not_create_prior_access():
    scene=seed_scene();state=State('child')
    bad=replace(scene,exposures=(replace(scene.exposures[0],heard_time=99),)+scene.exposures[1:])
    with pytest.raises(Refusal,match='SPEAKER_ACTION_OR_ACCESS_UNVERIFIED'):eligible(bad,state,'discussion')
    assert not any(c.source=='parent_said' for c in eligible(scene,state,'loss'))

def test_exact_replay_and_no_change_remain_distinct_from_mutating_lineage():
    scene,state=begin();scene2,state2=begin();assert state.hash()==state2.hash()
    c=next(c for c in eligible(scene,state,'later') if c.mode=='NO_CHANGE')
    p=propose(scene,state,'later',c.id);g=fixture_grant(p,'child')
    assert append_test_only(scene,state,p,g) is state
    assert audit_no_change(scene,state,p,g).state_before_hash==state.hash()

def test_tampered_proposal_preimage_with_fresh_fixture_grant_refused():
    scene=seed_scene();state=State('child',procedure_refs=('old_watchful_habit',))
    c=next(c for c in eligible(scene,state,'discussion') if c.source=='parent_said')
    p=propose(scene,state,'discussion',c.id);p['source_preimages']=()
    with pytest.raises(Refusal,match='PROPOSAL_RECOMPUTATION_FAILED'):
        append_test_only(scene,state,p,fixture_grant(p,'child'))

def twice():
    scene,state=begin()
    c=next(c for c in eligible(scene,state,'later') if c.mode=='DIFFERENTIATE')
    p=propose(scene,state,'later',c.id);state=append_test_only(scene,state,p,fixture_grant(p,'child'))
    # New processing time supplies a lawful future continuation without a new relevance label.
    e=Event('future','PROCESS',12,'child',('child','caregiver','peer'),('loss_discussion',),
            parent_event_id='loss',parent_event_hash=objective_event_hash(scene.events[0]))
    own=replace(scene.actors[0],access=scene.actors[0].access+('future',))
    return replace(scene,events=scene.events+(e,),actors=(own,)+scene.actors[1:]),state

@pytest.mark.parametrize('attack',['observed_history','relevance_deleted','relevance_witness'])
def test_consumed_later_relation_source_must_remain_bound(attack):
    scene,state=twice();assert eligible(scene,state,'future')
    if attack=='observed_history':
        bad=rewrite_history(scene,'child','later_observed_counterpart',activity='observed_counterpart_action:ALLOW')
    elif attack=='relevance_deleted':bad=replace(scene,relevance=())
    else:bad=replace(scene,relevance=(replace(scene.relevance[0],observer='peer'),))
    # This source enabled the already appended DIFFERENTIATE at t9.
    with pytest.raises(Refusal,match='SOURCE_PREIMAGE|SOURCE_IDENTITY|LINEAGE'):
        eligible(bad,state,'future')
