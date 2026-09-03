#!/usr/bin/env python3
"""Bounded relation-specific M1/V554 ingress for admitted FIELD FORGE relations.

This module is a sibling of the frozen empirical M1 ingress.  It does not
reinterpret DIRECT_STRUCTURAL_EMPIRICAL_ADMISSION or V553_TEMPORAL_OBJECT,
does not call V553, and does not create relation-admission authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef as Pre553AuthorityRef,
    ExactRef as Pre553ExactRef,
)

from rawlsing_next.m1_temporal_v554_admission_dedup import (
    CONDITION_DISPOSITION,
    M1DecisionState,
    M1Evaluation,
    SCR554_CONTRACT_ID,
    TARGET_USE,
    _b1,
    _block_for_conditions,
    _condition,
    _exact_ref,
    _f2,
    _handoff,
    _nonempty,
    _publication,
    _rule,
    _seq,
    _sha,
    _urn,
    canonical_json,
    semantic_hash,
)

RELATION_M1_CONTRACT_ID = "M1_ADMITTED_FIELD_FORGE_RELATION_V554_INGRESS@1.0.0"
RELATION_BASIS_KIND = "ADMITTED_FIELD_FORGE_RELATION"
SIG_004 = "V554-SIG-004-NONTEMPORAL-ADMITTED-RELATION-EXACT"
RELATION_ADMISSION_SCHEMA = "PREV3_FIELD_FORGE_RELATION_ADMISSION@1.0.0"
RELATION_ADMISSION_REF_KIND = "PREV3_FIELD_FORGE_RELATION_ADMISSION"
RELATION_ADMISSION_POSITIVE_STATE = "ADMITTED"
RELATION_TEMPORAL_DISPOSITION = "NO_NEW_V553_TEMPORAL_MEANING_REQUIRED"
RELATION_INFORMATION_LOSS = "NONE__REFERENCE_PRESERVING"

RELATION_EQ_FIELDS = (
    "focal_structural_proposition_ref",
    "target_use",
    "v554_rule_id",
    "v554_rule_version",
    "v554_rule_hash",
    "basis_semantic_class",
    "rule_relevant_structural_semantic_identity_fingerprint",
    "relation_participant_role_order_cardinality_fingerprint",
    "native_scope_identity_fingerprint",
    "rule_relevant_effective_time_semantics_fingerprint",
    "originating_admitted_relation_lineage_fingerprint",
    "source_universe_fingerprint",
    "estimand_fingerprint",
    "measure_and_weight_authority_fingerprint",
    "rule_relevant_source_relation_comparability_authority_fingerprint",
    "interpretation_critical_semantic_authority_fingerprint",
)

RELATION_PROJECTION_SLOTS = (
    "relation_admission_ref",
    "relation_admission_authority_ref",
    "relation_admission_rule_ref",
    "relation_admission_decision_state",
    "field_forge_relation_ref",
    "relation_semantic_identity_refs",
    "relation_participant_role_order_cardinality_refs",
    "focal_structural_proposition_ref",
    "native_scope_identity_refs",
    "source_universe_refs",
    "risk_set_refs",
    "target_use_ref",
    "requested_downstream_owner_or_contract_family",
    "target_use_permission_refs",
    "effective_time_or_interval_refs_required_by_target_use",
    "estimand_refs",
    "measure_and_weight_authority_refs",
    "source_relation_comparability_authority_refs_where_required",
    "applicable_negative_denial_noncomparability_refs",
    "interpretation_critical_authority_refs",
    "producer_replay_locator_or_reference_root",
    "authority_current_selection_dependency_provenance_refs",
    "information_loss_declaration",
    "temporal_semantic_disposition",
)

_FORBIDDEN_RELATION_PATH_KEYS = frozenset(
    {
        "structural_empirical_admission_id",
        "structural_empirical_admission_content_hash",
        "originating_structural_empirical_admission_refs",
        "originating_structural_empirical_admission_lineage_fingerprint",
        "v553_object_id",
        "v553_object_content_hash",
        "v553_object_family",
        "v553_families",
        "scr553_request_ref",
        "scr553_decision_state",
    }
)


class RelationPreparationState(str, Enum):
    RELATION_BASIS_READY = "RELATION_BASIS_READY"
    VALID_EMPTY = "VALID_EMPTY"
    DENIED = "DENIED"
    DEFERRED_MISSING_AUTHORITY = "DEFERRED_MISSING_AUTHORITY"
    UNRESOLVED = "UNRESOLVED"
    NONCOMPARABLE = "NONCOMPARABLE"
    TARGET_USE_NOT_PERMITTED = "TARGET_USE_NOT_PERMITTED"
    TEMPORALIZATION_REQUIRED = "TEMPORALIZATION_REQUIRED"
    INTEGRITY_FAILURE = "INTEGRITY_FAILURE"


@dataclass(frozen=True)
class RelationBasisPreparation:
    state: RelationPreparationState
    reason: str
    candidate: Mapping[str, Any] | None
    blocker_refs: tuple[str, ...] = ()

    @property
    def ready(self) -> bool:
        return self.state is RelationPreparationState.RELATION_BASIS_READY


class RelationIngressIntegrity(ValueError):
    pass


class RelationEquivalenceUnknown(ValueError):
    pass


def _contains_forbidden_key(value: Any) -> str | None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if key in _FORBIDDEN_RELATION_PATH_KEYS:
                return key
            found = _contains_forbidden_key(item)
            if found:
                return found
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for item in value:
            found = _contains_forbidden_key(item)
            if found:
                return found
    return None


def _authority_ref(value: Any, name: str) -> dict[str, str]:
    """Normalize exact PRE553 or legacy relation-lane authority identity losslessly."""
    if isinstance(value, Pre553AuthorityRef):
        return {
            "authority_id": _nonempty(value.authority_id, f"{name}.authority_id"),
            "authority_version": _nonempty(
                value.authority_version, f"{name}.authority_version"
            ),
            "authority_content_hash": _sha(
                value.authority_content_hash, f"{name}.authority_content_hash"
            ),
        }
    if not isinstance(value, Mapping):
        raise RelationIngressIntegrity(f"{name} must be exact authority identity")
    if set(value) == {
        "authority_id", "authority_version", "authority_content_hash"
    }:
        return {
            "authority_id": _nonempty(value.get("authority_id"), f"{name}.authority_id"),
            "authority_version": _nonempty(
                value.get("authority_version"), f"{name}.authority_version"
            ),
            "authority_content_hash": _sha(
                value.get("authority_content_hash"),
                f"{name}.authority_content_hash",
            ),
        }
    if set(value) == {"id", "version", "hash"}:
        return {
            "authority_id": _nonempty(value.get("id"), f"{name}.id"),
            "authority_version": _nonempty(value.get("version"), f"{name}.version"),
            "authority_content_hash": _sha(value.get("hash"), f"{name}.hash"),
        }
    if set(value) == {"id", "version", "content_hash"}:
        return {
            "authority_id": _nonempty(value.get("id"), f"{name}.id"),
            "authority_version": _nonempty(value.get("version"), f"{name}.version"),
            "authority_content_hash": _sha(
                value.get("content_hash"), f"{name}.content_hash"
            ),
        }
    raise RelationIngressIntegrity(
        f"{name} must preserve exact authority id/version/hash fields"
    )


def _relation_exact_ref(value: Any, name: str) -> dict[str, str]:
    if isinstance(value, Pre553ExactRef):
        return {
            "kind": _nonempty(value.kind, f"{name}.kind"),
            "object_id": _nonempty(value.object_id, f"{name}.object_id"),
            "content_hash": _sha(value.content_hash, f"{name}.content_hash"),
        }
    return _exact_ref(value, name)


def _typed_identity(value: Any, name: str) -> Any:
    """Preserve exact typed identity; never reduce refs/authorities to labels."""
    if isinstance(value, str):
        return _nonempty(value, name)
    if isinstance(value, Pre553ExactRef):
        return _relation_exact_ref(value, name)
    if isinstance(value, Pre553AuthorityRef):
        return _authority_ref(value, name)
    if isinstance(value, Mapping):
        keys = set(value)
        if keys == {"kind", "object_id", "content_hash"}:
            return _relation_exact_ref(value, name)
        if keys in (
            {"authority_id", "authority_version", "authority_content_hash"},
            {"id", "version", "hash"},
            {"id", "version", "content_hash"},
        ):
            return _authority_ref(value, name)
        # Participant/closure material may itself be a typed canonical mapping.
        canonical_json(value)
        return dict(value)
    raise RelationIngressIntegrity(
        f"{name} must be exact string/ref/authority/canonical mapping identity"
    )


def _typed_sequence(value: Any, name: str) -> tuple[Any, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise RelationIngressIntegrity(f"{name} must be sequence")
    return tuple(_typed_identity(item, name) for item in value)


def _relation_eq(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise RelationEquivalenceUnknown("relation equivalence key missing")
    if set(value) != set(RELATION_EQ_FIELDS):
        raise RelationEquivalenceUnknown("relation equivalence key fields unresolved")
    out = dict(value)
    for key in RELATION_EQ_FIELDS:
        if out[key] in (None, "", [], {}):
            raise RelationEquivalenceUnknown(
                f"relation equivalence component unresolved: {key}"
            )
        canonical_json(out[key])
    if out["basis_semantic_class"] != RELATION_BASIS_KIND:
        raise RelationIngressIntegrity("relation equivalence basis_semantic_class mismatch")
    if out["target_use"] != TARGET_USE:
        raise RelationIngressIntegrity("relation equivalence target_use mismatch")
    return out


def _admission_ref(admission: Mapping[str, Any]) -> dict[str, str]:
    return {
        "kind": RELATION_ADMISSION_REF_KIND,
        "object_id": _nonempty(
            admission.get("field_forge_relation_admission_id"),
            "field_forge_relation_admission_id",
        ),
        "content_hash": _sha(
            admission.get("field_forge_relation_admission_content_hash"),
            "field_forge_relation_admission_content_hash",
        ),
    }


def _validate_positive_admission(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise RelationIngressIntegrity("relation_admission must be mapping")
    admission = dict(value)
    if (
        _nonempty(admission.get("schema_id"), "relation_admission.schema_id")
        != RELATION_ADMISSION_SCHEMA
    ):
        raise RelationIngressIntegrity("relation admission schema mismatch")
    if (
        _nonempty(admission.get("admission_decision_state"), "admission_decision_state")
        != RELATION_ADMISSION_POSITIVE_STATE
    ):
        raise RelationIngressIntegrity(
            "only positive ADMITTED relation admission may prepare M1 basis"
        )
    if _nonempty(admission.get("target_use_ref"), "target_use_ref") != TARGET_USE:
        raise RelationIngressIntegrity("relation admission target use mismatch")
    if (
        _nonempty(
            admission.get("requested_downstream_owner_or_contract_family"),
            "requested_downstream_owner_or_contract_family",
        )
        != RELATION_M1_CONTRACT_ID
    ):
        raise RelationIngressIntegrity(
            "relation admission is not bound to exact relation M1 ingress contract"
        )
    _admission_ref(admission)
    _relation_exact_ref(
        admission.get("field_forge_relation_ref"), "field_forge_relation_ref"
    )
    _nonempty(admission.get("relation_owner_ref_or_id"), "relation_owner_ref_or_id")
    _typed_identity(admission.get("relation_rule_ref"), "relation_rule_ref")
    _nonempty(admission.get("relation_typed_state"), "relation_typed_state")
    _authority_ref(admission.get("admission_authority_ref"), "admission_authority_ref")
    _typed_identity(admission.get("admission_rule_ref"), "admission_rule_ref")
    if (
        _nonempty(
            admission.get("relation_information_loss_declaration"),
            "relation_information_loss_declaration",
        )
        != RELATION_INFORMATION_LOSS
    ):
        raise RelationIngressIntegrity(
            "GT2 relation admission must preserve NONE__REFERENCE_PRESERVING"
        )
    return admission


def make_nonpositive_relation_basis_preparation(
    state: RelationPreparationState | str,
    reason: str,
    *,
    blocker_refs: Sequence[str] = (),
) -> RelationBasisPreparation:
    """Preserve a lawful upstream preparation state without laundering it."""
    try:
        typed = RelationPreparationState(state)
    except ValueError as exc:
        raise RelationIngressIntegrity("unknown relation preparation state") from exc
    if typed is RelationPreparationState.RELATION_BASIS_READY:
        raise RelationIngressIntegrity(
            "positive preparation must be created from an exact admitted relation"
        )
    clean_reason = _nonempty(reason, "reason")
    refs = (
        tuple(sorted(set(_seq(tuple(blocker_refs), "blocker_refs"))))
        if blocker_refs
        else ()
    )
    return RelationBasisPreparation(typed, clean_reason, None, refs)


def prepare_admitted_field_forge_relation_basis(payload: Any) -> RelationBasisPreparation:
    """Validate one exact positive relation-admission projection for SIG-004.

    This is a compatibility preparation step only. It creates no admission,
    temporal, empirical, publication, or actor authority.
    """
    try:
        if not isinstance(payload, Mapping):
            raise RelationIngressIntegrity(
                "relation basis preparation payload must be mapping"
            )
        forbidden = _contains_forbidden_key(payload)
        if forbidden:
            raise RelationIngressIntegrity(
                f"forbidden empirical/V553 coercion key on relation path: {forbidden}"
            )
        admission = _validate_positive_admission(payload.get("relation_admission"))
        basis_ref = _relation_exact_ref(payload.get("basis_ref"), "basis_ref")
        expected_basis_ref = {
            "kind": RELATION_BASIS_KIND,
            "object_id": _admission_ref(admission)["object_id"],
            "content_hash": _admission_ref(admission)["content_hash"],
        }
        if basis_ref != expected_basis_ref:
            raise RelationIngressIntegrity(
                "relation basis ref must preserve exact admitted-relation identity/hash"
            )
        projection = payload.get("projection")
        if not isinstance(projection, Mapping):
            raise RelationIngressIntegrity("relation projection must be mapping")
        projection = dict(projection)
        if set(projection) != set(RELATION_PROJECTION_SLOTS):
            missing = sorted(set(RELATION_PROJECTION_SLOTS) - set(projection))
            extra = sorted(set(projection) - set(RELATION_PROJECTION_SLOTS))
            raise RelationIngressIntegrity(
                f"relation projection fields mismatch missing={missing!r} extra={extra!r}"
            )
        if semantic_hash(projection) != _sha(
            payload.get("projection_hash"), "projection_hash"
        ):
            raise RelationIngressIntegrity("relation projection hash mismatch")

        if (
            _relation_exact_ref(
                projection["relation_admission_ref"],
                "projection.relation_admission_ref",
            )
            != _admission_ref(admission)
        ):
            raise RelationIngressIntegrity("projection relation admission ref mismatch")
        if _authority_ref(
            projection["relation_admission_authority_ref"],
            "projection.relation_admission_authority_ref",
        ) != _authority_ref(
            admission["admission_authority_ref"],
            "admission.admission_authority_ref",
        ):
            raise RelationIngressIntegrity(
                "projection relation admission authority mismatch"
            )
        if _typed_identity(
            projection["relation_admission_rule_ref"],
            "projection.relation_admission_rule_ref",
        ) != _typed_identity(
            admission["admission_rule_ref"], "admission.admission_rule_ref"
        ):
            raise RelationIngressIntegrity("projection relation admission rule mismatch")
        if (
            _nonempty(
                projection["relation_admission_decision_state"],
                "projection.relation_admission_decision_state",
            )
            != RELATION_ADMISSION_POSITIVE_STATE
        ):
            raise RelationIngressIntegrity("projection admission decision is not ADMITTED")
        if _relation_exact_ref(
            projection["field_forge_relation_ref"],
            "projection.field_forge_relation_ref",
        ) != _relation_exact_ref(
            admission["field_forge_relation_ref"], "admission.field_forge_relation_ref"
        ):
            raise RelationIngressIntegrity("projection FIELD FORGE relation ref mismatch")
        if _nonempty(projection["target_use_ref"], "projection.target_use_ref") != TARGET_USE:
            raise RelationIngressIntegrity("projection target use mismatch")
        if (
            _nonempty(
                projection["requested_downstream_owner_or_contract_family"],
                "projection.requested_downstream_owner_or_contract_family",
            )
            != RELATION_M1_CONTRACT_ID
        ):
            raise RelationIngressIntegrity("projection downstream contract mismatch")
        if (
            _nonempty(
                projection["information_loss_declaration"],
                "projection.information_loss_declaration",
            )
            != RELATION_INFORMATION_LOSS
        ):
            raise RelationIngressIntegrity(
                "relation basis projection widened information-loss declaration"
            )
        if (
            _nonempty(
                projection["temporal_semantic_disposition"],
                "projection.temporal_semantic_disposition",
            )
            != RELATION_TEMPORAL_DISPOSITION
        ):
            return RelationBasisPreparation(
                RelationPreparationState.TEMPORALIZATION_REQUIRED,
                "SIG-004 cannot fabricate or coerce V553 temporal meaning",
                None,
                (),
            )

        _typed_sequence(
            projection["relation_semantic_identity_refs"],
            "relation_semantic_identity_refs",
        )
        participants = _typed_sequence(
            projection["relation_participant_role_order_cardinality_refs"],
            "relation_participant_role_order_cardinality_refs",
        )
        if not participants:
            raise RelationIngressIntegrity(
                "relation participant role/order/cardinality identity required"
            )
        scopes = _typed_sequence(
            projection["native_scope_identity_refs"], "native_scope_identity_refs"
        )
        if not scopes:
            raise RelationIngressIntegrity("native scope identity required")
        universes = _typed_sequence(
            projection["source_universe_refs"], "source_universe_refs"
        )
        if not universes:
            raise RelationIngressIntegrity("source universe identity required")
        risks = _typed_sequence(projection["risk_set_refs"], "risk_set_refs")
        if not risks:
            raise RelationIngressIntegrity("risk-set identity required")
        permissions = _typed_sequence(
            projection["target_use_permission_refs"], "target_use_permission_refs"
        )
        if not permissions:
            raise RelationIngressIntegrity("target-use permission refs required")
        _typed_sequence(
            projection["effective_time_or_interval_refs_required_by_target_use"],
            "effective_time_or_interval_refs_required_by_target_use",
        )
        _typed_sequence(projection["estimand_refs"], "estimand_refs")
        _typed_sequence(
            projection["measure_and_weight_authority_refs"],
            "measure_and_weight_authority_refs",
        )
        _typed_sequence(
            projection["source_relation_comparability_authority_refs_where_required"],
            "source_relation_comparability_authority_refs_where_required",
        )
        _typed_sequence(
            projection["applicable_negative_denial_noncomparability_refs"],
            "applicable_negative_denial_noncomparability_refs",
        )
        _typed_sequence(
            projection["interpretation_critical_authority_refs"],
            "interpretation_critical_authority_refs",
        )
        closure_refs = _typed_sequence(
            projection["authority_current_selection_dependency_provenance_refs"],
            "authority_current_selection_dependency_provenance_refs",
        )
        if not closure_refs:
            raise RelationIngressIntegrity(
                "authority/currentness/dependency/provenance closure required"
            )
        _typed_identity(
            projection["producer_replay_locator_or_reference_root"],
            "producer_replay_locator_or_reference_root",
        )
        if _nonempty(
            projection["focal_structural_proposition_ref"],
            "projection.focal_structural_proposition_ref",
        ) != _nonempty(
            payload.get("focal_structural_proposition_ref"),
            "focal_structural_proposition_ref",
        ):
            raise RelationIngressIntegrity(
                "projection focal structural proposition mismatch"
            )

        shared_sequence_fields = (
            "relation_semantic_identity_refs",
            "relation_participant_role_order_cardinality_refs",
            "native_scope_identity_refs",
            "source_universe_refs",
            "risk_set_refs",
            "target_use_permission_refs",
            "effective_time_or_interval_refs_required_by_target_use",
            "estimand_refs",
            "measure_and_weight_authority_refs",
            "source_relation_comparability_authority_refs_where_required",
            "applicable_negative_denial_noncomparability_refs",
            "interpretation_critical_authority_refs",
            "authority_current_selection_dependency_provenance_refs",
        )
        for field in shared_sequence_fields:
            projected = _typed_sequence(projection[field], field)
            admitted = _typed_sequence(admission.get(field, ()), field)
            if semantic_hash(list(projected)) != semantic_hash(list(admitted)):
                raise RelationIngressIntegrity(
                    f"projection/admission exact sequence mismatch: {field}"
                )
        if _typed_identity(
            projection["producer_replay_locator_or_reference_root"],
            "projection.producer_replay_locator_or_reference_root",
        ) != _typed_identity(
            admission.get("producer_replay_locator_or_reference_root"),
            "admission.producer_replay_locator_or_reference_root",
        ):
            raise RelationIngressIntegrity("projection/admission replay root mismatch")

        eq = _relation_eq(payload.get("equivalence_key"))
        if (
            eq["focal_structural_proposition_ref"]
            != projection["focal_structural_proposition_ref"]
        ):
            raise RelationIngressIntegrity(
                "equivalence/projection focal proposition mismatch"
            )
        expected_fingerprints = {
            "rule_relevant_structural_semantic_identity_fingerprint": semantic_hash(
                list(_typed_sequence(
                    projection["relation_semantic_identity_refs"],
                    "relation_semantic_identity_refs",
                ))
            ),
            "relation_participant_role_order_cardinality_fingerprint": semantic_hash(
                list(_typed_sequence(
                    projection["relation_participant_role_order_cardinality_refs"],
                    "relation_participant_role_order_cardinality_refs",
                ))
            ),
            "native_scope_identity_fingerprint": semantic_hash(
                list(_typed_sequence(
                    projection["native_scope_identity_refs"],
                    "native_scope_identity_refs",
                ))
            ),
            "rule_relevant_effective_time_semantics_fingerprint": semantic_hash(
                {
                    "disposition": projection["temporal_semantic_disposition"],
                    "refs": list(
                        projection[
                            "effective_time_or_interval_refs_required_by_target_use"
                        ]
                    ),
                }
            ),
            "originating_admitted_relation_lineage_fingerprint": semantic_hash(
                projection["relation_admission_ref"]
            ),
            "source_universe_fingerprint": semantic_hash(
                list(_typed_sequence(
                    projection["source_universe_refs"],
                    "source_universe_refs",
                ))
            ),
            "estimand_fingerprint": semantic_hash(list(_typed_sequence(
                projection["estimand_refs"], "estimand_refs"
            ))),
            "measure_and_weight_authority_fingerprint": semantic_hash(
                list(_typed_sequence(
                    projection["measure_and_weight_authority_refs"],
                    "measure_and_weight_authority_refs",
                ))
            ),
            "rule_relevant_source_relation_comparability_authority_fingerprint": semantic_hash(
                list(_typed_sequence(
                    projection[
                        "source_relation_comparability_authority_refs_where_required"
                    ],
                    "source_relation_comparability_authority_refs_where_required",
                ))
            ),
            "interpretation_critical_semantic_authority_fingerprint": semantic_hash(
                list(_typed_sequence(
                    projection["interpretation_critical_authority_refs"],
                    "interpretation_critical_authority_refs",
                ))
            ),
        }
        for field, expected in expected_fingerprints.items():
            if eq[field] != expected:
                raise RelationIngressIntegrity(
                    f"relation equivalence fingerprint mismatch: {field}"
                )

        semantics = payload.get("selected_rule_relevant_basis_semantics")
        if semantics in (None, "", [], {}):
            raise RelationIngressIntegrity(
                "selected rule-relevant relation basis semantics missing"
            )
        canonical_json(semantics)

        candidate = {
            "basis_kind": RELATION_BASIS_KIND,
            "basis_ref": basis_ref,
            "projection": projection,
            "projection_hash": semantic_hash(projection),
            "equivalence_key": eq,
            "selected_rule_relevant_basis_semantics": semantics,
        }
        return RelationBasisPreparation(
            RelationPreparationState.RELATION_BASIS_READY,
            "exact positive admitted FIELD FORGE relation basis prepared for SIG-004",
            candidate,
            (),
        )
    except RelationEquivalenceUnknown as exc:
        return RelationBasisPreparation(
            RelationPreparationState.INTEGRITY_FAILURE, str(exc), None, ()
        )
    except (RelationIngressIntegrity, TypeError, ValueError, KeyError) as exc:
        return RelationBasisPreparation(
            RelationPreparationState.INTEGRITY_FAILURE,
            str(exc) or "invalid relation basis preparation",
            None,
            (),
        )


_PREPARATION_TO_M1_STATE = {
    RelationPreparationState.VALID_EMPTY: M1DecisionState.VALID_EMPTY,
    RelationPreparationState.DENIED: M1DecisionState.INELIGIBLE_EXPLICIT_DENIAL,
    RelationPreparationState.DEFERRED_MISSING_AUTHORITY: M1DecisionState.INELIGIBLE_MISSING_REQUIRED_AUTHORITY,
    RelationPreparationState.UNRESOLVED: M1DecisionState.INELIGIBLE_UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY,
    RelationPreparationState.NONCOMPARABLE: M1DecisionState.INELIGIBLE_UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY,
    RelationPreparationState.TARGET_USE_NOT_PERMITTED: M1DecisionState.INELIGIBLE_EXPLICIT_DENIAL,
    RelationPreparationState.TEMPORALIZATION_REQUIRED: M1DecisionState.INELIGIBLE_TEMPORAL_SIGNATURE,
    RelationPreparationState.INTEGRITY_FAILURE: M1DecisionState.INTEGRITY_FAILURE,
}

_PREPARATION_PRECEDENCE = (
    RelationPreparationState.INTEGRITY_FAILURE,
    RelationPreparationState.DENIED,
    RelationPreparationState.TARGET_USE_NOT_PERMITTED,
    RelationPreparationState.TEMPORALIZATION_REQUIRED,
    RelationPreparationState.DEFERRED_MISSING_AUTHORITY,
    RelationPreparationState.NONCOMPARABLE,
    RelationPreparationState.UNRESOLVED,
    RelationPreparationState.VALID_EMPTY,
)


def _blocked_preparation_m1_state(
    preparations: Sequence[RelationBasisPreparation],
) -> M1DecisionState:
    states = {item.state for item in preparations if not item.ready}
    for state in _PREPARATION_PRECEDENCE:
        if state in states:
            return _PREPARATION_TO_M1_STATE[state]
    return M1DecisionState.INELIGIBLE_UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY


def _parse_invocation(
    *,
    governed_use_id: str,
    v554_rule_ref: Mapping[str, Any],
    focal_structural_proposition_ref: str,
    required_authority_snapshot_refs: Sequence[str],
    authority_bundle_material: Mapping[str, Any],
    producer_reference_spine_fingerprint: str,
    conditions: Sequence[Mapping[str, Any]],
    publication_authority: Mapping[str, Any] | None,
) -> dict[str, Any]:
    use = _nonempty(governed_use_id, "governed_use_id")
    rule = _rule(v554_rule_ref)
    prop = _nonempty(
        focal_structural_proposition_ref, "focal_structural_proposition_ref"
    )
    snapshots = tuple(
        sorted(
            set(
                _seq(
                    required_authority_snapshot_refs,
                    "required_authority_snapshot_refs",
                )
            )
        )
    )
    if not snapshots:
        raise RelationIngressIntegrity("required authority snapshot refs missing")
    if not isinstance(authority_bundle_material, Mapping) or not authority_bundle_material:
        raise RelationIngressIntegrity("authority_bundle_material required")
    canonical_json(authority_bundle_material)
    parsed_conditions = tuple(_condition(item) for item in conditions)
    return {
        "use": use,
        "rule": rule,
        "sig": SIG_004,
        "prop": prop,
        "origins": (),
        "snapshots": snapshots,
        "conditions": parsed_conditions,
        "auth": dict(authority_bundle_material),
        "spine": _nonempty(
            producer_reference_spine_fingerprint,
            "producer_reference_spine_fingerprint",
        ),
        "publication": _publication(publication_authority),
    }


def _failure(
    state: M1DecisionState,
    reason: str,
    *,
    governed_use_id: str = "",
    rejected: Sequence[str] = (),
) -> M1Evaluation:
    return M1Evaluation(
        RELATION_M1_CONTRACT_ID,
        state,
        reason,
        governed_use_id,
        RELATION_BASIS_KIND,
        0,
        None,
        None,
        (),
        None,
        None,
        tuple(sorted(set(rejected))),
    )


def evaluate_m1_admitted_field_forge_relation_v554(
    *,
    governed_use_id: str,
    v554_rule_ref: Mapping[str, Any],
    focal_structural_proposition_ref: str,
    preparations: Sequence[RelationBasisPreparation],
    required_authority_snapshot_refs: Sequence[str],
    authority_bundle_material: Mapping[str, Any],
    producer_reference_spine_fingerprint: str,
    conditions: Sequence[Mapping[str, Any]] = (),
    publication_authority: Mapping[str, Any] | None = None,
    reference_only_basis_refs: Sequence[str] = (),
) -> M1Evaluation:
    """Evaluate exact non-temporal admitted-relation support at V554.

    No temporal/V553 path exists in this contract. Non-ready preparation
    objects remain typed preparation outcomes and are never silently converted
    to coherent M1 VALID_EMPTY.
    """
    try:
        i = _parse_invocation(
            governed_use_id=governed_use_id,
            v554_rule_ref=v554_rule_ref,
            focal_structural_proposition_ref=focal_structural_proposition_ref,
            required_authority_snapshot_refs=required_authority_snapshot_refs,
            authority_bundle_material=authority_bundle_material,
            producer_reference_spine_fingerprint=producer_reference_spine_fingerprint,
            conditions=conditions,
            publication_authority=publication_authority,
        )
        if isinstance(preparations, (str, bytes)) or not isinstance(
            preparations, Sequence
        ):
            raise RelationIngressIntegrity("preparations must be sequence")
        if any(not isinstance(item, RelationBasisPreparation) for item in preparations):
            raise RelationIngressIntegrity(
                "preparations must contain exact RelationBasisPreparation values"
            )
        blocked = [item for item in preparations if not item.ready]
        if blocked:
            states = ",".join(item.state.value for item in blocked)
            reasons = "; ".join(item.reason for item in blocked)
            return _failure(
                _blocked_preparation_m1_state(blocked),
                f"typed relation preparation not ready [{states}]: {reasons}",
                governed_use_id=i["use"],
                rejected=reference_only_basis_refs,
            )

        block = _block_for_conditions(i["conditions"])
        if block:
            f2 = _f2(i["conditions"], None) if i["conditions"] else ()
            i["origins"] = tuple(
                sorted(
                    {
                        item.candidate["projection"]["relation_admission_ref"][
                            "object_id"
                        ]
                        for item in preparations
                        if item.candidate is not None
                    }
                )
            )
            b1 = _b1(i, block, None, f2) if f2 else None
            return M1Evaluation(
                RELATION_M1_CONTRACT_ID,
                block,
                "producer-governed hard negative/static authority blocks relation F1",
                i["use"],
                RELATION_BASIS_KIND,
                0,
                None,
                None,
                f2,
                b1,
                _handoff(i, None, f2, b1) if f2 else None,
                tuple(sorted(set(reference_only_basis_refs))),
            )

        if not preparations:
            return _failure(
                M1DecisionState.VALID_EMPTY,
                "coherent zero relation basis candidates; no filler",
                governed_use_id=i["use"],
                rejected=reference_only_basis_refs,
            )

        candidates = [
            dict(item.candidate)
            for item in preparations
            if item.candidate is not None
        ]
        for candidate in candidates:
            if candidate["basis_kind"] != RELATION_BASIS_KIND:
                raise RelationIngressIntegrity(
                    "non-relation basis may not count under SIG-004"
                )
            eq = candidate["equivalence_key"]
            if (
                eq["focal_structural_proposition_ref"] != i["prop"]
                or eq["target_use"] != TARGET_USE
                or eq["v554_rule_id"] != i["rule"]["id"]
                or eq["v554_rule_version"] != i["rule"]["version"]
                or eq["v554_rule_hash"] != i["rule"]["hash"]
                or eq["basis_semantic_class"] != RELATION_BASIS_KIND
            ):
                raise RelationIngressIntegrity(
                    "relation candidate/invocation binding mismatch"
                )
            projection = candidate["projection"]
            if (
                projection["temporal_semantic_disposition"]
                != RELATION_TEMPORAL_DISPOSITION
            ):
                return _failure(
                    M1DecisionState.INELIGIBLE_TEMPORAL_SIGNATURE,
                    "SIG-004 requires no new V553-owned temporal meaning",
                    governed_use_id=i["use"],
                    rejected=reference_only_basis_refs,
                )

        groups: dict[str, list[Mapping[str, Any]]] = {}
        for candidate in candidates:
            groups.setdefault(
                semantic_hash(candidate["equivalence_key"]), []
            ).append(candidate)

        eligible: list[
            tuple[Mapping[str, Any], list[Mapping[str, Any]]]
        ] = []
        rejected = list(reference_only_basis_refs)
        for key in sorted(groups):
            group = groups[key]
            if (
                len(
                    {
                        semantic_hash(
                            item["selected_rule_relevant_basis_semantics"]
                        )
                        for item in group
                    }
                )
                != 1
            ):
                return _failure(
                    M1DecisionState.EQUIVALENCE_UNKNOWN,
                    "equivalent relation candidates disagree on rule-relevant semantics",
                    governed_use_id=i["use"],
                    rejected=rejected,
                )
            eligible.append((group[0]["equivalence_key"], group))

        if len(eligible) != 1:
            rejected.extend(
                candidate["basis_ref"]["object_id"]
                for _, group in eligible
                for candidate in group
            )
            return _failure(
                M1DecisionState.INELIGIBLE_UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY,
                "multiple distinct admitted-relation basis groups; no winner heuristic",
                governed_use_id=i["use"],
                rejected=rejected,
            )

        eq, counting = eligible[0]
        semantics = counting[0]["selected_rule_relevant_basis_semantics"]
        basis_material = {
            "equivalence_key": eq,
            "required_basis_kind": RELATION_BASIS_KIND,
            "selected_rule_relevant_basis_semantics": semantics,
        }
        basis_id = _urn("v554:basis", basis_material)
        authority_fp = semantic_hash(
            {
                "scr554_contract": SCR554_CONTRACT_ID,
                "m1_contract": RELATION_M1_CONTRACT_ID,
                "v554_rule_ref": i["rule"],
                "signature_id": SIG_004,
                "selected_basis_semantic_identity": basis_id,
                "required_authority_snapshot_refs": list(i["snapshots"]),
                "external_authority_bundle_material": i["auth"],
            }
        )
        f1_material = {
            "contract_version": "1.0.0",
            "equivalence_key": eq,
            "canonical_basis_semantic_id": basis_id,
            "rule_id": i["rule"]["id"],
            "rule_version": i["rule"]["version"],
            "rule_hash": i["rule"]["hash"],
            "signature_id": SIG_004,
            "target_use": TARGET_USE,
            "authority_bundle_fingerprint": authority_fp,
        }
        f1_id = _urn("v554:f1", f1_material)
        exact_basis_refs = sorted(
            (candidate["basis_ref"] for candidate in counting),
            key=canonical_json,
        )
        exact_admission_refs = sorted(
            (
                candidate["projection"]["relation_admission_ref"]
                for candidate in counting
            ),
            key=canonical_json,
        )
        exact_relation_refs = sorted(
            (
                candidate["projection"]["field_forge_relation_ref"]
                for candidate in counting
            ),
            key=canonical_json,
        )
        lineage_closure_fingerprint = semantic_hash({
            "basis_refs": exact_basis_refs,
            "admission_refs": exact_admission_refs,
            "field_forge_relation_refs": exact_relation_refs,
        })
        f1 = {
            "family": "F1",
            "state": "ELIGIBLE",
            "f1_id": f1_id,
            "canonical_basis_semantic_id": basis_id,
            "provenance_alias_refs": sorted(
                {candidate["basis_ref"]["object_id"] for candidate in counting}
            ),
            "provenance_alias_exact_refs": exact_basis_refs,
            "originating_relation_admission_exact_refs": exact_admission_refs,
            "originating_field_forge_relation_exact_refs": exact_relation_refs,
            "lineage_closure_fingerprint": lineage_closure_fingerprint,
            "authority_bundle_fingerprint": authority_fp,
            "material": f1_material,
        }

        i["origins"] = tuple(
            sorted(
                {
                    candidate["projection"]["relation_admission_ref"]["object_id"]
                    for candidate in counting
                }
            )
        )
        f2 = _f2(i["conditions"], f1_id)
        b1 = _b1(i, M1DecisionState.ELIGIBLE, f1_id, f2)
        handoff = _handoff(i, f1, f2, b1)
        return M1Evaluation(
            RELATION_M1_CONTRACT_ID,
            M1DecisionState.ELIGIBLE,
            "all frozen relation-specific M1 gates passed",
            i["use"],
            RELATION_BASIS_KIND,
            1,
            basis_id,
            f1,
            f2,
            b1,
            handoff,
            tuple(sorted(set(rejected))),
        )
    except RelationEquivalenceUnknown as exc:
        return _failure(
            M1DecisionState.EQUIVALENCE_UNKNOWN,
            str(exc),
            governed_use_id=governed_use_id if isinstance(governed_use_id, str) else "",
            rejected=reference_only_basis_refs,
        )
    except (RelationIngressIntegrity, TypeError, ValueError, KeyError) as exc:
        return _failure(
            M1DecisionState.INTEGRITY_FAILURE,
            str(exc) or "invalid relation-specific M1 invocation",
            governed_use_id=governed_use_id if isinstance(governed_use_id, str) else "",
            rejected=reference_only_basis_refs,
        )
