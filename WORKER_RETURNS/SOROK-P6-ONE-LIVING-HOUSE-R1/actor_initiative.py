"""Bounded sourcefree Nadia initiative through the existing P6 world writer.

A model proposes an immediate action. The writer independently rechecks
the exact selected packet against the committed present world, actor-local
checkpoint and actor-specific route source before it may mutate anything.
Movement observations require explicit sourcefree origin/destination access.
This owns no V3 belief, memory or historical personhood authority.
"""
from copy import deepcopy
from dataclasses import dataclass, field

from developmental_recursion.contracts import RecursionRefusal, digest
from house import read_house

ACTION = "visit_adjacent_room"
GRADE = "SOURCEFREE_PROVISIONAL_ACTOR_WORLD_ACTION_NOT_NATIVE"
VISIBLE = "VISIBLE"
ROUTE_SOURCE = "SOURCEFREE_ACTOR_LOCAL_ADJACENCY"
_SELECTION_MARKER = object()


@dataclass(frozen=True)
class VisitSelection:
    """Exact model-selected visit, bound to the actor-local checkpoint."""

    selection_id: str
    actor_id: str
    packet: dict
    decision: dict
    actor_route: dict
    packet_hash: str
    decision_hash: str
    route_hash: str
    token: object = field(repr=False, compare=False)


def route_from_context(context, origin=None):
    """Return only an actor-local typed route, never objective room topology."""
    if type(context) is not dict or context.get("grade") != "SOURCEFREE_FIXTURE":
        return None
    routes = context.get("routes")
    if isinstance(routes, dict):
        if origin is None:
            return None
        route = routes.get(origin)
    else:
        route = context.get("route")
        if origin is not None and isinstance(route, dict) and route.get("origin") != origin:
            return None
    if (type(route) is not dict or set(route) != {"origin", "destination", "source"}
            or route.get("source") != ROUTE_SOURCE
            or not isinstance(route.get("origin"), str) or not route["origin"]
            or not isinstance(route.get("destination"), str) or not route["destination"]
            or route["origin"] == route["destination"]):
        return None
    return {
        "origin": route["origin"],
        "destination": route["destination"],
        "source": ROUTE_SOURCE,
    }


def destination_if_eligible(session, world, house, actor_id, local_context):
    """Qualify movement from checkpointed actor-local route, not model prose."""
    if (not session.scene_open()
            or local_context is None
            or local_context.get("grade") != "SOURCEFREE_FIXTURE"
            or actor_id != world.actor_state["A"].get("actor_id")
            or house.get("situated_conditions", {}).get("grade") != "SOURCEFREE_FIXTURE"):
        return None
    position = world.positions.get("A")
    route = route_from_context(local_context, position)
    if route is None:
        return None
    room = house["rooms"].get(position)
    if not isinstance(room, dict):
        return None
    target = route["destination"]
    if (route["origin"] != position or target != room.get("other")
            or target not in house["rooms"] or target == position):
        return None
    return target


def destination_affordance(session, world, house, actor_id, local_context):
    target = destination_if_eligible(session, world, house, actor_id, local_context)
    route = route_from_context(local_context, world.positions.get("A"))
    if target is None or route is None:
        return None
    return {
        "action": ACTION,
        "origin": route["origin"],
        "destination": target,
        "basis": ROUTE_SOURCE,
        "route_hash": digest(route),
    }


