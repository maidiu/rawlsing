"""Independent G5 hostile probe: an old authentic receipt is not current authority."""
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


def test_old_authentic_receipt_cannot_be_replayed_as_current_operation(tmp_path):
    state = tmp_path / "stale-receipt"
    run_p6.experience(state, Namespace(command="new", request_id=None,
                                       situated_house=True))
    run_p6.experience(state, Namespace(command="approach", request_id="old"))
    old = json.loads((state / "p4_receipts.json").read_text())["turns"][-1]["receipt"]
    old_event = old["performed"]
    run_p6.experience(state, Namespace(command="wait", duration=4,
                                       request_id="later"))
    owner = run_p6.open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        world, house = read_house(session)
        packet = {"cues": [old["outward_cue"]],
                  "recent_self_actions": [], "recent_speech": []}
        interval = {"start": old_event["clock"] - 1, "end": world.clock}
        assert world.clock > old_event["clock"]
        assert current_p3_actor_access(
            session, interval, world, house, packet,
            source_receipt=old) is False
    finally:
        owner.close()
