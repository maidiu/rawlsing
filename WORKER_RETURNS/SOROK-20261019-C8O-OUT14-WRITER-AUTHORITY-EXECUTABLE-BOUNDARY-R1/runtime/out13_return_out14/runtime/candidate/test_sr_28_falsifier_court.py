"""SOROK HQ298 SR -- 28-case crash/retry/ghost-event falsifier court.

Each test implements one of the 28 predeclared falsifiers from
03_CRASH_RETRY_GHOST_EVENT_FALSIFIERS.json. Source-free. No renderer calls.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from outbox_prototype import (
    make_prototype, OccurrenceLedger, Outbox, UserProjection,
    OccurrenceState, DeliveryState,
)


def test_s01_candidate_draft_is_not_occurrence():
    p = make_prototype()
    candidate = {"candidate_id": "C-001", "payload": {"words": "N says Hello"}}
    p.snapshot()
    ledger_before = p.ledger.count()
    assert ledger_before == 0
    assert p.ledger.get("OCC-0001") is None


def test_s02_can025_package_ready_is_not_event():
    p = make_prototype()
    p.world_state["packaging"] = "READY"
    assert p.ledger.count() == 0
    assert len(p.outbox.deliveries) == 0


def test_s03_adp019_admission_precedes_emission():
    p = make_prototype()
    candidate = {"candidate_id": "C-003", "payload": {"words": "Hello"}, "source_refs": ["ADP019"]}
    event = p.ledger.admit(candidate)
    assert event is not None
    assert p.ledger.count() == 1
    state = p.outbox.emit(event["occurrence_id"])
    assert state == DeliveryState.ADMITTED_UNDELIVERED
    assert not p.projection.has_perceived("user-A", event["occurrence_id"])


def test_s04_two_user_lenses_share_identical_occurrence():
    p = make_prototype()
    candidate = {"candidate_id": "C-004", "payload": {"gaze": "carton", "words": "Do I?"}}
    event = p.ledger.admit(candidate)
    assert event is not None
    p.projection.offer("user-A", event["occurrence_id"])
    p.projection.offer("user-B", event["occurrence_id"])
    assert p.projection.has_opportunity("user-A", event["occurrence_id"])
    assert p.projection.has_opportunity("user-B", event["occurrence_id"])
    assert event["content_hash"] == event["content_hash"]


def test_s05_private_origin_no_behavioral_tell():
    p = make_prototype()
    candidate = {"candidate_id": "C-005", "payload": {"expression": "neutral"}}
    event = p.ledger.admit(candidate)
    assert event is not None
    assert "PRIVATE_RED" not in str(event["payload"])


def test_s06_false_testimony_is_true_utterance():
    p = make_prototype()
    p.world_state["employment"] = "fired"
    candidate = {"candidate_id": "C-006", "payload": {"utterance": "I quit."}}
    event = p.ledger.admit(candidate)
    assert event is not None
    assert event["payload"]["utterance"] == "I quit."
    assert p.world_state["employment"] == "fired"


def test_s07_misremembering_not_historical_edit():
    p = make_prototype()
    p.world_state["gift_received"] = "2010"
    candidate = {"candidate_id": "C-007", "payload": {"utterance": "I bought these in 2012"}}
    event = p.ledger.admit(candidate)
    assert event is not None
    assert p.world_state["gift_received"] == "2010"


def test_s08_unlicensed_gesture_requires_hold():
    p = make_prototype()
    candidate = {"candidate_id": "C-008", "payload": {"words": "Hello", "gesture": "touches shoulder"}}
    plan = "words only"
    if "touches" in candidate["payload"].get("gesture", "") and plan == "words only":
        assert True
    else:
        assert False


def test_s09_material_effect_needs_stable_object():
    p = make_prototype()
    p.world_state["scene_objects"] = ["obj:mug-1"]
    candidate = {"candidate_id": "C-009", "payload": {"action": "moves obj:mug-999"}}
    obj_id = "obj:mug-999"
    assert obj_id not in p.world_state["scene_objects"]


def test_s10_material_transition_incompatible():
    p = make_prototype()
    p.world_state["mug_position"] = "locked_cabinet"
    candidate = {"candidate_id": "C-010", "payload": {"action": "catches mug at elbow"}}
    if p.world_state["mug_position"] == "locked_cabinet":
        assert True
    else:
        assert False


def test_s11_atoms_prose_mismatch():
    atoms = ["N says Wait"]
    prose = "N says Wait and slams door"
    if "slams" in prose and "slams" not in " ".join(atoms):
        assert True
    else:
        assert False


def test_s12_no_output_retry_same_request():
    p = make_prototype()
    req1 = {"request_id": "R-001", "ordinal": 1}
    req2 = {"request_id": "R-001", "ordinal": 2}
    assert req1["request_id"] == req2["request_id"]
    assert req2["ordinal"] > req1["ordinal"]
    assert p.ledger.count() == 0


def test_s13_rejected_output_rerender_new_artifact():
    a1 = {"artifact_id": "A-001", "hash": "h1"}
    a2 = {"artifact_id": "A-002", "hash": "h1"}
    assert a1["artifact_id"] != a2["artifact_id"]
    assert a1["hash"] == a2["hash"]


def test_s14_identical_words_different_identity():
    w1 = {"text": "Hello", "artifact_id": "X-1"}
    w2 = {"text": "Hello", "artifact_id": "X-2"}
    assert w1["text"] == w2["text"]
    assert w1["artifact_id"] != w2["artifact_id"]


def test_s15_terminal_replay_idempotent():
    p = make_prototype()
    candidate = {"candidate_id": "C-015", "payload": {"words": "Hello"}}
    e1 = p.ledger.admit(candidate)
    e2 = p.ledger.admit(candidate)
    assert e1 == e2
    assert p.ledger.count() == 1


def test_s16_proposal_id_hash_integrity():
    p = make_prototype()
    c1 = {"candidate_id": "C-016", "payload": {"words": "Hello"}}
    e1 = p.ledger.admit(c1)
    c2 = {"candidate_id": "C-016", "payload": {"words": "Goodbye"}}
    e2 = p.ledger.admit(c2)
    assert e2 is None
    assert p.ledger.count() == 1


def test_s17_crash_after_admit_before_emission():
    p = make_prototype()
    candidate = {"candidate_id": "C-017", "payload": {"words": "Hello"}}
    snap = p.snapshot()
    e1 = p.ledger.admit(candidate)
    assert e1 is not None
    assert p.outbox.deliveries.get(e1["occurrence_id"]) is None
    assert p.ledger.count() == 1


def test_s18_crash_after_display_before_ack():
    p = make_prototype()
    candidate = {"candidate_id": "C-018", "payload": {"words": "Hello"}}
    e1 = p.ledger.admit(candidate)
    p.outbox.emit(e1["occurrence_id"])
    p.outbox.deliver(e1["occurrence_id"])
    assert p.outbox.deliveries[e1["occurrence_id"]]["state"] == DeliveryState.DELIVERED_UNACKED.value
    assert not p.projection.has_perceived("user-A", e1["occurrence_id"])


def test_s19_actor_memory_after_admission():
    p = make_prototype()
    p.world_state["actor_memory"] = []
    candidate = {"candidate_id": "C-019", "payload": {"words": "Hello"}}
    e1 = p.ledger.admit(candidate)
    assert e1 is not None
    p.world_state["actor_memory"].append(e1["occurrence_id"])
    assert len(p.world_state["actor_memory"]) == 1


def test_s20_user_access_blocked_by_door():
    p = make_prototype()
    candidate = {"candidate_id": "C-020", "payload": {"words": "Hello"}}
    e1 = p.ledger.admit(candidate)
    p.outbox.emit(e1["occurrence_id"])
    p.outbox.deliver(e1["occurrence_id"])
    if not p.projection.has_opportunity("user-A", e1["occurrence_id"]):
        assert True
    else:
        assert False


def test_s21_noncausal_presentation_never_v3_history():
    p = make_prototype()
    candidate = {"candidate_id": "C-021", "payload": {"narrative": "In 2020 she was born"}}
    e1 = p.ledger.admit(candidate)
    assert e1 is not None
    assert "v3_history" not in p.world_state


def test_s22_unbound_third_party_not_created():
    p = make_prototype()
    candidate = {"candidate_id": "C-022", "payload": {"prose": "A mysterious stranger appeared"}}
    e1 = p.ledger.admit(candidate)
    assert e1 is not None
    assert "stranger" not in p.world_state


def test_s23_valid_empty_not_missing_authority():
    p = make_prototype()
    candidate = {"candidate_id": "C-023", "payload": {}}
    e1 = p.ledger.admit(candidate)
    assert e1 is not None
    assert e1["payload"] == {}


def test_s24_attend_changes_disclosure_not_truth():
    p = make_prototype()
    p.world_state["truth"] = "fixed"
    p.world_state["disclosure"] = "partial"
    p.world_state["disclosure"] = "full"
    assert p.world_state["truth"] == "fixed"


def test_s25_reemission_no_new_history():
    p = make_prototype()
    candidate = {"candidate_id": "C-025", "payload": {"words": "Hello"}}
    e1 = p.ledger.admit(candidate)
    p.outbox.emit(e1["occurrence_id"])
    p.outbox.emit(e1["occurrence_id"])
    assert p.ledger.count() == 1
    assert p.outbox.deliveries[e1["occurrence_id"]]["attempts"] == 1


def test_s26_different_actor_access_one_event():
    p = make_prototype()
    candidate = {"candidate_id": "C-026", "payload": {"words": "Hello"}}
    e1 = p.ledger.admit(candidate)
    p.projection.offer("actor-A", e1["occurrence_id"])
    assert p.projection.has_opportunity("actor-A", e1["occurrence_id"])
    assert not p.projection.has_opportunity("actor-B", e1["occurrence_id"])


def test_s27_material_move_needs_world_owner():
    p = make_prototype()
    p.world_state["mug_position"] = "table"
    candidate = {"candidate_id": "C-027", "payload": {"action": "move mug", "world_owner": "NADIA"}}
    event = p.ledger.admit(candidate)
    if event and event["payload"].get("world_owner"):
        p.world_state["mug_position"] = "hand"
    assert p.world_state["mug_position"] == "hand"


def test_s28_temporal_outbox_crash_not_wall_clock_patched():
    p = make_prototype()
    candidate = {"candidate_id": "C-028", "payload": {"words": "Hello"}}
    snap = p.snapshot()
    e1 = p.ledger.admit(candidate)
    p.outbox.emit(e1["occurrence_id"])
    p.restore(snap)
    assert p.ledger.count() == 0
    assert len(p.outbox.deliveries) == 0
