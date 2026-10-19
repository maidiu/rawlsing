"""R3 successor heldout: sourcefree actor OWNERSHIP is not observer identity.

These checks are independent of the original R2 91+3+11+14 frozen files.
They neither grant native ADP authority nor derive an actual psychological choice.
"""
from dataclasses import asdict, replace
import pytest
from kernel import (
    Actor, Event, History, HistoryWitness, Refusal, State, MODES,
    append_test_only, audit_no_change, digest, eligible, fixture_grant,
    objective_event_hash, propose, seed_scene, validate
)
from test_heldout_actor_independence import seeded_past
from test_local_hostile import twice

RELATION_MODES = set(MODES) - {'NO_CHANGE'}


def _observation_owner(scene, owner):
    """Refresh only the child's t9 observation and its synthetic witness hash."""
    a=scene.actors[0]
    observed=next(h for h in a.history if h.id=='later_observed_counterpart')
    revised=replace(observed, observed_action_owner=owner)
    a=replace(a, history=tuple(revised if h.id==observed.id else h for h in a.history))
    witnesses=tuple(replace(w, history_hash=digest(asdict(revised)))
        if w.actor=='child' and w.history_id==observed.id else w
        for w in scene.history_witnesses)
    return replace(scene, actors=(a,)+scene.actors[1:], history_witnesses=witnesses)


def _event_owner(scene, owner):
    e=next(e for e in scene.events if e.id=='later')
    new=replace(e, action_owner=owner, participants=('child',owner))
    return replace(scene, events=tuple(new if old.id==e.id else old for old in scene.events),
        relevance=tuple(replace(x, later_event_hash=objective_event_hash(new))
            if x.later_event_id==e.id else x for x in scene.relevance))


def _receipt_owner(scene, owner):
    return replace(scene, relevance=tuple(replace(x,observed_action_owner=owner)
        for x in scene.relevance))


def _independent_child_source(scene):
    old=scene.actors[0]
    h=History('independent_child_t7', 'child', 7, old.private_project, True, False)
    w=HistoryWitness(h.id,digest(asdict(h)),'child','caregiver',7,
        'actor_activity','INDEPENDENT_PROJECT')
    return replace(scene, actors=(replace(old, history=old.history+(h,)),)+scene.actors[1:],
        history_witnesses=scene.history_witnesses+(w,))


def _second_independent_other(scene):
    h=History('q_independent_activity','other_Q',7,'volunteer_project',True,False)
    a=Actor('other_Q',(h,),('later',),'volunteer_project',22,'any')
    w=HistoryWitness(h.id,digest(asdict(h)),a.id,'caregiver',7,
        'actor_activity','INDEPENDENT_PROJECT')
    return replace(scene, actors=scene.actors+(a,),history_witnesses=scene.history_witnesses+(w,))


def test_self_action_with_fully_matched_actor_receipts_is_still_refused():
    scene,state=seeded_past()
    scene=_independent_child_source(scene)
    scene=_event_owner(scene,'child')
    scene=_observation_owner(scene,'child')
    scene=_receipt_owner(scene,'child')
    validate(scene)
    assert scene.relevance[0].observed_action_owner=='child'
    assert scene.actors[0].history[-2].observed_action_owner=='child'
    assert {c.mode for c in eligible(scene,state,'later')}=={'NO_CHANGE'}


def test_two_genuine_independent_people_are_admissible_without_a_hardcoded_owner():
    scene,state=seeded_past()
    assert RELATION_MODES <= {c.mode for c in eligible(scene,state,'later')}
    scene=_second_independent_other(scene)
    scene=_event_owner(scene,'other_Q')
    scene=_observation_owner(scene,'other_Q')
    scene=_receipt_owner(scene,'other_Q')
    validate(scene)
    assert RELATION_MODES <= {c.mode for c in eligible(scene,state,'later')}
    c=next(c for c in eligible(scene,state,'later') if c.mode=='DIFFERENTIATE')
    p=propose(scene,state,'later',c.id)
    sources={k for k,_,_ in p['source_preimages']}
    assert {'RELATION_RELEVANCE','RELATION_OBSERVED_HISTORY','RELATION_HISTORY_WITNESS'} <= sources
    assert append_test_only(scene,state,p,fixture_grant(p,'child')).lineage[-1].source_preimages==p['source_preimages']


