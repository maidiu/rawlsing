"""Sourcefree room and object facts held in the received BP4 world checkpoint."""

from developmental_recursion.contracts import RecursionRefusal, digest

from encounter import movement_evidence
from mii import close_available

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

GALLERY_ROOMS = {
    "gallery": {"other": "storeroom", "line": "A narrow gallery opens toward a storeroom."},
    "storeroom": {"other": "gallery", "line": "The gallery is behind you. Shelves line the storeroom."},
}
GALLERY_OBJECTS = {
    "hinge": {
        "room": "gallery", "glance": "A brass hinge rests on a plinth.",
        "close": "The hinge carries the stamped mark G-17.",
        "specialist_identity": "the stamped brass hinge",
        "marking": "stamped-mark-g-17",
        "evidence": "The hinge carries the stamped mark G-17.",
    },
    "ledger": {
        "room": "storeroom", "glance": "A cloth-bound ledger lies on a shelf.",
        "close": "The ledger's spine is worn at the lower corner.",
    },
}
GALLERY_HISTORY = ()
GALLERY_SOURCE = digest({
    "rooms": GALLERY_ROOMS, "objects": GALLERY_OBJECTS,
    "history": GALLERY_HISTORY,
})

SYMBOLIC_ROOMS = {
    "salon": {"other": "alcove", "line": "A quiet salon opens toward a small alcove."},
    "alcove": {"other": "salon", "line": "The salon is behind you. A shelf fills the alcove."},
}
SYMBOLIC_OBJECTS = {
    "watch": {
        "room": "salon", "glance": "A steel watch lies open on a velvet cloth.",
        "close": "The watch carries an engraved crest.",
        "specialist_identity": "the engraved steel watch",
        "marking": "engraved-crest", "evidence": "The watch carries an engraved crest.",
    },
    "icon": {
        "room": "alcove", "glance": "A small painted icon rests on a shelf.",
        "close": "The icon's border is worn smooth.",
    },
}
SYMBOLIC_HISTORY = ()
SYMBOLIC_SOURCE = digest({
    "rooms": SYMBOLIC_ROOMS, "objects": SYMBOLIC_OBJECTS,
    "history": SYMBOLIC_HISTORY,
})


def facts_for(history, objects, epoch):
    result = {}
    for row in history:
        clock = epoch + row["offset"]
        if (row["id"] in result or row["object"] not in objects
                or clock >= epoch or any(parent not in result or result[parent]["clock"] >= clock
                                        for parent in row["depends_on"])):
            raise RecursionRefusal("P6_INVALID_OBJECT_CHRONOLOGY")
        result[row["id"]] = {**row, "clock": clock}
    return result


def facts(epoch):
    return facts_for(HISTORY, OBJECTS, epoch)


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


def _material(source):
    if source == SOURCE:
        return ROOMS, OBJECTS, HISTORY, True
    if source == GALLERY_SOURCE:
        return GALLERY_ROOMS, GALLERY_OBJECTS, GALLERY_HISTORY, False
    if source == SYMBOLIC_SOURCE:
        return SYMBOLIC_ROOMS, SYMBOLIC_OBJECTS, SYMBOLIC_HISTORY, False
    return None


def establish(session):
    world = session.world()
    root = session.read_root()["root_hash"]
    epoch = world.clock
    world.resources[SLOT] = {
        "root": root, "branch": session.branch_id, "source": SOURCE, "epoch": epoch,
        "rooms": ROOMS, "objects": OBJECTS,
        "presentation_conditions": {
            "grade": "SOURCEFREE_FIXTURE", "light": "lit",
            "sightline": "unobstructed", "legibility": "readable",
            "observer": session.meta["user_actor"], "objects": {},
        },
        "history": {"strap-repair": facts(epoch)["strap-repair"]},
    }
    session.product._checkpoint(session.branch_id, world.clock, world)


def establish_gallery(session):
    world = session.world()
    root = session.read_root()["root_hash"]
    epoch = world.clock
    user = session.meta["user_actor"]
    world.positions[user] = "gallery"
    world.resources[SLOT] = {
        "root": root, "branch": session.branch_id, "source": GALLERY_SOURCE,
        "epoch": epoch, "rooms": GALLERY_ROOMS, "objects": GALLERY_OBJECTS,
        "presentation_conditions": {
            "grade": "SOURCEFREE_FIXTURE", "light": "lit",
            "sightline": "unobstructed", "legibility": "readable",
            "observer": user, "objects": {},
        },
        "history": {},
    }
    session.product._checkpoint(session.branch_id, world.clock, world)


