"""A3-A5 sourcefree multicontact life scenario over I1's guarded product.

The scenario does not invent a personality. It records performed material
inspection activity, an independently sourced coactor's request, a test-only
custody transition, and B's independent market commission. Every change is a
sealed C12 world event or a real BP4 action; A5 only reads the result.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from bp4.canon import digest
from bp4.world import WorldState

from .events import make_cp_event

GRADE = "TEST_ONLY_SOURCEFREE_CP_A5_LIFE_NOT_NATIVE"
SCENARIO_SCHEMA = "SOROK_CP_A5_SCENARIO_TRACE@1"
COACTOR_C = {
    "actor_id": "TEST_ONLY_CP_A5_ACTOR_C",
    "source_ref": "TEST_ONLY_CP_A5_COACTOR_SOURCE_C",
    "source_grade": "TEST_ONLY_SOURCEFREE_COACTOR",
    "snapshot": {
        "role": "carrier",
        "cash": 41,
        "material_remaining": 1,
        "free_hours": 8,
        "completed_units": 0,
        "position": "workshop",
    },
    "native": False,
}
COACTOR_C["source_hash"] = digest(COACTOR_C)
COACTOR_C["snapshot_hash"] = digest(COACTOR_C["snapshot"])

CUSTODY_RULE_NAME = "cp_a5.test_only.cross_context_material_custody"
CUSTODY_RULE = {
    "name": CUSTODY_RULE_NAME,
    "minimum_inspections": 3,
    "minimum_contexts": 2,
    "decision": "RETAIN_TOOL",
    "grade": "TEST_ONLY_SOURCEFREE_TRANSITION_RULE",
    "native": False,
}
CUSTODY_RULE["hash"] = digest(CUSTODY_RULE)


@dataclass
class CPLife:
    """Build and record one multi-context A3-A5 life on a guarded product."""

    product: Any
    include_b_activity: bool = True
    grant_a_access: bool = True
    custody_rule: bool = True
    context_profile: str = "cross_context"
    root: Path = field(default_factory=Path)
    trace: dict = field(default_factory=dict)

    @property
    def branch(self) -> str:
        return self.product.branch_id

    def _world(self) -> WorldState:
        return self.product._world(self.branch)

    def _append(self, *, clock: int, kind: str, actor_id: str, location: str,
                summary: str, body: dict, mutate=None) -> dict:
        world = self._world()
        world.advance(clock)
        sequence = len(world.events)
        event = make_cp_event(
            clock=clock, kind=kind, actor_id=actor_id, location=location,
            summary=summary, body=body, sequence=sequence)
        world.add_event(event)
        self.product.store.append_world_event(self.branch, event)
        if mutate is not None:
            mutate(world)
        for observer in ("A", "B"):
            if world.positions.get(observer) == location:
                if not (observer == "A" and not self.grant_a_access
                        and kind in {"B_TAKE_TOOL", "B_RETURN_TOOL",
                                     "B_MARKET_COMMISSION"}):
                    self.product.store.record_perception(
                        self.branch, actor_id=observer,
                        event_id=event["event_id"], clock=clock,
                        channel="co_present")
        self.product._checkpoint(self.branch, clock, world)
        return event

    def _inspection_rounds(self) -> list[dict]:
        events = []
        if self.context_profile == "single_context":
            for wait in (5, 5):
                self.product.wait(wait)
                events.append(self.product.inspect())
            return events
        events.append(self.product.inspect())
        self.product.wait(5)
        self.product.travel("market")
        events.append(self.product.inspect())
        self.product.wait(5)
        self.product.travel("workshop")
        events.append(self.product.inspect())
        self.product.wait(5)
        return events

    def _custody_evidence(self) -> dict:
        events = [e for e in self.product.store.world_events(self.branch)
                  if e.get("actor_id") == "A" and e.get("kind") == "INSPECT"]
        contexts = sorted({e.get("location") for e in events})
        return {
            "inspection_count": len(events),
            "contexts": contexts,
            "event_ids": [e["event_id"] for e in events],
            "qualified": len(events) >= 3 and len(contexts) >= 2,
        }

    def _decide_custody(self, request: dict) -> dict:
        evidence = self._custody_evidence()
        if not self.custody_rule:
            return self._append(
                clock=62, kind="A4_CUSTODY_HELD", actor_id="A",
                location="workshop",
                summary="The custody request is held: no test-only transition rule.",
                body={"state": "HELD", "code": "MISSING_CUSTODY_RULE",
                      "request_id": request["event_id"],
                      "evidence": evidence})
        if not evidence["qualified"]:
            return self._append(
                clock=62, kind="A4_CUSTODY_HELD", actor_id="A",
                location="workshop",
                summary="The custody request is held: inspection evidence is insufficient.",
                body={"state": "HELD", "code": "INSUFFICIENT_EVIDENCE",
                      "request_id": request["event_id"],
                      "evidence": evidence})
        return self._append(
            clock=62, kind="A4_CUSTODY_DECISION", actor_id="A",
            location="workshop",
            summary="A retains the workshop tool after cross-context inspection.",
            body={"state": "DECIDED", "decision": "RETAIN_TOOL",
                  "rule": CUSTODY_RULE_NAME, "rule_hash": CUSTODY_RULE["hash"],
                  "request_id": request["event_id"],
                  "evidence": evidence})

    def _attempt_repair(self, clock: int, label: str) -> dict:
        world = self._world()
        if world.clock < clock:
            self.product.wait(clock - world.clock)
            world = self._world()
        if not world.resources.get("workshop", {}).get("tool_available"):
            return self._append(
                clock=clock, kind="A_REPAIR_BLOCKED", actor_id="A",
                location="workshop",
                summary="A cannot repair: the workshop tool is away.",
                body={"reason": "TOOL_UNAVAILABLE", "attempt": label})
        result = self.product.repair()
        return {"result": result, "event_id": result.get("event_id")}

    def run(self) -> dict:
        self.product.wait(30)  # I1's source-owned B market event at clock 40
        inspections = self._inspection_rounds()

        # C is a separately sourced coactor with its own resource snapshot.
        # C acts at the workshop; A perceives only the public request/withdrawal.
        self._append(
            clock=60, kind="C_ARRIVE", actor_id="C", location="workshop",
            summary="A carrier arrives at the workshop with a separate source.",
            body={"coactor_source": COACTOR_C,
                  "public_state": {"position": "workshop"}})
        request = self._append(
            clock=60, kind="C_TOOL_REQUEST", actor_id="C", location="workshop",
            summary="The carrier asks A to borrow the workshop tool.",
            body={"coactor_source": COACTOR_C,
                  "request": "borrow_workshop_tool",
                  "relation": "REQUESTED"})
        decision = self._decide_custody(request)
        self._append(
            clock=65, kind="C_WITHDRAW", actor_id="C", location="workshop",
            summary="The carrier withdraws the request and leaves the workshop.",
            body={"coactor_source": COACTOR_C,
                  "relation": "REQUEST_UNMET",
                  "request_id": request["event_id"]})
        self._append(
            clock=66, kind="C_LEAVE", actor_id="C", location="workshop",
            summary="The carrier leaves for the market.",
            body={"coactor_source": COACTOR_C, "to": "market"})

        if self.include_b_activity:
            self._append(
                clock=68, kind="B_RETURN_WORKSHOP", actor_id="B",
                location="workshop",
                summary="B returns to the workshop before the next market commission.",
                body={"source_ref": self.product.artifacts.life.b_source.source_ref,
                      "source_hash": self.product.artifacts.life.b_source.source_hash},
                mutate=lambda world: world.positions.__setitem__("B", "workshop"))
            self._append(
                clock=70, kind="B_TAKE_TOOL", actor_id="B", location="workshop",
                summary="B independently takes the workshop tool for a market commission.",
                body={"source_owned": True, "tool_used": True},
                mutate=lambda world: world.resources["workshop"].__setitem__(
                    "tool_available", False))
            self._append(
                clock=72, kind="B_GO_MARKET", actor_id="B", location="market",
                summary="B carries the tool to the market.",
                body={"to": "market"},
                mutate=lambda world: world.positions.__setitem__("B", "market"))
            def _commission(world: WorldState) -> None:
                state = world.actor_state["B"]
                state["completed_units"] = int(state.get("completed_units", 0)) + 1
                state["cash"] = int(state.get("cash", 0)) + 2
            self._append(
                clock=75, kind="B_MARKET_COMMISSION", actor_id="B",
                location="market",
                summary="B completes an independent market commission with the tool.",
                body={"source_owned": True, "tool_used": True,
                      "completed_delta": 1, "cash_delta": 2,
                      "material_delta": 0},
                mutate=_commission)
            self._append(
                clock=80, kind="A_REPAIR_BLOCKED", actor_id="A",
                location="workshop",
                summary="A cannot repair while B's commission holds the tool.",
                body={"reason": "TOOL_UNAVAILABLE", "attempt": "after_b_take"})
            self._append(
                clock=90, kind="B_RETURN_TOOL", actor_id="B",
                location="workshop",
                summary="B returns the tool to the workshop.",
                body={"source_owned": True, "tool_returned": True},
                mutate=lambda world: (
                    world.positions.__setitem__("B", "workshop"),
                    world.resources["workshop"].__setitem__(
                        "tool_available", True)))
        # The later repair is a real BP4 action; B's tool return makes it possible.
        repaired = self._attempt_repair(100, "after_b_return")

        state = self.product.store.latest_state(self.branch)
        events = self.product.store.world_events(self.branch)
        self.trace = {
            "schema": SCENARIO_SCHEMA,
            "grade": GRADE,
            "native": False,
            "branch": self.branch,
            "actor": "A",
            "coactor_c": COACTOR_C,
            "custody_rule": CUSTODY_RULE,
            "inspections": inspections,
            "inspection_evidence": self._custody_evidence(),
            "decision_event": decision["event_id"],
            "decision_body": decision["body"],
            "repair_after_return": repaired,
            "clock": state["world"]["clock"],
            "tool_available": state["world"]["resources"]["workshop"]["tool_available"],
            "actors": {actor: dict(state["actors"][actor]["state"])
                       for actor in ("A", "B")},
            "event_ids": {
                kind: [event["event_id"] for event in events if event["kind"] == kind]
                for kind in sorted({event["kind"] for event in events})
            },
            "event_count": len(events),
            "known_a_event_ids": [p["event_id"] for p in
                                  self.product.store.perceptions(self.branch, "A")],
        }
        return self.trace


def build_cp_life(root, artifacts, *, include_b_activity: bool = True,
                  grant_a_access: bool = True, custody_rule: bool = True,
                  context_profile: str = "cross_context") -> tuple:
    """Create a fresh guarded product and run the CP-A5 scenario."""
    from bp2p4.i1_product import GuardedJoinedProduct

    product = GuardedJoinedProduct(Path(root), artifacts=artifacts)
    life = CPLife(product, include_b_activity=include_b_activity,
                  grant_a_access=grant_a_access, custody_rule=custody_rule,
                  context_profile=context_profile, root=Path(root))
    try:
        trace = life.run()
    finally:
        product.close()
    return life, trace
