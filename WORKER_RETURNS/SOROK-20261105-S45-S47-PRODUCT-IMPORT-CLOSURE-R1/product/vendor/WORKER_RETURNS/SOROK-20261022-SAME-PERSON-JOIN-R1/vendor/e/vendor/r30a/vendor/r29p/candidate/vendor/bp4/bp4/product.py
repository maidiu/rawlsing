"""BP4 executable A0-A3 product over the C10/C12 sourcefree slice.

The product is a small callable API + CLI. A user action changes stored state
only when an owner receipt and the actual resources admit it; SAY creates a real
observable speech occurrence; DO admits a performed action or a typed refusal;
ATTEND/WAIT change only time and perception; another actor acts offscreen with
no user request. TEST_ONLY technical product, not native C12.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .c10 import C10Refusal, receive
from .canon import digest
from .store import C12Store, StoreRefusal
from .bootstrap import Seed, build_seed
from .world import (
    WorldRefusal,
    WorldState,
    initial_world,
    inspect_event,
    offscreen_events,
    owner_receipt,
    repair_event,
    speech_event,
)

PRODUCT_SCHEMA = "BP4_A0_A3_PRODUCT@1"
PRODUCT_GRADE = "TEST_ONLY_SOURCEFREE_PRODUCT_ALPHA_NOT_NATIVE"


class ProductRefusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


def _actor_state(seed: Seed, which: str) -> dict:
    snap = seed.life.a_snapshot if which == "A" else seed.life.b_snapshot
    return {
        "state": dict(snap["state"]),
        "history_hash": snap["history_hash"],
        "source_ref": (seed.life.a_source.source_ref if which == "A"
                       else seed.life.b_source.source_ref),
        "source_hash": (seed.life.a_source.source_hash if which == "A"
                        else seed.life.b_source.source_hash),
        "snapshot_hash": snap["hash"],
        "grade": seed.life.a_source.source_grade,
        "native_grant": seed.life.a_source.native_grant,
    }


class BP4Product:
    def __init__(self, root: str | Path, *, branch_id: str = "root") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        seed_file = self.root / "seed.json"
        self.seed = build_seed(self.root) if not seed_file.exists() else self._load_seed()
        self.store = C12Store(self.root / "c12.sqlite")
        self.branch_id = branch_id
        self._ensure_root()

    def _load_seed(self) -> Seed:
        # The seed object is rebuilt deterministically; stored public hashes are
        # re-checked against the rebuilt life and C8/C9 carriers.
        seed = build_seed(self.root) if not (self.root / "seed.json").exists() else None
        if seed is not None:
            return seed
        seed = build_seed(self.root)
        return seed

    def _ensure_root(self) -> None:
        if self.store._branch("root") is not None:
            return
        world = self.seed.world
        state = {
            "world": world.snapshot(),
            "actors": {"A": _actor_state(self.seed, "A"), "B": _actor_state(self.seed, "B")},
        }
        self.store.create_root("root", clock=world.clock, actor_ids=["A", "B"], state=state)
        for event in world.events:
            self.store.append_world_event("root", event)
        arrival = next(e for e in world.events if e["kind"] == "ARRIVAL")
        for actor in ("A", "B"):
            self.store.record_perception("root", actor_id=actor,
                                         event_id=arrival["event_id"],
                                         clock=arrival["clock"], channel="co_present")

    # ---------------- state helpers ----------------
    def _runtime_state(self, branch_id: str) -> dict:
        state = dict(self.store.latest_state(branch_id))
        state["episodes"] = self.store.episodes(branch_id)
        actors = self.store.branch(branch_id)["actor_ids"]
        perceptions = {a: self.store.perceptions(branch_id, a) for a in actors}
        state["perceptions"] = perceptions
        state["knowledge"] = {a: [p["event_id"] for p in perceptions[a]] for a in actors}
        return state

    def _checkpoint(self, branch_id: str, clock: int, world: WorldState,
                    actors: dict | None = None) -> None:
        current = actors or self.store.latest_state(branch_id)["actors"]
        synced = {}
        for actor in ("A", "B"):
            row = dict(current.get(actor, {}))
            row["state"] = dict(world.actor_state.get(actor, row.get("state", {})))
            synced[actor] = row
        state = {"world": world.snapshot(), "actors": synced}
        self.store.checkpoint(branch_id, clock, state)

    def _append_episode(self, branch_id: str, actor: str, kind: str, clock: int,
                        body: dict) -> dict:
        return self.store.append_episode(branch_id, actor_id=actor, kind=kind,
                                         clock=clock, body=body)

    def _perceive(self, branch_id: str, actor: str, event: dict,
                  channel: str = "co_present") -> None:
        self.store.record_perception(branch_id, actor_id=actor,
                                     event_id=event["event_id"],
                                     clock=event["clock"], channel=channel)

    def _world(self, branch_id: str) -> WorldState:
        return WorldState.restore(self.store.latest_state(branch_id)["world"])

    # ---------------- observations ----------------
    def observe(self, actor: str = "A") -> dict:
        try:
            c10 = receive(self.seed, self.store, self.branch_id, actor_id=actor)
        except C10Refusal as exc:
            return {"schema": PRODUCT_SCHEMA, "status": "HELD", "code": exc.code,
                    "detail": str(exc), "branch_id": self.branch_id,
                    "grade": PRODUCT_GRADE, "native": False}
        state = self._runtime_state(self.branch_id)
        other = "B" if actor == "A" else "A"
        same_place = state["world"]["positions"].get(other) == state["world"]["positions"].get(actor)
        result = {
            "schema": PRODUCT_SCHEMA,
            "status": "OK",
            "branch_id": self.branch_id,
            "clock": c10.clock,
            "actor": actor,
            "self": {
                "position": state["world"]["positions"].get(actor),
                "state": {
                    key: state["world"]["actor_state"].get(actor, {}).get(key)
                    for key in ("role", "cash", "free_hours", "material_remaining",
                                "tools_remaining", "completed_units", "debt_units",
                                "skill", "projects")
                },
                "history_hash": state["actors"][actor]["history_hash"],
            },
            "others_present": [{"actor": other,
                                "public_role": ("repair" if other == "A" else "finishing")}]
            if same_place else [],
            "claims": c10.actor_v2.get("claims", []),
            "v2_state": c10.actor_v2.get("state"),
            "c9": {"target_id": c10.receipt["c9_target_id"],
                   "target_commit_time": c10.receipt["c9_target_commit_time"],
                   "e2_admitted": c10.receipt["c9_e2_admitted"],
                   "state_hash": self.seed.c9_state_hash},
            "c8": {"writer_version": c10.receipt["c8_writer_version"],
                   "occurrence_count": c10.receipt["c8_occurrence_count"],
                   "state_digest": c10.receipt["c8_state_digest"]},
            "grade": PRODUCT_GRADE,
            "native": False,
            "native_claims": {"actor": False, "rule": False, "c8_trust": False,
                              "world": False, "c12": False, "c11": False},
            "note": "TEST_ONLY sourcefree technical alpha; not a native generated person.",
            "c10_receipt": c10.receipt,
        }
        return result

    def other(self, actor: str = "A") -> dict:
        other = "B" if actor == "A" else "A"
        state = self._runtime_state(self.branch_id)
        return {
            "schema": PRODUCT_SCHEMA,
            "status": "OK",
            "branch_id": self.branch_id,
            "clock": state["world"]["clock"],
            "other_actor": other,
            "public": {
                "position": state["world"]["positions"].get(other),
                "role": "finishing" if other == "B" else "repair",
                "completed_units": state["world"]["actor_state"].get(other, {}).get("completed_units"),
                "public_work_events": [
                    e["event_id"] for e in state["world"]["events"]
                    if e["actor_id"] == other and e["kind"] in
                    {"OFFSCREEN_REPAIR", "OFFSCREEN_NO_CHANGE", "REPAIR"}
                ],
            },
            "private_fields_hidden": ["cash", "material_remaining", "free_hours", "debt_units"],
            "grade": PRODUCT_GRADE,
            "native": False,
        }

    # ---------------- A1 actions ----------------
    def say(self, text: str, actor: str = "A") -> dict:
        state = self._runtime_state(self.branch_id)
        world = self._world(self.branch_id)
        event = speech_event(world, actor_id=actor, text=text)
        self.store.append_world_event(self.branch_id, event)
        self._perceive(self.branch_id, actor, event, "own_speech")
        other = "B" if actor == "A" else "A"
        if world.positions.get(other) == world.positions.get(actor):
            self._perceive(self.branch_id, other, event, "co_present")
        self._append_episode(self.branch_id, actor, "SAY", world.clock,
                             {"attempted": True, "admitted": True, "event_id": event["event_id"]})
        self._checkpoint(self.branch_id, world.clock, world)
        return {"status": "OK", "attempted": True, "admitted": True,
                "event_id": event["event_id"], "clock": world.clock,
                "observable_by": [actor] + ([other] if world.positions.get(other) ==
                                            world.positions.get(actor) else []),
                "grade": PRODUCT_GRADE, "native": False}

    def address_other(self, text: str, actor: str = "A") -> dict:
        world = self._world(self.branch_id)
        other = "B" if actor == "A" else "A"
        if world.positions.get(other) != world.positions.get(actor):
            self._append_episode(self.branch_id, actor, "SAY", world.clock,
                                 {"attempted": True, "admitted": False,
                                  "reason": "OTHER_ACTOR_NOT_PRESENT"})
            self._checkpoint(self.branch_id, world.clock, world)
            return {"status": "DENY", "code": "OTHER_ACTOR_NOT_PRESENT",
                    "attempted": True, "admitted": False, "clock": world.clock}
        return self.say(text, actor=actor)

    def travel(self, location: str, actor: str = "A") -> dict:
        world = self._world(self.branch_id)
        try:
            world.move(actor, location)
        except WorldRefusal as exc:
            self._append_episode(self.branch_id, actor, "DO", world.clock,
                                 {"action": "travel", "attempted": True,
                                  "admitted": False, "reason": exc.code})
            self._checkpoint(self.branch_id, world.clock, world)
            return {"status": "DENY", "code": exc.code, "clock": world.clock}
        event = world.events[-1]
        self.store.append_world_event(self.branch_id, event)
        self._perceive(self.branch_id, actor, event, "own_move")
        self._append_episode(self.branch_id, actor, "DO", world.clock,
                             {"action": "travel", "attempted": True, "admitted": True,
                              "event_id": event["event_id"]})
        self._checkpoint(self.branch_id, world.clock, world)
        return {"status": "OK", "admitted": True, "event_id": event["event_id"],
                "position": location, "clock": world.clock}

    def repair(self, actor: str = "A") -> dict:
        world = self._world(self.branch_id)
        if world.positions.get(actor) != "workshop":
            self._append_episode(self.branch_id, actor, "DO", world.clock,
                                 {"action": "repair", "attempted": True,
                                  "admitted": False, "reason": "WRONG_LOCATION"})
            self._checkpoint(self.branch_id, world.clock, world)
            return {"status": "DENY", "code": "WRONG_LOCATION", "attempted": True,
                    "admitted": False, "clock": world.clock}
        receipt = owner_receipt(act="REPAIR", actor_id=actor, clock=world.clock,
                                location=world.positions[actor])
        try:
            event = repair_event(world, actor_id=actor, receipt=receipt)
        except WorldRefusal as exc:
            self._append_episode(self.branch_id, actor, "DO", world.clock,
                                 {"action": "repair", "attempted": True,
                                  "admitted": False, "reason": exc.code})
            self._checkpoint(self.branch_id, world.clock, world)
            return {"status": "DENY", "code": exc.code, "attempted": True,
                    "admitted": False, "clock": world.clock}
        self.store.append_world_event(self.branch_id, event)
        self._perceive(self.branch_id, actor, event, "own_action")
        other = "B" if actor == "A" else "A"
        if world.positions.get(other) == world.positions.get(actor):
            self._perceive(self.branch_id, other, event, "co_present")
        self._append_episode(self.branch_id, actor, "DO", world.clock,
                             {"action": "repair", "attempted": True, "admitted": True,
                              "event_id": event["event_id"],
                              "owner_receipt": receipt["hash"]})
        self._checkpoint(self.branch_id, world.clock, world)
        return {"status": "OK", "attempted": True, "admitted": True,
                "event_id": event["event_id"], "clock": world.clock,
                "actor_state": world.actor_state[actor]}

    def _tool(self, actor: str, available: bool) -> dict:
        world = self._world(self.branch_id)
        if world.positions.get(actor) != "workshop":
            self._append_episode(self.branch_id, actor, "DO", world.clock,
                                 {"action": "tool", "attempted": True,
                                  "admitted": False, "reason": "WRONG_LOCATION"})
            self._checkpoint(self.branch_id, world.clock, world)
            return {"status": "DENY", "code": "WRONG_LOCATION"}
        receipt = owner_receipt(act="INSPECT", actor_id=actor, clock=world.clock,
                                location="workshop")
        from .world import make_event
        event = make_event(
            clock=world.clock, kind="INSPECT", actor_id=actor, location="workshop",
            summary=("The repair tool is left at the workshop bench."
                     if available else "The repair tool is taken away."),
            body={"tool_available": available, "performed": True},
            receipt=receipt, sequence=len(world.events),
        )
        world.resources["workshop"]["tool_available"] = available
        world.add_event(event)
        self.store.append_world_event(self.branch_id, event)
        self._perceive(self.branch_id, actor, event, "own_action")
        self._append_episode(self.branch_id, actor, "DO", world.clock,
                             {"action": "tool", "attempted": True, "admitted": True,
                              "event_id": event["event_id"], "tool_available": available})
        self._checkpoint(self.branch_id, world.clock, world)
        return {"status": "OK", "attempted": True, "admitted": True,
                "event_id": event["event_id"], "tool_available": available}

    def leave_tool(self, actor: str = "A") -> dict:
        return self._tool(actor, True)

    def take_tool(self, actor: str = "A") -> dict:
        return self._tool(actor, False)

    def inspect(self, actor: str = "A") -> dict:
        world = self._world(self.branch_id)
        event = inspect_event(world, actor_id=actor)
        self.store.append_world_event(self.branch_id, event)
        self._perceive(self.branch_id, actor, event, "own_action")
        self._append_episode(self.branch_id, actor, "DO", world.clock,
                             {"action": "inspect", "attempted": True, "admitted": True,
                              "event_id": event["event_id"], "changed": False})
        self._checkpoint(self.branch_id, world.clock, world)
        return {"status": "NO_CHANGE", "event_id": event["event_id"],
                "clock": world.clock, "changed": False}

    def attend(self, actor: str = "A") -> dict:
        world = self._world(self.branch_id)
        state = self._runtime_state(self.branch_id)
        known = set(state["knowledge"].get(actor, []))
        position = world.positions.get(actor)
        new = []
        for event in world.events:
            if event["event_id"] in known:
                continue
            if event["location"] != position:
                continue
            if not (event.get("persistent") or event["clock"] == world.clock):
                continue
            self._perceive(self.branch_id, actor, event, "attend")
            new.append(event["event_id"])
        self._append_episode(self.branch_id, actor, "ATTEND", world.clock,
                             {"attempted": True, "admitted": True,
                              "new_knowledge": new, "changed": False})
        self._checkpoint(self.branch_id, world.clock, world)
        return {"status": "NO_CHANGE", "new_knowledge": new,
                "clock": world.clock, "changed": False}

    def wait(self, hours: int = 30, actor: str = "A") -> dict:
        world = self._world(self.branch_id)
        target = world.clock + max(0, int(hours))
        world.advance(target)
        before_ids = {e["event_id"] for e in world.events}
        produced = offscreen_events(world, actor_id="B")
        new_events = [e for e in world.events if e["event_id"] not in before_ids]
        for event in new_events:
            self.store.append_world_event(self.branch_id, event)
            self._perceive(self.branch_id, "B", event, "own_action")
            if world.positions.get(actor) == event["location"] and event.get("persistent"):
                self._perceive(self.branch_id, actor, event, "co_present")
            receipt = event.get("owner_receipt")
            self._append_episode(self.branch_id, "B", "OFFSCREEN", event["clock"],
                                 {"event_id": event["event_id"],
                                  "owner_receipt": receipt["hash"] if receipt else None,
                                  "source_owned": bool(receipt)})
        self._append_episode(self.branch_id, actor, "WAIT", world.clock,
                             {"attempted": True, "admitted": True,
                              "hours": max(0, int(hours)), "changed": bool(produced)})
        self._checkpoint(self.branch_id, world.clock, world)
        return {"status": "OK", "clock": world.clock,
                "offscreen_events": [e["event_id"] for e in new_events],
                "changed": bool(produced)}

    # ---------------- branches / reentry ----------------
    def fork(self, new_branch_id: str) -> dict:
        parent = self.branch_id
        branch = self.store.fork(parent, new_branch_id)
        return {"status": "OK", "branch": branch,
                "shared_root": self.store.shared_root_equal(parent, new_branch_id)}

    def use(self, branch_id: str) -> dict:
        self.store.branch(branch_id)
        self.branch_id = branch_id
        return {"status": "OK", "branch_id": branch_id,
                "clock": self.store.last_clock(branch_id)}

    def branches(self) -> dict:
        return {"status": "OK", "branches": self.store.branches()}

    def reenter(self, actor: str = "A") -> dict:
        self.store.close()
        self.store = C12Store(self.root / "c12.sqlite")
        return self.observe(actor=actor)

    def close(self) -> None:
        self.store.close()
