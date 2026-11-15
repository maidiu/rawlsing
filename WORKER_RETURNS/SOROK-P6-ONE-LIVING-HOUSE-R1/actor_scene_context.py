"""Evidence-filtered present-scene actor continuity, never biographical memory.

A world event belongs in the actor's near-term context only when the
world itself holds that exact event AND the actor's own perception stream
records it as an act she performed.  This does not promote an action to a
durable psychological/ADP016 memory or a historical trait.
"""

OWN_ACTS = frozenset({"MOVE", "REPAIR"})
LIMIT = 6


def recent_self_actions(session, *, actor_slot="A", limit=LIMIT):
    if actor_slot != "A" or type(limit) is not int or not 1 <= limit <= LIMIT:
        raise ValueError("P6_SCENE_SELF_ACTION_SCOPE_INVALID")
    world = session.world()
    if actor_slot not in world.actor_state:
        raise ValueError("P6_SCENE_ACTOR_NOT_IN_WORLD")
    actor_id = world.actor_state[actor_slot].get("actor_id")
    root = session.read_root()
    if not actor_id or actor_id not in root["actor_ids"]:
        raise ValueError("P6_SCENE_ACTOR_ROOT_MISMATCH")

    # Read the actor's canonical perception/access stream, not P4 receipts
    # or any user-visible narrated transcript. Only self-performed actions.
    rows = session.product.store.perceptions(session.branch_id, actor_slot)
    result, seen = [], set()
    for perceived in reversed(rows):
        event_id = perceived.get("event_id")
        if not isinstance(event_id, str) or event_id in seen:
            continue
        event = session.event(event_id)
        if (not isinstance(event, dict)
                or event.get("kind") not in OWN_ACTS
                or event.get("actor_id") != actor_slot
                or type(event.get("clock")) is not int
                or event["clock"] != perceived.get("clock")
                or event["clock"] > world.clock
                or not isinstance(event.get("hash"), str)
                or not event.get("location")):
            continue
        seen.add(event_id)
        result.append({
            "event_id": event_id,
            "event_hash": event["hash"],
            "clock": event["clock"],
            "kind": event["kind"],
            "location": event["location"],
            "source": "COMMITTED_SELF_ACTION_WITH_ACTOR_PERCEPTION",
        })
        if len(result) >= limit:
            break
    return list(reversed(result))
