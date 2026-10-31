"""Read-only A5 encounter over the durable CP-A5 history.

The reader never appends, checkpoints, renders into storage or invents an
experience. It exposes only events present in A's C12 perception rows, a
derived test-only disposition view, and explanatory renderings of those facts.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from bp4.canon import digest

from .events import CP_GRADE

VIEW_SCHEMA = "SOROK_CP_A5_ENCOUNTER_VIEW@1"
ANSWER_SCHEMA = "SOROK_CP_A5_ENCOUNTER_ANSWER@1"


class EncounterRefusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


def _event_map(events: list[dict]) -> dict[str, dict]:
    return {event["event_id"]: event for event in events}


def _known_events(events: list[dict], known_ids: set[str]) -> list[dict]:
    return [event for event in events if event["event_id"] in known_ids]


def _disposition(events: list[dict]) -> dict:
    inspections = [event for event in events
                   if event.get("actor_id") == "A"
                   and event.get("kind") == "INSPECT"]
    contexts = sorted({event.get("location") for event in inspections})
    qualified = len(inspections) >= 3 and len(contexts) >= 2
    return {
        "name": "cross_context_material_verification",
        "state": "ESTABLISHED" if qualified else "INSUFFICIENT",
        "inspection_count": len(inspections),
        "contexts": contexts,
        "event_ids": [event["event_id"] for event in inspections],
        "grade": "TEST_ONLY_SOURCEFREE_DERIVED_DISPOSITION",
        "native": False,
        "note": "This is repeated performed inspection evidence, not a personality trait.",
    }


def _relations(known: list[dict]) -> list[dict]:
    rows = []
    for event in known:
        if event.get("actor_id") != "C":
            continue
        body = event.get("body", {})
        rows.append({
            "coactor": "C",
            "kind": event["kind"],
            "relation": body.get("relation", "UNSPECIFIED"),
            "event_id": event["event_id"],
            "clock": event["clock"],
            "summary": event["summary"],
        })
    return rows


class EncounterReader:
    """A5 read-only view of one actor's durable C12 history."""

    def __init__(self, root: str | Path, *, branch_id: str = "root",
                 actor_id: str = "A") -> None:
        if actor_id != "A":
            raise EncounterRefusal("ENCOUNTER_ACTOR_SWAP_REFUSED", actor_id)
        from bp2p4.i1_product import GuardedJoinedProduct

        self.root = Path(root)
        self.branch_id = branch_id
        self.actor_id = actor_id
        try:
            self.product = GuardedJoinedProduct.reopen(
                self.root, branch_id=branch_id)
        except Exception as error:  # noqa: BLE001 - any open failure is a refusal
            raise EncounterRefusal(
                "ENCOUNTER_BRANCH_REFUSED",
                type(error).__name__ + ":" + str(error)) from error
        try:
            self.product.store.branch(self.branch_id)
        except Exception as error:  # noqa: BLE001 - unknown branch is a refusal
            self.product.close()
            raise EncounterRefusal(
                "ENCOUNTER_BRANCH_REFUSED",
                type(error).__name__ + ":" + str(error)) from error
        try:
            self.product.verify_join()
            report = self.product.verify_c12()
        except Exception as error:  # noqa: BLE001
            self.product.close()
            raise EncounterRefusal(
                "ENCOUNTER_GUARD_REFUSED",
                type(error).__name__ + ":" + str(error)) from error
        if not report["ok"]:
            self.product.close()
            raise EncounterRefusal("ENCOUNTER_GUARD_REFUSED", str(report["errors"]))
        branch = self.product.store.branch(self.branch_id)
        if "A" not in branch["actor_ids"]:
            self.product.close()
            raise EncounterRefusal("ENCOUNTER_ACTOR_IDENTITY_REFUSED")
        self.c12_report = report

    def close(self) -> None:
        self.product.close()

    def __enter__(self) -> "EncounterReader":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def all_events(self) -> list[dict]:
        return self.product.store.world_events(self.branch_id)

    def perceptions(self, actor: str = "A") -> list[dict]:
        return self.product.store.perceptions(self.branch_id, actor)

    def canonical_digest(self) -> str:
        state = self.product.store.latest_state(self.branch_id)
        return digest({
            "state": state,
            "episodes": self.product.store.episodes(self.branch_id),
            "events": self.all_events(),
            "perceptions": self.perceptions("A"),
        })

    def total_changes(self) -> int:
        return int(self.product.store.db.total_changes)

    def view(self) -> dict:
        state = self.product.store.latest_state(self.branch_id)
        events = self.all_events()
        known_ids = {row["event_id"] for row in self.perceptions("A")}
        known = _known_events(events, known_ids)
        return {
            "schema": VIEW_SCHEMA,
            "status": "OK",
            "grade": CP_GRADE,
            "native": False,
            "actor": "A",
            "branch_id": self.branch_id,
            "as_of_clock": state["world"]["clock"],
            "position": state["world"]["positions"].get("A"),
            "canonical_digest": self.canonical_digest(),
            "observed_event_count": len(events),
            "accessed_event_count": len(known_ids),
            "remembered_event_count": len(known_ids),
            "known_event_ids": sorted(known_ids),
            "remembered_events": [
                {"event_id": event["event_id"], "kind": event["kind"],
                 "clock": event["clock"], "location": event["location"],
                 "summary": event["summary"]}
                for event in known
            ],
            "unperceived_event_count": len(events) - len(known),
            "disposition": _disposition(events),
            "relations": _relations(known),
            "tool_available": state["world"]["resources"]["workshop"].get(
                "tool_available"),
        }

    def ask(self, question: str) -> dict:
        before = self.total_changes()
        state = self.product.store.latest_state(self.branch_id)
        events = self.all_events()
        known_ids = {row["event_id"] for row in self.perceptions("A")}
        known = _known_events(events, known_ids)
        by_kind: dict[str, list[dict]] = {}
        for event in events:
            by_kind.setdefault(event["kind"], []).append(event)
        q = " ".join(question.lower().strip().split())
        evidence: list[str] = []
        if "where" in q and ("you" in q or "a" in q):
            status = "OK"
            answer = "A is at the " + str(state["world"]["positions"].get("A")) + "."
        elif "tool" in q:
            take = by_kind.get("B_TAKE_TOOL", [])
            blocked = by_kind.get("A_REPAIR_BLOCKED", [])
            returned = by_kind.get("B_RETURN_TOOL", [])
            visible = [event for event in take + blocked + returned
                       if event["event_id"] in known_ids]
            if not any(event["kind"] == "B_TAKE_TOOL" for event in visible):
                status = "UNKNOWN"
                answer = ("UNKNOWN: A has no perceived event of who moved the "
                          "workshop tool.")
                evidence = []
            else:
                status = "OK"
                answer = ("A perceived B take the workshop tool, could not repair "
                          "while it was away, and perceived its return.")
                evidence = [event["event_id"] for event in visible]
        elif "market" in q:
            commission = by_kind.get("B_MARKET_COMMISSION", [])
            visible = [event for event in commission
                       if event["event_id"] in known_ids]
            if not commission:
                status = "UNKNOWN"
                answer = "UNKNOWN: A perceived no B market activity."
                evidence = []
            elif not visible:
                status = "UNKNOWN"
                answer = "UNKNOWN: A did not perceive B's market commission."
                evidence = []
            else:
                status = "OK"
                answer = "A perceived B's market commission."
                evidence = [event["event_id"] for event in visible]
        elif "carrier" in q or "coactor" in q or q.strip() in {"c", "who is c"}:
            carrier = [event for event in known if event.get("actor_id") == "C"]
            if carrier:
                status = "OK"
                answer = ("A perceived C request the tool and then withdraw the "
                          "request; the request remains unmet.")
                evidence = [event["event_id"] for event in carrier]
            else:
                status = "UNKNOWN"
                answer = "UNKNOWN: A perceived no carrier event."
                evidence = []
        elif "remember" in q or "what happened" in q or "what do you know" in q:
            status = "OK"
            answer = ("A's remembered events are the perceptions listed in the "
                      "read-only view.")
            evidence = sorted(known_ids)
        elif "who are you" in q or "identity" in q:
            status = "OK"
            answer = "A is the same sourcefree joined actor; no native identity is claimed."
        else:
            status = "UNKNOWN"
            answer = "UNKNOWN: this encounter has no grounded answer for that question."
        after = self.total_changes()
        return {
            "schema": ANSWER_SCHEMA,
            "status": status,
            "grade": CP_GRADE,
            "native": False,
            "actor": "A",
            "branch_id": self.branch_id,
            "question": question,
            "answer": answer,
            "evidence_event_ids": evidence,
            "read_only": before == after,
            "canonical_digest": self.canonical_digest(),
        }