def _select_visit(session, packet, decision):
    """Bind the actual reconsider selection to one session-local writer scope.

    Only ``situated.reconsider`` calls this after the model decision is
    grounded. The world writer consumes this stored selection; it never
    accepts caller-supplied packet or decision values.
    """
    from situated import actor_context_for, decision_is_grounded

    world, house = read_house(session)
    actor = world.actor_state["A"].get("actor_id")
    checkpoint_context = actor_context_for(actor, house.get("situated_actor_context"))
    route = route_from_context(checkpoint_context, world.positions.get("A"))
    if (type(packet) is not dict or type(decision) is not dict
            or checkpoint_context is None or route is None
            or packet.get("actor") != actor
            or packet.get("actor_context") != checkpoint_context
            or packet.get("actor_route") != route
            or packet.get("actor_route_hash") != digest(route)
            or packet.get("room") != world.positions["A"]
            or packet.get("clock") != world.clock
            or packet.get("world_state_hash") != digest(world.snapshot())
            or packet.get("house_source") != house["source"]
            or packet.get("conditions_hash") != digest(house["situated_conditions"])
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
                decision, packet.get("cues", ()), packet.get("available_actions", ())
            )):
        raise RecursionRefusal("P6_INITIATIVE_SELECTION_NOT_ADMITTED")
    selection = VisitSelection(
        selection_id="P6_VISIT_" + digest({
            "packet": packet, "decision": decision, "route": route,
        })[:24],
        actor_id=actor,
        packet=deepcopy(packet),
        decision=deepcopy(decision),
        actor_route=deepcopy(route),
        packet_hash=digest(packet),
        decision_hash=digest(decision),
        route_hash=digest(route),
        token=_SELECTION_MARKER,
    )
    session._p6_miii_visit_selection = selection
    return selection


def visit_adjacent_room(session, expected_actor_id):
    """World-authorize the stored model-selected MOVE; no selection, no write."""
    from bp4.world import make_event
    from situated import actor_context_for, decision_is_grounded

    selection = getattr(session, "_p6_miii_visit_selection", None)
    if (not isinstance(selection, VisitSelection)
            or selection.token is not _SELECTION_MARKER):
        raise RecursionRefusal("P6_INITIATIVE_SELECTION_NOT_ADMITTED")
    packet, decision = selection.packet, selection.decision

    world, house = read_house(session)
    actor = world.actor_state["A"].get("actor_id")
    if actor != expected_actor_id or selection.actor_id != actor:
        raise RecursionRefusal("P6_INITIATIVE_ACTOR_IDENTITY_MISMATCH")

    checkpoint_context = actor_context_for(actor, house.get("situated_actor_context"))
    route = route_from_context(checkpoint_context, world.positions.get("A"))
    target = destination_if_eligible(session, world, house, actor, checkpoint_context)
    if target is None or route is None:
        raise RecursionRefusal("P6_INITIATIVE_CHECKPOINT_AUTHORITY_MISSING")

    if (selection.packet_hash != digest(packet)
            or selection.decision_hash != digest(decision)
            or selection.actor_route != route
            or selection.route_hash != digest(route)
            or type(packet) is not dict or type(decision) is not dict
            or packet.get("actor") != actor
            or packet.get("room") != world.positions["A"]
            or packet.get("clock") != world.clock
            or packet.get("world_state_hash") != digest(world.snapshot())
            or packet.get("house_source") != house["source"]
            or packet.get("conditions_hash") != digest(house["situated_conditions"])
            or packet.get("actor_context") != checkpoint_context
            or packet.get("actor_context_hash") != digest(house["situated_actor_context"])
            or packet.get("actor_route") != route
            or packet.get("actor_route_hash") != digest(route)
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

    # Consume the transient selection exactly once before any writer IO.
    # A failure after this boundary remains a P4 pending operation, not an
    # invitation to retry and produce duplicate world events.
    del session._p6_miii_visit_selection
    current = world.positions["A"]
    user = session.meta["user_actor"]
    observer_room = world.positions.get(user)
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
            "actor_route": deepcopy(route), "actor_route_hash": digest(route),
            "selection_id": selection.selection_id,
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
         "selection_id": selection.selection_id,
         "actor_route_hash": digest(route),
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
        "selection_id": selection.selection_id,
        "actor_route": deepcopy(route), "route_hash": digest(route),
        "source_packet_hash": digest(packet), "grade": GRADE,
    }
