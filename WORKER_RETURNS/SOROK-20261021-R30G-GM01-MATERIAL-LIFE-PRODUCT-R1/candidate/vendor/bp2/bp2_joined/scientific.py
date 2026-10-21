"""One finite PS0-D01-based CAN008/CAN011/ADP scientific-decision request.

This is a request, not an issued rule. It carries the exact finite trial the
joined producer actually executes, the two concrete competitor outcomes it
already distinguishes (CREATE versus lawful NO_CHANGE/DENY), the proposed-only
TEST_ONLY rule bodies with their content identities, the forbidden shortcuts,
and the exact competent owner decisions required to turn any of it into native
science.

It deliberately contains no trait, affect, need, practice-rate or developmental
coefficient. A role, seed, fixture or repeated test event cannot create acquired
human personality here.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from . import bootstrap

bootstrap.install()

from bp1.canon import digest  # noqa: E402

REQUEST_SCHEMA = "BP2_PS0_D01_SCIENTIFIC_DECISION_REQUEST@1"
PS0_COMMIT = "b1f8155338e6fae9fdca0fd11a810199ed12f3ca"
PS0_D01_SOURCE = (
    "WORKER_RETURNS/SOROK-20261019-PS0-INDEPENDENT-PERSON-SCIENCE-R1/"
    "05_PRECISE_SCIENTIFIC_DECISION_OWNER_DOCKET.md"
)
DECISION_OPTIONS = ("ADOPT", "REVISE", "REJECT", "REQUEST_EVIDENCE")

FORBIDDEN_SHORTCUTS = (
    "P psychology without a P source",
    "historical copy of one actor into a second actor",
    "actor knowability inferred from a structural source",
    "automatic trauma, trait, need or attachment coefficient",
    "narrator- or response-text-performed event",
    "production registry entry created by a fixture, hash or boolean",
    "future-child information influencing a present outcome",
    "two acts treated as a universal habit/practice law",
    "role, seed, stereotype or fixture identity as acquired personality",
)


def _rule_proposal(kind: str, semantics: Mapping[str, Any]) -> dict:
    return {
        "kind": kind,
        "status": "PROPOSED_ONLY_NOT_ISSUED",
        "test_only_semantics": dict(semantics),
        "test_only_content_hash": digest(dict(semantics)),
        "native_content_hash": None,
        "issuer_decision_required": True,
    }


def build_scientific_decision_request(
    *,
    run_receipt: Mapping[str, Any] | None = None,
    no_change_evidence: Mapping[str, Any] | None = None,
    deny_evidence: Mapping[str, Any] | None = None,
) -> dict:
    """Build the finite scientific-decision dossier."""
    from .producer import rule_a_semantics, target_semantics

    rule_a = rule_a_semantics("TEST_ONLY_BP1_ACTOR_A")
    rule_t = target_semantics(digest(rule_a))
    alternatives: dict[str, Any] = {
        "positive_create": {
            "status": "EXECUTED" if run_receipt else "DECLARED",
            "conditions": [
                "two distinct BP1 enacted acts",
                "an independent other-actor performed offer",
                "granted material access in the event scene",
                "separately granted CAN011 target update",
            ],
            "observed": _compact_run(run_receipt) if run_receipt else None,
        },
        "lawful_no_change": {
            "status": "EXECUTED" if no_change_evidence else "DECLARED",
            "conditions": [
                "insufficient distinct independently enacted history, or no "
                "eligible material source",
            ],
            "requirement": "occurrence preserved, no target row, no ghost state",
            "observed": dict(no_change_evidence) if no_change_evidence else None,
        },
        "lawful_deny": {
            "status": "EXECUTED" if deny_evidence else "DECLARED",
            "conditions": [
                "target permission revoked, or the target request is self-issued",
            ],
            "requirement": "DENY branch committed, no target row, occurrence kept",
            "observed": dict(deny_evidence) if deny_evidence else None,
        },
    }
    request = {
        "schema": REQUEST_SCHEMA,
        "request_id": "PS0-D01-BP2-RULE-A-T-REQUEST-R1",
        "status": "SCIENTIFIC_DECISION_REQUEST__NOT_AN_ISSUED_RULE",
        "based_on": {
            "ps0_commit": PS0_COMMIT,
            "ps0_document": PS0_D01_SOURCE,
            "ps0_trial": "PS0-D01",
            "p0_architecture": "4073ae2a3363d05e429e3be885486f094414b8ce",
            "pa0_atlas": "3b39c86b376efff8c11833b8451c1791adddb9bc",
        },
        "one_finite_trial": {
            "description": (
                "Same-world E1 occurrence -> persisted target -> an actual, "
                "independently performed later E2 action, with a source "
                "severance RED and a separate no-effect alternative GREEN."),
            "input": [
                "one committed BP3 C8 occurrence carrying two distinct BP1 "
                "actor/history identities and one shared material task",
                "the other actor's own performed offer (not the focal actor's)",
                "an externally issued concrete CAN008 RULE_A (this request asks "
                "for it; the TEST_ONLY body here is a placeholder)",
                "a separately owned concrete CAN011 RULE_T and grant (requested)",
                "an independently performed later E2 action owner receipt "
                "(requested)",
            ],
            "operation": [
                "actor ingress", "E1 event witness", "read-only conditioning",
                "RULE_A response", "RULE_T target evaluation",
                "atomic durable full-record commit", "later committed-state read",
                "independent E2 admission bound to the consumed state hash",
            ],
            "observable": [
                "target branch CREATE / NO_CHANGE / DENY",
                "target record hash and consumed state hash",
                "E2 admission or typed hold",
                "the six same-assertion source severances",
            ],
            "falsifiers": [
                "the named joined assertion fails when any one source edge is cut",
                "a fabricated response cannot create a durable target",
                "a self-performer cannot pass E2 admission",
                "no target row exists on NO_CHANGE or DENY",
            ],
        },
        "requested_new_scientific_rule_a": _rule_proposal("CAN008_RULE_A", rule_a),
        "requested_new_scientific_rule_t": _rule_proposal("CAN011_RULE_T", rule_t),
        "proposed_scope": {
            "semantic_object": "c9p:coordinated_material_inspection",
            "state_kind": "V3MS_PRACTICE",
            "subject_scope": "one exact actor id",
            "temporal_sufficiency": "not decided by this worker",
            "transfer_to_later_choice": "not decided by this worker",
            "valid_empty_condition": "insufficient declared enacted history",
        },
        "alternatives_considered": alternatives,
        "forbidden_shortcuts": list(FORBIDDEN_SHORTCUTS),
        "decision_options": list(DECISION_OPTIONS),
        "competent_owners": [
            {
                "owner": "CAN008 R2 concrete RULE_A issuing authority",
                "decision": (
                    "issue one exact rule body/version/content hash, subject and "
                    "readset scope, response alternatives and valid-empty "
                    "condition, with adoption provenance and effective time"),
                "current_state": "CAN008_RULE_ISSUER_UNVERIFIED__UNISSUED",
            },
            {
                "owner": "CAN011 separate target-state owner",
                "decision": (
                    "issue one exact RULE_T (kind, semantic object, operation, "
                    "state kind), plus a CREATE/NO_CHANGE/DENY grant with before "
                    "and write sets, expiry and revocation"),
                "current_state": "RULE_T_AND_GRANT_UNISSUED",
            },
            {
                "owner": "ADP019 V3 external admission court",
                "decision": "admit the exact precipitating occurrence and emit the owner receipt",
                "current_state": "ADP019_ADMISSION_RECEIPT_ABSENT",
            },
            {
                "owner": "ADP010 encounter owner",
                "decision": "bind AVAILABLE -> OPPORTUNITY -> ENCOUNTER for this exact subject",
                "current_state": "OPPORTUNITY_AND_ENCOUNTER_UNISSUED",
            },
            {
                "owner": "ADP007 actor genesis / ADP015 other-and-family owner",
                "decision": "issue the native actor and independent other source",
                "current_state": "TEST_ONLY_FIXTURE_ACTORS_NOT_NATIVE",
            },
            {
                "owner": "native later-action / actuator owner",
                "decision": "admit one independently performed E2 action after the commit",
                "current_state": "TEST_ONLY_DECLARED_ACTUATOR_NOT_NATIVE",
            },
            {
                "owner": "PSEPF production-registry binder",
                "decision": "populate the accepted production transition registry by owner action",
                "current_state": "PRODUCTION_REGISTRY_EMPTY",
            },
        ],
        "what_is_not_claimed": [
            "no native actor, person, parent, child or genealogy",
            "no native CAN008 RULE_A or CAN011 RULE_T",
            "no ADP010 encounter, ADP019 admission or native E2",
            "no psychology, personality, need, practice rate or universal coefficient",
            "no production install, KMS key or trusted anchor",
            "no L2 native-scientific or L3 user-product release",
        ],
        "evidence_grade": {
            "current": "L1_PHYSICALLY_EXECUTABLE_SOURCEFREE_TECHNICAL_POSITIVE",
            "target_after_owner_decisions": "L2_NATIVE_SCIENTIFIC_RELEASE",
            "this_worker_issues_none_of_the_above": True,
        },
    }
    request["request_hash"] = digest(request)
    return request


def _compact_run(receipt: Mapping[str, Any]) -> dict:
    keys = (
        "c8_occurrence_id", "c8_state_digest", "actor_id", "other_actor_id",
        "actor_source_hash", "other_source_hash", "rule_a_content_hash",
        "rule_t_content_hash", "grant_hash", "target_record_hash",
        "consumed_state_hash", "e2_actuator_ref", "e2_occurrence_ref",
        "e2_consumed_state_hash", "adp019_admission_receipt",
    )
    return {key: receipt.get(key) for key in keys}


def write_scientific_decision_request(path, **kwargs) -> dict:
    request = build_scientific_decision_request(**kwargs)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(request, indent=2, sort_keys=True) + "\n",
                      encoding="utf8")
    return request


__all__ = [
    "DECISION_OPTIONS",
    "FORBIDDEN_SHORTCUTS",
    "PS0_COMMIT",
    "PS0_D01_SOURCE",
    "REQUEST_SCHEMA",
    "build_scientific_decision_request",
    "write_scientific_decision_request",
]
