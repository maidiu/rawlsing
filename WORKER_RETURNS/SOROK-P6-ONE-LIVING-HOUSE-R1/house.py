"""Sourcefree room and object facts held in the received BP4 world checkpoint."""

import math

from developmental_recursion.contracts import RecursionRefusal, detached, digest
from developmental_recursion.p2_owner import (
    branch_is_ancestor,
    material_fact_source,
    write_material_fact,
)

from encounter import movement_evidence
from mii import close_available

SLOT = "p6_house"
HOUSEHOLD_SLOT = "p6_household"
HOUSEHOLD_SCHEMA = "SOROK_HOUSEHOLD_MATERIAL@1"
HOUSEHOLD_READ_SCHEMA = "SOROK_HOUSEHOLD_MATERIAL_READ@1"
HOUSEHOLD_GRADE = "SOURCEFREE_FIXTURE"
HOUSEHOLD_FIELDS = frozenset({"schema", "grade", "place", "owner", "resources"})
HOUSEHOLD_STORED_FIELDS = frozenset({
    *HOUSEHOLD_FIELDS, "root", "branch", "epoch", "source",
})
PARENT_CHOICE_INPUT_SCHEMA = "SOROK_PARENT_CHOICE_INPUT@1"
DWELLING_SLOT = "p6_dwelling"
DWELLING_SCHEMA = "SOROK_DWELLING_MATERIAL@1"
DWELLING_READ_SCHEMA = "SOROK_DWELLING_MATERIAL_READ@1"
DWELLING_GRADE = "SOURCEFREE_FIXTURE"
DWELLING_FIELDS = frozenset({"schema", "grade", "home", "space", "acoustics", "costs"})
DWELLING_STORED_FIELDS = frozenset({*DWELLING_FIELDS, "root", "branch", "epoch", "source"})
DRUM_KIT_REQUEST_SCHEMA = "SOROK_DRUM_KIT_REQUEST@1"
MATERIAL_FEASIBILITY_SCHEMA = "SOROK_MATERIAL_FEASIBILITY@1"
MOTHER_MATERIAL_INPUT_SCHEMA = "SOROK_MOTHER_MATERIAL_INPUT@1"
DWELLING_INSTRUMENT_POLICIES = frozenset({
    "prohibited", "acoustic_instruments_with_quiet_hours", "UNRESTRICTED", "UNKNOWN",
})
HOUSEHOLD_WORLD_RESOURCE_SLOTS = frozenset({"workshop"})
HOUSEHOLD_ACTOR_SLOTS = frozenset({"A"})
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


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _scalar(value):
    return type(value) in (bool, int, str)


def household_fixture(session):
    """Bounded household fixture bound to the actual root actor and house place."""
    world = session.world()
    holder = world.actor_state.get("A")
    actor_id = holder.get("actor_id") if isinstance(holder, dict) else None
    root = session.read_root()
    if not _text(actor_id) or actor_id not in root["actor_ids"]:
        raise RecursionRefusal("P6_HOUSEHOLD_OWNER_UNAVAILABLE")
    place = {
        "dwelling_id": "dwelling:p6-workshop-home",
        "kind": "two_room_dwelling",
        "rooms": list(ROOMS),
        "tenure": "rented",
        "tenancy": {
            "holder_actor_slot": "A",
            "landlord_ref": "SOURCEFREE_FIXTURE_LANDLORD",
        },
    }
    return {
        "schema": HOUSEHOLD_SCHEMA,
        "grade": HOUSEHOLD_GRADE,
        "place": place,
        "owner": {
            "actor_slot": "A",
            "actor_id": actor_id,
            "authority": "household_holder",
        },
        "resources": {
            "bindings": [
                {"kind": "WORLD_RESOURCE", "slot": "workshop",
                 "fields": ["tool_available", "material"]},
                {"kind": "ACTOR_STATE", "actor_slot": "A",
                 "fields": ["cash", "material_remaining", "free_hours"]},
            ],
        },
    }


