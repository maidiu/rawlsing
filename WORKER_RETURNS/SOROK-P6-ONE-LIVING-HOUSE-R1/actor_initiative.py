"""Bounded sourcefree Nadia initiative through the existing P6 world writer.

A model proposes an immediate action. The writer independently rechecks
the exact selection packet against the committed present world, actor-local
checkpoint and destination affordance before it may mutate anything.
Movement observations require explicit sourcefree origin/destination access.
This owns no V3 belief, memory or historical personhood authority.
"""
from developmental_recursion.contracts import RecursionRefusal, digest
from house import read_house

ACTION = "visit_adjacent_room"
GRADE = "SOURCEFREE_PROVISIONAL_ACTOR_WORLD_ACTION_NOT_NATIVE"
VISIBLE = "VISIBLE"


def destination_if_eligible(session, world, house, actor_id, local_context):
    """Qualify movement from checkpointed present scene, not model prose."""
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


def destination_affordance(session, world, house, actor_id, local_context):
    target = destination_if_eligible(session, world, house, actor_id, local_context)
    if target is None:
        return None
    # The actor knows a neighboring room exists, not whether a private
    # player is there or what unseen activity is happening inside.
    return {
        "action": ACTION,
        "origin": world.positions["A"],
        "destination": target,
        "basis": "SOURCEFREE_CHECKPOINTED_ADJACENCY",
    }


def visit_adjacent_room(session, expected_actor_id, *, packet=None, decision=None):
    """World-authorize one model-selected MOVE; no valid packet, no world write.

    A correct actor ID alone is not an admission. The packet must be this
    exact actor's source-bound current-scene projection, including a fresh
    world hash; the selected decision must satisfy the same grounding
    constraints as the selector. This is an internal sourcefree interface,
    not a cryptographic authorization for externally supplied code.
    """
    from bp4.world import make_event
    from situated import actor_context_for, decision_is_grounded

    world, house = read_house(session)
    actor = world.actor_state["A"].get("actor_id")
    if actor != expected_actor_id:
        raise RecursionRefusal("P6_INITIATIVE_ACTOR_IDENTITY_MISMATCH")

    checkpoint_context = actor_context_for(actor, house.get("situated_actor_context"))
    target = destination_if_eligible(session, world, house, actor, checkpoint_context)
    if target is None:
        raise RecursionRefusal("P6_INITIATIVE_CHECKPOINT_AUTHORITY_MISSING")

    if (type(packet) is not dict or type(decision) is not dict
            or packet.get("actor") != actor
            or packet.get("room") != world.positions["A"]
            or packet.get("clock") != world.clock
            or packet.get("world_state_hash") != digest(world.snapshot())
            or packet.get("house_source") != house["source"]
            or packet.get("conditions_hash") != digest(house["situated_conditions"])
            or packet.get("actor_context") != checkpoint_context
            or packet.get("actor_context_hash") != digest(house["situated_actor_context"])
            or packet.get("root_hash") != session.read_root()["root_hash"]
            or packet.get("branch_id") != session.branch_id
            or ACTION not in packet.get("available_actions", ())
            or not isinstance(packet.get("action_affordances"), list)
            or destination_affordance(
                session, world, house, actor, checkpoint_context
            ) not in packet["action_affordances"]
            or decision.get("action") != ACTION
            or not decision_is_grounded(
                decision, packet.get("cues", ()), packet["available_actions"]
            )):
        raise RecursionRefusal("P6_INITIATIVE_ADMISSION_STALE_OR_INVALID")

    current = world.positions["A"]
    user = session.meta["user_actor"]
    observer_room = world.positions.get(user)
    # Both lanes are separately declared in the checkpointed sourcefree
    # conditions. Neither co-presence alone nor the final position grants
    # an origin-side or destination-side observation.
    lane = (
        "origin" if observer_room == current else
        "destination" if observer_room == target else None
    )
    access = house["situated_conditions"].get("actor_move_visibility")
    visible = (
        lane is not None and isinstance(access, dict)
        and access.get(lane) == VISIBLE
    )

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
    if visible:
        session.product._perceive(
            session.branch_id, user, event,
            channel=f"p6_sourcefree_actor_move_{lane}",
        )
    episode = session.product._append_episode(
        session.branch_id, "A", "P6_SITUATED_ACTOR_CONDUCT", world.clock,
        {"event_id": event["event_id"], "operation": ACTION,
         "world_hash": event["hash"],
         "actor_decision_hash": digest(decision),
         "source_packet_hash": digest(packet)},
    )
    session.product._checkpoint(session.branch_id, world.clock, world)
    return {
        "admitted": True, "status": "OK",
        "event_id": event["event_id"], "event_hash": event["hash"],
        "actor_id": "A", "origin": current, "destination": target,
        "parent_episode": episode["episode_id"],
        "user_observation": lane if visible else "HELD_UNQUALIFIED",
        "source_packet_hash": digest(packet), "grade": GRADE,
    }
