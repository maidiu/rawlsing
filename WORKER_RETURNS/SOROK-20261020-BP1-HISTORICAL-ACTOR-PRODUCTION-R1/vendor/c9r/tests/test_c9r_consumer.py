"""C9R repaired direct consumer court: E1 -> RULE_A -> RULE_T -> exact persisted
record -> later independently performed E2 action, with falsifiable faults.

All identities and rules here are explicitly TEST_ONLY declared evidence. No
native actor, rule, target grant, ADP019 event or performed action is claimed.
"""
from __future__ import annotations

import sys
from dataclasses import replace
from pathlib import Path

import pytest

RET = Path(__file__).resolve().parents[1]
for path in (str(RET), str(RET / "runtime" / "native")):
    if path not in sys.path:
        sys.path.insert(0, path)

from candidate import (  # noqa: E402
    ActorIdentityRecord,
    CandidateStore,
    LaterActionConsumer,
    LaterActionStatus,
    ResponseRule,
    ResponseRuleRegistry,
    TargetBranch,
    TargetReason,
    TargetRule,
    TargetRuleRegistry,
    TransactionRefusal,
    admit_performed_action,
    bind_conditioning,
    digest,
    evaluate_release_gate,
    evaluate_response,
    evaluate_target,
    lookup_rule,
    make_conditioning_source,
    make_event_witness,
    make_performed_action_receipt,
    make_target_permission,
    read_target_for_later_action,
    seal,
)
from candidate.pipeline import run_candidate_path  # noqa: E402

A = "TEST_ONLY_C9R_A"
P = "TEST_ONLY_P"
ISSUER = "TEST_ONLY_C9R_TARGET_OWNER"
RESPONSE_ISSUER = "TEST_ONLY_C9R_RESPONSE_OWNER"
HISTORY = ("TEST_ONLY_ACT_H1", "TEST_ONLY_ACT_H2")
OFFER = "TEST_ONLY_P_OFFER"
MATERIAL = "TEST_ONLY_C9R_GARAGE"


def _actor():
    return ActorIdentityRecord(
        A, "ACTIVE", "STANDING_CURRENT", 10, "TEST_ONLY_ACTOR_SOURCE", "test-only-actor-digest"
    ).sealed()


def _event_ref():
    return _event()["hash"]


def _event():
    return make_event_witness(
        event_id="TEST_ONLY_E1",
        owner_ref="TEST_ONLY_EVENT_OWNER",
        time=15,
        content={"fact": "tool_offer", "scene": "garage", "participants": [A, P]},
        actor_role=A,
    )


def _sources():
    return [
        make_conditioning_source(
            source_ref=MATERIAL,
            source_class="ResolvedStructuralContext",
            subject=A,
            body={"tool": "wrench", "access": "granted", "as_of": 15, "scene": "garage"},
        )
    ]


def _rule():
    return ResponseRule(
        "TEST_ONLY_C9R_RULE_A",
        "1",
        digest({"test_only": "C9R_A_RULE"}),
        "TEST_ONLY_CAN008",
        "1",
        RESPONSE_ISSUER,
        True,
        (A,),
        ("ResolvedStructuralContext",),
        "TEST_ONLY_SOURCEFREE_TECHNICAL",
        ("two distinct declared enacted acts", "independent P offer", "material access"),
    )


