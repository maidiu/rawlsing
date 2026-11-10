"""Bounded sourcefree Nadia initiative through the existing P6 world writer.

A model selects one allowed immediate action.  This module alone performs the
actor move and records the world event.  It owns no V3 belief, intention,
memory or historical personality authority.
"""
from developmental_recursion.contracts import RecursionRefusal
from house import read_house


ACTION = "visit_adjacent_room"
GRADE = "SOURCEFREE_PROVISIONAL_ACTOR_WORLD_ACTION_NOT_NATIVE"


def destination_if_eligible(session, world, house, actor_id, local_context):
    """Qualify the *option* from real scene facts, not from a model assertion."""
    if (not session.scene_open()
            or local_context is None
            or local_context.get("grade") != "SOURCEFREE_FIXTURE"
            or actor_id != world.actor_state["A"].get("actor_id")
            or house.get("situated_conditions", {}).get("grade") != "SOURCEFREE_FIXTURE"):
        return None
    position = world.positions.get("A")
    room = house["rooms"].get(position)
    if not isinstance(room, dict):
        return None
    target = room.get("other")
    if target not in house["rooms"] or target == position:
        return None
    return target


def visit_adjacent_room(session, expected_actor_id):
    """Admit an actor-originated MOVE, or explicitly refuse with no world write."""
    from bp4.world import make_event

    world, house = read_house(session)
    actor = world.actor_state["A"].get("actor_id")
    if actor != expected_actor_id:
        raise RecursionRefusal("P6_INITIATIVE_ACTOR_IDENTITY_MISMATCH")
    current = world.positions.get("A")
    room = house["rooms"].get(current)
    target = room.get("other") if isinstance(room, dict) else None
    if (not session.scene_open()
            or house.get("situated_conditions", {}).get("grade") != "SOURCEFREE_FIXTURE"
            or target not in house["rooms"] or target == current):
        return {"admitted": False, "status": "UNAVAILABLE", "grade": GRADE}

    # Only the world writer creates the objective consequence. No model text
    # or sourcefree character fixture is treated as a historical fact.
    event = make_event(
        clock=world.clock,
        kind="MOVE",
        actor_id="A",
        location=target,
        summary="The worker walks into the adjoining room.",
        body={
            "origin": current, "target": target,
            "root": house["root"], "branch": house["branch"],
            "house_source": house["source"],
            "actor_action": ACTION, "grade": GRADE,
        },
        sequence=len(world.events),
    )
    world.positions["A"] = target
    world.add_event(event)
    session._append_event(event, perceive=("A",))
    episode = session.product._append_episode(
        session.branch_id, "A", "P6_SITUATED_ACTOR_CONDUCT", world.clock,
        {"event_id": event["event_id"], "operation": ACTION, "world_hash": event["hash"]},
    )
    session.product._checkpoint(session.branch_id, world.clock, world)
    # User access is based on actual co-presence after movement.  The actor
    # does not gain any extra perception of the user's intentions.
    session._perceive_if_present(event, session.meta["user_actor"])
    return {
        "admitted": True,
        "status": "OK",
        "event_id": event["event_id"],
        "event_hash": event["hash"],
        "actor_id": "A",
        "origin": current,
        "destination": target,
        "parent_episode": episode["episode_id"],
        "grade": GRADE,
    }
