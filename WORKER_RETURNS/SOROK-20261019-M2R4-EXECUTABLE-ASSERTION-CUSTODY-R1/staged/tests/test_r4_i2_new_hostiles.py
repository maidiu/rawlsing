"""Independent executable implementation of the 12 frozen R4-I2 prospective cases.

Plan source: WORKER_RETURNS/SOROK-20261018-M2R4-RULE-WITNESS-INDEPENDENT-I2-R1/
test_plan_preregistered.json at 8e74be26d14dae270ed6723d5e878f59446c94bd.
The claim IDs and expected oracles are unchanged. No R4 candidate or frozen test
was edited. All scenes, witnesses and grants are synthetic TEST_ONLY fixtures.
"""
from dataclasses import asdict, replace

import pytest

from kernel import (
    MODES, RULE_HASH, Actor, History, HistoryWitness, Refusal, State,
    append_test_only, audit_no_change, digest, eligible, fixture_grant,
    objective_event_hash, propose, validate,
)
from test_heldout_actor_independence import seeded_past
from test_local_hostile import twice

RELATION_MODES = set(MODES) - {"NO_CHANGE"}
R3_RULE_HASH = "8cc1f8495ee84170f77df0532f21c077b630de3af2d72d3c6f5dd7793eec9ece"


def observe(scene, *, action_event_observer=None, relevance_observer=None,
            history_observer=None):
    later = next(e for e in scene.events if e.id == "later")
    if action_event_observer is not None:
        changed_event = replace(later, observer=action_event_observer)
        scene = replace(
            scene,
            events=tuple(changed_event if e.id == "later" else e for e in scene.events),
            relevance=tuple(
                replace(x, later_event_hash=objective_event_hash(changed_event))
                if x.later_event_id == "later" else x
                for x in scene.relevance),
        )
    if relevance_observer is not None:
        scene = replace(scene, relevance=tuple(
            replace(x, observer=relevance_observer) for x in scene.relevance))
    if history_observer is not None:
        scene = replace(scene, history_witnesses=tuple(
            replace(w, observer=history_observer)
            if w.actor == "child" and w.history_id == "later_observed_counterpart"
            else w for w in scene.history_witnesses))
    validate(scene)
    return scene


def modes(scene, state):
    return {c.mode for c in eligible(scene, state, "later")}


def test_i2n01_forged_rule_digest():
    """Recomputed content digest does not authorize an arbitrary rule hash."""
    scene, state = seeded_past()
    original = state.lineage[0]
    forged = replace(original, rule_hash="f" * 64)
    fields = asdict(forged)
    fields.pop("hash")
    forged = replace(forged, hash=digest(fields))
    tampered = replace(state, lineage=(forged,))
    with pytest.raises(Refusal, match="HISTORICAL_RULE_IDENTITY_UNQUALIFIED"):
        eligible(scene, tampered, "later")


def test_i2n02_event_owner_self_observer():
    """Owner-as-objective-event-observer cannot support other-person modes."""
    scene, state = seeded_past()
    changed = observe(scene, action_event_observer="other_P")
    assert modes(changed, state) == {"NO_CHANGE"}


def test_i2n03_relevance_owner_self_observer():
    """Owner-as-Relevance.observer cannot support other-person modes."""
    scene, state = seeded_past()
    changed = observe(scene, relevance_observer="other_P")
    assert modes(changed, state) == {"NO_CHANGE"}


def test_i2n04_history_owner_self_observer():
    """Owner-as-HistoryWitness.observer cannot support other-person modes."""
    scene, state = seeded_past()
    changed = observe(scene, history_observer="other_P")
    assert modes(changed, state) == {"NO_CHANGE"}


def test_i2n05_shared_nonowner_observer_positive():
    """All three channels may name the same non-owner observer and remain eligible."""
    scene, state = seeded_past()
    changed = observe(scene, action_event_observer="peer",
                      relevance_observer="peer", history_observer="peer")
    assert modes(changed, state) == set(MODES)
    assert RELATION_MODES <= modes(changed, state)


