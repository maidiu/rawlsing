"""Two-actor historical person-forming composer over G18 material receipts.

This is a sourcefree historical actor/other producer at TEST_ONLY grain. The G18
source-issued material and performed-action receipts are reused for the joint
material task. Each BP1 actor has its own source, G18 history, append-only ledger,
state and snapshot. The shared objective event is an objective fact recorded
identically in both ledgers; it grants no actor state or psychology.

NOT native ADP007 actor genesis, not a CAN008/CAN011 rule, not a person, parent,
child or genealogy claim.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any

from .canon import digest, seal
from .ledger import (
    ActorLedger,
    LedgerRefusal,
    make_objective_event,
    verify_snapshot,
)
from .source import (
    ActorSource,
    TEST_ONLY_PREFIX,
    issue_actor_source,
)

A_ACTOR = "TEST_ONLY_BP1_ACTOR_A"
B_ACTOR = "TEST_ONLY_BP1_ACTOR_B"


def _world(units: int = 5) -> dict:
    from lab_sgi1.history import PersonHistoryBuilder
    base = deepcopy(next(
        e["payload"] for e in PersonHistoryBuilder("BP1_BASE", "BP1_SEED").build()
        if e["kind"] == "WORLD_MATERIAL"))
    base["material_units"] = units
    return base


def issue_default_sources() -> tuple[ActorSource, ActorSource]:
    a = issue_actor_source(
        actor_id=A_ACTOR, role="repair", seed="BP1_SEED_A_REPAIR",
        birth_clock=10, initial_cash=30, initial_free_hours=30,
        material_units=5, other_actor_id=B_ACTOR)
    b = issue_actor_source(
        actor_id=B_ACTOR, role="finishing", seed="BP1_SEED_B_FINISH",
        birth_clock=12, initial_cash=30, initial_free_hours=30,
        material_units=2, other_actor_id=A_ACTOR)
    return a, b


def build_actor_history(source: ActorSource) -> tuple[list[dict], dict]:
    from lab_sgi1.history import PersonHistoryBuilder, replay_history
    events = PersonHistoryBuilder(
        source.actor_id, source.seed, role=source.role,
        material=_world(source.material_units)).build()
    replay = replay_history(events)
    if not replay["valid"]:
        raise LedgerRefusal("ACTOR_G18_HISTORY_NOT_RESOLVED")
    return events, replay


def future_child_findings(value: Any) -> list[dict]:
    """Recursive future-child scan over a nested payload (G18 guard reuse)."""
    from lab_sgi1.proposal import find_future_child_material
    return find_future_child_material(value, "$")


def assert_no_future_child(value: Any):
    findings = future_child_findings(value)
    if findings:
        raise LedgerRefusal("FUTURE_CHILD_INFORMATION_LEAK")


@dataclass
class TwoActorLife:
    a_source: ActorSource
    b_source: ActorSource
    a_events: list[dict]
    b_events: list[dict]
    a_replay: dict
    b_replay: dict
    material: dict
    witness: dict
    objective: dict
    a_ledger: ActorLedger
    b_ledger: ActorLedger
    a_snapshot: dict
    b_snapshot: dict

    def receipt(self) -> dict:
        return {
            "schema": "BP1_TWO_ACTOR_LIFE@1",
            "source_grade": self.a_source.source_grade,
            "native_grant": self.a_source.native_grant,
            "actor_ids": [self.a_source.actor_id, self.b_source.actor_id],
            "source_refs": [self.a_source.source_ref, self.b_source.source_ref],
            "source_hashes": [self.a_source.source_hash, self.b_source.source_hash],
            "g18_history_hashes": [self.a_replay["history_hash"],
                                   self.b_replay["history_hash"]],
            "shared_objective_ref": self.objective["objective_event_id"],
            "shared_objective_hash": self.objective["objective_hash"],
            "material_event_ref": self.material["event_id"],
            "material_receipt_id": digest(self.material["source_receipt"]),
            "witness_status": self.witness["status"],
            "witness_ref": self.witness["event_id"],
            "performed_actions": [
                {
                    "owner_id": action["owner_id"],
                    "event_id": action["event_id"],
                    "receipt_id": digest(action["source_receipt"]),
                    "before": action["before"],
                    "after": action["after"],
                    "material_event_ref": action["material_event_ref"],
                }
                for action in self.witness["actions"]
            ],
            "ledger_event_refs": {
                self.a_source.actor_id: list(self.a_ledger.event_ids),
                self.b_source.actor_id: list(self.b_ledger.event_ids),
            },
            "snapshots": [self.a_snapshot, self.b_snapshot],
            "state_hashes": [self.a_snapshot["state_hash"],
                             self.b_snapshot["state_hash"]],
            "history_hashes": [self.a_snapshot["history_hash"],
                               self.b_snapshot["history_hash"]],
            "claim": ("TWO_SOURCEFREE_HISTORICAL_ACTOR_LEDGERS_WITH_"
                      "INDEPENDENT_PERFORMED_ACTIONS_AND_SHARED_OBJECTIVE_"
                      "FACTS_NOT_NATIVE_ACTORS"),
            "native_actor_claim": False,
            "psychology_claim": False,
        }


def build_two_actor_life() -> TwoActorLife:
    from lab_sgi1.joint import (
        material_joint_opportunity, observe_joint_actions, validate_joint,
    )
    a_source, b_source = issue_default_sources()
    a_events, a_replay = build_actor_history(a_source)
    b_events, b_replay = build_actor_history(b_source)
    material = material_joint_opportunity(
        effective_index=200, units=1, payment_per_actor=2, task_hours=1)
    anchor = {"actor_id": a_source.actor_id, "history_events": a_events}
    witness = observe_joint_actions(anchor, b_events, material)
    if witness["status"] != "WITNESSED" or not validate_joint(anchor, b_events, witness):
        raise LedgerRefusal("JOINT_PERFORMED_ACTION_NOT_WITNESSED")
    objective = make_objective_event(
        material, witness, [a_source.actor_id, b_source.actor_id])
    a_ledger = ActorLedger(a_source, prior_history_events=a_events)
    b_ledger = ActorLedger(b_source, prior_history_events=b_events)
    a_ledger.append_shared_objective(
        objective, parents=(a_ledger.prior_history_event_id,))
    b_ledger.append_shared_objective(
        objective, parents=(b_ledger.prior_history_event_id,))
    a_action = next(x for x in witness["actions"]
                    if x["owner_id"] == a_source.actor_id)
    b_action = next(x for x in witness["actions"]
                    if x["owner_id"] == b_source.actor_id)
    a_ledger.append_performed_action(
        a_action, material, objective["objective_event_id"],
        parents=(a_ledger.prior_history_event_id,
                 a_ledger.objective_events[-1].event_id))
    b_ledger.append_performed_action(
        b_action, material, objective["objective_event_id"],
        parents=(b_ledger.prior_history_event_id,
                 b_ledger.objective_events[-1].event_id))
    a_ledger.append_other_action(
        b_action, material,
        parents=(a_ledger.objective_events[-1].event_id,))
    b_ledger.append_other_action(
        a_action, material,
        parents=(b_ledger.objective_events[-1].event_id,))
    a_ledger.append_relation_view(
        b_source.actor_id, "UNKNOWN_OR_NONRECIPROCAL",
        "NO_PSYCHIC_RELATION_OWNER_GRANT",
        parents=(a_ledger.events[-1].event_id,))
    b_ledger.append_relation_view(
        a_source.actor_id, "UNKNOWN_OR_NONRECIPROCAL",
        "NO_PSYCHIC_RELATION_OWNER_GRANT",
        parents=(b_ledger.events[-1].event_id,))
    for ledger in (a_ledger, b_ledger):
        accepted, errors = ledger.verify()
        if not accepted:
            raise LedgerRefusal("LEDGER_REPLAY_NOT_VALID:" + ",".join(errors))
    a_snapshot = a_ledger.snapshot()
    b_snapshot = b_ledger.snapshot()
    for snapshot in (a_snapshot, b_snapshot):
        accepted, reason = verify_snapshot(snapshot)
        if not accepted:
            raise LedgerRefusal("SNAPSHOT_NOT_VALID:" + str(reason))
    return TwoActorLife(
        a_source=a_source, b_source=b_source, a_events=a_events,
        b_events=b_events, a_replay=a_replay, b_replay=b_replay,
        material=material, witness=witness, objective=objective,
        a_ledger=a_ledger, b_ledger=b_ledger,
        a_snapshot=a_snapshot, b_snapshot=b_snapshot)


def build_no_change_life() -> dict:
    """A lawful NO_CHANGE: the actor's own material is exhausted before the task."""
    from lab_sgi1.joint import (
        material_joint_opportunity, observe_joint_actions,
    )
    a_source = issue_actor_source(
        actor_id="TEST_ONLY_BP1_ACTOR_A_NOCHANGE", role="repair",
        seed="BP1_SEED_NOCHANGE", birth_clock=10, material_units=2,
        other_actor_id=B_ACTOR)
    b_source = issue_actor_source(
        actor_id=B_ACTOR, role="finishing", seed="BP1_SEED_B_FINISH",
        birth_clock=12, material_units=4, other_actor_id=a_source.actor_id)
    a_events, a_replay = build_actor_history(a_source)
    b_events, b_replay = build_actor_history(b_source)
    material = material_joint_opportunity(
        effective_index=210, units=1, payment_per_actor=2, task_hours=1)
    anchor = {"actor_id": a_source.actor_id, "history_events": a_events}
    witness = observe_joint_actions(anchor, b_events, material)
    objective = make_objective_event(
        material, witness, [a_source.actor_id, b_source.actor_id])
    ledger = ActorLedger(a_source, prior_history_events=a_events)
    ledger.append_shared_objective(
        objective, parents=(ledger.prior_history_event_id,))
    a_action = next(x for x in witness["actions"]
                    if x["owner_id"] == a_source.actor_id)
    before_state = ledger.state
    refusal = ""
    try:
        ledger.append_performed_action(
            a_action, material, objective["objective_event_id"],
            consume_own_material=True, own_material_units=1,
            parents=(ledger.prior_history_event_id,
                     ledger.objective_events[-1].event_id))
    except LedgerRefusal as exc:
        refusal = str(exc)
        ledger.append_no_change(
            "OWN_MATERIAL_EXHAUSTED", parents=(ledger.events[-1].event_id,))
    return {
        "schema": "BP1_NO_CHANGE_LIFE@1",
        "actor_id": a_source.actor_id,
        "refusal": refusal,
        "state_before": before_state,
        "state_after": ledger.state,
        "state_unchanged": before_state == ledger.state,
        "snapshot": ledger.snapshot(),
        "ledger_event_kinds": [e.kind for e in ledger.events],
        "g18_history_hash": a_replay["history_hash"],
        "material_event_ref": material["event_id"],
        "native_grant": a_source.native_grant,
        "source_grade": a_source.source_grade,
    }


