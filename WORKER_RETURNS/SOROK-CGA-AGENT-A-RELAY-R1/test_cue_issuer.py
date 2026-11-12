"""Agent A relay: current event != source-issued current *sensory cue*.

Reproduces a forged non-fixture modality for an actual committed and
actor-perceived world event. It is not sufficient that the event exists and the
actor perceived it; the purported cue must have an admissible evidence issuer.
"""
from argparse import Namespace
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
P6 = ROOT / "WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1"
if str(P6) not in sys.path:
    sys.path.insert(0, str(P6))

import run_p6
from situated import current_p3_actor_access
from house import read_house


def test_world_real_perceived_event_cannot_become_forged_sensory_cue(tmp_path):
    state = tmp_path / "actual-world"
    run_p6.experience(state, Namespace(command="new", request_id=None,
                                       situated_house=True))
    owner = run_p6.open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        world, house = read_house(session)
        perceived = session.product.store.perceptions(session.branch_id, "A")
        rows = [(session.event(r["event_id"]), r) for r in perceived]
        rows = [(event, row) for event, row in rows
                if event and type(event.get("clock")) is int
                and event["clock"] <= world.clock]
        assert rows, "Actual P2/P3/P4 world should have actor perception capital"
        event, perception = rows[-1]
        assert perception["clock"] == event["clock"]
        interval = {"start": event["clock"], "end": world.clock}
        # This is *not* a true P6 encounter/movement or instrument cue.
        # B's fallback would accept it by event-id membership and modality.
        forged = {
            "event_id": event["event_id"],
            "clock": event["clock"],
            "event_hash": event["hash"],
            "modality": "AUDITORY",
            "basis": "CLAIMED_BUT_NEVER_ISSUED",
        }
        packet = {"cues": [forged], "recent_speech": [],
                  "recent_self_actions": []}
        assert current_p3_actor_access(session, interval, world, house, packet) is False
        # Missing even the event hash must not be an alternate acceptance route.
        stripped = dict(forged)
        del stripped["event_hash"]
        assert current_p3_actor_access(
            session, interval, world, house,
            {**packet, "cues": [stripped]}) is False
    finally:
        owner.close()


def test_actual_current_outward_receipt_grants_only_exact_one_operation(tmp_path):
    """Same actual world: issuer + performed event + conduct parent required."""
    import json
    from copy import deepcopy

    state = tmp_path / "performed"
    run_p6.experience(state, Namespace(command="new", request_id=None,
                                       situated_house=True))
    run_p6.experience(state, Namespace(command="approach",
                                       request_id="current-approach"))
    ledger = json.loads((state / "p4_receipts.json").read_text())
    receipt = ledger["turns"][-1]["receipt"]
    owner = run_p6.open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        world, house = read_house(session)
        cue = receipt["outward_cue"]
        assert cue["grade"] == "SOURCEFREE_FIXTURE"
        assert receipt["performed"]["event_id"] == cue["event_id"]
        packet = {"cues": [cue], "recent_self_actions": [], "recent_speech": []}
        interval = receipt["interval"]
        before = owner.store.head()
        assert current_p3_actor_access(
            session, interval, world, house, packet, source_receipt=receipt) is True
        assert current_p3_actor_access(
            session, interval, world, house, packet) is False
        forged = deepcopy(receipt)
        forged["performed"]["event_id"] = "counterfeit-performed-event"
        assert current_p3_actor_access(
            session, interval, world, house, packet, source_receipt=forged) is False
        stripped = deepcopy(receipt)
        stripped["outward_cue"] = None
        assert current_p3_actor_access(
            session, interval, world, house, packet, source_receipt=stripped) is False
        assert owner.store.head() == before
    finally:
        owner.close()


def test_first_consumer_binds_current_world_readset_separately_from_p3(tmp_path):
    """No unsupported proof leap from B1 history to present-world observation."""
    state = tmp_path / "actual-first-consumer"
    packets = []

    def interpret(packet):
        packets.append(packet)
        return {"attention": "uncertain", "interpretation": "Sourcefree cue available.",
                "action": "continue", "cue_event_id": None, "channel": None}

    run_p6.experience(state, Namespace(command="new", request_id=None,
                                       situated_house=True))
    run_p6.experience(state, Namespace(command="approach", request_id="real",
                                       target=None), interpret=interpret,
                      sourcefree_p3_bridge=True)
    assert len(packets) == 1
    p3 = packets[0]["sourcefree_p3"]
    assert p3["status"] == "PRIOR_P3_CANDIDATES"
    assert len(p3["records"]) == 1
    assert len(p3["world_readset"]) == len(p3["actor_access_evidence"]) == 1
    proof = p3["actor_access_evidence"][0]
    assert proof["basis"] == "P6_OUTWARD_CURRENT_OPERATION_DERIVED"
    assert proof["event_hash"] == p3["world_readset"][0]
    assert proof["event_hash"] not in p3["readset"]
    assert p3["stimulus_to_mediator_relevance"] == "UNISSUED_NATIVE_RULE"

    import json
    turns = json.loads((state / "p4_receipts.json").read_text())["turns"]
    committed = turns[-1]["receipt"]["outward_cue"]
    assert committed["event_hash"] == proof["event_hash"]