def _bindings(bindings, world):
    if not isinstance(bindings, list) or not bindings:
        raise RecursionRefusal("P6_HOUSEHOLD_RESOURCE_BINDING")
    resolved, seen = [], set()
    for binding in bindings:
        if not isinstance(binding, dict):
            raise RecursionRefusal("P6_HOUSEHOLD_RESOURCE_BINDING")
        kind = binding.get("kind")
        if kind == "WORLD_RESOURCE":
            if set(binding) != {"kind", "slot", "fields"}:
                raise RecursionRefusal("P6_HOUSEHOLD_RESOURCE_BINDING")
            slot = binding.get("slot")
            row = world.resources.get(slot) if _text(slot) else None
            if (slot not in HOUSEHOLD_WORLD_RESOURCE_SLOTS
                    or not isinstance(row, dict)):
                raise RecursionRefusal("P6_HOUSEHOLD_RESOURCE_BINDING")
            key = ("WORLD_RESOURCE", slot)
        elif kind == "ACTOR_STATE":
            if set(binding) != {"kind", "actor_slot", "fields"}:
                raise RecursionRefusal("P6_HOUSEHOLD_RESOURCE_BINDING")
            slot = binding.get("actor_slot")
            row = world.actor_state.get(slot) if _text(slot) else None
            if slot not in HOUSEHOLD_ACTOR_SLOTS or not isinstance(row, dict):
                raise RecursionRefusal("P6_HOUSEHOLD_RESOURCE_BINDING")
            key = ("ACTOR_STATE", slot)
        else:
            raise RecursionRefusal("P6_HOUSEHOLD_RESOURCE_BINDING")
        fields = binding.get("fields")
        if (not isinstance(fields, list) or not fields or len(set(fields)) != len(fields)
                or any(not _text(field) for field in fields) or key in seen
                or any(field not in row or not _scalar(row[field]) for field in fields)):
            raise RecursionRefusal("P6_HOUSEHOLD_RESOURCE_BINDING")
        seen.add(key)
        if kind == "WORLD_RESOURCE":
            resolved.append({"kind": kind, "slot": slot,
                             "fields": {field: row[field] for field in fields}})
        else:
            resolved.append({"kind": kind, "actor_slot": slot,
                             "actor_id": row.get("actor_id"),
                             "fields": {field: row[field] for field in fields}})
    return resolved


def _material_provenance(stored_branch, current_branch):
    inherited = stored_branch != current_branch
    return {
        "stored_branch": stored_branch,
        "current_branch": current_branch,
        "inherited": inherited,
        "scope": "P6_MATERIAL_FACT_ONLY",
        "fork_state": ("C12_FORK_WITHOUT_S46_INTERVAL_STATE"
                       if inherited else "CURRENT_BRANCH"),
    }


def _number(value):
    return type(value) in (int, float) and math.isfinite(value)


def _number_or_unknown(value):
    return value == "UNKNOWN" or _number(value)


def _nonneg(value):
    return _number(value) and value >= 0


def _nonneg_or_unknown(value):
    return value == "UNKNOWN" or _nonneg(value)


def _int_or_unknown(value):
    return value == "UNKNOWN" or (type(value) is int and value >= 0)


