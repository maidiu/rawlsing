"""C9R cold-process worker: build or inspect one candidate SQLite database.

Used only by the return's cold-replay driver in fresh interpreters. No native
authority and no external source are used.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
for path in (str(RET), str(RET / "runtime" / "native")):
    if path not in sys.path:
        sys.path.insert(0, path)

from candidate import (  # noqa: E402
    CandidateStore,
    LaterActionConsumer,
    LaterActionStatus,
    ResponseRule,
    ResponseRuleRegistry,
    TargetRule,
    TargetRuleRegistry,
    bind_conditioning,
    digest,
    evaluate_response,
    lookup_rule,
    make_conditioning_source,
    make_event_witness,
    make_target_permission,
    read_target_for_later_action,
)
from candidate.pipeline import run_candidate_path  # noqa: E402

A = "TEST_ONLY_C9R_A"
ISSUER = "TEST_ONLY_C9R_TARGET_OWNER"
HISTORY = ("TEST_ONLY_ACT_H1", "TEST_ONLY_ACT_H2")
OFFER = "TEST_ONLY_P_OFFER"
MATERIAL = "TEST_ONLY_C9R_GARAGE"


def actor():
    from candidate import ActorIdentityRecord

    return ActorIdentityRecord(
        A, "ACTIVE", "STANDING_CURRENT", 10, "TEST_ONLY_ACTOR_SOURCE", "test-only-actor-digest"
    ).sealed()


def event():
    return make_event_witness(
        event_id="TEST_ONLY_E1",
        owner_ref="TEST_ONLY_EVENT_OWNER",
        time=15,
        content={"fact": "tool_offer", "scene": "garage", "participants": [A, "TEST_ONLY_P"]},
        actor_role=A,
    )


def sources():
    return [
        make_conditioning_source(
            source_ref=MATERIAL,
            source_class="ResolvedStructuralContext",
            subject=A,
            body={"tool": "wrench", "access": "granted", "as_of": 15, "scene": "garage"},
        )
    ]


def rule():
    return ResponseRule(
        "TEST_ONLY_C9R_RULE_A",
        "1",
        digest({"test_only": "C9R_A_RULE"}),
        "TEST_ONLY_CAN008",
        "1",
        "TEST_ONLY_C9R_RESPONSE_OWNER",
        True,
        (A,),
        ("ResolvedStructuralContext",),
        "TEST_ONLY_SOURCEFREE_TECHNICAL",
        ("two distinct declared enacted acts", "independent P offer", "material access"),
    )


def target_rule(r):
    return TargetRule(
        "TEST_ONLY_C9R_RULE_T",
        "1",
        r.rule_content_hash,
        "TEST_ONLY_CAN011",
        "1",
        ISSUER,
        True,
        "V3MS_PRACTICE",
        ("CREATE",),
        ("c9p:coordinated_material_inspection",),
        "TEST_ONLY_SOURCEFREE_TECHNICAL",
    )


def logical_state(store):
    return store._logical_readset()


def build(path):
    with CandidateStore(path) as store:
        r = rule()
        lookup = lookup_rule(
            ResponseRuleRegistry.test_only((r,)),
            authority_id=r.authority_id,
            rule_version=r.rule_version,
            rule_content_hash=r.rule_content_hash,
            subject=A,
        )
        conditioning = bind_conditioning(subject=A, sources=sources(), as_of=20)
        response = evaluate_response(
            rule_lookup=lookup,
            event_ref=event()["hash"],
            event_time=15,
            subject=A,
            conditioning_readset=conditioning.readset_refs,
            actor_history_refs=HISTORY,
            other_person_offer_ref=OFFER,
            material_opportunity_ref=MATERIAL,
            prior_response_count=0,
            material_eligible=True,
            eligible_material_refs=(MATERIAL,),
        )
        permission = make_target_permission(
            grant_id="TEST_ONLY_C9R_GRANT",
            issuer_ref=ISSUER,
            actor_id=A,
            rule_content_hash=r.rule_content_hash,
            before_target_hash=store.target_state_hash(),
            response_hash=response.receipt_hash,
            issued_at=10,
        )
        result = run_candidate_path(
            store=store,
            actor_raw=actor(),
            event_raw=event(),
            conditioning_sources=sources(),
            response_registry=ResponseRuleRegistry.test_only((r,)),
            target_registry=TargetRuleRegistry.test_only((target_rule(r),)),
            authority_id=r.authority_id,
            rule_version=r.rule_version,
            rule_content_hash=r.rule_content_hash,
            as_of=20,
            permitted_issuer_refs=frozenset({ISSUER}),
            other_person_offer_ref=OFFER,
            material_opportunity_ref=MATERIAL,
            enacted_history_refs=HISTORY,
            later_consumer=LaterActionConsumer("TEST_ONLY_C9R_E2_READER", "committed_target_state"),
            later_as_of=30,
            target_permission=permission,
        )
        committed = store.read_target_state(result.decision.target_id)
        return {
            "committed": result.committed,
            "branch": result.decision.branch.value,
            "target_id": result.decision.target_id,
            "record_hash": result.decision.record_hash,
            "stored_state_hash": digest(committed),
            "stored_semantic_object_ref": committed.get("semantic_object_ref"),
            "logical_readset": logical_state(store),
            "receipt": result.receipt.receipt_hash,
        }


def inspect(path):
    with CandidateStore(path) as store:
        ids = sorted(store.committed_target_ids())
        records = {tid: store.read_target_state(tid) for tid in ids}
        reads = {}
        for tid in ids:
            read = read_target_for_later_action(
                store,
                consumer=LaterActionConsumer("TEST_ONLY_C9R_E2_READER", "committed_target_state"),
                middle_state_id=tid,
                as_of=30,
                commit_time=15,
                expected_actor_id=A,
            )
            reads[tid] = {
                "status": read.status.value,
                "state_hash": read.state_hash,
                "read_receipt": read.read_receipt_hash,
            }
        return {
            "logical_readset": logical_state(store),
            "records": records,
            "reads": reads,
            "integrity_check": store.db.execute("PRAGMA integrity_check").fetchone()[0],
        }


if __name__ == "__main__":
    mode, path = sys.argv[1], sys.argv[2]
    if mode == "build":
        print(json.dumps(build(path), sort_keys=True))
    elif mode == "inspect":
        print(json.dumps(inspect(path), sort_keys=True))
    else:
        raise SystemExit("UNKNOWN_MODE")
