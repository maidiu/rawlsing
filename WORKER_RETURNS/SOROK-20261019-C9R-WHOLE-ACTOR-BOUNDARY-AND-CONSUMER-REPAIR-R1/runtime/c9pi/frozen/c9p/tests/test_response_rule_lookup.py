"""(d) CAN008 response-rule registry lookup and refusal tests."""
from __future__ import annotations

from conftest import ACTOR_ID, TEST_ONLY_ISSUER, build_response_rule
from candidate.canon import digest
from candidate.response_rules import (
    ResponseRule,
    ResponseRuleRegistry,
    ResponseStatus,
    RuleLookupStatus,
    evaluate_response,
    lookup_rule,
)


def test_production_registry_lookup_returns_rule_absent() -> None:
    registry = ResponseRuleRegistry.production()
    result = lookup_rule(
        registry,
        authority_id="TEST_ONLY_CAN008_AUTHORITY",
        rule_version="1",
        rule_content_hash=digest({"rule": "x"}),
        subject=ACTOR_ID,
    )
    assert result.status is RuleLookupStatus.RULE_ABSENT
    assert result.reason == "CAN008_RULE_ABSENT_FROM_REGISTRY"
    assert result.issuer_verified is False


def test_unverified_issuer_lookup_returns_issuer_unverified() -> None:
    rule = build_response_rule()
    unverified = ResponseRule(
        rule_id=rule.rule_id,
        rule_version=rule.rule_version,
        rule_content_hash=rule.rule_content_hash,
        authority_id=rule.authority_id,
        authority_version=rule.authority_version,
        issuer_ref=rule.issuer_ref,
        issuer_verified=False,
        allowed_subjects=rule.allowed_subjects,
        permitted_readset_classes=rule.permitted_readset_classes,
        grade=rule.grade,
        predicates=rule.predicates,
    )
    registry = ResponseRuleRegistry.test_only((unverified,))
    result = lookup_rule(
        registry,
        authority_id=rule.authority_id,
        rule_version=rule.rule_version,
        rule_content_hash=rule.rule_content_hash,
        subject=ACTOR_ID,
    )
    assert result.status is RuleLookupStatus.RULE_ISSUER_UNVERIFIED
    assert result.reason == "CAN008_RULE_ISSUER_UNVERIFIED"


def test_test_only_registry_lookup_is_found_but_never_native() -> None:
    rule = build_response_rule()
    registry = ResponseRuleRegistry.test_only((rule,))
    result = lookup_rule(
        registry,
        authority_id=rule.authority_id,
        rule_version=rule.rule_version,
        rule_content_hash=rule.rule_content_hash,
        subject=ACTOR_ID,
    )
    assert result.status is RuleLookupStatus.FOUND
    assert result.issuer_verified is True
    assert result.grade == "TEST_ONLY_SOURCEFREE_TECHNICAL"


def test_subject_not_allowed_is_binding_mismatch() -> None:
    rule = build_response_rule()
    registry = ResponseRuleRegistry.test_only((rule,))
    result = lookup_rule(
        registry,
        authority_id=rule.authority_id,
        rule_version=rule.rule_version,
        rule_content_hash=rule.rule_content_hash,
        subject="OTHER_ACTOR",
    )
    assert result.status is RuleLookupStatus.RULE_BINDING_MISMATCH
    assert result.reason == "CAN008_RULE_SUBJECT_NOT_ALLOWED"


def test_absent_rule_yields_refused_response_with_readset() -> None:
    registry = ResponseRuleRegistry.production()
    lookup = lookup_rule(
        registry,
        authority_id="TEST_ONLY_CAN008_AUTHORITY",
        rule_version="1",
        rule_content_hash=digest({"rule": "x"}),
        subject=ACTOR_ID,
    )
    response = evaluate_response(
        rule_lookup=lookup,
        event_ref="event-hash",
        event_time=15,
        subject=ACTOR_ID,
        conditioning_readset=("src-1",),
        actor_history_refs=("h-a", "h-b"),
        other_person_offer_ref="offer-1",
        material_opportunity_ref="world-1",
        prior_response_count=0,
    )
    assert response.status is ResponseStatus.REFUSED
    assert response.target_proposals == ()
    assert "event-hash" in response.readset_refs


def test_unverified_rule_yields_held_response() -> None:
    rule = build_response_rule()
    unverified = ResponseRule(
        rule_id=rule.rule_id,
        rule_version=rule.rule_version,
        rule_content_hash=rule.rule_content_hash,
        authority_id=rule.authority_id,
        authority_version=rule.authority_version,
        issuer_ref=rule.issuer_ref,
        issuer_verified=False,
        allowed_subjects=rule.allowed_subjects,
        permitted_readset_classes=rule.permitted_readset_classes,
        grade=rule.grade,
        predicates=rule.predicates,
    )
    registry = ResponseRuleRegistry.test_only((unverified,))
    lookup = lookup_rule(
        registry,
        authority_id=rule.authority_id,
        rule_version=rule.rule_version,
        rule_content_hash=rule.rule_content_hash,
        subject=ACTOR_ID,
    )
    response = evaluate_response(
        rule_lookup=lookup,
        event_ref="event-hash",
        event_time=15,
        subject=ACTOR_ID,
        conditioning_readset=("src-1",),
        actor_history_refs=("h-a", "h-b"),
        other_person_offer_ref="offer-1",
        material_opportunity_ref="world-1",
        prior_response_count=0,
    )
    assert response.status is ResponseStatus.HELD
    assert response.reason == "CAN008_RULE_ISSUER_UNVERIFIED"


def test_found_rule_with_no_enacted_history_is_valid_empty() -> None:
    rule = build_response_rule()
    registry = ResponseRuleRegistry.test_only((rule,))
    lookup = lookup_rule(
        registry,
        authority_id=rule.authority_id,
        rule_version=rule.rule_version,
        rule_content_hash=rule.rule_content_hash,
        subject=ACTOR_ID,
    )
    response = evaluate_response(
        rule_lookup=lookup,
        event_ref="event-hash",
        event_time=15,
        subject=ACTOR_ID,
        conditioning_readset=("src-1",),
        actor_history_refs=(),
        other_person_offer_ref="offer-1",
        material_opportunity_ref="world-1",
        prior_response_count=0,
    )
    assert response.status is ResponseStatus.RESPONSE_EFFECTS_VALID_EMPTY
    assert response.target_proposals == ()


def test_found_rule_with_full_inputs_emits_exactly_one_proposal() -> None:
    rule = build_response_rule()
    registry = ResponseRuleRegistry.test_only((rule,))
    lookup = lookup_rule(
        registry,
        authority_id=rule.authority_id,
        rule_version=rule.rule_version,
        rule_content_hash=rule.rule_content_hash,
        subject=ACTOR_ID,
    )
    response = evaluate_response(
        rule_lookup=lookup,
        event_ref="event-hash",
        event_time=15,
        subject=ACTOR_ID,
        conditioning_readset=("src-1",),
        actor_history_refs=("h-a", "h-b"),
        other_person_offer_ref="offer-1",
        material_opportunity_ref="world-1",
        prior_response_count=0,
    )
    assert response.status is ResponseStatus.RESPONSE_COMMITTED
    assert len(response.target_proposals) == 1
    assert response.target_proposals[0]["state_kind_id"] == "V3MS_PRACTICE"
    assert response.recruited_refs == ("h-a", "h-b")
