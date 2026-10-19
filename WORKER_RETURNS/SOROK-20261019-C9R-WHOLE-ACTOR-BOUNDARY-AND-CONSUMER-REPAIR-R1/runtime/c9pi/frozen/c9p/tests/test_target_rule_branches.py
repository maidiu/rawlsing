"""(e) CAN011 target rule, permission and CREATE / NO_CHANGE / DENY branch tests."""
from __future__ import annotations

from conftest import (
    ACTOR_ID,
    TEST_ONLY_TARGET_ISSUER,
    build_response_rule,
    build_target_rule,
)
from candidate.canon import seal
from candidate.response_rules import ResponseRuleRegistry, evaluate_response, lookup_rule
from candidate.target_rules import (
    TargetBranch,
    TargetReason,
    TargetRuleRegistry,
    evaluate_target,
    make_target_permission,
)

EVENT_HASH = "event-hash-e1"


def _proposal(rule_hash: str, event_hash: str = EVENT_HASH) -> dict:
    return seal(
        {
            "schema": "C9P_TARGET_PROPOSAL@1",
            "actor_id": ACTOR_ID,
            "state_kind_id": "V3MS_PRACTICE",
            "operation": "CREATE",
            "proposed_effective_time": 15,
            "semantic_object_ref": "c9p:coordinated_material_inspection",
            "target_refs": ["c9p:practice"],
            "causal_parent_refs": [event_hash, "h-a", "h-b"],
            "source_update_rule_ref": rule_hash,
            "evaluator_receipts": ["src-1"],
            "numeric_rule_ref": None,
            "stochastic_receipt_ref": None,
        }
    )


def _decision(registry, proposal, permission, **kwargs):
    defaults = dict(
        registry=registry,
        proposal=proposal,
        permission=permission,
        actor_id=ACTOR_ID,
        before_target_hash="before-hash",
        existing_target_ids=frozenset(),
        prior_event_hash=EVENT_HASH,
        as_of=20,
        enacted_history_refs=("h-a", "h-b"),
        permitted_issuer_refs=frozenset({TEST_ONLY_TARGET_ISSUER}),
    )
    defaults.update(kwargs)
    return evaluate_target(**defaults)


def test_production_registry_denies_target_rule_absent() -> None:
    rule = build_response_rule()
    decision = _decision(
        TargetRuleRegistry.production(), _proposal(rule.rule_content_hash), None
    )
    assert decision.branch is TargetBranch.DENY
    assert decision.reason is TargetReason.TARGET_RULE_ABSENT
    assert decision.record_hash == ""


def test_self_issued_permission_is_denied() -> None:
    rule = build_response_rule()
    registry = TargetRuleRegistry.test_only((build_target_rule(rule.rule_content_hash),))
    decision = _decision(
        registry,
        _proposal(rule.rule_content_hash),
        None,
        request_is_self_issued=True,
    )
    assert decision.branch is TargetBranch.DENY
    assert decision.reason is TargetReason.PERMISSION_SELF_ISSUED


def test_missing_permission_is_denied() -> None:
    rule = build_response_rule()
    registry = TargetRuleRegistry.test_only((build_target_rule(rule.rule_content_hash),))
    decision = _decision(registry, _proposal(rule.rule_content_hash), None)
    assert decision.branch is TargetBranch.DENY
    assert decision.reason is TargetReason.PERMISSION_MISSING


def test_foreign_owner_permission_is_denied() -> None:
    rule = build_response_rule()
    registry = TargetRuleRegistry.test_only((build_target_rule(rule.rule_content_hash),))
    permission = make_target_permission(
        grant_id="g1",
        issuer_ref="FOREIGN_ISSUER",
        actor_id=ACTOR_ID,
        rule_content_hash=rule.rule_content_hash,
        before_target_hash="before-hash",
        response_hash="r1",
        issued_at=10,
    )
    decision = _decision(
        registry,
        _proposal(rule.rule_content_hash),
        permission,
    )
    assert decision.branch is TargetBranch.DENY
    assert decision.reason is TargetReason.PERMISSION_FOREIGN_OWNER


def test_revoked_permission_is_denied() -> None:
    rule = build_response_rule()
    registry = TargetRuleRegistry.test_only((build_target_rule(rule.rule_content_hash),))
    permission = make_target_permission(
        grant_id="g1",
        issuer_ref=TEST_ONLY_TARGET_ISSUER,
        actor_id=ACTOR_ID,
        rule_content_hash=rule.rule_content_hash,
        before_target_hash="before-hash",
        response_hash="r1",
        issued_at=10,
        revoked=True,
    )
    decision = _decision(
        registry,
        _proposal(rule.rule_content_hash),
        permission,
    )
    assert decision.branch is TargetBranch.DENY
    assert decision.reason is TargetReason.PERMISSION_REVOKED