def establish_symbolic(session):
    world = session.world()
    root = session.read_root()["root_hash"]
    epoch = world.clock
    user = session.meta["user_actor"]
    world.positions[user] = "salon"
    world.resources[SLOT] = {
        "root": root, "branch": session.branch_id, "source": SYMBOLIC_SOURCE,
        "epoch": epoch, "rooms": SYMBOLIC_ROOMS, "objects": SYMBOLIC_OBJECTS,
        "presentation_conditions": {
            "grade": "SOURCEFREE_FIXTURE", "light": "lit",
            "sightline": "unobstructed", "legibility": "readable",
            "observer": user, "objects": {},
        },
        "history": {},
    }
    session.product._checkpoint(session.branch_id, world.clock, world)


def read_house(session):
    world = session.world()
    house = world.resources.get(SLOT)
    if not house or house.get("root") != session.read_root()["root_hash"]:
        raise RecursionRefusal("P6_HOUSE_SOURCE_OR_ROOT_MISMATCH")
    if house.get("branch") != session.branch_id:
        raise RecursionRefusal("P6_HOUSE_SOURCE_OR_ROOT_MISMATCH")
    material = _material(house.get("source"))
    if material is None:
        raise RecursionRefusal("P6_HOUSE_SOURCE_OR_ROOT_MISMATCH")
    rooms, objects, history_spec, requires_repair = material
    if (digest({"rooms": rooms, "objects": objects, "history": history_spec})
            != house.get("source")
            or house.get("rooms") != rooms or house.get("objects") != objects):
        raise RecursionRefusal("P6_HOUSE_SOURCE_OR_ROOT_MISMATCH")
    expected = facts_for(history_spec, objects, house["epoch"])
    history = house["history"]
    if (requires_repair and "strap-repair" not in history) or any(
            row != expected.get(ref) or any(parent not in history for parent in row["depends_on"])
            for ref, row in history.items()):
        raise RecursionRefusal("P6_OBJECT_PROVENANCE_MISMATCH")
    return world, house


def close_on_repair(session, event):
    """Resolve the support history on actual workshop work, even out of sight."""
    if event["kind"] != "REPAIR" or event["actor_id"] != "A" or event["location"] != "workshop":
        return
    world, house = read_house(session)
    if house.get("source") != SOURCE:
        return
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
            (not moving and (item is None or item["room"] != room)) or
            (not moving and not close_available(house, session.meta["user_actor"], target))):
        return {}, {"admission": "UNAVAILABLE", "performed": False, "observation": None}

    body = {"target": target}
    if moving:
        body.update(origin=room, root=house["root"], branch=house["branch"],
                    house_source=house["source"])
        house.pop("outward_near_actor", None)
        world.positions[user] = target
        room = target
        summary = f"You go into the {room}."
    else:
        summary = item["close"]
        if target in {"sandals", "photo"}:
            # Canonical closure is distinct from the close physical observation.
            house["history"]["photo-exposure"] = facts(house["epoch"])["photo-exposure"]
    event = make_event(clock=world.clock, kind="MOVE" if moving else "INSPECT",
                       actor_id=user, location=room, summary=summary, body=body,
                       sequence=len(world.events))
    world.add_event(event)
    session._append_event(event, perceive=(user,))
    if not moving:
        session._perceive_if_present(event, "A", "B")
    session.product._append_episode(session.branch_id, user, "P6_HOUSE_CONDUCT", world.clock,
                                    {"event_id": event["event_id"], "operation": action["operation"]})
    session.product._checkpoint(session.branch_id, world.clock, world)
    receipt = {"performed": event}
    if moving:
        committed_world, committed_house = read_house(session)
        receipt["encounter_evidence"] = movement_evidence(
            session, event, committed_world, committed_house,
        )
    return receipt, {"admission": "ADMITTED", "performed": True,
                     "observation": project_event(event)}


def scene(session):
    world, house = read_house(session)
    room = world.positions[session.meta["user_actor"]]
    return {
        "room": room, "orientation": house["rooms"][room]["line"],
        "exit": house["rooms"][room]["other"],
        "objects": {ref: row["glance"] for ref, row in house["objects"].items() if row["room"] == room},
    }
