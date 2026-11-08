"""Sourcefree room and object facts held in the received BP4 world checkpoint."""

from developmental_recursion.contracts import RecursionRefusal, digest

SLOT = "p6_house"
ROOMS = {
    "workshop": {"other": "living room", "line": "A doorway leads from the workbench into the living room."},
    "living room": {"other": "workshop", "line": "The workbench is through the doorway. A low shelf runs along the wall."},
}
OBJECTS = {
    "bench": {"room": "workshop", "glance": "The bench stands beside the doorway.",
              "close": "Shallow cuts cross the bench top."},
    "mug": {"room": "workshop", "glance": "A mug stands beside the bench.",
            "close": "There is a chip in the rim."},
    "sandals": {"room": "living room", "glance": "A pair of brown sandals lies beneath the shelf.",
                "close": "Blue thread crosses the left strap. The cork at the heel is dark.",
                "specialist_identity": "the repaired blue-thread sandals",
                "marking": "blue-thread-left-strap",
                "evidence": "Blue thread crosses the left strap."},
    "photo": {"room": "living room", "glance": "A photograph leans against the wall on the shelf.",
              "close": "In the photograph, brown sandals lie on a step. Blue thread crosses the left strap."},
    "coaster": {"room": "living room", "glance": "A round cork coaster lies on the shelf.",
                "close": "A shallow ring marks the cork."},
}
# Offsets refer to the established encounter clock. The photograph captures
# the repaired strap, so its exposure has to follow the repair.
HISTORY = (
    {"id": "bench-installation", "object": "bench", "offset": -14, "depends_on": []},
    {"id": "strap-repair", "object": "sandals", "offset": -9, "depends_on": []},
    {"id": "photo-exposure", "object": "photo", "offset": -4, "depends_on": ["strap-repair"],
     "depicts": "sandals"},
)
SOURCE = digest({"rooms": ROOMS, "objects": OBJECTS, "history": HISTORY})


def facts(epoch):
    result = {}
    for row in HISTORY:
        clock = epoch + row["offset"]
        if (row["id"] in result or row["object"] not in OBJECTS
                or clock >= epoch or any(parent not in result or result[parent]["clock"] >= clock
                                        for parent in row["depends_on"])):
            raise RecursionRefusal("P6_INVALID_OBJECT_CHRONOLOGY")
        result[row["id"]] = {**row, "clock": clock}
    return result


def recognize(target, evidence_text, objects=None):
    """Return a stable identity only from the exact committed object marking."""
    item = (objects if objects is not None else OBJECTS).get(target)
    if (not item or not item.get("specialist_identity")
            or not item.get("marking") or item.get("evidence") not in str(evidence_text)):
        return None
    return {
        "object_id": target,
        "identity": item["specialist_identity"],
        "marking": item["marking"],
        "evidence": item["evidence"],
    }


def derive_recognition(objects, turns, events, user_visible):
    """Reconstruct earned identities from owner events, not ledger copies."""
    recognized = {}
    for ordinal, turn in enumerate(turns or (), start=1):
        action = turn.get("action") or {}
        if action.get("operation") != "INSPECT_OBJECT":
            continue
        target = action.get("target")
        performed = (turn.get("receipt") or {}).get("performed") or {}
        event_id = performed.get("event_id")
        event = (events or {}).get(event_id) if event_id else None
        if (not target or not isinstance(event, dict)
                or event_id not in (user_visible or ())
                or event.get("kind") != "INSPECT"
                or event.get("actor_id") != "U"
                or (event.get("body") or {}).get("target") != target):
            continue
        earned = recognize(target, event.get("summary", ""), objects)
        if earned is not None:
            recognized[target] = {
                **earned,
                "event_id": event_id,
                "turn": ordinal,
            }
    return recognized


def establish(session):
    world = session.world()
    root = session.read_root()["root_hash"]
    epoch = world.clock
    world.resources[SLOT] = {
        "root": root, "branch": session.branch_id, "source": SOURCE, "epoch": epoch,
        "rooms": ROOMS, "objects": OBJECTS,
        "history": {"strap-repair": facts(epoch)["strap-repair"]},
    }
    session.product._checkpoint(session.branch_id, world.clock, world)


def read_house(session):
    world = session.world()
    house = world.resources.get(SLOT)
    if (not house or house.get("source") != SOURCE
            or digest({"rooms": ROOMS, "objects": OBJECTS, "history": HISTORY}) != SOURCE
            or house.get("root") != session.read_root()["root_hash"]
            or house.get("branch") != session.branch_id
            or house.get("rooms") != ROOMS or house.get("objects") != OBJECTS):
        raise RecursionRefusal("P6_HOUSE_SOURCE_OR_ROOT_MISMATCH")
    expected = facts(house["epoch"])
    history = house["history"]
    if ("strap-repair" not in history or any(
            row != expected.get(ref) or any(parent not in history for parent in row["depends_on"])
            for ref, row in history.items())):
        raise RecursionRefusal("P6_OBJECT_PROVENANCE_MISMATCH")
    return world, house


def close_on_repair(session, event):
    """Resolve the support history on actual workshop work, even out of sight."""
    if event["kind"] != "REPAIR" or event["actor_id"] != "A" or event["location"] != "workshop":
        return
    world, house = read_house(session)
    if "bench-installation" not in house["history"]:
        house["history"]["bench-installation"] = facts(house["epoch"])["bench-installation"]
        session.product._append_episode(
            session.branch_id, "A", "P6_OBJECT_CLOSURE", world.clock,
            {"source_event_id": event["event_id"], "fact_id": "bench-installation",
             "source_hash": SOURCE},
        )
        session.product._checkpoint(session.branch_id, world.clock, world)


def perform(session, action):
    from bp4.world import make_event
    from s45_projection.projection import project_event

    world, house = read_house(session)
    user = session.meta["user_actor"]
    room = world.positions[user]
    target = action["target"]
    moving = action["operation"] == "GO"
    item = house["objects"].get(target)
    if (not session.scene_open() or
            (moving and target != house["rooms"][room]["other"]) or
            (not moving and (item is None or item["room"] != room))):
        return {}, {"admission": "UNAVAILABLE", "performed": False, "observation": None}

    if moving:
        world.positions[user] = target
        room = target
        summary = f"You go into the {room}."
    else:
        summary = item["close"]
        if target in {"sandals", "photo"}:
            # Canonical closure is distinct from the close physical observation.
            house["history"]["photo-exposure"] = facts(house["epoch"])["photo-exposure"]
    event = make_event(clock=world.clock, kind="MOVE" if moving else "INSPECT",
                       actor_id=user, location=room, summary=summary, body={"target": target},
                       sequence=len(world.events))
    world.add_event(event)
    session._append_event(event, perceive=(user,))
    if not moving:
        session._perceive_if_present(event, "A", "B")
    session.product._append_episode(session.branch_id, user, "P6_HOUSE_CONDUCT", world.clock,
                                    {"event_id": event["event_id"], "operation": action["operation"]})
    session.product._checkpoint(session.branch_id, world.clock, world)
    return {"performed": event}, {"admission": "ADMITTED", "performed": True,
                                  "observation": project_event(event)}


def scene(session):
    world, house = read_house(session)
    room = world.positions[session.meta["user_actor"]]
    return {
        "room": room, "orientation": house["rooms"][room]["line"],
        "exit": house["rooms"][room]["other"],
        "objects": {ref: row["glance"] for ref, row in house["objects"].items() if row["room"] == room},
    }
