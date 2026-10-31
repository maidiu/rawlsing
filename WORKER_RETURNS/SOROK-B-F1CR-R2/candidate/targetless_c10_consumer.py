"""Sourcefree targetless C10 continuing-history adapter over R5 F1C TEST_ONLY B.

The adapter consumes R5's exact original F1C history/material intervention
candidate. It does not issue a native B, actor, Rule A/T, practice, utterance or
C9/C10 authority. REFUSE, SILENCE, no proposal, HELD, UNOBSERVED and evaluated
NO_CHANGE are distinct sourcefree states.
"""
from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Mapping

SCHEMA = "SOROK_B_F1CR_R2_TARGETLESS_C10_CONTINUITY@1"
MATERIAL_SCHEMA = "SOROK_B_F1CR_R2_MATERIAL_LEDGER@1"
GRADE = "TEST_ONLY_SOURCEFREE_B_HISTORY_AND_TARGETLESS_C10_NOT_NATIVE"

TARGETLESS_STATES = {
    "TARGETLESS_REFUSE",
    "TARGETLESS_SILENCE",
    "TARGETLESS_NO_PROPOSAL",
    "TARGETLESS_UNOBSERVED",
    "EVALUATED_NO_CHANGE",
    "HELD_MISSING_RULE",
}
SHARE_STATES = {"SHARE_OBSERVED", "SHARE_UNOBSERVED"}


class ContinuityRefusal(AssertionError):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def require(condition: Any, code: str) -> None:
    if not condition:
        raise ContinuityRefusal(code)


def digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False, default=str).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True)
class MaterialLedger:
    """Exact material/time ledger with no clamp path."""

    schema: str
    state: str
    stock_before: int
    replenished: int
    consumed: int
    stock_after: int
    hours_before: int
    hours_after: int
    events: tuple[Mapping[str, Any], ...]
    receipt: Mapping[str, Any]

    def __post_init__(self) -> None:
        require(self.schema == MATERIAL_SCHEMA, "MATERIAL_SCHEMA")
        require(self.state in {"MATERIAL_BALANCED", "REFUSED_MATERIAL_EXHAUSTED"},
                "MATERIAL_STATE")
        require(all(isinstance(x, int) and not isinstance(x, bool) for x in (
            self.stock_before, self.replenished, self.consumed,
            self.stock_after, self.hours_before, self.hours_after,
        )), "MATERIAL_INTEGER")
        require(self.stock_before >= 0 and self.replenished >= 0 and self.consumed >= 0,
                "MATERIAL_NEGATIVE")
        require(self.stock_after >= 0, "MATERIAL_CLAMPED_OR_NEGATIVE")
        require(self.stock_after == self.stock_before + self.replenished - self.consumed,
                "MATERIAL_CONSERVATION")
        require(self.consumed <= self.stock_before + self.replenished,
                "MATERIAL_OVERCONSUMPTION")
        require(self.hours_after <= self.hours_before, "MATERIAL_HOURS")
        require(self.receipt.get("schema") == MATERIAL_SCHEMA, "MATERIAL_RECEIPT")
        require(self.receipt.get("receipt_hash") == digest(
            {k: v for k, v in self.receipt.items() if k != "receipt_hash"}
        ), "MATERIAL_RECEIPT_HASH")
        if self.state == "REFUSED_MATERIAL_EXHAUSTED":
            require(self.consumed == 0, "REFUSAL_CONSUMED_MATERIAL")
            require(self.stock_after == self.stock_before + self.replenished,
                    "REFUSAL_STOCK_CHANGED")
            require(self.hours_after == self.hours_before, "REFUSAL_USED_HOURS")

    @classmethod
    def consume(cls, *, stock_before: int, replenish: int, consume: int,
                hours_before: int, hours_after: int, tick: int,
                replenishment_ref: str | None = None,
                work_ref: str = "I1_MARKET_WORK") -> "MaterialLedger":
        events: list[dict[str, Any]] = []
        if replenish:
            require(bool(replenishment_ref), "REPLENISHMENT_REF_REQUIRED")
            events.append({
                "kind": "MATERIAL_REPLENISHMENT", "tick": tick - 1,
                "units": replenish, "source": "TEST_ONLY_SOURCE_VISIBLE_PRIOR_STOCK",
                "receipt_ref": replenishment_ref,
            })
        if stock_before + replenish < consume:
            raise ContinuityRefusal("MATERIAL_EXHAUSTED")
        events.append({
            "kind": work_ref, "tick": tick, "material_delta": -consume,
            "stock_before": stock_before, "replenished": replenish,
            "stock_after": stock_before + replenish - consume,
            "hours_before": hours_before, "hours_after": hours_after,
        })
        receipt = {
            "schema": MATERIAL_SCHEMA, "state": "MATERIAL_BALANCED",
            "stock_before": stock_before, "replenished": replenish,
            "consumed": consume, "stock_after": stock_before + replenish - consume,
            "hours_before": hours_before, "hours_after": hours_after,
            "events": events, "clamped": False,
        }
        receipt["receipt_hash"] = digest(receipt)
        return cls(MATERIAL_SCHEMA, "MATERIAL_BALANCED", stock_before, replenish,
                   consume, stock_before + replenish - consume, hours_before,
                   hours_after, tuple(events), receipt)

    @classmethod
    def explicit_refusal(cls, *, stock_before: int, replenish: int,
                         hours_before: int, tick: int,
                         reason: str = "MATERIAL_EXHAUSTED") -> "MaterialLedger":
        require(stock_before + replenish < 1 or reason == "EXPLICIT_NON_STOCKING_ACTION",
                "REFUSAL_NOT_WARRANTED")
        events = ({
            "kind": "MATERIAL_WORK_REFUSED", "tick": tick,
            "material_delta": 0, "reason": reason,
        },)
        receipt = {
            "schema": MATERIAL_SCHEMA, "state": "REFUSED_MATERIAL_EXHAUSTED",
            "stock_before": stock_before, "replenished": replenish,
            "consumed": 0, "stock_after": stock_before + replenish,
            "hours_before": hours_before, "hours_after": hours_before,
            "events": list(events), "clamped": False, "reason": reason,
        }
        receipt["receipt_hash"] = digest(receipt)
        return cls(MATERIAL_SCHEMA, "REFUSED_MATERIAL_EXHAUSTED", stock_before,
                   replenish, 0, stock_before + replenish, hours_before,
                   hours_before, events, receipt)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema, "state": self.state,
            "stock_before": self.stock_before, "replenished": self.replenished,
            "consumed": self.consumed, "stock_after": self.stock_after,
            "hours_before": self.hours_before, "hours_after": self.hours_after,
            "events": list(self.events), "receipt": dict(self.receipt),
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "MaterialLedger":
        return cls(value["schema"], value["state"], value["stock_before"],
                   value["replenished"], value["consumed"], value["stock_after"],
                   value["hours_before"], value["hours_after"],
                   tuple(value["events"]), dict(value["receipt"]))