def _target_rule(rule=None):
    rule = rule or _rule()
    return TargetRule(
        "TEST_ONLY_C9R_RULE_T",
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


def _response_receipt_hash(store):
    event = _event()
    rule = _rule()
    lookup = lookup_rule(
        ResponseRuleRegistry.test_only((rule,)),
        authority_id=rule.authority_id,
        rule_version=rule.rule_version,
        rule_content_hash=rule.rule_content_hash,
        subject=A,
    )
    conditioning = bind_conditioning(subject=A, sources=_sources(), as_of=20)
    response = evaluate_response(
        rule_lookup=lookup,
        event_ref=event["hash"],
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
    assert response.receipt_hash
    return response.receipt_hash


def _permission(store, *, response_hash):
    rule = _rule()
    return make_target_permission(
        grant_id="TEST_ONLY_C9R_GRANT",
        issuer_ref=ISSUER,
        actor_id=A,
        rule_content_hash=rule.rule_content_hash,
        before_target_hash=store.target_state_hash(),
        response_hash=response_hash,
        issued_at=10,
    )


def _run(store, *, action_receipt=None, history=HISTORY, material_eligible=None):
    rule = _rule()
    response_hash = _response_receipt_hash(store)
    permission = _permission(store, response_hash=response_hash)
    return run_candidate_path(
        store=store,
        actor_raw=_actor(),
        event_raw=_event(),
        conditioning_sources=_sources(),
        response_registry=ResponseRuleRegistry.test_only((rule,)),
        target_registry=TargetRuleRegistry.test_only((_target_rule(rule),)),
        authority_id=rule.authority_id,
        rule_version=rule.rule_version,
        rule_content_hash=rule.rule_content_hash,
        as_of=20,
        permitted_issuer_refs=frozenset({ISSUER}),
        other_person_offer_ref=OFFER,
        material_opportunity_ref=MATERIAL,
        enacted_history_refs=history,
        later_consumer=LaterActionConsumer("TEST_ONLY_C9R_E2_READER", "committed_target_state"),
        later_as_of=30,
        target_permission=permission,
        action_owner_receipt=action_receipt,
        expected_act="inspect_with_tool",
    )


def test_full_e1_to_e2_consumer_path(tmp_path):
    path = tmp_path / "consumer.sqlite"
    with CandidateStore(path) as store:
        first = _run(store)
        assert first.receipt.committed
        assert first.decision.branch is TargetBranch.CREATE
        target_id = first.decision.target_id
        committed = store.read_target_state(target_id)
        assert committed is not None
        assert committed.get("semantic_object_ref") == "c9p:coordinated_material_inspection"
        assert committed.get("effective_from") == 15
        assert _event_ref() in committed.get("causal_parent_refs", [])
        assert committed.get("record_hash") == first.decision.record_hash
        assert committed.get("permission_ref") == "TEST_ONLY_C9R_GRANT"
        preimage = committed.get("record_preimage")
        assert isinstance(preimage, dict)
        assert digest({k: v for k, v in preimage.items() if k != "hash"}) == committed.get("record_hash")
        assert first.receipt.authorization_hash == first.decision.authorization_hash
        assert first.later_read.status is LaterActionStatus.ACTION_ADMISSION_HELD
        assert first.later_read.committed_record == committed
        assert first.later_read.state_hash == digest(committed)
        receipt = make_performed_action_receipt(
            actor_id=A,
            act="inspect_with_tool",
            actuator_ref="TEST_ONLY_ACTUATOR_P",
            occurrence_ref="TEST_ONLY_OCCURRENCE_E2",
            action_time=25,
            consumed_state_hash=first.later_read.state_hash,
            target_commit_time=15,
        )
        admitted = admit_performed_action(
            owner_receipt=receipt,
            expected_actor_id=A,
            expected_act="inspect_with_tool",
            consumed_state_hash=first.later_read.state_hash,
            as_of=30,
            target_commit_time=15,
        )
        assert admitted.admitted
        assert admitted.actuator_ref == "TEST_ONLY_ACTUATOR_P"
        assert admitted.consumed_state_hash == first.later_read.state_hash
    with CandidateStore(path) as reopened:
        record = reopened.read_target_state(target_id)
        assert record == committed
        read = read_target_for_later_action(
            reopened,
            consumer=LaterActionConsumer("TEST_ONLY_C9R_E2_READER", "committed_target_state"),
            middle_state_id=target_id,
            as_of=30,
            commit_time=15,
            expected_actor_id=A,
        )
        assert read.status is LaterActionStatus.ACTION_ADMISSION_HELD
        assert read.state_hash == digest(committed)


def test_second_full_run_admits_independently_performed_e2(tmp_path):
    probe_path = tmp_path / "probe.sqlite"
    with CandidateStore(probe_path) as probe:
        probe_run = _run(probe)
        consumed = probe_run.later_read.state_hash
    receipt = make_performed_action_receipt(
        actor_id=A,
        act="inspect_with_tool",
        actuator_ref="TEST_ONLY_ACTUATOR_P",
        occurrence_ref="TEST_ONLY_OCCURRENCE_E2",
        action_time=25,
        consumed_state_hash=consumed,
        target_commit_time=15,
    )
    with CandidateStore(tmp_path / "full.sqlite") as store:
        result = _run(store, action_receipt=receipt)
        assert result.committed
        assert getattr(result.action_admission, "admitted", False)
        assert result.action_admission.consumed_state_hash == consumed
        assert result.later_read.state_hash == consumed


def test_valid_no_change_preserves_occurrence_and_creates_no_target(tmp_path):
    path = tmp_path / "nochange.sqlite"
    with CandidateStore(path) as store:
        result = _run(store, history=())
        assert result.committed
        assert result.decision.branch is TargetBranch.NO_CHANGE
        assert result.decision.reason is TargetReason.NO_PROPOSAL
        assert not store.committed_target_ids()
        assert _event_ref() in store.committed_event_hashes()
    with CandidateStore(path) as reopened:
        assert not reopened.committed_target_ids()
        assert _event_ref() in reopened.committed_event_hashes()


def test_removed_enacted_source_cannot_create(tmp_path):
    with CandidateStore(tmp_path / "removed.sqlite") as store:
        rule = _rule()
        response_hash = _response_receipt_hash(store)
        permission = _permission(store, response_hash=response_hash)
        lookup = lookup_rule(
            ResponseRuleRegistry.test_only((rule,)),
            authority_id=rule.authority_id,
            rule_version=rule.rule_version,
            rule_content_hash=rule.rule_content_hash,
            subject=A,
        )
        conditioning = bind_conditioning(subject=A, sources=_sources(), as_of=20)
        response = evaluate_response(
            rule_lookup=lookup,
            event_ref=_event_ref(),
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
        baseline = evaluate_target(
            registry=TargetRuleRegistry.test_only((_target_rule(rule),)),
            proposal=response.target_proposals[0],
            permission=permission,
            actor_id=A,
            before_target_hash=store.target_state_hash(),
            existing_target_ids=frozenset(),
            prior_event_hash=_event_ref(),
            as_of=20,
            enacted_history_refs=HISTORY,
            permitted_issuer_refs=frozenset({ISSUER}),
            response_hash=response_hash,
        )
        assert baseline.branch is TargetBranch.CREATE
        removed = evaluate_target(
            registry=TargetRuleRegistry.test_only((_target_rule(rule),)),
            proposal=response.target_proposals[0],
            permission=permission,
            actor_id=A,
            before_target_hash=store.target_state_hash(),
            existing_target_ids=frozenset(),
            prior_event_hash=_event_ref(),
            as_of=20,
            enacted_history_refs=(),
            permitted_issuer_refs=frozenset({ISSUER}),
            response_hash=response_hash,
        )
        assert removed.branch is TargetBranch.NO_CHANGE


def test_corrupt_target_preimage_is_refused(tmp_path):
    with CandidateStore(tmp_path / "corrupt.sqlite") as store:
        result = _run(store)
        assert result.receipt.committed
        decision = result.decision
        corrupted = dict(decision.record_body)
        corrupted["semantic_object_ref"] = "CORRUPTED-SEMANTIC-OBJECT"
        resealed = seal({k: v for k, v in corrupted.items() if k != "hash"})
        forged = replace(decision, record_body=resealed)
        store.admit_occurrence(_event())
        receipt = store.commit(
            event=_event(),
            response=seal(
                {
                    "event_ref": _event_ref(),
                    "receipt_hash": decision.response_hash,
                }
            ),
            decision=forged,
            readset_refs=decision.readset_refs,
        )
        assert not receipt.committed


def test_revoked_permission_between_proposal_and_commit_is_refused(tmp_path):
    with CandidateStore(tmp_path / "revoked_probe.sqlite") as probe:
        result = _run(probe)
        assert result.receipt.committed
        decision = result.decision
    with CandidateStore(tmp_path / "revoked.sqlite") as store:
        preimage = dict(decision.authorization_preimage)
        revoked_permission = seal(
            {
                **{k: v for k, v in preimage["permission"].items() if k != "hash"},
                "revoked": True,
            }
        )
        preimage["permission"] = revoked_permission
        resealed = seal({k: v for k, v in preimage.items() if k != "hash"})
        forged = replace(
            decision,
            authorization_preimage=resealed,
            authorization_hash=resealed["hash"],
        )
        store.admit_occurrence(_event())
        receipt = store.commit(
            event=_event(),
            response=seal(
                {
                    "event_ref": _event_ref(),
                    "receipt_hash": decision.response_hash,
                }
            ),
            decision=forged,
            readset_refs=decision.readset_refs,
        )
        assert not receipt.committed


def test_substituted_consumer_body_is_refused(tmp_path):
    with CandidateStore(tmp_path / "substituted.sqlite") as store:
        result = _run(store)
        target_id = result.decision.target_id

        class Substituted(LaterActionConsumer):
            def read_target(self, store, middle_state_id, as_of):
                real = store.read_target_state(middle_state_id)
                return {"actor_id": "TEST_ONLY_OTHER", "invented_practice": True}, digest(real)

        read = read_target_for_later_action(
            store,
            consumer=Substituted("TEST_ONLY_SUBSTITUTED", "committed_target_state"),
            middle_state_id=target_id,
            as_of=30,
            commit_time=15,
        )
        assert read.status is LaterActionStatus.CONSUMER_READSET_MISMATCH


def test_mismatched_performed_action_is_refused(tmp_path):
    consumed = "a" * 64
    receipt = make_performed_action_receipt(
        actor_id=A,
        act="inspect_with_tool",
        actuator_ref="TEST_ONLY_ACTUATOR_P",
        occurrence_ref="TEST_ONLY_OCCURRENCE_E2",
        action_time=25,
        consumed_state_hash="b" * 64,
        target_commit_time=15,
    )
    result = admit_performed_action(
        owner_receipt=receipt,
        expected_actor_id=A,
        expected_act="inspect_with_tool",
        consumed_state_hash=consumed,
        as_of=30,
        target_commit_time=15,
    )
    assert not getattr(result, "admitted", False)


def test_native_guard_denial_holds_native_positive_claim(tmp_path):
    with CandidateStore(tmp_path / "native.sqlite") as store:
        rule = _rule()
        response_hash = _response_receipt_hash(store)
        permission = _permission(store, response_hash=response_hash)
        result = run_candidate_path(
            store=store,
            actor_raw=_actor(),
            event_raw=_event(),
            conditioning_sources=_sources(),
            response_registry=ResponseRuleRegistry.test_only((rule,)),
            target_registry=TargetRuleRegistry.test_only((_target_rule(rule),)),
            authority_id=rule.authority_id,
            rule_version=rule.rule_version,
            rule_content_hash=rule.rule_content_hash,
            as_of=20,
            permitted_issuer_refs=frozenset({ISSUER}),
            other_person_offer_ref=OFFER,
            material_opportunity_ref=MATERIAL,
            enacted_history_refs=HISTORY,
            later_consumer=LaterActionConsumer("TEST_ONLY_C9R_E2_READER", "committed_target_state"),
            later_as_of=30,
            target_permission=permission,
            native_positive_claim=True,
        )
        assert 'DENY_ZERO_EFFECT' in result.conditioning.guard_outcome
        assert result.decision.branch is TargetBranch.DENY
        assert result.decision.reason is TargetReason.NATIVE_ADMISSIBILITY_HELD
        assert not store.committed_target_ids()
        assert evaluate_release_gate().held
        assert evaluate_release_gate(rule_a_issuer_verified=True).held


def test_test_only_publication_is_never_native_authority(tmp_path):
    with CandidateStore(tmp_path / "grade.sqlite") as store:
        result = _run(store)
        assert result.decision.publication_grade == "TEST_ONLY_SOURCEFREE_TECHNICAL"
        assert result.decision.record_body["native_admissibility"] == "HELD_UNISSUED"
        gate = evaluate_release_gate(
            rule_a_issuer_verified=True,
            rule_t_issuer_verified=True,
            adp019_witness_present=True,
            adp010_witness_present=True,
            positive_registry_entries=1,
            performed_action_owner_proved=True,
            later_action_consumer_bound=True,
        )
        assert gate.held
        assert "rule_a_issuer_verified" in gate.caller_supplied_booleans_ignored