def build_denied_life() -> dict:
    """A lawful DENY: the source has no PERFORMED_ACTION permission."""
    from lab_sgi1.joint import (
        material_joint_opportunity, observe_joint_actions,
    )
    permissions = ("PRIOR_HISTORY", "SHARED_OBJECTIVE", "NO_CHANGE", "DENY")
    a_source = issue_actor_source(
        actor_id="TEST_ONLY_BP1_ACTOR_A_DENIED", role="repair",
        seed="BP1_SEED_DENIED", birth_clock=10, material_units=5,
        event_permissions=permissions, other_actor_id=B_ACTOR)
    b_source = issue_actor_source(
        actor_id=B_ACTOR, role="finishing", seed="BP1_SEED_B_FINISH",
        birth_clock=12, material_units=4, other_actor_id=a_source.actor_id)
    a_events, _ = build_actor_history(a_source)
    b_events, _ = build_actor_history(b_source)
    material = material_joint_opportunity(
        effective_index=220, units=1, payment_per_actor=2, task_hours=1)
    anchor = {"actor_id": a_source.actor_id, "history_events": a_events}
    witness = observe_joint_actions(anchor, b_events, material)
    objective = make_objective_event(
        material, witness, [a_source.actor_id, b_source.actor_id])
    ledger = ActorLedger(a_source, prior_history_events=a_events)
    ledger.append_shared_objective(
        objective, parents=(ledger.prior_history_event_id,))
    a_action = next(x for x in witness["actions"]
                    if x["owner_id"] == a_source.actor_id)
    before_state = ledger.state
    refusal = ""
    try:
        ledger.append_performed_action(
            a_action, material, objective["objective_event_id"],
            parents=(ledger.prior_history_event_id,
                     ledger.objective_events[-1].event_id))
    except LedgerRefusal as exc:
        refusal = str(exc)
        ledger.append_deny(
            "ACTOR_PERMISSION_DENIED", parents=(ledger.events[-1].event_id,))
    return {
        "schema": "BP1_DENIED_LIFE@1",
        "actor_id": a_source.actor_id,
        "refusal": refusal,
        "state_before": before_state,
        "state_after": ledger.state,
        "state_unchanged": before_state == ledger.state,
        "snapshot": ledger.snapshot(),
        "ledger_event_kinds": [e.kind for e in ledger.events],
        "material_event_ref": material["event_id"],
        "native_grant": a_source.native_grant,
        "source_grade": a_source.source_grade,
    }
