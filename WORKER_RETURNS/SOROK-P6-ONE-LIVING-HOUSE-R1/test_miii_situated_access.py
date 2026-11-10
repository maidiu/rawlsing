"""MIII Grade A: actual P6 movement reaches existing S45 actor-access receipts.

These are sourcefree boundary tests, not tests of vision, hearing, actual conscious
noticing, actor intent-attribution, CAN-008 psychology or native V2 expression.
"""
from argparse import Namespace
import json

from run_p6 import experience, open_owner


def _run(state, command, **kwargs):
    return experience(state, Namespace(command=command, request_id=None, **kwargs))


def _evidence(state):
    owner = open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        ledger = json.loads((state / "p4_receipts.json").read_text())
        by_actor = {
            actor: list(session.product.store.perceptions(session.branch_id, actor))
            for actor in ("A", "B")
        }
        return ledger, dict(session.world().positions), list(session.events()), by_actor
    finally:
        owner.close()


def test_real_go_uses_actor_access_owner_and_internal_first_reader(tmp_path):
    _run(tmp_path, "new")
    _run(tmp_path, "go", target="living room")
    _run(tmp_path, "go", target="workshop")
    ledger, positions, events, by_actor = _evidence(tmp_path)
    turns = [row for row in ledger["turns"] if row["action"]["operation"] == "GO"]
    assert len(turns) == 2
    assert positions["U"] == "workshop"
    assert len({row["receipt"]["performed"]["event_id"] for row in turns}) == 2

    for turn in turns:
        performed = turn["receipt"]["performed"]
        assert performed["kind"] == "MOVE"
        assert turn["receipt"]["interval"] is not None
        assert performed in events
        assert "expression" not in turn["receipt"]  # movement is not a forced response
        for actor in ("A", "B"):
            receipt = turn["receipt"]["actor_access"][actor]
            matches = [
                row for row in by_actor[actor]
                if row["event_id"] == performed["event_id"]
                and row["clock"] == performed["clock"]
            ]
            assert receipt["source_event_id"] == performed["event_id"]
            assert receipt["source_event_hash"] == performed["hash"]
            assert receipt["source_clock"] == performed["clock"]
            assert receipt["recorded_access"] is bool(matches)
            assert receipt["access_grade"] == "S45_SOURCEFREE_COPRESENT_ONLY"
            assert receipt["actor_uptake"] == "NOT_EVALUATED"
            assert receipt["interpretation"] == "NOT_EVALUATED"

    # The historical actor's world-eligible encounter is proved without a
    # fabricated sensory modality or psychological response.
    assert any(
        turn["receipt"]["actor_access"]["A"]["recorded_access"]
        for turn in turns
    )


def test_private_user_gaze_neither_commits_actor_event_nor_changes_actor_receipts(tmp_path):
    _run(tmp_path, "new")
    _run(tmp_path, "go", target="living room")
    before_ledger, before_positions, before_events, before_access = _evidence(tmp_path)

    gaze_file = tmp_path / "p6_gaze.json"
    gaze = json.loads(gaze_file.read_text())
    gaze["history"] = [{"target": "photo", "turn": 1, "shown": False,
                        "available": ["photo", "sandals", "coaster"]}]
    gaze_file.write_text(json.dumps(gaze))
    _run(tmp_path, "view")

    after_ledger, after_positions, after_events, after_access = _evidence(tmp_path)
    assert after_ledger["turns"] == before_ledger["turns"]
    assert after_positions == before_positions
    assert after_events == before_events
    assert after_access == before_access


def test_unavailable_conduct_and_duplicate_request_do_not_create_extra_access(tmp_path):
    _run(tmp_path, "new")
    before = _evidence(tmp_path)
    assert _run(tmp_path, "go", target="workshop")["admission"] == "UNAVAILABLE"
    after = _evidence(tmp_path)
    assert after[2] == before[2]
    assert after[3] == before[3]

    first = experience(tmp_path, Namespace(command="go", target="living room",
                                          request_id="miii-once"))
    after_first = _evidence(tmp_path)
    replay = experience(tmp_path, Namespace(command="go", target="living room",
                                           request_id="miii-once"))
    after_replay = _evidence(tmp_path)
    assert replay["admission"] == first["admission"] == "ADMITTED"
    assert after_replay[0]["turns"] == after_first[0]["turns"]
    assert after_replay[2] == after_first[2]
    assert after_replay[3] == after_first[3]
