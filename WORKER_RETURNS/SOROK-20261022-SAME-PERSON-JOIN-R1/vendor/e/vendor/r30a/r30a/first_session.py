"""R30A first-neighbor session over the immutable R29P C12/M6 product.

The user is a visitor U.  The neighbor is R29P actor A; actor B is A's
independent co-worker.  A/B state, the objective world, C12 facts and M6
perception are actual R29P code.  U is a product-shell actor added only to the
session branch; the original C12 root remains A/B.

Every user SAY/DO is a proposal recorded in C12.  Every admitted actor speech,
gesture or material action is written as a source-owned world event before it is
visible to the user.  The phenomenal compositor only selects among events U
actually perceived.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from . import bootstrap

bootstrap.install()

from bp1.canon import digest  # noqa: E402
from bp4.perception import render_requested_event  # noqa: E402
from bp4.world import (  # noqa: E402
    WorldRefusal,
    initial_world,
    inspect_event,
    make_event,
    offscreen_events,
    owner_receipt,
    repair_event,
    speech_event,
)
from r29p.product import R29PProduct  # noqa: E402
from r29p.runner import build_bundle  # noqa: E402

from .phenomenal import compose  # noqa: E402

SCHEMA = "R30A_FIRST_NEIGHBOR_SESSION@1"
BRANCH = "first_session"
GRADE = "TEST_ONLY_SOURCEFREE_R30A_FIRST_NEIGHBOR_PRODUCT_NOT_NATIVE"
USER_ACTOR = "U"


class SessionRefusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code
        self.detail = detail


def _public_role(state: dict, actor: str) -> str:
    return str(state.get("actor_state", {}).get(actor, {}).get("role", "neighbor"))


def _write_meta(state_root: Path, meta: dict) -> None:
    (state_root / "session.json").write_text(
        json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf8")


def _read_meta(state_root: Path) -> dict:
    path = state_root / "session.json"
    if not path.exists():
        raise SessionRefusal("SESSION_NOT_FOUND", str(path))
    return json.loads(path.read_text(encoding="utf8"))


class FirstSession:
    """A persistent user-facing session over one actual R29P product root."""

    def __init__(self, product: R29PProduct, state_root: Path, meta: dict):
        self.product = product
        self.state_root = Path(state_root)
        self.meta = meta
        self.branch_id = meta.get("branch_id", BRANCH)
        self.product.use(self.branch_id)

    # ------------------------------------------------------------------
    # construction / cold reopen
    # ------------------------------------------------------------------
    @classmethod
    def start(cls, state_root, *, scenario: str = "available",
              attention: str = "focused", variant: str = "A_REPAIR_LONG"):
        state_root = Path(state_root)
        state_root.mkdir(parents=True, exist_ok=True)
        if (state_root / "session.json").exists():
            raise SessionRefusal("SESSION_EXISTS__NO_AUTOMATIC_REROLL", str(state_root))
        if scenario not in {"available", "pressed"}:
            raise SessionRefusal("SCENARIO_UNKNOWN", scenario)
        product, artifacts, producer = build_bundle(state_root, variant=variant)
        producer.close()
        try:
            session = cls._attach_new(product, state_root, scenario=scenario,
                                      attention=attention, variant=variant)
            return session
        except Exception:
            product.close()
            raise

    @classmethod
    def _attach_new(cls, product: R29PProduct, state_root: Path, *,
                    scenario: str, attention: str, variant: str):
        store = product.store
        if store._branch(BRANCH) is None:
            store.fork("root", BRANCH)
        product.use(BRANCH)
        branch = store.branch(BRANCH)
        actors = sorted(set(branch["actor_ids"]) | {USER_ACTOR})
        if actors != branch["actor_ids"]:
            store.db.execute("UPDATE branch SET actor_ids=? WHERE branch_id=?",
                             (json.dumps(actors), BRANCH))
            store.db.commit()
        world = product._world(BRANCH)
        if scenario == "pressed":
            world.actor_state["A"] = dict(world.actor_state["A"])
            world.actor_state["A"]["free_hours"] = 0
        world.positions[USER_ACTOR] = "workshop"
        world.actor_state[USER_ACTOR] = {
            "role": "visitor",
            "actor_id": "TEST_ONLY_R30A_USER_U",
            "free_hours": 8,
            "material_remaining": 0,
            "tools_remaining": 0,
        }
        # A branch-local checkpoint before the user's arrival.
        product._checkpoint(BRANCH, world.clock, world)
        arrival = make_event(
            clock=world.clock,
            kind="ARRIVAL",
            actor_id=USER_ACTOR,
            location="workshop",
            summary="You come up the stairs and stop at the open workshop door.",
            body={"public_role": "visitor", "present_with": ["A", "B"]},
            sequence=len(world.events),
        )
        world.add_event(arrival)
        store.append_world_event(BRANCH, arrival)
        for actor in ("U", "A", "B"):
            store.record_perception(BRANCH, actor_id=actor,
                                    event_id=arrival["event_id"],
                                    clock=arrival["clock"], channel="co_present")
        for event in world.events:
            if event.get("kind") == "ARRIVAL" and event.get("actor_id") == "B":
                store.record_perception(BRANCH, actor_id=USER_ACTOR,
                                        event_id=event["event_id"],
                                        clock=event["clock"], channel="co_present")
        product._append_episode(BRANCH, USER_ACTOR, "ARRIVE", world.clock,
                                {"event_id": arrival["event_id"],
                                 "location": "workshop"})
        product._checkpoint(BRANCH, world.clock, world)
        meta = {
            "schema": SCHEMA,
            "grade": GRADE,
            "product_root": str(product.root),
            "state_root": str(state_root),
            "branch_id": BRANCH,
            "scenario": scenario,
            "attention": attention,
            "variant": variant,
            "r29p_source_ref": "001b506fa26ae879ff5b6e57138fc2696e12b538",
            "user_actor": USER_ACTOR,
        }
        _write_meta(state_root, meta)
        return cls(product, state_root, meta)

    @classmethod
    def open(cls, state_root, *, attention: str | None = None):
        state_root = Path(state_root)
        meta = _read_meta(state_root)
        if attention:
            meta["attention"] = attention
            _write_meta(state_root, meta)
        product = R29PProduct.reopen(Path(meta["product_root"]), branch_id="root")
        try:
            product.use(meta["branch_id"])
            session = cls(product, state_root, meta)
            verification = session.verify()
            if not verification.get("ok"):
                raise SessionRefusal(
                    "C12_VERIFY_FAILED", json.dumps(verification.get("errors", [])))
            return session
        except Exception:
            product.close()
            raise

    def close(self) -> None:
        self.product.close()

    # ------------------------------------------------------------------
    # public state
    # ------------------------------------------------------------------
    def world(self):
        return self.product._world(self.branch_id)

    def clock(self) -> int:
        return int(self.product.store.last_clock(self.branch_id))

    def episodes(self, actor: str | None = None):
        rows = self.product.store.episodes(self.branch_id)
        if actor is None:
            return rows
        return [row for row in rows if row["actor_id"] == actor]

    def events(self):
        return self.product.store.world_events(self.branch_id)

    def event(self, event_id: str):
        return self.product.store.world_event(self.branch_id, event_id)

    def user_perceived_ids(self) -> set[str]:
        return {row["event_id"] for row in
                self.product.store.perceptions(self.branch_id, USER_ACTOR)}

    def _last_user_kind(self):
        rows = self.episodes(USER_ACTOR)
        return rows[-1]["kind"] if rows else ""

    def _action_seq(self) -> int:
        return len(self.episodes()) + 1

    def scene_open(self) -> bool:
        terminal = [
            row for row in self.episodes(USER_ACTOR)
            if row["kind"] in {"ARRIVE", "RETURN", "LEAVE", "SCENE_END", "OFFSCREEN"}
        ]
        if not terminal:
            return False
        return terminal[-1]["kind"] in {"ARRIVE", "RETURN"}

    def contact_status(self) -> bool:
        rows = [row for row in self.episodes("A") if row["kind"] == "CONTACT"]
        return bool(rows and rows[-1]["body"].get("established") is True)

    def messages(self):
        rows = [
            row for row in self.episodes()
            if row["kind"] == "MESSAGE"
        ]
        return [
            {
                "seq": row["clock"],
                "sender": "you" if row["actor_id"] == USER_ACTOR else "neighbor",
                "text": row["body"].get("text", ""),
                "clock": row["clock"],
                "episode_id": row["episode_id"],
            }
            for row in rows
        ]

    def status(self) -> dict:
        world = self.world()
        present = [
            {
                "actor": actor,
                "public_role": _public_role(world.snapshot(), actor),
            }
            for actor in ("A", "B")
            if world.positions.get(actor) == world.positions.get(USER_ACTOR)
        ]
        return {
            "schema": SCHEMA,
            "grade": GRADE,
            "native": False,
            "clock": self.clock(),
            "location": world.positions.get(USER_ACTOR),
            "scene_open": self.scene_open(),
            "present": present,
            "contact": self.contact_status(),
            "messages": len(self.messages()),
            "attention": self.meta.get("attention", "focused"),
            "scenario": self.meta.get("scenario", "available"),
            "branch_id": self.branch_id,
        }

    def verify(self) -> dict:
        return self.product.c12_verify(self.branch_id)

    def custody(self) -> dict:
        source = self.product.joined_source()
        return {
            "schema": "R30A_CUSTODY@1",
            "grade": GRADE,
            "r29p_source_ref": self.meta.get("r29p_source_ref"),
            "branch_id": self.branch_id,
            "c12_path": str(self.product.store.path),
            "c12_verify": self.verify(),
            "source": source,
            "c12_counts": self.product.store.verify(self.branch_id)["counts"],
            "world_clock": self.clock(),
            "events": len(self.events()),
            "episodes": len(self.episodes()),
        }

    # ------------------------------------------------------------------
    # C12 / M6 helpers
    # ------------------------------------------------------------------
    def _m6_ready(self, actor: str, event_id: str):
        state = self.product._runtime_state(self.branch_id)
        events = self.events()
        return render_requested_event(actor, self.clock(), state, events, event_id)

    def _append_event(self, event: dict, *, perceive: tuple[str, ...] = ()) -> dict:
        self.product.store.append_world_event(self.branch_id, event)
        for actor in perceive:
            self.product.store.record_perception(
                self.branch_id, actor_id=actor, event_id=event["event_id"],
                clock=event["clock"], channel="co_present")
        return event

    def _perceive_if_present(self, event: dict, *actors: str) -> None:
        world = self.world()
        for actor in actors:
            if actor == event.get("actor_id") or (
                    world.positions.get(actor) == event.get("location")):
                self.product.store.record_perception(
                    self.branch_id, actor_id=actor, event_id=event["event_id"],
                    clock=event["clock"], channel="co_present")

    def _actor_say(self, actor: str, text: str, *, gesture: str = "",
                   tone: str = "", episode_kind: str = "SAY") -> dict:
        world = self.world()
        event = make_event(
            clock=world.clock, kind="SPEECH", actor_id=actor,
            location=world.positions.get(actor, "workshop"),
            summary=f"{actor} says: {text}",
            body={"text": text, "gesture": gesture, "tone": tone,
                  "public_role": _public_role(world.snapshot(), actor)},
            sequence=len(world.events),
        )
        world.add_event(event)
        self._append_event(event, perceive=(actor,))
        self._perceive_if_present(event, USER_ACTOR, "A", "B")
        self.product._append_episode(
            self.branch_id, actor, episode_kind, world.clock,
            {"event_id": event["event_id"], "text": text,
             "gesture": gesture, "tone": tone})
        self.product._checkpoint(self.branch_id, world.clock, world)
        return event

    def _maybe_actor_initiates(self) -> list[dict]:
        if not self.scene_open():
            return []
        if any(row["kind"] in {"INITIATE", "SAY"} for row in self.episodes("A")):
            return []
        world = self.world()
        if world.positions.get("A") != world.positions.get(USER_ACTOR):
            return []
        state_a = world.actor_state.get("A", {})
        if int(state_a.get("free_hours", 0)) < 1:
            return []
        event = self._actor_say(
            "A",
            "You're looking at the seam. Can you see the gap?",
            gesture="A tilts the piece toward you.",
            tone="ordinary",
            episode_kind="INITIATE",
        )
        return [event]

    # ------------------------------------------------------------------
    # user actions
    # ------------------------------------------------------------------
    def _require_scene(self):
        if not self.scene_open():
            raise SessionRefusal("SCENE_CLOSED__USE_RETURN")

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
        event_id = event["event_id"]
        produced = []
        a_sees = self._m6_ready("A", event_id)
        b_sees = self._m6_ready("B", event_id)
        text_l = text.strip().lower()
        if a_sees.get("state") == "READY":
            if any(word in text_l for word in ("stupid", "shut up", "idiot")):
                produced.append(self._actor_say(
                    "A", "Then we're done here.",
                    gesture="A turns back to the bench.", tone="flat"))
                self.product._append_episode(
                    self.branch_id, USER_ACTOR, "SCENE_END", self.clock(),
                    {"reason": "ACTOR_WITHDREW"})
            elif any(word in text_l for word in ("help", "hand", "hold", "need")):
                a_state = world.actor_state["A"]
                can_take = (
                    int(a_state.get("free_hours", 0)) >= 1
                    and int(a_state.get("material_remaining", 0)) >= 1
                    and int(a_state.get("tools_remaining", 0)) >= 1
                    and a_state.get("availability_status") == "available_for_encounter"
                )
                produced.append(self._actor_say(
                    "A",
                    ("If you're offering, the near edge needs a hand."
                     if can_take else "I can't take that on now. I have to finish."),
                    gesture=("A keeps one hand on the bench."
                             if can_take else "A keeps both hands on the piece."),
                    tone="practical" if can_take else "firm"))
            elif any(word in text_l for word in ("new", "moved", "moving", "landing")):
                produced.append(self._actor_say(
                    "A", "Which side of the landing?",
                    gesture="A glances toward the doorway.",
                    tone="ordinary"))
            elif any(word in text_l for word in ("what", "work", "doing", "repair", "seam")):
                produced.append(self._actor_say(
                    "A", "A repair I said I'd finish. The tool's still on the bench.",
                    gesture="A taps the bench once.",
                    tone="ordinary"))
            elif any(word in text_l for word in ("number", "contact", "call", "message")):
                produced.append(self._actor_say(
                    "A", "Ask me before the shift ends. Not while I'm holding this.",
                    gesture="A shifts the piece in their hands.",
                    tone="guarded"))
            elif any(word in text_l for word in ("finisher", " b ", "other")):
                produced.append(self._actor_say(
                    "A", "The finisher. We share the bench, not the schedule.",
                    gesture="A does not look toward B.",
                    tone="dry"))
            elif text_l.endswith("?") or text_l.startswith(("hello", "hi", "hey")):
                produced.append(self._actor_say(
                    "A", "You're new on this landing.",
                    gesture="A looks up briefly.",
                    tone="neutral"))
            elif int(world.actor_state["A"].get("free_hours", 0)) < 1:
                produced.append(self._actor_say(
                    "A", "I can't stop. The market closes.",
                    gesture="A keeps working.",
                    tone="brisk"))
            else:
                produced.append(self._actor_say(
                    "A", "You can stay if you want. Mind the shavings.",
                    gesture="A nods at the floor.",
                    tone="ordinary"))
        if b_sees.get("state") == "READY" and any(
                word in text_l for word in ("finisher", " b ", "market", "pieces")):
            produced.append(self._actor_say(
                "B", "Market's still open.",
                gesture="B does not look up from the pieces.",
                tone="indifferent"))
        return {
            "status": "OK",
            "user_event": self.event(event_id),
            "actor_events": produced,
            "surface": compose(self, [event_id] + [e["event_id"] for e in produced],
                               attention=self.meta.get("attention", "focused")),
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
        a_state = world.actor_state["A"]
        available = (
            int(a_state.get("free_hours", 0)) >= 1
            and int(a_state.get("material_remaining", 0)) >= 1
            and int(a_state.get("tools_remaining", 0)) >= 1
            and a_state.get("availability_status") == "available_for_encounter"
        )
        produced = []
        if not available:
            produced.append(self._actor_say(
                "A", "I can't take that on now. I have to finish.",
                gesture="A keeps both hands on the piece.",
                tone="firm"))
            self.product._append_episode(
                self.branch_id, "A", "REFUSAL", world.clock,
                {"action": "refuse_help", "reason": "NO_CAPACITY",
                 "user_proposal": True, "action_seq": self._action_seq()})
        else:
            receipt = owner_receipt(
                act="REPAIR", actor_id="A", clock=world.clock,
                location=world.positions["A"])
            event = repair_event(world, actor_id="A", receipt=receipt)
            self._append_event(event, perceive=("A",))
            self._perceive_if_present(event, USER_ACTOR, "B")
            self.product._append_episode(
                self.branch_id, "A", "DO", world.clock,
                {"action": "repair", "admitted": True,
                 "event_id": event["event_id"], "user_proposal": True,
                 "action_seq": self._action_seq()})
            produced.append(event)
            produced.append(self._actor_say(
                "A", "Hold the near edge. I'll check the seam.",
                gesture="A sets the tool beside your hand.",
                tone="practical"))
            self.product._checkpoint(self.branch_id, world.clock, world)
        return {
            "status": "OK",
            "accepted": available,
            "actor_events": produced,
            "surface": compose(self, [e["event_id"] for e in produced],
                               attention=self.meta.get("attention", "focused")),
        }

    def inspect(self) -> dict:
        self._require_scene()
        world = self.world()
        event = inspect_event(world, actor_id=USER_ACTOR)
        self._append_event(event, perceive=(USER_ACTOR,))
        self._perceive_if_present(event, "A", "B")
        self.product._append_episode(
            self.branch_id, USER_ACTOR, "DO", world.clock,
            {"action": "inspect", "admitted": True,
             "event_id": event["event_id"], "changed": False,
             "action_seq": self._action_seq()})
        self.product._checkpoint(self.branch_id, world.clock, world)
        return {
            "status": "NO_CHANGE",
            "surface": compose(self, [event["event_id"]],
                               attention=self.meta.get("attention", "focused")),
        }

    def travel(self, location: str) -> dict:
        self._require_scene()
        world = self.world()
        try:
            world.move(USER_ACTOR, location)
        except WorldRefusal as exc:
            raise SessionRefusal(exc.code) from exc
        event = world.events[-1]
        self._append_event(event, perceive=(USER_ACTOR,))
        self.product._append_episode(
            self.branch_id, USER_ACTOR, "DO", world.clock,
            {"action": "travel", "admitted": True,
             "event_id": event["event_id"], "to": location,
             "action_seq": self._action_seq()})
        self.product._checkpoint(self.branch_id, world.clock, world)
        return {
            "status": "OK",
            "surface": compose(self, [event["event_id"]],
                               attention=self.meta.get("attention", "focused")),
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
        produced = self._maybe_actor_initiates()
        ids = new + [e["event_id"] for e in produced]
        return {
            "status": "NO_CHANGE",
            "new_knowledge": new,
            "surface": compose(self, ids, attention=self.meta.get("attention", "focused")),
        }

    def wait(self, hours: int = 30) -> dict:
        self._require_scene()
        world = self.world()
        target = world.clock + max(0, int(hours))
        world.advance(target)
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
        result = {"clock": world.clock,
                  "offscreen_events": [event["event_id"] for event in new_events]}
        produced = []
        if self.clock() >= 40 and self.scene_open():
            if int(world.actor_state["A"].get("free_hours", 0)) < 1:
                produced.append(self._actor_say(
                    "A", "I have to go. The market closes.",
                    gesture="A takes the tool and steps toward the door.",
                    tone="brisk"))
            else:
                produced.append(self._actor_say(
                    "A", "I need to get this to the market before the light goes.",
                    gesture="A begins packing the bench.",
                    tone="ordinary"))
            self.product._append_episode(
                self.branch_id, USER_ACTOR, "SCENE_END", self.clock(),
                {"reason": "ACTOR_HAS_TO_LEAVE"})
        ids = list(result.get("offscreen_events", [])) + [e["event_id"] for e in produced]
        return {
            "status": "OK",
            "clock": result.get("clock"),
            "scene_open": self.scene_open(),
            "surface": compose(self, ids, attention=self.meta.get("attention", "focused")),
        }

    def leave(self) -> dict:
        if not self.scene_open():
            return {"status": "NO_CHANGE", "scene_open": False}
        world = self.world()
        self.product._append_episode(
            self.branch_id, USER_ACTOR, "LEAVE", world.clock,
            {"reason": "USER_LEFT_PORTAL", "action_seq": self._action_seq()})
        self.product._checkpoint(self.branch_id, world.clock, world)
        return {"status": "OK", "scene_open": False,
                "surface": ["You step back through the portal. The workshop continues without you."]}

    def ask_contact(self) -> dict:
        self._require_scene()
        world = self.world()
        if world.positions.get("A") != world.positions.get(USER_ACTOR):
            raise SessionRefusal("NEIGHBOR_NOT_PRESENT")
        self.product._append_episode(
            self.branch_id, USER_ACTOR, "DO", world.clock,
            {"action": "ask_contact", "attempted": True, "admitted": None,
             "action_seq": self._action_seq()})
        repaired = any(row["actor_id"] == "A" and row["kind"] == "DO"
                       and row["body"].get("action") == "repair"
                       for row in self.episodes())
        a_speech = [row for row in self.episodes("A") if row["kind"] == "SAY"]
        available = int(world.actor_state["A"].get("free_hours", 0)) >= 1
        established = bool(available and (repaired or len(a_speech) >= 2))
        text = ("All right. The landing line is enough."
                if established else "Not yet. I don't know you.")
        gesture = ("A wipes their hands and gives the number."
                   if established else "A keeps working.")
        produced = [self._actor_say("A", text, gesture=gesture,
                                    tone="ordinary" if established else "guarded")]
        self.product._append_episode(
            self.branch_id, "A", "CONTACT", world.clock,
            {"established": established, "channel": "landing_line" if established else "",
             "user_proposal": True, "speech_event_id": produced[0]["event_id"],
             "action_seq": self._action_seq()})
        self.product._append_episode(
            self.branch_id, USER_ACTOR, "CONTACT", world.clock,
            {"established": established, "channel": "landing_line" if established else "",
             "action_seq": self._action_seq()})
        self.product._checkpoint(self.branch_id, world.clock, world)
        return {
            "status": "OK",
            "contact": established,
            "surface": compose(self, [e["event_id"] for e in produced],
                               attention=self.meta.get("attention", "focused")),
        }

    # ------------------------------------------------------------------
    # outside-portal channel
    # ------------------------------------------------------------------
    def send_message(self, text: str) -> dict:
        if self.scene_open():
            raise SessionRefusal("SCENE_OPEN__USE_SAY")
        if not self.contact_status():
            raise SessionRefusal("NO_CONTACT_CHANNEL")
        if not text.strip():
            raise SessionRefusal("EMPTY_MESSAGE")
        world = self.world()
        self.product._append_episode(
            self.branch_id, USER_ACTOR, "MESSAGE", world.clock,
            {"text": text.strip(), "direction": "to_neighbor",
             "channel": "landing_line", "action_seq": self._action_seq()})
        return {"status": "SENT", "text": text.strip()}

    def advance_offscreen(self, hours: int = 30) -> dict:
        if self.scene_open():
            raise SessionRefusal("SCENE_OPEN__USE_WAIT")
        world = self.world()
        world.advance(world.clock + max(0, int(hours)))
        before = {event["event_id"] for event in world.events}
        produced = offscreen_events(world, actor_id="B")
        new_events = [event for event in world.events if event["event_id"] not in before]
        for event in new_events:
            self.product.store.append_world_event(self.branch_id, event)
            self.product.store.record_perception(
                self.branch_id, actor_id="B", event_id=event["event_id"],
                clock=event["clock"], channel="own_action")
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
        if self.contact_status() and int(hours) >= 2:
            a_state = world.actor_state["A"]
            if int(a_state.get("free_hours", 0)) >= 1:
                repaired = any(row["actor_id"] == "A" and row["kind"] == "DO"
                               and row["body"].get("action") == "repair"
                               for row in self.episodes())
                text = ("The seam held. I'm at the market until six."
                        if repaired else
                        "The bench is clear. The finisher took the pieces to market.")
                message = self.product._append_episode(
                    self.branch_id, "A", "MESSAGE", world.clock,
                    {"text": text, "direction": "to_user",
                     "channel": "landing_line", "action_seq": self._action_seq()})
        return {
            "status": "OK",
            "clock": world.clock,
            "offscreen_events": [event["event_id"] for event in new_events],
            "message": message["body"]["text"] if message else None,
        }

    def check_messages(self) -> dict:
        return {
            "contact": self.contact_status(),
            "messages": self.messages(),
            "status": "OK" if self.contact_status() else "NO_CHANNEL",
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
        produced = self._actor_return_greeting()
        produced += self._maybe_actor_initiates()
        ids = list(result.get("new_knowledge", [])) + [e["event_id"] for e in produced]
        return {
            "status": "OK",
            "scene_open": True,
            "surface": compose(self, ids, attention=self.meta.get("attention", "focused")),
        }

    def _actor_return_greeting(self) -> list[dict]:
        world = self.world()
        if world.positions.get("A") != world.positions.get(USER_ACTOR):
            return []
        repaired = any(row["actor_id"] == "A" and row["kind"] == "DO"
                       and row["body"].get("action") == "repair"
                       for row in self.episodes())
        text = "The seam held. You came back." if repaired else "You came back."
        gesture = ("A lifts the finished piece an inch off the bench."
                   if repaired else "A looks up from the bench.")
        return [self._actor_say("A", text, gesture=gesture, tone="ordinary")]

    def fork_alt(self) -> dict:
        result = self.product.fork("alt")
        return {"status": "OK", "fork": result,
                "shared_root": result.get("shared_root")}
