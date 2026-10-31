"""C4 historical actor snapshot -> exact C9R E1 -> target -> later E2 bridge.

This bridge consumes the pinned C9R sourcefree candidate at TEST_ONLY grade. It
does not promote C9R's disputed author positives or issue native RULE_A/RULE_T.
The historical actor source is the BP1 ledger snapshot; the C9R ingress record is
derived from that snapshot and bound to its sealed hash. A source-edge mutation
or a consumed-state mutation must fail the same named positive assertion.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any

from .canon import digest, valid
from .ledger import verify_snapshot
from .source import BP1_ACTOR_SOURCE_GRADE, BP1_NATIVE_GRANT, TEST_ONLY_PREFIX

ISSUER = "TEST_ONLY_BP1_TARGET_OWNER"
RESPONSE_ISSUER = "TEST_ONLY_BP1_RESPONSE_OWNER"
EVENT_OWNER = "TEST_ONLY_BP1_EVENT_OWNER"
ACTUATOR = "TEST_ONLY_ACTUATOR_B"
OCCURRENCE = "TEST_ONLY_OCCURRENCE_E2"
EXPECTED_ACT = "inspect_with_tool"


class BP1C9Refusal(ValueError):
    pass


@dataclass
class BP1C9Result:
    life: Any
    actor: Any
    actor_record: dict
    event: dict
    conditioning: list[dict]
    rule: Any
    target_rule: Any
    permission: dict
    response_hash: str
    pipeline: Any
    e2: Any
    committed: bool
    state_hash: str = ""
    target_id: str = ""
    commit_time: int = 0
    later_as_of: int = 0

    def receipt(self) -> dict:
        return {
            "schema": "BP1_C9_POSITIVE_RECEIPT@1",
            "committed": self.committed,
            "target_id": self.target_id,
            "state_hash": self.state_hash,
            "actor_id": self.actor_record["actor_id"],
            "actor_source_ref": self.actor_record["source_ref"],
            "actor_source_hash": self.actor_record["source_hash"],
            "actor_source_grade": self.actor.source_grade,
            "native_grant": self.actor.native_grant,
            "event_ref": self.event["event_id"],
            "event_hash": self.event["hash"],
            "material_event_ref": self.life.material["event_id"],
            "other_offer_ref": self.life.b_ledger.performed_action_events[0].event_id,
            "enacted_history_refs": self._history_refs(),
            "target_record_hash": (
                self.pipeline.decision.record_hash
                if self.pipeline and self.pipeline.decision else ""),
            "consumed_state_hash": self.state_hash,
            "target_commit_time": self.commit_time,
            "later_as_of": self.later_as_of,
            "e2_admitted": bool(self.e2 and getattr(self.e2, "admitted", False)),
            "e2_reason": (
                str(getattr(self.e2, "reason", "")) if self.e2 else ""),
            "e2_actuator_ref": (
                getattr(self.e2, "actuator_ref", "") if self.e2 else ""),
            "native_actor_claim": False,
            "native_rule_claim": False,
            "native_e2_claim": False,
        }

    def _history_refs(self) -> list[str]:
        refs = []
        for event in self.life.a_ledger.events:
            if event.kind in {"PRIOR_HISTORY", "PERFORMED_ACTION"}:
                refs.append(event.event_id)
        return refs


def _snapshot(life, actor: str) -> dict:
    if actor == "A":
        return life.a_snapshot
    if actor == "B":
        return life.b_snapshot
    raise BP1C9Refusal("ACTOR_NOT_IN_LIFE")


def _actor_source(life, actor: str):
    return life.a_source if actor == "A" else life.b_source


def build_c9_actor_record(life, *, actor: str = "A",
                          snapshot: dict | None = None) -> dict:
    from candidate import ActorIdentityRecord
    expected = life.a_snapshot["hash"] if actor == "A" else life.b_snapshot["hash"]
    snapshot = _snapshot(life, actor) if snapshot is None else snapshot
    accepted, reason = verify_snapshot(snapshot, expected_hash=expected)
    if not accepted:
        raise BP1C9Refusal("ACTOR_SNAPSHOT_NOT_AUTHENTICATED:" + str(reason))
    source = _actor_source(life, actor)
    return ActorIdentityRecord(
        actor_id=source.actor_id,
        activation_status="ACTIVE",
        standing_state=snapshot["state_hash"],
        currentness_as_of=int(snapshot["last_clock"]),
        source_ref=source.source_ref,
        source_hash=snapshot["hash"],
    ).sealed()


def _event_time(life, actor: str) -> int:
    snapshot = _snapshot(life, actor)
    return int(snapshot["last_clock"]) + 1


def build_c9_event(life, *, actor: str = "A", event_time: int | None = None) -> dict:
    from candidate import make_event_witness
    snapshot = _snapshot(life, actor)
    time = _event_time(life, actor) if event_time is None else int(event_time)
    if time < int(snapshot["last_clock"]):
        raise BP1C9Refusal("EVENT_TIME_BEFORE_ACTOR_CURRENTNESS")
    action_events = life.a_ledger.performed_action_events if actor == "A" else \
        life.b_ledger.performed_action_events
    if not action_events:
        raise BP1C9Refusal("NO_PERFORMED_ACTION_TO_CONSUME")
    return make_event_witness(
        event_id=TEST_ONLY_PREFIX + "E1_" + life.objective["objective_hash"],
        owner_ref=EVENT_OWNER,
        time=time,
        content={
            "fact": "joint_material_task",
            "scene": "workshop",
            "participants": [life.a_source.actor_id, life.b_source.actor_id],
            "objective_event_ref": life.objective["objective_event_id"],
            "objective_hash": life.objective["objective_hash"],
            "material_event_ref": life.material["event_id"],
            "performed_action_ref": action_events[0].event_id,
            "source_grade": BP1_ACTOR_SOURCE_GRADE,
            "native_grant": BP1_NATIVE_GRANT,
        },
        actor_role=life.a_source.actor_id if actor == "A" else life.b_source.actor_id,
    )


def build_c9_conditioning(life, *, actor: str = "A", as_of: int | None = None,
                          event_time: int | None = None) -> list[dict]:
    from candidate import make_conditioning_source
    snapshot = _snapshot(life, actor)
    source = _actor_source(life, actor)
    time = int(snapshot["last_clock"]) + 5 if as_of is None else int(as_of)
    effective = int(snapshot["last_clock"]) if event_time is None else int(event_time)
    return [make_conditioning_source(
        source_ref=TEST_ONLY_PREFIX + "MATERIAL_" + actor,
        source_class="ResolvedStructuralContext",
        subject=source.actor_id,
        body={
            "access": "granted",
            "as_of": effective,
            "scene": "workshop",
            "material_remaining": snapshot["state"].get("material_remaining"),
            "cash": snapshot["state"].get("cash"),
            "completed_units": snapshot["state"].get("completed_units"),
            "material_event_ref": life.material["event_id"],
            "source_grade": BP1_ACTOR_SOURCE_GRADE,
            "native_grant": BP1_NATIVE_GRANT,
        },
    )]


def _response_rule(actor_id: str):
    from candidate import ResponseRule
    return ResponseRule(
        "TEST_ONLY_BP1_CAN008_RULE_A",
        "1",
        digest({"test_only": "BP1_RULE_A", "native": False}),
        "TEST_ONLY_CAN008",
        "1",
        RESPONSE_ISSUER,
        True,
        (actor_id,),
        ("ResolvedStructuralContext",),
        "TEST_ONLY_SOURCEFREE_TECHNICAL",
        ("two distinct declared enacted acts", "independent other offer",
         "material access"),
    )


def _target_rule(rule):
    from candidate import TargetRule
    return TargetRule(
        "TEST_ONLY_BP1_CAN011_RULE_T",
        "1",
        rule.rule_content_hash,
        "TEST_ONLY_CAN011",
        "1",
        ISSUER,
        True,
        "V3MS_PRACTICE",
        ("CREATE",),
        ("c9p:coordinated_material_inspection",),
        "TEST_ONLY_SOURCEFREE_TECHNICAL",
    )


def _consumed_state(pipeline) -> str:
    """The exact committed later-read state hash consumed by E2."""
    return pipeline.later_read.state_hash


def _history_refs(life) -> tuple[str, ...]:
    refs = []
    for event in life.a_ledger.events:
        if event.kind in {"PRIOR_HISTORY", "PERFORMED_ACTION"}:
            refs.append(event.event_id)
    return tuple(refs)


def _response_hash(life, actor_id: str, event: dict, sources: list[dict],
                   as_of: int) -> str:
    from candidate import (
        ResponseRuleRegistry, bind_conditioning, evaluate_response, lookup_rule,
    )
    rule = _response_rule(actor_id)
    lookup = lookup_rule(
        ResponseRuleRegistry.test_only((rule,)),
        authority_id=rule.authority_id,
        rule_version=rule.rule_version,
        rule_content_hash=rule.rule_content_hash,
        subject=actor_id,
    )
    conditioning = bind_conditioning(subject=actor_id, sources=sources, as_of=as_of)
    material_ref = sources[0]["source_ref"]
    other_ref = life.b_ledger.performed_action_events[0].event_id
    response = evaluate_response(
        rule_lookup=lookup,
        event_ref=event["hash"],
        event_time=event["time"],
        subject=actor_id,
        conditioning_readset=conditioning.readset_refs,
        actor_history_refs=_history_refs(life),
        other_person_offer_ref=other_ref,
        material_opportunity_ref=material_ref,
        prior_response_count=0,
        material_eligible=True,
        eligible_material_refs=(material_ref,),
    )
    if not response.receipt_hash:
        raise BP1C9Refusal("RESPONSE_RECEIPT_MISSING")
    return response.receipt_hash


def run_bp1_c9(life, store, *, actor: str = "A",
               as_of: int | None = None,
               later_as_of: int | None = None) -> BP1C9Result:
    from candidate import (
        LaterActionConsumer, ResponseRuleRegistry, TargetRuleRegistry,
        make_target_permission,
    )
    from candidate.pipeline import run_candidate_path
    snapshot = _snapshot(life, actor)
    accepted, reason = verify_snapshot(
        snapshot, expected_hash=life.a_snapshot["hash"] if actor == "A" else
        life.b_snapshot["hash"])
    if not accepted:
        raise BP1C9Refusal("ACTOR_SNAPSHOT_NOT_AUTHENTICATED:" + str(reason))
    source = _actor_source(life, actor)
    event = build_c9_event(life, actor=actor)
    event_time = event["time"]
    time = event_time + 5 if as_of is None else int(as_of)
    if time < event_time:
        raise BP1C9Refusal("AS_OF_BEFORE_EVENT")
    sources = build_c9_conditioning(life, actor=actor, as_of=time,
                                    event_time=event_time)
    rule = _response_rule(source.actor_id)
    target_rule = _target_rule(rule)
    response_hash = _response_hash(life, source.actor_id, event, sources, time)
    permission = make_target_permission(
        grant_id="TEST_ONLY_BP1_GRANT",
        issuer_ref=ISSUER,
        actor_id=source.actor_id,
        rule_content_hash=rule.rule_content_hash,
        before_target_hash=store.target_state_hash(),
        response_hash=response_hash,
        issued_at=time - 1,
    )
    later = time + 10 if later_as_of is None else int(later_as_of)
    pipeline = run_candidate_path(
        store=store,
        actor_raw=build_c9_actor_record(life, actor=actor),
        event_raw=event,
        conditioning_sources=sources,
        response_registry=ResponseRuleRegistry.test_only((rule,)),
        target_registry=TargetRuleRegistry.test_only((target_rule,)),
        authority_id=rule.authority_id,
        rule_version=rule.rule_version,
        rule_content_hash=rule.rule_content_hash,
        as_of=time,
        permitted_issuer_refs=frozenset({ISSUER}),
        other_person_offer_ref=life.b_ledger.performed_action_events[0].event_id,
        material_opportunity_ref=sources[0]["source_ref"],
        enacted_history_refs=_history_refs(life),
        later_consumer=LaterActionConsumer(
            "TEST_ONLY_BP1_E2_READER", "committed_target_state"),
        later_as_of=later,
        target_permission=permission,
        action_owner_receipt=None,
        expected_act=EXPECTED_ACT,
    )
    committed = bool(pipeline.committed)
    state_hash = ""
    target_id = ""
    e2 = None
    if committed and pipeline.later_read is not None:
        from candidate import admit_performed_action, make_performed_action_receipt
        state_hash = _consumed_state(pipeline)
        target_id = pipeline.decision.target_id if pipeline.decision else ""
        receipt = make_performed_action_receipt(
            actor_id=source.actor_id,
            act=EXPECTED_ACT,
            actuator_ref=ACTUATOR,
            occurrence_ref=OCCURRENCE,
            action_time=later,
            consumed_state_hash=state_hash,
            target_commit_time=time,
        )
        e2 = admit_performed_action(
            owner_receipt=receipt,
            expected_actor_id=source.actor_id,
            expected_act=EXPECTED_ACT,
            consumed_state_hash=state_hash,
            as_of=later + 1,
            target_commit_time=time,
        )
    return BP1C9Result(
        life=life, actor=source,
        actor_record=build_c9_actor_record(life, actor=actor),
        event=event, conditioning=sources, rule=rule,
        target_rule=target_rule, permission=permission,
        response_hash=response_hash, pipeline=pipeline, e2=e2,
        committed=committed, state_hash=state_hash, target_id=target_id,
        commit_time=time, later_as_of=later,
    )
