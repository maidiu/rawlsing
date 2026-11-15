"""CAN008 response-rule registry lookup and refusal.

C9R hardening: registry lookup accepts only an explicitly typed TEST_ONLY
registry whose entries are sealed by this module's factory, or the empty
production registry. A caller-constructed registry carrying a forged
`CURRENT_ACCEPTED` grade, an unsealed rehashed entry, or a hash-only alias is
refused. A TEST_ONLY rule is never native authority.

Declared-evidence adapter: under the TEST_ONLY grade, enacted-history, offer and
material references must be explicitly `TEST_ONLY_`-namespaced, distinct and not
derived from the focal actor, and at least two distinct enacted acts are
required. This is adapter verification of declared test-only evidence, NOT an
H1/H2/H3 scientific threshold and NOT native practice formation.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping

from .canon import digest, seal, valid

RESPONSE_RULE_SCHEMA = "C9P_CAN008_RESPONSE_RULE@1"
GRADE_TEST_ONLY = "TEST_ONLY_SOURCEFREE_TECHNICAL"
GRADE_PRODUCTION_EMPTY = "PRODUCTION_EMPTY"
TEST_ONLY_PREFIX = "TEST_ONLY"

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

    @property
    def authenticated(self) -> bool:
        return False


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
            grade=GRADE_PRODUCTION_EMPTY,
            rules=DEFAULT_ISSUED_RESPONSE_RULES,
        )

    @staticmethod
    def test_only(rules: tuple[ResponseRule, ...]) -> "ResponseRuleRegistry":
        table = {rule.registry_key(): seal(rule.as_dict()) for rule in rules}
        return ResponseRuleRegistry(
            registry_id="V3_ACTOR_RESPONSE_RULE_REGISTRY",
            registry_version="1.0.0",
            grade=GRADE_TEST_ONLY,
            rules=MappingProxyType(table),
        )


def _unverified(reason: str, grade: str = "") -> RuleLookupResult:
    return RuleLookupResult(
        status=RuleLookupStatus.RULE_ISSUER_UNVERIFIED,
        rule_id="",
        rule_version="",
        rule_content_hash="",
        authority_id="",
        issuer_verified=False,
        grade=grade,
        reason=reason,
    )


def lookup_rule(
    registry: ResponseRuleRegistry,
    *,
    authority_id: str,
    rule_version: str,
    rule_content_hash: str,
    subject: str,
) -> RuleLookupResult:
    """Look up one concrete CAN008 response rule with strict custody checks."""
    if registry.grade not in (GRADE_PRODUCTION_EMPTY, GRADE_TEST_ONLY):
        return _unverified("UNRECOGNIZED_REGISTRY_GRADE", str(registry.grade))
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
    if not isinstance(entry, Mapping) or not valid(dict(entry)):
        return _unverified("CAN008_RULE_ENTRY_UNSEALED", registry.grade)
    if entry.get("rule_content_hash") != rule_content_hash:
        return _unverified("CAN008_RULE_CONTENT_HASH_BINDING_MISMATCH", registry.grade)
    if not entry.get("issuer_verified", False):
        return _unverified("CAN008_RULE_ISSUER_UNVERIFIED", registry.grade)
    entry_grade = entry.get("grade", "")
    if entry_grade != registry.grade:
        return _unverified("CAN008_RULE_GRADE_MISMATCH", str(entry_grade))
    if registry.grade == GRADE_TEST_ONLY and not str(entry.get("issuer_ref", "")).startswith(
        TEST_ONLY_PREFIX
    ):
        return _unverified("CAN008_TEST_ONLY_ISSUER_NAMESPACE_REQUIRED", registry.grade)
    allowed = entry.get("allowed_subjects", [])
    if subject not in allowed:
        return RuleLookupResult(
            status=RuleLookupStatus.RULE_BINDING_MISMATCH,
            rule_id=entry.get("rule_id", ""),
            rule_version=rule_version,
            rule_content_hash=rule_content_hash,
            authority_id=authority_id,
            issuer_verified=True,
            grade=entry_grade,
            reason="CAN008_RULE_SUBJECT_NOT_ALLOWED",
        )
    return RuleLookupResult(
        status=RuleLookupStatus.FOUND,
        rule_id=entry.get("rule_id", ""),
        rule_version=rule_version,
        rule_content_hash=rule_content_hash,
        authority_id=authority_id,
        issuer_verified=True,
        grade=entry_grade,
        reason="OK_TEST_ONLY_NOT_NATIVE"
        if entry_grade == GRADE_TEST_ONLY
        else "OK",
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
    eligible_material_refs: tuple[str, ...] = ()
    declared_history_refs: tuple[str, ...] = ()
    declared_offer_ref: str = ""
    s35_receipt: Mapping[str, Any] | None = None

    @property
    def has_effect(self) -> bool:
        return bool(self.target_proposals)


def _valid_declared_history(refs: Any, subject: str) -> tuple[bool, str]:
    if not isinstance(refs, (list, tuple)) or len(refs) < 2:
        return (False, "INSUFFICIENT_ENACTED_HISTORY")
    if any(not isinstance(ref, str) or not ref.strip() for ref in refs):
        return (False, "INVALID_ENACTED_HISTORY_REF")
    if len(set(refs)) != len(refs):
        return (False, "DUPLICATE_ENACTED_HISTORY_REF")
    prefix = subject + ":"
    for ref in refs:
        if ref == subject or ref.startswith(prefix):
            return (False, "SELF_DERIVED_ENACTED_HISTORY")
        if not ref.startswith(TEST_ONLY_PREFIX):
            return (False, "ENACTED_HISTORY_NOT_DECLARED_TEST_ONLY")
    return (True, "OK")


def _valid_declared_offer(ref: Any, subject: str) -> tuple[bool, str]:
    if not isinstance(ref, str) or not ref.strip():
        return (False, "ABSENT_INDEPENDENT_P_ACTION")
    if ref == subject or ref.startswith(subject + ":"):
        return (False, "SELF_OFFER_NOT_INDEPENDENT_P_ACTION")
    if not ref.startswith(TEST_ONLY_PREFIX):
        return (False, "OFFER_NOT_DECLARED_TEST_ONLY")
    return (True, "OK")


def _valid_declared_material(ref: Any) -> tuple[bool, str]:
    if not isinstance(ref, str) or not ref.strip():
        return (False, "ABSENT_MATERIAL_OPPORTUNITY")
    if not ref.startswith(TEST_ONLY_PREFIX):
        return (False, "MATERIAL_NOT_DECLARED_TEST_ONLY")
    return (True, "OK")


def _empty(
    *,
    event_ref: str,
    rule_lookup: RuleLookupResult,
    readset: tuple[str, ...],
    reason: str,
    material_refs: tuple[str, ...] = (),
    history_refs: tuple[str, ...] = (),
    offer_ref: str = "",
) -> ResponseResult:
    return ResponseResult(
        status=ResponseStatus.RESPONSE_EFFECTS_VALID_EMPTY,
        event_ref=event_ref,
        rule_lookup=rule_lookup,
        recruited_refs=(),
        uptake_refs=(),
        candidate_route="NO_QUALIFYING_DECLARED_EVIDENCE",
        target_proposals=(),
        readset_refs=readset,
        reason=reason,
        receipt_hash="",
        eligible_material_refs=material_refs,
        declared_history_refs=history_refs,
        declared_offer_ref=offer_ref,
    )


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
    material_eligible: bool | None = None,
    eligible_material_refs: tuple[str, ...] = (),
) -> ResponseResult:
    """Derive one bounded immediate response from admitted inputs.

    This never mints target-update permission, knowledge, memory, belief or
    other-person action. A non-found or unverified rule is a typed refusal/hold.
    Under the TEST_ONLY grade, declared evidence must satisfy the explicit
    namespace/distinctness adapter; otherwise the result is VALID_EMPTY.
    """
    readset = tuple(
        [event_ref, *conditioning_readset, *actor_history_refs]
        + ([other_person_offer_ref] if other_person_offer_ref else [])
        + ([material_opportunity_ref] if material_opportunity_ref else [])
    )
    status = rule_lookup.status
    if status is RuleLookupStatus.RULE_ABSENT:
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
    if status is RuleLookupStatus.RULE_ISSUER_UNVERIFIED:
        return ResponseResult(
            status=ResponseStatus.HELD,
            event_ref=event_ref,
            rule_lookup=rule_lookup,
            recruited_refs=(),
            uptake_refs=(),
            candidate_route="",
            target_proposals=(),
            readset_refs=readset,
            reason=rule_lookup.reason or "CAN008_RULE_ISSUER_UNVERIFIED",
            receipt_hash="",
        )
    if status in (RuleLookupStatus.RULE_BINDING_MISMATCH, RuleLookupStatus.REQUEST_INVALID):
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
    history_ok, history_reason = _valid_declared_history(actor_history_refs, subject)
    offer_ok, offer_reason = _valid_declared_offer(other_person_offer_ref, subject)
    material_ok, material_reason = _valid_declared_material(material_opportunity_ref)
    if not history_ok or not offer_ok or not material_ok:
        return _empty(
            event_ref=event_ref,
            rule_lookup=rule_lookup,
            readset=readset,
            reason=(
                history_reason
                if not history_ok
                else offer_reason
                if not offer_ok
                else material_reason
            ),
            history_refs=tuple(actor_history_refs),
            offer_ref=other_person_offer_ref,
        )
    if material_eligible is False:
        return _empty(
            event_ref=event_ref,
            rule_lookup=rule_lookup,
            readset=readset,
            reason="NO_ELIGIBLE_MATERIAL_SOURCE",
            material_refs=eligible_material_refs,
            history_refs=tuple(actor_history_refs),
            offer_ref=other_person_offer_ref,
        )
    uptake = tuple(f"declared_uptake:{event_ref}:{ref}" for ref in conditioning_readset)
    recruited = tuple(actor_history_refs)
    receipt_hash = digest(
        {
            "event_ref": event_ref,
            "rule": rule_lookup.rule_content_hash,
            "readset": list(readset),
            "grade": rule_lookup.grade,
        }
    )
    proposal = seal(
        {
            "schema": "C9P_TARGET_PROPOSAL@1",
            "actor_id": subject,
            "state_kind_id": "V3MS_PRACTICE",
            "operation": "CREATE",
            "proposed_effective_time": event_time,
            "proposed_payload_delta_or_replacement": {
                "practice_label": "coordinated_material_inspection",
                "declared_history_refs": list(actor_history_refs),
                "declared_offer_ref": other_person_offer_ref,
                "declared_material_ref": material_opportunity_ref,
                "eligible_material_refs": list(eligible_material_refs),
                "grade": rule_lookup.grade,
            },
            "semantic_object_ref": "c9p:coordinated_material_inspection",
            "target_refs": ["c9p:practice"],
            "causal_parent_refs": [event_ref, *actor_history_refs],
            "source_update_rule_ref": rule_lookup.rule_content_hash,
            "response_receipt_ref": receipt_hash,
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
        receipt_hash=receipt_hash,
        eligible_material_refs=tuple(eligible_material_refs),
        declared_history_refs=tuple(actor_history_refs),
        declared_offer_ref=other_person_offer_ref,
    )


__all__ = [
    "DEFAULT_ISSUED_RESPONSE_RULES",
    "GRADE_PRODUCTION_EMPTY",
    "GRADE_TEST_ONLY",
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