def _read_household_document(document, world, root, branch, actor_ids, *,
                             branch_ok=None):
    if not isinstance(document, dict) or set(document) != HOUSEHOLD_STORED_FIELDS:
        raise RecursionRefusal("P6_HOUSEHOLD_SCHEMA")
    if document.get("schema") != HOUSEHOLD_SCHEMA or document.get("grade") != HOUSEHOLD_GRADE:
        raise RecursionRefusal("P6_HOUSEHOLD_SCHEMA")
    stored_branch = document.get("branch")
    if (document.get("root") != root
            or (stored_branch != branch
                and not (branch_ok is not None
                         and branch_ok(stored_branch, document.get("epoch"))))):
        raise RecursionRefusal("P6_HOUSEHOLD_SOURCE_OR_ROOT_MISMATCH")
    epoch = document.get("epoch")
    if (isinstance(epoch, bool) or not isinstance(epoch, int)
            or epoch < 0 or epoch > world.clock):
        raise RecursionRefusal("P6_HOUSEHOLD_SOURCE_OR_ROOT_MISMATCH")
    source = document.get("source")
    if (not isinstance(source, str) or len(source) != 64
            or material_fact_source(document) != source):
        raise RecursionRefusal("P6_HOUSEHOLD_SOURCE_OR_ROOT_MISMATCH")
    place = document.get("place")
    if (not isinstance(place, dict)
            or set(place) != {"dwelling_id", "kind", "rooms", "tenure", "tenancy"}
            or not _text(place.get("dwelling_id")) or not _text(place.get("kind"))
            or not _text(place.get("tenure")) or place.get("rooms") != list(ROOMS)):
        raise RecursionRefusal("P6_HOUSEHOLD_SCHEMA")
    tenancy = place.get("tenancy")
    if (not isinstance(tenancy, dict)
            or set(tenancy) != {"holder_actor_slot", "landlord_ref"}
            or not _text(tenancy.get("holder_actor_slot"))
            or not _text(tenancy.get("landlord_ref"))):
        raise RecursionRefusal("P6_HOUSEHOLD_SCHEMA")
    owner = document.get("owner")
    if (not isinstance(owner, dict)
            or set(owner) != {"actor_slot", "actor_id", "authority"}
            or owner.get("authority") != "household_holder"
            or not _text(owner.get("actor_slot")) or not _text(owner.get("actor_id"))):
        raise RecursionRefusal("P6_HOUSEHOLD_OWNER_MISMATCH")
    holder = world.actor_state.get(owner["actor_slot"])
    if (not isinstance(holder, dict) or holder.get("actor_id") != owner["actor_id"]
            or tenancy["holder_actor_slot"] != owner["actor_slot"]
            or owner["actor_id"] not in actor_ids):
        raise RecursionRefusal("P6_HOUSEHOLD_OWNER_MISMATCH")
    resources = document.get("resources")
    if not isinstance(resources, dict) or set(resources) != {"bindings"}:
        raise RecursionRefusal("P6_HOUSEHOLD_RESOURCE_BINDING")
    resolved = _bindings(resources.get("bindings"), world)
    material_hash = digest({
        "root": root, "branch": branch, "clock": world.clock,
        "epoch": epoch, "source": source, "place": detached(place),
        "owner": detached(owner), "resources": resolved,
    })
    return {
        "schema": HOUSEHOLD_READ_SCHEMA,
        "grade": HOUSEHOLD_GRADE,
        "root": root,
        "branch": branch,
        "clock": world.clock,
        "epoch": epoch,
        "source": source,
        "material_hash": material_hash,
        "place": detached(place),
        "owner": detached(owner),
        "resources": resolved,
        "world_state_hash": digest(world.snapshot()),
        "provenance": _material_provenance(stored_branch, branch),
    }


def establish_household(session, *, fixture=None):
    """Admit the bounded household fixture through the actual P2 world writer."""
    world = session.world()
    root = session.read_root()["root_hash"]
    content = detached(household_fixture(session) if fixture is None else fixture)
    document = {**content, "root": root, "branch": session.branch_id,
                "epoch": world.clock}
    document["source"] = material_fact_source(document)
    _read_household_document(document, world, root, session.branch_id,
                             tuple(session.read_root().get("actor_ids") or ()))
    existing = world.resources.get(HOUSEHOLD_SLOT)
    if existing is not None and existing != document:
        raise RecursionRefusal("P6_HOUSEHOLD_ALREADY_ESTABLISHED")
    write_material_fact(session, slot=HOUSEHOLD_SLOT, document=document)
    return read_household(session)


def read_household(session):
    """Read the world-owned household fixture, never a PsycheStore record."""
    world = session.world()
    document = world.resources.get(HOUSEHOLD_SLOT)
    if document is None:
        raise RecursionRefusal("P6_HOUSEHOLD_ABSENT")
    root_row = session.read_root()
    return _read_household_document(
        document, world, root_row["root_hash"], session.branch_id,
        tuple(root_row.get("actor_ids") or ()),
        branch_ok=lambda stored, epoch: branch_is_ancestor(session, stored, epoch),
    )


