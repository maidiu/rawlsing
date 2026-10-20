"""CAN008 response-rule registry lookup and refusal.

The production registry is empty. A lookup against an empty registry returns
`RULE_ABSENT`; a lookup against a registry whose entries are not backed by a
competent issuer returns `RULE_ISSUER_UNVERIFIED`. A TEST_ONLY registry is
explicitly typed and can never satisfy the native release gate.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping

from .canon import digest, seal

RESPONSE_RULE_SCHEMA = "C9P_CAN008_RESPONSE_RULE@1"

# The active production registry contains no issued CAN008 concrete rule.
DEFAULT_ISSUED_RESPONSE_RULES: Mapping[tuple[str, str, str], Mapping[str, Any]] = (
    MappingProxyType({})
)


class RuleLookupStatus(str, Enum):
    FOUND = "FOUND"
    RULE_ABSENT = "RULE_ABSENT"
    RULE_ISSUER_UNVERIFIED = "RULE_ISSUER_UNVERIFIED"
    RULE_BINDING_MISMATCH = "RULE_BINDING_MISMATCH"
    REQUEST_INVALID = "REQUEST_INVALID"


class ResponseStatus(str, Enum):
    RESPONSE_COMMITTED = "RESPONSE_COMMITTED"
    RESPONSE_EFFECTS_VALID_EMPTY = "RESPONSE_EFFECTS_VALID_EMPTY"
    REFUSED = "REFUSED"
    HELD = "HELD"


@dataclass(frozen=True)
class RuleLookupResult:
    """Typed result of one CAN008 response-rule registry lookup."""

    status: RuleLookupStatus
    rule_id: str
    rule_version: str
    rule_content_hash: str
    authority_id: str
    issuer_verified: bool
    grade: str
    reason: str

    @property
    def found(self) -> bool:
        return self.status is RuleLookupStatus.FOUND


@dataclass(frozen=True)
class ResponseRule:
    """One concrete CAN008 response rule body as presented by a registry."""

    rule_id: str
    rule_version: str
    rule_content_hash: str
    authority_id: str
    authority_version: str
    issuer_ref: str
    issuer_verified: bool
    allowed_subjects: tuple[str, ...]
    permitted_readset_classes: tuple[str, ...]
    grade: str
    predicates: tuple[str, ...]
    effect_kind: str = "TRANSFORM"
    numeric_policy: str = "NONE"
    stochastic_policy: str = "NO_DRAWS"

    def registry_key(self) -> tuple[str, str, str]:
        return (self.authority_id, self.rule_version, self.rule_content_hash)

    def as_dict(self) -> dict:
        return {
            "schema": RESPONSE_RULE_SCHEMA,
            "rule_id": self.rule_id,
            "rule_version": self.rule_version,
            "rule_content_hash": self.rule_content_hash,
            "authority_id": self.authority_id,
            "authority_version": self.authority_version,
            "issuer_ref": self.issuer_ref,
            "issuer_verified": self.issuer_verified,
            "allowed_subjects": list(self.allowed_subjects),
            "permitted_readset_classes": list(self.permitted_readset_classes),
            "grade": self.grade,
            "predicates": list(self.predicates),
            "effect_kind": self.effect_kind,
            "numeric_policy": self.numeric_policy,
            "stochastic_policy": self.stochastic_policy,
        }


@dataclass(frozen=True)
class ResponseRuleRegistry:
    """A response-rule registry. Production instances hold no issued rules."""

    registry_id: str
    registry_version: str
    grade: str
    rules: Mapping[tuple[str, str, str], Mapping[str, Any]]

    @staticmethod
    def production() -> "ResponseRuleRegistry":
        return ResponseRuleRegistry(
            registry_id="V3_ACTOR_RESPONSE_RULE_REGISTRY",
            registry_version="1.0.0",
            grade="PRODUCTION_EMPTY",
            rules=DEFAULT_ISSUED_RESPONSE_RULES,
        )

    @staticmethod
    def test_only(rules: tuple[ResponseRule, ...]) -> "ResponseRuleRegistry":
        table = {rule.registry_key(): rule.as_dict() for rule in rules}
        return ResponseRuleRegistry(
            registry_id="V3_ACTOR_RESPONSE_RULE_REGISTRY",
            registry_version="1.0.0",
            grade="TEST_ONLY_SOURCEFREE_TECHNICAL",
            rules=MappingProxyType(table),
        )


def lookup_rule(
    registry: ResponseRuleRegistry,
    *,
    authority_id: str,
    rule_version: str,
    rule_content_hash: str,
    subject: str,
) -> RuleLookupResult:
    """Look up one concrete CAN008 response rule.

    A production registry with no entry returns `RULE_ABSENT`. An entry whose
    `issuer_verified` is False returns `RULE_ISSUER_UNVERIFIED`. A TEST_ONLY entry
    is returned with `grade='TEST_ONLY_SOURCEFREE_TECHNICAL'` and can never
    satisfy the native release gate.
    """
    key = (authority_id, rule_version, rule_content_hash)
    entry = registry.rules.get(key)
    if entry is None:
        return RuleLookupResult(
            status=RuleLookupStatus.RULE_ABSENT,
            rule_id="",
            rule_version=rule_version,
            rule_content_hash=rule_content_hash,
            authority_id=authority_id,
            issuer_verified=False,
            grade=registry.grade,
            reason="CAN008_RULE_ABSENT_FROM_REGISTRY",
        )
    if not entry.get("issuer_verified", False):
        return RuleLookupResult(
            status=RuleLookupStatus.RULE_ISSUER_UNVERIFIED,
            rule_id=entry.get("rule_id", ""),
            rule_version=rule_version,
            rule_content_hash=rule_content_hash,
            authority_id=authority_id,
            issuer_verified=False,
            grade=entry.get("grade", registry.grade),
            reason="CAN008_RULE_ISSUER_UNVERIFIED",
        )
    allowed = entry.get("allowed_subjects", [])
    if subject not in allowed:
        return RuleLookupResult(
            status=RuleLookupStatus.RULE_BINDING_MISMATCH,
            rule_id=entry.get("rule_id", ""),
            rule_version=rule_version,
            rule_content_hash=rule_content_hash,
            authority_id=authority_id,
            issuer_verified=True,
            grade=entry.get("grade", registry.grade),
            reason="CAN008_RULE_SUBJECT_NOT_ALLOWED",
        )
    return RuleLookupResult(
        status=RuleLookupStatus.FOUND,
        rule_id=entry.get("rule_id", ""),
        rule_version=rule_version,
        rule_content_hash=rule_content_hash,
        authority_id=authority_id,
        issuer_verified=True,
        grade=entry.get("grade", registry.grade),
        reason="OK",
    )


@dataclass(frozen=True)
class ResponseResult:
    """Bounded CAN008 immediate-response outcome for one admitted event."""

    status: ResponseStatus
    event_ref: str
    rule_lookup: RuleLookupResult
    recruited_refs: tuple[str, ...]
    uptake_refs: tuple[str, ...]
    candidate_route: str
    target_proposals: tuple[Mapping[str, Any], ...]
    readset_refs: tuple[str, ...]
    reason: str
    receipt_hash: str


def evaluate_response(
    *,
    rule_lookup: RuleLookupResult,
    event_ref: str,
    event_time: int,
    subject: str,
    conditioning_readset: tuple[str, ...],
    actor_history_refs: tuple[str, ...],
    other_person_offer_ref: str,
    material_opportunity_ref: str,
    prior_response_count: int,
) -> ResponseResult:
    """Derive one bounded immediate response from admitted inputs.

    This never mints target-update permission, knowledge, memory, belief or
    other-person action. When the rule lookup did not find an issuer-verified
    rule, the result is a typed refusal or hold with no target proposals.
    """
    readset = tuple(
        [event_ref, *conditioning_readset, *actor_history_refs]
        + ([other_person_offer_ref] if other_person_offer_ref else [])
        + ([material_opportunity_ref] if material_opportunity_ref else [])
    )
    if rule_lookup.status is RuleLookupStatus.RULE_ABSENT:
        return ResponseResult(
            status=ResponseStatus.REFUSED,
            event_ref=event_ref,
            rule_lookup=rule_lookup,
            recruited_refs=(),
            uptake_refs=(),
            candidate_route="",
            target_proposals=(),
            readset_refs=readset,
            reason="CAN008_RULE_ABSENT_FROM_REGISTRY",
            receipt_hash="",
        )
    if rule_lookup.status is RuleLookupStatus.RULE_ISSUER_UNVERIFIED:
        return ResponseResult(
            status=ResponseStatus.HELD,
            event_ref=event_ref,
            rule_lookup=rule_lookup,
            recruited_refs=(),
            uptake_refs=(),
            candidate_route="",
            target_proposals=(),
            readset_refs=readset,
            reason="CAN008_RULE_ISSUER_UNVERIFIED",
            receipt_hash="",
        )
    if rule_lookup.status is RuleLookupStatus.RULE_BINDING_MISMATCH:
        return ResponseResult(
            status=ResponseStatus.REFUSED,
            event_ref=event_ref,
            rule_lookup=rule_lookup,
            recruited_refs=(),
            uptake_refs=(),
            candidate_route="",
            target_proposals=(),
            readset_refs=readset,
            reason=rule_lookup.reason,
            receipt_hash="",
        )
    if rule_lookup.status is RuleLookupStatus.REQUEST_INVALID:
        return ResponseResult(
            status=ResponseStatus.REFUSED,
            event_ref=event_ref,
            rule_lookup=rule_lookup,
            recruited_refs=(),
            uptake_refs=(),
            candidate_route="",
            target_proposals=(),
            readset_refs=readset,
            reason=rule_lookup.reason,
            receipt_hash="",
        )
    if not actor_history_refs or not other_person_offer_ref or not material_opportunity_ref:
        return ResponseResult(
            status=ResponseStatus.RESPONSE_EFFECTS_VALID_EMPTY,
            event_ref=event_ref,
            rule_lookup=rule_lookup,
            recruited_refs=(),
            uptake_refs=(),
            candidate_route="NO_QUALIFYING_ENACTED_HISTORY",
            target_proposals=(),
            readset_refs=readset,
            reason="VALID_EMPTY",
            receipt_hash="",
        )
    uptake = tuple(f"uptake:{event_ref}:{ref}" for ref in conditioning_readset)
    recruited = tuple(actor_history_refs)
    proposal = seal(
        {
            "schema": "C9P_TARGET_PROPOSAL@1",
            "actor_id": subject,
            "state_kind_id": "V3MS_PRACTICE",
            "operation": "CREATE",
            "proposed_effective_time": event_time,
            "semantic_object_ref": "c9p:coordinated_material_inspection",
            "target_refs": ["c9p:practice"],
            "causal_parent_refs": [event_ref, *actor_history_refs],
            "source_update_rule_ref": rule_lookup.rule_content_hash,
            "evaluator_receipts": list(conditioning_readset),
            "numeric_rule_ref": None,
            "stochastic_receipt_ref": None,
        }
    )
    return ResponseResult(
        status=ResponseStatus.RESPONSE_COMMITTED,
        event_ref=event_ref,
        rule_lookup=rule_lookup,
        recruited_refs=recruited,
        uptake_refs=uptake,
        candidate_route="COORDINATED_MATERIAL_INSPECTION",
        target_proposals=(proposal,),
        readset_refs=readset,
        reason="OK",
        receipt_hash=digest(
            {
                "event_ref": event_ref,
                "rule": rule_lookup.rule_content_hash,
                "readset": list(readset),
            }
        ),
    )


__all__ = [
    "DEFAULT_ISSUED_RESPONSE_RULES",
    "RESPONSE_RULE_SCHEMA",
    "ResponseResult",
    "ResponseRule",
    "ResponseRuleRegistry",
    "ResponseStatus",
    "RuleLookupResult",
    "RuleLookupStatus",
    "evaluate_response",
    "lookup_rule",
]
