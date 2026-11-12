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
