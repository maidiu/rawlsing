"""Sourcefree caller-speech admission on the received P2 encounter root."""

from developmental_recursion.contracts import RecursionRefusal, digest


def developing_actor(session, actor_ref):
    """Resolve the world's actor alias from a performed P2 action binding."""
    for row in reversed(session.read_events()):
        if row["actor_id"] != actor_ref or not row.get("performed"):
            continue
        action = session.event(row["action_event_id"])
        if (action and action["hash"] == row["action_event_hash"]
                and action["actor_id"] != session.meta["user_actor"]):
            return action["actor_id"]
    raise RecursionRefusal("P4_ACTOR_ACTION_BINDING_UNAVAILABLE")


def admit_speech(session, *, text, actor_ref):
    """Record the attempt, then commit and perceive speech only if admitted.

    The interaction owner calls this inside its serialized operation. This
    function returns internal receipts for the actor uptake and surface readers.
    """
    # P2's product bootstrap resolves the canonical world implementation.
    from bp4.world import make_event

    if not isinstance(text, str):
        raise RecursionRefusal("P4_SAY_REQUIRES_TEXT")
    user = session.meta["user_actor"]
    world = session.world()
    actor = developing_actor(session, actor_ref)
    attempt = {
        "operation": "SAY",
        "text": text,
        "performer": user,
        "root": session.read_root()["root_hash"],
        "branch": session.branch_id,
        "clock": world.clock,
        "sequence": session._action_seq(),
    }
    attempt["hash"] = digest(attempt)
    refusal = None
    if not text.strip():
        refusal = "EMPTY_SPEECH"
    elif not session.scene_open() or user not in world.positions:
        refusal = "SCENE_CLOSED"

    result = {"attempt": attempt, "admission": refusal or "ADMITTED",
              "performed": None, "actor_access": None}
    if refusal is None:
        event = make_event(
            clock=world.clock, kind="SPEECH", actor_id=user,
            location=world.positions[user], summary=f"{user} says: {text}",
            body={"text": text, "observable": True, "attempt_hash": attempt["hash"]},
            sequence=len(world.events),
        )
        world.add_event(event)
        session._append_event(event, perceive=(user,))
        session._perceive_if_present(event, actor)
        result["performed"] = session.event(event["event_id"])
        result["actor_access"] = next((
            row for row in session.product.store.perceptions(session.branch_id, actor)
            if row["event_id"] == event["event_id"] and row["clock"] == event["clock"]
        ), None)
    session.product._append_episode(
        session.branch_id, user, "P4_SAY", world.clock,
        {"attempt": attempt, "admission": result["admission"],
         "event_id": (result["performed"] or {}).get("event_id")},
    )
    session.product._checkpoint(session.branch_id, world.clock, world)
    return result