def parent_choice_input(session):
    """Freeze the read-only household input; no parent action is performed."""
    household = read_household(session)
    return {
        "schema": PARENT_CHOICE_INPUT_SCHEMA,
        "grade": "SOURCEFREE_S2_ONLY",
        "first_consumer": "NONE_VERIFIED",
        "parent_decision": "NOT_EVALUATED",
        "parent_action": None,
        "source": {
            "owner": "S47_P2_OBJECTIVE_WORLD",
            "slot": HOUSEHOLD_SLOT,
            "ref": "P6_HOUSEHOLD:" + household["source"],
            "hash": household["source"],
            "material_hash": household["material_hash"],
            "stored_branch": household["provenance"]["stored_branch"],
            "inherited": household["provenance"]["inherited"],
            "fork_state": household["provenance"]["fork_state"],
        },
        "root_hash": household["root"],
        "branch_id": household["branch"],
        "clock": household["clock"],
        "epoch": household["epoch"],
        "household": {
            "place": household["place"],
            "owner": household["owner"],
            "resources": household["resources"],
        },
        "provenance": detached(household["provenance"]),
        "read_boundary": {
            "psyche_store": "NOT_READ",
            "parent_hidden_reason": "NOT_READ",
            "model_prose": "NOT_READ",
        },
    }


DRUM_KIT_REQUESTS = {
    "acoustic": {
        "schema": DRUM_KIT_REQUEST_SCHEMA,
        "grade": DWELLING_GRADE,
        "request_id": "request:drum-kit:acoustic",
        "kind": "acoustic_drum_kit",
        "setup": "acoustic",
        "footprint_m2": 2.4,
        "loudness_db": 95,
        "purchase_price": 180,
        "currency_unit": "sourcefree_currency_unit",
    },
    "junior": {
        "schema": DRUM_KIT_REQUEST_SCHEMA,
        "grade": DWELLING_GRADE,
        "request_id": "request:drum-kit:junior",
        "kind": "junior_drum_kit",
        "setup": "acoustic",
        "footprint_m2": 1.2,
        "loudness_db": 70,
        "purchase_price": 40,
        "currency_unit": "sourcefree_currency_unit",
    },
}


def dwelling_fixture(session):
    """Bounded home/tenancy/space/acoustics/costs committed through B01 facts."""
    household = read_household(session)
    place = household["place"]
    owner = household["owner"]
    return {
        "schema": DWELLING_SCHEMA,
        "grade": DWELLING_GRADE,
        "home": {
            "dwelling_id": place["dwelling_id"],
            "kind": place["kind"],
            "rooms": list(place["rooms"]),
            "tenure": place["tenure"],
            "tenancy": {
                "holder_actor_slot": owner["actor_slot"],
                "landlord_ref": place["tenancy"]["landlord_ref"],
                "instrument_policy": "acoustic_instruments_with_quiet_hours",
                "lease_constraints": ["no_structural_changes", "quiet_hours_22_07"],
            },
        },
        "space": {
            "usable_room": "living room",
            "floor_area_m2": 8.0,
            "clearance_m2": 1.0,
            "ceiling_height_m": 2.4,
        },
        "acoustics": {
            "wall_construction": "masonry",
            "sound_rating_db": 45,
            "max_indoor_loudness_db": 80,
            "neighbor_shared_walls": 2,
            "quiet_hours": "22:00-07:00",
        },
        "costs": {
            "monthly_rent": 12,
            "rent_due_now": 12,
            "currency_unit": "sourcefree_currency_unit",
        },
    }


