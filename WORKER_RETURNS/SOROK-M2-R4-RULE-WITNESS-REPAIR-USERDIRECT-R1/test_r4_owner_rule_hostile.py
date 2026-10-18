"""R4 bounded implementer-owned hostile controls; independent later I2 still required.

These exercises are deliberately separate from previous author/I2 source files.
Never construe synthetic receipt issuers as native ADP owners.
"""
from dataclasses import asdict, replace
import pytest
from kernel import (
    Actor, History, HistoryWitness, Refusal, State, RULE_HASH,
    append_test_only, audit_no_change, digest, eligible, fixture_grant,
    objective_event_hash, propose, seed_scene, validate,
)
from test_heldout_actor_independence import seeded_past
from test_local_hostile import twice


def t9(scene):
    return next(e for e in scene.events if e.id=='later')


def observe(scene, *, action_event_observer=None, relevance_observer=None, history_observer=None):
    e=t9(scene)
    if action_event_observer is not None:
        changed_e=replace(e, observer=action_event_observer)
        scene=replace(scene, events=tuple(changed_e if x.id=='later' else x for x in scene.events),
             relevance=tuple(replace(x,later_event_hash=objective_event_hash(changed_e))
                             if x.later_event_id=='later' else x for x in scene.relevance))
    if relevance_observer is not None:
        scene=replace(scene,relevance=tuple(replace(x,observer=relevance_observer) for x in scene.relevance))
    if history_observer is not None:
        scene=replace(scene,history_witnesses=tuple(replace(w,observer=history_observer)
            if w.actor=='child' and w.history_id=='later_observed_counterpart' else w
            for w in scene.history_witnesses))
    validate(scene)
    return scene


@pytest.mark.parametrize('one_self_witness',('objective_event','relevance','history_witness'))
def test_single_self_witness_channel_alone_does_not_enable_counterpart(one_self_witness):
    s,st=seeded_past()
    k={'objective_event':'action_event_observer',
       'relevance':'relevance_observer','history_witness':'history_observer'}[one_self_witness]
    changed=observe(s,**{k:'other_P'})
    assert {c.mode for c in eligible(changed,st,'later')}=={'NO_CHANGE'}


def test_three_independent_witness_channels_restore_modes():
    s,st=seeded_past()
    other=observe(s,action_event_observer='child',relevance_observer='peer',history_observer='caregiver')
    assert len(eligible(other,st,'later'))==7


def test_owner_witness_alternative_cannot_displace_consumed_independent_alternative():
    scene,state=twice()
    baseline=eligible(scene,state,'future')
    owner_attests=replace(scene.relevance[0],observer='other_P')
    changed=replace(scene,relevance=scene.relevance+(owner_attests,))
    assert eligible(changed,state,'future')==baseline


def test_owner_witness_alternative_cannot_replace_only_consumed_receipt():
    scene,state=twice()
    bad=replace(scene,relevance=(replace(scene.relevance[0],observer='other_P'),))
    with pytest.raises(Refusal,match='SOURCE_PREIMAGE_IDENTITY_COLLISION'):
        eligible(bad,state,'future')


def test_legitimate_third_party_witness_replacement_after_proposal_denied():
    scene,state=seeded_past()
    choice=next(c for c in eligible(scene,state,'later') if c.mode=='NARROW')
    p=propose(scene,state,'later',choice.id)
    unchanged_state=state.hash()
    witnessed=observe(scene, history_observer='peer')
    assert any(c.id==choice.id for c in eligible(witnessed,state,'later'))
    with pytest.raises(Refusal,match='PROPOSAL_RECOMPUTATION_FAILED'):
        append_test_only(witnessed,state,p,fixture_grant(p,'child'))
    assert state.hash()==unchanged_state


def test_old_rule_digest_rewritten_to_valid_content_hash_is_refused_on_future():
    scene,state=twice()
    original=state.lineage[0]
    fake=replace(original,rule_hash='0'*64)
    fields=asdict(fake);fields.pop('hash')
    fake=replace(fake,hash=digest(fields))
    newer=replace(state,lineage=(fake,)+state.lineage[1:])
    with pytest.raises(Refusal,match='LINEAGE_PARENT_INVALID|HISTORICAL_RULE_IDENTITY_UNQUALIFIED'):
        eligible(scene,newer,'future')
    assert original.rule_hash==RULE_HASH


def test_future_rule_digest_rewritten_to_valid_content_hash_is_refused():
    scene,state=seeded_past()
    original=state.lineage[0]
    fake=replace(original,rule_hash='1'*64)
    fields=asdict(fake);fields.pop('hash')
    newer=replace(state,lineage=(replace(fake,hash=digest(fields)),))
    with pytest.raises(Refusal,match='HISTORICAL_RULE_IDENTITY_UNQUALIFIED'):
        eligible(scene,newer,'later')


def test_original_rule_readset_and_two_successive_records_remain_consistent():
    scene,state=twice()
    assert all(r.rule_hash==RULE_HASH for r in state.lineage)
    assert len(state.lineage)==2
    assert eligible(scene,state,'future')


def test_no_change_still_preserves_exact_state_when_owner_witness_is_disqualified():
    scene,state=seeded_past()
    scene=observe(scene,history_observer='other_P')
    assert {x.mode for x in eligible(scene,state,'later')}=={'NO_CHANGE'}
    c=eligible(scene,state,'later')[0]
    p=propose(scene,state,'later',c.id)
    grant=fixture_grant(p,'child')
    before=state.hash()
    assert append_test_only(scene,state,p,grant) is state
    assert audit_no_change(scene,state,p,grant).state_before_hash==before
    assert state.hash()==before


def test_actor_owner_can_be_independent_person_without_being_a_witness():
    scene,state=seeded_past()
    # Replacing the action-owner's observed participation by the observer's
    # independent evidence must never change the owner of the historical action.
    event=t9(scene)
    assert event.action_owner=='other_P'
    assert event.observer=='child'
    assert scene.relevance[0].observed_action_owner=='other_P'
    assert next(h for h in scene.actors[0].history if h.id=='later_observed_counterpart').observed_action_owner=='other_P'
    assert {x.mode for x in eligible(scene,state,'later')}=={
        'NO_CHANGE','REATTRIBUTE','NARROW','GENERALIZE','REINFORCE','CONTRADICT','DIFFERENTIATE'
    }
