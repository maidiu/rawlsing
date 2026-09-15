"""Adopted GT12 relation-specific PRE-V3 -> M4 permission descent.

This module is intentionally a clean-sideline executable binding for the
content-addressed authority adopted by Vozhd at 00374882168f8ca64606fef3ca84e246f1c573e9.
It does not discover authority from prose, infer a weaker/stronger M4 atom, or
generalize beyond the frozen GT2 relation-specific V554 seam.
"""
from __future__ import annotations

from types import MappingProxyType
from typing import Any, Mapping

from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.wave1_ff_prev3_relation_admission import (
    AdmissionDecision,
    GT2_CONDITIONER,
    GT2_CONDITIONER_IMPL,
    GT2_DOWNSTREAM_CONTRACT,
    GT2_Q86_SOURCE_STRUCTURE,
    GT2_RELATION_FAMILY,
    GT2_RELATION_OWNER,
    GT2_RISK_SET_ID,
    GT2_RISK_SET_MEMBER_SET_SHA256,
    GT2_SOURCE_PATH,
    GT2_SOURCE_SHA256,
    GT2_TARGET,
    GT2_TARGET_IMPL,
    GT2_TARGET_USE,
    Prev3FieldForgeRelationAdmission,
    make_gt2_relation_admission_rule,
)
from rawlsing_next.m4_v557_v558_publication_repository import (
    AuthorityRef as M4AuthorityRef,
    V557DecisionState,
)
from rawlsing_next.m1_temporal_v554_admission_dedup import semantic_hash


BINDING_SCHEMA = "GT12_ADOPTED_PREV3_TO_M4_PERMISSION_BINDING@1.0.0"
AUTHORITY_ID = "GT12_RELATION_SPECIFIC_PREV3_TO_M4_PRODUCER_PERMISSION_TRANSLATION_AUTHORITY"
AUTHORITY_VERSION = "1.0.0"
AUTHORITY_CONTENT_HASH = "d052e299206b837292225853fca7ffcf8a3c02b6479c53065ad3aca135be489c"
ADOPTION_RECEIPT_ID = "GT12_PERMISSION_TRANSLATION_AUTHORITY_ADOPTION"
ADOPTION_RECEIPT_VERSION = "1.0.0"
ADOPTION_RECEIPT_CONTENT_HASH = "fe527dd7d6f5163edd5867adf9da2b03ea581c7d78758fe07bf6857c3fd4c46f"
ADOPTION_COMMIT = "00374882168f8ca64606fef3ca84e246f1c573e9"
ADOPTED_PRODUCER_ALLOWED_USES = ("CONTEXT",)
ADOPTED_V557_DECISION_STATE = V557DecisionState.ALLOW_CONTEXT_ONLY
ADOPTED_V557_ALLOWED_USES = ("CONTEXT",)
ADOPTED_V558_REQUESTED_USES = ("CONTEXT",)
AUTHORIZED_EFFECT = (
    "ACTOR_INDEPENDENT_STRUCTURAL_CONTEXT_AVAILABILITY_AND_EXACT_V558_RESOLUTION_ONLY"
)

ADOPTED_AUTHORITY_REF = M4AuthorityRef(
    AUTHORITY_ID, AUTHORITY_VERSION, AUTHORITY_CONTENT_HASH
)
ADOPTED_ADOPTION_RECEIPT_REF = M4AuthorityRef(
    ADOPTION_RECEIPT_ID, ADOPTION_RECEIPT_VERSION, ADOPTION_RECEIPT_CONTENT_HASH
)


class GT12PermissionTranslationError(ValueError):
    """The adopted relation-specific permission descent failed closed."""


def _require_exact_authority_ref(
    actual: M4AuthorityRef, expected: M4AuthorityRef, name: str
) -> None:
    if not isinstance(actual, M4AuthorityRef):
        raise GT12PermissionTranslationError(f"{name} must be exact M4 AuthorityRef")
    if actual != expected:
        raise GT12PermissionTranslationError(f"{name} identity/version/hash mismatch")


