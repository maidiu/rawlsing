import json
import sys
from pathlib import Path

import pytest

P3_TESTS = (Path(__file__).resolve().parents[1] /
            "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests")
sys.path.insert(0, str(P3_TESTS))

from p3_fixture_support import build_case
from developmental_recursion.contracts import RecursionRefusal
from p3 import test_rules
from response import express, read_response
from speech import admit_speech


def test_performed_speech_reads_real_prior_p3_formation(tmp_path, monkeypatch):
    outcomes = [("recognized_plan",), ("imposed_plan",), ()]
    receipts = []
    for index, history in enumerate(outcomes):
        case = build_case(tmp_path / str(index), history_outcomes=history,
                          include_compression=False, standpoints=False)
        try:
            # Use the actual P3 owner to form its records through P2.
            proposal = case.proposals[0]
            case.owner.realize("p4-formation", proposal, case.owner.snapshot())
            session = case.base_owner.fanin.session
            world_before = session.world().snapshot()
            scope = dict(case.plans[0], relation_ref=case.plans[0]["relation_refs"][0])
            speech = admit_speech(session, text="Could you look at this edge?",
                                  actor_ref=case.initial.actor)
            # A later access must recruit strictly antecedent records.
            session.produce_interval(case.base_owner.fanin.deps["make_domain"](
                mode="ACTUAL", start=session.clock(), end=session.clock() + 2))
            with pytest.raises(RecursionRefusal, match="P4_SPEECH_IDENTITY_MISMATCH"):
                read_response(case.owner, speech, scope)
            speech = admit_speech(session, text="Could you look at this edge?",
                                  actor_ref=case.initial.actor)
            uptake = read_response(case.owner, speech, scope)
            assert speech["performed"]["hash"] in uptake["readset"]

            if index == 0:
                from bp4.world import make_event
                from run_p4 import surface

                actor_private = "ACTOR_PRIVATE_P4_CONTROL_7f88"
                user_private = "USER_PRIVATE_P4_CONTROL_4b32"
                world = session.world()
                actor = uptake["actor_alias"]
                private_event = make_event(
                    clock=world.clock, kind="INSPECT", actor_id=actor,
                    location=world.positions[actor], summary=actor_private,
                    body={"text": actor_private}, sequence=len(world.events),
                )
                world.add_event(private_event)
                session._append_event(private_event, perceive=(actor,))
                session.product._append_episode(
                    session.branch_id, session.meta["user_actor"], "PRIVATE_NOTE",
                    world.clock, {"text": user_private},
                )
                session.product._checkpoint(session.branch_id, world.clock, world)
                assert session.event(private_event["event_id"])["summary"] == actor_private
                assert session.episodes(session.meta["user_actor"])[-1]["body"]["text"] == user_private
                assert read_response(case.owner, speech, scope) == uptake
                public = json.dumps(surface(case.owner, {"turns": []}))
                assert actor_private not in public and user_private not in public
                with monkeypatch.context() as cut:
                    cut.setattr(test_rules, "B1_PATH", tmp_path / "absent")
                    with pytest.raises(RecursionRefusal, match="P3_B1_SOURCE_SEVERED"):
                        read_response(case.owner, speech, scope)
                assert read_response(case.owner, speech, scope) == uptake

            event, observed = express(session, uptake)
            assert observed["event_id"] == event["event_id"]
            assert observed["actor_visible_id"] != speech["performed"]["actor_id"]
            receipts.append((world_before, uptake["mode"], observed["body_public"]["text"]))
        finally:
            case.cycle.engine.close()
            case.owner.close()

    assert receipts[0][0] == receipts[1][0] == receipts[2][0]
    assert [row[1] for row in receipts] == ["joint_check", "private_check", "inspect_alone"]
    assert len({row[2] for row in receipts}) == 3