def test_i2n06_other_q_positive():
    """A second distinct other with real independent project supplies the option."""
    scene, state = seeded_past()
    other_q = Actor(
        "other_Q",
        (History("other_q_project", "other_Q", 3, "own_other_project", True, False),),
        ("later",), "own_other_project", 19, "unspecified")
    later = next(e for e in scene.events if e.id == "later")
    changed_later = replace(later, participants=("child", "other_Q"),
                            action_owner="other_Q")
    child = scene.actors[0]
    child_history = tuple(
        replace(h, observed_action_owner="other_Q")
        if h.id == "later_observed_counterpart" else h for h in child.history)
    child = replace(child, history=child_history)
    witnesses = []
    for witness in scene.history_witnesses:
        if witness.actor == "child" and witness.history_id == "later_observed_counterpart":
            observed = next(h for h in child_history
                            if h.id == "later_observed_counterpart")
            witness = replace(witness, history_hash=digest(asdict(observed)))
        witnesses.append(witness)
    q_history = other_q.history[0]
    witnesses.append(HistoryWitness(
        q_history.id, digest(asdict(q_history)), "other_Q", "caregiver",
        q_history.time, "actor_activity", "INDEPENDENT_PROJECT"))
    relevance = replace(scene.relevance[0],
                        later_event_hash=objective_event_hash(changed_later),
                        observed_action_owner="other_Q")
    changed = replace(
        scene, actors=(child,) + scene.actors[1:] + (other_q,),
        events=tuple(changed_later if e.id == "later" else e for e in scene.events),
        history_witnesses=tuple(witnesses), relevance=(relevance,))
    validate(changed)
    assert modes(changed, state) == set(MODES)


def test_i2n07_future_history_t10_cannot_prove_t9():
    """A future history/witness/relevance cannot authorize a t9 possibility."""
    scene, state = seeded_past()
    child = scene.actors[0]
    past = next(h for h in child.history if h.id == "later_observed_counterpart")
    future = replace(past, time=10)
    witnesses = tuple(
        replace(w, time=10, history_hash=digest(asdict(future)))
        if w.actor == "child" and w.history_id == past.id else w
        for w in scene.history_witnesses)
    changed = replace(
        scene,
        actors=(replace(child, history=tuple(
            future if h.id == past.id else h for h in child.history)),)
        + scene.actors[1:],
        history_witnesses=witnesses,
        relevance=(replace(scene.relevance[0], time=10),))
    validate(changed)
    assert modes(changed, state) == {"NO_CHANGE"}


def test_i2n08_consumed_witness_change_postproposal():
    """A consumed witness changed after proposal must refuse the same append."""
    scene, state = seeded_past()
    choice = next(c for c in eligible(scene, state, "later") if c.mode == "NARROW")
    proposal = propose(scene, state, "later", choice.id)
    changed = observe(scene, history_observer="peer")
    with pytest.raises(Refusal, match="PROPOSAL_RECOMPUTATION_FAILED"):
        append_test_only(changed, state, proposal, fixture_grant(proposal, "child"))


def test_i2n09_unconsumed_alternative_stable():
    """An added disqualified alternative cannot rewrite the consumed lineage."""
    scene, state = twice()
    baseline = eligible(scene, state, "future")
    owner_attests = replace(scene.relevance[0], observer="other_P")
    changed = replace(scene, relevance=scene.relevance + (owner_attests,))
    assert eligible(changed, state, "future") == baseline


def test_i2n10_old_version_rule_unqualified():
    """A legacy @0.4.1 rehashed rule cannot migrate silently to @0.4.2."""
    scene, state = seeded_past()
    original = state.lineage[0]
    old = replace(original, rule_hash=R3_RULE_HASH)
    fields = asdict(old)
    fields.pop("hash")
    old = replace(old, hash=digest(fields))
    with pytest.raises(Refusal, match="HISTORICAL_RULE_IDENTITY_UNQUALIFIED"):
        eligible(scene, replace(state, lineage=(old,)), "later")


def test_i2n11_nochange_unchanged_state():
    """Disqualify the only witness channel; NO_CHANGE must be non-mutating."""
    scene, state = seeded_past()
    scene = observe(scene, history_observer="other_P")
    assert modes(scene, state) == {"NO_CHANGE"}
    candidate = eligible(scene, state, "later")[0]
    proposal = propose(scene, state, "later", candidate.id)
    grant = fixture_grant(proposal, "child")
    before = state.hash()
    returned = append_test_only(scene, state, proposal, grant)
    assert returned is state
    assert state.hash() == before
    assert audit_no_change(scene, state, proposal, grant).state_before_hash == before


def test_i2n12_consumed_source_replaced_on_continuation():
    """Replacing a consumed relevance source must fail on continuation."""
    scene, state = twice()
    changed = replace(
        scene, relevance=(replace(scene.relevance[0],
                                  observed_action_owner="caregiver"),))
    validate(changed)
    with pytest.raises(Refusal, match="SOURCE_PREIMAGE_IDENTITY_COLLISION"):
        eligible(changed, state, "future")