def _read_dwelling_document(document, world, root, branch, household, *,
                            branch_ok=None):
    if not isinstance(document, dict) or set(document) != DWELLING_STORED_FIELDS:
        raise RecursionRefusal("P6_DWELLING_SCHEMA")
    if document.get("schema") != DWELLING_SCHEMA or document.get("grade") != DWELLING_GRADE:
        raise RecursionRefusal("P6_DWELLING_SCHEMA")
    stored_branch = document.get("branch")
    if (document.get("root") != root
            or (stored_branch != branch
                and not (branch_ok is not None
                         and branch_ok(stored_branch, document.get("epoch"))))):
        raise RecursionRefusal("P6_DWELLING_SOURCE_OR_ROOT_MISMATCH")
    epoch = document.get("epoch")
    if (isinstance(epoch, bool) or not isinstance(epoch, int)
            or epoch < 0 or epoch > world.clock):
        raise RecursionRefusal("P6_DWELLING_SOURCE_OR_ROOT_MISMATCH")
    source = document.get("source")
    if (not isinstance(source, str) or len(source) != 64
            or material_fact_source(document) != source):
        raise RecursionRefusal("P6_DWELLING_SOURCE_OR_ROOT_MISMATCH")
    home = document.get("home")
    place = household["place"]
    owner = household["owner"]
    if (not isinstance(home, dict)
            or set(home) != {"dwelling_id", "kind", "rooms", "tenure", "tenancy"}
            or not _text(home.get("dwelling_id")) or not _text(home.get("kind"))
            or not _text(home.get("tenure")) or home.get("rooms") != list(ROOMS)):
        raise RecursionRefusal("P6_DWELLING_SCHEMA")
    tenancy = home.get("tenancy")
    if (not isinstance(tenancy, dict)
            or set(tenancy) != {"holder_actor_slot", "landlord_ref",
                                "instrument_policy", "lease_constraints"}
            or not _text(tenancy.get("holder_actor_slot"))
            or not _text(tenancy.get("landlord_ref"))
            or tenancy.get("instrument_policy") not in DWELLING_INSTRUMENT_POLICIES):
        raise RecursionRefusal("P6_DWELLING_TENANCY")
    constraints = tenancy.get("lease_constraints")
    if (not isinstance(constraints, list) or not constraints
            or len(set(constraints)) != len(constraints)
            or any(not _text(item) for item in constraints)):
        raise RecursionRefusal("P6_DWELLING_TENANCY")
    if (home["dwelling_id"] != place["dwelling_id"]
            or home["kind"] != place["kind"]
            or home["rooms"] != place["rooms"]
            or home["tenure"] != place["tenure"]
            or tenancy["holder_actor_slot"] != owner["actor_slot"]
            or tenancy["landlord_ref"] != place["tenancy"]["landlord_ref"]):
        raise RecursionRefusal("P6_DWELLING_HOUSEHOLD_MISMATCH")
    space = document.get("space")
    if (not isinstance(space, dict)
            or set(space) != {"usable_room", "floor_area_m2", "clearance_m2",
                              "ceiling_height_m"}
            or space.get("usable_room") not in home["rooms"]
            or not _nonneg_or_unknown(space.get("floor_area_m2"))
            or not _nonneg_or_unknown(space.get("clearance_m2"))
            or not _number_or_unknown(space.get("ceiling_height_m"))
            or (space.get("ceiling_height_m") != "UNKNOWN"
                and space["ceiling_height_m"] <= 0)):
        raise RecursionRefusal("P6_DWELLING_SPACE")
    acoustics = document.get("acoustics")
    if (not isinstance(acoustics, dict)
            or set(acoustics) != {"wall_construction", "sound_rating_db",
                                  "max_indoor_loudness_db", "neighbor_shared_walls",
                                  "quiet_hours"}
            or not (_text(acoustics.get("wall_construction"))
                    or acoustics.get("wall_construction") == "UNKNOWN")
            or not _nonneg_or_unknown(acoustics.get("sound_rating_db"))
            or not _nonneg_or_unknown(acoustics.get("max_indoor_loudness_db"))
            or not _int_or_unknown(acoustics.get("neighbor_shared_walls"))
            or not _text(acoustics.get("quiet_hours"))):
        raise RecursionRefusal("P6_DWELLING_ACOUSTICS")
    costs = document.get("costs")
    if (not isinstance(costs, dict)
            or set(costs) != {"monthly_rent", "rent_due_now", "currency_unit"}
            or not _nonneg_or_unknown(costs.get("monthly_rent"))
            or not _nonneg_or_unknown(costs.get("rent_due_now"))
            or not _text(costs.get("currency_unit"))):
        raise RecursionRefusal("P6_DWELLING_COSTS")
    material_hash = digest({
        "root": root, "branch": branch, "clock": world.clock,
        "epoch": epoch, "source": source, "home": detached(home),
        "space": detached(space), "acoustics": detached(acoustics),
        "costs": detached(costs),
    })
    return {
        "schema": DWELLING_READ_SCHEMA,
        "grade": DWELLING_GRADE,
        "root": root,
        "branch": branch,
        "clock": world.clock,
        "epoch": epoch,
        "source": source,
        "material_hash": material_hash,
        "home": detached(home),
        "space": detached(space),
        "acoustics": detached(acoustics),
        "costs": detached(costs),
        "household_source": household["source"],
        "household_material_hash": household["material_hash"],
        "world_state_hash": digest(world.snapshot()),
        "provenance": _material_provenance(stored_branch, branch),
    }


