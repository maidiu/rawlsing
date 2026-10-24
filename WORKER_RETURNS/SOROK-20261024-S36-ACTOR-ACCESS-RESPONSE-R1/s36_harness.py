"""Shared TEST_ONLY harness for S36 S35 bridge vectors and evidence."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Mapping

RET = Path(__file__).resolve().parent
for path in (str(RET), str(RET / "runtime" / "native")):
    if path not in sys.path:
        sys.path.insert(0, path)

from candidate import (  # noqa: E402
    CandidateStore,
    ResponseRule,
    ResponseRuleRegistry,
    TargetRuleRegistry,
    bind_conditioning,
    digest,
    evaluate_response,
    lookup_rule,
    make_conditioning_source,
    make_event_witness,
    seal,
)
from candidate.actor_access_response import (  # noqa: E402
    S35ActorAccessRequest,
    make_actor_local_access_witness,
    make_actor_owned_response_witness,
)
from candidate.identity import ACTOR_RECORD_SCHEMA  # noqa: E402
from candidate.pipeline import run_candidate_path  # noqa: E402

A = "TEST_ONLY_S36_A"
B = "TEST_ONLY_S36_B"
ACTOR_SOURCE = "TEST_ONLY_S36_ACTOR_SOURCE"
EVENT_OWNER = "TEST_ONLY_S36_EVENT_OWNER"
ACCESS_SOURCE = "TEST_ONLY_ADP017_ACCESS_S36"
RESPONSE_SOURCE = "TEST_ONLY_A_RESPONSE_S36"
MATERIAL = "TEST_ONLY_S36_MATERIAL"
RESPONSE_ISSUER = "TEST_ONLY_S36_RESPONSE_OWNER"
RULE_AUTHORITY = "TEST_ONLY_S36_CAN008"
LEGACY_HISTORY = ("TEST_ONLY_S36_ACT_H1", "TEST_ONLY_S36_ACT_H2")
LEGACY_OFFER = "TEST_ONLY_S36_P_OFFER"

_AUTO = object()


def actor_record(labels: Mapping[str, Any] | None = None) -> dict:
    body = {
        "schema": ACTOR_RECORD_SCHEMA,
        "actor_id": A,
        "activation_status": "ACTIVE",
        "standing_state": "STANDING_CURRENT",
        "currentness_as_of": 10,
        "source_ref": ACTOR_SOURCE,
        "source_hash": "test-only-s36-actor-digest",
    }
    if labels:
        body.update(dict(labels))
    return seal(body)


def event_record(
    *,
    event_id: str = "TEST_ONLY_S36_E1",
    event_time: int = 15,
    b_act: str = "SHARE_TOOL",
    scene: str = "garage",
    extra_content: Mapping[str, Any] | None = None,
) -> dict:
    content = {
        "fact": "tool_offer",
        "scene": scene,
        "participants": [A, B],
        "b_act": b_act,
    }
    if extra_content:
        content.update(dict(extra_content))
    return make_event_witness(
        event_id=event_id,
        owner_ref=EVENT_OWNER,
        time=event_time,
        content=content,
        actor_role=A,
    )


def conditioning_sources(
    *, scene: str = "garage", as_of: int = 15, source_ref: str = MATERIAL
) -> list[dict]:
    return [
        make_conditioning_source(
            source_ref=source_ref,
            source_class="ResolvedStructuralContext",
            subject=A,
            body={"tool": "wrench", "access": "granted", "as_of": as_of, "scene": scene},
        )
    ]


def response_rule() -> ResponseRule:
    return ResponseRule(
        "TEST_ONLY_S36_CAN008_A",
        "1",
        digest({"test_only": "S36_S35_ACTOR_ACCESS_RESPONSE_RULE"}),
        RULE_AUTHORITY,
        "1",
        RESPONSE_ISSUER,
        True,
        (A,),
        ("ADP017_ACTOR_LOCAL_ACCESS", "A_ACTOR_PERFORMED_IMMEDIATE_RESPONSE"),
        "TEST_ONLY_SOURCEFREE_TECHNICAL",
        (
            "source_bound_actor_local_e1_access",
            "separately_witnessed_actor_owned_response",
            "zero_target_proposals",
        ),
    )


def legacy_rule() -> ResponseRule:
    return ResponseRule(
        "TEST_ONLY_S36_LEGACY_CAN008_A",
        "1",
        digest({"test_only": "S36_LEGACY_TWO_HISTORY_RULE"}),
        "TEST_ONLY_S36_LEGACY_CAN008",
        "1",
        "TEST_ONLY_S36_LEGACY_OWNER",
        True,
        (A,),
        ("ResolvedStructuralContext",),
        "TEST_ONLY_SOURCEFREE_TECHNICAL",
        ("two distinct declared enacted acts", "independent P offer", "material access"),
    )


def access_witness(event: Mapping[str, Any], **overrides: Any) -> dict:
    values = {
        "actor_id": A,
        "event_ref": event["hash"],
        "access_time": event["time"],
        "source_ref": ACCESS_SOURCE,
        "access_status": "ACCESSIBLE",
        "scene": event["content"]["scene"],
        "content": {"modality": "TEST_ONLY_ADP017_EXACT_E1_ACCESS"},
        "revoked": False,
    }
    values.update(overrides)
    return make_actor_local_access_witness(**values)


def response_witness(event: Mapping[str, Any], **overrides: Any) -> dict:
    values = {
        "actor_id": A,
        "event_ref": event["hash"],
        "response_ref": "TEST_ONLY_S36_A_REQUEST_TOOL",
        "response_kind": "REQUEST_TOOL",
        "response_time": event["time"] + 1,
        "source_ref": RESPONSE_SOURCE,
        "content": {"public_surface": "REQUEST_TOOL_WITHIN_CURRENT_MATERIAL_CONTEXT"},
        "revoked": False,
    }
    values.update(overrides)
    return make_actor_owned_response_witness(**values)


def reseal_with(record: Mapping[str, Any], **changes: Any) -> dict:
    body = {key: value for key, value in record.items() if key != "hash"}
    body.update(changes)
    return seal(body)


def run_s35_case(
    store: CandidateStore,
    *,
    event_id: str = "TEST_ONLY_S36_E1",
    event_time: int = 15,
    as_of: int = 20,
    b_act: str = "SHARE_TOOL",
    material: bool = True,
    access: Any = _AUTO,
    response: Any = _AUTO,
    access_kwargs: Mapping[str, Any] | None = None,
    response_kwargs: Mapping[str, Any] | None = None,
    contradictory_context: bool = False,
    contradictory_refs: tuple[str, ...] = (),
    revoked_source_refs: frozenset[str] = frozenset(),
    history: tuple[str, ...] = (),
    actor_labels: Mapping[str, Any] | None = None,
    target_registry: TargetRuleRegistry | None = None,
    target_permission: Mapping[str, Any] | None = None,
    permitted_issuer_refs: frozenset[str] = frozenset(),
    native_positive_claim: bool = False,
    later_consumer: Any = None,
) -> tuple[Any, dict]:
    event = event_record(
        event_id=event_id,
        event_time=event_time,
        b_act=b_act,
    )
    if access is _AUTO:
        access = access_witness(event, **(access_kwargs or {}))
    if response is _AUTO:
        response = response_witness(event, **(response_kwargs or {}))
    request = S35ActorAccessRequest(
        access_witness=access,
        response_witness=response,
        contradictory_context=contradictory_context,
        contradictory_refs=tuple(contradictory_refs),
        revoked_source_refs=frozenset(revoked_source_refs),
    )
    rule = response_rule()
    result = run_candidate_path(
        store=store,
        actor_raw=actor_record(actor_labels),
        event_raw=event,
        conditioning_sources=conditioning_sources() if material else [],
        response_registry=ResponseRuleRegistry.test_only((rule,)),
        target_registry=target_registry or TargetRuleRegistry.production(),
        authority_id=rule.authority_id,
        rule_version=rule.rule_version,
        rule_content_hash=rule.rule_content_hash,
        as_of=as_of,
        permitted_issuer_refs=permitted_issuer_refs,
        other_person_offer_ref="",
        material_opportunity_ref="",
        enacted_history_refs=tuple(history),
        later_consumer=later_consumer,
        later_as_of=as_of + 10,
        target_permission=target_permission,
        action_owner_receipt=None,
        expected_act="",
        native_positive_claim=native_positive_claim,
        s35_request=request,
    )
    return result, event


def committed_response(store: CandidateStore, response_ref: str) -> dict | None:
    row = store.db.execute(
        "SELECT body FROM response WHERE hash=?", (response_ref,)
    ).fetchone()
    return json.loads(row[0]) if row else None


def refusal_case(case: str):
    event = event_record()
    if case == "access_wrong_actor":
        return access_witness(event, actor_id="TEST_ONLY_S36_OTHER"), None, frozenset()
    if case == "access_wrong_event":
        return access_witness(event, event_ref="TEST_ONLY_S36_WRONG_EVENT"), None, frozenset()
    if case == "access_wrong_source_hash":
        tampered = reseal_with(
            access_witness(event), source_hash=digest({"tampered": "access"})
        )
        return tampered, None, frozenset()
    if case == "access_wrong_scene":
        return access_witness(event, scene="TEST_ONLY_OTHER_ROOM"), None, frozenset()
    if case == "access_before_event":
        return access_witness(event, access_time=event["time"] - 1), None, frozenset()
    if case == "access_after_as_of":
        return access_witness(event, access_time=21), None, frozenset()
    if case == "access_revoked_field":
        return access_witness(event, revoked=True), None, frozenset()
    if case == "access_revoked_source":
        return access_witness(event), None, frozenset({ACCESS_SOURCE})
    if case == "access_bad_namespace":
        return access_witness(event, source_ref="TEST_ONLY_OTHER_ACCESS"), None, frozenset()
    if case == "response_wrong_actor":
        return access_witness(event), response_witness(
            event, actor_id="TEST_ONLY_S36_OTHER"
        ), frozenset()
    if case == "response_wrong_event":
        return access_witness(event), response_witness(
            event, event_ref="TEST_ONLY_S36_WRONG_EVENT"
        ), frozenset()
    if case == "response_wrong_source_hash":
        tampered = reseal_with(
            response_witness(event), source_hash=digest({"tampered": "response"})
        )
        return access_witness(event), tampered, frozenset()
    if case == "response_before_access":
        return access_witness(event), response_witness(
            event, response_time=event["time"] - 1
        ), frozenset()
    if case == "response_after_as_of":
        return access_witness(event), response_witness(event, response_time=21), frozenset()
    if case == "response_revoked_field":
        return access_witness(event), response_witness(event, revoked=True), frozenset()
    if case == "response_revoked_source":
        return access_witness(event), response_witness(event), frozenset(
            {RESPONSE_SOURCE}
        )
    if case == "response_bad_kind":
        return access_witness(event), response_witness(
            event, response_kind="INFERRED_GRATITUDE"
        ), frozenset()
    if case == "response_bad_namespace":
        return access_witness(event), response_witness(
            event, source_ref="TEST_ONLY_OTHER_RESPONSE"
        ), frozenset()
    raise AssertionError(case)


def legacy_two_history_response():
    event = event_record(event_id="TEST_ONLY_S36_LEGACY_E1", event_time=15)
    rule = legacy_rule()
    lookup = lookup_rule(
        ResponseRuleRegistry.test_only((rule,)),
        authority_id=rule.authority_id,
        rule_version=rule.rule_version,
        rule_content_hash=rule.rule_content_hash,
        subject=A,
    )
    view = bind_conditioning(subject=A, sources=conditioning_sources(), as_of=20)
    return evaluate_response(
        rule_lookup=lookup,
        event_ref=event["hash"],
        event_time=15,
        subject=A,
        conditioning_readset=view.readset_refs,
        actor_history_refs=LEGACY_HISTORY,
        other_person_offer_ref=LEGACY_OFFER,
        material_opportunity_ref=MATERIAL,
        prior_response_count=0,
        material_eligible=True,
        eligible_material_refs=(MATERIAL,),
    ), event


__all__ = [
    "A",
    "ACCESS_SOURCE",
    "ACTOR_SOURCE",
    "B",
    "EVENT_OWNER",
    "LEGACY_HISTORY",
    "LEGACY_OFFER",
    "MATERIAL",
    "RESPONSE_ISSUER",
    "RESPONSE_SOURCE",
    "RET",
    "RULE_AUTHORITY",
    "access_witness",
    "actor_record",
    "committed_response",
    "conditioning_sources",
    "event_record",
    "legacy_rule",
    "legacy_two_history_response",
    "refusal_case",
    "reseal_with",
    "response_rule",
    "response_witness",
    "run_s35_case",
]