def render_encounter(view: dict, style: str = "plain") -> str:
    """Pure explanatory rendering; never writes canonical state."""
    disposition = view["disposition"]
    events = view["remembered_events"]
    if style == "compact":
        return (
            f"A@{view['as_of_clock']} {view['position']} | "
            f"events={len(events)} | disposition={disposition['state']} | "
            f"tool={'present' if view['tool_available'] else 'away'}"
        )
    if style != "plain":
        raise ValueError("UNKNOWN_RENDER_STYLE:" + style)
    lines = [
        f"A is at the {view['position']} at clock {view['as_of_clock']}.",
        f"Remembered events: {len(events)}.",
    ]
    for event in events:
        lines.append(f"- {event['kind']} at {event['clock']}: {event['summary']}")
    lines.append(
        "Derived inspection evidence: "
        f"{disposition['state']} ({disposition['inspection_count']} in "
        f"{len(disposition['contexts'])} contexts).")
    lines.append(
        "Carrier relation: " + (
            view["relations"][-1]["relation"] if view["relations"] else "UNKNOWN"))
    return "\n".join(lines)


__all__ = [
    "ANSWER_SCHEMA",
    "EncounterReader",
    "EncounterRefusal",
    "VIEW_SCHEMA",
    "render_encounter",
]
