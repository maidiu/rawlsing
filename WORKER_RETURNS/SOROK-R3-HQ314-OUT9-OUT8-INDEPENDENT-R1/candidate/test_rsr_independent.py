"""HQ299 RSR independent source-free boundary tests against exact SR prototype.

Tests starting with test_red_ are intended to be *strict independent
acceptance requirements*. Failures are retained as actual review findings;
they do not modify frozen S01--S28 tests or assert accepted ADP019 authority.
"""
from __future__ import annotations
import copy
from outbox_prototype import make_prototype, DeliveryState, _hash


def candidate(label, **payload):
    return {"candidate_id": label, "payload": payload}


def admitted():
    p = make_prototype()
    e = p.ledger.admit(candidate("SOURCEFREE", utterance="I quit."))
    return p,e


def test_positive_same_candidate_replay_returns_same_event_no_extra_admit():
    p,e = admitted()
    twice = p.ledger.admit(candidate("SOURCEFREE", utterance="I quit."))
    assert twice == e
    assert p.ledger.count() == 1


def test_positive_false_testimony_does_not_directly_mutate_world_truth():
    p=make_prototype()
    p.world_state["employment"] = "fired"
    e=p.ledger.admit(candidate("UTTERANCE", utterance="I quit."))
    assert e is not None and e["payload"]["utterance"] == "I quit."
    assert p.world_state["employment"] == "fired"


def test_positive_delivery_ack_does_not_automatically_call_perceive():
    p,e=admitted(); eid=e["occurrence_id"]
    p.outbox.emit(eid);p.outbox.deliver(eid);p.outbox.ack(eid)
    assert not p.projection.has_perceived("user-A",eid)
    assert p.outbox.deliveries[eid]["state"] == DeliveryState.ACKNOWLEDGED.value


def test_positive_same_admitted_event_can_be_differently_offered():
    p,e=admitted(); eid=e["occurrence_id"]
    assert p.projection.offer("viewer-A", eid)
    assert not p.projection.has_opportunity("viewer-B", eid)
    assert p.ledger.count() == 1


def test_red_perceive_without_offer_or_delivery_must_refuse():
    p,e=admitted(); eid=e["occurrence_id"]
    # Calling a client perception API should not be able to assert the user
    # perceived an event which was never emitted or even offered.
    assert p.projection.perceive("user-A",eid) is False
    assert not p.projection.has_perceived("user-A",eid)


def test_red_offer_unknown_unadmitted_event_must_refuse():
    p=make_prototype()
    assert p.projection.offer("user-A","OCC-9999") is False
    assert not p.projection.has_opportunity("user-A","OCC-9999")


def test_red_emit_unknown_unadmitted_event_must_refuse():
    p=make_prototype()
    assert p.outbox.emit("OCC-9999") == DeliveryState.NOT_SENT
    assert "OCC-9999" not in p.outbox.deliveries


def test_red_snapshot_restore_must_revert_user_opportunity():
    p,e=admitted(); eid=e["occurrence_id"]
    before=p.snapshot()
    p.projection.offer("user-A",eid)
    p.restore(before)
    assert not p.projection.has_opportunity("user-A",eid)


def test_red_snapshot_restore_must_preserve_committed_opportunity():
    p,e=admitted(); eid=e["occurrence_id"]
    p.projection.offer("user-A",eid)
    committed=p.snapshot()
    second=make_prototype();second.restore(copy.deepcopy(committed))
    assert second.projection.has_opportunity("user-A",eid)


def test_red_mutable_candidate_payload_cannot_rewrite_committed_event():
    p=make_prototype()
    payload={"utterance":"I quit.","extra":{"truth":"not quit"}}
    e=p.ledger.admit({"candidate_id":"C-TEST", "payload":payload})
    asserted=copy.deepcopy(e["payload"])
    payload["extra"]["truth"]="quit"
    assert e["payload"] == asserted
    assert e["content_hash"] == _hash(e["payload"])


def test_red_mutable_external_event_view_cannot_edit_ledger():
    p,e=admitted()
    e["payload"]["utterance"]="I actually quit."
    stored=p.ledger.get(e["occurrence_id"])
    assert stored["content_hash"] == _hash(stored["payload"])


def test_red_snapshot_is_immutable_against_subsequent_nested_event_mutation():
    p=make_prototype()
    e=p.ledger.admit({"candidate_id":"IMM", "payload":{"utterance":"Hello", "nested":{"x":1}}})
    snap=p.snapshot()
    e["payload"]["nested"]["x"]=2
    assert snap["ledger"][0]["payload"]["nested"]["x"] == 1


def test_red_source_refs_are_part_of_admission_identity():
    p=make_prototype()
    first={"candidate_id":"C1", "payload":{"utterance":"I quit"}, "source_refs":["AUTH_A"]}
    second={"candidate_id":"C1", "payload":{"utterance":"I quit"}, "source_refs":["AUTH_B"]}
    original=p.ledger.admit(first)
    newer=p.ledger.admit(second)
    assert newer is None  # same content, changed source/authorization != same event
    assert original["source_refs"] == ["AUTH_A"]


def test_red_untyped_world_fact_claim_in_actor_utterance_cannot_be_admitted_as_event():
    p=make_prototype();p.world_state["employment"]="fired"
    # A user's or actor's utterance can be admitted as an utterance, but its
    # side-car alleged objective employment transition lacks world-owner rule.
    e=p.ledger.admit(candidate("FALSE-FACT", utterance="I quit.",
                               objective_employment_transition="quit"))
    assert e is None
    assert p.world_state["employment"] == "fired"


def test_red_missing_causal_time_requires_hold_not_occurrence():
    p=make_prototype()
    e=p.ledger.admit({"candidate_id":"NO-TIME", "payload":{"utterance":"Hello"},"causal_time":None})
    assert e is None
    assert p.ledger.count() == 0


def test_red_missing_admission_source_must_not_be_assumed_adp019():
    p=make_prototype()
    e=p.ledger.admit({"candidate_id":"NO-AUTH", "payload":{"utterance":"Hello"},"source_refs":[]})
    assert e is None


def test_red_display_ack_does_not_authorize_ghost_offer_to_other_viewers():
    p,e=admitted(); eid=e["occurrence_id"]
    p.outbox.emit(eid);p.outbox.deliver(eid);p.outbox.ack(eid)
    assert not p.projection.has_opportunity("viewer-A", eid)
    assert not p.projection.has_opportunity("viewer-B", eid)
    # ACK cannot *by itself* make a viewer have perceived.
    assert not p.projection.has_perceived("viewer-A", eid)
    assert not p.projection.has_perceived("viewer-B", eid)