def test_expired_permission_is_denied() -> None:
    rule = build_response_rule()
    registry = TargetRuleRegistry.test_only((build_target_rule(rule.rule_content_hash),))
    permission = make_target_permission(
        grant_id="g1",
        issuer_ref=TEST_ONLY_TARGET_ISSUER,
        actor_id=ACTOR_ID,
        rule_content_hash=rule.rule_content_hash,
        before_target_hash="before-hash",
        response_hash="r1",
        issued_at=10,
        expires_at=15,
    )
    decision = _decision(
        registry,
        _proposal(rule.rule_content_hash),
        permission,
        as_of=20,
    )
    assert decision.branch is TargetBranch.DENY
    assert decision.reason is TargetReason.PERMISSION_EXPIRED


def test_stale_prestate_conflict_is_denied() -> None:
    rule = build_response_rule()
    registry = TargetRuleRegistry.test_only((build_target_rule(rule.rule_content_hash),))
    permission = make_target_permission(
        grant_id="g1",
        issuer_ref=TEST_ONLY_TARGET_ISSUER,
        actor_id=ACTOR_ID,
        rule_content_hash=rule.rule_content_hash,
        before_target_hash="WRONG_BEFORE",
        response_hash="r1",
        issued_at=10,
    )
    decision = _decision(
        registry,
        _proposal(rule.rule_content_hash),
        permission,
    )
    assert decision.branch is TargetBranch.DENY
    assert decision.reason is TargetReason.PRESTATE_CONFLICT


def test_insufficient_enacted_history_yields_no_change() -> None:
    rule = build_response_rule()
    registry = TargetRuleRegistry.test_only((build_target_rule(rule.rule_content_hash),))
    permission = make_target_permission(
        grant_id="g1",
        issuer_ref=TEST_ONLY_TARGET_ISSUER,
        actor_id=ACTOR_ID,
        rule_content_hash=rule.rule_content_hash,
        before_target_hash="before-hash",
        response_hash="r1",
        issued_at=10,
    )
    decision = _decision(
        registry,
        _proposal(rule.rule_content_hash),
        permission,
        enacted_history_refs=(),
    )
    assert decision.branch is TargetBranch.NO_CHANGE
    assert decision.reason is TargetReason.INSUFFICIENT_ENACTED_HISTORY
    assert decision.after_target_hash == decision.before_target_hash


def test_valid_grant_with_enacted_history_yields_create() -> None:
    rule = build_response_rule()
    registry = TargetRuleRegistry.test_only((build_target_rule(rule.rule_content_hash),))
    permission = make_target_permission(
        grant_id="g1",
        issuer_ref=TEST_ONLY_TARGET_ISSUER,
        actor_id=ACTOR_ID,
        rule_content_hash=rule.rule_content_hash,
        before_target_hash="before-hash",
        response_hash="r1",
        issued_at=10,
    )
    decision = _decision(
        registry,
        _proposal(rule.rule_content_hash),
        permission,
    )
    assert decision.branch is TargetBranch.CREATE
    assert decision.reason is TargetReason.OK
    assert decision.record_hash
    assert decision.after_target_hash != decision.before_target_hash
    assert "g1" in decision.readset_refs


def test_no_proposal_yields_no_change() -> None:
    rule = build_response_rule()
    registry = TargetRuleRegistry.test_only((build_target_rule(rule.rule_content_hash),))
    decision = _decision(registry, None, None)
    assert decision.branch is TargetBranch.NO_CHANGE
    assert decision.reason is TargetReason.NO_PROPOSAL


def test_unissued_rule_yields_target_rule_unissued() -> None:
    rule = build_response_rule()
    registry = TargetRuleRegistry.test_only(())
    decision = _decision(
        TargetRuleRegistry(
            registry_id="V3_DEVELOPMENTAL_MIDDLE_STATE_REGISTRY",
            registry_version="1.0.0",
            grade="TEST_ONLY_SOURCEFREE_TECHNICAL",
            rules={},
        ),
        _proposal(rule.rule_content_hash),
        None,
    )
    assert decision.branch is TargetBranch.DENY
    assert decision.reason is TargetReason.TARGET_RULE_UNISSUED


def test_response_to_target_end_to_end_create() -> None:
    rule = build_response_rule()
    response_registry = ResponseRuleRegistry.test_only((rule,))
    lookup = lookup_rule(
        response_registry,
        authority_id=rule.authority_id,
        rule_version=rule.rule_version,
        rule_content_hash=rule.rule_content_hash,
        subject=ACTOR_ID,
    )
    response = evaluate_response(
        rule_lookup=lookup,
        event_ref=EVENT_HASH,
        event_time=15,
        subject=ACTOR_ID,
        conditioning_readset=("src-1",),
        actor_history_refs=("h-a", "h-b"),
        other_person_offer_ref="offer-1",
        material_opportunity_ref="world-1",
        prior_response_count=0,
    )
    assert response.target_proposals
    registry = TargetRuleRegistry.test_only((build_target_rule(rule.rule_content_hash),))
    permission = make_target_permission(
        grant_id="g1",
        issuer_ref=TEST_ONLY_TARGET_ISSUER,
        actor_id=ACTOR_ID,
        rule_content_hash=rule.rule_content_hash,
        before_target_hash="before-hash",
        response_hash=response.receipt_hash,
        issued_at=10,
    )
    decision = _decision(registry, response.target_proposals[0], permission)
    assert decision.branch is TargetBranch.CREATE
