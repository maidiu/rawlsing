"""Exact source-free PRE553 J family-role/certification succession runtime.

Implements only HQD-122:
exact current J subject/component set + exact family-item-role authority/mapping
-> ComponentAuthorityVectorReceipt(J_FAMILY_ITEM_ROLE)
-> named M1 prerequisite channel
+ exact caller-supplied component evidence premises
-> exact six-state J certification contribution determinant.

No source reads, historical packet execution, Field Forge/B5 effects, product
publication/current-selection, structural admission, or actor/V3 semantics.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

import rawlsing_next.pre553_learned_empirical_adjudication as m1
from rawlsing_next.pre553_component_authority_vector import (
    ComponentAuthorityBinding,
    ComponentAuthorityVectorReceipt,
    authoritative_value_digest,
    build_component_authority_vector_receipt,
    reload_component_authority_vector_receipt,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    Pre553IntegrityError,
    authority_ref,
    canonicalize,
    exact_ref,
    semantic_hash,
)


ROLE_SUCCESSION_CONTRACT_ID = "PRE553_J_FAMILY_ITEM_ROLE_SUCCESSION@1.0.0"
ROLE_AUTHORITY_ID = "PRE553_J_FAMILY_ITEM_ROLE_AUTHORITY"
ROLE_AUTHORITY_VERSION = "1.0.0"
ROLE_AUTHORITY_DIMENSION = "J_FAMILY_ITEM_ROLE"
ROLE_BINDING_METADATA = "FAMILY_ITEM_ROLE_MEMBER"
ROLE_VOCABULARY = (
    "exception_case",
    "elective_case",
    "social_condition",
    "family_size_condition",
    "economic_condition",
    "target_case",
)
ROLE_DIGEST_TO_TOKEN = MappingProxyType(
    {authoritative_value_digest(token): token for token in ROLE_VOCABULARY}
)
ROLE_CHANNEL_ID = "j_family_item_role_vector"
ROLE_CHANNEL_KIND = "PRE553_J_FAMILY_ITEM_ROLE_VECTOR"
ROLE_CHANNEL_RELATION_KINDS = (
    "GOVERNED_FAMILY_ITEM_ROLE_FOR_COMPONENT_SET",
    "ROLE_VECTOR_PREMISE_FOR_J_CERTIFICATION",
)
ROLE_MAPPING_MODE = (
    "EXACT_IDENTITY_SIX_TOKEN_VOCABULARY_WITH_TYPED_NEGATIVE_UNRESOLVED"
)
ROLE_SEMANTIC_CEILING = "J_FAMILY_ITEM_ROLE_PREMISE_ONLY"
CURRENT_JOINT_CONTRACT_ID = "CURRENT_JOINT_AUTHORITY_CONTRACT@1"

CLAIM_FAMILY_ID = "PRE553_J_JOINT_RELATION_EVIDENCE"
CLAIM_RULE_ID = "PRE553_J_COMPONENT_CERTIFICATION_CONTRIBUTION_RULE@1.0.0"
VALIDATOR_ALGORITHM_ID = (
    "PRE553_J_COMPONENT_CERTIFICATION_CONTRIBUTION_VALIDATOR@1.0.0"
)
CONTRIBUTION_VOCABULARY = (
    "relation_component",
    "context_component",
    "special_or_missing_component",
    "explained_nonrelation_component",
    "blocked_component",
    "unresolved_component",
)
CONTEXT_LIKE_CONTRIBUTIONS = (
    "context_component",
    "special_or_missing_component",
    "explained_nonrelation_component",
)
MINIMUM_RELATION_COMPONENTS = 2
J_COMPONENT_PREMISES_SCOPE_KEY = "pre553_j_component_certification_premises"
J_M1_SEMANTIC_CEILING = (
    m1.M1_DEFAULT_SEMANTIC_CEILING
    + "__J_FAMILY_ROLE_EXACT_AUTHORITY_REQUIRED"
    + "__NO_NEGATIVE_OR_UNKNOWN_ROLE_RELATION_PROMOTION"
)

_ROLE_STATES = frozenset({"VALUE", "UNRESOLVED", "DENIED", "NONCOMPARABLE"})
_BLOCKED_ROLE_STATES = frozenset({"DENIED", "NONCOMPARABLE"})
_MATCH_STATES = frozenset({
    "ACCEPTED_MATCH",
    "AMBIGUOUS_MATCH",
    "NO_ACCEPTED_MATCH",
    "UNRESOLVED_MATCH",
    "DENIED",
    "CONFLICTING",
})
_ELIGIBILITY_STATES = frozenset({
    "ELIGIBLE_RELATION",
    "CONTEXT_OR_NONRELATION",
    "NOT_REQUIRED",
    "UNRESOLVED",
    "DENIED",
    "NONCOMPARABLE",
    "CONFLICTING",
})
_BLOCKED_MATCH_STATES = frozenset({"AMBIGUOUS_MATCH", "DENIED", "CONFLICTING"})
_BLOCKED_ELIGIBILITY_STATES = frozenset(
    {"DENIED", "NONCOMPARABLE", "CONFLICTING"}
)


class JRoleCertificationError(Pre553IntegrityError):
    """Exact J succession contract/replay material is malformed."""


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise JRoleCertificationError(f"{name} must be non-empty exact string")
    return value.strip()


def _positive_int(value: Any, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise JRoleCertificationError(f"{name} must be positive integer")
    return value


def _refs(
    values: Iterable[ExactRef | Mapping[str, Any]], name: str
) -> tuple[ExactRef, ...]:
    refs = tuple(exact_ref(value, name) for value in values)
    return tuple(sorted(set(refs), key=lambda ref: ref.key))


def _authority_refs(
    values: Iterable[AuthorityRef | Mapping[str, Any]], name: str
) -> tuple[AuthorityRef, ...]:
    refs = tuple(authority_ref(value, name) for value in values)
    return tuple(sorted(set(refs), key=lambda ref: ref.key))


def _derived_ref(kind: str, label: str, material: Any) -> ExactRef:
    digest = semantic_hash(material)
    return ExactRef(kind, f"urn:rawlsing:pre553:j:{label}:sha256:{digest}", digest)


def _role_authority(value: AuthorityRef | Mapping[str, Any]) -> AuthorityRef:
    ref = authority_ref(value, "role_authority_ref")
    if (
        ref.authority_id != ROLE_AUTHORITY_ID
        or ref.authority_version != ROLE_AUTHORITY_VERSION
    ):
        raise JRoleCertificationError(
            "J family-role authority must use exact adopted authority id/version"
        )
    return ref


def _governed_ids(values: Sequence[str], name: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise JRoleCertificationError(f"{name} must be explicit ordered sequence")
    result = tuple(_text(value, name) for value in values)
    if not result or len(set(result)) != len(result):
        raise JRoleCertificationError(f"{name} must be nonempty and unique")
    return result


@dataclass(frozen=True)
class JFamilyRoleAssignment:
    component_id: str
    component_ref: ExactRef
    ordinal: int
    authority_state: str
    role_token: str | None
    value_authority_ref: AuthorityRef
    succession_invoked: bool
    predecessor_current_mapping_ref: ExactRef | None = None
    dependency_refs: tuple[ExactRef, ...] = ()
    negative_or_limit_refs: tuple[ExactRef, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "component_id", _text(self.component_id, "component_id"))
        object.__setattr__(
            self, "component_ref", exact_ref(self.component_ref, "component_ref")
        )
        object.__setattr__(self, "ordinal", _positive_int(self.ordinal, "ordinal"))
        if self.authority_state not in _ROLE_STATES:
            raise JRoleCertificationError("unknown J family-role authority state")
        object.__setattr__(
            self,
            "value_authority_ref",
            authority_ref(self.value_authority_ref, "value_authority_ref"),
        )
        if not isinstance(self.succession_invoked, bool):
            raise JRoleCertificationError("succession_invoked must be boolean")
        if self.predecessor_current_mapping_ref is not None:
            object.__setattr__(
                self,
                "predecessor_current_mapping_ref",
                exact_ref(
                    self.predecessor_current_mapping_ref,
                    "predecessor_current_mapping_ref",
                ),
            )
        object.__setattr__(
            self,
            "dependency_refs",
            _refs(self.dependency_refs, "role_assignment_dependency_ref"),
        )
        object.__setattr__(
            self,
            "negative_or_limit_refs",
            _refs(
                self.negative_or_limit_refs,
                "role_assignment_negative_or_limit_ref",
            ),
        )
        if self.authority_state == "VALUE":
            if self.role_token not in ROLE_VOCABULARY:
                raise JRoleCertificationError(
                    "VALUE role assignment requires exact six-token role"
                )
        elif self.role_token is not None:
            raise JRoleCertificationError(
                "non-VALUE role assignment may not carry role token"
            )
        if (
            self.authority_state in _BLOCKED_ROLE_STATES
            and not self.negative_or_limit_refs
        ):
            raise JRoleCertificationError(
                f"{self.authority_state} requires exact negative/limit ref"
            )


@dataclass(frozen=True)
class JComponentCertificationPremise:
    component_id: str
    component_ref: ExactRef
    ordinal: int
    evidence_match_disposition: str
    relation_eligibility_disposition: str
    special_or_missing_response: bool = False
    governed_nonrelation_explained: bool = False
    authority_refs: tuple[AuthorityRef, ...] = ()
    dependency_refs: tuple[ExactRef, ...] = ()
    negative_or_limit_refs: tuple[ExactRef, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "component_id", _text(self.component_id, "component_id"))
        object.__setattr__(
            self, "component_ref", exact_ref(self.component_ref, "component_ref")
        )
        object.__setattr__(self, "ordinal", _positive_int(self.ordinal, "ordinal"))
        if self.evidence_match_disposition not in _MATCH_STATES:
            raise JRoleCertificationError("unknown evidence-match disposition")
        if self.relation_eligibility_disposition not in _ELIGIBILITY_STATES:
            raise JRoleCertificationError("unknown relation-eligibility disposition")
        if not isinstance(self.special_or_missing_response, bool):
            raise JRoleCertificationError("special_or_missing_response must be boolean")
        if not isinstance(self.governed_nonrelation_explained, bool):
            raise JRoleCertificationError(
                "governed_nonrelation_explained must be boolean"
            )
        if self.special_or_missing_response and self.governed_nonrelation_explained:
            raise JRoleCertificationError(
                "component cannot be both special/missing and explained nonrelation"
            )
        object.__setattr__(
            self,
            "authority_refs",
            _authority_refs(self.authority_refs, "component_premise_authority_ref"),
        )
        object.__setattr__(
            self,
            "dependency_refs",
            _refs(self.dependency_refs, "component_premise_dependency_ref"),
        )
        object.__setattr__(
            self,
            "negative_or_limit_refs",
            _refs(
                self.negative_or_limit_refs,
                "component_premise_negative_or_limit_ref",
            ),
        )

    def as_dict(self) -> Mapping[str, Any]:
        return {
            "component_id": self.component_id,
            "component_ref": self.component_ref.as_dict(),
            "ordinal": self.ordinal,
            "evidence_match_disposition": self.evidence_match_disposition,
            "relation_eligibility_disposition": self.relation_eligibility_disposition,
            "special_or_missing_response": self.special_or_missing_response,
            "governed_nonrelation_explained": self.governed_nonrelation_explained,
            "authority_refs": [ref.as_dict() for ref in self.authority_refs],
            "dependency_refs": [ref.as_dict() for ref in self.dependency_refs],
            "negative_or_limit_refs": [
                ref.as_dict() for ref in self.negative_or_limit_refs
            ],
        }

    @classmethod
    def from_dict(
        cls, value: Mapping[str, Any]
    ) -> "JComponentCertificationPremise":
        fields = {
            "component_id",
            "component_ref",
            "ordinal",
            "evidence_match_disposition",
            "relation_eligibility_disposition",
            "special_or_missing_response",
            "governed_nonrelation_explained",
            "authority_refs",
            "dependency_refs",
            "negative_or_limit_refs",
        }
        if not isinstance(value, Mapping) or set(value) != fields:
            raise JRoleCertificationError(
                "component premise must carry exact field set"
            )
        return cls(
            component_id=value["component_id"],
            component_ref=exact_ref(value["component_ref"], "component_ref"),
            ordinal=value["ordinal"],
            evidence_match_disposition=value["evidence_match_disposition"],
            relation_eligibility_disposition=value[
                "relation_eligibility_disposition"
            ],
            special_or_missing_response=value["special_or_missing_response"],
            governed_nonrelation_explained=value[
                "governed_nonrelation_explained"
            ],
            authority_refs=tuple(
                authority_ref(ref, "component_premise_authority_ref")
                for ref in value["authority_refs"]
            ),
            dependency_refs=tuple(
                exact_ref(ref, "component_premise_dependency_ref")
                for ref in value["dependency_refs"]
            ),
            negative_or_limit_refs=tuple(
                exact_ref(ref, "component_premise_negative_or_limit_ref")
                for ref in value["negative_or_limit_refs"]
            ),
        )


def build_j_family_item_role_vector(
    *,
    vector_subject_ref: ExactRef | Mapping[str, Any],
    governed_component_ids: Sequence[str],
    role_contract_ref: ExactRef | Mapping[str, Any],
    mapping_contract_ref: ExactRef | Mapping[str, Any],
    role_authority_ref: AuthorityRef | Mapping[str, Any],
    role_assignments: Sequence[JFamilyRoleAssignment],
    replay_contract_ref: ExactRef | Mapping[str, Any],
    dependency_refs: Iterable[ExactRef | Mapping[str, Any]] = (),
) -> ComponentAuthorityVectorReceipt:
    """Produce exact J_FAMILY_ITEM_ROLE vector; missing mapping stays unresolved."""
    subject = exact_ref(vector_subject_ref, "vector_subject_ref")
    governed = _governed_ids(governed_component_ids, "governed_component_ids")
    role_contract = exact_ref(role_contract_ref, "role_contract_ref")
    mapping_contract = exact_ref(mapping_contract_ref, "mapping_contract_ref")
    role_authority = _role_authority(role_authority_ref)
    replay_contract = exact_ref(replay_contract_ref, "replay_contract_ref")
    dependencies = _refs(dependency_refs, "role_vector_dependency_ref")
    if isinstance(role_assignments, (str, bytes)) or not isinstance(
        role_assignments, Sequence
    ):
        raise JRoleCertificationError("role_assignments must be explicit sequence")
    assignments = tuple(role_assignments)
    if not assignments or any(
        not isinstance(row, JFamilyRoleAssignment) for row in assignments
    ):
        raise JRoleCertificationError(
            "role_assignments require exact JFamilyRoleAssignment rows"
        )
    by_id = {component_id: [] for component_id in governed}
    for row in assignments:
        if row.component_id not in by_id:
            raise JRoleCertificationError(
                "role assignment outside governed component set"
            )
        if row.value_authority_ref != role_authority:
            raise JRoleCertificationError(
                "per-value role authority must equal exact adopted role authority"
            )
        by_id[row.component_id].append(row)
    if any(len(rows) != 1 for rows in by_id.values()):
        raise JRoleCertificationError(
            "producer requires exactly one role assignment per component"
        )
    ordered = tuple(by_id[component_id][0] for component_id in governed)
    if tuple(row.ordinal for row in ordered) != tuple(
        range(1, len(governed) + 1)
    ):
        raise JRoleCertificationError(
            "role assignment ordinals must equal governed component order"
        )

    bindings = []
    replay_rows = []
    for row in ordered:
        state = row.authority_state
        token = row.role_token
        if (
            state == "VALUE"
            and row.succession_invoked
            and row.predecessor_current_mapping_ref is None
        ):
            state, token = "UNRESOLVED", None
        bindings.append(
            ComponentAuthorityBinding(
                component_id=row.component_id,
                component_ref=row.component_ref,
                producer_family=ROLE_SUCCESSION_CONTRACT_ID,
                role=ROLE_BINDING_METADATA,
                ordinal_or_null=row.ordinal,
                multiplicity_index=0,
                authority_state=state,
                authoritative_value_digest=(
                    authoritative_value_digest(token)
                    if state == "VALUE"
                    else None
                ),
                value_authority_ref=row.value_authority_ref,
                negative_or_limit_refs=row.negative_or_limit_refs,
            )
        )
        replay_rows.append({
            "component_id": row.component_id,
            "component_ref": row.component_ref.as_dict(),
            "ordinal": row.ordinal,
            "effective_authority_state": state,
            "effective_role_token": token,
            "value_authority_ref": row.value_authority_ref.as_dict(),
            "succession_invoked": row.succession_invoked,
            "predecessor_current_mapping_ref": (
                None
                if row.predecessor_current_mapping_ref is None
                else row.predecessor_current_mapping_ref.as_dict()
            ),
            "dependency_refs": [
                ref.as_dict() for ref in row.dependency_refs
            ],
            "negative_or_limit_refs": [
                ref.as_dict() for ref in row.negative_or_limit_refs
            ],
        })
    replay_root = _derived_ref(
        "PRE553JRoleVectorReplay",
        "role-vector-replay",
        {
            "contract_id": ROLE_SUCCESSION_CONTRACT_ID,
            "authority_dimension": ROLE_AUTHORITY_DIMENSION,
            "vector_subject_ref": subject.as_dict(),
            "governed_component_ids": list(governed),
            "role_contract_ref": role_contract.as_dict(),
            "mapping_contract_ref": mapping_contract.as_dict(),
            "role_authority_ref": role_authority.as_dict(),
            "role_assignments": replay_rows,
            "replay_contract_ref": replay_contract.as_dict(),
            "dependency_refs": [ref.as_dict() for ref in dependencies],
        },
    )
    return build_component_authority_vector_receipt(
        vector_subject_ref=subject,
        authority_dimension_contract_ref=role_contract,
        vector_rule_authority_ref=role_authority,
        governed_component_ids=governed,
        component_bindings=tuple(bindings),
        producer_replay_locator_or_reference_root=replay_root,
    )


def _claimed_vector_ref(value: Any) -> ExactRef | None:
    if isinstance(value, ComponentAuthorityVectorReceipt):
        return value.ref
    if isinstance(value, Mapping):
        try:
            return ExactRef(
                "ComponentAuthorityVectorReceipt@1.0.0",
                value["object_id"],
                value["content_hash"],
            )
        except Exception:
            return None
    return None


def _make_role_channel(
    *,
    state: str,
    reason_code: str | None,
    role_vector_ref: ExactRef,
    role_vector_snapshot: Mapping[str, Any],
    expected_subject_ref: ExactRef,
    expected_component_ids: tuple[str, ...],
    role_contract_ref: ExactRef,
    mapping_contract_ref: ExactRef,
    expected_role_authority_ref: AuthorityRef,
    current_subject_family_authority_ref: AuthorityRef,
    component_mapping_refs: Mapping[str, ExactRef | None],
    replay_contract_ref: ExactRef,
    replay_refs: tuple[ExactRef, ...],
    value_authority_refs: tuple[AuthorityRef, ...],
    dependency_refs: tuple[ExactRef, ...],
    coverage_proof_hash: str | None,
) -> m1.M1PrerequisiteChannel:
    detail = {
        "contract_id": ROLE_SUCCESSION_CONTRACT_ID,
        "authority_dimension": ROLE_AUTHORITY_DIMENSION,
        "vector_subject_ref": expected_subject_ref.as_dict(),
        "role_vector_ref": role_vector_ref.as_dict(),
        "role_vector_snapshot": canonicalize(role_vector_snapshot),
        "governed_component_ids": list(expected_component_ids),
        "role_vocabulary_version": ROLE_SUCCESSION_CONTRACT_ID,
        "role_vocabulary": list(ROLE_VOCABULARY),
        "mapping_mode": ROLE_MAPPING_MODE,
        "mapping_contract_ref": mapping_contract_ref.as_dict(),
        "component_mapping_refs": {
            component_id: None if ref is None else ref.as_dict()
            for component_id, ref in component_mapping_refs.items()
        },
        "current_joint_contract": CURRENT_JOINT_CONTRACT_ID,
        "semantic_ceiling": ROLE_SEMANTIC_CEILING,
        "expected_role_authority_ref": expected_role_authority_ref.as_dict(),
        "current_subject_family_authority_ref": (
            current_subject_family_authority_ref.as_dict()
        ),
        "value_authority_refs": [
            ref.as_dict() for ref in value_authority_refs
        ],
        "role_contract_ref": role_contract_ref.as_dict(),
        "replay_contract_ref": replay_contract_ref.as_dict(),
        "replay_refs": [ref.as_dict() for ref in replay_refs],
        "role_vector_coverage_proof_hash": coverage_proof_hash,
    }
    if reason_code is not None:
        detail["terminal_reason_code"] = reason_code
    return m1.M1PrerequisiteChannel(
        channel_id=ROLE_CHANNEL_ID,
        channel_kind=ROLE_CHANNEL_KIND,
        state=state,
        authority_refs=_authority_refs(
            (
                expected_role_authority_ref,
                current_subject_family_authority_ref,
                *value_authority_refs,
            ),
            "role_channel_authority_ref",
        ),
        dependency_refs=dependency_refs,
        relation_kinds=ROLE_CHANNEL_RELATION_KINDS,
        detail=detail,
    )


def build_j_family_item_role_channel(
    *,
    role_vector: ComponentAuthorityVectorReceipt | Mapping[str, Any],
    expected_subject_ref: ExactRef | Mapping[str, Any],
    expected_component_ids: Sequence[str],
    role_contract_ref: ExactRef | Mapping[str, Any],
    mapping_contract_ref: ExactRef | Mapping[str, Any],
    expected_role_authority_ref: AuthorityRef | Mapping[str, Any],
    current_subject_family_authority_ref: AuthorityRef | Mapping[str, Any],
    component_mapping_refs: Mapping[
        str, ExactRef | Mapping[str, Any] | None
    ],
    succession_component_ids: Iterable[str],
    replay_contract_ref: ExactRef | Mapping[str, Any],
    replay_refs: Iterable[ExactRef | Mapping[str, Any]],
) -> m1.M1PrerequisiteChannel:
    """Validate role-vector authority/mapping/replay and build named M1 channel."""
    subject = exact_ref(expected_subject_ref, "expected_subject_ref")
    expected_ids = _governed_ids(
        expected_component_ids, "expected_component_ids"
    )
    role_contract = exact_ref(role_contract_ref, "role_contract_ref")
    mapping_contract = exact_ref(mapping_contract_ref, "mapping_contract_ref")
    role_authority = _role_authority(expected_role_authority_ref)
    subject_authority = authority_ref(
        current_subject_family_authority_ref,
        "current_subject_family_authority_ref",
    )
    replay_contract = exact_ref(replay_contract_ref, "replay_contract_ref")
    exact_replay_refs = _refs(replay_refs, "role_vector_replay_ref")
    succession_ids = frozenset(
        _text(value, "succession_component_id")
        for value in succession_component_ids
    )
    if not succession_ids.issubset(set(expected_ids)):
        raise JRoleCertificationError(
            "succession_component_ids outside expected component set"
        )
    if not isinstance(component_mapping_refs, Mapping):
        raise JRoleCertificationError(
            "component_mapping_refs must be exact mapping"
        )
    if set(component_mapping_refs) != set(expected_ids):
        raise JRoleCertificationError(
            "component_mapping_refs must name exact component set"
        )
    exact_mappings = {
        component_id: (
            None
            if component_mapping_refs[component_id] is None
            else exact_ref(
                component_mapping_refs[component_id],
                "component_mapping_ref",
            )
        )
        for component_id in expected_ids
    }

    claimed_ref = _claimed_vector_ref(role_vector)
    if claimed_ref is None:
        claimed_ref = _derived_ref(
            "ComponentAuthorityVectorReceipt@1.0.0",
            "unreadable-role-vector",
            canonicalize(role_vector),
        )
    snapshot = (
        role_vector.as_dict()
        if isinstance(role_vector, ComponentAuthorityVectorReceipt)
        else dict(role_vector)
    )
    try:
        vector = (
            role_vector
            if isinstance(role_vector, ComponentAuthorityVectorReceipt)
            else reload_component_authority_vector_receipt(role_vector)
        )
    except Exception:
        dependencies = _refs(
            (
                claimed_ref,
                role_contract,
                mapping_contract,
                replay_contract,
                *[
                    ref
                    for ref in exact_mappings.values()
                    if ref is not None
                ],
                *exact_replay_refs,
            ),
            "role_channel_dependency_ref",
        )
        return _make_role_channel(
            state="INTEGRITY_FAILURE",
            reason_code="J_ROLE_VECTOR_REPLAY_MISMATCH",
            role_vector_ref=claimed_ref,
            role_vector_snapshot=snapshot,
            expected_subject_ref=subject,
            expected_component_ids=expected_ids,
            role_contract_ref=role_contract,
            mapping_contract_ref=mapping_contract,
            expected_role_authority_ref=role_authority,
            current_subject_family_authority_ref=subject_authority,
            component_mapping_refs=exact_mappings,
            replay_contract_ref=replay_contract,
            replay_refs=exact_replay_refs,
            value_authority_refs=(),
            dependency_refs=dependencies,
            coverage_proof_hash=None,
        )

    by_id: dict[str, list[ComponentAuthorityBinding]] = {
        component_id: [] for component_id in vector.governed_component_ids
    }
    for binding in vector.component_bindings:
        by_id.setdefault(binding.component_id, []).append(binding)
    value_authorities = _authority_refs(
        (
            binding.value_authority_ref
            for binding in vector.component_bindings
            if binding.authority_state == "VALUE"
        ),
        "role_value_authority_ref",
    )
    producer_replay = (
        vector.producer_replay_locator_or_reference_root
        if isinstance(
            vector.producer_replay_locator_or_reference_root, ExactRef
        )
        else None
    )
    dependencies = _refs(
        (
            vector.ref,
            role_contract,
            mapping_contract,
            replay_contract,
            *[
                ref for ref in exact_mappings.values() if ref is not None
            ],
            *exact_replay_refs,
        ),
        "role_channel_dependency_ref",
    )

    state, reason = "SATISFIED", None
    if vector.vector_subject_ref != subject:
        state, reason = "BLOCKED", "J_ROLE_PREREQUISITE_BLOCKED"
    elif vector.governed_component_ids != expected_ids:
        state, reason = "INTEGRITY_FAILURE", "J_COMPONENT_SET_MISMATCH"
    elif vector.authority_dimension_contract_ref != role_contract:
        state, reason = "BLOCKED", "J_ROLE_PREREQUISITE_BLOCKED"
    elif vector.vector_rule_authority_ref != role_authority:
        state, reason = "BLOCKED", "J_ROLE_PREREQUISITE_BLOCKED"
    elif vector.ambiguous_component_ids:
        state, reason = "BLOCKED", "J_ROLE_PREREQUISITE_BLOCKED"
    elif vector.denied_component_ids or vector.noncomparable_component_ids:
        state, reason = "BLOCKED", "J_ROLE_PREREQUISITE_BLOCKED"
    elif (
        vector.missing_component_ids
        or vector.unresolved_component_ids
        or vector.governed_empty_component_ids
    ):
        state, reason = "UNRESOLVED", "J_ROLE_PREREQUISITE_UNRESOLVED"
    else:
        for component_id in expected_ids:
            rows = by_id.get(component_id, ())
            if len(rows) != 1:
                state, reason = (
                    "BLOCKED",
                    "J_ROLE_PREREQUISITE_BLOCKED",
                )
                break
            binding = rows[0]
            if binding.authority_state != "VALUE":
                state, reason = (
                    "UNRESOLVED",
                    "J_ROLE_PREREQUISITE_UNRESOLVED",
                )
                break
            if (
                binding.authoritative_value_digest
                not in ROLE_DIGEST_TO_TOKEN
                or binding.role != ROLE_BINDING_METADATA
            ):
                state, reason = (
                    "INTEGRITY_FAILURE",
                    "UNKNOWN_ROLE_TOKEN_CONTRACT_FAILURE",
                )
                break
            if (
                component_id in succession_ids
                and exact_mappings[component_id] is None
            ):
                state, reason = (
                    "UNRESOLVED",
                    "J_ROLE_PREREQUISITE_UNRESOLVED",
                )
                break
    if state == "SATISFIED" and (
        producer_replay is None or producer_replay not in exact_replay_refs
    ):
        state, reason = (
            "INTEGRITY_FAILURE",
            "J_ROLE_VECTOR_REPLAY_MISMATCH",
        )

    return _make_role_channel(
        state=state,
        reason_code=reason,
        role_vector_ref=vector.ref,
        role_vector_snapshot=vector.as_dict(),
        expected_subject_ref=subject,
        expected_component_ids=expected_ids,
        role_contract_ref=role_contract,
        mapping_contract_ref=mapping_contract,
        expected_role_authority_ref=role_authority,
        current_subject_family_authority_ref=subject_authority,
        component_mapping_refs=exact_mappings,
        replay_contract_ref=replay_contract,
        replay_refs=exact_replay_refs,
        value_authority_refs=value_authorities,
        dependency_refs=dependencies,
        coverage_proof_hash=vector.coverage_proof_hash,
    )


def build_j_component_premise_scope(
    premises: Sequence[JComponentCertificationPremise],
    *,
    base_scope: Mapping[str, Any] | None = None,
) -> Mapping[str, Any]:
    """Bind exact caller-owned component premises into M1 requested_scope."""
    if isinstance(premises, (str, bytes)) or not isinstance(
        premises, Sequence
    ):
        raise JRoleCertificationError("premises must be explicit sequence")
    rows = tuple(premises)
    if not rows or any(
        not isinstance(row, JComponentCertificationPremise)
        for row in rows
    ):
        raise JRoleCertificationError(
            "premises require exact JComponentCertificationPremise rows"
        )
    ordered = tuple(sorted(rows, key=lambda row: row.ordinal))
    if len({row.component_id for row in ordered}) != len(ordered):
        raise JRoleCertificationError("duplicate component premise")
    if len({row.ordinal for row in ordered}) != len(ordered):
        raise JRoleCertificationError("duplicate component premise ordinal")
    result = {} if base_scope is None else dict(canonicalize(base_scope))
    if J_COMPONENT_PREMISES_SCOPE_KEY in result:
        raise JRoleCertificationError(
            "base scope already owns J component premise key"
        )
    result[J_COMPONENT_PREMISES_SCOPE_KEY] = [
        row.as_dict() for row in ordered
    ]
    return result


def j_validator_parameters_ref(
    *,
    role_contract_ref: ExactRef | Mapping[str, Any],
    mapping_contract_ref: ExactRef | Mapping[str, Any],
    role_authority_ref: AuthorityRef | Mapping[str, Any],
    current_selection_authority_ref: AuthorityRef | Mapping[str, Any],
) -> ExactRef:
    role_contract = exact_ref(role_contract_ref, "role_contract_ref")
    mapping_contract = exact_ref(mapping_contract_ref, "mapping_contract_ref")
    role_authority = _role_authority(role_authority_ref)
    selection_authority = authority_ref(
        current_selection_authority_ref,
        "current_selection_authority_ref",
    )
    return _derived_ref(
        "M1ValidatorParameters",
        "j-certification-validator-parameters",
        {
            "claim_family_id": CLAIM_FAMILY_ID,
            "claim_rule_id": CLAIM_RULE_ID,
            "validator_algorithm_identity": VALIDATOR_ALGORITHM_ID,
            "role_contract_ref": role_contract.as_dict(),
            "mapping_contract_ref": mapping_contract.as_dict(),
            "role_authority_ref": role_authority.as_dict(),
            "current_selection_authority_ref": (
                selection_authority.as_dict()
            ),
            "role_vocabulary": list(ROLE_VOCABULARY),
            "contribution_vocabulary": list(CONTRIBUTION_VOCABULARY),
            "minimum_relation_components": MINIMUM_RELATION_COMPONENTS,
            "context_like_contributions": list(
                CONTEXT_LIKE_CONTRIBUTIONS
            ),
        },
    )


def build_j_family_rule_binding(
    *,
    validator_authority_ref: AuthorityRef | Mapping[str, Any],
    current_selection_authority_ref: AuthorityRef | Mapping[str, Any],
    role_authority_ref: AuthorityRef | Mapping[str, Any],
    role_contract_ref: ExactRef | Mapping[str, Any],
    mapping_contract_ref: ExactRef | Mapping[str, Any],
    uncertainty_policy_ref: ExactRef | Mapping[str, Any],
    replay_contract_ref: ExactRef | Mapping[str, Any],
    allowed_input_object_families_and_states: Mapping[str, Any],
    required_coverage_strength: Mapping[str, Any],
    additional_authority_closure_refs: Iterable[
        AuthorityRef | Mapping[str, Any]
    ] = (),
) -> m1.M1FamilyRuleBinding:
    validator_authority = authority_ref(
        validator_authority_ref, "validator_authority_ref"
    )
    selection_authority = authority_ref(
        current_selection_authority_ref,
        "current_selection_authority_ref",
    )
    role_authority = _role_authority(role_authority_ref)
    role_contract = exact_ref(role_contract_ref, "role_contract_ref")
    mapping_contract = exact_ref(
        mapping_contract_ref, "mapping_contract_ref"
    )
    uncertainty_policy = exact_ref(
        uncertainty_policy_ref, "uncertainty_policy_ref"
    )
    replay_contract = exact_ref(replay_contract_ref, "replay_contract_ref")
    closure = _authority_refs(
        (
            validator_authority,
            selection_authority,
            *tuple(additional_authority_closure_refs),
        ),
        "j_rule_binding_authority_closure_ref",
    )
    return m1.M1FamilyRuleBinding(
        claim_family_id=CLAIM_FAMILY_ID,
        claim_rule_id=CLAIM_RULE_ID,
        validator_authority_ref=validator_authority,
        selection_purpose="CURRENT_GOVERNED_USE",
        current_selection_authority_ref=selection_authority,
        applicability_scope={
            "source_universe_refs": "EXPLICIT_UNRESTRICTED",
            "risk_set_refs": "EXPLICIT_UNRESTRICTED",
            "measure_basis_refs": "EXPLICIT_UNRESTRICTED",
            "topology_scope_material": "EXPLICIT_UNRESTRICTED",
            "requested_scope": "EXPLICIT_UNRESTRICTED",
            "j_family_item_role_authority_ref": (
                role_authority.as_dict()
            ),
            "j_role_contract_ref": role_contract.as_dict(),
            "j_mapping_contract_ref": mapping_contract.as_dict(),
            "j_current_selection_authority_ref": (
                selection_authority.as_dict()
            ),
        },
        allowed_input_object_families_and_states=(
            allowed_input_object_families_and_states
        ),
        required_prerequisite_channels=(ROLE_CHANNEL_ID,),
        required_source_relation_kinds=ROLE_CHANNEL_RELATION_KINDS,
        required_measure_weight_estimand_authorities=(),
        required_coverage_strength=required_coverage_strength,
        uncertainty_policy_ref=uncertainty_policy,
        output_semantic_contract={
            "truth_bearing_claim_emission": "PROHIBITED",
            "j_relation_promotion_requires_exact_positive_family_role_authority": True,
            "negative_or_unknown_family_role_relation_promotion": "PROHIBITED",
        },
        semantic_ceiling=J_M1_SEMANTIC_CEILING,
        validator_algorithm_identity_if_required=(
            VALIDATOR_ALGORITHM_ID
        ),
        validator_parameters_ref=j_validator_parameters_ref(
            role_contract_ref=role_contract,
            mapping_contract_ref=mapping_contract,
            role_authority_ref=role_authority,
            current_selection_authority_ref=selection_authority,
        ),
        replay_contract_ref=replay_contract,
        authority_closure_refs=closure,
    )


def _validate_j_binding(binding: m1.M1FamilyRuleBinding) -> None:
    if (
        binding.claim_family_id != CLAIM_FAMILY_ID
        or binding.claim_rule_id != CLAIM_RULE_ID
    ):
        raise JRoleCertificationError(
            "J validator binding claim identity mismatch"
        )
    if (
        binding.selection_purpose != "CURRENT_GOVERNED_USE"
        or binding.current_selection_authority_ref is None
    ):
        raise JRoleCertificationError(
            "J validator requires exact CURRENT_GOVERNED_USE authority"
        )
    if (
        binding.validator_algorithm_identity_if_required
        != VALIDATOR_ALGORITHM_ID
    ):
        raise JRoleCertificationError(
            "J validator algorithm identity mismatch"
        )
    if binding.required_prerequisite_channels != (ROLE_CHANNEL_ID,):
        raise JRoleCertificationError(
            "J validator requires exact named role prerequisite"
        )
    if set(binding.required_source_relation_kinds) != set(
        ROLE_CHANNEL_RELATION_KINDS
    ):
        raise JRoleCertificationError(
            "J validator required relation-kind contract mismatch"
        )
    if binding.semantic_ceiling != J_M1_SEMANTIC_CEILING:
        raise JRoleCertificationError(
            "J validator semantic ceiling mismatch"
        )
    scope = binding.applicability_scope
    role_authority = _role_authority(
        scope["j_family_item_role_authority_ref"]
    )
    role_contract = exact_ref(
        scope["j_role_contract_ref"], "j_role_contract_ref"
    )
    mapping_contract = exact_ref(
        scope["j_mapping_contract_ref"], "j_mapping_contract_ref"
    )
    selection_authority = authority_ref(
        scope["j_current_selection_authority_ref"],
        "j_current_selection_authority_ref",
    )
    if selection_authority != binding.current_selection_authority_ref:
        raise JRoleCertificationError(
            "J current-selection authority binding mismatch"
        )
    if binding.validator_parameters_ref != j_validator_parameters_ref(
        role_contract_ref=role_contract,
        mapping_contract_ref=mapping_contract,
        role_authority_ref=role_authority,
        current_selection_authority_ref=selection_authority,
    ):
        raise JRoleCertificationError(
            "J validator parameter identity mismatch"
        )


def build_j_validator_registry(
    binding: m1.M1FamilyRuleBinding,
) -> m1.M1ValidatorRegistry:
    _validate_j_binding(binding)
    return m1.M1ValidatorRegistry(
        (
            m1.FamilyValidatorRegistration.from_binding(
                binding, j_component_certification_validator
            ),
        )
    )


def _load_role_channel(
    context: m1.M1ValidatorContext,
) -> tuple[
    m1.M1PrerequisiteChannel,
    ComponentAuthorityVectorReceipt,
    Mapping[str, Any],
]:
    channel = context.evidence_context["prerequisite_channels"].get(
        ROLE_CHANNEL_ID
    )
    if (
        channel is None
        or channel.channel_kind != ROLE_CHANNEL_KIND
        or channel.state != "SATISFIED"
    ):
        raise JRoleCertificationError(
            "exact SATISFIED J role prerequisite channel missing"
        )
    if set(channel.relation_kinds) != set(ROLE_CHANNEL_RELATION_KINDS):
        raise JRoleCertificationError(
            "J role prerequisite relation kinds mismatch"
        )
    detail = channel.detail
    required = {
        "contract_id",
        "authority_dimension",
        "vector_subject_ref",
        "role_vector_ref",
        "role_vector_snapshot",
        "governed_component_ids",
        "role_vocabulary_version",
        "role_vocabulary",
        "mapping_mode",
        "mapping_contract_ref",
        "component_mapping_refs",
        "current_joint_contract",
        "semantic_ceiling",
        "expected_role_authority_ref",
        "current_subject_family_authority_ref",
        "value_authority_refs",
        "role_contract_ref",
        "replay_contract_ref",
        "replay_refs",
        "role_vector_coverage_proof_hash",
    }
    if set(detail) != required:
        raise JRoleCertificationError(
            "J role prerequisite detail contract mismatch"
        )
    if (
        detail["contract_id"] != ROLE_SUCCESSION_CONTRACT_ID
        or detail["authority_dimension"] != ROLE_AUTHORITY_DIMENSION
        or detail["role_vocabulary_version"]
        != ROLE_SUCCESSION_CONTRACT_ID
        or tuple(detail["role_vocabulary"]) != ROLE_VOCABULARY
        or detail["mapping_mode"] != ROLE_MAPPING_MODE
        or detail["current_joint_contract"] != CURRENT_JOINT_CONTRACT_ID
        or detail["semantic_ceiling"] != ROLE_SEMANTIC_CEILING
    ):
        raise JRoleCertificationError(
            "J role prerequisite semantic contract mismatch"
        )
    vector = reload_component_authority_vector_receipt(
        detail["role_vector_snapshot"]
    )
    if vector.ref != exact_ref(
        detail["role_vector_ref"], "role_vector_ref"
    ):
        raise JRoleCertificationError("J role vector replay/ref mismatch")
    if (
        vector.coverage_proof_hash
        != detail["role_vector_coverage_proof_hash"]
    ):
        raise JRoleCertificationError(
            "J role vector coverage proof mismatch"
        )
    return channel, vector, detail


def _premises(
    context: m1.M1ValidatorContext,
    vector: ComponentAuthorityVectorReceipt,
) -> tuple[JComponentCertificationPremise, ...]:
    raw = context.input_bundle.requested_scope.get(
        J_COMPONENT_PREMISES_SCOPE_KEY
    )
    if (
        not isinstance(raw, Sequence)
        or isinstance(raw, (str, bytes))
        or not raw
    ):
        raise JRoleCertificationError(
            "exact J component premise vector missing"
        )
    rows = tuple(
        JComponentCertificationPremise.from_dict(value) for value in raw
    )
    ordered = tuple(sorted(rows, key=lambda row: row.ordinal))
    if tuple(row.ordinal for row in ordered) != tuple(
        range(1, len(ordered) + 1)
    ):
        raise JRoleCertificationError(
            "J component premise ordinal mismatch"
        )
    if tuple(
        row.component_id for row in ordered
    ) != vector.governed_component_ids:
        raise JRoleCertificationError(
            "J component premise set/order mismatch"
        )
    by_id = {
        binding.component_id: binding
        for binding in vector.component_bindings
    }
    for row in ordered:
        binding = by_id.get(row.component_id)
        if (
            binding is None
            or row.component_ref != binding.component_ref
            or binding.ordinal_or_null != row.ordinal
        ):
            raise JRoleCertificationError(
                "J component premise identity mismatch"
            )
    return ordered


def _require_positive_authorities(
    context: m1.M1ValidatorContext,
    channel: m1.M1PrerequisiteChannel,
    premises: Sequence[JComponentCertificationPremise],
) -> None:
    states = {
        snapshot.authority_ref: snapshot.typed_state
        for snapshot in context.input_bundle.authority_snapshots
    }
    required = set(channel.authority_refs)
    for premise in premises:
        required.update(premise.authority_refs)
    if any(states.get(ref) != "ALLOW" for ref in required):
        raise JRoleCertificationError(
            "J certification authority snapshot closure not positive exact"
        )


def _role_tokens(
    vector: ComponentAuthorityVectorReceipt,
) -> Mapping[str, str | None]:
    result = {}
    for binding in vector.component_bindings:
        if binding.authority_state == "VALUE":
            token = ROLE_DIGEST_TO_TOKEN.get(
                binding.authoritative_value_digest
            )
            if token is None:
                raise JRoleCertificationError(
                    "UNKNOWN_ROLE_TOKEN_CONTRACT_FAILURE"
                )
            result[binding.component_id] = token
        else:
            result[binding.component_id] = None
    return MappingProxyType(result)


def _contribution(
    role_binding: ComponentAuthorityBinding,
    premise: JComponentCertificationPremise,
) -> str:
    if (
        role_binding.authority_state in _BLOCKED_ROLE_STATES
        or premise.evidence_match_disposition
        in _BLOCKED_MATCH_STATES
        or premise.relation_eligibility_disposition
        in _BLOCKED_ELIGIBILITY_STATES
    ):
        return "blocked_component"
    if (
        role_binding.authority_state != "VALUE"
        or premise.evidence_match_disposition == "UNRESOLVED_MATCH"
        or premise.relation_eligibility_disposition == "UNRESOLVED"
    ):
        return "unresolved_component"
    if premise.special_or_missing_response:
        return "special_or_missing_component"
    if premise.governed_nonrelation_explained:
        return "explained_nonrelation_component"
    if (
        premise.evidence_match_disposition == "ACCEPTED_MATCH"
        and premise.relation_eligibility_disposition
        == "ELIGIBLE_RELATION"
    ):
        return "relation_component"
    if premise.evidence_match_disposition == "ACCEPTED_MATCH":
        return "context_component"
    return "unresolved_component"


def _validation_result(
    context: m1.M1ValidatorContext,
    *,
    outcome: str,
    reason_code: str,
    determinant: Mapping[str, Any],
    explanation: Mapping[str, Any],
) -> m1.FamilyValidationResult:
    binding = context.family_rule_binding
    return m1.FamilyValidationResult(
        claim_family_id=binding.claim_family_id,
        claim_rule_id=binding.claim_rule_id,
        family_rule_binding_ref=binding.ref,
        validator_authority_ref=binding.validator_authority_ref,
        validator_algorithm_identity=(
            binding.validator_algorithm_identity_if_required
        ),
        adjudication_outcome=outcome,
        reason_code=reason_code,
        relation_proposition_identity_ref=None,
        semantic_claim_identity_ref=None,
        semantic_assertion_polarity_or_state="NONE",
        semantic_ceiling=binding.semantic_ceiling,
        determinant_material=determinant,
        explanation_material=explanation,
        effects=dict(m1._FALSE_EFFECTS),
    )


def j_component_certification_validator(
    context: m1.M1ValidatorContext,
) -> m1.FamilyValidationResult:
    """Derive exactly one adopted six-state contribution per governed component."""
    binding = context.family_rule_binding
    _validate_j_binding(binding)
    try:
        channel, vector, detail = _load_role_channel(context)
    except Exception as exc:
        return _validation_result(
            context,
            outcome="INTEGRITY_FAILURE",
            reason_code="J_ROLE_VECTOR_REPLAY_MISMATCH",
            determinant={"integrity_failure": str(exc)},
            explanation={
                "reason_code": "J_ROLE_VECTOR_REPLAY_MISMATCH",
                "detail": str(exc),
            },
        )

    scope = binding.applicability_scope
    expected_role_authority = _role_authority(
        scope["j_family_item_role_authority_ref"]
    )
    expected_role_contract = exact_ref(
        scope["j_role_contract_ref"], "j_role_contract_ref"
    )
    expected_mapping_contract = exact_ref(
        scope["j_mapping_contract_ref"], "j_mapping_contract_ref"
    )
    if (
        vector.vector_rule_authority_ref != expected_role_authority
        or vector.authority_dimension_contract_ref
        != expected_role_contract
        or exact_ref(
            detail["mapping_contract_ref"], "mapping_contract_ref"
        )
        != expected_mapping_contract
    ):
        return _validation_result(
            context,
            outcome="BLOCKED",
            reason_code="J_ROLE_PREREQUISITE_BLOCKED",
            determinant={"role_vector_ref": vector.ref.as_dict()},
            explanation={
                "reason_code": "J_ROLE_PREREQUISITE_BLOCKED"
            },
        )
    if tuple(detail["governed_component_ids"]) != (
        vector.governed_component_ids
    ):
        return _validation_result(
            context,
            outcome="INTEGRITY_FAILURE",
            reason_code="J_COMPONENT_SET_MISMATCH",
            determinant={"role_vector_ref": vector.ref.as_dict()},
            explanation={"reason_code": "J_COMPONENT_SET_MISMATCH"},
        )
    try:
        tokens = _role_tokens(vector)
        premises = _premises(context, vector)
        _require_positive_authorities(context, channel, premises)
    except JRoleCertificationError as exc:
        if str(exc) == "UNKNOWN_ROLE_TOKEN_CONTRACT_FAILURE":
            reason, outcome = (
                "UNKNOWN_ROLE_TOKEN_CONTRACT_FAILURE",
                "INTEGRITY_FAILURE",
            )
        elif "premise" in str(exc) and (
            "mismatch" in str(exc) or "identity" in str(exc)
        ):
            reason, outcome = (
                "J_COMPONENT_SET_MISMATCH",
                "INTEGRITY_FAILURE",
            )
        else:
            reason, outcome = (
                "J_ROLE_PREREQUISITE_BLOCKED",
                "BLOCKED",
            )
        return _validation_result(
            context,
            outcome=outcome,
            reason_code=reason,
            determinant={
                "role_vector_ref": vector.ref.as_dict(),
                "failure": str(exc),
            },
            explanation={"reason_code": reason, "detail": str(exc)},
        )

    by_id = {
        row.component_id: row for row in vector.component_bindings
    }
    ordered_contributions = []
    contribution_tokens = []
    for premise in premises:
        role_binding = by_id[premise.component_id]
        contribution = _contribution(role_binding, premise)
        contribution_tokens.append(contribution)
        ordered_contributions.append({
            "component_ref": premise.component_ref.as_dict(),
            "component_id": premise.component_id,
            "ordinal": premise.ordinal,
            "family_role_token_or_typed_state": (
                tokens[premise.component_id]
                if role_binding.authority_state == "VALUE"
                else role_binding.authority_state
            ),
            "contribution_token": contribution,
            "evidence_match_disposition": (
                premise.evidence_match_disposition
            ),
            "relation_eligibility_disposition": (
                premise.relation_eligibility_disposition
            ),
            "authority_refs": [
                ref.as_dict() for ref in premise.authority_refs
            ],
            "dependency_refs": [
                ref.as_dict() for ref in premise.dependency_refs
            ],
            "negative_or_limit_refs": [
                ref.as_dict()
                for ref in _refs(
                    (
                        *role_binding.negative_or_limit_refs,
                        *premise.negative_or_limit_refs,
                    ),
                    "j_determinant_negative_or_limit_ref",
                )
            ],
        })

    relation_count = contribution_tokens.count("relation_component")
    context_count = sum(
        contribution_tokens.count(token)
        for token in CONTEXT_LIKE_CONTRIBUTIONS
    )
    blocked_count = contribution_tokens.count("blocked_component")
    unresolved_count = contribution_tokens.count("unresolved_component")
    determinant = {
        "ordered_contributions": ordered_contributions,
        "relation_count": relation_count,
        "context_count": context_count,
        "blocked_count": blocked_count,
        "unresolved_count": unresolved_count,
        "role_vector_ref": vector.ref.as_dict(),
        "role_vector_coverage_proof_hash": (
            vector.coverage_proof_hash
        ),
        "contribution_rule_id": CLAIM_RULE_ID,
        "prerequisite_channel_ref": channel.ref.as_dict(),
        "replay_contract_ref": binding.replay_contract_ref.as_dict(),
    }
    if blocked_count:
        reason, outcome = (
            (
                "J_AMBIGUOUS_COMPONENT_MATCH",
                "BLOCKED",
            )
            if any(
                row.evidence_match_disposition == "AMBIGUOUS_MATCH"
                for row in premises
            )
            else ("J_ROLE_PREREQUISITE_BLOCKED", "BLOCKED")
        )
    elif unresolved_count:
        reason, outcome = (
            "J_COMPONENT_CONTRIBUTION_UNRESOLVED",
            "UNRESOLVED",
        )
    elif relation_count < MINIMUM_RELATION_COMPONENTS:
        reason, outcome = (
            "INSUFFICIENT_JOINT_RELATION_COMPONENTS",
            "RULE_NOT_SATISFIED",
        )
    elif context_count:
        reason, outcome = (
            "J_JOINT_RELATION_EVIDENCE_WITH_CONTEXT",
            "RULE_SATISFIED",
        )
    else:
        reason, outcome = (
            "J_JOINT_RELATION_EVIDENCE",
            "RULE_SATISFIED",
        )
    return _validation_result(
        context,
        outcome=outcome,
        reason_code=reason,
        determinant=determinant,
        explanation={
            "reason_code": reason,
            "relation_count": relation_count,
            "context_count": context_count,
            "blocked_count": blocked_count,
            "unresolved_count": unresolved_count,
            "ordered_contribution_tokens": contribution_tokens,
        },
    )


__all__ = [
    "ROLE_SUCCESSION_CONTRACT_ID",
    "ROLE_AUTHORITY_ID",
    "ROLE_AUTHORITY_VERSION",
    "ROLE_AUTHORITY_DIMENSION",
    "ROLE_BINDING_METADATA",
    "ROLE_VOCABULARY",
    "ROLE_CHANNEL_ID",
    "ROLE_CHANNEL_KIND",
    "ROLE_CHANNEL_RELATION_KINDS",
    "CLAIM_FAMILY_ID",
    "CLAIM_RULE_ID",
    "VALIDATOR_ALGORITHM_ID",
    "CONTRIBUTION_VOCABULARY",
    "CONTEXT_LIKE_CONTRIBUTIONS",
    "MINIMUM_RELATION_COMPONENTS",
    "J_COMPONENT_PREMISES_SCOPE_KEY",
    "J_M1_SEMANTIC_CEILING",
    "JRoleCertificationError",
    "JFamilyRoleAssignment",
    "JComponentCertificationPremise",
    "build_j_family_item_role_vector",
    "build_j_family_item_role_channel",
    "build_j_component_premise_scope",
    "j_validator_parameters_ref",
    "build_j_family_rule_binding",
    "build_j_validator_registry",
    "j_component_certification_validator",
]
