"""Bounded read-only JOIN-E x S35 compatibility evaluation.

The S35 selector is evaluated against the JOIN-E persisted source, E1 event,
C12 root/branch and clock. No S35 C9 store is created and the JOIN-E stores are
never mutated by this module.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any, Mapping

from candidate import (
    ResponseStatus,
    TargetBranch,
    TargetReason,
    TargetRuleRegistry,
    bind_conditioning,
    digest,
    eligible_material,
    evaluate_target,
    ingress_event,
    lookup_rule,
    make_conditioning_source,
)
from candidate.response_rules import ResponseRule, ResponseRuleRegistry

from . import access
from .access import (
    S35ActorAccessRequest,
    S35Context,
    S35_GRADE_CONTROLLED,
    S35_QUALIFICATION_CONTROLLED,
)
from .readback import read_c12

RULE_ID = "TEST_ONLY_S35_JOIN_E_CAN008_A"
RULE_AUTHORITY = "TEST_ONLY_S35_JOIN_E_A_AUTHORITY"
RULE_VERSION = "1"
RULE_CONTENT_HASH = digest(
    {"schema": "S35_JOIN_E_ACCESS_RESPONSE_RULE@1", "test_only": True}
)
RULE_ISSUER = "TEST_ONLY_S35_JOIN_E_RESPONSE_OWNER"


def source_material_access(source: Mapping[str, Any]) -> bool:
    return bool(
        source.get("b_performed") is True
        and source.get("b_operation") == "SHARE_TOOL"
        and int(source.get("b_quantity", 0)) >= 1
        and source.get("material_feasible_after") is True
    )


def operation_only_material_grant(source: Mapping[str, Any]) -> bool:
    return bool(
        source.get("b_operation") == "SHARE_TOOL"
        and int(source.get("b_quantity", 0)) >= 1
    )


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def store_hashes(bundle: Mapping[str, Any]) -> dict:
    paths = {
        "c9.sqlite": Path(bundle["c9_path"]),
        "c12.sqlite": Path(bundle["c12_path"]),
    }
    return {
        name: _sha256(path) if path.exists() else ""
        for name, path in paths.items()
    }


def read_c9_summary(bundle: Mapping[str, Any]) -> dict:
    path = Path(bundle["c9_path"])
    connection = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        occurrences = [
            (str(row[0]), json.loads(row[1]))
            for row in connection.execute(
                "SELECT hash, body FROM occurrence ORDER BY hash"
            )
        ]
        event_identity = [
            (str(row[0]), str(row[1]))
            for row in connection.execute(
                "SELECT event_id, hash FROM event_identity ORDER BY event_id"
            )
        ]
        target_rows = [
            (str(row[0]), json.loads(row[1]))
            for row in connection.execute(
                "SELECT id, body FROM target_state ORDER BY id"
            )
        ]
        clocks = [
            int(row[0])
            for row in connection.execute("SELECT clock FROM clock ORDER BY clock")
        ]
    finally:
        connection.close()
    target_hash = digest([body for _id, body in target_rows])
    return {
        "occurrences": occurrences,
        "event_identity": event_identity,
        "target_ids": [row[0] for row in target_rows],
        "target_state_hash": target_hash,
        "last_clock": max(clocks) if clocks else 0,
    }


def full_pipeline_incompatibility(bundle: Mapping[str, Any]) -> dict:
    c9 = read_c9_summary(bundle)
    actor_id = bundle["source_actor_map"]["TEST_ONLY_R31J_A"]
    event = bundle["e1_event"]
    ingress = ingress_event(
        event,
        as_of=int(bundle["c12"]["branch_clock"]),
        last_time=int(c9["last_clock"]),
        prior_event_hashes=frozenset(row[0] for row in c9["occurrences"]),
        focal_actor_id=actor_id,
    )
    return {
        "event_time": int(bundle["event_time"]),
        "c9_last_clock": int(c9["last_clock"]),
        "c12_branch_clock": int(bundle["c12"]["branch_clock"]),
        "event_time_gt_c12_clock": int(bundle["event_time"])
        > int(bundle["c12"]["branch_clock"]),
        "event_already_admitted": any(
            row[1] == bundle["e1_event_hash"] for row in c9["event_identity"]
        ),
        "ingress_status": ingress.status.value,
        "ingress_reason": ingress.reason.value,
        "same_root_c9_reexecution_lawful": ingress.admitted,
    }


def build_context(bundle: Mapping[str, Any]) -> dict:
    c12 = read_c12(bundle["c12_path"])
    branch_id = bundle["branch_id"]
    branch = c12["branches"][branch_id]
    root_branch = c12["branches"]["root"]
    root_state = c12["checkpoints"]["root"][-1]
    actor_id = bundle["source_actor_map"]["TEST_ONLY_R31J_A"]
    context = S35Context(
        actor_id=actor_id,
        event_ref=bundle["e1_event_hash"],
        event_id=bundle["event_id"],
        event_time=int(bundle["event_time"]),
        as_of=int(c12["last_clock"].get(branch_id, 0)),
        scene=str(bundle["scene"]),
        root_id=str(root_branch["branch_id"]),
        root_branch_hash=digest(root_branch),
        root_state_hash=str(root_state["hash"]),
        branch_id=branch_id,
        branch_hash=digest(branch),
        branch_parent_id=str(branch["parent_branch_id"]),
        branch_fork_clock=int(branch["fork_clock"]),
        clock=int(c12["last_clock"].get(branch_id, 0)),
        material_eligible=False,
        eligible_material_refs=(),
    )
    actor_snapshot = bundle["actor_snapshot"]
    access_granted = source_material_access(bundle["source"])
    conditioning_source = make_conditioning_source(
        source_ref="TEST_ONLY_S35_JOIN_E_MATERIAL_A",
        source_class="ResolvedStructuralContext",
        subject=actor_id,
        body={
            "access": "granted" if access_granted else "denied",
            "as_of": int(bundle["event_time"]),
            "scene": str(bundle["scene"]),
            "material_remaining": actor_snapshot["state"].get("material_remaining"),
            "material_ref": bundle["source"].get("b_event_hash"),
            "material_feasible_after": bundle["source"].get(
                "material_feasible_after"
            ),
            "source_grade": "TEST_ONLY_SOURCEFREE_JOIN_E_NOT_NATIVE",
            "native_grant": False,
        },
    )
    conditioning = bind_conditioning(
        subject=actor_id,
        sources=[conditioning_source],
        as_of=context.clock,
    )
    material_ok, material_refs, material_reason = eligible_material(
        conditioning,
        event_scene=context.scene,
        event_time=context.event_time,
        as_of=context.clock,
    )
    context = S35Context(
        **{
            **context.as_dict(),
            "material_eligible": material_ok,
            "eligible_material_refs": tuple(material_refs),
        }
    )
    return {
        "context": context,
        "conditioning": conditioning,
        "conditioning_source": conditioning_source,
        "material_eligible": material_ok,
        "material_refs": tuple(material_refs),
        "material_reason": material_reason,
        "access_granted": access_granted,
    }


def make_rule(actor_id: str) -> ResponseRule:
    return ResponseRule(
        RULE_ID,
        RULE_VERSION,
        RULE_CONTENT_HASH,
        RULE_AUTHORITY,
        "1",
        RULE_ISSUER,
        True,
        (actor_id,),
        (access.S35_ACCESS_SOURCE_CLASS, access.S35_ACTION_SOURCE_CLASS),
        "TEST_ONLY_SOURCEFREE_TECHNICAL",
        (
            "join_e_source_binding",
            "a_local_perception_receipt",
            "a_owned_action_occurrence_receipt",
            "zero_target_proposals",
        ),
    )


def evaluate(
    bundle: Mapping[str, Any],
    *,
    controlled: bool = False,
    perception_status: str = "ACCESSIBLE",
    action_kind: str = "REQUEST_TOOL",
    action_present: bool = True,
) -> dict:
    built = build_context(bundle)
    context = built["context"]
    rule = make_rule(context.actor_id)
    registry = ResponseRuleRegistry.test_only((rule,))
    lookup = lookup_rule(
        registry,
        authority_id=rule.authority_id,
        rule_version=rule.rule_version,
        rule_content_hash=rule.rule_content_hash,
        subject=context.actor_id,
    )
    if controlled:
        perception = access.make_a_local_perception_receipt(
            context=context,
            source_ref="TEST_ONLY_ADP017_ACCESS_S35_A_LOCAL_PERCEPTION",
            perception_ref="TEST_ONLY_JOIN_E_PERCEPTION_" + perception_status,
            access_status=perception_status,
            perceived_at=context.event_time,
            scene=context.scene,
            content={
                "join_e_state_root": bundle["state_root"],
                "join_e_disposition": bundle["disposition"],
            },
            evidence_grade=S35_GRADE_CONTROLLED,
            actual_actor_input=False,
            qualification=S35_QUALIFICATION_CONTROLLED,
        )
        action = None
        if action_present:
            action = access.make_a_owned_action_receipt(
                context=context,
                source_ref="TEST_ONLY_A_ACTION_S35_A_OWNED",
                action_ref="TEST_ONLY_JOIN_E_ACTION_" + action_kind,
                action_kind=action_kind,
                performed=True,
                action_time=context.event_time + 1,
                content={
                    "join_e_state_root": bundle["state_root"],
                    "join_e_disposition": bundle["disposition"],
                },
                evidence_grade=S35_GRADE_CONTROLLED,
                actual_actor_input=False,
                qualification=S35_QUALIFICATION_CONTROLLED,
            )
    else:
        perception = None
        action = None
    request = S35ActorAccessRequest(
        perception_receipt=perception,
        action_receipt=action,
    )
    evaluation = access.evaluate_actor_access_response(
        rule_lookup=lookup,
        event_ref=context.event_ref,
        event_time=context.event_time,
        subject=context.actor_id,
        request=request,
        conditioning_readset=built["conditioning"].readset_refs,
        context=context,
        as_of=context.clock,
        material_eligible=built["material_eligible"],
        eligible_material_refs=built["material_refs"],
    )
    c9 = read_c9_summary(bundle)
    decision = evaluate_target(
        registry=TargetRuleRegistry.production(),
        proposal=None,
        permission=None,
        actor_id=context.actor_id,
        before_target_hash=c9["target_state_hash"],
        existing_target_ids=frozenset(c9["target_ids"]),
        prior_event_hash=context.event_ref,
        as_of=context.clock,
        enacted_history_refs=(),
        permitted_issuer_refs=frozenset(),
        response_hash=evaluation.response.receipt_hash,
    )
    return {
        "context": context,
        "built": built,
        "evaluation": evaluation,
        "decision": decision,
        "c9": c9,
        "operation_only_material_grant": operation_only_material_grant(
            bundle["source"]
        ),
    }


def summary(result: Mapping[str, Any]) -> dict:
    evaluation = result["evaluation"]
    decision = result["decision"]
    receipt = evaluation.receipt or {}
    return {
        "outcome": evaluation.response.reason,
        "response_status": evaluation.response.status.value,
        "target_proposals": len(evaluation.response.target_proposals),
        "target_branch": decision.branch.value,
        "target_reason": decision.reason.value,
        "target_id": decision.target_id,
        "s35_receipt_hash": receipt.get("hash", ""),
        "evidence_grade": receipt.get("evidence_grade", ""),
        "actual_actor_input": receipt.get("actual_actor_input"),
        "qualification": receipt.get("qualification", ""),
        "hold_reason": receipt.get("hold_reason", ""),
        "event_time": result["context"].event_time,
        "clock": result["context"].clock,
        "material_eligible": result["built"]["material_eligible"],
        "material_refs": list(result["built"]["material_refs"]),
        "material_reason": result["built"]["material_reason"],
        "access_granted": result["built"]["access_granted"],
        "operation_only_material_grant": result["operation_only_material_grant"],
    }


__all__ = [
    "build_context",
    "evaluate",
    "full_pipeline_incompatibility",
    "make_rule",
    "operation_only_material_grant",
    "read_c9_summary",
    "source_material_access",
    "store_hashes",
    "summary",
]
