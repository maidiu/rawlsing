"""Sourcefree objective world state and owner-sourced world events (TEST_ONLY).

The world clock, positions, resources and events are separate from any actor's
perception or history. A world event requires an explicit owner receipt; a
narrated intention, a user sentence or an actor's self-attestation is not an
event. This is a TEST_ONLY world, not native Pyat N11/N12.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any

from .canon import assert_no_forbidden, digest, seal, valid

WORLD_OWNER = "TEST_ONLY_BP4_WORLD_OWNER"
WORLD_GRADE = "TEST_ONLY_SOURCEFREE_WORLD_NOT_NATIVE"
WORLD_SCHEMA = "BP4_OBJECTIVE_WORLD@1"
EVENT_SCHEMA = "BP4_WORLD_EVENT@1"
RECEIPT_SCHEMA = "BP4_WORLD_OWNER_RECEIPT@1"

LOCATIONS = ("workshop", "market")


class WorldRefusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


def owner_receipt(*, act: str, actor_id: str, clock: int, location: str) -> dict:
    body = {
        "schema": RECEIPT_SCHEMA,
        "owner_ref": WORLD_OWNER,
        "act": act,
        "actor_id": actor_id,
        "clock": clock,
        "location": location,
        "performed": True,
        "grade": WORLD_GRADE,
        "native": False,
    }
    return seal(body)


def validate_owner_receipt(receipt: Any, *, actor_id: str, act: str, clock: int | None = None) -> dict:
    if not isinstance(receipt, dict) or not valid(receipt):
        raise WorldRefusal("WORLD_OWNER_RECEIPT_UNSEALED")
    if receipt.get("owner_ref") != WORLD_OWNER:
        raise WorldRefusal("WORLD_OWNER_NOT_RECOGNIZED", str(receipt.get("owner_ref")))
    if receipt.get("performed") is not True:
        raise WorldRefusal("WORLD_ACTION_NOT_PERFORMED")
    if receipt.get("actor_id") != actor_id:
        raise WorldRefusal("WORLD_ACTION_ACTOR_MISMATCH")
    if receipt.get("act") != act:
        raise WorldRefusal("WORLD_ACTION_ACT_MISMATCH")
    if clock is not None and receipt.get("clock") != clock:
        raise WorldRefusal("WORLD_ACTION_CLOCK_MISMATCH")
    if receipt.get("native") is not False:
        raise WorldRefusal("WORLD_ACTION_FALSE_NATIVE_GRANT")
    return receipt


def make_event(*, clock: int, kind: str, actor_id: str, location: str,
               summary: str, body: dict, receipt: dict | None = None,
               persistent: bool = False, sequence: int = 0) -> dict:
    if kind not in {"ARRIVAL", "MOVE", "SPEECH", "INSPECT", "REPAIR", "NO_CHANGE",
                    "OFFSCREEN_REPAIR", "OFFSCREEN_NO_CHANGE", "REFUSAL", "ATTEND"}:
        raise WorldRefusal("UNKNOWN_WORLD_EVENT_KIND", kind)
    if receipt is not None:
        validate_owner_receipt(receipt, actor_id=actor_id, act=kind, clock=clock)
    base = {
        "schema": EVENT_SCHEMA,
        "clock": int(clock),
        "kind": kind,
        "actor_id": actor_id,
        "location": location,
        "summary": summary,
        "body": body,
        "owner_receipt": receipt,
        "persistent": bool(persistent),
        "sequence": int(sequence),
        "grade": WORLD_GRADE,
        "native": False,
    }
    assert_no_forbidden(base)
    event_id = "TEST_ONLY_BP4_WORLD_EVT_" + digest(base)
    event = {"event_id": event_id, **base}
    event["hash"] = digest(event)
    return event


@dataclass
class WorldState:
    clock: int = 10
    positions: dict[str, str] = field(default_factory=dict)
    actor_state: dict[str, dict] = field(default_factory=dict)
    resources: dict[str, dict] = field(default_factory=dict)
    events: list[dict] = field(default_factory=list)
    offscreen_done: bool = False
    schema: str = WORLD_SCHEMA
    owner: str = WORLD_OWNER
    grade: str = WORLD_GRADE
    native: bool = False

    def add_event(self, event: dict) -> dict:
        if event["clock"] < self.clock - 1 and not event.get("persistent"):
            raise WorldRefusal("RETROACTIVE_WORLD_EVENT")
        if any(existing["event_id"] == event["event_id"] for existing in self.events):
            raise WorldRefusal("DUPLICATE_WORLD_EVENT")
        self.events.append(deepcopy(event))
        self.clock = max(self.clock, event["clock"])
        return event

    def advance(self, to_clock: int) -> None:
        if to_clock < self.clock:
            raise WorldRefusal("WORLD_CLOCK_REVERSED")
        self.clock = int(to_clock)

    def move(self, actor_id: str, location: str) -> None:
        if location not in LOCATIONS:
            raise WorldRefusal("WORLD_LOCATION_UNKNOWN")
        if self.positions.get(actor_id) == location:
            raise WorldRefusal("ALREADY_AT_LOCATION")
        self.positions[actor_id] = location
        self.add_event(make_event(
            clock=self.clock, kind="MOVE", actor_id=actor_id, location=location,
            summary=f"{actor_id} moves to {location}.", body={"to": location},
            sequence=len(self.events),
        ))

    def snapshot(self) -> dict:
        data = {
            "schema": self.schema,
            "clock": self.clock,
            "positions": deepcopy(self.positions),
            "actor_state": deepcopy(self.actor_state),
            "resources": deepcopy(self.resources),
            "events": deepcopy(self.events),
            "offscreen_done": self.offscreen_done,
            "owner": self.owner,
            "grade": self.grade,
            "native": self.native,
        }
        data["hash"] = digest(data)
        return data

    @classmethod
    def restore(cls, data: dict) -> "WorldState":
        if not isinstance(data, dict) or data.get("schema") != WORLD_SCHEMA:
            raise WorldRefusal("WORLD_SNAPSHOT_INVALID")
        body = {k: v for k, v in data.items() if k != "hash"}
        if digest(body) != data.get("hash"):
            raise WorldRefusal("WORLD_SNAPSHOT_HASH_MISMATCH")
        world = cls(
            clock=int(data["clock"]),
            positions=deepcopy(data["positions"]),
            actor_state=deepcopy(data["actor_state"]),
            resources=deepcopy(data["resources"]),
            events=deepcopy(data["events"]),
            offscreen_done=bool(data["offscreen_done"]),
        )
        return world


def initial_world(life) -> WorldState:
    world = WorldState(
        clock=10,
        positions={"A": "workshop", "B": "workshop"},
        actor_state={
            "A": deepcopy(life.a_snapshot["state"]),
            "B": deepcopy(life.b_snapshot["state"]),
        },
        resources={"workshop": {"tool_available": True, "material": 2},
                   "market": {"material": 0}},
    )
    arrival = make_event(
        clock=10, kind="ARRIVAL", actor_id="B", location="workshop",
        summary="The finishing worker is already at the workshop bench.",
        body={"public_role": "finishing", "present_with": ["A"]},
    )
    world.add_event(arrival)
    return world


def offscreen_events(world: WorldState, *, actor_id: str) -> list[dict]:
    """One source-owned offscreen life event at clock 40, no user input required."""
    if world.offscreen_done or world.clock < 40:
        return []
    world.offscreen_done = True
    if world.positions.get(actor_id) == "workshop":
        world.positions[actor_id] = "market"
        world.add_event(make_event(
            clock=40, kind="MOVE", actor_id=actor_id, location="market",
            summary="The finishing worker takes the completed pieces to the market.",
            body={"to": "market"}, sequence=len(world.events),
        ))
    if world.resources["workshop"].get("tool_available"):
        receipt = owner_receipt(act="OFFSCREEN_REPAIR", actor_id=actor_id,
                                clock=40, location="market")
        state = world.actor_state[actor_id]
        state["completed_units"] = int(state.get("completed_units", 0)) + 1
        state["cash"] = int(state.get("cash", 0)) + 2
        state["material_remaining"] = max(0, int(state.get("material_remaining", 0)) - 1)
        event = make_event(
            clock=40, kind="OFFSCREEN_REPAIR", actor_id=actor_id, location="market",
            summary="A market stall is refurbished while the user is away.",
            body={"completed_delta": 1, "cash_delta": 2, "material_delta": -1,
                  "tool_used": True, "source_owned": True},
            receipt=receipt, persistent=True, sequence=len(world.events),
        )
    else:
        receipt = owner_receipt(act="OFFSCREEN_NO_CHANGE", actor_id=actor_id,
                                clock=40, location="market")
        event = make_event(
            clock=40, kind="OFFSCREEN_NO_CHANGE", actor_id=actor_id, location="market",
            summary="The finishing worker cannot complete the stall: the tool is gone.",
            body={"reason": "NO_TOOL", "completed_delta": 0},
            receipt=receipt, persistent=True, sequence=len(world.events),
        )
    world.add_event(event)
    world.clock = max(world.clock, 40)
    return [event]


def repair_event(world: WorldState, *, actor_id: str, receipt: dict) -> dict:
    state = world.actor_state[actor_id]
    if int(state.get("material_remaining", 0)) < 1:
        raise WorldRefusal("MATERIAL_EXHAUSTED")
    if int(state.get("free_hours", 0)) < 1:
        raise WorldRefusal("NO_FREE_HOURS")
    event = make_event(
        clock=world.clock, kind="REPAIR", actor_id=actor_id,
        location=world.positions[actor_id],
        summary="A material repair is performed in the workshop.",
        body={"completed_delta": 1, "cash_delta": 2, "material_delta": -1,
              "hours_delta": -1, "source_owned": True},
        receipt=receipt, sequence=len(world.events),
    )
    state["completed_units"] = int(state.get("completed_units", 0)) + 1
    state["cash"] = int(state.get("cash", 0)) + 2
    state["material_remaining"] = int(state.get("material_remaining", 0)) - 1
    state["free_hours"] = int(state.get("free_hours", 0)) - 1
    world.add_event(event)
    return event


def speech_event(world: WorldState, *, actor_id: str, text: str) -> dict:
    if not text.strip():
        raise WorldRefusal("EMPTY_SPEECH")
    event = make_event(
        clock=world.clock, kind="SPEECH", actor_id=actor_id,
        location=world.positions[actor_id],
        summary=f"{actor_id} says: {text.strip()}",
        body={"text": text.strip(), "observable": True},
        sequence=len(world.events),
    )
    world.add_event(event)
    return event


def inspect_event(world: WorldState, *, actor_id: str) -> dict:
    event = make_event(
        clock=world.clock, kind="INSPECT", actor_id=actor_id,
        location=world.positions[actor_id],
        summary="The actor inspects the present material but changes nothing.",
        body={"changed": False}, sequence=len(world.events),
    )
    world.add_event(event)
    return event