@dataclass(frozen=True)
class BAction:
    action: str
    performer: str | None
    kind: str
    observed: bool
    a_event_access: bool
    a_tool_access: bool
    b_hours_before: int
    b_hours_after: int
    b_history_digest: str
    shared_history_digest: str
    material: MaterialLedger
    performed: bool
    evaluated: bool
    evaluation_receipt: Mapping[str, Any] | None
    source_record: Mapping[str, Any]

    def __post_init__(self) -> None:
        require(self.action in {"SHARE", "REFUSE", "SILENCE", "NO_PROPOSAL", "NO_CHANGE"},
                "B_ACTION")
        require(self.kind in {"TEST_ONLY_INTERVENTION", "NON_EVENT_CONDITION",
                              "EVALUATED_NO_CHANGE"}, "B_KIND")
        require(self.a_event_access == (self.observed and self.performed), "A_EVENT_ACCESS")
        if self.action == "REFUSE":
            require(self.performer == "B" and self.performed, "REFUSE_REQUIRES_PERFORMER")
            require(not self.a_tool_access, "REFUSE_TOOL_ACCESS")
        if self.action == "SHARE":
            require(self.performer == "B" and self.performed, "SHARE_REQUIRES_PERFORMER")
            require(self.a_tool_access, "SHARE_TOOL_ACCESS")
        if self.action == "SILENCE":
            require(self.performer is None and not self.performed, "SILENCE_IS_NON_EVENT")
            require(not self.a_event_access and not self.a_tool_access, "SILENCE_ACCESS")
        if self.action == "NO_PROPOSAL":
            require(self.performer is None and not self.performed, "NO_PROPOSAL_IS_NON_EVENT")
            require(not self.a_event_access and not self.a_tool_access, "NO_PROPOSAL_ACCESS")
        if self.action == "NO_CHANGE":
            require(self.performer is None and not self.performed, "NO_CHANGE_NOT_PERFORMED")
            if self.evaluated:
                receipt = self.evaluation_receipt or {}
                require(receipt.get("decision_state") == "NO_CHANGE", "NO_CHANGE_RECEIPT")
                require(bool(receipt.get("rule_ref")) and bool(receipt.get("receipt_hash")),
                        "NO_CHANGE_RECEIPT")
            else:
                require(self.evaluation_receipt is None, "HELD_HAS_NO_RECEIPT")
        require(self.b_history_digest and self.shared_history_digest, "B_ROOTS")

    def to_dict(self) -> dict[str, Any]:
        return {
            "action": self.action, "performer": self.performer, "kind": self.kind,
            "observed": self.observed, "a_event_access": self.a_event_access,
            "a_tool_access": self.a_tool_access, "b_hours_before": self.b_hours_before,
            "b_hours_after": self.b_hours_after,
            "b_history_digest": self.b_history_digest,
            "shared_history_digest": self.shared_history_digest,
            "material": self.material.to_dict(), "performed": self.performed,
            "evaluated": self.evaluated,
            "evaluation_receipt": copy.deepcopy(self.evaluation_receipt),
            "source_record": copy.deepcopy(self.source_record),
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "BAction":
        return cls(value["action"], value["performer"], value["kind"],
                   value["observed"], value["a_event_access"], value["a_tool_access"],
                   value["b_hours_before"], value["b_hours_after"],
                   value["b_history_digest"], value["shared_history_digest"],
                   MaterialLedger.from_dict(value["material"]), value["performed"],
                   value["evaluated"], copy.deepcopy(value["evaluation_receipt"]),
                   copy.deepcopy(value["source_record"]))


class BWorld:
    """One exact R5 F1C TEST_ONLY B world, checked against its live prehistory."""

    def __init__(self) -> None:
        import f1c
        self.f1c = f1c
        self.life, self.frozen, self.expected = f1c.freeze()

    def verify(self) -> None:
        require(digest(self.frozen) == self.expected, "FROZEN_ROOT_CHANGED")
        live = self.f1c.live_prior(self.life)
        require(digest(live["A"]) == digest(self.frozen["prior"]["A"]),
                "LIVE_A_HISTORY_CHANGED")
        require(digest(live["B"]) == digest(self.frozen["prior"]["B"]),
                "LIVE_B_HISTORY_CHANGED")
        require(digest(live["shared"]) == digest(self.frozen["prior"]["shared"]),
                "LIVE_SHARED_HISTORY_CHANGED")

    def action(self, action: str, *, observed: bool = True,
               market_work: MaterialLedger | None = None,
               evaluation_receipt: Mapping[str, Any] | None = None,
               no_resource: bool = False, encumbered: bool = False,
               cut_source: bool = False, forged_shared: bool = False,
               forged_b: bool = False) -> BAction:
        self.verify()
        require(not forged_b, "B_HISTORY_CHANGED")
        require(not forged_shared, "SHARED_HISTORY_CHANGED")
        b_digest = digest(self.frozen["prior"]["B"])
        shared_digest = digest(self.frozen["prior"]["shared"])
        world = self.frozen["world"]
        b_hours = int(world["B_free_hours"])
        if action in {"SHARE", "REFUSE", "SILENCE"}:
            _w, post, source, record = self.f1c.intervene(
                self.frozen, action, observed=observed, cut_source=cut_source,
                no_resource=no_resource, encumbered=encumbered,
            )
            b_hours_after = int(post["B_free_hours"])
            require((record["performer"] == "B") == (action != "SILENCE"),
                    "B_PERFORMER_MISMATCH")
            material = market_work or MaterialLedger.consume(
                stock_before=0, replenish=0, consume=0, hours_before=b_hours,
                hours_after=b_hours_after, tick=250,
                work_ref="B_TOOL_ACTION_NO_MATERIAL",
            )
            return BAction(
                action=action, performer=record["performer"], kind=record["kind"],
                observed=observed, a_event_access=record["A_event_access"],
                a_tool_access=record["A_tool_access"], b_hours_before=b_hours,
                b_hours_after=b_hours_after, b_history_digest=b_digest,
                shared_history_digest=shared_digest, material=material,
                performed=record["performer"] is not None, evaluated=False,
                evaluation_receipt=None, source_record=record,
            )
        material = market_work or MaterialLedger.consume(
            stock_before=0, replenish=0, consume=0, hours_before=b_hours,
            hours_after=b_hours, tick=250, work_ref="B_NO_ACTION_NO_MATERIAL",
        )
        if action == "NO_PROPOSAL":
            record = {
                "action": "NO_PROPOSAL", "kind": "NON_EVENT_CONDITION",
                "performer": None, "A_event_access": False,
                "A_tool_access": False, "receipt_hash": digest(
                    {"action": "NO_PROPOSAL", "tick": 250}),
            }
            return BAction(action, None, "NON_EVENT_CONDITION", observed, False,
                           False, b_hours, b_hours, b_digest, shared_digest,
                           material, False, False, None, record)
        if action == "NO_CHANGE":
            evaluated = evaluation_receipt is not None
            record = {
                "action": "NO_CHANGE", "kind": "EVALUATED_NO_CHANGE",
                "performer": None, "A_event_access": False,
                "A_tool_access": False,
                "receipt_hash": digest(evaluation_receipt or {"held": True, "tick": 250}),
            }
            return BAction(action, None, "EVALUATED_NO_CHANGE", observed, False,
                           False, b_hours, b_hours, b_digest, shared_digest,
                           material, False, evaluated,
                           copy.deepcopy(evaluation_receipt), record)
        raise ContinuityRefusal("UNSUPPORTED_B_ACTION")


def _state(action: BAction) -> str:
    if action.action == "SHARE":
        return "SHARE_OBSERVED" if action.observed else "SHARE_UNOBSERVED"
    if action.action == "REFUSE":
        return "TARGETLESS_REFUSE"
    if action.action == "SILENCE":
        return "TARGETLESS_SILENCE"
    if action.action == "NO_PROPOSAL":
        return "TARGETLESS_NO_PROPOSAL"
    if action.action == "NO_CHANGE":
        return "EVALUATED_NO_CHANGE" if action.evaluated else "HELD_MISSING_RULE"
    raise ContinuityRefusal("UNKNOWN_ACTION_STATE")


@dataclass(frozen=True)
class TargetlessC10Ledger:
    schema: str
    roots: Mapping[str, Any]
    action: BAction
    state: str
    c9_proposal: None
    c9_target: None
    performed_e2: bool
    learned_practice: bool
    utterance: None
    durable_history: tuple[Mapping[str, Any], ...]
    tick_before: int
    tick_after: int
    receipt: Mapping[str, Any]

    def __post_init__(self) -> None:
        require(self.schema == SCHEMA, "C10_SCHEMA")
        expected = None if self.action.action == "SHARE" else _state(self.action)
        if self.action.action == "SHARE":
            require(self.state in SHARE_STATES, "C10_SHARE_STATE")
        else:
            require(self.state == expected, "C10_STATE")
        if self.state in TARGETLESS_STATES:
            require(self.c9_proposal is None and self.c9_target is None,
                    "TARGETLESS_MUST_NOT_FABRICATE_TARGET")
            require(not self.performed_e2 and not self.learned_practice,
                    "TARGETLESS_MUST_NOT_FABRICATE_E2_OR_PRACTICE")
            require(self.utterance is None, "TARGETLESS_MUST_NOT_FABRICATE_UTTERANCE")
            require(self.tick_after > self.tick_before, "TARGETLESS_MUST_ADVANCE_TIME")
            require(bool(self.durable_history), "TARGETLESS_DURABILITY")
        if self.state == "HELD_MISSING_RULE":
            require(not self.action.evaluated, "HELD_WITH_EVALUATION")
        if self.state == "EVALUATED_NO_CHANGE":
            require(self.action.evaluated, "NO_CHANGE_WITHOUT_EVALUATION")
        require(self.receipt.get("schema") == SCHEMA, "C10_RECEIPT_SCHEMA")
        require(self.receipt.get("receipt_hash") == digest(
            {k: v for k, v in self.receipt.items() if k != "receipt_hash"}
        ), "C10_RECEIPT_HASH")

    @classmethod
    def build(cls, action: BAction, *, tick_before: int = 241,
              tick_after: int = 251) -> "TargetlessC10Ledger":
        state = _state(action)
        roots = {
            "b_history_digest": action.b_history_digest,
            "shared_history_digest": action.shared_history_digest,
            "frozen_root": action.source_record.get("frozen_parent_hash"),
            "action_receipt_hash": action.source_record.get("receipt_hash"),
        }
        durable = (
            {"kind": "B_ACTION_RECORD", "action": action.action,
             "performer": action.performer, "observed": action.observed,
             "tick": tick_after, "receipt_hash": action.source_record.get("receipt_hash")},
            {"kind": "MATERIAL_LEDGER", "receipt_hash": action.material.receipt["receipt_hash"],
             "stock_after": action.material.stock_after,
             "hours_after": action.material.hours_after},
        )
        receipt = {
            "schema": SCHEMA, "state": state, "roots": roots,
            "action": action.to_dict(), "c9_proposal": None, "c9_target": None,
            "performed_e2": False, "learned_practice": False, "utterance": None,
            "durable_history": list(durable), "tick_before": tick_before,
            "tick_after": tick_after,
        }
        receipt["receipt_hash"] = digest(receipt)
        return cls(SCHEMA, roots, action, state, None, None, False, False, None,
                   durable, tick_before, tick_after, receipt)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema, "roots": dict(self.roots),
            "action": self.action.to_dict(), "state": self.state,
            "c9_proposal": None, "c9_target": None,
            "performed_e2": self.performed_e2,
            "learned_practice": self.learned_practice, "utterance": None,
            "durable_history": list(self.durable_history),
            "tick_before": self.tick_before, "tick_after": self.tick_after,
            "receipt": dict(self.receipt),
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "TargetlessC10Ledger":
        return cls(value["schema"], dict(value["roots"]),
                   BAction.from_dict(value["action"]), value["state"], None, None,
                   value["performed_e2"], value["learned_practice"], None,
                   tuple(value["durable_history"]), value["tick_before"],
                   value["tick_after"], dict(value["receipt"]))


@dataclass
class ContinuingPerson:
    actor_id: str = "A"
    memory: list[dict[str, Any]] = field(default_factory=list)
    tool_access: int = 0
    c10_history: list[str] = field(default_factory=list)

    def consume(self, ledger: TargetlessC10Ledger) -> None:
        action = ledger.action
        if action.observed and action.performed:
            event_kind = {"SHARE": "B_SHARED_TOOL", "REFUSE": "B_REFUSED_TOOL"}[action.action]
            self.memory.append({
                "kind": event_kind, "actor": "B", "observed": True,
                "performed": True, "tick": ledger.tick_after,
                "receipt_hash": action.source_record.get("receipt_hash"),
            })
        elif ledger.state == "EVALUATED_NO_CHANGE":
            self.memory.append({
                "kind": "EVALUATED_NO_CHANGE", "actor": "A", "observed": True,
                "performed": False, "evaluated": True,
                "tick": ledger.tick_after,
                "receipt_hash": (action.evaluation_receipt or {}).get("receipt_hash"),
            })
        if action.a_tool_access:
            self.tool_access = 1
        self.c10_history.append(ledger.receipt["receipt_hash"])

    def assert_memory_consistency(self) -> None:
        for event in self.memory:
            require(event.get("observed") is True, "UNOBSERVED_EVENT_IN_MEMORY")
            if event.get("actor") == "B":
                require(event.get("performed") is True, "FABRICATED_B_EVENT_IN_MEMORY")
            if event.get("kind") == "EVALUATED_NO_CHANGE":
                require(event.get("evaluated") is True, "NO_CHANGE_WITHOUT_EVALUATION")
                require(bool(event.get("receipt_hash")), "NO_CHANGE_WITHOUT_RECEIPT")

    def read_later(self) -> dict[str, Any]:
        self.assert_memory_consistency()
        b_events = [e for e in self.memory if e.get("actor") == "B"]
        return {
            "actor_id": self.actor_id, "memory": copy.deepcopy(self.memory),
            "tool_access": self.tool_access, "c10_history": list(self.c10_history),
            "can_read_B_behavior": bool(b_events),
            "b_event_kinds": [e["kind"] for e in b_events],
            "evaluated_no_change": any(e["kind"] == "EVALUATED_NO_CHANGE" for e in self.memory),
        }

    def to_dict(self) -> dict[str, Any]:
        return {"actor_id": self.actor_id, "memory": copy.deepcopy(self.memory),
                "tool_access": self.tool_access, "c10_history": list(self.c10_history)}

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "ContinuingPerson":
        return cls(value["actor_id"], copy.deepcopy(value["memory"]),
                   value["tool_access"], list(value["c10_history"]))


def cold_replay(payload: Mapping[str, Any]) -> dict[str, Any]:
    ledger = TargetlessC10Ledger.from_dict(payload["ledger"])
    person = ContinuingPerson.from_dict(payload["person"])
    person.assert_memory_consistency()
    return {
        "ledger_hash": ledger.receipt["receipt_hash"],
        "state": ledger.state,
        "person": person.to_dict(),
        "read": person.read_later(),
    }
