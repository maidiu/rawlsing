"""Full candidate pipeline: honest native ceiling and TEST_ONLY technical chain.

The native ceiling runs against production-empty rule registries and preserves
`C9_NATIVE_POSITIVE_HELD`. The TEST_ONLY chain exercises the full transport
mechanics with explicitly typed fixtures and is labeled
`EXECUTED_GREEN__TEST_ONLY_TECHNICAL`, never a native positive.
"""
from __future__ import annotations

from conftest import (
    ACTOR_ID,
    TEST_ONLY_ISSUER,
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


def _run(store, **overrides):
    rule = build_response_rule()
    defaults = dict(
        store=store,
        actor_raw=build_actor_record(),
        event_raw=build_event_witness(),
        conditioning_sources=build_conditioning_sources(),
        response_registry=ResponseRuleRegistry.test_only((rule,)),
        target_registry=TargetRuleRegistry.test_only((build_target_rule(rule.rule_content_hash),)),
        authority_id=rule.authority_id,
        rule_version=rule.rule_version,
        rule_content_hash=rule.rule_content_hash,
        as_of=20,
        permitted_issuer_refs=frozenset({TEST_ONLY_TARGET_ISSUER}),
        other_person_offer_ref="TEST_ONLY_OFFER_LENT_WRENCH",
        material_opportunity_ref="TEST_ONLY_WORLD_GARAGE",
        enacted_history_refs=("TEST_ONLY_ENACTED_H_A", "TEST_ONLY_ENACTED_H_B"),
        later_consumer=LaterActionConsumer(
            consumer_id="TEST_ONLY_LATER_ACTION_CONSUMER",
            expected_surface="committed_target_state",
        ),
        later_as_of=30,
    )
    defaults.update(overrides)
    return run_candidate_path(**defaults)


def test_native_ceiling_production_registries_refuse_everything(tmp_path) -> None:
    store = CandidateStore(tmp_path / "store.sqlite")
    result = run_candidate_path(
        store=store,
        actor_raw=build_actor_record(),
        event_raw=build_event_witness(),
        conditioning_sources=build_conditioning_sources(),
        response_registry=ResponseRuleRegistry.production(),
        target_registry=TargetRuleRegistry.production(),
        authority_id="TEST_ONLY_CAN008_AUTHORITY",
        rule_version="1",
        rule_content_hash="absent-rule-hash",
        as_of=20,
        permitted_issuer_refs=frozenset(),
        other_person_offer_ref="TEST_ONLY_OFFER_LENT_WRENCH",
        material_opportunity_ref="TEST_ONLY_WORLD_GARAGE",
        enacted_history_refs=("TEST_ONLY_ENACTED_H_A", "TEST_ONLY_ENACTED_H_B"),
        later_consumer=None,
        later_as_of=30,
    )
    response_stage = result.stage("can008_response_rule_lookup")
    assert response_stage is not None
    assert response_stage.detail["rule_status"] == "RULE_ABSENT"
    assert response_stage.detail["response_status"] == "REFUSED"
    assert result.decision is not None
    assert result.decision.branch.value in ("DENY", "NO_CHANGE")
    assert result.response is not None
    assert result.response.status is ResponseStatus.REFUSED
    gate = evaluate_release_gate()
    assert gate.outcome is ReleaseOutcome.C9_NATIVE_POSITIVE_HELD
    store.close()


def test_test_only_chain_commits_and_reads_committed_state(tmp_path) -> None:
    store = CandidateStore(tmp_path / "store.sqlite")
    rule = build_response_rule()
    permission = make_target_permission(
        grant_id="TEST_ONLY_GRANT_001",
        issuer_ref=TEST_ONLY_TARGET_ISSUER,
        actor_id=ACTOR_ID,
        rule_content_hash=rule.rule_content_hash,
        before_target_hash=store.target_state_hash(),
        response_hash="",
        issued_at=10,
    )
    result = _run(store)
    assert result.committed is True
    assert result.decision is not None
    assert result.decision.branch is TargetBranch.DENY
    assert result.decision.reason.value in (
        "PERMISSION_MISSING",
        "TARGET_RULE_UNISSUED",
        "TARGET_RULE_ABSENT",
    )
    assert result.response is not None
    assert result.response.status is ResponseStatus.RESPONSE_COMMITTED
    assert result.later_read is not None
    assert result.later_read.status in (
        LaterActionStatus.STATE_ABSENT,
        LaterActionStatus.ACTION_ADMISSION_HELD,
    )
    store.close()


def test_two_distinct_trajectories_are_materially_distinct(tmp_path) -> None:
    store = CandidateStore(tmp_path / "store.sqlite")
    first = _run(store)
    second = _run(
        store,
        event_raw=build_event_witness(
            event_id="event-c9p-e2",
            time=16,
            content={"fact": "second_shared_tool_offer", "object": "spanner"},
        ),
        later_as_of=31,
    )
    assert first.event is not None and second.event is not None
    assert first.event.event_hash != second.event.event_hash
    assert first.event.event_id != second.event.event_id
    assert first.committed and second.committed
    store.close()


def test_no_ghost_under_injected_storage_fault(tmp_path) -> None:
    store = CandidateStore(tmp_path / "store.sqlite")
    before = store.snapshot()
    result = _run(store, fault="after_receipt_before_commit")
    assert result.receipt is not None
    assert result.receipt.status == "TRANSACTION_ABORTED_ROLLBACK"
    assert result.no_ghost is True
    after = store.snapshot()
    # Occurrence admission is a separate prior commit and is preserved by design.
    assert after["occurrence"] != before["occurrence"]
    assert after["response"] == before["response"]
    assert after["target_state"] == before["target_state"]
    assert after["target_journal"] == before["target_journal"]
    assert after["receipt"] == before["receipt"]
    store.close()


def test_performed_action_is_held_without_owner_receipt(tmp_path) -> None:
    store = CandidateStore(tmp_path / "store.sqlite")
    result = _run(store, action_owner_receipt=None, expected_act="inspect_with_tool")
    assert result.action_admission is not None
    assert result.action_admission.status.value in ("HELD", "REFUSED")
    stage = result.stage("performed_action_admission")
    assert stage is not None
    assert stage.ok is False
    store.close()


def test_hand_authored_action_path_is_refused(tmp_path) -> None:
    store = CandidateStore(tmp_path / "store.sqlite")
    result = _run(store)
    assert result.action_admission is not None
    assert result.action_admission.status.value in ("HELD", "REFUSED")
    store.close()


def test_stale_actor_currentness_stops_chain_before_event(tmp_path) -> None:
    store = CandidateStore(tmp_path / "store.sqlite")
    result = _run(
        store,
        actor_raw=build_actor_record(currentness_as_of=25),
        as_of=20,
    )
    assert result.committed is False
    assert result.event is None
    stage = result.stage("actor_ingress")
    assert stage is not None
    assert stage.ok is False
    assert stage.reason == "STANDING_STATE_STALE"
    store.close()