def _dwelling_document(session, facts):
    world = session.world()
    root = session.read_root()["root_hash"]
    content = detached(dwelling_fixture(session) if facts is None else facts)
    document = {**content, "root": root, "branch": session.branch_id,
                "epoch": world.clock}
    document["source"] = material_fact_source(document)
    household = read_household(session)
    _read_dwelling_document(document, world, root, session.branch_id, household)
    return document


def establish_dwelling(session, *, facts=None):
    """Admit one bounded dwelling material fact through the actual P2 writer."""
    world = session.world()
    document = _dwelling_document(session, facts)
    existing = world.resources.get(DWELLING_SLOT)
    if existing is not None and existing != document:
        raise RecursionRefusal("P6_DWELLING_ALREADY_ESTABLISHED")
    write_material_fact(session, slot=DWELLING_SLOT, document=document)
    return read_dwelling(session)


def commit_dwelling(session, *, facts=None):
    """Commit selected dwelling facts; the checkpoint keeps the current source."""
    document = _dwelling_document(session, facts)
    if session.world().resources.get(DWELLING_SLOT) == document:
        return read_dwelling(session)
    write_material_fact(session, slot=DWELLING_SLOT, document=document)
    return read_dwelling(session)


def read_dwelling(session):
    """Read source-qualified dwelling material, never a psyche or class label."""
    world = session.world()
    document = world.resources.get(DWELLING_SLOT)
    if document is None:
        raise RecursionRefusal("P6_DWELLING_ABSENT")
    household = read_household(session)
    root_row = session.read_root()
    return _read_dwelling_document(
        document, world, root_row["root_hash"], session.branch_id, household,
        branch_ok=lambda stored, epoch: branch_is_ancestor(session, stored, epoch),
    )


def _validate_drum_kit_request(request):
    fields = {"schema", "grade", "request_id", "kind", "setup",
              "footprint_m2", "loudness_db", "purchase_price", "currency_unit"}
    if not isinstance(request, dict) or set(request) != fields:
        raise RecursionRefusal("P6_DRUM_KIT_REQUEST_SCHEMA")
    request = detached(request)
    if (request.get("schema") != DRUM_KIT_REQUEST_SCHEMA
            or request.get("grade") != DWELLING_GRADE
            or not _text(request.get("request_id"))
            or not _text(request.get("kind"))
            or not _text(request.get("setup"))
            or not _text(request.get("currency_unit"))
            or not _nonneg(request.get("footprint_m2"))
            or not _nonneg(request.get("loudness_db"))
            or not _nonneg(request.get("purchase_price"))
            or request["footprint_m2"] <= 0):
        raise RecursionRefusal("P6_DRUM_KIT_REQUEST_SCHEMA")
    return request


def _household_cash(household):
    for binding in household["resources"]:
        if (binding.get("kind") == "ACTOR_STATE"
                and binding.get("actor_slot") == "A"):
            cash = (binding.get("fields") or {}).get("cash")
            return cash if _nonneg(cash) else None
    return None


