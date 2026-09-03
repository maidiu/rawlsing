"""Frozen GT2 FIELD FORGE relation -> PRE-V3 admission sibling jurisdiction.

This module implements only the frozen GT2 relation-admission boundary for
EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0 and target use
STRUCTURAL_MEDIATION_INPUT. It does not call I04/P06, construct EmpiricalFact
or StructuralEmpiricalAdmission, create an M1 basis, or infer actor state.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    Pre553IntegrityError,
    authority_ref,
    canonicalize,
    exact_ref,
    semantic_hash,
)

RULE_CONTRACT_ID = "FIELD_FORGE_RELATION_ADMISSION_RULE@1.0.0"
RECEIPT_CONTRACT_ID = "PREV3_FIELD_FORGE_RELATION_ADMISSION@1.0.0"
OWNER = "PREV3_FIELD_FORGE_RELATION_ADMISSION_OWNER"
GT2_RELATION_FAMILY = "EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0"
GT2_RELATION_OWNER = "FIELD_FORGE_ACTOR_INDEPENDENT_RELATION_OWNER"
GT2_TARGET_USE = "STRUCTURAL_MEDIATION_INPUT"
GT2_DOWNSTREAM_CONTRACT = "M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0"
GT2_ADMISSION_OPERATION = "ADMIT_EXACT_GT2_FIELD_FORGE_RELATION_FOR_STRUCTURAL_MEDIATION_INPUT"
GT2_SOURCE_FAMILY = "Afrobarometer"
GT2_SOURCE_WAVE = "R5"
GT2_SOURCE_PATH = "Data/Afro Barometer Round 5.sav"
GT2_SOURCE_SHA256 = "c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651"
GT2_RISK_SET_ID = "FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1"
GT2_RISK_SET_ROWS = 19_210
GT2_RISK_SET_MEMBER_SET_SHA256 = "0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b"
GT2_CONDITIONER = "Q86B"
GT2_TARGET = "Q86A"
GT2_CONDITIONER_IMPL = "question_impl.phase0.2fb3a62609dad4c1306d"
GT2_TARGET_IMPL = "question_impl.phase0.67f036c0efb7fb98ff4a"
GT2_Q86_SOURCE_STRUCTURE = "cssu.r1.afrobarometer.r5.d8478014cb0a506fe6c4"
FROZEN_CANARY_COMMIT = "a9416094cbb4653dd2de2e4aa7b67577a355560c"
WAVE_PROGRAM_COMMIT = "17b9abc5c8c3038d14670c6e68136bb868f5073a"
WAVE1_CENTRAL_FANIN_COMMIT = "6a4bf89c5403459d43dcb925c1f98a7b30dd6f49"
ADMISSION_LOCAL_INFORMATION_LOSS = "NONE__REFERENCE_PRESERVING"

POSITIVE_RELATION_STATES = frozenset({"SUPPORTED"})
UPSTREAM_NEGATIVE_TO_DECISION = MappingProxyType({
    "OBSERVED_ZERO": "UNRESOLVED",
    "VALID_EMPTY": "VALID_EMPTY",
    "ZERO_DENOMINATOR_ABSTENTION": "VALID_EMPTY",
    "UNDEFINED_FOR_OBJECT": "OUT_OF_SCOPE",
    "OUT_OF_SCOPE": "OUT_OF_SCOPE",
    "DENIED": "DENIED",
    "UNRESOLVED_AUTHORITY": "MISSING_AUTHORITY",
    "MISSING_AUTHORITY": "MISSING_AUTHORITY",
    "UNRESOLVED": "UNRESOLVED",
    "NONCOMPARABLE": "NONCOMPARABLE",
    "NO_TRANSPORT": "NONCOMPARABLE",
    "BLOCKED_EXPLICIT_AUTHORITY": "BLOCKED_EXPLICIT_AUTHORITY",
    "OBSERVABILITY_LIMIT": "OBSERVABILITY_LIMIT",
    "INTEGRITY_FAILURE": "INTEGRITY_FAILURE",
})


class RelationAdmissionError(Pre553IntegrityError):
    pass


class RelationAdmissionTypeError(RelationAdmissionError):
    pass


class RelationAdmissionReplayError(RelationAdmissionError):
    pass


class AdmissionDecision(str, Enum):
    ADMITTED = "ADMITTED"
    VALID_EMPTY = "VALID_EMPTY"
    MISSING_AUTHORITY = "MISSING_AUTHORITY"
    DENIED = "DENIED"
    DEFERRED = "DEFERRED"
    OUT_OF_SCOPE = "OUT_OF_SCOPE"
    NONCOMPARABLE = "NONCOMPARABLE"
    UNRESOLVED = "UNRESOLVED"
    BLOCKED_EXPLICIT_AUTHORITY = "BLOCKED_EXPLICIT_AUTHORITY"
    OBSERVABILITY_LIMIT = "OBSERVABILITY_LIMIT"
    INTEGRITY_FAILURE = "INTEGRITY_FAILURE"


def _require_sha256(value: Any, name: str) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
        raise RelationAdmissionError(f"{name} must be lowercase sha256")
    return value


def _require_git_sha(value: Any, name: str) -> str:
    if not isinstance(value, str) or len(value) != 40 or any(c not in "0123456789abcdef" for c in value):
        raise RelationAdmissionError(f"{name} must be lowercase git sha")
    return value


def _tokens(values: Sequence[str], name: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise RelationAdmissionError(f"{name} must be a sequence")
    out: list[str] = []
    for value in values:
        if not isinstance(value, str) or not value.strip():
            raise RelationAdmissionError(f"{name} contains empty token")
        value = value.strip()
        if value.upper() in {"LATEST", "DEFAULT", "FUZZY", "NEAREST", "*"}:
            raise RelationAdmissionError(f"{name} may not use mutable/fuzzy selectors")
        out.append(value)
    return tuple(sorted(set(out)))


def _refs(values: Sequence[ExactRef | Mapping[str, Any]], name: str) -> tuple[ExactRef, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise RelationAdmissionError(f"{name} must be a sequence")
    return tuple(sorted({exact_ref(value, name) for value in values}, key=lambda ref: ref.key))


def _auths(values: Sequence[AuthorityRef | Mapping[str, Any]], name: str) -> tuple[AuthorityRef, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise RelationAdmissionError(f"{name} must be a sequence")
    return tuple(sorted({authority_ref(value, name) for value in values}, key=lambda ref: ref.key))


def _derived_ref(kind: str, object_id: str, material: Mapping[str, Any]) -> ExactRef:
    return ExactRef(kind, object_id, semantic_hash(material))


@dataclass(frozen=True)
class ParticipantBinding:
    role: str
    ordinal: int
    native_variable: str
    question_impl_id: str
    source_structure_id: str
    participant_ref: ExactRef
    multiplicity: int = 1

    def __post_init__(self) -> None:
        if self.role not in {"CONDITIONER", "TARGET"}:
            raise RelationAdmissionError("participant role must be CONDITIONER or TARGET")
        if not isinstance(self.ordinal, int) or isinstance(self.ordinal, bool) or self.ordinal < 0:
            raise RelationAdmissionError("participant ordinal must be a nonnegative integer")
        if not isinstance(self.multiplicity, int) or isinstance(self.multiplicity, bool) or self.multiplicity <= 0:
            raise RelationAdmissionError("participant multiplicity must be a positive integer")
        for name in ("native_variable", "question_impl_id", "source_structure_id"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise RelationAdmissionError(f"{name} must be non-empty")
        object.__setattr__(self, "participant_ref", exact_ref(self.participant_ref, "participant_ref"))

    def material(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "ordinal": self.ordinal,
            "native_variable": self.native_variable,
            "question_impl_id": self.question_impl_id,
            "source_structure_id": self.source_structure_id,
            "participant_ref": self.participant_ref.as_dict(),
            "multiplicity": self.multiplicity,
        }


@dataclass(frozen=True)
class FieldForgeRelationEvidence:
    relation_ref: ExactRef
    relation_content_hash_echo: str
    relation_family: str
    relation_owner: str
    relation_rule_ref: ExactRef
    relation_rule_content_hash_echo: str
    relation_typed_state: str
    source_artifact_ref: ExactRef
    source_family: str
    source_wave: str
    risk_set_ref: ExactRef
    risk_set_row_count: int
    participants: tuple[ParticipantBinding, ...]
    relation_permission_ceiling: tuple[str, ...]
    relation_authority_refs: tuple[AuthorityRef, ...]
    relation_current_selection_refs: tuple[ExactRef, ...]
    relation_semantic_identity_refs: tuple[ExactRef, ...]
    native_scope_identity_refs: tuple[ExactRef, ...]
    source_universe_refs: tuple[ExactRef, ...]
    relation_dependency_refs: tuple[ExactRef, ...]
    relation_negative_or_limit_refs: tuple[ExactRef, ...]
    relation_information_loss_declaration: str
    relation_replay_root: ExactRef

    def __post_init__(self) -> None:
        object.__setattr__(self, "relation_ref", exact_ref(self.relation_ref, "relation_ref"))
        _require_sha256(self.relation_content_hash_echo, "relation_content_hash_echo")
        if self.relation_content_hash_echo != self.relation_ref.content_hash:
            raise RelationAdmissionError("relation content-hash echo mismatch")
        object.__setattr__(self, "relation_rule_ref", exact_ref(self.relation_rule_ref, "relation_rule_ref"))
        _require_sha256(self.relation_rule_content_hash_echo, "relation_rule_content_hash_echo")
        if self.relation_rule_content_hash_echo != self.relation_rule_ref.content_hash:
            raise RelationAdmissionError("relation rule content-hash echo mismatch")
        for name in ("relation_family", "relation_owner", "relation_typed_state", "source_family", "source_wave", "relation_information_loss_declaration"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise RelationAdmissionError(f"{name} must be non-empty")
        object.__setattr__(self, "source_artifact_ref", exact_ref(self.source_artifact_ref, "source_artifact_ref"))
        object.__setattr__(self, "risk_set_ref", exact_ref(self.risk_set_ref, "risk_set_ref"))
        object.__setattr__(self, "relation_replay_root", exact_ref(self.relation_replay_root, "relation_replay_root"))
        if not isinstance(self.risk_set_row_count, int) or isinstance(self.risk_set_row_count, bool) or self.risk_set_row_count < 0:
            raise RelationAdmissionError("risk_set_row_count must be a nonnegative integer")
        participants = tuple(sorted(self.participants, key=lambda participant: participant.ordinal))
        if not participants or any(not isinstance(item, ParticipantBinding) for item in participants):
            raise RelationAdmissionError("participants must be ParticipantBinding objects")
        if len({item.ordinal for item in participants}) != len(participants):
            raise RelationAdmissionError("participants require unique ordinals")
        object.__setattr__(self, "participants", participants)
        object.__setattr__(self, "relation_permission_ceiling", _tokens(self.relation_permission_ceiling, "relation_permission_ceiling"))
        for name in (
            "relation_current_selection_refs", "relation_semantic_identity_refs",
            "native_scope_identity_refs", "source_universe_refs",
            "relation_dependency_refs", "relation_negative_or_limit_refs",
        ):
            object.__setattr__(self, name, _refs(getattr(self, name), name))
        object.__setattr__(self, "relation_authority_refs", _auths(self.relation_authority_refs, "relation_authority_refs"))


@dataclass(frozen=True)
class RelationAdmissionAuthorityBinding:
    authority_ref: AuthorityRef
    decision_state: str
    current_selection_ref: ExactRef
    operation: str
    relation_family: str
    target_use: str
    downstream_contract: str
    frozen_contract_commit: str
    central_fanin_commit: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "authority_ref", authority_ref(self.authority_ref))
        object.__setattr__(self, "current_selection_ref", exact_ref(self.current_selection_ref))
        if self.decision_state not in {"ALLOW", "DENY", "DEFER", "MISSING_AUTHORITY", "UNKNOWN", "OUT_OF_SCOPE"}:
            raise RelationAdmissionError("invalid relation-admission authority state")
        _require_git_sha(self.frozen_contract_commit, "frozen_contract_commit")
        _require_git_sha(self.central_fanin_commit, "central_fanin_commit")

    def material(self) -> Mapping[str, Any]:
        return canonicalize({
            "authority_ref": self.authority_ref,
            "decision_state": self.decision_state,
            "current_selection_ref": self.current_selection_ref,
            "operation": self.operation,
            "relation_family": self.relation_family,
            "target_use": self.target_use,
            "downstream_contract": self.downstream_contract,
            "frozen_contract_commit": self.frozen_contract_commit,
            "central_fanin_commit": self.central_fanin_commit,
        })


@dataclass(frozen=True)
class FieldForgeRelationAdmissionRule:
    authority_binding: RelationAdmissionAuthorityBinding
    allowed_relation_rule_ref: ExactRef
    allowed_relation_states: tuple[str, ...]
    output_permission_subset: tuple[str, ...]
    required_source_artifact_ref: ExactRef
    required_risk_set_ref: ExactRef
    required_risk_set_row_count: int
    required_participants: tuple[ParticipantBinding, ...]
    required_information_loss_declaration: str = ADMISSION_LOCAL_INFORMATION_LOSS

    def __post_init__(self) -> None:
        if not isinstance(self.authority_binding, RelationAdmissionAuthorityBinding):
            raise RelationAdmissionTypeError("authority_binding must be RelationAdmissionAuthorityBinding")
        object.__setattr__(self, "allowed_relation_rule_ref", exact_ref(self.allowed_relation_rule_ref))
        object.__setattr__(self, "required_source_artifact_ref", exact_ref(self.required_source_artifact_ref))
        object.__setattr__(self, "required_risk_set_ref", exact_ref(self.required_risk_set_ref))
        object.__setattr__(self, "allowed_relation_states", _tokens(self.allowed_relation_states, "allowed_relation_states"))
        if not set(self.allowed_relation_states).issubset(POSITIVE_RELATION_STATES):
            raise RelationAdmissionError("GT2 rule may allow only genuinely positive FIELD FORGE relation states")
        object.__setattr__(self, "output_permission_subset", _tokens(self.output_permission_subset, "output_permission_subset"))
        if self.output_permission_subset != (GT2_TARGET_USE,):
            raise RelationAdmissionError("GT2 rule may grant only STRUCTURAL_MEDIATION_INPUT")
        binding = self.authority_binding
        expected = (GT2_ADMISSION_OPERATION, GT2_RELATION_FAMILY, GT2_TARGET_USE, GT2_DOWNSTREAM_CONTRACT)
        if (binding.operation, binding.relation_family, binding.target_use, binding.downstream_contract) != expected:
            raise RelationAdmissionError("authority binding is outside frozen GT2 jurisdiction")

    def material(self) -> Mapping[str, Any]:
        return canonicalize({
            "contract": RULE_CONTRACT_ID,
            "owner": OWNER,
            "authority_binding": self.authority_binding.material(),
            "allowed_relation_rule_ref": self.allowed_relation_rule_ref,
            "allowed_relation_states": self.allowed_relation_states,
            "output_permission_subset": self.output_permission_subset,
            "required_source_artifact_ref": self.required_source_artifact_ref,
            "required_risk_set_ref": self.required_risk_set_ref,
            "required_risk_set_row_count": self.required_risk_set_row_count,
            "required_participants": [participant.material() for participant in self.required_participants],
            "required_information_loss_declaration": self.required_information_loss_declaration,
        })

    @property
    def ref(self) -> ExactRef:
        return _derived_ref("FIELD_FORGE_RELATION_ADMISSION_RULE", RULE_CONTRACT_ID, self.material())


@dataclass(frozen=True)
class RelationAdmissionRequest:
    relation: FieldForgeRelationEvidence
    target_use: str = GT2_TARGET_USE
    downstream_contract: str = GT2_DOWNSTREAM_CONTRACT

    def __post_init__(self) -> None:
        if not isinstance(self.relation, FieldForgeRelationEvidence):
            raise RelationAdmissionTypeError("relation must be FieldForgeRelationEvidence")


@dataclass(frozen=True)
class Prev3FieldForgeRelationAdmission:
    decision: AdmissionDecision
    reason_code: str
    relation_ref: ExactRef
    relation_content_hash_echo: str
    relation_owner: str
    relation_rule_ref: ExactRef
    relation_rule_content_hash_echo: str
    relation_typed_state: str
    admission_rule_ref: ExactRef
    admission_authority_ref: AuthorityRef
    admission_current_selection_ref: ExactRef
    target_use: str
    downstream_contract: str
    target_use_permissions: tuple[str, ...]
    relation_permission_ceiling: tuple[str, ...]
    relation_semantic_identity_refs: tuple[ExactRef, ...]
    native_scope_identity_refs: tuple[ExactRef, ...]
    source_universe_refs: tuple[ExactRef, ...]
    risk_set_ref: ExactRef
    participants: tuple[ParticipantBinding, ...]
    applicable_negative_denial_noncomparability_refs: tuple[ExactRef, ...]
    relation_authority_refs: tuple[AuthorityRef, ...]
    dependency_refs: tuple[ExactRef, ...]
    relation_information_loss_declaration: str
    admission_information_loss_declaration: str
    producer_replay_locator_or_reference_root: ExactRef
    historical_authority_material_hash: str

    @property
    def is_positive(self) -> bool:
        return self.decision is AdmissionDecision.ADMITTED

    def material(self) -> Mapping[str, Any]:
        return canonicalize({
            "contract": RECEIPT_CONTRACT_ID,
            "owner": OWNER,
            "decision": self.decision.value,
            "reason_code": self.reason_code,
            "relation_ref": self.relation_ref,
            "relation_content_hash_echo": self.relation_content_hash_echo,
            "relation_owner": self.relation_owner,
            "relation_rule_ref": self.relation_rule_ref,
            "relation_rule_content_hash_echo": self.relation_rule_content_hash_echo,
            "relation_typed_state": self.relation_typed_state,
            "admission_rule_ref": self.admission_rule_ref,
            "admission_authority_ref": self.admission_authority_ref,
            "admission_current_selection_ref": self.admission_current_selection_ref,
            "target_use": self.target_use,
            "downstream_contract": self.downstream_contract,
            "target_use_permissions": self.target_use_permissions,
            "relation_permission_ceiling": self.relation_permission_ceiling,
            "relation_semantic_identity_refs": self.relation_semantic_identity_refs,
            "native_scope_identity_refs": self.native_scope_identity_refs,
            "source_universe_refs": self.source_universe_refs,
            "risk_set_ref": self.risk_set_ref,
            "participants": [participant.material() for participant in self.participants],
            "applicable_negative_denial_noncomparability_refs": self.applicable_negative_denial_noncomparability_refs,
            "relation_authority_refs": self.relation_authority_refs,
            "dependency_refs": self.dependency_refs,
            "relation_information_loss_declaration": self.relation_information_loss_declaration,
            "admission_information_loss_declaration": self.admission_information_loss_declaration,
            "producer_replay_locator_or_reference_root": self.producer_replay_locator_or_reference_root,
            "historical_authority_material_hash": self.historical_authority_material_hash,
            "semantic_ceiling": {
                "empirical_fact_created": False,
                "structural_empirical_admission_created": False,
                "m1_basis_created": False,
                "actor_inference_allowed": False,
            },
        })

    @property
    def ref(self) -> ExactRef:
        return _derived_ref("PREV3_FIELD_FORGE_RELATION_ADMISSION", RECEIPT_CONTRACT_ID, self.material())


def frozen_gt2_admission_authority_binding() -> RelationAdmissionAuthorityBinding:
    material = {
        "owner": OWNER,
        "operation": GT2_ADMISSION_OPERATION,
        "relation_family": GT2_RELATION_FAMILY,
        "target_use": GT2_TARGET_USE,
        "downstream_contract": GT2_DOWNSTREAM_CONTRACT,
        "frozen_contract_commit": FROZEN_CANARY_COMMIT,
        "central_fanin_commit": WAVE1_CENTRAL_FANIN_COMMIT,
        "wave_program_commit": WAVE_PROGRAM_COMMIT,
    }
    authority = AuthorityRef("GT2_FF_PREV3_RELATION_ADMISSION_AUTHORITY", "R1", semantic_hash(material))
    selection = _derived_ref(
        "RELATION_ADMISSION_CURRENT_SELECTION",
        "urn:rawlsing:prev3:gt2-relation-admission-current-selection",
        {
            "authority_ref": authority.as_dict(),
            "frozen_contract_commit": FROZEN_CANARY_COMMIT,
            "central_fanin_commit": WAVE1_CENTRAL_FANIN_COMMIT,
            "state": "CURRENT_FOR_FROZEN_GT2_CANARY_ONLY",
        },
    )
    return RelationAdmissionAuthorityBinding(
        authority,
        "ALLOW",
        selection,
        GT2_ADMISSION_OPERATION,
        GT2_RELATION_FAMILY,
        GT2_TARGET_USE,
        GT2_DOWNSTREAM_CONTRACT,
        FROZEN_CANARY_COMMIT,
        WAVE1_CENTRAL_FANIN_COMMIT,
    )


def make_gt2_relation_admission_rule(
    *,
    allowed_relation_rule_ref: ExactRef | Mapping[str, Any],
    condition_participant_ref: ExactRef | Mapping[str, Any],
    target_participant_ref: ExactRef | Mapping[str, Any],
) -> FieldForgeRelationAdmissionRule:
    participants = (
        ParticipantBinding(
            "CONDITIONER", 0, GT2_CONDITIONER, GT2_CONDITIONER_IMPL,
            GT2_Q86_SOURCE_STRUCTURE, exact_ref(condition_participant_ref),
        ),
        ParticipantBinding(
            "TARGET", 1, GT2_TARGET, GT2_TARGET_IMPL,
            GT2_Q86_SOURCE_STRUCTURE, exact_ref(target_participant_ref),
        ),
    )
    return FieldForgeRelationAdmissionRule(
        frozen_gt2_admission_authority_binding(),
        exact_ref(allowed_relation_rule_ref),
        tuple(sorted(POSITIVE_RELATION_STATES)),
        (GT2_TARGET_USE,),
        ExactRef("SOURCE_ARTIFACT", GT2_SOURCE_PATH, GT2_SOURCE_SHA256),
        ExactRef("RISK_SET", GT2_RISK_SET_ID, GT2_RISK_SET_MEMBER_SET_SHA256),
        GT2_RISK_SET_ROWS,
        participants,
    )


def _authority_decision(rule: FieldForgeRelationAdmissionRule) -> tuple[AdmissionDecision | None, str | None]:
    return {
        "ALLOW": (None, None),
        "DENY": (AdmissionDecision.DENIED, "ADMISSION_AUTHORITY_DENIED"),
        "DEFER": (AdmissionDecision.DEFERRED, "ADMISSION_AUTHORITY_DEFERRED"),
        "MISSING_AUTHORITY": (AdmissionDecision.MISSING_AUTHORITY, "ADMISSION_AUTHORITY_UNAVAILABLE"),
        "UNKNOWN": (AdmissionDecision.MISSING_AUTHORITY, "ADMISSION_AUTHORITY_UNAVAILABLE"),
        "OUT_OF_SCOPE": (AdmissionDecision.OUT_OF_SCOPE, "ADMISSION_AUTHORITY_OUT_OF_SCOPE"),
    }.get(rule.authority_binding.decision_state, (AdmissionDecision.INTEGRITY_FAILURE, "ADMISSION_AUTHORITY_STATE_INVALID"))


def _upstream_decision(state: str, allowed: Sequence[str]) -> tuple[AdmissionDecision | None, str | None]:
    if state in allowed:
        return None, None
    mapped = UPSTREAM_NEGATIVE_TO_DECISION.get(state)
    if mapped:
        return AdmissionDecision(mapped), f"UPSTREAM_RELATION_{state}"
    return AdmissionDecision.UNRESOLVED, "UPSTREAM_RELATION_STATE_NOT_AUTHORIZED_FOR_GT2"


def _same_participants(left: Sequence[ParticipantBinding], right: Sequence[ParticipantBinding]) -> bool:
    return [canonicalize(item.material()) for item in left] == [canonicalize(item.material()) for item in right]


def _integrity_decision(
    relation: FieldForgeRelationEvidence,
    rule: FieldForgeRelationAdmissionRule,
) -> tuple[AdmissionDecision | None, str | None]:
    checks = (
        (relation.relation_family == GT2_RELATION_FAMILY, AdmissionDecision.OUT_OF_SCOPE, "RELATION_FAMILY_NOT_FROZEN_GT2"),
        (relation.relation_owner == GT2_RELATION_OWNER, AdmissionDecision.INTEGRITY_FAILURE, "RELATION_OWNER_MISMATCH"),
        (relation.relation_rule_ref == rule.allowed_relation_rule_ref, AdmissionDecision.INTEGRITY_FAILURE, "RELATION_RULE_REF_MISMATCH"),
        (relation.source_family == GT2_SOURCE_FAMILY and relation.source_wave == GT2_SOURCE_WAVE, AdmissionDecision.OUT_OF_SCOPE, "SOURCE_FAMILY_OR_WAVE_MISMATCH"),
        (relation.source_artifact_ref == rule.required_source_artifact_ref, AdmissionDecision.INTEGRITY_FAILURE, "SOURCE_ARTIFACT_IDENTITY_MISMATCH"),
        (relation.risk_set_ref == rule.required_risk_set_ref, AdmissionDecision.INTEGRITY_FAILURE, "RISK_SET_IDENTITY_MISMATCH"),
        (relation.risk_set_row_count == rule.required_risk_set_row_count, AdmissionDecision.INTEGRITY_FAILURE, "RISK_SET_ROW_COUNT_MISMATCH"),
        (_same_participants(relation.participants, rule.required_participants), AdmissionDecision.INTEGRITY_FAILURE, "PARTICIPANT_ROLE_ORDER_IDENTITY_MISMATCH"),
        (relation.relation_information_loss_declaration == rule.required_information_loss_declaration, AdmissionDecision.INTEGRITY_FAILURE, "RELATION_INFORMATION_LOSS_MISMATCH"),
        (bool(relation.relation_semantic_identity_refs and relation.native_scope_identity_refs and relation.source_universe_refs), AdmissionDecision.INTEGRITY_FAILURE, "RELATION_SEMANTIC_SCOPE_UNIVERSE_CLOSURE_MISSING"),
        (bool(relation.relation_authority_refs and relation.relation_current_selection_refs), AdmissionDecision.MISSING_AUTHORITY, "UPSTREAM_RELATION_AUTHORITY_OR_CURRENT_SELECTION_MISSING"),
        (bool(relation.relation_dependency_refs), AdmissionDecision.INTEGRITY_FAILURE, "RELATION_DEPENDENCY_CLOSURE_MISSING"),
    )
    for ok, decision, reason in checks:
        if not ok:
            return decision, reason
    return None, None


def _historical_authority_hash(
    relation: FieldForgeRelationEvidence,
    rule: FieldForgeRelationAdmissionRule,
) -> str:
    return semantic_hash({
        "admission_authority_binding": rule.authority_binding.material(),
        "admission_rule_ref": rule.ref.as_dict(),
        "relation_authority_refs": [ref.as_dict() for ref in relation.relation_authority_refs],
        "relation_current_selection_refs": [ref.as_dict() for ref in relation.relation_current_selection_refs],
    })


def _receipt(
    relation: FieldForgeRelationEvidence,
    rule: FieldForgeRelationAdmissionRule,
    decision: AdmissionDecision,
    reason: str,
) -> Prev3FieldForgeRelationAdmission:
    permissions = rule.output_permission_subset if decision is AdmissionDecision.ADMITTED else ()
    dependencies = tuple(sorted(
        set(relation.relation_dependency_refs + (relation.relation_ref, relation.relation_rule_ref, rule.ref)),
        key=lambda ref: ref.key,
    ))
    return Prev3FieldForgeRelationAdmission(
        decision=decision,
        reason_code=reason,
        relation_ref=relation.relation_ref,
        relation_content_hash_echo=relation.relation_content_hash_echo,
        relation_owner=relation.relation_owner,
        relation_rule_ref=relation.relation_rule_ref,
        relation_rule_content_hash_echo=relation.relation_rule_content_hash_echo,
        relation_typed_state=relation.relation_typed_state,
        admission_rule_ref=rule.ref,
        admission_authority_ref=rule.authority_binding.authority_ref,
        admission_current_selection_ref=rule.authority_binding.current_selection_ref,
        target_use=GT2_TARGET_USE,
        downstream_contract=GT2_DOWNSTREAM_CONTRACT,
        target_use_permissions=permissions,
        relation_permission_ceiling=relation.relation_permission_ceiling,
        relation_semantic_identity_refs=relation.relation_semantic_identity_refs,
        native_scope_identity_refs=relation.native_scope_identity_refs,
        source_universe_refs=relation.source_universe_refs,
        risk_set_ref=relation.risk_set_ref,
        participants=relation.participants,
        applicable_negative_denial_noncomparability_refs=relation.relation_negative_or_limit_refs,
        relation_authority_refs=relation.relation_authority_refs,
        dependency_refs=dependencies,
        relation_information_loss_declaration=relation.relation_information_loss_declaration,
        admission_information_loss_declaration=ADMISSION_LOCAL_INFORMATION_LOSS,
        producer_replay_locator_or_reference_root=relation.relation_replay_root,
        historical_authority_material_hash=_historical_authority_hash(relation, rule),
    )


def evaluate_gt2_relation_admission(
    request: RelationAdmissionRequest,
    rule: FieldForgeRelationAdmissionRule,
) -> Prev3FieldForgeRelationAdmission:
    if not isinstance(request, RelationAdmissionRequest):
        raise RelationAdmissionTypeError("request must be RelationAdmissionRequest")
    if not isinstance(rule, FieldForgeRelationAdmissionRule):
        raise RelationAdmissionTypeError("rule must be FieldForgeRelationAdmissionRule")
    relation = request.relation
    if request.target_use != GT2_TARGET_USE:
        return _receipt(relation, rule, AdmissionDecision.OUT_OF_SCOPE, "TARGET_USE_MISMATCH")
    if request.downstream_contract != GT2_DOWNSTREAM_CONTRACT:
        return _receipt(relation, rule, AdmissionDecision.OUT_OF_SCOPE, "DOWNSTREAM_CONTRACT_MISMATCH")
    decision, reason = _authority_decision(rule)
    if decision:
        return _receipt(relation, rule, decision, reason or "ADMISSION_AUTHORITY_BLOCKED")
    decision, reason = _integrity_decision(relation, rule)
    if decision:
        return _receipt(relation, rule, decision, reason or "RELATION_INTEGRITY_BLOCKED")
    decision, reason = _upstream_decision(relation.relation_typed_state, rule.allowed_relation_states)
    if decision:
        return _receipt(relation, rule, decision, reason or "UPSTREAM_RELATION_BLOCKED")
    if GT2_TARGET_USE not in relation.relation_permission_ceiling:
        return _receipt(relation, rule, AdmissionDecision.DENIED, "TARGET_USE_NOT_PERMITTED_BY_RELATION")
    if not set(rule.output_permission_subset).issubset(set(relation.relation_permission_ceiling)):
        return _receipt(relation, rule, AdmissionDecision.INTEGRITY_FAILURE, "ADMISSION_PERMISSION_WIDENING")
    if relation.relation_negative_or_limit_refs:
        return _receipt(relation, rule, AdmissionDecision.UNRESOLVED, "APPLICABLE_UPSTREAM_NEGATIVE_OR_LIMIT_REFS_PRESENT")
    return _receipt(
        relation,
        rule,
        AdmissionDecision.ADMITTED,
        "EXACT_GT2_RELATION_ADMITTED_FOR_STRUCTURAL_MEDIATION_INPUT",
    )


def replay_gt2_relation_admission(
    *,
    relation: FieldForgeRelationEvidence,
    rule: FieldForgeRelationAdmissionRule,
    historical_receipt: Prev3FieldForgeRelationAdmission,
) -> Prev3FieldForgeRelationAdmission:
    if not isinstance(historical_receipt, Prev3FieldForgeRelationAdmission):
        raise RelationAdmissionReplayError("historical receipt type mismatch")
    if historical_receipt.relation_ref != relation.relation_ref:
        raise RelationAdmissionReplayError("historical relation ref mismatch")
    if historical_receipt.admission_rule_ref != rule.ref:
        raise RelationAdmissionReplayError("historical admission rule ref mismatch")
    if historical_receipt.historical_authority_material_hash != _historical_authority_hash(relation, rule):
        raise RelationAdmissionReplayError("historical authority material mismatch")
    replayed = evaluate_gt2_relation_admission(RelationAdmissionRequest(relation), rule)
    if replayed.ref != historical_receipt.ref:
        raise RelationAdmissionReplayError("deterministic historical replay mismatch")
    return replayed


__all__ = [
    "RULE_CONTRACT_ID", "RECEIPT_CONTRACT_ID", "OWNER", "GT2_RELATION_FAMILY",
    "GT2_RELATION_OWNER", "GT2_TARGET_USE", "GT2_DOWNSTREAM_CONTRACT",
    "GT2_ADMISSION_OPERATION", "GT2_SOURCE_FAMILY", "GT2_SOURCE_WAVE",
    "GT2_SOURCE_PATH", "GT2_SOURCE_SHA256", "GT2_RISK_SET_ID", "GT2_RISK_SET_ROWS",
    "GT2_RISK_SET_MEMBER_SET_SHA256", "GT2_CONDITIONER", "GT2_TARGET",
    "FROZEN_CANARY_COMMIT", "WAVE1_CENTRAL_FANIN_COMMIT",
    "ADMISSION_LOCAL_INFORMATION_LOSS", "AdmissionDecision", "ParticipantBinding",
    "FieldForgeRelationEvidence", "RelationAdmissionAuthorityBinding",
    "FieldForgeRelationAdmissionRule", "RelationAdmissionRequest",
    "Prev3FieldForgeRelationAdmission", "RelationAdmissionError",
    "RelationAdmissionTypeError", "RelationAdmissionReplayError",
    "frozen_gt2_admission_authority_binding", "make_gt2_relation_admission_rule",
    "evaluate_gt2_relation_admission", "replay_gt2_relation_admission",
]
