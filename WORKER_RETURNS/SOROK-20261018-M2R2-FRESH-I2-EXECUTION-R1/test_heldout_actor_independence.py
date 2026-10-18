"""Fresh I2 heldout, not a modification of any R2 committed test.
Expected scientific law: self-owned action is NOT independent counterpart-action evidence.
"""
from dataclasses import replace,asdict
import hashlib
import pytest
from kernel import (
    seed_scene, State, eligible, propose, append_test_only, fixture_grant,
    History, HistoryWitness, objective_event_hash, digest, MODES, validate
)

RELATION_MODES=set(MODES)-{'NO_CHANGE'}

def seeded_past():
    scene=seed_scene()
    state=State('child',procedure_refs=('old_watchful_habit',))
    c=next(c for c in eligible(scene,state,'discussion') if c.source=='parent_said' and c.stance=='REJECT')
    p=propose(scene,state,'discussion',c.id,affect_ref='first_distress',public_action_ref='public_lock_check')
    return scene,append_test_only(scene,state,p,fixture_grant(p,'child'))

def with_child_independent_action(scene):
    """Same t9 counterpart-material action, with child the actual lawful action owner."""
    independent=History('child_independent_project','child',7,'repair_bicycle',True,False)
    witness=HistoryWitness(independent.id,digest(asdict(independent)),'child','caregiver',7,'actor_activity','INDEPENDENT_PROJECT')
    child=replace(scene.actors[0],history=scene.actors[0].history+(independent,))
    later=next(x for x in scene.events if x.id=='later')
    later=replace(later,action_owner='child')
    changed_events=tuple(later if x.id=='later' else x for x in scene.events)
    relevance=tuple(replace(x,later_event_hash=objective_event_hash(later)) if x.later_event_id=='later' else x for x in scene.relevance)
    return replace(scene,actors=(child,)+scene.actors[1:], events=changed_events,history_witnesses=scene.history_witnesses+(witness,),relevance=relevance)

def test_genuine_other_owned_counterpart_is_positive():
    scene,state=seeded_past()
    validate(scene)
    assert next(e for e in scene.events if e.id=='later').action_owner=='other_P'
    modes={c.mode for c in eligible(scene,state,'later')}
    assert RELATION_MODES <= modes


def test_child_self_action_must_not_be_admitted_as_counterpart():
    scene,state=seeded_past()
    own=with_child_independent_action(scene)
    validate(own)  # separately proves actual valid scene; no malformed-fixture refusal
    assert next(e for e in own.events if e.id=='later').action_owner=='child'
    assert own.relevance[0].observer!='child'
    assert own.relevance[0].later_event_hash==objective_event_hash(next(e for e in own.events if e.id=='later'))
    modes={c.mode for c in eligible(own,state,'later')}
    assert modes=={'NO_CHANGE'}, f'CHILD_SELF_ACTION_WRONGLY_ADMITTED_AS_COUNTERPART: {sorted(modes)}'
