"""Shared fixtures for the C9P candidate test suite.

Every fixture is explicitly typed as TEST_ONLY sourcefree technical material.
No fixture is ever presented as a competent issuer, a native positive authority
or a performed action.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

RETURN_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = RETURN_DIR.parents[1]
for entry in (str(REPO_ROOT), str(RETURN_DIR)):
    if entry not in sys.path:
        sys.path.insert(0, entry)

from candidate.action_admission import make_performed_action_receipt  # noqa: E402
from candidate.canon import digest, seal  # noqa: E402
from candidate.conditioning import make_conditioning_source  # noqa: E402
from candidate.events import GRADE_TEST_ONLY, make_event_witness  # noqa: E402
from candidate.identity import ACTOR_RECORD_SCHEMA  # noqa: E402
from candidate.response_rules import ResponseRule, ResponseRuleRegistry  # noqa: E402
from candidate.target_rules import TargetRule, TargetRuleRegistry, make_target_permission  # noqa: E402

ACTOR_ID = "actor-c9p-001"
TEST_ONLY_ISSUER = "TEST_ONLY_CAN008_C9P_ISSUER"
TEST_ONLY_TARGET_ISSUER = "TEST_ONLY_CAN011_C9P_ISSUER"


def build_actor_record(
    *,
    actor_id: str = ACTOR_ID,
    activation_status: str = "ACTIVE",
    standing_state: str = "STANDING_CURRENT",
    currentness_as_of: int = 10,
    as_of: int = 20,
) -> dict:
    """Return one sealed TEST_ONLY actor identity record."""
    del as_of
    return seal(
        {
            "schema": ACTOR_RECORD_SCHEMA,
            "actor_id": actor_id,
            "activation_status": activation_status,
            "standing_state": standing_state,
            "currentness_as_of": currentness_as_of,
            "source_ref": f"TEST_ONLY_ACTOR_SOURCE:{actor_id}",
            "source_hash": digest({"actor": actor_id, "source": "TEST_ONLY"}),
        }
    )


def build_event_witness(
    *,
    event_id: str = "event-c9p-e1",
    time: int = 15,
    actor_role: str = "ACTOR_A",
    owner_ref: str = "TEST_ONLY_EVENT_OWNER",
    content: dict | None = None,
    causal_parent_refs: tuple[str, ...] = (),
) -> dict:
    """Return one sealed TEST_ONLY precipitating event witness."""
    return make_event_witness(
        event_id=event_id,
        owner_ref=owner_ref,
        time=time,
        content=content or {"fact": "shared_tool_offer", "object": "wrench"},
        actor_role=actor_role,
        admission_grade=GRADE_TEST_ONLY,
        causal_parent_refs=causal_parent_refs,
    )


def build_conditioning_sources(subject: str = ACTOR_ID) -> list[dict]:
    """Return two sealed read-only conditioning sources for `subject`."""
    return [
        make_conditioning_source(
            source_ref="TEST_ONLY_PERSON_STATE:standing",
            source_class="ResolvedStructuralContext",
            subject=subject,
            body={"standing": "cycle_maintenance_project_active"},
        ),
        make_conditioning_source(
            source_ref="TEST_ONLY_WORLD_STATE:garage",
            source_class="V553_V558_STRUCTURAL_OBJECT",
            subject=subject,
            body={"tool": "wrench_available", "access": "granted"},
        ),
    ]


def build_response_rule() -> ResponseRule:
    """Return one explicitly TEST_ONLY CAN008 response rule body."""
    return ResponseRule(
        rule_id="TEST_ONLY_H1_PRACTICE_RESPONSE",
        rule_version="1",
        rule_content_hash=digest(
            {"rule": "TEST_ONLY_H1_PRACTICE_RESPONSE", "version": "1"}
        ),
        authority_id="TEST_ONLY_CAN008_AUTHORITY",
        authority_version="1",
        issuer_ref=TEST_ONLY_ISSUER,
        issuer_verified=True,
        allowed_subjects=(ACTOR_ID,),
        permitted_readset_classes=("ResolvedStructuralContext", "V553_V558_STRUCTURAL_OBJECT"),
        grade="TEST_ONLY_SOURCEFREE_TECHNICAL",
        predicates=(
            "admitted event with actor receivability",
            "independent other-person offer",
            "two source-owned enacted history refs",
            "material opportunity present",
        ),
    )


def build_target_rule(rule_content_hash: str) -> TargetRule:
    """Return one explicitly TEST_ONLY CAN011 target rule bound to `rule_content_hash`."""
    return TargetRule(
        rule_id="TEST_ONLY_H1_PRACTICE_TARGET",
        rule_version="1",
        rule_content_hash=rule_content_hash,
        authority_id="TEST_ONLY_CAN011_AUTHORITY",
        authority_version="1",
        issuer_ref=TEST_ONLY_TARGET_ISSUER,
        issuer_verified=True,
        state_kind_id="V3MS_PRACTICE",
        allowed_operations=("CREATE",),
        accepted_semantic_objects=("c9p:coordinated_material_inspection",),
        grade="TEST_ONLY_SOURCEFREE_TECHNICAL",
    )


@pytest.fixture
def actor_record() -> dict:
    return build_actor_record()


@pytest.fixture
def event_witness() -> dict:
    return build_event_witness()


@pytest.fixture
def conditioning_sources() -> list[dict]:
    return build_conditioning_sources()


@pytest.fixture
def response_rule() -> ResponseRule:
    return build_response_rule()


@pytest.fixture
def response_registry(response_rule: ResponseRule) -> ResponseRuleRegistry:
    return ResponseRuleRegistry.test_only((response_rule,))


@pytest.fixture
def target_registry(response_rule: ResponseRule) -> TargetRuleRegistry:
    return TargetRuleRegistry.test_only(
        (build_target_rule(response_rule.rule_content_hash),)
    )


@pytest.fixture
def enacted_history_refs() -> tuple[str, ...]:
    return ("TEST_ONLY_ENACTED_H_A", "TEST_ONLY_ENACTED_H_B")


@pytest.fixture
def permitted_issuers() -> frozenset[str]:
    return frozenset({TEST_ONLY_TARGET_ISSUER})


@pytest.fixture
def target_permission(response_rule: ResponseRule, actor_record: dict) -> dict:
    return make_target_permission(
        grant_id="TEST_ONLY_GRANT_001",
        issuer_ref=TEST_ONLY_TARGET_ISSUER,
        actor_id=actor_record["actor_id"],
        rule_content_hash=response_rule.rule_content_hash,
        before_target_hash="",
        response_hash="",
        issued_at=10,
    )


@pytest.fixture
def performed_action_receipt() -> dict:
    return make_performed_action_receipt(
        actor_id=ACTOR_ID,
        act="inspect_with_tool",
        actuator_ref="TEST_ONLY_ACTUATOR",
        occurrence_ref="TEST_ONLY_OCCURRENCE_E2",
        action_time=30,
        consumed_state_hash="TEST_ONLY_CONSUMED_STATE_HASH",
    )
