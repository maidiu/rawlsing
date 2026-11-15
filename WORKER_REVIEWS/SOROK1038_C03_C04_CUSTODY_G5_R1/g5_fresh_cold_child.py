"""Fresh-process cold reopen witness for SOROK #1030 C03/C04 custody."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
J1 = ROOT / "WORKER_RETURNS" / "SOROK-E01-J1-995-R1"
P3_TESTS = ROOT / "WORKER_RETURNS" / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1" / "tests"
for path in (J1, P3_TESTS):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from test_j1_three_head_join import PARENT_ID  # noqa: E402
from p3_fixture_support import reopen_owner  # noqa: E402
from developmental_recursion.parent_activity import (  # noqa: E402
    PARENT_PURCHASE_KIND, read_parent_history,
)
from developmental_recursion.parent_speech import (  # noqa: E402
    PARENT_UTTERANCE_KIND, read_child_uptake, read_parent_utterance,
)
from run_p6 import child_speech_experience  # noqa: E402
import j1_join  # noqa: E402

RENT_KIND = "P2_HOUSEHOLD_RENT"


def snapshot(session, store):
    return {
        "clock": session.clock(),
        "episodes": len(store.episodes(session.branch_id)),
        "world_events": len(store.world_events(session.branch_id)),
        "perceptions": len(store.perceptions(session.branch_id)),
    }


def count_kind(session, kind):
    return sum(1 for row in session.product.store.episodes(session.branch_id)
               if row.get("kind") == kind)


def main(path: str) -> None:
    data = json.loads(Path(path).read_text())
    case = SimpleNamespace(
        source=data["case"]["source"],
        history=data["case"]["history"],
        plans=data["case"]["plans"],
        catalog=data["case"]["catalog"],
        compression_specs=data["case"]["compression_specs"],
        standpoints=data["case"]["standpoints"],
        state_root=Path(data["case"]["state_root"]),
    )
    base, owner = reopen_owner(case)
    try:
        session = base.fanin.session
        store = session.product.store
        before = snapshot(session, store)
        head_before = owner.store.head()
        eid = data["speech_event_id"]
        focal = data["focal"]
        receipt = data["utterance_receipt"]
        uptake = read_child_uptake(session, focal, eid)
        p6 = child_speech_experience(session, event_id=eid)
        joined = j1_join.compose_j1(
            owner, session, child_id=focal, speech_event_id=eid,
            utterance_receipt=receipt, plan=data["plan"])
        parent = read_parent_utterance(
            session, PARENT_ID, "j1-speech", as_actor=PARENT_ID)
        history = read_parent_history(session, PARENT_ID, as_actor=PARENT_ID)
        event = session.event(eid)
        after = snapshot(session, store)
        head_after = owner.store.head()
        child_blob = json.dumps({
            "uptake": uptake,
            "p6": p6,
            "child_experience": joined["child_experience"],
            "immediate_uptake": joined["immediate_uptake"],
        })
        result = {
            "process": "FRESH_INTERPRETER",
            "event_hash_exact": event["hash"] == data["event_hash"],
            "event_text_exact": event["body"]["text"] == data["text"],
            "uptake_status": uptake["status"],
            "p6_status": p6["status"],
            "joined_status": joined["status"],
            "d03_status": joined["immediate_uptake"]["status"],
            "d03_modes": joined["immediate_uptake"]["immediate_response"][
                "eligible_modes"],
            "subsequent_performed": joined["subsequent_event"]["performed"],
            "durable_formation": joined["durable_formation"],
            "language_generation_owner": p6["response_input"][
                "language_generation_owner"],
            "text_source": p6["response_input"]["text_source"],
            "speech_episode_count": count_kind(session, PARENT_UTTERANCE_KIND),
            "purchase_episode_count": count_kind(session, PARENT_PURCHASE_KIND),
            "rent_episode_count": count_kind(session, RENT_KIND),
            "history_purchase_count": history["purchase_episode_count"],
            "hidden_absent_from_child": data["hidden"] not in child_blob,
            "hidden_hash_absent_from_child": "hidden_reason_hash" not in child_blob,
            "parent_read_status": parent["status"],
            "parent_hidden_exact": parent["hidden_reason"] == {
                "reason": data["hidden"]},
            "snapshot_before": before,
            "snapshot_after": after,
            "snapshot_unchanged": before == after,
            "p3_head_unchanged": head_before == head_after,
        }
        print(json.dumps(result, sort_keys=True))
    finally:
        owner.close()


if __name__ == "__main__":
    main(sys.argv[1])