def _participant_material(admission: Prev3FieldForgeRelationAdmission) -> tuple[Mapping[str, Any], ...]:
    participants = tuple(item.material() for item in admission.participants)
    if len(participants) != 2:
        raise GT12PermissionTranslationError("GT2 permission authority requires exactly two participants")
    expected = (
        ("CONDITIONER", 0, GT2_CONDITIONER, GT2_CONDITIONER_IMPL, GT2_Q86_SOURCE_STRUCTURE),
        ("TARGET", 1, GT2_TARGET, GT2_TARGET_IMPL, GT2_Q86_SOURCE_STRUCTURE),
    )
    actual = tuple(
        (
            item["role"],
            item["ordinal"],
            item["native_variable"],
            item["question_impl_id"],
            item["source_structure_id"],
        )
        for item in participants
    )
    if actual != expected:
        raise GT12PermissionTranslationError("GT2 permission authority participant/source order mismatch")
    return participants


def derive_adopted_permission_binding(
    admission: Prev3FieldForgeRelationAdmission,
    *,
    authority_ref: M4AuthorityRef = ADOPTED_AUTHORITY_REF,
    adoption_receipt_ref: M4AuthorityRef = ADOPTED_ADOPTION_RECEIPT_REF,
) -> Mapping[str, Any]:
    """Validate exact frozen GT2 positive lineage and derive CONTEXT only."""
    if not isinstance(admission, Prev3FieldForgeRelationAdmission):
        raise GT12PermissionTranslationError(
            "permission descent requires exact Prev3FieldForgeRelationAdmission"
        )
    _require_exact_authority_ref(authority_ref, ADOPTED_AUTHORITY_REF, "translation authority")
    _require_exact_authority_ref(
        adoption_receipt_ref, ADOPTED_ADOPTION_RECEIPT_REF, "translation adoption receipt"
    )
    if admission.decision is not AdmissionDecision.ADMITTED or not admission.is_positive:
        raise GT12PermissionTranslationError("translation requires exact positive ADMITTED receipt")
    if admission.relation_typed_state != "SUPPORTED":
        raise GT12PermissionTranslationError("translation requires relation typed state SUPPORTED")
    if admission.relation_ref.kind != GT2_RELATION_FAMILY:
        raise GT12PermissionTranslationError("translation relation family mismatch")
    if admission.relation_owner != GT2_RELATION_OWNER:
        raise GT12PermissionTranslationError("translation relation owner mismatch")
    if admission.relation_content_hash_echo != admission.relation_ref.content_hash:
        raise GT12PermissionTranslationError("translation relation exact hash mismatch")
    if admission.relation_rule_content_hash_echo != admission.relation_rule_ref.content_hash:
        raise GT12PermissionTranslationError("translation relation-rule exact hash mismatch")
    if admission.target_use != GT2_TARGET_USE:
        raise GT12PermissionTranslationError("translation target use mismatch")
    if tuple(admission.target_use_permissions) != (GT2_TARGET_USE,):
        raise GT12PermissionTranslationError("translation requires singleton upstream target-use permission")
    if tuple(admission.relation_permission_ceiling) != (GT2_TARGET_USE,):
        raise GT12PermissionTranslationError("translation relation permission ceiling is not exact frozen singleton")
    if admission.downstream_contract != GT2_DOWNSTREAM_CONTRACT:
        raise GT12PermissionTranslationError("translation downstream M1 contract mismatch")
    if admission.applicable_negative_denial_noncomparability_refs:
        raise GT12PermissionTranslationError("translation cannot launder negative/denial/noncomparability refs")

    expected_risk = ExactRef(
        "RISK_SET", GT2_RISK_SET_ID, GT2_RISK_SET_MEMBER_SET_SHA256
    )
    if admission.risk_set_ref != expected_risk:
        raise GT12PermissionTranslationError("translation risk-set identity mismatch")
    expected_source = ExactRef("SOURCE_ARTIFACT", GT2_SOURCE_PATH, GT2_SOURCE_SHA256)
    if expected_source not in admission.dependency_refs:
        raise GT12PermissionTranslationError("translation exact Afrobarometer R5 source dependency missing")

    participants = _participant_material(admission)
    expected_rule = make_gt2_relation_admission_rule(
        allowed_relation_rule_ref=admission.relation_rule_ref,
        condition_participant_ref=admission.participants[0].participant_ref,
        target_participant_ref=admission.participants[1].participant_ref,
    )
    if admission.admission_authority_ref != expected_rule.authority_binding.authority_ref:
        raise GT12PermissionTranslationError("translation PRE-V3 admission authority mismatch")
    if admission.admission_current_selection_ref != expected_rule.authority_binding.current_selection_ref:
        raise GT12PermissionTranslationError("translation PRE-V3 current-selection mismatch")
    if admission.admission_rule_ref != expected_rule.ref:
        raise GT12PermissionTranslationError("translation PRE-V3 admission rule mismatch")

    material = {
        "schema": BINDING_SCHEMA,
        "adoption_commit": ADOPTION_COMMIT,
        "translation_authority_ref": authority_ref.as_dict(),
        "translation_adoption_receipt_ref": adoption_receipt_ref.as_dict(),
        "upstream_admission_ref": admission.ref.as_dict(),
        "upstream_admission_authority_ref": admission.admission_authority_ref.as_dict(),
        "upstream_admission_rule_ref": admission.admission_rule_ref.as_dict(),
        "upstream_admission_current_selection_ref": admission.admission_current_selection_ref.as_dict(),
        "field_forge_relation_ref": admission.relation_ref.as_dict(),
        "field_forge_relation_rule_ref": admission.relation_rule_ref.as_dict(),
        "field_forge_relation_owner": admission.relation_owner,
        "relation_typed_state": admission.relation_typed_state,
        "target_use": admission.target_use,
        "target_use_permissions": list(admission.target_use_permissions),
        "relation_permission_ceiling": list(admission.relation_permission_ceiling),
        "risk_set_ref": admission.risk_set_ref.as_dict(),
        "participants": list(participants),
        "producer_allowed_uses": list(ADOPTED_PRODUCER_ALLOWED_USES),
        "v557_required_decision_state": ADOPTED_V557_DECISION_STATE.value,
        "v557_allowed_uses": list(ADOPTED_V557_ALLOWED_USES),
        "v558_requested_uses": list(ADOPTED_V558_REQUESTED_USES),
        "authorized_effect": AUTHORIZED_EFFECT,
    }
    binding_hash = semantic_hash(material)
    return MappingProxyType({**material, "binding_hash": binding_hash})