def material_feasibility(session, request=None):
    """Evaluate one concrete request against committed world material facts."""
    dwelling = read_dwelling(session)
    household = read_household(session)
    request = _validate_drum_kit_request(
        DRUM_KIT_REQUESTS["acoustic"] if request is None else request
    )
    home, space = dwelling["home"], dwelling["space"]
    acoustics, costs = dwelling["acoustics"], dwelling["costs"]
    policy = home["tenancy"]["instrument_policy"]
    reasons, unknowns, conditions = [], [], []
    if policy == "prohibited":
        reasons.append("REFUSED_TENANCY")
    elif policy == "UNKNOWN":
        unknowns.append("UNKNOWN_TENANCY_POLICY")
    elif policy == "acoustic_instruments_with_quiet_hours":
        conditions.append("QUIET_HOURS=" + acoustics["quiet_hours"])
    max_db = acoustics["max_indoor_loudness_db"]
    if max_db == "UNKNOWN":
        unknowns.append("UNKNOWN_ACOUSTICS")
    elif request["loudness_db"] > max_db:
        reasons.append("REFUSED_NOISE")
    area = space["floor_area_m2"]
    clearance = space["clearance_m2"]
    if area == "UNKNOWN" or clearance == "UNKNOWN":
        unknowns.append("UNKNOWN_SPACE")
    elif request["footprint_m2"] > area - clearance:
        reasons.append("REFUSED_SPACE")
    cash = _household_cash(household)
    rent = costs["rent_due_now"]
    if request["currency_unit"] != costs["currency_unit"]:
        unknowns.append("UNKNOWN_CURRENCY")
    elif cash is None or rent == "UNKNOWN":
        unknowns.append("UNKNOWN_AFFORDABILITY")
    elif request["purchase_price"] > cash - rent:
        reasons.append("REFUSED_AFFORDABILITY")
    status = "REFUSED" if reasons else ("UNKNOWN" if unknowns else "ADMISSIBLE")
    return {
        "schema": MATERIAL_FEASIBILITY_SCHEMA,
        "grade": "SOURCEFREE_S2_ONLY",
        "status": status,
        "reasons": reasons,
        "unknowns": unknowns,
        "conditions": conditions,
        "request": request,
        "dwelling": {
            "source": dwelling["source"],
            "material_hash": dwelling["material_hash"],
            "provenance": dwelling["provenance"],
        },
        "household": {
            "source": household["source"],
            "material_hash": household["material_hash"],
            "provenance": household["provenance"],
        },
        "root_hash": dwelling["root"],
        "branch_id": dwelling["branch"],
        "clock": dwelling["clock"],
        "material_reader": "house.material_feasibility",
        "mother_decision": "NOT_EVALUATED",
        "parent_action": None,
        "possession_created": False,
        "read_boundary": {
            "psyche_store": "NOT_READ",
            "class_to_trait": "NOT_APPLIED",
            "model_prose": "NOT_READ",
        },
    }


def mother_material_input(session, request=None):
    """Freeze the material input for the later mother decision candidate."""
    dwelling = read_dwelling(session)
    household = read_household(session)
    feasibility = material_feasibility(session, request)
    return {
        "schema": MOTHER_MATERIAL_INPUT_SCHEMA,
        "grade": "SOURCEFREE_S2_ONLY",
        "first_consumer": "NONE_VERIFIED",
        "material_reader": "house.material_feasibility",
        "mother_decision": "NOT_EVALUATED",
        "parent_action": None,
        "request": detached(feasibility["request"]),
        "dwelling": dwelling,
        "household": household,
        "feasibility": feasibility,
        "read_boundary": {
            "psyche_store": "NOT_READ",
            "class_to_trait": "NOT_APPLIED",
            "model_prose": "NOT_READ",
        },
    }


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
    establish_household(session)
    establish_dwelling(session)


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
    if not branch_is_ancestor(session, house.get("branch"), house.get("epoch")):
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