@pytest.mark.parametrize('bad', ['receipt_other_Q','observation_other_Q','receipt_missing','observation_missing'])
def test_misattributed_or_missing_action_owner_never_enables_counterpart(bad):
    scene,state=seeded_past()
    if bad=='receipt_other_Q': scene=_receipt_owner(scene,'other_Q')
    if bad=='observation_other_Q': scene=_observation_owner(scene,'other_Q')
    if bad=='receipt_missing': scene=_receipt_owner(scene,None)
    if bad=='observation_missing': scene=_observation_owner(scene,None)
    validate(scene)
    assert {c.mode for c in eligible(scene,state,'later')}=={'NO_CHANGE'}


def test_own_action_witnessed_by_two_independent_observers_remains_own_action():
    scene,state=seeded_past()
    scene=_independent_child_source(scene)
    scene=_event_owner(scene,'child')
    scene=_observation_owner(scene,'child')
    scene=_receipt_owner(scene,'child')
    scene=replace(scene,relevance=scene.relevance+(replace(scene.relevance[0],observer='peer'),))
    validate(scene)
    assert {c.mode for c in eligible(scene,state,'later')}=={'NO_CHANGE'}


@pytest.mark.parametrize('swapped',['receipt','observation','event'])
def test_source_owner_replacement_after_proposal_fails_before_append(swapped):
    scene,state=seeded_past()
    choice=next(c for c in eligible(scene,state,'later') if c.mode=='DIFFERENTIATE')
    proposal=propose(scene,state,'later',choice.id)
    grant=fixture_grant(proposal,'child')
    if swapped=='receipt': changed=_receipt_owner(scene,'caregiver')
    elif swapped=='observation': changed=_observation_owner(scene,'caregiver')
    else:
        changed=_event_owner(scene,'child')
        changed=_independent_child_source(changed)
        changed=_observation_owner(changed,'child')
        changed=_receipt_owner(changed,'child')
    validate(changed)
    with pytest.raises(Refusal):
        append_test_only(changed,state,proposal,grant)
    assert state.hash()==proposal['state_before_hash']


@pytest.mark.parametrize('swapped',['receipt','observation'])
def test_committed_consumed_owner_preimages_cannot_be_reissued(swapped):
    scene,state=twice()
    if swapped=='receipt': changed=_receipt_owner(scene,'caregiver')
    else: changed=_observation_owner(scene,'caregiver')
    validate(changed)
    with pytest.raises(Refusal,match='SOURCE_PREIMAGE_IDENTITY_COLLISION'):
        eligible(changed,state,'future')


def test_no_change_still_does_not_consume_relation_and_does_not_mutate_state():
    scene,state=seeded_past()
    scene=_receipt_owner(scene,'caregiver')
    c=next(c for c in eligible(scene,state,'later') if c.mode=='NO_CHANGE')
    p=propose(scene,state,'later',c.id)
    grant=fixture_grant(p,'child')
    assert not any(kind.startswith('RELATION_') for kind,_,_ in p['source_preimages'])
    assert append_test_only(scene,state,p,grant) is state
    assert audit_no_change(scene,state,p,grant).state_before_hash==state.hash()


def test_exact_replay_is_deterministic_for_genuine_other_and_remains_mutable_only_by_new_append():
    scene,state=seeded_past()
    a=tuple(eligible(scene,state,'later'))
    b=tuple(eligible(scene,state,'later'))
    assert a==b
    c=next(x for x in a if x.mode=='NARROW')
    p1=propose(scene,state,'later',c.id)
    p2=propose(scene,state,'later',c.id)
    assert p1==p2
    g=fixture_grant(p1,'child')
    d1=append_test_only(scene,state,p1,g)
    d2=append_test_only(scene,state,p1,g)
    assert d1.hash()==d2.hash()
    with pytest.raises(Refusal, match='STALE_LINEAGE_STATE'):
        append_test_only(scene,d1,p1,g)
