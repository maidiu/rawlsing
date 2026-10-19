"""CAN011 target rule, permission and CREATE / NO_CHANGE / DENY branch evaluation.

Target permission is a separate jurisdiction from the CAN008 response rule. A
self-issued permission, a foreign owner grant and an unissued target rule are all
refused with typed reasons. The production target-rule registry is empty.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping

from .canon import digest, seal

TARGET_RULE_SCHEMA = "C9P_CAN011_TARGET_RULE@1"
TARGET_PERMISSION_SCHEMA = "C9P_CAN011_TARGET_PERMISSION@1"

DEFAULT_ISSUED_TARGET_RULES: Mapping[tuple[str, str, str], Mapping[str, Any]] = (
    MappingProxyType({})
)


class TargetBranch(str, Enum):
    CREATE = "CREATE"
    NO_CHANGE = "NO_CHANGE"
    DENY = "DENY"


class TargetReason(str, Enum):
    OK = "OK"
    TARGET_RULE_ABSENT = "TARGET_RULE_ABSENT"
    TARGET_RULE_UNISSUED = "TARGET_RULE_UNISSUED"
    TARGET_RULE_ISSUER_UNVERIFIED = "TARGET_RULE_ISSUER_UNVERIFIED"
    PERMISSION_MISSING = "PERMISSION_MISSING"
    PERMISSION_SELF_ISSUED = "PERMISSION_SELF_ISSUED"
    PERMISSION_FOREIGN_OWNER = "PERMISSION_FOREIGN_OWNER"
    PERMISSION_REVOKED = "PERMISSION_REVOKED"
    PERMISSION_EXPIRED = "PERMISSION_EXPIRED"
    PERMISSION_BINDING_MISMATCH = "PERMISSION_BINDING_MISMATCH"
    PRESTATE_CONFLICT = "PRESTATE_CONFLICT"
    DUPLICATE_TARGET_IDENTITY = "DUPLICATE_TARGET_IDENTITY"
    CAUSAL_PARENT_STALE = "CAUSAL_PARENT_STALE"
    SEMANTIC_OBJECT_NOT_ACCEPTED = "SEMANTIC_OBJECT_NOT_ACCEPTED"
    INSUFFICIENT_ENACTED_HISTORY = "INSUFFICIENT_ENACTED_HISTORY"
    PROPOSAL_INTEGRITY_FAILURE = "PROPOSAL_INTEGRITY_FAILURE"
    NO_PROPOSAL = "NO_PROPOSAL"


@dataclass(frozen=True)
class TargetRule:
    """One separately issued CAN011 target update rule body."""

    rule_id: str
    rule_version: str
    rule_content_hash: str
    authority_id: str
    authority_version: str
    issuer_ref: str
    issuer_verified: bool
    state_kind_id: str
    allowed_operations: tuple[str, ...]
    accepted_semantic_objects: tuple[str, ...]
    grade: str

    def registry_key(self) -> tuple[str, str, str]:
        return (self.authority_id, self.rule_version, self.rule_content_hash)

    def as_dict(self) -> dict:
        return {
            "schema": TARGET_RULE_SCHEMA,
            "rule_id": self.rule_id,
            "rule_version": self.rule_version,
            "rule_content_hash": self.rule_content_hash,
            "authority_id": self.authority_id,
            "authority_version": self.authority_version,
            "issuer_ref": self.issuer_ref,
            "issuer_verified": self.issuer_verified,
            "state_kind_id": self.state_kind_id,
            "allowed_operations": list(self.allowed_operations),
            "accepted_semantic_objects": list(self.accepted_semantic_objects),
            "grade": self.grade,
        }


@dataclass(frozen=True)
class TargetRuleRegistry:
    """A CAN011 target-rule registry. Production instances hold no issued rules."""

    registry_id: str
    registry_version: str
    grade: str
    rules: Mapping[tuple[str, str, str], Mapping[str, Any]]

    @staticmethod
    def production() -> "TargetRuleRegistry":
        return TargetRuleRegistry(
            registry_id="V3_DEVELOPMENTAL_MIDDLE_STATE_REGISTRY",
            registry_version="1.0.0",
            grade="PRODUCTION_EMPTY",
            rules=DEFAULT_ISSUED_TARGET_RULES,
        )

    @staticmethod
    def test_only(rules: tuple[TargetRule, ...]) -> "TargetRuleRegistry":
        table = {rule.registry_key(): rule.as_dict() for rule in rules}
        return TargetRuleRegistry(
            registry_id="V3_DEVELOPMENTAL_MIDDLE_STATE_REGISTRY",
            registry_version="1.0.0",
            grade="TEST_ONLY_SOURCEFREE_TECHNICAL",
            rules=MappingProxyType(table),
        )


@dataclass(frozen=True)
class TargetPermission:
    """One separately authenticated CAN011 target-update grant."""

    grant_id: str
    issuer_ref: str
    issuer_scope: str
    actor_id: str
    rule_content_hash: str
    before_target_hash: str
    response_hash: str
    issued_at: int
    expires_at: int | None
    revoked: bool
    grade: str

    def sealed(self) -> dict:
        return seal(
            {
                "schema": TARGET_PERMISSION_SCHEMA,
                "grant_id": self.grant_id,
                "issuer_ref": self.issuer_ref,
                "issuer_scope": self.issuer_scope,
                "actor_id": self.actor_id,
                "rule_content_hash": self.rule_content_hash,
                "before_target_hash": self.before_target_hash,
                "response_hash": self.response_hash,
                "issued_at": self.issued_at,
                "expires_at": self.expires_at,
                "revoked": self.revoked,
                "grade": self.grade,
            }
        )


@dataclass(frozen=True)
class TargetDecision:
    """Typed CREATE / NO_CHANGE / DENY outcome for one target proposal."""

    branch: TargetBranch
    reason: TargetReason
    actor_id: str
    state_kind_id: str
    proposal_hash: str
    record_hash: str
    before_target_hash: str
    after_target_hash: str
    readset_refs: tuple[str, ...]
    permission_ref: str

    @property
    def committed(self) -> bool:
        return self.branch is TargetBranch.CREATE


def _deny(
    reason: TargetReason,
    *,
    actor_id: str = "",
    state_kind_id: str = "",
    proposal_hash: str = "",
    before_target_hash: str = "",
    readset_refs: tuple[str, ...] = (),
    permission_ref: str = "",
) -> TargetDecision:
    return TargetDecision(
        branch=TargetBranch.DENY,
        reason=reason,
        actor_id=actor_id,
        state_kind_id=state_kind_id,
        proposal_hash=proposal_hash,
        record_hash="",
        before_target_hash=before_target_hash,
        after_target_hash=before_target_hash,
        readset_refs=readset_refs,
        permission_ref=permission_ref,
    )


def _no_change(
    reason: TargetReason,
    *,
    actor_id: str = "",
    state_kind_id: str = "",
    proposal_hash: str = "",
    before_target_hash: str = "",
    readset_refs: tuple[str, ...] = (),
    permission_ref: str = "",
) -> TargetDecision:
    return TargetDecision(
        branch=TargetBranch.NO_CHANGE,
        reason=reason,
        actor_id=actor_id,
        state_kind_id=state_kind_id,
        proposal_hash=proposal_hash,
        record_hash="",
        before_target_hash=before_target_hash,
        after_target_hash=before_target_hash,
        readset_refs=readset_refs,
        permission_ref=permission_ref,
    )


def evaluate_target(
    *,
    registry: TargetRuleRegistry,
    proposal: Mapping[str, Any] | None,
    permission: Mapping[str, Any] | None,
    actor_id: str,
    before_target_hash: str,
    existing_target_ids: frozenset[str],
    prior_event_hash: str,
    as_of: int,
    enacted_history_refs: tuple[str, ...],
    permitted_issuer_refs: frozenset[str],
    request_is_self_issued: bool = False,
) -> TargetDecision:
    """Evaluate one CAN011 target proposal against rule, permission and prestate.

    Branch contract:
    - `CREATE` only when an issuer-verified target rule and a separately
      authenticated, unexpired, unrevoked permission bind the exact proposal.
    - `NO_CHANGE` when the rule permits the operation but the enacted history is
      insufficient for the proposed semantic object.
    - `DENY` on every missing, self-issued, foreign, revoked, expired, stale or
      integrity-failing condition. State is never partially mutated.
    """
    if request_is_self_issued:
        return _deny(
            TargetReason.PERMISSION_SELF_ISSUED,
            actor_id=actor_id,
            before_target_hash=before_target_hash,
        )
    if proposal is None:
        return _no_change(
            TargetReason.NO_PROPOSAL,
            actor_id=actor_id,
            before_target_hash=before_target_hash,
        )
    if not isinstance(proposal, Mapping):
        return _deny(
            TargetReason.PROPOSAL_INTEGRITY_FAILURE,
            actor_id=actor_id,
            before_target_hash=before_target_hash,
        )
    from .canon import valid as _valid

    if not _valid(proposal):
        return _deny(
            TargetReason.PROPOSAL_INTEGRITY_FAILURE,
            actor_id=actor_id,
            before_target_hash=before_target_hash,
        )
    proposal_hash = proposal.get("hash", "")
    if proposal.get("actor_id") != actor_id:
        return _deny(
            TargetReason.PROPOSAL_INTEGRITY_FAILURE,
            actor_id=actor_id,
            proposal_hash=proposal_hash,
            before_target_hash=before_target_hash,
        )
    rule_hash = proposal.get("source_update_rule_ref", "")
    entry = registry.rules.get(("CAN011_TARGET", "1", rule_hash))
    if entry is None:
        entry = None
        for key, value in registry.rules.items():
            if key[2] == rule_hash:
                entry = value
                break
    if entry is None:
        return _deny(
            TargetReason.TARGET_RULE_ABSENT
            if registry.grade == "PRODUCTION_EMPTY"
            else TargetReason.TARGET_RULE_UNISSUED,
            actor_id=actor_id,
            state_kind_id=proposal.get("state_kind_id", ""),
            proposal_hash=proposal_hash,
            before_target_hash=before_target_hash,
        )
    if not entry.get("issuer_verified", False):
        return _deny(
            TargetReason.TARGET_RULE_ISSUER_UNVERIFIED,
            actor_id=actor_id,
            state_kind_id=proposal.get("state_kind_id", ""),
            proposal_hash=proposal_hash,
            before_target_hash=before_target_hash,
        )
    if permission is None:
        return _deny(
            TargetReason.PERMISSION_MISSING,
            actor_id=actor_id,
            state_kind_id=proposal.get("state_kind_id", ""),
            proposal_hash=proposal_hash,
            before_target_hash=before_target_hash,
        )
    if not _valid(permission):
        return _deny(
            TargetReason.PERMISSION_BINDING_MISMATCH,
            actor_id=actor_id,
            state_kind_id=proposal.get("state_kind_id", ""),
            proposal_hash=proposal_hash,
            before_target_hash=before_target_hash,
        )
    if permission.get("actor_id") != actor_id:
        return _deny(
            TargetReason.PERMISSION_FOREIGN_OWNER,
            actor_id=actor_id,
            state_kind_id=proposal.get("state_kind_id", ""),
            proposal_hash=proposal_hash,
            before_target_hash=before_target_hash,
        )
    if permission.get("revoked"):
        return _deny(
            TargetReason.PERMISSION_REVOKED,
            actor_id=actor_id,
            state_kind_id=proposal.get("state_kind_id", ""),
            proposal_hash=proposal_hash,
            before_target_hash=before_target_hash,
        )
    expires_at = permission.get("expires_at")
    if isinstance(expires_at, int) and not isinstance(expires_at, bool) and as_of >= expires_at:
        return _deny(
            TargetReason.PERMISSION_EXPIRED,
            actor_id=actor_id,
            state_kind_id=proposal.get("state_kind_id", ""),
            proposal_hash=proposal_hash,
            before_target_hash=before_target_hash,
        )
    if permission.get("rule_content_hash") != rule_hash:
        return _deny(
            TargetReason.PERMISSION_BINDING_MISMATCH,
            actor_id=actor_id,
            state_kind_id=proposal.get("state_kind_id", ""),
            proposal_hash=proposal_hash,
            before_target_hash=before_target_hash,
        )
    if permission.get("before_target_hash") != before_target_hash:
        return _deny(
            TargetReason.PRESTATE_CONFLICT,
            actor_id=actor_id,
            state_kind_id=proposal.get("state_kind_id", ""),
            proposal_hash=proposal_hash,
            before_target_hash=before_target_hash,
        )
    issuer_ref = permission.get("issuer_ref", "")
    if issuer_ref not in permitted_issuer_refs:
        return _deny(
            TargetReason.PERMISSION_FOREIGN_OWNER,
            actor_id=actor_id,
            state_kind_id=proposal.get("state_kind_id", ""),
            proposal_hash=proposal_hash,
            before_target_hash=before_target_hash,
        )
    semantic_object = proposal.get("semantic_object_ref", "")
    if semantic_object not in entry.get("accepted_semantic_objects", []):
        return _deny(
            TargetReason.SEMANTIC_OBJECT_NOT_ACCEPTED,
            actor_id=actor_id,
            state_kind_id=proposal.get("state_kind_id", ""),
            proposal_hash=proposal_hash,
            before_target_hash=before_target_hash,
        )
    state_kind_id = proposal.get("state_kind_id", "")
    if state_kind_id != entry.get("state_kind_id"):
        return _deny(
            TargetReason.PROPOSAL_INTEGRITY_FAILURE,
            actor_id=actor_id,
            state_kind_id=state_kind_id,
            proposal_hash=proposal_hash,
            before_target_hash=before_target_hash,
        )
    operation = proposal.get("operation", "")
    if operation not in entry.get("allowed_operations", []):
        return _deny(
            TargetReason.PROPOSAL_INTEGRITY_FAILURE,
            actor_id=actor_id,
            state_kind_id=state_kind_id,
            proposal_hash=proposal_hash,
            before_target_hash=before_target_hash,
        )
    target_id = proposal.get("target_middle_state_id") or proposal_hash
    if operation == "CREATE" and target_id in existing_target_ids:
        return _deny(
            TargetReason.DUPLICATE_TARGET_IDENTITY,
            actor_id=actor_id,
            state_kind_id=state_kind_id,
            proposal_hash=proposal_hash,
            before_target_hash=before_target_hash,
        )
    parents = proposal.get("causal_parent_refs") or ()
    if prior_event_hash not in parents:
        return _deny(
            TargetReason.CAUSAL_PARENT_STALE,
            actor_id=actor_id,
            state_kind_id=state_kind_id,
            proposal_hash=proposal_hash,
            before_target_hash=before_target_hash,
        )
    if not enacted_history_refs:
        return _no_change(
            TargetReason.INSUFFICIENT_ENACTED_HISTORY,
            actor_id=actor_id,
            state_kind_id=state_kind_id,
            proposal_hash=proposal_hash,
            before_target_hash=before_target_hash,
            permission_ref=permission.get("grant_id", ""),
        )
    record_body = {
        "schema": "C9P_TARGET_RECORD@1",
        "actor_id": actor_id,
        "middle_state_id": target_id,
        "registry_id": registry.registry_id,
        "registry_version": registry.registry_version,
        "state_kind_id": state_kind_id,
        "semantic_object_ref": semantic_object,
        "lifecycle_status": "ACTIVE",
        "effective_from": proposal.get("proposed_effective_time", as_of),
        "governed_payload": proposal.get("proposed_payload_delta_or_replacement"),
        "creation_rule_ref": rule_hash,
        "causal_parent_refs": list(parents),
        "permission_ref": permission.get("grant_id", ""),
    }
    record = seal(record_body)
    readset = (
        rule_hash,
        permission.get("grant_id", ""),
        prior_event_hash,
        *enacted_history_refs,
    )
    return TargetDecision(
        branch=TargetBranch.CREATE,
        reason=TargetReason.OK,
        actor_id=actor_id,
        state_kind_id=state_kind_id,
        proposal_hash=proposal_hash,
        record_hash=record["hash"],
        before_target_hash=before_target_hash,
        after_target_hash=digest({"before": before_target_hash, "record": record["hash"]}),
        readset_refs=readset,
        permission_ref=permission.get("grant_id", ""),
    )


def make_target_permission(
    *,
    grant_id: str,
    issuer_ref: str,
    actor_id: str,
    rule_content_hash: str,
    before_target_hash: str,
    response_hash: str,
    issued_at: int,
    expires_at: int | None = None,
    revoked: bool = False,
    grade: str = "TEST_ONLY_SOURCEFREE_TECHNICAL",
    issuer_scope: str = "COMMISSION_AUTHORIZED_TEST_ONLY",
) -> dict:
    """Build one sealed target permission for candidate transport."""
    return seal(
        {
            "schema": TARGET_PERMISSION_SCHEMA,
            "grant_id": grant_id,
            "issuer_ref": issuer_ref,
            "issuer_scope": issuer_scope,
            "actor_id": actor_id,
            "rule_content_hash": rule_content_hash,
            "before_target_hash": before_target_hash,
            "response_hash": response_hash,
            "issued_at": issued_at,
            "expires_at": expires_at,
            "revoked": revoked,
            "grade": grade,
        }
    )


__all__ = [
    "DEFAULT_ISSUED_TARGET_RULES",
    "TARGET_PERMISSION_SCHEMA",
    "TARGET_RULE_SCHEMA",
    "TargetBranch",
    "TargetDecision",
    "TargetPermission",
    "TargetReason",
    "TargetRule",
    "TargetRuleRegistry",
    "evaluate_target",
    "make_target_permission",
]
