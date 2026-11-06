"""Adapter to the accepted S47 actor/world owner, at its TEST_ONLY scope.

Callers supply the case, source and permitted participants. The shared engine
does not select a workshop, actor or developmental response. P2 has no native
operation-id recovery, so interrupted writes remain ambiguous and fail closed.
"""
from __future__ import annotations

from dataclasses import asdict
import fcntl
import json
from pathlib import Path
import sqlite3
import sys
from typing import Mapping

from .contracts import (
    EventProposal, RealizedEvent, RecursionRefusal, StateIdentity,
    canonical, detached, digest,
)


def load_p2():
    repo = Path(__file__).resolve().parents[3]
    package = repo / "WORKER_RETURNS/SOROK-P2-PRODUCT-FANIN-20261105-R1"
    if not (package / "p2_product_fanin/integration.py").is_file():
        raise RecursionRefusal("P2_SOURCE_MISSING")
    if str(package) not in sys.path:
        sys.path.insert(0, str(package))
    from p2_product_fanin.integration import P2ProductFanin
    return P2ProductFanin


class P2Owner:
    grade = "TEST_ONLY_S47_OWNER_NOT_NATIVE_DEVELOPMENTAL_SCIENCE"

    def __init__(self, fanin, *, case: Mapping, source: Mapping,
                 participants: tuple[str, ...]):
        self.fanin = fanin
        self.case = detached(case)
        self.source = detached(source)
        self.participants = participants
        self.source_ref = "P2_INPUT:" + digest({"case": self.case, "source": self.source})
        root = fanin.session.read_root()
        if participants != tuple(root["actor_ids"]):
            raise RecursionRefusal("P2_PARTICIPANTS_NOT_BOUND_TO_ROOT")
        self.actor = root["actor_ids"][0]
        self.db = sqlite3.connect(Path(fanin.session.state_root) / "recursion_owner.sqlite")
        self.db.execute("CREATE TABLE IF NOT EXISTS operations "
                        "(id TEXT PRIMARY KEY, proposal TEXT NOT NULL, "
                        "before_state TEXT NOT NULL, result TEXT)")
        self.db.commit()

    def snapshot(self) -> StateIdentity:
        s = self.fanin.session
        verified = s.verify()
        if not verified.get("ok"):
            raise RecursionRefusal("P2_SOURCE_OR_STATE_VERIFICATION_FAILED")
        material = {
            "world": vars(s.world()),
            "events": s.read_events(),
            "intervals": s.read_interval_states(),
            "encounters": s.read_encounters(),
        }
        return StateIdentity(self.fanin.root_hash, self.actor, s.branch_id,
                             s.clock(), digest(material))

    def validate_proposal(self, proposal: EventProposal) -> None:
        if proposal.operation != "ADMIT_EVENT":
            raise RecursionRefusal("P2_OPERATION_NOT_QUALIFIED:" + proposal.operation)
        if proposal.source_refs != (self.source_ref,):
            raise RecursionRefusal("P2_ABSENT_OR_WRONG_SOURCE")
        if proposal.participants != self.participants or not self.participants:
            raise RecursionRefusal("P2_PARTICIPANT_SCOPE_MISMATCH")
        if set(proposal.circumstances) - {"history_refs", "language_context"}:
            raise RecursionRefusal("P2_UNSUPPORTED_EVENT_CIRCUMSTANCES")
        now = self.snapshot().clock
        if isinstance(proposal.event_time, bool) or not isinstance(proposal.event_time, int):
            raise RecursionRefusal("P2_INVALID_EVENT_CLOCK")
        if proposal.event_time <= now:
            raise RecursionRefusal("P2_EVENT_CLOCK_NOT_FUTURE")
        if proposal.interval is not None:
            if set(proposal.interval) != {"mode", "span"}:
                raise RecursionRefusal("P2_INTERVAL_SCHEMA")
            span = proposal.interval["span"]
            if isinstance(span, bool) or not isinstance(span, int) or span < 1:
                raise RecursionRefusal("P2_INVALID_INTERVAL_SPAN")
            if proposal.interval["mode"] not in {"ACTUAL", "SCHEDULED_ONLY"}:
                raise RecursionRefusal("P2_UNQUALIFIED_INTERVAL_MODE")
            if now + span >= proposal.event_time:
                raise RecursionRefusal("P2_INTERVAL_CROSSES_EVENT_CLOCK")

    def realize(self, operation_id: str, proposal: EventProposal,
                expected: StateIdentity) -> RealizedEvent:
        lock = Path(self.fanin.session.state_root) / "recursion_owner.lock"
        with lock.open("a") as handle:
            fcntl.flock(handle, fcntl.LOCK_EX)
            return self._realize(operation_id, proposal, expected)

    def _realize(self, operation_id: str, proposal: EventProposal,
                 expected: StateIdentity) -> RealizedEvent:
        proposal_hash = digest(proposal.document())
        # BEGIN IMMEDIATE serializes adapter calls, including native owner writes.
        self.db.execute("BEGIN IMMEDIATE")
        row = self.db.execute("SELECT proposal, before_state, result FROM operations "
                              "WHERE id=?", (operation_id,)).fetchone()
        if row is not None:
            self.db.rollback()
            if row[:2] != (proposal_hash, canonical(expected.document())):
                raise RecursionRefusal("P2_OPERATION_REUSE_MISMATCH")
            if row[2] is None:
                raise RecursionRefusal("P2_AMBIGUOUS_PRIOR_OPERATION_HOLD")
            body = json.loads(row[2])
            body["before"] = StateIdentity(**body["before"])
            body["after"] = StateIdentity(**body["after"])
            body["readset"] = tuple(body["readset"])
            result = RealizedEvent(**body)
            if self.snapshot() != result.after:
                raise RecursionRefusal("P2_REPLAY_STATE_MISMATCH")
            return result
        try:
            if self.snapshot() != expected:
                raise RecursionRefusal("P2_STALE_ROOT_BRANCH_CLOCK_OR_STATE")
            self.validate_proposal(proposal)
            self.db.execute("INSERT INTO operations VALUES (?,?,?,NULL)",
                            (operation_id, proposal_hash, canonical(expected.document())))
            self.db.commit()
        except BaseException:
            self.db.rollback()
            raise
        # The reservation survives errors/crashes. Native P2 operations are never
        # reissued blindly. A pending result requires owner-level reconciliation.
        s = self.fanin.session
        material_before = detached(s.world().actor_state)
        interval_result = None
        if proposal.interval is not None:
            deps = self.fanin.deps
            start = s.clock()
            domain = deps["make_domain"](mode=proposal.interval["mode"], start=start,
                                         end=start + proposal.interval["span"])
            interval_result = s.produce_interval(domain)
        refs = tuple(proposal.circumstances.get("history_refs") or ())
        if not refs:
            refs = tuple(x["e1_event_id"] for x in s.read_events())
        kwargs = {}
        if "language_context" in proposal.circumstances:
            kwargs["language_context"] = detached(proposal.circumstances["language_context"])
        admitted = s.admit_event(case=self.case, source=self.source,
                                 history_event_refs=refs, event_time=proposal.event_time,
                                 **kwargs)
        event = admitted.get("event") or {}
        event_ref = event.get("e1_event_id")
        if not event_ref:
            raise RecursionRefusal("P2_NATIVE_EVENT_NOT_REALIZED")
        read = s.read_event(event_ref)
        language = s.read_s43_event(event_ref)
        conditioning = s.read_c9_conditioning(event_ref)
        from p2_continuation.continuation import _s43_summary, _c9_summary
        observation = {
            "event_ref": event_ref,
            "event_hash": read["e1_event_hash"],
            "status": admitted.get("status"),
            "event_ordinal": event.get("event_ordinal"),
            "performed": event.get("performed"),
            "s43": _s43_summary(language),
            "c9": _c9_summary(conditioning),
        }
        after = self.snapshot()
        consequence = {
            "grade": self.grade,
            "owner_state_changed": expected.state_hash != after.state_hash,
            "material_state_changed": material_before != detached(s.world().actor_state),
            "interval": detached(interval_result),
            "immediate_response": observation["c9"],
            "durable_psychological_transition": "MISSING_RULE",
            "independent_B": "CONTROLLED_SOURCEFREE_PARTICIPANT_ONLY",
        }
        result = RealizedEvent(
            operation_id, proposal_hash, expected, after, "REALIZED",
            {"event": detached(read), "interval": detached(interval_result)},
            self.fanin.public_opportunity(observation), consequence,
            (self.source_ref, read["e1_event_hash"]), "P2_EVENT:" + read["e1_event_hash"],
        )
        self.db.execute("UPDATE operations SET result=? WHERE id=?",
                        (canonical(asdict(result)), operation_id))
        self.db.commit()
        return result

    def close(self) -> None:
        self.db.close()
        self.fanin.close()
