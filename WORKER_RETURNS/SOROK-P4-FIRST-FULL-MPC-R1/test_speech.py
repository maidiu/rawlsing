from developmental_recursion.p2_owner import load_p2

from speech import admit_speech


def test_caller_speech_reaches_same_root_world_and_actor(tmp_path):
    fanin = load_p2().start(tmp_path / "world")
    try:
        session = fanin.session
        actor_ref = session.read_root()["actor_ids"][0]
        text = "  I can wait, but I need the bench after you.  "
        result = admit_speech(session, text=text, actor_ref=actor_ref)
        event = result["performed"]
        assert result["attempt"]["text"] == text
        assert result["admission"] == "ADMITTED"
        assert event["body"]["text"] == text
        assert event["body"]["attempt_hash"] == result["attempt"]["hash"]
        assert result["actor_access"]["event_id"] == event["event_id"]
        assert result["actor_access"]["actor_id"] != event["actor_id"]

        before = session.events()
        refused = admit_speech(session, text="   ", actor_ref=actor_ref)
        assert refused["admission"] == "EMPTY_SPEECH"
        assert refused["performed"] is refused["actor_access"] is None
        assert session.events() == before
    finally:
        fanin.close()

    reopened = load_p2().open(tmp_path / "world")
    try:
        assert reopened.session.event(event["event_id"]) == event
        assert reopened.session.read_root()["root_hash"] == result["attempt"]["root"]
        assert reopened.session.branch_id == result["attempt"]["branch"]
    finally:
        reopened.close()
