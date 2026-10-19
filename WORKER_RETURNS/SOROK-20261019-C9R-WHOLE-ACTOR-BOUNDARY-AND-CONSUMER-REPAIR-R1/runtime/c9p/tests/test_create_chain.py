"""TEST_ONLY technical CREATE chain through the full pipeline with typed permission.

This exercises the complete candidate transport with an explicitly typed
TEST_ONLY permission. The release gate stays `C9_NATIVE_POSITIVE_HELD` regardless.
The label is `EXECUTED_GREEN__TEST_ONLY_TECHNICAL`, never `NATIVE_C9_POSITIVE`.
"""
from __future__ import annotations

from conftest import (
    ACTOR_ID,
    TEST_ONLY_TARGET_ISSUER,
    build_actor_record,
    build_conditioning_sources,
    build_event_witness,
    build_response_rule,
    build_target_rule,
)
from candidate.later_action import LaterActionConsumer, LaterActionStatus
from candidate.pipeline import run_candidate_path
from candidate.release_gate import ReleaseOutcome, evaluate_release_gate
from candidate.response_rules import ResponseRuleRegistry, ResponseStatus
from candidate.target_rules import TargetBranch, TargetRuleRegistry, make_target_permission
from candidate.transaction import CandidateStore


def test_test_only_full_create_chain_commits_target_and_reads_it(tmp_path) -> None:
    store = CandidateStore(tmp_path / "store.sqlite")
    rule = build_response_rule()
    target_registry = TargetRuleRegistry.test_only((build_target_rule(rule.rule_content_hash),))
    before_hash = store.target_state_hash()
    permission = make_target_permission(
        grant_id="TEST_ONLY_GRANT_CREATE_001",
        issuer_ref=TEST_ONLY_TARGET_ISSUER,
        actor_id=ACTOR_ID,
        rule_content_hash=rule.rule_content_hash,
        before_target_hash=before_hash,
        response_hash="",
        issued_at=10,
    )
    consumer = LaterActionConsumer(
        consumer_id="TEST_ONLY_LATER_ACTION_CONSUMER",
        expected_surface="committed_target_state",
    )
    result = run_candidate_path(
        store=store,
        actor_raw=build_actor_record(),
        event_raw=build_event_witness(),
        conditioning_sources=build_conditioning_sources(),
        response_registry=ResponseRuleRegistry.test_only((rule,)),
        target_registry=target_registry,
        authority_id=rule.authority_id,
        rule_version=rule.rule_version,
        rule_content_hash=rule.rule_content_hash,
        as_of=20,
        permitted_issuer_refs=frozenset({TEST_ONLY_TARGET_ISSUER}),
        other_person_offer_ref="TEST_ONLY_OFFER_LENT_WRENCH",
        material_opportunity_ref="TEST_ONLY_WORLD_GARAGE",
        enacted_history_refs=("TEST_ONLY_ENACTED_H_A", "TEST_ONLY_ENACTED_H_B"),
        later_consumer=consumer,
        later_as_of=30,
        target_permission=permission,
        expected_act="inspect_with_tool",
    )
    assert result.committed is True
    assert result.response is not None
    assert result.response.status is ResponseStatus.RESPONSE_COMMITTED
    assert result.decision is not None
    assert result.decision.branch is TargetBranch.CREATE, result.decision.reason.value
    assert result.decision.record_hash
    assert result.later_read is not None
    assert result.later_read.status is LaterActionStatus.ACTION_ADMISSION_HELD
    assert result.later_read.committed_record is not None
    assert result.later_read.state_hash
    gate = evaluate_release_gate()
    assert gate.outcome is ReleaseOutcome.C9_NATIVE_POSITIVE_HELD
    store.close()


def test_test_only_create_chain_survives_cold_reopen(tmp_path) -> None:
    path = tmp_path / "store.sqlite"
    rule = build_response_rule()
    target_registry = TargetRuleRegistry.test_only((build_target_rule(rule.rule_content_hash),))
    store = CandidateStore(path)
    before_hash = store.target_state_hash()
    permission = make_target_permission(
        grant_id="TEST_ONLY_GRANT_CREATE_002",
        issuer_ref=TEST_ONLY_TARGET_ISSUER,
        actor_id=ACTOR_ID,
        rule_content_hash=rule.rule_content_hash,
        before_target_hash=before_hash,
        response_hash="",
        issued_at=10,
    )
    consumer = LaterActionConsumer(
        consumer_id="TEST_ONLY_LATER_ACTION_CONSUMER",
        expected_surface="committed_target_state",
    )
    result = run_candidate_path(
        store=store,
        actor_raw=build_actor_record(),
        event_raw=build_event_witness(),
        conditioning_sources=build_conditioning_sources(),
        response_registry=ResponseRuleRegistry.test_only((rule,)),
        target_registry=target_registry,
        authority_id=rule.authority_id,
        rule_version=rule.rule_version,
        rule_content_hash=rule.rule_content_hash,
        as_of=20,
        permitted_issuer_refs=frozenset({TEST_ONLY_TARGET_ISSUER}),
        other_person_offer_ref="TEST_ONLY_OFFER_LENT_WRENCH",
        material_opportunity_ref="TEST_ONLY_WORLD_GARAGE",
        enacted_history_refs=("TEST_ONLY_ENACTED_H_A", "TEST_ONLY_ENACTED_H_B"),
        later_consumer=consumer,
        later_as_of=30,
        target_permission=permission,
    )
    assert result.decision is not None
    committed_id = result.decision.proposal_hash
    store.close()
    reopened = CandidateStore(path)
    record = reopened.read_target_state(committed_id)
    assert record is not None, "cold reopen must find the committed target record"
    assert record["record_hash"] == result.decision.record_hash
    from candidate.later_action import read_target_for_later_action

    cold_read = read_target_for_later_action(
        reopened,
        consumer=consumer,
        middle_state_id=committed_id,
        as_of=35,
        commit_time=15,
        action_admission_owner_ref="TEST_ONLY_ACTUATOR",
    )
    assert cold_read.status is LaterActionStatus.READ_OK
    assert cold_read.committed_record is not None
    reopened.close()
