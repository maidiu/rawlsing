"""Sourcefree outward conduct in the existing two-room house."""

from developmental_recursion.contracts import RecursionRefusal, digest
from house import read_house
from actor_initiative import ROUTE_SOURCE

OPERATIONS = {"play": "PLAY_INSTRUMENT", "stop-playing": "STOP_INSTRUMENT",
              "approach": "APPROACH", "orient": "ORIENT"}
SOURCE = digest({"instrument": "mandolin", "room": "living room",
                 "placement": "workshop doorway to bench", "version": 1})


def establish_demo_conditions(session):
    """Checkpoint the declared conditions of the opt-in workshop demo."""
    world, house = read_house(session)
    house["situated_conditions"] = {
        "grade": "SOURCEFREE_FIXTURE", "hearing": "available", "sound_path": "audible",
        "bench_view": "facing_away", "footsteps": "audible",
        "actor_move_visibility": {"origin": "VISIBLE", "destination": "VISIBLE"},
    }
    house["situated_actor_context"] = {
        "grade": "SOURCEFREE_FIXTURE", "actor_id": world.actor_state["A"]["actor_id"],
        "priority": "Finish the current bench work while the material allows it.",
        "relationship": "A visitor in the workshop.",
        "routes": {
            room: {
                "origin": room,
                "destination": facts["other"],
                "source": ROUTE_SOURCE,
            }
            for room, facts in house["rooms"].items()
        },
    }
    session.product._checkpoint(session.branch_id, world.clock, world)


def perform(session, action):
    from bp4.world import make_event
    from s45_projection.projection import project_event

    world, house = read_house(session)
    user = session.meta["user_actor"]
    room = world.positions[user]
    operation = action["operation"]
    sound = operation in {"PLAY_INSTRUMENT", "STOP_INSTRUMENT"}
    playing = house.get("mandolin_playing", False)
    valid = session.scene_open() and (
        (room == "living room" and playing == (operation == "STOP_INSTRUMENT")) if sound
        else room == world.positions.get("A") == "workshop"
    )
    if not valid:
        return {}, {"admission": "UNAVAILABLE", "performed": False, "observation": None}

    body = {"root": house["root"], "branch": house["branch"], "source": SOURCE}
    if sound:
        playing = operation == "PLAY_INSTRUMENT"
        house["mandolin_playing"] = playing
        body.update(instrument="mandolin", sounding=playing)
        summary = "You begin playing the mandolin." if playing else "You stop playing the mandolin."
    else:
        if operation == "APPROACH":
            house["outward_near_actor"] = True
            summary = "You step from the doorway toward the bench."
        else:
            summary = "You turn toward the worker at the bench."
        body.update(target="A", near=house.get("outward_near_actor", False),
                    oriented_toward=operation == "ORIENT")

    event = make_event(clock=world.clock, kind=operation, actor_id=user, location=room,
                       summary=summary, body=body, sequence=len(world.events))
    world.add_event(event)
    session._append_event(event, perceive=(user,))
    parent = session.product._append_episode(
        session.branch_id, user, "P6_HOUSE_CONDUCT", world.clock,
        {"event_id": event["event_id"], "operation": operation},
    )
    session.product._checkpoint(session.branch_id, world.clock, world)
    committed, resource = read_house(session)
    if (session.event(event["event_id"]) != event or event["clock"] != committed.clock
            or not any(row["episode_id"] == parent["episode_id"] and row["body"] ==
                       {"event_id": event["event_id"], "operation": operation}
                       for row in session.episodes(user))):
        raise RecursionRefusal("P6_OUTWARD_CONDUCT_SOURCE_MISMATCH")
    cue = sensory_candidate(event, committed, resource)
    return {"performed": event, "outward_cue": cue}, {
        "admission": "ADMITTED", "performed": True, "observation": project_event(event),
    }


def sensory_candidate(event, world, house):
    """Only checkpointed sourcefree conditions establish modality access."""
    facts = house.get("situated_conditions", {})
    if facts.get("grade") != "SOURCEFREE_FIXTURE":
        return None
    kind = event["kind"]
    body = event["body"]
    same_room = world.positions.get("A") == event["location"]
    hearing = facts.get("hearing") == "available"
    if kind in {"PLAY_INSTRUMENT", "STOP_INSTRUMENT"}:
        acoustic_path = facts.get("sound_path")
        if not hearing or not (same_room or (world.positions.get("A") == "workshop"
                                             and acoustic_path == "audible")):
            return None
        channels = ["AUDITORY"]
        detail = {"instrument": body["instrument"], "sounding": body["sounding"]}
    else:
        if not same_room:
            return None
        view = facts.get("bench_view")
        channels = ["VISUAL"] if view == "facing_player" else []
        if kind == "APPROACH" and hearing and facts.get("footsteps") == "audible":
            channels.append("AUDITORY")
        if not channels:
            return None
        detail = {"near": body["near"]}
        if "VISUAL" in channels:
            detail["oriented_toward_actor"] = body["oriented_toward"]
    return {"event_id": event["event_id"], "event_hash": event["hash"], "clock": event["clock"],
            "kind": kind, "channels": channels, "detail": detail,
            "condition_source": digest(facts), "grade": "SOURCEFREE_FIXTURE"}
