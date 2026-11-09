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
                                  actor_ref=case.initial.actor, request_edge=True)
            # A later access must recruit strictly antecedent records.
            session.produce_interval(case.base_owner.fanin.deps["make_domain"](
                mode="ACTUAL", start=session.clock(), end=session.clock() + 2))
            with pytest.raises(RecursionRefusal, match="P4_SPEECH_IDENTITY_MISMATCH"):
                read_response(case.owner, speech, scope)
            speech = admit_speech(session, text="Could you look at this edge?",
                                  actor_ref=case.initial.actor, request_edge=True)
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
                ledger = {"turns": [], "antecedent": {"identity": {"clock": session.clock()}}}
                public = json.dumps(surface(case.owner, ledger))
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


def test_non_edge_speech_recruits_received_p3_history_through_p4(tmp_path):
    from types import SimpleNamespace

    from run_p4 import act, new, open_owner

    request = "Could we go over that edge together?"
    departure = "I'll let you get on with your work."

    def transduce(*, event_id, event_hash, text):
        # Fixture transport supplies meaning only. P3 and P2 own the result.
        move, referent = {
            request: ("REQUEST", "CURRENT_EDGE"),
            departure: ("ASSERTION", None),
        }[text]
        return {"event_id": event_id, "event_hash": event_hash, "hypotheses": [
            {"move": move, "referent": referent, "span": [0, len(text)], "uncertain": False}
        ]}

    for index, (history, text, expected) in enumerate((
        ("recognized_plan", request, "joint_check"),
        ("recognized_plan", departure, None),
        ("imposed_plan", request, "private_check"),
    )):
        state = tmp_path / str(index)
        ledger_file = state / "p4_receipts.json"
        new(state, ledger_file, history)
        ledger = json.loads(ledger_file.read_text())
        owner = open_owner(state / "actual-p2")
        try:
            head = owner.store.head()
            args = SimpleNamespace(command="say", text=text, request_edge=False,
                                   request_id="non-edge")
            public = act(owner, ledger_file, ledger, args, transduce=transduce)
            turn = ledger["turns"][-1]
            uptake = turn["receipt"]["uptake"]
            assert turn["receipt"]["speech"]["actor_access"]
            assert uptake["mode"] == expected
            assert uptake["semantic_encounter"]["native_plan"] == "BLOCKED_NAMED_AUTHORITY_REQUIRED"
            assert owner.store.head() == head
            assert (public["observation"] is not None) is (expected is not None)
            if expected is None:
                assert uptake["status"] == "SEMANTIC_VALID_EMPTY"
                assert "recruitment" not in uptake
            else:
                assert any(row["mode"] == expected and row["activation"] == "ELIGIBLE"
                           for row in uptake["recruitment"]["entries"])
                event = turn["receipt"]["expression"]
                assert owner.base_owner.fanin.session.event(event["event_id"]) == event
                assert public["observation"]["event_id"] == event["event_id"]
            assert "semantic_encounter" not in public
        finally:
            owner.close()


def test_live_recruitment_loses_and_recovers_exact_p3_mediator(tmp_path):
    from run_p4 import new, open_owner

    ledger_file = tmp_path / "p4_receipts.json"
    new(tmp_path, ledger_file, "recognized_plan")
    scope = json.loads(ledger_file.read_text())["scope"]
    owner = open_owner(tmp_path / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        actor = owner.snapshot().document()["actor"]
        speech = admit_speech(session, text="Can we check the edge together?",
                              actor_ref=actor, request_edge=False)

        def transduce(*, event_id, event_hash, text):
            return {"event_id": event_id, "event_hash": event_hash, "hypotheses": [
                {"move": "REQUEST", "referent": "CURRENT_EDGE",
                 "span": [0, len(text)], "uncertain": False}
            ]}

        def read():
            return read_response(owner, speech, scope, transduce=transduce)

        def wrong_source(**kwargs):
            return {**transduce(**kwargs), "event_hash": "0" * 64}

        def unauthorized(**kwargs):
            return {**transduce(**kwargs), "registry_override": "attempted escalation"}

        def ambiguous(**kwargs):
            proposal = transduce(**kwargs)
            proposal["hypotheses"][0]["uncertain"] = True
            return proposal

        for provider, status in (
            (wrong_source, "SEMANTIC_PROPOSAL_REFUSED"),
            (unauthorized, "SEMANTIC_PROPOSAL_REFUSED"),
            (ambiguous, "SEMANTIC_AMBIGUITY_HELD"),
        ):
            uptake = read_response(owner, speech, scope, transduce=provider)
            assert uptake["status"] == status
            assert uptake["mode"] is None
            assert "recruitment" not in uptake

        before = read()
        assert before["mode"] == "joint_check"
        relevant = [entry for entry in before["recruitment"]["entries"]
                    if entry["activation"] == "ELIGIBLE" and entry["mode"] == "joint_check"]
        assert len(relevant) == 1
        event = speech["performed"]
        head = owner.store.head()
        # Test-only fault injection into the real query source. Rollback
        # restores the exact row, including provenance and chain metadata.
        database = owner.store._connection
        database.execute("SAVEPOINT mediator_cut")
        try:
            removed = database.execute("DELETE FROM p3_records WHERE record_id=? AND hash=?",
                                       (relevant[0]["record_id"], relevant[0]["record_hash"]))
            assert removed.rowcount == 1
            severed = read()
            assert severed["mode"] is None
            assert relevant[0]["record_hash"] not in severed["readset"]
            assert severed["semantic_encounter"] == before["semantic_encounter"]
        finally:
            database.execute("ROLLBACK TO mediator_cut")
            database.execute("RELEASE mediator_cut")
        assert read() == before
        assert session.event(event["event_id"]) == event
        assert owner.store.head() == head
        expression, public = express(session, read())
        assert public["event_id"] == expression["event_id"]
    finally:
        owner.close()
