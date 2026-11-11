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

from .canon import assert_no_forbidden, canonical, digest, seal, valid

WORLD_OWNER = "TEST_ONLY_BP4_WORLD_OWNER"
WORLD_GRADE = "TEST_ONLY_SOURCEFREE_WORLD_NOT_NATIVE"
WORLD_SCHEMA = "BP4_OBJECTIVE_WORLD@1"
EVENT_SCHEMA = "BP4_WORLD_EVENT@1"
RECEIPT_SCHEMA = "BP4_WORLD_OWNER_RECEIPT@1"

LOCATIONS = ("workshop", "market")
HISTORY_POLICY_SLOT = "test_only.material_history_policy.v1"


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
                    "OFFSCREEN_REPAIR", "OFFSCREEN_NO_CHANGE", "REFUSAL", "ATTEND",
                    "PLAY_INSTRUMENT", "STOP_INSTRUMENT", "APPROACH", "ORIENT",
                    "HISTORICAL_MATERIAL"}:
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

    def configure_experimental_history(self, *, root: str, branch: str,
                                       source_event_ref: dict, target_ids: list[str],
                                       entities: list[dict], earliest: int) -> dict:
        """Trusted sourcefree scene initialization, never a model permission.

        This is an explicitly experimental BP4 policy. It cannot issue a native
        world, actor-state, memory, belief, or shared-root write capability.
        No such policy is installed by the ordinary P4/P6 entry points.
        """
        if self.native or self.owner != WORLD_OWNER or self.grade != WORLD_GRADE:
            raise WorldRefusal("H1_OWNER_NOT_GRANTED")
        source = next((e for e in self.events
                       if e["event_id"] == source_event_ref.get("object_id")
                       and e["hash"] == source_event_ref.get("content_hash")), None)
        if (source is None or source_event_ref.get("kind") != "WORLD_EVENT"
                or source.get("kind") not in {"ARRIVAL", "MOVE", "REPAIR", "OFFSCREEN_REPAIR"}
                or type(earliest) is not int or earliest < source["clock"]
                or earliest > self.clock or not root or not branch
                or not target_ids or len(set(target_ids)) != len(target_ids)
                or len(target_ids) > 8):
            raise WorldRefusal("H1_SOURCE_POLICY_INVALID")
        allowed_entities = []
        for entity in entities:
            ref, record = entity.get("ref", {}), entity.get("record", {})
            if (set(entity) != {"ref", "record"}
                    or set(ref) != {"kind", "object_id", "content_hash"}
                    or ref["kind"] not in {"INSTITUTION", "MATERIAL_ACTIVITY", "PLACE"}
                    or not ref["object_id"] or ref["content_hash"] != digest(record)
                    or record.get("object_id") != ref["object_id"]
                    or record.get("kind") != ref["kind"]
                    or record.get("evidence_class") != "SOURCEFREE_SYNTHETIC"
                    or record.get("source_event_ref") != source_event_ref):
                raise WorldRefusal("H1_SOURCE_ENTITY_INVALID")
            if ref["kind"] == "PLACE" and record.get("location") not in (
                    set(self.positions.values()) | set(self.resources) | set(LOCATIONS)):
                raise WorldRefusal("H1_PLACE_SOURCE_NOT_GRANTED")
            allowed_entities.append(deepcopy(entity))
        body = {"schema": "BP4_EXPERIMENTAL_MATERIAL_HISTORY_POLICY@1",
                "owner": WORLD_OWNER, "grade": WORLD_GRADE, "native": False,
                "root": root, "branch": branch, "source_event_ref": source_event_ref,
                "target_ids": sorted(target_ids), "entities": allowed_entities,
                "window": [earliest, self.clock], "allowed_H_classes": ["H0", "H1"],
                "actor_effects": False, "shared_root_write": False,
                "historical_support_rule": "NOT_AFTER_EFFECTIVE_TIME"}
        policy = seal(body)
        registry = self.resources.get(HISTORY_POLICY_SLOT, {})
        if registry.get("schema") == body["schema"]:
            registry = {registry["hash"]: registry}
        registry = deepcopy(registry)
        registry[policy["hash"]] = policy
        self.resources[HISTORY_POLICY_SLOT] = registry
        return deepcopy(policy)

    def material_history_policy(self, *, root: str, branch: str, policy_hash=None) -> dict:
        registry = self.resources.get(HISTORY_POLICY_SLOT, {})
        if registry.get("schema") == "BP4_EXPERIMENTAL_MATERIAL_HISTORY_POLICY@1":
            registry = {registry["hash"]: registry}
        if policy_hash is None and len(registry) == 1:
            policy_hash = next(iter(registry))
        policy = registry.get(policy_hash)
        if (self.native or not isinstance(policy, dict) or not valid(policy)
                or policy.get("owner") != WORLD_OWNER or policy.get("native") is not False
                or policy.get("grade") != WORLD_GRADE or policy.get("root") != root
                or policy.get("branch") != branch or policy.get("actor_effects") is not False
                or policy.get("shared_root_write") is not False):
            raise WorldRefusal("H1_OWNER_NOT_GRANTED")
        parent = policy["source_event_ref"]
        if not any(e["event_id"] == parent["object_id"] and e["hash"] == parent["content_hash"]
                   for e in self.events):
            raise WorldRefusal("H1_POLICY_PARENT_MISSING")
        return deepcopy(policy)

    @staticmethod
    def material_history_effective_time(event):
        # Canonical material episodes are appended now but describe a separately
        # admitted past time. Their admission clock is not their causal date.
        stamp = (event.get("body", {}).get("effective_time")
                 if event.get("kind") == "HISTORICAL_MATERIAL" else event.get("clock"))
        return stamp if type(stamp) is int and stamp <= event["clock"] else None

    def admit_material_history(self, *, root: str, branch: str, policy_hash: str,
                                occurrence: dict, dependency_refs: list[dict]) -> dict:
        """Admit an objective experimental episode through this world owner.

        The event is appended at admission time; its distinct effective time
        never rewrites an earlier world checkpoint or grants actor perception.
        Current material/actor effects are not accepted by this bounded writer.
        """
        policy = self.material_history_policy(root=root, branch=branch, policy_hash=policy_hash)
        if policy["hash"] != policy_hash:
            raise WorldRefusal("H1_POLICY_CHANGED")
        allowed = {"ref", "kind", "dependency_group", "group_id", "asserted_H_class",
                   "effective_time", "place_ref", "actor_refs", "target_ids", "action",
                   "effects", "causal_parents", "source_refs", "participants"}
        if set(occurrence) - allowed or occurrence.get("asserted_H_class") != "H1":
            raise WorldRefusal("H1_UNSUPPORTED_EFFECT_OR_FIELD")
        effective = occurrence.get("effective_time")
        targets = occurrence.get("target_ids", [])
        if (type(effective) is not int or not policy["window"][0] <= effective <= policy["window"][1]
                or not targets or not set(targets) <= set(policy["target_ids"])
                or occurrence.get("effects") not in (None, [], {})):
            raise WorldRefusal("H1_CHRONOLOGY_OR_EFFECT_NOT_GRANTED")
        if occurrence.get("action") not in {"PRODUCTION", "ACQUISITION", "REPAIR",
                                            "USE", "TRANSFER", "MATERIAL_LABOR"}:
            raise WorldRefusal("H1_ACTION_NOT_GRANTED")
        actor_refs = occurrence.get("actor_refs", [])
        for actor in actor_refs:
            actor_id = actor.get("object_id")
            expected = {"kind": "ACTOR", "object_id": actor_id,
                        "content_hash": digest({"root": root, "actor_id": actor_id})}
            if actor != expected or actor_id not in {
                    row.get("actor_id") for row in self.actor_state.values()}:
                raise WorldRefusal("H1_ACTOR_SOURCE_NOT_GRANTED")
        source = policy["source_event_ref"]
        parents = occurrence.get("causal_parents", [])
        if not parents or not all(any(e["event_id"] == p.get("object_id")
                                      and e["hash"] == p.get("content_hash")
                                      and self.material_history_effective_time(e) is not None
                                      and self.material_history_effective_time(e) <= effective
                                      for e in self.events)
                                  for p in parents):
            raise WorldRefusal("H1_CAUSAL_PARENT_NOT_GRANTED")
        # This experimental ABI treats source_refs as historical support, not
        # retrospective testimony. Present appearance remains binding packet
        # context/readset, but cannot masquerade as earlier support evidence.
        for ref in occurrence.get("source_refs", []):
            actual = next((event for event in self.events
                           if event["event_id"] == ref.get("object_id")
                           and event["hash"] == ref.get("content_hash")), None)
            if (ref.get("kind") != "WORLD_EVENT" or actual is None
                    or actual["kind"] not in {"ARRIVAL", "MOVE", "APPROACH", "REPAIR",
                                              "OFFSCREEN_REPAIR", "HISTORICAL_MATERIAL"}):
                raise WorldRefusal("H1_SOURCE_NOT_GRANTED")
            stamp = self.material_history_effective_time(actual)
            if stamp is None or stamp > effective:
                raise WorldRefusal("H1_SOURCE_AFTER_EFFECTIVE_TIME")
        entities = {canonical(e["ref"]) for e in policy["entities"]}
        places = {canonical(e["ref"]) for e in policy["entities"] if e["ref"]["kind"] == "PLACE"}
        if canonical(occurrence.get("place_ref")) not in places:
            raise WorldRefusal("H1_PLACE_SOURCE_NOT_GRANTED")
        place = next(e["record"]["location"] for e in policy["entities"]
                     if e["ref"] == occurrence["place_ref"])
        for actor in actor_refs:
            alias = next(alias for alias, row in self.actor_state.items()
                         if row.get("actor_id") == actor["object_id"])
            positions = [event for event in self.events
                         if event["actor_id"] == alias and event["clock"] <= effective
                         and event["kind"] in {"ARRIVAL", "MOVE", "APPROACH"}]
            if not positions:
                raise WorldRefusal("H1_ACTOR_LOCATION_NOT_ESTABLISHED")
            position = max(positions, key=lambda e: (e["clock"], e.get("sequence", 0)))
            if position["location"] != place:
                raise WorldRefusal("H1_ACTOR_LOCATION_CONFLICT")
            if any(event["actor_id"] == alias and event["clock"] == effective
                   and event["kind"] != "HISTORICAL_MATERIAL" for event in self.events):
                raise WorldRefusal("H1_CLOSED_ACTOR_EVENT_OVERLAP")
        principals = {canonical(e) for e in actor_refs}
        for role in occurrence.get("participants", []):
            if (set(role) != {"role", "ref"} or role["role"] not in {
                    "PRODUCER", "RECIPIENT", "REPAIRER", "LABOR_PARTICIPANT",
                    "INSTITUTION", "MATERIAL_ACTIVITY"}
                    or canonical(role["ref"]) not in entities | principals
                    or (role["ref"].get("kind") !=
                        (role["role"] if role["role"] in {"INSTITUTION", "MATERIAL_ACTIVITY"}
                         else "ACTOR"))):
                raise WorldRefusal("H1_PARTICIPANT_NOT_GRANTED")
        body = {"history_schema": "BP4_EXPERIMENTAL_MATERIAL_EPISODE@1",
                "root": root, "branch": branch, "policy_hash": policy_hash,
                "source_event_ref": source, "proposal": deepcopy(occurrence),
                "dependency_refs": deepcopy(dependency_refs),
                "effective_time": effective, "source_owned": True,
                "actor_access": "NOT_GRANTED", "user_access": "NOT_GRANTED"}
        existing = next((e for e in self.events if e["kind"] == "HISTORICAL_MATERIAL"
                         and e["body"] == body), None)
        if existing is not None:
            return deepcopy(existing)
        actor_id = next((alias for alias, row in self.actor_state.items()
                         if actor_refs and row.get("actor_id") == actor_refs[0]["object_id"]),
                        WORLD_OWNER)
        event = make_event(clock=self.clock, kind="HISTORICAL_MATERIAL", actor_id=actor_id,
                           location="HISTORICAL_SOURCE_SCOPE",
                           summary="An objective material episode is admitted.", body=body,
                           receipt=owner_receipt(act="HISTORICAL_MATERIAL", actor_id=actor_id,
                                                 clock=self.clock, location="HISTORICAL_SOURCE_SCOPE"),
                           sequence=len(self.events))
        self.add_event(event)
        return deepcopy(event)

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
