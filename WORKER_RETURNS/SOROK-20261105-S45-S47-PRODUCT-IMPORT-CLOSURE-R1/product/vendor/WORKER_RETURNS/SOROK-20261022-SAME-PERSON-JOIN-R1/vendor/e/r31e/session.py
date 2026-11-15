"""R31E first-neighbor session with actor-conditioned expression admission."""
from __future__ import annotations

from . import bootstrap

bootstrap.install()

from bp4.world import speech_event, offscreen_events, WorldRefusal  # noqa: E402
from r30a.first_session import (  # noqa: E402
    FirstSession,
    SessionRefusal,
    USER_ACTOR,
    GRADE as R30A_GRADE,
)
from r30a.phenomenal import compose  # noqa: E402

from . import expression  # noqa: E402

GRADE = "TEST_ONLY_SOURCEFREE_R31E_ACTOR_EXPRESSION_NOT_NATIVE"


class R31ESession(FirstSession):
    """R30A scene with a versioned actor-expression/admission port."""

    def status(self) -> dict:
        result = super().status()
        result["schema"] = "R31E_FIRST_NEIGHBOR_SESSION@1"
        result["grade"] = GRADE
        result["expression_port"] = expression.PORT_SCHEMA
        result["actor_model"] = "LIVE_ACTOR_MODEL_NOT_RUN"
        return result

    def custody(self) -> dict:
        result = super().custody()
        result["schema"] = "R31E_CUSTODY@1"
        result["grade"] = GRADE
        result["expression_port"] = {
            "schema": expression.PORT_SCHEMA,
            "version": 1,
            "contract_schema": expression.CONTRACT_SCHEMA,
            "admission_schema": expression.ADMISSION_SCHEMA,
            "live_actor_model": "LIVE_ACTOR_MODEL_NOT_RUN",
        }
        return result

    def _respond(self, kind: str, text: str = "", event_id: str = "") -> dict:
        result = expression.respond(self, trigger_kind=kind, text=text,
                                    event_id=event_id)
        self.last_expression = result
        return result

    def _surface(self, event_ids):
        return compose(self, event_ids,
                       attention=self.meta.get("attention", "focused"))

    def say(self, text: str) -> dict:
        self._require_scene()
        if not text.strip():
            raise SessionRefusal("EMPTY_SPEECH")
        world = self.world()
        event = speech_event(world, actor_id=USER_ACTOR, text=text.strip())
        self._append_event(event, perceive=(USER_ACTOR,))
        self._perceive_if_present(event, "A", "B")
        self.product._append_episode(
            self.branch_id, USER_ACTOR, "SAY", world.clock,
            {"attempted": True, "admitted": True,
             "event_id": event["event_id"], "action_seq": self._action_seq()})
        self.product._checkpoint(self.branch_id, world.clock, world)
        m6 = self._m6_ready("A", event["event_id"])
        if m6.get("state") != "READY":
            return {
                "status": "OK",
                "user_event": event,
                "strategy": "NO_ACTOR_PERCEPTION",
                "candidate": None,
                "admission": None,
                "surface": self._surface([event["event_id"]]),
            }
        result = self._respond("SAY", text.strip(), event["event_id"])
        surface = self._surface([event["event_id"]] + result["event_ids"])
        return {
            "status": "OK",
            "user_event": event,
            "strategy": result["candidate"]["strategy"],
            "candidate": result["candidate"],
            "admission": result["admission"],
            "contract_hash": result["contract"]["contract_hash"],
            "surface": surface,
        }

    def do_help(self) -> dict:
        self._require_scene()
        world = self.world()
        if world.positions.get("A") != world.positions.get(USER_ACTOR):
            raise SessionRefusal("NEIGHBOR_NOT_PRESENT")
        self.product._append_episode(
            self.branch_id, USER_ACTOR, "DO", world.clock,
            {"action": "offer_help", "attempted": True, "admitted": None,
             "action_seq": self._action_seq()})
        result = self._respond("DO_HELP")
        accepted = bool(result["admission"]["action_event_id"])
        return {
            "status": "OK",
            "accepted": accepted,
            "strategy": result["candidate"]["strategy"],
            "candidate": result["candidate"],
            "admission": result["admission"],
            "contract_hash": result["contract"]["contract_hash"],
            "surface": self._surface(result["event_ids"]),
        }

    def ask_contact(self) -> dict:
        self._require_scene()
        world = self.world()
        if world.positions.get("A") != world.positions.get(USER_ACTOR):
            raise SessionRefusal("NEIGHBOR_NOT_PRESENT")
        self.product._append_episode(
            self.branch_id, USER_ACTOR, "DO", world.clock,
            {"action": "ask_contact", "attempted": True, "admitted": None,
             "action_seq": self._action_seq()})
        result = self._respond("CONTACT")
        return {
            "status": "OK",
            "contact": result["candidate"]["contact"] == "GRANT",
            "outcome": result["candidate"]["contact"],
            "strategy": result["candidate"]["strategy"],
            "candidate": result["candidate"],
            "admission": result["admission"],
            "contract_hash": result["contract"]["contract_hash"],
            "surface": self._surface(result["event_ids"]),
        }

    def attend(self) -> dict:
        self._require_scene()
        world = self.world()
        state = self.product._runtime_state(self.branch_id)
        known = set(state["knowledge"].get(USER_ACTOR, []))
        position = world.positions.get(USER_ACTOR)
        new = []
        for event in world.events:
            if event["event_id"] in known:
                continue
            if event["location"] != position:
                continue
            if not (event.get("persistent") or event["clock"] == world.clock):
                continue
            self.product.store.record_perception(
                self.branch_id, actor_id=USER_ACTOR, event_id=event["event_id"],
                clock=event["clock"], channel="attend")
            new.append(event["event_id"])
        self.product._append_episode(
            self.branch_id, USER_ACTOR, "ATTEND", world.clock,
            {"attempted": True, "admitted": True, "new_knowledge": new,
             "changed": False, "action_seq": self._action_seq()})
        self.product._checkpoint(self.branch_id, world.clock, world)
        produced = []
        if (self.scene_open()
                and not any(row["kind"] in {"SAY", "INITIATE"}
                            for row in self.episodes("A"))):
            result = self._respond("INITIATE")
            produced = result["event_ids"]
        return {
            "status": "NO_CHANGE",
            "new_knowledge": new,
            "surface": self._surface(new + produced),
        }

    def wait(self, hours: int = 30) -> dict:
        self._require_scene()
        world = self.world()
        world.advance(world.clock + max(0, int(hours)))
        before_ids = {event["event_id"] for event in world.events}
        offscreen_events(world, actor_id="B")
        new_events = [event for event in world.events
                      if event["event_id"] not in before_ids]
        for event in new_events:
            self.product.store.append_world_event(self.branch_id, event)
            self.product.store.record_perception(
                self.branch_id, actor_id="B", event_id=event["event_id"],
                clock=event["clock"], channel="own_action")
            self._perceive_if_present(event, USER_ACTOR, "A")
            self.product._append_episode(
                self.branch_id, "B", "OFFSCREEN", event["clock"],
                {"event_id": event["event_id"],
                 "source_owned": bool(event.get("owner_receipt"))})
        self.product._append_episode(
            self.branch_id, USER_ACTOR, "WAIT", world.clock,
            {"attempted": True, "admitted": True,
             "hours": max(0, int(hours)), "changed": bool(new_events),
             "action_seq": self._action_seq()})
        self.product._checkpoint(self.branch_id, world.clock, world)
        produced = []
        if self.clock() >= 40 and self.scene_open():
            result = self._respond("DEPART")
            produced = result["event_ids"]
            self.product._append_episode(
                self.branch_id, USER_ACTOR, "SCENE_END", self.clock(),
                {"reason": "ACTOR_HAS_TO_LEAVE"})
        return {
            "status": "OK",
            "clock": world.clock,
            "scene_open": self.scene_open(),
            "surface": self._surface([e["event_id"] for e in new_events] + produced),
        }

    def advance_offscreen(self, hours: int = 30) -> dict:
        if self.scene_open():
            raise SessionRefusal("SCENE_OPEN__USE_WAIT")
        world = self.world()
        world.advance(world.clock + max(0, int(hours)))
        before = {event["event_id"] for event in world.events}
        offscreen_events(world, actor_id="B")
        new_events = [event for event in world.events
                      if event["event_id"] not in before]
        for event in new_events:
            self.product.store.append_world_event(self.branch_id, event)
            self.product.store.record_perception(
                self.branch_id, actor_id="B", event_id=event["event_id"],
                clock=event["clock"], channel="own_action")
            if world.positions.get("A") == event.get("location"):
                self.product.store.record_perception(
                    self.branch_id, actor_id="A", event_id=event["event_id"],
                    clock=event["clock"], channel="co_present")
            self.product._append_episode(
                self.branch_id, "B", "OFFSCREEN", event["clock"],
                {"event_id": event["event_id"],
                 "source_owned": bool(event.get("owner_receipt"))})
        self.product._append_episode(
            self.branch_id, USER_ACTOR, "OFFSCREEN", world.clock,
            {"hours": max(0, int(hours)), "outside_portal": True,
             "action_seq": self._action_seq()})
        self.product._checkpoint(self.branch_id, world.clock, world)
        message = None
        message_result = None
        if self.contact_status() and int(hours) >= 2:
            if int(world.actor_state["A"].get("free_hours", 0)) >= 1:
                message_result = self._respond("MESSAGE")
                message = message_result["candidate"]["speech"]
        return {
            "status": "OK",
            "clock": world.clock,
            "offscreen_events": [event["event_id"] for event in new_events],
            "message": message,
            "message_admission": message_result["admission"] if message_result else None,
        }

    def return_session(self) -> dict:
        if self.scene_open():
            return {"status": "NO_CHANGE", "scene_open": True,
                    "surface": ["You are already through the portal."]}
        world = self.world()
        self.product._append_episode(
            self.branch_id, USER_ACTOR, "RETURN", world.clock,
            {"location": world.positions.get(USER_ACTOR),
             "action_seq": self._action_seq()})
        self.product._checkpoint(self.branch_id, world.clock, world)
        result = self.product.attend(actor=USER_ACTOR)
        expression_result = self._respond("RETURN")
        ids = list(result.get("new_knowledge", [])) + expression_result["event_ids"]
        return {
            "status": "OK",
            "scene_open": True,
            "strategy": expression_result["candidate"]["strategy"],
            "candidate": expression_result["candidate"],
            "admission": expression_result["admission"],
            "surface": self._surface(ids),
        }
