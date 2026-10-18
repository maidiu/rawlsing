"""HQ329 M3 strict RED reproducer, independently authored after pinning M2@5c2fbe14.
Run with exact M2 kernel.py in PYTHONPATH. This suite is INTENTIONALLY RED against M2.
These tests never mutate M2 source or the frozen M1/I2 cases.
"""
from dataclasses import replace, asdict
import pytest
from kernel import (seed_scene, State, eligible, propose, fixture_grant,
                    append_test_only, digest, Refusal)

def fixed_t6_interpretation():
    scene = seed_scene()
    state = State('child', procedure_refs=('old_watchful_habit',))
    option = next(c for c in eligible(scene, state, 'discussion')
                  if c.source == 'parent_said' and c.stance == 'REJECT')
    proposal = propose(scene, state, 'discussion', option.id,
                       affect_ref='first_distress', public_action_ref='public_lock_check')
    return scene, append_test_only(scene, state, proposal, fixture_grant(proposal, 'child'))

def test_R3_01_past_heard_words_cannot_change_without_current_lineage_source_collision():
    scene, state = fixed_t6_interpretation()
    changed_words = replace(scene.speech[0], words='It was definitely the children of group Z.')
    changed = replace(scene, speech=(changed_words,) + scene.speech[1:],
        speech_actions=(replace(scene.speech_actions[0],
                                speech_hash=digest(asdict(changed_words))),) + scene.speech_actions[1:],
        exposures=(replace(scene.exposures[0],
                           speech_hash=digest(asdict(changed_words))),) + scene.exposures[1:])
    with pytest.raises(Refusal, match='SOURCE_PREIMAGE|SOURCE_IDENTITY_COLLISION'):
        eligible(changed, state, 'later')

def test_R3_02_prior_practical_orientation_cannot_change_unnoticed_after_lineage_append():
    scene, state = fixed_t6_interpretation()
    child = scene.actors[0]
    changed_habit = replace(child.history[1],
                            activity='fully different old practical orientation')
    changed_witnesses = tuple(
        replace(w, history_hash=digest(asdict(changed_habit)))
        if w.actor == 'child' and w.history_id == changed_habit.id else w
        for w in scene.history_witnesses)
    changed = replace(scene,
        actors=(replace(child, history=child.history[:1] + (changed_habit,) + child.history[2:]),)
               + scene.actors[1:],
        history_witnesses=changed_witnesses)
    with pytest.raises(Refusal, match='SOURCE_PREIMAGE|SOURCE_IDENTITY_COLLISION'):
        eligible(changed, state, 'later')

def test_R3_03_earlier_affective_witness_rewrite_cannot_change_historical_lineage_source():
    scene, state = fixed_t6_interpretation()
    child = scene.actors[0]
    changed_affect = replace(child.history[2],
                             activity='happy delight instead of distress')
    changed_witnesses = tuple(
        replace(w, history_hash=digest(asdict(changed_affect)))
        if w.actor == 'child' and w.history_id == changed_affect.id else w
        for w in scene.history_witnesses)
    changed = replace(scene,
        actors=(replace(child, history=child.history[:2] + (changed_affect,) + child.history[3:]),)
               + scene.actors[1:],
        history_witnesses=changed_witnesses)
    with pytest.raises(Refusal, match='SOURCE_PREIMAGE|SOURCE_IDENTITY_COLLISION'):
        eligible(changed, state, 'later')
