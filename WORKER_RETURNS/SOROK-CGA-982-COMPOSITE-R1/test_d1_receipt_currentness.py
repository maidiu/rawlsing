"""CG-A G5-D1 repair regression: a stale authentic receipt is not current authority."""
from argparse import Namespace
import json
from pathlib import Path
import sys

P6 = Path(__file__).resolve().parents[2] / "WORKER_RETURNS" / "SOROK-P6-ONE-LIVING-HOUSE-R1"
if str(P6) not in sys.path:
    sys.path.insert(0, str(P6))

import run_p6
from house import read_house
from situated import current_p3_actor_access


def _run(state, command, request_id):
    run_p6.experience(state, Namespace(command=command, request_id=request_id,
                                       duration=4 if command == "wait" else None,
                                       situated_house=True))


def _receipt(state):
    return json.loads((state / "p4_receipts.json").read_text())["turns"][-1]["receipt"]


def test_stale_authentic_receipt_is_not_current_authorization(tmp_path):
    state = tmp_path / "receipt-currentness"
    _run(state, "new", None)
    _run(state, "approach", "old")
    old = _receipt(state)
    old_event = old["performed"]
    _run(state, "wait", "later")
    owner = run_p6.open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        world, house = read_house(session)
        packet = {"cues": [old["outward_cue"]],
                  "recent_self_actions": [], "recent_speech": []}
        broadened = {"start": old_event["clock"] - 1, "end": world.clock}
        assert world.clock > old_event["clock"]
        assert current_p3_actor_access(
            session, broadened, world, house, packet,
            source_receipt=old) is False
        assert current_p3_actor_access(
            session, old["interval"], world, house, packet,
            source_receipt=old) is False
    finally:
        owner.close()

    _run(state, "approach", "current")
    current = _receipt(state)
    owner = run_p6.open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        world, house = read_house(session)
        packet = {"cues": [current["outward_cue"]],
                  "recent_self_actions": [], "recent_speech": []}
        assert current_p3_actor_access(
            session, current["interval"], world, house, packet,
            source_receipt=current) is True
    finally:
        owner.close()
