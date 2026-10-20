#!/usr/bin/env python3
"""Produce the bounded two-actor material-contrast receipt for G18.

Not a human-life, genealogy, psychological or native-authority claim. Two finite
sourcefree histories with distinct actors, roles, material budgets and performed
actions are replayed and jointly witnessed through the authenticated source
boundary. The receipt records exactly what differs and what remains HOLD.
"""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RETURN / "candidate"))
from lab_sgi1.history import PersonHistoryBuilder, replay_history  # noqa: E402
from lab_sgi1.joint import (  # noqa: E402
    material_joint_opportunity, observe_joint_actions,
    verify_material_source, verify_performed_action,
)
from lab_sgi1.relation import reconcile  # noqa: E402
from lab_sgi1.continuation import forward_continuation  # noqa: E402


def world(units):
    base = deepcopy(next(
        e["payload"] for e in PersonHistoryBuilder("X", "Y").build()
        if e["kind"] == "WORLD_MATERIAL"))
    base["material_units"] = units
    return base


def build(actor, seed, role, units):
    return PersonHistoryBuilder(actor, seed, role=role,
                                material=world(units)).build()


def main():
    e_repair = build("G18_REPAIR", "SEED_REPAIR", "repair", 5)
    e_finish = build("G18_FINISH", "SEED_FINISH", "finishing", 4)
    r_repair = replay_history(e_repair)
    r_finish = replay_history(e_finish)
    material = material_joint_opportunity(effective_index=200)
    anchor = dict(actor_id="G18_REPAIR", history_events=e_repair)
    witness = observe_joint_actions(anchor, e_finish, material)
    relation = reconcile(anchor, e_finish, dict(
        candidate_kind="PROVISIONAL_COUNTERPART", joint_evidence=witness))
    continuation = forward_continuation(anchor, e_finish, relation)

    exhausted = build("G18_FINISH_EXHAUSTED", "SEED_FINISH", "finishing", 3)
    r_exhausted = replay_history(exhausted)
    witness_exhausted = observe_joint_actions(anchor, exhausted, material)
    relation_exhausted = reconcile(anchor, exhausted, dict(
        candidate_kind="PROVISIONAL_COUNTERPART",
        joint_evidence=witness_exhausted))
    continuation_exhausted = forward_continuation(
        anchor, exhausted, relation_exhausted)

    material_ok, material_reason, payload = verify_material_source(
        witness["material"])
    action_checks = [verify_performed_action(a, material)
                     for a in witness["actions"]]
    receipt = dict(
        schema="SOROK_G18_TWO_ACTOR_MATERIAL_CONTRAST@1",
        claim=("TWO_FINITE_SOURCEFREE_MATERIAL_HISTORIES_WITH_DISTINCT_"
               "PERFORMED_ACTIONS_NOT_TWO_DEVELOPED_HUMAN_LIVES"),
        science_grade="SOURCEFREE_FINITE_MATERIAL_VARIATION_ONLY",
        native_grant="NOT_GRANTED",
        human_life_or_genealogy_claim=False,
        actor_ids=["G18_REPAIR", "G18_FINISH"],
        distinct_history_hashes=[r_repair["history_hash"],
                                 r_finish["history_hash"]],
        distinct_event_ids=[
            sorted({e["event_id"] for e in e_repair}
                   - {e["event_id"] for e in e_finish}),
            sorted({e["event_id"] for e in e_finish}
                   - {e["event_id"] for e in e_repair}),
        ],
        states=dict(
            repair=dict(role=r_repair["state"]["role"],
                        completed_units=r_repair["state"]["completed_units"],
                        material_remaining=r_repair["state"]["material_remaining"],
                        cash=r_repair["state"]["cash"],
                        free_hours=r_repair["state"]["free_hours"]),
            finishing=dict(role=r_finish["state"]["role"],
                           completed_units=r_finish["state"]["completed_units"],
                           material_remaining=r_finish["state"]["material_remaining"],
                           cash=r_finish["state"]["cash"],
                           free_hours=r_finish["state"]["free_hours"]),
        ),
        witness=dict(status=witness["status"],
                     participants=witness["participants"],
                     material_verified=material_ok,
                     material_reason=material_reason,
                     source_scope=payload and witness["material"][
                         "source_receipt"]["scope"],
                     action_receipt_checks=[dict(accepted=a, reason=b)
                                            for a, b in action_checks]),
        performed_actions=[dict(owner_id=a["owner_id"],
                                before=a["before"], after=a["after"])
                           for a in witness["actions"]],
        continuation=dict(
            status=relation["status"],
            admitted=len(continuation["continuation_events"]),
            performed_units={e["actor"]: e["payload"]["units_performed"]
                             for e in continuation["continuation_events"]},
            after_completed_units={e["actor"]:
                                   e["payload"]["after"]["completed_units"]
                                   for e in continuation["continuation_events"]},
            parental_status=continuation["parental_status"],
            household_admission=continuation["household_admission"],
            perceived_states=relation.get("perceived_states"),
        ),
        lawful_no_change_alternative=dict(
            actor="G18_FINISH_EXHAUSTED",
            material_remaining=r_exhausted["state"]["material_remaining"],
            witness_status=witness_exhausted["status"],
            relationship_status=relation_exhausted["status"],
            continuation_actors=[e["actor"] for e in
                                 continuation_exhausted["continuation_events"]],
            nonnegative_material=all(
                v >= 0 for v in (r_exhausted["state"]["material_remaining"],)),
        ),
        holds=[
            "NO_NATIVE_ACTOR_OR_BIOLOGY_ISSUANCE",
            "NO_PSYCHOLOGICAL_LAW_OR_CALIBRATION",
            "NO_HUMAN_LIFE_OR_GENEALOGY_CLAIM",
            "M2_MP_NATIVE_SOURCES_REMAIN_TYPED_HOLDS",
            "C9_E1_E2_AND_C11_REMAIN_UNISSUED",
        ],
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
