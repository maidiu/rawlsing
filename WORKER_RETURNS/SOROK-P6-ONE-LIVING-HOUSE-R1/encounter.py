"""P6 movement evidence, separate from actor perception and world writes."""

from developmental_recursion.contracts import RecursionRefusal, digest

# Explicit sourcefree scene law, available only when a fixture establishes
# these facts in the existing world checkpoint. No ordinary house has them.
VISUAL_FIXTURE = {
    "grade": "SOURCEFREE_TEST_ONLY",
    "transition": ["living room", "workshop"],
    "illumination": "lit",
    "sightline": "unobstructed",
    "recipients": {
        "A": {"location": "workshop", "facing": "doorway", "visual_capacity": "available"},
        "B": {"location": "workshop", "facing": "away", "visual_capacity": "available"},
    },
}
VISUAL_SOURCE = digest(VISUAL_FIXTURE)


def movement_evidence(session, event, world, house):
    """Derive actor-relative eligibility for the just-committed P6 GO."""
    user = session.meta["user_actor"]
    body = event["body"]
    origin = body.get("origin")
    destination = event["location"]
    if (session.event(event["event_id"]) != event or event["kind"] != "MOVE"
            or event["actor_id"] != user or event["clock"] != world.clock
            or body.get("root") != house["root"] or body.get("branch") != house["branch"]
            or body.get("house_source") != house["source"]
            or body.get("target") != destination or world.positions.get(user) != destination
            or house["rooms"].get(origin, {}).get("other") != destination):
        raise RecursionRefusal("P6_ENCOUNTER_MOVEMENT_SOURCE_MISMATCH")
    if not any(row["kind"] == "P6_HOUSE_CONDUCT" and row["clock"] == event["clock"]
               and row["body"] == {"event_id": event["event_id"], "operation": "GO"}
               for row in reversed(session.episodes(user))):
        raise RecursionRefusal("P6_ENCOUNTER_MOVEMENT_PARENT_MISSING")

    fixture = house.get("movement_visual_fixture")
    known_visual = (fixture == {"source": VISUAL_SOURCE, "facts": VISUAL_FIXTURE}
                    and digest(VISUAL_FIXTURE) == VISUAL_SOURCE
                    and event["clock"] == house["epoch"] + 1
                    and [origin, destination] == VISUAL_FIXTURE["transition"])
    evidence = []
    for actor in ("A", "B"):
        position = world.positions.get(actor)
        modality, eligibility, basis = None, "UNKNOWN", "NO_QUALIFIED_MODALITY"
        if known_visual:
            condition = VISUAL_FIXTURE["recipients"][actor]
            if position == condition["location"]:
                modality = "VISUAL"
                eligibility = "ELIGIBLE" if condition["facing"] == "doorway" else "UNAVAILABLE"
                basis = "SOURCEFREE_DOORWAY_SIGHTLINE" if eligibility == "ELIGIBLE" else "FACING_AWAY"
        evidence.append({
            "schema": "P6_MOVEMENT_EVIDENCE@1",
            "grade": "SOURCEFREE_TEST_ONLY",
            "root": house["root"], "branch": house["branch"], "clock": event["clock"],
            "event_id": event["event_id"], "event_hash": event["hash"],
            "world_source": house["source"], "modality_source": VISUAL_SOURCE if modality else None,
            "performer": user, "recipient": actor,
            "origin": origin, "destination": destination, "recipient_location": position,
            "modality": modality, "eligibility": eligibility, "basis": basis,
            "uptake": "HOLD_ACTOR_REGISTRATION_OWNER_MISSING",
        })
    return evidence
