"""Freshly authored independent I2 cases. Not part of the M2 R3 author's 135.

Expected scientific boundaries are explicit. A RED is retained as an adverse finding,
not silently patched. All actors, witnesses and grants here are synthetic test fixtures.
"""
from dataclasses import asdict, replace
import pytest
from kernel import (
    Refusal, State, MODES, append_test_only, digest, eligible,
    fixture_grant, propose, seed_scene, validate,
)
from test_heldout_actor_independence import seeded_past
from test_local_hostile import twice

MODES_REL = set(MODES)-{'NO_CHANGE'}


def test_i2_01_historical_lineage_rule_hash_must_not_accept_a_different_rule():
    scene, state = seeded_past()
    old = state.lineage[0]
    forged = replace(old, rule_hash='DIFFERENT_UNISSUED_RULE_HASH')
    fields = asdict(forged)
    fields.pop('hash')
    forged = replace(forged, hash=digest(fields))  # attacker recomputes unkeyed content digest
    tampered = replace(state, lineage=(forged,))
    assert tampered.lineage[0].rule_hash != old.rule_hash
    validate(scene)
    with pytest.raises(Refusal, match='RULE|LINEAGE_INTEGRITY'):
        eligible(scene, tampered, 'later')


def test_i2_02_other_owner_cannot_be_sole_witness_of_own_action_and_child_observation():
    scene, state = seeded_past()
    owner='other_P'
    # Every first-hand action/observation receipt now relies solely on the action
    # owner. The unrelated past INDEPENDENT_PROJECT retains its earlier witness.
    later=next(e for e in scene.events if e.id=='later')
    changed_event=replace(later,observer=owner)
    changed_events=tuple(changed_event if e.id=='later' else e for e in scene.events)
    rev=tuple(replace(r,observer=owner,later_event_hash=digest(asdict(changed_event)))
              if r.later_event_id=='later' else r for r in scene.relevance)
    witnesses=tuple(replace(w,observer=owner)
              if w.actor=='child' and w.history_id=='later_observed_counterpart' else w
              for w in scene.history_witnesses)
    changed=replace(scene,events=changed_events,relevance=rev,history_witnesses=witnesses)
    validate(changed)
    assert owner==changed.relevance[0].observer
    modes={c.mode for c in eligible(changed,state,'later')}
    assert modes=={'NO_CHANGE'}, f'SELF_ATTESTED_COUNTERPART_ACTION_ADMITTED: {sorted(modes)}'


def test_i2_03_unconsumed_alternative_may_expire_between_proposal_and_append():
    scene,state=seeded_past()
    alternative=replace(scene.relevance[0],observer='peer')
    scene=replace(scene,relevance=scene.relevance+(alternative,))
    proposal=propose(scene,state,'later',next(c.id for c in eligible(scene,state,'later') if c.mode=='NO_CHANGE'))
    assert not any(x[0].startswith('RELATION_') for x in proposal['source_preimages'])
    # For an actual consumed relation, continue from valid earlier history.
    scene, state=seeded_past()
    alternative=replace(scene.relevance[0],observer='peer')
    scene=replace(scene,relevance=scene.relevance+(alternative,))
    selected=next(c for c in eligible(scene,state,'later') if c.mode=='DIFFERENTIATE')
    p=propose(scene,state,'later',selected.id)
    consumed=next(z[2] for z in p['source_preimages'] if z[0]=='RELATION_RELEVANCE')
    changed_receipts=tuple(replace(r,time=99) if digest(asdict(r))!=consumed else r for r in scene.relevance)
    changed=replace(scene,relevance=changed_receipts)
    assert any(digest(asdict(r))==consumed for r in changed.relevance)
    done=append_test_only(changed,state,p,fixture_grant(p,'child'))
    assert done.lineage[-1].source_preimages==p['source_preimages']


def test_i2_04_future_observed_history_and_reissued_clock_do_not_enable_relation():
    scene,state=seeded_past()
    child=scene.actors[0]
    past=next(h for h in child.history if h.id=='later_observed_counterpart')
    future=replace(past,time=10)
    witnesses=tuple(replace(w,time=10,history_hash=digest(asdict(future)))
           if w.actor=='child' and w.history_id==past.id else w
           for w in scene.history_witnesses)
    changed=replace(scene,actors=(replace(child,history=tuple(future if h.id==past.id else h for h in child.history)),)+scene.actors[1:],
                    history_witnesses=witnesses,relevance=(replace(scene.relevance[0],time=10),))
    validate(changed)
    assert {c.mode for c in eligible(changed,state,'later')}=={'NO_CHANGE'}


def test_i2_05_late_consumed_action_owner_source_cannot_be_rewritten_for_future():
    scene,state=twice()
    receipt=replace(scene.relevance[0], observed_action_owner='caregiver')
    changed=replace(scene,relevance=(receipt,))
    validate(changed)
    with pytest.raises(Refusal,match='SOURCE_PREIMAGE_IDENTITY_COLLISION'):
        eligible(changed,state,'future')


def test_i2_06_nochange_denies_psychological_state_mutation_with_different_grant():
    scene,state=seeded_past()
    before=state.hash()
    c=next(c for c in eligible(scene,state,'later') if c.mode=='NO_CHANGE')
    p=propose(scene,state,'later',c.id)
    legitimate=fixture_grant(p,'child')
    assert append_test_only(scene,state,p,legitimate) is state
    assert state.hash()==before
    with pytest.raises(Refusal,match='OWNER_PERMISSION_NOT_GRANTED'):
        append_test_only(scene,state,p,dict(legitimate,issuer='BAD_ISSUER'))
    assert state.hash()==before