def require_exact_downstream_use_shape(
    *,
    v557_decision_state: V557DecisionState | str,
    v557_allowed_uses: Any,
    requested_resolution_uses: Any,
) -> None:
    try:
        state = V557DecisionState(v557_decision_state)
    except (TypeError, ValueError) as exc:
        raise GT12PermissionTranslationError("unknown V557 decision state on adopted GT2 path") from exc
    if state is not ADOPTED_V557_DECISION_STATE:
        raise GT12PermissionTranslationError("adopted GT2 path requires ALLOW_CONTEXT_ONLY")
    if isinstance(v557_allowed_uses, (str, bytes)) or tuple(v557_allowed_uses) != ADOPTED_V557_ALLOWED_USES:
        raise GT12PermissionTranslationError("adopted GT2 path requires exact V557 uses ('CONTEXT',)")
    if isinstance(requested_resolution_uses, (str, bytes)) or tuple(requested_resolution_uses) != ADOPTED_V558_REQUESTED_USES:
        raise GT12PermissionTranslationError("adopted GT2 path requires exact V558 requested uses ('CONTEXT',)")


__all__ = [
    "BINDING_SCHEMA",
    "AUTHORITY_ID",
    "AUTHORITY_VERSION",
    "AUTHORITY_CONTENT_HASH",
    "ADOPTION_RECEIPT_ID",
    "ADOPTION_RECEIPT_VERSION",
    "ADOPTION_RECEIPT_CONTENT_HASH",
    "ADOPTION_COMMIT",
    "ADOPTED_PRODUCER_ALLOWED_USES",
    "ADOPTED_V557_DECISION_STATE",
    "ADOPTED_V557_ALLOWED_USES",
    "ADOPTED_V558_REQUESTED_USES",
    "AUTHORIZED_EFFECT",
    "ADOPTED_AUTHORITY_REF",
    "ADOPTED_ADOPTION_RECEIPT_REF",
    "GT12PermissionTranslationError",
    "derive_adopted_permission_binding",
    "require_exact_downstream_use_shape",
]
